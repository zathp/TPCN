# Luna-0 architecture decision — slow temporal-integration state (ACP-0008)

- Agent: Luna-0 Architecture Guardian; date 2026-10-05; base revision `b0363ee035b1ffc60bd00d46277a0c789f11e570` (`HEAD == origin/main`, clean at start).
- Status: complete (governance only). Outcome: **ACP-0008 accepted as experimental, opt-in, default-disabled; Luna-38 AUTHORIZED / NOT EXECUTED.**
- Architecture change: true (new optional neuron state), proposal `workflow/docs/architecture_proposals/ACP-0008.md`; contract text not yet amended.
- Files changed: ACP-0008, this handoff, `.github/agents/luna-38.agent.md`, `LUNA_WORKFLOW.md`, `ARCHITECTURE_CHANGELOG.md`. No production code, tests, ACP-0007 or Luna-33..37 artifact changed.

## Decision and evidence

Owner decision: introduce a distinct slower internal integration state so temporally separated sub-threshold routed inputs can accumulate and be compressed into one canonical emission, while keeping fast output dynamics, canonical emission and extreme-excitation return behavior.

Evidence (Luna-37, reviewed): 1715 transfers per edge condition, 0 destination emissions, max destination state 0.6855 (w=1) / 0.9327 (w=2) < theta_E=1, arrival gaps >= ~12.9 vs decay rate 1.0. Failure is sub-threshold magnitude plus fast decay between arrivals, so w=2 changed magnitude but not accumulation. Luna-37 stays `NOT SUPPORTED IN THIS SETUP`; Luna-33/34/ACP-0007 verdicts are unchanged and nothing here reinterprets them.

## Model (full derivation in ACP-0008)

States: fast `x` (unchanged), slow `z`, canonical emission via the existing production path. Per event: `x <- x e^{-lambda dt}`, `z <- z e^{-lambda_z dt}`. External input `v` in mode N that leaves `|x| < theta_E`: `z <- clip(z + kappa v, +-Z_max)`; if `|z| >= theta_Z` and `x z >= 0`: `z <- z - s theta_Z`, `x <- x + s theta_Z` (then ordinary admission; `x in [theta_Z, theta_Z+theta_E) subset [theta_E, theta_M)`). Predeclared: `lambda_z=0.1`, `kappa=1`, `theta_Z=1`, `Z_max=4` (tau_z = 10 tau_fast; unit-normalized, not calibrated).

Reset/compression: subtractive discharge consumes exactly `theta_Z`, retains residual; one discharge per external event; amplitude and identity from the existing rules.

Oscillator staging: the existing E2 M regime (extreme-excitation return) is unchanged and independent of `z`; a `z`-driven multi-spike regime is deferred to a later Luna to avoid confounding.

Boundedness: `|z| <= Z_max`; discharges <= (|z0| + kappa sum|v|)/theta_Z; no discharge without an external input; no same-time loop; no free emission; neutral attractor.

## Prototype arithmetic (Luna-0 scratch check, not an experiment, no repository files)

| Fixture | Result |
|---|---|
| A: one 0.4 at t=0 | no emission; z=0.4 |
| B: 0.4 at t=0,2,4,6 | z=0.4, 0.72749, 0.99562, then discharge at t=6 (x=1.4625, z residual 0.21514) -> one emission |
| B3: first three | z=0.99562 < 1, no emission |
| C, spacing 10 | z=0.4, 0.54715, 0.60129, 0.6212, no emission |
| C, spacing 40 | z ≈ 0.4073, no emission |
| D: 1.2 isolated | legacy path; z=0 |
| negative mirror of B | one emission, negative sign |

Caveat: B3 sits only 0.0044 below `theta_Z`; B's success is deliberately near threshold and is a test of the equations, not a calibration. The contract requires exact-formula comparison and not just emission counts.

## Interface audit (not modified)

`ir2.py` (`neuron_to_ir2*`, `neuron_from_ir2*`) and `visualization.py` (`ExcursionNeuronRecord.from_neuron`) assume scalar `x`; Luna-38 must make them reject integration-enabled neurons. `experiment_excursion_runtime.py` and `experiments.py` construct default `E1Config`, so are unaffected when disabled. Routing, prediction, error, reward, eligibility, ACP-0007 evidence: unchanged.

## Known unknowns

Inputs during non-N modes are not integrated; no energy accounting for `z`; `x z >= 0` sign gating; unit-scale parameters may not rescue Luna-37 streams (decay 0.275 per 12.9 gap; steady-state z for 0.4 inputs ≈ 0.55 < 1); no biological-equivalence claim; hardware precision unproven; whether an eventual task stream needs different parameters is deferred and must be separately justified, never swept in Luna-38.

## Next

Luna-38 execution (`.github/agents/luna-38.agent.md`, AUTHORIZED / NOT EXECUTED), then independent Luna-0 review.
