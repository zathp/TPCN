# Luna-23 Completion Handoff - E2 Logical-Time Representability

```yaml
tpcn_handoff:
  agent: "Luna-23"
  luna_identifier: "Luna-23"
  descriptive_name: "ACP-0004 E2 logical-time representability correction"
  task_id: "luna-23-e2-time-representability-20261003"
  component: "MultiExcursionNeuron analytic S_REARM scheduling"
  status: "implementation and verification complete; awaiting Luna-0 independent review"
  contract_version: "1.1"
  branch: "main"
  starting_revision: "3ec3c4a7991c28f59e1419c9f3656267efed2875"
  implementation_revision: "4c1efd6c31aed86748dcacf596401579c2b94bc8"
  handoff_publication_revision: "pending; this value will be finalized after initial publication"
  dependencies:
    - "Accepted ACP-0004 E2 / Luna-21"
    - "Luna-0 second independent review of Luna-22"
    - "Luna-0 authorization for Luna-23"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/excursion_neuron.py"
    - "tests/test_e2_multi_excursion.py"
    - "workflow/handoffs/luna-23-e2-time-representability-20261003.md"
  terminal_verdict: "PASS — LUNA-23 E2 LOGICAL-TIME REPRESENTABILITY CORRECTION READY FOR INDEPENDENT REVIEW"
```

## Baseline and worktree

- Fetched `origin` before editing; `main` and `origin/main` both pointed to
  `3ec3c4a7991c28f59e1419c9f3656267efed2875` (`docs: correct Luna-22 review publication SHA`).
- The worktree was clean at that starting revision.
- The authorized lineage was present: Luna-22 `a206f2e8`, Luna-0 review
  `F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb`, and publication
  reconciliation `188e00bb`; current `main` is the corrected reference commit.
- Implementation is commit `4c1efd6c31aed86748dcacf596401579c2b94bc8`.
- Handoff publication revision will be recorded in the final handoff metadata
  update. The implementation and handoff are intended for Luna-0 verification.

## Reproduced values and correction

The focused regression executes the pending-event path into the real
`_finish_rearm()` transition with both polarities. For the independently
observed negative state:

```text
clock                  = 45.27906122689938
x                      = -0.2500000000000003
theta_r                = 0.25
decay_rate             = 1.0
analytic_delay         = 1.110223024625156e-15
raw clock + delay      = 45.27906122689938
next representable time= 45.27906122689939
stored due time        = 45.27906122689939
```

The positive-polarity counterpart, `x = 0.2500000000000003`, produces the same
positive analytic delay and stored due time.

Only E2 `S_REARM` scheduling may use the fallback, and only when the current
state is above `theta_r`, the analytic delay is finite and positive, and its
sum rounds exactly to the current timestamp. The stored time is
`math.nextafter(current_time, math.inf)`, then goes through the existing
finite/strict-future validation and pending-event creation path. Other
non-future E2 timestamps remain rejected. In particular, configured `M_EMIT`
and `M_REARM` delays receive no representability fallback.

The finite-return fixture processes timestamps
`[45.27906122689938, 45.27906122689939]`, verifies strict increase, and
terminates in two processed events with no pending event. Positive and
negative finite-return bounds and the multiple-emission identity/spacing
control also pass. The existing configured-delay negative control still
rejects the smallest positive subnormal `m_emit_delay` at initial time `1e308`.

The IEEE-754 `nextafter` operation is only a software-reference timestamp
representation mechanism. The intended behavior remains a finite positive
logical return delay with strict-future event ordering. No floating-point ULP
rule is proposed as canonical hardware behavior, and no hardware-equivalence
claim is made.

## Verification

| Validation | Result |
|---|---|
| Focused E2 file, `tests/test_e2_multi_excursion.py` | **42 passed** |
| Exact-boundary positive/negative test | **2 passed**; deterministic, strictly future, finite, bounded |
| Existing configured unrepresentable-delay rejection | **Passed** within the focused E2 suite |
| E1, E2, E2 IR-2 and IR-2 suites | **203 passed** |
| Luna-22 prescribed integration regression set | **320 passed** |
| Four-class non-structural `test_labels_do_not_change_canonical_four_class_trace` | **Passed** |
| Spiral non-structural label-invariance test | **Passed** |
| Full CPU suite, `pytest -q -rs` | **24 failed, 775 passed, 1 skipped** (CUDA unavailable) |
| `compileall -q tpcn tests` | **Passed** |
| Pylance diagnostics for the two changed Python files | **No diagnostics** |
| `git diff --check` | **Passed** |

### Representability failures removed

The seven failures attributed to the defect in the Luna-0 review no longer
fail from `E2 internal events require a finite positive logical delay`:

1. `test_labels_do_not_change_canonical_four_class_trace` now passes.
2. `test_scale_runner_retains_all_policies_and_causal_evidence` proceeds beyond
   the E2 return and reaches the separately known structural/default-model
   rejection.
3. `test_requested_policy_is_executed_by_classifier[fixed]` now passes.
4. `test_policy_changes_classifier_execution_state` proceeds beyond the E2
   return and reaches the separately known structural/default-model rejection.
5. `test_requested_scale_reaches_classifier_configuration` now passes.
6. `test_policy_scale_cross_product_preserves_provenance_and_serialization`
   proceeds beyond the E2 return and reaches the separately known
   structural/default-model rejection.
7. `test_control_results_are_deterministic_and_include_required_order_controls`
   proceeds beyond the E2 no-learning path and reaches the separately known
   structural/default-model rejection.

Thus all seven E2 representability exceptions are removed; three tests now
pass outright, while four expose later out-of-scope structural/default-model
failures. The four are not reported as passing.

### Remaining full-suite failures

The full suite has 24 failures, classified against the Luna-0 review:

| Group | Remaining failed test identities | Remaining cause |
|---|---|---|
| `tests/test_cpu_visualization.py` (3) | `test_capture_modes_do_not_change_training_result`; `test_snapshot_sequence_is_deterministic_and_replays_offline`; `test_replay_rejects_missing_malformed_and_over_limit_data` | TPCV-1 scalar `.activation` assumptions are incompatible with `MultiExcursionNeuron`. |
| `tests/test_luna12b_integration.py` (4) | `test_structural_run_is_deterministic_and_has_real_bounded_mutations`; `test_capture_is_downstream_only_for_structural_decisions`; `test_controls_report_behavior_and_topology_without_assuming_benefit`; `test_structural_evidence_is_label_isolated` | Structural-plasticity consumers conflict with fixed `EXCURSION_V1` integration. |
| `tests/test_luna12e_integration.py` (2) | `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`; `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` | Legacy prediction-loss and reset-time observable assumptions. |
| `tests/test_luna12l_temporal_scale.py` (8) | `test_scale_runner_retains_all_policies_and_causal_evidence`; `test_requested_policy_is_executed_by_classifier[baseline]`; `[random]`; `[temporal]`; `[reversed]`; `test_policy_changes_classifier_execution_state`; `test_policy_scale_cross_product_preserves_provenance_and_serialization`; `test_condition_fails_on_classifier_provenance_mismatch` | Structural/default-model setup failures under `EXCURSION_V1`; the first and last also no longer fail at the E2 representability boundary. |
| `tests/test_spiral_benchmark.py` (1) | `test_control_results_are_deterministic_and_include_required_order_controls` | Its later structural control requests unavailable structural plasticity after the E2 no-learning control completes. |
| `tests/test_temporal_analysis.py` (3) | `test_flat_metrics_and_changing_topology_are_reported`; `test_rejection_reason_aggregation_preserves_observed_reasons`; `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` | Replay fixtures use the structural CPU experiment path rejected by `EXCURSION_V1`. |
| `tests/test_viewer_3d.py` (3) | `test_layout_and_scene_generation_are_deterministic_and_diagnostic`; `test_topology_deltas_and_bounded_prune_highlights`; `test_playback_filters_selection_neighborhood_and_metrics` | Viewer fixtures request structural CPU training rejected by `EXCURSION_V1`. |

These categories total 24 and are not corrected by Luna-23. Luna-24's IR-2
startup provenance issue and dataset reproducibility remain unresolved and
were not edited or executed as work items.

## Architecture audit

| Clause | Disposition |
|---|---|
| A01 — Event-driven computation | **Preserved.** Work remains triggered by pending internal events; no global neural clock was added. |
| A02 — Local time | **Corrected at the representation boundary.** Analytic decay remains local; the due timestamp is strictly later. |
| A03 — Finite propagation | **Strict-future ordering restored** for the valid positive analytic return case; no same-time transition is created. |
| A08 — Bounded dynamics | **Preserved.** Existing event budget remains in force; the positive/negative regression returns in two processed events. |
| A15 — Hardware independence | **Preserved as a semantic requirement.** `nextafter` is explicitly software-float-specific; no hardware equivalence is claimed. |

A01-A15 text, E2 state transitions, E1 source behavior, event identity,
generation validation, and standalone IR-2 schema/runtime behavior are
unchanged. The only runtime change is E2 strict-future representation of an
otherwise valid analytic `S_REARM`.

## Status and stop boundary

- **Passed:** bounded E2 correction; focused positive/negative boundary;
  finite return and identity controls; E1/E2/IR-2 references; prescribed
  integration set; label invariance; compilation, diagnostics and diff check.
- **Failed:** full CPU suite remains at 24 out-of-scope failures listed above.
- **Not run:** hardware/backend validation; independent Luna-0 review.
- **Not applicable:** downstream consumer migration, Luna-24 changes, dataset
  reproduction and hardware-equivalence claims.

**Terminal verdict: PASS — LUNA-23 E2 LOGICAL-TIME REPRESENTABILITY CORRECTION
READY FOR INDEPENDENT REVIEW.**

Stop here and return this handoff to Luna-0. Do not execute Luna-24, migrate
consumers, or close Luna-22.
