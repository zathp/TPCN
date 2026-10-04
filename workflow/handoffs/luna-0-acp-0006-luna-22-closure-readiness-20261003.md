# Luna-0 ACP-0006 / Luna-22 Closure-Readiness Review

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Fresh Luna-22 remaining-gate classification"
  task_id: "luna-0-acp-0006-luna-22-closure-readiness-20261003"
  component: "ACP-0006 first CPU software-reference integration"
  status: "blocked by one verified core integration defect; bounded correction authorized"
  contract_version: "1.1"
  branch: "main"
  base_revision: "42026a9fc3ccc1b1fdc83e0344c79312f2d76b14"
  result_revision: "42026a9fc3ccc1b1fdc83e0344c79312f2d76b14 (reviewed implementation baseline)"
  dependencies:
    - "Accepted ACP-0006"
    - "Luna-23 independent closure"
    - "Luna-24 independent closure"
    - "Luna-25 independent closure for luna25-v1"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["INDEPENDENT REVIEW", "INTEGRATION DECISION", "VERIFICATION"]
  hypothesis: "The accepted Luna-22 CPU integration satisfies all owned ACP-0006 correctness gates after Luna-23, Luna-24 and Luna-25 closure."
  counter_hypothesis: "A valid workload exposes an owned integration defect even though the focused suite and dataset reproducibility gate pass."
  interfaces_relied_on:
    - "ExcursionCharacterRuntime and its single bounded per-character queue"
    - "MultiExcursionNeuron E2 and BoundedTopology"
    - "LocalPredictor, PredictionError, EligibilityLedger and StreamingCharacterClassifier"
    - "Accepted ACP-0006 rules 1-17"
  label_information_boundary:
    - "The input stream is incrementally admitted; predictions target the next actual scalar contribution at the configured port."
    - "Labels are used only by post-readout outer reward/prototype orchestration; they are not neural inputs or prediction targets."
  timing_assumptions:
    - "No global neural timestep; positive finite edge delays; shared queue with causal external-input watermark."
    - "Prediction errors traverse directed edges at each edge's declared finite delay."
  reset_boundaries:
    - "Character-local queue, eligibility, predictor, error-delivery guard and classifier reset after settling/readout/reward."
    - "Luna-24 integrated IR-2 quiescent startup correction remains closed."
  resource_bounds:
    - "Queue, events, topology, route contexts, prediction capacity/expiry, eligibility traces, provenance and error-delivery guard are finite."
  authorized_scope:
    - "Read-only review of published implementation, test outcomes and exact failure causes."
    - "Governance-only Luna-22 readiness handoff and status updates."
    - "Authorize one bounded Luna-26 correction for ACP-0006 rule 6."
  unauthorized_scope:
    - "No production/runtime/test changes in this review."
    - "No downstream consumer migration or efficacy redesign."
    - "No ACP/A01-A15 changes, hardware work or Luna-22 closure."
  controls:
    - "Real causal prediction/error fixture with a later admitted scalar."
    - "Positive-delay delayed-credit fixture with duplicate replay."
    - "Valid three-node multi-hop error path counterexample."
    - "Current full CPU suite and exact test failure identities."
  measurements:
    - "Focused integration, prescribed regression and full-suite outcomes."
    - "Prediction/error identity, target, timestamps, payload, route source/destination and delivery count."
    - "Credit trace ownership, decay, reward timestamp, credit mutation and duplicate idempotency."
  information_boundary_check:
    - "Existing no-label-leakage and incremental-input tests pass; the real causal probes use only admitted input values."
  hardware_mapping:
    - "Software-reference CPU review only; no hardware equivalence or physical-energy claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10", "A11", "A12", "A13", "A14", "A15"]
  preserves:
    - "Luna-23, Luna-24 and Luna-25 remain closed within their exact scopes."
    - "No architecture contract or ACP-0006 rule is changed."
    - "The 24 downstream failures are not silently repaired or conflated with core integration."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-acp-0006-luna-22-closure-readiness-20261003.md"
    - "workflow/handoffs/luna-0-authorization-luna-26-prediction-error-multihop-routing-20261003.md"
    - ".github/agents/luna-26.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Focused Luna-22 integration file: 43 passed."
    - "Prescribed ACP-0006 regression set: 334 passed."
    - "Prediction/error local matching and delayed-credit mechanics verified by focused tests and independent runtime probes."
    - "Luna-25 dataset gate: CLOSED / reproducible for luna25-v1."
    - "Luna-23 E2 correction and Luna-24 IR-2 startup correction remain independently closed."
  tests_failed:
    - "Three-node multi-hop prediction-error probe: matched error reached n0/n1 but failed to reach reachable n2, contrary to ACP-0006 rule 6."
    - "Full CPU suite: 24 known downstream compatibility failures, 796 passed, 1 CUDA-unavailable skip."
  tests_not_run:
    - "Post-correction multi-hop tests; Luna-26 is authorized but not executed."
    - "Hardware equivalence, full-dataset efficacy and physical-energy calibration."
  assumptions:
    - "The exact `F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` token in the request is not a valid/resolvable Git object; actual lineage below is verified from Git's commit graph."
  unresolved:
    - "Luna-22 is blocked only by the identified ACP-0006 multi-hop prediction-error forwarding defect among reviewed core integration items."
    - "Prediction/error task efficacy and useful delayed-credit learning are not established by luna25-v1; they are not correctness blockers under ACP-0006."
    - "The historical Luna-22 sample membership/loader is unreconstructable."
    - "The 24 downstream consumer failures remain separately governed compatibility work and are not Luna-22 closure blockers."
  recommended_next_agent:
    - "Luna-26 for the narrowly scoped multi-hop prediction-error forwarding correction."
```

## Outcome and owned scope

This is a read-only integration/governance review. No runtime or test code was
changed. The governance outcome is one bounded authorized follow-up (Luna-26);
this review itself neither executes Luna-26 nor closes Luna-22.

**HYPOTHESIZED (review starting point):** After Luna-23/24/25, Luna-22 may
meet its remaining correctness gates. **OBSERVED:** The real three-node
prediction-error probe fails to deliver to a reachable second hop.
**INFERRED:** The failed route is an adapter-level violation of already
accepted ACP-0006 rule 6; it warrants one bounded corrective assignment, not
an architecture change.

Governance files created/updated by this publication:

- `.github/agents/luna-26.agent.md`
- `workflow/handoffs/luna-0-authorization-luna-26-prediction-error-multihop-routing-20261003.md`
- `workflow/handoffs/luna-0-acp-0006-luna-22-closure-readiness-20261003.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`

## Verdict and starting state

**SCENARIO C — BLOCKED FOR ONE CORE ACP-0006 PREDICTION-ERROR
FORWARDING DEFECT.** Luna-22 is **IMPLEMENTED / BLOCKED / NOT CLOSED**.
**OBSERVED:** The starting checkout was clean `main`, with `HEAD == origin/main ==
42026a9fc3ccc1b1fdc83e0344c79312f2d76b14`, subject
`docs: independently review Luna-25 dataset evidence`.

The commit graph verifies the Luna-22 implementation
`a206f2e8fec8f0c72d9196b2bcca9d2e734c7974`, published second-review commit
`baec12ad368239d959ca747d5a4e28c96746dd6e`, review metadata commits
`188e00bbfdb9edd9acf3c8529c630dac3eff5ba9` and
`3ec3c4a7991c28f59e1419c9f3656267efed2875`, Luna-23 correction
`4c1efd6c31aed86748dcacf596401579c2b94bc8`, Luna-23 closure
`c0e3e6905e329e5c268d6c63cbb3bd8d89345136`, Luna-24 correction
`8e184e1bdceeb2873b2ea7479da953760b58ffbf`, Luna-24 closure
`1642b991f82403140d0f29b5a2ff10b3d2628cda`, Luna-25 evidence
`5cb17d9bb79c848c27805cb79484d9ab3cd0f5b8`, Luna-25 completion handoff
`425180bfb2b02691cf64f392f071795cc812cd72`, and Luna-25 independent closure
at the starting revision. The literal token
`F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` supplied as two intermediate
lineage entries did not resolve with `git cat-file`; the real published Git
commits and their ancestry are recorded above, without treating that token as
a verified object.

Luna-23, Luna-24 and Luna-25 remain **CLOSED / INDEPENDENTLY VERIFIED** in
their exact scopes. Luna-25 closes only `luna25-v1` dataset/split/result
reproducibility and does not reconstruct the historical Luna-22 membership.

## Remaining-gate classification

| Open observation | Category | Closure effect and contractual basis |
|---|---|---|
| Multi-hop opaque `PredictionError` forwarding repeats the original source hop and fails to reach later reachable nodes. | **A. LUNA-22 CONTRACT CORRECTNESS BLOCKER** | ACP-0006 rule 6 expressly requires each destination to forward the error over that node's outgoing edges, with finite delay and one credit application per destination. Independent three-node probe failed this exact requirement. |
| `luna25-v1` observed zero matches/errors, low classification accuracy, and zero matched delayed credit. | **C. TASK-EFFICACY FOLLOW-UP** | ACP-0006 distinguishes integration correctness from task-efficacy proof and sets no accuracy threshold. The data/configuration did not exercise predictive/credit efficacy; it does not negate a working mechanism. |
| Original Luna-22 160-record membership, loader and preprocessing were not retained. | **D. HISTORICAL-EVIDENCE LIMITATION** | Not recoverable from aggregate accuracy/seed alone. Luna-25 satisfies the replacement dataset gate under the distinctly versioned `luna25-v1`; exact historical reconstruction is not an accepted literal requirement. |
| 24 downstream failures across visualization, structural experiments, legacy observables, temporal-scale/spiral, analysis and viewer. | **B. DOWNSTREAM COMPATIBILITY / MIGRATION BLOCKER** for those consumers; **not a Luna-22 closure blocker** | The tests assume scalar/TANH behavior or structural mutation explicitly forbidden in the first EXCURSION_V1 integration. ACP-0006 requires running/reporting the suite and applicable regressions, not making every historical/downstream consumer green under the new default. Luna-22's agent contract asks to run the full suite and return results; it does not state that unrelated consumer failures must be repaired. Luna-0 workflow policy says failed applicable invariants block readiness, not unrelated work. Every current failure was inspected and classified below. |
| Structural plasticity experiments, improved predictive efficacy, useful delayed-credit learning, writer-disjoint or full-dataset efficacy, and hardware/backend equivalence. | **E. OPTIONAL FUTURE RESEARCH** (or not applicable to this CPU gate) | These are not established by this evidence; fixed topology is required for the first integration. No accuracy/effectiveness or hardware threshold may be retroactively imposed. |

## Prediction, error and expiry mechanics

**LOCAL PREDICTION/ERROR MECHANICS VERIFIED; MULTI-HOP ROUTING FAILED.**
The focused `test_integrated_delayed_prediction_error` is non-vacuous:
external `1.2` at `t=0` causes a real E2 excursion/prediction; later admitted
`0.4` at `t=1` resolves the configured `"external-input:scalar"` prediction.
An independent probe observed prediction value `0.3`, target `0.4`, signed
error `0.10000000000000003`, prediction timestamp `0.5`, observation/error
timestamp `1.0`, and the same prediction ID on the local error event. The
error event entered the shared bounded character queue, was delivered to the
local ledger, and in a one-edge probe arrived at the first neighbor at
`1.25` with unchanged `PredictionError` metadata. Instrumented calls confirmed
that `PredictionError` was never passed to `MultiExcursionNeuron.receive_event()`.

The focused test by itself does not test a topology edge or identity/timing
fields beyond observation time. The independent probe extended it to a valid
`n0 -> n1 -> n2` directed path. The first event was locally delivered at
`n0 @ 1.0`, then arrived at `n1 @ 1.25`; the next recorded error was again
`n0 -> n1 @ 1.5` with the same event ID, deeper duplicate path metadata, and
no event at reachable `n2`. `_deliver_prediction_error()` passes the original
source into `BoundedTopology.route()` at every destination, so it repeats
`n0`'s outgoing edge rather than forwarding from `n1`. The finite dedupe
guard prevents an unbounded loop but does not satisfy the accepted multi-hop
route. This is an integration defect in the Luna-22-owned runtime adapter,
not a change request to the closed topology component.

**PREDICTION EXPIRY IS NOT A MATCHING IMPOSSIBILITY.** Luna-25's
`created predictions == emissions`, all expired, zero matches is a
configuration/workload efficacy observation. `test_integrated_delayed_prediction_error`
and the independent probe causally matched a real emission-generated
prediction with a later admitted target inside its 4-second expiry. Thus an
accepted valid workload can match with the production implementation. The
dataset's short per-character stream and emission/settling timing did not
produce a later in-window target for its generated predictions. Do not change
expiry or prediction ownership in Luna-26.

## Delayed-credit mechanics

**DELAYED-CREDIT MECHANICS VERIFIED.** The focused test creates an actual
emission and eligibility trace, then applies the authorized outer reward at
positive logical delay `0.25` after settling. Independent instrumentation
observed the matched reward at logical time `5.25`; it targeted the exact
emission trace `test:char:n0:excursion:1`. The trace's eligibility decayed
from `0.2647490707753786` at time `1.0` to `0.09149483061331778` at `5.25`,
and its credit changed to `0.10064431367464957`. Replaying the same reward
message ID returned `duplicate`, zero credit and no trace mutation. Existing
`tests/test_eligibility.py` additionally exercises duplicate idempotency and
the finite FIFO identity window. This is a real causal emitted-activity
sequence, not credit assigned to silent hidden state.

Luna-25's zero matched delayed-credit count therefore means **useful
delayed-credit learning was not demonstrated on that dataset/configuration**,
not that the integration API cannot match or deliver credit.

## Dataset, focused tests, and suite results

- Dataset gate: **CLOSED / REPRODUCIBLE for `luna25-v1`**; independent review
  verified 2,858 records, 20 classes, 80/40/40 selected examples, 4/2/2 per
  class, source SHA-256
  `00ab9af03f74167b5ddee9d5f3e7ed3da8df0bc49d2e9c4078c51857fdc13ebe`,
  split membership, metrics and two-run output reproduction.
- The published run's verified accuracy was train/validation/test
  `0.150/0.125/0.175` (12/80, 5/40, 7/40 correct); macro-F1 was
  `0.0727/0.0428/0.0989`. Each split had zero matched predictions/errors and
  zero matched delayed credit. These results show weak classification and no
  predictive/credit efficacy on this configuration, not a failure of local
  matching/credit correctness or an unauthorized accuracy-threshold failure.
- The run used the retained `luna25-v1` 160-record 20-class split. The
  declared runtime bounds included prediction capacity 8/character,
  4-second prediction expiry and provenance capacity 16. Queue peaks were
  189/512, 188/512 and 187/512; active connections were 1/8 and fan-in/out
  utilization 0.00625/0.00625. Reported activity-cost proxy totals were
  25,450.3444, 12,718.3620 and 12,445.2308 units for train, validation and
  test, respectively; they are not joules or calibrated physical energy.
  Detailed component arithmetic is in the published Luna-25 review.
- Historical dataset: **not reconstructable**. No retained old membership or
  loader/preprocessing record identifies the former subset. This is not a
  blocker because Luna-25 explicitly replaces it with `luna25-v1`.
- Focused Luna-22 suite: `python -m pytest -q tests/test_excursion_integration.py`
  — **43 passed**. All required named tests and additional bound/reset cases
  pass; the non-vacuity qualifications and discovered multi-hop gap are
  recorded above.
- Prescribed ACP-0006 regression command — **334 passed**.
- Current full suite — **24 failed, 796 passed, 1 skipped, 821 collected**.
  The skip is CUDA unavailable. Exact failures and stack causes are in the
  matrix below. No Luna-22-owned test failed in that suite.
- The 24 failures are not converted into an integration acceptance criterion
  of “entire historical CPU suite green under EXCURSION_V1.” They are
  separately classified consumer compatibility failures; no downstream fix
  is authorized here.

## Consumer-by-consumer compatibility matrix

| Consumer group | Failing tests | Direct failure cause | Current model assumption | Accepted ACP-0006 behavior | Classification | Production change required? | Test/fixture migration required? | Legacy-control path sufficient? | New architecture decision required? | Blocks Luna-22 closure? | Recommended next bounded action |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CPU visualization / TPCV capture | `test_capture_modes_do_not_change_training_result`; `test_snapshot_sequence_is_deterministic_and_replays_offline`; `test_replay_rejects_missing_malformed_and_over_limit_data` | `NeuronRecord.from_neuron()` reads scalar `.activation`; `MultiExcursionNeuron` has no such attribute. | Capture consumes `TPCNNeuron` scalar activation/state by default. | EXCURSION_V1 routes only actual excursions; silence is not a fabricated scalar. TPCV remains downstream and non-backpressuring. | **B** | Not for Luna-22. A separate observer adaptation may be needed for E2 capture; never synthesize `.activation`. | Yes: explicitly choose legacy snapshot fixtures or add E2-observable fields under the existing TPCV-1 limits. | Yes for historical scalar capture; not for E2 capture. | Not for preserving legacy capture. If extending TPCV-1 fields/semantics, obtain the applicable visualization-format decision first. | **No** | Keep as separately scoped read-only Luna-12A/TPCV compatibility work; preserve non-interference. |
| Luna-12B structural experiment | `test_structural_run_is_deterministic_and_has_real_bounded_mutations`; `test_capture_is_downstream_only_for_structural_decisions`; `test_controls_report_behavior_and_topology_without_assuming_benefit`; `test_structural_evidence_is_label_isolated` | `ExperimentConfig` rejects `structural_plasticity=True` under default EXCURSION_V1. | Structural experiment assumes implicit legacy/default model with enabled mutations. | First ACP-0006 integration must be fixed topology with structural plasticity off; TANH_LEGACY is explicit control. | **B** | No core change. Consumer may explicitly select TANH_LEGACY for legacy structural comparison. | Yes, select explicit legacy model or separately authorize a later E2 structural integration. | Yes for legacy structural results; no for enabling E2 growth. | No for explicit legacy control; yes only for a future E2 structural-learning contract. | **No** | Migrate the structural experiment fixture/control path separately; do not enable plasticity in Luna-22. |
| Luna-12E routed activity / reset observables | `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`; `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` | Edge changes event/energy/route metrics but not root-input prediction loss (`1.1725` both); second assertion expects final scalar clock `0/1` but E2's declared settling/reset timestamp is `5.0`. | Any topology change alters predictor loss; neuron clock exposes legacy point/reset scalar values. | Predictions are made only from configured predictor-source emissions; E2 clock/reset follows the accepted local-time settling boundary. | **B** | No Luna-22 fix indicated. | Yes, assert an E2-owned observable or explicitly run the legacy comparison. | Yes for the old scalar observables; E2 assertions should reflect ACP ownership/reset semantics. | No; ACP-0006 already determines these observables. | **No** | Update Luna-12E tests to distinguish routed activity/energy from root prediction loss and to assert the declared E2 reset boundary. |
| Luna-12L temporal-scale suite | `test_scale_runner_retains_all_policies_and_causal_evidence`; `test_requested_policy_is_executed_by_classifier[baseline]`, `[random]`, `[temporal]`, `[reversed]`; `test_policy_changes_classifier_execution_state`; `test_policy_scale_cross_product_preserves_provenance_and_serialization`; `test_condition_fails_on_classifier_provenance_mismatch` | All eight fail during config construction because non-fixed policies request `structural_plasticity=True` with default EXCURSION_V1; the provenance test never reaches its intended assertion. | Temporal-policy classifier expects enabled structural plasticity and implicit default selection. | ACP-0006 fixes EXCURSION_V1 topology; structural plasticity is off. | **B** | No core change. | Yes: explicit legacy model for legacy policy comparisons, and repair tests to reach their intended provenance assertions. | Likely for the existing TANH structural experiment; this review makes no post-migration pass claim. | No for legacy experiments; yes only for a future EXCURSION_V1 structural contract. | **No** | Separate temporal experiment/model-selection migration; rerun after fixture correction because current failures stop at construction. |
| Spiral benchmark structural control | `test_control_results_are_deterministic_and_include_required_order_controls` | The structural-plasticity control constructs EXCURSION_V1 with `structural_plasticity=True` and is rejected before the remaining controls run. | Benchmark assumes structural run can use default model. | First integration stays fixed topology; structural adaptation is separately authorized. | **B** | No core change. | Yes: make the benchmark control explicitly select legacy where semantically intended, or separately govern E2 structural work. | Yes for the historical structural control only. | No for legacy control; yes for later E2 structure. | **No** | Scope a spiral-control migration separately; rerun the whole control suite after model selection is explicit. |
| Temporal analysis | `test_flat_metrics_and_changing_topology_are_reported`; `test_rejection_reason_aggregation_preserves_observed_reasons`; `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` | Structural fixtures are rejected by EXCURSION_V1 in two tests; capture in the remaining test fails on missing scalar `.activation`. | Analysis fixtures expect legacy structural training and scalar TPCV snapshots. | Analysis remains downstream/read-only; fixed topology is first integration; E2 has no fabricated scalar activation. | **B** | No Luna-22 core change. | Yes: provide explicit compatible legacy replay or a TPCV-supported E2 diagnostic fixture. | Yes for historical structural/scalar analyses; not E2 topology growth. | Only if analysis requires new TPCV fields or E2 structural semantics. | **No** | Separate replay-fixture migration; preserve raw measurements and non-causal analysis. |
| 3D viewer | `test_layout_and_scene_generation_are_deterministic_and_diagnostic`; `test_topology_deltas_and_bounded_prune_highlights`; `test_playback_filters_selection_neighborhood_and_metrics` | Shared scene fixture requests structural CPU training under EXCURSION_V1; config rejects before viewer code executes. | Viewer fixture assumes a structural-plasticity training source is available by default. | Viewer is downstream-only; no mutation or feedback; first EXCURSION_V1 path is fixed topology. | **B** | No Luna-22 change. | Yes: use a declared structural legacy replay or a separately authorized E2 structural artifact. | Yes for legacy replay; no for producing E2 mutations. | Only if proposing E2 structure or changing the viewer data contract. | **No** | Separate replay-source decision and viewer fixture task after compatible source is selected. |

All 24 current failures are classified as downstream compatibility or
consumer-test migration (B), not Luna-22 contract correctness failures. Their
groups have distinct owners/semantics and are not combined into a generic
“make the suite green” assignment. No downstream implementation is assigned
by this review.

## Regression-policy interpretation

The Luna-22 agent contract requires running the full CPU suite and returning
all results; it does not say that every historical/downstream test must pass
under the new model. ACP-0006 acceptance is the focused required tests,
independent causal review and **applicable** existing regressions. It states
that integration correctness is not task-efficacy proof, fixes topology and
structural plasticity off, maintains explicit TANH_LEGACY compatibility, and
preserves downstream-only TPCV semantics. Luna-0's review policy blocks
failed applicable invariants, not unrelated useful work. The exact 24 stack
traces show legacy scalar assumptions or structural plasticity requests
outside the fixed-topology first integration. The full suite is run and
reported, and failures are classified; repository-wide suite green is not a
literal Luna-22 correctness gate.

The exception is not “an unrelated test failed”: the independent three-node
probe violates the accepted multi-hop error-routing rule in Luna-22's owned
runtime. That contract failure is the sole current Luna-22 blocker.

## Validation record

| Command or procedure | Revision / environment | Observed result |
|---|---|---|
| `python -m pytest -q tests/test_excursion_integration.py` | Reviewed baseline `42026a9`; Python 3.11.5 | **PASS: 43 passed.** |
| Prescribed ACP-0006 regression modules: `tests/test_experiments.py`, `tests/test_excursion_neuron.py`, `tests/test_e2_multi_excursion.py`, `tests/test_event_runtime.py`, `tests/test_topology.py`, `tests/test_predictive_coding.py`, `tests/test_eligibility.py`, `tests/test_streaming_classifier.py`, `tests/test_energy_utility.py`, `tests/test_ir2.py`, `tests/test_e2_ir2.py`, `tests/test_stroke_dataset.py` | Reviewed baseline `42026a9`; Python 3.11.5 | **PASS: 334 passed.** |
| `python -m pytest -q -rs` | Reviewed baseline `42026a9`; Python 3.11.5 | **FAIL: 24 known downstream failures, 796 passed, 1 CUDA-unavailable skip.** |
| `python -m pytest --collect-only -q` | Reviewed baseline `42026a9`; Python 3.11.5 | **PASS: 821 collected.** |
| Causal prediction/error probe: admit external `1.2` at `t=0`, allow real E2 emission/prediction (`0.3 @ t=0.5`), then admit target `0.4 @ t=1` and instrument routing/delivery | Reviewed baseline `42026a9`; CPU runtime; ephemeral review probe, no script retained | **PASS locally:** real nonzero error `+0.1` matches prediction ID and enters local consumer; **FAIL multi-hop:** n0→n1 @ 1.25 then repeated n0→n1 @ 1.5; n2 not delivered. |
| Delayed-credit probe: actual emitted-excursion eligibility, positive-delay authorized reward at logical time `5.25`, then replay same reward ID | Reviewed baseline `42026a9`; CPU runtime; ephemeral review probe, no script retained | **PASS:** trace credit `0.10064431367464957`; replay reported `duplicate` and made no credit mutation. |
| Full dataset reconstruction, two-run reproduction, metric/resource arithmetic, label/future probes | Luna-25 `luna25-v1`; details in prior Luna-25 independent review | **PASS for dataset reproducibility only;** does not establish efficacy or close multi-hop routing. |
| `git diff --check` | Governance-only review publication | **PASS** after edits; no production code/test edits. |

The two small runtime probes were not retained as scripts; Luna-26's required
tests must make the route counterexample persistent and reproducible. No
post-correction check is claimed.

## Architecture clause audit

| Clause | Readiness finding |
|---|---|
| A01 | Shared queue, causal admission ordering and no-global-timestep focused tests pass. |
| A02 | E2 persistent local state, timing and reset tests pass; no global timestep is introduced. |
| A03 | Ordinary finite-delay routed event tests pass. **Prediction-error forwarding over a reachable multi-hop path fails**; Luna-26 owns this correction. |
| A04 | Finite topology, queue, event budgets and bounds pass focused/regression tests. The failed error route is not unbounded, but is semantically incomplete. |
| A05 | Integrated runner does not require a spatial reservoir. |
| A06 | Local real emission→prediction→later admitted target→nonzero error works. Multi-hop error propagation is a correctness blocker. Luna-25's zero real-data matches are efficacy/configuration, not proof of API failure. |
| A07 | Focused relabeling and future-input tests pass; Luna-25 independent pre-readout trace and shared-prefix suffix probes pass. Reward is label-dependent only after readout under the accepted outer boundary. |
| A08 | Queue, budgets, topology and error dedupe are finite; stress/incomplete-settling cases report bounded failure explicitly. |
| A09 | Energy proxy accounting and component regression tests pass; no calibrated joule claim. |
| A10 | Reward/utility accounting is exercised. Luna-25 does not establish high-utility efficacy; no energy-only or inactivity inference is made. |
| A11 | Real positive-delay reward modifies the matching actual excursion trace; delayed decay and duplicate idempotency are observed. Luna-25's zero matched credit is task-efficacy only. |
| A12-A13 | Optional operator/gating choices remain experiments, not mandatory invariants. |
| A14 | Fixed topology and disabled structural plasticity are enforced for EXCURSION_V1; the rejected structural consumer tests do not authorize growth. |
| A15 | CPU software-reference only; no backend/hardware equivalence or calibration claim. |

## Closure scenario, dependency order, and successor

Scenario C is selected because a valid three-node error-routing counterexample
shows an integration defect. The minimal dependency order is:

1. **Luna-26:** fix and test hop-local forwarding in the integration adapter,
   preserving queue bounds, route delays, error identity/payload, and
   per-destination dedupe. This requires no architecture decision: ACP-0006
   rule 6 already specifies the behavior.
2. **Luna-0:** independently review the exact Luna-26 revision and rerun
   focused, prescribed and full regressions. Only if this route defect is
   closed and no new applicable failures appear may Luna-22 closure be
   reconsidered.
3. Downstream visualization, structural experiments, legacy observables,
   temporal/spiral analysis and viewer compatibility remain separate tracks.
   They are not prerequisites for Luna-22 under current ACP/workflow policy.
4. Any future task-efficacy experiment for prediction matching, predictive
   loss or useful delayed credit is separate and is not a retroactive
   correctness condition.

**Luna-26 authorized: YES, not executed.** Its exact scope, baseline and
acceptance criteria are in `.github/agents/luna-26.agent.md` and
`workflow/handoffs/luna-0-authorization-luna-26-prediction-error-multihop-routing-20261003.md`.
No consumer migration is assigned. No owner decision is needed to implement
the already accepted hop-forwarding rule. Project-owner choice is only needed
before separately authorizing any future E2 structural-plasticity or expanded
visualization/data-format contract.

## Governance disposition

- Luna-22: **IMPLEMENTED / BLOCKED / NOT CLOSED**, solely on the verified
  multi-hop prediction-error forwarding defect among reviewed core items.
- Luna-23: **CLOSED / INDEPENDENTLY VERIFIED**.
- Luna-24: **CLOSED / INDEPENDENTLY VERIFIED**.
- Luna-25: **CLOSED / INDEPENDENTLY VERIFIED** for `luna25-v1` reproducibility.
- Luna-26: **AUTHORIZED / NOT EXECUTED** for the bounded correction only.
- ACP-0006 and A01-A15: unchanged; no architecture proposal required.

## Reproduction, rollback and next assignment

Re-run the focused and prescribed test commands above from the published
baseline. The multi-hop counterexample can be reproduced using the
non-vacuous E2 emission/matching sequence recorded in the prediction/error
section, connected through the bounded directed path `n0 -> n1 -> n2`, while
instrumenting route source, destination, time and `PredictionError` identity.
Luna-26 must retain that case and add convergent-path and unreachable-node
controls; see its agent contract for complete acceptance.

No production files or test fixtures changed in this review. There is no
runtime rollback. If a governance correction is needed, publish a narrowly
scoped follow-up rather than reverting unrelated history. **Next assignment:**
Luna-26 implements and verifies only adapter-level hop-local prediction-error
forwarding; Luna-0 independently reviews its handoff and revision before
reconsidering Luna-22 closure.
