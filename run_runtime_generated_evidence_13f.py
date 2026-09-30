"""Run the CPU-only Luna-13F runtime-generated evidence experiment."""

from __future__ import annotations

import argparse
import subprocess

from tpcn.runtime_generated_evidence import RuntimeEvidenceConfig, run_experiment, write_artifacts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts/runtime-generated-local-evidence-13f")
    parser.add_argument("--baseline-revision", required=True)
    parser.add_argument("--executed-revision", default=None)
    args = parser.parse_args()
    artifact = run_experiment(RuntimeEvidenceConfig())
    tree_state = subprocess.check_output(("git", "status", "--short"), text=True).strip() or "clean"
    executed_revision = args.executed_revision or subprocess.check_output(("git", "rev-parse", "HEAD"), text=True).strip()
    write_artifacts(
        artifact,
        args.output_dir,
        baseline_revision=args.baseline_revision,
        executed_revision=executed_revision,
        tree_state=tree_state,
    )
    primary = artifact["primary"]
    print("primary-selected", primary["admission"]["selected_candidate"])
    print("primary-scores", primary["admission"]["scores"])
    print("held-out", artifact["held_out"]["candidate_A"]["task_result"], artifact["held_out"]["candidate_B"]["task_result"])
    print("terminal-status", artifact["terminal_status"])


if __name__ == "__main__":
    main()
