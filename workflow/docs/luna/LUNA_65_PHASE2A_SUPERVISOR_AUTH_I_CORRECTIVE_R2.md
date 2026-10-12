# Luna-65 Phase 2A Supervisor Corrective Contract — R2

**Gate:** `L65-PHASE2A-SUPERVISOR-AUTH-I-CORRECTIVE-R2`

**Status:** **DRAFT FOR INDEPENDENT REVIEW — CORRECTIVE SUPERVISOR
IMPLEMENTATION NOT AUTHORIZED.**

**Disposition target:** **PASS — CORRECTIVE IMPLEMENTATION CONTRACT READY
FOR OWNER AUTHORIZATION**, only if the exact-byte A–D review passes and the
owner decisions requested in §10 are explicitly resolved. Otherwise
**BLOCKED — CORRECTIVE CONTRACT INCOMPLETE**.

This governance-only contract does not modify the supervisor, qualify
Windows enforcement, or authorize any runtime operation. It supersedes
neither the accepted Phase 2A policy nor its previous proposal. The prior
corrective R1 draft and handoff remain unchanged historical evidence.

## 1. Provenance and preserved state

The expected baseline was verified: branch
`governance/luna64-r4.3-freeze-20261010`, `HEAD`
`1d6325f3ca738b32a6ee9e1a5613d2faa9458770`, parent
`d11d370a7c97184529845c9cac984fc22018c576`.

| Artifact | Checkout SHA-256 | State at review start |
|---|---|---|
| `scripts/luna65_phase2a_supervisor.py` (21,494 bytes) | `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1` | Untracked, blocked scaffold |
| `workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_AUTH_I_CORRECTIVE_R1.md` | `4E625C363A239BAB1386E0DE454A11F0F23972BFB5BD9137141946C282750999` | Untracked, historical draft; preserve unchanged |
| `workflow/handoffs/luna-0-luna65-phase2a-corrective-contract-review-r1-20261012.md` | `04B048E42913B26FFCAB6173A94134BF200055F4435C3536ED08F0D32C4A2C00` | Untracked, historical handoff; preserve unchanged |
| `workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_IMPLEMENTATION_AUTH_R1.md` | `31C2CEDAAC91C78A79D746879AEB52759A92335DDA7D18EDC5F0E055F141EA97` | Tracked proposal |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `64AF62CD2E8CD0696BF52EEDF63672FB04399EF949B580FD551360A0F237ED61` | Pre-existing modified CRLF `-text` file |

Do not overwrite or reinterpret the R1 review findings. The source remains
incomplete and unqualified. Its missing admission, controller, evidence,
containment, and bounded-cessation implementation are not enforcement
evidence.

## 2. Frozen requirements and scope

The accepted requirements remain:

| Requirement | Value |
|---|---:|
| Monitored aggregate job user + kernel CPU | 120 seconds |
| Monitored wall budget from controller `T0` | 120 seconds |
| Primary termination request if active | `T0 + 115 seconds` |
| Job-wide memory ceiling | 268,435,456 bytes aggregate concurrent private committed memory |
| Total retained-artifact ceiling | 1,048,576 bytes |
| Retries | Zero |
| Containment | Whole admitted process tree; fail closed |

The sole proposed implementation file remains
`scripts/luna65_phase2a_supervisor.py`. It may implement fixed internal
controller/watchdog/observer modes, but may not invoke a shell or accept an
arbitrary command, executable, working directory, environment, evidence
destination, retry count, or resource limit. Any required helper, installed
service, test/fixture, host ACL change, filesystem quota, or other file
requires separate exact owner authorization. No TPCN production file or
fixture may be changed under this contract.

## 3. Windows admission contract

The sequence below is the source-level requirement. Successful API returns
do not prove effective token restrictions, filesystem isolation, or
qualification.

### 3.1 Restricted primary token

1. Open the trusted controller process token with `OpenProcessToken` for
   `TOKEN_QUERY | TOKEN_DUPLICATE | TOKEN_ASSIGN_PRIMARY |
   TOKEN_ADJUST_DEFAULT | TOKEN_ADJUST_GROUPS |
   TOKEN_ADJUST_PRIVILEGES`. `CreateRestrictedToken` returns a handle with
   the same granted access as its input handle; verify that the resulting
   handle retains the rights needed below. Use `CreateRestrictedToken` with
   `WRITE_RESTRICTED | DISABLE_MAX_PRIVILEGE`; disable every enabled group
   not needed for the fixed interpreter invocation and add a unique
   per-run restricting SID. Never use `SANDBOX_INERT`.
2. Set low integrity with `SetTokenInformation(TokenIntegrityLevel)`,
   requiring `TOKEN_ADJUST_DEFAULT` on the restricted token handle.
   Query back `TokenGroups`, `TokenRestrictedSids`, `TokenPrivileges`,
   `TokenIntegrityLevel`, and token type with `GetTokenInformation`;
   require `IsTokenRestricted` and exact comparison with the controller's
   fixed expected profile. Any extra enabled privilege/group, absent
   restricting SID, or mismatch rejects admission.
   For `AccessCheck`, duplicate the restricted primary token with
   `DuplicateTokenEx` as a `TokenImpersonation` token at
   `SecurityImpersonation` level, with `TOKEN_QUERY`; use only that
   impersonation-token handle for access checks, then close it. Keep the
   restricted `TokenPrimary` handle for `CreateProcessAsUserW`.
3. Use this restricted primary token for `CreateProcessAsUserW`. Microsoft
   documents that `SE_ASSIGNPRIMARYTOKEN_NAME` is not required when the
   token is a restricted version of the caller's primary token. The caller
   still must satisfy `SE_INCREASE_QUOTA_NAME` requirements; enable it only
   if present and authorized. If required privilege/rights are unavailable,
   fail closed. Do not fall back to `CreateProcessW`,
   `CreateProcessWithLogonW`, or an unrestricted token.
4. The exact enabled-group SID list and required interpreter access must be
   frozen in the later invocation profile. They are not inferred from
   “as appropriate”; lack of the owner-reviewed profile blocks admission.

### 3.2 Exact environment

The child environment is constructed, never copied from the caller. The
only permitted names are:

`SystemRoot`, `WINDIR`, `SystemDrive`, `PATH`, `TEMP`, `TMP`,
`PYTHONHASHSEED`, `PYTHONDONTWRITEBYTECODE`, `PYTHONNOUSERSITE`,
`PYTHONSAFEPATH`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD`, and the controller-
generated `TPCN_RESULT_HANDLE`.

`PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONNOUSERSITE=1`, `PYTHONSAFEPATH=1`, and
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`. The OS path values, exact pinned
interpreter PATH, and dedicated non-writable `TEMP`/`TMP` values must be
frozen in the signed invocation profile and hashed into the manifest.
`PYTHONPATH`, `PYTHONHOME`, proxy variables, user-site paths,
`PYTEST_ADDOPTS`, `PYTEST_PLUGINS`, arbitrary `LOCALAPPDATA`, evidence
paths, and every unlisted variable are absent.

Construct a sorted UTF-16LE `NAME=value\0...\0\0` buffer in controller-owned
memory; pass it as `lpEnvironment` to `CreateProcessAsUserW` with
`CREATE_UNICODE_ENVIRONMENT`. Do not call `CreateProcessW` for environment
construction. Free the controller allocation with its matching allocator
(`HeapFree` for `HeapAlloc`, or `LocalFree` for `LocalAlloc`) on every
success/failure path after the create call returns. Record the exact block
digest and reject unexpected values. If the workload cannot operate with
this profile, reject admission; do not widen it.

### 3.3 Pipe inheritance and ownership

Create dedicated anonymous pipes with inheritable security attributes, then
make every controller-side endpoint non-inheritable with
`SetHandleInformation`. `STARTUPINFOEX` uses
`PROC_THREAD_ATTRIBUTE_HANDLE_LIST` containing only child stdin-read,
stdout-write, stderr-write, and the fixed versioned result-write endpoints.
Only those child endpoints remain inheritable; set `bInheritHandles=TRUE`,
`STARTF_USESTDHANDLES`, and the exact stdin/stdout/stderr handles.
The child-side numeric value of the inherited result-write handle is
provided only in the controller-generated `TPCN_RESULT_HANDLE` environment
entry as an unsigned decimal `uintptr_t` string. This generated value is
part of the exact per-run environment profile, not caller input. The worker
must parse it strictly, verify that it identifies an inherited pipe handle,
and write only the frozen Phase 2A JSONL schema: UTF-8 without BOM, LF
terminated, monotonically increasing record sequence, and no record above
4,096 bytes including LF. The controller rejects wrong schema/version,
sequence gaps or duplicates, invalid UTF-8/JSON, and oversized records.
The schema and record payload remain those of the separately accepted
Phase 2A fixture contract; this supervisor contract does not alter them.

The workload uses synchronous anonymous-pipe `ReadFile` calls on exactly
three dedicated controller reader threads, one per stdout, stderr, and
result pipe. Do not request overlapped I/O on anonymous pipes. Each reader
owns its read handle and its single 4,096-byte slot; the controller writer
consumes that slot under the single-producer/single-consumer ownership rule
in §4. On shutdown or failure, stop/job-terminate the workload, close the
controller read handles only after the corresponding synchronous reads have
returned, and join each reader within the finite post-budget deadline. A
reader thread that fails to return by that deadline is
`TERMINATION_UNCONFIRMED` and `EVIDENCE_INCOMPLETE`; do not report EOF.

After `CreateProcessAsUserW` succeeds, immediately close every
controller-held duplicate of a child endpoint. The controller retains only
stdin-write (closed before resume to deliver EOF) and stdout/stderr/result
read endpoints. Close stdin-write before resumption. This is required for
EOF detection; process exit alone does not guarantee pipe EOF while another
write handle remains open. After `CreateProcessAsUserW` returns, whether
successfully or with failure, if the attribute list was initialized, call
`DeleteProcThreadAttributeList` exactly once and free its backing allocation
on every path. On process-creation failure, also close every pipe end and
cancel the evidence reservation;
every later admission-rejection branch closes all handles it owns after
termination/reconciliation. No evidence file/directory, job, watchdog, or
controller handle is inherited.

### 3.4 Create, assign, verify, resume, or reject

The supervisor exposes only the fixed primary invocation plus fixed
watchdog and optional ETW-observer internal modes in this same allowlisted
source file. The primary first samples `T0` with `QueryPerformanceCounter`
and records `QueryPerformanceFrequency`, before starting any helper or
other setup. It creates and configures the workload Job Object and private
channels before launching helpers. The mandatory helper order is: create,
resume, and verify the optional observer first; then create the watchdog
suspended, duplicate and validate all required remote handles, resume it,
and verify readiness. Only after both required helpers are ready may it
create the workload process. It launches each helper only with the pinned interpreter and
exact absolute script path; command lines contain only the fixed
internal-mode selector and generated run nonce, with no shell, dynamic
import string, caller-supplied argument, working directory, or inherited
environment. Create each helper suspended with
`CreateProcessAsUserW`, `CREATE_SUSPENDED |
CREATE_UNICODE_ENVIRONMENT | EXTENDED_STARTUPINFO_PRESENT`, and a
`STARTUPINFOEX` explicit handle list containing only the private
control-channel endpoints and, for the watchdog only, its caller-status
write endpoint. Every listed source handle is explicitly inheritable,
`bInheritHandles=TRUE` is passed to `CreateProcessAsUserW`, and no
pseudo-handle is listed; only the listed handles are inherited. The
watchdog and observer receive separately
constructed exact UTF-16LE environments from the frozen helper profile;
they receive no worker result handle, evidence path, or unrelated
inheritable handle. Create one local message-mode caller-status named pipe
before the watchdog, with a protected DACL for the invoking caller and this
run's watchdog, remote clients rejected, overlapped I/O, and requested
buffers no larger than 1,024 bytes. Only the watchdog receives its
inheritable write handle in its explicit handle list and is the sole status
writer; `bInheritHandles=TRUE` is mandatory. The primary sends
success/failure and final commit details to the watchdog over the private
channel. The watchdog emits exactly one UTF-8 JSON status record no larger
than 1,024 bytes, using one overlapped write bounded by the absolute
observation deadline, then closes the status handle; the caller requires
one valid record followed by EOF. A success record is permitted only after
the watchdog validates the commit and observes the primary process signaled
with the expected successful exit code. EOF without a valid record or a
malformed, oversized, duplicate, incomplete, or timed-out record is
supervisor failure.
The primary receives
only the owner-approved supervisor invocation profile and evidence
destination. Close every
controller-held duplicate of helper child endpoints immediately after
creation, retain only the intended peer endpoints, and close all unused
pipe ends before resuming the helper. Create the watchdog suspended with
only its private control-channel and caller-status handles in its inherited
handle list. While it is suspended, the primary uses `DuplicateHandle` to
place the exact preconfigured workload Job Object handle and exact primary
process handle into the watchdog with their required minimal rights; when
Q03 is selected, it also duplicates the exact observer process handle.
These handles are remote duplicates, not inherited handles in the watchdog's
startup list. The watchdog validates all received handle values, the
primary PID/creation time, the job configuration, and the optional observer
identity before readiness. The primary transmits the target-process handle
values and startup record over the private channel before resuming the
watchdog. For every initialized helper
`STARTUPINFOEX` attribute list, call `DeleteProcThreadAttributeList` once
after the process-creation call returns on both success and failure, then
free its backing allocation; close all created helper handles on every
rejection path. The watchdog must be running and
ready before workload process creation; the optional observer must be
running and ready before workload process creation when Q03 is selected.
The helpers are not assigned to the workload Job Object. Verify
`IsProcessInJob(helper, workloadJob, &inJob) == FALSE` for each exact
created process handle. Any helper launch, identity, environment, or handle
check failure aborts admission and prevents workload creation/resumption.
The exact helper token profile, enabled groups/privileges, ETW privilege
requirements, and helper environment values must be frozen in the
owner-reviewed invocation profile; until then this is an explicit profile
blocker, not an assumed trusted boundary.

1. Complete identity, environment, ACL, evidence reservation, pipe, and
   controller-time setup before creating any helper or workload process.
   Prepare the optional observer configuration, but do not start the
   observer until the workload Job Object has been fully configured in
   item 2. No workload process may be created until the selected observer
   and the watchdog have each completed their startup/readiness handshake.
2. Create and fully configure a fresh unnamed Job Object with a restrictive
   security descriptor and non-inheritable handle before creating either
   helper. Set exactly
   `JOB_OBJECT_LIMIT_JOB_MEMORY | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`;
   leave `JOB_OBJECT_LIMIT_BREAKAWAY_OK` and
   `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK` unset. Associate the completion
   port and read back the configured values.
   If Q03 observer coverage is selected, create the observer suspended
   under the frozen helper profile, close all unused pipe ends, resume it
   exactly once, and require its `OBSERVER_READY` acknowledgment and live
   heartbeat before proceeding. If readiness fails, stop/reap the observer
   and abort without creating a workload process.
   Then create the watchdog suspended with only its private
   control-channel and caller-status endpoints. Retain its exact process
   handle. While it remains suspended, duplicate the exact primary process
   handle and configured workload Job Object handle into it, and, when
   selected, duplicate the exact observer process handle as well. Transfer
   all resulting remote handle values and the immutable startup record
   over the private channel. The watchdog validates the primary identity,
   job configuration, and optional observer identity/handle before it is
   resumed. Resume the watchdog exactly once and require its readiness
   acknowledgment within 100 ms of watchdog process creation. The primary
   continues monitoring the observer while the watchdog starts. Any
   duplicate, identity, handle, readiness, or heartbeat failure aborts
   admission and prevents workload creation.
   The primary sends the watchdog one immutable, versioned startup record
   containing `controller_T0_qpc`, the recorded QPC frequency, the
   configured deadlines, and a run nonce over the private startup channel
   before watchdog readiness. The watchdog validates the record schema,
   nonce, frequency, monotonic deadline arithmetic, and the pinned primary
   identity, then acknowledges the exact record digest and deadline values.
   Missing, duplicate, malformed, inconsistent, or unacknowledged startup
   state is controller failure: the watchdog does not report readiness and
   the primary does not create or resume the workload. Both controllers
   use the same QPC time base and frequency for deadline comparisons; the
   watchdog does not start its wall clock on receipt.
   After the job, channels, evidence reservation, and any selected observer
   are initialized, the primary resumes the watchdog before any workload
   process creation. The primary must receive the readiness
   acknowledgement within 100 ms of watchdog process creation; the watchdog
   must receive and validate the startup record within the same interval.
   Expiry is `WATCHDOG_STARTUP_TIMEOUT`: the watchdog exits with failure,
   the primary aborts admission, and no workload process is created.
   The 115-second early-stop deadline bounds all remaining pre-admission
   setup. If no workload has been admitted by `T0 + 115 seconds`, the
   watchdog closes its admission gate, records
   `ADMISSION_DEADLINE_EXCEEDED`, and rejects every subsequent
   `RESUME_INTENT`; it does not issue the primary's 115-second workload
   termination request. The primary owns that request and must stop setup,
   terminate any assigned suspended process, and must not create or resume a
   workload after the deadline. If the primary stops responding while an
   assigned process remains, the ordinary 100 ms stale-primary path makes
   the watchdog terminate the job.
   Admission state is a primary-authored, monotonically sequenced protocol:
   `SETUP`, `SUSPENDED_ASSIGNED`, `RESUME_INTENT`, `ADMITTED`, or `CLOSED`.
   Before calling `ResumeThread`, the primary sends `RESUME_INTENT` and
   requires the watchdog to acknowledge the same run nonce and state
   sequence while its gate remains open. It then rechecks local QPC
   immediately before the call. At `T0 + 115 seconds`, the primary
   atomically closes its own admission state; the watchdog closes its gate
   at that same QPC deadline. A transition racing the deadline is not
   permission to continue: if `ResumeThread` returns after the deadline,
   record the admission and immediately request termination; report wall
   overrun. Duplicate or out-of-order state sequence numbers are protocol
   failures, not refreshed admission permission.
   When Q03 observer coverage is selected by the owner, the observer startup
   in item 2 must acknowledge `OBSERVER_READY` within 100 ms of observer
   process creation, reporting the run nonce, session identity, successful
   `StartTraceW`/provider-enable/consumer-start status, enabled process
   start-key property, event-clock configuration, and initial
   `ControlTraceW` loss counters. The primary accepts readiness only if all
   statuses succeed and initial lost-event counters are zero. Missing,
   late, malformed, or failed readiness aborts admission; no workload
   process is created or resumed. If the owner has not selected Q03 observer
   coverage, do not start ETW and do not claim Q03 detection/recovery.
   During an enabled Q03 run, observer readiness remains live: it sends
   sequenced heartbeat/loss-counter records every 20 ms to both primary and
   watchdog. A lost event, nonzero loss counter, failed `ProcessTrace`,
   observer process exit, or missing/stale heartbeat is an immediate Q03
   coverage failure. The primary closes admission or terminates the active
   job; the watchdog independently terminates an admitted job if it detects
   observer loss. There is no silent continuation with Q03 coverage absent.
   Before `CreateProcessAsUserW` and again immediately before `ResumeThread`,
   the primary samples QPC and requires the 115-second early-stop deadline
   not yet to have elapsed. If either check is at or beyond `T0 + 115
   seconds`, reject admission; if a suspended process already exists,
   terminate it and confirm cleanup without resuming it. Sample QPC again
   immediately after a successful `ResumeThread`; if the deadline crossed
   during the call, record admission and request whole-job termination
   immediately. The primary owns the 115-second wall-stop and cumulative
   CPU-limit requests; the watchdog owns the independent 120-second
   escalation and stale-primary requests. Actual cessation after a deadline
   is an observed overrun, not an extension of the budget.
   Build the worker identity with a unique restricting SID and
   `WRITE_RESTRICTED`; grant no filesystem or registry write ACE to that
   per-run SID. Before resume, read back ACLs for the exact interpreter,
   libraries, fixture, checkout, `TEMP`/`TMP`, and evidence paths and use
   `AccessCheck` with the restricted token for required access. For each
   object type, define its `GENERIC_MAPPING`, call `MapGenericMask` on the
   desired access mask, and require the API call to succeed separately
   from the returned `AccessStatus`: required read/execute probes must be
   granted; prohibited write probes must be denied. An API failure or
   unexpected status rejects admission. Reject
   unexpected writable paths and inherited writable handles. `AccessCheck`
   uses the restricted impersonation-token duplicate described in §3.1,
   not the primary token. This is a default-deny design requirement, not
   proof of a whole-machine sandbox;
   alternate filesystems, reparse/hard-link paths, registry objects, and
   target-host effective access remain qualification obligations.
3. Retain and verify the exact watchdog process handle returned at its
   creation; use that handle as the target-process handle for duplication
   and to observe/terminate only that watchdog instance.
   Duplicate the exact primary process handle into the watchdog with
   `PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_TERMINATE | SYNCHRONIZE`;
   the watchdog retains and waits on this handle, never reopens primary by
   PID, and may use that same verified handle for bounded
   `TerminateProcess` if finalization exceeds its deadline. Call
   `DuplicateHandle(GetCurrentProcess(), intendedJob, watchdogProcess,
   &remoteJob, JOB_OBJECT_QUERY | JOB_OBJECT_TERMINATE | SYNCHRONIZE,
   FALSE, 0)`. Convey the returned target-process handle value through the
   private bounded startup channel. The source/target process handles must
   grant `PROCESS_DUP_HANDLE`; record the source job identity, requested
   rights, returned value, and transfer acknowledgment. This duplication
   creates a handle to the same kernel job object; a successful API call
   from the intended source handle is the identity link. The watchdog
   verifies the received handle by querying expected job limits/accounting
   before readiness. The observer receives no job handle. When the observer
   is enabled, the primary retains the exact observer process handle returned
   at creation and duplicates that same handle into the watchdog with
   `PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_TERMINATE | SYNCHRONIZE`;
   the watchdog never reopens the observer by PID. Verify and record the
   duplicated handle and observer identity before readiness so either
   trusted controller can stop/reap the observer on failure. The observer
   sends correlated live process identities to the primary; the primary
   opens each live process with
   `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE)` and
   performs targeted membership checks with its
   original intended-job handle.
4. Prepare the workload `STARTUPINFOEX` attribute list with both
   `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` and
   `PROC_THREAD_ATTRIBUTE_JOB_LIST`; the job-list value contains only the
   already configured intended workload Job Object. Windows supports this
   creation-time job association beginning with Windows 10 version 1709.
   Require the pinned target OS to support this attribute. If the attribute
   is rejected or target support is not established, fail admission; do not
   fall back to creating an unassigned process and later calling
   `AssignProcessToJobObject`.
5. Call `CreateProcessAsUserW` with the restricted primary token, exact
   absolute `lpApplicationName`, exact command line/current directory,
   constructed environment, explicit handle list, and
   `CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT |
   EXTENDED_STARTUPINFO_PRESENT`, `bInheritHandles=TRUE`, and both
   attribute-list entries above. Job association is applied as part of
   process creation. Do not claim admission until the exact returned root
   handle passes the intended-job membership and PID-list checks below. On
   stale-primary detection in any state, the watchdog immediately requests
   `TerminateJobObject` without waiting for the primary, then terminates the
   primary through its retained exact process handle if still alive. It
   waits at most 100 ms for the primary handle to signal; after it signals,
   the watchdog re-queries the entire job and
   terminates it again if any member exists. It never assumes the job is
   empty from a stale admission-state message. This also covers a suspended
   root created before the primary could publish its process information.
   No fixture code runs while suspended.
6. On the root process handle, call `IsProcessInJob(root, intendedJob, &inJob)` and
   require success and `inJob == TRUE`. A call with `hJob == NULL` answers
   only membership in any job and is not acceptable for this check.
7. Query `JobObjectBasicProcessIdList` and
   `JobObjectBasicAccountingInformation`; require the suspended root PID
   in the intended job's PID list and `ActiveProcesses` equal to that
   list's count. Query/read back effective job memory and breakaway flags.
   Verify watchdog and observer are not members of the intended workload
   job, using `IsProcessInJob(process, intendedJob, &inJob)`; enclosing-job
   membership must be separately recorded and cannot be called proof that
   they are outside all jobs.
8. Only after all checks succeed, call `ResumeThread` exactly once. The
   return must be exactly `1`, the prior suspend count for the one
   `CREATE_SUSPENDED` increment. `-1`, `0`, or any value above `1` is an
   admission failure: do not claim admission, terminate the intended job,
   observe/reconcile exit, and classify containment/evidence failure as
   appropriate. A zero return means the thread was already runnable and
   may have executed; terminate immediately and never report that fixture
   code did not execute. Immediately before the call, save the successful
   `JobObjectBasicAccountingInformation` counters as
   `workload_cpu_baseline_user_100ns` and
   `workload_cpu_baseline_kernel_100ns`. Record
   `workload_admission_qpc` only after return value `1`. Monitored CPU usage
   is `(current.TotalUserTime - baseline_user) +
   (current.TotalKernelTime - baseline_kernel)`, converted from 100-ns
   units to seconds without floating-point accumulation. The final
   post-cessation query uses the same baseline. A current counter below its
   baseline, any regression, failed query, or missing baseline is
   `RESOURCE_MEASUREMENT_INCONCLUSIVE`. This defines CPU budget origin as
   workload admission and excludes suspended setup time; all setup remains
   inside wall time.

Any failure before process creation: close all allocated environment,
attribute-list, pipe, job, watchdog, and observer handles and release
reserved evidence without claiming a workload launch. Any process-creation
failure closes all child/parent pipe endpoints and frees environment and
attribute-list storage. Any failure after the suspended, creation-time
job-associated root exists: request `TerminateJobObject` and also request
`TerminateProcess` through the exact root process handle returned by
`CreateProcessAsUserW`; this covers a failed/mismatched job-membership check
without reopening by PID. Record both API calls and their results. Wait on
that exact root handle with `WaitForSingleObject`, then require successful
job accounting and complete PID-list reconciliation with zero active
members. Never resume on any admission failure. If cleanup or exit
cannot be confirmed, record `TERMINATION_UNCONFIRMED` and
`EVIDENCE_INCOMPLETE`; no success result.

After the workload is absent/confirmed stopped on every abort path, the
primary sends bounded sequenced `ABORT`/`STOP` messages to every started
helper and requires acknowledgment plus process exit within 100 ms. An
enabled observer must stop/flush its ETW session and report final loss
counters before exit. If an observer is unresponsive, the watchdog or
primary uses its retained process handle (never a PID reopen) to request
`TerminateProcess`, waits up to 100 ms, and separately records the request
and exit observation; the supervising controller also issues
`ControlTraceW(sessionName, properties, EVENT_TRACE_CONTROL_STOP)` for the
identified session and verifies the query/stop result. The same
stop-and-reap rule applies to the watchdog after the job is empty. Do not
close helper process handles
until their process objects are signaled. If a helper cannot be stopped and
reaped within the bound, retain its exact handle while possible, report
`TERMINATION_UNCONFIRMED`/`EVIDENCE_INCOMPLETE`, and do not claim a clean
shutdown. Closing a process handle alone is never reported as stopping or
reaping the helper.

## 4. Evidence writer and retained artifacts

Select exactly one trusted writer: the primary controller process is the
exclusive owner of all retained files and the only process allowed to
create, append, rename, hash, or export them. Watchdog and observer send
bounded, versioned messages to this controller; they do not write files.
The worker can only write into bounded stdout/stderr/result pipes. This
selection keeps a single ownership authority, but it does not make evidence
survive controller-process failure. The watchdog sends bounded nonblocking
or overlapped control records; it never blocks waiting for the writer.
The primary's heartbeat includes the latest CPU-sample QPC/sequence and
writer state (`IDLE` or `BUSY`), operation-start QPC/sequence, and
last-completed-write QPC/sequence. When the watchdog detects primary
process-death, stale sample, or stalled-writer progress, it records
`failed_component=PRIMARY_CONTROLLER` and `detected_by=WATCHDOG`, plus
aggregate `CONTROLLER_FAILURE`. It treats writer progress older than 100 ms
as failure only while the writer reports `BUSY`; an idle writer is monitored
by the independent primary heartbeat, not by an advancing file-write
counter. A failed bounded send records sender, intended receiver, and
detector; the opposite endpoint independently records a stale/missing
heartbeat if observed. Neither authority may block waiting for that
channel. Every controller-failure event must include
`failed_component`, `detected_by`, source-local sequence, QPC, and trigger;
`CONTROLLER_FAILURE` is an aggregate class and is never emitted without
those attribution fields. When the primary detects watchdog death or a response older than
100 ms, it records `failed_component=WATCHDOG` and
`detected_by=PRIMARY_CONTROLLER`, plus aggregate `CONTROLLER_FAILURE`, and
requests whole-job termination. The watchdog holds a non-inheritable
duplicate of the intended
Job Object handle with only
`JOB_OBJECT_QUERY | JOB_OBJECT_TERMINATE | SYNCHRONIZE` rights; the primary
retains the original. Dual-controller hang remains an unqualified failure
case.

All watchdog, observer, acknowledgment, and control traffic uses at most six
directed bounded channels: primary-to-watchdog and watchdog-to-primary,
primary-to-observer and observer-to-primary, and watchdog-to-observer and
observer-to-watchdog, omitting observer channels when Q03 is disabled. Each
direction permits at most 16 outstanding messages, including any in-flight
message, with a maximum encoded size of 1,024 bytes per message. The 16
fixed slots include serialization, transport, and receive parsing; do not
copy a message into a second queue. Across all six directions, message
storage is at most 98,304 bytes. Sending is nonblocking. A full queue,
oversized or malformed message, or failed send is a controller/protocol
failure: do not drop or overwrite a message; close admission and request
whole-job termination if a workload process is assigned or admitted. If
observer event records cannot fit their bounded channels, classify observer
event loss as `PROCESS_CONTAINMENT_FAILURE` and terminate rather than
silently dropping the evidence.

Implement each directed control channel as a distinct local named-pipe
instance created with `CreateNamedPipeW` using
`PIPE_ACCESS_DUPLEX | FILE_FLAG_OVERLAPPED`,
`PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT |
PIPE_REJECT_REMOTE_CLIENTS`, and requested inbound/outbound buffers no
larger than 1,024 bytes. Use a protected DACL limited to the exact trusted
controller/helper identities in the run profile, unique per-run pipe names,
and authenticate each connection with the run nonce and process identity.
Issue at most one overlapped read and one overlapped write per direction;
use `GetOverlappedResult` to retire each completed operation. Cancel pending
operations with `CancelIoEx`, wait for their completion, and close each
event/pipe handle once during shutdown. The API buffer-size parameters do
not establish exact kernel allocation; do not claim they enforce a physical
memory limit. The application queue/message limits above are hard source
requirements. A channel setup, ACL, authentication, cancellation, or
operation-completion failure is fail-closed.

The controller writer must:

- Reserve the complete 1,048,576-byte aggregate budget before admission.
  Preserve the accepted sub-reservations: compressed result ledger 786,432;
  stdout 32,768; stderr 32,768; invocation manifest 16,384; resource
  record 16,384; failure record 8,192; SHA-256 manifest 8,192; and remaining
  aggregate slack 147,456 bytes.
- Drain stdout, stderr, and the result pipe concurrently from before
  `ResumeThread` until all reach EOF, using exactly one dedicated reader
  thread per synchronous anonymous pipe so backpressure on one pipe cannot
  prevent draining the others. Each stream has one reader as the sole producer and one serialized
  writer as the sole consumer of a single 4,096-byte slot. The reader owns
  the slot while filling it; after publishing a completed chunk, it cannot
  reuse or overwrite the slot until the writer releases it. The writer
  consumes that slot in place and does not copy its payload into another
  queue. The slot is also the stream's sole synchronous `ReadFile` buffer;
  do not make another unaccounted copy. Result-line assembly uses
  one additional 4,096-byte buffer, which accepts arbitrary pipe chunk
  boundaries and rejects a line exceeding 4,096 bytes including LF.
  Compression consumes one complete validated line at a time from that
  buffer and writes into one 8,192-byte output buffer; enforce that output
  bound for every call, including finalization. The compressor must use a
  fixed, source-declared internal-memory bound and bounded allocator; an
  allocator request above that bound fails closed before allocation.
  Dedicated synchronous readers need no overlapped-I/O buffers. Set each
  anonymous-pipe buffer request to 4,096 bytes and account requested kernel
  pipe storage separately; because `CreatePipe` does not provide a query
  proving exact kernel allocation, that storage size is not represented as
  a qualified physical-memory bound. Application-owned staging is bounded
  to 24,576 bytes total: 12,288 bytes for three reader slots, 4,096 bytes
  for result-line assembly, and 8,192 bytes for compressor output, plus the
  declared fixed compressor state. Any unavailable/enforced allocator bound
  is an implementation blocker, not permission to allocate without bound.
  Each source has independent byte, record, and
  high-water accounting. A
  reader or writer stall, queue overflow,
  malformed result record, or output-allocation overflow requests whole-job
  termination, marks `ARTIFACT_LIMIT_EXCEEDED` or
  `EVIDENCE_INCOMPLETE` as applicable, and records the failed component.
  A blocking `ReadFile` with an outstanding read is a valid waiting state,
  not a stall. Each reader records its thread state and QPC/sequence on
  every read completion and immediately issues the next read. Reader thread
  exit, read failure other than recognized EOF, queue failure, or failure to
  issue the next read within 100 ms of a successful read completion is
  `PIPE_READER_FAILURE`; the primary requests whole-job termination. The
  primary checks reader-thread handles and state at each 10 ms supervision
  cycle. EOF is accepted only as a completed stream after the process/job
  shutdown protocol, not as evidence that mandatory records were retained.
  Continue servicing all three pipes only as needed to avoid deadlock, while
  counting any bytes that cannot be retained as unretained; never silently
  truncate or describe incomplete capture as success. Concurrent drain is
  required for the result pipe as well as stdout/stderr; process exit alone
  does not establish result-stream completeness.
- Validate every bounded JSONL record against the fixed schema/order and
  account its exact bytes before writing. Before each append to any retained
  artifact, compute the exact bytes to be written and check both that item's
  remaining reservation and the aggregate current high-water plus the new
  bytes; do not issue the write if either check would exceed its cap.
  Stream one lossless gzip output to a same-volume `.part`; no raw full-ledger
  copy. For each compressor output chunk, check the exact compressed byte
  count before writing. Apply the same pre-write rule to stdout, stderr,
  invocation/resource/failure manifests, hashes, temporary files, and any
  export.   Reserve 8,192 bytes within the result-ledger allocation for gzip
  finalization output before accepting result data; also preserve the
  separately allocated mandatory failure/hash records. Account every
  finalization chunk before write. If a chunk, trailer, or mandatory record
  cannot fit, do not write beyond budget; stop the workload, preserve
  already verified evidence where possible, and classify
  `ARTIFACT_LIMIT_EXCEEDED`/`EVIDENCE_INCOMPLETE`. Account `.part`,
  metadata, hashes, failure records and any export in the same retained
  high-water total. Rename only after a successful flush/close and
  integrity check; record simultaneous file-size high-water. Rename must
  not create a second file copy. No export unless separately budgeted within
  the same ceiling.
- Write an invocation manifest before admission; include exact command,
  revision, source/fixture/interpreter identities, environment digest,
  policy constants, and output profile. Write resource and failure records,
  then hash exact final retained bytes into the reserved SHA-256 manifest.
  `sha256.json` lists all other final artifacts and explicitly excludes its
  own bytes to avoid recursive self-hashing. Hashing/manifest finalization
  is part of evidence commit, not a second unaccounted copy. Keep the
  watchdog alive and heartbeating through stream EOF, evidence flush/close,
  hash completion, and atomic final-path commit. Only after that commit, the
  primary sends a bounded `EVIDENCE_COMMIT` control record with its QPC and
  final status; the watchdog acknowledges that exact sequence, then closes
  its duplicated job handle and exits. If the primary stalls or exits during finalization,
  the watchdog reports controller failure and does not acknowledge success.
  The `final_evidence_commit_qpc` is the primary's post-commit QPC sent in
  this control record and returned in the caller-facing supervisor status;
  it is not embedded in or self-hashed by the already committed artifact
  set. Preserve that status record within the caller's separately governed
  result channel; it is not an additional retained supervisor file.
- Preserve mandatory records. If the next required record cannot fit, stop
  the workload and report incomplete evidence; do not drop records, enlarge
  allocations, or claim success.

If a writer operation fails, the controller requests whole-job termination,
records `EVIDENCE_INCOMPLETE`, and attempts only bounded reserved failure
finalization. If the writer process itself exits or becomes unavailable,
the watchdog terminates the workload; no other process becomes a second
writer. The run is failed and evidence incomplete. A durable failure
manifest cannot be promised after writer death, storage failure, or power
loss; the process exit/observer evidence is not substituted for a committed
manifest. If the writer stalls, the watchdog detects the stale writer
progress record and terminates the workload. If the primary/writer exits,
the watchdog detects process exit, terminates the workload, and returns a
failure status to its invoker. It never becomes a second file writer.
Failure of both trusted processes remains an unqualified failure case;
kill-on-last-handle-close is a fallback, not observed cessation.

The known 8,196-record ledger is not proven to fit the allocation. The
existing proposal explicitly places a synthetic sizing case before Phase 2A
implementation or execution. That gate remains a separate owner-authorized
qualification prerequisite; it is not evidence that the writer's source
implementation is correct and must not be run under this governance task.

## 5. Memory semantics

### 5.1 Selected Windows control and observations

The specified enforcement candidate is
`SetInformationJobObject(JobObjectExtendedLimitInformation, ...)` with
`JOBOBJECT_EXTENDED_LIMIT_INFORMATION.BasicLimitInformation.LimitFlags`
including `JOB_OBJECT_LIMIT_JOB_MEMORY` and
`JobMemoryLimit = 268435456`, read back with
`QueryInformationJobObject` before resume. Configure
`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` separately in the same flags. A
configured job limit prevents further commit charge to the job beyond the
configured job memory limit; it is not a per-process or working-set cap.

Record `PeakJobMemoryUsed` as the Job Object's peak memory usage for its
processes. Separately sample each member's
`PROCESS_MEMORY_COUNTERS_EX.PrivateUsage` via `GetProcessMemoryInfo`;
Microsoft documents `PrivateUsage` as the process's commit charge (total
private memory the memory manager committed for that process). Take a
complete initial `JobObjectBasicProcessIdList` and active count; if the
returned PID list is truncated, repeat with sufficient capacity until
`NumberOfProcessIdsInList == NumberOfAssignedProcesses`, and require that
complete count to equal `ActiveProcesses` from
`JobObjectBasicAccountingInformation`. Open one `PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE` handle per
listed member, and capture
`GetProcessId` plus `GetProcessTimes` creation time on each exact handle.
Query each handle's `PrivateUsage`, bracketing the query with QPC samples.
Then query the job PID list and active count again, again requiring a
complete non-truncated list and equality between its complete count and
`ActiveProcesses`. Require identical member PID sets/counts; for every
listed PID, reopen a query handle and
require its `GetProcessId` and `GetProcessTimes` creation time to match the
captured identity and require `WaitForSingleObject(handle, 0) ==
WAIT_TIMEOUT` using its `SYNCHRONIZE` right. Require
successful queries and a total first-query-start to last-query-end span no
greater than the 10 ms monitor interval. Otherwise mark
`MEMORY_MEASUREMENT_INCONCLUSIVE` and immediately request whole-job
termination. Record every per-process value, handle identity, QPC interval,
query result, and aggregate sample span.

Even a stable-membership sum within 10 ms is a **sampled sum over an
interval, not an atomic simultaneous snapshot**. Label it as diagnostic;
do not claim it proves the accepted concurrent private-commit ceiling was
met. If a complete sampled sum is at or above 268,435,456 bytes, immediately
request whole-job termination and record
`PRIVATE_USAGE_SAMPLED_SUM_THRESHOLD_REACHED`; do not claim that this
sample alone proves the exact concurrent metric. A sampled sum below the
threshold likewise does not prove compliance between samples. The metric
equivalence/enforcement blocker in §5.2 remains controlling. Any missing
PID, failed `OpenProcess`/memory query, identity mismatch, or query failure
invalidates the sample and prohibits a pass.

### 5.2 Accepted-metric discrepancy — owner-policy blocker

The accepted policy is the sum of concurrent member `PrivateUsage` values.
Microsoft documentation describes `JobMemoryLimit` as virtual memory that
can be committed for the job and `PeakJobMemoryUsed` as peak memory usage of
all processes associated with the job. It does **not** define `JobMemoryLimit`
or `PeakJobMemoryUsed` as the exact sum of the per-process
`PROCESS_MEMORY_COUNTERS_EX.PrivateUsage` values, nor specify equality,
inclusion/exclusion, or accounting synchronization for that sum.

Therefore this contract does not claim that the selected job limit enforces
the accepted private-commit metric. Keep the mismatch as an explicit owner
policy blocker. The owner must either (a) accept the Job Object job-commit
charge as the enforcement metric with the existing byte threshold and
preserve private-usage sum as a separately reported diagnostic, or (b)
retain the exact private-commit acceptance and require a documented,
conservative enforcement mapping before implementation is authorized. No
silent metric substitution is allowed. Runtime comparison is qualification
evidence, not a substitute for an authoritative semantic definition.

## 6. Monitoring, termination, and cessation

### 6.1 Separate time points

Record QPC and frequency. Keep these immutable timestamps distinct:

1. `controller_T0_qpc`: trusted primary entry, before setup.
2. `workload_admission_qpc`: successful `ResumeThread` observation.
3. `termination_request_qpc`: one record per actual `TerminateJobObject`
   call, with authority, reason, sampled CPU/wall, return and Win32 error.
4. `job_completion_observation_qpc`: the first QPC at which a successful
   job-accounting query reports `ActiveProcesses == 0` and a complete job
   PID-list query reports zero members, paired with the immediately prior
   successful QPC sample that observed an active member. Report that
   observation interval, not an exact physical exit time.
5. `final_evidence_commit_qpc`: sampled by the primary immediately after
   all bounded streams are drained, required files are flushed/closed,
   hashes/manifests are finalized, and final paths are committed. The
   primary sends this QPC and final status to the still-live watchdog over
   the private channel, which emits the caller-facing result; it is not
   embedded in or self-hashed by the already committed artifact set.

The cited Microsoft Job Object documentation describes the job handle
becoming signaled when all associated processes terminate because an
end-of-job time limit was exceeded; this supervisor does not set that limit
and must not use a signaled job handle as its completion condition.
Workload-job completion requires all of: a successful
`QueryInformationJobObject(JobObjectBasicAccountingInformation)` with
`ActiveProcesses == 0`; a complete `JobObjectBasicProcessIdList` with zero
members; all known member process handles signaled; all controller-held
child-write endpoints closed; and stdout/stderr/result reader threads at
EOF. Record `job_completion_observation_qpc` at the first successful
accounting/PID-list reconciliation that confirms zero members, paired with
the immediately preceding successful QPC sample that observed an active
member. Report this interval, not an exact physical exit time. `WaitForSingleObject`
on the job handle, `TerminateJobObject` success, completion-port messages,
or root-process exit alone do not establish job completion.
If ETW is enabled, it must additionally reconcile all correlated descendants
as exited with no event loss. `TerminateJobObject` success, completion-port
messages, or root-process exit alone do not establish job completion.

After confirmed cessation, take the required final CPU query using the
admission baseline from §3.4. Then stop the observer with a sequenced
command; within 100 ms require it to stop/flush the ETW session, report
final event-loss counters, and exit. Drain all streams to EOF, close their
handles, and require all reader threads to exit within the
owner-approved post-budget observation deadline. The primary writer then
flushes/closes and commits the reserved artifacts and hash manifest.
Immediately after successful final-path commit, record
`final_evidence_commit_qpc` and send `EVIDENCE_COMMIT` with the same
sequence/QPC/status to the watchdog over the private channel. The watchdog
validates the record and acknowledges the same sequence within 100 ms.
Only after that acknowledgment does the primary close every remaining
workload, process, thread, pipe, job, observer, watchdog, and
control-channel handle exactly once, then exit with success only if every
required close succeeds. The watchdog retains its exact primary process
handle, waits for it to signal, and checks its exit code; it emits the sole
caller-facing success record only after observing the primary's successful
exit and validating the committed evidence status. A primary cleanup
failure, missing acknowledgment, failed ETW stop/flush, unexpected
controller exit, writer stall, unsuccessful primary exit, or handle-close
failure makes the run `EVIDENCE_INCOMPLETE`/`CONTROLLER_FAILURE`; do not
report success. A missing or unsuccessful primary exit by the finalization
cutoff is failure even if `EVIDENCE_COMMIT` was received. When ETW was not
enabled, observer shutdown is not applicable but all other handle-closure
requirements remain. The watchdog must remain available through evidence
commit, primary cleanup, and primary exit; receipt of `EVIDENCE_COMMIT`
alone is never a successful shutdown condition.

At each monitor sample (target 10 ms; gaps above 100 ms are inconclusive),
query cumulative user/kernel time from
`JobObjectBasicAccountingInformation`, subtract the saved pre-resume
baseline in each component, and sum the nonnegative deltas. At `>= 120
seconds` of admission-relative aggregate CPU while active,
request whole-job termination immediately. At `T0 + 115 seconds`, request
termination if active. At `T0 + 120 seconds`, the independent watchdog
requests escalation if active. These are requests, not proof of cessation.
Any final observed admission-relative CPU delta `> 120 seconds` is
`CPU_BUDGET_EXCEEDED`; report its raw total and overshoot. If any required
query fails, counters regress, or sample gap exceeds 100 ms, classify
`RESOURCE_MEASUREMENT_INCONCLUSIVE`, request termination, and do not report
the CPU budget passed. If cessation is not confirmed by the owner-approved finite
post-budget deadline, report the latest successful sample and explicitly
mark final CPU accounting unavailable; do not infer a pass from that
sample. Once cessation is confirmed, take and record one final successful
`JobObjectBasicAccountingInformation` query, subtracting the same admission
baseline, before classifying CPU usage.
This post-cessation query is required even if the last periodic sample was
recent. If it fails, regresses, or cannot be reconciled with the terminated
job, classify `RESOURCE_MEASUREMENT_INCONCLUSIVE`; do not report CPU-budget
compliance.
There are zero retries of the workload. The primary owns CPU-threshold,
115-second and local-failure requests; the watchdog owns heartbeat-loss,
primary-death and 120-second escalation requests. Each authority increments
its own monotonic request sequence and records every actual API call,
including duplicates. The same mandatory request record applies to every
`TerminateJobObject` and `TerminateProcess` call, including pre-assignment
cleanup and Q03 recovery: record API, authority, reason, exact target job or
process instance, request QPC, source-local sequence, return value and
Win32 error. The writer assigns an ingest sequence to each received record
and retains source, source sequence, trigger, QPC and API result.
Cross-authority ordering is by recorded QPC then writer ingest sequence,
never by an invented total order. Termination API errors and all later
observations are separately recorded.

The liveness protocol is symmetric and sequence-based. While setup or a run
is active, each controller sends a heartbeat every 20 ms containing run
nonce, sender-local sequence, state, and QPC; primary heartbeats additionally
include the latest CPU-sample sequence/QPC and each reader's state. When Q03
observer coverage is enabled, the observer is a third peer: it sends
heartbeats to both primary and watchdog every 20 ms, including ETW session
state, `ProcessTrace` status, current loss counters, and last processed-event
QPC. Each receiver acknowledges each accepted heartbeat with the matching
nonce, sequence, and its own QPC. Freshness is measured from the receiver's local
QPC sampled when the matching, valid message is accepted; sender timestamps
are retained for audit but never reset the receiver's stale timer. A message
with the wrong nonce, duplicate/decreasing sender sequence, or unmatched
ack sequence is rejected, logged as `CONTROLLER_PROTOCOL_FAILURE`, and
does not refresh freshness; a protocol violation immediately closes
admission and is handled as controller failure. A missing, invalid, or
unacknowledged heartbeat older than 100 ms is stale. The primary then
records watchdog failure and requests whole-job termination. The watchdog
records primary failure and immediately requests whole-job termination
without waiting for primary exit. It then terminates the primary through its
retained exact process handle if still alive, waits at most 100 ms for that
handle to signal, and re-queries the workload job after
primary exit. It requests job termination again if any member remains,
regardless of the last admission-state message. If primary does not signal
within 100 ms, record `TERMINATION_UNCONFIRMED` for it and continue bounded
job accounting/PID reconciliation and termination attempts until the
applicable absolute observation deadline. It exits without claiming success
only after the primary is signaled and the job is confirmed empty or the
finite deadline expires with `TERMINATION_UNCONFIRMED`.
Heartbeats are monitored during admission setup as well as workload
execution. The 100 ms startup handshake deadline in §3.4 is distinct from
the ongoing 20 ms heartbeat cadence.

While Q03 observer coverage is enabled, event loss, `ProcessTrace` failure,
observer process exit, a malformed observer message, or a missing/stale
observer heartbeat causes immediate `PROCESS_CONTAINMENT_FAILURE`, closes
admission, and requests whole-job termination if any workload process is
assigned or admitted. The watchdog independently applies the same failure
action on observer loss even if primary heartbeats remain fresh. Before
admission, abort and stop/reap the observer; never resume while Q03 coverage
is required but unavailable.

Before `ResumeThread`, the primary must publish a successful baseline job
CPU sample and its sequence/QPC in the acknowledged `RESUME_INTENT` state.
While state is `ADMITTED` and the job is not confirmed complete, the
watchdog independently requires the reported CPU-sample sequence to
increase and its sample QPC to be monotonic and no later than the receiver's
current QPC. If there is no sample or the age from the receiver's current
QPC to the latest sample QPC exceeds 100 ms, even while primary heartbeats
remain fresh, the watchdog records
`RESOURCE_MEASUREMENT_INCONCLUSIVE`/`CPU_SAMPLE_STALE` and requests
whole-job termination. After termination is requested, sample freshness no
longer substitutes for the required final post-cessation query; absence or
failure of that query prevents a CPU-budget pass.

Any observed cessation after `T0 + 120 seconds` or final evidence commit
after `T0 + 120 seconds` is a failed wall-budget result. A post-budget
observation window does not extend allowed workload execution or change
that failure rule.

### 6.2 Finite post-budget observation candidate

Proposed owner decision: a **15-second observation-only window**, ending at
`T0 + 135 seconds`, for the independent watchdog to collect job-member
accounting/PID reconciliation and any Q03 recovery evidence after the
120-second wall threshold. Only the primary's dedicated reader threads can
observe stdout/stderr/result pipe EOF; if the primary fails, pipe-completeness
observation is unavailable and the result is `EVIDENCE_INCOMPLETE`. The
window permits no workload execution and does not increase the wall budget.
At the end, if cessation is not
confirmed, report `TERMINATION_UNCONFIRMED`,
`RESOURCE_MEASUREMENT_INCONCLUSIVE`, and `EVIDENCE_INCOMPLETE`; stop
observing and never report success. Final evidence commit after 120 seconds
still fails the wall budget.

Let `D` be the owner-approved observation duration. At
`T0 + 120 seconds + D - 100 milliseconds`, the watchdog requires both a
valid `EVIDENCE_COMMIT` and a signaled primary process handle with the
expected successful exit code. Receipt of the commit record without
successful primary cleanup and exit is not completion. If either condition
is absent, it records and requests termination of the workload job
immediately if any member is present, then records and requests termination
of the primary through the retained exact process handle, without waiting
beyond that instant. It waits at most the remaining 100 ms for the primary
process handle to signal, then re-queries the workload job.
If any member remains, it requests job termination again and continues
bounded accounting/PID reconciliation up to the absolute observation
endpoint `T0 + 120 seconds + D`. At that endpoint
the watchdog reports any remaining uncertainty and exits; it performs no
unbounded wait. `D` must exceed 100 ms so this bounded final cleanup interval
exists. The primary must finish reader joins, observer shutdown, artifact
flush/close, hash completion, final-path commit, the `EVIDENCE_COMMIT`
acknowledgment, all remaining handle cleanup, and successful process exit
before the cutoff. At the cutoff, if either commit validation or successful
primary exit is missing, the watchdog performs the failure path below even
if one of those two conditions is satisfied. If any required step remains
incomplete, mark `EVIDENCE_INCOMPLETE`; do not extend observation or
continue writing. The watchdog retains the exact primary process handle
duplicated before worker creation and uses that same handle for the one
deadline `TerminateProcess` request. It reports the resulting observation
or `TERMINATION_UNCONFIRMED` to its caller. This is failure cleanup, not a
second evidence writer; no artifact is declared committed by the watchdog.
The workload wall-budget failure at cessation or commit after T0+120 remains
in force regardless of whether evidence finalizes before the observation
deadline.

**15 seconds is a proposed value, not an owner decision.** It is based on a
historical candidate only; no termination-latency evidence establishes its
sufficiency. Owner must accept this value or specify another finite positive
bound and exact unconfirmed-cessation point before implementation
authorization. No indefinite wait or unbounded event history is allowed.

## 7. Job membership, Q03, and ETW

Windows Job Object semantics provide the primary containment mechanism:
after the suspended root is assigned to the intended job, ordinary child
processes inherit job association by default. With both breakaway flags
unset, a child cannot use the documented breakaway mechanism to leave that
job. Job accounting, active count, PID list, job signaling, and targeted
`IsProcessInJob(process, intendedJob, ...)` checks are sufficient to observe
and terminate admitted **job members**. They do not enumerate a process
created outside the job by a broker/service/remote-process path, and a
`NULL` job handle to `IsProcessInJob` does not prove membership in the
intended job.

ETW is therefore **not a substitute for Job Object containment** and is
not required to prove that the assigned root belongs to the intended job.
It is required only if the policy claims detection/recovery of an escaped
or externally created descendant (Q03), which Job Object accounting cannot
establish by itself. The contract's Q03 observer candidate is a separate
trusted process mode using NT Kernel Logger process start/stop events,
QPC-based event timestamps, checked event-loss counters, and
`EVENT_ENABLE_PROPERTY_PROCESS_START_KEY`. Correlate a process instance by
PID plus `EVENT_EXTENDED_ITEM_PROCESS_START_KEY.ProcessStartKey` and
observed parent instance; parent PID alone is not an identity.

`GetProcessInformation(ProcessTelemetryIdInformation)` is invalid:
`ProcessTelemetryIdInformation` is not a member of the documented
`PROCESS_INFORMATION_CLASS` accepted by `GetProcessInformation`. Microsoft
documents the `PROCESS_TELEMETRY_ID_INFORMATION` structure and describes
`ProcessStartKey`, but says that the structure has no associated header or
import library. The candidate query is `NtQueryInformationProcess` with
`ProcessTelemetryIdInformation` (class value 64) and that structure on the
exact process handle. The current Microsoft `NtQueryInformationProcess`
reference lists class 64 and the associated structure, but warns that the
function may be altered or unavailable in future Windows versions. This
version-sensitive reference does not establish a supported cross-version
guarantee or host qualification
([NtQueryInformationProcess](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntqueryinformationprocess),
[PROCESS_TELEMETRY_ID_INFORMATION_TYPE](https://learn.microsoft.com/en-us/windows/win32/devnotes/process_telemetry_id_information_type),
[PROCESS_INFORMATION_CLASS](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ne-processthreadsapi-process_information_class)).
Therefore this is **not an established stable, supported API guarantee**.
The structure documentation lists Windows 10 as its minimum client, but
does not establish class-64 availability, stability, or class-specific
handle-access requirements. The candidate requests at least
`PROCESS_QUERY_LIMITED_INFORMATION`; a query failure is closed, and the
implementation must not silently broaden rights. Do not claim that the
candidate is qualified or portable. A Q03 recovery implementation may use
it only if the owner explicitly accepts this version-sensitive native
interface and pins/qualifies the exact Windows build, handle rights, and
returned structure; otherwise safe Q03 termination remains blocked pending
a supported identity-query path or a separately authorized OS-enforced
boundary.

If the owner separately accepts that Q03 query, open a process handle with
`PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE` for observation, then
call `NtQueryInformationProcess` on that exact handle using the pinned
`ProcessTelemetryIdInformation` class candidate. Require `NT_SUCCESS`,
validate the returned structure size/header and process ID, and require the
returned `ProcessStartKey` to equal the ETW event key before
`IsProcessInJob(process, intendedJob, &inJob)`. If termination is required,
open one handle with
`PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_TERMINATE | SYNCHRONIZE`,
repeat the same query and checks on that exact termination-capable handle,
and require equality to the ETW identity before using that same handle for
`TerminateProcess` and `WaitForSingleObject`. Never validate one handle's
PID identity and then terminate through a separately opened, unvalidated
PID handle. If the class is rejected, the returned structure is malformed,
or the key is missing or mismatched, do not act on that handle; classify
identity as ambiguous and fail Q03 recovery closed. The observer has no job
handle and does not call the membership API itself.

On event loss, observer exit, unresolvable ancestry, or observed descendant
outside the intended job: fail closed, stop remaining cases, record
`PROCESS_CONTAINMENT_FAILURE`, and terminate the intended job. Terminating
an identified outside process is permitted only when the owner has approved
the version-pinned Q03 identity-query candidate above (or a supported
alternative) and the exact termination-capable handle passes the identity
check; then call `TerminateProcess` through that same handle, wait on it,
and reconcile descendants until the owner-approved post-budget deadline. If
no approved identity query is available, do not terminate by PID alone;
record `TERMINATION_UNCONFIRMED`, retain Q03 as blocked, and require a
separately authorized OS-enforced boundary or accepted identity-query path.
If access is denied, the observer cannot reconcile, or exit is not
confirmed, record `TERMINATION_UNCONFIRMED`; never resume an escaped
suspended process.

ETW start/stop evidence does not alone prove ancestry completeness, prevent
an escaped process executing before detection, or guarantee termination of
protected/service-owned processes. Required kernel-session privilege,
session availability, event-loss accounting, event ordering, ancestry
correlation, Q03 response, and target-host coverage remain runtime
qualification obligations. If owner policy requires a hard guarantee
against broker/service/remote creation rather than detection-and-recovery,
the present design is insufficient; identify and separately authorize an
OS-enforced boundary. Do not claim ETW or Job Objects alone provide that
guarantee.

## 8. Traceability and review boundary

The matrix separates source completeness, OS/API semantics, runtime
qualification, policy, and blockers. Static source review can verify that
code requests/checks the specified operations; it cannot prove that Windows
enforced them on the target host.

| Requirement | Source-level implementation obligation | OS/API semantic review | Runtime qualification | Owner-policy decision / blocker |
|---|---|---|---|---|
| Exact command/profile/source identity | Fixed allowlist; hash by opened handle; reject mismatch | File/API behavior review | TOCTOU and target profile | Fixture/interpreter identities absent; profile must be approved |
| Restricted token and write boundary | Create/query exact restricted primary token; verify fixed-path ACLs/effective access; fail closed | `CreateRestrictedToken`, `SetTokenInformation`, `AccessCheck`/`MapGenericMask`, `CreateProcessAsUserW` requirements | Effective token, whole-machine write denial, ACL/reparse/hard-link alternate paths, application compatibility | Exact group/privilege set and writable-path threat model must be frozen |
| Environment | Exact names/values including generated decimal `TPCN_RESULT_HANDLE`; local UTF-16 block; free on every path | `CREATE_UNICODE_ENVIRONMENT` interpretation | Target runtime compatibility | Host-dependent path values require profile |
| Pipes/handles | Explicit inheritable handle lists with `bInheritHandles=TRUE`; close controller copies; versioned result protocol; synchronous anonymous-pipe readers on dedicated threads; three single-producer/single-consumer 4,096-byte slots, one 4,096-byte result-line buffer, one 8,192-byte compressor output buffer and bounded compressor allocator; bounded named-pipe control channels; reader monitors; attribute-list cleanup; stop/reap helpers | `CreatePipe` synchronous-I/O semantics, `STARTUPINFOEX`, `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`, `CreateNamedPipeW` | Kernel pipe allocation, EOF, deadlock, handle leakage, concurrent drain under backpressure, helper shutdown | Exact helper token/environment profile required |
| Job setup/assignment | Configure/read back flags before creation; use creation-time `PROC_THREAD_ATTRIBUTE_JOB_LIST`; targeted intended-job membership and complete PID checks; resume only after pass | Process attribute support, job association, breakaway, nested-job semantics | Target OS, enclosing jobs, Q03, failure cleanup | Whole-tree guarantee scope must be accepted |
| CPU/wall/controller supervision | Save pre-resume user/kernel CPU baseline; compare admission-relative deltas including final post-cessation query; watchdog independently terminates on stale primary/sample and inspects whole job; immutable T0/deadline startup record; strict sequenced admission states; primary owns 115 s request; 20 ms heartbeats; watchdog remains live through evidence commit, primary handle cleanup/exit, and caller-status emission; caller success requires a validated commit and successful primary exit before the finite finalization deadline | Job accounting and shared QPC/wait semantics | Cadence, overshoot, watchdog death, deadline races, cessation interval | 120 s/115 s are frozen; post-budget window requires owner choice |
| Job completion | Poll successful job accounting and complete PID-list queries to reconcile zero active members; require known process handles signaled and reader EOF; report a bounded observation interval | Job accounting/PID-list queries; job-object signal is not used because docs tie it to end-of-job time-limit handling | Reconciliation under termination/races | Owner accepts interval-based cessation evidence |
| Job memory control | Set/read back `JobMemoryLimit=268435456`; reconcile complete, untruncated PID lists and active counts before/after per-member identity-checked `PrivateUsage` queries; require stable membership and <=10 ms sample span; invalid sample or sum >= ceiling immediately terminates | Job memory charge vs process commit definitions; per-process `GetProcessMemoryInfo` semantics | Allocation-denial behavior, sampling span, observed charges | Sampled sum is not atomic; **unresolved metric equivalence; explicit blocker** |
| Artifact ceiling/writer | One writer; pre-reservation and exact pre-write cap checks for compressed output, finalization, metadata, hashes and exports; fail incomplete | File/pipe/gzip semantics | Ledger fit, crash/storage failure, all-write boundary | Existing proposal requires separately authorized synthetic sizing before Phase 2A implementation |
| Q03/ETW | Observer readiness before workload when selected; start/stop parsing, instance correlation, loss checks, stop/reap; do not terminate outside-job process unless same-handle identity is verified | ETW semantics; `NtQueryInformationProcess` class 64 is version-sensitive and not a cross-version guarantee | Privileges, complete coverage, lag, exact host/class/structure behavior, Q03 recovery | Owner must explicitly accept version-pinned native identity query or separately authorize supported identity path/OS boundary |
| Zero retries/scientific isolation | No retry loop; exact fixture command only; no TPCN behavior change | Not applicable | Later authorized fixture confirms command behavior | Fixture absent and execution not authorized |
| Publication/provenance | Exact changed-file list, source and artifact hashes | Git object/staging semantics | Exact staged-byte check and remote fetch | Only after review PASS and owner authorization |

The listed source obligations are reviewable without runtime execution.
Qualification tasks are not silently pulled into source review. The
governing proposal explicitly requires ledger sizing before Phase 2A
implementation or execution; that specific requirement remains a gate
unless the owner changes it. No runtime evidence is claimed in this R2
review.

## 9. Static validation and authorization boundary

If a separate owner authorization approves implementation against the exact
R2 SHA and source profile, static validation may be limited to:

1. Source/document review.
2. Syntax-only compilation without import or launch:
   `.\.venv\Scripts\python.exe -m py_compile scripts\luna65_phase2a_supervisor.py`
3. `git diff --check` for tracked modifications and a source-only no-index
   whitespace check for the untracked source, recording the expected
   difference exit code separately.
4. Changed-file allowlist and checkout-byte SHA-256 identities; independent
   precommit review of exact staged bytes/Git object identity before any
   publication.

Syntax compilation may generate an ignored `__pycache__` file. It is a
temporary validation byproduct, not an authorized implementation file or
publication artifact; record and remove only that exact generated file if
cleanup is authorized.

No supervisor invocation, import, test, smoke test, resource probe, sizing
run, qualification, Phase 2A/2B fixture, dataset, training, scoring, or
Spiral benchmark is authorized here. Static success is not evidence of
enforcement.

## 10. Exact implementation authorization request (draft only)

> I authorize only corrective implementation of
> `scripts/luna65_phase2a_supervisor.py` against the exact baseline
> `1d6325f3ca738b32a6ee9e1a5613d2faa9458770` and the exact R2 contract
> checkout SHA-256 identified by the completed independent review handoff.
> I approve the fixed Phase 2A supervisor design and its named source-level
> obligations, with the following policy decisions expressly recorded:
> (1) memory enforcement metric: **[owner selects Job Object job-commit
> charge or retains private-commit mapping blocker]**; (2) post-budget
> observation window: **[owner accepts 15 seconds or specifies another
> finite value]**; (3) cessation evidence: **[owner accepts bounded
> observation interval, not an exact physical exit timestamp]**; and
> (4) Q03 assurance scope: **[owner accepts a version-pinned
> `NtQueryInformationProcess` class-64 identity-query candidate and its
> qualification, approves a supported alternative, or separately
> authorizes an OS-enforced boundary]**. The implementation
> allowlist is the single named Python file; any additional file/host
> provisioning requires separate authorization. I authorize only source
> review, the specified nonexecuting `py_compile`, diff/provenance checks,
> and exact-byte review. I do not authorize supervisor invocation, runtime
> tests/probes/sizing/qualification, Phase 2A/2B fixtures, dataset or
> benchmark execution, or publication before independent precommit review.
> Authorization Q remains separate. Implementation may not begin until
> the governing proposal's synthetic ledger-sizing prerequisite has been
> completed under its own explicit authorization and its result reviewed,
> unless the owner separately and explicitly changes that prerequisite.

This wording is not an authorization. No implementation may begin until
owner choices are explicit, every owner-policy blocker that prevents
enforcement is resolved, the exact contract/source identities are bound,
the separately authorized ledger-sizing prerequisite is completed (or
explicitly changed by the owner), and the owner issues a separate
affirmative authorization.

## 11. Current governance status

**Corrective supervisor implementation: NOT AUTHORIZED.**

**Supervisor qualification: NOT AUTHORIZED.**

**Phase 2A and Phase 2B fixtures: NOT AUTHORIZED.**

**Full Spiral execution: BLOCKED.**

**Luna-64 corrective execution: BLOCKED.**

**Luna-63C: FROZEN.**

No architecture clause or ACP is changed. This document is a new R2
governance draft; it does not overwrite the R1 draft/handoff or publish an
implementation. Publication and workflow update are conditional on an
integrated independent PASS and exact-byte provenance verification.

## 12. References

- [CreateRestrictedToken](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createrestrictedtoken)
- [CreateProcessAsUserW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasuserw)
- [Process creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags)
- [Process and thread handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)
- [CreatePipe](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-createpipe)
- [CreateNamedPipeW](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-createnamedpipew)
- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information)
- [PROCESS_MEMORY_COUNTERS_EX](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-process_memory_counters_ex)
- [IsProcessInJob](https://learn.microsoft.com/en-us/windows/win32/api/jobapi/nf-jobapi-isprocessinjob)
- [GetProcessInformation](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocessinformation)
- [EVENT_EXTENDED_ITEM_PROCESS_START_KEY](https://learn.microsoft.com/en-us/windows/win32/api/evntcons/ns-evntcons-event_extended_item_process_start_key)
- [ENABLE_TRACE_PARAMETERS](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-enable_trace_parameters)
- [AccessCheck](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-accesscheck)
- [MapGenericMask](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-mapgenericmask)
- [QueryInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject)
- [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
- [TerminateProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject)
- [WaitForSingleObject](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
- [Event Tracing for Windows](https://learn.microsoft.com/en-us/windows/win32/etw/about-event-tracing)
