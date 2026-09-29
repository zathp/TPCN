import math

import pytest

from tpcn.temporal_crossover import CrossoverConfig, frozen_crossover, run_condition, run_suite


def test_frozen_crossover_matches_implemented_equation() -> None:
    config = CrossoverConfig()
    derivation = frozen_crossover(config)
    left = derivation["left_residual_at_execution_decay"] * math.exp(
        -derivation["scoring_decay_crossover"] * config.observation_intervals[0]
    )
    right = derivation["right_residual_at_execution_decay"] * math.exp(
        -derivation["scoring_decay_crossover"] * config.observation_intervals[1]
    )
    assert left == pytest.approx(right)


def test_runtime_local_decay_crosses_one_slot_structural_choice() -> None:
    low = run_condition("decay_low")
    high = run_condition("decay_high")
    assert low["complete"] and high["complete"]
    assert len(low["records"]) == len(high["records"]) == 2
    assert low["ranked_candidates"] == ("right", "left")
    assert high["ranked_candidates"] == ("left", "right")
    assert low["admission"]["selected_candidate"] == "right"
    assert high["admission"]["selected_candidate"] == "left"
    assert len(low["admission"]["final_edges"]) == 1
    assert low["admission"]["rejected_candidates"][0]["reason"] == "edge_capacity"


def test_candidate_records_are_runtime_local_and_bounded() -> None:
    result = run_condition("decay_high")
    assert {record["evidence_source"] for record in result["records"]} == {"runtime_local_decay_score"}
    assert all(record["originating_observation"]["source"].startswith("stimulus-") for record in result["records"])
    assert all(record["followup_observation"]["source"] == "target" for record in result["records"])
    assert all(record["decision_timestamp"] <= result["decision_timestamp"] for record in result["records"])
    assert result["runtime"]["execution"]["processed_event_count"] <= 8
    assert result["runtime"]["execution"]["pending_event_count"] == 0


def test_future_probe_cannot_change_frozen_candidate_evidence() -> None:
    current = run_condition("decay_high", future_probe=False)
    future = run_condition("decay_high", future_probe=True)
    assert current["ranked_candidates"] == future["ranked_candidates"]
    assert current["candidate_scores"] == future["candidate_scores"]
    assert current["admission"]["final_edges"] == future["admission"]["final_edges"]


def test_controls_and_one_slot_accounting() -> None:
    reversed_result = run_condition("reversed")
    shuffled_result = run_condition("shuffled")
    fixed_result = run_condition("fixed")
    uniform_result = run_condition("uniform")
    neutral_result = run_condition("neutral")
    assert reversed_result["records"] == ()
    assert shuffled_result["records"] == ()
    assert fixed_result["admission"]["selected_candidate"] is None
    assert len(fixed_result["admission"]["final_edges"]) == 0
    assert uniform_result["admission"]["selected_candidate"] == "right"
    assert neutral_result["admission"]["selected_candidate"] == "right"
    assert uniform_result["admission"]["capacity_before"]["remaining_slots"] == 1


def test_mirror_and_relabel_follow_evidence_not_identifier_order() -> None:
    relabeled = run_condition(
        "decay_high", config=CrossoverConfig(candidate_ids=("z_candidate", "a_candidate")),
    )
    mirrored = run_condition("decay_high", mirror=True)
    assert relabeled["admission"]["selected_candidate"] == "z_candidate"
    assert mirrored["records"][0]["candidate_role"] in {"left", "right"}
    assert mirrored["admission"]["selected_role"] == "left"
    assert mirrored["admission"]["selected_candidate"] == "right"


def test_tie_is_explicit_and_replay_is_deterministic() -> None:
    first = run_condition("decay_near")
    second = run_condition("decay_near")
    assert first == second
    assert first["ranked_candidates"] == ("left", "right")
    assert first["admission"]["tie_rule"] == "score descending, then candidate identifier ascending"


def test_suite_contains_required_control_categories() -> None:
    results = run_suite()
    assert {result["condition"] for result in results} == {
        "decay_low", "decay_high", "decay_near", "ordinary", "reversed", "shuffled",
        "random", "score_shuffled", "fixed", "uniform", "neutral",
    }