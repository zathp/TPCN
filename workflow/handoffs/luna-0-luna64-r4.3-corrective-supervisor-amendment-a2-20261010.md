# Luna-0 — Luna-64 R4.3 Corrective Supervisor Amendment A2

**Amendment ID:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A2`
**Status:** Governance proposal; independent prereview pending
**Parent gate:** `L64-TB-R4.3-CORRECTIVE-20261010`
**Parent gate SHA-256:** `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369`
**Owner authorization commit:** `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`
**A1 publication commit:** `d20aab249e42575ccc571c9c72153a3bb4b412db`
**Corrective baseline:** `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`
**Proposed disposition:** **Option D — remain blocked**

This is governance-only work. It does not amend the frozen R4.3 scientific
protocol, implement the reward correction, execute a supervisor or
qualification case, consume any test allowance, or authorize scientific
work. The existing reject-only malformed second-reward-origin acceptance is
preserved as part of the original corrective authorization; no new
malformed-input policy is introduced.

## 1. Reconciled predecessor evidence

The following were checked against the repository and current worktrees:

| Identity | Reconciliation |
|---|---|
| Parent gate | The published handoff file SHA-256 is `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369`. |
| Parent authorization | Commit `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a` exists and is an ancestor of A1 publication commit `d20aab249e42575ccc571c9c72153a3bb4b412db`. It authorized the parent corrective scope and reject-only malformed second-origin policy, not a changed resource policy. |
| A1 amendment | Published file SHA-256 is `40A5085CB6B11047013DC0701DB56DEEF5FA7A32A6E76FAA29B7A2A2D2B213E4`. |
| A1 independent review | Published file SHA-256 is `4287E7C34A9E51DB5A976F3AB36B1149706C76195F71B711160F78C1719A8365`; verdict **BLOCKED — RESOURCE SUPERVISION UNRESOLVED**. |
| A1 publication | Commit `d20aab249e42575ccc571c9c72153a3bb4b412db` is published on `governance/luna64-r4.3-freeze-20261010`. |
| Corrective worktree | Branch `experiment/luna64-r4.3-reward-lifecycle-correction-20261010` is clean at `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`. |
| Execution marker | `%LOCALAPPDATA%\TPCN\luna64-r43-corrective-implementation-20261010.json` is absent. |
| Corrective execution artifacts | The corrective supervisor and corrective evidence directory are absent from the corrective worktree. No corrective tests or supervisor qualification were run for this amendment. |
| Original pilot | The original closure remains **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not an efficacy result; its pilot budget remains exhausted. |
| Protocol and isolation | The frozen R4.3 protocol and original pilot evidence are not changed. Luna-63C remains isolated. |

These repository and marker checks do not prove that no unrecorded process
ever ran outside retained evidence; no such broader claim is made.

## 2. Formal bootstrap boundary

The proposed two-component design has:

- **Component A — trusted bootstrap launcher:** creates/configures a private
  Job Object, launches Component B suspended, checks containment and limits,
  and supervises failure/timeout cleanup. It must never run a benchmark,
  corrective test, training, or scientific workload.
- **Component B — contained corrective supervisor:** runs only after it and
  its descendants are within the verified job boundary; it may coordinate
  only the three exact parent-gate focused tests in their existing order.

Windows Job Objects do not retroactively bound the process that creates the
job. Without a separately verified outer boundary already in force before
Component A starts, Component A is outside the inner job until it has
created and configured that job and launched/assigned B. Its memory, CPU and
wall time during that interval are not hard-limited by the inner job.
Measuring that interval after the fact does not enforce a maximum.

| Operation | Executor and boundary | Required rights / maximum | Failure modes and evidence | Fail-closed result |
|---|---|---|---|---|
| Start A | External caller starts A. No approved outer job, VM, or container boundary is established for A. | One launcher start; ordinary process-creation rights. The caller's privilege/job context is unknown until queried. | Record parent identity, token/session, job membership and launch time. Failure or inability to establish those facts leaves A's pre-job resource usage unbounded. | Do not claim containment; no corrective invocation. This is the unresolved bootstrap interval. |
| Create private job | A, outside the proposed inner job. | One `CreateJobObject` call; handle ACL must be private and non-inheritable. | Record returned handle identity/ACL and error. Failure leaves no job boundary. | Exit without creating B. |
| Configure hard limits | A, outside the proposed inner job. | One verified configuration transaction per required information class. The job handle needs `JOB_OBJECT_SET_ATTRIBUTES` and `JOB_OBJECT_QUERY`; process assignment needs `JOB_OBJECT_ASSIGN_PROCESS` plus target-process `PROCESS_SET_QUOTA` and `PROCESS_TERMINATE` rights unless creation-time association is used. | Record `SetInformationJobObject` inputs, results and query-back values. Partial configuration or API/version incompatibility is failure. | Terminate any suspended child; do not resume anything. |
| Configure advisory notification and completion port | A, outside the proposed inner job. | One completion-port association and one notification-limit configuration if the warning is retained. | Record exact information class/structure, limit flags, values, association and query result. An absent or delayed message is not evidence that the hard limit was or was not reached. | Monitoring setup failure prevents launch. Notification is not enforcement. |
| Configure launcher watchdog / artifacts | A, outside the proposed inner job. | Exactly one watchdog and a fixed output destination; no arbitrary command execution. | Record monotonic start/deadline, command allowlist, and output cap. The watchdog is itself outside any established bound in the current design. | Any watchdog or output-control setup failure prevents launch. |
| Create B suspended | A, outside the proposed inner job. B must not execute authorized code yet. | One `CreateProcess` with `CREATE_SUSPENDED`; a creation-time job list may be used only if supported and verified. No fallback to running B before assignment. | Record image path/hash, argv, PID/TID, creation flags, job-list attributes and return codes. | On any uncertainty, terminate B while suspended and close handles. |
| Assign B to job | A, outside the proposed inner job. | One assignment, with required job/process access rights; or one creation-time job association. | Record `AssignProcessToJobObject` / process-attribute result and subsequent `IsProcessInJob`/job PID-list evidence. Existing incompatible outer jobs or access denial are failure. | Terminate B suspended; never resume it. |
| Verify pre-resume limits and membership | A, outside the proposed inner job. | Query each configured information class and B's membership/affinity before one resume. | Record exact values, active process list, affinity mask, enclosing job context and timestamp. Host policy may silently impose more restrictive effective limits. | Any unavailable or mismatched query blocks resume. |
| Resume B | A, outside the proposed inner job. | One resume only, after all checks pass. | Record successful resume and monotonic time. A resume API failure is fatal. | Terminate B/job and do not retry under the one-shot authorization. |
| Spawn focused test children | B, required to be in the configured job before it starts. | At most the three exact allowlisted child commands, serially once each. Use ordinary `CreateProcess` with `CREATE_SUSPENDED`; descendants normally join the parent's job. No WMI launch, breakaway flag, arbitrary command, or alternate executable. | Record PID, full command identity, inherited job membership, effective affinity and resume. Verify each child before resuming that child. | On failed child membership/affinity or unexpected process, terminate the job; do not start another child or retry. |
| Advance/run and enforce watchdogs | B monitors the tests; A is required as an independent watchdog/cleanup owner. B and children are in the job; A is not in the inner job. | Parent limits remain one core, 120 aggregate CPU seconds, 180 aggregate wall seconds, and 5 MiB artifacts. Qualification budget is separate and unapproved. | Job user-time limits are user-mode accounting and are checked periodically; they are not wall-clock enforcement. Wall time needs an external watchdog. Record job accounting plus per-process counters and missing telemetry. | Any cap breach, incomplete monitor, query failure, timeout, or unexpected exit stops execution and triggers job termination. This policy cannot be guaranteed while A itself has no pre-existing boundary. |
| Handle allocation failure / limit violation | The allocating process first sees commit failure; A/B monitors attempt to identify/report it. | No more commits above an enforced job commit cap, if that alternative is later approved and configured. No automatic job termination is implied by commit denial. | Record allocation API/status when available, hard-limit configuration, job violation query and notification timeline. A failed allocation may be handled by the application and execution may continue unless explicitly aborted. | Any observed/ambiguous limit event aborts and terminates the whole job. Missing telemetry is `INCOMPLETE`, never a clean pass. |
| Failure cleanup | A must remain alive to terminate the job, or a separately trusted external owner must do so. | `TerminateJobObject` or guaranteed last-handle close under `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; verify no associated process remains. | Record termination request, exit codes, remaining job PIDs, process handles and close order. A crash of A/B, leaked duplicate handle, or inaccessible job can undermine cleanup. | If tree termination cannot be verified, report failure and do not continue. |
| Close handles/finalize | A and B, both with explicit ownership; B exits after A has reconciled results. | Close all handles exactly once; only A retains the job handle needed for termination. | Record final accounting/query status, exit codes, artifact bytes, handle ownership and job-empty notification/query. | Missing final accounting or live descendants means incomplete/failed; no PASS. |

### Unbounded interval

Under the currently evidenced environment, A's execution from process start
through job creation, hard-limit installation, child assignment and resume is
not inside a verified resource boundary. The inner Job Object can constrain
B and included descendants only after association. This interval cannot be
closed by reporting A's measured peak after launch. No separately authorized
external job/service, container, VM, or trusted launcher contract has been
established for this task.

## 3. Component interaction and bootstrap alternatives

If a future approved external boundary exists, Component A and B should use
a fixed, local, versioned, size-capped request/response channel (inherited
pipe or private named pipe with an ACL restricted to the current identity).
The request may contain only the gate ID, exact worktree revision, mode
`All`, and the fixed test allowlist; no shell fragments, arbitrary paths,
environment overrides, or dynamically selected commands. B returns a
bounded structured status and artifact manifest. A validates schema,
sequence number, process identities and exit status before finalizing.
Channel loss, malformed/oversized data, duplicate messages, or supervisor
death is fatal. This channel does not itself establish resource containment.

| Alternative | Assessment |
|---|---|
| **A — Separately bounded launcher** | Potentially acceptable only if an already controlled external parent places A under an enforceable boundary before A executes and limits A's resources separately from B's corrective-workload budget. No such parent/job or launcher allowance is established or authorized here. A cannot self-assign retroactively and then claim its earlier resources were bounded. |
| **B — Explicit minimal bootstrap exception** | Not selected. A finite operation count, short maximum lifetime, and sampled memory/CPU are useful audit constraints but do not enforce a maximum. Calling an observed resource maximum an enforced budget would repeat the A1 defect. No exception is authorized. |
| **C — Externally managed containment** | Not selected. No available, independently authorized OS service, container runtime or VM policy is evidenced as launching A already inside the required boundary. A container/VM metric would also need its own explicit accounting definition and would not automatically equal Windows aggregate working set. |
| **D — Remain BLOCKED** | **Selected.** No current candidate closes the bootstrap interval with an evidenced, authorized, fail-closed boundary. This preserves the original aggregate-working-set requirement as unmet rather than substituting an unapproved metric. |

Windows 8 and later support nested jobs; Windows 10 supports
`PROC_THREAD_ATTRIBUTE_JOB_LIST`. These platform capabilities do not prove
that this host's actual parent-job/token/session context permits the proposed
assignment, nor do they bound the process that performs the assignment.
Runtime qualification cannot cure the absent authorization to run it.

The future child/grandchild proof is staged: verify B before resuming B;
after B runs a bounded process-creation fixture, create a grandchild
suspended, verify its job membership and affinity before resuming it, then
verify accounting after its parent exits. A grandchild cannot be checked
before it exists. Working-set observation and artifact output also require
explicit missing-data and overrun fixtures.

## 4. Memory metric and notification semantics

### No resource-policy substitution is selected

The parent gate's required memory condition remains **512 MiB aggregate peak
working set for the supervisor and its complete process tree**. A1's
candidate alternative was a Job Object hard ceiling of
`536870912` bytes (512 MiB) of **job-wide committed memory**, using
`JOB_OBJECT_LIMIT_JOB_MEMORY` and
`JOBOBJECT_EXTENDED_LIMIT_INFORMATION.JobMemoryLimit`. That is a different
quantity. It does not establish, approximate as a proof, or retrospectively
satisfy the original aggregate-working-set requirement. Because this A2
selects Option D, the candidate remains **not selected, not owner-approved,
and not an authorized limit**.

If a future owner-approved amendment considers this alternative, it must
state the exact set of assigned processes and account for the launcher. Job
committed memory includes the sum charged to processes in the configured
job; descendants are included only while assigned to the job hierarchy.
The launcher is excluded from A1's inner-job limit until it is assigned to a
pre-existing parent boundary, which has not been demonstrated. Committed
memory is not resident working set, private working set, kernel memory, or
total machine RAM. `PeakJobMemoryUsed` is committed-memory job accounting,
not a working-set measurement.

Required telemetry distinction:

| Measurement | Classification | Missing data |
|---|---|---|
| Job-wide commit ceiling, if later selected and installed | `ENFORCED` for commits charged to that job, not for out-of-job processes | Configuration/query failure is a gate failure. |
| Job committed-memory high-water (`PeakJobMemoryUsed`) | `MEASURED` job accounting, never working set | Missing value is `INCOMPLETE`. |
| Per-process current `WorkingSetSize` | `MEASURED` observation | Missing process/sample is `INCOMPLETE`, never zero. |
| Per-process `PeakWorkingSetSize` | `MEASURED` lifetime observation for that process | Missing value or PID coverage is `INCOMPLETE`. |
| Sum of sampled process working sets | `MEASURED` simultaneous observation only | It is not a proof of peak aggregate working set over time. |
| Estimated resident/working-set bound from commit ceiling | `ESTIMATED` only; not permitted as acceptance evidence | Must not be reported as enforced. |
| Parent's aggregate peak working-set ceiling | `UNAVAILABLE / NOT ENFORCED` under the evidenced Job Object interface | Remains an unresolved blocker. |

### Hard limit versus warning notification

If a future authorized specification uses a Job Object commit alternative,
the only hard memory ceiling is set through
`SetInformationJobObject(JobObjectExtendedLimitInformation)` with
`JOB_OBJECT_LIMIT_JOB_MEMORY` and the exact `JobMemoryLimit`. A commit that
would exceed this ceiling is denied. The API does not, by itself, promise to
terminate the process or job. The allocating process may handle failure and
continue; the supervisor must treat a verified or ambiguous denied
allocation as fatal and terminate the process tree.

A separate `JobObjectNotificationLimitInformation` configuration is
advisory. Its `JOB_OBJECT_LIMIT_JOB_MEMORY` flag and `JobMemoryLimit` field
describe a notification threshold in that information class; they do not
install the hard ceiling. On crossing, processes may continue allocating
past that threshold until the hard ceiling denies a commit. For a future
proposal only, an exact 480 MiB threshold would be
`503316480` bytes. It is not selected or authorized by A2; the earlier
“one page below” formula is withdrawn rather than reinterpreted.

With an associated I/O completion port:

- `JOB_OBJECT_MSG_NOTIFICATION_LIMIT` is the advisory-threshold message.
  The monitor must query `JobObjectLimitViolationInformation` and retain the
  exact structure, timestamp and result.
- Ordinary messages, including `JOB_OBJECT_MSG_JOB_MEMORY_LIMIT`, are not
  guaranteed to arrive. Their absence does not establish that no event
  occurred.
- Microsoft documents notifications for the
  `JobObjectNotificationLimitInformation` class as guaranteed to arrive;
  delivery remains asynchronous, not a pre-allocation barrier. A stopped or
  unavailable monitor cannot handle the message in time.
- A missing message or failed query is **INCOMPLETE / FAIL**, never evidence
  that the threshold was not crossed. The hard limit remains the independent
  commit control, but does not rescue missing monitoring or prove
  application-level abort.
- Job memory-limit denial is not automatically equivalent to job
  termination. Explicit supervisor/watchdog termination and verification
  are required.

No warning threshold may be treated as the enforcement mechanism. No
notification event may be used to claim aggregate working-set compliance.

The parent CPU-time term also remains a strict 120-second aggregate ceiling.
`PerJobUserTimeLimit` counts user-mode execution time and is checked
periodically; it is not, by itself, proof that combined user-plus-kernel CPU
time stayed below a strict ceiling. Future qualification must measure job
user and kernel accounting and establish a separately enforceable stop
boundary with demonstrated headroom. If that cannot be established, the CPU
limit remains an execution blocker; it may not be silently redefined as
user-mode CPU time.

## 5. Process-tree containment contract

The intended future contained subtree is B, all three authorized child test
processes, and every descendant they create. The future implementation must
prove all of the following before any test process is resumed:

1. The actual parent job chain, token, session and security descriptor are
   queried. Any incompatible enclosing job, UI restriction, token, or
   assignment permission fails closed; API presence alone is insufficient.
2. B is created suspended and assigned at process creation where available,
   or is assigned while suspended before a single resume. Membership is
   independently queried; a failed or ambiguous check means terminate, not
   resume.
3. B launches children only through the fixed `CreateProcess` allowlist.
   Normal children are expected to inherit job membership. WMI process
   creation, services, shell indirection, `CREATE_BREAKAWAY_FROM_JOB`,
   both job breakaway limit flags, and arbitrary executables are forbidden.
4. Each child is created suspended, its job membership, executable identity,
   command, and effective one-core affinity are verified, and only then is
   it resumed. A child or grandchild outside the job is an immediate failure.
5. A job active-process cap is configured to the qualification or corrective
   maximum and queried back. The exact proposed qualification cap is four
   concurrent processes including B; the parent corrective tests remain
   serial. Unexpected process creation terminates the job.
6. `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` is configured, no job handle is
   inheritable or duplicated beyond the named owner, and `TerminateJobObject`
   is available to the independent watchdog. Last-handle-close semantics
   must be verified; a leaked handle cannot be assumed to kill the tree.
7. Parent/job termination, B failure, a missing completion-port monitor,
   timeout, failed accounting query, or cleanup error triggers job
   termination. The owner verifies the job is empty and records remaining
   PIDs before allowing any subsequent action.
8. Any failed assignment or monitor setup occurs while all children are
   suspended. Terminate suspended processes and close process/thread handles;
   never fall back to unsupervised launch.

Windows documentation supports default descendant association for ordinary
`CreateProcess` children when breakaway is not enabled, and nested-job
hierarchies on current Windows releases. It does not prove this repository's
runtime policy, all indirect process-creation routes, the actual parent-job
context, or the pre-launch bootstrap boundary. Those remain qualification
obligations; because no qualification is authorized, they are unresolved.

## 6. Preserved parent resource terms and qualification proposal

The original corrective allowance is unchanged and remains unconsumed:

| Resource | Parent corrective allowance |
|---|---:|
| Corrective supervisor invocation | 1 |
| Focused child tests | Exactly 3 named tests, once each, in the existing order |
| Combined synthetic stimulus/trace records | 512 maximum |
| CPU allocation | 1 logical CPU |
| Aggregate CPU time | 120 seconds |
| Aggregate wall time | 180 seconds |
| Aggregate artifacts | 5 MiB |
| Scientific workload | Prohibited |

The single parent invocation and three tests are not used for supervisor
qualification. No allowance is replenished, reinterpreted, or consumed by
this governance work.

### Separate, proposed qualification boundary (not authorized)

If and only if a future governance amendment first proves an outer
resource boundary and the owner separately approves this exact qualification
boundary, the proposal is:

- one invocation of a dedicated native-process qualification harness;
- one logical CPU; aggregate CPU time no more than 120 seconds;
- aggregate wall time no more than 180 seconds;
- at most 64 process/trace records and four active processes including the
  contained supervisor;
- at most 5 MiB qualification artifacts;
- candidate inner-job hard commit ceiling 536870912 bytes, **only if**
  separately approved; working-set samples are observations, not a hard
  aggregate limit;
- no corrective child tests, pilot runner, benchmark, training/evaluation,
  scientific data, network, GPU, production/core, ACP, or Luna-63C code;
- a unique A2 qualification one-shot marker, separate from and incapable of
  resetting or consuming the parent corrective marker:
  `%LOCALAPPDATA%\TPCN\luna64-r43-supervisor-a2-qualification-20261010.json`;
- no retry after interruption, failure, or uncertain marker state.

This proposal is not executable under A2: it does not bound its own launcher,
and no owner approval exists for an additional invocation. The qualification
allowance is distinct from the parent corrective allowance and requires
explicit authorization. A qualification run would not count as or authorize
the parent corrective invocation.

### Required deterministic qualification cases

| Case | Expected result |
|---|---|
| Successful pre-execution containment | Verify B and its exact limits/affinity before resuming B; then verify each child and grandchild while suspended before resuming that process. Any mismatch fails before that process executes. |
| Job creation failure | No B/test process starts; nonzero failure record; no fallback. |
| Hard-limit configuration failure or query-back mismatch | No process resumes; close/terminate suspended processes; fail. |
| Suspended B assignment failure | B is terminated while suspended; no test code runs; invocation is consumed if qualification was separately authorized. |
| Direct child and grandchild | Both appear in the expected job/outer chain before resume and remain accounted after child exit. Any escape fails and terminates remaining processes. |
| Denied memory commitment | A controlled commit beyond the hard cap fails; log the failed operation/status and job accounting; supervisor explicitly aborts and terminates. A continuing process is not an automatic OS kill and must be reported as a failure. |
| Hard-limit violation with delayed warning | If this separate notification-only qualification is owner-approved, configure the exact 480 MiB advisory threshold and 512 MiB candidate hard cap. The hard cap prevents over-limit commit regardless of warning timing. Warning arrival is logged as advisory; if required event/query evidence is delayed or absent, result is incomplete/fail, not PASS. |
| Normal below-limit execution | Completes with queried job commit peak and separately sampled per-process working sets; never labels one metric as another. |
| Missing completion-port message | Ordinary-message absence is classified inconclusive. Missing guaranteed notification/query evidence is a qualification failure; no pass based on silence. |
| Supervisor/monitor failure | External watchdog terminates the job, verifies no live descendants and records cleanup; any unverified descendant is a failure. |
| Unexpected child termination | Record child exit, stop later child starts, terminate remaining processes, consume invocation; no retry. |
| Breakaway attempt | Creation fails or the process is proved still contained. Any escaped or unaccounted process is a failure. |
| Nested-job incompatibility | Fail before resume; no fallback to uncontained execution. |
| CPU affinity | B, child, grandchild each report/query one permitted processor mask before resume; any other effective mask fails. |
| CPU time | Aggregate job user and kernel accounting plus limit behavior are recorded. The 120-second policy is not PASS unless a separately enforceable stop boundary and any checking/termination headroom are shown not to exceed the authorized ceiling. `PerJobUserTimeLimit` alone does not establish this. |
| Wall time | Independent watchdog stops the full process tree at 180 seconds; a watchdog outside a verified outer boundary is not acceptable evidence. |
| One-shot marker | Atomic create-new before any probe process; existing, malformed, inaccessible or uncertain marker blocks; failure consumes the invocation and cannot be reset. |
| Artifact cap | Aggregate outputs remain within 5 MiB; output-channel/filesystem failure is fatal and no cleanup may erase failure evidence. |
| Artifact-cap overrun | A controlled write beyond the configured cap is rejected before exceeding 5 MiB; no second destination or unaccounted output is allowed. If the boundary is exceeded or cannot be reconciled, fail and retain bounded failure evidence. |

Qualification must complete and receive independent review before any
corrective implementation can be considered. A passing qualification would
prove only the tested supervisor mechanism under the tested host context,
not scientific efficacy, the original working-set limit unless directly
enforced, or authorization for the parent tests.

## 7. Machine-readable policy

The versioned policy companion is
[`luna64-r4.3-corrective-supervisor-resource-policy-a2-20261010.json`](luna64-r4.3-corrective-supervisor-resource-policy-a2-20261010.json).
Its JSON Schema companion is
[`luna64-r4.3-corrective-supervisor-resource-policy-a2-20261010.schema.json`](luna64-r4.3-corrective-supervisor-resource-policy-a2-20261010.schema.json).
Together they record candidate versus selected controls, process scopes,
exact bytes, measurement classes, allowed executables, qualification cases,
failure classifications and approvals. The schema rejects invalid
structural/status/budget combinations; additional comparisons in the
`validation_rules` are mandatory before any future approval. Current status
is `blocked`; no resource policy replacement is selected.

## 8. Microsoft documentation basis

The review uses Microsoft Win32 documentation:

- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) — default child association, breakaway behavior, completion-port messages, accounting and job termination.
- [JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information) — `JobMemoryLimit`, commit accounting, and `PeakJobMemoryUsed`.
- [JOBOBJECT_NOTIFICATION_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_notification_limit_information) — distinct notification class, advisory behavior, and violation queries.
- [SetInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-setinformationjobobject) and [QueryInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject) — limit setup and evidence queries.
- [JOBOBJECT_BASIC_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information) — job/process user-time and affinity semantics.
- [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject) — required job/process rights and assignment failures.
- [Nested Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs) — hierarchy compatibility and inherited association.
- [Process Creation Flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags) — suspended creation and breakaway flag behavior.
- [UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute) — process-thread creation attributes, including `PROC_THREAD_ATTRIBUTE_JOB_LIST`.
- [JOBOBJECT_ASSOCIATE_COMPLETION_PORT](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port) — completion-port association.

Windows 10 version `10.0.19045` was recorded during A1 reconciliation. The
API documentation shows relevant OS support but is not runtime evidence that
the current token, outer-job chain, privilege context or limits work in this
host. No Job Object or test process was created for A2.

## 9. Independent prereview required

Three independent reviewers, none of whom authored this A2 package, are
assigned separate read-only scopes:

1. **Windows resource enforcement:** validate hard versus notification
   semantics, bootstrap coverage, exact process-tree assumptions, OS rights,
   CPU/wall limits, and the fail-closed cases.
2. **Governance/resource accounting:** reconcile exact predecessors,
   unchanged parent allowances, the separate proposed qualification budget,
   owner-approval boundaries, metrics and non-substitution.
3. **Scientific isolation:** verify no protocol, reward implementation,
   experimental execution, efficacy claim, pilot authorization or Luna-63C
   contamination.

The Luna-0 final disposition must reconcile their findings against this exact
proposal and its policy JSON. Required outcomes are:

- **PASS — A2 READY FOR OWNER AUTHORIZATION**, or
- **BLOCKED — RESOURCE SUPERVISION UNRESOLVED**.

A PASS would be prereview only; owner approval would still be required for
any changed resource definition and qualification boundary. Under the
currently verified evidence, Option D is the proposed disposition and the
original working-set condition remains unsatisfied.

## 10. Current authorization boundaries

- A2 amendment approval: **not obtained**.
- A2-selected replacement memory policy: **none**.
- Supervisor qualification invocation: **not authorized**.
- Parent corrective supervisor invocation: **not run; allowance unused**.
- Three focused tests: **not run; allowance unused**.
- Corrective implementation: **not authorized by A2; blocked by unresolved
  resource boundary**.
- Scientific rerun: **not authorized**; original pilot budget remains
  exhausted.
- Frozen R4.3 protocol, pilot closure and artifacts: **unchanged**.
- Production/core or ACP changes: **none**.
- Luna-63C: **untouched and isolated**.
