# Luna-0 — Luna-64 Corrective Supervisor Resource Amendment A1

**Amendment ID:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A1`
**Status:** **BLOCKED — RESOURCE SUPERVISION UNRESOLVED**
**Parent gate:** `L64-TB-R4.3-CORRECTIVE-20261010`
**Parent gate SHA-256:** `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369`
**Parent gate publication:** `439c0c930489ed032dc10950bbd51fe3f153d05a`
**Parent owner-authorization commit:** `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`
**Corrective baseline:** `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`
**Corrective branch/worktree:** `experiment/luna64-r4.3-reward-lifecycle-correction-20261010` / `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna64-r4.3-reward-lifecycle-correction-20261010`

This is a governance-only proposal. It does not amend the frozen scientific
protocol, authorize implementation, authorize any focused test, consume the
parent gate's one-shot allowance, or authorize a scientific workload.

## 1. Reconciled authorization and execution state

The parent gate's final published bytes match its specified SHA-256. Its
independent prereview returned **PASS — CORRECTIVE GATE READY FOR OWNER
AUTHORIZATION**. The repository owner separately authorized that gate and
explicitly accepted its reject-only malformed second-reward-origin policy.
That approval remains valid for the original corrective scope, but does not
approve this changed memory metric.

The authorization commit is an ancestor of the current governance revision.
The corrective worktree remains clean at the approved baseline above, whose
parent is original pilot handoff `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`.
The original pilot implementation is `d709c5aab0a841a8dfb193bd26b306d9b4198392`;
the original independent closure is
`515dde66f37ca67c44a39f02e13f2e59b2f10d1d`. Its disposition remains
**NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not a scientific efficacy
result, and its pilot budget remains exhausted.

**OBSERVED:** the corrective worktree has no corrective diff, the specified
`run-r4.3-corrective-checks.ps1` supervisor does not exist there, the
one-shot marker
`%LOCALAPPDATA%\TPCN\luna64-r43-corrective-implementation-20261010.json`
is absent, and no corrective evidence directory exists in the governance
worktree. The prior execution handoff reports that no tests or workload ran.
This review did not execute a test or supervisor. Git and marker state
establish no published/retained corrective execution artifacts; they cannot
independently prove the absence of an unrecorded process invocation outside
the repository. No claim beyond those records and observations is made.

The reviewed protocol is the frozen
`experiments/luna64/luna64-track-b-protocol-r4.json`. Its R4.3 timing, reward,
eligibility, event identity, and learning rules are outside this amendment.
The Luna-64 contract remains experimental and isolated from Luna-63C.

## 2. Windows metric reconciliation

The available host is **Microsoft Windows 10 Pro, 64-bit, version
10.0.19045**. Microsoft documents nested jobs from Windows 8 onward and
`PROC_THREAD_ATTRIBUTE_JOB_LIST` from Windows 10 onward. Those OS capabilities
exist here. No Job Object was created and no privilege, outer-job
compatibility, completion-port behavior, or resource-limit enforcement was
exercised in this governance task. Any runtime setup or query failure must
stop before a focused test starts.

These quantities are distinct:

| Quantity | Meaning and evidence | Enforceable by the proposed job memory limit? |
|---|---|---|
| Job-wide committed memory | Sum of committed memory for processes assigned to a job. `JOB_OBJECT_LIMIT_JOB_MEMORY` / `JobMemoryLimit` sets this job-wide ceiling. | **Yes**, at the configured job boundary. A commit operation that would exceed it fails. |
| Per-process committed memory | One process's committed virtual memory. `JOB_OBJECT_LIMIT_PROCESS_MEMORY` constrains it independently. | Not the selected aggregate limit. |
| Current working set | Resident pages currently in a process's working set (`WorkingSetSize`). | **No.** |
| Peak working set | A process's lifetime peak resident working set (`PeakWorkingSetSize`). | **No.** |
| Sum of concurrent working sets | The instantaneous sum across all processes at one observation time. | **No.** Per-process samples can produce observations only for processes actually observed. |
| Peak aggregate working set over time | Maximum concurrent working-set sum across the complete process tree over the run. | **No.** No documented Job Object aggregate peak-working-set counter establishes it; best-effort process notifications cannot prove complete per-process capture. |

`PeakJobMemoryUsed` is Job Object memory accounting associated with job memory
limits; it must be recorded as committed-memory accounting, never relabeled
as a working-set value. Neither the committed-memory ceiling nor its peak
proves a bound on all resident-memory categories, kernel memory, or total
machine RAM use. `GetProcessMemoryInfo` current/peak working-set readings and
sampled aggregate sums remain **observations**, with incomplete coverage
explicitly reported.

### Candidate comparison

- **A — Job-wide committed-memory ceiling:** selected for proposal. The
  documented Job Object limit is a native hard ceiling over committed memory
  charged to processes in the job. It changes the metric and does not prove
  the original aggregate-working-set limit.
- **B — Per-process working-set limits:** rejected as the primary control.
  `JOB_OBJECT_LIMIT_WORKINGSET` supplies the same minimum/maximum working-set
  sizes separately for each process. It is not an aggregate counter or
  aggregate ceiling. Multiplying a per-process maximum by an assumed process
  count would require an independently hard active-process bound and still
  would not establish a reliable aggregate peak across every relevant memory
  category. It is less direct and more complex than Candidate A.
- **C — Container or VM isolation:** not selected. No separately authorized
  container/VM execution boundary is established. Such a limit would require
  its own verified accounting definition and cannot be assumed equivalent
  to Windows aggregate working set.
- **D — Original aggregate-working-set requirement:** remains
  **NOT ENFORCEABLE/UNVERIFIED** by the documented Job Object aggregate
  accounting path. Retaining it unchanged would leave the corrective run
  blocked.

## 3. Proposed minimal resource amendment

Subject to separate owner approval, replace only the parent gate's memory
hard-limit definition:

> **Enforced memory limit:** 512 MiB (`536870912` bytes) of job-wide committed
> memory, enforced by Windows Job Objects with
> `JOB_OBJECT_LIMIT_JOB_MEMORY` and
> `JOBOBJECT_EXTENDED_LIMIT_INFORMATION.JobMemoryLimit = 536870912`.

The ceiling applies to the dedicated supervised job: its actual test
supervisor process and all authorized test descendants must be associated
with that job before executing authorized test code. A minimal bootstrap
that creates/configures the job and launches the supervisor is not an
authorized test process; its role, resource observation, and exclusion from
the job boundary must be explicit in implementation evidence. No test,
benchmark, or scientific code may run in that bootstrap. If the owner or
reviewer requires the bootstrap's memory to be inside the hard ceiling and
that cannot be demonstrated, this amendment is blocked rather than silently
claiming full-process coverage.

Before any authorized test process executes, the implementation must:

1. Create a fresh private Job Object and install the 536870912-byte
   job-commit ceiling, `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, and the existing
   one-core affinity constraint. Do not set either breakaway flag.
2. Install and verify the job's completion-port/resource notification
   configuration before starting the supervisor or any test child. Configure
   a guaranteed `JobObjectNotificationLimitInformation` job-memory threshold
   one system page below the hard ceiling. Reaching that warning threshold
   must be explicitly logged and must terminate the supervised run; this is
   a fail-stop warning threshold, not a replacement hard-limit value.
3. Create the actual supervisor suspended and associate it at process
   creation with `PROC_THREAD_ATTRIBUTE_JOB_LIST` (supported on this host's
   Windows version), then verify job membership and effective affinity
   before resuming it. The supervisor must apply the same suspended,
   assigned, verified-before-resume boundary to each authorized test child.
   Any unsupported attribute, assignment failure, invalid effective
   affinity, preexisting incompatible job limit, or unverified membership
   fails closed before tests.
4. Keep the Job Object handle non-inheritable and do not duplicate it.
   On unrecoverable monitor/supervisor failure, close the last job handle or
   call `TerminateJobObject`; verify all active descendants terminate. Do
   not continue after missing measurements, lost process containment, or
   notification-monitor failure.
5. Record Job Object commit-limit configuration, actual committed-memory
   high-water values, notification/limit outcomes, process identities,
   per-observable-process current and peak working-set samples, observed
   aggregate working-set samples, sampling gaps, and artifact byte totals.
   Label working-set figures as observations only. A missing process or
   sample is `incomplete`, never zero.

The documented `JOB_OBJECT_MSG_JOB_MEMORY_LIMIT` is useful evidence, but
ordinary completion-port messages are not guaranteed to arrive. Do not infer
that no commit-limit attempt occurred from a missing such message. The
guaranteed notification-limit event is an asynchronous warning signal, not a
barrier: the monitor may receive it after another commit attempt. The hard
job ceiling, not the notification, prevents job commits above 536870912
bytes. The monitor must stop the run when the warning is received, and the
controlled qualification below must separately establish the hard
commit-ceiling behavior and explicit reporting of an allocation attempt
that cannot commit. A missing/ambiguous violation signal or failed
qualification blocks implementation execution.

The proposed notification threshold wording means
`536870912 - GetSystemInfo.dwPageSize` bytes. On the current host,
`SystemPageSize` is 4096 bytes, yielding 536866816 bytes. This is not a
511-MiB-minus-page threshold; no such threshold is specified by the parent
gate or owner request. A successor package must state the exact threshold
and page-size source, and obtain review of its exact bytes.

`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` guarantees job-process termination when
the last job handle closes. Default child association supplies descendant
containment when breakaway is not enabled. Job Object docs note that
processes created through WMI `Win32_Process.Create` are not automatically
associated; such launch mechanisms are forbidden to the supervisor and
children. Windows 10 supports nesting, but an enclosing host job can impose
more restrictive effective memory/affinity limits or prevent assignment.
The runtime preflight must fail closed on incompatible conditions; API
availability alone is not proof of successful host-context enforcement.

This is an explicit change of measurement policy. It does **not** satisfy,
reconstruct, or retrospectively validate the parent's aggregate
working-set requirement.

## 4. Unchanged parent budget and forbidden work

All non-memory terms and the unconsumed original allowance remain exactly as
published in the parent gate:

| Term | Unchanged parent limit |
|---|---|
| Corrective supervisor invocations | One; the one-shot marker remains absent and unused |
| Focused child tests | Exactly three, once each, in the existing order and under the exact `Mode All` invocation |
| Synthetic lifecycle/trace records | 512 combined maximum |
| CPU allocation | One logical CPU |
| CPU time | 120 seconds aggregate |
| Wall time | 180 seconds aggregate |
| Artifacts | 5 MiB aggregate |
| Scientific workload / pilot rerun | Prohibited |

This amendment does not permit extra focused tests, retries, a benchmark,
training/evaluation, another pilot, production/core changes, ACP adoption,
architecture promotion, or Luna-63C work. The original pilot allowance
remains exhausted. The three focused tests remain unrun and the original
one-shot allowance remains unconsumed.

## 5. Required supervisor qualification and separate proposed boundary

The existing three-child `Mode All` allowance cannot also be treated as a
supervisor self-test budget: its command allowlist is fixed, and adding probe
children to it would change that gate. Therefore the following is a **new,
separate proposed authorization boundary**, not granted by this amendment's
publication or by the earlier owner authorization:

- **Purpose:** qualify only the Windows supervisor/resource-control
  mechanism before corrective implementation begins.
- **Proposed sole invocation:**
  `powershell.exe -NoProfile -File experiments/luna64/test-r4.3-corrective-supervisor.ps1 -Mode Qualification`
- **Proposed one-shot marker:**
  `%LOCALAPPDATA%\TPCN\luna64-r43-supervisor-a1-qualification-20261010.json`.
  It is a distinct marker and may not reset or consume the original
  corrective-test marker.
- **Proposed files:** the supervisor
  `experiments/luna64/run-r4.3-corrective-checks.ps1`, a dedicated
  supervisor-qualification test script at the command path above, and
  bounded qualification evidence under
  `workflow/evidence/luna64-r4.3-supervisor-a1-qualification-20261010/`.
  No files are created by this governance task.
- **Proposed limits:** one invocation; one logical CPU; 120 CPU seconds;
  180 wall seconds; 512 MiB job-wide committed memory; 5 MiB artifacts; at
  most 64 qualification process/trace records and no more than four active
  probe processes, counting the supervisor. Memory probes may request one
  page beyond the cap but may not commit beyond the enforced job ceiling.
- **Prohibited:** any of the three focused correctness tests, pilot runner,
  benchmark generator, training/evaluation, scientific data, network, GPU,
  production/core or Luna-63C code.
- **Approval rule:** this qualification invocation requires explicit owner
  approval of this separate boundary. It is not an additional test retry and
  does not replenish the parent budget. If not separately approved, no
  qualification invocation and no corrective implementation may start.

Qualification must provide evidence for:

1. Hard and notification limits are installed and query back with the exact
   expected values before any supervisor/test code resumes.
2. Suspended creation-time job association, membership verification, and
   effective one-core affinity precede execution.
3. Normal child and grandchild processes remain in the job; breakaway
   attempts are rejected or remain contained; unsupported WMI-style process
   creation is not used.
4. A controlled over-limit commit attempt fails at the Job Object limit and
   is explicitly recorded; the separate guaranteed notification threshold
   is received and handled. No run may continue after the warning or a
   monitoring failure.
5. A normal below-limit run completes with reconciled job commit and
   per-process working-set telemetry, explicitly distinguishing the
   metrics.
6. Supervisor crash/monitor failure closes or terminates the job and leaves
   no live descendant; affinity, wall-time, CPU-time, one-shot-marker, and
   artifact caps are all verified without changing their original limits.
7. Nested-job or current-token restrictions cause an explicit fail-closed
   result rather than fallback execution.

These supervisor qualification checks are **not run** during amendment
preparation. Static review, API documentation, or a passing later
qualification must not be described as execution of the three focused
reward-lifecycle tests.

## 6. Independent prereview assignment

The independent reviewer must not be the author of this amendment and must
review the exact draft bytes. The reviewer must verify:

- Parent gate hash, prereview, owner authorization and corrective baseline.
- Original pilot evidence preservation and the unchanged
  **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT** verdict.
- The blocker: Job Objects expose no documented aggregate peak-working-set
  hard limit, and process-level samples/notifications cannot prove complete
  aggregate working-set coverage.
- The distinct meanings of job commit, process commit, current/peak working
  set, sampled simultaneous sum and peak aggregate working set.
- Whether the proposed 536870912-byte job commit limit is a native hard
  limit on Windows 10 and whether the notification channel, assignment,
  containment and fail-closed claims are appropriately bounded.
- The suspended/creation-time assignment, nesting, privilege/context gates,
  breakaway assumptions, bootstrap scope and no-unmonitored-continuation
  rule.
- All unchanged budget terms, proposed separate qualification boundary,
  unconsumed original marker/allowance, and no protocol or scientific change.
- That a valid alternative resource ceiling is not proof that the original
  aggregate-working-set requirement was met.
- No implementation, focused test, scientific workload, or Luna-63C
  contamination occurred.

Required verdict:

- **PASS — AMENDMENT READY FOR OWNER AUTHORIZATION**, or
- **BLOCKED — RESOURCE SUPERVISION UNRESOLVED**.

PASS is only independent prereview. It is not owner approval and does not
authorize supervisor qualification, corrective implementation, focused
tests, or scientific execution.

## 7. Owner and execution status

- **Amendment owner approval:** Not granted; this prereview is blocked.
- **Separate supervisor-qualification approval:** Not granted; no
  qualification invocation is authorized.
- **Corrective implementation:** Blocked. The original owner authorization
  does not approve the changed memory policy or resolve the bootstrap
  resource boundary.
- **Parent focused-test allowance:** One invocation / three exact tests;
  unconsumed and unchanged.
- **Scientific rerun authorization:** None. The original pilot budget is
  exhausted.
- **Architecture/ACP status:** No architecture change; no ACP proposed.
- **Luna-63C:** Isolated and untouched.

## 8. Microsoft documentation consulted

- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [JOBOBJECT_BASIC_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information)
- [JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information)
- [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
- [Nested Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs)
- [UpdateProcThreadAttribute (`PROC_THREAD_ATTRIBUTE_JOB_LIST`)](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)
- [JOBOBJECT_ASSOCIATE_COMPLETION_PORT](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port)
- [JOBOBJECT_NOTIFICATION_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_notification_limit_information)
- [PROCESS_MEMORY_COUNTERS](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-process_memory_counters)
- [SetInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-setinformationjobobject)
- [JOBOBJECT_BASIC_ACCOUNTING_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information)
- [JOBOBJECT_CPU_RATE_CONTROL_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_cpu_rate_control_information)

## 9. Independent prereview outcome

**Reviewed draft SHA-256:**
`5B381B568AB0A9C633E6A5EB5DB86ABD0F66487D933719A4E99C92F6BF20D1DD`.
**Verdict:** **BLOCKED — RESOURCE SUPERVISION UNRESOLVED**.

The separate read-only Luna-0 reviewer confirmed that the parent gate,
authorization, corrective baseline, marker state, and absence of corrective
implementation/evidence reconcile. The reviewer confirmed the proposed
536870912-byte `JOB_OBJECT_LIMIT_JOB_MEMORY` ceiling is a valid, enforceable
job-wide committed-memory alternative, but does **not** satisfy the original
aggregate-working-set requirement.

The substantive blocker is bootstrap coverage: the process creating the job
is outside the job and has no enforced memory bound. The complete invocation
resource boundary is therefore unresolved. A successor package must either
include the bootstrap under an enforceable resource boundary or specify a
separately bounded and explicitly owner-authorized launcher exception.
Telemetry alone is not enforcement.

The reviewer also required the asynchronous notification limitation and
threshold to be made explicit. The reviewed draft said “one system page
below” the 512 MiB ceiling, whose literal formula is
`536870912 - pageSize`; with this host's 4096-byte page size that is
`536866816` bytes. The review response additionally referred to a
`511 MiB - pageSize` target (`535818240` bytes), which appears in neither
the owner request nor the reviewed draft. That discrepancy is preserved
here rather than silently adopting a new threshold. Any successor package
must state and independently review its chosen warning threshold.

The reviewer found the other budget terms, proposed separate qualification
boundary, original pilot disposition, no-protocol-change boundary, and
Luna-63C isolation consistent with the governance record. No tests or
workloads were run by the reviewer. The reviewer response is preserved in
the
[independent prereview record](luna-0-independent-review-luna64-r4.3-corrective-supervisor-amendment-a1-20261010.md).

This is publication of a blocked proposal and its findings, not approval of
the amended resource policy. The previous owner authorization is
insufficient for this change. Supervisor qualification, corrective
implementation, focused tests, and scientific rerun remain unapproved; the
original one-shot marker and focused-test allowance remain unconsumed.
