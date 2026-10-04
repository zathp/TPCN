# Luna-30 completion handoff — corrected

## Status and scope correction

Luna-30 is **IMPLEMENTED / CORRECTED / PUBLISHED / AWAITING INDEPENDENT REVIEW**.
This bounded corrective pass does not create a new Luna, request an architecture
decision, or expand the authorized scope.

The initial Luna-30 implementation introduced one unauthorized temporal-analysis
accounting change: it added `mutation_rejection_reasons["accepted"]` to accepted
additions and growth attempts. This was a **BOUNDED IMPLEMENTATION SCOPE DEFECT**.
The correction restored pre-Luna-30 accounting semantics:

- `accepted` is counted only from `accepted_additions`.
- `growth_attempts` is the recognized rejection reason counts plus accepted additions.
- An `accepted` key in `mutation_rejection_reasons` is not treated as an addition.
- The fixture now supplies `accepted_additions` separately from rejection reasons.

Architecture impact: **NONE**.

The initial viewer correction remains preserved. `NodeView.activation` is
`float | None`; TPCV-1 preserves the exact stored activation and TPCV-2 maps it
to `None`. Inspection follows the same mapping. Active filtering uses the
canonical `active` field, and no scalar activation is synthesized from other
TPCV-2 fields.

The temporal-analysis production edits are limited to version-neutral
capability-limit wording and restoring the pre-existing accounting semantics.
Analysis remains replay-only, descriptive, and non-causal. Edge existence does
not prove edge use; per-edge use remains unavailable without routed event
identity.

## Files changed by corrective pass

- `tpcn/temporal_analysis.py`
- `tests/test_temporal_analysis.py`

The initial Luna-30 implementation also changed:

- `tpcn/viewer_3d.py`
- `tests/test_viewer_3d.py`
- `workflow/handoffs/luna-30-tpcv2-replay-consumer-compatibility-20261004.md`

No TPCV schema, CPU visualization, structural growth, or ACP-0007 behavior was touched.

## Direct reproduction and corrected behavior

Pre-correction valid TPCV-2 probe:

- `VisualizationScene.nodes()` and `VisualizationScene.inspect()` consumed a canonical `ExcursionNeuronRecord` with no scalar `activation`.
- Both paths raised `AttributeError` when reading `neuron.activation`.

Corrected behavior:

- `NodeView.activation` is `float | None`.
- TPCV-1 activation is preserved exactly.
- TPCV-2 activation projects to `None`.
- `VisualizationScene.inspect()["activation"]` follows the same mapping.
- The canonical `record.active` continues to drive active-only filtering; there is no synthesized TPCV-2 activation.

## Files changed

- `tpcn/viewer_3d.py`
- `tpcn/temporal_analysis.py`
- `tests/test_viewer_3d.py`
- `tests/test_temporal_analysis.py`

## Validation commands and exact results

Commands run:

```bash
cd "C:\Users\zathp\Documents\programming\TPCN"
python -m pytest -q tests/test_temporal_analysis.py tests/test_viewer_3d.py
python -m pytest -q tests/test_temporal_analysis.py tests/test_viewer_3d.py tests/test_cpu_visualization.py tests/test_visualization.py tests/test_luna12b_integration.py tests/test_luna28_excursion_structural_growth.py
python -m pytest -q -rs
python -m pytest --collect-only -q
python -m compileall -q tpcn tests
git diff --check
```

Observed results:

- Focused consumer suite (`test_temporal_analysis.py`, `test_viewer_3d.py`):
  **19 passed**.
- Combined focused suite (the six listed files): **108 passed**.
- Full suite (`python -m pytest -q -rs`): **896 passed, 11 failed, 1 skipped**
  (**908 collected**, 11.96s).
- Collection (`python -m pytest --collect-only -q`): **908 tests collected**.
- Compile (`python -m compileall -q tpcn tests`): **PASS**.
- Pylance/repository diagnostics on all four changed Python/test files:
  **PASS — no errors found** in `viewer_3d.py`, `temporal_analysis.py`,
  `test_viewer_3d.py`, and `test_temporal_analysis.py`.
- `git diff --check`: **PASS**.
- Direct accounting probe returned `duplicate=2`, `fan_in_full=1`,
  `accepted=1`, `growth_attempts=4`.
- No tests were deleted, no xfail conversion or unconditional skip was added,
  and no tests were deselected. The Luna-30 test migrations retained equivalent
  behaviors while net adding tests; collection is 908 versus the pre-Luna-30
  baseline of 898.

## Full-suite failure reconciliation

Every remaining failure is in the expected unrelated historical groups:

| Test/module group | Count | Classification | Luna-30 path changed? | Why not a Luna-30 regression |
|---|---:|---|---|---|
| `tests/test_luna12e_integration.py::test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes` | 1 | Historical Luna-12E failure | No | Fails because adding the edge does not change prediction loss; the test and experiment computation are outside this replay-consumer correction. |
| `tests/test_luna12e_integration.py::test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` | 1 | Historical Luna-12E failure | No | Fails on the expected clock timestamp reset; neuron runtime and experiment reset semantics are untouched. |
| `tests/test_luna12l_temporal_scale.py` (the eight failures listed below) | 8 | Historical Luna-12L failures | No | Existing structural-plasticity configurations fail the `ExperimentConfig` structural-observation guard. Neither Luna-12L nor experiment configuration/execution code is changed. |
| `tests/test_spiral_benchmark.py::test_control_results_are_deterministic_and_include_required_order_controls` | 1 | Historical spiral benchmark failure | No | Fails when a structural-plasticity config omits structural observation; spiral benchmark and experiment execution are untouched. |

The eight Luna-12L failures are:

- `test_scale_runner_retains_all_policies_and_causal_evidence`
- `test_requested_policy_is_executed_by_classifier[baseline]`
- `test_requested_policy_is_executed_by_classifier[random]`
- `test_requested_policy_is_executed_by_classifier[temporal]`
- `test_requested_policy_is_executed_by_classifier[reversed]`
- `test_policy_changes_classifier_execution_state`
- `test_policy_scale_cross_product_preserves_provenance_and_serialization`
- `test_condition_fails_on_classifier_provenance_mismatch`

There are zero temporal-analysis failures, zero 3D-viewer failures, and zero
new applicable regressions. The full suite exactly reconciles with the
expected historical groups: 2 Luna-12E, 8 Luna-12L, and 1 spiral.

## Architecture clause audit

- A01: analysis and viewer remain downstream-only; no clock or backpressure introduced.
- A04: replay and viewer state remain bounded and deterministic.
- A06: prediction/error computation is untouched.
- A07: no labels or task outcomes are promoted into structural evidence.
- A08: deterministic replay/view histories are retained; synthetic removal is explicitly replay-only display evidence.
- A10: metrics remain descriptive and non-causal.
- A14: accepted ACP-0007 scope is preserved; no E2 pruning promotion.
- A15: software replay only; no hardware-equivalence claim.

Additional scope verdicts:

- ACP required: **NO**.
- TPCV schema change: **NO**.
- Architecture change: **NO**.
- E2 pruning: **NOT AUTHORIZED**.
- ACP-0002 N3: **NOT AUTHORIZED**.
- Replay consumer compatibility: **ESTABLISHED**.
- Task efficacy: **NOT ESTABLISHED**.
- Resource benefit: **NOT ESTABLISHED**.

## Assumptions and limitations

- The issue is confined to downstream compatibility between TPCV-2 canonical records and replay consumers.
- TPCV-2 continues to intentionally omit scalar activation.
- This work does not claim new causal or efficacy behavior for structural growth or route usage.

## Revision provenance

- Contract version: **1.2**.
- Authorization source revision: `727a00aed08a4ba2c7194a70cde603f60ab35065`.
- Authorization publication revision: `4013bfb15fe01acf9df6d7de7c0a2e7f50847d8b`.
- Initial implementation revision: `6fdc363e788c11f9738ffb7dd02f0bc51749aeaa`.
- Corrective implementation revision: `9b9d97326c8c822dc2608a8237e64fe852296f84`.
- Handoff publication revision: to be recorded after the separate handoff commit.
- Final `origin/main`: to be verified and reported after publication.

Corrective-pass final diff audit found only `tpcn/temporal_analysis.py` and
`tests/test_temporal_analysis.py` changed. The required terminal push check
will confirm `HEAD == origin/main` and a clean worktree.
