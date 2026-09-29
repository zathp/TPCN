"""Generate the bounded Luna-12N direction/decay experiment artifacts."""

from __future__ import annotations

import argparse
import subprocess

from tpcn.temporal_direction import run_temporal_direction_suite, write_artifacts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/temporal-direction-12n-corrected")
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2, 3, 4])
    args = parser.parse_args()
    baseline = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    results = run_temporal_direction_suite(seeds=tuple(args.seeds), baseline_revision=baseline)
    write_artifacts(results, args.output, baseline_revision=baseline)
    print(f"wrote {len(results)} Luna-12N records to {args.output}")


if __name__ == "__main__":
    main()
