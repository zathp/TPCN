"""Run the Luna-12K capacity-pressure and path-shortening fixture."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from tpcn.temporal_capacity import CapacityPressureConfig, run_temporal_capacity_suite


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/temporal-capacity-12k"))
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    args = parser.parse_args()
    config = CapacityPressureConfig()
    results = run_temporal_capacity_suite(seeds=tuple(args.seeds), config=config)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "config.json").write_text(
        json.dumps({
            "baseline_revision": "e0f308f5aa76cdf41578f0574a2135b9bb0b256d",
            "config": asdict(config),
            "seeds": args.seeds,
        }, indent=2, sort_keys=True)
    )
    (args.output / "results.json").write_text(
        json.dumps([asdict(result) for result in results], indent=2, sort_keys=True)
    )
    for result in results:
        metrics = result.metrics
        print(
            f"{metrics.policy} seed={metrics.seed} shortcut={metrics.shortcut_selected} "
            f"accepted={metrics.accepted_additions} rejected={metrics.rejection_reasons} "
            f"delay={metrics.shortest_path_delay_after} events={metrics.after.event_count}"
        )


if __name__ == "__main__":
    main()