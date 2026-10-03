# Luna-0 Independent Closure — ACP-0005 TPCN-IR-2

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent TPCN-IR-2 schema closure"
  task_id: "independent-closure-acp-0005"
  component: "TPCN-IR-2 schema and E1 transfer adapter"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "630af038dafd91903e3b03c26059989585b3760c"
  result_revision: "corrective review revision pending publication"
  dependencies: ["ACP-0004 E1 closed", "ACP-0003 H1/IR-1 closed"]
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["VERIFICATION", "IMPLEMENTATION"]
  hypothesis: "IR-2 preserves all supported bounded E1 state and explicit IR-1 migration semantics."
  counter_hypothesis: "Transfer loses provenance lifecycle, legacy gain, finite resources, ownership, or ordering."
  interfaces_relied_on: ["ACP-0004 E1", "TPCN-IR-1", "ACP-0002 N2 Model-B"]
  label_information_boundary: ["No labels, evaluation, learning or reward state is represented."]
  timing_assumptions: ["Local timestamps and finite delays remain logical values."]
  reset_boundaries: ["Reconstruction restores counters and does not call reset."]
  resource_bounds: ["Finite network limits, event queue capacity, provenance capacity and one pending internal event."]
  authorized_scope: ["Independent ACP-0005 review and surgical schema corrections only."]
  unauthorized_scope: ["E2/M runtime, H2, N3, backends, hardware, calibration and learning."]
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A08", "A11", "A15"]
  preserves: ["A01-A15", "TPCN-IR-1 explicit upgrade boundary", "TPCV-1 separation"]
  architecture_change: false
  proposal: "ACP-0005"
  tests_added: ["adversarial IR-2 migration, M consistency and resource fixtures"]
  tests_passing: ["73 focused IR-2/E1/IR-1 tests", "full CPU suite pending corrective rerun"]
  tests_failed: []
  tests_not_run: ["GPU/FPGA/FPAA, E2/M runtime, H2, N3 and hardware equivalence"]
  assumptions: ["Generation reset remains E1-compatible because episode identity prevents stale cross-episode validation."]
  unresolved: ["Publication verification of the corrective revision."]
  recommended_next_agent: ["Project owner: authorize a separate bounded E2/M dispatch review only after this closure."]
```

## Review result

**OBSERVED:** The published implementation had five closure defects: hidden
pre-admission provenance state was not transferred; IR-1 upgrade omitted
legacy neuron gain, represented events and resource limits; explicit node
endpoints were widened silently; M ownership/phase consistency was incomplete;
and E1 conversion derived M parameters from unrelated E1 fields.

**CORRECTED:** The schema now transfers the missing bounded state, preserves
the complete supported IR-1 representation, rejects malformed topology,
validates schema-only M records, and leaves M parameters absent on E1-only
records. No E2/M execution or architecture change was introduced.

## Closure gate

The corrective revision is **PASS — TPCN-IR-2 EXCURSION EXECUTION SCHEMA
INDEPENDENTLY VERIFIED AND CLOSED**, conditional only on final publication
verification. Focused review tests pass 73 cases. A01-A15 remain unchanged.

E2/M, ACP-0003 H2, ACP-0002 N3, backends, hardware, calibration, Luna-13F
reopening and Luna-13G remain unauthorized.
