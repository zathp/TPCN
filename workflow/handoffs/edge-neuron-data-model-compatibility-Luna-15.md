# Luna-15 N1 Handoff

```yaml
tpcn_handoff:
  agent: Luna-15
  luna_identifier: "Luna-15"
  descriptive_name: "ACP-0002 Edge/Neuron Data Model and Compatibility"
  task_id: "ACP-0002-N1"
  component: "Edge and canonical neuron data model"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "aee448a0e1f8064c3b4b84cefb210e337958d213"
  result_revision: "4297f4348f8d1d19438fea91c99bc72648cd4c3c (initial commit; final amended hash recorded below)"
  dependencies:
    - "ACP-0002 accepted for staged implementation"
  owner: "Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "Validated explicit N1 state plus a legacy identity route marker preserves current construction, replay, observer, and payload behavior."
  counter_hypothesis: "A focused or regression test changes due to the representational fields or topology rebuilds."
  interfaces_relied_on: ["Edge", "BoundedTopology", "TPCNNeuron", "StructuralPlasticityController", "EdgeInstrumentation"]
  label_information_boundary: ["No labels enter edge or neuron state."]
  timing_assumptions: ["Propagation delay remains finite and positive; event timestamps and queue sequence ordering remain unchanged."]
  reset_boundaries: ["Neuron reset retains neuron_gain; topology reset/rebuild retains explicit edge records."]
  resource_bounds: ["Existing fan-in, fan-out, edge, routing, candidate, and queue limits are unchanged."]
  authorized_scope: ["Validated edge_weight, divider_strength, reference", "neuron_gain compatibility", "full-record topology rebuild", "observer inspection", "focused tests and documentation"]
  unauthorized_scope: ["N2 transfer execution", "edge learning", "temporary/probationary edges", "maturation", "new pruning or reward semantics", "Luna-13G", "hardware equivalence"]
  controls: ["Legacy three-tuples", "explicit Edge records", "observer on/off path", "payload identity and Model-B non-activation check"]
  measurements: ["Focused N1 pass count", "topology/neuron/structural regression count", "payload, timestamp, sequence, and representation equality"]
  information_boundary_check: ["Candidate score is not copied into edge parameters; route uses no observer or label data."]
  hardware_mapping: ["Fields are bounded finite logical scalars; no hardware behavior is claimed."]
  architecture_invariants_touched: ["A03 positive finite delay", "A04 bounded topology", "A08 bounded state", "A14 structural compatibility", "A15 hardware independence"]
  preserves: ["A01-A15", "event-driven execution", "local time", "predictive/error paths", "delayed credit", "energy semantics", "Luna-13F closure"]
  architecture_change: false
  proposal: "ACP-0002"
  files_changed:
    - "tpcn/topology.py"
    - "tpcn/canonical_neuron.py"
    - "tpcn/structural_plasticity.py"
    - "tpcn/edge_instrumentation.py"
    - "tests/test_acp0002_n1.py"
    - "workflow/docs/architecture/ACP-0002-N1.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/edge-neuron-data-model-compatibility-Luna-15.md"
  tests_added: ["tests/test_acp0002_n1.py"]
  tests_passing:
    - "python -m pytest tests/test_acp0002_n1.py -q: 18 passed"
    - "relevant regression command: 178 passed"
    - "python -m pytest -q: 309 passed, 1 skipped"
    - "python -m compileall -q tpcn tests"
    - "git diff --check"
  tests_failed: []
  tests_not_run:
    - "CUDA/hardware gates: not applicable to N1"
  assumptions: ["The current clean main revision is the synchronized origin/main baseline."]
  unresolved: ["N2 must choose an explicit legacy-transfer migration gate because tanh(a) is not raw identity."]
  recommended_next_agent: ["Return to Luna-0 for independent N1 review; N2 remains unauthorized."]
```

## Evidence

**OBSERVED:** The N1 edge fields are validated and included in frozen dataclass
equality and deterministic representation. Legacy three-tuples construct
`w=1.0`, `d=1.0`, `r=0.0` records with `legacy_identity=True`. Explicit records
survive topology construction, structural growth rebuilds, and pruning of
another edge. Instrumentation exposes all fields.

**OBSERVED:** `BoundedTopology.route()` remains unchanged semantically: it
queues the original payload, preserves source/destination/event type, adds the
existing positive delay, and receives deterministic queue sequence numbers.
N1 does not evaluate the Model-B equation or add an edge runtime cost.

**OBSERVED:** `input_gain` and `neuron_gain` resolve to one stored
`neuron_gain`; equal aliases work and disagreement is rejected. Existing
`input_gain` callers remain valid.

**INFERRED:** The record and adapter provide data-model compatibility without
claiming future signal-equation compatibility.

**HYPOTHESIZED:** A separately authorized N2 migration gate can activate Model-B
without silently changing legacy comparisons. N1 does not test or implement
that transfer.

## Validation record

The focused command was `python -m pytest tests/test_acp0002_n1.py -q` with 18
passed. The relevant regression command passed 178 tests. The full CPU suite
was `python -m pytest -q` with 309 passed and 1 skipped. Static checks passed
with `python -m compileall -q tpcn tests` and `git diff --check`; diagnostics
reported no errors in the changed Python files. The starting revision was
`aee448a0e1f8064c3b4b84cefb210e337958d213`, branch `main`, with a clean tree
and tree hash `bab9b3a695bf258617b91bced1913fb4695121fc`. The initial
publication commit was `4297f4348f8d1d19438fea91c99bc72648cd4c3c`; the final
amended publication revision is recorded by final repository verification. No
N2 authorization is implied.

## Gate

ACP-0002 remains **Accepted for staged implementation**. N1 completion does not
authorize N2. A01-A15 are unchanged. Luna-13F is **CLOSED**. Luna-13G is
**unauthorized**. Control returns to Luna-0 for independent review.
