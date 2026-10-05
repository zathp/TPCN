from __future__ import annotations

from unittest import mock

import pytest

import run_luna39_acp0008_propagation_emission_diagnostic as luna39
import run_luna43_acp0008_destination_integration_mechanism as luna43


def test_unauthorized_execution_revision_is_a_stop_condition(monkeypatch) -> None:
    def git_output(*args: str) -> str:
        if args[0] == "branch":
            return luna43.BRANCH
        if args[0] == "rev-parse":
            if args[1] == "origin/main":
                return luna43.AUTHORIZATION_BASELINE
            return "execution-revision"
        if args[0] == "status":
            return ""
        if args[0] == "merge-base":
            return "different-ancestor"
        raise AssertionError(args)

    monkeypatch.setattr(luna43, "_git_output", git_output)

    with pytest.raises(luna43.StopCondition, match="authorization revision is not an ancestor"):
        luna43._collect_provenance()


def test_runtime_trace_record_preserves_emission_tuple_layout() -> None:
    emission = (
        1.5, "relay", "relay", "excursion_emission", 0.25,
        "event-id", 17, "episode-id", "lineage-id", ("root",), True,
    )

    assert luna43._runtime_trace_record(emission) == {
        "timestamp": 1.5,
        "source": "relay",
        "destination": "relay",
        "event_type": "excursion_emission",
        "payload": 0.25,
        "event_id": "event-id",
        "sequence": 17,
        "episode_id": "episode-id",
        "lineage_id": "lineage-id",
        "causal_roots": ["root"],
        "roots_truncated": True,
    }


def test_replay_blocker_preserves_successful_initial_run(tmp_path, monkeypatch) -> None:
    first_run = {"result": "initial run"}
    replay_error = luna43.StopCondition("replay stopped", {"reason": "replay detail"})
    monkeypatch.setattr(luna43, "_phase_once", mock.Mock(side_effect=[first_run, replay_error]))

    results, _ = luna43.run_experiment(
        tmp_path,
        execution_provenance={
            "execution_revision": "test-revision",
            "execution_repo_revision": "test-revision",
        },
        validate_execution_environment=False,
    )

    assert results["first_run"] == first_run
    assert results["stop_reason"] == "replay stopped"
    assert results["replay_run_digest"] == {
        "initial_digest": luna43._digest(first_run),
        "replay_digest": None,
        "equal": False,
        "not_run_after_blocker": False,
        "replay_blocked": {"reason": "replay stopped", "detail": {"reason": "replay detail"}},
    }


def test_initial_run_blocker_marks_replay_not_run(tmp_path, monkeypatch) -> None:
    initial_error = luna43.StopCondition("initial stopped", {"reason": "initial detail"})
    monkeypatch.setattr(luna43, "_phase_once", mock.Mock(side_effect=initial_error))

    results, _ = luna43.run_experiment(
        tmp_path,
        execution_provenance={
            "execution_revision": "test-revision",
            "execution_repo_revision": "test-revision",
        },
        validate_execution_environment=False,
    )

    assert results["first_run"] == {
        "blocked": {"reason": "initial stopped", "detail": {"reason": "initial detail"}}
    }
    assert results["replay_run_digest"]["not_run_after_blocker"] is True
    assert results["replay_run_digest"]["initial_digest"] is None


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
