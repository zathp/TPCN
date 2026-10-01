# Luna-0 Architecture Review Handoff: ACP-0002

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0 architecture review"
  descriptive_name: "Independent edge signal transformation and neuron gain separation"
  task_id: luna-0-architecture-review-acp-0002
  component: "Canonical topology edge and event-driven neuron signal path"
  status: complete
  contract_version: "1.1"
  branch: main
  base_revision: 25aa7697d523c13f0fdcf56c84170ceb553cc229
  result_revision: uncommitted
  dependencies: ["Luna-13F closed"]
  owner: "Project owner for architecture decision"
  classification: ["ARCHITECTURE-PROMOTION"]
  hypothesis: "Model B interpolation can represent an independently buffered per-edge reference and adjustable signal-divider strength while preserving bounded causal semantics."
  counter_hypothesis: "Reference interpolation fails endpoint independence, boundedness, distinct w/d roles or hardware-neutral mapping."
  interfaces_relied_on: ["Edge", "BoundedTopology.route", "EventQueue", "TPCNNeuron.receive_event", "StructuralPlasticityController"]
  label_information_boundary: ["Labels remain outside edge transformation and neuron state."]
  timing_assumptions: ["Positive finite edge delays; timestamp then sequence ordering; no global neural timestep."]
  reset_boundaries: ["Neuron dynamic state resets at the existing character boundary; persistent topology/edge parameters persist unless an explicit topology reset is requested."]
  resource_bounds: ["w [-2,2]", "d [0,1]", "r [-1,1]", "g [0,2]", "bounded neuron state", "existing edge/fan-in/fan-out/routing/queue limits"]
  authorized_scope: ["Architecture assessment", "ACP-0002 creation", "workflow/changelog/handoff documentation"]
  unauthorized_scope: ["Production code", "edge learning", "probation/maturation", "local time-series predictor", "Luna-13G"]
  controls: ["Analytic transfer fixtures", "Model A versus Model B grid", "identity-adapter legacy comparison", "deterministic replay", "observer ON/OFF", "label/future isolation"]
  measurements: ["Edge contribution", "arrival timestamp", "state/activation bounds", "fan-in and delay behavior", "resource proxy impact"]
  information_boundary_check: ["Edge transform consumes only source activation and edge-local bounded state; evaluation and labels are excluded."]
  hardware_mapping: ["Finite digital fields or later conductance/divider/reference/delay elements; hardware clocks are not neural time."]
  architecture_invariants_touched: ["A01-A15 reviewed; no clause changed"]
  preserves: ["Closed Luna-13F negative result", "Luna-13G unauthorized", "event runtime", "local decay", "finite propagation", "predictive coding and delayed credit contracts"]
  architecture_change: true
  proposal: ACP-0002
  files_changed: ["workflow/docs/architecture_proposals/ACP-0002.md", "workflow/ARCHITECTURE_CHANGELOG.md", "workflow/docs/luna/LUNA_WORKFLOW.md", "workflow/handoffs/luna-0-architecture-review-ACP-0002.md"]
  tests_added: []
  tests_passing: ["Repository baseline clean and synchronized at 25aa7697d523c13f0fdcf56c84170ceb553cc229", "Requested analytic grid: Model B passes d=0 reference endpoint and d=1 signal endpoint; bounded output verified algebraically"]
  tests_failed: []
  tests_not_run: ["Production implementation and runtime analytic tests; production code was not changed"]
  assumptions: ["Source and reference values use normalized [-1,1] logical units."]
  unresolved: ["final numeric precision", "future edge learning rule", "hardware calibration"]
  recommended_next_agent: ["Luna-1/Luna-2/Luna-4 owners implement N1 edge/neuron data model and compatibility representation with independent verification"]
```

## Outcome and architecture evidence

**OBSERVED:** The requested grid shows the subtraction form emits zero for
every reference when `d=0`. **INFERRED:** this is incompatible with an
independently buffered reference endpoint. **SELECTED:**
`v_ij = d_ij*tanh(w_ij*a_i) + (1-d_ij)*r_ij` preserves endpoint semantics,
boundedness and distinct `w`/`d` controls.

ACP-0002 is **Accepted for staged implementation**. Only N1, edge/neuron data
model and compatibility representation, is authorized. N2 transfer semantics,
edge learning, temporary maturation, local predictors and Luna-13G remain
unauthorized. The contract remains version 1.1 and no A01-A15 clause is
amended.

## Validation record

| Command or procedure | Revision / environment | Observed result |
|---|---|---|
| Repository status, revision and diff check | `25aa7697d523c13f0fdcf56c84170ceb553cc229`, `main`, Windows | Clean, `HEAD == origin/main`, diff check passed |
| Read governing contract, changelog, workflow, acceptance criteria, ACP template | Same revision | Sources present under `workflow/`; next unused ACP is `ACP-0002` |
| Inspect current edge/neuron/runtime APIs | Same revision | Edge carries endpoint/delay/routing metadata; neuron applies `input_gain`; runtime is event-driven |
| Requested analytic comparison | `w=1`, `a in {-1,0,1}`, `d in {0,0.5,1}`, `r in {-0.5,0,0.5}` | Model A fails reference endpoint at `d=0`; Model B passes `d=0 -> r`, `d=1 -> tanh(a)` and remains in `[-1,1]` |
| Implementation tests | N1 not yet implemented | Not run; no production code changed |
| Hardware equivalence | Out of scope | Not run |

## Next assignment

The next bounded implementation assignment is **N1 - edge/neuron data model
and compatibility representation**, owned jointly by the topology/runtime
maintainers. N1 must represent bounded `w`, `d`, `r` and `neuron_gain`, retain
an explicit legacy identity adapter, and add no transfer execution or learning.
Integration remains blocked pending N1 verification.
