"""Focused recurrence, domain, exact ordering, replay and evidence tests."""
from copy import deepcopy
from decimal import Decimal, localcontext
import math

import pytest

from experiments.luna47a import run as lane

RATES = tuple(lane.CONFIG["rates"].values())


def updates(events):
    previous = 0.0
    rows = []
    for i, (t, u) in enumerate(events):
        rows.append({"timestamp": t, "prior_clock": previous, "queue_sequence": i,
                     "event_id": f"test:{i}", "payload": u, "is_reception": True})
        previous = t
    return rows


@pytest.mark.parametrize("rate", RATES)
@pytest.mark.parametrize("dt", [0.0, 1e-12, 0.125, 80.0, 8000.0, 1e12])
def test_continuous_target_high_precision(rate, dt):
    observed = lane.step(0.75, dt, -0.125, rate)
    with localcontext() as context:
        context.prec = 90
        exponent = -Decimal.from_float(rate) * Decimal.from_float(dt)
        target = float(Decimal("0.75") * exponent.exp() - Decimal("0.125"))
    assert lane.evidence.checked(observed["state_after"], target, "Decimal CT target")["matches"]
    assert observed["rho"] == math.exp(-rate * dt)


@pytest.mark.parametrize("rate", RATES)
@pytest.mark.parametrize("left,right", [(0.0, 80.0), (0.125, 80.0), (80.0, 800.0), (1e12, 0.0)])
def test_event_time_semigroup(rate, left, right):
    split = lane.step(lane.step(0.75, left, 0, rate)["state_after"], right, 0, rate)["state_after"]
    whole = lane.step(0.75, left + right, 0, rate)["state_after"]
    assert lane.evidence.checked(split, whole, "analytical semigroup")["matches"]


@pytest.mark.parametrize("rate", RATES)
def test_signed_recurrence_and_reset(rate):
    rows = updates([(0.0, 0.6), (80.0, 0.6), (81.0, -0.4)])
    result = lane.accumulate(rows, rate)
    expected = 0.0
    for source, observed in zip(rows, result["rows"]):
        expected = expected * math.exp(-rate * (source["timestamp"] - source["prior_clock"])) + source["payload"]
        assert observed["state_after"] == expected
    assert lane.accumulate(rows, rate) == result
    assert lane.accumulate(updates([(0.0, -0.4)]), rate)["rows"][0]["state_before"] == 0


@pytest.mark.parametrize("payload", [1.0, -1.0, math.nextafter(1.0, 0.0), -math.nextafter(1.0, 0.0)])
def test_threshold_exact_no_tolerance(payload):
    row = lane.step(0, 0, payload, RATES[0])
    assert row["crosses"] == (abs(payload) >= 1)
    assert row["threshold_margin"] == abs(payload) - 1


@pytest.mark.parametrize("rate", RATES)
def test_sign_cancellation_not_absolute_accumulation(rate):
    result = lane.accumulate(updates([(0.0, 0.75), (0.0, -0.75)]), rate)
    assert result["rows"][-1]["state_after"] == 0
    assert not result["crosses"]


def test_equal_time_order_and_noncommutativity():
    equal = lane.accumulate(updates([(0.0, 0.6), (0.0, 0.6)]), RATES[0])
    assert equal["rows"][1]["dt"] == 0 and equal["rows"][1]["state_after"] == 1.2
    left = lane.accumulate(updates([(0.0, 0.75), (80.0, -0.25)]), RATES[0])
    right = lane.accumulate(updates([(0.0, -0.25), (80.0, 0.75)]), RATES[0])
    assert left["rows"][-1]["state_after"] != right["rows"][-1]["state_after"]
    bad = updates([(0.0, 0.6), (0.0, 0.6)])
    bad[1]["queue_sequence"] = bad[0]["queue_sequence"]
    with pytest.raises(lane.evidence.Blocked, match="queue"):
        lane.accumulate(bad, RATES[0])


def test_intervening_update_and_zero_deposition():
    rows = updates([(0.0, 0.75), (40.0, 123.0), (80.0, 0.1)])
    rows[1]["is_reception"] = False
    result = lane.accumulate(rows, RATES[0])
    assert result["rows"][1]["payload"] == 0
    expected = 0.75 * math.exp(-RATES[0] * 80) + 0.1
    assert lane.evidence.checked(result["rows"][-1]["state_after"], expected, "intervening")["matches"]
    bad = deepcopy(rows)
    bad[2]["prior_clock"] = 0
    with pytest.raises(lane.evidence.Blocked, match="continuity"):
        lane.accumulate(bad, RATES[0])


@pytest.mark.parametrize("rate", RATES)
@pytest.mark.parametrize("payload", [1e6, -1e6])
def test_capacity_and_extreme_values(rate, payload):
    rows = updates([(0.0, payload)] * 4096)
    result = lane.accumulate(rows, rate)
    assert all(abs(r["state_after"]) <= 4 and math.isfinite(r["state_after"]) for r in result["rows"])
    assert result["clipped_events"] == 4096
    assert lane.step(result["rows"][-1]["state_after"], 1e12, 0, rate)["state_after"] == 0
    with pytest.raises(lane.evidence.Blocked, match="capacity"):
        lane.accumulate(rows + [rows[-1]], rate)


@pytest.mark.parametrize("field,value", [
    ("timestamp", float("nan")), ("timestamp", float("inf")),
    ("timestamp", -1), ("timestamp", 1e12 + 1),
    ("payload", 1e6 + 1), ("payload", float("-inf")),
    ("payload", True), ("prior_clock", -1),
])
def test_unsupported_domain_rejected(field, value):
    rows = updates([(0.0, 0.5)])
    rows[0][field] = value
    with pytest.raises(lane.evidence.Blocked):
        lane.accumulate(rows, RATES[0])


def test_undeclared_rate_and_negative_elapsed():
    for kwargs in (dict(rate=0), dict(rate=-1), dict(dt=-1), dict(previous=4.1)):
        args = dict(previous=0, dt=0, payload=0.1, rate=RATES[0])
        args.update(kwargs)
        with pytest.raises(lane.evidence.Blocked):
            lane.step(**args)


@pytest.mark.parametrize("rescues,drive,gate,expected", [
    ([33, 33], 0, True, "SUPPORTED"), ([0, 33], 0, True, "SUPPORTED"),
    ([1, 32], 0, True, "PARTIALLY SUPPORTED"),
    ([0, 0], 0, True, "NOT SUPPORTED"), ([33, 33], 1, True, "BLOCKED"),
    ([33, 33], 0, False, "BLOCKED"),
])
def test_verdict_boundaries(rescues, drive, gate, expected):
    assert lane.classify(33, rescues, drive, gate) == expected
    assert lane.classify(0, rescues, drive, gate) == "BLOCKED"


def test_no_receptions_and_drive_negative():
    empty = lane.compare({"stream_id": "empty", "updates": [], "category": "NO-RECEPTIONS"})
    assert all(v["maximum_absolute_state"] == 0 and not v["crosses"] for v in empty["variants"].values())
    for rate in RATES:
        assert not lane.accumulate(updates([(0.0, 0.4), (0.0, 0.3)]), rate)["crosses"]


def test_no_gain_change_and_qualification_identity():
    rows = updates([(0.0, 0.6), (80.0, 0.6)])
    stream = {"stream_id": "retention", "updates": rows, "category": "TEMPORAL-RETENTION-LIMITED"}
    result = lane.compare(stream)
    assert not result["variants"]["baseline_tau80"]["crosses"]
    assert result["variants"]["retention_tau800"]["crosses"]
    for variant in result["variants"].values():
        assert [r["payload"] for r in variant["rows"]] == [0.6, 0.6]
        assert all(abs(r["state_after"]) <= 4 for r in variant["rows"])


def test_exact_deterministic_canonical_replay_and_nonmutation():
    rows = updates([(0.0, 0.6), (0.0, -0.1), (80.0, 0.6)])
    stream = {"stream_id": "test", "updates": rows}
    original = deepcopy(stream)
    assert lane.evidence.canonical(lane.compare(stream)) == lane.evidence.canonical(lane.compare(stream))
    assert stream == original


def test_owned_output_alias_and_protected_paths(tmp_path, monkeypatch):
    monkeypatch.setattr(lane, "ROOT", tmp_path)
    own = tmp_path / "artifacts/luna47a"
    assert lane.output_directory(own) == own
    for path in (tmp_path, tmp_path / "artifacts/luna46-analysis.json",
                 own / "../../outside", tmp_path / "tpcn"):
        with pytest.raises(lane.evidence.Blocked, match="namespace"):
            lane.output_directory(path)


def test_corrupt_retained_pin():
    with pytest.raises(lane.evidence.Blocked, match="pin"):
        lane.verify_retained(b"{}", b"{}")


def test_git_byte_adapter_preserves_exact_integrity():
    pin = lane.materialization_check(b'{"x":1}\r\n', b'{"x":1}\n')
    assert not pin["physical_equals_git"] and pin["exact_lf_crlf_equivalence"]
    assert pin["physical_sha256"] != pin["git_sha256"]
    assert lane.materialization_check(b'{"x":1}\n', b'{"x":1}\n')["physical_equals_git"]
    with pytest.raises(lane.evidence.Blocked, match="beyond"):
        lane.materialization_check(b'{"x":2}\r\n', b'{"x":1}\n')


def test_authoritative_git_evidence_integrity_only():
    source, observations = lane.materialize_evidence()
    integrity = lane.evidence.verify_integrity(source)
    assert integrity["status"] == "PASS" and len(integrity["inputs"]) == 33
    assert len(observations) == 34
    assert all(row["physical_equals_git"] or row["exact_lf_crlf_equivalence"]
               for row in observations.values())
    inventory = lane.physical_inventory(observations)
    assert all(inventory[name]["sha256"] == row["physical_sha256"]
               for name, row in observations.items())
    retained = (source / lane.RETAINED).read_bytes()
    assert lane.verify_retained(retained, retained)["verdict"] == "MIXED"


def test_write_new_exact_and_never_overwrite(tmp_path):
    target = tmp_path / "test.json"
    value = {"state": 0.125}
    identity = lane.write_new(target, value)
    assert target.read_bytes() == lane.evidence.canonical(value) + b"\n"
    assert lane.evidence.sha(target.read_bytes()) == identity["sha256"]
    with pytest.raises(lane.evidence.Blocked, match="overwrite"):
        lane.write_new(target, value)


def test_fixed_synthetic_controls():
    controls = lane.synthetic_controls()
    assert len(controls) == 5
    assert lane.evidence.canonical(controls) == lane.evidence.canonical(lane.synthetic_controls())
    assert all(not c["variants"]["baseline_tau80"]["clipped_events"] for c in controls)


def test_numerical_audit_retained_measurements():
    audit = lane.numerical_audit()
    assert len(audit["targets"]) == 18 and len(audit["stress"]) == 6
    assert all(row["comparison"]["matches"] for row in audit["targets"])
    assert all(row["maximum_absolute_state"] == 4 and row["clipped_events"] == 4096
               and row["after_extreme_gap"]["state_after"] == 0 for row in audit["stress"])


def test_saved_bundle_exact_replay():
    directory = lane.ROOT / "artifacts/luna47a"
    if not (directory / "results.json").exists():
        pytest.skip("outcome bundle not generated before protocol/code commit")
    manifest = lane.evidence.read_json(directory / "manifest.json")
    for name, pin in manifest["files"].items():
        data = (directory / name).read_bytes()
        assert len(data) == pin["byte_length"]
        assert lane.evidence.sha(data) == pin["sha256"]
    inputs = lane.evidence.read_json(directory / "inputs.json")
    result = lane.analyze(inputs)
    assert lane.evidence.canonical(result) + b"\n" == (directory / "results.json").read_bytes()
