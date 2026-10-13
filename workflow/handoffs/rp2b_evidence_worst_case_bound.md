# RP-2B Lane E — Static retained-evidence worst-case sizing

**Revision:** Corrective R1 — 2026-10-12  
**Reviewed baseline:** `96fb4aec100578db6939136b4ed7985478f18bb8`  
**Scope:** static contract/schema/source/package sizing only. No execution, preflight, probe, wrapper, test, or runtime operation was performed.  
**Verdict:** **BLOCKED — EVIDENCE FIT NOT ESTABLISHED**

## 1. Decision and sizing boundary

The frozen RP-2 restricted-token contract (§5, “Output,” and its evidence
accounting paragraphs) requires at most **1,048,576 logical bytes** across
simultaneously retained artifact files and representations, with a
**917,504-byte payload ceiling** and **131,072-byte finalization reserve**.
It requires every representation to be counted, including encoded/raw copies,
structured evidence and temporary/final copies; it also requires retained
high-water, final-size reconciliation, consumed-reserve and discarded-byte
evidence. A write-time guard is not a proof that every required maximum or
failure record can be retained.

Use the following scope distinction:

* **On-disk retained evidence:** the files under the fresh `EvidenceLeaf`.
* **Simultaneously retained representations:** file bytes plus live
  in-memory/encoded/decoded representations counted by the contract while
  present. These contribute to the peak even when they are not separate
  files.
* **Transient working buffers:** short-lived reader, parser, serializer,
  hashing and native/API buffers. They are not additional retained evidence
  files; where source accounting includes them (for example in `MemoryBytes`
  or a reservation), that accounting contribution must still be counted
  once at peak. No independent upper bound for all such transient buffers is
  specified by the contract.
* **External governance evidence:** authorization, provenance, review,
  operator/host binding, and any future signed or immutable manifest kept
  outside `EvidenceLeaf`. No rule reviewed here says whether this entire
  package is inside or outside the 1 MiB run-artifact ceiling, or fixes its
  serialized schema/maximum size. Its contribution is therefore
  **UNBOUNDED / not specifiable** for an aggregate that includes it.

Accordingly the governing total is a peak, not a sum of unrelated nominal
estimates:

```text
TOTAL_MAX = max over every lifecycle instant t of
    [D(t) + M(t) + P(t) + X(t)]

D(t) = on-disk artifact bytes retained at t
M(t) = other simultaneously retained in-memory representations counted by contract
P(t) = live probe representation reservation/count not already included in M(t)
X(t) = any external/console/operator/manifest evidence that the governing
       boundary requires retained and counted at t

Required proof: TOTAL_MAX <= 1,048,576 bytes, with payload-only growth
<= 917,504 bytes and finalization evidence fitting without discarding any
mandatory record.
```

The source approximates this with `DiskBytes + MemoryBytes +
RemoteLiveReservation + Extra`; exact equivalence between every required
record and these accounting terms is not established. Do not add the same
representation twice, but do count each distinct simultaneous copy. Do not
infer fit from the fact that `Charge` rejects a write that would cross its
current ceiling.

## 2. Retained artifact inventory

The source’s intended leaf has ten possible fixed filenames, not a separately
serialized `manifest.json`. The manifest-like file inventory is embedded in
`report.json`. Five files are created empty after leaf creation; `outer.jsonl`
is created on its first outer record; the three `low-*.bin` files are created
only after a successful Low-create result; and `report.json` is attempted
during finalization. Thus an early failure may leave no leaf, and a leaf
without Low creation has fewer than ten files. This differs from Lane D’s
assertion that exactly ten files are always present; the governing post-run
checklist names ten files.

| Mandatory evidence / destination | Serialization and encoding in source | Count / source bound | Maximum retained bytes proved by specification/source |
|---|---|---:|---|
| `medium-stdout.bin` — P relay, U1–U3 records, lifecycle, and hex-encoded Low capture chunks | Byte-preserved P stdout. Relay is compact, sorted-key ASCII JSONL (`json.dumps(... ensure_ascii=True, sort_keys=True, separators=(",", ":")) + LF`). Each P relay line is at most 16,384 bytes. Low payload chunks are at most 4,096 raw bytes and encoded as lowercase hex in JSON, so their relay representation is larger than the decoded bytes. | One stream; total relay send cap is 458,752 bytes ordinarily and 491,520 bytes for designated cleanup stages (917,504/2 plus 32,768); 16,384-byte record cap. | **≤491,520 bytes** for this raw relay stream under the source send counter. It does not bound duplicated `U*.jsonl`, decoded Low files, or concurrent representations. |
| `medium-stderr.bin` — raw P diagnostics | Byte-preserved binary capture; no text decoding or escaping by O. Probe cleanup-failure path writes a textual diagnostic to stderr. | One stream; subject to O’s aggregate charging, no independent per-file cap. | **Not independently specifiable**. Aggregate write guard applies, but the diagnostic path is not given a complete maximum length. |
| `U1.jsonl`, `U2.jsonl`, `U3.jsonl` — security/token, runtime/environment, and PSS/object/resource observations | Relay bytes copied to each section file with LF. Input is ASCII JSONL; each source record is capped at 16,384 bytes. JSON strings from Python use ASCII escapes; the wrapper’s own JSON uses UTF-8. | Inventory walks cap at 256 entries each; three named inventory checkpoints can therefore emit up to 768 entry records plus completion records. Additional records are constrained by relay aggregate and per-record limits. | **No independently derivable aggregate maximum** beyond `DiskBytes`/overall guard; every copied section record is a second retained representation of relay content. |
| `low-stdout.bin`, `low-stderr.bin`, `low-ledger.bin` — decoded Low streams | Original captured bytes, hex-decoded from the Medium relay. Low emits ASCII compact sorted-key JSONL `READY` and `END` on each of the three streams. Each Low record is limited to 16,384 bytes; wrapper validates two records per stream for complete streams. | Three files; valid complete path has two records per stream. Decoded chunk size ≤4,096 bytes per relay capture. Files are conditional on Low creation. | **≤32,768 bytes per stream** only for the expected two-record Low protocol. Invalid/extra output is a failure and remains subject to aggregate charge; the contract does not assign a separate disk cap per Low file. |
| `outer.jsonl` — O admission, preflight, pipe, stop, and cessation observations | Compact PowerShell `ConvertTo-Json -Depth 30 -Compress`, UTF-8 plus LF. Individual O records are limited to 16,384 bytes. Outer records include run/source/host bindings, token and SD readbacks, process/job/timing results, failure events, and retained P FINAL data. | One append stream; no explicit record-count constant. Process and wait paths are bounded by the 10/5/20-second deadlines but API latency and exact event count are not a deterministic serialization schema. | **No independently proved maximum**; only overall charge protects writes. |
| `report.json` — final result and per-file manifest | PowerShell compact JSON, UTF-8 plus LF, schema label `L65-RP2-FINAL-1`. Includes verdict, run/tick values, cessation, alert, errors, Low sizes, per-file lengths/SHA-256, byte counters, limits, and evidence-claim text. | One final record; errors capped at 8 with a separate omitted count; inventory map/file map depend on observed run. No dedicated maximum report length is specified. It excludes its own final length/hash from the embedded `files` map. | **Not independently specifiable.** `Charge` constrains its write against the remaining 1 MiB total; this does not prove the required report fits for every legal preceding payload/failure state. |
| Report digest and final console line | Wrapper prints verdict, `report.json` length, SHA-256 and high-water to `[Console]::WriteLine`; controller errors and unresolved-containment alert also use `[Console]::Error.WriteLine`. | No file, record cap, capture sink, or charge path is specified for these console records. | **UNBOUNDED / not specifiable** as retained evidence. The source does not route these bytes through `Charge`/`Write-Artifact`; retention/capture and length are not bounded by this evidence ledger. |

The contract’s expected ten-file set is: `report.json`, `outer.jsonl`,
`medium-stdout.bin`, `medium-stderr.bin`, `U1.jsonl`, `U2.jsonl`, `U3.jsonl`,
`low-stdout.bin`, `low-stderr.bin`, and `low-ledger.bin`. The source’s
conditional file creation and console-only failure/alert paths prevent a
static claim that all required records are always materialized in those ten
files.

## 3. Mandatory-field inventory and bounds

| Governing requirement | Where represented / format | Known bounds | Maximum / gap |
|---|---|---|---|
| Authorization and execution grant | Prior authorization and current RP-2B candidate package; no authorized run grant is present. The candidate is JSON, but no JSON Schema or serialization-size rule is supplied. | Current candidate status is blocked and execution is false. Future grant values include operator, run ID, destination and profile reconciliation. | **UNBOUNDED / not specifiable** for any retained authorization bundle; future content and whether included in 1 MiB are undefined. |
| Provenance and source identity | Static commit, branch, probe/wrapper paths, Git blobs, checkout SHA-256, literal byte length/digest, host/interpreter identities; source preflight record and report do not constitute the full external provenance package. | Fixed source digests have 64 uppercase hex characters; Git object IDs are fixed 40 hex characters; literal is 6,583 ASCII bytes. Run ID is ASCII grammar `[A-Za-z0-9][A-Za-z0-9-]{0,63}`. | Static identity values are bounded, but their full serialized authorization/provenance record has **no specified schema or total maximum**. |
| Host and environment | `preflight` O record and P relay P0/U2/Low READY observations. Includes host image/version/bitness, fixed paths, file hashes/tree digests, OS tuple, cwd, argv, environment, interpreter and module observations. | Host file list: 5 fixed files; host trees: 6 fixed roots with declared counts; Python tree rows: 11 fixed roots; process/environment schemas and source record cap 16,384 bytes. | Per-record cap exists, but the whole set, any retained operator transcript, and any required external host attestation lack a complete max/schema. |
| Preflight and source admission | O `preflight`, `Medium-pipe`, `P-admission`, and final token readback records in `outer.jsonl`; no evidence leaf exists if failure occurs before leaf creation. | Each outer JSONL record ≤16,384 bytes. Fixed baseline path and hash values; run ID ≤64 characters. | Number/complete mandatory preflight record set on every failure path is not specified to be materialized; console preflight diagnostics are uncharged. |
| Security and token | U1/U2/U3, preflight/admission records, Low READY observations; ASCII/UTF-8 JSON. Token query buffers ≤65,536 bytes; group/restricting/privilege enumeration ≤256 entries; privilege name buffer 256 wide characters; each record ≤16,384 bytes. | Enumeration and record limits exist. Python failure errors retain at most 8 entries; each string is shortened when over 512 characters to a 480-character prefix plus marker. | No exact all-record count/serialized aggregate is specified independently of the 491,520 relay budget and overall guard. |
| Process/job and resource | P relay and outer/report observations: create results, PID/creation time, image, handles, job membership/limits, resource samples, stream status, EOF, exit and high-water. JSON integers and strings. | Active-process backstop 8; inventory cap 256; P active 10 s, cleanup ≤5 s, O deadline 20 s; job memory charge 67,108,864 bytes and job user-time 5 s in frozen source. Resource sampling attempts at 250 ms intervals. | Deadlines bound intended sampling duration, not API-call latency or exact record count. Full output-size proof is absent. These RP-2 values also do not satisfy the separate requested 256 MiB/120 s resource profile (Lane B/Luna-0 blocker). |
| Timing and timestamps | O/P monotonic `GetTickCount64` millisecond ticks in JSON; P0 also includes `time.time_ns()` wall-clock nanoseconds. No ISO timestamp format is emitted by these source records. | Tick and integer fields have machine-width source types; P0 wall timestamp is integer nanoseconds. Run ID has 64-character maximum but is not itself a timestamp schema. | Runtime numeric spelling is finite per type, but no exact max serialized record set/count is proved. External review/operator timestamp strings are not format-bounded. |
| Cessation and alert | P `FINAL` contains cessation state and alert text; `report.json` copies final-P state and operator alert; O may also emit an unresolved alert to console stderr. | Source verdict vocabulary: `RP2_PASS`, `RP2_PARTIAL`, `RP2_FAIL`, `RP2_UNKNOWN_FAIL_CLOSED`, `RP2_CONTRACT_DEFECT`. Alert text is a fixed literal in source records. Missing Low cessation must remain UNKNOWN and alert the operator. | The in-file alert value is finite, but the mandatory operator alert is also console-only and uncharged; no bound/capture/retention rule. Lane D’s alternate classification names are not canonical. |
| Failure evidence and truncation | P cleanup ledger/final record, O `errors`, omitted counters, outer failure records, report. | P stores at most 8 errors and at most 4 values per error; long strings truncate to 480 plus marker. O stores at most 8 failures; strings longer than 512 truncate to 480 plus marker; later failures increment an omitted counter. O record ≤16,384 bytes. | These caps bound some diagnostics, not all O record counts, exception objects/non-string fields, console diagnostics, or the required retention of every failure. Truncation/omission is explicitly evidence loss, not a basis to count omitted content as retained. |
| Manifests and digests | `report.json.files` maps already-written artifact names to `{length, sha256}`; fixed source/host tree manifests are digests over enumerated file identities. Wrapper prints report’s own hash to console after writing. | Up to 9 prior leaf files can enter `files` (the other eight non-report artifacts plus conditional Low streams); each digest is 64 hex characters, each length is numeric. Source closure counts are fixed by the source tables. | No schema-level byte ceiling for `report.json`; report self-digest is outside it; console digest is uncharged. External authorization/provenance manifests have no bounded format or growth rule. |
| Classification / final disposition | `L65-RP2-FINAL-1` report and P `FINAL` record. | Five canonical source classifications listed above; finite literals. | Literal values are bounded; classification evidence as a complete manifest/report still has no proven maximum. |
| Cleanup and partial-run preservation | Contract requires retained partial evidence, no overwrite/reuse, and no cleanup that deletes evidence. Source closes owned handles/streams and removes in-memory/native resources where safe; no temporary artifact schema is defined. | One invocation, zero retries, one Low creation attempt, at most one exact-handle P termination request; no source-created temporary files are specified. | Failure before leaf creation can leave no evidence. Finalization/write failure can leave an incomplete leaf/report; the contract says preserve it, so its final retained size/manifest completeness is not guaranteed. No deletion authority is supplied. |

## 4. Serialization, escaping, paths, growth, and lifecycle

1. **JSON formats are not one canonical schema.** Python P relay/Low records
   use compact sorted-key ASCII JSON with `ensure_ascii=True` and LF. The
   PowerShell O and report records use `ConvertTo-Json` followed by UTF-8 and
   LF. Raw binary stream files preserve captured bytes. The source contains
   record labels and runtime validators, not a complete published JSON
   Schema for every record or a byte-sizing schema for the complete
   authorization/evidence package. ASCII JSON escaping can expand characters
   (for example, non-ASCII BMP characters as `\uXXXX`); hex relay capture
   doubles every raw input byte before JSON framing. No text-size estimate may
   substitute for serialized-byte counts.
2. **Paths and manifest growth.** The wrapper requires the exact base
   `C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\rp2-` plus a 1–64
   character run ID; it rejects noncanonical/alternate-stream routes and
   reparse points. The leaf names are fixed. `report.json`’s file manifest can
   contain at most the other nine named artifacts (conditional Low files
   included); each hash is 64 hex characters. File names, JSON property
   names, nested final-P data and PowerShell JSON escaping contribute overhead
   not separately budgeted as a fixed schema size.
3. **Time and exact event count.** The operation windows (10 s active, up to
   5 s cleanup, 20 s outer) and 250 ms resource-sample condition constrain
   intended event opportunities; they are not a formal maximum event-count
   schema. API latency is expressly not hard bounded. The 16,384-byte record
   cap and aggregate byte guard constrain writes but do not provide an
   independently computed total of every mandatory record.
4. **Representation overlap.** Medium stdout retains relay bytes; U1–U3 retain
   copies of section records; Low files retain decoded bytes whose hex
   encodings were present in the relay; and final report metadata repeats
   selected final-P/error/size/hash information. These copies overlap in
   meaning but are distinct bytes and count concurrently when live. The
   contract prohibits treating their semantic overlap as byte deduplication.
5. **Failure states.** Failures before fresh-leaf creation produce no leaf.
   Failures after leaf creation may leave empty/partial streams; failures
   during finalization can leave a partial `report.json` or omit its hash and
   final accounting. If O cannot write the report, a stderr message and
   `RP2_UNKNOWN_FAIL_CLOSED` alert may be the only terminal notification, and
   those console bytes are not charged. Required partial evidence must be
   preserved, not removed to make a size calculation pass.
6. **No standalone manifest file / no approved cap for future governance
   growth.** Runtime’s `report.json` is the only file-list manifest; current
   authorization candidate and review/handoff records are separate
   documentation/JSON files. No file-count, field-length, revision-history,
   signature/attestation, or aggregate package-growth rule bounds those
   future materials.

## 5. Transient buffers versus retained evidence

The following are not independent retained evidence files, but their
simultaneous representations matter to the contract’s peak charge:

* P token/API buffers are capped at 65,536 bytes; three Low logical record
  reservations are 49,152 bytes; record/line and stream buffers include
  16,384-byte limits and 4,096-byte read chunks. P declares a 393,216-byte
  retained-representation reservation. This is a source accounting
  reservation, not an exact serialized byte total for all records.
* O declares a 131,072-byte fixed memory reservation and three-times-JSON
  projections for selected retained O metadata; it also accounts for a
  partial relay line and the remote reservation. Actual object/runtime
  allocator size is not thereby bounded or measured exactly.
* Reader buffers, parser objects, conversion arrays, JSON serializers,
  hashing buffers, and native/API structure buffers are transient. They must
  not be misreported as on-disk bytes; any portion retained simultaneously
  must still be represented in the all-representation peak. The materials do
  not give a complete independent maximum for all such buffers.
* The contract counts temporary/final copies when simultaneously retained.
  Source claims no P-created temporary/intermediate artifact. O’s `report`
  serialization and hash computation, P’s report/relay serialization, and
  decoded Low byte arrays are still live representations during parts of
  finalization/capture. Their complete maximum lifetime overlap is not
  established by a schema-level proof.

## 6. Calculation and prior findings

The only unconditional arithmetic established from the frozen constants is:

```text
TOTAL_LIMIT       = 1,048,576 bytes
PAYLOAD_LIMIT     =   917,504 bytes
FINAL_RESERVE     =   131,072 bytes
P reservation    =   393,216 bytes
O fixed reserve  =   131,072 bytes
P ordinary relay =   458,752 bytes
P cleanup-stage relay ceiling = 491,520 bytes
```

These are ceilings/reservations, **not** a sum that establishes fit. In
particular, the source’s `Charge` checks
`DiskBytes + MemoryBytes + RemoteLiveReservation + Extra` against either
917,504 or 1,048,576. A successful check proves only that this particular
write is accepted against the current counters. The 1 MiB final cap and
reserve-before-write policy do not prove that all required records,
duplications, hashes, external manifest material, and failure/alert evidence
fit for every admitted maximum/failure path.

Lane D’s asserted ~774 KiB peak (`~180 KiB disk + ~210 KiB O memory +
384 KiB remote reservation`) is **not** a worst-case calculation. Its per-file
figures are labeled “typical,” its disk/memory partition has no source-derived
serialized-size/count table, it does not reconcile simultaneously retained
relay and copied U/Low representations, and it excludes/requires
reconciliation for wrapper console diagnostics and finalization. Luna-0
independently identified that evidence-fit conclusion as unsupported and
required a worst-case schema bound. Lane B separately found that the frozen
64 MiB/5 s/10-5-20 RP-2 profile conflicts with the requested 256 MiB/120 s
profile; this report does not resolve that distinct blocker. Luna-0 also
rejected Lane C’s corrupted report and unsupported ABI claim. These prior
findings are carried forward; no Lane D estimate is reused as a bound.

## 7. Unresolved points and disposition

1. The exact aggregate sizing boundary for external authorization,
   provenance, operator/host attestations, terminal console output and
   retained review/manifest documents is unspecified.
2. The complete mandatory-record schema, per-field character/byte maxima,
   escaping rules across both serializers, and maximum count for every O/P
   record and error/failure path are not specified together in one
   machine-checkable schema.
3. Exact maximum sizes of `outer.jsonl`, `U1.jsonl`–`U3.jsonl`, and
   `report.json` are not derived from the record limits, inventory caps,
   identifiers, duplicated representations, and maximum failure data.
4. Mandatory operator alert and final report digest are printed to console
   outside the charged artifact writer; their capture/retention and size are
   not bounded.
5. The ten-file checklist and conditional source file creation diverge on
   preflight failure and Low-not-created branches. Incomplete artifacts must
   be preserved, but their final manifest/digest completeness is not
   guaranteed.
6. A cap-induced rejection/omission is fail-closed behavior, not proof that
   the full required evidence fits. It cannot be counted as acceptable
   truncation or used to discard mandatory evidence.

No machine-checkable sizing model is emitted: the reviewed materials define
record labels, constants and runtime checks, but do not provide a complete
schema for all mandatory retained content or its out-of-leaf boundary. Adding
one would require inventing constraints not present in the governing
materials.

**Verdict: BLOCKED — EVIDENCE FIT NOT ESTABLISHED**

### Sources reviewed

* `workflow/docs/luna/LUNA_65_PHASE2A_RP2_RESTRICTED_TOKEN_COMPATIBILITY_CONTRACT.md`
  §§5–6 (retention, byte-accounting, failure classifications).
* `workflow/docs/luna/LUNA_65_PHASE2A_RP2_OUTER_LAUNCHER_CORRECTIVE_R1.md`
  §§3–7 (single writer, relay, representation accounting, failures).
* `workflow/docs/luna/LUNA_65_PHASE2A_RP2_R1_OWNER_DECISIONS.md`,
  D-RP2-MEDIUM-1 and D-RP2-OUTER-1.
* `scripts/luna65_phase2a_rp2_compatibility_probe.py`, constants and
  serializers/accounting at lines 20–35, 208–223, 254–269, 720–722,
  890–931, 1115–1167, 1288–1360, 1530–1654, 1700–1792.
* `scripts/luna65_phase2a_rp2_outer_wrapper.ps1`, constants and serializers/
  accounting at lines 20–27, 594–649, 655–710, 724–764, 773–778,
  829–833, 903–925, 944–1043.
* Current RP-2B package:
  `workflow/handoffs/rp2b_authorization_manifest_candidate.json`,
  `rp2b_authorization_readiness.md`, `rp2b_lane_b_resource_readiness.md`,
  `rp2b_lane_d_operator_evidence_readiness.md`.
* Prior adjudication:
  `workflow/handoffs/rp2b_luna0_independent_review.md` §§2–4 and
  `rp2b_lane_c_native_race_readiness.md` as characterized by that review.
  Lane D’s unsupported `~774 KiB` estimate is in §3 of its report.
