# Luna-0 Independent Architecture Review: ACP-0004

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of ACP-0004 canonical excursion neuron"
  task_id: "luna-0-independent-review-ACP-0004"
  component: "Canonical neuron architecture"
  status: "complete"
  contract_version: "1.1"
  branch: "copilot/architecture-update-next-canonical-neuron-model"
  base_revision: "c18757739f4055bbb5721520a14382701e177d64"
  result_revision: "uncommitted review disposition"
  dependencies:
    - "ACP-0002 N2 CLOSED"
    - "ACP-0003 H1 independently verified and CLOSED"
    - "ACP-0003 H2 unauthorized"
  owner: "Luna-0 Architecture Guardian / project owner"
  classification: ["VERIFICATION", "ARCHITECTURE_REVIEW"]
  hypothesis: "ACP-0004 defines an implementable backend-neutral bounded excursion state machine."
  counter_hypothesis: "Cardinality, autonomous timing, state ownership, edge-source semantics, provenance bounds, or IR migration remain ambiguous."
  interfaces_relied_on:
    - "A01-A15 architecture contract"
    - "ACP-0002 N2 Model-B edge transfer"
    - "ACP-0003 TPCN-IR-1 and backend separation"
  label_information_boundary:
    - "No labels, future inputs or global orchestration state may enter the proposed neuron."
  timing_assumptions:
    - "No global neural timestep; autonomous return requires explicit finite local internal events."
    - "Equal-time external events remain sequential and deterministically ordered."
  resource_bounds:
    - "X_max, amplitude, phase, hysteresis, provenance, pending internal events and event budgets must be finite."
  authorized_scope:
    - "Independent review and documentation correction of ACP-0004."
    - "Terminology clarification in ACP-0003 without changing authorization."
  unauthorized_scope:
    - "Production neuron, learning, GPU/FPGA/FPAA backends, ACP-0003 H2, ACP-0002 N3, Luna-13G and Luna-19."
  controls:
    - "One canonical excursion must map to one digital emission event unless a future proposal defines explicit framing and identity."
    - "Canonical excursion remains distinct from digital event and analog spike realization."
    - "No implementation-ready acceptance is inferred from conceptual coherence."
  measurements:
    - "No runtime measurements; this is a documentation review."
  architecture_invariants_touched:
    - "A01"
    - "A02"
    - "A03"
    - "A06"
    - "A07"
    - "A08"
    - "A11"
    - "A15"
  preserves:
    - "A01-A15 unchanged"
    - "Model-B z=tanh(wa), v=dz+(1-d)r"
    - "TPCN-IR-1 current scope"
    - "ACP-0002 N3 unauthorized"
    - "ACP-0003 H2 unauthorized"
    - "Luna-13F CLOSED; Luna-13G unauthorized; Luna-17 reserved"
  architecture_change: false
  proposal: "ACP-0004 remains Draft; revision required before acceptance"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/docs/architecture_proposals/ACP-0003.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-independent-review-ACP-0004.md"
  tests_added: []
  tests_passing:
    - "Proposal and authoritative-state source audit"
    - "Baseline revision and clean-start verification"
  tests_failed: []
  tests_not_run:
    - "Runtime/build/lint tests: no production code changed."
    - "Backend, H2, calibration and hardware-equivalence checks: unauthorized."
  assumptions:
    - "The project owner will decide whether to revise or reject ACP-0004."
  unresolved:
    - "All eleven blocking canonical decisions listed in ACP-0004 review disposition."
    - "No implementation dispatch is justified."
  recommended_next_agent:
    - "Project owner/Luna-0 to revise ACP-0004; independent re-review after the blockers are resolved."
```

## Review outcome

**ACP-0004 REMAINS DRAFT — NOT ACCEPTED FOR STAGED IMPLEMENTATION.**

The terminology boundary and general bounded-accumulator direction are
architecturally compatible. They are insufficient for acceptance because the
draft leaves digital cardinality, autonomous internal event scheduling,
ordinary-return re-arm, exact discharge semantics, signed emission identity,
bounded provenance overflow, post-migration Model-B source value, and IR
versioning open. The complete blocker list is recorded in ACP-0004.

No production code, learning rule, backend, H2 work, edge learning, N3 work,
Luna-13G work or Luna-19 contract was created or authorized.
