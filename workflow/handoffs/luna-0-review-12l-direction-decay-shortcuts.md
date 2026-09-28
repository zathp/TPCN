# Luna-0 Review Handoff - Luna-12L and Direction/Decay Shortcut Study

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  luna_identifier: "Luna-0 review after Luna-12L"
  descriptive_name: "Temporal direction and intrinsic-decay-gated shortcut review"
  task_id: "luna-0-review-12l-direction-decay-shortcuts"
  component: "review of Luna-12H through corrected Luna-12L structural evidence"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "3122c7dbae2589c1c78fe6169d394f525c212ec1"
  result_revision: "uncommitted"
  dependencies:
    - "Luna-12H completion handoff"
    - "Luna-12I completion handoff"
    - "Luna-12J PASS WITH FOLLOW-UP handoff"
    - "Luna-12K execution handoff and Luna-0 review"
    - "corrected Luna-12L completion handoff"
  owner: "Luna-0 Architecture Guardian"
  classification: ["ARCHITECTURE-REVIEW", "EVIDENCE-REVIEW"]
  hypothesis: "Locally observed event direction interpreted through the source neuron's intrinsic decay may increase genuine causal compression or useful route allocation under equal opportunity."
  counter_hypothesis: "Direction and decay-relative gating do not improve shortcut yield or useful routed computation, or any structural gain is offset by prediction, energy, traffic or lifecycle cost."
  interfaces_relied_on:
    - "TPCNNeuron local elapsed-time exponential decay"
    - "BoundedTopology finite positive-delay routing"
    - "TemporalAssociationPolicy and CandidateEvidence"
    - "StructuralPlasticityController admission, rejection and pruning API"
    - "Luna-12K causal path fixture and corrected Luna-12L provenance"
  authorized_scope:
    - "Review completed evidence and define a bounded next experimental question."
    - "Specify instrumentation and controls; do not implement the mechanism."
  unauthorized_scope:
    - "Do not create or dispatch a successor Luna."
    - "Do not amend A14, mandate edge direction, mandate a decay threshold, alter pruning/decay semantics, or add protected edges."
    - "Do not introduce genetic hyperparameters, a local micro-NN, global topology inputs, or a new topology."
  controls:
    - "current temporal-association direction"
    - "reversed candidate direction"
    - "decay-gated current direction"
    - "decay-gated reversed direction"
    - "fixed topology as a no-growth reference"
    - "random legal growth only if candidate exposure and mutation effort remain equal"
  measurements:
    - "candidate exposure, accepted mutations, shortcut yield, hop and cumulative-delay change"
    - "arrival timing, routed events, comparable useful work and causal intervention effect"
    - "fan-in/out pressure, competing-route traffic, prediction/error, proxy energy and utility"
    - "per-edge utilization and lifecycle timestamps, strength/utility trajectories and rejection reasons"
  information_boundary_check:
    - "Structural decisions may consume only local timestamps, elapsed time, local decay parameters/residual state, local activity and local edge/eligibility/usage state."
    - "Global shortest paths, labels, task accuracy, whole-network energy, centrality and global topology remain offline evaluation only."
  hardware_mapping:
    - "Direction, finite counters, local elapsed time and bounded residual/usage state are hardware-realizable reference quantities."
    - "No hardware equivalence or physical energy calibration is claimed."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "Event-driven execution, intrinsic local time, finite unequal-delay propagation, bounded topology/dynamics, predictive/error events, local accounting, delayed credit and hardware independence."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-review-12l-direction-decay-shortcuts.md"
  tests_added: []
  tests_passing:
    - "Evidence and source review completed against current repository."
  tests_failed: []
  tests_not_run:
    - "No new mechanism or next experiment executed."
    - "Hardware, real-data and physical-energy validation remain not applicable/unauthorized."
  assumptions:
    - "The corrected Luna-12L handoff and artifacts are current worktree evidence based on HEAD 3122c7d; their uncommitted status is retained explicitly."
  unresolved:
    - "Whether edge orientation or decay-relative gating causes useful causal compression outside the small 12K fixture."
    - "Whether current edge lifecycle loss prevents fair measurement of newly useful routes."
  recommended_next_agent:
    - "No successor is ready to be created; owner authorization is required after this review."
```

## Baseline and evidence reviewed

**Baseline:** current repository HEAD is `3122c7dbae2589c1c78fe6169d394f525c212ec1`.
The corrected Luna-12L implementation, artifacts and handoff are uncommitted
worktree evidence and are not silently treated as committed history.

Reviewed sources and evidence:

- Luna-12H: intrinsic bounded exponential decay, persistent local state,
  unequal cumulative delays, timestamp-preserving fan-in and bounded recurrence.
- Luna-12I: bounded source-local temporal association and explicit rejection;
  useful task/path benefit remained untested at policy completion.
- Luna-12J: `PASS WITH FOLLOW-UP`; temporal growth formed useful convergence
  in the small fixture, but candidate exposure was imperfect and no long path
  existed.
- Luna-12K: `PASS WITH FOLLOW-UP`; equal exposure and actual capacity pressure
  produced a real temporal shortcut in 5/5 retained seeds, changing delay from
  `3.0` to `0.75` and changing routed computation under removal replay.
- Corrected Luna-12L: `NOT SUPPORTED`; the pre-coupling artifact is invalid and
  preserved separately. Corrected four-class accuracy/order evidence did not
  support temporal classification benefit, reference-scale structural policy
  distinction did not survive expanded scale, and temporal proxy energy was
  higher than fixed. This does not refute shortcut formation itself.

## Conclusions retained from 12K and corrected 12L

**OBSERVED:** 12K established genuine shortcut formation, finite-delay path
reduction, competing-capacity pressure and a causal routed-computation change.
It did not establish that the current direction is uniquely correct, that the
old route becomes redundant, or that the result improves energy or prediction.

**OBSERVED:** Corrected 12L established valid policy/scale provenance and
retained a reference-scale causal topology effect. It did not establish
four-class classification benefit, temporal-order readout benefit, expanded-
scale policy advantage, or an acceptable cost tradeoff. Its zero exposed
prediction loss is an instrumentation limitation, not perfect prediction.

**INFERRED:** The corrected 12L negative result bears directly on scaling and
readout/order representation, but is not a failure of shortcut formation.
The remaining structural question is whether temporal edge orientation and
decay-relative timing can distinguish a genuinely compressive route from an
equal-depth duplicate.

## Proposed experimental question

Tentative title, with no Luna number assigned:

**Temporal Direction and Intrinsic-Decay-Gated Shortcut Verification**

Question: under equal candidate exposure, mutation effort, finite resources,
delays and workload, does locally legal temporal direction and/or a gate
relative to the neuron's own decay law increase the fraction of accepted
mutations that create useful causal compression?

The falsifiable primary hypothesis is:

> Locally available event timing, interpreted through intrinsic decay and
> connection direction, can increase shortcut yield or useful route allocation
> without global topology knowledge.

For the current exponential reference, a candidate may use a local residual
quantity equivalent to `D = exp(-lambda * dt)`. Any threshold or function is
experimental and relative to the neuron's declared dynamics; no fixed global
`dt` threshold is authorized.

## Controls and intervention

Use one bounded competing-path fixture derived from 12K, with the long route
functional before growth and multiple legal competitors. Compare the four
factorial policy variants: current direction, reversed direction, decay-gated
current direction and decay-gated reversed direction. Retain fixed topology as
the no-growth reference. Retain random legal growth only if it receives the
same candidate set, exposure, attempts and resource budget; otherwise it is a
separate diagnostic, not a matched claim.

For each accepted candidate, replay the same input before growth, after growth,
and after removal of the candidate. The intervention must test routed events,
arrival timestamps, downstream state/output and prediction/error, not merely
graph distance. Include equal-time and unequal-delay cases so hop count cannot
stand in for causal delay.

## Shortcut definition and gate measurements

An accepted mutation counts as a **candidate shortcut** only when a matched
before/after replay shows one or more of:

- reduced hop count between causally related activity;
- reduced cumulative propagation delay;
- earlier meaningful downstream arrival;
- reduced routed work for a comparable outcome; or
- improved useful computation under equal declared resources.

The primary ratio is:

`shortcut_yield = accepted mutations with measurable causal-path reduction / accepted structural mutations`.

Report the numerator components separately. Also report accepted edges,
candidate exposure, hop/delay deltas, arrival time, routed-event count,
fan-in/out pressure, utilization, prediction loss/error activity, proxy energy
and units, utility definition, task effect if a valid task is retained, and
all seeds including failures and rejected admissions.

## Instrumentation review

Already exposed in the current reference path:

- local neuron decay rate and elapsed-time evolution;
- edge endpoints, positive propagation delay and routing cost field;
- candidate score/evidence, accepted growth, rejection cause, pruning result;
- topology snapshots, active-edge set in the 12K replay, event paths,
  hop/delay observations, arrivals, routed-event count and causal removal;
- aggregate fan-in/out, candidate exposure, mutations, churn, prediction
  error, proxy energy and utility.

Missing before any edge-lifecycle or protection experiment:

- per-edge traffic count and traffic timestamps, including shortcut versus
  competing-route use;
- old-path utilization before and after shortcut formation;
- new-edge first-use, last-use and utilization-over-time;
- edge birth/growth timestamp and pruning/replacement timestamp;
- persistent edge strength, utility, eligibility or usage state trajectories;
- per-edge prediction contribution and resource contribution where measurable;
- explicit pruning/rejection reason tied to the candidate and route;
- evidence that the old path remains useful, becomes redundant, serves another
  temporal context, or disappears before comparison.

The current `Edge` has no lifecycle state, and `temporal_analysis` explicitly
reports per-edge use as unavailable because replay snapshots preserve topology
existence rather than edge event identity. Do not change pruning or decay
semantics merely to obtain these measurements.

## Edge lifecycle and back-burner hypotheses

First determine whether the existing controller can retain a new edge long
enough for measurement. Do not add a protection period now. Record whether
weakening/pruning can remove an edge before first use or before a competing
route comparison.

Back-burner hypothesis only:

> A newly formed edge that carries useful causal traffic may need a bounded,
> local, deterministic or explicitly seeded evaluation interval before ordinary
> weakening or pruning decides whether it replaces, coexists with, or loses to
> the older route.

Any later test must be bounded, resource-aware, hardware-realizable and must
not create immortal edges.

Separate future research note: a bounded local inherited hyperparameter
description might eventually express decay, growth sensitivity, association
threshold, energy weighting, prediction dynamics or pruning sensitivity.
This is not part of the next experiment. No global hyperparameter database,
runtime trainer input, hyperparameter evolution, or local micro-NN is
authorized. Any future version must preserve A07 locality, A04 boundedness and
A15 realizability.

## Local versus offline information

Legal structural inputs: local event timestamps, local elapsed time, the
neuron's own decay parameter or residual state, locally observed activity,
local edge state, local usage and local eligibility.

Offline evaluation only: global shortest paths, global topology centrality,
whole-network energy, global traffic summaries, class labels, task accuracy,
and any future-event or evaluation outcome. These may score the experiment but
must not enter candidate evidence, routing, predictor state, structural
decisions, eligibility or energy computation.

## Recommended gate and authorization

- **PASS:** direction/decay-aware policy improves genuine shortcut yield or
  useful causal compression under equal opportunity, causal intervention
  confirms a routed computation change, and locality is clean.
- **PASS WITH FOLLOW-UP:** compression improves but lifecycle, energy or
  prediction/traffic tradeoffs remain unresolved.
- **NOT SUPPORTED:** controlled variants do not improve compression or useful
  computation.
- **INCONCLUSIVE:** valid execution cannot distinguish direction and decay
  effects.
- **BLOCKED:** missing instrumentation, provenance, locality or implementation
  defects prevent a trustworthy comparison.

This review recommends **instrumentation-first planning**, followed by the
tentative four-variant experiment only after the missing route/lifecycle
records are available. No successor Luna is ready to be created or dispatched
from this review. No A14 change, ACP, protected-edge rule, permanent decay
threshold, reversed-direction mandate or hyperparameter-expression mechanism
is authorized.

## Validation record

| Procedure | Revision / environment | Result |
|---|---|---|
| Required architecture/workflow/evidence review | HEAD `3122c7d`, Windows worktree | completed |
| Current source instrumentation audit | HEAD plus uncommitted 12L worktree | missing per-edge traffic and lifecycle state confirmed |
| New experiment or mechanism | not run | not authorized by this review |
| Hardware, real-data and physical-energy validation | not applicable/unauthorized | not run |