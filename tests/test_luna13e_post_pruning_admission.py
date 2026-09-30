from tpcn.post_pruning_admission import (
    AdmissionQualityConfig,
    _base_edges,
    _candidate_edges,
    _competition,
    _evaluate,
    _topology,
    run_experiment,
)


def test_harmful_growth_reference_and_candidate_ground_truth_are_frozen() -> None:
    artifact = run_experiment()
    reference = artifact["stage_A_harmful_growth_reproduction"]
    assert reference["baseline_post_pruning"]["task_result"] == "2/2"
    assert reference["baseline_post_pruning"]["total_events"] == 8
    assert reference["baseline_post_pruning"]["proxy_energy"] == 8.0
    assert reference["harmful_post_growth"]["task_result"] == "1/2"
    assert reference["harmful_post_growth"]["total_events"] == 16
    assert reference["harmful_post_growth"]["proxy_energy"] == 16.0
    assert "expected held-out task 1/2" in artifact["frozen_ground_truth"]["H"]
    assert reference["diagnostic_trace"]["harmful_post_growth"][1]["target_state"] is not None
    assert reference["diagnostic_trace"]["harmful_post_growth"][1]["target_arrivals"] == (1.0, 1.0, 4.0, 4.0)
    assert artifact["frozen_ground_truth"]["external_only"]
    assert artifact["frozen_ground_truth"]["frozen_before_policy_comparison"]


def test_one_slot_competition_has_two_legal_candidates_and_current_policy() -> None:
    artifact = run_experiment()
    competition = artifact["competition"]
    config = AdmissionQualityConfig()
    base = _topology(config, _base_edges(config))
    for edge in _candidate_edges(config).values():
        individual = _topology(config, _base_edges(config))
        individual.connect(*edge)
        assert len(individual) == 3
    assert competition["relevant_free_slots"] == 1
    assert competition["chosen_candidate"] == "G"
    assert competition["rejected_candidate"] == "H"
    assert competition["scores"]["G"] > competition["scores"]["H"]
    assert competition["ranks"] == {"G": 1, "H": 2}
    assert competition["evaluation"]["task_result"] == "2/2"
    assert len(competition["final_edges"]) == len(base.edges) + 1


def test_beneficial_and_harmful_candidates_are_separately_evaluated() -> None:
    config = AdmissionQualityConfig()
    base = _base_edges(config)
    candidates = _candidate_edges(config)
    beneficial = _evaluate(config, base + (candidates["G"],), "G-held-out")
    harmful = _evaluate(config, base + (candidates["H"],), "H-held-out")
    assert beneficial["task_result"] == "2/2"
    assert harmful["task_result"] == "1/2"
    assert beneficial["completion_status"] == "completed"
    assert harmful["completion_status"] == "completed"


def test_provenance_is_pre_admission_local_bounded_and_score_driving() -> None:
    competition = run_experiment()["competition"]
    records = competition["candidate_evidence"]
    assert {record["candidate"] for record in records} == {"G", "H"}
    assert all(record["local"] and record["bounded"] and record["pre_admission"] for record in records)
    assert all(not record["future_dependent"] and not record["label_dependent"] for record in records)
    assert all(record["used_in_canonical_score"] for record in records)
    assert all("observation_records" in record for record in records)


def test_relabeling_and_mirrored_roles_follow_evidence() -> None:
    controls = run_experiment()["controls"]
    assert controls["relabelled"]["chosen_candidate"] == "G"
    assert controls["mirrored"]["chosen_candidate"] == "G"
    assert controls["relabelled"]["evaluation"]["task_result"] == "2/2"
    assert controls["mirrored"]["evaluation"]["task_result"] == "2/2"


def test_evidence_equalized_control_is_reported_as_tie_breaking() -> None:
    equalized = run_experiment()["controls"]["evidence_equalized"]
    assert equalized["scores"] == {"G": 1.0, "H": 1.0}
    assert equalized["ranks"]["G"] != equalized["ranks"]["H"]
    assert equalized["rejection_reason"] == "lost_one_slot_rank_competition"


def test_future_events_and_label_mutation_do_not_change_admission() -> None:
    artifact = run_experiment()
    current = artifact["competition"]
    future = artifact["controls"]["future_events_after_decision"]
    labels = artifact["controls"]["label_mutated"]
    assert (current["scores"], current["ranks"], current["chosen_candidate"], current["final_graph_fingerprint"]) == (
        future["scores"], future["ranks"], future["chosen_candidate"], future["final_graph_fingerprint"]
    )
    assert (current["scores"], current["ranks"], current["chosen_candidate"]) == (
        labels["scores"], labels["ranks"], labels["chosen_candidate"]
    )
    assert labels["runtime_input_unchanged"]
    assert labels["mutated_external_targets"] == ("late", "on_time")


def test_current_architecture_has_no_threshold_or_abstention() -> None:
    semantics = run_experiment()["threshold_and_abstention"]
    assert semantics["score_threshold"] is None
    assert semantics["confidence_threshold"] is None
    assert semantics["abstention_supported"] is False
    assert semantics["forced_growth_when_selected"] is True
    assert semantics["negative_score_growth"]["status"] == "grown"


def test_fixed_no_growth_and_random_controls_are_bounded() -> None:
    artifact = run_experiment(AdmissionQualityConfig(random_seeds=(0, 1, 2, 3, 4)))
    fixed = artifact["controls"]["fixed_no_growth"]
    assert fixed["task_result"] == "1/2"
    assert fixed["completion_status"] == "completed"
    random_controls = artifact["controls"]["random"]
    assert [item["seed"] for item in random_controls] == [0, 1, 2, 3, 4]
    assert {item["selected_candidate"] for item in random_controls} == {"G", "H"}
    assert all(item["evaluation"]["completion_status"] == "completed" for item in random_controls)


def test_ablation_inventory_separates_canonical_score_from_unavailable_signals() -> None:
    artifact = run_experiment()
    assert artifact["ablations"]["temporal_evidence_only"]["chosen_candidate"] == "G"
    assert artifact["ablations"]["score_removed"]["scores"] == {"G": 0.0, "H": 0.0}
    assert artifact["ablations"]["utility_reward_removed"]["available"] is False
    assert artifact["ablations"]["prediction_error_removed"]["available"] is False
    inventory = artifact["evidence_inventory"]
    assert "CandidateEvidence.score" in inventory["available"]
    assert "propagation_delay; no predicted total path cost" in inventory["available_but_not_used"]
    assert "task result" in inventory["unavailable_before_admission"]
