"""Frozen pre-outcome tests, using independent equation/count oracles."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
import math
import subprocess

import pytest

from experiments.luna47d.model import (Config, canonical, load_fixtures, reconcile,
                                      scientific_failures, simulate)
import experiments.luna47d.run as luna47d_run
from experiments.luna47d.run import analyze, negative_controls

FIXTURES = load_fixtures()


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda f: f["id"])
def test_frozen_regime_count_identity_return_and_replay(fixture):
    result = simulate(fixture)
    assert not scientific_failures(result)
    assert reconcile(result)
    assert canonical(result) == canonical(simulate(fixture))
    assert result["metrics"]["output_count"] == fixture["expected_count"]
    assert result["metrics"]["recovery_delay"] <= 144
    assert result["metrics"]["final_abs_state"] <= 1e-6
    assert result["metrics"]["max_abs_state"] <= 32
    assert result["metrics"]["opportunity_count"] <= 128
    assert result["metrics"]["pending_at_horizon"] is None
    assert [m["input_id"] for m in result["reconciliation"]] == [e["id"] for e in fixture["inputs"]]
    for mapping in result["reconciliation"]:
        assert mapping["output_ids"] == [o["id"] for o in result["outputs"]
                                        if mapping["input_id"] in o["contributors"]]
    for ordinal, output in enumerate(result["outputs"]):
        assert output["id"] == f'{fixture["id"]}/out/{ordinal}'
        assert output["sign"] == fixture["polarity"]


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda f: f["id"])
def test_every_continuous_segment_and_drain_has_analytic_oracle(fixture):
    result = simulate(fixture)
    input_by_id = {e["id"]: e for e in fixture["inputs"]}
    previous, time = 0.0, Fraction(0)
    for row in result["trace"]:
        t = Fraction(row["time"])
        assert t >= time
        assert row["previous_state"] == previous
        assert row["previous_time"] == str(time)
        expected_pre = previous * math.exp(-0.125 * float(t - time))
        assert row["pre"] == pytest.approx(expected_pre, rel=1e-12, abs=1e-12)
        if row["kind"] == "input":
            expected_post = expected_pre + input_by_id[row["id"]]["drive"]
        elif row["output_id"]:
            assert abs(expected_pre) >= 1  # exact threshold
            expected_post = math.copysign(max(0, abs(expected_pre) - 4), expected_pre)
            assert abs(expected_post) < abs(expected_pre)
        else:
            expected_post = expected_pre
        assert row["post"] == pytest.approx(expected_post, rel=1e-12, abs=1e-12)
        previous, time = row["post"], t


@pytest.mark.parametrize("charge,count", [(1, 0), (1.01, 0), (1.25, 1), (2.5, 1),
                                         (8, 2), (12, 3), (32, 7)])
def test_isolated_burst_independent_count_and_exact_time_oracle(charge, count):
    fixture = {"id": "oracle", "family": "oracle", "polarity": 1,
               "inputs": [{"id": "i0", "time": "0", "drive": charge}], "expected_count": count}
    result = simulate(fixture)
    # Independent closed-form recurrence before the kth saturated drain.
    a = math.exp(-0.125 * 0.5)
    expected = []
    for k in range(1, 33):
        before = a**k * charge - 4 * a * (1 - a**(k - 1)) / (1 - a)
        if before < 1:
            break
        expected.append(str(Fraction(k, 2)))
        if before <= 4:
            break
    assert len(expected) == count
    assert [o["time"] for o in result["outputs"]] == expected


def select(family, polarity=1):
    return deepcopy(next(f for f in FIXTURES if f["family"] == family and f["polarity"] == polarity))


def test_cluster_compression_reconciles_three_distinct_inputs_to_one_output():
    fixture = select("moderate-cluster")
    result = simulate(fixture)
    assert result["outputs"][0]["contributors"] == [e["id"] for e in fixture["inputs"]]
    assert [m["output_ids"] for m in result["reconciliation"]] == [
        [result["outputs"][0]["id"]]] * 3
    expected_charge = sum(1.25 * math.exp(-0.125 * float(Fraction(1, 2) - Fraction(e["time"])))
                          for e in fixture["inputs"])
    due = next(r for r in result["trace"] if r["kind"] == "opportunity")
    assert due["pre"] == pytest.approx(expected_charge, abs=1e-12, rel=1e-12)
    assert due["post"] == 0
    assert result["metrics"]["recovery_time"] == 0.5


def test_exact_threshold_no_tolerance_and_leak_before_output_negative():
    result = simulate(select("threshold-boundary"))
    assert result["metrics"]["opportunity_count"] == 1
    assert result["outputs"] == []
    assert result["trace"][1]["decision"] == "below-threshold-no-output"
    assert result["trace"][1]["pre"] < 1
    assert result["metrics"]["exact_zero_final"] is False
    assert result["metrics"]["recovery_time"] == pytest.approx(math.log(1 / 1e-6) / 0.125)


@pytest.mark.parametrize("period", ["2/4", "0.5"])
def test_equivalent_period_encoding_passes_latency_check(period):
    result = simulate(select("moderate-low"), replace(Config(), period=period))
    assert not scientific_failures(result)


def test_subthreshold_recovery_is_leak_not_reset():
    result = simulate(select("subthreshold"))
    assert len(result["trace"]) == 2
    assert result["trace"][-1]["post"] == 0.5 * math.exp(-0.125 * 144)
    assert result["metrics"]["recovery_delay"] == pytest.approx(math.log(0.5 / 1e-6) / 0.125)


def test_due_time_tie_admits_input_first():
    fixture = select("moderate-low")
    fixture["inputs"].append({"id": "at-due", "time": "1/2", "drive": 1.25})
    result = simulate(fixture)
    assert [r["kind"] for r in result["trace"][:3]] == ["input", "input", "opportunity"]
    assert result["outputs"][0]["contributors"][-1] == "at-due"


def test_prefix_causality_and_reset_without_shared_state():
    fixture = select("separated-moderate")
    prefix = deepcopy(fixture)
    prefix["inputs"] = prefix["inputs"][:1]
    prefix["expected_count"] = 1
    full = simulate(fixture)
    first = simulate(prefix)
    assert full["outputs"][:1] == first["outputs"]
    assert simulate(select("idle"))["outputs"] == []
    assert canonical(first) == canonical(simulate(prefix))


def test_same_time_cancellation_and_empty_idle_have_no_idle_ticks():
    result = simulate(select("cancellation"))
    assert result["outputs"] == []
    assert result["trace"][1]["post"] == 0
    assert result["metrics"]["recovery_time"] == 0
    idle = simulate(select("idle"))
    assert len(idle["trace"]) == 1
    assert idle["metrics"]["opportunity_count"] == 0
    assert idle["metrics"]["recovery_time"] == 0
    assert idle["metrics"]["recovery_delay"] == 0


@pytest.mark.parametrize("cfg", [
    replace(Config(), leak=0), replace(Config(), leak=-1), replace(Config(), period="0"),
    replace(Config(), quantum=0), replace(Config(), quantum=0.5),
    replace(Config(), theta=0), replace(Config(), epsilon=0),
    replace(Config(), tail="1"), replace(Config(), leak=float("nan")),
    replace(Config(), quantum=float("inf")), replace(Config(), period="2"),
])
def test_reject_self_sustaining_unbounded_or_nonrecovering_parameter_domains(cfg):
    with pytest.raises(ValueError):
        simulate(select("moderate-low"), cfg)


@pytest.mark.parametrize("mutation", ["duplicate", "late", "overdrive", "nonfinite", "capacity", "time"])
def test_invalid_input_domains_reject_not_clip(mutation):
    fixture = select("moderate-cluster")
    if mutation == "duplicate":
        fixture["inputs"][1]["id"] = fixture["inputs"][0]["id"]
    elif mutation == "late":
        fixture["inputs"][1]["time"] = "-1"
    elif mutation == "overdrive":
        fixture["inputs"][0]["drive"] = 33
    elif mutation == "nonfinite":
        fixture["inputs"][0]["drive"] = float("inf")
    elif mutation == "capacity":
        fixture["inputs"] = [{"id": str(i), "time": "0", "drive": 0} for i in range(17)]
    else:
        fixture["inputs"][0]["time"] = "65"
    with pytest.raises(ValueError):
        simulate(fixture)


@pytest.mark.parametrize("mutation", ["missing-output", "renamed-output", "time", "input", "mapping"])
def test_exact_identity_replay_detects_missing_events_not_compression(mutation):
    result = simulate(select("moderate-cluster"))
    if mutation == "missing-output":
        result["outputs"].clear()
    elif mutation == "renamed-output":
        result["outputs"][0]["id"] = "other"
    elif mutation == "time":
        result["outputs"][0]["time"] = "5000000000001/10000000000000"
    elif mutation == "input":
        result["trace"][0]["id"] = "other"
    else:
        result["reconciliation"][0]["output_ids"].clear()
    with pytest.raises(ValueError, match="replay mismatch"):
        reconcile(result)


def test_negative_controls_preserve_failure_and_explicit_rejection():
    controls = negative_controls([simulate(f) for f in FIXTURES])
    assert len(controls) == 13
    assert all(c["detected"] for c in controls)
    weak = [c for c in controls if c["type"] == "real-alternate-configuration"]
    assert len(weak) == 2
    assert all(c["result"]["metrics"]["output_count"] == 3 for c in weak)
    assert all("count/compression-regime" in c["failures"] for c in weak)
    sustaining = next(c for c in controls if c["id"] == "self-sustaining-output")
    assert "output-after-neutral/self-sustaining" in sustaining["failures"]
    overflow = next(c for c in controls if c["id"] == "output-budget-overflow")
    assert "unbounded-output-count" in overflow["failures"]
    state = next(c for c in controls if c["id"] == "state-overflow")
    assert "unbounded-state" in state["failures"]
    recovery = next(c for c in controls if c["id"] == "failed-recovery")
    assert "loss-of-bounded-neutral-recovery" in recovery["failures"]


def test_nondissipative_mutant_cannot_be_reported_as_truncated_success(monkeypatch):
    # Deliberately bypass admission validation to exercise runtime guard failure,
    # NOT a legal parameter condition and NOT an observation of the primary model.
    monkeypatch.setattr(Config, "validate", lambda self: None)
    with pytest.raises(RuntimeError, match="output budget exceeded"):
        simulate(select("moderate-low"), replace(Config(), quantum=0, leak=0))
    with pytest.raises(RuntimeError, match="opportunity watchdog"):
        simulate(select("moderate-low"), replace(Config(), theta=0.01, quantum=0, leak=0))


def test_primary_symmetry_and_full_initial_replay():
    analysis = analyze()
    assert analysis["verdict"] == "SUPPORTED"
    assert all(s["pass"] for s in analysis["symmetry"])
    assert analysis["initial_sha256"] == analysis["replay_sha256"]
    assert analysis["replay_byte_equal"]
    assert sum(r["metrics"]["output_count"] for r in analysis["initial"]) == 40


def test_source_manifest_rejects_mismatched_revision_checkout(tmp_path, monkeypatch):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"],
                   cwd=tmp_path, check=True)
    source = tmp_path / "source.py"
    source.write_bytes(b"committed\r\n")
    subprocess.run(["git", "add", "source.py"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=tmp_path, check=True)
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True
    ).strip()
    source.write_bytes(b"working tree\n")
    monkeypatch.setattr(luna47d_run, "ROOT", tmp_path)
    monkeypatch.setattr(luna47d_run, "SOURCES", ["source.py"])

    with pytest.raises(ValueError, match="checkout source differs"):
        luna47d_run.source_manifest(revision)
