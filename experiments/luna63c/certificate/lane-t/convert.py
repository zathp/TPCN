"""Luna-63C Stage-A lane T: exact N3 event-time mapping certificate.

Pure-Python exact integer/Fraction arithmetic over W's committed exact rational
enclosures. No schedule data, input time, or ordinal is invented: rows without a
frozen/W-certified time source are BLOCKED.
"""
import hashlib
import json
import re
import struct
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FIX = ROOT / "experiments/luna63c/fixture-freeze/fixtures.json"
FREEZE = ROOT / "experiments/luna63c/fixture-freeze/FIXTURE_FREEZE.md"
WMAT = ROOT / "experiments/luna63c/certificate/lane-w/coverage_matrix.json"
WMAN = ROOT / "experiments/luna63c/certificate/lane-w/manifest.json"

PINS = {
    "source_branch_head": "19caa49d7620062c06ad74d19528e47725f86b37",
    "fixture_publication": "583148e2812b93d519a3dc2821944d08446497b7",
    "w_complete_commit": "17907c67d52cc338249b66f28c3179cd97572c6e",
    "fixtures_json_canonical_sha256": "AF81F3390274B2D565F90CBF12C116C78F45C5DF65D6C28BA88194E9DF2F70FB",
    "fixtures_json_blob": "8c4f9d20dda217d71ef1bcbb4fdefd0e3507ed92",
    "fixture_freeze_md_sha256": "B3BB25D65A8344363DF17F2A6FF3085034FDC431605B6FBA729499D512BE667F",
    "fixture_freeze_md_blob": "fc3d883e72ec3062e07cc453927ee76cba4aa561",
    "n4_requirements_revision": "9cc92adb56e388d8675d538410b319fd8d8841a5",
    "arithmetic_profile_revision": "87179ba2f5da13da7bc70727e72c000de924ed80",
    "design_revision": "3e7d31b9a527e908b21abee3766906084e7cd082",
    "w_matrix_sha256": "0B5AB09AE5E4A29AD951B00563C64F5D445D0665B332154C9D40F93335F90D9F",
}
UNITS_PER_TU_EXP = 1074  # exact active-time unit is 2^-1074 TU
T_CLOCK = F(2) ** 20

EXTERNAL_KINDS = ("STORE", "RECALL", "RESET", "ATTEMPT", "INVALID_TIMESTAMP")


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


def canon(o):
    return json.dumps(o, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def fx(d):
    return F(int(d["numerator"]), int(d["denominator"]))


def iv(d):
    return fx(d["lower_exact"]), fx(d["upper_exact"])


def iv_digest(lo, hi):
    return sha(f"{lo.numerator}/{lo.denominator}:{hi.numerator}/{hi.denominator}".encode())


# ---------------------------------------------------------------- binary64 grid
def ulp_exp(x):
    """Exponent e of the binary64 spacing 2^e at positive normal x (x>=2^-1022)."""
    assert x > 0
    n = x.numerator.bit_length() - x.denominator.bit_length()
    e = n
    while F(2) ** e > x:
        e -= 1
    while F(2) ** (e + 1) <= x:
        e += 1
    assert e >= -1022
    return e - 52


def floor64(x):
    u = F(2) ** ulp_exp(x)
    return (x // u) * u


def ceil64(x):
    f = floor64(x)
    if f == x:
        return f
    return f + F(2) ** ulp_exp(x)  # binade crossing: spacing at f equals next grid step except at 2^k, handled by test


def b64(x):
    f = float(x)
    assert F(f) == x, "not a binary64 value"
    return {"hex": f.hex(), "bits": "0x%016x" % struct.unpack("<Q", struct.pack("<d", f))[0]}


def predecessor_proof(c):
    """Exact predecessor of binary64 value c via bit decrement (not nextafter evidence)."""
    bits = struct.unpack("<Q", struct.pack("<d", float(c)))[0]
    p = struct.unpack("<d", struct.pack("<Q", bits - 1))[0]
    return F(p)


# ---------------------------------------------------------------- W evidence
def load_w():
    m = json.loads(WMAT.read_text(encoding="utf-8"))
    return m, {r["row_id"]: r for r in m["rows"]}


def both(enc):
    """Return the tightest interval consistent across the 256/512-bit enclosures."""
    a, b = iv(enc["256"]), iv(enc["512"])
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    assert lo <= hi
    return lo, hi, {p: iv(enc[p]) for p in ("256", "512")}


def derive_near_clock(ev):
    lo, hi, _ = both(ev["T_life_A4"]["enclosures"])
    a, b = floor64(T_CLOCK - hi), floor64(T_CLOCK - lo)
    if a != b:
        return None
    t = a
    ulp = F(2) ** ulp_exp(t)
    succ = t + ulp
    exp1_lo, exp1_hi = t + lo, t + hi
    c1 = ceil64(exp1_lo), ceil64(exp1_hi)
    out = {
        "t_star": t, "ulp": ulp, "successor": succ, "T_life": (lo, hi),
        "expiry1_ceiling": c1[0] if c1[0] == c1[1] else None,
        "instance2_expiry_lower_bound_exceeds_clock": (succ + lo) > T_CLOCK,
        "instance1_expiry_real_within": (exp1_lo > T_CLOCK - ulp, exp1_hi <= T_CLOCK),
        "t_star_ok": t + hi <= T_CLOCK and (t + ulp) + lo > T_CLOCK,
    }
    return out


def derive_sub_ulp(ev, nc):
    lo, hi, _ = both(ev["quiet_times"]["Q_ABOVE"])
    t, ulp = nc["t_star"], nc["ulp"]
    if not (0 < lo and hi <= ulp):
        return None
    c = ceil64(t + lo), ceil64(t + hi)
    if c[0] != c[1]:
        return None
    ceil = c[0]
    return {"s_q": (lo, hi), "ceiling": ceil, "predecessor": predecessor_proof(ceil),
            "active_units": (hi * 2 ** UNITS_PER_TU_EXP), "expiry_ceiling": nc["expiry1_ceiling"]}


# ---------------------------------------------------------------- inventory
def parse_range(tok):
    m = re.fullmatch(r"(.*?)(\d+)\.\.(.*?)(\d+)", tok)
    if not m:
        return [tok]
    pre, a, _, b = m.groups()
    w = len(a)
    return [f"{pre}{i:0{w}d}" for i in range(int(a), int(b) + 1)]


def kind_of(name):
    n = name
    if n.startswith("SEMANTICALLY_INVALID_STORE"):
        return "EXTERNAL_STORE"
    if n.startswith("SEMANTICALLY_INVALID_RECALL") or n.startswith("VALID_EXTERNAL_RECALL"):
        return "EXTERNAL_RECALL"
    if n.startswith("STORE"):
        return "EXTERNAL_STORE"
    if n.startswith("RECALL"):
        return "EXTERNAL_RECALL"
    if n.startswith("RESET"):
        return "EXTERNAL_RESET"
    if "_CREATED" in n or "_CANCELLED" in n or "_INVALIDATED" in n:
        return "TIMER_LIFECYCLE_REFERENCE"
    if n.startswith("TIMER_CROSSING_POP_STALE"):
        return "STALE_TIMER_POP"
    if n.startswith("TIMER_EXPIRY"):
        return "EXPIRY_TIMER"
    if n.startswith("TIMER_"):
        return "FLOW_TIMER"
    if n in ("OUTPUT_COMMIT", "ROOT_COMMIT"):
        return "OUTPUT_COMMIT"
    if n == "OUTPUT_PROCESS":
        return "OUTPUT_PROCESS"
    if n == "ATTEMPT":
        return "OVERFLOW_ATTEMPT"
    if n.startswith("INVALID_TIMESTAMP"):
        return "INVALID_TIMESTAMP_INPUT"
    if n == "CLOSED_EPISODE_INGRESS":
        return "CLOSED_INGRESS"
    raise ValueError(n)


def short(n):
    return re.sub(r"_(\d+|[A-Z_]*NONFINITE|OUT_OF_DOMAIN|LATE|UNORDERABLE)$", "", n)


def build_inventory(f):
    ev, obs = [], []

    def add(fix, case, inst, eid, kind, src, **kw):
        ev.append(dict(fixture=fix, case=case, instance=inst, event_id=eid, kind=kind, source=src, **kw))

    fixtures = {x["id"]: x for x in f["fixtures"]}
    for fid in ("C0", "C1"):
        for cp in fixtures[fid]["checkpoints"]:
            obs.append({"fixture": fid, "event_id": cp["id"], "status": "OBSERVATION_ONLY",
                        "reason": "state observation; no scheduled event (N3 not applicable)"})
    for cid in fixtures["C2"]["A1_checkpoints"]:
        obs.append({"fixture": "C2", "event_id": cid, "status": "OBSERVATION_ONLY",
                    "reason": "A1 state checkpoint at an exact authored active time; not a scheduled event"})
    for cp in fixtures["C3"]["checkpoints"]:
        for h in (fixtures["C3"]["hold_durations_TU"] if cp["id"].endswith("DURING_HOLD") else [None]):
            obs.append({"fixture": "C3", "event_id": cp["id"] + ("" if h is None else f"@{h}"), "status": "OBSERVATION_ONLY",
                        "reason": "state observation; HOLD duration contributes exactly 0 active units"})
    for i in fixtures["C1"]["inputs"]:
        add("C1", "C1", "C1", i["event_id"], "EXTERNAL_RECALL", "fixtures.C1.inputs")
    c2 = fixtures["C2"]
    for cs in c2["cases"]:
        cid = cs["case_id"]
        if cid == "A0":
            add("C2", cid, "C2.A0", "C2.A0.ZERO", "EXTERNAL_STORE", "fixtures.C2.cases")
            continue
        for p in ("P", "N"):
            inst = f"C2.{cid}.{p}"
            add("C2", cid, inst, f"{inst}.STORE", "EXTERNAL_STORE", "fixtures.C2.event_identity_rule")
            if cs["release"]:
                for suf, k in (("RECALL_ON", "EXTERNAL_RECALL"), ("TIMER_QUIET", "FLOW_TIMER"), ("TIMER_EXPIRY", "EXPIRY_TIMER")):
                    add("C2", cid, inst, f"{inst}.{suf}", k, "fixtures.C2.event_identity_rule(derived suffix)")
    for fid in ("C3", "C4", "C6"):
        for eid in fixtures[fid]["event_ids"]:
            add(fid, fid, fid, eid, "FLOW_TIMER" if fid == "C6" else kind_of(re.sub(r"^C\d\.", "", eid)), f"fixtures.{fid}.event_ids")
    t = fixtures["C3"]["expiry_boundary_instance"]
    add("C3", "C3.EXPIRY_TIE", "C3.EXPIRY_TIE", t["event_id"], "EXTERNAL_RECALL", "fixtures.C3.expiry_boundary_instance")
    add("C3", "C3.EXPIRY_TIE", "C3.EXPIRY_TIE", t["timer_record_id"], "EXPIRY_TIMER", "fixtures.C3.expiry_boundary_instance")
    for inst in fixtures["C5"]["fresh_instances"]:
        for eid in inst["event_ids"]:
            add("C5", "C5." + inst["instance"], "C5." + inst["instance"], eid, c5kind(eid), "fixtures.C5.fresh_instances")
    c7 = fixtures["C7"]
    c7ids = []
    for c in c7["cases"]:
        groups = [(c["id"], c["events"])] if "events" in c and "instances" not in c or c["id"] == "C7.NEAR_CLOCK_LIMIT" else [(f'{c["id"]}.{i["id"]}', i["events"]) for i in c.get("instances", [])]
        for inst, evs in groups:
            toks = [e for t_ in evs for e in parse_range(t_)]
            for pos, n in enumerate(toks, 1):
                eid = f"{c['id']}.{n}" if c["id"] != "C7.TIMESTAMP_INVALID" else f"{inst}.{n}"
                add("C7", c["id"], inst, eid, kind_of(n), "fixtures.C7.cases", local=n, frozen_list_position=pos)
                c7ids.append(eid)
    # fixture-listed near-clock events cover two instances; handled in schedule
    return ev, obs, c7ids


def c5kind(eid):
    s = eid.split(".")[-1]
    return {"STORE": "EXTERNAL_STORE", "RECALL_ON": "EXTERNAL_RECALL", "TIMER_CROSSING": "FLOW_TIMER",
            "OUTPUT_COMMIT": "OUTPUT_COMMIT", "OUTPUT_PROCESS": "OUTPUT_PROCESS", "TIMER_REARM": "FLOW_TIMER",
            "TIMER_QUIET": "FLOW_TIMER", "TIMER_EXPIRY": "EXPIRY_TIMER"}[s]


# ---------------------------------------------------------------- schedule
W_REF = {"EXPIRY": "C4.EXPIRY", "QUIET": "C4.QUIET", "CROSS": "C4.UP_ROOT", "REARM": "C4.REARM_ROOT"}


def rel_source(local, kind):
    n = local
    if kind == "EXTERNAL_STORE" or n.startswith("STORE"):
        return "t_store (external fixture origin; numeric value not frozen)", None
    if "EXPIRY" in n:
        return "t_store + T_life (W-certified duration; absolute origin t_store unfrozen)", "EXPIRY"
    if "QUIET" in n:
        return "t_store + T_q (W-certified duration; absolute origin unfrozen)", "QUIET"
    if "REARM" in n:
        return "t_store + s_rearm(4) (W-certified; absolute origin unfrozen)", "REARM"
    if "CROSSING" in n or n in ("OUTPUT_COMMIT", "ROOT_COMMIT", "OUTPUT_PROCESS"):
        return "t_store + s_up(4) / ceil64 (W-certified; absolute origin unfrozen)", "CROSS"
    if n.startswith("RECALL_ON") or "RECALL" in n:
        return "external input time not frozen (shares STORE time only where the case says so)", None
    return "external input time not frozen", None


def predecessor(toks, i):
    n = toks[i]
    prev = toks[:i]

    def last(pred):
        for q in reversed(prev):
            if pred(q):
                return q
        return None
    ext = last(lambda q: q.split("_")[0] in ("STORE", "RECALL", "RESET", "SEMANTICALLY", "VALID", "ATTEMPT"))
    sfx = re.search(r"_(\d+)$", n)
    s = sfx.group(1) if sfx else None
    if n.startswith("TIMER_EXPIRY_CREATED"):
        return last(lambda q: q.startswith("STORE"))
    if "_CREATED" in n:
        if n.startswith("TIMER_CROSSING"):
            return last(lambda q: q.startswith("RECALL_ON"))
        if n.startswith("TIMER_REARM"):
            return last(lambda q: q.startswith("TIMER_CROSSING_") and "CREATED" not in q and "CANCELLED" not in q) or last(lambda q: q == "ROOT_COMMIT")
        if n.startswith("TIMER_QUIET"):
            return last(lambda q: q.startswith("TIMER_REARM_") and "_" in q and "CREATED" not in q and "CANCELLED" not in q) or last(lambda q: q.startswith("RECALL_ON"))
    if "INVALIDATED" in n:
        return last(lambda q: q.startswith(("TIMER_QUIET_", "RESET", "ATTEMPT")) and "CREATED" not in q)
    if "CANCELLED" in n:
        return ext
    if n.startswith("TIMER_CROSSING_POP_STALE"):
        return last(lambda q: "CANCELLED" in q)
    if re.fullmatch(r"TIMER_(CROSSING|REARM|QUIET)_\d+", n):
        return last(lambda q: q == n.replace("TIMER_", "TIMER_", 1).replace("_" + s, "_CREATED_" + s))
    if n in ("OUTPUT_COMMIT", "ROOT_COMMIT"):
        return last(lambda q: re.fullmatch(r"TIMER_CROSSING_\d+", q) is not None)
    if n == "OUTPUT_PROCESS":
        return last(lambda q: q in ("OUTPUT_COMMIT", "ROOT_COMMIT"))
    if n.startswith("RESET") and "OUTPUT_PROCESS" in prev:
        return "OUTPUT_PROCESS"
    if n == "TIMER_EXPIRY_1" or re.fullmatch(r"TIMER_EXPIRY_\d+", n):
        return last(lambda q: q.startswith("TIMER_EXPIRY_CREATED"))
    if n.startswith("VALID_EXTERNAL_RECALL") or n.startswith("SEMANTICALLY_INVALID_RECALL"):
        return "TIMER_EXPIRY_1"
    if n.startswith("INVALID_TIMESTAMP"):
        return last(lambda q: q.startswith("STORE"))
    if n == "CLOSED_EPISODE_INGRESS":
        return "ATTEMPT"
    if n.startswith(("STORE", "TIMER_CROSSING_POP")):
        return None
    return ext


NON_C7_PRED = {"RECALL_ON": "STORE", "TIMER_CROSSING": "RECALL_ON", "OUTPUT_COMMIT": "TIMER_CROSSING",
               "OUTPUT_PROCESS": "OUTPUT_COMMIT", "TIMER_REARM": "TIMER_CROSSING", "TIMER_EXPIRY": "STORE"}


def non_c7_pred(e):
    eid, fix = e["event_id"], e["fixture"]
    base, _, loc = eid.rpartition(".")
    if fix == "C1":
        return ["C1.RECALL_ON"] if loc == "RECALL_OFF" else []
    if fix == "C6":
        return {"ROOT_UP": [], "ROOT_REARM": ["C6.ROOT_UP"], "QUIET": ["C6.ROOT_REARM"]}[loc]
    if eid == "C3.EXPIRY_TIE.RECALL":
        return ["C3.EXPIRY_TIE.TIMER_EXPIRY"]
    if eid == "C3.EXPIRY_TIE.TIMER_EXPIRY":
        return ["UNIDENTIFIED_TIE_INSTANCE_STORE(no frozen event ID)"]
    if fix == "C2":
        if loc in ("STORE", "ZERO"):
            return []
        if loc == "TIMER_QUIET":
            return [base + ".RECALL_ON"]
        return [base + "." + NON_C7_PRED[loc]] if loc != "TIMER_EXPIRY" else [base + ".STORE"]
    if loc == "STORE":
        return []
    if loc == "TIMER_QUIET":
        return [base + (".TIMER_REARM" if fix in ("C4", "C5") else ".RECALL_ON")]
    return [base + "." + NON_C7_PRED[loc]]


def precedence(local, kind):
    p = []
    if kind in ("EXTERNAL_STORE", "EXTERNAL_RECALL", "EXTERNAL_RESET"):
        p.append("external records at one represented time are ordered by destination delivery ordinal; internal boundaries precede them")
    if "EXPIRY" in local and kind == "EXPIRY_TIMER":
        p.append("expiry preempts every uncommitted boundary and same-time external application")
    if "REARM" in local and kind == "FLOW_TIMER":
        p.append("rearm strictly precedes quiet; coalesced ceilings keep rearm before quiet")
    if kind == "OUTPUT_COMMIT":
        p.append("commit at mathematical root, persisted to processing at represented t_emit")
    if kind == "OUTPUT_PROCESS":
        p.append("processing precedes same-time reset/cleanup")
    if kind == "INVALID_TIMESTAMP_INPUT":
        p.append("consumes audit identity/count only; installs no order key; no settlement")
    if kind in ("OVERFLOW_ATTEMPT", "CLOSED_INGRESS"):
        p.append("no timestamp or ordinal allocated by rule")
    if not p:
        p.append("per-record lifecycle reference; allocates no destination ordinal")
    return p


def build_schedule(f, w_rows, wm):
    inv, obs, c7ids = build_inventory(f)
    ev = wm["evidence"]
    nc = derive_near_clock(ev)
    su = derive_sub_ulp(ev, nc) if nc else None
    toks_by_inst = {}
    for e in inv:
        if e["fixture"] == "C7":
            toks_by_inst.setdefault(e["instance"], []).append(e["local"])
    certified = {}
    if nc and nc["t_star_ok"] and nc["expiry1_ceiling"] == T_CLOCK and nc["instance2_expiry_lower_bound_exceeds_clock"]:
        h = b64(nc["t_star"])
        hs = b64(nc["successor"])
        hc = b64(T_CLOCK)
        base = "C7.NEAR_CLOCK_LIMIT."
        w_nc = ["C7.NEAR_CLOCK_LIMIT.LIFETIME_SOURCE", "C4.EXPIRY"]
        certified[base + "STORE_LAST_IN_DOMAIN_ORIGIN_1"] = dict(
            instance="NEAR_CLOCK.instance_1", ordinal=1, preds=[], time=nc["t_star"], b=h,
            note="largest binary64 t with exact t+T_life<=2^20 (floor uniqueness over W T_life interval); accepted STORE", w=w_nc)
        certified[base + "TIMER_EXPIRY_CREATED_FOR_INSTANCE_1"] = dict(
            instance="NEAR_CLOCK.instance_1", ordinal=2, preds=[base + "STORE_LAST_IN_DOMAIN_ORIGIN_1"], time=nc["t_star"], b=h,
            due=T_CLOCK, due_b=hc, note="creation at t*; due ceiling64(t*+T_life)=2^20 inclusive, in domain, strictly after cause", w=w_nc)
        certified[base + "STORE_NEXT_ORIGIN_1"] = dict(
            instance="NEAR_CLOCK.instance_2", ordinal=1, preds=[], time=nc["successor"], b=hs,
            note="immediate successor origin t*+2^-33; exact t+T_life>2^20 so STORE is rejected out-of-domain before episode/timer", w=w_nc)
        if su:
            sb = "C7.POSITIVE_SUB_ULP."
            ts = nc["t_star"]
            tq = ts + nc["ulp"]
            w_su = ["C7.POSITIVE_SUB_ULP.Q_ABOVE_CLASS", "C7.POSITIVE_SUB_ULP.QUIET_BEFORE_EXPIRY", "C7.NEAR_CLOCK_LIMIT.LIFETIME_SOURCE"]
            seq = [("STORE_UPPER_Q_NEIGHBOR_1", ts, 1, [], "STORE at near-limit origin t*"),
                   ("TIMER_EXPIRY_CREATED_1", ts, 2, ["STORE_UPPER_Q_NEIGHBOR_1"], "expiry created at t*, due 2^20"),
                   ("RECALL_ON_1", ts, 3, ["STORE_UPPER_Q_NEIGHBOR_1"], "same binary64 time as STORE; ordered after it by external delivery"),
                   ("TIMER_QUIET_CREATED_1", ts, 4, ["RECALL_ON_1"], "created at processed RECALL cause t*"),
                   ("TIMER_QUIET_1", tq, 5, ["TIMER_QUIET_CREATED_1"], "due ceiling64(t*+s_q)=t*+2^-33; 0<s_q<=2^-33 certified; strictly future"),
                   ("TIMER_EXPIRY_INVALIDATED_AT_QUIET_1", tq, 6, ["TIMER_QUIET_1"], "quiet terminal at t*+2^-33 < 2^20 invalidates existing expiry record")]
            for n, tt, o, pr, note in seq:
                certified[sb + n] = dict(instance="POSITIVE_SUB_ULP", ordinal=o, preds=[sb + p for p in pr], time=tt, b=b64(tt), note=note, w=w_su,
                                         sub=n in ("TIMER_QUIET_1", "TIMER_EXPIRY_INVALIDATED_AT_QUIET_1"))
                if n == "TIMER_EXPIRY_CREATED_1":
                    certified[sb + n].update(due=T_CLOCK, due_b=hc)
    rows = []
    for e in inv:
        row = {k: e[k] for k in ("fixture", "case", "instance", "event_id", "kind")}
        row["frozen_source"] = e["source"]
        if e["event_id"] in certified:
            c = certified[e["event_id"]]
            row.update(status="CERTIFIED", blocked_reasons=[], time_source_class="FROZEN_DERIVED_FROM_W_INTERVAL",
                       time_source=c["note"], w_evidence=c["w"],
                       instance_component=c["instance"], causal_predecessors=c["preds"],
                       precedence_dependencies=precedence(e["local"], e["kind"]),
                       domain_rationale="0<=t<=2^20 inclusive; finite binary64; strict-future where a timer",
                       exact_time={"num": c["time"].numerator, "den": c["time"].denominator}, binary64=c["b"],
                       final_ordinal=c["ordinal"],
                       ordinal_scope="1-based position in the proven per-component causal/precedence order; not a destination delivery counter")
            if "due" in c:
                row["due_time"] = {"num": c["due"].numerator, "den": c["due"].denominator}
                row["due_binary64"] = c["due_b"]
            if c.get("sub"):
                row["ceiling_proof"] = {
                    "real_interval_s_q_exact_lower": su["s_q"][0].numerator, "real_interval_s_q_exact_lower_den": su["s_q"][0].denominator,
                    "real_interval_s_q_exact_upper": su["s_q"][1].numerator, "real_interval_s_q_exact_upper_den": su["s_q"][1].denominator,
                    "ceiling": b64(su["ceiling"]), "predecessor_binary64_exact": b64(su["predecessor"]),
                    "predecessor_is_cause_time": su["predecessor"] == nc["t_star"],
                    "endpoint_equal_ceilings": True,
                    "accumulated_active_units_upper_bound_exact": str(su["active_units"].numerator // su["active_units"].denominator),
                    "unit": "2^-1074 TU", "exact_release_interval_units_2pow1041": str(2 ** 1041),
                    "note": "nextafter used only as a cross-check; proof is exact grid arithmetic"}
            rows.append(row)
            continue
        rows.append(blocked_row(row, e, toks_by_inst))
    return inv, obs, rows, nc, su


def blocked_row(row, e, toks_by_inst):
    fix, kind = e["fixture"], e["kind"]
    local = e.get("local") or e["event_id"].split(".")[-1]
    src, wk = rel_source(local, kind)
    reasons = []
    case = e["case"]
    if kind == "OVERFLOW_ATTEMPT" or kind == "CLOSED_INGRESS":
        src = "no timestamp by frozen rule"
        reasons = ["NO_TIMESTAMP_BY_RULE_PRECEDENCE_DEPENDS_ON_BLOCKED_INSTANCE_SCHEDULE"]
        cls = "NO_TIMESTAMP_BY_RULE"
    elif kind == "INVALID_TIMESTAMP_INPUT" or case == "C7.TIMESTAMP_INVALID":
        reasons = ["INVALID_TIMESTAMP_ENVELOPE_NOT_FROZEN", "PRECEDING_STORE_TIME_t_store_UNSPECIFIED"]
        cls = "EXTERNAL_UNSPECIFIED"
    elif case == "C7.OUTPUT_EXPIRY_COALESCENCE":
        reasons = ["EXTERNAL_INPUT_TIME_UNSPECIFIED", "COALESCENCE_WITNESS_t_store_AND_t_late_NOT_FROZEN"]
        cls = "EXTERNAL_UNSPECIFIED"
    elif "EXPIRY_COALESCENCE" in case or case == "C3.EXPIRY_TIE":
        reasons = ["EXTERNAL_INPUT_TIME_UNSPECIFIED", "EXPIRY_COALESCENCE_PACKET_CHOICE_DEPENDS_ON_UNFROZEN_t_store"]
        cls = "EXTERNAL_UNSPECIFIED"
    elif kind == "EXTERNAL_STORE" or src.startswith("t_store"):
        reasons = ["EXTERNAL_INPUT_TIME_UNSPECIFIED" if kind == "EXTERNAL_STORE" else "ABSOLUTE_ORIGIN_t_store_UNFROZEN"]
        cls = "EXTERNAL_UNSPECIFIED" if kind == "EXTERNAL_STORE" else "W_CERTIFIED_OFFSET_UNFROZEN_ORIGIN"
    elif kind in ("EXTERNAL_RECALL", "EXTERNAL_RESET"):
        reasons = ["EXTERNAL_INPUT_TIME_UNSPECIFIED"]
        cls = "EXTERNAL_UNSPECIFIED"
    else:
        reasons = ["ABSOLUTE_ORIGIN_t_store_UNFROZEN"]
        cls = "W_CERTIFIED_OFFSET_UNFROZEN_ORIGIN" if wk else "EXTERNAL_UNSPECIFIED"
    if fix == "C6":
        reasons = ["RELEASE_ORIGIN_NOT_FROZEN_NUMERICALLY"]
        cls = "W_CERTIFIED_OFFSET_UNFROZEN_ORIGIN"
    if fix == "C7" and case == "C7.RESET_BEFORE_COMMIT" and local.startswith("RESET"):
        reasons = ["EXTERNAL_INPUT_TIME_UNSPECIFIED", "RESET_TIME_ONLY_CONSTRAINED_TO_AN_OPEN_INTERVAL"]
    if fix == "C7" and case == "C7.ALTERNATING_RECALL" and local.startswith("RECALL_O"):
        reasons = ["EXTERNAL_INPUT_TIME_UNSPECIFIED", "s_pause_AND_RESUME_TIME_ONLY_CONSTRAINED_TO_INTERVALS"]
    if fix == "C7":
        toks = toks_by_inst[e["instance"]]
        pr = predecessor(toks, e["frozen_list_position"] - 1)
        pre = e["instance"] if case == "C7.TIMESTAMP_INVALID" else e["event_id"].rsplit(".", 1)[0]
        pr = [f"{pre}.{pr}"] if pr else []
    else:
        pr = non_c7_pred(e)
    row.update(status="BLOCKED", blocked_reasons=reasons, time_source_class=cls, time_source=src,
               w_evidence=([W_REF[wk]] if wk else []), instance_component=e["instance"],
               causal_predecessors=pr,
               precedence_dependencies=precedence(local, kind),
               domain_rationale="cannot be certified: finite clock-domain and strict-future checks need the absolute time",
               exact_time=None, binary64=None, final_ordinal=None, ordinal_scope=None)
    return row


# ---------------------------------------------------------------- driver
def git(*a):
    return subprocess.run(["git", "-C", str(ROOT)] + list(a), capture_output=True, text=True, check=True).stdout.strip()


def verify_pins():
    raw = FIX.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n")
    assert sha(canonical) == PINS["fixtures_json_canonical_sha256"]
    assert sha(FREEZE.read_bytes()) == PINS["fixture_freeze_md_sha256"]
    assert sha(WMAT.read_bytes().replace(b"\r\n", b"\n"))  # present
    wm = json.loads(WMAN.read_text(encoding="utf-8"))
    return wm


def generate():
    verify_pins()
    f = json.loads(FIX.read_bytes().replace(b"\r\n", b"\n"))
    wm, w_rows = load_w()
    inv, obs, rows, nc, su = build_schedule(f, w_rows, wm)
    n_c7 = sum(1 for r in rows if r["fixture"] == "C7")
    summary = {"events": len(rows), "certified": sum(r["status"] == "CERTIFIED" for r in rows),
               "blocked": sum(r["status"] == "BLOCKED" for r in rows), "observation_rows": len(obs),
               "c7_identities": n_c7, "c7_certified": sum(r["status"] == "CERTIFIED" for r in rows if r["fixture"] == "C7"),
               "c7_blocked": sum(r["status"] == "BLOCKED" for r in rows if r["fixture"] == "C7")}
    verdict = "T COMPLETE — N3 CLOSED FOR FROZEN EVENT INVENTORY" if summary["blocked"] == 0 else "T BLOCKED — N3 NOT CLOSED"
    inventory = {"format": "luna63c-lane-t-inventory", "pins": PINS, "counts": summary,
                 "events": [{k: v for k, v in e.items() if k != "local"} for e in inv], "observation_rows": obs}
    schedule = {"format": "luna63c-lane-t-schedule", "verdict": verdict, "pins": PINS, "counts": summary,
                "model_constants": {"T_clock_TU": "2^20 inclusive", "active_unit": "2^-1074 TU",
                                    "authored_exact_offsets_units": {"1_TU": str(2 ** 1074), "2_TU": str(2 ** 1075)},
                                    "hold_active_units": "0 for HOLD durations 0,1,2 TU"},
                "rows": rows, "observation_rows": obs}
    return inventory, schedule


FILES = ("inventory.json", "schedule.json")


def write():
    inventory, schedule = generate()
    (HERE / "inventory.json").write_bytes(canon(inventory).encode())
    (HERE / "schedule.json").write_bytes(canon(schedule).encode())
    man = {"format": "luna63c-lane-t-manifest", "pins": PINS, "verdict": schedule["verdict"], "counts": schedule["counts"],
           "files": {n: sha((HERE / n).read_bytes()) for n in FILES + ("convert.py", "test_lane_t.py")},
           "environment": {"python": sys.version.split()[0], "arithmetic": "pure Python exact int/Fraction; no gmpy2/MPFR in T",
                           "w_input": "committed lane-w/coverage_matrix.json exact rational enclosures"}}
    (HERE / "manifest.json").write_bytes(canon(man).encode())
    return man


def check():
    inventory, schedule = generate()
    for n, o in (("inventory.json", inventory), ("schedule.json", schedule)):
        assert (HERE / n).read_bytes() == canon(o).encode(), n + " differs"
    man = json.loads((HERE / "manifest.json").read_text())
    for n, h in man["files"].items():
        assert sha((HERE / n).read_bytes()) == h, n
    return schedule["counts"]


if __name__ == "__main__":
    if "--check" in sys.argv:
        print(check())
    else:
        print(write())