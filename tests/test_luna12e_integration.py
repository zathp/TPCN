import pytest

from tpcn.event_runtime import Event, EventQueue
from tpcn.experiments import ExperimentConfig, ExperimentRunner, make_synthetic_workload
from tpcn.structural_plasticity import CandidateEvidence, StructuralPlasticityController
from tpcn.topology import BoundedTopology
from tpcn.canonical_neuron import TPCNNeuron


def evidence(source: str, destination: str) -> CandidateEvidence:
    return CandidateEvidence(source, source, destination, 1.0, 1.0, f"{source}-{destination}")


def deliver(network: BoundedTopology, neurons: dict[str, TPCNNeuron], event: Event, queue: EventQueue[Event], limit: float) -> list[Event]:
    network.route(event, queue)
    delivered: list[Event] = []
    while queue and queue.peek() is not None and queue.peek().timestamp <= limit:
        pending = queue.peek()
        assert pending is not None
        item = queue.pop_ready(pending.timestamp)
        neurons[item.destination].receive_event(item)
        delivered.append(item)
    return delivered


def test_reachable_edge_addition_and_pruning_change_future_network_activity() -> None:
    topology = BoundedTopology(("a", "b"), fan_in_limit=1, fan_out_limit=1, edge_capacity=1)
    neurons = {node: TPCNNeuron(node) for node in topology.nodes}
    queue = EventQueue[Event](capacity=4)
    source_event = Event(0.0, "a", "a", "signal", 0.75)

    assert deliver(topology, neurons, source_event, queue, 2.0) == []
    controller = StructuralPlasticityController(topology, local_neighbors={"a": ("b",)})
    assert controller.grow(evidence("a", "b")).status == "grown"
    controller.topology.route(source_event, queue)
    assert queue.peek() is not None
    assert queue.peek().timestamp == pytest.approx(1.0)
    with pytest.raises(IndexError):
        queue.pop_ready(0.5)
    event = queue.pop_ready(1.0)
    neurons[event.destination].receive_event(event)
    assert event.destination == "b"
    assert neurons["b"].processed_events == 1

    assert controller.prune("a", "b").status == "pruned"
    assert controller.topology.route(source_event, queue) == ()


def test_pruning_keeps_already_queued_event_but_removes_later_route() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b"), (("a", "b", 2.0),), fan_in_limit=1, fan_out_limit=1, edge_capacity=1
    )
    controller = StructuralPlasticityController(topology)
    queue = EventQueue[Event](capacity=4)
    controller.topology.route(Event(1.0, "a", "a", "signal", 1.0), queue)
    assert controller.prune("a", "b").status == "pruned"
    assert queue.pop_ready(3.0).destination == "b"
    assert controller.topology.route(Event(3.0, "a", "a", "signal", 1.0), queue) == ()


def test_multi_hop_route_uses_each_receiving_neuron_as_next_source() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b", "c"), (("a", "b", 1.0), ("b", "c", 1.5)), fan_in_limit=1, fan_out_limit=1
    )
    neurons = {node: TPCNNeuron(node) for node in topology.nodes}
    queue = EventQueue[Event](capacity=8)
    first = Event(0.0, "a", "a", "signal", 0.5)
    topology.route(first, queue)
    delivered = []
    while queue:
        pending = queue.peek()
        assert pending is not None
        event = queue.pop_ready(pending.timestamp)
        neurons[event.destination].receive_event(event)
        delivered.append(event)
        topology.route(Event(event.timestamp, event.destination, event.destination, event.event_type,
                             neurons[event.destination].activation), queue)

    assert [(event.destination, event.timestamp) for event in delivered] == [("b", 1.0), ("c", 2.5)]
    assert neurons["b"].processed_events == neurons["c"].processed_events == 1


def test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes() -> None:
    workload = make_synthetic_workload(examples_per_class=1, points_per_example=2)
    config = ExperimentConfig(seed=11, topology_initial_edges=0, topology_edge_capacity=1, max_points=2)
    runner = ExperimentRunner(config)
    without_edge = runner.evaluate(workload)
    assert not any(item[1] == "neuron-0" and item[2] == "neuron-1" for item in without_edge.event_trace)

    assert runner.topology is not None
    runner.topology.connect("neuron-0", "neuron-1", 1.0)
    with_edge = runner.evaluate(workload)
    assert any(item[1] == "neuron-0" and item[2] == "neuron-1" for item in with_edge.event_trace)
    assert with_edge.metrics.event_count > without_edge.metrics.event_count
    assert with_edge.metrics.prediction_loss != pytest.approx(without_edge.metrics.prediction_loss)


def test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary() -> None:
    workload = make_synthetic_workload(examples_per_class=1, points_per_example=2)
    runner = ExperimentRunner(ExperimentConfig(seed=4, topology_initial_edges=0, max_points=2))
    runner.evaluate(workload)
    first_ids = tuple(id(neuron) for neuron in runner.last_neurons)
    runner.evaluate(workload)
    assert first_ids == tuple(id(neuron) for neuron in runner.last_neurons)
    assert runner.last_neurons[0].clock.timestamp == pytest.approx(0.0)
    assert runner.last_neurons[1].clock.timestamp == pytest.approx(1.0)
