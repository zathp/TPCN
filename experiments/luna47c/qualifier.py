"""Label-free, bounded, causal input qualification, not excitation integration."""
from dataclasses import asdict, dataclass
import math


METHODS = ("fixed", "adaptive", "robust")


@dataclass(frozen=True)
class Config:
    method: str
    initial_noise: float = 0.25
    multiplier: float = 2.0
    baseline_tau: float = 20.0
    noise_tau: float = 4.0
    baseline_clip: float = 0.25
    robust_clip_multiple: float = 2.0
    noise_floor: float = 0.05
    input_bound: float = 16.0
    baseline_bound: float = 4.0

    def __post_init__(self):
        if self.method not in METHODS:
            raise ValueError("unknown method")
        for name, value in asdict(self).items():
            if name != "method" and (not math.isfinite(value) or value <= 0):
                raise ValueError("parameters must be finite and positive")
        if not self.noise_floor <= self.initial_noise <= self.input_bound:
            raise ValueError("invalid initial noise")
        if self.baseline_bound > self.input_bound:
            raise ValueError("invalid baseline bound")


class Qualifier:
    """Three scalar state slots; no samples, labels, counters or global state."""
    __slots__ = ("config", "baseline", "noise", "last_time")

    def __init__(self, config: Config):
        self.config = config
        self.reset()

    def reset(self):
        self.baseline = 0.0
        self.noise = self.config.initial_noise
        self.last_time = None

    def process(self, timestamp: float, raw: float) -> dict:
        c = self.config
        if not math.isfinite(timestamp) or timestamp < 0:
            raise ValueError("invalid timestamp")
        if not math.isfinite(raw) or abs(raw) > c.input_bound:
            raise ValueError("input outside finite bound")
        if self.last_time is not None and timestamp <= self.last_time:
            raise ValueError("timestamps must strictly increase")
        dt = 1.0 if self.last_time is None else timestamp - self.last_time
        b, n = self.baseline, self.noise
        residual = raw - b
        band = c.multiplier * n
        excess = math.copysign(max(abs(residual) - band, 0.0), residual)
        # All methods share clipped baseline tracking to isolate noise policy.
        alpha_b = -math.expm1(-dt / c.baseline_tau)
        step = max(-c.baseline_clip, min(c.baseline_clip, residual))
        self.baseline = max(-c.baseline_bound, min(c.baseline_bound, b + alpha_b * step))
        if c.method != "fixed":
            target = abs(residual)
            if c.method == "robust":
                target = min(target, c.robust_clip_multiple * n)
            alpha_n = -math.expm1(-dt / c.noise_tau)
            self.noise = max(c.noise_floor, min(c.input_bound, n + alpha_n * (target - n)))
        self.last_time = timestamp
        return {"timestamp": timestamp, "raw": raw, "B": b, "N": n,
                "band": band, "E": excess, "B_after": self.baseline,
                "N_after": self.noise, "dt": dt}
