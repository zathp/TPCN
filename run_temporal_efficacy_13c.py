"""Run the bounded Luna-13C useful causal effect experiment."""

from __future__ import annotations

import argparse
import subprocess

from tpcn.causal_utility import UtilityConfig, run_experiment, write_artifacts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts/useful-causal-effect-13c")
    parser.add_argument("--baseline-revision", required=True)
    parser.add_argument("--executed-revision", default=None)
    args = parser.parse_args()
    artifact = run_experiment(config=UtilityConfig())
    tree_state = subprocess.check_output(("git", "status", "--short"), text=True).strip() or "clean"
    write_artifacts(
        artifact,
        args.output_dir,
        baseline_revision=args.baseline_revision,
        executed_revision=args.executed_revision or subprocess.check_output(("git", "rev-parse", "HEAD"), text=True).strip(),
        tree_state=tree_state,
    )
    for condition, result in artifact["results"].items():
        print(condition, result["primary_metric_value"], result["graph_fingerprint"], result["all_completed"])


if __name__ == "__main__":
    main()