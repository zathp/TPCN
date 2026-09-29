"""Bounded, label-free streaming character readout outside the TPCN core."""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real

from .event_runtime import Event
from .stroke_dataset import END_CHARACTER, START_CHARACTER


END_STROKE = "end_stroke"
ACTIVITY_EVENT = "activity"
CLASS_LABELS = tuple(chr(ord("A") + index) for index in range(26))


def _finite(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


@dataclass(frozen=True, slots=True)
class ClassEvidence:
    """Non-authoritative inspection data for the active character."""

    scores: tuple[float, ...]
    probabilities: tuple[float, ...]
    confidence: float
    event_count: int
    character_index: int | None


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    """One authoritative result emitted at a character boundary."""

    label: str
    class_index: int
    scores: tuple[float, ...]
    probabilities: tuple[float, ...]
    confidence: float
    character_index: int
    start_source: str
    start_timestamp: float
    start_sequence: int
    end_source: str
    end_timestamp: float
    end_sequence: int
    activity_event_count: int


class StreamingCharacterClassifier:
    """Read bounded numeric TPCN activity and classify completed characters."""

    def __init__(self, *, max_activity_events: int = 4096, activity_gain: float = 0.25) -> None:
        if isinstance(max_activity_events, bool) or not isinstance(max_activity_events, int):
            raise TypeError("max_activity_events must be an integer")
        if max_activity_events <= 0:
            raise ValueError("max_activity_events must be positive")
        self.max_activity_events = max_activity_events
        self.activity_gain = _finite(activity_gain, "activity_gain")
        if self.activity_gain < 0.0:
            raise ValueError("activity_gain must be nonnegative")
        self.reset()

    @property
    def class_labels(self) -> tuple[str, ...]:
        return CLASS_LABELS

    @property
    def is_active(self) -> bool:
        return self._active

    @property
    def authoritative_result(self) -> ClassificationResult | None:
        return self._result

    @property
    def activity_event_count(self) -> int:
        return self._activity_event_count

    @property
    def local_timestamp(self) -> float:
        return self._last_timestamp

    def reset(self) -> None:
        """Clear character-local state and any prior authoritative result."""
        self._active = False
        self._scores = [0.0] * len(CLASS_LABELS)
        self._activity_event_count = 0
        self._character_index: int | None = None
        self._start_event: Event | None = None
        self._result: ClassificationResult | None = None
        self._last_timestamp = 0.0

    def _validate_timestamp(self, timestamp: float) -> None:
        if timestamp < self._last_timestamp:
            raise ValueError("classifier events must have nondecreasing timestamps")

    def _commit_timestamp(self, timestamp: float) -> None:
        self._last_timestamp = timestamp

    def ingest_event(self, event: Event) -> ClassEvidence | ClassificationResult | None:
        """Consume one canonical boundary or numeric TPCN activity event."""
        if not isinstance(event, Event):
            raise TypeError("event must be a canonical Event")
        self._validate_timestamp(event.timestamp)

        if event.event_type == START_CHARACTER:
            if self._active:
                raise ValueError("character is already active")
            self._active = True
            self._scores = [0.0] * len(CLASS_LABELS)
            self._activity_event_count = 0
            self._result = None
            self._start_event = event
            self._character_index = getattr(event.payload, "character_index", None)
            self._commit_timestamp(event.timestamp)
            return None

        if event.event_type == END_STROKE:
            if not self._active:
                raise ValueError("stroke boundary received outside an active character")
            evidence = self.evidence()
            self._commit_timestamp(event.timestamp)
            return evidence

        if event.event_type == END_CHARACTER:
            return self.finalize_character(event)

        if not self._active:
            raise ValueError("activity received outside an active character")
        return self.ingest_activity(event)

    def ingest_activity(self, event: Event) -> ClassEvidence:
        """Consume one numeric activity event during the active character."""
        if not isinstance(event, Event):
            raise TypeError("event must be a canonical Event")
        if not self._active:
            raise ValueError("activity received outside an active character")
        if event.event_type != ACTIVITY_EVENT:
            raise ValueError("event is not a classifier activity event")
        self._validate_timestamp(event.timestamp)
        activity = _finite(event.payload, "activity payload")
        if self._activity_event_count >= self.max_activity_events:
            raise BufferError("character activity capacity reached")
        for class_index in range(len(self._scores)):
            direction = (class_index - 12.5) / 12.5
            self._scores[class_index] = max(
                -1.0,
                min(1.0, self._scores[class_index] + self.activity_gain * activity * direction),
            )
        self._activity_event_count += 1
        self._commit_timestamp(event.timestamp)
        return self.evidence()

    def finalize_character(self, end_event: Event) -> ClassificationResult:
        """Emit the sole authoritative result for a completed character."""
        if not isinstance(end_event, Event) or end_event.event_type != END_CHARACTER:
            raise ValueError("finalization requires an END_CHARACTER event")
        if not self._active or self._start_event is None:
            raise ValueError("no active character to finalize")
        self._validate_timestamp(end_event.timestamp)
        character_index = getattr(end_event.payload, "character_index", self._character_index)
        if character_index is None:
            raise ValueError("character boundary must provide character_index")
        self._character_index = int(character_index)
        self._result = self._finalize(end_event)
        self._active = False
        self._commit_timestamp(end_event.timestamp)
        return self._result

    def evidence(self) -> ClassEvidence:
        """Return a snapshot without changing state or finalizing the character."""
        probabilities = self._probabilities()
        return ClassEvidence(
            tuple(self._scores), probabilities, max(probabilities),
            self._activity_event_count, self._character_index,
        )

    def _probabilities(self) -> tuple[float, ...]:
        peak = max(self._scores)
        exponentials = tuple(math.exp(score - peak) for score in self._scores)
        total = sum(exponentials)
        return tuple(value / total for value in exponentials)

    def _finalize(self, end_event: Event) -> ClassificationResult:
        probabilities = self._probabilities()
        class_index = max(range(len(self._scores)), key=lambda index: (self._scores[index], -index))
        assert self._start_event is not None
        return ClassificationResult(
            CLASS_LABELS[class_index], class_index, tuple(self._scores),
            probabilities, probabilities[class_index],
            self._character_index if self._character_index is not None else 0,
            self._start_event.source, self._start_event.timestamp, self._start_event.sequence,
            end_event.source, end_event.timestamp, end_event.sequence, self._activity_event_count,
        )


__all__ = [
    "ACTIVITY_EVENT",
    "CLASS_LABELS",
    "ClassEvidence",
    "ClassificationResult",
    "END_STROKE",
    "StreamingCharacterClassifier",
]