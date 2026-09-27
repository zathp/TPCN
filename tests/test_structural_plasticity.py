from tpcn.event_runtime import Event, EventQueue
from tpcn.structural_plasticity import CandidateEvidence, StructuralPlasticityController
from tpcn.topology import BoundedTopology


def evidence(source, destination, score, evidence_id=""):
    return CandidateEvidence(source, source, destination, score, 2.0, evidence_id)


def make_controller(candidate_capacity=4):
    topology = BoundedTopology(("a", "b", "c", "d"), fan_in_limit=1, fan_out_limit=1, edge_capacity=2)
    return StructuralPlasticityController(topology, candidate_capacity=candidate_capacity)


def test_selection_is_local_deterministic_and_tie_breaks_by_endpoint():
    controller = make_controller()
    selected = controller.select((evidence("a", "c", 1.0, "z"), evidence("a", "b", 1.0, "a")))
    assert selected.destination == "b"


def test_locality_and_duplicate_rejection_are_explicit():
    controller = make_controller()
    try:
        controller.submit(CandidateEvidence("b", "a", "c", 1.0, 1.0))
    except ValueError as error:
        assert "source" in str(error)
    else:
        raise AssertionError("non-local evidence was accepted")
    assert controller.grow(evidence("a", "b", 1.0)).status == "grown"
    assert controller.grow(evidence("a", "b", 2.0)).status == "duplicate"


def test_growth_respects_fan_out_and_edge_capacity():
    controller = make_controller()
    assert controller.grow(evidence("a", "b", 1.0)).status == "grown"
    assert controller.grow(evidence("a", "c", 2.0)).status == "full_capacity"
    assert controller.state.edge_count == 1


def test_growth_respects_fan_in_limit_and_empty_adaptation_is_rejected():
    controller = make_controller()
    assert controller.grow(evidence("c", "b", 1.0)).status == "grown"
    assert controller.grow(evidence("a", "b", 2.0)).status == "full_capacity"
    assert controller.adapt(()).status == "rejected"
    assert controller.prune("a", "d").status == "rejected"


def test_candidate_storage_is_bounded_and_full_capacity_is_reported():
    controller = make_controller(candidate_capacity=1)
    assert controller.submit(evidence("a", "b", 1.0)).status == "accepted"
    assert controller.submit(evidence("c", "d", 1.0)).status == "full_capacity"
    assert controller.state.candidate_count == 1
    assert controller.state.routing_capacity == 2


def test_pruning_preserves_in_flight_event_and_removes_future_route():
    controller = make_controller()
    controller.grow(evidence("a", "b", 1.0))
    queue = EventQueue[Event](capacity=4)
    queued = controller.topology.route(Event(1.0, "a", "a", "signal", "payload"), queue)
    assert len(queued) == 1
    assert controller.prune("a", "b").status == "pruned"
    assert len(controller.topology) == 0
    assert queue.pop_ready(3.0).destination == "b"
    assert controller.topology.route(Event(4.0, "a", "a", "signal", "payload"), queue) == ()


def test_replay_produces_identical_bounded_state_and_routing():
    candidates = (evidence("a", "b", 1.0), evidence("c", "d", 2.0))
    left = make_controller()
    right = make_controller()
    assert left.adapt(candidates).edge == right.adapt(candidates).edge
    assert left.state == right.state
    assert tuple(left.topology.edges) == tuple(right.topology.edges)


def test_explicit_local_neighborhood_rejects_non_local_growth():
    topology = BoundedTopology(("a", "b", "c"), fan_in_limit=2, fan_out_limit=2, edge_capacity=4)
    controller = StructuralPlasticityController(topology, local_neighbors={"a": ("b",), "b": ("c",)})
    assert controller.grow(evidence("a", "c", 2.0)).status == "rejected"
    assert controller.grow(evidence("a", "b", 1.0)).status == "grown"


def test_batch_growth_is_bounded_and_atomic_on_capacity_failure():
    topology = BoundedTopology(("a", "b", "c"), fan_in_limit=2, fan_out_limit=2, edge_capacity=1)
    controller = StructuralPlasticityController(topology, max_growth_per_adaptation=2)
    results = controller.adapt_many((evidence("a", "b", 2.0), evidence("b", "c", 1.0)))
    assert [result.status for result in results] == ["full_capacity", "full_capacity"]
    assert len(controller.topology) == 0


def test_batch_growth_replay_uses_stable_score_and_endpoint_order():
    candidates = (evidence("b", "c", 1.0, "z"), evidence("a", "b", 1.0, "a"), evidence("a", "c", 2.0, "top"))
    left = StructuralPlasticityController(
        BoundedTopology(("a", "b", "c"), fan_in_limit=2, fan_out_limit=2, edge_capacity=3),
        max_growth_per_adaptation=2,
    )
    right = StructuralPlasticityController(
        BoundedTopology(("a", "b", "c"), fan_in_limit=2, fan_out_limit=2, edge_capacity=3),
        max_growth_per_adaptation=2,
    )
    assert tuple(result.edge for result in left.adapt_many(candidates)) == tuple(result.edge for result in right.adapt_many(candidates))
    assert tuple(left.topology.edges) == tuple(right.topology.edges)


def test_pruning_is_deterministic_and_respects_minimum_retention():
    topology = BoundedTopology.from_edges(
        ("a", "b", "c"),
        (("a", "b", 1.0), ("b", "c", 2.0)),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=3,
    )
    controller = StructuralPlasticityController(topology, minimum_edge_count=1)
    results = controller.prune_by_score({("a", "b"): 0.5, ("b", "c"): 0.5}, maximum=2)
    assert len(results) == 1
    assert results[0].edge.source == "a"
    assert controller.prune("b", "c").status == "retention_limit"


def test_repeated_adaptation_keeps_candidate_and_topology_state_bounded():
    controller = StructuralPlasticityController(
        BoundedTopology(("a", "b", "c", "d"), fan_in_limit=2, fan_out_limit=2, edge_capacity=4),
        candidate_capacity=2,
        max_growth_per_adaptation=1,
    )
    for index in range(20):
        source, destination = (("a", "b"), ("c", "d"))[index % 2]
        controller.submit(evidence(source, destination, float(index)))
        controller.adapt_many((evidence(source, destination, float(index)),))
        assert controller.state.candidate_count <= 2
        assert controller.state.edge_count <= 4
    assert controller.state.candidate_capacity == 2


def test_separate_controllers_do_not_share_locality_or_candidate_state():
    first = StructuralPlasticityController(
        BoundedTopology(("a", "b"), fan_in_limit=1, fan_out_limit=1, edge_capacity=1),
        local_neighbors={"a": ("b",)},
    )
    second = StructuralPlasticityController(
        BoundedTopology(("a", "b"), fan_in_limit=1, fan_out_limit=1, edge_capacity=1),
        local_neighbors={"a": ()},
    )
    assert first.submit(evidence("a", "b", 1.0)).status == "accepted"
    assert second.state.candidate_count == 0
    assert second.grow(evidence("a", "b", 1.0)).status == "rejected"