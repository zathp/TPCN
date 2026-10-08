from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from experiments.luna54 import run as luna54


ROOT = Path(__file__).resolve().parents[1]
FROZEN_CONFIG = json.loads(
    (ROOT / "artifacts/luna45-depth2-frozen-config-20261006-r2/config.json").read_bytes()
)
LUNA54_CONFIG = json.loads(
    (ROOT / "experiments/luna54/config.json").read_bytes()
)
BOUNDS = {
    "runtime": LUNA54_CONFIG["runtime"],
    "topology": LUNA54_CONFIG["topology"],
}


def _synthetic_inputs(values: tuple[float, ...]) -> list[dict[str, object]]:
    events = []
    for index, value in enumerate(values):
        timestamp = float(index * 20)
        events.append(
            {
                "event_id": f"synthetic-source:{index}",
                "queue_sequence": index,
                "source_queue_sequence": index,
                "source": "source",
                "destination": "relay",
                "receiver_node": "relay",
                "event_type": "excursion",
                "payload": value,
                "payload_bits": luna54.float_bits(value),
                "lineage_id": 1,
                "originating_emission_id": f"synthetic-source:{index}",
                "scheduled_delivery_timestamp": timestamp,
                "reception_timestamp": timestamp,
                "causal_roots": [f"synthetic-root:{index}"],
                "roots_truncated": False,
                "route_depth": 1,
                "route_path": ["source", "relay"],
            }
        )
    return events


def _config(condition: str):
    relay, destination, _ = luna54._config_for_condition(
        condition, FROZEN_CONFIG, LUNA54_CONFIG
    )
    return relay, destination


def test_condition_isolation_changes_only_relay_decay() -> None:
    _, _, control = luna54._config_for_condition(
        "control", FROZEN_CONFIG, LUNA54_CONFIG
    )
    _, _, intervention = luna54._config_for_condition(
        "intervention", FROZEN_CONFIG, LUNA54_CONFIG
    )

    assert control["changed_paths_from_historical"] == []
    assert intervention["changed_paths_from_historical"] == [
        "relay.integration.decay_rate_z"
    ]
    assert control["destination"] == intervention["destination"]


def test_retained_input_order_is_preserved_and_intervention_routes() -> None:
    control_relay, control_destination = _config("control")
    treatment_relay, treatment_destination = _config("intervention")
    inputs = _synthetic_inputs((0.4, 0.4, 0.4))

    control = luna54.run_stream(
        "synthetic-001", inputs, control_relay, control_destination, BOUNDS
    )
    treatment = luna54.run_stream(
        "synthetic-001", inputs, treatment_relay, treatment_destination, BOUNDS
    )

    assert [row["source_queue_sequence"] for row in treatment["source_inputs"]] == [0, 1, 2]
    assert control["relay_discharge_count"] == 0
    assert treatment["relay_discharge_count"] == 1
    assert treatment["relay_discharge_emission_count"] == 1
    assert treatment["relay_canonical_emission_count"] == 1
    assert treatment["relay_to_destination_enqueues"][0]["event_id"] == (
        treatment["relay_emissions"][0]["event_id"]
    )
    assert treatment["destination_reception_count"] == 1
    assert treatment["route_reconciliation"]["reconciles"] is True
    assert treatment["destination_threshold_crossings"] == 0


def test_independent_recurrence_rejects_a_mutated_state() -> None:
    relay, destination = _config("intervention")
    output = luna54.run_stream(
        "synthetic-002",
        _synthetic_inputs((0.4, 0.4, 0.4)),
        relay,
        destination,
        BOUNDS,
    )
    mutated = deepcopy(output["relay_integration_traces"])
    mutated[-1]["z_after_input"] += 0.01

    with pytest.raises(luna54.GateError, match="input update"):
        luna54.audit_recurrence(mutated, relay, "synthetic-002/relay")


def test_destination_decay_is_historical_under_intervention() -> None:
    relay, destination, result = luna54._config_for_condition(
        "intervention", FROZEN_CONFIG, LUNA54_CONFIG
    )

    assert relay.integration.decay_rate_z == 0.00125
    assert destination.integration.decay_rate_z == 0.0125
    assert result["only_intervention_path"] == "relay.integration.decay_rate_z"


def test_no_input_runtime_has_no_neural_or_route_output() -> None:
    relay, destination = _config("intervention")

    result = luna54.run_stream(
        "synthetic-003", [], relay, destination, BOUNDS
    )

    assert result["relay_integration_count"] == 0
    assert result["relay_discharge_count"] == 0
    assert result["relay_canonical_emission_count"] == 0
    assert result["relay_to_destination_enqueues"] == []
    assert result["destination_reception_count"] == 0
    assert result["destination_threshold_crossings"] == 0
    assert result["destination_canonical_emission_count"] == 0


def test_route_reconciliation_detects_payload_mutation() -> None:
    enqueue = {
        "event_id": "relay:excursion:1",
        "queue_sequence": 4,
        "event_type": "excursion",
        "payload": 0.5,
        "payload_bits": luna54.float_bits(0.5),
        "source": "relay",
        "destination": "destination",
        "lineage_id": 1,
        "originating_emission_id": "relay:excursion:1",
        "scheduled_delivery_timestamp": 2.0,
        "causal_roots": ["root:0"],
        "roots_truncated": False,
        "route_depth": 1,
        "route_path": ["relay", "destination"],
    }
    reception = dict(enqueue)

    assert luna54.reconcile_routes([enqueue], [reception], require_complete=True)["reconciles"]
    reception["payload"] = 0.51

    with pytest.raises(luna54.GateError, match="route reconciliation failed"):
        luna54.reconcile_routes([enqueue], [reception], require_complete=True)
