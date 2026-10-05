# Luna-38 Handoff - ACP-0008 Slow Temporal-Integration State

Status: **SUPPORTED (unit-fixture mechanism only)**. Start revision `597f73b`; ending revision = the commit containing this file (see git log).

## Files changed
`tpcn/excursion_neuron.py` (IntegrationConfig, E1Config.integration=None appended, trace, z dynamics); guards (`ValueError`) in `tpcn/ir2.py::_neuron_to_ir2` and `tpcn/visualization.py::ExcursionNeuronRecord.from_neuron`; `tests/test_luna38_excursion_integration_state.py` (38 tests); `artifacts/luna38-acp0008-integration/fixture_results.json` (exact values and full per-event traces); this handoff. No governance, ACP, routing, eligibility, reward or prediction files touched.

## Implementation
- `IntegrationConfig(decay_rate_z=0.1, input_gain=1.0, discharge_quantum=1.0, z_max=4.0)` (aliases lambda_z, kappa, theta_Z, Z_max); positive/finite, `discharge_quantum <= z_max`. E1Config validates `lambda_z < lambda`, `theta_Z >= theta_E`, `theta_E + theta_Z < theta_M`.
- `z` decays with exp(-lambda_z*elapsed) in every `_advance_to`. For an external input in mode N leaving |x| < theta_E, z = clip(z + kappa*v). If |z| >= theta_Z and x*z >= 0, at most one subtractive discharge per external event (z -= s*theta_Z, x += s*theta_Z), then the unchanged admission/emission path. The E2 M regime never reads or changes z.
- `theta_E` stays the existing `E1Config.theta_e`; no second threshold API, no theta_I, no coupling of theta_Z to theta_E. `integration=None` is bit-identical (original code path; serialization unchanged).
- `integration_state` and bounded `integration_trace` (capacity event_budget) are read-only. Trace entries also include theta_e, classification (none/direct/integrated_discharge), emission id/time and state at emission.

## Fixture results (exact, from artifact)
| Id | Result |
|---|---|
| A | 0 emissions; z=0.4 after input; |z|,|x|<1e-4 at t=100 |
| B | z after inputs 0.4, 0.727490, 0.995620; discharge at t=6; x after 1.4625; residual z 0.21514; 1 emission at t=6.5 (positive) |
| B3 | 0 emissions; z=0.9956203 |
| C10 | 0 emissions; z 0.4, 0.54715, 0.60129, 0.6212007 |
| C40 | 0 emissions; max z 0.4074629 |
| D | 1 emission at 0.5, identical to integration=None; z=0 |
| F | 1 emission at 6.5, negative, mirrored z |
| G | 10 emissions (every 12 time units, each following a discharge); z bounded; conservation holds from trace; no emission without external input |
| H | 0 emissions (disabled control) |
| I | no discharge when x*z<0; z retained (state set via private `_z` poke because no public path yields x*z<0 with |z|>=1) |
| J | default theta_E=1 reproduces legacy; disabled config serialization unchanged |
| K | theta_E=1.5 (theta_hold=1.5, theta_Z=1.5): B and v=1.2 produce 0 emissions (higher threshold never adds emissions) |
| L | theta_E=0.5: isolated v=0.6 emits directly (integrated=False, z=0); same input at default: none. B at theta_E=0.5 still integrates on all four events and emits via discharge at 6.5 (classification integrated_discharge) |

Temporal selectivity: spacing 2 emits (1); spacing 10 and 40 do not (0). Direct emissions (D, L isolated) are distinguishable from integrated emissions (B, F, G) by trace `classification`/`integrated`.

Also tested: neutral attractor (z, x -> 0 without input), deterministic replay (identical results and ids), bounded trace/queue, reset, strictly positive discharge-to-emission delay, M regime with z=0 equals disabled neuron, Single and Multi neurons, IR-2 guards and a theta_e=0.75 IR-2 round-trip for disabled integration.

## Validation
Legacy focused files (neuron, E2, ir2, e2_ir2, excursion_integration, visualization): 278 passed before the new file. New file: 38 passed. Full suite: **990 passed, 1 skipped (CUDA)**; baseline 952 + 38 new. `git diff --check` clean; `compileall` OK.

## Interface audit
Routing, prediction-error, eligibility, reward, event ids/ordering and energy accounting code untouched; emission uses the unchanged `_emit_ordinary` path. No tuning, no parameter or threshold sweep, defaults as predeclared.

## Limits / unresolved
IntegrationConfig is not exported from `tpcn/__init__.py` (not authorized). Integration-enabled neurons cannot be exported to IR-2/TPCV (guarded). Trace `x_before_decay`/`z_before_decay` are values at the last update. This establishes only unit-fixture mechanism behavior; no task efficacy, Luna-37 rescue, structural growth, hardware or biological claim; ACP-0008 not promoted into the architecture contract.
