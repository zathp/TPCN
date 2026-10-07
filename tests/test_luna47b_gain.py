import copy
import json
import math

import pytest

from experiments.luna47b import diagnostic as d


def test_artifact_comparison_allows_only_crlf_checkout_conversion():
    expected = b'{"value":"line one\\nline two"}\n'
    assert d.artifact_matches_checkout(expected, expected)
    assert d.artifact_matches_checkout(expected.replace(b"\n", b"\r\n"), expected)
    assert not d.artifact_matches_checkout(expected + b"\r", expected)
    assert not d.artifact_matches_checkout(expected + b" ", expected)


def rows(inputs, gaps=None):
    gaps = gaps or [0.0] * len(inputs)
    clock = 0.0
    state = 0.0
    result = []
    for i, (value, gap) in enumerate(zip(inputs, gaps)):
        prior = clock
        clock += gap
        rho = math.exp(-0.0125 * gap)
        before = state
        state = rho * state + value
        result.append(dict(event_id=str(i), queue_sequence=i, timestamp=clock,
                           prior_clock=prior, dt=gap, rho=rho, input=value,
                           is_reception=True, state_before=before, state_after=state))
    return result


@pytest.mark.parametrize("inputs,gaps", [
    ([0.2], [4]), ([-0.25, -0.3], [0, 80]),
    ([0.4, -0.4, 0.2], [0, 0, 0]),
    ([0.4, -0.1, 0.3], [10, 80, 4]),
    ([0, 0], [0, 7]), ([], []),
])
def test_critical_and_brackets(inputs, gaps):
    events = rows(inputs, gaps)
    derived = d.derive(events)
    critical = derived["critical_gain"]
    if critical is None:
        assert not d.trajectory(events, 1e6)["crosses"]
    else:
        assert not d.trajectory(events, 0.99 * critical)["crosses"]
        assert d.trajectory(events, 1.01 * critical)["crosses"]
        assert critical * derived["maximum_abs_unit_gain"] == pytest.approx(1)


def test_threshold_exact_no_tolerance_and_censoring():
    events = rows([0.5, 0.5, -0.4])
    assert not d.trajectory(rows([math.nextafter(1.0, 0.0)]), 1)["crosses"]
    actual = d.trajectory(events, 1)
    assert actual["first_crossing"]["queue_sequence"] == 1
    assert actual["events"][2]["censored"]
    assert actual["events"][2]["input"] == -0.4
    assert actual["events"][2]["state_input"] is None


def test_saturation_finite_and_unchanged_input():
    events = rows([-0.5, 0.3])
    original = copy.deepcopy(events)
    result = d.trajectory(events, 1e6)
    assert events == original
    assert result["saturations"] == 1
    assert result["first_crossing"]["state_input"] == -4
    assert result["maximum_abs_evaluated_state"] <= 4


@pytest.mark.parametrize("gain", [-1, math.inf, math.nan, 1000001])
def test_invalid_gain(gain):
    with pytest.raises(ValueError, match="BLOCKED"):
        d.trajectory(rows([0.2]), gain)


def test_signed_cancellation_and_reversal():
    result = d.trajectory(rows([0.4, -0.5]), 1)
    assert result["cancelled_magnitude_before_stop"] == 0.4
    assert result["sign_reversals_before_stop"] == 1
    assert not result["crosses"]
    assert result["events"][1]["state_input"] == pytest.approx(-0.1)


def test_baseline_invariance_and_reset():
    events = rows([0.3, -0.1, 0.2], [3, 9, 80])
    calculated = d.derive(events)
    result = d.trajectory(events, 1)
    assert [e["state_input"] for e in result["events"]] == calculated["states"]
    assert d.trajectory(events, 1) == result
    events[1]["state_after"] += 0.01
    with pytest.raises(ValueError, match="recurrence mismatch"):
        d.derive(events)


def test_full_retained_reconstruction_and_determinism():
    document, provenance = d.reconstruct()
    result = d.analyze(document)
    assert provenance["phase_digests"]["initial"] == provenance["phase_digests"]["replay"]
    assert d.retained.canonical(result) == d.retained.canonical(d.analyze(document))
    assert len(result["sequences"]) == 320
    assert sum(s["receptions"] for s in result["sequences"]) == 235
    assert result["retained_verdict"] == "MIXED"
    for i, summary in enumerate(result["summaries"]):
        assert summary["rescued"] == sum(
            s["global_arms"][i]["crosses"] for s in result["sequences"]
            if s["category"] == "DRIVE-LIMITED")
        assert summary["unintended_crossings"] == sum(
            s["global_arms"][i]["crosses"] for s in result["sequences"]
            if s["category"] != "DRIVE-LIMITED")
        assert summary["maximum_abs_evaluated_state"] <= 4
    for s in result["sequences"]:
        for arm in s["global_arms"] + s["local_brackets"]:
            for event in arm["events"]:
                assert math.isfinite(event["deposit"])
                if not event["censored"]:
                    assert event["crossed"] == (abs(event["state_input"]) >= 1)
                    assert abs(event["state_input"]) <= 4


def test_retained_artifact_if_present():
    path = d.ROOT / "artifacts/luna47b/results.json"
    if not path.exists():
        pytest.skip("outcome artifact not generated during protocol precommit")
    output = json.loads(path.read_bytes())
    assert output["output_digest"] == d.retained.digest(
        {k: v for k, v in output.items() if k != "output_digest"})
    assert output["replay"]["equal"]
    document = json.loads((d.ROOT / d.RETAINED).read_bytes())
    assert output["result"] == d.analyze(document)
