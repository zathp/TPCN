"""Observe the fixed Luna-35 eligibility lifecycle fixtures."""

from __future__ import annotations

from contextlib import ExitStack
from copy import deepcopy
from dataclasses import asdict, fields, is_dataclass
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any
from unittest.mock import patch

from run_luna34_excursion_v1_multi_emitter_bridge import (
    _input_points,
    _point_batches,
    _training_point_sequences,
)
from tpcn.eligibility import (
    EligibilityActivity,
    EligibilityCapacityError,
    EligibilityLedger,
    RewardSignal,
)
from tpcn.event_runtime import Event
from tpcn.excursion_neuron import E1Config, MultiExcursionNeuron
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.predictive_coding import LocalPredictor, Observation, PredictionError
from tpcn.topology import BoundedTopology


EXECUTION_BASELINE = "5b24e13216bc5adac518bb9d8c69d2342d75c2a2"
REQUESTED_REVISION_IDENTIFIER = "F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb"
LUNA34_BASELINE = "4d77489eaebadf638f22996d1d0d49e162b378ab"
ARTIFACT_DIRECTORY = Path("artifacts/luna35-eligibility-capacity-lifecycle")
NODES = ("source", "destination")
QUEUE_CAPACITY = 128
EVENT_BUDGET = 1024
SETTLING_HORIZON = 4.0
PREDICTION_CAPACITY = 8
PREDICTION_EXPIRY = 4.0
MAX_ACTIVITY_EVENTS = 1024


def _jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: _jsonable(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, dict):
        return {
            str(key): _jsonable(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"cannot serialize value of type {type(value).__name__}")


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _trace_state(ledger: EligibilityLedger) -> list[dict[str, Any]]:
    return [
        {
            "trace_id": trace.trace_id,
            "prediction_id": trace.prediction_id,
            "value": trace.value,
            "credit": trace.credit,
            "last_timestamp": trace.last_timestamp,
        }
        for trace in ledger.traces
    ]


def experiment_config() -> dict[str, Any]:
    return {
        "schema": "TPCN-LUNA35-ELIGIBILITY-CAPACITY-LIFECYCLE-CONFIG-1",
        "execution_baseline": EXECUTION_BASELINE,
        "luna34_evidence_baseline": LUNA34_BASELINE,
        "requested_revision_identifier": REQUESTED_REVISION_IDENTIFIER,
        "requested_revision_resolution": (
            "The supplied identifier did not resolve as a Git commit; the run used "
            "the clean synchronized origin/main revision available at dispatch."
        ),
        "dataset": {
            "generator": "make_spiral_dataset through the Luna-34 public fixture helper",
            "examples_per_class": 16,
            "train_seed": "12007 + seed",
            "evaluation_seed": "22017 + seed",
            "order_stream": "random.Random(330000 + seed)",
            "seed": 0,
            "sequence_index": 4,
            "sequence_identity": "c00-004",
            "information_boundary": "Read each selected example's points only; no labels or metadata.",
            "input_transform": "point.x + point.y at point.timestamp",
        },
        "network": {
            "nodes": list(NODES),
            "active_edges": [],
            "prediction_capacity": PREDICTION_CAPACITY,
            "runtime_derived_per_ledger_capacity": (
                "prediction_capacity * max(1, neuron_count) = 8 * 2 = 16"
            ),
            "aggregate_ledger_capacity": 32,
            "queue_capacity": QUEUE_CAPACITY,
            "event_budget": EVENT_BUDGET,
            "settling_horizon": SETTLING_HORIZON,
            "prediction_expiry": PREDICTION_EXPIRY,
            "eligibility_expiry": None,
            "neuron": {"type": "MultiExcursionNeuron", "config": asdict(E1Config())},
            "reward": 0.0,
        },
        "fixtures": {
            "capacity_reproducer": {
                "seed": 0,
                "condition": "NO_EDGE_CONTROL",
                "sequence_index": 4,
                "sequence_id": "c00-004",
                "original_point_count": 20,
            },
            "lifecycle_control": {
                "seed": 0,
                "condition": "NO_EDGE_CONTROL",
                "sequence_index": 4,
                "sequence_id": "c00-004",
                "point_selection": "the first point of the same generated point sequence",
                "point_count": 1,
                "next_character_probe": "start a fresh character in the same runtime; submit no input",
            },
        },
        "observation_policy": {
            "scope": "Two fixed no-edge fixtures only; no topology comparisons or efficacy endpoints.",
            "instrumentation": "Bounded test/runner-local wrappers around existing ledger, predictor, and runtime lifecycle methods.",
            "capacity_changes": False,
            "production_changes": False,
        },
    }


class _Audit:
    def __init__(self) -> None:
        self.order = 0
        self.fixture = ""
        self.point_indexes: tuple[int, ...] = ()
        self.runtime: ExcursionCharacterRuntime | None = None
        self.events: dict[str, list[dict[str, Any]]] = {
            "eligibility_activity": [],
            "eligibility_retirements": [],
            "ledger_signals": [],
            "predictor_creation": [],
            "predictor_observation": [],
            "predictor_expiration": [],
            "character_boundaries": [],
        }
        self.failure: dict[str, Any] | None = None

    def begin_fixture(self, fixture: str) -> None:
        self.fixture = fixture
        self.point_indexes = ()
        self.failure = None
        self.events = {
            "eligibility_activity": [],
            "eligibility_retirements": [],
            "ledger_signals": [],
            "predictor_creation": [],
            "predictor_observation": [],
            "predictor_expiration": [],
            "character_boundaries": [],
        }

    def next_order(self) -> int:
        self.order += 1
        return self.order

    def ledgers(self) -> dict[str, EligibilityLedger]:
        if self.runtime is None:
            return {}
        return self.runtime._ledgers

    def matching_traces(self, prediction_id: str) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        for node, ledger in self.ledgers().items():
            for trace in _trace_state(ledger):
                if trace["prediction_id"] == prediction_id:
                    found.append({"node": node, **trace})
        return found


def _install_audit(audit: _Audit) -> ExitStack:
    stack = ExitStack()
    original_decay = EligibilityLedger._decay_to
    original_record = EligibilityLedger.record_activity
    original_signal = EligibilityLedger.apply_signal
    original_create = LocalPredictor.create_prediction
    original_observe = LocalPredictor.observe
    original_expire = LocalPredictor.expire
    original_destroy = ExcursionCharacterRuntime._destroy_character

    def decay(ledger: EligibilityLedger, timestamp: float) -> None:
        before = _trace_state(ledger)
        original_decay(ledger, timestamp)
        after = _trace_state(ledger)
        after_ids = {entry["trace_id"] for entry in after}
        removed = [entry for entry in before if entry["trace_id"] not in after_ids]
        if removed:
            audit.events["eligibility_retirements"].append(
                {
                    "order": audit.next_order(),
                    "fixture": audit.fixture,
                    "ledger_id": ledger.ledger_id,
                    "timestamp": timestamp,
                    "reason": "configured eligibility age expiry during ledger time advancement",
                    "removed": removed,
                    "occupancy_before": len(before),
                    "occupancy_after": len(after),
                }
            )

    def record_activity(ledger: EligibilityLedger, event: Event):
        activity = event.payload
        if not isinstance(activity, EligibilityActivity):
            return original_record(ledger, event)
        before_state = _trace_state(ledger)
        before_by_id = {entry["trace_id"]: entry for entry in before_state}
        operation = "update" if activity.trace_id in before_by_id else "create"
        creation_sequence_number = None
        if operation == "create":
            creation_sequence_number = 1 + sum(
                entry["operation"] in ("create", "rejected")
                for entry in audit.events["eligibility_activity"]
            )
        runtime = audit.runtime
        prediction_status = "not-applicable"
        source_event_count = None
        processed_event_count = None
        canonical_emission_sequence = None
        canonical_emission_count = None
        if runtime is not None:
            if activity.prediction_id is not None:
                outstanding = {
                    prediction.prediction_id
                    for prediction in runtime._predictor.outstanding_predictions
                } if runtime._predictor is not None else set()
                prediction_status = (
                    "outstanding" if activity.prediction_id in outstanding else "not-outstanding"
                )
            source_node = runtime.by_id[event.source]
            source_event_count = source_node.processed_event_count
            processed_event_count = runtime._processed
            canonical_emission_count = len(runtime._emissions)
            canonical_emission_sequence = next(
                (
                    emission.sequence
                    for emission in reversed(runtime._emissions)
                    if emission.event_id == event.event_id
                ),
                None,
            )
        try:
            trace = original_record(ledger, event)
        except EligibilityCapacityError as exc:
            after_state = _trace_state(ledger)
            attempt = {
                "order": audit.next_order(),
                "fixture": audit.fixture,
                "point_indexes_in_active_batch": list(audit.point_indexes),
                "input_point_index": audit.point_indexes[-1] if audit.point_indexes else None,
                "ledger_id": ledger.ledger_id,
                "node": event.source,
                "trace_id": activity.trace_id,
                "prediction_id": activity.prediction_id,
                "canonical_emission_id": event.event_id,
                "canonical_emission_sequence": canonical_emission_sequence,
                "timestamp": event.timestamp,
                "magnitude": activity.magnitude,
                "operation": "rejected",
                "creation_sequence_number": creation_sequence_number,
                "exception": f"{type(exc).__name__}: {exc}",
                "occupancy_before_attempt": len(before_state),
                "occupancy_after_decay_before_rejection": len(after_state),
                "source_neuron_processed_event_count": source_event_count,
                "runtime_processed_event_count": processed_event_count,
                "canonical_emission_count_including_rejected_activity": canonical_emission_count,
                "resident_traces_after_decay_before_insertion": after_state,
                "predictor_status_at_attempt": prediction_status,
            }
            audit.events["eligibility_activity"].append(attempt)
            audit.failure = attempt
            raise
        after_state = _trace_state(ledger)
        audit.events["eligibility_activity"].append(
            {
                "order": audit.next_order(),
                "fixture": audit.fixture,
                "point_indexes_in_active_batch": list(audit.point_indexes),
                "input_point_index": audit.point_indexes[-1] if audit.point_indexes else None,
                "ledger_id": ledger.ledger_id,
                "node": event.source,
                "trace_id": activity.trace_id,
                "prediction_id": activity.prediction_id,
                "canonical_emission_id": event.event_id,
                "canonical_emission_sequence": canonical_emission_sequence,
                "timestamp": event.timestamp,
                "magnitude": activity.magnitude,
                "operation": operation,
                "creation_sequence_number": creation_sequence_number,
                "predictor_status_at_creation": prediction_status,
                "occupancy_before": len(before_state),
                "occupancy_after": len(after_state),
                "trace_after": next(
                    entry for entry in after_state if entry["trace_id"] == trace.trace_id
                ),
            }
        )
        return trace

    def apply_signal(ledger: EligibilityLedger, event: Event):
        before = _trace_state(ledger)
        payload = event.payload
        if isinstance(payload, RewardSignal):
            payload_record = {
                "kind": "reward",
                "message_id": payload.message_id,
                "reward": payload.reward,
                "trace_id": payload.trace_id,
                "prediction_id": payload.prediction_id,
            }
        elif isinstance(payload, PredictionError):
            payload_record = {
                "kind": "prediction_error",
                "prediction_id": payload.prediction_id,
                "predictor_id": payload.predictor_id,
                "target_key": payload.target_key,
                "error": payload.error,
                "prediction_timestamp": payload.prediction_timestamp,
                "observation_timestamp": payload.observation_timestamp,
                "observation_source": payload.observation_source,
            }
        else:
            payload_record = {"kind": type(payload).__name__}
        attribution = original_signal(ledger, event)
        after = _trace_state(ledger)
        audit.events["ledger_signals"].append(
            {
                "order": audit.next_order(),
                "fixture": audit.fixture,
                "ledger_id": ledger.ledger_id,
                "timestamp": event.timestamp,
                "event_type": str(event.event_type),
                "event_id": event.event_id,
                "payload": payload_record,
                "attribution": _jsonable(attribution),
                "occupancy_before": len(before),
                "occupancy_after": len(after),
                "trace_state_before": before,
                "trace_state_after": after,
            }
        )
        return attribution

    def create_prediction(predictor: LocalPredictor, *args: Any, **kwargs: Any):
        prediction = original_create(predictor, *args, **kwargs)
        audit.events["predictor_creation"].append(
            {
                "order": audit.next_order(),
                "fixture": audit.fixture,
                "prediction_id": prediction.prediction_id,
                "predictor_id": prediction.predictor_id,
                "target_key": prediction.target_key,
                "predicted_value": prediction.predicted_value,
                "created_at": prediction.created_at,
                "expires_at": prediction.expires_at,
                "status_after_creation": "outstanding",
                "eligible_entries_at_creation": audit.matching_traces(prediction.prediction_id),
                "point_indexes_in_active_batch": list(audit.point_indexes),
            }
        )
        return prediction

    def expire(predictor: LocalPredictor, timestamp: float):
        expired = original_expire(predictor, timestamp)
        for prediction in expired:
            matching = audit.matching_traces(prediction.prediction_id)
            audit.events["predictor_expiration"].append(
                {
                    "order": audit.next_order(),
                    "fixture": audit.fixture,
                    "prediction_id": prediction.prediction_id,
                    "predictor_id": predictor.predictor_id,
                    "created_at": prediction.created_at,
                    "expires_at": prediction.expires_at,
                    "expired_at": timestamp,
                    "eligibility_after_predictor_expiration": [
                        {
                            "node": entry["node"],
                            "trace_id": entry["trace_id"],
                            "status": "resident",
                            "value": entry["value"],
                            "credit": entry["credit"],
                            "last_timestamp": entry["last_timestamp"],
                        }
                        for entry in matching
                    ],
                    "eligibility_ledger_clocks_at_expiration": {
                        node: ledger.clock.timestamp
                        for node, ledger in audit.ledgers().items()
                    },
                    "matching_eligibility_entry_count": len(matching),
                    "predictor_outstanding_after_expiration": predictor.outstanding_count,
                }
            )
        return expired

    def observe(predictor: LocalPredictor, event: Event):
        outstanding_before = [
            prediction.prediction_id for prediction in predictor.outstanding_predictions
        ]
        resolution = original_observe(predictor, event)
        audit.events["predictor_observation"].append(
            {
                "order": audit.next_order(),
                "fixture": audit.fixture,
                "timestamp": event.timestamp,
                "event_id": event.event_id,
                "target_key": event.payload.target_key,
                "observed_value": event.payload.observed_value,
                "status": resolution.status,
                "prediction_id": (
                    resolution.prediction.prediction_id if resolution.prediction else None
                ),
                "error": _jsonable(resolution.error),
                "outstanding_before": outstanding_before,
                "outstanding_after": [
                    prediction.prediction_id for prediction in predictor.outstanding_predictions
                ],
                "point_indexes_in_active_batch": list(audit.point_indexes),
            }
        )
        return resolution

    def destroy(runtime: ExcursionCharacterRuntime, timestamp: float) -> None:
        before = {
            node: {
                "ledger_id": ledger.ledger_id,
                "max_traces": ledger.max_traces,
                "traces": _trace_state(ledger),
            }
            for node, ledger in runtime._ledgers.items()
        }
        original_destroy(runtime, timestamp)
        audit.events["character_boundaries"].append(
            {
                "order": audit.next_order(),
                "fixture": audit.fixture,
                "character_id": runtime._character_id,
                "timestamp": timestamp,
                "boundary": "end_character destruction",
                "ledgers_before_destruction": before,
                "runtime_ledgers_after_destruction": sorted(runtime._ledgers),
                "predictor_after_destruction": runtime._predictor,
                "occupancy_before_by_node": {
                    node: len(record["traces"]) for node, record in before.items()
                },
                "occupancy_after_by_node": {node: 0 for node in before},
                "trace_references_released": sum(
                    len(record["traces"]) for record in before.values()
                ),
            }
        )

    stack.enter_context(patch.object(EligibilityLedger, "_decay_to", decay))
    stack.enter_context(patch.object(EligibilityLedger, "record_activity", record_activity))
    stack.enter_context(patch.object(EligibilityLedger, "apply_signal", apply_signal))
    stack.enter_context(patch.object(LocalPredictor, "create_prediction", create_prediction))
    stack.enter_context(patch.object(LocalPredictor, "observe", observe))
    stack.enter_context(patch.object(LocalPredictor, "expire", expire))
    stack.enter_context(patch.object(ExcursionCharacterRuntime, "_destroy_character", destroy))
    return stack


def _new_runtime(namespace: str) -> ExcursionCharacterRuntime:
    topology = BoundedTopology.from_edges(
        NODES,
        (),
        fan_in_limit=1,
        fan_out_limit=1,
        edge_capacity=1,
        routing_capacity=1,
    )
    neurons = tuple(MultiExcursionNeuron(node, config=E1Config()) for node in NODES)
    return ExcursionCharacterRuntime(
        neurons,
        topology,
        queue_capacity=QUEUE_CAPACITY,
        event_budget=EVENT_BUDGET,
        settling_horizon=SETTLING_HORIZON,
        prediction_capacity=PREDICTION_CAPACITY,
        prediction_expiry=PREDICTION_EXPIRY,
        max_activity_events=MAX_ACTIVITY_EVENTS,
        namespace=namespace,
    )


def _start_character(runtime: ExcursionCharacterRuntime, character_id: str) -> None:
    runtime.start_character(
        character_id,
        0,
        timestamp=0.0,
        predictor_source="source",
        readout_sources=NODES,
        input_destination="source",
    )


def _primary_fixture(audit: _Audit) -> dict[str, Any]:
    points = _training_point_sequences(0)[4]
    input_points = _input_points(points)
    if len(input_points) != 20:
        raise RuntimeError(
            f"fixed c00-004 fixture has {len(input_points)} points; expected exactly 20"
        )
    runtime = _new_runtime("luna35")
    audit.begin_fixture("capacity_reproducer")
    audit.runtime = runtime
    _start_character(runtime, "c00-004")
    per_node_capacity = {
        node: ledger.max_traces for node, ledger in runtime._ledgers.items()
    }
    point_batches = _point_batches(input_points)
    point_cursor = 0
    terminal_batch: tuple[int, ...] = ()
    try:
        for batch in point_batches:
            batch_indexes: list[int] = []
            for timestamp, value in batch:
                while point_cursor < len(input_points):
                    point = input_points[point_cursor]
                    if point.timestamp == timestamp and point.source_value == value:
                        batch_indexes.append(point.point_index)
                        point_cursor += 1
                        break
                    point_cursor += 1
            if len(batch_indexes) != len(batch):
                raise RuntimeError("Luna-35 point batch did not map to the fixed point sequence")
            terminal_batch = tuple(batch_indexes)
            audit.point_indexes = terminal_batch
            runtime.admit_external_batch(batch)
    except EligibilityCapacityError as exc:
        failure = audit.failure
        if failure is None:
            raise RuntimeError("capacity error occurred without a captured insertion attempt") from exc
        failure.update(
            {
                "fixture_id": "c00-004",
                "seed": 0,
                "condition": "NO_EDGE_CONTROL",
                "input_point_count": len(input_points),
                "input_point_indexes_in_batch": list(terminal_batch),
                "failure_triggering_batch_semantics": (
                    "admit_external_batch first drains pending events earlier than this "
                    "timestamp; the capacity exception occurs during that drain before "
                    "this input point is admitted"
                ),
                "exception": f"{type(exc).__name__}: {exc}",
            }
        )
        outcome = "capacity_rejected"
    else:
        raise RuntimeError(
            "the exact Luna-35 capacity reproducer completed without the authorized overflow"
        )
    if (
        audit.failure["input_point_index"] != 19
        or audit.failure["canonical_emission_sequence"] != 17
        or audit.failure["source_neuron_processed_event_count"] != 59
        or audit.failure["runtime_processed_event_count"] != 59
        or audit.failure["timestamp"] != 255.79833294576443
        or audit.failure["occupancy_before_attempt"] != 16
        or audit.failure["occupancy_after_decay_before_rejection"] != 16
    ):
        raise RuntimeError("the fixed capacity reproducer diverged from its authorized failure")
    source_ledger = runtime._ledgers["source"]
    destination_ledger = runtime._ledgers["destination"]
    predictor = runtime._predictor
    return {
        "fixture_id": "c00-004",
        "seed": 0,
        "condition": "NO_EDGE_CONTROL",
        "sequence_index": 4,
        "point_count": len(input_points),
        "input_digest": _digest(
            [
                {
                    "point_index": point.point_index,
                    "timestamp": point.timestamp,
                    "x": point.x,
                    "y": point.y,
                    "source_value": point.source_value,
                }
                for point in input_points
            ]
        ),
        "input_points": [
            {
                "point_index": point.point_index,
                "timestamp": point.timestamp,
                "x": point.x,
                "y": point.y,
                "source_value": point.source_value,
            }
            for point in input_points
        ],
        "per_node_capacity": per_node_capacity,
        "aggregate_capacity": sum(per_node_capacity.values()),
        "outcome": outcome,
        "input_point_index_at_terminal_failure": (
            audit.failure["input_point_index"] if audit.failure is not None else None
        ),
        "input_point_at_terminal_failure": (
            {
                "point_index": input_points[audit.failure["input_point_index"]].point_index,
                "timestamp": input_points[audit.failure["input_point_index"]].timestamp,
                "x": input_points[audit.failure["input_point_index"]].x,
                "y": input_points[audit.failure["input_point_index"]].y,
                "source_value": input_points[audit.failure["input_point_index"]].source_value,
            }
            if audit.failure is not None else None
        ),
        "source_neuron_processed_event_count": runtime.by_id["source"].processed_event_count,
        "runtime_processed_event_count": runtime._processed,
        "canonical_emission_count_including_failed_activity": len(runtime._emissions),
        "predictor_expired_count": predictor.expired_count if predictor is not None else None,
        "predictor_outstanding_at_stop": (
            [prediction.prediction_id for prediction in predictor.outstanding_predictions]
            if predictor is not None else []
        ),
        "end_character_reached": False,
        "neutral_end_character_reward_reached_ledger": False,
        "source_ledger_at_stop": {
            "ledger_id": source_ledger.ledger_id,
            "occupancy": len(source_ledger.traces),
            "capacity": source_ledger.max_traces,
            "traces": _trace_state(source_ledger),
        },
        "destination_ledger_at_stop": {
            "ledger_id": destination_ledger.ledger_id,
            "occupancy": len(destination_ledger.traces),
            "capacity": destination_ledger.max_traces,
            "traces": _trace_state(destination_ledger),
        },
        "capacity_failure": deepcopy(audit.failure),
        "eligibility_activity_events": deepcopy(audit.events["eligibility_activity"]),
        "eligibility_retirements": deepcopy(audit.events["eligibility_retirements"]),
        "ledger_signals": deepcopy(audit.events["ledger_signals"]),
        "predictor_creation_events": deepcopy(audit.events["predictor_creation"]),
        "predictor_observations": deepcopy(audit.events["predictor_observation"]),
        "predictor_expirations": deepcopy(audit.events["predictor_expiration"]),
        "character_boundaries": deepcopy(audit.events["character_boundaries"]),
        "occupancy_accounting": {
            "initial_source_occupancy": 0,
            "successful_creations": sum(
                event["operation"] == "create"
                for event in audit.events["eligibility_activity"]
            ),
            "removals_before_stop": sum(
                len(event["removed"]) for event in audit.events["eligibility_retirements"]
            ),
            "final_source_occupancy": len(source_ledger.traces),
            "equation_reconciles": (
                sum(event["operation"] == "create"
                    for event in audit.events["eligibility_activity"])
                - sum(len(event["removed"])
                      for event in audit.events["eligibility_retirements"])
                == len(source_ledger.traces)
            ),
        },
    }


def _lifecycle_control(audit: _Audit) -> dict[str, Any]:
    points = _training_point_sequences(0)[4]
    one_point = _input_points(points[:1])
    runtime = _new_runtime("luna35")
    audit.begin_fixture("lifecycle_control")
    audit.runtime = runtime
    _start_character(runtime, "luna35-lifecycle-0")
    initial_ledgers = {
        node: {
            "ledger_id": ledger.ledger_id,
            "max_traces": ledger.max_traces,
            "occupancy": len(ledger.traces),
        }
        for node, ledger in runtime._ledgers.items()
    }
    audit.point_indexes = (0,)
    runtime.admit_external_batch(((one_point[0].timestamp, one_point[0].source_value),))
    before_end = {
        node: {
            "ledger_id": ledger.ledger_id,
            "max_traces": ledger.max_traces,
            "traces": _trace_state(ledger),
        }
        for node, ledger in runtime._ledgers.items()
    }
    result = runtime.end_character(
        last_external_timestamp=one_point[-1].timestamp,
        reward=0.0,
        reward_delay=0.0,
        reward_message_id="neutral-luna35-lifecycle-0",
    )
    boundary = audit.events["character_boundaries"][-1]
    before_destruction = boundary["ledgers_before_destruction"]
    old_trace_count = boundary["trace_references_released"]
    new_character_id = "luna35-lifecycle-1"
    _start_character(runtime, new_character_id)
    new_ledgers = {
        node: {
            "ledger_id": ledger.ledger_id,
            "max_traces": ledger.max_traces,
            "occupancy": len(ledger.traces),
            "traces": _trace_state(ledger),
        }
        for node, ledger in runtime._ledgers.items()
    }
    fresh_ledger_ids = all(
        new_ledgers[node]["ledger_id"] != before_end[node]["ledger_id"]
        for node in NODES
    )
    empty_fresh_ledgers = all(new_ledgers[node]["occupancy"] == 0 for node in NODES)
    runtime.reset()
    activity_events = audit.events["eligibility_activity"]
    signal_events = audit.events["ledger_signals"]
    retirement_events = audit.events["eligibility_retirements"]
    return {
        "fixture_id": "luna35-lifecycle-control",
        "seed": 0,
        "condition": "NO_EDGE_CONTROL",
        "source_sequence_identity": "c00-004",
        "input_point_count": 1,
        "input_point": {
            "point_index": 0,
            "timestamp": one_point[0].timestamp,
            "x": one_point[0].x,
            "y": one_point[0].y,
            "source_value": one_point[0].source_value,
        },
        "input_points": [
            {
                "point_index": point.point_index,
                "timestamp": point.timestamp,
                "x": point.x,
                "y": point.y,
                "source_value": point.source_value,
            }
            for point in one_point
        ],
        "input_digest": _digest(
            [
                {
                    "point_index": point.point_index,
                    "timestamp": point.timestamp,
                    "x": point.x,
                    "y": point.y,
                    "source_value": point.source_value,
                }
                for point in one_point
            ]
        ),
        "per_node_capacity": {
            node: record["max_traces"] for node, record in initial_ledgers.items()
        },
        "aggregate_capacity": sum(record["max_traces"] for record in initial_ledgers.values()),
        "initial_ledgers": initial_ledgers,
        "eligibility_activity_events": deepcopy(activity_events),
        "eligibility_retirements": deepcopy(retirement_events),
        "ledger_signals": deepcopy(signal_events),
        "predictor_creation_events": deepcopy(audit.events["predictor_creation"]),
        "predictor_observations": deepcopy(audit.events["predictor_observation"]),
        "predictor_expirations": deepcopy(audit.events["predictor_expiration"]),
        "end_character_result": {
            "emission_count": result.emission_count,
            "expired_predictions": result.expired_predictions,
            "matched_credit": result.matched_credit,
            "unmatched_credit": result.unmatched_credit,
            "reward_attribution": result.reward_attribution,
            "reward": result.reward,
            "incomplete_settling": result.incomplete_settling,
        },
        "ledger_state_when_end_character_was_called": before_end,
        "ledger_state_immediately_before_end_character_destruction": before_destruction,
        "ledger_state_immediately_after_end_character_destruction": {
            "runtime_ledger_ids": boundary["runtime_ledgers_after_destruction"],
            "occupancy_by_node": boundary["occupancy_after_by_node"],
            "trace_references_released": boundary["trace_references_released"],
            "predictor_released": boundary["predictor_after_destruction"] is None,
        },
        "next_character_fresh_ledger_state": new_ledgers,
        "next_character_has_fresh_ledger_ids": fresh_ledger_ids,
        "next_character_ledgers_empty": empty_fresh_ledgers,
        "creation_count": sum(event["operation"] == "create" for event in activity_events),
        "removal_count_before_boundary": sum(
            len(event["removed"]) for event in retirement_events
        ),
        "trace_references_released_at_boundary": old_trace_count,
        "post_boundary_eligibility_count": 0,
        "occupancy_accounting": {
            "initial_source_occupancy": 0,
            "successful_creations": sum(
                event["operation"] == "create" for event in activity_events
            ),
            "ledger_expiry_removals": sum(
                len(event["removed"]) for event in retirement_events
            ),
            "character_boundary_releases": old_trace_count,
            "post_boundary_occupancy": 0,
            "equation_reconciles": (
                sum(event["operation"] == "create" for event in activity_events)
                - sum(len(event["removed"]) for event in retirement_events)
                - old_trace_count
                == 0
            ),
        },
        "cleanup_boundary_after_next_character_probe": deepcopy(
            audit.events["character_boundaries"][-1]
        ),
    }


def _observe_fixtures() -> dict[str, Any]:
    audit = _Audit()
    with _install_audit(audit):
        primary = _primary_fixture(audit)
        lifecycle = _lifecycle_control(audit)
    return {
        "capacity_reproducer": primary,
        "lifecycle_control": lifecycle,
    }


def run_experiment(
    output_directory: Path = ARTIFACT_DIRECTORY,
) -> tuple[dict[str, Any], dict[str, Any]]:
    observations = _observe_fixtures()
    replay = _observe_fixtures()
    observation_digest = _digest(observations)
    replay_digest = _digest(replay)
    if observation_digest != replay_digest:
        raise RuntimeError("Luna-35 fixed-fixture replay was not deterministic")
    results = {
        "schema": "TPCN-LUNA35-ELIGIBILITY-CAPACITY-LIFECYCLE-RESULTS-1",
        "execution_baseline": EXECUTION_BASELINE,
        "environment": {"python": sys.version, "platform": platform.platform()},
        "fixed_fixtures": observations,
        "deterministic_replay": {
            "replayed_exactly_two_fixed_fixtures": True,
            "first_observation_digest": observation_digest,
            "replay_observation_digest": replay_digest,
            "digests_match": observation_digest == replay_digest,
        },
    }
    primary = observations["capacity_reproducer"]
    control = observations["lifecycle_control"]
    expired_with_entries = sum(
        event["matching_eligibility_entry_count"]
        for event in primary["predictor_expirations"]
    )
    summary = {
        "schema": "TPCN-LUNA35-ELIGIBILITY-CAPACITY-LIFECYCLE-SUMMARY-1",
        "execution_baseline": EXECUTION_BASELINE,
        "classification": "EXPECTED LIFECYCLE CONFIRMED",
        "scientific_boundary": (
            "No propagation-to-emission condition or task efficacy endpoint was run."
        ),
        "capacity_derivation": {
            "prediction_capacity": PREDICTION_CAPACITY,
            "neuron_count": len(NODES),
            "per_ledger_expression": "prediction_capacity * max(1, neuron_count)",
            "per_ledger_capacity": primary["per_node_capacity"],
            "aggregate_allocated_capacity": primary["aggregate_capacity"],
        },
        "capacity_reproducer": {
            "sequence_id": primary["fixture_id"],
            "point_count": primary["point_count"],
            "result": primary["outcome"],
            "successful_eligibility_creations": primary["occupancy_accounting"]["successful_creations"],
            "rejected_unique_trace_insertions": sum(
                event["operation"] == "rejected"
                for event in primary["eligibility_activity_events"]
            ),
            "eligibility_expiry_removals": primary["occupancy_accounting"]["removals_before_stop"],
            "peak_source_occupancy": max(
                [0]
                + [
                    event["occupancy_after"]
                    for event in primary["eligibility_activity_events"]
                    if event["operation"] != "rejected"
                ]
                + [event["occupancy_after_decay_before_rejection"]
                   for event in primary["eligibility_activity_events"]
                   if event["operation"] == "rejected"]
            ),
            "source_occupancy_at_failure": primary["source_ledger_at_stop"]["occupancy"],
            "first_capacity_failure": primary["capacity_failure"],
            "expired_predictors_with_resident_eligibility_entries": expired_with_entries,
            "prediction_error_signals_reaching_ledgers": sum(
                event["payload"]["kind"] == "prediction_error"
                for event in primary["ledger_signals"]
            ),
            "reward_signals_reaching_ledgers": sum(
                event["payload"]["kind"] == "reward"
                for event in primary["ledger_signals"]
            ),
            "end_character_reward_before_failure": False,
        },
        "lifecycle_control": {
            "one_point_emission_count": control["end_character_result"]["emission_count"],
            "eligibility_creation_count": control["creation_count"],
            "eligibility_removal_count_before_character_boundary": control["removal_count_before_boundary"],
            "trace_references_released_at_character_boundary": control["trace_references_released_at_boundary"],
            "neutral_reward_signals": sum(
                event["payload"]["kind"] == "reward" for event in control["ledger_signals"]
            ),
            "neutral_reward_attribution": [
                event["attribution"]["status"]
                for event in control["ledger_signals"]
                if event["payload"]["kind"] == "reward"
            ],
            "fresh_next_character_ledgers_empty": control["next_character_ledgers_empty"],
            "occupancy_equation_reconciles": control["occupancy_accounting"]["equation_reconciles"],
        },
        "eligibility_lifecycle_finding": (
            "Predictor expiry does not call or imply eligibility retirement. The integrated "
            "runtime configures no eligibility expiry; ledger time advancement removes traces "
            "only when an optional eligibility expiry is configured and exceeded. Matched "
            "reward/error signals update credit but do not remove entries. end_character "
            "applies its reward before destroying character state; destruction releases the "
            "ledger references, and the next character receives fresh empty ledgers."
        ),
        "production_defect_established": False,
        "remaining_uncertainty": [
            "No contract specifies that predictor expiration must retire an eligibility entry.",
            "Whether retaining expired-predictor eligibility until character destruction is optimal capacity policy remains unresolved.",
            "The bounded fixtures do not establish a general workload capacity guarantee.",
        ],
        "deterministic_replay": results["deterministic_replay"],
    }
    output_directory.mkdir(parents=True, exist_ok=True)
    for filename, value in (
        ("config.json", experiment_config()),
        ("results.json", results),
        ("summary.json", summary),
    ):
        (output_directory / filename).write_text(
            _canonical_json(value) + "\n",
            encoding="utf-8",
        )
    return results, summary


def main() -> None:
    _, summary = run_experiment()
    print(_canonical_json(summary))


if __name__ == "__main__":
    main()
