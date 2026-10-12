# Luna-65 Phase 2A Supervisor Corrective Contract — R6

**Gate:** `L65-PHASE2A-SUPERVISOR-AUTH-I-CORRECTIVE-R6`

**Status:** **DRAFT FOR INDEPENDENT REVIEW — SOURCE IMPLEMENTATION, STATIC
VALIDATION, QUALIFICATION, AND EXECUTION NOT AUTHORIZED.**

**Integrated disposition:** **BLOCKED — R6 CORRECTIVE CONTRACT
INCOMPLETE**, pending fresh exact-byte review and the technical/policy
blockers listed below.

This is governance-only. It does not alter the accepted Phase 2A resource
limits, authorize source implementation or static validation, run ETW, or
authorize qualification, sizing, fixtures, or benchmarks. R1, R2, and
their handoffs remain historical evidence; none is overwritten.

## 1. Provenance and preserved state

Expected baseline verified for this review:

- Branch: `governance/luna64-r4.3-freeze-20261010`
- Local HEAD and remote-tracking baseline:
  `1d6325f3ca738b32a6ee9e1a5613d2faa9458770`
- Parent: `d11d370a7c97184529845c9cac984fc22018c576`

The user-provided R6 instruction attachment was read as a read-only
snapshot, 14,735 bytes, SHA-256
`6B572A2734D7839524F4F38E566E695798F3B39ABA4FDC394C184948742471AB`.
The new D9/D10 decisions below are attributed to that instruction.

| Artifact | Raw checkout SHA-256 | Review-start identity/state |
|---|---|---|
| `scripts/luna65_phase2a_supervisor.py` | `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1` | 21,494 bytes, untracked fail-closed scaffold |
| R5 contract `LUNA_65_PHASE2A_SUPERVISOR_AUTH_I_CORRECTIVE_R2.md` | `9D80C19E9CE5CA82695747DA17D740B7AD0FA679AA0F3141AB214E49CC2708A9` | 80,656 bytes; CRLF checkout |
| R5 handoff `luna-0-luna65-phase2a-corrective-contract-review-r2.md` | `1EDF09B57DB4368903CD0C6BA95B1133CC02FAE17F2CBDB2C2E9E6FB8AE6CEA7` | 12,161 bytes; untracked |
| R1 corrective draft | `4E625C363A239BAB1386E0DE454A11F0F23972BFB5BD9137141946C282750999` | Untracked; preserved |
| R1 corrective handoff | `04B048E42913B26FFCAB6173A94134BF200055F4435C3536ED08F0D32C4A2C00` | Untracked; preserved |
| Implementation proposal R1 | `31C2CEDAAC91C78A79D746879AEB52759A92335DDA7D18EDC5F0E055F141EA97` | Tracked; unchanged |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `64AF62CD2E8CD0696BF52EEDF63672FB04399EF949B580FD551360A0F237ED61` | Pre-existing modified file; preserved |

No staged changes were present. The pre-existing workflow modification,
scaffold, drafts, and handoffs are preserved. R6 is a new document; it does
not replace R2 or reclassify any historical review.

## 2. Owner decisions and unchanged resource policy

### D9 — finite post-budget observation

**OWNER ACCEPTED FOR PHASE 2A DESIGN ONLY.** The trusted controller may
continue termination observation for at most 15 seconds after the
120-second workload wall budget. The proposed absolute points from workload
clock origin `T0` are. `T0` retains the controlling proposal's definition:
the trusted supervisor's first-entry QPC before setup; it is not reset at
workload admission or helper readiness.

> “The trusted controller may continue termination observation for up to
> 15 seconds beyond the 120-second workload wall budget.”
>
> “The observation interval is not additional workload execution
> authority.”

| Time | Required interpretation |
|---:|---|
| `T0 + 115 s` | Primary requests whole-job termination if workload remains active. |
| `T0 + 120 s` | Workload wall budget expires; any later workload cessation or evidence commit is a wall-budget failure. A later failure/incomplete-evidence record may still be preserved, but it cannot convert the run into a budget-compliant success. |
| `T0 + 135 s` | Observation deadline. This bounds controller observation only; it is not a guaranteed physical termination deadline or permission for workload execution. |

The supervisor must actively request termination of an over-budget
workload. If cessation is unresolved at 135 seconds, classify
`CONTAINMENT_FAILURE`/`TERMINATION_UNCONFIRMED`, preserve available
evidence, and do not report success. D9 changes no CPU, memory, artifact,
retry, or fixture authorization.

### D10 — cessation evidence

**OWNER ACCEPTED FOR PHASE 2A DESIGN ONLY.** A bounded observation interval,
not an invented exact physical exit time, is the required cessation
evidence. Record: last successful observation with a relevant job process
active; first subsequent successful observation with no relevant job
process; timestamp source and QPC frequency for both; exact query/API
results and whether all required job/process observations agree;
termination-request timestamp(s); job-completion observation timestamp;
and final evidence-commit timestamp. If required observations are missing,
contradictory, or cannot establish the interval, classify cessation as
unconfirmed.

> “A bounded observed-cessation interval is sufficient evidence format.”
> “When a valid observation interval cannot be established, mark cessation
> unconfirmed.”

### Frozen resource policy

This corrective contract applies only to the Luna-65 Phase 2A direct-neuron
capacity fixture. No R6 text changes these limits:

- 120 seconds monitored cumulative job user-plus-kernel CPU.
- 120 seconds monitored wall time from controller `T0`.
- Five-second early stop; request termination at 115 seconds if active.
- 268,435,456 bytes aggregate concurrent private committed memory
  (metric mapping remains unresolved).
- 1,048,576 bytes maximum retained artifacts.
- Zero retries; whole admitted process-tree containment; fail closed.

D9/D10 are design decisions only. They do not authorize implementation,
static validation, qualification, tests, synthetic sizing, fixtures, or
benchmarks.

## 3. Observer lifecycle and ownership state machine

R5's design flaw was starting the optional observer before the watchdog
owned it. The R6 source contract requires that **no ETW observer or session
become active before an independently running trusted watchdog has accepted
responsibility for stopping and reaping it**.

The preferred single-source-file design has fixed primary, watchdog, and
optional observer modes. The watchdog is started first in a nonobserving
state. An optional observer process is created suspended and cannot call
`StartTraceW` before watchdog registration and activation. The observer is
placed at creation into a separate, narrowly scoped observer Job Object
configured with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` and no breakaway flags.
This helper job is distinct from the workload job; observer resource use is
not represented as workload CPU or memory. The watchdog holds query and
terminate authority over this helper job and exact observer process/thread
handles. The primary retains independent cleanup authority until orderly
handoff and process exit.

Required ordering:

1. The primary creates three distinct unnamed jobs before any helper:
   (a) a workload job; (b) an observer helper job; and (c) a watchdog-only
   bootstrap job. Each has a restrictive DACL, non-inheritable handle, and
   configured/read-back `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, with no
   breakaway flags. Initially, only the primary holds the bootstrap-job
   handle; it is not inherited or duplicated into a suspended or unready
   watchdog. The workload and observer helper job handles are retained by
   the primary and duplicated into the watchdog only after watchdog process
   creation. Configure private channels, evidence reservations, and the
   exact controller-time record. No workload or observer process exists.
2. The primary creates the watchdog suspended, with its fixed restricted
   profile, explicit control/status handle list, and the bootstrap job as
   the sole `PROC_THREAD_ATTRIBUTE_JOB_LIST` entry. Creation fails closed
   if this job association is unsupported or rejected. If process creation
   returns failure, treat `PROCESS_INFORMATION` as invalid and create no
   process handle from its contents. Release the startup attribute
   resources and call `TerminateJobObject` on the dedicated bootstrap job,
   then query complete membership. If the query fails or returns members,
   enumerate and reconcile exact member handles and keep the primary as
   cleanup owner until the job is observed empty. If emptiness cannot be
   established, classify containment failure, retain valid job handles,
   and admit no work. Do not call `TerminateProcess` with an invalid or
   nonexistent handle. If creation succeeds,
   retain the exact returned handles and use the post-creation cleanup
   path on every later failure. The watchdog has no
   handle to the bootstrap job. The primary retains the exact watchdog
   process/thread handles and duplicates the exact primary-process,
   workload-job, and observer-job handles into the watchdog while it is
   suspended, using
   `DuplicateHandle` with a target process handle carrying
   `PROCESS_DUP_HANDLE`, `bInheritHandle=FALSE`, and `dwOptions=0`.
   Every remote process/job handle is therefore noninheritable by the
   watchdog. The remote job rights are only
   `JOB_OBJECT_QUERY | JOB_OBJECT_TERMINATE | SYNCHRONIZE`; the target
   process handle is `PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_TERMINATE
   | SYNCHRONIZE`. For `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`, set
   `bInheritHandles=TRUE` and mark only the explicitly listed child handles
   inheritable for creation; every unlisted controller handle remains
   noninheritable. It sends a versioned startup record carrying nonce, QPC
   frequency, immutable deadlines, and profile digest. The bootstrap-job
   handle is specifically excluded from this transfer.
3. The primary resumes the watchdog and requires its readiness acknowledgment
   by the 100-ms startup deadline. The watchdog validates all received
   handle values and target identities, job configuration, startup record,
   channels, and deadlines. It acknowledges `WATCHDOG_READY` as
   **NONOBSERVING**. It does not start ETW or admit workload execution. If
   handle duplication, resume, identity validation, or readiness fails
   after successful process creation while the primary remains alive, the
   primary immediately requests `TerminateProcess` through the exact
   watchdog handle, requires `WaitForSingleObject(watchdog, 100 ms) ==
   WAIT_OBJECT_0`, and checks the exit status; remote duplicates close when
   the target process exits. If the exact wait fails, times out, or reports
   any value other than `WAIT_OBJECT_0`, the primary also calls
   `TerminateJobObject` on the primary-owned bootstrap job, then waits on
   the exact watchdog process handle and queries the bootstrap job's
   complete membership. No observer or workload may exist yet. If the
   watchdog is still not signaled or job membership is not empty after the
   bounded startup-cleanup attempt, classify containment failure, retain
   all still-valid exact handles, keep the primary alive as cleanup owner,
   and continue observation; do not admit work, close a possibly
   non-last job handle, or return success. A wait/API failure is not proof
   of cessation.
   If the primary dies before this handshake completes, its sole
   bootstrap-job handle closes; the watchdog-only job must terminate the
   suspended or unready watchdog, which closes its remote job/process
   handles. This kill-on-close fallback is required source behavior, not
   proof that the OS enforced it on the target host.
4. Only after `WATCHDOG_READY`, the primary duplicates the bootstrap-job
   handle into the running watchdog with `JOB_OBJECT_QUERY | SYNCHRONIZE`,
   `bInheritHandle=FALSE`, and `dwOptions=0`.
   The primary transmits the returned remote handle value in a
   nonce-bound handoff record. The watchdog validates that exact handle
   using `IsProcessInJob(GetCurrentProcess(), remoteBootstrapJob, &member)`
   and requires `member == TRUE`; this checks the watchdog's own membership
   in that specific job, rather than inferring it from successful
   assignment. It acknowledges `WATCHDOG_SUPERVISION_OWNED` only after the
   check succeeds. Until this acknowledgment, the primary retains its
   original bootstrap handle and no observer/workload may be created.
   After acknowledgment, the primary closes its original bootstrap handle
   exactly once; the watchdog's duplicate is then the sole remaining
   bootstrap-job handle, allowing it to survive primary failure. Once this
   handoff completes, primary-handle closure does not trigger kill-on-close
   while the watchdog still owns its duplicate; a hung watchdog after
   simultaneous primary failure therefore has no established OS fallback.
   This remains an explicit containment blocker. A
   duplication error, invalid/unknown remote handle value, failed
   membership check, or lost acknowledgment is a fail-closed startup error:
   create no observer/workload, request watchdog termination through the
   exact process handle, wait and check its exit, then close the primary
   bootstrap handle only after the watchdog is observed signaled. A failed
   primary close is recorded once and is not blindly retried; keep the
   primary alive, use any still-valid exact handles for cleanup, and
   classify unresolved ownership as containment failure. If the primary fails before
   duplication, its handle closure triggers the bootstrap job's
   kill-on-close action. If duplication succeeds but the handle value or
   acknowledgment is lost, the watchdog has no permission to start an
   observer/workload; on detecting primary loss it exits, closing any
   received duplicate. If the primary fails after the watchdog has
   validated the duplicate but before acknowledgment is received, the
   watchdog follows its primary-loss cleanup path and exits. Record both
   sides of every handoff outcome. The watchdog job contains only the
   watchdog. Kill-on-close and this ownership transfer are source
   requirements, not proof of target-host enforcement.
5. If ETW is not selected, the observer path is explicitly disabled and
   Q03 is not claimed. If ETW is required by the approved Q03 assurance
   profile, the primary creates separate run-scoped, unidirectional
   overlapped command, status, and ETW-event named-pipe endpoints with a
   restrictive ACL. Only primary, watchdog, and observer profiles may
   access them; the worker receives no endpoint. The primary creates the
   observer suspended with the exact observer helper job supplied through
   creation-time `PROC_THREAD_ATTRIBUTE_JOB_LIST`, and only its
   command-read, status-write, and event-write handles in
   `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`.
   `bInheritHandles=TRUE`; only those listed observer endpoints are
   inheritable for creation, and all other controller handles are
   noninheritable. If observer process creation returns
   failure, treat `PROCESS_INFORMATION` as invalid, call
   `TerminateJobObject` on the dedicated observer helper job, and query
   complete membership. If the query fails or returns members, enumerate
   and reconcile exact member handles and keep the primary/watchdog as
   cleanup owners until the job is observed empty. If emptiness cannot be
   established, classify containment failure and do not create the
   workload. Do not attempt exact-process termination without a returned
   process handle. On successful creation, the primary closes its local
   copies of observer-only pipe endpoints and retains its controller
   endpoints. The primary retains the ETW-event read endpoint as the sole
   evidence-writer input; the watchdog receives only command-write and
   status-read endpoints for bounded stop/heartbeat control. The observer
   entry point must accept
   only fixed internal mode and nonce and must not start a trace before its
   activation protocol. If the primary fails during creation, the already
   ready watchdog detects primary-handle signal/staleness and terminates
   the entire observer helper job; it does not depend on a returned
   observer PID or process handle.
6. The primary duplicates the watchdog-only command-write endpoint with
   `GENERIC_WRITE` and status-read endpoint with `GENERIC_READ` into the
   watchdog using `bInheritHandle=FALSE` and `dwOptions=0`; the primary
   retains its primary-side control endpoints and ETW-event read endpoint.
   endpoints. The primary duplicates the exact observer process handle into the
   watchdog with `PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_TERMINATE |
   SYNCHRONIZE`, and the exact primary thread handle with
   `THREAD_QUERY_LIMITED_INFORMATION | THREAD_SUSPEND_RESUME | SYNCHRONIZE`,
   each with `bInheritHandle=FALSE` and `dwOptions=0`.
   It sends process/thread IDs, creation time, process start identity where
   available, expected observer-job membership, session nonce, and remote
   handle values. Before ownership acknowledgment or thread resumption,
   the watchdog validates identity against the exact handles and requires
   `IsProcessInJob(exactObserverProcess, observerJob, &member)` to succeed
   with `member == TRUE`. It also requires
   `JobObjectBasicAccountingInformation.ActiveProcesses == 1` and a
   complete `JobObjectBasicProcessIdList` containing only the PID returned
   by `GetProcessId(exactObserverProcess)`, bound to that exact handle with
   `GetProcessTimes` creation time. The PID list is not itself treated as a
   process-instance identity. A failed query, mismatch, unexpected member,
   or incomplete list prevents activation and workload admission.
7. The watchdog assumes explicit ownership by recording the registration
   sequence and acknowledging `OBSERVER_OWNED` only after it can activate
   the suspended observer and terminate/reap it or its entire observer
   helper job. Until that acknowledgment, the observer remains suspended
   with no ETW session started. If registration fails, the primary and
   watchdog both request termination of the observer helper job and
   reconcile zero active members; no workload is created.
8. Only the watchdog activates the observer with the retained exact thread
   handle. It records the `ResumeThread` result and requires the exact
   expected suspend-count transition. The observer then starts the uniquely
   named run-scoped ETW session and reports `OBSERVER_READY` only after
   successful `StartTraceW`, provider enablement, consumer start, event
   clock configuration, process-start-key enablement, and zero initial
   loss counters. For the kernel process provider, process-start-key
   enablement is specifically `EnableTraceEx2` with an
   `ENABLE_TRACE_PARAMETERS` structure at
   `ENABLE_TRACE_PARAMETERS_VERSION_2` and
   `EnableProperty = EVENT_ENABLE_PROPERTY_PROCESS_START_KEY`; the observer
   must check the API result and record the exact provider/control/flags.
   The watchdog retains responsibility; the primary also
   receives and validates observer readiness and fresh heartbeats.
9. Workload admission is ordered and auditable. Before creating a process,
   validate the exact allowlisted command, source/fixture/interpreter
   identities, worker profile, constructed environment, pipe endpoints,
   output/evidence boundary, and workload-job limits/configuration. Create
   the worker suspended using `CreateProcessAsUserW` and
   `STARTUPINFOEXW`/`PROC_THREAD_ATTRIBUTE_JOB_LIST`, with the workload job
   as its creation-time job association and only the explicit child pipe
   handles in `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`; set
   `bInheritHandles=TRUE`, make only those listed pipe handles inheritable
   for creation, and keep all other controller handles noninheritable.
   Fail closed if any required creation attribute or job association is
   unavailable; do not resume a process that was not associated at
   creation. If `CreateProcessAsUserW` returns failure, treat
   `PROCESS_INFORMATION` as invalid, do not use its fields as process
   handles, call `TerminateJobObject` on the dedicated workload job, and
   query complete membership. If the query fails or reports any members,
   enumerate and reconcile exact member handles and keep the primary and
   watchdog as cleanup owners until emptiness is observed; if it cannot be
   established, classify containment failure and do not report admission.
   If creation succeeds, retain the exact process/thread handles; close
   controller copies of child-only pipe endpoints. Before any
   `ResumeThread`, verify on that exact process
   handle that `IsProcessInJob(process, workloadJob, &member)` succeeds
   with `member == TRUE`, query `JobObjectBasicAccountingInformation` and
   require the expected active-process count, and retrieve the complete
   `JobObjectBasicProcessIdList` until its returned list is complete and
   contains only `GetProcessId(exactProcessHandle)`; bind that PID to the
   exact handle's `GetProcessTimes` creation time. The PID list alone does
   not establish process-instance identity; reject unexpected or
   contradictory members.
   Re-read required job limits and breakaway settings. Only after all
   checks pass may the primary resume the exact thread; record the prior
   suspend count and require the expected transition. Any validation,
   query, or resume failure means no fixture code may execute: terminate
   the workload job, wait/reconcile the exact handles and empty membership,
   and classify unconfirmed cleanup as containment failure. Workload
   creation and resume remain forbidden until watchdog readiness, required
   observer ownership/readiness (when Q03 requires it), and this entire
   admission gate pass.
10. The workload job also has `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` and no
   breakaway flags. Both primary and watchdog hold a handle during normal
   supervision. If both trusted controllers exit, closure of their last
   workload-job handles is an OS-requested fallback termination, not an
   observed cessation result.
11. Normal shutdown stops workload admission, confirms workload cessation
   using D10, then asks the observer to stop/flush. The watchdog independently
   observes observer exit and helper-job emptiness. Only after observer
   cleanup is confirmed may evidence finalization report complete.

The watchdog is created and acknowledged before any observer process,
closing the R5 pre-readiness gap. A suspended observer created before ownership
acknowledgment is incapable by design of starting ETW. No process is
described as safe merely because its PID was registered; exact handles,
creation identity, and job membership are required.

### Failure responsibility matrix

| Failure point | Immediate cleanup owner and action | Required observation/result |
|---|---|---|
| Primary fails before watchdog readiness | No observer/workload exists. The primary-only bootstrap-job handle closes; its kill-on-close limit terminates the watchdog, whose exit closes duplicated workload/observer job handles. | No workload admitted. This fallback remains target-host qualification, not a success claim. |
| Watchdog creation/resume/readiness fails while primary lives | If the creation API failed, treat `PROCESS_INFORMATION` as invalid; terminate/reconcile the dedicated bootstrap job without using a nonexistent process handle. After successful creation, use the exact watchdog process handle; on failed wait, terminate/reconcile the bootstrap job and retain handles/ownership until its member list is empty or report unresolved containment. No observer/workload may exist. | `CONTROLLER_FAILURE`; if process exit or empty job membership cannot be established, containment failure and evidence incomplete. |
| Primary fails after initial watchdog readiness but before bootstrap ownership acknowledgment | No observer/workload exists. If no duplicate was created, primary-handle closure triggers kill-on-close. If a remote duplicate exists but its value/acknowledgment was lost, the watchdog detects primary loss and exits without admitting work; its process exit closes all remote handles. | No observer session; no workload admitted; no successful status. This partial-transfer cleanup remains target-host qualification. |
| Primary fails after `WATCHDOG_SUPERVISION_OWNED`, before observer creation | The watchdog retains its bootstrap and observer/workload job handles, detects primary failure, and remains responsible for empty-job reconciliation before exiting. | No observer session; no workload admitted. |
| Primary fails during observer process creation, before registration | Watchdog monitors primary handle and observer helper-job membership; it terminates the entire observer helper job on stale-primary signal/timeout, then reconciles empty membership. | No ETW start is permitted before ownership ack; cleanup unconfirmed by deadline is containment failure. |
| Primary fails while registration is in flight | Watchdog accepts only a complete, nonce-matched registration. If valid, it takes ownership and stops/reaps; otherwise it terminates all members of the dedicated observer helper job. | No ambiguous PID-only cleanup. Evidence incomplete if exact empty state is not observed. |
| Primary fails after observer activation | Watchdog owns the observer process/thread/job and ETW session name; it issues `ControlTraceW(STOP)` and terminates/reaps the observer/helper job, then reconciles process/event state. | Observer cleanup has its own request/result/interval; no successful run status on failure. |
| Observer creation, identity check, transfer, or registration timeout | Primary and watchdog request observer-job termination. Watchdog waits/reconciles boundedly; primary does not create workload. | `CONTROLLER_FAILURE` or `PROCESS_CONTAINMENT_FAILURE`; evidence incomplete if cleanup unconfirmed. |
| Observer readiness or ETW startup failure | Watchdog issues stop for the run-scoped session if created, terminates/reaps observer job, reconciles; no workload admitted. | `Q03_COVERAGE_UNAVAILABLE`; no Q03-enabled success. |
| Watchdog dies | Primary immediately terminates workload and observer helper jobs, calls `ControlTraceW(STOP)` for registered session, and reconciles exact process handles and job membership. | No workload continuation; controller failure; if primary cannot establish cleanup, containment failure. |
| ETW loss, consumer failure, or observer heartbeat stale | Watchdog immediately closes admission, requests workload-job termination, stops ETW and reaps observer; primary independently applies same fail-closed action. | `Q03_COVERAGE_LOST`; continue bounded observation; no pass from prior events. |
| ETW stop/flush fails | Watchdog and primary each issue bounded stop attempts through the run-scoped session identity and terminate/reap observer; do not retry workload. | Record every call/error; `OBSERVER_CLEANUP_UNCONFIRMED`, evidence incomplete. |
| Simultaneous primary and observer failure | Watchdog acts from retained exact handles, stops session, terminates observer/workload jobs, observes. If watchdog also dies, kill-on-last-job-handle-close is only fallback. | Unless exact cessation/cleanup is independently observed, `CONTAINMENT_FAILURE`; never infer Off from deadline or handle close alone. |
| Watchdog failure during/after registration | While alive, the primary uses the exact watchdog handle to request termination; it stops any registered ETW session, terminates helper/workload jobs as applicable, and reconciles exact handles and membership. If a wait fails, it retains valid handles and remains cleanup owner. After ownership transfer, the watchdog holds the last bootstrap-job handle; primary failure or closure of its former handle cannot trigger kill-on-close while the watchdog still holds that duplicate. | A hung watchdog combined with primary loss has no established OS fallback; classify `CONTAINMENT_FAILURE`, do not claim the Job Object guarantees cleanup, and keep this an explicit blocker. |

For each startup failure, issue the applicable exact-handle or whole-helper-
job termination request immediately and record each API result. Startup and
registration acknowledgments are bounded at 100 ms; no workload may be
created after `T0+115s`. A failed helper wait is not retried as a workload:
record `TERMINATION_UNCONFIRMED`, continue bounded job reconciliation, and
preserve the evidence-incomplete disposition. Active workload termination
requests are immediate at the 115/120-second points and at any loss of
required observer/controller coverage. The watchdog reserves the final
100 ms before `T0+135s` for bounded termination/reconciliation and status
handoff. The D9 observation window never permits workload execution. At
`T0+135s`, any uncertain workload, observer, watchdog, ETW session, or
required job membership is `CONTAINMENT_FAILURE`; preserve what was
committed, mark missing evidence explicitly, and never claim guaranteed
physical termination. Exact OS cleanup behavior on simultaneous trusted
controller loss is not established here.

## 4. ETW and Q03 assurance decision

Job Object membership/accounting and `IsProcessInJob(process, intendedJob)`
are the ordinary authoritative APIs for whether a currently observed
process is a member of the intended job. Creation-time
`PROC_THREAD_ATTRIBUTE_JOB_LIST`, disabled breakaway flags, and read-back
prevent ordinary child breakaway when their supported semantics and
effective configuration hold. Job queries do **not** enumerate a process
created outside that job through a broker, service, or remote-process path.
Therefore Job Object APIs alone cannot establish the broader Q03 claim
that no relevant outside-job descendant exists.

ETW process start/stop events provide timestamped observer records and
potential identity/parent-correlation evidence when configured and
loss-free. Consumer callback delivery order is not treated as causal event
order; correlate using documented event timestamps/clock conversion and
preserve ordering uncertainty. ETW
does not assign job membership, prevent process creation, guarantee complete
coverage under event loss/provider failure, or guarantee termination of a
protected or service-owned process. Treat it as necessary diagnostic and
detection evidence for a Q03 detect/recover claim, **not** as an
OS-enforced containment boundary.

When the kernel process provider is used, the concrete documented
process-start-key control is `EnableTraceEx2` with
`ENABLE_TRACE_PARAMETERS.Version =
ENABLE_TRACE_PARAMETERS_VERSION_2` and
`EnableTraceParameters.EnableProperty =
EVENT_ENABLE_PROPERTY_PROCESS_START_KEY`. A successful call establishes
only that the requested property was enabled for that provider/session; it
does not by itself establish that a particular event's extended-data key
belongs to the event subject, that a pre-existing suspended root receives
a usable start event, or that its key can be read from the exact process
handle. Provider event schema and event-subject binding must be verified
for the pinned Windows/provider version. This resolves the required
enablement control, not the remaining identity-correlation blocker.

Disposition:

- ETW is not required for the narrower source-level assertion that the
  suspended admitted root is assigned to the intended Job Object and
  ordinary descendants cannot use configured breakaway.
- If Phase 2A acceptance requires detect/recover assurance for
  broker/service/remote-created outside-job processes, ETW coverage or a
  separately approved OS-enforced boundary is required on every case for
  which that claim is made. An ETW-disabled run cannot claim Q03 or
  complete whole-tree protection.
- A supervisor may be specified with ETW disabled only under an owner
  decision that limits its assurance claim to verified Job Object members;
  that does not silently satisfy the accepted whole-tree requirement.
- Lost/late/contradictory ETW events, nonzero loss counters, failed
  `ProcessTrace`, observer death, or stale heartbeat immediately invalidate
  Q03 coverage and trigger whole-job termination. Missing event is not
  evidence of no outside process.
- An independent observer is necessary to detect process events not
  represented in workload-job accounting, but the required privileges,
  session authority, event completeness, and cleanup after controller loss
  remain unqualified.

R6 does not remove Q03. Whether Q03 detect/recover is mandatory for every
Phase 2A case versus a narrower documented Job Object claim is an owner
policy question; until resolved, whole-tree assurance remains blocked.

## 5. Memory accounting disposition

The required control candidate remains
`SetInformationJobObject(JobObjectExtendedLimitInformation,
JOBOBJECT_EXTENDED_LIMIT_INFORMATION)` with
`JOB_OBJECT_LIMIT_JOB_MEMORY` and exact `JobMemoryLimit = 268435456`
bytes; read back before workload resume. The measured high-water source is
`PeakJobMemoryUsed` from the same information class. The observed per-process
diagnostic is `PROCESS_MEMORY_COUNTERS_EX.PrivateUsage` from
`GetProcessMemoryInfo`, summed over a complete identity-checked member list.
The Job Object charge includes all processes associated with that job;
descendant coverage is therefore only the set actually associated with it.

Microsoft's public `JOBOBJECT_EXTENDED_LIMIT_INFORMATION` reference says
`JobMemoryLimit` limits virtual memory that can be committed for the job
and `PeakJobMemoryUsed` is peak memory usage of processes associated with
the job. The `PROCESS_MEMORY_COUNTERS_EX` reference defines `PrivateUsage`
as process commit charge/private usage. Those documents do not state that
the job's measured charge is exactly the contemporaneous sum of each
member's `PrivateUsage`, nor define a conservative ratio or additive
overhead. It is not responsible to infer either equivalence or a stronger
limit from the shared phrase “commit.”

**Classification: C — non-equivalence has not been ruled out by authoritative
documented semantics; explicit owner-policy amendment is required.** Do not
call the sampled `PrivateUsage` sum a hard enforcement mechanism: sampling
is non-atomic and can miss peaks. Do not call `PeakJobMemoryUsed` the
accepted metric without a documented mapping.

Narrow owner decision requested before implementation authorization:

1. Either explicitly amend the Phase 2A enforced metric to the documented
   Job Object job-commit charge at the unchanged 268,435,456-byte threshold,
   retaining per-process `PrivateUsage` only as a labeled diagnostic; or
2. Retain the exact concurrent-private-commit acceptance and provide an
   authoritative conservative enforcement mapping that cannot undercount
   it, or separately authorize a new enforcement mechanism.

Record `PeakJobMemoryUsed`, effective flags/value, memory-limit failures,
allocation failures, and timestamped per-process diagnostics separately.
Job-memory limit behavior on allocation failure and target-build enforcement
require qualification; failed commit alone is not proof that the workload
or descendants ceased.

## 6. Worker and helper profiles

The R2 draft did not contain enough owner-supplied facts to freeze exact
profiles. R6 states required fields and refuses to invent user names, SIDs,
paths, privilege lists, or executable hashes. These profiles must be
completed and approved before any implementation authorization.

| Role | Executable / identity requirements | Token, privileges, groups, integrity | Environment, handles, cwd, paths | Authority and unresolved profile fields |
|---|---|---|---|---|
| Primary controller | Exact reviewed source bytes and interpreter image identity; trusted invoking account and process instance pinned. | Restricted primary token profile must specify token type, enabled/disabled groups, restricted SID set, integrity, and only required privileges. `SE_INCREASE_QUOTA_NAME`/other requirements must be justified; no assumed elevation. | New explicit Unicode environment; no inherited caller environment; exact cwd and profile path; evidence writer only writable target; explicit handle list; no workload result authority. | Owns admission/evidence and original Job Object handles; may create only fixed internal modes. Exact account, executable digest, token SIDs, env values, cwd, ACLs, and paths remain owner/profile blockers. |
| Watchdog | Same allowlisted source/interpreter identities with fixed watchdog mode; exact process creation identity registered. | Separate minimum token. Must state process/job query/termination rights and ETW session stop authority, if it performs Q03 cleanup. | Constructed exact environment; only private channels, caller-status endpoint, duplicated exact process/job handles; no evidence file writer or workload path. | Must terminate/reap workload and observer resources without relying on primary. ETW privileges and session ownership/cleanup semantics remain unverified. |
| Optional ETW observer | Fixed internal mode, pinned interpreter/source, run-scoped nonce; process/thread instance created suspended. | Minimum profile capable of required kernel process tracing and session control; enumerate required privilege/enablement explicitly from supported API docs and qualification; no blanket admin assumption. | Exact constructed environment; receives only control/event channel and required session data; no workload evidence directory or arbitrary writable path. | No workload Job Object authority; cannot resume itself before watchdog owns exact process/thread/job handles. Session cleanup under abrupt observer/watchdog failure remains blocker. |
| Untrusted Phase 2A worker | Exact Python executable, package/library tree and test fixture revision/hash; exact command/argv and cwd. | Restricted primary token created with exact expected group/privilege set and low integrity; unique restricting SID; write-restricted; no token/profile ambiguity. | Only fixed Unicode environment variables; explicit pipe handles only; read-only source/interpreter inputs; no evidence-directory access; no arbitrary writable path; network denied if available via an approved OS boundary. | Assigned to workload Job Object at creation; no Job Object handle or termination authority; no unrestricted process creation/broker rights. Full filesystem/network/process-creation denial requires OS-enforced checks and qualification, not environment variables. |

An environment allowlist is determinism/hygiene, not a security boundary.
ACL `AccessCheck` probes cover only enumerated objects and do not establish
absence of alternate paths, reparse/hard-link aliases, registry writes,
network, broker, or service routes. Every profile must distinguish requested
policy from Windows-enforced controls and from controls that have only been
qualified on the pinned host. Exact profiles are unavailable; this remains
an implementation authorization blocker.

## 7. Q03 process identity and recovery

The existing R2 candidate is `NtQueryInformationProcess` with
`ProcessTelemetryIdInformation` (class value 64) on the exact process
handle. It may be compared with an ETW process-start key only if the selected
provider's event schema establishes that the event's key identifies the
created process rather than the process logging the event. The ETW
structure reference by itself does not establish that provider-specific
binding. The process start key is used as process-instance identity only
after that binding is documented and validated; PID alone is insufficient.
A candidate identity chain must include:

1. ETW process-start event PID, parent PID/instance key, event timestamp and
   event-clock conversion, and a process start key only if the selected
   provider's schema establishes that the key belongs to the created
   process (not merely the process logging the event), with run/session
   identity and no loss.
2. The primary/watchdog opens an exact live process handle with query and
   synchronization rights; `GetProcessId` and `GetProcessTimes` creation
   time bind the handle to the observed PID/process instance.
3. Query class 64 on that same handle; require successful status, expected
   returned structure length/fields, matching process ID and
   `ProcessStartKey`. The observer event key and native query must agree.
4. Call `IsProcessInJob(exactHandle, intendedWorkloadJob, &inJob)` on the
   same identity-bound handle. For a required outside-job termination,
   obtain/retain a handle with `PROCESS_TERMINATE`, repeat identity checks
   on that exact handle, then terminate and wait on that same handle;
   never reopen by PID between check and termination.
5. Correlate process stop events by PID plus start key only when the event
   schema binding has been established; require loss-free start/stop
   coverage and pair with direct process-handle/job observations. Missing
   parent, key, schema binding, stop, access, or loss information means
   ambiguous identity and `TERMINATION_UNCONFIRMED`, not guessed cleanup.

The public `NtQueryInformationProcess` documentation warns the function may
change or be unavailable, while class-64 structure support/rights are not a
stable cross-version guarantee. No simpler documented supported interface
was established in this review that supplies the ETW process-start key for
the exact handle. `GetProcessInformation` does not document class 64.
Therefore the class-64 method remains a version-pinned candidate only:
pin Windows build/UBR, SDK declarations, ntdll export, structure layout,
status codes, rights, and process-key correlation; independently qualify
against PID reuse, event loss, races, nested/enclosing jobs, access denial,
and exit/termination behavior. It is not qualified by contract text.

Q03 remains blocked unless owner accepts this candidate and its qualification
or authorizes a supported alternative/OS-enforced boundary. ETW start/stop
events are supplementary detection evidence, not job membership proof or
prevention. A missed/lost event, unsupported query, process access denial,
or identity mismatch stops admission and causes fail-closed termination
requests; unconfirmed identity is never killed by PID alone.

## 8. Artifact and ledger requirements

The retained-artifact cap remains exactly 1,048,576 bytes. R2's sole trusted
writer and byte-accounting design is retained as a proposal: pre-reserve all
categories; count compressed/finalized artifact bytes, temporary files,
manifests, hashes, invocation and failure records, stdout/stderr, JSONL
ledger, and exports against the same hard total; account high-water before
each write/rename; never silently truncate, omit, or discard a mandatory
record. On writer failure, cap exhaustion, failed flush/hash/rename, or
missing mandatory evidence, stop admission/terminate active work and report
`EVIDENCE_INCOMPLETE`. Do not promise a durable failure manifest if the
writer/storage itself has failed. The watchdog is not a second file writer.

Each one of up to 8,196 target-counter probes requires a lossless JSONL
record with stable schema/version, run nonce, record/ingest sequence,
probe index and target identity, operation/outcome, target and coupled
counter deltas, status/error, QPC/frequency, and relevant CPU/wall/memory/
termination state. The invocation/profile/source identities, stdout,
stderr, final resource summary, failures, and file/hash manifest are
mandatory as specified in the R2 evidence design. Compression is lossless;
gzip trailer/finalization, temporary intermediates and final-path bytes
must fit within the same total.

The proposed R2 reservations total 1 MiB (ledger 786,432; stdout/stderr
32,768 each; invocation/resource records 16,384 each; failure/hash
manifests 8,192 each; slack 147,456). They do not prove the 8,196 complete
records fit. Exact analytical upper bound is not established.

**Disposition:** ledger compatibility is unproven and the controlling
proposal requires a separately authorized synthetic sizing prerequisite.
The narrowly scoped future authorization request is: generate only
deterministic synthetic records matching the frozen complete 8,196-record
schema; size the uncompressed records, lossless-compressed result,
compression trailer, required manifests/hashes, stdout/stderr maxima,
temporary/final-path overlap, and failure reserve against the exact
1,048,576-byte total; retain a bounded report of per-category and
high-water bytes; do not import/invoke the supervisor, fixture, TPCN
modules, or benchmark, and do not access network/datasets. The request
must bind exact schema and generator identities and be separately reviewed
and authorized before execution. No sizing is authorized here. If complete
evidence cannot fit, stop and request an owner decision; do not raise the
cap or drop evidence.

Filesystem controls do not follow from pipe capture. Worker access to all
controller-owned evidence paths must be denied by a pinned ACL/security
boundary; enumerate and qualify alternate filesystem, reparse, hard-link,
temporary, and export paths. Until proven, direct unaccounted writes remain
a qualification/security blocker.

## 9. Termination, cessation, and evidence timeline

Record immutable controller `T0` and QPC frequency. Monitor job aggregate
CPU from the pre-resume user/kernel accounting baseline; sample target
10 ms. Synchronous query, termination, and evidence operations run on
separate, single-flight operation workers, never on the watchdog's control
loop. Query and evidence operations cannot block termination. Termination
requests for the workload job, observer job, watchdog process, and primary
process use independent target-specific workers and can be dispatched
concurrently; no unresolved request for one target may serialize another
target's cleanup. The watchdog control loop waits on completion events,
process/channel events, and a deadline timer using
`WaitForMultipleObjects`; each timeout is no later than the earliest next
10-ms sampling point, 100-ms accounting-gap limit, `T0+115s`, `T0+120s`,
`T0+134.9s`, or `T0+135s` obligation. It rechecks QPC/deadlines after every
wake. Waitable-timer and scheduler delays are not OS timing guarantees;
late wake/query is recorded as a gap/overrun and cannot pass. A worker
timeout is outstanding/inconclusive, not success, and no duplicate
operation for the same target is started merely to hide the first
unresolved call. The separately required watchdog termination escalation
at `T0+120s`, and the `T0+134.9s` final cleanup requests, are distinct
controller/deadline actions and must each be recorded; they are not
workload retries. A failed accounting query or any gap above 100 ms
immediately closes admission, dispatches whole-job termination on the
independent workload-target lane, and makes CPU accounting incomplete; it
cannot yield a successful result. At the first observed
aggregate CPU `>=120s`, request whole-job termination immediately. This is
a monitored trip point, not a demonstrated instantaneous hard cap: sampling
and termination latency can produce overshoot, which must be reported as
`CPU_OVERRUN` using the greatest observed aggregate value and request
timestamp. No positive overshoot is authorized by this design. At
`T0+115s`, request whole-job termination if active; at `T0+120s`, the
independent watchdog issues/escalates the request if active. A termination
API return is a request result, not cessation.

For cessation, record:

- `last_active_observation`: QPC, source, successful accounting
  `ActiveProcesses > 0`, complete nonempty PID-list identities/count, and
  any required known member process handles observed nonsignaled.
  `WaitForSingleObject(handle, 0) == WAIT_TIMEOUT` means the process handle
  was not signaled as terminated at that observation; `WAIT_OBJECT_0` means
  the process handle is signaled (terminated). `WAIT_FAILED`, unexpected
  return values, or missing `SYNCHRONIZE` rights make that process
  observation inconclusive. Never describe a signaled process handle as
  active.
- `first_empty_observation`: QPC, source, successful
  `JobObjectBasicAccountingInformation.ActiveProcesses == 0`, complete
  `JobObjectBasicProcessIdList` empty, known member handles signaled, and
  required pipe endpoints/readers at EOF. Each previously retained member
  handle must return `WAIT_OBJECT_0`; `WAIT_TIMEOUT` or `WAIT_FAILED` is
  contradictory/inconclusive and prevents the empty observation from
  passing. If Q03 is required, ETW start/stop reconciliation must also be
  loss-free and agree.
- Per-source query/API status, QPC frequency, job identity, PID plus
  creation/start-key identities where available, request sequence/QPC,
  job-completion observation QPC, and final evidence commit QPC.
- The observed interval `[last_active_observation_qpc,
  first_empty_observation_qpc]`; do not synthesize an exact process exit
  time. D10 is not satisfied if the prior active observation or first
  successful empty observation is absent.

Budget-compliant success requires both (a) a valid observed-cessation
interval whose upper endpoint is no later than `T0+120s`, and (b) completion
of the final success-evidence commit no later than `T0+120s`. If either
endpoint/commit is later, or the cessation interval straddles the deadline,
classify `WALL_BUDGET_UNCONFIRMED`/`WALL_OVERRUN` as applicable and do not
report a budget-compliant success. The D9 post-deadline interval allows
observation, cleanup, and preservation of failure/incomplete-evidence
records only; it does not extend permitted workload execution or cure a
late success-evidence commit. If the workload remains active at the
120-second escalation point, request termination, but do not infer that the
request stopped execution.

Job handle signaling, completion-port notifications, root exit, successful
`TerminateJobObject`, or ETW alone cannot establish the full cessation
contract. Reconcile direct Job Object accounting and complete PID list.
ETW, when Q03 is selected, is additional evidence; if sources disagree,
classify containment failure and preserve both observations.

At `T0+134.9s`, if required cleanup or a valid caller-status handoff is
absent, the watchdog requests termination of any remaining workload and
observer helper-job members and requests termination of a nonexiting
primary through its exact retained process handle. It uses the remaining
100 ms only for finite waits, job/process queries, and the final
failure/incomplete-status attempt; every wait receives only the remaining
deadline duration. At `T0+135s`, it starts no new query, cleanup, or
observation operation. Any operation worker still pending is recorded as
`OUTSTANDING_AT_CUTOFF`; the watchdog does not wait past the cutoff, does
not treat a queued or attempted status as committed, and reports
`EVIDENCE_INCOMPLETE` if the failure record was not committed. The control
loop remains responsive because it does not execute synchronous query,
termination, or evidence operations inline. A pending operation may
continue after the logical cutoff; this is not workload authority or proof
of cleanup, and its state remains explicitly unconfirmed. The watchdog
must not call a potentially blocking
`ControlTraceW` synchronously on its control loop. It sends a bounded,
overlapped stop request over the command endpoint to the already-running
observer, which calls `ControlTraceW(..., EVENT_TRACE_CONTROL_STOP)` using
the exact run-scoped session identity and returns the API result through
the status endpoint.
The watchdog monitors the observer's exact process handle and bounds the
response wait by `T0+135s`. If observer/session cleanup remains unresolved
at `T0+134.9s`, it dispatches both the stop request and observer-job
termination through their independent target-specific lanes; it records
any API result that arrives, but does not infer that the session stopped
from a request or process termination. At `T0+135s` no new cleanup request
starts; pending stop/termination work is classified as outstanding and
unconfirmed.

No API completion or physical process cessation is guaranteed by this
logical cutoff. If a wait/query/status operation remains outstanding at
`T0+135s`, record the last completed observation, classify the affected
state `CONTAINMENT_FAILURE`/`TERMINATION_UNCONFIRMED` or
`OBSERVER_CLEANUP_UNCONFIRMED`, preserve available failure evidence, and do
not report success. No additional workload execution is permitted. The
controller stops initiating bounded observation and reports only what was
last successfully observed; it does not assert the workload is Off.
Preserve available evidence and mark incomplete categories. Separate
workload cessation interval from watchdog/observer/ETW cleanup intervals.
Do not report success while a mandatory observer/watchdog remains unmanaged
or unobserved.

## 10. Traceability and gates

| Requirement | Design/source obligation | OS/API semantic question | Runtime qualification | Owner decision / status |
|---|---|---|---|---|
| Admission and Job Object | Freeze exact command/source/fixture/profile; configure/read back job; create suspended with creation-time job-list/explicit pipe-handle list; verify exact-handle membership, accounting count, complete PID list and limits before exact-thread resume; terminate/reconcile on any failure | Target OS, enclosing/nested job and creation failure semantics | Exact host, races, containment, cleanup and untrusted-code nonexecution | Source contract specified; runtime unqualified |
| Watchdog/observer lifecycle | Watchdog assigned to primary-owned kill-on-close bootstrap job, nonobserving and ready before observer exists; observer suspended, registered by exact handles, watchdog-owned activation; workload/helper jobs have kill-on-close fallback; no workload until observer ready | Job close/ETW session lifetime, remote handle rights, ControlTrace ownership | Crash at every transition; simultaneous controller loss; session stop/reap | **Unresolved: ETW session cleanup after all trusted controllers fail is not established** |
| D9/D10 timing/cessation | 115/120/135 absolute points; fail closed on accounting gaps; observed CPU overshoot; cessation interval and final success-evidence commit must meet the 120-second wall deadline | QPC/wait/job query semantics | Sampling gaps, blocking-call deadlines, termination latency, contradiction and deadline tests | D9/D10 accepted for design only; overshoot is not authorized |
| Memory | `JobObjectExtendedLimitInformation`, `JOB_OBJECT_LIMIT_JOB_MEMORY`, exact 268435456; record peak and sampled PrivateUsage separately | Job commit charge is not documented as exact concurrent private-usage sum | Target allocation denial and counters | **Classification C; owner metric amendment required** |
| Identity profiles | Freeze exact primary/watchdog/observer/worker executable, account, token, groups, privilege, integrity, environment, handles, paths, network/process rights | Restricted-token, ACL, ETW privilege and API semantics | Effective denial, path aliases, target host | **Profile missing; implementation blocker** |
| Q03 | ETW process start/stop, start key, exact-handle class-64 identity candidate; same-handle membership/termination | Version-sensitive `NtQueryInformationProcess` class 64 | Pinned build/UBR, loss, PID reuse, races, access denial, recovery | **Owner acceptance/alternative required; unqualified** |
| Evidence cap | One writer, complete schema, exact byte checks, lossless compression, no truncation | Filesystem/rename/hash semantics | Crash, cap, stalls, max ledger fit | **8,196 records not sized; prerequisite remains separately authorized** |
| Execution authority | Single implementation file only; no static check under this request | Not applicable | Separate authorization needed | **Implementation and static validation NOT AUTHORIZED** |
| Scientific separation | No fixture/production edits; Phase 2A only in a later authorization | Not applicable | No workload run | Phase 2B and Spiral remain prohibited |

Statuses are distinct: R6 design draft is **not implementation**; a future
implementation may be **implemented but unqualified**; only separate
runtime qualification and owner Authorization Q could establish
**independently qualified for execution**. Contract PASS would mean
contract-ready-for-owner-authorization only.

## 11. Independent review and publication boundary

Fresh exact-byte reviewers are required:

- **A:** watchdog readiness, observer ownership/activation, suspended
  admission, handle transfer, and fail-closed lifecycle.
- **B:** D9/D10, CPU/wall sampling, 15-second observation, cessation
  intervals, and termination/controller failure.
- **C:** memory mapping, exact profiles, Q03/ETW authority, artifact
  enforcement and ledger-sizing prerequisites.
- **D:** provenance, D9/D10 decision fidelity, scope, Luna-64 isolation,
  and Luna-63C freeze.

Each reviewer must distinguish source design from documented OS semantics
and runtime qualification. Integrated allowed results are:

**PASS — R6 CORRECTIVE CONTRACT READY FOR OWNER AUTHORIZATION**

or

**BLOCKED — R6 CORRECTIVE CONTRACT INCOMPLETE**

This draft is expected to remain blocked while §10 owner and technical
gates remain open. If blocked, preserve draft and findings; do not update
the authoritative workflow, stage, commit, push, or publish a PASS claim.
Only on integrated PASS may the separately reviewed governance publication
allowlist include this R6 contract and the necessary workflow update.
Exact staged-byte/Git-blob review, commit, push, fetch, remote ancestry and
hash verification are still mandatory; none authorizes source implementation.

## 12. Current boundaries and references

**Supervisor source implementation: NOT AUTHORIZED.**

**Static validation: NOT AUTHORIZED.**

**Supervisor qualification: NOT AUTHORIZED.**

**Synthetic ledger sizing: NOT AUTHORIZED.**

**Phase 2A direct-counter fixtures: NOT AUTHORIZED.**

**Phase 2B network fixtures: NOT AUTHORIZED.**

**Full Spiral execution: BLOCKED.**

**Luna-64 corrective execution: BLOCKED.**

**Luna-63C certification: FROZEN.**

No TPCN architecture clause or ACP is changed. No code, ETW collector,
test, sizing case, fixture, or benchmark was executed.

References:

- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information)
- [PROCESS_MEMORY_COUNTERS_EX](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-process_memory_counters_ex)
- [CreateProcessAsUserW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasuserw)
- [UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)
- [ENABLE_TRACE_PARAMETERS](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-enable_trace_parameters)
- [EnableTraceEx2](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-enabletraceex2)
- [EVENT_EXTENDED_ITEM_PROCESS_START_KEY](https://learn.microsoft.com/en-us/windows/win32/api/evntcons/ns-evntcons-event_extended_item_process_start_key)
- [NtQueryInformationProcess](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntqueryinformationprocess)
- [ETW overview](https://learn.microsoft.com/en-us/windows/win32/etw/about-event-tracing)
