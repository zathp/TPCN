from __future__ import annotations

import json
from pathlib import Path

import pytest

import run_luna34_excursion_v1_multi_emitter_bridge as base
import run_luna37_excursion_v1_propagation_emission_diagnostic as luna37
from tpcn.stroke_dataset import StrokePoint


def _points() -> tuple[StrokePoint, ...]:
    return (StrokePoint(0.6, 0.6, timestamp=0.0),)


def _record(condition: str, points=None) -> dict:
    return luna37._character_record(
        seed=0, sequence_index=0, condition=condition, points=points or _points()
    )


def test_explicit_capacity_reaches_both_ledgers_and_reconciles() -> None:
    for condition in luna37.CONDITIONS:
        record = _record(condition)
        assert record["eligibility"]["runtime_property_capacity"] == 1024
        ledgers = record["eligibility"]["ledgers"]
        assert len(ledgers) == 2
        assert all(item["configured_capacity"] == 1024 for item in ledgers)
        assert all(item["reconciles"] and item["peak_occupancy"] < 1024 for item in ledgers)
        assert all(
            item["initial_occupancy"] + item["created"] - item["removed"] == item["final_occupancy"]
            for item in ledgers
        )


def test_previous_blocker_character_no_longer_overflows_at_declared_capacity() -> None:
    points = base._training_point_sequences(0)[4]
    record = luna37._character_record(
        seed=0, sequence_index=4, condition="NO_EDGE_CONTROL", points=points
    )
    source = [item for item in record["eligibility"]["ledgers"] if item["ledger_id"].endswith("source")][0]
    assert source["created"] == source["peak_occupancy"] == 18 > 16
    assert record["eligibility"]["capacity_errors"] == []


def test_no_edge_control_has_no_transfer_or_destination_activity() -> None:
    record = _record("NO_EDGE_CONTROL")
    counts = record["mechanism_counts"]
    assert record["edge"] is None
    assert counts["routed_transfers"] == counts["destination_receptions"] == 0
    assert counts["destination_canonical_emissions"] == 0
    assert counts["source_canonical_emissions"] > 0
    assert record["no_edge_contaminated"] is False


def test_emission_is_separate_from_reception_and_state_change() -> None:
    record = _record("STATIC_N2_BOUND_SENSITIVITY")
    counts = record["mechanism_counts"]
    assert counts["destination_receptions"] == counts["routed_transfers"] > 0
    assert counts["destination_state_changes"] > 0
    destination = [e for e in record["canonical_emissions"] if e["emitter_id"] == "destination"]
    assert counts["destination_canonical_emissions"] == len(destination)
    assert counts["destination_canonical_emissions"] < counts["destination_receptions"]


def test_labels_do_not_reach_records() -> None:
    text = json.dumps(_record("DEFAULT_STATIC_EDGE"))
    assert "label" not in text
    assert base._training_point_sequences(0)[0][0].__class__ is StrokePoint


def test_capacity_error_is_a_stop_condition(monkeypatch) -> None:
    monkeypatch.setattr(luna37, "ELIGIBILITY_CAPACITY", 1)
    with pytest.raises(luna37.StopCondition):
        luna37._character_record(
            seed=0, sequence_index=4, condition="NO_EDGE_CONTROL",
            points=base._training_point_sequences(0)[4],
        )


def test_deterministic_and_artifacts_complete(tmp_path: Path) -> None:
    _, summary = luna37.run_experiment(tmp_path, seeds=(0,))
    assert summary["deterministic_replay"]["equal"] is True
    assert summary["design_counts"]["character_condition_executions"] == 192
    assert summary["eligibility_capacity"] == 1024
    for name in ("config.json", "results.json", "summary.json"):
        assert (tmp_path / name).is_file()
    config = json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))
    assert config["network"]["eligibility_capacity"]["value"] == 1024
    assert config["network"]["eligibility_capacity"]["tuned"] is False
