# Luna-26 — ACP-0006 Multi-Hop Prediction-Error Routing Correction

```yaml
tpcn_handoff:
  agent: "Luna-26 ACP-0006 Multi-Hop Prediction-Error Routing Correction"
  luna_identifier: "Luna-26"
  descriptive_name: "Correct integrated opaque prediction-error forwarding"
  task_id: "luna-26-prediction-error-multihop-routing-20261003"
  component: "ACP-0006 integrated prediction-error forwarding"
  status: "implemented and verified; returned for independent Luna-0 review"
  contract_version: "ACP-0006 1.1"
  branch: "main"
  base_revision: "e5d31236432ca5301ca5ca4ba8eb699006a55b09"
  implementation_revision: "9f2e5d98e9abfd3702eb55a4af76c41009872abc"
  dependencies:
    - "Luna-0 closure-readiness review and Luna-26 authorization"
    - "Accepted ACP-0006 rule 6"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "A forwarding anchor at the current destination permits bounded, opaque, deterministic hop-by-hop delivery using the unchanged BoundedTopology API."
  counter_hypothesis: "The adapter-only correction cannot preserve local delivery, identity, queue ordering, or per-destination idempotency."
  authorized_files:
    - "tpcn/experiment_excursion_runtime.py"
    - "tests/test_excursion_integration.py"
    - "workflow/handoffs/luna-26-prediction-error-multihop-routing-20261003.md"
  architecture_change: false
  proposal: null
  hardware_equivalence: "not claimed"
  luna22_status: "remains blocked pending independent Luna-0 review"
```

## Outcome

**PASS for the bounded Luna-26 correction.** The adapter now routes a matched
`PredictionError` from the current destination by constructing a fresh
forwarding anchor whose source is that destination. The event timestamp,
opaque payload, event ID and lineage ID are retained. The historical arriving
event is not mutated; the existing topology API still performs the ordinary
finite-delay routing and assigns queued sequence numbers.

No topology, neuron, predictor, eligibility, reward, dataset, ACP, A01-A15,
or downstream-consumer code or contract was changed. This handoff returns the
evidence to Luna-0; Luna-26 does not close Luna-22.

## Baseline and test-first evidence

- Checkout before editing: branch `main`, `HEAD == origin/main ==
  e5d31236432ca5301ca5ca4ba8eb699006a55b09`, clean worktree. This is the exact
  synchronized publication revision required by the authorization.
- Python: 3.11.5, system interpreter
  `C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe`.
- The actual integration fixture admits `1.2` at `t=0`, observes a configured
  source E2 emission and prediction of approximately `0.3` at `t=0.5`, then
  admits `0.4` at `t=1.0`. The resulting runtime-generated prediction error
  is nonzero (`+0.1`). No prediction error is fabricated by the fixture.
- Before the production change, the newly added real-error routing controls
  produced **4 failures and 1 pass**. The multi-hop path repeatedly routed
  from `n0` to `n1` instead of advancing from `n1` to `n2`; the diamond could
  not continue correctly after its first hop. The queue-capacity/fan-out
  atomicity control passed on the authorization baseline.
- After the production change, the complete integration file passes.

## Routing evidence

All times below come from the runtime trace. Error payload equality checks
cover every `PredictionError` field; trace checks cover prediction identity,
event identity, lineage, causal roots, truncation state and route context.
Ledger instrumentation confirms each reachable node consumes the unchanged
error payload. Instrumented neuron receivers confirm prediction-error events
are not passed to `MultiExcursionNeuron.receive_event()`.

| Control | Directed topology / observed routed errors | Result |
|---|---|---|
| One-hop and reverse/unreachable | `n0 -> n1 (0.25)` and `n2 -> n1 (0.10)`; local `n0 -> n0 @ 1.00`, then `n0 -> n1 @ 1.25`; `n2` receives none | Pass; only the current node's outgoing edge is used |
| Two-hop, unequal delays | `n0 -> n1 (0.25) -> n2 (0.40)`; arrivals `1.00`, `1.25`, `1.65`; sources `n0`, `n0`, `n1` | Pass; cumulative edge delays and route depth/path are exact |
| Non-numeric edge settings | One- and two-hop edges use non-identity Model-B parameters | Pass; prediction-error metadata and values remain unchanged |
| Convergent diamond | `n0 -> n1/n2`, both branches reach `n3` at `1.65`, then one `n3 -> n4 @ 1.95` | Pass; two arrivals converge, but the existing `(prediction_id, destination)` guard applies/forwards at `n3` once |
| Deterministic replay | Same diamond run twice | Pass; ordered error transcripts match |
| Directed cycle | `n0 -> n1 -> n0` | Pass; the return arrival is suppressed by the destination guard; no unbounded loop |
| Queue-capacity failure | Two-edge fan-out with insufficient remaining queue capacity | Pass; raises `QueueCapacityError` explicitly and leaves no partial fan-out |
| Character boundary | Repeat the same character identifier and therefore the same prediction identity after the previous character ends | Pass; guard state is empty at reset and the second real error reaches `n1` |

The complete payload assertions include `prediction_id`, `predictor_id`,
`target_key`, `predicted_value`, `observed_value`, `error`,
`prediction_timestamp`, `observation_timestamp` and `observation_source`.
Every routed hop retains event ID and lineage ID; queue sequence remains
fresh per queued event. No routed arrival precedes the observation timestamp.

## Validation record

| Check | Result |
|---|---|
| Focused integration suite: `python -m pytest -q tests/test_excursion_integration.py` | **PASS: 49 passed** (43 existing and 6 added controls) |
| ACP-0006 regression plus focused suite: integration file and `test_experiments.py`, `test_excursion_neuron.py`, `test_e2_multi_excursion.py`, `test_event_runtime.py`, `test_topology.py`, `test_predictive_coding.py`, `test_eligibility.py`, `test_streaming_classifier.py`, `test_energy_utility.py`, `test_ir2.py`, `test_e2_ir2.py`, `test_stroke_dataset.py` | **PASS: 340 passed** |
| The 12 listed ACP-0006 regression modules alone | **PASS: 291 passed**. Together with the 49-test focused integration file, this is 340 passed. |
| Full CPU suite: `python -m pytest -q` | **FAIL: 24 failed, 802 passed, 1 skipped; 827 collected**. The 24 failures are the same downstream compatibility cases recorded by Luna-0 at baseline; none is in the changed integration file. |
| Full collection: `python -m pytest --collect-only -q` | **PASS: 827 collected**, six more than the 821 baseline tests because six controls were added |
| `python -m compileall -q tpcn tests` | **PASS** |
| Diagnostics for `tpcn/experiment_excursion_runtime.py` and `tests/test_excursion_integration.py` | **PASS: no errors reported** |
| `git diff --check` | **PASS** |
| Hardware equivalence / physical-energy calibration | **NOT APPLICABLE; not claimed or authorized** |

### Full-suite downstream failure classification

The full suite's 24 failures match the baseline classification. These are
not Luna-26 regressions and were not changed:

| Consumer group | Failed tests | Baseline cause / classification |
|---|---|---|
| CPU visualization / TPCV capture (3) | `test_capture_modes_do_not_change_training_result`; `test_snapshot_sequence_is_deterministic_and_replays_offline`; `test_replay_rejects_missing_malformed_and_over_limit_data` | Downstream snapshot code expects scalar `.activation`, which `MultiExcursionNeuron` does not expose |
| Luna-12B structural experiment (4) | `test_structural_run_is_deterministic_and_has_real_bounded_mutations`; `test_capture_is_downstream_only_for_structural_decisions`; `test_controls_report_behavior_and_topology_without_assuming_benefit`; `test_structural_evidence_is_label_isolated` | Fixtures request structural plasticity under default `EXCURSION_V1`, which is intentionally unavailable |
| Luna-12E integration (2) | `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`; `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` | Assertions assume routed activity changes root prediction loss and legacy scalar clock/reset behavior |
| Luna-12L temporal scale (8) | `test_scale_runner_retains_all_policies_and_causal_evidence`; `test_requested_policy_is_executed_by_classifier[baseline]`; `[random]`; `[temporal]`; `[reversed]`; `test_policy_changes_classifier_execution_state`; `test_policy_scale_cross_product_preserves_provenance_and_serialization`; `test_condition_fails_on_classifier_provenance_mismatch` | Structural policy fixtures are rejected at configuration construction under `EXCURSION_V1`; the intended later assertions are not reached |
| Spiral benchmark (1) | `test_control_results_are_deterministic_and_include_required_order_controls` | Structural control is rejected under the fixed-topology excursion integration |
| Temporal analysis (3) | `test_flat_metrics_and_changing_topology_are_reported`; `test_rejection_reason_aggregation_preserves_observed_reasons`; `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` | Legacy structural/scalar snapshot assumptions in downstream fixtures |
| 3D viewer (3) | `test_layout_and_scene_generation_are_deterministic_and_diagnostic`; `test_topology_deltas_and_bounded_prune_highlights`; `test_playback_filters_selection_neighborhood_and_metrics` | Shared source fixture requests structural CPU training under `EXCURSION_V1` and fails before viewer code runs |

These classifications are taken from the published Luna-0 closure-readiness
matrix. No consumer migration or failure repair is in Luna-26 scope.

## Passed, failed, not-run and not-applicable summary

- **Passed:** Test-first reproduction against the exact authorization
  baseline; six added routing/reset/capacity controls after correction; all 49
  focused integration tests; 340 tests in the combined focused/regression
  set; compileall; diagnostics; diff check; collection audit.
- **Failed:** Full CPU suite, solely the 24 classified downstream compatibility
  failures above. This is consistent with the published baseline failure
  set; it does not constitute a failed Luna-26-owned test.
- **Not run:** No additional training-efficacy or dataset benchmark run was
  required or authorized. Existing label isolation and incremental-admission
  tests remain covered by the focused and regression suites.
- **Not applicable:** Hardware equivalence and physical-energy calibration.

## Return boundary

This is a CPU software-reference integration correction only. The
`BoundedTopology.route()` API and numeric Model-B transfer remain unchanged.
Luna-22 remains **BLOCKED / NOT CLOSED** until Luna-0 independently reviews
this implementation and evidence.
