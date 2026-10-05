"""Run the bounded Luna-41 ACP-0008 temporal calibration experiment."""

from __future__ import annotations

from contextlib import ExitStack
from dataclasses import asdict, is_dataclass
from enum import Enum
import hashlib
import json
import math
import platform
import sys
from pathlib import Path
from typing import Any, Iterable
from unittest import mock

import run_luna39_acp0008_propagation_emission_diagnostic as luna39
from tpcn.eligibility import EligibilityCapacityError, EligibilityLedger
from tpcn.event_runtime import Event, EventQueue, EventType, QueueCapacityError
from tpcn.excursion_neuron import (
    E1Config,
    ExcursionEmission,
    IntegrationConfig,
    MultiExcursionNeuron,
)
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.topology import BoundedTopology, Edge, TopologyCapacityError


START_REVISION = "714cad5a7eea55af4cd8529b0244a8c5723e2fd7"
ARTIFACT_DIRECTORY = Path("artifacts/luna41-acp0008-temporal-calibration")
CANDIDATES = (0.1, 0.05, 0.025, 0.0125)
PHASE_A_FIXTURES = (
    "ISOLATED",
    "NEAR_PAIR",
    "NEAR_TRIPLE",
    "FAR_TRIPLE",
    "NEGATIVE_NEAR_TRIPLE",
    "INTEGRATION_DISABLED",
)
PHASE_B_ARMS = (
    "CALIBRATED",
    "DEFAULT",
    "DISABLED",
)
SEEDS = (0, 1, 2, 3, 4)
NEAR_INTERVAL = 12.9
FAR_INTERVAL = 51.6
ROUTED_AMPLITUDE = 0.4
SOURCE_EMISSION_AMPLITUDE = math.atanh(ROUTED_AMPLITUDE)
SOURCE_PEAK_INPUT = 4.0 * SOURCE_EMISSION_AMPLITUDE
PHASE_A_QUEUE_CAPACITY = 64
PHASE_A_EVENT_BUDGET = 64
PHASE_B_ELIGIBILITY_CAPACITY = 1024
PHASE_B_QUEUE_CAPACITY = 128
PHASE_B_RUNTIME_EVENT_BUDGET = 1024
PHASE_B_MAX_ACTIVITY_EVENTS = 1024
PHASE_B_SETTLING_HORIZON = 4.0
PHASE_B_PREDICTION_CAPACITY = 8
PHASE_B_PREDICTION_EXPIRY = 4.0
PHASE_B_NEURON_EVENT_BUDGET = 4096
PHASE_B_NODES = ("source", "relay", "destination")
Z_TOLERANCE = 1e-12
PREDICTION_TOLERANCE = 1e-5
ROUTE_PAYLOAD_TOLERANCE = 1e-12

PREDICTED_FIXTURE_MAGNITUDES = {
    0.1: {"NEAR_PAIR": 0.5101083132359009, "NEAR_TRIPLE": 0.5404179148450391, "FAR_TRIPLE": 0.4023098667203739},
    0.05: {"NEAR_PAIR": 0.6098650168426372, "NEAR_TRIPLE": 0.7199733300785381, "FAR_TRIPLE": 0.4326062814833999},
    0.025: {"NEAR_PAIR": 0.6897343727227663, "NEAR_TRIPLE": 0.8995993895654033, "FAR_TRIPLE": 0.5404179148450391},
    0.0125: {"NEAR_PAIR": 0.740431709876014, "NEAR_TRIPLE": 1.0301660825987804, "FAR_TRIPLE": 0.7199733300785381},
}


class StopCondition(RuntimeError):
    """A frozen Luna-41 stop condition; the affected arm is not retried."""

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
    return json.dumps(
        _jsonable(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def experiment_config() -> dict[str, Any]:
    return {
        "schema": "TPCN-LUNA41-ACP0008-TEMPORAL-CALIBRATION-1",
        "authorization_revision": START_REVISION,
        "candidate_order": list(CANDIDATES),
        "phase_a": {
            "source_peak_input": SOURCE_PEAK_INPUT,
            "source_emission_amplitude": SOURCE_EMISSION_AMPLITUDE,
            "expected_routed_amplitude": ROUTED_AMPLITUDE,
            "near_interval": NEAR_INTERVAL,
            "far_interval": FAR_INTERVAL,
            "queue_capacity": PHASE_A_QUEUE_CAPACITY,
            "processed_event_limit": PHASE_A_EVENT_BUDGET,
            "neuron_event_budget": PHASE_A_EVENT_BUDGET,
            "fixtures": {
                "ISOLATED": {"inputs": [0.0], "sign": 1},
                "NEAR_PAIR": {"inputs": [0.0, NEAR_INTERVAL], "sign": 1},
                "NEAR_TRIPLE": {
                    "inputs": [0.0, NEAR_INTERVAL, 2.0 * NEAR_INTERVAL],
                    "sign": 1,
                },
                "FAR_TRIPLE": {"inputs": [0.0, FAR_INTERVAL, 2.0 * FAR_INTERVAL], "sign": 1},
                "NEGATIVE_NEAR_TRIPLE": {
                    "inputs": [0.0, NEAR_INTERVAL, 2.0 * NEAR_INTERVAL],
                    "sign": -1,
                },
                "INTEGRATION_DISABLED": {
                    "inputs": [0.0, NEAR_INTERVAL, 2.0 * NEAR_INTERVAL],
                    "sign": 1,
                    "integration": None,
                },
            },
            "topology": {
                "nodes": ["source", "relay"],
                "edge": {
                    "source": "source",
                    "destination": "relay",
                    "delay": 1.0,
                    "w": 1.0,
                    "d": 1.0,
                    "r": 0.0,
                },
                "fan_in_limit": 1,
                "fan_out_limit": 1,
                "edge_capacity": 1,
                "routing_capacity": 1,
            },
            "fixed_neuron_parameters": {
                "decay_rate": 1.0,
                "theta_E": 1.0,
                "theta_Z": 1.0,
                "input_gain": 1.0,
                "z_max": 4.0,
            },
            "neutral_probe": {
                "delay_after_last_input_or_discharge_tau_z": 10.0,
                "required_abs_z_below": 1e-4,
                "input": 0.0,
            },
            "expected_magnitudes": PREDICTED_FIXTURE_MAGNITUDES,
            "analytic_tolerance": PREDICTION_TOLERANCE,
        },
        "phase_b": {
            "stream_source": "read-only Luna-39/Luna-34 make_spiral_dataset helper",
            "seeds": list(SEEDS),
            "examples_per_class": 16,
            "characters_per_seed": 64,
            "train_seed": "12007 + seed",
            "evaluation_seed": "22017 + seed (generated by inherited helper, not consumed)",
            "ordering": "random.Random(330000 + seed).shuffle(point_sequences)",
            "input": "point.x + point.y at point.timestamp; preserve same-timestamp batching",
            "arms": list(PHASE_B_ARMS),
            "topology": {
                "nodes": list(PHASE_B_NODES),
                "edges": [
                    {"source": "source", "destination": "relay", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
                    {"source": "relay", "destination": "destination", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
                ],
                "fan_in_limit": 2,
                "fan_out_limit": 2,
                "edge_capacity": 3,
                "routing_capacity": 3,
            },
            "runtime": {
                "neuron_event_budget": PHASE_B_NEURON_EVENT_BUDGET,
                "queue_capacity": PHASE_B_QUEUE_CAPACITY,
                "runtime_event_budget": PHASE_B_RUNTIME_EVENT_BUDGET,
                "max_activity_events": PHASE_B_MAX_ACTIVITY_EVENTS,
                "settling_horizon": PHASE_B_SETTLING_HORIZON,
                "prediction_capacity": PHASE_B_PREDICTION_CAPACITY,
                "prediction_expiry": PHASE_B_PREDICTION_EXPIRY,
                "eligibility_capacity_per_ledger": PHASE_B_ELIGIBILITY_CAPACITY,
                "neutral_reward": 0.0,
            },
        },
        "replay_runs": 2,
    }


def _phase_a_schedule(fixture: str) -> tuple[tuple[float, float], ...]:
    if fixture == "ISOLATED":
        times = (0.0,)
        sign = 1.0
    elif fixture == "NEAR_PAIR":
        times = (0.0, NEAR_INTERVAL)
        sign = 1.0
    elif fixture in ("NEAR_TRIPLE", "INTEGRATION_DISABLED"):
        times = (0.0, NEAR_INTERVAL, 2.0 * NEAR_INTERVAL)
        sign = 1.0
    elif fixture == "NEGATIVE_NEAR_TRIPLE":
        times = (0.0, NEAR_INTERVAL, 2.0 * NEAR_INTERVAL)
        sign = -1.0
    elif fixture == "FAR_TRIPLE":
        times = (0.0, FAR_INTERVAL, 2.0 * FAR_INTERVAL)
        sign = 1.0
    else:
        raise ValueError(f"unknown Phase-A fixture: {fixture}")
    return tuple((time, sign * SOURCE_PEAK_INPUT) for time in times)


def _emission_record(emission: ExcursionEmission) -> dict[str, Any]:
    return {
        "event_id": emission.event_id,
        "sequence": emission.sequence,
        "source": emission.source,
        "timestamp": float(emission.timestamp),
        "payload": float(emission.payload),
        "lineage_id": emission.lineage_id,
        "episode_id": emission.episode_id,
    }


def _topology_phase_a() -> BoundedTopology:
    return BoundedTopology.from_edges(
        ("source", "relay"),
        (
            Edge(
                "source",
                "relay",
                1.0,
                edge_weight=1.0,
                divider_strength=1.0,
                reference=0.0,
            ),
        ),
        fan_in_limit=1,
        fan_out_limit=1,
        edge_capacity=1,
        routing_capacity=1,
    )


def _queue_record(event: Event) -> dict[str, Any]:
    return {
        "timestamp": float(event.timestamp),
        "source": event.source,
        "destination": event.destination,
        "event_type": _jsonable(event.event_type),
        "payload": _jsonable(event.payload),
        "sequence": event.sequence,
        "event_id": event.event_id,
        "lineage_id": event.lineage_id,
    }


def _run_phase_a_fixture(decay_rate_z: float, fixture: str) -> dict[str, Any]:
    disabled = fixture == "INTEGRATION_DISABLED"
    integration = (
        None
        if disabled
        else IntegrationConfig(decay_rate_z=decay_rate_z)
    )
    source = MultiExcursionNeuron(
        "source",
        config=E1Config(event_budget=PHASE_A_EVENT_BUDGET),
    )
    relay = MultiExcursionNeuron(
        "relay",
        config=E1Config(
            event_budget=PHASE_A_EVENT_BUDGET,
            integration=integration,
        ),
    )
    neurons = {"source": source, "relay": relay}
    topology = _topology_phase_a()
    queue: EventQueue[Event] = EventQueue(PHASE_A_QUEUE_CAPACITY)
    queue_peak = 0
    processed = 0
    events: list[dict[str, Any]] = []
    transfers: list[dict[str, Any]] = []
    canonical_emissions: list[dict[str, Any]] = []
    state_after_events: list[dict[str, Any]] = []
    inputs = _phase_a_schedule(fixture)
    for index, (timestamp, value) in enumerate(inputs):
        queue.push(
            Event(
                timestamp,
                "luna41-stimulus",
                "source",
                EventType.INPUT,
                value,
                event_id=f"phase-a:{decay_rate_z}:{fixture}:input:{index}",
            )
        )
    queue_peak = len(queue)

    def process_queue() -> None:
        nonlocal processed, queue_peak
        while queue:
            if processed >= PHASE_A_EVENT_BUDGET:
                raise StopCondition(
                    "Phase-A processed-event limit exceeded",
                    {
                        "decay_rate_z": decay_rate_z,
                        "fixture": fixture,
                        "processed": processed,
                        "queue_pending": len(queue),
                    },
                )
            next_event = queue.peek()
            if next_event is None:
                raise RuntimeError("Phase-A queue lost its next event")
            event = queue.pop_ready(next_event.timestamp)
            processed += 1
            neuron = neurons.get(event.destination)
            if neuron is None:
                raise StopCondition(
                    "Phase-A event addressed an unknown neuron",
                    {"fixture": fixture, "event": _queue_record(event)},
                )
            emission = neuron.receive_event(event, queue)
            event_record = _queue_record(event)
            event_record["emission_id"] = None if emission is None else emission.event_id
            event_record["neuron_state_after"] = {
                "x": float(neuron.state),
                "z": (
                    None
                    if neuron.integration_state is None
                    else float(neuron.integration_state)
                ),
                "mode": _jsonable(neuron.mode),
                "last_update_timestamp": float(neuron.last_update_timestamp),
            }
            events.append(event_record)
            state_after_events.append(
                {
                    "neuron": neuron.neuron_id,
                    "event_id": event.event_id,
                    "timestamp": event.timestamp,
                    **event_record["neuron_state_after"],
                }
            )
            if emission is not None:
                canonical = _emission_record(emission)
                canonical_emissions.append(canonical)
                routed = topology.route(
                    Event(
                        emission.timestamp,
                        emission.source,
                        emission.source,
                        EventType.EXCURSION,
                        emission.payload,
                        event_id=emission.event_id,
                        lineage_id=emission.lineage_id,
                    ),
                    queue,
                )
                for routed_event in routed:
                    transfer = _queue_record(routed_event)
                    transfer.update(
                        {
                            "emission_event_id": emission.event_id,
                            "emission_timestamp": emission.timestamp,
                            "arrival_timestamp": routed_event.timestamp,
                            "edge": "source->relay",
                            "model_b_payload": routed_event.payload,
                            "delay": topology.edge("source", "relay").propagation_delay,
                        }
                    )
                    transfers.append(transfer)
            queue_peak = max(queue_peak, len(queue))
            if queue_peak > PHASE_A_QUEUE_CAPACITY:
                raise StopCondition(
                    "Phase-A queue capacity exceeded",
                    {"fixture": fixture, "queue_peak": queue_peak},
                )

    try:
        process_queue()
    except QueueCapacityError as error:
        raise StopCondition(
            "Phase-A queue capacity exceeded",
            {"fixture": fixture, "message": str(error), "queue_peak": queue_peak},
        ) from error

    last_input_or_discharge = max(
        [item["arrival_timestamp"] for item in transfers]
        + [
            float(entry.timestamp)
            for entry in relay.integration_trace
            if entry.discharge_amount != 0.0
        ]
    )
    tau_z = 1.0 / decay_rate_z
    probe_timestamp = math.nextafter(
        last_input_or_discharge + 10.0 * tau_z,
        math.inf,
    )
    queue.push(
        Event(
            probe_timestamp,
            "luna41-neutral-probe",
            "relay",
            EventType.INPUT,
            0.0,
            event_id=f"phase-a:{decay_rate_z}:{fixture}:neutral-probe",
        )
    )
    queue_peak = max(queue_peak, len(queue))
    try:
        process_queue()
    except QueueCapacityError as error:
        raise StopCondition(
            "Phase-A queue capacity exceeded during neutral probe",
            {"fixture": fixture, "message": str(error), "queue_peak": queue_peak},
        ) from error

    trace = [_jsonable(entry) for entry in relay.integration_trace]
    source_trace = [_jsonable(entry) for entry in source.integration_trace]
    trace_bounds_ok = all(
        abs(float(entry[field])) <= source.config.x_max
        for entry in source_trace
        for field in ("x_before_decay", "x_after_decay", "x_after_input", "x_post_discharge")
    ) and all(
        abs(float(entry[field])) <= relay.config.x_max
        for entry in trace
        for field in ("x_before_decay", "x_after_decay", "x_after_input", "x_post_discharge")
    )
    state_bounds_ok = (
        abs(float(source.state)) <= source.config.x_max
        and abs(float(relay.state)) <= relay.config.x_max
        and trace_bounds_ok
        and (
            relay.integration_state is None
            or abs(float(relay.integration_state)) <= 4.0
        )
    )
    probe_events = [
        event
        for event in events
        if event["event_id"] == f"phase-a:{decay_rate_z}:{fixture}:neutral-probe"
    ]
    probe_z = (
        float(relay.integration_state)
        if relay.integration_state is not None
        else None
    )
    return {
        "decay_rate_z": decay_rate_z,
        "tau_z": tau_z,
        "fixture": fixture,
        "integration_enabled": not disabled,
        "schedule": [
            {
                "timestamp": timestamp,
                "source_input": value,
                "source_canonical_payload_expected": math.copysign(
                    SOURCE_EMISSION_AMPLITUDE, value
                ),
                "routed_payload_expected": math.copysign(ROUTED_AMPLITUDE, value),
            }
            for timestamp, value in inputs
        ],
        "source_canonical_emissions": [
            item for item in canonical_emissions if item["source"] == "source"
        ],
        "relay_canonical_emissions": [
            item for item in canonical_emissions if item["source"] == "relay"
        ],
        "transfers": transfers,
        "processed_events": events,
        "state_after_each_processed_event": state_after_events,
        "source_integration_trace": source_trace,
        "relay_integration_trace": trace,
        "relay_inputs": [
            {
                "timestamp": item["timestamp"],
                "event_id": item["event_id"],
                "payload": item["payload"],
            }
            for item in events
            if item["destination"] == "relay" and item["event_type"] != EventType.INTERNAL.value
        ],
        "neutral_probe": {
            "timestamp": probe_timestamp,
            "delay_from_last_input_or_discharge": probe_timestamp - last_input_or_discharge,
            "event_count": len(probe_events),
            "input_value": 0.0,
            "z_after_probe": probe_z,
            "emission_count_after_probe": len(
                [item for item in canonical_emissions if item["source"] == "relay"]
            ),
            "evidence": False,
        },
        "resources": {
            "queue_capacity": PHASE_A_QUEUE_CAPACITY,
            "queue_peak": queue_peak,
            "processed_event_limit": PHASE_A_EVENT_BUDGET,
            "processed_events": processed,
            "source_event_budget": source.config.event_budget,
            "source_processed_events": source.processed_event_count,
            "relay_event_budget": relay.config.event_budget,
            "relay_processed_events": relay.processed_event_count,
        },
        "final_state": {
            "source_x": float(source.state),
            "relay_x": float(relay.state),
            "relay_z": probe_z,
            "state_bounds_ok": state_bounds_ok,
        },
    }


def _analytic_recurrence_check(record: dict[str, Any]) -> dict[str, Any]:
    if not record["integration_enabled"]:
        return {"applicable": False, "passed": True, "checks": []}
    decay_rate = float(record["decay_rate_z"])
    expected_z = 0.0
    previous_timestamp = 0.0
    checks: list[dict[str, Any]] = []
    entries = record["relay_integration_trace"]
    for entry in entries:
        timestamp = float(entry["timestamp"])
        elapsed_total = timestamp - previous_timestamp
        expected_decayed = expected_z * math.exp(-decay_rate * elapsed_total)
        input_value = float(entry["input_value"])
        integrated = bool(entry["integrated"])
        expected_after_input = (
            max(-4.0, min(4.0, expected_decayed + input_value))
            if integrated
            else expected_decayed
        )
        discharge_expected = (
            math.copysign(1.0, expected_after_input)
            if integrated
            and abs(expected_after_input) >= 1.0
            and float(entry["x_after_input"]) * expected_after_input >= 0.0
            else 0.0
        )
        expected_post_discharge = expected_after_input - discharge_expected
        comparisons = {
            "z_after_decay": abs(float(entry["z_after_decay"]) - expected_decayed) <= Z_TOLERANCE,
            "z_after_input": abs(float(entry["z_after_input"]) - expected_after_input) <= Z_TOLERANCE,
            "discharge": abs(float(entry["discharge_amount"]) - discharge_expected) <= Z_TOLERANCE,
            "z_post_discharge": abs(float(entry["z_post_discharge"]) - expected_post_discharge) <= Z_TOLERANCE,
        }
        checks.append(
            {
                "timestamp": timestamp,
                "elapsed_since_previous_external_update": elapsed_total,
                "z_before_event": expected_z,
                "z_after_decay_expected": expected_decayed,
                "input_contribution": input_value,
                "z_after_input_expected": expected_after_input,
                "discharge_expected": discharge_expected,
                "z_post_discharge_expected": expected_post_discharge,
                "comparisons": comparisons,
                "passed": all(comparisons.values()),
            }
        )
        expected_z = expected_post_discharge
        previous_timestamp = timestamp
    return {
        "applicable": True,
        "passed": all(item["passed"] for item in checks),
        "tolerance": Z_TOLERANCE,
        "checks": checks,
    }


def _phase_a_expectation(record: dict[str, Any]) -> dict[str, Any]:
    fixture = record["fixture"]
    expected_relay_emissions = 1 if fixture in ("NEAR_TRIPLE", "NEGATIVE_NEAR_TRIPLE") and record["integration_enabled"] else 0
    relay_emissions = record["relay_canonical_emissions"]
    expected_transfers = len(record["schedule"])
    payload_deltas = [
        abs(
            float(transfer["model_b_payload"])
            - float(schedule["routed_payload_expected"])
        )
        for transfer, schedule in zip(record["transfers"], record["schedule"])
    ]
    source_emission_deltas = [
        abs(
            float(emission["payload"])
            - float(schedule["source_canonical_payload_expected"])
        )
        for emission, schedule in zip(
            record["source_canonical_emissions"], record["schedule"]
        )
    ]
    payload_ok = (
        len(record["source_canonical_emissions"]) == expected_transfers
        and len(record["transfers"]) == expected_transfers
        and all(delta <= ROUTE_PAYLOAD_TOLERANCE for delta in payload_deltas)
        and all(delta <= ROUTE_PAYLOAD_TOLERANCE for delta in source_emission_deltas)
    )
    trace_by_emission = {
        entry["emission_id"]: entry
        for entry in record["relay_integration_trace"]
        if entry["emission_id"] is not None
    }
    emission_classes = [
        trace_by_emission.get(emission["event_id"], {}).get("classification")
        for emission in relay_emissions
    ]
    class_ok = (
        all(value == "integrated_discharge" for value in emission_classes)
        if expected_relay_emissions
        else len(relay_emissions) == 0
    )
    no_multi_discharge = all(
        abs(float(entry["discharge_amount"])) <= 1.0 + Z_TOLERANCE
        for entry in record["relay_integration_trace"]
    ) and sum(
        float(entry["discharge_amount"]) != 0.0
        for entry in record["relay_integration_trace"]
    ) <= sum(
        entry["destination"] == "relay" and entry["event_type"] != EventType.INTERNAL.value
        for entry in record["processed_events"]
    )
    z_bound = all(
        abs(float(entry["z_before_decay"])) <= 4.0 + Z_TOLERANCE
        and abs(float(entry["z_after_decay"])) <= 4.0 + Z_TOLERANCE
        and abs(float(entry["z_after_input"])) <= 4.0 + Z_TOLERANCE
        and abs(float(entry["z_post_discharge"])) <= 4.0 + Z_TOLERANCE
        for entry in record["relay_integration_trace"]
    )
    probe = record["neutral_probe"]
    probe_ok = (
        probe["event_count"] == 1
        and probe["delay_from_last_input_or_discharge"] >= 10.0 * record["tau_z"]
        and (
            not record["integration_enabled"]
            or abs(float(probe["z_after_probe"])) < 1e-4
        )
    )
    equations = _analytic_recurrence_check(record)
    analytic_expected = None
    analytic_observed = None
    if record["integration_enabled"]:
        if fixture == "ISOLATED":
            analytic_expected = 0.4
            analytic_observed = abs(float(record["relay_integration_trace"][0]["z_after_input"]))
        elif fixture in PREDICTED_FIXTURE_MAGNITUDES[record["decay_rate_z"]]:
            analytic_expected = PREDICTED_FIXTURE_MAGNITUDES[record["decay_rate_z"]][fixture]
            target = [
                entry
                for entry in record["relay_integration_trace"]
                if entry["input_value"] != 0.0
            ]
            analytic_observed = abs(float(target[-1]["z_after_input"]))
    analytic_ok = (
        analytic_expected is None
        or abs(float(analytic_observed) - analytic_expected) <= PREDICTION_TOLERANCE
    )
    expected_is_integrated = fixture in ("NEAR_TRIPLE", "NEGATIVE_NEAR_TRIPLE") and record["integration_enabled"]
    if expected_is_integrated and relay_emissions:
        discharge_entry = next(
            entry
            for entry in record["relay_integration_trace"]
            if entry["emission_id"] == relay_emissions[0]["event_id"]
        )
        observed_peak = max(
            abs(float(discharge_entry["x_post_discharge"])),
            abs(float(discharge_entry["x_at_emission"])),
        )
        expected_payload = math.copysign(
            0.25 + (1.0 - 0.25) * min(1.0, max(0.0, (observed_peak - 1.0) / (4.0 - 1.0))),
            float(discharge_entry["x_post_discharge"]),
        )
        emission_payload_ok = abs(float(relay_emissions[0]["payload"]) - expected_payload) <= PREDICTION_TOLERANCE
        polarity_ok = math.copysign(1.0, float(relay_emissions[0]["payload"])) == math.copysign(1.0, float(discharge_entry["x_post_discharge"]))
    else:
        observed_peak = None
        expected_payload = None
        emission_payload_ok = not relay_emissions
        polarity_ok = not relay_emissions
    causality_ok = len(relay_emissions) <= len(record["transfers"]) and all(
        (
            emission["event_id"] in trace_by_emission
            and float(emission["timestamp"])
            > float(trace_by_emission[emission["event_id"]]["timestamp"])
            and any(
                float(transfer["timestamp"])
                <= float(trace_by_emission[emission["event_id"]]["timestamp"])
                for transfer in record["transfers"]
            )
        )
        for emission in relay_emissions
    )
    passed = all(
        (
            payload_ok,
            class_ok,
            causality_ok,
            no_multi_discharge,
            z_bound,
            probe_ok,
            equations["passed"],
            analytic_ok,
            len(relay_emissions) == expected_relay_emissions,
            record["final_state"]["state_bounds_ok"],
            emission_payload_ok,
            polarity_ok,
        )
    )
    return {
        "passed": passed,
        "expected_relay_emissions": expected_relay_emissions,
        "observed_relay_emissions": len(relay_emissions),
        "all_source_emissions_and_model_b_payloads_match": payload_ok,
        "route_payload_tolerance": ROUTE_PAYLOAD_TOLERANCE,
        "maximum_model_b_payload_error": max(payload_deltas, default=0.0),
        "maximum_source_amplitude_error": max(source_emission_deltas, default=0.0),
        "emission_classification": emission_classes,
        "all_emissions_integration_mediated_when_required": class_ok,
        "emissions_have_causal_prior_inputs_and_positive_delay": causality_ok,
        "at_most_one_discharge_per_external_event": no_multi_discharge,
        "z_bound": z_bound,
        "neutral_probe": probe_ok,
        "recurrence": equations,
        "analytic_prediction_expected_abs_z": analytic_expected,
        "analytic_prediction_observed_abs_z": analytic_observed,
        "analytic_prediction_match": analytic_ok,
        "ordinary_emission_payload": {
            "observed_peak": observed_peak,
            "expected_payload": expected_payload,
            "observed_payload": (
                None if not relay_emissions else float(relay_emissions[0]["payload"])
            ),
            "matches": emission_payload_ok,
            "polarity_matches_captured_state": polarity_ok,
        },
        "input_causality": len(relay_emissions) <= len(record["transfers"]),
    }


def _run_phase_a_once() -> dict[str, Any]:
    outcomes: list[dict[str, Any]] = []
    for decay_rate_z in CANDIDATES:
        for fixture in PHASE_A_FIXTURES:
            record = _run_phase_a_fixture(decay_rate_z, fixture)
            record["validation"] = _phase_a_expectation(record)
            record["record_digest"] = _digest(record)
            outcomes.append(record)
    by_candidate: dict[str, dict[str, Any]] = {}
    for candidate in CANDIDATES:
        candidate_records = [
            item for item in outcomes if item["decay_rate_z"] == candidate
        ]
        by_candidate[str(candidate)] = {
            "fixtures": {
                item["fixture"]: {
                    "passed": item["validation"]["passed"],
                    "digest": item["record_digest"],
                    "relay_emissions": item["validation"]["observed_relay_emissions"],
                }
                for item in candidate_records
            },
            "passed": all(item["validation"]["passed"] for item in candidate_records),
        }
    passing = [candidate for candidate in CANDIDATES if by_candidate[str(candidate)]["passed"]]
    selected = max(passing) if passing else None
    return {
        "candidate_order": list(CANDIDATES),
        "records": outcomes,
        "candidate_outcomes": by_candidate,
        "selected_decay_rate_z": selected,
        "selection_rule": "largest decay_rate_z among candidates passing every Phase-A fixture",
        "all_fixtures_passed_some_candidate": selected is not None,
    }


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

    def observe(
        self,
        ledger: EligibilityLedger,
        callback: Any,
        timestamp: float,
        trace_id: str | None,
    ) -> Any:
        before = {trace.trace_id for trace in ledger.traces}
        stats = self.stats[ledger.ledger_id]
        try:
            result = callback()
        except EligibilityCapacityError:
            self.capacity_errors.append(
                {
                    "ledger_id": ledger.ledger_id,
                    "trace_id": trace_id,
                    "timestamp": timestamp,
                    "occupancy": len(before),
                    "capacity": ledger.max_traces,
                }
            )
            raise
        after = {trace.trace_id for trace in ledger.traces}
        stats["created"] += len(after - before)
        stats["removed"] += len(before - after)
        stats["peak"] = max(stats["peak"], len(after))
        return result

    def finalize(self) -> list[dict[str, Any]]:
        values = []
        for ledger_id, stats in self.stats.items():
            item = dict(stats)
            ledger = self.ledgers[ledger_id]
            item["final"] = len(ledger.traces)
            item["reconciles"] = (
                item["initial"] + item["created"] - item["removed"] == item["final"]
            )
            values.append(item)
        return sorted(values, key=lambda item: item["ledger_id"])


def _point_batches(points: Iterable[Any]) -> tuple[tuple[tuple[float, float], ...], ...]:
    batches: list[list[tuple[float, float]]] = []
    last_timestamp: float | None = None
    for point in points:
        timestamp = float(point.timestamp)
        value = float(point.x) + float(point.y)
        if not math.isfinite(timestamp) or not math.isfinite(value):
            raise StopCondition("invalid Phase-B input timestamp or value", {})
        if last_timestamp is not None and timestamp < last_timestamp:
            raise StopCondition("Phase-B timestamps are not ordered", {"timestamp": timestamp})
        if not batches or timestamp != last_timestamp:
            batches.append([])
        batches[-1].append((timestamp, value))
        last_timestamp = timestamp
    return tuple(tuple(batch) for batch in batches)


def _phase_b_topology() -> BoundedTopology:
    return BoundedTopology.from_edges(
        PHASE_B_NODES,
        (
            Edge("source", "relay", 1.0, edge_weight=1.0, divider_strength=1.0, reference=0.0),
            Edge("relay", "destination", 1.0, edge_weight=1.0, divider_strength=1.0, reference=0.0),
        ),
        fan_in_limit=2,
        fan_out_limit=2,
        edge_capacity=3,
        routing_capacity=3,
    )


def _runtime_trace_record(item: tuple[Any, ...]) -> dict[str, Any]:
    fields = (
        "timestamp",
        "source",
        "destination",
        "event_type",
        "payload",
        "sequence",
        "event_id",
        "lineage_id",
        "causal_roots",
        "route_depth",
        "route_path",
        "roots_truncated",
    )
    return {key: _jsonable(value) for key, value in zip(fields, item)}


def _phase_b_character(
    *,
    arm: str,
    decay_rate_z: float,
    seed: int,
    sequence_index: int,
    points: tuple[Any, ...],
) -> dict[str, Any]:
    integration = None
    if arm == "CALIBRATED":
        integration = IntegrationConfig(decay_rate_z=decay_rate_z)
    elif arm == "DEFAULT":
        integration = IntegrationConfig()
    elif arm != "DISABLED":
        raise ValueError(f"unknown Phase-B arm: {arm}")
    neuron_map = {
        node: MultiExcursionNeuron(
            node,
            config=E1Config(
                event_budget=PHASE_B_NEURON_EVENT_BUDGET,
                integration=integration if node == "relay" else None,
            ),
        )
        for node in PHASE_B_NODES
    }
    neurons = tuple(neuron_map[node] for node in PHASE_B_NODES)
    topology = _phase_b_topology()
    batches = _point_batches(points)
    input_digest = _digest(batches)
    character_id = f"c{seed:02d}-{sequence_index:03d}"
    runtime = ExcursionCharacterRuntime(
        neurons,
        topology,
        queue_capacity=PHASE_B_QUEUE_CAPACITY,
        event_budget=PHASE_B_RUNTIME_EVENT_BUDGET,
        settling_horizon=PHASE_B_SETTLING_HORIZON,
        prediction_capacity=PHASE_B_PREDICTION_CAPACITY,
        prediction_expiry=PHASE_B_PREDICTION_EXPIRY,
        max_activity_events=PHASE_B_MAX_ACTIVITY_EVENTS,
        namespace=f"luna41-{arm.lower()}-seed-{seed}",
        eligibility_capacity=PHASE_B_ELIGIBILITY_CAPACITY,
    )
    audit = _EligibilityAudit()
    original_reset = MultiExcursionNeuron.reset
    original_ledger_init = EligibilityLedger.__init__
    original_record_activity = EligibilityLedger.record_activity
    original_apply_signal = EligibilityLedger.apply_signal
    neuron_snapshots: dict[str, dict[str, Any]] = {}

    def capture_reset(neuron: MultiExcursionNeuron, *, timestamp: float = 0.0) -> None:
        neuron_snapshots[neuron.neuron_id] = {
            "emissions": [_emission_record(item) for item in neuron.emissions],
            "integration_trace": [_jsonable(item) for item in neuron.integration_trace],
            "x": float(neuron.state),
            "z": (
                None
                if neuron.integration_state is None
                else float(neuron.integration_state)
            ),
            "last_update_timestamp": float(neuron.last_update_timestamp),
            "processed_events": neuron.processed_event_count,
        }
        original_reset(neuron, timestamp=timestamp)

    def ledger_init(ledger: EligibilityLedger, *args: Any, **kwargs: Any) -> None:
        original_ledger_init(ledger, *args, **kwargs)
        audit.register(ledger)

    def record_activity(ledger: EligibilityLedger, event: Event) -> Any:
        return audit.observe(
            ledger,
            lambda: original_record_activity(ledger, event),
            event.timestamp,
            getattr(event.payload, "trace_id", None),
        )

    def apply_signal(ledger: EligibilityLedger, event: Event) -> Any:
        return audit.observe(
            ledger,
            lambda: original_apply_signal(ledger, event),
            event.timestamp,
            getattr(event.payload, "trace_id", None),
        )

    try:
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(MultiExcursionNeuron, "reset", capture_reset))
            stack.enter_context(mock.patch.object(EligibilityLedger, "__init__", ledger_init))
            stack.enter_context(
                mock.patch.object(EligibilityLedger, "record_activity", record_activity)
            )
            stack.enter_context(
                mock.patch.object(EligibilityLedger, "apply_signal", apply_signal)
            )
            runtime.start_character(
                character_id,
                sequence_index,
                timestamp=0.0,
                predictor_source="source",
                readout_sources=PHASE_B_NODES,
                input_destination="source",
            )
            for batch in batches:
                runtime.admit_external_batch(batch)
            last_timestamp = batches[-1][-1][0] if batches else 0.0
            runtime_result = runtime.end_character(
                last_external_timestamp=last_timestamp,
                reward=0.0,
                reward_delay=0.0,
                reward_message_id=f"luna41-neutral-{character_id}",
            )
    except EligibilityCapacityError as error:
        raise StopCondition(
            "Phase-B eligibility capacity exceeded",
            {
                "arm": arm,
                "seed": seed,
                "character_id": character_id,
                "capacity_errors": audit.capacity_errors,
                "message": str(error),
            },
        ) from error
    except (QueueCapacityError, TopologyCapacityError, BufferError) as error:
        raise StopCondition(
            "Phase-B bounded runtime capacity exceeded",
            {
                "arm": arm,
                "seed": seed,
                "character_id": character_id,
                "exception": type(error).__name__,
                "message": str(error),
            },
        ) from error
    except Exception as error:
        raise StopCondition(
            "Phase-B production runtime exception",
            {
                "arm": arm,
                "seed": seed,
                "character_id": character_id,
                "exception": type(error).__name__,
                "message": str(error),
            },
        ) from error

    ledgers = audit.finalize()
    if (
        len(ledgers) != len(PHASE_B_NODES)
        or any(item["capacity"] != PHASE_B_ELIGIBILITY_CAPACITY for item in ledgers)
        or any(not item["reconciles"] for item in ledgers)
        or any(item["peak"] >= PHASE_B_ELIGIBILITY_CAPACITY for item in ledgers)
        or audit.capacity_errors
    ):
        raise StopCondition(
            "Phase-B eligibility ledger reconciliation/capacity failure",
            {"ledgers": ledgers, "capacity_errors": audit.capacity_errors},
        )
    if (
        runtime_result.execution.budget_exhausted
        or runtime_result.execution.pending_event_count != 0
        or not runtime_result.execution.completed
    ):
        raise StopCondition(
            "Phase-B runtime did not settle within declared event bounds",
            {
                "arm": arm,
                "seed": seed,
                "character_id": character_id,
                "execution": _jsonable(runtime_result.execution),
            },
        )
    for snapshot in neuron_snapshots.values():
        if (
            abs(float(snapshot["x"])) > 8.0
            or (
                snapshot["z"] is not None
                and abs(float(snapshot["z"])) > 4.0
            )
        ):
            raise StopCondition(
                "Phase-B neuron state exceeded a configured bound",
                {
                    "arm": arm,
                    "seed": seed,
                    "character_id": character_id,
                    "snapshot": snapshot,
                },
            )

    trace_records = [_runtime_trace_record(item) for item in runtime_result.trace]
    route_events = [
        item
        for item in trace_records
        if item["event_type"] == EventType.EXCURSION.value
    ]
    relay_trace = neuron_snapshots["relay"]["integration_trace"]
    relay_emissions = neuron_snapshots["relay"]["emissions"]
    classified_emissions = []
    for emission in relay_emissions:
        trace_entry = next(
            (
                entry
                for entry in relay_trace
                if entry["emission_id"] == emission["event_id"]
            ),
            None,
        )
        classification = (
            "integration-mediated"
            if trace_entry is not None
            and trace_entry["classification"] == "integrated_discharge"
            else "direct"
        )
        classified_emissions.append(
            {
                **emission,
                "classification": classification,
                "trace_classification": (
                    None if trace_entry is None else trace_entry["classification"]
                ),
                "integration_trace": trace_entry,
            }
        )
    transfers = [
        item
        for item in route_events
        if item["source"] in ("source", "relay")
        and (item["source"], item["destination"])
        in (("source", "relay"), ("relay", "destination"))
    ]
    source_emissions = neuron_snapshots["source"]["emissions"]
    destination_emissions = neuron_snapshots["destination"]["emissions"]
    expected_payloads = {
        item["event_id"]: math.tanh(float(item["payload"]))
        for item in source_emissions + relay_emissions
    }
    route_payload_checks = [
        {
            "event_id": item["event_id"],
            "source": item["source"],
            "destination": item["destination"],
            "timestamp": item["timestamp"],
            "payload": item["payload"],
            "expected_model_b_payload": expected_payloads.get(item["event_id"]),
            "matches": (
                item["event_id"] in expected_payloads
                and abs(float(item["payload"]) - expected_payloads[item["event_id"]])
                <= PREDICTION_TOLERANCE
            ),
        }
        for item in transfers
    ]
    return {
        "arm": arm,
        "decay_rate_z": decay_rate_z if arm == "CALIBRATED" else (0.1 if arm == "DEFAULT" else None),
        "seed": seed,
        "sequence_index": sequence_index,
        "character_id": character_id,
        "input_digest": input_digest,
        "input_batches": batches,
        "source_emissions": source_emissions,
        "relay_emissions": classified_emissions,
        "destination_emissions": destination_emissions,
        "routed_signal_transfers": transfers,
        "model_b_transfer_checks": route_payload_checks,
        "relay_integration_trace": relay_trace,
        "destination_receptions": [
            item for item in trace_records
            if item["destination"] == "destination"
            and item["event_type"] == EventType.EXCURSION.value
        ],
        "runtime_events": trace_records,
        "resource_high_water": {
            "queue_capacity": PHASE_B_QUEUE_CAPACITY,
            "queue_peak": runtime_result.peak_queue_occupancy,
            "runtime_event_budget": PHASE_B_RUNTIME_EVENT_BUDGET,
            "processed_events": runtime_result.execution.processed_event_count,
            "runtime_pending_events": runtime_result.execution.pending_event_count,
            "max_activity_events": PHASE_B_MAX_ACTIVITY_EVENTS,
            "eligibility_ledgers": ledgers,
            "prediction_capacity": PHASE_B_PREDICTION_CAPACITY,
            "prediction_expired": runtime_result.expired_predictions,
        },
        "settling": {
            "completed": runtime_result.execution.completed,
            "termination_reason": runtime_result.execution.termination_reason,
            "last_event_timestamp": runtime_result.execution.last_event_timestamp,
            "horizon": last_timestamp + PHASE_B_SETTLING_HORIZON,
        },
        "state_at_teardown": neuron_snapshots,
        "counts": {
            "source_emissions": len(source_emissions),
            "relay_emissions": len(classified_emissions),
            "relay_integrated_emissions": sum(
                item["classification"] == "integration-mediated"
                for item in classified_emissions
            ),
            "relay_direct_emissions": sum(
                item["classification"] == "direct" for item in classified_emissions
            ),
            "signal_transfers": len(transfers),
            "destination_receptions": len(
                [
                    item for item in trace_records
                    if item["destination"] == "destination"
                    and item["event_type"] == EventType.EXCURSION.value
                ]
            ),
            "destination_emissions": len(destination_emissions),
            "relay_max_abs_z": max(
                (
                    abs(float(entry[key]))
                    for entry in relay_trace
                    for key in (
                        "z_before_decay",
                        "z_after_decay",
                        "z_after_input",
                        "z_post_discharge",
                    )
                ),
                default=0.0,
            ),
        },
        "causality_reconciles": (
            all(item["matches"] for item in route_payload_checks)
            and len(transfers)
            == len(
                [
                    emission
                    for emission in source_emissions + relay_emissions
                    if any(
                        edge["source"] == emission["source"]
                        for edge in (
                            {"source": "source"},
                            {"source": "relay"},
                        )
                    )
                ]
            )
            and all(
                item["timestamp"] >= next(
                    emission["timestamp"]
                    for emission in source_emissions + relay_emissions
                    if emission["event_id"] == item["event_id"]
                )
                for item in transfers
            )
        ),
    }


def _phase_b_once(selected_decay_rate_z: float) -> dict[str, Any]:
    records: dict[str, dict[str, list[dict[str, Any]]]] = {
        arm: {str(seed): [] for seed in SEEDS} for arm in PHASE_B_ARMS
    }
    input_digests: dict[str, dict[str, str]] = {}
    for arm in PHASE_B_ARMS:
        for seed in SEEDS:
            sequences = luna39.base._training_point_sequences(seed)
            if len(sequences) != 64:
                raise StopCondition(
                    "frozen stream did not produce 64 point sequences",
                    {"seed": seed, "observed": len(sequences)},
                )
            seed_records: list[dict[str, Any]] = []
            records[arm][str(seed)] = seed_records
            for sequence_index, points in enumerate(sequences):
                record = _phase_b_character(
                    arm=arm,
                    decay_rate_z=selected_decay_rate_z,
                    seed=seed,
                    sequence_index=sequence_index,
                    points=points,
                )
                record["record_digest"] = _digest(record)
                seed_records.append(record)
            input_digests[arm][str(seed)] = _digest(
                [item["input_digest"] for item in seed_records]
            )
    paired_input_invariance = all(
        input_digests[arm][str(seed)] == input_digests["CALIBRATED"][str(seed)]
        for arm in PHASE_B_ARMS
        for seed in SEEDS
    )
    if not paired_input_invariance:
        raise StopCondition(
            "Phase-B source input streams differ across paired arms",
            {"input_digests": input_digests},
        )
    all_records = [
        record
        for arm in PHASE_B_ARMS
        for seed in SEEDS
        for record in records[arm][str(seed)]
    ]
    return {
        "selected_decay_rate_z": selected_decay_rate_z,
        "records": records,
        "input_digests": input_digests,
        "paired_input_invariance": paired_input_invariance,
        "execution_count": len(all_records),
        "summary": {
            arm: {
                "characters": sum(len(records[arm][str(seed)]) for seed in SEEDS),
                "source_emissions": sum(
                    record["counts"]["source_emissions"]
                    for seed in SEEDS
                    for record in records[arm][str(seed)]
                ),
                "relay_emissions": sum(
                    record["counts"]["relay_emissions"]
                    for seed in SEEDS
                    for record in records[arm][str(seed)]
                ),
                "relay_integrated_emissions": sum(
                    record["counts"]["relay_integrated_emissions"]
                    for seed in SEEDS
                    for record in records[arm][str(seed)]
                ),
                "relay_direct_emissions": sum(
                    record["counts"]["relay_direct_emissions"]
                    for seed in SEEDS
                    for record in records[arm][str(seed)]
                ),
                "source_to_relay_transfers": sum(
                    sum(
                        item["source"] == "source" and item["destination"] == "relay"
                        for item in record["routed_signal_transfers"]
                    )
                    for seed in SEEDS
                    for record in records[arm][str(seed)]
                ),
                "relay_to_destination_transfers": sum(
                    sum(
                        item["source"] == "relay" and item["destination"] == "destination"
                        for item in record["routed_signal_transfers"]
                    )
                    for seed in SEEDS
                    for record in records[arm][str(seed)]
                ),
                "destination_receptions": sum(
                    record["counts"]["destination_receptions"]
                    for seed in SEEDS
                    for record in records[arm][str(seed)]
                ),
                "destination_emissions": sum(
                    record["counts"]["destination_emissions"]
                    for seed in SEEDS
                    for record in records[arm][str(seed)]
                ),
                "max_abs_z": max(
                    (
                        record["counts"]["relay_max_abs_z"]
                        for seed in SEEDS
                        for record in records[arm][str(seed)]
                    ),
                    default=0.0,
                ),
                "all_causality_checks_pass": all(
                    record["causality_reconciles"]
                    for seed in SEEDS
                    for record in records[arm][str(seed)]
                ),
                "resource_high_water": {
                    "queue_peak": max(
                        record["resource_high_water"]["queue_peak"]
                        for seed in SEEDS
                        for record in records[arm][str(seed)]
                    ),
                    "runtime_event_peak": max(
                        record["resource_high_water"]["processed_events"]
                        for seed in SEEDS
                        for record in records[arm][str(seed)]
                    ),
                    "eligibility_peak": max(
                        ledger["peak"]
                        for seed in SEEDS
                        for record in records[arm][str(seed)]
                        for ledger in record["resource_high_water"]["eligibility_ledgers"]
                    ),
                },
            }
            for arm in PHASE_B_ARMS
        },
    }


def _phase_a_summary(phase_a: dict[str, Any]) -> dict[str, Any]:
    return {
        "selected_decay_rate_z": phase_a["selected_decay_rate_z"],
        "candidate_outcomes": phase_a["candidate_outcomes"],
        "records": [
            {
                "decay_rate_z": item["decay_rate_z"],
                "fixture": item["fixture"],
                "passed": item["validation"]["passed"],
                "digest": item["record_digest"],
            }
            for item in phase_a["records"]
        ],
    }


def _write_json(path: Path, value: Any) -> None:
    path.write_text(_canonical_json(value) + "\n", encoding="utf-8")


def run_experiment(
    output_directory: Path = ARTIFACT_DIRECTORY,
) -> tuple[dict[str, Any], dict[str, Any]]:
    output_directory.mkdir(parents=True, exist_ok=True)
    frozen_config = experiment_config()
    phase_a_first = _run_phase_a_once()
    phase_a_replay = _run_phase_a_once()
    phase_a_first_digest = _digest(phase_a_first)
    phase_a_replay_digest = _digest(phase_a_replay)
    phase_a_replay_equal = phase_a_first_digest == phase_a_replay_digest
    phase_a = {
        **phase_a_first,
        "replay": {
            "initial_digest": phase_a_first_digest,
            "replay_digest": phase_a_replay_digest,
            "equal": phase_a_replay_equal,
        },
    }
    selected = phase_a_first["selected_decay_rate_z"]
    fatal_phase_a_records = [
        {
            "decay_rate_z": record["decay_rate_z"],
            "fixture": record["fixture"],
            "payload_match": record["validation"][
                "all_source_emissions_and_model_b_payloads_match"
            ],
            "recurrence_match": record["validation"]["recurrence"]["passed"],
            "state_bounds": record["final_state"]["state_bounds_ok"],
            "neutral_probe": record["validation"]["neutral_probe"],
        }
        for record in phase_a_first["records"]
        if (
            not record["validation"]["all_source_emissions_and_model_b_payloads_match"]
            or not record["validation"]["recurrence"]["passed"]
            or not record["final_state"]["state_bounds_ok"]
            or not record["validation"]["neutral_probe"]
        )
    ]
    phase_a["fatal_contract_violations"] = fatal_phase_a_records
    frozen_phase_a = _phase_a_summary(phase_a_first)
    frozen_record = {
        "schema": "TPCN-LUNA41-PHASE-A-FREEZE-1",
        "recorded_before_phase_b_stream_creation": True,
        "configuration_digest": _digest(frozen_config),
        "selected_decay_rate_z": selected,
        "selection_rule": phase_a_first["selection_rule"],
        "phase_a_results_digest": phase_a_first_digest,
        "phase_a_replay": {
            "initial_digest": phase_a_first_digest,
            "replay_digest": phase_a_replay_digest,
            "equal": phase_a_replay_equal,
        },
        "phase_a_summary_digest": _digest(frozen_phase_a),
        "fixed_parameters": frozen_config["phase_a"]["fixed_neuron_parameters"],
        "candidate_outcomes": phase_a_first["candidate_outcomes"],
        "complete_phase_a_records": phase_a_first["records"],
    }
    frozen_record_digest = _digest(frozen_record)
    frozen_record["freeze_record_digest"] = frozen_record_digest
    _write_json(output_directory / "phase_a_freeze.json", frozen_record)
    freeze = {
        "configuration": {
            "decay_rate_z": selected,
            "fixed": frozen_config["phase_a"]["fixed_neuron_parameters"],
        },
        "phase_a_digest": _digest(frozen_phase_a),
        "phase_a_results_digest": phase_a_first_digest,
        "selection_rule": phase_a_first["selection_rule"],
        "freeze_record_digest": frozen_record_digest,
        "phase_b_created_after_freeze": False,
    }
    if not phase_a_replay_equal:
        phase_b = None
        terminal_status = "BLOCKED"
        stop_reason = "Phase-A deterministic replay mismatch"
    elif fatal_phase_a_records:
        phase_b = None
        terminal_status = "BLOCKED"
        if any(not item["payload_match"] for item in fatal_phase_a_records):
            stop_reason = (
                "Phase-A source canonical emission/Model-B route did not produce "
                "the declared +/-0.4 payload within floating-point tolerance"
            )
        elif any(not item["recurrence_match"] for item in fatal_phase_a_records):
            stop_reason = "Phase-A ACP-0008 recurrence did not match the production trace"
        elif any(not item["state_bounds"] for item in fatal_phase_a_records):
            stop_reason = "Phase-A neuron state exceeded a declared bound"
        else:
            stop_reason = "Phase-A neutral-return probe did not meet its declared criterion"
    elif selected is None:
        phase_b = None
        terminal_status = "NOT SUPPORTED IN THIS SETUP"
        stop_reason = "No predeclared decay_rate_z candidate passed every Phase-A fixture"
    else:
        freeze["phase_b_created_after_freeze"] = True
        # The Phase-A decision and digest are fixed before the point streams are generated.
        try:
            phase_b_first = _phase_b_once(selected)
            phase_b_replay = _phase_b_once(selected)
            phase_b_first_digest = _digest(phase_b_first)
            phase_b_replay_digest = _digest(phase_b_replay)
            phase_b = {
                **phase_b_first,
                "deterministic_replay": {
                    "initial_digest": phase_b_first_digest,
                    "replay_digest": phase_b_replay_digest,
                    "equal": phase_b_first_digest == phase_b_replay_digest,
                },
            }
        except StopCondition as error:
            phase_b = {
                "blocked": {
                    "reason": error.reason,
                    "detail": error.detail,
                }
            }
            terminal_status = "BLOCKED"
            stop_reason = error.reason
        if phase_b is not None and "blocked" not in phase_b:
            if phase_b["deterministic_replay"]["equal"] and all(
                arm_summary["all_causality_checks_pass"]
                for arm_summary in phase_b["summary"].values()
            ):
                relay_supported = (
                    phase_b["summary"]["CALIBRATED"]["relay_integrated_emissions"] > 0
                )
                terminal_status = (
                    "SUPPORTED"
                    if relay_supported
                    else "NOT SUPPORTED IN THIS SETUP"
                )
                stop_reason = None
            else:
                terminal_status = "BLOCKED"
                stop_reason = (
                    "Phase-B replay, event reconciliation, or causal Model-B validation failed"
                )

    results = {
        "schema": "TPCN-LUNA41-ACP0008-TEMPORAL-CALIBRATION-RESULTS-1",
        "authorization_revision": START_REVISION,
        "execution_revision": None,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "analytic_prediction": {
            "status": "pre-execution prediction, not an observation",
            "only_expected_candidate": 0.0125,
            "predictions": PREDICTED_FIXTURE_MAGNITUDES,
        },
        "phase_a": phase_a,
        "freeze": freeze,
        "phase_b": phase_b,
        "terminal_status": terminal_status,
        "stop_reason": stop_reason,
        "interpretation_boundary": (
            "Bounded ACP-0008 configuration and mechanism evidence only; no efficacy, "
            "task performance, ACP-0007, structural growth, energy benefit, hardware "
            "equivalence, biological realism, parameter optimality, or promotion claim."
        ),
    }
    result_digest = _digest(results)
    summary = {
        "schema": "TPCN-LUNA41-ACP0008-TEMPORAL-CALIBRATION-SUMMARY-1",
        "terminal_status": terminal_status,
        "stop_reason": stop_reason,
        "selected_decay_rate_z": selected,
        "phase_a_replay": phase_a["replay"],
        "phase_b_replay": (
            None if phase_b is None else phase_b["deterministic_replay"]
        ),
        "phase_a_candidate_outcomes": phase_a["candidate_outcomes"],
        "phase_b_summary": None if phase_b is None else phase_b["summary"],
        "results_digest": result_digest,
        "phase_a_passed": selected is not None and phase_a_replay_equal,
        "phase_b_run": phase_b is not None,
        "acp0008_status": "experimental, opt-in, unpromoted",
        "acp0007_enabled": False,
    }
    output_directory.mkdir(parents=True, exist_ok=True)
    for name, value in (
        ("config.json", frozen_config),
        ("results.json", results),
        ("summary.json", summary),
    ):
        _write_json(output_directory / name, value)
    return results, summary


def main() -> None:
    _, summary = run_experiment()
    print(_canonical_json(summary))


if __name__ == "__main__":
    main()
