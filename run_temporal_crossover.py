"""Run the bounded Luna-13B causal local temporal crossover experiment."""

from __future__ import annotations

import argparse
import subprocess

from tpcn.temporal_crossover import CrossoverConfig, run_suite, write_artifacts


def _revision() -> str:
    return subprocess.check_output(("git", "rev-parse", "HEAD"), text=True).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts/causal-local-temporal-crossover-13b")
    parser.add_argument("--baseline-revision", required=True)
    parser.add_argument("--executed-revision", default=None)
    args = parser.parse_args()
    config = CrossoverConfig()
    results = run_suite(config=config)
    write_artifacts(
        results,
        args.output_dir,
        baseline_revision=args.baseline_revision,
        executed_revision=args.executed_revision or _revision(),
        config=config,
    )
    for result in results:
        print(
            result["condition"],
            "mirror=" + str(result["mirror"]),
            "rank=" + repr(result["ranked_candidates"]),
            "selected=" + repr(result["admission"]["selected_candidate"]),
            "completed=" + str(result["complete"]),
        )


if __name__ == "__main__":
    main()