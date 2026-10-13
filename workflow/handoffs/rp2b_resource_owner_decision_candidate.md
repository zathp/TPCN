# RP-2B resource owner decision — candidate only

**Revision:** Corrective R1 — 2026-10-12  
**Status: DRAFT / NOT AN OWNER DECISION / NOT AUTHORIZATION**

This document offers decision text for explicit owner review after Lane B-R.
It does not revise or supplement any frozen contract, adopt Resource Policy
R2 for Phase 2B, or authorize implementation, preflight, probe, wrapper,
testing, or execution. No option below is approved.

## Verified decision boundary

At baseline `96fb4aec100578db6939136b4ed7985478f18bb8`,
`workflow/docs/luna/LUNA_65_PHASE2A_RP2_R1_OWNER_DECISIONS.md` §2 records
D-RP2-OUTER-1 as accepted for the bounded synthetic diagnostic only. Section
3 preserves the 64 MiB Job Object memory charge, 8-process backstop,
5-second job user-time backstop, 1 MiB logical evidence ceiling, and
one-invocation/zero-retry envelope as unqualified and unexecuted.

`workflow/docs/luna/LUNA_65_PHASE2A_RESOURCE_POLICY_R2.md` §§2–3 accepts
120-second aggregate job user-plus-kernel CPU and elapsed-wall budgets,
268,435,456-byte memory policy, and 1,048,576 retained-artifact bytes for
Phase 2A qualification design only. It expressly does not amend Phase 2B.
The R2 text requires monitored budgets with failure on observed overrun; it
does not promise zero CPU overshoot or cessation exactly at the wall deadline.
Its §5 distinguishes the Job Object `JobMemoryLimit` from the separately
observed aggregate concurrent private-commit metric and requires their
relationship to be demonstrated, not assumed.

Static RP-2 source remains configured to the frozen profile:
`scripts/luna65_phase2a_rp2_compatibility_probe.py:1047–1062,1073–1113`
and `scripts/luna65_phase2a_rp2_outer_wrapper.ps1:22–27,604–640,928–952`.
Static caps and telemetry are not runtime qualification or proof of maximum
evidence fit.

## Owner to select exactly one disposition

### A — Keep and affirm the frozen RP-2 profile

**Candidate decision text:** “For RP-2B, the request for a 256 MiB /
120-second envelope is withdrawn or is not applicable. RP-2B remains bound
only to the existing frozen RP-2 profile: 64 MiB Job Object job-memory
charge; 8-process backstop; 5-second job user-time backstop; 10-second
active interval; at most 5 seconds cleanup; 20-second outer deadline;
zero retries; and 1 MiB logical retained-evidence ceiling. This decision
selects the intended design profile only; it does not claim resource
qualification, worst-case evidence fit, hard real-time cessation, or grant
execution.”

**Required owner confirmation:** specifically accept the metric distinctions
and frozen timing/termination limitations stated above. D-RP2-OUTER-1 is
already a diagnostic-design decision, but does not on its own resolve the
later 256 MiB / 120-second request or authorize RP-2B.

### B — Amend the RP-2B contract to the requested envelope

**Candidate decision text:** “I intend the requested 256 MiB / 120-second /
1 MiB resource envelope to govern RP-2B, subject to a separately reviewed
contract and implementation change. This is not approval of the existing
source as compliant and is not execution authorization.”

**Minimum obligations affected before any future execution decision:**

- **Memory:** specify whether 256 MiB means Job Object committed-memory
  charge, aggregate concurrent private commit, or both; identify exact
  bytes, Windows Job Object limit/readback, monitoring, and evidence for the
  relationship. Do not call either metric working set or system-wide
  resident memory.
- **CPU:** replace/reconcile the frozen 5-second job-user-time backstop with
  an explicitly defined 120-second aggregate job-wide user-plus-kernel CPU
  budget, including monitor source, sampling/gap, threshold trigger, final
  accounting, overshoot treatment, and failure classification. Per-process
  CPU and recording a job counter are not substitutes.
- **Wall and cessation:** replace/reconcile the frozen 10-second active,
  at-most-5-second cleanup, 20-second outer deadlines with the requested
  120-second elapsed-wall policy. Define monotonic clock, early stop,
  escalation, cleanup allowance, final overrun test, and cessation evidence.
  A termination request must not be represented as confirmed exit.
- **Other frozen controls:** decide explicitly whether the 8-process bound,
  zero-retry rule, fail-closed UNKNOWN handling, and containment limits stay
  in force and how they interact with the amended clocks and CPU limit.
- **Evidence:** retain the 1,048,576-byte ceiling only with an exact
  definition of every retained/staged representation and an independently
  supported maximum-size accounting argument, including success and failure
  records, finalization, stdout/stderr/ledger, manifests/reports, and
  simultaneous bytes. Establish that the updated writer stops before quota
  overflow and that mandatory complete evidence fits; do not rely on a
  typical-volume estimate.
- **Controlled evidence and authority:** amend the RP-2B contract and owner
  record, reconcile source and traceability, obtain independent static
  review, and produce the exact required non-runtime/runtime qualification
  evidence only under separate authorization. Any later execution requires
  its own exact owner grant; this decision text grants none.

### C — Hold RP-2B blocked

**Candidate decision text:** “No resource profile is selected for the
requested RP-2B work at this time. Preserve the existing frozen contract and
source without representing them as compliant with the new request. No
implementation, preflight, probe, wrapper, test, or execution is authorized.
Revisit only after an explicit owner decision and satisfactory independent
readiness review.”

## No selection entered

Owner selection: **NONE**  
Owner / date / signature or authoritative instruction: **NOT PROVIDED HERE**  
Contract amendment identifier (if B): **NOT ISSUED**  
Separate RP-2B execution authorization: **NOT GRANTED**

**Lane B-R recommendation:** record C as the present blocked review
disposition, not as the owner's final policy choice. Do not record A or B
as approved without the owner's explicit decision. Preserve the distinction
between an owner policy choice and later proof that the source and evidence
meet that policy.
