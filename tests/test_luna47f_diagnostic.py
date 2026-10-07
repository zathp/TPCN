"""Synthetic unit fixtures only; retained scoring runs after protocol commit."""
from copy import deepcopy
import importlib.util
from pathlib import Path

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


@pytest.mark.parametrize("limit", ["fan_in_limit", "fan_out_limit", "edge_capacity", "routing_capacity"])
def test_saturation(graph, limit):
    graph[limit] = 1 if limit.startswith("fan_") else 2
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


def test_fixed_output_guard_and_existing_output(tmp_path, monkeypatch):
    monkeypatch.setattr(d, "ROOT", tmp_path)
    output = d.safe_output()
    output.parent.mkdir(parents=True)
    output.write_bytes(b"unchanged")
    with pytest.raises(ValueError, match="already exists"):
        d.run()
    assert output.read_bytes() == b"unchanged"


def test_no_production_imports():
    import ast
    tree = ast.parse(FILE.read_text())
    imports = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    imports += [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
    assert not any(name and (name.startswith(("tpcn", "run_", "scripts"))) for name in imports)


def test_exact_git_materialization_only():
    original = b'{"unchanged":1}\n'
    assert d.verify_materialization(original, original) == "exact"
    assert d.verify_materialization(original.replace(b"\n", b"\r\n"), original).startswith("exact-Git")
    with pytest.raises(ValueError, match="beyond"):
        d.verify_materialization(b'{"unchanged":2}\r\n', original)
    with pytest.raises(ValueError, match="beyond"):
        d.verify_materialization(original+b"\n", original)
