"""Train the deterministic Luna-9 synthetic workload and save TPCV-1 replay data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tpcn.cpu_visualization import ReplaySequence, run_cpu_training


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--examples-per-class", type=int, default=2)
    parser.add_argument("--snapshot-every", type=int, default=0, help="0 disables capture")
    parser.add_argument("--max-snapshots", type=int, default=64)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/cpu-tpcv"))
    parser.add_argument("--replay", type=Path, help="Load and inspect an existing replay directory")
    parser.add_argument("--structural-plasticity", action="store_true", help="Reserved; Luna-10 integration is deferred")
    args = parser.parse_args()

    if args.structural_plasticity:
        parser.error("structural-plasticity visualization is deferred; fixed topology is the validated default")
    if args.replay is not None:
        sequence = ReplaySequence.load(args.replay, max_snapshots=args.max_snapshots)
        print(json.dumps({"snapshots": len(sequence.snapshots), "digest": sequence.digest,
                          "frames": sequence.frames(), "changes": sequence.changes(),
                          "metrics": sequence.metrics}, sort_keys=True, default=list))
        return 0

    result, capture = run_cpu_training(
        epochs=args.epochs,
        seed=args.seed,
        examples_per_class=args.examples_per_class,
        snapshot_every=args.snapshot_every,
        max_snapshots=args.max_snapshots,
    )
    sequence = ReplaySequence(capture.snapshots, capture.metrics)
    sequence.save(args.output_dir)
    print(json.dumps({"output_dir": str(args.output_dir), "snapshots": len(sequence.snapshots),
                      "digest": sequence.digest, "accuracy": result.evaluation.metrics.accuracy,
                      "replay": f"python train_cpu_visualization.py --replay {args.output_dir}"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())