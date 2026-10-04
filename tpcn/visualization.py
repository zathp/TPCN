"""Downstream-only deterministic snapshots for TPCN observability.

The format is intentionally independent of the computational event path. It
serializes only state supplied by a caller through this pull interface.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import struct
from numbers import Real
from typing import Iterable, Sequence

from .excursion_neuron import E1Mode, MultiExcursionNeuron

MAGIC = b"TPCV"
FORMAT_VERSION = 1
EXCURSION_FORMAT_VERSION = 2
MAX_IDENTIFIER_BYTES = 255
MAX_RECORDS = 65_535
MAX_EXPORT_BYTES = 1_048_576
INCOMPLETE_CAPTURE = 0x01
_HEADER = struct.Struct(">4sBBHIdIII")
_NEURON_FIXED = struct.Struct(">BBddI")
_EXCURSION_NEURON_FIXED = struct.Struct(">BBdI")
_CONNECTION_FIXED = struct.Struct(">d")
_MODE_TO_CODE = {
    E1Mode.N: 0,
    E1Mode.S_PENDING: 1,
    E1Mode.S_RETURN: 2,
    E1Mode.M_ACTIVE: 3,
}
_CODE_TO_MODE = {code: mode for mode, code in _MODE_TO_CODE.items()}
_EXCURSION_MODES = frozenset(_MODE_TO_CODE)
_EXCURSION_NEURON_FLAGS = 0x07


class VisualizationFormatError(ValueError):
    """Raised when a diagnostic snapshot is invalid or unsupported."""


def _finite(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _bounded_uint(value: int, name: str, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= maximum:
        raise ValueError(f"{name} must be an integer in [0, {maximum}]")
    return value


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")
    if len(value.encode("utf-8")) > MAX_IDENTIFIER_BYTES:
        raise ValueError(f"{name} exceeds {MAX_IDENTIFIER_BYTES} UTF-8 bytes")
    return value


@dataclass(frozen=True, slots=True)
class NeuronRecord:
    """Legitimately observable neuron state at one capture boundary."""

    neuron_id: str
    active: bool
    state: float
    activation: float
    processed_events: int
    position: tuple[int, int] | None = None

    def __post_init__(self) -> None:
        _identifier(self.neuron_id, "neuron_id")
        if not isinstance(self.active, bool):
            raise TypeError("active must be a boolean")
        object.__setattr__(self, "state", _finite(self.state, "state"))
        object.__setattr__(self, "activation", _finite(self.activation, "activation"))
        object.__setattr__(self, "processed_events", _bounded_uint(self.processed_events, "processed_events", 0xFFFFFFFF))
        if self.position is not None:
            if (not isinstance(self.position, tuple) or len(self.position) != 2 or
                    any(isinstance(value, bool) or not isinstance(value, int) or not -0x80000000 <= value <= 0x7FFFFFFF
                        for value in self.position)):
                raise ValueError("position must contain two signed 32-bit integers")

    @classmethod
    def from_neuron(cls, neuron: object, *, position: tuple[int, int] | None = None) -> "NeuronRecord":
        return cls(
            neuron_id=getattr(neuron, "neuron_id"),
            active=bool(getattr(neuron, "activation") != 0.0),
            state=getattr(neuron, "state"),
            activation=getattr(neuron, "activation"),
            processed_events=getattr(neuron, "processed_events"),
            position=position,
        )


@dataclass(frozen=True, slots=True)
class ExcursionNeuronRecord:
    """Instantaneous EXCURSION_V1 observation; activation is not defined."""

    neuron_id: str
    active: bool
    mode: E1Mode
    state: float
    pending_internal_work: bool
    processed_events: int
    position: tuple[int, int] | None = None

    def __post_init__(self) -> None:
        _identifier(self.neuron_id, "neuron_id")
        if not isinstance(self.mode, E1Mode) or self.mode not in _EXCURSION_MODES:
            raise ValueError("mode must be a supported excursion mode")
        if not isinstance(self.active, bool):
            raise TypeError("active must be a boolean")
        if self.active != (self.mode != E1Mode.N):
            raise ValueError("active must equal (mode != N)")
        if not isinstance(self.pending_internal_work, bool):
            raise TypeError("pending_internal_work must be a boolean")
        object.__setattr__(self, "state", _finite(self.state, "state"))
        object.__setattr__(
            self, "processed_events",
            _bounded_uint(self.processed_events, "processed_events", 0xFFFFFFFF),
        )
        if self.position is not None:
            if (not isinstance(self.position, tuple) or len(self.position) != 2 or
                    any(isinstance(value, bool) or not isinstance(value, int) or
                        not -0x80000000 <= value <= 0x7FFFFFFF
                        for value in self.position)):
                raise ValueError("position must contain two signed 32-bit integers")

    @classmethod
    def from_neuron(
        cls,
        neuron: MultiExcursionNeuron,
        *,
        position: tuple[int, int] | None = None,
    ) -> "ExcursionNeuronRecord":
        if not isinstance(neuron, MultiExcursionNeuron):
            raise TypeError("neuron must be a MultiExcursionNeuron")
        mode = neuron.mode
        return cls(
            neuron_id=neuron.neuron_id,
            active=mode != E1Mode.N,
            mode=mode,
            state=neuron.state,
            pending_internal_work=neuron.pending_internal_event is not None,
            processed_events=neuron.processed_event_count,
            position=position,
        )


@dataclass(frozen=True, slots=True)
class ConnectionRecord:
    """A directed topology edge; no synthetic strength is invented."""

    source: str
    destination: str
    propagation_delay: float

    def __post_init__(self) -> None:
        _identifier(self.source, "source")
        _identifier(self.destination, "destination")
        delay = _finite(self.propagation_delay, "propagation_delay")
        if delay < 0.0:
            raise ValueError("propagation_delay must be nonnegative")
        object.__setattr__(self, "propagation_delay", delay)


@dataclass(frozen=True, slots=True)
class VisualizationSnapshot:
    """Immutable, bounded pull snapshot detached from TPCN execution."""

    timestamp: float
    epoch: int
    neurons: tuple[NeuronRecord | ExcursionNeuronRecord, ...] = ()
    connections: tuple[ConnectionRecord, ...] = ()
    incomplete: bool = False
    format_version: int = FORMAT_VERSION

    def __post_init__(self) -> None:
        timestamp = _finite(self.timestamp, "timestamp")
        if timestamp < 0.0:
            raise ValueError("timestamp must be nonnegative")
        object.__setattr__(self, "timestamp", timestamp)
        object.__setattr__(self, "epoch", _bounded_uint(self.epoch, "epoch", 0xFFFFFFFF))
        if (isinstance(self.format_version, bool) or
                not isinstance(self.format_version, int) or
                self.format_version not in (FORMAT_VERSION, EXCURSION_FORMAT_VERSION)):
            raise ValueError("unsupported snapshot version")
        neurons = tuple(self.neurons)
        connections = tuple(self.connections)
        if len(neurons) > MAX_RECORDS or len(connections) > MAX_RECORDS:
            raise ValueError(f"a snapshot supports at most {MAX_RECORDS} records of each kind")
        expected_neuron_type = (
            ExcursionNeuronRecord
            if self.format_version == EXCURSION_FORMAT_VERSION
            else NeuronRecord
        )
        if any(not isinstance(item, expected_neuron_type) for item in neurons):
            raise TypeError(
                f"TPCV-{self.format_version} neurons must contain "
                f"{expected_neuron_type.__name__} values"
            )
        if any(not isinstance(item, ConnectionRecord) for item in connections):
            raise TypeError("connections must contain ConnectionRecord values")
        if len({item.neuron_id for item in neurons}) != len(neurons):
            raise ValueError("neuron identifiers must be unique")
        if len({(item.source, item.destination) for item in connections}) != len(connections):
            raise ValueError("connection endpoints must be unique")
        if not isinstance(self.incomplete, bool):
            raise TypeError("incomplete must be a boolean")
        object.__setattr__(self, "neurons", tuple(sorted(neurons, key=lambda item: item.neuron_id)))
        object.__setattr__(self, "connections", tuple(sorted(connections, key=lambda item: (item.source, item.destination))))

    @classmethod
    def from_components(
        cls,
        neurons: Iterable[object] = (),
        *,
        topology: object | None = None,
        timestamp: float | None = None,
        epoch: int = 0,
        incomplete: bool = False,
    ) -> "VisualizationSnapshot":
        neuron_items = tuple(neurons)
        neuron_records: tuple[NeuronRecord | ExcursionNeuronRecord, ...] = tuple(
            item
            if isinstance(item, (NeuronRecord, ExcursionNeuronRecord))
            else (
                ExcursionNeuronRecord.from_neuron(item)
                if isinstance(item, MultiExcursionNeuron)
                else NeuronRecord.from_neuron(item)
            )
            for item in neuron_items
        )
        versions = {
            EXCURSION_FORMAT_VERSION if isinstance(item, ExcursionNeuronRecord) else FORMAT_VERSION
            for item in neuron_records
        }
        if len(versions) > 1:
            raise ValueError("a snapshot cannot mix TPCV-1 and TPCV-2 neuron records")
        format_version = next(iter(versions), FORMAT_VERSION)
        edges = () if topology is None else tuple(
            ConnectionRecord(edge.source, edge.destination, edge.propagation_delay)
            for edge in getattr(topology, "edges")
        )
        if timestamp is None:
            timestamp = max((getattr(item, "clock").timestamp for item in neuron_items), default=0.0)
        return cls(timestamp, epoch, neuron_records, edges, incomplete, format_version)


def export_snapshot(snapshot: VisualizationSnapshot, *, max_bytes: int = MAX_EXPORT_BYTES) -> bytes:
    """Encode one snapshot in its canonical versioned TPCV format."""
    if not isinstance(snapshot, VisualizationSnapshot):
        raise TypeError("snapshot must be a VisualizationSnapshot")
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes <= 0:
        raise ValueError("max_bytes must be a positive integer")
    flags = INCOMPLETE_CAPTURE if snapshot.incomplete else 0
    body = bytearray()
    if snapshot.format_version == FORMAT_VERSION:
        for neuron in snapshot.neurons:
            identifier = neuron.neuron_id.encode("utf-8")
            neuron_flags = (1 if neuron.active else 0) | (2 if neuron.position is not None else 0)
            body.extend(struct.pack(">B", len(identifier)))
            body.extend(identifier)
            body.extend(_NEURON_FIXED.pack(neuron_flags, 0, neuron.state, neuron.activation, neuron.processed_events))
            if neuron.position is not None:
                body.extend(struct.pack(">ii", *neuron.position))
    else:
        for neuron in snapshot.neurons:
            identifier = neuron.neuron_id.encode("utf-8")
            neuron_flags = (
                (1 if neuron.active else 0)
                | (2 if neuron.position is not None else 0)
                | (4 if neuron.pending_internal_work else 0)
            )
            body.extend(struct.pack(">B", len(identifier)))
            body.extend(identifier)
            body.extend(_EXCURSION_NEURON_FIXED.pack(
                neuron_flags, _MODE_TO_CODE[neuron.mode], neuron.state, neuron.processed_events,
            ))
            if neuron.position is not None:
                body.extend(struct.pack(">ii", *neuron.position))
    for connection in snapshot.connections:
        source = connection.source.encode("utf-8")
        destination = connection.destination.encode("utf-8")
        body.extend(struct.pack(">B", len(source)))
        body.extend(source)
        body.extend(struct.pack(">B", len(destination)))
        body.extend(destination)
        body.extend(_CONNECTION_FIXED.pack(connection.propagation_delay))
    header = _HEADER.pack(MAGIC, snapshot.format_version, flags, 0, snapshot.epoch, snapshot.timestamp,
                          len(snapshot.neurons), len(snapshot.connections), len(body))
    result = header + bytes(body)
    if len(result) > min(max_bytes, MAX_EXPORT_BYTES):
        raise OverflowError("snapshot exceeds the bounded export size")
    return result


def parse_snapshot(data: bytes | bytearray | memoryview, *, max_bytes: int = MAX_EXPORT_BYTES) -> VisualizationSnapshot:
    """Parse and validate one complete canonical snapshot."""
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data must be bytes-like")
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes <= 0:
        raise ValueError("max_bytes must be a positive integer")
    data_size = data.nbytes if isinstance(data, memoryview) else len(data)
    if data_size > min(max_bytes, MAX_EXPORT_BYTES):
        raise VisualizationFormatError("snapshot exceeds the bounded parser size")
    raw = bytes(data)
    if len(raw) < _HEADER.size:
        raise VisualizationFormatError("snapshot header is truncated")
    magic, version, flags, reserved, epoch, timestamp, neuron_count, connection_count, body_length = _HEADER.unpack_from(raw)
    if magic != MAGIC:
        raise VisualizationFormatError("invalid snapshot magic")
    if version not in (FORMAT_VERSION, EXCURSION_FORMAT_VERSION):
        raise VisualizationFormatError(f"unsupported snapshot version: {version}")
    if flags & ~INCOMPLETE_CAPTURE or reserved:
        raise VisualizationFormatError("reserved header bits are nonzero")
    if neuron_count > MAX_RECORDS or connection_count > MAX_RECORDS:
        raise VisualizationFormatError("record count exceeds the bounded format")
    if body_length != len(raw) - _HEADER.size:
        raise VisualizationFormatError("snapshot framing length does not match payload")
    offset = _HEADER.size
    neurons: list[NeuronRecord | ExcursionNeuronRecord] = []
    try:
        for _ in range(neuron_count):
            identifier_length = raw[offset]
            offset += 1
            identifier = raw[offset:offset + identifier_length].decode("utf-8")
            offset += identifier_length
            position = None
            if version == FORMAT_VERSION:
                neuron_flags, reserved_neuron, state, activation, processed_events = _NEURON_FIXED.unpack_from(raw, offset)
                offset += _NEURON_FIXED.size
                if reserved_neuron or neuron_flags & ~0x03:
                    raise VisualizationFormatError("reserved neuron bits are nonzero")
                if neuron_flags & 0x02:
                    position = struct.unpack_from(">ii", raw, offset)
                    offset += 8
                neurons.append(
                    NeuronRecord(
                        identifier, bool(neuron_flags & 1), state, activation,
                        processed_events, position,
                    )
                )
            else:
                neuron_flags, mode_code, state, processed_events = _EXCURSION_NEURON_FIXED.unpack_from(raw, offset)
                offset += _EXCURSION_NEURON_FIXED.size
                if neuron_flags & ~_EXCURSION_NEURON_FLAGS:
                    raise VisualizationFormatError("reserved neuron bits are nonzero")
                if mode_code not in _CODE_TO_MODE:
                    raise VisualizationFormatError("invalid excursion mode")
                if neuron_flags & 0x02:
                    position = struct.unpack_from(">ii", raw, offset)
                    offset += 8
                mode = _CODE_TO_MODE[mode_code]
                try:
                    neurons.append(ExcursionNeuronRecord(
                        identifier,
                        bool(neuron_flags & 1),
                        mode,
                        state,
                        bool(neuron_flags & 0x04),
                        processed_events,
                        position,
                    ))
                except (ValueError, TypeError) as error:
                    raise VisualizationFormatError(
                        f"malformed TPCV-2 neuron record: {error}"
                    ) from error
        connections: list[ConnectionRecord] = []
        for _ in range(connection_count):
            source_length = raw[offset]
            offset += 1
            source = raw[offset:offset + source_length].decode("utf-8")
            offset += source_length
            destination_length = raw[offset]
            offset += 1
            destination = raw[offset:offset + destination_length].decode("utf-8")
            offset += destination_length
            delay = _CONNECTION_FIXED.unpack_from(raw, offset)[0]
            offset += _CONNECTION_FIXED.size
            connections.append(ConnectionRecord(source, destination, delay))
    except (IndexError, UnicodeDecodeError, struct.error, ValueError, TypeError) as error:
        if isinstance(error, VisualizationFormatError):
            raise
        raise VisualizationFormatError("malformed snapshot record") from error
    if offset != len(raw):
        raise VisualizationFormatError("snapshot contains trailing bytes")
    try:
        return VisualizationSnapshot(
            timestamp, epoch, tuple(neurons), tuple(connections),
            bool(flags & INCOMPLETE_CAPTURE), version,
        )
    except (ValueError, TypeError) as error:
        raise VisualizationFormatError("snapshot contains invalid values") from error


class SnapshotCollector:
    """Optional bounded diagnostic buffer; it is never part of execution."""

    def __init__(self, *, enabled: bool = True, capacity: int = 64) -> None:
        self.enabled = enabled
        self.capacity = _bounded_uint(capacity, "capacity", MAX_RECORDS)
        if self.capacity == 0:
            raise ValueError("capacity must be positive")
        self._snapshots: list[VisualizationSnapshot] = []

    @property
    def snapshots(self) -> tuple[VisualizationSnapshot, ...]:
        return tuple(self._snapshots)

    def capture(self, snapshot: VisualizationSnapshot) -> bytes | None:
        if not self.enabled:
            return None
        if len(self._snapshots) >= self.capacity:
            raise OverflowError("snapshot collector capacity reached")
        self._snapshots.append(snapshot)
        return export_snapshot(snapshot)


class ReferenceVisualizer:
    """Machine-readable reference visualizer for offline snapshot inspection."""

    def __init__(self, snapshots: Iterable[VisualizationSnapshot] = ()) -> None:
        self.snapshots = tuple(snapshots)
        versions = {snapshot.format_version for snapshot in self.snapshots}
        if len(versions) > 1:
            raise ValueError("a replay sequence cannot mix TPCV versions")

    @classmethod
    def load(cls, records: Iterable[bytes | bytearray | memoryview]) -> "ReferenceVisualizer":
        return cls(parse_snapshot(record) for record in records)

    def frames(self) -> tuple[dict[str, object], ...]:
        frames = []
        for snapshot in self.snapshots:
            frame: dict[str, object] = {
                "epoch": snapshot.epoch,
                "timestamp": snapshot.timestamp,
                "incomplete": snapshot.incomplete,
                "neurons": tuple(
                    (
                        item.neuron_id, item.active, item.state, item.activation,
                    )
                    if isinstance(item, NeuronRecord)
                    else (
                        item.neuron_id, item.active, item.state, None, item.mode.value,
                        item.pending_internal_work, item.processed_events,
                    )
                    for item in snapshot.neurons
                ),
                "connections": tuple(
                    (item.source, item.destination, item.propagation_delay)
                    for item in snapshot.connections
                ),
            }
            if snapshot.format_version == EXCURSION_FORMAT_VERSION:
                frame["format_version"] = EXCURSION_FORMAT_VERSION
            frames.append(frame)
        return tuple(frames)

    def changes(self) -> tuple[dict[str, object], ...]:
        changes: list[dict[str, object]] = []
        for previous, current in zip(self.snapshots, self.snapshots[1:]):
            previous_neurons = {item.neuron_id: item for item in previous.neurons}
            current_neurons = {item.neuron_id: item for item in current.neurons}
            previous_edges = {(item.source, item.destination) for item in previous.connections}
            current_edges = {(item.source, item.destination) for item in current.connections}
            changes.append({
                "from_epoch": previous.epoch,
                "to_epoch": current.epoch,
                "changed_neurons": tuple(sorted(identifier for identifier in current_neurons
                                                if identifier in previous_neurons and current_neurons[identifier] != previous_neurons[identifier])),
                "added_neurons": tuple(sorted(set(current_neurons) - set(previous_neurons))),
                "removed_neurons": tuple(sorted(set(previous_neurons) - set(current_neurons))),
                "added_connections": tuple(sorted(current_edges - previous_edges)),
                "removed_connections": tuple(sorted(previous_edges - current_edges)),
            })
        return tuple(changes)

    def connection_timeline(self) -> tuple[dict[str, object], ...]:
        """Describe real edge persistence and deltas without mutating execution."""
        timeline: list[dict[str, object]] = []
        for previous, current in zip(self.snapshots, self.snapshots[1:]):
            previous_edges = {(item.source, item.destination) for item in previous.connections}
            current_edges = {(item.source, item.destination) for item in current.connections}
            timeline.append({
                "from_epoch": previous.epoch,
                "to_epoch": current.epoch,
                "unchanged_connections": tuple(sorted(previous_edges & current_edges)),
                "added_connections": tuple(sorted(current_edges - previous_edges)),
                "recently_pruned_connections": tuple(sorted(previous_edges - current_edges)),
            })
        return tuple(timeline)


__all__ = [
    "ConnectionRecord", "EXCURSION_FORMAT_VERSION", "ExcursionNeuronRecord",
    "FORMAT_VERSION", "MAX_EXPORT_BYTES", "MAX_RECORDS", "NeuronRecord",
    "ReferenceVisualizer", "SnapshotCollector", "VisualizationFormatError", "VisualizationSnapshot",
    "export_snapshot", "parse_snapshot",
]