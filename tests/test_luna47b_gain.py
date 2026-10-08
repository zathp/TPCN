import copy
import json
import math
import subprocess

import pytest

from experiments.luna47b import diagnostic as d


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


def test_full_retained_reconstruction_and_determinism(monkeypatch):
    def reject_current_analyzer(*args, **kwargs):
        pytest.fail("current analyzer was used for historical reconstruction")

    monkeypatch.setattr(d.retained, "verify_integrity", reject_current_analyzer)
    monkeypatch.setattr(d.retained, "analyze_sequence", reject_current_analyzer)
    document, provenance = d.reconstruct()
    result = d.analyze(document)
    sources = provenance["analyzer_sources"]
    assert sources["historical_revision"] == d.BASE
    assert sources["historical_git_blob"] == "08f217daec167b2abc82f5988dba660c19f4ae0e"
    assert sources["recorded_execution_revision"] == d.HISTORICAL_EXECUTION_REVISION
    assert sources["execution_git_blob"] == sources["historical_git_blob"]
    assert sources["current_revision"] == d.CURRENT_ANALYZER_REVISION
    assert sources["current_git_blob"] == "59d24b08ffa0a2a9a1ebe03a35ae595fb646fcd4"
    assert sources["current_git_blob"] != sources["historical_git_blob"]
    assert sources["reconstruction_source"] == "authenticated historical Git object"
    assert provenance["historical_lane"]["retained_result_sha256"] == d.LUNA47B_RESULT_SHA256
    assert provenance["historical_lane"]["retained_validation_sha256"] == d.LUNA47B_VALIDATION_SHA256
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


@pytest.mark.parametrize(("identity", "message"), [
    ({"historical_revision": "HEAD"}, "historical analyzer revision differs"),
    ({"historical_blob": "0" * 40}, "historical analyzer Git object pin differs"),
    ({"historical_blob": d.CURRENT_ANALYZER_BLOB},
     "historical analyzer Git object pin differs"),
    ({"execution_revision": "HEAD"}, "historical analyzer execution revision differs"),
    ({"current_blob": "0" * 40}, "reviewed current analyzer Git object pin differs"),
])
def test_luna52_historical_analyzer_rejects_substituted_identity(tmp_path, identity, message):
    with pytest.raises(ValueError, match=message):
        d.load_historical_analyzer(tmp_path, **identity)


def test_luna52_historical_analyzer_object_must_be_retrievable(tmp_path):
    with pytest.raises(ValueError, match="object unavailable"):
        d.load_historical_analyzer(tmp_path)


def test_luna52_historical_analyzer_bytes_must_match_git_blob(monkeypatch):
    actual_git = d.git

    def changed_historical_source(*args, **kwargs):
        result = actual_git(*args, **kwargs)
        if args[:2] == ("show", f"{d.BASE}:{d.ANALYZER_PATH}"):
            return result + b"\n# unauthorized historical source edit\n"
        return result

    monkeypatch.setattr(d, "git", changed_historical_source)
    with pytest.raises(ValueError, match="bytes do not match its Git object"):
        d.load_historical_analyzer()


def _clone_repo(tmp_path):
    clone = tmp_path / "repo"
    subprocess.run(
        ["git", "clone", "--quiet", "--shared", str(d.ROOT), str(clone)],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(["git", "config", "user.name", "Luna-52 tests"],
                   cwd=clone, check=True)
    subprocess.run(["git", "config", "user.email", "luna52-tests@example.invalid"],
                   cwd=clone, check=True)
    return clone


def test_luna52_current_analyzer_source_is_separately_pinned(tmp_path):
    clone = _clone_repo(tmp_path)
    current = clone / d.ANALYZER_PATH
    current.write_bytes(current.read_bytes() + b"\n# unreviewed current source\n")
    with pytest.raises(ValueError, match="current analyzer checkout differs"):
        d.load_historical_analyzer(clone)


@pytest.mark.parametrize(("path", "message"), [
    ("experiments/luna47b/PROTOCOL.md", "protocol checkout differs"),
    ("artifacts/luna47b/results.json", "retained Luna-47B result identity differs"),
    ("artifacts/luna47b/validation.json", "retained Luna-47B validation identity differs"),
])
def test_luna52_retained_lane_metadata_rejects_protocol_and_result_substitution(
    tmp_path, path, message
):
    clone = _clone_repo(tmp_path)
    target = clone / path
    target.write_bytes(target.read_bytes() + b"\n")
    with pytest.raises(ValueError, match=message):
        d.verify_historical_lane_metadata(clone)


def test_luna52_historical_reconstruction_rejects_changed_consumed_input(tmp_path):
    clone = _clone_repo(tmp_path)
    changed = clone / d.retained.L45 / "summary.json"
    changed.write_bytes(changed.read_bytes() + b" ")
    subprocess.run(["git", "add", str(changed.relative_to(clone))],
                   cwd=clone, check=True)
    subprocess.run(["git", "commit", "-m", "mutate retained Luna-45 input"],
                   cwd=clone, check=True, capture_output=True, text=True)
    with pytest.raises(ValueError, match="evidence differs beyond Git checkout materialization"):
        d.reconstruct(clone)


@pytest.mark.parametrize(("path", "message"), [
    ("artifacts/luna47b/results.json", "retained Luna-47B result identity differs"),
    ("experiments/luna47b/PROTOCOL.md", "protocol checkout differs"),
    ("run_luna46_depth_scaling_diagnostic.py", "current analyzer checkout differs"),
])
def test_luna52_reconstruction_rejects_retained_lane_mutation(tmp_path, path, message):
    clone = _clone_repo(tmp_path)
    changed = clone / path
    changed.write_bytes(changed.read_bytes() + b"\n# unauthorized mutation\n")

    with pytest.raises(ValueError, match=message):
        d.reconstruct(clone)


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
