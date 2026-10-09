"""Execute Luna-53 on authenticated retained destination arrivals only."""

from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from enum import Enum
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import sys
from typing import Any

from tpcn.event_runtime import Event, EventQueue, EventType, execute_bounded
from tpcn.excursion_neuron import E1Config, IntegrationConfig, MultiExcursionNeuron


ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION_REVISION = "04305a2917195888cbbcccf378eba7971551e9b5"
CONFIG_PATH = Path("experiments/luna53/config.json")
PROTOCOL_PATH = Path("experiments/luna53/protocol.json")
OUTPUT_DIRECTORY = Path("artifacts/luna53")
CONTROL_DECAY = 0.0125
INTERVENTION_DECAY = 0.00125
EVENT_BUDGET = 4096
QUEUE_CAPACITY = 128
RECURRENCE_EPSILON_FACTOR = 64.0
Record = dict[str, Any]

PINNED_FILES: dict[str, dict[str, str]] = {
    "artifacts/luna45-depth2-frozen-config-20261006-r2/config.json": {
        "sha256": "a19bf911ebe04c52aba7d83e376faac853519db3308419ca8bfcad35143858e1",
        "git_blob": "1fcf4e9865d1b6d1af9f39ab74d399eb6496b166",
    },
    "artifacts/luna45-acp0008-depth2-destination-integration-20261006/artifact-integrity.json": {
        "sha256": "a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e",
        "git_blob": "b1aaef4006422f321922bfb58425e4fb646d96b9",
    },
    "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json": {
        "sha256": "0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e",
        "git_blob": "9506369d97babf7bc0ef15ed52efb738dcdcd549",
    },
    "artifacts/luna47a/inputs.json": {
        "sha256": "03b5a27700723afa266e63b516c6b3dfbc9a7accc6983d21a4f7a12e4383b185",
        "git_blob": "24989419f87dcf49ff0a651e5909c995e0d25fc0",
    },
    "artifacts/luna47a/results.json": {
        "sha256": "d1cac5065410767a42a35f99b659b4a4377f1b84d300e5cfd3ed304600322cff",
        "git_blob": "1526d1d15cbb59b0ca3d0fa04ef04f1c2c803f8f",
    },
}
RUNTIME_SOURCE_BLOBS = {
    "tpcn/excursion_neuron.py": "c0bdece6b15009db4e2b7d69c3242be174b5de80",
    "tpcn/event_runtime.py": "f4aacb5d782f19e30fd9e562d56d62faefa9002f",
    "run_luna45_acp0008_depth2_destination_integration.py": (
        "957f0ed197c22099c17275bf1d083ba85a7c0346"
    ),
}
FIXTURE_PROVENANCE_SOURCES = (
    (
        "10994419cec3646d30d965372f88d10605d83d57",
        "scripts/build_luna44_canonical_fixture.py",
        "696051cc3690aafc9f342e569697469a111757c37c2666b0c026333e6b16efce",
    ),
    (
        "a79494cd66be28fd291ed11eddd62d342f457cfd",
        "run_luna34_excursion_v1_multi_emitter_bridge.py",
        "17e581cf702fae1f56889472a967d2e8e5fec37cc041edba8247da14a0a8b5db",
    ),
    (
        "a79494cd66be28fd291ed11eddd62d342f457cfd",
        "tpcn/spiral_benchmark.py",
        "2ffb1b5ebb23f016436043118bc675eddaa14bfd923129359fe61a12df94d9f0",
    ),
    (
        "a79494cd66be28fd291ed11eddd62d342f457cfd",
        "tpcn/stroke_dataset.py",
        "daca268597e2467bf984922ee77736b584bef9743b6f41ad729d7cb4d3c3ede7",
    ),
)
LUNA44_FIXTURE = {
    "revision": "6413cffe6982bccc6698af6bebfae51f04e71dd9",
    "path": "artifacts/luna44-canonical-fixture/fixture.json",
    "git_blob": "c1fa6ed863c91b5084e38920258483657e035c61",
    "sha256": "66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629",
}
LUNA44_MANIFEST = {
    "revision": "86e5a2f389af06b06bf04a614edaed88e0847902",
    "path": "artifacts/luna44-canonical-fixture/provenance.json",
    "git_blob": "eb9179abae7eed10891e6022832f16735111b220",
    "sha256": "6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22",
}


class GateError(RuntimeError):
    """A required Luna-53 execution or interpretation gate failed."""


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


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def float_bits(value: float) -> str:
    return struct.pack(">d", float(value)).hex()


def _run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout.strip()


def _blob_at(revision: str, path: str) -> str:
    return _run_git("rev-parse", f"{revision}:{path}")


def _verify_blob(revision: str, path: str, expected: str) -> str:
    actual = _blob_at(revision, path)
    if actual != expected:
        raise GateError(f"Git blob mismatch for {revision}:{path}: {actual}")
    return actual


def _historical_blob_bytes(revision: str, path: str, expected_blob: str) -> bytes:
    try:
        blob = _verify_blob(revision, path, expected_blob)
        return subprocess.check_output(
            ["git", "cat-file", "blob", blob],
            cwd=ROOT,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as error:
        raise GateError(f"missing pinned historical object for {revision}:{path}") from error


def _verify_checkout_materialization(working: bytes, pinned: bytes) -> str:
    if working == pinned:
        return "exact"
    if (
        b"\x00" not in pinned
        and b"\r\n" not in pinned
        and working == pinned.replace(b"\n", b"\r\n")
    ):
        return "exact-Git-LF-to-CRLF-checkout"
    raise GateError("file checkout differs beyond exact Git line-ending materialization")


def _verified_file(
    path: str,
    expected_sha256: str,
    *,
    expected_size: int | None = None,
    canonical_bytes: bytes | None = None,
) -> tuple[bytes, Record]:
    source = ROOT / path
    try:
        raw = source.read_bytes()
    except OSError as error:
        raise GateError(f"missing required pinned file {path}: {error}") from error

    if canonical_bytes is not None:
        materialization = _verify_checkout_materialization(raw, canonical_bytes)
        permitted = [(sha256(canonical_bytes), len(canonical_bytes))]
        if b"\x00" not in canonical_bytes and b"\r\n" not in canonical_bytes:
            crlf = canonical_bytes.replace(b"\n", b"\r\n")
            permitted.append((sha256(crlf), len(crlf)))
        recorded = next(
            (size for digest_value, size in permitted if digest_value == expected_sha256),
            None,
        )
        if recorded is None:
            raise GateError(f"historical SHA-256 does not identify Git object for {path}")
        if expected_size is not None and recorded != expected_size:
            raise GateError(f"canonical byte length mismatch for {path}")
        return raw, {
            "path": path,
            "checkout_bytes": len(raw),
            "canonical_bytes": len(canonical_bytes),
            "checkout_sha256": sha256(raw),
            "canonical_sha256": sha256(canonical_bytes),
            "checkout_materialization": materialization,
        }

    normalized = raw.replace(b"\r\n", b"\n")
    raw_hash = sha256(raw)
    normalized_hash = sha256(normalized)
    if expected_sha256 not in (raw_hash, normalized_hash):
        raise GateError(f"file SHA-256 mismatch for {path}")
    canonical_size = len(normalized) if normalized_hash == expected_sha256 else len(raw)
    if expected_size is not None and canonical_size != expected_size:
        raise GateError(f"canonical byte length mismatch for {path}")
    return raw, {
        "path": path,
        "checkout_bytes": len(raw),
        "canonical_bytes": canonical_size,
        "checkout_sha256": raw_hash,
        "canonical_sha256": normalized_hash,
    }


def _read_json(path: str, expected_sha256: str, *, expected_size: int | None = None) -> tuple[Record, Record]:
    raw, identity = _verified_file(path, expected_sha256, expected_size=expected_size)
    try:
        parsed = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GateError(f"invalid pinned JSON artifact {path}: {error}") from error
    if not isinstance(parsed, dict):
        raise GateError(f"pinned artifact is not a JSON object: {path}")
    return parsed, identity


def _verify_object_sha(revision: str, path: str, expected_sha256: str) -> Record:
    blob = _blob_at(revision, path)
    content = subprocess.run(
        ["git", "cat-file", "blob", blob],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    actual_sha = sha256(content)
    if actual_sha != expected_sha256:
        raise GateError(f"historical source SHA-256 mismatch for {revision}:{path}")
    return {
        "revision": revision,
        "path": path,
        "git_blob": blob,
        "sha256": actual_sha,
        "byte_length": len(content),
    }


def _same_float(observed: float, expected: float) -> bool:
    tolerance = RECURRENCE_EPSILON_FACTOR * sys.float_info.epsilon * max(
        1.0, abs(observed), abs(expected)
    )
    return abs(observed - expected) <= tolerance


def _require_same_float(observed: float, expected: float, detail: str) -> None:
    if not _same_float(float(observed), float(expected)):
        raise GateError(
            f"{detail}: observed {observed!r}, expected {expected!r} "
            f"(64-epsilon policy)"
        )


def _artifact_payload_digest(artifact: Record) -> bool:
    clean = dict(artifact)
    claimed = clean.pop("artifact_digest", None)
    return isinstance(claimed, str) and claimed == digest(clean)


def _check_runtime_sources(execution_revision: str) -> Record:
    identities: dict[str, Record] = {}
    for path, expected_blob in RUNTIME_SOURCE_BLOBS.items():
        authorization_blob = _verify_blob(AUTHORIZATION_REVISION, path, expected_blob)
        execution_blob = _blob_at(execution_revision, path)
        if execution_blob != authorization_blob:
            raise GateError(f"authorized runtime source changed: {path}")
        identities[path] = {
            "authorization_git_blob": authorization_blob,
            "execution_git_blob": execution_blob,
        }
    lane_sources = (
        "experiments/luna53/run.py",
        "experiments/luna53/config.json",
        "experiments/luna53/protocol.json",
    )
    if execution_revision == AUTHORIZATION_REVISION:
        identities["lane_publication"] = {
            "status": "pre-publication preflight only",
            "working_tree_sha256": {
                path: sha256((ROOT / path).read_bytes()) for path in lane_sources
            },
        }
    else:
        for path in lane_sources:
            if _blob_at(execution_revision, path) != _blob_at("HEAD", path):
                raise GateError(f"executed Luna-53 source is not the committed HEAD: {path}")
            identities[path] = {"execution_git_blob": _blob_at(execution_revision, path)}
    return identities


def _verify_canonical_config(config: Record) -> Record:
    published_path = "artifacts/luna45-depth2-frozen-config-20261006-r2/config.json"
    _verify_blob(AUTHORIZATION_REVISION, published_path, PINNED_FILES[published_path]["git_blob"])
    frozen, file_identity = _read_json(
        published_path,
        PINNED_FILES[published_path]["sha256"],
    )
    declared_config_digest = digest(frozen)
    if declared_config_digest != "cb6621ff403836e1b72b86a65375df11c2841df61030fbe5dd8a654a70394c1a":
        raise GateError("Luna-45 frozen configuration digest mismatch")
    actual_destination = frozen["neuron_configurations"]["DESTINATION_CALIBRATED"]["destination"]
    if actual_destination != config["historical_destination"]:
        raise GateError("Luna-53 destination configuration differs from pinned Luna-45")
    for condition, rate in (
        ("control", CONTROL_DECAY),
        ("intervention", INTERVENTION_DECAY),
    ):
        if config["conditions"][condition]["decay_rate_z"] != rate:
            raise GateError(f"unexpected {condition} decay value")
    if set(config["conditions"]) != {"control", "intervention"}:
        raise GateError("unexpected experimental conditions")
    baseline = deepcopy(config["historical_destination"])
    treatment = deepcopy(config["historical_destination"])
    baseline["integration"]["decay_rate_z"] = config["conditions"]["control"]["decay_rate_z"]
    treatment["integration"]["decay_rate_z"] = config["conditions"]["intervention"]["decay_rate_z"]
    differences = _diff_paths(baseline, treatment)
    if differences != ["integration.decay_rate_z"]:
        raise GateError(f"intervention has non-authorized config differences: {differences}")
    if config["runtime"] != {
        "initial_timestamp": 0.0,
        "queue_capacity": QUEUE_CAPACITY,
        "event_budget": EVENT_BUDGET,
        "neuron_event_budget": EVENT_BUDGET,
    }:
        raise GateError("runtime bounds differ from the predeclared configuration")
    return {
        "file": file_identity,
        "configuration_digest": declared_config_digest,
        "destination_configuration": actual_destination,
        "only_changed_path": differences[0],
    }


def _diff_paths(left: Any, right: Any, prefix: str = "") -> list[str]:
    if isinstance(left, dict) and isinstance(right, dict):
        paths: list[str] = []
        if left.keys() != right.keys():
            return [prefix or "<root>"]
        for key in sorted(left):
            child = f"{prefix}.{key}" if prefix else key
            paths.extend(_diff_paths(left[key], right[key], child))
        return paths
    if left != right:
        return [prefix]
    return []


def _verify_fixture_provenance() -> Record:
    fixture, fixture_identity = _read_json(
        LUNA44_FIXTURE["path"],
        LUNA44_FIXTURE["sha256"],
        expected_size=3_451_453,
    )
    fixture_blob = _verify_blob(
        LUNA44_FIXTURE["revision"],
        LUNA44_FIXTURE["path"],
        LUNA44_FIXTURE["git_blob"],
    )
    manifest, manifest_identity = _read_json(
        LUNA44_MANIFEST["path"],
        LUNA44_MANIFEST["sha256"],
        expected_size=36_113,
    )
    manifest_blob = _verify_blob(
        LUNA44_MANIFEST["revision"],
        LUNA44_MANIFEST["path"],
        LUNA44_MANIFEST["git_blob"],
    )
    if manifest.get("fixture_json_sha256") != LUNA44_FIXTURE["sha256"]:
        raise GateError("Luna-44 provenance manifest does not pin the frozen fixture")
    if manifest.get("semantic_fixture_digest") != (
        "6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305"
    ):
        raise GateError("Luna-44 semantic fixture identity mismatch")
    sources = [
        _verify_object_sha(revision, path, expected_sha)
        for revision, path, expected_sha in FIXTURE_PROVENANCE_SOURCES
    ]
    if fixture.get("sequences") is None:
        raise GateError("frozen Luna-44 fixture has no sequence records")
    return {
        "fixture": {**fixture_identity, "git_blob": fixture_blob},
        "manifest": {**manifest_identity, "git_blob": manifest_blob},
        "source_objects": sources,
        "semantic_sha256": manifest["semantic_fixture_digest"],
    }


def _verify_input_catalog() -> tuple[Record, Record]:
    catalog_path = "artifacts/luna45-acp0008-depth2-destination-integration-20261006/artifact-integrity.json"
    _verify_blob(
        AUTHORIZATION_REVISION,
        catalog_path,
        PINNED_FILES[catalog_path]["git_blob"],
    )
    catalog, catalog_identity = _read_json(
        catalog_path,
        PINNED_FILES[catalog_path]["sha256"],
        expected_size=7_121,
    )
    if not all(
        catalog.get(flag) is True
        for flag in (
            "all_internal_and_file_digests_pass",
            "all_phase_digests_recomputed",
            "all_raw_captures_match_arm_records",
        )
    ):
        raise GateError("pinned Luna-45 raw-route integrity catalog is not PASS")
    if catalog.get("execution_revision") != "97a93b394d071413075a1f102fdef695664722ff":
        raise GateError("unexpected Luna-45 raw-route execution revision")
    if catalog.get("fixture_file_sha256") != LUNA44_FIXTURE["sha256"]:
        raise GateError("raw-route catalog fixture identity differs")
    return catalog, catalog_identity


def _verify_catalog_artifact(
    relative_path: str,
    catalog: Record,
    *,
    parse: bool,
) -> tuple[Record | None, Record]:
    path = f"artifacts/luna45-acp0008-depth2-destination-integration-20261006/{relative_path}"
    expected = catalog["files"].get(relative_path)
    if not isinstance(expected, dict):
        raise GateError(f"raw-route catalog omits {relative_path}")
    _, identity = _verified_file(
        path,
        expected["file_sha256"],
        expected_size=expected["byte_length"],
    )
    blob = _blob_at(AUTHORIZATION_REVISION, path)
    identity["git_blob"] = blob
    if not parse:
        return None, identity
    value = json.loads((ROOT / path).read_bytes())
    if not isinstance(value, dict) or value.get("artifact_digest") != expected["artifact_digest"]:
        raise GateError(f"catalog artifact digest differs for {relative_path}")
    if not _artifact_payload_digest(value):
        raise GateError(f"internal artifact digest failure for {relative_path}")
    return value, identity


def _route_event_key(event: Record) -> tuple[str, int]:
    return str(event["event_id"]), int(event["queue_sequence"])


def _compare_route_event(observed: Record, expected: Record, stream_id: str, phase: str) -> None:
    fields = (
        "event_id",
        "queue_sequence",
        "source",
        "destination",
        "event_type",
        "payload",
        "payload_bits",
        "payload_encoding",
        "lineage_id",
        "originating_emission_id",
        "route_path",
        "route_depth",
        "causal_roots",
        "roots_truncated",
    )
    for field in fields:
        if observed.get(field) != expected.get(field):
            raise GateError(f"{phase}/{stream_id} raw route mismatch at {field}")
    observed_time = observed.get("reception_timestamp", observed.get("timestamp"))
    expected_time = expected.get("reception_timestamp", expected.get("timestamp"))
    if observed_time != expected_time:
        raise GateError(f"{phase}/{stream_id} raw route timestamp mismatch")


def _verify_phase_reconciliation(
    phase: str,
    inputs: Record,
    l46: Record,
    route_capture: Record,
) -> tuple[list[Record], Record]:
    streams = inputs["phases"][phase]["primary"]
    diagnostic_by_id = {row["stream_id"]: row for row in l46["sequences"]}
    if len(streams) != 320 or len({row["stream_id"] for row in streams}) != 320:
        raise GateError(f"{phase} does not contain exactly 320 unique streams")
    counts: defaultdict[str, int] = defaultdict(int)
    for row in streams:
        category = row["category"]
        if category not in ("TEMPORAL-RETENTION-LIMITED", "DRIVE-LIMITED", "NO-RECEPTIONS"):
            raise GateError(f"unexpected retained classification {category}")
        counts[category] += 1
        diagnostic = diagnostic_by_id.get(row["stream_id"])
        if diagnostic is None or diagnostic["category"] != category:
            raise GateError(f"{phase}/{row['stream_id']} classification differs from Luna-46")
        if row["raw_identity_sha256"] != row["fixture_sequence_sha256"]:
            raise GateError(f"{phase}/{row['stream_id']} fixture identity mismatch")
        if row["raw_arrivals"] != sorted(
            row["raw_arrivals"], key=lambda item: item["queue_sequence"]
        ):
            raise GateError(f"{phase}/{row['stream_id']} arrivals are not in retained order")
        if len({item["queue_sequence"] for item in row["raw_arrivals"]}) != len(row["raw_arrivals"]):
            raise GateError(f"{phase}/{row['stream_id']} has duplicate source queue sequences")
        recurrence = {item["event_id"]: item for item in diagnostic["recurrence_evidence"]}
        updates = {item["event_id"]: item for item in row["updates"]}
        if len(row["raw_arrivals"]) != len(recurrence) or set(recurrence) != set(updates):
            raise GateError(f"{phase}/{row['stream_id']} Luna-46 update inventory mismatch")
        for arrival in row["raw_arrivals"]:
            reception = arrival["raw_reception"]
            if (
                reception.get("source") != "relay"
                or reception.get("destination") != "destination"
                or reception.get("route_path") != ["relay", "destination"]
                or reception.get("route_depth") != 1
                or reception.get("event_type") != EventType.EXCURSION.value
            ):
                raise GateError(f"{phase}/{row['stream_id']} input is outside the declared route")
            recurrence_row = recurrence.get(arrival["event_id"])
            update = updates.get(arrival["event_id"])
            if recurrence_row is None or update is None:
                raise GateError(f"{phase}/{row['stream_id']} arrival is absent from Luna-46")
            for field in ("event_id", "queue_sequence", "timestamp", "payload"):
                if arrival[field] != recurrence_row[field] or arrival[field] != update[field]:
                    raise GateError(
                        f"{phase}/{row['stream_id']} Luna-46 arrival mismatch at {field}"
                    )

    expected_counts = {
        "TEMPORAL-RETENTION-LIMITED": 33,
        "DRIVE-LIMITED": 75,
        "NO-RECEPTIONS": 212,
    }
    if dict(counts) != expected_counts:
        raise GateError(f"{phase} class inventory mismatch: {dict(counts)}")
    captured_by_id = {
        row["stream_id"]: row["events"]
        for row in route_capture["per_sequence"]
    }
    if len(captured_by_id) != 320:
        raise GateError(f"{phase} Luna-45 route catalog is missing streams")
    actual_count = 0
    for row in streams:
        source_events = [
            event
            for event in captured_by_id[row["stream_id"]]
            if event.get("destination") == "destination"
        ]
        retained_events = [item["raw_reception"] for item in row["raw_arrivals"]]
        if len(source_events) != len(retained_events):
            raise GateError(f"{phase}/{row['stream_id']} destination reception count differs")
        source_by_key = {_route_event_key(event): event for event in source_events}
        retained_by_key = {_route_event_key(event): event for event in retained_events}
        if source_by_key.keys() != retained_by_key.keys():
            raise GateError(f"{phase}/{row['stream_id']} destination event identities differ")
        for key, event in retained_by_key.items():
            _compare_route_event(event, source_by_key[key], row["stream_id"], phase)
        actual_count += len(retained_events)
    if actual_count != 235:
        raise GateError(f"{phase} expected 235 destination arrivals; observed {actual_count}")
    return streams, {
        "phase": phase,
        "stream_count": len(streams),
        "category_counts": dict(counts),
        "destination_reception_count": actual_count,
        "route_event_reconciliation": "PASS",
    }


def verify_provenance(execution_revision: str | None = None) -> tuple[Record, Record]:
    """Verify the pinned evidence without invoking a neuron or route generator."""
    revision = execution_revision or _run_git("rev-parse", "HEAD")
    _run_git("merge-base", "--is-ancestor", AUTHORIZATION_REVISION, revision)
    runtime_sources = _check_runtime_sources(revision)
    config = json.loads((ROOT / CONFIG_PATH).read_bytes())
    protocol = json.loads((ROOT / PROTOCOL_PATH).read_bytes())
    config_identity = _verify_canonical_config(config)

    verified_files: dict[str, Record] = {}
    for path, pins in PINNED_FILES.items():
        canonical = _historical_blob_bytes(
            AUTHORIZATION_REVISION,
            path,
            pins["git_blob"],
        )
        _, verified_files[path] = _verified_file(
            path,
            pins["sha256"],
            canonical_bytes=canonical,
        )
        verified_files[path]["git_blob"] = pins["git_blob"]

    fixture_identity = _verify_fixture_provenance()
    catalog, catalog_identity = _verify_input_catalog()
    luna46 = json.loads(
        (ROOT / "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json").read_bytes()
    )
    if len(luna46["sequences"]) != 320:
        raise GateError("pinned Luna-46 diagnostic has the wrong stream count")
    inputs = json.loads((ROOT / "artifacts/luna47a/inputs.json").read_bytes())
    results = json.loads((ROOT / "artifacts/luna47a/results.json").read_bytes())

    phase_captures: dict[str, Record] = {}
    route_file_identities: dict[str, Record] = {}
    for phase in ("initial", "replay"):
        route_name = f"{phase}-destination_calibrated-reception.json"
        arm_name = f"{phase}-destination_calibrated.json"
        capture, route_file_identities[route_name] = _verify_catalog_artifact(
            route_name, catalog, parse=True
        )
        _, route_file_identities[arm_name] = _verify_catalog_artifact(
            arm_name, catalog, parse=False
        )
        if capture is None:
            raise GateError(f"missing retained {phase} raw-route capture")
        phase_captures[phase] = capture

    phases: dict[str, list[Record]] = {}
    reconciliation: dict[str, Record] = {}
    for phase in ("initial", "replay"):
        phases[phase], reconciliation[phase] = _verify_phase_reconciliation(
            phase, inputs, luna46, phase_captures[phase]
        )
    for stream_id in {row["stream_id"] for row in phases["initial"]}:
        initial = next(row for row in phases["initial"] if row["stream_id"] == stream_id)
        replay = next(row for row in phases["replay"] if row["stream_id"] == stream_id)
        if initial["raw_arrivals"] != replay["raw_arrivals"]:
            raise GateError(f"retained initial/replay input differs for {stream_id}")

    tau800_ids = sorted(
        row["stream_id"]
        for row in results["primary"]
        if row["original_category"] == "TEMPORAL-RETENTION-LIMITED"
        and row["variants"]["retention_tau800"]["crosses"]
    )
    declared_tau800_ids = sorted(
        protocol["predeclared_luna47a_tau800_retention_crossing_streams"]
    )
    if tau800_ids != declared_tau800_ids or len(tau800_ids) != 19:
        raise GateError("Luna-47A predeclared tau800 target IDs do not match retained results")
    for phase in ("initial", "replay"):
        if digest(phases[phase]) != digest(phases["initial"]):
            raise GateError("retained initial/replay stream inputs are not identical")

    identities = {
        "authorization_revision": AUTHORIZATION_REVISION,
        "execution_revision": revision,
        "runtime_source_blobs": runtime_sources,
        "pinned_files": verified_files,
        "luna44_fixture_provenance": fixture_identity,
        "luna45_catalog": {
            **catalog_identity,
            "artifact_digest": catalog["artifact_digest"],
            "catalog_entries_verified": route_file_identities,
        },
        "luna45_config": config_identity,
        "luna46": {
            "path": "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json",
            "stream_count": len(luna46["sequences"]),
            "output_digest": luna46.get("output_digest"),
        },
        "luna47a": {
            "inputs_path": "artifacts/luna47a/inputs.json",
            "results_path": "artifacts/luna47a/results.json",
            "tau800_target_crossings": tau800_ids,
        },
        "phase_reconciliation": reconciliation,
        "conditions": {
            "control_decay_rate_z": CONTROL_DECAY,
            "intervention_decay_rate_z": INTERVENTION_DECAY,
            "only_changed_path": config_identity["only_changed_path"],
        },
        "protocol_sha256": sha256((ROOT / PROTOCOL_PATH).read_bytes()),
        "config_sha256": sha256((ROOT / CONFIG_PATH).read_bytes()),
    }
    return identities, {
        "config": config,
        "protocol": protocol,
        "inputs": inputs,
        "luna46": luna46,
        "luna47a_results": results,
        "catalog": catalog,
        "route_captures": phase_captures,
        "phase_streams": phases,
    }


def _serialize_enum(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _serialize_enum(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {key: _serialize_enum(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serialize_enum(item) for item in value]
    return value


def _pending_state(neuron: MultiExcursionNeuron) -> Record | None:
    pending = neuron.pending_internal_event
    if pending is None:
        return None
    return {
        "neuron_id": pending.neuron_id,
        "episode_id": pending.episode_id,
        "generation": pending.generation,
        "kind": pending.kind.value,
        "timestamp": pending.timestamp,
        "queue_sequence": pending.queue_sequence,
    }


def _neuron_state(neuron: MultiExcursionNeuron) -> Record:
    return {
        "x": float(neuron.x),
        "z": float(neuron.integration_state or 0.0),
        "clock": float(neuron.clock.timestamp),
        "mode": neuron.mode.value,
        "ordinary_episode_id": neuron.ordinary_episode_id,
        "multi_episode_id": neuron.multi_episode_id,
        "m_phase": None if neuron.m_phase is None else neuron.m_phase.value,
        "generation_token": neuron.generation_token,
        "processed_event_count": neuron.processed_event_count,
        "pending_event": _pending_state(neuron),
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


def _make_destination_config(config: Record, condition: str) -> E1Config:
    destination = deepcopy(config["historical_destination"])
    destination["integration"]["decay_rate_z"] = config["conditions"][condition]["decay_rate_z"]
    integration = IntegrationConfig(**destination.pop("integration"))
    return E1Config(**destination, integration=integration)


def run_stream(arrivals: list[Record], config: E1Config) -> Record:
    """Run one label-free destination-only E2 execution from retained arrivals."""
    if not isinstance(config, E1Config) or config.integration is None:
        raise TypeError("Luna-53 requires the existing integration-enabled E2 neuron")
    if config.event_budget != EVENT_BUDGET:
        raise GateError("destination event budget differs from the frozen contract")
    ordered = sorted(arrivals, key=lambda item: item["source_queue_sequence"])
    if len(ordered) != len(arrivals):
        raise GateError("arrival inventory changed during execution")

    queue: EventQueue[Event] = EventQueue(QUEUE_CAPACITY)
    source_sequence_by_runtime_sequence: dict[int, int] = {}
    input_identity_by_event_id: dict[str, Record] = {}
    for arrival in ordered:
        if arrival["event_type"] != EventType.EXCURSION.value:
            raise GateError("unsupported retained external event type")
        event = Event(
            timestamp=arrival["timestamp"],
            source=arrival["source"],
            destination=arrival["destination"],
            event_type=EventType.EXCURSION,
            payload=arrival["payload"],
            event_id=arrival["event_id"],
            lineage_id=arrival["lineage_id"],
        )
        queued = queue.push(event)
        source_sequence_by_runtime_sequence[queued.sequence] = arrival["source_queue_sequence"]
        if arrival["event_id"] in input_identity_by_event_id:
            raise GateError("duplicate retained event identity")
        input_identity_by_event_id[arrival["event_id"]] = arrival

    neuron = MultiExcursionNeuron(
        "destination",
        config=config,
        initial_timestamp=0.0,
    )
    event_records: list[Record] = []

    def handle(event: Event, active_queue: EventQueue[Event]) -> None:
        before = _neuron_state(neuron)
        integration_count = len(neuron.integration_trace)
        emission_count = len(neuron.emissions)
        if event.event_type == EventType.INTERNAL:
            pending_payload = _serialize_enum(event.payload)
            source_queue_sequence = None
        else:
            pending_payload = None
            if event.sequence not in source_sequence_by_runtime_sequence:
                raise GateError("runtime external event is not a retained arrival")
            source_queue_sequence = source_sequence_by_runtime_sequence[event.sequence]
        neuron.receive_event(event, active_queue)
        after = _neuron_state(neuron)
        trace = None
        if len(neuron.integration_trace) != integration_count:
            if len(neuron.integration_trace) != integration_count + 1:
                raise GateError("unexpected integration trace growth")
            trace = _serialize_enum(neuron.integration_trace[-1])
        new_emissions = list(neuron.emissions)[emission_count:]
        event_records.append({
            "runtime_queue_sequence": event.sequence,
            "source_queue_sequence": source_queue_sequence,
            "event_type": (
                event.event_type.value
                if isinstance(event.event_type, EventType)
                else str(event.event_type)
            ),
            "source": event.source,
            "destination": event.destination,
            "event_id": event.event_id,
            "lineage_id": event.lineage_id,
            "timestamp": float(event.timestamp),
            "payload": float(event.payload) if event.event_type != EventType.INTERNAL else None,
            "payload_bits": (
                float_bits(float(event.payload))
                if event.event_type != EventType.INTERNAL
                else None
            ),
            "internal_payload": pending_payload,
            "before": before,
            "after": after,
            "integration_trace": trace,
            "emissions": [_emission_record(item) for item in new_emissions],
        })

    execution = execute_bounded(queue, handle, event_budget=EVENT_BUDGET)
    if not execution.completed or execution.pending_event_count != 0:
        raise GateError("bounded E2 event execution did not complete")
    if execution.processed_event_count != neuron.processed_event_count:
        raise GateError("runtime and neuron event counters disagree")
    if neuron.out_of_scope or neuron.boundary_reports:
        raise GateError("E2 execution reached an unauthorized boundary")
    recurrence = audit_recurrence(event_records, config)
    emissions = [_emission_record(item) for item in neuron.emissions]
    traces = [
        _serialize_enum(trace)
        for trace in neuron.integration_trace
    ]
    if len(traces) != len(arrivals):
        raise GateError("one retained external arrival did not produce one E2 integration trace")
    peak_pre_discharge = max(
        (abs(float(trace["z_after_input"])) for trace in traces),
        default=0.0,
    )
    peak_post_discharge = max(
        (abs(float(trace["z_post_discharge"])) for trace in traces),
        default=0.0,
    )
    threshold_crossings = [
        trace for trace in traces
        if abs(float(trace["z_after_input"])) >= config.integration.discharge_quantum
    ]
    discharges = [
        trace for trace in traces
        if float(trace["discharge_amount"]) != 0.0
    ]
    clipping_events = []
    for trace in traces:
        z_unclipped = float(trace["z_after_decay"])
        if trace["integrated"]:
            z_unclipped += config.integration.input_gain * float(trace["input_value"])
        if abs(z_unclipped) > config.integration.z_max:
            clipping_events.append({
                "timestamp": trace["timestamp"],
                "kind": "z",
                "unclipped": z_unclipped,
                "limit": config.integration.z_max,
            })
        x_unclipped = float(trace["x_after_decay"]) + float(trace["input_value"])
        if abs(x_unclipped) > config.x_max:
            clipping_events.append({
                "timestamp": trace["timestamp"],
                "kind": "x",
                "unclipped": x_unclipped,
                "limit": config.x_max,
            })

    return {
        "input_event_count": len(arrivals),
        "input_events": deepcopy(ordered),
        "events": event_records,
        "integration_traces": traces,
        "emissions": emissions,
        "final_state": _neuron_state(neuron),
        "execution": {
            "completed": execution.completed,
            "budget_exhausted": execution.budget_exhausted,
            "configured_event_budget": execution.configured_event_budget,
            "processed_event_count": execution.processed_event_count,
            "pending_event_count": execution.pending_event_count,
            "termination_reason": execution.termination_reason,
            "last_event_timestamp": execution.last_event_timestamp,
            "peak_queue_occupancy": execution.peak_queue_occupancy,
            "neuron_processed_event_count": neuron.processed_event_count,
            "generation_token": neuron.generation_token,
        },
        "recurrence_oracle": recurrence,
        "max_abs_z_before_discharge": peak_pre_discharge,
        "max_abs_z_after_discharge": peak_post_discharge,
        "threshold": config.integration.discharge_quantum,
        "threshold_margin": config.integration.discharge_quantum - peak_pre_discharge,
        "crossed_threshold": bool(threshold_crossings),
        "threshold_crossing_count": len(threshold_crossings),
        "first_threshold_crossing_time": (
            float(threshold_crossings[0]["timestamp"]) if threshold_crossings else None
        ),
        "discharge_count": len(discharges),
        "canonical_emission_count": len(emissions),
        "linked_integration_emissions": _linked_integration_emissions(traces, emissions),
        "clipping_events": clipping_events,
    }


def audit_recurrence(event_records: list[Record], config: E1Config) -> Record:
    """Independently recompute event-time z decay/deposition/discharge equations."""
    assert config.integration is not None
    z_state = 0.0
    last_clock = 0.0
    checks = 0
    max_abs_error = 0.0
    for record in event_records:
        before = record["before"]
        after = record["after"]
        _require_same_float(float(before["z"]), z_state, "oracle prior z")
        if float(before["clock"]) != last_clock:
            raise GateError("oracle local-clock continuity failure")
        event_type = record["event_type"]
        if event_type == EventType.INTERNAL.value:
            expected_advance = float(record["timestamp"]) - last_clock
            advanced = float(after["clock"]) - last_clock
            if advanced not in (0.0, expected_advance):
                raise GateError("internal E2 event advanced to an unexpected local time")
            dt = advanced
            expected_decay = z_state * math.exp(-config.integration.decay_rate_z * dt)
            expected_post = expected_decay
            trace = None
        else:
            dt = float(record["timestamp"]) - last_clock
            if float(after["clock"]) != float(record["timestamp"]):
                raise GateError("external E2 arrival did not advance local time to its timestamp")
            expected_decay = z_state * math.exp(-config.integration.decay_rate_z * dt)
            trace = record["integration_trace"]
            if trace is None:
                raise GateError("external event is missing its integration trace")
            _require_same_float(float(trace["z_before_decay"]), z_state, "trace prior z")
            _require_same_float(float(trace["z_after_decay"]), expected_decay, "trace z decay")
            integrated = (
                trace["mode_before"] == "N"
                and abs(float(trace["x_after_input"])) < config.theta_e
            )
            if bool(trace["integrated"]) != integrated:
                raise GateError("integration qualification differs from E2 state/input rule")
            expected_input = expected_decay
            if integrated:
                expected_input = max(
                    -config.integration.z_max,
                    min(
                        config.integration.z_max,
                        expected_decay + config.integration.input_gain * float(record["payload"]),
                    ),
                )
            _require_same_float(
                float(trace["z_after_input"]), expected_input, "oracle z after input"
            )
            should_discharge = (
                integrated
                and abs(expected_input) >= config.integration.discharge_quantum
                and float(trace["x_after_input"]) * expected_input >= 0.0
            )
            expected_discharge = (
                math.copysign(config.integration.discharge_quantum, expected_input)
                if should_discharge
                else 0.0
            )
            if float(trace["discharge_amount"]) != expected_discharge:
                raise GateError("E2 discharge differs from independent threshold/sign oracle")
            expected_post = expected_input - expected_discharge
            _require_same_float(
                float(trace["z_post_discharge"]), expected_post, "oracle z after discharge"
            )
            checks += 1

        _require_same_float(float(after["z"]), expected_post, "oracle event z state")
        error = abs(float(after["z"]) - expected_post)
        max_abs_error = max(max_abs_error, error)
        z_state = expected_post
        last_clock = float(after["clock"])
    return {
        "passed": True,
        "equation": "z_next = clip(z * exp(-decay_rate_z * local_dt) + kappa * v) then sign-qualified subtractive discharge",
        "external_updates_checked": checks,
        "processed_events_checked": len(event_records),
        "max_abs_residual": max_abs_error,
        "tolerance_formula": (
            "64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))"
        ),
    }


def _linked_integration_emissions(traces: list[Record], emissions: list[Record]) -> list[Record]:
    emissions_by_id = {item["event_id"]: item for item in emissions}
    linked: list[Record] = []
    for trace in traces:
        if float(trace["discharge_amount"]) == 0.0:
            continue
        emission_id = trace.get("emission_id")
        emission = emissions_by_id.get(emission_id)
        linked.append({
            "discharge_timestamp": trace["timestamp"],
            "discharge_amount": trace["discharge_amount"],
            "integration_emission_id": emission_id,
            "canonical_emission": emission,
            "emission_linked": emission is not None,
        })
    return linked


def _arrivals_for_stream(stream: Record) -> list[Record]:
    arrivals: list[Record] = []
    for item in stream["raw_arrivals"]:
        reception = item["raw_reception"]
        enqueue = item["raw_enqueue"]
        arrival = {
            "event_id": item["event_id"],
            "source_queue_sequence": int(item["queue_sequence"]),
            "timestamp": float(item["timestamp"]),
            "payload": float(item["payload"]),
            "payload_bits": float_bits(float(item["payload"])),
            "source": reception["source"],
            "destination": reception["destination"],
            "event_type": reception["event_type"],
            "lineage_id": reception.get("lineage_id"),
            "originating_emission_id": reception.get("originating_emission_id"),
            "route_path": list(reception["route_path"]),
            "route_depth": int(reception["route_depth"]),
            "enqueue_timestamp": float(enqueue["enqueue_timestamp"]),
            "scheduled_delivery_timestamp": float(enqueue["scheduled_delivery_timestamp"]),
        }
        if (
            arrival["event_id"] != reception["event_id"]
            or arrival["source_queue_sequence"] != reception["queue_sequence"]
            or arrival["timestamp"] != reception["reception_timestamp"]
            or arrival["payload_bits"] != reception["payload_bits"]
            or arrival["timestamp"] != arrival["scheduled_delivery_timestamp"]
        ):
            raise GateError(f"retained arrival identity differs for {stream['stream_id']}")
        arrivals.append(arrival)
    return arrivals


def _serialize_integration_trace(trace: Any) -> Record:
    result = _serialize_enum(trace)
    for key in ("x_before_decay", "x_after_decay", "z_before_decay", "z_after_decay",
                "x_after_input", "z_after_input", "x_post_discharge", "z_post_discharge"):
        result[key] = float(result[key])
    result["timestamp"] = float(result["timestamp"])
    result["elapsed"] = float(result["elapsed"])
    result["input_value"] = float(result["input_value"])
    return result


def _baseline_compatibility(
    streams: list[Record],
    outputs: list[Record],
    baseline_arm: Record,
    luna46: Record,
) -> Record:
    expected_by_id = {item["stream_id"]: item for item in baseline_arm["records"]}
    l46_by_id = {item["stream_id"]: item for item in luna46["sequences"]}
    failures: list[Record] = []
    compared = 0
    for stream, output in zip(streams, outputs, strict=True):
        stream_id = stream["stream_id"]
        expected_record = expected_by_id[stream_id]
        expected_traces = expected_record["destination_integration_trace"]
        observed_traces = output["integration_traces"]
        if len(expected_traces) != len(observed_traces):
            failures.append({
                "stream_id": stream_id,
                "field": "trace_count",
                "expected": len(expected_traces),
                "observed": len(observed_traces),
            })
            continue
        for index, (expected, observed) in enumerate(zip(expected_traces, observed_traces, strict=True)):
            for field in (
                "timestamp", "elapsed", "input_value", "theta_e", "theta_z",
                "decay_rate", "decay_rate_z", "mode_before", "x_before_decay",
                "x_after_decay", "z_before_decay", "z_after_decay", "x_after_input",
                "z_after_input", "integrated", "discharge_amount",
                "x_post_discharge", "z_post_discharge", "crossed_theta_e",
                "classification", "emission_id",
            ):
                actual_value = observed.get(field)
                expected_value = expected.get(field)
                matches = (
                    _same_float(float(actual_value), float(expected_value))
                    if isinstance(actual_value, (int, float))
                    and not isinstance(actual_value, bool)
                    and isinstance(expected_value, (int, float))
                    and not isinstance(expected_value, bool)
                    else actual_value == expected_value
                )
                if not matches:
                    failures.append({
                        "stream_id": stream_id,
                        "event_index": index,
                        "field": field,
                        "expected": expected_value,
                        "observed": actual_value,
                    })
                    break
            compared += 1
        diagnostic = l46_by_id[stream_id]
        l46_rows = diagnostic["recurrence_evidence"]
        if len(l46_rows) != len(observed_traces):
            failures.append({
                "stream_id": stream_id,
                "field": "luna46_recurrence_count",
                "expected": len(l46_rows),
                "observed": len(observed_traces),
            })
        for index, (expected, observed) in enumerate(zip(l46_rows, observed_traces)):
            if expected["event_id"] != output["input_events"][index]["event_id"]:
                failures.append({
                    "stream_id": stream_id,
                    "event_index": index,
                    "field": "luna46_event_id",
                })
                continue
            if float(observed["discharge_amount"]) != 0.0:
                failures.append({
                    "stream_id": stream_id,
                    "event_index": index,
                    "field": "unexpected_historical_discharge",
                })
            if not _same_float(
                float(observed["z_after_input"]), float(expected["state_after"])
            ):
                failures.append({
                    "stream_id": stream_id,
                    "event_index": index,
                    "field": "luna46_state_after",
                    "expected": expected["state_after"],
                    "observed": observed["z_after_input"],
                })
        if output["emissions"]:
            failures.append({
                "stream_id": stream_id,
                "field": "unexpected_historical_canonical_emission",
                "count": len(output["emissions"]),
            })
    return {
        "passed": not failures,
        "luna45_streams_compared": len(outputs),
        "luna45_integration_traces_compared": compared,
        "luna46_streams_compared": len(outputs),
        "failures": failures[:100],
        "failure_count": len(failures),
        "tolerance_formula": (
            "64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))"
        ),
    }


def _class_summary(records: list[Record], condition: str) -> Record:
    result: dict[str, Record] = {}
    for category in (
        "TEMPORAL-RETENTION-LIMITED",
        "DRIVE-LIMITED",
        "NO-RECEPTIONS",
    ):
        group = [item for item in records if item["category"] == category]
        max_z = [float(item["max_abs_z_before_discharge"]) for item in group]
        margins = [float(item["threshold_margin"]) for item in group]
        result[category] = {
            "n": len(group),
            "destination_receptions": sum(item["input_event_count"] for item in group),
            "total_signed_drive": sum(
                float(event["payload"])
                for item in group
                for event in item["input_events"]
            ),
            "total_absolute_drive": sum(
                abs(float(event["payload"]))
                for item in group
                for event in item["input_events"]
            ),
            "threshold_crossing_streams": sum(bool(item["crossed_threshold"]) for item in group),
            "discharge_streams": sum(item["discharge_count"] > 0 for item in group),
            "discharge_count": sum(item["discharge_count"] for item in group),
            "canonical_emission_streams": sum(
                item["canonical_emission_count"] > 0 for item in group
            ),
            "canonical_emission_count": sum(
                item["canonical_emission_count"] for item in group
            ),
            "peak_state": _distribution(max_z),
            "threshold_margin": _distribution(margins),
            "clipping_event_count": sum(len(item["clipping_events"]) for item in group),
            "max_processed_events_per_stream": max(
                (item["execution"]["processed_event_count"] for item in group),
                default=0,
            ),
        }
    return {"condition": condition, "classes": result}


def _distribution(values: list[float]) -> Record:
    ordered = sorted(values)
    if not ordered:
        return {"count": 0, "minimum": None, "median": None, "mean": None, "maximum": None}
    middle = len(ordered) // 2
    median = (
        ordered[middle]
        if len(ordered) % 2
        else (ordered[middle - 1] + ordered[middle]) / 2.0
    )
    return {
        "count": len(ordered),
        "minimum": ordered[0],
        "median": median,
        "mean": sum(ordered) / len(ordered),
        "maximum": ordered[-1],
    }


def _paired_summary(control: list[Record], intervention: list[Record]) -> Record:
    by_control = {item["stream_id"]: item for item in control}
    by_intervention = {item["stream_id"]: item for item in intervention}
    if by_control.keys() != by_intervention.keys():
        raise GateError("condition stream identities differ")
    paired: dict[str, list[Record]] = defaultdict(list)
    for stream_id in sorted(by_control):
        left = by_control[stream_id]
        right = by_intervention[stream_id]
        if left["category"] != right["category"]:
            raise GateError(f"condition category metadata differs for {stream_id}")
        category = left["category"]
        peak_delta = (
            float(right["max_abs_z_before_discharge"])
            - float(left["max_abs_z_before_discharge"])
        )
        margin_delta = float(right["threshold_margin"]) - float(left["threshold_margin"])
        paired[category].append({
            "stream_id": stream_id,
            "control_peak_abs_z": left["max_abs_z_before_discharge"],
            "intervention_peak_abs_z": right["max_abs_z_before_discharge"],
            "peak_abs_z_delta": peak_delta,
            "control_threshold_margin": left["threshold_margin"],
            "intervention_threshold_margin": right["threshold_margin"],
            "threshold_margin_delta": margin_delta,
            "control_crossed": left["crossed_threshold"],
            "intervention_crossed": right["crossed_threshold"],
            "new_threshold_crossing": (
                right["crossed_threshold"] and not left["crossed_threshold"]
            ),
            "control_discharges": left["discharge_count"],
            "intervention_discharges": right["discharge_count"],
            "new_integration_discharge": (
                right["discharge_count"] > left["discharge_count"]
            ),
            "control_linked_emissions": sum(
                item["emission_linked"] for item in left["linked_integration_emissions"]
            ),
            "intervention_linked_emissions": sum(
                item["emission_linked"] for item in right["linked_integration_emissions"]
            ),
            "new_linked_emission": (
                len(right["linked_integration_emissions"])
                > len(left["linked_integration_emissions"])
                and all(
                    item["emission_linked"]
                    for item in right["linked_integration_emissions"]
                )
            ),
        })
    summary: dict[str, Record] = {}
    for category, rows in paired.items():
        summary[category] = {
            "n": len(rows),
            "new_threshold_crossings": sum(row["new_threshold_crossing"] for row in rows),
            "newly_rescued_with_linked_emission": sum(
                row["new_integration_discharge"] and row["new_linked_emission"]
                for row in rows
            ),
            "control_crossing_streams": sum(row["control_crossed"] for row in rows),
            "intervention_crossing_streams": sum(row["intervention_crossed"] for row in rows),
            "control_discharge_streams": sum(row["control_discharges"] > 0 for row in rows),
            "intervention_discharge_streams": sum(
                row["intervention_discharges"] > 0 for row in rows
            ),
            "control_linked_emission_streams": sum(
                row["control_linked_emissions"] > 0 for row in rows
            ),
            "intervention_linked_emission_streams": sum(
                row["intervention_linked_emissions"] > 0 for row in rows
            ),
            "control_canonical_emission_streams": sum(
                by_control[row["stream_id"]]["canonical_emission_count"] > 0
                for row in rows
            ),
            "intervention_canonical_emission_streams": sum(
                by_intervention[row["stream_id"]]["canonical_emission_count"] > 0
                for row in rows
            ),
            "peak_abs_z_delta": _distribution(
                [row["peak_abs_z_delta"] for row in rows]
            ),
            "threshold_margin_delta": _distribution(
                [row["threshold_margin_delta"] for row in rows]
            ),
            "state_delta_by_stream": rows,
        }

    target = summary["TEMPORAL-RETENTION-LIMITED"]
    drives = summary["DRIVE-LIMITED"]
    no_reception = [
        item for item in intervention if item["category"] == "NO-RECEPTIONS"
    ]
    if any(
        item["input_event_count"] != 0
        or item["events"]
        or item["emissions"]
        or item["final_state"]["x"] != 0.0
        or item["final_state"]["z"] != 0.0
        for item in no_reception
    ):
        raise GateError("no-reception group acquired an event, state, or emission")
    no_reception_summary = summary["NO-RECEPTIONS"]
    if target["newly_rescued_with_linked_emission"] > 0 and (
        drives["intervention_discharge_streams"] == 0
        and drives["intervention_canonical_emission_streams"] == 0
        and no_reception_summary["intervention_discharge_streams"] == 0
        and no_reception_summary["intervention_canonical_emission_streams"] == 0
    ):
        verdict = "SUPPORTED"
    elif (
        target["new_threshold_crossings"] > 0
        or target["intervention_discharge_streams"] > 0
        or any(row["peak_abs_z_delta"] != 0.0 for row in target["state_delta_by_stream"])
    ):
        verdict = "PARTIALLY SUPPORTED"
    else:
        verdict = "NOT SUPPORTED"
    return {
        "classes": summary,
        "no_reception_invariant": "PASS",
        "contract_verdict": verdict,
    }


def _input_event_records(stream_results: list[Record]) -> Record:
    output: list[Record] = []
    for stream in stream_results:
        for event in stream["events"]:
            if event["event_type"] != EventType.EXCURSION.value:
                continue
            output.append({
                "stream_id": stream["stream_id"],
                "event_id": event["event_id"],
                "source_queue_sequence": event["source_queue_sequence"],
                "runtime_queue_sequence": event["runtime_queue_sequence"],
                "timestamp": event["timestamp"],
                "payload": event["payload"],
                "payload_bits": event["payload_bits"],
            })
    return {"external_event_count": len(output), "events": output}


def _condition_record(
    stream: Record,
    phase: str,
    condition: str,
    config: Record,
    luna46: Record,
) -> Record:
    arrivals = _arrivals_for_stream(stream)
    neuron_config = _make_destination_config(config, condition)
    raw = run_stream(arrivals, neuron_config)
    return {
        "stream_id": stream["stream_id"],
        "category": stream["category"],
        "phase": phase,
        "reset_identity": f"{phase}:{condition}:{stream['stream_id']}",
        "luna46_fixture_sequence_sha256": stream["fixture_sequence_sha256"],
        "luna47a_input_digest": stream["input_digest"],
        "destination_receptions": len(arrivals),
        "total_signed_drive": sum(float(event["payload"]) for event in arrivals),
        "total_absolute_drive": sum(abs(float(event["payload"])) for event in arrivals),
        "reception_intervals": [
            float(right["timestamp"]) - float(left["timestamp"])
            for left, right in zip(arrivals, arrivals[1:])
        ],
        **raw,
    }


def _scientific_payload(
    condition: str,
    config: Record,
    class_summary: Record,
    streams: list[Record],
) -> Record:
    phase_independent_streams = [
        {
            key: value
            for key, value in stream.items()
            if key not in {"phase", "reset_identity"}
        }
        for stream in streams
    ]
    return {
        "condition": condition,
        "decay_rate_z": config["conditions"][condition]["decay_rate_z"],
        "destination_config": _make_config_dict(config, condition),
        "class_summary": class_summary,
        "streams": phase_independent_streams,
    }


def _control_file(phase: str) -> Path:
    return ROOT / OUTPUT_DIRECTORY / f"luna53-control-{phase}.json"


def _read_run_file(path: Path) -> Record:
    if not path.is_file():
        raise GateError(f"required prior Luna-53 control output does not exist: {path}")
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict) or value.get("schema") != "TPCN-LUNA53-RUN-1":
        raise GateError(f"invalid Luna-53 run result: {path}")
    return value


def _require_control_gate() -> None:
    for required_phase in ("initial", "replay"):
        path = _control_file(required_phase)
        if not path.exists():
            raise GateError(f"{required_phase} historical-control execution is required first")
        prior = _read_run_file(path)
        if prior.get("condition") != "control" or not prior["baseline_compatibility"]["passed"]:
            raise GateError("historical control reproduction failed; intervention is blocked")
    if all(_control_file(item).exists() for item in ("initial", "replay")):
        initial = _read_run_file(_control_file("initial"))
        replay = _read_run_file(_control_file("replay"))
        if initial["scientific_digest"] != replay["scientific_digest"]:
            raise GateError("historical control initial/replay outcomes are not identical")


def run_one(
    phase: str,
    condition: str,
    execution_id: str,
    *,
    output_path: Path | None = None,
) -> Record:
    if phase not in ("initial", "replay") or condition not in ("control", "intervention"):
        raise ValueError("invalid Luna-53 phase or condition")
    if not re.fullmatch(r"[A-Za-z0-9_-]{4,80}", execution_id):
        raise ValueError("execution_id must be a fresh bounded identifier")
    revision = _run_git("rev-parse", "HEAD")
    if revision == AUTHORIZATION_REVISION:
        raise GateError("commit Luna-53 protocol, configuration, runner, and tests before execution")
    dirty_lane = subprocess.run(
        [
            "git", "diff", "--quiet", "HEAD", "--",
            "experiments/luna53", "tests/test_luna53_retention.py",
        ],
        cwd=ROOT,
        check=False,
    )
    if dirty_lane.returncode != 0:
        raise GateError("Luna-53 implementation/protocol changed after its execution commit")
    identities, data = verify_provenance(revision)
    config = data["config"]
    if condition == "intervention":
        _require_control_gate()

    streams = data["phase_streams"][phase]
    result_records = [
        _condition_record(stream, phase, condition, config, data["luna46"])
        for stream in streams
    ]
    if condition == "control":
        baseline_path = (
            f"artifacts/luna45-acp0008-depth2-destination-integration-20261006/"
            f"{phase}-destination_calibrated.json"
        )
        expected_sha = data["catalog"]["files"][f"{phase}-destination_calibrated.json"]["file_sha256"]
        baseline_arm, _ = _read_json(
            baseline_path,
            expected_sha,
            expected_size=data["catalog"]["files"][f"{phase}-destination_calibrated.json"]["byte_length"],
        )
        compatibility = _baseline_compatibility(
            streams,
            result_records,
            baseline_arm,
            data["luna46"],
        )
        if not compatibility["passed"]:
            raise GateError(
                "historical control failed Luna-45/Luna-46 reproduction: "
                f"{compatibility['failure_count']} mismatches"
            )
    else:
        compatibility = {
            "passed": True,
            "required_historical_control_files": [
                str(_control_file("initial").relative_to(ROOT)),
                str(_control_file("replay").relative_to(ROOT)),
            ],
            "intervention_not_used_for_control_gate": True,
        }

    class_summary = _class_summary(result_records, condition)
    event_summary = _input_event_records(result_records)
    scientific_payload = _scientific_payload(
        condition, config, class_summary, result_records
    )
    output = {
        "schema": "TPCN-LUNA53-RUN-1",
        "authorization_revision": AUTHORIZATION_REVISION,
        "execution_revision": revision,
        "execution_id": execution_id,
        "phase": phase,
        "condition": condition,
        "fresh_process_execution": True,
        "labels_entered_runtime": False,
        "upstream_route_executed": False,
        "destination_outputs_rerouted": False,
        "input_event_inventory": event_summary,
        "provenance": identities,
        "condition_configuration": scientific_payload["destination_config"],
        "baseline_compatibility": compatibility,
        "scientific_digest": digest(scientific_payload),
        "class_summary": class_summary,
        "streams": result_records,
    }
    if output_path is None:
        output_path = ROOT / OUTPUT_DIRECTORY / f"luna53-{condition}-{phase}.json"
    resolved_output = output_path.resolve()
    if resolved_output.parent != (ROOT / OUTPUT_DIRECTORY).resolve():
        raise ValueError("Luna-53 output must be directly under artifacts/luna53")
    if resolved_output.exists():
        raise FileExistsError(f"refusing to overwrite Luna-53 evidence: {resolved_output}")
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_bytes(canonical_bytes(output) + b"\n")
    output["artifact_sha256"] = sha256(resolved_output.read_bytes())
    return output


def _make_config_dict(config: Record, condition: str) -> Record:
    result = deepcopy(config["historical_destination"])
    result["integration"]["decay_rate_z"] = config["conditions"][condition]["decay_rate_z"]
    return result


def summarize_outputs() -> Record:
    required = {
        (condition, phase): ROOT / OUTPUT_DIRECTORY / f"luna53-{condition}-{phase}.json"
        for condition in ("control", "intervention")
        for phase in ("initial", "replay")
    }
    outputs: dict[tuple[str, str], Record] = {}
    execution_revisions: set[str] = set()
    for key, path in required.items():
        outputs[key] = _read_run_file(path)
        if outputs[key]["condition"] != key[0] or outputs[key]["phase"] != key[1]:
            raise GateError(f"unexpected run identity/configuration in {path.name}")
        scientific_payload = _scientific_payload(
            key[0],
            {
                "conditions": {
                    "control": {"decay_rate_z": CONTROL_DECAY},
                    "intervention": {"decay_rate_z": INTERVENTION_DECAY},
                },
                "historical_destination": outputs[key]["condition_configuration"],
            },
            outputs[key]["class_summary"],
            outputs[key]["streams"],
        )
        if outputs[key]["scientific_digest"] != digest(scientific_payload):
            raise GateError(f"scientific digest mismatch in {path.name}")
        execution_revisions.add(outputs[key]["execution_revision"])
    if len(execution_revisions) != 1:
        raise GateError("phase-condition executions used different source revisions")
    ids = [item["execution_id"] for item in outputs.values()]
    if len(set(ids)) != 4:
        raise GateError("phase-condition runs must have distinct execution IDs")
    for phase in ("initial", "replay"):
        control = outputs[("control", phase)]
        if not control["baseline_compatibility"]["passed"]:
            raise GateError(f"{phase} historical control reproduction did not pass")
        intervention = outputs[("intervention", phase)]
        if intervention["condition_configuration"]["integration"]["decay_rate_z"] != INTERVENTION_DECAY:
            raise GateError("intervention result carries the wrong decay value")
    for condition in ("control", "intervention"):
        if outputs[(condition, "initial")]["scientific_digest"] != outputs[(condition, "replay")]["scientific_digest"]:
            raise GateError(f"{condition} initial/replay records are not bit-identical")

    control = outputs[("control", "initial")]["streams"]
    intervention = outputs[("intervention", "initial")]["streams"]
    paired = _paired_summary(control, intervention)
    no_reception_control = [
        item for item in control if item["category"] == "NO-RECEPTIONS"
    ]
    no_reception_intervention = [
        item for item in intervention if item["category"] == "NO-RECEPTIONS"
    ]
    if any(
        item["input_event_count"] != 0 or item["events"] or item["emissions"]
        for item in no_reception_control + no_reception_intervention
    ):
        raise GateError("no-reception group received an event or emitted")
    evidence_files: dict[str, Record] = {}
    for (condition, phase), path in required.items():
        evidence_files[str(path.relative_to(ROOT))] = {
            "sha256": sha256(path.read_bytes()),
            "bytes": path.stat().st_size,
            "execution_id": outputs[(condition, phase)]["execution_id"],
            "scientific_digest": outputs[(condition, phase)]["scientific_digest"],
        }
    summary = {
        "schema": "TPCN-LUNA53-SUMMARY-1",
        "authorization_revision": AUTHORIZATION_REVISION,
        "execution_revision": outputs[("control", "initial")]["execution_revision"],
        "condition_pair": {
            "control_decay_rate_z": CONTROL_DECAY,
            "intervention_decay_rate_z": INTERVENTION_DECAY,
            "only_changed_path": "destination.integration.decay_rate_z",
        },
        "phase_condition_executions": evidence_files,
        "historical_control_compatibility": {
            phase: outputs[("control", phase)]["baseline_compatibility"]
            for phase in ("initial", "replay")
        },
        "class_summary_by_condition": {
            condition: outputs[(condition, "initial")]["class_summary"]
            for condition in ("control", "intervention")
        },
        "paired_causal_class_summary": paired,
        "retained_initial_replay_exact": True,
        "no_reception_invariant": "PASS",
        "forbidden_interpretations": [
            "task-level efficacy",
            "general TPCN performance improvement",
            "optimal or production decay_rate_z",
            "architecture promotion",
            "structural-growth efficacy",
            "hardware equivalence or biological plausibility",
            "superiority over other neural architectures",
        ],
    }
    summary["artifact_digest"] = digest(summary)
    return summary


def _write_summary() -> Record:
    summary = summarize_outputs()
    path = ROOT / OUTPUT_DIRECTORY / "summary.json"
    if path.exists():
        raise FileExistsError(f"refusing to overwrite Luna-53 summary: {path}")
    path.write_bytes(canonical_bytes(summary) + b"\n")
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--run-one", action="store_true")
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--phase", choices=("initial", "replay"))
    parser.add_argument("--condition", choices=("control", "intervention"))
    parser.add_argument("--execution-id")
    args = parser.parse_args(argv)
    modes = sum((args.preflight, args.run_one, args.summarize))
    if modes != 1:
        parser.error("choose exactly one of --preflight, --run-one, or --summarize")
    try:
        if args.preflight:
            identities, _ = verify_provenance()
            print(json.dumps({
                "status": "PASS",
                "authorization_revision": AUTHORIZATION_REVISION,
                "execution_revision": identities["execution_revision"],
                "streams_per_phase": 320,
                "destination_arrivals_per_phase": 235,
                "phase_reconciliation": identities["phase_reconciliation"],
            }, sort_keys=True))
            return 0
        if args.run_one:
            if not args.phase or not args.condition or not args.execution_id:
                parser.error("--run-one requires --phase, --condition, and --execution-id")
            result = run_one(args.phase, args.condition, args.execution_id)
            print(json.dumps({
                "status": "PASS",
                "condition": args.condition,
                "phase": args.phase,
                "execution_id": args.execution_id,
                "streams": len(result["streams"]),
                "scientific_digest": result["scientific_digest"],
                "artifact_sha256": result["artifact_sha256"],
            }, sort_keys=True))
            return 0
        summary = _write_summary()
        print(json.dumps({
            "status": "PASS",
            "contract_verdict": summary["paired_causal_class_summary"]["contract_verdict"],
            "artifact_sha256": sha256(
                (ROOT / OUTPUT_DIRECTORY / "summary.json").read_bytes()
            ),
        }, sort_keys=True))
        return 0
    except (GateError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"LUNA-53 BLOCKED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
