---
tpcn_handoff:
  agent: "Lead Luna-47 Orchestrator"
  luna_identifier: "Luna-47"
  descriptive_name: "Final corrective pass and Luna-48 readiness gate"
  task_id: "luna-47-final-corrective-pass-20261007"
  component: "Luna-47 evidence integrity and workflow state"
  status: "complete - FINAL CORRECTIVE PASS INCOMPLETE; no successor authorized"
  contract_version: "1.2"
  base_revision: "ce411ec049501b7ac6d05702ed242d4829ad24d7"
  owner: "Project owner"
  classification:
    - "corrective validation"
    - "FOLLOW-UP REQUIRED"
    - "no architecture change"
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna47f/diagnostic.py"
    - "artifacts/luna47f/diagnostic.json"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-47-final-corrective-pass-20261007.md"
  tests_passing:
    - "Luna-47 focused suite: 307 passed"
    - "Luna-47F retained replay: 5 passed"
    - "Historical/core compatibility audit: 377 passed"
  tests_failed:
    - "Full repository suite: 1 failed, 7 errors, 1632 passed, 1 skipped"
    - "Luna-44 canonical fixture materialization remains incompatible with the pinned source on Windows"
  unresolved:
    - "Retention, gain, qualification, compression, topology-candidate and analog-variation mechanisms were not composed or tested for task efficacy."
    - "The full repository regression gate is not green."
    - "Luna-47F retained replay previously rejected the integrated main branch because it compared working-tree ownership against the historical authorization commit; the guard is now limited to staged and unstaged changes."
    - "Existing Windows versus frozen-Linux fixture materialization failures remain outside this corrective scope."
  disposition: "FINAL CORRECTIVE PASS INCOMPLETE"
  recommended_next_agent:
    - "Luna-0 Architecture Guardian for an independent review and a separately authorized bounded follow-up decision."
---

# Luna-47 final corrective pass — 2026-10-07

## Result

The integrated `origin/main` baseline was `ce411ec049501b7ac6d05702ed242d4829ad24d7`.
The retained Luna-47F replay guard was corrected so that it detects only
staged or unstaged working-tree mutations, rather than treating every
published commit after the historical lane authorization as a non-owned
change. The retained diagnostic artifact was regenerated from that corrected
source and its code/protocol hashes were checked directly.

This closes the integrated-replay harness defect but does not close the
scientific or repository-wide Luna-47 gates.

## Validation

- Luna-47 focused tests: **307 passed**.
- Luna-47F retained replay: **5 passed**.
- Historical/core compatibility audit: **377 passed**.
- Full suite: **1 failed, 7 errors, 1632 passed, 1 skipped**. The failure
  and errors are the existing Luna-44 canonical-fixture source/materialization
  checks (`authorized generator source differs from the pinned baseline`) on
  this Windows checkout.
- The independent Luna-47 review remains authoritative: the lane results are
  isolated, several are only partially supported or proxy/model evidence, and
  no integrated efficacy, hardware equivalence, or successor experiment was
  authorized.

## Disposition

**FINAL CORRECTIVE PASS INCOMPLETE.**

This pass does **not** authorize Luna-48. The minimum next action is for
Luna-0 to independently review this correction and decide whether to authorize
a narrowly bounded follow-up that addresses the unresolved Windows materialization
gate and one explicitly defined causal mechanism question. No composition,
production promotion, ACP action, or Luna-48 contract is created here.
