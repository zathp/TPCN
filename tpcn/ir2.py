"""TPCN-IR-2 schema and ACP-0004 E1 conversion helpers.

IR-2 is a bounded transfer representation, not a complete live-runtime
checkpoint.  It deliberately has no backend, calibration, prediction,
eligibility, reward, energy, or visualization state.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import json
import math
from numbers import Real
from typing import Any, Mapping

from .excursion_neuron import (
    E1Config,
    E1InternalEventKind,
    E1Mode,
    MPhase as E2MPhase,
    MultiExcursionNeuron,
    PendingInternalEvent,
    ProvenanceEntry,
    SingleExcursionNeuron,
)
from .execution_ir import ExecutionIR, IREvent


IR2_VERSION = "TPCN-IR-2"
IR2_SCHEMA_REVISION = 1
TANH_LEGACY = "TANH_LEGACY"
EXCURSION_V1 = "EXCURSION_V1"
SUPPORTED_DYNAMICS_MODELS = frozenset({TANH_LEGACY, EXCURSION_V1})
EXECUTION_ORDER_POLICY = "DESTINATION_LOCAL_EXTERNAL_BEFORE_INTERNAL_V1"
IR2_TPCV_SEPARATION = "TPCV-1 is downstream-only visualization and is not TPCN-IR-2."


class IR2UnsupportedRuntimeError(RuntimeError):
    """The schema is valid, but the current reference runtime cannot execute it."""


class IR2DowngradeError(ValueError):
    """An IR-2 record cannot be represented losslessly by IR-1."""


def _finite(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _id(value: object, name: str, *, allow_none: bool = False) -> int | None:
    if value is None and allow_none:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _positive_int(value: object, name: str) -> int:
    result = _id(value, name)
    assert result is not None
    if result == 0:
        raise ValueError(f"{name} must be positive")
    return result


class IR2Mode(str, Enum):
    N = "N"
    S_PENDING = "S_PENDING"
    S_RETURN = "S_RETURN"
    M_ACTIVE = "M_ACTIVE"


class MPhase(str, Enum):
    ARMED = "ARMED"
    REFRACTORY = "REFRACTORY"


class IR2PendingKind(str, Enum):
    S_EMIT = "S_EMIT"
    S_REARM = "S_REARM"
    M_EMIT = "M_EMIT"
    M_REARM = "M_REARM"


@dataclass(frozen=True, slots=True)
class IR2Edge:
    source: str
    destination: str
    w: float
    d: float
    r: float
    propagation_delay: float
    routing_metadata: Mapping[str, Any] | None = None
    routing_cost: int = 1
    legacy_identity: bool = True

    def __post_init__(self) -> None:
        _text(self.source, "source")
        _text(self.destination, "destination")
        w, d, r, delay = (_finite(v, n) for v, n in (
            (self.w, "w"), (self.d, "d"), (self.r, "r"),
            (self.propagation_delay, "propagation_delay"),
        ))
        if not -2.0 <= w <= 2.0 or not 0.0 <= d <= 1.0 or not -1.0 <= r <= 1.0:
            raise ValueError("invalid Model-B edge bounds")
        if delay <= 0.0:
            raise ValueError("propagation_delay must be positive")
        _positive_int(self.routing_cost, "routing_cost")
        if not isinstance(self.legacy_identity, bool):
            raise TypeError("legacy_identity must be a boolean")
        object.__setattr__(self, "w", w)
        object.__setattr__(self, "d", d)
        object.__setattr__(self, "r", r)
        object.__setattr__(self, "propagation_delay", delay)
        if self.routing_metadata is not None:
            if not isinstance(self.routing_metadata, Mapping):
                raise TypeError("routing_metadata must be a mapping")
            json.dumps(self.routing_metadata, sort_keys=True, allow_nan=False)


@dataclass(frozen=True, slots=True)
class IR2Provenance:
    causal_event_id: str | int
    timestamp: float
    signed_contribution: float
    episode_id: int | None
    lineage_id: int | None

    def __post_init__(self) -> None:
        if isinstance(self.causal_event_id, bool) or not isinstance(self.causal_event_id, (str, int)):
            raise TypeError("causal_event_id must be a string or integer")
        if isinstance(self.causal_event_id, str) and not self.causal_event_id:
            raise ValueError("causal_event_id must not be empty")
        _finite(self.timestamp, "timestamp")
        _finite(self.signed_contribution, "signed_contribution")
        _id(self.episode_id, "episode_id", allow_none=True)
        _id(self.lineage_id, "lineage_id", allow_none=True)


@dataclass(frozen=True, slots=True)
class IR2PendingInternal:
    neuron_id: str
    kind: IR2PendingKind
    timestamp: float
    episode_id: int
    generation: int
    queue_sequence: int = -1

    def __post_init__(self) -> None:
        _text(self.neuron_id, "neuron_id")
        object.__setattr__(self, "kind", IR2PendingKind(self.kind))
        _finite(self.timestamp, "timestamp")
        _positive_int(self.episode_id, "episode_id")
        _positive_int(self.generation, "generation")
        if self.queue_sequence < -1:
            raise ValueError("queue_sequence must be -1 or nonnegative")
        if self.queue_sequence != -1:
            _id(self.queue_sequence, "queue_sequence")


@dataclass(frozen=True, slots=True)
class IR2Event:
    timestamp: float
    source: str
    destination: str
    event_type: str
    payload: Any
    sequence: int = -1

    def __post_init__(self) -> None:
        if _finite(self.timestamp, "timestamp") < 0.0:
            raise ValueError("timestamp must be nonnegative")
        _text(self.source, "source")
        _text(self.destination, "destination")
        _text(self.event_type, "event_type")
        json.dumps(self.payload, allow_nan=False)
        if self.sequence < -1 or (self.sequence != -1 and _id(self.sequence, "sequence") is None):
            raise ValueError("sequence must be -1 or nonnegative")


@dataclass(frozen=True, slots=True)
class IR2Neuron:
    neuron_id: str
    dynamics_model: str = EXCURSION_V1
    x: float = 0.0
    local_last_update_time: float = 0.0
    mode: IR2Mode = IR2Mode.N
    decay_rate: float = 1.0
    x_max: float = 8.0
    theta_r: float = 0.25
    theta_e: float = 1.0
    theta_hold: float = 1.5
    theta_m: float = 4.0
    delta_t_e: float = 0.5
    delta_t_m_emit: float | None = 1.0
    delta_t_m_rearm: float | None = 1.0
    delta_x_e: float | None = 1.0
    a_min: float = 0.25
    a_max: float = 1.0
    provenance_capacity: int = 16
    event_budget: int = 4096
    ordinary_episode_id: int | None = None
    lineage_id: int | None = None
    captured_polarity: int | None = None
    m_peak: float = 0.0
    m_phase: MPhase | None = None
    multi_episode_id: int | None = None
    pending_internal_event: IR2PendingInternal | None = None
    provenance: tuple[IR2Provenance, ...] = ()
    provenance_truncated: bool = False
    generation_token: int = 0
    next_event_identity: int = 0
    next_episode_identity: int = 0
    next_lineage_identity: int = 0
    next_input_identity: int = 0
    processed_event_count: int = 0
    input_contribution_count: int = 0
    neuron_gain: float = 1.0
    unassigned_provenance_count: int = 0
    unassigned_provenance_truncated: bool = False

    def __post_init__(self) -> None:
        _text(self.neuron_id, "neuron_id")
        if self.dynamics_model not in SUPPORTED_DYNAMICS_MODELS:
            raise ValueError(f"unsupported dynamics_model: {self.dynamics_model!r}")
        object.__setattr__(self, "mode", IR2Mode(self.mode))
        if self.m_phase is not None:
            object.__setattr__(self, "m_phase", MPhase(self.m_phase))
        x = _finite(self.x, "x")
        timestamp = _finite(self.local_last_update_time, "local_last_update_time")
        if timestamp < 0.0:
            raise ValueError("local_last_update_time must be nonnegative")
        values = {name: _finite(getattr(self, name), name) for name in (
            "decay_rate", "x_max", "theta_r", "theta_e", "theta_hold", "theta_m",
            "delta_t_e", "a_min", "a_max", "neuron_gain",
        )}
        optional_values = {}
        for name in ("delta_t_m_emit", "delta_t_m_rearm", "delta_x_e"):
            value = getattr(self, name)
            optional_values[name] = None if value is None else _finite(value, name)
        has_m_configuration = any(value is not None for value in optional_values.values())
        if has_m_configuration and not all(
            value is not None for value in optional_values.values()
        ):
            raise ValueError("M timing and discharge configuration must be complete")
        if has_m_configuration and any(
            value <= 0.0 for value in optional_values.values() if value is not None
        ):
            raise ValueError("M timing and discharge configuration must be positive")
        if (
            optional_values["delta_x_e"] is not None
            and optional_values["delta_x_e"] > values["x_max"]
        ):
            raise ValueError("delta_x_e must not exceed x_max")
        if values["decay_rate"] < 0 or values["x_max"] <= 0:
            raise ValueError("decay_rate must be nonnegative and x_max positive")
        if self.dynamics_model == EXCURSION_V1 and values["decay_rate"] == 0:
            raise ValueError("decay_rate must be positive for EXCURSION_V1")
        if self.dynamics_model == EXCURSION_V1 and not (
            values["theta_r"] < values["theta_e"] <= values["theta_hold"]
            < values["theta_m"] <= values["x_max"]
        ):
            raise ValueError("invalid threshold ordering")
        if self.dynamics_model == EXCURSION_V1 and values["delta_t_e"] <= 0:
            raise ValueError("all delays must be positive")
        if self.dynamics_model == EXCURSION_V1 and (
            optional_values["delta_x_e"] is not None
            and not 0 < optional_values["delta_x_e"] <= values["x_max"]
            or not 0 < values["a_min"] <= values["a_max"]
        ):
            raise ValueError("invalid excursion bounds")
        if self.dynamics_model == EXCURSION_V1 and not 0.0 <= values["neuron_gain"] <= 2.0:
            raise ValueError("neuron_gain must be within [0, 2]")
        if self.mode == IR2Mode.M_ACTIVE and (
            optional_values["delta_t_m_emit"] is None
            or optional_values["delta_t_m_rearm"] is None
            or optional_values["delta_x_e"] is None
            or optional_values["delta_t_m_emit"] <= 0
            or optional_values["delta_t_m_rearm"] <= 0
            or optional_values["delta_x_e"] <= 0
        ):
            raise ValueError("M_ACTIVE requires positive M configuration")
        if abs(x) > values["x_max"]:
            raise ValueError("x exceeds x_max")
        if not 1 <= self.provenance_capacity <= 64 or not isinstance(self.provenance_capacity, int):
            raise ValueError("provenance_capacity must be in [1, 64]")
        _positive_int(self.event_budget, "event_budget")
        for name in ("ordinary_episode_id", "lineage_id", "multi_episode_id"):
            _id(getattr(self, name), name, allow_none=True)
        if self.captured_polarity not in (None, -1, 1):
            raise ValueError("captured_polarity must be -1, 1, or None")
        _finite(self.m_peak, "m_peak")
        for name in ("generation_token", "next_event_identity", "next_episode_identity",
                     "next_lineage_identity", "next_input_identity", "processed_event_count",
                     "input_contribution_count"):
            _id(getattr(self, name), name)
        _id(self.unassigned_provenance_count, "unassigned_provenance_count")
        if not isinstance(self.unassigned_provenance_truncated, bool):
            raise TypeError("unassigned_provenance_truncated must be boolean")
        if len(self.provenance) > self.provenance_capacity:
            raise ValueError("provenance exceeds capacity")
        if not isinstance(self.provenance_truncated, bool):
            raise TypeError("provenance_truncated must be boolean")
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "local_last_update_time", timestamp)
        for name, value in values.items():
            object.__setattr__(self, name, value)
        for name, value in optional_values.items():
            object.__setattr__(self, name, value)
        counters = (
            "generation_token",
            "next_event_identity",
            "next_episode_identity",
            "next_lineage_identity",
            "next_input_identity",
            "processed_event_count",
            "input_contribution_count",
        )
        if any(getattr(self, name) > self.event_budget for name in counters):
            raise ValueError("IR-2 counters exceed the declared event budget")
        self._validate_cross_fields()

    def _validate_cross_fields(self) -> None:
        pending = self.pending_internal_event
        mode = self.mode
        has_m_configuration = any(
            getattr(self, name) is not None
            for name in ("delta_t_m_emit", "delta_t_m_rearm", "delta_x_e")
        )
        if mode == IR2Mode.N:
            if any(getattr(self, name) is not None for name in (
                "ordinary_episode_id", "lineage_id", "captured_polarity",
                "m_phase", "multi_episode_id",
            )):
                raise ValueError("N cannot own an ordinary episode")
            if pending is not None:
                raise ValueError("N cannot have a pending internal event")
        elif mode == IR2Mode.S_PENDING:
            if self.m_phase is not None or self.multi_episode_id is not None:
                raise ValueError("S_PENDING cannot own an M episode")
            if self.ordinary_episode_id is None or self.lineage_id is None or self.captured_polarity is None:
                raise ValueError("S_PENDING requires episode, lineage, and polarity")
            if (
                self.ordinary_episode_id > self.next_episode_identity
                or self.lineage_id > self.next_lineage_identity
            ):
                raise ValueError("S_PENDING identity high-water marks are behind active identities")
            if pending is None or pending.kind is not IR2PendingKind.S_EMIT:
                raise ValueError("S_PENDING requires exactly one S_EMIT")
        elif mode == IR2Mode.S_RETURN:
            if self.m_phase is not None or self.multi_episode_id is not None:
                raise ValueError("S_RETURN cannot own an M episode")
            if self.ordinary_episode_id is None or self.lineage_id is None:
                raise ValueError("S_RETURN requires episode and lineage")
            if (
                self.ordinary_episode_id > self.next_episode_identity
                or self.lineage_id > self.next_lineage_identity
            ):
                raise ValueError("S_RETURN identity high-water marks are behind active identities")
            if pending is not None and pending.kind is not IR2PendingKind.S_REARM:
                raise ValueError("S_RETURN permits only S_REARM")
        else:
            if (
                self.m_phase is None
                or self.multi_episode_id is None
                or self.lineage_id is None
            ):
                raise ValueError("M_ACTIVE requires phase, multi_episode_id, and lineage")
            if self.ordinary_episode_id is not None or self.captured_polarity is not None:
                raise ValueError("M_ACTIVE cannot own ordinary episode state")
            if (
                self.next_episode_identity < self.multi_episode_id
                or self.next_lineage_identity < self.lineage_id
            ):
                raise ValueError("M_ACTIVE identity high-water marks are behind active identities")
            if pending is None or pending.kind not in (IR2PendingKind.M_EMIT, IR2PendingKind.M_REARM):
                raise ValueError("M_ACTIVE requires a valid M pending event")
            if (self.m_phase, pending.kind) not in (
                (MPhase.ARMED, IR2PendingKind.M_EMIT),
                (MPhase.REFRACTORY, IR2PendingKind.M_REARM),
            ):
                raise ValueError("M phase and pending event kind are inconsistent")
        if pending is not None:
            if (
                pending.neuron_id != self.neuron_id
                or pending.timestamp < self.local_last_update_time
            ):
                raise ValueError("pending internal event has wrong owner or timestamp")
            if has_m_configuration and pending.timestamp <= self.local_last_update_time:
                raise ValueError("E2 pending internal event must be strictly future")
            if mode == IR2Mode.M_ACTIVE and pending.episode_id != self.multi_episode_id:
                raise ValueError("M pending event has wrong episode ownership")
            if pending.episode_id != self.ordinary_episode_id and mode != IR2Mode.M_ACTIVE:
                raise ValueError("pending event has wrong episode ownership")
            if pending.generation != self.generation_token:
                raise ValueError("pending event generation does not match current generation")
        ids = [entry.causal_event_id for entry in self.provenance]
        if len(ids) != len(set(ids)):
            raise ValueError("provenance causal identities must be unique")
        for entry in self.provenance:
            if mode == IR2Mode.M_ACTIVE and (
                entry.episode_id != self.multi_episode_id
                or entry.lineage_id != self.lineage_id
            ):
                raise ValueError("M provenance ownership does not match active episode")
            if mode not in (IR2Mode.N, IR2Mode.M_ACTIVE) and (entry.episode_id, entry.lineage_id) != (self.ordinary_episode_id, self.lineage_id):
                raise ValueError("provenance ownership does not match active episode")

    def to_dict(self) -> dict[str, Any]:
        result = {field.name: _encode(getattr(self, field.name)) for field in fields(self)}
        result["neuron_id"] = self.neuron_id
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "IR2Neuron":
        if not isinstance(data, Mapping):
            raise TypeError("IR-2 neuron must be a mapping")
        values = dict(data)
        values["provenance"] = tuple(IR2Provenance(**entry) for entry in values.get("provenance", ()))
        pending = values.get("pending_internal_event")
        values["pending_internal_event"] = IR2PendingInternal(**pending) if pending is not None else None
        return cls(**values)


@dataclass(frozen=True, slots=True)
class TPCNIR2:
    neurons: tuple[IR2Neuron, ...]
    edges: tuple[IR2Edge, ...] = ()
    events: tuple[IR2Event, ...] = ()
    execution_order_policy: str = EXECUTION_ORDER_POLICY
    ir_version: str = IR2_VERSION
    schema_revision: int = IR2_SCHEMA_REVISION
    nodes: tuple[str, ...] = ()
    fan_in_limit: int = 1
    fan_out_limit: int = 1
    edge_capacity: int = 1
    routing_capacity: int = 1
    event_queue_capacity: int = 1
    event_budget: int | None = None

    def __post_init__(self) -> None:
        if self.ir_version != IR2_VERSION or self.schema_revision != IR2_SCHEMA_REVISION:
            raise ValueError("unsupported TPCN-IR-2 version or schema revision")
        if self.execution_order_policy != EXECUTION_ORDER_POLICY:
            raise ValueError("unsupported execution_order_policy")
        if len({neuron.neuron_id for neuron in self.neurons}) != len(self.neurons):
            raise ValueError("neurons must have unique identifiers")
        explicit_nodes = bool(self.nodes)
        nodes = set(self.nodes) or {n.neuron_id for n in self.neurons}
        if explicit_nodes and (
            any(neuron.neuron_id not in nodes for neuron in self.neurons)
            or any(edge.source not in nodes or edge.destination not in nodes for edge in self.edges)
        ):
            raise ValueError("edge endpoints must be declared nodes")
        nodes.update(edge.source for edge in self.edges)
        nodes.update(edge.destination for edge in self.edges)
        if any(not isinstance(node, str) or not node for node in nodes):
            raise ValueError("nodes must be non-empty strings")
        endpoints = [(edge.source, edge.destination) for edge in self.edges]
        if len(endpoints) != len(set(endpoints)):
            raise ValueError("duplicate directed edges are not supported")
        for name in ("fan_in_limit", "fan_out_limit", "edge_capacity", "routing_capacity", "event_queue_capacity"):
            _positive_int(getattr(self, name), name)
        if self.event_budget is not None:
            _positive_int(self.event_budget, "event_budget")
        if len(self.edges) > self.edge_capacity or len(self.events) > self.event_queue_capacity:
            raise ValueError("IR-2 records exceed declared finite capacity")
        sequences = [event.sequence for event in self.events if event.sequence >= 0]
        if len(sequences) != len(set(sequences)):
            raise ValueError("events must have unique sequence identities")
        object.__setattr__(self, "nodes", tuple(sorted(nodes)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "ir_version": self.ir_version,
            "schema_revision": self.schema_revision,
            "execution_order_policy": self.execution_order_policy,
            "nodes": list(self.nodes),
            "edges": [_encode(edge) for edge in self.edges],
            "events": [_encode(event) for event in self.events],
            "neurons": [neuron.to_dict() for neuron in self.neurons],
            "limits": {
                "fan_in": self.fan_in_limit,
                "fan_out": self.fan_out_limit,
                "edge_capacity": self.edge_capacity,
                "routing_capacity": self.routing_capacity,
                "event_queue_capacity": self.event_queue_capacity,
                "event_budget": self.event_budget,
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"), allow_nan=False)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TPCNIR2":
        if not isinstance(data, Mapping):
            raise TypeError("TPCN-IR-2 must be a mapping")
        if data.get("ir_version") != IR2_VERSION or data.get("schema_revision") != IR2_SCHEMA_REVISION:
            raise ValueError("unsupported TPCN-IR-2 version or schema revision")
        edges = tuple(IR2Edge(**edge) for edge in data.get("edges", ()))
        events = tuple(IR2Event(**event) for event in data.get("events", ()))
        neurons = tuple(IR2Neuron.from_dict(neuron) for neuron in data.get("neurons", ()))
        limits = data.get("limits")
        if not isinstance(limits, Mapping):
            raise ValueError("IR-2 limits are required")
        return cls(
            neurons,
            edges,
            events=events,
            execution_order_policy=data.get("execution_order_policy", ""),
            nodes=tuple(data.get("nodes", ())),
            fan_in_limit=limits["fan_in"],
            fan_out_limit=limits["fan_out"],
            edge_capacity=limits["edge_capacity"],
            routing_capacity=limits["routing_capacity"],
            event_queue_capacity=limits["event_queue_capacity"],
            event_budget=limits.get("event_budget"),
        )

    @classmethod
    def from_json(cls, payload: str) -> "TPCNIR2":
        try:
            value = json.loads(payload)
        except json.JSONDecodeError as error:
            raise ValueError("invalid TPCN-IR-2 JSON") from error
        return cls.from_dict(value)


def _encode(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    if isinstance(value, Mapping):
        return {key: _encode(item) for key, item in value.items()}
    if hasattr(value, "to_dict"):
        return _encode(value.to_dict())
    if is_dataclass(value):
        return {field.name: _encode(getattr(value, field.name)) for field in fields(value)}
    return value


def neuron_to_ir2(neuron: SingleExcursionNeuron) -> IR2Neuron:
    if not isinstance(neuron, SingleExcursionNeuron):
        raise TypeError("neuron_to_ir2 requires a SingleExcursionNeuron")
    if isinstance(neuron, MultiExcursionNeuron):
        raise TypeError("use neuron_to_ir2_e2 for a MultiExcursionNeuron")
    return _neuron_to_ir2(neuron, e2_capable=False)


def neuron_to_ir2_e2(neuron: MultiExcursionNeuron) -> IR2Neuron:
    if not isinstance(neuron, MultiExcursionNeuron):
        raise TypeError("neuron_to_ir2_e2 requires a MultiExcursionNeuron")
    return _neuron_to_ir2(neuron, e2_capable=True)


def _neuron_to_ir2(
    neuron: SingleExcursionNeuron,
    *,
    e2_capable: bool,
) -> IR2Neuron:
    config = neuron.config
    pending = neuron.pending_internal_event
    pending_ir = None if pending is None else IR2PendingInternal(
        pending.neuron_id, IR2PendingKind(pending.kind.value), pending.timestamp,
        pending.episode_id, pending.generation, pending.queue_sequence,
    )
    return IR2Neuron(
        neuron_id=neuron.neuron_id,
        dynamics_model=EXCURSION_V1,
        x=neuron.x,
        local_last_update_time=neuron.last_update_timestamp,
        mode=IR2Mode(neuron.mode.value),
        decay_rate=config.decay_rate,
        x_max=config.x_max,
        theta_r=config.theta_r,
        theta_e=config.theta_e,
        theta_hold=config.theta_hold,
        theta_m=config.theta_m,
        delta_t_e=config.emission_delay,
        delta_t_m_emit=config.m_emit_delay if e2_capable else None,
        delta_t_m_rearm=config.m_rearm_delay if e2_capable else None,
        delta_x_e=config.delta_x_e if e2_capable else None,
        a_min=config.a_min,
        a_max=config.a_max,
        provenance_capacity=config.provenance_capacity,
        event_budget=config.event_budget,
        ordinary_episode_id=neuron.ordinary_episode_id,
        lineage_id=neuron.lineage_id,
        captured_polarity=neuron.captured_polarity,
        m_peak=neuron.m_peak,
        pending_internal_event=pending_ir,
        provenance=tuple(
            IR2Provenance(e.event_id, e.timestamp, e.contribution, e.episode_id, e.lineage_id)
            for e in neuron.provenance
        ),
        provenance_truncated=neuron.provenance_truncated,
        generation_token=neuron.generation_token,
        next_event_identity=neuron._event_identity,
        next_episode_identity=neuron._episode_identity,
        next_lineage_identity=neuron._lineage_identity,
        next_input_identity=neuron._input_identity,
        processed_event_count=neuron.processed_event_count,
        input_contribution_count=neuron.input_contribution_count,
        unassigned_provenance_count=neuron._unassigned_provenance_count,
        unassigned_provenance_truncated=neuron._unassigned_provenance_truncated,
        m_phase=(
            MPhase(neuron.m_phase.value)
            if e2_capable and neuron.m_phase is not None
            else None
        ),
        multi_episode_id=(
            neuron.multi_episode_id if e2_capable else None
        ),
    )


def neuron_from_ir2(record: IR2Neuron) -> SingleExcursionNeuron:
    if record.dynamics_model == TANH_LEGACY:
        raise IR2UnsupportedRuntimeError("TANH_LEGACY requires the IR-1 reference runtime")
    if record.mode == IR2Mode.M_ACTIVE:
        raise IR2UnsupportedRuntimeError("M_ACTIVE is valid IR-2 data but unsupported by the E1 runtime")
    config = E1Config(
        decay_rate=record.decay_rate, x_max=record.x_max, theta_r=record.theta_r,
        theta_e=record.theta_e, theta_hold=record.theta_hold, theta_m=record.theta_m,
        emission_delay=record.delta_t_e, a_min=record.a_min, a_max=record.a_max,
        provenance_capacity=record.provenance_capacity, event_budget=record.event_budget,
    )
    neuron = SingleExcursionNeuron(record.neuron_id, config=config,
                                    initial_state=record.x,
                                    initial_timestamp=record.local_last_update_time)
    neuron.mode = E1Mode(record.mode.value)
    neuron.ordinary_episode_id = record.ordinary_episode_id
    neuron.lineage_id = record.lineage_id
    neuron.captured_polarity = record.captured_polarity
    neuron.m_peak = record.m_peak
    neuron.generation_token = record.generation_token
    neuron._event_identity = record.next_event_identity
    neuron._episode_identity = record.next_episode_identity
    neuron._lineage_identity = record.next_lineage_identity
    neuron._input_identity = record.next_input_identity
    neuron.processed_event_count = record.processed_event_count
    neuron.input_contribution_count = record.input_contribution_count
    neuron._provenance.extend(ProvenanceEntry(
        entry.causal_event_id, entry.timestamp, entry.signed_contribution,
        entry.episode_id, entry.lineage_id) for entry in record.provenance)
    neuron.provenance_truncated = record.provenance_truncated
    neuron._unassigned_provenance_count = record.unassigned_provenance_count
    neuron._unassigned_provenance_truncated = record.unassigned_provenance_truncated
    if record.pending_internal_event is not None:
        pending = record.pending_internal_event
        neuron.pending_internal_event = PendingInternalEvent(
            pending.neuron_id, pending.episode_id, pending.generation,
            E1InternalEventKind(pending.kind.value), pending.timestamp,
            pending.queue_sequence,
        )
    return neuron


def neuron_from_ir2_e2(record: IR2Neuron) -> MultiExcursionNeuron:
    if not isinstance(record, IR2Neuron):
        raise TypeError("neuron_from_ir2_e2 requires a validated IR2Neuron")
    if record.dynamics_model != EXCURSION_V1:
        raise IR2UnsupportedRuntimeError(
            "TPCN-IR-2 E2 reconstruction requires EXCURSION_V1"
        )
    if (
        record.pending_internal_event is not None
        and record.pending_internal_event.timestamp <= record.local_last_update_time
    ):
        raise ValueError(
            "E2 reconstruction requires pending internal events strictly after local time"
        )
    defaults = E1Config()
    config = E1Config(
        decay_rate=record.decay_rate,
        x_max=record.x_max,
        theta_r=record.theta_r,
        theta_e=record.theta_e,
        theta_hold=record.theta_hold,
        theta_m=record.theta_m,
        emission_delay=record.delta_t_e,
        m_emit_delay=(
            defaults.m_emit_delay
            if record.delta_t_m_emit is None
            else record.delta_t_m_emit
        ),
        m_rearm_delay=(
            defaults.m_rearm_delay
            if record.delta_t_m_rearm is None
            else record.delta_t_m_rearm
        ),
        delta_x_e=(
            defaults.delta_x_e
            if record.delta_x_e is None
            else record.delta_x_e
        ),
        a_min=record.a_min,
        a_max=record.a_max,
        provenance_capacity=record.provenance_capacity,
        event_budget=record.event_budget,
    )
    neuron = MultiExcursionNeuron(
        record.neuron_id,
        config=config,
        initial_state=record.x,
        initial_timestamp=record.local_last_update_time,
    )
    neuron.mode = E1Mode(record.mode.value)
    neuron.ordinary_episode_id = record.ordinary_episode_id
    neuron.lineage_id = record.lineage_id
    neuron.captured_polarity = record.captured_polarity
    neuron.m_peak = record.m_peak
    neuron.m_phase = (
        E2MPhase(record.m_phase.value) if record.m_phase is not None else None
    )
    neuron.multi_episode_id = record.multi_episode_id
    neuron.generation_token = record.generation_token
    neuron._event_identity = record.next_event_identity
    neuron._episode_identity = record.next_episode_identity
    neuron._lineage_identity = record.next_lineage_identity
    neuron._input_identity = record.next_input_identity
    neuron.processed_event_count = record.processed_event_count
    neuron.input_contribution_count = record.input_contribution_count
    neuron._provenance.extend(
        ProvenanceEntry(
            entry.causal_event_id,
            entry.timestamp,
            entry.signed_contribution,
            entry.episode_id,
            entry.lineage_id,
        )
        for entry in record.provenance
    )
    neuron.provenance_truncated = record.provenance_truncated
    neuron._unassigned_provenance_count = record.unassigned_provenance_count
    neuron._unassigned_provenance_truncated = (
        record.unassigned_provenance_truncated
    )
    if record.pending_internal_event is not None:
        pending = record.pending_internal_event
        neuron.pending_internal_event = PendingInternalEvent(
            pending.neuron_id,
            pending.episode_id,
            pending.generation,
            E1InternalEventKind(pending.kind.value),
            pending.timestamp,
            pending.queue_sequence,
        )
    return neuron


def ir2_from_ir1(ir: ExecutionIR) -> TPCNIR2:
    """Perform the deliberate, lossless IR-1 TANH upgrade."""
    if any(n.activation_model != "tanh" for n in ir.neurons):
        raise ValueError("IR-1 upgrade supports only tanh legacy neurons")
    neurons = tuple(IR2Neuron(
        neuron_id=n.neuron_id,
        dynamics_model=TANH_LEGACY,
        x=n.state,
        local_last_update_time=n.local_timestamp,
        mode=IR2Mode.N,
        decay_rate=n.decay_rate,
        x_max=n.state_limit,
        neuron_gain=n.neuron_gain,
        provenance_capacity=16,
        event_budget=ir.event_budget or 4096,
    ) for n in ir.neurons)
    edges = tuple(IR2Edge(e.source, e.destination, e.edge_weight, e.divider_strength,
                          e.reference, e.propagation_delay,
                          routing_cost=e.routing_cost, legacy_identity=e.legacy_identity)
                   for e in ir.edges)
    events = tuple(IR2Event(e.timestamp, e.source, e.destination, e.event_type, e.payload, e.sequence)
                   for e in ir.events)
    return TPCNIR2(
        neurons, edges, events=events, nodes=ir.nodes,
        fan_in_limit=ir.fan_in_limit, fan_out_limit=ir.fan_out_limit,
        edge_capacity=ir.edge_capacity, routing_capacity=ir.routing_capacity,
        event_queue_capacity=ir.event_queue_capacity, event_budget=ir.event_budget,
    )


def downgrade_ir2_to_ir1(ir: TPCNIR2) -> ExecutionIR:
    if any(n.dynamics_model == EXCURSION_V1 for n in ir.neurons):
        raise IR2DowngradeError("EXCURSION_V1 cannot be downgraded to IR-1")
    raise IR2DowngradeError("IR-2 downgrade is unsupported; use explicit IR-1 source data")


__all__ = [
    "IR2_VERSION", "IR2_SCHEMA_REVISION", "TANH_LEGACY", "EXCURSION_V1",
    "SUPPORTED_DYNAMICS_MODELS", "EXECUTION_ORDER_POLICY", "IR2_TPCV_SEPARATION",
    "IR2UnsupportedRuntimeError", "IR2DowngradeError", "IR2Mode", "MPhase",
    "IR2PendingKind", "IR2Edge", "IR2Provenance", "IR2PendingInternal",
    "IR2Event", "IR2Neuron", "TPCNIR2", "neuron_to_ir2", "neuron_from_ir2",
    "neuron_to_ir2_e2", "neuron_from_ir2_e2",
    "ir2_from_ir1", "downgrade_ir2_to_ir1",
]

IR2Network = TPCNIR2
ExecutionIR2 = TPCNIR2
ir1_to_ir2 = ir2_from_ir1
ir2_to_ir1 = downgrade_ir2_to_ir1
excursion_neuron_to_ir2 = neuron_to_ir2
