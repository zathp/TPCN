---
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Post-Luna-30 Luna-12E EXCURSION_V1 observable compatibility decision"
  task_id: "luna-0-post-luna30-luna12e-e2-observable-decision-20261004"
  component: "Luna-12E integration-test compatibility and governance"
  status: "complete"
  contract_version: "1.2"
  branch: "main"
  base_revision: "8d5f7f5ad1c594df3cd886de327eb14c3dfbe15c"
  result_revision: "main"
  dependencies:
    - "Luna-28 closed / independently verified"
    - "Luna-29 closed / independently verified"
    - "Luna-30 closed / independently verified"
    - "ACP-0007 accepted"
  owner: "Luna-0"
  classification:
    - "GOVERNANCE"
    - "VERIFICATION"
    - "TEST-ONLY COMPATIBILITY CLASSIFICATION"
  hypothesis: "Both remaining Luna-12E failures are stale legacy observables; current public EXCURSION_V1 routed metrics and terminal reset state can test the intended properties without production changes."
  counter_hypothesis: "A current public observable is unavailable or runtime terminal state contradicts the accepted EXCURSION_V1 lifecycle."
  interfaces_relied_on:
    - "ExperimentRunner.evaluate and last_neurons"
    - "EvaluationResult.event_trace and public ExperimentMetrics"
    - "MultiExcursionNeuron.clock, state, mode, and pending_event"
  label_information_boundary:
    - "No label flow or runtime data path changed."
    - "No label or future-point leakage was introduced."
  timing_assumptions:
    - "Event-local E2 time; no required global neural clock."
    - "Fixture external timestamps are 0.0 and 1.0."
    - "Configured settling_horizon is 4.0."
  reset_boundaries:
    - "End-character settles through last_external_timestamp + settling_horizon."
    - "Character destruction resets state at that horizon."
    - "The test observes post-evaluation terminal reset state, not the instant before the next input."
  resource_bounds:
    - "No runtime or resource configuration changed."
    - "The existing finite E2/event and settling limits remain in force."
  authorized_scope:
    - "Reproduce two named Luna-12E failures."
    - "Probe current causal-routing and public reset observables."
    - "Publish Luna-31 test-only authorization if both failures are stale-oracle issues."
  unauthorized_scope:
    - "Production code, tests, E2 runtime, prediction, routing, reset semantics."
    - "Luna-12L or spiral fixes."
    - "ACP, Architecture Contract 1.2, or A01-A15 changes."
    - "Executing Luna-31."
  controls:
    - "No-edge versus a single neuron-0 -> neuron-1 edge."
    - "Default EXCURSION_V1 compared to an explicit TANH_LEGACY reset probe."
    - "Repeated evaluation with identity comparison."
  measurements:
    - "Event count: 12 without edge; 14 with edge."
    - "Edge-transfer proxy: 0 without edge; 1.358357398350786 with edge."
    - "Maximum route depth: 0 without edge; 1 with edge."
    - "Prediction loss: 1.1724999999999999 in both conditions."
    - "EXCURSION_V1 terminal clocks: 5.0 for both neurons."
    - "EXCURSION_V1 terminal state/mode: neutral state 0.0, mode N; no pending event."
  information_boundary_check:
    - "No neural inputs or labels changed; downstream evaluation remains unchanged."
  hardware_mapping:
    - "Software-reference test observables only; no hardware execution or equivalence claim."
  architecture_invariants_touched:
    - "A01/A02: local event time and character-local horizon preserved."
    - "A03/A04: delayed finite routed-edge evidence observed."
    - "A06: prediction semantics unchanged; no loss delta required."
    - "A07: no global learning input or leakage change."
    - "A08: existing finite event/settling bounds unchanged."
    - "A15: software reference only."
  preserves:
    - "Architecture Contract 1.2 and A01-A15."
    - "Accepted ACP-0007; fixed-topology EXCURSION_V1 default."
    - "Luna-28/29/30 closed status."
    - "Historical general-topology Luna-12E component regressions."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-31.agent.md"
    - "workflow/handoffs/luna-0-post-luna30-luna12e-e2-observable-decision-20261004.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Causal-routing diagnostic probe: no-edge/no-route, edge route, 12->14 events, edge cost 0->1.358357398350786, depth 0->1."
    - "Reset diagnostic probe: identity stable, both final clocks 5.0, state 0.0, mode N, no pending work."
    - "Explicit TANH_LEGACY probe: identity stable and terminal clocks [0.0, 1.0]."
  tests_failed:
    - "The two requested stale-oracle Luna-12E tests were reproduced failing at prediction-loss inequality and old terminal-clock expectation."
  tests_not_run:
    - "Full test suite; prior independently verified baseline remains 896 passed, 11 failed, 1 skipped, 908 collected."
    - "Full Luna-12E suite and unrelated integration regressions."
  assumptions:
    - "The verified live origin/main closure commit is the intended baseline despite an unresolvable opaque revision token in the pasted request."
  unresolved:
    - "Luna-31 implementation and completion review remain pending."
    - "After Luna-31, the previously observed 8 Luna-12L and 1 spiral failures remain out of scope."
  recommended_next_agent:
    - "Luna-31 — Luna-12E EXCURSION_V1 Observable Compatibility Correction (authorized, not executed)"
---

# Outcome and scope

**PASS — LUNA-12E EXCURSION_V1 OBSERVABLE COMPATIBILITY CLASSIFIED;
LUNA-31 AUTHORIZED / NOT EXECUTED.**

This is a governance and verification-only decision. No production code or
test files were edited; Luna-31 itself was not executed. The only source of
truth for architecture remains the contract; this test-oracle correction
requires no ACP and makes no architecture promotion.

## Baseline and Luna-30 closure verification

At start, `main` was clean and synchronized:

```text
HEAD == origin/main
8d5f7f5ad1c594df3cd886de327eb14c3dfbe15c
docs: close Luna-30 replay consumer compatibility
```

The source request supplied
`F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` as an exact revision. Git
could not resolve that string. The live remote branch nevertheless matched
the expected Luna-30 closure subject and the verified closure revision above;
work proceeded from that actual synchronized commit. The current verification
confirmed the branch, commit subject, remote equality, and clean initial
worktree. Luna-28, Luna-29, and Luna-30 remain closed/independently verified;
ACP-0007 remains accepted; Architecture Contract 1.2 remains current.

The prior Luna-30 full-suite evidence was 896 passed, 11 failed, 1 skipped
(908 collected). The outstanding groups were 2 Luna-12E, 8 Luna-12L, and 1
spiral. The full suite was not rerun for this governance decision.

## Failure reproduction

Command, using the selected Python 3.11.5 interpreter:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m pytest -q tests/test_luna12e_integration.py::test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes tests/test_luna12e_integration.py::test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary
```

**OBSERVED:** both tests failed as specified. The first passed route absence,
route presence, and event-count increase, then failed only because prediction
loss was equal. The second passed object-identity stability and failed at its
first legacy exact-clock assertion: observed `5.0`, expected `0.0`. A separate
reset probe observed `[5.0, 5.0]` for both neurons.

## Causal-routing probe

Fixture: `make_synthetic_workload(examples_per_class=1,
points_per_example=2)`, seed 11, zero initial edges, edge capacity 1, and
`max_points=2`. The intervention added one directed edge,
`neuron-0 -> neuron-1`, with delay 1.0.

| Observation | No edge | With edge |
|---|---:|---:|
| Route trace `neuron-0 -> neuron-1` | absent | present |
| Public `metrics.event_count` | 12 | 14 |
| `edge_transfer_proxy` | 0.0 | 1.358357398350786 |
| `maximum_route_depth` | 0 | 1 |
| `prediction_loss` | 1.1724999999999999 | 1.1724999999999999 |

**OBSERVED:** the with-edge trace has an `EXCURSION` routed at `t=1.5` from
`neuron-0` to `neuron-1`, and a routed `prediction_error` at `t=2.0` over the
same path. The existing public metric is named `event_count`, rather than
`processed_event_count`; its measured increase is 12 to 14.

**INFERRED:** route absence/presence, extra events, positive edge-transfer
cost, and greater route depth directly evidence that the edge is causally
exercised. The prediction-loss inequality is not a valid required proxy for
that fact. The one-way edge terminates downstream from the predictor source;
equal external-target loss in this fixture does not imply failed routing.
Prediction semantics and the experiment are not changed, and no task-efficacy
claim follows.

## Reset and timing probe

Fixture: two-point synthetic workload (external timestamps 0.0 and 1.0),
seed 4, default EXCURSION_V1, repeated evaluation.

| Observation | Result |
|---|---|
| Neuron object identity across evaluations | stable |
| Last external timestamp | 1.0 |
| Configured `settling_horizon` | 4.0 |
| Expected terminal local timestamp | 5.0 |
| Final local timestamps | `[5.0, 5.0]` |
| Public `mode` | `E1Mode.N` for both |
| Public `state` | `0.0` for both |
| Public `pending_event` | `None` for both |

**OBSERVED:** `end_character` settles through
`last_external_timestamp + settling_horizon`, then character destruction
resets each neuron at that horizon. The subsequent `start_character` resets
neurons to its supplied first timestamp. Public reset observables are
available: local clock, mode, `state`, and `pending_event`.

**INFERRED:** the test's post-evaluation observations should assert the
settling-horizon timestamp and neutral/reset state. They must not compare the
terminal timestamp to the next character's first input timestamp: this fixture
does not observe the instant before that input.

### TANH_LEGACY disposition

**OBSERVED:** running the same reset/identity fixture with explicit
`neuron_model="TANH_LEGACY"` retained identity and yielded final clocks
`[0.0, 1.0]` on `TPCNNeuron` instances. The old exact-clock expectations have
meaning as model-scoped legacy behavior. Luna-31 may preserve them in a
separate explicit legacy control if inexpensive; this is not a gate and must
not replace the EXCURSION_V1 reset assertions.

## Assertion matrix

| Assertion / observable | Disposition | Reason |
|---|---|---|
| First test: route absent without edge | **KEEP** | Directly verifies the no-edge control. |
| First test: route present with edge | **KEEP** | Directly verifies the intervention reaches the declared endpoint. |
| First test: event-count increase | **KEEP** | Public `metrics.event_count` measured 12 → 14. |
| First test: prediction-loss inequality | **REMOVE AS STALE** | Equal 1.1724999999999999 losses coexist with direct routing evidence. |
| First test: edge-transfer comparison | **NEW E2 ORACLE** | Public transfer proxy measured 0 → 1.358357398350786. |
| First test: route-depth comparison | **NEW E2 ORACLE** | Public maximum route depth measured 0 → 1. |
| Second test: stable neuron identity | **KEEP** | Persistent objects remained identical across evaluations. |
| Second test: terminal clock `== 0.0` | **LEGACY-ONLY** | Stale for current E2 terminal state; valid for explicit TANH_LEGACY fixture. |
| Second test: terminal clock `== 1.0` | **LEGACY-ONLY** | Stale for current E2 terminal state; valid for explicit TANH_LEGACY fixture. |
| Second test: horizon-derived terminal clock | **NEW E2 ORACLE** | `1.0 + 4.0 == 5.0` observed for both neurons. |
| Second test: neutral mode/state after reset | **NEW E2 ORACLE** | Public mode `N` and state `0.0` observed. |
| Second test: no pending work | **NEW E2 ORACLE** | Public pending-event observation is `None`. |

## Architecture audit

| Clause | Disposition |
|---|---|
| A01 | Preserved: no global neural clock is introduced. |
| A02 | Preserved: event-local E2 time and the local settling/reset boundary remain explicit. |
| A03 | Directly observed: finite delayed edge routing is present at `t=1.5`, with routed error traffic at `t=2.0`. |
| A04 | Preserved: one edge is added within the existing finite topology. |
| A06 | Prediction semantics are unchanged. Equal scalar prediction loss for this intervention is not a routing defect or evidence of efficacy. |
| A07 | No neural inputs, labels, or future information are added. |
| A08 | Existing finite event and settling bounds remain unchanged. |
| A15 | Software-reference evidence only; no hardware equivalence claim. |

ACP-0007 remains accepted. No ACP, contract amendment, schema change, runtime
change, or production observability is required. E2 pruning and N3 remain
unauthorized. The first three legacy/general topology component tests remain
outside this compatibility decision and are not to be altered.

## Luna-31 authorization

**Authorized, not executed.** Exact contract:

```text
.github/agents/luna-31.agent.md
Luna-31 — Luna-12E EXCURSION_V1 Observable Compatibility Correction
```

Sequence: `Luna-0 -> Luna-31 -> Luna-0`.

Luna-31 owns only:

```text
tests/test_luna12e_integration.py
workflow/handoffs/luna-31-luna12e-e2-observable-compatibility-20261004.md
```

Prohibited files include `tpcn/experiments.py`,
`tpcn/experiment_excursion_runtime.py`, `tpcn/excursion_neuron.py`,
`tpcn/predictive_coding.py`, `tpcn/topology.py`,
`tpcn/structural_plasticity.py`, `tpcn/cpu_visualization.py`, and
`tpcn/visualization.py`; all Luna-12L and spiral code/tests; and the first
three historical Luna-12E topology component tests.

Required verification: all `tests/test_luna12e_integration.py` tests,
relevant EXCURSION_V1 integration/routing and Luna-26 multi-hop routing
regressions, and the full suite. Require zero Luna-12E failures and zero new
applicable regressions. Full-suite expected remaining issue groups are
Luna-12L (8) and spiral (1); do not hard-code a total pass count. If the
existing public observables prove insufficient, or production files appear
necessary, stop and return to Luna-0. No task efficacy or architecture
promotion claim is allowed.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Exact two-case pytest reproduction | Windows, Python 3.11.5, `main` / `origin/main` at `8d5f7f5ad1c594df3cd886de327eb14c3dfbe15c` | 2 failed, at the specified stale assertions | Terminal run in this Luna-0 session |
| No-edge / with-edge diagnostic | Same checkout; seed 11, synthetic 26-class workload, 1 example/class, 2 points/example | Event count 12 → 14; transfer 0 → 1.358357398350786; depth 0 → 1; routed trace present; loss equal | Pylance-selected Python snippet output |
| Reset/identity diagnostic | Same checkout; seed 4, default EXCURSION_V1 | Stable identities; `[5.0, 5.0]`; mode N; state 0; no pending event | Pylance-selected Python snippet output |
| Explicit TANH_LEGACY diagnostic | Same checkout; seed 4 | Stable identities; final clocks `[0.0, 1.0]` | Pylance-selected Python snippet output |
| Full suite / full Luna-12E file / unrelated regressions | Not run | Not run; prior full-suite baseline is recorded above | Not applicable |
| `git diff --check` after governance edits | Current worktree | Pass | No whitespace errors |

## Benchmark and resource results

- Dataset/split: no real dataset or benchmark; deterministic synthetic
  two-point-per-example diagnostic only.
- Diagnostic seeds/configurations: routed-edge probe seed 11, one generated
  example per class, two points per example, zero initial edges, one-edge
  capacity, `max_points=2`; reset probe seed 4, same two-point fixture, default
  `settling_horizon=4.0`.
- Classification efficacy: not evaluated. Prediction loss is reported above
  as an observability result only; no benefit is claimed.
- Activation counts, calibrated energy units, utility, latency calibration,
  and hardware results: not applicable / not measured.
- Connectivity and routing: one finite edge intervention; route depth changed
  0 to 1, and event-time trace showed delivery at 1.5 and prediction-error
  routing at 2.0. These are logical event-time units, not wall-clock latency.
- Resource interpretation: `edge_transfer_proxy` is the experiment's
  uncalibrated proxy, not physical energy. Existing event, queue, and settling
  bounds were not changed or independently benchmarked here.

## Assumptions, limitations, and next assignment

**HYPOTHESIZED before probes:** the first failure was a stale metric oracle and
the second stale timing oracle. The observed current public evidence supports
that classification. The single routed edge does not demonstrate task
improvement, and this governance-only work did not rerun the full suite.

## Reproduction and rollback

From the repository root, reproduce the two observed failures with the
command in the validation table. The causal and reset probes use the same
workload/configurations recorded above and in the measurement tables.

The safe restoration point is base revision
`8d5f7f5ad1c594df3cd886de327eb14c3dfbe15c`. If the project owner withdraws
this authorization, revert only the Luna-31 authorization profile, this
decision handoff, and the two governance entries added for this decision;
preserve the prior Luna-30 closure and all unrelated work.

Next assignment: **Luna-31**, as authorized above, followed by independent
review and closure by **Luna-0**. Luna-31 is not executed by this handoff.
