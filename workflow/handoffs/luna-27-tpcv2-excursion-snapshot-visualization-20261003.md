# Luna-27 TPCV-2 EXCURSION_V1 Snapshot Visualization

```yaml
tpcn_handoff:
  agent: "Luna-27"
  luna_identifier: "Luna-27"
  descriptive_name: "TPCV-2 EXCURSION_V1 snapshot visualization"
  task_id: "luna-27-tpcv2-excursion-snapshot-visualization-20261003"
  component: "CPU snapshot capture, codec, and offline replay"
  status: "complete — submitted to Luna-0 for independent review"
  contract_version: "TPCV-1 preserved; TPCV-2 for EXCURSION_V1"
  branch: "main"
  base_revision: "10b9bfa09c949576099a220c2f507d939c01c337"
  result_revision: "3bb8edc — implementation; this handoff is committed separately"
  dependencies:
    - "Luna-0 post-ACP-0006 TPCV / EXCURSION_V1 compatibility decision"
    - "Luna-0 Luna-27 authorization"
  owner: "Luna-27"
  classification: ["IMPLEMENTATION", "VERIFICATION", "DOWNSTREAM REPRESENTATION"]
  hypothesis: "A dedicated TPCV-2 CPU representation can capture EXCURSION_V1 observations without changing TPCV-1 bytes or neural computation."
  counter_hypothesis: "Honest excursion observations cannot be represented and replayed within the authorized format bounds while preserving TPCV-1."
  interfaces_relied_on:
    - "VisualizationSnapshot, ExcursionNeuronRecord, export_snapshot, parse_snapshot"
    - "CPUTrainingCapture and ReplaySequence"
    - "MultiExcursionNeuron public state, mode, pending_internal_event, and processed_event_count"
  label_information_boundary:
    - "Snapshots contain no labels, future inputs, future rewards, or future structural decisions."
  timing_assumptions:
    - "Capture occurs only at existing CPU epoch boundaries and describes an instantaneous state."
    - "No global neural timestep or interval activity is introduced."
  reset_boundaries:
    - "No computation or reset semantics changed."
  resource_bounds:
    - "TPCV snapshot remains bounded to 1 MiB with at most 65,535 neuron and connection records."
    - "IDs remain nonempty UTF-8 up to 255 bytes; coordinates remain signed 32-bit."
    - "Replay record count, each record, aggregate replay data, and metric/manifest data are bounded."
  authorized_scope:
    - "Implement TPCV-2 instantaneous EXCURSION_V1 CPU capture, encoding, decoding, and homogeneous-version replay."
    - "Modify only the six Luna-27-owned files."
  unauthorized_scope:
    - "No neuron, runtime, event, IR-2, learning, reward, topology, training, GPU, FPGA, viewer, or temporal-analysis behavior changes."
    - "Do not repair the 21 classified downstream full-suite failures."
  controls:
    - "Pre-change TPCV-1 120-byte fixture and SHA-256 golden."
    - "Capture disabled/every-epoch/every-N-epochs training-result equivalence."
    - "Deterministic repeated snapshots and detached offline replay."
    - "Malformed, oversized, unsupported-version, and mixed-version rejection."
  measurements:
    - "Focused visualization/CPU/GPU tests: 33 passed, 1 skipped."
    - "Full suite: 821 passed, 21 failed, 1 skipped; all 21 failures are the previously classified downstream groups."
  information_boundary_check:
    - "TPCV-2 records only x/state, current mode, derived active, pending-work existence, processed-event count, optional position, and existing connection records."
    - "No payload, queue sequence, emissions/history, provenance, counters, prediction/eligibility ledgers, or queue state is serialized."
  hardware_mapping:
    - "TPCV-2 is implemented for the CPU reference path only."
    - "GPU TPCV-1 regression passes; no EXCURSION_V1 GPU, ModelSim/FPGA parity, or hardware equivalence is claimed."
  architecture_invariants_touched: ["A01", "A04", "A07", "A08", "A15"]
  preserves:
    - "TPCV-1 encoding, decoding, frame meaning, and canonical fixture bytes."
    - "Downstream-only epoch-boundary observation and fixed topology."
    - "Training results and event/computation behavior under capture frequency changes."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/visualization.py"
    - "tpcn/cpu_visualization.py"
    - "tests/test_visualization.py"
    - "tests/test_cpu_visualization.py"
    - "workflow/docs/luna/VISUALIZATION_CONTRACT.md"
    - "workflow/handoffs/luna-27-tpcv2-excursion-snapshot-visualization-20261003.md"
  tests_added:
    - "TPCV-1 golden-byte/digest preservation."
    - "TPCV-2 deterministic round trip, four mode encodings, observation mapping, version identity, and activation unavailability."
    - "TPCV-2 invalid version/mode/flags, malformed framing/UTF-8/numbers, and bounded memoryview parsing."
    - "Mixed-version replay, oversized record/manifest rejection, and excursion-state observation through public neuron APIs."
  tests_passing:
    - "tests/test_visualization.py, tests/test_cpu_visualization.py, tests/test_gpu_visualization.py: 33 passed, 1 skipped."
    - "Full suite: 821 passed."
    - "compileall for the four changed Python files."
    - "Pylance diagnostics on the four changed Python files: no errors."
    - "git diff --check."
  tests_failed:
    - "21 previously classified downstream tests remain failing; see Validation record."
  tests_not_run:
    - "No GPU EXCURSION_V1, ModelSim, FPGA, or hardware-equivalence test is authorized or claimed."
  assumptions:
    - "The published Luna-0 Decision C and exact six-file ownership remain authoritative."
  unresolved:
    - "Luna-0 independent review is pending; no successor assignment is authorized."
  recommended_next_agent: ["Luna-0 Architecture Guardian"]
```

## Outcome and owned scope

**OBSERVED:** the original CPU visualization path failed because it requested
`MultiExcursionNeuron.activation`, which is not defined. The implementation
adds an explicit `ExcursionNeuronRecord` and TPCV-2 codec branch. The TPCV-1
record layout and frame shape are retained; a fixed pre-change fixture remains
120 bytes with SHA-256
`0ad558e8e229f1a4598513987b44715a051f43f399540c82e2515137af9b6eb8`.

**OBSERVED:** TPCV-2 uses the header version as its model discriminator. The
CPU observer records `state=x`, `active=(mode != N)`, the explicit mode,
pending-internal-work existence, and total processed-event count. Its binary
record has no activation field; the shared frame tuple places `None` in the
historical activation position and appends mode, pending-work, and event
count. Replay preserves the version and rejects mixed-version sequences.
File and in-memory replay inputs are size-checked before unbounded
materialization.

**INFERRED:** passing capture equivalence and deterministic replay controls
supports that observation remains downstream-only for the exercised
synthetic CPU workload. No changes were made to neural computation, queue
ordering, predictions, learning, rewards, topology, or training results.

Changed only the six authorized files listed in the YAML. No architecture
contract, ACP, core, GPU, viewer, or unrelated failure-group file was changed.

## Architecture evidence

| Clause | Evidence |
|---|---|
| A01 | Capture remains an epoch-boundary pull; no global neural tick or event injection was added. |
| A04 | Existing bounded topology/connection representation and record limits are retained. |
| A07 | Snapshot fields are observations only; labels and training outcomes do not enter neuron computation. |
| A08 | Snapshot, record, sequence, metric, and manifest input bounds are enforced. |
| A15 | The format remains hardware-neutral, but only CPU TPCV-2 behavior is implemented and tested. |

No A01–A15 requirement changed. No ACP or architecture promotion is proposed.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_visualization.py tests/test_cpu_visualization.py tests/test_gpu_visualization.py` | Windows, Python 3.11.5; current implementation; deterministic test seeds | **33 passed, 1 skipped** | Focused TPCV-1/TPCV-2, CPU replay, and GPU TPCV-1 regression |
| `python -m pytest -q` | Windows, Python 3.11.5; full repository suite | **821 passed, 21 failed, 1 skipped** | All 21 failures are listed below and match the classified downstream groups |
| `python -m compileall -q tpcn/visualization.py tpcn/cpu_visualization.py tests/test_visualization.py tests/test_cpu_visualization.py` | Python 3.11.5 | **Passed** | No syntax/bytecode errors |
| Pylance diagnostics on the four changed Python files | Workspace diagnostics | **No errors found** | `visualization.py`, `cpu_visualization.py`, and both touched tests |
| `git diff --check` | Implementation revision `3bb8edc` | **Passed** | No whitespace errors |

The full-suite baseline recorded by the preceding Luna-0 review was **804
passed, 24 failed, 1 skipped, 829 collected**. This run resolves the three
CPU visualization failures and adds 14 tests; it leaves the same 21 classified
failures, for 843 collected tests total:

- `tests/test_luna12b_integration.py`: `test_structural_run_is_deterministic_and_has_real_bounded_mutations`,
  `test_capture_is_downstream_only_for_structural_decisions`,
  `test_controls_report_behavior_and_topology_without_assuming_benefit`,
  `test_structural_evidence_is_label_isolated`.
- `tests/test_luna12e_integration.py`:
  `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`,
  `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary`.
- `tests/test_luna12l_temporal_scale.py`: `test_scale_runner_retains_all_policies_and_causal_evidence`,
  `test_requested_policy_is_executed_by_classifier[baseline]`,
  `test_requested_policy_is_executed_by_classifier[random]`,
  `test_requested_policy_is_executed_by_classifier[temporal]`,
  `test_requested_policy_is_executed_by_classifier[reversed]`,
  `test_policy_changes_classifier_execution_state`,
  `test_policy_scale_cross_product_preserves_provenance_and_serialization`,
  `test_condition_fails_on_classifier_provenance_mismatch`.
- `tests/test_spiral_benchmark.py`:
  `test_control_results_are_deterministic_and_include_required_order_controls`.
- `tests/test_temporal_analysis.py`: `test_flat_metrics_and_changing_topology_are_reported`,
  `test_rejection_reason_aggregation_preserves_observed_reasons`,
  `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation`.
- `tests/test_viewer_3d.py`: `test_layout_and_scene_generation_are_deterministic_and_diagnostic`,
  `test_topology_deltas_and_bounded_prune_highlights`,
  `test_playback_filters_selection_neighborhood_and_metrics`.

These are outside Luna-27 ownership and were not modified.

## Benchmark and resource results

No dataset/accuracy or energy benchmark applies. The synthetic CPU training
tests verify deterministic capture/replay and equal `TrainingResult` values
with capture disabled, every epoch, and every two epochs. Snapshot and replay
size/count bounds are checked. No hardware latency, physical energy, GPU
EXCURSION_V1, or FPGA/ModelSim result is claimed.

## Assumptions, limitations and unresolved issues

**OBSERVED:** the changed-file diagnostics were clean and the focused
visualization/GPU tests passed. The one skipped test remains skipped by the
existing suite.

**INFERRED:** the full-suite failures are unchanged, out-of-scope downstream
failures because their exact classified test groups remain and no files in
those groups were changed. They are preserved for their owners.

**HYPOTHESIZED:** none; Luna-27 does not claim an efficacy or hardware
hypothesis result.

The implementation is ready for independent Luna-0 review only. This handoff
does not close Luna-27 architecturally or authorize a successor.

## Reproduction and rollback

From the repository root, use Python 3.11.5 and run:

```powershell
python -m pytest -q tests/test_visualization.py tests/test_cpu_visualization.py tests/test_gpu_visualization.py
python -m pytest -q
```

The implementation commit is `3bb8edc` on top of the published Luna-27
authorization baseline `10b9bfa09c949576099a220c2f507d939c01c337`. Restore
only the six listed Luna-27 files if a rollback is explicitly authorized;
preserve unrelated work.

## Next assignment

Return to **Luna-0 Architecture Guardian** for independent review of the
implementation and evidence. The independent review should verify byte-level
TPCV-1 compatibility, TPCV-2 semantics/bounds, the full-suite failure
classification, and exact file ownership. No later Luna, GPU migration,
hardware parity claim, or architecture promotion is authorized by this
handoff.
