---
name: Luna-30 TPCV-2 Replay Consumer Compatibility Correction
description: Correct TPCV-2 optional activation projection in the detached viewer and migrate temporal-analysis/viewer tests to deterministic replay fixtures.
---

# Luna-30 — TPCV-2 Replay Consumer Compatibility Correction

## Authorization and baseline

Luna-30 is **AUTHORIZED / NOT EXECUTED** for the bounded downstream
compatibility correction and focused verification described here.

Authorization began on clean synchronized `main` at
`727a00aed08a4ba2c7194a70cde603f60ab35065`
(`docs: classify replay consumer compatibility blockers`). The review and
scope decision are recorded in
`workflow/handoffs/luna-0-post-luna29-replay-consumer-compatibility-decision-20261004.md`;
the authorization is recorded in
`workflow/handoffs/luna-0-authorization-luna-30-tpcv2-replay-consumer-compatibility-20261004.md`.
Before editing, verify the branch is `main`, `HEAD == origin/main`, and the
worktree is clean. The exact baseline must be an ancestor of `HEAD`. If
production, tests, ACP, architecture-contract text, or unrelated architecture
semantics have changed since that baseline, stop and return to Luna-0 for
reconciliation.

Closed prerequisites remain:

- ACP-0007: **ACCEPTED**.
- Architecture Contract: **1.2**, unchanged.
- Luna-28 and Luna-29: **CLOSED / INDEPENDENTLY VERIFIED**.
- EXCURSION_V1 fixed topology remains the ordinary default.
- E2 structural growth remains explicit opt-in.
- E2 pruning and ACP-0002 N3 remain **NOT AUTHORIZED**.
- TPCV-2 remains the canonical downstream EXCURSION_V1 observation schema.

This is a downstream compatibility correction, not an ACP-0007 defect,
Luna-29 defect, TPCV-2 schema defect, or architecture change. No ACP is
required.

Mandatory sequence: `Luna-0 authorization -> Luna-30 -> Luna-0 independent
review`. Do not execute this contract during authorization.

## Verified defect and semantic decision

The canonical TPCV-2 `ExcursionNeuronRecord` exposes `neuron_id`, `active`,
`mode`, `state`, `pending_internal_work`, `processed_events`, and optional
`position`. It intentionally has no scalar `activation`; activation is not
defined for EXCURSION_V1. The Luna-0 review reproduced valid TPCV-2 records
raising `AttributeError` in both `VisualizationScene.nodes()` and
`VisualizationScene.inspect()` because the viewer reads `.activation`.

Correct only the downstream compatibility projection:

- `NodeView.activation` is `float | None`.
- TPCV-1 `NeuronRecord` projects its exact recorded float activation.
- TPCV-2 `ExcursionNeuronRecord` projects `None`.
- `VisualizationScene.inspect()["activation"]` follows the same mapping.
- Never synthesize TPCV-2 activation from `state`, `active`, `mode`, payload,
  or processed-event counts. In particular, do not map `active` to `0.0/1.0`.
- TPCV-2 activity filtering continues to use the canonical `record.active`.
- Keep `mode`, `pending_internal_work`, and other meanings unchanged; no new
  viewer mode/UI is required.

The `tpcn.temporal_analysis` algorithms remain replay-only, descriptive, and
non-causal. Update only TPCV-1-specific limitation wording to version-neutral
wording, preserving the fact that edge use is unavailable without per-edge
routed-event identity. Do not infer use from edge existence or add event-use
data.

## Objective

1. Make the detached viewer consume valid TPCV-2 records without accessing a
   nonexistent scalar activation, while preserving exact TPCV-1 activation.
2. Migrate the three temporal-analysis and three 3D-viewer tests from obsolete
   `run_cpu_training(..., structural_plasticity=True)` fixtures to deterministic
   detached replay sequences with explicit records and metric timelines.
3. Preserve descriptive analysis/comparison behavior, deterministic layout,
   selection/inspection, neighborhood and active-only filters, metrics,
   playback/camera controls, edge addition display, and generic removal
   highlights.
4. Keep replay removal provenance explicitly synthetic and detached in the
   fixture. A replay edge's disappearance describes a snapshot difference; it
   is not evidence of an ACP-0007 E2 pruning event.

The consumers do not need live structural training to validate their offline
behavior. Luna-29 has already demonstrated a real ACP-0007-grown edge in
TPCV-2; Luna-30 need not rerun growth.

## Exact owned files

Luna-30 may edit only:

- `tpcn/viewer_3d.py` — TPCV-version-aware optional activation projection.
- `tpcn/temporal_analysis.py` — version-neutral capability-limit wording only.
- `tests/test_viewer_3d.py` — deterministic detached TPCV-2 consumer and
  compatibility tests.
- `tests/test_temporal_analysis.py` — deterministic detached replay and
  explicit metrics tests.
- `workflow/handoffs/luna-30-tpcv2-replay-consumer-compatibility-20261004.md`
  — completion evidence.

If a required correction needs any other file, stop and return to Luna-0;
do not expand this assignment.

## Prohibited files and behavior

Do not modify:

- `tpcn/visualization.py` or any TPCV schema/codec or add TPCV-3.
- `tpcn/cpu_visualization.py` or reopen the Luna-29 helper.
- `tpcn/experiments.py`, `tpcn/structural_observation.py`,
  `tpcn/temporal_association.py`, `tpcn/structural_plasticity.py`,
  `tpcn/topology.py`, or `tpcn/excursion_neuron.py`.
- `Main.py`, `viz_tpcn_3d.py`, the CPU CLI, GPU/FPGA/FPAA code, or hardware
  interfaces.
- Luna-12L, spiral, or Luna-12E source or tests.
- Any other production code, tests, architecture documents, or public API.

Do not enable or implement E2 pruning, change topology persistence, add
structural evidence, alter event timing, feed viewer/analysis state into
computation, claim task/resource efficacy, or make hardware-equivalence
claims. Do not alter TPCV-1 activation semantics or synthesize scalar
activation for TPCV-2.

## Required fixture and test behavior

Use canonical `ExcursionNeuronRecord`, `ConnectionRecord`, and
`VisualizationSnapshot` values encoded as valid TPCV-2 records inside a
bounded `ReplaySequence`. Include multiple snapshots with deterministic
activity, processed-event, metric, and topology changes. The viewer replay
may use:

- Snapshot 0: baseline edge set.
- Snapshot 1: one added edge.
- Snapshot 2: a previously present edge absent.

Explicitly identify the removal as **synthetic detached replay evidence**
for display behavior. It is not E2 pruning evidence. No live training or
structural-learning assertion is needed.

Cover, using repository naming conventions:

- A valid canonical TPCV-2 record passes through `VisualizationScene.nodes()`
  and `inspect()` without error.
- For TPCV-2, activation is `None`, while node/inspection `active`, `state`,
  and `processed_events` equal the canonical record.
- An adversarial active TPCV-2 record with nontrivial state and active mode
  still projects activation as `None`; no scalar surrogate is synthesized.
- TPCV-1 retains the exact recorded float activation in `NodeView` and
  inspection.
- TPCV-2 active-only filtering uses `active`.
- Deterministic layout, nodes, digest, selection, neighborhood, inspection,
  metrics synchronization, playback stepping/seek, play/pause/speed, and
  camera controls work from detached TPCV-2 replay.
- Topology additions are displayed; generic snapshot-difference removals
  are highlighted; bounded scene history remains enforced. Tests and handoff
  must not call the removal an E2 prune.
- Temporal analysis classifies an explicit supplied metric trend and known
  topology change, aggregates explicitly supplied rejection reasons, and
  compares two detached replays with raw deltas without causation or
  superiority claims.
- Per-edge use stays unavailable without event-path evidence.
- Malformed replay validation remains covered.

At minimum cover the following behaviors (test names may follow the current
repository style):

```text
test_tpcv2_scene_nodes_do_not_require_scalar_activation
test_tpcv2_nodeview_activation_is_absent_or_none
test_tpcv2_inspect_activation_is_absent_or_none
test_tpcv1_viewer_preserves_scalar_activation
test_tpcv2_active_filter_uses_active_field
test_tpcv2_layout_is_deterministic
test_tpcv2_selection_and_neighborhood_work
test_tpcv2_metrics_remain_synchronized
test_tpcv2_topology_addition_is_displayed
test_generic_replay_removal_is_highlighted
test_generic_removal_does_not_claim_e2_pruning
test_temporal_analysis_classifies_explicit_supplied_metric_trend
test_temporal_analysis_aggregates_explicit_rejection_reasons
test_compare_replays_reports_raw_deltas_without_causal_claim
test_edge_usage_remains_unavailable_without_event-path-evidence
```

## Required pre/post validation

Record the pre-correction direct valid-record probe and its `AttributeError`
in the completion handoff. The Luna-0 blocked review already records the
pre-migration consumer pytest state: **6 failed, 3 passed**, with all six
blocked first by the intentional missing-observation guard. Do not bypass
that guard to establish pre-correction downstream behavior.

After correction, run:

```text
python -m pytest -q tests/test_temporal_analysis.py tests/test_viewer_3d.py
python -m pytest -q tests/test_cpu_visualization.py tests/test_visualization.py
python -m pytest -q tests/test_luna12b_integration.py tests/test_luna28_excursion_structural_growth.py
```

All assigned consumer tests must pass. No TPCV, Luna-28, or Luna-29 regression
is permitted. Also run a combined focused suite containing all six files
above and record the exact count.

Run full suite:

```text
python -m pytest -q -rs
```

Baseline before Luna-30 was 880 passed, 17 failed, 1 skipped, 898 collected.
Expected unrelated historical groups are Luna-12E (2), Luna-12L (8), and
spiral (1), for 11 remaining failures. Do not hard-code a new pass total;
require zero temporal-analysis failures, zero viewer failures, and no new
applicable regression. Reconcile actual full-suite results explicitly.

Run collection and static checks:

```text
python -m pytest --collect-only -q
python -m compileall -q tpcn tests
git diff --check
```

Confirm that no tests were deleted, xfailed, skipped, or deselected to
manufacture a pass. Run Pylance/diagnostics on all four changed Python and
test files.

## Architecture and completion boundary

Audit and report A01, A04, A06, A07, A08, A10, A14, and A15:

- A01: analysis and viewer remain downstream-only; no clock or backpressure.
- A04: replay and viewer state remain bounded.
- A06: prediction/error computation is untouched.
- A07: no labels/task outcomes become structural evidence.
- A08: deterministic replay/view state and bounded histories are preserved.
- A10: descriptive metrics only; no efficacy claim.
- A14: accepted ACP-0007 scope preserved; no E2 pruning promotion.
- A15: software replay only; no hardware-equivalence claim.

ACP required: **NO**. TPCV schema change: **NO**. Architecture change:
**NO**.

Return a completed handoff to Luna-0 with files changed, exact revision,
commands/environment/results, direct repro and corrected behavior, test
failure reconciliation, clause audit, assumptions, and limitations. Luna-30
does not independently close itself; Luna-0 must review the completion
evidence. Do not authorize or execute a successor.
