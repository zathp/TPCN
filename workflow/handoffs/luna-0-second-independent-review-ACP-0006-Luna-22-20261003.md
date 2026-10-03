# Luna-0 Second Independent Review - ACP-0006 / Luna-22

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Second independent review of Luna-22 CPU excursion integration"
  task_id: "luna-0-second-independent-review-ACP-0006-Luna-22-20261003"
  component: "ACP-0006 experiment integration, E2 scheduling and IR-2 startup boundary"
  status: "blocked; Luna-22 is not independently closed"
  contract_version: "1.1"
  branch: "main"
  base_revision: "a206f2e8fec8f0c72d9196b2bcca9d2e734c7974"
  result_revision: "baec12ad368239d959ca747d5a4e28c96746dd6e"
  dependencies:
    - "Accepted ACP-0006 and Luna-22 implementation/handoff published"
    - "ACP-0004 E2 / Luna-21 independently closed"
    - "TPCN-IR-2 schema revision 1 independently closed"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["INDEPENDENT REVIEW", "ARCHITECTURE CONFORMANCE VERIFICATION", "ADVERSARIAL VERIFICATION"]
  hypothesis: "The published integration and IR-2 correction satisfy ACP-0006 and the applicable software-reference integration gates."
  counter_hypothesis: "A valid causal workload or valid quiescent-state boundary exposes an integration or closed-component defect."
  interfaces_relied_on:
    - "ExcursionCharacterRuntime and the shared character EventQueue"
    - "MultiExcursionNeuron E2 internal-event validity and reset"
    - "TPCN-IR-2 schema revision 1 and standalone E2 adapters"
    - "Bounded Model-B topology, predictor, eligibility ledger and streaming classifier"
  label_information_boundary:
    - "Synthetic label-isolation tests pass; neural paths receive no labels."
    - "Dataset run details are reported separately; no efficacy claim is made."
  timing_assumptions:
    - "Causal external-input watermark and destination-local external-before-internal ordering."
    - "Finite positive logical internal and edge delays."
    - "A representable logical timestamp must remain strictly later than the neuron's current timestamp."
  reset_boundaries:
    - "Character queue and sidecar are destroyed after settling; E2 state resets while identity high-water counters survive."
    - "IR-2 integrated startup is only for a fresh, uniformly EXCURSION_V1 quiescent boundary."
  resource_bounds:
    - "Finite shared queue, event budget, route sidecar, provenance, predictor and eligibility capacities."
    - "Finite settling horizon and explicit incomplete-run reporting."
  authorized_scope:
    - "Read-only review of published Luna-22 implementation, tests, handoff and exact commit delta."
    - "Independent test execution, runtime probes, review handoff and workflow/changelog synchronization."
    - "Two narrow corrective authorizations recorded below."
  unauthorized_scope:
    - "Downstream visualization or research-consumer migration."
    - "Learning, prediction, reward, Model-B or A01-A15 redesign."
    - "N3, H2, GPU, FPGA, FPAA, IR-3, hardware equivalence or calibration."
  controls:
    - "Accepted ACP-0006 and unchanged A01-A15 architecture contract."
    - "Standalone E2 / IR-2 reference tests and explicit TANH_LEGACY compatibility mode."
  measurements:
    - "Focused and prescribed regression counts, full-suite failures and skip identity."
    - "Independent t0/t1/t2, IR-2 boundary and floating-point rearm probes."
  information_boundary_check:
    - "No label or future input was used in the scheduler or E2 probes."
  hardware_mapping:
    - "Software-reference review only; no hardware mapping or equivalence evidence."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "A01-A15 and ACP-0006; no architecture contract or canonical equation was changed."
    - "Standalone E2 active/pending IR-2 round trips and schema revision 1."
    - "Luna-22's five-file implementation scope; no implementation file was edited in this review."
  architecture_change: false
  proposal: "ACP-0006"
  files_changed:
    - ".github/agents/luna-23.agent.md"
    - ".github/agents/luna-24.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-23-e2-time-representability-20261003.md"
    - "workflow/handoffs/luna-0-authorization-luna-24-ir2-provenance-20261003.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-second-independent-review-ACP-0006-Luna-22-20261003.md"
  files_reviewed:
    - ".github/agents/luna-0.agent.md"
    - ".github/agents/luna-21.agent.md"
    - ".github/agents/luna-22.agent.md"
    - "workflow/ARCHITECTURE_CONTRACT.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md"
    - "workflow/docs/architecture_proposals/README.md"
    - "workflow/docs/architecture_proposals/ACP-TEMPLATE.md"
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/docs/architecture_proposals/ACP-0006.md"
    - "workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md"
    - "workflow/handoffs/excursion-runtime-integration-Luna-22.md"
    - "tpcn/experiments.py"
    - "tpcn/experiment_excursion_runtime.py"
    - "tpcn/excursion_neuron.py"
    - "tpcn/ir2.py"
    - "tests/test_excursion_integration.py"
    - "tests/test_experiments.py"
    - "tests/test_e2_ir2.py"
  tests_added: []
  tests_passing:
    - "Focused Luna-22 tests: 41 passed."
    - "Prescribed component/integration regression set: 318 passed."
    - "Independent t0/t1/t2 runtime probe confirmed 0.0 input, 1.0 input, then 2.0 internal work; t1 changed S_EMIT generation 1 to M_EMIT generation 3."
    - "Generation-mismatched stale S_EMIT was consumed as a no-op; the valid M_EMIT retained both causal roots."
    - "IR-2 probes confirmed positive, negative and smallest positive residual x rejection; both unassigned-provenance markers rejection; valid high-water acceptance; mixed model and S_PENDING/S_RETURN/M_ACTIVE rejection."
    - "Same-time external-before-internal, emission-only routing, delayed prediction error, delayed credit, readout, finite settling, reset and identity high-water integration tests pass."
  tests_failed:
    - "Full CPU suite: 27 failed, 770 passed, 1 skipped."
    - "IR-2 integrated startup incorrectly accepts assigned residual provenance and provenance_truncated=True."
    - "A valid E2 return at logical time 45.27906122689938 computes positive delay 1.110223024625156e-15, but floating-point addition leaves the due timestamp unchanged and E2 raises ValueError."
  tests_not_run:
    - "A new retained/reproducible UCI loader, split and per-class metric report; the published ad-hoc loader and per-class table are unavailable."
    - "Hardware/backend validation, unauthorized by this review."
  assumptions:
    - "The ACP-0006 startup gate's 'no residual provenance' includes an assigned provenance tuple or sticky provenance_truncated flag, not only unassigned-provenance counters."
    - "A mathematically positive delay that cannot advance the current floating-point timestamp must be handled without silently scheduling same-time work; Luna-23 must stop if the compatible behavior is not determinate."
  unresolved:
    - "Luna-22 cannot close until both corrective tasks and the actual sequential-dataset evidence gate are complete."
    - "Twenty downstream failures remain to be assigned consumer-specific compatibility/migration decisions after core blockers are resolved."
    - "No downstream migration is authorized by this review."
  recommended_next_agent:
    - "Luna-23: bounded ACP-0004 E2 positive-delay representability correction."
    - "Luna-24: bounded ACP-0006 IR-2 residual-provenance startup correction."
```

## Review baseline and exact implementation delta

**OBSERVED:** The second review started at published revision
`a206f2e8fec8f0c72d9196b2bcca9d2e734c7974` on `main`, with
`HEAD == origin/main` and a clean worktree. The implementation commit's parent
is `c13deb06427c64d00f603b1b1a1c75e442392fb8`. Its complete delta contains
only the five expected Luna-22 files:

- `tests/test_excursion_integration.py` (added)
- `tests/test_experiments.py` (modified)
- `tpcn/experiment_excursion_runtime.py` (added)
- `tpcn/experiments.py` (modified)
- `workflow/handoffs/excursion-runtime-integration-Luna-22.md` (added)

No closed component, IR-2 schema, Model-B equation, ACP-0002 through
ACP-0006, architecture contract, or A01-A15 text was changed by Luna-22 or by
this review. Luna-22's published file ownership is respected.

## Validation performed

| Command or procedure | Revision / environment | Result |
|---|---|---|
| `python -m pytest -q tests/test_experiments.py tests/test_excursion_integration.py` | `a206f2e`, Windows, Python 3.11.5 | **41 passed** |
| Luna-22 prescribed 13-file regression command from its handoff | `a206f2e`, Windows, Python 3.11.5 | **318 passed** |
| `python -m pytest -q -rs` | `a206f2e`, Windows, Python 3.11.5 | **27 failed, 770 passed, 1 skipped** |
| `python -m pytest -q --tb=no` over the seven failing consumer modules | Same | **27 failed, 12 passed**; exact failure identities recorded below |
| `tests/test_luna12l_temporal_scale.py` with short tracebacks | Same | **11 failed, 1 passed**; six numeric-delay failures and five structural-plasticity/default-model failures |
| `tests/test_spiral_benchmark.py` with short tracebacks | Same | **1 failed, 5 passed**; positive E2 rearm delay rounded to the current timestamp |
| Independent Python runtime probe of the required scheduler sequence | Workspace Python 3.11.5 | `0.0` external, `1.0` external, then `2.0` internal; pending S_EMIT generation 1 changed to M_EMIT generation 3 |
| Independent IR-2 startup boundary probes | Workspace Python 3.11.5 | Results detailed in the matrix below |

The skipped test is `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`;
the reason is `CUDA is unavailable`. The CUDA skip is not a Luna-22 failure.

`runTests` did not discover tests in the supplied Python files in this
workspace; the same focused and regression commands were run successfully with
the selected Python 3.11.5 interpreter and pytest.

## Causal scheduler and integration observations

The independent runtime trace used the required counterexample:

1. External input at `t0=0.0`, payload `1.2`, scheduled `S_EMIT @ 2.0`,
   generation 1.
2. External input at `t1=1.0`, payload `4.0`, was admitted before `t2`. It
   changed the active pending slot to `M_EMIT @ 2.0`, generation 3.
3. At `t2=2.0`, the old generation-1 S event remained in the queue and was
   traced, but `MultiExcursionNeuron._receive_internal()` rejected it against
   the current pending slot. It caused no emission. The valid generation-3 M
   event then emitted and retained causal roots from both inputs.
4. The trace prefix was `(0.0, INPUT), (1.0, INPUT)`. Emissions occurred at
   `2.0` and `4.0`; the additional later S emission is the M episode's valid
   residual transition, not execution of the stale generation-1 event.

**PASS:** The stale event is computationally inert, same-time external input
precedes internal work, and the t1 event changes/reschedules pending E2 work.
The queue still accounts for stale work and it remains visible in the event
trace; the stale record is not silently removed.

The focused integration tests additionally confirm:

- Silence emits no readout activity and creates no routed neural signal;
  only actual `ExcursionEmission` values route through Model-B.
- A later input matches one prediction, creates one explicit
  `PredictionError` at the observation timestamp, and has positive loss in the
  synthetic fixture.
- Delayed reward matches emitted-excursion eligibility with the declared
  `0.25` reward latency.
- Classifier activity count equals emission count; the single-emission
  readout feature is `0.3`.
- Finite settling reports one pending/beyond-deadline event and an incomplete
  run rather than claiming completion.
- Reset invalidates old pending work; identity high-water counters survive
  character reset.

These pass the synthetic mechanics gates. They do not establish useful
predictive task efficacy on the retained real-data run.

## IR-2 startup boundary

| Case | Observed integrated-startup result | Verdict |
|---|---|---|
| Uniform `EXCURSION_V1`, N, x=0, no pending/episode/lineage/provenance | Accepted; deterministic continuation test passes | Pass |
| Valid retained identity high-water counters | Accepted | Pass |
| Positive x=0.25 | Rejected | Pass |
| Negative x=-0.25 | Rejected | Pass |
| Smallest positive subnormal nonzero x | Rejected exactly; no epsilon normalization | Pass |
| `unassigned_provenance_count > 0` | Rejected | Pass |
| `unassigned_provenance_truncated=True` | Rejected | Pass |
| S_PENDING, S_RETURN and M_ACTIVE with valid pending E2 records | Rejected as live-network resume | Pass |
| Mixed `EXCURSION_V1` / `TANH_LEGACY` records | Rejected | Pass |
| Non-empty assigned `provenance` tuple with N and x=0 | **Accepted** | **Fail** |
| `provenance_truncated=True` with N and x=0 | **Accepted** | **Fail** |

The Luna-22 correction correctly rejects nonzero x and both unassigned
provenance cases, including tiny exact nonzero x. It does not reject assigned
residual provenance or the sticky `provenance_truncated` flag. The valid
quiescent startup contract expressly requires no residual provenance and
restores only approved counters/configuration; therefore these accepted
records violate the integrated-startup boundary. This is a Luna-22 adapter
defect, not a request to extend IR-2. Standalone E2 active/pending round trips
remain supported by the existing adapter, and the schema remains revision 1.

## E2 logical-time representability defect

The label-isolation test in the four-class temporal-scale benchmark fails on a
valid deterministic event stream. An independent reproduction observed:

```text
clock       = 45.27906122689938
x           = -0.2500000000000003
theta_r     = 0.25
computed_dt = 1.110223024625156e-15  # positive
clock + dt  = 45.27906122689938      # rounds to current float
nextafter   = 45.27906122689939
```

The E2 `_finish_rearm()` path passes `clock + computed_dt` to the strict-future
`_schedule()` check, which raises `ValueError("E2 internal events require a
finite positive logical delay")`. This blocks valid non-structural E2
classification workloads, including the temporal-scale label-isolation case
and the spiral-control run. It originates in closed E2 logical-time
representability, not the Luna-22 event queue or downstream visualization.
No runtime fix was made during this review.

## Classification of all 27 full-suite failures

| Consumer / count | Failed tests and observed cause | Review classification |
|---|---|---|
| `tests/test_cpu_visualization.py` (3) | `test_capture_modes_do_not_change_training_result`; `test_snapshot_sequence_is_deterministic_and_replays_offline`; `test_replay_rejects_missing_malformed_and_over_limit_data`. TPCV-1 `NeuronRecord.from_neuron()` assumes scalar `.activation`, which `MultiExcursionNeuron` does not expose. | Visualization/API compatibility, not an E2 emission defect. Do not synthesize an activation value. A separate decision must choose explicit legacy visualization or an E2-specific observation contract. |
| `tests/test_luna12b_integration.py` (4) | `test_structural_run_is_deterministic_and_has_real_bounded_mutations`; `test_capture_is_downstream_only_for_structural_decisions`; `test_controls_report_behavior_and_topology_without_assuming_benefit`; `test_structural_evidence_is_label_isolated`. Structural consumers request plasticity while the default is EXCURSION_V1, which ACP-0006 intentionally keeps fixed-topology. | Legacy structural experiment compatibility; must not be force-enabled in ACP-0006. A separate scoped task must choose explicit TANH_LEGACY or await a future structural integration authorization. |
| `tests/test_luna12e_integration.py` (2) | `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`: added edge changes route/event/energy metrics but leaves root-input prediction loss at `1.1725`; the legacy test assumes any topology change changes prediction loss. `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary`: expects a final clock of 0.0/1.0, while E2 reset occurs at the declared settling boundary (observed 5.0). | Old scalar-path assertions do not match ACP-0006 prediction ownership or E2 local reset timestamp. These are not evidence that route/order/reset mechanics failed; update the consumer-specific observable or explicitly preserve its legacy condition in a separate authorization. |
| `tests/test_luna12l_temporal_scale.py` (11) | Six E2 positive-delay representability failures: `test_labels_do_not_change_canonical_four_class_trace`; `test_scale_runner_retains_all_policies_and_causal_evidence`; `test_requested_policy_is_executed_by_classifier[fixed]`; `test_policy_changes_classifier_execution_state`; `test_requested_scale_reaches_classifier_configuration`; `test_policy_scale_cross_product_preserves_provenance_and_serialization`. Five structural/default-model failures: `[baseline]`, `[random]`, `[temporal]`, `[reversed]` instances of `test_requested_policy_is_executed_by_classifier`, plus `test_condition_fails_on_classifier_provenance_mismatch` (fails before the intended provenance mismatch because the classifier configuration requests unsupported structural plasticity). | Six are the E2 defect assigned to Luna-23; five are old structural classifier consumers and must remain outside the fixed-topology first integration. |
| `tests/test_spiral_benchmark.py` (1) | `test_control_results_are_deterministic_and_include_required_order_controls`: the first no-learning E2 control fails on the positive-delay representability case before the later structural control. | E2 defect assigned to Luna-23; not a structural-plasticity-only failure. |
| `tests/test_temporal_analysis.py` (3) | `test_flat_metrics_and_changing_topology_are_reported`; `test_rejection_reason_aggregation_preserves_observed_reasons`; `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation`. Their replay fixture uses the structural CPU experiment path, rejected under EXCURSION_V1. | Legacy structural experiment/replay compatibility. The synthetic offline-only lifetime and edge-use cases pass. |
| `tests/test_viewer_3d.py` (3) | `test_layout_and_scene_generation_are_deterministic_and_diagnostic`; `test_topology_deltas_and_bounded_prune_highlights`; `test_playback_filters_selection_neighborhood_and_metrics`. Their shared scene fixture requests structural CPU training, rejected under EXCURSION_V1. | Viewer remains downstream-only; its structural replay source needs an explicit model/compatibility decision. |

Totals reconcile: 7 positive-delay E2 failures; 15 structural-plasticity /
legacy-default failures; 3 visualization scalar-field failures; and 2
Luna-12E legacy-observable failures = 27.

## Consumer migration matrix and authorization

| Consumer class | Correct bounded treatment | Authorized now? |
|---|---|---|
| CPU TPCV-1 snapshots, temporal replay analysis and 3D viewer | Keep capture downstream-only. Do not invent an activation for E2. Decide separately between explicitly selected TANH_LEGACY snapshots and a separately specified E2-compatible visualization record contract. | No |
| Structural/plasticity experiment controls in Luna-12B, Luna-12L, spiral benchmark, temporal analysis and viewer fixtures | ACP-0006 deliberately rejects structural plasticity in its EXCURSION_V1 integration. Preserve the legacy experiment as explicitly TANH_LEGACY or defer until separately authorized structural semantics exist; do not silently enable plasticity on E2. | No |
| Luna-12E topology causal/readout tests | Update the expected causal observable to a valid E2-path consequence, or explicitly retain the original scalar-path experiment. Do not assume prediction loss must change when an edge changes routed activity. | No |
| Accepted integrated E2 logical-time path | Correct the positive-delay-to-representable-timestamp boundary and add a focused E2 regression without changing neuron equations. | **Luna-23 authorized** |
| ACP-0006 integrated IR-2 startup | Reject residual assigned provenance and sticky truncation, preserve standalone round trips and schema revision 1. | **Luna-24 authorized** |

The two corrective tasks have non-overlapping implementation ownership and no
ACP is indicated unless a compatible correction proves impossible. Downstream
migration is **not authorized** while the integrated path has the two
reproduced defects and the dataset evidence remains incomplete. The agents
must stop and return evidence if their scoped fix requires new semantics.

## Dataset evidence

The Luna-22 handoff reports a UCI Character Trajectories run: 2,858 examples,
20 classes, 160 stratified subset examples (80/40/40 train/validation/test),
seed `20261003`, validation accuracy `0.125`, test accuracy `0.175`, and
10.0 logical seconds settling. The raw `.mat` data was present in session-local
storage during this review, but the exact ad-hoc loader/split script and
per-class table were not retained. The reported test subset had zero matched
predictions and prediction loss 0; it does not establish predictive-task
efficacy. Writer-disjointness is unavailable.

**Verdict:** This is useful reported evidence, not a repository-reproducible
benchmark result. The dataset gate is not satisfied because the exact split
and per-class results cannot be independently reconstructed from retained
implementation artifacts. Low accuracy alone does not fail a numerical
threshold; ACP-0006 establishes none.

## A01-A15 audit

| Clause | Review disposition |
|---|---|
| A01 | Scheduler fixtures pass event-triggered execution and no-global-timestep mechanics. The E2 representability failure blocks full valid-workload acceptance. |
| A02 | Local timestamps and event-driven state work in focused tests; strict-future scheduling fails when a positive delay is below the timestamp ULP. Blocked by Luna-23. |
| A03 | Finite delayed Model-B routing is verified. Same-timestamp rounding prevents a valid E2 sequence from continuing; blocked by Luna-23. |
| A04 | Fixed topology, fan-in/out and finite queue/routing bounds are preserved; existing topology regressions and overflow tests pass. |
| A05 | No spatial reservoir dependency was introduced. |
| A06 | Synthetic delayed prediction/error mechanics pass. The reported real-data test has no matched predictions; predictive task efficacy is not established. |
| A07 | Labels remain outside neural inputs; relabeling invariance and delayed local credit tests pass. Dataset efficacy remains unverified. |
| A08 | State, queues, sidecars, provenance, budgets and settling remain explicitly bounded. The E2 rearm error blocks valid temporal completion and must be corrected. |
| A09 | Activity-cost proxy components reconcile in the integration tests; they are not calibrated physical energy. |
| A10 | Existing utility tests and integration parity are preserved; no claim that utility suppresses E2 execution or that energy units are physical. |
| A11 | Synthetic delayed eligibility/reward attribution passes; the dataset handoff reports no matched test credit. |
| A12 | Not applicable; no mandatory pathway count is introduced. |
| A13 | Not applicable; explicit gating remains optional. |
| A14 | First integration correctly fixes topology and rejects structural plasticity. No structural-learning claim is accepted here. |
| A15 | Hardware-neutral software-reference scope only. No FPGA, FPAA, GPU equivalence or hardware validation is claimed. |

No A01-A15 clause text or accepted architecture was changed. ACP-0006 remains
accepted and unchanged.

## Terminal verdict and next bounded work

**Terminal verdict: BLOCKED - NOT CLOSED.** The published Luna-22 implementation
is not accepted as integration-ready. The initial x/unassigned-provenance
correction passes those specific cases but does not close the complete
quiescent-startup gate. The positive-delay representability failure is a
separate E2 component defect that blocks normal non-structural temporal runs.
The real-data evidence is not reproducible and omits required per-class
metrics.

**Luna-23 is authorized / not executed** to implement and verify only the
contract-compatible E2 strict-future timestamp correction in
`.github/agents/luna-23.agent.md`.

**Luna-24 is authorized / not executed** to complete only the integrated IR-2
residual-provenance rejection in `.github/agents/luna-24.agent.md`.

No dataset, visualization, structural-research or Luna-12E downstream
migration is authorized. After both corrective handoffs, Luna-0 must rerun
the focused, prescribed and full suites, resolve the dataset reproducibility
gate, and issue a fresh closure decision. Do not execute a downstream
migration in this review.

## Publication

Review starting revision: `a206f2e8fec8f0c72d9196b2bcca9d2e734c7974`.
The first pushed review-publication commit is recorded in the
`ARCHITECTURE_CHANGELOG.md` entry added with this handoff.
