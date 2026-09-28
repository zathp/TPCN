from tpcn.temporal_efficacy import (
    TemporalEfficacyConfig,
    run_temporal_efficacy,
    run_temporal_efficacy_suite,
)


def test_all_policies_share_identical_finite_bounds_and_temporal_growth_forms_fanin():
    config = TemporalEfficacyConfig()
    results = [run_temporal_efficacy(policy, seed=3, config=config) for policy in
               ("fixed", "baseline", "random", "temporal", "reversed")]

    assert all(result.metrics.edge_capacity == config.edge_capacity for result in results)
    assert all(result.metrics.edge_count <= config.edge_capacity for result in results)
    assert all(max(value for _, value in result.metrics.fan_in_distribution) <= config.fan_in_limit
               for result in results)
    temporal = next(result for result in results if result.metrics.policy == "temporal")
    assert temporal.metrics.convergent_fan_in_motifs == 1
    assert {edge[:2] for edge in temporal.metrics.topology_edges} == {("a", "target"), ("b", "target")}


def test_temporal_growth_is_deterministic_and_reversed_timing_destroys_candidates():
    first = run_temporal_efficacy("temporal", seed=11)
    second = run_temporal_efficacy("temporal", seed=11)
    reversed_result = run_temporal_efficacy("reversed", seed=11)

    assert first == second
    assert first.metrics.replay_digest == second.metrics.replay_digest
    assert reversed_result.metrics.candidate_count == 0
    assert reversed_result.metrics.accepted_additions == 0


def test_learned_edges_change_actual_routed_computation_and_intervention_removes_effect():
    temporal = run_temporal_efficacy("temporal", seed=0)
    fixed = run_temporal_efficacy("fixed", seed=0)

    assert temporal.metrics.event_count > fixed.metrics.event_count
    assert temporal.metrics.class_separation > fixed.metrics.class_separation
    assert temporal.causal_intervention is not None
    assert temporal.causal_intervention.changed
    assert temporal.causal_intervention.removed_event_count < temporal.causal_intervention.present_event_count


def test_seeded_random_control_uses_same_candidate_budget_without_label_input():
    first = run_temporal_efficacy("random", seed=5)
    second = run_temporal_efficacy("random", seed=5)
    suite = run_temporal_efficacy_suite(seeds=(5,))

    assert first.metrics.candidate_proposals == second.metrics.candidate_proposals == 2
    assert first.metrics.candidate_space_size == second.metrics.candidate_space_size == 6
    assert first.metrics.topology_edges == second.metrics.topology_edges
    assert len(suite) == 5
    assert all(result.metrics.prediction_loss >= 0.0 for result in suite)