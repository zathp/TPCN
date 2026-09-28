import pytest

from tpcn.temporal_capacity import (
    CANDIDATE_ENDPOINTS,
    CapacityPressureConfig,
    LONG_PATH,
    run_temporal_capacity,
    run_temporal_capacity_suite,
)


POLICIES = ("fixed", "baseline", "random", "temporal", "reversed")


def test_adaptive_conditions_receive_equal_candidate_exposure_and_bounds() -> None:
    config = CapacityPressureConfig()
    results = [run_temporal_capacity(policy, seed=3, config=config) for policy in POLICIES]
    adaptive = results[1:]

    assert all(result.metrics.candidate_set == CANDIDATE_ENDPOINTS for result in results)
    assert {result.metrics.candidates_exposed for result in adaptive} == {len(CANDIDATE_ENDPOINTS)}
    assert {result.metrics.candidates_considered for result in adaptive} == {9}
    assert {result.metrics.growth_attempts for result in adaptive} == {config.max_growth_attempts}
    assert all(result.metrics.edge_count <= config.edge_capacity for result in results)
    assert all(max(value for _, value in result.metrics.fan_in_distribution) <= config.fan_in_limit
               for result in results)
    assert all(max(value for _, value in result.metrics.fan_out_distribution) <= config.fan_out_limit
               for result in results)


def test_initial_long_path_is_functional_with_explicit_finite_delays() -> None:
    result = run_temporal_capacity("fixed", seed=0)
    assert tuple(edge[:2] for edge in result.metrics.topology_before) == LONG_PATH
    assert result.metrics.shortest_path_hops_before == 3
    assert result.metrics.shortest_path_delay_before == pytest.approx(3.0)
    assert result.metrics.before.path_hops == (3, 3)
    assert result.metrics.before.path_delays == pytest.approx((3.0, 3.0))
    assert result.metrics.before.routed_event_count == 6


def test_temporal_growth_forms_real_shortcut_under_capacity_pressure() -> None:
    result = run_temporal_capacity("temporal", seed=0)
    metrics = result.metrics

    assert metrics.temporal_preference
    assert metrics.shortcut_selected
    assert metrics.shortest_path_hops_after == 1
    assert metrics.shortest_path_delay_after == pytest.approx(0.75)
    assert metrics.path_shortening == pytest.approx(2.25)
    assert metrics.rejection_reasons == (("fan_in_full", 1), ("fan_out_full", 1))
    assert metrics.accepted_additions == 1
    assert metrics.shortcut_used
    assert any(arrival[2] == 1 and arrival[1] == pytest.approx(0.75) for arrival in metrics.after.target_arrivals)


def test_shortcut_removal_changes_actual_routed_computation_and_state() -> None:
    result = run_temporal_capacity("temporal", seed=1)
    intervention = result.causal_intervention

    assert intervention is not None
    assert intervention.edge == ("source", "target")
    assert intervention.changed
    assert intervention.present.routed_event_count > intervention.removed.routed_event_count
    assert intervention.present.event_count > intervention.removed.event_count
    assert intervention.present.target_states != intervention.removed.target_states
    assert intervention.removed.path_hops == (3, 3)
    assert intervention.removed.path_delays == pytest.approx((3.0, 3.0))


def test_controls_and_reversed_timing_do_not_get_temporal_shortcut_preference() -> None:
    baseline = run_temporal_capacity("baseline", seed=0)
    random_result = run_temporal_capacity("random", seed=0)
    reversed_result = run_temporal_capacity("reversed", seed=0)
    temporal = run_temporal_capacity("temporal", seed=0)

    assert not baseline.metrics.shortcut_selected
    assert not reversed_result.metrics.shortcut_selected
    assert temporal.metrics.shortcut_selected
    assert reversed_result.metrics.observation_count == temporal.metrics.observation_count
    assert "fan_out_full" in dict(reversed_result.metrics.rejection_reasons)
    assert random_result.metrics.candidates_exposed == temporal.metrics.candidates_exposed


def test_same_seed_reproduces_selection_topology_and_replay() -> None:
    first = run_temporal_capacity("random", seed=7)
    second = run_temporal_capacity("random", seed=7)
    assert first == second
    assert first.metrics.after.digest == second.metrics.after.digest


def test_suite_retains_all_declared_seeds_and_records_pressure() -> None:
    results = run_temporal_capacity_suite(seeds=(0, 1, 2))
    assert len(results) == 15
    assert {result.metrics.seed for result in results} == {0, 1, 2}
    assert all(result.metrics.rejected_mutations >= 0 for result in results)
    assert any(result.metrics.rejected_mutations > 0 for result in results)