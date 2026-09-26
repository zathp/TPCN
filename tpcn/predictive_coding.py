"""Bounded local prediction matching and causally queued error events.

Prediction semantics are local and event-driven. A prediction is a scalar
target value identified by ``(predictor_id, sequence)`` and associated with an
explicit target key. An observation carries that key and a scalar value. The
oldest eligible prediction for a key wins, with the deterministic prediction
ID as tie-breaker. Error is ``observed - predicted``.

Observations match by event timestamp, so delayed observations may resolve
predictions after arbitrary local-time intervals. Expiry is exclusive: an
observation at the expiry timestamp is eligible, while one after it is not.
Error events use the observation timestamp as their causal timestamp and are
queued through Luna-1; a supplied topology performs finite delayed routing.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real
from typing import TYPE_CHECKING

from .event_runtime import Event, EventQueue, LocalClock

if TYPE_CHECKING:
    from .canonical_neuron import TPCNNeuron
    from .topology import BoundedTopology


PREDICTION_EVENT = "prediction"
PREDICTION_ERROR_EVENT = "prediction_error"


def _finite_real(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _optional_time(value: Real | None, name: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number or None")
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


@dataclass(frozen=True, slots=True)
class Prediction:
    """One bounded outstanding local prediction record."""

    prediction_id: str
    predictor_id: str
    target_key: str
    predicted_value: float
    created_at: float
    expected_resolution_at: float | None
    expires_at: float | None


@dataclass(frozen=True, slots=True)
class Observation:
    """The local value that can resolve a prediction with the same key."""

    target_key: str
    observed_value: float

    def __post_init__(self) -> None:
        if not isinstance(self.target_key, str) or not self.target_key:
            raise ValueError("target_key must be a non-empty string")
        object.__setattr__(self, "observed_value", _finite_real(self.observed_value, "observed_value"))


@dataclass(frozen=True, slots=True)
class PredictionError:
    """Explicit local error information carried by an error event."""

    prediction_id: str
    predictor_id: str
    target_key: str
    predicted_value: float
    observed_value: float
    error: float
    prediction_timestamp: float
    observation_timestamp: float
    observation_source: str


@dataclass(frozen=True, slots=True)
class PredictionResolution:
    """Result of processing one observation."""

    status: str
    prediction: Prediction | None
    error: PredictionError | None


class PredictionCapacityError(BufferError):
    """Raised when bounded outstanding prediction capacity is full."""


class LocalPredictor:
    """A bounded predictor with no global registry or fixed timestep."""

    def __init__(self, predictor_id: str, *, max_outstanding: int, error_destination: str) -> None:
        if not isinstance(predictor_id, str) or not predictor_id:
            raise ValueError("predictor_id must be a non-empty string")
        if isinstance(max_outstanding, bool) or not isinstance(max_outstanding, int) or max_outstanding <= 0:
            raise ValueError("max_outstanding must be a positive integer")
        if not isinstance(error_destination, str) or not error_destination:
            raise ValueError("error_destination must be a non-empty string")
        self.predictor_id = predictor_id
        self.max_outstanding = max_outstanding
        self.error_destination = error_destination
        self.clock = LocalClock()
        self._next_sequence = 0
        self._outstanding: dict[str, Prediction] = {}
        self.matched_count = 0
        self.unmatched_observation_count = 0
        self.expired_count = 0

    @property
    def outstanding_count(self) -> int:
        return len(self._outstanding)

    @property
    def outstanding_predictions(self) -> tuple[Prediction, ...]:
        return tuple(sorted(self._outstanding.values(), key=lambda item: (item.created_at, item.prediction_id)))

    def create_prediction(
        self,
        target_key: str,
        predicted_value: Real,
        *,
        timestamp: float | None = None,
        expected_resolution_at: float | None = None,
        expires_at: float | None = None,
    ) -> Prediction:
        if not isinstance(target_key, str) or not target_key:
            raise ValueError("target_key must be a non-empty string")
        if self.outstanding_count >= self.max_outstanding:
            raise PredictionCapacityError("outstanding prediction capacity reached")
        created_at = self.clock.timestamp if timestamp is None else _finite_real(timestamp, "timestamp")
        self.clock.advance_to(created_at)
        expected = _optional_time(expected_resolution_at, "expected_resolution_at")
        expires = _optional_time(expires_at, "expires_at")
        if expected is not None and expected < created_at:
            raise ValueError("expected_resolution_at cannot precede timestamp")
        if expires is not None and expires < created_at:
            raise ValueError("expires_at cannot precede timestamp")
        prediction_id = f"{self.predictor_id}:prediction:{self._next_sequence}"
        self._next_sequence += 1
        prediction = Prediction(
            prediction_id,
            self.predictor_id,
            target_key,
            _finite_real(predicted_value, "predicted_value"),
            created_at,
            expected,
            expires,
        )
        self._outstanding[prediction_id] = prediction
        return prediction

    def create_prediction_from_neuron(
        self,
        neuron: TPCNNeuron,
        target_key: str,
        *,
        expected_resolution_at: float | None = None,
        expires_at: float | None = None,
    ) -> Prediction:
        """Create a prediction from one canonical neuron's local activation."""
        return self.create_prediction(
            target_key,
            neuron.activation,
            timestamp=neuron.clock.timestamp,
            expected_resolution_at=expected_resolution_at,
            expires_at=expires_at,
        )

    def emit_prediction(
        self,
        prediction: Prediction,
        queue: EventQueue[Event],
        destination: str,
        *,
        delay: float = 0.0,
    ) -> Event:
        """Queue a prediction record without mutating its remote destination."""
        if prediction.predictor_id != self.predictor_id:
            raise ValueError("prediction does not belong to this predictor")
        if not isinstance(destination, str) or not destination:
            raise ValueError("destination must be a non-empty string")
        return queue.push_propagated(
            prediction.created_at,
            self.predictor_id,
            destination,
            PREDICTION_EVENT,
            prediction,
            delay,
        )

    def expire(self, timestamp: float) -> tuple[Prediction, ...]:
        """Expire records strictly before the supplied local timestamp."""
        current = _finite_real(timestamp, "timestamp")
        self.clock.advance_to(current)
        expired = tuple(
            sorted(
                (prediction for prediction in self._outstanding.values() if prediction.expires_at is not None and prediction.expires_at < current),
                key=lambda item: (item.expires_at, item.prediction_id),
            )
        )
        for prediction in expired:
            del self._outstanding[prediction.prediction_id]
        self.expired_count += len(expired)
        return expired

    def observe(self, event: Event) -> PredictionResolution:
        """Match one addressed local observation without emitting remotely."""
        if not isinstance(event.payload, Observation):
            raise TypeError("observation event payload must be an Observation")
        self.clock.advance_to(event.timestamp)
        self.expire(event.timestamp)
        candidates = [
            prediction
            for prediction in self._outstanding.values()
            if prediction.target_key == event.payload.target_key
            and (prediction.expires_at is None or event.timestamp <= prediction.expires_at)
        ]
        if not candidates:
            self.unmatched_observation_count += 1
            return PredictionResolution("unmatched", None, None)
        prediction = min(candidates, key=lambda item: (item.created_at, item.prediction_id))
        observed = event.payload.observed_value
        error = PredictionError(
            prediction.prediction_id,
            self.predictor_id,
            prediction.target_key,
            prediction.predicted_value,
            observed,
            observed - prediction.predicted_value,
            prediction.created_at,
            event.timestamp,
            event.source,
        )
        del self._outstanding[prediction.prediction_id]
        self.matched_count += 1
        return PredictionResolution("matched", prediction, error)

    def process_observation(
        self,
        event: Event,
        queue: EventQueue[Event],
        topology: BoundedTopology | None = None,
    ) -> PredictionResolution:
        """Resolve locally, then queue the explicit error through the runtime."""
        resolution = self.observe(event)
        if resolution.error is None:
            return resolution
        error_event = Event(
            event.timestamp,
            self.predictor_id,
            self.error_destination,
            PREDICTION_ERROR_EVENT,
            resolution.error,
        )
        if topology is None:
            queue.push(error_event)
        else:
            topology.route(error_event, queue)
        return resolution


__all__ = [
    "LocalPredictor",
    "Observation",
    "PREDICTION_EVENT",
    "PREDICTION_ERROR_EVENT",
    "Prediction",
    "PredictionCapacityError",
    "PredictionError",
    "PredictionResolution",
]