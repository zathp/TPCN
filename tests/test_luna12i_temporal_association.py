import random

from tpcn.event_runtime import Event, EventQueue
from tpcn.structural_plasticity import StructuralPlasticityController
from tpcn.temporal_association import TemporalAssociationPolicy
from tpcn.topology import BoundedTopology


NODES = ("a", "b", "c", "d", "e")
NEIGHBORS = {"a": ("c", "d"), "b": ("c", "e")}


def make_policy(**overrides):
    options = {
        "history_capacity": 6,
        "candidate_capacity": 8,
        "association_window": 2.0,
        "maximum_score": 4,
        "local_neighbors": NEIGHBORS,
    }
    options.update(overrides)
    return TemporalAssociationPolicy(NODES, **options)


def feed(policy, observations):
    for observer, node, timestamp in observations:
        policy.observe(observer, node, timestamp)


def source_local_sequence(source, target, repetitions):
    observations = []
    for index in range(repetitions):
        observations.extend(((source, source, float(index * 2)), (source, target, float(index * 2 + 1))))
    return observations


def test_repeated_local_association_is_bounded_and_deterministic():
    observations = source_local_sequence("a", "c", 3) + [("a", "a", 8.0), ("a", "d", 9.0)]
    left = make_policy()
    right = make_policy()
    feed(left, observations)
    feed(right, observations)

    assert [(item.source, item.destination, item.score) for item in left.candidates] == [
        ("a", "c", 3), ("a", "d", 1)
    ]
    assert left.candidates == right.candidates
    assert left.state.history_count <= len(NODES) * left.state.history_capacity
    assert left.state.candidate_count <= left.state.candidate_capacity
    assert all(item.observer == item.source for item in left.candidates)


def test_reversed_local_order_falsifies_the_association_signal():
    ordered = [("a", "a", 0.0), ("a", "a", 1.0), ("a", "a", 2.0),
               ("a", "c", 3.0), ("a", "c", 4.0), ("a", "c", 5.0)]
    reversed_order = [(observer, node, float(index)) for index, (observer, node, _) in enumerate(reversed(ordered))]

    temporal = make_policy()
    control = make_policy()
    feed(temporal, ordered)
    feed(control, reversed_order)

    assert [(item.source, item.destination, item.score) for item in temporal.candidates] == [("a", "c", 2)]
    assert control.candidates == ()


def test_candidate_capacity_rejection_and_reset_are_explicit():
    policy = make_policy(candidate_capacity=1)
    feed(policy, source_local_sequence("a", "c", 1) + source_local_sequence("b", "e", 1))

    assert policy.state.candidate_count == 1
    assert policy.candidate_rejections == 1
    assert policy.candidate_rejection_reasons == (("candidate_capacity", 1),)
    policy.reset()
    assert policy.state.observation_count == 0
    assert policy.state.history_count == 0
    assert policy.candidates == ()
    assert policy.candidate_rejections == 0


def grow(candidates, *, seed=None):
    topology = BoundedTopology(NODES, fan_in_limit=2, fan_out_limit=2, edge_capacity=4)
    controller = StructuralPlasticityController(
        topology,
        max_growth_per_adaptation=2,
        local_neighbors=NEIGHBORS,
    )
    selected = tuple(candidates)
    if seed is not None:
        selected = tuple(random.Random(seed).sample(selected, 2))
    results = controller.adapt_many(selected, maximum=2)
    return controller, results


def test_temporal_candidates_form_convergent_fanin_against_matched_random_control():
    policy = make_policy()
    feed(policy, source_local_sequence("a", "c", 3) + source_local_sequence("b", "c", 3))
    temporal = policy.candidates
    distractors = temporal + (
        temporal[0].__class__("a", "a", "d", 1, 1.0, "distractor-a"),
        temporal[0].__class__("b", "b", "e", 1, 1.0, "distractor-b"),
    )

    temporal_controller, temporal_results = grow(temporal)
    random_controller, random_results = grow(distractors, seed=7)
    temporal_topology = temporal_controller.topology
    random_topology = random_controller.topology

    assert [result.status for result in temporal_results] == ["grown", "grown"]
    assert len(temporal_topology.incoming("c")) == 2
    assert len(random_results) == 2
    assert len(random_topology) <= random_topology.edge_capacity
    assert all(len(random_topology.incoming(node)) <= random_topology.fan_in_limit for node in NODES)

    queue = EventQueue[Event](capacity=4)
    temporal_topology.route(Event(0.0, "a", "a", "signal", 1.0), queue)
    temporal_topology.route(Event(0.0, "b", "b", "signal", 1.0), queue)
    arrivals = [queue.pop_ready(1.0), queue.pop_ready(1.0)]
    assert [event.destination for event in arrivals] == ["c", "c"]
    assert [event.timestamp for event in arrivals] == [1.0, 1.0]