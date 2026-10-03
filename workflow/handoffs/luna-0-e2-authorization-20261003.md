# Luna-0 ACP-0004 E2/M Authorization

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "ACP-0004 E2 multi-excursion runtime authorization"
  task_id: "luna-0-e2-authorization-20261003"
  component: "ACP-0004 E2/M governance dispatch"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "40b453784b015552738f202c9a765a2f0587f533"
  result_revision: "uncommitted authorization documentation"
  dependencies:
    - "ACP-0004 E1 independently closed"
    - "ACP-0005 TPCN-IR-2 independently closed"
    - "Luna-0 blocked E2/M dispatch review"
  owner: "Luna-0 Architecture Guardian / project owner"
  classification: ["ARCHITECTURE-PROMOTION", "VERIFICATION"]
  hypothesis: "The explicit ACP-0004 and ACP-0005 clarifications provide one bounded implementation interpretation for E2/M."
  counter_hypothesis: "Episode identity, lineage, provenance, reset or IR-2 capability remains ambiguous or contradicts closed architecture."
  interfaces_relied_on:
    - "ACP-0004 E1 and E2/M"
    - "ACP-0005 TPCN-IR-2 revision 1"
    - "neuron_from_ir2 E1-only adapter"
    - "ACP-0002 N2 Model-B"
    - "A01-A15"
  label_information_boundary:
    - "No labels, evaluation, learning, reward or global orchestration state enters E2."
  timing_assumptions:
    - "Local analytic decay and finite positive delays."
    - "Destination-local external-before-internal ordering."
    - "No global neural timestep."
  reset_boundaries:
    - "M reset clears character-local state and valid pending work, emits nothing, and retains identity high-water counters."
  resource_bounds:
    - "Bounded x, modes/phases, one valid internal event, provenance, identities and event budget."
  authorized_scope:
    - "Create and authorize Luna-21 for E2 runtime and E2-capable IR-2 reconstruction."
    - "Predeclare bounded E2 fixtures and independent completion review."
  unauthorized_scope:
    - "Executing Luna-21 in this task."
    - "H2, N3, learning, reward redesign, backends, hardware, calibration, TPCN-IR-3 and A01-A15 changes."
  controls:
    - "Closed E1 runtime and E1-only IR-2 adapter remain regression controls."
    - "IR-2 schema revision remains 1 with shared validation."
  measurements:
    - "No runtime measurements; governance-only authorization."
  information_boundary_check:
    - "All authorized E2 state is local, bounded and causally available."
  hardware_mapping:
    - "Canonical excursions remain logical digital events; no backend is authorized."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A08", "A11", "A15"]
  preserves:
    - "A01-A15"
    - "ACP-0004 E1 closure"
    - "ACP-0005 schema revision 1 and E1 rejection boundary"
    - "ACP-0002 N2 Model-B"
    - "Luna-17 reserved status"
    - "Luna-13F CLOSED and Luna-13G unauthorized"
  architecture_change: false
  proposal: "ACP-0004 E2 clarification and staged implementation authorization"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/docs/architecture_proposals/ACP-0005.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-e2-dispatch-review-20261003.md"
    - "workflow/handoffs/luna-0-e2-authorization-20261003.md"
    - ".github/agents/luna-21.agent.md"
  tests_added: []
  tests_passing:
    - "Starting revision verified as 40b453784b015552738f202c9a765a2f0587f533."
    - "All four prior dispatch blockers reconciled against closed E1 and IR-2 state."
    - "IR-2 source inspection confirmed shared episode counter and E1 M rejection."
  tests_failed: []
  tests_not_run:
    - "E2 runtime, E2 adapter, full CPU, backend and hardware tests: not run by governance task."
  assumptions:
    - "The named E2 adapter paths will be implemented without changing schema revision 1."
  unresolved:
    - "Runtime implementation and independent verification evidence remain outstanding."
  recommended_next_agent:
    - "Luna-21: implement and verify the authorized E2 scope."
    - "Luna-0: independently review Luna-21 completion."
```

## Decision

**PASS — ACP-0004 E2/M IMPLEMENTATION BOUNDARY CLARIFIED; LUNA-21
AUTHORIZED BUT NOT EXECUTED.**

The final residual S episode receives a new shared-counter episode identity,
retains the M lineage, re-owns active provenance with sticky truncation, and
does not exist for direct M-to-N return. Reset and stale-event semantics are
explicit. `neuron_from_ir2` remains E1-only; the named E2 capability is
`neuron_to_ir2_e2` / `neuron_from_ir2_e2`. TPCN-IR-2 remains schema revision
1. No E2 runtime or tests were executed by Luna-0.
