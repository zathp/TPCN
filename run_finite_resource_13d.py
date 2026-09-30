"""Run the bounded Luna-13D finite-resource experiment."""

from __future__ import annotations

import argparse
import subprocess

from tpcn.finite_resource import run_experiment, write_artifacts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts/finite-resource-utility-13d")
    parser.add_argument("--baseline-revision", required=True)
    parser.add_argument("--executed-revision", default=None)
    args = parser.parse_args()
    artifact = run_experiment()
    tree_state = subprocess.check_output(("git", "status", "--short"), text=True).strip() or "clean"
    executed_revision = args.executed_revision or subprocess.check_output(("git", "rev-parse", "HEAD"), text=True).strip()
    write_artifacts(
        artifact,
        args.output_dir,
        baseline_revision=args.baseline_revision,
        executed_revision=executed_revision,
        tree_state=tree_state,
    )
    for name, stage in artifact["stages"].items():
        if name == "A_baseline":
            stage = stage["reference"]
        if isinstance(stage, dict) and "task_result" in stage:
            print(name, stage["task_result"], stage["total_events"], stage["completion_status"])


if __name__ == "__main__":
    main()