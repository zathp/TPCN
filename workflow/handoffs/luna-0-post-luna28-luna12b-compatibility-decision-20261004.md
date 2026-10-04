# Luna-0 Post-Luna-28 Luna-12B Compatibility Decision

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "First downstream compatibility governance review after Luna-28"
  task_id: "luna-0-post-luna28-luna12b-compatibility-decision-20261004"
  component: "Luna-12B CPU persistent-topology and structural-plasticity visualization"
  status: "complete / Luna-29 authorized, not executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "c654ffe9c8d4a6d179781696d9ba5cd239e12795"
  result_revision: "governance publication pending"
  dependencies:
    - "Accepted ACP-0007"
    - "Luna-28 independent closure"
  owner: "Luna-0 Architecture Guardian"
  classification: ["GOVERNANCE", "LEGACY-CONTRACT RECONCILIATION", "DOWNSTREAM-MIGRATION CLASSIFICATION"]
  hypothesis: "Luna-12B can migrate its CPU helper and tests to explicit ACP-0007 growth-only E2 without pruning promotion or TPCV redesign."
  counter_hypothesis: "A missing explicit API, actual TPCV-2 representation defect, or unavoidable pruning requirement would block or redirect migration."
  interfaces_relied_on:
    - "run_cpu_training"
    - "ExperimentConfig and public ExperimentMetrics.structural_decisions"
    - "TPCV-2 snapshots and ReplaySequence.connection_timeline()"
  label_information_boundary:
    - "The migrated label-isolation test must compare public emission observations, candidate evidence/ranks/decisions and topology."
  timing_assumptions:
    - "No change to ACP-0007 emission timestamps, association window, or fixed growth delay."
  reset_boundaries:
    - "No change to character-local evidence or experiment topology persistence."
  resource_bounds:
    - "Explicit ExperimentConfig is required for E2 growth, including complete explicit neighborhoods and finite ACP-0007 bounds."
  authorized_scope:
    - "Governance-only review and bounded Luna-29 dispatch."
  unauthorized_scope:
    - "Implementation, tests, E2 pruning, TPCV codec changes, or any downstream migration beyond Luna-12B."
  controls:
    - "Four-test Luna-12B reproduction."
    - "Luna-28 focused suite."
    - "CPU visualization and TPCV-2 focused suites."
    - "Direct E2 metric and TANH_LEGACY compatibility probes."
  measurements:
    - "Luna-12B: 4 failed at one explicit E2 observation guard."
    - "Luna-28: 44 passed."
    - "CPU visualization and visualization: 30 passed."
    - "E2 sample metrics: 3 processed events and 1 excursion."
    - "TANH_LEGACY structural probe: 2 additions, 2 removals."
  information_boundary_check:
    - "No hidden-neighborhood profile authorized; wrapper forwards a supplied validated config."
  hardware_mapping:
    - "CPU reference only; no equivalence claim."
  architecture_invariants_touched: ["A01", "A04", "A06", "A07", "A08", "A10", "A14", "A15"]
  preserves:
    - "ACP-0007 growth-only E2, fixed topology default, and no E2 pruning."
    - "Generic replay removals and explicit TANH_LEGACY behavior."
    - "TPCV-2 schema and downstream-only capture."
  architecture_change: false
  proposal: "No ACP required for this downstream compatibility adapter."
  files_changed:
    - ".github/agents/luna-29.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md"
    - "workflow/handoffs/luna-0-post-luna28-luna12b-compatibility-decision-20261004.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing: []
  tests_failed:
    - "Four Luna-12B tests fail at the expected guard because they request structural_plasticity=True without ACP-0007 observation/policy/neighborhood/bounds."
  tests_not_run:
    - "Full suite; not needed for this bounded governance review."
  assumptions:
    - "Expected publication subject confirms baseline although pasted Git identifier is malformed."
  unresolved:
    - "CLI old boolean and downstream consumers are outside Luna-29."
    - "17 other known repository failures remain separate."
  recommended_next_agent:
    - "Luna-29, then Luna-0 independent review."
```

## Starting revision and Luna-28 state

The review began on `main`, clean, with
`HEAD == origin/main == c654ffe9c8d4a6d179781696d9ba5cd239e12795`,
subject `docs: close independent Luna-28 review`. The identifier in the
dispatch text did not resolve as a Git commit and is not used as provenance.

Luna-28 remains **CLOSED / INDEPENDENTLY VERIFIED** under accepted ACP-0007
and architecture contract 1.2. The implementation established the tested
path from canonical E2 emissions through bounded local observation and
character-local temporal evidence to quiescent growth and a later actual
routed E2 event. Fixed-topology E2 remains default. Growth is opt-in; E2
pruning and N3 remain unauthorized. Task efficacy and resource benefit remain
unestablished.

## Four-failure reproduction

Command:

```text
python -m pytest -q tests/test_luna12b_integration.py
```

Observed: **4 failed in 0.36s**. All four fail during
`ExperimentConfig.__post_init__` with:

```text
ValueError: structural plasticity is unavailable unless structural observation is enabled
```

The wrapper builds `ExperimentConfig(... structural_plasticity=True)` without
`structural_observation=True`, `structural_policy="e2_local_temporal"`, an
explicit complete `structural_neighbors` map, or the finite ACP-0007 bounds.
This is the intended E2 guard, not a Luna-28 core defect:

1. `test_structural_run_is_deterministic_and_has_real_bounded_mutations`
2. `test_capture_is_downstream_only_for_structural_decisions`
3. `test_controls_report_behavior_and_topology_without_assuming_benefit`
4. `test_structural_evidence_is_label_isolated`

Before authorization, Luna-28 focused tests passed (**44 passed**),
CPU-visualization plus visualization/TPCV tests passed (**30 passed**), and a
direct E2 metric fixture observed `event_count == processed_event_count == 3`
while `activation_count == excursion_count == 1`. An explicit
`TANH_LEGACY` structural probe completed four epochs with two additions, two
removals, bounded history and bounded topology.

## Assertion-by-assertion matrix

| Test | Assertion | Historical meaning | Classification | Disposition | Replacement evidence | Architecture change? | Owner |
|---|---|---|---|---|---|---|---|
| Deterministic bounded mutations | Same-seed `TrainingResult` equal | Replayable computation and topology | VALID DOWNSTREAM VISUALIZATION INVARIANT | Keep | Repeat exact explicit config, input and seed | No | Luna-29 |
| Deterministic bounded mutations | Same-seed snapshots equal | Deterministic downstream capture | VALID DOWNSTREAM VISUALIZATION INVARIANT | Keep | Compare TPCV-2 records | No | Luna-29 |
| Deterministic bounded mutations | At least one accepted addition | Demonstrate real structural growth | CURRENT ACP-0007 E2 INVARIANT as a deterministic mechanism fixture, not a universal workload promise | Replace | Use explicit E2 fixture; assert an admitted growth and decision | No | Luna-29 |
| Deterministic bounded mutations | At least one pruned connection | General historical grow/prune adaptation | HISTORICAL PRE-ACP-0007 ASSERTION; REQUIRES FUTURE PRUNING CONTRACT for E2 | Retag / remove from E2 | Separate explicit TANH_LEGACY regression; no E2 prune requirement | Yes for future E2 pruning | Luna-29; future pruning owner is Luna-0/project owner |
| Deterministic bounded mutations | Connection count <= capacity | Finite topology | CURRENT ACP-0007 E2 INVARIANT | Keep | Check every E2 history row | No | Luna-29 |
| Deterministic bounded mutations | Fan-in utilization <= 1 | Legal bounded topology | CURRENT ACP-0007 E2 INVARIANT | Keep | Check every E2 history row | No | Luna-29 |
| Deterministic bounded mutations | Fan-out utilization <= 1 | Legal bounded topology | CURRENT ACP-0007 E2 INVARIANT | Keep | Check every E2 history row | No | Luna-29 |
| Deterministic bounded mutations | Mutation history <= 32 | Bounded observability state | CURRENT ACP-0007 E2 INVARIANT | Keep | Check configured history limit | No | Luna-29 |
| Capture downstream-only | Capture-off result equals capture-on | Capture cannot affect computation/decisions | VALID DOWNSTREAM VISUALIZATION INVARIANT | Keep | Compare complete `TrainingResult`, including structural decisions | No | Luna-29 |
| Capture downstream-only | Capture-off stores no snapshots | Disabled collector is inert | VALID DOWNSTREAM VISUALIZATION INVARIANT | Keep | Assert empty snapshot tuple | No | Luna-29 |
| Capture downstream-only | Replay shows added connections | Display topology growth across snapshots | VALID DOWNSTREAM VISUALIZATION INVARIANT | Keep / replace | Use TPCV-2 connection timeline for a real deterministic E2 addition | No | Luna-29 |
| Capture downstream-only | Replay shows recently pruned connections | Old E2 replay requires removal | HISTORICAL PRE-ACP-0007 ASSERTION; REQUIRES FUTURE PRUNING CONTRACT for E2 | Retag / remove from E2 | Keep generic edge-removal replay coverage and explicit TANH regression; do not demand E2 prune | Yes for future E2 pruning | Luna-29; future pruning owner is Luna-0/project owner |
| Controls | Fixed topology retains connection count | Fixed matched control | CURRENT ACP-0007 E2 INVARIANT for the fixed-topology control | Keep | Compare first/last fixed E2 topology counts | No | Luna-29 |
| Controls | Structural mutation count observed | Show enabled structural mechanism ran | VALID DOWNSTREAM VISUALIZATION INVARIANT; not efficacy | Replace | Assert observation/candidate/attempt/admission fields and decisions | No | Luna-29 |
| Controls | Learning-disabled control has zero parameter updates | Isolate outer readout learning | VALID DOWNSTREAM VISUALIZATION INVARIANT | Keep | Existing `parameter_updates == 0` oracle | No | Luna-29 |
| Controls | `event_count == activation_count` for all modes | Legacy treated each event as activation | STALE TEST EXPECTATION for E2 metric semantics | Replace | Assert `event_count == processed_event_count` and `activation_count == excursion_count` | No | Luna-29 |
| Controls | Energy >= 0 | Nonnegative diagnostic resource proxy | VALID DOWNSTREAM VISUALIZATION INVARIANT | Keep | Preserve; label units as uncalibrated proxy | No | Luna-29 |
| Controls | Utility == reward - energy | Net utility at default energy weight | VALID DOWNSTREAM VISUALIZATION INVARIANT only with `energy_weight=1.0` | Keep with explicit config | Assert formula only under that stated setting | No | Luna-29 |
| Label isolation | Mutation history unchanged after label mutation | Labels do not change structural outcome | CURRENT ACP-0007 E2 INVARIANT | Replace | Compare full public structural decisions/evidence and final topology across relabeling | No | Luna-29 |
| TANH_LEGACY compatibility | Historical growth and pruning still execute when explicitly selected | Preserve pre-E2 reference behavior | TANH_LEGACY-ONLY REGRESSION | Keep separately | Explicit legacy config yields historical additions/removals with bounds | No | Luna-29 |

## Core decisions

### Growth and pruning

An accepted addition remains appropriate as a deterministic mechanism
acceptance fixture. It is not a claim that every dataset/configuration must
grow, nor evidence of task benefit. Capacity, fan-in/out and finite history
assertions remain applicable.

The old `pruned_connections > 0` and E2 recently-pruned timeline requirements
are historical pre-ACP-0007 assertions. E2 migration must not satisfy them by
enabling `prune()`, `prune_by_score()`, edge-retention utility or replacement.
The legacy behavior should remain separately exercised under explicit
`TANH_LEGACY`; generic snapshot replay continues to represent edge removals.
No pruning ambiguity blocks a growth-only migration.

### CPU helper API

Decision: **Option A**, with an explicit public pass-through:

```text
run_cpu_training(..., experiment_config: ExperimentConfig | None = None)
```

The supplied `ExperimentConfig` is the source of truth for the runner, and
its seed drives synthetic workload construction. Duplicate/conflicting
runner settings must be rejected, not silently ignored. Capture frequency,
snapshot capacity and workload-size parameters remain helper-level options.
When no config is supplied, existing scalar convenience behavior and defaults
remain; `structural_plasticity=True` alone continues to raise the existing
explicit E2 guard. No profile, implicit all-to-all topology, or new
`structural_config` abstraction is authorized.

No TPCV change is needed. TPCV-2 preserves canonical connection records, and
the existing connection timeline reports adjacent-snapshot additions and
removals. Capture remains downstream-only. The current E2 result already
exposes `structural_decisions`, including observations, candidates, selected
candidate/rank/status and before/after topology, so label isolation should use
that stronger evidence plus final topology rather than mutation history alone.

TANH_LEGACY explicit historical growth/pruning is preserved. It is never
selected as a default or substituted for E2.

## Downstream classification and architecture audit

- **Temporal analysis:** Luna-12B's explicit helper API is a **prerequisite**
  for later consumers that use its old structural boolean. Their own call
  sites and assertions still need a separate migration; not authorized here.
- **3D viewer:** Luna-12B's explicit helper API is a **prerequisite** for the
  current snapshot-construction setup, but viewer migration remains separately
  gated.
- **Luna-12L:** separate. Its baseline/random/temporal/reversed E2 policies
  conflict with ACP-0007's only accepted E2 policy.
- **Spiral:** separate structural policy/configuration decision; not included.
- **Luna-12E:** two stale assertions remain classified separately and are
  untouched.
- **CLI:** the old structural boolean CLI surface is outside Luna-29; it is
  not permitted to invent ACP-0007 settings and remains an explicit
  compatibility limitation.

| Clause | Assessment |
|---|---|
| A01 | Capture remains at existing epoch boundaries; no clock, event ordering or backpressure changes. |
| A04 | Existing bounded topology and finite metrics/history remain; snapshots represent the actual topology. |
| A06 | Prediction/error semantics are unchanged and no efficacy is required. |
| A07 | Caller supplies explicit local evidence configuration; labels and capture do not feed the scorer. |
| A08 | Existing runtime, queue, event, history and snapshot limits remain. |
| A10 | Energy remains diagnostic; no energy-minimization objective or benefit assertion. |
| A14 | Accepted opt-in local growth only; E2 pruning remains unauthorized. |
| A15 | CPU software reference only; no hardware-equivalence claim. |

**ACP required? No. Luna-29 authorized? Yes, limited to the existing accepted
contract.** Exact ownership and stop conditions are in
`.github/agents/luna-29.agent.md` and
`workflow/handoffs/luna-0-authorization-luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md`.
Luna-29 is not executed by this review.

## Remaining suite failures and terminal disposition

The last full repository run remains **865 passed, 21 failed, 1 skipped, 887
collected**. The four Luna-12B failures are the only target here. The other
17 remain separate: Luna-12E (2), Luna-12L (8), spiral benchmark (1), temporal
analysis (3), and 3D viewer (3).

**PASS — LUNA-12B POST-ACP-0007 COMPATIBILITY CLASSIFIED; LUNA-29 AUTHORIZED /
NOT EXECUTED.** No production code or test was changed in this governance
invocation. No pruning was enabled, no codec change is needed, and no other
downstream migration is authorized.
