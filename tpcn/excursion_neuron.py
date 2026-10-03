"""ACP-0004 E1 static leaky accumulator and single-excursion reference."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from enum import Enum
import math
from numbers import Real
from typing import Deque

from .event_runtime import Event, EventQueue, EventType, LocalClock, PropagationDelay


P_MAX = 64


def _finite_real(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _positive(value: Real, name: str) -> float:
    result = _finite_real(value, name)
    if result <= 0.0:
        raise ValueError(f"{name} must be positive")
    return result


class E1Mode(str, Enum):
    N = "N"
    S_PENDING = "S_PENDING"
    S_RETURN = "S_RETURN"


class E1InternalEventKind(str, Enum):
    S_EMIT = "S_EMIT"
    S_REARM = "S_REARM"


class E1OutOfScopeBoundary(RuntimeError):
    """Raised when a neuron is used after reaching the unauthorized M boundary."""


class E1EventBudgetExceeded(RuntimeError):
    """Raised when the finite E1 execution budget is exhausted."""


@dataclass(frozen=True, slots=True)
class E1Config:
    """Validated finite parameters for the ACP-0004 E1 reference."""

    decay_rate: float = 1.0
    x_max: float = 8.0
    theta_r: float = 0.25
    theta_e: float = 1.0
    theta_hold: float = 1.5
    theta_m: float = 4.0
    emission_delay: float = 0.5
    a_min: float = 0.25
    a_max: float = 1.0
    provenance_capacity: int = 16
    event_budget: int = 4096

    def __post_init__(self) -> None:
        decay_rate = _positive(self.decay_rate, "decay_rate")
        x_max = _positive(self.x_max, "x_max")
        theta_r = _positive(self.theta_r, "theta_r")
        theta_e = _positive(self.theta_e, "theta_e")
        theta_hold = _positive(self.theta_hold, "theta_hold")
        theta_m = _positive(self.theta_m, "theta_m")
        emission_delay = _positive(self.emission_delay, "emission_delay")
        a_min = _positive(self.a_min, "a_min")
        a_max = _positive(self.a_max, "a_max")
        if not theta_r < theta_e <= theta_hold < theta_m <= x_max:
            raise ValueError("thresholds must satisfy theta_r < theta_e <= theta_hold < theta_m <= x_max")
        if a_min > a_max:
            raise ValueError("a_min must not exceed a_max")
        if (
            isinstance(self.provenance_capacity, bool)
            or not isinstance(self.provenance_capacity, int)
            or not 1 <= self.provenance_capacity <= P_MAX
        ):
            raise ValueError(f"provenance_capacity must be an integer in [1, {P_MAX}]")
        if (
            isinstance(self.event_budget, bool)
            or not isinstance(self.event_budget, int)
            or self.event_budget <= 0
        ):
            raise ValueError("event_budget must be a positive integer")
        object.__setattr__(self, "decay_rate", decay_rate)
        object.__setattr__(self, "x_max", x_max)
        object.__setattr__(self, "theta_r", theta_r)
        object.__setattr__(self, "theta_e", theta_e)
        object.__setattr__(self, "theta_hold", theta_hold)
        object.__setattr__(self, "theta_m", theta_m)
        object.__setattr__(self, "emission_delay", emission_delay)
        object.__setattr__(self, "a_min", a_min)
        object.__setattr__(self, "a_max", a_max)

    @property
    def lambda_(self) -> float:
        return self.decay_rate

    @property
    def X_max(self) -> float:
        return self.x_max

    @property
    def theta_R(self) -> float:
        return self.theta_r

    @property
    def theta_E(self) -> float:
        return self.theta_e

    @property
    def theta_M(self) -> float:
        return self.theta_m

    @property
    def Delta_t_E(self) -> float:
        return self.emission_delay


@dataclass(frozen=True, slots=True)
class ProvenanceEntry:
    event_id: str | int
    timestamp: float
    contribution: float
    episode_id: int | None = None
    lineage_id: int | None = None


@dataclass(frozen=True, slots=True)
class PendingInternalEvent:
    neuron_id: str
    episode_id: int
    generation: int
    kind: E1InternalEventKind
    timestamp: float
    queue_sequence: int = -1


@dataclass(frozen=True, slots=True)
class BoundaryReport:
    timestamp: float
    magnitude: float
    mode: E1Mode
    lineage_id: int | None
    reason: str = "M boundary is outside ACP-0004 E1 scope"


@dataclass(frozen=True, slots=True)
class ExcursionEmission:
    event_id: str
    sequence: int
    source: str
    timestamp: float
    payload: float
    lineage_id: int
    episode_id: int
    event_type: EventType = EventType.EXCURSION

    def as_event(self, destination: str) -> Event:
        return Event(
            self.timestamp,
            self.source,
            destination,
            self.event_type,
            self.payload,
            event_id=self.event_id,
            lineage_id=self.lineage_id,
        )

    def enqueue(
        self,
        queue: EventQueue[Event],
        destination: str,
        *,
        delay: PropagationDelay = 0.0,
    ) -> Event:
        return queue.push_propagated(
            self.timestamp,
            self.source,
            destination,
            self.event_type,
            self.payload,
            delay,
            event_id=self.event_id,
            lineage_id=self.lineage_id,
        )


class SingleExcursionNeuron:
    """A bounded E1 neuron with one ordinary excursion per admitted episode."""

    def __init__(
        self,
        neuron_id: str,
        *,
        config: E1Config | None = None,
        initial_state: Real = 0.0,
        initial_timestamp: Real = 0.0,
    ) -> None:
        if not isinstance(neuron_id, str) or not neuron_id:
            raise ValueError("neuron_id must be a non-empty string")
        self.config = config if config is not None else E1Config()
        if not isinstance(self.config, E1Config):
            raise TypeError("config must be an E1Config")
        initial = _finite_real(initial_state, "initial_state")
        if abs(initial) > self.config.x_max:
            raise ValueError("initial_state must be within [-x_max, x_max]")
        self.neuron_id = neuron_id
        self.clock = LocalClock(_finite_real(initial_timestamp, "initial_timestamp"))
        self.x = initial
        self.mode = E1Mode.N
        self.pending_internal_event: PendingInternalEvent | None = None
        self.generation_token = 0
        self.ordinary_episode_id: int | None = None
        self.lineage_id: int | None = None
        self.captured_polarity: int | None = None
        self.m_peak = 0.0
        self._provenance: Deque[ProvenanceEntry] = deque(maxlen=self.config.provenance_capacity)
        self.provenance_truncated = False
        self._unassigned_provenance_count = 0
        self._unassigned_provenance_truncated = False
        self.boundary_reports: Deque[BoundaryReport] = deque(maxlen=self.config.event_budget)
        self.emissions: Deque[ExcursionEmission] = deque(maxlen=self.config.event_budget)
        self.input_contribution_count = 0
        self.processed_event_count = 0
        self._event_identity = 0
        self._episode_identity = 0
        self._lineage_identity = 0
        self._input_identity = 0
        self.out_of_scope = False

    @property
    def state(self) -> float:
        return self.x

    @property
    def last_update_timestamp(self) -> float:
        return self.clock.timestamp

    @property
    def provenance(self) -> tuple[ProvenanceEntry, ...]:
        return tuple(self._provenance)

    @property
    def pending_event(self) -> PendingInternalEvent | None:
        return self.pending_internal_event

    @property
    def last_emission(self) -> ExcursionEmission | None:
        return self.emissions[-1] if self.emissions else None

    def reset(self, *, timestamp: Real = 0.0) -> None:
        """Reset bounded character-local state without reusing event identities."""
        reset_time = _finite_real(timestamp, "timestamp")
        self.generation_token = 0
        self.pending_internal_event = None
        self.clock = LocalClock(reset_time)
        self.x = 0.0
        self.mode = E1Mode.N
        self.ordinary_episode_id = None
        self.lineage_id = None
        self.captured_polarity = None
        self.m_peak = 0.0
        self._provenance.clear()
        self.provenance_truncated = False
        self._unassigned_provenance_count = 0
        self._unassigned_provenance_truncated = False
        self.boundary_reports.clear()
        self.emissions.clear()
        self.out_of_scope = False
        self.input_contribution_count = 0
        self.processed_event_count = 0

    def receive_event(
        self,
        event: Event,
        queue: EventQueue[Event] | None = None,
    ) -> ExcursionEmission | None:
        """Process one external or locally scheduled event."""
        if event.destination != self.neuron_id:
            raise ValueError("event destination does not address this neuron")
        if event.event_type == EventType.INTERNAL:
            return self._receive_internal(event, queue)
        if self.out_of_scope:
            raise E1OutOfScopeBoundary("neuron reached the unauthorized M boundary")
        if isinstance(event.payload, bool) or not isinstance(event.payload, Real):
            raise TypeError("E1 external contribution must be a real number")
        contribution = _finite_real(event.payload, "contribution")
        self._consume_budget()
        self._advance_to(event.timestamp)
        self.x = self._clip(self.x + contribution)
        self._record_provenance(event, contribution)
        self.input_contribution_count += 1
        self._update_after_external(queue)
        return None

    def receive_contribution(
        self,
        timestamp: Real,
        contribution: Real,
        *,
        source: str = "external",
        event_id: str | int | None = None,
        queue: EventQueue[Event] | None = None,
    ) -> ExcursionEmission | None:
        """Create and process a local external contribution."""
        if event_id is None:
            event_id = f"{self.neuron_id}:input:{self._input_identity}"
            self._input_identity += 1
        event = Event(timestamp, source, self.neuron_id, EventType.INPUT, contribution, event_id=event_id)
        return self.receive_event(event, queue)

    def process_pending(
        self,
        *,
        through: Real | None = None,
        queue: EventQueue[Event] | None = None,
    ) -> ExcursionEmission | None:
        """Process the valid pending internal event without a polling loop."""
        pending = self.pending_internal_event
        if pending is None:
            return None
        limit = pending.timestamp if through is None else _finite_real(through, "through")
        if pending.timestamp > limit:
            return None
        event = Event(
            pending.timestamp,
            self.neuron_id,
            self.neuron_id,
            EventType.INTERNAL,
            pending,
            sequence=pending.queue_sequence,
        )
        return self.receive_event(event, queue)

    def _receive_internal(
        self,
        event: Event,
        queue: EventQueue[Event] | None,
    ) -> ExcursionEmission | None:
        if not isinstance(event.payload, PendingInternalEvent):
            raise TypeError("internal E1 event payload is invalid")
        self._consume_budget()
        pending = self.pending_internal_event
        payload = event.payload
        if (
            pending is None
            or self.out_of_scope
            or payload.neuron_id != self.neuron_id
            or payload.episode_id != pending.episode_id
            or payload.generation != pending.generation
            or payload.kind != pending.kind
            or payload.timestamp != pending.timestamp
            or event.timestamp != pending.timestamp
            or (
                pending.queue_sequence >= 0
                and event.sequence >= 0
                and event.sequence != pending.queue_sequence
            )
        ):
            return None
        self.pending_internal_event = None
        self._advance_to(event.timestamp)
        if payload.kind == E1InternalEventKind.S_EMIT:
            return self._emit_ordinary(queue)
        return self._finish_rearm(queue)

    def _update_after_external(self, queue: EventQueue[Event] | None) -> None:
        magnitude = abs(self.x)
        if self.mode == E1Mode.N:
            if magnitude >= self.config.theta_m:
                self._report_boundary()
            elif magnitude >= self.config.theta_e:
                self._admit_ordinary(queue)
            return
        if self.mode == E1Mode.S_PENDING:
            self.m_peak = max(self.m_peak, magnitude)
            if magnitude >= self.config.theta_m:
                self._report_boundary()
            return
        self._cancel_pending()
        if magnitude >= self.config.theta_m:
            self._report_boundary()
        elif magnitude <= self.config.theta_r:
            self._close_episode()
        else:
            self._schedule(E1InternalEventKind.S_REARM, self.clock.timestamp + self._rearm_delay(magnitude), queue)

    def _admit_ordinary(self, queue: EventQueue[Event] | None) -> None:
        self._episode_identity += 1
        self._lineage_identity += 1
        self.ordinary_episode_id = self._episode_identity
        self.lineage_id = self._lineage_identity
        pending_provenance = tuple(
            entry for entry in self._provenance if entry.episode_id is None
        )
        self._provenance.clear()
        self.provenance_truncated = self._unassigned_provenance_truncated
        self._unassigned_provenance_count = 0
        self._unassigned_provenance_truncated = False
        self._provenance.extend(
            replace(
                entry,
                episode_id=self.ordinary_episode_id,
                lineage_id=self.lineage_id,
            )
            for entry in pending_provenance
        )
        self.captured_polarity = 1 if self.x > 0.0 else -1
        self.m_peak = abs(self.x)
        self.mode = E1Mode.S_PENDING
        self._schedule(
            E1InternalEventKind.S_EMIT,
            self.clock.timestamp + self.config.emission_delay,
            queue,
        )

    def _emit_ordinary(self, queue: EventQueue[Event] | None) -> ExcursionEmission | None:
        if self.mode != E1Mode.S_PENDING or self.ordinary_episode_id is None or self.lineage_id is None:
            return None
        self.m_peak = max(self.m_peak, abs(self.x))
        span = self.config.theta_m - self.config.theta_e
        fraction = max(0.0, min(1.0, (self.m_peak - self.config.theta_e) / span))
        amplitude = self.config.a_min + (self.config.a_max - self.config.a_min) * fraction
        payload = float(self.captured_polarity or 1) * amplitude
        self._event_identity += 1
        emission = ExcursionEmission(
            event_id=f"{self.neuron_id}:excursion:{self._event_identity}",
            sequence=self._event_identity,
            source=self.neuron_id,
            timestamp=self.clock.timestamp,
            payload=payload,
            lineage_id=self.lineage_id,
            episode_id=self.ordinary_episode_id,
        )
        self.emissions.append(emission)
        self.mode = E1Mode.S_RETURN
        magnitude = abs(self.x)
        if magnitude <= self.config.theta_r:
            self._close_episode()
        else:
            self._schedule(
                E1InternalEventKind.S_REARM,
                self.clock.timestamp + self._rearm_delay(magnitude),
                queue,
            )
        return emission

    def _finish_rearm(self, queue: EventQueue[Event] | None) -> None:
        magnitude = abs(self.x)
        if magnitude <= self.config.theta_r:
            self._close_episode()
            return None
        if magnitude - self.config.theta_r <= math.ulp(self.config.theta_r):
            self.x = math.copysign(self.config.theta_r, self.x)
            self._close_episode()
            return None
        self._schedule(
            E1InternalEventKind.S_REARM,
            self.clock.timestamp + self._rearm_delay(magnitude),
            queue,
        )
        return None

    def _schedule(
        self,
        kind: E1InternalEventKind,
        timestamp: float,
        queue: EventQueue[Event] | None,
    ) -> None:
        if self.ordinary_episode_id is None:
            raise RuntimeError("cannot schedule an E1 event without an ordinary episode")
        self._advance_generation()
        candidate = PendingInternalEvent(
            self.neuron_id,
            self.ordinary_episode_id,
            self.generation_token,
            kind,
            timestamp,
        )
        if queue is not None:
            queued = queue.push(
                Event(
                    timestamp,
                    self.neuron_id,
                    self.neuron_id,
                    EventType.INTERNAL,
                    candidate,
                )
            )
            candidate = replace(candidate, queue_sequence=queued.sequence)
        self.pending_internal_event = candidate

    def _cancel_pending(self) -> None:
        if self.pending_internal_event is not None:
            self._advance_generation()
            self.pending_internal_event = None

    def _advance_generation(self) -> None:
        if self.generation_token >= self.config.event_budget:
            raise E1EventBudgetExceeded("E1 generation budget exhausted")
        self.generation_token += 1

    def _consume_budget(self) -> None:
        if self.processed_event_count >= self.config.event_budget:
            raise E1EventBudgetExceeded("E1 event budget exhausted")
        self.processed_event_count += 1

    def _advance_to(self, timestamp: float) -> None:
        elapsed = self.clock.advance_to(timestamp)
        if elapsed:
            self.x = self._clip(self.x * math.exp(-self.config.decay_rate * elapsed))

    def _record_provenance(self, event: Event, contribution: float) -> None:
        event_id: str | int
        if event.event_id is not None:
            event_id = event.event_id
        elif event.sequence >= 0:
            event_id = f"{event.source}:{event.sequence}"
        else:
            event_id = f"{event.source}:input:{self._input_identity}"
            self._input_identity += 1
        active_episode = self.ordinary_episode_id if self.mode != E1Mode.N else None
        active_lineage = self.lineage_id if self.mode != E1Mode.N else None
        if active_episode is None:
            self._unassigned_provenance_count += 1
            if self._unassigned_provenance_count > self.config.provenance_capacity:
                self._unassigned_provenance_truncated = True
        if len(self._provenance) == self._provenance.maxlen:
            self.provenance_truncated = True
        self._provenance.append(
            ProvenanceEntry(
                event_id,
                event.timestamp,
                contribution,
                active_episode,
                active_lineage,
            )
        )

    def _report_boundary(self) -> None:
        self.boundary_reports.append(
            BoundaryReport(
                self.clock.timestamp,
                abs(self.x),
                self.mode,
                self.lineage_id,
            )
        )
        self.out_of_scope = True
        self._cancel_pending()

    def _close_episode(self) -> None:
        self.mode = E1Mode.N
        self.pending_internal_event = None
        self.ordinary_episode_id = None
        self.lineage_id = None
        self.captured_polarity = None
        self.m_peak = 0.0
        self._unassigned_provenance_count = 0
        self._unassigned_provenance_truncated = False

    def _rearm_delay(self, magnitude: float) -> float:
        return math.log(magnitude / self.config.theta_r) / self.config.decay_rate

    def _clip(self, value: float) -> float:
        return max(-self.config.x_max, min(self.config.x_max, value))


E1Neuron = SingleExcursionNeuron
CanonicalExcursionNeuron = SingleExcursionNeuron


__all__ = [
    "P_MAX",
    "E1Config",
    "E1Mode",
    "E1InternalEventKind",
    "E1OutOfScopeBoundary",
    "E1EventBudgetExceeded",
    "ProvenanceEntry",
    "PendingInternalEvent",
    "BoundaryReport",
    "ExcursionEmission",
    "SingleExcursionNeuron",
    "E1Neuron",
    "CanonicalExcursionNeuron",
]
