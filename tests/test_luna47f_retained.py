"""Checks of retained Luna-47F results; never execute a production run."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT/"artifacts/luna47f/diagnostic.json"


@pytest.fixture(scope="module")
def result():
    if not OUTPUT.exists():
        pytest.skip("Outcome not generated: commit protocol/code before retained scoring.")
    return json.loads(OUTPUT.read_bytes())


def test_replay_and_nonmutation_manifest(result):
    assert result["replay_equal"]
    assert result["non_mutation"]["pre"] == result["non_mutation"]["post"]
    assert result["non_mutation"]["protected_tracked_files"] == len(result["non_mutation"]["pre"])
    encoded = json.dumps(result["analysis"], sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode()
    assert hashlib.sha256(encoded).hexdigest() == result["analysis_sha256"]


def test_causal_rows_are_reconciled_to_exact_retained_observations(result):
    phase_path = result["trace_roles"]["initial"]["phase"]
    phase = json.loads((ROOT/phase_path).read_bytes())

    def resolve(pointer):
        value = phase
        for piece in pointer.strip("/").split("/"):
            value = value[int(piece)] if isinstance(value, list) else value[piece]
        return value

    for row in result["analysis"]["rows"]:
        assert row["candidate_time"] == row["target"]["time"]
        assert row["source"]["time"] < row["target"]["time"]
        assert row["lag"] == row["target"]["time"]-row["source"]["time"]
        for role in ("source", "target"):
            original = resolve(row[role]["json_pointer"])
            assert row[role+"_delta"] == original.get("payload", original.get("input_value"))
        a, b = row["source_delta"], row["target_delta"]
        similarity = min(abs(a), abs(b))/max(abs(a), abs(b)) if a and b else None
        assert similarity == row["delta_similarity"]
        compatible = bool(a and b and (a > 0) == (b > 0) and similarity >= 0.5)
        assert compatible == row["delta_compatible"]
        assert row["opportunity"] == (compatible and 0 < row["lag"] <= 4.0)
        chain = row["causal_chain"]
        assert all(chain[i]["time"] < chain[i+1]["time"] for i in range(len(chain)-1))
        for observation in [*chain, row["source"], row["target"]]:
            original = resolve(observation["json_pointer"])
            timestamp = original.get("timestamp", original.get("reception_timestamp"))
            assert timestamp == observation["time"]
            if "event_id" in original:
                assert original["event_id"] == observation["event_id"]
            if "roots_truncated" in original:
                assert original["roots_truncated"] == observation["roots_truncated"]


def test_opportunity_is_not_intrinsic_compatibility_or_usable_edge(result):
    analysis = result["analysis"]
    assert analysis["verdict"] in ("PARTIALLY SUPPORTED", "NOT SUPPORTED")
    assert "source_intrinsic_state_delta_compatibility" in analysis["blocked_metrics"]
    assert "source_local_candidate_availability" in analysis["blocked_metrics"]
    for row in analysis["rows"]:
        assert row["classification"]["usable_edge"] is None
        assert row["classification"]["local_observation_availability"] == "BLOCKED"
        assert row["classification"]["prospective_delay_reduction"] is None
        if row["target"]["node"] == "destination":
            assert not row["target_canonical_emission_association"]


def test_family_totals_do_not_pool_overlapping_chains(result):
    analysis = result["analysis"]
    for family, summary in analysis["summary"].items():
        rows = [r for r in analysis["rows"] if r["family"] == family]
        opportunities = [r for r in rows if r["opportunity"]]
        assert len(rows) == summary["enumerated_pairs"]
        assert len(opportunities) == summary["candidate_opportunities"]
        assert sum(r["classification"]["existing_edge_duplicate"] for r in opportunities) == summary["existing_edge_duplicates"]
        assert sum(r["repeated_endpoint_proposal"] for r in opportunities) == summary["repeated_endpoint_proposals"]
    # Static capacity is not consumed by repeated hypothetical proposals.
    novel = [r for r in analysis["rows"] if r["classification"]["capacity_feasible_novel"]]
    assert all(not any(r["classification"]["saturated"].values()) for r in novel)


def test_reproduction_check_is_read_only(result):
    before = OUTPUT.read_bytes()
    run = subprocess.run([sys.executable, str(ROOT/"experiments/luna47f/diagnostic.py"), "--check"],
                         cwd=ROOT, capture_output=True, text=True, timeout=180)
    assert run.returncode == 0, run.stdout + run.stderr
    assert OUTPUT.read_bytes() == before
