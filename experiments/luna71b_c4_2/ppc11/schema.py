from __future__ import annotations

from collections.abc import Mapping
import json
import math
import re
import struct
from typing import Any

SCHEMA_VERSION = "ppc11-paired-trace-1"
SIDES = {"original", "instrumented"}
ARMS = {"A", "B", "C", "D"}
SPLITS = {"train", "validation", "test"}
COMPARISONS = {*(f"P{i:02d}" for i in range(1, 12)), "BRANCH"}
ENVELOPE_FIELDS = {
    "schema_version", "side", "run_id", "source_revision",
    "runtime_manifest_sha256", "seed", "arm", "split", "example_id",
    "exposure_id", "record_index", "comparison_id", "record_type", "payload",
}

RECORDS: dict[str, tuple[str, frozenset[str]]] = {
    "input_event": ("P01", frozenset({"event_type", "payload", "payload_type", "timestamp", "input_order", "channel_id", "event_id"})),
    "enqueue": ("P02", frozenset({"anchor", "event_type", "payload", "timestamp", "enqueue_order", "queue_sequence", "priority_key", "admission_outcome", "occupancy_before", "occupancy_after"})),
    "schedule": ("P02", frozenset({"anchor", "event_type", "payload", "timestamp", "queue_sequence", "priority_key", "tie_break_cause"})),
    "dequeue": ("P02", frozenset({"anchor", "event_type", "payload", "timestamp", "queue_sequence", "priority_key", "dequeue_order", "tie_break_cause"})),
    "process": ("P02", frozenset({"anchor", "event_type", "payload", "timestamp", "queue_sequence", "process_order"})),
    "prediction_create": ("P03", frozenset({"prediction_id", "expected_symbol", "created_at", "due_at", "expires_at"})),
    "prediction_match": ("P03", frozenset({"prediction_id", "observed_symbol", "matched_at", "outcome"})),
    "prediction_expire": ("P03", frozenset({"prediction_id", "expired_at", "outcome"})),
    "prediction_settle": ("P03", frozenset({"prediction_id", "settled_at", "disposition"})),
    "omission_resolve": ("P04", frozenset({"prediction_id", "omitted_symbol", "omission_at", "outcome"})),
    "omission_route": ("P04", frozenset({"prediction_id", "route", "payload", "event_id", "routed_at"})),
    "omission_delivery": ("P04", frozenset({"prediction_id", "route", "payload", "event_id", "delivered_at", "outcome"})),
    "readout_feature": ("P05", frozenset({"decision_id", "decision_at", "feature"})),
    "readout_drive": ("P06", frozenset({"decision_id", "class_index", "weight", "bias", "feature", "drive"})),
    "readout_activation": ("P06", frozenset({"decision_id", "class_index", "pre_transfer", "post_transfer"})),
    "readout_decision": ("P06", frozenset({"decision_id", "winner", "tie_set", "tie_break_order", "tie_break_result"})),
    "eligibility_create": ("P07", frozenset({"trace_id", "owner", "trace_kind", "value", "created_at", "expires_at"})),
    "eligibility_expire": ("P07", frozenset({"trace_id", "owner", "expired_at", "expiry_boundary", "value"})),
    "eligibility_consume": ("P07", frozenset({"trace_id", "owner", "consumed_at", "value", "outcome"})),
    "eligibility_admission": ("P07", frozenset({"trace_id", "owner", "capacity", "occupancy_before", "decision", "reason"})),
    "feedback_schedule": ("P08", frozenset({"feedback_id", "origin_id", "due_at", "scheduled_at", "sign", "magnitude"})),
    "feedback_apply": ("P08", frozenset({"feedback_id", "origin_id", "due_at", "applied_at", "application_order", "sign", "magnitude"})),
    "feedback_reject": ("P08", frozenset({"feedback_id", "origin_id", "rejected_at", "reason", "duplicate"})),
    "parameter_initial": ("P09", frozenset({"manifest_sha256", "parameters"})),
    "parameter_transition": ("P09", frozenset({"parameter_id", "parameter_kind", "old_value", "new_value", "cause", "transition_order", "timestamp"})),
    "parameter_final": ("P09", frozenset({"manifest_sha256", "parameters"})),
    "classification_output": ("P10", frozenset({"predicted_class", "output_at", "emissions"})),
    "queue_state": ("P11", frozenset({"occupancy", "capacity", "pending"})),
    "admission_decision": ("P11", frozenset({"anchor", "admission_outcome", "occupancy_before", "occupancy_after", "queue_sequence"})),
    "event_processed": ("P11", frozenset({"event_id", "processed_at", "process_order", "processed_count"})),
    "queue_failure": ("P11", frozenset({"anchor", "occupancy", "capacity", "reason"})),
    "terminal_state": ("P11", frozenset({"last_operation", "timestamp", "occupancy", "capacity", "pending"})),
    "branch_state": ("BRANCH", frozenset({"branch_name", "evidence_state", "occurrence_count", "occurrences"})),
    "capture_gap": ("BRANCH", frozenset({"requirement_id", "field_path", "source_point", "reason"})),
}

BRANCHES = (
    "queue_overflow_drop_failure", "duplicate_feedback", "rejected_feedback",
    "prediction_expiration", "prediction_settlement", "omission_resolution",
    "score_tie", "eligibility_expiration", "eligibility_consumption",
)
EVIDENCE_STATES = {"MEASURED_ZERO", "MEASURED_POSITIVE", "COMPLETE_UNEXERCISED", "EVIDENCE_UNAVAILABLE"}
PAIR_OUTCOMES = {"BOTH_ZERO", "EXERCISED_AND_COMPARED", "UNEXERCISED", "ONE_SIDED_OCCURRENCE", "EVIDENCE_UNAVAILABLE"}
ADMISSION_OUTCOMES = {"ADMITTED", "REJECTED_CAPACITY", "REJECTED_INVALID", "OTHER_FAILURE"}


def f64(value: float) -> dict[str, str]:
    if not isinstance(value, float):
        raise TypeError("f64 source value must be a Python float")
    return {"kind": "f64", "bits_be_hex": struct.pack(">d", value).hex()}


def f32_bits(bits_be_hex: str) -> dict[str, str]:
    if not isinstance(bits_be_hex, str) or len(bits_be_hex) != 8 or any(c not in "0123456789abcdef" for c in bits_be_hex):
        raise ValueError("f32 requires eight lowercase hexadecimal digits")
    return {"kind": "f32", "bits_be_hex": bits_be_hex}


def encode_source_value(value: Any) -> Any:
    """Encode source values without JSON numeric coercion or float normalization."""
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, float):
        return f64(value)
    if isinstance(value, int):
        return {"kind": "pyint", "decimal": str(value)}
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise TypeError("source mapping keys must be strings")
        return {"kind": "map", "entries": {key: encode_source_value(item) for key, item in value.items()}}
    if isinstance(value, (list, tuple)):
        return [encode_source_value(item) for item in value]
    if hasattr(value, "value") and isinstance(value.value, (str, int)):
        return encode_source_value(value.value)
    if hasattr(value, "__dataclass_fields__"):
        from dataclasses import asdict
        return encode_source_value(asdict(value))
    raise TypeError(f"unsupported source value type: {type(value).__qualname__}")


def encode_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, Mapping) or any(not isinstance(key, str) for key in payload):
        raise TypeError("record payload must be a string-keyed mapping")
    encoded: dict[str, Any] = {}
    for key, value in payload.items():
        if key == "anchor":
            if not isinstance(value, Mapping) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in value.items()):
                raise TypeError("alignment anchor must be a string mapping")
            encoded[key] = dict(value)
        else:
            encoded[key] = encode_source_value(value)
    return encoded


def _validate_encoded(value: Any, path: str = "payload") -> None:
    if isinstance(value, float):
        raise ValueError(f"JSON numeric float forbidden at {path}; use typed bits")
    if isinstance(value, int) and not isinstance(value, bool):
        raise ValueError(f"JSON numeric integer forbidden in payload at {path}; use typed pyint")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_encoded(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        if value.get("kind") == "f64":
            if set(value) != {"kind", "bits_be_hex"} or not isinstance(value["bits_be_hex"], str) or len(value["bits_be_hex"]) != 16 or any(c not in "0123456789abcdef" for c in value["bits_be_hex"]):
                raise ValueError(f"invalid f64 bits at {path}")
            return
        if value.get("kind") == "f32":
            if set(value) != {"kind", "bits_be_hex"} or not isinstance(value["bits_be_hex"], str) or len(value["bits_be_hex"]) != 8 or any(c not in "0123456789abcdef" for c in value["bits_be_hex"]):
                raise ValueError(f"invalid f32 bits at {path}")
            return
        if value.get("kind") == "pyint":
            if set(value) != {"kind", "decimal"} or not isinstance(value["decimal"], str) or not value["decimal"] or str(int(value["decimal"])) != value["decimal"]:
                raise ValueError(f"invalid pyint at {path}")
            return
        if re.fullmatch(r"[iu](8|16|32|64)", str(value.get("kind"))):
            width = int(value["kind"][1:]) // 4
            if set(value) != {"kind", "bits_be_hex"} or not isinstance(value["bits_be_hex"], str) or not re.fullmatch(rf"[0-9a-f]{{{width}}}", value["bits_be_hex"]):
                raise ValueError(f"invalid fixed-width integer at {path}")
            return
        if value.get("kind") == "map":
            if set(value) != {"kind", "entries"} or not isinstance(value["entries"], dict):
                raise ValueError(f"invalid map encoding at {path}")
            for key, item in value["entries"].items():
                if not isinstance(key, str):
                    raise ValueError(f"non-string map key at {path}")
                _validate_encoded(item, f"{path}.$map.{key}")
            return
        if "kind" in value:
            raise ValueError(f"unsupported typed value at {path}")
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"non-string object key at {path}")
            _validate_encoded(item, f"{path}.{key}")
        return
    if value is not None and not isinstance(value, (str, bool)):
        raise ValueError(f"unsupported JSON value at {path}")


def integer_value(value: Any) -> int:
    if not isinstance(value, dict):
        raise ValueError("expected tagged integer")
    _validate_encoded(value)
    kind = value.get("kind", "")
    if kind == "pyint":
        return int(value["decimal"])
    if re.fullmatch(r"[iu](8|16|32|64)", kind):
        number = int(value["bits_be_hex"], 16)
        width = int(kind[1:])
        return number - (1 << width) if kind[0] == "i" and number >= 1 << (width - 1) else number
    raise ValueError("expected tagged integer")


def _validate_source_value(value: Any) -> None:
    _validate_encoded(value)
    if isinstance(value, list):
        for item in value:
            _validate_source_value(item)
    elif isinstance(value, dict):
        if "kind" not in value:
            raise ValueError("source objects require a tagged map")
        if value["kind"] == "map":
            for item in value["entries"].values():
                _validate_source_value(item)


def _validate_family(kind: str, payload: dict[str, Any]) -> None:
    strings = {
        "event_type", "payload_type", "channel_id", "event_id", "prediction_id",
        "expected_symbol", "observed_symbol", "outcome", "disposition",
        "omitted_symbol", "decision_id", "trace_id", "owner", "trace_kind",
        "expiry_boundary", "decision", "reason", "feedback_id", "origin_id",
        "manifest_sha256", "parameter_id", "parameter_kind", "cause",
        "admission_outcome", "last_operation", "branch_name", "evidence_state",
        "requirement_id", "field_path", "source_point",
    }
    integers = {
        "input_order", "enqueue_order", "queue_sequence", "occupancy_before",
        "occupancy_after", "dequeue_order", "process_order", "class_index",
        "winner", "tie_break_result", "capacity", "application_order", "sign",
        "transition_order", "predicted_class", "occupancy", "processed_count",
    }
    numbers = {
        "timestamp", "created_at", "due_at", "expires_at", "matched_at",
        "expired_at", "settled_at", "omission_at", "routed_at", "delivered_at",
        "decision_at", "feature", "weight", "bias", "drive", "pre_transfer",
        "post_transfer", "value", "consumed_at", "scheduled_at", "applied_at",
        "magnitude", "rejected_at", "old_value", "new_value", "output_at",
        "processed_at",
    }
    for field, value in payload.items():
        if field != "anchor":
            _validate_source_value(value)
        if field in strings:
            if not isinstance(value, str) or not value:
                raise ValueError(f"{kind}.{field} requires a non-empty string")
        elif field in integers:
            if field == "queue_sequence" and value is None and payload.get("admission_outcome") != "ADMITTED":
                continue
            if field == "sign":
                signs = value if isinstance(value, list) else [value]
                if isinstance(value, list) and len(signs) != 4:
                    raise ValueError("feedback sign vector requires four class values")
                if any(integer_value(sign) not in {-1, 0, 1} for sign in signs):
                    raise ValueError("invalid feedback sign")
                continue
            number = integer_value(value)
            if number < 0 and not (field == "queue_sequence" and payload.get("admission_outcome") != "ADMITTED" and number == -1):
                raise ValueError(f"{kind}.{field} requires a nonnegative integer")
            if field in {"class_index", "winner", "tie_break_result", "predicted_class"} and number not in range(4):
                raise ValueError(f"{kind}.{field} requires a four-class index")
        elif field in numbers:
            if value is None and ((kind == "terminal_state" and field == "timestamp") or field == "expires_at"):
                continue
            if not isinstance(value, dict) or value.get("kind") not in {"f32", "f64", "pyint", "i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64"}:
                raise ValueError(f"{kind}.{field} requires a tagged numeric source value")
            if field in {"feature", "weight", "bias", "drive", "pre_transfer", "post_transfer",
                         "old_value", "new_value", "magnitude"} and value["kind"] not in {"f32", "f64"}:
                raise ValueError(f"{kind}.{field} requires source float bits")
        elif field == "duplicate":
            if type(value) is not bool:
                raise ValueError("feedback duplicate requires bool")
        elif field in {"tie_set", "tie_break_order"}:
            if not isinstance(value, list):
                raise ValueError(f"{field} requires an ordered list")
            indices = [integer_value(item) for item in value]
            if not indices or len(indices) != len(set(indices)) or any(i not in range(4) for i in indices):
                raise ValueError(f"invalid {field}")
            if field == "tie_break_order" and set(indices) != set(range(4)):
                raise ValueError("tie_break_order requires all four classes")
        elif field == "priority_key":
            if not isinstance(value, list) or len(value) != 2:
                raise ValueError("priority_key requires timestamp and sequence")
            _validate_family(kind, {"timestamp": value[0], "queue_sequence": value[1],
                                    "admission_outcome": payload.get("admission_outcome", "ADMITTED")})
        elif field in {"parameters"}:
            if not isinstance(value, dict) or value.get("kind") != "map" or not value["entries"]:
                raise ValueError("parameters require a nonempty typed source map")
        elif field in {"route", "emissions", "pending"}:
            if not isinstance(value, list):
                raise ValueError(f"{field} requires an ordered list")
            if field == "route" and (not value or any(not isinstance(item, str) or not item for item in value)):
                raise ValueError("route requires nonempty identities")
            if field in {"emissions", "pending"} and any(not isinstance(item, dict) or item.get("kind") != "map" for item in value):
                raise ValueError(f"{field} requires typed source objects")
        elif field == "tie_break_cause":
            if value is None and kind == "schedule":
                continue
            if value not in {"timestamp_then_assigned_sequence", "external_before_internal_same_destination_same_timestamp"}:
                raise ValueError("invalid observed tie-break cause")
        elif field not in {"anchor", "payload", "occurrence_count", "occurrences"}:
            raise ValueError(f"unvalidated family field: {kind}.{field}")
    if "manifest_sha256" in payload and not re.fullmatch(r"[0-9a-f]{64}", payload["manifest_sha256"]):
        raise ValueError("invalid manifest SHA-256")
    if kind == "terminal_state" and payload["last_operation"] not in {"before_first_event", "enqueue", "dequeue", "process"}:
        raise ValueError("terminal last_operation must be a completed P02 operation")
    if kind == "input_event":
        expected_type = payload["payload_type"]
        value = payload["payload"]
        supported = {"str": isinstance(value, str), "bool": type(value) is bool,
                     "float": isinstance(value, dict) and value.get("kind") == "f64",
                     "int": isinstance(value, dict) and value.get("kind") == "pyint",
                     "dict": isinstance(value, dict) and value.get("kind") == "map",
                     "list": isinstance(value, list), "NoneType": value is None}
        if not supported.get(expected_type, False):
            raise ValueError("input payload_type does not establish encoded source type")


def validate_record(row: Any, *, expected_side: str | None = None) -> None:
    if not isinstance(row, dict) or set(row) != ENVELOPE_FIELDS:
        raise ValueError("record envelope has missing or unknown fields")
    if row["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported schema_version")
    if not isinstance(row["side"], str) or row["side"] not in SIDES or (expected_side is not None and row["side"] != expected_side):
        raise ValueError("invalid or unexpected side")
    for field in ("run_id", "source_revision", "runtime_manifest_sha256", "example_id", "exposure_id"):
        if not isinstance(row[field], str) or not row[field]:
            raise ValueError(f"{field} must be a non-empty string")
    if len(row["runtime_manifest_sha256"]) != 64 or any(c not in "0123456789abcdef" for c in row["runtime_manifest_sha256"]):
        raise ValueError("runtime_manifest_sha256 must be lowercase SHA-256")
    if not re.fullmatch(r"[0-9a-f]{40}\+sha256:[0-9a-f]{64}", row["source_revision"]):
        raise ValueError("source_revision requires a Git commit and source-manifest SHA-256")
    if isinstance(row["seed"], bool) or not isinstance(row["seed"], int) or row["seed"] != 17:
        raise ValueError("seed must be typed integer 17")
    if not isinstance(row["arm"], str) or not isinstance(row["split"], str) or row["arm"] not in ARMS or row["split"] not in SPLITS:
        raise ValueError("invalid arm or split")
    if isinstance(row["record_index"], bool) or not isinstance(row["record_index"], int) or row["record_index"] < 0:
        raise ValueError("record_index must be a nonnegative integer")
    if not isinstance(row["comparison_id"], str) or row["comparison_id"] not in COMPARISONS:
        raise ValueError("invalid comparison_id")
    if not isinstance(row["record_type"], str) or row["record_type"] not in RECORDS:
        raise ValueError("unknown record_type")
    comparison, required = RECORDS[row["record_type"]]
    if row["comparison_id"] != comparison:
        raise ValueError("record_type/comparison_id mismatch")
    if not isinstance(row["payload"], dict) or set(row["payload"]) != required:
        raise ValueError(f"{row['record_type']} payload has missing or unknown fields")
    _validate_encoded(row["payload"])
    _validate_family(row["record_type"], row["payload"])
    if row["record_type"] in {"enqueue", "schedule", "dequeue", "process", "admission_decision", "queue_failure"}:
        anchor = row["payload"].get("anchor")
        if not isinstance(anchor, dict) or set(anchor) != {"exposure_id", "event_id", "source", "destination", "event_type"}:
            raise ValueError("P02/P11 alignment anchor must have exactly five fields")
        if any(not isinstance(anchor[key], str) or not anchor[key] for key in anchor):
            raise ValueError("P02/P11 anchor fields must be non-empty strings")
        if anchor["exposure_id"] != row["exposure_id"] or ("event_type" in row["payload"] and anchor["event_type"] != row["payload"]["event_type"]):
            raise ValueError("anchor differs from captured event/exposure")
    if row["record_type"] == "enqueue" and row["payload"]["admission_outcome"] not in ADMISSION_OUTCOMES:
        raise ValueError("invalid admission_outcome")
    if row["record_type"] == "admission_decision" and row["payload"]["admission_outcome"] not in ADMISSION_OUTCOMES:
        raise ValueError("invalid admission_outcome")
    if row["record_type"] == "branch_state":
        payload = row["payload"]
        if payload["branch_name"] not in BRANCHES or payload["evidence_state"] not in EVIDENCE_STATES:
            raise ValueError("invalid conditional branch state")
        state = payload["evidence_state"]
        count, occurrences = payload["occurrence_count"], payload["occurrences"]
        if state == "MEASURED_POSITIVE":
            if not isinstance(occurrences, list) or integer_value(count) <= 0 or integer_value(count) != len(occurrences):
                raise ValueError("positive branch state requires a positive measured counter and occurrence records")
            if any(not isinstance(item, dict) or item.get("kind") != "map" for item in occurrences):
                raise ValueError("positive branch occurrences require typed source record objects")
        elif state == "MEASURED_ZERO":
            if not isinstance(count, dict) or count.get("kind") != "pyint" or count["decimal"] != "0" or occurrences != []:
                raise ValueError("measured-zero state requires an explicit zero counter and empty occurrence records")
        elif state == "COMPLETE_UNEXERCISED":
            if count is not None or occurrences is not None:
                raise ValueError("complete-unexercised state cannot invent a zero counter")
        elif count is not None or occurrences is not None:
            raise ValueError("unavailable state must not claim an occurrence count")


def canonical_line(row: dict[str, Any]) -> bytes:
    validate_record(row)
    return (json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
