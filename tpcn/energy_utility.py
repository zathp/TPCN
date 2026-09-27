"""Bounded local activity accounting and explicit reward-adjusted utility.

Energy values are declared activity-cost proxy units, not calibrated joules.
The metering clock advances only when this local component observes activity or
is explicitly updated; it is not a neural timestep. Reward messages retain an
opaque credit identifier so Luna-8 can attribute delayed credit without
requiring Luna-5 to own eligibility policy.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real
from typing import Literal

from .event_runtime import Event, LocalClock
from .predictive_coding import PredictionError


def _finite(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _nonnegative(value: Real, name: str) -> float:
    result = _finite(value, name)
    if result < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return result


@dataclass(frozen=True, slots=True)
class EnergySnapshot:
    """Inspectible local meter state in declared proxy units."""

    energy: float
    activity: float
    counters: tuple[tuple[str, int], ...]
    timestamp: float
    idle_time: float
    unit: str


@dataclass(frozen=True, slots=True)
class RewardMessage:
    """A causally delivered local reward with an opaque attribution key."""

    credit_id: str
    reward: float
    timestamp: float

    def __post_init__(self) -> None:
        if not isinstance(self.credit_id, str) or not self.credit_id:
            raise ValueError("credit_id must be a non-empty string")
        object.__setattr__(self, "reward", _finite(self.reward, "reward"))
        object.__setattr__(self, "timestamp", _nonnegative(self.timestamp, "timestamp"))


@dataclass(frozen=True, slots=True)
class UsefulnessObservation:
    """A local usefulness signal kept separate from reward attribution."""

    activity_id: str
    usefulness: float
    timestamp: float

    def __post_init__(self) -> None:
        if not isinstance(self.activity_id, str) or not self.activity_id:
            raise ValueError("activity_id must be a non-empty string")
        object.__setattr__(self, "usefulness", _finite(self.usefulness, "usefulness"))
        object.__setattr__(self, "timestamp", _nonnegative(self.timestamp, "timestamp"))


@dataclass(frozen=True, slots=True)
class UtilityDecision:
    energy_cost: float
    reward: float
    utility: float
    retain: bool
    formula: str


class LocalEnergyModel:
    """Finite local activity meter with deterministic saturating overflow."""

    _KNOWN_COUNTERS = (
        "events_received",
        "events_emitted",
        "neuron_activations",
        "operator_activations",
        "state_changes",
        "connection_activity",
        "prediction_errors",
    )

    def __init__(
        self,
        meter_id: str,
        *,
        max_energy: float = 1_000_000.0,
        max_counter: int = 1_000_000,
        unit: str = "activity-cost-proxy",
    ) -> None:
        if not isinstance(meter_id, str) or not meter_id:
            raise ValueError("meter_id must be a non-empty string")
        max_energy = _nonnegative(max_energy, "max_energy")
        if max_energy == 0.0:
            raise ValueError("max_energy must be positive")
        if isinstance(max_counter, bool) or not isinstance(max_counter, int) or max_counter <= 0:
            raise ValueError("max_counter must be a positive integer")
        if not isinstance(unit, str) or not unit:
            raise ValueError("unit must be a non-empty string")
        self.meter_id = meter_id
        self.max_energy = max_energy
        self.max_counter = max_counter
        self.unit = unit
        self.clock = LocalClock()
        self.energy = 0.0
        self.activity = 0.0
        self.idle_time = 0.0
        self.last_update_elapsed = 0.0
        self._counters = {name: 0 for name in self._KNOWN_COUNTERS}

    def _advance_meter_time(self, timestamp: float) -> None:
        elapsed = self.clock.advance_to(timestamp)
        self.idle_time = min(self.max_energy, self.idle_time + elapsed)
        self.last_update_elapsed = elapsed

    def _increment(self, category: str, amount: int) -> None:
        self._counters[category] = min(self.max_counter, self._counters[category] + amount)

    def observe_activity(
        self,
        category: str,
        *,
        cost: float = 1.0,
        timestamp: float | None = None,
        count: int = 1,
    ) -> EnergySnapshot:
        """Record one local activity observation without updating other nodes."""
        if not isinstance(category, str) or not category:
            raise ValueError("category must be a non-empty string")
        if category not in self._counters:
            raise ValueError("category is not a declared local activity counter")
        cost = _nonnegative(cost, "cost")
        if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            raise ValueError("count must be a positive integer")
        current = self.clock.timestamp if timestamp is None else _nonnegative(timestamp, "timestamp")
        self._advance_meter_time(current)
        self.idle_time = 0.0
        increment = min(self.max_energy, cost * count)
        self.activity = min(self.max_energy, self.activity + increment)
        self.energy = min(self.max_energy, self.energy + increment)
        self._increment(category, count)
        return self.snapshot()

    def observe_event(self, event: Event, *, cost: float = 1.0) -> EnergySnapshot:
        """Account for one locally observed event; payload remains opaque."""
        return self.observe_activity("events_received", cost=cost, timestamp=event.timestamp)

    def observe_prediction_error(self, error: PredictionError, *, base_cost: float = 1.0) -> EnergySnapshot:
        """Account for a causal Luna-3 error using local error magnitude only."""
        return self.observe_activity(
            "prediction_errors",
            cost=base_cost + abs(error.error),
            timestamp=error.observation_timestamp,
        )

    def update(self, dt: float) -> EnergySnapshot:
        """Advance only this meter's measurement clock by an irregular interval."""
        elapsed = _nonnegative(dt, "dt")
        self._advance_meter_time(self.clock.timestamp + elapsed)
        return self.snapshot()

    def snapshot(self) -> EnergySnapshot:
        return EnergySnapshot(
            self.energy,
            self.activity,
            tuple(sorted(self._counters.items())),
            self.clock.timestamp,
            self.idle_time,
            self.unit,
        )


class RewardAdjustedUtility:
    """Explicit local utility evaluator; no formula is imposed by the core."""

    def __init__(
        self,
        *,
        formula: Literal["net", "ratio"] = "net",
        energy_weight: float = 1.0,
        epsilon: float = 1e-9,
        threshold: float = 0.0,
        max_messages: int = 1024,
        max_signal: float = 1_000_000.0,
    ) -> None:
        if formula not in ("net", "ratio"):
            raise ValueError("formula must be 'net' or 'ratio'")
        if isinstance(max_messages, bool) or not isinstance(max_messages, int) or max_messages <= 0:
            raise ValueError("max_messages must be a positive integer")
        max_signal = _nonnegative(max_signal, "max_signal")
        if max_signal == 0.0:
            raise ValueError("max_signal must be positive")
        self.formula = formula
        self.energy_weight = _nonnegative(energy_weight, "energy_weight")
        self.epsilon = _nonnegative(epsilon, "epsilon")
        self.threshold = _finite(threshold, "threshold")
        self.max_messages = max_messages
        self.max_signal = max_signal
        self.reward_total = 0.0
        self.usefulness_total = 0.0
        self.reward_messages = 0
        self.usefulness_messages = 0
        self.last_reward: RewardMessage | None = None
        self.last_usefulness: UsefulnessObservation | None = None

    def observe_reward(self, message: RewardMessage) -> None:
        """Consume one local/causal reward message without attributing credit."""
        if self.reward_messages >= self.max_messages:
            raise BufferError("reward message capacity reached")
        self.reward_messages += 1
        self.reward_total = max(-self.max_signal, min(self.max_signal, self.reward_total + message.reward))
        self.last_reward = message

    def observe_usefulness(self, observation: UsefulnessObservation) -> None:
        if self.usefulness_messages >= self.max_messages:
            raise BufferError("usefulness message capacity reached")
        self.usefulness_messages += 1
        self.usefulness_total = max(
            -self.max_signal,
            min(self.max_signal, self.usefulness_total + observation.usefulness),
        )
        self.last_usefulness = observation

    def evaluate(self, energy_cost: float, reward: float = 0.0) -> UtilityDecision:
        cost = _nonnegative(energy_cost, "energy_cost")
        reward = _finite(reward, "reward")
        if self.formula == "net":
            utility = reward - self.energy_weight * cost
        else:
            utility = reward / (cost + self.epsilon)
        return UtilityDecision(cost, reward, utility, cost > 0.0 and utility > self.threshold, self.formula)

    def evaluate_last_reward(self, energy_cost: float) -> UtilityDecision:
        reward = 0.0 if self.last_reward is None else self.last_reward.reward
        return self.evaluate(energy_cost, reward)


__all__ = [
    "EnergySnapshot",
    "LocalEnergyModel",
    "RewardAdjustedUtility",
    "RewardMessage",
    "UsefulnessObservation",
    "UtilityDecision",
]