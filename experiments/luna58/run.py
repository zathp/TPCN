"""Run the single-point Luna-58 finite destination-retention experiment."""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

from experiments.luna54 import run as luna54
from experiments.luna55 import run as luna55
from experiments.luna55.run import GateError


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = Path("experiments/luna58/config.json")
OUTPUT = Path("artifacts/luna58")
AUTHORIZATION_REVISION = "7dd3dc868e7518a33418d4df94b07c15dea52adb"
SELECTION_PATH = "artifacts/luna55-selection/post-luna54-destination-oracle.json"
RR_INITIAL = "artifacts/luna55/rr-initial.json"
RR_REPLAY = "artifacts/luna55/rr-replay.json"
RR_SUMMARY = "artifacts/luna55/summary-v3.json"
INPUT_PINS = {
    "experiments/luna55/config.json": (
        "197ebd8efc5449e1e973d4c6d96bdf12f40e1f31",
        "103594c2906fafb60684fc4f67adf22ffc0722eb268506e9d35d027bd98fcbba",
    ),
    "artifacts/luna54/intervention-initial.json": (
        "6de22f1f5406f378e115a818e01e459ec6ddf3e6",
        "62b4fe16da456a37ffe7014d495ce1e74ddad174bd853e1656a40256eee7b702",
    ),
    "artifacts/luna54/intervention-replay.json": (
        "684fc1f3adfbd26dbbca1a656c1d14c5e8ac92a8",
        "d7c3d69f9a6f184517eb465393eb6ace57e9210ef27a8cd5e8a5c52e1fb57bc4",
    ),
    SELECTION_PATH: (
        "a63a5edddd6f24b2625192b398b74a84125b97bb",
        "2ac7b79015c00d5055b1b6226ce23239f691ba07a368e80768737e39f0b2bd57",
    ),
    RR_INITIAL: (
        "b29e76709a6d502ee8f48aa4e4ea4f31fa9388ca",
        "2043a03744af925345a34ee3e7e704914c35f13faf1e9175bab9c9e600ad8b8b",
    ),
    RR_REPLAY: (
        "61baf5aa4c42a0c518d0c0fbf91e110acd8fe987",
        "7445773d6907488501a90d97064ebece57ccb9b0508b75df3f54fbe9a0555085",
    ),
    RR_SUMMARY: (
        "063b03ea84933f930ce95b2fe15e8ee83e0e4172",
        "5f1bba890f00c117a019dccf39948ec9b2169579f3ce749c81c03edfd85a3f86",
    ),
}
SOURCE_PATHS = (
    "tpcn/excursion_neuron.py",
    "tpcn/event_runtime.py",
    "tpcn/experiment_excursion_runtime.py",
    "tpcn/topology.py",
)
Record = dict[str, Any]


def _git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
    )
    return result.stdout if binary else result.stdout.strip()


def _json(path: str | Path) -> Record:
    value = json.loads((ROOT / path).read_bytes().decode("utf-8-sig"))
    if not isinstance(value, dict):
        raise GateError(f"expected JSON object in {path}")
    return value


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _semantic_digest(value: Record, field: str) -> str:
    clean = dict(value)
    claimed = clean.pop(field, None)
    actual = _sha_bytes(
        json.dumps(
            clean,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    )
    if claimed != actual:
        raise GateError(f"embedded {field} mismatch")
    return actual


def _validate_checkout_bytes(path: str, blob: str, expected_sha: str) -> bytes:
    """Accept only the exact Git blob or its exact LF-to-CRLF checkout form."""
    try:
        raw_object = _git("cat-file", "blob", blob, binary=True)
    except subprocess.CalledProcessError as error:
        raise GateError(f"missing authenticated Git blob {blob} for {path}") from error
    if not isinstance(raw_object, bytes):
        raise GateError(f"Git blob was not returned as bytes for {path}")
    actual_blob = str(_git("rev-parse", f"{AUTHORIZATION_REVISION}:{path}"))
    if actual_blob != blob:
        raise GateError(f"pinned Git blob differs at authorization revision: {path}")
    raw_checkout = (ROOT / path).read_bytes()
    crlf_form = raw_object.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    if raw_checkout not in (raw_object, crlf_form):
        raise GateError(f"checkout is not exact object bytes or exact CRLF form: {path}")
    if _sha_bytes(raw_checkout) != expected_sha:
        raise GateError(f"pinned checkout SHA-256 mismatch: {path}")
    return raw_checkout


def _verify_authorized_baseline() -> str:
    head = str(_git("rev-parse", "HEAD"))
    remote = str(_git("rev-parse", "origin/main"))
    if head != AUTHORIZATION_REVISION or remote != AUTHORIZATION_REVISION:
        raise GateError(
            f"execution must start at published authorization {AUTHORIZATION_REVISION}; "
            f"observed HEAD={head}, origin/main={remote}"
        )
    return head


def _authenticate_inputs(config: Record) -> dict[str, Record]:
    if config.get("schema") != "TPCN-LUNA58-CONFIG-1":
        raise GateError("Luna-58 configuration schema mismatch")
    if config.get("authorization_revision") != AUTHORIZATION_REVISION:
        raise GateError("Luna-58 execution authorization revision mismatch")
    verified: dict[str, Record] = {}
    for path, (blob, sha256) in INPUT_PINS.items():
        raw = _validate_checkout_bytes(path, blob, sha256)
        value = json.loads(raw.decode("utf-8-sig"))
        if not isinstance(value, dict):
            raise GateError(f"pinned input is not a JSON object: {path}")
        if path in (RR_INITIAL, RR_REPLAY, RR_SUMMARY):
            luna55._verify_digest(path, value)
        if path.startswith("artifacts/luna54/"):
            luna55._verify_digest(path, value)
            if value.get("scientific_digest") != config[
                "expected_intervention_source_scientific_digest"
            ]:
                raise GateError(f"source scientific digest mismatch: {path}")
        verified[path] = value

    selection = verified[SELECTION_PATH]
    if selection.get("schema") != "TPCN-LUNA55-SELECTION-1":
        raise GateError("frozen selection schema mismatch")
    rr_initial, rr_replay = verified[RR_INITIAL], verified[RR_REPLAY]
    rr_summary = verified[RR_SUMMARY]
    for phase, value in (("initial", rr_initial), ("replay", rr_replay)):
        if (
            value.get("phase") != phase
            or value.get("condition") != "RR"
            or value.get("status") != "PASS"
            or value.get("stream_count") != config["expected_stream_count"]
            or value.get("configuration_digest")
            != config["expected_luna55_configuration_digest"]
            or value.get("input_phase_digest")
            != config["expected_source_input_phase_digest"]
        ):
            raise GateError(f"retained RR {phase} scientific identity mismatch")
    if (
        rr_initial["streams"] != rr_replay["streams"]
        or rr_summary.get("artifact_digest")
        != "eee9c5f86d4692d654c3c660a79e629a8e3c45f4dc0b7ea9a0be6faf86532f22"
    ):
        raise GateError("retained RR replay or summary digest mismatch")
    return verified


def _strata(selection: Record, rr_initial: Record) -> tuple[dict[str, set[str]], dict[str, str]]:
    rows = selection.get("streams")
    if not isinstance(rows, list) or len(rows) != 320:
        raise GateError("frozen Luna-55 selection must contain 320 streams")
    categories = {
        item["stream_id"]: item["historical_stratum"]
        for item in rows
    }
    if len(categories) != 320:
        raise GateError("duplicate frozen stream ID")
    by_id = {row["stream_id"]: row for row in rows}
    rr_by_id = {row["stream_id"]: row for row in rr_initial["streams"]}
    target = set(luna55.TARGET_IDS)
    eplus = {
        sid
        for sid, row in by_id.items()
        if row["historical_stratum"] == "DRIVE-LIMITED"
        and row["additional_arrival_count"] > 0
        and not row["zero_decay_crossing"]
    }
    e0 = {
        sid
        for sid, row in by_id.items()
        if row["historical_stratum"] == "DRIVE-LIMITED"
        and row["additional_arrival_count"] == 0
    }
    nr1 = {
        sid for sid, row in by_id.items()
        if row["post_Luna54_classification"].startswith("NR1")
    }
    nr0 = {
        sid for sid, row in by_id.items()
        if row["post_Luna54_classification"].startswith("NR0")
    }
    secondary = {
        sid for sid, category in categories.items()
        if category == "TEMPORAL-RETENTION-LIMITED"
    }
    rr_responders = {sid for sid in target if rr_by_id[sid]["crossing"]}
    rr_nonresponders = target - rr_responders
    groups = {
        "primary_rr_nonresponders": rr_nonresponders,
        "primary_rr_responders": rr_responders,
        "Eplus_zero_decay_insufficient": eplus,
        "E0_no_additional_arrival": e0,
        "NR1_upstream_active_no_historical_reception": nr1,
        "NR0_no_input": nr0,
        "secondary_temporal_retention": secondary,
    }
    expected = {
        "primary_rr_nonresponders": 6,
        "primary_rr_responders": 10,
        "Eplus_zero_decay_insufficient": 49,
        "E0_no_additional_arrival": 10,
        "NR1_upstream_active_no_historical_reception": 189,
        "NR0_no_input": 23,
        "secondary_temporal_retention": 33,
    }
    if {name: len(ids) for name, ids in groups.items()} != expected:
        raise GateError("frozen RR target/control population partition mismatch")
    if set.union(*groups.values()) != set(categories):
        raise GateError("frozen populations do not cover all 320 streams")
    if sum(len(groups[name]) for name in (
        "primary_rr_nonresponders", "primary_rr_responders",
        "Eplus_zero_decay_insufficient", "E0_no_additional_arrival",
        "NR1_upstream_active_no_historical_reception", "NR0_no_input",
        "secondary_temporal_retention",
    )) != 320:
        raise GateError("frozen evaluation strata overlap")
    return groups, categories


def _source_route_signature(event: Record) -> tuple[Any, ...]:
    return (
        event["event_id"],
        event["payload_bits"],
        float(event["reception_timestamp"]),
        event["source"],
        event["destination"],
    )


def _relay_emission_signature(event: Record) -> tuple[Any, ...]:
    return (
        event["event_id"],
        event["payload_bits"],
        float(event["timestamp"]),
        event["source"],
    )


def _destination_route_signatures(row: Record) -> list[tuple[Any, ...]]:
    return [
        luna55._route_signature(event, "reception_timestamp")
        for event in row["destination_receptions"]
    ]


def _first_discharge(traces: list[Record]) -> Record | None:
    for trace in traces:
        if float(trace["discharge_amount"]) != 0.0:
            return {
                "timestamp": float(trace["timestamp"]),
                "signed_input": float(trace["input_value"]),
                "pre_input_z": float(trace["z_before_decay"]),
                "pre_addition_z": float(trace["z_after_decay"]),
                "post_input_z": float(trace["z_after_input"]),
                "post_discharge_z": float(trace["z_post_discharge"]),
                "discharge_amount": float(trace["discharge_amount"]),
                "emission_id": trace["emission_id"],
                "emission_timestamp": trace["emission_timestamp"],
            }
    return None


def _enrich_stream(row: Record, stratum: str) -> Record:
    row["evaluator_stratum"] = stratum
    traces = row["destination_integration_traces"]
    peak = max(
        (abs(float(trace["z_after_input"])) for trace in traces),
        default=0.0,
    )
    row["destination_peak_abs_z"] = peak
    row["destination_threshold_margin"] = 1.0 - peak
    row["response"] = luna55._response_l54(row)
    row["crossing"] = bool(row["destination_threshold_crossings"])
    row["first_destination_crossing"] = _first_discharge(traces)
    row["source_input_signature"] = [
        _source_route_signature(event) for event in row["source_inputs"]
    ]
    row["relay_emission_signature"] = [
        _relay_emission_signature(event) for event in row["relay_emissions"]
    ]
    row["destination_route_signature"] = _destination_route_signatures(row)
    return row


def _assert_runtime_bounds(row: Record, phase: str, condition: str) -> None:
    if not row["relay_oracle"]["passed"] or not row["destination_oracle"]["passed"]:
        raise GateError(f"independent E2 recurrence audit failed: {condition}/{phase}/{row['stream_id']}")
    if (
        not row["route_reconciliation"]["reconciles"]
        or not row["route_links_complete"]
        or not row["route_lineage_authenticated"]
        or not row["resources"]["settling_completed"]
        or row["resources"]["pending_events"] != 0
        or not all(
            row["resources"][name]
            for name in (
                "queue_bound_pass",
                "runtime_budget_pass",
                "neuron_budget_pass",
                "state_bounds_pass",
            )
        )
    ):
        raise GateError(f"route/bounds gate failed: {condition}/{phase}/{row['stream_id']}")
    if luna55._clipping_count(
        row["relay_integration_traces"], row["_relay_config"]
    ) + luna55._clipping_count(
        row["destination_integration_traces"], row["_destination_config"]
    ):
        raise GateError(f"z clipping observed: {condition}/{phase}/{row['stream_id']}")
    if row["roots_truncated_count"] < 0:
        raise GateError(f"invalid root-truncation count: {condition}/{phase}/{row['stream_id']}")


def _phase_record(
    phase: str,
    condition_name: str,
    condition: Record,
    selection: Record,
    categories: dict[str, str],
    frozen: Record,
    runtime_config: Record,
    experiment_config: Record,
    phase_data: Record,
    execution_revision: str,
) -> Record:
    relay, destination, effective = luna55._make_configs(frozen, condition)
    stream_ids = [item["stream_id"] for item in selection["streams"]]
    if len(stream_ids) != 320 or set(stream_ids) != set(phase_data["streams"]):
        raise GateError(f"source phase stream inventory changed: {phase}/{condition_name}")
    bounds = {
        "runtime": runtime_config["runtime"],
        "topology": runtime_config["topology"],
    }
    relay_config = luna54.jsonable(relay)
    destination_config = luna54.jsonable(destination)
    streams = []
    for stream_id in stream_ids:
        source_inputs = phase_data["streams"][stream_id]["source_inputs"]
        row = luna54.run_stream(
            stream_id,
            source_inputs,
            relay,
            destination,
            bounds,
        )
        row = _enrich_stream(row, categories[stream_id])
        row["_relay_config"] = relay_config
        row["_destination_config"] = destination_config
        _assert_runtime_bounds(row, phase, condition_name)
        row.pop("_relay_config")
        row.pop("_destination_config")
        streams.append(row)
    route_totals = {
        key: sum(row["route_reconciliation"][source_key] for row in streams)
        for key, source_key in (
            ("enqueued", "enqueued_count"),
            ("received", "received_count"),
            ("matched", "matched_count"),
            ("unmatched", "unmatched_enqueue_count"),
        )
    }
    route_totals["mismatches"] = route_totals["unmatched"] + sum(
        row["route_reconciliation"]["orphan_reception_count"]
        + row["route_reconciliation"]["duplicate_enqueue_count"]
        + row["route_reconciliation"]["duplicate_reception_count"]
        for row in streams
    )
    if (
        route_totals["enqueued"] != experiment_config["expected_route_count_per_phase"]
        or route_totals["received"] != experiment_config["expected_route_count_per_phase"]
        or route_totals["matched"] != experiment_config["expected_route_count_per_phase"]
        or route_totals["mismatches"] != 0
    ):
        raise GateError(f"421-route reconciliation failed: {condition_name}/{phase}")
    trunc_ids = sorted(
        row["stream_id"] for row in streams if row["roots_truncated_count"]
    )
    if trunc_ids != experiment_config["expected_inherited_truncated_streams"]:
        raise GateError(f"root truncation differs from frozen RR: {condition_name}/{phase}")
    return {
        "schema": "TPCN-LUNA58-PHASE-1",
        "status": "PASS",
        "phase": phase,
        "condition": condition_name,
        "execution_revision": execution_revision,
        "runner": {
            "path": "experiments/luna58/run.py",
            "sha256": _sha_bytes((ROOT / "experiments/luna58/run.py").read_bytes()),
        },
        "configuration": effective,
        "configuration_digest": _sha_bytes(
            json.dumps(effective, sort_keys=True, separators=(",", ":")).encode()
        ),
        "source_input_phase_digest": phase_data["input_digest"],
        "stream_count": len(streams),
        "source_input_count": sum(row["source_input_count"] for row in streams),
        "relay_emission_count": sum(
            row["relay_canonical_emission_count"] for row in streams
        ),
        "destination_reception_count": sum(
            row["destination_reception_count"] for row in streams
        ),
        "destination_crossing_count": sum(
            row["destination_threshold_crossings"] for row in streams
        ),
        "route_reconciliation": route_totals,
        "root_truncation_stream_ids": trunc_ids,
        "resource_bounds": {
            "queue_capacity": bounds["runtime"]["queue_capacity"],
            "runtime_event_budget": bounds["runtime"]["runtime_event_budget"],
            "per_neuron_event_budget": bounds["runtime"]["neuron_event_budget"],
            "settling_horizon": bounds["runtime"]["settling_horizon"],
            "peak_queue_occupancy": max(row["resources"]["queue_peak"] for row in streams),
            "peak_runtime_events": max(row["resources"]["processed_events"] for row in streams),
            "peak_relay_neuron_events": max(
                row["resources"]["neuron_processed_events"]["relay"] for row in streams
            ),
            "peak_destination_neuron_events": max(
                row["resources"]["neuron_processed_events"]["destination"] for row in streams
            ),
            "pending_events": sum(row["resources"]["pending_events"] for row in streams),
            "bound_failures": 0,
            "clipping_events": 0,
        },
        "runtime_source_identities": {
            path: {
                "git_blob": str(_git("rev-parse", f"HEAD:{path}")),
                "sha256": _sha_bytes((ROOT / path).read_bytes()),
            }
            for path in SOURCE_PATHS
        },
        "python": sys.version,
        "platform": platform.platform(),
        "labels_entered_runtime": False,
        "streams": streams,
    }


def _write_artifact(path: Path, record: Record) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    record["artifact_digest"] = luna55._artifact_digest(record)
    payload = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    with path.open("xb") as handle:
        handle.write(payload)
    if path.read_bytes() != payload:
        raise OSError(f"artifact readback mismatch: {path}")
    return _sha_bytes(payload)


def _stream_map(record: Record) -> dict[str, Record]:
    return {row["stream_id"]: row for row in record["streams"]}


def _verify_control_reproduction(control: Record, retained: Record) -> Record:
    actual, expected = _stream_map(control), _stream_map(retained)
    if set(actual) != set(expected):
        raise GateError("fresh RR control stream IDs differ from retained RR")
    exact_fields = (
        "source_inputs",
        "relay_emissions",
        "relay_integration_traces",
        "destination_receptions",
        "destination_integration_traces",
        "destination_emissions",
        "route_reconciliation",
        "relay_oracle",
        "destination_oracle",
        "resources",
        "destination_state",
    )
    for stream_id in actual:
        current, old = actual[stream_id], expected[stream_id]
        if any(current[field] != old[field] for field in exact_fields):
            raise GateError(f"fresh finite RR control differs from frozen RR: {stream_id}")
        if current["destination_route_signature"] != [
            luna55._route_signature(event, "reception_timestamp")
            for event in old["destination_receptions"]
        ]:
            raise GateError(f"fresh RR control route signature mismatch: {stream_id}")
    return {
        "passed": True,
        "streams_exact": len(actual),
        "source_inputs_exact": True,
        "relay_emissions_exact": True,
        "destination_route_signatures_exact": 421,
        "destination_receptions_exact": 421,
        "integration_and_runtime_records_exact": True,
    }


def _verify_intervention_routes(control: Record, intervention: Record) -> Record:
    before, after = _stream_map(control), _stream_map(intervention)
    if set(before) != set(after):
        raise GateError("intervention stream IDs differ from RR control")
    arrivals = 0
    for stream_id in before:
        base, changed = before[stream_id], after[stream_id]
        if base["source_inputs"] != changed["source_inputs"]:
            raise GateError(f"source input drift under intervention: {stream_id}")
        if base["relay_emissions"] != changed["relay_emissions"]:
            raise GateError(f"relay event stream drift under intervention: {stream_id}")
        if base["source_input_signature"] != changed["source_input_signature"]:
            raise GateError(f"source signature drift under intervention: {stream_id}")
        if base["relay_emission_signature"] != changed["relay_emission_signature"]:
            raise GateError(f"relay signature drift under intervention: {stream_id}")
        if base["destination_route_signature"] != changed["destination_route_signature"]:
            raise GateError(f"destination route signature drift under intervention: {stream_id}")
        if base["roots_truncated_count"] != changed["roots_truncated_count"]:
            raise GateError(f"root-truncation count drift under intervention: {stream_id}")
        if base["relay_root_expansion_complete"] != changed["relay_root_expansion_complete"]:
            raise GateError(f"relay root expansion drift under intervention: {stream_id}")
        if base["source_root_expansion_complete"] != changed["source_root_expansion_complete"]:
            raise GateError(f"source root expansion drift under intervention: {stream_id}")
        arrivals += len(changed["destination_route_signature"])
    if arrivals != 421:
        raise GateError(f"intervention route signature count was {arrivals}, expected 421")
    return {
        "passed": True,
        "streams": len(before),
        "source_input_signatures_exact": True,
        "relay_emission_signatures_exact": True,
        "destination_route_signatures_exact": arrivals,
        "complete_route_fields_compared": [
            "event_id", "payload_bits", "timestamp", "source", "destination",
            "lineage_id", "originating_emission_id", "causal_roots",
            "roots_truncated", "route_depth", "route_path",
            "scheduled_delivery_timestamp",
        ],
        "no_new_root_truncation": True,
    }


def _verify_acceptance(
    phases: dict[str, Record],
    groups: dict[str, set[str]],
    route_audits: dict[str, Record],
) -> Record:
    control_initial = _stream_map(phases["rr-control-initial"])
    control_replay = _stream_map(phases["rr-control-replay"])
    int_initial = _stream_map(phases["finite-initial"])
    int_replay = _stream_map(phases["finite-replay"])
    if control_initial != control_replay or int_initial != int_replay:
        raise GateError("initial/replay stream records differ within a condition")
    for key in ("finite-initial", "finite-replay"):
        rows = _stream_map(phases[key])
        for stream_id in groups["primary_rr_nonresponders"] | groups["primary_rr_responders"]:
            row = rows[stream_id]
            if not row["source_root_expansion_complete"] or not row[
                "relay_root_expansion_complete"
            ] or row["roots_truncated_count"]:
                raise GateError(f"primary target root expansion/truncation failure: {stream_id}")
    result_counts: dict[str, dict[str, int]] = {}
    for key in ("finite-initial", "finite-replay"):
        rows = _stream_map(phases[key])
        result_counts[key] = {
            name: sum(bool(rows[sid]["destination_threshold_crossings"]) for sid in ids)
            for name, ids in groups.items()
        }
        if result_counts[key]["primary_rr_nonresponders"] != 6:
            raise GateError(f"one or more of the six predicted rescues missed in {key}")
        if result_counts[key]["primary_rr_responders"] != 10:
            raise GateError(f"one or more RR responder controls failed in {key}")
        for group in (
            "Eplus_zero_decay_insufficient",
            "E0_no_additional_arrival",
            "NR1_upstream_active_no_historical_reception",
            "NR0_no_input",
        ):
            if result_counts[key][group] != 0:
                raise GateError(f"new negative-control crossing in {group}/{key}")
    if route_audits["finite-initial"] != route_audits["finite-replay"]:
        raise GateError("route audit changed between finite intervention phases")
    return {
        "status": "PASS",
        "initial_replay_identical": True,
        "crossings_by_group": result_counts,
        "all_six_primary_nonresponders_crossed": True,
        "all_ten_rr_positive_controls_crossed": True,
        "specified_negative_controls_zero": True,
        "secondary_temporal_retention_reported_separately": True,
    }


def _summary(
    phases: dict[str, Record],
    phase_hashes: dict[str, str],
    verified: dict[str, Record],
    groups: dict[str, set[str]],
    route_audits: dict[str, Record],
    acceptance: Record,
    inputs: Record,
) -> Record:
    rows = _stream_map(phases["finite-initial"])
    strata: Record = {}
    for name, ids in groups.items():
        subset = [rows[sid] for sid in sorted(ids)]
        strata[name] = {
            "stream_count": len(subset),
            "crossings": sum(bool(row["destination_threshold_crossings"]) for row in subset),
            "relay_emissions": sum(row["relay_canonical_emission_count"] for row in subset),
            "destination_receptions": sum(row["destination_reception_count"] for row in subset),
            "discharges": sum(row["destination_discharge_count"] for row in subset),
            "canonical_emissions": sum(
                row["destination_canonical_emission_count"] for row in subset
            ),
            "maximum_queue_events": max(
                (row["resources"]["processed_events"] for row in subset), default=0
            ),
            "maximum_destination_peak_abs_z": max(
                (row["destination_peak_abs_z"] for row in subset), default=0.0
            ),
        }
    per_target: list[Record] = []
    rr_base = _stream_map(verified[RR_INITIAL])
    for stream_id in luna55.TARGET_IDS:
        base, row = rr_base[stream_id], rows[stream_id]
        traces = row["destination_integration_traces"]
        per_target.append({
            "stream_id": stream_id,
            "rr_baseline_crossed": bool(base["crossing"]),
            "intervention_crossed": bool(row["destination_threshold_crossings"]),
            "source_input_count": row["source_input_count"],
            "relay_emission_count": row["relay_canonical_emission_count"],
            "destination_reception_count": row["destination_reception_count"],
            "destination_route_signature": row["destination_route_signature"],
            "destination_payloads_signed": [float(e["payload"]) for e in row["destination_receptions"]],
            "integration_trace": [
                {
                    "timestamp": trace["timestamp"],
                    "elapsed": trace["elapsed"],
                    "signed_payload": trace["input_value"],
                    "z_before_decay": trace["z_before_decay"],
                    "z_after_decay": trace["z_after_decay"],
                    "z_after_input": trace["z_after_input"],
                    "z_post_discharge": trace["z_post_discharge"],
                    "discharge_amount": trace["discharge_amount"],
                    "mode_before": trace["mode_before"],
                    "emission_id": trace["emission_id"],
                    "emission_timestamp": trace["emission_timestamp"],
                }
                for trace in traces
            ],
            "first_crossing": row["first_destination_crossing"],
            "discharge_count": row["destination_discharge_count"],
            "canonical_emission_count": row["destination_canonical_emission_count"],
            "route_reconciles": row["route_reconciliation"]["reconciles"],
            "route_roots_truncated_count": row["roots_truncated_count"],
        })
    return {
        "schema": "TPCN-LUNA58-SUMMARY-1",
        "status": "PASS",
        "authorization_revision": AUTHORIZATION_REVISION,
        "execution_revision": str(_git("rev-parse", "HEAD")),
        "configuration_digest_rr": phases["rr-control-initial"]["configuration_digest"],
        "configuration_digest_intervention": phases["finite-initial"]["configuration_digest"],
        "sole_configuration_delta": "destination.integration.decay_rate_z: 0.00125 -> 0.00001",
        "provenance": inputs,
        "retained_luna55_summary_digest": verified[RR_SUMMARY]["artifact_digest"],
        "route_reconciliation": route_audits,
        "acceptance": acceptance,
        "phase_artifact_sha256": phase_hashes,
        "strata": strata,
        "primary_targets_frozen_order": per_target,
        "phase_resource_bounds": {
            key: value["resource_bounds"] for key, value in phases.items()
        },
        "labels_entered_runtime": False,
        "initial_replay_are_independent_samples": False,
        "interpretation_boundary": (
            "One bounded ACP-0008 software-reference mechanism experiment only; "
            "no task efficacy, generalization, production, hardware-equivalence, "
            "architecture-promotion, or physical-energy claim."
        ),
    }


def execute() -> Record:
    start_revision = _verify_authorized_baseline()
    config = _json(CONFIG_PATH)
    verified = _authenticate_inputs(config)
    selection = verified[SELECTION_PATH]
    rr_initial, rr_replay = verified[RR_INITIAL], verified[RR_REPLAY]
    groups, categories = _strata(selection, rr_initial)
    sources, _protocol, l54_config, frozen, _l46_integrity = (
        luna55._load_verified_luna54_sources()
    )
    if config["runtime"] != {
        "queue_capacity": l54_config["runtime"]["queue_capacity"],
        "runtime_event_budget": l54_config["runtime"]["runtime_event_budget"],
        "per_neuron_event_budget": l54_config["runtime"]["neuron_event_budget"],
        "settling_horizon": l54_config["runtime"]["settling_horizon"],
    }:
        raise GateError("Luna-58 runtime bounds differ from frozen Luna-55")
    phases: dict[str, Record] = {}
    hashes: dict[str, str] = {}

    # The matched finite RR control is executed and authenticated before the
    # one-point destination-retention intervention is interpreted.
    rr_condition = _json("experiments/luna55/config.json")["conditions"]["RR"]
    for phase, retained in (("initial", rr_initial), ("replay", rr_replay)):
        phase_data = luna54._load_phase(phase, sources)[3]
        if phase_data["input_digest"] != config["expected_source_input_phase_digest"]:
            raise GateError(f"authenticated source input digest mismatch in {phase}")
        key = f"rr-control-{phase}"
        record = _phase_record(
            phase, "RR_CONTROL", rr_condition, selection, categories,
            frozen, l54_config, config, phase_data, start_revision,
        )
        record["retained_rr_reproduction"] = _verify_control_reproduction(record, retained)
        phases[key] = record
        hashes[key] = _write_artifact(OUTPUT / f"{key}.json", record)
    if _stream_map(phases["rr-control-initial"]) != _stream_map(phases["rr-control-replay"]):
        raise GateError("fresh RR control initial/replay records differ")

    intervention_condition = deepcopy(rr_condition)
    intervention_condition["destination_decay_rate_z"] = config[
        "intervention_destination_decay_rate_z"
    ]
    baseline_cfg = luna55._make_configs(frozen, rr_condition)[2]
    intervention_cfg = luna55._make_configs(frozen, intervention_condition)[2]
    changed = luna54._diff_paths(baseline_cfg, intervention_cfg)
    if changed != ["destination.integration.decay_rate_z"]:
        raise GateError(f"intervention changed unauthorized fields: {changed}")
    if baseline_cfg["relay"] != intervention_cfg["relay"]:
        raise GateError("relay configuration changed in the destination-only intervention")
    if (
        intervention_cfg["relay"]["integration"]["decay_rate_z"] != 0.00125
        or intervention_cfg["destination"]["integration"]["decay_rate_z"] != 0.00001
    ):
        raise GateError("intervention decay values do not match the frozen contract")

    route_audits: dict[str, Record] = {}
    for phase in ("initial", "replay"):
        phase_data = luna54._load_phase(phase, sources)[3]
        key = f"finite-{phase}"
        record = _phase_record(
            phase, "FINITE_DESTINATION", intervention_condition,
            selection, categories, frozen, l54_config, config, phase_data,
            start_revision,
        )
        phases[key] = record
        hashes[key] = _write_artifact(OUTPUT / f"{key}.json", record)
        route_audits[key] = _verify_intervention_routes(
            phases[f"rr-control-{phase}"], record
        )

    # Reconcile all 421 historical RR routes in each fresh control phase too.
    for phase, retained in (("initial", rr_initial), ("replay", rr_replay)):
        fresh = phases[f"rr-control-{phase}"]
        audit = _verify_control_reproduction(fresh, retained)
        route_audits[f"rr-control-{phase}"] = audit
        route_audits[f"finite-{phase}"] = _verify_intervention_routes(
            fresh, phases[f"finite-{phase}"]
        )
    acceptance = _verify_acceptance(phases, groups, route_audits)
    provenance = {
        "authenticated_inputs": {
            path: {
                "git_blob": INPUT_PINS[path][0],
                "sha256": INPUT_PINS[path][1],
            }
            for path in INPUT_PINS
        },
        "retained_source_scientific_digest": config[
            "expected_intervention_source_scientific_digest"
        ],
        "rr_configuration_digest": config["expected_luna55_configuration_digest"],
        "source_input_phase_digest": config["expected_source_input_phase_digest"],
        "start_revision": start_revision,
    }
    result = _summary(
        phases, hashes, verified, groups, route_audits, acceptance, provenance
    )
    result["artifact_sha256"] = _write_artifact(OUTPUT / "summary.json", result)
    return result


def verify_artifacts() -> Record:
    summary = _json(OUTPUT / "summary.json")
    luna55._verify_digest(str(OUTPUT / "summary.json"), summary)
    names = (
        "rr-control-initial", "rr-control-replay", "finite-initial", "finite-replay",
    )
    for name in names:
        phase = _json(OUTPUT / f"{name}.json")
        luna55._verify_digest(str(OUTPUT / f"{name}.json"), phase)
        if phase.get("status") != "PASS" or phase.get("stream_count") != 320:
            raise GateError(f"Luna-58 phase artifact failed verification: {name}")
        if _sha_bytes((OUTPUT / f"{name}.json").read_bytes()) != summary[
            "phase_artifact_sha256"
        ][name]:
            raise GateError(f"Luna-58 phase file hash mismatch: {name}")
    return {
        "status": "PASS",
        "phase_artifacts": list(names),
        "summary_sha256": _sha_bytes((OUTPUT / "summary.json").read_bytes()),
        "all_artifact_digests_valid": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args(argv)
    result = verify_artifacts() if args.verify else execute()
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
