"""Luna-65 Phase 2A synthetic ledger-sizing generator (L65-PHASE2A-LEDGER-SIZING-S1).

Synthetic-only. Produces one deterministic width-bound profile of at most
8,196 schema-shaped records, generated exactly once, and measures its
gzip-compressed size. No TPCN import, no neuron, no live E2 identity
counters, no Spiral data, no training or scoring.

Owner decisions bound to this source (recorded in the S1-A implementation
handoff workflow/handoffs/luna-0-luna65-s1a-implementation-20261012.md and the
authoritative workflow as directly supplied owner conversation decisions;
no attachment bytes are claimed verified):
  O11 amendment  time.monotonic() for wall monitoring and time.process_time()
          for CPU accounting are permitted; the 30 s CPU requirement stays.
  D-S1-1  One width-bound profile, generated once, <= 8,196 records.
          Classifications: FITS_WORST / EXCEEDS_WORST / GENERATOR_FAILURE.
          No nominal-fit claim and no two-run determinism claim. The
          constructed profile is a sizing sample, not a proven upper bound
          on all possible compressed ledgers.
  D-S1-2  Option 1. Checkpoint `x`, local-time and pending-event-time values
          are replaced by deterministic maximum-length (24-character repr)
          finite binary64 literals. This is a sizing-only exception to the
          exact numeric values of the capacity scenarios; the synthetic
          values do NOT reproduce the scenario recurrence behavior. Identity
          strings, ordinals, field mappings and schema constraints stay exact.

Usage (not executed under S1-A):
  python -B scripts/luna65_phase2a_ledger_sizing.py --output-dir <new-dir>
"""

import gzip
import hashlib
import json
import sys
import time
import zlib
from pathlib import Path

SCHEMA_VERSION = "luna65-phase2a-probe-v1"
FIXTURE_VERSION = "l65-phase2a-v1"
PROFILE = "width-bound-v1"
NEURON_ID = "l65-capacity-node"
EXCEPTION_TYPE = "tpcn.excursion_neuron.E1EventBudgetExceeded"

COUNTERS = ("input", "episode", "lineage", "output_event")
PROBES_PER_COUNTER = 2049
LAST_ALLOCATION_PROBE = 2048
MAX_RECORDS = 8196

LEDGER_ALLOCATION_BYTES = 786432
RETAINED_CAP_BYTES = 1048576
SIZING_JSON_MAX_BYTES = 16384
WALL_LIMIT_SECONDS = 30.0
CPU_LIMIT_SECONDS = 30.0
GUARD_INTERVAL = 256

LCG_SEED = 0x4C36355F53315A41
LCG_MULTIPLIER = 6364136223846793005
LCG_INCREMENT = 1442695040888963407
LCG_MASK = (1 << 64) - 1
STRESS_REPR_LENGTH = 24
STRESS_MAX_ATTEMPTS = 256

REJECTION_MESSAGES = {
    "input": "E2 input identity budget exhausted",
    "episode": "E2 episode identity budget exhausted",
    "lineage": "E2 lineage identity budget exhausted",
    "output_event": "E2 output-event identity budget exhausted",
}

DISCLOSURES = {
    "profile_scope": "one width-bound profile generated once; not a nominal profile",
    "not_a_proven_upper_bound": "the constructed sample is not a proven upper bound on all possible compressed ledgers",
    "no_nominal_fit_claim": True,
    "no_two_run_determinism_claim": True,
    "numeric_exception": "checkpoint x, local_time and pending_event_time are deterministic maximum-length binary64 literals (D-S1-2 Option 1); they do not reproduce the capacity-scenario recurrence behavior",
    "exact_fields": "identity strings, ordinals, counter snapshots, deltas, outcomes, exception objects and processed_event_count are exact",
    "checkpoint_keys": "mode, phase, local_time, x, pending_event_kind, pending_event_time, processed_event_count (generator-chosen key names; the published schema does not fix them)",
    "preparation_deltas": "output_event probes use character-admission deltas episode 1, lineage 1, input 0, output_event 0",
    "fit_rule": "classification uses the length of the complete closed gzip stream (deflate end block and 8-byte trailer included) against the 786,432-byte ledger allocation",
    "memory": "not measured or enforced; up to 786,432 compressed bytes are buffered in process",
}


class GeneratorFailure(Exception):
    pass


class Lcg:
    def __init__(self, seed):
        self.state = seed & LCG_MASK

    def next_u32(self):
        self.state = (self.state * LCG_MULTIPLIER + LCG_INCREMENT) & LCG_MASK
        return self.state >> 32


class StressFloats:
    """Deterministic finite binary64 values whose repr has the maximum length."""

    def __init__(self, seed):
        self.lcg = Lcg(seed)

    def next(self):
        for _ in range(STRESS_MAX_ATTEMPTS):
            lead = 1 + self.lcg.next_u32() % 9
            digits = "".join(str(self.lcg.next_u32() % 10) for _ in range(16))
            exponent = 300 + self.lcg.next_u32() % 8
            value = float("-%d.%se-%d" % (lead, digits, exponent))
            if len(repr(value)) == STRESS_REPR_LENGTH:
                return value
        raise GeneratorFailure("stress literal construction exhausted")


class CountingSink:
    """Counts every compressed byte; buffers them only while they can still fit."""

    def __init__(self, buffer_limit):
        self.buffer_limit = buffer_limit
        self.buffer = bytearray()
        self.total = 0
        self.overflowed = False

    def write(self, data):
        self.total += len(data)
        if not self.overflowed:
            if len(self.buffer) + len(data) > self.buffer_limit:
                self.overflowed = True
                self.buffer = bytearray()
            else:
                self.buffer += data
        return len(data)

    def flush(self):
        pass


def snapshot(episode, input_count, lineage, output_event):
    return {
        "episode": episode,
        "input": input_count,
        "lineage": lineage,
        "output_event": output_event,
    }


def checkpoint(stress, mode, phase, pending_kind, count):
    x_value = stress.next()
    local_time = stress.next()
    pending_time = stress.next() if pending_kind is not None else None
    return {
        "mode": mode,
        "phase": phase,
        "local_time": local_time,
        "x": x_value,
        "pending_event_kind": pending_kind,
        "pending_event_time": pending_time,
        "processed_event_count": count,
    }


def output_character(probe):
    """Map an output_event probe 1..2048 to (character, ordinal within character)."""
    if probe <= 1023:
        return 1, probe
    if probe <= 2046:
        return 2, probe - 1023
    return 3, probe - 2046


def build_record(stress, counter, probe):
    rejected = probe == PROBES_PER_COUNTER
    target_delta = 0 if rejected else 1
    prior = probe - 1
    zero_prep = snapshot(0, 0, 0, 0)
    post_rearm = None
    identity = None

    if counter == "input":
        before = snapshot(0, prior, 0, 0)
        after = snapshot(0, prior + target_delta, 0, 0)
        coupled = {"episode": 0, "lineage": 0, "output_event": 0}
        prep = zero_prep
        if not rejected:
            identity = "%s:input:%d" % (NEURON_ID, prior)
        state = checkpoint(stress, "N", None, None, 0 if rejected else 1)
    elif counter == "episode":
        before = snapshot(prior, 0, prior, 0)
        after = snapshot(prior + target_delta, 0, prior + target_delta, 0)
        coupled = {"input": 0, "lineage": target_delta, "output_event": 0}
        prep = zero_prep
        if not rejected:
            identity = probe
        if rejected:
            state = checkpoint(stress, "N", None, None, 1)
        else:
            state = checkpoint(stress, "S_PENDING", None, "S_EMIT", 1)
    elif counter == "lineage":
        before = snapshot(prior, 0, prior, 0)
        after = snapshot(prior + target_delta, 0, prior + target_delta, 0)
        coupled = {"episode": target_delta, "input": 0, "output_event": 0}
        prep = zero_prep
        if not rejected:
            identity = probe
        if rejected:
            state = checkpoint(stress, "N", None, None, 1)
        else:
            state = checkpoint(stress, "M_ACTIVE", "ARMED", "M_EMIT", 1)
    elif counter == "output_event":
        prep = snapshot(1, 0, 1, 0)
        coupled = {"episode": 0, "input": 0, "lineage": 0}
        if rejected:
            before = snapshot(4, 0, 4, 2048)
            after = snapshot(4, 0, 4, 2048)
            state = checkpoint(stress, "M_ACTIVE", "ARMED", None, 2)
        else:
            character, ordinal = output_character(probe)
            before = snapshot(character, 0, character, prior)
            after = snapshot(character, 0, character, probe)
            identity = "%s:excursion:%d" % (NEURON_ID, probe)
            state = checkpoint(stress, "M_ACTIVE", "REFRACTORY", "M_REARM", 2 * ordinal)
            post_rearm = checkpoint(stress, "M_ACTIVE", "ARMED", "M_EMIT", 2 * ordinal + 1)
    else:
        raise GeneratorFailure("unknown counter")

    exception = None
    if rejected:
        exception = {"type": EXCEPTION_TYPE, "message": REJECTION_MESSAGES[counter]}

    return {
        "schema_version": SCHEMA_VERSION,
        "fixture_version": FIXTURE_VERSION,
        "counter_under_test": counter,
        "probe_index": probe,
        "initial_state_id": "l65-phase2a-%s-fresh-zero-v1" % counter,
        "neuron_id": NEURON_ID,
        "counter_snapshot_before": before,
        "counter_snapshot_after": after,
        "target_counter_delta": target_delta,
        "coupled_counter_deltas": coupled,
        "preparation_counter_deltas": prep,
        "allocated_identity": identity,
        "exception": exception,
        "expected_outcome": "capacity_rejected" if rejected else "allocated",
        "observed_outcome": "capacity_rejected" if rejected else "allocated",
        "completion_status": "expected",
        "state_checkpoint": state,
        "post_rearm_checkpoint": post_rearm,
    }


def canonical_line(record):
    text = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return text.encode("ascii") + b"\n"


def canonical_bytes(obj):
    return canonical_line(obj)


def generate(start_wall, start_cpu):
    stress = StressFloats(LCG_SEED)
    sink = CountingSink(LEDGER_ALLOCATION_BYTES)
    gz = gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=sink, mtime=0)
    digest = hashlib.sha256()
    uncompressed = 0
    count = 0
    per_counter = {name: 0 for name in COUNTERS}
    for counter in COUNTERS:
        for probe in range(1, PROBES_PER_COUNTER + 1):
            if count >= MAX_RECORDS:
                raise GeneratorFailure("record ceiling exceeded")
            line = canonical_line(build_record(stress, counter, probe))
            digest.update(line)
            uncompressed += len(line)
            gz.write(line)
            count += 1
            per_counter[counter] += 1
            if count % GUARD_INTERVAL == 0:
                if time.monotonic() - start_wall > WALL_LIMIT_SECONDS:
                    raise GeneratorFailure("wall guard exceeded")
                if time.process_time() - start_cpu > CPU_LIMIT_SECONDS:
                    raise GeneratorFailure("cpu guard exceeded")
    gz.close()
    if count != MAX_RECORDS:
        raise GeneratorFailure("record count mismatch")
    for name in COUNTERS:
        if per_counter[name] != PROBES_PER_COUNTER:
            raise GeneratorFailure("per-counter count mismatch")
    return {
        "records": count,
        "per_counter": per_counter,
        "uncompressed_bytes": uncompressed,
        "compressed_bytes": sink.total,
        "stream_sha256": digest.hexdigest(),
        "gz_bytes": None if sink.overflowed else bytes(sink.buffer),
    }


def manifest_base():
    return {
        "gate": "L65-PHASE2A-LEDGER-SIZING-S1",
        "schema_version": SCHEMA_VERSION,
        "fixture_version": FIXTURE_VERSION,
        "profile": PROFILE,
        "lcg": {
            "seed": LCG_SEED,
            "multiplier": LCG_MULTIPLIER,
            "increment": LCG_INCREMENT,
            "modulus_bits": 64,
        },
        "python_version": sys.version,
        "zlib_version": zlib.ZLIB_VERSION,
        "zlib_runtime_version": zlib.ZLIB_RUNTIME_VERSION,
        "gzip": {"compresslevel": 9, "mtime": 0, "filename": ""},
        "ledger_allocation_bytes": LEDGER_ALLOCATION_BYTES,
        "retained_cap_bytes": RETAINED_CAP_BYTES,
        "max_records": MAX_RECORDS,
        "disclosures": DISCLOSURES,
    }


def write_new(path, data):
    with path.open("xb") as handle:
        handle.write(data)
    path.chmod(0o444)


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def finalize(out_dir, result, failure, wall, cpu):
    manifest = manifest_base()
    manifest["wall_seconds_observed"] = wall
    manifest["cpu_seconds_observed"] = cpu
    gz_data = None
    if failure is not None:
        manifest["classification"] = "GENERATOR_FAILURE"
        manifest["failure"] = failure[:200]
    else:
        compressed = result["compressed_bytes"]
        fits = compressed <= LEDGER_ALLOCATION_BYTES
        manifest["classification"] = "FITS_WORST" if fits else "EXCEEDS_WORST"
        manifest["records"] = result["records"]
        manifest["records_per_counter"] = result["per_counter"]
        manifest["uncompressed_bytes"] = result["uncompressed_bytes"]
        manifest["compressed_bytes"] = compressed
        manifest["bytes_per_record_compressed"] = compressed / result["records"]
        manifest["bytes_per_record_uncompressed"] = result["uncompressed_bytes"] / result["records"]
        manifest["margin_to_allocation_bytes"] = LEDGER_ALLOCATION_BYTES - compressed
        manifest["decompressed_stream_sha256"] = result["stream_sha256"]
        manifest["gz_written"] = fits
        if fits:
            gz_data = result["gz_bytes"]
    sizing_data = canonical_bytes(manifest)
    if len(sizing_data) > SIZING_JSON_MAX_BYTES:
        raise GeneratorFailure("sizing.json over bound")
    files = [("sizing.json", sizing_data)]
    if gz_data is not None:
        files.append(("results.jsonl.gz", gz_data))
    listing = [
        {"path": name, "sha256": sha256_hex(data), "bytes": len(data)}
        for name, data in files
    ]
    sha_data = canonical_bytes({"files": listing})
    files.append(("sha256.json", sha_data))
    total = sum(len(data) for _, data in files)
    if total > RETAINED_CAP_BYTES:
        raise GeneratorFailure("retained artifacts over cap")
    for name, data in files:
        write_new(out_dir / name, data)
    return manifest["classification"], total


def parse_args(argv):
    if len(argv) != 3 or argv[1] != "--output-dir" or not argv[2]:
        raise GeneratorFailure("usage: --output-dir <new-dir>")
    return Path(argv[2])


def main(argv):
    start_wall = time.monotonic()
    start_cpu = time.process_time()
    try:
        out_dir = parse_args(argv)
        if out_dir.exists():
            raise GeneratorFailure("output directory already exists")
        out_dir.mkdir(parents=True, exist_ok=False)
    except (GeneratorFailure, OSError) as error:
        sys.stderr.write("GENERATOR_FAILURE %s\n" % str(error)[:200])
        return 1
    result = None
    failure = None
    try:
        result = generate(start_wall, start_cpu)
    except Exception as error:
        failure = "%s: %s" % (type(error).__name__, error)
    wall = time.monotonic() - start_wall
    cpu = time.process_time() - start_cpu
    try:
        classification, total = finalize(out_dir, result, failure, wall, cpu)
    except Exception as error:
        sys.stderr.write("GENERATOR_FAILURE %s\n" % str(error)[:200])
        return 1
    sys.stdout.write("%s retained_bytes=%d\n" % (classification, total))
    if classification == "FITS_WORST":
        return 0
    if classification == "EXCEEDS_WORST":
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
