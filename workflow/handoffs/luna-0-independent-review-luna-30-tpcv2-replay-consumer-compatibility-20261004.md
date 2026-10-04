---
tpcn_handoff:
  agent: Luna-0
  luna_identifier: Luna-0
  descriptive_name: Independent review of Luna-30 TPCV-2 replay consumer compatibility
  task_id: luna-0-independent-review-luna-30-tpcv2-replay-consumer-compatibility-20261004
  component: Detached temporal analysis and 3D replay viewer
  status: complete
  contract_version: "1.2"
  branch: main
  review_starting_revision: 188dfd49fddc6702e86c56210f26455e6513050f
  authorization_source_revision: 727a00aed08a4ba2c7194a70cde603f60ab35065
  authorization_publication_revision: 4013bfb15fe01acf9df6d7de7c0a2e7f50847d8b
  initial_implementation_revision: 6fdc363e788c11f9738ffb7dd02f0bc51749aeaa
  corrective_implementation_revision: 9b9d97326c8c822dc2608a8237e64fe852296f84
  luna30_handoff_publication_revision: 7ec041fcadaa2015dd2bebf7b7f23ed48e5b745a
  final_pre_review_provenance_revision: 188dfd49fddc6702e86c56210f26455e6513050f
  classification: [INDEPENDENT VERIFICATION, ADVERSARIAL COMPATIBILITY AUDIT, GOVERNANCE CLOSURE]
  architecture_change: false
  proposal: null
  authorized_scope: TPCV-2 downstream replay viewer compatibility only
  successor_authorized: false
---

# Outcome

**PASS — LUNA-30 TPCV-2 REPLAY CONSUMER COMPATIBILITY CORRECTION
INDEPENDENTLY VERIFIED / CLOSED** for its exact downstream replay-consumer
scope. No production or test files were changed during this independent
review.

## Review baseline and provenance

The review began from clean synchronized `main`:

- Branch: `main`.
- `HEAD == origin/main == 188dfd49fddc6702e86c56210f26455e6513050f`.
- Subject: `docs: finalize Luna-30 publication provenance`.
- Worktree was clean.

All requested lineage links were verified as ancestors in order:

1. Authorization source / post-Luna-29 classification:
   `727a00aed08a4ba2c7194a70cde603f60ab35065`.
2. Luna-30 authorization publication:
   `4013bfb15fe01acf9df6d7de7c0a2e7f50847d8b`.
3. Initial Luna-30 implementation:
   `6fdc363e788c11f9738ffb7dd02f0bc51749aeaa`.
4. Bounded accounting correction:
   `9b9d97326c8c822dc2608a8237e64fe852296f84`.
5. Corrected completion-handoff publication:
   `7ec041fcadaa2015dd2bebf7b7f23ed48e5b745a`.
6. Final handoff provenance publication / pre-review revision:
   `188dfd49fddc6702e86c56210f26455e6513050f`.

Scope deltas:

- Authorization publication to initial implementation changed only
  `tpcn/viewer_3d.py`, `tpcn/temporal_analysis.py`,
  `tests/test_viewer_3d.py`, `tests/test_temporal_analysis.py`, and the
  Luna-30 completion handoff. All are Luna-30-owned paths.
- Initial implementation to bounded correction changed only
  `tpcn/temporal_analysis.py` and `tests/test_temporal_analysis.py`.
- The accounting edit restored the pre-Luna-30 accepted-addition semantics;
  it is not a newly authorized accounting behavior.
- Corrective implementation through the final pre-review revision changed
  only the completion handoff.
- No prohibited production, test, schema, experiment, topology, structural
  learning, CLI, GPU, FPGA, FPAA, or hardware path changed.

The initial implementation briefly contained an unauthorized accounting
interpretation. Its correction is explicit in the published completion
handoff and independently verified below; the final implementation does not
retain that defect.

## Canonical TPCV-2 record and optional activation audit

`ExcursionNeuronRecord` in `tpcn/visualization.py` contains `neuron_id`,
`active`, `mode`, `state`, `pending_internal_work`, `processed_events`, and
optional `position`. It intentionally has no scalar `activation`. TPCV-2
continues to describe EXCURSION_V1 observations without assigning scalar
activation semantics.

`VisualizationSnapshot` validates record classes against `format_version`;
normal replay construction parses bounded serialized snapshot bytes into
these version-specific canonical records. Therefore the viewer's optional
`getattr(record, "activation", None)` projection operates within the
validated replay boundary and does not make ordinary replay parsing accept
arbitrary record objects.

Independent adversarial probe results:

- `NodeView.activation` is `float | None`.
- TPCV-2 active record, `mode=M_ACTIVE`, `state=1.25`, and 12 processed
  events: `nodes()` returns activation `None`; `inspect()["activation"]`
  also returns `None`.
- No activation is derived from `active`, state, mode, pending work, or
  processed-event count.
- A canonical TPCV-1 record with activation `0.37` returns exactly `0.37`
  through both `nodes()` and `inspect()`.
- TPCV-2 `active_only` filtering selects from the canonical `active` field.
- **TPCV-2 scalar activation: ABSENT / None.**
- **TPCV-1 scalar activation: PRESERVED.**

## Detached viewer and topology-difference audit

Repeated byte-identical TPCV-2 replay produced identical diagnostic layout,
node projection, and replay digest. Independent exercise covered selection,
inspection, neighborhood, active-only filtering, epoch-synchronized metrics,
seek, step, first, last, playback tick, orbit, pan, zoom, and fit.

Adjacent detached snapshots established:

- Absent-to-present edge yields `SnapshotDiff.added_edges` and an `"added"`
  rendered edge.
- Present-to-absent edge yields `removed_edges` and a generic display
  highlight whose renderer label remains `"pruned"`.
- The latter is **GENERIC DETACHED SNAPSHOT REMOVAL**, not an E2 pruning
  event, not computational evidence, and not authority to implement pruning.

## Temporal-analysis audit

The final production delta in `tpcn/temporal_analysis.py` relative to the
authorization floor contains only:

- Version-neutral replay capability-limit wording, preserving the principle
  that topology existence is not per-edge routed-event use evidence.
- The bounded correction to restore the prior accepted-addition accounting
  semantics after the initial implementation scope defect.

No other analysis or classifier behavior was changed. The analyzer and viewer
consume detached `ReplaySequence` records and metrics and have no execution
path into `ExperimentRunner`, event queues, neurons, topology mutation,
structural evidence, prediction, reward, eligibility, or computation
backpressure.

### Accepted/rejection accounting

The recognized rejection counts remain separate from accepted additions:

- Explicit probe with `duplicate=2`, `fan_in_full=1`, and
  `accepted_additions=1` returned `duplicate=2`, `fan_in_full=1`,
  `accepted=1`, `growth_attempts=4`.
- Adversarial probe with
  `mutation_rejection_reasons["accepted"]=99` and no
  `accepted_additions` returned `accepted=0`, `growth_attempts=3`.
- Thus `accepted = sum(accepted_additions)`; an `"accepted"` rejection-map
  key is not accepted-growth evidence.

The migrated rejection fixture supplies `accepted_additions` separately from
`mutation_rejection_reasons`.

### Remaining replay-analysis semantics

- Limitations are version-neutral and state that replay does not carry
  routed per-edge event identity; edge existence cannot establish usage.
- For ordinary detached replay, `used_recently is None`,
  `used_frequently is None`, and `edge_use_evidence == "unavailable"`.
- The classifier fixture explicitly supplies topology changes and increasing
  accuracy; its “changing topology / improving behavior” result describes
  those supplied values and makes no TPCN efficacy claim.
- `compare_replays` returns raw `left`, `right`, and
  `delta_right_minus_left` values descriptively; it does not infer causation
  or superiority.
- Malformed replay input remains rejected.

## Independent validation

| Check | Independent result |
|---|---|
| `python -m pytest -q tests/test_temporal_analysis.py tests/test_viewer_3d.py` | **19 passed** |
| Combined temporal analysis, viewer, CPU visualization, visualization, Luna-12B, and Luna-28 tests | **108 passed** |
| `python -m pytest -q -rs` | **896 passed, 11 failed, 1 skipped** in 19.09s |
| `python -m pytest --collect-only -q` | **908 tests collected** |
| `python -m compileall -q tpcn tests` | **PASS** |
| Pylance/repository diagnostics on `tpcn/viewer_3d.py`, `tpcn/temporal_analysis.py`, `tests/test_viewer_3d.py`, and `tests/test_temporal_analysis.py` | **PASS — no errors found in all four files** |
| `git diff --check` at review baseline | **PASS** |

No tests were deleted or hidden from collection; no xfail conversion,
unconditional skip, or deselection was introduced. The three stale
viewer/analysis training fixtures were migrated to explicit detached replay
fixtures; test collection increased from the cited pre-Luna-30 898 to 908.
The one skip is the existing CUDA-unavailable GPU visualization test.

## Full-suite reconciliation

All 11 independent full-suite failures were enumerated and confirmed to be
outside Luna-30's changed source and test paths:

| Group | Count | Exact failure(s) | Classification |
|---|---:|---|---|
| Luna-12E (`tests/test_luna12e_integration.py`) | 2 | `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`; `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` | Historical prediction-loss delta expectation and final/reset clock timestamp expectation; runtime and tests were not changed. |
| Luna-12L (`tests/test_luna12l_temporal_scale.py`) | 8 | `test_scale_runner_retains_all_policies_and_causal_evidence`; `test_requested_policy_is_executed_by_classifier[baseline]`; `[random]`; `[temporal]`; `[reversed]`; `test_policy_changes_classifier_execution_state`; `test_policy_scale_cross_product_preserves_provenance_and_serialization`; `test_condition_fails_on_classifier_provenance_mismatch` | Historical structural-policy/configuration boundary; these cases fail at the explicit structural-observation validation guard. No Luna-12L/configuration source or test changed. |
| Spiral (`tests/test_spiral_benchmark.py`) | 1 | `test_control_results_are_deterministic_and_include_required_order_controls` | Historical structural configuration/policy consumer issue at the same structural-observation guard; spiral source/test unchanged. |

There were zero temporal-analysis failures, zero 3D-viewer failures, and zero
new applicable regressions. The 11 failures reconcile exactly to 2 Luna-12E,
8 Luna-12L, and 1 spiral. They were not repaired or migrated in this review.

## Architecture and governance audit

| Clause | Independent result |
|---|---|
| A01 | **PASS** — consumers remain downstream; no neural clock, execution timing, or backpressure added. |
| A04 | **PASS** — replay records and scene history, neighborhood depth, and edge rendering use existing finite bounds. |
| A06 | **PASS** — prediction/error computation is untouched. |
| A07 | **PASS** — supplied descriptive metrics do not become neural or structural inputs. |
| A08 | **PASS** — deterministic detached replay and bounded viewer history are preserved. |
| A10 | **PASS** — metrics remain descriptive and non-causal. |
| A14 | **PASS WITH ACP-0007 SCOPE** — no growth semantics changed or E2 pruning promoted. |
| A15 | **PASS FOR SOFTWARE REPLAY ONLY** — no hardware-equivalence claim or test. |

Additional status:

- ACP required: **NO**.
- TPCV schema change: **NO**.
- Architecture change: **NO**.
- ACP-0007: **UNCHANGED / ACCEPTED**.
- E2 pruning: **NOT AUTHORIZED**.
- ACP-0002 N3: **NOT AUTHORIZED**.
- Replay consumer compatibility: **ESTABLISHED**.
- Task efficacy: **NOT ESTABLISHED**.
- Resource benefit: **NOT ESTABLISHED**.
- Hardware equivalence: **NOT ESTABLISHED**.
- Luna-31 or any successor: **NOT AUTHORIZED**.

## Closure disposition

**CLOSED / INDEPENDENTLY VERIFIED** only for Luna-30's downstream
TPCV-2 replay-consumer compatibility scope:

- TPCV-2 viewer compatibility: **INDEPENDENTLY VERIFIED**.
- TPCV-2 activation: **None / no scalar semantics**.
- TPCV-1 activation: **PRESERVED**.
- Temporal-analysis accepted/rejection accounting:
  **RESTORED / VERIFIED**.
- TPCV schema and ACP-0007: **UNCHANGED**.
- E2 pruning: **NOT AUTHORIZED**.
- Task efficacy and resource benefit: **NOT ESTABLISHED**.
- Hardware equivalence: **NOT ESTABLISHED**.
- Successor authorization: **NO**.

Review publication is limited to this handoff and the governance-only
Luna-workflow and architecture-changelog closure entries. No production or
test files were modified by Luna-0.
