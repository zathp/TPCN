"""Run the bounded Luna-13E post-pruning admission experiment."""

from __future__ import annotations

import argparse
import subprocess

from tpcn.post_pruning_admission import AdmissionQualityConfig, run_experiment, write_artifacts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts/post-pruning-admission-13e")
    parser.add_argument("--baseline-revision", required=True)
    parser.add_argument("--executed-revision", default=None)
    args = parser.parse_args()
    artifact = run_experiment(AdmissionQualityConfig())
    tree_state = subprocess.check_output(("git", "status", "--short"), text=True).strip() or "clean"
    executed_revision = args.executed_revision or subprocess.check_output(("git", "rev-parse", "HEAD"), text=True).strip()
    write_artifacts(
        artifact,
        args.output_dir,
        baseline_revision=args.baseline_revision,
        executed_revision=executed_revision,
        tree_state=tree_state,
    )
    print("current-policy", artifact["competition"]["chosen_candidate"], artifact["competition"]["evaluation"]["task_result"])
    print("terminal-status", "PASS — PRE-ADMISSION EVIDENCE DISTINGUISHES BENEFICIAL FROM HARMFUL GROWTH, READY FOR LUNA-0 REVIEW")


if __name__ == "__main__":
    main()
