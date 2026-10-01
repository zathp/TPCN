import math

import pytest

from tpcn.canonical_neuron import TPCNNeuron
from tpcn.edge_instrumentation import EdgeInstrumentation
from tpcn.event_runtime import Event, EventQueue, EventType, execute_bounded
from tpcn.structural_plasticity import CandidateEvidence, StructuralPlasticityController
from tpcn.topology import BoundedTopology, Edge


def model_b(a: float, weight: float, divider: float, reference: float) -> float:
    return divider * math.tanh(weight * a) + (1.0 - divider) * reference


@pytest.mark.parametrize("a", [-1.0, 0.0, 1.0])
@pytest.mark.parametrize("weight", [-2.0, 0.0, 2.0])
@pytest.mark.parametrize("divider", [0.0, 0.25, 0.5, 0.75, 1.0])
@pytest.mark.parametrize("reference", [-1.0, -0.5, 0.0, 0.5, 1.0])
def test_model_b_transfer_matches_analytic_equation(a, weight, divider, reference):
    edge = Edge("source", "target", 1.0, edge_weight=weight,
                divider_strength=divider, reference=reference)
    topology = BoundedTopology.from_edges(("source", "target"), (edge,),
                                          fan_in_limit=1, fan_out_limit=1)
    routed = topology.route(Event(0.0, "source", "source", EventType.SIGNAL, a), EventQueue(2))[0]
    assert routed.payload == pytest.approx(model_b(a, weight, divider, reference))
    assert -1.0 <= routed.payload <= 1.0


@pytest.mark.parametrize("divider, expected", [(0.0, 0.75), (1.0, math.tanh(0.5))])
def test_divider_endpoints_are_reference_and_transformed_signal(divider, expected):
    edge = Edge("source", "target", 1.0, divider_strength=divider, reference=0.75)
    topology = BoundedTopology.from_edges(("source", "target"), (edge,),
                                          fan_in_limit=1, fan_out_limit=1)
    routed = topology.route(Event(0.0, "source", "source", "signal", 0.5), EventQueue(1))[0]
    assert routed.payload == pytest.approx(expected)


def test_weight_zero_removes_source_branch_but_preserves_reference_interpolation():
    edge = Edge("source", "target", 1.0, edge_weight=0.0,
                divider_strength=0.25, reference=-0.8)
    topology = BoundedTopology.from_edges(("source", "target"), (edge,),
                                          fan_in_limit=1, fan_out_limit=1)
    routed = topology.route(Event(0.0, "source", "source", "signal", 1.0), EventQueue(1))[0]
    assert routed.payload == pytest.approx(-0.6)


def test_control_payloads_remain_opaque_and_are_not_edge_transformed():
    edge = Edge("source", "target", 1.0, edge_weight=-2.0,
                divider_strength=0.25, reference=0.75)
    topology = BoundedTopology.from_edges(("source", "target"), (edge,),
                                          fan_in_limit=1, fan_out_limit=1)
    marker = {"credit_id": "reward-1"}
    routed = topology.route(Event(0.0, "source", "target", EventType.CONTROL, marker), EventQueue(1))[0]
    assert routed.payload is marker


def test_signed_weight_and_activation_have_odd_signal_component():
    for activation, weight in ((0.8, 1.5), (0.8, -1.5), (-0.8, 1.5), (-0.8, -1.5)):
        positive = model_b(activation, weight, 1.0, 0.0)
        negative = model_b(-activation, weight, 1.0, 0.0)
        assert negative == pytest.approx(-positive)


def test_each_edge_dimension_is_independently_effective():
    assert model_b(0.7, 0.5, 0.6, -0.2) != pytest.approx(model_b(0.7, 1.5, 0.6, -0.2))
    assert model_b(0.7, 1.0, 0.25, -0.2) != pytest.approx(model_b(0.7, 1.0, 0.75, -0.2))
    assert model_b(0.7, 1.0, 0.6, -0.8) != pytest.approx(model_b(0.7, 1.0, 0.6, 0.8))


def test_fan_out_computes_each_edge_from_the_same_source_activation():
    topology = BoundedTopology.from_edges(
        ("source", "left", "right"),
        (Edge("source", "left", 1.0, edge_weight=2.0),
         Edge("source", "right", 1.0, edge_weight=-1.0, divider_strength=0.5, reference=0.2)),
        fan_in_limit=1, fan_out_limit=2)
    routed = topology.route(Event(0.0, "source", "source", "signal", 0.5), EventQueue(2))
    by_destination = {event.destination: event.payload for event in routed}
    assert by_destination["left"] == pytest.approx(model_b(0.5, 2.0, 1.0, 0.0))
    assert by_destination["right"] == pytest.approx(model_b(0.5, -1.0, 0.5, 0.2))


def test_equal_time_fan_in_is_sequential_and_deterministic():
    topology = BoundedTopology.from_edges(
        ("a", "b", "target"),
        (Edge("a", "target", 1.0, edge_weight=2.0),
         Edge("b", "target", 1.0, edge_weight=-1.0, divider_strength=0.5, reference=0.4)),
        fan_in_limit=2, fan_out_limit=1)

    def run():
        neurons = {node: TPCNNeuron(node, decay_rate=0.2) for node in ("a", "b", "target")}
        queue = EventQueue(4)
        topology.route(Event(0.0, "a", "a", "signal", 0.5), queue)
        topology.route(Event(0.0, "b", "b", "signal", 0.5), queue)
        trace = []
        while queue:
            event = queue.pop_ready(queue.peek().timestamp)
            trace.append((event.sequence, event.timestamp, event.destination, event.payload))
            neurons[event.destination].receive_event(event)
        return trace, neurons["target"].state

    first, first_state = run()
    second, second_state = run()
    assert first == second
    assert first_state == second_state
    assert first[-1][1] == pytest.approx(1.0)


def test_unequal_delays_have_no_pre_arrival_effect_and_decay_between_arrivals():
    topology = BoundedTopology.from_edges(
        ("source", "target"), (Edge("source", "target", 1.0),),
        fan_in_limit=1, fan_out_limit=1)
    neuron = TPCNNeuron("target", decay_rate=1.0)
    queue = EventQueue(2)
    topology.route(Event(0.0, "source", "source", "signal", 1.0), queue)
    assert neuron.state == 0.0
    neuron.receive_event(queue.pop_ready(1.0))
    state_at_first = neuron.state
    queue.push(Event(2.0, "source", "target", "signal", 0.5))
    assert neuron.state == state_at_first
    neuron.receive_event(queue.pop_ready(2.0))
    assert neuron.state == pytest.approx(state_at_first * math.exp(-1.0) + 0.5)


def test_bounded_recurrent_execution_reports_budget_and_finite_state():
    topology = BoundedTopology.from_edges(
        ("a", "b"), (Edge("a", "b", 1.0, edge_weight=2.0), Edge("b", "a", 1.0, edge_weight=-2.0)),
        fan_in_limit=1, fan_out_limit=1, edge_capacity=2, routing_capacity=1)
    queue = EventQueue(4)
    neurons = {node: TPCNNeuron(node, decay_rate=0.1) for node in ("a", "b")}
    queue.push(Event(0.0, "a", "a", "signal", 1.0))

    def handle(event, pending):
        activation = neurons[event.destination].receive_event(event)
        topology.route(Event(event.timestamp, event.destination, event.destination, "signal", activation), pending)

    result = execute_bounded(queue, handle, event_budget=5)
    assert result.budget_exhausted
    assert result.pending_event_count <= queue.capacity
    assert all(math.isfinite(neuron.state) and abs(neuron.state) <= neuron.state_limit
               for neuron in neurons.values())


def test_structural_growth_defaults_and_reconstruction_preserve_model_b_state():
    topology = BoundedTopology(("a", "b", "c"), fan_in_limit=2, fan_out_limit=2, edge_capacity=2)
    controller = StructuralPlasticityController(topology)
    grown = controller.grow(CandidateEvidence("a", "a", "b", 99.0, 1.0))
    assert grown.edge == Edge("a", "b", 1.0)
    explicit = Edge("b", "c", 1.0, edge_weight=-1.5, divider_strength=0.25, reference=0.5)
    rebuilt = BoundedTopology.from_edges(("a", "b", "c"), (grown.edge, explicit),
                                         fan_in_limit=2, fan_out_limit=2, edge_capacity=2)
    assert rebuilt.edge("b", "c") == explicit
    first = rebuilt.route(Event(0.0, "b", "b", "signal", 0.4), EventQueue(1))[0]
    second = BoundedTopology.from_edges(("a", "b", "c"), rebuilt.edges,
                                        fan_in_limit=2, fan_out_limit=2, edge_capacity=2).route(
                                            Event(0.0, "b", "b", "signal", 0.4), EventQueue(1))[0]
    assert first.payload == pytest.approx(second.payload)


def test_observer_on_off_and_replay_have_identical_computation():
    edge = Edge("a", "b", 1.0, edge_weight=-1.25, divider_strength=0.75, reference=0.2)
    topology = BoundedTopology.from_edges(("a", "b"), (edge,), fan_in_limit=1, fan_out_limit=1)

    def run(observer=None):
        queue = EventQueue(2)
        routed = topology.route(Event(0.0, "a", "a", "signal", 0.6), queue, observer=observer)[0]
        return routed.timestamp, routed.payload, routed.sequence

    first = run()
    assert first == run(EdgeInstrumentation())
    assert first == run()