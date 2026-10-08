"""Synthetic unit fixtures only; retained scoring runs after protocol commit."""
from copy import deepcopy
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

import pytest

FILE = Path(__file__).resolve().parents[1]/"experiments/luna47f/diagnostic.py"
SPEC = importlib.util.spec_from_file_location("luna47f_diagnostic", FILE)
d = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(d)


@pytest.fixture
def graph():
    return {"nodes": ["source", "relay", "destination"], "fan_in_limit": 2,
            "fan_out_limit": 2, "edge_capacity": 3, "routing_capacity": 3,
            "edges": [{"source": "source", "destination": "relay", "delay": 1.0},
                      {"source": "relay", "destination": "destination", "delay": 1.0}]}


@pytest.mark.parametrize("a,b,ok", [
    (1, 0.5, True), (-1, -0.5, True), (1, 0.499999999, False),
    (1, -1, False), (0, 1, False), (0, 0, False), (1, 2, True),
])
def test_similarity(a, b, ok):
    assert d.compatible(a, b)[0] == ok


@pytest.mark.parametrize("value", [float("inf"), float("nan"), True, None, "1"])
def test_nonfinite_or_nonnumeric_rejected(value):
    with pytest.raises(ValueError):
        d.compatible(value, 1)


def test_classifications_without_mutation(graph):
    before = deepcopy(graph)
    short = d.classify(graph, "source", "destination")
    assert short["predicted_hop_reduction"] == 1
    assert short["existing_shortest_path_delay"] == 2
    assert short["fan_in_opportunity"] and short["capacity_feasible_novel"]
    assert not short["existing_edge_duplicate"] and not short["cycle_forming"]
    assert short["usable_edge"] is None and short["local_observation_availability"] == "BLOCKED"
    assert d.classify(graph, "source", "relay")["existing_edge_duplicate"]
    assert d.classify(graph, "destination", "source")["cycle_forming"]
    assert graph == before
    assert d.canonical(short) == d.canonical(d.classify(graph, "source", "destination"))


def test_routing_capacity_is_per_source(graph):
    graph["routing_capacity"] = 2
    graph["edge_capacity"] = 10
    graph["edges"].extend(
        {"source": "unrelated-"+str(i), "destination": "other-"+str(i), "delay": 1.0}
        for i in range(3)
    )
    result = d.classify(graph, "source", "destination")
    assert result["saturated"]["routing_capacity"] is False
    assert result["capacity_feasible_novel"] is True


@pytest.mark.parametrize("limit", ["fan_in_limit", "fan_out_limit", "edge_capacity", "routing_capacity"])
def test_saturation(graph, limit):
    graph[limit] = 1 if limit.startswith("fan_") or limit == "routing_capacity" else 2
    result = d.classify(graph, "source", "destination")
    assert result["saturated"][limit] is True
    assert result["capacity_feasible_novel"] is False


@pytest.mark.parametrize("limit", ["fan_in_limit", "fan_out_limit", "edge_capacity", "routing_capacity"])
def test_missing_capacity_is_blocked_not_zero(graph, limit):
    del graph[limit]
    result = d.classify(graph, "source", "destination")
    assert result["capacity_status"] == "BLOCKED"
    assert result["saturated"][limit] is None
    assert result["capacity_feasible_novel"] is None


@pytest.mark.parametrize("lag,ok", [(-1, False), (0, False), (1, True), (4, True), (4.000001, False)])
def test_strict_causal_direction_and_window(graph, lag, ok):
    source = d.ref("source", "e1", 10, "/source/0")
    target = d.ref("destination", "e2", 10+lag, "/target/0")
    result = d.row("output-drive-proxy", "test", source, target, 1, 0.5, [], graph)
    assert result["opportunity"] == ok
    assert result["candidate_time"] == target["time"]


def test_self_pair_rejected(graph):
    source = d.ref("source", "e1", 0, "/source/0")
    with pytest.raises(ValueError, match="self"):
        d.row("test", "s", source, source, 1, 1, [], graph)


def test_duplicate_identity_is_not_collapsed():
    with pytest.raises(ValueError, match="duplicate"):
        d.keyed([{"id": 1}, {"id": 1}], lambda x: x["id"])


def test_repeated_proposals_reset_by_family_and_character(graph):
    source = d.ref("source", "e1", 0, "/source/0")
    target = d.ref("destination", "e2", 2, "/target/0")
    first = d.row("output-drive-proxy", "s0", source, target, 1, 1, [], graph)
    rows = [deepcopy(first) for _ in range(5)]
    rows[1]["opportunity"] = False
    rows[3]["stream_id"] = "s1"
    rows[4]["family"] = "local-deposition"
    d.annotate_repetition(rows)
    assert [r["repeated_endpoint_proposal"] for r in rows] == [False, False, True, False, False]
    expected = d.canonical(rows)
    d.annotate_repetition(rows)
    assert d.canonical(rows) == expected


def synthetic_phase(graph):
    """320 explicitly synthetic empty streams, one complete two-hop trigger."""
    for edge in graph["edges"]:
        edge["w"] = 1.0
    ep, rp, records = [], [], []
    for i in range(320):
        sid = "synthetic-"+str(i)
        record = {"stream_id": sid, "source_emissions": [], "relay_emissions": [],
                  "destination_emissions": [], "routing_enqueue_events": [],
                  "receiver_reception_events": [], "relay_integration_trace": [],
                  "destination_integration_trace": [], "relay_state_trajectory": [],
                  "resource_high_water": {"topology_"+k: graph[k] for k in
                                         ("fan_in_limit", "fan_out_limit", "edge_capacity", "routing_capacity")}}
        record["resource_high_water"]["topology_edge_peak"] = 2
        records.append(record)
        ep.append({"stream_id": sid, "events": []})
        rp.append({"stream_id": sid, "events": []})
    record = records[0]
    record["source_emissions"] = [{"event_id": "source-e", "payload": 1.0, "timestamp": 0.0}]
    record["relay_emissions"] = [{"event_id": "relay-e", "payload": 0.8, "timestamp": 1.5,
                                 "integration_trace_check": {"matches": True, "trace_emission_id": "relay-e",
                                                             "event_id": "source-e", "timestamp": 1.0,
                                                             "input_value": __import__("math").tanh(1.0)}}]
    for q, source, target, eid, payload, time in [
        (1, "source", "relay", "source-e", __import__("math").tanh(1.0), 1.0),
        (2, "relay", "destination", "relay-e", __import__("math").tanh(0.8), 2.5),
    ]:
        shared = {"source": source, "destination": target, "event_id": eid,
                  "originating_emission_id": eid, "payload": payload,
                  "payload_bits": d.bits(payload), "payload_encoding": {"hex": payload.hex()},
                  "lineage_id": q, "route_depth": 1, "route_path": [source, target],
                  "causal_roots": ["synthetic-root"], "roots_truncated": True,
                  "queue_sequence": q, "scheduled_delivery_timestamp": time}
        enqueue = {**shared, "enqueue_timestamp": time-1}
        receive = {**shared, "reception_timestamp": time}
        ep[0]["events"].append(enqueue)
        rp[0]["events"].append(receive)
        trace = {"timestamp": time, "input_value": payload,
                 "x_after_decay": 0, "x_after_input": payload}
        if target == "relay":
            trace.update({"emission_id": "relay-e", "emission_timestamp": 1.5})
            record["relay_state_trajectory"] = [{"event_id": eid, "timestamp": time}]
        record[target+"_integration_trace"].append(trace)
    record["routing_enqueue_events"] = deepcopy(ep[0]["events"])
    record["receiver_reception_events"] = deepcopy(rp[0]["events"])
    return {"records": records}, {"per_sequence": ep}, {"per_sequence": rp}


def test_synthetic_chain_replay_determinism_and_strict_nonmutation(graph):
    phase, enqueues, receptions = synthetic_phase(graph)
    before = d.canonical([phase, enqueues, receptions, graph])
    result = d.analyze(phase, enqueues, receptions, graph)
    assert d.canonical(result) == d.canonical(d.analyze(phase, enqueues, receptions, graph))
    assert d.canonical([phase, enqueues, receptions, graph]) == before
    assert result["reconciled_route_pairs"] == 2
    assert result["truncated_root_route_pairs"] == 2
    assert result["verdict"] == "PARTIALLY SUPPORTED"
    assert result["summary"]["output-drive-proxy"]["shortening_opportunities"] == 1
    assert result["summary"]["local-deposition"]["existing_edge_duplicates"] == 1
    assert all(r["strict_causal_direction"] for r in result["rows"])
    assert all(not r["target_canonical_emission_association"] for r in result["rows"]
               if r["target"]["node"] == "destination")


@pytest.mark.parametrize("mutation", ["time", "bits", "trigger", "roots", "capacity", "raw"])
def test_synthetic_identity_failures_block_instead_of_fabricating(graph, mutation):
    phase, enqueues, receptions = synthetic_phase(graph)
    if mutation == "time":
        receptions["per_sequence"][0]["events"][0]["reception_timestamp"] = 0
    elif mutation == "bits":
        receptions["per_sequence"][0]["events"][0]["payload_bits"] = d.bits(0)
    elif mutation == "trigger":
        phase["records"][0]["relay_emissions"][0]["integration_trace_check"]["event_id"] = "absent"
    elif mutation == "roots":
        enqueues["per_sequence"][0]["events"][0]["roots_truncated"] = False
    elif mutation == "capacity":
        phase["records"][0]["resource_high_water"]["topology_fan_in_limit"] = 3
    else:
        phase["records"][0]["routing_enqueue_events"] = []
    with pytest.raises(ValueError):
        d.analyze(phase, enqueues, receptions, graph)


def test_local_deposition_is_not_net_decay_change():
    event = {"payload": 0.5, "payload_bits": d.bits(0.5), "reception_timestamp": 2}
    record = {"relay_integration_trace": [{"timestamp": 2, "input_value": 0.5,
                                         "x_after_decay": 0.25, "x_after_input": 0.75}]}
    before = deepcopy(record)
    assert d.deposit(record, event, "relay")[1]["input_value"] == 0.5
    assert record == before
    record["relay_integration_trace"][0]["x_after_input"] = 1
    with pytest.raises(ValueError, match="equation"):
        d.deposit(record, event, "relay")


def test_missing_deposition_blocked():
    with pytest.raises(ValueError, match="missing"):
        d.deposit({"relay_integration_trace": []},
                  {"reception_timestamp": 2, "payload_bits": d.bits(1)}, "relay")


def test_truncated_roots_not_expanded():
    observation = d.ref("relay", "e", 1, "/r/0", True)
    assert observation["roots_truncated"] is True
    assert "complete_roots" not in observation


@pytest.mark.parametrize("path,ok", [
    ("experiments/luna47f/diagnostic.py", True), ("artifacts/luna47f/diagnostic.json", True),
    ("tests/test_luna47f_diagnostic.py", True),
    ("workflow/handoffs/luna-47f-candidate-generation-diagnostic-20261006.md", True),
    ("tpcn/topology.py", False), ("artifacts/luna45/config.json", False),
    ("tests/test_luna47g_test.py", False), ("workflow/ARCHITECTURE_CONTRACT.md", False),
])
def test_scope(path, ok):
    assert d.owned(path) == ok


def test_luna51_consumed_input_identity_is_historically_anchored_and_local():
    pinned = b'{"value":1}\n'
    record = {
        "baseline_git_blob": "historical-blob",
        "published_sha256": d.sha(pinned),
        "published_bytes": len(pinned),
    }
    for path in d.CONSUMED_INPUTS:
        assert d.verify_consumed_input(
            path, pinned, pinned, record, "historical-blob"
        )["checkout_materialization"] == "exact"
        assert d.verify_consumed_input(
            path,
            pinned.replace(b"\n", b"\r\n"),
            pinned,
            record,
            "historical-blob",
        )["checkout_materialization"] == "exact-Git-LF-to-CRLF-checkout"
        with pytest.raises(ValueError, match="beyond Git newline"):
            d.verify_consumed_input(
                path, pinned + b" ", pinned, record, "historical-blob"
            )
        with pytest.raises(ValueError, match="beyond Git newline"):
            d.verify_consumed_input(
                path,
                b'{"value":2}\n',
                pinned,
                record,
                "historical-blob",
            )
    with pytest.raises(ValueError, match="revision differs"):
        d.verify_consumed_input(
            d.CONSUMED_INPUTS[0],
            pinned,
            pinned,
            record,
            "historical-blob",
            revision="HEAD",
        )
    with pytest.raises(ValueError, match="Git object identity differs"):
        d.verify_consumed_input(
            d.CONSUMED_INPUTS[0], pinned, pinned, record, "wrong-blob"
        )
    with pytest.raises(ValueError, match="outside the Luna47F consumed set"):
        d.verify_consumed_input(
            "workflow/unrelated.md", pinned, pinned, record, "historical-blob"
        )


def test_luna51_historical_inventory_rejects_wrong_revision_and_input_set():
    retained = {
        "evidence_baseline": d.BASE,
        "source_inventory": {path: {} for path in d.CONSUMED_INPUTS},
    }
    with pytest.raises(ValueError, match="baseline revision differs"):
        d.verify_historical_inputs(Path.cwd(), retained, revision="HEAD")
    retained["source_inventory"]["workflow/new-file.md"] = {}
    with pytest.raises(ValueError, match="consumed-input inventory differs"):
        d.verify_historical_inputs(Path.cwd(), retained)


def test_luna51_protocol_and_execution_code_keep_their_historical_git_identities():
    retained = d.verify_retained_files(d.ROOT)
    protocol = d.verify_historical_source(
        d.ROOT,
        "experiments/luna47f/PROTOCOL.md",
        d.PROTOCOL_REVISION,
        retained["protocol_sha256"],
        d.PROTOCOL_REVISION,
    )
    code = d.verify_historical_source(
        d.ROOT,
        "experiments/luna47f/diagnostic.py",
        d.CODE_SOURCE_REVISION,
        retained["code_sha256"],
        d.CODE_SOURCE_REVISION,
    )
    assert protocol["recorded_execution_sha256"] == retained["protocol_sha256"]
    assert code["recorded_execution_sha256"] == retained["code_sha256"]
    with pytest.raises(ValueError, match="source revision differs"):
        d.verify_historical_source(
            d.ROOT,
            "experiments/luna47f/PROTOCOL.md",
            "HEAD",
            retained["protocol_sha256"],
            d.PROTOCOL_REVISION,
        )
    with pytest.raises(ValueError, match="source identity differs"):
        d.verify_historical_source(
            d.ROOT,
            "experiments/luna47f/PROTOCOL.md",
            d.PROTOCOL_REVISION,
            "0" * 64,
            d.PROTOCOL_REVISION,
        )


def test_luna51_live_pre_post_guard_detects_mutation_but_ignores_unrelated_evolution(tmp_path):
    protected = tmp_path / "input.json"
    protected.write_bytes(b'{"value":1}\n')
    before = d.protected_snapshot(tmp_path, ("input.json",))
    (tmp_path / "later-governance.md").write_text("new reviewed record")
    after_unrelated = d.protected_snapshot(tmp_path, ("input.json",))
    d.verify_live_nonmutation(before, after_unrelated)

    protected.write_bytes(b'{"value":2}\n')
    after_mutation = d.protected_snapshot(tmp_path, ("input.json",))
    with pytest.raises(ValueError, match="changed during verification"):
        d.verify_live_nonmutation(before, after_mutation)


def test_luna51_retained_artifact_hashes_reject_result_and_validation_substitution(tmp_path):
    source_result = d.ROOT / "artifacts/luna47f/diagnostic.json"
    source_validation = d.ROOT / "artifacts/luna47f/validation.json"
    result_path = tmp_path / "artifacts/luna47f/diagnostic.json"
    validation_path = tmp_path / "artifacts/luna47f/validation.json"
    result_path.parent.mkdir(parents=True)
    result_bytes = source_result.read_bytes()
    validation_bytes = source_validation.read_bytes()
    result_path.write_bytes(result_bytes)
    validation_path.write_bytes(validation_bytes)

    assert d.verify_retained_files(tmp_path)["schema"] == "TPCN-LUNA47F-REPLAY-1"

    result_path.write_bytes(result_bytes + b" ")
    with pytest.raises(ValueError, match="result identity differs"):
        d.verify_retained_files(tmp_path)
    result_path.write_bytes(result_bytes)
    validation_path.write_bytes(validation_bytes + b" ")
    with pytest.raises(ValueError, match="validation identity differs"):
        d.verify_retained_files(tmp_path)


def test_fixed_output_guard_and_existing_output(tmp_path, monkeypatch):
    monkeypatch.setattr(d, "ROOT", tmp_path)
    output = d.safe_output()
    output.parent.mkdir(parents=True)
    output.write_bytes(b"unchanged")
    with pytest.raises(ValueError, match="already exists"):
        d.run()
    assert output.read_bytes() == b"unchanged"


def test_retained_analysis_content_checked_even_with_matching_hash(graph):
    analysis = d.classify(graph, "source", "destination")
    result = {
        "analysis": analysis,
        "analysis_sha256": d.sha(d.canonical(analysis)),
        "protocol_sha256": "protocol-hash",
        "source_inventory": {},
        "non_mutation": {"pre": {}},
        "code_sha256": "code-hash",
    }
    retained = deepcopy(result)
    retained["analysis"]["capacity_status"] = "CORRUPTED"
    retained["analysis_sha256"] = d.sha(d.canonical(retained["analysis"]))
    with pytest.raises(ValueError, match="retained analysis drift"):
        d.validate_retained(retained, result, {}, {})


def test_retained_protocol_hash_checked(graph):
    analysis = d.classify(graph, "source", "destination")
    result = {
        "analysis": analysis,
        "analysis_sha256": d.sha(d.canonical(analysis)),
        "protocol_sha256": "protocol-hash",
        "source_inventory": {},
        "non_mutation": {"pre": {}},
        "code_sha256": "code-hash",
    }
    retained = deepcopy(result)
    retained["protocol_sha256"] = "corrupted-protocol-hash"
    with pytest.raises(ValueError, match="retained protocol drift"):
        d.validate_retained(retained, result, {}, {})


def test_no_production_imports():
    import ast
    tree = ast.parse(FILE.read_text())
    imports = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    imports += [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
    assert not any(name and (name.startswith(("tpcn", "run_", "scripts"))) for name in imports)


def test_luna51_exact_git_materialization_only():
    original = b'{"unchanged":1}\n'
    assert d.verify_materialization(original, original) == "exact"
    assert d.verify_materialization(original.replace(b"\n", b"\r\n"), original).startswith("exact-Git")
    for changed in (
        b'{"unchanged":2}\r\n',
        original + b" ",
        original.replace(b"\n", b"\r\n", 1) + b"\n",
        original.replace(b"\n", b"\r"),
        original.rstrip(b"\n"),
        original + b"\x00",
    ):
        with pytest.raises(ValueError, match="beyond"):
            d.verify_materialization(changed, original)


def _cli_repository(tmp_path):
    repo = tmp_path / "repo"
    subprocess.run(
        ["git", "clone", "--quiet", "--shared", str(d.ROOT), str(repo)],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(["git", "config", "user.name", "Luna-52 CLI tests"],
                   cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "luna52-cli@example.invalid"],
                   cwd=repo, check=True)
    current_diagnostic = repo / "experiments/luna47f/diagnostic.py"
    current_diagnostic.write_bytes(FILE.read_bytes())
    subprocess.run(
        ["git", "add", "experiments/luna47f/diagnostic.py"],
        cwd=repo,
        check=True,
    )
    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet", "--",
         "experiments/luna47f/diagnostic.py"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if staged.returncode == 1:
        subprocess.run(
            ["git", "commit", "-m", "apply reviewed Luna-52 verification ownership"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
    elif staged.returncode != 0:
        raise subprocess.CalledProcessError(
            staged.returncode, staged.args, output=staged.stdout, stderr=staged.stderr
        )
    status = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=repo, text=True
    )
    if status:
        raise AssertionError(f"CLI repository baseline is not clean:\n{status}")
    return repo


def _git(repo, *args):
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def test_luna52_cli_repository_accepts_already_committed_verifier(tmp_path):
    repo = _cli_repository(tmp_path)

    assert (repo / "experiments/luna47f/diagnostic.py").read_bytes() == FILE.read_bytes()
    assert _git(repo, "rev-parse", "HEAD") == _git(d.ROOT, "rev-parse", "HEAD")
    assert not _git(repo, "status", "--porcelain")


def test_luna52_cli_repository_commits_changed_verifier(tmp_path, monkeypatch):
    changed_verifier = tmp_path / "diagnostic.py"
    changed_verifier.write_bytes(FILE.read_bytes() + b"\n# isolated bootstrap fixture\n")
    monkeypatch.setattr(sys.modules[__name__], "FILE", changed_verifier)

    repo = _cli_repository(tmp_path)

    assert (repo / "experiments/luna47f/diagnostic.py").read_bytes() == changed_verifier.read_bytes()
    assert _git(repo, "rev-parse", "HEAD") != _git(d.ROOT, "rev-parse", "HEAD")
    assert not _git(repo, "status", "--porcelain")

    _commit_change(
        repo,
        "artifacts/luna45-acp0008-depth2-destination-integration-20261006/config.json",
        (repo / "artifacts/luna45-acp0008-depth2-destination-integration-20261006/config.json")
        .read_bytes() + b" ",
    )
    assert not _git(repo, "status", "--porcelain")


def _commit_change(repo, relative, content):
    target = repo / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    subprocess.run(["git", "add", relative], cwd=repo, check=True)
    subprocess.run(
        ["git", "commit", "-m", "isolated Luna-52 adversarial fixture"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


def _run_public_check(repo, env=None):
    command = [
        sys.executable,
        str(repo / "experiments/luna47f/diagnostic.py"),
        "--check",
    ]
    result = subprocess.run(
        command,
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert result.args == command
    return result


def test_luna52_public_check_rejects_consumed_input_mutation(tmp_path):
    repo = _cli_repository(tmp_path)
    path = d.CONSUMED_INPUTS[0]
    target = repo / path
    _commit_change(repo, path, target.read_bytes() + b" ")
    result = _run_public_check(repo)
    assert result.returncode != 0
    assert "baseline input bytes differ beyond Git newline materialization" in result.stderr


def test_luna52_public_check_rejects_historical_identity_substitution(tmp_path):
    repo = _cli_repository(tmp_path)
    path = d.CONSUMED_INPUTS[0]
    target = repo / path
    _commit_change(repo, path, target.read_bytes() + b" ")
    subprocess.run(
        ["git", "replace", d.BASE, "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    result = _run_public_check(repo)
    assert result.returncode != 0
    assert "historical input Git object identity differs" in result.stderr


@pytest.mark.parametrize("path", [
    "experiments/luna47f/PROTOCOL.md",
    "artifacts/luna45-acp0008-depth2-destination-integration-20261006/config.json",
])
def test_luna52_public_check_rejects_protocol_and_configuration_mutation(tmp_path, path):
    repo = _cli_repository(tmp_path)
    target = repo / path
    _commit_change(repo, path, target.read_bytes() + b" ")
    result = _run_public_check(repo)
    assert result.returncode != 0
    assert ("historical source" in result.stderr.lower()
            or "baseline input bytes differ" in result.stderr.lower())


@pytest.mark.parametrize("path", [
    "artifacts/luna47f/diagnostic.json",
    "artifacts/luna47f/validation.json",
])
def test_luna52_public_check_rejects_retained_evidence_mutation(tmp_path, path):
    repo = _cli_repository(tmp_path)
    target = repo / path
    _commit_change(repo, path, target.read_bytes() + b" ")
    result = _run_public_check(repo)
    assert result.returncode != 0
    assert "retained Luna47F" in result.stderr
    assert "identity differs" in result.stderr


def test_luna52_public_check_rejects_same_path_content_substitution(tmp_path):
    repo = _cli_repository(tmp_path)
    path = d.CONSUMED_INPUTS[3]
    _commit_change(repo, path, b'{"substituted":true}\n')
    result = _run_public_check(repo)
    assert result.returncode != 0
    assert "baseline input bytes differ beyond Git newline materialization" in result.stderr


def test_luna52_public_check_accepts_unrelated_evolution(tmp_path):
    repo = _cli_repository(tmp_path)
    governance = "workflow/handoffs/luna52-unrelated-governance-test.txt"
    unrelated_source = "tests/test_luna52_unrelated_source.py"
    _commit_change(repo, governance, b"later independent governance record\n")
    _commit_change(repo, unrelated_source, b"def unrelated_test():\n    return True\n")
    result = _run_public_check(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS: retained analysis, replay, inputs, code and protected hashes" in result.stdout


def test_luna52_public_check_accepts_exact_git_crlf_materialization(tmp_path):
    repo = _cli_repository(tmp_path)
    path = d.CONSUMED_INPUTS[0]
    subprocess.run(["git", "config", "core.autocrlf", "true"], cwd=repo, check=True)
    subprocess.run(["git", "checkout", "--force", "--", path], cwd=repo, check=True)
    result = _run_public_check(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS: retained analysis, replay, inputs, code and protected hashes" in result.stdout


def test_luna52_public_check_detects_live_mutation(tmp_path):
    repo = _cli_repository(tmp_path)
    shim = tmp_path / "python-startup"
    shim.mkdir()
    (shim / "sitecustomize.py").write_text(
        "import inspect\n"
        "import os\n"
        "from pathlib import Path\n"
        "target = Path(os.environ['LUNA52_MUTATION_TARGET']).resolve()\n"
        "original = Path.read_bytes\n"
        "mutated = False\n"
        "def instrumented_read_bytes(path):\n"
        "    global mutated\n"
        "    data = original(path)\n"
        "    frame = inspect.currentframe().f_back\n"
        "    in_snapshot = False\n"
        "    while frame is not None:\n"
        "        if frame.f_code.co_name == 'protected_snapshot':\n"
        "            in_snapshot = True\n"
        "            break\n"
        "        frame = frame.f_back\n"
        "    if not mutated and in_snapshot and path.resolve() == target:\n"
        "        path.write_bytes(data + b' ')\n"
        "        mutated = True\n"
        "    return data\n"
        "Path.read_bytes = instrumented_read_bytes\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["LUNA52_MUTATION_TARGET"] = str(repo / "artifacts/luna47f/validation.json")
    env["PYTHONPATH"] = str(shim) + os.pathsep + env.get("PYTHONPATH", "")
    result = _run_public_check(repo, env)
    assert result.returncode != 0
    assert "protected live input changed during verification" in result.stderr
