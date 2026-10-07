"""Independent retained-data oracle: no worker or production imports.

Reads pinned Git objects and read-only checkouts. Writes only its own report.
Scientific equation comparisons use 64 epsilon (A/B/F) or 1e-12 (C/D/G);
identity, integers, thresholds, draw values and Git objects compare exactly.
"""
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import heapq
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
AUTH = "789dda5988daf72f375d9713bd76a6da2b9e8b34"
REFS = dict(zip("abcdefg", (
    "eb56684eaa10dc9b765927ef8e883c7d56cb025b",
    "41a0a28f6f85023b8933a47650f66628b0a9ceb0",
    "609b2e5f8a7ae123f9b7f7da5c89378e29353624",
    "deb01f07a0d6b315855d2fab57d558be303f95f3",
    "4e413415a31853877333810d7093f415f93f72f7",
    "8cddf9d5d3fc0ea6971dc54645e8033c290dc852",
    "42698364392901de955ca04a770c975a1b0a94d2")))
L45 = "artifacts/luna45-acp0008-depth2-destination-integration-20261006/"
L44 = "artifacts/luna44-acp0008-independent-routing-rerun-20261005/"
CHECKS = Counter()
MAX_RESIDUAL = defaultdict(float)
BLOB_CACHE = {}


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=root)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(ref, path):
    key = (ref, path)
    if key not in BLOB_CACHE:
        BLOB_CACHE[key] = git(ROOT, "show", f"{ref}:{path}")
    return BLOB_CACHE[key]


def load(letter, filename):
    return json.loads(blob(REFS[letter], f"artifacts/luna47{letter}/{filename}"))


def exact(a, b, what):
    if a != b:
        raise AssertionError(f"{what}: {str(a)[:200]} != {str(b)[:200]}")
    CHECKS[what] += 1


def close(a, b, what, tolerance=None):
    residual = abs(a - b)
    bound = tolerance if tolerance is not None else (
        64 * sys.float_info.epsilon * max(1, abs(a), abs(b)))
    if not math.isfinite(a) or not math.isfinite(b) or residual > bound:
        raise AssertionError(f"{what}: {a} != {b}; residual={residual}, bound={bound}")
    CHECKS[what] += 1
    MAX_RESIDUAL[what] = max(MAX_RESIDUAL[what], residual)


def canonical(value, newline=False, indent=None):
    return (json.dumps(value, sort_keys=True, allow_nan=False,
                       separators=None if indent else (",", ":"), indent=indent)
            + ("\n" if newline else "")).encode()


def owned(letter, path):
    return (path.startswith((f"experiments/luna47{letter}/",
                             f"artifacts/luna47{letter}/"))
            or path.startswith(f"tests/test_luna47{letter}_")
            or (path.startswith(f"workflow/handoffs/luna-47{letter}-")
                and path.endswith("-20261006.md")))


def inventory():
    report = {}
    for letter, ref in REFS.items():
        tree = ROOT.parent / f"luna47{letter}"
        exact(git(tree, "rev-parse", "HEAD").decode().strip(), ref, "pinned HEAD")
        exact(git(tree, "status", "--porcelain"), b"", "lane clean")
        git(tree, "merge-base", "--is-ancestor", AUTH, ref)
        changed = git(tree, "diff", "--name-only", AUTH, ref).decode().splitlines()
        exact(all(owned(letter, p) for p in changed), True, "lane ownership")
        rows = []
        for path in changed:
            committed, physical = blob(ref, path), (tree / path).read_bytes()
            status = ("exact" if committed == physical else
                      "exact LF-to-CRLF" if b"\r\n" not in committed and
                      committed.replace(b"\n", b"\r\n") == physical else "OTHER")
            exact(status != "OTHER", True, "changed-file materialization")
            rows.append(dict(path=path, git_blob=git(
                tree, "rev-parse", f"{ref}:{path}").decode().strip(),
                git_sha256=sha(committed), git_bytes=len(committed),
                file_sha256=sha(physical), file_bytes=len(physical),
                materialization=status))
        history = []
        for commit in git(tree, "rev-list", "--reverse", f"{AUTH}..{ref}").decode().splitlines():
            history.append(dict(commit=commit, metadata=git(
                tree, "show", "-s", "--format=%aI %cI %s", commit).decode().strip(),
                changed_paths=git(tree, "diff-tree", "--no-commit-id", "--name-only",
                                  "-r", commit).decode().splitlines()))
        report[letter] = dict(ref=ref, files=rows, history=history)
    return report


def source_integrity():
    catalog = json.loads(blob(BASE, L45 + "artifact-integrity.json"))
    sources = {}
    for name, pin in catalog["files"].items():
        path = L45 + name
        data = blob(BASE, path)
        exact(sha(data), pin["file_sha256"], "L45 catalog sha256")
        exact(len(data), pin["byte_length"], "L45 catalog length")
        doc = json.loads(data)
        body = {k: v for k, v in doc.items() if k != "artifact_digest"}
        exact(sha(canonical(body)), pin["artifact_digest"], "L45 internal digest")
        for letter, ref in REFS.items():
            exact(git(ROOT, "rev-parse", f"{ref}:{path}"),
                  git(ROOT, "rev-parse", f"{BASE}:{path}"), "shared evidence blob")
            physical = (ROOT.parent / f"luna47{letter}" / path).read_bytes()
            status = ("exact" if physical == data else
                      "exact LF-to-CRLF" if physical == data.replace(b"\n", b"\r\n")
                      else "OTHER")
            exact(status != "OTHER", True, "shared evidence materialization")
            sources[f"{letter}:{path}"] = dict(
                file_sha256=sha(physical), git_sha256=sha(data),
                file_bytes=len(physical), git_bytes=len(data), status=status)
    phases = []
    for phase in ("initial", "replay"):
        eq = json.loads(blob(BASE, L45 + f"{phase}-destination_calibrated-enqueue.json"))
        rx = json.loads(blob(BASE, L45 + f"{phase}-destination_calibrated-reception.json"))
        count, downstream = 0, 0
        for e, r in zip(eq["per_sequence"], rx["per_sequence"]):
            exact(e["stream_id"], r["stream_id"], "raw stream")
            lookup = {(x["source"], x["destination"], x["event_id"], x["queue_sequence"]): x
                      for x in e["events"]}
            exact(len(lookup), len(e["events"]), "unique raw enqueue")
            exact(len(e["events"]), len(r["events"]), "raw coverage")
            seen = set()
            for receive in r["events"]:
                key = tuple(receive[k] for k in ("source", "destination", "event_id", "queue_sequence"))
                exact(key not in seen, True, "unique raw reception")
                seen.add(key)
                queued = lookup[key]
                for k in ("payload", "payload_bits", "lineage_id", "causal_roots",
                          "roots_truncated", "route_depth", "route_path",
                          "scheduled_delivery_timestamp"):
                    exact(queued[k], receive[k], "raw identity " + k)
                exact(receive["reception_timestamp"], queued["scheduled_delivery_timestamp"], "raw arrival")
                count += 1
                downstream += receive["destination"] == "destination"
        exact(count, 1950, "raw total")
        exact(downstream, 235, "downstream total")
        phases.append(dict(phase=phase, pairs=count, downstream=downstream))
    return dict(catalog_files=len(catalog["files"]), phases=phases, materialization=sources)


def ab():
    retained = json.loads(blob(BASE, "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json"))
    exact(retained["verdict"], "MIXED", "preserved MIXED")
    exact(sha(canonical({k: v for k, v in retained.items() if k != "output_digest"})),
          retained["output_digest"], "L46 internal digest")
    aa, bb = load("a", "results.json"), load("b", "results.json")["result"]
    counts, rescue = Counter(), defaultdict(Counter)
    criticals, critical_target = [], []
    aindex = {s["stream_id"]: s for s in aa["primary"]}
    bindex = {s["stream_id"]: s for s in bb["sequences"]}
    for seq in retained["sequences"]:
        counts[seq["category"]] += 1
        payloads = {r["queue_sequence"]: r["payload"] for r in seq["recurrence_evidence"]}
        rows = seq["all_update_boundaries"]
        unit, maximum = 0.0, 0.0
        for row in rows:
            u = payloads[row["queue_sequence"]] if row["is_reception"] else 0.0
            unit = math.exp(-0.0125 * (row["timestamp"] - row["prior_clock"])) * unit + u
            close(unit, row["state_after"], "baseline recurrence")
            maximum = max(maximum, abs(unit))
        critical = 1 / maximum if maximum else None
        close(critical or 0, bindex[seq["stream_id"]]["derivation"]["critical_gain"] or 0,
              "B critical gain")
        if critical:
            criticals.append(critical)
            if seq["category"] == "DRIVE-LIMITED":
                critical_target.append(critical)
        for name, rate in aa["config"]["rates"].items():
            z, crosses = 0.0, False
            for row, saved in zip(rows, aindex[seq["stream_id"]]["variants"][name]["rows"]):
                u = payloads[row["queue_sequence"]] if row["is_reception"] else 0.0
                before = z * math.exp(-rate * (row["timestamp"] - row["prior_clock"]))
                z = max(-4.0, min(4.0, before + u))
                close(before, saved["retained_state"], "A retained state")
                close(z, saved["state_after"], "A state")
                exact(abs(z) >= 1, saved["crosses"], "A threshold")
                crosses |= abs(z) >= 1
            exact(crosses, aindex[seq["stream_id"]]["variants"][name]["crosses"], "A stream crossing")
            if crosses:
                rescue[name][seq["category"]] += 1
        for saved in bindex[seq["stream_id"]]["global_arms"] + bindex[seq["stream_id"]]["local_brackets"]:
            state, first = 0.0, None
            for row, event in zip(rows, saved["events"]):
                if first is not None:
                    exact(event["censored"], True, "B post-cross censor")
                    continue
                u = payloads[row["queue_sequence"]] if row["is_reception"] else 0.0
                state = max(-4.0, min(4.0, math.exp(-.0125 * row["dt"]) * state
                                     + saved["gain"] * u))
                close(state, event["state_input"], "B state")
                exact(abs(state) >= 1, event["crossed"], "B threshold")
                if abs(state) >= 1:
                    first = row["event_id"]
            exact(first is not None, saved["crosses"], "B first crossing")
    exact(dict(counts), {"NO-RECEPTIONS": 212, "TEMPORAL-RETENTION-LIMITED": 33,
                        "DRIVE-LIMITED": 75}, "L46 partition")
    historical = {}
    for name, rate in aa["config"]["rates"].items():
        crossings, clips = 0, 0
        for stream in aa["historical"]:
            z = 0.0
            crossing = False
            for saved in stream["variants"][name]["rows"]:
                raw = z * math.exp(-rate * saved["dt"]) + saved["payload"]
                z = max(-4.0, min(4.0, raw))
                clips += z != raw
                crossing |= abs(z) >= 1
                close(z, saved["state_after"], "A historical state")
            crossings += crossing
        exact(crossings, aa["historical_summary"][name]["crossing_streams"], "A historical count")
        exact(clips, aa["historical_summary"][name]["clipped_events"], "A historical clipping")
        historical[name] = dict(crossing_streams=crossings, clipped_events=clips)
    target_counts = []
    for i, gain in enumerate(bb["global_gains"]):
        target, other = 0, 0
        for s in bb["sequences"]:
            crossing = s["global_arms"][i]["crosses"]
            if s["category"] == "DRIVE-LIMITED":
                target += crossing
            else:
                other += crossing
        exact(target, bb["summaries"][i]["rescued"], "B rescue aggregate")
        exact(other, bb["summaries"][i]["unintended_crossings"], "B other aggregate")
        target_counts.append(dict(gain=gain, rescued=target, unintended=other))
    return dict(partition=dict(counts), A_rescues={k: dict(v) for k, v in rescue.items()},
                A_historical=historical, B_critical_range=[min(critical_target), max(critical_target)],
                B_critical_target_median=sorted(critical_target)[len(critical_target)//2],
                B_arms=target_counts)


def c():
    science = load("c", "replay.json")["science"]
    fixtures = {f["identity"]: f for f in science["fixtures"]}
    report = []
    for run in science["runs"]:
        fixture = fixtures[run["fixture"]]
        exact(len(fixture["inputs"]), 240, "C fixture capacity")
        for (t, value), b, n, s in zip(fixture["inputs"], fixture["baseline_truth"],
                                     fixture["noise_truth"], fixture["signal_truth"]):
            exact(value, b+n+s, "C fixture decomposition")
        config = run["configuration"]
        generated = []
        for control, saved_rows in ((False, run["events"]),
                                    (True, run["signal_free_control_events"])):
            baseline, noise, prior = 0.0, .25, None
            result = []
            for i, ((timestamp, raw), saved) in enumerate(zip(fixture["inputs"], saved_rows)):
                if control:
                    raw = fixture["baseline_truth"][i] + fixture["noise_truth"][i]
                dt = 1.0 if prior is None else timestamp - prior
                residual = raw - baseline
                excess = math.copysign(max(abs(residual) - 2 * noise, 0.0), residual)
                newb = max(-4, min(4, baseline - math.expm1(-dt/20) *
                                  max(-.25, min(.25, residual))))
                target = abs(residual)
                if run["method"] == "robust":
                    target = min(target, 2*noise)
                newn = noise if run["method"] == "fixed" else max(
                    .05, min(16, noise - math.expm1(-dt/4) * (target-noise)))
                for key, value in (("B", baseline), ("N", noise), ("E", excess),
                                   ("B_after", newb), ("N_after", newn)):
                    close(value, saved[key], "C " + key, 1e-12)
                exact(excess != 0, saved["E"] != 0, "C admission")
                result.append(dict(E=excess, B=baseline, N=noise, B_after=newb, N_after=newn))
                baseline, noise, prior = newb, newn, timestamp
            generated.append(result)
        events, controls = generated
        truth = fixture["signal_truth"]
        false = sum(e["E"] != 0 and s == 0 for e, s in zip(events, truth))
        missed = sum(e["E"] == 0 and s != 0 for e, s in zip(events, truth))
        exact(false, run["metrics"]["false_admissions"], "C false admissions")
        exact(missed, run["metrics"]["missed_meaningful"], "C misses")
        report.append(dict(fixture=run["fixture"], method=run["method"],
                           false_admissions=false, misses=missed))
    return dict(fixtures=len(fixtures), runs=len(report), tested_and_control_events=23040,
                metrics=report)


def simulate_d(fixture, cfg):
    # Independent priority-queue formulation of the declared synthetic drain.
    pending = False
    queue = [(Fraction(e["time"]), 0, i, e["drive"], e["id"])
             for i, e in enumerate(fixture["inputs"])]
    heapq.heapify(queue)
    state, prior, serial = 0.0, Fraction(0), len(queue)
    outputs, boundaries = [], []
    while queue:
        t, kind, _, drive, identity = heapq.heappop(queue)
        before = state * math.exp(-cfg["leak"] * float(t-prior))
        state = before + drive
        if kind == 1:
            pending = False
            if abs(state) >= cfg["theta"]:
                outputs.append((str(t), 1 if state > 0 else -1))
                state = math.copysign(max(0.0, abs(state)-cfg["quantum"]), state)
        if abs(state) >= cfg["theta"] and not pending:
            serial += 1
            heapq.heappush(queue, (t+Fraction(cfg["period"]), 1, serial, 0.0, None))
            pending = True
        boundaries.append((str(t), before, state))
        prior = t
    horizon = (Fraction(fixture["inputs"][-1]["time"])
               if fixture["inputs"] else Fraction(0)) + Fraction(cfg["tail"])
    final = state * math.exp(-cfg["leak"] * float(horizon-prior))
    return outputs, boundaries, final


def d():
    doc = load("d", "evidence.json")["analysis"]
    records = doc["initial"]
    report = []
    exact(records, doc["replay"], "D exact phase replay")
    for record in records:
        outputs, trace, final = simulate_d(record["trajectory"], record["configuration"])
        exact(outputs, [(o["time"], o["sign"]) for o in record["outputs"]], "D output identities/time/sign")
        actual = [r for r in record["trace"] if r["kind"] != "observation"]
        exact(len(trace), len(actual), "D trace coverage")
        for (t, before, after), row in zip(trace, actual):
            exact(t, row["time"], "D boundary time")
            close(before, row["pre"], "D pre state", 1e-12)
            close(after, row["post"], "D post state", 1e-12)
        close(final, record["metrics"]["final_abs_state"] *
              (-1 if record["trace"][-1]["post"] < 0 else 1), "D final state", 1e-12)
        exact(len(outputs), record["trajectory"]["expected_count"], "D expected regime")
        exact(abs(final) <= 1e-6, True, "D neutral recovery")
        report.append(dict(trajectory=record["trajectory"]["id"], outputs=len(outputs)))
    for control in doc["negative_controls"]:
        if control["id"].startswith("weak-drain"):
            outputs, _, _ = simulate_d(control["result"]["trajectory"], control["result"]["configuration"])
            exact(len(outputs), 3, "D weak-drain negative")
    return dict(trajectories=len(records), inputs=sum(len(r["trajectory"]["inputs"]) for r in records),
                outputs=sum(r["outputs"] for r in report), records=report,
                weak_drain_outputs_per_polarity=3)


def f():
    doc = load("f", "diagnostic.json")
    phase = json.loads(blob(BASE, L45 + "initial-destination_calibrated.json"))
    graph = doc["retained_configuration"]["experiment"]["topology"]
    edges = {(e["source"], e["destination"]) for e in graph["edges"]}
    seen, counts, streams = Counter(), Counter(), defaultdict(set)

    def pointer(reference):
        value = phase
        for segment in reference["json_pointer"].split("/")[1:]:
            value = value[int(segment)] if isinstance(value, list) else value[segment]
        return value

    for row in doc["analysis"]["rows"]:
        source, target = row["source"], row["target"]
        a, b = pointer(source), pointer(target)
        source_value = a["payload"] if row["family"] == "output-drive-proxy" else a["input_value"]
        target_value = b.get("input_value", b.get("payload"))
        exact(source_value, row["source_delta"], "F source delta reference")
        exact(target_value, row["target_delta"], "F target delta reference")
        lag = target["time"] - source["time"]
        exact(lag, row["lag"], "F lag")
        compatible = (source_value != 0 and target_value != 0 and
                      (source_value > 0) == (target_value > 0) and
                      min(abs(source_value), abs(target_value)) /
                      max(abs(source_value), abs(target_value)) >= .5)
        opportunity = compatible and 0 < lag <= 4
        exact(opportunity, row["opportunity"], "F opportunity")
        endpoints = (source["node"], target["node"])
        duplicate = endpoints in edges
        exact(duplicate, row["classification"]["existing_edge_duplicate"], "F static duplicate")
        for before, after in zip(row["causal_chain"], row["causal_chain"][1:]):
            exact(before["time"] < after["time"], True, "F trigger causal direction")
            pointer(before)
            pointer(after)
        if opportunity:
            family = row["family"]
            counts[family + ":opportunities"] += 1
            streams[family].add(row["stream_id"])
            counts[family + ":duplicates"] += duplicate
            if not duplicate:
                exact(endpoints, ("source", "destination"), "F novel endpoints")
                exact(row["classification"]["predicted_hop_reduction"], 1, "F hop reduction")
                exact(row["classification"]["capacity_feasible_novel"], True, "F novel capacity")
                exact(row["target_canonical_emission_association"], False, "F novel emission absent")
                counts["novel"] += 1
            key = (family, row["stream_id"], endpoints)
            exact(row["repeated_endpoint_proposal"], seen[key] > 0, "F repetitions")
            seen[key] += 1
    exact(counts["novel"], 235, "F novel total")
    return dict(rows=len(doc["analysis"]["rows"]), counts=dict(counts),
                streams={k: len(v) for k, v in streams.items()},
                source_local_availability="BLOCKED", useful_novel_emission_associations=0)


def g_sim(params, fixture, noise, sign, cfg):
    queue = [(t, 0, i, sign*(x+params["N"]*n))
             for i, ((t, x), n) in enumerate(zip(fixture, noise))]
    queue.append((fixture[-1][0] + cfg["settle_interval"], 2, len(queue), 0.0))
    heapq.heapify(queue)
    z, prior, pending, serial = 0.0, 0.0, False, len(queue)
    trace, outputs = [], []
    admitted, deposition, peak = 0, 0.0, 0.0
    while queue:
        t, kind, _, x = heapq.heappop(queue)
        z *= math.exp(-(t-prior)*params["L"]/(params["R"]*params["C"]))
        prior = t
        before = z
        qualified, raw = False, z
        if kind == 0:
            band = .25*params["T"] + math.copysign(1.0, x)*params["O"]
            qualified = abs(params["G"]*x) >= band
            if qualified:
                admitted += 1
                deposit = params["G"]*x/params["C"]
                deposition += abs(deposit)
                raw = z + deposit
                z = max(-8.0, min(8.0, raw))
        elif kind == 1:
            pending = False
        peak = max(peak, abs(z))
        pre_output, output = z, None
        if kind != 2 and abs(z) >= params["T"]:
            output = math.tanh(z)
            outputs.append(dict(time=t, value=output, kind=kind))
            z -= math.copysign(min(abs(z), .75*params["T"]), z)
        scheduled = None
        if kind != 2 and abs(z) >= params["T"] and not pending:
            scheduled = t + .1
            serial += 1
            heapq.heappush(queue, (scheduled, 1, serial, 0.0))
            pending = True
        trace.append(dict(time=t, kind=kind, input=x, before=before, qualified=qualified,
                          raw=raw, pre_output=pre_output, output=output, after=z, scheduled=scheduled))
    return dict(trace=trace, outputs=outputs, admitted=admitted, deposition=deposition,
                peak=peak, final=z, neutral=abs(z) <= 1e-6)


def g():
    lane = ROOT.parent / "luna47g"
    cfg = json.loads(blob(REFS["g"], "experiments/luna47g/config.json"))
    fixtures = json.loads(blob(REFS["g"], "experiments/luna47g/fixtures.json"))
    summary = load("g", "summary.json")
    counts, corners, draw_checks, event_checks = Counter(), 0, 0, 0
    rngs = {}
    for filename in ("samples.jsonl.gz", "corners.jsonl.gz"):
        with gzip.open(lane / "artifacts/luna47g" / filename, "rt", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                p = row["parameters"]
                if filename.startswith("samples"):
                    rng = rngs.setdefault((row["band"], row["seed"]), random.Random(row["seed"]))
                    units = [rng.uniform(-1, 1) for _ in range(8)]
                    exact(units, row["parameter_units"], "G RNG parameter draw")
                    generated_noise = {k: [rng.uniform(-1, 1) for _ in v] for k, v in fixtures.items()}
                    exact(generated_noise, row["noise_units"], "G RNG noise draw")
                    b = cfg["bands"][row["band"]]
                    expected = dict(R=1+b*(units[0]+units[1])/2, C=1+b*(units[0]+units[2])/2,
                                    G=1+b*units[3], T=1+b*units[4], L=1+b*units[5],
                                    O=.2*b*units[6], N=.08*(1+b*units[7]))
                    exact(expected, p, "G parameter transforms")
                    draw_checks += 1
                else:
                    corners += 1
                reconstructed = {}
                for group, sign, offset in (("positive", 1, p["O"]), ("negative", -1, p["O"]),
                                            ("offset_mirror", -1, -p["O"])):
                    params = dict(p, O=offset)
                    generated = {}
                    for name, fixture in fixtures.items():
                        actual = row["outcome"]["runs"][group][name]
                        independent = g_sim(params, fixture, row["noise_units"][name], sign, cfg)
                        exact(len(actual["trace"]), len(independent["trace"]), "G trace coverage")
                        for observed, computed in zip(actual["trace"], independent["trace"]):
                            for key in ("kind", "time", "qualified", "scheduled"):
                                exact(observed[key], computed[key], "G trace " + key)
                            for key in ("input", "before", "raw", "pre_output", "after"):
                                close(observed[key], computed[key], "G state " + key, 1e-12)
                            exact(observed["output"] is None, computed["output"] is None, "G output decision")
                            if observed["output"] is not None:
                                close(observed["output"], computed["output"], "G output value", 1e-12)
                            event_checks += 1
                        exact(actual["outputs"], independent["outputs"], "G exact output trace")
                        for key in ("admitted", "deposition", "peak", "final", "neutral"):
                            exact(actual[key], independent[key], "G run " + key)
                        generated[name] = independent
                    if group in ("positive", "negative"):
                        n, s, near, far, moderate, extreme = [
                            generated[k] for k in ("noise", "single", "near", "far", "moderate", "extreme")]
                        gates = dict(
                            noise=n["admitted"] == 0 and not n["outputs"],
                            single=s["admitted"] == 1 and s["peak"] >= .3 and not s["outputs"],
                            accumulation=near["admitted"] == 2 and near["peak"] >= 1.5*s["peak"]
                            and bool(near["outputs"]) and not far["outputs"],
                            compression=moderate["admitted"] == 3 and len(moderate["outputs"]) == 1
                            and abs(sum(o["value"] for o in moderate["outputs"])) <= .9*moderate["deposition"],
                            return_=extreme["admitted"] == 1 and 2 <= len(extreme["outputs"]) <= 16
                            and any(o["kind"] == 1 for o in extreme["outputs"])
                            and abs(sum(o["value"] for o in extreme["outputs"])) <= extreme["deposition"],
                            neutral=all(v["neutral"] for v in generated.values()))
                        gates["return"] = gates.pop("return_")
                        exact(gates, row["outcome"]["signed_gates"][group], "G signed regime gates")
                        reconstructed[group] = gates
                regime_pass = all(v for gates in reconstructed.values() for v in gates.values())
                exact(regime_pass, row["outcome"]["pass_"], "G sample pass")
                if filename.startswith("samples"):
                    counts[row["band"] + ":n"] += 1
                    counts[row["band"] + ":failed"] += not regime_pass
    for band, entry in summary["bands"].items():
        exact(counts[band+":n"], entry["n"], "G sample denominator")
        exact(counts[band+":failed"], entry["failures"], "G failure aggregate")
    return dict(samples=draw_checks, corners=corners, reconstructed_events=event_checks,
                counts=dict(counts), scope="independent assumed stand-in; no composed-lane or hardware yield inference")


def e():
    matrix = load("e", "primitive-matrix.json")
    catalogs = {alias: json.loads(blob(REFS["e"], path))
                for alias, path in matrix["source_catalogs"].items()}
    sources = {alias+":"+s["id"]: s for alias, c in catalogs.items() for s in c["sources"]}
    offers = []
    for component in matrix["components"]:
        availability = component["availability"]
        exact(availability["owner_access"], "BLOCKED", "E owner gate")
        if availability["status"] == "independent_public_stock":
            matches = [sources[r] for r in component["source_refs"] if
                       sources[r]["kind"] == "distributor" and
                       sources[r].get("product", {}).get("mpn") == component["part_number"]]
            exact(len(matches), 1, "E exact offer identity")
            source = matches[0]
            exact(source["product"]["offers"]["inventoryLevel"],
                  availability["stock_count"], "E captured stock")
            offers.append(dict(part=component["part_number"], url=source["url"],
                               stock=availability["stock_count"], price=availability["price_USD"],
                               retrieved_utc=source["retrieved_at_utc"]))
    exact(len(offers), 8, "E discrete offer count")
    return dict(offers=offers, primitive_families=len(matrix["primitives"]),
                owner_access="BLOCKED", independent_FPAA_availability="BLOCKED",
                predeclaration="Criteria first committed together with findings; prior freeze not independently proven")


def main():
    start = time.monotonic()
    report = dict(schema="LUNA47-REVIEW-ORACLE-1", python=sys.version,
                  interpreter=sys.executable, reviewer_baseline=git(ROOT, "rev-parse", "HEAD").decode().strip(),
                  lane_inventory=inventory(), source_integrity=source_integrity(),
                  AB=ab(), C=c(), D=d(), E=e(), F=f(), G=g())
    report.update(check_counts=dict(CHECKS), max_residuals=dict(MAX_RESIDUAL),
                  seconds=time.monotonic()-start, status="PASS")
    (OUT / "independent-verification.json").write_text(
        json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("status", "seconds", "AB", "D", "E", "F", "G")},
                     indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        details = traceback.format_exc()
        with (OUT / "oracle-development-failures.log").open("a", encoding="utf-8") as log:
            log.write(details + "\n")
        raise
