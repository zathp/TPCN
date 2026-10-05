from __future__ import annotations

import math

import run_luna41_acp0008_temporal_calibration as luna41


def test_phase_a_configuration_contains_only_predeclared_candidates() -> None:
    config = luna41.experiment_config()

    assert config["candidate_order"] == [0.1, 0.05, 0.025, 0.0125]
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
    assert config["phase_b"]["runtime"]["eligibility_capacity_per_ledger"] == 1024


def test_isolated_routed_input_matches_normalized_amplitude_and_leaks() -> None:
    record = luna41._run_phase_a_fixture(0.1, "ISOLATED")
    validation = luna41._phase_a_expectation(record)

    assert len(record["source_canonical_emissions"]) == 1
    assert len(record["transfers"]) == 1
    assert math.isclose(record["transfers"][0]["model_b_payload"], 0.4, abs_tol=1e-12)
    assert record["relay_integration_trace"][0]["z_after_input"] == 0.4
    assert record["neutral_probe"]["event_count"] == 1
    assert abs(record["neutral_probe"]["z_after_probe"]) < 1e-4
    assert validation["recurrence"]["passed"]
    assert validation["passed"]


def test_near_pair_records_source_residual_payload_deviation() -> None:
    record = luna41._run_phase_a_fixture(0.1, "NEAR_PAIR")
    validation = luna41._phase_a_expectation(record)

    assert len(record["transfers"]) == 2
    assert record["transfers"][0]["model_b_payload"] == 0.4
    assert record["transfers"][1]["model_b_payload"] > 0.4
    assert validation["maximum_model_b_payload_error"] > luna41.ROUTE_PAYLOAD_TOLERANCE
    assert not validation["all_source_emissions_and_model_b_payloads_match"]
    assert validation["recurrence"]["passed"]
    assert not validation["passed"]


def test_slowest_candidate_emits_one_signed_integration_mediated_relay_spike() -> None:
    positive = luna41._run_phase_a_fixture(0.0125, "NEAR_TRIPLE")
    negative = luna41._run_phase_a_fixture(0.0125, "NEGATIVE_NEAR_TRIPLE")
    positive_validation = luna41._phase_a_expectation(positive)
    negative_validation = luna41._phase_a_expectation(negative)

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


def test_disabled_control_uses_public_zero_probe_without_integration() -> None:
    record = luna41._run_phase_a_fixture(0.0125, "INTEGRATION_DISABLED")
    validation = luna41._phase_a_expectation(record)

    assert not record["integration_enabled"]
    assert record["relay_integration_trace"] == []
    assert record["neutral_probe"]["event_count"] == 1
    assert record["neutral_probe"]["z_after_probe"] is None
    assert record["relay_canonical_emissions"] == []
    assert not validation["all_source_emissions_and_model_b_payloads_match"]
    assert not validation["passed"]


def test_point_batches_preserve_equal_timestamp_order_and_signed_values() -> None:
    class Point:
        def __init__(self, timestamp: float, x: float, y: float) -> None:
            self.timestamp = timestamp
            self.x = x
            self.y = y

    batches = luna41._point_batches(
        (
            Point(0.0, 0.25, -0.5),
            Point(0.0, 0.5, 0.125),
            Point(1.0, -0.75, 0.25),
        )
    )

    assert batches == (((0.0, -0.25), (0.0, 0.625)), ((1.0, -0.5),))
