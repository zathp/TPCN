from dataclasses import replace

from tpcn.runtime_generated_evidence import RuntimeEvidenceConfig, run_experiment


def test_neutral_mappings_remove_role_keyed_pre_admission_construction():
    artifact = run_experiment()
    assert artifact["terminal_status"] == "NEGATIVE RESULT - RUNTIME EVIDENCE GENERATED BUT DOES NOT PREDICT USEFUL GROWTH"
    assert set(artifact["neutral_mappings"]) == {"P0", "P1"}
    for mapping in artifact["neutral_mappings"].values():
        assert set(mapping["mapping"]["candidates"]) == {"candidate_A", "candidate_B"}
        assert mapping["runtime"]["mapping_id"] in {"P0", "P1"}
        assert mapping["admission"]["selected_candidate"] in {"candidate_A", "candidate_B"}
    assert "beneficial_role" not in artifact["configuration"]
    assert "harmful_role" not in artifact["configuration"]


def test_runtime_evidence_is_local_bounded_and_pre_admission():
    primary = run_experiment()["primary"]
    runtime = primary["runtime"]
    assert runtime["observations"]
    assert runtime["owner"] == "source"
    assert runtime["bounds"]["maximum_tracked_candidates"] == 2
    assert all(item["receiving_local_component"] == "source" for item in runtime["observations"])
    assert all(item["evidence_timestamp"] <= runtime["decision_timestamp"] for item in runtime["observations"])
    assert runtime["execution"]["completed"]
    assert not runtime["execution"]["budget_exhausted"]


def test_one_slot_competition_has_two_legal_neutral_candidates():
    admission = run_experiment()["primary"]["admission"]
    assert admission["relevant_free_slots"] == 1
    assert admission["legal_candidates"] == {"candidate_A": True, "candidate_B": True}
    assert len(admission["rejected_candidates"]) == 1
    assert admission["rejected_candidates"][0]["reason"] == "edge_capacity"


def test_cross_mapping_reports_post_hoc_utility_only_after_admission():
    mappings = run_experiment()["neutral_mappings"]
    assert mappings["P0"]["admission"]["selected_candidate"] == "candidate_A"
    assert mappings["P1"]["admission"]["selected_candidate"] == "candidate_A"
    assert mappings["P0"]["held_out"]["candidate_A"]["task_result"] == "2/2"
    assert mappings["P1"]["held_out"]["candidate_A"]["task_result"] == "1/2"
    assert mappings["P0"]["runtime"]["decision_timestamp"] < mappings["P0"]["selected_held_out"]["first_held_out_timestamp"]


def test_required_controls_are_executed():
    controls = run_experiment()["controls"]
    assert controls["external_label_mutation"]["pre_admission_unchanged"]
    assert controls["locality_attack"]["passed"]
    assert controls["neutral_decay"]["status"] == "executed"
    assert len(controls["neutral_decay"]["runs"]) == 3
    assert controls["candidate_saturation_reset_eviction"]["bounded"]
    assert controls["candidate_saturation_reset_eviction"]["deterministic"]
    assert controls["mirrored"]["admission"]["selected_candidate"] == "candidate_B"


def test_controls_preserve_or_expose_runtime_decision_boundaries():
    artifact = run_experiment()
    primary = artifact["primary"]["admission"]
    controls = artifact["controls"]
    assert primary["scores"] == controls["future_events"]["admission"]["scores"]
    assert primary["selected_candidate"] == controls["future_events"]["admission"]["selected_candidate"]
    assert controls["candidate_order"]["selected_candidate"] == primary["selected_candidate"]
    assert set(controls["no_evidence"]["admission"]["scores"].values()) == {0.0}
    assert controls["external_label_mutation"]["selected_candidate"] == primary["selected_candidate"]


def test_decay_sweep_shows_count_based_score_and_local_state_effect():
    runs = run_experiment()["controls"]["neutral_decay"]["runs"]
    score_sets = {tuple(sorted(run["scores"].items())) for run in runs.values()}
    assert len(score_sets) == 1
    assert all(run["runtime"]["decay_rate"] >= 0.0 for run in runs.values())


def test_replay_and_budget_are_deterministic():
    config = RuntimeEvidenceConfig(random_seeds=(10, 11))
    assert run_experiment(config) == run_experiment(config)
    limited = run_experiment(replace(config, event_budget=2))
    assert limited["primary"]["runtime"]["execution"]["budget_exhausted"]
    assert limited["primary"]["admission"]["status"] == "incomplete"


def test_neutral_mapping_is_independent_of_external_label_metadata():
    first = run_experiment()
    second = run_experiment()
    assert first["primary"]["runtime"]["schedule"] == second["primary"]["runtime"]["schedule"]
    assert first["controls"]["external_label_mutation"]["scores"] == second["controls"]["external_label_mutation"]["scores"]


def test_score_reconstruction_uses_runtime_observations():
    artifact = run_experiment()
    runtime = artifact["primary"]["runtime"]
    observed = {endpoint: 0 for endpoint in runtime["candidate_endpoints"].values()}
    for item in runtime["observations"]:
        observed[item["candidate"]] += int(item["evidence_update"] > 0.0)
    assert artifact["primary"]["admission"]["scores"] == {
        ("source", endpoint): float(count) for endpoint, count in observed.items()
    }


def test_chronology_label_and_locality_controls_are_executed():
    artifact = run_experiment()
    controls = artifact["controls"]
    assert controls["chronology_attack"]["passed"]
    chronology = controls["chronology_attack"]["results"]
    assert chronology["before_decision"]["accepted_into_held_out_phase"] is False
    assert chronology["equal_decision"]["accepted_into_held_out_phase"] is False
    assert chronology["after_decision"]["accepted_into_held_out_phase"] is True
    assert controls["external_label_mutation"]["passed"]
    assert controls["external_label_mutation"]["pre_admission_unchanged"]
    assert controls["locality_attack"]["passed"]
    locality = controls["locality_attack"]
    assert locality["prohibited_field_mutated"]["after"] == 999
    assert locality["candidate_A_raw_evidence_before"] == locality["candidate_A_raw_evidence_after"]
    assert locality["raw_evidence_before"] != locality["raw_evidence_after"]
    assert locality["dependency_trace"]["prohibited_inputs_read"] == []


def test_future_continuation_changes_live_state_but_not_completed_decision():
    future = run_experiment()["controls"]["future_events"]
    runtime = future["runtime"]
    continuation = runtime["future_continuation"]
    assert continuation["processed_event_count"] == 10
    assert continuation["pending_event_count"] == 0
    assert all(item["event_type"].startswith("future_") for item in continuation["actual_events"])
    assert future["post_future_live_state"]["live_evidence"] != future["pre_future_snapshot"]["frozen_evidence"]
    assert future["historical_decision_unchanged"]


def test_chronology_records_actual_queue_processing_order():
    chronology = run_experiment()["controls"]["chronology_attack"]["results"]
    for name, result in chronology.items():
        sequence = result["processing_sequence"]
        assert result["processed_event_count"] <= result["event_budget"]
        assert "held_out_evaluation" in result["actual_processing_order"]
        if name == "after_decision":
            assert result["actual_processing_order"].index("structural_admission") < result["actual_processing_order"].index("held_out_evaluation")
        else:
            assert result["actual_processing_order"].index("held_out_evaluation") < result["actual_processing_order"].index("structural_admission")
        assert sequence[result["actual_processing_order"].index("held_out_evaluation")]["phase"] in {"pre_admission", "post_admission"}


def test_candidate_lifecycle_and_budget_controls_are_bounded():
    artifact = run_experiment()
    lifecycle = artifact["controls"]["candidate_saturation_reset_eviction"]
    budget = artifact["controls"]["budget_boundary"]
    assert lifecycle["bounded"] and lifecycle["deterministic"]
    assert "reset clears history" in lifecycle["reset_semantics"]
    assert lifecycle["stale_state_reuse"]["clean"]
    assert lifecycle["expiry_semantics"].startswith("NOT APPLICABLE")
    assert lifecycle["eviction_semantics"].startswith("NOT APPLICABLE")
    assert budget["passed"]
    assert not budget["runs"]["B-1"]["valid_admission"]
    assert budget["runs"]["B"]["valid_admission"]
    assert budget["runs"]["B"]["scores"] == budget["runs"]["large"]["scores"]


def test_contract_audit_has_no_unexplained_missing_controls():
    audit = run_experiment()["contract_audit"]
    assert audit["complete"]
    assert audit["summary"]["FAIL"] == 0
    assert audit["summary"]["NOT APPLICABLE - CONDITION NOT TRIGGERED"] == 2
    assert all(item["status"] != "NOT RUN" for item in audit["requirements"])
