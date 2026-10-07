"""Replay verified retained boundaries; never execute or modify production."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys

import run_luna46_depth_scaling_diagnostic as retained

ROOT = Path(__file__).resolve().parents[2]
BASE = "789dda5988daf72f375d9713bd76a6da2b9e8b34"
EVIDENCE_BASE = "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
BRANCH = "copilot/luna47b-investigation"
RETAINED = Path("artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json")
MODULE = Path("experiments/luna47b/diagnostic.py")
PROTOCOL = Path("experiments/luna47b/PROTOCOL.md")
EXPECTED_COUNTS = {"NO-RECEPTIONS": 212, "DRIVE-LIMITED": 75,
                   "TEMPORAL-RETENTION-LIMITED": 33}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT)


def ensure(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError("BLOCKED: " + reason)


def finite(value: float) -> float:
    ensure(math.isfinite(value), "nonfinite numerical value")
    return value


def close(observed: float, expected: float) -> dict:
    bound = 64 * sys.float_info.epsilon * max(1, abs(observed), abs(expected))
    residual = abs(observed - expected)
    ensure(residual <= bound, "recurrence mismatch")
    return {"observed": observed, "expected": expected,
            "residual": residual, "bound": bound}


def boundaries(sequence: dict) -> list[dict]:
    inputs = {r["queue_sequence"]: r["payload"] for r in sequence["recurrence_evidence"]}
    rows = []
    previous_time = None
    for row in sequence["all_update_boundaries"]:
        ensure(previous_time is None or row["prior_clock"] == previous_time,
               "missing intervening update")
        dt = finite(row["timestamp"] - row["prior_clock"])
        ensure(dt >= 0 and dt == row["dt"], "retained elapsed time differs")
        rho = math.exp(-0.0125 * dt)
        ensure(rho == row["rho"], "retention coefficient differs")
        rows.append({**row, "input": finite(inputs[row["queue_sequence"]])
                     if row["is_reception"] else 0.0})
        previous_time = row["timestamp"]
    ensure(len(rows) <= 512, "sequence update budget exceeded")
    return rows


def derive(rows: list[dict]) -> dict:
    state = 0.0
    states = []
    for row in rows:
        state = finite(row["rho"] * state + row["input"])
        close(row["state_after"], state)
        ensure((abs(state) >= 1) == (abs(row["state_after"]) >= 1),
               "baseline threshold classification mismatch")
        states.append(state)
    maximum = max([0.0, *map(abs, states)])
    return {"states": states, "maximum_abs_unit_gain": maximum,
            "critical_gain": None if maximum == 0 else finite(1.0 / maximum),
            "status": "NO-CROSSING: ZERO RESPONSE" if maximum == 0 else "FINITE"}


def trajectory(rows: list[dict], gain: float) -> dict:
    ensure(math.isfinite(gain) and 0 <= gain <= 1e6, "gain outside declared domain")
    state = 0.0
    first = None
    events = []
    saturations = 0
    cancelled = 0.0
    sign_reversals = 0
    for row in rows:
        event = {k: row[k] for k in ("event_id", "queue_sequence", "timestamp",
                                    "prior_clock", "dt", "rho", "is_reception", "input")}
        deposit = finite(gain * row["input"])
        event["deposit"] = deposit
        if first is not None:
            event.update(censored=True, state_before=None, state_decayed=None,
                         state_unclipped=None, state_input=None, crossed=None)
        else:
            before = state
            pre = finite(row["rho"] * before)
            raw = finite(pre + deposit)
            state = max(-4.0, min(4.0, raw))
            saturated = state != raw
            saturations += saturated
            opposing = pre * deposit < 0
            loss = min(abs(pre), abs(deposit)) if opposing else 0.0
            cancelled += loss
            sign_reversals += opposing and pre * state < 0
            crossing = abs(state) >= 1.0
            event.update(censored=False, state_before=before, state_decayed=pre,
                         state_unclipped=raw, state_input=state, crossed=crossing,
                         saturated=saturated, cancelled_magnitude=loss,
                         opposing=opposing)
            if crossing:
                first = {**event}
        events.append(event)
    return {"gain": gain, "crosses": first is not None, "first_crossing": first,
            "events": events, "saturations": saturations,
            "cancelled_magnitude_before_stop": cancelled,
            "sign_reversals_before_stop": sign_reversals,
            "maximum_abs_evaluated_state": max([0.0, *[abs(e["state_input"])
                for e in events if not e["censored"]]])}


def reconstruct() -> tuple[dict, dict]:
    # Reuse reviewed read-only integrity/reconciliation routines, not its CLI
    # (which intentionally enforces the historical Luna-46 branch).
    ensure((ROOT / RETAINED).read_bytes() == git("show", f"{EVIDENCE_BASE}:{RETAINED.as_posix()}"),
           "retained corrected artifact changed")
    for path in ("run_luna46_depth_scaling_diagnostic.py",):
        ensure((ROOT / path).read_bytes().replace(b"\r\n", b"\n")
               == git("show", f"{BASE}:{path}"),
               "reviewed analyzer changed")
    integrity = retained.verify_integrity(ROOT)
    document = json.loads((ROOT / RETAINED).read_bytes())
    ensure(retained.digest({k: v for k, v in document.items() if k != "output_digest"})
           == document["output_digest"], "corrected output internal digest differs")
    ensure(document["verdict"] == "MIXED", "retained verdict differs")
    load = lambda path: json.loads((ROOT / path).read_bytes())
    config = load(retained.L45 / "config.json")["experiment"]
    retained.validate_config(config, load(retained.L44 / "config.json")["experiment"])
    summary = load(retained.L45 / "summary.json")
    for arm in ("DESTINATION_DISABLED", "DESTINATION_DEFAULT", retained.CALIBRATED):
        retained.verify_phase_pair(load(retained.L45 / f"initial-{arm.lower()}.json"),
                                   load(retained.L45 / f"replay-{arm.lower()}.json"),
                                   config, summary, arm)
    phases = {}
    for phase in ("initial", "replay"):
        records = load(retained.L45 / f"{phase}-destination_calibrated.json")["records"]
        enqueues = retained.select_raw(load(retained.L45 / f"{phase}-destination_calibrated-enqueue.json"),
                                       records, phase, "enqueue", retained.CALIBRATED)
        receptions = retained.select_raw(load(retained.L45 / f"{phase}-destination_calibrated-reception.json"),
                                         records, phase, "reception", retained.CALIBRATED)
        results = []
        for record, queued, received in zip(records, enqueues, receptions):
            hop = lambda rows: [r for r in rows if r["source"] == "relay"
                                and r["destination"] == "destination"]
            arrivals = retained.reconcile(hop(queued), hop(received), "relay", "destination")
            results.append(retained.analyze_sequence(record["stream_id"], arrivals,
                           retained.destination_updates(record, arrivals)))
        ensure(results == document["sequences"], "exact reconstructed retained sequences differ")
        phases[phase] = retained.digest(results)
    ensure(phases["initial"] == phases["replay"], "retained replay differs")
    ensure(dict(Counter(s["category"] for s in document["sequences"])) == EXPECTED_COUNTS,
           "retained category partition differs")
    return document, {"integrity": integrity, "phase_digests": phases,
                      "retained_sha256": retained.sha((ROOT / RETAINED).read_bytes()),
                      "configuration_digest": retained.digest(config)}


def analyze(document: dict) -> dict:
    # Complete analytical derivation before selecting any tested gain.
    prepared = [(s, boundaries(s)) for s in document["sequences"]]
    derived = [derive(rows) for _, rows in prepared]
    criticals = sorted(d["critical_gain"] for d in derived if d["critical_gain"] is not None)
    ensure(bool(criticals), "empty applicable population")
    anchors = [min(criticals), statistics.median(criticals), max(criticals)]
    gains = sorted({1.0, *(factor * a for a in anchors for factor in (0.99, 1.01))})
    ensure(len(gains) <= 7 and max(gains) <= 1e6, "global gain budget exceeded")
    sequences = []
    for (sequence, rows), calculated in zip(prepared, derived):
        arms = [trajectory(rows, gain) for gain in gains]
        local = []
        critical = calculated["critical_gain"]
        if critical is not None:
            local = [trajectory(rows, critical * factor) for factor in (0.99, 1.01)]
            ensure(not local[0]["crosses"] and local[1]["crosses"],
                   "analytical critical bracket failed")
        sequences.append({"stream_id": sequence["stream_id"], "category": sequence["category"],
                          "receptions": sequence["receptions"], "retained_boundaries": rows,
                          "derivation": calculated, "global_arms": arms, "local_brackets": local})
    summaries = []
    for i, gain in enumerate(gains):
        target = [s for s in sequences if s["category"] == "DRIVE-LIMITED"]
        other = [s for s in sequences if s["category"] != "DRIVE-LIMITED"]
        rescued = sum(s["global_arms"][i]["crosses"] for s in target)
        unintended = sum(s["global_arms"][i]["crosses"] for s in other)
        arms = [s["global_arms"][i] for s in sequences]
        summaries.append({"gain": gain, "rescued": rescued, "target_denominator": len(target),
                          "rescued_fraction": rescued / len(target),
                          "unintended_crossings": unintended, "non_target_denominator": len(other),
                          "non_target_fraction": unintended / len(other),
                          "other_reception_denominator": 33,
                          "other_reception_fraction": unintended / 33,
                          "saturations": sum(a["saturations"] for a in arms),
                          "maximum_abs_evaluated_state": max(a["maximum_abs_evaluated_state"] for a in arms),
                          "cancelled_magnitude_before_stop": sum(a["cancelled_magnitude_before_stop"] for a in arms),
                          "sign_reversals_before_stop": sum(a["sign_reversals_before_stop"] for a in arms)})
    best = max(s["rescued"] for s in summaries)
    verdict = ("SUPPORTED" if best == 75 else "PARTIALLY SUPPORTED" if best else "NOT SUPPORTED")
    return {"critical_anchors": anchors, "global_gains": gains, "sequences": sequences,
            "summaries": summaries, "verdict": verdict, "retained_verdict": "MIXED",
            "target_critical_range": [min(s["derivation"]["critical_gain"] for s in sequences
                                        if s["category"] == "DRIVE-LIMITED"),
                                    max(s["derivation"]["critical_gain"] for s in sequences
                                        if s["category"] == "DRIVE-LIMITED")]}


def run(replay_revision: str | None = None) -> dict:
    ensure(git("branch", "--show-current").decode().strip() == BRANCH, "branch differs")
    current = git("rev-parse", "HEAD").decode().strip()
    revision = replay_revision or current
    git("merge-base", "--is-ancestor", revision, current)
    git("merge-base", "--is-ancestor", BASE, revision)
    ensure(not git("status", "--porcelain"), "execution requires clean committed worktree")
    source_hashes = {}
    for path in (MODULE, PROTOCOL):
        data = (ROOT / path).read_bytes()
        committed = git("show", f"{revision}:{path.as_posix()}")
        ensure(data.replace(b"\r\n", b"\n") == committed, "protocol/code not committed")
        source_hashes[path.as_posix()] = {
            "worktree_sha256": retained.sha(data),
            "committed_sha256": retained.sha(committed),
            "comparison": "CRLF-to-LF text materialization only; evidence bytes never normalized"}
    document, provenance = reconstruct()
    result = analyze(document)
    replay = analyze(document)
    ensure(retained.canonical(result) == retained.canonical(replay), "gain replay bytes differ")
    output = {"schema": "TPCN-LUNA47B-GAIN-1", "authorization_revision": BASE,
              "production_evidence_revision": EVIDENCE_BASE, "execution_revision": revision,
              "source_hashes": source_hashes, "provenance": provenance,
              "environment": {"python": sys.version, "platform": sys.platform},
              "replay": {"equal": True, "initial_digest": retained.digest(result),
                         "replay_digest": retained.digest(replay)},
              "protocol": (ROOT / PROTOCOL).read_text(encoding="utf-8"),
              "result": result}
    output["output_digest"] = retained.digest(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    path = ROOT / "artifacts/luna47b/results.json"
    revision = json.loads(path.read_bytes())["execution_revision"] if args.replay else None
    output = run(revision)
    data = retained.canonical(output) + b"\n"
    if args.replay:
        ensure(path.read_bytes() == data, "published replay artifact differs")
    else:
        ensure(not path.exists(), "refusing to overwrite retained lane output")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(json.dumps({"verdict": output["result"]["verdict"],
                      "summaries": output["result"]["summaries"],
                      "target_critical_range": output["result"]["target_critical_range"],
                      "sha256": retained.sha(data)}, indent=2))


if __name__ == "__main__":
    main()
