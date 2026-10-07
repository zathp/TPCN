"""Frozen acceptance tests for isolated qualification; no production imports."""
from dataclasses import asdict
import inspect
import math

import pytest

from experiments.luna47c import qualifier
from experiments.luna47c.evaluate import experiment, score, trace
from experiments.luna47c.fixtures import FAMILIES, SAMPLES, canonical, digest, fixtures
from experiments.luna47c.qualifier import Config, METHODS, Qualifier


@pytest.mark.parametrize("method", METHODS)
def test_equations_prior_state_and_reset(method):
    q = Qualifier(Config(method))
    e = q.process(1.0, 8.0)
    assert e["B"] == 0 and e["N"] == .25 and e["E"] == 7.5
    assert e["B_after"] == pytest.approx(-math.expm1(-1 / 20) * .25, abs=1e-12)
    target = .5 if method == "robust" else 8.0
    expected_n = .25 if method == "fixed" else .25 - math.expm1(-.25) * (target - .25)
    assert e["N_after"] == pytest.approx(expected_n, abs=1e-12)
    q.reset()
    assert q.process(1.0, 8.0) == e


def test_fixture_coverage_hashes_times_mirrors():
    fs = fixtures()
    assert len(fs) == 16 and {f.family for f in fs} == set(FAMILIES)
    assert len({digest(f.serialized()) for f in fs}) == 16
    assert fs == fixtures()
    for a, b in zip(fs[::2], fs[1::2]):
        assert len(a.inputs) == SAMPLES
        assert all(t1 < t2 for (t1, _), (t2, _) in zip(a.inputs, a.inputs[1:]))
        assert len({a.inputs[i][0] - a.inputs[i-1][0] for i in range(1, SAMPLES)}) == 4
        assert all(t == u and x == -y for (t, x), (u, y) in zip(a.inputs, b.inputs))


def test_truth_not_in_mechanism():
    assert tuple(inspect.signature(Qualifier.process).parameters) == ("self", "timestamp", "raw")
    source = inspect.getsource(qualifier)
    assert "fixtures" not in source and "evaluate" not in source and "tpcn" not in source
    f = fixtures()[4]
    events = trace(f.inputs, "robust")
    # Alter evaluator truth only: outputs still arise from identical raw pairs.
    assert trace(f.inputs, "robust") == events
    from dataclasses import replace
    fake = replace(f, signal_truth=(0.0,) * SAMPLES)
    assert fake.inputs == f.inputs
    assert score(fake, events, events) != score(f, events, events)
    assert trace(fake.inputs, "robust") == events


@pytest.mark.parametrize("method", METHODS)
def test_bounded_state_and_no_history(method):
    q = Qualifier(Config(method))
    for i in range(10000):
        e = q.process(i * 1.25, 16.0 if i % 2 else -16.0)
        assert abs(q.baseline) <= 4 and .05 <= q.noise <= 16
        assert math.isfinite(e["E"]) and abs(e["E"]) <= 20
    assert not hasattr(q, "__dict__")
    assert set(q.__slots__) == {"config", "baseline", "noise", "last_time"}


@pytest.mark.parametrize("method", METHODS)
def test_sign_symmetry_and_boundary(method):
    positive, negative = Qualifier(Config(method)), Qualifier(Config(method))
    assert positive.process(1, .5)["E"] == 0
    assert negative.process(1, -.5)["E"] == 0
    for i, value in enumerate((.500001, -.7, 8, -.9, 0, -16, 16), start=2):
        a, b = positive.process(i, value), negative.process(i, -value)
        for key in ("B", "E", "B_after"):
            assert a[key] == pytest.approx(-b[key], abs=1e-12)
        for key in ("N", "N_after"):
            assert a[key] == pytest.approx(b[key], abs=1e-12)


@pytest.mark.parametrize("timestamp,raw", [(float("nan"), 0), (-1, 0),
                                          (1, float("inf")), (1, 16.001)])
def test_reject_invalid_input_without_mutation(timestamp, raw):
    q = Qualifier(Config("robust"))
    before = q.baseline, q.noise, q.last_time
    with pytest.raises(ValueError):
        q.process(timestamp, raw)
    assert (q.baseline, q.noise, q.last_time) == before


def test_time_and_configuration_validation():
    q = Qualifier(Config("adaptive"))
    q.process(1, 0)
    for t in (1, .5):
        with pytest.raises(ValueError):
            q.process(t, 0)
    for kwargs in ({"method": "unknown"}, {"noise_tau": 0}, {"multiplier": float("nan")},
                   {"initial_noise": .01}, {"baseline_bound": 17}):
        values = asdict(Config("fixed"))
        values.update(kwargs)
        with pytest.raises(ValueError):
            Config(**values)


def test_explicit_contamination_failure_and_robust_protection():
    f = next(f for f in fixtures() if f.identity == "contamination_chain:+1")
    a, r, fixed = [trace(f.inputs, m) for m in ("adaptive", "robust", "fixed")]
    assert a[60]["N_after"] > r[60]["N_after"] * 4
    assert a[61]["E"] == 0 and r[61]["E"] > 0 and fixed[61]["E"] > 0
    assert a[61]["band"] > abs(a[61]["raw"] - a[61]["B"])
    # Spike-free matched control admits the same later raw at this point.
    control = trace(tuple((t, 0.0) for t, _ in f.inputs), "adaptive")
    assert abs(a[61]["raw"] - control[61]["B"]) > control[61]["band"]


def test_exact_replay_scoring_and_recovery():
    result = experiment()
    assert canonical(result) == canonical(experiment())
    assert len(result["runs"]) == 48 and all(x["within_tolerance"] for x in result["symmetry"])
    assert result["gates"]["failure_chain_observed"]
    assert result["gates"]["robust_chain_protection"]
    for r in result["runs"]:
        m = r["metrics"]
        assert 0 <= m["false_admissions"] <= m["noise_only"]
        assert 0 <= m["missed_meaningful"] <= m["meaningful"]
        if m["meaningful"] == 0:
            assert m["recovery_status"] == "not_applicable"
            assert m["noise_contamination_max"] == m["baseline_pull_max"] == 0
        if m["recovery"] is not None:
            assert m["recovery"]["elapsed_time"] > 0
