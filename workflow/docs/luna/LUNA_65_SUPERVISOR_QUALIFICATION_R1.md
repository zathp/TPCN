# Luna-65 Phase 2 Windows Job Object Supervisor Qualification — R1

**Gate identity:** `L65-PHASE2-WINDOWS-SUPERVISOR-QUALIFICATION-R1`

**Status:** **BLOCKED — SUPERVISOR QUALIFICATION CONTRACT INCOMPLETE.** This
is a governance-only decision package. It contains no implementation
authorization and no qualification, fixture, benchmark, or resource-probe
execution authorization. The owner accepted the capacity-only replacement
protocol for qualification design; no Phase 2A/2B execution is authorized.

**Required resource profile to be protected:** 120 seconds aggregate
user-plus-kernel job CPU; 268,435,456 bytes aggregate concurrent private
commit charge; 120 seconds invocation wall time; 1,048,576 bytes combined
retained artifacts; zero retries.

The Windows Job Object API exposes job-wide user-plus-kernel accounting but
does not expose a hard cumulative user-plus-kernel CPU limit. Its hard
per-job time limit applies to user-mode CPU only and is checked periodically.
The wall-time controller also has no documented finite upper bound from
termination request to last process exit. In addition, the Job Object memory
limit is defined as aggregate job committed virtual memory, and the
equivalence to the Phase 2 contract's exact private-commit metric has not
been qualified. The compressed evidence ledger and workload-to-evidence
writer boundary also remain unqualified. These are explicit blockers, not
substitutions or silent relaxations.

## 1. Authority, baseline, and scope

### 1.1 Verified repository baseline

| Item | Verified identity |
|---|---|
| Branch | `governance/luna64-r4.3-freeze-20261010` |
| HEAD | `61b034931f00095549c278c249e9379dd27e8893` |
| Worktree | Clean before this governance task |
| Phase 2 capacity contract SHA-256 | `e3462e0d8d64b2373ce3adba514509c7fe3a5846e245778778a8f050c8028b1b` |
| Phase 2A correction handoff SHA-256 | `459e4ac9cac322a88bf580f2f1016082fef7e7c9a69369c0322ba7305181e684` |
| Luna-65 Spiral resumption contract SHA-256 | `1f1d4dd96e21ee760d32cdde4f0415576c9bae6af01b82db2a9c4e1d9fb5c777` |
| Phase 1 closure handoff SHA-256 | `4b4d7bf378c3c38ffc755106ece597a6fbeea9ec712cfb5aff105989e680e022` |

The baseline contract's four counter fixtures and the 8,196-probe
Phase 2A maximum, and the 136-call/139,264-event/2,176-input Phase 2B maximum,
are accepted for **qualification design only** by the owner instruction
dated 2026-10-12 and recorded in
[`LUNA_65_PHASE2_CAPACITY.md`](LUNA_65_PHASE2_CAPACITY.md). The accepted
replacement is capacity-only; it changes no Spiral scientific condition,
protocol, data, training, metric, or acceptance criterion.

### 1.2 Gate boundaries

This document defines design and decision prerequisites for a future
supervisor qualification. It does not authorize:

- installing or modifying infrastructure, creating an AppContainer profile,
  changing account/volume policy, or implementing the supervisor;
- implementing or running `tests/test_luna65_capacity_direct.py` or
  `tests/test_luna65_capacity_network.py`;
- any capacity probe, supervisor qualification case, test, benchmark,
  dataset generation, training, evaluation, or scoring;
- Phase 2A, Phase 2B, Spiral, or Simon Says execution;
- Luna-64 corrective execution or changes to frozen Luna-63C evidence.

The current checkout contains governance and resource-policy records but no
identified Windows Job Object supervisor implementation. The Phase 2A and
Phase 2B fixture modules are not materialized. The Phase 1 supervisor
observations are not qualification evidence. Luna-64 R4.3 supervisor
qualification is blocked and is neither imported nor reinterpreted here.

The environment was read-only identified as Windows 10 Pro, 22H2, build
19045.6466. This identifies the design target only; no Windows Job Object
operation or qualification probe was run.

### 1.3 Preserved governance and evidence

- Luna-12G remains the historical `TANH_LEGACY` benchmark result.
- Full-replication E2 capacity is unproven; full Spiral remains **BLOCKED**.
- Simon Says remains **SOURCE RECOVERY ONLY**.
- Luna-64 corrective execution remains **BLOCKED**.
- Luna-63C certification remains **FROZEN**.
- No ACP or architecture-contract change is proposed; this is an execution
  control and evidence-boundary design, not a neural architecture change.

## 2. Trusted supervisor boundary

### 2.1 Proposed components

| Component | Trust and responsibility |
|---|---|
| Primary controller | Trusted, pinned executable and configuration. Validates the reviewed run manifest, creates/configures the Job Object, launches only the exact approved profile, measures monotonic wall time, drains pipes, requests whole-job termination, waits for cessation, and finalizes evidence. |
| Independent watchdog | Trusted, separate process outside the workload Job Object. Receives a restricted job handle and controller process handle, monitors a heartbeat/deadline, and calls `TerminateJobObject` if the controller exits or stops making progress. It does not run tests or write workload inputs. |
| Workload | Untrusted fixture process plus all descendants. Runs under a restricted standard-user/AppContainer identity if qualification confirms Python and the pinned repository are usable with only the required read access. It receives no Job Object handle and no evidence-directory write permission. |
| Evidence writer | Trusted controller-side writer, outside the workload Job Object. Accounts every byte before retention, writes only to the unique external evidence directory, closes and hashes retained files, and records incomplete outcomes. |
| Independent observer | Read-only observer used during qualification to cross-check Job Object membership, process IDs, process start/exit, accounting, and termination stages. It is not a replacement for Job Object enforcement. |

This split is a proposed design, not existing infrastructure. Qualification
must record controller, watchdog, observer, Python, pytest, fixture, and
source identities by absolute path, version, and SHA-256.

### 2.2 Fail-closed admission sequence

1. Verify the clean reviewed source revision; exact Python executable,
   fixture/test hash, pytest identity, working directory, argument vector,
   environment allowlist, output destination, and signed/immutable supervisor
   profile. Reject changed or missing inputs before process creation.
2. Create a fresh, non-named Job Object with a restrictive security
   descriptor and non-inheritable handle. Configure all selected limits and
   `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; do not set
   `JOB_OBJECT_LIMIT_BREAKAWAY_OK` or
   `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK`.
3. Read back every configured limit and record both requested and effective
   values. If a required setting, query, handle, ACL, watchdog, pipe, evidence
   reservation, or policy check fails, do not create or resume the workload.
4. Create the exact child with `CreateProcessW` using
   `CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT |
   EXTENDED_STARTUPINFO_PRESENT`. Supply only an explicit inherited-handle
   allowlist for the required standard streams and any separately approved
   evidence channel. The Job Object handle is never in that list.
5. Assign the still-suspended process with `AssignProcessToJobObject`.
   Confirm membership with `IsProcessInJob` and a Job Object process-list
   query. Resume the initial thread only after assignment and all read-back
   checks pass. On any failure, terminate the suspended process and close
   handles without resuming it.
6. Start `T0` at the supervisor's main-entry timestamp, before manifest
   validation and Job Object setup; include all controller preflight,
   process creation, assignment, workload, termination, process reaping,
   pipe EOF, evidence flush/close, and integrity-manifest finalization.
   Controller executable startup before its first user-mode instruction is
   not directly measurable by this process and must be recorded separately
   by any invoking shell/host.

The controller must fail closed if already subject to an incompatible parent
job, if nested-job assignment fails, or if the effective outer-job
restrictions cannot be queried and reconciled. Windows 8 and later support
nested jobs, but parent-job restrictions compose and can still prevent
assignment or impose stricter limits. No breakaway is permitted. Child and
grandchild association is inherited by the Job Object unless breakaway is
explicitly enabled; the design enables neither breakaway mode.

### 2.3 Child creation and process-tree proof

The exact `CreateProcessW` flags omit `CREATE_BREAKAWAY_FROM_JOB`. A
qualification worker may attempt that flag, but the required observation is
that no successful descendant executes outside the assigned job: creation
must fail or the resulting child must be independently proven to remain in
the job. A `True` return from ordinary parent-PID enumeration is not
containment evidence.

Qualification cross-checks:

- the worker reports each known direct-child and grandchild PID over a
  supervisor-controlled channel and holds those processes at a test barrier;
- `IsProcessInJob` checks every reported live process against the exact job
  while it is held at the barrier;
- the PID-list cardinality from
  `QueryInformationJobObject(JobObjectBasicProcessIdList)` is compared with
  `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.ActiveProcesses` while the known
  processes are held, then both are checked empty after job completion;
- a separate process observer records starts/exits, detects event loss, and
  reconciles the known process lifecycle after the barrier is released. The
  observer technology, event-loss signal, and polling interval must be frozen
  in the qualification manifest before implementation.
- rapid exit, concurrent spawn/termination, nested-job rejection, and
  controller/job-handle closure are classified separately.

PID lists and event tracing are verification instruments, not enforcement.
If an independent observer cannot detect the deliberately attempted
breakaway or reconcile the final zero-active-process state, the case fails.
System shutdown or kernel failure may terminate processes without allowing
the controller to flush evidence; such a loss is an incomplete run, not a
successful cleanup.

## 3. CPU accounting and limit mismatch

### 3.1 Documented Windows semantics

On the verified Windows 10 target, the documented Job Object interface
provides:

- `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.TotalUserTime` and
  `TotalKernelTime`, each aggregating active and terminated job processes.
  They are represented in 100-nanosecond ticks; that unit does **not** prove
  100-nanosecond update or enforcement granularity.
- `JOBOBJECT_BASIC_LIMIT_INFORMATION.PerJobUserTimeLimit` with
  `JOB_OBJECT_LIMIT_JOB_TIME`, which limits the sum of **user-mode** execution
  time for job processes. Windows periodically checks the total and performs
  the configured end-of-job action. Kernel-mode time is not included.
- `JOB_OBJECT_LIMIT_PROCESS_TIME`, which is a per-process user-mode limit,
  not a job-wide aggregate limit.
- `JOBOBJECT_CPU_RATE_CONTROL_INFORMATION`, which is a processor-rate
  scheduling control. It is not a cumulative lifetime CPU budget.
- `JOBOBJECT_NOTIFICATION_LIMIT_INFORMATION` notifications, which do not
  terminate or constrain processes by themselves.

Therefore the sum `TotalUserTime + TotalKernelTime` can be observed and
reported for the entire job, including terminated descendants, but no
documented Job Object hard-limit field enforces that combined sum at
120 seconds. A sampled controller can call `TerminateJobObject` after
observing a crossing, but the sample interval, scheduling delay, accounting
update, controller failure, and termination latency permit overshoot and do
not constitute a hard 120-second combined-CPU cap.

### 3.2 Required accounting record

For every qualification case, record:

- requested and read-back Job Object limits and flags;
- `TotalUserTime`, `TotalKernelTime`, their sum, and each raw tick value;
- the QPC timestamp for each accounting sample in the live measurement
  stream; retain the sample count, configured cadence, maximum observed gap
  and its endpoint timestamps, threshold-bracketing samples, and final sample
  in bounded evidence. Do not retain an unbounded full sample stream; if a
  full trace is retained, its bytes count against the artifact ceiling;
- observed counter increments for each process lifecycle, including exited
  child/grandchild processes;
- sample interval, highest observed query gap, counter regression or
  discontinuity, CPU-limit notification time (if used), termination request,
  and last-process-exit time;
- controller/watchdog CPU separately; only processes assigned to the
  workload job count toward the job metric.

The 100-nanosecond representation is not a claim about actual accounting
granularity. Determine the practical reporting/update resolution by a
separately authorized synthetic qualification; no fixed kernel polling
period or strict overshoot is documented by the cited API pages.

### 3.3 Unresolved owner decision

The frozen Phase 2A resource term is **120 seconds aggregate user-plus-kernel
job CPU**. Job Objects alone cannot provide the required hard enforcement.
Before execution, the owner must choose one of these non-silent resolutions:

1. Keep the combined 120-second hard ceiling and authorize evaluation of a
   separately identified enforcement mechanism that demonstrably enforces
   cumulative user-plus-kernel CPU for the complete process tree; or
2. Explicitly amend the resource contract to a documented Job Object
   user-mode CPU limit and state that kernel CPU is separately observed but
   not hard-capped; or
3. Explicitly accept a sampled combined-accounting watchdog with a declared
   sample period and measured overshoot, acknowledging that this is not a
   hard 120-second cap.

Options 2 and 3 change the accepted resource guarantee and require explicit
owner approval plus contract revision. None is selected here. CPU-rate
limiting or a per-process user-time limit must not be represented as
equivalent.

**Disposition:** The current combined CPU requirement is a hard blocker for
claiming a qualified Windows Job Object supervisor.

## 4. Aggregate memory enforcement

### 4.1 Candidate native limit

`JOBOBJECT_EXTENDED_LIMIT_INFORMATION.JobMemoryLimit`, enabled by
`JOB_OBJECT_LIMIT_JOB_MEMORY` in `BasicLimitInformation.LimitFlags`, is the
candidate job-wide enforcement setting. Its documented quantity is virtual
memory that can be committed for the job, in bytes. It is distinct from:

- `JOB_OBJECT_LIMIT_PROCESS_MEMORY` / `ProcessMemoryLimit`, which constrain
  each process independently;
- working-set bounds, which concern resident pages and do not equal commit;
- lifetime allocation totals, which are not a concurrent live-memory metric;
- process working-set peaks.

The proposed configured value is exactly **268,435,456 bytes**. The design
must not set a per-process memory limit as a substitute. On reaching the
job-wide commit ceiling, the expected behavior to qualify is commit denial
(for example, a failed commit request); this is not presumed to terminate
the job or emit a guaranteed notification. The worker must handle allocation
failure and report it through the trusted evidence channel. If it cannot,
the supervisor terminates the job and records the observed status without
calling it a successful limit test.

`PeakJobMemoryUsed` and job memory accounting are evidence sources; a
notification limit alone is not enforcement. Qualification must also sample
the live processes' private commit (`PROCESS_MEMORY_COUNTERS_EX.PrivateUsage`)
and compare the concurrent sum against the job-accounted current/peak values.
The exact relationship between that measured sum and the Job Object's
committed-virtual-memory limit must be demonstrated on this OS build before
calling it the accepted **aggregate concurrent private commit charge**.
Differences, query gaps, and process-exit accounting effects are retained
explicitly. The metric is not working-set sum and is not whole-machine
memory.

### 4.2 Memory failure classification

| Observation | Classification |
|---|---|
| Job-wide `JOB_OBJECT_LIMIT_JOB_MEMORY` is read back as configured, the aggregate job commit is prevented from exceeding the ceiling, and independent live private-commit evidence reconciles | Candidate enforcement pass, subject to independent review |
| Only a process limit, working-set limit, or notification is active | Wrong control; fail |
| Commit failure occurs below the expected aggregate threshold and cannot be attributed | Inconclusive; fail closed |
| Commit exceeds the configured Job Object ceiling or a process escapes accounting | Enforcement failure; terminate the entire job |
| Worker allocation failure cannot be recorded or process cessation cannot be confirmed | Incomplete; no pass |

No memory limit has been configured or probed in this task.

## 5. Wall-time enforcement and termination

Use `QueryPerformanceCounter` / `QueryPerformanceFrequency` for elapsed
monotonic time, not wall-clock time. Use the supervisor-main-entry `T0`
defined in §2.2. At `T0 + 120 seconds`, the controller requests whole-job
termination with `TerminateJobObject` (or closes the final kill-on-close
handle as a fail-closed fallback). Record distinct timestamps for:

1. deadline reached;
2. termination requested;
3. `TerminateJobObject` return value/time (request API result, not proof all
   processes exited);
4. job signaled / active-process count reaches zero;
5. last child/grandchild process exit confirmed;
6. pipe EOF and evidence flush/close;
7. final evidence hash and supervisor completion.

The measured invocation includes controller preflight, process creation and
assignment, and ends only after process cessation and evidence finalization.
Controller executable startup before its first user-mode instruction is
outside this process's clock and must be recorded separately by the invoking
host. A controller cannot claim that process cessation occurs exactly at 120
seconds: the API provides no documented finite maximum from request to last
process exit.

An initial **15-second termination-grace candidate** is proposed only for
qualification planning: a test requesting termination at 120 seconds records
whether all workload processes cease by `T0 + 135 seconds`. This is an
observed acceptance target, not a proven Windows bound, and changes the
effective elapsed-time envelope. The existing 120-second term is not silently
amended. Owner approval is required before treating a 15-second grace as
acceptable. Any last-process exit later than the approved deadline, failed
wait, or unconfirmed descendant is a failed/incomplete run, not success.

The watchdog must terminate the job if the primary controller exits or
misses the declared heartbeat. If both controller and watchdog are hung or
the OS is unavailable, no finite process-cessation guarantee is claimed.
Termination latency is empirical per qualification conditions; it is not an
analytical upper bound for arbitrary Windows scheduling or system failure.

## 6. Controller failure, handle safety, and output draining

- The unnamed Job Object is created with a restrictive security descriptor;
  the workload is never given a job handle, process-duplication access to
  either controller, or an inheritable handle to the watchdog.
- `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` is set. The primary controller and
  watchdog hold only the intentional private references needed for
  independent termination; each process has a shutdown path that calls
  `TerminateJobObject`. If both trusted processes exit and the last job
  handle closes, Windows' kill-on-close action is the final fallback.
- Do not claim kill-on-close works if an untrusted descendant can retain or
  duplicate a job handle. Qualification must verify the explicit inherited
  handle list, process security, and inability of the restricted workload
  identity to open/duplicate controller handles.
- Monitor heartbeats, controller process exit, watchdog exit, and I/O-reader
  health. Failure to start either trusted monitor blocks workload admission.
  Loss of a pipe reader causes immediate termination; never leave a writer
  blocked while the controller waits for process exit.
- A successful `TerminateJobObject` return is recorded as a request/API
  result only. Confirm process cessation from the signaled job and observed
  zero active members; record individual process exits when available.
- On controller failure, an independent watchdog attempts termination and
  writes a bounded `controller_lost` failure record. If both fail, last-handle
  closure can terminate the workload but cannot guarantee evidence flush.
  System shutdown, kernel failure, power loss, and disk failure cannot be
  promised to preserve a final manifest.

The proposed restricted workload is an AppContainer/low-privilege standard
user with read-only access to the pinned repository and Python environment,
no network capability, no Job Object handle, and no write permission to the
external evidence directory. AppContainer compatibility, inherited standard
handles, pytest behavior, and access-denial behavior are untested. Do not
weaken restrictions or add writable paths to make a case pass without owner
approval.

## 7. Retained-artifact enforcement and evidence channel

### 7.1 Scope and byte accounting

The 1,048,576-byte retained-artifact ceiling includes every file retained in
the run directory or kept as a temporary/partial artifact after termination:
compressed JSONL, invocation manifest, resource observations, bounded
stdout/stderr, failure record, SHA-256 manifest, and any staging copy.
Temporary and final copies count simultaneously while both exist. No
uncompressed JSONL copy is retained. No scratch file may remain outside the
declared evidence directory at completion.

Record separately:

- bytes emitted by the workload when independently observable;
- bytes read from each pipe by the controller;
- bytes retained to each file;
- bytes drained and discarded after a retention quota is reached;
- compressed and decompressed JSONL byte counts;
- peak simultaneous retained/staging bytes and final logical file sizes.

The Phase 1 1,114,112-byte pipe observation is not a strict emitted-byte
bound. The child may emit more than the controller reads before termination;
this design makes no strict emitted-byte claim.

### 7.2 Controller-owned retention quotas

The following is a proposed per-file maximum allocation within the unchanged
1 MiB aggregate ceiling:

| Retained object | Maximum bytes |
|---|---:|
| `results.jsonl.gz` | 786,432 |
| `stdout.txt` | 32,768 |
| `stderr.txt` | 32,768 |
| `manifest.json` | 16,384 |
| `resource.json` | 16,384 |
| `failure.json` | 8,192 |
| `sha256.json` | 8,192 |
| Reserved aggregate slack | 147,456 |
| **Total** | **1,048,576** |

The controller reserves the fixed metadata and failure-record space before
admission. It writes each retained byte only after checking the remaining
per-file and combined quota. If a quota would be exceeded, it records the
first cause, requests job termination, drains/discards bounded pipe data to
avoid deadlock, preserves only complete records, closes a partial gzip stream
only if it can be explicitly labelled incomplete, and never emits a
success-shaped manifest. If a failure/hash record cannot be retained, the
absence and reason must be captured in all remaining evidence and reported
as incomplete. File rename is same-directory and no second full copy is
created.

These quotas bound files the trusted controller chooses to retain. They do
not by themselves constrain arbitrary workload file writes or every
filesystem temporary allocation.

### 7.3 Unresolved workload-write boundary

The Phase 2A contract requires a named external evidence directory and a
compressed JSONL result, but the test's path from in-process probe records
to a trusted controller-owned writer is not yet specified. Giving the
workload ordinary write access to that directory would let it bypass the
controller's retained-byte checks. Windows Job Objects provide no
per-job filesystem quota.

Two options require explicit owner/design review before fixture
implementation:

1. Add a bounded supervisor-mediated evidence channel and keep all evidence
   files controller-owned; this requires a reviewed Phase 2A writer/interface
   addendum and must preserve the exact authorized command; or
2. Provide an independently qualified per-run storage quota/volume that
   constrains every writable workload path and counts simultaneous temporary
   copies, including sparse-file logical sizes.

Until one option is selected and shown to fail closed, arbitrary child
writes outside the controller's retained set are a residual exposure and
the retained-artifact ceiling is not an execution-ready end-to-end bound.
No filesystem quota, sandbox, volume, or evidence channel was created here.

## 8. Analytical compressed-ledger sizing

The frozen Phase 2A schema has 8,196 records: 6,147 input/episode/lineage
attempts and 2,049 output-event attempts. Output-event success records
contain both immediate-emission and post-rearm checkpoints; the other
scenarios have smaller checkpoint payloads. The canonical records repeat
long field names, counter snapshots, and enum values, while timestamps,
floating-point state, and identity strings vary.

The following are **schema-based planning estimates only**, not measurements
and not a generated fixture ledger:

| Estimate | Per-record planning size | Raw JSONL total |
|---|---:|---:|
| Compact structural floor (not a valid all-scenario ledger) | 500 bytes | 4,098,000 bytes (3.91 MiB) |
| Likely mixed average: 850 bytes for 6,147 simpler records and 1,400 bytes for 2,049 output records | weighted 987.5 bytes | 8,093,550 bytes (about 7.72 MiB) |
| Conservative planning envelope: 2,048 bytes for every record | 2,048 bytes | 16,777,216 bytes (16 MiB) |

The floor and planning envelope are not formal byte bounds:
the published schema does not freeze every nested checkpoint key/value
projection or a maximum encoded record length. Before any sizing run, the
schema must be made byte-bounded without dropping fields.

Gzip framing and DEFLATE block overhead add bytes; they do not guarantee a
useful compression ratio. For a no-savings planning
case, the compressed payload remains near the raw size plus framing/block
overhead, well above the 786,432-byte JSONL allocation and 1 MiB total cap.
Repeated JSON keys make material compression plausible, but no ratio can be
assumed or claimed from the schema alone. An illustrative 6:1 compression
ratio yields about 1.29 MiB before metadata; 10:1 yields about 0.77 MiB
before metadata. Both ratios are assumptions, not evidence. Given only the
frozen schema, compatibility with the 768 KiB ledger allocation and total
artifact ceiling is **not established**.

The permitted next measurement is case Q10 below: a separate, owner-
authorized synthetic schema-shape evidence-sizing qualification. The frozen
schema does not yet provide complete deterministic record-shape values,
timestamps, or every nested checkpoint projection needed to instantiate that
ledger. A schema/writer addendum must freeze these input shapes and identities
before Q10 can run. It must not
instantiate `MultiExcursionNeuron`, call the Phase 2A fixture, use benchmark
data, or produce task examples. It must report raw bytes, gzip bytes, exact
Python/zlib versions, record-shape input digest, and simultaneous temporary
storage. If the complete synthetic ledger exceeds the allocation, stop and
seek either a lossless representation/schema review or an explicit owner-
approved increase in retained-artifact ceiling. Never truncate or omit
required record fields.

## 9. Exact Phase 2A command profile

The future fixture invocation remains exactly:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -x tests/test_luna65_capacity_direct.py
```

Expected working directory:
`C:\Users\Patrick\Documents\ActiveCode\TPCN`.

The Phase 2A contract specifies two environment overrides only:
`PYTHONHASHSEED=0` and `TPCN_LUNA65_EVIDENCE_DIR`, which must resolve to the
unique external run directory under
`%LOCALAPPDATA%\TPCN\evidence\luna65\phase2a\`. The complete workload
environment is not yet frozen: the contract does not enumerate every
inherited key/value or explicitly require removal of all unlisted inherited
variables. Before implementation, an addendum must freeze the exact
inheritance/allowlist policy while preserving both specified overrides, this
evidence path, and the approved restricted-user access model.

Before admission, the trusted controller verifies the absolute resolved
Python executable and SHA-256, current Git revision and clean tree, fixture
file path/hash, pytest package identity, exact argument vector, working
directory, allowlisted environment, run-ID/output path, and exact external
evidence destination. The invocation may use only the approved no-network
profile. The supervisor does not accept arbitrary command strings, shell
syntax, user-selected modules, or alternate scripts. A mismatch is rejected
before process creation and logged without attempting the workload.

The command profile is a design requirement only. The test file does not
exist in the verified checkout, the supervisor does not exist, and no
invocation was attempted.

## 10. Qualification case matrix

All cases are supervisor-only and use deterministic synthetic workers, not
the E2 capacity fixture or benchmark data. Each case runs once; retries and
replacement cases are zero. Limits below are proposed qualification-lane
ceilings, separate from the Phase 2A allowance. The **job memory ceiling**
for cases other than Q06 is 67,108,864 bytes; Q06 uses 268,435,456 bytes.
The per-case artifact bound is 1,048,576 bytes combined, with the retained
file allocations in §7.2. The job CPU ceilings are observed aggregate
user-plus-kernel budgets; Windows Job Objects alone cannot hard-enforce the
qualification aggregate either.

| Case | Synthetic input and expected observation | Failure classification | Max job CPU | Max wall | Max job memory | Max retained artifacts |
|---|---|---|---:|---:|---:|---:|
| Q01 Suspended admission | Start a synthetic no-op suspended; verify no user code runs before assignment/read-back; resume once after `IsProcessInJob` is true. | Pre-resume execution, wrong membership, or limit mismatch: admission failure. | 1 s | 10 s | 64 MiB | 1 MiB |
| Q02 Child and grandchild | Worker starts one child and one grandchild; all three report IDs and remain in the same Job Object through orderly exit. | Any live PID outside the job or unreconciled process count: containment failure. | 1 s | 10 s | 64 MiB | 1 MiB |
| Q03 Breakaway request | Worker attempts `CREATE_BREAKAWAY_FROM_JOB | CREATE_SUSPENDED` and reports any created child's PID while holding it at a supervisor-visible barrier. Breakaway denial is the expected pass. If a child exists, controller and watchdog recovery are required before any resume. | Only an attributable breakaway denial passes normally. An unexpected outside-job child stays suspended; controller must open/terminate it directly and confirm exit before job teardown. Record PID, open/terminate results and errors, request/exit timestamps, wait result, and exit status. Any access, termination, or confirmation failure stops the complete qualification as incomplete; no later case runs. This cleanup capability is unqualified and Q03 remains gated on owner approval of the workload ACL/controller identity and independent recovery review. | 1 s | 10 s | 64 MiB | 1 MiB |
| Q04 Nested-job interaction | In one case, test a standalone supervisor creating its fresh workload job, then a supervisor inside a restrictive outer job attempting a nested workload job; verify effective composed limits if accepted or fail-closed rejection before resume. | Any weakened outer limit, unverified effective limit, or resumed workload after incompatible assignment fails. Record success/rejection per subcase. | 1 s | 10 s | 64 MiB | 1 MiB |
| Q05 CPU semantics/limit | Use `JOB_OBJECT_LIMIT_JOB_TIME` with `PerJobUserTimeLimit=20,000,000` 100-ns units (2.0 seconds) and explicitly set `JobObjectEndOfJobTimeInformation.EndOfJobTimeAction=JOB_OBJECT_TERMINATE_AT_END_OF_JOB`. Record requested/read-back settings. Run a user-mode burner expected to trigger the action and a separate bounded kernel-heavy worker that exits before the 2.0-second user-time threshold. Sample job accounting at a 10-ms target cadence; track each QPC timestamp and actual query gap online, retaining the QPC frequency, sample count, maximum-gap duration and endpoints, threshold-bracketing samples, final user/kernel totals, and last-process-exit time. | Missing/unverified action, failure of the user-mode subcase to terminate by its 20-s case deadline, or missing bounded sample/exit data is fail or inconclusive. The kernel-heavy subcase is inconclusive if user time reaches the limit before its planned exit. A query gap over 100 ms makes the overshoot estimate inconclusive. Report the observed threshold/exit bracket; 100 ms is a data-quality threshold, not an OS guarantee. Any claim that the user-only limit enforces combined CPU is a contract failure. Does not qualify the 120-s combined requirement. | 4 s | 20 s | 64 MiB | 1 MiB |
| Q06 Job memory | Small native worker commits until just beyond a 268,435,456-byte job limit; expected commit denial is recorded while the worker reports. Compare live private-commit sum, job accounting, and peak. | Wrong metric, excess commit, unhandled failure, or no reconciliation: memory-control failure. | 3 s | 20 s | 256 MiB | 1 MiB |
| Q07 Wall termination | Synthetic sleeper remains alive through the 120-second QPC deadline; controller calls `TerminateJobObject`, records request/return/last exit, and tests the candidate 15-second grace. | Any process survives beyond the owner-approved deadline or is not confirmed dead: wall/termination failure. | 2 s | 135 s | 64 MiB | 1 MiB |
| Q08 Controller failure | Primary controller is deliberately ended; independent watchdog detects loss and terminates the job. A separate subcase closes the final job handle to verify kill-on-close. | Descendant survives, watchdog cannot act, or handle can be retained by workload: fail closed. | 1 s | 20 s | 64 MiB | 1 MiB |
| Q09 Pipe/artifact exhaustion | Synthetic worker emits at least 2 MiB on stdout and stderr. Writer retains only reserved quota, drains/discards excess, records read/retained counts, terminates, and leaves an explicitly incomplete record. | Deadlock, quota overflow, uncontrolled disk file, or success-shaped manifest: artifact failure. | 1 s | 20 s | 64 MiB | 1 MiB |
| Q10 Compressed ledger sizing | After a schema/writer addendum freezes all deterministic record shapes, produce 8,196 synthetic records (no neuron, task examples, or fixture) with both checkpoint shapes; gzip using pinned Python/zlib settings. | Incomplete shapes, unbounded record size, ledger >786,432 bytes, total >1MiB, or simultaneous-copy overrun: sizing failure. | 5 s | 30 s | 64 MiB | 1 MiB |
| Q11 Evidence integrity | Produce one complete synthetic evidence set and one forced incomplete set; verify atomic file completion, byte lengths, SHA-256, incomplete status, failure record, read-only retention, and missing-record handling. | Hash mismatch, partial success-shaped evidence, or unrecorded missing file: integrity failure. | 2 s | 20 s | 64 MiB | 1 MiB |
| Q12 Command/zero-retry policy | Validate the exact Phase 2A path/argv/hash profile without launching the E2 fixture. Submit disallowed command/module/cwd/hash variations and verify rejection before process creation; record one attempt only. | Any alternate command accepted, any fixture launched, or any retry: authorization-boundary failure. | 1 s | 10 s | 64 MiB | 1 MiB |

Q05's two-second limit is a reduced synthetic semantics check, not evidence
for the 120-second Phase 2A CPU threshold. Q07's 15-second grace is a
candidate that requires owner approval and still provides an observed
qualification target rather than a universal OS bound. Q10 is the only
permitted compression-size generation and requires a separate owner decision
and explicit qualification authorization.

## 11. Separate qualification budget

Proposed maximum for the complete R1 qualification lane, if later authorized:

| Bound | Qualification proposal |
|---|---:|
| Cases | Exactly Q01–Q12, one invocation each |
| Case retries/replacements | 0 |
| Aggregate observed job user-plus-kernel CPU | 30 seconds |
| Aggregate wall | 360 seconds |
| Concurrent Job Object memory | 268,435,456 bytes |
| Retained artifacts, all files combined | 1,048,576 bytes |
| Network access | None |
| E2 calls, datasets, benchmark examples, training, or scoring | 0 |

Per-case maxima in §10 sum to 315 seconds, with 45 seconds of aggregate
wall headroom for setup and finalization. Per-case observed job CPU maxima
sum to 23 seconds; the 30-second aggregate is a stop target, not a hard
Windows Job Object guarantee. The 360-second wall budget is likewise a
controller/watchdog stop target until termination latency is independently
demonstrated. The memory ceiling matches the Phase 2A proposed job limit;
control-plane memory is separately observed and not represented as part of
the workload job metric.

This budget is not funded by, deducted from, or authorized under Phase 2A,
Phase 2B, Luna-64, or any benchmark allowance. Owner authorization must name
the exact Q01–Q12 case package and accept the unresolved measurement semantics
before any case runs. No such authorization exists in this task.

## 12. Owner decisions required

Before the supervisor contract can become execution-ready, the owner must
record decisions on:

1. **CPU:** preserve the hard 120-second user-plus-kernel requirement and
   require a different independently identified enforcement technology, or
   explicitly amend the metric/guarantee to one of the alternatives in §3.3.
2. **Wall:** whether the 120-second deadline is a termination-request
   trigger with a separate grace interval, and if so the approved maximum
   elapsed deadline and failure policy. The 15-second candidate in §5 is
   not accepted by default.
3. **Memory metric:** whether the Windows job-wide commit limit is accepted
   only after live `PrivateUsage` reconciliation or an alternative
   enforcement technology is required if they differ.
4. **Evidence writer:** choose the bounded controller-mediated channel or
   qualified per-run storage quota in §7.3; approve any Phase 2A interface or
   environment addendum required to implement it.
5. **Ledger:** authorize synthetic Q10 sizing under the separate budget and
   determine the next step if the actual compressed ledger exceeds 768 KiB.
6. **Isolation:** approve the AppContainer/restricted-token access profile
   and any required path/ACL/host setup only after a no-admin feasibility
   review; no infrastructure change is approved here.
7. **Q03 escape recovery:** approve the workload process ACL, controller and
   watchdog identities, required terminate/synchronize access, recovery order,
   bounded exit-confirmation policy, and evidence fields for an unexpected
   outside-job suspended child. Independently review/qualify this capability
   before Q03; if it is unavailable, Q03 and the qualification remain blocked.
8. **Qualification execution:** after the exact final contract and supervisor
   identity are independently reviewed, separately authorize the Q01–Q12
   synthetic qualification budget. This decision does not authorize Phase
   2A or Phase 2B.

An owner decision cannot substitute for demonstrated enforcement or
independent review. A change to existing resource limits, evidence schema,
environment, or execution restrictions requires explicit owner approval and
contract revision.

## 13. Independent review plan and current disposition

Four independent, read-only review lanes assessed the R1 design:

| Reviewer | Required scope |
|---|---|
| A — Windows Job Object correctness | Supported Windows 10 APIs; aggregate CPU, job memory, nested jobs, children, effective limits, accounting, and termination behavior. |
| B — Supervisor security/failure behavior | Suspended admission, handle inheritance/duplication, breakaway, controller/watchdog failure, kill-on-close, output reader failure, and unauthorized command rejection. |
| C — Evidence/artifact budget | Schema-derived size estimates, gzip overhead, combined retained-byte budget, partial/failure records, temporary copies, and integrity. |
| D — Governance/provenance | Owner acceptance scope, exact baseline and source hashes, Phase 2A/2B separation, capacity arithmetic, no benchmark execution, Luna-64 non-borrowing, and Luna-63C preservation. |

| Reviewer | Disposition and remaining boundary |
|---|---|
| A — Windows Job Object correctness | **PASS — Q05 sampling and end-of-job action are specified.** The user-time-only job limit remains distinct from aggregate user-plus-kernel CPU; Q05 does not qualify the Phase 2A combined limit. |
| B — Supervisor security/failure behavior | **PASS — fail-closed framing is adequate.** Normal breakaway is denied; unexpected outside-job-child cleanup remains owner-gated and unqualified. |
| C — Evidence/artifact budget | **PASS WITH CLARIFICATIONS — bounded summary and quota structure are coherent.** No measured or exact ledger-size proof was established; Q10 requires the schema/writer addendum, and the inherited-environment policy remains unresolved. |
| D — Governance/provenance | **PASS — publication scope is governance-only.** No execution status changed; Phase 2A/2B remain unauthorized, and Luna-64/Luna-63C evidence is not borrowed or modified. |

The independent findings do not close the following execution blockers:

- Windows Job Objects cannot hard-limit aggregate user-plus-kernel CPU at
  120 seconds using the documented job-time limit; combined counters are
  observable only.
- The wall trigger cannot promise last process exit by 120 seconds; no
  finite API termination-latency bound is documented.
- The Job Object commit limit is not yet shown equivalent to the precise
  accepted concurrent private-commit metric.
- No exact size proof exists for the 8,196-record gzip ledger under a
  768-KiB ledger allocation and 1-MiB combined artifact limit.
- The full workload environment allowlist is not frozen by the published
  Phase 2A contract; it specifies `PYTHONHASHSEED=0` and the external
  evidence-directory variable as overrides but does not freeze inherited
  environment handling.
- No approved, qualified channel transfers JSONL from the restricted test
  process to controller-owned evidence without granting bypassable write
  access.
- Q03's direct recovery of any unexpected outside-job suspended child is not
  qualified for the proposed restricted workload ACL/controller identity.
- The independent process-observer technology, event-loss signal, and
  polling interval still need to be frozen before qualification-case
  implementation.

**Integrated Luna-0 disposition: BLOCKED — SUPERVISOR QUALIFICATION CONTRACT
INCOMPLETE.** Reviewers found the qualification-design framing coherent, but
the resource guarantees, evidence path, and recovery/observation controls
remain unresolved. In particular, there is no identified independently
qualified supervisor. This result authorizes neither qualification execution
nor Phase 2A/2B.

The final Luna-0 disposition is exactly:

**PASS — LUNA-65 SUPERVISOR QUALIFICATION CONTRACT READY FOR OWNER AUTHORIZATION**

or

**BLOCKED — SUPERVISOR QUALIFICATION CONTRACT INCOMPLETE**

Only the blocked disposition applies to this R1. A future PASS would mean
only that a specific qualification plan is sufficiently specified for a
later owner authorization. It would not qualify a supervisor, authorize
installing/implementing/running it, or authorize Phase 2A/2B.

## 14. References and validation boundaries

Authoritative Windows API references:

- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [JOBOBJECT_BASIC_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information)
- [JOBOBJECT_BASIC_ACCOUNTING_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information)
- [JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information)
- [JOBOBJECT_NOTIFICATION_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_notification_limit_information)
- [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
- [QueryInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject)
- [TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject)
- [Nested Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs)

Repository facts were inspected statically. The Windows edition/build was read
from local OS metadata. No API was called; no binary or supervisor was
created, installed, configured, or executed; no fixture, test, Q01–Q12
qualification case, benchmark, or resource probe was run. No compressed
evidence data was generated or measured.
