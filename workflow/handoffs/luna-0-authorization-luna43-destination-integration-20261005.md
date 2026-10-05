---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-43 destination integration mechanism authorization"
  task_id: "luna-0-authorization-luna43-destination-integration-20261005"
  component: "ACP-0008 fixed-topology downstream destination integration"
  status: "complete"
  contract_version: "1.2"
  branch: "copilot/execute-luna-43-cycle"
  base_revision: "b6ca4a67783bf37ded146944f8dc9afaf5277f11"
  result_revision: "the commit publishing this authorization"
  dependencies:
    - "Project-owner direction in the current task"
    - "Luna-42 execution and independent post-Luna-42 review"
    - "Accepted experimental ACP-0008"
    - "Accepted ACP-0007, unchanged"
  owner: "Project owner"
  classification:
    - "governance-only authorization"
    - "bounded mechanism experiment"
    - "Luna-43 AUTHORIZED / NOT EXECUTED"
  hypothesis: "With a frozen ACP-0008-calibrated relay, destination integration configuration may change downstream destination state/emissions on the reviewed fixed two-hop stream."
  counter_hypothesis: "Disabled, default, and calibrated destination conditions yield no distinct destination behavior, or causal/runtime/replay checks fail."
  interfaces_relied_on:
    - "MultiExcursionNeuron and per-neuron E1Config.integration"
    - "IntegrationConfig(decay_rate_z=...)"
    - "ExcursionCharacterRuntime"
    - "BoundedTopology and immutable Edge / ordinary Model-B transfer"
  label_information_boundary:
    - "Only ordered points/times enter the neural runtime; labels/classes are not read."
    - "No task, classification, accuracy, prediction, reward, or efficacy endpoint."
  timing_assumptions:
    - "Exact Luna-42 Phase-B point streams, timestamps, route delay, and settling horizon."
    - "Both ordinary edge delays remain 1.0; no global neural timestep."
  reset_boundaries:
    - "Fresh per-character source, relay, destination, runtime queue, and local state."
    - "No topology mutation or cross-character neural state."
  resource_bounds:
    - "Luna-42 Phase-B bounds frozen: queue 128; runtime event/activity budgets 1024; neuron event budget 4096."
    - "Prediction capacity 8 / expiry 4.0; eligibility capacity 1024 per ledger; settling horizon 4.0."
    - "Three nodes; fan-in/out 2; edge/routing capacity 3; exactly two fixed edges."
  authorized_scope:
    - "Compare destination integration disabled, default, and calibrated at decay_rate_z=0.0125."
    - "Hold relay at calibrated decay_rate_z=0.0125 in every arm."
    - "Reuse matched Luna-42 Phase-B streams, seeds, sequence ordering, and runtime bounds."
    - "Create only Luna-43-owned runner, focused tests, artifacts, and execution handoff."
  unauthorized_scope:
    - "No execution during this Luna-0 authorization pass."
    - "No Luna-40/41/42 runner execution, repair, or artifact/historical-outcome changes."
    - "No production/API, topology, parameter, ACP, architecture, or prior-test changes."
    - "No shortcut edge, ACP-0007 growth, efficacy/task metric, energy benefit, promotion, hardware claim, or Luna-44 authorization."
  controls:
    - "DESTINATION_DISABLED: integration=None"
    - "DESTINATION_DEFAULT: IntegrationConfig() with decay_rate_z=0.1"
    - "DESTINATION_CALIBRATED: IntegrationConfig(decay_rate_z=0.0125)"
    - "Identical fixed source->relay->destination topology; both edges w=1, d=1, r=0, delay=1.0."
  measurements:
    - "Input digests and exact source/relay/destination configurations."
    - "Source emissions, relay emissions, ordinary transfers/receptions, destination integration traces and direct/integrated emissions."
    - "Identity, ordering, route, timestamp, payload, state-bound, resource, settling, and deterministic-replay checks."
  information_boundary_check:
    - "No labels, classes, task outcomes, or evaluation records feed neural inputs or condition selection."
  hardware_mapping:
    - "Not run; software-reference mechanism experiment only; no equivalence claim."
  architecture_invariants_touched:
    - "A01/A03: event-driven causal finite-delay routing."
    - "A04: finite fixed topology and resource bounds."
    - "A07/A08: local bounded ACP-0008 state; no global/task input."
    - "A14: structural adaptation remains disabled."
  preserves:
    - "ACP-0008 remains experimental, opt-in, and unpromoted."
    - "ACP-0007 remains unchanged and disabled."
    - "Luna-41 remains historically BLOCKED."
    - "Luna-42 and its independent review remain unchanged."
    - "The prior test-comparison authorization is retained as history but superseded before execution."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-43.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna43-destination-integration-20261005.md"
    - "workflow/handoffs/luna-0-authorization-luna43-test-comparison-policy-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Baseline full suite: 1019 passed, 4 target-test failures, 1 CUDA-unavailable skip; 1024 collected."
    - "Focused API/runtime regression selection: 217 passed."
  tests_failed:
    - "Four known exact-comparison assertions in Luna-41/Luna-42 tests compare computed 0.39999999999999997 with literal 0.4."
  tests_not_run:
    - "Luna-43 experiment, runner, and artifacts: not run/not created."
    - "Hardware validation: not applicable."
  assumptions:
    - "The four baseline assertion failures are the known ACP-0008 nominal-float comparison issue; no unrelated failure was observed."
    - "Current explicit project-owner direction supersedes the earlier no-successor review and mistaken test-only Luna-43 assignment."
  unresolved:
    - "Luna-43 execution and independent post-execution Luna-0 review remain outstanding."
  recommended_next_agent:
    - "Luna-43 for the exact bounded mechanism experiment; return to Luna-0 for independent review."
---

# Luna-0 authorization — Luna-43 destination integration mechanism

## Decision

**Luna-43 is AUTHORIZED / NOT EXECUTED** only for the destination-integration
mechanism experiment specified in `.github/agents/luna-43.agent.md`. The current
project-owner direction explicitly starts a new authorization cycle after the
independent Luna-42 review. It therefore supersedes that review's then-current
"no Luna-43 authorized" disposition.

The earlier publication `b495da7ddfe264b33adbb93690543b6c73a31b08` mistakenly
authorized only a test-comparison correction under the same Luna identifier.
That test-only assignment is superseded before execution; do not execute it.
Its handoff is retained as history and amended with this supersession notice.
This authorization does not authorize Luna-44.

## Evidence and interface assessment

The repository's actual governance root is `workflow/`; the profile path
`tpcn-luna-workflow/` is absent. Reviewed the contract, changelog, workflow,
acceptance criteria, ACP template/README, Luna handoff template, ACP-0007,
ACP-0008, Luna-40/41/42 handoffs, Luna-42 executor contract/runner/results,
the independent post-Luna-42 review, and relevant neuron/runtime/topology code.
Raw Luna-42 artifacts were inspected rather than relying only on its review.

**OBSERVED:** The production API cleanly supports the requested conditions.
`E1Config.integration` is per neuron; `IntegrationConfig()` provides the
default `decay_rate_z=0.1`, and `IntegrationConfig(decay_rate_z=0.0125)` is
valid for the reviewed fast `decay_rate=1.0`. The Luna-42 Phase-B runner already
constructs the ordinary fixed topology with only `source -> relay` and
`relay -> destination`, both delay 1.0 and Model-B `w=1`, `d=1`, `r=0`; it
creates per-character `MultiExcursionNeuron`s and runs them through
`ExcursionCharacterRuntime`. Setting only destination `integration` per arm
while holding relay calibrated is expressible without a production change.
The fixed two-edge topology excludes a direct source-to-destination shortcut.
The runtime does not enable structural plasticity; the experiment contract
explicitly prohibits growth and uses no structural controller.

**OBSERVED:** Luna-42's Phase-B protocol used five seeds, 64 sequences per seed,
matched point streams, fresh character state, and the capacities listed in this
handoff. It read points rather than labels. It recorded 235 calibrated relay
integration-mediated emissions and 235 onward transfers/receptions in the
calibrated arm, with no destination emissions because destination integration
was disabled in all Phase-B arms. Thus there is a concrete routed stream for
the downstream destination comparison. This does not predetermine a destination
emission or a positive result.

**PRESERVED:** Luna-41 remains BLOCKED; Luna-42 remains independently reviewed;
ACP-0007 remains unchanged and disabled; ACP-0008 remains experimental,
opt-in, and unpromoted. No A01-A15 clause or ACP changes. This is a mechanism
experiment, not task efficacy, architecture promotion, or hardware validation.

## Baseline validation

The starting code/test revision was the clean `b6ca4a67783bf37ded146944f8dc9afaf5277f11`,
equal to fetched `origin/main`. The earlier baseline run used Python 3.12.3,
pytest 9.1.1, NumPy 2.5.3, SciPy 1.18.1, and PyTorch 2.14.1. The full command
was `python -m pytest -q -rs`: **1019 passed, 4 failed, 1 skipped; 1024
collected**. The only skip was the CUDA-unavailable GPU visualization test.
All four failures were the already identified exact equality assertions in
`tests/test_luna41_acp0008_temporal_calibration.py` and
`tests/test_luna42_acp0008_corrective_calibration.py`, comparing computed
`0.39999999999999997` to decimal `0.4`. No unrelated failure was observed.
These are recorded, not repaired, by this authorization.

The additional API/runtime/routing baseline selection was run with:

```text
python -m pytest -q tests/test_excursion_neuron.py tests/test_excursion_integration.py tests/test_e2_multi_excursion.py tests/test_topology.py tests/test_event_runtime.py tests/test_luna38_excursion_integration_state.py tests/test_luna39_acp0008_propagation_emission_diagnostic.py tests/test_luna41_acp0008_temporal_calibration.py tests/test_luna42_acp0008_corrective_calibration.py
```

Result: **217 passed, 4 failed** in 9.31 seconds. The same four known float
assertions were the only failures; all other selected ACP-0008, neuron, runtime
and routing tests passed. The full-suite baseline result above was recorded on
the clean starting revision; the additional focused selection was rerun with no
source/test changes (the intervening commit was governance-only).

`git diff --check` passed on the original clean baseline. Final governance
changes must also pass `git diff --check` before publication. No calibration
runner was executed and no experiment artifacts were created.

## Validation and readiness

| Check | Status | Evidence |
|---|---|---|
| Production API supports exact three-condition configuration | **Passed** | Per-neuron E1 integration config, existing Phase-B runner, runtime and fixed topology reviewed |
| No direct shortcut; ordinary fixed `w=1` hops | **Passed** | Two explicit edges in `_phase_b_topology()` |
| Growth disabled / ACP-0007 unchanged | **Passed** | Fixed topology/runtime path; ACP-0007 remains disabled |
| ACP-0008 status | **Preserved** | Experimental, opt-in, unpromoted |
| Relevant/full baseline tests | **Passed with known target failures** | Counts above; no unrelated failures |
| Luna-43 runner/experiment/artifacts | **Not run** | Explicitly excluded from authorization pass |
| Hardware equivalence | **Not applicable / not run** | No hardware claim |

This is authorization readiness only, not integration readiness. No architecture
change or ACP is required. No accuracy threshold is introduced.

## Next bounded assignment

Luna-43 owns only its runner, focused tests, artifacts, and completed execution
handoff. It must keep the relay fixed at calibrated `0.0125`, vary only the
destination among disabled/default/calibrated, preserve the reviewed fixed
two-hop topology and every other parameter, and report mechanism outcomes
without task-efficacy claims. The next step after its handoff is an independent
Luna-0 review; no further Luna is authorized.
