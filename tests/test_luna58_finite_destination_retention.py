"""Acceptance checks for the published Luna-58 bounded mechanism run."""

from __future__ import annotations

import json
from pathlib import Path

from experiments.luna54 import run as luna54
from experiments.luna55 import run as luna55
from experiments.luna58 import run as luna58


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "luna58"


def _record(name: str) -> dict:
    return json.loads((OUTPUT / name).read_text(encoding="utf-8"))


def _route_signature(row: dict) -> list[tuple]:
    return [
        luna55._route_signature(event, "reception_timestamp")
        for event in row["destination_receptions"]
    ]


def test_luna58_phase_and_summary_artifact_digests_are_valid() -> None:
    result = luna58.verify_artifacts()
    assert result["status"] == "PASS"
    assert result["all_artifact_digests_valid"] is True
    assert result["phase_artifacts"] == [
        "rr-control-initial",
        "rr-control-replay",
        "finite-initial",
        "finite-replay",
    ]


def test_only_finite_destination_decay_changes_and_runtime_bounds_are_frozen() -> None:
    control = _record("rr-control-initial.json")
    intervention = _record("finite-initial.json")
    assert luna54._diff_paths(
        control["configuration"], intervention["configuration"]
    ) == ["destination.integration.decay_rate_z"]
    assert control["configuration"]["relay"] == intervention["configuration"]["relay"]
    assert control["configuration"]["relay"]["integration"]["decay_rate_z"] == 0.00125
    assert control["configuration"]["destination"]["integration"]["decay_rate_z"] == 0.00125
    assert intervention["configuration"]["destination"]["integration"]["decay_rate_z"] == 0.00001
    for name in ("rr-control-initial.json", "rr-control-replay.json",
                 "finite-initial.json", "finite-replay.json"):
        phase = _record(name)
        assert phase["stream_count"] == 320
        assert phase["source_input_phase_digest"] == (
            "d73c99d83847b50bb5cb66920b95c3546d818874f582b6b6d9d8c5bfa90aaa3b"
        )
        assert phase["resource_bounds"]["queue_capacity"] == 128
        assert phase["resource_bounds"]["runtime_event_budget"] == 1024
        assert phase["resource_bounds"]["per_neuron_event_budget"] == 4096
        assert phase["resource_bounds"]["settling_horizon"] == 4.0
        assert phase["resource_bounds"]["pending_events"] == 0
        assert phase["resource_bounds"]["bound_failures"] == 0
        assert phase["resource_bounds"]["clipping_events"] == 0
        assert phase["labels_entered_runtime"] is False


def test_all_421_routes_reproduce_and_intervention_is_route_invariant() -> None:
    summary = _record("summary.json")
    for phase in ("initial", "replay"):
        frozen = _record(f"rr-control-{phase}.json")
        changed = _record(f"finite-{phase}.json")
        retained = json.loads(
            (ROOT / "artifacts" / "luna55" / f"rr-{phase}.json").read_text()
        )
        frozen_rows = {row["stream_id"]: row for row in frozen["streams"]}
        changed_rows = {row["stream_id"]: row for row in changed["streams"]}
        retained_rows = {row["stream_id"]: row for row in retained["streams"]}
        assert set(frozen_rows) == set(changed_rows) == set(retained_rows)
        assert sum(len(row["destination_receptions"]) for row in frozen_rows.values()) == 421
        for stream_id, row in frozen_rows.items():
            assert row["source_inputs"] == retained_rows[stream_id]["source_inputs"]
            assert row["relay_emissions"] == retained_rows[stream_id]["relay_emissions"]
            assert _route_signature(row) == _route_signature(retained_rows[stream_id])
            assert changed_rows[stream_id]["source_inputs"] == row["source_inputs"]
            assert changed_rows[stream_id]["relay_emissions"] == row["relay_emissions"]
            assert _route_signature(changed_rows[stream_id]) == _route_signature(row)
            assert (
                changed_rows[stream_id]["roots_truncated_count"]
                == row["roots_truncated_count"]
            )
        assert summary["route_reconciliation"][f"rr-control-{phase}"]["passed"] is True
        assert summary["route_reconciliation"][f"finite-{phase}"]["passed"] is True
        assert summary["route_reconciliation"][f"finite-{phase}"][
            "destination_route_signatures_exact"
        ] == 421
        assert frozen["root_truncation_stream_ids"] == [
            "c00-019", "c00-059", "c01-006", "c01-008", "c01-035", "c02-058", "c04-046"
        ]
        assert changed["root_truncation_stream_ids"] == frozen["root_truncation_stream_ids"]


def test_six_rescues_controls_and_observed_first_crossings() -> None:
    summary = _record("summary.json")
    acceptance = summary["acceptance"]
    assert acceptance["status"] == "PASS"
    assert acceptance["initial_replay_identical"] is True
    assert acceptance["all_six_primary_nonresponders_crossed"] is True
    assert acceptance["all_ten_rr_positive_controls_crossed"] is True
    assert acceptance["specified_negative_controls_zero"] is True
    groups = summary["strata"]
    assert groups["primary_rr_nonresponders"]["stream_count"] == 6
    assert groups["primary_rr_nonresponders"]["crossings"] == 6
    assert groups["primary_rr_responders"]["stream_count"] == 10
    assert groups["primary_rr_responders"]["crossings"] == 10
    for name, count in (
        ("Eplus_zero_decay_insufficient", 49),
        ("E0_no_additional_arrival", 10),
        ("NR1_upstream_active_no_historical_reception", 189),
        ("NR0_no_input", 23),
    ):
        assert groups[name]["stream_count"] == count
        assert groups[name]["crossings"] == 0
    assert groups["secondary_temporal_retention"]["stream_count"] == 33
    assert groups["secondary_temporal_retention"]["crossings"] == 33

    finite = _record("finite-initial.json")
    finite_rows = {row["stream_id"]: row for row in finite["streams"]}
    target_rows = summary["primary_targets_frozen_order"]
    assert [row["stream_id"] for row in target_rows] == list(luna55.TARGET_IDS)
    nonresponders = {
        row["stream_id"] for row in target_rows if not row["rr_baseline_crossed"]
    }
    assert nonresponders == {
        "c00-011", "c00-037", "c01-020", "c02-015", "c02-023", "c02-046"
    }
    for target in target_rows:
        stream = finite_rows[target["stream_id"]]
        discharge = next(
            trace for trace in stream["destination_integration_traces"]
            if float(trace["discharge_amount"]) != 0.0
        )
        observed = target["first_crossing"]
        assert target["intervention_crossed"] is True
        assert observed["timestamp"] == discharge["timestamp"]
        assert observed["signed_input"] == discharge["input_value"]
        assert observed["pre_addition_z"] == discharge["z_after_decay"]
        assert observed["post_discharge_z"] == discharge["z_post_discharge"]
    for condition in ("rr-control", "finite"):
        initial = _record(f"{condition}-initial.json")
        replay = _record(f"{condition}-replay.json")
        assert initial["streams"] == replay["streams"]
