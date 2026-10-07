"""Reviewer-owned subprocess harness; never writes tracked lane files."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def run(name, cwd, args, overrides=None):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cwd)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.update(overrides or {})
    xml_path = OUT / (name + ".xml")
    xml_path.unlink(missing_ok=True)
    command = [sys.executable, "-m", "pytest", *args, "-ra",
               f"--junitxml={xml_path}"]
    start = time.monotonic()
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (OUT / (name + ".log")).open("wb") as log:
        log.write((f"cwd={cwd}\ncommand={command!r}\n"
                   f"PYTHONPATH={env['PYTHONPATH']}\nPYTHONHASHSEED=0\n"
                   f"PYTHONDONTWRITEBYTECODE=1\nstarted={stamp}\n").encode())
        log.write(f"process_local_overrides={overrides or {}}\n".encode())
        log.flush()
        process = subprocess.run(command, cwd=cwd, env=env, stdout=log,
                                 stderr=subprocess.STDOUT, check=False)
    record = {
        "name": name, "cwd": str(cwd), "command": command,
        "python": sys.version, "executable": sys.executable,
        "revision": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=cwd, text=True).strip(),
        "started_utc": stamp, "seconds": time.monotonic() - start,
        "exit_code": process.returncode,
        "environment": {k: env[k] for k in
                        ("PYTHONPATH", "PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE")},
        "process_local_overrides": overrides or {},
        "log_sha256": hashlib.sha256(
            (OUT / (name + ".log")).read_bytes()).hexdigest(),
    }
    (OUT / (name + "-execution.json")).write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record), flush=True)
    print((OUT / (name + ".log")).read_text(
        encoding="utf-8", errors="replace")[-5000:], flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("full", "focused", "boundary", "newline", "predictive"))
    options = parser.parse_args()
    if options.mode == "full":
        run("governance-full", ROOT, ["tests"])
    elif options.mode == "focused":
        for letter in "abcdefg":
            lane = ROOT.parent / f"luna47{letter}"
            tests = sorted(lane.glob(f"tests/test_luna47{letter}_*.py"))
            run(f"lane-{letter}-focused", lane,
                [str(p.relative_to(lane)) for p in tests])
    elif options.mode == "boundary":
        tests = sorted(
            p for p in (ROOT / "tests").glob("test_*.py")
            if any(word in p.name for word in (
                "event_runtime", "excursion", "topology", "prediction",
                "eligibility", "reward", "energy", "structural", "luna11",
                "temporal_state")))
        run("governance-boundary", ROOT,
            [str(p.relative_to(ROOT)) for p in tests])
    elif options.mode == "predictive":
        run("governance-predictive", ROOT, [
            "tests/test_canonical_event_neuron.py",
            "tests/test_predictive_coding.py"])
    else:
        run("governance-newline-override", ROOT, [
            "tests/test_luna44_canonical_fixture.py",
            "tests/test_luna44_canonical_fixture_verification.py",
            "tests/test_luna46_depth_scaling_diagnostic.py"], {
                "GIT_CONFIG_COUNT": "2",
                "GIT_CONFIG_KEY_0": "core.autocrlf",
                "GIT_CONFIG_VALUE_0": "false",
                "GIT_CONFIG_KEY_1": "core.eol",
                "GIT_CONFIG_VALUE_1": "lf",
            })
