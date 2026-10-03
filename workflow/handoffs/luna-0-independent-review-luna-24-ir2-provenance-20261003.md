# Luna-0 Independent Review — Luna-24 IR-2 Provenance Boundary

```yaml
tpcn_handoff:
  agent: "Luna-0"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent verification of Luna-24 ACP-0006 startup boundary"
  task_id: "luna-0-independent-review-luna-24-ir2-provenance-20261003"
  component: "Integrated TPCN-IR-2 quiescent startup"
  status: "PASS; Luna-24 closed; Luna-22 remains blocked"
  contract_version: "1.1"
  branch: "main"
  base_revision: "e59e8933bfa98cd607ca424250a051499b519b5a"
  implementation_revision: "8e184e1bdceeb2873b2ea7479da953760b58ffbf"
  result_revision: "Review publication commit adding this handoff; exact hash is reported in the completion summary."
  dependencies:
    - "Accepted ACP-0006 clause 13"
    - "Luna-24 implementation and completion handoff"
    - "Luna-23 independently closed"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["INDEPENDENT CORRECTIVE REVIEW", "IR-2 STARTUP-BOUNDARY VERIFICATION", "ADVERSARIAL OVER-REJECTION REVIEW", "REGRESSION VERIFICATION"]
  hypothesis: "Luna-24 rejects all residual provenance only at integrated quiescent startup while preserving standalone E2/IR-2 state and allowed identity history."
  counter_hypothesis: "The integration guard either still accepts residual provenance, rejects valid transferable history, or changes standalone/schema semantics."
  interfaces_relied_on:
    - "ExcursionCharacterRuntime.from_quiescent_ir2"
    - "IR2Neuron / TPCNIR2 schema revision 1"
    - "neuron_from_ir2_e2 and neuron_to_ir2_e2"
    - "START_CHARACTER reset and character-scoped event runtime"
  label_information_boundary:
    - "Review probes used serialized neuron state, model tags, queue/topology data and declared runtime configuration only."
    - "No labels, future points, rewards, task metrics or dataset state entered validation."
  timing_assumptions:
    - "A quiescent local timestamp is finite logical-time history; the explicit START_CHARACTER timestamp resets local clocks before event execution."
  reset_boundaries:
    - "START_CHARACTER clears local activity counters, m_peak, generation and provenance while preserving output/episode/lineage/input identity high-water counters."
  resource_bounds:
    - "Existing bounded provenance, event counters, event budget, queue, topology and settling remain unchanged."
  authorized_scope:
    - "Read-only independent verification of exact Luna-24 commits, source, tests, accepted contracts and full CPU suite."
    - "Review handoff and workflow/changelog status publication."
    - "One bounded follow-on dataset-reproducibility authorization."
  unauthorized_scope:
    - "Luna-24 production changes."
    - "Luna-22 closure, dataset execution, downstream migration or broad test repair."
    - "ACP/A01-A15 changes, IR-2 schema changes, N3/H2, backends or hardware validation."
  controls:
    - "Exact parent implementation inspection and valid assigned-provenance fixtures."
    - "Clean startup, high-water continuity, signed zero, exact residual x, active/pending, shared queue, mixed model and standalone E2 controls."
    - "Focused, prescribed, full-suite and collection-count reruns."
  measurements:
    - "Startup exception type/message; IR-2 round-trip state; identity allocation; test counts, failure identities and collection count."
  information_boundary_check:
    - "No external task labels, future points, global clock or evaluation state was consulted by adapter validation."
  hardware_mapping:
    - "Hardware-neutral software-reference verification only; no equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A08", "A15"]
  preserves:
    - "A01-A15, ACP-0004/ACP-0005/ACP-0006 and TPCN-IR-2 schema revision 1."
    - "Standalone active/pending/provenance E2 round-trip behavior."
    - "Luna-23 closed representability correction."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna-24-ir2-provenance-20261003.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Focused integration: 43 passed."
    - "Standalone IR-2/E2 reference suite: 203 passed."
    - "Luna-22 focused controls: 55 passed."
    - "Prescribed integration regression set: 334 passed."
    - "Full CPU suite: 789 passed, 24 failed, 1 skipped; failure identities match the known downstream groups."
    - "Collection: 814 tests; compileall, Pylance diagnostics and diff checks passed."
  tests_failed:
    - "The same 24 downstream tests remain failing; none is attributable to Luna-24."
  tests_not_run:
    - "Dataset loader/split/per-class result reconstruction."
    - "Hardware/backend equivalence."
  assumptions:
    - "ACP-0006 clause 13's fresh integrated startup excludes assigned provenance and sticky truncation as residual causal provenance; this was explicitly authorized by Luna-0."
  unresolved:
    - "The UCI Character Trajectories loader/split/per-class evidence is not retained and remains a separate gate."
    - "Downstream compatibility and migration decisions remain unresolved and are not one homogeneous implementation task."
  recommended_next_agent:
    - "Luna-25 for bounded, repository-reproducible sequential-dataset evidence; no downstream migration is authorized."
```

## Outcome, revisions and exact delta

**OBSERVED:** Review started on clean `main` at
`e59e8933bfa98cd607ca424250a051499b519b5a`, equal to `origin/main`, with
subject `docs: record Luna-24 provenance boundary verification`. The commit
chain is:

```text
6c012f9feeff6481a44bd6d40414b4749b21db17
    authorized post-Luna-23 baseline
-> 8e184e1bdceeb2873b2ea7479da953760b58ffbf
    Luna-24 implementation
-> e59e8933bfa98cd607ca424250a051499b519b5a
    Luna-24 handoff publication / review start
```

`c0e3e6905e329e5c268d6c63cbb3bd8d89345136` (Luna-23 independent closure)
is an ancestor of the review tip. Luna-23 remains
**CLOSED / INDEPENDENTLY VERIFIED**.

The exact implementation delta from `6c012f9` through `8e184e1` contains
only:

- `tpcn/experiment_excursion_runtime.py`: two additional rejection terms
  inside `ExcursionCharacterRuntime.from_quiescent_ir2()`, before topology
  reconstruction and before `neuron_from_ir2_e2()`.
- `tests/test_excursion_integration.py`: focused integrated startup tests
  covering the new rejection terms and valid/invalid boundary controls.

No `IR2Neuron`, `TPCNIR2`, schema, E2 converter, `MultiExcursionNeuron`,
runtime scheduler or experiment behavior changed. The handoff publication
commit adds documentation only.

**OBSERVED parent behavior:** At `6c012f9`, the startup predicate checked
`x` and the two unassigned-provenance markers but omitted
`record.provenance` and `record.provenance_truncated`. It then passed the
record to `neuron_from_ir2_e2()`, whose reconstruction copies both assigned
provenance entries and their truncation flag. Thus both otherwise-quiescent
cases reached integrated reconstruction on the parent. This conclusion is
from direct inspection of the exact parent implementation and unchanged
converter, not solely Luna-24's handoff.

**OBSERVED corrected behavior:** Current valid revision-1 records with
assigned provenance, sticky assigned truncation, or combined assigned and
unassigned provenance markers raise
`IR2UnsupportedRuntimeError("integrated IR-2 startup rejects residual state or provenance")`
at the integrated startup boundary. No normalization or clearing occurs.

## Independent startup-boundary evidence

| Case | Independent evidence | Result |
|---|---|---|
| Assigned provenance only | Valid `IR2Provenance` record used in focused tests and standalone schema construction | Rejected by integrated adapter |
| Assigned provenance with sticky truncation | Focused parameterized case | Rejected |
| Sticky truncation with empty tuple | Focused parameterized case | Rejected |
| Assigned plus unassigned count | Focused test; independent runtime probe | Rejected |
| Assigned plus unassigned truncation | Independent runtime probe with schema-valid record | Rejected |
| Unassigned count only / unassigned truncation only | Focused parameterized tests | Rejected |
| `x=+0.25`, `x=-0.25` | Focused parameterized tests | Rejected |
| Smallest positive and negative finite subnormal `x` | Focused parameterized tests using `math.nextafter` | Rejected exactly; no epsilon normalization |
| `x=+0.0` and `x=-0.0` | Serialized/deserialized in focused tests | Both accepted; `copysign` confirms sign survives JSON round trip |
| Clean `N`, exact zero, no active/pending/provenance | Existing deterministic reconstruction test runs input and settling twice | Accepted; identical event traces |
| Nonzero permitted event/episode/lineage/input high-water marks | Focused test | Accepted; subsequent event ID and episode/lineage IDs exceed prior values |
| Generation, processed-event and input-contribution counters | Independent probe | Accepted while quiescent; `START_CHARACTER` resets local counters/generation before execution |
| `S_PENDING`, active `S_RETURN`, `M_ACTIVE` with valid pending E2 records | Focused parameterized tests and standalone E2 conversion | Rejected only by integrated startup as live-network resume |
| Mixed model tags | Existing focused integration test | Rejected |
| Non-empty shared queue | Focused test with schema-valid `IR2Event` | Rejected |
| Standalone E2 active/pending/provenance | Four-file reference suite, including existing provenance/truncation and continuation tests | Pass; transfer semantics unchanged |
| Schema revision | Runtime constant and serialized `TPCNIR2` record inspected | `IR2_SCHEMA_REVISION == 1`; serialization reports 1 |

The standalone provenance representation and reconstruction remain legal;
the new restriction is local to integrated fresh startup.

## Field classification and over-rejection audit

`IR2Neuron.__post_init__` and `_validate_cross_fields()` own schema consistency;
`from_quiescent_ir2()` adds only the accepted integrated boundary. “Accepted”
below means schema-valid quiescent history may be present in the transferable
record; the first `START_CHARACTER` reset still establishes the new character
state before processing.

| Field(s) | Category | Integrated startup rule / evidence |
|---|---|---|
| `neuron_id` | STATIC CONFIGURATION | Required non-empty, unique network identity; unchanged. |
| `dynamics_model` | STATIC CONFIGURATION | Must be uniformly `EXCURSION_V1`; mixed/legacy selection rejected. |
| `x` | RESIDUAL LOCAL DYNAMIC STATE | Must compare exactly equal to `0.0`; signed zeros pass, every tested nonzero finite value fails. |
| `local_last_update_time` | RESIDUAL LOCAL DYNAMIC STATE, quiescent local-time history | Schema requires finite nonnegative time; ACP-0004/0005 define local transferable time and do not require it be zero. Probe accepted `10.0`; `START_CHARACTER(timestamp=12.0)` reset the clock to 12 before execution. Not a global time/timestep. |
| `mode` | RESIDUAL LOCAL DYNAMIC STATE | Must be `N`; other valid E2 modes rejected at integration boundary. |
| `decay_rate`, `x_max`, `theta_r`, `theta_e`, `theta_hold`, `theta_m` | STATIC CONFIGURATION | Schema validates finite values and accepted ordering/bounds; adapter does not over-reject non-default values. |
| `delta_t_e`, `delta_t_m_emit`, `delta_t_m_rearm`, `delta_x_e` | STATIC CONFIGURATION | Existing schema/config validation remains authoritative; no timing semantics changed. |
| `a_min`, `a_max`, `neuron_gain` | STATIC CONFIGURATION | Schema validates bounds. `neuron_gain` is not an E2 runtime field and is not a new startup gate. |
| `provenance_capacity`, per-neuron `event_budget` | STATIC CONFIGURATION / resource bounds | Schema validates finite limits; no change. |
| `ordinary_episode_id`, `lineage_id`, `multi_episode_id` | UNSUPPORTED LIVE-RESUME STATE when active; schema-owned invalidity in `N` | N-mode cross-field validator forbids non-`None` IDs. Live modes are rejected by the adapter. No duplicate schema validation added. |
| `captured_polarity`, `m_phase` | UNSUPPORTED LIVE-RESUME STATE | N-mode schema rejects captured polarity and phase; active E2 mode is rejected by integration. |
| `pending_internal_event` | UNSUPPORTED LIVE-RESUME STATE | N-mode schema forbids pending work; valid pending work in active modes is rejected at integration. Standalone E2 reconstruction is unchanged. |
| `m_peak` | RESIDUAL LOCAL DYNAMIC STATE, inactive in `N` | A valid nonzero value is accepted by IR-2 and the adapter, but `START_CHARACTER` resets it to zero before any integrated event. ACP-0006 does not require a separate zero gate; no active episode/mode can consume it. |
| `provenance` | RESIDUAL PROVENANCE | Must be empty at integrated startup; standalone transfer still preserves it. |
| `provenance_truncated` | RESIDUAL PROVENANCE | Must be false; sticky loss is rejected even with empty tuple. |
| `unassigned_provenance_count`, `unassigned_provenance_truncated` | RESIDUAL PROVENANCE | Count must be zero and truncation false; existing guard retained. |
| `generation_token` | PERMITTED IDENTITY / COUNTER HISTORY | ACP-0005 includes generation tokens among transferable bounded counters. Accepted by startup; reset to zero at character start under existing reset semantics. |
| `next_event_identity`, `next_episode_identity`, `next_lineage_identity`, `next_input_identity` | PERMITTED IDENTITY / COUNTER HISTORY | Accepted and reconstructed. Output/episode/lineage/input high-water values survive character reset as specified; output identities do not reuse prior IDs. |
| `processed_event_count`, `input_contribution_count` | PERMITTED BOUNDED COUNTER HISTORY | Schema bounds them by event budget; accepted as record history and reset to zero at `START_CHARACTER`, before neural execution. |

**Timestamp interpretation:** ACP-0004 defines local monotonic timestamps and
ACP-0005 carries finite local update time in transferable neuron state.
Neither accepted ACP-0006's quiescent clause nor the Luna-24 authorization
requires zero local timestamp. A nonzero timestamp is not pending work or an
active episode. The integrated character explicitly establishes its own
timestamp by resetting neurons at `START_CHARACTER`; this is observed
behavior, so no timestamp ambiguity or extra guard is inferred.

**Episode-field ownership:** Direct construction probes confirm that an
otherwise-`N` `IR2Neuron` with ordinary episode, lineage, multi-episode,
captured-polarity, M-phase or pending-event residue is rejected by
revision-1 cross-field schema validation. The integration adapter therefore
does not need to duplicate those constraints.

## Empty network and topology/schema ownership

**OBSERVED:** `TPCNIR2(())` is schema-valid, but
`ExcursionCharacterRuntime.from_quiescent_ir2(TPCNIR2(()), ...)` fails during
bounded-topology construction with `ValueError("nodes must contain non-empty strings")`.
The runtime constructor also rejects empty neuron collections. No empty
integrated runtime is created.

**Disposition: NOT APPLICABLE / SCHEMA-PERMITTED.** ACP-0006 does not require
an empty integrated network; IR-2's permissive empty container is a schema
choice, while the experiment runtime needs nodes. This creates no hidden
unbounded or causality behavior and does not justify a redundant adapter rule.

**OBSERVED:** `TPCNIR2` rejects duplicate neuron IDs and an edge endpoint
outside an explicit declared-node set with `ValueError` during construction.
No duplicate topology/schema validation is added by Luna-24.

## Test results and remaining failures

Environment: Windows, Python 3.11.5.

| Command | Independent result |
|---|---|
| `python -m pytest -q tests/test_excursion_integration.py` | **43 passed** |
| `python -m pytest -q tests/test_ir2.py tests/test_e2_ir2.py tests/test_excursion_neuron.py tests/test_e2_multi_excursion.py` | **203 passed** |
| `python -m pytest -q tests/test_experiments.py tests/test_excursion_integration.py` | **55 passed** |
| Prescribed 13-file integration regression set | **334 passed** |
| `python -m pytest -q -rs` | **24 failed, 789 passed, 1 skipped** |
| `python -m pytest --collect-only -q` | **814 tests collected** |
| `python -m compileall -q tpcn tests` | Passed |
| Pylance diagnostics on source and focused tests | No diagnostics |
| `git diff --check` | Passed |

The one skip is `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics` because CUDA is unavailable. The 14 additional passing collected cases correspond to Luna-24's test delta; source diff inspection found no deleted, skipped, xfailed or deselected tests.

The 24 full-suite failures match the already classified downstream groups:

| File/group | Count | Classification |
|---|---:|---|
| `tests/test_cpu_visualization.py` | 3 | `test_capture_modes_do_not_change_training_result`; `test_snapshot_sequence_is_deterministic_and_replays_offline`; `test_replay_rejects_missing_malformed_and_over_limit_data` |
| `tests/test_luna12b_integration.py` | 4 | `test_structural_run_is_deterministic_and_has_real_bounded_mutations`; `test_capture_is_downstream_only_for_structural_decisions`; `test_controls_report_behavior_and_topology_without_assuming_benefit`; `test_structural_evidence_is_label_isolated` |
| `tests/test_luna12e_integration.py` | 2 | `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`; `test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary` |
| `tests/test_luna12l_temporal_scale.py` | 8 | `test_scale_runner_retains_all_policies_and_causal_evidence`; `test_requested_policy_is_executed_by_classifier[baseline]`; `[random]`; `[temporal]`; `[reversed]`; `test_policy_changes_classifier_execution_state`; `test_policy_scale_cross_product_preserves_provenance_and_serialization`; `test_condition_fails_on_classifier_provenance_mismatch` |
| `tests/test_spiral_benchmark.py` | 1 | `test_control_results_are_deterministic_and_include_required_order_controls` |
| `tests/test_temporal_analysis.py` | 3 | `test_flat_metrics_and_changing_topology_are_reported`; `test_rejection_reason_aggregation_preserves_observed_reasons`; `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` |
| `tests/test_viewer_3d.py` | 3 | `test_layout_and_scene_generation_are_deterministic_and_diagnostic`; `test_topology_deltas_and_bounded_prune_highlights`; `test_playback_filters_selection_neighborhood_and_metrics` |
| **Total** | **24** | All previously known; no Luna-24 failure |

These identities and groups match the pre-existing post-Luna-23 failure set;
no downstream file was changed.

## Architecture audit

- **A01:** The exact production delta adds a startup condition only; no clock,
  tick, scheduler or event-execution rule was introduced.
- **A02:** Neuron equations and temporal evolution are unchanged. Exact
  `x == 0.0` is validated without normalization; valid local timestamp
  history is retained until explicit character reset.
- **A03:** Positive delays, queue ordering and pending-event semantics are
  untouched; active/pending state cannot be resumed by this adapter.
- **A04:** Node, edge, fan-in/out, queue and routing capacities are unchanged;
  valid bounded IR-2 topology is still reconstructed as before.
- **A08:** Assigned and unassigned provenance residue is rejected, never
  erased; event/provenance capacity rules remain unchanged.
- **A15:** This is software-reference integration validation only; it defines
  no hardware checkpoint representation or equivalence claim.

No A01-A15 text, accepted ACP or canonical IR-2 meaning changed. This enforces
the accepted ACP-0006 clause 13 admissibility boundary and does not redefine
valid standalone serialized provenance.

## Dataset and governance status

**DATASET EVIDENCE GATE — STILL UNRESOLVED.** The reported UCI Character
Trajectories result has no retained exact loader/split script and per-class
table. This review did not download data, run a replacement benchmark or
claim reproduction.

Luna-24 is **CLOSED / INDEPENDENTLY VERIFIED**. Luna-23 remains
**CLOSED / INDEPENDENTLY VERIFIED**. Luna-22 remains **BLOCKED / NOT CLOSED**:
the dataset reproducibility/per-class evidence and downstream compatibility
decisions remain separate open requirements. No ACP-0006 repository-wide
integration readiness is claimed.

The downstream group is not one semantic migration: visualization expects
scalar observations; structural tests invoke a disabled first-integration
policy; temporal/spiral consumers encode experiment assumptions; temporal
analysis and the 3D viewer are observers. No broad “make all tests pass” task
is authorized. The next bounded action is to authorize reproducible
sequential-dataset evidence independently; consumer-by-consumer compatibility
decisions remain deferred for later Luna-0 governance.

## Terminal verdict

**PASS — LUNA-24 ACP-0006 IR-2 QUIESCENT PROVENANCE BOUNDARY
INDEPENDENTLY VERIFIED / CLOSED.**

Keep Luna-22 blocked, keep Luna-23 closed, and return for a fresh Luna-0
integration decision after the dataset and separately governed downstream
compatibility work. No production repair or downstream migration was
performed during this review.
