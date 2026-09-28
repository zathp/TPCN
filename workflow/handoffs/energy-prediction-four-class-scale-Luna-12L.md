# Luna-12L Execution Handoff

This is the completed execution record. It returns evidence to Luna-0 and
does not promote A14 or authorize any later milestone.

```yaml
tpcn_handoff:
  agent: Luna-12L Energy/Prediction Tradeoff and Four-Class Temporal Scale Verification
  luna_identifier: "Luna-12L"
  descriptive_name: "Energy/Prediction Tradeoff and Four-Class Temporal Scale Verification"
  task_id: "energy-prediction-four-class-temporal-scale-luna-12l"
  component: "four-class temporal spiral benchmark with bounded structural-growth controls and joint resource/prediction analysis"
  status: "complete-corrective-rerun"
  contract_version: "1.1"
  branch: "main"
  base_revision: "3122c7dbae2589c1c78fe6169d394f525c212ec1"
  result_revision: "uncommitted"
  dependencies:
    - "Luna-12K PASS WITH FOLLOW-UP review"
    - "Luna-12J efficacy evidence"
    - "Luna-12I temporal-association policy"
    - "Luna-12H intrinsic temporal and unequal-delay semantics"
    - "Luna-12E persistent routed topology"
    - "Luna-12G spiral benchmark and external readout"
    - "Luna-4 bounded topology and Luna-10 structural plasticity"
  owner: "Luna-12L execution owner"
  classification: ["EXPERIMENT", "VERIFICATION"]
  hypothesis: "Temporal-associative growth retains useful four-class temporal classification and causal path allocation at two bounded scales, but must be judged jointly against prediction quality and proxy/resource cost."
  counter_hypothesis: "Four-class scaling removes the structural benefit, the benefit is a static shortcut, or energy/prediction costs become unfavorable without a compensating measured benefit."
  interfaces_relied_on:
    - "Accepted Luna-12G spiral generator and external readout"
    - "Luna-12E actual event-routing topology"
    - "Luna-12I CandidateEvidence temporal-association policy"
    - "Pre-12I structural-growth policy and random legal control"
    - "EventQueue, canonical timestamps and finite positive delays"
    - "Existing prediction/error and local proxy-energy instrumentation"
  label_information_boundary:
    - "Labels are external readout/evaluation metadata only and cannot enter events, payloads, identifiers, predictor state, routing, structural evidence, eligibility or energy computation."
    - "A sequence-boundary/check event may be reused only if identical and class-neutral across all four classes and carries no future outcome."
  timing_assumptions:
    - "Use canonical event timestamps, positive finite edge delays and deterministic equal-time ordering."
    - "At least one declared order intervention preserves the intended event multiset or spatial samples while changing temporal order."
  reset_boundaries:
    - "Reset event/local temporal state, predictor state, queue and per-example history at declared sequence boundaries; topology/controller reset policy is identical across policies."
  resource_bounds:
    - "Reference scale: seven-node routed fixture, edge/routing capacity 6, fan-in/out 2, candidate/history capacity 8, queue/event capacity 16, three growth attempts."
    - "Expanded scale: 12-node routed fixture, edge/routing capacity 10, fan-in/out 3, candidate/history capacity 12, queue/event capacity 24, five growth attempts."
    - "All candidates, histories, edges, paths, queues, lineages, mutations and analysis buffers are finite."
  authorized_scope:
    - "Add or extend the four-class synthetic benchmark, bounded scale configurations, tradeoff metrics, focused tests, machine-readable artifacts and analysis."
    - "Make the smallest measurement exposure fix only when a demonstrated defect prevents a legal experiment."
    - "Retain fixed, pre-12I, random, temporal-associative and reversed/shuffled/timing-destroyed controls with seeds 0-4."
  unauthorized_scope:
    - "Do not modify ARCHITECTURE_CONTRACT.md or A14, promote temporal association, create a permanent energy/prediction objective or authorize a successor."
    - "Do not redesign canonical neuron semantics, predictive coding, the 12I policy, energy architecture, topology authority or readout."
    - "Do not inject class markers, labels, future observations or global metrics into canonical computation."
    - "Do not claim real-dataset, handwriting, GPU/FPGA/ModelSim or hardware acceptance."
  controls:
    - "Fixed topology"
    - "Pre-12I structural growth"
    - "Random legal structural growth"
    - "Luna-12I temporal-associative structural growth"
    - "Reversed, shuffled or timing-destroyed temporal order"
    - "Optional oracle-like selector only as a non-architectural diagnostic"
  measurements:
    - "Overall and per-class four-class accuracy, four-by-four confusion, class separation and external readout evidence"
    - "Left/right and inward/outward confusion, especially same-handed outward/inward pairs"
    - "Prediction loss, prediction-error activity/timing, events, routed events and neuron activations"
    - "Proxy/resource energy with units, calibration status and comparative ratios"
    - "Candidate exposure/consideration/selection, attempts, accepted/rejected growth, rejection reasons, pruning/replacement, churn and stabilization"
    - "Fan-in/out, saturation, convergent motifs, edge utilization, path hops, cumulative delays and arrival timestamps"
    - "Class-specific edge utilization, capacity conflict and shortcut survival/removal intervention"
    - "Same-seed benchmark, structural-decision and replay determinism"
  information_boundary_check:
    - "Direct tests must perturb labels and order/future information to show that canonical traces and structural decisions remain label-free and causal."
  hardware_mapping:
    - "Finite counters, bounded histories, positive-delay routing and explicit resource proxies remain software-reference compatible with eventual FPGA/FPAA/hybrid mapping; no hardware equivalence is claimed."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "Event-driven execution, local time, finite propagation, bounded topology/dynamics, predictive/error events, local energy semantics, delayed credit, label isolation and hardware-neutral reference behavior."
  architecture_change: false
  gate: "NOT SUPPORTED (corrected evidence; prior result invalid)"
  proposal: null
  files_changed:
    - "tpcn/experiments.py"
    - "tpcn/spiral_benchmark.py"
    - "tpcn/temporal_capacity.py"
    - "tpcn/temporal_scale.py"
    - "tpcn/__init__.py"
    - "run_temporal_scale.py"
    - "tests/test_spiral_benchmark.py"
    - "tests/test_luna12l_temporal_scale.py"
    - "artifacts/temporal-scale-12l/config.json"
    - "artifacts/temporal-scale-12l/results.json"
    - "artifacts/temporal-scale-12l-invalid-pre-coupling/ (preserved invalid predecessor)"
  tests_added:
    - "tests/test_luna12l_temporal_scale.py: 12 focused coupling/provenance tests"
  tests_passing:
    - "Focused corrected 12L slice: 12 passed"
    - "Affected prior-Luna, routing, spiral/readout and structural slice: 72 passed"
    - "Full pytest: 194 passed, 1 skipped"
    - "compileall: passed"
    - "Workspace diagnostics for touched files: no errors"
    - "git diff --check: passed; existing LF/CRLF warning only"
  tests_failed: []
  tests_not_run:
    - "Real dataset, hardware equivalence, GPU/FPGA/ModelSim and A14 promotion; excluded or unauthorized."
  assumptions:
    - "The current Luna-0 12K review is authoritative evidence for creating this bounded follow-up."
    - "Existing spiral, readout, routing, prediction and proxy-energy interfaces can expose the required measurements without changing their semantics."
  unresolved:
    - "Whether four-class traversal-direction information is represented by the current legal event path."
    - "Whether the 12K energy/prediction cost is useful routed activity, timing alignment, objective separation or an unfavorable degradation."
    - "Whether the benefit survives the expanded bounded scale and creates class-resource conflict."
  recommended_next_agent:
    - "Luna-12L execution owner after a separate explicit assignment."
    - "Luna-0 Architecture Guardian for evidence review after execution."
    - "No successor Luna is authorized by this contract."
```

## Dispatch provenance

**OBSERVED:** Current repository HEAD is `3122c7dbae2589c1c78fe6169d394f525c212ec1`.
The namespace scan found no existing Luna-12L agent, specification or handoff.

**OBSERVED:** The current Luna-0 review assigns Luna-12K `PASS WITH FOLLOW-UP`.
The reviewed evidence records temporal shortcut selection in `5/5` seeds,
control selection in `0/5`, a three-hop / `3.0` path, a one-hop / `0.75`
shortcut, and removal restoration of the routed trace and downstream state.

**OBSERVED:** The reviewed tradeoff records temporal proxy energy `9.850877`
versus adaptive-control `9.274247`, and temporal prediction loss `1.284030`
versus adaptive-control `1.025229`.

**INFERRED:** A two-scale, four-class experiment is a bounded response to the
specific unresolved 12K energy/prediction and scale questions. It is not
architecture-promotion evidence.

**HYPOTHESIZED:** The temporal policy may retain useful path allocation while
its additional cost is explainable or bounded. This must be tested and may be
rejected.

## Planned validation record

| Command or procedure | Revision / environment / seed | Expected status at creation | Evidence |
|---|---|---|---|
| Namespace and baseline audit | Windows, `3122c7d`, current worktree | passed for creation | current repository scan |
| Luna-12K artifact and review audit | `3122c7d`, seeds 0-4 | passed for creation | `artifacts/temporal-capacity-12k/results.json`, current 12K review |
| Focused 12L tests and runner | explicit execution assignment required | not run | future 12L artifacts |
| 12K/12J/12I/12H/12E and affected regression tests | explicit execution assignment required | not run | future 12L handoff |
| Full pytest, compileall, diagnostics, git diff --check | explicit execution assignment required | not run | future 12L handoff |

## Required completion evidence

The execution owner must retain every seed and unfavorable result, publish the
machine-readable per-scale/per-policy artifact, distinguish OBSERVED,
INFERRED and HYPOTHESIZED statements, classify all checks, and return the
completed handoff to Luna-0. A positive result does not change A14 or authorize
any later Luna.

## Reproduction and rollback

Creation provenance is the current main revision above. Execution must record
its result revision and exact commands before changing implementation files.
Restore only the execution-owned files to the recorded base revision if the
separately assigned experiment is rolled back; preserve unrelated worktree
changes and this creation record unless the owner explicitly requests its
removal.

## Next assignment

Assign the Luna-12L execution role explicitly with the listed inputs and owned
files. After execution, Luna-0 reviews the evidence and decides whether the
result is ready, blocked or requires a bounded response. No later Luna is
created or authorized by this contract.

## Corrective execution evidence

Luna-0 found the original result **BLOCKED**: the runner varied structural
fixtures while every classifier row came from the fixed topology, and several
metrics were taken from a separate structural replay. The original artifact is
preserved at `artifacts/temporal-scale-12l-invalid-pre-coupling` and is
superseded, not evidence.

The repair carries named policy and scale through `ExperimentConfig`, invokes
the requested policy in the classifier, configures the requested node count,
checks requested/executed provenance, and takes classifier prediction,
energy, event and activation metrics from that same run. Structural edge,
path, mutation and intervention metrics remain explicitly sourced from the
matching structural condition. Deliberate provenance mismatch is tested and
raises.

The corrected command was:

```text
python run_temporal_scale.py --output artifacts/temporal-scale-12l --seeds 0 1 2 3 4
```

The corrected artifact contains 50 records across both scales, five policies
and seeds 0 through 4. Its config records the corrective status and superseded
artifact. The four external labels remain
`spiral-left-outward`, `spiral-right-outward`, `spiral-left-inward` and
`spiral-right-inward`; labels remain outside canonical computation.

**OBSERVED:** Corrected mean classifier accuracy was `0.300` for reference
fixed, baseline, temporal and reversed, and `0.250` for random. Expanded mean
accuracy was `0.225` for every policy. Reversed-order mean accuracy matched
the corresponding selected condition in this run, so temporal order did not
produce a measurable readout effect.

**OBSERVED:** Reference temporal structural growth selected a shortcut in
`5/5` seeds, while fixed, baseline, random and reversed selected none. The
learned-edge intervention changed routed computation in the retained causal
cases. Expanded temporal selected a shortcut in `5/5`, but baseline and
reversed also selected one in `5/5`, so the reference policy distinction did
not survive the larger scale.

**OBSERVED:** Corrected classifier proxy energy means were `48.103` fixed,
`51.467` temporal at reference and `48.923` fixed, `51.231` temporal at
expanded. Prediction loss was zero in the exposed classifier metric for this
run; this is an instrumentation result, not evidence of perfect prediction.
Proxy energy remains uncalibrated, and attribution among useful routing,
shortcut traffic, growth evaluation, weak edges and prediction processing is
unavailable.

**INFERRED:** The repair establishes valid policy/scale provenance and retains
a real reference-scale causal topology effect, but the corrected four-class
classification and expanded-scale comparison do not establish a useful
temporal-associative advantage or an acceptable measured tradeoff.

**HYPOTHESIZED:** Weak order sensitivity may reflect limitations of the
existing synthetic readout or timing alignment. No predictor, readout, energy
model or 12I policy redesign was made.

## Direct answers and gate

1. Four classes were generated and externally represented, but useful class
   separation was not demonstrated.
2. The order intervention did not change measured readout accuracy.
3. Temporal growth produced causal reference-scale path allocation.
4. The policy-specific structural distinction was not unique at expanded scale.
5. The exposed prediction-loss metric was zero; its adequacy requires follow-up.
6. Temporal classifier proxy energy was higher than fixed at both scales.
7. Cost attribution is unavailable; proxy units are not physical energy.
8. Structural mutation and rejection metrics were retained per condition.
9. The learned-edge intervention changed routed computation where selected.
10. The corrected evidence is sufficient for Luna-0 review, not promotion.

Focused corrected 12L tests: **passed, 12**. Affected prior-Luna and related
tests: **passed, 72**. Full pytest: **passed, 194 passed, 1 skipped**.
Compileall, workspace diagnostics and `git diff --check`: **passed**.
Hardware and real-data checks: **not applicable/unauthorized**.

**Corrected primary gate: NOT SUPPORTED.** Return this evidence to Luna-0.
The old result remains invalid/superseded. Do not amend A14, create a
permanent energy/prediction objective, claim handwriting or real-data success,
or authorize a successor Luna.
