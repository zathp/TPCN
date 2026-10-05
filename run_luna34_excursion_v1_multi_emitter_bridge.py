"""Run the bounded Luna-34 EXCURSION_V1 multi-emitter mechanism diagnostic."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields, is_dataclass
import hashlib
import json
import math
import platform
import random
import sys
from pathlib import Path
from typing import Any, Iterable

from tpcn.event_runtime import Event, EventQueue, EventType
from tpcn.excursion_neuron import E1Config, E1Mode, MultiExcursionNeuron, PendingInternalEvent
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.spiral_benchmark import SpiralConfig, make_spiral_dataset
from tpcn.stroke_dataset import StrokePoint
from tpcn.structural_observation import StructuralObservationPlane
from tpcn.topology import BoundedTopology, Edge


EXECUTION_BASELINE = "c6f0f3b0e8c2e4d0883c7e1627cd5112ab6fa937"
API_BASELINE = "1e2f80aa9e37b332e0637f6ff8b0df18d5f2ceb6"
CONDITIONS = (
    "NO_EDGE_CONTROL",
    "DEFAULT_STATIC_EDGE",
    "STATIC_N2_BOUND_SENSITIVITY",
)
NODES = ("source", "destination")
NEIGHBORS = {"source": ("destination",), "destination": ()}
ARTIFACT_DIRECTORY = Path("artifacts/acp0007-luna34-multi-emitter-bridge")
QUEUE_CAPACITY = 128
EVENT_BUDGET = 1024
SETTLING_HORIZON = 4.0
PREDICTION_CAPACITY = 8
PREDICTION_EXPIRY = 4.0
MAX_ACTIVITY_EVENTS = 1024
ASSOCIATION_WINDOW = 4.0
MAXIMUM_SCORE = 3
GROWTH_DELAY = 0.4


@dataclass(frozen=True, slots=True)
class InputPoint:
    point_index: int
    timestamp: float
    x: float
    y: float
    source_value: float


def _jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: _jsonable(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, (EventType, E1Mode)):
        return value.value
    if isinstance(value, dict):
        return {
            str(key): _jsonable(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, PendingInternalEvent):
        return {
            "neuron_id": value.neuron_id,
            "episode_id": value.episode_id,
            "generation": value.generation,
            "kind": value.kind.value,
            "timestamp": value.timestamp,
            "queue_sequence": value.queue_sequence,
        }
    raise TypeError(f"cannot serialize value of type {type(value).__name__}")


def _canonical_json(value: Any) -> str:
    return json.dumps(
        _jsonable(value),
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def experiment_config() -> dict[str, Any]:
    return {
        "schema": "TPCN-LUNA34-EXCURSION-V1-1",
        "execution_baseline": EXECUTION_BASELINE,
        "api_baseline": API_BASELINE,
        "dataset": {
            "generator": "make_spiral_dataset",
            "examples_per_class": 16,
            "train_seed": "12007 + seed",
            "evaluation_seed": "22017 + seed (generated only; not consumed)",
            "spiral_config": asdict(SpiralConfig()),
            "training_order": "random.Random(330000 + seed).shuffle(point_sequences)",
            "input_transform": "point.x + point.y at point.timestamp",
            "label_access": "prohibited; only each training example's points are read",
            "opaque_character_id": "seed and shuffled sequence index only",
        },
        "network": {
            "nodes": list(NODES),
            "edge_capacity": 1,
            "routing_capacity": 1,
            "fan_in_limit": 1,
            "fan_out_limit": 1,
            "observation_neighbors": NEIGHBORS,
            "propagation_delay": 1.0,
            "neuron": {
                "type": "MultiExcursionNeuron",
                "config": asdict(E1Config()),
                "initial_state": 0.0,
            },
            "queue_capacity": QUEUE_CAPACITY,
            "runtime_event_budget_per_character": EVENT_BUDGET,
            "settling_horizon": SETTLING_HORIZON,
            "prediction_capacity": PREDICTION_CAPACITY,
            "prediction_expiry": PREDICTION_EXPIRY,
            "max_activity_events": MAX_ACTIVITY_EVENTS,
            "structural_neighborhood_limit": 1,
            "structural_reverse_observer_limit": 1,
            "structural_history_capacity": 8,
            "structural_candidate_capacity": 4,
            "structural_association_window": ASSOCIATION_WINDOW,
            "structural_maximum_score": MAXIMUM_SCORE,
            "structural_growth_delay": GROWTH_DELAY,
            "topology_mutation": False,
            "reward": 0.0,
        },
        "conditions": {
            "NO_EDGE_CONTROL": {"active_edges": []},
            "DEFAULT_STATIC_EDGE": {
                "active_edges": [
                    {
                        "source": "source",
                        "destination": "destination",
                        "edge_weight": 1.0,
                        "divider_strength": 1.0,
                        "reference": 0.0,
                        "propagation_delay": 1.0,
                    }
                ]
            },
            "STATIC_N2_BOUND_SENSITIVITY": {
                "active_edges": [
                    {
                        "source": "source",
                        "destination": "destination",
                        "edge_weight": 2.0,
                        "divider_strength": 1.0,
                        "reference": 0.0,
                        "propagation_delay": 1.0,
                    }
                ]
            },
        },
        "expected_design": {
            "seeds": [0, 1, 2, 3, 4],
            "training_characters_per_seed": 64,
            "input_streams": 320,
            "character_condition_executions": 960,
        },
        "excluded_endpoints": [
            "classification accuracy or correctness",
            "held-out, prediction, resource, or task efficacy",
            "readout outputs and class-derived metadata",
            "edge admission or topology mutation",
        ],
    }


def _edge(condition: str) -> Edge | None:
    if condition == "NO_EDGE_CONTROL":
        return None
    if condition == "DEFAULT_STATIC_EDGE":
        weight = 1.0
    elif condition == "STATIC_N2_BOUND_SENSITIVITY":
        weight = 2.0
    else:
        raise ValueError(f"unknown Luna-34 condition: {condition!r}")
    return Edge(
        "source",
        "destination",
        1.0,
        edge_weight=weight,
        divider_strength=1.0,
        reference=0.0,
    )


def _topology(condition: str) -> BoundedTopology:
    edge = _edge(condition)
    return BoundedTopology.from_edges(
        NODES,
        () if edge is None else (edge,),
        fan_in_limit=1,
        fan_out_limit=1,
        edge_capacity=1,
        routing_capacity=1,
    )


def _input_points(points: Iterable[StrokePoint]) -> tuple[InputPoint, ...]:
    converted: list[InputPoint] = []
    previous_timestamp: float | None = None
    for index, point in enumerate(points):
        timestamp = float(point.timestamp)
        x = float(point.x)
        y = float(point.y)
        if not all(math.isfinite(item) for item in (timestamp, x, y)):
            raise ValueError("input points must have finite coordinates and timestamps")
        if previous_timestamp is not None and timestamp < previous_timestamp:
            raise ValueError("generated training point timestamps must be nondecreasing")
        converted.append(InputPoint(index, timestamp, x, y, x + y))
        previous_timestamp = timestamp
    if not converted:
        raise ValueError("a Luna-34 character must contain at least one point")
    return tuple(converted)


def _point_batches(points: tuple[InputPoint, ...]) -> tuple[tuple[tuple[float, float], ...], ...]:
    batches: list[tuple[tuple[float, float], ...]] = []
    current_timestamp: float | None = None
    current: list[tuple[float, float]] = []
    for point in points:
        if current_timestamp is None or point.timestamp == current_timestamp:
            current_timestamp = point.timestamp
            current.append((point.timestamp, point.source_value))
            continue
        batches.append(tuple(current))
        current_timestamp = point.timestamp
        current = [(point.timestamp, point.source_value)]
    batches.append(tuple(current))
    return tuple(batches)


def _pending_record(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, PendingInternalEvent):
        raise TypeError("internal trace event did not expose PendingInternalEvent payload")
    return {
        "neuron_id": payload.neuron_id,
        "episode_id": payload.episode_id,
        "generation": payload.generation,
        "kind": payload.kind.value,
        "scheduled_timestamp": payload.timestamp,
        "queue_sequence": payload.queue_sequence,
    }


def _replay_destination(
    routed: list[dict[str, Any]],
    *,
    horizon: float,
) -> tuple[list[dict[str, Any]], tuple[dict[str, Any], ...], float, bool, float, str]:
    config = E1Config()
    neuron = MultiExcursionNeuron("destination", config=config)
    queue: EventQueue[Event] = EventQueue(QUEUE_CAPACITY)
    state_records: list[dict[str, Any]] = []
    replay_emissions: list[dict[str, Any]] = []
    max_pre_threshold_magnitude = 0.0
    threshold_crossed = False

    def process_internal_before(timestamp: float, *, inclusive: bool) -> None:
        while queue:
            pending = queue.peek()
            if pending is None:
                break
            due = pending.timestamp <= timestamp if inclusive else pending.timestamp < timestamp
            if not due:
                break
            internal = queue.pop_ready(pending.timestamp)
            emitted = neuron.receive_event(internal, queue)
            if emitted is not None:
                replay_emissions.append(
                    {
                        "event_id": emitted.event_id,
                        "emitter_id": emitted.source,
                        "timestamp": emitted.timestamp,
                        "payload": emitted.payload,
                    }
                )

    for transfer in routed:
        timestamp = transfer["arrival_timestamp"]
        process_internal_before(timestamp, inclusive=False)
        elapsed = timestamp - neuron.last_update_timestamp
        state_before = max(
            -config.x_max,
            min(
                config.x_max,
                neuron.state * math.exp(-config.decay_rate * elapsed),
            ),
        )
        previous_mode = neuron.mode
        event = Event(
            timestamp,
            "source",
            "destination",
            EventType.EXCURSION,
            transfer["transformed_payload"],
            sequence=transfer["receive_sequence"],
            event_id=transfer["emission_event_id"],
            lineage_id=transfer["lineage_id"],
        )
        immediate_emission = neuron.receive_event(event, queue)
        if immediate_emission is not None:
            replay_emissions.append(
                {
                    "event_id": immediate_emission.event_id,
                    "emitter_id": immediate_emission.source,
                    "timestamp": immediate_emission.timestamp,
                    "payload": immediate_emission.payload,
                }
            )
        state_after = neuron.state
        if not threshold_crossed:
            max_pre_threshold_magnitude = max(
                max_pre_threshold_magnitude,
                abs(state_before),
            )
            threshold_crossed = (
                previous_mode == E1Mode.N and neuron.mode != E1Mode.N
            )
        transfer["destination_state_before"] = state_before
        transfer["destination_state_after"] = state_after
        transfer["destination_mode_after"] = neuron.mode.value
        state_records.append(
            {
                "event_id": transfer["emission_event_id"],
                "arrival_timestamp": timestamp,
                "state_before": state_before,
                "state_after": state_after,
                "mode_after": neuron.mode.value,
            }
        )

    process_internal_before(horizon, inclusive=True)
    final_elapsed = horizon - neuron.last_update_timestamp
    final_state = max(
        -config.x_max,
        min(
            config.x_max,
            neuron.state * math.exp(-config.decay_rate * final_elapsed),
        ),
    )
    return (
        state_records,
        tuple(replay_emissions),
        max_pre_threshold_magnitude,
        threshold_crossed,
        final_state,
        neuron.mode.value,
    )


def _emission_intervals(emissions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        emissions,
        key=lambda item: (item["timestamp"], item["emitter_id"], item["event_id"]),
    )
    return [
        {
            "earlier_event_id": earlier["event_id"],
            "earlier_emitter_id": earlier["emitter_id"],
            "earlier_timestamp": earlier["timestamp"],
            "later_event_id": later["event_id"],
            "later_emitter_id": later["emitter_id"],
            "later_timestamp": later["timestamp"],
            "interval": later["timestamp"] - earlier["timestamp"],
        }
        for earlier, later in zip(ordered, ordered[1:])
    ]


def _character_record(
    *,
    seed: int,
    sequence_index: int,
    condition: str,
    points: tuple[StrokePoint, ...],
) -> dict[str, Any]:
    input_points = _input_points(points)
    character_id = f"c{seed:02d}-{sequence_index:03d}"
    plane = StructuralObservationPlane(
        NODES,
        NEIGHBORS,
        neighborhood_limit=1,
        reverse_observer_limit=1,
        history_capacity=8,
        candidate_capacity=4,
        association_window=ASSOCIATION_WINDOW,
        maximum_score=MAXIMUM_SCORE,
        propagation_delay=GROWTH_DELAY,
    )
    observer_records: list[tuple[str, str | int, float]] = []

    def observe(emitter_id: str, event_id: str | int, timestamp: float) -> None:
        plane.observe_emission(emitter_id, event_id, timestamp)
        observer_records.append((emitter_id, event_id, timestamp))

    topology = _topology(condition)
    edge = _edge(condition)
    neurons = tuple(
        MultiExcursionNeuron(node, config=E1Config())
        for node in NODES
    )
    runtime = ExcursionCharacterRuntime(
        neurons,
        topology,
        queue_capacity=QUEUE_CAPACITY,
        event_budget=EVENT_BUDGET,
        settling_horizon=SETTLING_HORIZON,
        prediction_capacity=PREDICTION_CAPACITY,
        prediction_expiry=PREDICTION_EXPIRY,
        max_activity_events=MAX_ACTIVITY_EVENTS,
        namespace="luna34",
        emission_observer=observe,
    )
    runtime.start_character(
        character_id,
        sequence_index,
        timestamp=0.0,
        predictor_source="source",
        readout_sources=NODES,
        input_destination="source",
    )
    for batch in _point_batches(input_points):
        runtime.admit_external_batch(batch)
    last_timestamp = input_points[-1].timestamp
    result = runtime.end_character(
        last_external_timestamp=last_timestamp,
        reward=0.0,
        reward_delay=0.0,
        reward_message_id=f"neutral-{character_id}",
    )
    snapshot = plane.freeze()

    emissions: list[dict[str, Any]] = []
    runtime_input_events: list[dict[str, Any]] = []
    routed: list[dict[str, Any]] = []
    destination_internal_events: list[dict[str, Any]] = []
    for trace in result.trace:
        if trace[3] == "excursion_emission":
            emissions.append(
                {
                    "emitter_id": trace[1],
                    "event_id": trace[5],
                    "timestamp": trace[0],
                    "payload": trace[4],
                    "payload_sign": 0 if trace[4] == 0 else (1 if trace[4] > 0 else -1),
                    "payload_magnitude": abs(trace[4]),
                }
            )
        elif trace[3] == EventType.INPUT:
            runtime_input_events.append(
                {
                    "event_id": trace[6],
                    "timestamp": trace[0],
                    "source": trace[1],
                    "destination": trace[2],
                    "value": trace[4],
                }
            )
        elif trace[3] == EventType.EXCURSION:
            routed.append(
                {
                    "emission_event_id": trace[6],
                    "emitter_id": trace[1],
                    "destination": trace[2],
                    "emission_timestamp": trace[0] - edge.propagation_delay if edge else None,
                    "arrival_timestamp": trace[0],
                    "transformed_payload": trace[4],
                    "payload_sign": 0 if trace[4] == 0 else (1 if trace[4] > 0 else -1),
                    "payload_magnitude": abs(trace[4]),
                    "propagation_delay": edge.propagation_delay if edge else None,
                    "receive_sequence": trace[5],
                    "lineage_id": trace[7],
                    "route_depth": trace[9],
                    "route_path": list(trace[10]),
                    "edge_transfer_proxy": abs(trace[4]),
                }
            )
        elif trace[2] == "destination" and trace[3] == EventType.INTERNAL:
            destination_internal_events.append(
                {
                    "timestamp": trace[0],
                    "sequence": trace[5],
                    "payload": _pending_record(trace[4]),
                }
            )

    actual_identity_records = {
        (item["emitter_id"], item["event_id"], item["timestamp"])
        for item in emissions
    }
    observer_identity_records = set(observer_records)
    if actual_identity_records != observer_identity_records:
        raise RuntimeError("canonical emission trace and observation callback identities differ")
    unique_emissions = {
        (item["emitter_id"], item["event_id"]): item
        for item in emissions
    }
    emissions = sorted(
        unique_emissions.values(),
        key=lambda item: (item["timestamp"], item["emitter_id"], item["event_id"]),
    )
    emission_by_identity = {
        (item["emitter_id"], item["event_id"]): item
        for item in emissions
    }

    for transfer in routed:
        source_emission = emission_by_identity.get(
            (transfer["emitter_id"], transfer["emission_event_id"])
        )
        if source_emission is None:
            raise RuntimeError("routed event identity does not reconcile to an emission")
        if transfer["destination"] != "destination" or edge is None:
            raise RuntimeError("unexpected routed event outside the declared fixed edge")
        transfer["emission_timestamp"] = source_emission["timestamp"]
        expected_payload = (
            edge.divider_strength * math.tanh(edge.edge_weight * source_emission["payload"])
            + (1.0 - edge.divider_strength) * edge.reference
        )
        if not math.isclose(
            transfer["transformed_payload"],
            expected_payload,
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise RuntimeError("routed payload differs from the declared Model-B transform")
        if not math.isclose(
            transfer["arrival_timestamp"] - transfer["emission_timestamp"],
            edge.propagation_delay,
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise RuntimeError("routed event does not preserve the declared positive delay")
    for index, transfer in enumerate(routed, start=1):
        transfer["destination_receive_count"] = index

    horizon = last_timestamp + SETTLING_HORIZON
    (
        destination_state_records,
        replay_destination_emissions,
        max_pre_threshold_magnitude,
        threshold_crossed,
        destination_state_at_horizon,
        destination_mode_at_horizon,
    ) = _replay_destination(routed, horizon=horizon)
    actual_destination_emissions = [
        {
            "event_id": item["event_id"],
            "emitter_id": item["emitter_id"],
            "timestamp": item["timestamp"],
            "payload": item["payload"],
        }
        for item in emissions
        if item["emitter_id"] == "destination"
    ]
    if replay_destination_emissions != tuple(actual_destination_emissions):
        raise RuntimeError("public destination replay does not reproduce canonical emissions")

    legal_intervals = [
        {
            "source_event_id": source["event_id"],
            "destination_event_id": destination["event_id"],
            "source_timestamp": source["timestamp"],
            "destination_timestamp": destination["timestamp"],
            "interval": destination["timestamp"] - source["timestamp"],
        }
        for source in emissions
        if source["emitter_id"] == "source"
        for destination in emissions
        if destination["emitter_id"] == "destination"
        and 0.0 < destination["timestamp"] - source["timestamp"] <= ASSOCIATION_WINDOW
    ]
    candidates = [
        _jsonable(candidate)
        for candidate in snapshot.candidates
    ]
    legal_candidate_count = 0
    for candidate in snapshot.candidates:
        if candidate.observer != candidate.source or candidate.destination not in NEIGHBORS[candidate.source]:
            raise RuntimeError("frozen observation plane exposed nonlocal candidate evidence")
        if not any(
            interval["source_timestamp"] < interval["destination_timestamp"]
            and 0.0 < interval["destination_timestamp"] - interval["source_timestamp"] <= ASSOCIATION_WINDOW
            for interval in legal_intervals
        ):
            raise RuntimeError("frozen candidate lacks a legal within-character emission interval")
        legal_candidate_count += 1

    route_sign_runs: list[dict[str, Any]] = []
    for transfer in routed:
        sign = transfer["payload_sign"]
        if route_sign_runs and route_sign_runs[-1]["sign"] == sign:
            route_sign_runs[-1]["event_ids"].append(transfer["emission_event_id"])
            route_sign_runs[-1]["length"] += 1
        else:
            route_sign_runs.append(
                {
                    "sign": sign,
                    "event_ids": [transfer["emission_event_id"]],
                    "length": 1,
                }
            )

    emitters = sorted({emitter for emitter, _ in unique_emissions})
    execution = {
        "completed": result.execution.completed,
        "event_budget_exhausted": result.execution.budget_exhausted,
        "event_budget": result.execution.configured_event_budget,
        "events_processed": result.execution.processed_event_count,
        "pending_event_count": result.pending_event_count,
        "beyond_deadline_event_count": result.beyond_deadline_event_count,
        "incomplete_settling": result.incomplete_settling,
        "last_event_timestamp": result.execution.last_event_timestamp,
        "peak_queue_occupancy": result.peak_queue_occupancy,
        "queue_capacity": QUEUE_CAPACITY,
        "settling_horizon": SETTLING_HORIZON,
        "settling_deadline": horizon,
        "receiving_neuron_count": result.receiving_neuron_count,
        "emitting_neuron_count": result.emitting_neuron_count,
        "max_route_depth": result.max_route_depth,
        "silent_event_count": result.silent_event_count,
    }
    if execution["events_processed"] > EVENT_BUDGET:
        raise RuntimeError("runtime exceeded the per-character event budget")
    if execution["peak_queue_occupancy"] > QUEUE_CAPACITY:
        raise RuntimeError("runtime exceeded the per-character queue capacity")
    if execution["completed"] != (execution["pending_event_count"] == 0):
        raise RuntimeError("runtime completion and pending-work counts do not reconcile")
    if condition == "NO_EDGE_CONTROL" and (routed or actual_destination_emissions):
        raise RuntimeError("no-edge control produced routed work or a destination emission")

    record: dict[str, Any] = {
        "seed": seed,
        "condition": condition,
        "character_id": character_id,
        "sequence_index": sequence_index,
        "input_digest": _digest(
            [
                (point.timestamp, point.x, point.y, point.source_value)
                for point in input_points
            ]
        ),
        "input_points": [asdict(point) for point in input_points],
        "source_input_events": runtime_input_events,
        "canonical_emissions": emissions,
        "routed_contributions": routed,
        "destination_internal_events": destination_internal_events,
        "destination_state_replay": {
            "records": destination_state_records,
            "replayed_emissions": list(replay_destination_emissions),
            "maximum_decayed_magnitude_before_threshold_crossing": max_pre_threshold_magnitude,
            "threshold_crossed": threshold_crossed,
            "state_at_settling_deadline": destination_state_at_horizon,
            "mode_at_settling_deadline": destination_mode_at_horizon,
        },
        "emission_intervals": _emission_intervals(emissions),
        "routed_contribution_sign_runs": route_sign_runs,
        "distinct_emitters": emitters,
        "distinct_emitter_count": len(emitters),
        "has_multiple_distinct_emitters": len(emitters) >= 2,
        "characters_with_two_or_more_emitters": int(len(emitters) >= 2),
        "source_before_destination_intervals": legal_intervals,
        "structural_observation": {
            "candidate_count": len(snapshot.candidates),
            "legal_candidate_count": legal_candidate_count,
            "candidates": candidates,
            "observation_count": snapshot.observation_count,
            "observation_work": snapshot.observation_work,
            "candidate_rejections": snapshot.candidate_rejections,
        },
        "edge": None if edge is None else _jsonable(edge),
        "execution": execution,
    }
    record["replay_digest"] = _digest(record)
    return record


def _condition_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "character_count": len(records),
        "source_emitting_characters": sum(
            any(emission["emitter_id"] == "source" for emission in record["canonical_emissions"])
            for record in records
        ),
        "destination_emitting_characters": sum(
            any(emission["emitter_id"] == "destination" for emission in record["canonical_emissions"])
            for record in records
        ),
        "characters_with_two_or_more_emitters": sum(
            record["has_multiple_distinct_emitters"] for record in records
        ),
        "source_emissions": sum(
            emission["emitter_id"] == "source"
            for record in records
            for emission in record["canonical_emissions"]
        ),
        "destination_emissions": sum(
            emission["emitter_id"] == "destination"
            for record in records
            for emission in record["canonical_emissions"]
        ),
        "routed_contributions": sum(len(record["routed_contributions"]) for record in records),
        "destination_receive_count": sum(len(record["routed_contributions"]) for record in records),
        "candidate_characters": sum(
            record["structural_observation"]["legal_candidate_count"] > 0
            for record in records
        ),
        "legal_candidates": sum(
            record["structural_observation"]["legal_candidate_count"]
            for record in records
        ),
        "execution_completions": sum(record["execution"]["completed"] for record in records),
        "incomplete_characters": sum(
            record["execution"]["incomplete_settling"] for record in records
        ),
        "total_pending_events": sum(
            record["execution"]["pending_event_count"] for record in records
        ),
        "maximum_events_processed": max(
            (record["execution"]["events_processed"] for record in records),
            default=0,
        ),
        "maximum_queue_occupancy": max(
            (record["execution"]["peak_queue_occupancy"] for record in records),
            default=0,
        ),
        "maximum_route_depth": max(
            (record["execution"]["max_route_depth"] for record in records),
            default=0,
        ),
        "maximum_destination_accumulator_magnitude_before_threshold_crossing": max(
            (
                record["destination_state_replay"][
                    "maximum_decayed_magnitude_before_threshold_crossing"
                ]
                for record in records
            ),
            default=0.0,
        ),
        "replay_digest": _digest([record["replay_digest"] for record in records]),
    }


def _summarize(results: dict[str, Any]) -> dict[str, Any]:
    per_seed: dict[str, Any] = {}
    for seed, conditions in results["runs"].items():
        per_seed[seed] = {
            condition: _condition_summary(records)
            for condition, records in conditions.items()
        }
    global_conditions = {
        condition: _condition_summary(
            [
                record
                for conditions in results["runs"].values()
                for record in conditions[condition]
            ]
        )
        for condition in CONDITIONS
    }
    sensitivity_streams = []
    for seed, conditions in results["runs"].items():
        default_by_id = {
            record["character_id"]: record
            for record in conditions["DEFAULT_STATIC_EDGE"]
        }
        sensitive_by_id = {
            record["character_id"]: record
            for record in conditions["STATIC_N2_BOUND_SENSITIVITY"]
        }
        for character_id in sorted(default_by_id):
            default = default_by_id[character_id]
            sensitive = sensitive_by_id[character_id]
            default_bridge = default["has_multiple_distinct_emitters"]
            sensitive_bridge = sensitive["has_multiple_distinct_emitters"]
            default_candidates = default["structural_observation"]["legal_candidate_count"]
            sensitive_candidates = sensitive["structural_observation"]["legal_candidate_count"]
            if (sensitive_bridge and not default_bridge) or (
                sensitive_candidates > 0 and default_candidates == 0
            ):
                sensitivity_streams.append(
                    {
                        "seed": int(seed),
                        "character_id": character_id,
                        "default_destination_emissions": sum(
                            item["emitter_id"] == "destination"
                            for item in default["canonical_emissions"]
                        ),
                        "sensitivity_destination_emissions": sum(
                            item["emitter_id"] == "destination"
                            for item in sensitive["canonical_emissions"]
                        ),
                        "default_legal_candidates": default_candidates,
                        "sensitivity_legal_candidates": sensitive_candidates,
                    }
                )

    default_bridge = (
        global_conditions["DEFAULT_STATIC_EDGE"]["characters_with_two_or_more_emitters"] > 0
    )
    any_bridge = any(
        global_conditions[condition]["characters_with_two_or_more_emitters"] > 0
        for condition in CONDITIONS
    )
    candidate_formation = any(
        global_conditions[condition]["legal_candidates"] > 0
        for condition in CONDITIONS
    )
    no_edge_is_negative = (
        global_conditions["NO_EDGE_CONTROL"]["routed_contributions"] == 0
        and global_conditions["NO_EDGE_CONTROL"]["destination_emissions"] == 0
        and global_conditions["NO_EDGE_CONTROL"]["legal_candidates"] == 0
    )
    classifications = []
    if any_bridge:
        classifications.append("MULTI-EMITTER BRIDGE ESTABLISHED")
    if not default_bridge:
        classifications.append("MULTI-EMITTER BRIDGE NOT ESTABLISHED UNDER DEFAULT EDGE")
    if sensitivity_streams:
        classifications.append("STATIC N2 TRANSFER SENSITIVITY ESTABLISHED")
    if candidate_formation:
        classifications.append("CANDIDATE FORMATION ESTABLISHED")
    else:
        classifications.append("CANDIDATE FORMATION NOT ESTABLISHED")
    return {
        "schema": "TPCN-LUNA34-EXCURSION-V1-SUMMARY-1",
        "execution_baseline": EXECUTION_BASELINE,
        "api_baseline": API_BASELINE,
        "design_counts": {
            "seeds": len(results["runs"]),
            "input_streams": sum(
                len(next(iter(conditions.values())))
                for conditions in results["runs"].values()
            ),
            "character_condition_executions": sum(
                len(records)
                for conditions in results["runs"].values()
                for records in conditions.values()
            ),
        },
        "per_seed": per_seed,
        "per_condition": global_conditions,
        "no_edge_control_is_genuine_negative": no_edge_is_negative,
        "static_n2_transfer_sensitivity_streams": sensitivity_streams,
        "terminal_classifications": classifications,
        "limitations": [],
        "interpretation_boundary": (
            "Mechanism evidence is bounded to the declared generated training point streams "
            "and the three fixed topology conditions; it is not task efficacy, beneficial "
            "structural growth, prediction/resource benefit, architecture promotion, or hardware validation."
        ),
    }


def _training_point_sequences(seed: int) -> tuple[tuple[StrokePoint, ...], ...]:
    dataset = make_spiral_dataset(
        examples_per_class=16,
        train_seed=12007 + seed,
        evaluation_seed=22017 + seed,
        config=SpiralConfig(),
    )
    point_sequences = [example.points for example in dataset.train]
    random.Random(330000 + seed).shuffle(point_sequences)
    if len(point_sequences) != 64:
        raise RuntimeError("Luna-34 requires exactly 64 training point sequences per seed")
    return tuple(point_sequences)


def run_experiment(
    output_directory: Path = ARTIFACT_DIRECTORY,
) -> tuple[dict[str, Any], dict[str, Any]]:
    runs: dict[str, Any] = {}
    for seed in range(5):
        point_sequences = _training_point_sequences(seed)
        seed_runs: dict[str, list[dict[str, Any]]] = {}
        for condition in CONDITIONS:
            seed_runs[condition] = [
                _character_record(
                    seed=seed,
                    sequence_index=sequence_index,
                    condition=condition,
                    points=points,
                )
                for sequence_index, points in enumerate(point_sequences)
            ]
        paired_digests = {
            record["character_id"]: record["input_digest"]
            for record in seed_runs[CONDITIONS[0]]
        }
        if any(
            {
                record["character_id"]: record["input_digest"]
                for record in seed_runs[condition]
            }
            != paired_digests
            for condition in CONDITIONS[1:]
        ):
            raise RuntimeError("paired conditions did not consume identical point streams")
        runs[str(seed)] = seed_runs

    results = {
        "schema": "TPCN-LUNA34-EXCURSION-V1-RESULTS-1",
        "execution_baseline": EXECUTION_BASELINE,
        "api_baseline": API_BASELINE,
        "conditions": list(CONDITIONS),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "runs": runs,
    }
    summary = _summarize(results)
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
