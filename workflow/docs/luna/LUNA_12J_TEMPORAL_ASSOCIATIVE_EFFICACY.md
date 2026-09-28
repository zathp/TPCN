# Luna-12J - Temporal-Associative Structural Learning Efficacy and Causal Verification

This specification defines a controlled experiment and verification milestone.
It does not promote the Luna-12I mechanism into A14, change the architecture
contract, authorize a bootstrap trainer, or authorize any later Luna.

```yaml
luna:
  identifier: Luna-12J
  name: Temporal-Associative Structural Learning Efficacy and Causal Verification
  task_id: temporal-associative-structural-learning-efficacy-luna-12j
  classification: [EXPERIMENT, VERIFICATION]
  baseline_revision: "05d23eba86b806e9fe7e43d5dc66321f2c4bf612"
  dependencies: [Luna-12I, Luna-12H, Luna-12E, Luna-4, Luna-10]
  owner: "Luna-0 Architecture Guardian pending experiment-owner assignment"
  production_code_authorized: "only the smallest declared exposure fix; otherwise experiment components"
```

## Purpose and hypothesis

Luna-12J answers:

> Does the Luna-12I temporal-associative structural-growth mechanism produce
> useful computational or task-level benefit, and can that benefit be causally
> attributed to the learned topology rather than merely to additional edges or
> structural churn?

**Hypothesis:** Repeated locally observable temporal succession can guide
bounded structural plasticity toward useful convergent and/or shortened causal
pathways, and those topology changes can improve downstream temporal
computation compared with structurally legal but temporally uninformed growth.

The hypothesis is falsified, in the tested scope, by equivalent or worse
computation/task behavior under matched budgets, no meaningful causal effect
from learned edges, no difference from destroyed temporal relationships, or
resource/churn costs that erase the claimed benefit. A negative result is valid.
The result must be one of `supported`, `partially supported`, `not supported`,
`inconclusive`, or `blocked`.

## Required comparison

Use the accepted persistent bounded topology and the real Luna-12E event-routing
path. Compare, with the same declared workload, seeds, topology bounds,
delays, mutation effort and reset policy:

1. Fixed topology.
2. Existing pre-12I structural-plasticity policy.
3. Random legal structural growth.
4. Luna-12I temporal-associative structural growth.

Where practical, include a temporal-causality control: shuffled order,
reversed order, destroyed timing association, or a matched event multiset with
altered temporal order. These controls must distinguish benefit from temporal
structural evidence from benefit caused only by adding or changing edges.

### Equal-resource discipline

Match edge, fan-in, fan-out, candidate, state, event, mutation-attempt,
epoch/sequence and processing budgets. Do not give temporal association more
edges, attempts, epochs, events, candidate capacity or state. If exact equality
is impossible, record the mismatch and normalize or discuss its effect.
Retain every declared seed and failed admission; do not search for favorable
seeds.

## Benchmark and computational boundary

Prefer an existing deterministic temporal benchmark accepted by the workflow.
The Luna-12G spiral benchmark may be used if its controls expose the temporal
computational difference under study. If it cannot distinguish the policies,
authorize only the smallest deterministic synthetic temporal fixture needed to
isolate structural learning. Do not introduce a real-world dataset or claim
real-data generalization.

Topology mutations must be applied through the existing bounded mutation
authority and must change the actual routed event path used by neural
computation. A disconnected visualization graph, auxiliary topology, topology
appearance, or edge-count change is not computational evidence.

## Preserved invariants and information boundaries

The experiment preserves A01 event-driven computation, A02 intrinsic temporal
state, A03 finite propagation and unequal delays, A04 bounded topology, A06
predictive coding, A07 local learning and information boundaries, A08 bounded
recurrence, A09/A10 local energy and utility semantics, A11 delayed credit,
A14 bounded structural plasticity, and A15 hardware independence.

Labels remain outside canonical neural events, predictor state, routing,
topology evidence, structural-learning evidence, eligibility and energy
computation. Candidate evidence may use only causally/local observable event
history. No future event, global topology statistic, evaluation metric,
unrestricted trainer state, wall-clock time or label may enter a structural
decision. Every history, candidate, edge, queue, lineage/path, mutation and
measurement buffer must be finite and declared.

## Required measurements

Record where applicable, for every condition and seed:

- task accuracy or class separation, prediction loss and prediction-error behavior;
- processed events, neuron activations, estimated energy/resource cost, units and utility;
- edge count, accepted additions, removals/pruning and every growth rejection reason;
- fan-in/out distributions, saturation, convergent fan-in motifs and active-edge utilization;
- causal path length, cumulative propagation delay and path shortening;
- duplicate proposals, replacement rate, edge churn and topology stabilization;
- same-seed structural and computational determinism.

Useful tradeoffs count as evidence when measured: the same task result with
fewer events, the same prediction quality at lower resource cost, better
prediction under an equal edge budget, or shorter useful causal paths.
Accuracy alone is insufficient.

## Causal intervention

Do not infer causation from topology/behavior correlation alone. Include at
least one focused intervention where practical:

- remove a learned shortcut or one convergent input;
- freeze the learned topology;
- replace a learned edge with a legal random edge; or
- replay identical events before and after a topology intervention.

Record the chain `local temporal evidence -> structural decision -> real
topology change -> changed routed event path -> changed downstream neural
state/output`, without labels entering the neural core.

## Explicit fan-in question

The handoff must answer whether ordinary growth consumes topology capacity
before useful convergent fan-in can form. Measure whether fan-in capacity is
reached, useful convergence forms before saturation, temporal association
changes candidate selection, path shortening changes arrival timing, edge
replacement is required, unused edges dominate capacity, or the original
concern is unsupported. Do not assume the concern is confirmed.

## Authorized scope and exclusions

Luna-12J may own experiment fixtures, controlled runner options, measurement
hooks, analysis code, focused tests and this handoff. A production change is
allowed only to expose an already-supported configuration or measurement and
must be the smallest demonstrated fix. If a defect prevents valid evaluation,
demonstrate it and either apply that authorized minimal fix or return
`BLOCKED` to Luna-0.

It must not redesign the Luna-12I policy because results are weak, change the
canonical architecture, modify A14 to require temporal association, introduce
labels/global learning/future information, add an auxiliary topology, claim
real-data or hardware acceptance, or authorize Luna-12K or another successor.

## Required verification and validation

Focused tests must establish that:

1. All compared policies obey identical topology bounds.
2. Temporal association consumes no labels or future information.
3. Same seed and configuration reproduce structural decisions.
4. Temporal growth makes the intended real topology changes.
5. Those changes alter actual routed computation.
6. Removing/disabling the learned connection changes or removes its downstream causal contribution.

Use parameterized tests where appropriate. Run focused Luna-12J tests,
Luna-12I tests, Luna-12H temporal tests, relevant Luna-12E computational
routing tests, affected structural-plasticity and classifier/readout
regressions, full `pytest`, compile/static validation, workspace diagnostics,
and `git diff --check`. Classify each result as passed, failed, not run or not
applicable; an unexecuted check is never passing evidence.

## Gate definitions

- **PASS:** controlled evidence demonstrates meaningful computational/task
  benefit from temporal-associative growth and supports the relevant causal
  link. This does not promote the mechanism into A14.
- **PASS WITH FOLLOW-UP:** credible benefit exists but a precise bounded issue
  remains, such as limited seeds, fixture-only benefit, uncertain energy
  tradeoff, benchmark limitation or missing scale evidence. Name the follow-up.
- **INCONCLUSIVE:** the valid experiment cannot distinguish the policies.
- **NOT SUPPORTED:** valid controlled evidence does not support the proposed
  advantage in the tested scope.
- **BLOCKED:** a defect, invalid benchmark, information leak, broken causal
  path, nondeterminism or missing dependency prevents a valid experiment.

## Evidence and promotion boundary

The handoff separates `OBSERVED`, `INFERRED` and `HYPOTHESIZED` statements.
Even a PASS returns control to Luna-0. The temporal-association algorithm does
not automatically become a mandatory A14 mechanism. Luna-0 may retain it as
optional, authorize broader verification, promote only a general principle,
open an ACP for the specific mechanism, or reject/deprecate it. No later
implementation Luna is automatically authorized.

The handoff must record baseline revision, policy definitions,
benchmark/workload, seed set, resource budgets, controls, commands, raw and
summarized measurements, causal intervention, topology/task/resource evidence,
negative results, limitations, tests, clauses, files, evidence classifications,
gate decision, recommended Luna-0 action, and direct answers to:

1. Did temporal growth form more useful convergence than controls?
2. Did it shorten meaningful causal paths?
3. Did those changes affect real neural computation?
4. Did computation improve task behavior or resource efficiency?
5. Did the result survive comparable structural budgets?
6. Did destroying temporal relationships reduce or eliminate the effect?
7. Is the evidence strong enough for a separate architecture-promotion review?

## Dependency graph

```text
Luna-12H
    |
    v
Luna-12I  Temporal-Associative Structural Growth
    |
    v
Luna-12J  Efficacy + Causal Verification
    |
    v
Luna-0 review
```

Luna-13 and Luna-14 remain independent siblings. No successor beyond the
Luna-0 review is authorized by this milestone.