"""Train the deterministic Luna-9 synthetic workload and save TPCV-1 replay data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tpcn.cpu_visualization import ReplaySequence, run_cpu_training
from tpcn.temporal_analysis import analyze_replay, compare_replays, summarize_analysis


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--examples-per-class", type=int, default=2)
    parser.add_argument("--snapshot-every", type=int, default=0, help="0 disables capture")
    parser.add_argument("--max-snapshots", type=int, default=64)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/cpu-tpcv"))
    parser.add_argument("--replay", type=Path, help="Load and inspect an existing replay directory")
    parser.add_argument("--structural-plasticity", action="store_true", help="Enable bounded Luna-10 topology adaptation")
    parser.add_argument("--no-learning", action="store_true", help="Disable the bounded outer-loop readout updates")
    parser.add_argument("--compare", type=Path, help="Compare replay analysis with a second replay directory")
    args = parser.parse_args()

    if args.replay is not None:
        sequence = ReplaySequence.load(args.replay, max_snapshots=args.max_snapshots)
        analysis = analyze_replay(sequence)
        if args.compare is not None:
            other = ReplaySequence.load(args.compare, max_snapshots=args.max_snapshots)
            print(summarize_analysis(analysis))
            print(json.dumps(compare_replays(sequence, other), sort_keys=True))
            return 0
        print(json.dumps({"snapshots": len(sequence.snapshots), "digest": sequence.digest,
                          "frames": sequence.frames(), "changes": sequence.changes(),
                          "connection_timeline": sequence.connection_timeline(),
                          "metrics": sequence.metrics, "analysis": analysis}, sort_keys=True, default=list))
        print(summarize_analysis(analysis))
        return 0

    result, capture = run_cpu_training(
        epochs=args.epochs,
        seed=args.seed,
        examples_per_class=args.examples_per_class,
        snapshot_every=args.snapshot_every,
        max_snapshots=args.max_snapshots,
        structural_plasticity=args.structural_plasticity,
        learning_enabled=not args.no_learning,
    )
    sequence = ReplaySequence(capture.snapshots, capture.metrics)
    sequence.save(args.output_dir)
    analysis = analyze_replay(sequence)
    (args.output_dir / "analysis.json").write_text(json.dumps(analysis, sort_keys=True, indent=2), encoding="utf-8")
    before = result.before.metrics if result.before is not None else result.evaluation.metrics
    after = result.after.metrics if result.after is not None else result.evaluation.metrics
    print(json.dumps({"output_dir": str(args.output_dir), "snapshots": len(sequence.snapshots),
                      "digest": sequence.digest, "starting_connections": before.connection_count,
                      "ending_connections": after.connection_count,
                      "additions": sum(item.accepted_additions for item in result.history),
                      "removals": sum(item.pruned_connections for item in result.history),
                      "mutation_rejections": sum(item.rejected_mutations for item in result.history),
                      "active_neuron_fraction": after.active_neuron_count / max(1, args.examples_per_class * 2),
                      "prediction_loss_before": before.prediction_loss, "prediction_loss_after": after.prediction_loss,
                      "accuracy_before": before.accuracy, "accuracy_after": after.accuracy,
                      "reward_before": before.reward, "reward_after": after.reward,
                      "energy_before": before.energy, "energy_after": after.energy,
                      "analysis": str(args.output_dir / "analysis.json"),
                      "utility_before": before.utility, "utility_after": after.utility,
                      "replay": f"python train_cpu_visualization.py --replay {args.output_dir}"}, sort_keys=True))
    print(summarize_analysis(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())