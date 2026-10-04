# Luna-29 Completion Handoff — ACP-0007 CPU Structural Replay Compatibility

- Contract version: 1.2 (unchanged)
- Status: **awaiting Luna-0 independent review** (not self-closed; no successor authorized)
- Execution source: `d000d882482e1e9e1c7cd00a0a03f5d1a03931f1` (`docs: clarify Luna-29 execution baseline`), clean `main == origin/main` verified after fetch
- Authorization publication / lineage floor: `aad4b0db09773ebca9314d188c3b24297ad17c44` (verified ancestor; the only post-floor commit is d000d88, governance-only: agent contract, workflow doc, changelog, authorization/compatibility/corrective handoffs)
- Compatibility-review baseline: `c654ffe9c8d4a6d179781696d9ba5cd239e12795` (not an execution gate)
- Execution starting revision: `d000d882482e1e9e1c7cd00a0a03f5d1a03931f1`
- Implementation revision: `252fa15073e983a793a06b0ba3c79c84ced84637`
- Handoff publication revision: separate documentation commit following the implementation commit (this handoff); final synchronized publication revision is recorded in the Luna-0 return.
- Result revision: implementation revision `252fa15073e983a793a06b0ba3c79c84ced84637`; handoff publication is separate.

## Owned files changed

- `tpcn/cpu_visualization.py`
- `tests/test_luna12b_integration.py`
- `tests/test_cpu_visualization.py`
- `workflow/handoffs/luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md`

No other file was modified (CLI, experiments, structural, topology, TPCV codec, viewers, GPU/FPGA untouched).

## Helper API

`run_cpu_training(*, config: ExperimentConfig | None = None, epochs: int | _NotProvided = _NOT_PROVIDED, seed: int | _NotProvided = _NOT_PROVIDED, examples_per_class: int = 2, snapshot_every: int = 0, max_snapshots: int = 64, structural_plasticity: bool | _NotProvided = _NOT_PROVIDED, learning_enabled: bool | _NotProvided = _NOT_PROVIDED)`

- `config` must be an `ExperimentConfig` (else `TypeError`); it is the source of truth for all runner settings and its seed drives `make_synthetic_workload`.
- Private sentinel defaults distinguish omitted runner scalars from explicitly supplied values (including `None`). Scalar runner options supplied alongside `config` that differ from it raise `ValueError("... conflicts with the supplied ExperimentConfig")`; equal values are accepted.
- Without `config` the legacy convenience route is unchanged (epochs=3, seed=0, structural_plasticity=False, learning_enabled=True; fixed-topology E2 default).
- `structural_plasticity=True` without config still builds the legacy config and is rejected by existing E2 validation (no invented neighborhood/policy/bounds).
- Capture (`snapshot_every`, `max_snapshots`) and workload size (`examples_per_class`) remain separate from runner configuration. `tpcn/experiments.py` guard untouched; E2 pruning not enabled; TANH is not the default.

## Explicit E2 fixture (tests)

Nodes `neuron-0..2`; `structural_neighbors = {neuron-0: (neuron-2,), neuron-1: (), neuron-2: ()}`; policy `e2_local_temporal`, `structural_observation=True`; neighborhood limit 2, reverse-observer limit 2, association window 4.0, history capacity 8, candidate capacity 4, max score 3, growth delay 0.4, growth attempt budget 4; fan-in 2, fan-out 2, edge capacity 4; `energy_weight=1.0`, neutral reward, settling horizon 8.0. Initial topology: chain `neuron-0→neuron-1→neuron-2` (delay 0.2, divider 0, reference 1.0), installed on the runner as in the Luna-28 fixture (private `_topology`/`plasticity.topology`/`_network.set_topology`) with one 3.5-amplitude character.

Public `structural_decisions` result: status `grown`, rank 1, `neuron-0→neuron-2`, delay 0.4; metrics: attempts 1, mutation_count = accepted_additions = 1, rejected 0, pruned 0, connections 3/4, finite utilization ≤ 1, mutation history ≤ 32.

## TPCV-2 replay

Pre-growth snapshot (initial chain) plus captured post-growth snapshot, both `EXCURSION_FORMAT_VERSION`: `connection_timeline` shows `added_connections == (("neuron-0","neuron-2"),)`, unchanged chain edges, no `recently_pruned_connections`. A separate generic synthetic replay test still shows an adjacent-snapshot removed edge as `recently_pruned_connections`, with no E2-pruning implication.

## Capture equality and label evidence

Capture off vs on: identical `TrainingResult`, `structural_decisions` and final topology; off yields no snapshots. Label A vs Z: equal emission observations, candidates (score/identity), selected candidate, rank, status, before/after topology and final topology (not `mutation_history` alone).

## Migrated Luna-12B tests (all four pass)

1. deterministic bounded mutations → growth-only E2 decisions/snapshots, no pruning requirement
2. capture downstream-only → decisions, topology, snapshot on/off, TPCV-2 added edge
3. controls → fixed / E2 / learning-off; `event_count == processed_event_count`, `activation_count == excursion_count`, energy ≥ 0, `utility == reward - energy` (explicit `energy_weight=1.0`), no benefit assumed
4. label isolation via public structural evidence

Added: config helper/conflict/TypeError tests, default route + legacy boolean rejection, no-E2-pruning across epochs, explicit `TANH_LEGACY` regression (deterministic, additions and `pruned_connections > 0`, replay `recently_pruned_connections`, capture non-interference).

## Commands (exact)

| Command | Result |
|---|---|
| `python -m pytest -q tests/test_luna12b_integration.py` | 13 passed |
| `python -m pytest -q tests/test_luna28_excursion_structural_growth.py` | 44 passed |
| `python -m pytest -q tests/test_cpu_visualization.py tests/test_visualization.py` | 32 passed |
| `python -m pytest -q tests/test_luna12b_integration.py tests/test_luna28_excursion_structural_growth.py tests/test_cpu_visualization.py tests/test_visualization.py` | 89 passed |
| `python -m pytest -q tests/test_experiments.py` | 12 passed |
| `python -m pytest -q -rs` | 880 passed, 17 failed, 1 skipped; 898 collected |
| `python -m pytest --collect-only -q` | 898 collected |
| `python -m compileall -q tpcn tests` | passed |
| Pylance diagnostics for the three changed Python files | no diagnostics |
| `git diff --check` | passed |

The 17 full-suite failures remain outside the authorized migration: Luna-12E
(2), Luna-12L (8), spiral benchmark (1), temporal analysis (3), and 3D viewer
(3); each fails at the existing opt-in structural-observation guard. The
pre-Luna-29 baseline was 865 passed, 21 failed, 1 skipped (887 collected); the
four Luna-12B failures are resolved, with no new applicable regression.

Collection audit: all existing test targets remain collected; the migration
does not delete or xfail tests, add unconditional skips, or deselect tests.
The existing deterministic/bounded structural test name was retained.

## Architecture audit

- A01: PASS — capture remains a downstream observer; no clock or event execution change.
- A04: PASS — topology, histories, snapshots and metrics remain bounded.
- A06: PASS — prediction/error semantics unchanged.
- A07: PASS — explicit caller-supplied local neighborhood; public structural evidence remains label-isolated.
- A08: PASS — deterministic bounded runtime/history behavior preserved.
- A10: PASS — energy remains diagnostic; no efficacy or energy-benefit assertion.
- A14: PASS within ACP-0007 — opt-in growth only; E2 pruning remains disabled.
- A15: PASS for CPU software reference only; no hardware-equivalence claim.

## Limitations

- `run_cpu_training` builds only the fixed synthetic workload; its low-amplitude inputs with legacy-identity edges produce no downstream emissions, so helper runs with E2 growth enabled yield `no_candidate` (valid but no growth). The real-growth fixture therefore drives `ExperimentRunner` + `CPUTrainingCapture` directly with a custom character and privately injected topology (same technique as Luna-28). No new helper workload/topology API was authorized.
- CLI and other downstream consumers (temporal analysis, 3D viewer, etc.) not migrated or verified; no full-suite or downstream-readiness claim.
- Evidence is mechanism validity only; no accuracy, prediction, reward, energy or task-efficacy benefit is claimed (A10, A14, A15 respected).

CPU replay compatibility: **ESTABLISHED for the authorized Luna-12B helper and
replay path**. ACP-0007 mechanism: **PRESERVED**. Task efficacy: **NOT
ESTABLISHED**. Resource benefit: **NOT ESTABLISHED**.

Returned to Luna-0 for independent review; status is **IMPLEMENTED / PUBLISHED
/ AWAITING INDEPENDENT REVIEW**; no successor authorized. The handoff is
published separately after implementation revision
`252fa15073e983a793a06b0ba3c79c84ced84637`; the resulting publication SHA is
reported by Luna-0 after push.
