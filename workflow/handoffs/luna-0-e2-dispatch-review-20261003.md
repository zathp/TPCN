# Luna-0 ACP-0004 E2/M Dispatch Review

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "ACP-0004 E2 multi-excursion return dispatch review"
  task_id: "luna-0-e2-dispatch-review-20261003"
  component: "ACP-0004 E2/M governance dispatch"
  status: "blocked"
  contract_version: "1.1"
  branch: "main"
  base_revision: "8136c0e298a8fc8a72722eca349fd047b01f9aa0"
  result_revision: "uncommitted clarification gate"
  dependencies:
    - "ACP-0004 E1 independently closed"
    - "ACP-0005 TPCN-IR-2 independently closed"
  owner: "Luna-0 Architecture Guardian / project owner"
  classification: ["ARCHITECTURE-PROMOTION", "VERIFICATION"]
  hypothesis: "Accepted ACP-0004 and ACP-0005 fully determine a bounded E2/M implementation boundary."
  counter_hypothesis: "Final residual identity, reset behavior, provenance ownership, or E2 reconstruction remains open to implementation-specific interpretation."
  interfaces_relied_on:
    - "ACP-0004 E1 and E2/M contract"
    - "ACP-0005 TPCN-IR-2 schema"
    - "ACP-0002 N2 Model-B transfer"
    - "A01-A15"
  label_information_boundary:
    - "No labels, evaluation state, learning state or global orchestration state enters the canonical neuron."
  timing_assumptions:
    - "Local analytic decay and finite positive internal delays."
    - "Destination-local external-before-internal ordering."
    - "No global neural timestep."
  reset_boundaries:
    - "E2 reset semantics during M are unresolved and block dispatch."
  resource_bounds:
    - "Bounded x, mode/phase, one valid internal event, provenance capacity, identities and event budget."
  authorized_scope:
    - "Review E2/M implementation readiness."
    - "Record the exact clarification gate in ACP-0004 and workflow records."
  unauthorized_scope:
    - "Luna-21 creation or authorization."
    - "E2 runtime, IR-2 schema revision, learning, H2, N3, backends, hardware and calibration."
  controls:
    - "Closed E1 behavior remains the regression baseline."
    - "Closed IR-2 schema remains the transfer baseline."
  measurements:
    - "Repository revision and documentation consistency only; no runtime measurements."
  information_boundary_check:
    - "The unresolved items concern identity/reset/schema interfaces, not label or global-state access."
  hardware_mapping:
    - "No backend or hardware work authorized."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A08", "A11", "A15"]
  preserves:
    - "ACP-0004 E1 closure"
    - "ACP-0005 IR-2 closure"
    - "A01-A15"
    - "ACP-0002 N2 Model-B semantics"
    - "Luna-17 reserved status"
    - "Luna-13F CLOSED and Luna-13G unauthorized"
  architecture_change: false
  proposal: "ACP-0004 clarification required before E2 dispatch"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-e2-dispatch-review-20261003.md"
  tests_added: []
  tests_passing:
    - "Starting revision verified as 8136c0e298a8fc8a72722eca349fd047b01f9aa0."
    - "ACP-0004/ACP-0005 state-machine and schema review completed."
  tests_failed: []
  tests_not_run:
    - "E2 runtime, IR-2 E2 adapter, full CPU suite, backend, hardware and learning tests: blocked or unauthorized."
  assumptions:
    - "The clarification gate is documentation-only and does not alter A01-A15."
  unresolved:
    - "Final residual ordinary episode identity."
    - "Final residual provenance episode ownership."
    - "Reset clearing/retained identity behavior during M."
    - "Named E2-capable IR-2 reconstruction interface and E1 rejection boundary."
  recommended_next_agent:
    - "Luna-0/project owner: amend ACP-0004 and reconcile ACP-0005 before creating Luna-21."
```

## Decision

**E2/M DISPATCH BLOCKED — ACP-0004 does not yet answer the four identity,
reset, provenance, and reconstruction-boundary questions listed above
unambiguously.**

The accepted M mode/phase, entry thresholds, promotion rules, timing,
payload, discharge, finite-return bound, cancellation, event identity,
bounded provenance, Model-B transfer, predictive-coding boundary, delayed
credit boundary, and backend neutrality are otherwise sufficient as
implementation constraints. This review deliberately did not create or
authorize Luna-21 and did not run E2 runtime tests.
