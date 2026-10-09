"""Independent measurement oracle and focused frozen L63A acceptance.

Oracle/reference functions import no model functions or production code.
Subject imports occur only in fixture/test/materialization helpers.
"""

from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import struct
import sys

import pytest


def bits(value):
    return struct.pack(">d", value).hex()


def closed_form(z0, release_time):
    """Independent high-precision reference; no recurrence/model calls."""
    with localcontext() as ctx:
        ctx.prec = 60
        duration = Decimal(release_time.numerator) / Decimal(release_time.denominator)
        return float(Decimal(str(z0)) * (-duration / Decimal(8)).exp())


def reference_schedules():
    """Literal contract schedule, independent of the protocol loader."""
    def observations(times):
        return [(str(t), "observation", None) for t in times]

    schedules = [
        ("A1-normal", 1, observations(["1/4", "7/4", 4, 8, 32, 36])),
        ("A2-hold", 0, observations(["1/4", "7/4", 4, 8, 32, 63])),
    ]
    for prefix, gate in (("A3-A5-H", 0), ("normal-comparator-H", 1)):
        for h in (2, 8, 32):
            events = observations([Fraction(h, 8), Fraction(h, 2), h])
            events += [(str(h), "cue", 1)]
            events += observations([Fraction(h) + Fraction(1, 4),
                                    Fraction(h) + Fraction(7, 4), h + 4])
            schedules.append((prefix + str(h), gate, events))
    schedules.extend([
        ("prior-gate-switch", 1, [
            ("1/4", "observation", None), ("1", "cue", 0),
            ("7/4", "observation", None), ("4", "observation", None),
            ("8", "observation", None), ("8", "cue", 1),
            ("33/4", "observation", None), ("39/4", "observation", None),
            ("12", "observation", None),
        ]),
        ("expiry-boundary", 0, [
            ("63", "observation", None), ("64", "cue", 1),
            ("64", "observation", None), ("65", "observation", None),
        ]),
        ("duplicate-cue", 0, [
            ("2", "observation", None), ("2", "cue", 1), ("2", "cue", 1),
            ("9/4", "observation", None), ("15/4", "observation", None),
            ("6", "observation", None),
        ]),
    ])
    return schedules


def reference_instances():
    return [
        (sid + "/" + label, z0, label, sid, gate, events)
        for z0, label in ((-0.75, "negative"), (0.0, "zero"), (0.75, "positive"))
        for sid, gate, events in reference_schedules()
    ]


def measure_instance(instance, reference):
    """Measure already materialized rows; cannot drive subject state."""
    identity, z0, label, sid, gate, listed = reference
    assert instance["id"] == identity
    assert instance["schedule_id"] == sid
    assert instance["preload"] == {
        "id": label, "rational": str(Fraction(z0)), "float": z0,
    }
    assert instance["initial_gate"] == gate
    assert instance["generated_output_events"] == 0
    events = list(listed)
    if sid != "expiry-boundary":
        events.append(("64", "expiry", None))
    assert len(instance["trace"]) == len(events)
    release = Fraction(0)
    last = Fraction(0)
    state = z0
    status = "ACTIVE"
    due = 64.0
    reason = None
    measured = []
    for n, (row, (rational, kind, cue)) in enumerate(zip(instance["trace"], events)):
        t = Fraction(rational)
        assert row["id"] == identity + ("/due-expiry" if kind == "expiry" else f"/event/{n}")
        assert row["ordinal"] == n
        assert row["time_rational"] == rational
        assert row["time_float"] == float(t)
        assert row["prior_time_rational"] == str(last)
        assert row["prior_time"] == float(last)
        assert row["kind"] == kind and row["cue"] == cue
        assert row["prior_gate"] == gate
        assert row["prior_status"] == status
        assert row["prior_due"] == due
        assert row["event_count"] == n + 1
        assert row["dt"] == float(t - last)
        if state is None:
            assert row["prior_state"] is None
        else:
            assert bits(row["prior_state"]) == bits(state)
        hold_identity = None
        if status == "EXPIRED":
            expected = None
            action = "terminal-report"
            rejection = "terminal-no-revival" if kind == "cue" else None
            assert row["pre_state"] is None and row["post_state"] is None
        elif t >= 64:
            # Stored pre-clear value; no post-expiry ordinary evolution.
            expected = closed_form(z0, release)
            assert bits(row["pre_state"]) == bits(state)
            assert row["post_state"] is None
            last, state, status, due = Fraction(64), None, "EXPIRED", None
            reason = "absolute-TTL-equality-or-later"
            action = "expiry"
            rejection = "expiry-preempts-cue" if kind == "cue" else None
        else:
            if gate == 1:
                release += t - last
            expected = closed_form(z0, release)
            if gate == 0 or t == last:
                hold_identity = bits(row["pre_state"]) == bits(state)
                assert hold_identity
            assert bits(row["pre_state"]) == bits(row["post_state"])
            if z0 == 0:
                assert bits(row["post_state"]) == bits(0.0)
            state, last = row["post_state"], t
            if kind == "cue":
                gate = cue
            action = "gate-applied" if kind == "cue" else "observation"
            rejection = None
        error = None if expected is None else abs(row["pre_state"] - expected)
        tolerance = None if expected is None else 1e-12 + 1e-12 * abs(expected)
        if error is not None:
            assert error <= tolerance
        assert row["post_gate"] == gate
        assert row["last_time"] == float(last)
        assert row["status"] == status
        assert row["due"] == due
        assert row["action"] == action
        assert row["rejection"] == rejection
        assert row["reason"] == reason
        measured.append({
            **row, "total_release_time_rational": str(release),
            "expected_pre_state": expected, "abs_error": error,
            "residual": None if expected is None else row["pre_state"] - expected,
            "tolerance": tolerance, "hold_or_equal_time_bits_identical": hold_identity,
            "pre_state_bits": None if row["pre_state"] is None else bits(row["pre_state"]),
            "post_state_bits": None if row["post_state"] is None else bits(row["post_state"]),
        })
    assert instance["final_status"] == "EXPIRED"
    assert instance["processed_events"] == len(events) <= 32
    maximum = max(abs(row[k]) for row in instance["trace"]
                  for k in ("prior_state", "pre_state", "post_state") if row[k] is not None)
    assert instance["max_abs_state"] == maximum <= 4
    return {**instance, "trace": measured}


def evaluate(outcome):
    refs = reference_instances()
    assert len(outcome["instances"]) == len(refs) == 33
    measured = [measure_instance(i, r) for i, r in zip(outcome["instances"], refs)]
    controls(measured)
    return {
        **outcome, "instances": measured,
        "measurements": {
            "instance_count": 33,
            "event_count": sum(len(i["trace"]) for i in measured),
            "max_abs_error": max(r["abs_error"] for i in measured for r in i["trace"]
                                 if r["abs_error"] is not None),
            "max_abs_state": max(i["max_abs_state"] for i in measured),
            "hold_max_abs_change": 0.0,
            "generated_output_events": 0,
            "all_controls_passed": True,
        },
    }


def controls(instances):
    by_id = {i["id"]: i for i in instances}
    for z0, label in ((-0.75, "negative"), (0.0, "zero"), (0.75, "positive")):
        held_post = []
        for h in (2, 8, 32):
            held = by_id[f"A3-A5-H{h}/{label}"]["trace"]
            normal = by_id[f"normal-comparator-H{h}/{label}"]["trace"]
            assert all(bits(r["post_state"]) == bits(z0) for r in held[:4])
            held_post.append([bits(r["post_state"]) for r in held[4:7]])
            for r in held[4:7]:
                expected = closed_form(z0, Fraction(r["time_rational"]) - h)
                assert abs(r["post_state"] - expected) <= 1e-12 + 1e-12 * abs(expected)
            if z0 != 0:
                assert abs(normal[2]["post_state"]) < abs(held[2]["post_state"])
                if h == 32:
                    # Analytically predeclared comparison, not underflow/exact loss.
                    expected = closed_form(z0, Fraction(32))
                    assert abs(normal[2]["post_state"] - expected) <= 1e-12 + 1e-12 * abs(expected)
        assert held_post[0] == held_post[1] == held_post[2]
        switched = by_id[f"prior-gate-switch/{label}"]["trace"]
        expected = closed_form(z0, Fraction(1))
        assert abs(switched[4]["post_state"] - expected) <= 1e-12 + 1e-12 * abs(expected)
        assert bits(switched[1]["post_state"]) == bits(switched[4]["post_state"])
        duplicate = by_id[f"duplicate-cue/{label}"]["trace"]
        assert all(bits(r["post_state"]) == bits(z0) for r in duplicate[:3])
        boundary = by_id[f"expiry-boundary/{label}"]["trace"]
        assert boundary[1]["action"] == "expiry"
        assert boundary[1]["post_gate"] == 0
        assert boundary[1]["rejection"] == "expiry-preempts-cue"
        assert all(r["post_state"] is None for r in boundary[1:])


@pytest.fixture(scope="module")
def outcome():
    from experiments.luna63a.run import materialize
    return materialize()


@pytest.mark.parametrize("index", range(33), ids=[r[0] for r in reference_instances()])
def test_frozen_instance_oracle(outcome, index):
    measure_instance(outcome["instances"][index], reference_instances()[index])


def test_matrix_controls(outcome):
    evaluate(outcome)


def test_independent_replay(outcome):
    from experiments.luna63a.run import canonical, materialize
    assert canonical(evaluate(outcome)) == canonical(evaluate(materialize()))


@pytest.mark.parametrize("z0", [-0.75, 0.0, 0.75])
@pytest.mark.parametrize("gate", [0, 1])
def test_semigroup_observation_noninterference(z0, gate):
    from experiments.luna63a.model import Retention
    split, whole = Retention(z0, gate), Retention(z0, gate)
    split.process(0.25)
    split.process(1.75)
    split.process(4.0)
    whole.process(4.0)
    expected = closed_form(z0, Fraction(4 * gate))
    tolerance = 1e-12 + 1e-12 * abs(expected)
    assert abs(split.z - whole.z) <= tolerance
    assert abs(split.z - expected) <= tolerance
    if gate == 0:
        assert bits(split.z) == bits(whole.z) == bits(z0)


@pytest.mark.parametrize("gate", [False, True, -1, 2, 0.5, 1.0, float("nan"), float("inf"), "1", None])
def test_nonbinary_initial_and_cue_fault(gate):
    from experiments.luna63a.model import ModelFault, Retention
    with pytest.raises(ModelFault):
        Retention(0.75, gate)
    local = Retention(0.75, 0)
    with pytest.raises(ModelFault):
        local.process(1, "cue", gate)
    assert local.status == "FAULT" and local.z == 0.75 and local.due is None
    with pytest.raises(ModelFault):
        local.process(2, "cue", 1)


@pytest.mark.parametrize("z0", [-4.01, 4.01, float("nan"), float("inf"), -float("inf"), True])
def test_invalid_preload(z0):
    from experiments.luna63a.model import ModelFault, Retention
    with pytest.raises(ModelFault):
        Retention(z0, 0)


@pytest.mark.parametrize("t", [-0.25, 65.25, float("nan"), float("inf"), -float("inf"), True])
def test_invalid_time(t):
    from experiments.luna63a.model import ModelFault, Retention
    local = Retention(-0.75, 0)
    with pytest.raises(ModelFault):
        local.process(t)
    assert local.status == "FAULT" and local.z == -0.75


def test_late_time():
    from experiments.luna63a.model import ModelFault, Retention
    local = Retention(0.75, 0)
    local.process(2)
    with pytest.raises(ModelFault):
        local.process(1.75)
    assert local.status == "FAULT" and local.last_time == 2


def test_event_overflow_explicit():
    from experiments.luna63a.model import ModelFault, Retention
    local = Retention(0.75, 0)
    for _ in range(32):
        local.process(0)
    with pytest.raises(ModelFault):
        local.process(0)
    assert local.count == 32 and local.status == "FAULT" and local.z == 0.75


@pytest.mark.parametrize("z0", [-4.0, 4.0])
def test_bound_endpoints_validation_only(z0):
    from experiments.luna63a.model import Retention
    local = Retention(z0, 1)
    assert abs(local.process(4)["post_state"]) <= 4
    local.process(4, "cue", 0)
    retained = bits(local.z)
    local.process(63)
    assert bits(local.z) == retained


def test_no_revival_or_payload_output_interface():
    from experiments.luna63a.model import Retention
    local = Retention(0.75, 0)
    row = local.process(64, "cue", 1)
    assert row["rejection"] == "expiry-preempts-cue"
    row = local.process(65, "cue", 1)
    assert row["rejection"] == "terminal-no-revival"
    assert local.status == "EXPIRED" and local.z is None and local.R == 0
    assert not any(hasattr(local, key) for key in
                   ("reset", "preload", "emit", "outputs", "threshold", "x", "pending_spike"))
    fresh = Retention(0.75, 0)
    assert fresh is not local and fresh.status == "ACTIVE"
    with pytest.raises(TypeError):
        fresh.process(1, "cue", 1, value=0.75)


def test_cue_source_anti_command():
    import ast
    source = Path(__file__).resolve().parents[1] / "experiments/luna63a/model.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    setter = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_set_gate")
    assignments = [n for n in ast.walk(setter) if isinstance(n, ast.Assign)]
    assert len(assignments) == 1
    assert ast.unparse(assignments[0].targets[0]) == "self.R"
    assert ast.unparse(assignments[0].value) == "gate"
    assert not any(isinstance(n, ast.Call) for n in ast.walk(setter))
    for relative in ("model.py", "run.py"):
        text = (source.parent / relative).read_text(encoding="utf-8")
        parsed = ast.parse(text)
        for node in ast.walk(parsed):
            if isinstance(node, ast.Import):
                assert not any(n.name.startswith("tpcn") for n in node.names)
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith("tpcn")


def record(freeze):
    """Artifact publication: fresh independent runs, downstream oracle only."""
    import platform
    import subprocess

    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    from experiments.luna63a.run import canonical, digest, materialize

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root)

    assert git("branch", "--show-current").decode().strip() == "experiment/luna63a-binary-adaptive-decay"
    assert git("rev-parse", "HEAD").decode().strip() == freeze
    assert not git("status", "--porcelain")
    paths = [
        "experiments/luna63a/__init__.py", "experiments/luna63a/model.py",
        "experiments/luna63a/run.py", "experiments/luna63a/protocol.json",
        "experiments/luna63a/README.md", "tests/test_luna63a_adaptive_decay.py",
        ".github/agents/luna-63a.agent.md",
        "workflow/ARCHITECTURE_CONTRACT.md", "workflow/ARCHITECTURE_CHANGELOG.md",
        "workflow/docs/luna/LUNA_WORKFLOW.md",
        "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md",
        "workflow/docs/architecture_proposals/README.md",
        "workflow/docs/architecture_proposals/ACP-TEMPLATE.md",
        "workflow/docs/architecture_proposals/ACP-0008.md",
        "workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md",
        "workflow/handoffs/luna-0-independent-review-luna62-20261009.md",
        "workflow/handoffs/luna-0-luna63-mechanism-authorization-20261009.md",
        "tpcn/event_runtime.py", "tpcn/excursion_neuron.py",
        "tpcn/experiment_excursion_runtime.py", "tpcn/topology.py",
        "tpcn/predictive_coding.py", "tpcn/eligibility.py",
        "experiments/luna47a/PROTOCOL.md", "experiments/luna47d/PROTOCOL.md",
        "experiments/luna47d/model.py",
    ] + ["tests/" + name for name in (
        "test_event_runtime.py", "test_excursion_neuron.py", "test_e2_multi_excursion.py",
        "test_luna38_excursion_integration_state.py", "test_predictive_coding.py",
        "test_luna47a_retention.py", "test_luna47d_output_model.py")]
    identities = {}
    for path in paths:
        committed = git("show", freeze + ":" + path)
        checkout = (root / path).read_bytes()
        assert checkout == committed or checkout == committed.replace(b"\n", b"\r\n")
        identities[path] = {
            "git_blob": git("rev-parse", freeze + ":" + path).decode().strip(),
            "git_sha256": hashlib.sha256(committed).hexdigest(),
            "checkout_sha256": hashlib.sha256(checkout).hexdigest(),
            "git_bytes": len(committed), "checkout_bytes": len(checkout),
            "byte_relation": "identical" if checkout == committed else "exact-LF-to-CRLF",
        }
    initial = evaluate(materialize())
    replay = evaluate(materialize())
    assert canonical(initial) == canonical(replay)
    target = root / "artifacts/luna63a"
    target.mkdir(parents=True, exist_ok=True)
    for name, data in (("results.json", initial), ("replay.json", replay)):
        (target / name).write_bytes(canonical(data))
    manifest = {
        "schema": "L63A-MANIFEST-1",
        "starting_sha": "e52098b2141a3f121f23b512e877783a64ef8baa",
        "governance_sha": "e52098b2141a3f121f23b512e877783a64ef8baa",
        "scientific_source_sha": "8123147e04c6044d12023f541cf63130cdbb7dcc",
        "original_blocked_handoff_sha": "1d1bee9a1c39edd1a0b4278d86d5750e4590b6d6",
        "pre_outcome_sha": freeze, "implementation_sha": freeze,
        "contract_blob": identities[".github/agents/luna-63a.agent.md"]["git_blob"],
        "command": f"python tests/test_luna63a_adaptive_decay.py --record {freeze}",
        "environment": {
            "executable": sys.executable, "version": sys.version,
            "implementation": platform.python_implementation(),
            "platform": platform.platform(), "machine": platform.machine(),
        },
        "run_labels": ["initial", "independent-fresh-replay"],
        "instance_ids": [i["id"] for i in initial["instances"]],
        "source_identities": identities,
        "protocol_sha256": initial["protocol_sha256"],
        "artifact_sha256": {"results.json": digest(initial), "replay.json": digest(replay)},
        "deterministic_replay_exact": True,
        "scientific_disposition_pending_regressions": "SUPPORTED — ADAPTIVE-TAU HOLD/RELEASE",
        "regressions": "Not yet recorded; do not infer regression PASS",
        "manifest_hash": "External handoff/publication; no recursive self-hash",
    }
    (target / "manifest.json").write_bytes(canonical(manifest))
    print(json.dumps({
        "measurements": initial["measurements"],
        "initial_sha256": digest(initial), "replay_sha256": digest(replay),
        "manifest_sha256": digest(manifest),
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--record":
        record(sys.argv[2])
    else:
        raise SystemExit("Use --record PRE_OUTCOME_SHA after focused tests")
