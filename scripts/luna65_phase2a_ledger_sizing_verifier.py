"""Luna-65 Phase 2A S1-B independent read-only evidence verifier.

Gate: L65-PHASE2A-S1B-EXECUTION-CONTRACT-V1 (contract section 6; owner
implementation authorization for D-S1B-2).

Standard library only. It does not import the sizing generator or any TPCN
module, reads no environment variable, and never writes. It re-derives every
expected value from the published schema in its own code and never accepts the
generator's own fit declaration as evidence. Verdicts apply only to the
constructed single width-bound synthetic profile; they are not a universal
compression bound, a nominal fit, a two-run determinism claim, or neuron-runtime
capacity. Same-user tampering is not excluded.

Usage (post-run, interpreter -I -B, run only after the generator has ended):
  python -I -B scripts/luna65_phase2a_ledger_sizing_verifier.py
      --run-root <output dir> --wrapper-dir <run-id>.wrapper
      --repo-root <repository root> --expected-wrapper-sha256 <hex>
"""

import gzip
import hashlib
import json
import sys
import zlib
from pathlib import Path

GENERATOR_REL = "scripts/luna65_phase2a_ledger_sizing.py"
GENERATOR_SHA256_CRLF = "dd2a3df5d51f234b9a90f8c58f69ed84cdd02dc5b9379b1d19a71cb15d719212"
GENERATOR_GIT_BLOB = "088d569c1787e08e3995d10d94aade8517093093"
CONTRACT_REL = "workflow/docs/luna/LUNA_65_PHASE2A_S1B_EXECUTION_CONTRACT.md"
WRAPPER_REL = "scripts/luna65_phase2a_s1b_wrapper.ps1"
WRAPPER_KEYS = frozenset((
    "schema", "run_id", "invocation_count", "wrapper_sha256", "verifier_sha256", "generator_sha256", "exit_utc",
    "generator_blob", "contract_blob", "interpreter_path", "interpreter_sha256", "powershell_version",
    "arguments", "working_directory", "wait_ms", "cleanup_window_ms", "pid", "parent_pid", "start_utc",
    "process_start_time_utc", "exited_within_wait", "elapsed_ms_at_exit", "termination_requested",
    "termination_request_elapsed_ms", "taskkill_exit_code", "cessation_confirmed", "cessation_elapsed_ms",
    "children_before_termination", "children_after_exit", "exit_code", "stdout", "stdout_truncated",
    "stderr", "stderr_truncated", "output_dir_total_bytes", "retained_upper_bound_bytes", "final_state",
    "failure_reason",
))
CONTRACT_GIT_BLOB = "b251e3d09d7e12d1008b34ec3e8c3dd2dbd6e3a2"
INTERPRETER_PATH = "C:\\Users\\Patrick\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
INTERPRETER_SHA256 = "4fb049eeddd221e5470cd33177299dd13f85eba25beef7aced7a0890ad85181f"
PYTHON_VERSION_PREFIX = "3.11.4 "
EVIDENCE_PARENT = "C:\\Users\\Patrick\\AppData\\Local\\TPCN\\evidence\\luna65\\phase2a-sizing"
REPO_ROOT_EXPECTED = "C:\\Users\\Patrick\\Documents\\ActiveCode\\TPCN"

RECORDS = 8196
PROBES = 2049
COUNTERS = ("input", "episode", "lineage", "output_event")
LEDGER_ALLOCATION = 786432
RETAINED_CAP = 1048576
WRAPPER_JSON_MAX = 16384
WALL_LIMIT = 30.0
CPU_LIMIT = 30.0
OUTER_WAIT_MS = 45000
ORIGINAL_VERIFIER_SHA256 = "27d5969035dae923cadc3518d2c1a398ceb3413eab702a4298e71fe2f1eb7d6e"

SCHEMA_VERSION = "luna65-phase2a-probe-v1"
FIXTURE_VERSION = "l65-phase2a-v1"
NEURON_ID = "l65-capacity-node"
EXC_TYPE = "tpcn.excursion_neuron.E1EventBudgetExceeded"
EXC_MESSAGES = {
    "input": "E2 input identity budget exhausted",
    "episode": "E2 episode identity budget exhausted",
    "lineage": "E2 lineage identity budget exhausted",
    "output_event": "E2 output-event identity budget exhausted",
}
LCG_SEED = 0x4C36355F53315A41
LCG_MUL = 6364136223846793005
LCG_INC = 1442695040888963407
MASK64 = (1 << 64) - 1
NUM = "<NUM>"

CLASS_EXIT = {"FITS_WORST": 0, "EXCEEDS_WORST": 2, "GENERATOR_FAILURE": 1}


class Checks:
    def __init__(self):
        self.items = []

    def add(self, number, name, ok, detail=""):
        self.items.append((number, name, bool(ok), str(detail)[:300]))
        return bool(ok)

    def failed(self):
        return [item for item in self.items if not item[2]]


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def git_blob_hex(data):
    normalized = data.replace(b"\r\n", b"\n")
    header = b"blob %d\x00" % len(normalized)
    return hashlib.sha1(header + normalized).hexdigest()


def utc_ms(text):
    # strict "YYYY-MM-DDTHH:MM:SS.fffZ" -> milliseconds since 1970-01-01 (proleptic Gregorian)
    if not isinstance(text, str) or len(text) != 24 or text[4] != "-" or text[7] != "-" or text[10] != "T" or text[13] != ":" or text[16] != ":" or text[19] != "." or text[23] != "Z":
        raise ValueError("bad timestamp")
    digits = text[0:4] + text[5:7] + text[8:10] + text[11:13] + text[14:16] + text[17:19] + text[20:23]
    if not digits.isdigit() or not digits.isascii():
        raise ValueError("bad timestamp")
    year, month, day, hour, minute, second, milli = int(text[0:4]), int(text[5:7]), int(text[8:10]), int(text[11:13]), int(text[14:16]), int(text[17:19]), int(text[20:23])
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    month_days = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if not (1 <= year <= 9999 and 1 <= month <= 12 and 1 <= day <= month_days[month - 1] and hour <= 23 and minute <= 59 and second <= 59):
        raise ValueError("bad timestamp")
    shifted = year - (1 if month <= 2 else 0)
    era = shifted // 400
    year_of_era = shifted - era * 400
    day_of_year = (153 * (month + (-3 if month > 2 else 9)) + 2) // 5 + day - 1
    day_of_era = year_of_era * 365 + year_of_era // 4 - year_of_era // 100 + day_of_year
    days = era * 146097 + day_of_era - 719468
    return (((days * 24 + hour) * 60 + minute) * 60 + second) * 1000 + milli


def canonical(obj):
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return text.encode("ascii") + b"\n"


def _no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def _reject_constant(name):
    raise ValueError("non-finite constant")


def parse_json(raw):
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicates, parse_constant=_reject_constant)


def valid_run_id(name):
    if len(name) != 24 or name[8] != "T" or name[15] != "Z" or name[16] != "-":
        return False
    digits = name[:8] + name[9:15]
    return digits.isdigit() and all(ch in "0123456789abcdef" for ch in name[17:])


def norm_path(text):
    return str(text).replace("/", "\\").rstrip("\\").lower()


class Replay:
    """Independent LCG replay of the D-S1-2 sizing-only 24-character literals."""

    def __init__(self):
        self.state = LCG_SEED & MASK64

    def u32(self):
        self.state = (self.state * LCG_MUL + LCG_INC) & MASK64
        return self.state >> 32

    def literal(self):
        for _ in range(256):
            lead = 1 + self.u32() % 9
            tail = "".join(str(self.u32() % 10) for _ in range(16))
            exponent = 300 + self.u32() % 8
            value = float("-%d.%se-%d" % (lead, tail, exponent))
            if len(repr(value)) == 24:
                return value
        raise ValueError("literal construction exhausted")


def snap(episode, input_count, lineage, output_event):
    return {"episode": episode, "input": input_count, "lineage": lineage, "output_event": output_event}


def cp(mode, phase, kind, count):
    return {
        "mode": mode,
        "phase": phase,
        "local_time": NUM,
        "x": NUM,
        "pending_event_kind": kind,
        "pending_event_time": NUM if kind is not None else None,
        "processed_event_count": count,
    }


def expected_record(counter, probe):
    """Expected record with the three D-S1-2 numeric slots replaced by NUM."""
    rej = probe == PROBES
    prior = probe - 1
    delta = 0 if rej else 1
    zero = snap(0, 0, 0, 0)
    post = None
    if counter == "input":
        before = snap(0, prior, 0, 0)
        after = snap(0, prior + delta, 0, 0)
        coupled = {"episode": 0, "lineage": 0, "output_event": 0}
        prep = zero
        ident = None if rej else "%s:input:%d" % (NEURON_ID, prior)
        state = cp("N", None, None, 0 if rej else 1)
    elif counter in ("episode", "lineage"):
        before = snap(prior, 0, prior, 0)
        after = snap(prior + delta, 0, prior + delta, 0)
        prep = zero
        ident = None if rej else probe
        if counter == "episode":
            coupled = {"input": 0, "lineage": delta, "output_event": 0}
            state = cp("N", None, None, 1) if rej else cp("S_PENDING", None, "S_EMIT", 1)
        else:
            coupled = {"episode": delta, "input": 0, "output_event": 0}
            state = cp("N", None, None, 1) if rej else cp("M_ACTIVE", "ARMED", "M_EMIT", 1)
    else:
        prep = snap(1, 0, 1, 0)
        coupled = {"episode": 0, "input": 0, "lineage": 0}
        if rej:
            before = snap(4, 0, 4, 2048)
            after = snap(4, 0, 4, 2048)
            ident = None
            state = cp("M_ACTIVE", "ARMED", None, 2)
        else:
            if probe <= 1023:
                char, ordinal = 1, probe
            elif probe <= 2046:
                char, ordinal = 2, probe - 1023
            else:
                char, ordinal = 3, probe - 2046
            before = snap(char, 0, char, prior)
            after = snap(char, 0, char, probe)
            ident = "%s:excursion:%d" % (NEURON_ID, probe)
            state = cp("M_ACTIVE", "REFRACTORY", "M_REARM", 2 * ordinal)
            post = cp("M_ACTIVE", "ARMED", "M_EMIT", 2 * ordinal + 1)
    outcome = "capacity_rejected" if rej else "allocated"
    return {
        "schema_version": SCHEMA_VERSION,
        "fixture_version": FIXTURE_VERSION,
        "counter_under_test": counter,
        "probe_index": probe,
        "initial_state_id": "l65-phase2a-%s-fresh-zero-v1" % counter,
        "neuron_id": NEURON_ID,
        "counter_snapshot_before": before,
        "counter_snapshot_after": after,
        "target_counter_delta": delta,
        "coupled_counter_deltas": coupled,
        "preparation_counter_deltas": prep,
        "allocated_identity": ident,
        "exception": {"type": EXC_TYPE, "message": EXC_MESSAGES[counter]} if rej else None,
        "expected_outcome": outcome,
        "observed_outcome": outcome,
        "completion_status": "expected",
        "state_checkpoint": state,
        "post_rearm_checkpoint": post,
    }


def split_numeric(record):
    """Return (record with NUM placeholders, ordered actual numeric values, error)."""
    values = []
    out = dict(record)
    for key in ("state_checkpoint", "post_rearm_checkpoint"):
        item = out.get(key)
        if item is None:
            continue
        if not isinstance(item, dict):
            return None, values, "checkpoint not an object"
        item = dict(item)
        for field in ("x", "local_time", "pending_event_time"):
            if field not in item:
                return None, values, "missing checkpoint field"
            value = item[field]
            if field == "pending_event_time" and value is None:
                continue
            if type(value) is not float:
                return None, values, "checkpoint numeric is not a binary64 literal"
            values.append(value)
            item[field] = NUM
        out[key] = item
    return out, values, None


def expected_numeric_count(expected):
    total = 0
    for key in ("state_checkpoint", "post_rearm_checkpoint"):
        item = expected.get(key)
        if item is None:
            continue
        total += 2 + (1 if item["pending_event_time"] is not None else 0)
    return total


def verify_ledger(raw, checks):
    ok = True
    header_ok = len(raw) > 18 and raw[:2] == b"\x1f\x8b" and raw[2] == 8 and raw[3] == 0 and raw[4:8] == b"\x00\x00\x00\x00"
    ok &= checks.add(8, "gzip header (deflate, no flags, mtime 0, no filename)", header_ok)
    data = None
    try:
        decoder = zlib.decompressobj(31)
        data = decoder.decompress(raw) + decoder.flush()
        stream_ok = decoder.eof and decoder.unused_data == b""
        ok &= checks.add(8, "single complete gzip member, CRC32 and ISIZE verified by zlib", stream_ok)
        try:
            twin = gzip.decompress(raw)
            ok &= checks.add(8, "gzip module decompress agrees", twin == data)
        except Exception as error:
            ok &= checks.add(8, "gzip module decompress agrees", False, error)
    except Exception as error:
        checks.add(8, "single complete gzip member, CRC32 and ISIZE verified by zlib", False, error)
        return None
    lines = data.split(b"\n")
    tail_ok = lines and lines[-1] == b""
    ok &= checks.add(4, "ledger ends with a newline", tail_ok)
    lines = lines[:-1]
    ok &= checks.add(4, "exactly %d records" % RECORDS, len(lines) == RECORDS, len(lines))
    if len(lines) != RECORDS:
        return None
    replay = Replay()
    mismatches = []
    numeric_failures = []
    order = [(counter, probe) for counter in COUNTERS for probe in range(1, PROBES + 1)]
    for (counter, probe), line in zip(order, lines):
        try:
            record = parse_json(line)
            if canonical(record) != line + b"\n":
                mismatches.append((counter, probe, "non-canonical line"))
                continue
        except Exception as error:
            mismatches.append((counter, probe, "unparseable: %s" % error))
            continue
        expected = expected_record(counter, probe)
        normalized, values, error = split_numeric(record) if isinstance(record, dict) else (None, [], "not an object")
        wanted = expected_numeric_count(expected)
        try:
            literals = [replay.literal() for _ in range(wanted)]
        except ValueError as exc:
            numeric_failures.append((counter, probe, str(exc)))
            literals = []
        if error is not None or normalized is None:
            mismatches.append((counter, probe, error))
            continue
        if canonical(normalized) != canonical(expected):
            mismatches.append((counter, probe, "field mismatch"))
        if len(values) != wanted or any(
            repr(a) != repr(b) or len(repr(a)) != 24 or a != a or a in (float("inf"), float("-inf"))
            for a, b in zip(values, literals)
        ):
            numeric_failures.append((counter, probe, "LCG replay mismatch"))
    ok &= checks.add(5, "schema version and fixed fields on every record", not mismatches, mismatches[:3])
    ok &= checks.add(6, "full independent record reconstruction (excluding the three D-S1-2 numeric slots)", not mismatches, mismatches[:3])
    ok &= checks.add(7, "D-S1-2 numeric slots equal frozen LCG replay and are 24-character finite binary64", not numeric_failures, numeric_failures[:3])
    return data


def check_identity(repo_root, checks):
    generator = (repo_root / GENERATOR_REL).read_bytes()
    checks.add(1, "generator SHA-256 equals frozen CRLF worktree value", sha256_hex(generator) == GENERATOR_SHA256_CRLF)
    checks.add(1, "generator Git blob (LF-normalized) equals frozen value", git_blob_hex(generator) == GENERATOR_GIT_BLOB)
    contract = (repo_root / CONTRACT_REL).read_bytes()
    checks.add(1, "S1-B contract Git blob equals frozen value", git_blob_hex(contract) == CONTRACT_GIT_BLOB)
    return sha256_hex(generator), git_blob_hex(generator), git_blob_hex(contract)


def main(argv):
    args = {}
    index = 1
    names = ("--run-root", "--wrapper-dir", "--repo-root", "--expected-wrapper-sha256")
    while index < len(argv):
        if argv[index] not in names or index + 1 >= len(argv) or argv[index] in args:
            sys.stderr.write("usage error\n")
            return 3
        args[argv[index]] = argv[index + 1]
        index += 2
    if len(args) != len(names):
        sys.stderr.write("usage error\n")
        return 3

    checks = Checks()
    run_root = Path(args["--run-root"])
    wrapper_dir = Path(args["--wrapper-dir"])
    repo_root = Path(args["--repo-root"])
    expected_wrapper = args["--expected-wrapper-sha256"].lower()
    own_sha = sha256_hex(Path(__file__).read_bytes())
    classification = None
    report = None
    try:
        report = run_checks(checks, run_root, wrapper_dir, repo_root, expected_wrapper, own_sha)
    except Exception as error:
        checks.add(0, "verifier completed without an internal error", False, "%s: %s" % (type(error).__name__, error))
    for number, name, ok, detail in checks.items:
        sys.stdout.write("CHECK %s %s %s%s\n" % (number, "PASS" if ok else "FAIL", name, (" [%s]" % detail) if detail and not ok else ""))
    failed = checks.failed()
    if failed or report is None:
        sys.stdout.write("VERDICT EVIDENCE_REJECTED\nFINAL GENERATOR_FAILURE (evidence rejected, %d failed check(s))\n" % len(failed))
        return 3
    classification = report
    sys.stdout.write("VERDICT VERIFIED_%s\nFINAL %s\n" % (classification, classification))
    sys.stdout.write("SCOPE constructed single width-bound profile only; no universal bound, nominal fit, two-run determinism or runtime-capacity claim\n")
    if classification != "FITS_WORST":
        sys.stdout.write("LIMIT no ledger retained; record content (checks 4-8) not verifiable\n")
    return 0


def run_checks(checks, run_root, wrapper_dir, repo_root, expected_wrapper, own_sha):
    checks.add(0, "repo root is the frozen path", norm_path(repo_root) == norm_path(REPO_ROOT_EXPECTED))
    run_id = run_root.name
    checks.add(0, "run id format <UTC yyyymmddThhmmssZ>-<7 hex>", valid_run_id(run_id), run_id)
    checks.add(0, "run root and wrapper directory are frozen siblings", norm_path(run_root.parent) == norm_path(EVIDENCE_PARENT) and wrapper_dir.name == run_id + ".wrapper" and norm_path(wrapper_dir.parent) == norm_path(EVIDENCE_PARENT))
    parent_names = sorted(entry.name for entry in run_root.parent.iterdir())
    checks.add(0, "evidence parent holds exactly one attempt", parent_names == sorted([run_id, run_id + ".wrapper"]), parent_names)

    gen_sha, gen_blob, contract_blob = check_identity(repo_root, checks)

    # wrapper evidence
    wrapper_names = sorted(entry.name for entry in wrapper_dir.iterdir())
    checks.add(2, "wrapper directory holds exactly invocation.lock and wrapper.json", wrapper_names == ["invocation.lock", "wrapper.json"], wrapper_names)
    lock_raw = (wrapper_dir / "invocation.lock").read_bytes()
    wrapper_raw = (wrapper_dir / "wrapper.json").read_bytes()
    checks.add(10, "wrapper.json size <= 16,384 bytes", len(wrapper_raw) <= WRAPPER_JSON_MAX, len(wrapper_raw))
    lock = parse_json(lock_raw)
    wrapper = parse_json(wrapper_raw)
    checks.add(2, "invocation lock and wrapper.json are canonical JSON", canonical(lock) == lock_raw and canonical(wrapper) == wrapper_raw)
    wrapper_file_sha = sha256_hex((repo_root / WRAPPER_REL).read_bytes())
    checks.add(2, "wrapper source file SHA-256 equals the expected wrapper hash", wrapper_file_sha == expected_wrapper, wrapper_file_sha)
    checks.add(2, "invocation lock identifies this run and the expected wrapper", isinstance(lock, dict) and lock.get("run_id") == run_id and str(lock.get("wrapper_sha256", "")).lower() == expected_wrapper and lock.get("schema") == "luna65-s1b-lock-v1")
    if not isinstance(wrapper, dict):
        checks.add(2, "wrapper.json is an object", False)
        return None
    script = repo_root / GENERATOR_REL
    expected_args = '-I -B "%s" --output-dir "%s"' % (str(script), str(run_root))
    checks.add(2, "wrapper schema, run id and invocation count 1", wrapper.get("schema") == "luna65-s1b-wrapper-v1" and wrapper.get("run_id") == run_id and wrapper.get("invocation_count") == 1)
    checks.add(2, "wrapper bound the expected wrapper identity", str(wrapper.get("wrapper_sha256", "")).lower() == expected_wrapper)
    checks.add(2, "wrapper bound the frozen original verifier identity", str(wrapper.get("verifier_sha256", "")).lower() == ORIGINAL_VERIFIER_SHA256, "original=%s corrected_running=%s" % (ORIGINAL_VERIFIER_SHA256, own_sha))
    checks.add(2, "wrapper bound the frozen generator, contract and interpreter", str(wrapper.get("generator_sha256", "")).lower() == gen_sha and str(wrapper.get("generator_blob", "")).lower() == gen_blob and str(wrapper.get("contract_blob", "")).lower() == contract_blob and str(wrapper.get("interpreter_sha256", "")).lower() == INTERPRETER_SHA256 and norm_path(wrapper.get("interpreter_path", "")) == norm_path(INTERPRETER_PATH))
    checks.add(2, "wrapper command and working directory equal the frozen command", wrapper.get("arguments") == expected_args and norm_path(wrapper.get("working_directory", "")) == norm_path(REPO_ROOT_EXPECTED) and wrapper.get("wait_ms") == OUTER_WAIT_MS)
    checks.add(2, "wrapper recorded a process id and start time", isinstance(wrapper.get("pid"), int) and isinstance(wrapper.get("start_utc"), str) and wrapper.get("start_utc") != "")
    state = wrapper.get("final_state")
    checks.add(2, "wrapper final state is COMPLETED with exit within the wait", state == "COMPLETED" and wrapper.get("exited_within_wait") is True and wrapper.get("termination_requested") is False, state)
    elapsed = wrapper.get("elapsed_ms_at_exit")
    checks.add(12, "outer elapsed time (wrapper.json stopwatch only) is below 45,000 ms", type(elapsed) is int and 0 <= elapsed < OUTER_WAIT_MS, elapsed)
    try:
        wall_ms = utc_ms(wrapper.get("exit_utc")) - utc_ms(wrapper.get("start_utc"))
        time_ok = type(elapsed) is int and abs(wall_ms - elapsed) <= 2000
    except (TypeError, ValueError, IndexError):
        wall_ms = None
        time_ok = False
    checks.add(12, "wrapper start/exit UTC times agree with the stopwatch elapsed time (+/-2000 ms)", time_ok, wall_ms)
    children = wrapper.get("children_after_exit")
    checks.add(2, "no child processes observed after exit", isinstance(children, dict) and children.get("count") == 0)
    checks.add(2, "wrapper.json has exactly the frozen field set", set(wrapper) == WRAPPER_KEYS, sorted(set(wrapper) ^ WRAPPER_KEYS))
    checks.add(2, "wrapper normal-completion fields and null termination evidence", (
        type(wrapper.get("parent_pid")) is int
        and str(wrapper.get("powershell_version", "")).startswith("5.1.")
        and isinstance(wrapper.get("process_start_time_utc"), str) and wrapper.get("process_start_time_utc") != ""
        and wrapper.get("cleanup_window_ms") == 10000
        and wrapper.get("termination_request_elapsed_ms") is None
        and wrapper.get("taskkill_exit_code") is None
        and wrapper.get("cessation_confirmed") is False
        and wrapper.get("cessation_elapsed_ms") is None
        and wrapper.get("children_before_termination") is None
        and wrapper.get("stderr_truncated") is False
        and wrapper.get("failure_reason") == ""
        and isinstance(children, dict) and set(children) == {"count", "truncated", "entries"}
        and children.get("truncated") is False and children.get("entries") == []
    ))
    exit_code = wrapper.get("exit_code")

    # generator output tree
    names = sorted(entry.name for entry in run_root.iterdir())
    sizing_path = run_root / "sizing.json"
    if "sizing.json" not in names:
        checks.add(3, "sizing.json present", False, names)
        return None
    sizing_raw = sizing_path.read_bytes()
    manifest = parse_json(sizing_raw)
    checks.add(13, "sizing.json is canonical JSON", isinstance(manifest, dict) and canonical(manifest) == sizing_raw)
    if not isinstance(manifest, dict):
        return None
    classification = manifest.get("classification")
    checks.add(14, "classification is a defined value", classification in CLASS_EXIT, classification)
    if classification not in CLASS_EXIT:
        return None
    expected_names = ["sha256.json", "sizing.json"] + (["results.jsonl.gz"] if classification == "FITS_WORST" else [])
    checks.add(3, "exact output file set for the classification", names == sorted(expected_names), names)
    checks.add(2, "wrapper exit code agrees with the classification", exit_code == CLASS_EXIT[classification], exit_code)

    sizes = {}
    for name in names:
        sizes[name] = (run_root / name).stat().st_size
    checks.add(10, "sizing.json <= 16,384 bytes", sizes.get("sizing.json", 0) <= 16384)
    output_total = sum(sizes.values())
    aggregate = output_total + len(lock_raw) + len(wrapper_raw)
    checks.add(11, "output directory <= 1,048,576 bytes", output_total <= RETAINED_CAP, output_total)
    checks.add(11, "aggregate retained evidence <= 1,048,576 bytes", aggregate <= RETAINED_CAP, aggregate)
    checks.add(11, "wrapper-recorded output total and retained bound equal recomputed values", wrapper.get("output_dir_total_bytes") == output_total and wrapper.get("retained_upper_bound_bytes") == output_total + len(lock_raw) + WRAPPER_JSON_MAX, (wrapper.get("output_dir_total_bytes"), wrapper.get("retained_upper_bound_bytes")))
    expected_summary = "%s retained_bytes=%d" % (classification, output_total)
    checks.add(13, "wrapper stdout equals the generator summary line (F3 cross-check)", wrapper.get("stdout") in (expected_summary + "\n", expected_summary + "\r\n") and wrapper.get("stdout_truncated") is False, wrapper.get("stdout"))
    checks.add(13, "wrapper stderr empty", wrapper.get("stderr") == "")

    # manifest constants
    constants_ok = (
        manifest.get("gate") == "L65-PHASE2A-LEDGER-SIZING-S1"
        and manifest.get("schema_version") == SCHEMA_VERSION
        and manifest.get("fixture_version") == FIXTURE_VERSION
        and manifest.get("profile") == "width-bound-v1"
        and manifest.get("lcg") == {"seed": LCG_SEED, "multiplier": LCG_MUL, "increment": LCG_INC, "modulus_bits": 64}
        and manifest.get("gzip") == {"compresslevel": 9, "mtime": 0, "filename": ""}
        and manifest.get("ledger_allocation_bytes") == LEDGER_ALLOCATION
        and manifest.get("retained_cap_bytes") == RETAINED_CAP
        and manifest.get("max_records") == RECORDS
        and str(manifest.get("python_version", "")).startswith(PYTHON_VERSION_PREFIX)
        and manifest.get("zlib_version") == zlib.ZLIB_VERSION
        and manifest.get("zlib_runtime_version") == zlib.ZLIB_RUNTIME_VERSION
    )
    checks.add(13, "manifest constants (gate, schema, profile, LCG, gzip, allocation, cap, interpreter)", constants_ok)
    disclosures = manifest.get("disclosures")
    disclosure_ok = (
        isinstance(disclosures, dict)
        and disclosures.get("no_nominal_fit_claim") is True
        and disclosures.get("no_two_run_determinism_claim") is True
        and "not a proven upper bound" in str(disclosures.get("not_a_proven_upper_bound", ""))
        and "one width-bound profile" in str(disclosures.get("profile_scope", ""))
        and "D-S1-2" in str(disclosures.get("numeric_exception", ""))
    )
    checks.add(14, "D-S1-1 and D-S1-2 disclosures present", disclosure_ok)
    wall = manifest.get("wall_seconds_observed")
    cpu = manifest.get("cpu_seconds_observed")
    checks.add(12, "generator wall and CPU (manifest) <= 30 s", type(wall) is float and type(cpu) is float and 0 <= wall <= WALL_LIMIT and 0 <= cpu <= CPU_LIMIT, (wall, cpu))

    # sha256.json
    sha_raw = (run_root / "sha256.json").read_bytes()
    sha_doc = parse_json(sha_raw)
    listing_ok = isinstance(sha_doc, dict) and set(sha_doc) == {"files"} and canonical(sha_doc) == sha_raw
    listed = {}
    if listing_ok and isinstance(sha_doc["files"], list):
        for entry in sha_doc["files"]:
            if isinstance(entry, dict) and set(entry) == {"path", "sha256", "bytes"}:
                listed[entry["path"]] = entry
            else:
                listing_ok = False
    else:
        listing_ok = False
    want = sorted(name for name in names if name != "sha256.json")
    listing_ok = listing_ok and sorted(listed) == want
    if listing_ok:
        for name in want:
            data = (run_root / name).read_bytes()
            if listed[name]["sha256"] != sha256_hex(data) or listed[name]["bytes"] != len(data):
                listing_ok = False
    checks.add(13, "sha256.json canonical and equal to actual files, hashes and sizes", listing_ok)

    if classification == "FITS_WORST":
        raw = (run_root / "results.jsonl.gz").read_bytes()
        checks.add(9, "complete gzip file size equals manifest compressed_bytes", manifest.get("compressed_bytes") == len(raw), len(raw))
        checks.add(9, "complete gzip file size <= 786,432 (recomputed fit)", len(raw) <= LEDGER_ALLOCATION, len(raw))
        data = verify_ledger(raw, checks)
        checks.add(13, "manifest counts and sizes equal the recomputed ledger", data is not None
                   and manifest.get("records") == RECORDS
                   and manifest.get("records_per_counter") == {name: PROBES for name in COUNTERS}
                   and manifest.get("uncompressed_bytes") == len(data)
                   and manifest.get("decompressed_stream_sha256") == sha256_hex(data)
                   and manifest.get("bytes_per_record_compressed") == len(raw) / RECORDS
                   and manifest.get("bytes_per_record_uncompressed") == len(data) / RECORDS
                   and manifest.get("margin_to_allocation_bytes") == LEDGER_ALLOCATION - len(raw)
                   and manifest.get("gz_written") is True)
        checks.add(14, "recomputed classification FITS_WORST equals the manifest and exit code", len(raw) <= LEDGER_ALLOCATION)
    elif classification == "EXCEEDS_WORST":
        compressed = manifest.get("compressed_bytes")
        checks.add(9, "manifest compressed_bytes exceeds the allocation (not independently verifiable)", type(compressed) is int and compressed > LEDGER_ALLOCATION, compressed)
        checks.add(13, "manifest records, margin and gz_written consistent", manifest.get("records") == RECORDS and manifest.get("gz_written") is False and manifest.get("margin_to_allocation_bytes") == LEDGER_ALLOCATION - compressed)
    else:
        checks.add(14, "failure manifest carries a failure reason and no result fields", isinstance(manifest.get("failure"), str) and "compressed_bytes" not in manifest and "records" not in manifest)
    return classification


if __name__ == "__main__":
    sys.exit(main(sys.argv))
