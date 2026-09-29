import pytest
import json

from tpcn.temporal_direction import (
    CANDIDATE_ENDPOINTS,
    compare_normalized_replay,
    DECAY_RATES,
    POLICIES,
    run_temporal_direction,
    run_temporal_direction_suite,
    write_artifacts,
)


def test_policy_matrix_and_candidate_exposure_are_bounded_and_matched() -> None:
    results = run_temporal_direction_suite(seeds=(0, 1))
    assert len(results) == 6 * 2 * len(DECAY_RATES)
    assert {result.policy for result in results} == set(POLICIES)
    assert {result.candidates_exposed for result in results} == {len(CANDIDATE_ENDPOINTS)}
    assert {result.candidates_considered for result in results} == {15}
    assert {result.attempts for result in results} == {3}


def test_current_matches_existing_temporal_direction_and_reversed_changes_orientation() -> None:
    current = run_temporal_direction("current", seed=0, decay_rate=0.5)
    reversed_result = run_temporal_direction("reversed", seed=0, decay_rate=0.5)
    assert current.direction == "current"
    assert current.accepted_edges[0] == ("source", "target")
    assert reversed_result.direction == "reversed"
    assert ("target", "source") in reversed_result.accepted_edges
    assert ("source", "target") not in reversed_result.accepted_edges


def test_decay_uses_intrinsic_parameter_and_local_relative_setting() -> None:
    weak = run_temporal_direction("decay", seed=0, decay_rate=0.25)
    strong = run_temporal_direction("decay", seed=0, decay_rate=1.0)
    assert weak.decay_mode == "intrinsic_decay_relative"
    assert strong.decay_mode == "intrinsic_decay_relative"
    assert weak.decay_context and strong.decay_context
    assert {record["decay_rate"] for record in weak.decay_context} == {0.25}
    assert {record["decay_rate"] for record in strong.decay_context} == {1.0}
    assert weak.candidate_scores != strong.candidate_scores


def test_static_and_used_shortcuts_require_distinct_evidence() -> None:
    current = run_temporal_direction("current", seed=0, decay_rate=0.5)
    fixed = run_temporal_direction("fixed", seed=0, decay_rate=0.5)
    assert current.static_shortcut_count == 1
    assert current.used_shortcut_count == 1
    assert current.causal_delay_delta == pytest.approx(2.25)
    assert current.new_route_traffic["POST_MUTATION"] > 0
    assert fixed.static_shortcut_count == 0
    assert fixed.used_shortcut_count == 0
    assert fixed.static_shortcut_yield is None


def test_phase_scoped_traffic_and_removal_intervention_are_measured() -> None:
    result = run_temporal_direction("current", seed=2, decay_rate=0.5)
    assert result.old_route_traffic == {
        "PRE_MUTATION": 2, "POST_MUTATION": 2, "POST_REMOVAL": 2,
    }
    assert result.new_route_traffic == {"POST_MUTATION": 2}
    assert result.causal_intervention is not None
    assert result.causal_intervention["changed"]
    assert result.causal_intervention["present_trace"] != result.causal_intervention["removed_trace"]


def test_same_seed_is_deterministic_and_raw_observer_is_edge_2() -> None:
    first = run_temporal_direction("decay", seed=3, decay_rate=0.5)
    second = run_temporal_direction("decay", seed=3, decay_rate=0.5)
    assert first == second
    assert first.raw_12m["schema_version"] == "TPCN-EDGE-2"
    assert any(item["kind"] == "edge_created" for item in first.raw_12m["lifecycle"])
    assert any(item["kind"] == "decay_context" for item in first.raw_12m["lifecycle"])


def test_labels_and_global_topology_are_not_policy_inputs() -> None:
    first = run_temporal_direction("current", seed=4, decay_rate=0.5)
    second = run_temporal_direction("current", seed=4, decay_rate=0.5)
    assert first.candidate_scores == second.candidate_scores
    assert first.accepted_edges == second.accepted_edges
    assert all("label" not in item for item in first.raw_12m["lifecycle"])


def test_decay_records_candidate_local_intervals_and_changes_competing_rank() -> None:
    current = run_temporal_direction("current", seed=0, decay_rate=0.5)
    decay = run_temporal_direction("decay", seed=0, decay_rate=0.5)
    intervals = {record["delta_t"] for record in decay.candidate_records}
    assert len(intervals) > 2
    assert all(record["delta_t"] == pytest.approx(
        record["destination_timestamp"] - record["source_timestamp"]
    ) for record in decay.candidate_records)
    current_ranks = {tuple((record["source"], record["destination"])): record["rank"]
                     for record in current.candidate_records}
    decay_ranks = {tuple((record["source"], record["destination"])): record["rank"]
                   for record in decay.candidate_records}
    assert current_ranks != decay_ranks


def test_phase_labels_alone_do_not_count_as_causal_change() -> None:
    evidence = {"normalized": {"trace": (("source", 0.0),), "target_arrivals": (),
                                "target_states": (), "prediction_loss": 0.0,
                                "prediction_errors": 0}}
    assert compare_normalized_replay(evidence, evidence)["changed"] is False


def test_yield_denominator_includes_non_shortcut_mutations() -> None:
    result = run_temporal_direction("current", seed=0, decay_rate=0.5)
    assert result.accepted_mutation_count == len(result.accepted_mutations) == 2
    assert result.static_shortcut_count == 1
    assert result.static_shortcut_yield == pytest.approx(0.5)
    assert result.used_shortcut_yield == pytest.approx(0.5)
    assert any(not mutation["static_shortcut"] for mutation in result.accepted_mutations)


def test_zero_acceptance_summary_and_per_record_baseline_are_preserved(tmp_path) -> None:
    result = run_temporal_direction("fixed", seed=0, decay_rate=0.5, baseline_revision="test-baseline")
    assert result.baseline_revision == "test-baseline"
    write_artifacts((result,), str(tmp_path), baseline_revision="test-baseline")
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert summary["fixed"]["static_shortcut_yield"] is None
    assert summary["fixed"]["used_shortcut_yield"] is None
