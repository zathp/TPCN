# Luna-0 Architecture Decision — ACP-0006 Excursion Integration

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Excursion integration and migration architecture decision"
  task_id: "luna-0-architecture-decision-ACP-0006-20261003"
  component: "Network-level migration of ACP-0004 E1/E2 into predictive-coding experiments"
  status: "complete; ACP-0006 under review; owner acceptance required"
  contract_version: "1.1"
  branch: "main"
  base_revision: "813186f87e7074415b550cf051ad2435c028d52a"
  result_revision: "publication commit to be recorded after commit"
  dependencies:
    - "ACP-0002 N2 static Model-B transfer, closed"
    - "ACP-0003 H1 Execution IR/backend skeleton, closed"
    - "ACP-0004 E1 and E2 excursion reference, closed"
    - "ACP-0005 TPCN-IR-2 schema revision 1/E2 reconstruction, closed"
    - "Luna-21 independent corrective closure"
  owner: "Project owner; explicit acceptance is required by proposal governance"
  classification: ["ARCHITECTURE DECISION", "MIGRATION CONTRACT DEFINITION", "CROSS-COMPONENT INTERFACE DEFINITION"]
  hypothesis: "A separate, bounded integration/migration ACP is required because current accepted proposals do not normatively define the experiment network's causal scheduler, migration selector or cross-component interfaces."
  counter_hypothesis: "ACP-0004/0005 already determine these network behaviors, so a compatible implementation-only integration dispatch is sufficient."
  interfaces_relied_on:
    - "_ComputationalNetwork and ExperimentRunner"
    - "TPCNNeuron event/activation API"
    - "MultiExcursionNeuron / ExcursionEmission / PendingInternalEvent"
    - "EventQueue / execute_bounded"
    - "BoundedTopology Model-B route"
    - "LocalPredictor / PredictionError"
    - "EligibilityLedger / EligibilityActivity / RewardSignal"
    - "StreamingCharacterClassifier"
    - "LocalEnergyModel"
    - "IR-2 E1/E2 adapters"
  label_information_boundary:
    - "Labels remain external and may affect only post-readout outer reward/prototype updates."
    - "Prediction observations use only the current admitted numeric input payload."
  timing_assumptions:
    - "Per-character logical time is monotonic; no global neural tick or wall-clock wait."
    - "External inputs are admitted incrementally against an input-time watermark."
    - "Edges retain finite positive propagation delays and established deterministic tie ordering."
  reset_boundaries:
    - "Character queue/route sidecar are discarded after bounded settling; E2 pending work is invalidated by neuron reset."
    - "Neuron identity high-water counters persist across character reset."
    - "Experiment reset creates a new namespace and destroys all model/readout state."
  resource_bounds:
    - "Finite per-character queue and integrated event budget."
    - "Existing per-neuron E2 budget and provenance capacity."
    - "Bounded prediction/eligibility/error-delivery/readout statistics and route path."
  authorized_scope:
    - "Inspect current architecture and source evidence."
    - "Classify and document the missing integration boundary."
    - "Create ACP-0006 Under review and a Luna-0 decision handoff."
    - "Update workflow and changelog to identify proposal status."
  unauthorized_scope:
    - "Production integration or any implementation campaign."
    - "ACP acceptance/promotion without explicit project-owner acceptance."
    - "Successor Luna contract, Luna identifier assignment or authorization."
    - "A01-A15 changes, N3, H2, IR-3, learning/reward redesign, backends, calibration or hardware."
  controls:
    - "Explicit network-wide TANH_LEGACY comparison/control."
    - "Network-wide EXCURSION_V1/E2 integrated condition."
    - "Same external stream, fixed topology, timestamps, budgets, reset and label boundary."
  measurements:
    - "Repository baseline, queue/runtime API, emitted event identity, prediction/eligibility/readout adapter surfaces, IR-2 exclusions and proposal/Luna numbering."
  information_boundary_check:
    - "No implementation; proposed contract excludes labels/future stream data from neural inputs."
  hardware_mapping:
    - "Hardware-neutral logical proposal only; no backend mapping or equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "A01-A15 text."
    - "ACP-0002 N2, ACP-0004 E1/E2 and ACP-0005 schema revision 1."
    - "Luna-21 closed status."
    - "Fixed-topology/no-N3 first integration boundary."
  architecture_change: false
  proposal: "ACP-0006, Under review"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0006.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-architecture-decision-ACP-0006-20261003.md"
  files_reviewed:
    - "workflow/ARCHITECTURE_CONTRACT.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md"
    - "workflow/docs/architecture_proposals/README.md"
    - "workflow/docs/architecture_proposals/ACP-TEMPLATE.md"
    - "workflow/docs/architecture_proposals/ACP-0002.md"
    - "workflow/docs/architecture_proposals/ACP-0003.md"
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/docs/architecture_proposals/ACP-0005.md"
    - "workflow/handoffs/luna-0-post-e2-integration-dependency-review-20261003.md"
    - "workflow/handoffs/luna-0-independent-corrective-review-ACP-0004-E2-Luna-21-20261003.md"
    - "tpcn/experiments.py"
    - "tpcn/canonical_neuron.py"
    - "tpcn/excursion_neuron.py"
    - "tpcn/event_runtime.py"
    - "tpcn/topology.py"
    - "tpcn/predictive_coding.py"
    - "tpcn/eligibility.py"
    - "tpcn/streaming_classifier.py"
    - "tpcn/energy_utility.py"
    - "tpcn/ir2.py"
    - "tests/test_e2_ir2.py"
  tests_added: []
  tests_passing:
    - "No runtime test was run; this is an architecture proposal."
    - "Repository synchronization and baseline verification passed."
    - "git diff --check passed."
  tests_failed: []
  tests_not_run:
    - "All tests and runtime experiments."
    - "All GPU, FPGA, FPAA, ModelSim, calibration and hardware-equivalence checks."
  assumptions:
    - "The published main SHA is the baseline authority."
    - "The repository's ACP policy requiring project-owner acceptance governs this proposal."
  unresolved:
    - "Project owner must accept, request specific revisions, or reject ACP-0006."
    - "No implementation readiness/authorization exists until ACP-0006 is accepted and a separate bounded Luna contract is authorized."
  recommended_next_agent:
    - "Project owner: choose accept/revise/reject for ACP-0006."
    - "Luna-0: after explicit acceptance only, identify the next unused Luna role and issue a bounded integration contract."
```

## Synchronization and decision authority

**OBSERVED:** `git fetch origin` completed. Branch `main` was clean;
`HEAD == origin/main == 813186f87e7074415b550cf051ad2435c028d52a`, subject
`Reconcile Luna-21 status and integration readiness`. No newer governance
commit existed at review start.

The current ACP policy says the project owner or an explicitly delegated
architecture decision-maker records acceptance; an agent recommendation
alone does not amend the architecture. The governing proposals identify the
project owner as decision owner. No explicit project-owner acceptance of this
integration contract is present in the reviewed repository state. Therefore
this is a complete proposed decision, not an accepted/promoted canonical
change.

## Architecture evidence and classification

**OBSERVED:** The ordinary experiment network is scalar/continuous: it
constructs `TPCNNeuron`, routes each returned activation and exposes scalar
activation-derived values to prediction, eligibility, energy and readout.
It makes a fresh queue for each input point and drains queued future work.

**OBSERVED:** The E2 runtime changes bounded local state on external/internal
events and may return no `ExcursionEmission` or one canonical output. E2
pending work is queued in logical time; an emission carries unique event
identity, timestamp, signed payload, episode and lineage. Model-B routes
numeric excursion payloads through finite edge delays and preserves emission
identity and lineage. No integrated experiment-network consumer exists.

**OBSERVED:** ACP-0004 specifies the excursion output and post-migration
`a_i := p_exc`, but not the network scheduler, predictor/readout/credit
adapter or model selector. ACP-0005 excludes complete queue, predictor,
eligibility/reward and classifier state. Acceptance criteria require causal
sequential classification, explicit prediction errors, delayed credit,
declared settling and reset behavior.

**DECISION:** Choice C is recommended and ACP-0006 is created **Under
review**. This is a network-level composition boundary, not an E1/E2 neuron
amendment and not a routine implementation-only task. A01-A15 text remains
unchanged until owner acceptance and subsequent promotion.

## Proposed decisions for all 17 boundaries

The normative candidate rules are fully specified in
`workflow/docs/architecture_proposals/ACP-0006.md`. Summary:

1. **Production model:** network-wide construction-selected
   `EXCURSION_V1`, backed by the E2-capable runtime; no mixed models.
2. **Causal event loop:** one incremental bounded character queue; drain only
   timestamps `< t` before admitting the next external time `t`, then admit
   same-time available inputs before draining through `t`.
3. **Internal event/path ownership:** bounded scheduler sidecar carries causal
   root IDs into internal work; each distinct emission begins a fresh bounded
   route path while retaining causal roots and neuron lineage.
4. **Outgoing routing:** no emission means no route; one emission routes
   exactly its signed payload under unchanged Model-B.
5. **Prediction creation:** only configured predictor-source emissions create
   predictions; `p_exc` predicts the next scalar input payload on the
   configured causal input port.
6. **Prediction error:** later actual input creates the existing
   `PredictionError`; error metadata is dispatched locally and propagated
   over finite existing edges without numeric Model-B transfer.
7. **Eligibility:** only emissions create traces; magnitude is `abs(p_exc)`,
   trace ID is namespaced excursion identity and prediction ID is linked when
   present. Existing delayed credit is retained; one outer reward targets the
   first readout-excursion trace, otherwise it is explicitly unmatched.
8. **Readout:** classifier consumes each actual configured readout
   `ExcursionEmission`; silence produces no event.
9. **External learning:** existing outer prototype/readout learner adapts to
   bounded signed-sum/count excursion statistics; labels remain post-readout
   only.
10. **Settling:** after the final point, process through a declared finite
    logical horizon under a finite event budget; partial results are marked
    incomplete and pending work is reported.
11. **Reset:** destroy queue/sidecar, reset neuron-local episode state and
    clear character-local predictor, eligibility, error-delivery and
    classifier state; preserve E2 identity high-water marks.
12. **Queue lifetime:** one queue per character; never per point or across
    characters.
13. **IR-2:** integrated startup accepts only uniform, quiescent clean
    `EXCURSION_V1` neuron state with no in-flight/shared scheduler or
    predictor/ledger/readout state; full live resume needs a future format.
14. **Legacy:** `TANH_LEGACY` remains an explicit uniform compatibility/replay
    control, with no implicit fallback.
15. **E1/E2 role:** E2-capable runtime is the sole proposed production
    excursion path; E1 remains reference/control.
16. **Energy:** event-processing, excursion amplitude, Model-B edge work and
    prediction-error cost are separated in bounded activity-cost-proxy units;
    no calibrated energy claim.
17. **Structural plasticity:** off; fixed topology; no N3 or new structural
    semantics.

## Required future implementation controls and tests

Controls: explicit `TANH_LEGACY` versus `EXCURSION_V1`, identical external
stream/topology/budgets/timestamps/label boundary/reset/readout; numeric
equality is not required. Tests include silence/no-route, emission-only
routing, same-time external-before-internal ordering, bounded queue,
integrated delayed prediction error and credit, event-based readout, finite
settling, stale-work reset, identity high-water persistence, quiescent IR-2
startup, explicit legacy selection, no label leak, deterministic replay and
no global timestep.

Mandatory adversarial fixture:

```text
external input @ t0 schedules E2 internal work @ t2
external input @ t1, with t0 < t1 < t2
```

The observed order must be `t0`, `t1`, `t2`; the `t1` input must be able to
alter/cancel/reschedule the due E2 work before `t2`.

## Validation and limitations

| Procedure | Result |
|---|---|
| Fetch, branch, clean-state and revision verification | PASS; baseline exactly matched the requested published SHA |
| Source/governance inspection | Completed; files enumerated in YAML |
| Tests / runtime experiments | Not run; no production behavior changed |
| Hardware/backend checks | Not run; unauthorized and outside scope |
| `git diff --check` | PASS |

## Owner choices and authorization boundary

The only remaining project-owner choices are:

1. Accept ACP-0006 as written.
2. Request specific revisions and return it to Luna-0.
3. Reject ACP-0006.

No numbered successor Luna contract has been created or authorized. After
owner acceptance only, Luna-0 must check the then-current Luna numbering,
create a bounded first-integration contract, and return to independent review
after implementation. No integration readiness is claimed here.
