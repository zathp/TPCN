"""Run the Luna-12L four-class scale experiment and write JSON evidence."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from tpcn.temporal_scale import SCALES, run_luna12l_suite

BASELINE_REVISION = "3122c7dbae2589c1c78fe6169d394f525c212ec1"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/temporal-scale-12l"))
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    args = parser.parse_args()
    results = run_luna12l_suite(seeds=tuple(args.seeds))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "config.json").write_text(json.dumps({
        "baseline_revision": BASELINE_REVISION,
        "run_status": "corrective-rerun-after-luna-0-blocked-review",
        "supersedes": "artifacts/temporal-scale-12l-invalid-pre-coupling",
        "policy_scale_coupling": "classifier and structural metrics are executed from the same requested policy and scale; mismatches raise",
        "class_labels": [
            "spiral-left-outward", "spiral-right-outward",
            "spiral-left-inward", "spiral-right-inward",
        ],
        "scales": [asdict(scale) for scale in SCALES],
        "policies": ["fixed", "baseline", "random", "temporal", "reversed"],
        "seeds": args.seeds,
        "zero_correct_ratio_policy": "null",
    }, indent=2, sort_keys=True))
    (args.output / "results.json").write_text(
        json.dumps([asdict(result) for result in results], indent=2, sort_keys=True)
    )
    for result in results:
        print(f"{result.scale} {result.policy} seed={result.seed} "
              f"accuracy={result.accuracy:.3f} energy={result.proxy_energy:.6f} "
              f"delay={result.path_delay:.3f} shortcut={result.shortcut_selected}")


if __name__ == "__main__":
    main()
