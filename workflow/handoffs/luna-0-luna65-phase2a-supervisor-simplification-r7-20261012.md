# Luna-0 Handoff — Luna-65 Phase 2A Supervisor Simplification R7

```yaml
tpcn_handoff:
  agent: Luna-0
  task_id: "L65-PHASE2A-SUPERVISOR-SIMPLIFICATION-R7"
  component: "Luna-65 Phase 2A supervisor governance design"
  status: "pass-design-ready-for-owner-decision"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "1d6325f3ca738b32a6ee9e1a5613d2faa9458770"
  classification: ["governance-only", "independent-review"]
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_SIMPLIFICATION_R7.md (new)"
    - "workflow/handoffs/luna-0-luna65-phase2a-supervisor-simplification-r7-20261012.md (new)"
    - "workflow/docs/luna/LUNA_WORKFLOW.md (R7 entry only)"
  tests_run: []
  tests_not_run:
    - "No static validation, supervisor execution, qualification, sizing, fixtures, benchmarks or scientific experiments; none authorized."
  preserves:
    - "Scaffold scripts/luna65_phase2a_supervisor.py SHA-256 67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1 (untracked, unpublished, unmodified)."
    - "R6 contract 5747D1DD5A76C4D4C3BF5EC6FEB220AF268D05CE5FC0B6E24F84D443A487C152 and R6 handoff 8D681CAFC5BE6F6E73F591934F8A73405F595A6DE745F0521C349E9FD625C3D2; original R6 BLOCKED verdict."
    - "Unpublished R1/R2 records and the pre-existing uncommitted Authorization I workflow entry."
  r7_contract_sha256: "7096BB6782CFE1092B5B4F4DF1803788664D69DCFADF4F885D78F00066C073E2"
  integrated_disposition: "PASS — SIMPLIFIED SUPERVISOR DESIGN READY FOR OWNER DECISION"
```

## Outcome

Three candidates were compared. **B-min** (watchdog is launcher, holds only a
`PROCESS_TERMINATE | SYNCHRONIZE` handle to the controller and no job handle;
controller owns the sole unnamed job handle and all evidence; no ETW, no
bootstrap or observer job, no job-handle duplication) is the **recommended
candidate, not an owner selection**. Candidate A is acceptable only if the owner
accepts that a hung controller is uncovered. Candidate C (R6) is not
recommended: its only indispensable addition is system-wide process-creation
detection, which is additive and separately owner-gated, and its job-handle
duplication weakens kill-on-close.

## Owner-decision provenance

O1–O8 (120 s CPU, 120 s wall, 115 s early termination, 15 s observation that is
not execution permission, bounded cessation intervals, 268,435,456 B memory,
1,048,576 B artifacts, zero retries) are recorded as directly supplied
conversation evidence. The R6-referenced attachment was not accessible; its
bytes were not verified and its hash is not reproduced.

## Dispositions

- **Q03:** split into A (breakaway/descendants: OS-enforced, no ETW needed; pass
  criterion is no outside-job child, not `CreateProcess` failure), B
  (cooperative outside-child recovery: runtime qualification), C1 (new
  outside-job process detection: owner decision) and C2 (injection into an
  existing process: outside any process-start observer; owner decision). Not
  waived.
- **Controller failure:** crash is OS-enforced (kill-on-close) once the sole-handle
  condition holds; hang is converted to crash by the watchdog (design-controlled,
  runtime qualification). Watchdog hang is undetectable (UN/OD). Controller hang
  plus lost watchdog is unresolved. The `T0+135 s` watchdog action is
  unconditional.
- **Memory:** equivalence or conservative dominance of Job Object job-memory
  over aggregate `PrivateUsage` is not established. Owner decision D-R7-2; the
  256 MiB ceiling is unchanged.
- **Evidence:** single controller-owned pipe capture with bounded buffers,
  drain-and-discard on writer stall, contiguous ledger, hard 1 MiB accounting.
  Fit of the 8,196-record ledger is **not** established (786,432 / 8,196 ≈ 95.95
  B per record); a separately authorized synthetic sizing is a prerequisite for
  implementation authorization.

## Independent review

Four read-only lanes reviewed exact bytes. Round 1 and round 2 returned BLOCKED
(findings: B-min presented as selected; startup acknowledgment; watchdog death
racing admission; watchdog hang misclassified; 135 s cutoff versus evidence;
Q03-C injection and breakaway-oracle overstatement; end-of-job action read-back;
reader backpressure; the committed-status exemption from the cutoff). Round 3
on SHA-256 `7096BB67…073E2`: **A PASS, B PASS, C PASS, D PASS.**

## Remaining owner decisions

D-R7-1 through D-R7-8 as listed in the R7 contract section 10.3. Frozen token,
ACL and identity profiles are not invented.

## Authorization state

**Supervisor implementation: NOT AUTHORIZED.**
**Supervisor qualification: NOT AUTHORIZED.**
**Phase 2A/2B fixtures: NOT AUTHORIZED.**
**Full Spiral execution: BLOCKED.**
**Luna-64 corrective execution: BLOCKED.**
**Luna-63C: FROZEN.**

Exact authorization needed next: an owner decision recording D-R7-1 through
D-R7-8, followed by a separate implementation authorization naming the single
file `scripts/luna65_phase2a_supervisor.py`, the reviewed contract SHA-256 and
the frozen profiles. A separate authorization is required for synthetic
evidence sizing and for qualification.
