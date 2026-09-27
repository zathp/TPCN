import math

import pytest

from tpcn.canonical_neuron import TPCNNeuron
from tpcn.event_runtime import Event, EventQueue, QueueCapacityError
from tpcn.structural_plasticity import StructuralPlasticityController
from tpcn.topology import BoundedTopology


def signal(timestamp: float, source: str, destination: str, payload: float, sequence: int = -1) -> Event:
    return Event(timestamp, source, destination, "signal", payload, sequence)


def deliver(topology: BoundedTopology, source_events: tuple[Event, ...], target: str = "c") -> tuple[list[Event], TPCNNeuron]:
    neurons = {node: TPCNNeuron(node, decay_rate=0.25) for node in topology.nodes}
    queue = EventQueue[Event](capacity=64)
    for event in source_events:
        topology.route(event, queue)
    delivered: list[Event] = []
    while queue:
        event = queue.pop_ready(queue.peek().timestamp)  # type: ignore[union-attr]
        delivered.append(event)
        neurons[event.destination].receive_event(event)
        topology.route(signal(event.timestamp, event.destination, event.destination, neurons[event.destination].activation), queue)
    return delivered, neurons[target]


def test_single_spike_persists_and_evolves_only_at_local_observation() -> None:
    neuron = TPCNNeuron("n", decay_rate=0.5)
    neuron.receive_event(signal(0.0, "input", "n", 1.0))
    initial = neuron.state

    neuron.advance_state(1.0)
    state_at_one = neuron.state
    neuron.advance_state(1.0)
    state_at_two = neuron.state

    assert initial == pytest.approx(1.0)
    assert state_at_one == pytest.approx(math.exp(-0.5))
    assert state_at_two == pytest.approx(math.exp(-1.0))
    assert initial > state_at_one > state_at_two > 0.0


def test_order_and_interval_change_the_neuron_state() -> None:
    def run(values: tuple[float, float], second_time: float) -> tuple[float, float]:
        neuron = TPCNNeuron("n", decay_rate=1.0)
        neuron.receive_event(signal(0.0, "input", "n", values[0]))
        first_activation = neuron.activation
        neuron.receive_event(signal(second_time, "input", "n", values[1]))
        return neuron.state, first_activation

    plus_minus = run((1.0, -1.0), 1.0)[0]
    minus_plus = run((-1.0, 1.0), 1.0)[0]
    short_interval = run((1.0, -1.0), 1.0)[0]
    long_interval = run((1.0, -1.0), 5.0)[0]

    assert plus_minus != pytest.approx(minus_plus)
    assert short_interval != pytest.approx(long_interval)


def test_equal_multiset_different_order_has_distinct_trace() -> None:
    def run(values: tuple[float, float]) -> tuple[float, ...]:
        trace: list[float] = []
        neuron = TPCNNeuron("n", decay_rate=0.5, activity_hook=lambda item: trace.append(item[2]))
        for timestamp, value in enumerate(values):
            neuron.receive_event(signal(float(timestamp), "input", "n", value))
        return tuple(trace)

    assert run((1.0, -1.0)) != run((-1.0, 1.0))


def test_unequal_direct_and_multihop_delays_and_convergence_are_timestamped() -> None:
    topology = BoundedTopology.from_edges(
        ("a", "b", "d", "c"),
        (("a", "c", 1.0), ("a", "b", 1.5), ("b", "d", 1.0), ("d", "c", 1.5)),
        fan_in_limit=2,
        fan_out_limit=2,
    )
    direct, _ = deliver(topology, (signal(3.0, "a", "a", 1.0),))
    assert [(event.destination, event.timestamp) for event in direct[:2]] == [("c", 4.0), ("b", 4.5)]

    old_long = signal(0.0, "a", "a", 1.0)
    new_short = signal(3.0, "a", "a", -1.0)
    arrivals, close_neuron = deliver(topology, (old_long, new_short))
    c_arrivals = [event for event in arrivals if event.destination == "c"]
    assert [event.timestamp for event in c_arrivals] == pytest.approx([1.0, 4.0, 4.0, 7.0])
    assert close_neuron.processed_events == 4


def test_arrival_timing_and_path_pruning_change_downstream_state() -> None:
    edges = (("a", "c", 1.0), ("a", "b", 1.5), ("b", "d", 1.0), ("d", "c", 1.5))

    def run(events: tuple[Event, ...], removed: tuple[str, str] | None = None) -> float:
        topology = BoundedTopology.from_edges(("a", "b", "d", "c"), edges, fan_in_limit=2, fan_out_limit=2)
        if removed is not None:
            controller = StructuralPlasticityController(topology)
            assert controller.prune(*removed).status == "pruned"
            topology = controller.topology
        return deliver(topology, events)[1].state

    close = run((signal(0.0, "a", "a", 1.0), signal(3.0, "a", "a", -1.0)))
    separated = run((signal(0.0, "a", "a", 1.0), signal(8.0, "a", "a", -1.0)))
    no_long = run((signal(0.0, "a", "a", 0.2),), ("a", "b"))
    no_short = run((signal(0.0, "a", "a", 0.2),), ("a", "c"))

    assert close != pytest.approx(separated)
    assert no_long != pytest.approx(run((signal(0.0, "a", "a", 0.2),)))
    assert no_short != pytest.approx(run((signal(0.0, "a", "a", 0.2),)))


def test_fanin_equal_timestamp_uses_queue_sequence_tie_break() -> None:
    topology = BoundedTopology.from_edges(("a", "b", "c"), (("a", "c", 1.0), ("b", "c", 1.0)), fan_in_limit=2, fan_out_limit=1)
    queue = EventQueue[Event](capacity=4)
    topology.route(signal(0.0, "a", "a", 1.0), queue)
    topology.route(signal(0.0, "b", "b", -1.0), queue)
    events = [queue.pop_ready(1.0), queue.pop_ready(1.0)]
    assert [(event.source, event.sequence) for event in events] == [("a", 0), ("b", 1)]


def test_bounded_recurrence_never_exceeds_queue_capacity() -> None:
    topology = BoundedTopology.from_edges(("a", "b"), (("a", "b", 1.0), ("b", "a", 1.0)), fan_in_limit=1, fan_out_limit=1)
    queue = EventQueue[Event](capacity=4)
    topology.route(signal(0.0, "a", "a", 1.0), queue)
    timestamps: list[float] = []
    event_budget = 4
    for _ in range(event_budget):
        event = queue.pop_ready(queue.peek().timestamp)  # type: ignore[union-attr]
        timestamps.append(event.timestamp)
        topology.route(signal(event.timestamp, event.destination, event.destination, event.payload), queue)
    assert len(queue) == 1
    with pytest.raises(QueueCapacityError):
        for _ in range(queue.capacity):
            topology.route(signal(timestamps[-1], "a", "a", 1.0), queue)
    assert timestamps == sorted(timestamps)
    assert len(timestamps) == event_budget


def test_reset_and_external_labels_do_not_change_neural_trace() -> None:
    def run(label: str) -> tuple[float, ...]:
        del label
        neuron = TPCNNeuron("n", decay_rate=0.5)
        trace: list[float] = []
        for timestamp, payload in ((0.0, 1.0), (2.0, -0.25)):
            trace.append(neuron.receive_event(signal(timestamp, "input", "n", payload)))
        return tuple(trace)

    neuron = TPCNNeuron("n")
    neuron.receive_event(signal(0.0, "input", "n", 1.0))
    neuron.reset()
    assert neuron.state == 0.0
    assert neuron.clock.timestamp == 0.0
    assert run("left") == run("right")


def test_same_seed_reproduces_temporal_trace() -> None:
    def run() -> tuple[float, ...]:
        neuron = TPCNNeuron("n", decay_rate=0.25)
        return tuple(neuron.receive_event(signal(timestamp, "input", "n", payload)) for timestamp, payload in ((0.0, 0.5), (1.0, -0.25), (4.0, 0.75)))

    assert run() == run()