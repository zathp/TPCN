# Luna-0 Independent Review Handoff — Luna-28 EXCURSION_V1 Local Temporal Growth

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of Luna-28 EXCURSION_V1 local temporal structural growth"
  task_id: "luna-0-independent-review-luna-28-excursion-local-temporal-growth-20261004"
  component: "ACP-0007 bounded E2 emission-observation and post-character growth path"
  status: "complete"
  contract_version: "1.2"
  branch: "main"
  base_revision: "028b5793917efb2c1af279691d1611427de3a86c"
  result_revision: "028b5793917efb2c1af279691d1611427de3a86c (reviewed source; governance publication is separate)"
  dependencies:
    - "Accepted ACP-0007"
    - "Luna-0 owner decision and Luna-28 authorization"
    - "Luna-28 implementation handoff"
  owner: "Luna-0 Architecture Guardian"
  classification: ["INDEPENDENT REVIEW", "GOVERNANCE CLOSURE"]
  hypothesis: "The published Luna-28 path implements the accepted bounded, causal, local, deterministic, growth-only ACP-0007 mechanism without changing unrelated canonical behavior."
  counter_hypothesis: "A lifecycle, information-boundary, resource-bound, causal-routing, compatibility, or regression defect would block closure."
  interfaces_relied_on:
    - "ExcursionCharacterRuntime._consume_emission() optional observer"
    - "StructuralObservationPlane and TemporalAssociationPolicy"
    - "StructuralPlasticityController and BoundedTopology"
    - "ExperimentRunner post-character execution and topology synchronization"
  label_information_boundary:
    - "Labels, task results, payload magnitude, reward, prediction loss, readout, energy and future suffixes do not score candidates."
    - "External labels and later suffix controls preserve a completed frozen decision."
  timing_assumptions:
    - "Association requires strictly increasing emission timestamps within the finite configured window."
    - "Admitted edge delay is the configured finite positive delay; no delay learning occurs."
    - "Actual later E2 route arrival is source emission time plus edge delay."
  reset_boundaries:
    - "Evidence is character-local and discarded after the post-character decision."
    - "Experiment reset creates fresh structural state; admitted topology persists only within the experiment."
  resource_bounds:
    - "At most emission_count * (1 + reverse_observer_limit) observation deliveries."
    - "History and candidates bounded per source; controller candidate bound is node_count * per_source_candidate_capacity."
    - "Topology edge, fan-in/out, routing, runtime queue/event, attempt-budget and retained-history limits remain finite."
  authorized_scope:
    - "Read-only independent source, test, architecture and publication-lineage review."
    - "Governance-only review handoff, workflow and changelog publication after passing audit."
  unauthorized_scope:
    - "Production or test implementation changes."
    - "Downstream migration, efficacy claims, pruning, N3 parameter learning, A14 promotion or hardware work."
  controls:
    - "Observation enabled versus disabled."
    - "Equal-time and non-neighbor emission exclusion."
    - "Label mutation, future-suffix and capture-on/off non-interference."
    - "Incomplete character, budget exhaustion, active-runtime mutation, finite topology and deterministic replay."
    - "Fixed-topology and TANH_LEGACY compatibility."
  measurements:
    - "Later routed excursion at 4.4 from emission at 4.0 over an admitted 0.4-delay edge."
    - "Two-source/two-candidate aggregate bound check: 2 candidates <= 4 controller capacity."
    - "Independent full suite: 887 collected; 865 passed, 21 failed, 1 skipped."
  information_boundary_check:
    - "Observed canonical emission identity/timestamp only; no payload magnitude or global/task-derived evidence."
    - "Observation plane remains separate from neural event queues and downstream visualization."
  hardware_mapping:
    - "Software reference only; no FPGA, FPAA, hybrid or hardware-equivalence validation."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "Contract version 1.2 and the substantive scope of A01-A15."
    - "Fixed-topology EXCURSION_V1 default and TANH_LEGACY compatibility."
    - "Prediction/error, eligibility, readout, reward, energy and visualization semantics."
  architecture_change: false
  proposal: "ACP-0007 remains accepted; no amendment or promotion."
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna-28-excursion-local-temporal-growth-20261004.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Focused Luna-28 suite: 44 passed."
    - "Closed-component regression suite: 168 passed."
    - "Collection audit: 887 tests collected."
    - "python -m compileall -q tpcn tests: passed."
    - "Pylance problems check for the four Luna-28 implementation/test files: no errors."
    - "Independent repeated-run probe: same decision, topology and later route trace."
    - "Independent aggregate candidate-capacity probe: 2 candidate records within 4-slot controller capacity."
    - "git diff --check: passed before review publication."
  tests_failed:
    - "Full repository suite: 21 failures; all reconcile to 19 known downstream opt-in-guard failures and 2 stale Luna-12E assertions; no Luna-28 regression."
  tests_not_run:
    - "Hardware, GPU execution beyond the existing CUDA-unavailable skip, FPGA, FPAA and hardware equivalence."
  assumptions:
    - "The review brief's identifier F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb does not resolve to a Git commit; published Git SHA ac321abba6f4772f18fa459d4442e8f4ef4867e is used."
    - "Previously published focused/regression/static checks are independently repeated or inspected as described below."
  unresolved:
    - "The full repository remains non-green due to the documented downstream compatibility and stale legacy assertion groups."
    - "Task efficacy and resource benefit are not established."
    - "No downstream integration or hardware readiness is established."
  recommended_next_agent:
    - "No successor is authorized. Any downstream migration or new efficacy experiment requires a separate project-owner/Luna-0 decision."
```

## Outcome, baseline and publication lineage

**PASS — Luna-28 is independently verified and closed for its authorized
mechanism scope.** This is not a finding that the full repository is
integration-ready and is not a task-efficacy or resource-benefit result.
No implementation or test file was changed during the review.

**OBSERVED:** focused and closed-component suites pass; independent source
inspection and adversarial probes confirm bounded local evidence, quiescent
growth, deterministic replay and later causal routing. The full suite retains
the 21 classified failures below.

**INFERRED:** the published implementation satisfies the accepted ACP-0007
mechanism criteria within its tested CPU EXCURSION_V1 scope.

**HYPOTHESIZED:** task or resource benefit is not tested by this closure and
remains unestablished.

The review began on clean `main` with
`HEAD == origin/main == 028b5793917efb2c1af279691d1611427de3a86c`.
Git lineage confirms:

- Authorization baseline: `6d6688186742dd8c44b25c6a6c4c0ebaa626758d`.
- Implementation: `ac321abba6f4772f18fa459d4442e8f4ef4867e4`.
- Implementation delta from its parent: exactly
  `tests/test_luna28_excursion_structural_growth.py`,
  `tpcn/experiment_excursion_runtime.py`, `tpcn/experiments.py`, and
  `tpcn/structural_observation.py`.
- Handoff publication: `512b7cab73446ba036cb5e9189afe49e4b9c2393`, adding only
  `workflow/handoffs/luna-28-excursion-local-temporal-growth-20261004.md`.
- Revision pin: `028b5793917efb2c1af279691d1611427de3a86c`, changing only that
  handoff.

The additional implementation identifier in the review brief,
`F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb`, failed Git commit-object
resolution. It is not used as provenance. The source SHA above is verified
against the published commit and handoff.

## Review findings

No release-blocking defect was found in the owned Luna-28 mechanism:

- **Evidence and locality:** observation originates only from actual
  `ExcursionEmission` callbacks. The plane validates explicit static directed
  neighborhoods, bounded reverse-observer fanout, finite history/candidate
  capacities and emission timestamps. Candidate score uses strictly
  earlier-to-later count evidence, saturates at its configured limit, and
  carries the configured positive edge delay. No labels, payload magnitude,
  task metrics, prediction/reward/readout data, energy, visualization data,
  or global post-hoc trace is used.
- **Lifecycle and mutation:** the runner requires successful complete
  character execution and teardown before freezing evidence and attempting
  growth. Mutation is blocked while runtime work is active. Incomplete or
  budget-exhausted characters do not grow; character evidence is consumed,
  while admitted topology persists for later characters in the experiment.
- **Boundedness and convergence:** per-source evidence aggregates to a finite
  controller bound of `node_count * candidate_capacity`. An independent
  probe generated two local candidates with per-source capacity 1 on a
  four-node plane; both fit the four-candidate controller bound. Existing
  controller admission continues to enforce edge, routing, fan-in, fan-out,
  locality, atomicity and deterministic rejection constraints. The declared
  convergent-fan-in capacity test and configuration leave a legal bounded
  convergent case available.
- **Causal integration and replay:** independent repeated executions yielded
  matching decisions, topology and later route trace. The later actual route
  is `neuron-0 -> neuron-2` at `4.4`, from source emission at `4.0` plus
  admitted delay `0.4`. This establishes mechanism use only; it does not
  establish task benefit.
- **Non-interference and compatibility:** focused tests cover observation
  on/off equivalence, labels/future suffixes, capture-on/off, completed
  character invariance, fixed-topology availability and explicit policy
  validation. Source review and a direct configuration probe confirm
  `TANH_LEGACY` remains separate compatibility behavior. No pruning or
  edge-parameter (`w`, `d`, `r`) learning was introduced.

### A01-A15 assessment

| Clause | Review result | Evidence / boundary |
|---|---|---|
| A01 | PASS | Events remain causal; no global neural timestep or execution-batch clock was introduced. |
| A02 | PASS | Existing event-driven local timestamp behavior is used; no neuron state/equation change. |
| A03 | PASS | Edge delay is finite, positive and configured; the later route arrives at `4.0 + 0.4 = 4.4`. |
| A04 | PASS WITH SCOPE | Finite topology, routing, fan-in/out, candidate and attempt limits remain enforced; a bounded convergent route is testable. |
| A05 | PASS | No spatial-reservoir dependency is introduced. |
| A06 | PASS | Existing predictive coding and explicit error-event behavior are unchanged; the admitted edge has a later real routed excursion. |
| A07 | PASS | Structural evidence is emission-local and label/task/global-state isolated. |
| A08 | PASS | Existing bounded runtime plus finite local evidence, queue/event and growth budgets; deterministic reset/lifecycle. |
| A09 | PASS | Energy computation is unchanged; activity cost remains diagnostic proxy, not calibrated physical energy. |
| A10 | PASS | No energy-minimization objective or utility change; no efficacy claim. |
| A11 | PASS | Prediction, error, eligibility, delayed credit and reward semantics are unchanged. |
| A12-A13 | PASS / NOT A REQUIREMENT | No mandatory ten-pathway or explicit-gate behavior is introduced. |
| A14 | PASS WITH EXPERIMENTAL SCOPE | Only the accepted ACP-0007 opt-in growth mechanism is reviewed; no promotion or task-utility claim. |
| A15 | PASS FOR SOFTWARE REFERENCE ONLY | Hardware-neutral software path; no FPGA/FPAA/hybrid or equivalence validation. |

## Independent validation

Environment: Windows, Python 3.11.5 at
`C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe`.

| Command or procedure | Observed result | Classification |
|---|---|---|
| `python -m pytest tests/test_luna28_excursion_structural_growth.py -q` | 44 passed | PASS |
| `python -m pytest tests/test_excursion_integration.py tests/test_e2_multi_excursion.py tests/test_structural_plasticity.py tests/test_luna12i_temporal_association.py tests/test_luna13f_runtime_generated_evidence.py tests/test_cpu_visualization.py tests/test_visualization.py tests/test_experiments.py -q` | 168 passed | PASS |
| `python -m pytest -q -rs` | 865 passed, 21 failed, 1 skipped in 13.56s | FAIL overall; failures reconciled below |
| `python -m pytest --collect-only -q` | 887 collected; increase of 44 accounted for by Luna-28 module | PASS |
| `python -m compileall -q tpcn tests` | Passed | PASS |
| Pylance problems for four changed implementation/test files | No errors | PASS |
| Direct deterministic/adversarial runtime probes | Causal route, non-neighbor isolation, equal-time exclusion, saturation, invalid locality rejection, evaluation immutability, active-runtime mutation rejection, incomplete-character discard and budget exhaustion verified | PASS |
| Repeated independent fresh-run probe | Same admission decision, topology and real later route trace | PASS |
| Aggregate capacity probe | Two observed candidates fit four-slot controller capacity for four nodes at per-source capacity one | PASS |
| `git diff --check` before governance changes | Passed | PASS |
| Hardware, GPU hardware execution, FPGA, FPAA, hardware equivalence | Not run | NOT RUN |

### Full-suite failure reconciliation

The full-suite failures reproduce the published classifications and contain no
Luna-28 test regression:

| Count | Tests | Cause |
|---:|---|---|
| 4 | `test_luna12b_integration.py`: `test_structural_run_is_deterministic_and_has_real_bounded_mutations`, `test_capture_is_downstream_only_for_structural_decisions`, `test_controls_report_behavior_and_topology_without_assuming_benefit`, `test_structural_evidence_is_label_isolated` | Old downstream E2 setup is rejected at the intentional missing-observation opt-in guard. |
| 8 | `test_luna12l_temporal_scale.py`: `test_scale_runner_retains_all_policies_and_causal_evidence`, `test_requested_policy_is_executed_by_classifier[baseline]`, `[random]`, `[temporal]`, `[reversed]`, `test_policy_changes_classifier_execution_state`, `test_policy_scale_cross_product_preserves_provenance_and_serialization`, `test_condition_fails_on_classifier_provenance_mismatch` | Prior E2 structural policy contract; fails at the explicit guard before old-policy behavior. |
| 1 | `test_spiral_benchmark.py::test_control_results_are_deterministic_and_include_required_order_controls` | Structural-control runner uses the old E2 growth setup and fails at the same guard. |
| 3 | `test_temporal_analysis.py`: `test_flat_metrics_and_changing_topology_are_reported`, `test_rejection_reason_aggregation_preserves_observed_reasons`, `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` | Old structural-training path fails at the same guard. |
| 3 | `test_viewer_3d.py`: `test_layout_and_scene_generation_are_deterministic_and_diagnostic`, `test_topology_deltas_and_bounded_prune_highlights`, `test_playback_filters_selection_neighborhood_and_metrics` | Old structural-training setup fails at the same guard. |
| 1 | `test_luna12e_integration.py::test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes` | Stale legacy assertion expects prediction-loss change; observed loss remains `1.1724999999999999` although routed activity differs. |
| 1 | `test_luna12e_integration.py::test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` | Stale legacy clock assertion expects zero rather than the observed post-evaluation E2 horizon timestamp `5.0`. |

The one skip is the existing
`tests/test_gpu_visualization.py:61` conditional skip because CUDA is
unavailable. The 19 downstream failures are not post-guard migration results;
the two Luna-12E assertions remain separately classified. Neither group was
modified or silently reclassified by this review.

## Architecture disposition, limitations and next assignment

ACP-0007 remains accepted and unchanged. Architecture contract version 1.2
and A01-A15 are unchanged. This review closes only the implementation and
focused mechanism verification. Full-suite green status, downstream
integration, accuracy/prediction/reward/resource efficacy, pruning, N3
learning, A14 promotion and hardware equivalence remain **NOT ESTABLISHED**.
The existing full suite is not integration-ready while those downstream
failures remain.

No successor or downstream migration is authorized. Any compatibility
migration or separate efficacy experiment requires a new bounded assignment
and the applicable project-owner/Luna-0 authorization. The fixed-topology
EXCURSION_V1 configuration remains the default and rollback path.

## Reproduction and rollback

Re-run the focused, regression, collection and full-suite commands from the
published Luna-28 handoff using the stated Python 3.11.5 interpreter. No
production rollback is required by this review. Preserve the implementation
and accepted ACP-0007; reverting to the pre-growth baseline would remove the
reviewed opt-in mechanism and is not requested.
