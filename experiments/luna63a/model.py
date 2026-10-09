"""One local scalar with binary leak gate and terminal bounded lifetime."""

import math
from numbers import Real

LAMBDA_0 = 0.125
Z_MAX = 4.0
TTL = 64.0
MAX_EVENTS = 32


class ModelFault(ValueError):
    """Visible fail-lock; state is never cleared into apparent success."""


def binary(value):
    if type(value) is not int or value not in (0, 1):
        raise ModelFault("gate must be integer 0 or 1, not bool")
    return value


def finite(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ModelFault(f"{name} must be a real non-bool number")
    result = float(value)
    if not math.isfinite(result):
        raise ModelFault(f"{name} must be finite")
    return result


class Retention:
    """No preload/reset/output API after fresh initialization; no reuse."""

    __slots__ = ("z", "last_time", "R", "status", "count", "due", "reason")

    def __init__(self, preload, gate):
        z = finite(preload, "preload")
        if abs(z) > Z_MAX:
            raise ModelFault("preload exceeds magnitude bound 4")
        self.R = binary(gate)
        self.z = z
        self.last_time = 0.0
        self.status = "ACTIVE"
        self.count = 0
        self.due = TTL
        self.reason = None

    def _fault(self, reason):
        self.status = "FAULT"
        self.reason = reason
        self.due = None
        raise ModelFault(reason)

    def _settle(self, t):
        # The ONLY ordinary z write: prior gate, not the incoming cue.
        dt = t - self.last_time
        if self.R == 1 and dt != 0.0:
            self.z = self.z * math.exp(-LAMBDA_0 * dt)
        # HOLD and dt=0 preserve binary64 bits exactly.
        self.last_time = t

    def _set_gate(self, gate):
        # Cue carries only a binary leak choice; no scalar/output writes.
        self.R = gate

    def process(self, t, kind="observation", gate=None):
        """Insertion order is caller order. Due expiry can be preempted by cue."""
        if self.status == "FAULT":
            raise ModelFault(self.reason)
        try:
            t = finite(t, "timestamp")
        except ModelFault as exc:
            self._fault(str(exc))
        if not 0.0 <= t <= 65.0 or t < self.last_time:
            self._fault("timestamp outside [0,65] or late")
        if kind not in ("observation", "cue", "expiry"):
            self._fault("invalid event kind")
        if kind == "expiry" and (t != TTL or gate is not None):
            self._fault("due expiry must occur at 64 without payload")
        if kind == "observation" and gate is not None:
            self._fault("observation accepts no payload")
        if self.count >= MAX_EVENTS:
            self._fault("event budget 32 exhausted; no truncation")
        prior = {
            "prior_gate": self.R, "prior_time": self.last_time,
            "prior_state": self.z, "prior_status": self.status,
            "prior_due": self.due,
        }
        self.count += 1
        retained = self.z
        action, rejection = "observation", None
        if self.status == "EXPIRED":
            action = "terminal-report"
            rejection = "terminal-no-revival" if kind == "cue" else None
        elif t >= TTL:
            # Equality check occurs before cue validation/application.
            self.z = None  # only permitted post-init direct clear
            self.last_time = TTL
            self.status = "EXPIRED"
            self.reason = "absolute-TTL-equality-or-later"
            self.due = None
            action = "expiry"
            rejection = "expiry-preempts-cue" if kind == "cue" else None
        else:
            if kind == "cue":
                try:
                    binary(gate)
                except ModelFault as exc:
                    self._fault(str(exc))
            self._settle(t)
            retained = self.z
            if kind == "cue":
                self._set_gate(gate)
                action = "gate-applied"
            if not math.isfinite(self.z) or abs(self.z) > Z_MAX:
                self._fault("state bound violated")
        return {
            **prior, "time_float": t, "kind": kind, "cue": gate,
            "dt": t - prior["prior_time"], "pre_state": retained,
            "post_state": self.z, "post_gate": self.R,
            "last_time": self.last_time, "status": self.status,
            "due": self.due, "event_count": self.count,
            "action": action, "rejection": rejection, "reason": self.reason,
        }
