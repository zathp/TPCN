import random

import pytest

from tpcn.event_runtime import (
    BoundedExecutionResult,
    Event,
    EventQueue,
    EventType,
    LateEventError,
    LocalClock,
    QueueCapacityError,
    execute_bounded,
)


def test_irregular_local_time_has_no_global_neural_clock() -> None:
    first = LocalClock()
    second = LocalClock()

    assert first.advance_to(0.25) == pytest.approx(0.25)
    assert second.timestamp == 0.0
    assert second.advance_to(1.75) == pytest.approx(1.75)
    assert first.advance_to(2.0) == pytest.approx(1.75)


def test_idle_queue_does_not_dispatch_without_a_ready_event() -> None:
    queue = EventQueue(capacity=2)
    queue.push(Event(4.0, "a", "b", EventType.SIGNAL, None))

    with pytest.raises(IndexError):
        queue.pop_ready(3.999)
    assert len(queue) == 1


def test_queue_orders_by_arrival_then_deterministic_sequence() -> None:
    queue = EventQueue(capacity=8)
    later = queue.push(Event(2.0, "a", "b", EventType.SIGNAL, "later"))
    first = queue.push(Event(1.0, "a", "b", EventType.SIGNAL, "first"))
    second = queue.push(Event(1.0, "c", "b", EventType.SIGNAL, "second"))

    assert [event.payload for event in queue.drain()] == ["first", "second", "later"]
    assert (first.sequence, second.sequence, later.sequence) == (1, 2, 0)


def test_propagation_delay_and_zero_delay_are_queued_causally() -> None:
    queue = EventQueue(capacity=4)
    delayed = queue.push_propagated(3.0, "source", "destination", EventType.SIGNAL, "delayed", 2.5)
    zero = queue.push_propagated(3.0, "source", "destination", EventType.SIGNAL, "zero", 0.0)

    assert delayed.timestamp == pytest.approx(5.5)
    assert queue.pop_ready_batch(3.0) == [zero]
    assert queue.peek() == delayed


def test_late_events_are_rejected_without_mutating_local_time() -> None:
    clock = LocalClock(2.0)

    with pytest.raises(LateEventError):
        clock.advance_to(1.0)
    assert clock.timestamp == 2.0


def test_capacity_uses_backpressure_and_keeps_pending_state_bounded() -> None:
    queue = EventQueue(capacity=2)
    event = Event(0.0, "a", "b", EventType.INPUT, None)
    queue.push(event)
    queue.push(event)

    with pytest.raises(QueueCapacityError):
        queue.push(event)
    assert len(queue) == 2


def test_serial_and_batched_execution_have_identical_causal_trace() -> None:
    def execute(batch: bool) -> list[tuple[str, float, int]]:
        queue = EventQueue(capacity=32)
        for payload, timestamp in (("a", 0.0), ("b", 0.0), ("c", 1.0)):
            queue.push(Event(timestamp, "input", "node", EventType.SIGNAL, payload))
        trace: list[tuple[str, float, int]] = []
        while queue:
            ready = queue.pop_ready_batch(queue.peek().timestamp) if batch else [queue.pop_ready(queue.peek().timestamp)]
            for event in ready:
                trace.append((event.payload, event.timestamp, event.sequence))
                if event.destination == "node":
                    queue.push_propagated(event.timestamp, "node", "sink", EventType.SIGNAL, event.payload, 0.0)
        return trace

    assert execute(batch=False) == execute(batch=True)


def test_seeded_inputs_replay_identically() -> None:
    def run(seed: int) -> list[tuple[float, int, int]]:
        random_source = random.Random(seed)
        queue = EventQueue(capacity=16)
        for _ in range(6):
            timestamp = random_source.choice((0.0, 0.5, 2.0))
            queue.push(Event(timestamp, "source", "destination", EventType.INPUT, random_source.random()))
        return [(event.timestamp, event.sequence, event.payload) for event in queue.drain()]

    assert run(17) == run(17)
    assert run(17) != run(18)


def test_invalid_events_and_delays_are_rejected() -> None:
    with pytest.raises(ValueError):
        Event(-1.0, "a", "b", EventType.SIGNAL, None)
    with pytest.raises(ValueError):
        Event(0.0, "", "b", EventType.SIGNAL, None)
    with pytest.raises(ValueError):
        Event(0.0, "a", "", EventType.SIGNAL, None)
    with pytest.raises(ValueError):
        EventQueue(capacity=2).push_propagated(0.0, "a", "b", EventType.SIGNAL, None, -0.1)


@pytest.mark.parametrize("budget", (1, 2, 8, 64))
def test_bounded_execution_reports_recurrent_budget_exhaustion(budget: int) -> None:
    queue = EventQueue[Event](capacity=8)
    queue.push(Event(0.0, "a", "a", EventType.SIGNAL, 1.0))

    def continue_cycle(event: Event, pending: EventQueue[Event]) -> None:
        pending.push_propagated(event.timestamp, event.destination, event.source, EventType.SIGNAL, event.payload, 1.0)

    result = execute_bounded(queue, continue_cycle, event_budget=budget)

    assert isinstance(result, BoundedExecutionResult)
    assert result.configured_event_budget == budget
    assert result.processed_event_count == budget
    assert result.pending_event_count == 1
    assert result.completed is False
    assert result.budget_exhausted is True
    assert result.termination_reason == "budget_exhausted"
    assert result.last_event_timestamp == pytest.approx(float(budget - 1))


def test_bounded_execution_reports_completion_without_pending_work() -> None:
    queue = EventQueue[Event](capacity=4)
    queue.push(Event(2.0, "a", "b", EventType.SIGNAL, None))

    result = execute_bounded(queue, lambda event, pending: None, event_budget=1)

    assert result == BoundedExecutionResult(True, False, 1, 1, 0, "completed", 2.0, 1)