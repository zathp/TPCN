"""Replay verified retained boundaries; never execute or modify production."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys
from types import ModuleType
from unittest.mock import patch

import run_luna46_depth_scaling_diagnostic as retained

ROOT = Path(__file__).resolve().parents[2]
BASE = "789dda5988daf72f375d9713bd76a6da2b9e8b34"
EVIDENCE_BASE = "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
HISTORICAL_EXECUTION_REVISION = "38891b81754ce385c55f96e4020e2bf04c2b9a5d"
HISTORICAL_ANALYZER_BLOB = "08f217daec167b2abc82f5988dba660c19f4ae0e"
CURRENT_ANALYZER_REVISION = "e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e"
CURRENT_ANALYZER_BLOB = "59d24b08ffa0a2a9a1ebe03a35ae595fb646fcd4"
ANALYZER_PATH = "run_luna46_depth_scaling_diagnostic.py"
BRANCH = "copilot/luna47b-investigation"
RETAINED = Path("artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json")
LUNA47B_RESULT = Path("artifacts/luna47b/results.json")
LUNA47B_VALIDATION = Path("artifacts/luna47b/validation.json")
LUNA47B_RESULT_SHA256 = "b120d2cc5718649fb0d57d93611ddb89b45113e79c0d3003cf330fe092d0fb83"
LUNA47B_VALIDATION_SHA256 = "1ef630d88e4699e9bcc1e5d05e2cc868f12f38a3958f8f1a065a4132df628fe0"
MODULE = Path("experiments/luna47b/diagnostic.py")
PROTOCOL = Path("experiments/luna47b/PROTOCOL.md")
EXPECTED_COUNTS = {"NO-RECEPTIONS": 212, "DRIVE-LIMITED": 75,
                   "TEMPORAL-RETENTION-LIMITED": 33}


def git(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.check_output(["git", "--no-pager", *args], cwd=root)


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


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def verify_historical_lane_metadata(root: Path = ROOT) -> dict:
    result_bytes = (root / LUNA47B_RESULT).read_bytes()
    validation_bytes = (root / LUNA47B_VALIDATION).read_bytes()
    ensure(retained.sha(result_bytes) == LUNA47B_RESULT_SHA256,
           "retained Luna-47B result identity differs")
    ensure(retained.sha(validation_bytes) == LUNA47B_VALIDATION_SHA256,
           "retained Luna-47B validation identity differs")

    result = json.loads(result_bytes)
    ensure(result.get("execution_revision") == HISTORICAL_EXECUTION_REVISION,
           "retained Luna-47B execution revision differs")
    source_hashes = result.get("source_hashes")
    ensure(isinstance(source_hashes, dict), "retained Luna-47B source identities missing")
    try:
        historical_module = git(
            "show", f"{HISTORICAL_EXECUTION_REVISION}:{ANALYZER_PATH}", root=root
        )
        historical_protocol = git(
            "show", f"{HISTORICAL_EXECUTION_REVISION}:{PROTOCOL.as_posix()}", root=root
        )
    except subprocess.CalledProcessError as error:
        raise ValueError("BLOCKED: retained Luna-47B source object unavailable") from error

    ensure(
        git_blob_sha(historical_module) == HISTORICAL_ANALYZER_BLOB,
        "retained Luna-47B historical analyzer object differs",
    )
    recorded_protocol = source_hashes.get(PROTOCOL.as_posix(), {})
    ensure(
        recorded_protocol.get("committed_sha256") == retained.sha(historical_protocol),
        "retained Luna-47B protocol execution identity differs",
    )
    working_protocol = (root / PROTOCOL).read_bytes()
    ensure(
        working_protocol == historical_protocol
        or working_protocol == historical_protocol.replace(b"\n", b"\r\n"),
        "Luna-47B protocol checkout differs beyond Git newline materialization",
    )
    ensure(
        result.get("protocol") == historical_protocol.decode("utf-8"),
        "retained Luna-47B protocol content differs",
    )
    return {
        "execution_revision": result["execution_revision"],
        "historical_analyzer_sha256": retained.sha(historical_module),
        "historical_protocol_sha256": retained.sha(historical_protocol),
        "retained_result_sha256": retained.sha(result_bytes),
        "retained_validation_sha256": retained.sha(validation_bytes),
    }


def load_historical_analyzer(
    root: Path = ROOT,
    *,
    historical_revision: str = BASE,
    historical_blob: str = HISTORICAL_ANALYZER_BLOB,
    execution_revision: str = HISTORICAL_EXECUTION_REVISION,
    current_revision: str = CURRENT_ANALYZER_REVISION,
    current_blob: str = CURRENT_ANALYZER_BLOB,
) -> tuple[ModuleType, dict]:
    ensure(historical_revision == BASE, "historical analyzer revision differs")
    ensure(execution_revision == HISTORICAL_EXECUTION_REVISION,
           "historical analyzer execution revision differs")
    ensure(historical_blob == HISTORICAL_ANALYZER_BLOB,
           "historical analyzer Git object pin differs")
    ensure(current_revision == CURRENT_ANALYZER_REVISION,
           "reviewed current analyzer revision differs")
    ensure(current_blob == CURRENT_ANALYZER_BLOB,
           "reviewed current analyzer Git object pin differs")

    try:
        historical_object = git(
            "rev-parse", f"{historical_revision}:{ANALYZER_PATH}", root=root
        ).decode().strip()
        historical_bytes = git(
            "show", f"{historical_revision}:{ANALYZER_PATH}", root=root
        )
        execution_object = git(
            "rev-parse", f"{execution_revision}:{ANALYZER_PATH}", root=root
        ).decode().strip()
        current_object = git(
            "rev-parse", f"{current_revision}:{ANALYZER_PATH}", root=root
        ).decode().strip()
        current_bytes = git(
            "show", f"{current_revision}:{ANALYZER_PATH}", root=root
        )
    except subprocess.CalledProcessError as error:
        raise ValueError("BLOCKED: required historical/current analyzer object unavailable") from error

    ensure(historical_object == HISTORICAL_ANALYZER_BLOB,
           "historical analyzer Git object differs")
    ensure(execution_object == HISTORICAL_ANALYZER_BLOB,
           "recorded execution analyzer Git object differs")
    ensure(current_object == CURRENT_ANALYZER_BLOB,
           "reviewed current analyzer Git object differs")
    ensure(git_blob_sha(historical_bytes) == historical_object,
           "historical analyzer bytes do not match its Git object")
    ensure(git_blob_sha(current_bytes) == current_object,
           "reviewed current analyzer bytes do not match its Git object")

    working_current = (root / ANALYZER_PATH).read_bytes()
    ensure(
        working_current == current_bytes
        or working_current == current_bytes.replace(b"\n", b"\r\n"),
        "current analyzer checkout differs beyond Git newline materialization",
    )

    module = ModuleType("_luna47b_historical_luna46_analyzer")
    module.__file__ = str(root / ANALYZER_PATH)
    module.__package__ = ""
    exec(compile(historical_bytes, module.__file__, "exec"), module.__dict__)
    return module, {
        "historical_revision": historical_revision,
        "historical_git_blob": historical_object,
        "historical_sha256": retained.sha(historical_bytes),
        "recorded_execution_revision": execution_revision,
        "execution_git_blob": execution_object,
        "current_revision": current_revision,
        "current_git_blob": current_object,
        "current_sha256": retained.sha(current_bytes),
        "current_checkout_sha256": retained.sha(working_current),
        "current_checkout_materialization": (
            "exact" if working_current == current_bytes
            else "exact-Git-LF-to-CRLF-checkout"
        ),
        "reconstruction_source": "authenticated historical Git object",
    }


def reconstruct(root: Path = ROOT) -> tuple[dict, dict]:
    # Reuse reviewed read-only integrity/reconciliation routines, not its CLI
    # (which intentionally enforces the historical Luna-46 branch).
    lane_metadata = verify_historical_lane_metadata(root)
    materialization = {}
    cache = {}

    analyzer, analyzer_sources = load_historical_analyzer(root)

    def committed_bytes(path: Path) -> bytes:
        relative = path.relative_to(root).as_posix()
        if relative not in cache:
            committed = git("show", f"{EVIDENCE_BASE}:{relative}", root=root)
            worktree = path.read_bytes()
            ensure(worktree == committed or worktree == committed.replace(b"\n", b"\r\n"),
                   "evidence differs beyond Git checkout materialization")
            ensure(git("rev-parse", f"HEAD:{relative}", root=root) ==
                   git("rev-parse", f"{EVIDENCE_BASE}:{relative}", root=root),
                   "evidence Git blob changed")
            cache[relative] = committed
            materialization[relative] = {
                "consumed_committed_sha256": analyzer.sha(committed),
                "consumed_revision": EVIDENCE_BASE, "byte_length": len(committed),
                "worktree_sha256": analyzer.sha(worktree),
                "worktree_equal": worktree == committed,
                "checkout_only_crlf": worktree != committed}
        return cache[relative]

    with patch.object(analyzer, "read_bytes", committed_bytes):
        integrity = analyzer.verify_integrity(root)
    document = json.loads(committed_bytes(root / RETAINED))
    ensure(analyzer.digest({k: v for k, v in document.items() if k != "output_digest"})
           == document["output_digest"], "corrected output internal digest differs")
    ensure(document["verdict"] == "MIXED", "retained verdict differs")
    load = lambda path: json.loads(committed_bytes(root / path))
    config = load(retained.L45 / "config.json")["experiment"]
    analyzer.validate_config(config, load(retained.L44 / "config.json")["experiment"])
    summary = load(retained.L45 / "summary.json")
    for arm in ("DESTINATION_DISABLED", "DESTINATION_DEFAULT", retained.CALIBRATED):
        analyzer.verify_phase_pair(load(retained.L45 / f"initial-{arm.lower()}.json"),
                                   load(retained.L45 / f"replay-{arm.lower()}.json"),
                                   config, summary, arm)
    phases = {}
    for phase in ("initial", "replay"):
        records = load(retained.L45 / f"{phase}-destination_calibrated.json")["records"]
        enqueues = analyzer.select_raw(load(retained.L45 / f"{phase}-destination_calibrated-enqueue.json"),
                                       records, phase, "enqueue", retained.CALIBRATED)
        receptions = analyzer.select_raw(load(retained.L45 / f"{phase}-destination_calibrated-reception.json"),
                                         records, phase, "reception", retained.CALIBRATED)
        results = []
        for record, queued, received in zip(records, enqueues, receptions):
            hop = lambda rows: [r for r in rows if r["source"] == "relay"
                                and r["destination"] == "destination"]
            arrivals = analyzer.reconcile(hop(queued), hop(received), "relay", "destination")
            results.append(analyzer.analyze_sequence(record["stream_id"], arrivals,
                           analyzer.destination_updates(record, arrivals)))
        ensure(results == document["sequences"], "exact reconstructed retained sequences differ")
        phases[phase] = analyzer.digest(results)
    ensure(phases["initial"] == phases["replay"], "retained replay differs")
    ensure(dict(Counter(s["category"] for s in document["sequences"])) == EXPECTED_COUNTS,
           "retained category partition differs")
    return document, {"integrity": integrity, "phase_digests": phases,
                      "retained_sha256": analyzer.sha(committed_bytes(root / RETAINED)),
                      "configuration_digest": analyzer.digest(config),
                      "materialization": materialization,
                      "analyzer_sources": analyzer_sources,
                      "historical_lane": lane_metadata}


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
