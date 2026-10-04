# Luna-28 Completion Handoff — EXCURSION_V1 Local Temporal Structural Growth

```yaml
tpcn_handoff:
  agent: "Luna-28 Structural Plasticity and Topology Adaptation"
  luna_identifier: "Luna-28"
  descriptive_name: "EXCURSION_V1 local temporal structural-growth integration"
  task_id: "luna-28-excursion-local-temporal-growth-20261004"
  component: "Opt-in bounded E2 emission observation and post-character growth"
  status: "IMPLEMENTED / PUBLISHED / AWAITING INDEPENDENT REVIEW"
  contract_version: "1.2"
  branch: "main"
  base_revision: "6d6688186742dd8c44b25c6a6c4c0ebaa626758d"
  implementation_revision: "ac321abba6f4772f18fa459d4442e8f4ef4867e4"
  handoff_publication_revision: "512b7ca — docs: record Luna-28 structural growth verification"
  result_revision: "Implementation ac321abba6f4772f18fa459d4442e8f4ef4867e4; handoff published separately"
  authorization:
    - "ACP-0007 accepted contract"
    - "Luna-0 authorization handoff at the base revision"
  owner: "Luna-28"
  classification: ["IMPLEMENTATION", "FOCUSED VERIFICATION"]
  architecture_change: false
  proposal: null
  authorized_scope:
    - "tpcn/experiments.py"
    - "tpcn/experiment_excursion_runtime.py"
    - "tpcn/structural_observation.py"
    - "tests/test_luna28_excursion_structural_growth.py"
    - "workflow/handoffs/luna-28-excursion-local-temporal-growth-20261004.md"
  files_changed:
    - "tpcn/experiments.py"
    - "tpcn/experiment_excursion_runtime.py"
    - "tpcn/structural_observation.py"
    - "tests/test_luna28_excursion_structural_growth.py"
    - "workflow/handoffs/luna-28-excursion-local-temporal-growth-20261004.md"
  environment:
    os: "Windows"
    python: "3.11.5"
    interpreter: "C:\\Users\\zathp\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
  tests_passed:
    - "Focused Luna-28 suite: 44 passed."
    - "Closed-component regression suite: 168 passed."
    - "Full repository suite: 865 passed, 21 known downstream failures, 1 existing CUDA skip; 887 collected; 13.05s."
    - "Collection audit: 887 tests collected; no existing tests removed/renamed/xfail-marked or deselected."
    - "Compile gate: python -m compileall -q tpcn tests passed."
    - "Pylance problems check: no errors in the four implementation/test files."
    - "git diff --check: passed before implementation commit."
  tests_failed:
    - "19 known downstream compatibility failures, all terminating at the intentional E2 structural-observation opt-in guard."
    - "2 stale Luna-12E legacy assertions: prediction-loss delta and final-clock expectation."
  tests_not_run:
    - "Hardware, GPU, FPGA, and hardware-equivalence behavior."
  not_applicable:
    - "Accuracy, prediction-loss, reward, or energy efficacy."
    - "Pruning and N3 edge-parameter learning."
    - "Downstream visualization or experiment consumer migration."
  recommended_next_agent: ["Luna-0 Architecture Guardian"]
```

## Revision, baseline, and scope

The required starting state was verified before implementation: branch `main`,
`HEAD == origin/main ==
6d6688186742dd8c44b25c6a6c4c0ebaa626758d`, with a clean worktree. The
remote subject was `docs: accept ACP-0007 and authorize Luna-28`. The
implementation commit is `ac321abba6f4772f18fa459d4442e8f4ef4867e4`
(`feat: integrate E2 local temporal structural growth`). This handoff is
published separately after that implementation commit.

Only the five authorized files listed above are changed. The implementation
commit contains exactly the four code/test files; this documentation file is
the separate handoff publication. No architecture
contract, ACP, core neuron, topology/controller, prediction, eligibility,
IR-2, visualization, or downstream consumer file was modified. The
fixed-topology `EXCURSION_V1` configuration remains the default.

## Implementation and bounds

Structural observation and E2 growth are both explicitly opt-in. Growth
requires observation and policy identifier `e2_local_temporal`; legacy E2
policy identifiers fail explicitly. `TANH_LEGACY` keeps its historical
compatibility path.

The added `ExperimentConfig` options are `structural_observation`,
`structural_neighbors`, `structural_neighborhood_limit`,
`structural_reverse_observer_limit`, `structural_association_window`,
`structural_history_capacity`, `structural_candidate_capacity`,
`structural_maximum_score`, `structural_growth_delay`, and
`structural_growth_attempt_budget`.

The optional observation hook runs at
`ExcursionCharacterRuntime._consume_emission()` and exposes only emitter ID,
canonical emission event ID, and timestamp. A static, explicit, normalized
directed neighborhood is required for every topology node. Self-neighbors,
duplicates, unknown nodes, excess per-source neighbors, and excess
reverse-observer counts are rejected. Each source owns a bounded
`TemporalAssociationPolicy`; its evidence is new for each character,
score-saturated, frozen after character completion, and discarded after the
single post-character decision. No payload, labels, task feature/loss,
prediction/reward/readout/energy information, or visualization data enters
the score.

The integrated causal fixture uses:

| Bound | Configured value |
|---|---:|
| Nodes | 3 |
| Explicit neighborhoods | `neuron-0: [neuron-2]`; `neuron-1: []`; `neuron-2: []` |
| Per-source neighborhood / reverse-observer limits | 2 / 2 (actual maxima 1 / 1) |
| Association window | 4.0 |
| Per-source history / candidate capacity | 8 / 4 |
| Maximum candidate score | 3 |
| Admitted-edge delay | 0.4 |
| Experiment growth-attempt budget | 4 |
| Topology edge capacity; fan-in / fan-out | 4; 2 / 2 |
| Queue capacity; per-character event budget | 128; 1024 |
| Decision and mutation-history retention | 32 each |

The observation plane performs at most `emission_count * (1 +
reverse_observer_limit)` deliveries. Retained observations and candidates
are bounded by `node_count * history_capacity` and `node_count *
candidate_capacity`, respectively. The controller is authoritative; after
successful admission its replacement topology is adopted by the runner and
the compute network used by subsequent E2 characters. There is no pruning
invocation, and no parameter learning for edge `w`, `d`, or `r`.

## Causal evidence and controls

The integrated character fixture began with only
`neuron-0 -> neuron-1` and `neuron-1 -> neuron-2`, each at delay `0.2`.
Its topology before growth was exactly
`((neuron-0, neuron-1, 0.2), (neuron-1, neuron-2, 0.2))`; after admission it
also contains `(neuron-0, neuron-2, 0.4)`.
Observed actual emission chronology included `neuron-0 @ 4.0`,
`neuron-1 @ 4.7`, and `neuron-2 @ 5.4`. Only the statically permitted
`neuron-0`/`neuron-2` observation relationship contributed the candidate:
source `neuron-0`, destination `neuron-2`, score `1`, configured delay
`0.4`, rank `1`. The candidate was frozen after the completed, successfully
settled character and runtime teardown. The single post-character controller
attempt was admitted; the edge was absent before and present afterward.

A later matched character used the same topology and produced a real delayed
E2 route from `neuron-0` to `neuron-2`: source emission at `4.0`, routed
arrival at `4.4` (emission time plus the admitted `0.4` delay). The causal
fixture recorded 15 processed events without that edge versus 16 with it;
the edge-transfer activity-cost proxy changed from `2.0` to
`2.761594155955765`. Route depth did not decrease. This demonstrates
mechanism-level route use only; no task efficacy is claimed.

Controls exercised:

- Observation-on versus observation-off character results are equal,
  including the runtime result fields and unchanged topology.
- Equal-time emissions and non-neighbor emissions do not create a candidate;
  source-before-neighbor emissions do, within the configured window.
- Candidate score saturation and candidate-capacity rejection are bounded
  and reported. Edge-capacity, fan-in, fan-out, and other rejected admissions
  are deterministic and leave topology unchanged.
- Incomplete settling and exhausted event/attempt budgets discard evidence
  and do not grow. The finite experiment attempt budget is reflected in
  metrics; at most one attempt and one admitted edge occur per character.
- Label mutation and a later suffix do not change the earlier structural
  decision. Character evidence is reset; admitted topology persists within
  the experiment and `ExperimentRunner.reset()` clears the structural state.
- The convergent fan-in fixture admits two legal sources to a shared target
  while retaining its declared capacity.
- Capture-on/off produces identical structural decisions. TPCV-2 capture is
  exercised downstream through the existing CPU capture/parser; no
  visualization implementation was changed.
- The energy field is an uncalibrated `activity-cost-proxy` in model
  diagnostic units, not physical energy and never an input to structural
  evidence.
- `TANH_LEGACY` remains on its historical compatibility path; E2 legacy
  structural policy identifiers are explicitly rejected by the focused
  configuration tests.
- Edge-capacity, fan-in, and fan-out rejection tests confirm stable reason
  reporting and atomic topology preservation. N3 parameters `w`, `d`, and
  `r` are unchanged by admitted growth. A test replaces both pruning entry
  points with fail-fast sentinels and verifies the growth flow never invokes
  either.

## Verification record

Focused acceptance command:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m pytest tests/test_luna28_excursion_structural_growth.py -q
```

**44 passed.** This covers all 33 named mandatory acceptance tests, including
the convergent-fan-in fixture, plus explicit bounded-neighborhood and
reverse-observer validation.

Closed-component regression command:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m pytest tests/test_excursion_integration.py tests/test_e2_multi_excursion.py tests/test_structural_plasticity.py tests/test_luna12i_temporal_association.py tests/test_luna13f_runtime_generated_evidence.py tests/test_cpu_visualization.py tests/test_visualization.py tests/test_experiments.py -q
```

**168 passed.** No Luna-26-named test module was present; E2 integration
coverage in `test_excursion_integration.py` was included for the routing
regression.

Full repository suite:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m pytest -q -rs
```

**21 failed, 865 passed, 1 skipped in 13.05s; 887 tests collected/executed.**
All 21 failures were individually inspected and classified:

| Count | Classification | Failure group and observed cause |
|---:|---|---|
| 4 | KNOWN DOWNSTREAM COMPATIBILITY FAILURE | `test_luna12b_integration.py`: `test_structural_run_is_deterministic_and_has_real_bounded_mutations`, `test_capture_is_downstream_only_for_structural_decisions`, `test_controls_report_behavior_and_topology_without_assuming_benefit`, and `test_structural_evidence_is_label_isolated` still use the pre-ACP-0007 E2 runner contract. Each is rejected by the explicit missing-observation guard. |
| 8 | KNOWN DOWNSTREAM COMPATIBILITY FAILURE | `test_luna12l_temporal_scale.py`: `test_scale_runner_retains_all_policies_and_causal_evidence`, `test_requested_policy_is_executed_by_classifier[baseline]`, `[random]`, `[temporal]`, `[reversed]`, `test_policy_changes_classifier_execution_state`, `test_policy_scale_cross_product_preserves_provenance_and_serialization`, and `test_condition_fails_on_classifier_provenance_mismatch` request the prior E2 structural mode. All stop at the structural-observation guard before old-policy behavior can run. Legacy `baseline`, `random`, `temporal`, and `reversed` policies are not accepted E2 growth policies. |
| 1 | KNOWN DOWNSTREAM COMPATIBILITY FAILURE | `test_spiral_benchmark.py::test_control_results_are_deterministic_and_include_required_order_controls`: its structural-control runner uses the old default E2 growth setup and stops at the same guard. |
| 3 | KNOWN DOWNSTREAM COMPATIBILITY FAILURE | `test_temporal_analysis.py`: `test_flat_metrics_and_changing_topology_are_reported`, `test_rejection_reason_aggregation_preserves_observed_reasons`, and `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` call the old structural training path and stop at the same guard. |
| 3 | KNOWN DOWNSTREAM COMPATIBILITY FAILURE | `test_viewer_3d.py`: `test_layout_and_scene_generation_are_deterministic_and_diagnostic`, `test_topology_deltas_and_bounded_prune_highlights`, and `test_playback_filters_selection_neighborhood_and_metrics` use the old structural-training setup and stop at the same guard. |
| 1 | STALE LEGACY ASSERTION | `test_luna12e_integration.py::test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes` expects prediction loss to differ across a routed edge, but observed loss is identical (`1.1724999999999999`) while event count and activity differ. This is the documented legacy pre-E2 prediction-loss expectation. |
| 1 | STALE LEGACY ASSERTION | `test_luna12e_integration.py::test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` expects the final clock to be zero; the E2 result is `5.0`, matching the documented legacy pre-E2 clock expectation. |

There were **no NEW LUNA-28 REGRESSION**, **UNRELATED PREEXISTING
FAILURE**, or **UNKNOWN — REQUIRES REVIEW** results. The downstream groups
remain unmigrated and were not edited. Luna-12E's two legacy assertions
remain separately classified; no E2 computation change was made.

Collection audit:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m pytest --collect-only -q
```

**887 tests collected in 2.38s.** Relative to the pre-Luna-28 collection of
843, the 44 added tests account for the entire increase. No existing tests
were deleted, renamed, xfail-marked, unconditionally skipped, or deselected.
The single skip is the pre-existing conditional
`tests/test_gpu_visualization.py:61` skip because CUDA is unavailable.

Static compilation:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m compileall -q tpcn tests
```

**Passed.** Pylance reported no errors in all four changed
implementation/test files. `git diff --check` passed immediately before
the implementation commit.

The previously recorded dependency result remains: five structural
downstream groups had 19 failures and 12 passes, with all 19 failures
terminating at the intentional guard; 69 structural/evidence regression
tests passed. Those remain dependency evidence, not post-guard results.

## Architecture and efficacy audit

| Invariant | Result | Basis / scope |
|---|---|---|
| A01 | PASS | Event-triggered emissions and local delivery; no global neural timestep was added. |
| A03 | PASS | Configured candidate edge delay is finite and strictly positive; no delay learning. |
| A04 | PASS | Neighborhood, reverse observers, history, candidates, scores, growth attempts, queue, event execution, topology, and retained histories are bounded. |
| A06 | PASS | The later matched E2 character records an actual delayed routed excursion over the admitted edge. |
| A07 | PASS | Candidate evidence is local and emission-only; task labels, payload magnitude, global traces, reward, prediction results, and utility do not score candidates. |
| A08 | PASS | Explicit deterministic ordering, bounded candidate selection, per-character freeze/discard, and finite attempt budget. |
| A10 | PASS | Energy remains an uncalibrated activity-cost proxy for diagnostics only. |
| A11 | PASS | No prediction, prediction-error, eligibility, classifier, or reward semantics were changed. |
| A14 | PASS WITH SCOPE | Accepted ACP-0007 bounded growth experiment only; no architecture-wide or consumer promotion. |
| A15 | PASS FOR SOFTWARE-REFERENCE PORTABILITY | Hardware-neutral Python reference path only; no hardware-equivalence result. |

```text
mechanism validity: ESTABLISHED
task efficacy: NOT ESTABLISHED
resource benefit: NOT ESTABLISHED
```

The causal route proves mechanism use, not classification or prediction
benefit. Event count and the edge-transfer proxy increased in the causal
fixture; neither is a resource benefit claim. Luna-13F's negative efficacy
result is unchanged.

## Verdict and limits

**PASS — Luna-28 implementation and focused verification complete; return
to Luna-0 for independent review.** The 21 full-suite failures are confined
to the documented downstream compatibility and stale legacy assertion
groups; the 44 added Luna-28 tests and all 168 closed-component regressions
pass. This does not establish accuracy/prediction/reward/resource benefit,
pruning, N3 learning, hardware equivalence, downstream readiness, or
architecture promotion. No successor is authorized by this handoff.
