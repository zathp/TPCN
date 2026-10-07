"""Fixed, bounded Luna-47A offline replay. Run as python -m experiments.luna47a.run."""
from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal, localcontext
import math
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

import run_luna46_depth_scaling_diagnostic as evidence

ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION = "789dda5988daf72f375d9713bd76a6da2b9e8b34"
BASELINE = "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
BRANCH = "copilot/luna47a-investigation"
RETAINED = Path("artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json")
RETAINED_HASH = "54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51"
RETAINED_BYTES = 2337376
CONFIG = {
    "schema": "TPCN-LUNA47A-CONFIG-1",
    "rates": {"baseline_tau80": 0.0125, "retention_tau800": 0.00125,
              "retention_tau8000": 0.000125},
    "state_cap": 4.0, "threshold": 1.0, "input_gain": 1.0,
    "baseline_estimation": "frozen zero reference",
    "qualification": "identity; exact frozen signed admitted payload",
    "reset": "state=clock=0 per character",
    "output": "none; no discharge; crossing is not emission",
    "max_time": 1e12, "max_payload": 1e6, "max_events": 4096,
    "max_streams": 320, "max_file_bytes": 100 * 1024 * 1024,
    "equation_tolerance": "64*epsilon*max(1,abs(observed),abs(expected))",
    "threshold_tolerance": 0, "replay": "exact canonical bytes",
}
Record = dict[str, Any]
require = evidence.require


def finite(value: Any, lower: float, upper: float, name: str) -> float:
    require(type(value) in (float, int), f"{name}: numeric scalar required")
    result = float(value)
    require(math.isfinite(result) and lower <= result <= upper, f"{name}: outside domain")
    return result


def step(previous: float, dt: float, payload: float, rate: float) -> Record:
    """Continuous relaxation then unit-gain deposition and unchanged cap."""
    previous = finite(previous, -4, 4, "state")
    dt = finite(dt, 0, CONFIG["max_time"], "elapsed")
    payload = finite(payload, -CONFIG["max_payload"], CONFIG["max_payload"], "payload")
    require(rate in CONFIG["rates"].values(), "undeclared rate")
    rho = math.exp(-rate * dt)
    retained = previous * rho
    unbounded = retained + payload
    after = min(4.0, max(-4.0, unbounded))
    return {"state_before": previous, "dt": dt, "rho": rho, "retained_state": retained,
            "payload": payload, "unclipped": unbounded, "state_after": after,
            "clipped": after != unbounded, "signed_decay_loss": previous - retained,
            "absolute_decay_loss": abs(previous) - abs(retained),
            "positive_boundary_margin": after - 1.0, "negative_boundary_margin": -after - 1.0,
            "threshold_margin": abs(after) - 1.0,
            "crosses": abs(after) >= 1.0}


def accumulate(updates: list[Record], rate: float) -> Record:
    require(len(updates) <= CONFIG["max_events"], "event capacity")
    state, clock = 0.0, None
    last_key: tuple[float, int] | None = None
    ids: set[int] = set()
    rows = []
    first = None
    for update in updates:
        t = finite(update["timestamp"], 0, CONFIG["max_time"], "timestamp")
        prior = finite(update["prior_clock"], 0, CONFIG["max_time"], "prior clock")
        queue = update["queue_sequence"]
        require(type(queue) is int and queue >= 0 and queue not in ids, "duplicate/invalid queue")
        ids.add(queue)
        key = (t, queue)
        require(last_key is None or key > last_key, "event order")
        if clock is None:
            clock = prior
        require(evidence.bits(prior) == evidence.bits(clock) and t >= prior, "clock continuity")
        payload = update["payload"] if update["is_reception"] else 0.0
        row = step(state, t - prior, payload, rate)
        row.update({k: update[k] for k in
                    ("timestamp", "prior_clock", "queue_sequence", "event_id", "is_reception")})
        if row["crosses"] and first is None:
            first = {k: row[k] for k in ("timestamp", "queue_sequence", "event_id", "state_after")}
        rows.append(row)
        state, clock, last_key = row["state_after"], t, key
    values = [r["state_after"] for r in rows]
    return {"rows": rows, "crosses": first is not None, "first_crossing": first,
            "minimum_signed_state": min(values, default=0.0),
            "maximum_signed_state": max(values, default=0.0),
            "maximum_absolute_state": max(map(abs, values), default=0.0),
            "clipped_events": sum(r["clipped"] for r in rows)}


def compare(stream: Record) -> Record:
    variants = {name: accumulate(stream["updates"], rate)
                for name, rate in CONFIG["rates"].items()}
    baseline = variants["baseline_tau80"]
    for name, result in variants.items():
        for row, reference in zip(result["rows"], baseline["rows"]):
            row["baseline_state_after"] = reference["state_after"]
            row["difference_from_baseline"] = row["state_after"] - reference["state_after"]
        result["changed_state_events"] = sum(
            evidence.bits(r["state_after"]) != evidence.bits(b["state_after"])
            for r, b in zip(result["rows"], baseline["rows"]))
        result["changed_crossing_events"] = sum(
            r["crosses"] != b["crosses"] for r, b in zip(result["rows"], baseline["rows"]))
    return {"stream_id": stream["stream_id"], "original_category": stream.get("category"),
            "receptions": sum(u["is_reception"] for u in stream["updates"]), "variants": variants}


def classify(retention_count: int, rescues: list[int], drive_crossings: int,
             gate: bool = True) -> str:
    if not gate or retention_count <= 0 or drive_crossings:
        return "BLOCKED"
    if max(rescues, default=0) == retention_count:
        return "SUPPORTED"
    if any(rescues):
        return "PARTIALLY SUPPORTED"
    return "NOT SUPPORTED"


def summarize(results: list[Record], primary: bool) -> Record:
    summary: Record = {}
    for name in CONFIG["rates"]:
        entries = [(r, r["variants"][name]) for r in results]
        rescued = [r["stream_id"] for r, v in entries
                   if r["original_category"] == "TEMPORAL-RETENTION-LIMITED" and v["crosses"]]
        summary[name] = {
            "crossing_streams": sum(v["crosses"] for _, v in entries),
            "rescued_retention_ids": rescued, "rescued_retention_count": len(rescued),
            "unrescued_retention_ids": [r["stream_id"] for r, v in entries
                                       if r["original_category"] == "TEMPORAL-RETENTION-LIMITED"
                                       and not v["crosses"]],
            "drive_crossing_ids": [r["stream_id"] for r, v in entries
                                  if r["original_category"] == "DRIVE-LIMITED" and v["crosses"]],
            "drive_remaining_ids": [r["stream_id"] for r, v in entries
                                   if r["original_category"] == "DRIVE-LIMITED" and not v["crosses"]],
            "clipped_events": sum(v["clipped_events"] for _, v in entries),
            "changed_state_events": sum(v["changed_state_events"] for _, v in entries),
            "changed_crossing_events": sum(v["changed_crossing_events"] for _, v in entries),
            "changed_crossing_streams": sum(
                v["crosses"] != r["variants"]["baseline_tau80"]["crosses"] for r, v in entries),
            "maximum_absolute_state": max((v["maximum_absolute_state"] for _, v in entries), default=0),
        }
    if primary:
        observed = Counter(r["original_category"] for r in results)
        counts = {category: observed[category] for category in evidence.CATEGORIES}
        variants = [summary[n] for n in CONFIG["rates"] if n != "baseline_tau80"]
        summary["original_categories"] = counts
        summary["retention_union_ids"] = sorted(set().union(
            *(set(v["rescued_retention_ids"]) for v in variants)))
        summary["verdict"] = classify(
            counts.get("TEMPORAL-RETENTION-LIMITED", 0),
            [v["rescued_retention_count"] for v in variants],
            sum(len(v["drive_crossing_ids"]) for v in variants),
            not any(summary[n]["clipped_events"] for n in CONFIG["rates"]),
        )
    return summary


def hop(rows: list[Record], source: str, destination: str) -> list[Record]:
    return [r for r in rows if (r["source"], r["destination"]) == (source, destination)]


def historical_updates(arrivals: list[Record]) -> list[Record]:
    prior = 0.0
    result = []
    for row in arrivals:
        result.append({k: row[k] for k in ("timestamp", "queue_sequence", "event_id", "payload")})
        result[-1].update({"prior_clock": prior, "is_reception": True})
        prior = row["timestamp"]
    return result


def verify_retained(data: bytes, committed: bytes) -> Record:
    require(len(data) == RETAINED_BYTES and evidence.sha(data) == RETAINED_HASH, "Luna46 file pin")
    require(data == committed, "retained working bytes differ from evidence baseline")
    value = evidence.parse(data)
    require(evidence.digest({k: v for k, v in value.items() if k != "output_digest"})
            == value["output_digest"], "Luna46 internal digest")
    require(value["verdict"] == "MIXED", "preserve MIXED")
    require(value["replay"]["analytical_bytes_equal"] is True, "retained replay gate")
    require(len(value["sequences"]) == CONFIG["max_streams"], "Luna46 inventory")
    return value


def materialization_check(physical: bytes, committed: bytes) -> Record:
    require(physical == committed or physical.replace(b"\r\n", b"\n") == committed,
            "checkout bytes differ beyond exact CRLF materialization")
    return {"physical_sha256": evidence.sha(physical), "physical_byte_length": len(physical),
            "git_sha256": evidence.sha(committed), "git_byte_length": len(committed),
            "physical_equals_git": physical == committed,
            "exact_lf_crlf_equivalence": physical.replace(b"\r\n", b"\n") == committed}


def materialize_evidence() -> tuple[Path, Record]:
    """Exact baseline Git bytes, never repairs historical checkout files."""
    names = [evidence.L45 / "artifact-integrity.json", RETAINED]
    for phase in ("initial", "replay"):
        names.append(evidence.L45 / f"{phase}-gates.json")
        for arm in ("destination_calibrated", "destination_default", "destination_disabled"):
            names.extend(evidence.L45 / f"{phase}-{arm}{suffix}.json"
                         for suffix in ("", "-enqueue", "-reception"))
    names.extend(evidence.L45 / name for name in ("config.json", "summary.json"))
    names.extend(evidence.L44 / name for name in evidence.HISTORY_FILES)
    names.extend((evidence.VERIFICATION, Path("artifacts/luna44-canonical-fixture/provenance.json"),
                  Path("artifacts/luna44-canonical-fixture/fixture.json")))
    cache = ROOT / "experiments/luna47a/_evidence"
    require(cache.resolve() == cache.absolute(), "aliased evidence cache")
    observations = {}
    for name in names:
        committed = evidence.git("show", f"{BASELINE}:{name.as_posix()}", root=ROOT)
        observations[name.as_posix()] = materialization_check((ROOT / name).read_bytes(), committed)
        target = cache / name
        require(cache in target.resolve().parents, "cache alias escape")
        if target.exists():
            require(target.read_bytes() == committed, "cached authoritative bytes changed")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(committed)
    return cache, observations


def physical_inventory(observations: Record) -> Record:
    return {name: {"sha256": evidence.sha((ROOT / name).read_bytes()),
                   "byte_length": (ROOT / name).stat().st_size} for name in observations}


def verified_inputs() -> Record:
    """Read reviewed evidence only; never invoke a production runner."""
    source_root, materialization = materialize_evidence()
    integrity = evidence.verify_integrity(source_root)
    retained = verify_retained(evidence.read_bytes(source_root / RETAINED),
                              evidence.git("show", f"{BASELINE}:{RETAINED.as_posix()}", root=ROOT))

    def load(path: Path) -> Record:
        return evidence.verify_artifact(evidence.read_bytes(source_root / path),
                                        integrity["inputs"][str(path)], {})

    config45 = load(evidence.L45 / "config.json")["experiment"]
    config44 = load(evidence.L44 / "config.json")["experiment"]
    evidence.validate_config(config45, config44)
    evidence.exact(config45, retained["frozen_configuration"], "retained config")
    summary45 = load(evidence.L45 / "summary.json")
    phase_gates = {}
    for arm in ("DESTINATION_DISABLED", "DESTINATION_DEFAULT", evidence.CALIBRATED):
        phase_gates[arm] = evidence.verify_phase_pair(
            load(evidence.L45 / f"initial-{arm.lower()}.json"),
            load(evidence.L45 / f"replay-{arm.lower()}.json"), config45, summary45, arm)
    historical = load(evidence.L44 / "results.json")["runs"]["CALIBRATED"]
    require(len(historical) == CONFIG["max_streams"], "historical inventory")
    for record in historical:
        require(evidence.digest({k: v for k, v in record.items() if k != "record_digest"})
                == record["record_digest"], "historical record digest")
    phases = {}
    expected_order = [f"c{seed:02d}-{index:03d}" for seed in range(5) for index in range(64)]
    route_counts = {}
    for phase in ("initial", "replay"):
        records = load(evidence.L45 / f"{phase}-destination_calibrated.json")["records"]
        require(len(records) == CONFIG["max_streams"], "primary inventory")
        evidence.exact([r["stream_id"] for r in records], expected_order, "primary order")
        enqueues = evidence.select_raw(
            load(evidence.L45 / f"{phase}-destination_calibrated-enqueue.json"),
            records, phase, "enqueue", evidence.CALIBRATED)
        receives = evidence.select_raw(
            load(evidence.L45 / f"{phase}-destination_calibrated-reception.json"),
            records, phase, "reception", evidence.CALIBRATED)
        hist_enqueues = evidence.select_raw(load(evidence.L44 / f"routing-{phase}-enqueue.json"),
                                           historical, phase, "enqueue", "CALIBRATED")
        hist_receives = evidence.select_raw(load(evidence.L44 / f"routing-{phase}-reception.json"),
                                           historical, phase, "reception", "CALIBRATED")
        primary, outside, reconstructions = [], [], []
        second_count, first_count = 0, 0
        for index, record in enumerate(records):
            prior = historical[index]
            for field in ("stream_id", "seed", "sequence_index", "fixture_sequence_sha256",
                          "raw_identity", "raw_identity_sha256", "input_digest"):
                evidence.exact(record[field], prior[field], f"matched historical identity {field}")
            require(record["settling"]["completed"] and prior["settling"]["completed"],
                    "incomplete settling")
            evidence.exact(record["neuron_configuration"]["destination"],
                           config45["neuron_configurations"][evidence.CALIBRATED]["destination"],
                           "node configuration")
            require(record["arm"] == evidence.CALIBRATED
                    and record["destination_decay_rate_z"] == 0.0125, "arm/rate")
            for rows in (enqueues[index], receives[index]):
                require(all((r["source"], r["destination"]) in
                            (("source", "relay"), ("relay", "destination")) for r in rows),
                        "unexpected route")
                evidence.unique(rows, "queue_sequence")
            arrivals = evidence.reconcile(hop(enqueues[index], "relay", "destination"),
                                          hop(receives[index], "relay", "destination"),
                                          "relay", "destination")
            first = evidence.reconcile(hop(enqueues[index], "source", "relay"),
                                       hop(receives[index], "source", "relay"), "source", "relay")
            hist_arrivals = evidence.reconcile(hop(hist_enqueues[index], "source", "relay"),
                                              hop(hist_receives[index], "source", "relay"),
                                              "source", "relay")
            evidence.exact(record["destination_receptions"], [a["raw_reception"] for a in arrivals],
                           "destination coverage")
            emissions = evidence.unique(record["relay_emissions"], "event_id")
            for arrival in arrivals:
                require(arrival["event_id"] in emissions, "emission origin")
                emission = emissions[arrival["event_id"]]
                require(evidence.bits(emission["timestamp"]) ==
                        evidence.bits(arrival["raw_enqueue"]["enqueue_timestamp"]), "emission time")
                require(emission["source"] == "relay" and emission["lineage_id"] ==
                        arrival["raw_enqueue"]["lineage_id"], "emission lineage")
                evidence.checked(arrival["payload"], math.tanh(evidence.number(emission["payload"])),
                                 "fixed-w=1 transfer")
            updates = evidence.destination_updates(record, arrivals)
            reconstructed = evidence.analyze_sequence(record["stream_id"], arrivals, updates)
            evidence.exact(reconstructed, retained["sequences"][index], "reviewed Luna46 recurrence")
            boundaries = reconstructed["all_update_boundaries"]
            reception_map = {r["queue_sequence"]: r for r in arrivals}
            stream_updates = [
                {**{k: u[k] for k in ("timestamp", "prior_clock", "queue_sequence", "event_id",
                                     "is_reception")},
                 "payload": reception_map[u["queue_sequence"]]["payload"] if u["is_reception"] else 0.0,
                 "actual_state_after": u["state_after"],
                 "actual_retained_state": u["retained_state"]}
                for u in boundaries]
            identity = {k: record[k] for k in ("stream_id", "seed", "sequence_index",
                                             "fixture_sequence_sha256", "raw_identity",
                                             "raw_identity_sha256", "input_digest")}
            primary.append({**identity, "category": reconstructed["category"],
                            "updates": stream_updates, "raw_arrivals": arrivals})
            outside.append({**identity, "updates": historical_updates(hist_arrivals),
                            "raw_arrivals": hist_arrivals,
                            "historical_canonical_emissions": len(prior["relay_emissions"])})
            reconstructions.append(reconstructed)
            second_count += len(arrivals)
            first_count += len(first)
        require(evidence.aggregate(reconstructions)["verdict"] == "MIXED", "historical verdict")
        phases[phase] = {"primary": primary, "historical": outside}
        route_counts[phase] = {"second_hop": second_count, "first_hop": first_count}
    evidence.exact(phases["initial"], phases["replay"], "exact extracted phase replay")
    return {"schema": "TPCN-LUNA47A-INPUT-1", "integrity": integrity,
            "source_byte_policy": "exact Git baseline blobs; no historical-file normalization",
            "materialization": materialization,
            "retained_luna46": {"path": RETAINED.as_posix(), "sha256": RETAINED_HASH,
                                "byte_length": RETAINED_BYTES, "output_digest": retained["output_digest"]},
            "frozen_configuration": config45, "historical_configuration": config44,
            "phase_gates": phase_gates, "reconciled_route_counts": route_counts, "phases": phases}


def synthetic_controls() -> list[Record]:
    fixtures = {
        "isolated_impulse": [(0.0, 0.75), (80.0, 0.0)],
        "same_time": [(0.0, 0.6), (0.0, 0.6)],
        "opposing_cancellation": [(0.0, 0.75), (80.0, -0.75)],
        "sparse_subthreshold": [(0.0, 0.3), (80000.0, 0.3)],
        "long_gap_forgetting": [(0.0, 0.75), (1e12, 0.75)],
    }
    result = []
    for name, events in fixtures.items():
        prior = 0.0
        rows = []
        for queue, (t, payload) in enumerate(events):
            rows.append({"timestamp": t, "prior_clock": prior, "payload": payload,
                         "queue_sequence": queue, "event_id": f"{name}:{queue}", "is_reception": True})
            prior = t
        result.append(compare({"stream_id": name, "updates": rows}))
    return result


def numerical_audit() -> Record:
    """Fixed task-independent domain endpoints and analytical-target checks."""
    targets = []
    stress = []
    for name, rate in CONFIG["rates"].items():
        for dt in (0.0, 1e-12, 0.125, 80.0, 8000.0, 1e12):
            row = step(0.75, dt, -0.125, rate)
            with localcontext() as context:
                context.prec = 90
                exponent = -Decimal.from_float(rate) * Decimal.from_float(dt)
                target = float(Decimal("0.75") * exponent.exp() - Decimal("0.125"))
            targets.append({"variant": name, "dt": dt, "rho": row["rho"],
                            "comparison": evidence.checked(row["state_after"], target,
                                                           "90-digit continuous-time target")})
        for payload in (-1e6, 1e6):
            rows = [{"timestamp": 0.0, "prior_clock": 0.0, "queue_sequence": i,
                     "event_id": f"stress:{i}", "is_reception": True, "payload": payload}
                    for i in range(CONFIG["max_events"])]
            result = accumulate(rows, rate)
            forgotten = step(result["rows"][-1]["state_after"], 1e12, 0.0, rate)
            require(all(math.isfinite(r["state_after"]) and abs(r["state_after"]) <= 4
                        for r in result["rows"]), "numerical stress stability")
            stress.append({"variant": name, "events": len(rows), "payload": payload,
                           "timestamps": "all zero, increasing queue_sequence",
                           "minimum_signed_state": result["minimum_signed_state"],
                           "maximum_signed_state": result["maximum_signed_state"],
                           "maximum_absolute_state": result["maximum_absolute_state"],
                           "clipped_events": result["clipped_events"],
                           "after_extreme_gap": forgotten})
    return {"targets": targets, "stress": stress,
            "domain_rejection": "synthetic tests cover unsupported/nonfinite/capacity/order cases"}


def analyze(inputs: Record) -> Record:
    phase_results = {}
    comparisons = []
    for phase, groups in inputs["phases"].items():
        primary = [compare(s) for s in groups["primary"]]
        historical = [compare(s) for s in groups["historical"]]
        require(len(primary) == len(historical) == CONFIG["max_streams"], "analysis inventory")
        for source, result in zip(groups["primary"], primary):
            for update, row in zip(source["updates"], result["variants"]["baseline_tau80"]["rows"]):
                comparisons.append(evidence.checked(update["actual_state_after"], row["state_after"],
                                                    "baseline component vs actual"))
                comparisons.append(evidence.checked(update["actual_retained_state"], row["retained_state"],
                                                    "baseline retained state vs actual"))
                require((abs(update["actual_state_after"]) >= 1) == row["crosses"],
                        "actual threshold mismatch")
        phase_results[phase] = {"primary": primary, "historical": historical}
    evidence.exact(phase_results["initial"], phase_results["replay"], "variant replay")
    results = phase_results["initial"]
    primary_summary = summarize(results["primary"], True)
    require(primary_summary["original_categories"] == {
        "NO-RECEPTIONS": 212, "TEMPORAL-RETENTION-LIMITED": 33, "DRIVE-LIMITED": 75,
        "ALREADY-CROSSING": 0, "CANCELLATION-LIMITED": 0},
        "preserved category inventory")
    return {"schema": "TPCN-LUNA47A-RESULT-1", "config": CONFIG,
            "primary": results["primary"], "historical": results["historical"],
            "synthetic_controls": synthetic_controls(),
            "numerical_audit": numerical_audit(),
            "summary": primary_summary, "historical_summary": summarize(results["historical"], False),
            "baseline_comparisons": comparisons,
            "replay": {"initial_replay_equal": True, "analytical_sha256": evidence.digest(results)},
            "verdict": primary_summary["verdict"], "preserved_luna46_verdict": "MIXED",
            "feedback": "NONE", "efficacy": "NOT RUN", "hardware": "NOT RUN",
            "historical_interpretation": "no-output component counterfactual, not full-neuron replay"}


def output_directory(path: Path) -> Path:
    namespace = ROOT / "artifacts" / "luna47a"
    resolved = path.resolve()
    require(namespace.resolve() == namespace.absolute(), "aliased owned namespace")
    require(resolved == namespace or namespace in resolved.parents, "outside owned artifact namespace")
    return resolved


def execution_identity() -> Record:
    revision = evidence.git("rev-parse", "HEAD", root=ROOT).decode().strip()
    require(evidence.git("branch", "--show-current", root=ROOT).decode().strip() == BRANCH, "lane branch")
    require(not evidence.git("status", "--porcelain=v1", root=ROOT), "commit before execution; clean required")
    evidence.git("merge-base", "--is-ancestor", AUTHORIZATION, revision, root=ROOT)
    evidence.git("merge-base", "--is-ancestor", BASELINE, AUTHORIZATION, root=ROOT)
    files = ("experiments/luna47a/run.py", "experiments/luna47a/PROTOCOL.md",
             "tests/test_luna47a_retention.py", "run_luna46_depth_scaling_diagnostic.py")
    identities = {}
    for name in files:
        data = (ROOT / name).read_bytes()
        committed = evidence.git("show", f"{revision}:{name}", root=ROOT)
        # Git may materialize CRLF: retain both identities, require semantic text equality.
        require(data.replace(b"\r\n", b"\n") == committed.replace(b"\r\n", b"\n"),
                f"uncommitted execution source: {name}")
        identities[name] = {"working_sha256": evidence.sha(data), "git_sha256": evidence.sha(committed)}
    require(evidence.git("show", f"{BASELINE}:run_luna46_depth_scaling_diagnostic.py", root=ROOT)
            == evidence.git("show", f"{revision}:run_luna46_depth_scaling_diagnostic.py", root=ROOT),
            "reviewed analyzer modified")
    return {"revision": revision, "authorization_revision": AUTHORIZATION,
            "production_evidence_baseline": BASELINE, "branch": BRANCH, "files": identities}


def write_new(path: Path, value: Record) -> Record:
    payload = evidence.canonical(value) + b"\n"
    require(not path.exists(), f"refusing overwrite: {path}")
    with path.open("xb") as stream:
        stream.write(payload)
    require(path.read_bytes() == payload, "write readback")
    return {"sha256": evidence.sha(payload), "byte_length": len(payload)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/luna47a")
    parser.add_argument("--verify", action="store_true", help="replay saved bundle without writing")
    args = parser.parse_args(argv)
    try:
        directory = output_directory(args.output)
        if args.verify:
            manifest = evidence.read_json(directory / "manifest.json")
            for name, pin in manifest["files"].items():
                require(name in ("inputs.json", "results.json"), "manifest file name")
                data = evidence.read_bytes(directory / name)
                require(evidence.sha(data) == pin["sha256"] and len(data) == pin["byte_length"],
                        f"bundle hash: {name}")
            inputs = evidence.read_json(directory / "inputs.json")
            evidence.exact(inputs, verified_inputs(), "saved inputs vs raw evidence")
            regenerated = analyze(inputs)
            require(evidence.canonical(regenerated) + b"\n" == (directory / "results.json").read_bytes(),
                    "saved results replay bytes")
            print(f"PASS exact bundle replay: {regenerated['verdict']}; "
                  f"result_sha256={manifest['files']['results.json']['sha256']}")
            return 0
        code = execution_identity()
        require(not directory.exists() or not any(directory.iterdir()), "new empty output required")
        inputs = verified_inputs()
        result = analyze(inputs)
        require(result["verdict"] != "BLOCKED", "mechanism prerequisite failed")
        post_integrity = evidence.verify_integrity(ROOT / "experiments/luna47a/_evidence")
        evidence.exact(inputs["integrity"], post_integrity, "retained post-execution immutability")
        expected_physical = {name: {"sha256": row["physical_sha256"],
                                    "byte_length": row["physical_byte_length"]}
                             for name, row in inputs["materialization"].items()}
        evidence.exact(expected_physical, physical_inventory(inputs["materialization"]),
                       "historical physical checkout immutability")
        directory.mkdir(parents=True, exist_ok=True)
        pins = {name: write_new(directory / name, value)
                for name, value in (("inputs.json", inputs), ("results.json", result))}
        manifest = {"schema": "TPCN-LUNA47A-BUNDLE-1", "code": code, "files": pins,
                    "configuration_sha256": evidence.digest(CONFIG),
                    "input_semantic_sha256": evidence.digest(inputs),
                    "result_semantic_sha256": evidence.digest(result),
                    "environment": {"python": sys.version, "executable": sys.executable,
                                    "implementation": sys.implementation.name,
                                    "platform": platform.platform(), "epsilon": sys.float_info.epsilon},
                    "retained_immutability": "PASS; pre/post 33-file Git evidence integrity exact; "
                                            "34 historical physical checkout files unchanged",
                    "verdict": result["verdict"]}
        write_new(directory / "manifest.json", manifest)
        print(evidence.canonical({"verdict": result["verdict"], "summary": result["summary"],
                                  "files": pins}).decode())
        return 0
    except (evidence.Blocked, OSError, KeyError, TypeError, ValueError,
            subprocess.CalledProcessError) as error:
        print(f"BLOCKED: {type(error).__name__}: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
