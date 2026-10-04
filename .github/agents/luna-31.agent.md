---
name: Luna-31 Luna-12E EXCURSION_V1 Observable Compatibility Correction
description: Replace stale Luna-12E test expectations with current public EXCURSION_V1 observables; test-only scope.
---

# Luna-31 — Luna-12E EXCURSION_V1 Observable Compatibility Correction

## Authorization and baseline

This is an authorized, bounded **test-only compatibility correction**:

```text
Luna-0 -> Luna-31 -> Luna-0
```

Luna-0 independently classified the two remaining Luna-12E failures as stale
test oracles. Luna-31 is **AUTHORIZED / NOT EXECUTED** by the authorization
record in
`workflow/handoffs/luna-0-post-luna30-luna12e-e2-observable-decision-20261004.md`.

The verified baseline is clean `main` at
`8d5f7f5ad1c594df3cd886de327eb14c3dfbe15c`
(`docs: close Luna-30 replay consumer compatibility`). Before implementation,
verify `HEAD == origin/main`, the worktree is clean, and the baseline is an
ancestor of the working revision. The opaque revision string in the source
request did not resolve as a Git revision; Luna-0 recorded that discrepancy.

Read the architecture contract, changelog, Luna workflow, acceptance criteria,
Luna-12E contract, Luna-0 classification and authorization handoff, and the
handoff template before editing. Preserve unrelated work.

## Classification, hypothesis, and boundaries

- Classification: **IMPLEMENTATION + TEST COMPATIBILITY + FOCUSED VERIFICATION**.
- Hypothesis: both failures result from legacy observable assertions that no
  longer express the current default EXCURSION_V1 behavior; accepted public
  metrics and reset-state observations suffice to verify the intended
  invariants without production changes.
- Counter-hypothesis: if a legitimate current public observable is unavailable
  or contradicts the accepted lifecycle, stop and return to Luna-0.
- No production implementation, runtime, prediction, topology-routing, reset,
  architecture, or schema change is authorized.
- No prediction-loss delta, classification benefit, reward benefit, utility
  benefit, structural-learning benefit, energy benefit, or hardware equivalence
  claim is authorized.
- Architecture Contract 1.2, A01-A15 and accepted ACP-0007 remain unchanged.
  E2 pruning and ACP-0002 N3 remain unauthorized.

## Exact ownership

Luna-31 owns only:

```text
tests/test_luna12e_integration.py
workflow/handoffs/luna-31-luna12e-e2-observable-compatibility-20261004.md
```

No production files are owned. If another file or interface must change, stop
and return to Luna-0 without expanding scope.

Do not change:

```text
tpcn/experiments.py
tpcn/experiment_excursion_runtime.py
tpcn/excursion_neuron.py
tpcn/predictive_coding.py
tpcn/topology.py
tpcn/structural_plasticity.py
tpcn/cpu_visualization.py
tpcn/visualization.py
```

Also prohibit all Luna-12L and spiral code/tests, and the first three
Luna-12E historical component tests for legacy topology growth/pruning,
already-queued delivery after pruning, and multi-hop source progression.
Their legacy/general topology coverage is not authorization for E2 pruning.

## Required compatibility oracles

### Routed-topology test

Keep assertions that the route is absent without the edge and present with the
edge. Keep the event-count comparison using the current public metric
`metrics.event_count` (the live API does not name this field
`processed_event_count`). Require the reachable edge to produce observable
routed traffic and increased work. Add/retain public metric comparisons showing
that `edge_transfer_proxy` and `maximum_route_depth` increase.

Remove the required prediction-loss inequality. For this fixture, equal
prediction loss is allowed and must be recorded as an observation, not treated
as a routing failure. Do not redesign predictions or alter the workload to
manufacture a delta.

### Character reset and identity test

Keep stable neuron identity across repeated evaluations. For the current
default EXCURSION_V1, replace the old exact terminal-clock assertions with:

```text
terminal local clock == last external timestamp + configured settling_horizon
neutral state / mode
no pending internal work
```

Use only existing public interfaces: the local clock timestamp, `state`,
`mode`, and `pending_event` (or its public equivalent). For this fixture, the
last external timestamp is `1.0`, the configured horizon is `4.0`, and the
terminal timestamp is `5.0`. Do not claim that the terminal timestamp equals
the next character's first input timestamp: the test observes neurons after
the whole evaluation, not at the pre-input boundary.

The old `0.0` / `1.0` terminal-clock expectations are **LEGACY-ONLY**. A
separate explicit `TANH_LEGACY` regression may preserve them if it remains
small and model-specific, but it is not a gate for accepting the EXCURSION_V1
oracle. Do not tag the E2 reset test as legacy.

## Acceptance criteria

1. Without the edge, no `neuron-0 -> neuron-1` route appears.
2. With the edge, an actual routed event/trace entry for
   `neuron-0 -> neuron-1` appears.
3. Public event-count/work metric increases with the reachable edge.
4. `edge_transfer_proxy` is positive/increases with the edge.
5. `maximum_route_depth` increases with the edge.
6. Equal `prediction_loss` is permitted and explicitly recorded; no efficacy
   conclusion follows.
7. Persistent neuron identity remains stable across repeated evaluation.
8. Terminal E2 local time equals the fixture's last external timestamp plus
   the configured settling horizon.
9. E2 neuron mode/state are neutral after character-local reset.
10. No pending internal event remains at the observed terminal boundary.
11. No production code changes.
12. All Luna-12E tests pass, and no new applicable regression is introduced.

## Verification

Run:

```text
python -m pytest -q tests/test_luna12e_integration.py
```

Run the relevant existing EXCURSION_V1 integration/routing and Luna-26
multi-hop prediction-error routing regressions. Run the full test suite and
record the exact results. The prior baseline was 896 passed, 11 failed, and
1 skipped (908 collected), with 8 Luna-12L and 1 spiral failures remaining
after removing the two Luna-12E failures. Do not hard-code a resulting pass
count. Require zero Luna-12E failures and zero new applicable regressions.

Record commands, revision, environment, observations, failures and checks not
run in the owned completion handoff. Do not claim that this test-only
compatibility correction establishes learning or task efficacy.

## Stop conditions and return

If an assertion cannot be expressed using existing public evidence, if any
production file appears necessary, or if runtime behavior contradicts the
accepted EXCURSION_V1 lifecycle, stop and return to Luna-0. Do not implement
observability or change semantics. On completion, return the test diff and
handoff to Luna-0 for independent review; do not expand this assignment.
