---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "ACP-0008 task-independent calibration decision"
  task_id: "luna-0-acp0008-calibration-decision-20261005"
  component: "Governance decision for bounded slow-integration calibration"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "0c0e475a89361713d1f462c5500b4d49bd860b9d"
  result_revision: "the Git commit that publishes this handoff"
  dependencies: []
  owner: "Project owner"
  classification: ["GOVERNANCE", "CALIBRATION AUTHORIZATION", "NOT EXECUTED"]
  hypothesis: "A finite task-independent decay-rate set can be tested against explicit normalized near/far temporal requirements before a frozen relay-stream characterization."
  counter_hypothesis: "No candidate satisfies all frozen fixtures, or the selected calibration generates no relay emission on the frozen Phase-B stream."
  interfaces_relied_on: ["ACP-0008 IntegrationConfig", "existing EXCURSION_V1 event queue and BoundedTopology public path"]
  label_information_boundary: ["Phase A uses synthetic normalized values only.", "Phase B reads only timestamps and points from the existing unlabeled stimulus generator.", "No label, class identity, task metric, reward, or readout may select or change calibration."]
  timing_assumptions: ["Local time only; no global neural timestep.", "Near gap 12.9 is a prior independently observed local routed-arrival reference.", "Far gap is fixed at 4x near gap.", "All emissions use the unchanged positive-delay canonical path."]
  reset_boundaries: ["Fresh source and relay for every Phase-A fixture/candidate.", "Fresh per-character neurons for each Phase-B arm; topology remains frozen."]
  resource_bounds: ["Phase A event queue and processed-event limits fixed at 64 per fixture.", "Phase B retains Luna-40 queue=128, event budget=1024, prediction capacity=8, eligibility capacity=1024, and all frozen topology bounds; no capacity increases."]
  authorized_scope: ["Create the bounded Luna-41 execution contract.", "Calibrate only decay_rate_z from the four frozen values using Phase A.", "If Phase A passes, freeze the selected configuration and characterize the existing unlabeled fixed-w=1 relay stream in Phase B."]
  unauthorized_scope: ["Do not execute Luna-41 in this governance pass.", "No threshold, input-gain, fast-decay, theta_Z, z_max, topology, ACP-0007, or production-code changes.", "No task fitting, efficacy, accuracy, energy-benefit, promotion, hardware-equivalence, or biological claim."]
  controls: ["Unchanged default decay_rate_z=0.1.", "Integration-disabled control.", "Isolated input, near pair, far triple, and negative mirror."]
  measurements: ["Per-event z recurrence and bound.", "Direct vs integration-mediated canonical emissions.", "Routed payload/timestamp/event identity.", "Deterministic replay digest and resource high-water marks."]
  information_boundary_check: ["No label or downstream evaluation signal enters any neural input, Phase-A candidate selection, or Phase-B configuration."]
  hardware_mapping: ["No hardware implementation/equivalence test authorized; abstract resource implications remain unmeasured."]
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A14", "A15 (no change to these invariants)"]
  preserves: ["Event-driven local elapsed-time integration and finite propagation.", "ACP-0008 remains experimental, opt-in, and unpromoted.", "All Luna-33 through Luna-40 and ACP-0007 verdicts."]
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-41.agent.md"
    - "workflow/handoffs/luna-0-acp0008-calibration-decision-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "Luna-41 Phase A and Phase B: explicitly not executed."
    - "No automated tests or full suite: not run; this pass changes governance documents only."
    - "Analytic fixture predictions are design calculations, not runtime validation."
    - "Hardware equivalence and task efficacy: unauthorized."
  assumptions: ["The existing public event/neuron/topology interfaces can express the declared deterministic route; Luna-41 must block rather than extend them if they cannot.", "The accepted default source amplitude rule maps the declared source peak to canonical amplitude atanh(0.4)."]
  unresolved: ["Luna-41 runtime evidence and independent review remain outstanding.", "No conclusion is made that the calibrated relay emits on Phase B."]
  recommended_next_agent: ["Luna-41 bounded implementation and experiment", "Luna-0 independent review after completed evidence"]
---

# Luna-0 decision — bounded ACP-0008 calibration

## Outcome and decision

**Principled bounded calibration is sufficiently specified. Luna-41 is
AUTHORIZED / NOT EXECUTED.** This governance pass authorizes the finite,
task-independent experiment described in
`.github/agents/luna-41.agent.md`; it does not execute it, establish any
measured result, change production behavior, or promote ACP-0008.

The decision follows the owner-directed calibration request after the
independent Luna-40 result. Luna-40 remains **NOT SUPPORTED IN THIS SETUP**:
no relay emission or ACP-0007 candidate/admission formed. This is neither a
production defect nor evidence that changing ACP-0008 parameters will make
the Phase-B relay emit. Luna-39's fixed-`w=1` zero-emission result and its
`w=2` contextual sensitivity are not calibration targets. The newly
authorized experiment tests whether an explicit local-time integration
requirement can be represented by a bounded, normalized fixture before
checking a frozen `w=1` stream.

## Calibration basis

Change only `decay_rate_z` over the finite set
`{0.1, 0.05, 0.025, 0.0125}`; the first value is the existing default.
Keep `theta_E=1.0`, `theta_Z=1.0`, `input_gain=1.0`, `z_max=4.0`, and fast
decay `1.0`. Keep ACP-0007 disabled. These values are configuration
candidates under accepted ACP-0008, not a change to its equations or
architecture.

The normalized routed amplitude `0.4` is a previously used ACP-0008 unit
fixture, not extracted from task labels or Phase-B outcomes. It remains
subthreshold in the fast state and requires at least three coincident
contributions to cross `theta_Z=1`. The near interval `12.9` is a local
routed-arrival gap recorded in the independently reviewed Luna-37/39
mechanism evidence; the far interval is predeclared as four times that
value. The Phase-A criteria are explicit: isolated and two-near inputs do
not discharge; three near inputs produce exactly one integration-mediated
relay emission; three far inputs do not; the negative mirror preserves sign;
the disabled control has no emission; all traces follow the ACP-0008
recurrence, remain bounded, return below `1e-4` after at least ten slow
time-constants, and replay identically.

Analytic calculations predict near-pair and near-triple pre-discharge
magnitudes of `(0.510108, 0.540418)`, `(0.609865, 0.719973)`,
`(0.689735, 0.899599)`, and `(0.740432, 1.030166)` in candidate order;
far-triple values remain below threshold for all candidates. Thus the
equations predict that only `decay_rate_z=0.0125` will pass; that prediction
is not a result. The actual Phase-A production-path evidence is required.
Selection, if any, uses the predeclared fastest-decay-passing rule. No
candidate-set expansion or fixture changes are authorized.

Only after Phase A passes and its configuration/results are hashed and
frozen may Luna-41 run the paired Phase-B relay-stream characterization.
Phase B uses identical unlabeled points, ordering, seeds, fixed `w=1`
topology, and runtime bounds across calibrated, default, and disabled
integration arms. It measures relay state/emissions and actual onward route
effects only. No task metric can alter the selected configuration; zero
relay emissions is an explicitly valid negative result.

## Architecture and historical boundaries

No Architecture Contract amendment or new ACP is needed: Luna-41 selects
among values of the already accepted optional ACP-0008 integration
configuration. ACP-0008 remains **EXPERIMENTAL, OPT-IN, UNPROMOTED**. No
claim is made that the candidate values are generally optimal, biologically
meaningful, hardware-equivalent, or useful for a task. ACP-0007 evidence,
growth, pruning, edge parameters, thresholds, fast dynamics, reward,
eligibility, prediction-error routing, and bounded topology are unchanged.

Historical results remain unchanged: Luna-40's no-candidate/no-admission
verdict; Luna-39's `w=1`/`w=2` mechanism result; Luna-38's unit mechanism
result; earlier Luna-33/34/37 findings; and ACP-0007's status. Any
contradiction, missing public interface, resource overflow, or failed replay
must be returned as blocked/failed evidence, not repaired through expanded
scope.

## Files and validation

This pass changes only the Luna-41 contract, this governance handoff, the
Luna workflow, and the architecture changelog. The baseline revision is
`0c0e475a89361713d1f462c5500b4d49bd860b9d`. No runner, tests, artifacts,
production files, architecture proposal, or architecture-contract text are
created or changed. Governance document checks and `git diff --check` are
to be recorded in the completion report. The full suite is not required for
this documentation-only authorization and will not be represented as rerun.

## Next assignment

Luna-41 owns only the runner, focused tests, experiment artifacts, and its
completion handoff. Run it only from the published authorization revision,
only with the frozen design, and return the complete evidence to Luna-0 for
independent review. **No execution occurs in this Luna-0 pass.**
