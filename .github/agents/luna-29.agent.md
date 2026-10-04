---
name: Luna-29 ACP-0007 CPU Structural Replay Compatibility
description: Migrate the Luna-12B CPU helper and tests to explicit ACP-0007 growth-only E2 configuration and TPCV-2 replay.
---

# Luna-29 — ACP-0007 CPU Structural Replay Compatibility

## Authorization and baseline

Luna-29 is authorized for downstream CPU-helper compatibility implementation
and focused verification only. ACP-0007 is accepted, architecture contract
version 1.2 is unchanged, and Luna-28 is closed and independently verified.
The authorization baseline is clean `main` at
`c654ffe9c8d4a6d179781696d9ba5cd239e12795` (the publication subject is
`docs: close independent Luna-28 review`). The identifier supplied as the
baseline in the dispatch text is not a Git object; use the verified Git SHA
above.

Before editing, verify `HEAD == origin/main`, branch `main`, clean worktree,
and read ACP-0007, the architecture contract, Luna-28 implementation and
independent-review handoffs, this contract, the authorization handoff, the
Luna-12B tests/handoff, CPU helper, replay implementation, and visualization
contract. Stop if the starting revision differs or new architecture decisions
change this authorization.

Mandatory sequence: `Luna-0 authorization -> Luna-29 -> Luna-0 independent
review`. Return a completed evidence handoff to Luna-0. Do not authorize or
execute a successor.

## Objective

Provide a clear public CPU helper boundary for already-authorized ACP-0007
E2 growth and migrate the Luna-12B CPU structural replay assertions from the
pre-ACP-0007 growth-plus-pruning contract to the accepted growth-only
mechanism. This is an adapter/test migration, not a new evidence producer or
architecture change.

The helper must accept the existing public `ExperimentConfig` as an optional
explicit full runner configuration. When supplied, that config is the source
of truth for runner settings and its seed drives synthetic workload
generation. Preserve the existing defaults and scalar convenience route when
no config is supplied. Reject conflicting simultaneously supplied
runner-configuration values rather than silently ignoring them. Keep capture
and workload-size options separate from runner configuration.

The meaning of `run_cpu_training(structural_plasticity=True)` without an
explicit config remains: construct the legacy convenience configuration and
let E2 validation reject it because it lacks ACP-0007's explicit local
observation configuration. Do not invent a neighborhood, policy, bounds, or
demo profile. Callers enable E2 growth by supplying an `ExperimentConfig`
with `structural_observation=True`, `structural_plasticity=True`,
`structural_policy="e2_local_temporal"`, an explicit complete directed
`structural_neighbors` map, and all finite positive ACP-0007 bounds. The
fixed-topology E2 default remains available.

Do not require or enable E2 pruning. Keep historical `TANH_LEGACY`
growth/pruning behavior separately testable with an explicit
`ExperimentConfig(neuron_model="TANH_LEGACY", ...)`; do not make TANH the
default.

## Exact owned files

Luna-29 owns only:

- `tpcn/cpu_visualization.py`
- `tests/test_luna12b_integration.py`
- `tests/test_cpu_visualization.py`
- `workflow/handoffs/luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md`

Do not modify the CPU CLI, core experiment runtime/configuration, structural
observation or association implementation, topology/plasticity controller,
TPCV codec/contract, temporal-analysis, 3D-viewer, Luna-12L, spiral, Luna-12E,
GPU, FPGA or hardware code/tests. If an owned-file fix is insufficient, stop
and report the exact evidence to Luna-0.

## Required compatibility behavior

- Keep capture downstream-only: same config/workload with capture disabled
  and enabled yields identical `TrainingResult` and structural decisions.
- Preserve disabled capture producing no snapshots.
- Use TPCV-2 snapshots of the actual bounded topology. Replay must show an
  admitted growth edge as an adjacent-snapshot addition when the fixture
  records the pre- and post-growth topologies; no TPCV schema change is
  authorized.
- Configure an explicit deterministic small E2 fixture whose observations,
  candidates, ranks/decisions and topology are available through existing
  public `ExperimentMetrics.structural_decisions`. Do not use labels,
  task outcomes, energy, prediction loss, payload magnitude, global trace
  scoring, or implicit neighborhoods.
- Keep a matched fixed-topology control and make no accuracy, prediction,
  reward, or energy benefit requirement.
- Require finite connection/fan-in/fan-out utilization, bounded mutation
  history, explicit growth attempts/admissions/rejections, and no E2 pruning.
- Under label mutation, compare the strongest existing public structural
  evidence: emission observations, candidate score/identity, selected
  candidate/rank/status, before/after topology and final topology. Do not use
  `mutation_history` equality as the sole label-isolation oracle.
- Replace the legacy E2 `event_count == activation_count` assertion with
  the actual E2 metric meanings (`event_count == processed_event_count`,
  `activation_count == excursion_count`). Event and emission counts need not
  be equal. Keep energy nonnegativity. Assert
  `utility == reward - energy` only in a fixture that explicitly uses the
  repository's `energy_weight=1.0` net-utility configuration.
- Remove any requirement for E2 `pruned_connections > 0` or E2
  `recently_pruned_connections`. Preserve generic replay's adjacent-snapshot
  removed-edge representation and a distinct explicit TANH_LEGACY regression.

## Required focused tests

Run:

```text
python -m pytest -q tests/test_luna12b_integration.py
python -m pytest -q tests/test_luna28_excursion_structural_growth.py
python -m pytest -q tests/test_cpu_visualization.py tests/test_visualization.py
```

Tests must cover the config-taking helper contract and conflict/error
behavior; default/fixed behavior and the old boolean's explicit E2 rejection;
deterministic growth-only decisions and snapshots; capture on/off
non-interference; a real added edge visible in TPCV-2 replay; bounded metrics;
label isolation using public evidence; utility/metric semantics; no E2
pruning; and explicit TANH_LEGACY historical pruning compatibility. Generic
synthetic replay must continue to represent edge removal without implying
that E2 pruning is enabled.

Do not repair other full-suite downstream failures. Do not claim full-suite
green or downstream migration readiness.

## Architecture boundary

No ACP is required for a CPU wrapper adapting to existing accepted ACP-0007.
Preserve:

- A01: causal event execution; no neural clock or capture backpressure.
- A04: finite topology and bounded replay/metrics.
- A06: no change to predictive coding or error events.
- A07: no hidden/nonlocal structural evidence or label leakage.
- A08: deterministic bounded histories and existing runtime limits.
- A10: no energy-minimization or efficacy claim.
- A14: opt-in local growth only; no pruning promotion.
- A15: software reference behavior only; no hardware-equivalence claim.

Any request for E2 pruning, hidden neighborhoods, new evidence/score/policy,
TPCV semantic redesign, or new topology-persistence behavior is outside
scope and must return to Luna-0/project owner for governance. Do not edit
`tpcn/experiments.py` to remove its accepted guard.

## Completion handoff

Use contract version 1.2 and record baseline/result revisions, exact owned
files, helper API behavior, explicit topology/bounds, test commands/counts,
TPCV-2 addition replay, capture equality, all four migrated test outcomes,
the TANH_LEGACY regression, full-suite status if run, failed/not-run checks,
and remaining CLI/downstream limitations. Distinguish mechanism validity
from task efficacy and resource benefit. Return to Luna-0; do not authorize
another Luna.
