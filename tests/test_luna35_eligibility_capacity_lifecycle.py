from __future__ import annotations

import json

import pytest

from run_luna35_eligibility_capacity_lifecycle import (
    EXECUTION_BASELINE,
    _observe_fixtures,
    run_experiment,
)


@pytest.fixture(scope="module")
def observations() -> dict:
    return _observe_fixtures()


def test_capacity_reproducer_records_every_eligibility_transition(observations: dict) -> None:
    assert set(observations) == {"capacity_reproducer", "lifecycle_control"}
    primary = observations["capacity_reproducer"]

    assert primary["fixture_id"] == "c00-004"
    assert primary["point_count"] == 20
    assert primary["per_node_capacity"] == {"source": 16, "destination": 16}
    assert primary["aggregate_capacity"] == 32
    assert primary["outcome"] == "capacity_rejected"
    assert primary["occupancy_accounting"] == {
        "initial_source_occupancy": 0,
        "successful_creations": 16,
        "removals_before_stop": 0,
        "final_source_occupancy": 16,
        "equation_reconciles": True,
    }
    assert [
        (event["creation_sequence_number"], event["occupancy_before"], event["occupancy_after"])
        for event in primary["eligibility_activity_events"][:16]
    ] == [(index, index - 1, index) for index in range(1, 17)]

    failure = primary["capacity_failure"]
    assert failure["input_point_index"] == 19
    assert failure["source_neuron_processed_event_count"] == 59
    assert failure["runtime_processed_event_count"] == 59
    assert failure["canonical_emission_sequence"] == 17
    assert failure["canonical_emission_id"] == "source:excursion:17"
    assert failure["creation_sequence_number"] == 17
    assert failure["occupancy_before_attempt"] == 16
    assert failure["occupancy_after_decay_before_rejection"] == 16
    assert len(failure["resident_traces_after_decay_before_insertion"]) == 16
    assert failure["exception"] == (
        "EligibilityCapacityError: eligibility trace capacity reached"
    )
    resident = failure["resident_traces_after_decay_before_insertion"]
    assert [trace["trace_id"] for trace in resident] == [
        f"luna35:c00-004:source:excursion:{index}" for index in range(1, 17)
    ]
    assert all(trace["credit"] == 0.0 for trace in resident)
    assert all(trace["last_timestamp"] == failure["timestamp"] for trace in resident)


def test_predictor_expiry_reward_and_character_reset_are_distinct(observations: dict) -> None:
    primary = observations["capacity_reproducer"]
    assert len(primary["predictor_creation_events"]) == 17
    assert len(primary["predictor_observations"]) == 19
    assert all(item["status"] == "unmatched" for item in primary["predictor_observations"])
    assert len(primary["predictor_expirations"]) == 16
    assert all(item["matching_eligibility_entry_count"] == 1 for item in primary["predictor_expirations"])
    assert all(
        item["eligibility_after_predictor_expiration"][0]["status"] == "resident"
        for item in primary["predictor_expirations"]
    )
    assert primary["eligibility_retirements"] == []
    assert primary["ledger_signals"] == []
    assert primary["end_character_reached"] is False
    assert primary["neutral_end_character_reward_reached_ledger"] is False

    control = observations["lifecycle_control"]
    assert control["input_point_count"] == 1
    assert control["end_character_result"]["emission_count"] == 1
    assert control["creation_count"] == 1
    assert control["removal_count_before_boundary"] == 0
    assert len(control["ledger_signals"]) == 1
    reward = control["ledger_signals"][0]
    assert reward["payload"] == {
        "kind": "reward",
        "message_id": "neutral-luna35-lifecycle-0",
        "reward": 0.0,
        "trace_id": "luna35:luna35-lifecycle-0:source:excursion:1",
        "prediction_id": None,
    }
    assert reward["attribution"]["status"] == "matched"
    assert reward["occupancy_before"] == reward["occupancy_after"] == 1
    assert control["ledger_state_immediately_before_end_character_destruction"]["source"]["traces"][0][
        "trace_id"
    ] == reward["payload"]["trace_id"]
    assert control["ledger_state_immediately_after_end_character_destruction"] == {
        "runtime_ledger_ids": [],
        "occupancy_by_node": {"source": 0, "destination": 0},
        "trace_references_released": 1,
        "predictor_released": True,
    }
    assert control["next_character_has_fresh_ledger_ids"] is True
    assert control["next_character_ledgers_empty"] is True
    assert control["occupancy_accounting"]["equation_reconciles"] is True


def test_replay_is_deterministic_and_writes_only_authorized_artifacts(tmp_path) -> None:
    results, summary = run_experiment(tmp_path)

    assert results["execution_baseline"] == EXECUTION_BASELINE
    assert set(results["fixed_fixtures"]) == {"capacity_reproducer", "lifecycle_control"}
    assert results["deterministic_replay"]["digests_match"] is True
    assert results["deterministic_replay"]["replayed_exactly_two_fixed_fixtures"] is True
    assert summary["classification"] == "EXPECTED LIFECYCLE CONFIRMED"
    assert summary["production_defect_established"] is False
    assert summary["capacity_reproducer"]["successful_eligibility_creations"] == 16
    assert summary["capacity_reproducer"]["source_occupancy_at_failure"] == 16
    assert summary["lifecycle_control"]["occupancy_equation_reconciles"] is True
    assert {path.name for path in tmp_path.iterdir()} == {
        "config.json",
        "results.json",
        "summary.json",
    }
    saved = json.loads((tmp_path / "results.json").read_text(encoding="utf-8"))
    assert saved["deterministic_replay"]["first_observation_digest"] == (
        saved["deterministic_replay"]["replay_observation_digest"]
    )
