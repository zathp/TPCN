"""Run the bounded Luna-43 destination-integration mechanism comparison."""

from __future__ import annotations

from contextlib import ExitStack
from dataclasses import asdict, is_dataclass
from enum import Enum
import hashlib
import json
import math
import platform
import random
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable
from unittest import mock

import run_luna39_acp0008_propagation_emission_diagnostic as luna39
from tpcn.eligibility import EligibilityCapacityError, EligibilityLedger
from tpcn.event_runtime import Event, EventType, QueueCapacityError
from tpcn.excursion_neuron import (
    E1Config,
    ExcursionEmission,
    IntegrationConfig,
    MultiExcursionNeuron,
)
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.topology import BoundedTopology, Edge, TopologyCapacityError


AUTHORIZATION_REVISION = "f304e96f994d5b3f7842589c1b505d09c8fae4c6"
AUTHORIZATION_BASELINE = "b6ca4a67783bf37ded146944f8dc9afaf5277f11"
BRANCH = "copilot/execute-luna-43-cycle"
ARTIFACT_DIRECTORY = Path("artifacts/luna43-acp0008-destination-integration-mechanism")
HISTORICAL_RESULTS = Path("artifacts/luna42-acp0008-corrective-calibration/results.json")

ARMS = ("DESTINATION_DISABLED", "DESTINATION_DEFAULT", "DESTINATION_CALIBRATED")
SEEDS = (0, 1, 2, 3, 4)
NODES = ("source", "relay", "destination")
EDGE_LIST = (
    {"source": "source", "destination": "relay", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
    {"source": "relay", "destination": "destination", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
)
DECAY_RATE_Z = 0.0125
QUEUE_CAPACITY = 128
RUNTIME_EVENT_BUDGET = 1024
MAX_ACTIVITY_EVENTS = 1024
SETTLING_HORIZON = 4.0
PREDICTION_CAPACITY = 8
PREDICTION_EXPIRY = 4.0
ELIGIBILITY_CAPACITY = 1024
NEURON_EVENT_BUDGET = 4096
FLOAT_TOLERANCE_MULTIPLIER = 64.0
ASSOCIATION_WINDOW = 4.0
EXPECTED_HISTORICAL_COUNTS = {
    "CALIBRATED": {
        "characters": 320,
        "source_emissions": 1715,
        "source_to_relay_transfers": 1715,
        "relay_emissions": 235,
        "relay_integrated_emissions": 235,
        "relay_direct_emissions": 0,
        "relay_to_destination_transfers": 235,
        "destination_receptions": 235,
    },
}
HISTORICAL_ARM = {
    "DESTINATION_CALIBRATED": "CALIBRATED",
    "DESTINATION_DEFAULT": "CALIBRATED",
    "DESTINATION_DISABLED": "CALIBRATED",
}


class StopCondition(RuntimeError):
    def __init__(self, reason: str, detail: dict[str, Any] | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.detail = detail or {}


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_jsonable(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite experiment value")
        return value
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if hasattr(value, "__dict__"):
        return _jsonable(vars(value))
    return repr(value)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        _jsonable(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _artifact_digest(value: dict[str, Any]) -> str:
    payload = dict(value)
    payload.pop("artifact_digest", None)
    payload.pop("aggregate_run_digest", None)
    return _digest(payload)


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _float_tolerance(observed: float, expected: float) -> float:
    return FLOAT_TOLERANCE_MULTIPLIER * sys.float_info.epsilon * max(
        1.0, abs(observed), abs(expected)
    )


def _float_check(observed: float, expected: float) -> dict[str, Any]:
    error = abs(observed - expected)
    tolerance = _float_tolerance(observed, expected)
    return {
        "observed": observed,
        "expected": expected,
        "abs_error": error,
        "tolerance": tolerance,
        "matches": error <= tolerance,
    }


def _equivalent(observed: Any, expected: Any) -> bool:
    if isinstance(observed, bool) or isinstance(expected, bool):
        return observed is expected
    if isinstance(observed, float) and isinstance(expected, float):
        return _float_check(observed, expected)["matches"]
    if type(observed) is not type(expected):
        return False
    if isinstance(observed, dict):
        return (
            observed.keys() == expected.keys()
            and all(_equivalent(observed[key], expected[key]) for key in observed)
        )
    if isinstance(observed, (list, tuple)):
        return len(observed) == len(expected) and all(
            _equivalent(left, right) for left, right in zip(observed, expected)
        )
    return observed == expected


def _git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout.strip()


def _float_info() -> dict[str, Any]:
    return {
        key: getattr(sys.float_info, key)
        for key in (
            "epsilon", "dig", "mant_dig", "max", "max_10_exp", "max_exp",
            "min", "min_10_exp", "min_exp", "radix", "rounds",
        )
    }


def _full_node_configurations() -> dict[str, Any]:
    configs: dict[str, Any] = {}
    for arm in ARMS:
        configs[arm] = {
            node: _jsonable(
                asdict(
                    E1Config(
                        event_budget=NEURON_EVENT_BUDGET,
                        integration=(
                            None
                            if node == "source"
                            else IntegrationConfig(decay_rate_z=DECAY_RATE_Z)
                            if node == "relay"
                            else _integration_for_arm(arm)
                        ),
                    )
                )
            )
            for node in NODES
        }
    return configs


def _runner_sha256() -> str:
    return _file_sha256(Path(__file__))


def _collect_provenance(*, require_clean: bool = True) -> dict[str, Any]:
    branch = _git_output("branch", "--show-current")
    head = _git_output("rev-parse", "HEAD")
    upstream = _git_output("rev-parse", "@{u}")
    origin_main = _git_output("rev-parse", "origin/main")
    status = _git_output("status", "--porcelain")
    if branch != BRANCH or head != upstream:
        raise StopCondition(
            "execution must start on the synchronized published Luna-43 runner branch",
            {"branch": branch, "head": head, "upstream": upstream},
        )
    if _git_output("merge-base", AUTHORIZATION_REVISION, "HEAD") != AUTHORIZATION_REVISION:
        raise StopCondition("authorization revision is not an ancestor of execution HEAD")
    if origin_main != AUTHORIZATION_BASELINE:
        raise StopCondition(
            "origin/main differs from the authorized starting baseline",
            {"origin_main": origin_main, "expected": AUTHORIZATION_BASELINE},
        )
    if require_clean and status:
        raise StopCondition(
            "retained execution requires a clean worktree and index",
            {"git_status_porcelain": status.splitlines()},
        )
    return {
        "authorization_revision": AUTHORIZATION_REVISION,
        "execution_revision": head,
        "execution_repo_revision": head,
        "branch": branch,
        "upstream_revision": upstream,
        "origin_main_revision": origin_main,
        "git_status_porcelain_at_launch": status.splitlines(),
        "runner_file": Path(__file__).name,
        "runner_sha256": _runner_sha256(),
        "python": sys.version,
        "platform": platform.platform(),
        "float_info": _float_info(),
        "config_identity": "TPCN-LUNA43-ACP0008-DESTINATION-INTEGRATION-1",
        "floating_point_tolerance_rule": {
            "formula": "64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))",
            "multiplier": FLOAT_TOLERANCE_MULTIPLIER,
            "epsilon": sys.float_info.epsilon,
        },
    }


def _verify_execution(provenance: dict[str, Any], phase: str) -> None:
    head = _git_output("rev-parse", "HEAD")
    runner = _runner_sha256()
    if head != provenance["execution_revision"] or runner != provenance["runner_sha256"]:
        raise StopCondition(
            f"{phase} provenance changed",
            {
                "expected_execution_revision": provenance["execution_revision"],
                "observed_execution_revision": head,
                "expected_runner_sha256": provenance["runner_sha256"],
                "observed_runner_sha256": runner,
            },
        )


def experiment_config() -> dict[str, Any]:
    return {
        "schema": "TPCN-LUNA43-ACP0008-DESTINATION-INTEGRATION-1",
        "authorization_revision": AUTHORIZATION_REVISION,
        "scientific_scope": "bounded mechanism comparison only; no task efficacy, labels, growth, or tuning",
        "historical_reference": {
            "path": str(HISTORICAL_RESULTS),
            "artifact_sha256": _file_sha256(HISTORICAL_RESULTS),
            "historical_execution_revision": "d073ecc13e789105c611181992ce4c8d48c79030",
            "historical_arm_used_for_all_luna43_conditions": "CALIBRATED (relay decay_rate_z=0.0125)",
            "gate_counts": EXPECTED_HISTORICAL_COUNTS,
            "reconciliation": (
                "Exact input digests, discrete event identities/order/route/provenance and "
                "aggregate counts; binary64 equation-derived values in historical numeric "
                "records are equivalent under 64 * epsilon * max(1, |observed|, |expected|). "
                "The historical calibrated-relay arm is the reference for all three Luna-43 "
                "arms. Historical global queue sequence counters are excluded from cross-platform "
                "comparison; route-list order, timestamps and canonical event identities remain "
                "checked. All same-run destination arms must match relay records exactly."
            ),
        },
        "seeds": list(SEEDS),
        "characters_per_seed": 64,
        "stream_source": "read-only Luna-39/Luna-34 make_spiral_dataset helper; points/timestamps only",
        "stream_ordering": "inherited _training_point_sequences(seed) exact Luna-42 Phase-B ordering",
        "input": "point.x + point.y at point.timestamp; exact same-timestamp batching",
        "node_configuration": {
            "source": {
                "integration": None,
                "decay_rate": 1.0,
                "theta_E": 1.0,
                "theta_Z": 1.0,
                "input_gain": 1.0,
                "z_max": 4.0,
            },
            "relay": {
                "integration": {"decay_rate_z": DECAY_RATE_Z},
                "decay_rate": 1.0,
                "theta_E": 1.0,
                "theta_Z": 1.0,
                "input_gain": 1.0,
                "z_max": 4.0,
            },
            "destination_by_arm": {
                "DESTINATION_DISABLED": {
                    "integration": None,
                    "path": "actual E1Config.integration=None production path",
                },
                "DESTINATION_DEFAULT": {
                    "integration": {"decay_rate_z": 0.1, "input_gain": 1.0, "discharge_quantum": 1.0, "z_max": 4.0},
                    "path": "IntegrationConfig()",
                },
                "DESTINATION_CALIBRATED": {
                    "integration": {"decay_rate_z": DECAY_RATE_Z, "input_gain": 1.0, "discharge_quantum": 1.0, "z_max": 4.0},
                    "path": "IntegrationConfig(decay_rate_z=0.0125)",
                },
            },
            "unchanged_e1_defaults": {
                "decay_rate": 1.0,
                "theta_E": 1.0,
                "theta_Z": 1.0,
                "input_gain": 1.0,
                "z_max": 4.0,
            },
        },
        "full_e1_configuration_by_arm": _full_node_configurations(),
        "topology": {
            "nodes": list(NODES),
            "edges": list(EDGE_LIST),
            "fan_in_limit": 2,
            "fan_out_limit": 2,
            "edge_capacity": 3,
            "routing_capacity": 3,
            "growth_enabled": False,
            "candidate_creation": False,
            "admissions": False,
            "pruning": False,
            "topology_mutations_allowed": 0,
        },
        "runtime": {
            "queue_capacity": QUEUE_CAPACITY,
            "runtime_event_budget": RUNTIME_EVENT_BUDGET,
            "max_activity_events": MAX_ACTIVITY_EVENTS,
            "settling_horizon": SETTLING_HORIZON,
            "prediction_capacity": PREDICTION_CAPACITY,
            "prediction_expiry": PREDICTION_EXPIRY,
            "eligibility_capacity_per_ledger": ELIGIBILITY_CAPACITY,
            "neuron_event_budget": NEURON_EVENT_BUDGET,
            "neutral_reward": 0.0,
            "association_window": ASSOCIATION_WINDOW,
        },
        "exact_checks": [
            "matched point-stream/input digests",
            "event identity, route, order, and copied transfer/reception payload equality",
            "relay history against the matching raw Luna-42 arm and exact destination-arm invariance",
            "replay digests",
            "no topology mutation",
        ],
        "equation_checks": [
            "Model-B payload reconstruction",
            "destination ACP-0008 state recurrence with declared binary64 tolerance",
        ],
        "replay_runs": 2,
    }


def _emission_record(emission: ExcursionEmission) -> dict[str, Any]:
    return {
        "event_id": emission.event_id,
        "sequence": emission.sequence,
        "source": emission.source,
        "timestamp": emission.timestamp,
        "payload": emission.payload,
        "lineage_id": emission.lineage_id,
        "episode_id": emission.episode_id,
    }


def _point_batches(points: Iterable[Any]) -> tuple[tuple[tuple[float, float], ...], ...]:
    batches: list[list[tuple[float, float]]] = []
    last_timestamp: float | None = None
    for point in points:
        timestamp = float(point.timestamp)
        value = float(point.x) + float(point.y)
        if not math.isfinite(timestamp) or not math.isfinite(value):
            raise StopCondition("non-finite point input or timestamp")
        if last_timestamp is not None and timestamp < last_timestamp:
            raise StopCondition("input timestamps are not ordered", {"timestamp": timestamp})
        if not batches or timestamp != last_timestamp:
            batches.append([])
        batches[-1].append((timestamp, value))
        last_timestamp = timestamp
    return tuple(tuple(batch) for batch in batches)


def _topology() -> BoundedTopology:
    return BoundedTopology.from_edges(
        NODES,
        (
            Edge("source", "relay", 1.0, edge_weight=1.0, divider_strength=1.0, reference=0.0),
            Edge("relay", "destination", 1.0, edge_weight=1.0, divider_strength=1.0, reference=0.0),
        ),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=3,
        routing_capacity=3,
    )


def _topology_record(topology: BoundedTopology) -> list[dict[str, Any]]:
    return [
        {
            "source": edge.source,
            "destination": edge.destination,
            "delay": edge.propagation_delay,
            "w": edge.edge_weight,
            "d": edge.divider_strength,
            "r": edge.reference,
        }
        for edge in topology.edges
    ]


def _runtime_trace_record(item: tuple[Any, ...]) -> dict[str, Any]:
    if item[3] == "excursion_emission":
        fields = (
            "timestamp", "source", "destination", "event_type", "payload", "event_id",
            "sequence", "episode_id", "lineage_id", "causal_roots", "roots_truncated",
        )
        return {name: _jsonable(value) for name, value in zip(fields, item)}
    fields = (
        "timestamp", "source", "destination", "event_type", "payload", "sequence",
        "event_id", "lineage_id", "causal_roots", "route_depth", "route_path",
        "roots_truncated",
    )
    return {name: _jsonable(value) for name, value in zip(fields, item)}


class _EligibilityAudit:
    def __init__(self) -> None:
        self.stats: dict[str, dict[str, Any]] = {}
        self.ledgers: dict[str, EligibilityLedger] = {}
        self.capacity_errors: list[dict[str, Any]] = []

    def register(self, ledger: EligibilityLedger) -> None:
        self.ledgers[ledger.ledger_id] = ledger
        self.stats[ledger.ledger_id] = {
            "ledger_id": ledger.ledger_id,
            "capacity": ledger.max_traces,
            "initial": len(ledger.traces),
            "created": 0,
            "removed": 0,
            "peak": len(ledger.traces),
        }

    def observe(self, ledger: EligibilityLedger, callback: Any, event: Event) -> Any:
        before = {item.trace_id for item in ledger.traces}
        try:
            result = callback()
        except EligibilityCapacityError:
            self.capacity_errors.append(
                {
                    "ledger_id": ledger.ledger_id,
                    "event_id": event.event_id,
                    "timestamp": event.timestamp,
                    "occupancy": len(before),
                    "capacity": ledger.max_traces,
                }
            )
            raise
        after = {item.trace_id for item in ledger.traces}
        stats = self.stats[ledger.ledger_id]
        stats["created"] += len(after - before)
        stats["removed"] += len(before - after)
        stats["peak"] = max(stats["peak"], len(after))
        return result

    def finalize(self) -> list[dict[str, Any]]:
        records = []
        for ledger_id, stats in self.stats.items():
            item = dict(stats)
            ledger = self.ledgers[ledger_id]
            item["final"] = len(ledger.traces)
            item["reconciles"] = (
                item["initial"] + item["created"] - item["removed"] == item["final"]
            )
            records.append(item)
        return sorted(records, key=lambda item: item["ledger_id"])


def _integration_for_arm(arm: str) -> IntegrationConfig | None:
    if arm == "DESTINATION_DISABLED":
        return None
    if arm == "DESTINATION_DEFAULT":
        return IntegrationConfig()
    if arm == "DESTINATION_CALIBRATED":
        return IntegrationConfig(decay_rate_z=DECAY_RATE_Z)
    raise ValueError(f"unknown destination condition {arm}")


def _state_record(neuron: MultiExcursionNeuron) -> dict[str, Any]:
    return {
        "x": float(neuron.state),
        "z": None if neuron.integration_state is None else float(neuron.integration_state),
        "mode": neuron.mode.value,
        "last_update_timestamp": float(neuron.last_update_timestamp),
        "processed_events": neuron.processed_event_count,
        "provenance_truncated": neuron.provenance_truncated,
        "unassigned_provenance_count": neuron._unassigned_provenance_count,
        "unassigned_provenance_truncated": neuron._unassigned_provenance_truncated,
    }


def _run_character(
    *, arm: str, seed: int, sequence_index: int, points: tuple[Any, ...]
) -> dict[str, Any]:
    character_id = f"c{seed:02d}-{sequence_index:03d}"
    batches = _point_batches(points)
    if not batches:
        raise StopCondition("frozen stream produced an empty character", {"character_id": character_id})
    input_digest = _digest(batches)
    destination_integration = _integration_for_arm(arm)
    integrations = {
        "source": None,
        "relay": IntegrationConfig(decay_rate_z=DECAY_RATE_Z),
        "destination": destination_integration,
    }
    neurons = {
        node: MultiExcursionNeuron(
            node,
            config=E1Config(
                event_budget=NEURON_EVENT_BUDGET,
                integration=integrations[node],
            ),
        )
        for node in NODES
    }
    runtime_topology = _topology()
    topology_before = _topology_record(runtime_topology)
    runtime = ExcursionCharacterRuntime(
        tuple(neurons[node] for node in NODES),
        runtime_topology,
        queue_capacity=QUEUE_CAPACITY,
        event_budget=RUNTIME_EVENT_BUDGET,
        settling_horizon=SETTLING_HORIZON,
        prediction_capacity=PREDICTION_CAPACITY,
        prediction_expiry=PREDICTION_EXPIRY,
        max_activity_events=MAX_ACTIVITY_EVENTS,
        namespace=f"luna42-{HISTORICAL_ARM[arm].lower()}-seed-{seed}",
        eligibility_capacity=ELIGIBILITY_CAPACITY,
    )
    audit = _EligibilityAudit()
    reset_snapshots: dict[str, dict[str, Any]] = {}
    destination_inputs: list[dict[str, Any]] = []
    relay_inputs: list[dict[str, Any]] = []
    original_reset = MultiExcursionNeuron.reset
    original_receive = MultiExcursionNeuron.receive_event
    original_ledger_init = EligibilityLedger.__init__
    original_record_activity = EligibilityLedger.record_activity
    original_apply_signal = EligibilityLedger.apply_signal

    def capture_reset(neuron: MultiExcursionNeuron, *, timestamp: float = 0.0) -> None:
        reset_snapshots[neuron.neuron_id] = {
            "emissions": [_emission_record(item) for item in neuron.emissions],
            "integration_trace_objects": list(neuron.integration_trace),
            "state": _state_record(neuron),
        }
        original_reset(neuron, timestamp=timestamp)

    def ledger_init(ledger: EligibilityLedger, *args: Any, **kwargs: Any) -> None:
        original_ledger_init(ledger, *args, **kwargs)
        audit.register(ledger)

    def record_activity(ledger: EligibilityLedger, event: Event) -> Any:
        return audit.observe(ledger, lambda: original_record_activity(ledger, event), event)

    def apply_signal(ledger: EligibilityLedger, event: Event) -> Any:
        return audit.observe(ledger, lambda: original_apply_signal(ledger, event), event)

    def capture_receive(
        neuron: MultiExcursionNeuron, event: Event, queue: Any = None
    ) -> Any:
        is_relay_reception = (
            neuron.neuron_id == "relay"
            and event.event_type == EventType.EXCURSION
            and event.source == "source"
        )
        is_destination_reception = (
            neuron.neuron_id == "destination"
            and event.event_type == EventType.EXCURSION
            and event.source == "relay"
        )
        before = _state_record(neuron) if is_destination_reception else None
        previous_episode = neuron.ordinary_episode_id if is_destination_reception else None
        result = original_receive(neuron, event, queue)
        if is_relay_reception:
            relay_inputs.append({
                "event_id": event.event_id,
                "source": event.source,
                "destination": event.destination,
                "timestamp": float(event.timestamp),
                "payload": float(event.payload),
                "sequence": event.sequence,
                "lineage_id": event.lineage_id,
                "integration_trace_object": neuron.integration_trace[-1],
            })
        if is_destination_reception:
            trace_object = (
                neuron.integration_trace[-1]
                if neuron.config.integration is not None
                else None
            )
            destination_inputs.append(
                {
                    "event_id": event.event_id,
                    "source": event.source,
                    "destination": event.destination,
                    "timestamp": float(event.timestamp),
                    "payload": float(event.payload),
                    "sequence": event.sequence,
                    "lineage_id": event.lineage_id,
                    "before": before,
                    "after": _state_record(neuron),
                    "episode_id_after_input": (
                        neuron.ordinary_episode_id
                        if neuron.ordinary_episode_id != previous_episode
                        else None
                    ),
                    "integration_trace_object": trace_object,
                }
            )
        return result

    try:
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(MultiExcursionNeuron, "reset", capture_reset))
            stack.enter_context(mock.patch.object(MultiExcursionNeuron, "receive_event", capture_receive))
            stack.enter_context(mock.patch.object(EligibilityLedger, "__init__", ledger_init))
            stack.enter_context(mock.patch.object(EligibilityLedger, "record_activity", record_activity))
            stack.enter_context(mock.patch.object(EligibilityLedger, "apply_signal", apply_signal))
            runtime.start_character(
                character_id,
                sequence_index,
                timestamp=0.0,
                predictor_source="source",
                readout_sources=NODES,
                input_destination="source",
            )
            for batch in batches:
                runtime.admit_external_batch(batch)
            last_timestamp = batches[-1][-1][0]
            runtime_result = runtime.end_character(
                last_external_timestamp=last_timestamp,
                reward=0.0,
                reward_delay=0.0,
                reward_message_id=f"luna43-neutral-{character_id}",
            )
    except EligibilityCapacityError as error:
        raise StopCondition("eligibility capacity exceeded", {
            "arm": arm, "seed": seed, "character_id": character_id, "message": str(error),
            "partial_destination_receptions": destination_inputs,
            "partial_relay_receptions": relay_inputs,
            "runtime_events_so_far": [
                _runtime_trace_record(item) for item in getattr(runtime, "_trace", ())
            ],
        }) from error
    except (QueueCapacityError, TopologyCapacityError, BufferError) as error:
        raise StopCondition("bounded runtime capacity exceeded", {
            "arm": arm, "seed": seed, "character_id": character_id,
            "exception": type(error).__name__, "message": str(error),
            "partial_destination_receptions": destination_inputs,
            "partial_relay_receptions": relay_inputs,
            "runtime_events_so_far": [
                _runtime_trace_record(item) for item in getattr(runtime, "_trace", ())
            ],
        }) from error
    except StopCondition:
        raise
    except Exception as error:
        raise StopCondition("production runtime exception", {
            "arm": arm, "seed": seed, "character_id": character_id,
            "exception": type(error).__name__, "message": str(error),
        }) from error

    ledgers = audit.finalize()
    if (
        len(ledgers) != len(NODES)
        or any(row["capacity"] != ELIGIBILITY_CAPACITY or not row["reconciles"] for row in ledgers)
        or any(row["peak"] >= ELIGIBILITY_CAPACITY for row in ledgers)
        or audit.capacity_errors
    ):
        raise StopCondition("eligibility ledger reconciliation/capacity failure", {
            "arm": arm, "seed": seed, "character_id": character_id,
            "eligibility_ledgers": ledgers, "capacity_errors": audit.capacity_errors,
        })
    if (
        runtime_result.execution.budget_exhausted
        or runtime_result.execution.pending_event_count != 0
        or not runtime_result.execution.completed
    ):
        raise StopCondition("runtime did not settle within declared event bounds", {
            "arm": arm, "seed": seed, "character_id": character_id,
            "execution": _jsonable(runtime_result.execution),
            "partial_destination_receptions": destination_inputs,
            "partial_relay_receptions": relay_inputs,
            "runtime_events_so_far": [
                _runtime_trace_record(item) for item in runtime_result.trace
            ],
        })
    if set(reset_snapshots) != set(NODES):
        raise StopCondition("neuron teardown snapshots are incomplete", {
            "expected_nodes": list(NODES), "observed_nodes": sorted(reset_snapshots),
        })
    topology_after = _topology_record(runtime_topology)
    if topology_after != topology_before or topology_after != list(EDGE_LIST):
        raise StopCondition("fixed topology changed during character", {
            "before": topology_before, "after": topology_after,
        })

    snapshots = {
        node: {
            "emissions": reset_snapshots[node]["emissions"],
            "integration_trace": [
                _jsonable(trace) for trace in reset_snapshots[node]["integration_trace_objects"]
            ],
            "state": reset_snapshots[node]["state"],
        }
        for node in NODES
    }
    source_emissions = snapshots["source"]["emissions"]
    relay_emissions = snapshots["relay"]["emissions"]
    destination_emissions = snapshots["destination"]["emissions"]
    trace_records = [_runtime_trace_record(item) for item in runtime_result.trace]
    routed_events = [
        item for item in trace_records
        if item["event_type"] == EventType.EXCURSION.value
        and (item["source"], item["destination"]) in (
            ("source", "relay"), ("relay", "destination")
        )
    ]
    emission_by_id = {
        item["event_id"]: item
        for node in ("source", "relay")
        for item in snapshots[node]["emissions"]
    }
    relay_receptions = []
    relay_route_events = [
        item for item in routed_events
        if item["source"] == "source" and item["destination"] == "relay"
    ]
    if len(relay_inputs) != len(relay_route_events):
        raise StopCondition("source->relay routed-event/reception count mismatch", {
            "arm": arm, "character_id": character_id,
            "route_count": len(relay_route_events), "reception_count": len(relay_inputs),
        })
    for captured in relay_inputs:
        route_event = next(
            (
                item for item in relay_route_events
                if item["event_id"] == captured["event_id"]
                and item["timestamp"] == captured["timestamp"]
                and item["payload"] == captured["payload"]
                and item["sequence"] == captured["sequence"]
                and item["lineage_id"] == captured["lineage_id"]
            ),
            None,
        )
        source_emission = emission_by_id.get(captured["event_id"])
        trace = _jsonable(captured["integration_trace_object"])
        if (
            route_event is None
            or source_emission is None
            or source_emission["source"] != "source"
            or not source_emission["timestamp"] < captured["timestamp"]
            or trace["timestamp"] != captured["timestamp"]
            or trace["input_value"] != captured["payload"]
        ):
            raise StopCondition("relay reception/integration trace lacks exact routed-source provenance", {
                "arm": arm, "character_id": character_id, "reception": captured,
                "route_event": route_event, "source_emission": source_emission, "trace": trace,
            })
        relay_receptions.append({
            "event_id": captured["event_id"],
            "source": "source",
            "destination": "relay",
            "arrival_timestamp": captured["timestamp"],
            "arrival_payload": captured["payload"],
            "route_event": route_event,
            "prior_source_canonical_event": source_emission,
            "integration_trace": trace,
        })
    route_reconciliations = []
    for event in routed_events:
        emission = emission_by_id.get(event["event_id"])
        if emission is None:
            raise StopCondition("routed event lacks its prior canonical emission", {
                "arm": arm, "character_id": character_id, "route_event": event,
            })
        expected_payload = math.tanh(float(emission["payload"]))
        match = _float_check(float(event["payload"]), expected_payload)
        route_reconciliations.append({
            "route_event": event,
            "canonical_emission": emission,
            "model_b_expected_payload": expected_payload,
            "model_b_comparison": match,
            "payload_finite": math.isfinite(float(event["payload"])),
            "emission_precedes_arrival": emission["timestamp"] < event["timestamp"],
        })
        if (
            not match["matches"]
            or not emission["timestamp"] < event["timestamp"]
            or emission["source"] != event["source"]
            or event["route_path"] != [event["source"], event["destination"]]
        ):
            raise StopCondition("Model-B transfer/canonical-emission reconciliation failed", {
                "arm": arm, "character_id": character_id, "reconciliation": route_reconciliations[-1],
            })

    event_by_identity = {
        (item["event_id"], item["source"], item["destination"], item["timestamp"]): item
        for item in routed_events
    }
    for captured in destination_inputs:
        event = event_by_identity.get((
            captured["event_id"], "relay", "destination", captured["timestamp"]
        ))
        if (
            event is None
            or event["payload"] != captured["payload"]
            or event["sequence"] != captured["sequence"]
            or event["lineage_id"] != captured["lineage_id"]
        ):
            raise StopCondition("destination reception does not exactly reconcile to routed event", {
                "arm": arm, "character_id": character_id, "captured": captured, "route_event": event,
            })
        prior_relay = emission_by_id.get(captured["event_id"])
        if prior_relay is None or prior_relay["source"] != "relay":
            raise StopCondition("destination reception lacks prior relay canonical event", {
                "arm": arm, "character_id": character_id, "captured": captured,
            })
        captured["prior_relay_canonical_event"] = prior_relay
        captured["route_event"] = event
        captured["stream_identity"] = {
            "character_id": character_id, "seed": seed, "sequence_index": sequence_index,
            "input_digest": input_digest,
        }
        captured["destination_integration"] = (
            None if destination_integration is None else _jsonable(destination_integration)
        )
        dt = captured["timestamp"] - captured["before"]["last_update_timestamp"]
        captured["elapsed_since_destination_update"] = dt
        trace_object = captured.pop("integration_trace_object")
        if trace_object is not None:
            trace = _jsonable(trace_object)
            captured["integration_trace"] = trace
            captured["stage_states"] = {
                "x_before_decay": trace["x_before_decay"],
                "z_before_decay": trace["z_before_decay"],
                "x_after_decay": trace["x_after_decay"],
                "z_after_decay": trace["z_after_decay"],
                "x_after_input": trace["x_after_input"],
                "z_after_input": trace["z_after_input"],
                "discharge_amount": trace["discharge_amount"],
                "x_post_discharge": trace["x_post_discharge"],
                "z_post_discharge": trace["z_post_discharge"],
            }
            expected_decay = float(trace["z_before_decay"]) * math.exp(
                -float(trace["decay_rate_z"]) * float(trace["elapsed"])
            )
            recurrence = _float_check(float(trace["z_after_decay"]), expected_decay)
            if not recurrence["matches"]:
                raise StopCondition("destination ACP-0008 decay recurrence mismatch", {
                    "arm": arm, "character_id": character_id, "event_id": captured["event_id"],
                    "comparison": recurrence,
                })
            captured["z_decay_recurrence"] = recurrence
        else:
            decay = math.exp(-float(neurons["destination"].config.decay_rate) * dt)
            x_after_decay = float(captured["before"]["x"]) * decay
            captured["integration_trace"] = None
            captured["stage_states"] = {
                "x_before_decay": captured["before"]["x"],
                "z_before_decay": None,
                "x_after_decay": x_after_decay,
                "z_after_decay": None,
                "x_after_input": captured["after"]["x"],
                "z_after_input": None,
                "discharge_amount": 0.0,
                "x_post_discharge": captured["after"]["x"],
                "z_post_discharge": None,
            }
            captured["z_decay_recurrence"] = None
            captured["disabled_x_decay_reconstruction"] = {
                "decay_rate": neurons["destination"].config.decay_rate,
                "elapsed": dt,
                "decay_factor": decay,
                "x_after_decay_reconstructed": x_after_decay,
                "integration_state_absent": captured["after"]["z"] is None,
            }
        episode_id = captured["episode_id_after_input"]
        destination_emission = next(
            (
                item for item in destination_emissions
                if episode_id is not None and item["episode_id"] == episode_id
            ),
            None,
        )
        captured["emission_identity"] = (
            None if destination_emission is None else destination_emission["event_id"]
        )
        if destination_emission is None:
            captured["emission_classification"] = "no_emission"
        else:
            matching_trace = next(
                (
                    trace for trace in snapshots["destination"]["integration_trace"]
                    if trace.get("emission_id") == destination_emission["event_id"]
                ),
                None,
            )
            if destination_integration is not None:
                if matching_trace is None:
                    raise StopCondition("destination emission lacks ACP-0008 trace classification", {
                        "arm": arm, "character_id": character_id,
                        "emission": destination_emission, "reception": captured,
                    })
                captured["emission_classification"] = (
                    "integration-mediated"
                    if matching_trace["classification"] == "integrated_discharge"
                    else "direct"
                )
            else:
                captured["emission_classification"] = "direct_disabled_path"
            captured["emission_record"] = {
                **destination_emission,
                "classification_derived_from_trace": (
                    None if matching_trace is None else matching_trace["classification"]
                ),
                "integration_trace": matching_trace,
                "post_discharge_state": (
                    None if matching_trace is None else {
                        "x": matching_trace["x_post_discharge"],
                        "z": matching_trace["z_post_discharge"],
                    }
                ),
            }

    destination_emission_records = []
    for emission in destination_emissions:
        input_matches = [
            item for item in destination_inputs
            if item["episode_id_after_input"] == emission["episode_id"]
        ]
        if len(input_matches) != 1:
            raise StopCondition("destination canonical emission lacks one unique routed input", {
                "arm": arm, "character_id": character_id, "emission": emission,
                "causal_input_count": len(input_matches),
            })
        cause = input_matches[0]
        if cause.get("emission_record", {}).get("event_id") != emission["event_id"]:
            raise StopCondition("destination emission identity does not reconcile to its causal input trace", {
                "arm": arm, "character_id": character_id, "emission": emission, "cause": cause,
            })
        destination_emission_records.append({
            **emission,
            "classification": cause["emission_classification"],
            "trace_classification": (
                None if cause["integration_trace"] is None
                else cause["integration_trace"]["classification"]
            ),
            "cause_stream_identity": cause["stream_identity"],
            "prior_relay_canonical_event": cause["prior_relay_canonical_event"],
            "route_event": cause["route_event"],
            "arrival_timestamp": cause["timestamp"],
            "arrival_payload": cause["payload"],
            "integration_trace": cause["integration_trace"],
            "state_stages": cause["stage_states"],
            "post_discharge_state": {
                "x": cause["stage_states"]["x_post_discharge"],
                "z": cause["stage_states"]["z_post_discharge"],
            },
        })

    # A capture is a reception only if it is an actual routed delivery.
    reception_keys = {
        (item["event_id"], item["timestamp"], item["payload"])
        for item in destination_inputs
    }
    expected_reception_keys = {
        (item["event_id"], item["timestamp"], item["payload"])
        for item in routed_events if item["destination"] == "destination"
    }
    if reception_keys != expected_reception_keys:
        raise StopCondition("destination route/reception identities do not reconcile", {
            "arm": arm, "character_id": character_id,
            "captured_count": len(reception_keys), "routed_count": len(expected_reception_keys),
        })

    classified_relay_emissions = []
    relay_trace = snapshots["relay"]["integration_trace"]
    for emission in relay_emissions:
        trace = next((item for item in relay_trace if item.get("emission_id") == emission["event_id"]), None)
        classification = (
            "integration-mediated"
            if trace is not None and trace["classification"] == "integrated_discharge"
            else "direct"
        )
        if trace is None or trace["classification"] != "integrated_discharge":
            raise StopCondition("frozen relay emission is not trace-verified integrated discharge", {
                "arm": arm, "character_id": character_id, "emission": emission, "trace": trace,
            })
        matching_receptions = [
            item for item in relay_receptions
            if item["integration_trace"]["timestamp"] == trace["timestamp"]
            and item["integration_trace"]["input_value"] == trace["input_value"]
            and item["integration_trace"]["emission_id"] == emission["event_id"]
        ]
        causal_reception = matching_receptions[0] if len(matching_receptions) == 1 else None
        if causal_reception is None or not causal_reception["arrival_timestamp"] < emission["timestamp"]:
            raise StopCondition("relay integration emission lacks an earlier actual routed input", {
                "arm": arm, "character_id": character_id, "emission": emission,
                "integration_trace": trace, "causal_reception": causal_reception,
            })
        classified_relay_emissions.append({
            **emission,
            "classification": classification,
            "trace_classification": trace["classification"],
            "integration_trace": trace,
            "causal_routed_reception": causal_reception,
        })

    for node in NODES:
        state = snapshots[node]["state"]
        if state["provenance_truncated"] or state["unassigned_provenance_truncated"]:
            # Route sidecar ancestry can be explicitly capped; neuron-local
            # provenance truncation would invalidate the retained local trace.
            raise StopCondition("neuron-local provenance was truncated", {
                "arm": arm, "character_id": character_id, "node": node, "state": state,
            })
        if abs(state["x"]) > 8.0 or (state["z"] is not None and abs(state["z"]) > 4.0):
            raise StopCondition("neuron state exceeded declared bounds", {
                "arm": arm, "character_id": character_id, "node": node, "state": state,
            })

    if runtime_result.execution.processed_event_count > RUNTIME_EVENT_BUDGET:
        raise StopCondition("runtime event budget exceeded", {"character_id": character_id})
    if runtime_result.peak_queue_occupancy > QUEUE_CAPACITY:
        raise StopCondition("event queue capacity exceeded", {"character_id": character_id})

    relay_times = [float(item["timestamp"]) for item in classified_relay_emissions]
    arrival_times = [
        float(item["timestamp"]) for item in routed_events
        if item["source"] == "relay" and item["destination"] == "destination"
    ]
    relay_spacings = [
        {"previous_timestamp": left, "timestamp": right, "delta": right - left}
        for left, right in zip(relay_times, relay_times[1:])
    ]
    arrival_spacings = [
        {"previous_arrival_timestamp": left, "arrival_timestamp": right, "delta": right - left}
        for left, right in zip(arrival_times, arrival_times[1:])
    ]
    return {
        "arm": arm,
        "seed": seed,
        "sequence_index": sequence_index,
        "character_id": character_id,
        "input_digest": input_digest,
        "input_batches": batches,
        "node_integration_config": {
            node: (
                None if integrations[node] is None else _jsonable(integrations[node])
            )
            for node in NODES
        },
        "topology": topology_before,
        "topology_after_character": topology_after,
        "source_emissions": source_emissions,
        "relay_emissions": classified_relay_emissions,
        "destination_emissions": destination_emissions,
        "destination_emission_records": destination_emission_records,
        "routed_events": routed_events,
        "route_reconciliations": route_reconciliations,
        "relay_integration_trace": relay_trace,
        "relay_receptions": relay_receptions,
        "destination_receptions": destination_inputs,
        "runtime_events": trace_records,
        "route_context_roots_truncated": sum(
            bool(item.get("roots_truncated", False)) for item in trace_records
        ),
        "state_at_teardown": {node: snapshots[node]["state"] for node in NODES},
        "resource_high_water": {
            "queue_capacity": QUEUE_CAPACITY,
            "queue_peak": runtime_result.peak_queue_occupancy,
            "runtime_event_budget": RUNTIME_EVENT_BUDGET,
            "processed_events": runtime_result.execution.processed_event_count,
            "pending_events": runtime_result.execution.pending_event_count,
            "max_activity_events": MAX_ACTIVITY_EVENTS,
            "eligibility_capacity_per_ledger": ELIGIBILITY_CAPACITY,
            "eligibility_ledgers": ledgers,
            "prediction_capacity": PREDICTION_CAPACITY,
            "prediction_expiry": PREDICTION_EXPIRY,
            "prediction_expired": runtime_result.expired_predictions,
            "prediction_peak_pending": None,
            "prediction_peak_visibility": "not exposed by the production runtime result",
        },
        "settling": {
            "completed": runtime_result.execution.completed,
            "termination_reason": runtime_result.execution.termination_reason,
            "last_event_timestamp": runtime_result.execution.last_event_timestamp,
            "horizon": last_timestamp + SETTLING_HORIZON,
        },
        "timing_metrics": {
            "relay_emission_spacings": relay_spacings,
            "relay_to_destination_arrival_spacings": arrival_spacings,
            "destination_z_before_input": [
                {
                    "event_id": item["event_id"],
                    "timestamp": item["timestamp"],
                    "z_before_decay": item["stage_states"]["z_before_decay"],
                    "z_after_decay": item["stage_states"]["z_after_decay"],
                    "retention_ratio": (
                        None if item["stage_states"]["z_before_decay"] in (None, 0.0)
                        else item["stage_states"]["z_after_decay"] / item["stage_states"]["z_before_decay"]
                    ),
                    "z_discharge": item["stage_states"]["discharge_amount"],
                }
                for item in destination_inputs
            ],
            "max_abs_destination_z": max(
                (
                    abs(float(value))
                    for item in destination_inputs
                    for value in (
                        item["stage_states"]["z_before_decay"],
                        item["stage_states"]["z_after_decay"],
                        item["stage_states"]["z_after_input"],
                        item["stage_states"]["z_post_discharge"],
                    )
                    if value is not None
                ),
                default=0.0,
            ),
            "destination_discharges": [
                {
                    "timestamp": item["timestamp"],
                    "event_id": item["event_id"],
                    "discharge_amount": item["stage_states"]["discharge_amount"],
                }
                for item in destination_inputs
                if item["stage_states"]["discharge_amount"] != 0.0
            ],
            "destination_emission_timestamps": [
                item["timestamp"] for item in destination_emissions
            ],
        },
        "counts": {
            "source_emissions": len(source_emissions),
            "source_to_relay_transfers": sum(
                item["source"] == "source" and item["destination"] == "relay"
                for item in routed_events
            ),
            "relay_emissions": len(classified_relay_emissions),
            "relay_integrated_emissions": sum(
                item["classification"] == "integration-mediated"
                for item in classified_relay_emissions
            ),
            "relay_direct_emissions": sum(
                item["classification"] == "direct" for item in classified_relay_emissions
            ),
            "relay_to_destination_transfers": sum(
                item["source"] == "relay" and item["destination"] == "destination"
                for item in routed_events
            ),
            "destination_receptions": len(destination_inputs),
            "destination_emissions": len(destination_emissions),
        },
        "all_route_reconciliations_pass": all(
            item["model_b_comparison"]["matches"] and item["payload_finite"]
            and item["emission_precedes_arrival"]
            for item in route_reconciliations
        ),
    }


def _historical_results() -> dict[str, Any]:
    try:
        historical = json.loads(HISTORICAL_RESULTS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise StopCondition("raw Luna-42 reference artifact is unreadable", {
            "path": str(HISTORICAL_RESULTS), "error": str(error),
        }) from error
    if historical.get("provenance", {}).get("execution_revision") != (
        "d073ecc13e789105c611181992ce4c8d48c79030"
    ):
        raise StopCondition("raw Luna-42 artifact has unexpected execution revision")
    if historical.get("phase_b", {}).get("selected_decay_rate_z") != DECAY_RATE_Z:
        raise StopCondition("Luna-42 calibrated relay used a different decay value")
    return historical


def _historical_route_view(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{key: value for key, value in event.items() if key != "sequence"} for event in events]


def _historical_record_match(record: dict[str, Any], historical: dict[str, Any]) -> dict[str, Any]:
    historical_arm = HISTORICAL_ARM[record["arm"]]
    old = historical["phase_b"]["records"][historical_arm][str(record["seed"])][record["sequence_index"]]
    comparisons: dict[str, bool] = {
        "input_digest": record["input_digest"] == old["input_digest"],
        "source_emissions": _equivalent(record["source_emissions"], old["source_emissions"]),
        "relay_emission_records": _equivalent([
            {k: v for k, v in item.items() if k in (
                "event_id", "sequence", "source", "timestamp", "payload", "lineage_id", "episode_id",
                "classification", "trace_classification", "integration_trace",
            )}
            for item in record["relay_emissions"]
        ], old["relay_emissions"]),
        "relay_integration_trace": _equivalent(record["relay_integration_trace"], old["relay_integration_trace"]),
        "source_to_relay_route_events": _equivalent(_historical_route_view([
            item for item in record["routed_events"]
            if item["source"] == "source" and item["destination"] == "relay"
        ]), _historical_route_view([
            item for item in old["routed_signal_transfers"]
            if item["source"] == "source" and item["destination"] == "relay"
        ])),
        "relay_to_destination_route_events": _equivalent(_historical_route_view([
            item for item in record["routed_events"]
            if item["source"] == "relay" and item["destination"] == "destination"
        ]), _historical_route_view([
            item for item in old["routed_signal_transfers"]
            if item["source"] == "relay" and item["destination"] == "destination"
        ])),
        "destination_reception_identity": _equivalent([
            (item["event_id"], item["timestamp"], item["payload"])
            for item in record["destination_receptions"]
        ], [
            (item["event_id"], item["timestamp"], item["payload"])
            for item in old["destination_receptions"]
        ]),
    }
    return {
        "arm": record["arm"],
        "historical_arm": historical_arm,
        "character_id": record["character_id"],
        "checks": comparisons,
        "matches": all(comparisons.values()),
        "observed_counts": record["counts"],
        "historical_counts": old["counts"],
    }


def _phase_once() -> dict[str, Any]:
    historical = _historical_results()
    records: dict[str, dict[str, list[dict[str, Any]]]] = {
        arm: {str(seed): [] for seed in SEEDS} for arm in ARMS
    }
    input_digests: dict[str, dict[str, str]] = {arm: {} for arm in ARMS}
    historical_checks: list[dict[str, Any]] = []
    for arm in ARMS:
        for seed in SEEDS:
            sequences = luna39.base._training_point_sequences(seed)
            if len(sequences) != 64:
                raise StopCondition("frozen stream did not produce exactly 64 sequences", {
                    "arm": arm, "seed": seed, "observed": len(sequences),
                })
            for sequence_index, points in enumerate(sequences):
                try:
                    record = _run_character(
                        arm=arm, seed=seed, sequence_index=sequence_index, points=points
                    )
                except StopCondition as error:
                    error.detail.update({
                        "arm": arm,
                        "seed": seed,
                        "sequence_index": sequence_index,
                        "completed_records_in_arm_seed": len(records[arm][str(seed)]),
                    })
                    error.detail["partial_record_counts"] = {
                        key: sum(len(rows) for rows in seed_map.values())
                        for key, seed_map in records.items()
                    }
                    error.detail["partial_records"] = records
                    raise
                record["historical_reconciliation"] = _historical_record_match(record, historical)
                if not record["historical_reconciliation"]["matches"]:
                    raise StopCondition("Luna-42 historical per-character gate failed", {
                        "arm": arm, "seed": seed, "sequence_index": sequence_index,
                        "historical_reconciliation": record["historical_reconciliation"],
                        "failed_record": record,
                        "partial_records": records,
                        "partial_record_counts": {
                            key: sum(len(rows) for rows in seed_map.values())
                            for key, seed_map in records.items()
                        },
                        "partial_records": records,
                    })
                if not record["all_route_reconciliations_pass"]:
                    raise StopCondition("route or canonical-emission provenance failed", {
                        "arm": arm, "seed": seed, "sequence_index": sequence_index,
                        "partial_record_counts": {
                            key: sum(len(rows) for rows in seed_map.values())
                            for key, seed_map in records.items()
                        },
                        "failed_record": record,
                        "partial_records": records,
                    })
                record["record_digest"] = _digest(record)
                records[arm][str(seed)].append(record)
            input_digests[arm][str(seed)] = _digest(
                [item["input_digest"] for item in records[arm][str(seed)]]
            )
    paired = all(
        input_digests[arm][str(seed)] == input_digests[ARMS[0]][str(seed)]
        for arm in ARMS for seed in SEEDS
    )
    if not paired:
        raise StopCondition("matched input digest differs across destination conditions", {
            "input_digests": input_digests,
        })
    relay_arm_invariance = {}
    for seed in SEEDS:
        for sequence_index in range(64):
            matched = [
                records[arm][str(seed)][sequence_index]
                for arm in ARMS
            ]
            signatures = [_relay_signature(record) for record in matched]
            equal = all(signature == signatures[0] for signature in signatures[1:])
            relay_arm_invariance[f"{seed}:{sequence_index}"] = equal
            if not equal:
                raise StopCondition("destination condition changed the frozen relay history", {
                    "seed": seed,
                    "sequence_index": sequence_index,
                    "arm_digests": [_digest(signature) for signature in signatures],
                })

    counts_by_arm = {}
    for arm in ARMS:
        flat = [record for seed in SEEDS for record in records[arm][str(seed)]]
        counts = {
            name: sum(record["counts"][name] for record in flat)
            for name in (
                "source_emissions", "source_to_relay_transfers", "relay_emissions",
                "relay_integrated_emissions", "relay_direct_emissions",
                "relay_to_destination_transfers", "destination_receptions",
                "destination_emissions",
            )
        }
        expected = EXPECTED_HISTORICAL_COUNTS[HISTORICAL_ARM[arm]]
        counts["characters"] = len(flat)
        mismatches = {
            key: {"observed": counts.get(key), "expected": value}
            for key, value in expected.items()
            if counts.get(key) != value
        }
        if mismatches:
            raise StopCondition("aggregate Luna-42 relay gate/counts failed", {
                "arm": arm, "observed": counts, "expected": expected, "mismatches": mismatches,
                "records": records[arm],
            })
        counts["max_abs_destination_z"] = max(
            (
                record["timing_metrics"]["max_abs_destination_z"]
                for record in flat
            ),
            default=0.0,
        )
        counts["max_queue_peak"] = max(
            (record["resource_high_water"]["queue_peak"] for record in flat), default=0
        )
        counts["max_runtime_events"] = max(
            (record["resource_high_water"]["processed_events"] for record in flat), default=0
        )
        counts["max_eligibility_occupancy"] = max(
            (
                ledger["peak"] for record in flat
                for ledger in record["resource_high_water"]["eligibility_ledgers"]
            ),
            default=0,
        )
        counts["max_neuron_events"] = max(
            (
                state["processed_events"]
                for record in flat for state in record["state_at_teardown"].values()
            ),
            default=0,
        )
        counts["route_context_roots_truncated"] = sum(
            record["route_context_roots_truncated"] for record in flat
        )
        counts["historical_per_character_matches"] = sum(
            record["historical_reconciliation"]["matches"] for record in flat
        )
        counts["historical_per_character_total"] = len(flat)
        counts["paired_inputs_match"] = paired
        counts["topology_mutations"] = sum(
            record["topology"] != record["topology_after_character"] for record in flat
        )
        counts["candidate_creations"] = 0
        counts["admissions"] = 0
        counts["pruning_events"] = 0
        counts["relay_spacing"] = _spacing_summary(
            [
                item["delta"]
                for record in flat
                for item in record["timing_metrics"]["relay_emission_spacings"]
            ]
        )
        counts["arrival_spacing"] = _spacing_summary(
            [
                item["delta"]
                for record in flat
                for item in record["timing_metrics"]["relay_to_destination_arrival_spacings"]
            ]
        )
        destination_z_inputs = [
            item["z_before_decay"]
            for record in flat
            for item in record["timing_metrics"]["destination_z_before_input"]
            if item["z_before_decay"] is not None
        ]
        counts["destination_z_before_input"] = {
            "observations": len(destination_z_inputs),
            "minimum": min(destination_z_inputs, default=None),
            "maximum": max(destination_z_inputs, default=None),
        }
        counts["destination_retention_observations"] = sum(
            item["retention_ratio"] is not None
            for record in flat
            for item in record["timing_metrics"]["destination_z_before_input"]
        )
        counts["destination_discharge_records"] = [
            discharge
            for record in flat
            for discharge in record["timing_metrics"]["destination_discharges"]
        ]
        counts_by_arm[arm] = counts

    precursor = _association_scan(records)
    return {
        "selected_decay_rate_z": DECAY_RATE_Z,
        "records": records,
        "input_digests": input_digests,
        "paired_input_invariance": paired,
        "historical_reference_artifact_sha256": _file_sha256(HISTORICAL_RESULTS),
        "historical_reconciliation": {
            "all_character_arm_records_match": all(
                record["historical_reconciliation"]["matches"]
                for arm in ARMS for seed in SEEDS for record in records[arm][str(seed)]
            ),
            "counts": counts_by_arm,
        },
        "relay_arm_invariance": {
            "exact_match": all(relay_arm_invariance.values()),
            "matched_character_count": len(relay_arm_invariance),
            "failed_character_count": sum(not match for match in relay_arm_invariance.values()),
        },
        "association_precursor_scan": precursor,
        "execution_count": sum(
            len(records[arm][str(seed)]) for arm in ARMS for seed in SEEDS
        ),
        "summary": counts_by_arm,
    }


def _relay_signature(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "input_digest": record["input_digest"],
        "source_emissions": record["source_emissions"],
        "relay_emissions": record["relay_emissions"],
        "relay_integration_trace": record["relay_integration_trace"],
        "source_to_relay_routes": [
            item for item in record["routed_events"]
            if item["source"] == "source" and item["destination"] == "relay"
        ],
        "relay_to_destination_routes": [
            item for item in record["routed_events"]
            if item["source"] == "relay" and item["destination"] == "destination"
        ],
    }


def _association_scan(records: dict[str, dict[str, list[dict[str, Any]]]]) -> dict[str, Any]:
    arms: dict[str, Any] = {}
    for arm in ARMS:
        flat = [record for seed in SEEDS for record in records[arm][str(seed)]]
        total_destination_emissions = sum(
            len(record["destination_emissions"]) for record in flat
        )
        if total_destination_emissions == 0:
            arms[arm] = {
                "scan_performed": False,
                "reason": "destination canonical emission prerequisite absent",
                "pair_counts": {
                    "source_to_relay": 0,
                    "relay_to_destination": 0,
                    "source_to_destination": 0,
                    "source_to_destination_missing_edge": 0,
                },
                "unique_stream_opportunities": 0,
                "candidate_precursor_records": [],
            }
            continue
        pair_counts = {
            "source_to_relay": 0,
            "relay_to_destination": 0,
            "source_to_destination": 0,
            "source_to_destination_missing_edge": 0,
        }
        opportunities: set[tuple[int, int]] = set()
        candidate_records = []
        for record in flat:
            emissions = {
                node: sorted(
                    (
                        item for item in record[f"{node}_emissions"]
                    ),
                    key=lambda item: (item["timestamp"], item["event_id"]),
                )
                for node in NODES
            }
            for source, destination, key in (
                ("source", "relay", "source_to_relay"),
                ("relay", "destination", "relay_to_destination"),
                ("source", "destination", "source_to_destination"),
            ):
                for earlier in emissions[source]:
                    for later in emissions[destination]:
                        delta = float(later["timestamp"]) - float(earlier["timestamp"])
                        if 0.0 < delta <= ASSOCIATION_WINDOW:
                            pair_counts[key] += 1
                            if key == "source_to_destination":
                                pair_counts["source_to_destination_missing_edge"] += 1
                                opportunities.add((record["seed"], record["sequence_index"]))
                                candidate_records.append({
                                    "character_id": record["character_id"],
                                    "seed": record["seed"],
                                    "sequence_index": record["sequence_index"],
                                    "source_emitter": "source",
                                    "source_event_id": earlier["event_id"],
                                    "source_timestamp": earlier["timestamp"],
                                    "destination_emitter": "destination",
                                    "destination_event_id": later["event_id"],
                                    "destination_timestamp": later["timestamp"],
                                    "delta": delta,
                                    "association_window": ASSOCIATION_WINDOW,
                                    "direct_edge_present": False,
                                    "classification": "candidate-opportunity precursor only",
                                })
        arms[arm] = {
            "scan_performed": True,
            "reason": "destination canonical emissions present",
            "pair_counts": pair_counts,
            "unique_stream_opportunities": len(opportunities),
            "candidate_precursor_records": candidate_records,
        }
    return {
        "semantics": "existing ACP-0007 ordered canonical-emitter association; 0 < dt <= 4.0",
        "receptions_are_emissions": False,
        "mutation": "none; no candidate created or admitted; topology unchanged",
        "arms": arms,
    }


def _spacing_summary(values: list[float]) -> dict[str, Any]:
    return {
        "observations": len(values),
        "minimum": min(values, default=None),
        "maximum": max(values, default=None),
        "mean": (sum(values) / len(values)) if values else None,
    }


def _summarize_replay(first: dict[str, Any], replay: dict[str, Any]) -> dict[str, Any]:
    first_digest = _digest(first)
    replay_digest = _digest(replay)
    return {
        "initial_digest": first_digest,
        "replay_digest": replay_digest,
        "equal": first_digest == replay_digest,
    }


def run_experiment(
    output_directory: Path = ARTIFACT_DIRECTORY,
    *,
    execution_provenance: dict[str, Any] | None = None,
    validate_execution_environment: bool = True,
) -> tuple[dict[str, Any], dict[str, Any]]:
    output_directory.mkdir(parents=True, exist_ok=True)
    provenance = (
        _collect_provenance() if execution_provenance is None else dict(execution_provenance)
    )
    if not provenance.get("execution_revision") or not provenance.get("execution_repo_revision"):
        raise StopCondition("execution provenance revision fields must be non-null")
    frozen_config = experiment_config()
    config_digest = _digest(frozen_config)
    provenance["config_digest"] = config_digest
    provenance["historical_artifact_sha256"] = frozen_config["historical_reference"]["artifact_sha256"]
    history: dict[str, Any] | None = None
    replay: dict[str, Any] | None = None
    terminal_status = "BLOCKED"
    stop_reason: str | None = None
    try:
        if validate_execution_environment:
            _verify_execution(provenance, "before retained experiment")
        history = _phase_once()
    except StopCondition as error:
        stop_reason = error.reason
        history = {"blocked": {"reason": error.reason, "detail": error.detail}}
        replay_digest = {
            "initial_digest": None,
            "replay_digest": None,
            "equal": False,
            "not_run_after_blocker": True,
        }
    else:
        initial_digest = _digest(history)
        try:
            replay = _phase_once()
        except StopCondition as error:
            stop_reason = error.reason
            replay_digest = {
                "initial_digest": initial_digest,
                "replay_digest": None,
                "equal": False,
                "not_run_after_blocker": False,
                "replay_blocked": {"reason": error.reason, "detail": error.detail},
            }
        else:
            replay_digest = _summarize_replay(history, replay)
            terminal_status = (
                "PASS — bounded mechanism gate"
                if replay_digest["equal"]
                and history["paired_input_invariance"]
                and history["historical_reconciliation"]["all_character_arm_records_match"]
                else "BLOCKED"
            )
            if terminal_status == "BLOCKED":
                stop_reason = "replay, paired-input, or historical relay reconciliation failed"
    if validate_execution_environment:
        _verify_execution(provenance, "completion")
    config_artifact = {
        "schema": "TPCN-LUNA43-ACP0008-DESTINATION-INTEGRATION-CONFIG-1",
        "provenance": provenance,
        "configuration": frozen_config,
        "configuration_digest": config_digest,
    }
    results = {
        "schema": "TPCN-LUNA43-ACP0008-DESTINATION-INTEGRATION-RESULTS-1",
        "provenance": provenance,
        "frozen_configuration": frozen_config,
        "configuration_digest": config_digest,
        "terminal_status": terminal_status,
        "stop_reason": stop_reason,
        "first_run": history,
        "replay_run_digest": replay_digest,
        "interpretation_boundary": (
            "Mechanism-only. No classification, accuracy, efficacy, prediction improvement, "
            "reward, utility, energy benefit, structural-growth benefit, hardware equivalence, "
            "ACP promotion, WEMA, or Luna-44 authorization is claimed."
        ),
    }
    replay_artifact = {
        "schema": "TPCN-LUNA43-REPLAY-DIGEST-1",
        "provenance": provenance,
        "frozen_configuration": frozen_config,
        "configuration_digest": config_digest,
        "whole_experiment_initial_digest": replay_digest["initial_digest"],
        "whole_experiment_replay_digest": replay_digest["replay_digest"],
        "equal": replay_digest["equal"],
        "replay_run_digest": replay_digest,
    }
    config_artifact["artifact_digest"] = _artifact_digest(config_artifact)
    results["artifact_digest"] = _artifact_digest(results)
    replay_artifact["artifact_digest"] = _artifact_digest(replay_artifact)
    summary = {
        "schema": "TPCN-LUNA43-ACP0008-DESTINATION-INTEGRATION-SUMMARY-1",
        "provenance": provenance,
        "frozen_configuration": frozen_config,
        "configuration_digest": config_digest,
        "terminal_status": terminal_status,
        "stop_reason": stop_reason,
        "arm_summary": (
            history.get("summary") if history is not None and "summary" in history else None
        ),
        "association_precursor_scan": (
            history.get("association_precursor_scan")
            if history is not None and "association_precursor_scan" in history else None
        ),
        "replay": replay_digest,
        "results_digest": results["artifact_digest"],
        "replay_artifact_digest": replay_artifact["artifact_digest"],
    }
    summary["artifact_digest"] = _artifact_digest(summary)
    aggregate_digest = _digest({
        "config.json": config_artifact["artifact_digest"],
        "results.json": results["artifact_digest"],
        "summary.json": summary["artifact_digest"],
        "replay.json": replay_artifact["artifact_digest"],
    })
    for artifact in (config_artifact, results, summary, replay_artifact):
        artifact["aggregate_run_digest"] = aggregate_digest
        artifact["artifact_digest"] = _artifact_digest(artifact)
    for name, artifact in (
        ("config.json", config_artifact),
        ("results.json", results),
        ("summary.json", summary),
        ("replay.json", replay_artifact),
    ):
        (output_directory / name).write_text(_canonical_json(artifact) + "\n", encoding="utf-8")
    return results, summary


if __name__ == "__main__":
    try:
        _, final_summary = run_experiment()
    except StopCondition as error:
        print(_canonical_json({
            "terminal_status": "BLOCKED",
            "stop_reason": error.reason,
            "detail": error.detail,
        }))
        raise SystemExit(2) from error
    print(_canonical_json(final_summary))
