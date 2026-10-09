from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from experiments.luna54 import run as luna54
from experiments.luna55 import run as luna55


ROOT = Path(__file__).resolve().parents[1]


def test_luna55_retained_phase_pins_and_population_partition():
    selection, categories, retained = luna55._phase_pins_and_populations()
    compatibility = luna55._verify_phase_compatibility(selection, retained)

    assert len(categories) == 320
    assert len(luna55.TARGET_IDS) == 16
    assert compatibility["passed"]
    assert compatibility["phase_checks"]["initial"]["matched_arrivals"] == 235
    assert compatibility["phase_checks"]["replay"]["matched_historical_destination_traces"] == 235


def test_luna55_has_only_two_frozen_factorial_settings():
    selection = json.loads(
        (ROOT / "experiments/luna55/config.json").read_text(encoding="utf-8")
    )
    frozen = json.loads(
        (ROOT / "artifacts/luna45-depth2-frozen-config-20261006-r2/config.json").read_text(
            encoding="utf-8"
        )
    )
    nodes = frozen["neuron_configurations"]["DESTINATION_CALIBRATED"]
    expected = {
        "HH": (0.0125, 0.0125, []),
        "RH": (0.00125, 0.0125, ["relay.integration.decay_rate_z"]),
        "HR": (0.0125, 0.00125, ["destination.integration.decay_rate_z"]),
        "RR": (
            0.00125,
            0.00125,
            ["destination.integration.decay_rate_z", "relay.integration.decay_rate_z"],
        ),
    }
    for arm, (relay_rate, destination_rate, changed_paths) in expected.items():
        relay, destination, _ = luna55._make_configs(
            frozen, selection["conditions"][arm]
        )
        relay_record = luna54.jsonable(relay)
        destination_record = luna54.jsonable(destination)
        baseline = {"relay": nodes["relay"], "destination": nodes["destination"]}
        actual = {"relay": relay_record, "destination": destination_record}
        assert relay.integration.decay_rate_z == relay_rate
        assert destination.integration.decay_rate_z == destination_rate
        assert luna54._diff_paths(baseline, actual) == changed_paths


def test_destination_response_requires_linked_emission_and_complete_roots():
    row = {
        "destination_integration_traces": [
            {"discharge_amount": 1.0, "emission_id": "destination:1"}
        ],
        "destination_emissions": [{"event_id": "destination:1"}],
        "destination_discharge_count": 1,
        "route_lineage_authenticated": True,
        "route_links_complete": True,
        "destination_receptions": [{"roots_truncated": False}],
    }

    assert luna55._response_l54(row)
    truncated = deepcopy(row)
    truncated["destination_receptions"][0]["roots_truncated"] = True
    assert not luna55._response_l54(truncated)
    unlinked = deepcopy(row)
    unlinked["destination_emissions"] = []
    assert not luna55._response_l54(unlinked)


def test_destination_only_response_requires_linked_emission_and_matched_roots():
    row = {
        "integration_traces": [
            {"discharge_amount": 1.0, "emission_id": "destination:1"}
        ],
        "emissions": [{"event_id": "destination:1"}],
        "discharge_count": 1,
        "root_lineage_complete": True,
    }
    assert luna55._response_l53(row)
    assert not luna55._response_l53({**row, "root_lineage_complete": False})
