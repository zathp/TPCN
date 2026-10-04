# Luna-26 Corrective Completion Handoff — Route-Path No-Revisit

```yaml
tpcn_handoff:
  agent: "Luna-26"
  luna_identifier: "Luna-26"
  descriptive_name: "ACP-0006 prediction-error route-path no-revisit correction"
  task_id: "luna-26-corrective-route-path-20261003"
  component: "BoundedTopology destination exclusion for opaque prediction-error forwarding"
  status: "PASS — IMPLEMENTED / INDEPENDENTLY VERIFIED / CLOSED"
  contract_version: "ACP-0006 1.1 (unchanged)"
  branch: "main"
  starting_revision: "f63e59552bf1f18b8cf1137abdf331f3aa8056f4"
  starting_origin_main: "f63e59552bf1f18b8cf1137abdf331f3aa8056f4"
  starting_worktree: "clean"
  implementation_revision: "8a14681fe6a770e75136227c5059bc9c76ae5d46"
  authorization: "workflow/handoffs/luna-0-authorization-luna-26-corrective-route-path-20261003.md"
  independent_review: "workflow/handoffs/luna-0-independent-review-luna-26-prediction-error-routing-20261003.md"
  files_changed:
    - "tpcn/topology.py"
    - "tpcn/experiment_excursion_runtime.py"
    - "tests/test_topology.py"
    - "tests/test_excursion_integration.py"
    - "workflow/handoffs/luna-26-corrective-route-path-20261003.md"
  architecture_change: false
  acp_or_a01_a15_changed: false
  luna22_status: "PASS — bounded ACP-0006 first CPU software-reference integration independently verified / closed"
  independent_review_pending: false
```

## Authorization and implementation boundary

The working checkout was verified before edits as clean `main`, with both
`HEAD` and `origin/main` exactly
`f63e59552bf1f18b8cf1137abdf331f3aa8056f4`. The corrective authorization and
its Luna-26 agent section were read before implementation. The authorization
permits the topology API extension notwithstanding the earlier owned-file
list; no other source or governance files were changed.

`BoundedTopology.route()` now accepts optional keyword-only
`exclude_destinations: Iterable[str] = ()`. It filters only edges whose
destination is in that call's exclusion collection, preserving topology
insertion order for remaining edges. Filtering happens before route-capacity
and event-queue preflight and before any push; the existing complete-fan-out
atomic admission remains intact. The default empty exclusion keeps existing
callers' route behavior unchanged.

Only `_deliver_prediction_error()` supplies the arriving
`RouteContext.route_path`. Numeric signal/excursion transformation and every
other route caller remain unchanged. No global visited set was added. The
per-`(prediction_id, destination)` delivery guard remains in place for
convergence and character reset.

## Regression evidence

Before changing production code, the corrective regression command was run
against the exact starting checkout:

```text
python -m pytest -q \
  tests/test_topology.py::test_route_excludes_only_visited_destinations_before_atomic_admission \
  tests/test_topology.py::test_excluded_destination_does_not_consume_sequence_or_break_capacity_atomicity \
  tests/test_excursion_integration.py::test_integrated_prediction_error_excludes_cycle_return_and_keeps_legal_fanout
```

**RED as required:** 3 failed. The topology tests reported that baseline
`route()` did not accept `exclude_destinations`; the integrated actual-error
case observed the prohibited `n1 -> n0` arrival at `1.65` in addition to the
legal `n1 -> n2` fan-out. This reproduces the authorization-baseline defect.

After the correction, the same regression cases pass as part of the focused
suite. The cycle-plus-fan-out integration case creates its prediction from a
configured-source E2 `ExcursionEmission`, admits the later target scalar at
the same input port, and verifies a nonzero matched mismatch. The route trace
is `n0 -> n0 @ 1.00`, `n0 -> n1 @ 1.25`, and `n1 -> n2 @ 1.85`; the cycle
return to `n0` is never queued. The legal sibling still arrives.

The focused controls verify:

- **API/default compatibility:** existing unfiltered route tests continue to
  pass; filtering removes only visited destinations and retains the other
  fan-out in deterministic edge order.
- **No excluded-edge queue work:** an all-excluded route returns no events;
  the next legal queue push receives sequence 0. The route observer sees
  only admitted legal edges.
- **Capacity atomicity:** preflight checks only the post-exclusion legal
  fan-out. If that fan-out cannot fit, the existing queue, sequence high-water,
  and event admission remain unchanged.
- **Path and timing:** one-hop and two-hop delivery use directed edges and
  cumulative unequal finite delays; the back-edge-plus-legal-sibling case
  verifies no repeated node, and route depths remain below network node count.
- **Identity and opacity:** all tested hops retain the same
  `PredictionError` payload and its prediction ID, signed error, prediction
  and observation values/timestamps, observation source, event ID, lineage,
  causal roots, and truncation state. Non-identity Model-B parameters do not
  transform the metadata.
- **Isolation/accounting:** error events are delivered to local ledgers and
  not to `MultiExcursionNeuron.receive_event()`. The cycle regression checks
  that error cost equals the accepted local consumers and edge-transfer cost
  equals the actually routed trace events. An instrumented sidecar attachment
  check observes only the root, `n1`, and `n2` error arrivals; the excluded
  back-edge has no sidecar, trace arrival, or edge/error charge.
- **Convergence/reset:** equal-time diamond arrivals retain deterministic
  sequence ordering and distinct legal paths to the shared node. The existing
  destination guard applies local error once at convergence and allows only
  one continuation to the downstream node. Character reset clears the guard.
- **Causality and bounded state:** prediction/error generation remains from
  admitted inputs only. Existing label-isolation, future-input ordering,
  queue/event budgets, settling/reset, and provenance-bound tests remain
  active and pass.

## Validation

### Passed

| Command/check | Result |
|---|---|
| Three corrective regressions against starting checkout | **3 failed as expected** before implementation |
| `python -m pytest -q tests/test_topology.py tests/test_excursion_integration.py` | **60 passed** |
| `python -m pytest -q tests/test_experiments.py tests/test_excursion_integration.py` | **14 passed** |
| Prescribed ACP-0006 regression set: `tests/test_experiments.py`, `test_excursion_neuron.py`, `test_e2_multi_excursion.py`, `test_event_runtime.py`, `test_topology.py`, `test_predictive_coding.py`, `test_eligibility.py`, `test_streaming_classifier.py`, `test_energy_utility.py`, `test_ir2.py`, `test_e2_ir2.py`, `test_stroke_dataset.py`, and `test_excursion_integration.py` | **342 passed** |
| `python -m pytest -q tests/test_excursion_integration.py::test_integrated_delayed_credit tests/test_eligibility.py` | **61 passed** |
| `python -m pytest --collect-only -q` | **829 collected** |
| `python -m compileall -q tpcn tests` | **Passed** |
| Diagnostics for `tpcn/topology.py`, `tpcn/experiment_excursion_runtime.py`, `tests/test_topology.py`, and `tests/test_excursion_integration.py` | **No errors found** |
| `git diff --check` | **Passed** |

### Failed — known downstream suite incompatibilities, not changed here

`python -m pytest -q -rs` and the identity-only rerun both report **24 failed,
804 passed, 1 skipped**. The failures are outside the authorized files and
match the already documented downstream consumer groups. They were not
repaired or treated as routing regressions.

| Group | Count and failing test identities | Classification |
|---|---|---|
| `tests/test_cpu_visualization.py` | 3: `test_capture_modes_do_not_change_training_result`; `test_snapshot_sequence_is_deterministic_and_replays_offline`; `test_replay_rejects_missing_malformed_and_over_limit_data` | Visualization consumer assumes legacy neuron activation observables absent from the excursion neuron. |
| `tests/test_luna12b_integration.py` | 4: `test_structural_run_is_deterministic_and_has_real_bounded_mutations`; `test_capture_is_downstream_only_for_structural_decisions`; `test_controls_report_behavior_and_topology_without_assuming_benefit`; `test_structural_evidence_is_label_isolated` | Structural experiments request plasticity unavailable in the fixed-topology excursion integration. |
| `tests/test_luna12e_integration.py` | 2: `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`; `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` | Existing experiment consumer expects legacy activation/classifier observables. |
| `tests/test_luna12l_temporal_scale.py` | 8: `test_scale_runner_retains_all_policies_and_causal_evidence`; `test_requested_policy_is_executed_by_classifier[baseline]`; `[random]`; `[temporal]`; `[reversed]`; `test_policy_changes_classifier_execution_state`; `test_policy_scale_cross_product_preserves_provenance_and_serialization`; `test_condition_fails_on_classifier_provenance_mismatch` | Policy/scale consumers expect legacy classifier execution and matching provenance/configuration. |
| `tests/test_spiral_benchmark.py` | 1: `test_control_results_are_deterministic_and_include_required_order_controls` | Existing benchmark control assumes legacy downstream observables. |
| `tests/test_temporal_analysis.py` | 3: `test_flat_metrics_and_changing_topology_are_reported`; `test_rejection_reason_aggregation_preserves_observed_reasons`; `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` | Analysis fixtures assume legacy scalar activation or topology/metric semantics. |
| `tests/test_viewer_3d.py` | 3: `test_layout_and_scene_generation_are_deterministic_and_diagnostic`; `test_topology_deltas_and_bounded_prune_highlights`; `test_playback_filters_selection_neighborhood_and_metrics` | Viewer fixtures construct downstream records from legacy neuron activation and topology observables. |

### Not run

- A hardware implementation, hardware equivalence, or physical-energy
  calibration; none is authorized by this correction.
- A new dataset benchmark, efficacy study, or full UCI re-evaluation; none is
  in scope.

### Not applicable

- ACP/A01-A15 amendment, predictor/error/eligibility/reward redesign,
  downstream-consumer migration, or broader topology redesign.
- The 1 skipped full-suite test is `tests/test_gpu_visualization.py:61`
  (`CUDA is unavailable`); GPU validation is not applicable to this CPU
  software-reference correction.

## Independent review and closure

The optional per-call exclusion was sufficient within the authorized topology
API and integration boundary. No scope expansion was required. Luna-0
independently reviewed this corrective implementation and closed Luna-26 for
the bounded route-path correction. Luna-22 is also closed only for the
accepted first fixed-topology `EXCURSION_V1` CPU software-reference
integration. This does not establish task efficacy, useful delayed-credit
learning, downstream migration, or hardware equivalence. See
`workflow/handoffs/luna-0-independent-review-luna-26-prediction-error-routing-20261003.md`
for the complete review and explicitly bounded closure decision.
