# Luna-65 Phase 2A Supervisor Authorization I Corrective Contract — R1

**Gate:** `L65-PHASE2A-SUPERVISOR-AUTH-I-CORRECTIVE-R1`

**Status:** **DRAFT FOR INDEPENDENT REVIEW — CORRECTIVE IMPLEMENTATION NOT
AUTHORIZED.**

**Current implementation disposition:** **BLOCKED — IMPLEMENTATION
INCOMPLETE.**

This document proposes a narrowly bounded contract for correcting the
Luna-65 Phase 2A supervisor. It does not qualify a supervisor, authorize
source changes, authorize operating-system provisioning, or authorize
execution. It does not replace the Phase 2A policy in
[`LUNA_65_PHASE2A_SUPERVISOR_IMPLEMENTATION_AUTH_R1.md`](LUNA_65_PHASE2A_SUPERVISOR_IMPLEMENTATION_AUTH_R1.md)
or its resource limits. The source remains a fail-closed, unqualified
scaffold.

## 1. Starting provenance and current state

The reviewed proposal commit is `1d6325f3ca738b32a6ee9e1a5613d2faa9458770`
on branch `governance/luna64-r4.3-freeze-20261010`. Checkout inspection
found that this is `HEAD`, with parent
`d11d370a7c97184529845c9cac984fc22018c576`; the proposal commit object
exists and its proposal-file blob is `3aefe152d0cf55bb759dec85551efb3239d541fc`.
The latter matches the indexed/committed blob.

| Artifact | Observed checkout SHA-256 | Git state |
|---|---|---|
| `scripts/luna65_phase2a_supervisor.py` (21,494 bytes) | `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1` | Untracked; not operational |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `64AF62CD2E8CD0696BF52EEDF63672FB04399EF949B580FD551360A0F237ED61` | Modified, uncommitted |
| `workflow/handoffs/luna-0-luna65-phase2a-authorization-i-review-20261012.md` | `B542AD2FD7BD6B587280420D8210F570CF13A66CA6F4CE86F461DDA3D94A46C4` | Untracked |
| `workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_IMPLEMENTATION_AUTH_R1.md` | `31C2CEDAAC91C78A79D746879AEB52759A92335DDA7D18EDC5F0E055F141EA97` | Tracked at proposal commit; unchanged |

The current workflow and handoff hashes are checkout-byte identities, not
committed Git-blob identities. The pre-existing uncommitted governance work
is preserved. No file was staged, and this corrective review does not treat
the source candidate as complete or publishable.

**Observed source state:** it contains policy constants and partial Job
Object configuration/accounting helpers, but no suspended process
creation/assignment/resume path, watchdog, process observer, restricted
workload token, direct-write boundary, controller-owned evidence writer,
bounded cessation deadline, or working workload admission path. Its entry
point rejects admission. No runtime execution is authorized or reported.

The exact Phase 2A fixture `tests/test_luna65_capacity_direct.py` is absent
from this checkout. Its identity and the future pinned Python/pytest
identities therefore remain unavailable.

The owner-provided source hashes match the checked-out bytes. Reviewer D
initially misread the prompt as not supplying expected hashes; that
statement is corrected here. Review D did not identify a source-hash
mismatch.

## 2. Frozen policy and decision boundary

The policy below is unchanged from the accepted Phase 2A design:

| Control | Required value |
|---|---:|
| Monitored aggregate job user plus kernel CPU | 120 seconds |
| Monitored wall interval | 120 seconds from supervisor `T0` |
| Primary early wall-stop request | `T0 + 115 seconds` |
| Watchdog deadline escalation | `T0 + 120 seconds` if the job remains active |
| Job-wide memory-control candidate | 268,435,456 bytes |
| Accepted memory measure | Aggregate concurrent job-wide private committed bytes |
| Combined retained-artifact ceiling | 1,048,576 bytes |
| Retries | Zero |

The CPU and wall limits are monitored budgets, not hard execution-time
guarantees. Requests and API success returns are not cessation evidence.
Any observed CPU total above 120 seconds or observed workload cessation /
supervisor completion after 120 seconds fails. The 115-second request leaves
the accepted five-second margin; it does not claim bounded Windows
termination latency.

**Open owner decisions block a final implementation authorization:**

1. Freeze a maximum post-120-second observation interval and the exact point
   at which `TERMINATION_UNCONFIRMED` is recorded. The earlier 15-second
   R1 candidate is not accepted by this contract. The same frozen deadline
   must govern Q03 escaped-process recovery; there is no separate Q03 grace.
2. Decide whether a QPC timestamp of *observed cessation confirmation* is
   acceptable evidence, rather than an exact kernel process-exit instant.
   The documented wait/accounting interfaces expose observation time; they
   do not provide an exact QPC timestamp for the physical exit event.
3. Resolve whether the accepted private-commit metric may be proven by the
   Job Object commit charge as a conservative ceiling, or retain a hard
   implementation blocker until the documented metric mismatch is
   reconciled.

No default value or equivalence is inferred for these decisions.

## 3. Corrective implementation scope

### 3.1 Repository file allowlist

The preferred and only proposed implementation file remains:

* `scripts/luna65_phase2a_supervisor.py`

It may contain fixed internal controller, watchdog, observer, and writer
modes, all selected by private, enumerated mode arguments. It must not accept
an arbitrary executable, shell command, Python module, working directory,
environment, evidence destination, retry count, or budget.

No separate repository implementation file is currently necessary for the
controller/watchdog/writer orchestration. If the process observer requires a
privileged service, installed helper, signed external profile, host policy,
AppContainer/package provisioning, filesystem quota, VHD, or another source
file, that dependency is not covered by this proposed one-file allowlist.
Stop and obtain a separate owner authorization naming the exact files and
host changes before implementing it. Do not create or modify fixtures, test
files, `tpcn/` modules, worker modules, or benchmark code.

### 3.2 Fail-closed status

The implementation must refuse admission unless every prelaunch check and
required observer is ready. It must keep refusing admission while any
required identity, privilege, containment, metric, observer, post-budget
deadline, or evidence check is unresolved. It may not describe this
candidate as operational or qualified.

## 4. Admission lifecycle

The following order is mandatory. T0 is sampled on the first supervisor
main-entry instruction, before preflight. Admission setup and evidence
finalization consume the same wall interval; the wall clock does not restart
at process creation.

| Order | Required operation and API surface | Refusal/cleanup behavior |
|---|---|---|
| 1 | Capture `QueryPerformanceCounter` and `QueryPerformanceFrequency`; record invoking process-start observation separately. | QPC/frequency query failure is `RESOURCE_MEASUREMENT_INCONCLUSIVE`; no workload process is created. |
| 2 | Check the exact immutable command tuple, working directory, checkout/revision/clean-source policy, source identity, fixture path and SHA-256, interpreter and pytest identities, and fixed evidence profile. Open and hash files by handle; resolve final paths and reject unexpected reparse points/path changes. The later exact owner authorization supplies the source hash in its fixed invocation profile; hash source bytes and compare against that approved value, never accept a caller-selected override. Do not embed a self-hash as an independent identity anchor. | Any missing or mismatched value rejects admission. Fixture and interpreter hashes must come from a later exact owner-approved profile; do not invent current hashes. |
| 3 | Construct the exact environment block from the approved names only. Use `CreateProcessW` with `CREATE_UNICODE_ENVIRONMENT`; provide a sorted UTF-16 double-NUL-terminated block, never copy the caller's environment. Preserve the approved fixed values and omit unlisted variables, including `PYTHONPATH`, `PYTHONHOME`, proxy variables, and evidence-directory variables. | Invalid/missing values reject admission. Do not widen the allowlist to make pytest or the fixture operate. |
| 4 | Create the controller-owned evidence directory and apply/check controller-only access. Reserve the complete artifact budget before launch. Create bounded anonymous pipes for stdin, stdout, stderr, and the versioned result channel. The controller closes the stdin writer before resume so the child reads EOF. The child receives no evidence path or evidence-file handle. | Failed ACL/read-back/reservation/pipe setup rejects admission. |
| 5 | Obtain the trusted primary token with `OpenProcessToken`; build a restricted primary token using `CreateRestrictedToken` with `WRITE_RESTRICTED`, `DISABLE_MAX_PRIVILEGE`, disabled administrative/enabled groups as appropriate, and an unpredictable per-run restricting SID. Use `SetTokenInformation(TokenIntegrityLevel)` to set low integrity. Verify effective token properties with `GetTokenInformation` and `IsTokenRestricted`. | Any token API failure, unexpected enabled privilege/group, or identity mismatch rejects admission. |
| 6 | Start the independent process observer before workload creation and prove it is ready with no event loss. | Missing privilege, observer startup failure, event-loss signal, or missed readiness rejects admission. |
| 7 | Create a fresh unnamed Job Object with a restrictive security descriptor and non-inheritable handle using `CreateJobObjectW`. Configure the memory and kill-on-last-handle-close flags using `SetInformationJobObject(JobObjectExtendedLimitInformation, ...)`. Explicitly leave both breakaway flags unset. Query settings back before creating or resuming workload code. | Exact flag/value mismatch rejects admission. |
| 8 | Associate the job with a controller-owned completion port using `CreateIoCompletionPort`, `SetInformationJobObject(JobObjectAssociateCompletionPortInformation, ...)`, and `GetQueuedCompletionStatus`; configure/read back the notification limit as specified in §8. Start the separate watchdog outside the job, duplicate the job handle to it with only `JOB_OBJECT_QUERY`, `JOB_OBJECT_TERMINATE`, and `SYNCHRONIZE` rights, establish authenticated bounded heartbeat/control channels, and prove ready state. | Failure rejects admission; informational message absence is never proof that no limit event occurred. Watchdog/handle/channel readiness failure also rejects admission. |
| 9 | Construct `STARTUPINFOEX`; mark only the explicitly approved child-side pipe handles inheritable, set `bInheritHandles=TRUE`, and pass only those handles via `InitializeProcThreadAttributeList` and `UpdateProcThreadAttribute(PROC_THREAD_ATTRIBUTE_HANDLE_LIST)`. Set `STARTF_USESTDHANDLES` and the exact stdin/stdout/stderr pipe endpoints in `STARTUPINFO`; the versioned result channel is an explicit listed handle. Use the exact Python executable as `lpApplicationName`, an exact quoted command line, and `CreateProcessAsUserW` with `CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT | EXTENDED_STARTUPINFO_PRESENT`. No shell. | On pre-assignment failure, terminate the suspended root with `TerminateProcess`, wait on its process handle, verify it exited, and record failure. It has not been resumed and no fixture code may execute. |
| 10 | Assign the suspended process with `AssignProcessToJobObject`. Verify the root with `IsProcessInJob`, reconcile `QueryInformationJobObject(JobObjectBasicProcessIdList)` with `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.ActiveProcesses`, and read back effective memory/breakaway settings. Verify observer and watchdog are outside the workload job. | Any assignment or reconciliation failure: terminate the still-suspended root directly if it is not in the job; terminate the job if it is; wait and record observations. Never resume. |
| 11 | Verify the final command, environment digest, source/fixture/interpreter identities, observer-ready state, handle allowlist, token state, job limits, and wall deadline are still unchanged. If current QPC is at or beyond `T0 + 115 s`, refuse admission rather than starting work after the early-stop boundary. Otherwise call `ResumeThread` exactly once. Start job CPU accounting at the first successful resume. | Any failure before a successful resume leaves the fixture unexecuted and rejects admission. |

`CreateProcessAsUserW` must receive the restricted version of the trusted
controller's primary token. Microsoft documents that a restricted version
of the caller's primary token can be used without
`SeAssignPrimaryTokenPrivilege`; all other privilege/access failures remain
fail-closed. Do not use `SANDBOX_INERT`.

No token or DACL setting is assumed effective merely because a setter
returned success: query token and Job Object settings back and record exact
effective values. The precise Windows build, token, DACL, path, and nested
job behavior still require later qualification.

## 5. Monitoring, failure, and cessation record

### 5.1 Primary monitor

* Use QPC only for elapsed time. Record frequency and every monitor
  timestamp; target a 10-ms cadence and classify any observed sample gap
  above 100 ms as inconclusive.
* At every sample query
  `JobObjectBasicAccountingInformation`: raw `TotalUserTime`,
  `TotalKernelTime`, combined 100-ns value, converted seconds, active
  process count, QPC, and query result. Reject query failure, negative or
  regressing counters, missing member accounting, or a gap over 100 ms.
* At the first observed combined CPU value `>= 1,200,000,000` 100-ns units
  while the job is active, immediately request `TerminateJobObject`. The
  CPU-at-request value is the exact triggering sample, not a later query.
  Record reason `CPU_THRESHOLD`, raw CPU at request, QPC, return/error, and
  all subsequent requests/observations. A final total `> 1,200,000,000` is
  `CPU_BUDGET_EXCEEDED`; report exact observed overshoot. The final total is
  the last successful accounting query after cessation confirmation; if
  unavailable, classify measurement/evidence incomplete. Do not add a CPU
  grace allowance.
* At `T0 + 115 s`, if the job is active, request `TerminateJobObject` with
  reason `WALL_EARLY_STOP`. At `T0 + 120 s`, the watchdog independently
  issues its final escalation request with reason `WALL_DEADLINE_ESCALATION`
  if the job remains active. CPU/115-second/monitor-failure requests belong
  to the primary; heartbeat and 120-second escalation requests belong to the
  watchdog. These are distinct authorities by design. If both issue near
  the boundary, record both calls with source-local sequence, reason,
  request QPC, sampled CPU when available, return/error, and subsequent
  observations; a duplicate request is not cessation evidence. A request
  never substitutes for observing cessation.
* The primary sends a bounded heartbeat record containing its QPC every
  monitor sample (target 10-ms cadence) over a private controller channel.
  The watchdog checks at a target 10-ms cadence. The heartbeat contains
  sample sequence, sample QPC, latest CPU query status and raw accounting
  totals. A failed query is reported as failure, not as a healthy sample.
  The watchdog compares its own QPC against the latest valid sample QPC and
  requests termination if the sample is stale by 100 ms or reports failure;
  repeating heartbeats cannot mask a stalled accounting sample. It also
  compares the last heartbeat receive QPC to detect a stalled primary.
  The watchdog sends a corresponding liveness response every 50 ms only
  after completing its own checks; the primary compares its QPC against
  the last response. The watchdog also watches the primary process handle
  independently. The primary watches the watchdog process handle and
  channel; if the watchdog exits or its response is 100 ms late, the primary
  records `CONTROLLER_FAILURE`, requests job termination, and cannot report
  success. The watchdog stays outside the workload job.
* If the primary exits or hangs, the watchdog requests termination and
  continues independent job/ETW cessation observation until the frozen
  deadline. If the watchdog exits, the primary remains responsible for
  monitoring and termination. If both trusted processes fail, closing their
  last job handle invokes the configured kill-on-close fallback; that
  fallback is recorded only if an observer survives and sees it. It never
  substitutes for a cessation record. If no trusted observer survives,
  evidence is incomplete and cessation is unconfirmed.
  A simultaneous hang of both trusted processes is not made safe by
  kill-on-close (handles remain open); no hard response-time guarantee is
  claimed for that condition. It remains a `CONTROLLER_FAILURE` /
  `TERMINATION_UNCONFIRMED` qualification blocker.
* Record every monitor sample, termination reason/request/return/error,
  `ActiveProcesses`, PID-list result, completion-port message, observer
  event/loss counter, process exit observation, pipe EOF, final resource
  query, and evidence-finalization result. Storage is pre-bounded by the
  artifact reservations; do not keep an unbounded in-memory event history.

### 5.2 Distinguish request from observed cessation

Maintain separate immutable records for:

1. Each termination request: requester, reason, request QPC, CPU/wall
   sample (the triggering accounting sample for CPU), API return, and
   Win32 error. The primary and watchdog use separate source-local sequence
   numbers; each actual API call is recorded, including intentional
   re-requests at the deadline.
2. Each later observation: QPC, job handle signaled state, active count,
   PID list, known process handles/signals/exit status, observer state and
   pipe EOF state.
3. Final cessation confirmation: separately record the QPC when each
   condition is first observed—job handle signaled, Job Object active count
   zero, all enumerated workload process handles signaled, ETW graph
   reconciled with no descendant, and required pipes at EOF.
   `cessation_confirmed_observed_qpc` is the maximum of those observation
   QPCs: it is the first time all persistent conditions have been observed
   true. If active count is nonzero or the PID list is nonempty when the job
   handle first signals, record the mismatch, do not confirm cessation, and
   continue bounded queries until reconciled or the frozen deadline.

Record the ETW kernel process-stop event timestamp (with the trace clock
configured to QPC) as `last_process_stop_event_qpc`. It is the timestamp of
the observed kernel trace event, not a stronger claim about the physical
execution instant. Label item 3 `cessation_confirmed_observed_qpc`; it is
the latest observation among required persistent conditions, not the event
timestamp. Where available, record `GetProcessTimes` exit FILETIME
separately and do not present it as QPC. Owner acceptance of this evidence
rule remains pending under §2.

At the end, make a final CPU query and record final user/kernel totals,
CPU overshoot, maximum sample gap, cessation-observation QPC, elapsed wall
time, active count/PID-list reconciliation, exit codes and outstanding
descendants. Any observed cessation QPC or supervisor completion after
`T0 + 120 s` fails wall budget.

**[OWNER DECISION REQUIRED BEFORE IMPLEMENTATION]** Continue observing only
until `T0 + 120 seconds + POST_BUDGET_OBSERVATION_SECONDS`, where the owner
must freeze `POST_BUDGET_OBSERVATION_SECONDS` as a positive bounded integer.
At that deadline, if no independent cessation confirmation exists, record
`TERMINATION_UNCONFIRMED`, finalize the bounded failure record, and stop
observing. Do not default to the historical 15-second candidate.
This is also the sole Q03 recovery deadline. If cessation is unconfirmed at
that deadline, report the last successful CPU sample with its QPC,
`final_cpu_query_status=NOT_OBTAINED_NO_CESSATION`, and
`RESOURCE_MEASUREMENT_INCONCLUSIVE`; do not call it a final total or claim
that the CPU budget passed. If cessation is confirmed, obtain and record the
required post-cessation accounting query before finalization; query failure
is likewise inconclusive.

### 5.3 Failure handling

Record the first failure and all subsequently observed failures. Preserve the
existing classes:

`CPU_BUDGET_EXCEEDED`, `WALL_BUDGET_EXCEEDED`, `MEMORY_LIMIT_EXCEEDED`,
`ARTIFACT_LIMIT_EXCEEDED`, `CONTROLLER_FAILURE`,
`PROCESS_CONTAINMENT_FAILURE`, `TERMINATION_UNCONFIRMED`,
`EVIDENCE_INCOMPLETE`, and `RESOURCE_MEASUREMENT_INCONCLUSIVE`.

Record `TERMINATION_REQUEST_FAILED` as an explicit failure event with API,
request reason, QPC, and Win32 error; also classify `CONTROLLER_FAILURE`.
Any false `TerminateJobObject` result is a request failure, including
`ERROR_INVALID_HANDLE` and `ERROR_ACCESS_DENIED`; never infer that an
invalid handle means the job is empty. Continue independent observation and
the other authority's permitted escalation if its valid handle remains.
If cessation is not then confirmed by the frozen observation deadline, also
classify `TERMINATION_UNCONFIRMED`. Query/cadence/counter failures
record `RESOURCE_MEASUREMENT_INCONCLUSIVE` and immediately request whole-job
termination. Memory/artifact/containment failures stop further admitted
work, request termination, preserve bounded evidence, and never yield a
success result.

No broad exception may produce a success-shaped fallback. On primary
controller exception or process death, the watchdog requests termination
and independently observes; dual-controller failure relies only on
`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` as a final fallback and is not called
confirmed cessation without the observations above.

## 6. Process-tree and identity containment

### 6.1 Job Object controls

Configure exactly `JOB_OBJECT_LIMIT_JOB_MEMORY |
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; do not set
`JOB_OBJECT_LIMIT_BREAKAWAY_OK` or
`JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK`. Windows documents that ordinary
`CreateProcess` children inherit job membership by default and that the
breakaway flags alter this behavior. Verify membership for every process
event and reconcile active count with `JobObjectBasicProcessIdList`.

The Windows 10 target supports nested jobs, but enclosing-job policy may
constrain assignment and child behavior. `AssignProcessToJobObject` failure,
unexpected enclosing-job composition, or inability to read back effective
limits rejects admission. Do not claim the outer job's limits are irrelevant.
The workload never receives a job handle or trusted controller handle.
All handles are non-inheritable except the explicit pipe list; the worker
inherits no process/job/watchdog/evidence-directory handle.

### 6.2 Independent observer candidate and Q03 stop rule

The candidate external observer is a separate trusted process mode in the
same authorized source using the NT Kernel Logger ETW process tracing
surface: `StartTraceW`/`ControlTraceW`, `OpenTraceW`, and `ProcessTrace`,
with `EVENT_TRACE_FLAG_PROCESS` and QPC timestamps
(`EVENT_TRACE_PROPERTIES.Wnode.ClientContext = 1`). Record process
start/stop events and check `EVENT_TRACE_PROPERTIES` loss counters
(`EventsLost`, `RealTimeBuffersLost`, and `LogBuffersLost`). It starts before
workload admission and maintains a bounded process-instance graph keyed by
PID plus creation identity, not PID alone. For every observed process whose
parent chain reaches a workload member, query `IsProcessInJob` and reconcile
the job PID list.

ETW is a **candidate**, not yet a qualified observer. Kernel-session
privileges (including required administrative/system-profile access),
session conflicts, event ordering/loss, startup readiness,
coverage of process creation routes, and exact child ancestry are not
established for the target host. If the observer cannot start with required
privilege, if any loss counter changes, if its session stops, or if ancestry
cannot be reconciled, fail closed before admission or terminate immediately
after admission. The job PID list alone is not an outside-job observer.

On a detected outside-job descendant (Q03), record
`PROCESS_CONTAINMENT_FAILURE`, stop all subsequent cases, terminate the
in-job job, and use `OpenProcess` with only
`PROCESS_TERMINATE | SYNCHRONIZE | PROCESS_QUERY_LIMITED_INFORMATION` to
terminate each observed escaped process and descendants. Confirm each
individual exit with `WaitForSingleObject` and reconcile the ETW graph until
no descendant remains. If access is denied, an event is lost, process
identity is ambiguous, descendants cannot be enumerated, or exit cannot be
confirmed by the §5.2 deadline `T0 + 120 seconds +
POST_BUDGET_OBSERVATION_SECONDS`, record
`TERMINATION_UNCONFIRMED`. Never resume an escaped suspended child or
continue the suite after Q03.

This recovery sequence is a proposed response, **not proof that an
arbitrary outside process can always be discovered or terminated**. ETW
observation can lag process creation; a child may execute before the
observer responds. Protected processes, service-created processes, and
unavailable privileges can defeat recovery. Qualification must demonstrate
the exact Q03 scenario and failure behavior on the target build. If the
project requires a guarantee stronger than detection plus bounded recovery,
an independently privileged observer or host policy requires a separate
owner authorization.

## 7. Restricted token and filesystem boundary

The worker token is created with a unique per-run restricting SID and
`CreateRestrictedToken(WRITE_RESTRICTED | DISABLE_MAX_PRIVILEGE, ...)`.
Microsoft documents that restricted-SID access checks are in addition to
enabled-SID checks, and that `WRITE_RESTRICTED` uses restricting SIDs for
write access. The token also uses a low integrity level via
`SetTokenInformation(TokenIntegrityLevel)`. Verify the token with
`IsTokenRestricted` and `GetTokenInformation`; never set `SANDBOX_INERT`.

The intended filesystem policy is default-deny for worker writes: no
existing file, directory, registry key, volume, or device receives a write
ACE for the unpredictable restricting SID. Grant only read/execute to the
required pinned interpreter, Python libraries, pytest package, fixture,
and checkout. Apply and read back controller-only ACLs to the evidence
directory. The only worker write-capable handles are the explicitly
inherited stdout/stderr/result pipes; those handles grant access only to
their respective controller pipe endpoints, not to a filesystem path.
Set `TEMP`/`TMP` to the reviewed dedicated path with no worker write grant.
Keep the checkout, user profile, temp, registry, and evidence paths
unwritable by the worker. Resolve final paths, reject unreviewed reparse
points/network paths, and do not provide writable mapped sections or other
inherited handles.

Low integrity and `WRITE_RESTRICTED` are defense-in-depth, not an already
qualified whole-machine sandbox. Qualification must show effective denies
for every relevant write target, including alternate filesystems, reparse
paths, registry objects, and inherited handles, and establish that the
fixture/test works without any write access. Mandatory Integrity Control
labels may be used as a second barrier only with separate exact review of
the SACL and effective access. The previous proposal does not authorize
AppContainer provisioning, filesystem quotas, VHDs, system policy, or
host-wide ACL changes. If the restricted token cannot enforce the required
boundary without those, stop and obtain separate owner approval; never call
pipe caps filesystem-wide containment.

The environment allowlist omits proxy and Python path/home injection but
does not itself disable networking. Phase 2A admits no network operation.
If network prevention is required by the eventual threat model, the
existing authorization does not provision an OS network boundary; obtain
separate owner approval and qualification rather than infer it from the
environment block.

## 8. Memory control and accepted metric

Use `SetInformationJobObject(JobObjectExtendedLimitInformation, ...)` with
`JOBOBJECT_EXTENDED_LIMIT_INFORMATION.BasicLimitInformation.LimitFlags =
JOB_OBJECT_LIMIT_JOB_MEMORY | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` and
`JobMemoryLimit = 268435456`. Query the same information class back and
require exact flags and byte value before resuming. Do not set per-process
memory or working-set limits as substitutes.

Set and verify `JobObjectNotificationLimitInformation` with the matching
268,435,456-byte `JobMemoryLimit` and
`JOB_OBJECT_LIMIT_JOB_MEMORY`; associate the completion port before
admission. Record `JOB_OBJECT_MSG_NOTIFICATION_LIMIT` if delivered and
`JOB_OBJECT_MSG_JOB_MEMORY_LIMIT` if received. Notification events are
informational; an absent ordinary completion message is not evidence that
no limit was reached. Record allocation failures and request whole-job
termination on an observed limit failure, then confirm cessation separately.

Observe:

* `JOBOBJECT_EXTENDED_LIMIT_INFORMATION.PeakJobMemoryUsed` as a job
  high-water mark, not an instantaneous private-byte sum.
* `GetProcessMemoryInfo(PROCESS_MEMORY_COUNTERS_EX).PrivateUsage` for each
  enumerated in-job PID, holding a process handle while reading it; record
  query QPCs, skew, missing/exited PIDs, and reconciliation against active
  count and PID list.
* The job's enforced commit limit and exact setting read-back.

Microsoft documents `JobMemoryLimit` as the virtual memory that can be
committed for the job and `PeakJobMemoryUsed` as peak usage of processes
associated with the job. The owner-accepted metric is a sum of concurrent
per-process `PrivateUsage` commit charges. These documented surfaces do not
declare that Job Object commit is the exact same metric or provide an
atomic per-process-private sum. Sampling private usage has skew and can miss
short peaks. The implementation must record this discrepancy and must not
claim metric equivalence or a hard accepted-metric ceiling until independent
review/qualification establishes a conservative mapping. If it cannot,
admission stays disabled pending a separate owner policy decision; no limit
value is silently changed.

## 9. Controller-owned retained evidence

All worker evidence crosses explicit bounded pipes to one trusted controller
writer. The worker receives no evidence-directory path, file handle, writable
directory, or general-purpose file endpoint. The writer validates bounded,
versioned records and accounts bytes before each retained write.

| Reserved item | Maximum bytes |
|---|---:|
| `results.jsonl.gz` (including its `.part` while open) | 786,432 |
| `stdout.txt` | 32,768 |
| `stderr.txt` | 32,768 |
| `manifest.json` | 16,384 |
| `resource.json` | 16,384 |
| `failure.json` | 8,192 |
| `sha256.json` | 8,192 |
| Aggregate slack for all remaining accounted files/metadata | 147,456 |
| **Combined ceiling** | **1,048,576** |

The complete allocations are reserved before admission. Every partial,
temporary, intermediate, manifest, log, failure, integrity, and export file
counts against both its per-item reservation and the combined 1-MiB ceiling.
The JSONL writer uses one gzip stream to a same-volume `.part`; it never
retains a second complete raw ledger or export copy. After validation,
flush, close, and hashing, rename within the same volume; account any
simultaneous file bytes and never assume rename itself bounds total
artifacts. Hash exact final bytes with SHA-256 and record source, fixture,
interpreter, environment, evidence, and manifest identities.

The stdout/stderr readers continue draining after retention quotas are
reached but retain no additional bytes. Track emitted when knowable,
read/captured, discarded, and retained counts independently. Bound pipe
records, reader queues, compression buffers, and in-memory summaries.
Reserve failure and integrity capacity before starting. If the next record
or artifact would overflow any cap, stop further records, request
termination, drain/discard bounded input, preserve reserved failure evidence
if possible, classify `ARTIFACT_LIMIT_EXCEEDED` and
`EVIDENCE_INCOMPLETE`, and never truncate mandatory data or report success.
Export is a separately counted write; if it cannot fit, do not export under
this authorization.

This design prevents the worker from writing to the controller evidence
directory only if the token/handle/file-system boundary in §7 is effective.
Pipe byte accounting alone is not filesystem-wide containment.

The 8,196-record gzip ledger is not proven to fit the 786,432-byte result
allocation. The prior design estimates require roughly 5.21:1–21.33:1
lossless compression and are not proven upper bounds. No sizing run is
authorized by this contract. Ledger fit remains a hard prerequisite to a
later synthetic-qualification request; overflow is a failure, not permission
to omit fields or enlarge the allocation.

## 10. Exact future static validation boundary

For a separately authorized corrective source implementation, permitted
checks are limited to:

1. Source/document review.
2. Syntax-only compilation, without import or launch:
   `.\.venv\Scripts\python.exe -m py_compile scripts\luna65_phase2a_supervisor.py`
3. Whitespace/diff checking for tracked edits with `git diff --check`.
   For the untracked source, use a source-only no-index check; record its
   expected difference exit status separately from whitespace diagnostics.
4. Exact changed-file allowlist and checkout-byte SHA-256 identities;
   after independent precommit approval, compare exact staged bytes/Git
   object identity before any publication.

No imports, supervisor entry-point invocation, runtime snippets, tests,
smoke tests, synthetic workers, stress probes, sizing runs, supervisor
qualification, Phase 2A/2B fixtures, datasets, training, scoring, or Spiral
work are authorized. A later source edit after the listed static checks
invalidates those results and requires the same permitted checks again.
Static success is not evidence of Windows API enforcement or operational
correctness.

## 11. Independent reviews and current disposition

The following read-only lanes reviewed the existing proposal/candidate to
identify corrective requirements. These findings are historical inputs,
not approval of this contract. Current R1 exact-byte reviewer outcomes are
recorded in the Luna-0 corrective-contract handoff.

| Lane | Bounded scope | Existing-candidate review result |
|---|---|---|
| A — Windows process admission / Job Object semantics | Suspended process admission, membership, breakaway, memory API semantics | PASS for documented proposal/API design; not implementation or qualification approval. `IsProcessInJob` was not freshly re-fetched in that lane. |
| B — monitoring / termination / controller failure | CPU/wall sampling, watchdog, termination, cessation, bounded failure path | BLOCKED for the current source: no watchdog, unbounded post-budget wait, insufficient separated cessation observation, missing failure classifications/termination reasons. |
| C — restricted environment / filesystem / evidence | Restricted token, direct-write boundary, observer, evidence retention | PASS for proposal-readiness only; external observer, Q03, write-boundary qualification, private-commit reconciliation, ledger fit and dual-controller failure remain blocked. |
| D — governance / provenance / authority | Exact identities, allowlist, status and execution boundaries | PASS for governance boundary. Its note that hashes were not supplied was mistaken; all three expected checkout SHA-256 values were supplied and independently matched. |

The lane-A and lane-C passes are limited to proposal completeness/API
description. Lane-B's implementation findings remain valid. Their blocking
points were used to revise the §5 contract text; this does not imply that
their earlier reviews apply to the revised text.

**Integrated disposition:** **BLOCKED — CORRECTIVE CONTRACT NOT READY FOR
OWNER AUTHORIZATION.** Owner decisions in §2 remain prerequisites even if
the reviewers find this text complete. Any external observer/service/host
change must be separately authorized.

## 12. Proposed explicit corrective implementation authorization

The following wording is **draft language only**, not an authorization:

> I authorize only corrective implementation of
> `scripts/luna65_phase2a_supervisor.py` against the exact revision and
> contract SHA-256 identified in the approved Luna-65 Phase 2A corrective
> implementation handoff. Scope is restricted to the fixed Phase 2A
> supervisor path described in that contract. I authorize only the listed
> nonexecuting source review, `py_compile`, diff/provenance, and exact-byte
> checks. No other source/test/fixture/document is in the implementation
> allowlist unless separately named and approved. This authorization does
> not authorize supervisor invocation, runtime smoke/qualification, token or
> host provisioning outside the approved source's transient operation,
> synthetic/resource/evidence probes, Phase 2A/2B fixtures, datasets,
> training, scoring, benchmark execution, or publication before independent
> precommit approval and exact-byte verification. Authorization Q remains a
> distinct later decision.

This draft may be submitted to the owner only after the integrated contract
disposition is PASS and each decision in §2 has an explicit recorded value
or acceptance. The exact source revision/hash and exact allowed command
remain to be filled from the implementation candidate after review; they
must not be guessed or backfilled as though already authorized.

## 13. Preserved governance boundaries

This is execution-resource and security governance, not a TPCN architecture
change. A01–A15, the architecture contract, and the changelog are unchanged;
QPC is a supervisor clock only and never a neural/event timestep. No ACP is
proposed. The Luna-65 Phase 2 resource policy is unchanged.

**Corrective implementation: NOT YET AUTHORIZED.**

**Supervisor qualification: NOT AUTHORIZED.**

**Phase 2A/2B fixtures: NOT AUTHORIZED.**

**Full Spiral benchmark: BLOCKED.**

**Luna-64 corrective execution: BLOCKED.**

**Luna-63C certification: FROZEN.**

## References

- [CreateRestrictedToken](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createrestrictedtoken)
- [Restricted Tokens](https://learn.microsoft.com/en-us/windows/win32/secauthz/restricted-tokens)
- [CreateProcessAsUserW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasuserw)
- [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [STARTUPINFOEX and PROC_THREAD_ATTRIBUTE_HANDLE_LIST](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information)
- [QueryInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject)
- [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
- [IsProcessInJob](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-isprocessinjob)
- [Event Tracing for Windows](https://learn.microsoft.com/en-us/windows/win32/etw/about-event-tracing)
- [EVENT_TRACE_PROPERTIES](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-event_trace_properties)
