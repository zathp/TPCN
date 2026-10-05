"""Run the bounded Luna-39 ACP-0008 propagation-to-emission diagnostic."""

from __future__ import annotations

from contextlib import ExitStack
from dataclasses import asdict
import json
import math
import platform
import sys
from pathlib import Path
from typing import Any, Callable
from unittest import mock

import run_luna34_excursion_v1_multi_emitter_bridge as base
from tpcn.eligibility import EligibilityCapacityError, EligibilityLedger
from tpcn.event_runtime import Event, EventQueue, EventType
from tpcn.excursion_neuron import (
    E1Config,
    IntegrationConfig,
    MultiExcursionNeuron,
)
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.stroke_dataset import StrokePoint


EXECUTION_BASELINE = "5ff87535ace61137892f7063a81f5f63e542fa4d"
ARMS = ("LEGACY_REPRODUCTION", "ACP0008_INTEGRATION")
CONDITIONS = base.CONDITIONS
ELIGIBILITY_CAPACITY = 1024
ARTIFACT_DIRECTORY = Path("artifacts/acp0008-luna39-propagation-emission-diagnostic")
SEEDS = (0, 1, 2, 3, 4)
_canonical_json = base._canonical_json
_digest = base._digest
_active_replay_trace: list[dict[str, Any]] = []


class StopCondition(RuntimeError):
    """A predeclared Luna-39 stop condition; the run is never retried."""

    def __init__(self, reason: str, detail: dict[str, Any]) -> None:
        super().__init__(reason)
        self.reason = reason
        self.detail = detail


class _OccupancyAudit:
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
        return sorted(records, key=lambda item: item["ledger_id"])


def experiment_config() -> dict[str, Any]:
    return {
        "schema": "TPCN-LUNA39-ACP0008-PROPAGATION-EMISSION-CONFIG-1",
        "execution_baseline": EXECUTION_BASELINE,
        "inherited_fixture": "Luna-37 EXCURSION_V1 two-node propagation diagnostic",
        "dataset": {
            "generator": "make_spiral_dataset via read-only Luna-34 helper",
            "examples_per_class": 16,
            "train_seed": "12007 + seed",
            "evaluation_seed": "22017 + seed",
            "spiral_config": asdict(base.SpiralConfig()),
            "order_stream": "random.Random(330000 + seed).shuffle(point_sequences)",
            "input_transform": "point.x + point.y at point.timestamp",
            "information_boundary": "Only example.points are consumed; labels and metadata are not read.",
            "seeds": list(SEEDS),
            "characters_per_seed": 64,
        },
        "network": {
            "nodes": list(base.NODES),
            "edge_capacity": 1,
            "routing_capacity": 1,
            "fan_in_limit": 1,
            "fan_out_limit": 1,
            "propagation_delay": 1.0,
            "divider_strength": 1.0,
            "reference": 0.0,
            "queue_capacity": base.QUEUE_CAPACITY,
            "runtime_event_budget": base.EVENT_BUDGET,
            "settling_horizon": base.SETTLING_HORIZON,
            "prediction_capacity": base.PREDICTION_CAPACITY,
            "prediction_expiry": base.PREDICTION_EXPIRY,
            "max_activity_events": base.MAX_ACTIVITY_EVENTS,
            "eligibility_capacity": {
                "value": ELIGIBILITY_CAPACITY,
                "scope": "finite per-ledger value passed explicitly to ExcursionCharacterRuntime",
                "tuned": False,
                "searched": False,
            },
            "neutral_reward": 0.0,
        },
        "arms": {
            "LEGACY_REPRODUCTION": {
                "source_neuron": {"type": "MultiExcursionNeuron", "config": asdict(E1Config())},
                "destination_neuron": {
                    "type": "MultiExcursionNeuron",
                    "config": asdict(E1Config()),
                    "integration_enabled": False,
                },
            },
            "ACP0008_INTEGRATION": {
                "source_neuron": {"type": "MultiExcursionNeuron", "config": asdict(E1Config())},
                "destination_neuron": {
                    "type": "MultiExcursionNeuron",
                    "config": asdict(E1Config(integration=IntegrationConfig())),
                    "integration_enabled": True,
                },
            },
        },
        "conditions": {
            "NO_EDGE_CONTROL": {"active_edges": []},
            "DEFAULT_STATIC_EDGE": {
                "source": "source",
                "destination": "destination",
                "edge_weight": 1.0,
                "divider_strength": 1.0,
                "reference": 0.0,
                "propagation_delay": 1.0,
            },
            "STATIC_N2_BOUND_SENSITIVITY": {
                "source": "source",
                "destination": "destination",
                "edge_weight": 2.0,
                "divider_strength": 1.0,
                "reference": 0.0,
                "propagation_delay": 1.0,
            },
        },
        "design": {
            "arms": len(ARMS),
            "conditions": len(CONDITIONS),
            "seeds": len(SEEDS),
            "characters_per_seed": 64,
            "character_condition_arm_executions": 1920,
            "full_run_replayed_twice": True,
            "growth": False,
            "pruning": False,
            "task_efficacy_endpoint": False,
        },
        "stop_conditions": [
            "legacy reproduction gate mismatch",
            "EligibilityCapacityError",
            "eligibility peak occupancy equals capacity",
            "other production exception",
            "nondeterministic replay",
            "label/class information reaches input, artifact, or result",
            "eligibility occupancy does not reconcile",
            "required events or integration_trace are not observable",
            "non-finite neuron state",
        ],
    }


def _replay_destination_with_config(
    routed: list[dict[str, Any]],
    *,
    horizon: float,
    config: E1Config,
) -> tuple[list[dict[str, Any]], tuple[dict[str, Any], ...], float, bool, float, str]:
    neuron = MultiExcursionNeuron("destination", config=config)
    queue: EventQueue[Event] = EventQueue(base.QUEUE_CAPACITY)
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
            min(config.x_max, neuron.state * math.exp(-config.decay_rate * elapsed)),
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
            max_pre_threshold_magnitude = max(max_pre_threshold_magnitude, abs(state_before))
            threshold_crossed = previous_mode.value == "N" and neuron.mode.value != "N"
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
        min(config.x_max, neuron.state * math.exp(-config.decay_rate * final_elapsed)),
    )
    _active_replay_trace[:] = [
        base._jsonable(entry) for entry in neuron.integration_trace
    ]
    return (
        state_records,
        tuple(replay_emissions),
        max_pre_threshold_magnitude,
        threshold_crossed,
        final_state,
        neuron.mode.value,
    )


def _derived_emission_classification(
    trace: list[dict[str, Any]], emission: dict[str, Any]
) -> str:
    matches = [
        entry for entry in trace
        if entry.get("emission_id") == emission["event_id"]
        and entry.get("emission_timestamp") == emission["timestamp"]
    ]
    if len(matches) != 1:
        raise StopCondition(
            "destination emission cannot be reconstructed from integration_trace",
            {"emission": emission, "matching_trace_entries": len(matches)},
        )
    entry = matches[0]
    discharge = float(entry["discharge_amount"])
    prior_z = float(entry["z_after_decay"])
    z_after_input = float(entry["z_after_input"])
    theta_z = float(entry["theta_z"])
    earlier_integrations = [
        previous for previous in trace
        if previous["timestamp"] < entry["timestamp"]
        and previous["integrated"]
        and previous["z_after_input"] != 0.0
    ]
    if (
        discharge != 0.0
        and bool(entry["integrated"])
        and prior_z != 0.0
        and len(earlier_integrations) >= 1
        and abs(z_after_input) >= theta_z
    ):
        return "integrated_discharge"
    if (
        discharge == 0.0
        and not bool(entry["integrated"])
        and abs(float(entry["x_after_input"])) >= float(entry["theta_e"])
        and z_after_input == prior_z
    ):
        return "direct"
    return "inconsistent"


def _integration_timing_analysis(
    trace: list[dict[str, Any]],
    emissions: list[dict[str, Any]],
    *,
    input_gain: float,
) -> list[dict[str, Any]]:
    analyses = []
    for emission in emissions:
        if emission["classification"] != "integrated_discharge":
            continue
        discharge_entry = next(
            entry for entry in trace
            if entry.get("emission_id") == emission["event_id"]
            and entry.get("emission_timestamp") == emission["timestamp"]
        )
        last_discharge_index = max(
            (
                index for index, entry in enumerate(trace)
                if entry["timestamp"] < discharge_entry["timestamp"]
                and entry["discharge_amount"] != 0.0
            ),
            default=-1,
        )
        candidates = [
            entry for index, entry in enumerate(trace)
            if index > last_discharge_index
            and entry["timestamp"] <= discharge_entry["timestamp"]
            and entry["integrated"]
        ]
        receptions = []
        previous_timestamp = None
        previous_residual = None
        for entry in candidates:
            timestamp = entry["timestamp"]
            receptions.append(
                {
                    "routed_emission_event_id": entry["routed_emission_event_id"],
                    "timestamp": timestamp,
                    "inter_arrival_gap": (
                        None if previous_timestamp is None else timestamp - previous_timestamp
                    ),
                    "z_before_decay": entry["z_before_decay"],
                    "z_after_decay": entry["z_after_decay"],
                    "slow_state_retained_fraction": (
                        None
                        if previous_residual in (None, 0.0)
                        else entry["z_after_decay"] / previous_residual
                    ),
                    "input_value": entry["input_value"],
                    "slow_input_contribution": input_gain * entry["input_value"],
                    "z_after_input": entry["z_after_input"],
                }
            )
            previous_timestamp = timestamp
            previous_residual = entry["z_post_discharge"]
        analyses.append(
            {
                "emission_event_id": emission["event_id"],
                "emission_timestamp": emission["timestamp"],
                "contributing_receptions": receptions,
                "z_immediately_before_final_input": discharge_entry["z_after_decay"],
                "final_input_value": discharge_entry["input_value"],
                "final_slow_input_contribution": (
                    input_gain * discharge_entry["input_value"]
                ),
                "z_before_discharge": discharge_entry["z_after_input"],
                "theta_Z": discharge_entry["theta_z"],
                "discharge_amount": discharge_entry["discharge_amount"],
                "discharge_timestamp": discharge_entry["timestamp"],
                "canonical_emission_timestamp": emission["timestamp"],
            }
        )
    return analyses


def _character_record(
    *,
    arm: str,
    seed: int,
    sequence_index: int,
    condition: str,
    points: tuple[StrokePoint, ...],
) -> dict[str, Any]:
    integration_enabled = arm == "ACP0008_INTEGRATION"
    destination_config = (
        E1Config(integration=IntegrationConfig()) if integration_enabled else E1Config()
    )
    occupancy = _OccupancyAudit()
    neurons: dict[str, MultiExcursionNeuron] = {}
    runtimes: list[ExcursionCharacterRuntime] = []
    captured_traces: dict[str, list[dict[str, Any]]] = {}
    captured_states: dict[str, dict[str, float | None]] = {}
    original_replay = base._replay_destination
    original_reset = MultiExcursionNeuron.reset

    def neuron_factory(node: str, *, config: E1Config) -> MultiExcursionNeuron:
        selected = destination_config if node == "destination" else E1Config()
        neuron = MultiExcursionNeuron(node, config=selected)
        neurons[node] = neuron
        return neuron

    def runtime_factory(*args: Any, **kwargs: Any) -> ExcursionCharacterRuntime:
        kwargs["namespace"] = "luna39"
        kwargs["eligibility_capacity"] = ELIGIBILITY_CAPACITY
        runtime = ExcursionCharacterRuntime(*args, **kwargs)
        runtimes.append(runtime)
        return runtime

    def neuron_reset(neuron: MultiExcursionNeuron, *, timestamp: float = 0.0) -> None:
        captured_traces[neuron.neuron_id] = [
            base._jsonable(entry) for entry in neuron.integration_trace
        ]
        integration_state = neuron.integration_state
        captured_states[neuron.neuron_id] = {
            "x": float(neuron.state),
            "z": None if integration_state is None else float(integration_state),
        }
        original_reset(neuron, timestamp=timestamp)

    def replay(
        routed: list[dict[str, Any]], *, horizon: float
    ) -> tuple[list[dict[str, Any]], tuple[dict[str, Any], ...], float, bool, float, str]:
        if integration_enabled:
            return _replay_destination_with_config(
                routed, horizon=horizon, config=destination_config
            )
        _active_replay_trace.clear()
        return original_replay(routed, horizon=horizon)

    original_init = EligibilityLedger.__init__
    original_record = EligibilityLedger.record_activity
    original_signal = EligibilityLedger.apply_signal

    def ledger_init(ledger: EligibilityLedger, *args: Any, **kwargs: Any) -> None:
        original_init(ledger, *args, **kwargs)
        occupancy.register(ledger)

    def record_activity(ledger: EligibilityLedger, event: Any) -> Any:
        return occupancy.observe(
            ledger,
            lambda: original_record(ledger, event),
            event.timestamp,
            getattr(event.payload, "trace_id", None),
        )

    def apply_signal(ledger: EligibilityLedger, event: Any) -> Any:
        return occupancy.observe(
            ledger,
            lambda: original_signal(ledger, event),
            event.timestamp,
            getattr(event.payload, "trace_id", None),
        )

    with ExitStack() as stack:
        stack.enter_context(mock.patch.object(base, "MultiExcursionNeuron", neuron_factory))
        stack.enter_context(mock.patch.object(base, "ExcursionCharacterRuntime", runtime_factory))
        stack.enter_context(mock.patch.object(base, "_replay_destination", replay))
        stack.enter_context(mock.patch.object(MultiExcursionNeuron, "reset", neuron_reset))
        stack.enter_context(mock.patch.object(EligibilityLedger, "__init__", ledger_init))
        stack.enter_context(mock.patch.object(EligibilityLedger, "record_activity", record_activity))
        stack.enter_context(mock.patch.object(EligibilityLedger, "apply_signal", apply_signal))
        try:
            record = base._character_record(
                seed=seed,
                sequence_index=sequence_index,
                condition=condition,
                points=points,
            )
        except EligibilityCapacityError as error:
            raise StopCondition(
                "EligibilityCapacityError",
                {
                    "arm": arm,
                    "seed": seed,
                    "condition": condition,
                    "character_id": f"c{seed:02d}-{sequence_index:03d}",
                    "capacity_errors": occupancy.capacity_errors,
                    "message": str(error),
                },
            ) from error

    if len(runtimes) != 1 or set(neurons) != set(base.NODES):
        raise StopCondition(
            "required runtime or neuron instrumentation was not observable",
            {"runtime_count": len(runtimes), "neuron_ids": sorted(neurons)},
        )
    runtime = runtimes[0]
    if runtime.eligibility_capacity != ELIGIBILITY_CAPACITY:
        raise StopCondition(
            "effective eligibility capacity differs from 1024",
            {"effective_capacity": runtime.eligibility_capacity},
        )
    ledgers = occupancy.finalize()
    if len(ledgers) != 2 or any(item["configured_capacity"] != ELIGIBILITY_CAPACITY for item in ledgers):
        raise StopCondition("eligibility ledger capacity is not 1024", {"ledgers": ledgers})
    if not all(item["reconciles"] for item in ledgers):
        raise StopCondition("eligibility occupancy does not reconcile", {"ledgers": ledgers})
    if any(item["peak_occupancy"] >= ELIGIBILITY_CAPACITY for item in ledgers):
        raise StopCondition("eligibility peak occupancy reached capacity", {"ledgers": ledgers})
    if occupancy.capacity_errors:
        raise StopCondition("EligibilityCapacityError", {"capacity_errors": occupancy.capacity_errors})

    destination = neurons["destination"]
    actual_trace = captured_traces.get("destination", [])
    replay_trace = list(_active_replay_trace)
    if integration_enabled:
        if len(actual_trace) != len(record["routed_contributions"]) or actual_trace != replay_trace:
            first_difference = None
            for actual, replayed in zip(actual_trace, replay_trace):
                if actual != replayed:
                    first_difference = {
                        key: {"actual": actual.get(key), "replay": replayed.get(key)}
                        for key in sorted(set(actual) | set(replayed))
                        if actual.get(key) != replayed.get(key)
                    }
                    break
            raise StopCondition(
                "required integration_trace is not observable or deterministic",
                {
                    "actual_trace_count": len(actual_trace),
                    "routed_transfer_count": len(record["routed_contributions"]),
                    "replay_trace_count": len(replay_trace),
                    "first_trace_difference": first_difference,
                },
            )
    elif actual_trace or destination.config.integration is not None:
        raise StopCondition("integration-disabled destination retained slow state", {})

    enriched_trace = []
    for index, entry in enumerate(actual_trace):
        if index >= len(record["routed_contributions"]):
            raise StopCondition("integration_trace contains an unmatched entry", {"entry": entry})
        transfer = record["routed_contributions"][index]
        if (
            entry["timestamp"] != transfer["arrival_timestamp"]
            or entry["input_value"] != transfer["transformed_payload"]
        ):
            raise StopCondition(
                "integration_trace does not match routed transfer",
                {"trace": entry, "transfer": transfer},
            )
        enriched = dict(entry)
        enriched["routed_emission_event_id"] = transfer["emission_event_id"]
        enriched["route_depth"] = transfer["route_depth"]
        enriched_trace.append(enriched)

    destination_emissions = [
        item for item in record["canonical_emissions"] if item["emitter_id"] == "destination"
    ]
    for emission in destination_emissions:
        classification = _derived_emission_classification(enriched_trace, emission)
        matching_trace = next(
            entry for entry in enriched_trace
            if entry.get("emission_id") == emission["event_id"]
            and entry.get("emission_timestamp") == emission["timestamp"]
        )
        if classification != matching_trace["classification"]:
            raise StopCondition(
                "trace state and production emission classification disagree",
                {
                    "emission": emission,
                    "derived_classification": classification,
                    "trace_classification": matching_trace["classification"],
                },
            )
        emission["classification"] = classification
    integration_timing = _integration_timing_analysis(
        enriched_trace,
        destination_emissions,
        input_gain=(
            destination_config.integration.input_gain
            if destination_config.integration is not None else 0.0
        ),
    )

    state_before_reset = captured_states.get("destination")
    if state_before_reset is None:
        raise StopCondition("destination state was not observable at character reset", {})
    all_state_values = [
        float(value)
        for value in state_before_reset.values()
        if value is not None
    ]
    for entry in enriched_trace:
        for key in (
            "x_before_decay",
            "x_after_decay",
            "x_after_input",
            "x_post_discharge",
            "x_at_emission",
            "z_before_decay",
            "z_after_decay",
            "z_after_input",
            "z_post_discharge",
            "z_at_emission",
        ):
            value = entry.get(key)
            if value is not None:
                all_state_values.append(float(value))
    if any(not math.isfinite(value) for value in all_state_values):
        raise StopCondition("non-finite destination state", {"state_values": all_state_values})

    max_z = max(
        (abs(value) for entry in enriched_trace for value in (
            entry["z_before_decay"], entry["z_after_decay"], entry["z_after_input"],
            entry["z_post_discharge"], entry.get("z_at_emission"),
        ) if value is not None),
        default=0.0,
    )
    max_z = max(
        max_z,
        0.0 if state_before_reset["z"] is None else abs(state_before_reset["z"]),
    )
    max_x = max(
        (abs(value) for entry in enriched_trace for value in (
            entry["x_before_decay"], entry["x_after_decay"], entry["x_after_input"],
            entry["x_post_discharge"], entry.get("x_at_emission"),
        ) if value is not None),
        default=0.0,
    )
    state_replay_values = [
        value
        for state in record["destination_state_replay"]["records"]
        for value in (state["state_before"], state["state_after"])
    ]
    state_at_horizon = record["destination_state_replay"]["state_at_settling_deadline"]
    if state_at_horizon is not None:
        state_replay_values.append(float(state_at_horizon))
    max_x = max(max_x, *(abs(value) for value in state_replay_values))
    max_x = max(max_x, abs(state_before_reset["x"]))
    transfers = record["routed_contributions"]
    source_emissions = [
        item for item in record["canonical_emissions"] if item["emitter_id"] == "source"
    ]
    reception_count = len(transfers)
    state_changes = sum(
        item["state_after"] != item["state_before"]
        for item in record["destination_state_replay"]["records"]
    )
    integrations = sum(bool(item["integrated"]) for item in enriched_trace)
    discharges = sum(float(item["discharge_amount"]) != 0.0 for item in enriched_trace)
    record.update(
        {
            "arm": arm,
            "source_config": asdict(E1Config()),
            "destination_config": asdict(destination_config),
            "theta_E": destination.config.theta_e,
            "theta_Z": (
                destination.config.integration.discharge_quantum
                if destination.config.integration is not None else None
            ),
            "destination_integration_trace": enriched_trace,
            "destination_canonical_emissions": destination_emissions,
            "destination_additional_emissions": destination_emissions[1:],
            "integration_timing_analysis": integration_timing,
            "destination_state_maxima": {"max_abs_x": max_x, "max_abs_z": max_z},
            "destination_runtime_state_before_reset": state_before_reset,
            "eligibility": {
                "runtime_effective_capacity": runtime.eligibility_capacity,
                "ledgers": ledgers,
                "capacity_errors": occupancy.capacity_errors,
            },
            "mechanism_counts": {
                "source_canonical_emissions": len(source_emissions),
                "routed_transfers": len(transfers),
                "destination_receptions": reception_count,
                "destination_state_changes": state_changes,
                "destination_integration_updates": integrations,
                "destination_z_accumulations": sum(
                    item["z_after_input"] != item["z_after_decay"]
                    for item in enriched_trace
                ),
                "destination_discharges": discharges,
                "destination_canonical_emissions": len(destination_emissions),
                "destination_integrated_emissions": sum(
                    item["classification"] == "integrated_discharge"
                    for item in destination_emissions
                ),
                "destination_direct_emissions": sum(
                    item["classification"] == "direct"
                    for item in destination_emissions
                ),
                "distinct_emitters": len(record["distinct_emitters"]),
                "runtime_events_used": record["execution"]["events_processed"],
            },
            "no_edge_contaminated": bool(
                condition == "NO_EDGE_CONTROL"
                and (
                    transfers
                    or reception_count
                    or max_z != 0.0
                    or destination_emissions
                )
            ),
            "replay_integration_trace_equal": (
                not integration_enabled or actual_trace == replay_trace
            ),
        }
    )
    record["replay_digest"] = _digest(record)
    if condition == "NO_EDGE_CONTROL" and record["no_edge_contaminated"]:
        raise StopCondition(
            "NO-EDGE CONTROL NOT A VALID NEGATIVE CONTROL",
            {
                "arm": arm,
                "seed": seed,
                "character_id": record["character_id"],
                "mechanism_counts": record["mechanism_counts"],
                "maximum_abs_z": max_z,
            },
        )
    return record


def _ratio(count: int, total: int) -> dict[str, int]:
    return {"count": count, "total": total}


def _cell_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    counts = [record["mechanism_counts"] for record in records]
    ledgers = [ledger for record in records for ledger in record["eligibility"]["ledgers"]]
    executions = len(records)
    return {
        "executions": executions,
        "source_emitting_characters": _ratio(
            sum(item["source_canonical_emissions"] > 0 for item in counts), executions
        ),
        "destination_receiving_characters": _ratio(
            sum(item["destination_receptions"] > 0 for item in counts), executions
        ),
        "destination_canonical_emitting_characters": _ratio(
            sum(item["destination_canonical_emissions"] > 0 for item in counts), executions
        ),
        "destination_integrated_emitting_characters": _ratio(
            sum(item["destination_integrated_emissions"] > 0 for item in counts), executions
        ),
        "destination_direct_emitting_characters": _ratio(
            sum(item["destination_direct_emissions"] > 0 for item in counts), executions
        ),
        "total_source_emissions": sum(item["source_canonical_emissions"] for item in counts),
        "total_transfers": sum(item["routed_transfers"] for item in counts),
        "total_destination_receptions": sum(item["destination_receptions"] for item in counts),
        "total_destination_state_changes": sum(item["destination_state_changes"] for item in counts),
        "total_z_accumulations": sum(item["destination_z_accumulations"] for item in counts),
        "total_discharges": sum(item["destination_discharges"] for item in counts),
        "total_destination_canonical_emissions": sum(
            item["destination_canonical_emissions"] for item in counts
        ),
        "total_integrated_emissions": sum(item["destination_integrated_emissions"] for item in counts),
        "total_direct_emissions": sum(item["destination_direct_emissions"] for item in counts),
        "maximum_abs_z": max(
            (record["destination_state_maxima"]["max_abs_z"] for record in records),
            default=0.0,
        ),
        "maximum_abs_x": max(
            (record["destination_state_maxima"]["max_abs_x"] for record in records),
            default=0.0,
        ),
        "maximum_route_depth": max(
            (record["execution"]["max_route_depth"] for record in records), default=0
        ),
        "peak_eligibility_occupancy": max(
            (item["peak_occupancy"] for item in ledgers), default=0
        ),
        "maximum_final_eligibility_occupancy": max(
            (item["final_occupancy"] for item in ledgers), default=0
        ),
        "eligibility_created": sum(item["created"] for item in ledgers),
        "eligibility_removed": sum(item["removed"] for item in ledgers),
        "all_eligibility_ledgers_reconcile": all(item["reconciles"] for item in ledgers),
        "runtime_events_used": sum(item["runtime_events_used"] for item in counts),
        "incomplete_settling_characters": sum(
            not record["execution"]["completed"] for record in records
        ),
        "no_edge_contaminated_characters": sum(record["no_edge_contaminated"] for record in records),
    }


def _stream_invariance(
    results: dict[str, Any],
) -> dict[str, Any]:
    mismatches = []
    queue_sequence_differences = 0
    legacy = results["runs"].get("LEGACY_REPRODUCTION", {})
    integrated = results["runs"].get("ACP0008_INTEGRATION", {})
    for seed in sorted(set(legacy) & set(integrated)):
        for condition in CONDITIONS:
            left = legacy[seed].get(condition, [])
            right = integrated[seed].get(condition, [])
            if len(left) != len(right):
                mismatches.append({"seed": int(seed), "condition": condition, "reason": "record count"})
                continue
            for old, new in zip(left, right):
                for field in ("source_input_events", "canonical_emissions", "routed_contributions"):
                    old_value = (
                        [item for item in old[field] if item["emitter_id"] == "source"]
                        if field == "canonical_emissions" else old[field]
                    )
                    new_value = (
                        [item for item in new[field] if item["emitter_id"] == "source"]
                        if field == "canonical_emissions" else new[field]
                    )
                    if field == "routed_contributions":
                        routed_fields = (
                            "emission_event_id",
                            "emitter_id",
                            "destination",
                            "emission_timestamp",
                            "arrival_timestamp",
                            "transformed_payload",
                            "payload_sign",
                            "payload_magnitude",
                            "propagation_delay",
                            "destination_receive_count",
                            "lineage_id",
                            "route_depth",
                            "route_path",
                        )
                        queue_sequence_differences += sum(
                            old_item.get("receive_sequence") != new_item.get("receive_sequence")
                            for old_item, new_item in zip(old[field], new[field])
                        )
                        old_value = [
                            {key: item.get(key) for key in routed_fields}
                            for item in old_value
                        ]
                        new_value = [
                            {key: item.get(key) for key in routed_fields}
                            for item in new_value
                        ]
                    if old_value != new_value:
                        mismatches.append(
                            {
                                "seed": int(seed),
                                "condition": condition,
                                "character_id": old["character_id"],
                                "field": field,
                            }
                        )
                        break
    return {
        "identical": not mismatches,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:20],
        "runtime_queue_sequence_difference_count": queue_sequence_differences,
        "queue_sequence_note": (
            "Runtime-global receive_sequence can shift when destination emissions add local "
            "events; routed identity, arrival time, payload, delay, receive order and depth "
            "are compared independently."
        ),
    }


def _legacy_gate(results: dict[str, Any], *, full_population: bool) -> dict[str, Any]:
    arm_runs = results["runs"].get("LEGACY_REPRODUCTION", {})
    per_condition = {}
    for condition in CONDITIONS:
        records = [
            record
            for conditions in arm_runs.values()
            for record in conditions.get(condition, [])
        ]
        summary = _cell_summary(records)
        per_condition[condition] = summary
    if not full_population:
        return {"passed": True, "scope": "partial focused-test fixture", "per_condition": per_condition}
    expected = {
        "NO_EDGE_CONTROL": (1715, 0, 0),
        "DEFAULT_STATIC_EDGE": (1715, 1715, 0),
        "STATIC_N2_BOUND_SENSITIVITY": (1715, 1715, 0),
    }
    mismatches = {}
    for condition, (source, transfers, destination) in expected.items():
        actual = per_condition[condition]
        triple = (
            actual["total_source_emissions"],
            actual["total_transfers"],
            actual["total_destination_canonical_emissions"],
        )
        if triple != (source, transfers, destination):
            mismatches[condition] = {
                "expected": [source, transfers, destination],
                "actual": list(triple),
            }
    return {
        "passed": not mismatches,
        "scope": "full Luna-37 historical reproduction gate",
        "expected_source_transfers_destination": {
            key: list(value) for key, value in expected.items()
        },
        "mismatches": mismatches,
        "per_condition": per_condition,
    }


def _run_once(seeds: tuple[int, ...]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    results: dict[str, Any] = {
        "schema": "TPCN-LUNA39-ACP0008-PROPAGATION-EMISSION-RESULTS-1",
        "execution_baseline": EXECUTION_BASELINE,
        "eligibility_capacity": ELIGIBILITY_CAPACITY,
        "arms": list(ARMS),
        "conditions": list(CONDITIONS),
        "environment": {"python": sys.version, "platform": platform.platform()},
        "runs": {arm: {} for arm in ARMS},
    }
    stop: dict[str, Any] | None = None
    for arm in ARMS:
        for seed in seeds:
            seed_runs: dict[str, list[dict[str, Any]]] = {
                condition: [] for condition in CONDITIONS
            }
            results["runs"][arm][str(seed)] = seed_runs
            try:
                sequences = base._training_point_sequences(seed)
                if len(sequences) != 64:
                    raise StopCondition(
                        "fixture did not produce the contract-declared 64 streams",
                        {"seed": seed, "actual": len(sequences)},
                    )
                for condition in CONDITIONS:
                    for sequence_index, points in enumerate(sequences):
                        seed_runs[condition].append(
                            _character_record(
                                arm=arm,
                                seed=seed,
                                sequence_index=sequence_index,
                                condition=condition,
                                points=points,
                            )
                        )
            except StopCondition as error:
                stop = {"reason": error.reason, "detail": error.detail}
            except Exception as error:
                stop = {
                    "reason": "production exception",
                    "detail": {
                        "arm": arm,
                        "seed": seed,
                        "type": type(error).__name__,
                        "message": str(error),
                    },
                }
            if stop is not None:
                return results, stop
        if arm == "LEGACY_REPRODUCTION":
            gate = _legacy_gate(results, full_population=(seeds == SEEDS))
            results["legacy_reproduction_gate"] = gate
            if not gate["passed"]:
                return results, {
                    "reason": "legacy reproduction gate mismatch",
                    "detail": gate,
                }

    stream_check = _stream_invariance(results)
    results["source_and_transfer_stream_invariance"] = stream_check
    if not stream_check["identical"]:
        stop = {
            "reason": "source or transfer streams differ across arms",
            "detail": stream_check,
        }
    return results, stop


def _all_digest(results: dict[str, Any]) -> str:
    return _digest(
        [
            record["replay_digest"]
            for arm in ARMS
            for seed in sorted(results["runs"][arm], key=int)
            for condition in CONDITIONS
            for record in results["runs"][arm][seed][condition]
        ]
    )


def _summarize(
    results: dict[str, Any],
    stop: dict[str, Any] | None,
    replay: dict[str, Any] | None,
) -> dict[str, Any]:
    per_seed = {
        arm: {
            seed: {
                condition: _cell_summary(records)
                for condition, records in conditions.items()
            }
            for seed, conditions in results["runs"].get(arm, {}).items()
        }
        for arm in ARMS
    }
    per_arm_condition = {
        arm: {
            condition: _cell_summary(
                [
                    record
                    for conditions in results["runs"].get(arm, {}).values()
                    for record in conditions.get(condition, [])
                ]
            )
            for condition in CONDITIONS
        }
        for arm in ARMS
    }
    integrated = per_arm_condition["ACP0008_INTEGRATION"]
    integrated_emissions = sum(
        integrated[condition]["total_destination_canonical_emissions"]
        for condition in CONDITIONS
    )
    default_emissions = integrated["DEFAULT_STATIC_EDGE"]["total_integrated_emissions"]
    n2_emissions = integrated["STATIC_N2_BOUND_SENSITIVITY"]["total_integrated_emissions"]
    default_by_character = {
        (seed, record["character_id"]): record
        for seed, conditions in results["runs"].get("ACP0008_INTEGRATION", {}).items()
        for record in conditions.get("DEFAULT_STATIC_EDGE", [])
    }
    n2_sensitive_streams = []
    for seed, conditions in results["runs"].get("ACP0008_INTEGRATION", {}).items():
        for record in conditions.get("STATIC_N2_BOUND_SENSITIVITY", []):
            paired = default_by_character.get((seed, record["character_id"]))
            if (
                paired is not None
                and record["mechanism_counts"]["destination_integrated_emissions"] > 0
                and paired["mechanism_counts"]["destination_integrated_emissions"] == 0
            ):
                n2_sensitive_streams.append(
                    {
                        "seed": int(seed),
                        "character_id": record["character_id"],
                        "n2_integrated_emissions": record["mechanism_counts"][
                            "destination_integrated_emissions"
                        ],
                        "default_integrated_emissions": 0,
                    }
                )
    legacy_emissions = sum(
        per_arm_condition["LEGACY_REPRODUCTION"][condition][
            "total_destination_canonical_emissions"
        ]
        for condition in CONDITIONS
    )
    direct_integrated_emissions = sum(
        integrated[condition]["total_direct_emissions"] for condition in CONDITIONS
    )
    no_edge_clean = (
        integrated["NO_EDGE_CONTROL"]["total_transfers"] == 0
        and integrated["NO_EDGE_CONTROL"]["total_destination_receptions"] == 0
        and integrated["NO_EDGE_CONTROL"]["maximum_abs_z"] == 0.0
        and integrated["NO_EDGE_CONTROL"]["total_destination_canonical_emissions"] == 0
    )
    classifications = []
    gate = results.get("legacy_reproduction_gate", {"passed": False})
    if gate.get("passed"):
        classifications.append("LEGACY ARM REPRODUCES LUNA-37")
    elif stop and stop.get("reason") == "legacy reproduction gate mismatch":
        classifications.append("LEGACY ARM DOES NOT REPRODUCE LUNA-37")
    if stop is not None:
        classifications.append("BLOCKED - FIXTURE OR PUBLIC API INSUFFICIENT")
    else:
        if integrated_emissions == 0:
            classifications.append("INTEGRATED DESTINATION EMISSION ABSENT IN ALL CONDITIONS")
        if default_emissions > 0:
            classifications.append("INTEGRATED DESTINATION EMISSION PRESENT UNDER DEFAULT STATIC EDGE")
        if n2_emissions > 0 and default_emissions == 0:
            classifications.append("INTEGRATED DESTINATION EMISSION PRESENT ONLY UNDER STATIC N2 SENSITIVITY")
        if direct_integrated_emissions > 0 or legacy_emissions > 0:
            classifications.append("DESTINATION EMISSION WITHOUT INTEGRATION (INCONSISTENT)")
        if not no_edge_clean:
            classifications.append("NO-EDGE CONTROL NOT A VALID NEGATIVE CONTROL")
        if all(
            integrated[condition]["maximum_abs_z"] < 1.0
            and integrated[condition]["total_discharges"] == 0
            for condition in CONDITIONS
        ):
            classifications.append("Z ACCUMULATED BUT NEVER REACHED DISCHARGE")
        if n2_sensitive_streams:
            classifications.append("STATIC N2 CHANGES RESULT RELATIVE TO DEFAULT")
    total_executions = sum(
        len(records)
        for arm in results["runs"].values()
        for conditions in arm.values()
        for records in conditions.values()
    )
    return {
        "schema": "TPCN-LUNA39-ACP0008-PROPAGATION-EMISSION-SUMMARY-1",
        "execution_baseline": EXECUTION_BASELINE,
        "complete": stop is None and total_executions == 1920,
        "stop_condition": stop,
        "design_counts": {
            "seeds": len(results["runs"].get("LEGACY_REPRODUCTION", {})),
            "character_condition_arm_executions": total_executions,
        },
        "legacy_reproduction_gate": gate,
        "source_and_transfer_stream_invariance": results.get(
            "source_and_transfer_stream_invariance"
        ),
        "per_seed": per_seed,
        "per_arm_condition": per_arm_condition,
        "no_edge_control_is_genuine_negative": no_edge_clean and stop is None,
        "static_n2_sensitive_streams": n2_sensitive_streams,
        "deterministic_replay": replay,
        "terminal_classifications": classifications,
        "interpretation_boundary": (
            "Bounded propagation-level mechanism observation only; not ACP-0007 efficacy, "
            "candidate formation, structural growth, pruning, accuracy, calibration, "
            "generality, hardware equivalence, or ACP-0008 promotion."
        ),
    }


def run_experiment(
    output_directory: Path = ARTIFACT_DIRECTORY,
    seeds: tuple[int, ...] = SEEDS,
) -> tuple[dict[str, Any], dict[str, Any]]:
    results, stop = _run_once(seeds)
    replay_results, replay_stop = _run_once(seeds)
    first = _all_digest(results)
    second = _all_digest(replay_results)
    replay = {
        "initial_digest": first,
        "replay_digest": second,
        "equal": first == second and stop == replay_stop,
    }
    if not replay["equal"] and stop is None:
        stop = {
            "reason": "nondeterministic replay",
            "detail": {"initial_digest": first, "replay_digest": second},
        }
    results["deterministic_replay"] = replay
    summary = _summarize(results, stop, replay)
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
