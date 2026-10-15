"""Replay-first, downstream-only state for the Luna-12C 3D viewer.

This module deliberately contains no TPCN execution objects. It turns an
immutable :class:`ReplaySequence` into bounded renderer state that can be
tested without a display or OpenGL context.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Literal

from .cpu_visualization import ReplaySequence, ReplaySequenceError
from .temporal_analysis import analyze_replay


ViewerMode = Literal["overview", "activity", "structural", "neighborhood", "utility"]
CoordinateSource = Literal["canonical", "diagnostic"]


@dataclass(frozen=True, slots=True)
class NodeView:
    neuron_id: str
    position: tuple[float, float, float]
    active: bool
    state: float
    activation: float | None
    processed_events: int
    selected: bool = False
    changed: bool = False


@dataclass(frozen=True, slots=True)
class EdgeView:
    source: str
    destination: str
    propagation_delay: float
    kind: Literal["persistent", "added", "pruned"] = "persistent"


@dataclass(frozen=True, slots=True)
class SnapshotDiff:
    added_edges: frozenset[tuple[str, str]] = frozenset()
    removed_edges: frozenset[tuple[str, str]] = frozenset()
    persistent_edges: frozenset[tuple[str, str]] = frozenset()
    changed_neurons: frozenset[str] = frozenset()


@dataclass(slots=True)
class CameraState:
    yaw: float = 35.0
    pitch: float = 20.0
    distance: float = 18.0
    target: tuple[float, float, float] = (0.0, 0.0, 0.0)

    def reset(self, *, distance: float = 18.0) -> None:
        self.yaw = 35.0
        self.pitch = 20.0
        self.distance = distance
        self.target = (0.0, 0.0, 0.0)


@dataclass(slots=True)
class ViewerFilters:
    mode: ViewerMode = "overview"
    active_only: bool = False
    changed_only: bool = False
    neighborhood_depth: int = 1
    max_edges: int = 2000

    def __post_init__(self) -> None:
        if self.neighborhood_depth < 0 or self.neighborhood_depth > 8:
            raise ValueError("neighborhood_depth must be in [0, 8]")
        if self.max_edges <= 0:
            raise ValueError("max_edges must be positive")


def _diagnostic_layout(neuron_ids: Iterable[str], radius: float = 6.0) -> dict[str, tuple[float, float, float]]:
    """Place IDs on a deterministic Fibonacci sphere; no random state is used."""
    ordered = tuple(sorted(set(neuron_ids)))
    count = len(ordered)
    if not count:
        return {}
    golden = math.pi * (3.0 - math.sqrt(5.0))
    result = {}
    for index, neuron_id in enumerate(ordered):
        y = 1.0 - (2.0 * (index + 0.5) / count)
        ring = math.sqrt(max(0.0, 1.0 - y * y))
        angle = golden * index
        result[neuron_id] = (radius * ring * math.cos(angle), radius * y, radius * ring * math.sin(angle))
    return result


def _coordinates(sequence: ReplaySequence) -> tuple[CoordinateSource, dict[str, tuple[float, float, float]]]:
    ids = {neuron.neuron_id for snapshot in sequence.snapshots for neuron in snapshot.neurons}
    positions = {neuron.neuron_id: neuron.position for snapshot in sequence.snapshots for neuron in snapshot.neurons
                 if neuron.position is not None}
    if len(positions) == len(ids) and ids:
        return "canonical", {identifier: (float(point[0]), float(point[1]), 0.0) for identifier, point in positions.items()}
    return "diagnostic", _diagnostic_layout(ids)


def _diff(previous: object | None, current: object) -> SnapshotDiff:
    current_neurons = {item.neuron_id: item for item in current.neurons}
    current_edges = {(item.source, item.destination) for item in current.connections}
    if previous is None:
        return SnapshotDiff(persistent_edges=frozenset(current_edges),
                            changed_neurons=frozenset(current_neurons))
    previous_neurons = {item.neuron_id: item for item in previous.neurons}
    previous_edges = {(item.source, item.destination) for item in previous.connections}
    return SnapshotDiff(
        added_edges=frozenset(current_edges - previous_edges),
        removed_edges=frozenset(previous_edges - current_edges),
        persistent_edges=frozenset(current_edges & previous_edges),
        changed_neurons=frozenset(identifier for identifier in current_neurons
                                  if identifier not in previous_neurons
                                  or current_neurons[identifier] != previous_neurons[identifier]),
    )


class VisualizationScene:
    """Deterministic, bounded renderer state detached from computation."""

    def __init__(self, replay: ReplaySequence, *, history_limit: int = 4,
                 prune_highlight_snapshots: int = 3, added_highlight_snapshots: int = 3) -> None:
        if not isinstance(replay, ReplaySequence) or not replay.snapshots:
            raise ReplaySequenceError("viewer requires at least one replay snapshot")
        if history_limit <= 0 or prune_highlight_snapshots < 0 or added_highlight_snapshots < 0:
            raise ValueError("history limits must be positive and bounded")
        self.replay = replay
        self.history_limit = history_limit
        self.prune_highlight_snapshots = prune_highlight_snapshots
        self.added_highlight_snapshots = added_highlight_snapshots
        self.coordinate_source, self.positions = _coordinates(replay)
        self.snapshot_index = 0
        self.playing = False
        self.playback_speed = 4.0
        self.selected_neuron: str | None = None
        self.selected_edge: tuple[str, str] | None = None
        self.filters = ViewerFilters()
        self.camera = CameraState()
        self._history: list[int] = [0]
        self._playback_fraction = 0.0

    @property
    def snapshot(self):
        return self.replay.snapshots[self.snapshot_index]

    @property
    def diff(self) -> SnapshotDiff:
        previous = None if self.snapshot_index == 0 else self.replay.snapshots[self.snapshot_index - 1]
        return _diff(previous, self.snapshot)

    @property
    def metrics(self) -> dict[str, object] | None:
        epoch = self.snapshot.epoch
        return next((dict(item) for item in self.replay.metrics if item.get("epoch") == epoch), None)

    @property
    def available_modes(self) -> tuple[ViewerMode, ...]:
        available = ["overview", "activity", "structural", "neighborhood"]
        metrics = self.metrics or {}
        if "energy" in metrics or "utility" in metrics:
            available.append("utility")
        return tuple(available)  # type: ignore[return-value]

    def seek(self, index: int) -> int:
        if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < len(self.replay.snapshots):
            raise IndexError("snapshot index is out of range")
        self.snapshot_index = index
        self._history.append(index)
        del self._history[:-self.history_limit]
        self._playback_fraction = 0.0
        current_ids = {item.neuron_id for item in self.snapshot.neurons}
        if self.selected_neuron is not None and self.selected_neuron not in current_ids:
            self.selected_neuron = None
        current_edges = {(item.source, item.destination) for item in self.snapshot.connections}
        if (self.selected_edge is not None and self.selected_edge not in current_edges
                and self.selected_edge not in self.diff.removed_edges):
            self.selected_edge = None
        return index

    def first(self) -> int:
        return self.seek(0)

    def last(self) -> int:
        return self.seek(len(self.replay.snapshots) - 1)

    def step(self, amount: int = 1) -> int:
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise TypeError("step amount must be an integer")
        return self.seek(max(0, min(len(self.replay.snapshots) - 1, self.snapshot_index + amount)))

    def tick(self, elapsed_seconds: float) -> int:
        if self.playing and math.isfinite(elapsed_seconds) and elapsed_seconds >= 0.0:
            self._playback_fraction += elapsed_seconds * self.playback_speed
            steps = int(self._playback_fraction)
            if steps:
                remainder = self._playback_fraction - steps
                self.step(steps)
                self._playback_fraction = remainder
        return self.snapshot_index

    def orbit(self, yaw_delta: float, pitch_delta: float) -> None:
        self.camera.yaw += float(yaw_delta)
        self.camera.pitch = max(-89.0, min(89.0, self.camera.pitch + float(pitch_delta)))

    def pan(self, x_delta: float, y_delta: float, z_delta: float = 0.0) -> None:
        self.camera.target = tuple(value + delta for value, delta in zip(
            self.camera.target, (float(x_delta), float(y_delta), float(z_delta))))

    def zoom(self, distance_delta: float) -> None:
        self.camera.distance = max(0.1, self.camera.distance + float(distance_delta))

    def fit(self) -> None:
        if not self.positions:
            self.camera.reset()
            return
        coordinates = tuple(self.positions.values())
        center = tuple(sum(point[axis] for point in coordinates) / len(coordinates) for axis in range(3))
        extent = max(max(abs(point[axis] - center[axis]) for point in coordinates) for axis in range(3))
        self.camera.target = center
        self.camera.distance = max(4.0, extent * 3.0)

    def set_mode(self, mode: ViewerMode) -> None:
        if mode not in self.available_modes:
            raise ValueError(f"viewer mode is unavailable: {mode}")
        self.filters.mode = mode

    def select(self, neuron_id: str | None) -> None:
        if neuron_id is not None and neuron_id not in self.positions:
            raise KeyError(neuron_id)
        self.selected_neuron = neuron_id
        self.selected_edge = None

    def select_edge(self, edge: tuple[str, str] | None) -> None:
        if edge is not None:
            source, destination = edge
            if source not in self.positions or destination not in self.positions:
                raise KeyError(edge)
            current = {(item.source, item.destination) for item in self.snapshot.connections}
            removed = {(item.source, item.destination) for item in self.edges() if item.kind == "pruned"}
            if edge not in current and edge not in removed:
                raise KeyError(edge)
        self.selected_edge = edge
        if edge is not None:
            self.selected_neuron = None

    def neighborhood(self, depth: int | None = None) -> frozenset[str]:
        if self.selected_neuron is None:
            return frozenset()
        limit = self.filters.neighborhood_depth if depth is None else depth
        if limit < 0 or limit > 8:
            raise ValueError("neighborhood depth must be in [0, 8]")
        neighbors = {self.selected_neuron}
        for _ in range(limit):
            neighbors.update(edge.source for edge in self.snapshot.connections if edge.destination in neighbors)
            neighbors.update(edge.destination for edge in self.snapshot.connections if edge.source in neighbors)
        return frozenset(neighbors)

    def nodes(self) -> tuple[NodeView, ...]:
        allowed = self.neighborhood() if self.filters.mode == "neighborhood" else None
        return tuple(NodeView(item.neuron_id, self.positions[item.neuron_id], item.active, item.state,
                              getattr(item, "activation", None), item.processed_events,
                              item.neuron_id == self.selected_neuron,
                              item.neuron_id in self.diff.changed_neurons)
                     for item in self.snapshot.neurons
                     if (allowed is None or item.neuron_id in allowed) and (not self.filters.active_only or item.active)
                     and (not self.filters.changed_only or item.neuron_id in self.diff.changed_neurons))

    def edges(self) -> tuple[EdgeView, ...]:
        visible_nodes = {node.neuron_id for node in self.nodes()}
        diff = self.diff
        recent_added: set[tuple[str, str]] = set()
        if self.added_highlight_snapshots:
            first_transition = max(1, self.snapshot_index - self.added_highlight_snapshots + 1)
            for index in range(first_transition, self.snapshot_index + 1):
                transition = _diff(self.replay.snapshots[index - 1], self.replay.snapshots[index])
                recent_added.update(transition.added_edges)
        result: list[EdgeView] = []
        records = {item.neuron_id: item for item in self.snapshot.neurons}
        for edge in self.snapshot.connections:
            key = (edge.source, edge.destination)
            if edge.source not in visible_nodes or edge.destination not in visible_nodes:
                continue
            if self.filters.mode == "activity" and not (records[edge.source].active or records[edge.destination].active):
                continue
            if self.filters.mode == "structural" and key not in diff.added_edges:
                continue
            result.append(EdgeView(edge.source, edge.destination, edge.propagation_delay,
                                   "added" if key in recent_added else "persistent"))
        recent_pruned: set[tuple[str, str]] = set()
        first_transition = max(1, self.snapshot_index - self.prune_highlight_snapshots + 1)
        for index in range(first_transition, self.snapshot_index + 1):
            transition = _diff(self.replay.snapshots[index - 1], self.replay.snapshots[index])
            recent_pruned.update(transition.removed_edges)
        result.extend(EdgeView(source, destination, 0.0, "pruned") for source, destination in sorted(recent_pruned))
        return tuple(result[:self.filters.max_edges])

    def inspect_edge(self, edge: tuple[str, str] | None = None) -> dict[str, object] | None:
        key = self.selected_edge if edge is None else edge
        if key is None:
            return None
        current = {(item.source, item.destination): item for item in self.snapshot.connections}
        if key in current:
            record = current[key]
            status = "added" if any(item.source == key[0] and item.destination == key[1]
                                    and item.kind == "added" for item in self.edges()) else "persistent"
            delay: float | None = record.propagation_delay
        elif any((item.source, item.destination) == key and item.kind == "pruned" for item in self.edges()):
            status = "removed in snapshot diff (not evidence of biological or E2 pruning)"
            record = next(item
                          for previous in reversed(self.replay.snapshots[:self.snapshot_index])
                          for item in previous.connections
                          if (item.source, item.destination) == key)
            delay = record.propagation_delay
        else:
            return None
        return {"source": key[0], "destination": key[1], "status": status,
                "propagation_delay": delay}

    def inspect(self, neuron_id: str | None = None) -> dict[str, object] | None:
        identifier = self.selected_neuron if neuron_id is None else neuron_id
        if identifier is None:
            return None
        neuron = next((item for item in self.snapshot.neurons if item.neuron_id == identifier), None)
        if neuron is None:
            return None
        incoming = tuple(sorted(edge.source for edge in self.snapshot.connections if edge.destination == identifier))
        outgoing = tuple(sorted(edge.destination for edge in self.snapshot.connections if edge.source == identifier))
        return {"neuron_id": identifier, "position": self.positions[identifier], "state": neuron.state,
                "activation": getattr(neuron, "activation", None), "active": neuron.active,
                "processed_events": neuron.processed_events, "fan_in": len(incoming), "fan_out": len(outgoing),
                "incoming": incoming, "outgoing": outgoing,
                "topology_changes": tuple(sorted(key for key in self.diff.added_edges | self.diff.removed_edges
                                                  if identifier in key))}

    def summary(self) -> dict[str, object]:
        metrics = self.metrics or {}
        active = sum(item.active for item in self.snapshot.neurons)
        analysis = analyze_replay(self.replay)
        return {"snapshot": self.snapshot_index, "epoch": self.snapshot.epoch, "nodes_active": active,
                "node_count": len(self.snapshot.neurons), "connections": len(self.snapshot.connections),
                "added": len(self.diff.added_edges), "removed": len(self.diff.removed_edges),
            "never_active": sum(1 for item in self.snapshot.neurons if not item.active), "metrics": metrics,
            "analysis_classification": analysis["classification"],
            "edge_use_evidence": analysis["edge_summary"]["edge_use_evidence"]}


__all__ = ["CameraState", "EdgeView", "NodeView", "SnapshotDiff", "ViewerFilters", "VisualizationScene"]