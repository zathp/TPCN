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
    M_ACTIVE = "M_ACTIVE"


class E1InternalEventKind(str, Enum):
    S_EMIT = "S_EMIT"
    S_REARM = "S_REARM"
    M_EMIT = "M_EMIT"
    M_REARM = "M_REARM"


class MPhase(str, Enum):
    ARMED = "ARMED"
    REFRACTORY = "REFRACTORY"


class E1OutOfScopeBoundary(RuntimeError):
    """Raised when a neuron is used after reaching the unauthorized M boundary."""


class E1EventBudgetExceeded(RuntimeError):
    """Raised when the finite E1 execution budget is exhausted."""


@dataclass(frozen=True, slots=True)
class IntegrationConfig:
    """ACP-0008 opt-in slow integration state parameters (experimental)."""

    decay_rate_z: float = 0.1
    input_gain: float = 1.0
    discharge_quantum: float = 1.0
    z_max: float = 4.0

    def __post_init__(self) -> None:
        for name in ("decay_rate_z", "input_gain", "discharge_quantum", "z_max"):
            object.__setattr__(self, name, _positive(getattr(self, name), name))
        if self.discharge_quantum > self.z_max:
            raise ValueError("discharge_quantum must not exceed z_max")

    @property
    def lambda_z(self) -> float:
        return self.decay_rate_z

    @property
    def kappa(self) -> float:
        return self.input_gain

    @property
    def theta_Z(self) -> float:
        return self.discharge_quantum

    @property
    def Z_max(self) -> float:
        return self.z_max


@dataclass(frozen=True, slots=True)
class E1Config:
    """Validated E1 parameters and bounded M settings consumed by E2 only."""

    decay_rate: float = 1.0
    x_max: float = 8.0
    theta_r: float = 0.25
    theta_e: float = 1.0
    theta_hold: float = 1.5
    theta_m: float = 4.0
    emission_delay: float = 0.5
    m_emit_delay: float = 1.0
    m_rearm_delay: float = 1.0
    delta_x_e: float = 1.0
    a_min: float = 0.25
    a_max: float = 1.0
    provenance_capacity: int = 16
    event_budget: int = 4096
    integration: IntegrationConfig | None = None

    def __post_init__(self) -> None:
        decay_rate = _positive(self.decay_rate, "decay_rate")
        x_max = _positive(self.x_max, "x_max")
        theta_r = _positive(self.theta_r, "theta_r")
        theta_e = _positive(self.theta_e, "theta_e")
        theta_hold = _positive(self.theta_hold, "theta_hold")
        theta_m = _positive(self.theta_m, "theta_m")
        emission_delay = _positive(self.emission_delay, "emission_delay")
        m_emit_delay = _positive(self.m_emit_delay, "m_emit_delay")
        m_rearm_delay = _positive(self.m_rearm_delay, "m_rearm_delay")
        delta_x_e = _positive(self.delta_x_e, "delta_x_e")
        a_min = _positive(self.a_min, "a_min")
        a_max = _positive(self.a_max, "a_max")
        if not theta_r < theta_e <= theta_hold < theta_m <= x_max:
            raise ValueError("thresholds must satisfy theta_r < theta_e <= theta_hold < theta_m <= x_max")
        if delta_x_e > x_max:
            raise ValueError("delta_x_e must not exceed x_max")
        if self.integration is not None:
            integration = self.integration
            if not isinstance(integration, IntegrationConfig):
                raise TypeError("integration must be an IntegrationConfig or None")
            if not integration.decay_rate_z < decay_rate:
                raise ValueError("decay_rate_z must be smaller than decay_rate")
            if integration.discharge_quantum < theta_e:
                raise ValueError("discharge_quantum (theta_Z) must be at least theta_e")
            if not theta_e + integration.discharge_quantum < theta_m:
                raise ValueError("theta_e + discharge_quantum must be below theta_m")
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
        object.__setattr__(self, "m_emit_delay", m_emit_delay)
        object.__setattr__(self, "m_rearm_delay", m_rearm_delay)
        object.__setattr__(self, "delta_x_e", delta_x_e)
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


@dataclass(slots=True)
class IntegrationTraceEntry:
    """Per-external-event ACP-0008 diagnostic record (emission fields filled when the episode emits)."""

    timestamp: float
    elapsed: float
    input_value: float
    theta_e: float
    theta_z: float
    decay_rate: float
    decay_rate_z: float
    mode_before: E1Mode
    x_before_decay: float
    x_after_decay: float
    z_before_decay: float
    z_after_decay: float
    x_after_input: float
    z_after_input: float
    integrated: bool
    discharge_amount: float
    x_post_discharge: float
    z_post_discharge: float
    crossed_theta_e: bool
    admitted_episode_id: int | None
    classification: str
    emission_id: str | None = None
    emission_timestamp: float | None = None
    x_at_emission: float | None = None
    z_at_emission: float | None = None


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
        self._z = 0.0
        self._integration_trace: Deque[IntegrationTraceEntry] = deque(maxlen=self.config.event_budget)
        self._trace_by_episode: dict[int, IntegrationTraceEntry] = {}

    @property
    def integration_state(self) -> float | None:
        """Slow state z; None when integration is disabled."""
        return self._z if self.config.integration is not None else None

    @property
    def integration_trace(self) -> tuple[IntegrationTraceEntry, ...]:
        return tuple(self._integration_trace)

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
    def _active_episode_identity(self) -> int | None:
        return self.ordinary_episode_id

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
        self._z = 0.0
        self._integration_trace.clear()
        self._trace_by_episode.clear()

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
        integration = self.config.integration
        if integration is None:
            self._advance_to(event.timestamp)
            self.x = self._clip(self.x + contribution)
            self._record_provenance(event, contribution)
            self.input_contribution_count += 1
            self._update_after_external(queue)
            return None
        mode_before = self.mode
        x_before = self.x
        z_before = self._z
        previous = self.clock.timestamp
        self._advance_to(event.timestamp)
        x_decayed = self.x
        z_decayed = self._z
        self.x = self._clip(self.x + contribution)
        self._record_provenance(event, contribution)
        self.input_contribution_count += 1
        x_input = self.x
        integrated = False
        discharge = 0.0
        if mode_before == E1Mode.N and abs(self.x) < self.config.theta_e:
            integrated = True
            z_limit = integration.z_max
            self._z = max(-z_limit, min(z_limit, self._z + integration.input_gain * contribution))
        z_input = self._z
        if integrated and abs(self._z) >= integration.discharge_quantum and self.x * self._z >= 0.0:
            sign = 1.0 if self._z > 0.0 else -1.0
            discharge = sign * integration.discharge_quantum
            self._z -= discharge
            self.x = self._clip(self.x + discharge)
        x_post = self.x
        z_post = self._z
        episode_before = self.ordinary_episode_id
        self._update_after_external(queue)
        admitted = (
            self._admitted_from(mode_before, episode_before)
        )
        episode = self.ordinary_episode_id if admitted else None
        if admitted:
            classification = "integrated_discharge" if discharge != 0.0 else "direct"
        else:
            classification = "none"
        entry = IntegrationTraceEntry(
            timestamp=event.timestamp,
            elapsed=event.timestamp - previous,
            input_value=contribution,
            theta_e=self.config.theta_e,
            theta_z=integration.discharge_quantum,
            decay_rate=self.config.decay_rate,
            decay_rate_z=integration.decay_rate_z,
            mode_before=mode_before,
            x_before_decay=x_before,
            x_after_decay=x_decayed,
            z_before_decay=z_before,
            z_after_decay=z_decayed,
            x_after_input=x_input,
            z_after_input=z_input,
            integrated=integrated,
            discharge_amount=discharge,
            x_post_discharge=x_post,
            z_post_discharge=z_post,
            crossed_theta_e=abs(x_post) >= self.config.theta_e,
            admitted_episode_id=episode,
            classification=classification,
        )
        self._integration_trace.append(entry)
        if episode is not None:
            self._trace_by_episode[episode] = entry
        return None

    def _admitted_from(self, mode_before: E1Mode, episode_before: int | None) -> bool:
        return (
            mode_before == E1Mode.N
            and self.mode == E1Mode.S_PENDING
            and self.ordinary_episode_id is not None
            and self.ordinary_episode_id != episode_before
        )

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
            or event.source != self.neuron_id
            or payload.neuron_id != self.neuron_id
            or payload.episode_id != self._active_episode_identity
            or payload.episode_id != pending.episode_id
            or payload.generation != pending.generation
            or payload.kind != pending.kind
            or payload.timestamp != pending.timestamp
            or event.timestamp != pending.timestamp
            or event.sequence != pending.queue_sequence
            or (
                payload.kind == E1InternalEventKind.M_EMIT
                and getattr(self, "m_phase", None) != MPhase.ARMED
            )
            or (
                payload.kind == E1InternalEventKind.M_REARM
                and getattr(self, "m_phase", None) != MPhase.REFRACTORY
            )
        ):
            return None
        self.pending_internal_event = None
        self._advance_to(event.timestamp)
        if payload.kind == E1InternalEventKind.S_EMIT:
            return self._emit_ordinary(queue)
        if payload.kind == E1InternalEventKind.S_REARM:
            return self._finish_rearm(queue)
        return self._handle_m_internal(payload.kind, queue)

    def _handle_m_internal(
        self,
        kind: E1InternalEventKind,
        queue: EventQueue[Event] | None,
    ) -> ExcursionEmission | None:
        del queue
        if self.mode == E1Mode.M_ACTIVE:
            raise E1OutOfScopeBoundary(
                f"{kind.value} requires the E2 MultiExcursionNeuron runtime"
            )
        return None

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
        traced = self._trace_by_episode.pop(self.ordinary_episode_id, None)
        if traced is not None:
            traced.emission_id = emission.event_id
            traced.emission_timestamp = emission.timestamp
            traced.x_at_emission = self.x
            traced.z_at_emission = self._z
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
        episode_id = self._active_episode_identity
        if episode_id is None:
            raise RuntimeError("cannot schedule an internal event without an active episode")
        self._advance_generation()
        candidate = PendingInternalEvent(
            self.neuron_id,
            episode_id,
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
            if self.config.integration is not None:
                self._z *= math.exp(-self.config.integration.decay_rate_z * elapsed)

    def _record_provenance(self, event: Event, contribution: float) -> None:
        event_id: str | int
        if event.event_id is not None:
            event_id = event.event_id
        elif event.sequence >= 0:
            event_id = f"{event.source}:{event.sequence}"
        else:
            event_id = f"{event.source}:input:{self._input_identity}"
            self._input_identity += 1
        active_episode = self._active_episode_identity if self.mode != E1Mode.N else None
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


class MultiExcursionNeuron(SingleExcursionNeuron):
    """ACP-0004 E2 reference with bounded, event-driven M excursions."""

    def __init__(
        self,
        neuron_id: str,
        *,
        config: E1Config | None = None,
        initial_state: Real = 0.0,
        initial_timestamp: Real = 0.0,
    ) -> None:
        super().__init__(
            neuron_id,
            config=config,
            initial_state=initial_state,
            initial_timestamp=initial_timestamp,
        )
        self.m_phase: MPhase | None = None
        self.multi_episode_id: int | None = None

    @property
    def _active_episode_identity(self) -> int | None:
        if self.mode == E1Mode.M_ACTIVE:
            return self.multi_episode_id
        return self.ordinary_episode_id

    def reset(self, *, timestamp: Real = 0.0) -> None:
        super().reset(timestamp=timestamp)
        self.m_phase = None
        self.multi_episode_id = None

    def receive_contribution(
        self,
        timestamp: Real,
        contribution: Real,
        *,
        source: str = "external",
        event_id: str | int | None = None,
        queue: EventQueue[Event] | None = None,
    ) -> ExcursionEmission | None:
        if event_id is None:
            self._require_identity_capacity(self._input_identity, "input")
        return super().receive_contribution(
            timestamp,
            contribution,
            source=source,
            event_id=event_id,
            queue=queue,
        )

    def _require_identity_capacity(self, current: int, name: str) -> None:
        if current >= self.config.event_budget:
            raise E1EventBudgetExceeded(f"E2 {name} identity budget exhausted")

    def _update_after_external(self, queue: EventQueue[Event] | None) -> None:
        magnitude = abs(self.x)
        if self.mode == E1Mode.N:
            if magnitude >= self.config.theta_m:
                self._admit_multi(queue, preserve_lineage=False)
            elif magnitude >= self.config.theta_e:
                self._admit_ordinary(queue)
            return
        if self.mode == E1Mode.S_PENDING:
            self.m_peak = max(self.m_peak, magnitude)
            if magnitude >= self.config.theta_m:
                self._cancel_pending()
                self._admit_multi(queue, preserve_lineage=True)
            return
        if self.mode == E1Mode.S_RETURN:
            self._cancel_pending()
            if magnitude >= self.config.theta_m:
                self._admit_multi(queue, preserve_lineage=True)
            elif magnitude <= self.config.theta_r:
                self._close_episode()
            else:
                self._schedule(
                    E1InternalEventKind.S_REARM,
                    self.clock.timestamp + self._rearm_delay(magnitude),
                    queue,
                )
            return

        if self.mode != E1Mode.M_ACTIVE:
            raise RuntimeError(f"unsupported E2 mode: {self.mode!r}")
        if self.m_phase not in (MPhase.ARMED, MPhase.REFRACTORY):
            raise RuntimeError("M_ACTIVE requires a valid M phase")
        self._cancel_pending()
        if magnitude <= self.config.theta_hold:
            if magnitude >= self.config.theta_e:
                self._finish_m_to_ordinary(queue)
            else:
                self._close_episode()
        else:
            kind = (
                E1InternalEventKind.M_EMIT
                if self.m_phase == MPhase.ARMED
                else E1InternalEventKind.M_REARM
            )
            delay = (
                self.config.m_emit_delay
                if kind == E1InternalEventKind.M_EMIT
                else self.config.m_rearm_delay
            )
            self._schedule(kind, self.clock.timestamp + delay, queue)

    def _schedule(
        self,
        kind: E1InternalEventKind,
        timestamp: float,
        queue: EventQueue[Event] | None,
    ) -> None:
        due_time = _finite_real(timestamp, "internal event timestamp")
        if due_time <= self.clock.timestamp:
            if (
                due_time == self.clock.timestamp
                and kind == E1InternalEventKind.S_REARM
                and abs(self.x) > self.config.theta_r
            ):
                analytic_delay = self._rearm_delay(abs(self.x))
                if (
                    math.isfinite(analytic_delay)
                    and analytic_delay > 0.0
                    and self.clock.timestamp + analytic_delay == due_time
                ):
                    due_time = math.nextafter(self.clock.timestamp, math.inf)
            if not math.isfinite(due_time) or due_time <= self.clock.timestamp:
                raise ValueError("E2 internal events require a finite positive logical delay")
        super()._schedule(kind, due_time, queue)

    def _record_provenance(self, event: Event, contribution: float) -> None:
        if event.event_id is None and event.sequence < 0:
            self._require_identity_capacity(self._input_identity, "input")
        super()._record_provenance(event, contribution)

    def _admit_ordinary(self, queue: EventQueue[Event] | None) -> None:
        self._require_identity_capacity(self._episode_identity, "episode")
        self._require_identity_capacity(self._lineage_identity, "lineage")
        super()._admit_ordinary(queue)

    def _admit_multi(
        self,
        queue: EventQueue[Event] | None,
        *,
        preserve_lineage: bool,
    ) -> None:
        needs_lineage = not preserve_lineage or self.lineage_id is None
        if needs_lineage:
            self._require_identity_capacity(self._lineage_identity, "lineage")
        self._require_identity_capacity(self._episode_identity, "episode")
        if self.pending_internal_event is not None:
            self._cancel_pending()
        if needs_lineage:
            self._lineage_identity += 1
            self.lineage_id = self._lineage_identity
        self._episode_identity += 1
        self.multi_episode_id = self._episode_identity
        self.ordinary_episode_id = None
        self.captured_polarity = None
        self.m_peak = max(self.m_peak, abs(self.x))
        if not preserve_lineage:
            unassigned = tuple(
                entry for entry in self._provenance if entry.episode_id is None
            )
            self._provenance.clear()
            self._provenance.extend(unassigned)
            self.provenance_truncated = self._unassigned_provenance_truncated
        else:
            self.provenance_truncated = (
                self.provenance_truncated or self._unassigned_provenance_truncated
            )
        self._unassigned_provenance_count = 0
        self._unassigned_provenance_truncated = False
        self._reown_provenance(self.multi_episode_id)
        self.mode = E1Mode.M_ACTIVE
        self.m_phase = MPhase.ARMED
        self._schedule(
            E1InternalEventKind.M_EMIT,
            self.clock.timestamp + self.config.m_emit_delay,
            queue,
        )

    def _handle_m_internal(
        self,
        kind: E1InternalEventKind,
        queue: EventQueue[Event] | None,
    ) -> ExcursionEmission | None:
        if self.mode != E1Mode.M_ACTIVE or self.multi_episode_id is None:
            return None
        magnitude = abs(self.x)
        if kind == E1InternalEventKind.M_REARM:
            if magnitude > self.config.theta_hold:
                self.m_phase = MPhase.ARMED
                self._schedule(
                    E1InternalEventKind.M_EMIT,
                    self.clock.timestamp + self.config.m_emit_delay,
                    queue,
                )
            elif magnitude >= self.config.theta_e:
                self._finish_m_to_ordinary(queue)
            else:
                self._close_episode()
            return None
        if kind != E1InternalEventKind.M_EMIT:
            return None
        if magnitude <= self.config.theta_hold:
            if magnitude >= self.config.theta_e:
                self._finish_m_to_ordinary(queue)
            else:
                self._close_episode()
            return None

        if self.lineage_id is None:
            raise RuntimeError("M episode has no causal lineage")
        self._require_identity_capacity(self._event_identity, "output-event")
        self._event_identity += 1
        emission = ExcursionEmission(
            event_id=f"{self.neuron_id}:excursion:{self._event_identity}",
            sequence=self._event_identity,
            source=self.neuron_id,
            timestamp=self.clock.timestamp,
            payload=math.copysign(self.config.a_max, self.x),
            lineage_id=self.lineage_id,
            episode_id=self.multi_episode_id,
        )
        self.emissions.append(emission)
        remaining = max(self.config.theta_hold, magnitude - self.config.delta_x_e)
        self.x = math.copysign(remaining, self.x)
        if remaining <= self.config.theta_hold:
            self._finish_m_to_ordinary(queue)
        else:
            self.m_phase = MPhase.REFRACTORY
            self._schedule(
                E1InternalEventKind.M_REARM,
                self.clock.timestamp + self.config.m_rearm_delay,
                queue,
            )
        return emission

    def _finish_m_to_ordinary(self, queue: EventQueue[Event] | None) -> None:
        if self.lineage_id is None:
            raise RuntimeError("M episode has no causal lineage")
        self._require_identity_capacity(self._episode_identity, "episode")
        if self.pending_internal_event is not None:
            self._cancel_pending()
        self._episode_identity += 1
        self.ordinary_episode_id = self._episode_identity
        self.multi_episode_id = None
        self.m_phase = None
        self.captured_polarity = 1 if self.x > 0.0 else -1
        self.m_peak = abs(self.x)
        self._reown_provenance(self.ordinary_episode_id)
        self.mode = E1Mode.S_PENDING
        self._schedule(
            E1InternalEventKind.S_EMIT,
            self.clock.timestamp + self.config.emission_delay,
            queue,
        )

    def _reown_provenance(self, episode_id: int) -> None:
        if self.lineage_id is None:
            raise RuntimeError("cannot assign provenance without a lineage")
        retained = tuple(
            replace(entry, episode_id=episode_id, lineage_id=self.lineage_id)
            for entry in self._provenance
        )
        self._provenance.clear()
        self._provenance.extend(retained)

    def _emit_ordinary(self, queue: EventQueue[Event] | None) -> ExcursionEmission | None:
        self._require_identity_capacity(self._event_identity, "output-event")
        return super()._emit_ordinary(queue)

    def _close_episode(self) -> None:
        was_multi = self.mode == E1Mode.M_ACTIVE
        super()._close_episode()
        self.multi_episode_id = None
        self.m_phase = None
        if was_multi:
            self._provenance.clear()
            self.provenance_truncated = False


__all__ = [
    "P_MAX",
    "E1Config",
    "E1Mode",
    "E1InternalEventKind",
    "MPhase",
    "E1OutOfScopeBoundary",
    "E1EventBudgetExceeded",
    "ProvenanceEntry",
    "PendingInternalEvent",
    "BoundaryReport",
    "ExcursionEmission",
    "SingleExcursionNeuron",
    "E1Neuron",
    "CanonicalExcursionNeuron",
    "MultiExcursionNeuron",
]
