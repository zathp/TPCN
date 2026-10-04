---
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Post-Luna-29 replay consumer compatibility classification"
  task_id: "luna-0-post-luna29-replay-consumer-compatibility-decision-20261004"
  component: "Temporal analysis and detached 3D replay viewer"
  status: "blocked"
  contract_version: "1.2"
  branch: "main"
  base_revision: "5a0d4f9b8f30a3d436a05f9c3676f86e450b2a05"
  result_revision: "5a0d4f9b8f30a3d436a05f9c3676f86e450b2a05 (governance classification only)"
  dependencies:
    - "Accepted ACP-0007"
    - "Luna-28 closed / independently verified"
    - "Luna-29 closed / independently verified"
  owner: "Luna-0"
  classification: ["GOVERNANCE", "OBSERVATION", "VERIFICATION"]
  hypothesis: "The six temporal-analysis/viewer failures are stale pre-ACP-0007 fixtures over otherwise compatible replay consumers."
  counter_hypothesis: "A consumer defect on valid detached TPCV-2 replay would invalidate a pure fixture-only classification."
  interfaces_relied_on:
    - "ReplaySequence"
    - "TPCV-1 NeuronRecord and TPCV-2 ExcursionNeuronRecord"
    - "analyze_replay and compare_replays"
    - "VisualizationScene.nodes(), inspect(), edges(), and summary()"
  label_information_boundary:
    - "The reviewed consumers receive detached replay snapshots and metrics only; no labels become structural evidence."
  timing_assumptions:
    - "Snapshot epoch/timestamp are observations; neither consumer schedules or executes neural events."
  reset_boundaries:
    - "No neural reset behavior is changed or consumed as a runtime control."
  resource_bounds:
    - "ReplaySequence retains existing bounded record and byte limits."
    - "VisualizationScene bounds renderer history, neighborhood depth, and edge count."
  authorized_scope:
    - "Read-only source/test/governance audit and failure reproduction."
    - "Create this classification handoff."
  unauthorized_scope:
    - "No production or test edits."
    - "No Luna-30 execution or authorization."
    - "No E2 pruning, TPCV schema change, TPCV-3, or architecture promotion."
    - "No Luna-12L, spiral, Luna-12E, CLI, GPU, FPGA, FPAA, or hardware migration."
  controls:
    - "Reproduce only the six assigned consumer failures."
    - "Run unchanged replay and closed Luna-28/Luna-29 focused suites."
    - "Construct one valid TPCV-2 snapshot and exercise viewer nodes()/inspect()."
  measurements:
    - "Targeted pytest pass/fail counts and first failure guard."
    - "Focused unchanged prerequisite suite result."
    - "Runtime result for valid TPCV-2 viewer operations."
  information_boundary_check:
    - "Source inspection confirms both modules consume ReplaySequence and expose detached, descriptive state."
    - "No consumer path feeds analysis/viewer state back to ExperimentRunner or structural evidence."
  hardware_mapping:
    - "Software analysis and visualization only; no hardware validation."
  architecture_invariants_touched:
    - "Audited A01, A04, A06, A07, A08, A10, A14, and A15."
    - "No clause text or architecture scope changed."
  preserves:
    - "ACP-0007 accepted, opt-in, growth-only semantics."
    - "E2 pruning remains unauthorized."
    - "Generic detached edge-removal display remains distinct from computational pruning."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-post-luna29-replay-consumer-compatibility-decision-20261004.md"
  tests_added: []
  tests_passing:
    - "Unaffected CPU/TPCV, Luna-12B, and Luna-28 focused suites: 89 passed."
    - "Valid TPCV-2 parser/runtime probe completed; it reproduced viewer AttributeError in nodes() and inspect()."
  tests_failed:
    - "Assigned temporal-analysis and 3D viewer suites: 6 failed, 3 passed; all six failures stopped at the missing structural-observation configuration guard."
  tests_not_run:
    - "No post-guard consumer assertions were run by altering or bypassing the intentional E2 guard."
    - "No interactive graphics, GPU, FPGA, FPAA, real-dataset, or hardware test was authorized."
  assumptions:
    - "A detached synthetic TPCV-2 sequence is sufficient for consumer-only topology addition/removal tests; no live growth training is required for scene/replay algorithms."
  unresolved:
    - "VisualizationScene.nodes() and inspect() do not support the canonical TPCV-2 ExcursionNeuronRecord shape."
    - "Temporal-analysis limitation strings name TPCV-1 even where the limitation applies to TPCV-2 as well."
    - "No implementation owner or authorized correction task is assigned for the newly observed viewer defect."
  recommended_next_agent:
    - "Luna-0 / project owner: issue a separate bounded correction authorization for the demonstrated TPCV-2 viewer defect before downstream consumer migration."
---

# Terminal verdict

**BLOCKED — CURRENT DOWNSTREAM REPLAY CONSUMER DEFECT.** The six assigned
pytest failures are indeed caused first by pre-ACP-0007 live-training fixture
calls that request `structural_plasticity=True` without explicit structural
observation configuration. However, an independent valid TPCV-2 replay probe
demonstrates a separate existing defect in `tpcn/viewer_3d.py`: both
`VisualizationScene.nodes()` and `VisualizationScene.inspect()` access
`.activation` on an `ExcursionNeuronRecord`, which intentionally has no such
field. TPCV-2 defines `active`, excursion `mode`, `state`, and
`processed_events`; it does not define scalar activation. Therefore the
current viewer cannot be classified as compatible with valid TPCV-2 replay
without a bounded implementation correction.

No production or test file was changed. The starting and classification
revision is clean synchronized `main`, `HEAD == origin/main ==
5a0d4f9b8f30a3d436a05f9c3676f86e450b2a05`, subject
`docs: close independent Luna-29 review`. The Luna-29 closure remains intact:
ACP-0007 is accepted, Architecture Contract 1.2 remains authoritative,
Luna-28 and Luna-29 remain closed, fixed topology remains the ordinary
EXCURSION_V1 default, a bare E2 structural boolean remains invalid, and E2
pruning remains unauthorized.

## Reproduction and validation

| Command or procedure | Observed result |
|---|---|
| `python -m pytest -q tests\test_temporal_analysis.py tests\test_viewer_3d.py` | 6 failed, 3 passed. All six failing cases raise `ValueError: structural plasticity is unavailable unless structural observation is enabled` while constructing the existing obsolete `run_cpu_training(..., structural_plasticity=True)` fixtures. No guard was bypassed. |
| `python -m pytest -q tests\test_cpu_visualization.py tests\test_visualization.py tests\test_luna12b_integration.py tests\test_luna28_excursion_structural_growth.py` | 89 passed. |
| Pylance-selected Python 3.11.5 runtime probe: construct/export/parse a TPCV-2 `ExcursionNeuronRecord`, then call scene nodes and inspect | Both calls reproduce `AttributeError: 'ExcursionNeuronRecord' object has no attribute 'activation'`; record format is 2, `active` is false, and `has_activation` is false. |

The six reproduced failures are:

1. `test_flat_metrics_and_changing_topology_are_reported`
2. `test_rejection_reason_aggregation_preserves_observed_reasons`
3. `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation`
4. `test_layout_and_scene_generation_are_deterministic_and_diagnostic`
5. `test_topology_deltas_and_bounded_prune_highlights`
6. `test_playback_filters_selection_neighborhood_and_metrics`

The three other tests in those files pass at this revision. The failures
confirm the stale fixture setup only; they do not establish that the
post-migration consumer assertions pass.

## Source classification

### Temporal analysis

`tpcn.temporal_analysis` accepts `ReplaySequence`; it does not call
`run_cpu_training`, inspect a live runner/topology, select a structural policy,
or mutate topology. Its algorithms calculate snapshot lifetimes, topology
changes, supplied metric deltas, and supplied rejection counts. The analyzer
is **replay-only, descriptive, non-causal, and downstream**. No E2 pruning,
TANH behavior, or historical structural policy is required.

The old workload-based `"improving behavior"` expectation is not a
mechanism requirement. A future compatibility test should supply a detached
sequence with explicit topology changes and controlled metrics, and assert
the descriptive classification from those values. The analyzer should report
the evidence supplied, not require the E2 workload to improve.

`USAGE_UNAVAILABLE` and the `limitations` entry say “TPCV-1” for restrictions
that also apply to TPCV-2: neither snapshot schema carries per-edge routed
event identities/paths, and neither makes a per-neuron emitted-event
identity available for deriving edge exercise. These strings are stale and
should be made version-neutral in a future bounded compatibility task, e.g.
“TPCV snapshots encode topology existence, not per-edge event paths.”
No new usage field or TPCV codec change is necessary.

The analyzer's use of `active` and `processed_events` is compatible with
TPCV-2. Its `activation_count` is an aggregate count of active neurons, not a
claim that TPCV-2 has a scalar activation field. Preserve that distinction;
do not add scalar activation semantics to EXCURSION_V1.

### 3D viewer

`tpcn.viewer_3d` accepts a `ReplaySequence`, stores renderer/camera/filter
state, and derives diffs from adjacent immutable snapshots. It has no
execution object or computation feedback path. Added/removed edges are
differences between replay snapshots. `EdgeView(kind="pruned")` is a
visualization label for a previously present edge no longer present in a
later snapshot; it is not an E2 pruning operation or authorization.

The confirmed defect is the unconditional scalar-activation access in
`nodes()` and `inspect()`. This conflicts with the canonical TPCV-2
`ExcursionNeuronRecord` schema. The Luna-12C viewer component is the
historical component owner; Luna-0/project owner must assign an authorized
correction owner before implementation. No change to
`tpcn/viewer_3d.py` is authorized by this governance classification.

## Assertion-by-assertion matrix

| Test / assertion | Historical assertion | Intended consumer invariant | ACP-0007 / TPCV-2 status | Disposition for future migration | Replacement evidence | Production change required? | Architecture change required? |
|---|---|---|---|---|---|---|---|
| Temporal: `test_flat_metrics_and_changing_topology_are_reported` | One helper training run has non-flat prediction loss; topology changes with non-flat metrics; classification is specifically “changing topology / improving behavior”; metric deltas exist. | Analyzer reports supplied flatness, topology deltas, classification, and metric deltas. No efficacy assumption. | E2 does not promise metric improvement; TPCV-2 supplies topology and metrics are detached replay metadata. | Replace workload-specific flatness/improvement assumptions with a deterministic replay whose metric trend and edge additions are explicit. Keep metric-delta assertion. | Known adjacent-snapshot topology delta and controlled metrics; assert classification derived from supplied accuracy trend. | No, except version-neutral limitations wording if included. | No. |
| Temporal: `test_rejection_reason_aggregation_preserves_observed_reasons` | Arbitrary training run must emit duplicate rejection and at least one acceptance. | Analyzer preserves recorded reasons/counts; does not generate them. | ACP-0007 outcomes are observable, but no specific workload must produce a duplicate. | Replace live-run outcomes with explicit serialized rejection metrics; retain aggregation and accepted/attempt arithmetic assertions. | Synthetic metric rows explicitly containing `duplicate`, `accepted_additions`, and `mutation_rejection_reasons`. | No. | No. |
| Temporal: `test_compare_runs_reports_raw_metric_deltas_without_claiming_causation` | Compares two helper training runs, one with invalid bare structural boolean. | Compare supplied replays' raw metric/topology/activity values and digests without a causal/superiority claim. | Valid detached TPCV-2 is sufficient; no structural learning required. | Replace both live runs with two deterministic detached replays; retain non-null raw values, delta key, and digest checks. | Two replay fixtures with explicitly distinct metadata/metric timelines. | No. | No. |
| Viewer: `test_layout_and_scene_generation_are_deterministic_and_diagnostic` | Two old live structural runs happen to generate replay/layout; positions/nodes/digest match. | The same replay yields deterministic diagnostic positions, nodes, and scene state. | A detached TPCV-2 fixture is sufficient; no growth training required. | Replace live helper fixture with a deterministic replay. This assertion is currently blocked by `nodes()` activation access on TPCV-2. | Repeat scene creation from byte-identical TPCV-2 records. | **Yes —** TPCV-2-safe view projection in `tpcn/viewer_3d.py` is needed first. | No. |
| Viewer: `test_topology_deltas_and_bounded_prune_highlights` | One training run must show an added edge and a pruned edge; history remains bounded. | Show additions and removed-edge highlights from detached snapshot differences; bound viewer history. | TPCV-2 edge sets support both. A removed edge in test replay is synthetic visualization evidence, not E2 pruning. | Retag removal provenance as synthetic replay capability; use deterministic snapshot 0 baseline, snapshot 1 addition, snapshot 2 removal; keep bounded history assertion. | Synthetic detached TPCV-2 adjacent snapshots with known deltas. | **Yes —** viewer TPCV-2 access correction needed before rendering nodes. | No. |
| Viewer: `test_playback_filters_selection_neighborhood_and_metrics` | Playback/filter/camera assertions indirectly depend on old live structural training. | Selection, neighborhood, metrics, active filter, stepping/tick, and camera controls behave deterministically on replay. | These are detached viewer-state behaviors; E2 growth and pruning are irrelevant. | Replace fixture with deterministic detached TPCV-2 replay and explicit metrics. | Multi-snapshot TPCV-2 sequence and explicit metric timeline; verify node activity comes from the record's `active` field. | **Yes —** `nodes()` and `inspect()` currently fail on `ExcursionNeuronRecord`. | No. |

## Fixture, addition, and removal decisions

- **Live training versus replay:** these analysis and viewer assertions
  exercise offline consumers. Prefer deterministic detached replay bytes and
  explicit metrics over an arbitrary live structural-training run. Do not
  bypass the E2 validation guard to reach later assertions.
- **E2 addition:** a real E2-generated edge is not required for every
  consumer assertion. Luna-29 already verified a real admitted edge in
  TPCV-2. Consumer tests can use a deterministic snapshot addition.
- **Viewer removal highlight:** retain generic display of an edge that
  disappears between snapshots. Use a synthetic detached replay and state
  that its removal is not an E2 prune. Do not enable or imply E2 pruning.
- **TPCV-2 adequacy:** records provide node state/activity/mode,
  processed-event counts, topology edges and propagation delays, epoch, and
  an external metrics timeline. These suffice for the described lifetime,
  topology-diff, playback, and diagnostic-layout behaviors once the viewer
  reads the correct TPCV-2 record shape. Per-edge event-use evidence remains
  unavailable; preserve that as unavailable. No TPCV-3 or codec change is
  justified.
- **Activation terminology:** TPCV-1 retains its compatibility scalar
  activation. TPCV-2 explicitly has no activation field. `active` is the
  canonical excursion activity indicator. A future viewer correction should
  represent activation as absent/`None` for TPCV-2 rather than synthesizing a
  scalar.
- **Temporal analyzer source:** a small wording correction to
  `tpcn/temporal_analysis.py` is justified in a future authorized migration
  because its version-specific limitation text is stale. Its algorithm does
  not otherwise require a production change for the six fixture failures.
- **Viewer source:** `tpcn/viewer_3d.py` has a demonstrated compatibility bug
  on valid TPCV-2, not merely a stale fixture. This blocks a clean
  fixture-only consumer migration until separately authorized and corrected.

## Architecture audit

| Clause | Finding |
|---|---|
| A01 | Analyzer and viewer operate after capture on replay; no neural clock, runtime work, or capture backpressure. |
| A04 | Replay bounds, scene history, neighborhood depth, and maximum rendered edges are finite. |
| A06 | No predictive/error computation changes; metrics are descriptive. |
| A07 | No label/task-derived structural evidence; analysis and rendering are downstream only. |
| A08 | Replay digest/layout are deterministic; viewer history is bounded. |
| A10 | No energy minimization or improvement objective is required; comparisons expose raw deltas without causation. |
| A14 | ACP-0007 remains opt-in and growth-only; removed-edge display is not E2 pruning. |
| A15 | CPU/software replay consumers only; no hardware-equivalence claim. |

**ACP required? No** for a future correction limited to replay fixtures,
version-neutral analyzer wording, and TPCV-2 view projection. No new topology,
learning, event-use, or schema semantics are implicated.

**Luna-30 authorized? No.** This review stops at the demonstrated production
consumer defect under the requested blocked outcome. No Luna-30 contract or
implementation task is created. Luna-0/project owner should issue a new,
bounded authorization that owns the TPCV-2 viewer projection defect and the
test-fixture migration; only after that may downstream compatibility be
reassessed.

The next authorized correction should consider these candidate files only:

- `tests/test_temporal_analysis.py`
- `tests/test_viewer_3d.py`
- `tpcn/temporal_analysis.py` (version-neutral capability-limit wording)
- `tpcn/viewer_3d.py` (only the demonstrated TPCV-2 activation projection defect)
- a narrowly scoped completion handoff

Keep `tpcn/cpu_visualization.py`, `tpcn/visualization.py`,
`tpcn/experiments.py`, CLI, GPU, FPGA, FPAA, and hardware paths prohibited
unless new evidence and separate authorization justify an expansion. No ACP,
TPCV-3, E2 pruning, structural-evidence change, or architecture promotion is
requested.

## Remaining independent failure groups

This governance review does not include:

- Luna-12E: 2 legacy-observable assertions.
- Luna-12L: 8 structural-policy/configuration failures.
- Spiral benchmark: 1 structural-policy/configuration failure.

They remain separate governance tracks and are not authorized by this
classification. The unchanged prerequisite slices passed 89 tests; no other
failure groups were rerun here.

## Repository and publication state

At the start, `main` was clean and synchronized at the required revision.
This handoff records the current read-only classification; before any future
publication, verify that no concurrent repository change has altered the
branch or worktree. The attached assignment snapshot was read-only and was
not modified.
