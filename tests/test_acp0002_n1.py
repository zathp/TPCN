import math

import pytest

from tpcn.canonical_neuron import TPCNNeuron
from tpcn.edge_instrumentation import EdgeInstrumentation
from tpcn.event_runtime import Event, EventQueue
from tpcn.structural_plasticity import CandidateEvidence, StructuralPlasticityController
from tpcn.topology import BoundedTopology, Edge


def test_edge_accepts_canonical_bounds_and_preserves_explicit_record():
    edge = Edge("a", "b", 1.25, routing_cost=3, edge_weight=-2.0,
                divider_strength=0.0, reference=1.0)

    assert edge.edge_weight == -2.0
    assert edge.divider_strength == 0.0
    assert edge.reference == 1.0
    assert edge.propagation_delay == 1.25
    assert edge.routing_cost == 3
    assert edge.legacy_identity is True


@pytest.mark.parametrize("field,value", [
    ("edge_weight", -2.1), ("edge_weight", 2.1),
    ("divider_strength", -0.1), ("divider_strength", 1.1),
    ("reference", -1.1), ("reference", 1.1),
])
def test_edge_rejects_out_of_range_parameters(field, value):
    with pytest.raises(ValueError):
        Edge("a", "b", 1.0, **{field: value})


@pytest.mark.parametrize("field", ["edge_weight", "divider_strength", "reference"])
def test_edge_rejects_nonfinite_and_boolean_parameters(field):
    for value in (math.nan, math.inf, -math.inf, True, False):
        with pytest.raises((TypeError, ValueError)):
            Edge("a", "b", 1.0, **{field: value})


def test_edge_and_neuron_retain_positive_delay_and_gain_bounds():
    with pytest.raises(ValueError):
        Edge("a", "b", 0.0)
    with pytest.raises(ValueError):
        Edge("a", "b", math.inf)
    assert TPCNNeuron("n", neuron_gain=0.0).neuron_gain == 0.0
    assert TPCNNeuron("n", neuron_gain=2.0).neuron_gain == 2.0
    for value in (-0.1, 2.1, math.nan, math.inf, True):
        with pytest.raises((TypeError, ValueError)):
            TPCNNeuron("n", neuron_gain=value)


def test_neuron_gain_alias_is_behaviorally_compatible_and_conflicts_reject():
    legacy = TPCNNeuron("n", input_gain=0.75)
    canonical = TPCNNeuron("n", neuron_gain=0.75)
    both = TPCNNeuron("n", input_gain=0.75, neuron_gain=0.75)

    assert legacy.neuron_gain == canonical.neuron_gain == both.neuron_gain == 0.75
    assert legacy.input_gain == canonical.input_gain == 0.75
    with pytest.raises(ValueError, match="must agree"):
        TPCNNeuron("n", input_gain=0.5, neuron_gain=1.0)


def test_legacy_three_tuple_and_explicit_edge_topology_construction():
    explicit = Edge("a", "b", 2.0, routing_cost=4, edge_weight=1.5,
                    divider_strength=0.25, reference=-0.5)
    topology = BoundedTopology.from_edges(
        ("a", "b", "c"), (explicit, ("b", "c", 1.0)),
        fan_in_limit=2, fan_out_limit=2, edge_capacity=2,
    )

    assert topology.edge("a", "b") == explicit
    assert topology.edge("b", "c").edge_weight == 1.0
    assert topology.edge("b", "c").legacy_identity is True


def test_rebuild_and_prune_preserve_explicit_edge_state():
    explicit = Edge("a", "b", 2.0, routing_cost=4, edge_weight=1.5,
                    divider_strength=0.25, reference=-0.5)
    topology = BoundedTopology.from_edges(
        ("a", "b", "c"), (explicit, ("b", "c", 1.0)),
        fan_in_limit=2, fan_out_limit=2, edge_capacity=3,
    )
    controller = StructuralPlasticityController(topology)

    assert controller.prune("b", "c").status == "pruned"
    assert controller.topology.edge("a", "b") == explicit


def test_structural_growth_uses_defaults_and_never_copies_candidate_score():
    topology = BoundedTopology(("a", "b"), fan_in_limit=1, fan_out_limit=1, edge_capacity=1)
    controller = StructuralPlasticityController(topology)

    result = controller.grow(CandidateEvidence("a", "a", "b", 99.0, 1.5))

    assert result.status == "grown"
    assert result.edge == Edge("a", "b", 1.5)
    assert result.edge.edge_weight != 99.0


def test_observer_exposes_edge_parameters_without_affecting_model_b_route():
    edge = Edge("a", "b", 1.5, routing_cost=2, edge_weight=-1.5,
                divider_strength=0.25, reference=0.75)
    topology = BoundedTopology.from_edges(
        ("a", "b"), (edge,), fan_in_limit=1, fan_out_limit=1, edge_capacity=1,
    )
    observer = EdgeInstrumentation()
    queue = EventQueue[Event](capacity=2)
    payload = 0.5
    emitted = topology.route(Event(2.0, "a", "ignored", "signal", payload), queue, observer=observer)[0]
    record = observer.snapshot()["edges"][0]

    expected = 0.25 * math.tanh(-1.5 * payload) + 0.75 * 0.75
    assert emitted.payload == pytest.approx(expected)
    assert emitted.timestamp == 3.5
    assert record["edge_weight"] == -1.5
    assert record["divider_strength"] == 0.25
    assert record["reference"] == 0.75
    assert record["delay"] == 1.5
    assert record["routing_cost"] == 2


def test_n2_route_preserves_event_order_and_applies_model_b_transfer():
    edge = Edge("a", "b", 1.0, edge_weight=2.0, divider_strength=0.0, reference=-1.0)
    topology = BoundedTopology.from_edges(
        ("a", "b"), (edge,), fan_in_limit=1, fan_out_limit=1, edge_capacity=1,
    )
    queue = EventQueue[Event](capacity=2)
    payload = 0.37
    first = topology.route(Event(4.0, "a", "ignored", "signal", payload), queue)[0]
    second = topology.route(Event(4.0, "a", "ignored", "signal", payload), queue)[0]

    expected = -1.0
    assert first.payload == pytest.approx(expected)
    assert second.payload == pytest.approx(expected)
    assert (first.timestamp, first.source, first.destination, first.sequence) == (5.0, "a", "b", 0)
    assert second.sequence == 1
    assert first.payload == pytest.approx(math.tanh(2.0 * payload) * 0.0 - 1.0)


def test_explicit_edge_records_replay_deterministically():
    edge = Edge("a", "b", 1.0, routing_cost=2, edge_weight=-0.5,
                divider_strength=0.4, reference=0.2)
    first = BoundedTopology.from_edges(("a", "b"), (edge,), fan_in_limit=1, fan_out_limit=1)
    second = BoundedTopology.from_edges(("a", "b"), (edge,), fan_in_limit=1, fan_out_limit=1)

    assert first.edges == second.edges
    assert repr(first.edges) == repr(second.edges)
