import math
import random

import pytest

from tpcn import TPCNNeuron as PublicTPCNNeuron
from tpcn.canonical_neuron import TPCNNeuron
from tpcn.event_runtime import Event, EventQueue, EventType


def make_event(timestamp: float, destination: str, payload: float) -> Event:
    return Event(timestamp, "source", destination, EventType.SIGNAL, payload)


def test_canonical_neuron_is_exported_from_public_package() -> None:
    assert PublicTPCNNeuron is TPCNNeuron


def test_receipt_is_local_and_idle_neurons_are_untouched() -> None:
    first = TPCNNeuron("first")
    second = TPCNNeuron("second")

    first.receive_event(make_event(0.25, "first", 0.75))

    assert first.state != 0.0
    assert first.processed_events == 1
    assert second.state == 0.0
    assert second.processed_events == 0
    assert second.clock.timestamp == 0.0


def test_irregular_event_times_use_local_elapsed_time() -> None:
    neuron = TPCNNeuron("node", decay_rate=1.0)

    neuron.receive_event(make_event(0.5, "node", 1.0))
    first_state = neuron.state
    neuron.receive_event(make_event(2.0, "node", 0.0))

    assert neuron.clock.timestamp == pytest.approx(2.0)
    assert neuron.state == pytest.approx(first_state * math.exp(-1.5))


def test_state_and_activation_are_bounded_under_stress() -> None:
    neuron = TPCNNeuron("node", state_limit=0.5)

    for index in range(100):
        neuron.receive_event(make_event(index / 10, "node", 100.0 if index % 2 else -100.0))

    assert abs(neuron.state) <= 0.5
    assert abs(neuron.activation) <= 1.0
    assert 0.0 <= neuron.eligibility_state <= 1.0


def test_emission_is_queued_with_propagation_delay() -> None:
    source = TPCNNeuron("source")
    destination = TPCNNeuron("destination")
    source.receive_event(make_event(1.0, "source", 1.0))
    queue = EventQueue(capacity=4)

    emitted = source.emit_event(queue, "destination", delay=2.5)

    assert destination.state == 0.0
    assert emitted.timestamp == pytest.approx(3.5)
    with pytest.raises(IndexError):
        queue.pop_ready(3.499)
    destination.receive_event(queue.pop_ready(3.5))
    assert destination.state != 0.0


def test_local_hook_has_only_local_activity_arguments() -> None:
    observed: list[tuple[str, float, float]] = []
    neuron = TPCNNeuron("node", activity_hook=observed.append)

    neuron.receive_event(make_event(2.0, "node", 0.5))

    assert observed == [("node", 2.0, neuron.activation)]
    assert neuron.prediction_error == 0.0


def test_neuron_rejects_nonlocal_label_like_payloads() -> None:
    neuron = TPCNNeuron("node")

    with pytest.raises(TypeError):
        neuron.receive_event(make_event(0.0, "node", {"label": "A"}))


def test_ordered_batch_delivery_matches_serial_delivery() -> None:
    inputs = [make_event(0.0, "node", 0.5), make_event(0.0, "node", -0.25)]
    serial = TPCNNeuron("node")
    batched = TPCNNeuron("node")
    serial_queue = EventQueue(capacity=4)
    batch_queue = EventQueue(capacity=4)
    for event in inputs:
        serial_queue.push(event)
        batch_queue.push(event)

    while serial_queue:
        serial.receive_event(serial_queue.pop_ready(0.0))
    for event in batch_queue.pop_ready_batch(0.0):
        batched.receive_event(event)

    assert (serial.state, serial.activation) == (batched.state, batched.activation)


def test_identical_ordered_inputs_and_seed_are_deterministic() -> None:
    def run(seed: int) -> tuple[float, float, int]:
        random_source = random.Random(seed)
        neuron = TPCNNeuron("node")
        for timestamp in (0.0, 0.25, 1.5, 2.0):
            neuron.receive_event(make_event(timestamp, "node", random_source.uniform(-2.0, 2.0)))
        return neuron.state, neuron.activation, neuron.processed_events

    assert run(17) == run(17)
    assert run(17) != run(18)