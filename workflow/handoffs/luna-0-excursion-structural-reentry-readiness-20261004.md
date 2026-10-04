# Luna-0 EXCURSION_V1 Structural Re-entry Readiness

**BLOCKED — EXCURSION_V1 STRUCTURAL RE-ENTRY REQUIRES ARCHITECTURE
DECISION**

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  luna_identifier: "Luna-0 EXCURSION_V1 structural re-entry readiness"
  descriptive_name: "Structural evidence and dependency-root review"
  task_id: luna-0-excursion-structural-reentry-readiness-20261004
  component: "EXCURSION_V1 structural evidence, mutation lifecycle, downstream blockers"
  status: blocked
  contract_version: "1.1"
  branch: main
  base_revision: d9abe5e3a5b9b3c6d6049ac4c64647463c33ba2d
  result_revision: "governance publication; see changelog entry"
  dependencies: ["accepted ACP-0006", "closed Luna-27", "classified Luna-12E failures"]
  owner: "Luna-0 / project owner"
  classification: ["GOVERNANCE", "ARCHITECTURE-READINESS REVIEW", "VERIFICATION"]
  hypothesis: "The current guard is the immediate test dependency root, but removing it alone would not produce contract-compliant E2 structural learning."
  counter_hypothesis: "An already accepted E2-local evidence producer and complete mutation lifecycle exist and can be integrated without architectural choice."
  interfaces_relied_on:
    - "ExperimentConfig and ExperimentRunner"
    - "ExcursionCharacterRuntime"
    - "BoundedTopology"
    - "CandidateEvidence and StructuralPlasticityController"
    - "TemporalAssociationPolicy"
    - "TPCV-2 downstream capture"
  label_information_boundary:
    - "No labels, outer readout, global metrics, held-out outcomes, or future data may determine structural admission."
  timing_assumptions:
    - "Quiescent mutation boundary recommended; active-character mutation is not authorized."
    - "Structural decisions need a frozen pre-decision evidence set and deterministic equal-time ordering."
  reset_boundaries:
    - "ACP-0006 preserves topology over character reset and destroys the model/topology at experiment reset."
    - "Evidence/candidate persistence across characters and epochs remains undecided for E2 integration."
  resource_bounds:
    - "Existing controller bounds candidates, growth, edge capacity, fan-in/out, routing capacity and deterministic admission."
    - "Any E2 evidence history and mutation history must also remain finite."
  authorized_scope:
    - "Read-only architecture/evidence review, focused dependency tests, and governance-document publication."
  unauthorized_scope:
    - "Production or test-code changes, removal/weakening of the E2 guard, structural runtime integration, and Luna-28 creation/execution."
    - "N3 edge-parameter learning, pruning integration, and downstream consumer migrations."
  controls:
    - "Five named downstream test groups"
    - "Existing structural-controller and evidence-producer regression tests"
  measurements:
    - "First failing exception per test; source provenance and runtime mutation boundaries; evidence/policy semantics"
  information_boundary_check:
    - "Historical ExperimentRunner score is post-character aggregate, not proven source-local evidence."
  hardware_mapping:
    - "No hardware implementation or equivalence claim; A15 remains untested here."
  architecture_invariants_touched: ["A01", "A03", "A04", "A06", "A07", "A08", "A10", "A11", "A14", "A15"]
  preserves:
    - "ACP-0006 §17 fixed-topology first-integration boundary"
    - "Luna-13F negative result for useful-growth prediction"
    - "Luna-12E routed-topology causation classification"
  architecture_change: false
  proposal: "Draft ACP-0007; pending owner decision"
  files_changed:
    - "workflow/handoffs/luna-0-excursion-structural-reentry-readiness-20261004.md"
    - "workflow/docs/architecture_proposals/ACP-0007.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "69 structural/evidence controller tests"
    - "12 of 31 tests in the five downstream groups"
    - "git diff --check"
  tests_failed:
    - "19 of 31 downstream-group tests stop at the intentional EXCURSION_V1 structural-mode guard"
  tests_not_run:
    - "Full repository suite"
    - "Any test with the guard bypassed or a production structural E2 path"
    - "Hardware/GPU equivalence"
  assumptions:
    - "The current test group failures are dependency evidence, not proof that all post-guard downstream assertions pass."
  unresolved:
    - "Actual E2-local evidence feed and score semantics"
    - "TemporalAssociationPolicy production promotion"
    - "Candidate destination and propagation-delay provenance"
    - "Evidence chronology, freeze, consumption, and cross-character/epoch state"
    - "Pruning contract and incomplete-settling behavior"
  recommended_next_agent:
    - "Project owner / architecture decision-maker to review Draft ACP-0007; then Luna-0 to issue a bounded dispatch or close the proposal"
```

## Starting state and scope

**OBSERVED.** Review began at clean `main` with
`HEAD == origin/main == d9abe5e3a5b9b3c6d6049ac4c64647463c33ba2d`,
subject `docs: classify Luna-12E downstream failures`. No implementation
files or tests were changed. Luna-22 through Luna-27 remain closed as stated
in the authoritative workflow. The prior Luna-12E classification is not
reopened.

This is a governance-only decision. ACP-0006 §17 continues to require fixed
topology for the first integrated path, with structural mode disabled. It
permits later re-entry only under the existing local-evidence contract and
separate authorization; it does not approve a specific E2 evidence producer.
Draft ACP-0007 records the unresolved architecture decision. It is not
accepted, does not modify A01-A15 or ACP-0006, and is not an implementation
authorization.

## Structural dependency reproduction

Exact command:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m pytest tests/test_luna12b_integration.py tests/test_luna12l_temporal_scale.py tests/test_spiral_benchmark.py tests/test_temporal_analysis.py tests/test_viewer_3d.py -q
```

**OBSERVED:** `19 failed, 12 passed in 1.72s`. Every one of the 19 failures
raised the same `ValueError` from `ExperimentConfig.__post_init__`:
`structural plasticity is unavailable in the excursion integration`. No
failing test reached its downstream classifier/replay/viewer assertions after
that guard. Some Luna-12L capacity-pressure fixture work executes before its
classifier configuration raises. This establishes the immediate dependency
root, not that all later assertions will pass when a structural E2 path exists.

| Group | Failing tests | Immediate point of failure |
|---|---:|---|
| Luna-12B | 4 | `test_structural_run_is_deterministic_and_has_real_bounded_mutations`, `test_capture_is_downstream_only_for_structural_decisions`, `test_controls_report_behavior_and_topology_without_assuming_benefit`, `test_structural_evidence_is_label_isolated`; run/config construction |
| Luna-12L | 8 | `test_scale_runner_retains_all_policies_and_causal_evidence`, `test_requested_policy_is_executed_by_classifier` for baseline/random/temporal/reversed, `test_policy_changes_classifier_execution_state`, `test_policy_scale_cross_product_preserves_provenance_and_serialization`, `test_condition_fails_on_classifier_provenance_mismatch`; classifier config |
| Spiral benchmark | 1 | `test_control_results_are_deterministic_and_include_required_order_controls`; explicit structural control in `run_controls()` |
| Temporal analysis | 3 | `test_flat_metrics_and_changing_topology_are_reported`, `test_rejection_reason_aggregation_preserves_observed_reasons`, `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation`; structural replay construction |
| 3D viewer | 3 | `test_layout_and_scene_generation_are_deterministic_and_diagnostic`, `test_topology_deltas_and_bounded_prune_highlights`, `test_playback_filters_selection_neighborhood_and_metrics`; `_scene()` replay construction before viewer state |

The other 12 selected tests passed. No bypass/monkeypatch of the intentional
guard was used. Full-suite status remains the previously reported
implementation-run `821 passed, 21 failed, 1 skipped`; this review did not
rerun the full suite. The two remaining Luna-12E failures are not included in
this rerun and remain classified as legacy loss-delta/exact-clock observables,
not failures of routed-topology causation.

Relevant existing structural/evidence tests:

```text
python -m pytest tests/test_structural_plasticity.py tests/test_luna12i_temporal_association.py tests/test_luna13f_runtime_generated_evidence.py tests/test_luna13e_post_pruning_admission.py tests/test_luna13d_finite_resource.py tests/test_luna13b_temporal_crossover.py tests/test_luna13c_causal_utility.py -q
```

**OBSERVED:** `69 passed in 5.63s`. This preserves their declared experiment
contracts; it does not promote those fixtures into the integrated E2 path.

## Dependency graph and downstream dispositions

```text
Current EXCURSION_V1 + structural_plasticity guard
    |
    +--> Luna-12B: 4/4 structural CPU integration tests fail at config
    +--> Luna-12L: 8/8 structural classifier conditions fail at config
    +--> Spiral benchmark: explicit plasticity control fails at config
    +--> Temporal analysis: 3/3 structural replay fixtures fail before analysis
    +--> 3D viewer: 3/3 structural replay fixtures fail before viewer state
```

The guard is the directly observed test root for all 19. Removing it alone is
not a valid remedy:

- **Luna-12B:** determinism, bounded admission, capture non-interference,
  behavior/topology reporting, and label isolation remain useful acceptance
  goals. They need E2-specific checks, especially a real delayed routed
  excursion caused by accepted growth. The old assertions for activity/loss
  are not automatically valid for E2.
- **Luna-12L:** its scale/policy experiment is not purely a structural
  integration test. For non-fixed policies,
  `_classification_metrics()` enables plasticity and requests `baseline`,
  `random`, `temporal`, or `reversed`; the experiment's policies are
  fixture/control choices and do not supply an accepted E2-local score. Its
  eight failures stop at the guard, so there is no observed post-guard test
  failure yet. It remains a separate experimental consumer; growth
  authorization would not certify these policies.
- **Spiral benchmark:** the structural condition is an explicit experimental
  comparison. It must not become valid automatically merely because an E2
  structural mode is later authorized. Its evidence producer and task-level
  protocol need separate review.
- **Temporal analysis:** all three failed tests call the blocked replay
  producer. The pure replay-analysis tests passed. The analysis remains
  downstream-only; after structural E2 replay exists, separate consumer tests
  must verify the actual TPCV metrics/schema and avoid making analysis a
  mutation input.
- **3D viewer:** all three tests fail in `_scene()` while obtaining a
  structural replay, before viewer semantics execute. The viewer remains
  downstream-only and must not become a Luna-28 dependency.
- **Luna-12E:** the two legacy assertions remain separate. The published
  classification already shows edge-caused routed activity (12→14 events,
  route depth 0→1, edge-transfer proxy 0→1.358357398350786) despite unchanged
  prediction loss; exact old post-run clock values are not current E2 reset
  invariants.

## Historical ExperimentRunner evidence audit

**OBSERVED.** `_execute()` runs all workload examples, then calls
`_adapt_topology()` once after that pass when `update=True`. E2
`_run_excursion_example()` creates a per-character runtime with the same
`_topology` held by `ExperimentRunner`, calls `end_character()`, and returns
only after the runtime destroys its character queue and sidecar. `_ensure_topology()`
also gives the controller and `_ComputationalNetwork` the same topology.
After pruning replaces the controller's topology, the runner installs that
topology into `_network` for future routing. This is the correct shared-graph
intent and the current full-pass mutation point is quiescent for these
character runtime objects.

The timing point is not enough to make its score legal:

| Input to `_adapt_topology()` | Observed producer/meaning | Local-evidence finding |
|---|---|---|
| `source = nodes[index % len(nodes)]` | source chosen by position in completed example list | Not a source-local observation; depends on workload ordering/index |
| destination | configured endpoint policy (`baseline`, `temporal`, `reversed`) or seeded random choice | Candidate-generation experiment, not derived from the source's local E2 evidence; endpoint policy cannot be promoted by implication |
| `run.feature` | E2 `ExcursionCharacterResult.feature`, an aggregate readout-source excursion mean returned after `END_CHARACTER` | Outer/readout aggregate, not evidence shown to be available to the selected source |
| `run.loss` | character prediction-loss total from matched prediction errors | Label-free is not enough; aggregate post-character prediction/error statistic, with no provenance tying score to the candidate source |
| score | `abs(run.feature) + run.loss` | Experiment-level/postprocessed score; not accepted source-local candidate score |
| epoch / evidence ID | workload pass and enumeration metadata | May name a deterministic decision but cannot serve as local structural evidence |
| propagation delay | fixed `1.0` | Finite and positive, but not derived from local candidate evidence in this integration |
| pruning score | `abs(run.feature)` mapped by enumerating edges | Not edge-use, last-use age, local utility, or a locally attributed cost; no valid pruning evidence |

The `_adapt_topology()` score must be replaced for any E2 re-entry. Setting
`observer=source` in `CandidateEvidence` does not establish locality. The
historical `fixed` policy also falls through to the baseline destination when
structural mode is true; the E2 integration must have an independently
verified fixed/no-mutation control rather than reusing this branch.

## Existing controller and evidence mechanism

**OBSERVED.** `CandidateEvidence` validates distinct nonempty endpoints,
finite score, positive finite delay and source-observer identity.
`StructuralPlasticityController` validates endpoint membership/locality,
bounds candidate storage, orders ties deterministically, and uses the public
topology API for growth. `adapt_many()` uses bounded atomic admission.
`prune()` leaves already queued in-flight events alone. These are useful
controller/topology contracts; they do not validate evidence provenance or
pruning-score origin.

**OBSERVED.** `TemporalAssociationPolicy` keeps bounded per-observer event
history and bounded score/candidate state, increments a candidate score for
earlier/later observations within a configured window, and emits
`CandidateEvidence(observer=source, source=source, destination=observed node,
score=count, propagation_delay=configured positive delay)`. Its timing window,
score cap, source/destination mapping, event feed, and reset/use context were
experimental in Luna-12I; that handoff explicitly says no A14 promotion and
that full ExperimentRunner task-level integration was not tested.

**OBSERVED.** Luna-13F uses that policy in a bounded CPU fixture around
`TPCNNeuron`, with fixture-addressed candidate observations delivered to one
source. Its final closure supports the tested runtime evidence mechanism and
canonical admission, passes locality/chronology/future/label controls, but
does **not** support useful-growth prediction or resource benefit. It closed
as a negative result and explicitly leaves successors unauthorized.

**Decision.** Selecting `TemporalAssociationPolicy` for ordinary
EXCURSION_V1 event processing would be **B — promotion of an experimental
fixture mechanism into integrated behavior**, not a mere public-API reuse.
The public export and A07/A14 permission do not define which E2 events the
source can observe or how the source identifies candidate destinations. The
Luna-13F fixture's arbitrary addressed candidate observations are not proof
that the normal directed E2 route makes those observations locally
available. A separate project-owner architecture decision is required. The
draft ACP-0007 records this boundary; it is not accepted.

## Mutation, evidence, persistence, and pruning decisions

| Topic | Readiness finding |
|---|---|
| Mutation timing | **Recommended proposal selects:** after each fully completed E2 character is settled and runtime resources are destroyed, before the next `START_CHARACTER`; never during a character, full workload pass, or phase. This keeps the decision local to one bounded character's frozen evidence. Owner acceptance is still required. |
| Candidate generation | Historical example-index and fixed policy mappings are not local production evidence. Random endpoints may remain a control, not an evidence-directed learner. The E2-local candidate endpoint source is unresolved. |
| Candidate evidence source | Historical feature/loss scores are invalid as source-local evidence. TemporalAssociationPolicy is locally bounded in its experiment fixture but not approved as E2 production producer. |
| Score function | No accepted normal-E2 score rule. The Luna-13B crossover was a controlled mechanism experiment; Luna-13F association count did not predict useful growth. No task, reward, outer feature, or accuracy score is authorized. |
| Chronology | Must freeze only evidence whose source observations predate the quiescent decision; equal-time event ordering must be deterministic; post-decision/future-suffix and held-out observations must not alter the decision. Actual E2 evidence-to-decision chronology is unspecified. |
| Evidence freeze/consumption | Candidate decisions need immutable snapshots; future live evidence cannot rewrite prior selection. Whether to consume/reset candidates at a character decision or aggregate bounded per-source candidates across a full epoch is unspecified. |
| Topology persistence | **Accepted:** topology persists across character reset; new experiment/model reset creates a new topology namespace. The same topology must route subsequent E2 events. |
| Evidence persistence | Not defined for an integrated E2 path. Luna-12I resets temporal history between sequences; Luna-13F freezes at a fixture decision/reset. Recommended first step: no evidence/candidate carry-over beyond the declared decision and no hidden carry between experiments; exact E2 boundary needs owner decision. |
| Growth | Controller has bounded legal growth APIs, but evidence producer/score and runtime destination mapping are not contract-complete. Future causal gate must show a later real E2 routed event, not merely an edge in a graph. |
| Pruning | **Not ready.** Existing `prune_by_score` trusts caller-supplied scores. Luna-13D's endpoint-authored scores failed independent evidence scrutiny; Luna-13E addressed admission quality, not local edge retention. Recommend excluding pruning from the first re-entry. |
| In-flight events | Historical pruning semantics leave queued deliveries unchanged. At the recommended quiescent character boundary there should be no live queue/sidecar, so the in-flight case is not normally exercised; do not change the historical behavior. |
| Incomplete settling | Runtime can report pending work/incomplete settling then destroy character state. It is unresolved whether partial characters may contribute evidence. Recommended behavior: no mutation evidence from incomplete/budget-exhausted characters. |
| Labels and future data | Must not influence score, candidate identity/rank, mutation, or topology. External reward/readout remains at its accepted post-readout boundary only. |
| Boundedness and determinism | Preserve edge/fan-in/out/routing/candidate/history/mutation bounds, finite delay, atomic admission, deterministic ranking/replay; require capture-on/off mutation and route equality. |
| TPCV-2 | Downstream-only instantaneous observation. It may display later edge changes but cannot generate/rank/approve/commit mutations or become a learning dependency. |
| Energy | Report only the uncalibrated activity-cost proxy. It is not an admission objective absent a separately accepted utility rule. |
| TANH_LEGACY | Keep explicit network-wide compatibility selection available; do not require numeric E2/TANH equality. Fixed-topology E2 is the primary control. |
| N3 and neuron equations | N3 (`w`, `d`, `r`) remains unauthorized. No change to MultiExcursionNeuron state machine, thresholds, return dynamics, or emission semantics. |

## Readiness matrix

| Topic | Current accepted contract / implementation | Decision still needed? | Safe first behavior / tests | Likely files; downstream groups |
|---|---|---|---|---|
| Mutation boundary | ACP-0006 fixes the first integration; current `_execute()` adapts after all examples, when per-character runtimes have returned | Yes: per-character vs full-pass boundary and treatment of incomplete runs | Prefer post-character quiescence; assert no queue, sidecar, pending work, or unsettled errors before commit | `tpcn/experiments.py`, focused tests; downstream 12B, temporal analysis, viewer |
| Candidate-generation policy | Historical endpoints derive from example index, configured policy, or seeded random | Yes: lawful actual E2-local destination observation | Use only a declared local event surface; random is a control, not learned evidence | likely `experiments.py` and tests; 12L/spiral remain separate |
| Evidence source | `run.feature + run.loss` violates demonstrated source locality; `TemporalAssociationPolicy` is an experimental producer | Yes: explicit production promotion or another accepted producer | Feed bounded evidence only from actual local E2-observable events; label/future mutation controls | possibly existing `temporal_association.py` only if explicitly authorized; 12B |
| Score and delay | Controller validates finite values only; experimental policies use count/residual scores and configured delays | Yes: score, delay provenance, ranking/threshold semantics | No readout/accuracy/reward score; freeze raw local evidence; tests cover score provenance and deterministic ties | `experiments.py` and focused tests; 12L/spiral not automatically |
| Chronology | Luna-13F tested freeze and before/equal/after attacks in a fixture; E2 integration has no structural decision timestamp | Yes: E2 decision cutoff and equal-time rule | Decision after all admitted events through declared boundary; suffix/held-out mutation cannot alter prior record | `experiments.py`, tests; analysis downstream |
| Evidence lifecycle | Luna-12I history resets per sequence; no E2 integration policy | Yes: accept/reject explicit lifecycle | Proposal: bounded evidence created within one character, frozen after complete settling, consumed once at the quiescent decision, then discarded; incomplete characters contribute none; no carry across characters/epochs/experiments | `experiments.py`, tests; all consumers |
| Topology persistence | ACP-0006 preserves topology across characters; experiment reset destroys model/topology; current runner retains a single graph | No for basic persistence; yes for structural checkpoint formats | Persist accepted mutations only within one experiment; IR-2 remains unchanged | `experiments.py`; TPCV consumers later |
| Growth | Controller legal bounded growth exists; _adapt's E2 score/endpoint producer is not legal | Yes: E2 evidence integration | Growth-only first; actual future E2 route must change after legal growth | `experiments.py`, focused integration tests; 12B |
| Pruning | Controller supports prune with queued events untouched; Luna-13D score evidence invalid; 13E is admission-only | Yes: local edge-use/retention evidence | Exclude pruning initially; later causal test of route removal after pruning | no pruning ownership now; 12B/analysis/viewer later |
| Labels/future | A07/ACP-0006 prohibit hidden label/future inputs; Luna-13F controls passed in fixture | No principle; yes for E2 integration proof | Identical event stream + relabel and suffix mutation leave frozen candidates/ranks/topology identical | tests; 12B, 12L/spiral remain separate |
| Boundedness/atomicity | Public controller/topology APIs already enforce bounds and deterministic growth | No controller redesign shown necessary | Test each limit and all-or-none admission through shared graph | focused tests; 12B |
| In-flight routing | Prune preserves already queued events; E2 runtime queue/sidecar is per-character | Yes only if mutations occur mid-character | Disallow mid-character mutation; assert quiescence; retain historical queued-event semantics | no runtime change authorized; 12B |
| TPCV-2 | Luna-27 accepted downstream-only instantaneous EXCURSION observation | No semantic change; downstream schema coverage still needed | Capture-on/off exact equality; TPCV does not feed mutation | later CPU visualization consumer; temporal analysis/viewer |
| Energy/readout | ACP-0006 uses activity-cost proxy and outer readout boundary; E2 feature is outer aggregate | Yes if proposed as score | Diagnostics only; no physical joule or score claim | report/metrics only; Luna-12L separate |
| Controls/N3/hardware | Fixed E2 control required; TANH explicit compatibility; N3 and hardware equivalence unauthorized | No change to these gates | Keep fixed E2 control; compatibility semantics tagged; no N3/hardware work | tests only; no GPU/FPGA downstream ownership |

## Architecture audit (A01-A15)

This is a readiness audit, not a claim that structural E2 adaptation passed:

- **A01 / A03 — preserved by proposed boundary:** decisions occur between
  event-driven character runtimes; finite positive propagation remains
  explicit. No global neural timestep is proposed. No mutation is authorized.
- **A04 / A08 — existing controller supports bounded mutation:** edge,
  fan-in/out, routing, candidate/growth and execution bounds are present.
  Integrated E2 evidence history and partial-run behavior still need a
  contract and tests.
- **A06 / A11 — preserve:** no prediction/error, eligibility, reward or credit
  semantics change. Prediction-loss aggregate is not used as structural
  score.
- **A07 — blocker:** historical ExperimentRunner score is not shown local to
  candidate source; the E2 observation-to-candidate map is unspecified.
- **A10 — preserve:** activity-cost proxy is diagnostic, not an energy-only
  topology objective. Useful computation may not be suppressed by default.
- **A14 — supported direction, not an integration authorization:** local
  bounded changes are permitted, but the evidence producer and mutation
  lifecycle are not accepted for EXCURSION_V1 production training.
- **A15 — not established:** no hardware mapping or equivalence was run.
- **A02 / A05 / A09 / A12 / A13:** no neuron temporal-state, reservoir,
  energy-model, pathway-count, or gating changes proposed.

## Exact terminal disposition

**ACP required? YES.** The current score/evidence producer, source-local E2
observation feed, candidate mapping, evidence lifecycle, and (if included)
pruning rule require a real architecture decision. Draft ACP-0007 is provided
for project-owner review. It is not accepted.

**Luna-13F promotion decision:** Use in normal EXCURSION_V1 training would
promote an experimental fixture mechanism; not authorized. Its tested
evidence mechanism remains supported in the fixture, while useful-growth
prediction remains **NOT SUPPORTED** and resource benefit **NOT ESTABLISHED**.

**Growth authorized? NO. Pruning authorized? NO. Luna-28 authorized? NO.**
The current guard remains. Do not create or execute Luna-28 until an owner
decision closes the identified semantics and Luna-0 issues a separate
bounded dispatch.

## Validation record

| Command or procedure | Result |
|---|---|
| Baseline status, branch, HEAD and origin/main | passed: clean `main`, both at `d9abe5e3a5b9b3c6d6049ac4c64647463c33ba2d` |
| Five downstream groups | `19 failed, 12 passed`; all 19 stop at the intentional config guard |
| Structural controller/evidence regression slice | `69 passed` |
| Full repository test suite | not rerun |
| Guard-bypassed post-guard downstream tests | not run; bypass prohibited |
| `git diff --check` | run after governance edits; see final publication state |
| GPU/FPGA/FPAA/hardware equivalence | not run; not applicable to this governance review |

## Next bounded assignment

Project owner / delegated architecture decision-maker: review Draft ACP-0007
and decide whether to promote a specific source-local E2 observation/evidence
contract, retain the fixed-topology-only boundary, or reject the proposed
re-entry. If accepted, return to Luna-0 to publish exact mutation/evidence
semantics and issue a separate implementation dispatch. No implementation
agent is authorized yet.
