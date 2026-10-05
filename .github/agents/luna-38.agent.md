---
name: Luna-38 ACP-0008 Slow Temporal-Integration State
description: Implement and verify only the accepted ACP-0008 opt-in slow integration state in the EXCURSION_V1 neuron with unit mechanism fixtures; no task efficacy, ACP-0007 or routing change.
---

# Luna-38 — ACP-0008 Slow Temporal-Integration State

## Authorization and baseline

```text
Luna-0 -> Luna-38 -> Luna-0
```

Luna-38 is **AUTHORIZED / NOT EXECUTED** under accepted
`workflow/docs/architecture_proposals/ACP-0008.md` and
`workflow/handoffs/luna-0-owner-decision-acp0008-temporal-integration-20261005.md`.
Execution baseline: the published Luna-0 ACP-0008 revision (verify clean
`main == origin/main`, record the exact revision, and read ACP-0008 in full;
it is the mathematical specification). Luna-37 (NOT SUPPORTED IN THIS SETUP),
Luna-34, Luna-33 and ACP-0007 are historical and must not be edited or
reinterpreted. Return everything to Luna-0; do not self-close, promote into
`ARCHITECTURE_CONTRACT.md`, or authorize another Luna.

## Primary hypothesis

An opt-in `IntegrationConfig` slow state `z` (`lambda_z=0.1`, `kappa=1.0`,
`theta_Z=1.0`, `Z_max=4.0`, with the existing `lambda=1`, `theta_E=1`,
`theta_M=4`, `emission_delay=0.5`) lets temporally close sub-threshold inputs
compress into one canonical emission, while isolated, far-spaced or
disabled-mode inputs do not. Counter-result: any fixture below deviating from
its predeclared outcome, any emission without an external input, or a bound
violation.

## Implementation (the only production edit)

1. Add frozen `IntegrationConfig` and an optional `E1Config.integration=None`
   (appended last, keyword-compatible), with ACP-0008 validation
   (finite, positive, `lambda_z < lambda`, `theta_Z >= theta_E`,
   `theta_E + theta_Z < theta_M`, `theta_Z <= Z_max`). Serialization of the
   disabled config must be unchanged.
2. Implement the ACP-0008 equations exactly: decay of `z` with elapsed time at
   every `_advance_to`; integration only for external inputs in mode `N` that
   leave `|x| < theta_E`; discharge only when `|z| >= theta_Z` and `x*z >= 0`,
   at most one per external event, subtractive, then the unchanged ordinary
   admission and emission path. Apply identically to `SingleExcursionNeuron`
   and `MultiExcursionNeuron`; the E2 `M` regime must not read or change `z`.
3. Expose read-only `integration_state` (and a bounded trace, capacity
   `event_budget`, recording per external event: timestamp, elapsed, input,
   `x` before/after decay, `z` before/after decay, `z` after input, integrated
   flag, discharge amount, configured `theta_E`, emission id, post-discharge
   `x` and `z`).
4. Make `neuron_to_ir2`, `neuron_to_ir2_e2` and
   `ExcursionNeuronRecord.from_neuron` raise a clear `ValueError`/`TypeError`
   for integration-enabled neurons (smallest guard; no schema change). Add
   these guards without otherwise editing those modules.
5. With `integration=None` behavior must be bit-identical to baseline.

## Predeclared fixtures (normalized units, no tuning, no sweeps)

Fresh neuron, `E1Config(integration=IntegrationConfig())`, external input
payload `v` at time `t`:

| Id | Stream | Required outcome |
|---|---|---|
| A | `v=0.4` at `t=0`; observe at `t=100` | 0 emissions; `z=0.4` after input; `|z|<1e-4`, `|x|<1e-4` at 100 |
| B | `v=0.4` at `t=0,2,4,6` | `z` after inputs 0.4, 0.727490, 0.995620 (±1e-5); exactly one discharge at `t=6`; `x` after discharge 1.4625 (±1e-4); residual `z` 0.21514 (±1e-5); exactly one canonical emission at `t=6.5`, positive |
| B3 | first three B inputs | 0 emissions; `z=0.99562` |
| C10 | `v=0.4` at `t=0,10,20,30` | 0 emissions; `z` 0.4, 0.54715, 0.60129, 0.6212 (±1e-4) |
| C40 | `v=0.4` at `t=0,40,80,120` | 0 emissions; `z` max ≤ 0.4075 |
| D | `v=1.2` at `t=0` | one emission identical in ids, timestamps, payload to the `integration=None` run; `z=0` |
| F | B with `v=-0.4` | one emission at `t=6.5`, negative sign, mirrored `z` |
| G | 40 inputs `v=0.4` at spacing 3 | `|z| <= Z_max` always; discharges ≤ floor(Σκ|v|/θ_Z); `θ_Z × discharges` equals integrated minus decayed minus remaining `z` (conservation check from trace); no emission lacking an external input |
| H | B stream with `integration=None` | 0 emissions (disabled control) |
| I | mixed-sign inputs | no discharge when `x*z < 0`; `z` retained |

Threshold-configurability fixtures (API/dynamics validation only; exactly
these three non-default values, no sweep, no Luna-37 data):

| Id | Config | Stream | Required outcome |
|---|---|---|---|
| J | default `theta_e=1`, `IntegrationConfig()` omitted | fixtures from the existing neuron tests | unchanged; the existing suite passes unmodified (default-threshold compatibility) |
| K | `theta_e=1.5`, `theta_hold=1.5`, `IntegrationConfig(theta_z=1.5)` (`theta_E+theta_Z=3<theta_M`) | B stream (0.4 at 0,2,4,6) and D-like `v=1.2` | 0 emissions in both; for every stream, emissions at `theta_e=1.5` are a subset of those at default (higher-threshold control: never creates an emission absent at the lower threshold); `z` still integrates (record `z` trajectory) |
| L | `theta_e=0.5`, default `IntegrationConfig()` | isolated `v=0.6` at `t=0` | one emission at `t=0.5` directly from `x`, `integrated=False`, `z=0` throughout, no discharge; the same input at default `theta_e=1` gives 0 emissions. Also the B stream with `theta_e=0.5` still shows `z` trajectory identical to B and emission via discharge at `t=6` (`integrated=True` for the first four inputs, `0.4<0.5`) |

Every threshold fixture must retain in its trace the configured `theta_E`,
the `z` trajectory, the threshold-crossing `x` (value and event), the exact
canonical emission event and the post-emission `x`/`z`, so a reviewer can
tell *emission through accumulated evidence* (`integrated=True`, `z`
discharge, `x` crossing after discharge) from *emission because the
threshold was lowered for one isolated input* (`integrated=False`, no
discharge). The code must read `config.theta_e` at each use (no cached
constants), reject no new threshold values beyond the existing
`E1Config` validation plus the ACP-0008 integration validation, and leave
the `theta_e` field and IR-2 serialization unchanged. Luna-38 must not add
threshold learning, homeostasis, optimization or runtime mutation.

Required temporal-selectivity comparison: B (Δ=2) emits; C10 (Δ=10) and C40
(Δ=40) do not. Report it explicitly. Unit tests must also assert
deterministic replay (identical results and event ids on two runs), bounded
queue/trace behavior, strictly positive delay between discharge and
emission, and that `M`-regime behavior with integration enabled but `z=0`
equals the disabled neuron. Optional extreme-excitation (E) fixture is
**not** part of Luna-38; the `z`-driven oscillator is staged out.

## Files

Allowed: `tpcn/excursion_neuron.py`; minimal guards in `tpcn/ir2.py` and
`tpcn/visualization.py` (item 4 only); `tests/test_luna38_excursion_integration_state.py`;
`workflow/handoffs/luna-38-acp0008-temporal-integration-<date>.md`; optional
`artifacts/luna38-acp0008-integration/` (fixture results with exact values).
An explanatory sentence in `workflow/docs/architecture/` is allowed only if
it states the status as experimental. Prohibited: `ARCHITECTURE_CONTRACT.md`,
`ARCHITECTURE_CHANGELOG.md`, `LUNA_WORKFLOW.md`, ACP-0007/0008, this
contract, experiment/runtime/routing/eligibility/reward/prediction code, any
Luna-33..37 test or artifact, and any tuning of existing tests. Do not
change existing test expectations; stale expectations are reported, not
edited.

## Required validation

Baseline: 952 passed, 1 skipped (CUDA), 953 collected. Focused:
`test_excursion_neuron.py`, `test_e2_multi_excursion.py`, `test_ir2.py`,
`test_e2_ir2.py`, `test_excursion_integration.py`, `test_visualization.py`,
`test_luna37_*`, plus the new file. Full suite expected: 952 plus new tests
passed, 1 skipped. Report each count change, `git diff --check`, and compile
checks.

## Stop conditions — return BLOCKED, do not broaden

Stop and report if satisfying a fixture or the ACP would require changes to:
reward semantics, prediction-error semantics, ACP-0007, structural growth,
eligibility lifetime, event ordering, a global timestep, or unbounded
same-time event generation; if no stable bounded implementation of the
ACP-0008 equations exists; if disabled mode cannot be bit-identical; or if the
IR/TPCV guards need schema changes. Do not alter parameters to pass a
fixture: report the deviation.

## Prohibited conclusions

A pass establishes only that the specified bounded slow-state mechanism
behaves as predeclared on unit fixtures. It does not establish task efficacy,
rescue of Luna-37 or Luna-33 streams (Luna-37 gaps of ≥12.9 decay by 0.275,
and calibration is not authorized), candidate formation, structural growth,
temporal specificity beyond the three predeclared spacings, biological
equivalence, hardware equivalence, energy benefit, contract promotion, or
any z-driven oscillator behavior, and any claim that a threshold value is
optimal, learned or task-appropriate (fixtures K and L validate only that
`theta_e` is causally connected to emission). No parameter sweep or parameter change is
authorized.

## Completion

Handoff must include fixture tables with exact values, trace excerpts,
interface audit, test counts and the exact commit. End with exactly:

**Luna-38 complete; returned to Luna-0 for independent post-Luna-38 review. ACP-0008 not promoted into the architecture contract. No next Luna authorized.**
