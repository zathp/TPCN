"""Deterministic, bounded event-driven runtime primitives.

Time is represented as nonnegative floating-point units. An event is ordered by
arrival timestamp and its monotonically increasing sequence identifier, except
that an external event for a destination is selected before an internal event
for that same destination at the same timestamp. The sequence identifier is
assigned by the queue, so equal-time behavior does not depend on host thread
scheduling.

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
    EXCURSION = "excursion"
    INTERNAL = "internal"
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
    event_id: str | int | None = field(default=None, compare=False)
    lineage_id: str | int | None = field(default=None, compare=False)

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
        if self.event_id is not None and (
            isinstance(self.event_id, bool) or not isinstance(self.event_id, (str, int))
        ):
            raise TypeError("event_id must be a string, integer, or None")
        if self.lineage_id is not None and (
            isinstance(self.lineage_id, bool) or not isinstance(self.lineage_id, (str, int))
        ):
            raise TypeError("lineage_id must be a string, integer, or None")


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

    def __init__(self, capacity: int, *, observer: Any = None) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self._pending: list[tuple[float, int, Event]] = []
        self._next_sequence = 0
        self._observer = observer
        self._observer_order = 0

    def __len__(self) -> int:
        return len(self._pending)

    def _snapshot(self) -> list[Event]:
        return [item[2] for item in sorted(self._pending, key=lambda item: (item[0], item[1]))]

    def _tie_break_cause(self, event: Event) -> str:
        same_time = [item[2] for item in self._pending if item[0] == event.timestamp]
        external_destinations = {other.destination for other in same_time
                                 if other.event_type != EventType.INTERNAL}
        if any(other.event_type == EventType.INTERNAL
               and other.destination in external_destinations
               and other.sequence < event.sequence for other in same_time):
            return "external_before_internal_same_destination_same_timestamp"
        return "timestamp_then_assigned_sequence"

    def _observe(self, operation: str, event: Event, *, before: int, after: int,
                 reason: str | None = None, tie_break_cause: str | None = None) -> None:
        callback = getattr(self._observer, "queue_transition", None)
        if callback is not None:
            callback(operation, event=event, occupancy_before=before, occupancy_after=after,
                     capacity=self.capacity, pending=self._snapshot(),
                     queue_sequence=event.sequence, reason=reason,
                     tie_break_cause=tie_break_cause)

    def _before_next_event(self) -> bool:
        callback = getattr(self._observer, "before_next_event", None)
        return True if callback is None else bool(callback(self))

    def _after_event(self) -> None:
        callback = getattr(self._observer, "after_event", None)
        if callback is not None:
            callback()

    def _finish_execution(self) -> bool:
        callback = getattr(self._observer, "finish", None)
        if callback is not None:
            return callback(queue=self) is not False
        return True

    def push(self, event: Event) -> Event:
        before = len(self)
        try:
            if before >= self.capacity:
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
                event.event_id,
                event.lineage_id,
            )
            self._next_sequence += 1
            heapq.heappush(self._pending, (queued.timestamp, queued.sequence, queued))
        except (BufferError, ValueError) as error:
            self._observe("queue_failure", event, before=before, after=before,
                          reason=type(error).__name__)
            raise
        self._observe("enqueue", queued, before=before, after=len(self))
        return queued

    def _next_ready_index(self) -> int | None:
        if not self._pending:
            return None
        timestamp = self._pending[0][0]
        same_time = [
            (index, item[2])
            for index, item in enumerate(self._pending)
            if item[0] == timestamp
        ]
        external_destinations = {
            event.destination
            for _, event in same_time
            if event.event_type != EventType.INTERNAL
        }
        eligible = [
            (index, event)
            for index, event in same_time
            if event.event_type != EventType.INTERNAL
            or event.destination not in external_destinations
        ]
        return min(eligible, key=lambda item: item[1].sequence)[0]

    def _pop_next_ready(self) -> Event:
        index = self._next_ready_index()
        if index is None:
            raise IndexError("no event is ready")
        _, _, event = self._pending[index]
        self._pending[index] = self._pending[-1]
        self._pending.pop()
        heapq.heapify(self._pending)
        return event

    def push_propagated(
        self,
        emission_time: LocalTimestamp,
        source: str,
        destination: str,
        event_type: EventType | str,
        payload: EventPayload,
        delay: PropagationDelay,
        *,
        event_id: str | int | None = None,
        lineage_id: str | int | None = None,
    ) -> Event:
        emission = _time(emission_time, "emission_time")
        propagation = _time(delay, "delay")
        return self.push(
            Event(
                emission + propagation,
                source,
                destination,
                event_type,
                payload,
                event_id=event_id,
                lineage_id=lineage_id,
            )
        )

    def peek(self) -> Event | None:
        index = self._next_ready_index()
        return None if index is None else self._pending[index][2]

    def pop_ready(self, through: LocalTimestamp) -> Event:
        limit = _time(through, "through")
        if not self._pending or self._pending[0][0] > limit:
            raise IndexError("no event is ready")
        cause = None
        if self._observer is not None:
            event = self.peek()
            assert event is not None
            cause = self._tie_break_cause(event)
        before = len(self)
        popped = self._pop_next_ready()
        self._observe("dequeue", popped, before=before, after=len(self), tie_break_cause=cause)
        return popped

    def pop_ready_batch(self, through: LocalTimestamp, limit: int | None = None) -> list[Event]:
        if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0):
            raise ValueError("limit must be a positive integer")
        events: list[Event] = []
        through_limit = _time(through, "through")
        while self._pending and self._pending[0][0] <= through_limit:
            if limit is not None and len(events) >= limit:
                break
            events.append(self._pop_next_ready())
        return events

    def drain(self) -> Iterable[Event]:
        while self._pending:
            yield self._pop_next_ready()


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
    pair_stopped = False
    try:
        while queue and processed < event_budget:
            if not queue._before_next_event():
                pair_stopped = True
                break
            next_event = queue.peek()
            assert next_event is not None
            event = queue.pop_ready(next_event.timestamp)
            handler(event, queue)
            queue._observe("process", event, before=len(queue), after=len(queue))
            processed += 1
            last_timestamp = event.timestamp
            peak_queue = max(peak_queue, len(queue))
            queue._after_event()
    except BaseException:
        callback = getattr(queue._observer, "execution_failed", None)
        if callback is not None:
            callback(queue)
        raise
    finally:
        pair_stopped = not queue._finish_execution() or pair_stopped
    pending = len(queue)
    exhausted = pending > 0 and processed >= event_budget
    return BoundedExecutionResult(
        completed=not exhausted and not pair_stopped,
        budget_exhausted=exhausted,
        configured_event_budget=event_budget,
        processed_event_count=processed,
        pending_event_count=pending,
        termination_reason=("paired_stop" if pair_stopped else
                            "budget_exhausted" if exhausted else "completed"),
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