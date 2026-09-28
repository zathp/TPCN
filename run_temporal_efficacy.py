"""Run the Luna-12J controlled temporal-association efficacy fixture."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from tpcn.temporal_efficacy import TemporalEfficacyConfig, run_temporal_efficacy_suite


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/temporal-efficacy-12j"))
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    args = parser.parse_args()
    config = TemporalEfficacyConfig()
    results = run_temporal_efficacy_suite(seeds=tuple(args.seeds), config=config)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "config.json").write_text(
        json.dumps({"config": asdict(config), "seeds": args.seeds}, indent=2, sort_keys=True)
    )
    (args.output / "results.json").write_text(
        json.dumps([asdict(result) for result in results], indent=2, sort_keys=True)
    )
    for result in results:
        metrics = result.metrics
        print(
            f"{metrics.policy} seed={metrics.seed} accuracy={metrics.accuracy:.3f} "
            f"separation={metrics.class_separation:.6f} edges={metrics.edge_count} "
            f"motifs={metrics.convergent_fan_in_motifs} events={metrics.event_count} "
            f"energy={metrics.energy:.6f}"
        )


if __name__ == "__main__":
    main()