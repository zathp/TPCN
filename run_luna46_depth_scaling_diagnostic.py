"""Luna-46 downstream-only offline diagnostic (never imports TPCN or a runner).

TPCN-LUNA46-OFFLINE-1 binds immutable inputs, code/environment, replay, sequence
evidence and a mechanism-only verdict. Inputs are the published Luna-44/45
inventory; limits are 320 characters, 4096 observations/character, 100 MiB/file.
The CLI requires an explicit new output path in the artifacts/luna46-* namespace,
canonically disjoint from retained evidence and the frozen Luna-44 fixture tree
(suggested: artifacts/luna46-depth-scaling-diagnostic/analysis.json), verifies integrity before loading
analytical inputs, and never captures, generates, tunes, or feeds back results.

Percentiles use sorted linear interpolation at (n-1)*p, p=50,75,90,95,99.
Empty distributions have null statistics; zero ties are retained. Alignment
uses the actual pre-input signed state; zero state/input are separate cases.
Retention ratios with zero previous state are null, not invented full retention.
Critical rates are analytical-only status classifications; a boundary is
reported only when same-sign monotonicity proves it unique (never tuning).
Clipping, discharge, non-integrating receptions or unexplained state changes
are BLOCKED rather than replaced with an alternate production configuration.
Matching roots_truncated flags describe bounded causal-root metadata, not
missing raw captures; preserve/count them without claiming complete ancestry.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import statistics
import struct
import subprocess
import sys
from typing import Any

from scripts.verify_luna44_canonical_fixture import EXPECTED_FIXTURE_PATH


Record = dict[str, Any]
ROOT = Path(__file__).resolve().parent
BASELINE = "d1f901d3d995dc013f22dd086ae1ed8ffd28293d"
AUTHORIZATION = "bb080228bac2287da49c1b47fc1484b436a59106"
BRANCH = "copilot/luna46-depth-scaling-diagnostic"
L45 = Path("artifacts/luna45-acp0008-depth2-destination-integration-20261006")
L44 = Path("artifacts/luna44-acp0008-independent-routing-rerun-20261005")
CATALOG_HASH = "a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e"
VERIFICATION = Path("artifacts/luna45-corrective-verification-20261006-r1/verification.json")
FIXTURE_ROOT = Path(EXPECTED_FIXTURE_PATH).parent
OUTPUT_NAMESPACE = "luna46-"
VERIFICATION_HASH = "547336a1140ea89b6b85cc76807ac5e931fb402296aebe759165804ecd6c103f"
FIXTURE_HASH = "66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629"
FIXTURE_DIGEST = "6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305"
FIXTURE_REVISION = "6413cffe6982bccc6698af6bebfae51f04e71dd9"
MANIFEST_HASH = "6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22"
MANIFEST_REVISION = "86e5a2f389af06b06bf04a614edaed88e0847902"
MANIFEST_BLOB = "eb9179abae7eed10891e6022832f16735111b220"
CONFIG45 = "cb6621ff403836e1b72b86a65375df11c2841df61030fbe5dd8a654a70394c1a"
CONFIG44 = "942b86a9cd7a3965265ec9d01aff7e0b0e2bf68b309f0e0bd22dc4cbae71884e"
REVISION45 = "97a93b394d071413075a1f102fdef695664722ff"
REVISION44 = "4baab60f87b820db800e04d0eb3277fb0e94f9b3"
RUNNER44_GIT_HASH = "032a0386b04b66d3ee67601d2f52fd828f54697be745a0caeff8e4c076e5215b"
HISTORY_FILES = {
    "config.json": (62236, "1cb40064bfb26572da86419898275d62a55a2f5eae5c1041976ffca3e4e484d3"),
    "summary.json": (166982, "5e10242aaf3219fca81a6fab62f252fb9f5a770a1b13ce6a4eeb36ff9da35f36"),
    "results.json": (87543502, "16deacb459a9c6715c14fd7caa5ecf4f6910776316fb80e890a1969fa92aa6e9"),
    "routing-initial-enqueue.json": (2849711, "61e0040541a4ac877a833f7d7605138edb065547cb154b7a46bade4de1e7139b"),
    "routing-initial-reception.json": (3966120, "d1e24f6239e9f0758e3991a2416d826407a5d12adf73c5ef97762ba89861b44a"),
    "routing-replay-enqueue.json": (2849710, "0663fee326614a74fb14770c45b4fbe7abb015c3510afd92022f80a43ac88f69"),
    "routing-replay-reception.json": (3966119, "c6aa27f550dc6ac6e7e572b8ade143f36a02707f1041f0a0c45a5452ee83c9b0"),
}
RATE = 0.0125
TAU = 80.0
THRESHOLD = 1.0
PERCENTILES = (50, 75, 90, 95, 99)
MAX_FILE_BYTES = 100 * 1024 * 1024
MAX_SEQUENCES = 320
MAX_EVENTS = 4096
CALIBRATED = "DESTINATION_CALIBRATED"
CATEGORIES = (
    "NO-RECEPTIONS", "ALREADY-CROSSING", "TEMPORAL-RETENTION-LIMITED",
    "CANCELLATION-LIMITED", "DRIVE-LIMITED",
)
POLICY = {
    "lambda": RATE, "tau": TAU, "theta_Z": THRESHOLD,
    "reset": "z=z0=0 per character; first interval uses retained prior_clock",
    "zero_decay": "signed prefix, analytically no discharge",
    "threshold": "abs(state)>=1 exactly; no tolerance",
    "equation_tolerance": "64*sys.float_info.epsilon*max(1,abs(observed),abs(expected))",
    "percentiles": list(PERCENTILES),
    "percentile_estimator": "linear interpolation at (n-1)*p/100",
    "zero_state": "alignment=zero-reference; retention_ratio=null",
    "zero_payload": "separate; breaks consecutive same-sign runs",
    "critical_rate": None,  # set below from CRITICAL_RATE_POLICY
    "limits": {"characters": MAX_SEQUENCES, "events_per_character": MAX_EVENTS,
               "bytes_per_file": MAX_FILE_BYTES},
    "boundary_policy": "BLOCKED for clipping, discharge, or non-integrating reception",
    "actual_state": "retained post-update state validated against signed recurrence; threshold flags must agree exactly",
    "roots_truncated": "exact matching boolean metadata; not raw-capture truncation or complete ancestry evidence",
}

# Analytical-only boundary of the declared signed equation; never production tuning,
# never a network rate sweep, never a configuration recommendation, never fed back.
CRITICAL_SOLVER_TOLERANCE = 64 * sys.float_info.epsilon * RATE
CRITICAL_SOLVER_ITERATIONS = 1100  # exceeds binary64 bisection depth on [0, RATE]
CRITICAL_RATE_POLICY = {
    "scope": "OFFLINE ANALYTICAL ONLY; not production tuning, rate sweep or recommendation",
    "equation": "z_k(l)=sum_{i<=k} u_i*exp(-l*(t_k-t_i)), retained timestamps/order/reset, "
                "no discharge/clipping; F(l)=max_k abs(z_k(l)); crossing F(l)>=1",
    "domain": "l in [0, inf); F(0)=signed zero-decay oracle, F(lambda)=actual-rate recurrence",
    "uniqueness": "same-sign payloads make every abs(z_k) continuous non-increasing; with "
                  "F(0)>=1>F(lambda) a second root would force a rate-independent maximizer "
                  "with F=1 at every rate, contradicting F(lambda)<1; so {F>=1}=[0,l*]",
    "solver": {"method": "bisection on [0, lambda] keeping F(lo)>=1>F(hi)",
               "max_iterations": CRITICAL_SOLVER_ITERATIONS,
               "stop": "hi-lo<=tolerance and no representable midpoint",
               "tolerance": CRITICAL_SOLVER_TOLERANCE, "returned": "lo"},
    "verification": "abs(F(l*)-1) under 64-epsilon policy; F(max(0,l*-tolerance))>=1 and "
                    "F(l*+tolerance)<1; failure reports NOT COMPUTED, never a tuned estimate",
    "statuses": {
        "NOT APPLICABLE: NO RECEPTIONS": "no recurrence",
        "NOT APPLICABLE: ALREADY-CROSSING": "actual rate already crosses",
        "NO FINITE CRITICAL RATE: SINGLETON": "single reception; state is rate-independent",
        "ABSENT: NO CROSSING AT ANY NONNEGATIVE RATE": "sum(abs(u))<1 bounds abs(z_k(l))<1",
        "NOT APPLICABLE: NO ZERO-DECAY CROSSING": "signed cancellation; no zero-decay root, "
            "no claim about other rates",
        "NOT COMPUTED: NON-MONOTONE SIGNED": "mixed signs; uniqueness unproven, no root selected",
        "ZERO-BOUNDARY": "F(0)==1 exactly; crossing only at l=0",
        "UNIQUE": "verified unique finite boundary in (0, lambda)",
        "NOT COMPUTED: VERIFICATION FAILED": "bracket/residual/perturbation check failed",
    },
}
POLICY["critical_rate"] = CRITICAL_RATE_POLICY


class Blocked(ValueError):
    """Invalid/incomplete evidence; no support-shaped fallback."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise Blocked(reason)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: Any) -> str:
    return sha(canonical(value))


def number(value: Any) -> float:
    require(type(value) in (int, float), "non-numeric value")
    result = float(value)
    require(math.isfinite(result), "non-finite value")
    return result


def bits(value: Any) -> str:
    return struct.pack(">d", number(value)).hex()


def exact(left: Any, right: Any, reason: str) -> None:
    require(canonical(left) == canonical(right), reason)


def equation(observed: Any, expected: float) -> Record:
    observed = number(observed)
    expected = number(expected)
    bound = 64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))
    residual = observed - expected
    return {"observed": observed, "expected": expected, "residual": residual,
            "bound": bound, "matches": abs(residual) <= bound}


def checked(observed: Any, expected: float, reason: str) -> Record:
    evidence = equation(observed, expected)
    require(evidence["matches"], f"recurrence mismatch: {reason}: {evidence}")
    return evidence


def _object(pairs: list[tuple[str, Any]]) -> Record:
    result: Record = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_bytes(path: Path) -> bytes:
    require(path.is_file(), f"missing required input: {path}")
    require(path.stat().st_size <= MAX_FILE_BYTES, f"file capacity exceeded: {path}")
    return path.read_bytes()


def parse(data: bytes) -> Record:
    value = json.loads(data, object_pairs_hook=_object)
    require(isinstance(value, dict), "expected JSON object")
    canonical(value)  # rejects non-finite JSON values, including nested values
    return value


def read_json(path: Path) -> Record:
    return parse(read_bytes(path))


def verify_artifact(data: bytes, identity: Record, pins: Record) -> Record:
    require(len(data) == identity["byte_length"], "artifact length differs")
    require(sha(data) == identity["file_sha256"], "artifact file hash differs")
    value = parse(data)
    body = {key: item for key, item in value.items() if key != "artifact_digest"}
    require(digest(body) == value["artifact_digest"], "internal artifact digest differs")
    if "artifact_digest" in identity:
        require(value["artifact_digest"] == identity["artifact_digest"], "catalog internal digest differs")
    for key, expected in pins.items():
        exact(value[key], expected, f"provenance pin differs: {key}")
    return value


def git(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(["git", "--no-pager", *args], cwd=root,
                          capture_output=True, check=True).stdout


def verify_integrity(root: Path = ROOT) -> Record:
    """Read-only hash/catalog/config/provenance check; NO sequence statistics."""
    catalog_bytes = read_bytes(root / L45 / "artifact-integrity.json")
    require(sha(catalog_bytes) == CATALOG_HASH, "published Luna45 catalog hash differs")
    catalog = parse(catalog_bytes)
    require(digest({k: v for k, v in catalog.items() if k != "artifact_digest"})
            == catalog["artifact_digest"], "catalog internal digest differs")
    expected_names = {"config.json", "summary.json", "initial-gates.json", "replay-gates.json"}
    for phase in ("initial", "replay"):
        for arm in ("destination_calibrated", "destination_default", "destination_disabled"):
            expected_names.update(f"{phase}-{arm}{suffix}.json" for suffix in ("", "-enqueue", "-reception"))
    require(set(catalog["files"]) == expected_names and catalog["file_count"] == 22,
            "catalog coverage differs")
    require(digest(catalog["files"]) == catalog["ordered_artifact_catalog_digest"],
            "ordered catalog digest differs")
    pins45 = {
        "runner_revision": REVISION45, "execution_revision": REVISION45,
        "config_digest": CONFIG45, "fixture_file_sha256": FIXTURE_HASH,
        "fixture_semantic_digest": FIXTURE_DIGEST, "fixture_revision": FIXTURE_REVISION,
        "fixture_manifest_revision": MANIFEST_REVISION, "fixture_manifest_sha256": MANIFEST_HASH,
        "fixture_manifest_git_blob": MANIFEST_BLOB,
        "authorization_revision": "9af6b4435ac581887f04f0951d0f7b16d7d661cd",
        "runner_sha256": "078a4fb7020414a3a017006291b778576ea72aeff08024063d7040ffe3307085",
    }
    pins44 = {
        "runner_revision": REVISION44, "execution_revision": REVISION44,
        "config_digest": CONFIG44, "fixture_revision": FIXTURE_REVISION,
        "fixture_sha256": FIXTURE_DIGEST,
        "authorization_revision": "ff4bf51dcaab2e7b66f0409f4d63a33649c3e104",
        "runner_sha256": "2bfd6341b0c2db496ad51efbf4fe6855d25f10824cac72fbd3303d4f1bc5664d",
    }
    identities: Record = {}
    total = 0
    for name, identity in catalog["files"].items():
        value = verify_artifact(read_bytes(root / L45 / name), identity, pins45)
        if name == "config.json":
            require(digest(value["experiment"]) == CONFIG45, "Luna45 config digest differs")
        identities[str(L45 / name)] = identity
        total += identity["byte_length"]
    require(total == catalog["total_bytes"], "catalog total length differs")
    for name, (length, file_hash) in HISTORY_FILES.items():
        identity = {"byte_length": length, "file_sha256": file_hash}
        value = verify_artifact(read_bytes(root / L44 / name), identity, pins44)
        if name == "config.json":
            require(digest(value["experiment"]) == CONFIG44, "Luna44 config digest differs")
        identities[str(L44 / name)] = {**identity, "artifact_digest": value["artifact_digest"]}
    for path, expected_hash in (
        (VERIFICATION, VERIFICATION_HASH),
        (Path("artifacts/luna44-canonical-fixture/provenance.json"), MANIFEST_HASH),
        (Path("artifacts/luna44-canonical-fixture/fixture.json"), FIXTURE_HASH),
    ):
        data = read_bytes(root / path)
        require(sha(data) == expected_hash, f"published evidence hash differs: {path}")
        identities[str(path)] = {"file_sha256": sha(data), "byte_length": len(data)}
    manifest = read_json(root / "artifacts/luna44-canonical-fixture/provenance.json")
    manifest_path = "artifacts/luna44-canonical-fixture/provenance.json"
    require(git("rev-parse", f"{MANIFEST_REVISION}:{manifest_path}", root=root).decode().strip()
            == MANIFEST_BLOB, "manifest Git blob differs")
    require(sha(git("show", f"{MANIFEST_REVISION}:{manifest_path}", root=root)) == MANIFEST_HASH,
            "manifest committed bytes differ")
    for source in manifest["source_files"]:
        require(sha(git("show", f"{source['revision']}:{source['path']}", root=root))
                == source["sha256"], f"retained source pin differs: {source['path']}")
    for revision, path, file_hash in (
        (REVISION45, "run_luna45_acp0008_depth2_destination_integration.py", pins45["runner_sha256"]),
        # Luna44 separately retained CRLF execution bytes and an LF Git blob.
        (REVISION44, "run_luna44_acp0008_canonical_fixture_rebaseline.py", RUNNER44_GIT_HASH),
    ):
        require(sha(git("show", f"{revision}:{path}", root=root)) == file_hash,
                "retained runner Git bytes differ")
    git("merge-base", "--is-ancestor", BASELINE, AUTHORIZATION, root=root)
    git("merge-base", "--is-ancestor", "5ebc9ae7dcaae7ff45f0769686885dcae3f2dea4", BASELINE, root=root)
    identities[str(L45 / "artifact-integrity.json")] = {
        "file_sha256": CATALOG_HASH, "byte_length": len(catalog_bytes)}
    return {"status": "PASS", "scope": "integrity/provenance only; no sequence analysis",
            "runner44_source_identity": {"git_blob_sha256": RUNNER44_GIT_HASH,
                                         "retained_execution_bytes_sha256": pins44["runner_sha256"]},
            "inputs": identities}


def distribution(values: list[float]) -> Record:
    values = [number(value) for value in values]
    ordered = sorted(values)
    def percentile(level: int) -> float | None:
        if not ordered:
            return None
        position = (len(ordered) - 1) * level / 100
        low = math.floor(position)
        high = math.ceil(position)
        return ordered[low] + (ordered[high] - ordered[low]) * (position - low)
    return {
        "count": len(values), "values": values,
        "mean": statistics.mean(values) if values else None,
        "median": statistics.median(values) if values else None,
        "min": min(values) if values else None, "max": max(values) if values else None,
        "percentiles": {str(level): percentile(level) for level in PERCENTILES},
    }


def timing(arrivals: list[Record]) -> Record:
    gaps = [number(right["timestamp"]) - number(left["timestamp"])
            for left, right in zip(arrivals, arrivals[1:])]
    require(all(gap >= 0 for gap in gaps), "arrival order decreases")
    runs: list[Record] = []
    current: list[Record] = []
    sign = 0
    def finish() -> None:
        if current:
            run_gaps = [b["timestamp"] - a["timestamp"] for a, b in zip(current, current[1:])]
            duration = current[-1]["timestamp"] - current[0]["timestamp"]
            runs.append({"sign": sign, "length": len(current), "gaps": run_gaps,
                         "duration": duration, "duration_over_tau": duration / TAU})
    for arrival in arrivals:
        payload = number(arrival["payload"])
        new_sign = (payload > 0) - (payload < 0)
        if new_sign == 0 or new_sign != sign:
            finish()
            current = []
        sign = new_sign
        if sign:
            current.append(arrival)
    finish()
    run_gaps = [gap for run in runs for gap in run["gaps"]]
    return {
        "gaps": distribution(gaps), "zero_gap_count": gaps.count(0.0),
        "positive_gaps": distribution([gap for gap in gaps if gap > 0]),
        "gap_over_tau": distribution([gap / TAU for gap in gaps]),
        "constructive_runs": runs,
        "run_lengths": distribution([float(run["length"]) for run in runs]),
        "run_gaps": distribution(run_gaps),
        "run_positive_gaps": distribution([gap for gap in run_gaps if gap > 0]),
        "run_zero_gap_count": run_gaps.count(0.0),
        "run_gaps_over_tau": distribution([gap / TAU for gap in run_gaps]),
        "zero_payload_count": sum(number(a["payload"]) == 0 for a in arrivals),
        "first_interval": "excluded from arrival gaps; use retained prior_clock for recurrence",
    }


def extrema(values: list[float]) -> Record:
    return {"min": min([0.0, *values]), "max": max([0.0, *values]),
            "max_abs": max([0.0, *(abs(value) for value in values)])}


def category(count: int, actual_crosses: bool, zero_crosses: bool, absolute_input: float) -> str:
    if not count:
        return CATEGORIES[0]
    if actual_crosses:
        return CATEGORIES[1]
    if zero_crosses:
        return CATEGORIES[2]
    if absolute_input >= THRESHOLD:
        return CATEGORIES[3]
    return CATEGORIES[4]


def signed_maximum(steps: list[tuple[float, float]], rate: float) -> float:
    """F(rate) of the declared signed equation over retained (dt, payload) updates."""
    state = 0.0
    peak = 0.0
    for dt, payload in steps:
        state = state * math.exp(-rate * dt) + payload
        peak = max(peak, abs(state))
    return peak


def critical_rate(category_name: str, steps: list[tuple[float, float]],
                  payloads: list[float]) -> Record:
    """Analytical-only critical-rate classification; never production tuning or a sweep."""
    def result(status: str, rate: float | None = None, **extra: Any) -> Record:
        return {"status": status, "critical_rate": rate,
                "reason": CRITICAL_RATE_POLICY["statuses"][status], **extra}
    if category_name == CATEGORIES[0]:
        return result("NOT APPLICABLE: NO RECEPTIONS")
    if category_name == CATEGORIES[1]:
        return result("NOT APPLICABLE: ALREADY-CROSSING")
    if len(payloads) == 1:
        return result("NO FINITE CRITICAL RATE: SINGLETON")
    if category_name == CATEGORIES[4]:
        return result("ABSENT: NO CROSSING AT ANY NONNEGATIVE RATE")
    if category_name == CATEGORIES[3]:
        return result("NOT APPLICABLE: NO ZERO-DECAY CROSSING")
    require(category_name == CATEGORIES[2], "invalid critical-rate category")
    if any(p > 0 for p in payloads) and any(p < 0 for p in payloads):
        return result("NOT COMPUTED: NON-MONOTONE SIGNED")
    low, high = signed_maximum(steps, 0.0), signed_maximum(steps, RATE)
    if not (low >= THRESHOLD > high):
        return result("NOT COMPUTED: VERIFICATION FAILED", bracket=[low, high])
    if low == THRESHOLD:
        return result("ZERO-BOUNDARY", 0.0, F_zero=low, F_lambda=high)
    lo, hi = 0.0, RATE
    iterations = 0
    while iterations < CRITICAL_SOLVER_ITERATIONS:
        middle = lo + (hi - lo) / 2
        if hi - lo <= CRITICAL_SOLVER_TOLERANCE and middle in (lo, hi):
            break
        iterations += 1
        if signed_maximum(steps, middle) >= THRESHOLD:
            lo = middle
        else:
            hi = middle
    root = lo
    below_rate = max(0.0, root - CRITICAL_SOLVER_TOLERANCE)
    above_rate = root + CRITICAL_SOLVER_TOLERANCE
    residual = equation(signed_maximum(steps, root), THRESHOLD)
    below, above = signed_maximum(steps, below_rate), signed_maximum(steps, above_rate)
    checks = {"iterations": iterations, "bracket": [lo, hi], "residual": residual,
              "below": {"rate": below_rate, "F": below, "crosses": below >= THRESHOLD},
              "above": {"rate": above_rate, "F": above, "crosses": above >= THRESHOLD}}
    if (hi - lo <= CRITICAL_SOLVER_TOLERANCE and residual["matches"]
            and checks["below"]["crosses"] and not checks["above"]["crosses"]):
        return result("UNIQUE", root, verification=checks)
    return result("NOT COMPUTED: VERIFICATION FAILED", verification=checks)


def unique(rows: list[Record], key: str) -> dict[Any, Record]:
    require(len(rows) <= MAX_EVENTS, "event capacity exceeded")
    result: dict[Any, Record] = {}
    for row in rows:
        require(row[key] not in result, f"duplicate {key}: {row[key]}")
        result[row[key]] = row
    return result


def reconcile(enqueued: list[Record], received: list[Record],
              source: str, destination: str) -> list[Record]:
    """Independent raw captures, not inferred arrivals; retain reception order."""
    admissions = unique(enqueued, "queue_sequence")
    receptions = unique(received, "queue_sequence")
    unique(enqueued, "event_id")
    unique(received, "event_id")
    require(set(admissions) == set(receptions), "missing/orphan raw capture")
    require([e["queue_sequence"] for e in enqueued] == [r["queue_sequence"] for r in received],
            "capture order differs")
    result = []
    previous: tuple[float, int] | None = None
    for row in received:
        enqueue = admissions[row["queue_sequence"]]
        require(type(row["queue_sequence"]) is int and row["queue_sequence"] >= 0,
                "invalid queue identity")
        transition = row["receiver_state_transition"]
        require(transition["processed_events_after"] == transition["processed_events_before"] + 1
                and transition["event_sequence"] == row["queue_sequence"],
                "successful receiver consumption counter/sequence differs")
        for field in ("event_id", "event_type", "source", "destination", "payload", "payload_bits",
                      "lineage_id", "originating_emission_id", "route_path", "route_depth",
                      "causal_roots", "roots_truncated"):
            exact(enqueue[field], row[field], f"raw capture identity differs: {field}")
        require(row["source"] == source and row["destination"] == destination
                and row["receiver_node"] == destination, "endpoint differs")
        require(row["event_type"] == "excursion", "capture is not a routed excursion")
        require(row["route_path"] == [source, destination] and row["route_depth"] == 1,
                "retained route path/depth differs")
        require(row["event_id"] == row["originating_emission_id"], "emission identity differs")
        require(type(row["roots_truncated"]) is bool, "invalid roots_truncated metadata")
        require(row["payload_bits"] == bits(row["payload"]), "payload bits differ")
        if "payload_encoding" in row:
            expected_encoding = {"decimal": repr(number(row["payload"])),
                                 "hex": number(row["payload"]).hex()}
            exact(row["payload_encoding"], expected_encoding, "reception payload encoding differs")
            exact(enqueue["payload_encoding"], expected_encoding, "enqueue payload encoding differs")
        timestamp = number(row["reception_timestamp"])
        require(bits(timestamp) == bits(enqueue["scheduled_delivery_timestamp"]), "arrival timestamp bits differ")
        require(timestamp > number(enqueue["enqueue_timestamp"]), "non-causal reception")
        if "scheduled_delivery_timestamp" in row:
            require(bits(timestamp) == bits(row["scheduled_delivery_timestamp"]), "reception schedule differs")
        order = (timestamp, row["queue_sequence"])
        require(previous is None or order > previous, "retained deterministic order differs")
        previous = order
        result.append({"timestamp": timestamp, "payload": number(row["payload"]),
                       "event_id": row["event_id"], "queue_sequence": row["queue_sequence"],
                       "causal_roots": row["causal_roots"], "roots_truncated": row["roots_truncated"],
                       "raw_enqueue": enqueue, "raw_reception": row})
    return result


def roots_metadata(rows: list[Record]) -> Record:
    flags = [row["roots_truncated"] for row in rows]
    require(all(type(flag) is bool for flag in flags), "invalid roots_truncated metadata")
    count = sum(flags)
    return {"receptions": len(flags), "true_count": count, "false_count": len(flags) - count,
            "true_fraction": count / len(flags) if flags else None,
            "meaning": "bounded causal-root metadata; raw capture completeness checked independently"}


def analyze_sequence(stream_id: str, arrivals: list[Record], updates: list[Record]) -> Record:
    """Synthetic or verified retained boundaries; actual updates are never skipped."""
    require(len(arrivals) <= MAX_EVENTS and len(updates) <= MAX_EVENTS, "sequence capacity exceeded")
    reception_index = unique(arrivals, "queue_sequence")
    update_index = unique(updates, "queue_sequence")
    require(set(reception_index) <= set(update_index), "reception trajectory missing")
    external = [row for row in updates if row["event_type"] == "excursion"]
    require([row["queue_sequence"] for row in external] == [row["queue_sequence"] for row in arrivals],
            "trajectory reception order/coverage differs")
    zero = 0.0
    previous_z = 0.0
    previous_time: float | None = None
    boundary_evidence: list[Record] = []
    evidence: list[Record] = []
    actual_values: list[float] = []
    zero_values: list[float] = []
    first_actual = None
    first_zero = None
    steps: list[tuple[float, float]] = []
    for update in updates:
        timestamp = number(update["timestamp"])
        prior = number(update["prior_clock"])
        require(timestamp >= prior, "negative retained interval")
        if previous_time is not None:
            require(bits(prior) == bits(previous_time), "intervening update/prior timestamp missing")
        before = number(update["z_before"])
        require(bits(before) == bits(previous_z), "retained state continuity/reset differs")
        dt = timestamp - prior
        rho = math.exp(-RATE * dt)
        pre_input = rho * previous_z
        is_reception = update["queue_sequence"] in reception_index
        payload = 0.0
        if is_reception:
            arrival = reception_index[update["queue_sequence"]]
            require(bits(timestamp) == bits(arrival["timestamp"]), "trajectory arrival timestamp differs")
            exact(update["event_id"], arrival["event_id"], "trajectory event identity differs")
            require(bits(update["payload"]) == bits(arrival["payload"]), "trajectory payload bits differ")
            payload = number(arrival["payload"])
        expected = pre_input + payload
        steps.append((dt, payload))
        actual = number(update["z_after"])
        check = checked(actual, expected, f"{stream_id}/{update['queue_sequence']}")
        require((abs(actual) >= THRESHOLD) == (abs(expected) >= THRESHOLD),
                "exact actual/expected threshold boundary differs; no threshold tolerance")
        actual_values.append(actual)
        if abs(actual) >= THRESHOLD and first_actual is None:
            first_actual = {"event_id": update["event_id"], "queue_sequence": update["queue_sequence"],
                            "timestamp": timestamp, "state": actual}
        loss = before - pre_input
        absolute_loss = abs(before) - abs(pre_input)
        if is_reception:
            zero += payload
        boundary = {
            "event_id": update["event_id"], "queue_sequence": update["queue_sequence"],
            "timestamp": timestamp, "prior_clock": prior, "dt": dt, "rho": rho,
            "state_before": before, "retained_state": pre_input, "state_after": actual,
            "signed_decay_loss": loss, "absolute_decay_loss": absolute_loss,
            "retention_ratio": None if before == 0 else abs(pre_input) / abs(before),
            "recurrence": check, "is_reception": is_reception,
            "retained_trace_checks": update.get("retained_trace_checks"),
            "zero_decay_state": zero, "signed_zero_minus_actual": zero - actual,
            "abs_zero_minus_actual": abs(zero - actual),
            "abs_excursion_difference": abs(zero) - abs(actual),
        }
        boundary_evidence.append(boundary)
        if is_reception:
            zero_values.append(zero)
            if abs(zero) >= THRESHOLD and first_zero is None:
                first_zero = {"event_id": update["event_id"], "queue_sequence": update["queue_sequence"],
                              "timestamp": timestamp, "state": zero}
            alignment = ("zero-input" if payload == 0 else "zero-reference" if pre_input == 0
                         else "constructive" if pre_input * payload > 0 else "opposing")
            cancelled = min(abs(pre_input), abs(payload)) if alignment == "opposing" else 0.0
            evidence.append({
                **boundary, "payload": payload, "zero_decay_state": zero,
                "roots_truncated": arrival["roots_truncated"],
                "causal_roots": arrival["causal_roots"],
                "signed_zero_minus_actual": zero - actual,
                "abs_zero_minus_actual": abs(zero - actual),
                "abs_excursion_difference": abs(zero) - abs(actual),
                "alignment": alignment, "cancelled_magnitude": cancelled,
                "overshoot_magnitude": max(0.0, abs(payload) - abs(pre_input)) if alignment == "opposing" else 0.0,
                "actual_crosses": abs(actual) >= THRESHOLD, "zero_crosses": abs(zero) >= THRESHOLD,
            })
        previous_z, previous_time = actual, timestamp
    absolute_input = sum(abs(number(a["payload"])) for a in arrivals)
    counts = Counter(row["alignment"] for row in evidence)
    category_name = category(len(arrivals), first_actual is not None, first_zero is not None, absolute_input)
    return {
        "stream_id": stream_id, "receptions": len(arrivals),
        "roots_truncated_metadata": roots_metadata(arrivals),
        "signed_sum": sum(number(a["payload"]) for a in arrivals),
        "total_absolute_input": absolute_input,
        "actual": extrema(actual_values), "zero_decay": extrema(zero_values),
        "maximum_retained_state": extrema([row["retained_state"] for row in boundary_evidence]),
        "maximum_abs_difference": max([0.0, *(row["abs_zero_minus_actual"] for row in boundary_evidence)]),
        "maximum_abs_excursion_difference": max([0.0, *(abs(row["abs_excursion_difference"]) for row in boundary_evidence)]),
        "actual_crosses": first_actual is not None, "zero_crosses": first_zero is not None,
        "first_actual_crossing": first_actual, "first_zero_crossing": first_zero,
        "category": category_name,
        "alignment_counts": {key: counts[key] for key in ("constructive", "opposing", "zero-reference", "zero-input")},
        "constructive_input_magnitude": sum(abs(row["payload"]) for row in evidence if row["alignment"] == "constructive"),
        "opposing_input_magnitude": sum(abs(row["payload"]) for row in evidence if row["alignment"] == "opposing"),
        "cancelled_magnitude": sum(row["cancelled_magnitude"] for row in evidence),
        "signed_decay_loss": sum(row["signed_decay_loss"] for row in boundary_evidence),
        "absolute_decay_loss": sum(row["absolute_decay_loss"] for row in boundary_evidence),
        "rho": distribution([row["rho"] for row in boundary_evidence]),
        "retention_ratio": distribution([row["retention_ratio"] for row in boundary_evidence if row["retention_ratio"] is not None]),
        "recurrence_evidence": evidence, "all_update_boundaries": boundary_evidence,
        "timing": timing(arrivals),
        "critical_rate": critical_rate(category_name, steps, [number(a["payload"]) for a in arrivals]),
    }


def verdict(counts: Record) -> Record:
    require(set(counts) == set(CATEGORIES), "invalid category inventory")
    require(all(type(value) is int and value >= 0 for value in counts.values()), "invalid category counts")
    n = sum(counts.values()) - counts[CATEGORIES[0]]
    retention = counts[CATEGORIES[2]]
    drive = counts[CATEGORIES[3]] + counts[CATEGORIES[4]]
    substantial = (n + 3) // 4
    material = (n + 9) // 10
    three_quarters = (3 * n + 3) // 4
    outcome = "BLOCKED" if n == 0 else "MIXED"
    if n and retention >= substantial and drive < material:
        outcome = "SUPPORTS TEMPORAL-RETENTION BOTTLENECK"
    elif n and drive >= three_quarters and retention < material:
        outcome = "SUPPORTS DRIVE/CANCELLATION BOTTLENECK"
    return {"verdict": outcome, "reception_bearing_N": n, "counts": counts,
            "fractions": {key: None if not n or key == CATEGORIES[0] else value / n
                          for key, value in counts.items()},
            "cutoffs": {"substantial": substantial, "material": material,
                        "drive_cancellation_support": three_quarters},
            "reason": "N=0: insufficient evidence" if not n else "predeclared exact category cutoffs",
            "efficacy": "NOT EVALUATED"}


def aggregate(sequences: list[Record]) -> Record:
    counts = {key: sum(row["category"] == key for row in sequences) for key in CATEGORIES}
    evidence = [item for row in sequences for item in row["recurrence_evidence"]]
    boundaries = [item for row in sequences for item in row["all_update_boundaries"]]
    result = verdict(counts)
    result.update({
        "sequence_count": len(sequences),
        "receptions": sum(row["receptions"] for row in sequences),
        "roots_truncated_metadata": roots_metadata(evidence),
        "sequences_with_roots_truncated": sum(
            row["roots_truncated_metadata"]["true_count"] > 0 for row in sequences),
        **{key: sum(row[key] for row in sequences) for key in (
            "signed_sum", "total_absolute_input", "constructive_input_magnitude",
            "opposing_input_magnitude", "cancelled_magnitude", "signed_decay_loss", "absolute_decay_loss")},
        "actual": extrema([item["state_after"] for item in boundaries]),
        "zero_decay": extrema([item["zero_decay_state"] for item in evidence]),
        "maximum_retained_state": extrema([item["retained_state"] for item in boundaries]),
        "maximum_abs_difference": max([0.0, *(row["maximum_abs_difference"] for row in sequences)]),
        "maximum_abs_excursion_difference": max([0.0, *(row["maximum_abs_excursion_difference"] for row in sequences)]),
        "alignment_counts": {key: sum(row["alignment_counts"][key] for row in sequences)
                             for key in ("constructive", "opposing", "zero-reference", "zero-input")},
        "actual_crossing_sequences": sum(row["actual_crosses"] for row in sequences),
        "zero_crossing_sequences": sum(row["zero_crosses"] for row in sequences),
        "rho": distribution([row["rho"] for row in boundaries]),
        "retention_ratio": distribution([row["retention_ratio"] for row in boundaries if row["retention_ratio"] is not None]),
        "timing": pooled_timing([row["timing"] for row in sequences]),
        "critical_rate_status_counts": dict(sorted(Counter(
            row["critical_rate"]["status"] for row in sequences).items())),
    })
    return result


def pooled_timing(items: list[Record]) -> Record:
    gaps = [gap for item in items for gap in item["gaps"]["values"]]
    runs = [run for item in items for run in item["constructive_runs"]]
    run_gaps = [gap for run in runs for gap in run["gaps"]]
    return {"gaps": distribution(gaps), "zero_gap_count": gaps.count(0.0),
            "positive_gaps": distribution([gap for gap in gaps if gap > 0]),
            "gap_over_tau": distribution([gap / TAU for gap in gaps]),
            "constructive_runs": runs,
            "run_lengths": distribution([float(run["length"]) for run in runs]),
            "run_gaps": distribution(run_gaps),
            "run_positive_gaps": distribution([gap for gap in run_gaps if gap > 0]),
            "run_zero_gap_count": run_gaps.count(0.0),
            "run_gaps_over_tau": distribution([gap / TAU for gap in run_gaps]),
            "zero_payload_count": sum(item["zero_payload_count"] for item in items),
            "pooling": "within-character gaps only; never bridge resets"}


def stream_metrics(streams: list[list[Record]]) -> Record:
    payloads = [number(row["payload"]) for stream in streams for row in stream]
    spans = [stream[-1]["timestamp"] - stream[0]["timestamp"] for stream in streams if len(stream) > 1]
    exposure = sum(spans)
    intervals = sum(max(0, len(stream) - 1) for stream in streams)
    return {"receptions": len(payloads),
            "roots_truncated_metadata": roots_metadata([row for stream in streams for row in stream]),
            "per_character_counts": distribution([float(len(s)) for s in streams]),
            "payloads": distribution(payloads), "absolute_payloads": distribution([abs(p) for p in payloads]),
            "signs": {"positive": sum(p > 0 for p in payloads), "negative": sum(p < 0 for p in payloads),
                      "zero": sum(p == 0 for p in payloads)},
            "interval_statistics": {
                "interval_count": intervals, "observed_duration": exposure,
                "mean_interval_duration": exposure / intervals if intervals else None,
                "reciprocal_mean_interval": intervals / exposure if exposure > 0 else None,
                "reciprocal_mean_interval_units": "intervals per retained logical-time unit",
                "definition": "within-character inter-arrival intervals divided by the summed "
                              "first-to-last arrival durations; this is reciprocal mean interval, "
                              "not an event rate over the observation window",
                "zero_or_missing_duration": "reciprocal mean interval is null; no zero is imputed",
            },
            "timing": pooled_timing([timing(stream) for stream in streams])}


def depth_comparison(first: list[list[Record]], second: list[list[Record]],
                     fairness: Record, fixture_exposures: list[float] | None = None) -> Record:
    fair = all(fairness.values()) and bool(fairness)
    upstream, downstream = stream_metrics(first), stream_metrics(second)
    common_exposure = None
    if fixture_exposures is not None:
        require(len(fixture_exposures) == len(first) == len(second), "depth exposure inventory differs")
        require(all(number(span) >= 0 for span in fixture_exposures), "negative fixture exposure")
        common_exposure = sum(fixture_exposures)
    for metrics in (upstream, downstream):
        metrics["common_fixture_event_rate"] = {
            "event_count": metrics["receptions"],
            "observation_window_duration": common_exposure,
            "events_per_time_unit": metrics["receptions"] / common_exposure
            if common_exposure is not None and common_exposure > 0 else None,
            "units": "routed receptions per retained logical-time unit",
            "definition": "routed reception count / sum(last-first frozen point timestamp) "
                          "over matched characters",
            "zero_or_missing_exposure": "event rate is null; no zero is imputed",
        }
    return {"fair": fair, "matching_checks": fairness,
            "limitation": "different hop exposure; not identical layer statistics" if fair
                          else "unfair/missing fixture, sequence, reset, phase or capture match; descriptive only",
            "first_hop": upstream, "second_hop": downstream,
            "differences": {"receptions": downstream["receptions"] - upstream["receptions"],
                            "mean_run_length": None if upstream["timing"]["run_lengths"]["mean"] is None
                            or downstream["timing"]["run_lengths"]["mean"] is None else
                            downstream["timing"]["run_lengths"]["mean"] - upstream["timing"]["run_lengths"]["mean"]},
            "interpretation": "mechanism-only depth description; no efficacy or tuning recommendation"}


def phase_bytes(artifact: Record, config: Record) -> bytes:
    return canonical({"fixture_file_sha256": FIXTURE_HASH, "fixture_semantic_digest": FIXTURE_DIGEST,
                      "config": config, "records": artifact["records"], "per_arm_report": artifact["report"]})


def verify_phase_pair(initial: Record, replay: Record, config: Record, summary: Record, arm: str) -> Record:
    for phase, artifact in (("initial", initial), ("replay", replay)):
        require(artifact["phase"] == phase and artifact["arm"] == arm and artifact["blocker"] is None,
                "phase identity/blocker differs")
        require(sha(phase_bytes(artifact, config)) == artifact["phase_digest"]
                == summary[f"{phase}_digests"][arm], "phase internal digest differs")
    first, second = phase_bytes(initial, config), phase_bytes(replay, config)
    require(first == second, "canonical replay bytes differ")
    return {"canonical_bytes_equal": True, "sha256": sha(first), "byte_length": len(first)}


def select_raw(raw: Record, records: list[Record], phase: str, stream: str,
               arm: str) -> list[list[Record]]:
    require(raw["phase"] == phase and raw["capture_stream"] == stream, "raw phase/stream differs")
    if "per_sequence" in raw:
        require(raw["arm"] == arm, "raw arm differs")
        rows = raw["per_sequence"]
    else:
        rows = raw["per_arm"][arm]
    require(len(rows) == len(records), "raw sequence inventory differs")
    unique(rows, "stream_id")
    field = "routing_enqueue_events" if stream == "enqueue" else "receiver_reception_events"
    result = []
    for row, record in zip(rows, records):
        exact(row["stream_id"], record["stream_id"], "raw sequence identity/order differs")
        exact(row["events"], record[field], "raw capture differs from retained records")
        if "stream_digest" in row:
            require(digest(row["events"]) == row["stream_digest"], "raw stream internal digest differs")
            require(row["capture_status"] == "completed", "incomplete raw capture")
            exact([row["seed"], row["sequence_index"]], [record["seed"], record["sequence_index"]],
                  "raw seed/sequence differs")
        result.append(row["events"])
    if "streams_digest" in raw:
        require(digest(raw["per_arm"]) == raw["streams_digest"], "raw aggregate digest differs")
    return result


def destination_updates(record: Record, arrivals: list[Record]) -> list[Record]:
    trajectory = [dict(row) for row in record["destination_state_trajectory"]]
    external = [row for row in trajectory if row["event_type"] == "excursion"]
    traces = record["destination_integration_trace"]
    evidence = record["destination_evidence"]
    require(len(external) == len(traces) == len(evidence) == len(arrivals),
            "destination trace/evidence inventory differs")
    for captured, trace, retained, arrival in zip(external, traces, evidence, arrivals):
        require(bits(trace["timestamp"]) == bits(captured["timestamp"])
                and bits(trace["input_value"]) == bits(captured["payload"])
                and bits(trace["elapsed"]) == bits(captured["timestamp"] - captured["prior_clock"]),
                "trace timestamp/payload/elapsed differs")
        require(bits(trace["z_before_decay"]) == bits(captured["z_before"])
                and bits(retained["z_before_decay"]) == bits(captured["z_before"])
                and bits(retained["elapsed"]) == bits(trace["elapsed"]),
                "copied prior state/elapsed bits differ")
        require(trace["mode_before"] == captured["mode_before"] == "N" and trace["integrated"] is True,
                "non-integrating reception boundary: BLOCKED")
        for key, value in (("theta_e", 1.0), ("theta_z", THRESHOLD),
                           ("decay_rate", 1.0), ("decay_rate_z", RATE)):
            require(bits(trace[key]) == bits(value), f"trace configuration differs: {key}")
        exact(retained["actual_reception"], arrival["raw_reception"], "retained actual reception differs")
        exact(retained["queue_admission"], arrival["raw_enqueue"], "retained queue admission differs")
        require(retained["stream_id"] == record["stream_id"], "evidence stream differs")
        require(bits(retained["arrival_timestamp"]) == bits(arrival["timestamp"])
                and bits(retained["routed_contribution"]) == bits(arrival["payload"]),
                "evidence arrival/payload differs")
        require(number(trace["discharge_amount"]) == number(retained["discharge_amount"]) == 0
                and retained["discharge_decision"] is False and retained["discharge_sign"] == 0,
                "discharge boundary present: BLOCKED")
        before = number(captured["z_before"])
        dt = captured["timestamp"] - captured["prior_clock"]
        pre = before * math.exp(-RATE * dt)
        after = pre + number(captured["payload"])
        require(abs(after) <= 4.0, "clipping boundary present: BLOCKED")
        require(abs(number(trace["x_after_input"])) < 1, "fast direct-admission boundary: BLOCKED")
        trace_checks = {}
        for field, expected in (("z_before_decay", before), ("z_after_decay", pre),
                                ("z_after_input", after), ("z_post_discharge", after)):
            trace_checks[f"trace.{field}"] = checked(trace[field], expected, f"trace {field}")
        for field, expected in (("z_before_decay", before), ("elapsed", dt),
                                ("z_after_decay", pre), ("z_after_contribution", after),
                                ("resulting_z", after)):
            trace_checks[f"evidence.{field}"] = checked(retained[field], expected, f"evidence {field}")
        require(bits(captured["z_before"]) == bits(arrival["raw_reception"]["receiver_state_transition"]["z_before"])
                and bits(captured["z_after"]) == bits(arrival["raw_reception"]["receiver_state_transition"]["z_after"]),
                "actual receiver state differs from trajectory")
        require(bits(trace["z_post_discharge"]) == bits(captured["z_after"])
                and bits(retained["resulting_z"]) == bits(captured["z_after"]),
                "copied resulting state bits differ")
        captured["retained_trace_checks"] = trace_checks
    return trajectory


def validate_config(config45: Record, config44: Record) -> Record:
    require(digest(config45) == CONFIG45 and digest(config44) == CONFIG44, "frozen configuration changed")
    target = config45["neuron_configurations"][CALIBRATED]["destination"]
    exact(target["integration"], {"decay_rate_z": RATE, "discharge_quantum": THRESHOLD,
                                 "input_gain": 1.0, "z_max": 4.0}, "destination integration config differs")
    require(target["theta_e"] == 1.0 and 1 / RATE == TAU and config45["structural_plasticity"] is False,
            "threshold/tau/structural configuration differs")
    return config45


def execution_identity(root: Path = ROOT) -> Record:
    revision = git("rev-parse", "HEAD", root=root).decode().strip()
    require(git("branch", "--show-current", root=root).decode().strip() == BRANCH, "analysis branch differs")
    require(not git("status", "--porcelain=v1", root=root), "analysis requires clean worktree")
    published = git("ls-remote", "origin", f"refs/heads/{BRANCH}", root=root).decode().split()
    require(bool(published) and published[0] == revision and revision != AUTHORIZATION,
            "implementation must be pushed before retained analysis")
    git("merge-base", "--is-ancestor", AUTHORIZATION, revision, root=root)
    source = read_bytes(root / Path(__file__).name)
    require(source == git("show", f"{revision}:{Path(__file__).name}", root=root),
            "analyzer must be committed unchanged before analysis")
    return {"revision": revision, "sha256": sha(source), "module": Path(__file__).name}


def offline_analysis(root: Path = ROOT) -> Record:
    code_identity = execution_identity(root)
    integrity = verify_integrity(root)
    def load(path: Path) -> Record:
        return verify_artifact(read_bytes(root / path), integrity["inputs"][str(path)], {})
    config45 = load(L45 / "config.json")["experiment"]
    config44 = load(L44 / "config.json")["experiment"]
    validate_config(config45, config44)
    summary = load(L45 / "summary.json")
    require(summary["status"] == "PASS" and summary["verdict"] == "NOT SUPPORTED IN THIS SETUP"
            and summary["replay_equal"] is True and summary["initial_blocker"] is None
            and summary["replay_blocker"] is None, "prior Luna45 disposition/replay differs")
    replay_checks = {}
    for arm in ("DESTINATION_DISABLED", "DESTINATION_DEFAULT", CALIBRATED):
        initial = load(L45 / f"initial-{arm.lower()}.json")
        replay = load(L45 / f"replay-{arm.lower()}.json")
        replay_checks[arm] = verify_phase_pair(initial, replay, config45, summary, arm)
    historical = load(L44 / "results.json")["runs"]["CALIBRATED"]
    require(len(historical) == MAX_SEQUENCES, "Luna44 sequence inventory incomplete")
    for record in historical:
        require(digest({k: v for k, v in record.items() if k != "record_digest"})
                == record["record_digest"], "historical record digest differs")
    first_streams: list[list[Record]] = []
    second_streams: list[list[Record]] = []
    fixture_exposures: list[float] = []
    phase_results: dict[str, list[Record]] = {}
    fairness = {"fixture": canonical(config45["fixture"]) == canonical(config44["fixture"]),
                "runtime_reset_semantics": canonical(config45["runtime"]) == canonical(config44["runtime"]),
                "sequence_identity": True, "phase": True, "capture_semantics": True}
    for phase in ("initial", "replay"):
        records = load(L45 / f"{phase}-destination_calibrated.json")["records"]
        require(len(records) == MAX_SEQUENCES, "Luna45 sequence inventory incomplete")
        unique(records, "stream_id")
        expected_order = [f"c{seed:02d}-{index:03d}" for seed in range(5) for index in range(64)]
        exact([r["stream_id"] for r in records], expected_order, "sequence order differs")
        enqueues = select_raw(load(L45 / f"{phase}-destination_calibrated-enqueue.json"),
                              records, phase, "enqueue", CALIBRATED)
        receptions = select_raw(load(L45 / f"{phase}-destination_calibrated-reception.json"),
                                records, phase, "reception", CALIBRATED)
        hist_enqueues = select_raw(load(L44 / f"routing-{phase}-enqueue.json"),
                                  historical, phase, "enqueue", "CALIBRATED")
        hist_receptions = select_raw(load(L44 / f"routing-{phase}-reception.json"),
                                    historical, phase, "reception", "CALIBRATED")
        results = []
        for index, record in enumerate(records):
            prior = historical[index]
            for field in ("stream_id", "seed", "sequence_index", "fixture_sequence_sha256",
                          "raw_identity", "raw_identity_sha256", "input_digest"):
                fairness["sequence_identity"] &= canonical(record[field]) == canonical(prior[field])
            fairness["runtime_reset_semantics"] &= (
                record["settling"]["completed"] is True and prior["settling"]["completed"] is True)
            for node in ("relay", "destination"):
                observations = record[f"{node}_state_trajectory"]
                if observations:
                    fairness["runtime_reset_semantics"] &= number(observations[0]["z_before"]) == 0
            if prior["relay_state_trajectory"]:
                fairness["runtime_reset_semantics"] &= number(prior["relay_state_trajectory"][0]["z_before"]) == 0
            fairness["capture_semantics"] &= (
                canonical(record["routing_capture_sources"]) == canonical(prior["routing_capture_sources"]))
            require(record["arm"] == CALIBRATED and record["destination_decay_rate_z"] == RATE,
                    "calibrated record config differs")
            unique(enqueues[index], "queue_sequence")
            unique(receptions[index], "queue_sequence")
            unique(hist_enqueues[index], "queue_sequence")
            unique(hist_receptions[index], "queue_sequence")
            exact(record["neuron_configuration"]["destination"],
                  config45["neuron_configurations"][CALIBRATED]["destination"], "record node config differs")
            def hop(rows: list[Record], source: str, destination: str) -> list[Record]:
                return [row for row in rows if row["source"] == source and row["destination"] == destination]
            require(all((r["source"], r["destination"]) in (("source", "relay"), ("relay", "destination"))
                        for r in enqueues[index] + receptions[index]), "unexpected routing endpoint")
            arrivals = reconcile(hop(enqueues[index], "relay", "destination"),
                                 hop(receptions[index], "relay", "destination"), "relay", "destination")
            reconcile(hop(enqueues[index], "source", "relay"),
                      hop(receptions[index], "source", "relay"), "source", "relay")
            first = reconcile(hop(hist_enqueues[index], "source", "relay"),
                              hop(hist_receptions[index], "source", "relay"), "source", "relay")
            exact(record["destination_receptions"],
                  [a["raw_reception"] for a in arrivals], "successful destination reception coverage differs")
            relay_emissions = unique(record["relay_emissions"], "event_id")
            for arrival in arrivals:
                require(arrival["event_id"] in relay_emissions, "relay emission origin missing")
                retained_emission = relay_emissions[arrival["event_id"]]
                require(bits(arrival["raw_enqueue"]["enqueue_timestamp"]) == bits(retained_emission["timestamp"]),
                        "relay emission timestamp differs")
                require(retained_emission["source"] == "relay"
                        and retained_emission["lineage_id"] == arrival["raw_enqueue"]["lineage_id"],
                        "relay emission source/lineage differs")
                checked(arrival["payload"], math.tanh(number(retained_emission["payload"])),
                        "retained fixed-w=1 Model-B transfer")
            results.append(analyze_sequence(record["stream_id"], arrivals, destination_updates(record, arrivals)))
            if phase == "initial":
                first_streams.append(first)
                second_streams.append(arrivals)
                point_times = [float.fromhex(point["t"]["hex"]) for point in record["point_inputs"]]
                require(bool(point_times) and all(math.isfinite(t) for t in point_times)
                        and all(b >= a for a, b in zip(point_times, point_times[1:])),
                        "frozen point exposure timestamps invalid")
                fixture_exposures.append(point_times[-1] - point_times[0])
        phase_results[phase] = results
    exact(phase_results["initial"], phase_results["replay"], "analytical replay bytes differ")
    results = phase_results["initial"]
    result = {
        "schema": "TPCN-LUNA46-OFFLINE-1", "classification": "OFFLINE MECHANISM DIAGNOSTIC / VERIFICATION",
        "authorization_revision": AUTHORIZATION, "baseline": BASELINE,
        "code": code_identity,
        "environment": {"python": sys.version, "implementation": sys.implementation.name,
                        "platform": platform.platform(), "epsilon": sys.float_info.epsilon},
        "integrity": integrity, "policy": POLICY, "frozen_configuration": config45,
        "replay": {"retained_phase_bytes": replay_checks, "analytical_bytes_equal": True,
                   "analytical_sha256": digest(results)},
        "sequences": results, "aggregate": aggregate(results),
        "depth_comparison": depth_comparison(first_streams, second_streams, fairness, fixture_exposures),
        "preserves": {"Luna42": "PASS WITH FOLLOW-UP", "Luna43": "BLOCKED / DESTINATION COMPARISON UNDETERMINED",
                      "Luna44": "reviewed canonical-fixture relay-propagation baseline",
                      "Luna45": "NOT SUPPORTED IN THIS SETUP",
                      "ACP0007": "unchanged/disabled", "ACP0008": "experimental/opt-in/unpromoted"},
        "feedback": "NONE; downstream only", "efficacy": "NOT EVALUATED",
        "critical_rate": POLICY["critical_rate"],
    }
    result["verdict"] = result["aggregate"]["verdict"]
    result["output_digest"] = digest(result)
    return result


def validate_output_path(output: Path, root: Path | None = None) -> Path:
    """Canonical (symlink/junction-resolving) output guard; no string-prefix checks.

    Rejects any tree overlap in either direction with retained evidence or the
    frozen fixture root, then requires the artifacts/luna46-* namespace.
    """
    root = ROOT if root is None else root
    resolved = Path(output).resolve()
    protected = {"Luna45 evidence": root / L45, "Luna44 evidence": root / L44,
                 "Luna45 verification": root / VERIFICATION.parent,
                 "frozen Luna44 fixture": root / FIXTURE_ROOT}
    for name, directory in protected.items():
        tree = directory.resolve()
        require(not (resolved == tree or tree in resolved.parents or resolved in tree.parents),
                f"output overlaps {name} tree: {resolved}")
    namespace = (root / "artifacts").resolve()
    require(namespace in resolved.parents, f"output outside artifacts/{OUTPUT_NAMESPACE}*: {resolved}")
    require(resolved.relative_to(namespace).parts[0].startswith(OUTPUT_NAMESPACE),
            f"output outside artifacts/{OUTPUT_NAMESPACE}*: {resolved}")
    return resolved


def write_output(path: Path, result: Record) -> None:
    require(not path.exists(), f"refusing overwrite: {path}")
    payload = canonical(result) + b"\n"
    with path.open("xb") as stream:
        stream.write(payload)
    require(path.read_bytes() == payload, "output readback differs")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="new diagnostic JSON file (never overwrite)")
    args = parser.parse_args(argv)
    try:
        require(not os.path.lexists(args.output), f"refusing overwrite: {args.output}")
        validate_output_path(args.output)
        require(args.output.parent.is_dir(), "output parent directory missing")
        result = offline_analysis()
        require(result["verdict"] != "BLOCKED", result["aggregate"]["reason"])
        write_output(args.output, result)
    except (Blocked, OSError, KeyError, TypeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"BLOCKED: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(f"{result['verdict']}: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
