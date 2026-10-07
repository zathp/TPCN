"""Standard-library, downstream-only retained replay; never imports production."""
from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import json
import math
from pathlib import Path
import platform
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
AUTH = "789dda5988daf72f375d9713bd76a6da2b9e8b34"
BASE = "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
L45 = "artifacts/luna45-acp0008-depth2-destination-integration-20261006"
WINDOW = 4.0
RATIO = 0.5
LIMIT = 100 * 1024 * 1024


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_materialization(working, pinned):
    """Permit only Git's exact LF->CRLF checkout transform, without editing inputs."""
    if working == pinned:
        return "exact"
    require(b"\r\n" not in pinned and working == pinned.replace(b"\n", b"\r\n"),
            "baseline input bytes differ beyond Git newline materialization")
    return "exact-Git-LF-to-CRLF-checkout"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT)


def finite(value):
    require(type(value) in (int, float) and math.isfinite(value), "nonfinite scalar")
    return float(value)


def bits(value):
    return struct.pack(">d", finite(value)).hex()


def equation(a, b):
    a, b = finite(a), finite(b)
    require(abs(a-b) <= 64 * sys.float_info.epsilon * max(1, abs(a), abs(b)),
            "equation mismatch")


def compatible(a, b):
    a, b = finite(a), finite(b)
    similarity = min(abs(a), abs(b))/max(abs(a), abs(b)) if a and b else None
    ok = bool(a and b and (a > 0) == (b > 0) and similarity >= RATIO)
    return ok, similarity


def distance(graph, source, target):
    """Shortest existing hop path only; never inserts a hypothetical edge."""
    queue = deque([(source, 0, 0.0)])
    seen = {source}
    while queue:
        node, hops, delay = queue.popleft()
        if node == target:
            return hops, delay
        for edge in graph["edges"]:
            if edge["source"] == node and edge["destination"] not in seen:
                seen.add(edge["destination"])
                queue.append((edge["destination"], hops+1, delay+edge["delay"]))
    return None, None


def classify(graph, source, target):
    edges = graph["edges"]
    duplicate = any(e["source"] == source and e["destination"] == target for e in edges)
    cycle = distance(graph, target, source)[0] is not None
    incoming = {e["source"] for e in edges if e["destination"] == target}
    outgoing = {e["destination"] for e in edges if e["source"] == source}
    usage = {"fan_in_limit": len(incoming), "fan_out_limit": len(outgoing),
             "edge_capacity": len(edges),
             "routing_capacity": sum(e["source"] == source for e in edges)}
    saturated = {k: usage[k] >= graph[k] if k in graph else None for k in usage}
    feasible = None if None in saturated.values() else not any(saturated.values()) and not duplicate and not cycle
    hops, delay = distance(graph, source, target)
    return {"existing_edge_duplicate": duplicate, "cycle_forming": cycle,
            "saturated": saturated, "capacity_status": "BLOCKED" if feasible is None else "OBSERVED",
            "capacity_feasible_novel": feasible, "existing_shortest_hops": hops,
            "existing_shortest_path_delay": delay,
            "predicted_hop_reduction": hops-1 if not duplicate and hops and hops > 1 else 0,
            "fan_in_opportunity": not duplicate and bool(incoming - {source}),
            "prospective_delay_reduction": None, "prospective_delay_status": "BLOCKED",
            "local_observation_availability": "BLOCKED", "usable_edge": None}


def row(family, stream, source, target, a, b, chain, graph):
    require(source["node"] != target["node"], "self pair")
    lag = finite(target["time"]) - finite(source["time"])
    ok, similarity = compatible(a, b)
    return {"family": family, "stream_id": stream, "source": source, "target": target,
            "candidate_time": target["time"], "lag": lag,
            "source_delta": a, "target_delta": b, "delta_similarity": similarity,
            "delta_compatible": ok, "strict_causal_direction": lag > 0,
            "in_window": 0 < lag <= WINDOW, "opportunity": ok and 0 < lag <= WINDOW,
            "causal_chain": chain, "trigger_identity_proven": True,
            "classification": classify(graph, source["node"], target["node"])}


def keyed(items, key):
    result = {}
    for index, item in enumerate(items):
        identity = key(item)
        require(identity not in result, "duplicate retained identity")
        result[identity] = (index, item)
    return result


def ref(node, event, time, pointer, roots_truncated=False):
    return {"node": node, "event_id": event, "time": time, "trace": "phase",
            "json_pointer": pointer, "roots_truncated": roots_truncated}


def deposit(record, event, node):
    traces = record[node+"_integration_trace"]
    matches = [(i, t) for i, t in enumerate(traces)
               if t["timestamp"] == event["reception_timestamp"]
               and bits(t["input_value"]) == event["payload_bits"]]
    require(len(matches) == 1, "ambiguous/missing local deposition")
    index, trace = matches[0]
    equation(trace["x_after_input"]-trace["x_after_decay"], event["payload"])
    return index, trace


def annotate_repetition(rows):
    repeated = Counter()
    for candidate in rows:
        key = (candidate["family"], candidate["stream_id"],
               candidate["source"]["node"], candidate["target"]["node"])
        candidate["repeated_endpoint_proposal"] = candidate["opportunity"] and repeated[key] > 0
        if candidate["opportunity"]:
            repeated[key] += 1


def analyze(phase, enqueues, receptions, graph):
    require(len(phase["records"]) == 320, "stream budget")
    eqs = keyed(enqueues["per_sequence"], lambda s: s["stream_id"])
    rxs = keyed(receptions["per_sequence"], lambda s: s["stream_id"])
    rows, reconciled, truncated, coincidences = [], 0, 0, 0
    seen_streams = set()
    for record_index, record in enumerate(phase["records"]):
        sid = record["stream_id"]
        require(not record["destination_emissions"], "destination emission association needs explicit trigger reconciliation")
        require(sid not in seen_streams, "duplicate stream")
        seen_streams.add(sid)
        ep, rp = eqs[sid][1]["events"], rxs[sid][1]["events"]
        require(len(ep) <= 4096 and len(ep) == len(rp), "route budget/count")
        event_key = lambda e: (e["source"], e["destination"], e["event_id"], e["queue_sequence"])
        emap, rmap = keyed(ep, event_key), keyed(rp, event_key)
        require(emap.keys() == rmap.keys(), "orphan route")
        require(record["routing_enqueue_events"] == ep and record["receiver_reception_events"] == rp,
                "raw/phase route identity")
        high = record["resource_high_water"]
        for field in ("fan_in_limit", "fan_out_limit", "edge_capacity", "routing_capacity"):
            require(high["topology_"+field] == graph[field], "capacity configuration mismatch")
        require(high["topology_edge_peak"] == len(graph["edges"]), "edge occupancy mismatch")
        emissions = {}
        prefix = f"/records/{record_index}"
        for node in graph["nodes"]:
            emissions[node] = keyed(record[node+"_emissions"], lambda e: e["event_id"])

        def emission(node, event_id):
            i, e = emissions[node][event_id]
            return e, ref(node, event_id, e["timestamp"],
                          prefix+f"/{node}_emissions/{i}")

        def reception_reference(e, i):
            return ref(e["destination"], e["event_id"], e["reception_timestamp"],
                       prefix+f"/receiver_reception_events/{i}", e["roots_truncated"])

        def trigger(relay):
            check = relay["integration_trace_check"]
            require(check["matches"] and check["trace_emission_id"] == relay["event_id"],
                    "relay trigger check")
            matches = [(i, e) for i, e in enumerate(rp)
                       if e["destination"] == "relay" and e["event_id"] == check["event_id"]
                       and e["reception_timestamp"] == check["timestamp"]]
            require(len(matches) == 1, "relay trigger identity")
            i, e = matches[0]
            ti, t = deposit(record, e, "relay")
            require(t["emission_id"] == relay["event_id"] and
                    t["emission_timestamp"] == relay["timestamp"], "trigger emission mismatch")
            require(bits(check["input_value"]) == e["payload_bits"], "trigger input mismatch")
            trajectory = [v for v in record["relay_state_trajectory"]
                          if v["event_id"] == e["event_id"] and v["timestamp"] == check["timestamp"]]
            require(len(trajectory) == 1, "trigger trajectory mismatch")
            return i, e, ti, t

        for identity, (i, receive) in rmap.items():
            _, enqueue = emap[identity]
            for field in ("source", "destination", "event_id", "originating_emission_id",
                          "payload", "payload_bits", "payload_encoding", "lineage_id",
                          "route_depth", "route_path", "causal_roots", "roots_truncated",
                          "queue_sequence", "scheduled_delivery_timestamp"):
                require(enqueue[field] == receive[field], "enqueue/reception mismatch: "+field)
            require(bits(receive["payload"]) == receive["payload_bits"], "payload bits")
            require(receive["reception_timestamp"] == enqueue["scheduled_delivery_timestamp"],
                    "reception time mismatch")
            source, target = receive["source"], receive["destination"]
            edges = [e for e in graph["edges"] if e["source"] == source and e["destination"] == target]
            require(len(edges) == 1 and edges[0]["delay"] > 0, "unknown route")
            e, er = emission(source, receive["event_id"])
            require(enqueue["enqueue_timestamp"] == e["timestamp"], "enqueue emission time")
            equation(receive["reception_timestamp"], e["timestamp"]+edges[0]["delay"])
            require(receive["reception_timestamp"] > e["timestamp"], "nonfuture route")
            require(receive["route_path"] == [source, target], "route path")
            equation(receive["payload"], math.tanh(e["payload"]*edges[0]["w"]))
            ti, t = deposit(record, receive, target)
            rr = reception_reference(receive, i)
            direct = row("output-drive-proxy", sid, er, rr, e["payload"], t["input_value"],
                         [er, rr], graph)
            direct["target_canonical_emission_association"] = False
            if target == "relay":
                direct["target_canonical_emission_association"] = any(
                    re["integration_trace_check"]["event_id"] == receive["event_id"] and
                    0 < re["timestamp"]-rr["time"] <= WINDOW
                    for _, re in emissions["relay"].values())
            direct["target_state_deposition_observed"] = True
            rows.append(direct)
            reconciled += 1
            truncated += int(receive["roots_truncated"])
            if target != "destination":
                continue
            ri, reception, rti, trace = trigger(e)
            se, sr = emission("source", reception["event_id"])
            relay_ref = reception_reference(reception, ri)
            chain = [sr, relay_ref, er, rr]
            require(all(chain[j]["time"] < chain[j+1]["time"] for j in range(3)),
                    "noncausal trigger chain")
            proxy = row("output-drive-proxy", sid, sr, rr, se["payload"], t["input_value"],
                        chain, graph)
            local_source = ref("relay", reception["event_id"], trace["timestamp"],
                               prefix+f"/relay_integration_trace/{rti}", reception["roots_truncated"])
            local_target = ref("destination", receive["event_id"], t["timestamp"],
                               prefix+f"/destination_integration_trace/{ti}", receive["roots_truncated"])
            local = row("local-deposition", sid, local_source, local_target,
                        trace["input_value"], t["input_value"], chain, graph)
            for candidate in (proxy, local):
                candidate["target_canonical_emission_association"] = False
                candidate["target_state_deposition_observed"] = True
                rows.append(candidate)
            # Same-stream temporal coincidence control; no fake times/ancestry.
            for _, other in emissions["source"].values():
                if other["event_id"] != se["event_id"]:
                    lag = rr["time"] - other["timestamp"]
                    if 0 < lag <= WINDOW and compatible(other["payload"], t["input_value"])[0]:
                        coincidences += 1

    require(seen_streams == set(eqs) == set(rxs), "stream identity mismatch")
    annotate_repetition(rows)
    summaries = {}
    for family in ("output-drive-proxy", "local-deposition"):
        selected = [r for r in rows if r["family"] == family]
        opportunities = [r for r in selected if r["opportunity"]]
        novel = [r for r in opportunities if r["classification"]["capacity_feasible_novel"]]
        summaries[family] = {
            "enumerated_pairs": len(selected), "candidate_opportunities": len(opportunities),
            "unique_streams": len({r["stream_id"] for r in opportunities}),
            "unique_endpoint_pairs": sorted({(r["source"]["node"], r["target"]["node"])
                                            for r in opportunities}),
            "existing_edge_duplicates": sum(r["classification"]["existing_edge_duplicate"] for r in opportunities),
            "repeated_endpoint_proposals": sum(r["repeated_endpoint_proposal"] for r in opportunities),
            "cycle_forming": sum(r["classification"]["cycle_forming"] for r in opportunities),
            "saturated": {k: sum(r["classification"]["saturated"][k] is True for r in opportunities)
                          for k in ("fan_in_limit", "fan_out_limit", "edge_capacity", "routing_capacity")},
            "novel_capacity_feasible": len(novel),
            "shortening_opportunities": sum(r["classification"]["predicted_hop_reduction"] > 0 for r in novel),
            "fan_in_creation_opportunities": sum(r["classification"]["fan_in_opportunity"] for r in novel),
            "target_emission_associations": sum(r["target_canonical_emission_association"] for r in opportunities),
            "novel_target_emission_associations": sum(r["target_canonical_emission_association"] for r in novel),
            "compatible_outside_window": sum(r["delta_compatible"] and not r["in_window"] for r in selected),
            "lag_band_4_to_8": sum(r["delta_compatible"] and WINDOW < r["lag"] <= 2*WINDOW for r in selected),
            "reverse_order_exclusions": len(selected),
            "candidate_lags": dict(sorted(Counter(str(r["lag"]) for r in opportunities).items())),
        }
    proxy_count = summaries["output-drive-proxy"]["novel_capacity_feasible"]
    return {"rows": rows, "summary": summaries, "reconciled_route_pairs": reconciled,
            "truncated_root_route_pairs": truncated, "streams": len(seen_streams),
            "compatible_nontrigger_temporal_coincidences": coincidences,
            "verdict": "PARTIALLY SUPPORTED" if proxy_count else "NOT SUPPORTED",
            "blocked_metrics": {
                "source_intrinsic_state_delta_compatibility": "Source pre/post update states not retained.",
                "source_local_candidate_availability": "No downstream observation return channel retained.",
                "new_edge_delay_and_delay_reduction": "No proposed edge configuration; hop reduction is analytical only.",
                "usable_reachable_candidate_edges": "No admission, locality validation or counterfactual routing authorized.",
                "task_utility_and_efficacy": "No intervention/task scoring authorized; state deposition is not utility.",
                "complete_causal_ancestry": "Bounded roots may truncate; only exact trigger chains are proven.",
            }}


def owned(path):
    return (path.startswith(("experiments/luna47f/", "artifacts/luna47f/")) or
            path.startswith("tests/test_luna47f_") and path.endswith(".py") or
            path == "workflow/handoffs/luna-47f-candidate-generation-diagnostic-20261006.md")


def protected_snapshot():
    paths = git("ls-files", "-z").decode().split("\0")
    return {p: sha((ROOT/p).read_bytes()) for p in sorted(paths) if p and not owned(p)}


def safe_output():
    path = ROOT/"artifacts/luna47f/diagnostic.json"
    for component in (ROOT, ROOT/"artifacts", path.parent, path):
        require(not component.is_symlink(), "symlink output")
        if component.exists():
            attributes = getattr(component.stat(), "st_file_attributes", 0)
            require(not attributes & 0x400, "reparse output")
    return path


def validate_retained(retained, result, inventory, pre):
    require(canonical(retained["analysis"]) == canonical(result["analysis"]),
            "retained analysis drift")
    require(retained["analysis_sha256"] == result["analysis_sha256"], "retained analysis hash drift")
    require(retained["protocol_sha256"] == result["protocol_sha256"], "retained protocol drift")
    require(retained["source_inventory"] == inventory, "retained input drift")
    require(retained["non_mutation"]["pre"] == pre, "protected snapshot drift")
    require(retained["code_sha256"] == result["code_sha256"], "code drift")


def run(check=False):
    output = safe_output()
    require(check or not output.exists(), "output already exists; use --check")
    changed = git("diff", "--name-only", AUTH).decode().splitlines()
    require(all(owned(p) for p in changed), "non-owned change")
    pre = protected_snapshot()
    inventory, loaded = {}, {}
    names = ["config.json", "artifact-integrity.json", "summary.json"]
    for phase in ("initial", "replay"):
        names += [f"{phase}-destination_calibrated{suffix}.json" for suffix in ("", "-enqueue", "-reception")]
    paths = [L45+"/"+n for n in names] + [
        "artifacts/luna44-canonical-fixture/fixture.json",
        "artifacts/luna44-canonical-fixture/provenance.json",
        "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json",
    ]
    # Fixture filename is checked against committed provenance rather than guessed.
    manifest_path = "artifacts/luna44-canonical-fixture/provenance.json"
    manifest = json.loads((ROOT/manifest_path).read_bytes())
    paths[paths.index("artifacts/luna44-canonical-fixture/fixture.json")] = manifest["fixture_path"]
    for path in paths:
        data = (ROOT/path).read_bytes()
        require(len(data) <= LIMIT, "input size limit")
        pinned = git("show", BASE+":"+path)
        materialization = verify_materialization(data, pinned)
        inventory[path] = {"sha256": sha(data), "bytes": len(data),
                           "published_sha256": sha(pinned), "published_bytes": len(pinned),
                           "checkout_materialization": materialization,
                           "baseline_git_blob": git("rev-parse", BASE+":"+path).decode().strip()}
        loaded[path] = json.loads(pinned)
        if "artifact_digest" in loaded[path]:
            body = {k: v for k, v in loaded[path].items() if k != "artifact_digest"}
            require(sha(canonical(body)) == loaded[path]["artifact_digest"], "internal digest: "+path)
    catalog = loaded[L45+"/artifact-integrity.json"]
    for name in names:
        if name == "artifact-integrity.json":
            continue
        identity = inventory[L45+"/"+name]
        published = catalog["files"][name]
        require(identity["published_sha256"] == published["file_sha256"] and
                identity["published_bytes"] == published["byte_length"], "catalog file pin")
        require(loaded[L45+"/"+name]["artifact_digest"] == published["artifact_digest"], "catalog digest pin")
    config = loaded[L45+"/config.json"]
    require(sha(canonical(config["experiment"])) == config["config_digest"], "configuration digest")
    graph = config["experiment"]["topology"]
    require(config["experiment"]["structural_plasticity"] is False, "growth enabled")
    initial, replay = [
        analyze(*(loaded[L45+f"/{p}-destination_calibrated{s}.json"] for s in ("", "-enqueue", "-reception")), graph)
        for p in ("initial", "replay")]
    require(canonical(initial) == canonical(replay), "replay analysis differs")
    l46 = loaded["artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json"]
    # Preserve complete retained output identity; no recomputation/reinterpretation.
    post = protected_snapshot()
    require(pre == post, "protected file changed")
    result = {"schema": "TPCN-LUNA47F-REPLAY-1", "authorization_revision": AUTH,
              "evidence_baseline": BASE, "execution_revision": git("rev-parse", "HEAD").decode().strip(),
              "code_sha256": sha(Path(__file__).read_bytes()),
              "protocol_sha256": sha((Path(__file__).parent/"PROTOCOL.md").read_bytes()),
              "environment": {"python": sys.version, "platform": platform.platform(),
                              "epsilon": sys.float_info.epsilon, "executable": sys.executable},
              "rules": {"window": WINDOW, "similarity_min": RATIO, "equation_epsilon_multiple": 64,
                        "units": "retained logical time and scalar signed drive",
                        "reset": "per stream", "max_streams": 320, "max_routes_per_stream": 4096},
              "source_inventory": inventory, "retained_configuration": config,
              "luna46_preserved": {"sha256": inventory["artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json"]["sha256"],
                                   "verdict": "MIXED", "retained_schema": l46.get("schema")},
              "analysis": initial, "replay_equal": True, "analysis_sha256": sha(canonical(initial)),
              "non_mutation": {"pre": pre, "post": post, "equal": True,
                               "aggregate_sha256": sha(canonical(pre)),
                               "protected_tracked_files": len(pre)},
              "trace_roles": {p: {"phase": L45+f"/{p}-destination_calibrated.json",
                                  "enqueue": L45+f"/{p}-destination_calibrated-enqueue.json",
                                  "reception": L45+f"/{p}-destination_calibrated-reception.json"}
                              for p in ("initial", "replay")}}
    if check:
        retained = json.loads(output.read_bytes())
        validate_retained(retained, result, inventory, pre)
        print("PASS: retained analysis, replay, inputs, code and protected hashes")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as handle:
            handle.write(canonical(result)+b"\n")
        print(initial["verdict"], json.dumps(initial["summary"], sort_keys=True))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    run(parser.parse_args().check)
