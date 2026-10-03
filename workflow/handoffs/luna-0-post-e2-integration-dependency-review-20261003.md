# Luna-0 Post-E2 Integration Dependency Review

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Post-E2 integration dependency review"
  task_id: "luna-0-post-e2-integration-dependency-review-20261003"
  component: "ACP-0004 excursion runtime integration with the predictive-coding experiment path"
  status: "complete; integration blocked pending migration-boundary decision"
  contract_version: "1.1"
  branch: "main"
  base_revision: "c872dc8fbf74bf1a4e836619f1e02a96271c8633"
  result_revision: "governance publication commit; see Git history"
  dependencies:
    - "Luna-19 ACP-0004 E1 implementation and independent closure"
    - "Luna-20 ACP-0005 TPCN-IR-2 revision 1 implementation and independent closure"
    - "Luna-21 ACP-0004 E2 runtime and corrective IR-2 review closure"
    - "ACP-0002 N2 Model-B"
  owner: "Project owner / Luna-0 architecture authority"
  classification: ["GOVERNANCE REVIEW", "INTEGRATION-READINESS REVIEW"]
  hypothesis: "Closed E1/E2 components and ACP-0004 fully specify the next production-path integration so a bounded successor implementation can be dispatched without further migration decisions."
  counter_hypothesis: "The actual runtime lacks an excursion consumer and ACP-0004 does not specify the migration/model-selection and learning interfaces needed for a safe integration dispatch."
  interfaces_relied_on:
    - "ExperimentRunner and _ComputationalNetwork"
    - "TPCNNeuron.receive_event and scalar activation"
    - "LocalPredictor.create_prediction and create_prediction_from_neuron"
    - "EligibilityActivity, EligibilityLedger and PredictionError"
    - "SingleExcursionNeuron / MultiExcursionNeuron receive_event, pending-event queue and ExcursionEmission"
    - "neuron_from_ir2 and neuron_from_ir2_e2"
    - "ACP-0004 post-migration Model-B source rule"
  label_information_boundary:
    - "No labels or evaluation state were introduced into canonical neuron state."
  timing_assumptions:
    - "No timing behavior was changed; a future integration must preserve local event timestamps, positive finite propagation and deterministic ordering."
  reset_boundaries:
    - "No reset behavior was changed; a future integration must specify reset of pending internal events and preserve identity high-water marks."
  resource_bounds:
    - "No runtime or resource bounds were changed."
  authorized_scope:
    - "Inspect current workflow status and reconcile the stale Luna-21 table row."
    - "Determine whether the accepted excursion architecture and closed reference components support an integration dispatch."
    - "Record evidence, unresolved decisions and integration readiness."
  unauthorized_scope:
    - "Production code changes, successor Luna execution or contract creation."
    - "New ACP, canonical migration, architecture promotion, learning changes, backend work or hardware equivalence."
  controls:
    - "Preserve the published Luna-21 independent closure and historical blocking review."
    - "Preserve ACP-0004 staged status and ACP-0005 schema revision 1."
    - "Preserve ACP-0002 N2 and A01-A15."
  measurements:
    - "Inspected runtime construction, routing, prediction, eligibility, reset, excursion APIs, IR-2 adapters, tests and governance records."
  information_boundary_check:
    - "Review only; no new data or information path was implemented."
  hardware_mapping:
    - "None; backend and hardware gates remain closed or reserved."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A11", "A15"]
  preserves:
    - "Luna-21 independently verified closure."
    - "ACP-0004 accepted-for-staged-implementation status."
    - "ACP-0005 / TPCN-IR-2 schema revision 1."
    - "ACP-0002 N2 and A01-A15."
    - "All independent backend, hardware, N3, H2 and IR-3 gates."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-post-e2-integration-dependency-review-20261003.md"
  files_reviewed:
    - "workflow/ARCHITECTURE_CONTRACT.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md"
    - "workflow/docs/architecture_proposals/README.md"
    - "workflow/docs/architecture_proposals/ACP-TEMPLATE.md"
    - "workflow/docs/architecture_proposals/ACP-0003.md"
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/docs/architecture_proposals/ACP-0005.md"
    - "workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md"
    - "workflow/handoffs/luna-0-independent-corrective-review-ACP-0004-E2-Luna-21-20261003.md"
    - "tpcn/experiments.py"
    - "tpcn/canonical_neuron.py"
    - "tpcn/excursion_neuron.py"
    - "tpcn/predictive_coding.py"
    - "tpcn/eligibility.py"
    - "tpcn/ir2.py"
    - "tests/test_experiments.py"
    - "tests/test_excursion_neuron.py"
    - "tests/test_e2_multi_excursion.py"
    - "tests/test_ir2.py"
    - "tests/test_e2_ir2.py"
  tests_added: []
  tests_passing:
    - "Not applicable; documentation/governance-only review."
  tests_failed: []
  tests_not_run:
    - "No tests or runtime experiments; no production code changed."
    - "No hardware/backend validation."
  assumptions:
    - "The Git SHA and published main branch are authoritative for baseline."
  unresolved:
    - "Project owner / Luna-0 must decide whether the normal production path selects EXCURSION_V1 as its canonical neuron, and how explicitly labelled TANH_LEGACY compatibility is exposed."
    - "Specify how excursion outputs drive Model-B routing, prediction creation/target matching, explicit prediction-error delivery, eligibility attribution and the external readout."
    - "Specify how reset, pending internal work, identity high-water marks and IR-2 reconstruction interact with a live integrated network."
    - "No successor Luna number or implementation assignment is authorized until these boundaries are recorded."
  recommended_next_agent:
    - "Project owner / Luna-0: record the migration/model-selection and cross-component interface decision, then determine whether it is a compatible implementation dispatch or requires an ACP."
```

## Outcome and owned scope

The stale Luna-21 status-table row was corrected from the superseded blocked
verdict to `CLOSED / independently verified`. This reconciles the table with
the current workflow prose and Luna-0's independent corrective closure. The
earlier blocked review remains historical evidence.

## Architecture evidence

**OBSERVED:** `ExperimentRunner` constructs `_ComputationalNetwork`, whose
neurons are `TPCNNeuron` instances. Its event handler feeds numeric payloads to
`TPCNNeuron.receive_event`, routes returned scalar activations, and exposes
those scalars to prediction, eligibility and readout logic. The
`LocalPredictor.create_prediction_from_neuron` adapter also accepts
`TPCNNeuron`.

**OBSERVED:** `SingleExcursionNeuron` and `MultiExcursionNeuron` are exposed
reference components. Their `receive_event` API accepts an event and optional
queue and may produce an `ExcursionEmission`; E2 also schedules internal
events. Production references outside the excursion module are IR-2
serialization/reconstruction and package exports. The experiment network has
no excursion runtime consumer. Existing component and IR-2 tests cover neuron
behavior and serialization/reconstruction, not connection to the predictive
coding experiment network.

**OBSERVED:** ACP-0004 says that after migration, Model-B source activity is
`a_i := p_exc`; the old continuous output is an explicitly labelled
compatibility/diagnostic value, not a second canonical stream. ACP-0005/IR-2
represents and reconstructs excursion-neuron state but is not a live-network
checkpoint or network-level model selector.

**INFERRED:** The accepted semantics fix what a migrated excursion contributes
to Model-B, but do not provide a complete migration contract for the current
ordinary runtime. No canonical behavior is changed by this review.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `git status --short --branch`; `git rev-parse HEAD`; `git rev-parse origin/main` | Windows; baseline `c872dc8fbf74bf1a4e836619f1e02a96271c8633` | Clean `main`; local HEAD equals origin/main | Command output |
| Source and governance inspection | Published baseline; no runtime execution | Confirms ordinary network uses `TPCNNeuron`; excursion code is separate; workflow table was stale | Files listed in YAML |
| Tests / runtime experiments | Not run | Documentation-only change; no implementation claim | Not applicable |
| `git diff --check` | Review result revision | Passed | Changelog and final session report |

## Assumptions, limitations and unresolved issues

The next step is a project-owner / Luna-0 decision, not an implementation
dispatch. The owner should decide the normal path's canonical model-selection
behavior, compatibility boundary and how predictions, errors, credit and
readout consume excursion events. The owner should also decide whether
existing ACP-0004/0005 contracts suffice for that work or an ACP clarification
is required. No ACP-0006 or Luna-22 is proposed by this review.

## Next assignment

Project owner / Luna-0: record those bounded interface and migration decisions.
Only after that decision should Luna-0 classify the work as compatible
integration or architecture change, assign a new Luna identifier if needed,
and authorize a handoff. Integration readiness remains **blocked**.
