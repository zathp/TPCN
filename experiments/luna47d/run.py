"""Generate or verify replay evidence, writing only the owned artifact path."""
import argparse
from copy import deepcopy
from dataclasses import asdict, replace
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys

from .model import (Config, canonical, digest, load_fixtures, reconcile,
                    scientific_failures, simulate)

ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION = "789dda5988daf72f375d9713bd76a6da2b9e8b34"
BASELINE = "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
OUTPUT = ROOT / "artifacts/luna47d/evidence.json"
SOURCES = [
    "experiments/luna47d/PROTOCOL.md",
    "experiments/luna47d/fixtures.json",
    "experiments/luna47d/model.py",
    "experiments/luna47d/run.py",
    "tests/test_luna47d_output_model.py",
]


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT).decode().strip()


def source_manifest(revision):
    manifest = []
    for path in SOURCES:
        checkout = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        committed = subprocess.check_output(
            ["git", "--no-pager", "show", f"{revision}:{path}"], cwd=ROOT
        ).replace(b"\r\n", b"\n")
        if checkout != committed:
            raise ValueError(f"checkout source differs from {revision}: {path}")
        manifest.append({
            "path": path, "git_blob": git("rev-parse", f"{revision}:{path}"),
            "sha256_lf": hashlib.sha256(committed).hexdigest(),
        })
    return manifest


def negative_controls(primary):
    controls = []
    for fixture in load_fixtures():
        if fixture["family"] == "moderate-cluster":
            result = simulate(fixture, replace(Config(), quantum=1))
            failures = scientific_failures(result)
            reconcile(result)
            controls.append({"id": f'weak-drain/{fixture["polarity"]}',
                             "type": "real-alternate-configuration",
                             "result": result, "failures": failures,
                             "detected": "count/compression-regime" in failures})
    base = next(r for r in primary if r["trajectory"]["id"] == "moderate-low/positive")
    config_cases = [
        ("zero-leak", replace(Config(), leak=0)),
        ("zero-period", replace(Config(), period="0")),
        ("zero-drain", replace(Config(), quantum=0)),
        ("short-horizon", replace(Config(), tail="1")),
    ]
    for identity, cfg in config_cases:
        try:
            simulate(base["trajectory"], cfg)
        except ValueError as exc:
            controls.append({"id": identity, "type": "invalid-configuration",
                             "configuration": asdict(cfg), "rejection": str(exc), "detected": True})
        else:
            controls.append({"id": identity, "detected": False})
    for identity, drive in (("oversized-drive", 33), ("nonfinite-drive", float("inf"))):
        fixture = deepcopy(base["trajectory"])
        fixture["inputs"][0]["drive"] = drive
        try:
            simulate(fixture)
        except ValueError as exc:
            # The invalid nonfinite value is represented symbolically in JSON.
            controls.append({"id": identity, "type": "invalid-input",
                             "input_id": fixture["inputs"][0]["id"],
                             "input_time": fixture["inputs"][0]["time"],
                             "drive": drive if identity == "oversized-drive" else "+infinity",
                             "rejection": str(exc), "detected": True})
        else:
            controls.append({"id": identity, "detected": False})

    for identity in ("self-sustaining-output", "missing-output", "state-overflow",
                     "failed-recovery", "output-budget-overflow"):
        record = deepcopy(base)
        if identity == "self-sustaining-output":
            extra = deepcopy(record["outputs"][0])
            extra.update(id="injected/out/extra", time="100")
            record["outputs"].append(extra)
            record["metrics"]["output_count"] += 1
        elif identity == "missing-output":
            record["outputs"].clear()
            record["metrics"]["output_count"] = 0
        elif identity == "state-overflow":
            record["trace"][0]["post"] = 33
            record["metrics"]["max_abs_state"] = 33
        elif identity == "failed-recovery":
            record["trace"][-1]["post"] = 1
            record["metrics"].update(final_abs_state=1, recovery_time=None,
                                     recovery_delay=None, pending_at_horizon="145")
        else:
            record["outputs"] = [
                dict(record["outputs"][0], id=f"injected/out/{i}", time=str(i + 1))
                for i in range(33)
            ]
            record["metrics"]["output_count"] = 33
        failures = scientific_failures(record)
        try:
            reconcile(record)
        except ValueError as exc:
            mismatch = str(exc)
        else:
            mismatch = None
        controls.append({"id": identity, "type": "synthetic-record-fault-NOT-model-observation",
                         "record": record, "failures": failures,
                         "replay_rejection": mismatch,
                         "detected": bool(failures) and mismatch is not None})
    return controls


def analyze():
    fixtures = load_fixtures()
    initial = [simulate(f) for f in fixtures]
    replay = [simulate(f) for f in fixtures]
    replay_equal = canonical(initial) == canonical(replay)
    failures = {r["trajectory"]["id"]: scientific_failures(r) for r in initial}
    for result in initial:
        reconcile(result)
    symmetry = []
    for positive, negative in zip(initial[::2], initial[1::2]):
        symmetric = (
            positive["metrics"] == negative["metrics"]
            and [(o["time"], o["sign"]) for o in positive["outputs"]]
            == [(o["time"], -o["sign"]) for o in negative["outputs"]]
            and all(a["pre"] == -b["pre"] and a["post"] == -b["post"]
                    for a, b in zip(positive["trace"], negative["trace"]))
            and len(positive["trace"]) == len(negative["trace"])
        )
        symmetry.append({"family": positive["trajectory"]["family"], "pass": symmetric})
    negatives = negative_controls(initial)
    all_pass = (not any(failures.values()) and replay_equal and
                all(s["pass"] for s in symmetry) and all(c["detected"] for c in negatives))
    target = [r for r in initial if r["trajectory"]["family"] in
              ("moderate-low", "moderate-high", "moderate-cluster",
               "extreme-low", "extreme", "extreme-cap", "extreme-cluster")]
    some_pass = any(not scientific_failures(r) for r in target)
    return {
        "initial": initial, "replay": replay, "initial_sha256": digest(initial),
        "replay_sha256": digest(replay), "replay_byte_equal": replay_equal,
        "primary_failures": failures, "symmetry": symmetry, "negative_controls": negatives,
        "verdict": "SUPPORTED" if all_pass else "PARTIALLY SUPPORTED" if some_pass else "NOT SUPPORTED",
    }


def build():
    if git("status", "--porcelain"):
        raise ValueError("commit protocol/code/tests before outcome generation; worktree must be clean")
    revision = git("rev-parse", "HEAD")
    if subprocess.run(["git", "merge-base", "--is-ancestor", AUTHORIZATION, revision], cwd=ROOT).returncode:
        raise ValueError("wrong authorization ancestry")
    analysis = analyze()
    record = {
        "schema": "L47D-EVIDENCE-1",
        "scope": "independent synthetic output model only; no upstream reachability claim",
        "provenance": {
            "authorization_revision": AUTHORIZATION, "production_evidence_revision": BASELINE,
            "source_revision": revision, "branch": git("branch", "--show-current"),
            "sources": source_manifest(revision),
            "python": sys.version, "implementation": platform.python_implementation(),
            "platform": platform.platform(), "seed": None,
        },
        "replay_metadata": {
            "command": "python -m experiments.luna47d.run --verify",
            "canonical_encoding": "UTF-8 sorted keys indent 2 final LF allow_nan=False",
            "identity_and_timestamp_tolerance": 0,
            "replay_byte_tolerance": 0, "threshold_tolerance": 0,
            "equation_abs_rel_tolerance": 1e-12,
            "event_time_encoding": "exact rational string",
            "recovery_time_encoding": "analytic binary64 metric, not an event",
        },
        "analysis": analysis,
    }
    record["integrity_sha256"] = digest(record)
    return record


def verify(record):
    payload = deepcopy(record)
    stored = payload.pop("integrity_sha256")
    if digest(payload) != stored:
        raise ValueError("artifact integrity mismatch")
    provenance = record["provenance"]
    if (provenance["authorization_revision"] != AUTHORIZATION or
            provenance["production_evidence_revision"] != BASELINE):
        raise ValueError("baseline mismatch")
    if provenance["sources"] != source_manifest(provenance["source_revision"]):
        raise ValueError("source manifest mismatch")
    # Comparing all records rejects renamed/missing inputs/outputs and false metrics.
    if canonical(record["analysis"]) != canonical(analyze()):
        raise ValueError("full fixture/output identity and result replay mismatch")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.generate == args.verify:
        parser.error("select exactly one of --generate or --verify")
    if args.generate:
        # Resolve and check the fixed path, including existing directory aliases.
        owned = ROOT / "artifacts/luna47d"
        if owned.resolve() != owned.absolute() or OUTPUT.resolve() != OUTPUT.absolute():
            raise ValueError("artifact alias outside fixed owned path")
        record = build()
        owned.mkdir(parents=True, exist_ok=True)
        with OUTPUT.open("xb") as stream:
            stream.write(canonical(record))
        print(f'Generated {OUTPUT}; verdict {record["analysis"]["verdict"]}')
    else:
        record = json.loads(OUTPUT.read_text(encoding="utf-8"))
        verify(record)
        print(f'Verified all identities/states/metrics and replay; {record["analysis"]["verdict"]}')


if __name__ == "__main__":
    main()
