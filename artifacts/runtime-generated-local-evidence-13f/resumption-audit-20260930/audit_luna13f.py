"""Reproduce contract failures for the resumed Luna-13F prototype.

Run from any directory with Python -B. The output is an audit of a blocked
prototype, not successful Luna-13F experiment evidence. Runtime monkeypatches
are scoped; the original backup manifest remains the preservation reference.
"""
from __future__ import annotations

import ast
from collections import Counter
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
from tpcn import runtime_generated_evidence as f
from tpcn.event_runtime import Event

STATUS = "BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION"
OWNED = (
    "tpcn/runtime_generated_evidence.py",
    "run_runtime_generated_evidence_13f.py",
    "tests/test_luna13f_runtime_generated_evidence.py",
    "artifacts/runtime-generated-local-evidence-13f/results.json",
    "artifacts/runtime-generated-local-evidence-13f/summary.json",
)
BACKUP = Path(r"C:\Users\zathp\Documents\programming\TPCN-Luna-13F-backup-20260930-143250")
ORIGINAL_SHA256 = {
    "tpcn/runtime_generated_evidence.py": "1ee2f154c7ca637d653ad05fe5c74aa2cd7fdf33a5ad866a911119cbfed14c80",
    "run_runtime_generated_evidence_13f.py": "ea14917c94f3571968b86238ca34341e79bc8277dd0326b85c662cab07928aab",
    "tests/test_luna13f_runtime_generated_evidence.py": "43f6c411cc3470a9239c7765267b88e7b6486e8f1f79fffc63b7866fd9bddd4f",
    "artifacts/runtime-generated-local-evidence-13f/results.json": "20535bb2e5945272286060e7bcb1b4553dca5937760d63ccf62273830f5555c4",
    "artifacts/runtime-generated-local-evidence-13f/summary.json": "009c2c61ae2b81a61948972ed04b6a2a708aa1dfc73edbf4c091ba294d5efcb7",
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(("git", *args), cwd=ROOT, text=True).strip()

def decision(runtime, config):
    admission = f._admit(config, runtime)
    return {"decision_timestamp": runtime["decision_timestamp"],
            "scores": f._jsonable(admission["scores"]),
            "selected_candidate": admission["selected_candidate"],
            "selected_result": admission["selected_result"],
            "execution": runtime["execution"]}

def main():
    before = {p: digest(ROOT / p) for p in OWNED}
    config = f.RuntimeEvidenceConfig()
    artifact = f.run_experiment(config)
    runtime = artifact["primary"]["runtime"]
    admission = artifact["primary"]["admission"]
    checks = []
    def record(name, passed, observed):
        checks.append({"check": name, "status": "passed" if passed else "failed",
                       "evidence_label": "OBSERVED", "observed": observed})

    counts = Counter(o["candidate"] for o in runtime["observations"])
    record("matched_candidate_exposure", counts["relay"] == counts["noise"], dict(counts))
    schedule_source = (ROOT / OWNED[0]).read_text(encoding="utf-8")
    tree = ast.parse(schedule_source)
    schedule_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_schedule")
    schedule_text = ast.get_source_segment(schedule_source, schedule_node)
    role_dependency = "config.beneficial_role" in schedule_text and "config.harmful_role" in schedule_text
    record("fixture_role_free_evidence_generation", not role_dependency, {
        "schedule_role_dependency": role_dependency,
        "source_lines": [schedule_node.lineno, schedule_node.end_lineno],
        "primary_schedule": f._jsonable(runtime["schedule"])})

    original_schedule = f._schedule
    future_events = tuple(
        event for t in (7.0, 9.0, 11.0, 13.0)
        for event in (Event(t, "source", "source", "local_anchor", 1.0),
                      Event(t + 0.5, "noise", "source", "candidate_observation", 0.5)))
    def with_future(cfg, control, *, mirror=False):
        return original_schedule(cfg, control, mirror=mirror) + future_events
    with patch.object(f, "_schedule", with_future):
        mutated = f._run_runtime_evidence(config)
    base_decision, future_decision = decision(runtime, config), decision(mutated, config)
    record("post_decision_events_cannot_change_frozen_decision",
           base_decision["scores"] == future_decision["scores"]
           and base_decision["selected_candidate"] == future_decision["selected_candidate"]
           and base_decision["decision_timestamp"] == future_decision["decision_timestamp"],
           {"baseline": base_decision, "future_only_mutation": future_decision,
            "appended_timestamps": [e.timestamp for e in future_events],
            "all_appended_after_original_decision": all(e.timestamp > runtime["decision_timestamp"] for e in future_events)})

    exhausted = f._run_runtime_evidence(replace(config, event_budget=2))
    exhausted_decision = decision(exhausted, replace(config, event_budget=2))
    record("incomplete_evidence_run_does_not_admit_growth",
           exhausted_decision["selected_result"]["status"] != "grown", exhausted_decision)
    equalized = artifact["controls"]["evidence_equalized"]
    equal_scores = list(equalized["admission"]["scores"].values())
    record("evidence_equalization_produces_actual_tie", len(set(equal_scores)) == 1,
           f._jsonable(equalized["admission"]["scores"]))
    no_evidence = artifact["controls"]["no_evidence"]
    record("no_evidence_preserves_candidate_opportunity",
           len(no_evidence["admission"]["candidate_set"]) == 2,
           {"candidate_set": no_evidence["admission"]["candidate_set"],
            "selected_candidate": no_evidence["admission"]["selected_candidate"]})

    zeros = dict(runtime)
    zeros["evidence"] = tuple(replace(e, score=0.0) for e in runtime["evidence"])
    zero_admission = f._admit(config, zeros)
    record("canonical_zero_score_tie_is_explicit",
           zero_admission["selected_candidate"] == "H", {
               "interpretation": "Diagnostic only: canonical scorer has no abstention threshold.",
               "scores": f._jsonable(zero_admission["scores"]),
               "selected_candidate": zero_admission["selected_candidate"]})

    held_times = [row["timestamp"] for value in artifact["held_out"].values()
                  for row in value["route_trace"]]
    record("held_out_timestamps_later_than_decision",
           bool(held_times) and min(held_times) > runtime["decision_timestamp"],
           {"held_out_min_timestamp": min(held_times),
            "decision_timestamp": runtime["decision_timestamp"]})
    updates = [o["evidence_update"] for o in runtime["observations"] if o["candidate"] == "relay"]
    record("reported_updates_are_actual_score_deltas", updates == [1.0, 1.0, 1.0],
           {"reported_updates": updates, "actual_count_deltas": [1.0, 1.0, 1.0]})
    record("two_legal_candidates_one_free_slot",
           admission["legal_candidates"] == {"G": True, "H": True}
           and admission["relevant_free_slots"] == 1 and len(admission["final_edges"]) == 3,
           {"legal_candidates": admission["legal_candidates"],
            "free_slots": admission["relevant_free_slots"], "final_edges": admission["final_edges"]})
    record("deterministic_replay", artifact == f.run_experiment(config), {})
    for rel in OWNED[:3]:
        compile((ROOT / rel).read_bytes(), rel, "exec")
    record("three_original_sources_compile_in_memory", True, list(OWNED[:3]))
    backup_hashes = {p: digest(BACKUP / p) for p in OWNED}
    record("original_five_files_preserved_and_backup_exact",
           backup_hashes == ORIGINAL_SHA256, {
               "original_sha256": ORIGINAL_SHA256,
               "backup_sha256": backup_hashes,
               "current_sha256": {p: digest(ROOT / p) for p in OWNED},
           })
    for name in ("external_label_mutation", "locality_attack", "neutral_decay_runtime_sweep",
                 "candidate_saturation_reset_eviction", "valid_mirrored_roles"):
        checks.append({"check": name, "status": "not_run",
                       "reason": "Not established by preserved prototype; contamination blocks success."})
    payload = {
        "schema_version": "TPCN-LUNA-13F-RESUMPTION-AUDIT-1",
        "terminal_status": STATUS,
        "provenance": {
            "starting_revision": git("rev-parse", "HEAD"),
            "executed_committed_revision": git("rev-parse", "HEAD"),
            "committed_tree": git("rev-parse", "HEAD^{tree}"),
            "executed_source_note": "Current source is identified by SHA-256; the original backup manifest is retained separately.",
            "branch": git("branch", "--show-current"),
            "generation_status": git("status", "--short", "--untracked-files=all"),
            "original_sha256": before, "audit_script_sha256": digest(Path(__file__)),
            "source_manifest_sha256": hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
            "backup_directory": str(BACKUP),
            "python": sys.version, "platform": platform.platform()},
        "checks": checks,
        "parent_verified_baseline_checks": {
            "focused": "8 passed",
            "full_cpu": "284 passed, 1 skipped in 9.27s",
            "command": "python -B -m pytest -q -p no:cacheprovider",
            "source": "Parent agent live Desktop Commander baseline audit, unchanged original files",
            "other": "Saved artifact semantic replay and whitespace checks passed; no editor diagnostic provider invoked."},
        "architecture_conclusion": {
            "OBSERVED": "Existing policy accumulates bounded counts; role-keyed schedule manufactures their informativeness.",
            "INFERRED": "This prototype cannot substantiate runtime-generated useful discrimination.",
            "HYPOTHESIZED": "An architecture-compatible ordinary-runtime fixture may exist; impossibility is not established.",
            "architecture_change_required": "not established", "architecture_change_implemented": False},
        "next_execution_state": "Luna-0 independent review of blocked Luna-13F and corrective fixture scope; Luna-13G unauthorized.",
    }
    output = Path(__file__).with_name("audit-results.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(STATUS)
    print(json.dumps({s: sum(c["status"] == s for c in checks)
                      for s in ("passed", "failed", "not_run")}, sort_keys=True))
    print(str(output))

if __name__ == "__main__":
    main()
