from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import struct
from typing import Any

from .schema import BRANCHES, RECORDS, integer_value
from .trace import read_trace

CORE_RECORDS = {
    "P01": {"input_event"},
    "P02": {"enqueue", "schedule", "dequeue", "process"},
    "P03": {"prediction_create", "prediction_match"},
    "P04": {"omission_resolve", "omission_route", "omission_delivery"},
    "P05": {"readout_feature"},
    "P06": {"readout_drive", "readout_activation", "readout_decision"},
    "P07": {"eligibility_create", "eligibility_expire", "eligibility_consume", "eligibility_admission"},
    "P08": {"feedback_schedule", "feedback_apply", "feedback_reject"},
    "P09": {"parameter_initial", "parameter_transition", "parameter_final"},
    "P10": {"classification_output"},
    "P11": {"queue_state", "admission_decision", "event_processed"},
}

BRANCH_RECORDS = {
    "queue_overflow_drop_failure": "queue_failure",
    "duplicate_feedback": "feedback_reject",
    "rejected_feedback": "feedback_reject",
    "prediction_expiration": "prediction_expire",
    "prediction_settlement": "prediction_settle",
    "omission_resolution": "omission_resolve",
    "score_tie": "readout_decision",
    "eligibility_expiration": "eligibility_expire",
    "eligibility_consumption": "eligibility_consume",
}


def _parameter_manifest_digest(parameters: Any) -> str:
    """Reproduce the copied Python source's manifest hash, never its parity values."""
    def source(value: Any) -> Any:
        if isinstance(value, list):
            return [source(item) for item in value]
        if not isinstance(value, dict):
            return value
        if value["kind"] == "map":
            return {key: source(item) for key, item in value["entries"].items()}
        if value["kind"] == "pyint":
            return integer_value(value)
        if value["kind"] == "f64":
            return struct.unpack(">d", bytes.fromhex(value["bits_be_hex"]))[0]
        raise ValueError("copied Python parameter manifest source type unavailable")
    raw = json.dumps(source(parameters), sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _branch_observations(records: list[dict[str, Any]], name: str) -> list[Any]:
    payloads = [r["payload"] for r in records if r["record_type"] == BRANCH_RECORDS[name]]
    if name == "duplicate_feedback":
        payloads = [p for p in payloads if p["duplicate"]]
    if name == "score_tie":
        payloads = [p for p in payloads if len(p["tie_set"]) > 1]
    return [{"kind": "map", "entries": {
        key: {"kind": "map", "entries": value} if key == "anchor" else value
        for key, value in p.items()}} for p in payloads]


def _shape_gaps(records: list[dict[str, Any]], side: str) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []

    def gap(item: str, path: str) -> None:
        gaps.append({"comparison_id": item, "field_path": f"{side}:{path}"})

    def rows(kind: str) -> list[dict[str, Any]]:
        return [r["payload"] for r in records if r["record_type"] == kind]

    inputs = rows("input_event")
    if [integer_value(p["input_order"]) for p in inputs] != list(range(len(inputs))) or len({p["event_id"] for p in inputs}) != len(inputs):
        gap("P01", "input_event.order_or_identity")
    for payload in inputs:
        enqueues = [p for p in rows("enqueue") if p["anchor"]["event_id"] == payload["event_id"]]
        if len(enqueues) != 1 or any(enqueues[0][key] != payload[key] for key in ("timestamp", "payload", "event_type")) or enqueues[0]["anchor"]["source"] != payload["channel_id"]:
            gap("P01", "input_event.enqueue_link")
    for enqueue in rows("enqueue"):
        anchor = enqueue["anchor"]
        admissions = [p for p in rows("admission_decision") if p["anchor"] == anchor]
        if len(admissions) != 1 or any(admissions[0][key] != enqueue[key] for key in (
            "admission_outcome", "occupancy_before", "occupancy_after", "queue_sequence")):
            gap("P11", f"{anchor['event_id']}.admission_link")
        schedules = [p for p in rows("schedule") if p["anchor"] == anchor]
        if enqueue["admission_outcome"] == "ADMITTED":
            if len(schedules) != 1 or any(schedules[0][key] != enqueue[key] for key in (
                "event_type", "payload", "timestamp", "queue_sequence", "priority_key")):
                gap("P02", f"{anchor['event_id']}.schedule_link")
        elif schedules:
            gap("P02", f"{anchor['event_id']}.rejected_schedule")
    for kind, previous in (("schedule", "enqueue"), ("dequeue", "enqueue"), ("process", "dequeue"),
                           ("admission_decision", "enqueue")):
        for row in records:
            if row["record_type"] != kind:
                continue
            p = row["payload"]
            matches = [r for r in records if r["record_type"] == previous
                       and r["payload"]["anchor"] == p["anchor"]
                       and r["record_index"] < row["record_index"]]
            if len(matches) != 1:
                gap("P11" if kind == "admission_decision" else "P02", f"{kind}.previous_operation_link")
    for state in rows("queue_state"):
        if integer_value(state["occupancy"]) != len(state["pending"]) or integer_value(state["occupancy"]) > integer_value(state["capacity"]):
            gap("P11", "queue_state.occupancy_shape")
    decisions = rows("readout_decision")
    features = rows("readout_feature")
    decision_ids = [p["decision_id"] for p in decisions]
    if len(set(decision_ids)) != len(decision_ids) or len(features) != len(decisions) or set(decision_ids) != {p["decision_id"] for p in features}:
        gap("P06", "decision_identity")
        gap("P05", "decision_feature.cardinality")
    for decision in decisions:
        identity = decision["decision_id"]
        fs = [p for p in features if p["decision_id"] == identity]
        drives = [p for p in rows("readout_drive") if p["decision_id"] == identity]
        activations = [p for p in rows("readout_activation") if p["decision_id"] == identity]
        if len(fs) != 1 or len(drives) != 4 or len(activations) != 4 or {integer_value(p["class_index"]) for p in drives} != set(range(4)) or {integer_value(p["class_index"]) for p in activations} != set(range(4)):
            gap("P06", f"{identity}.four_class_cardinality")
            if len(fs) != 1:
                gap("P05", f"{identity}.feature_cardinality")
            continue
        for drive in drives:
            activation = next(p for p in activations if p["class_index"] == drive["class_index"])
            if drive["feature"] != fs[0]["feature"] or activation["pre_transfer"] != drive["drive"]:
                gap("P06", f"{identity}.feature_activation_link")
        winner = integer_value(decision["winner"])
        ties = [integer_value(p) for p in decision["tie_set"]]
        order = [integer_value(p) for p in decision["tie_break_order"]]
        if winner != integer_value(decision["tie_break_result"]) or winner not in ties or winner != next(i for i in order if i in ties):
            gap("P06", f"{identity}.tie_result")
    for kind in ("readout_drive", "readout_activation"):
        if any(p["decision_id"] not in decision_ids for p in rows(kind)):
            gap("P06", f"{kind}.orphan")
    outputs = rows("classification_output")
    if len(outputs) != 1 or not decisions or outputs[0]["predicted_class"] != decisions[-1]["winner"]:
        gap("P10", "classification_output.decision_link")
    for kind, creation, identity, item in (
        ("prediction_match", "prediction_create", "prediction_id", "P03"),
        ("prediction_expire", "prediction_create", "prediction_id", "P03"),
        ("prediction_settle", "prediction_create", "prediction_id", "P03"),
        ("omission_resolve", "prediction_create", "prediction_id", "P04"),
        ("omission_route", "omission_resolve", "prediction_id", "P04"),
        ("omission_delivery", "omission_route", "event_id", "P04"),
        ("eligibility_expire", "eligibility_create", "trace_id", "P07"),
        ("eligibility_consume", "eligibility_create", "trace_id", "P07"),
        ("feedback_apply", "feedback_schedule", "feedback_id", "P08"),
    ):
        for row in records:
            if row["record_type"] == kind:
                matches = [r for r in records if r["record_type"] == creation and r["payload"][identity] == row["payload"][identity] and r["record_index"] < row["record_index"]]
                if len(matches) != 1:
                    gap(item, f"{kind}.{identity}.creation_link")
    for kind, identity, item in (
        ("prediction_create", "prediction_id", "P03"),
        ("eligibility_create", "trace_id", "P07"),
        ("feedback_schedule", "feedback_id", "P08"),
    ):
        ids = [p[identity] for p in rows(kind)]
        if len(ids) != len(set(ids)):
            gap(item, f"{kind}.duplicate_identity")
    processed = rows("event_processed")
    processes = rows("process")
    if len(processed) != len(processes) or any(
        p["event_id"] != op["anchor"]["event_id"] or p["processed_at"] != op["timestamp"]
        or integer_value(p["processed_count"]) != index + 1
        or integer_value(p["process_order"]) != index
        for index, (p, op) in enumerate(zip(processed, processes))
    ):
        gap("P11", "event_processed.process_link")
    initial, final = rows("parameter_initial"), rows("parameter_final")
    if len(initial) == len(final) == 1:
        def leaves(value: Any, prefix: str = "") -> dict[str, Any]:
            if isinstance(value, dict) and value.get("kind") == "map":
                result = {}
                for key, item in value["entries"].items():
                    result.update(leaves(item, f"{prefix}.{key}" if prefix else key))
                return result
            if isinstance(value, list):
                result = {}
                for index, item in enumerate(value):
                    result.update(leaves(item, f"{prefix}.{index}"))
                return result
            return {prefix: value}
        state = leaves(initial[0]["parameters"])
        for index, transition in enumerate(rows("parameter_transition")):
            path = transition["parameter_id"]
            if integer_value(transition["transition_order"]) != index or path not in state or state[path] != transition["old_value"]:
                gap("P09", f"{path}.transition_chain")
            state[path] = transition["new_value"]
        if state != leaves(final[0]["parameters"]):
            gap("P09", "parameter_final.transition_chain")
        parameter_records = [r["record_type"] for r in records if RECORDS[r["record_type"]][0] == "P09"]
        if parameter_records[0] != "parameter_initial" or parameter_records[-1] != "parameter_final":
            gap("P09", "parameter_snapshot.order")
    return gaps


@dataclass(frozen=True)
class Mismatch:
    comparison_id: str
    record_index: int
    field_path: str
    original: Any
    instrumented: Any


@dataclass
class ComparisonReport:
    schema_version: str
    overall_status: str
    item_status: dict[str, str]
    branch_status: dict[str, dict[str, str]]
    first_mismatch: Mismatch | None
    missing_evidence: list[dict[str, str]]
    raw: dict[str, dict[str, Any]]
    identities: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["first_mismatch"] = None if self.first_mismatch is None else asdict(self.first_mismatch)
        return result


def _first_difference(left: Any, right: Any, path: str) -> tuple[str, Any, Any] | None:
    if type(left) is not type(right):
        return path, left, right
    if isinstance(left, dict):
        if set(left) != set(right):
            return f"{path}.<keys>", sorted(left), sorted(right)
        for key in sorted(left):
            mismatch = _first_difference(left[key], right[key], f"{path}.{key}")
            if mismatch is not None:
                return mismatch
        return None
    if isinstance(left, list):
        if len(left) != len(right):
            return f"{path}.<length>", len(left), len(right)
        for index, (a, b) in enumerate(zip(left, right)):
            mismatch = _first_difference(a, b, f"{path}[{index}]")
            if mismatch is not None:
                return mismatch
        return None
    return None if left == right else (path, left, right)


def _verify_identity(records: list[dict[str, Any]], side: str, expected: dict[str, Any]) -> None:
    first = records[0]
    side_expected = expected[side]
    for field in ("source_revision", "runtime_manifest_sha256"):
        if side_expected.get(field) is None or first[field] != side_expected[field]:
            raise ValueError(f"{side} {field} is missing or mismatched")
    for field in ("seed", "arm", "split", "example_id", "exposure_id"):
        if expected.get(field) is None or first[field] != expected[field]:
            raise ValueError(f"shared {field} is missing or mismatched for {side}")
    if first["seed"] != 17:
        raise ValueError("paired PPC-11 contract requires seed 17")


def _branch_pair(original: dict[str, Any] | None, instrumented: dict[str, Any] | None) -> dict[str, str]:
    if original is None or instrumented is None:
        return {"original": "EVIDENCE_UNAVAILABLE", "instrumented": "EVIDENCE_UNAVAILABLE", "pair_outcome": "EVIDENCE_UNAVAILABLE"}
    a, b = original["evidence_state"], instrumented["evidence_state"]
    oa, ob = original["occurrences"], instrumented["occurrences"]
    if a == "MEASURED_POSITIVE" and not oa or b == "MEASURED_POSITIVE" and not ob:
        return {"original": "EVIDENCE_UNAVAILABLE" if not oa else a,
                "instrumented": "EVIDENCE_UNAVAILABLE" if not ob else b,
                "pair_outcome": "EVIDENCE_UNAVAILABLE"}
    conclusive_a = a in {"MEASURED_ZERO", "COMPLETE_UNEXERCISED"}
    conclusive_b = b in {"MEASURED_ZERO", "COMPLETE_UNEXERCISED"}
    comparison_status = "READY"
    if a == "MEASURED_ZERO" and b == "MEASURED_ZERO":
        outcome = "BOTH_ZERO"
    elif a == b == "MEASURED_POSITIVE":
        outcome = "EXERCISED_AND_COMPARED"
        if oa != ob or original["occurrence_count"] != instrumented["occurrence_count"]:
            comparison_status = "CONTRADICTED"
    elif (a == "MEASURED_POSITIVE" and conclusive_b) or (b == "MEASURED_POSITIVE" and conclusive_a):
        outcome = "ONE_SIDED_OCCURRENCE"
    elif conclusive_a and conclusive_b and "COMPLETE_UNEXERCISED" in {a, b}:
        outcome = "UNEXERCISED"
    else:
        outcome = "EVIDENCE_UNAVAILABLE"
    if outcome == "ONE_SIDED_OCCURRENCE":
        comparison_status = "CONTRADICTED"
    elif outcome == "EVIDENCE_UNAVAILABLE":
        comparison_status = "INCOMPLETE"
    return {"original": a, "instrumented": b, "pair_outcome": outcome,
            "comparison_status": comparison_status}




def _p11_stop_alignment(original: list[dict[str, Any]], instrumented: list[dict[str, Any]]) -> dict[str, Any] | None:
    failures = {
        "original": [row for row in original if row["record_type"] == "queue_failure"],
        "instrumented": [row for row in instrumented if row["record_type"] == "queue_failure"],
    }
    if not failures["original"] and not failures["instrumented"]:
        return None
    if len(failures["original"]) > 1 or len(failures["instrumented"]) > 1:
        return {"aligned": False, "reason": "multiple queue-failure triggers"}
    failed_side = "original" if failures["original"] else "instrumented"
    other_side = "instrumented" if failed_side == "original" else "original"
    failure = failures[failed_side][0]
    anchor = failure["payload"]["anchor"]
    streams = {"original": original, "instrumented": instrumented}
    failed_terminals = [r for r in streams[failed_side] if r["record_type"] == "terminal_state" and r["record_index"] > failure["record_index"]]
    other_terminals = [r for r in streams[other_side] if r["record_type"] == "terminal_state"]
    if len(failed_terminals) != 1 or len(other_terminals) != 1:
        return {"aligned": False, "failed_side": failed_side, "failure": failure,
                "reason": "actual terminal boundary missing or ambiguous"}
    other_terminal = other_terminals[0]
    admission = next((r for r in streams[other_side]
                      if r["record_type"] == "enqueue"
                      and r["record_index"] < other_terminal["record_index"]
                      and r["payload"]["anchor"] == anchor
                      and r["payload"]["admission_outcome"] == "ADMITTED"), None)
    return {"aligned": admission is not None, "failed_side": failed_side,
            "failure": failure, "admission": admission,
            "failed_terminal": failed_terminals[0], "other_terminal": other_terminal,
            "anchor": anchor,
            "reason": None if admission is not None else "counterpart pre-stop trace lacks exact admitted anchor"}

def compare_pair(original_path: str | Path, instrumented_path: str | Path, *, expected: dict[str, Any]) -> ComparisonReport:
    """Strict exact comparison. Inputs are independent raw side streams."""
    original, original_hash, original_bytes = read_trace(original_path, expected_side="original")
    instrumented, instrumented_hash, instrumented_bytes = read_trace(instrumented_path, expected_side="instrumented")
    _verify_identity(original, "original", expected)
    _verify_identity(instrumented, "instrumented", expected)
    if original[0]["run_id"] == instrumented[0]["run_id"]:
        raise ValueError("execution identities must be independent")
    if not isinstance(expected.get("fixture_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", expected["fixture_sha256"]):
        raise ValueError("frozen fixture identity is required")

    item_status: dict[str, str] = {}
    missing: list[dict[str, str]] = []
    # No frozen event-payload manifest is present in the copied C4.1 inputs.
    # A caller-supplied digest cannot bind P01 events to that missing evidence.
    missing.append({"comparison_id": "P01", "field_path": "frozen_fixture_payload_identity_unavailable"})
    for side, records in (("original", original), ("instrumented", instrumented)):
        missing.extend(_shape_gaps(records, side))
        for kind in ("parameter_initial", "parameter_final"):
            snapshots = [r["payload"] for r in records if r["record_type"] == kind]
            valid = len(snapshots) == 1
            for snapshot in snapshots:
                try:
                    digest = _parameter_manifest_digest(snapshot["parameters"])
                except (ValueError, KeyError, TypeError):
                    valid = False
                    continue
                valid = valid and digest == snapshot["manifest_sha256"]
                if kind == "parameter_initial":
                    valid = valid and digest == expected.get("initial_parameter_sha256")
            if not valid:
                missing.append({"comparison_id": "P09", "field_path": f"{side}:{kind}.captured_manifest_identity"})
    stop_alignment = _p11_stop_alignment(original, instrumented)
    first_mismatch: Mismatch | None = None
    ordered_mismatch: Mismatch | None = None
    global_missing: list[dict[str, str]] = []
    left_keys = [(r["comparison_id"], r["record_type"]) for r in original]
    right_keys = [(r["comparison_id"], r["record_type"]) for r in instrumented]
    if left_keys == right_keys:
        for index, (left_row, right_row) in enumerate(zip(original, instrumented)):
            diff = _first_difference(left_row["payload"], right_row["payload"], "payload")
            if diff is not None:
                ordered_mismatch = Mismatch(left_row["comparison_id"], index, *diff)
                break
    elif Counter(left_keys) == Counter(right_keys):
        index = next(i for i, (a, b) in enumerate(zip(left_keys, right_keys)) if a != b)
        ordered_mismatch = Mismatch(original[index]["comparison_id"], index, "record_type",
                                   {"comparison_id": original[index]["comparison_id"], "record_type": original[index]["record_type"]},
                                   {"comparison_id": instrumented[index]["comparison_id"], "record_type": instrumented[index]["record_type"]})
    else:
        left_counts, right_counts = Counter(left_keys), Counter(right_keys)
        for key in sorted(set(left_counts) | set(right_counts)):
            if left_counts[key] != right_counts[key]:
                global_missing.append({"comparison_id": key[0], "field_path": f"ordered_record_presence:{key[1]}"})
    a_by = {f"P{i:02d}": [r for r in original if r["comparison_id"] == f"P{i:02d}"] for i in range(1, 12)}
    b_by = {f"P{i:02d}": [r for r in instrumented if r["comparison_id"] == f"P{i:02d}"] for i in range(1, 12)}
    gaps = {"original": [r for r in original if r["record_type"] == "capture_gap"],
            "instrumented": [r for r in instrumented if r["record_type"] == "capture_gap"]}
    for item in a_by:
        missing_families = []
        for side, stream, by in (("original", original, a_by), ("instrumented", instrumented, b_by)):
            available = {r["record_type"] for r in by[item]}
            missing_families.extend(f"{side}:{kind}" for kind in sorted(CORE_RECORDS[item] - available))
        if missing_families:
            item_status[item] = "INCOMPLETE"
            missing.extend({"comparison_id": item, "field_path": family} for family in missing_families)
            continue
        if any(r["payload"]["requirement_id"] == item for side in gaps for r in gaps[side]):
            item_status[item] = "INCOMPLETE"
            continue
        left = a_by[item]
        right = b_by[item]
        left_compare, right_compare = left, right
        if item == "P02" and stop_alignment is not None and not stop_alignment.get("aligned"):
            failed_side = stop_alignment.get("failed_side")
            failure = stop_alignment.get("failure")
            if failed_side in {"original", "instrumented"} and failure is not None:
                failed_anchor = failure["payload"]["anchor"]
                failed_records = left if failed_side == "original" else right
                failed_row = next((r for r in failed_records if r["record_type"] == "enqueue"
                                   and r["payload"]["anchor"] == failed_anchor
                                   and r["payload"]["admission_outcome"] != "ADMITTED"), None)
                if failed_row is not None:
                    if failed_side == "original":
                        left_compare = [r for r in left if r["record_index"] < failed_row["record_index"]]
                    else:
                        right_compare = [r for r in right if r["record_index"] < failed_row["record_index"]]
        mismatch = None
        for index in range(max(len(left_compare), len(right_compare))):
            if index >= len(left_compare) or index >= len(right_compare):
                mismatch = (index, "record.<presence>", None if index >= len(left_compare) else left_compare[index], None if index >= len(right_compare) else right_compare[index])
                break
            for field in ("record_type", "payload"):
                diff = _first_difference(left_compare[index][field], right_compare[index][field], field)
                if diff is not None:
                    mismatch = (index, *diff)
                    break
            if mismatch:
                break
        if mismatch:
            if mismatch[1] == "record.<presence>":
                item_status[item] = "INCOMPLETE"
                missing.append({"comparison_id": item, "field_path": "record_presence"})
            else:
                item_status[item] = "CONTRADICTED"
                if first_mismatch is None:
                    index, field_path, value_a, value_b = mismatch
                    first_mismatch = Mismatch(item, index, field_path, value_a, value_b)
        elif item == "P02" and stop_alignment is not None and not stop_alignment.get("aligned"):
            item_status[item] = "INCOMPLETE"
            missing.append({"comparison_id": "P02", "field_path": "P11.stop_alignment.counterpart_pre_stop_admission"})
        else:
            item_status[item] = "READY"

    missing.extend(global_missing)
    if ordered_mismatch is not None:
        first_mismatch = ordered_mismatch
        comparison = ordered_mismatch.comparison_id
        if comparison in item_status:
            item_status[comparison] = "CONTRADICTED"
    if stop_alignment is not None and stop_alignment.get("aligned"):
        item_status["P02"] = "CONTRADICTED"
        item_status["P11"] = "CONTRADICTED"
        missing = [m for m in missing if m["comparison_id"] not in {"P02", "P11"}]
        if first_mismatch is None:
            failure = stop_alignment["failure"]["payload"]
            admission = stop_alignment["admission"]["payload"]
            first_mismatch = Mismatch("P02", stop_alignment["failure"]["record_index"],
                                      "payload.admission_outcome", failure.get("admission_outcome"),
                                      admission.get("admission_outcome"))
    branch_maps: dict[str, dict[str, Any]] = {"original": {}, "instrumented": {}}
    for side, stream in (("original", original), ("instrumented", instrumented)):
        for row in stream:
            if row["record_type"] == "branch_state":
                branch = row["payload"]["branch_name"]
                if branch in branch_maps[side]:
                    raise ValueError(f"duplicate conditional branch status: {side}:{branch}")
                payload = row["payload"]
                observed = _branch_observations(stream, branch)
                state = payload["evidence_state"]
                consistent = (state == "EVIDENCE_UNAVAILABLE"
                              or state == "MEASURED_POSITIVE" and payload["occurrences"] == observed
                              or state in {"MEASURED_ZERO", "COMPLETE_UNEXERCISED"} and not observed)
                if not consistent:
                    missing.append({"comparison_id": RECORDS[BRANCH_RECORDS[branch]][0],
                                    "field_path": f"{side}:{branch}.inconsistent_occurrence_evidence"})
                    payload = {**payload, "evidence_state": "EVIDENCE_UNAVAILABLE",
                               "occurrence_count": None, "occurrences": None}
                branch_maps[side][branch] = payload
    branch_status = {name: _branch_pair(branch_maps["original"].get(name), branch_maps["instrumented"].get(name)) for name in BRANCHES}
    if stop_alignment is not None:
        if stop_alignment.get("aligned"):
            branch_status["queue_overflow_drop_failure"] = {
                "original": "MEASURED_POSITIVE" if stop_alignment["failed_side"] == "original" else "EVIDENCE_UNAVAILABLE",
                "instrumented": "MEASURED_POSITIVE" if stop_alignment["failed_side"] == "instrumented" else "EVIDENCE_UNAVAILABLE",
                "pair_outcome": "ONE_SIDED_OCCURRENCE", "comparison_status": "CONTRADICTED",
            }
            item_status["P11"] = "CONTRADICTED"
        else:
            branch_status["queue_overflow_drop_failure"] = {
                "original": "EVIDENCE_UNAVAILABLE", "instrumented": "EVIDENCE_UNAVAILABLE",
                "pair_outcome": "EVIDENCE_UNAVAILABLE", "comparison_status": "INCOMPLETE",
            }
            item_status["P11"] = "INCOMPLETE"
            missing.append({"comparison_id": "P11", "field_path": stop_alignment.get("reason", "stop alignment unavailable")})
            if first_mismatch is not None and first_mismatch.comparison_id == "P11":
                first_mismatch = None
    branch_items = {
        "queue_overflow_drop_failure": "P11",
        "duplicate_feedback": "P08",
        "rejected_feedback": "P08",
        "prediction_expiration": "P03",
        "prediction_settlement": "P03",
        "omission_resolution": "P04",
        "score_tie": "P06",
        "eligibility_expiration": "P07",
        "eligibility_consumption": "P07",
    }
    branch_rows = {
        side: {row["payload"]["branch_name"]: row for row in stream if row["record_type"] == "branch_state"}
        for side, stream in (("original", original), ("instrumented", instrumented))
    }
    for branch, status in branch_status.items():
        item = branch_items[branch]
        if status.get("comparison_status") == "CONTRADICTED":
            item_status[item] = "CONTRADICTED"
            if first_mismatch is None:
                left_state = branch_maps["original"].get(branch)
                right_state = branch_maps["instrumented"].get(branch)
                left_occurrences = None if left_state is None else left_state["occurrences"]
                right_occurrences = None if right_state is None else right_state["occurrences"]
                row = branch_rows["original"].get(branch) or branch_rows["instrumented"].get(branch)
                first_mismatch = Mismatch(item, -1 if row is None else row["record_index"],
                                          f"branch_state.{branch}.occurrences", left_occurrences, right_occurrences)
        elif status["pair_outcome"] == "EVIDENCE_UNAVAILABLE":
            if item_status[item] == "READY":
                item_status[item] = "INCOMPLETE"
            missing.append({"comparison_id": item, "field_path": f"branch_state.{branch}"})
    for evidence in missing:
        item = evidence["comparison_id"]
        if item in item_status and item_status[item] != "CONTRADICTED":
            item_status[item] = "INCOMPLETE"
    if "CONTRADICTED" in item_status.values():
        overall = "CONTRADICTED"
    elif "INCOMPLETE" in item_status.values() or any(s["pair_outcome"] == "EVIDENCE_UNAVAILABLE" for s in branch_status.values()):
        overall = "INCOMPLETE"
    elif any(s["comparison_status"] == "CONTRADICTED" for s in branch_status.values()):
        overall = "CONTRADICTED"
    else:
        overall = "READY"
    return ComparisonReport(
        schema_version="ppc11-paired-trace-1", overall_status=overall,
        item_status=item_status, branch_status=branch_status, first_mismatch=first_mismatch,
        missing_evidence=missing,
        raw={"original": {"path": str(original_path), "sha256": original_hash, "bytes": original_bytes},
             "instrumented": {"path": str(instrumented_path), "sha256": instrumented_hash, "bytes": instrumented_bytes}},
        identities={"expected": expected, "run_ids": {"original": original[0]["run_id"], "instrumented": instrumented[0]["run_id"]}},
    )
