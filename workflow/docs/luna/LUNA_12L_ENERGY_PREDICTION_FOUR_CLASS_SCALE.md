# Luna-12L - Energy/Prediction Tradeoff and Four-Class Temporal Scale Verification

This specification creates a narrowly scoped `EXPERIMENT` and `VERIFICATION`
follow-up to the reviewed Luna-12K result. It does not execute the experiment,
promote temporal-associative structural learning into A14, change the
architecture contract, or authorize any later Luna.

```yaml
luna:
  identifier: Luna-12L
  name: Energy/Prediction Tradeoff and Four-Class Temporal Scale Verification
  task_id: energy-prediction-four-class-temporal-scale-luna-12l
  classification: [EXPERIMENT, VERIFICATION]
  baseline_revision: "3122c7dbae2589c1c78fe6169d394f525c212ec1"
  dependencies: [Luna-12K, Luna-12J, Luna-12I, Luna-12H, Luna-12E, Luna-4, Luna-10, Luna-12G]
  owner: "Luna-0 Architecture Guardian pending experiment-owner assignment"
  production_code_authorized: "only the smallest demonstrated measurement exposure fix"
```

## Motivation and scope

The current Luna-0 review confirms Luna-12K `PASS WITH FOLLOW-UP`. In the
seven-node synthetic fixture, temporal growth selected the shortcut in `5/5`
seeds while baseline, random and reversed controls selected it in `0/5`; the
initial three-hop delay was `3.0`, the shortcut delay was `0.75`, and removal
restored the original routed trace and downstream state. The same evidence
shows a tradeoff: temporal proxy energy was `9.850877` versus adaptive-control
energy `9.274247`, while temporal prediction loss was `1.284030` versus
`1.025229`.

Luna-12L answers two narrow questions:

1. Does the temporal-associative policy retain useful classification and causal
   path-allocation behavior when the spiral task expands from two classes to
   four classes using handedness and traversal direction?
2. Can the observed energy and prediction-loss cost be explained, bounded or
   improved without destroying the causal structural benefit?

This is a scale-and-tradeoff experiment. It is not a general architecture
redesign, a new structural-learning algorithm, a real-dataset benchmark, an
A14 promotion, or a hardware-acceptance milestone.

## Hypotheses and falsifiers

**Primary hypothesis:** Temporal-associative growth retains a measurable
advantage in useful causal topology allocation as the synthetic temporal task
expands from two to four classes and from the reference scale to a modest
expanded scale, but its usefulness must be judged jointly against prediction
quality and computational/resource cost.

**Secondary hypothesis:** The Luna-12K cost increase is at least partly caused
by additional useful routed activity or structural allocation rather than
uncontrolled computation. This may be false.

The primary hypothesis is falsified in the tested scope when four-class
classification or useful path allocation is no better than matched controls,
the benefit disappears at the expanded scale, order controls perform
identically, class-resource conflict removes the advantage, or the
energy/prediction tradeoff is unfavorable without a measured compensating
benefit. An unfavorable result is valid evidence.

## Four-class temporal benchmark

Use the accepted Luna-12G generator conventions and these external labels:

- `spiral-left-outward`
- `spiral-right-outward`
- `spiral-left-inward`
- `spiral-right-inward`

`spiral-left` and `spiral-right` preserve the Luna-12G handedness convention.
The inward classes use the same general trajectory family as outward classes,
with reversed traversal or its explicitly declared causal equivalent. Where
practical, use the same geometric path in opposite directions as a focused
matched pair. The benchmark must make outward versus inward recognition depend
on event order, not a class-specific static shape.

Match point count, radius range, center, scale, noise distribution, sampling
density, amplitude range, event payload conventions, sequence duration and
identifier format across classes where practical. Use deterministic disjoint
train/evaluation streams and record generator metadata, transforms, seeds and
digests outside canonical input.

Do not add class markers such as `inward`, `outward`, `left`, `right` or a
class number to neural input. If an existing sequence-boundary/check event is
needed, reuse it and require that it is identical and class-neutral for all
four classes, contains no future outcome, and serves only its declared
control purpose. Labels remain external to readout supervision/evaluation and
must not enter canonical events, payloads, IDs, predictor state, routing,
topology evidence, structural decisions, eligibility or energy computation.

## Conditions and scale configurations

At each scale compare:

1. fixed topology;
2. pre-12I structural growth;
3. random legal structural growth;
4. Luna-12I temporal-associative structural growth; and
5. reversed, shuffled or timing-destroyed temporal evidence.

Use seeds `0, 1, 2, 3, 4`. Match candidate exposure, candidate count, growth
attempts, mutation budget, edge/fan-in/out bounds, examples, epochs,
queue/event budgets and reset policy within each scale. Report every exposed,
considered, selected, accepted and rejected candidate and every rejection
cause. Do not select seeds or tune after inspecting outcomes.

The minimum declared scales are:

| Scale | Bounded configuration |
|---|---|
| reference | The 12K seven-node routed fixture family; edge/routing capacity 6; fan-in/out 2; candidate/history capacity 8; queue/event capacity 16; three growth attempts; at least two examples per class per split. |
| expanded | A modest 12-node routed fixture; edge/routing capacity 10; fan-in/out 3; candidate/history capacity 12; queue/event capacity 24; five growth attempts; at least two examples per class under the same split protocol. |

All scale values are experiment settings, not architecture invariants. The
expanded scale remains bounded and interpretable; it is not a capacity search.
Serialize the exact configuration before execution.

## Temporal-order controls and reporting

Run at least one explicit order intervention: reverse an outward sequence into
matched inward traversal, shuffle event order while preserving the event
multiset, or destroy local timing while preserving spatial samples. Declare
before scoring whether the transformed target should invert, remain unchanged
or be ambiguous.

Report overall four-class accuracy, per-class accuracy, a four-by-four
confusion matrix, class separation/readout evidence, left-versus-right
confusion and inward-versus-outward confusion. Specifically report:

- left outward versus left inward;
- right outward versus right inward;
- left outward versus right outward; and
- left inward versus right inward.

Four-class accuracy alone is not evidence of temporal computation.

## Measurements and energy/prediction tradeoff

For every condition, scale and seed record classification, prediction and
resource evidence:

- accuracy, per-class accuracy, confusion, class separation and readout state;
- prediction loss, prediction-error count/activity and timing;
- proxy/resource energy, units and calibration status;
- total/routed events, neuron activations, edge count and active-edge
  utilization;
- fan-in/out distributions, saturation, convergent motifs, path hops,
  cumulative delays and arrival timestamps;
- candidate exposure, growth attempts, accepted additions, rejected causes,
  pruning/replacement, churn and stabilization;
- class-specific edge utilization and evidence of capacity conflict; and
- deterministic replay digest and causal-intervention results.

Calculate accuracy per event, accuracy per proxy-energy unit, prediction loss
per example, proxy energy per correctly classified example and events per
correctly classified example. Define the zero-correct policy for ratios.
These are experimental summaries, not permanent architecture objectives.
Continue to call the quantity proxy/resource energy; no physical-energy claim
is permitted without hardware calibration.

Where practical, estimate separate contributions from useful routed activity,
additional shortcut traffic, structural-growth evaluation, unused or weakly
used edges and prediction-error processing. Mark attribution unavailable when
the existing instrumentation cannot identify it.

Investigate the 12K prediction-loss increase without redesigning the
predictor. Test whether shortcut arrival timing, additional prediction
comparisons, shortened delays, discriminative path allocation or
prediction-error processing explains the difference. Classify the conclusion
as observed degradation, timing/alignment issue, expected objective separation
or unresolved.

## Causal intervention and class conflict

Retain the 12K causal intervention. Identify a learned temporal shortcut,
replay identical examples before and after its formation, remove or disable it,
and compare routed traces, path delay, downstream state/output, classification,
prediction loss, proxy energy and event/activation counts. Where practical,
measure whether a shortcut useful for one handedness/direction class consumes
capacity or harms another class.

Continue recording fan-in and fan-out saturation, edge replacement,
class-specific utilization, conflicting temporal associations, per-class
degradation and shortcut survival/pruning. The required causal chain is:

```text
local temporal evidence -> structural decision -> real topology change
-> changed routed computation -> downstream state/output and tradeoff
```

## Focused tests and required artifact

Focused tests must establish:

1. deterministic generation of all four classes;
2. matched inward/outward trajectories differ primarily by traversal direction;
3. class labels never enter canonical computation;
4. a boundary/check event, if used, is class-neutral;
5. same seed reproduces the benchmark and structural decisions;
6. all policies retain identical declared bounds at each scale;
7. the external readout represents all four classes;
8. an order intervention changes the intended temporal information;
9. energy and prediction metrics are recorded consistently; and
10. at least one learned-edge intervention changes real routed computation.

Each machine-readable artifact must contain baseline revision, exact
configuration, scale, seed, class definitions, policy, accuracy, per-class
accuracy, confusion data, prediction loss, energy proxy, event and activation
counts, edge count/utilization, structural mutations, path metrics and causal
intervention results.

## Validation and evidence classification

Run and classify separately as `passed`, `failed`, `not run` or `not
applicable`: focused 12L tests; 12K, 12J, 12I and 12H tests; relevant 12E
routing tests; affected spiral/readout and structural-plasticity tests; full
`pytest`; compileall/static validation; workspace diagnostics; and `git diff
--check`.

The completion handoff must separate:

- **OBSERVED:** direct four-class, topology, route, state, resource or test
  measurements;
- **INFERRED:** interpretations supported by those observations; and
- **HYPOTHESIZED:** untested scale, generalization or mechanism claims.

Use these gates:

- **PASS:** useful four-class structural/classification behavior survives both
  scales and the energy/prediction tradeoff is acceptable, bounded or
  meaningfully explained;
- **PASS WITH FOLLOW-UP:** evidence remains promising but a bounded issue
  remains, such as energy overhead, prediction degradation, scale sensitivity,
  class conflict or synthetic-only scope;
- **NOT SUPPORTED:** controlled evidence removes the useful benefit or yields
  an unfavorable tradeoff within the tested scope;
- **INCONCLUSIVE:** valid evidence cannot distinguish the policies; or
- **BLOCKED:** leakage, nondeterminism, invalid controls, broken causal
  semantics or an implementation defect prevents valid evaluation.

Any result returns to Luna-0. A gate does not promote A14, establish an energy-
prediction utility formula, imply handwriting/general-dataset success, or
authorize a successor.

## Architecture boundary and dependency

No A01-A15 clause is changed. Preserve A01-A04, A06-A11, A14 and A15. Do not
redesign the canonical neuron, predictor, energy model, readout, 12I policy or
topology authority. Do not claim real-data or hardware acceptance.

```text
Luna-12K PASS WITH FOLLOW-UP
    |
    v
Luna-12L  Energy / Prediction Tradeoff and Four-Class Temporal Scale
    |
    v
Luna-0 review
```

Luna-13 and Luna-14 remain independent siblings. No later Luna is authorized
by this specification.
