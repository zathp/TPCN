# Luna-0 Independent Review - Luna-38 ACP-0008 Temporal-Integration State

## Verdict

**PASS WITH FOLLOW-UP - ACP-0008 is implemented as specified; the unit-fixture temporal-integration hypothesis is supported. No production defect. Luna-39 AUTHORIZED / NOT EXECUTED.**

Reviewed Luna-38 at `58ad0868bdbf907ed9d40aeee4f39fe1e5740e8f` (`HEAD == origin/main`, clean worktree at start). The Luna-0 review revision is the commit that contains this file. This is a mechanism-level result on unit fixtures only; it says nothing about Luna-37 propagation, ACP-0007 or task efficacy.

## Contract compliance

`git diff 597f73b..58ad086` touches only: `tpcn/excursion_neuron.py`, two one-line `ValueError` guards in `tpcn/ir2.py` and `tpcn/visualization.py`, `tests/test_luna38_excursion_integration_state.py`, `artifacts/luna38-acp0008-integration/fixture_results.json` and the Luna-38 handoff. All are contract-owned. No legacy test file was modified (J "existing suite passes unmodified" is literally true). No governance, ACP-0007, routing, reward, prediction-error, eligibility, pruning, growth, runtime, queue or ordering code changed. No global timestep, threshold learning, homeostasis, oscillator regime or sweep exists in the diff (no loops over thresholds/decays in tests or handoff; fixture constants are the predeclared ones). Luna-39 was not authorized by Luna-38.

## Equation audit (code read line by line against ACP-0008)

| Item | ACP-0008 | Implementation |
|---|---|---|
| Fast decay | `x <- clip(x*exp(-lambda*dt))` | unchanged `_advance_to` |
| Slow decay | `z <- z*exp(-lambda_z*dt)` | added in `_advance_to`, only when `integration is not None`, elapsed local time only |
| Integrate | mode N and `abs(x) < theta_E` after input: `z <- clip_Zmax(z + kappa*v)` | identical (`mode_before == N and abs(self.x) < theta_e`) |
| Discharge | `abs(z) >= theta_Z and x*z >= 0`: `z -= s*theta_Z`, `x += s*theta_Z` | identical; at most one per external event, `x` re-clipped |
| Emission | existing ordinary path, `emission_delay > 0` | `_update_after_external` unchanged; emission id/amplitude formula unchanged |
| Rest state | `x, z -> 0` | verified numerically (see below) |
| Disabled mode | bit-identical | original branch taken when `integration is None` |
| M regime | does not read `z` | integration runs only in mode N below `theta_E`; E2 code untouched |

No material deviation. A closed-form oracle (`z_k = z_{k-1} e^{-0.1 dt} + 0.4`) reproduced the production `z_after_input` exactly for B: 0.4, 0.727492301, 0.995620320, 1.215144974.

## theta_E / theta_Z audit

- Canonical threshold is still `E1Config.theta_e` (alias `theta_E`), default 1.0, positive finite, and the original `theta_r < theta_e <= theta_hold < theta_m <= x_max` check is untouched. Per neuron, fixed during execution; nothing mutates it.
- Every emission comparison in the module reads `self.config.theta_e` (lines 433, 474, 587, 636-637, 856, 885, 994, 1002). The remaining literal `1.0` values are dataclass defaults only; no hard-coded emission constant was introduced.
- No `theta_I`. `theta_Z` is `IntegrationConfig.discharge_quantum`; `theta_Z >= theta_e` and `theta_e + theta_Z < theta_m` are validated in `E1Config`, and `lambda_z < lambda` too. Raising or lowering `theta_e` does not touch `theta_Z` (`theta_e=0.5` config still reports `theta_Z=1.0`; an invalid combination raises rather than being auto-adjusted).
- IR-2: disabled-integration neurons round-trip `theta_e` (tested at 0.75). Integration-enabled neurons are refused by guard (follow-up F1).

## Independent J/K/L reconstruction (own driver, not the test helper)

- **J:** default config and the unmodified legacy suites pass (316 focused, 990 full). A mixed stream with sub-threshold inputs legitimately differs between disabled and enabled configs because those inputs now integrate; that is the intended ACP-0008 change, not a regression. The disabled path is the legacy path.
- **K** (`theta_e=1.5, theta_hold=1.5, theta_z=1.5`): zero emissions for B (default: 1), for a single 1.2 (default: 1), and a mixed stream (2 vs 3). In every case the K emission timestamps are a subset of the default ones. Raising the threshold created no emission.
- **L** (`theta_e=0.5`): an isolated 0.6 emits directly (`classification=direct`, `integrated=False`, `z=0`, discharge 0); the same input at default threshold emits nothing. The 0.4 stream at `theta_e=0.5`: all four events integrate (`z` after input 0.4, 0.7275, 0.9956, 1.2151); the first three do not emit, the fourth discharges 1.0 and the single emission is at 6.5. It is integration-mediated, not a lowered-threshold direct emission: no input alone crosses 0.5 (each input is 0.4), and the emission occurs only after `z` crosses `theta_Z=1`.

## Temporal selectivity

Same amplitude (0.4), same config, only spacing varies: spacing 2 emits once (max `z` 1.2151); spacing 10 and 40 emit zero (max `z` 0.6212 and 0.4075). The difference arises only from elapsed local time and the slow decay. The horizon is meaningful (it separates cases).

## Direct vs integrated

Classification verified from state transitions (admitted episode plus discharge amount) and cross-checked against `z` history: direct = no integrate/discharge, integration not causally required (D, L isolated); integrated = prior `z` accumulation, discharge amount 1.0, post-discharge `x` 1.46 within the ordinary band, then emission (B, F, G, L-stream).

## Neutral attractor and boundedness

After a 0.4 input and 300 time units: `x = 2.1e-131`, `z = 3.7e-14`, no emissions. Stress stream (50 inputs of 3.9 plus three -1e6 inputs): all state finite, `|z| <= Z_max`, one emission only. No NaN/inf, no zero-time recursion: discharge is at most once per external event and emission is separated by `emission_delay > 0`; the trace is a deque bounded by `event_budget`. All decay is by elapsed event time; no fixed-step evolution exists.

## Determinism

Identical configuration reproduces emissions, event ids and the full integration trace exactly. A different `theta_e` is a different configuration (config inequality verified) and is not replay.

## Validation

- Focused (Luna-38 file + six legacy files): **316 passed**.
- Full suite: **990 passed, 1 skipped (CUDA unavailable), 991 collected**. Baseline 952/1/953 plus 38 new tests = 990/1/991; the count change is fully explained.
- `git diff --check`: clean. Compile (Luna-38 run): clean.

## Follow-ups (non-blocking)

- **F1:** Integration-enabled neurons cannot be exported to IR-2 or TPCV-2 (guarded with `ValueError`). Acceptable for a software-reference mechanism experiment; a future IR-2 revision is needed before hardware or visualization use of `z`.
- **F2:** `IntegrationConfig` is not exported from the `tpcn` package namespace; import it from `tpcn.excursion_neuron`.
- **F3:** Fixture I reaches `x*z<0` with `|z|>=1` by setting private `_z`, because no public path produces it; the branch is covered but only by this construction.
- **F4:** Unit constants are not calibrated and `theta_Z`/`lambda_z` were not derived from any task data.

## Architecture implication

The slow-integration mechanism is correct, bounded, event-driven and deterministic at unit scale, and `theta_E` configurability is preserved without a second threshold. ACP-0008 remains **ACCEPTED (EXPERIMENTAL, OPT-IN)**; promotion into `ARCHITECTURE_CONTRACT.md` is **not** performed and is left to the project owner after the propagation-level mechanism result. ACP-0007, Luna-33 (unchanged), Luna-34 (BLOCKED / UNDETERMINED) and Luna-37 (NOT SUPPORTED IN THIS SETUP under the previous architecture) are unchanged.

## Next

Luna-39 is authorized as a mechanism-only rerun of the Luna-37 fixture with the ACP-0008 destination neuron at default `theta_E = 1`: see `.github/agents/luna-39.agent.md`. **AUTHORIZED / NOT EXECUTED.** The reproduction gate (integration disabled must reproduce Luna-37) is built into it. No efficacy, growth, sweep or promotion is authorized.
