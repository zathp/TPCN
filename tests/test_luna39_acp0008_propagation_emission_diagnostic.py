from __future__ import annotations

import json
from pathlib import Path

import run_luna39_acp0008_propagation_emission_diagnostic as luna39
from tpcn.excursion_neuron import E1Config, IntegrationConfig
from tpcn.stroke_dataset import StrokePoint


def _points() -> tuple[StrokePoint, ...]:
    return (StrokePoint(0.6, 0.6, timestamp=0.0),)


def _record(arm: str, condition: str) -> dict:
    return luna39._character_record(
        arm=arm,
        seed=0,
        sequence_index=0,
        condition=condition,
        points=_points(),
    )


def test_declared_configuration_has_exact_population_and_parameters() -> None:
    config = luna39.experiment_config()
    assert config["design"]["character_condition_arm_executions"] == 1920
    assert config["network"]["eligibility_capacity"]["value"] == 1024
    assert config["arms"]["ACP0008_INTEGRATION"]["source_neuron"]["config"] == (
        config["arms"]["LEGACY_REPRODUCTION"]["source_neuron"]["config"]
    )
    destination = config["arms"]["ACP0008_INTEGRATION"]["destination_neuron"]["config"]
    assert destination["theta_e"] == 1.0
    assert destination["integration"] == {
        "decay_rate_z": 0.1,
        "input_gain": 1.0,
        "discharge_quantum": 1.0,
        "z_max": 4.0,
    }
    assert E1Config(integration=IntegrationConfig()).theta_E == 1.0


def test_explicit_capacity_reaches_both_ledgers_and_reconciles() -> None:
    record = _record("ACP0008_INTEGRATION", "DEFAULT_STATIC_EDGE")
    assert record["eligibility"]["runtime_effective_capacity"] == 1024
    ledgers = record["eligibility"]["ledgers"]
    assert len(ledgers) == 2
    assert all(item["configured_capacity"] == 1024 for item in ledgers)
    assert all(item["reconciles"] and item["peak_occupancy"] < 1024 for item in ledgers)
    assert all(
        item["initial_occupancy"] + item["created"] - item["removed"]
        == item["final_occupancy"]
        for item in ledgers
    )


def test_only_destination_has_integration_enabled() -> None:
    record = _record("ACP0008_INTEGRATION", "DEFAULT_STATIC_EDGE")
    assert record["source_config"] == record["destination_config"] | {
        "integration": None
    }
    assert record["destination_config"]["integration"] == {
        "decay_rate_z": 0.1,
        "input_gain": 1.0,
        "discharge_quantum": 1.0,
        "z_max": 4.0,
    }
    legacy = _record("LEGACY_REPRODUCTION", "DEFAULT_STATIC_EDGE")
    assert legacy["source_config"] == legacy["destination_config"]
    assert legacy["destination_integration_trace"] == []


def test_no_edge_has_no_transfer_reception_or_slow_state() -> None:
    record = _record("ACP0008_INTEGRATION", "NO_EDGE_CONTROL")
    counts = record["mechanism_counts"]
    assert record["edge"] is None
    assert counts["routed_transfers"] == 0
    assert counts["destination_receptions"] == 0
    assert counts["destination_canonical_emissions"] == 0
    assert record["destination_state_maxima"]["max_abs_z"] == 0.0
    assert record["destination_runtime_state_before_reset"]["z"] == 0.0
    assert record["destination_integration_trace"] == []
    assert record["no_edge_contaminated"] is False


def test_reception_z_and_canonical_emission_are_distinct() -> None:
    record = _record("ACP0008_INTEGRATION", "DEFAULT_STATIC_EDGE")
    counts = record["mechanism_counts"]
    assert record["execution"]["max_route_depth"] == 1
    assert counts["routed_transfers"] == counts["destination_receptions"] > 0
    assert counts["destination_z_accumulations"] > 0
    assert counts["destination_canonical_emissions"] == 0
    assert record["replay_integration_trace_equal"] is True
    assert len(record["destination_integration_trace"]) == counts["destination_receptions"]


def test_emission_classification_uses_trace_state() -> None:
    trace = [
        {
            "timestamp": 1.0,
            "integrated": True,
            "z_after_input": 0.4,
            "z_after_decay": 0.0,
            "discharge_amount": 0.0,
            "theta_z": 1.0,
            "x_after_input": 0.4,
            "theta_e": 1.0,
            "classification": "none",
        },
        {
            "timestamp": 14.0,
            "integrated": True,
            "z_after_input": 1.1,
            "z_after_decay": 0.7,
            "discharge_amount": 1.0,
            "theta_z": 1.0,
            "x_after_input": 0.5,
            "theta_e": 1.0,
            "classification": "integrated_discharge",
            "emission_id": "destination:excursion:1",
            "emission_timestamp": 14.5,
        },
    ]
    emission = {
        "event_id": "destination:excursion:1",
        "timestamp": 14.5,
    }
    assert luna39._derived_emission_classification(trace, emission) == "integrated_discharge"
    direct = [
        {
            "timestamp": 1.0,
            "integrated": False,
            "z_after_input": 0.0,
            "z_after_decay": 0.0,
            "discharge_amount": 0.0,
            "theta_z": 1.0,
            "x_after_input": 1.2,
            "theta_e": 1.0,
            "classification": "direct",
            "emission_id": "destination:excursion:2",
            "emission_timestamp": 1.5,
        }
    ]
    assert luna39._derived_emission_classification(
        direct,
        {"event_id": "destination:excursion:2", "timestamp": 1.5},
    ) == "direct"


def test_label_isolation_and_legacy_gate_checks_reference_counts() -> None:
    record = _record("LEGACY_REPRODUCTION", "STATIC_N2_BOUND_SENSITIVITY")
    serialized = json.dumps(record)
    assert '"label"' not in serialized
    assert '"class"' not in serialized
    legacy_results = {
        "runs": {
            "LEGACY_REPRODUCTION": {
                "0": {
                    "NO_EDGE_CONTROL": [record],
                    "DEFAULT_STATIC_EDGE": [record],
                    "STATIC_N2_BOUND_SENSITIVITY": [record],
                }
            }
        }
    }
    partial = luna39._legacy_gate(legacy_results, full_population=False)
    assert partial["passed"] is True
    assert partial["scope"] == "partial focused-test fixture"
    full_check = luna39._legacy_gate(legacy_results, full_population=True)
    assert full_check["passed"] is False
    assert set(full_check["mismatches"]) == set(luna39.CONDITIONS)


def test_one_seed_full_replay_is_deterministic_and_writes_artifacts(tmp_path: Path) -> None:
    results, summary = luna39.run_experiment(tmp_path, seeds=(0,))
    assert summary["deterministic_replay"]["equal"] is True
    assert summary["design_counts"]["character_condition_arm_executions"] == 384
    assert results["legacy_reproduction_gate"]["passed"] is True
    assert results["legacy_reproduction_gate"]["scope"] == "partial focused-test fixture"
    assert results["source_and_transfer_stream_invariance"]["identical"] is True
    n2 = summary["per_arm_condition"]["ACP0008_INTEGRATION"][
        "STATIC_N2_BOUND_SENSITIVITY"
    ]
    assert n2["total_destination_canonical_emissions"] > 0
    assert n2["total_integrated_emissions"] == n2["total_destination_canonical_emissions"]
    assert n2["total_direct_emissions"] == 0
    integrated_records = results["runs"]["ACP0008_INTEGRATION"]["0"][
        "STATIC_N2_BOUND_SENSITIVITY"
    ]
    timing = [
        item
        for record in integrated_records
        for item in record["integration_timing_analysis"]
    ]
    assert len(timing) == n2["total_integrated_emissions"]
    assert all(
        len(item["contributing_receptions"]) >= 2
        and item["discharge_amount"] != 0.0
        and item["z_immediately_before_final_input"] != 0.0
        for item in timing
    )
    for name in ("config.json", "results.json", "summary.json"):
        assert (tmp_path / name).is_file()
