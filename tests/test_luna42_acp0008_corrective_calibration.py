from __future__ import annotations

import math
import json
from pathlib import Path

import pytest

import run_luna42_acp0008_corrective_calibration as luna42


def test_phase_a_configuration_contains_only_predeclared_candidates() -> None:
    config = luna42.experiment_config()

    assert config["candidate_order"] == [0.1, 0.05, 0.025, 0.0125]
    assert (
        config["floating_point_policy"]["formula"]
        == "64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))"
    )
    assert config["phase_a"]["fixed_neuron_parameters"] == {
        "decay_rate": 1.0,
        "theta_E": 1.0,
        "theta_Z": 1.0,
        "input_gain": 1.0,
        "z_max": 4.0,
    }
    assert config["phase_a"]["topology"]["edge"]["w"] == 1.0
    assert config["phase_a"]["near_interval"] == 12.9
    assert config["phase_a"]["far_interval"] == 51.6
    assert (
        config["phase_a"]["pre_execution_ideal_input_predictions"][
            "predicted_selected_candidate_if_phase_a_matches_idealized_inputs"
        ]
        == 0.0125
    )
    assert config["phase_b"]["runtime"]["eligibility_capacity_per_ledger"] == 1024


def test_isolated_routed_input_preserves_exact_provenance() -> None:
    record = luna42._run_phase_a_fixture(0.1, "ISOLATED")
    validation = luna42._phase_a_expectation(record)

    assert len(record["source_input_events"]) == 1
    assert len(record["source_canonical_emissions"]) == 1
    assert len(record["transfers"]) == 1
    assert len(record["relay_receptions"]) == 1
    assert math.isclose(record["transfers"][0]["model_b_payload"], 0.4, abs_tol=1e-12)
    assert (
        record["transfers"][0]["model_b_payload"]
        == record["relay_receptions"][0]["payload"]
    )
    assert record["relay_integration_trace"][0]["z_after_input"] == 0.4
    assert record["neutral_probe"]["event_count"] == 1
    assert abs(record["neutral_probe"]["z_after_probe"]) < 1e-4
    assert validation["provenance_reconciles"]
    assert validation["transfer_reception_identity_exact"]
    assert validation["recurrence"]["passed"]
    assert validation["passed"]


def test_near_pair_uses_actual_production_routed_payloads() -> None:
    record = luna42._run_phase_a_fixture(0.1, "NEAR_PAIR")
    validation = luna42._phase_a_expectation(record)

    assert len(record["transfers"]) == 2
    assert record["transfers"][0]["model_b_payload"] == 0.4
    assert record["transfers"][1]["model_b_payload"] > 0.4
    assert record["transfers"][1]["model_b_payload"] == record["relay_receptions"][1]["payload"]
    assert validation["source_ordinary_emission_formula_matches"]
    assert validation["model_b_formula_matches"]
    assert validation["actual_input_oracle"]["matches_trace"]
    assert not validation["actual_input_oracle"]["predicted_crosses_threshold"]
    assert validation["provenance_reconciles"]
    assert validation["recurrence"]["passed"]
    assert validation["passed"]


def test_slowest_candidate_emits_one_signed_integration_mediated_relay_spike() -> None:
    positive = luna42._run_phase_a_fixture(0.0125, "NEAR_TRIPLE")
    negative = luna42._run_phase_a_fixture(0.0125, "NEGATIVE_NEAR_TRIPLE")
    positive_validation = luna42._phase_a_expectation(positive)
    negative_validation = luna42._phase_a_expectation(negative)

    assert len(positive["relay_canonical_emissions"]) == 1
    assert len(negative["relay_canonical_emissions"]) == 1
    assert positive_validation["emission_classification"] == ["integrated_discharge"]
    assert negative_validation["emission_classification"] == ["integrated_discharge"]
    assert positive["relay_canonical_emissions"][0]["payload"] > 0.0
    assert negative["relay_canonical_emissions"][0]["payload"] < 0.0
    assert math.isclose(
        positive["relay_canonical_emissions"][0]["payload"],
        -negative["relay_canonical_emissions"][0]["payload"],
        abs_tol=1e-12,
    )
    assert positive_validation["recurrence"]["passed"]
    assert negative_validation["recurrence"]["passed"]
    assert positive_validation["ordinary_emission_payload"]["matches"]
    assert negative_validation["ordinary_emission_payload"]["matches"]
    assert positive_validation["actual_input_oracle"]["predicted_crosses_threshold"]
    assert negative_validation["actual_input_oracle"]["predicted_crosses_threshold"]
    assert positive_validation["passed"]
    assert negative_validation["passed"]


def test_disabled_control_uses_public_zero_probe_without_integration() -> None:
    record = luna42._run_phase_a_fixture(0.0125, "INTEGRATION_DISABLED")
    validation = luna42._phase_a_expectation(record)

    assert not record["integration_enabled"]
    assert record["relay_integration_trace"] == []
    assert record["neutral_probe"]["event_count"] == 1
    assert record["neutral_probe"]["z_after_probe"] is None
    assert record["relay_canonical_emissions"] == []
    assert validation["provenance_reconciles"]
    assert validation["recurrence"]["passed"]
    assert validation["passed"]


def test_point_batches_preserve_equal_timestamp_order_and_signed_values() -> None:
    class Point:
        def __init__(self, timestamp: float, x: float, y: float) -> None:
            self.timestamp = timestamp
            self.x = x
            self.y = y

    batches = luna42._point_batches(
        (
            Point(0.0, 0.25, -0.5),
            Point(0.0, 0.5, 0.125),
            Point(1.0, -0.75, 0.25),
        )
    )

    assert batches == (((0.0, -0.25), (0.0, 0.625)), ((1.0, -0.5),))


def test_run_experiment_records_non_null_provenance_and_freeze_before_phase_b(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[float] = []

    def fake_phase_b_once(selected_decay_rate_z: float) -> dict[str, object]:
        calls.append(selected_decay_rate_z)
        return {
            "summary": {
                "CALIBRATED": {"all_causality_checks_pass": True, "relay_integrated_emissions": 1},
                "DEFAULT": {"all_causality_checks_pass": True, "relay_integrated_emissions": 0},
                "DISABLED": {"all_causality_checks_pass": True, "relay_integrated_emissions": 0},
            }
        }

    monkeypatch.setattr(luna42, "_phase_b_once", fake_phase_b_once)
    results, summary = luna42.run_experiment(
        output_directory=tmp_path,
        execution_provenance={
            "authorization_revision": luna42.START_REVISION,
            "execution_revision": "runner-commit",
            "origin_main_revision": "runner-commit",
            "branch": "main",
            "runner_sha256": "abc123",
            "python": "3.11-test",
            "platform": "test-platform",
            "float_info": {"epsilon": 1.0},
        },
        validate_execution_environment=False,
    )

    assert calls == [0.0125, 0.0125]
    assert results["provenance"]["execution_revision"] == "runner-commit"
    assert summary["provenance"]["execution_revision"] == "runner-commit"
    freeze_artifact = json.loads((tmp_path / "phase_a_freeze.json").read_text(encoding="utf-8"))
    config_artifact = json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))
    assert freeze_artifact["recorded_before_phase_b_stream_creation"] is True
    assert freeze_artifact["provenance"]["execution_revision"] == "runner-commit"
    assert config_artifact["provenance"]["config_digest"] == results["provenance"]["config_digest"]


def test_phase_b_once_builds_paired_input_digests_for_all_arms() -> None:
    phase_b = luna42._phase_b_once(0.0125)

    assert phase_b["paired_input_invariance"]
    assert set(phase_b["input_digests"]) == {"CALIBRATED", "DEFAULT", "DISABLED"}
    assert all(set(seed_map) == {"0", "1", "2", "3", "4"} for seed_map in phase_b["input_digests"].values())
