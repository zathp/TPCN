from dataclasses import replace

from tpcn.finite_resource import FiniteResourceConfig, _pruning_eligibility, run_experiment


def test_useful_edge_and_external_baseline_complete() -> None:
    artifact = run_experiment()
    baseline = artifact["stages"]["A_baseline"]["reference"]
    assert artifact["structural_learning"]["learned_edge"] == ("right", "target", 1.0)
    assert baseline["useful_edge_present"]
    assert baseline["task_result"] == "2/2"
    assert baseline["completion_status"] == "completed"
    assert baseline["proxy_energy_unit"] == "activity-cost-proxy; uncalibrated"
    assert baseline["queue_peak"] >= 2


def test_distractors_and_capacity_pressure_record_reasons() -> None:
    artifact = run_experiment()
    distractor = artifact["stages"]["B_distractor"]
    assert distractor["useful_edge_present"]
    assert all(item["status"] == "grown" for item in distractor["mutations"])
    pressure = artifact["stages"]["C_capacity_pressure"]
    assert [item["capacity"] for item in pressure] == [4, 5, 6]
    assert any(item["failure_categories"]["capacity_failure"] for item in pressure)
    assert any(
        mutation["reason"] in {"edge_capacity", "fan_in_full", "fan_out_full"}
        for item in pressure
        for mutation in item["mutations"]
        if mutation["status"] == "full_capacity"
    )


def test_declared_pruning_removes_low_value_edges_and_frees_capacity() -> None:
    artifact = run_experiment()
    pruning = artifact["stages"]["D_pruning"]
    assert pruning["capacity_freed"] == 2
    assert {item["edge"]["source"] for item in pruning["mutations"]} == {"left", "noise"}
    assert pruning["useful_edge_present"]
    assert pruning["task_result"] == "2/2"


def test_post_pruning_growth_uses_normal_admission_without_replacement() -> None:
    artifact = run_experiment()
    post_pruning = artifact["stages"]["E_post_pruning_growth"]
    assert artifact["interpretation"]["replacement_authorized"] is False
    assert [item["status"] for item in post_pruning["mutations"]] == ["grown", "grown"]
    assert post_pruning["capacity_freed_before_growth"] == 2
    assert post_pruning["completion_status"] == "completed"


def test_fixed_and_random_controls_record_seed_provenance_and_resources() -> None:
    artifact = run_experiment(FiniteResourceConfig(random_seeds=(0, 1, 2, 3, 4)))
    fixed = artifact["controls"]["fixed_topology"]
    assert fixed["capacity_policy"] == "fixed-topology"
    random_results = artifact["controls"]["random_growth"]
    assert [result["seed"] for result in random_results] == [0, 1, 2, 3, 4]
    assert {result["selected_edge"][0] for result in random_results} == {"left", "right"}
    assert all(result["completion_status"] == "completed" for result in random_results)
    assert all(result["total_events"] >= 2 and result["proxy_energy"] >= 0.0 for result in random_results)


def test_budget_exhaustion_is_explicit_and_not_completed() -> None:
    artifact = run_experiment(FiniteResourceConfig(event_budget=1))
    baseline = artifact["stages"]["A_baseline"]["reference"]
    assert baseline["completion_status"] == "budget_exhausted"
    assert baseline["failure_categories"]["budget_exhaustion"]
    assert all(case["completion"]["termination_reason"] == "budget_exhausted" for case in baseline["case_results"])


def test_pruning_score_is_observed_use_and_thresholds_have_declared_boundaries() -> None:
    artifact = run_experiment()
    evidence = artifact["stages"]["D_pruning"]["pruning_evidence"]
    useful = next(item for item in evidence if item["edge"] == ("right", "target", 1.0))
    unused = next(item for item in evidence if item["edge"] == ("left", "noise", 4.0))
    assert useful["use_count"] == 4
    assert useful["pruning_score"] == useful["observed_utility"] == 4.0
    assert unused["use_count"] == 0
    assert unused["pruning_score"] == unused["observed_utility"] == 0.0

    base = {"inactivity_age": 0.0, "observed_utility": 0.0}
    assert _pruning_eligibility(base, FiniteResourceConfig(pruning_utility_threshold=0.1))[0]
    assert not _pruning_eligibility(base, FiniteResourceConfig(pruning_utility_threshold=0.0))[0]
    for age, expected in ((1.0, False), (2.0, True), (3.0, True)):
        evidence_case = {"inactivity_age": age, "observed_utility": 1.0}
        assert _pruning_eligibility(evidence_case, FiniteResourceConfig(pruning_inactivity_threshold=2))[0] is expected


def test_threshold_changes_can_change_pruning_decisions() -> None:
    no_utility_pruning = run_experiment(FiniteResourceConfig(pruning_inactivity_threshold=10, pruning_utility_threshold=0.0))
    utility_pruning = run_experiment(FiniteResourceConfig(pruning_inactivity_threshold=10, pruning_utility_threshold=0.1))
    assert no_utility_pruning["stages"]["D_pruning"]["mutations"] == ()
    assert len(utility_pruning["stages"]["D_pruning"]["mutations"]) == 2


def test_relabeling_and_mirrored_roles_follow_measured_evidence() -> None:
    original = run_experiment()
    relabeled = run_experiment(replace(
        FiniteResourceConfig(),
        node_ids=("u-left", "u-right", "u-target", "u-relay", "u-noise"),
    ))
    mirrored = run_experiment(replace(
        FiniteResourceConfig(),
        node_ids=("m-left", "m-right", "m-target", "m-relay", "m-noise"),
        task_source_role="left",
    ))
    for artifact in (original, relabeled, mirrored):
        pruning = artifact["stages"]["D_pruning"]
        assert pruning["task_result"] == "2/2"
        assert pruning["capacity_freed"] == 2
        assert all(item["reason"] == "inactivity_and_utility" for item in pruning["mutations"])
        assert artifact["stages"]["A_baseline"]["reference"]["useful_edge_present"]
    assert {item["edge"]["destination"].split("-")[-1] for item in original["stages"]["D_pruning"]["mutations"]} == {"noise", "target"}
    assert {item["edge"]["destination"].split("-")[-1] for item in mirrored["stages"]["D_pruning"]["mutations"]} == {"noise", "target"}
    assert all(item["edge"]["source"] != "m-left" for item in mirrored["stages"]["D_pruning"]["mutations"] if item["edge"]["destination"] == "m-target")


def test_artifact_declares_threshold_semantics_and_identity_controls() -> None:
    artifact = run_experiment()
    semantics = artifact["pruning_semantics"]
    assert semantics["labels_or_endpoint_identity_used"] is False
    assert "inactivity_age" in semantics["evidence_fields"]
    assert "observed_utility" in semantics["evidence_fields"]
    assert [item["actual_eligible"] for item in artifact["threshold_validation"]] == [False, True, True, False, True]
    assert set(artifact["identity_controls"]) == {"relabeled", "mirrored"}
    assert all(item["capacity_freed"] == 2 for item in artifact["identity_controls"].values())