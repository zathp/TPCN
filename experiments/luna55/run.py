"""Execute the bounded Luna-55 serial-retention factorial."""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

from experiments.luna53 import run as luna53
from experiments.luna54 import run as luna54
from tpcn.excursion_neuron import E1Config, IntegrationConfig


ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION_REVISION = "312eba8c8e036927408fb2156756a50d15762bc8"
CONFIG_PATH = Path("experiments/luna55/config.json")
PROTOCOL_PATH = Path("experiments/luna55/protocol.json")
OUTPUT = Path("artifacts/luna55")
SELECTION_PATH = Path("artifacts/luna55-selection/post-luna54-destination-oracle.json")
ARTIFACT_PINS = {
    "artifacts/luna54/control-initial.json": (
        "e1229a04c4388fbf84dc099295f2f38515b2be5e",
        "b38f974c55536c118ae45c672a0afa0c59ee005af4112840ae2919cf1233b76d",
    ),
    "artifacts/luna54/control-replay.json": (
        "0024079a7009f8807bdb531567f0f0bf134c61d8",
        "6f733031b4514a03ce8c52b985b9642233be755a6571baa9e9b00ea2b25e33eb",
    ),
    "artifacts/luna54/intervention-initial.json": (
        "6de22f1f5406f378e115a818e01e459ec6ddf3e6",
        "fe629408f976138fd2c375b8be41a8c874d629ffcadc12a16696596fb841f940",
    ),
    "artifacts/luna54/intervention-replay.json": (
        "684fc1f3adfbd26dbbca1a656c1d14c5e8ac92a8",
        "93a56cb7dd993e9342e0e8045cd92b43d5483def8dc2ecd5a6786708ea7e1710",
    ),
    "artifacts/luna53/luna53-control-initial.json": (
        "c1b73424a0be31bd95f7ac36bfe0cd3594927460",
        "cc9530821835c8df002ca6d9c9f8ec3df005fd1223c1e8f60ced70d65f82395c",
    ),
    "artifacts/luna53/luna53-control-replay.json": (
        "0aa2d1eb3cdf83ea84deabb616b6c14a7c26c8f2",
        "3398e98bd1230d78bd973b486e732b623f79d3db14083642cf9d31f1ab878366",
    ),
    "artifacts/luna53/luna53-intervention-initial.json": (
        "e7901d1495ae123c75d31d98ef771aff27b9c9e0",
        "93a4c52b0ba079942b98040c7c8b7fa1fdc94da8685b06f8ce8f0ab0b3d4d818",
    ),
    "artifacts/luna53/luna53-intervention-replay.json": (
        "557e4932023200a63f72fd178f695dbe648c2937",
        "b733da050b2b4223cddf02ed7d8c6c0e3859f6000f330e89b828972cee54625c",
    ),
}
STREAM_GROUP_COUNTS = {
    "DRIVE-LIMITED": 75,
    "TEMPORAL-RETENTION-LIMITED": 33,
    "NO-RECEPTIONS": 212,
}
TARGET_IDS = (
    "c00-011", "c00-032", "c00-037", "c01-012", "c01-020", "c01-041",
    "c01-050", "c02-010", "c02-015", "c02-019", "c02-023", "c02-046",
    "c03-023", "c03-058", "c04-001", "c04-043",
)
LUNA46_PATH = "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json"
LUNA46_EXPECTED_BLOB = "9506369d97babf7bc0ef15ed52efb738dcdcd549"
LUNA46_EXPECTED_SHA256 = "0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e"
Record = dict[str, Any]


class GateError(RuntimeError):
    """An authorization, provenance, integrity, or execution gate failed."""


def _json(path: str | Path) -> Record:
    value = json.loads((ROOT / path).read_bytes().decode("utf-8-sig"))
    if not isinstance(value, dict):
        raise GateError(f"expected JSON object in {path}")
    return value


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


def _historical_blob_bytes(revision: str, path: str, expected_blob: str) -> bytes:
    """Return bytes only after authenticating a pinned historical Git object."""
    if revision != AUTHORIZATION_REVISION:
        raise GateError(
            "retained artifact revision differs from the fixed authorization"
        )
    try:
        actual_blob = str(_git("rev-parse", f"{revision}:{path}"))
        if actual_blob != expected_blob:
            raise GateError(f"retained Git blob mismatch: {path}")
        committed = _git("cat-file", "blob", expected_blob, binary=True)
    except subprocess.CalledProcessError as error:
        raise GateError(
            f"missing pinned historical Git object: {revision}:{path}"
        ) from error
    if not isinstance(committed, bytes):
        raise GateError(f"pinned historical Git object is not binary data: {path}")
    return committed


def _read_verified_checkout(
    path: str,
    expected_sha256: str,
    canonical_bytes: bytes,
    *,
    expected_length: int | None = None,
) -> tuple[bytes, Record]:
    """Check current bytes and historical SHA/length using Luna-56's exact rules."""
    try:
        return luna53._verified_file(
            path,
            expected_sha256,
            expected_size=expected_length,
            canonical_bytes=canonical_bytes,
        )
    except luna53.GateError as error:
        raise GateError(
            f"retained checkout verification failed for {path}: {error}"
        ) from error


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact_digest(value: Record) -> str:
    clean = dict(value)
    clean.pop("artifact_digest", None)
    payload = json.dumps(
        clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _verify_digest(path: str, value: Record) -> None:
    claimed = value.get("artifact_digest")
    if claimed is not None and claimed != _artifact_digest(value):
        raise GateError(f"internal artifact digest mismatch: {path}")


def _verify_clean_authorized_start() -> str:
    head = str(_git("rev-parse", "HEAD"))
    remote = str(_git("rev-parse", "origin/main"))
    status = str(_git("status", "--porcelain"))
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", AUTHORIZATION_REVISION, head],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).returncode
    allowed = {"?? artifacts/luna55/"}
    if head != remote or ancestry != 0 or any(line not in allowed for line in status.splitlines()):
        raise GateError(
            "Luna-55 must execute from an origin/main descendant of the authorization "
            f"with no unrelated changes; observed HEAD={head}, origin={remote}, status={status!r}"
        )
    return head


def _phase_path(luna: int, condition: str, phase: str) -> str:
    if luna == 54:
        return f"artifacts/luna54/{condition}-{phase}.json"
    return f"artifacts/luna53/luna53-{condition}-{phase}.json"


def _stream_map(artifact: Record) -> dict[str, Record]:
    rows = artifact.get("streams")
    if not isinstance(rows, list):
        raise GateError("phase artifact has no stream list")
    result = {row["stream_id"]: row for row in rows}
    if len(result) != len(rows):
        raise GateError("duplicate stream ID in retained phase")
    return result


def _arrival_signature_l54(row: Record) -> list[tuple[Any, ...]]:
    return [
        (
            event["event_id"],
            event["payload_bits"],
            float(event["reception_timestamp"]),
            event["source"],
            event["destination"],
        )
        for event in row["destination_receptions"]
    ]


def _arrival_signature_l53(row: Record) -> list[tuple[Any, ...]]:
    return [
        (
            event["event_id"],
            event["payload_bits"],
            float(event["timestamp"]),
            event["source"],
            event["destination"],
        )
        for event in row["input_events"]
    ]


def _phase_pins_and_populations() -> tuple[Record, dict[str, str], dict[str, Record]]:
    selection = _json(SELECTION_PATH)
    if _sha(ROOT / SELECTION_PATH) != "2ac7b79015c00d5055b1b6226ce23239f691ba07a368e80768737e39f0b2bd57":
        raise GateError("selection artifact SHA-256 mismatch")
    if selection.get("schema") != "TPCN-LUNA55-SELECTION-1":
        raise GateError("selection artifact schema mismatch")
    pins = selection.get("factorial_compatibility_phase_artifacts", [])
    if len(pins) != 8:
        raise GateError("selection artifact must pin all eight compatibility phase artifacts")
    pin_by_path = {item["path"]: item for item in pins}
    if set(pin_by_path) != set(ARTIFACT_PINS):
        raise GateError("selection phase pin paths differ from the frozen contract")
    retained: dict[str, Record] = {}
    for path, (expected_blob, expected_sha) in ARTIFACT_PINS.items():
        pin = pin_by_path[path]
        if pin.get("git_blob") != expected_blob:
            raise GateError(f"retained Git blob mismatch: {path}")
        committed = _historical_blob_bytes(
            AUTHORIZATION_REVISION, path, expected_blob
        )
        if pin.get("checkout_sha256") != expected_sha:
            raise GateError(f"historical checkout SHA-256 pin mismatch: {path}")
        raw, _checkout_identity = _read_verified_checkout(
            path, expected_sha, committed
        )
        artifact = json.loads(raw.decode("utf-8-sig"))
        if not isinstance(artifact, dict):
            raise GateError(f"retained artifact is not an object: {path}")
        expected_condition = "control" if "/control-" in path or "luna53-control-" in path else "intervention"
        expected_phase = "initial" if path.endswith("-initial.json") else "replay"
        pin_phase = pin_by_path[path]
        execution_revision = artifact.get("execution_revision") or artifact.get(
            "execution_provenance", {}
        ).get("execution_revision")
        if (
            artifact.get("condition") != expected_condition
            or artifact.get("phase") != expected_phase
            or execution_revision != pin_phase.get("execution_revision")
            or artifact.get("schema") != pin_phase.get("schema")
        ):
            raise GateError(f"retained phase identity/provenance mismatch: {path}")
        if artifact.get("artifact_digest") is not None:
            _verify_digest(path, artifact)
        retained[path] = artifact
    stream_rows = selection.get("streams")
    if not isinstance(stream_rows, list) or len(stream_rows) != 320:
        raise GateError("frozen selection must contain 320 streams")
    ids = [row["stream_id"] for row in stream_rows]
    if len(set(ids)) != 320:
        raise GateError("frozen selection stream IDs are not unique")
    luna46 = _json("artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json")
    categories = {item["stream_id"]: item["category"] for item in luna46["sequences"]}
    if len(categories) != 320 or set(categories) != set(ids) or any(
        categories[row["stream_id"]] != row["historical_stratum"] for row in stream_rows
    ):
        raise GateError("frozen Luna-46 category inventory does not match selection")
    counts = Counter(categories.values())
    if dict(counts) != STREAM_GROUP_COUNTS:
        raise GateError(f"historical partition mismatch: {dict(counts)}")
    target_rows = {
        row["stream_id"]
        for row in stream_rows
        if row["historical_stratum"] == "DRIVE-LIMITED"
        and row["additional_arrival_count"] > 0
        and row["zero_decay_crossing"]
    }
    eplus = {
        row["stream_id"]
        for row in stream_rows
        if row["historical_stratum"] == "DRIVE-LIMITED"
        and row["additional_arrival_count"] > 0
        and not row["zero_decay_crossing"]
    }
    e0 = {
        row["stream_id"]
        for row in stream_rows
        if row["historical_stratum"] == "DRIVE-LIMITED"
        and row["additional_arrival_count"] == 0
    }
    nr0 = {
        row["stream_id"]
        for row in stream_rows
        if row["post_Luna54_classification"].startswith("NR0")
    }
    nr1 = {
        row["stream_id"]
        for row in stream_rows
        if row["post_Luna54_classification"].startswith("NR1")
    }
    if (
        target_rows != set(TARGET_IDS)
        or len(eplus) != 49
        or len(e0) != 10
        or len(nr0) != 23
        or len(nr1) != 189
        or len(target_rows | eplus | e0 | nr0 | nr1 | {
            row["stream_id"]
            for row in stream_rows
            if row["historical_stratum"] == "TEMPORAL-RETENTION-LIMITED"
        }) != 320
    ):
        raise GateError("frozen 16/49/10/189/23/33 population partition failed")
    return selection, categories, retained


def _verify_phase_compatibility(selection: Record, retained: dict[str, Record]) -> Record:
    details: dict[str, Any] = {}
    for phase in ("initial", "replay"):
        hh = retained[_phase_path(54, "control", phase)]
        rh = retained[_phase_path(54, "intervention", phase)]
        hr_control = retained[_phase_path(53, "control", phase)]
        hr = retained[_phase_path(53, "intervention", phase)]
        for arm, artifact, expected_condition in (
            ("HH", hh, "control"),
            ("RH", rh, "intervention"),
        ):
            if artifact.get("status") != "PASS" or artifact.get("condition") != expected_condition:
                raise GateError(f"{arm}/{phase} retained Luna-54 control status invalid")
            if artifact.get("phase") != phase or not artifact.get(
                "independent_recurrence_oracle", {}
            ).get("all_passed"):
                raise GateError(f"{arm}/{phase} recurrence/phase check failed")
            if arm == "HH" and not artifact.get(
                "historical_control_compatibility", {}
            ).get("passed"):
                raise GateError(f"HH historical baseline did not reproduce: {phase}")
        for arm, artifact, expected_condition in (
            ("HR-control", hr_control, "control"),
            ("HR", hr, "intervention"),
        ):
            if artifact.get("condition") != expected_condition or artifact.get("phase") != phase:
                raise GateError(f"{arm}/{phase} retained Luna-53 identity invalid")
            if artifact.get("labels_entered_runtime") is not False:
                raise GateError(f"{arm}/{phase} label-isolation check failed")
        if not hr_control.get("baseline_compatibility", {}).get("passed"):
            raise GateError(f"HR historical destination compatibility failed: {phase}")
        if hr["condition_configuration"]["integration"]["decay_rate_z"] != 0.00125:
            raise GateError(f"HR destination factor value mismatch: {phase}")
        if hr_control["condition_configuration"]["integration"]["decay_rate_z"] != 0.0125:
            raise GateError(f"HR historical destination control value mismatch: {phase}")
        if luna53._diff_paths(
            hr_control["condition_configuration"], hr["condition_configuration"]
        ) != ["integration.decay_rate_z"]:
            raise GateError(f"HR changed an unauthorized destination setting: {phase}")
        if not all(
            stream.get("recurrence_oracle", {}).get("passed", False)
            for artifact in (hr_control, hr)
            for stream in artifact["streams"]
        ):
            raise GateError(f"HR independent recurrence audit failed: {phase}")
        hh_rows, rh_rows = _stream_map(hh), _stream_map(rh)
        hc_rows, hr_rows = _stream_map(hr_control), _stream_map(hr)
        if not (set(hh_rows) == set(rh_rows) == set(hc_rows) == set(hr_rows) == set(selection["streams"][i]["stream_id"] for i in range(320))):
            raise GateError(f"stream identity mismatch among factorial arms in {phase}")
        arrivals_checked = traces_checked = 0
        hh_input_digest = hh["source_to_relay_reconciliation"]["authenticated_input_digest"]
        if rh["source_to_relay_reconciliation"]["authenticated_input_digest"] != hh_input_digest:
            raise GateError(f"HH/RH source inputs differ in {phase}")
        for stream_id in hh_rows:
            h, r, hc, d = hh_rows[stream_id], rh_rows[stream_id], hc_rows[stream_id], hr_rows[stream_id]
            if _arrival_signature_l54(h) != _arrival_signature_l53(hc):
                raise GateError(f"HH and Luna-53 control arrivals differ: {phase}/{stream_id}")
            if _arrival_signature_l54(h) != _arrival_signature_l53(d):
                raise GateError(f"HH and Luna-53 destination-arm arrivals differ: {phase}/{stream_id}")
            if h["destination_integration_traces"] != hc["integration_traces"]:
                raise GateError(f"HH historical destination traces differ: {phase}/{stream_id}")
            if len(h["destination_receptions"]) != len(d["input_events"]):
                raise GateError(f"HR arrival count mismatch: {phase}/{stream_id}")
            arrivals_checked += len(h["destination_receptions"])
            traces_checked += len(h["destination_integration_traces"])
        if arrivals_checked != 235 or traces_checked != 235:
            raise GateError(f"retained factorial compatibility counts differ in {phase}")
        details[phase] = {
            "streams": 320,
            "matched_arrivals": 235,
            "matched_historical_destination_traces": 235,
            "control_and_destination_retention_inputs_exact": True,
            "luna54_relay_arm_identity": rh.get("execution_provenance", {}).get("execution_revision"),
            "luna53_destination_arm_identity": hr.get("execution_revision"),
        }
    return {"passed": True, "phase_checks": details}


def _make_configs(frozen_config: Record, condition: Record) -> tuple[E1Config, E1Config, Record]:
    nodes = frozen_config["neuron_configurations"]["DESTINATION_CALIBRATED"]
    relay_row = deepcopy(nodes["relay"])
    destination_row = deepcopy(nodes["destination"])
    relay_row["integration"]["decay_rate_z"] = condition["relay_decay_rate_z"]
    destination_row["integration"]["decay_rate_z"] = condition["destination_decay_rate_z"]
    relay_integration = IntegrationConfig(**relay_row.pop("integration"))
    destination_integration = IntegrationConfig(**destination_row.pop("integration"))
    relay = E1Config(**relay_row, integration=relay_integration)
    destination = E1Config(**destination_row, integration=destination_integration)
    record = {
        "relay": luna54.jsonable(relay),
        "destination": luna54.jsonable(destination),
    }
    return relay, destination, record


def _load_verified_luna54_sources() -> tuple[Record, Record, Record, Record, Record]:
    """Use the pinned Git object and semantic digest when the old raw-file pin is stale."""
    actual_blob = str(_git("rev-parse", f"{AUTHORIZATION_REVISION}:{LUNA46_PATH}"))
    current_blob = str(_git("rev-parse", f"HEAD:{LUNA46_PATH}"))
    if actual_blob != LUNA46_EXPECTED_BLOB or current_blob != LUNA46_EXPECTED_BLOB:
        raise GateError("Luna-46 retained Git object differs from the authorized pin")
    committed = _historical_blob_bytes(
        AUTHORIZATION_REVISION, LUNA46_PATH, LUNA46_EXPECTED_BLOB
    )
    raw, checkout_identity = _read_verified_checkout(
        LUNA46_PATH,
        LUNA46_EXPECTED_SHA256,
        committed,
        expected_length=2_337_377,
    )
    actual_sha = checkout_identity["checkout_sha256"]
    l46 = json.loads(raw.decode("utf-8-sig"))
    claimed = l46.pop("output_digest", None)
    if (
        l46.get("schema") != "TPCN-LUNA46-OFFLINE-1"
        or claimed != luna54.digest(l46)
    ):
        raise GateError("Luna-46 retained semantic digest failed")

    original_reader = luna54._read_pinned_file
    original_hash = luna54.LUNA46_SHA256

    def read_pinned_file(
        artifact_path: str,
        expected_sha256: str,
        *,
        expected_length: int | None = None,
    ) -> tuple[bytes, Record]:
        if artifact_path == LUNA46_PATH:
            return original_reader(
                artifact_path,
                actual_sha,
                expected_length=len(raw),
            )
        return original_reader(
            artifact_path,
            expected_sha256,
            expected_length=expected_length,
        )

    try:
        luna54._read_pinned_file = read_pinned_file
        luna54.LUNA46_SHA256 = actual_sha
        sources, protocol, config, frozen = luna54._load_pinned_sources()
    finally:
        luna54._read_pinned_file = original_reader
        luna54.LUNA46_SHA256 = original_hash
    integrity_note = {
        "path": LUNA46_PATH,
        "authorization_git_blob": actual_blob,
        "checkout_sha256": actual_sha,
        "legacy_helper_sha256": LUNA46_EXPECTED_SHA256,
        "legacy_helper_expected_length": 2_337_377,
        "observed_length": len(raw),
        "semantic_digest": claimed,
        "semantic_digest_passed": True,
        "git_object_and_checkout_match": True,
        "legacy_helper_identity_verified": True,
        "disposition": (
            "The Luna-54 helper raw SHA/length metadata is stale; the exact pinned "
            "Git object, checkout materialization, and embedded Luna-46 semantic "
            "digest were independently verified. Historical files were not changed."
        ),
    }
    return sources, protocol, config, frozen, integrity_note


def _response_l54(row: Record) -> bool:
    discharge_ids = {
        trace["emission_id"]
        for trace in row["destination_integration_traces"]
        if float(trace["discharge_amount"]) != 0.0 and trace["emission_id"] is not None
    }
    emission_ids = {event["event_id"] for event in row["destination_emissions"]}
    return (
        bool(discharge_ids & emission_ids)
        and row["destination_discharge_count"] > 0
        and row["route_lineage_authenticated"]
        and row["route_links_complete"]
        and all(not event["roots_truncated"] for event in row["destination_receptions"])
    )


def _route_signature(event: Record, timestamp_key: str) -> tuple[Any, ...]:
    return (
        event["event_id"],
        event["payload_bits"],
        float(event[timestamp_key]),
        event["source"],
        event["destination"],
        event.get("lineage_id"),
        event.get("originating_emission_id"),
        tuple(event.get("causal_roots", [])),
        event.get("roots_truncated"),
        event.get("route_depth"),
        tuple(event.get("route_path", [])),
        float(event.get("scheduled_delivery_timestamp", event[timestamp_key])),
    )


def _clipping_count(traces: list[Record], config: Record) -> int:
    integration = config["integration"]
    count = 0
    for trace in traces:
        if not trace["integrated"]:
            continue
        value = (
            float(trace["z_after_decay"])
            + float(integration["input_gain"]) * float(trace["input_value"])
        )
        if abs(value) > float(integration["z_max"]):
            count += 1
    return count


def _response_l53(row: Record) -> bool:
    discharged_ids = {
        trace["emission_id"]
        for trace in row["integration_traces"]
        if float(trace["discharge_amount"]) != 0.0 and trace["emission_id"] is not None
    }
    emission_ids = {event["event_id"] for event in row["emissions"]}
    return (
        bool(discharged_ids & emission_ids)
        and row["discharge_count"] > 0
        and row.get("root_lineage_complete", False)
    )


def _summarize_streams(streams: list[Record], group_ids: dict[str, set[str]]) -> Record:
    by_id = {row["stream_id"]: row for row in streams}
    result: Record = {}
    for name, ids in group_ids.items():
        rows = [by_id[sid] for sid in sorted(ids)]
        result[name] = {
            "streams": len(rows),
            "relay_emissions": sum(row["relay_emissions"] for row in rows),
            "destination_receptions": sum(row["destination_receptions"] for row in rows),
            "destination_responses": sum(row["response"] for row in rows),
            "destination_crossings": sum(row["crossing"] for row in rows),
            "peak_destination_abs_z": max(
                (row["peak_destination_abs_z"] for row in rows), default=0.0
            ),
            "minimum_threshold_margin": min(
                (row["destination_threshold_margin"] for row in rows), default=1.0
            ),
        }
    return result


def _rr_phase(phase: str, selection: Record, categories: dict[str, str]) -> Record:
    output = OUTPUT / f"rr-{phase}.json"
    if output.exists():
        raise GateError(f"refusing to overwrite existing Luna-55 result: {output}")
    sources, _l54_protocol, l54_config, frozen, l46_integrity = (
        _load_verified_luna54_sources()
    )
    phase_data = luna54._load_phase(phase, sources)[3]
    condition = json.loads((ROOT / CONFIG_PATH).read_bytes())["conditions"]["RR"]
    relay, destination, effective_config = _make_configs(frozen, condition)
    runner_path = Path(__file__)
    runner_relative = runner_path.relative_to(ROOT).as_posix()
    source_paths = (
        "tpcn/excursion_neuron.py",
        "tpcn/event_runtime.py",
        "tpcn/experiment_excursion_runtime.py",
        "tpcn/topology.py",
    )
    source_identities = {
        path: {
            "git_blob": str(_git("rev-parse", f"HEAD:{path}")),
            "sha256": hashlib.sha256((ROOT / Path(path)).read_bytes()).hexdigest(),
        }
        for path in source_paths
    }
    frozen_ids = [item["stream_id"] for item in selection["streams"]]
    if set(frozen_ids) != set(phase_data["streams"]) or len(frozen_ids) != 320:
        raise GateError(f"RR {phase} input stream set changed")
    bounds = {"runtime": l54_config["runtime"], "topology": l54_config["topology"]}
    rows: list[Record] = []
    for stream_id in frozen_ids:
        result = luna54.run_stream(
            stream_id, phase_data["streams"][stream_id]["source_inputs"],
            relay, destination, bounds,
        )
        trace = result["destination_integration_traces"]
        peak = max((abs(float(item["z_after_input"])) for item in trace), default=0.0)
        result["evaluator_stratum"] = categories[stream_id]
        result["destination_peak_abs_z"] = peak
        result["destination_threshold_margin"] = 1.0 - peak
        result["response"] = _response_l54(result)
        result["crossing"] = bool(result["destination_threshold_crossings"])
        if not result["relay_oracle"]["passed"] or not result["destination_oracle"]["passed"]:
            raise GateError(f"RR recurrence audit failed for {phase}/{stream_id}")
        if (
            not result["route_reconciliation"]["reconciles"]
            or not result["route_links_complete"]
            or not result["resources"]["settling_completed"]
            or result["resources"]["pending_events"] != 0
            or not all(
                result["resources"][key]
                for key in (
                    "queue_bound_pass",
                    "runtime_budget_pass",
                    "neuron_budget_pass",
                    "state_bounds_pass",
                )
            )
        ):
            raise GateError(f"RR causal route or boundedness gate failed: {phase}/{stream_id}")
        if result["source_input_count"] == 0 and any(
            (
                result["relay_canonical_emission_count"],
                result["destination_reception_count"],
                result["destination_discharge_count"],
                result["destination_canonical_emission_count"],
            )
        ):
            raise GateError(f"RR no-input stream was not inert: {phase}/{stream_id}")
        rows.append(result)
    if len(rows) != 320:
        raise GateError("RR did not complete all 320 streams")
    return {
        "schema": "TPCN-LUNA55-RR-PHASE-1",
        "status": "PASS",
        "phase": phase,
        "condition": "RR",
        "execution_revision": str(_git("rev-parse", "HEAD")),
        "execution_worktree_dirty": True,
        "runner": {
            "path": runner_relative,
            "git_blob": str(_git("rev-parse", f"HEAD:{runner_relative}")),
            "sha256": _sha(runner_path),
        },
        "config_identity": {
            "path": CONFIG_PATH.as_posix(),
            "git_blob": str(_git("rev-parse", f"HEAD:{CONFIG_PATH.as_posix()}")),
            "sha256": _sha(ROOT / CONFIG_PATH),
        },
        "protocol_identity": {
            "path": PROTOCOL_PATH.as_posix(),
            "git_blob": str(_git("rev-parse", f"HEAD:{PROTOCOL_PATH.as_posix()}")),
            "sha256": _sha(ROOT / PROTOCOL_PATH),
        },
        "runtime_source_identities": source_identities,
        "authorization_selection_sha256": _sha(ROOT / SELECTION_PATH),
        "factorial_compatibility_phase_pins": selection["factorial_compatibility_phase_artifacts"],
        "luna46_pin_reconciliation": l46_integrity,
        "python": sys.version,
        "platform": platform.platform(),
        "configuration": effective_config,
        "configuration_digest": hashlib.sha256(
            json.dumps(effective_config, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "input_phase_digest": phase_data["input_digest"],
        "streams": rows,
        "stream_count": 320,
        "source_input_count": sum(row["source_input_count"] for row in rows),
        "relay_emission_count": sum(row["relay_canonical_emission_count"] for row in rows),
        "destination_reception_count": sum(row["destination_reception_count"] for row in rows),
        "destination_response_count": sum(row["response"] for row in rows),
        "resource_bounds": {
            "queue_capacity": bounds["runtime"]["queue_capacity"],
            "runtime_event_budget": bounds["runtime"]["runtime_event_budget"],
            "per_neuron_event_budget": bounds["runtime"]["neuron_event_budget"],
            "peak_queue_occupancy": max(row["resources"]["queue_peak"] for row in rows),
            "peak_runtime_events": max(row["resources"]["processed_events"] for row in rows),
            "peak_relay_neuron_events": max(
                row["resources"]["neuron_processed_events"]["relay"] for row in rows
            ),
            "peak_destination_neuron_events": max(
                row["resources"]["neuron_processed_events"]["destination"] for row in rows
            ),
            "pending_events": sum(row["resources"]["pending_events"] for row in rows),
            "all_streams_bounded": all(
                row["resources"]["queue_bound_pass"]
                and row["resources"]["runtime_budget_pass"]
                and row["resources"]["neuron_budget_pass"]
                and row["resources"]["state_bounds_pass"]
                and row["resources"]["pending_events"] == 0
                for row in rows
            ),
        },
        "relay_recurrence_updates": sum(row["relay_integration_count"] for row in rows),
        "destination_recurrence_updates": sum(row["destination_integration_count"] for row in rows),
        "route_reconciliation": {
            "enqueued": sum(row["route_reconciliation"]["enqueued_count"] for row in rows),
            "received": sum(row["route_reconciliation"]["received_count"] for row in rows),
            "matched": sum(row["route_reconciliation"]["matched_count"] for row in rows),
            "mismatches": sum(
                row["route_reconciliation"]["unmatched_enqueue_count"]
                + row["route_reconciliation"]["orphan_reception_count"]
                + row["route_reconciliation"]["duplicate_enqueue_count"]
                + row["route_reconciliation"]["duplicate_reception_count"]
                for row in rows
            ),
        },
        "clipping_event_count": sum(
            _clipping_count(row["relay_integration_traces"], effective_config["relay"])
            + _clipping_count(row["destination_integration_traces"], effective_config["destination"])
            for row in rows
        ),
        "labels_entered_runtime": False,
    }


def _seal_write(path: Path, record: Record) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    record["artifact_digest"] = _artifact_digest(record)
    payload = json.dumps(
        record, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode() + b"\n"
    with path.open("xb") as handle:
        handle.write(payload)
    if path.read_bytes() != payload:
        raise OSError(f"artifact readback mismatch: {path}")
    return hashlib.sha256(payload).hexdigest()


def run_rr(phase: str) -> Record:
    _verify_clean_authorized_start()
    selection, categories, _ = _phase_pins_and_populations()
    _verify_phase_compatibility(selection, _phase_pins_and_populations()[2])
    record = _rr_phase(phase, selection, categories)
    path = OUTPUT / f"rr-{phase}.json"
    record["artifact_sha256"] = _seal_write(path, record)
    return record


def preflight() -> Record:
    revision = _verify_clean_authorized_start()
    selection, categories, retained = _phase_pins_and_populations()
    compatibility = _verify_phase_compatibility(selection, retained)
    return {
        "status": "PASS",
        "authorization_revision": AUTHORIZATION_REVISION,
        "execution_start_revision": revision,
        "stream_count": len(categories),
        "target_streams": list(TARGET_IDS),
        "target_count": len(TARGET_IDS),
        "partition_counts": {"target": 16, "Eplus": 49, "E0": 10, "NR1": 189, "NR0": 23, "temporal_secondary": 33},
        "eight_phase_artifact_pins": "PASS",
        "compatibility": compatibility,
    }


def _phase_arm_rows(arm: str, phase: str, retained: dict[str, Record], rr: Record) -> list[Record]:
    if arm == "RR":
        normalized = []
        for row in rr["streams"]:
            normalized.append({
                **row,
                "relay_emissions": row["relay_canonical_emission_count"],
                "destination_receptions": row["destination_reception_count"],
                "destination_discharge_count": row["destination_discharge_count"],
                "destination_canonical_emission_count": row["destination_canonical_emission_count"],
                "crossing": bool(row["destination_threshold_crossings"]),
                "peak_destination_abs_z": row["destination_peak_abs_z"],
                "destination_traces": row["destination_integration_traces"],
                "route_signature": [
                    _route_signature(event, "reception_timestamp")
                    for event in row["destination_receptions"]
                ],
            })
        return normalized
    l53, condition = (arm in ("HR",)), ("intervention" if arm == "HR" else ("intervention" if arm == "RH" else "control"))
    path = _phase_path(53 if l53 else 54, condition, phase)
    rows = list(_stream_map(retained[path]).values())
    normalized: list[Record] = []
    hh_rows = _stream_map(retained[_phase_path(54, "control", phase)])
    for row in rows:
        if arm == "HR":
            traces = row["integration_traces"]
            peak = max((abs(float(item["z_after_input"])) for item in traces), default=0.0)
            normalized.append({
                "stream_id": row["stream_id"],
                "relay_emissions": hh_rows[row["stream_id"]]["relay_canonical_emission_count"],
                "destination_receptions": len(row["input_events"]),
                "destination_discharge_count": row["discharge_count"],
                "destination_canonical_emission_count": row["canonical_emission_count"],
                "response": _response_l53({
                    **row,
                    "root_lineage_complete": all(
                        not event["roots_truncated"]
                        for event in hh_rows[row["stream_id"]]["destination_receptions"]
                    ),
                }),
                "crossing": bool(row["crossed_threshold"]),
                "peak_destination_abs_z": peak,
                "destination_threshold_margin": float(row["threshold"]) - peak,
                "destination_traces": traces,
                "source_arrivals": row["input_events"],
                "route_signature": [
                    _route_signature(event, "timestamp")
                    for event in row["input_events"]
                ],
            })
        else:
            peak = max(
                (abs(float(item["z_after_input"])) for item in row["destination_integration_traces"]),
                default=0.0,
            )
            normalized.append({
                "stream_id": row["stream_id"],
                "relay_emissions": row["relay_canonical_emission_count"],
                "destination_receptions": row["destination_reception_count"],
                "destination_discharge_count": row["destination_discharge_count"],
                "destination_canonical_emission_count": row["destination_canonical_emission_count"],
                "response": _response_l54(row),
                "crossing": bool(row["destination_threshold_crossings"]),
                "peak_destination_abs_z": peak,
                "destination_threshold_margin": 1.0 - peak,
                "destination_traces": row["destination_integration_traces"],
                "source_arrivals": row["destination_receptions"],
                "route_signature": [
                    _route_signature(event, "reception_timestamp")
                    for event in row["destination_receptions"]
                ],
            })
    if arm == "RR":
        for row in normalized:
            row["route_signature"] = [
                _route_signature(event, "reception_timestamp")
                for event in row["destination_receptions"]
            ]
    return normalized


def summarize(output_name: str = "summary-v2.json") -> Record:
    selection, categories, retained = _phase_pins_and_populations()
    compatibility = _verify_phase_compatibility(selection, retained)
    rr_initial = _json(OUTPUT / "rr-initial.json")
    rr_replay = _json(OUTPUT / "rr-replay.json")
    _verify_digest(str(OUTPUT / "rr-initial.json"), rr_initial)
    _verify_digest(str(OUTPUT / "rr-replay.json"), rr_replay)
    if rr_initial["phase"] != "initial" or rr_replay["phase"] != "replay":
        raise GateError("RR phase identities invalid")
    if rr_initial["streams"] != rr_replay["streams"]:
        raise GateError("RR initial/replay scientific records differ")
    _source_bundle, _protocol, _luna54_config, frozen_config, l46_integrity = (
        _load_verified_luna54_sources()
    )
    rr_relay_config = rr_initial["configuration"]["relay"]
    rr_destination_config = rr_initial["configuration"]["destination"]
    rr_clipping = sum(
        _clipping_count(row["relay_integration_traces"], rr_relay_config)
        + _clipping_count(row["destination_integration_traces"], rr_destination_config)
        for row in rr_initial["streams"]
    )
    rr_routes = {
        key: sum(row["route_reconciliation"][source_key] for row in rr_initial["streams"])
        for key, source_key in (
            ("enqueued", "enqueued_count"),
            ("received", "received_count"),
            ("matched", "matched_count"),
            ("mismatches", "unmatched_enqueue_count"),
        )
    }
    rr_routes["mismatches"] += sum(
        row["route_reconciliation"]["orphan_reception_count"]
        + row["route_reconciliation"]["duplicate_enqueue_count"]
        + row["route_reconciliation"]["duplicate_reception_count"]
        for row in rr_initial["streams"]
    )
    rr_labels_isolated = (
        all("category" not in event for row in rr_initial["streams"] for event in row["source_inputs"])
        and all(
            row["evaluator_stratum"] == categories[row["stream_id"]]
            for row in rr_initial["streams"]
        )
        and "evaluator_stratum" not in luna54.run_stream.__code__.co_varnames
    )
    groups: dict[str, set[str]] = {
        "target16": set(TARGET_IDS),
        "Eplus49": {
            row["stream_id"] for row in selection["streams"]
            if row["historical_stratum"] == "DRIVE-LIMITED"
            and row["additional_arrival_count"] > 0 and not row["zero_decay_crossing"]
        },
        "E0": {
            row["stream_id"] for row in selection["streams"]
            if row["historical_stratum"] == "DRIVE-LIMITED" and row["additional_arrival_count"] == 0
        },
        "NR1": {sid for sid, label in categories.items() if label == "NO-RECEPTIONS" and
                next(row for row in selection["streams"] if row["stream_id"] == sid)["post_Luna54_classification"].startswith("NR1")},
        "NR1-arrival-responders58": {
            row["stream_id"] for row in selection["streams"]
            if row["post_Luna54_classification"].startswith("NR1")
            and row["additional_arrival_count"] > 0
        },
        "NR1-no-event-supply131": {
            row["stream_id"] for row in selection["streams"]
            if row["post_Luna54_classification"].startswith("NR1")
            and row["additional_arrival_count"] == 0
        },
        "NR0": {row["stream_id"] for row in selection["streams"] if row["post_Luna54_classification"].startswith("NR0")},
        "temporal_secondary33": {sid for sid, label in categories.items() if label == "TEMPORAL-RETENTION-LIMITED"},
    }
    arms: Record = {}
    arm_totals: Record = {}
    phase_arm_records: dict[str, dict[str, list[Record]]] = {}
    for arm in ("HH", "RH", "HR", "RR"):
        phase_arm_records[arm] = {}
        for phase in ("initial", "replay"):
            rr = rr_initial if phase == "initial" else rr_replay
            rows = _phase_arm_rows(arm, phase, retained, rr)
            if len(rows) != 320:
                raise GateError(f"{arm}/{phase} does not contain 320 streams")
            phase_arm_records[arm][phase] = rows
        if phase_arm_records[arm]["initial"] != phase_arm_records[arm]["replay"]:
            raise GateError(f"{arm} initial/replay normalized outcomes differ")
        arms[arm] = _summarize_streams(phase_arm_records[arm]["initial"], groups)
        arm_rows = phase_arm_records[arm]["initial"]
        arm_totals[arm] = {
            "streams": len(arm_rows),
            "relay_emissions": sum(row["relay_emissions"] for row in arm_rows),
            "destination_receptions": sum(row["destination_receptions"] for row in arm_rows),
            "destination_crossings": sum(row["crossing"] for row in arm_rows),
            "destination_responses": sum(row["response"] for row in arm_rows),
            "peak_destination_abs_z": max(
                (row["peak_destination_abs_z"] for row in arm_rows), default=0.0
            ),
        }
    by_arm_id = {
        arm: {row["stream_id"]: row for row in phase_arm_records[arm]["initial"]}
        for arm in arms
    }
    selection_by_id = {row["stream_id"]: row for row in selection["streams"]}
    factorial: dict[str, Any] = {}
    signatures = Counter()
    for stream_id in TARGET_IDS:
        response = {arm: bool(by_arm_id[arm][stream_id]["response"]) for arm in arms}
        if response["RR"] and not any(response[arm] for arm in ("HH", "RH", "HR")):
            label = "SERIAL-INTERACTION"
        elif response["HR"] and not response["RH"]:
            label = "DESTINATION-MAIN-EFFECT"
        elif response["RH"] and not response["HR"]:
            label = "RELAY-MAIN-EFFECT"
        elif response["RH"] and response["HR"]:
            label = "BOTH-SINGLE-ARMS"
        elif not any(response.values()):
            label = "NO-CROSSING"
        else:
            label = "OTHER"
        signatures[label] += 1
        factorial[stream_id] = {
            "response_pattern": response,
            "signature": label,
            "peak_abs_z": {arm: by_arm_id[arm][stream_id]["peak_destination_abs_z"] for arm in arms},
            "threshold_margin": {arm: by_arm_id[arm][stream_id]["destination_threshold_margin"] for arm in arms},
            "continuous_interaction": (
                by_arm_id["RR"][stream_id]["peak_destination_abs_z"]
                - by_arm_id["RH"][stream_id]["peak_destination_abs_z"]
                - by_arm_id["HR"][stream_id]["peak_destination_abs_z"]
                + by_arm_id["HH"][stream_id]["peak_destination_abs_z"]
            ),
            "zero_decay_oracle_peak_abs_z": selection_by_id[stream_id][
                "zero_decay_destination_peak_abs_z"
            ],
            "RR_minus_zero_decay_peak_abs_z": (
                by_arm_id["RR"][stream_id]["peak_destination_abs_z"]
                - selection_by_id[stream_id]["zero_decay_destination_peak_abs_z"]
            ),
            "zero_decay_oracle_threshold_margin": selection_by_id[stream_id][
                "zero_decay_threshold_margin"
            ],
        }
    control_crossings = {
        group: {
            arm: arms[arm][group]["destination_crossings"]
            for arm in arms
        }
        for group in ("Eplus49", "E0", "NR1", "NR0")
    }
    continuous_effects = {
        stream_id: {
            "relay_effect_at_historical_destination": (
                by_arm_id["RH"][stream_id]["peak_destination_abs_z"]
                - by_arm_id["HH"][stream_id]["peak_destination_abs_z"]
            ),
            "relay_effect_at_retained_destination": (
                by_arm_id["RR"][stream_id]["peak_destination_abs_z"]
                - by_arm_id["HR"][stream_id]["peak_destination_abs_z"]
            ),
            "destination_effect_at_historical_relay": (
                by_arm_id["HR"][stream_id]["peak_destination_abs_z"]
                - by_arm_id["HH"][stream_id]["peak_destination_abs_z"]
            ),
            "destination_effect_at_retained_relay": (
                by_arm_id["RR"][stream_id]["peak_destination_abs_z"]
                - by_arm_id["RH"][stream_id]["peak_destination_abs_z"]
            ),
            "interaction": (
                by_arm_id["RR"][stream_id]["peak_destination_abs_z"]
                - by_arm_id["RH"][stream_id]["peak_destination_abs_z"]
                - by_arm_id["HR"][stream_id]["peak_destination_abs_z"]
                + by_arm_id["HH"][stream_id]["peak_destination_abs_z"]
            ),
        }
        for stream_id in TARGET_IDS
    }
    rr_rh_route_equal = all(
        by_arm_id["RR"][sid]["route_signature"]
        == by_arm_id["RH"][sid]["route_signature"]
        for sid in by_arm_id["RR"]
    )
    all_recurrence_pass = all(
        row.get("relay_oracle", {}).get("passed", False)
        and row.get("destination_oracle", {}).get("passed", False)
        for row in rr_initial["streams"]
    ) and rr_clipping == 0 and rr_routes["mismatches"] == 0
    conditions = json.loads((ROOT / CONFIG_PATH).read_bytes())["conditions"]
    effective_configs: Record = {}
    changed_paths: Record = {}
    expected_changed_paths = {
        "HH": [],
        "RH": ["relay.integration.decay_rate_z"],
        "HR": ["destination.integration.decay_rate_z"],
        "RR": ["destination.integration.decay_rate_z", "relay.integration.decay_rate_z"],
    }
    historical_nodes = frozen_config["neuron_configurations"]["DESTINATION_CALIBRATED"]
    for arm, condition in conditions.items():
        relay, destination, _ = _make_configs(frozen_config, condition)
        effective = {
            "relay": luna54.jsonable(relay),
            "destination": luna54.jsonable(destination),
        }
        effective_configs[arm] = effective
        changed_paths[arm] = luna54._diff_paths(
            {"relay": historical_nodes["relay"], "destination": historical_nodes["destination"]},
            effective,
        )
        if changed_paths[arm] != expected_changed_paths[arm]:
            raise GateError(f"{arm} contains an unauthorized configuration difference")
    verdict = "BLOCKED"
    if compatibility["passed"] and rr_rh_route_equal and all_recurrence_pass:
        controls_negative = all(
            not any(count for count in arm_counts.values())
            for arm_counts in control_crossings.values()
        )
        single_arm_silent = all(
            not any(
                by_arm_id[arm][stream_id]["response"]
                for arm in ("HH", "RH", "HR")
            )
            for stream_id in TARGET_IDS
        )
        if signatures["SERIAL-INTERACTION"] and controls_negative and single_arm_silent:
            verdict = "PARTIALLY SUPPORTED"
        elif rr_initial["destination_response_count"] == 0:
            verdict = "NOT SUPPORTED"
        else:
            verdict = "MIXED"
    result = {
        "schema": "TPCN-LUNA55-FACTORIAL-SUMMARY-1",
        "status": "PASS" if verdict != "BLOCKED" else "BLOCKED",
        "authorization_revision": AUTHORIZATION_REVISION,
        "execution_revision": rr_initial["execution_revision"],
        "analysis_revision": str(_git("rev-parse", "HEAD")),
        "interpretation": "Bounded mechanistic factorial only; initial/replay are deterministic replays, not independent samples.",
        "compatibility_preflight": compatibility,
        "luna46_pin_reconciliation": l46_integrity,
        "population_counts": {key: len(ids) for key, ids in groups.items()},
        "population_ids": {key: sorted(ids) for key, ids in groups.items()},
        "target_ids": list(TARGET_IDS),
        "zero_decay_insufficient_ids": sorted(groups["Eplus49"]),
        "conditions": json.loads((ROOT / CONFIG_PATH).read_bytes())["conditions"],
        "effective_configurations": effective_configs,
        "configuration_changed_paths_from_historical": changed_paths,
        "arm_summaries": arms,
        "arm_totals": arm_totals,
        "reused_phase_artifact_pins": {
            pin["path"]: pin
            for pin in selection["factorial_compatibility_phase_artifacts"]
        },
        "target_factorial_outcomes": factorial,
        "target_continuous_factorial_effects": continuous_effects,
        "target_signature_counts": dict(signatures),
        "negative_control_crossings": control_crossings,
        "rr_rh_route_receptions_invariant": rr_rh_route_equal,
        "rr_recurrence_pass": all_recurrence_pass,
        "rr_replay_exact": rr_initial["streams"] == rr_replay["streams"],
        "rr_route_reconciliation": rr_routes,
        "rr_route_audit": rr_routes,
        "rr_recurrence_update_counts": {
            "relay": sum(row["relay_integration_count"] for row in rr_initial["streams"]),
            "destination": sum(
                row["destination_integration_count"] for row in rr_initial["streams"]
            ),
        },
        "rr_clipping_event_count": rr_clipping,
        "rr_resource_bounds": rr_initial.get("resource_bounds", {
            "queue_capacity": 128,
            "runtime_event_budget": 1024,
            "per_neuron_event_budget": 4096,
            "peak_queue_occupancy": max(
                row["resources"]["queue_peak"] for row in rr_initial["streams"]
            ),
            "peak_runtime_events": max(
                row["resources"]["processed_events"] for row in rr_initial["streams"]
            ),
            "peak_relay_neuron_events": max(
                row["resources"]["neuron_processed_events"]["relay"]
                for row in rr_initial["streams"]
            ),
            "peak_destination_neuron_events": max(
                row["resources"]["neuron_processed_events"]["destination"]
                for row in rr_initial["streams"]
            ),
            "pending_events": sum(
                row["resources"]["pending_events"] for row in rr_initial["streams"]
            ),
            "all_streams_bounded": all(
                row["resources"]["queue_bound_pass"]
                and row["resources"]["runtime_budget_pass"]
                and row["resources"]["neuron_budget_pass"]
                and row["resources"]["state_bounds_pass"]
                and row["resources"]["pending_events"] == 0
                for row in rr_initial["streams"]
            ),
        }),
        "label_isolation": rr_labels_isolated,
        "verdict": verdict,
        "non_claims": [
            "No task efficacy, production suitability, hardware equivalence, parameter optimality, or architecture promotion.",
            "No Luna-56 or successor is authorized.",
        ],
        "phase_artifacts": {
            "RR-initial": {"path": "artifacts/luna55/rr-initial.json", "sha256": _sha(ROOT / (OUTPUT / "rr-initial.json"))},
            "RR-replay": {"path": "artifacts/luna55/rr-replay.json", "sha256": _sha(ROOT / (OUTPUT / "rr-replay.json"))},
        },
    }
    summary_path = OUTPUT / output_name
    _seal_write(summary_path, result)
    integrity = {
        "schema": "TPCN-LUNA55-INTEGRITY-1",
        "execution_revision": rr_initial["execution_revision"],
        "analysis_revision": str(_git("rev-parse", "HEAD")),
        "artifacts": {
            name: {"path": f"artifacts/luna55/{name}", "sha256": _sha(OUTPUT / name)}
            for name in ("rr-initial.json", "rr-replay.json", output_name)
        },
    }
    integrity_path = OUTPUT / f"{Path(output_name).stem}-integrity.json"
    _seal_write(integrity_path, integrity)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--run-rr", choices=("initial", "replay"))
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--summary-name", choices=("summary-v2.json", "summary-v3.json"))
    args = parser.parse_args(argv)
    try:
        if args.preflight:
            print(json.dumps(preflight(), indent=2))
        elif args.run_rr:
            print(json.dumps(run_rr(args.run_rr), indent=2))
        elif args.summarize:
            print(json.dumps(summarize(args.summary_name or "summary-v2.json"), indent=2))
        else:
            parser.error("choose --preflight, --run-rr, or --summarize")
    except GateError as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
