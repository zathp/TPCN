"""Frozen synthetic generation and evaluator-only truth; never imported by mechanism."""
from dataclasses import asdict, dataclass
import hashlib
import json


def canonical(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class Fixture:
    identity: str
    family: str
    orientation: int
    inputs: tuple
    baseline_truth: tuple
    noise_truth: tuple
    signal_truth: tuple

    def serialized(self) -> dict:
        return asdict(self)


FAMILIES = ("stationary", "drift", "isolated", "clustered", "mixed_signs",
            "near_boundary", "contamination_chain", "noise_step")
NOISE = (-0.2, 0.1, -0.1, 0.2, 0.0, 0.15, -0.15, 0.0)
INTERVALS = (1.0, 0.5, 1.5, 0.75)
SAMPLES = 240


def fixtures() -> tuple:
    result = []
    for family in FAMILIES:
        baseline, noise, signal, times = [], [], [], []
        timestamp = 0.0
        for i in range(SAMPLES):
            timestamp += INTERVALS[i % len(INTERVALS)]
            times.append(timestamp)
            b = 0.8 * max(0, min(i - 40, 120)) / 120 if family == "drift" else 0.0
            n = NOISE[i % len(NOISE)]
            s = 0.0
            if family == "isolated" and i in (60, 120, 180):
                s = 8.0 if i != 120 else -8.0
            if family == "clustered" and (60 <= i < 68 or 140 <= i < 148):
                s = 1.2 if i < 100 else -1.2
            if family == "mixed_signs" and 60 <= i < 80:
                s = 1.2 if i % 2 == 0 else -1.2
            if family == "near_boundary" and i in (60, 80, 100, 120, 140, 160):
                # Meaning is defined by the injected source, not admission.
                s = (0.49, 0.50, 0.51, -0.49, -0.50, -0.51)[(i - 60) // 20]
                n = 0.0
            if family == "contamination_chain":
                n = 0.0
                if i == 60:
                    s = 8.0
                elif i in (61, 62, 64, 68):
                    s = 0.9
            if family == "noise_step" and 60 <= i < 160:
                n *= 4.0
            baseline.append(b)
            noise.append(n)
            signal.append(s)
        for orientation in (1, -1):
            result.append(Fixture(
                f"{family}:{orientation:+d}", family, orientation,
                tuple((t, orientation * (b + n + s))
                      for t, b, n, s in zip(times, baseline, noise, signal)),
                tuple(orientation * x for x in baseline),
                tuple(orientation * x for x in noise),
                tuple(orientation * x for x in signal)))
    return tuple(result)
