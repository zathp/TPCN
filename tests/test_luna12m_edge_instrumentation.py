from tpcn.edge_instrumentation import EdgeInstrumentation, run_competing_path_fixture
from tpcn.event_runtime import Event
from tpcn.structural_plasticity import MutationResult
from tpcn.structural_plasticity import CandidateEvidence, StructuralPlasticityController
from tpcn.topology import Edge
from tpcn.topology import BoundedTopology


def test_remove_and_recreate_edge_gets_a_new_generation() -> None:
    observer = EdgeInstrumentation()
    first = Edge("a", "b", 1.0)
    observer.register_edge(first, timestamp=2.0)
    observer.mutation(MutationResult("pruned", first), timestamp=4.0, edge=first)
    second = Edge("a", "b", 0.5)
    observer.register_edge(second, timestamp=7.0)

    identities = [row["identity"] for row in observer.snapshot()["edges"]]
    assert identities == [
        {"source": "a", "destination": "b", "generation": 0},
        {"source": "a", "destination": "b", "generation": 1},
    ]


def test_per_edge_traffic_and_first_last_use_are_recorded() -> None:
    observer = EdgeInstrumentation()
    edge = Edge("a", "b", 1.5)
    observer.register_edge(edge)
    observer.record_route(edge, Event(2.0, "a", "a", "signal", 1.0),
                          Event(3.5, "a", "b", "signal", 1.0))
    observer.record_route(edge, Event(5.0, "a", "a", "signal", 1.0),
                          Event(6.5, "a", "b", "signal", 1.0))

    row = observer.snapshot()["edges"][0]
    assert row["traffic_count"] == 2
    assert row["first_use"] == 2.0
    assert row["last_use"] == 5.0
    assert observer.snapshot()["traffic"][0]["arrival_timestamp"] == 3.5


def test_bounds_saturate_counters_and_ring_buffers() -> None:
    observer = EdgeInstrumentation(max_lifecycle_records=2, max_traffic_records=2, counter_limit=2)
    edge = Edge("a", "b", 1.0)
    observer.register_edge(edge)
    for timestamp in (1.0, 2.0, 3.0):
        observer.record_route(edge, Event(timestamp, "a", "a", "signal", 1.0),
                              Event(timestamp + 1.0, "a", "b", "signal", 1.0))

    snapshot = observer.snapshot()
    assert snapshot["edges"][0]["traffic_count"] == 2
    assert len(snapshot["traffic"]) == 2
    assert len(snapshot["lifecycle"]) <= 2


def test_competing_path_fixture_exposes_old_and_new_route_lifecycle() -> None:
    artifact = run_competing_path_fixture()
    edges = {(
        row["identity"]["source"], row["identity"]["destination"]): row
        for row in artifact["edges"]
    }
    assert edges[("source", "mid")]["traffic_count"] > 0
    assert edges[("source", "target")]["traffic_count"] > 0
    assert artifact["mutations"] == {"accepted": "grown", "rejected": "nonlocal", "pruned": "pruned"}
    assert artifact["rejection_results"] == {
        "candidate_capacity": "candidate_capacity",
        "duplicate": "duplicate",
        "edge_capacity": "edge_capacity",
        "fan_in_full": "fan_in_full",
        "fan_out_full": "fan_out_full",
    }
    rejection_reasons = {
        item["reason"] for item in artifact["lifecycle"]
        if item["kind"] == "candidate_rejected"
    }
    assert {"duplicate", "nonlocal", "fan_in_full", "fan_out_full",
            "edge_capacity", "candidate_capacity"} <= rejection_reasons
    assert any(item["kind"] == "edge_pruned" for item in artifact["lifecycle"])
    assert artifact["phases"] == ["PRE_SHORTCUT", "POST_SHORTCUT", "POST_REMOVAL"]
    assert artifact["analysis"] == {
        "old_route_before": 1,
        "old_route_after": 1,
        "shortcut_after": 1,
        "old_route_after_removal": 1,
        "shortcut_used": True,
        "persistent_edge_strength": "not available in current architecture",
        "persistent_edge_utility": "not available in current architecture",
    }
    assert edges[("source", "mid")]["traffic_by_phase"] == {
        "PRE_SHORTCUT": 1, "POST_SHORTCUT": 1, "POST_REMOVAL": 1,
    }
    assert edges[("source", "target")]["traffic_by_phase"] == {"POST_SHORTCUT": 1}


def test_competing_path_summary_is_derived_from_traffic_records() -> None:
    artifact = run_competing_path_fixture()
    traffic = list(artifact["traffic"])
    duplicated = [dict(record) for record in traffic if record["phase"] == "PRE_SHORTCUT"]
    traffic.extend(duplicated)
    measured = EdgeInstrumentation.measured_route_traffic(
        traffic, (("source", "mid"), ("mid", "target")), "PRE_SHORTCUT")
    assert measured == 2
    assert measured != artifact["analysis"]["old_route_before"]


def test_unavailable_and_real_zero_creation_timestamps_are_distinct() -> None:
    observer = EdgeInstrumentation()
    unavailable = Edge("a", "b", 1.0)
    observer.register_edge(unavailable)
    assert observer.snapshot()["edges"][0]["created_at"] is None
    assert observer.snapshot()["edges"][0]["created_at_domain"] == "unavailable"
    zero = Edge("c", "d", 1.0)
    observer.register_edge(zero, timestamp=0.0)
    assert observer.snapshot()["edges"][1]["created_at"] == 0.0
    assert observer.snapshot()["edges"][1]["created_at_domain"] == "event_timestamp"


def test_capacity_rejections_are_lifecycle_records() -> None:
    topology = BoundedTopology.from_edges(
        ("source", "left", "right", "target"),
        (("source", "left", 1.0), ("right", "target", 1.0)),
        fan_in_limit=1, fan_out_limit=1, edge_capacity=3, routing_capacity=3,
    )
    observer = EdgeInstrumentation()
    controller = StructuralPlasticityController(topology, local_neighbors={
        "source": ("left", "right"), "right": ("left",),
    }, observer=observer)
    fan_out = controller.grow(CandidateEvidence("source", "source", "right", 1.0, 1.0))
    fan_in = controller.grow(CandidateEvidence("right", "right", "left", 1.0, 1.0))
    assert fan_out.reason == "fan_out_full"
    assert fan_in.reason == "fan_in_full"
    reasons = [item["reason"] for item in observer.snapshot()["lifecycle"]
               if item["kind"] == "candidate_rejected"]
    assert "fan_out_full" in reasons
    assert "fan_in_full" in reasons


def test_decay_context_and_shortcut_replay_are_deterministic() -> None:
    first = run_competing_path_fixture(seed=3)
    second = run_competing_path_fixture(seed=3)
    assert first == second
    assert any(item["kind"] == "decay_context" for item in first["lifecycle"])
    context = first["decay_context"]
    assert context
    decay_records = [item for item in first["lifecycle"] if item["kind"] == "decay_context"]
    assert decay_records[-1]["decay_factor"] >= 0.0


def test_instrumentation_is_downstream_and_non_interfering() -> None:
    enabled = run_competing_path_fixture(instrument=True)
    disabled = run_competing_path_fixture(instrument=False)
    assert enabled["traces"] == disabled["traces"]
    assert enabled["digests"] == disabled["digests"]
    assert enabled["mutations"] == disabled["mutations"]
    assert enabled["run"]["seed"] == disabled["run"]["seed"]


def test_strength_utility_and_eligibility_are_reported_absent() -> None:
    audit = run_competing_path_fixture()["audit"]
    assert audit["persistent_edge_strength"] == "not present"
    assert audit["persistent_edge_utility"] == "not present"
    assert audit["persistent_edge_eligibility"] == "not present"