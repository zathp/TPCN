"""Run the Luna-12G synthetic benchmark and write reproducible JSON evidence."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from tpcn.spiral_benchmark import SpiralConfig, make_spiral_dataset, metadata_json, run_controls


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/spiral-handedness-12g"))
    parser.add_argument("--examples-per-class", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--train-seed", type=int, default=12007)
    parser.add_argument("--evaluation-seed", type=int, default=12017)
    args = parser.parse_args()
    config = SpiralConfig()
    dataset = make_spiral_dataset(examples_per_class=args.examples_per_class,
                                  train_seed=args.train_seed, evaluation_seed=args.evaluation_seed,
                                  config=config)
    controls = run_controls(dataset, epochs=args.epochs, max_points=config.max_points)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "config.json").write_text(json.dumps({"generator": asdict(config), "epochs": args.epochs,
                                                          "examples_per_class": args.examples_per_class,
                                                          "train_seed": args.train_seed,
                                                          "evaluation_seed": args.evaluation_seed}, indent=2, sort_keys=True))
    (args.output / "benchmark.json").write_text(metadata_json(dataset, controls))
    (args.output / "summary.json").write_text(json.dumps([asdict(control) for control in controls], indent=2, sort_keys=True))
    for control in controls:
        print(f"{control.name}: accuracy={control.accuracy:.4f} confidence={control.confidence:.4f} margin={control.margin:.4f}")


if __name__ == "__main__":
    main()