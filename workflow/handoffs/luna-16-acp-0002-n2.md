# Luna-16 ACP-0002 N2 Static Model-B Edge Transfer

```yaml
tpcn_handoff:
  agent: Luna-16
  luna_identifier: "Luna-16"
  descriptive_name: "ACP-0002 N2 Static Model-B Edge Transfer"
  task_id: "ACP-0002-N2"
  component: "Static edge transfer execution and ACP-approved destination neuron path"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "8760daf699237131e213cbf5df94b405bba8dfea"
  result_revision: "ed8aaff2d0d0d031c2c1f84b311251f530282479"
  dependencies: ["ACP-0002 accepted", "Luna-15 N1 and independent review published"]
  owner: "Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "Static Model-B transfer can become canonical while preserving event-runtime invariants."
  counter_hypothesis: "Transfer activation breaks causality, boundedness, deterministic replay, locality or structural limits."
  interfaces_relied_on: ["Edge", "BoundedTopology", "EventQueue", "TPCNNeuron", "StructuralPlasticityController", "EdgeInstrumentation", "TPCV-1"]
  label_information_boundary: ["Labels remain outside events, routing, topology, transfer and resource accounting.", "Future events do not enter transfer computation."]
  timing_assumptions: ["Positive finite delays, local timestamps and deterministic sequence ordering."]
  reset_boundaries: ["Existing neuron, queue, eligibility and topology reset semantics are retained."]
  resource_bounds: ["Existing finite edge, fan-in/out, routing, queue, state and event budgets."]
  authorized_scope: ["Static z=tanh(w*a) and v=d*z+(1-d)*r.", "Existing delayed destination integration.", "Analytic baseline and focused invariant tests."]
  unauthorized_scope: ["Edge learning", "probationary/maturing edges", "new utility/pruning policy", "temporal mini-networks", "hardware voltage semantics", "TPCV version change", "N3/later stages", "Luna-13G"]
  controls: ["Endpoints", "weight zero", "signed inputs/weights", "reference/divider independence", "fan-in/out", "equal/unequal delays", "recurrence budget", "reconstruction", "observer ON/OFF", "control payload", "full regression"]
  measurements: ["Analytic payloads, timestamps, state/activation, queue/event budgets, topology defaults, replay and observer equality."]
  information_boundary_check: ["Only source activation and immutable edge fields enter Model-B transfer."]
  hardware_mapping: ["Bounded multiply, fixed tanh, interpolation and delay; activity-cost proxy only, no joule claim."]
  architecture_invariants_touched: ["A01-A04", "A06-A11", "A14", "A15"]
  preserves: ["A01-A15", "historical artifact meaning", "Luna-13F closure", "Luna-13G unauthorized status"]
  architecture_change: false
  proposal: "ACP-0002 staged N2 authorization"
  files_changed: ["tpcn/topology.py", "tests/test_acp0002_n1.py", "tests/test_acp0002_n2.py", "tests/test_topology.py", "tests/test_luna11_adversarial.py", "tests/test_structural_plasticity.py", "workflow/docs/architecture_proposals/ACP-0002.md", "workflow/docs/luna/LUNA_WORKFLOW.md", "workflow/ARCHITECTURE_CHANGELOG.md", "workflow/handoffs/luna-16-acp-0002-n2.md", "artifacts/acp-0002-n2-model-b-baseline/baseline.json"]
  tests_added: ["tests/test_acp0002_n2.py"]
  tests_passing: ["Focused N2: 267 passed", "Full CPU suite: 549 passed, 1 skipped", "compileall", "git diff --check"]
  tests_failed: []
  tests_not_run: ["Independent Luna-0 N2 review", "hardware/CUDA acceptance", "TPCV version update"]
  assumptions: ["TPCV-1 remains an observational format and does not claim active transfer-state equivalence."]
  unresolved: ["Future computationally equivalent transfer-state replay requires separate TPCV governance."]
  recommended_next_agent: ["Luna-0 for independent N2 review; no successor stage is authorized."]
```

## Results

**OBSERVED:** The canonical edge equation is `z=tanh(w*a)` followed by
`v=d*z+(1-d)*r`. The destination equation remains local-time decay, clipped
integration, neuron gain and fixed `tanh` activation. `d=0` returns `r`,
`d=1` returns `z`, and `w=0` removes the source branch. Signed weights and
activations preserve the odd symmetry of the transformed source component;
the reference can intentionally break output symmetry.

**OBSERVED:** Fan-out computes independent payloads per edge. Equal-time fan-in
is processed sequentially in deterministic queue order. Unequal delays produce
no pre-arrival effect and decay between arrivals. A five-event recurrent run
stopped explicitly at the event budget with one pending event and peak queue
occupancy one. Structural growth uses `w=1,d=1,r=0`; reconstruction preserves
explicit edge state. Observer ON/OFF and replay are computationally equal.

**OBSERVED:** Each routed neural edge adds conceptual bounded operations for
`w*a`, fixed `tanh`, and divider interpolation. Existing resource semantics
permit only an activity-cost-proxy statement; no calibrated energy or hardware
equivalence is claimed.

**TPCV RESULT:** `TPCV-1 REMAINS VALID FOR ITS LIMITED DECLARED PURPOSE`.
Its omission of active transfer fields is explicit; no format change was made.

Historical pre-N2 results retain their original meaning. Luna-13F is CLOSED;
Luna-13G and N3/later ACP-0002 stages remain unauthorized. Return to Luna-0.