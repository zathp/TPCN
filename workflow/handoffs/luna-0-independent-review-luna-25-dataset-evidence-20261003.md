# Luna-0 Independent Review — Luna-25 Dataset Evidence

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of Luna-25 UCI evidence"
  task_id: "luna-0-independent-review-luna-25-dataset-evidence-20261003"
  component: "ACP-0006 UCI Character Trajectories CPU evidence gate"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "425180bfb2b02691cf64f392f071795cc812cd72"
  result_revision: "Review publication commit; not self-recorded in this handoff"
  dependencies:
    - "Accepted ACP-0006"
    - "Published Luna-25 implementation/evidence at 5cb17d9bb79c848c27805cb79484d9ab3cd0f5b8"
    - "Published Luna-25 completion handoff at 425180bfb2b02691cf64f392f071795cc812cd72"
  owner: "Project owner"
  classification: ["VERIFICATION", "OBSERVATION"]
  hypothesis: "The published luna25-v1 dataset evidence can be independently reproduced and its input, label, metric, and resource boundaries can be verified without changing production behavior."
  counter_hypothesis: "Independent data retrieval, split reconstruction, output regeneration, boundary probes, or metric/resource reconciliation materially disagree with the published evidence."
  interfaces_relied_on:
    - "Standalone UCI MATLAB dataset parser and deterministic split in scripts/benchmark_uci_character_trajectories.py"
    - "Existing ExperimentRunner EXCURSION_V1 CPU path"
    - "Existing incremental ExcursionCharacterRuntime input, prediction, reward, and settling interfaces"
  label_information_boundary:
    - "Labels are absent from StrokePoint, admitted input event payloads, prediction targets, topology, and the trace before END_CHARACTER."
    - "Labels select the outer post-readout reward; reward/utility/eligibility accounting can therefore depend on the true label after the prediction is complete."
    - "Evaluation uses update=False, so no class prototype/readout update is made on validation or test; the label-dependent post-readout reward is an evaluation/accounting operation, not evidence of predictive learning."
    - "No writer/subject identity was available in the retrieved MATLAB metadata; writer-disjointness is not claimed."
  timing_assumptions:
    - "Source order is retained; point timestamp is index * 0.005 seconds and restarts per character."
    - "Only a currently admitted point contributes to its input scalar; no future point or whole-character normalization is used."
    - "Character settling uses the configured 10-second local-time horizon."
  reset_boundaries:
    - "The existing runner resets character-local runtime state at each START_CHARACTER boundary."
    - "The existing training model/readout is retained between training characters and for validation/test evaluation; validation/test do not update the readout."
  resource_bounds:
    - "80 configured nodes; 1 initial edge; edge capacity 8; fan-in/out limits 2."
    - "Queue capacity 512; event budget 4096 per character; E2 neuron event budget 8192."
    - "Prediction capacity 8 per character; expiry 4 seconds; provenance capacity 16."
    - "Maximum input points 256; observed source maximum 205."
  authorized_scope:
    - "Read-only independent verification of the exact published Luna-25 revision."
    - "Independent source retrieval/parsing, split reconstruction, fresh-run reproduction, metric/resource arithmetic, and label/future-input probes."
    - "Create a Luna-0 review handoff and synchronize workflow/changelog governance status."
  unauthorized_scope:
    - "Changing benchmark/runtime code, tests, or Luna-25 committed evidence artifacts."
    - "Repairing the 24 downstream consumer failures."
    - "Closing Luna-22, asserting ACP-0006 integration readiness, or making hardware-equivalence claims."
  controls:
    - "Two fresh benchmark runs on the independently downloaded source."
    - "Same input/initialization with counterfactual outer labels."
    - "Same two-point prefix with different not-yet-admitted suffixes."
    - "Full-suite comparison against previously classified post-Luna-23 downstream failures."
  measurements:
    - "Independent UCI archive and extracted MAT SHA-256."
    - "Exact split member/rank/code reconstruction and canonical manifest digest."
    - "Stable output and training replay digests."
    - "Classification, prediction lifecycle, activity, queue, topology, settling, and energy-proxy arithmetic."
  information_boundary_check:
    - "Counterfactual-label probe: identical pre-reward input/runtime state and readout; outer reward differs only after END_CHARACTER."
    - "Differing-suffix probe: identical incremental admissions and runtime state through the shared prefix."
  hardware_mapping:
    - "Python CPU software-reference evidence only; no hardware backend or equivalence check."
  architecture_invariants_touched: ["A01", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "A01-A15 and accepted ACP-0006 remain unchanged."
    - "EXCURSION_V1 semantics, fixed topology, and downstream consumers remain unchanged."
    - "luna25-v1 is a new deterministic baseline, not an exact reconstruction of the Luna-22 subset."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna-25-dataset-evidence-20261003.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Luna-25 focused tests: 7 passed."
    - "Prescribed ACP-0006 regression set: 334 passed."
    - "Independent split, two-run reproduction, label/future-prefix probes, metric/resource reconciliation, and prediction lifecycle instrumentation: passed."
  tests_failed:
    - "Full CPU suite: 24 previously classified downstream failures; 796 passed; 1 CUDA-unavailable skip."
  tests_not_run:
    - "Hardware equivalence and physical-energy calibration: not applicable/not run."
    - "Full-dataset training: not run; this evidence gate uses a declared 160-record subset."
    - "Pylance diagnostics: not run during this review."
  assumptions:
    - "UCI dataset page identifies the dataset license as CC BY 4.0; the downloaded source bytes are verified by hash."
    - "No accuracy threshold is established by ACP-0006 or the source acceptance criteria."
  unresolved:
    - "Predictive efficacy and useful delayed-credit learning are not demonstrated: zero matched predictions, zero prediction errors, and zero matched credit."
    - "The 24 downstream compatibility failures still block overall Luna-22/ACP-0006 integration readiness."
    - "Writer-disjoint evaluation cannot be established from available source metadata."
  recommended_next_agent: []
```

## Outcome and reviewed scope

**PASS — Luna-25's bounded `luna25-v1` dataset reproducibility/evidence gate
is independently verified and closed.** This is not an exact reconstruction
of the historical Luna-22 subset, is not evidence of predictive efficacy, and
does not close Luna-22 or establish repository-wide ACP-0006 integration
readiness.

Review began on clean `main` at
`425180bfb2b02691cf64f392f071795cc812cd72`, equal to `origin/main`. The
verified publication lineage is:

```text
7e174de664bc116db77aad89c8bed08ca750bcd3
  -> 5cb17d9bb79c848c27805cb79484d9ab3cd0f5b8
  -> 425180bfb2b02691cf64f392f071795cc812cd72
```

The implementation/evidence delta contains only the standalone adapter,
focused tests, and three machine-readable artifacts. The separate publication
delta contains only the Luna-25 completion handoff. No production module,
benchmark code, test, or committed result artifact was changed in this review.

## Independent source and split verification

**OBSERVED:** The UCI Character Trajectories archive was downloaded again
from the recorded UCI URL into a fresh temporary directory. Its SHA-256 is
`5d2db017ef0d8cf0e65ed060c9e90399f78eb9f1e3cb63e22ca8c3ef4ba67d52`;
the independently extracted `mixoutALL_shifted.mat` SHA-256 is
`00ab9af03f74167b5ddee9d5f3e7ed3da8df0bc49d2e9c4078c51857fdc13ebe`.
SciPy independently parsed 2,858 finite `3-by-T` trajectories, with lengths
109–205 and `consts.dt == 0.005`. The one-based class-key mapping is the
published 20-class mapping `a,b,c,d,e,g,h,l,m,n,o,p,q,r,s,u,v,w,y,z`.

The raw MAT structure exposes fields `i`, `filename`, `penup`, `key`,
`charlabels`, `dt`, `xtraplen`, `sigma`, `D`, `datarescaled`, `units`,
`datanorm`, `N`, and `maxshift`; it has no writer/subject identity field.
`filename` identifies the source CSV name, not record writers. Consequently
writer-disjointness is unavailable and is not claimed.

**OBSERVED:** The split was reconstructed directly from the downloaded
records, integer source labels and IDs by the published SHA-256 ranking rule.
All selected source indices, class codes, ranks and split assignments match
the committed manifest exactly: 80 train, 40 validation and 40 test records,
with 4/2/2 per class. The canonical split-manifest digest independently
matches `79248deaa64b9b0f6143e5abc52beb01a46448434607bd920a1c0574d3557d80`.

**OBSERVED:** Two new benchmark runs on the independently downloaded MAT
source reproduced the committed stable per-split outputs and class reports.
Each stable output digest is
`236835bf31c001ff520ef9389674e969435c63fb7038fd6f0797292cdefa69cc`;
each training replay digest is
`441184878990df3a61fba67b72ea996b917650e19166cd2d0360e1c909ca39b6`.
The published `EXCURSION_V1` experiment config was accepted by the current
typed `ExperimentConfig`, and the fresh run produced the expected stable
digest.

The old 160-record Luna-22 membership, original loader and preprocessing
implementation are not retained. The matching validation/test aggregate
accuracies do not reconstruct that missing evidence. `luna25-v1` is a
separate baseline; the historical split and result remain unreconstructable.

## Causality and label boundary

**OBSERVED:** The adapter presents source-order points incrementally at
`index * 0.005` seconds, using only the current point's x/y velocity sum. It
ignores the third force row and performs no whole-character or
future-point-derived normalization. The source maximum of 205 is below the
256-point bound.

In the counterfactual-label probe, identical fresh initial state and identical
input were run with labels `a` and `z`. Neural input trace, emissions,
predictor state, queue, energy/meter and pre-reward state were identical; the
outer reward changed from `+1` to `-1` only after the post-readout
`END_CHARACTER` reward callback. The label does not enter `StrokePoint`,
neural event payload, prediction target or topology. The reward/utility and
eligibility accounting after readout is label-dependent by design. On
validation/test, `update=False` prevents class-prototype updates; those labels
can still affect post-readout reward/utility accounting. This distinction is
important: the run does not establish learning from held-out labels, and its
reward metrics are not label-independent measures.

The differing-suffix probe presented two streams with the same first two
points and different later suffixes. The admissions and runtime trace,
emissions, predictor state, queue, meter and neuron state matched through the
shared prefix, before either differing suffix was admitted. No lookahead
effect was observed.

## Independent metric and resource audit

The reported class prediction rows were independently reduced into confusion
matrices, supports, accuracy, per-class precision/recall/F1 and macro scores.
Every recomputed value exactly matches both the per-class report and the run
manifest. The independently verified aggregate scores are:

| Split | N | Correct | Accuracy | Macro precision | Macro recall | Macro F1 |
|---|---:|---:|---:|---:|---:|---:|
| Train, post-training | 80 | 12 | 0.150 | 0.0851 | 0.1500 | 0.0727 |
| Validation | 40 | 5 | 0.125 | 0.0270 | 0.1250 | 0.0428 |
| Test | 40 | 7 | 0.175 | 0.0998 | 0.1750 | 0.0989 |

Source trajectory lengths independently sum to 13,724 train, 6,862 validation
and 6,862 test input-point observations. A fresh run instrumented actual
`LocalPredictor.create_prediction` calls; for each reported partition,
created-prediction counts equal emission counts and expiry counts:

| Split | Input targets | Created predictions | Emissions | Expired | Matched | Prediction errors |
|---|---:|---:|---:|---:|---:|---:|
| Train, post-training evaluation | 13,724 | 138 | 138 | 138 | 0 | 0 |
| Validation | 6,862 | 67 | 67 | 67 | 0 | 0 |
| Test | 6,862 | 63 | 63 | 63 | 0 | 0 |

Thus zero matched and zero errors are accurately reported; prediction loss
is zero because no forecast matched an observed target. The unmatched counts
are target observations, not additional created predictions. Delayed credit
accounting ran, but matched credit is zero; useful delayed-credit learning is
not demonstrated.

For all three splits, processed events exactly equal emissions plus silent
events. Source-point counts equal reported prediction targets. Settling
completed for every character with no pending/beyond-deadline event, budget
exhaustion, or provenance truncation. Queue peaks are 189/512, 188/512 and
187/512; each partition reports 1/8 active connections and fan-in/out
utilization 0.00625/0.00625. Event-processing, emitted-amplitude,
edge-transfer and prediction-error proxy components sum to the reported
energy total within `1e-8`:

| Split | Event processing | Emitted amplitude | Edge transfer | Prediction error | Total proxy units |
|---|---:|---:|---:|---:|---:|
| Train | 25,353.0000 | 96.2244 | 1.1200 | 0 | 25,450.3444 |
| Validation | 12,670.0000 | 47.2421 | 1.1200 | 0 | 12,718.3620 |
| Test | 12,400.0000 | 44.5256 | 0.7051 | 0 | 12,445.2308 |

These are activity-cost proxy units, not joules or calibrated physical
energy. No numerical accuracy threshold is established by ACP-0006.

## Architecture and acceptance scope

No contract clause or ACP was changed. The evidence is a CPU dataset
reproducibility run, not an end-to-end architecture acceptance run:

| Clause | Review evidence / boundary |
|---|---|
| A01-A03 | Incremental, source-ordered timestamped inputs and the shared-prefix suffix probe support the stated causal input boundary. This dataset run does not independently prove every core event-order, finite-delay, unequal-path or batching invariant. |
| A04, A08 | The run declares finite nodes, topology, queue, event, prediction, point and provenance bounds; observed queue/event/settling measurements remain within those bounds. This is not a recurrent stress test. |
| A05 | The published run uses the existing EXCURSION_V1 CPU path and does not require the deprecated spatial reservoir. |
| A06 | **Not demonstrated:** no prediction matched; no explicit prediction-error event was generated; prediction efficacy is not established. |
| A07 | Label and future-input probes support the outer-label and incremental-input boundaries. Outer reward/utility remains label-dependent after readout, and is distinguished from pre-readout neural input. |
| A09-A10 | Energy proxy arithmetic reconciles and the utility/reward config is recorded. No calibrated energy, high-cost/high-reward survival or high-cost/low-reward suppression result is established here. |
| A11 | Runtime credit accounting is reported; no matched delayed credit occurred, so useful delayed-credit learning is not demonstrated. |
| A12-A13 | `event_only` is an experiment setting only; this run draws no conclusion that event-only activation or absence of gates is mandatory. |
| A14 | Structural plasticity is explicitly disabled and topology fixed; no structural-adaptation claim is made. |
| A15 | CPU software reference only. GPU/FPGA/FPAA equivalence is not tested or claimed. |

Accordingly, the independent dataset evidence gate passes, while the broader
streaming integration criteria involving predictive error, useful delayed
credit and downstream compatibility remain unresolved.

## Downstream consumer compatibility decision matrix

The full suite adds seven Luna-25 tests to the previous collection of 814,
for 821 collected. The fresh full CPU run reports 24 failed, 796 passed and
one skipped because CUDA is unavailable. All 24 failures are within the
already classified post-Luna-23 consumer groups; none is in the Luna-25 tests.
No broad downstream migration is authorized by this review.

| Consumer group | Current failing tests | Compatibility decision still needed | Boundary for any future task |
|---|---:|---|---|
| CPU TPCV visualization | 3: `test_capture_modes_do_not_change_training_result`; `test_snapshot_sequence_is_deterministic_and_replays_offline`; `test_replay_rejects_missing_malformed_and_over_limit_data` | Choose an explicit legacy visualization path or a bounded E2 observation contract; do not synthesize a scalar `.activation` for `MultiExcursionNeuron`. | Keep capture downstream-only; preserve event/neuron identity and avoid computation backpressure. |
| Luna-12B structural experiment | 4: `test_structural_run_is_deterministic_and_has_real_bounded_mutations`; `test_capture_is_downstream_only_for_structural_decisions`; `test_controls_report_behavior_and_topology_without_assuming_benefit`; `test_structural_evidence_is_label_isolated` | Decide whether this consumer explicitly selects a compatible legacy model or waits for separately authorized structural integration. Do not silently enable plasticity in fixed-topology EXCURSION_V1. | Retain A04/A07/A14 bounds, label isolation and explicit model selection. |
| Luna-12L temporal scale / spiral control | 8 temporal-scale tests: `test_scale_runner_retains_all_policies_and_causal_evidence`; `test_requested_policy_is_executed_by_classifier[baseline]`, `[random]`, `[temporal]`, `[reversed]`; `test_policy_changes_classifier_execution_state`; `test_policy_scale_cross_product_preserves_provenance_and_serialization`; `test_condition_fails_on_classifier_provenance_mismatch`. Plus `test_control_results_are_deterministic_and_include_required_order_controls`. | Separate structural-policy/default-model incompatibility from temporal experiment semantics and assign a scoped compatibility contract. | Preserve causal temporal evidence and do not change canonical E2 timing to satisfy legacy fixture assumptions. |
| Luna-12E legacy observables | 2: `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`; `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` | Decide which observable is authoritative for E2 prediction ownership and its declared reset boundary. | Do not claim topology changes must alter root-input prediction loss or replace E2 local-time semantics with a scalar clock. |
| Temporal analysis | 3: `test_flat_metrics_and_changing_topology_are_reported`; `test_rejection_reason_aggregation_preserves_observed_reasons`; `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` | Provide an explicitly compatible structural replay fixture or model-selection contract. | Analysis remains downstream/read-only and must not infer causation from raw deltas. |
| 3D viewer | 3: `test_layout_and_scene_generation_are_deterministic_and_diagnostic`; `test_topology_deltas_and_bounded_prune_highlights`; `test_playback_filters_selection_neighborhood_and_metrics` | Choose an authorized, compatible replay source for structural scenes. | Viewer remains downstream-only and must not trigger structural mutation or computation. |

Because these groups require distinct API/behavior decisions, **no single
successor implementation is assigned here**. Luna-22 remains
**BLOCKED / NOT CLOSED** pending those compatibility decisions and evidence of
the broader predictive/error/credit integration criteria.

## Validation record

| Command or procedure | Revision / environment | Observed result |
|---|---|---|
| Independent HTTP retrieval, SHA-256, SciPy parse and direct split reconstruction | Published source hashes; Python 3.11.5, NumPy 2.4.2, SciPy 1.17.1 | PASS: source identity/schema, 2,858 records, class mapping, exact membership/ranks and split digest match. |
| Two fresh benchmark repetitions from independently retrieved data | Published `luna25-v1` config and seed | PASS: both stable-output and training replay digests match the published artifacts. |
| Independent confusion, macro/per-class metric and support recomputation | Published per-example predictions | PASS: report and manifest agree exactly. |
| Runtime prediction-creation instrumentation; event/resource/energy arithmetic | Fresh run from the published config | PASS: split prediction creation/emission/expiry counts and resource/energy sums reconcile. |
| Counterfactual-label and differing-future-suffix probes | Fresh identical runner state | PASS: no pre-readout label effect and no future-suffix effect through shared prefix. |
| `python -m pytest -q tests/test_uci_character_trajectories_benchmark.py` | Python 3.11.5 | PASS: 7 passed. |
| Prescribed ACP-0006 regression command listed in Luna-25 implementation handoff | Python 3.11.5 | PASS: 334 passed. |
| `python -m pytest -q -rs` | Python 3.11.5 | FAIL: 24 known downstream tests; 796 passed; 1 CUDA-unavailable skip. |
| `python -m pytest --collect-only -q` | Python 3.11.5 | PASS: 821 collected. |
| `python -m compileall -q scripts tests` and `git diff --check` | Python 3.11.5; reviewed branch | PASS. |
| Pylance diagnostics / hardware equivalence | Review environment | NOT RUN; no code changed and no hardware claim is made. |

## Governance disposition and next bounded work

- **Luna-25:** CLOSED / independently verified for repository-retained
  `luna25-v1` dataset/split/result reproducibility evidence.
- **Luna-22:** BLOCKED / NOT CLOSED. Dataset reproducibility is resolved for
  the new baseline only; it does not reconstruct Luna-22's subset, demonstrate
  prediction/error or delayed-credit efficacy, or clear the 24 consumer
  failures.
- **Luna-23 and Luna-24:** remain CLOSED / independently verified.
- **ACP-0006 and A01-A15:** unchanged; no architecture promotion or hardware
  acceptance.
- **Next assignment:** no implementation agent is assigned until the project
  owner/Luna-0 selects a specific downstream compatibility contract. The
  consumer groups above must remain separate rather than being combined into
  a broad test-green effort.
