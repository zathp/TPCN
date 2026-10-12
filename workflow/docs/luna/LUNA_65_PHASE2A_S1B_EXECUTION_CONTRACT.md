# Luna-65 Phase 2A — S1-B Execution Contract and Independent Verifier Specification (V1)

Gate: `L65-PHASE2A-S1B-EXECUTION-CONTRACT-V1`
Status: **governance contract candidate. Not an execution authorization.**
Authority: Luna-0 (governance). Owner decisions below are PROPOSED and UNDECIDED.

This document executes nothing. The generator was not imported, run or probed.
Interpreter and host facts below were read with read-only commands only
(`python -I -c` to print `sys.version`, file hashes, free-space, path existence).

Maintained prohibitions: S1-B execution NOT AUTHORIZED; verifier implementation
NOT AUTHORIZED unless separately approved; supervisor implementation and
qualification NOT AUTHORIZED; Windows RP probes NOT AUTHORIZED; Phase 2A/2B
fixtures NOT AUTHORIZED; full Spiral benchmark BLOCKED; Luna-64 corrective
execution BLOCKED; Luna-63C FROZEN. D-R7P-1 is undecided. The earlier
"S1-B Authorization Candidate" message was a candidate, not an acceptance.

## 1. Verified baseline (independently re-read this session)

| Item | Value |
|---|---|
| Checkout commit | `08d67859d920364182a5508a1e797a61ce7e7a15` |
| Generator path | `scripts/luna65_phase2a_ledger_sizing.py` |
| Git blob | `088d569c1787e08e3995d10d94aade8517093093` |
| CRLF worktree SHA-256 | `DD2A3DF5D51F234B9A90F8C58F69ED84CDD02DC5B9379B1D19A71CB15D719212` |
| Worktree | only untracked `scripts/luna65_phase2a_supervisor.py` (SHA-256 `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`, not touched) |

The S1-A review package, S1-A handoffs and the generator are unmodified.
Worktree state refers to the pre-contract baseline; this candidate contract,
its handoff and the workflow update are additional untracked or modified
governance files.

### 1.1 Source-conformance findings against S1-A O8/O9 (read from source; not fixed here)

The generator is frozen and not modified by this gate. Reading `manifest_base()`
and `finalize()` against published O8/O9 shows:

- **F1** The manifest records no script path or generator hash/blob and no governing-contract identities. O9 requires "script path"; the generator hash and contract identities are not O9 fields but would make the evidence self-describing. Binding is therefore **external only**: the wrapper log and verifier check 1.
- **F2** O8 asks for a "finalization margin (deflate end block plus 8-byte trailer)". The manifest reports `margin_to_allocation_bytes` = allocation minus the complete closed gzip length (the flagged S1-A interpretation). No separately reserved finalization-margin field exists.
- **F3** The aggregate retained-artifact bytes are printed on stdout as `retained_bytes=` and are not in the manifest (the manifest cannot contain its own size). The verifier computes the aggregate independently.

These are disclosed deviations/interpretations, not waived. Any resolution that
changes the generator creates a new S1-A hash and requires renewed review and
owner acceptance. Proposed D-S1B-5 (section 7) asks the owner to either accept
F1–F3 with external binding, or direct a separate generator amendment before S1-B.
The generator's LF-normalized identity is carried by the Git blob. Execution
preflight must verify both the blob and the CRLF worktree SHA-256.

## 2. Frozen execution command

### 2.1 CLI as implemented (read from source, `parse_args` / `main`)

- Exactly `argv == [script, "--output-dir", <non-empty path>]`. Any other shape
  prints `GENERATOR_FAILURE usage...` to stderr and returns exit code 1 with no
  directory created. No other options exist. The generator reads no input file
  and no environment variable.
- If the path exists (file or directory, **including an empty directory**) the
  generator refuses and returns 1. Otherwise it calls
  `mkdir(parents=True, exist_ok=False)`: it creates missing parents silently.
- On completion it writes, in order, with exclusive-create mode, `sizing.json`,
  `results.jsonl.gz` only when the classification is `FITS_WORST`, and
  `sha256.json`, then sets each file read-only (Windows read-only attribute).
- Stdout is one line `"<CLASSIFICATION> retained_bytes=<n>"`. Exit codes:
  `0` = `FITS_WORST`, `2` = `EXCEEDS_WORST`, `1` = `GENERATOR_FAILURE` or
  usage/directory error.

### 2.2 Frozen values

| Item | Frozen value |
|---|---|
| Interpreter | `C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe` (base CPython, FileVersion 3.11.4, `sys.version` `3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)]`; file SHA-256 `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F`) |
| Why not `.venv\Scripts\python.exe` | `pyvenv.cfg` shows a venv launcher; on Windows the venv `python.exe` can spawn the base interpreter as a child process, so the tracked PID might not be the interpreter. The generator needs only the standard library, so the base interpreter is named directly to keep a single process (proposed D-S1B-1). |
| Interpreter flags | `-I -B` (isolated: ignores `PYTHON*` variables and user site; no bytecode written) |
| Script | `C:\Users\Patrick\Documents\ActiveCode\TPCN\scripts\luna65_phase2a_ledger_sizing.py` |
| Working directory | `C:\Users\Patrick\Documents\ActiveCode\TPCN` (repo root; the generator uses only the absolute `--output-dir`) |
| Evidence parent | `C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\phase2a-sizing` (outside the repository; published S1 destination `%LOCALAPPDATA%\TPCN\evidence\luna65\phase2a-sizing\<run-id>\`, R7 contract §9). Currently absent; see section 5. |
| Output directory (`--output-dir`) | `<evidence parent>\<run-id>` (the published run directory itself; no subdirectory) |
| Run id rule | published convention: `<UTC yyyymmddThhmmssZ>-<seven-character commit ID>` (R7 readiness §4); the timestamp and commit value are fixed by the final execution authorization and recorded in it before launch. A failed invocation is never retried under another run id or directory under this authorization. This contract makes no change to the published destination or run-id convention. |
| Wrapper evidence directory | `<evidence parent>\<run-id>.wrapper` (sibling, outside the generator's output directory; section 4/5) |
| Input files | none |
| Environment | no `PYTHON*`, `TPCN_*` variable set (none are currently set; wrapper must verify) and `-I`. No variable is passed to the generator for any purpose. |

### 2.3 Command (PowerShell 5.1.19041, `C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe`)

The argument string constructed by the wrapper (section 4) is exactly:

```text
-I -B "C:\Users\Patrick\Documents\ActiveCode\TPCN\scripts\luna65_phase2a_ledger_sizing.py" --output-dir "C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\phase2a-sizing\<run-id>"
```

`<run-id>` is substituted with the single value fixed in the final execution authorization.

The equivalent interactive form (reference only, not the authorized method
because it lacks the finite wait) is
`& 'C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe' -I -B <script> --output-dir <leaf>`.

## 3. Execution envelope and enforcement reality

| Limit | Proposed value | Actual mechanism | Enforcement status |
|---|---|---|---|
| Invocations / retries | 1 / 0 | wrapper lock file (section 4) | design-controlled (procedural) |
| Records | exactly 8,196 | generator constant `MAX_RECORDS`, per-counter 2,049 | generator-controlled; verifier re-counts |
| Wall 30 s | in-process, `time.monotonic()` | checked once every 256 records inside `generate()`; origin is the start of `main()`, not interpreter start | cooperative; not checked during gzip close, finalization or file writes |
| CPU 30 s | in-process, `time.process_time()` | same 256-record cadence; counts CPU of this process only | cooperative |
| Outer 45 s | wrapper `WaitForExit(45000)` | origin is a stopwatch started immediately before `Process.Start`; includes interpreter startup | best-effort: a termination request, not a guarantee |
| Compressed ledger <= 786,432 B | gzip stream length from a counting sink | measured, not enforced during generation; the ledger buffer holds at most 786,432 bytes | measured |
| Retained evidence <= 1,048,576 B | generator checks its total before writing; verifier re-sums | tree total plus wrapper log (section 5) | generator pre-check plus verifier |
| Memory | unmeasured, unenforced | none | design target 128 MiB only; **not a ceiling** |

Mismatches between the proposed envelope and its capability (all disclosed):

- **E1** Published D-R7P-1 wording says "record-count and elapsed-time checks per record"; the implementation checks every 256 records. No per-record cost measurement exists.
- **E2** CPU and wall guards are cooperative. A hang inside gzip, the OS or an unguarded phase is caught only by the 45 s outer wait.
- **E3** Generator wall/CPU origins differ from the outer 45 s origin. They are not comparable measurements.
- **E4** The wrapper measures wall only. It does not measure CPU or memory.
- **E5** Whole-process-tree termination is not established (section 4).
- **E6** Read-only attributes are not access control. Same-user processes can alter evidence; D-R7P-2 is unresolved for this run and **no tamper resistance is claimed**. The verifier gives post-hoc consistency detection only.
- **E7** The generator is single-threaded standard-library code with no subprocess use (verified at S1-A by AST scan), so no descendants are expected. That is an observation about the source, not an enforcement.

Overrun classification (wrapper and verifier):

- Outer timeout (no exit by 45 s): `OUTER_TIMEOUT`, reported `GENERATOR_FAILURE` with reason; stop, no retry.
- Self-reported wall or CPU observed > 30 s in a manifest that otherwise claims success: `BUDGET_VIOLATION`; verifier verdict is `EVIDENCE_REJECTED` (section 6.3).
- Unknown process state after termination attempt: `UNKNOWN_FAIL_CLOSED`; stop and report.

## 4. Attended execution and termination wrapper specification

The wrapper is a PowerShell 5.1 script to be written, reviewed and hashed
before execution. **It does not exist and is not authorized to be written by
this document.** It must be a separate approved artifact whose hash the owner
accepts. Requirements:

1. **Attendance.** An operator is present for the whole run and the cleanup interval. The wrapper prints the process id, start time, deadline and each state change to the visible console.
2. **Single invocation counter.** Before launch the wrapper creates the wrapper directory `<evidence parent>\<run-id>.wrapper` (must be absent) and inside it `invocation.lock` with `CreateNew`, recording UTC time and wrapper hash. A present lock or directory means a prior attempt existed: stop. The lock is never deleted.
3. **Launch.** `System.Diagnostics.ProcessStartInfo` with `UseShellExecute=$false`, `CreateNoWindow=$true`, redirected stdout/stderr, `FileName` and `Arguments` exactly as in section 2, `WorkingDirectory` per section 2.2. Stdout and stderr are drained by `ReadToEndAsync` tasks; captured text is truncated to 4,096 characters each when logged (source has two write sites and cannot emit more than a short line or a bounded traceback).
4. **Recorded start.** `[Diagnostics.Stopwatch]::StartNew()` immediately before `Process.Start`; record UTC time, PID, `StartTime`, image path, and the PID's parent PID.
5. **Finite wait.** `WaitForExit(45000)`.
6. **Termination on timeout.** Record the termination-request elapsed time, take a CIM `Win32_Process` snapshot of processes whose `ParentProcessId` equals the PID, then `taskkill.exe /PID <pid> /T /F`. Windows PowerShell 5.1 runs on .NET Framework, which lacks `Process.Kill(bool entireProcessTree)`; `taskkill /T` is the available tree-termination request and is best-effort.
7. **Cessation check.** `WaitForExit(10000)` then verify `Get-Process -Id <pid>` is absent. Repeat the CIM child snapshot. Record both.
8. **Cleanup observation.** Finite 10 s after the termination request; then stop observing.
9. **Fail closed.** If the PID cannot be confirmed absent, a child remains, the exit code is unavailable, or any wrapper error occurs: record `UNKNOWN_FAIL_CLOSED`, report to the operator, do not retry, do not delete evidence.
10. **No automatic retry.** On any outcome the wrapper exits once.
11. **Wrapper log.** `<run-id>.wrapper\wrapper.json` (<= 16,384 bytes, single write, canonical JSON): wrapper hash, command, PID, UTC times, stopwatch elapsed milliseconds for start, exit/termination request and cessation observation (the sole source of outer elapsed time), exit code, truncated stdout/stderr, termination fields, child snapshots, final state. Each child snapshot is limited to at most 8 entries of `{pid, parent_pid, name}` with `name` truncated to 64 characters and an explicit `truncated` flag and count; if the canonical log would still exceed 16,384 bytes the wrapper drops snapshot detail first, and if it still cannot fit, records `UNKNOWN_FAIL_CLOSED` with a minimal log.

What the wrapper cannot establish (reported, not upgraded): termination of
descendants that escape `taskkill /T` (for example a child whose parent already
exited); resource limits; memory; hard real-time behavior; protection against
the wrapper itself being killed. Because no Job Object is involved, **the
envelope is attended best-effort supervision**. If the owner requires
guaranteed whole-tree containment, that is the unqualified supervisor and S1-B
must wait (decision D-R7P-1 option B below).

## 5. Output-directory and evidence-tree requirements

1. Before the run, the operator creates the evidence parent chain `C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\phase2a-sizing` (currently absent; neither it nor `...\TPCN` exists) as empty directories, and the preflight confirms the parent is empty. The generator would otherwise create missing parents silently (`parents=True`). The wrapper then creates only `<run-id>.wrapper` containing `invocation.lock` and later `wrapper.json`.
2. The output directory `<evidence parent>\<run-id>` must be **absent** at launch. The generator refuses any existing directory, including an empty one, so "fresh, empty" in the owner candidate is satisfied by "absent; created empty by the generator". (Proposed D-S1B-4.)
3. Ownership and access: the current user `Patrick` creates everything; no ACL, token, firewall or privilege change is made. The volume is the local `C:` drive.
4. Disk space: preflight requires at least 2 GiB free on `C:` (210.8 GB observed read-only this session).
5. Files permitted in the output directory: exactly `sizing.json`, `sha256.json`, and `results.jsonl.gz` only for `FITS_WORST`. No temporary files exist by design; any other file is a defect.
6. Partial evidence: preserved unaltered. A failed run is never cleaned, overwritten or reused.
7. Overwrite prevention: lock file, generator `xb` exclusive-create and refusal of an existing directory.
8. Aggregate retained evidence = bytes under the output directory + `wrapper.json` + `invocation.lock`, which must be <= 1,048,576 bytes; the output directory by itself is <= 1,048,576 (generator pre-check).

## 6. Independent verifier specification

### 6.1 Identity (prerequisite, not present)

The verifier **does not exist**. Proposed separate implementation target:
`scripts/luna65_phase2a_ledger_sizing_verifier.py` (absent at commit
`08d67859`). Its SHA-256 and Git blob are intentionally unassigned and must not
be invented; they exist only after a separately authorized implementation and
independent review. Implementation: NOT AUTHORIZED here.

Constraints: standard library only (`gzip`, `hashlib`, `json`, `pathlib`, `sys`,
`zlib`); must **not** import the generator or any TPCN module; reads no
environment variable; read-only (never writes inside the evidence directories; prints the
verdict to stdout and exits); permitted environment is the section-2 interpreter
with `-I -B`, run after the generator process has ended. It re-derives every
expected value from the published schema and constants in its own code rather
than from the generator.

### 6.2 Inputs

`--run-root <path>` (the output directory) and `--wrapper-dir <path>` (the `<run-id>.wrapper` directory), plus constants of its own: expected generator commit, blob
and SHA-256 (section 1), the expected command string, and limits. It reads the
generator file bytes for hashing only (never executing it), `invocation.lock`,
`wrapper.json`, and the output directory tree.

### 6.3 Checks (each recorded pass/fail; verdict never copied from the generator)

1. Generator identity: SHA-256 and Git blob (LF normalization computed independently) equal section 1.
2. Invocation identity: the `wrapper.json` command, PID, single lock, exit code, and wrapper termination fields match section 2/4; the exit code agrees with the classification.
3. Required files: exact set per classification (section 5.5); nothing else.
4. Record count: 8,196 lines exactly (only when the gzip exists).
5. Schema version and fixed fields on every record (`schema_version`, `fixture_version`, `neuron_id`, `initial_state_id` per counter using the unmodified counter token, counter order input/episode/lineage/output_event, probe_index 1..2049 per counter).
6. Full independent reconstruction: for every record the verifier reconstructs the entire expected record in its own code and compares it byte-for-byte after canonical serialization, **excluding only the three D-S1-2 substituted checkpoint numeric fields (`x`, `local_time`, `pending_event_time`), for which check 7 is the exclusive authority** (check 6 still validates that those fields exist and, for pending times, their null/non-null mapping). This covers allocated identities, ordinals, both counter snapshots, target/coupled/preparation deltas, outcomes, completion status, exception objects, and both checkpoint objects (`mode`, `phase`, `pending_event_kind`, `processed_event_count`, the output-event processed-count sequence, the `post_rearm_checkpoint` presence/null mapping and values) against the published capacity schema.
7. Declared sizing-only numeric exceptions: the substituted checkpoint `x`, `local_time` and `pending_event_time` values must equal the deterministic sequence produced by replaying the frozen LCG (seed, multiplier, increment, 64-bit modulus as recorded in the S1-A source) in the consumption order defined by the generator source; each must also be a finite binary64 with a 24-character `repr`. Null pending times stay null. Independence is of code, not of specification: the consumption order is taken from the frozen source and must be disclosed as such. Any mismatch is `EVIDENCE_REJECTED`.
8. Compression-stream integrity: valid gzip, CRC32 and ISIZE agree, single member, header `mtime=0`, no filename.
9. Complete gzip size: file byte length equals the manifest's `compressed_bytes` and is <= 786,432.
10. Other sizes: `sizing.json`, `sha256.json`, `wrapper.json`, `invocation.lock` sizes.
11. Aggregate retained size <= 1,048,576.
12. Resource measurements: generator-owned wall <= 30 s and CPU <= 30 s from `sizing.json`; outer elapsed time < 45 s taken only from the canonical `wrapper.json` stopwatch field and validated against the wrapper's recorded start/exit times. Any excess yields `EVIDENCE_REJECTED`.
13. Internal consistency: `sha256.json` hashes equal the actual files; decompressed-stream SHA-256 equals the manifest value; uncompressed byte count; per-record bytes.
14. Verdict consistency: recomputed classification equals the manifest classification and exit code, and the disclosures required by D-S1-1/D-S1-2 are present (single profile, not a proven bound, no nominal-fit claim, no two-run determinism claim).

Verifier outputs: `VERIFIED_FITS_WORST`, `VERIFIED_EXCEEDS_WORST`,
`VERIFIED_GENERATOR_FAILURE`, or `EVIDENCE_REJECTED` with numbered reasons.

Limitations: for `EXCEEDS_WORST` or failure no gzip is retained, so record
content (checks 4–8) cannot be verified and only manifest and size consistency
are checkable; the verifier must say so. Same-user tampering is not excluded
(E6). The verifier shares the unqualified-host trust boundary.

### 6.4 Final reporting rule

Allowed final reports are `FITS_WORST`, `EXCEEDS_WORST`, `GENERATOR_FAILURE`.
`EVIDENCE_REJECTED` and `UNKNOWN_FAIL_CLOSED` are not sizing verdicts; they are
reported as `GENERATOR_FAILURE (evidence rejected, reason ...)` (proposed
D-S1B-3). `FITS_WORST` establishes only that the constructed width-bound
profile fits its declared allocation. It does not establish a universal
compression bound, a nominal fit, two-run determinism, or actual neuron-runtime
capacity.

## 7. Proposed D-R7P-1 decision record (UNDECIDED)

Published wording: the supervisor does not yet exist, so sizing would run
unsupervised with in-process guards (R7 readiness §4 / R7 contract §9).

Facts the owner must accept affirmatively before execution:

1. No qualified Phase 2A supervisor is present.
2. CPU and wall guards are cooperative, checked every 256 records (not per record).
3. Outer PowerShell termination is best-effort.
4. Memory is neither monitored nor enforced.
5. Whole-process-tree termination is not established.
6. Evidence is same-user writable; D-R7P-2 is not resolved for this run and no tamper resistance is claimed.
7. Verdicts apply only to the synthetic width-bound profile.

Option A (recommended only if the owner accepts the limitations): accept one
attended unsupervised S1-B invocation under this contract, one invocation, zero
retries.
Option B: decline; defer S1-B until the supervisor is qualified.

Companion proposed decisions: **D-S1B-1** base interpreter plus `-I -B`;
**D-S1B-2** separately authorize the verifier implementation and hash
(`scripts/luna65_phase2a_ledger_sizing_verifier.py`) and the wrapper
implementation and hash before execution; **D-S1B-3** reporting of non-verdict
outcomes; **D-S1B-4** absent-leaf output rule; **D-S1B-5** accept the source-conformance findings F1–F3 with external binding, or direct a separate generator amendment (new S1-A hash) before S1-B.

**No acceptance is recorded by this document.**

## 8. Owner authorization needed before execution (all required)

1. Decide D-R7P-1 (Option A) with the section 7 limitations stated.
2. Decide D-S1B-1 through D-S1B-5.
3. Separately authorize implementation of the verifier and wrapper, then independent review and publication of their hashes.
4. Luna-0 preflight after those publications: checkout, generator identity, command, run directory absence, disk space, verifier and wrapper identities, attendance, no discrepancy (stop on any mismatch).
5. A fresh explicit execution authorization naming the final commit and hashes.

Exact owner text proposal (not executed, not accepted): "I accept D-R7P-1
Option A with the stated limitations, D-S1B-1 through D-S1B-5, and authorize
exactly one attended S1-B invocation under contract `<commit>`, with wrapper
`<hash>`, verifier `<hash>`, zero retries."

## 9. Governance publication allowlist (this gate)

Only: this contract, its handoff
`workflow/handoffs/luna-0-luna65-s1b-execution-contract-20261012.md`, and
`workflow/docs/luna/LUNA_WORKFLOW.md`. The generator, supervisor scaffold and
all historical records are excluded.
