# Luna-0 TPCN-IR-2 Architecture Decision

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "TPCN-IR-2 excursion-neuron schema decision"
  task_id: "tpcn-ir-2-schema-decision"
  component: "hardware-neutral excursion execution schema"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "439e419a7e949d51fa487cac1acef0634c83215f"
  result_revision: "uncommitted governance changes"
  dependencies:
    - "ACP-0003 H1/TPCN-IR-1 independently closed"
    - "ACP-0004 E1 independently closed"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["ARCHITECTURE-PROMOTION", "VERIFICATION"]
  hypothesis: "An explicit bounded IR-2 can represent accepted E1 state and future M state without changing canonical runtime semantics."
  counter_hypothesis: "The schema requires implicit dynamics, unbounded state, backend leakage, or cannot preserve E1 continuation identities."
  interfaces_relied_on: ["TPCN-IR-1", "ACP-0002 N2 Model-B", "ACP-0004 E1"]
  label_information_boundary:
    - "No labels, evaluation state or global learning state enters IR-2."
  timing_assumptions:
    - "Logical local timestamps and finite positive delays are serialized."
    - "Destination-local external-before-internal ordering is versioned explicitly."
  reset_boundaries:
    - "Reset clears character-local state; transfer restores serialized state and counters."
  resource_bounds:
    - "Finite accumulator, event budget, provenance capacity, pending-event slot and identity counters."
  authorized_scope:
    - "ACP-0005 schema implementation and E1 conversion/reconstruction."
    - "Deterministic serialization and the predeclared IR-2 fixtures."
  unauthorized_scope:
    - "E2/M runtime, backends, learning, H2, N3, hardware, calibration and visualization semantics."
  controls:
    - "ACP-0003 H1/IR-1 compatibility and ACP-0004 E1 closed behavior."
    - "Explicit version, dynamics, mode, identity and cross-field validation."
  measurements:
    - "Schema validation, deterministic round trips, identity continuation and legacy regression results."
  information_boundary_check:
    - "No CUDA, RTL, FPGA placement, FPAA calibration or backend state is canonical IR-2 data."
  hardware_mapping:
    - "IR-2 is hardware-neutral; realization and calibration state remain adapter-owned."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A11", "A15"]
  preserves:
    - "A01-A15"
    - "ACP-0002 N2 Model-B"
    - "ACP-0003 H1/TPCN-IR-1"
    - "TPCV-1 downstream-only boundary"
  architecture_change: false
  proposal: "ACP-0005"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0005.md"
    - "workflow/docs/architecture_proposals/ACP-0003.md"
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/README.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-architecture-decision-IR-2.md"
    - ".github/agents/luna-20.agent.md"
  tests_added: []
  tests_passing:
    - "Repository revision and clean starting-state verification"
    - "Documentation consistency and merge-marker checks"
    - "git diff --check"
  tests_failed: []
  tests_not_run:
    - "IR-2 runtime, backend, hardware and E2/M tests: not implemented or unauthorized."
  assumptions:
    - "The existing H1 conversion boundary is the compatibility source for IR-1."
  unresolved:
    - "Luna-20 must implement and independently verify the accepted schema."
  recommended_next_agent:
    - "Luna-20: implement only ACP-0005, then return for independent review."
```

## Outcome

**OBSERVED:** ACP-0005 accepts `TPCN-IR-2` as a distinct schema version with
explicit dynamics, bounded E1 state, future M representation, migration
rules, validation and scope exclusions.

**INFERRED:** The schema can remain compatible with IR-1 only through an
explicit `TANH_LEGACY` tag and cannot safely downgrade `EXCURSION_V1`.

**OBSERVED:** No runtime, backend, learning or hardware implementation was
performed. The final publication is the uncommitted governance tree based on
`439e419a7e949d51fa487cac1acef0634c83215f`.

## Next assignment

Luna-20 may implement the ACP-0005 schema, deterministic serialization,
reference conversion/reconstruction and listed fixtures. It must return for
independent review. E2/M remains unauthorized and integration is not ready
until those checks pass.
