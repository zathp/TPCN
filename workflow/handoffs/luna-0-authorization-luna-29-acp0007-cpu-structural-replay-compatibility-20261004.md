# Luna-0 Authorization Handoff — Luna-29 ACP-0007 CPU Structural Replay Compatibility

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Authorization for Luna-12B CPU compatibility with ACP-0007 growth-only replay"
  task_id: "luna-29-acp0007-cpu-structural-replay-compatibility-20261004"
  component: "CPU training helper and Luna-12B TPCV-2 structural replay tests"
  status: "authorized / not started"
  contract_version: "1.2"
  branch: "main"
  base_revision: "c654ffe9c8d4a6d179781696d9ba5cd239e12795"
  authorization_source_revision: "F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb (opaque source token; not a Git object)"
  verified_review_revision: "c654ffe9c8d4a6d179781696d9ba5cd239e12795"
  authorization_publication_revision: "aad4b0db09773ebca9314d188c3b24297ad17c44"
  execution_lineage_floor: "aad4b0db09773ebca9314d188c3b24297ad17c44"
  result_revision: "not started"
  dependencies:
    - "Accepted ACP-0007"
    - "Luna-28 independent closure at 028b5793917efb2c1af279691d1611427de3a86c"
    - "This Luna-0 compatibility decision"
  owner: "Luna-29"
  classification: ["IMPLEMENTATION", "INTEGRATION", "FOCUSED VERIFICATION"]
  hypothesis: "The Luna-12B CPU wrapper and assertions can represent explicit ACP-0007 growth-only E2 without changing the core or TPCV schema."
  counter_hypothesis: "If explicit configuration cannot produce deterministic downstream TPCV-2 growth evidence within the owned wrapper/tests, stop and return to Luna-0."
  interfaces_relied_on:
    - "ExperimentConfig and ExperimentRunner public APIs"
    - "run_cpu_training and CPUTrainingCapture"
    - "ReplaySequence.connection_timeline()"
    - "Public ExperimentMetrics.structural_decisions"
    - "TPCV-2 canonical connection records"
  label_information_boundary:
    - "Labels and task outcomes remain excluded from local structural evidence."
    - "Label-mutation verification compares observations, candidates, ranking, decisions and resulting topology."
  timing_assumptions:
    - "ACP-0007 canonical emission timestamp and fixed configured growth delay semantics remain unchanged."
    - "Capture occurs at existing epoch boundaries and is downstream-only."
  reset_boundaries:
    - "No change to character, experiment or topology reset/persistence semantics."
  resource_bounds:
    - "Use all explicit finite ACP-0007 observation/evidence/attempt limits from the supplied ExperimentConfig."
    - "Preserve bounded snapshots, metrics, topology and mutation histories."
  authorized_scope:
    - "Add explicit ExperimentConfig pass-through to the CPU helper with conflict validation."
    - "Migrate only Luna-12B CPU structural integration and directly related CPU capture tests."
    - "Preserve growth-only E2, fixed topology, generic removal replay and explicit TANH_LEGACY historical behavior."
  unauthorized_scope:
    - "E2 pruning, replacement, or edge-retention learning."
    - "Production experiment/runtime/topology/controller or observation-plane changes."
    - "TPCV schema/codec changes."
    - "CPU CLI migration in this assignment."
    - "Temporal-analysis, 3D-viewer, Luna-12L, spiral, or Luna-12E migration."
    - "GPU/FPGA/FPAA/hardware-equivalence work or efficacy claims."
  controls:
    - "Fixed-topology matched control."
    - "Capture disabled versus enabled."
    - "Deterministic explicit E2 topology/configuration."
    - "Label mutation."
    - "Explicit TANH_LEGACY structural regression."
  measurements:
    - "Starting suite reproduction: four failures at the explicit missing-observation E2 guard."
    - "Before authorization, Luna-28 tests: 44 passed; CPU visualization plus TPCV tests: 30 passed."
    - "Before authorization, E2 metric probe: event_count=processed_event_count=3; activation_count=excursion_count=1."
    - "Before authorization, explicit TANH_LEGACY probe: 2 additions and 2 removals, with bounded history/topology."
  information_boundary_check:
    - "The wrapper forwards caller-supplied validated ExperimentConfig; it must not invent or hide structural_neighbors."
    - "Capture/replay may observe topology but cannot generate structural evidence or affect decisions."
  hardware_mapping:
    - "CPU software reference only; no hardware validation authorized."
  architecture_invariants_touched: ["A01", "A04", "A06", "A07", "A08", "A10", "A14", "A15"]
  preserves:
    - "ACP-0007 accepted growth-only semantics and E2 fixed-topology default."
    - "A01-A15 and Architecture Contract 1.2."
    - "TANH_LEGACY explicit compatibility and generic snapshot edge removal replay."
  architecture_change: false
  proposal: "None required; implementation is a downstream adapter to accepted ACP-0007. Any scope expansion requires a new decision."
  files_changed: []
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "Luna-29 tests are not run; authorization only."
    - "Full suite and unrelated downstream migrations are not required at this stage."
  assumptions:
    - "The requested revision token is malformed/non-Git; clean main and expected commit subject verify baseline c654ffe9c8d4a6d179781696d9ba5cd239e12795."
    - "TPCV-2's existing connection records and adjacent-snapshot replay are sufficient."
  unresolved:
    - "The historical CPU CLI boolean remains outside Luna-29 and is not converted to an implicit E2 profile."
    - "Temporal-analysis, 3D-viewer, Luna-12L, spiral and Luna-12E remain separately gated."
    - "Task efficacy and resource benefit remain unestablished."
  recommended_next_agent:
    - "Luna-29, then return to Luna-0 for independent review."
```

## Decision

**AUTHORIZED — LUNA-29 IMPLEMENTATION + FOCUSED VERIFICATION ONLY; NOT
STARTED.** Luna-29 may adapt the CPU training helper to accept an explicit
`ExperimentConfig` and migrate the Luna-12B compatibility tests to ACP-0007
growth-only E2 semantics under
`.github/agents/luna-29.agent.md`.

The supplied source token
`F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` is not a Git object and must
not be used as repository provenance or an execution baseline. Luna-0's
verified review revision was clean `main` at
`c654ffe9c8d4a6d179781696d9ba5cd239e12795`, subject
`docs: close independent Luna-28 review`.

The executable Luna-29 authorization package was first published at
`aad4b0db09773ebca9314d188c3b24297ad17c44`
(`docs: authorize Luna-29 CPU replay compatibility`). That revision is the
authorization publication revision and execution-lineage floor. Luna-29 must
run from clean, synchronized `main` descending from that floor, allowing only
governance-only clarifications/pinning for this authorization between the
floor and execution. A later production, test, ACP, contract, or architecture
semantics change requires stopping and returning to Luna-0.

## Contract reconciliation

ACP-0007 is accepted; architecture contract version 1.2 is unchanged; Luna-28
is closed. This assignment is only an adapter to already-authorized E2
growth-only behavior. No ACP is required. `run_cpu_training(structural_plasticity=True)`
without an explicit `ExperimentConfig` remains invalid for E2; it must not
silently create a policy, local-neighborhood map, or bounds. With a supplied
config, that config is the source of truth; conflicting duplicate runner
settings must fail explicitly. The fixed-topology default remains.

E2 pruning remains **NOT AUTHORIZED**. The historical addition/removal
expectation may be kept only in a separate explicit `TANH_LEGACY` regression.
Generic replay continues to represent edge-set additions and removals, but
TPCV snapshots do not prove why an edge disappeared. TPCV-2 connection records
and `ReplaySequence.connection_timeline()` already represent an edge absent
in one snapshot and present in the next; no codec/schema change is needed.

## Exact Luna-29 scope

Owned files:

- `tpcn/cpu_visualization.py`
- `tests/test_luna12b_integration.py`
- `tests/test_cpu_visualization.py`
- `workflow/handoffs/luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md`

No production experiment/runtime/configuration, topology/controller,
observation, replay codec, CPU CLI, temporal-analysis, 3D-viewer, Luna-12L,
spiral, or Luna-12E changes are authorized. The exact objective, API contract,
tests, stop conditions, and exclusions are in `.github/agents/luna-29.agent.md`.

## Required sequence and stop conditions

`Luna-0 -> Luna-29 -> Luna-0`. Luna-29 must stop and return if the accepted
growth mechanism cannot be represented in the owned helper/tests or if
production/core or TPCV codec changes appear necessary. No pruning, successor,
or downstream migration is authorized by completing Luna-29.

This authorization does not execute the assignment and does not establish
task efficacy, resource benefit, downstream integration readiness, or
hardware equivalence.

Luna-29 may execute from clean synchronized `main` descending from
`aad4b0db09773ebca9314d188c3b24297ad17c44`; the governance-only correction
and any other governance-only clarification/pinning for this authorization
are allowed descendants. Any intervening production, test, ACP, contract, or
architecture-semantics change requires stopping and returning to Luna-0.
