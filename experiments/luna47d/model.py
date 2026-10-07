"""Isolated L47D synthetic charge-drain output model; no TPCN imports."""
from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class Config:
    theta: float = 1.0
    quantum: float = 4.0
    leak: float = 0.125
    period: str = "1/2"
    epsilon: float = 1e-6
    tail: str = "144"

    def validate(self):
        numbers = (self.theta, self.quantum, self.leak, self.epsilon)
        if not all(math.isfinite(x) for x in numbers):
            raise ValueError("nonfinite configuration")
        if not (0.5 <= self.theta <= 2 and self.theta <= self.quantum <= 8):
            raise ValueError("threshold/drain domain")
        if not (0 < self.leak <= 1 and 0 < self.epsilon <= 1e-3):
            raise ValueError("positive dissipative leak/neutral tolerance required")
        if not Fraction(1, 8) <= Fraction(self.period) <= 1:
            raise ValueError("strict-future period domain")
        if float(Fraction(self.tail)) < math.log(32 / self.epsilon) / self.leak:
            raise ValueError("recovery horizon insufficient")


def load_fixtures():
    data = json.loads(Path(__file__).with_name("fixtures.json").read_text())
    if data["schema"] != "L47D-FIXTURE-1":
        raise ValueError("fixture schema")
    fixtures = []
    for family in data["families"]:
        for sign, suffix in ((1, "positive"), (-1, "negative")):
            identity = f'{family["id"]}/{suffix}'
            fixtures.append({
                "id": identity, "family": family["id"], "polarity": sign,
                "expected_count": family["expected_count"],
                "inputs": [{"id": f"{identity}/{i}", "time": t, "drive": sign * x}
                           for i, t, x in family["events"]],
            })
    return fixtures


def validate_fixture(fixture):
    events = fixture["inputs"]
    if len(events) > 16 or len({e["id"] for e in events}) != len(events):
        raise ValueError("input capacity/duplicate identity")
    times = [Fraction(e["time"]) for e in events]
    if times != sorted(times) or any(t < 0 or t > 64 for t in times):
        raise ValueError("late/out-of-range input time")
    if not all(math.isfinite(e["drive"]) for e in events):
        raise ValueError("nonfinite drive")
    if sum(abs(e["drive"]) for e in events) > 32:
        raise ValueError("absolute drive budget exceeded")


def simulate(fixture, config=Config()):
    config.validate()
    validate_fixture(fixture)
    inputs = fixture["inputs"]
    q, last, index, due, opportunity = 0.0, Fraction(0), 0, None, 0
    outputs, trace, contributors = [], [], []
    identity = fixture["id"]
    period = Fraction(config.period)
    last_input = Fraction(inputs[-1]["time"]) if inputs else Fraction(0)
    horizon = last_input + Fraction(config.tail)

    def evolve(t):
        return q * math.exp(-config.leak * float(t - last))

    def append(kind, event_id, t, pre, post, decision, output_id=None):
        trace.append({"kind": kind, "id": event_id, "time": str(t),
                      "previous_time": str(last), "previous_state": q,
                      "pre": pre, "post": post, "decision": decision,
                      "output_id": output_id,
                      "pending_time": None if due is None else str(due)})

    # At most one locally scheduled opportunity; no common timestep loop.
    while index < len(inputs) or due is not None:
        next_input = Fraction(inputs[index]["time"]) if index < len(inputs) else None
        if next_input is not None and (due is None or next_input <= due):
            e = inputs[index]
            t, pre = next_input, evolve(next_input)
            post = pre + e["drive"]
            contributors.append(e["id"])
            if due is None and abs(post) >= config.theta:
                due = t + period
            append("input", e["id"], t, pre, post, "drive-admitted")
            index += 1
        else:
            t, pre = due, evolve(due)
            opportunity += 1
            if opportunity > 128:
                raise RuntimeError("opportunity watchdog; no truncation permitted")
            due, post, out_id = None, pre, None
            decision = "below-threshold-no-output"
            if abs(pre) >= config.theta:
                out_id = f"{identity}/out/{len(outputs)}"
                outputs.append({"id": out_id, "time": str(t),
                                "sign": 1 if pre > 0 else -1,
                                "contributors": list(contributors),
                                "opportunity_id": f"{identity}/due/{opportunity - 1}"})
                post = math.copysign(max(0.0, abs(pre) - config.quantum), pre)
                # Canonical unsigned zero prevents mirrored JSON -0.0 residue.
                post = 0.0 if post == 0 else post
                decision = "emitted-and-drained"
                if abs(post) >= config.theta:
                    due = t + period
            append("opportunity", f"{identity}/due/{opportunity - 1}",
                   t, pre, post, decision, out_id)
        if not math.isfinite(post) or abs(post) > 32:
            raise RuntimeError("unbounded state")
        if len(outputs) > math.floor(32 / config.theta):
            raise RuntimeError("output budget exceeded; no truncation permitted")
        q, last = post, t
        if q == 0:
            contributors.clear()
    pre = evolve(horizon)
    append("observation", f"{identity}/horizon", horizon, pre, pre, "passive-observation")

    # After final excitation, |q| is monotone; find its first epsilon crossing
    # in the exact event-boundary segments (the analytic metric is not an event).
    recovery = 0.0 if not inputs else None
    for n, row in enumerate(trace):
        if recovery is not None:
            break
        if Fraction(row["time"]) < last_input:
            continue
        # Same-time rows must all be processed before declaring recovery.
        if n + 1 < len(trace) and trace[n + 1]["time"] == row["time"]:
            continue
        t = float(Fraction(row["time"]))
        state = abs(row["post"])
        crossing = t if state <= config.epsilon else t + math.log(state / config.epsilon) / config.leak
        end = float(Fraction(trace[n + 1]["time"])) if n + 1 < len(trace) else float(horizon)
        if crossing <= end:
            recovery = crossing
            break

    times = [Fraction(o["time"]) for o in outputs]
    mapping = [{
        "input_id": e["id"], "input_time": e["time"], "trace_id": e["id"],
        "output_ids": [o["id"] for o in outputs if e["id"] in o["contributors"]],
        "disposition": "participated-in-output" if any(e["id"] in o["contributors"] for o in outputs)
        else "admitted-no-associated-output",
    } for e in inputs]
    return {
        "trajectory": fixture, "fixture_sha256": digest(fixture),
        "configuration": asdict(config), "outputs": outputs, "trace": trace,
        "reconciliation": mapping,
        "metrics": {
            "output_count": len(outputs), "opportunity_count": opportunity,
            "first_latency": str(times[0] - Fraction(inputs[0]["time"])) if times else None,
            "spacings": [str(b - a) for a, b in zip(times, times[1:])],
            "max_abs_state": max((abs(r[k]) for r in trace for k in ("pre", "post")), default=0),
            "final_abs_state": abs(pre), "last_input_time": str(last_input),
            "horizon_time": str(horizon), "recovery_time": recovery,
            "recovery_delay": None if recovery is None else recovery - float(last_input),
            "exact_zero_final": pre == 0,
            "state_bound": 32, "output_bound": math.floor(32 / config.theta),
            "pending_at_horizon": None,
        },
    }


def scientific_failures(result):
    """Independent acceptance predicates; exact replay is a separate gate."""
    fixture, metrics = result["trajectory"], result["metrics"]
    config = Config(**result["configuration"])
    outputs, trace = result["outputs"], result["trace"]
    failures = []
    if len(outputs) != fixture["expected_count"] or metrics["output_count"] != len(outputs):
        failures.append("count/compression-regime")
    if metrics["max_abs_state"] > 32 or any(
        not math.isfinite(r[k]) or abs(r[k]) > 32 for r in trace for k in ("pre", "post")
    ):
        failures.append("unbounded-state")
    if len(outputs) > math.floor(32 / config.theta):
        failures.append("unbounded-output-count")
    if (metrics["recovery_delay"] is None or metrics["recovery_delay"] > float(Fraction(config.tail))
            or metrics["final_abs_state"] > config.epsilon
            or abs(trace[-1]["post"]) > config.epsilon or metrics["pending_at_horizon"] is not None):
        failures.append("loss-of-bounded-neutral-recovery")
    if outputs:
        if Fraction(metrics["first_latency"]) != Fraction(config.period):
            failures.append("latency")
        if any(Fraction(b["time"]) - Fraction(a["time"]) < Fraction(config.period)
               for a, b in zip(outputs, outputs[1:])):
            failures.append("spacing")
        recovery = metrics["recovery_time"]
        if recovery is not None and any(float(Fraction(o["time"])) > recovery for o in outputs):
            failures.append("output-after-neutral/self-sustaining")
    if len({o["id"] for o in outputs}) != len(outputs):
        failures.append("duplicate-output-identity")
    input_rows = [r for r in trace if r["kind"] == "input"]
    if [(r["id"], r["time"]) for r in input_rows] != [
        (e["id"], str(Fraction(e["time"]))) for e in fixture["inputs"]
    ]:
        failures.append("input-identity-reconciliation")
    emitted = [r for r in trace if r["output_id"] is not None]
    if [(r["output_id"], r["time"]) for r in emitted] != [(o["id"], o["time"]) for o in outputs]:
        failures.append("output-identity-reconciliation")
    return failures


def reconcile(result):
    """Every identity, timestamp, state, mapping and metric must replay exactly."""
    expected = simulate(result["trajectory"], Config(**result["configuration"]))
    if canonical(result) != canonical(expected):
        raise ValueError("identity/state/metric replay mismatch")
    return True
