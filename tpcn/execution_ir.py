"""Versioned, hardware-neutral TPCN execution representation.

This module is deliberately an adapter boundary.  Canonical reference
objects remain authoritative for execution; this IR only represents their
portable logical state and bounded configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from numbers import Real
from typing import Any, Mapping

from .canonical_neuron import TPCNNeuron
from .event_runtime import Event
from .topology import BoundedTopology, Edge


IR_VERSION = "TPCN-IR-1"
ACTIVATION_MODEL = "tanh"


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _finite(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _nonnegative(value: Real, name: str) -> float:
    result = _finite(value, name)
    if result < 0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def _positive_int(value: int, name: str, *, allow_zero: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or (value < 0 if allow_zero else value <= 0):
        qualifier = "nonnegative" if allow_zero else "positive"
        raise ValueError(f"{name} must be a {qualifier} integer")
    return value


def _payload(value: Any) -> Any:
    """Reject non-JSON payloads rather than silently changing logical state."""
    try:
        json.dumps(value, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise TypeError("event payload must be JSON-serializable and finite") from error
    return value


@dataclass(frozen=True, slots=True)
class IREdge:
    source: str
    destination: str
    edge_weight: float
    divider_strength: float
    reference: float
    propagation_delay: float
    routing_cost: int = 1
    legacy_identity: bool = True

    def __post_init__(self) -> None:
        _text(self.source, "source")
        _text(self.destination, "destination")
        weight = _finite(self.edge_weight, "edge_weight")
        divider = _finite(self.divider_strength, "divider_strength")
        reference = _finite(self.reference, "reference")
        delay = _finite(self.propagation_delay, "propagation_delay")
        if not -2.0 <= weight <= 2.0:
            raise ValueError("edge_weight must be within [-2.0, 2.0]")
        if not 0.0 <= divider <= 1.0:
            raise ValueError("divider_strength must be within [0.0, 1.0]")
        if not -1.0 <= reference <= 1.0:
            raise ValueError("reference must be within [-1.0, 1.0]")
        if delay <= 0.0:
            raise ValueError("propagation_delay must be finite and positive")
        _positive_int(self.routing_cost, "routing_cost")
        if not isinstance(self.legacy_identity, bool):
            raise TypeError("legacy_identity must be a boolean")


@dataclass(frozen=True, slots=True)
class IRNeuron:
    neuron_id: str
    decay_rate: float
    state_limit: float
    neuron_gain: float
    activation_model: str = ACTIVATION_MODEL
    state: float = 0.0
    local_timestamp: float = 0.0

    def __post_init__(self) -> None:
        _text(self.neuron_id, "neuron_id")
        decay = _nonnegative(self.decay_rate, "decay_rate")
        limit = _finite(self.state_limit, "state_limit")
        gain = _finite(self.neuron_gain, "neuron_gain")
        state = _finite(self.state, "state")
        timestamp = _nonnegative(self.local_timestamp, "local_timestamp")
        if limit <= 0.0:
            raise ValueError("state_limit must be positive")
        if not 0.0 <= gain <= 2.0:
            raise ValueError("neuron_gain must be within [0.0, 2.0]")
        if abs(state) > limit:
            raise ValueError("state must be within state_limit")
        _text(self.activation_model, "activation_model")
        object.__setattr__(self, "decay_rate", decay)
        object.__setattr__(self, "state_limit", limit)
        object.__setattr__(self, "neuron_gain", gain)
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "local_timestamp", timestamp)


@dataclass(frozen=True, slots=True)
class IREvent:
    timestamp: float
    source: str
    destination: str
    event_type: str
    payload: Any
    sequence: int = -1

    def __post_init__(self) -> None:
        _nonnegative(self.timestamp, "timestamp")
        _text(self.source, "source")
        _text(self.destination, "destination")
        _text(self.event_type, "event_type")
        _payload(self.payload)
        _positive_int(self.sequence, "sequence", allow_zero=True) if self.sequence != -1 else None
        if self.sequence < -1:
            raise ValueError("sequence must be a nonnegative integer or -1")


@dataclass(frozen=True, slots=True)
class ExecutionIR:
    """A finite logical network snapshot and optional pending input events."""

    edges: tuple[IREdge, ...]
    neurons: tuple[IRNeuron, ...]
    events: tuple[IREvent, ...] = ()
    nodes: tuple[str, ...] = ()
    fan_in_limit: int = 1
    fan_out_limit: int = 1
    edge_capacity: int = 1
    routing_capacity: int = 1
    event_queue_capacity: int = 1
    event_budget: int | None = None
    version: str = IR_VERSION

    def __post_init__(self) -> None:
        if self.version != IR_VERSION:
            raise ValueError(f"unsupported execution IR version: {self.version!r}")
        node_set = set(self.nodes)
        if not node_set:
            node_set = {n.neuron_id for n in self.neurons}
            node_set.update(e.source for e in self.edges)
            node_set.update(e.destination for e in self.edges)
            object.__setattr__(self, "nodes", tuple(sorted(node_set)))
        if len(node_set) != len(self.nodes) or any(not isinstance(n, str) or not n for n in self.nodes):
            raise ValueError("nodes must contain unique non-empty strings")
        neuron_ids = [n.neuron_id for n in self.neurons]
        if len(set(neuron_ids)) != len(neuron_ids):
            raise ValueError("neurons must have unique identifiers")
        if any(e.source not in node_set or e.destination not in node_set for e in self.edges):
            raise ValueError("edge endpoints must be declared nodes")
        _positive_int(self.fan_in_limit, "fan_in_limit")
        _positive_int(self.fan_out_limit, "fan_out_limit")
        _positive_int(self.edge_capacity, "edge_capacity")
        _positive_int(self.routing_capacity, "routing_capacity")
        _positive_int(self.event_queue_capacity, "event_queue_capacity")
        if self.event_budget is not None:
            _positive_int(self.event_budget, "event_budget")
        if len(self.edges) > self.edge_capacity or len(self.events) > self.event_queue_capacity:
            raise ValueError("IR records exceed declared finite capacity")

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "nodes": list(self.nodes),
            "limits": {
                "fan_in": self.fan_in_limit, "fan_out": self.fan_out_limit,
                "edge_capacity": self.edge_capacity, "routing_capacity": self.routing_capacity,
                "event_queue_capacity": self.event_queue_capacity, "event_budget": self.event_budget,
            },
            "edges": [_record(edge) for edge in self.edges],
            "neurons": [_record(neuron) for neuron in self.neurons],
            "events": [_record(event) for event in self.events],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"), allow_nan=False)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ExecutionIR":
        if not isinstance(data, Mapping):
            raise TypeError("execution IR must be a mapping")
        version = data.get("version")
        if version != IR_VERSION:
            raise ValueError(f"unsupported execution IR version: {version!r}")
        limits = data.get("limits")
        if not isinstance(limits, Mapping):
            raise ValueError("execution IR limits are required")
        return cls(
            tuple(IREdge(**edge) for edge in data.get("edges", ())),
            tuple(IRNeuron(**neuron) for neuron in data.get("neurons", ())),
            tuple(IREvent(**event) for event in data.get("events", ())),
            tuple(data.get("nodes", ())),
            fan_in_limit=limits["fan_in"], fan_out_limit=limits["fan_out"],
            edge_capacity=limits["edge_capacity"], routing_capacity=limits["routing_capacity"],
            event_queue_capacity=limits["event_queue_capacity"],
            event_budget=limits.get("event_budget"),
        )

    @classmethod
    def from_json(cls, payload: str) -> "ExecutionIR":
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as error:
            raise ValueError("invalid execution IR JSON") from error
        return cls.from_dict(data)


@dataclass(frozen=True, slots=True)
class ReferenceExecutionState:
    topology: BoundedTopology
    neurons: dict[str, TPCNNeuron]
    events: tuple[Event, ...]
    queue_capacity: int


def _record(value: object) -> dict[str, Any]:
    from dataclasses import fields
    return {field.name: getattr(value, field.name) for field in fields(value)}


def edge_to_ir(edge: Edge) -> IREdge:
    return IREdge(edge.source, edge.destination, edge.edge_weight, edge.divider_strength,
                  edge.reference, edge.propagation_delay, edge.routing_cost, edge.legacy_identity)


def neuron_to_ir(neuron: TPCNNeuron) -> IRNeuron:
    return IRNeuron(neuron.neuron_id, neuron.decay_rate, neuron.state_limit,
                    neuron.neuron_gain, ACTIVATION_MODEL, neuron.state, neuron.clock.timestamp)


def event_to_ir(event: Event) -> IREvent:
    event_type = event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type)
    return IREvent(event.timestamp, event.source, event.destination, event_type, event.payload, event.sequence)


def topology_to_ir(
    topology: BoundedTopology,
    neurons: Mapping[str, TPCNNeuron] | None = None,
    events: tuple[Event, ...] = (),
    *,
    event_queue_capacity: int = 1,
    event_budget: int | None = None,
) -> ExecutionIR:
    neuron_records = tuple(neuron_to_ir(neurons[node]) for node in topology.nodes) if neurons is not None else ()
    return ExecutionIR(tuple(edge_to_ir(edge) for edge in topology.edges), neuron_records,
                       tuple(event_to_ir(event) for event in events), tuple(topology.nodes),
                       topology.fan_in_limit, topology.fan_out_limit, topology.edge_capacity,
                       topology.routing_capacity, event_queue_capacity, event_budget)


def reference_from_ir(ir: ExecutionIR) -> ReferenceExecutionState:
    topology = BoundedTopology.from_edges(
        ir.nodes,
        tuple(Edge(e.source, e.destination, e.propagation_delay, routing_cost=e.routing_cost,
                   edge_weight=e.edge_weight, divider_strength=e.divider_strength,
                   reference=e.reference, legacy_identity=e.legacy_identity) for e in ir.edges),
        fan_in_limit=ir.fan_in_limit, fan_out_limit=ir.fan_out_limit,
        edge_capacity=ir.edge_capacity, routing_capacity=ir.routing_capacity,
    )
    neurons = {}
    for record in ir.neurons:
        neuron = TPCNNeuron(record.neuron_id, state_limit=record.state_limit,
                            decay_rate=record.decay_rate, neuron_gain=record.neuron_gain,
                            initial_state=record.state)
        neuron.clock.advance_to(record.local_timestamp)
        neurons[record.neuron_id] = neuron
    events = tuple(Event(e.timestamp, e.source, e.destination, e.event_type, e.payload, e.sequence)
                   for e in ir.events)
    return ReferenceExecutionState(topology, neurons, events, ir.event_queue_capacity)


__all__ = [
    "ACTIVATION_MODEL", "IR_VERSION", "ExecutionIR", "IREdge", "IREvent", "IRNeuron",
    "ReferenceExecutionState", "edge_to_ir", "event_to_ir", "neuron_to_ir",
    "reference_from_ir", "topology_to_ir",
]
