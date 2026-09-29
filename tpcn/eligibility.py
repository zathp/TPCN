"""Bounded local eligibility traces and causally delivered credit signals."""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real
from collections import OrderedDict

from .event_runtime import Event, LocalClock
from .predictive_coding import PredictionError


ELIGIBILITY_ACTIVITY_EVENT = "eligibility_activity"
REWARD_EVENT = "reward"


def _finite_real(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _nonnegative_real(value: Real, name: str) -> float:
    result = _finite_real(value, name)
    if result < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return result


@dataclass(frozen=True, slots=True)
class EligibilityActivity:
    """Local activity that can earn later credit."""

    trace_id: str
    magnitude: float
    prediction_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.trace_id, str) or not self.trace_id:
            raise ValueError("trace_id must be a non-empty string")
        object.__setattr__(self, "magnitude", _finite_real(self.magnitude, "magnitude"))
        if self.prediction_id is not None and (not isinstance(self.prediction_id, str) or not self.prediction_id):
            raise ValueError("prediction_id must be a non-empty string or None")


@dataclass(frozen=True, slots=True)
class RewardSignal:
    """A local reward with a stable logical delivery identity."""

    reward: float
    message_id: str
    trace_id: str | None = None
    prediction_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "reward", _finite_real(self.reward, "reward"))
        if not isinstance(self.message_id, str) or not self.message_id:
            raise ValueError("message_id must be a non-empty string")
        if self.trace_id is None and self.prediction_id is None:
            raise ValueError("trace_id or prediction_id is required")
        for value, name in ((self.trace_id, "trace_id"), (self.prediction_id, "prediction_id")):
            if value is not None and (not isinstance(value, str) or not value):
                raise ValueError(f"{name} must be a non-empty string or None")


@dataclass(frozen=True, slots=True)
class EligibilityTrace:
    trace_id: str
    prediction_id: str | None
    value: float
    credit: float
    last_timestamp: float


@dataclass(frozen=True, slots=True)
class CreditAttribution:
    status: str
    trace_id: str | None
    eligibility: float
    signal: float
    credit: float
    timestamp: float
    message_id: str | None = None


class EligibilityCapacityError(BufferError):
    """Raised when a new local trace would exceed finite trace capacity."""


class EligibilityLedger:
    """A finite, local ledger with timestamp-based exponential trace decay."""

    def __init__(
        self,
        ledger_id: str,
        *,
        max_traces: int,
        decay_time_constant: float,
        trace_limit: float = 1.0,
        credit_limit: float = 1.0,
        expiry: float | None = None,
        max_reward_identities: int = 64,
    ) -> None:
        if not isinstance(ledger_id, str) or not ledger_id:
            raise ValueError("ledger_id must be a non-empty string")
        if isinstance(max_traces, bool) or not isinstance(max_traces, int) or max_traces <= 0:
            raise ValueError("max_traces must be a positive integer")
        decay_time_constant = _nonnegative_real(decay_time_constant, "decay_time_constant")
        if decay_time_constant == 0.0:
            raise ValueError("decay_time_constant must be positive")
        trace_limit = _nonnegative_real(trace_limit, "trace_limit")
        credit_limit = _nonnegative_real(credit_limit, "credit_limit")
        if trace_limit == 0.0 or credit_limit == 0.0:
            raise ValueError("trace_limit and credit_limit must be positive")
        if expiry is not None:
            expiry = _nonnegative_real(expiry, "expiry")
        if (isinstance(max_reward_identities, bool) or not isinstance(max_reward_identities, int)
                or max_reward_identities <= 0):
            raise ValueError("max_reward_identities must be a positive integer")
        self.ledger_id = ledger_id
        self.max_traces = max_traces
        self.decay_time_constant = decay_time_constant
        self.trace_limit = trace_limit
        self.credit_limit = credit_limit
        self.expiry = expiry
        self.max_reward_identities = max_reward_identities
        self.clock = LocalClock()
        self._traces: dict[str, EligibilityTrace] = {}
        self._reward_identities: OrderedDict[str, str] = OrderedDict()

    @property
    def traces(self) -> tuple[EligibilityTrace, ...]:
        return tuple(self._traces.values())

    @property
    def retained_reward_identities(self) -> tuple[str, ...]:
        """Return accepted logical reward IDs in deterministic retention order."""
        return tuple(self._reward_identities)

    def reset(self) -> None:
        """Reset local traces, reward identity retention, and local time."""
        self.clock = LocalClock()
        self._traces.clear()
        self._reward_identities.clear()

    def _decay_to(self, timestamp: float) -> None:
        elapsed = self.clock.advance_to(timestamp)
        if not elapsed:
            return
        factor = math.exp(-elapsed / self.decay_time_constant)
        for trace_id, trace in tuple(self._traces.items()):
            value = trace.value * factor
            credit = trace.credit * factor
            if self.expiry is not None and timestamp - trace.last_timestamp > self.expiry:
                del self._traces[trace_id]
            else:
                self._traces[trace_id] = EligibilityTrace(trace_id, trace.prediction_id, value, credit, timestamp)

    def record_activity(self, event: Event) -> EligibilityTrace:
        if event.destination != self.ledger_id:
            raise ValueError("activity event does not address this ledger")
        if not isinstance(event.payload, EligibilityActivity):
            raise TypeError("activity event payload must be EligibilityActivity")
        activity = event.payload
        self._decay_to(event.timestamp)
        existing = self._traces.get(activity.trace_id)
        if existing is None and len(self._traces) >= self.max_traces:
            raise EligibilityCapacityError("eligibility trace capacity reached")
        value = activity.magnitude if existing is None else existing.value + activity.magnitude
        value = max(-self.trace_limit, min(self.trace_limit, value))
        credit = 0.0 if existing is None else existing.credit
        trace = EligibilityTrace(activity.trace_id, activity.prediction_id, value, credit, event.timestamp)
        self._traces[activity.trace_id] = trace
        return trace

    def apply_signal(self, event: Event) -> CreditAttribution:
        """Apply one causally arrived reward or signed prediction-error signal."""
        if event.destination != self.ledger_id:
            raise ValueError("credit event does not address this ledger")
        payload = event.payload
        if isinstance(payload, RewardSignal):
            signal = payload.reward
            trace_id = payload.trace_id
            prediction_id = payload.prediction_id
            message_id = payload.message_id
        elif isinstance(payload, PredictionError):
            signal = payload.error
            trace_id = None
            prediction_id = payload.prediction_id
            message_id = None
        else:
            raise TypeError("credit event payload must be RewardSignal or PredictionError")
        if message_id is not None and message_id in self._reward_identities:
            return CreditAttribution(
                "duplicate", self._reward_identities[message_id], 0.0, signal, 0.0,
                event.timestamp, message_id,
            )
        matches = [
            trace for trace in self._traces.values()
            if trace_id == trace.trace_id or (prediction_id is not None and prediction_id == trace.prediction_id)
        ]
        if not matches:
            return CreditAttribution("unmatched", None, 0.0, signal, 0.0, event.timestamp, message_id)
        self._decay_to(event.timestamp)
        matches = [
            trace for trace in self._traces.values()
            if trace_id == trace.trace_id or (prediction_id is not None and prediction_id == trace.prediction_id)
        ]
        if not matches:
            return CreditAttribution("expired", None, 0.0, signal, 0.0, event.timestamp, message_id)
        trace = min(matches, key=lambda item: item.trace_id)
        credit = max(-self.credit_limit, min(self.credit_limit, trace.credit + trace.value * signal))
        self._traces[trace.trace_id] = EligibilityTrace(trace.trace_id, trace.prediction_id, trace.value, credit, event.timestamp)
        if message_id is not None:
            self._reward_identities[message_id] = trace.trace_id
            while len(self._reward_identities) > self.max_reward_identities:
                self._reward_identities.popitem(last=False)
        return CreditAttribution("matched", trace.trace_id, trace.value, signal, credit, event.timestamp, message_id)


__all__ = [
    "CreditAttribution",
    "ELIGIBILITY_ACTIVITY_EVENT",
    "EligibilityActivity",
    "EligibilityCapacityError",
    "EligibilityLedger",
    "EligibilityTrace",
    "REWARD_EVENT",
    "RewardSignal",
]