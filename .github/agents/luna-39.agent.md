---
name: Luna-39 ACP-0008 Propagation-to-Emission Mechanism Diagnostic
description: Rerun the Luna-37 two-node mechanism fixture with the ACP-0008 slow-integration destination neuron at default theta_E=1; mechanism only; no sweeps, efficacy, growth or architecture change.
---

# Luna-39 - ACP-0008 Propagation-to-Emission Mechanism Diagnostic

## Authorization and baseline

```text
Luna-0 -> Luna-39 -> Luna-0
```

Luna-39 is **AUTHORIZED / NOT EXECUTED** by the independent post-Luna-38 review in
`workflow/handoffs/luna-0-independent-review-luna38-acp0008-temporal-integration-20261005.md`.
Baseline: the published Luna-0 post-Luna-38 revision recorded in that handoff.
Verify clean `main == origin/main` and record the exact revision first. Luna-39 is a
**new** Luna. Luna-37 stays **NOT SUPPORTED IN THIS SETUP** (previous architecture),
Luna-34 stays **BLOCKED / UNDETERMINED**, Luna-33 and ACP-0007 are unchanged.

This is a **MECHANISM EXPERIMENT + OBSERVATION** only. It is not a task-efficacy,
candidate-formation, growth, pruning or architecture experiment. Return all results
to Luna-0; do not self-close or authorize another Luna.

## Primary hypothesis

**H1:** With the destination neuron using ACP-0008 slow temporal integration at its
predeclared default parameters and the default canonical threshold `theta_E = 1`, the
sparse routed source->destination stream of the Luna-37 fixture produces at least one
destination canonical emission after a source canonical emission within the same
character, under at least one predeclared edge condition, and that emission is
**integration-mediated** (destination `z` accumulated over at least two transfers and
`theta_Z` discharge preceded it).

**Counter-hypothesis:** No destination canonical emission in any condition; or only under
`|w| = 2`; or emissions arise without integration; or the required events are not
observable. A negative result authorizes no change to weights, thresholds, decay rates,
`theta_Z`, windows or the contract and does not imply an architecture defect.

Reception, state or `z` accumulation and routed transfer are **not** canonical emission.
Count destination emission only from canonical emission events, deduplicated by emission
identity and emitter identity.

## Predeclared architecture parameters (never adjusted)

```text
destination neuron : MultiExcursionNeuron, E1Config(integration=IntegrationConfig())
theta_E            = 1.0   (E1Config default; NOT lowered)
IntegrationConfig  = decay_rate_z 0.1, input_gain 1.0, discharge_quantum (theta_Z) 1.0, z_max 4.0
all other E1Config fields = defaults (unchanged from Luna-37)
source neuron      : default E1Config, integration disabled (source stream identical to Luna-37)
eligibility_capacity = 1024 per ledger (Luna-37 value; same derivation; not searched)
```

Integration is enabled **only on the destination**, so the source emissions and the
routed stream must equal Luna-37 exactly and the comparison isolates the destination
mechanism. The destination has no outgoing edge, so its emissions cannot feed back.
Neurons are created fresh per character as in Luna-34/37, so `z` starts at 0 for every
character. Do not serialize integration-enabled neurons to IR-2 or TPCV-2 (guarded).

Ex-ante arithmetic note (non-binding, not a success criterion): the Luna-37 review
recorded maximum received magnitudes of about 0.6855 (`w=1`) and 0.9327 (`w=2`) with
inter-transfer gaps of at least about 12.9. With `lambda_z = 0.1` the retained fraction
per gap is at most about 0.275, so unit arithmetic permits a `w=2` discharge but not a
`w=1` discharge from two similar transfers. This was derived from reviewed data and
fixed parameters, was not used to choose any parameter, and may be falsified. Any
outcome is acceptable and must be reported as measured.

## Binding inputs, bounds and design

Use the Luna-37 contract and runner inputs and bounds verbatim (which in turn use the
Luna-34 sections "Public interfaces", "Predeclared conditions and controls" and "Frozen
transfer expectations"): seeds 0-4; 16 examples per class via `make_spiral_dataset`,
`train_seed=12007+seed`, `evaluation_seed=22017+seed`, `SpiralConfig()`; order stream
`random.Random(330000+seed)`; read only `points`, never labels or label-bearing metadata;
input `point.x + point.y`; same-timestamp batching; constant neutral reward; two-node
network and bounds (`edge_capacity=1`, `routing_capacity=1`, fan-in/out 1,
`propagation_delay=1.0`, `queue_capacity=128`, `runtime_event_budget=1024`,
`settling_horizon=4.0`, `prediction_capacity=8`, `prediction_expiry=4.0`,
`max_activity_events=1024`).

Factorial design, same streams in every cell:

| Arm | Destination neuron | Conditions |
|---|---|---|
| `LEGACY_REPRODUCTION` | `E1Config()` (integration disabled) | NO_EDGE_CONTROL, DEFAULT_STATIC_EDGE (`w=1.0`), STATIC_N2_BOUND_SENSITIVITY (`w=2.0`) |
| `ACP0008_INTEGRATION` | `E1Config(integration=IntegrationConfig())` | the same three conditions |

6 cells x 5 seeds x 64 characters = 1920 executions; no reduced fixture. Edge definitions
(`divider_strength=1.0`, `reference=0.0`) are as in Luna-37. No other weight, delay,
divider, reference, threshold, decay, quantum, amplitude, window, orientation or
initialization may be tested or altered.

**Reproduction gate:** the `LEGACY_REPRODUCTION` arm must reproduce the reviewed Luna-37
counts (source emissions 1715 and routed transfers 1715 for the two edge conditions, 0
for no-edge, destination canonical emissions 0 in all three) and the source/transfer
streams must be identical across arms. A mismatch is a stop condition: it means the
fixture, not ACP-0008, changed.

## Required instrumentation

Per seed, arm, condition and character retain bounded evidence to reconstruct:
source input value; source canonical emission (identity, timestamp, sign, magnitude);
each routed transfer (emission/arrival timestamps, transformed value, delay, receive
count, route depth); the destination `integration_trace` entries (elapsed, `x` and `z`
before/after decay and input, `theta_E`, `theta_Z`, integrated flag, discharge amount,
post-discharge state, classification, emission id and time); maximum `|z|` per
character and condition; destination canonical emissions with identity, timestamp and
`direct` versus `integrated_discharge` classification; additional emissions; distinct
emitters; settling completion; eligibility effective capacity, peak and final occupancy,
creations, removals and reconciliation (`0 + created - removed = final`); and replay
digests. Report reception, `z`/state accumulation, discharge, routed transfer and
canonical emission as separate counts. The no-edge cells must show zero transfers and
zero destination receptions and zero destination `z`. Replay the full run twice and
compare digests.

Classify every destination emission in the integration arm from its trace (discharge
amount and prior `z`), not from a stored boolean alone. Any destination emission
classified `direct` is reported as inconsistent with the ACP-0008 mechanism.

## Terminal classifications (independent axes)

- `LEGACY ARM REPRODUCES LUNA-37` / `LEGACY ARM DOES NOT REPRODUCE LUNA-37`
- `INTEGRATED DESTINATION EMISSION ABSENT IN ALL CONDITIONS`
- `INTEGRATED DESTINATION EMISSION PRESENT UNDER DEFAULT STATIC EDGE`
- `INTEGRATED DESTINATION EMISSION PRESENT ONLY UNDER STATIC N2 SENSITIVITY`
- `Z ACCUMULATED BUT NEVER REACHED DISCHARGE` (maximum `|z|` below `theta_Z` everywhere)
- `STATIC N2 CHANGES RESULT RELATIVE TO DEFAULT` (requires a paired stream where `w=2`
  yields an integrated destination emission absent at `w=1`)
- `DESTINATION EMISSION WITHOUT INTEGRATION (INCONSISTENT)`
- `NO-EDGE CONTROL NOT A VALID NEGATIVE CONTROL`
- `BLOCKED - FIXTURE OR PUBLIC API INSUFFICIENT` (identify the smallest missing
  interface or contract; do not implement it)

## Exact owned files

Luna-39 may add only:

```text
run_luna39_acp0008_propagation_emission_diagnostic.py
tests/test_luna39_acp0008_propagation_emission_diagnostic.py
artifacts/acp0008-luna39-propagation-emission-diagnostic/config.json
artifacts/acp0008-luna39-propagation-emission-diagnostic/results.json
artifacts/acp0008-luna39-propagation-emission-diagnostic/summary.json
workflow/handoffs/luna-39-acp0008-propagation-emission-diagnostic-20261005.md
```

It may import (read-only) the Luna-34 and Luna-37 runner helpers and construct neurons
and a runtime through existing public APIs. Production, core, runtime, eligibility,
predictor, reward, topology, structural-plane code, `ExperimentRunner`, ACP-0007,
ACP-0008, the Architecture Contract, workflow, changelog, Luna-33/34/35/36/37/38 files
and artifacts and historical evidence are prohibited. If a change outside these files
is needed, stop and return to Luna-0.

## Stop conditions

Stop and report (do not broaden or retry) on: reproduction-gate mismatch; an
`EligibilityCapacityError` at 1024; peak occupancy equal to capacity; any other
production exception; nondeterministic replay; label or class information reaching an
input, artifact or result; occupancy not reconciling; a required event or
`integration_trace` being unobservable; non-finite state; or any need to alter a
production semantic, bound, parameter or condition. Report the partial, accurately
classified result.

## Prohibited conclusions

Do not claim ACP-0007 efficacy, candidate formation in the four-class task, beneficial
growth, temporal specificity, generality, accuracy, prediction or resource benefit,
calibration, hardware equivalence, or that ACP-0008 should or should not be promoted, or
that an architecture change is required or unnecessary. Emission at `w=2` does not imply
emission at `w=1`. Absence of emission does not establish a defect. Do not interpret
reception or `z` as emission; do not lower `theta_E`, sweep `theta_E`, `lambda_z`,
`kappa`, `theta_Z`, `Z_max` or weights; do not tune after observing results; do not
change orientation, windows, pruning, N3, reward or eligibility semantics; do not
overstate a single-fixture mechanism as general.

## Validation and completion

Add focused deterministic tests (public path; explicit capacity 1024 reaches both
ledgers; integration enabled on the destination only; label isolation; no-edge control;
reception versus `z` versus emission separation; legacy-arm reproduction check; trace
classification from state; occupancy reconciliation; determinism). Run focused tests and
the full suite (baseline `990 passed, 1 skipped, 991 collected` plus the new tests),
`git diff --check` and compile checks. Commit, push to `origin/main`, verify
`HEAD == origin/main` with a clean worktree, hand off with the repository template and
return to Luna-0 for independent review.

**Status: AUTHORIZED / NOT EXECUTED.** Execution is not authorized as part of the Luna-0
review. No Luna-40 is authorized.
