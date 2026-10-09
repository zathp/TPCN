"""Materialize only the frozen scalar matrix. Oracle never drives the model."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path

from .model import Retention


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def protocol():
    return json.loads(Path(__file__).with_name("protocol.json").read_text(encoding="utf-8"))


def materialize():
    p = protocol()
    instances = []
    for preload in p["preloads"]:
        for schedule in p["schedules"]:
            identity = schedule["id"] + "/" + preload["id"]
            local = Retention(preload["float"], schedule["initial_gate"])
            rows = []
            for n, (rational, t, kind, cue) in enumerate(schedule["events"]):
                if float(Fraction(rational)) != t:
                    raise ValueError("protocol rational/float identity mismatch")
                row = local.process(t, kind, cue)
                rows.append({
                    **row, "id": identity + f"/event/{n}",
                    "ordinal": n, "time_rational": rational,
                    "prior_time_rational": str(Fraction(row["prior_time"])),
                })
            if local.due is not None:
                row = local.process(64.0, "expiry")
                rows.append({
                    **row, "id": identity + "/due-expiry",
                    "ordinal": len(rows), "time_rational": "64",
                    "prior_time_rational": str(Fraction(row["prior_time"])),
                })
            instances.append({
                "id": identity, "schedule_id": schedule["id"], "preload": preload,
                "initial_gate": schedule["initial_gate"], "trace": rows,
                "generated_output_events": 0,  # disconnected by construction
                "final_status": local.status, "processed_events": local.count,
                "max_abs_state": max(abs(row[k]) for row in rows
                                     for k in ("prior_state", "pre_state", "post_state")
                                     if row[k] is not None),
            })
    if len(instances) != 33:
        raise ValueError("frozen population must be 33")
    return {"schema": "L63A-OUTCOME-1", "protocol_sha256": digest(p), "instances": instances}


if __name__ == "__main__":
    # Console-only raw outcome; publication/evaluation uses focused test CLI.
    print(canonical(materialize()).decode("utf-8"), end="")
