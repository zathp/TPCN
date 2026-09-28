# Luna-12I - Temporal-Associative Structural Growth and Fan-In Formation

This specification is governed by the Future Luna Contract in
`LUNA_WORKFLOW.md` and ACP-0001. It defines a testable hypothesis only; it does
not claim that the mechanism works or authorize architecture promotion.

```yaml
luna:
  identifier: Luna-12I
  name: Temporal-Associative Structural Growth and Fan-In Formation
  task_id: temporal-associative-structural-growth-fan-in-formation-luna-12i
  classification: [EXPERIMENT, VERIFICATION]
  baseline_revision: "396504dbf240509fb897a37965ec9fee123d17d3"
  dependencies: [Luna-12H, Luna-4, Luna-10, Luna-12E]
  owner: "Luna-0 Architecture Guardian pending experiment-owner assignment"
  production_code_authorized: "only declared experiment components"
```

## Hypothesis and falsifier

Repeated, consistent short causal sequences may make a locally observed
earlier-to-later candidate preferable. The hypothesis is contradicted when
temporal association does not improve convergent causal organization over
matched controls, when shuffled/reversed timing performs equivalently, or when
it increases churn, resource use or prediction error without useful structural
or task improvement.

## Controls

Use matched fixed topology, the existing structural-plasticity policy, random
legal candidate selection and temporal-association candidate selection. Add
timing-shuffled and reversed-order association controls where practical. Keep
seeds, topology/resource budgets, delays, workload, resets and training effort
matched.

## Invariants and boundaries

Preserve A01-A08, A07 locality and label isolation, A09-A11, A14 and A15.
Use only causally/local available event timing. Do not use global topology
knowledge, labels, future events or evaluation-only metrics in canonical
structural decisions. Every candidate, history, edge, mutation, event,
lineage/path and queue must be bounded. New edges have positive finite delay
and cannot rewrite emitted or in-flight events.

## Measurements and verification

Measure fan-in/out distributions and saturation, edge utilization, accepted
growth, explicit rejection causes, duplicate proposals, candidate availability,
path lengths/delays, convergent motifs, repeated associations, path shortening,
replacement/pruning, lifetimes/churn, event count, prediction error,
energy/resource proxy and units, utility, task performance and determinism.
Record `OBSERVED`, `INFERRED` and `HYPOTHESIZED` separately. Run focused tests,
prior topology/plasticity/routing/neuron regressions, applicable full
regression, compile/static validation, diagnostics and `git diff --check`.

## Unauthorized work

Do not require a specific timing window or formula, redesign classification,
claim real-dataset or hardware acceptance, promote A14, add global learning,
inject labels, introduce unbounded topology or infer useful structure from
topology appearance alone.
