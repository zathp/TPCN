"""Deterministic, bounded event-driven runtime primitives.

Time is represented as nonnegative floating-point units. An event is ordered by
arrival timestamp and then by its monotonically increasing sequence identifier.
The sequence identifier is assigned by the queue, so equal-time behavior does
not depend on host thread scheduling.

Propagation uses ``arrival = emission + delay`` with ``delay >= 0``. A zero
delay event is still queued and cannot mutate its destination inline; its
sequence identifier gives it a deterministic place among other events at the
same timestamp. The queue rejects late events and overflow rather than
silently changing causal history.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import heapq
import math
from numbers import Real
from typing import Any, Callable, Generic, Iterable, TypeVar


class EventType(str, Enum):
    """Opaque runtime event categories; downstream components may extend this."""

    INPUT = "input"
    SIGNAL = "signal"
    CONTROL = "control"


EventPayload = Any
LocalTimestamp = float
PropagationDelay = float


class LateEventError(ValueError):
    """Raised when an event precedes the destination's committed local time."""


class QueueCapacityError(BufferError):
    """Raised when accepting an event would exceed finite queue capacity."""


def _time(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


@dataclass(frozen=True, slots=True)
class Event:
    """The minimum causally routable event record."""

    timestamp: LocalTimestamp
    source: str
    destination: str
    event_type: EventType | str
    payload: EventPayload
    sequence: int = field(default=-1, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "timestamp", _time(self.timestamp, "timestamp"))
        if not isinstance(self.source, str) or not self.source:
            raise ValueError("source must be a non-empty string")
        if not isinstance(self.destination, str) or not self.destination:
            raise ValueError("destination must be a non-empty string")
        if not isinstance(self.event_type, (EventType, str)) or not str(self.event_type):
            raise ValueError("event_type must be a non-empty string or EventType")
        if not isinstance(self.sequence, int) or self.sequence < -1:
            raise ValueError("sequence must be a nonnegative integer or -1")


class LocalClock:
    """Monotonic local time for one component; no global tick is implied."""

    def __init__(self, initial: LocalTimestamp = 0.0) -> None:
        self._timestamp = _time(initial, "initial")

    @property
    def timestamp(self) -> LocalTimestamp:
        return self._timestamp

    def advance_to(self, timestamp: LocalTimestamp) -> float:
        next_timestamp = _time(timestamp, "timestamp")
        if next_timestamp < self._timestamp:
            raise LateEventError(
                f"timestamp {next_timestamp} precedes local time {self._timestamp}"
            )
        elapsed = next_timestamp - self._timestamp
        self._timestamp = next_timestamp
        return elapsed


T = TypeVar("T")


class EventQueue(Generic[T]):
    """Finite causal priority queue with deterministic insertion tie ordering."""

    def __init__(self, capacity: int) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self._pending: list[tuple[float, int, Event]] = []
        self._next_sequence = 0

    def __len__(self) -> int:
        return len(self._pending)

    def push(self, event: Event) -> Event:
        if len(self) >= self.capacity:
            raise QueueCapacityError(
                f"event queue capacity {self.capacity} reached; apply backpressure"
            )
        if event.sequence != -1:
            raise ValueError("events must be submitted without a sequence identifier")
        queued = Event(
            event.timestamp,
            event.source,
            event.destination,
            event.event_type,
            event.payload,
            self._next_sequence,
        )
        self._next_sequence += 1
        heapq.heappush(self._pending, (queued.timestamp, queued.sequence, queued))
        return queued

    def push_propagated(
        self,
        emission_time: LocalTimestamp,
        source: str,
        destination: str,
        event_type: EventType | str,
        payload: EventPayload,
        delay: PropagationDelay,
    ) -> Event:
        emission = _time(emission_time, "emission_time")
        propagation = _time(delay, "delay")
        return self.push(Event(emission + propagation, source, destination, event_type, payload))

    def peek(self) -> Event | None:
        return self._pending[0][2] if self._pending else None

    def pop_ready(self, through: LocalTimestamp) -> Event:
        limit = _time(through, "through")
        if not self._pending or self._pending[0][0] > limit:
            raise IndexError("no event is ready")
        return heapq.heappop(self._pending)[2]

    def pop_ready_batch(self, through: LocalTimestamp, limit: int | None = None) -> list[Event]:
        if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0):
            raise ValueError("limit must be a positive integer")
        events: list[Event] = []
        while self._pending and self._pending[0][0] <= _time(through, "through"):
            if limit is not None and len(events) >= limit:
                break
            events.append(heapq.heappop(self._pending)[2])
        return events

    def drain(self) -> Iterable[Event]:
        while self._pending:
            yield heapq.heappop(self._pending)[2]


@dataclass(frozen=True, slots=True)
class BoundedExecutionResult:
    """Bounded execution accounting for one finite event-queue run."""

    completed: bool
    budget_exhausted: bool
    configured_event_budget: int
    processed_event_count: int
    pending_event_count: int
    termination_reason: str
    last_event_timestamp: LocalTimestamp | None
    peak_queue_occupancy: int


def execute_bounded(
    queue: EventQueue[Event],
    handler: Callable[[Event, EventQueue[Event]], None],
    *,
    event_budget: int,
) -> BoundedExecutionResult:
    """Process queued events until completion or an explicit finite budget."""
    if isinstance(event_budget, bool) or not isinstance(event_budget, int) or event_budget <= 0:
        raise ValueError("event_budget must be a positive integer")
    processed = 0
    peak_queue = len(queue)
    last_timestamp: LocalTimestamp | None = None
    while queue and processed < event_budget:
        next_event = queue.peek()
        assert next_event is not None
        event = queue.pop_ready(next_event.timestamp)
        handler(event, queue)
        processed += 1
        last_timestamp = event.timestamp
        peak_queue = max(peak_queue, len(queue))
    pending = len(queue)
    exhausted = pending > 0 and processed >= event_budget
    return BoundedExecutionResult(
        completed=not exhausted,
        budget_exhausted=exhausted,
        configured_event_budget=event_budget,
        processed_event_count=processed,
        pending_event_count=pending,
        termination_reason="budget_exhausted" if exhausted else "completed",
        last_event_timestamp=last_timestamp,
        peak_queue_occupancy=peak_queue,
    )


__all__ = [
    "Event",
    "EventPayload",
    "EventQueue",
    "EventType",
    "BoundedExecutionResult",
    "execute_bounded",
    "LateEventError",
    "LocalClock",
    "LocalTimestamp",
    "PropagationDelay",
    "QueueCapacityError",
]