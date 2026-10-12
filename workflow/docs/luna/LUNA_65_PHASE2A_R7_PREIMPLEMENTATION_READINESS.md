# Luna-65 Phase 2A R7 Preimplementation Readiness Package

**Gate:** `L65-PHASE2A-R7-PREIMPLEMENTATION-READINESS`
**Owner:** Luna-0 (governance and read-only feasibility analysis only)
**Date:** 2026-10-12

This package prepares owner decisions and bounded authorization candidates. It
runs nothing. No source implementation, static validation, runtime probe,
synthetic sizing execution, supervisor qualification, capacity fixture or
benchmark is authorized by it, and nothing in it is an owner acceptance. A
PASS on this package makes it ready for owner review only.

**Supervisor implementation: NOT AUTHORIZED.**
**Synthetic sizing execution: NOT AUTHORIZED.**
**Supervisor qualification: NOT AUTHORIZED.**
**Phase 2A/2B fixtures: NOT AUTHORIZED.**
**Full Spiral benchmark: BLOCKED.**
**Luna-64 corrective execution: BLOCKED.**
**Luna-63C: FROZEN.**

## 1. Verified publication baseline

| Item | Verified value |
|---|---|
| Branch | `governance/luna64-r4.3-freeze-20261010` |
| HEAD and `origin` | `33a753d3343ee6b2c3f5b40349d1cf06895eaa74` (parent `baf03722…`; R7 `2e6095d…` is an ancestor) |
| Commit content | exactly three files, 560 insertions |
| Authoritative contract | `workflow/docs/luna/LUNA_65_PHASE2A_R7_OWNER_DECISIONS_AND_PROFILES.md` |
| Scaffold | `scripts/luna65_phase2a_supervisor.py`, untracked, SHA-256 `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`, unchanged |
| Phase 2A test file | `tests/test_luna65_capacity_direct.py` **does not exist** |

Three-file identity reconciliation (each file separately; the contract result
does not stand in for the other two):

| File | Reviewed or worktree SHA-256 (CRLF checkout bytes) | Git blob content SHA-256 | Relation |
|---|---|---|---|
| Contract | `9CA2E34DCC1F35BA72156B86C889365C2EB6873979E7863248594AF214169B73` (the four-lane PASS hash) | `6C5EBFD955EFDF472897B18E0126E83C85AFF56AE98BA5BE0D5D3564EF984671` (Git blob `0759087811610f40c73de91d8662c28d8ebce54d`) | blob equals the worktree after CRLF to LF normalization |
| Handoff | `1C556A808CCCEB071EBAB89265B26F8E30342BA523D1EC8894508DCE105D2E19` | `1565AE8B1C1F1C4EC008273B65364C2AB3F4C001672F20DD19AD0C5B7D88895D` (blob `95b51cf8c558ed9734a1c189ad18a3a0c1d06d5b`) | equal after normalization; **never independently reviewed** |
| `LUNA_WORKFLOW.md` | `9AC157ED35427910149A9540A99F809BAE273F7DDD9AA9CF4B2AC928BD44FAFF` | same (blob `ed1acdee7ef245341b1a6f9d4599c0e812b88804`; the file is CRLF and `-text`) | raw bytes equal; entry not independently reviewed |

Findings of the reconciliation:

1. The independent reviews covered the contract only. The handoff and the workflow entry were written by Luna-0 after the reviews and were not themselves independently reviewed. This package submits them to review (lane D).
2. The handoff field `contract_sha256_lf_normalized` holds the CRLF worktree hash `9CA2E34D…`, not an LF-normalized hash. The LF-normalized (committed blob content) hash is `6C5EBFD9…4671`. The published records are not rewritten; this is an erratum, and the field is to be read as "reviewed worktree bytes".
3. The "contract hash" required by any future authorization is therefore two-valued: reviewed checkout bytes `9CA2E34D…` (CRLF on this host) and blob content `6C5EBFD9…` (LF). Authorization text must name which byte form it binds. The recommended binding is the Git blob ID plus the LF-normalized SHA-256, because it does not depend on `core.autocrlf` of the checkout.

## 2. Exact published wording

Quoted from the published contract (commit `33a753d`), unchanged.

**D-R7P-1 (§9, "Execution model decision"):** "the supervisor does not yet exist, so sizing runs unsupervised with in-process guards (record-count and elapsed-time checks per record). That is owner decision **D-R7P-1**."

**D-R7P-2 (§8):** "The D-R7-8 metric is defined over every file under the evidence tree. The architecture can enforce it against the controller and the Low-integrity workload, but not against peer same-user Medium processes, because the workload and `P`/`W` share the user SID and no separate identity is available without administrator action. The owner must either (a) accept that peer same-user tampering is outside the enforced boundary, with the finalization enumeration serving as post-hoc detection that fails the run on any excess, or (b) direct a separate-identity design. This contract does not amend the metric or the cap; it records the gap as a precondition to implementation authorization."

**R-TRUST (§11):** "`W` and `P` run under the same-user Medium token. Their 'no writes outside the evidence tree' and 'repository read-only' properties are source-level program behavior, verified by static review, not enforced by token, ACL or label. A defect or compromise of `W` or `P` is not contained by the OS."

**§4.4 workload environment allowlist** (all other variables absent): `PYTHONHASHSEED=0`; `TPCN_LUNA65_LEDGER_HANDLE=<decimal inherited ledger pipe handle>`; `PYTHONDONTWRITEBYTECODE=1`; `SYSTEMROOT=<host %SystemRoot%>`. `P` and `W` use the same allowlist plus the nonce and `T0` carried over pipes. The contract states that the substitution and the hygiene variables are "flagged for explicit owner acknowledgement in the implementation authorization (§12)."

**Additional amendment found by this review (not flagged by the published §4.4).** The published capacity command is `.\.venv\Scripts\python.exe -m pytest -q -x tests/test_luna65_capacity_direct.py`, "only the two specified environment overrides" and "retries are zero". Published contract §4.3 adds `-B` and `-p no:cacheprovider` to the workload invocation. That is a change to the published exact command and needs the same owner acknowledgement as the environment term. It is added to the matrix below as part of decision E.

No acceptance of any of these is inferred from the publication PASS.

## 3. Owner-decision matrix

The allowlist is **not** broadened: `TEMP`, `TMP`, `PATH`, `USERPROFILE`, `LOCALAPPDATA`, `PYTHONPATH` and every other variable remain absent. Whether the interpreter actually runs without them is runtime prerequisite U2, not a reason to add variables now. If U2 fails, a variable is added only by a new reviewed amendment.

### Decision A — D-R7P-1: unsupervised synthetic sizing

| Field | Content |
|---|---|
| 1. Proposed policy | One bounded sizing invocation of `L65-PHASE2A-LEDGER-SIZING-S1` (§4) with in-process guards only, before any supervisor exists |
| 2. Recommendation | Accept **only** the attended variant: owner present; exactly one invocation; zero retries; an outer wall timeout of 45 s imposed by the invoking PowerShell using `Wait-Process -Timeout` and `Stop-Process -Id <that PID>` (a plain wrapper, not the supervisor, not a source file); the S1 script passes its own non-execution static review first. If the owner declines, no sizing result is obtainable and implementation stays blocked, because the ledger path depends on the result |
| 3. Security implications | No Job Object, no memory limit, no token restriction, same-user Medium token with full user rights. Containment is the script's absence of any file, process or network code beyond a bounded output directory. The wall timeout is attended and best-effort; memory is neither checked nor measured by S1 (the 128 MiB value is a non-enforced by-construction design bound); a hung or runaway process has no OS-enforced or in-process ceiling |
| 4. Remaining proof obligations | S1 script written and statically reviewed for the exclusions of §4.3; an exact output-path rule; result independently re-verified (§4.8) |
| 5. Would authorize | exactly one execution of the reviewed S1 script under §4 ceilings, after a second explicit authorization naming the script's SHA-256. **Contract amendment requested as part of Decision A:** the published S1 contract requires nominal and width-bound profiles with `FITS_WORST_AND_NOMINAL` as the blocker-removing result. This package proposes a single width-bound profile (8,196 records in total) with `FITS_WORST` as the fit criterion and no nominal result. Until the owner expressly accepts that amendment, `FITS_WORST` is a proposal only and cannot remove the published sizing blocker; the published condition is retained |
| 6. Remains prohibited | any other execution; retries; supervisor work; reading E2 identity counters; Spiral inputs, training, scoring, network; writing outside the S1 output directory |

### Decision B — D-R7P-2: peer same-user evidence tampering

| Field | Content |
|---|---|
| 1. Proposed policy | Option (a) of the published text. The 1 MiB cap is enforced against controller-authored bytes and the Low workload. Peer same-user Medium writes are outside the enforced boundary and are detected only after the fact by the finalization tree enumeration, which fails the run on any excess or unexpected file |
| 2. Recommendation | Accept (a). Option (b) needs a separate account or another identity, which requires Windows account changes that this phase prohibits, and was not requested |
| 3. Security implications | A same-user process can add, change or delete evidence between controller writes and can raise the on-disk total past 1 MiB without the controller's accounting noticing until finalization. Evidence from a run is trustworthy only if the enumeration, the `sha256.json` manifest and a quiet host agree. The owner's "hard" retained-artifact requirement is thus narrowed to a hard limit on controller writes plus post-hoc detection. Acceptance must say so |
| 4. Remaining proof obligations | static review of reserve-before-write and finalization enumeration; qualification Q10 of the evidence writer |
| 5. Would authorize | implementation to treat peer same-user writes as out of scope and detect-only |
| 6. Remains prohibited | claiming the 1 MiB cap is enforced against all processes; any ACL, account or privilege change |

### Decision C — R-TRUST: trusted-controller filesystem behavior

| Field | Content |
|---|---|
| 1. Proposed policy | `W` and `P` run under the unmodified same-user Medium token; their path limits are program behavior |
| 2. Recommendation | Accept, with static review as the sole control and an explicit statement that a defect in `W` or `P` is not OS-contained. A derived restricted token for `P` is not recommended: it would force new designs for evidence-tree access and for deriving the workload token, and cannot be shown feasible here |
| 3. Security implications | A `W` or `P` defect can write anywhere the user can, including the repository and other evidence. No second line of defense exists |
| 4. Remaining proof obligations | single-file static review of the absence of write code paths other than the evidence tree; hash binding of source |
| 5. Would authorize | implementation of `W` and `P` under the unmodified token |
| 6. Remains prohibited | describing the evidence tree or repository as protected from `W`/`P`; adding privileges |

### Decision D — Environment allowlist and command amendment (§4.4 and `-B`, `-p no:cacheprovider`)

| Field | Content |
|---|---|
| 1. Proposed policy | The four-variable workload allowlist quoted in §2 and the two added interpreter and pytest flags, as the exact amendment of the published capacity terms |
| 2. Recommendation | Acknowledge exactly these and no others, conditional on the U2 probe. If U2 fails, return for a new reviewed amendment rather than widening |
| 3. Security implications | Removes the evidence path from the workload (the workload cannot name the evidence directory). `SYSTEMROOT` is not secret. The handle number reveals nothing usable without the handle. The test module must write canonical records to the inherited handle; that file does not yet exist |
| 4. Remaining proof obligations | the test module reads the handle variable and writes only to it; static review of its absence of other writes |
| 5. Would authorize | the supervisor to build exactly this environment and command |
| 6. Remains prohibited | any additional variable, `TEMP` or `TMP`, a different interpreter command, retry, network |

## 4. Synthetic ledger-sizing authorization proposal (`L65-PHASE2A-LEDGER-SIZING-S1`)

Two separate authorizations are required, in order. This package grants neither.

1. **S1-A (source and static review):** write the single file `scripts/luna65_phase2a_ledger_sizing.py` and perform nonexecuting static review (§4.9).
2. **S1-B (execution):** one execution, which needs the owner's acceptance of Decision A as an explicit statement and the S1 source SHA-256.

### 4.1 Identity
- Generator: `scripts/luna65_phase2a_ledger_sizing.py`, currently **absent**; its SHA-256 and Git blob ID are bound by S1-B. No hash is invented here.
- Schema: `luna65-phase2a-probe-v1`; fixture `l65-phase2a-v1`; the field table, canonical serialization and ordering of `LUNA_65_PHASE2_CAPACITY.md` (blob and SHA-256 of that file are bound by S1-A from the checkout).
- Interpreter: repository `.venv` Python 3.11.4 (launcher SHA-256 `B5442B36…F0CE`, base `4FB049EE…181F` per the published contract §3); record `sys.version`, `zlib.ZLIB_VERSION`, `zlib.ZLIB_RUNTIME_VERSION` and `gzip` module identity in the manifest.

### 4.2 Records generated
Exactly 8,196 synthetic records: counters `input`, `episode`, `lineage`, `output_event`, each probe 1–2,049, in the published order. Probes 1–2,048 expect `allocated`; 2,049 expects `capacity_rejected` with the exact published message for that counter. Values are closed-form functions of `(counter, probe_index)`.

- `allocated_identity` follows the published schema row exactly: for `input`, the emitted/provenance ID `l65-capacity-node:input:<ordinal>` (ordinal 0–2,047 for probes 1–2,048); for `episode` and `lineage`, the **integer** newly allocated counter value (not the external `l65-phase2a-episode-*` / `l65-phase2a-lineage-*` event-ID strings, which are admission inputs and are not `allocated_identity`); for `output_event`, the emitted excursion ID `l65-capacity-node:excursion:<global-output-ordinal>`; JSON null on the expected rejection (probe 2,049). Those external event-ID strings may appear only where the published schema already carries them. Checkpoint, snapshot, delta and exception fields are constructed per the published schema table; S1-A static review must compare every field against the published text and not against this summary.
- The generator must never import the TPCN package, call `neuron_to_ir2_e2`, create a neuron, allocate or read an actual E2 identity counter, or touch `.venv` packages beyond the standard library.

### 4.3 Exclusions
No Spiral or dataset input, no training, scoring or network, no subprocess, no environment read, no path other than the output directory, no `random` without a fixed seed, no clock in record content. `import` allowlist: `json`, `gzip`, `zlib`, `hashlib`, `sys`, `os` (path joining only), `time` (monotonic guard only), `io`, `pathlib`.

### 4.4 Determinism
No seed is needed: construction is closed-form. If any pseudo-random digit generation is used it uses a fixed arithmetic recurrence stated in the source, not `random`. To honor the 8,196-record ceiling as a **total** across the whole invocation, S1 generates exactly one profile, the width-bound (worst-case) profile, exactly once: 8,196 records in total, no second generation, no nominal profile and no double-generation check. Determinism is established instead by static review of the closed-form construction and by the SHA-256 of the single decompressed stream recorded in `sha256.json`. A nominal-profile sizing, if ever wanted, needs a separate authorization.

### 4.5 Compression
RFC 1952 gzip, level 9, `mtime=0`, no filename, via the standard-library `gzip` module on `zlib` as recorded. Sizes are measured with a counting sink. A `.gz` file is written only when its size does not exceed 786,432 bytes minus the finalization margin; otherwise only counts are written.

### 4.6 Command (proposal; not executed)
```powershell
.\.venv\Scripts\python.exe -B scripts\luna65_phase2a_ledger_sizing.py --output-dir "$env:LOCALAPPDATA\TPCN\evidence\luna65\phase2a-sizing\<run-id>"
```
Run from the Git top-level of the exact checkout, with `PYTHONHASHSEED=0` and no other override. `<run-id>` follows the capacity convention (UTC timestamp, hyphen, seven-character commit ID). The run directory is created new; an existing one means refuse. Arguments are an exact allowlist. The attended wrapper of Decision A recommendation 2 is the only addition.

### 4.7 Ceilings
- Invocations: exactly 1; retries 0; no second run after a classification other than a harness fault explicitly recorded as `GENERATOR_FAILURE`, and then only by a new authorization.
- Wall 30 s guard in process (checked every 256 records); outer attended timeout 45 s.
- CPU 30 s (in-process `time.process_time()` guard); the outer wrapper does not measure CPU.
- Memory: designed to hold one line and one running digest; no in-process memory guard is used (`ctypes` is not in the §4.3 allowlist). The 128 MiB figure is a design bound by construction, not a measured or enforced limit.
- Storage: total output ≤ 1,048,576 bytes; expected files `sizing.json`, `sha256.json` and conditionally the `.gz`; stdout one line of at most 1 KiB, stderr only the bounded failure line.

### 4.8 Output, manifest, success, failure and independent evidence
- Destination `%LOCALAPPDATA%\TPCN\evidence\luna65\phase2a-sizing\<run-id>\`, read-only after finalization, never committed.
- `sizing.json` (canonical): generator SHA-256, contract identities, versions, record count, uncompressed length, compressed length, bytes per record, margin to 786,432 minus the finalization margin, decompressed-stream SHA-256, wall and CPU observations from `time` (no memory measurement; the 128 MiB value is a declared by-construction bound only), classification.
- Classifications: `FITS_WORST` (worst-case profile fits; satisfies the sizing blocker for fit only if the Decision A amendment is accepted), `EXCEEDS_WORST`, `GENERATOR_FAILURE`. The published `FITS_NOMINAL_ONLY`/`EXCEEDS_BOTH` forms require the nominal profile and are not producible under this single-profile S1.
- Failure: any exception, count other than 8,196, index discontinuity, over-cap output, or elapsed over 30 s.
- Independent verification (a reviewer other than the executor, read-only): recompute the record count and sizes by decompressing the `.gz` if written; verify `sha256.json`; verify the generator source SHA-256 against the authorization; confirm nothing else exists in or beside the output directory; confirm the repository status is unchanged. The result stands only after that review.
- **Success** means a completed, verified classification. Only `FITS_WORST` removes the sizing blocker, and only if the owner has accepted the Decision A amendment (otherwise `FITS_WORST` is proposed-only and the published `FITS_WORST_AND_NOMINAL` condition stands); any other classification needs an owner-accepted path.

### 4.9 Risks added by running without the supervisor
No memory or CPU enforcement; no process-tree control; no token or integrity restriction; no no-breakaway guarantee; no controller-owned evidence writer or high-water accounting (the S1 script writes its own few bytes, bounded by construction rather than by an external accountant); the wall timeout is attended; any defect runs with the user's full rights. S1-A static review must therefore reject any file, process, network, environment or import beyond §4.3, and the only writes allowed are the two or three named files in the named directory.

## 5. Windows prerequisite U1–U8 feasibility matrix

Definitions are those published in contract §4.5. Categories: **S** source or documentation inspection; **H** read-only host configuration inspection; **R** runtime compatibility probe; **I** infrastructure configuration; **O** owner-policy decision. Nothing below is run here, and no account, ACL, token, privilege or firewall setting is changed.

| # | Prerequisite (published) | Categories | What is established now | Minimum evidence required later |
|---|---|---|---|---|
| U1 | `CreateProcessAsUser` with the restricted Low token and no `SeAssignPrimaryToken`/`SeIncreaseQuota` | S, R, O | Documentation suggests a restricted token derived from the caller's own primary token is assignable, but the documentation also names `SeIncreaseQuotaPrivilege`; the host lacks both. **Unverified**; not claimed | one probe that creates the restricted Low token from the invoking token and starts a fixed trivial child suspended; success or the exact Win32 error. If it fails with privilege-not-held: owner decision, no administrator path |
| U2 | exact interpreter chain under the Low token, UI restrictions, no console, correct imports | R | interpreter and launcher hashes known (read-only, §3) | the same probe family with `.venv\Scripts\python.exe -B -c <fixed no-op>` under the four-variable environment: exit code, no extra files created, imports resolved without `TEMP`/`PATH`, and the same with the intended pytest command only after the test file exists (then Phase 2A fixture authorization territory) |
| U3 | launcher passes the ledger handle to the child interpreter | R, O | undocumented in this package | probe: inherited pipe handle number visible and writable in the grandchild interpreter via the handle list; if not, owner decision on launching the base interpreter directly (which changes the published command and the interpreter identity) |
| U4 | Medium `NO_READ_UP`/`NO_WRITE_UP` labels deny a Low process `DUP_HANDLE`, `TERMINATE`, `VM_WRITE`, query | R | Medium is the default label of unlabelled objects and Mandatory Integrity Control is applied before the DACL (documentation); whether the default process label already blocks the write rights, and whether `NO_READ_UP` is present or needs adding, is **not established here** | with a probe-owned Medium target and a Low-token prober: attempt each named right and record the access-denied or granted result; a read-only query of the existing process label is an acceptable first step |
| U5 | enumerate Low-labelled writable locations | H, O | not enumerated; `LocalLow` and `AppDataLow` expected from documentation | read-only listing of Low-labelled directories and registry keys under the user profile and system paths (labels are readable without privilege as far as documented; unverified), then an owner decision to accept or request removal; no change made |
| U6 | set the mandatory-label ACE on `P`/`W`/evidence tree without `SeRelabelPrivilege` | S, R, O | documentation indicates a label at or below the caller's integrity needs no relabel privilege; whether it can be attached at process creation through the security descriptor is **unverified** | probe: create a directory and a child process with a Medium `NO_READ_UP|NO_WRITE_UP` label by the unprivileged user and read it back; failure means an owner decision on the process-protection claim, not an administrator action |
| U7 | network non-use by the workload | S, I, O | Low integrity does not block network access; AppContainer or firewall rules need system configuration | static review of the Phase 2A test for network imports and calls (S) plus an owner decision accepting non-enforcement, or an infrastructure change authorized separately. No technical network enforcement is claimed |
| U8 | same-user Medium processes can tamper with `P`, `W` and the evidence tree | O | accepted-limit item | covered by Decisions B and C; nothing further provable |

### 5.1 Proposed bounded probe authorizations (candidates only, none authorized)
A single probe source file would be needed, `scripts/luna65_phase2a_windows_probe.py` (absent; hash bound at authorization), run only by explicit owner authorization, never as part of qualification:

- **RP-1 read-only host inspection** (U4 query, U5): list labels and DACLs; no `SetSecurity*`, no `icacls /grant`, no registry write. Ceiling: 30 s wall, 5 MiB output outside the repository, one invocation, zero retries.
- **RP-2 token and launch compatibility** (U1, U2, U3): create the restricted Low token, create a probe-owned unnamed job, start `.venv\Scripts\python.exe -B -c "pass"`-class fixed children suspended, resume, read exit codes, close. Ceilings: 10 s wall; job memory 67,108,864 bytes; process limit 8; one invocation; zero retries; no repository write; output under the probe's own evidence directory only.
- **RP-3 label and denial** (U4, U6): create a probe-owned Medium-labelled target process and directory, attempt Low-token access, record results. No relabel privilege, no administrator, no change to any existing object.

Each probe is its own separately reviewed and separately authorized step, and none replaces Phase 2A qualification Q01–Q12. A probe result that contradicts the contract returns the contract for re-review rather than being waived.

## 6. Architecture limits preserved (no change)

B-min: the minimal watchdog launches the controller and retains only `PROCESS_TERMINATE | SYNCHRONIZE | PROCESS_QUERY_LIMITED_INFORMATION` on it; the controller owns the sole workload Job Object handle; no ETW observer. Preserved parameters: 120 s monitored aggregate CPU; 120 s monitored wall; 115 s early workload stop request; up to 15 s trusted observation (not execution permission); 50 ms heartbeat; 500 ms stale threshold; unconditional first-post-`T0+135 s` controller termination request; 268,435,456-byte job-commit charge limit (non-equivalent to aggregate private commit; owner-accepted); 1,048,576-byte logical retained-artifact high-water limit; zero retries. The watchdog deadlines are design parameters and **not** verified hard real-time guarantees. Accepted residual failure scenarios (hung `P` with dead or hung `W`, undetectable `W` hang, the admission-death race, failed termination, kill-on-close with no documented latency bound, Q03-C2) are unchanged.

## 7. Implementation-authorization candidate (identities to freeze)

| Item | State |
|---|---|
| Authoritative checkout commit | to be the commit that publishes this package; it cannot be named inside itself and is bound in the authorization text after publication |
| R7 contract | Git blob `0759087811610f40c73de91d8662c28d8ebce54d`; LF-normalized SHA-256 `6C5EBFD955EFDF472897B18E0126E83C85AFF56AE98BA5BE0D5D3564EF984671`; reviewed CRLF-checkout SHA-256 `9CA2E34D…9B73` |
| Supervisor source path | `scripts/luna65_phase2a_supervisor.py` only |
| Existing scaffold | untracked, `67542EDF…0AA1`; the implementation must start from a reviewed decision whether to replace it; it is not an input to publication |
| Phase 2A test file | **absent**; no SHA-256 is invented. Implementation remains blocked pending a separately reviewed binding procedure. Proposed procedure: the test file is created under a later Phase 2A fixture authorization; the supervisor then receives its expected path and SHA-256 and its own expected source SHA-256 as invocation arguments from the authorization text, records them, and refuses on mismatch |
| Profiles | watchdog, controller, workload exactly as in contract §4 |
| Source-change allowlist | one file, the supervisor |
| Permitted static validation | non-execution only: hash check, `git diff --check`, the §10.3 criteria of the contract; no `py_compile` execution of the supervisor, no import, no run |

If any prerequisite (S1 result, a probe, or an owner decision) changes the contract, the final implementation-authorization package requires another independent four-lane review.

## 8. Readiness dispositions (this package's own, pre-review)

| Area | Disposition |
|---|---|
| Owner-policy decisions A–D | ready for owner review |
| Synthetic sizing authorization | ready for owner review; S1-A not authorized, S1-B not authorized |
| Windows compatibility verification | probe authorizations specified; none authorized or run; U1–U8 remain unproven |
| Supervisor implementation authorization | **not ready**: sizing result, probes, the owner decisions, the test-file binding and the final package review are all outstanding |

## 9. Authorization state

**Supervisor implementation: NOT AUTHORIZED.**
**Synthetic sizing execution: NOT AUTHORIZED.**
**Supervisor qualification: NOT AUTHORIZED.**
**Phase 2A/2B fixtures: NOT AUTHORIZED.**
**Full Spiral benchmark: BLOCKED.**
**Luna-64 corrective execution: BLOCKED.**
**Luna-63C: FROZEN.**
