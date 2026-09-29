"""Run the bounded Luna-13C useful causal effect experiment."""

from __future__ import annotations

import argparse
from dataclasses import replace
import subprocess

from tpcn.causal_utility import UtilityConfig, run_experiment, write_artifacts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts/useful-causal-effect-13c")
    parser.add_argument("--baseline-revision", required=True)
    parser.add_argument("--executed-revision", default=None)
    args = parser.parse_args()
    config = UtilityConfig()
    artifact = run_experiment(config=config)
    independent_random_results = {}
    for seed in (0, 1):
        repeated = run_experiment(config=replace(config, random_seed=seed))
        random_result = repeated["results"]["random_growth"]
        independent_random_results[str(seed)] = {
            "graph_edges": random_result["graph_edges"],
            "graph_fingerprint": random_result["graph_fingerprint"],
            "accuracy": random_result["primary_metric_value"],
            "correct_cases": sum(case["correct"] for case in random_result["case_results"]),
            "case_count": len(random_result["case_results"]),
            "all_completed": random_result["all_completed"],
        }
    artifact["controls"]["independent_random_seed_results"] = independent_random_results
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