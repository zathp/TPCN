# Luna-0 Independent Review: ACP-0002 Stage N1

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of ACP-0002 Stage N1"
  task_id: "luna-0-review-acp-0002-n1"
  component: "Edge/neuron data model, compatibility, topology reconstruction and replay representation"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "7ddf00b6c7a8f01ad4ebe3483bc553c83dbe26d3"
  result_revision: "uncommitted review documentation"
  dependencies:
    - "ACP-0002 Accepted for staged implementation"
    - "Luna-15 N1 implementation handoff"
  owner: "Luna-0 Architecture Guardian"
  classification: ["VERIFICATION", "ARCHITECTURE-PROMOTION"]
  hypothesis: "N1 representation can preserve legacy runtime behavior while retaining bounded, inspectable edge and neuron state."
  counter_hypothesis: "Transfer fields alter routing, are lost during reconstruction, or make replay/fingerprints falsely identify distinct canonical edge state."
  interfaces_relied_on: ["Edge", "BoundedTopology", "TPCNNeuron", "StructuralPlasticityController", "EdgeInstrumentation", "TPCV-1"]
  label_information_boundary: ["No labels enter edge/neuron state, routing, or structural decisions."]
  timing_assumptions: ["Positive finite propagation delay, local timestamps, and queue sequence ordering remain unchanged."]
  reset_boundaries: ["Neuron reset remains character-local; persistent topology edge records survive rebuilds unless removed."]
  resource_bounds: ["Fan-in, fan-out, edge, routing, candidate, queue and bounded-state limits remain unchanged."]
  authorized_scope: ["Independent N1 review, evidence recording, workflow/changelog/handoff documentation"]
  unauthorized_scope: ["N2 transfer execution, adaptive edge learning, probationary edges, new utility policy, hardware equivalence, Luna-13G"]
  controls: ["Extreme dormant edge fields", "legacy three-tuples", "explicit Edge records", "prune/rebuild", "candidate-score separation", "observer route inspection", "gain alias equivalence"]
  measurements: ["Focused tests", "selected regression tests", "full CPU suite", "direct probes", "compileall", "git diff --check"]
  information_boundary_check: ["Routing reads delay/endpoints only; observer inspection is downstream-only; candidate scores are not edge parameters."]
  hardware_mapping: ["Fields remain bounded finite logical scalars; no hardware behavior or equivalence is claimed."]
  architecture_invariants_touched: ["A01 event-driven routing", "A02 local temporal state", "A03 finite delay", "A04 bounded topology", "A06 predictive paths", "A07 local learning", "A08 bounded state", "A09/A10 resource semantics", "A11 delayed credit", "A14 bounded structural plasticity", "A15 hardware independence"]
  preserves: ["A01-A15", "legacy payload routing", "event identity/timestamps/sequence", "Luna-13F closure"]
  architecture_change: false
  proposal: "ACP-0002"
  files_changed:
    - "workflow/docs/architecture/ACP-0002-N1.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-review-ACP-0002-N1.md"
  tests_added: []
  tests_passing:
    - "python -m pytest tests/test_acp0002_n1.py -q: 18 passed"
    - "Selected topology/neuron/structural/replay/regression tests: 83 passed; edge-instrumentation test file was not present"
    - "python -m pytest -q: 309 passed, 1 skipped"
    - "Direct edge-state/rebuild/defaults/routing/equality/bounds probe: DIRECT_N1_PROBE_PASS"
    - "Direct neuron-gain equivalence/conflict probe: NEURON_GAIN_PROBE_PASS"
    - "python -m compileall -q tpcn tests"
    - "git diff --check"
  tests_failed: []
  tests_not_run:
    - "CUDA and hardware gates: not applicable to N1"
    - "A separate legacy pre-N1 execution artifact comparison: not available; focused and full regression controls passed"
  assumptions: ["TPCV-1 remains a version-1 observability format; its contract explicitly requires a new format version for future connection fields."]
  unresolved: ["N2 must choose an explicit migration strategy because w=1,d=1,r=0 would produce tanh(a), not raw a, under Model-B."]
  recommended_next_agent: ["No N2 implementation assignment yet; project owner/Luna-0 must decide the explicit N2 legacy-equivalence boundary first."]
```

## Decision

**PASS - ACP-0002 N1 DATA MODEL AND COMPATIBILITY INDEPENDENTLY VERIFIED**

## Evidence

**OBSERVED:** `Edge` contains bounded `edge_weight` in `[-2,2]`,
`divider_strength` in `[0,1]`, `reference` in `[-1,1]`, positive finite delay,
and routing cost. Direct construction and public `from_edges()` paths reject
booleans, non-finite values and out-of-range values. Omitted transfer fields
produce exactly `1.0`, `1.0`, `0.0`; newly grown edges use those defaults.

**OBSERVED:** An explicit edge with `w=-2`, `d=0`, `r=1` routes the original
payload object unchanged. No `tanh`, multiplication, interpolation or
reference shift occurs. Event type, endpoints, timestamp, delay and sequence
remain legacy-compatible.

**OBSERVED:** `neuron_gain` is the single stored gain. `input_gain=x` and
`neuron_gain=x` produce equivalent state and activation across positive,
negative and delayed payloads; conflicting values are rejected.

**OBSERVED:** Explicit transfer fields survive topology pruning/reconstruction;
equality distinguishes edges differing only in any transfer field. Candidate
scores remain separate from grown edge state, and bounded admission/pruning
limits are unchanged.

**OBSERVED:** Edge instrumentation exposes the N1 fields without affecting
routing. TPCV-1 intentionally remains a version-1 observability boundary that
serializes endpoint and delay only; its contract requires a future format
version before connection transfer fields are encoded. This is an explicit
representation boundary, not a claim that TPCV-1 is complete N1 edge-state
serialization.

**INFERRED:** N1 successfully establishes representation compatibility without
changing network computation. A01-A15 are unchanged.

**HYPOTHESIZED:** A future N2 can activate static Model-B transfer only after
an explicit migration decision. N1 defaults are not a legacy signal identity
under that equation because `tanh(a) != a` in general.

## Governance gate

ACP-0002 remains **Accepted for staged implementation**. N1 is complete; N2 is
not authorized. N2 must remain separate from learning, maturation, probation,
new utility policy and time-series predictors. Luna-13F remains **CLOSED** and
Luna-13G remains unauthorized.
