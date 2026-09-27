"""Bounded causal encoding for sequential stroke records.

This adapter deliberately does not select a dataset or implement a classifier.
Labels and split membership remain external to the event payloads.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from numbers import Real
from typing import Iterable

from .event_runtime import Event


START_CHARACTER = "start_character"
STROKE_EVENT = "stroke"
END_CHARACTER = "end_character"


def _finite(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


@dataclass(frozen=True, slots=True)
class StrokePoint:
    """One native point supplied by an external dataset adapter."""

    x: float
    y: float
    timestamp: float | None = None
    pen_state: int = 1
    stroke_boundary: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _finite(self.x, "x"))
        object.__setattr__(self, "y", _finite(self.y, "y"))
        if self.timestamp is not None:
            timestamp = _finite(self.timestamp, "timestamp")
            if timestamp < 0.0:
                raise ValueError("timestamp must be nonnegative")
            object.__setattr__(self, "timestamp", timestamp)
        if isinstance(self.pen_state, bool) or not isinstance(self.pen_state, int):
            raise TypeError("pen_state must be an integer")


@dataclass(frozen=True, slots=True)
class StrokeEvent:
    """Causal features for one point; it intentionally has no label field."""

    x: float
    y: float
    dx: float
    dy: float
    pen_state: int
    stroke_boundary: bool


@dataclass(frozen=True, slots=True)
class CharacterBoundary:
    """Boundary metadata carried by the stream without task labels."""

    character_index: int


@dataclass(frozen=True, slots=True)
class LabeledCharacter:
    """External evaluation/training metadata, never a neural event payload."""

    character_id: str
    points: tuple[StrokePoint, ...]
    label: str | None = None
    split: str | None = None
    writer_id: str | None = None


@dataclass(frozen=True, slots=True)
class DatasetMetadata:
    """A declaration required by a benchmark runner, not a dataset claim."""

    name: str
    version: str
    permitted_use: str
    classes: tuple[str, ...] | None
    train_ids: tuple[str, ...]
    validation_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    writer_disjoint: bool | None


class CausalNormalizer:
    """Training-fitted affine normalization with no sequence look-ahead."""

    def __init__(self, x_offset: float, x_scale: float, y_offset: float, y_scale: float,
                 delta_scale: float) -> None:
        self.x_offset = _finite(x_offset, "x_offset")
        self.x_scale = self._positive_scale(x_scale, "x_scale")
        self.y_offset = _finite(y_offset, "y_offset")
        self.y_scale = self._positive_scale(y_scale, "y_scale")
        self.delta_scale = self._positive_scale(delta_scale, "delta_scale")

    @staticmethod
    def _positive_scale(value: Real, name: str) -> float:
        result = abs(_finite(value, name))
        return max(result, 1e-12)

    @classmethod
    def fit_training(cls, points: Iterable[StrokePoint]) -> "CausalNormalizer":
        values = tuple(points)
        if not values:
            raise ValueError("at least one training point is required")
        xs = [point.x for point in values]
        ys = [point.y for point in values]
        deltas = [abs(point.x) + abs(point.y) for point in values]
        return cls(
            (min(xs) + max(xs)) / 2.0,
            (max(xs) - min(xs)) / 2.0,
            (min(ys) + max(ys)) / 2.0,
            (max(ys) - min(ys)) / 2.0,
            max(deltas),
        )

    def transform(self, point: StrokePoint, previous: StrokePoint | None) -> StrokeEvent:
        previous_x = point.x if previous is None else previous.x
        previous_y = point.y if previous is None else previous.y
        return StrokeEvent(
            (point.x - self.x_offset) / self.x_scale,
            (point.y - self.y_offset) / self.y_scale,
            (point.x - previous_x) / self.delta_scale,
            (point.y - previous_y) / self.delta_scale,
            point.pen_state,
            point.stroke_boundary,
        )


class StrokeStreamEncoder:
    """Encode one finite character as ordered runtime events."""

    def __init__(self, normalizer: CausalNormalizer, *, max_points: int,
                 synthetic_interval: float | None = None) -> None:
        if isinstance(max_points, bool) or not isinstance(max_points, int) or max_points <= 0:
            raise ValueError("max_points must be a positive integer")
        self.normalizer = normalizer
        self.max_points = max_points
        if synthetic_interval is not None:
            synthetic_interval = _finite(synthetic_interval, "synthetic_interval")
            if synthetic_interval <= 0.0:
                raise ValueError("synthetic_interval must be positive")
        self.synthetic_interval = synthetic_interval
        self._character_index = 0
        self.reset()

    def reset(self) -> None:
        self._previous: StrokePoint | None = None
        self._active = False

    def encode(self, points: Iterable[StrokePoint], *, source: str,
               destination: str) -> tuple[Event, ...]:
        if not source or not destination:
            raise ValueError("source and destination must be non-empty")
        materialized = tuple(points)
        if not materialized:
            raise ValueError("a character must contain at least one point")
        if len(materialized) > self.max_points:
            raise BufferError("character point capacity reached")
        self.reset()
        self._active = True
        index = self._character_index
        events: list[Event] = []
        timestamp = self._timestamp(materialized[0], None)
        events.append(Event(timestamp, source, destination, START_CHARACTER, CharacterBoundary(index)))
        previous: StrokePoint | None = None
        last_timestamp = timestamp
        for point in materialized:
            timestamp = self._timestamp(point, previous, last_timestamp)
            if timestamp < last_timestamp:
                raise ValueError("stroke timestamps must be nondecreasing")
            events.append(Event(timestamp, source, destination, STROKE_EVENT,
                                self.normalizer.transform(point, previous)))
            previous = point
            last_timestamp = timestamp
        events.append(Event(last_timestamp, source, destination, END_CHARACTER, CharacterBoundary(index)))
        self._previous = None
        self._active = False
        self._character_index += 1
        return tuple(events)

    def _timestamp(self, point: StrokePoint, previous: StrokePoint | None,
                   previous_timestamp: float | None = None) -> float:
        if point.timestamp is not None:
            return point.timestamp
        if self.synthetic_interval is None:
            raise ValueError("timestamps are required unless synthetic_interval is declared")
        if previous is None:
            return 0.0
        return (previous_timestamp if previous_timestamp is not None else 0.0) + self.synthetic_interval


def serialize_stream(events: Iterable[Event]) -> tuple[tuple[object, ...], ...]:
    """Return a deterministic, label-free representation suitable for replay."""
    serialized: list[tuple[object, ...]] = []
    for event in events:
        payload = event.payload
        if hasattr(payload, "__dataclass_fields__"):
            payload_value: object = tuple(sorted(asdict(payload).items()))
        else:
            payload_value = payload
        serialized.append((event.timestamp, event.source, event.destination,
                           str(event.event_type), payload_value))
    return tuple(serialized)


__all__ = [
    "CausalNormalizer",
    "CharacterBoundary",
    "DatasetMetadata",
    "END_CHARACTER",
    "LabeledCharacter",
    "START_CHARACTER",
    "STROKE_EVENT",
    "StrokeEvent",
    "StrokePoint",
    "StrokeStreamEncoder",
    "serialize_stream",
]