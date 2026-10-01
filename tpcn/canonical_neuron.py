"""Minimal bounded event-driven neuron for the TPCN reference model."""

from __future__ import annotations

import math
from numbers import Real
from typing import Callable

from .event_runtime import Event, EventQueue, EventType, LocalClock, PropagationDelay


LocalActivity = tuple[str, float, float]
LocalActivityHook = Callable[[LocalActivity], None]
TemporalContextHook = Callable[[dict[str, float | str]], None]


def _nonnegative_real(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def _neuron_gain(value: Real) -> float:
    result = _nonnegative_real(value, "neuron_gain")
    if result > 2.0:
        raise ValueError("neuron_gain must be finite and within [0.0, 2.0]")
    return result


class TPCNNeuron:
    """A bounded, hardware-neutral neuron driven only by addressed events."""

    def __init__(
        self,
        neuron_id: str,
        *,
        state_limit: float = 1.0,
        decay_rate: float = 1.0,
        input_gain: float | None = None,
        neuron_gain: float | None = None,
        initial_state: float = 0.0,
        activity_hook: LocalActivityHook | None = None,
        temporal_context_hook: TemporalContextHook | None = None,
    ) -> None:
        if not isinstance(neuron_id, str) or not neuron_id:
            raise ValueError("neuron_id must be a non-empty string")
        state_limit = _nonnegative_real(state_limit, "state_limit")
        if state_limit == 0.0:
            raise ValueError("state_limit must be positive")
        decay_rate = _nonnegative_real(decay_rate, "decay_rate")
        if input_gain is None and neuron_gain is None:
            resolved_gain = 1.0
        elif input_gain is None:
            resolved_gain = _neuron_gain(neuron_gain)
        elif neuron_gain is None:
            resolved_gain = _neuron_gain(input_gain)
        else:
            legacy_gain = _neuron_gain(input_gain)
            canonical_gain = _neuron_gain(neuron_gain)
            if legacy_gain != canonical_gain:
                raise ValueError("input_gain and neuron_gain must agree when both are supplied")
            resolved_gain = canonical_gain
        if isinstance(initial_state, bool) or not isinstance(initial_state, Real):
            raise TypeError("initial_state must be a real number")
        initial_state = float(initial_state)
        if not math.isfinite(initial_state) or abs(initial_state) > state_limit:
            raise ValueError("initial_state must be finite and within state_limit")

        self.neuron_id = neuron_id
        self.state_limit = state_limit
        self.decay_rate = decay_rate
        self.neuron_gain = resolved_gain
        self.clock = LocalClock()
        self.state = initial_state
        self.activation = self._bounded_activation(self.state)
        self.prediction_state = 0.0
        self.prediction_error = 0.0
        self.eligibility_state = 0.0
        self.energy_state = 0.0
        self.processed_events = 0
        self._activity_hook = activity_hook
        self._temporal_context_hook = temporal_context_hook

    @property
    def input_gain(self) -> float:
        """Legacy read-only alias for the canonical neuron-owned gain."""
        return self.neuron_gain

    def _bounded_activation(self, state: float) -> float:
        return max(-1.0, min(1.0, math.tanh(state)))

    def _set_state(self, state: float) -> None:
        self.state = max(-self.state_limit, min(self.state_limit, state))
        self.activation = self._bounded_activation(self.state)

    def reset(self) -> None:
        """Reset character-local state while retaining this neuron's identity."""
        self.clock = LocalClock()
        self.state = 0.0
        self.activation = 0.0
        self.prediction_state = 0.0
        self.prediction_error = 0.0
        self.eligibility_state = 0.0
        self.energy_state = 0.0
        self.processed_events = 0

    def advance_state(self, dt: float) -> None:
        """Advance this neuron's local state by elapsed local time."""
        elapsed = _nonnegative_real(dt, "dt")
        self.clock.advance_to(self.clock.timestamp + elapsed)
        if elapsed:
            self._set_state(self.state * math.exp(-self.decay_rate * elapsed))

    def receive_event(self, event: Event) -> float:
        """Process one addressed numeric event and return the new activation."""
        if event.destination != self.neuron_id:
            raise ValueError("event destination does not address this neuron")
        if isinstance(event.payload, bool) or not isinstance(event.payload, Real):
            raise TypeError("neuron event payload must be a real number")
        pre_state = self.state
        elapsed = self.clock.advance_to(event.timestamp)
        if elapsed:
            self._set_state(self.state * math.exp(-self.decay_rate * elapsed))
        residual_state = self.state
        self._set_state(self.state + self.neuron_gain * float(event.payload))
        if self._temporal_context_hook is not None:
            self._temporal_context_hook({"neuron": self.neuron_id, "timestamp": event.timestamp,
                                         "delta_t": elapsed, "decay_rate": self.decay_rate,
                                         "pre_state": pre_state, "residual_state": residual_state,
                                         "post_state": self.state})
        self.processed_events += 1
        self.energy_state += abs(self.activation)
        self.eligibility_state = min(1.0, self.eligibility_state + abs(self.activation))
        if self._activity_hook is not None:
            self._activity_hook((self.neuron_id, event.timestamp, self.activation))
        return self.activation

    def emit_event(
        self,
        queue: EventQueue[Event],
        destination: str,
        *,
        event_type: EventType | str = EventType.SIGNAL,
        payload: float | None = None,
        delay: PropagationDelay = 0.0,
    ) -> Event:
        """Queue an output; the destination is never mutated inline."""
        output = self.activation if payload is None else payload
        if isinstance(output, bool) or not isinstance(output, Real):
            raise TypeError("emitted payload must be a real number")
        return queue.push_propagated(
            self.clock.timestamp,
            self.neuron_id,
            destination,
            event_type,
            float(output),
            delay,
        )


__all__ = ["LocalActivity", "LocalActivityHook", "TemporalContextHook", "TPCNNeuron"]