"""Downstream-only scoring and reproducible machine-readable replay package."""
from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys

from .fixtures import FAMILIES, canonical, digest, fixtures
from .qualifier import Config, METHODS, Qualifier


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "artifacts" / "luna47c"
BASE = "789dda5988daf72f375d9713bd76a6da2b9e8b34"
EVIDENCE_BASE = "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
TOLERANCE = 1e-12
RECOVERY_TOLERANCE = 0.025
RECOVERY_WINDOW = 5


def trace(inputs, method):
    q = Qualifier(Config(method))
    return [q.process(timestamp, raw) for timestamp, raw in inputs]


def score(fixture, events, control):
    truth = fixture.signal_truth
    admitted = [e["E"] != 0.0 for e in events]
    baseline_delta = [e["B_after"] - c["B_after"] for e, c in zip(events, control)]
    noise_delta = [e["N_after"] - c["N_after"] for e, c in zip(events, control)]
    meaningful = [i for i, s in enumerate(truth) if s != 0.0]
    recovery = None
    status = "not_applicable"
    if meaningful:
        status = "right_censored"
        last = meaningful[-1]
        for i in range(last + 1, len(events) - RECOVERY_WINDOW + 1):
            if all(abs(baseline_delta[j]) <= RECOVERY_TOLERANCE and
                   abs(noise_delta[j]) <= RECOVERY_TOLERANCE
                   for j in range(i, i + RECOVERY_WINDOW)):
                recovery = {"start_index": i, "confirmation_index": i + RECOVERY_WINDOW - 1,
                            "elapsed_time": events[i]["timestamp"] - events[last]["timestamp"]}
                status = "recovered"
                break
    errors = [abs(e["B"] - b) for e, b in zip(events, fixture.baseline_truth)]
    sign = {}
    for name, direction in (("positive", 1), ("negative", -1)):
        indices = [i for i in meaningful if truth[i] * direction > 0]
        sign[name] = {"meaningful": len(indices),
                      "missed": sum(not admitted[i] for i in indices),
                      "wrong_sign": sum(admitted[i] and events[i]["E"] * truth[i] < 0
                                        for i in indices)}
    return {
        "events": len(events), "meaningful": len(meaningful),
        "noise_only": len(events) - len(meaningful),
        "false_admissions": sum(a and s == 0 for a, s in zip(admitted, truth)),
        "missed_meaningful": sum(not admitted[i] for i in meaningful),
        "baseline_error_mean": sum(errors) / len(errors),
        "baseline_error_max": max(errors),
        "baseline_pull_max": max(abs(x) for x in baseline_delta),
        "noise_contamination_max": max(0.0, max(noise_delta)),
        "noise_difference_abs_max": max(abs(x) for x in noise_delta),
        "recovery_status": status, "recovery": recovery, "sign_counts": sign,
    }


def experiment():
    fs = fixtures()
    runs = []
    for f in fs:
        control_inputs = tuple((t, b + n) for (t, _), b, n in
                               zip(f.inputs, f.baseline_truth, f.noise_truth))
        for method in METHODS:
            events = trace(f.inputs, method)
            control = trace(control_inputs, method)
            runs.append({"fixture": f.identity, "fixture_sha256": digest(f.serialized()),
                         "method": method, "configuration": asdict(Config(method)),
                         "events": events, "signal_free_control_events": control,
                         "metrics": score(f, events, control)})
    indexed = {(r["fixture"], r["method"]): r for r in runs}
    symmetry = []
    for family in FAMILIES:
        for method in METHODS:
            a, b = indexed[(f"{family}:+1", method)], indexed[(f"{family}:-1", method)]
            error = max(max(abs(x["B"] + y["B"]), abs(x["N"] - y["N"]),
                            abs(x["E"] + y["E"]), abs(x["B_after"] + y["B_after"]),
                            abs(x["N_after"] - y["N_after"]))
                        for x, y in zip(a["events"], b["events"]))
            symmetry.append({"family": family, "method": method,
                             "mirror_max_absolute_error": error,
                             "within_tolerance": error <= TOLERANCE})
    chain = []
    for method in METHODS:
        r = indexed[("contamination_chain:+1", method)]
        c = r["signal_free_control_events"]
        later = (61, 62, 64, 68)
        chain.append({"method": method,
                      "spike_index": 60, "spike_N_after": r["events"][60]["N_after"],
                      "control_N_after": c[60]["N_after"],
                      "later_indices": later,
                      "later_misses": sum(r["events"][i]["E"] == 0 for i in later),
                      "control_threshold_would_admit_later": [
                          abs(r["events"][i]["raw"] - c[i]["B"]) > c[i]["band"]
                          for i in later]})
    # No single aggregate score: separate mechanism gates, fixed before execution.
    naive = next(x for x in chain if x["method"] == "adaptive")
    robust = next(x for x in chain if x["method"] == "robust")
    gates = {
        "failure_chain_observed": naive["spike_N_after"] > naive["control_N_after"] + 0.5
                                 and naive["later_misses"] >= 1
                                 and all(naive["control_threshold_would_admit_later"]),
        "robust_chain_protection": robust["later_misses"] < naive["later_misses"]
                                  and robust["spike_N_after"] < naive["spike_N_after"] * 0.25,
        "sign_symmetry": all(x["within_tolerance"] for x in symmetry),
        "universal_no_errors": all(r["metrics"]["false_admissions"] == 0 and
                                  r["metrics"]["missed_meaningful"] == 0 for r in runs),
    }
    if not gates["failure_chain_observed"] or not gates["sign_symmetry"]:
        verdict = "NOT SUPPORTED"
    elif gates["robust_chain_protection"] and gates["universal_no_errors"]:
        verdict = "SUPPORTED"
    elif gates["robust_chain_protection"]:
        verdict = "PARTIALLY SUPPORTED"
    else:
        verdict = "NOT SUPPORTED"
    return {"schema": "LUNA47C-1", "fixtures": [f.serialized() for f in fs],
            "runs": runs, "symmetry": symmetry, "contamination_chain": chain,
            "gates": gates, "verdict": verdict}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def source_hashes():
    paths = sorted((ROOT / "experiments" / "luna47c").glob("*.py"))
    paths += [ROOT / "experiments" / "luna47c" / "PROTOCOL.md"]
    paths += sorted((ROOT / "tests").glob("test_luna47c_*.py"))
    # Normalize checkout line endings; include actual hashes separately at capture.
    return {p.relative_to(ROOT).as_posix():
            hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
            for p in paths}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true",
                        help="Recompute and compare retained canonical scientific bytes")
    args = parser.parse_args()
    result = experiment()
    replay = experiment()
    if canonical(result) != canonical(replay):
        raise RuntimeError("nondeterministic same-process replay")
    if args.verify:
        retained = json.loads((OUTPUT / "replay.json").read_bytes())
        if canonical(retained["science"]) != canonical(result):
            raise RuntimeError("retained science differs")
        if retained["provenance"]["source_sha256_lf"] != source_hashes():
            raise RuntimeError("source differs from frozen package")
        manifest = json.loads((OUTPUT / "manifest.json").read_bytes())
        for name, sha in manifest["files_sha256"].items():
            if hashlib.sha256((OUTPUT / name).read_bytes()).hexdigest() != sha:
                raise RuntimeError(f"file digest differs: {name}")
        print("PASS: retained science, source identities and manifest hashes match")
        return
    revision = git("rev-parse", "HEAD")
    if git("status", "--porcelain", "--", "experiments/luna47c", "tests"):
        raise RuntimeError("commit code/protocol/tests before scoring publication")
    git("merge-base", "--is-ancestor", BASE, revision)
    package = {"science": result, "provenance": {
        "repository_revision": revision, "authorization_revision": BASE,
        "production_evidence_revision": EVIDENCE_BASE,
        "source_sha256_lf": source_hashes(),
        "python": sys.version, "platform": platform.platform(),
        "float_model": "Python binary64; libm expm1; absolute comparison 1e-12",
        "replay": {"same_process_exact": True, "science_sha256": digest(result),
                   "fresh_process_command": "python -m experiments.luna47c.evaluate --verify"},
    }}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    target = OUTPUT / "replay.json"
    if target.exists():
        raise RuntimeError("refusing to overwrite retained outcome")
    target.write_bytes(canonical(package))
    summary = {"verdict": result["verdict"], "gates": result["gates"],
               "contamination_chain": result["contamination_chain"],
               "symmetry": result["symmetry"],
               "metrics": [{k: r[k] for k in ("fixture", "method", "metrics")}
                           for r in result["runs"]]}
    (OUTPUT / "summary.json").write_bytes(canonical(summary))
    manifest = {"schema": "LUNA47C-MANIFEST-1",
                "files_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (target, OUTPUT / "summary.json")},
                "science_sha256": digest(result)}
    (OUTPUT / "manifest.json").write_bytes(canonical(manifest))
    print(json.dumps({"verdict": result["verdict"], "gates": result["gates"],
                      "contamination_chain": result["contamination_chain"]}, indent=2))


if __name__ == "__main__":
    main()
