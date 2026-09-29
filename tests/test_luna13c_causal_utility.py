from tpcn.causal_utility import UtilityConfig, run_experiment
from tpcn.temporal_crossover import run_condition


def test_required_intervention_matrix_has_expected_external_pattern():
    artifact = run_experiment()
    results = artifact["results"]
    assert set(results) == {
        "learned_present", "targeted_removed", "restored", "sham",
        "irrelevant_removed", "fixed_useful", "fixed_topology", "random_growth",
    }
    assert results["learned_present"]["primary_metric_value"] == 1.0
    assert results["targeted_removed"]["primary_metric_value"] == 0.5
    assert results["restored"]["primary_metric_value"] == 1.0
    assert results["sham"]["primary_metric_value"] == 1.0
    assert results["irrelevant_removed"]["primary_metric_value"] == 1.0
    assert results["fixed_useful"]["primary_metric_value"] == 1.0
    assert results["fixed_topology"]["primary_metric_value"] == 0.5


def test_learning_is_luna13b_local_and_restoration_is_exact():
    artifact = run_experiment()
    learning = artifact["structural_learning"]
    assert learning["learned_edge"] == ("right", "target", 1.0)
    assert {record["evidence_source"] for record in learning["candidate_records"]} == {"runtime_local_decay_score"}
    results = artifact["results"]
    assert results["learned_present"]["graph_fingerprint"] == results["restored"]["graph_fingerprint"]
    assert results["learned_present"]["graph_edges"] == results["restored"]["graph_edges"]
    assert results["targeted_removed"]["graph_fingerprint"] != results["learned_present"]["graph_fingerprint"]


def test_all_conditions_are_paired_and_complete_with_frozen_target():
    artifact = run_experiment(config=UtilityConfig(random_seed=1))
    assert artifact["task"]["target_independent_of_topology"]
    targets = {
        case["example_id"]: case["fixed_external_target"]
        for case in artifact["results"]["learned_present"]["case_results"]
    }
    for result in artifact["results"].values():
        assert result["checkpoint_fingerprint"] == artifact["structural_learning"]["frozen_checkpoint_fingerprint"]
        assert result["all_completed"]
        assert all(
            case["fixed_external_target"] == targets[case["example_id"]]
            for case in result["case_results"]
        )
        assert all(case["completion"]["termination_reason"] == "completed" for case in result["case_results"])


def test_label_relabeling_does_not_change_learning_or_neural_execution():
    first = run_experiment()
    second = run_experiment()
    assert first["structural_learning"] == second["structural_learning"]
    assert first["results"] == second["results"]


def test_future_probe_does_not_change_the_learned_edge_or_evidence():
    current = run_condition("decay_low", future_probe=False)
    future = run_condition("decay_low", future_probe=True)
    def semantic(record):
        return {
            key: value
            for key, value in record.items()
            if key not in {"originating_observation", "followup_observation"}
        }
    assert tuple(semantic(record) for record in current["records"]) == tuple(
        semantic(record) for record in future["records"]
    )
    assert tuple(
        (record["originating_observation"]["timestamp"], record["followup_observation"]["timestamp"])
        for record in current["records"]
    ) == tuple(
        (record["originating_observation"]["timestamp"], record["followup_observation"]["timestamp"])
        for record in future["records"]
    )
    assert current["admission"]["final_edges"] == future["admission"]["final_edges"]