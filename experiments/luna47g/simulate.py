"""Independent, downstream-only Luna-47G stand-in; no TPCN imports."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import heapq
import itertools
import json
import math
from pathlib import Path
import platform
import random
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
LANE = ROOT / "experiments/luna47g"
CONFIG = json.loads((LANE / "config.json").read_text(encoding="utf-8"))
FIXTURES = json.loads((LANE / "fixtures.json").read_text(encoding="utf-8"))
PARAMS = ("R", "C", "G", "T", "L", "O", "N")
REGIMES = ("noise", "single", "accumulation", "compression", "return", "neutral")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def nominal() -> dict[str, float]:
    return dict(R=1.0, C=1.0, G=1.0, T=1.0, L=1.0, O=0.0,
                N=CONFIG["base_noise_amplitude"])


def draw(rng: random.Random, band: float) -> tuple[dict[str, float], list[float]]:
    u = [rng.uniform(-1, 1) for _ in range(8)]
    common, r, c, g, t, leak, offset, noise = u
    return dict(R=1 + band * (common + r) / 2,
                C=1 + band * (common + c) / 2,
                G=1 + band * g, T=1 + band * t, L=1 + band * leak,
                O=0.2 * band * offset,
                N=CONFIG["base_noise_amplitude"] * (1 + band * noise)), u


def noise_draw(rng: random.Random) -> dict[str, list[float]]:
    return {name: [rng.uniform(-1, 1) for _ in events]
            for name, events in FIXTURES.items()}


def validate_params(p: dict[str, float]) -> None:
    if set(p) != set(PARAMS) or not all(math.isfinite(v) for v in p.values()):
        raise ValueError("invalid parameters")
    if not all(0.5 <= p[k] <= 1.5 for k in ("R", "C", "G", "T", "L")):
        raise ValueError("multipliers outside declared finite domain")
    if abs(p["O"]) > 0.1 or not 0.04 <= p["N"] <= 0.12:
        raise ValueError("offset/noise outside declared domain")


def simulate(p: dict[str, float], events: list[list[float]],
             noise: list[float], sign: int = 1, shift: float = 0.0) -> dict[str, Any]:
    """Process irregular events and one-shot local returns, never a neural tick."""
    validate_params(p)
    if sign not in (-1, 1) or len(events) != len(noise):
        raise ValueError("invalid sign/noise count")
    if not events or len(events) > CONFIG["max_inputs"]:
        raise ValueError("invalid input count")
    if not math.isfinite(shift) or shift < 0:
        raise ValueError("invalid time shift")
    queue: list[tuple[float, int, int, float]] = []
    previous = -1.0
    for i, ((t, x), n) in enumerate(zip(events, noise)):
        if not all(math.isfinite(v) for v in (t, x, n)) or t < previous or t < 0:
            raise ValueError("nonfinite/late/negative input")
        if abs(n) > 1 or abs(x) > CONFIG["input_bound"]:
            raise ValueError("input/noise bound")
        v = sign * (x + p["N"] * n)
        if abs(v) > CONFIG["input_bound"]:
            raise ValueError("perturbed input bound")
        heapq.heappush(queue, (t + shift, 0, i, v))
        previous = t
    heapq.heappush(queue, (previous + shift + CONFIG["settle_interval"], 2,
                          len(events), 0.0))
    z = 0.0
    last = shift
    pending = False
    serial = len(events) + 1
    admitted = clipped = processed = 0
    deposition = peak = 0.0
    trace: list[dict[str, Any]] = []
    outputs: list[dict[str, Any]] = []
    failure = None
    while queue:
        t, kind, _, x = heapq.heappop(queue)
        processed += 1
        if processed > CONFIG["max_processed_events"]:
            failure = "processed_event_budget"
            break
        if t < last:
            raise ValueError("time reversal")
        z *= math.exp(-(t - last) * p["L"] / (p["R"] * p["C"]))
        last = t
        before = z
        qualified = False
        raw = z
        if kind == 0:
            threshold = CONFIG["qualification_threshold"] * p["T"]
            threshold += math.copysign(1.0, x) * p["O"]
            qualified = abs(p["G"] * x) >= threshold
            if qualified:
                admitted += 1
                d = p["G"] * x / p["C"]
                deposition += abs(d)
                raw = z + d
                z = max(-CONFIG["state_bound"], min(CONFIG["state_bound"], raw))
                clipped += int(z != raw)
        elif kind == 1:
            pending = False
        peak = max(peak, abs(z))
        pre_output = z
        output = None
        if kind != 2 and abs(z) >= p["T"]:
            if len(outputs) >= CONFIG["max_outputs"]:
                failure = "output_budget"
                break
            output = math.tanh(z)
            outputs.append(dict(time=t, value=output, kind=kind))
            z -= math.copysign(min(abs(z), CONFIG["discharge_fraction"] * p["T"]), z)
        scheduled = None
        if kind != 2 and abs(z) >= p["T"] and not pending:
            scheduled = t + CONFIG["return_delay"]
            if not scheduled > t:
                raise ValueError("unrepresentable strict-future return")
            heapq.heappush(queue, (scheduled, 1, serial, 0.0))
            serial += 1
            pending = True
        trace.append(dict(time=t, kind=kind, input=x, before=before,
                          qualified=qualified, raw=raw, pre_output=pre_output,
                          output=output, after=z, scheduled=scheduled))
    bound = failure is None and all(
        abs(row["pre_output"]) <= CONFIG["state_bound"]
        and abs(row["after"]) <= CONFIG["state_bound"] for row in trace)
    bound = bound and all(abs(row["value"]) <= CONFIG["output_bound"] for row in outputs)
    return dict(admitted=admitted, deposition=deposition, peak=peak,
                final=z, clipped=clipped, processed=processed, outputs=outputs,
                trace=trace, failure=failure, bounds=bound,
                neutral=abs(z) <= CONFIG["neutral_tolerance"],
                return_outputs=sum(row["kind"] == 1 for row in outputs))


def criteria(runs: dict[str, dict[str, Any]]) -> dict[str, bool]:
    n, s, near, far, m, e = (runs[k] for k in
                             ("noise", "single", "near", "far", "moderate", "extreme"))
    return dict(
        noise=n["admitted"] == 0 and not n["outputs"],
        single=s["admitted"] == 1 and s["peak"] >= CONFIG["single_min_peak"]
        and not s["outputs"],
        accumulation=near["admitted"] == 2
        and near["peak"] >= CONFIG["near_single_peak_ratio"] * s["peak"]
        and bool(near["outputs"]) and not far["outputs"],
        compression=m["admitted"] == 3 and len(m["outputs"]) == 1
        and abs(sum(o["value"] for o in m["outputs"]))
        <= CONFIG["moderate_compression_ratio"] * m["deposition"],
        return_=e["admitted"] == 1 and 2 <= len(e["outputs"]) <= CONFIG["max_outputs"]
        and e["return_outputs"] >= 1
        and abs(sum(o["value"] for o in e["outputs"])) <= e["deposition"],
        neutral=all(v["neutral"] for v in runs.values()))


def mirror_equal(a: dict[str, Any], b: dict[str, Any]) -> bool:
    tol = CONFIG["numeric_absolute_tolerance"]
    if len(a["trace"]) != len(b["trace"]) or len(a["outputs"]) != len(b["outputs"]):
        return False
    if a["admitted"] != b["admitted"] or a["failure"] != b["failure"]:
        return False
    for x, y in zip(a["trace"], b["trace"]):
        if x["kind"] != y["kind"] or x["time"] != y["time"]:
            return False
        if x["qualified"] != y["qualified"] or x["scheduled"] != y["scheduled"]:
            return False
        for key in ("input", "before", "raw", "pre_output", "after"):
            if abs(x[key] + y[key]) > tol:
                return False
        if (x["output"] is None) != (y["output"] is None):
            return False
        if x["output"] is not None and abs(x["output"] + y["output"]) > tol:
            return False
    return abs(a["final"] + b["final"]) <= tol


def evaluate(p: dict[str, float], noise: dict[str, list[float]]) -> dict[str, Any]:
    positive = {k: simulate(p, v, noise[k]) for k, v in FIXTURES.items()}
    negative = {k: simulate(p, v, noise[k], -1) for k, v in FIXTURES.items()}
    mirror_p = dict(p, O=-p["O"])
    mirror = {k: simulate(mirror_p, v, noise[k], -1) for k, v in FIXTURES.items()}
    zero_p = dict(p, O=0.0)
    zero_pairs = {k: [simulate(zero_p, v, noise[k]),
                     simulate(zero_p, v, noise[k], -1)] for k, v in FIXTURES.items()}
    signed = {}
    for label, runs in (("positive", positive), ("negative", negative)):
        gates = criteria(runs)
        gates["return"] = gates.pop("return_")
        signed[label] = gates
    gates = {k: all(v[k] for v in signed.values()) for k in REGIMES}
    gates["bounds"] = all(v["bounds"] for group in (positive, negative, mirror)
                          for v in group.values())
    gates["bounds"] = gates["bounds"] and all(v["bounds"] for pair in zero_pairs.values()
                                             for v in pair)
    gates["mirror"] = all(mirror_equal(positive[k], mirror[k]) for k in FIXTURES)
    gates["zero_offset_mirror"] = all(mirror_equal(*pair) for pair in zero_pairs.values())
    transitions = []
    for a, b in zip(REGIMES, REGIMES[1:]):
        if gates[a] != gates[b]:
            transitions.append(dict(source=a, target=b, source_pass=gates[a],
                                    target_pass=gates[b]))
    asymmetry = {k: dict(admission_difference=positive[k]["admitted"] - negative[k]["admitted"],
                        output_count_difference=len(positive[k]["outputs"])
                        - len(negative[k]["outputs"]),
                        peak_difference=positive[k]["peak"] - negative[k]["peak"])
                 for k in FIXTURES}
    return dict(gates=gates, signed_gates=signed, failed=[k for k, v in gates.items() if not v],
                pass_=all(gates.values()), transitions=transitions, asymmetry=asymmetry,
                runs=dict(positive=positive, negative=negative, offset_mirror=mirror),
                zero_offset_controls=zero_pairs)


def wilson(failures: int, n: int) -> list[float]:
    z = CONFIG["confidence_z"]
    p = failures / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [max(0.0, center - half), min(1.0, center + half)]


def sensitivity(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for key in PARAMS:
        ordered = sorted(rows, key=lambda r: (r["parameters"][key], r["id"]))
        q = len(rows) // 4
        low = sum(not r["outcome"]["pass_"] for r in ordered[:q]) / q
        high = sum(not r["outcome"]["pass_"] for r in ordered[-q:]) / q
        xs = [r["parameters"][key] for r in rows]
        ys = [float(not r["outcome"]["pass_"]) for r in rows]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        covariance = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        denominator = math.sqrt(sum((x - mx) ** 2 for x in xs)
                                * sum((y - my) ** 2 for y in ys))
        result.append(dict(parameter=key, low_quartile_failure=low,
                           high_quartile_failure=high, risk_difference=high - low,
                           correlation=covariance / denominator if denominator else 0.0))
    return sorted(result, key=lambda r: (-abs(r["risk_difference"]), r["parameter"]))


def generate() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    rows = []
    bands = {}
    for band_name, b in CONFIG["bands"].items():
        group = []
        for seed in CONFIG["seeds"]:
            rng = random.Random(seed)
            for index in range(CONFIG["samples_per_seed_per_band"]):
                p, units = draw(rng, b)
                noise = noise_draw(rng)
                row = dict(id=f"{band_name}:{seed}:{index}", band=band_name,
                           seed=seed, index=index, parameter_units=units,
                           parameters=p, noise_units=noise, outcome=evaluate(p, noise))
                group.append(row)
        rows.extend(group)
        n = len(group)
        failed = sum(not r["outcome"]["pass_"] for r in group)
        counts = {k: sum(not r["outcome"]["gates"][k] for r in group)
                  for k in group[0]["outcome"]["gates"]}
        signed_counts = {s: {k: sum(not r["outcome"]["signed_gates"][s][k] for r in group)
                             for k in REGIMES} for s in ("positive", "negative")}
        transitions = {}
        for row in group:
            for t in row["outcome"]["transitions"]:
                name = f'{t["source"]}:{t["source_pass"]}->{t["target"]}:{t["target_pass"]}'
                transitions[name] = transitions.get(name, 0) + 1
        bands[band_name] = dict(n=n, failures=failed, failure_fraction=failed / n,
                               wilson95=wilson(failed, n), gate_failures=counts,
                               signed_gate_failures=signed_counts,
                               transitions=transitions, sensitivity=sensitivity(group),
                               seeds={str(s): sum(not r["outcome"]["pass_"] for r in group
                                                  if r["seed"] == s)
                                      for s in CONFIG["seeds"]},
                               clipped_runs=sum(run["clipped"] > 0 for row in group
                                                for run in row["outcome"]["runs"]["positive"].values()))
    corner_rows = []
    interactions = []
    noise = noise_draw(random.Random(CONFIG["interaction_seed"]))
    for name in CONFIG["interaction_bands"]:
        b = CONFIG["bands"][name]
        for pair in itertools.combinations(PARAMS, 2):
            flags = {}
            for a, c in itertools.product((-1, 1), repeat=2):
                p = nominal()
                for key, direction in zip(pair, (a, c)):
                    if key == "O":
                        p[key] = direction * 0.2 * b
                    elif key == "N":
                        p[key] *= 1 + direction * b
                    else:
                        p[key] = 1 + direction * b
                outcome = evaluate(p, noise)
                label = f"{a},{c}"
                flags[label] = int(not outcome["pass_"])
                corner_rows.append(dict(id=f"corner:{name}:{pair[0]}:{pair[1]}:{label}",
                                        band=name, pair=pair, directions=[a, c],
                                        parameters=p, noise_units=noise, outcome=outcome))
            interactions.append(dict(band=name, pair=pair, failures=flags,
                                     difference_in_differences=flags["1,1"] - flags["1,-1"]
                                     - flags["-1,1"] + flags["-1,-1"]))
    passing = [k for k, v in bands.items()
               if v["failure_fraction"] <= CONFIG["verdict_max_failure_fraction"]
               and all(v["gate_failures"][g] == 0 for g in
                       ("bounds", "mirror", "zero_offset_mirror"))]
    if len(passing) == len(bands):
        verdict = "SUPPORTED"
    elif "nominal" in passing and len(passing) > 1:
        verdict = "PARTIALLY SUPPORTED"
    else:
        verdict = "NOT SUPPORTED"
    return rows, corner_rows, dict(verdict=verdict, bands=bands, passing_bands=passing,
                                  interactions=interactions, sample_count=len(rows),
                                  corner_count=len(corner_rows))


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def provenance() -> dict[str, Any]:
    revision = git("rev-parse", "HEAD").decode().strip()
    paths = ["experiments/luna47g/config.json", "experiments/luna47g/fixtures.json",
             "experiments/luna47g/PROTOCOL.md", "experiments/luna47g/simulate.py",
             "tests/test_luna47g_robustness.py"]
    hashes = {}
    for path in paths:
        blob = git("show", f"{revision}:{path}")
        raw = (ROOT / path).read_bytes()
        if raw.replace(b"\r\n", b"\n") != blob.replace(b"\r\n", b"\n"):
            raise ValueError(f"uncommitted execution source {path}")
        hashes[path] = dict(git_blob_sha256=sha(blob), raw_sha256=sha(raw))
    return dict(execution_revision=revision, python=sys.version, platform=platform.platform(),
                authorization_revision=CONFIG["authorization_revision"],
                production_evidence_revision=CONFIG["production_evidence_revision"],
                configuration_sha256=sha(canonical(CONFIG)),
                fixture_sha256=sha(canonical(FIXTURES)), sources=hashes,
                tolerance=CONFIG["numeric_absolute_tolerance"],
                neutral_tolerance=CONFIG["neutral_tolerance"])


def output_directory() -> Path:
    target = ROOT / "artifacts/luna47g"
    if target.resolve() != ROOT.resolve() / "artifacts/luna47g":
        raise ValueError("output directory alias")
    target.mkdir(parents=True, exist_ok=True)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="compare, never overwrite retained bytes")
    args = parser.parse_args()
    prov = provenance()
    rows, corners, summary = generate()
    # Second in-memory execution checks RNG/event-state determinism before publication.
    again = generate()
    if canonical((rows, corners, summary)) != canonical(again):
        raise ValueError("in-memory replay mismatch")
    payloads = {"samples.jsonl.gz": gzip.compress(b"".join(canonical(r) for r in rows), mtime=0),
                "corners.jsonl.gz": gzip.compress(b"".join(canonical(r) for r in corners), mtime=0),
                "summary.json": canonical(summary)}
    manifest = dict(schema=CONFIG["schema"], provenance=prov,
                    files={k: dict(sha256=sha(v), bytes=len(v)) for k, v in payloads.items()},
                    in_memory_replay=True, component_specs="ASSUMED; Luna-47E not consumed")
    target = output_directory()
    if args.verify:
        retained = json.loads((target / "manifest.json").read_bytes())
        # Later publication commits change HEAD, not frozen execution sources.
        for key in ("configuration_sha256", "fixture_sha256", "sources",
                    "authorization_revision", "production_evidence_revision"):
            if retained["provenance"][key] != prov[key]:
                raise ValueError(f"source provenance mismatch: {key}")
        for name, data in payloads.items():
            if (target / name).read_bytes() != data:
                raise ValueError(f"fresh-process replay mismatch: {name}")
        if retained["files"] != manifest["files"]:
            raise ValueError("retained manifest mismatch")
        print("Fresh-process replay: PASS (all payload bytes and source hashes)")
    else:
        payloads["manifest.json"] = canonical(manifest)
        for name in payloads:
            if (target / name).exists():
                raise ValueError(f"refusing overwrite: {name}")
            if (target / name).resolve().parent != target.resolve():
                raise ValueError("output file alias")
        for name, data in payloads.items():
            (target / name).write_bytes(data)
        print(json.dumps(dict(verdict=summary["verdict"], bands={
            k: dict(failures=v["failures"], n=v["n"], gates=v["gate_failures"])
            for k, v in summary["bands"].items()}), indent=2))


if __name__ == "__main__":
    main()
