# Luna-0 Corrective Handoff — Luna-29 Execution Baseline

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Clarify Luna-29 authorization and execution lineage"
  task_id: "luna-0-corrective-luna29-execution-baseline-20261004"
  component: "Luna-29 authorization provenance and pre-edit gate"
  status: "complete"
  contract_version: "1.2"
  branch: "main"
  base_revision: "aad4b0db09773ebca9314d188c3b24297ad17c44"
  result_revision: "this handoff's governance correction publication commit"
  dependencies:
    - "Published Luna-29 authorization package"
    - "Accepted ACP-0007"
    - "Luna-28 independent review closure"
  owner: "Luna-0 Architecture Guardian"
  classification: ["GOVERNANCE CORRECTION", "REVISION-PROVENANCE CLARIFICATION"]
  hypothesis: "The Luna-29 stop resulted from conflating the review decision revision with the first publication of its executable authorization package."
  counter_hypothesis: "A substantive post-review architecture change would invalidate the authorization and require a new Luna-0 decision."
  interfaces_relied_on:
    - "Luna-29 authorization contract"
    - "Luna-0 authorization and compatibility-decision handoffs"
    - "Luna-0 independent-review handoff for Luna-28"
  label_information_boundary: ["Not applicable; governance-only work."]
  timing_assumptions: ["No runtime or event timing behavior changed."]
  reset_boundaries: ["No runtime reset behavior changed."]
  resource_bounds: ["No runtime resource behavior changed."]
  authorized_scope:
    - "Clarify authorization source and publication revisions."
    - "Repair the Luna-29 clean-main ancestry and governance-only descendant gate."
    - "Publish governance handoffs, workflow status, and changelog clarification."
  unauthorized_scope:
    - "Luna-29 implementation or tests."
    - "Changes to ACP-0007, Architecture Contract 1.2, A01-A15, or Luna-29 substantive scope."
    - "Authorization of a successor."
  controls: ["Compare c654ffe..aad4b0d changed paths and commit contents."]
  measurements:
    - "The revision delta contains exactly five governance/authorization files."
    - "No production, test, ACP-0007, architecture-contract, A01-A15, Luna-28 implementation, or TPCV semantic changes occur in that delta."
  information_boundary_check: ["No neural input, label, or runtime information was involved."]
  hardware_mapping: ["Not applicable; no hardware behavior changed."]
  architecture_invariants_touched: []
  preserves:
    - "ACP-0007 and Architecture Contract 1.2 unchanged."
    - "Luna-29 scope unchanged; no E2 pruning enabled."
    - "Luna-29 remains authorized but not executed."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-29.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md"
    - "workflow/handoffs/luna-0-post-luna28-luna12b-compatibility-decision-20261004.md"
    - "workflow/handoffs/luna-0-corrective-luna29-execution-baseline-20261004.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing: ["Revision-scope audit; git diff --check."]
  tests_failed: []
  tests_not_run: ["Implementation tests; this governance-only correction changes no executable code."]
  assumptions:
    - "The F9h... token is a supplied opaque identifier, not a Git object or repository-verifiable revision."
    - "c654ffe... is the verified repository revision against which Luna-0 made the compatibility decision."
    - "aad4b0d... is the first repository revision containing the Luna-29 authorization package."
  unresolved: []
  recommended_next_agent: ["Luna-29, then Luna-0 independent review."]
```

## Outcome and revision provenance

Starting revision: `aad4b0db09773ebca9314d188c3b24297ad17c44`
(`docs: authorize Luna-29 CPU replay compatibility`).

The earlier Luna-29 result is a **VALID GOVERNANCE STOP / NO FILES CHANGED**;
it was not an implementation failure. The authorization source token
`F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` is **NON-GIT / IGNORED FOR
REPOSITORY PROVENANCE**. The verified decision revision is
`c654ffe9c8d4a6d179781696d9ba5cd239e12795`; the authorization package
publication revision and execution-lineage floor are
`aad4b0db09773ebca9314d188c3b24297ad17c44`.

The `c654ffe..aad4b0d` delta is **GOVERNANCE ONLY**. It adds the Luna-29 agent
contract, authorization handoff, compatibility-decision handoff, workflow
entry, and changelog entry. It contains no production or test changes and no
ACP-0007, Architecture Contract, A01-A15, Luna-28 implementation, or TPCV
semantic changes.

## Decision and validation

- Architecture change: **NO**.
- Luna-29 substantive contract change: **NO**.
- Luna-29 status: **AUTHORIZED / NOT EXECUTED**.
- Required sequence: **Luna-0 corrective governance -> Luna-29 -> Luna-0
  independent review**.
- Validation: `git diff --check`, complete diff inspection, exact changed-path
  audit, and synchronized clean `main` verification after publication.
- Implementation tests: **NOT RUN / NOT APPLICABLE**; no executable code or
  tests are changed.

Luna-29 may execute only from clean synchronized `main` descending from the
execution-lineage floor. Any later descendants before execution must be
governance-only clarification/pinning for this authorization. A production,
test, ACP, contract, or architecture-semantics change requires stopping and
returning to Luna-0. This correction does not execute Luna-29 or authorize a
successor.
