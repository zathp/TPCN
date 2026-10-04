---
name: Luna-32 Historical Luna-12L / Spiral Model-Explicit Compatibility
description: Make the historical TANH_LEGACY model explicit for the Luna-12L four-class classifier conditions and the spiral run_controls family; no core, ACP or efficacy change.
---

# Luna-32 — Historical Luna-12L / Spiral Model-Explicit Compatibility

## Authorization and baseline

```text
Luna-0 -> Luna-32 -> Luna-0
```

Luna-32 is **AUTHORIZED / NOT EXECUTED** by
`workflow/handoffs/luna-0-post-luna31-luna12l-spiral-policy-compatibility-decision-20261004.md`.
Baseline: clean `main`, `HEAD == origin/main == 392ce2510660221d7486a59f184a1eeba6f17634`.
Verify branch, `HEAD == origin/main`, clean worktree and that no production code,
test, ACP or contract changed after the authorization publication; otherwise stop
and return to Luna-0. Luna-32 must not self-close and must not authorize a successor.

Classification: IMPLEMENTATION + EXPERIMENT COMPATIBILITY + PROVENANCE
PRESERVATION + FOCUSED VERIFICATION.

## Problem

Nine tests fail with `ValueError: structural plasticity is unavailable unless
structural observation is enabled`. `ExperimentConfig.neuron_model` now defaults
to `EXCURSION_V1`, whose growth path accepts only `structural_policy="e2_local_temporal"`
with explicit ACP-0007 bounds. Luna-12L (`tpcn/temporal_scale.py`) and the spiral
`run_controls()` family were authored (commits `3b2b032`, `06f74e4`) when the only
model was the legacy tanh model; the model was implicit. The legacy policies
`baseline/random/temporal/reversed` are real, distinct legacy topology-adaptation
paths under `TANH_LEGACY` (`ExperimentRunner._adapt_topology`) and have no exact
E2 equivalent.

## Required change

1. In `tpcn/temporal_scale.py::_classification_metrics`, set `neuron_model="TANH_LEGACY"`
   explicitly for **all five** policy conditions (including `fixed`). Never mix models
   across policies. Keep `structural_plasticity = policy != "fixed"` and
   `structural_policy = policy`. Scales, seeds, bounds and the `executed_policy`
   provenance guard stay as they are; `executed_policy` must remain a truthful
   statement of the policy the legacy runner executed. Expose the executed model
   (e.g. `executed_neuron_model="TANH_LEGACY"`) in the classifier provenance only if
   needed to make the label explicit, and include it in the provenance check.
2. In `tpcn/spiral_benchmark.py::run_controls`, make all ten controls use the same
   explicit `neuron_model="TANH_LEGACY"` (put it in the shared `base`). Do not make
   only the structural control legacy (cross-model confound). `run_policy_control`
   callers pass their own config; do not change its policy set.
3. Label the source docstrings/comments and tests `HISTORICAL COMPATIBILITY
   EXPERIMENT` and `NOT CURRENT EXCURSION_V1 / ACP-0007 EFFICACY EVIDENCE`.
4. Update the nine failing tests only as needed to state the explicit legacy model and
   the historical label. Preserve every invariant: requested==executed policy,
   policy-dependent classifier topology, distinct reference/expanded configurations,
   serialization, and the deliberate provenance-mismatch `RuntimeError`. Do not
   weaken or delete assertions. Do not add `xfail`/skip.

## Historical scales (preserve, not architecture invariants)

Reference: 7 nodes, edge capacity 6, fan in/out 2, candidate/history 8, queue/event
16, growth attempts 3. Expanded: 12 nodes, 10, 3, 12, 24, 5.

## Owned files

```text
tpcn/temporal_scale.py
tpcn/spiral_benchmark.py
tests/test_luna12l_temporal_scale.py
tests/test_spiral_benchmark.py
workflow/handoffs/luna-32-historical-temporal-spiral-model-compatibility-20261004.md
```

## Prohibited

`tpcn/experiments.py`, `tpcn/experiment_excursion_runtime.py`,
`tpcn/excursion_neuron.py`, `tpcn/structural_observation.py`,
`tpcn/temporal_association.py`, `tpcn/structural_plasticity.py`, `tpcn/topology.py`,
`tpcn/cpu_visualization.py`, `tpcn/visualization.py`, `run_temporal_scale.py`,
`run_spiral_benchmark.py`, everything under `artifacts/` (the corrected Luna-12L
artifact `artifacts/temporal-scale-12l` and the invalid pre-coupling artifact are frozen),
the handoffs of Luna-12L/12G, ACP-0007, the Architecture Contract, and all other tests
(including Luna-12E). No fake aliases `baseline|random|temporal|reversed ->
e2_local_temporal`. No new E2 experiment.

## No scientific laundering

Luna-0 probed explicit `TANH_LEGACY`: policies, events, classifier topology edge counts
and provenance reproduce, but proxy energy, replay digests and 7/30 sampled accuracies
differ from the retained artifact (current legacy code differs from the 12L-time code).
Therefore the compatibility run is **NOT** the same experiment and must not be
described as reproducing, correcting or superseding the corrected Luna-12L result
(`NOT SUPPORTED`). Do not regenerate, overwrite or append to the historical artifact or
handoff. Report any rerun numbers only as compatibility diagnostics.

## Verification

- `python -m pytest -q tests/test_luna12l_temporal_scale.py tests/test_spiral_benchmark.py`
  (expect 0 failures); tests prove explicit `TANH_LEGACY` for all conditions and that the
  provenance mismatch still raises.
- Evidence that `fixed` and the four legacy policies share one model and that the spiral
  structural control is not a cross-model comparison; spiral determinism (`first == second`).
- Full suite: expect 0 failures, no new regressions, no hard-coded pass count; record
  collection count and confirm no deleted/xfailed/skipped/deselected test.
- `python -m compileall -q tpcn tests`, `git diff --check`, diagnostics on touched files.
- Complete handoff (`contract_version: "1.2"`) recording the above, the not-same-experiment
  disclosure, A01/A03/A04/A06/A07/A08/A10/A14/A15 audit, and: task efficacy NOT
  ESTABLISHED, current E2 four-class validation NOT ESTABLISHED, hardware equivalence NOT
  ESTABLISHED.

## Stop conditions

Any need to change a prohibited file, any legacy policy that cannot truthfully execute
under `TANH_LEGACY`, a provenance guard that can only pass by string echo, or an
unexpected new failure: STOP and return to Luna-0. Commit and push only when
instructed; never self-close; Luna-33 is NOT AUTHORIZED.
