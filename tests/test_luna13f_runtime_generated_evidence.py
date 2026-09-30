from dataclasses import replace

from tpcn.runtime_generated_evidence import RuntimeEvidenceConfig, run_experiment


def test_runtime_evidence_is_generated_without_luna13e_tuple_helpers() -> None:
    artifact = run_experiment()
    primary = artifact["primary"]
    assert artifact["old_luna_13e_tuple_path"]["removed_from_primary"]
    assert artifact["terminal_status"] == "BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION"
    assert primary["runtime"]["observations"]
    assert primary["admission"]["scores"] == {("source", "relay"): 3.0, ("source", "noise"): 0.0}
    assert primary["admission"]["selected_candidate"] == "G"
    assert all(record["evidence_timestamp"] <= primary["runtime"]["decision_timestamp"]
               for record in primary["runtime"]["observations"])


def test_evidence_provenance_is_local_bounded_and_pre_admission() -> None:
    runtime = run_experiment()["primary"]["runtime"]
    assert runtime["owner"] == "source"
    assert runtime["bounds"]["maximum_tracked_candidates"] == 2
    assert runtime["bounds"]["history_capacity"] == 8
    assert all(item["receiving_local_component"] == "source" for item in runtime["observations"])
    assert all(item["evidence_timestamp"] <= runtime["decision_timestamp"] for item in runtime["observations"])
    assert runtime["execution"]["completed"]
    assert not runtime["execution"]["budget_exhausted"]


def test_one_slot_has_two_legal_candidates_and_only_one_admission() -> None:
    admission = run_experiment()["primary"]["admission"]
    assert admission["relevant_free_slots"] == 1
    assert admission["legal_candidates"] == {"G": True, "H": True}
    assert admission["selected_candidate"] == "G"
    assert len(admission["final_edges"]) == 3
    assert len(admission["rejected_candidates"]) == 1
    assert admission["rejected_candidates"][0]["reason"] == "edge_capacity"


def test_mirror_relabel_order_and_equalized_controls() -> None:
    controls = run_experiment()["controls"]
    assert controls["mirrored"]["admission"]["selected_candidate"] == "H"
    assert controls["relabelled"]["admission"]["selected_candidate"] == "G"
    assert controls["candidate_order"]["selected_candidate"] == "G"
    assert controls["evidence_equalized"]["admission"]["selected_candidate"] == "G"


def test_future_events_and_external_evaluation_do_not_drive_admission() -> None:
    artifact = run_experiment()
    primary = artifact["primary"]["admission"]
    future = artifact["controls"]["future_events"]["admission"]
    assert primary["scores"] == future["scores"]
    assert primary["selected_candidate"] == future["selected_candidate"]
    assert artifact["held_out"]["G"]["task_result"] == "2/2"
    assert artifact["held_out"]["H"]["task_result"] == "1/2"
    assert artifact["no_growth"]["task_result"] == "2/2"


def test_required_exposure_controls_are_reported_and_bounded() -> None:
    controls = run_experiment()["controls"]
    for name in ("time_shuffle", "reversed", "uniform", "no_evidence", "future_events"):
        assert "runtime" in controls[name]
        assert controls[name]["runtime"]["execution"]["configured_event_budget"] == 32
    assert controls["neutral_decay"]["status"] == "not_applicable"
    assert controls["no_evidence"]["admission"]["selected_candidate"] is None


def test_replay_is_deterministic_and_budget_is_configured() -> None:
    config = RuntimeEvidenceConfig(random_seeds=(10, 11))
    assert run_experiment(config) == run_experiment(config)
    limited = run_experiment(replace(config, event_budget=2))
    assert limited["primary"]["runtime"]["execution"]["budget_exhausted"]
    assert limited["primary"]["runtime"]["execution"]["configured_event_budget"] == 2


def test_score_reconstruction_uses_runtime_evidence_directly() -> None:
    artifact = run_experiment()
    runtime = artifact["primary"]["runtime"]
    observed_counts = {"relay": 0, "noise": 0}
    for item in runtime["observations"]:
        observed_counts[item["candidate"]] += int(item["evidence_update"] > 0.0)
    scores = artifact["primary"]["admission"]["scores"]
    assert scores[("source", "relay")] == observed_counts["relay"]
    assert scores[("source", "noise")] == observed_counts["noise"]
    assert artifact["analytic_expectation"]["held_out_evaluation_not_used"]
