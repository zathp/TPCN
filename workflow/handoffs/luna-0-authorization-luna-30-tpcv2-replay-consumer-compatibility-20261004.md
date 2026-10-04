---
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-30 TPCV-2 replay consumer compatibility authorization"
  task_id: "luna-0-authorization-luna-30-tpcv2-replay-consumer-compatibility-20261004"
  component: "Detached temporal-analysis and 3D replay consumers"
  status: "authorized-not-executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "727a00aed08a4ba2c7194a70cde603f60ab35065"
  result_revision: "governance-only authorization publication"
  dependencies:
    - "Accepted ACP-0007"
    - "Luna-28 closed / independently verified"
    - "Luna-29 closed / independently verified"
    - "Post-Luna-29 compatibility classification at 727a00aed08a4ba2c7194a70cde603f60ab35065"
  owner: "Project owner / Luna-0"
  classification: ["IMPLEMENTATION", "COMPATIBILITY", "FOCUSED VERIFICATION"]
  hypothesis: "The TPCV-2 activation AttributeError can be corrected by an optional downstream projection while preserving TPCV-1 scalar values, and stale consumer fixtures can be replaced with deterministic detached replay."
  counter_hypothesis: "A fix requiring schema, computation, topology, structural evidence, pruning, event-timing, or wider API changes is outside authorization and must stop."
  interfaces_relied_on:
    - "ReplaySequence"
    - "TPCV-1 NeuronRecord"
    - "TPCV-2 ExcursionNeuronRecord"
    - "VisualizationScene.nodes() and inspect()"
    - "analyze_replay() and compare_replays()"
  label_information_boundary:
    - "Detached consumer tests may include metrics for descriptive reporting only; no labels or task outcomes become structural evidence."
  timing_assumptions:
    - "Snapshot epoch and timestamps remain observations only; no event execution or neural clock is introduced."
  reset_boundaries:
    - "No neural reset or character lifecycle changes."
  resource_bounds:
    - "Existing ReplaySequence byte/record caps and scene history, neighborhood-depth, and edge-count limits remain unchanged."
  authorized_scope:
    - "Correct `NodeView.activation` projection to float for TPCV-1 and None for TPCV-2."
    - "Correct inspection activation projection with the same version distinction."
    - "Keep TPCV-2 activity filtering on canonical `active`; do not synthesize activation."
    - "Make TPCV-1-specific temporal-analysis limitation text version-neutral without adding edge-use data."
    - "Migrate the three temporal-analysis and three viewer tests to deterministic detached replay and explicit metrics."
    - "Add direct TPCV-2 and TPCV-1 compatibility regressions and required replay controls."
  unauthorized_scope:
    - "No TPCV schema/codec change and no TPCV-3."
    - "No E2 pruning, N3, topology, structural evidence, event timing, or computation changes."
    - "No change to `tpcn/cpu_visualization.py`, CPU helper, experiments, visualization schema, CLI, GPU, FPGA, FPAA, or hardware."
    - "No Luna-12L, spiral, or Luna-12E migration."
    - "No efficacy/resource-benefit or hardware-equivalence claim."
  controls:
    - "Direct valid TPCV-2 ExcursionNeuronRecord baseline regression."
    - "Active/nontrivial-state adversarial record proves no scalar synthesis."
    - "TPCV-1 exact scalar activation regression."
    - "Synthetic detached snapshot removal distinct from E2 pruning."
    - "Malformed replay and closed TPCV/Luna-28/Luna-29 regressions."
  measurements:
    - "Consumer, replay, closed-prerequisite, combined, full-suite, collection, compileall, and diagnostic results."
    - "No accuracy, prediction-loss, reward, utility, or energy improvement threshold."
  information_boundary_check:
    - "Analysis and viewer continue to consume detached replay only; snapshot difference is not an E2 pruning record."
  hardware_mapping:
    - "Software replay consumers only; no hardware validation."
  architecture_invariants_touched:
    - "A01, A04, A06, A07, A08, A10, A14, A15 audited; no substantive clause change."
  preserves:
    - "TPCV-1 activation float and TPCV-2 activation absence."
    - "TPCV-2 active/mode/state/processed-event meanings."
    - "Per-edge usage unavailable without route/event identity."
    - "Generic removed-edge visualization without E2 pruning authorization."
    - "Accepted ACP-0007 growth-only semantics."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-30.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-30-tpcv2-replay-consumer-compatibility-20261004.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Governance source audit confirms TPCV-2 ExcursionNeuronRecord intentionally has no activation; the defect is in downstream view projection."
    - "Governance source audit confirms analyzer and viewer operate on ReplaySequence and do not feed back into computation."
  tests_failed:
    - "Pre-authorization consumer reproduction recorded at baseline: 6 failed, 3 passed, all six first blocked by the missing structural-observation guard."
  tests_not_run:
    - "No production correction or test migration executed in this authorization invocation."
    - "Full suite and post-correction gates await Luna-30."
  assumptions:
    - "A deterministic synthetic detached TPCV-2 replay can exercise consumer snapshot differences without representing a live E2 growth/prune run."
  unresolved:
    - "Luna-30 completion and independent review remain outstanding."
    - "Luna-12E, Luna-12L, and spiral failures remain separate and out of scope."
  recommended_next_agent:
    - "Luna-30 — TPCV-2 Replay Consumer Compatibility Correction, implementation/verification only."
---

# Decision

**AUTHORIZED — LUNA-30 TPCV-2 REPLAY CONSUMER COMPATIBILITY CORRECTION;
NOT EXECUTED.** The authorization is limited to the TPCV-2 optional
activation projection defect in the detached viewer, version-neutral
temporal-analysis limitation wording, and migration of the six assigned
consumer tests to deterministic detached replay fixtures.

## Starting revision and closed status

Authorization starts from clean synchronized `main`:

- `HEAD == origin/main == 727a00aed08a4ba2c7194a70cde603f60ab35065`
- Subject: `docs: classify replay consumer compatibility blockers`
- The required revision is an ancestor of `HEAD`.
- No worktree changes were present before authorization.

The full blocked result is preserved in
`workflow/handoffs/luna-0-post-luna29-replay-consumer-compatibility-decision-20261004.md`.
Its terminal classification remains **BLOCKED — CURRENT DOWNSTREAM REPLAY
CONSUMER DEFECT** until Luna-30 implements and Luna-0 independently reviews
the bounded correction.

ACP-0007 remains accepted; Architecture Contract 1.2 remains unchanged;
Luna-28 and Luna-29 remain closed and independently verified. Fixed topology
remains the E2 default, growth remains explicit opt-in, E2 pruning and N3
remain unauthorized, and TPCV-2 remains canonical for downstream
EXCURSION_V1 observation.

## Defect and semantics

Canonical TPCV-2 `ExcursionNeuronRecord` contains neuron ID, `active`, mode,
state, pending internal work, processed-event count, and optional position.
It intentionally has no `activation` field. The blocked-review probe
reproduced `AttributeError` in `VisualizationScene.nodes()` and
`VisualizationScene.inspect()` on a valid parsed TPCV-2 record.

Luna-30 must expose the compatibility slot as `float | None`:

- TPCV-1 `NeuronRecord`: retain the exact scalar activation.
- TPCV-2 `ExcursionNeuronRecord`: return `None`.
- Do not derive a scalar from `active`, state, mode, payload, or processed
  events. Continue to use `active` for TPCV-2 active-only filtering.

`tpcn.temporal_analysis` remains detached, replay-only, descriptive, and
non-causal. Its TPCV-1-specific event-path/per-edge-usage limitation wording
may be made version-neutral. Per-edge usage remains unavailable without
event-path evidence; do not add fields or infer use from edge existence.

## Consumer fixture decisions

The six targeted baseline failures are stale calls to
`run_cpu_training(..., structural_plasticity=True)` without required
ACP-0007 observation settings; they fail at the explicit configuration
guard. Luna-30 must not bypass that guard. The analysis and viewer behavior
is downstream of replay, so deterministic detached TPCV-2 sequences and
explicit metric timelines are the appropriate tests.

The viewer fixture may contain a baseline, an adjacent-snapshot addition,
then an edge disappearance. The disappearance is **synthetic detached
replay evidence** for generic visualization behavior only; it is not an
ACP-0007 E2 pruning event. The analyzer must classify explicitly controlled
metric trends, aggregate explicitly supplied rejection reasons, and report
comparison deltas without causal/superiority claims. No task-benefit
assertion is authorized.

Luna-29 already independently demonstrated that a real ACP-0007 edge
addition is representable in TPCV-2. Luna-30 need not repeat live structural
training for these consumer tests.

## Exact Luna-30 contract and ownership

Descriptive name: **Luna-30 — TPCV-2 Replay Consumer Compatibility
Correction**.

Contract: `.github/agents/luna-30.agent.md`.

Authorization handoff: this file,
`workflow/handoffs/luna-0-authorization-luna-30-tpcv2-replay-consumer-compatibility-20261004.md`.

Luna-30 may own only:

- `tpcn/viewer_3d.py` — version-aware activation absence projection only.
- `tpcn/temporal_analysis.py` — version-neutral capability-limit wording
  only.
- `tests/test_viewer_3d.py`.
- `tests/test_temporal_analysis.py`.
- `workflow/handoffs/luna-30-tpcv2-replay-consumer-compatibility-20261004.md`.

Prohibited files include `tpcn/visualization.py`,
`tpcn/cpu_visualization.py`, `tpcn/experiments.py`,
`tpcn/structural_observation.py`, `tpcn/temporal_association.py`,
`tpcn/structural_plasticity.py`, `tpcn/topology.py`,
`tpcn/excursion_neuron.py`, `Main.py`, `viz_tpcn_3d.py`, CPU CLI, GPU, FPGA,
FPAA, hardware, Luna-12L, spiral, Luna-12E, and all other unlisted code/tests.
If a prohibited file is necessary, stop and return to Luna-0; do not broaden
scope.

## Required verification

The contract requires direct valid TPCV-2 regression in `nodes()` and
`inspect()`, `None` activation for TPCV-2 including an active/nontrivial-state
adversarial record, exact TPCV-1 float preservation, active filtering from
canonical `active`, deterministic layout/state, playback/selection/
neighborhood/metrics, addition/removal display with synthetic provenance,
explicit replay metrics/rejections/comparison, and edge-use-unavailable
controls.

Focused tests:

```text
python -m pytest -q tests/test_temporal_analysis.py tests/test_viewer_3d.py
python -m pytest -q tests/test_cpu_visualization.py tests/test_visualization.py
python -m pytest -q tests/test_luna12b_integration.py tests/test_luna28_excursion_structural_growth.py
```

All assigned tests must pass. Also run the combined six-file focused suite,
`python -m pytest -q -rs`, `python -m pytest --collect-only -q`,
`python -m compileall -q tpcn tests`, `git diff --check`, and diagnostics for
all four changed Python/test files. Preserve test collection; no deletion,
xfail, skip, or deselection to manufacture a pass.

The preceding full-suite baseline was 880 passed, 17 failed, 1 skipped,
898 collected. Luna-30 must obtain zero temporal-analysis failures and zero
viewer failures with no new applicable regression. Expected remaining
unrelated groups are Luna-12E (2), Luna-12L (8), and spiral (1); record actual
results rather than assuming totals.

## Architecture and governance boundary

Audit A01, A04, A06, A07, A08, A10, A14, and A15 in the completion handoff.
No architecture or ACP change is required: this assignment changes no
schema, neural computation, structural evidence, pruning, topology
persistence, or event timing. No hardware equivalence is authorized.

The required sequence is **Luna-0 -> Luna-30 -> Luna-0**. This governance
publication authorizes implementation but does not execute it or close the
blocked review.
