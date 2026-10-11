# Luna-0 Independent Prereview — Luna-64 Corrective Supervisor Amendment A1

**Date:** 2026-10-10
**Reviewed draft SHA-256:** `5B381B568AB0A9C633E6A5EB5DB86ABD0F66487D933719A4E99C92F6BF20D1DD`
**Verdict:** **BLOCKED — RESOURCE SUPERVISION UNRESOLVED**
**Reviewer:** Separate read-only Luna-0 Architecture Guardian subagent
**Scope:** Governance and Microsoft API documentation inspection only. No
file edits by reviewer, tests, supervisor invocation, pilot, or workload.

## Identity and execution state

- Parent gate file hash matches
  `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369`;
  published final bytes are in commit
  `439c0c930489ed032dc10950bbd51fe3f153d05a`.
- The owner's parent-gate authorization is published in
  `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`.
- Corrective branch
  `experiment/luna64-r4.3-reward-lifecycle-correction-20261010` is clean at
  `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`.
- The corrective supervisor, dedicated qualification script, corrective
  reward-reference/lifecycle tests, and qualification evidence are absent.
  The original one-shot marker is absent.
- Original pilot implementation and closure remain
  `d709c5aab0a841a8dfb193bd26b306d9b4198392` and
  `515dde66f37ca67c44a39f02e13f2e59b2f10d1d`.

## Technical findings

The reviewer confirmed that `JOB_OBJECT_LIMIT_JOB_MEMORY` with
`JobMemoryLimit = 536870912` is a native hard **job-wide committed-memory**
ceiling: a commit that would exceed the configured limit fails. It is
technically distinct from the original 512 MiB aggregate working-set
requirement and is **not proof** that the original requirement has been met.

The reviewer confirmed the following distinctions:

- Job-wide committed memory is not the same as per-process committed
  memory.
- Current and peak working set (`WorkingSetSize` and
  `PeakWorkingSetSize`) are process-level resident-memory readings.
- A sum of sampled process working sets is an observed simultaneous sum for
  processes captured at that sample; it does not establish peak aggregate
  working set across time.
- `JOB_OBJECT_LIMIT_WORKINGSET` applies the same working-set minimum/maximum
  separately to each process. Process count alone does not turn it into an
  aggregate limit.
- `PeakJobMemoryUsed` is not a working-set measurement.

Windows 10 version 10.0.19045 supports nested jobs and
`PROC_THREAD_ATTRIBUTE_JOB_LIST`. Suspended creation-time job assignment,
membership and affinity verification before resume, no-breakaway settings,
descendant containment and kill-on-last-job-handle-close are viable
mechanisms. Actual outer-job/token compatibility and privilege context were
not exercised and must fail closed if runtime qualification cannot establish
them. Microsoft documents that WMI `Win32_Process.Create` children are not
automatically associated with a job and that ordinary completion-port
messages, including `JOB_OBJECT_MSG_JOB_MEMORY_LIMIT`, are not guaranteed.
`JobObjectNotificationLimitInformation` notifications are guaranteed, but
they are notifications rather than hard limits; the hard commit ceiling is
the actual enforcement.

## Blockers

1. **Bootstrap coverage is unresolved.** The proposed bootstrap that creates
   the Job Object and launches the supervisor is excluded from the job, with
   no enforced memory bound. This does not bound the complete invocation.
   Resolve the boundary by including that process under an enforceable
   resource limit or by defining a separately bounded, explicitly
   owner-authorized launcher exception. Observation alone does not close the
   gap.
2. **Notification is asynchronous.** The threshold signal cannot be claimed
   to guarantee supervisor termination before another allocation reaches
   the hard ceiling. The hard job limit does enforce the cap; the amendment
   must distinguish the asynchronous notification from that enforcement.
3. **Threshold specification needs exact reconciliation.** The reviewed
   draft's wording “one system page below” means
   `536870912 - pageSize`, which is `536866816` bytes for a 4096-byte page.
   The review response referred to a `511 MiB - pageSize` target
   (`535818240` bytes), which is not specified in the owner request or
   reviewed draft. A successor proposal must specify its intended exact
   warning threshold and page-size source; no threshold should be silently
   inferred.

## Scope and disposition

The parent non-memory budget terms remain unchanged in the proposal. The
separate supervisor qualification invocation and marker are explicitly
proposed, not authorized, and would not consume the parent test allowance.
No frozen scientific protocol, pilot, architecture, ACP, production/core, or
Luna-63C change was found in scope.

**BLOCKED — RESOURCE SUPERVISION UNRESOLVED.** The Job Object commit ceiling
is a valid alternative resource metric, but bootstrap coverage and the
notification/threshold specification prevent readiness for owner
authorization. Independent prereview is not owner approval. No supervisor
qualification, corrective implementation, focused test, or scientific
rerun is authorized by this review.
