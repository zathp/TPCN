---
name: Luna-35 Eligibility Capacity Lifecycle Characterization
description: Characterize bounded per-character eligibility trace creation, occupancy, expiry, reward, and reset behavior without changing production semantics.
---

# Luna-35 — Eligibility Capacity Lifecycle Characterization

## Authorization and baseline

```text
Luna-0 -> Luna-35 -> Luna-0
```

Luna-35 is **AUTHORIZED / NOT EXECUTED** by the independent post-Luna-34
review in
`workflow/handoffs/luna-0-independent-review-luna34-eligibility-capacity-20261004.md`.
The Luna-34 execution evidence baseline is
`4d77489eaebadf638f22996d1d0d49e162b378ab`; before execution, verify a clean
`main` synchronized with `origin/main` containing this authorization and
record that exact `HEAD` as the run baseline. This is a bounded
**OBSERVATION + VERIFICATION** assignment, not a propagation-to-emission
experiment, task-efficacy experiment, production correction, or architecture
promotion.

## Primary hypothesis

For the fixed Luna-34 no-edge reproducer, each source canonical emission
creates a distinct local eligibility trace. Predictor records may expire
before the character ends while those eligibility entries remain resident;
the per-ledger hard capacity then rejects the first new trace beyond its
limit. Character destruction is the existing lifecycle boundary that releases
the ledger state.

**Counter-hypothesis:** existing reward, expiry, or character-boundary
behavior retires or reuses eligibility entries before the reported capacity
is reached, or the exact configured two-neuron run does not reproduce the
observed occupancy and overflow.

The goal is to determine whether this is expected finite-capacity behavior,
a lifecycle mismatch, an undocumented capacity contract, or a production
defect. Reaching the exception alone does not establish a defect.

## Evidence baseline and fixed diagnostic fixtures

Use the public data generation and runtime configuration recorded by Luna-34.
Read each generated example's `points` only; do not inspect labels or
label-bearing metadata.

The primary fixed reproducer is seed `0`, condition `NO_EDGE_CONTROL`,
shuffled sequence index `4` (`c00-004`), with 20 original training points,
input `point.x + point.y`, and the unchanged `random.Random(330000)` stream.
Use two neutral `MultiExcursionNeuron(config=E1Config())` instances, no route
edges, `prediction_capacity=8`, queue capacity `128`, event budget `1024`,
settling horizon `4.0`, prediction expiry `4.0`, neutral reward, and the
existing Luna-34 runtime behavior.

Use one low-activity, one-point no-edge character under the same settings
only as a lifecycle/control fixture. It checks normal `end_character()` and
the existing next-character reset boundary; it does not serve as an
experimental condition.

Do not run the other Luna-34 topology conditions, the complete five-seed
design, any efficacy endpoint, or a propagation-to-emission retry.

## Required observations

For each fixed fixture, record:

- Actual runtime-derived `EligibilityLedger.max_traces` per node and aggregate
  allocated trace capacity. Verify from source that the node count multiplier
  is applied in the per-ledger expression and that the runtime creates one
  ledger per node.
- Every eligibility activity event through the terminal point: node/ledger,
  trace ID, prediction ID, canonical emission ID, timestamp, magnitude,
  creation versus update, and occupancy before/after.
- At the first rejected insertion: exact seed/fixture, input point index,
  source event count, canonical emission sequence/identity, exception, and
  all resident trace identities, values, credits, timestamps and prediction
  IDs immediately after time decay and before insertion.
- Predictor creation, observation, match, unmatched-observation and expiry
  identities/timestamps; distinguish predictor expiry from eligibility
  retirement.
- Every prediction-error and reward signal that reaches a ledger, its
  identity, attribution status, and occupancy effect. Record whether the
  neutral end-character reward occurs before or after the overflow.
- Whether `apply_signal`, predictor expiry, and any other legitimate
  production event removes a trace. Do not infer retirement from zero or
  decayed eligibility value.
- Ledger state just before and after the existing end-character destruction
  boundary in the low-activity fixture, plus the state of the newly allocated
  ledger on its next character.
- Deterministic replay of the fixed observations and occupancy digest.

Use bounded, test-local instrumentation/wrappers where needed. Do not add
production observability or expose private runtime state as a new public API.
Clearly distinguish directly observed values from source-derived explanation.

## Bounds and controls

The diagnostic has exactly two fixed fixtures: the identified 20-point
no-edge reproducer and the one-point no-edge lifecycle control. The only
capacity configuration under test is the existing required
`prediction_capacity=8` with two nodes. Source inspection may verify the
capacity formula; do not sweep node counts, prediction capacities, trace
limits, expiry values, or workloads.

Do not increase capacity, alter expiry, change predictor/reward behavior, add
eligibility cleanup, or omit activity events to obtain a passing run.

## Exact owned files

Luna-35 may add/change only:

```text
run_luna35_eligibility_capacity_lifecycle.py
tests/test_luna35_eligibility_capacity_lifecycle.py
artifacts/luna35-eligibility-capacity-lifecycle/config.json
artifacts/luna35-eligibility-capacity-lifecycle/results.json
artifacts/luna35-eligibility-capacity-lifecycle/summary.json
workflow/handoffs/luna-35-eligibility-capacity-lifecycle-20261004.md
```

Do not modify production/core/runtime/eligibility code, dependency manifests,
ACP files, the Architecture Contract, workflow, changelog, Luna-34 files or
artifacts, Luna-33 evidence, or historical findings. If a production defect
is demonstrated, stop and return the evidence to Luna-0; do not repair it.

## Stop conditions and prohibited conclusions

Stop if the fixed reproducer does not match the declared points/configuration,
the runtime does not reproduce the exception, instrumentation alters
canonical results, or completing the observation would require changing
production behavior, capacity, prediction expiry, reward semantics, or the
stimulus.

Do not claim or infer:

- downstream canonical emission or its absence under either static edge;
- ACP-0007 candidate formation;
- task efficacy, prediction/resource benefit, useful growth or temporal
  specificity;
- a universal production defect from deterministic capacity overflow alone;
- architecture change, hardware equivalence, or authorization of another
  Luna.

## Completion and return

Run the focused Luna-35 tests, `tests/test_eligibility.py`,
`tests/test_excursion_integration.py`, the full repository suite, Python
compilation, and `git diff --check`. Preserve skipped tests and reasons.
Report the exact capacity derivation, event/trace lifecycle, character reset
behavior, passed/failed/not-run checks, remaining uncertainty, and whether
evidence suffices for a separately bounded corrective or diagnostic proposal.
Return to Luna-0. Luna-35 does not self-close and does not authorize Luna-36.
