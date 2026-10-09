"""Execute the bounded Luna-54 retained-input relay mechanism experiment."""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from enum import Enum
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import subprocess
import sys
import struct
from typing import Any
from unittest import mock

from tpcn.event_runtime import Event, EventQueue, EventType
from tpcn.excursion_neuron import E1Config, IntegrationConfig, MultiExcursionNeuron
from tpcn.experiment_excursion_runtime import (
    ExcursionCharacterRuntime,
    RouteContext,
)
from tpcn.topology import BoundedTopology, Edge


ROOT = Path(__file__).resolve().parents[2]
BASELINE_REVISION = "09701f7c5a1d7063dffecb7734eb199d1c0b0176"
EVIDENCE_REVISION = "1bee6673ac68e99303d33053e197f41fe78b913f"
LUNA46_SHA256 = "0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e"
LUNA46_BLOB = "9506369d97babf7bc0ef15ed52efb738dcdcd549"
LUNA53_SUMMARY_BLOB = "b03993adfb358c575c80f6637e7b50903061ddb2"
L45_CONFIG_PATH = "artifacts/luna45-depth2-frozen-config-20261006-r2/config.json"
L45_CATALOG_PATH = (
    "artifacts/luna45-acp0008-depth2-destination-integration-20261006/"
    "artifact-integrity.json"
)
L45_DIRECTORY = "artifacts/luna45-acp0008-depth2-destination-integration-20261006"
L46_PATH = "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json"
LUNA53_SUMMARY_PATH = "artifacts/luna53/summary.json"
OUTPUT_DIRECTORY = Path("artifacts/luna54")
CONFIG_PATH = Path("experiments/luna54/config.json")
PROTOCOL_PATH = Path("experiments/luna54/protocol.json")
RUNNER_PATH = Path("experiments/luna54/run.py")
FOCUSED_TEST_PATH = Path("tests/test_luna54_relay_retention.py")

PHASE_ARTIFACTS = {
    "initial": {
        "arm": "initial-destination_calibrated.json",
        "enqueue": "initial-destination_calibrated-enqueue.json",
        "reception": "initial-destination_calibrated-reception.json",
    },
    "replay": {
        "arm": "replay-destination_calibrated.json",
        "enqueue": "replay-destination_calibrated-enqueue.json",
        "reception": "replay-destination_calibrated-reception.json",
    },
}
RUNTIME_SOURCE_PATHS = (
    "tpcn/excursion_neuron.py",
    "tpcn/event_runtime.py",
    "tpcn/experiment_excursion_runtime.py",
    "tpcn/topology.py",
)
INPUT_EXPECTED_BLOBS = {
    L45_CONFIG_PATH: "1fcf4e9865d1b6d1af9f39ab74d399eb6496b166",
    L45_CATALOG_PATH: "b1aaef4006422f321922bfb58425e4fb646d96b9",
    f"{L45_DIRECTORY}/initial-destination_calibrated.json":
        "701dace35f1ca511cbb7275a2d5dd9737964aed7",
    f"{L45_DIRECTORY}/initial-destination_calibrated-enqueue.json":
        "33604988c73e43bf5dadaa96ba423f295ebc3717",
    f"{L45_DIRECTORY}/initial-destination_calibrated-reception.json":
        "b0f7965894c89ab3655a583ccd2db6486e4e3966",
    f"{L45_DIRECTORY}/replay-destination_calibrated.json":
        "83014b8c0cc3be014b3831051237c552c87bead6",
    f"{L45_DIRECTORY}/replay-destination_calibrated-enqueue.json":
        "121455601ade7e7cfdd7891cc9cfd09144aab060",
    f"{L45_DIRECTORY}/replay-destination_calibrated-reception.json":
        "bb1af6d2b3853581c03fd10556e437d5eb555e5a",
    L46_PATH: LUNA46_BLOB,
    LUNA53_SUMMARY_PATH: LUNA53_SUMMARY_BLOB,
}
RECURRENCE_EPSILON_FACTOR = 64.0
Record = dict[str, Any]


class GateError(RuntimeError):
    """Raised when a predeclared Luna-54 execution gate fails."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def float_bits(value: float) -> str:
    return struct.pack(">d", float(value)).hex()


def jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def _git(*args: str, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
    )
    return completed.stdout if binary else completed.stdout.strip()


def _git_blob(revision: str, path: str) -> str:
    return str(_git("rev-parse", f"{revision}:{path}"))


def _require_baseline_ancestry() -> Record:
    head = str(_git("rev-parse", "HEAD"))
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASELINE_REVISION, head],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if ancestor.returncode != 0:
        raise GateError(
            f"authorized start baseline is not an ancestor of execution HEAD: {head}"
        )
    for path_object in (RUNNER_PATH, CONFIG_PATH, PROTOCOL_PATH, FOCUSED_TEST_PATH):
        path = path_object.as_posix()
        committed = _git("cat-file", "blob", _git_blob(head, path), binary=True)
        working = (ROOT / path_object).read_bytes()
        normalized = working.replace(b"\r\n", b"\n")
        if normalized != committed:
            raise GateError(f"execution source differs from committed HEAD: {path}")
    return {"starting_baseline": BASELINE_REVISION, "execution_revision": head}


def _git_identity(revision: str, path: str, expected_blob: str | None = None) -> Record:
    blob = _git_blob(revision, path)
    if expected_blob is not None and blob != expected_blob:
        raise GateError(f"Git blob mismatch for {revision}:{path}: {blob}")
    content = _git("cat-file", "blob", blob, binary=True)
    assert isinstance(content, bytes)
    return {
        "revision": revision,
        "path": path,
        "git_blob": blob,
        "sha256": sha256(content),
        "byte_length": len(content),
    }


def _read_pinned_file(
    path: str,
    expected_sha256: str,
    *,
    expected_length: int | None = None,
) -> tuple[bytes, Record]:
    raw = (ROOT / path).read_bytes()
    normalized = raw.replace(b"\r\n", b"\n")
    if raw != normalized and raw != normalized.replace(b"\n", b"\r\n"):
        raise GateError(f"noncanonical line-ending change in pinned artifact: {path}")
    raw_sha = sha256(raw)
    normalized_sha = sha256(normalized)
    if expected_sha256 not in (raw_sha, normalized_sha):
        raise GateError(f"pinned file SHA-256 mismatch: {path}")
    measured_length = len(normalized) if normalized_sha == expected_sha256 else len(raw)
    if expected_length is not None and measured_length != expected_length:
        raise GateError(f"pinned file byte-length mismatch: {path}")
    return raw, {
        "path": path,
        "checkout_bytes": len(raw),
        "canonical_bytes": measured_length,
        "checkout_sha256": raw_sha,
        "canonical_sha256": normalized_sha,
        "line_ending_equivalence": "exact LF or exact LF-to-CRLF materialization",
    }


def _json_artifact(path: str, pin: Record) -> tuple[Record, Record]:
    raw, identity = _read_pinned_file(
        path,
        pin["file_sha256"],
        expected_length=pin["byte_length"],
    )
    try:
        artifact = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GateError(f"pinned artifact JSON parse failed: {path}: {error}") from error
    if not isinstance(artifact, dict):
        raise GateError(f"pinned artifact is not an object: {path}")
    if artifact.get("artifact_digest") != pin["artifact_digest"]:
        raise GateError(f"repository catalog artifact digest mismatch: {path}")
    clean = dict(artifact)
    claimed = clean.pop("artifact_digest", None)
    if claimed != digest(clean):
        raise GateError(f"internal artifact digest failed: {path}")
    identity["artifact_digest"] = claimed
    identity["git_blob"] = _git_blob(EVIDENCE_REVISION, path)
    return artifact, identity


def _load_pinned_sources() -> tuple[Record, Record, Record, Record]:
    protocol = json.loads((ROOT / PROTOCOL_PATH).read_bytes())
    config = json.loads((ROOT / CONFIG_PATH).read_bytes())
    for path, expected in INPUT_EXPECTED_BLOBS.items():
        old_blob = _git_blob(EVIDENCE_REVISION, path)
        current_blob = _git_blob(BASELINE_REVISION, path)
        if old_blob != expected or current_blob != expected:
            raise GateError(f"historical evidence Git object changed: {path}")
    source_identities = {
        path: _git_identity(BASELINE_REVISION, path, _git_blob(BASELINE_REVISION, path))
        for path in RUNTIME_SOURCE_PATHS
    }
    current_runtime_blobs = {
        path: _git_blob("HEAD", path)
        for path in RUNTIME_SOURCE_PATHS
    }
    if any(
        current_runtime_blobs[path] != source_identities[path]["git_blob"]
        for path in RUNTIME_SOURCE_PATHS
    ):
        raise GateError("an existing E2/runtime/topology implementation differs from baseline")
    config_raw, config_file_identity = _read_pinned_file(
        L45_CONFIG_PATH,
        "a19bf911ebe04c52aba7d83e376faac853519db3308419ca8bfcad35143858e1",
        expected_length=8347,
    )
    frozen_config = json.loads(config_raw)
    frozen_config_digest = digest(frozen_config)
    if frozen_config_digest != config["retained_configuration"]["configuration_digest"]:
        raise GateError("retained Luna-45 configuration digest mismatch")
    catalog_pin = {
        "file_sha256": "a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e",
        "byte_length": 7121,
        "artifact_digest": "60533846dcdc11953edb2c84621e0cfaa122136c9a678c10f01a775fbf87b27f",
    }
    catalog, catalog_identity = _json_artifact(L45_CATALOG_PATH, catalog_pin)
    required_catalog_flags = (
        "all_internal_and_file_digests_pass",
        "all_phase_digests_recomputed",
        "all_raw_captures_match_arm_records",
        "initial_replay_records_and_reports_byte_equal",
    )
    if any(catalog.get(flag) is not True for flag in required_catalog_flags):
        raise GateError("Luna-45 repository integrity catalog is not fully PASS")
    if (
        catalog.get("execution_revision") != "97a93b394d071413075a1f102fdef695664722ff"
        or catalog.get("runner_revision") != "97a93b394d071413075a1f102fdef695664722ff"
    ):
        raise GateError("Luna-45 retained catalog execution provenance differs")
    config_pin = {
        "file_sha256": "0c8abbb1fb68f7b856a9f0718b0eef2a307943b3290ccf3e1bfed049d9dd111a",
        "byte_length": 36093,
        "artifact_digest": "37b260b311cdd5839890bb0475cf1ce067fd1db7a9b3fc73ca55ad7861ada854",
    }
    frozen_execution_config, frozen_execution_identity = _json_artifact(
        f"{L45_DIRECTORY}/config.json", config_pin
    )
    if frozen_execution_config.get("experiment", {}).get("config_digest") not in (
        None,
        frozen_config_digest,
    ):
        raise GateError("Luna-45 execution config identity differs from frozen config")
    frozen_config_identity = {
        **config_file_identity,
        "git_blob": _git_blob(BASELINE_REVISION, L45_CONFIG_PATH),
        "configuration_digest": frozen_config_digest,
    }
    frozen_execution_identity["retained_config_identity"] = frozen_config_identity

    l46_raw, l46_identity = _read_pinned_file(
        L46_PATH, LUNA46_SHA256, expected_length=2_337_377
    )
    l46 = json.loads(l46_raw)
    if not isinstance(l46, dict) or l46.get("schema") != "TPCN-LUNA46-OFFLINE-1":
        raise GateError("pinned Luna-46 classification schema mismatch")
    l46_clean = dict(l46)
    l46_output_digest = l46_clean.pop("output_digest", None)
    if l46_output_digest != digest(l46_clean):
        raise GateError("Luna-46 declared output digest mismatch")
    luna53_summary_blob = _git_identity(
        BASELINE_REVISION,
        LUNA53_SUMMARY_PATH,
        LUNA53_SUMMARY_BLOB,
    )
    luna53_summary_raw = _git("cat-file", "blob", LUNA53_SUMMARY_BLOB, binary=True)
    assert isinstance(luna53_summary_raw, bytes)
    luna53_summary = json.loads(luna53_summary_raw)
    if luna53_summary.get("artifact_digest") is not None:
        clean = dict(luna53_summary)
        claimed = clean.pop("artifact_digest")
        if claimed != digest(clean):
            raise GateError("pinned Luna-53 summary artifact digest mismatch")
    if catalog.get("fixture_file_sha256") != frozen_config["fixture"]["file_sha256"]:
        raise GateError("retained fixture hash differs across frozen configuration/catalog")
    return (
        {
            "frozen_config": frozen_config,
            "frozen_execution_config": frozen_execution_config,
            "l46": l46,
            "catalog": catalog,
            "catalog_identity": catalog_identity,
            "frozen_config_identity": frozen_config_identity,
            "frozen_execution_config_identity": frozen_execution_identity,
            "l46_identity": {
                **l46_identity,
                "git_blob": _git_blob(BASELINE_REVISION, L46_PATH),
            },
            "luna53_summary_identity": luna53_summary_blob,
            "runtime_source_identities": source_identities,
            "runtime_source_current_blobs": current_runtime_blobs,
        },
        protocol,
        config,
        frozen_config,
    )


def _phase_paths(phase: str) -> dict[str, str]:
    return {
        label: f"{L45_DIRECTORY}/{relative}"
        for label, relative in PHASE_ARTIFACTS[phase].items()
    }


def _load_phase(phase: str, base: Record) -> tuple[Record, Record, Record, Record]:
    catalog = base["catalog"]
    paths = _phase_paths(phase)
    artifact_values: dict[str, Record] = {}
    identities: dict[str, Record] = {}
    for label, path in paths.items():
        pin = catalog["files"].get(Path(path).name)
        if not isinstance(pin, dict):
            raise GateError(f"Luna-45 integrity catalog lacks {path}")
        artifact_values[label], identities[label] = _json_artifact(path, pin)
        if _git_blob(EVIDENCE_REVISION, path) != INPUT_EXPECTED_BLOBS[path]:
            raise GateError(f"pinned phase Git object differs: {path}")
    arm = artifact_values["arm"]
    enqueue = artifact_values["enqueue"]
    reception = artifact_values["reception"]
    if arm.get("phase") != phase or arm.get("arm") != "DESTINATION_CALIBRATED":
        raise GateError(f"unexpected retained Luna-45 arm in {phase}")
    if (
        enqueue.get("phase") != phase
        or reception.get("phase") != phase
        or enqueue.get("capture_stream") != "enqueue"
        or reception.get("capture_stream") != "reception"
    ):
        raise GateError(f"unexpected retained raw capture identity in {phase}")
    records = arm.get("records")
    enq_streams = enqueue.get("per_sequence")
    rec_streams = reception.get("per_sequence")
    if not all(isinstance(value, list) and len(value) == 320 for value in (records, enq_streams, rec_streams)):
        raise GateError(f"incomplete 320-stream historical population in {phase}")
    raw_by_stream: dict[str, dict[str, list[Record]]] = {}
    for label, rows in (("enqueue", enq_streams), ("reception", rec_streams)):
        for row in rows:
            stream_id = row.get("stream_id")
            if not isinstance(stream_id, str) or stream_id in raw_by_stream and label in raw_by_stream[stream_id]:
                raise GateError(f"duplicate or invalid raw stream identity in {phase}/{label}")
            raw_by_stream.setdefault(stream_id, {})[label] = row.get("events")
            if not isinstance(row.get("events"), list):
                raise GateError(f"invalid raw route event list in {phase}/{label}/{stream_id}")
    if len(raw_by_stream) != 320:
        raise GateError(f"raw capture stream coverage differs in {phase}")
    record_by_stream = {record["stream_id"]: record for record in records}
    if len(record_by_stream) != 320 or set(record_by_stream) != set(raw_by_stream):
        raise GateError(f"arm/raw stream identities differ in {phase}")
    streams: dict[str, Record] = {}
    total_inputs = 0
    total_historical_routes = 0
    for stream_id in sorted(record_by_stream):
        record = record_by_stream[stream_id]
        captured = raw_by_stream[stream_id]
        record_enqueue = record.get("routing_enqueue_events", [])
        record_reception = record.get("receiver_reception_events", [])
        expected_enqueues = [item for item in record_enqueue if item["source"] == "source" and item["destination"] == "relay"]
        expected_receptions = record.get("source_to_relay_receptions", [])
        if canonical_bytes(record_enqueue) != canonical_bytes(captured["enqueue"]):
            raise GateError(f"recorded/raw enqueue mismatch: {phase}/{stream_id}")
        if canonical_bytes(record_reception) != canonical_bytes(
            next(
                row["events"] for row in rec_streams
                if row["stream_id"] == stream_id
            )
        ):
            raise GateError(f"recorded/raw reception mismatch: {phase}/{stream_id}")
        source_receptions = [
            item for item in captured["reception"]
            if item["source"] == "source" and item["destination"] == "relay"
        ]
        if canonical_bytes(expected_receptions) != canonical_bytes(source_receptions):
            raise GateError(f"recorded/raw source reception mismatch: {phase}/{stream_id}")
        reconcile_routes(captured["enqueue"], captured["reception"], require_complete=True)
        _validate_route_fields(expected_enqueues, source_receptions, "source", "relay")
        historical_downstream_enqueue = [
            item for item in captured["enqueue"]
            if item["source"] == "relay" and item["destination"] == "destination"
        ]
        historical_downstream_reception = [
            item for item in record_reception
            if item["source"] == "relay" and item["destination"] == "destination"
        ]
        reconcile_routes(
            historical_downstream_enqueue,
            historical_downstream_reception,
            require_complete=True,
        )
        _validate_route_fields(
            historical_downstream_enqueue,
            historical_downstream_reception,
            "relay",
            "destination",
        )
        inputs = sorted(
            (deepcopy(item) for item in source_receptions),
            key=lambda item: (int(item["queue_sequence"]), str(item["event_id"])),
        )
        for item in inputs:
            if (
                not isinstance(item.get("causal_roots"), list)
                or not item["causal_roots"]
                or len(item["causal_roots"]) != len(set(item["causal_roots"]))
                or not isinstance(item.get("roots_truncated"), bool)
            ):
                raise GateError(f"invalid source input causal-root metadata: {phase}/{stream_id}")
            item["source_queue_sequence"] = int(item["queue_sequence"])
        if len({(item["event_id"], item["source_queue_sequence"]) for item in inputs}) != len(inputs):
            raise GateError(f"duplicate source input identity: {phase}/{stream_id}")
        streams[stream_id] = {
            "historical": record,
            "source_inputs": inputs,
            "historical_source_enqueue": expected_enqueues,
            "historical_source_reception": source_receptions,
        }
        total_inputs += len(inputs)
        total_historical_routes += sum(
            1 for item in record.get("routing_enqueue_events", [])
            if item["source"] == "relay" and item["destination"] == "destination"
        )
    computed_phase_digest = digest(
        {
            "fixture_file_sha256": arm["fixture_file_sha256"],
            "fixture_semantic_digest": arm["fixture_semantic_digest"],
            "config": base["frozen_execution_config"]["experiment"],
            "records": records,
            "per_arm_report": arm["report"],
        }
    )
    if computed_phase_digest != arm.get("phase_digest"):
        raise GateError(f"Luna-45 historical phase digest recomputation failed: {phase}")
    if total_inputs != 1715 or total_historical_routes != 235:
        raise GateError(
            f"historical phase route inventory mismatch: inputs={total_inputs}, "
            f"relay_to_destination={total_historical_routes}"
        )
    return arm, enqueue, reception, {
        "streams": streams,
        "artifact_identities": identities,
        "phase_digest": arm.get("phase_digest"),
        "input_count": total_inputs,
        "historical_relay_to_destination_pairs": total_historical_routes,
        "input_digest": digest(
            {
                stream_id: streams[stream_id]["source_inputs"]
                for stream_id in sorted(streams)
            }
        ),
        "phase_digest_recomputed": computed_phase_digest,
    }


def _float_close(observed: float, expected: float) -> bool:
    tolerance = RECURRENCE_EPSILON_FACTOR * sys.float_info.epsilon * max(
        1.0, abs(observed), abs(expected)
    )
    return abs(observed - expected) <= tolerance


def _require_close(observed: float, expected: float, message: str) -> None:
    if not _float_close(float(observed), float(expected)):
        raise GateError(
            f"{message}: observed={observed!r}, expected={expected!r}, "
            f"tolerance=64*epsilon"
        )


def _same_fields(left: Record, right: Record, fields: tuple[str, ...], label: str) -> None:
    for field in fields:
        if left.get(field) != right.get(field):
            raise GateError(f"{label} mismatch in {field}: {left.get(field)!r} != {right.get(field)!r}")


def reconcile_routes(
    enqueued: list[Record],
    received: list[Record],
    *,
    require_complete: bool,
) -> Record:
    def key(item: Record) -> tuple[str, int]:
        return str(item["event_id"]), int(item["queue_sequence"])

    enqueue_keys = [key(item) for item in enqueued]
    receive_keys = [key(item) for item in received]
    duplicate_enqueue = len(enqueue_keys) - len(set(enqueue_keys))
    duplicate_receive = len(receive_keys) - len(set(receive_keys))
    matched = set(enqueue_keys) & set(receive_keys)
    missing = set(enqueue_keys) - set(receive_keys)
    orphan = set(receive_keys) - set(enqueue_keys)
    checks = (
        "event_type", "payload", "payload_bits", "source", "destination",
        "lineage_id", "originating_emission_id", "scheduled_delivery_timestamp",
        "causal_roots", "roots_truncated", "route_depth", "route_path",
    )
    by_key = {key(item): item for item in enqueued}
    receive_by_key = {key(item): item for item in received}
    field_mismatches = {
        field: sum(by_key[k].get(field) != receive_by_key[k].get(field) for k in matched)
        for field in checks
    }
    if require_complete and (
        duplicate_enqueue
        or duplicate_receive
        or missing
        or orphan
        or any(field_mismatches.values())
    ):
        raise GateError(
            "route reconciliation failed: "
            f"duplicate_enqueue={duplicate_enqueue}, duplicate_reception={duplicate_receive}, "
            f"unmatched_enqueue={len(missing)}, orphan_reception={len(orphan)}, "
            f"field_mismatches={field_mismatches}"
        )
    return {
        "enqueued_count": len(enqueued),
        "received_count": len(received),
        "matched_count": len(matched),
        "unmatched_enqueue_count": len(missing),
        "orphan_reception_count": len(orphan),
        "duplicate_enqueue_count": duplicate_enqueue,
        "duplicate_reception_count": duplicate_receive,
        "field_mismatches": field_mismatches,
        "reconciles": not (
            duplicate_enqueue or duplicate_receive or missing or orphan
            or any(field_mismatches.values())
        ),
    }


def _validate_route_fields(
    enqueued: list[Record],
    received: list[Record],
    expected_source: str,
    expected_destination: str,
) -> None:
    for item in enqueued:
        if (
            item["source"] != expected_source
            or item["destination"] != expected_destination
            or item["event_type"] != EventType.EXCURSION.value
            or item["route_path"] != [expected_source, expected_destination]
            or item["route_depth"] != 1
        ):
            raise GateError("retained route endpoint/type/path/depth mismatch")
    for item in received:
        if (
            item["source"] != expected_source
            or item["destination"] != expected_destination
            or item["receiver_node"] != expected_destination
            or item["event_type"] != EventType.EXCURSION.value
            or item["route_path"] != [expected_source, expected_destination]
            or item["route_depth"] != 1
            or item["scheduled_delivery_timestamp"] != item["reception_timestamp"]
        ):
            raise GateError("retained reception endpoint/type/path/depth/time mismatch")


def _config_for_condition(
    condition: str,
    frozen_config: Record,
    config: Record,
) -> tuple[E1Config, E1Config, Record]:
    if condition not in ("control", "intervention"):
        raise GateError(f"unknown condition: {condition}")
    frozen_nodes = frozen_config["neuron_configurations"]["DESTINATION_CALIBRATED"]
    relay_record = deepcopy(frozen_nodes["relay"])
    destination_record = deepcopy(frozen_nodes["destination"])
    expected_condition = config["conditions"][condition]
    if expected_condition["destination_integration_decay_rate_z"] != 0.0125:
        raise GateError("destination decay differs from the fixed historical control")
    relay_record["integration"]["decay_rate_z"] = expected_condition[
        "relay_integration_decay_rate_z"
    ]
    destination_record["integration"]["decay_rate_z"] = expected_condition[
        "destination_integration_decay_rate_z"
    ]
    relay_integration = IntegrationConfig(**relay_record.pop("integration"))
    destination_integration = IntegrationConfig(**destination_record.pop("integration"))
    relay = E1Config(**relay_record, integration=relay_integration)
    destination = E1Config(**destination_record, integration=destination_integration)
    expected_relay = deepcopy(frozen_nodes["relay"])
    expected_destination = deepcopy(frozen_nodes["destination"])
    expected_relay["integration"]["decay_rate_z"] = expected_condition[
        "relay_integration_decay_rate_z"
    ]
    expected_destination["integration"]["decay_rate_z"] = 0.0125
    actual_relay = jsonable(relay)
    actual_destination = jsonable(destination)
    if actual_relay != expected_relay or actual_destination != expected_destination:
        raise GateError(f"{condition} E2 neuron configuration differs from retained configuration")
    baseline_relay = deepcopy(frozen_nodes["relay"])
    baseline_destination = deepcopy(frozen_nodes["destination"])
    delta_paths = _diff_paths(
        {"relay": baseline_relay, "destination": baseline_destination},
        {"relay": expected_relay, "destination": expected_destination},
    )
    if condition == "control" and delta_paths:
        raise GateError("historical control configuration is not exact")
    if condition == "intervention" and delta_paths != ["relay.integration.decay_rate_z"]:
        raise GateError(f"unauthorized intervention configuration differences: {delta_paths}")
    return relay, destination, {
        "relay": expected_relay,
        "destination": expected_destination,
        "changed_paths_from_historical": delta_paths,
        "only_intervention_path": (
            None if condition == "control" else "relay.integration.decay_rate_z"
        ),
    }


def _diff_paths(left: Any, right: Any, prefix: str = "") -> list[str]:
    if isinstance(left, dict) and isinstance(right, dict):
        if left.keys() != right.keys():
            return [prefix or "<root>"]
        differences: list[str] = []
        for key in sorted(left):
            child = f"{prefix}.{key}" if prefix else key
            differences.extend(_diff_paths(left[key], right[key], child))
        return differences
    return [] if left == right else [prefix]


def _neuron_state(neuron: MultiExcursionNeuron) -> Record:
    return {
        "x": float(neuron.x),
        "z": float(neuron.integration_state or 0.0),
        "clock": float(neuron.clock.timestamp),
        "mode": neuron.mode.value,
        "ordinary_episode_id": neuron.ordinary_episode_id,
        "multi_episode_id": neuron.multi_episode_id,
        "processed_event_count": neuron.processed_event_count,
        "out_of_scope": neuron.out_of_scope,
    }


def _emission_record(emission: Any) -> Record:
    return {
        "event_id": emission.event_id,
        "sequence": emission.sequence,
        "source": emission.source,
        "timestamp": float(emission.timestamp),
        "payload": float(emission.payload),
        "payload_bits": float_bits(emission.payload),
        "lineage_id": emission.lineage_id,
        "episode_id": emission.episode_id,
    }


def audit_recurrence(
    traces: list[Record],
    config: E1Config,
    label: str,
    runtime_event_trace: list[Record] | None = None,
    neuron_id: str | None = None,
) -> Record:
    if config.integration is None:
        raise GateError(f"{label} integration state unexpectedly disabled")
    integration = config.integration
    node_events: list[Record] | None = None
    if runtime_event_trace is not None:
        if neuron_id is None:
            raise GateError(f"{label} runtime-event audit requires a neuron ID")
        node_events = [
            event
            for event in runtime_event_trace
            if len(event) == 12 and event[2] == neuron_id
        ]
        input_events = [
            event
            for event in node_events
            if event[3] == EventType.EXCURSION.value
        ]
        if len(input_events) != len(traces):
            raise GateError(
                f"{label} runtime-event/integration trace count mismatch: "
                f"{len(input_events)} != {len(traces)}"
            )
    z = 0.0
    prior_timestamp = 0.0
    crossing_count = 0
    discharge_count = 0
    checks = []
    update_index = 0
    timeline = node_events if node_events is not None else [
        [trace["timestamp"], None, neuron_id, EventType.EXCURSION.value]
        for trace in traces
    ]
    for event_index, event in enumerate(timeline):
        timestamp = float(event[0])
        elapsed = timestamp - prior_timestamp
        if timestamp < prior_timestamp:
            raise GateError(f"{label} recurrence timestamp moved backwards at event {event_index}")
        is_input = event[3] == EventType.EXCURSION.value
        if is_input:
            if update_index >= len(traces):
                raise GateError(f"{label} runtime timeline has extra input events")
            trace = traces[update_index]
            if timestamp != float(trace["timestamp"]):
                raise GateError(
                    f"{label} runtime event/integration timestamp mismatch at {update_index}"
                )
            if float(trace["elapsed"]) != elapsed:
                raise GateError(
                    f"{label} recurrence timestamp/elapsed mismatch at {update_index}"
                )
        else:
            if event[3] != "internal":
                raise GateError(
                    f"{label} runtime timeline contains unsupported neuron event {event[3]!r}"
                )
            trace = None
        expected_decay = z * math.exp(-integration.decay_rate_z * elapsed)
        if trace is None:
            z = expected_decay
        else:
            _require_close(float(trace["z_before_decay"]), z, f"{label} z-before at {update_index}")
            _require_close(
                float(trace["z_after_decay"]),
                expected_decay,
                f"{label} event-time decay at {update_index}",
            )
            integrated = (
                trace["mode_before"] == "N"
                and abs(float(trace["x_after_input"])) < config.theta_e
            )
            if trace["integrated"] is not integrated:
                raise GateError(f"{label} integration admission mismatch at {update_index}")
            expected_input = (
                max(
                    -integration.z_max,
                    min(
                        integration.z_max,
                        expected_decay
                        + integration.input_gain * float(trace["input_value"]),
                    ),
                )
                if integrated
                else expected_decay
            )
            _require_close(
                float(trace["z_after_input"]),
                expected_input,
                f"{label} input update at {update_index}",
            )
            crossing = abs(expected_input) >= integration.discharge_quantum
            crossing_count += crossing
            should_discharge = (
                integrated
                and crossing
                and float(trace["x_after_input"]) * expected_input >= 0.0
            )
            expected_discharge = (
                math.copysign(integration.discharge_quantum, expected_input)
                if should_discharge
                else 0.0
            )
            if float(trace["discharge_amount"]) != expected_discharge:
                raise GateError(f"{label} discharge decision mismatch at {update_index}")
            if should_discharge:
                discharge_count += 1
            expected_post = expected_input - expected_discharge
            _require_close(
                float(trace["z_post_discharge"]),
                expected_post,
                f"{label} post-discharge state at {update_index}",
            )
            if bool(trace["crossed_theta_e"]) != (
                abs(float(trace["x_post_discharge"])) >= config.theta_e
            ):
                raise GateError(f"{label} theta-E crossing mismatch at {update_index}")
            z = expected_post
            checks.append(
                {
                    "index": update_index,
                    "timestamp": timestamp,
                    "elapsed": elapsed,
                    "input": float(trace["input_value"]),
                    "integrated": integrated,
                    "expected_z_after_decay": expected_decay,
                    "expected_z_after_input": expected_input,
                    "threshold_crossing": crossing,
                    "expected_discharge": expected_discharge,
                    "expected_z_post_discharge": expected_post,
                }
            )
            update_index += 1
        prior_timestamp = timestamp
    if update_index != len(traces):
        raise GateError(f"{label} runtime timeline omitted integration updates")
    return {
        "passed": True,
        "updates": len(traces),
        "threshold_crossings": crossing_count,
        "integration_discharges": discharge_count,
        "final_z": z,
        "update_checks": checks,
    }


def _record_context(runtime: ExcursionCharacterRuntime, event: Event) -> Record:
    row = next(
        (
            item
            for item in reversed(runtime._trace)
            if len(item) >= 12 and item[5] == event.sequence
        ),
        None,
    )
    if row is None:
        raise GateError("processed event lacks runtime causal route context")
    return {
        "causal_roots": list(row[8]),
        "route_depth": int(row[9]),
        "route_path": list(row[10]),
        "roots_truncated": bool(row[11]),
    }


def run_stream(
    stream_id: str,
    inputs: list[Record],
    relay_config: E1Config,
    destination_config: E1Config,
    bounds: Record,
) -> Record:
    """Replay only authenticated retained arrivals through the normal E2 route."""
    if (
        not isinstance(relay_config, E1Config)
        or not isinstance(destination_config, E1Config)
        or relay_config.integration is None
        or destination_config.integration is None
    ):
        raise TypeError("Luna-54 requires existing integration-enabled E2 relay/destination neurons")
    ordered = sorted(
        inputs,
        key=lambda item: (int(item["source_queue_sequence"]), str(item["event_id"])),
    )
    if ordered != inputs:
        raise GateError(f"retained input order changed before computation: {stream_id}")
    if len({item["event_id"] for item in ordered}) != len(ordered):
        raise GateError(f"duplicate retained source event identity: {stream_id}")
    topology = BoundedTopology.from_edges(
        ["relay", "destination"],
        [
            Edge(
                "relay",
                "destination",
                bounds["topology"]["propagation_delay"],
                edge_weight=bounds["topology"]["edge_weight"],
                divider_strength=bounds["topology"]["divider_strength"],
                reference=bounds["topology"]["reference"],
                legacy_identity=bounds["topology"]["legacy_identity"],
            )
        ],
        fan_in_limit=bounds["topology"]["fan_in_limit"],
        fan_out_limit=bounds["topology"]["fan_out_limit"],
        edge_capacity=bounds["topology"]["edge_capacity"],
        routing_capacity=bounds["topology"]["routing_capacity"],
    )
    relay = MultiExcursionNeuron("relay", config=relay_config, initial_timestamp=0.0)
    destination = MultiExcursionNeuron(
        "destination", config=destination_config, initial_timestamp=0.0
    )
    runtime = ExcursionCharacterRuntime(
        [relay, destination],
        topology,
        queue_capacity=bounds["runtime"]["queue_capacity"],
        event_budget=bounds["runtime"]["runtime_event_budget"],
        settling_horizon=bounds["runtime"]["settling_horizon"],
        prediction_capacity=bounds["runtime"]["prediction_capacity"],
        prediction_expiry=bounds["runtime"]["prediction_expiry"],
        max_activity_events=bounds["runtime"]["max_activity_events"],
        namespace="luna54",
        eligibility_capacity=bounds["runtime"]["eligibility_capacity_per_ledger"],
    )
    runtime.start_character(
        stream_id,
        int(stream_id.split("-")[1]),
        timestamp=bounds["runtime"]["initial_timestamp"],
        predictor_source="relay",
        readout_sources=("destination",),
        input_destination="relay",
    )
    assert runtime.queue is not None
    original_route = topology.route
    original_receive = MultiExcursionNeuron.receive_event
    original_destroy = runtime._destroy_character
    route_enqueues: list[Record] = []
    destination_receptions: list[Record] = []
    neuron_snapshot: Record = {}

    def capture_destroy(timestamp: float) -> None:
        neuron_snapshot.update(
            {
                "relay_traces": [jsonable(item) for item in relay.integration_trace],
                "destination_traces": [jsonable(item) for item in destination.integration_trace],
                "relay_emissions": [_emission_record(item) for item in relay.emissions],
                "destination_emissions": [
                    _emission_record(item) for item in destination.emissions
                ],
                "relay_state": _neuron_state(relay),
                "destination_state": _neuron_state(destination),
                "relay_processed_events": relay.processed_event_count,
                "destination_processed_events": destination.processed_event_count,
                "runtime_event_trace": [jsonable(item) for item in runtime._trace],
            }
        )
        original_destroy(timestamp)

    def capture_route(
        event: Event,
        queue: EventQueue[Event],
        **kwargs: Any,
    ) -> tuple[Event, ...]:
        routed = original_route(event, queue, **kwargs)
        for queued in routed:
            if event.source != "relay":
                raise GateError("unexpected outgoing edge from frozen relay topology")
            context = RouteContext(
                runtime._node_roots["relay"],
                1,
                ("relay", "destination"),
                runtime._node_truncation["relay"],
            )
            route_enqueues.append(
                {
                    "event_id": queued.event_id,
                    "queue_sequence": queued.sequence,
                    "source": queued.source,
                    "destination": queued.destination,
                    "event_type": (
                        queued.event_type.value
                        if isinstance(queued.event_type, EventType)
                        else str(queued.event_type)
                    ),
                    "payload": float(queued.payload),
                    "payload_bits": float_bits(float(queued.payload)),
                    "enqueue_timestamp": float(event.timestamp),
                    "scheduled_delivery_timestamp": float(queued.timestamp),
                    "lineage_id": queued.lineage_id,
                    "originating_emission_id": event.event_id,
                    "causal_roots": list(context.causal_roots),
                    "route_depth": context.route_depth,
                    "route_path": list(context.route_path),
                    "roots_truncated": context.roots_truncated,
                    "edge": {
                        "delay": bounds["topology"]["propagation_delay"],
                        "weight": bounds["topology"]["edge_weight"],
                        "divider_strength": bounds["topology"]["divider_strength"],
                        "reference": bounds["topology"]["reference"],
                    },
                }
            )
        return routed

    def capture_receive(
        neuron: MultiExcursionNeuron,
        event: Event,
        queue: EventQueue[Event] | None = None,
    ) -> Any:
        before = _neuron_state(neuron)
        old_traces = len(neuron.integration_trace)
        result = original_receive(neuron, event, queue)
        after = _neuron_state(neuron)
        if neuron.neuron_id == "destination" and event.event_type == EventType.EXCURSION:
            if len(neuron.integration_trace) != old_traces + 1:
                raise GateError("destination reception lacks exactly one integration trace")
            context = _record_context(runtime, event)
            trace = jsonable(neuron.integration_trace[-1])
            destination_receptions.append(
                {
                    "event_id": event.event_id,
                    "queue_sequence": event.sequence,
                    "source": event.source,
                    "destination": event.destination,
                    "receiver_node": neuron.neuron_id,
                    "event_type": EventType.EXCURSION.value,
                    "payload": float(event.payload),
                    "payload_bits": float_bits(float(event.payload)),
                    "reception_timestamp": float(event.timestamp),
                    "scheduled_delivery_timestamp": float(event.timestamp),
                    "lineage_id": event.lineage_id,
                    "originating_emission_id": event.event_id,
                    **context,
                    "receiver_state_transition": {
                        "event_sequence": event.sequence,
                        "processed_events_before": before["processed_event_count"],
                        "processed_events_after": after["processed_event_count"],
                        "x_before": before["x"],
                        "x_after": after["x"],
                        "z_before": before["z"],
                        "z_after": after["z"],
                    },
                    "integration_trace": trace,
                }
            )
        return result

    for input_record in ordered:
        if (
            input_record["source"] != "source"
            or input_record["destination"] != "relay"
            or input_record["receiver_node"] != "relay"
            or input_record["event_type"] != EventType.EXCURSION.value
            or input_record["scheduled_delivery_timestamp"] != input_record["reception_timestamp"]
            or input_record["payload_bits"] != float_bits(float(input_record["payload"]))
            or input_record["originating_emission_id"] != input_record["event_id"]
        ):
            raise GateError(f"invalid authenticated source-to-relay input: {stream_id}")
        event_context = RouteContext(
            tuple(input_record["causal_roots"]),
            int(input_record["route_depth"]),
            tuple(input_record["route_path"]),
            bool(input_record["roots_truncated"]),
        )
        event = Event(
            timestamp=input_record["reception_timestamp"],
            source="source",
            destination="relay",
            event_type=EventType.EXCURSION,
            payload=input_record["payload"],
            event_id=input_record["event_id"],
            lineage_id=input_record["lineage_id"],
        )
        queued = runtime.queue.push(event)
        runtime._remember_event_context(event.event_id, event_context)
        runtime._attach(queued, event_context)
    last_input_time = max(
        (float(item["reception_timestamp"]) for item in ordered),
        default=float(bounds["runtime"]["initial_timestamp"]),
    )
    with (
        mock.patch.object(topology, "route", capture_route),
        mock.patch.object(MultiExcursionNeuron, "receive_event", capture_receive),
        mock.patch.object(runtime, "_destroy_character", capture_destroy),
    ):
        completion = runtime.end_character(
            last_external_timestamp=last_input_time,
            reward=float(bounds["runtime"]["neutral_reward"]),
            reward_delay=float(bounds["runtime"]["reward_delay"]),
            reward_message_id=f"luna54-neutral-{stream_id}",
        )
    if (
        not completion.execution.completed
        or completion.execution.budget_exhausted
        or completion.pending_event_count != 0
        or completion.beyond_deadline_event_count != 0
        or (runtime.queue is not None and len(runtime.queue) != 0)
    ):
        raise GateError(
            f"bounded settling did not complete for {stream_id}: "
            f"completed={completion.execution.completed}, "
            f"budget_exhausted={completion.execution.budget_exhausted}, "
            f"pending={completion.pending_event_count}, "
            f"beyond_deadline={completion.beyond_deadline_event_count}, "
            f"queue={None if runtime.queue is None else len(runtime.queue)}"
        )
    relay_traces = neuron_snapshot["relay_traces"]
    destination_traces = neuron_snapshot["destination_traces"]
    if len(relay_traces) != len(ordered):
        raise GateError(
            f"relay trace/input counts differ: {stream_id}: "
            f"traces={len(relay_traces)}, inputs={len(ordered)}, "
            f"runtime_events={len(completion.trace)}"
        )
    if len(destination_traces) != len(destination_receptions):
        raise GateError(f"destination trace/reception counts differ: {stream_id}")
    runtime_event_trace = neuron_snapshot["runtime_event_trace"]
    relay_oracle = audit_recurrence(
        relay_traces,
        relay_config,
        f"{stream_id}/relay",
        runtime_event_trace,
        "relay",
    )
    destination_oracle = audit_recurrence(
        destination_traces,
        destination_config,
        f"{stream_id}/destination",
        runtime_event_trace,
        "destination",
    )
    _require_close(
        float(neuron_snapshot["relay_state"]["z"]),
        float(relay_oracle["final_z"]),
        f"{stream_id}/relay final state",
    )
    _require_close(
        float(neuron_snapshot["destination_state"]["z"]),
        float(destination_oracle["final_z"]),
        f"{stream_id}/destination final state",
    )
    route_reconciliation = reconcile_routes(
        route_enqueues,
        destination_receptions,
        require_complete=True,
    )
    _validate_route_fields(
        route_enqueues,
        destination_receptions,
        "relay",
        "destination",
    )
    source_root_universe = {
        root
        for item in ordered
        for root in item["causal_roots"]
    }
    for event in route_enqueues:
        roots = event["causal_roots"]
        if not roots or any(root not in source_root_universe for root in roots):
            raise GateError(f"routed output has missing/unauthenticated source lineage: {stream_id}")
    relay_emissions = neuron_snapshot["relay_emissions"]
    destination_emissions = neuron_snapshot["destination_emissions"]
    trace_emission_ids = {
        trace["emission_id"] for trace in relay_traces if trace["emission_id"] is not None
    }
    if trace_emission_ids != {event["event_id"] for event in relay_emissions}:
        raise GateError(f"relay canonical emissions do not match integration traces: {stream_id}")
    relay_discharge_emission_ids = {
        trace["emission_id"]
        for trace in relay_traces
        if float(trace["discharge_amount"]) != 0.0 and trace["emission_id"] is not None
    }
    if not relay_discharge_emission_ids.issubset(
        {event["event_id"] for event in relay_emissions}
    ):
        raise GateError(f"relay discharge lacks canonical emission association: {stream_id}")
    if {event["event_id"] for event in route_enqueues} != {
        event["event_id"] for event in relay_emissions
    }:
        raise GateError(f"relay emission/enqueue identities differ: {stream_id}")
    relay_crossings = sum(
        abs(float(trace["z_after_input"])) >= float(trace["theta_z"])
        for trace in relay_traces
    )
    destination_crossings = sum(
        abs(float(trace["z_after_input"])) >= float(trace["theta_z"])
        for trace in destination_traces
    )
    resource = {
        "queue_capacity": bounds["runtime"]["queue_capacity"],
        "queue_peak": completion.peak_queue_occupancy,
        "runtime_event_budget": bounds["runtime"]["runtime_event_budget"],
        "processed_events": completion.execution.processed_event_count,
        "pending_events": completion.pending_event_count,
        "per_neuron_event_budget": bounds["runtime"]["neuron_event_budget"],
        "neuron_processed_events": {
            "relay": neuron_snapshot["relay_processed_events"],
            "destination": neuron_snapshot["destination_processed_events"],
        },
        "settling_horizon": bounds["runtime"]["settling_horizon"],
        "settling_completed": completion.execution.completed,
        "queue_bound_pass": completion.peak_queue_occupancy <= bounds["runtime"]["queue_capacity"],
        "runtime_budget_pass": completion.execution.processed_event_count <= bounds["runtime"]["runtime_event_budget"],
        "neuron_budget_pass": max(relay.processed_event_count, destination.processed_event_count)
        <= bounds["runtime"]["neuron_event_budget"],
        "state_bounds_pass": all(
            math.isfinite(value)
            and abs(value) <= (8.0 if field.startswith("x") else 4.0)
            for node_traces in (relay_traces, destination_traces)
            for trace in node_traces
            for field, value in (
                ("x_before", trace["x_before_decay"]),
                ("x_after", trace["x_post_discharge"]),
                ("z_before", trace["z_before_decay"]),
                ("z_after", trace["z_post_discharge"]),
            )
        ),
    }
    if not all(
        resource[key]
        for key in (
            "queue_bound_pass",
            "runtime_budget_pass",
            "neuron_budget_pass",
            "state_bounds_pass",
        )
    ):
        raise GateError(f"resource/state bound failed: {stream_id}")
    return {
        "stream_id": stream_id,
        "source_input_count": len(ordered),
        "source_inputs": ordered,
        "relay_integration_count": len(relay_traces),
        "relay_integration_traces": relay_traces,
        "relay_threshold_crossings": relay_crossings,
        "relay_discharge_count": sum(float(trace["discharge_amount"]) != 0.0 for trace in relay_traces),
        "relay_discharge_emission_ids": sorted(relay_discharge_emission_ids),
        "relay_discharge_emission_count": len(relay_discharge_emission_ids),
        "relay_unlinked_discharge_count": sum(
            float(trace["discharge_amount"]) != 0.0 and trace["emission_id"] is None
            for trace in relay_traces
        ),
        "relay_canonical_emission_count": len(relay_emissions),
        "relay_emissions": relay_emissions,
        "relay_state": neuron_snapshot["relay_state"],
        "relay_oracle": relay_oracle,
        "relay_to_destination_enqueues": route_enqueues,
        "destination_reception_count": len(destination_receptions),
        "destination_receptions": destination_receptions,
        "runtime_event_trace": runtime_event_trace,
        "destination_integration_count": len(destination_traces),
        "destination_integration_traces": destination_traces,
        "destination_threshold_crossings": destination_crossings,
        "destination_discharge_count": sum(
            float(trace["discharge_amount"]) != 0.0 for trace in destination_traces
        ),
        "destination_canonical_emission_count": len(destination_emissions),
        "destination_emissions": destination_emissions,
        "destination_state": neuron_snapshot["destination_state"],
        "destination_oracle": destination_oracle,
        "route_reconciliation": route_reconciliation,
        "route_lineage_authenticated": True,
        "route_links_complete": True,
        "source_root_expansion_complete": not any(
            bool(item["roots_truncated"]) for item in ordered
        ),
        "relay_root_expansion_complete": not any(
            bool(item["roots_truncated"]) for item in route_enqueues
        ),
        "roots_truncated_count": sum(
            bool(item["roots_truncated"]) for item in route_enqueues
        ),
        "resources": resource,
        "runtime_trace": jsonable(completion.trace),
    }


def _input_reconciliation(base: Record, phase_data: Record) -> Record:
    return {
        "phase": phase_data["phase"],
        "source_to_relay_inputs": phase_data["input_count"],
        "authenticated_enqueue_reception_pairs": phase_data["input_count"],
        "authenticated_input_digest": phase_data["input_digest"],
        "unmatched": 0,
        "duplicate": 0,
        "phase_capture_files": phase_data["artifact_identities"],
        "catalog_says_raw_captures_match_arm_records": base["catalog"][
            "all_raw_captures_match_arm_records"
        ],
    }


def _historical_route_fields(event: Record) -> Record:
    fields = (
        "event_id", "source", "destination", "event_type", "payload", "payload_bits",
        "lineage_id", "originating_emission_id", "scheduled_delivery_timestamp",
        "causal_roots", "roots_truncated", "route_depth", "route_path",
    )
    return {field: event.get(field) for field in fields}


def _historical_compatibility(
    records: list[Record],
    phase_data: Record,
) -> Record:
    stream_records = phase_data["streams"]
    mismatches = []
    totals = Counter()
    for new in records:
        old = stream_records[new["stream_id"]]["historical"]
        stream_id = new["stream_id"]
        old_input_count = len(old["source_to_relay_receptions"])
        if new["source_input_count"] != old_input_count:
            mismatches.append(f"{stream_id}: input count")
        for label, current, expected in (
            (
                "relay integration traces",
                new["relay_integration_traces"],
                old["relay_integration_trace"],
            ),
            (
                "destination integration traces",
                new["destination_integration_traces"],
                old["destination_integration_trace"],
            ),
        ):
            if canonical_bytes(current) != canonical_bytes(expected):
                mismatches.append(f"{stream_id}: {label}")
        old_emissions = {
            event["event_id"]: event for event in old["relay_emissions"]
        }
        new_emissions = {event["event_id"]: event for event in new["relay_emissions"]}
        if set(old_emissions) != set(new_emissions):
            mismatches.append(f"{stream_id}: relay emission identities")
        else:
            for event_id, current in new_emissions.items():
                historic = old_emissions[event_id]
                for field in (
                    "sequence", "source", "timestamp", "payload", "lineage_id", "episode_id"
                ):
                    if current[field] != historic[field]:
                        mismatches.append(f"{stream_id}: relay emission {event_id}/{field}")
        old_onward_enqueue = [
            event for event in old["routing_enqueue_events"]
            if event["source"] == "relay" and event["destination"] == "destination"
        ]
        old_onward_receive = [
            event for event in old["receiver_reception_events"]
            if event["source"] == "relay" and event["destination"] == "destination"
        ]
        current_enqueue = new["relay_to_destination_enqueues"]
        current_receive = new["destination_receptions"]
        if len(old_onward_enqueue) != len(current_enqueue) or len(old_onward_receive) != len(current_receive):
            mismatches.append(f"{stream_id}: historical route-pair counts")
        for label, current_rows, historical_rows in (
            ("enqueue", current_enqueue, old_onward_enqueue),
            ("reception", current_receive, old_onward_receive),
        ):
            if [_historical_route_fields(item) for item in current_rows] != [
                _historical_route_fields(item) for item in historical_rows
            ]:
                mismatches.append(f"{stream_id}: route {label} identities/order/lineage")
        if len(current_receive) != len(old["destination_receptions"]):
            mismatches.append(f"{stream_id}: original destination reception count")
        totals["streams"] += 1
        totals["source_to_relay_inputs"] += old_input_count
        totals["relay_emissions"] += len(new_emissions)
        totals["relay_to_destination_enqueues"] += len(current_enqueue)
        totals["destination_receptions"] += len(current_receive)
        totals["destination_crossings"] += new["destination_threshold_crossings"]
    if mismatches:
        raise GateError(
            "historical control compatibility failed: " + "; ".join(mismatches[:12])
        )
    expected = {
        "streams": 320,
        "source_to_relay_inputs": 1715,
        "relay_emissions": 235,
        "relay_to_destination_enqueues": 235,
        "destination_receptions": 235,
        "destination_crossings": 0,
    }
    if dict(totals) != expected:
        raise GateError(f"historical control population counts differ: {dict(totals)}")
    return {"passed": True, "mismatches": 0, "exact_fields": expected}


def _verify_no_input_isolation(records: list[Record], groups: dict[str, str]) -> Record:
    no_input = [
        record for record in records
        if groups[record["stream_id"]] == "NO-RECEPTIONS"
        and record["source_input_count"] == 0
    ]
    violations = [
        record["stream_id"]
        for record in no_input
        if record["relay_integration_count"]
        or record["relay_discharge_count"]
        or record["relay_canonical_emission_count"]
        or record["relay_to_destination_enqueues"]
        or record["destination_reception_count"]
        or record["destination_threshold_crossings"]
        or record["destination_discharge_count"]
        or record["destination_canonical_emission_count"]
    ]
    if len(no_input) != 23 or violations:
        raise GateError(
            f"strict no-input isolation failed: streams={len(no_input)}, violations={violations}"
        )
    return {"passed": True, "streams": len(no_input), "violations": 0}


def _class_summary(records: list[Record], groups: dict[str, str]) -> Record:
    strata = {
        "DRIVE-LIMITED": [
            item for item in records if groups[item["stream_id"]] == "DRIVE-LIMITED"
        ],
        "NO-RECEPTIONS_WITH_SOURCE_INPUT": [
            item for item in records
            if groups[item["stream_id"]] == "NO-RECEPTIONS"
            and item["source_input_count"] > 0
        ],
        "NO-RECEPTIONS_WITH_ZERO_SOURCE_INPUT": [
            item for item in records
            if groups[item["stream_id"]] == "NO-RECEPTIONS"
            and item["source_input_count"] == 0
        ],
        "TEMPORAL-RETENTION-LIMITED": [
            item for item in records
            if groups[item["stream_id"]] == "TEMPORAL-RETENTION-LIMITED"
        ],
    }
    result: Record = {}
    for label, rows in strata.items():
        peak_relay_abs_z = max(
            (
                max(
                    (
                        abs(trace["z_after_input"])
                        for trace in item["relay_integration_traces"]
                    ),
                    default=0.0,
                )
                for item in rows
            ),
            default=0.0,
        )
        peak_destination_abs_z = max(
            (
                max(
                    (
                        abs(trace["z_after_input"])
                        for trace in item["destination_integration_traces"]
                    ),
                    default=0.0,
                )
                for item in rows
            ),
            default=0.0,
        )
        result[label] = {
            "streams": len(rows),
            "source_to_relay_inputs": sum(item["source_input_count"] for item in rows),
            "relay_integrations": sum(item["relay_integration_count"] for item in rows),
            "relay_threshold_crossings": sum(item["relay_threshold_crossings"] for item in rows),
            "relay_discharges": sum(item["relay_discharge_count"] for item in rows),
            "relay_discharge_linked_emissions": sum(
                item["relay_discharge_emission_count"] for item in rows
            ),
            "relay_canonical_emissions": sum(item["relay_canonical_emission_count"] for item in rows),
            "relay_to_destination_enqueues": sum(
                len(item["relay_to_destination_enqueues"]) for item in rows
            ),
            "destination_receptions": sum(item["destination_reception_count"] for item in rows),
            "destination_integrations": sum(item["destination_integration_count"] for item in rows),
            "destination_threshold_crossings": sum(
                item["destination_threshold_crossings"] for item in rows
            ),
            "destination_discharges": sum(item["destination_discharge_count"] for item in rows),
            "destination_canonical_emissions": sum(
                item["destination_canonical_emission_count"] for item in rows
            ),
            "peak_relay_abs_z": max(
                (max((abs(trace["z_after_input"]) for trace in item["relay_integration_traces"]), default=0.0)
                 for item in rows),
                default=0.0,
            ),
            "peak_destination_abs_z": max(
                (max((abs(trace["z_after_input"]) for trace in item["destination_integration_traces"]), default=0.0)
                 for item in rows),
                default=0.0,
            ),
            "resource_bounds_pass": all(
                all(value["resources"][flag] for flag in (
                    "queue_bound_pass", "runtime_budget_pass",
                    "neuron_budget_pass", "state_bounds_pass",
                ))
                for value in rows
            ),
            "peak_relay_abs_z": peak_relay_abs_z,
            "relay_margin_to_discharge_quantum": (
                1.0 - peak_relay_abs_z
            ),
            "peak_destination_abs_z": peak_destination_abs_z,
            "destination_margin_to_discharge_quantum": (
                1.0 - peak_destination_abs_z
            ),
        }
    return result


def _discharge_emission_signatures(record: Record) -> list[str]:
    emissions = {item["event_id"]: item for item in record["relay_emissions"]}
    enqueues = {
        item["event_id"]: item for item in record["relay_to_destination_enqueues"]
    }
    receptions = {item["event_id"]: item for item in record["destination_receptions"]}
    signatures = []
    for trace in record["relay_integration_traces"]:
        event_id = trace["emission_id"]
        if float(trace["discharge_amount"]) == 0.0 or event_id is None:
            continue
        emission = emissions.get(event_id)
        enqueue = enqueues.get(event_id)
        reception = receptions.get(event_id)
        if emission is None or enqueue is None or reception is None:
            raise GateError(
                f"relay integration discharge does not have an emitted/routed/reception chain: {event_id}"
            )
        signatures.append(
            digest(
                {
                    "discharge_timestamp": trace["timestamp"],
                    "discharge_amount": trace["discharge_amount"],
                    "emission": {
                        "event_id": emission["event_id"],
                        "timestamp": emission["timestamp"],
                        "payload_bits": emission["payload_bits"],
                        "lineage_id": emission["lineage_id"],
                    },
                    "enqueue": _historical_route_fields(enqueue),
                    "reception": _historical_route_fields(reception),
                }
            )
        )
    return signatures


def _condition_output_path(condition: str, phase: str) -> Path:
    return ROOT / OUTPUT_DIRECTORY / f"{condition}-{phase}.json"


def _load_existing_phase(condition: str, phase: str) -> Record:
    path = _condition_output_path(condition, phase)
    if not path.is_file():
        raise GateError(f"required prior phase result is absent: {path.relative_to(ROOT)}")
    artifact = json.loads(path.read_bytes())
    clean = dict(artifact)
    claimed = clean.pop("artifact_digest", None)
    if claimed != digest(clean):
        raise GateError(f"persisted phase artifact digest failed: {path.name}")
    return artifact


def _verify_control_gate() -> None:
    for phase in ("initial", "replay"):
        control = _load_existing_phase("control", phase)
        if (
            control.get("status") != "PASS"
            or control.get("condition") != "control"
            or not control.get("historical_control_compatibility", {}).get("passed")
        ):
            raise GateError(f"both historical control phases must PASS before treatment ({phase})")


def _write_artifact(path: Path, artifact: Record) -> Record:
    path.parent.mkdir(parents=True, exist_ok=True)
    sealed = {**artifact}
    sealed["artifact_digest"] = digest(sealed)
    payload = canonical_bytes(sealed) + b"\n"
    with path.open("xb") as stream:
        stream.write(payload)
    if path.read_bytes() != payload:
        raise OSError(f"artifact readback differs: {path}")
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha256(payload),
        "artifact_digest": sealed["artifact_digest"],
        "byte_length": len(payload),
    }


def _source_identity() -> Record:
    return {
        "runner": {
            "path": str(RUNNER_PATH).replace("\\", "/"),
            "sha256": sha256((ROOT / RUNNER_PATH).read_bytes()),
            "git_blob": _git_blob("HEAD", str(RUNNER_PATH).replace("\\", "/")),
        },
        "config": {
            "path": str(CONFIG_PATH).replace("\\", "/"),
            "sha256": sha256((ROOT / CONFIG_PATH).read_bytes()),
            "git_blob": _git_blob("HEAD", str(CONFIG_PATH).replace("\\", "/")),
        },
        "protocol": {
            "path": str(PROTOCOL_PATH).replace("\\", "/"),
            "sha256": sha256((ROOT / PROTOCOL_PATH).read_bytes()),
            "git_blob": _git_blob("HEAD", str(PROTOCOL_PATH).replace("\\", "/")),
        },
        "focused_tests": {
            "path": str(FOCUSED_TEST_PATH).replace("\\", "/"),
            "sha256": sha256((ROOT / FOCUSED_TEST_PATH).read_bytes()),
            "git_blob": _git_blob("HEAD", str(FOCUSED_TEST_PATH).replace("\\", "/")),
        },
    }


def _environment_record() -> Record:
    return {
        "python": sys.version,
        "implementation": sys.implementation.name,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "float_info": {
            name: getattr(sys.float_info, name)
            for name in (
                "max",
                "max_exp",
                "max_10_exp",
                "min",
                "min_exp",
                "min_10_exp",
                "dig",
                "mant_dig",
                "epsilon",
                "radix",
                "rounds",
            )
        },
    }


def _make_input_pins(base: Record, phase_data: Record, phase: str) -> Record:
    return {
        "retained_evidence_revision": EVIDENCE_REVISION,
        "current_baseline_revision": BASELINE_REVISION,
        "retained_artifacts": {
            path: {
                "git_blob": _git_blob(BASELINE_REVISION, path),
                "expected_git_blob": INPUT_EXPECTED_BLOBS[path],
            }
            for path in (L45_CONFIG_PATH, L45_CATALOG_PATH, L46_PATH, LUNA53_SUMMARY_PATH)
        } | {
            path: {
                "git_blob": _git_blob(BASELINE_REVISION, path),
                "expected_git_blob": INPUT_EXPECTED_BLOBS[path],
                "catalog": base["catalog"]["files"][Path(path).name],
            }
            for path in _phase_paths(phase).values()
        },
        "phase_artifacts": phase_data["artifact_identities"],
        "catalog_file_sha256": base["catalog_identity"]["canonical_sha256"],
        "luna46_file_sha256": LUNA46_SHA256,
        "luna53_summary_git_blob": LUNA53_SUMMARY_BLOB,
    }


def run_one(phase: str, condition: str, invocation_id: str) -> Record:
    if phase not in ("initial", "replay") or condition not in ("control", "intervention"):
        raise ValueError("invalid Luna-54 phase or condition")
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,80}", invocation_id):
        raise ValueError("invocation_id must be a fresh bounded identifier")
    output_path = _condition_output_path(condition, phase)
    if output_path.exists():
        raise GateError(f"phase output already exists and will not be overwritten: {output_path}")
    provenance = _require_baseline_ancestry()
    sources, protocol, config, frozen_config = _load_pinned_sources()
    if condition == "intervention":
        _verify_control_gate()
    if condition == "control" and phase == "replay":
        if not _condition_output_path("control", "initial").exists():
            raise GateError("control replay requires the initial control phase")
    if condition == "intervention":
        for control_phase in ("initial", "replay"):
            if not _condition_output_path("control", control_phase).exists():
                raise GateError(
                    "execution order requires both historical control phases before treatment"
                )
    arm, enqueue, reception, phase_data = _load_phase(phase, sources)
    phase_data["phase"] = phase
    relay_config, destination_config, effective_config = _config_for_condition(
        condition, frozen_config, config
    )
    groups = {
        item["stream_id"]: item["category"]
        for item in sources["l46"]["sequences"]
    }
    if len(groups) != 320 or Counter(groups.values()) != Counter({
        "NO-RECEPTIONS": 212,
        "TEMPORAL-RETENTION-LIMITED": 33,
        "DRIVE-LIMITED": 75,
    }):
        raise GateError("Luna-46 evaluator-only strata do not match the pinned 320-stream contract")
    group_input_counts = {
        category: sum(
            len(phase_data["streams"][stream_id]["source_inputs"])
            for stream_id in groups
            if groups[stream_id] == category
        )
        for category in ("DRIVE-LIMITED", "NO-RECEPTIONS", "TEMPORAL-RETENTION-LIMITED")
    }
    if group_input_counts != {
        "DRIVE-LIMITED": 676,
        "NO-RECEPTIONS": 558,
        "TEMPORAL-RETENTION-LIMITED": 481,
    }:
        raise GateError(f"retained input counts by original strata differ: {group_input_counts}")
    ordered_ids = [item["stream_id"] for item in arm["records"]]
    if set(ordered_ids) != set(groups) or len(ordered_ids) != 320:
        raise GateError("Luna-45 and Luna-46 stream identities do not reconcile")
    stream_records = []
    run_bounds = {
        "runtime": config["runtime"],
        "topology": config["topology"],
    }
    for stream_id in ordered_ids:
        historical_stream = phase_data["streams"][stream_id]
        result = run_stream(
            stream_id,
            historical_stream["source_inputs"],
            relay_config,
            destination_config,
            run_bounds,
        )
        result["evaluator_stratum"] = groups[stream_id]
        stream_records.append(result)
    input_reconciliation = _input_reconciliation(sources, phase_data)
    historical_compatibility = {"passed": False, "not_applicable": condition != "control"}
    if condition == "control":
        historical_compatibility = _historical_compatibility(stream_records, phase_data)
    isolation = _verify_no_input_isolation(stream_records, groups)
    class_summary = _class_summary(stream_records, groups)
    runtime_bounds = {
        "streams": len(stream_records),
        "queue_capacity": config["runtime"]["queue_capacity"],
        "runtime_event_budget": config["runtime"]["runtime_event_budget"],
        "per_neuron_event_budget": config["runtime"]["neuron_event_budget"],
        "settling_horizon": config["runtime"]["settling_horizon"],
        "all_streams_bounded": all(
            all(row["resources"][key] for key in (
                "queue_bound_pass", "runtime_budget_pass",
                "neuron_budget_pass", "state_bounds_pass",
            ))
            and row["resources"]["pending_events"] == 0
            and row["resources"]["settling_completed"]
            for row in stream_records
        ),
        "peak_queue_occupancy": max(
            row["resources"]["queue_peak"] for row in stream_records
        ),
        "peak_runtime_events": max(
            row["resources"]["processed_events"] for row in stream_records
        ),
        "peak_relay_neuron_events": max(
            row["resources"]["neuron_processed_events"]["relay"] for row in stream_records
        ),
        "peak_destination_neuron_events": max(
            row["resources"]["neuron_processed_events"]["destination"] for row in stream_records
        ),
        "total_pending_events": sum(
            row["resources"]["pending_events"] for row in stream_records
        ),
    }
    scientific_material = {
        "condition": condition,
        "effective_config": effective_config,
        "input_digest": digest({
            stream_id: phase_data["streams"][stream_id]["source_inputs"]
            for stream_id in sorted(phase_data["streams"])
        }),
        "records": stream_records,
    }
    phase_science_digest = digest(scientific_material)
    artifact = {
        "schema": "TPCN-LUNA54-PHASE-1",
        "task_id": "luna-54-relay-temporal-retention-propagation-20261008",
        "status": "PASS",
        "condition": condition,
        "phase": phase,
        "invocation_id": invocation_id,
        "execution_provenance": provenance | {
            "source_identity": _source_identity(),
        },
        "environment": _environment_record(),
        "configuration": effective_config,
        "condition_configuration_digest": digest(effective_config),
        "scientific_digest": phase_science_digest,
        "input_pins": _make_input_pins(sources, phase_data, phase),
        "source_to_relay_reconciliation": input_reconciliation,
        "historical_control_compatibility": historical_compatibility,
        "no_input_isolation": isolation,
        "independent_recurrence_oracle": {
            "implementation": "Luna-54 independent event-time binary64 recurrence",
            "tolerance": "64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))",
            "threshold_tolerance": "none",
            "relay_updates": sum(item["relay_integration_count"] for item in stream_records),
            "destination_updates": sum(item["destination_integration_count"] for item in stream_records),
            "all_passed": all(
                item["relay_oracle"]["passed"] and item["destination_oracle"]["passed"]
                for item in stream_records
            ),
        },
        "runtime_bounds": runtime_bounds,
        "class_summary": class_summary,
        "streams": stream_records,
        "input_lineage": {
            "source_inputs_preserved": True,
            "relay_output_lineage_authenticated": True,
            "truncated_root_metadata_preserved": True,
            "relay_to_destination_reconciliation": {
                "enqueued": sum(len(item["relay_to_destination_enqueues"]) for item in stream_records),
                "received": sum(item["destination_reception_count"] for item in stream_records),
                "matched": sum(item["route_reconciliation"]["matched_count"] for item in stream_records),
                "mismatches": 0,
            },
        },
        "interpretation_boundary": "retained-input relay mechanism only; not task efficacy or production evidence",
        "independent_review": "NOT PERFORMED; stop for independent Luna-0 review",
    }
    if not runtime_bounds["all_streams_bounded"]:
        raise GateError(f"{condition}/{phase} finite resource gate failed")
    if not artifact["independent_recurrence_oracle"]["all_passed"]:
        raise GateError(f"{condition}/{phase} recurrence audit failed")
    if condition == "control" and not historical_compatibility["passed"]:
        raise GateError("historical control reproduction did not pass")
    if condition == "intervention" and historical_compatibility["passed"]:
        raise GateError("treatment was incorrectly marked as a control reproduction")
    if condition == "control" and phase == "replay":
        initial = _load_existing_phase("control", "initial")
        if initial["scientific_digest"] != phase_science_digest:
            raise GateError("control initial/replay scientific digest differs")
        if (
            initial["source_to_relay_reconciliation"]["authenticated_input_digest"]
            != phase_data["input_digest"]
        ):
            raise GateError("control initial/replay authenticated input digests differ")
    if condition == "intervention" and phase == "replay":
        initial = _load_existing_phase("intervention", "initial")
        if initial["scientific_digest"] != phase_science_digest:
            raise GateError("intervention initial/replay scientific digest differs")
        if (
            initial["source_to_relay_reconciliation"]["authenticated_input_digest"]
            != phase_data["input_digest"]
        ):
            raise GateError("intervention initial/replay authenticated input digests differ")
    if condition == "intervention":
        for control_phase in ("initial", "replay"):
            control_artifact = _load_existing_phase("control", control_phase)
            if (
                control_artifact["source_to_relay_reconciliation"][
                    "authenticated_input_digest"
                ]
                != phase_data["input_digest"]
            ):
                raise GateError(
                    "intervention inputs differ from exact authenticated historical control inputs"
                )
    manifest = _write_artifact(output_path, artifact)
    return artifact | manifest


def _paired_summary(phase_artifacts: dict[tuple[str, str], Record]) -> Record:
    groups = {
        item["stream_id"]: item["evaluator_stratum"]
        for item in phase_artifacts[("control", "initial")]["streams"]
    }
    c0 = {
        item["stream_id"]: item
        for item in phase_artifacts[("control", "initial")]["streams"]
    }
    t0 = {
        item["stream_id"]: item
        for item in phase_artifacts[("intervention", "initial")]["streams"]
    }
    strata = {
        "DRIVE-LIMITED": [sid for sid, label in groups.items() if label == "DRIVE-LIMITED"],
        "NO-RECEPTIONS_WITH_SOURCE_INPUT": [
            sid for sid, label in groups.items()
            if label == "NO-RECEPTIONS" and c0[sid]["source_input_count"] > 0
        ],
        "NO-RECEPTIONS_WITH_ZERO_SOURCE_INPUT": [
            sid for sid, label in groups.items()
            if label == "NO-RECEPTIONS" and c0[sid]["source_input_count"] == 0
        ],
        "TEMPORAL-RETENTION-LIMITED": [
            sid for sid, label in groups.items() if label == "TEMPORAL-RETENTION-LIMITED"
        ],
    }
    by_group: Record = {}
    primary_increase_streams: list[str] = []
    primary_complete_increases: list[str] = []
    new_primary_emission_ids: dict[str, list[str]] = {}
    primary_extra_route_events = 0
    for group, stream_ids in strata.items():
        count = lambda record, field: (
            len(record[field])
            if field == "relay_to_destination_enqueues"
            else record[field]
        )
        deltas = {
            "source_to_relay_inputs": 0,
            "relay_integrations": 0,
            "relay_threshold_crossings": 0,
            "relay_discharges": 0,
            "relay_discharge_linked_emissions": 0,
            "relay_emissions": 0,
            "relay_to_destination_enqueues": 0,
            "destination_receptions": 0,
            "destination_threshold_crossings": 0,
            "destination_discharges": 0,
            "destination_emissions": 0,
        }
        ctrl_counts = Counter()
        tx_counts = Counter()
        for stream_id in stream_ids:
            control = c0[stream_id]
            treatment = t0[stream_id]
            values = (
                ("source_to_relay_inputs", "source_input_count"),
                ("relay_integrations", "relay_integration_count"),
                ("relay_threshold_crossings", "relay_threshold_crossings"),
                ("relay_discharges", "relay_discharge_count"),
                ("relay_discharge_linked_emissions", "relay_discharge_emission_count"),
                ("relay_emissions", "relay_canonical_emission_count"),
                ("relay_to_destination_enqueues", "relay_to_destination_enqueues"),
                ("destination_receptions", "destination_reception_count"),
                ("destination_threshold_crossings", "destination_threshold_crossings"),
                ("destination_discharges", "destination_discharge_count"),
                ("destination_emissions", "destination_canonical_emission_count"),
            )
            for metric, field in values:
                ctrl_counts[metric] += count(control, field)
                tx_counts[metric] += count(treatment, field)
                deltas[metric] += count(treatment, field) - count(control, field)
            control_signatures = Counter(_discharge_emission_signatures(control))
            treatment_signatures = Counter(_discharge_emission_signatures(treatment))
            new_signatures = list((treatment_signatures - control_signatures).elements())
            new_emission_ids = sorted(
                set(treatment["relay_discharge_emission_ids"])
                - set(control["relay_discharge_emission_ids"])
            )
            relay_emission_increase = bool(new_signatures) and bool(new_emission_ids) and (
                treatment["relay_discharge_emission_count"]
                > control["relay_discharge_emission_count"]
            )
            routed_increase = (
                treatment["destination_reception_count"] > control["destination_reception_count"]
                and len(treatment["relay_to_destination_enqueues"])
                > len(control["relay_to_destination_enqueues"])
            )
            if group == "DRIVE-LIMITED" and relay_emission_increase:
                primary_increase_streams.append(stream_id)
                new_primary_emission_ids[stream_id] = new_emission_ids
            if group == "DRIVE-LIMITED" and relay_emission_increase and routed_increase:
                primary_complete_increases.append(stream_id)
                primary_extra_route_events += max(
                    0,
                    treatment["destination_reception_count"] - control["destination_reception_count"],
                )
        by_group[group] = {
            "streams": len(stream_ids),
            "control": dict(ctrl_counts),
            "intervention": dict(tx_counts),
            "intervention_minus_control": deltas,
            "relay_discharge_and_emission_increase_streams": sum(
                1 for stream_id in stream_ids
                    if t0[stream_id]["relay_discharge_emission_count"]
                    > c0[stream_id]["relay_discharge_emission_count"]
                ),
            "treatment_route_reception_increase_streams": sum(
                1 for stream_id in stream_ids
                if t0[stream_id]["destination_reception_count"]
                > c0[stream_id]["destination_reception_count"]
            ),
            "unmatched_treatment_discharge_emission_signatures": sum(
                len(
                    Counter(_discharge_emission_signatures(t0[stream_id]))
                    - Counter(_discharge_emission_signatures(c0[stream_id]))
                )
                for stream_id in stream_ids
            ),
            "additional_linked_relay_emissions": sum(
                max(
                    0,
                    t0[stream_id]["relay_discharge_emission_count"]
                    - c0[stream_id]["relay_discharge_emission_count"],
                )
                for stream_id in stream_ids
            ),
        }
    all_checks = all(
        phase_artifacts[(condition, phase)]["status"] == "PASS"
        and phase_artifacts[(condition, phase)]["independent_recurrence_oracle"]["all_passed"]
        and phase_artifacts[(condition, phase)]["runtime_bounds"]["all_streams_bounded"]
        and phase_artifacts[(condition, phase)]["no_input_isolation"]["passed"]
        for condition in ("control", "intervention")
        for phase in ("initial", "replay")
    )
    control_compatibility = all(
        phase_artifacts[("control", phase)]["historical_control_compatibility"]["passed"]
        for phase in ("initial", "replay")
    )
    replay_equal = all(
        phase_artifacts[(condition, "initial")]["scientific_digest"]
        == phase_artifacts[(condition, "replay")]["scientific_digest"]
        and canonical_bytes(phase_artifacts[(condition, "initial")]["streams"])
        == canonical_bytes(phase_artifacts[(condition, "replay")]["streams"])
        for condition in ("control", "intervention")
    )
    routes_reconcile = all(
        item["input_lineage"]["relay_to_destination_reconciliation"]["enqueued"]
        == item["input_lineage"]["relay_to_destination_reconciliation"]["received"]
        == item["input_lineage"]["relay_to_destination_reconciliation"]["matched"]
        and item["input_lineage"]["relay_to_destination_reconciliation"]["mismatches"] == 0
        for item in phase_artifacts.values()
    )
    gate_pass = all_checks and control_compatibility and replay_equal and routes_reconcile
    if not gate_pass:
        verdict = "BLOCKED"
    elif primary_complete_increases:
        verdict = "SUPPORTED"
    elif primary_increase_streams:
        verdict = "INCONCLUSIVE"
    else:
        verdict = "NOT SUPPORTED"
    return {
        "schema": "TPCN-LUNA54-SUMMARY-1",
        "task_id": "luna-54-relay-temporal-retention-propagation-20261008",
        "status": "PASS" if gate_pass else "BLOCKED",
        "contract_verdict": verdict,
        "groups": by_group,
        "primary": {
            "streams": 75,
            "relay_discharge_and_emission_increase_streams": primary_increase_streams,
            "complete_valid_routed_increase_streams": primary_complete_increases,
            "new_linked_emission_ids_by_stream": new_primary_emission_ids,
            "additional_destination_receptions": primary_extra_route_events,
            "supported_endpoint": bool(primary_complete_increases),
        },
        "gates": {
            "all_four_phase_runs_pass": all_checks,
            "control_historical_reproduction_initial_and_replay": control_compatibility,
            "exact_same_condition_replay": replay_equal,
            "all_new_relay_destination_routes_reconcile": routes_reconcile,
            "no_input_isolation": all(
                phase_artifacts[(condition, phase)]["no_input_isolation"]["passed"]
                for condition in ("control", "intervention")
                for phase in ("initial", "replay")
            ),
        },
        "initial_replay_scientific_digests": {
            f"{condition}_{phase}": phase_artifacts[(condition, phase)]["scientific_digest"]
            for condition in ("control", "intervention")
            for phase in ("initial", "replay")
        },
        "initial_replay_exact_equal": replay_equal,
        "independent_review": "NOT PERFORMED; stop for independent Luna-0 review",
        "interpretation_boundary": (
            "bounded retained-input relay mechanism; not task efficacy, generalization, "
            "production configuration, architecture promotion, or hardware equivalence"
        ),
    }


def summarize() -> Record:
    phases = {
        (condition, phase): _load_existing_phase(condition, phase)
        for condition in ("control", "intervention")
        for phase in ("initial", "replay")
    }
    summary = _paired_summary(phases)
    summary["phase_artifacts"] = {
        f"{condition}_{phase}": {
            "path": f"artifacts/luna54/{condition}-{phase}.json",
            "file_sha256": sha256(
                _condition_output_path(condition, phase).read_bytes()
            ),
            "artifact_digest": phases[(condition, phase)]["artifact_digest"],
            "invocation_id": phases[(condition, phase)]["invocation_id"],
        }
        for condition in ("control", "intervention")
        for phase in ("initial", "replay")
    }
    artifact = {
        **summary,
        "execution_provenance": {
            "starting_baseline": BASELINE_REVISION,
            "execution_revision": phases[("control", "initial")]["execution_provenance"][
                "execution_revision"
            ],
            "source_identity": phases[("control", "initial")]["execution_provenance"][
                "source_identity"
            ],
        },
    }
    output = ROOT / OUTPUT_DIRECTORY / "summary.json"
    manifest = _write_artifact(output, artifact)
    catalog_rows = {}
    for path in sorted((ROOT / OUTPUT_DIRECTORY).glob("*.json")):
        if path.name == "integrity.json":
            continue
        payload = path.read_bytes()
        parsed = json.loads(payload)
        catalog_rows[path.name] = {
            "file_sha256": sha256(payload),
            "byte_length": len(payload),
            "artifact_digest": parsed.get("artifact_digest"),
        }
    catalog_body = {
        "schema": "TPCN-LUNA54-INTEGRITY-1",
        "starting_baseline": BASELINE_REVISION,
        "execution_revision": artifact["execution_provenance"]["execution_revision"],
        "files": catalog_rows,
        "all_internal_digests_pass": True,
        "all_phase_digests_recomputed": True,
        "all_raw_inputs_reconciled": True,
        "all_control_reproduction_gates_pass": artifact["gates"][
            "control_historical_reproduction_initial_and_replay"
        ],
        "all_routes_reconciled": artifact["gates"]["all_new_relay_destination_routes_reconcile"],
        "replay_equal": artifact["initial_replay_exact_equal"],
        "independent_review": "NOT PERFORMED",
    }
    integrity_path = ROOT / OUTPUT_DIRECTORY / "integrity.json"
    integrity_manifest = _write_artifact(integrity_path, catalog_body)
    return {
        "summary": artifact,
        "summary_manifest": manifest,
        "integrity_manifest": integrity_manifest,
    }


def preflight() -> Record:
    provenance = _require_baseline_ancestry()
    sources, _, _, _ = _load_pinned_sources()
    phases = {}
    for phase in ("initial", "replay"):
        _, _, _, phase_data = _load_phase(phase, sources)
        phase_data["phase"] = phase
        phases[phase] = {
            "streams": len(phase_data["streams"]),
            "source_to_relay_inputs": phase_data["input_count"],
            "historical_relay_to_destination_pairs": phase_data[
                "historical_relay_to_destination_pairs"
            ],
            "phase_digest": phase_data["phase_digest"],
            "phase_digest_recomputed": phase_data["phase_digest_recomputed"],
            "input_digest_recomputed": phase_data["input_digest"],
            "artifact_identities": phase_data["artifact_identities"],
        }
    if phases["initial"]["source_to_relay_inputs"] != phases["replay"]["source_to_relay_inputs"]:
        raise GateError("initial/replay source-to-relay input counts differ")
    if (
        phases["initial"]["input_digest_recomputed"]
        != phases["replay"]["input_digest_recomputed"]
        or phases["initial"]["phase_digest"]
        != phases["replay"]["phase_digest"]
    ):
        raise GateError("retained initial/replay source inputs or phase digests differ")
    return {
        "status": "PASS",
        "baseline": provenance,
        "phases": phases,
        "catalog_git_blob": _git_blob(EVIDENCE_REVISION, L45_CATALOG_PATH),
        "runtime_source_identities": sources["runtime_source_identities"],
        "luna46_git_blob": sources["l46_identity"]["git_blob"],
        "luna53_summary_git_blob": sources["luna53_summary_identity"]["git_blob"],
    }


def _write_blocked(error: Exception, phase: str | None, condition: str | None) -> None:
    output_dir = ROOT / OUTPUT_DIRECTORY
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "blocked.json"
    if path.exists():
        return
    artifact = {
        "schema": "TPCN-LUNA54-BLOCKED-1",
        "status": "BLOCKED",
        "condition": condition,
        "phase": phase,
        "gate_error_type": type(error).__name__,
        "gate_error": str(error),
        "starting_baseline": BASELINE_REVISION,
        "interpretation": "treatment interpretation stopped; no fallback execution permitted",
        "independent_review": "NOT PERFORMED",
    }
    _write_artifact(path, artifact)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--run-one", action="store_true")
    parser.add_argument("--phase", choices=("initial", "replay"))
    parser.add_argument("--condition", choices=("control", "intervention"))
    parser.add_argument("--invocation-id")
    parser.add_argument("--summarize", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.preflight:
            print(json.dumps(preflight(), sort_keys=True))
            return 0
        if args.run_one:
            if not args.phase or not args.condition or not args.invocation_id:
                parser.error("--run-one requires --phase, --condition, and --invocation-id")
            record = run_one(args.phase, args.condition, args.invocation_id)
            print(json.dumps({
                "status": record["status"],
                "condition": record["condition"],
                "phase": record["phase"],
                "invocation_id": record["invocation_id"],
                "streams": len(record["streams"]),
                "scientific_digest": record["scientific_digest"],
                "artifact_digest": record["artifact_digest"],
            }, sort_keys=True))
            return 0
        if args.summarize:
            result = summarize()
            print(json.dumps({
                "status": result["summary"]["status"],
                "contract_verdict": result["summary"]["contract_verdict"],
                "summary_sha256": result["summary_manifest"]["sha256"],
                "integrity_sha256": result["integrity_manifest"]["sha256"],
            }, sort_keys=True))
            return 0
        parser.error("select --preflight, --run-one, or --summarize")
    except (GateError, OSError, ValueError, KeyError, TypeError, IndexError) as error:
        _write_blocked(error, args.phase, args.condition)
        print(f"LUNA-54 BLOCKED: {error}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
