---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-48 provenance correction authorization"
  task_id: "luna-0-authorization-luna48-20261007"
  component: "Governance-only canonical fixture materialization correction"
  status: "complete - AUTHORIZED / NOT EXECUTED"
  contract_version: "1.2"
  branch: "main"
  base_revision: "39bedbce47055a7b180593ea312c6b646510c566"
  result_revision: "governance authorization commit"
  owner: "Project owner"
  classification:
    - "governance-only authorization"
    - "provenance/infrastructure correction"
    - "no scientific successor experiment"
  hypothesis: "The Luna-44 materialization gate can be corrected by separating canonical Git-blob identity from Windows checkout encoding without changing fixture identity."
  counter_hypothesis: "The mismatch reflects a true source or fixture identity defect that cannot be corrected without changing the historical baseline."
  interfaces_relied_on:
    - "workflow/ARCHITECTURE_CONTRACT.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - ".github/agents/luna-48.agent.md"
    - "scripts/build_luna44_canonical_fixture.py"
    - "scripts/verify_luna44_canonical_fixture.py"
  label_information_boundary:
    - "No labels, evaluation statistics, or neural outputs are involved."
  timing_assumptions:
    - "No neural timing or event semantics are changed."
  reset_boundaries:
    - "Not applicable; fixture materialization only."
  resource_bounds:
    - "Existing fixture size and source-input bounds remain unchanged."
  authorized_scope:
    - "Correct the Luna-44 pinned-source materialization provenance path."
    - "Add or update focused tests for canonical versus checkout bytes."
    - "Re-run exact historical fixture and compatibility gates."
  unauthorized_scope:
    - "No fixture regeneration with changed identity."
    - "No source-pin, parameter, architecture, ACP, or scientific-hypothesis change."
    - "No composition of Luna-47 mechanisms."
    - "No causal experiment and no Luna-49 authorization."
  controls:
    - "Compare Git blob bytes and checkout bytes explicitly."
    - "Preserve committed fixture and semantic SHA-256 values."
    - "Require loud failure for altered source identity."
    - "Run independent materialization twice."
  measurements:
    - "Source Git-blob and checkout SHA-256 values."
    - "Fixture byte and semantic digests."
    - "Independent materialization equality."
  information_boundary_check:
    - "PASS: correction is downstream-only provenance handling."
  hardware_mapping:
    - "Not applicable."
  architecture_invariants_touched:
    - "No A01-A15 invariant changes."
  preserves:
    - "Luna-44 canonical fixture identity."
    - "Luna-46 MIXED evidence and Luna-47 isolated evidence."
    - "No Luna-48 scientific readiness claim."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-48.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-authorization-luna48-20261007.md"
  tests_added: []
  tests_passing:
    - "Luna-47 focused suite: 307 passed."
    - "Historical/core compatibility suite: 347 passed."
    - "Committed Luna-44 provenance verifier: passed."
  tests_failed:
    - "Luna-44 independent materialization: 1 failed and 7 setup errors under Windows CRLF checkout."
  tests_not_run:
    - "Luna-48 correction implementation: not run; governance only."
  assumptions:
    - "The pinned Git blobs remain authoritative."
  unresolved:
    - "Whether the correction can preserve all historical gates across supported environments remains to be demonstrated."
  recommended_next_agent:
    - "Luna-48 execution worker, from this committed governance revision, followed by independent Luna-0 review."
---

# Luna-48 authorization gate — AUTHORIZED / NOT EXECUTED

Independent Luna-0 review of published commit
`39bedbce47055a7b180593ea312c6b646510c566` found that the remaining
Luna-44 failure occurs before fixture generation. The temporary checkout at
the pinned source revision lacks the later repository LF attribute and
materializes Python sources as CRLF under the current Windows Git policy.
The worker hashes those checkout bytes against canonical Git-blob SHA-256
values, producing a loud provenance failure.

The committed source and fixture identities are internally valid in the
current checkout; the failure is therefore authorized as a bounded
materialization/provenance correction, not as permission to change the
historical fixture.

No causal Luna-47 mechanism experiment is authorized by this handoff.
Retention, gain, qualification, output compression, candidate generation and
analog variation remain isolated evidence, and Luna-46 remains MIXED.
After Luna-48 closes the provenance gate, Luna-0 must make a separate
evidence-based decision about any single causal mechanism question.
