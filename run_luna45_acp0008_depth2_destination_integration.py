"""Frozen-fixture Luna-45 execution worker; never a generator or reviewer.

Reuse Luna-44's reviewed production execution/capture driver, with an explicit
destination-only configuration adapter and additional receiver observations.
The historical namespace is held constant so canonical/queue identities remain
comparable, rather than normalizing away identity differences after execution.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any
from unittest import mock

import run_luna44_acp0008_canonical_fixture_rebaseline as reference
from tpcn.event_runtime import Event, EventQueue, EventType
from tpcn.excursion_neuron import E1Config, IntegrationConfig, MultiExcursionNeuron
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime


BASELINE = "b4536f151cb8f73a173aac225df24c8fc2259c88"
AUTHORIZATION_REVISION = "9af6b4435ac581887f04f0951d0f7b16d7d661cd"
BRANCH = "copilot/luna45-depth2-destination-integration"
HANDOFF = Path(
    "workflow/handoffs/luna-0-authorization-luna45-depth2-destination-integration-20261006.md"
)
HANDOFF_SHA256 = "c326548c8bd1b6795caca1bc2694993523c291ff1845e47b4f7e0c64dc61228e"
HANDOFF_COMMITTED_SHA256 = "498ce49dd8f32f9d971f1c893e46bdce9ea2247007e66461512e885a6e3e41d9"
REFERENCE_SOURCE_SHA256 = "782ab6474251abfbf138156e4126d590536a423c878029a270686081c7caec37"
HISTORY = Path("artifacts/luna44-acp0008-independent-routing-rerun-20261005")
HISTORY_REVISION = "4baab60f87b820db800e04d0eb3277fb0e94f9b3"
HISTORY_CONFIG_DIGEST = "942b86a9cd7a3965265ec9d01aff7e0b0e2bf68b309f0e0bd22dc4cbae71884e"
HISTORY_FILES = {
    "summary.json": "5e10242aaf3219fca81a6fab62f252fb9f5a770a1b13ce6a4eeb36ff9da35f36",
    "results.json": "16deacb459a9c6715c14fd7caa5ecf4f6910776316fb80e890a1969fa92aa6e9",
    "routing-initial-enqueue.json": "61e0040541a4ac877a833f7d7605138edb065547cb154b7a46bade4de1e7139b",
    "routing-initial-reception.json": "d1e24f6239e9f0758e3991a2416d826407a5d12adf73c5ef97762ba89861b44a",
}
ARMS = ("DESTINATION_DISABLED", "DESTINATION_DEFAULT", "DESTINATION_CALIBRATED")
ASSOCIATION_WINDOW = 4.0
OUTPUT = Path("artifacts/luna45-acp0008-depth2-destination-integration-20261006")
PUBLISHED_CONFIG = Path("artifacts/luna45-depth2-frozen-config-20261006-r2/config.json")
GIT_ENVIRONMENT = {
    "GIT_CONFIG_COUNT": "2",
    "GIT_CONFIG_KEY_0": "core.autocrlf",
    "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.eol",
    "GIT_CONFIG_VALUE_1": "lf",
}
FLOAT_FIELDS = frozenset({
    "payload", "m_peak", "x_before", "x_after", "z_before", "z_after",
    "x_before_decay", "x_after_decay", "z_before_decay", "z_after_decay",
    "x_after_input", "z_after_input", "x_post_discharge", "z_post_discharge",
    "discharge_amount", "x_at_emission", "z_at_emission",
    "scheduled_delivery_timestamp", "timestamp",
})

Record = dict[str, Any]


class Blocker(RuntimeError):
    def __init__(self, gate: str, detail: Record) -> None:
        super().__init__(f"{gate}: {detail.get('reason', 'mandatory check failed')}")
        self.gate = gate
        self.detail = detail


def digest(value: Any) -> str:
    return reference._digest(value)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def node_config(arm: str, node: str) -> E1Config:
    if arm not in ARMS or node not in reference.NODES:
        raise ValueError(f"unknown condition/node: {arm}/{node}")
    integration = None
    if node == "relay" or (node == "destination" and arm == ARMS[2]):
        integration = IntegrationConfig(decay_rate_z=0.0125)
    elif node == "destination" and arm == ARMS[1]:
        integration = IntegrationConfig()
    return E1Config(event_budget=4096, integration=integration)


def experiment_config() -> Record:
    inherited = reference.experiment_config()
    return {
        "schema": "TPCN-LUNA45-DEPTH2-1",
        "authorization_revision": AUTHORIZATION_REVISION,
        "authorization_handoff_revision": BASELINE,
        "authorization_handoff_sha256": HANDOFF_SHA256,
        "authorization_handoff_committed_sha256": HANDOFF_COMMITTED_SHA256,
        "authorization_handoff_byte_identity": "separate exact CRLF checkout and LF Git-blob pins",
        "baseline": BASELINE,
        "fixture": inherited["fixture"],
        "reference_driver_sha256": REFERENCE_SOURCE_SHA256,
        "historical_evidence": {
            "directory": HISTORY.as_posix(), "runner_revision": HISTORY_REVISION,
            "config_digest": HISTORY_CONFIG_DIGEST, "file_sha256": HISTORY_FILES,
            "arm": "CALIBRATED", "phase": "initial",
        },
        "neuron_configurations": {
            arm: {node: asdict(node_config(arm, node)) for node in reference.NODES}
            for arm in ARMS
        },
        "runtime": inherited["runtime"],
        "topology": inherited["topology"],
        "identity_namespace": "luna44-calibrated-seed-{seed}",
        "reward_message_identity": "luna44-neutral-{stream_id}",
        "only_varied_quantity": "destination.integration",
        "destination_evidence_fields": [
            "stream_id", "relay_emission_id", "queue_admission", "actual_reception",
            "reception_event_id", "payload_encoding", "arrival_timestamp",
            "x_before_decay", "x_after_decay", "x_after_update", "z_before_decay",
            "elapsed", "z_after_decay", "routed_contribution", "z_after_contribution",
            "discharge_decision", "discharge_amount", "discharge_sign",
            "resulting_z", "x_post_discharge", "classification",
            "canonical_emission_id", "oracle", "contributing_receptions",
        ],
        "structural_plasticity": False,
        "candidate_opportunity_precursors": {
            "association_window": ASSOCIATION_WINDOW,
            "endpoints": ["source", "destination"],
            "predicate": "0 < destination.timestamp - source.timestamp <= 4.0",
            "ordering": "fixture order, destination emission order, source emission order",
            "missing_edge": ["source", "destination"],
            "observational_only": True,
        },
        "numerical_policy": {
            "formula": reference.FLOAT_POLICY_FORMULA,
            "historical_float_fields": sorted(FLOAT_FIELDS),
            "historical_timestamp_exception": (
                "timestamp tolerance only on queue arrival and relay trajectory; "
                "canonical emission times, prior_clock and elapsed remain exact"
            ),
            "equation_fields": [
                "derived x+y", "ordinary emission payload", "Model-B payload",
                "arrival time", "x/z decay", "x/z input", "discharge", "post-discharge x/z",
            ],
            "exact": [
                "fixture bits/order", "identities/endpoints", "queue sequence",
                "source equality", "copied payload bits", "elapsed subtraction",
                "mode/threshold/discharge sign/classification", "hard bounds",
                "cross-arm content", "same-environment replay bits",
            ],
        },
        "gate_order": ["G1", "G2", "G3", "G4", "DESTINATION", "REPLAY"],
        "verdict_rule": "support requires genuine calibrated destination integrated emission",
        "replay": {
            "canonicalization": "sorted-key compact UTF-8 JSON; SHA-256",
            "material": [
                "fixture digests", "config", "ordered complete character records",
                "raw inputs", "source emissions", "both enqueue/reception streams",
                "relay trajectory/emissions", "destination evidence/chain",
                "per-arm report", "bounds/pending", "reconciliation counts",
            ],
            "excluded": ["wall-clock times", "PIDs", "paths", "environment strings"],
            "equality": "canonical bytes equal, including float bits",
            "initial_blocker": "no replay, initial/replay/summary digest null",
            "replay_blocker": "initial records and digest immutable; separate blocker",
        },
    }


def collect_provenance() -> Record:
    head = reference._git_output("rev-parse", "HEAD")
    runner = Path(__file__)
    problems = []
    if sys.version_info[:3] != (3, 11, 5):
        problems.append("requires Python 3.11.5")
    if {key: os.environ.get(key) for key in GIT_ENVIRONMENT} != GIT_ENVIRONMENT:
        problems.append("process-local Git LF overrides absent or changed")
    if reference._git_output("branch", "--show-current") != BRANCH:
        problems.append("wrong branch")
    if reference._git_output("status", "--porcelain", "--untracked-files=all"):
        problems.append("worktree not clean")
    if reference._git_output("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0] != head:
        problems.append("runner revision is not the exact published head")
    for revision in (BASELINE, AUTHORIZATION_REVISION, reference.FIXTURE_REVISION):
        if reference._git_output("merge-base", revision, head) != revision:
            problems.append(f"missing ancestor {revision}")
    committed = subprocess.run(
        ["git", "show", f"{head}:{runner.name}"], check=True, capture_output=True
    ).stdout
    if committed != runner.read_bytes():
        problems.append("runner bytes differ from committed runner")
    if file_hash(HANDOFF) != HANDOFF_SHA256:
        problems.append("final authorization handoff differs")
    committed_handoff = subprocess.run(
        ["git", "show", f"{BASELINE}:{HANDOFF.as_posix()}"],
        check=True, capture_output=True,
    ).stdout
    if hashlib.sha256(committed_handoff).hexdigest() != HANDOFF_COMMITTED_SHA256:
        problems.append("baseline authorization handoff differs")
    if file_hash(Path(reference.__file__)) != REFERENCE_SOURCE_SHA256:
        problems.append("reviewed execution driver differs")
    config_bytes = reference._canonical_bytes(experiment_config()) + b"\n"
    if not PUBLISHED_CONFIG.is_file() or PUBLISHED_CONFIG.read_bytes() != config_bytes:
        problems.append("published frozen configuration differs or is missing")
    committed_config = subprocess.run(
        ["git", "show", f"{head}:{PUBLISHED_CONFIG.as_posix()}"],
        check=True, capture_output=True,
    ).stdout
    if committed_config != config_bytes:
        problems.append("committed configuration differs")
    if problems:
        raise Blocker("PROVENANCE", {"reason": "; ".join(problems)})
    return {
        "baseline": BASELINE, "authorization_revision": AUTHORIZATION_REVISION,
        "authorization_handoff_revision": BASELINE,
        "authorization_handoff_sha256": HANDOFF_SHA256,
        "authorization_handoff_committed_sha256": HANDOFF_COMMITTED_SHA256,
        "runner_revision": head, "execution_revision": head,
        "runner_sha256": file_hash(runner),
        "reference_driver_sha256": REFERENCE_SOURCE_SHA256,
        "config_digest": digest(experiment_config()),
        "published_config_file_sha256": hashlib.sha256(config_bytes).hexdigest(),
        "fixture_revision": reference.FIXTURE_REVISION,
        "fixture_file_sha256": reference.FIXTURE_FILE_SHA256,
        "fixture_semantic_digest": reference.FIXTURE_SHA256,
        "fixture_manifest_revision": reference.FIXTURE_PROVENANCE_REVISION,
        "fixture_manifest_sha256": reference.FIXTURE_PROVENANCE_SHA256,
        "fixture_manifest_git_blob": reference.FIXTURE_PROVENANCE_GIT_BLOB,
        "environment": {
            "python": sys.version, "platform": platform.platform(),
            "implementation": sys.implementation.name,
            "float_info": reference._environment_record({})["float_info"],
            "git_overrides": GIT_ENVIRONMENT,
        },
    }


def load_inputs() -> tuple[Record, Record]:
    if reference.FIXTURE_PATH.stat().st_size != 3451453:
        raise Blocker("FIXTURE", {"reason": "fixture byte length differs"})
    fixture, manifest = reference.load_fixture()
    fixture_bytes = subprocess.run(
        ["git", "show", f"{reference.FIXTURE_REVISION}:{reference.FIXTURE_PATH.as_posix()}"],
        check=True, capture_output=True,
    ).stdout
    if fixture_bytes != reference.FIXTURE_PATH.read_bytes():
        raise Blocker("FIXTURE", {"reason": "fixture revision bytes differ"})
    return fixture, manifest


def load_history() -> tuple[list[Record], Record]:
    artifacts = {}
    for name, expected in HISTORY_FILES.items():
        path = HISTORY / name
        if file_hash(path) != expected:
            raise Blocker("G1", {"reason": f"historical file pin differs: {name}"})
        artifact = json.loads(path.read_bytes())
        if artifact["artifact_digest"] != reference._artifact_digest(artifact):
            raise Blocker("G1", {"reason": f"historical artifact digest differs: {name}"})
        if (
            artifact["runner_revision"] != HISTORY_REVISION
            or artifact["fixture_revision"] != reference.FIXTURE_REVISION
            or artifact["fixture_sha256"] != reference.FIXTURE_SHA256
            or artifact["config_digest"] != HISTORY_CONFIG_DIGEST
        ):
            raise Blocker("G1", {"reason": f"historical provenance differs: {name}"})
        artifacts[name] = artifact
    summary = artifacts["summary.json"]
    if summary["status"] != "PASS" or summary["verdict"] != "SUPPORTED":
        raise Blocker("G1", {"reason": "historical verdict differs"})
    records = artifacts["results.json"]["runs"]["CALIBRATED"]
    if len(records) != 320:
        raise Blocker("G1", {"reason": "historical calibrated records incomplete"})
    for index, record in enumerate(records):
        body = {key: value for key, value in record.items() if key != "record_digest"}
        if digest(body) != record["record_digest"]:
            raise Blocker("G1", {"reason": f"historical record digest differs: {index}"})
        for filename, field in (
            ("routing-initial-enqueue.json", "routing_enqueue_events"),
            ("routing-initial-reception.json", "receiver_reception_events"),
        ):
            raw = artifacts[filename]["per_arm"]["CALIBRATED"][index]
            if (
                raw["stream_id"] != record["stream_id"]
                or raw["events"] != record[field]
                or raw["stream_digest"] != digest(record[field])
            ):
                raise Blocker("G1", {"reason": f"historical actual capture differs: {index}/{field}"})
    return records, {
        "directory": HISTORY.as_posix(), "files": HISTORY_FILES,
        "arm": "CALIBRATED", "phase": "initial", "records": 320,
        "runner_revision": HISTORY_REVISION, "config_digest": HISTORY_CONFIG_DIGEST,
    }


def _state(neuron: MultiExcursionNeuron) -> Record:
    return {
        "x": float(neuron.state), "z": neuron.integration_state,
        "clock": float(neuron.clock.timestamp), "mode": neuron.mode.value,
        "processed_events": neuron.processed_event_count,
        "episode_id": neuron.ordinary_episode_id,
    }


def run_character(arm: str, sequence: Record) -> Record:
    """Additional observations delegate unchanged production methods exactly once."""
    observations: list[Record] = []
    trace_objects = []
    runtimes: list[ExcursionCharacterRuntime] = []
    original_receive = MultiExcursionNeuron.receive_event
    original_start = ExcursionCharacterRuntime.start_character
    original_reset = MultiExcursionNeuron.reset
    original_push = EventQueue.push_propagated
    original_attach = ExcursionCharacterRuntime._attach
    original_process = ExcursionCharacterRuntime._process_one
    partial_enqueue: list[Record] = []
    partial_reception: list[Record] = []
    snapshots: Record = {}
    receiver_context: Any = None

    def capture_start(runtime: ExcursionCharacterRuntime, *args: Any, **kwargs: Any) -> Any:
        runtimes.append(runtime)
        return original_start(runtime, *args, **kwargs)

    def capture_reset(neuron: MultiExcursionNeuron, *, timestamp: float = 0.0) -> None:
        snapshots[neuron.neuron_id] = {
            "state": _state(neuron),
            "emissions": [reference._emission_record(item) for item in neuron.emissions],
            "integration_trace": reference._jsonable(neuron.integration_trace),
        }
        original_reset(neuron, timestamp=timestamp)

    def capture_push(queue: EventQueue[Event], *args: Any, **kwargs: Any) -> Event:
        event = original_push(queue, *args, **kwargs)
        if event.event_type == EventType.EXCURSION:
            partial_enqueue.append({
                "event_id": event.event_id, "queue_sequence": event.sequence,
                "source": event.source, "destination": event.destination,
                "payload": float(event.payload), "payload_bits": reference._bits(event.payload),
                "payload_encoding": reference._float_record(event.payload),
                "enqueue_timestamp": float(args[0]),
                "scheduled_delivery_timestamp": float(event.timestamp),
                "lineage_id": event.lineage_id,
                "originating_emission_id": kwargs.get("event_id"),
            })
        return event

    def capture_attach(runtime: ExcursionCharacterRuntime, event: Event, context: Any) -> None:
        original_attach(runtime, event, context)
        if event.event_type == EventType.EXCURSION:
            row = next(item for item in reversed(partial_enqueue)
                       if item["queue_sequence"] == event.sequence)
            row.update(reference._jsonable(context))

    def capture_process(runtime: ExcursionCharacterRuntime, event: Event) -> None:
        nonlocal receiver_context
        previous = receiver_context
        receiver_context = runtime._sidecar.get(event.sequence)
        try:
            original_process(runtime, event)
        finally:
            receiver_context = previous

    def capture_receive(neuron: MultiExcursionNeuron, event: Event, queue: Any = None) -> Any:
        before = _state(neuron)
        result = original_receive(neuron, event, queue)
        after = _state(neuron)
        if event.event_type == EventType.EXCURSION:
            if receiver_context is None or after["processed_events"] != before["processed_events"] + 1:
                raise Blocker("G3", {"reason": "successful receiver context/counter absent"})
            partial_reception.append({
                "event_id": event.event_id, "queue_sequence": event.sequence,
                "source": event.source, "destination": event.destination,
                "receiver_node": neuron.neuron_id, "payload": float(event.payload),
                "payload_bits": reference._bits(event.payload),
                "payload_encoding": reference._float_record(event.payload),
                "reception_timestamp": after["clock"], "lineage_id": event.lineage_id,
                "originating_emission_id": event.event_id,
                **reference._jsonable(receiver_context), "before": before, "after": after,
            })
        if neuron.neuron_id == "destination":
            observations.append({
                "timestamp": float(event.timestamp), "event_id": event.event_id,
                "event_type": reference._jsonable(event.event_type),
                "payload": reference._jsonable(event.payload),
                "prior_clock": before["clock"], "mode_before": before["mode"],
                "x_before": before["x"], "z_before": before["z"],
                "x_after": after["x"], "z_after": after["z"], "mode_after": after["mode"],
                "queue_sequence": event.sequence,
                "episode_id_after": after["episode_id"],
            })
            if event.event_type == EventType.EXCURSION and neuron.config.integration is not None:
                trace_objects.append(neuron.integration_trace[-1])
        return result

    try:
        with (
            mock.patch.object(reference, "_e1_config", lambda _arm, node: node_config(arm, node)),
            mock.patch.object(MultiExcursionNeuron, "receive_event", capture_receive),
            mock.patch.object(MultiExcursionNeuron, "reset", capture_reset),
            mock.patch.object(ExcursionCharacterRuntime, "start_character", capture_start),
            mock.patch.object(ExcursionCharacterRuntime, "_attach", capture_attach),
            mock.patch.object(ExcursionCharacterRuntime, "_process_one", capture_process),
            mock.patch.object(EventQueue, "push_propagated", capture_push),
        ):
            record = reference._run_character(arm="CALIBRATED", sequence=sequence)
    except (RuntimeError, ValueError, BufferError) as error:
        partial = {
            "arm": arm, "stream_id": sequence["stream_id"], "seed": sequence["seed"],
            "sequence_index": sequence["sequence_index"], "completed": False,
            "routing_enqueue_events": partial_enqueue,
            "receiver_reception_events": partial_reception,
            "destination_state_trajectory": observations, "snapshots": snapshots,
            "exception": type(error).__name__, "reason": str(error),
        }
        if runtimes:
            runtime = runtimes[0]
            partial["runtime_processed_events"] = runtime._processed
            partial["pending_events"] = None if runtime.queue is None else len(runtime.queue)
            partial["runtime_events"] = reference._jsonable(runtime._trace)
            partial["active_states"] = {
                node: _state(neuron) for node, neuron in runtime.by_id.items()
            }
        raise Blocker("EXECUTION", partial) from error
    record.pop("record_digest")
    record["arm"] = arm
    record["destination_decay_rate_z"] = (
        None if node_config(arm, "destination").integration is None
        else node_config(arm, "destination").integration.decay_rate_z
    )
    record["destination_state_trajectory"] = observations
    record["destination_integration_trace"] = reference._jsonable(trace_objects)
    for field in ("routing_enqueue_events", "receiver_reception_events"):
        for item in record[field]:
            item["payload_encoding"] = reference._float_record(item["payload"])
    record["resource_high_water"].update({
        "prediction_expiry": 4.0, "settling_horizon": 4.0,
        "topology_fan_in_limit": 2, "topology_fan_out_limit": 2,
        "topology_edge_peak": len(runtimes[0].topology.edges),
        "topology_routing_peak": len(runtimes[0].topology.edges),
        "topology_fan_in_peak": max(Counter(edge.destination for edge in runtimes[0].topology.edges).values()),
        "topology_fan_out_peak": max(Counter(edge.source for edge in runtimes[0].topology.edges).values()),
    })
    return record


def upstream(record: Record) -> Record:
    return {
        key: record[key] for key in (
            "stream_id", "seed", "sequence_index", "fixture_sequence_sha256",
            "raw_identity", "raw_identity_sha256", "input_digest", "point_inputs",
            "input_batches", "source_emissions", "relay_state_trajectory",
            "relay_integration_trace",
        )
    } | {
        "source_to_relay_enqueue": [
            {k: v for k, v in item.items() if k != "payload_encoding"}
            for item in record["routing_enqueue_events"] if item["source"] == "source"
        ],
        "source_to_relay_reception": [
            {k: v for k, v in item.items() if k != "payload_encoding"}
            for item in record["receiver_reception_events"] if item["destination"] == "relay"
        ],
        "relay_to_destination_enqueue": [
            {k: v for k, v in item.items() if k != "payload_encoding"}
            for item in record["routing_enqueue_events"] if item["source"] == "relay"
        ],
        "relay_emissions": [
            {k: v for k, v in item.items() if k != "integration_trace_check"}
            for item in record["relay_emissions"]
        ],
    }


def compare_historical(observed: Any, expected: Any, path: str = "") -> list[Record]:
    checks = []
    if isinstance(observed, dict) and isinstance(expected, dict):
        if observed.keys() != expected.keys():
            return [{"field": path, "matches": False, "reason": "field set differs"}]
        for key in observed:
            checks.extend(compare_historical(observed[key], expected[key], f"{path}.{key}"))
    elif isinstance(observed, (list, tuple)) and isinstance(expected, (list, tuple)):
        if len(observed) != len(expected):
            return [{"field": path, "matches": False, "reason": "count differs"}]
        for index, (left, right) in enumerate(zip(observed, expected)):
            checks.extend(compare_historical(left, right, f"{path}[{index}]"))
    else:
        key = path.rsplit(".", 1)[-1]
        floating = (
            type(observed) is float and type(expected) is float and key in FLOAT_FIELDS
            and "raw_identity" not in path and "point_inputs" not in path
            and "input_batches" not in path
            and (key != "timestamp" or "enqueue" in path or "relay_state_trajectory" in path)
        )
        if floating:
            checks.append({"field": path, "policy": "equation", **reference._float_check(observed, expected)})
        else:
            equal = type(observed) is type(expected) and observed == expected
            if type(observed) is float and type(expected) is float:
                equal = reference._bits(observed) == reference._bits(expected)
            checks.append({"field": path, "policy": "exact", "observed": observed,
                           "expected": expected, "matches": equal})
    return checks


def reconcile(enqueued: list[Record], received: list[Record]) -> Record:
    report = reference._reconcile_route_events(enqueued, received)
    report["unmatched_reception_count"] = len(received) - report["matched_count"]
    report["source_mismatch_count"] = 0
    report["destination_mismatch_count"] = 0
    enqueues: dict[int, list[Record]] = {}
    receptions: dict[int, list[Record]] = {}
    for row in enqueued:
        enqueues.setdefault(row["queue_sequence"], []).append(row)
    for row in received:
        receptions.setdefault(row["queue_sequence"], []).append(row)
    for sequence, rows in enqueues.items():
        other = receptions.get(sequence, [])
        if len(rows) == len(other) == 1:
            report["source_mismatch_count"] += rows[0]["source"] != other[0]["source"]
            report["destination_mismatch_count"] += (
                rows[0]["destination"] != other[0]["destination"]
                or rows[0]["destination"] != other[0]["receiver_node"]
            )
    report["reconciles"] &= (
        not report["duplicate_enqueue_count"] and not report["unmatched_reception_count"]
        and not report["source_mismatch_count"] and not report["destination_mismatch_count"]
    )
    return report


def bounds_check(record: Record) -> Record:
    water = record["resource_high_water"]
    checks = {
        "queue": water["queue_capacity"] == 128 and water["queue_peak"] <= 128,
        "runtime": water["runtime_event_budget"] == 1024 and water["processed_events"] <= 1024,
        "activity": water["max_activity_events"] == 1024 and water["activity_high_water"] <= 1024,
        "neurons": water["per_neuron_event_budget"] == 4096
        and all(count <= 4096 for count in water["neuron_processed_events"].values()),
        "eligibility": water["eligibility_capacity_per_ledger"] == 1024
        and len(water["eligibility_ledgers"]) == 3
        and all(item["capacity"] == 1024 and item["peak"] <= 1024
                for item in water["eligibility_ledgers"]),
        "prediction": water["prediction_capacity"] == 8 and water["prediction_peak"] <= 8
        and water["prediction_expiry"] == 4.0,
        "topology": water["topology_edge_capacity"] == water["topology_routing_capacity"] == 3
        and water["topology_fan_in_limit"] == water["topology_fan_out_limit"] == 2
        and water["topology_edge_peak"] == water["topology_routing_peak"] == 2
        and water["topology_fan_in_peak"] <= 2 and water["topology_fan_out_peak"] <= 2,
        "completion": record["settling"]["completed"] and water["pending_events"] == 0
        and water["settling_horizon"] == 4.0,
        "state": all(
            abs(item[field]) <= (8.0 if field.startswith("x") else 4.0)
            for node in ("relay", "destination")
            for item in record[f"{node}_state_trajectory"]
            for field in ("x_before", "x_after", "z_before", "z_after")
            if item[field] is not None
        ),
    }
    return {"checks": checks, "matches": all(checks.values())}


def run_gates(runs: dict[str, list[Record]], historical: list[Record]) -> Record:
    checks: Record = {}
    calibrated = runs[ARMS[2]]
    if len(calibrated) != len(historical):
        raise Blocker("G1", {"reason": "sequence inventory differs"})
    checks["G1"] = []
    for current, old in zip(calibrated, historical):
        items = compare_historical(upstream(current), upstream(old))
        checks["G1"].append({"stream_id": current["stream_id"], "fields": items,
                             "historical_record_digest": old["record_digest"],
                             "matches": all(item["matches"] for item in items)})
        if not checks["G1"][-1]["matches"]:
            raise Blocker("G1", {"reason": "historical calibrated upstream differs", "checks": checks})
    checks["G2"] = []
    for arm in ARMS:
        if len(runs[arm]) != len(calibrated):
            raise Blocker("G2", {"reason": f"incomplete arm {arm}", "checks": checks})
        for current, control in zip(runs[arm], calibrated):
            equal = reference._canonical_bytes(upstream(current)) == reference._canonical_bytes(upstream(control))
            checks["G2"].append({"arm": arm, "stream_id": current["stream_id"], "matches": equal})
            if not equal:
                raise Blocker("G2", {"reason": "exact upstream cross-arm invariance failed", "checks": checks})
    checks["G3"] = []
    for arm in ARMS:
        for record in runs[arm]:
            reports = {}
            for source, destination in (("source", "relay"), ("relay", "destination")):
                enqueue = [item for item in record["routing_enqueue_events"]
                           if (item["source"], item["destination"]) == (source, destination)]
                receive = [item for item in record["receiver_reception_events"]
                           if item["receiver_node"] == destination]
                reports[f"{source}_to_{destination}"] = reconcile(enqueue, receive)
            reports["all"] = reconcile(record["routing_enqueue_events"], record["receiver_reception_events"])
            record["luna45_route_reconciliation"] = reports
            checks["G3"].append({"arm": arm, "stream_id": record["stream_id"], "reports": reports})
            if not all(item["reconciles"] for item in reports.values()):
                raise Blocker("G3", {"reason": "independent routing captures differ", "checks": checks})
    checks["G4"] = []
    for arm in ARMS:
        for record in runs[arm]:
            check = bounds_check(record)
            record["luna45_bounds"] = check
            checks["G4"].append({"arm": arm, "stream_id": record["stream_id"], **check})
            if not check["matches"]:
                raise Blocker("G4", {"reason": "bounds/completion failed", "checks": checks})
    return checks


def destination_evidence(record: Record) -> None:
    config = node_config(record["arm"], "destination")
    trajectory = record["destination_state_trajectory"]
    external = [item for item in trajectory if item["event_type"] == EventType.EXCURSION.value]
    traces = record["destination_integration_trace"]
    checks = reference._relay_recurrence_checks(traces, trajectory, config)
    if not all(item["matches"] for item in checks):
        raise Blocker("DESTINATION", {"reason": "independent recurrence mismatch", "checks": checks})
    if config.integration is None and (
        traces or any(item["z_before"] is not None or item["z_after"] is not None for item in trajectory)
    ):
        raise Blocker("DESTINATION", {"reason": "disabled destination exposes integration state"})
    evidence = []
    emissions = record["destination_emissions"]
    assigned: set[str] = set()
    contributing: list[Record] = []
    receptions = {item["queue_sequence"]: item for item in record["destination_receptions"]}
    enqueues = {item["queue_sequence"]: item for item in record["routing_enqueue_events"]
               if item["destination"] == "destination"}
    relay_emissions = {item["event_id"]: item for item in record["relay_emissions"]}
    for index, captured in enumerate(external):
        trace = traces[index] if config.integration is not None else None
        check = checks[index] if config.integration is not None else None
        reception = receptions[captured["queue_sequence"]]
        enqueue = enqueues[captured["queue_sequence"]]
        relay = relay_emissions[enqueue["event_id"]]
        dt = float(captured["timestamp"]) - float(captured["prior_clock"])
        if trace is not None:
            if (
                trace["theta_e"] != config.theta_e
                or trace["theta_z"] != config.integration.discharge_quantum
                or trace["decay_rate"] != config.decay_rate
                or trace["decay_rate_z"] != config.integration.decay_rate_z
            ):
                raise Blocker("DESTINATION", {"reason": "threshold/decay trace configuration mismatch"})
            assert check is not None
            discharge = check["discharge_amount"]["expected"]
            sign = 0 if discharge == 0.0 else (1 if discharge > 0.0 else -1)
            actual_sign = 0 if trace["discharge_amount"] == 0.0 else (1 if trace["discharge_amount"] > 0.0 else -1)
            if sign != actual_sign or (discharge != 0.0) != (trace["discharge_amount"] != 0.0):
                raise Blocker("DESTINATION", {"reason": "exact discharge decision/sign differs"})
            expected_category = check["expected_classification"]
            x_decay = check["x_after_decay"]["expected"]
            x_input = check["x_after_input"]["expected"]
        else:
            discharge = 0.0
            sign = 0
            x_decay = max(-config.x_max, min(config.x_max,
                         captured["x_before"] * math.exp(-config.decay_rate * dt)))
            x_input = max(-config.x_max, min(config.x_max, x_decay + captured["payload"]))
            expected_category = (
                "direct" if captured["mode_before"] == "N"
                and config.theta_e <= abs(x_input) < config.theta_m else "none"
            )
            fast_check = reference._float_check(captured["x_after"], x_input)
            if not fast_check["matches"]:
                raise Blocker("DESTINATION", {"reason": "disabled fast recurrence differs", "check": fast_check})
            check = {"fast_input": fast_check, "expected_classification": expected_category,
                     "dt": {"observed": dt, "expected": dt, "exact_match": True}}
        emission = next((item for item in emissions
                         if item["episode_id"] == captured["episode_id_after"]
                         and expected_category != "none"), None)
        if trace is not None and (
            trace["emission_id"] != (None if emission is None else emission["event_id"])
        ):
            raise Blocker("DESTINATION", {"reason": "trace canonical emission identity differs"})
        if expected_category != "none" and emission is None:
            raise Blocker("DESTINATION", {"reason": "admitted episode has no canonical emission"})
        contributing.append({
            "relay_emission_id": relay["event_id"], "relay_timestamp": relay["timestamp"],
            "reception_event_id": reception["event_id"],
            "reception_timestamp": reception["reception_timestamp"],
            "queue_sequence": reception["queue_sequence"],
        })
        category = "none" if emission is None else (
            "integration-mediated" if discharge != 0.0 else "direct"
        )
        row = {
            "stream_id": record["stream_id"], "relay_emission": relay,
            "queue_admission": enqueue, "actual_reception": reception,
            "relay_emission_id": relay["event_id"], "reception_event_id": reception["event_id"],
            "payload_encoding": reference._float_record(captured["payload"]),
            "arrival_timestamp": captured["timestamp"],
            "x_before_decay": captured["x_before"], "x_after_decay": x_decay,
            "x_after_update": x_input, "z_before_decay": captured["z_before"],
            "elapsed": dt, "z_after_decay": None if trace is None else trace["z_after_decay"],
            "routed_contribution": captured["payload"],
            "z_after_contribution": None if trace is None else trace["z_after_input"],
            "discharge_decision": discharge != 0.0, "discharge_amount": discharge,
            "discharge_sign": sign, "resulting_z": captured["z_after"],
            "x_post_discharge": captured["x_after"],
            "classification": category, "canonical_emission": emission,
            "canonical_emission_id": None if emission is None else emission["event_id"],
            "oracle": check, "contributing_receptions": deepcopy(contributing),
        }
        if emission is not None:
            assigned.add(emission["event_id"])
            row["relay_to_destination_emission_timing"] = [
                {**item, "delta": emission["timestamp"] - item["relay_timestamp"]}
                for item in contributing
            ]
            if category == "integration-mediated":
                row["genuine_chain"] = reconstruct_chain(record, row)
            contributing.clear()
        evidence.append(row)
    if assigned != {item["event_id"] for item in emissions}:
        raise Blocker("DESTINATION", {"reason": "unclassified canonical destination emission"})
    record["destination_evidence"] = evidence
    record["candidate_opportunity_precursors"] = precursor_scan(record)


def reconstruct_chain(record: Record, destination: Record) -> Record:
    links = []
    source_emissions = {item["event_id"]: item for item in record["source_emissions"]}
    input_roots = {f"{record['stream_id']}:input:{index}": item
                   for index, item in enumerate(record["point_inputs"])}
    source_enqueue = {item["event_id"]: item for item in record["routing_enqueue_events"]
                      if item["source"] == "source"}
    source_receive = {item["event_id"]: item for item in record["source_to_relay_receptions"]}
    relay_checks = {item["trace_emission_id"]: item for item in record["relay_recurrence_checks"]
                    if item["trace_emission_id"] is not None}
    for contribution in destination["contributing_receptions"]:
        relay = next(item for item in record["relay_emissions"]
                     if item["event_id"] == contribution["relay_emission_id"])
        check = relay_checks.get(relay["event_id"])
        if (
            check is None or not check["matches"]
            or check["expected_classification"] != "integrated_discharge"
        ):
            raise Blocker("DESTINATION", {"reason": "relay integrated emission link absent"})
        eligible = [item for item in record["source_to_relay_receptions"]
                    if item["reception_timestamp"] <= check["timestamp"]]
        causal = []
        for reception in eligible:
            source = source_emissions.get(reception["event_id"])
            enqueue = source_enqueue.get(reception["event_id"])
            roots = reception["causal_roots"]
            if (
                source is None or enqueue is None or reception["roots_truncated"]
                or not roots or any(root not in input_roots for root in roots)
                or not reconcile([enqueue], [source_receive[source["event_id"]]])["reconciles"]
            ):
                raise Blocker("DESTINATION", {"reason": "canonical source/admission/reception link absent"})
            causal.append({
                "source_inputs": [input_roots[root] for root in roots],
                "source_canonical_emission": source,
                "source_queue_admission": enqueue, "relay_actual_reception": reception,
                "source_to_relay_emission_delta": relay["timestamp"] - source["timestamp"],
            })
        if not causal:
            raise Blocker("DESTINATION", {"reason": "relay lacks canonical source evidence"})
        onward = next(item for item in record["routing_enqueue_events"]
                      if item["queue_sequence"] == contribution["queue_sequence"])
        receiver = next(item for item in record["destination_receptions"]
                        if item["queue_sequence"] == contribution["queue_sequence"])
        if not reconcile([onward], [receiver])["reconciles"]:
            raise Blocker("DESTINATION", {"reason": "onward actual consumption link absent"})
        links.append({
            "canonical_source_links": causal,
            "relay_state_trajectory": record["relay_state_trajectory"],
            "relay_recurrence": check, "relay_canonical_emission": relay,
            "relay_queue_admission": onward, "destination_actual_reception": receiver,
        })
    if not links or destination["canonical_emission"] is None:
        raise Blocker("DESTINATION", {"reason": "genuine chain incomplete"})
    return {
        "verified": True, "upstream_links": links,
        "destination_recurrence": destination["oracle"],
        "destination_canonical_emission": destination["canonical_emission"],
    }


def precursor_scan(record: Record) -> Record:
    destinations = record["destination_emissions"]
    pairs = []
    for later in destinations:
        for earlier in record["source_emissions"]:
            elapsed = later["timestamp"] - earlier["timestamp"]
            if 0.0 < elapsed <= ASSOCIATION_WINDOW:
                pairs.append({
                    "stream_id": record["stream_id"], "source_emitter": "source",
                    "destination_emitter": "destination",
                    "source_canonical_emission_id": earlier["event_id"],
                    "source_timestamp": earlier["timestamp"],
                    "destination_canonical_emission_id": later["event_id"],
                    "destination_timestamp": later["timestamp"], "elapsed": elapsed,
                    "source_to_destination_edge_exists": False,
                })
    return {
        "label": "candidate-opportunity precursors", "scan_performed": bool(destinations),
        "association_window": ASSOCIATION_WINDOW, "pairs": pairs, "count": len(pairs),
        "unique_characters": int(bool(pairs)), "candidate_instantiation": False,
    }


def arm_report(records: list[Record]) -> Record:
    evidence = [item for record in records for item in record.get("destination_evidence", [])]
    emitting = [item for item in evidence if item["canonical_emission"] is not None]
    z_values = [
        {"absolute_z": abs(item[key]), "z": item[key], "field": key,
         "stream_id": record["stream_id"], "timestamp": item["timestamp"],
         "event_id": item.get("event_id")}
        for record in records
        for item in record["destination_state_trajectory"]
        for key in ("z_before", "z_after") if item[key] is not None
    ] + [
        {"absolute_z": abs(item[key]), "z": item[key], "field": key,
         "stream_id": record["stream_id"], "timestamp": item["timestamp"],
         "event_id": reception["event_id"]}
        for record in records
        for item, reception in zip(record["destination_integration_trace"], record["destination_receptions"])
        for key in ("z_before_decay", "z_after_decay", "z_after_input", "z_post_discharge")
    ]
    counts = {
        "destination_receptions": sum(len(record["destination_receptions"]) for record in records),
        "direct_emissions": sum(item["classification"] == "direct" for item in emitting),
        "integration_mediated_emissions": sum(item["classification"] == "integration-mediated" for item in emitting),
        "genuine_integrated_emissions": sum(item.get("genuine_chain", {}).get("verified", False) for item in emitting),
    }
    return {
        "sequences": len(records), **counts,
        "destination_evidence_verified": all("destination_evidence" in record for record in records),
        "raw_destination_canonical_emissions": sum(len(record["destination_emissions"]) for record in records),
        "maximum_abs_z": max((item["absolute_z"] for item in z_values), default=0.0),
        "maximum_abs_z_location": max(z_values, key=lambda item: item["absolute_z"]) if z_values else None,
        "unique_emitting_characters": len({item["stream_id"] for item in emitting}),
        "emission_timing_and_contributing_receptions": [
            {"stream_id": item["stream_id"], "event_id": item["canonical_emission_id"],
             "classification": item["classification"],
             "contributing_reception_count": len(item["contributing_receptions"]),
             "timing": item["relay_to_destination_emission_timing"]}
            for item in emitting
        ],
        "candidate_opportunity_precursors": {
            "label": "candidate-opportunity precursors",
            "scan_performed": bool(emitting),
            "count": sum(record.get("candidate_opportunity_precursors", {}).get("count", 0) for record in records),
            "unique_characters": sum(record.get("candidate_opportunity_precursors", {}).get("unique_characters", 0) for record in records),
            "pairs": [item for record in records
                      for item in record.get("candidate_opportunity_precursors", {}).get("pairs", [])],
        },
        "upstream_counts": {
            key: sum(record["counts"][key] for record in records)
            for key in ("source_emissions", "source_to_relay_receptions",
                        "relay_integrated_emissions", "relay_direct_emissions",
                        "relay_to_destination_transfers")
        },
        "resource_high_water": reference._aggregate_arm(records)["resource_high_water"],
        "pending_events": sum(record["resource_high_water"]["pending_events"] for record in records),
        "route_reconciliation": {
            hop: {
                key: sum(record.get("luna45_route_reconciliation", {}).get(hop, {}).get(key, 0)
                         for record in records)
                for key in (
                    "enqueued_count", "received_count", "matched_count",
                    "unmatched_enqueue_count", "unmatched_reception_count", "orphan_reception_count",
                    "duplicate_enqueue_count", "duplicate_reception_count", "source_mismatch_count",
                    "destination_mismatch_count", "event_id_mismatch_count", "payload_mismatch_count",
                    "timing_mismatch_count", "route_path_mismatch_count", "provenance_mismatch_count",
                )
            } for hop in ("source_to_relay", "relay_to_destination", "all")
        },
    }


def phase_digest(records: list[Record], report: Record) -> str:
    return digest({
        "fixture_file_sha256": reference.FIXTURE_FILE_SHA256,
        "fixture_semantic_digest": reference.FIXTURE_SHA256,
        "config": experiment_config(), "records": records, "per_arm_report": report,
    })


def decide(replay_passes: bool, reports: Record) -> tuple[str, str]:
    if not replay_passes:
        return "BLOCKED", "BLOCKED"
    if reports[ARMS[2]]["genuine_integrated_emissions"] > 0:
        return "PASS", "SUPPORTED"
    return "PASS", "NOT SUPPORTED IN THIS SETUP"


def write_artifact(directory: Path, name: str, metadata: Record, body: Record) -> Record:
    artifact = reference._seal_artifact({**metadata, **body})
    path = directory / name
    payload = reference._canonical_bytes(artifact) + b"\n"
    with path.open("xb") as stream:
        stream.write(payload)
    if path.read_bytes() != payload:
        raise OSError(f"artifact readback differs: {path}")
    return {"file": name, "file_sha256": hashlib.sha256(payload).hexdigest(),
            "artifact_digest": artifact["artifact_digest"], "byte_length": len(payload)}


def persist_phase(directory: Path, phase: str, runs: dict[str, list[Record]],
                  metadata: Record, reports: Record, phase_digests: Record,
                  blocker: Record | None, gates: Record) -> Record:
    manifest = {}
    for arm in ARMS:
        stem = f"{phase}-{arm.lower()}"
        manifest[f"{arm}_records"] = write_artifact(directory, f"{stem}.json", metadata, {
            "schema": "TPCN-LUNA45-ARM-1", "phase": phase, "arm": arm,
            "records": runs[arm], "report": reports[arm],
            "phase_digest": phase_digests[arm], "blocker": blocker,
        })
        for stream, field in (("enqueue", "routing_enqueue_events"), ("reception", "receiver_reception_events")):
            manifest[f"{arm}_{stream}"] = write_artifact(directory, f"{stem}-{stream}.json", metadata, {
                "schema": "TPCN-LUNA45-RAW-1", "phase": phase, "arm": arm,
                "capture_stream": stream, "capture_scope": "routed EXCURSION",
                "per_sequence": [
                    {"stream_id": record["stream_id"], "events": record[field]}
                    for record in runs[arm]
                ],
            })
    manifest["gates"] = write_artifact(directory, f"{phase}-gates.json", metadata, {
        "schema": "TPCN-LUNA45-GATES-1", "phase": phase, "gates": gates, "blocker": blocker,
    })
    if blocker is not None and blocker.get("gate") == "EXECUTION":
        manifest["failed_character"] = write_artifact(directory, f"{phase}-failed-character.json", metadata, {
            "schema": "TPCN-LUNA45-FAILED-CHARACTER-1", "phase": phase,
            "failed_character": blocker,
        })
        for stream, field in (("enqueue", "routing_enqueue_events"), ("reception", "receiver_reception_events")):
            manifest[f"failed_{stream}"] = write_artifact(
                directory, f"{phase}-failed-{stream}.json", metadata, {
                    "schema": "TPCN-LUNA45-FAILED-RAW-1", "phase": phase,
                    "arm": blocker["arm"], "stream_id": blocker["stream_id"],
                    "capture_stream": stream, "events": blocker[field],
                },
            )
    return manifest


def execute_phase(fixture: Record, historical: list[Record]) -> tuple[dict[str, list[Record]], Record, Record, Record | None]:
    runs: dict[str, list[Record]] = {arm: [] for arm in ARMS}
    gates: Record = {}
    blocker = None
    try:
        for arm in ARMS:
            for sequence in fixture["sequences"]:
                runs[arm].append(run_character(arm, sequence))
        gates = run_gates(runs, historical)
        for arm in ARMS:
            for record in runs[arm]:
                destination_evidence(record)
    except Blocker as error:
        blocker = {"gate": error.gate, **error.detail}
        gates = error.detail.get("checks", gates)
    reports = {arm: arm_report(runs[arm]) for arm in ARMS}
    return runs, reports, gates, blocker


def run_experiment(output: Path = OUTPUT) -> Record:
    metadata = collect_provenance()
    fixture, manifest = load_inputs()
    historical, historical_identity = load_history()
    metadata["fixture_source_provenance"] = manifest
    metadata["historical_identity"] = historical_identity
    output.mkdir(parents=True, exist_ok=False)
    publications = {
        "config": write_artifact(output, "config.json", metadata, {
            "schema": "TPCN-LUNA45-CONFIG-1", "experiment": experiment_config(),
        })
    }
    initial, reports, gates, initial_blocker = execute_phase(fixture, historical)
    initial_digests = {
        arm: None if initial_blocker else phase_digest(initial[arm], reports[arm])
        for arm in ARMS
    }
    publications["initial"] = persist_phase(
        output, "initial", initial, metadata, reports, initial_digests, initial_blocker, gates
    )
    replay_digests: Record = {arm: None for arm in ARMS}
    replay_blocker = None
    replay_equal = False
    if initial_blocker is None:
        replay, replay_reports, replay_gates, replay_blocker = execute_phase(fixture, historical)
        if replay_blocker is None:
            replay_digests = {
                arm: phase_digest(replay[arm], replay_reports[arm]) for arm in ARMS
            }
            replay_equal = initial_digests == replay_digests
            if not replay_equal:
                replay_blocker = {"gate": "REPLAY", "reason": "canonical phase digests differ"}
        publications["replay"] = persist_phase(
            output, "replay", replay, metadata, replay_reports, replay_digests,
            replay_blocker, replay_gates,
        )
    if reference._git_output("rev-parse", "HEAD") != metadata["execution_revision"] or (
        file_hash(Path(__file__)) != metadata["runner_sha256"]
        or file_hash(Path(reference.__file__)) != REFERENCE_SOURCE_SHA256
    ):
        replay_blocker = {"gate": "PROVENANCE", "reason": "execution source/revision drift"}
        replay_equal = False
    status, verdict = decide(initial_blocker is None and replay_blocker is None and replay_equal, reports)
    summary = {
        "schema": "TPCN-LUNA45-SUMMARY-1", "status": status, "verdict": verdict,
        "initial_blocker": initial_blocker, "replay_blocker": replay_blocker,
        "replay_not_run": initial_blocker is not None,
        "initial_digests": initial_digests, "replay_digests": replay_digests,
        "replay_equal": replay_equal, "per_arm": reports,
        "between_arm_differences": [
            {"left": left, "right": right,
             "integrated_count_delta": reports[left]["integration_mediated_emissions"] - reports[right]["integration_mediated_emissions"],
             "direct_count_delta": reports[left]["direct_emissions"] - reports[right]["direct_emissions"],
             "max_abs_z_delta": reports[left]["maximum_abs_z"] - reports[right]["maximum_abs_z"]}
            for left, right in ((ARMS[2], ARMS[1]), (ARMS[2], ARMS[0]), (ARMS[1], ARMS[0]))
        ],
        "artifact_manifest": publications,
        "summary_digest": None,
        "independent_review": "NOT PERFORMED; return to lead orchestrator/Luna-0",
        "interpretation_boundary": "mechanism only; no efficacy, growth, promotion or successor",
    }
    if initial_blocker is None:
        summary["summary_digest"] = digest({
            "config_digest": metadata["config_digest"], "initial_digests": initial_digests,
            "replay_digests": replay_digests, "status": status, "verdict": verdict,
        })
    write_artifact(output, "summary.json", metadata, summary)
    return {**metadata, **summary}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--publish-config", action="store_true",
                        help="write only the predeclared config for the pre-science commit")
    args = parser.parse_args()
    if args.publish_config:
        PUBLISHED_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        with PUBLISHED_CONFIG.open("xb") as stream:
            stream.write(reference._canonical_bytes(experiment_config()) + b"\n")
        print(json.dumps({"config_digest": digest(experiment_config()),
                          "file_sha256": file_hash(PUBLISHED_CONFIG)}, sort_keys=True))
        return
    try:
        result = run_experiment(args.output)
    except (Blocker, OSError, subprocess.CalledProcessError, ValueError) as error:
        print(json.dumps({"status": "BLOCKED", "startup_error": str(error)}, sort_keys=True))
        raise SystemExit(1) from error
    print(json.dumps({key: result[key] for key in (
        "status", "verdict", "runner_revision", "config_digest",
        "initial_digests", "replay_digests", "initial_blocker", "replay_blocker",
    )}, sort_keys=True))
    if result["status"] == "BLOCKED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
