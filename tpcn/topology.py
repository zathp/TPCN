"""Finite event-routing topology built on the Luna-1 runtime."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from numbers import Real
from typing import Iterable, Mapping

from .event_runtime import Event, EventQueue, PropagationDelay, QueueCapacityError


class TopologyError(ValueError):
    """Base error for invalid topology configuration or routing requests."""


class TopologyCapacityError(TopologyError):
    """Raised when a finite topology resource budget would be exceeded."""


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _delay(value: Real) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError("delay must be a real number")
    result = float(value)
    if result <= 0.0 or result != result or result in (float("inf"), float("-inf")):
        raise ValueError("delay must be finite and positive")
    return result


def _bounded_real(value: Real, name: str, lower: float, upper: float) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if result != result or result in (float("inf"), float("-inf")) or not lower <= result <= upper:
        raise ValueError(f"{name} must be finite and within [{lower}, {upper}]")
    return result


def _routing_cost(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("routing_cost must be a positive integer")
    return value


@dataclass(frozen=True, slots=True)
class Edge:
    """A directed connection with bounded static Model-B transfer state."""

    source: str
    destination: str
    propagation_delay: PropagationDelay
    routing_cost: int = 1
    edge_weight: float = 1.0
    divider_strength: float = 1.0
    reference: float = 0.0
    legacy_identity: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source:
            raise ValueError("source must be a non-empty string")
        if not isinstance(self.destination, str) or not self.destination:
            raise ValueError("destination must be a non-empty string")
        object.__setattr__(self, "propagation_delay", _delay(self.propagation_delay))
        object.__setattr__(self, "routing_cost", _routing_cost(self.routing_cost))
        object.__setattr__(self, "edge_weight", _bounded_real(self.edge_weight, "edge_weight", -2.0, 2.0))
        object.__setattr__(self, "divider_strength", _bounded_real(self.divider_strength, "divider_strength", 0.0, 1.0))
        object.__setattr__(self, "reference", _bounded_real(self.reference, "reference", -1.0, 1.0))
        if not isinstance(self.legacy_identity, bool):
            raise TypeError("legacy_identity must be a boolean")


class BoundedTopology:
    """Finite directed graph with declared node, edge, fan-in and fan-out limits."""

    def __init__(
        self,
        nodes: Iterable[str],
        *,
        fan_in_limit: int,
        fan_out_limit: int,
        edge_capacity: int | None = None,
        routing_capacity: int | None = None,
    ) -> None:
        node_list = tuple(nodes)
        if not node_list or any(not isinstance(node, str) or not node for node in node_list):
            raise ValueError("nodes must contain non-empty strings")
        if len(set(node_list)) != len(node_list):
            raise ValueError("nodes must be unique")
        self.nodes = node_list
        self.fan_in_limit = _positive_integer(fan_in_limit, "fan_in_limit")
        self.fan_out_limit = _positive_integer(fan_out_limit, "fan_out_limit")
        self.edge_capacity = _positive_integer(edge_capacity, "edge_capacity") if edge_capacity is not None else len(node_list) * fan_out_limit
        self.routing_capacity = _positive_integer(routing_capacity, "routing_capacity") if routing_capacity is not None else self.edge_capacity
        if self.edge_capacity < 1 or self.routing_capacity < 1:
            raise ValueError("topology capacities must be positive")
        self._edges: dict[tuple[str, str], Edge] = {}

    @classmethod
    def from_edges(
        cls,
        nodes: Iterable[str],
        edges: Iterable[Edge | tuple[str, str, PropagationDelay]],
        *,
        fan_in_limit: int,
        fan_out_limit: int,
        edge_capacity: int | None = None,
        routing_capacity: int | None = None,
    ) -> "BoundedTopology":
        topology = cls(
            nodes,
            fan_in_limit=fan_in_limit,
            fan_out_limit=fan_out_limit,
            edge_capacity=edge_capacity,
            routing_capacity=routing_capacity,
        )
        for edge_spec in edges:
            if isinstance(edge_spec, Edge):
                topology._connect_edge(edge_spec)
            else:
                source, destination, delay = edge_spec
                topology.connect(source, destination, delay)
        return topology

    @classmethod
    def seeded(
        cls,
        nodes: Iterable[str],
        *,
        edge_count: int,
        fan_in_limit: int,
        fan_out_limit: int,
        seed: int,
        propagation_delay: PropagationDelay,
    ) -> "BoundedTopology":
        """Construct a reproducible bounded graph from sorted candidate endpoints."""
        topology = cls(nodes, fan_in_limit=fan_in_limit, fan_out_limit=fan_out_limit, edge_capacity=edge_count)
        if isinstance(edge_count, bool) or not isinstance(edge_count, int) or edge_count < 0:
            raise ValueError("edge_count must be a nonnegative integer")
        generator = random.Random(seed)
        candidates = [(source, destination) for source in sorted(topology.nodes) for destination in sorted(topology.nodes) if source != destination]
        generator.shuffle(candidates)
        for source, destination in candidates:
            if len(topology) == edge_count:
                break
            try:
                topology.connect(source, destination, propagation_delay)
            except TopologyCapacityError:
                continue
        if len(topology) != edge_count:
            raise TopologyCapacityError("edge_count cannot fit within topology budgets")
        return topology

    def __len__(self) -> int:
        return len(self._edges)

    @property
    def edges(self) -> tuple[Edge, ...]:
        return tuple(self._edges.values())

    def edge(self, source: str, destination: str) -> Edge:
        try:
            return self._edges[(source, destination)]
        except KeyError as error:
            raise TopologyError("edge does not exist") from error

    def connect(self, source: str, destination: str, propagation_delay: PropagationDelay) -> Edge:
        self._validate_node(source)
        self._validate_node(destination)
        if (source, destination) in self._edges:
            raise TopologyError("edge already exists")
        if len(self) >= self.edge_capacity:
            raise TopologyCapacityError("edge capacity reached")
        incoming = sum(edge.destination == destination for edge in self._edges.values())
        outgoing = sum(edge.source == source for edge in self._edges.values())
        if incoming >= self.fan_in_limit:
            raise TopologyCapacityError("destination fan-in limit reached")
        if outgoing >= self.fan_out_limit:
            raise TopologyCapacityError("source fan-out limit reached")
        return self._connect_edge(Edge(source, destination, _delay(propagation_delay)))

    def _connect_edge(self, edge: Edge) -> Edge:
        self._validate_node(edge.source)
        self._validate_node(edge.destination)
        if (edge.source, edge.destination) in self._edges:
            raise TopologyError("edge already exists")
        if len(self) >= self.edge_capacity:
            raise TopologyCapacityError("edge capacity reached")
        incoming = sum(existing.destination == edge.destination for existing in self._edges.values())
        outgoing = sum(existing.source == edge.source for existing in self._edges.values())
        if incoming >= self.fan_in_limit:
            raise TopologyCapacityError("destination fan-in limit reached")
        if outgoing >= self.fan_out_limit:
            raise TopologyCapacityError("source fan-out limit reached")
        self._edges[(edge.source, edge.destination)] = edge
        return edge

    def route(
        self,
        event: Event,
        queue: EventQueue[Event],
        *,
        observer: object | None = None,
        exclude_destinations: Iterable[str] = (),
    ) -> tuple[Event, ...]:
        """Queue delayed Model-B signal events without mutating destinations inline.

        Control and metadata payloads remain opaque; only numeric ``signal``
        events are edge-transformed. Optionally omit edges whose destinations
        are present in this per-call exclusion collection.
        """
        self._validate_node(event.source)
        excluded = frozenset(exclude_destinations)
        outgoing = tuple(
            edge
            for edge in self._edges.values()
            if edge.source == event.source and edge.destination not in excluded
        )
        if len(outgoing) > self.routing_capacity:
            raise TopologyCapacityError("routing capacity exceeded")
        if len(queue) + len(outgoing) > queue.capacity:
            raise QueueCapacityError("event queue capacity cannot admit complete fan-out")
        queued: list[Event] = []
        for edge in outgoing:
            payload = event.payload
            if event.event_type in ("signal", "excursion"):
                if isinstance(payload, bool) or not isinstance(payload, Real):
                    raise TypeError("signal event payload must be a real number")
                transformed = math.tanh(edge.edge_weight * float(payload))
                payload = edge.divider_strength * transformed + (1.0 - edge.divider_strength) * edge.reference
            routed = queue.push_propagated(
                event.timestamp,
                edge.source,
                edge.destination,
                event.event_type,
                payload,
                edge.propagation_delay,
                event_id=event.event_id,
                lineage_id=event.lineage_id,
            )
            queued.append(routed)
            if observer is not None:
                observer.record_route(edge, event, routed)
        return tuple(queued)

    def incoming(self, node: str) -> tuple[Edge, ...]:
        self._validate_node(node)
        return tuple(edge for edge in self._edges.values() if edge.destination == node)

    def outgoing(self, node: str) -> tuple[Edge, ...]:
        self._validate_node(node)
        return tuple(edge for edge in self._edges.values() if edge.source == node)

    def _validate_node(self, node: str) -> None:
        if node not in self.nodes:
            raise TopologyError(f"unknown node: {node!r}")


__all__ = ["BoundedTopology", "Edge", "TopologyCapacityError", "TopologyError"]