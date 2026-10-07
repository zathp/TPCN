"""Stand-in unit gates, not hardware/canonical-neuron assertions."""
import importlib.util
import gzip
import json
from pathlib import Path
import random
import sys

import pytest

PATH = Path(__file__).resolve().parents[1] / "experiments/luna47g/simulate.py"
SPEC = importlib.util.spec_from_file_location("luna47g_standin", PATH)
assert SPEC is not None and SPEC.loader is not None
model = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = model
SPEC.loader.exec_module(model)


def zero_noise():
    return {k: [0.0] * len(v) for k, v in model.FIXTURES.items()}


def test_nominal_noiseless_full_regime_chain():
    result = model.evaluate(model.nominal(), zero_noise())
    assert result["pass_"]
    assert result["failed"] == []
    assert result["transitions"] == []


def test_draw_replay_and_domains():
    for b in model.CONFIG["bands"].values():
        rng = random.Random(470601)
        for _ in range(256):
            p, units = model.draw(rng, b)
            model.validate_params(p)
            assert len(units) == 8
        assert model.draw(random.Random(123), b) == model.draw(random.Random(123), b)


def test_idle_analytic_decay_no_tick():
    p = model.nominal()
    run = model.simulate(p, [[0.0, 0.6]], [0.0])
    assert run["processed"] == 2
    assert [r["kind"] for r in run["trace"]] == [0, 2]
    assert run["final"] == pytest.approx(0.6 * model.math.exp(-20), abs=1e-15)
    assert run["neutral"]


def test_strict_future_bounded_multi_event_return():
    run = model.simulate(model.nominal(), [[0.0, 8.0]], [0.0])
    assert 2 <= len(run["outputs"]) <= 16
    assert run["return_outputs"] >= 1
    assert run["bounds"] and run["neutral"]
    assert all(r["scheduled"] is None or r["scheduled"] > r["time"] for r in run["trace"])
    assert len(run["trace"]) < 192


def test_saturation_is_reported_not_hidden():
    p = dict(model.nominal(), G=1.5, C=0.5)
    run = model.simulate(p, [[0.0, 8.0]], [0.0])
    assert run["clipped"] == 1
    assert run["peak"] == 8.0
    assert run["bounds"]


def test_mathematical_mirror_and_physical_offset_failure():
    p = dict(model.nominal(), T=0.5, O=0.1, G=1.5, N=0.12)
    noise = {k: [1.0] * len(v) for k, v in model.FIXTURES.items()}
    result = model.evaluate(p, noise)
    assert result["gates"]["mirror"] and result["gates"]["zero_offset_mirror"]
    assert not result["gates"]["noise"]
    assert result["asymmetry"]["noise"]["admission_difference"] != 0
    assert result["failed"] and result["transitions"]


def test_leakage_rc_return_failure_preserved():
    p = dict(model.nominal(), R=1.5, C=1.5, L=0.5)
    result = model.evaluate(p, zero_noise())
    assert not result["gates"]["neutral"]
    assert "neutral" in result["failed"]


def test_order_and_cancellation_not_unordered_sum():
    p = model.nominal()
    a = model.simulate(p, model.FIXTURES["order_forward"], [0.0, 0.0])
    b = model.simulate(p, model.FIXTURES["order_reverse"], [0.0, 0.0])
    assert abs(a["final"] - b["final"]) > 1e-12
    cancellation = model.simulate(p, model.FIXTURES["cancellation"], [0.0, 0.0])
    assert not cancellation["outputs"]
    assert abs(cancellation["trace"][1]["after"]) < 0.04


def test_translation_and_irregular_event_times():
    p = model.nominal()
    events = [[0.011, 0.6], [0.061, 0.6], [0.411, -0.45]]
    a = model.simulate(p, events, [0.0] * 3)
    b = model.simulate(p, events, [0.0] * 3, shift=123.0)
    assert a["admitted"] == b["admitted"]
    assert len(a["outputs"]) == len(b["outputs"])
    assert a["final"] == pytest.approx(b["final"], abs=1e-12)
    for x, y in zip(a["trace"], b["trace"]):
        assert x["after"] == pytest.approx(y["after"], abs=1e-12)
        assert x["time"] + 123 == pytest.approx(y["time"], abs=1e-12)


def test_equal_time_input_precedes_return():
    run = model.simulate(model.nominal(), [[0.0, 4.0], [0.1, -0.6]], [0.0, 0.0])
    ties = [r["kind"] for r in run["trace"] if r["time"] == 0.1]
    assert ties == [0, 1]


def test_reset_has_no_cross_fixture_state():
    p = model.nominal()
    first = model.simulate(p, [[0.0, 0.6]], [0.0])
    model.simulate(p, [[0.0, 4.0]], [0.0])
    assert first == model.simulate(p, [[0.0, 0.6]], [0.0])


@pytest.mark.parametrize("events,noise", [
    ([[0.0, float("nan")]], [0.0]), ([[1.0, 1.0], [0.0, 1.0]], [0.0, 0.0]),
    ([[-1.0, 1.0]], [0.0]), ([[0.0, 9.0]], [0.0]), ([[0.0, 1.0]], [1.1]),
    ([[0.0, 1.0]], []), ([], []), ([[0.0, 0.0]] * 129, [0.0] * 129)
])
def test_input_validation(events, noise):
    with pytest.raises(ValueError):
        model.simulate(model.nominal(), events, noise)


def test_output_budget_is_explicit(monkeypatch):
    monkeypatch.setitem(model.CONFIG, "max_outputs", 1)
    run = model.simulate(model.nominal(), [[0.0, 4.0]], [0.0])
    assert run["failure"] == "output_budget"
    assert not run["bounds"]


def test_event_budget_is_explicit(monkeypatch):
    monkeypatch.setitem(model.CONFIG, "max_processed_events", 1)
    run = model.simulate(model.nominal(), [[0.0, 4.0]], [0.0])
    assert run["failure"] == "processed_event_budget"
    assert not run["bounds"]


def test_unrepresentable_return_rejected():
    with pytest.raises(ValueError, match="strict-future"):
        model.simulate(model.nominal(), [[1e16, 4.0]], [0.0])


@pytest.mark.parametrize(("events", "shift"), [
    ([[1e20, 0.6]], 0.0),
    ([[0.0, 0.6]], 1e20),
    ([[1e308, 0.6]], 1e308),
])
def test_unrepresentable_shifted_or_terminal_time_rejected(events, shift):
    with pytest.raises(ValueError):
        model.simulate(model.nominal(), events, [0.0], shift=shift)


def test_canonical_and_wilson():
    assert model.canonical({"b": 2, "a": 1}) == b'{"a":1,"b":2}\n'
    low, high = model.wilson(0, 768)
    assert abs(low) < 1e-15 and 0.004 < high < 0.006
    with pytest.raises(ValueError):
        model.canonical({"nan": float("nan")})


def test_retained_artifact_integrity_and_criteria():
    target = model.ROOT / "artifacts/luna47g"
    if not (target / "manifest.json").exists():
        pytest.skip("retained outputs not executed yet")
    manifest = json.loads((target / "manifest.json").read_bytes())
    for name, entry in manifest["files"].items():
        data = (target / name).read_bytes()
        assert len(data) == entry["bytes"]
        assert model.sha(data) == entry["sha256"]
    rows = [json.loads(line) for line in
            gzip.decompress((target / "samples.jsonl.gz").read_bytes()).splitlines()]
    summary = json.loads((target / "summary.json").read_bytes())
    assert len(rows) == 3840
    for band, info in summary["bands"].items():
        group = [r for r in rows if r["band"] == band]
        assert len(group) == 768
        assert sum(not r["outcome"]["pass_"] for r in group) == info["failures"]
        for key, count in info["gate_failures"].items():
            assert sum(not r["outcome"]["gates"][key] for r in group) == count
    # Recompute selected retained rows directly from saved parameters/noise.
    for i in (0, 767, 768, 1535, 2304, 3072, 3839):
        row = rows[i]
        assert model.evaluate(row["parameters"], row["noise_units"]) == row["outcome"]
