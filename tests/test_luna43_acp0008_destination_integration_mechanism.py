from __future__ import annotations

import run_luna39_acp0008_propagation_emission_diagnostic as luna39
import run_luna43_acp0008_destination_integration_mechanism as luna43


def test_frozen_config_has_only_the_two_fixed_model_b_hops() -> None:
    config = luna43.experiment_config()

    assert config["authorization_revision"] == luna43.AUTHORIZATION_REVISION
    assert config["node_configuration"]["relay"]["integration"]["decay_rate_z"] == 0.0125
    assert config["node_configuration"]["destination_by_arm"]["DESTINATION_DISABLED"]["integration"] is None
    assert config["node_configuration"]["destination_by_arm"]["DESTINATION_DEFAULT"]["integration"]["decay_rate_z"] == 0.1
    assert config["node_configuration"]["destination_by_arm"]["DESTINATION_CALIBRATED"]["integration"]["decay_rate_z"] == 0.0125
    assert config["topology"]["edges"] == list(luna43.EDGE_LIST)
    assert not any(
        edge["source"] == "source" and edge["destination"] == "destination"
        for edge in config["topology"]["edges"]
    )
    assert config["topology"]["growth_enabled"] is False
    assert config["runtime"]["queue_capacity"] == 128
    assert config["runtime"]["runtime_event_budget"] == 1024


def test_destination_receptions_retain_trace_complete_causal_identity() -> None:
    points = luna39.base._training_point_sequences(0)[1]
    record = luna43._run_character(
        arm="DESTINATION_CALIBRATED",
        seed=0,
        sequence_index=1,
        points=points,
    )

    assert len(record["destination_receptions"]) == 3
    assert len(record["relay_emissions"]) == 3
    assert len(record["relay_receptions"]) == record["counts"]["source_to_relay_transfers"]
    assert all(
        emission["causal_routed_reception"]["event_id"]
        == emission["causal_routed_reception"]["route_event"]["event_id"]
        and emission["causal_routed_reception"]["integration_trace"]["timestamp"]
        == emission["integration_trace"]["timestamp"]
        for emission in record["relay_emissions"]
    )
    for reception in record["destination_receptions"]:
        assert reception["prior_relay_canonical_event"]["event_id"] == reception["event_id"]
        assert reception["route_event"]["event_id"] == reception["event_id"]
        assert reception["route_event"]["payload"] == reception["payload"]
        assert reception["stream_identity"]["input_digest"] == record["input_digest"]
        assert reception["integration_trace"]["timestamp"] == reception["timestamp"]
        assert reception["stage_states"]["z_after_input"] is not None
        assert reception["stage_states"]["z_post_discharge"] is not None
    assert record["all_route_reconciliations_pass"]
    assert record["topology"] == record["topology_after_character"]


def test_destination_disabled_is_the_real_none_path_and_relay_is_historically_fixed() -> None:
    points = luna39.base._training_point_sequences(0)[1]
    disabled = luna43._run_character(
        arm="DESTINATION_DISABLED",
        seed=0,
        sequence_index=1,
        points=points,
    )
    calibrated = luna43._run_character(
        arm="DESTINATION_CALIBRATED",
        seed=0,
        sequence_index=1,
        points=points,
    )
    default = luna43._run_character(
        arm="DESTINATION_DEFAULT",
        seed=0,
        sequence_index=1,
        points=points,
    )
    historical = luna43._historical_results()

    assert disabled["node_integration_config"]["destination"] is None
    assert len(disabled["destination_receptions"]) == 3
    assert all(item["integration_trace"] is None for item in disabled["destination_receptions"])
    assert all(item["stage_states"]["z_post_discharge"] is None for item in disabled["destination_receptions"])
    assert disabled["relay_emissions"] == calibrated["relay_emissions"]
    assert disabled["relay_integration_trace"] == calibrated["relay_integration_trace"]
    assert disabled["input_digest"] == calibrated["input_digest"]
    assert luna43._relay_signature(disabled) == luna43._relay_signature(default)
    assert luna43._relay_signature(default) == luna43._relay_signature(calibrated)
    assert disabled["node_integration_config"]["source"] == default["node_integration_config"]["source"]
    assert disabled["node_integration_config"]["relay"] == calibrated["node_integration_config"]["relay"]
    assert all(
        luna43._historical_record_match(record, historical)["matches"]
        for record in (disabled, default, calibrated)
    )


def test_precursor_scan_reports_zero_without_destination_emissions() -> None:
    records = {
        arm: {
            str(seed): [{
                "seed": seed,
                "sequence_index": 0,
                "character_id": f"c{seed:02d}-000",
                "source_emissions": [],
                "relay_emissions": [],
                "destination_emissions": [],
            }]
            for seed in luna43.SEEDS
        }
        for arm in luna43.ARMS
    }

    scan = luna43._association_scan(records)

    for arm in luna43.ARMS:
        assert not scan["arms"][arm]["scan_performed"]
        assert scan["arms"][arm]["pair_counts"]["source_to_destination_missing_edge"] == 0
        assert scan["arms"][arm]["candidate_precursor_records"] == []
