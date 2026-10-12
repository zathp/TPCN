# Luna-65 Phase 2A Supervisor Simplification Review R7

**Gate:** `L65-PHASE2A-SUPERVISOR-SIMPLIFICATION-R7`
**Role:** Luna-0, independent TPCN governance and Windows execution-containment reviewer
**Date:** 2026-10-12
**Status:** governance-only feasibility review; no implementation, static
validation, supervisor execution, qualification, fixture, benchmark or
scientific experiment is authorized or was performed.

This document does not replace or rewrite R1, R2 or R6, or their handoffs. The
original R6 verdict (**BLOCKED — R6 CORRECTIVE CONTRACT INCOMPLETE**) is
preserved unchanged.

## 1. Baseline and preserved evidence

- Branch `governance/luna64-r4.3-freeze-20261010`; HEAD and
  `origin/governance/luna64-r4.3-freeze-20261010`
  `1d6325f3ca738b32a6ee9e1a5613d2faa9458770`.
- Untracked supervisor scaffold `scripts/luna65_phase2a_supervisor.py`,
  SHA-256 `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`
  (verified; not modified, not imported, not executed, not published).
- R6 contract SHA-256
  `5747D1DD5A76C4D4C3BF5EC6FEB220AF268D05CE5FC0B6E24F84D443A487C152`
  and R6 handoff SHA-256
  `8D681CAFC5BE6F6E73F591934F8A73405F595A6DE745F0521C349E9FD625C3D2`
  (verified).
- The pre-existing uncommitted modification to
  `workflow/docs/luna/LUNA_WORKFLOW.md` and the unpublished R1/R2/R6 contracts
  and handoffs are preserved.

## 2. Owner-decision provenance

The authoritative policy statements are the owner's explicit decisions
supplied directly in the R7 task instruction (conversation evidence). They are
accepted for **Phase 2A qualification design only**:

| # | Decision |
|---|---|
| O1 | 120 s monitored aggregate job CPU (user + kernel). |
| O2 | 120 s monitored wall time. |
| O3 | Early termination request at 115 s. |
| O4 | Up to 15 s of post-budget trusted-controller **observation**; this is not workload execution permission. |
| O5 | Bounded cessation-observation intervals instead of exact physical exit timestamps. |
| O6 | 268,435,456-byte hard job-wide private-commit requirement. |
| O7 | 1,048,576-byte hard retained-artifact requirement. |
| O8 | Zero retries. |

R6 attributes its D9/D10 decisions to an owner attachment and records a
snapshot hash for it. That attachment's bytes are **not accessible to this
review**; a bounded (not exhaustive) search of the user profile's Downloads,
Documents, Copilot session-state and temporary locations found no file of the
recorded size that corresponds to it. The attachment hash is therefore neither
verified nor reproduced here. D9/D10 are consistent with O3–O5 as restated by
the owner in this task, and R7 relies only on the restated decisions O1–O8.
No decision here widens any limit, and the 256 MiB numerical ceiling is
unchanged.

## 3. Requirement basis

R7 evaluates the architectures against these requirements, each traced to an
owner decision or to a previously reviewed contract requirement:

| ID | Requirement | Source |
|---|---|---|
| R-CPU | Monitor aggregate job user+kernel CPU; terminate at the early-stop point; budget 120 s. | O1, O3 |
| R-WALL | Monitor wall time from controller `T0`; terminate request at `T0+115 s`; wall budget `T0+120 s`; observation cutoff `T0+135 s`. | O2–O4 |
| R-CESS | Record a bounded active→empty observation interval; otherwise cessation is unconfirmed. | O5 |
| R-MEM | Job-wide private commit ceiling of 268,435,456 bytes, hard. | O6 |
| R-ART | Retained artifacts ≤ 1,048,576 bytes, hard, no silent drop. | O7 |
| R-RETRY | No workload retry. | O8 |
| R-FAIL | Controller death must not leave workload processes running. | Prior reviewed containment contract (Q08) |
| R-TREE | Whole admitted process-tree containment. | Prior reviewed containment contract |

R-FAIL and R-TREE derive from the previously reviewed proposal contracts, not
from the owner decisions O1–O8. Whether the earlier **independent watchdog**
and **independent process observer** are mandatory *mechanisms* (as opposed to
the properties they were meant to secure) was never separately decided by the
owner; R7 treats the properties as required and the mechanisms as candidates.

## 4. Windows semantics relied upon

Statements are limited to documented behavior; items needing target-build
confirmation are marked and carried to qualification.

1. A Job Object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` terminates all
   associated processes when the **last handle** to the job is closed.
   Handles held by a process are closed by the OS when that process ends, for
   any reason. The job therefore survives a controller only if some *other*
   handle to it exists (duplicate, inherited copy, or named open).
2. An unnamed job cannot be opened by name. A process obtains a handle to it
   only by inheritance, by `DuplicateHandle`, or by being handed one.
   `DuplicateHandle` out of the controller requires `PROCESS_DUP_HANDLE` on the
   controller process; the workload's token and the controller's process
   security descriptor decide that access (design-controlled, qualification
   required).
3. With neither `JOB_OBJECT_LIMIT_BREAKAWAY_OK` nor
   `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK`, a member's request to create a
   child with `CREATE_BREAKAWAY_FROM_JOB` does not produce an outside-job
   child (documented as preventing breakaway; whether `CreateProcess` itself
   fails or the child stays in the job is target-build behavior to be
   recorded, not assumed), and ordinary descendants
   are placed in the job automatically. Creation-time
   `PROC_THREAD_ATTRIBUTE_JOB_LIST` places the new process in the named job at
   creation (supported Windows 10 / Server 2016 onward; unavailability is
   fail-closed).
4. `IsProcessInJob`, `JobObjectBasicAccountingInformation`
   (active/total process counts, user/kernel time) and
   `JobObjectBasicProcessIdList` describe membership of processes **associated
   with that job** only. They do not enumerate processes created outside it.
5. `JOB_OBJECT_LIMIT_JOB_MEMORY` limits the job-wide sum of committed memory;
   `PeakJobMemoryUsed` reports the job's peak. `JOB_OBJECT_LIMIT_JOB_TIME`
   with `JOB_OBJECT_TERMINATE_AT_END_OF_JOB` is an OS-enforced **user-mode**
   time limit only; no Job Object limit covers combined user+kernel CPU, and no
   Job Object limit covers wall time.
6. Job termination, kill-on-close and `TerminateJobObject` have no documented
   completion-latency bound. A process that cannot be terminated is an
   unresolved condition, not a recoverable one.
7. Process-creation events (ETW or any other system-wide observer) report that
   a process was created; they do not assign job membership, prevent creation,
   or (for brokered creation) identify the requesting member as the creator.

## 5. Candidate architectures

### A — Single trusted controller

One process `P` owns the sole job handle, suspended admission, resource
monitoring, stdout/stderr/ledger capture, the evidence writer, whole-job
termination and cessation observation.

| Property | Assessment |
|---|---|
| Controller crash before admission | No workload exists. OS-enforced: nothing to contain. |
| Controller crash after admission | The sole job handle closes with the process; kill-on-close terminates all members. **OS-enforced**, provided no second handle exists (§4.1–4.2) and the OS completes the kill (no latency bound; qualification). |
| Controller hang (alive, not progressing) | **Not covered.** No OS mechanism enforces wall time; only the OS user-mode job time limit (§4.5) bounds user CPU. Wall and combined-CPU budgets, evidence and early termination all stop. |
| Uncontained risks | Hang or livelock of `P`; same-user process holding `PROCESS_DUP_HANDLE` to `P`; Q03-C escapes (§6). |

A is the smallest design and has the strongest OS-enforced death behavior, but
has no mechanism for the hung-controller case.

### B — Controller plus minimal watchdog (recommended candidate, as refined: "B-min"; not owner-selected)

R7 recommends B-min; no architecture is selected until the owner records
D-R7-1. Sections 5 and 10 below are conditional on that decision.

R6's watchdog failed because it received **duplicated job handles**: that makes
kill-on-close depend on watchdog liveness (a hung watchdog holding the last
handle defeats it), and forced a bootstrap-job ownership-transfer protocol.
B-min removes the cause:

- The watchdog `W` **never holds a job handle** and never touches the workload.
  Its sole authority is `PROCESS_TERMINATE | SYNCHRONIZE` on `P`.
- `W` is the first process: it is the launcher and creates `P` itself, so it
  receives the exact `P` process handle from `CreateProcess`. No handle
  duplication into `W` is needed. `W` records `T0` (first-entry QPC, per the
  owner's `T0` definition) and passes it to `P`.
- `P` owns the sole job handle and everything in A. `W` converts a **hung**
  controller into a **dead** controller (`TerminateProcess(P)`), after which
  the OS-enforced kill-on-close of A applies. Cleanup of the workload is by the
  OS, not by watchdog authority.
- No ETW observer, bootstrap job, observer job, control/status pipes or
  ownership-transfer protocol exist.

Ownership before admission: `W` creates `P` and a pair of anonymous pipes
(`W→P` control/ack carrying `T0` and a run nonce; `P→W` heartbeat). Admission
protocol: (1) `P` sends heartbeat sequence 1 with the nonce; (2) `W` replies
with a nonce- and sequence-bound acknowledgment of that exact heartbeat;
(3) `P` validates the acknowledgment, checks `W`'s `SYNCHRONIZE` handle is
unsignaled immediately before creating the suspended root and again
immediately before resume, and only then resumes. Any timeout or mismatch
before resume terminates the exact suspended root handle and fails closed.
`P` also holds a `SYNCHRONIZE`-only handle to `W` (inherited through an
explicit handle list). The liveness check and admission cannot be made atomic:
`W` dying between the last check and workload start is a design-controlled race
that needs runtime qualification and an owner decision (D-R7-1); it is not a
guarantee.

Heartbeat: emitted **by `P`'s control loop** (not by an independent thread, so a
stuck loop cannot be masked), every ≤ 50 ms, carrying a sequence number and QPC.
`W` requests termination of `P` when no heartbeat arrives within 500 ms. All
blocking calls in `P` (file writes, pipe reads, termination) run on
single-flight worker threads and never in the control loop. These values are
design proposals for owner acknowledgement, not OS guarantees.

Final-evidence handoff: `P` must stop new observations and durably commit its
terminal record and manifest before a pre-cutoff point (proposal `T0+130 s`),
then send `W` a nonce-bound committed-status message (evidence delivery only).
`W` requests termination of `P` on its first control-loop execution at or after
`T0+135 s` if `P` is still alive, **unconditionally**: a committed status,
including one claiming job-empty cessation, never waives this action, because
`P` holds the sole job handle and only `P`'s exit triggers kill-on-close. A
well-behaved `P` exits immediately after its terminal commit; `W` records
whether a committed status was received and its content. This is a logical
observation cutoff, not a guaranteed physical kill time, and `W` records late
wake and request timestamps. If the cutoff wins before commit, uncommitted
evidence is incomplete. `W`
cannot detect its own hang, so the watchdog guarantee ends silently if `W`
hangs (see §9).

| Failure | Behavior |
|---|---|
| `W` fails before admission | `P` observes `W` exit, does not admit; if the job already exists it holds no members. |
| `P` fails before admission | No workload exists; `W` records failure and exits. |
| `P` crashes after admission | Sole job handle closes; OS kill-on-close terminates members (OS-enforced). `W` observes exit and reports. |
| `P` hangs after admission | `W` heartbeat timeout or the `T0+135 s` deadline terminates `P`; OS kill-on-close follows. Design-controlled + OS-enforced. |
| `W` crashes after admission | `P` observes it, requests whole-job termination, finalizes evidence as controller-failure; workload is not left running without supervision. |
| `W` hangs after admission | No effect on kill-on-close (it holds no job handle). `P` continues supervision; the hung-controller defense is lost for the rest of the run. Accepted only as part of the double-failure residual below. |
| `W` hung/dead **and** `P` hung | **Unresolved.** No independent enforcement mechanism exists beyond the OS user-time limit; recovery is not claimed. |
| `W` dead and `P` dead | OS kill-on-close from `P`'s death. Cessation unconfirmed; run fails closed. |

### C — Existing controller / watchdog / ETW design (R6)

R6 retains primary + watchdog (holding duplicated workload, observer and
bootstrap job handles) + optional ETW observer with a pipe-based start/status
protocol. Its indispensable-assurance claim reduces to one item: **system-wide
process-creation detection** that could reveal an outside-job process.
Everything else C provides is provided by A or B-min using fewer mechanisms,
and C adds the following defects not present in B-min:

- Handle duplication into the watchdog weakens kill-on-close (the unresolved
  R6 "hung watchdog holds the last handle" finding).
- Bootstrap, observer and workload job ownership transfers and observer pipes
  that R6 itself found incompletely specified.
- ETW privilege, session ownership and cleanup after controller loss are
  unqualified; observer death is itself a failure mode.

C is **not selected**. Whether detection of §6's Q03-C class is mandatory is an
owner decision (§6, D-R7-3); if it is mandatory, ETW (or an equivalent
observer) is **additive to B-min** under a separate design gate, not a
reason to retain C's job-handle protocol.

### Recommendation (not a selection)

**B-min** is the simplest architecture that retains (a) OS-enforced controller
death behavior, (b) hung-controller conversion to death, and (c) no ETW or
job-handle sharing. A is acceptable only if the owner accepts the hung-controller
residual (D-R7-1).

## 6. Q03 requirements analysis

Q03 (published qualification case `Q03 Breakaway request`) has three
requirement layers; they are separable and must not be conflated.

| Layer | Requirement | Mechanism | Disposition |
|---|---|---|---|
| Q03-A | A requested breakaway must not yield an outside-job child: if `CreateProcess` fails that is recorded evidence, and if it succeeds the identity-checked child must be in the intended job before it runs (API failure is not itself the pass criterion unless pinned to documented target-build behavior); ordinary descendants (Q02) stay in the job. | Job limit flags (no breakaway), `JOB_LIST` creation, read-back of effective flags, `IsProcessInJob`, `BasicProcessIdList` + accounting counts. | **OS-enforced** once flags are set and read back; verified by synthetic case. **No ETW needed.** |
| Q03-B | If an outside-job child nevertheless exists and its PID is self-reported by a cooperative synthetic worker while suspended at a barrier, terminate it through an identity-checked handle and prove cessation. | Controller opens the reported PID with terminate/synchronize/query rights, checks creation time and `IsProcessInJob`, terminates, waits. Requires only a process handle, no ETW. | **Runtime qualification required.** Reaching this path means Q03-A failed (the OS did not enforce the configured limit); the run is a `PROCESS_CONTAINMENT_FAILURE` and the suite stops. Access to the escaped child depends on the owner-approved token/ACL profile. |
| Q03-C1 | Detect and recover a **new process created outside the job** that is not self-reported: brokered creation (WMI, scheduler, COM/RPC services) or creation through a spoofed parent. | Job APIs cannot see these (§4.4). Prevention is by token/integrity/AppContainer restrictions (design-controlled). Detection of the creation event needs a system-wide process observer (ETW or equivalent). | **Unresolved; requires owner decision (D-R7-3).** An observer reports system-wide creation only; for brokered creation the creator is the broker, so attribution to the workload is not established (§4.7). It would be conservative anomaly detection with a false-positive policy on a shared host, not proof of absence. |
| Q03-C2 | Code execution or injection into a **pre-existing** process. | Process-creation observation yields no event for this. Only OS-enforced prevention (token/integrity/process ACL profile) or an injection-specific detector could address it. | **Outside any process-start observer's coverage. Unresolved; requires owner decision (D-R7-3):** exclude C2 from the claim, or require a separately specified prevention boundary or detector. An observer is not a remedy for C2. |

Properties that **genuinely require** an observer: only Q03-C detection. The
following do **not** require ETW: job membership, descendant inheritance,
breakaway denial, job-handle lifetime, controller-failure containment
(§5), cessation of job members, and Q03-B recovery of a cooperatively
reported child. An ETW-disabled run, as in B-min, **must not claim Q03-C or
whole-tree protection beyond verified Job Object members and the OS-enforced
denial profile**. Q03 is not waived: Q03-C remains a blocker until the owner
selects either (i) a narrowed assurance claim, or (ii) a separately
authorized observer design with explicit false-positive and loss policy.

## 7. Evidence capture through one controller-owned mechanism

- **Ownership.** `P` alone creates three unidirectional anonymous pipes:
  worker stdout (diagnostic), worker stderr (diagnostic) and a dedicated
  ledger channel (JSONL). `P` keeps all read ends non-inheritable. The worker
  receives only the write ends, via `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`
  (explicit list; `bInheritHandles = TRUE` is required by that API but only
  the listed handles are inherited), and stdin is the null device. The ledger
  handle value is passed on the worker argument vector, not the environment
  (the environment is a controller-constructed allowlist).
- **Child-side closure.** Immediately after `CreateProcess` returns, `P` closes
  its copies of every write end so that end-of-file occurs when all members
  holding them exit. End-of-file that does not arrive after the job is
  observed empty indicates a handle held outside the job (a leak), and is
  recorded as an evidence anomaly, not repaired.
- **Controller-side capture.** One reader thread per pipe feeds a bounded
  queue consumed by the single evidence-writer thread, which is the only
  writer of retained artifacts. The writer, readers and file I/O never run in
  the control loop, so none can block monitoring or termination.
- **Bounded buffers.** Each pipe has a fixed read buffer (proposal 64 KiB) and
  a fixed per-category byte quota. When a quota or the global cap would be
  exceeded the controller records `EVIDENCE_INCOMPLETE`, stops admitting data
  and requests whole-job termination. It never truncates, drops or
  overwrites a mandatory record silently.
- **Retained-artifact accounting.** All retained bytes (compressed ledger,
  stdout, stderr, manifests, hashes, invocation, resource and failure
  records, temporary files and trailers) count against the same 1,048,576-byte
  total and are counted before each write or rename. The ledger is compressed
  as a stream directly into its final path to avoid a temporary-copy overlap;
  the reserve for the compression trailer is held in advance. The R2
  reservation split (ledger 786,432; stdout and stderr 32,768 each;
  invocation and resource records 16,384 each; failure and hash manifests
  8,192 each; slack 147,456) totals exactly 1,048,576 and is retained as a
  proposal only.
- **Ledger completeness.** Each record carries schema version, run nonce, a
  contiguous record sequence and probe index. The controller rejects gaps,
  duplicates and out-of-order sequence, checks the final end-of-ledger record's
  count against the frozen expected count, and verifies the running hash.
  Missing, malformed, oversize or late records make the run
  `EVIDENCE_INCOMPLETE`. The controller can verify only what arrives; the
  frozen expected record count comes from the invocation profile, not from the
  worker.
- **No uncontrolled direct writes.** The worker is given no evidence path,
  file handle or writable evidence directory. Absence of a bypass depends on
  the owner-approved token/integrity/ACL profile for the workload and on a
  separate enumeration of alternate paths (reparse points, hard links,
  temporary and export paths). This is **design-controlled and runtime
  qualification required**, not pipe-capture-enforced. Worker writes outside
  the evidence tree are outside artifact accounting and are a filesystem
  confinement matter for the token profile.
- **Writer-stall policy.** Readers never block on the writer queue. On queue
  full, writer failure, quota exhaustion or a termination request, each reader
  atomically switches to bounded drain-and-discard (counting discarded bytes),
  so surviving workers cannot block on a full pipe and reader EOF is reported
  within a bounded timeout. Any discard or reader timeout is
  `EVIDENCE_INCOMPLETE`; mandatory records are never silently dropped.
- **Evidence failure.** A writer, flush, hash, rename or quota failure sets
  `EVIDENCE_INCOMPLETE`, requests whole-job termination, and the controller
  proceeds with termination and cessation observation independently of the
  writer. A durable failure record is not promised if storage itself fails;
  the absence of a committed final manifest is by definition a failed run.
  The watchdog is never a second evidence writer.
- **Sizing prerequisite (not assumed; an open gate, not a design defect).**
  Design readiness for owner decision does not depend on the sizing result; implementation authorization does. R7 does **not** assume 8,196 records
  fit. A guaranteed fit would require either an analytical raw upper bound
  at or below the ledger reservation (786,432 B / 8,196 ≈ 95 bytes per
  record, which a realistic JSONL record exceeds) or a measured result for
  worst-case entropy fields. A separately authorized synthetic sizing step
  must bind a frozen record schema and generator identity, size raw and
  compressed ledger, trailer, manifests, hashes, stdout and stderr maxima and
  failure reserve against the exact 1,048,576-byte total, and report
  per-category and high-water bytes, without importing the supervisor,
  fixture or TPCN modules. If complete evidence cannot fit, the matter returns
  to the owner; the cap is not raised and evidence is not dropped.

## 8. Memory-accounting disposition

Windows documents `JOB_OBJECT_LIMIT_JOB_MEMORY` as a limit on the job-wide sum
of **committed** memory that fails commits exceeding the limit, with
`PeakJobMemoryUsed` as the peak. It documents per-process `PrivateUsage` as the
process's private commit charge. Microsoft's documentation does not state that
the job's charge equals the sum of members' `PrivateUsage`, nor provide a
conservative ratio or additive overhead (for example for shared pagefile-backed
sections or page-table charges). It is therefore **not established** that the
job limit is equivalent to, or conservatively stronger than, the accepted
aggregate private-commit metric. It is, however, an **OS-enforced pre-commit
limit** whereas a sampled `PrivateUsage` sum is non-atomic detection that can
miss peaks.

**Disposition: C — neither equivalence nor conservative dominance is
established. Owner-policy decision required (D-R7-2).** The 268,435,456-byte
threshold is unchanged. Options: (1) explicitly amend the enforced metric to
the Job Object job-commit charge at the same threshold, retaining sampled
`PrivateUsage` as a labeled diagnostic; or (2) retain exact private commit and
separately authorize a mechanism with an authoritative conservative mapping.
Whichever is chosen, record the effective limit by read-back before resume,
`PeakJobMemoryUsed`, and allocation-failure outcomes separately; failed commit
is not proof the workload ceased.

## 9. Failure-state comparison

Class key: **OS** = OS-enforced; **DC** = design-controlled; **RQ** = runtime
qualification required; **UN** = unresolved; **OD** = owner decision
required.

| Condition | A | B-min (recommended) | C (R6) |
|---|---|---|---|
| Controller failure before admission | DC (no admission before completed startup protocol; RQ) | DC (same; RQ) | DC (RQ) |
| Controller crash after admission | OS (kill-on-close, RQ) | OS (kill-on-close, RQ) | **UN** if watchdog holds the last handle and is hung; else DC |
| Controller hang after admission | **UN/OD** (OS user-time limit only) | DC + OS (watchdog → terminate controller → kill-on-close; RQ) | DC (watchdog holds job handle; RQ) |
| Watchdog crash/exit | n/a | DC (controller detects the exit via its `SYNCHRONIZE` handle and fails closed; RQ) | DC/**UN** (job handles in the watchdog) |
| Watchdog hang (alive, not progressing) | n/a | **UN/OD**: undetectable by the controller; the hung-controller defense is silently lost, and a later controller hang is then not covered. Hung watchdog holds no job handle, so kill-on-close is unaffected. | **UN** (hung watchdog may hold the last job handle) |
| Watchdog dies concurrently with admission | n/a | **DC race, RQ; OD**: liveness check and admission cannot be made atomic (see §5 admission protocol). | **UN** |
| Simultaneous controller + watchdog failure | n/a | Both dead: OS. Controller hung + watchdog dead/hung: **UN** | **UN** (no independent mechanism identified) |
| Job handle duplication/leakage | DC (handle list, non-inheritable, token/ACL) + RQ | Same; watchdog never holds one | Increased: handles intentionally duplicated |
| Failed process assignment | DC: `JOB_LIST` atomic; creation or read-back failure → terminate exact root handle, no resume | Same | DC |
| Failed process termination | **UN** (no stronger primitive; record `TERMINATION_UNCONFIRMED`) | **UN**; escalation is controller exit then OS kill-on-close | **UN** |
| Evidence-writer failure | DC (fail closed, terminate; independent of writer) | DC | DC |
| Memory exhaustion | OS for the job limit; **OD** on metric (§8) | same | same |
| Wall/CPU budget violation | DC (10 ms sampling, 115 s termination); OS user-time limit partial backstop; combined CPU not OS-enforced | DC + `T0+135 s` watchdog deadline; same partial backstop | DC |
| Process escape (Q03-A) | OS (flags) + RQ | OS + RQ | OS + RQ |
| Process escape (Q03-C) | **UN/OD** | **UN/OD** | DC/RQ detection only, attribution unproven |
| Incomplete cessation evidence | DC (O5: unconfirmed) | DC | DC |

No claim of guaranteed recovery from simultaneous controller hang plus watchdog
loss is made for any candidate.

## 10. Minimum path to qualification (conditional: if the owner selects B-min under D-R7-1)

None of the following is authorized by R7.

### 10.1 Source-implementation obligations

1. A single source file with fixed internal modes `launcher/watchdog` and
   `controller`; no ETW, no observer, no bootstrap/observer job, no
   duplicated job handle, no named kernel objects.
2. Sole job handle in `P`: unnamed, non-inheritable, never duplicated;
   `KILL_ON_JOB_CLOSE`; no breakaway flags; `JOB_MEMORY` (per D-R7-2) at
   268,435,456; user-time limit as a partial backstop, with
   `JobObjectEndOfJobTimeInformation` explicitly set to
   `JOB_OBJECT_TERMINATE_AT_END_OF_JOB` and read back with the flag and
   `PerJobUserTimeLimit` (periodically checked, not a combined-CPU or wall bound)
   (D-R7-7); effective limits read back before resume.
3. Suspended workload creation with `JOB_LIST` and explicit handle list;
   `IsProcessInJob` verification and read-back before resume; any failure
   terminates the exact root handle without resume.
4. 10 ms job accounting sampling; accounting gap > 100 ms or failed query
   closes admission and requests whole-job termination; termination at
   `T0+115 s`; control loop never blocks on I/O.
5. Cessation interval, termination request timestamps, QPC frequency and
   unconfirmed classification exactly per O4/O5; observation ends at
   `T0+135 s`.
6. Controller-owned pipes, readers, bounded buffers, single writer, ledger
   contiguity and hash, byte accounting and failure behavior per §7.
7. Watchdog as launcher holding only the controller process handle;
   heartbeat from the control loop; nonce/sequence-bound startup acknowledgment;
   committed-status handoff (evidence delivery only; never waives the cutoff);
   terminate-controller on stale heartbeat or, unconditionally, at the
   first control-loop execution at or after `T0+135 s` if the controller is alive;
   no job handle, no evidence writing.
8. Explicit controller-built environment; restricted workload token profile
   per D-R7-4; no workload access to `P` or `W` beyond what the profile
   permits.
9. Fail-closed refusal on any unsupported API, build or configuration.
10. The scaffold's existing helpers may be reused only after static review;
    its absent post-budget cutoff and unbounded in-memory observation list are
    defects to be replaced.

### 10.2 Proposed permitted file allowlist

- **Implementation (future, if authorized):**
  `scripts/luna65_phase2a_supervisor.py` only.
- **Governance (this review):** this contract, its handoff, and the
  authoritative `LUNA_WORKFLOW.md` entry.
- **Not allowed under any R7-derived authorization:** TPCN production modules,
  fixtures, datasets, Luna-64/Luna-63C records, tests and workers. A synthetic
  qualification worker and sizing generator would need their own separately
  authorized allowlist and identity binding.

### 10.3 Remaining owner decisions

| ID | Decision |
|---|---|
| D-R7-1 | Select B-min (recommended) with explicit acceptance of its fault-model boundary (undetectable watchdog hang; watchdog death racing admission; controller hang plus lost watchdog), or A with explicit acceptance that a hung controller is not covered. |
| D-R7-2 | Memory metric: amend the enforced metric to job-commit charge at the same threshold, or authorize an authoritative conservative mapping (§8). |
| D-R7-3 | Q03-C1: narrow the claim to Job-verified membership plus the OS-enforced no-breakaway profile, or authorize a separate observer design gate with explicit false-positive and event-loss policy. Q03-C2: exclude from the claim, or require a separately specified prevention boundary or injection detector. |
| D-R7-4 | Freeze controller, watchdog and workload identity profiles (accounts, token type, restricting SIDs, integrity, privileges, process ACLs, evidence-tree ACL, interpreter/source identity). R7 does not invent them. |
| D-R7-5 | Authorize synthetic evidence sizing (schema and generator identity) and the owner path if complete evidence does not fit. |
| D-R7-6 | Acknowledge heartbeat parameters (50 ms period, 500 ms stale threshold) and the watchdog `T0+135 s` terminate-controller deadline. |
| D-R7-7 | Accept or decline the OS user-time limit as a partial backstop (it never kills before the combined 120 s CPU budget is exhausted, because combined CPU ≥ user CPU). |
| D-R7-8 | Define "retained artifact bytes" (final file sizes under the evidence tree, including temporary files while they exist). |

### 10.4 Static-review acceptance criteria (nonexecuting, future)

Exact-byte identity; single allowlisted file; no import of TPCN, fixture or
dataset code; no ETW and no `DuplicateHandle` of a job handle; job handle
creation parameters and non-inheritance; handle-list use; read-back before
resume; no blocking call in the control loop; every failure path terminates
or fails closed; deadline arithmetic matches O1–O5; per-category and global
byte accounting precede writes; no truncation path; heartbeat emitted from
the control loop; no network, no retry; owner decisions D-R7-1…8 reflected.

### 10.5 Synthetic qualification requirements (future, separately authorized)

On the pinned Windows build: Q01 suspended admission; Q02 child and
grandchild; Q03-A breakaway denial; Q03-B cooperative outside-child recovery
(only if Q03-A fails); Q04 nested-job behavior; Q05 user-time limit and
sampling gap semantics; Q06 job-memory limit behavior and metric
reconciliation; Q07 wall termination and the 15 s observation; Q08
controller crash, controller hang and watchdog crash/hang using B-min
(including the kill-on-close timing and the hung-watchdog case); Q09 handle
leakage and workload access to `P`/`W`; Q10 evidence sizing, quota, writer
failure and ledger gaps. Each case needs its own resource budget; none is
authorized.

### 10.6 Outstanding containment risks

Hung controller with dead or hung watchdog (UN); Q03-C escapes (UN/OD);
termination of an unkillable process (UN); no latency bound on kill-on-close
or `TerminateJobObject`; metric non-equivalence (OD); evidence-bypass paths
depend on the unfrozen token/ACL profile (DC/RQ); same-user processes with
`PROCESS_DUP_HANDLE` on the controller; nested-job and target-build behavior
(RQ); sampling-based CPU monitoring and combined CPU not OS-enforced.

## 11. Authorization state

**Supervisor implementation: NOT AUTHORIZED.**
**Supervisor qualification: NOT AUTHORIZED.**
**Phase 2A/2B fixtures: NOT AUTHORIZED.**
**Full Spiral execution: BLOCKED.**
**Luna-64 corrective execution: BLOCKED.**
**Luna-63C: FROZEN.**
