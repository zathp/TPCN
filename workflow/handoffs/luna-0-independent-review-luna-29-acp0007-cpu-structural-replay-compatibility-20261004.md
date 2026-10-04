---
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of Luna-29 CPU structural replay compatibility"
  task_id: "luna-0-independent-review-luna-29-acp0007-cpu-structural-replay-compatibility-20261004"
  component: "CPU visualization helper, Luna-12B CPU/TPCV-2 compatibility fixture"
  status: "complete"
  contract_version: "1.2"
  branch: "main"
  base_revision: "6e1387967de2d1170d5743a38927afe08b9ddab8"
  result_revision: "6e1387967de2d1170d5743a38927afe08b9ddab8 (reviewed code; closure publication is governance-only)"
  dependencies:
    - "Accepted ACP-0007"
    - "Closed Luna-28 implementation"
    - "Luna-29 authorization and implementation handoff"
  owner: "Luna-0"
  classification: ["VERIFICATION"]
  hypothesis: "The authorized config-taking CPU helper and migrated Luna-12B fixture preserve legacy convenience behavior, provide explicit bounded E2 configuration, and replay admitted growth in TPCV-2 without changing computation."
  counter_hypothesis: "A scoped regression, unauthorized architectural change, label/task leakage, unbounded mutation, E2 pruning, or failure to represent the fixture's admitted edge would block closure."
  interfaces_relied_on:
    - "run_cpu_training(config=ExperimentConfig(...))"
    - "ExperimentRunner and ExperimentConfig"
    - "ExperimentMetrics.structural_decisions"
    - "CPUTrainingCapture and ReplaySequence.connection_timeline()"
    - "TPCV-2 snapshot export and parsing"
  label_information_boundary:
    - "The E2 observation/candidate/admission path uses actual emissions and the explicit static bounded neighborhood; label-mutation tests compare public evidence and topology."
    - "No labels, task outcomes, energy, prediction loss, payload magnitude, or global trace scoring are introduced as structural evidence."
  timing_assumptions:
    - "E2 admission is post-character and quiescent under accepted ACP-0007."
    - "TPCV-2 is a downstream snapshot/replay representation; it does not participate in execution."
  reset_boundaries:
    - "The reviewed fixture uses the existing character-local E2 evidence lifecycle and the existing runner reset boundary."
  resource_bounds:
    - "The E2 fixture explicitly configures finite observation, candidate, history, growth-attempt, topology, queue, event, and replay bounds."
    - "Tests assert bounded connection/fan-in/fan-out utilization and mutation history."
  authorized_scope:
    - "Read-only independent review of Luna-29 implementation and evidence."
    - "If passing, governance-only review handoff, workflow, and changelog closure."
  unauthorized_scope:
    - "No production-code or test changes."
    - "No E2 pruning, N3, architecture promotion, hardware-equivalence claim, or downstream migration."
    - "No temporal-analysis, 3D viewer, Luna-12L, spiral, Luna-12E, GPU, FPGA, or CLI repair."
  controls:
    - "Default/fixed-topology helper path versus explicit E2 config."
    - "Capture disabled versus enabled."
    - "Deterministic repeated structural fixture."
    - "Label mutation with identical temporal input."
    - "Explicit TANH_LEGACY behavior kept separate from E2."
  measurements:
    - "Focused, combined, regression, full-suite, and collection test results."
    - "E2 decision, mutation, capacity, utilization, pruning, and TPCV-2 edge-delta assertions."
    - "Full-suite failure count and cause reconciliation."
  information_boundary_check:
    - "The structural-decision equality test compares observations, candidates, selected candidate, rank/status, before/after topology, and final topology across labels."
    - "Capture-on/off results and structural decisions are equal."
  hardware_mapping:
    - "CPU software-reference path only; no hardware mapping or equivalence was validated."
  architecture_invariants_touched:
    - "Reviewed preservation of A01-A15; no contract clause text or scope changed."
    - "ACP-0007 remains accepted, opt-in, growth-only, and bounded."
  preserves:
    - "Default fixed topology and scalar convenience behavior."
    - "Explicit rejection of a bare structural_plasticity=True E2 request."
    - "Generic replay representation of removed edges."
    - "Explicit TANH_LEGACY growth/pruning regression behavior."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Luna-12B integration: 13 passed."
    - "Luna-28 E2 structural growth: 44 passed."
    - "CPU visualization and TPCV visualization: 32 passed."
    - "Combined Luna-12B/Luna-28/CPU-TPCV slice: 89 passed."
    - "Experiment regression: 12 passed."
    - "Collection audit: 898 tests collected."
    - "Compileall, Pylance diagnostics for changed Python files, and git diff --check passed."
  tests_failed:
    - "Full suite: 880 passed, 17 failed, 1 skipped. Failures are outside Luna-29's changed paths; see reconciliation below."
  tests_not_run:
    - "CUDA execution was unavailable; the GPU visualization test was skipped."
    - "Downstream temporal-analysis and 3D-viewer migration/readiness were not authorized or established."
  assumptions:
    - "The public helper contract is configuration pass-through; it does not promise that its fixed synthetic workload will generate an E2 candidate."
    - "The deterministic real-growth test is an existing bounded downstream replay fixture using direct ExperimentRunner setup; its private setup installs only the initial topology, while the admitted edge is produced by the ACP-0007 runtime mechanism."
  unresolved:
    - "The broad suite remains non-green for the documented unrelated downstream failures."
    - "Temporal-analysis, 3D viewer, Luna-12L, spiral, and Luna-12E readiness remains unestablished."
  recommended_next_agent:
    - "Luna-0 / project owner: no successor is authorized by this closure; issue a separate bounded authorization if any downstream migration is wanted."
---

# Outcome

**PASS — LUNA-29 INDEPENDENTLY VERIFIED AND CLOSED FOR ITS AUTHORIZED
CPU-HELPER COMPATIBILITY SCOPE.** Review began at clean synchronized `main`,
with `HEAD == origin/main ==
6e1387967de2d1170d5743a38927afe08b9ddab8`. The reviewed Luna-29 implementation
is `252fa15073e983a793a06b0ba3c79c84ced84637`; its completion handoff was
published at the review baseline. The Luna-29 delta from its authorization
floor contains only the authorized helper, two owned test files, and
governance/handoff material. No production/test repair was made during this
review. The closure publication changes only this handoff, the Luna workflow,
and the architecture changelog.

The CPU helper accepts the existing `ExperimentConfig` as the source of
runner settings and uses its seed for synthetic workload generation. Omitted
scalar options remain distinguishable from explicit values; matching values
are accepted and conflicting values rejected. The no-config convenience
defaults remain unchanged. The supplied config was not mutated, capture
settings did not affect training output, and the helper's result matched a
direct `ExperimentRunner` run using the same config and workload.

## Public-helper / growth-fixture classification

- **SUPPORTED FOR CONFIGURATION PASS-THROUGH ONLY:** `run_cpu_training`
  forwards an explicitly valid E2 configuration and retains fixed-topology
  defaults.
- **NOT REQUIRED BY CONTRACT:** the fixed synthetic workload behind
  `run_cpu_training()` is not required to produce an admitted E2 edge. The
  Luna-29 objective and acceptance criteria require config pass-through plus
  a deterministic explicit growth fixture; they require TPCV-2 to show an
  addition when that fixture supplies before/after snapshots, not that the
  helper's default workload naturally creates a candidate.
- Consequently, no end-to-end public-helper growth claim is made. The replay
  fixture uses direct `ExperimentRunner` setup with a bounded explicit
  initial topology. That setup does not synthesize the admitted edge: the
  accepted runtime evidence/controller path produces the real growth
  decision, which is exposed through public `structural_decisions` and
  represented by adjacent TPCV-2 snapshots. This is valid downstream replay
  evidence for the stated acceptance contract, not proof that the helper's
  fixed workload grows.

## Independent evidence

**OBSERVED:** Repeated E2 fixture executions produced identical training
results, snapshots, structural decisions, candidate rank, and final topology.
The explicit candidate `neuron-0 -> neuron-2` at delay `0.4` was admitted
within finite topology capacity. Its addition appears in the TPCV-2
connection timeline against the supplied pre-growth topology. The E2
fixture reports no pruning, and its per-epoch topology does not lose edges.

**OBSERVED:** Capture enabled/disabled yielded equal training results,
structural decisions, and topology. Changing only the label while preserving
the temporal input yielded equal emission observations, candidates, selected
candidate/rank/status, before/after topology, and final topology. The fixed
control remained unchanged. Metric checks use
`event_count == processed_event_count` and
`activation_count == excursion_count`; the explicit `energy_weight=1.0`
fixture checks `utility == reward - energy` without asserting benefit.

**OBSERVED:** The old boolean-only E2 request continues to fail at explicit
structural-observation validation. The explicit TANH_LEGACY regression
continues to exercise its historical growth/pruning behavior separately;
generic replay still represents removed edges without implying E2 pruning.

**OBSERVED:** An independent Python 3.11.5 runtime probe confirmed that
non-default omitted E2 scalar options do not create false conflicts; the
exact supplied config and seed are used; config fields remain unchanged;
capture does not alter results; a representative legacy scalar call equals
its explicit-config counterpart; and the bare structural boolean remains
rejected.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_luna12b_integration.py` | Review baseline; Python 3.11.5 | 13 passed | Independent run |
| `python -m pytest -q tests/test_luna28_excursion_structural_growth.py` | Review baseline; Python 3.11.5 | 44 passed | Independent run |
| `python -m pytest -q tests/test_cpu_visualization.py tests/test_visualization.py` | Review baseline; Python 3.11.5 | 32 passed | Independent run |
| Combined Luna-12B, Luna-28, CPU visualization, and visualization tests | Review baseline; Python 3.11.5 | 89 passed | Independent run |
| `python -m pytest -q tests/test_experiments.py` | Review baseline; Python 3.11.5 | 12 passed | Independent run |
| `python -m pytest --collect-only -q` | Review baseline; Python 3.11.5 | 898 tests collected; no collection errors | Independent run |
| `python -m pytest -q -rs` | Review baseline; Python 3.11.5 | 880 passed, 17 failed, 1 skipped | Independent full suite and JUnit failure reconciliation |
| `python -m compileall -q tpcn tests` | Review baseline; Python 3.11.5 | Passed | Independent run |
| Pylance problems for `tpcn/cpu_visualization.py`, `tests/test_cpu_visualization.py`, and `tests/test_luna12b_integration.py` | Review workspace | No errors | Problems tool |
| `git diff --check aad4b0db09773ebca9314d188c3b24297ad17c44..HEAD` | Clean synchronized review baseline | Passed | Git |
| Read-only delta audit for full-suite failure sources | Authorization floor through review baseline | Failing runner/tests are unchanged in this Luna-29 delta | Git path audit |

### Full-suite reconciliation

All 17 failures were enumerated; none is in Luna-29's owned test files or
helper path:

- **2 Luna-12E legacy assertions:** routed activity changes event count but
  not the aggregate prediction-loss value (`1.1725` in both cases), and the
  neuron-identity/reset test observes timestamp `5.0` where the legacy
  assertion expects `0.0`. These are the previously documented stale
  downstream observables; their tests and runner source are unchanged by
  Luna-29.
- **8 Luna-12L temporal-scale tests, 1 spiral-benchmark test, 3
  temporal-analysis tests, and 3 3D-viewer tests:** each fails while
  constructing historical `EXCURSION_V1` structural-plasticity settings
  without the required ACP-0007 structural-observation configuration.
  These consumers are explicitly outside Luna-29 ownership and remain
  unmigrated.
- **1 GPU visualization test skipped:** CUDA is unavailable.

The full suite is therefore **not green** and must not be represented as
such. Its failures are not evidence of a Luna-29 regression: the failing
consumer tests and runtime configuration guard are outside and unchanged by
the Luna-29 delta, while all Luna-12B focused tests pass. No unrelated repair
was made.

## Architecture evidence and scope

| Clause / boundary | Review result |
|---|---|
| A01-A03 | Preserved: helper/capture are downstream wrappers; no global neural clock, batching semantics, or event timing change. |
| A04 | Preserved: the growth fixture uses explicit finite topology, fan-in/out, attempt, event, queue, and replay limits. |
| A05 | Preserved: no spatial-reservoir dependency introduced. |
| A06-A08 | Preserved: predictive coding/runtime learning are unchanged; structural evidence is emission-local and label-isolated; histories are bounded. |
| A09-A11 | Preserved: metric/energy reporting is observational; no calibrated energy, efficacy, or utility-benefit claim is made. |
| A12-A13 | Preserved: no pathway/gate choice is promoted to a mandatory invariant. |
| A14 | Preserved under accepted ACP-0007: explicit opt-in bounded growth only; E2 pruning remains unauthorized. |
| A15 | Preserved: CPU software reference only; hardware equivalence is untested and unclaimed. |

ACP-0007 remains **Accepted**. Architecture Contract 1.2 and A01-A15 are
unchanged. No architecture change or additional ACP is required for this
downstream adapter closure.

## Readiness, limitations, and next assignment

Luna-29 is closed for its authorized helper-compatibility and Luna-12B
focused-verification scope. This does not close or migrate Luna-12E, Luna-12L,
the spiral benchmark, temporal analysis, or the 3D viewer. Their readiness is
not established; their existing full-suite failures are recorded above.
There is no successor authorization. Luna-0 / the project owner must issue a
separate bounded authorization before any downstream migration or repair.

Rollback is limited to reverting the Luna-29 adapter/test migration at its
implementation boundary; this review made no code changes. The fixed-topology
default remains the safe ordinary path, and ACP-0007's explicit E2 validation
guard remains in force.
