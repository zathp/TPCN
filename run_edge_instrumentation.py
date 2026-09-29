"""Generate the bounded Luna-12M edge lifecycle diagnostic artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tpcn.edge_instrumentation import run_competing_path_fixture


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/edge-instrumentation-12m")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    enabled = run_competing_path_fixture(instrument=True)
    disabled = run_competing_path_fixture(instrument=False)
    artifact = {"schema_version": enabled["schema_version"], "enabled": enabled,
                "non_interference": {"traces_equal": enabled["traces"] == disabled["traces"],
                                      "digests_equal": enabled["digests"] == disabled["digests"],
                                      "mutations_equal": enabled["mutations"] == disabled["mutations"]}}
    (output / "edge_lifecycle.json").write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {"schema_version": enabled["schema_version"], "edges": enabled["edges"],
               "competing_paths": enabled["analysis"], "mutations": enabled["mutations"],
               "phases": enabled["phases"], "traffic": enabled["traffic"],
               "rejection_results": enabled["rejection_results"],
               "rejection_records": [record for record in enabled["lifecycle"]
                                     if record["kind"] == "candidate_rejected"],
               "decay_context_records": len(enabled["decay_context"]),
               "persistent_strength": "not available in current architecture",
               "persistent_utility": "not available in current architecture"}
    (output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": str(output / "edge_lifecycle.json"), "summary": str(output / "summary.json"),
                      "non_interference": artifact["non_interference"]}, sort_keys=True))


if __name__ == "__main__":
    main()