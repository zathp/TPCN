"""Run the bounded Luna-40 existing-growth/effective-drive characterization."""

from __future__ import annotations

from contextlib import ExitStack
from dataclasses import asdict, is_dataclass
from enum import Enum
import hashlib
import json
import math
import platform
import random
import sys
from pathlib import Path
from typing import Any, Callable
from unittest import mock

import run_luna39_acp0008_propagation_emission_diagnostic as luna39
from tpcn.eligibility import EligibilityCapacityError, EligibilityLedger
from tpcn.event_runtime import Event, EventQueue, EventType
from tpcn.excursion_neuron import E1Config, IntegrationConfig, MultiExcursionNeuron
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.structural_observation import StructuralObservationPlane
from tpcn.structural_plasticity import CandidateEvidence, StructuralPlasticityController
from tpcn.topology import BoundedTopology, Edge, TopologyCapacityError


START_REVISION = "a39dd335e7af1b18a8d28ef3faf7b975304132df"
NODES = ("source", "relay", "destination")
ARMS = (
    "FROZEN_NO_OBSERVATION",
    "FROZEN_OBSERVATION_ONLY",
    "LOCAL_GROWTH_ENABLED",
    "NO_LOCAL_EVIDENCE_CONTROL",
)
SEEDS = (0, 1, 2, 3, 4)
ELIGIBILITY_CAPACITY = 1024
QUEUE_CAPACITY = 128
RUNTIME_EVENT_BUDGET = 1024
SETTLING_HORIZON = 4.0
PREDICTION_CAPACITY = 8
PREDICTION_EXPIRY = 4.0
MAX_ACTIVITY_EVENTS = 1024
NEIGHBORHOOD_LIMIT = 2
REVERSE_OBSERVER_LIMIT = 2
ASSOCIATION_WINDOW = 4.0
HISTORY_CAPACITY = 8
CANDIDATE_CAPACITY = 4
MAXIMUM_SCORE = 3
GROWTH_DELAY = 0.4
GROWTH_ATTEMPT_BUDGET = 4
ARTIFACT_DIRECTORY = Path("artifacts/luna40-effective-routed-drive")


class StopCondition(RuntimeError):
    """A predeclared Luna-40 stop condition; the affected run is not retried."""

    def __init__(self, reason: str, detail: dict[str, Any]) -> None:
        super().__init__(reason)
        self.reason = reason
        self.detail = detail


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
            raise ValueError("non-finite scientific value")
        return value
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if hasattr(value, "__dict__"):
        return _jsonable(vars(value))
    return repr(value)


def _canonical_json(value: Any) -> str:
    return json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _edge_identity(source: str, destination: str) -> str:
    return f"{source}->{destination}"


def _edge_record(edge: Edge) -> dict[str, Any]:
    return {
        "identity": _edge_identity(edge.source, edge.destination),
        "source": edge.source,
        "destination": edge.destination,
        "delay": float(edge.propagation_delay),
        "w": float(edge.edge_weight),
        "d": float(edge.divider_strength),
        "r": float(edge.reference),
        "routing_cost": edge.routing_cost,
        "legacy_identity": edge.legacy_identity,
    }


def _topology_records(topology: BoundedTopology) -> list[dict[str, Any]]:
    return [_edge_record(edge) for edge in topology.edges]


def _initial_topology() -> BoundedTopology:
    return BoundedTopology.from_edges(
        NODES,
        (("source", "relay", 1.0), ("relay", "destination", 1.0)),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=3,
        routing_capacity=3,
    )


def _neighbors_for(arm: str) -> dict[str, tuple[str, ...]]:
    if arm == "NO_LOCAL_EVIDENCE_CONTROL":
        return {"source": (), "relay": (), "destination": ()}
    return {"source": ("destination",), "relay": (), "destination": ()}


def _point_batches(points: tuple[Any, ...]) -> tuple[tuple[tuple[float, float], ...], ...]:
    batches: list[list[tuple[float, float]]] = []
    last_timestamp: float | None = None
    for point in points:
        timestamp = float(point.timestamp)
        value = float(point.x) + float(point.y)
        if not math.isfinite(timestamp) or not math.isfinite(value):
            raise StopCondition("invalid input timestamp or value", {})
        if last_timestamp is not None and timestamp < last_timestamp:
            raise StopCondition("input timestamps are not ordered", {"timestamp": timestamp})
        if not batches or timestamp != last_timestamp:
            batches.append([])
        batches[-1].append((timestamp, value))
        last_timestamp = timestamp
    return tuple(tuple(batch) for batch in batches)


class _OccupancyAudit:
    """Bounded test-harness accounting over the existing public ledgers."""

    def __init__(self) -> None:
        self.ledgers: list[EligibilityLedger] = []
        self.stats: dict[str, dict[str, Any]] = {}
        self.capacity_errors: list[dict[str, Any]] = []

    def register(self, ledger: EligibilityLedger) -> None:
        self.ledgers.append(ledger)
        self.stats[ledger.ledger_id] = {
            "ledger_id": ledger.ledger_id,
            "configured_capacity": ledger.max_traces,
            "initial_occupancy": len(ledger.traces),
            "created": 0,
            "removed": 0,
            "peak_occupancy": len(ledger.traces),
        }

    def observe(
        self,
        ledger: EligibilityLedger,
        call: Callable[[], Any],
        timestamp: float,
        trace_id: str | None,
    ) -> Any:
        before = {trace.trace_id for trace in ledger.traces}
        stats = self.stats[ledger.ledger_id]
        try:
            result = call()
        except EligibilityCapacityError:
            self.capacity_errors.append(
                {
                    "ledger_id": ledger.ledger_id,
                    "trace_id": trace_id,
                    "creation_index": stats["created"] + 1,
                    "timestamp": timestamp,
                    "occupancy": len(before),
                    "capacity": ledger.max_traces,
                }
            )
            raise
        after = {trace.trace_id for trace in ledger.traces}
        stats["created"] += len(after - before)
        stats["removed"] += len(before - after)
        stats["peak_occupancy"] = max(stats["peak_occupancy"], len(after))
        return result

    def finalize(self) -> list[dict[str, Any]]:
        records = []
        for ledger in self.ledgers:
            stats = dict(self.stats[ledger.ledger_id])
            stats["final_occupancy"] = len(ledger.traces)
            stats["reconciles"] = (
                stats["initial_occupancy"] + stats["created"] - stats["removed"]
                == stats["final_occupancy"]
            )
            records.append(stats)
        return records


def _observer_associations(
    observations: list[dict[str, Any]],
    *,
    neighbors: dict[str, tuple[str, ...]],
) -> tuple[list[dict[str, Any]], dict[tuple[str, str], int]]:
    """Reconstruct local association pairs from actual callback observations."""
    histories: dict[str, list[dict[str, Any]]] = {node: [] for node in NODES}
    raw_counts: dict[tuple[str, str], int] = {}
    pairs: list[dict[str, Any]] = []
    for observation in observations:
        observer = observation["observer"]
        emitter = observation["emitter_id"]
        history = histories[observer]
        previous = next(
            (item for item in reversed(history) if item["emitter_id"] == observer),
            None,
        )
        if (
            emitter != observer
            and emitter in neighbors[observer]
            and previous is not None
        ):
            gap = observation["timestamp"] - previous["timestamp"]
            if 0.0 < gap <= ASSOCIATION_WINDOW:
                key = (observer, emitter)
                score_before = min(MAXIMUM_SCORE, raw_counts.get(key, 0))
                raw_counts[key] = raw_counts.get(key, 0) + 1
                pairs.append(
                    {
                        "observer": observer,
                        "source": observer,
                        "destination": emitter,
                        "source_event_id": previous["event_id"],
                        "source_timestamp": previous["timestamp"],
                        "destination_event_id": observation["event_id"],
                        "destination_timestamp": observation["timestamp"],
                        "gap": gap,
                        "score_before": score_before,
                        "score_after": min(MAXIMUM_SCORE, raw_counts[key]),
                    }
                )
        history.append(observation)
        del history[:-HISTORY_CAPACITY]
    return pairs, raw_counts


def _destination_classification(
    emission: dict[str, Any],
    integration_trace: list[dict[str, Any]],
) -> dict[str, Any]:
    matches = [
        entry for entry in integration_trace
        if entry.get("emission_id") == emission["event_id"]
        and entry.get("emission_timestamp") == emission["timestamp"]
    ]
    if len(matches) != 1:
        raise StopCondition(
            "destination canonical emission does not map uniquely to integration trace",
            {"emission": emission, "matching_trace_count": len(matches)},
        )
    entry = matches[0]
    threshold = float(entry["theta_z"])
    if (
        entry["classification"] == "integrated_discharge"
        and abs(float(entry["discharge_amount"])) > 0.0
        and abs(float(entry["z_after_input"])) >= threshold
        and abs(float(entry["z_post_discharge"])) < abs(float(entry["z_after_input"]))
    ):
        classification = "integrated_discharge"
    elif (
        entry["classification"] == "direct"
        and entry["discharge_amount"] == 0.0
        and entry["crossed_theta_e"]
    ):
        classification = "direct"
    else:
        raise StopCondition(
            "destination emission has inconsistent trace-derived classification",
            {"emission": emission, "trace": entry},
        )
    return {
        "event_id": emission["event_id"],
        "timestamp": emission["timestamp"],
        "classification": classification,
        "trace_emission_id": entry["emission_id"],
        "trace_emission_timestamp": entry["emission_timestamp"],
        "z_before_decay": entry["z_before_decay"],
        "z_after_decay": entry["z_after_decay"],
        "z_before_discharge": entry["z_after_input"],
        "discharge_amount": entry["discharge_amount"],
        "z_after_discharge": entry["z_post_discharge"],
        "theta_Z": threshold,
    }


def _actual_isolated_emission(node: str) -> dict[str, Any]:
    """Produce one canonical emission through the ordinary neuron event API."""
    neuron = MultiExcursionNeuron(node, config=E1Config(event_budget=4096))
    queue: EventQueue[Event] = EventQueue(capacity=8)
    neuron.receive_event(
        Event(0.0, node, node, EventType.INPUT, 1.2, event_id=f"{node}:equal-time-input"),
        queue,
    )
    emissions = []
    while queue:
        next_event = queue.peek()
        if next_event is None:
            break
        emission = neuron.receive_event(queue.pop_ready(next_event.timestamp), queue)
        if emission is not None:
            emissions.append(emission)
    if len(emissions) != 1:
        raise StopCondition(
            "equal-time control failed to produce one canonical emission",
            {"node": node, "emission_count": len(emissions)},
        )
    return _jsonable(emissions[0])


def _equal_time_negative_control() -> dict[str, Any]:
    """Verify equal-time rejection using actual canonical emissions."""
    source = _actual_isolated_emission("source")
    destination = _actual_isolated_emission("destination")
    if source["timestamp"] != destination["timestamp"]:
        raise StopCondition(
            "equal-time control fixture emissions did not share a timestamp",
            {"source": source, "destination": destination},
        )
    plane = StructuralObservationPlane(
        NODES,
        {"source": ("destination",), "relay": (), "destination": ()},
        neighborhood_limit=NEIGHBORHOOD_LIMIT,
        reverse_observer_limit=REVERSE_OBSERVER_LIMIT,
        history_capacity=HISTORY_CAPACITY,
        candidate_capacity=CANDIDATE_CAPACITY,
        association_window=ASSOCIATION_WINDOW,
        maximum_score=MAXIMUM_SCORE,
        propagation_delay=GROWTH_DELAY,
    )
    plane.observe_emission("source", source["event_id"], source["timestamp"])
    plane.observe_emission(
        "destination", destination["event_id"], destination["timestamp"]
    )
    snapshot = plane.freeze()
    return {
        "used_actual_canonical_emissions": True,
        "source_emission": source,
        "destination_emission": destination,
        "same_timestamp": source["timestamp"] == destination["timestamp"],
        "actual_observations": [_jsonable(item) for item in snapshot.observations],
        "observation_count": snapshot.observation_count,
        "candidate_count": len(snapshot.candidates),
        "candidates": [_jsonable(item) for item in snapshot.candidates],
        "passed": snapshot.candidates == (),
        "fixture_parameters_are_not_primary_run_parameters": (
            "This isolated event fixture verifies only the accepted strict-order rule."
        ),
    }


def _network_utilization(topology: BoundedTopology) -> dict[str, Any]:
    fan_in = {node: len(topology.incoming(node)) for node in NODES}
    fan_out = {node: len(topology.outgoing(node)) for node in NODES}
    return {
        "edge_count": len(topology),
        "edge_capacity": topology.edge_capacity,
        "edge_capacity_utilization": len(topology) / topology.edge_capacity,
        "routing_capacity": topology.routing_capacity,
        "routing_capacity_max_outgoing": max(fan_out.values(), default=0),
        "routing_capacity_utilization": max(fan_out.values(), default=0) / topology.routing_capacity,
        "fan_in": fan_in,
        "fan_out": fan_out,
        "fan_in_limit": topology.fan_in_limit,
        "fan_out_limit": topology.fan_out_limit,
        "max_fan_in": max(fan_in.values(), default=0),
        "max_fan_out": max(fan_out.values(), default=0),
    }


def _route_records(
    runtime_trace: tuple[tuple[object, ...], ...],
    emissions: list[dict[str, Any]],
    topology_before: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    edges = {(edge["source"], edge["destination"]): edge for edge in topology_before}
    emitted = {(entry["emitter_id"], entry["event_id"]): entry for entry in emissions}
    records: list[dict[str, Any]] = []
    for row in runtime_trace:
        if len(row) < 12:
            continue
        timestamp, source, destination, event_type = row[:4]
        payload = row[4]
        if getattr(event_type, "value", event_type) != "excursion":
            continue
        sequence, event_id, lineage_id, roots, route_depth, route_path, truncated = row[5:12]
        edge = edges.get((str(source), str(destination)))
        origin = emitted.get((str(source), event_id))
        if edge is None or origin is None:
            raise StopCondition(
                "routed event cannot be linked to its originating edge/emission",
                {"event_id": event_id, "source": source, "destination": destination},
            )
        expected = (
            edge["d"] * math.tanh(edge["w"] * float(origin["payload"]))
            + (1.0 - edge["d"]) * edge["r"]
        )
        if not math.isclose(expected, float(payload), rel_tol=0.0, abs_tol=1e-12):
            raise StopCondition(
                "routed Model-B payload does not match immutable edge parameters",
                {"expected": expected, "actual": payload, "edge": edge},
            )
        edge_id = edge["identity"]
        records.append(
            {
                "route_identity": f"{edge_id}|{event_id}",
                "edge_identity": edge_id,
                "source": source,
                "receiving_node": destination,
                "event_id": event_id,
                "lineage_id": lineage_id,
                "receive_sequence": sequence,
                "emission_timestamp": origin["timestamp"],
                "arrival_timestamp": float(timestamp),
                "payload_before_model_b": origin["payload"],
                "payload_after_model_b": float(payload),
                "w": edge["w"],
                "d": edge["d"],
                "r": edge["r"],
                "delay": edge["delay"],
                "route_depth": route_depth,
                "route_path": list(route_path),
                "causal_roots": list(roots),
                "provenance_truncated": bool(truncated),
            }
        )
    return records


def _integration_and_drive(
    trace_entries: list[dict[str, Any]],
    destination_routes: list[dict[str, Any]],
    destination_emissions: list[dict[str, Any]],
    final_state: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if len(trace_entries) != len(destination_routes):
        raise StopCondition(
            "destination integration trace and actual routed receptions differ",
            {
                "integration_trace_count": len(trace_entries),
                "destination_reception_count": len(destination_routes),
            },
        )
    enriched: list[dict[str, Any]] = []
    for entry, route in zip(trace_entries, destination_routes):
        if (
            float(entry["timestamp"]) != route["arrival_timestamp"]
            or float(entry["input_value"]) != route["payload_after_model_b"]
        ):
            raise StopCondition(
                "destination integration trace does not match routed reception",
                {"integration_trace": entry, "route": route},
            )
        enriched_entry = dict(entry)
        enriched_entry["route_identity"] = route["route_identity"]
        enriched_entry["edge_identity"] = route["edge_identity"]
        enriched_entry["route_path"] = route["route_path"]
        enriched_entry["routed_payload"] = route["payload_after_model_b"]
        enriched.append(enriched_entry)

    discharge_windows = []
    active_window: list[dict[str, Any]] = []
    for entry in enriched:
        if entry["integrated"]:
            active_window.append(
                {
                    "route_identity": entry["route_identity"],
                    "edge_identity": entry["edge_identity"],
                    "arrival_timestamp": entry["timestamp"],
                    "routed_payload": entry["routed_payload"],
                    "z_before_decay": entry["z_before_decay"],
                    "z_after_decay": entry["z_after_decay"],
                    "z_before_input": entry["z_after_decay"],
                    "z_after_input": entry["z_after_input"],
                    "theta_Z": entry["theta_z"],
                }
            )
        if entry["discharge_amount"] != 0.0:
            discharge_windows.append(
                {
                    "discharge_timestamp": entry["timestamp"],
                    "contributing_inputs_since_previous_discharge": list(active_window),
                    "contributing_edge_identities": sorted(
                        {item["edge_identity"] for item in active_window}
                    ),
                    "retained_z_immediately_before_discharge": entry["z_after_input"],
                    "theta_Z": entry["theta_z"],
                    "discharge_amount": entry["discharge_amount"],
                    "post_discharge_z": entry["z_post_discharge"],
                    "emission_id": entry["emission_id"],
                    "emission_timestamp": entry["emission_timestamp"],
                }
            )
            active_window = []
    max_z = max(
        (
            abs(float(entry[key]))
            for entry in enriched
            for key in ("z_after_decay", "z_after_input", "z_post_discharge")
        ),
        default=abs(float(final_state["z"] or 0.0)),
    )
    drive = {
        "ordered_destination_routes": [
            {
                "route_identity": route["route_identity"],
                "edge_identity": route["edge_identity"],
                "event_id": route["event_id"],
                "arrival_timestamp": route["arrival_timestamp"],
                "emission_timestamp": route["emission_timestamp"],
                "routed_payload": route["payload_after_model_b"],
                "route_path": route["route_path"],
            }
            for route in destination_routes
        ],
        "integrated_route_inputs": [
            {
                "route_identity": entry["route_identity"],
                "edge_identity": entry["edge_identity"],
                "arrival_timestamp": entry["timestamp"],
                "routed_payload": entry["routed_payload"],
                "z_before_decay": entry["z_before_decay"],
                "z_after_decay": entry["z_after_decay"],
                "z_after_input": entry["z_after_input"],
                "theta_Z": entry["theta_z"],
            }
            for entry in enriched if entry["integrated"]
        ],
        "discharge_windows": discharge_windows,
        "final_observed_z_after_character_settling": final_state["z"],
        "final_z_observation_timestamp": final_state["last_update_timestamp"],
        "maximum_abs_z_observed": max_z,
        "theta_Z": 1.0,
        "destination_emissions": destination_emissions,
        "z_attribution_note": (
            "Per-event ACP-0008 state is exact. Input identities are linked by "
            "runtime event ID/timestamp/payload. Scalar post-discharge residuals "
            "are not uniquely attributable to individual inputs; discharge windows "
            "therefore report the ordered inputs and measured aggregate z without "
            "inventing an allocation."
        ),
    }
    return enriched, drive


def _run_character(
    *,
    arm: str,
    seed: int,
    sequence_index: int,
    points: tuple[Any, ...],
    topology: BoundedTopology,
    controller: StructuralPlasticityController | None,
    attempts_so_far: int,
) -> tuple[dict[str, Any], BoundedTopology, int]:
    neighbors = _neighbors_for(arm)
    plane: StructuralObservationPlane | None = None
    if arm != "FROZEN_NO_OBSERVATION":
        plane = StructuralObservationPlane(
            NODES,
            neighbors,
            neighborhood_limit=NEIGHBORHOOD_LIMIT,
            reverse_observer_limit=REVERSE_OBSERVER_LIMIT,
            history_capacity=HISTORY_CAPACITY,
            candidate_capacity=CANDIDATE_CAPACITY,
            association_window=ASSOCIATION_WINDOW,
            maximum_score=MAXIMUM_SCORE,
            propagation_delay=GROWTH_DELAY,
        )
    observation_audit: list[dict[str, Any]] = []
    emission_order = 0

    def observe(emitter_id: str, event_id: str | int, timestamp: float) -> None:
        nonlocal emission_order
        if plane is None:
            raise RuntimeError("observation callback invoked while observation is disabled")
        if len(observation_audit) >= RUNTIME_EVENT_BUDGET * (1 + REVERSE_OBSERVER_LIMIT):
            raise BufferError("bounded Luna-40 observation audit capacity reached")
        plane.observe_emission(emitter_id, event_id, timestamp)
        for observer in (emitter_id, *sorted(
            source for source, destinations in neighbors.items() if emitter_id in destinations
        )):
            observation_audit.append(
                {
                    "observer": observer,
                    "emitter_id": emitter_id,
                    "event_id": event_id,
                    "timestamp": float(timestamp),
                    "callback_emission_order": emission_order,
                }
            )
        emission_order += 1

    neurons = (
        MultiExcursionNeuron("source", config=E1Config(event_budget=4096)),
        MultiExcursionNeuron("relay", config=E1Config(event_budget=4096)),
        MultiExcursionNeuron(
            "destination",
            config=E1Config(event_budget=4096, integration=IntegrationConfig()),
        ),
    )
    saved_neurons: dict[str, dict[str, Any]] = {}
    occupancy = _OccupancyAudit()
    original_reset = MultiExcursionNeuron.reset
    original_ledger_init = EligibilityLedger.__init__
    original_record_activity = EligibilityLedger.record_activity
    original_apply_signal = EligibilityLedger.apply_signal

    def capture_reset(neuron: MultiExcursionNeuron, *, timestamp: float = 0.0) -> None:
        emissions = []
        for item in neuron.emissions:
            event = _jsonable(item)
            event["emitter_id"] = item.source
            emissions.append(event)
        saved_neurons[neuron.neuron_id] = {
            "emissions": emissions,
            "integration_trace": [_jsonable(item) for item in neuron.integration_trace],
            "x": float(neuron.state),
            "z": (
                None if neuron.integration_state is None
                else float(neuron.integration_state)
            ),
            "last_update_timestamp": float(neuron.last_update_timestamp),
        }
        original_reset(neuron, timestamp=timestamp)

    def ledger_init(ledger: EligibilityLedger, *args: Any, **kwargs: Any) -> None:
        original_ledger_init(ledger, *args, **kwargs)
        occupancy.register(ledger)

    def record_activity(ledger: EligibilityLedger, event: Any) -> Any:
        return occupancy.observe(
            ledger,
            lambda: original_record_activity(ledger, event),
            event.timestamp,
            getattr(event.payload, "trace_id", None),
        )

    def apply_signal(ledger: EligibilityLedger, event: Any) -> Any:
        return occupancy.observe(
            ledger,
            lambda: original_apply_signal(ledger, event),
            event.timestamp,
            getattr(event.payload, "trace_id", None),
        )

    topology_before = _topology_records(topology)
    batches = _point_batches(points)
    input_digest = _digest(batches)
    character_id = f"c{seed:02d}-{sequence_index:03d}"
    runtime = ExcursionCharacterRuntime(
        neurons,
        topology,
        queue_capacity=QUEUE_CAPACITY,
        event_budget=RUNTIME_EVENT_BUDGET,
        settling_horizon=SETTLING_HORIZON,
        prediction_capacity=PREDICTION_CAPACITY,
        prediction_expiry=PREDICTION_EXPIRY,
        max_activity_events=MAX_ACTIVITY_EVENTS,
        namespace=f"luna40-seed-{seed}",
        emission_observer=observe if plane is not None else None,
        eligibility_capacity=ELIGIBILITY_CAPACITY,
    )
    try:
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(MultiExcursionNeuron, "reset", capture_reset))
            stack.enter_context(mock.patch.object(EligibilityLedger, "__init__", ledger_init))
            stack.enter_context(mock.patch.object(
                EligibilityLedger, "record_activity", record_activity
            ))
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
                reward_message_id=f"neutral-{character_id}",
            )
    except EligibilityCapacityError as error:
        raise StopCondition(
            "eligibility capacity error",
            {
                "arm": arm,
                "seed": seed,
                "character_id": character_id,
                "capacity_errors": occupancy.capacity_errors,
                "message": str(error),
            },
        ) from error
    except (BufferError, TopologyCapacityError) as error:
        raise StopCondition(
            "bounded capacity error",
            {
                "arm": arm,
                "seed": seed,
                "character_id": character_id,
                "error_type": type(error).__name__,
                "message": str(error),
                "queue_peak": runtime_result.peak_queue_occupancy
                if "runtime_result" in locals() else None,
                "processed_events": runtime_result.execution.processed_event_count
                if "runtime_result" in locals() else None,
            },
        ) from error
    except Exception as error:
        raise StopCondition(
            "runtime exception",
            {
                "arm": arm,
                "seed": seed,
                "character_id": character_id,
                "error_type": type(error).__name__,
                "message": str(error),
            },
        ) from error

    if (
        runtime_result.incomplete_settling
        or not runtime_result.execution.completed
        or runtime_result.execution.budget_exhausted
        or runtime_result.execution.pending_event_count != 0
        or runtime.queue is not None
        or runtime.sidecar
    ):
        raise StopCondition(
            "incomplete settling or live runtime state",
            {
                "arm": arm,
                "seed": seed,
                "character_id": character_id,
                "incomplete_settling": runtime_result.incomplete_settling,
                "execution": _jsonable(runtime_result.execution),
                "queue_is_none": runtime.queue is None,
                "sidecar_count": len(runtime.sidecar),
            },
        )
    if len(saved_neurons) != len(NODES):
        raise StopCondition(
            "neuron trace/state snapshot was not observable at teardown",
            {"saved_neurons": sorted(saved_neurons), "expected": list(NODES)},
        )
    ledgers = occupancy.finalize()
    if (
        len(ledgers) != len(NODES)
        or any(item["configured_capacity"] != ELIGIBILITY_CAPACITY for item in ledgers)
        or any(not item["reconciles"] for item in ledgers)
        or any(item["peak_occupancy"] >= ELIGIBILITY_CAPACITY for item in ledgers)
        or occupancy.capacity_errors
    ):
        raise StopCondition(
            "eligibility capacity/occupancy stop condition",
            {"ledgers": ledgers, "capacity_errors": occupancy.capacity_errors},
        )
    if plane is None:
        observation_snapshot = None
        observation_audit = []
        candidates: tuple[CandidateEvidence, ...] = ()
        candidate_rejections = 0
        rejection_reasons: tuple[tuple[str, int], ...] = ()
        observation_work = 0
    else:
        observation_snapshot = plane.freeze()
        if (
            observation_snapshot.observation_count != emission_order
            or observation_snapshot.observation_work != len(observation_audit)
        ):
            raise StopCondition(
                "structural observation accounting mismatch",
                {
                    "emissions": emission_order,
                    "observation_count": observation_snapshot.observation_count,
                    "observation_work": observation_snapshot.observation_work,
                    "retained_observation_audit": len(observation_audit),
                },
            )
        candidates = observation_snapshot.candidates
        candidate_rejections = observation_snapshot.candidate_rejections
        rejection_reasons = observation_snapshot.candidate_rejection_reasons
        observation_work = observation_snapshot.observation_work

    emissions = [
        emission
        for node in NODES
        for emission in saved_neurons[node]["emissions"]
    ]
    emissions.sort(key=lambda item: (item["timestamp"], item["sequence"], item["source"]))
    source_emissions = [item for item in emissions if item["source"] == "source"]
    destination_emissions_raw = [
        item for item in emissions if item["source"] == "destination"
    ]
    integration_trace = saved_neurons["destination"]["integration_trace"]
    destination_emissions = [
        _destination_classification(item, integration_trace)
        for item in destination_emissions_raw
    ]
    routes = _route_records(runtime_result.trace, emissions, topology_before)
    destination_routes = [
        route for route in routes if route["receiving_node"] == "destination"
    ]
    enriched_trace, effective_drive = _integration_and_drive(
        integration_trace,
        destination_routes,
        destination_emissions,
        saved_neurons["destination"],
    )
    if any(
        not math.isfinite(float(value))
        for node_state in saved_neurons.values()
        for key, value in node_state.items()
        if key in ("x", "z") and value is not None
    ):
        raise StopCondition(
            "non-finite neuron state",
            {"arm": arm, "seed": seed, "character_id": character_id},
        )

    pairs, association_counts = _observer_associations(
        observation_audit,
        neighbors=neighbors,
    )
    candidate_records = [_jsonable(item) for item in candidates]
    for candidate in candidate_records:
        key = (candidate["source"], candidate["destination"])
        candidate["raw_association_opportunities"] = association_counts.get(key, 0)
        candidate["association_evidence"] = [
            pair for pair in pairs
            if pair["source"] == candidate["source"]
            and pair["destination"] == candidate["destination"]
        ]
    if any(
        min(MAXIMUM_SCORE, association_counts.get(
            (candidate["source"], candidate["destination"]), 0
        )) != float(candidate["score"])
        for candidate in candidate_records
    ):
        raise StopCondition(
            "candidate score is not reconstructible from actual local observations",
            {"candidates": candidate_records, "associations": pairs},
        )

    pre_attempt_edges = _topology_records(topology)
    growth_attempt: dict[str, Any] = {
        "enabled": arm == "LOCAL_GROWTH_ENABLED",
        "attempted": False,
        "status": (
            "observation_only" if arm == "FROZEN_OBSERVATION_ONLY"
            else "no_candidate" if arm in ("LOCAL_GROWTH_ENABLED", "NO_LOCAL_EVIDENCE_CONTROL")
            else "disabled"
        ),
        "reason": None,
        "candidate_count": len(candidates),
        "selected_candidate": None,
        "selected_rank": None,
        "attempt_budget_before": attempts_so_far,
        "attempt_budget_limit": GROWTH_ATTEMPT_BUDGET,
        "attempt_budget_exhausted": False,
        "controller_candidate_capacity": (
            len(NODES) * CANDIDATE_CAPACITY if controller is not None else 0
        ),
        "controller_candidate_occupancy_before": (
            controller.state.candidate_count if controller is not None else 0
        ),
        "controller_candidate_occupancy_after": (
            controller.state.candidate_count if controller is not None else 0
        ),
        "topology_before_attempt": pre_attempt_edges,
        "topology_after_attempt": pre_attempt_edges,
        "mutation_result": None,
    }
    attempts_after = attempts_so_far
    if arm == "LOCAL_GROWTH_ENABLED" and candidates:
        if attempts_so_far >= GROWTH_ATTEMPT_BUDGET:
            growth_attempt["status"] = "budget_exhausted"
            growth_attempt["reason"] = "growth_attempt_budget"
            growth_attempt["attempt_budget_exhausted"] = True
        else:
            if controller is None:
                raise StopCondition("growth controller is missing", {})
            # The runtime has returned a complete result and destroyed queue,
            # sidecar, pending neuron state, predictor and ledgers before this call.
            selected = controller.select(candidates)
            if selected is None:
                growth_attempt["status"] = "candidate_unavailable"
                growth_attempt["reason"] = "no_valid_candidate"
            else:
                ordered = list(candidates)
                selected_rank = ordered.index(selected) + 1
                growth_attempt.update(
                    {
                        "attempted": True,
                        "status": "attempted",
                        "selected_candidate": _jsonable(selected),
                        "selected_rank": selected_rank,
                        "attempt_budget_before": attempts_so_far,
                    }
                )
                mutation = controller.grow(selected)
                attempts_after += 1
                topology = controller.topology
                growth_attempt["status"] = mutation.status
                growth_attempt["reason"] = mutation.reason
                growth_attempt["mutation_result"] = {
                    "status": mutation.status,
                    "reason": mutation.reason,
                    "edge": None if mutation.edge is None else _edge_record(mutation.edge),
                }
                growth_attempt["topology_after_attempt"] = _topology_records(topology)
                if mutation.status == "grown":
                    grown_edge = mutation.edge
                    if grown_edge is None or (
                        grown_edge.edge_weight != 1.0
                        or grown_edge.divider_strength != 1.0
                        or grown_edge.reference != 0.0
                        or grown_edge.propagation_delay != GROWTH_DELAY
                    ):
                        raise StopCondition(
                            "controller-admitted edge violates fixed Model-B defaults",
                            {"edge": None if grown_edge is None else _edge_record(grown_edge)},
                        )
                growth_attempt["controller_candidate_occupancy_after"] = (
                    controller.state.candidate_count
                )

    topology_after = _topology_records(topology)
    record = {
        "seed": seed,
        "character_index": sequence_index,
        "character_id": character_id,
        "arm": arm,
        "point_count": len(points),
        "input_batches": [
            {"timestamp": batch[0][0], "values": [item[1] for item in batch]}
            for batch in batches
        ],
        "input_digest": input_digest,
        "initial_topology_for_character": topology_before,
        "intermediate_topology_after_character": topology_after,
        "network_utilization_before": _network_utilization(
            # Rebuild is unnecessary: controller and topology still represent the
            # authoritative graph after the post-character decision.
            _topology_from_records(topology_before)
        ),
        "network_utilization_after": _network_utilization(topology),
        "canonical_emissions": emissions,
        "source_canonical_emissions": source_emissions,
        "routes": routes,
        "destination_receptions": destination_routes,
        "destination_integration_trace": enriched_trace,
        "destination_emissions": destination_emissions,
        "effective_drive": effective_drive,
        "structural": {
            "observation_enabled": plane is not None,
            "neighbors": {key: list(value) for key, value in neighbors.items()},
            "observations": observation_audit,
            "observation_count": emission_order,
            "observation_work": observation_work,
            "candidate_opportunities": len(pairs),
            "association_pairs": pairs,
            "candidates": candidate_records,
            "candidate_rejections": candidate_rejections,
            "candidate_rejection_reasons": dict(rejection_reasons),
            "candidate_occupancy": len(candidates),
            "candidate_capacity_per_source": CANDIDATE_CAPACITY,
        },
        "growth": growth_attempt,
        "eligibility": {
            "effective_capacity_per_ledger": ELIGIBILITY_CAPACITY,
            "ledgers": ledgers,
            "capacity_errors": occupancy.capacity_errors,
        },
        "runtime": {
            "queue_capacity": QUEUE_CAPACITY,
            "queue_peak": runtime_result.peak_queue_occupancy,
            "event_budget": RUNTIME_EVENT_BUDGET,
            "events_processed": runtime_result.execution.processed_event_count,
            "events_pending": runtime_result.execution.pending_event_count,
            "settling_horizon": SETTLING_HORIZON,
            "completed": runtime_result.execution.completed,
            "incomplete_settling": runtime_result.incomplete_settling,
            "stop_status": runtime_result.execution.termination_reason,
            "execution_budget_exhausted": runtime_result.execution.budget_exhausted,
            "max_route_depth": runtime_result.max_route_depth,
            "peak_queue_occupancy": runtime_result.peak_queue_occupancy,
            "reward": 0.0,
        },
        "neuron_state_at_teardown": saved_neurons,
        "runtime_event_trace": [_jsonable(row) for row in runtime_result.trace],
    }
    return record, topology, attempts_after


def _topology_from_records(records: list[dict[str, Any]]) -> BoundedTopology:
    return BoundedTopology.from_edges(
        NODES,
        tuple(
            Edge(
                item["source"],
                item["destination"],
                item["delay"],
                routing_cost=item["routing_cost"],
                edge_weight=item["w"],
                divider_strength=item["d"],
                reference=item["r"],
                legacy_identity=item["legacy_identity"],
            )
            for item in records
        ),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=3,
        routing_capacity=3,
    )


def _run_once(seeds: tuple[int, ...]) -> dict[str, Any]:
    results: dict[str, Any] = {
        "schema": "TPCN-LUNA40-EXISTING-GROWTH-EFFECTIVE-ROUTED-DRIVE-RESULTS-1",
        "start_revision": START_REVISION,
        "arms": list(ARMS),
        "environment": {"python": sys.version, "platform": platform.platform()},
        "runs": {arm: {} for arm in ARMS},
        "stopped": None,
        "equal_time_negative_control": None,
    }
    try:
        equal_time = _equal_time_negative_control()
        if not equal_time["passed"]:
            raise StopCondition("equal-time negative evidence control failed", equal_time)
        results["equal_time_negative_control"] = equal_time
        for arm in ARMS:
            for seed in seeds:
                sequences = luna39.base._training_point_sequences(seed)
                if len(sequences) != 64:
                    raise StopCondition(
                        "Luna-39 source generator did not yield 64 point sequences",
                        {"seed": seed, "sequence_count": len(sequences)},
                    )
                topology = _initial_topology()
                initial_edges = _topology_records(topology)
                controller = (
                    StructuralPlasticityController(
                        topology,
                        candidate_capacity=len(NODES) * CANDIDATE_CAPACITY,
                        max_growth_per_adaptation=1,
                        local_neighbors=_neighbors_for(arm),
                    )
                    if arm == "LOCAL_GROWTH_ENABLED"
                    else None
                )
                attempts = 0
                records = []
                for sequence_index, points in enumerate(sequences):
                    record, topology, attempts = _run_character(
                        arm=arm,
                        seed=seed,
                        sequence_index=sequence_index,
                        points=points,
                        topology=topology,
                        controller=controller,
                        attempts_so_far=attempts,
                    )
                    records.append(record)
                results["runs"][arm][str(seed)] = {
                    "initial_topology": initial_edges,
                    "final_topology": _topology_records(topology),
                    "growth_attempts_used": attempts,
                    "growth_attempt_budget": GROWTH_ATTEMPT_BUDGET,
                    "characters": records,
                }
        _verify_control_invariance(results)
    except StopCondition as error:
        results["stopped"] = {"reason": error.reason, "detail": error.detail}
    except Exception as error:
        results["stopped"] = {
            "reason": "unexpected exception",
            "detail": {"type": type(error).__name__, "message": str(error)},
        }
    return results


def _neural_projection(record: dict[str, Any]) -> dict[str, Any]:
    """Fields that must be identical in observation/no-local controls."""
    return {
        "input_digest": record["input_digest"],
        "input_batches": record["input_batches"],
        "canonical_emissions": record["canonical_emissions"],
        "routes": record["routes"],
        "destination_integration_trace": record["destination_integration_trace"],
        "destination_emissions": record["destination_emissions"],
        "neuron_state_at_teardown": record["neuron_state_at_teardown"],
        "runtime_event_trace": record["runtime_event_trace"],
        "eligibility": record["eligibility"],
        "runtime": record["runtime"],
    }


def _verify_control_invariance(results: dict[str, Any]) -> None:
    no_observation = results["runs"]["FROZEN_NO_OBSERVATION"]
    observation_only = results["runs"]["FROZEN_OBSERVATION_ONLY"]
    no_local = results["runs"]["NO_LOCAL_EVIDENCE_CONTROL"]
    for seed in no_observation:
        controls = (
            (observation_only[seed], "FROZEN_OBSERVATION_ONLY"),
            (no_local[seed], "NO_LOCAL_EVIDENCE_CONTROL"),
        )
        for key, first in enumerate(no_observation[seed]["characters"]):
            for second_run, arm in controls:
                second = second_run["characters"][key]
                if _neural_projection(first) != _neural_projection(second):
                    raise StopCondition(
                        "observation-only or no-local-evidence control changed neural behavior",
                        {
                            "seed": seed,
                            "character_id": first["character_id"],
                            "control_arm": arm,
                        },
                    )
                if first["initial_topology_for_character"] != second["initial_topology_for_character"]:
                    raise StopCondition(
                        "frozen/no-local control topology differs",
                        {"seed": seed, "character_id": first["character_id"], "arm": arm},
                    )
    for seed, seed_record in no_local.items():
        if (
            seed_record["final_topology"] != seed_record["initial_topology"]
            or any(
                character["structural"]["candidates"]
                or character["growth"]["attempted"]
                for character in seed_record["characters"]
            )
        ):
            raise StopCondition(
                "no-local-evidence control formed or admitted a candidate",
                {"seed": seed},
            )


def _aggregate_arm_seed(seed_record: dict[str, Any]) -> dict[str, Any]:
    characters = seed_record["characters"]
    routes = [route for item in characters for route in item["routes"]]
    dest_emissions = [
        emission for item in characters for emission in item["destination_emissions"]
    ]
    src_emissions = [
        emission for item in characters for emission in item["source_canonical_emissions"]
    ]
    emissions_by_node = {
        node: [
            emission
            for character in characters
            for emission in character["canonical_emissions"]
            if emission["emitter_id"] == node
        ]
        for node in NODES
    }
    destination_trace = [
        entry for item in characters for entry in item["destination_integration_trace"]
    ]
    attempts = [item["growth"] for item in characters if item["growth"]["attempted"]]
    admissions = [item for item in attempts if item["status"] == "grown"]
    used_edges = {item["edge_identity"] for item in routes}
    return {
        "characters": {"numerator": len(characters), "denominator": len(characters)},
        "source_emissions": len(src_emissions),
        "canonical_emissions_by_node": {
            node: len(items) for node, items in emissions_by_node.items()
        },
        "emitting_characters_by_node": {
            node: {
                "numerator": sum(
                    any(
                        emission["emitter_id"] == node
                        for emission in character["canonical_emissions"]
                    )
                    for character in characters
                ),
                "denominator": len(characters),
            }
            for node in NODES
        },
        "routed_transfers": len(routes),
        "routes_by_edge": {
            edge: sum(route["edge_identity"] == edge for route in routes)
            for edge in sorted(used_edges)
        },
        "characters_using_each_edge": {
            edge: {
                "numerator": sum(
                    any(
                        route["edge_identity"] == edge
                        for route in character["routes"]
                    )
                    for character in characters
                ),
                "denominator": len(characters),
            }
            for edge in sorted(
                {
                    route["edge_identity"]
                    for character in characters
                    for route in character["routes"]
                }
            )
        },
        "destination_receptions": len(
            [route for route in routes if route["receiving_node"] == "destination"]
        ),
        "destination_receiving_characters": {
            "numerator": sum(
                any(route["receiving_node"] == "destination" for route in item["routes"])
                for item in characters
            ),
            "denominator": len(characters),
        },
        "destination_z_updates": len(destination_trace),
        "destination_max_abs_z": max(
            (item["effective_drive"]["maximum_abs_z_observed"] for item in characters),
            default=0.0,
        ),
        "destination_emissions": {
            "total": len(dest_emissions),
            "direct": sum(item["classification"] == "direct" for item in dest_emissions),
            "integrated_discharge": sum(
                item["classification"] == "integrated_discharge" for item in dest_emissions
            ),
        },
        "destination_emitting_characters": sum(
            bool(item["destination_emissions"]) for item in characters
        ),
        "destination_emitting_characters_ratio": {
            "numerator": sum(bool(item["destination_emissions"]) for item in characters),
            "denominator": len(characters),
        },
        "source_emitting_characters": {
            "numerator": sum(
                any(emission["emitter_id"] == "source" for emission in item["canonical_emissions"])
                for item in characters
            ),
            "denominator": len(characters),
        },
        "candidate_opportunities": sum(
            item["structural"]["candidate_opportunities"] for item in characters
        ),
        "candidate_records": sum(
            len(item["structural"]["candidates"]) for item in characters
        ),
        "candidate_rejections": sum(
            item["structural"]["candidate_rejections"] for item in characters
        ),
        "growth_attempts": len(attempts),
        "successful_admissions": len(admissions),
        "used_shortcut_transfers": sum(
            route["edge_identity"] == "source->destination" for route in routes
        ),
        "used_relay_path_transfers": sum(
            route["edge_identity"] in ("source->relay", "relay->destination")
            for route in routes
        ),
        "runtime_events_processed": sum(
            item["runtime"]["events_processed"] for item in characters
        ),
        "maximum_route_depth": max(
            (item["runtime"]["max_route_depth"] for item in characters),
            default=0,
        ),
        "queue_peak": max(
            (item["runtime"]["queue_peak"] for item in characters),
            default=0,
        ),
        "eligibility_max_peak": max(
            (
                ledger["peak_occupancy"]
                for item in characters
                for ledger in item["eligibility"]["ledgers"]
            ),
            default=0,
        ),
        "eligibility_reconciliation_errors": sum(
            not ledger["reconciles"]
            for item in characters
            for ledger in item["eligibility"]["ledgers"]
        ),
    }


def _drive_interpretation(results: dict[str, Any]) -> dict[str, Any]:
    frozen = results["runs"]["FROZEN_NO_OBSERVATION"]
    growth = results["runs"]["LOCAL_GROWTH_ENABLED"]
    per_seed: dict[str, Any] = {}
    for seed, growth_run in growth.items():
        frozen_records = {
            item["character_id"]: item for item in frozen[seed]["characters"]
        }
        admitted_chars = [
            item for item in growth_run["characters"]
            if item["growth"]["status"] == "grown"
        ]
        shortcut_routes = [
            route
            for character in growth_run["characters"]
            for route in character["routes"]
            if route["edge_identity"] == "source->destination"
        ]
        drive_increase_chars = []
        boundary_cross_chars = []
        integrated_emission_chars = []
        paired_deltas = []
        for character in growth_run["characters"]:
            frozen_character = frozen_records[character["character_id"]]
            growth_z = character["effective_drive"]["maximum_abs_z_observed"]
            frozen_z = frozen_character["effective_drive"]["maximum_abs_z_observed"]
            delta = growth_z - frozen_z
            paired_deltas.append(delta)
            if delta > 1e-12 and any(
                route["edge_identity"] == "source->destination"
                for route in character["routes"]
            ):
                drive_increase_chars.append(character["character_id"])
            if any(
                route["edge_identity"] == "source->destination"
                for route in character["routes"]
            ) and any(
                abs(float(entry["z_after_input"])) >= float(entry["theta_z"])
                and entry["integrated"]
                for entry in character["destination_integration_trace"]
            ):
                boundary_cross_chars.append(character["character_id"])
            if any(
                emission["classification"] == "integrated_discharge"
                for emission in character["destination_emissions"]
            ):
                integrated_emission_chars.append(character["character_id"])

        if not admitted_chars:
            branch = "NO LEGAL EDGE ADMISSION"
        elif not shortcut_routes:
            branch = "ADMITTED BUT NO LATER CAUSALLY OBSERVED SHORTCUT TRANSFER"
        elif not drive_increase_chars:
            branch = "SHORTCUT USED; NO ATTRIBUTABLE MAX-|z| INCREASE VS PAIRED FROZEN RUN"
        elif boundary_cross_chars:
            branch = "ENDOGENOUS DRIVE REACHED"
        else:
            branch = "ENDOGENOUS DRIVE INCREASED, BOUNDARY NOT REACHED"
        per_seed[seed] = {
            "interpretation": branch,
            "admitted_character_ids": [item["character_id"] for item in admitted_chars],
            "later_shortcut_transfer_count": len(shortcut_routes),
            "later_shortcut_transfer_characters": sorted(
                {
                    character["character_id"]
                    for character in growth_run["characters"]
                    if any(
                        route["edge_identity"] == "source->destination"
                        for route in character["routes"]
                    )
                }
            ),
            "paired_max_abs_z_deltas_all_characters": paired_deltas,
            "characters_with_shortcut_attributable_max_abs_z_increase": drive_increase_chars,
            "characters_with_shortcut_route_and_trace_z_at_or_above_theta_Z": boundary_cross_chars,
            "integration_mediated_emission_characters": integrated_emission_chars,
            "destination_emissions": _aggregate_arm_seed(growth_run)["destination_emissions"],
        }
    return {
        "all_seed_count": len(per_seed),
        "all_seed_interpretations": per_seed,
        "prohibited_inference_boundary": (
            "Results apply only to the declared bounded stream/topology/configuration; "
            "no task efficacy, classification, generalization, growth usefulness, "
            "resource benefit, calibration, or ACP-0008 promotion is inferred."
        ),
    }


def _summarize(results: dict[str, Any]) -> dict[str, Any]:
    per_arm: dict[str, Any] = {}
    for arm in ARMS:
        seed_summaries = {
            seed: _aggregate_arm_seed(seed_record)
            for seed, seed_record in results["runs"][arm].items()
        }
        total: dict[str, Any] = {
            "seed_count": len(seed_summaries),
            "character_executions": sum(
                item["characters"]["numerator"] for item in seed_summaries.values()
            ),
        }
        for key in (
            "source_emissions",
            "routed_transfers",
            "destination_receptions",
            "destination_z_updates",
            "candidate_opportunities",
            "candidate_records",
            "candidate_rejections",
            "growth_attempts",
            "successful_admissions",
            "used_shortcut_transfers",
            "used_relay_path_transfers",
            "runtime_events_processed",
            "eligibility_reconciliation_errors",
        ):
            total[key] = sum(item[key] for item in seed_summaries.values())
        total["source_emitting_characters"] = {
            "numerator": sum(
                item["source_emitting_characters"]["numerator"]
                for item in seed_summaries.values()
            ),
            "denominator": sum(
                item["source_emitting_characters"]["denominator"]
                for item in seed_summaries.values()
            ),
        }
        total["destination_receiving_characters"] = {
            "numerator": sum(
                item["destination_receiving_characters"]["numerator"]
                for item in seed_summaries.values()
            ),
            "denominator": sum(
                item["destination_receiving_characters"]["denominator"]
                for item in seed_summaries.values()
            ),
        }
        total["destination_emitting_characters_ratio"] = {
            "numerator": sum(
                item["destination_emitting_characters_ratio"]["numerator"]
                for item in seed_summaries.values()
            ),
            "denominator": sum(
                item["destination_emitting_characters_ratio"]["denominator"]
                for item in seed_summaries.values()
            ),
        }
        total["destination_emissions"] = {
            key: sum(item["destination_emissions"][key] for item in seed_summaries.values())
            for key in ("total", "direct", "integrated_discharge")
        }
        total["destination_emitting_characters"] = sum(
            item["destination_emitting_characters"] for item in seed_summaries.values()
        )
        total["emitting_characters_by_node"] = {
            node: {
                "numerator": sum(
                    item["emitting_characters_by_node"][node]["numerator"]
                    for item in seed_summaries.values()
                ),
                "denominator": sum(
                    item["emitting_characters_by_node"][node]["denominator"]
                    for item in seed_summaries.values()
                ),
            }
            for node in NODES
        }
        total["canonical_emissions_by_node"] = {
            node: sum(
                item["canonical_emissions_by_node"][node]
                for item in seed_summaries.values()
            )
            for node in NODES
        }
        total["destination_max_abs_z"] = max(
            (item["destination_max_abs_z"] for item in seed_summaries.values()),
            default=0.0,
        )
        total["queue_peak"] = max(
            (item["queue_peak"] for item in seed_summaries.values()), default=0
        )
        total["eligibility_max_peak"] = max(
            (item["eligibility_max_peak"] for item in seed_summaries.values()),
            default=0,
        )
        total["maximum_route_depth"] = max(
            (item["maximum_route_depth"] for item in seed_summaries.values()),
            default=0,
        )
        all_route_edges = sorted(
            {
                edge
                for item in seed_summaries.values()
                for edge in item["routes_by_edge"]
            }
        )
        total["routes_by_edge"] = {
            edge: sum(
                item["routes_by_edge"].get(edge, 0)
                for item in seed_summaries.values()
            )
            for edge in all_route_edges
        }
        total["characters_using_each_edge"] = {
            edge: {
                "numerator": sum(
                    item["characters_using_each_edge"].get(edge, {}).get("numerator", 0)
                    for item in seed_summaries.values()
                ),
                "denominator": sum(
                    item["characters"]["denominator"] for item in seed_summaries.values()
                ),
            }
            for edge in all_route_edges
        }
        per_arm[arm] = {"per_seed": seed_summaries, "all_seed_total": total}
    return {
        "schema": "TPCN-LUNA40-EXISTING-GROWTH-EFFECTIVE-ROUTED-DRIVE-SUMMARY-1",
        "start_revision": START_REVISION,
        "arms": per_arm,
        "paired_growth_interpretation": _drive_interpretation(results),
        "equal_time_negative_control": results.get("equal_time_negative_control"),
        "replay": results.get("replay"),
        "stop": results.get("stopped"),
    }


def config_record() -> dict[str, Any]:
    return {
        "schema": "TPCN-LUNA40-EXISTING-GROWTH-EFFECTIVE-ROUTED-DRIVE-CONFIG-1",
        "start_revision": START_REVISION,
        "stream": {
            "generator": "read-only Luna-39/Luna-34 make_spiral_dataset",
            "seeds": list(SEEDS),
            "examples_per_class": 16,
            "training_seed": "12007 + seed",
            "evaluation_seed": "22017 + seed (generated but not consumed)",
            "stream_order": "random.Random(330000 + seed).shuffle(point_sequences)",
            "point_transform": "point.x + point.y at existing timestamp",
            "same_timestamp_batching": True,
            "labels_and_label_bearing_metadata_read": False,
        },
        "network": {
            "nodes": list(NODES),
            "initial_edges": [
                {"source": "source", "destination": "relay", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
                {"source": "relay", "destination": "destination", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
            ],
            "fan_in_limit": 2,
            "fan_out_limit": 2,
            "edge_capacity": 3,
            "routing_capacity": 3,
            "possible_growth": {
                "source": "source",
                "destination": "destination",
                "delay": GROWTH_DELAY,
                "w": 1.0,
                "d": 1.0,
                "r": 0.0,
                "created_only_by": "accepted StructuralPlasticityController admission from plane evidence",
            },
        },
        "neurons": {
            "source": {"class": "MultiExcursionNeuron", "E1Config": {"event_budget": 4096, "integration": None}},
            "relay": {"class": "MultiExcursionNeuron", "E1Config": {"event_budget": 4096, "integration": None}},
            "destination": {
                "class": "MultiExcursionNeuron",
                "E1Config": {
                    "event_budget": 4096,
                    "theta_E": 1.0,
                    "integration": {
                        "decay_rate_z": 0.1,
                        "input_gain": 1.0,
                        "theta_Z": 1.0,
                        "z_max": 4.0,
                    },
                },
            },
        },
        "runtime": {
            "queue_capacity": QUEUE_CAPACITY,
            "runtime_event_budget": RUNTIME_EVENT_BUDGET,
            "settling_horizon": SETTLING_HORIZON,
            "prediction_capacity": PREDICTION_CAPACITY,
            "prediction_expiry": PREDICTION_EXPIRY,
            "max_activity_events": MAX_ACTIVITY_EVENTS,
            "eligibility_capacity_per_ledger": ELIGIBILITY_CAPACITY,
            "neutral_reward": 0.0,
            "external_input_destination": "source",
        },
        "structural_policy": {
            "policy": "e2_local_temporal",
            "growth_neighbors": {"source": ["destination"], "relay": [], "destination": []},
            "no_local_neighbors": {"source": [], "relay": [], "destination": []},
            "neighborhood_limit": NEIGHBORHOOD_LIMIT,
            "reverse_observer_limit": REVERSE_OBSERVER_LIMIT,
            "association_window": ASSOCIATION_WINDOW,
            "history_capacity": HISTORY_CAPACITY,
            "candidate_capacity_per_source": CANDIDATE_CAPACITY,
            "maximum_score": MAXIMUM_SCORE,
            "structural_growth_delay": GROWTH_DELAY,
            "growth_attempt_budget_total_per_run": GROWTH_ATTEMPT_BUDGET,
            "maximum_successful_growths_per_character": 1,
            "evidence_source": "actual canonical emission identity and timestamp only",
        },
        "arms": list(ARMS),
        "total_character_executions_per_replay": len(SEEDS) * 64 * len(ARMS),
        "replay_count": 2,
        "endpoint": "actual route identities/payloads and destination ACP-0008 z trace; no task score",
    }


def run_experiment(
    output_directory: Path = ARTIFACT_DIRECTORY,
    *,
    seeds: tuple[int, ...] = SEEDS,
) -> tuple[dict[str, Any], dict[str, Any]]:
    first = _run_once(seeds)
    first_digest = _digest(
        {
            "runs": first["runs"],
            "equal_time_negative_control": first["equal_time_negative_control"],
        }
    )
    if first["stopped"] is not None:
        first["replay"] = {
            "initial_digest": first_digest,
            "replay_digest": None,
            "identical": False,
            "not_run_reason": "execution stopped before complete first pass",
        }
        summary = _summarize(first)
    else:
        replay = _run_once(seeds)
        replay_digest = _digest(
            {
                "runs": replay["runs"],
                "equal_time_negative_control": replay["equal_time_negative_control"],
            }
        )
        identical = replay["stopped"] is None and first_digest == replay_digest
        first["replay"] = {
            "initial_digest": first_digest,
            "replay_digest": replay_digest,
            "identical": identical,
            "replay_stop": replay["stopped"],
        }
        if not identical:
            first["stopped"] = {
                "reason": "nondeterministic full-run replay",
                "detail": {
                    "initial_digest": first_digest,
                    "replay_digest": replay_digest,
                    "replay_stop": replay["stopped"],
                },
            }
        summary = _summarize(first)
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / "config.json").write_text(
        json.dumps(config_record(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_directory / "results.json").write_text(
        json.dumps(first, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_directory / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return first, summary


def main() -> None:
    results, summary = run_experiment()
    print(
        json.dumps(
            {
                "stopped": results["stopped"],
                "replay": results.get("replay"),
                "summary": summary["paired_growth_interpretation"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
