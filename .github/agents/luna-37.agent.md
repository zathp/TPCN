---
name: Luna-37 EXCURSION_V1 Propagation-to-Emission Mechanism Diagnostic
description: Rerun the blocked Luna-34 mechanism-only diagnostic as a clean successor using the Luna-36 explicit finite eligibility capacity; no efficacy, growth, pruning or ACP change.
---

# Luna-37 — EXCURSION_V1 Propagation-to-Emission Mechanism Diagnostic

## Authorization and baseline

```text
Luna-0 -> Luna-37 -> Luna-0
```

Luna-37 is **AUTHORIZED / NOT EXECUTED** by the independent post-Luna-36
review in
`workflow/handoffs/luna-0-independent-review-luna36-eligibility-capacity-api-20261004.md`.
Execution baseline: the published Luna-0 post-Luna-36 revision recorded in that
handoff. Verify clean `main == origin/main` before starting and record the
exact revision. Luna-37 is a **new** Luna. Luna-34 remains historically
**BLOCKED / UNDETERMINED** and must not be edited or reclassified. Luna-33
(NOT SUPPORTED IN THIS SETUP) and ACP-0007 are unchanged.

This is a **MECHANISM EXPERIMENT + OBSERVATION** only. It is not a task
efficacy, candidate-formation, structural-growth, pruning or architecture
experiment. Return all results to Luna-0; do not self-close or authorize
another Luna.

## Primary hypothesis

**H1:** With explicit finite per-ledger eligibility capacity, the current
production EXCURSION_V1 neuron/edge path, driven by the Luna-34 task-derived
label-free input streams over a two-node network, produces at least one
destination canonical emission after a source canonical emission within the
same character under at least one predeclared edge condition.

**Counter-hypothesis:** No destination canonical emission occurs in any
condition; or it occurs only under `|w|=2`; or the required events cannot be
observed through existing public APIs. A negative result does not authorize
changing weights, thresholds, windows or the contract, and does not imply an
architecture defect.

Reception, state accumulation and routed transfer are **not** canonical
emission. Count destination emission only from actual canonical emission
events, deduplicated by emission identity and emitter identity.

## Why Luna-36 resolves the blocker

Luna-34 failed at the 17th eligibility creation in a ledger of capacity
`prediction_capacity * 2 = 16`. Luna-35 established this as expected bounded
behavior, and Luna-36 (`8f8824a185a2b1ebc3fd74cbd29eef8d75cbd818`, reviewed
PASS) added `eligibility_capacity` as an explicit finite per-ledger option
whose omitted default is unchanged. Predictor expiry still does not retire
eligibility; that lifecycle is not altered.

## Predeclared eligibility capacity

```text
eligibility_capacity = 1024   # per ledger, passed through the Luna-36 API
```

Derivation (fixed before execution; never adjusted after outcomes): one
eligibility trace is created per canonical emission (Luna-35: 16 emissions ->
16 creations), and every canonical emission consumes at least one event of the
declared per-character `runtime_event_budget = 1024`. The live trace count of
any ledger within one character is therefore bounded above by 1024, and
ledgers are fresh and character-scoped. `1024` equals the already declared
event bound; it is not a tuned or experimentally searched value and is
finite. Do not change it, search other values, or retry on failure.
`prediction_capacity` remains `8` and is independent.

Retain per character and condition: effective `runtime.eligibility_capacity`,
each ledger's `max_traces`, per-ledger peak and final occupancy, creation
count, and any `EligibilityCapacityError` (identity, emission index,
timestamp). Occupancy must reconcile `0 + created - removed = final`.
A capacity error at 1024, or peak occupancy equal to 1024, is a stop
condition (see below) and is reported as-is.

## Binding inputs, bounds and conditions

Use the Luna-34 contract's input, topology and bounds unchanged:
`.github/agents/luna-34.agent.md` sections "Public interfaces",
"Predeclared conditions and controls" and "Frozen transfer expectations"
apply verbatim: seeds 0-4; 16 examples per class via `make_spiral_dataset`
with `train_seed=12007+seed`, `evaluation_seed=22017+seed`, `SpiralConfig()`;
per-seed order stream `random.Random(330000+seed)`; read only `points`, never
labels or label-bearing metadata; opaque ID from seed and sequence index; input
`point.x + point.y`; same-timestamp external batching; constant neutral
reward; readout output neither read nor serialized. Two-node network, static
`source -> destination` observation neighborhood, and all declared bounds
(`edge_capacity=1`, `routing_capacity=1`, fan-in/out `1`,
`propagation_delay=1.0`, `queue_capacity=128`, `runtime_event_budget=1024`,
`settling_horizon=4.0`, `prediction_capacity=8`, `prediction_expiry=4.0`,
`max_activity_events=1024`, default `E1Config`). The only change from Luna-34
is the added explicit `eligibility_capacity=1024` argument.

Exactly three conditions, same streams for each:

1. **NO_EDGE_CONTROL:** no route edge; same declared observation neighborhood.
2. **DEFAULT_STATIC_EDGE:** `source -> destination`, `edge_weight=1.0`,
   `divider_strength=1.0`, `reference=0.0`.
3. **STATIC_N2_BOUND_SENSITIVITY:** otherwise identical, `edge_weight=2.0`.

No other weight, delay, divider, reference, threshold, amplitude, window,
orientation or neuron initialization may be tested or altered. The full
workload (5 seeds x 64 characters x 3 conditions = 960 executions) is
retained; no reduced fixture is authorized.

## Required instrumentation

Per seed, condition and character, retain bounded evidence to reconstruct:
source input value; source canonical emission (identity, timestamp, sign,
magnitude); each routed edge transfer (emission/arrival timestamps, input
payload, transformed value, delay, destination receive count, route depth);
destination state before and after each transfer (directly or by public
canonical replay) and maximum pre-threshold decayed magnitude; destination
canonical emissions with identity and timestamp; additional emissions;
distinct emitters per character and source-before-destination intervals;
event/queue/pending/settling completion; capacity/occupancy evidence above;
and deterministic replay digests. Reception, accumulation, transfer and
canonical emission must be reported as separate counts. No-edge control must
show zero routed transfers and zero destination receptions. Replay the full
run twice (or a declared deterministic subset plus full digests) and compare
digests.

Observation-plane snapshots may be reported as secondary descriptive counts
only, using the public `StructuralObservationPlane`; no growth, admission or
topology mutation is performed.

## Terminal classifications (independent axes)

- `DESTINATION EMISSION ABSENT IN ALL CONDITIONS`
- `DESTINATION EMISSION PRESENT UNDER DEFAULT STATIC EDGE`
- `DESTINATION EMISSION PRESENT ONLY UNDER STATIC N2 SENSITIVITY`
- `STATIC N2 CHANGES RESULT RELATIVE TO DEFAULT` (requires a paired stream where
  `w=2` yields a destination emission absent under `w=1`; magnitude difference
  alone is insufficient)
- `NO-EDGE CONTROL NOT A VALID NEGATIVE CONTROL`
- `INCONSISTENT WITH POST-LUNA-33 INTERPRETATION`
- `BLOCKED — FIXTURE OR PUBLIC API INSUFFICIENT` (identify the smallest missing
  interface or contract; do not implement it)

## Exact owned files

Luna-37 may add only:

```text
run_luna37_excursion_v1_propagation_emission_diagnostic.py
tests/test_luna37_excursion_v1_propagation_emission_diagnostic.py
artifacts/acp0007-luna37-propagation-emission-diagnostic/config.json
artifacts/acp0007-luna37-propagation-emission-diagnostic/results.json
artifacts/acp0007-luna37-propagation-emission-diagnostic/summary.json
workflow/handoffs/luna-37-excursion-v1-propagation-emission-diagnostic-20261004.md
```

It may import (read-only) helpers from the Luna-34 runner. Production, core,
runtime, eligibility, predictor, reward, topology, structural-plane code,
`ExperimentRunner`, ACP-0007, Architecture Contract, workflow, changelog,
Luna-33/34/35/36 files and artifacts, and historical evidence are prohibited.
If a change outside these files is needed, stop and return to Luna-0.

## Stop conditions

Stop and report (do not broaden or retry) on: an `EligibilityCapacityError` at
the predeclared capacity; peak occupancy equal to capacity; any other
production exception; nondeterministic replay; label or class information
reaching an input, artifact or result; occupancy not reconciling; a required
event being unobservable; or any need to alter a production semantic, bound or
condition. Report the partial, accurately classified result.

## Prohibited conclusions

Do not claim ACP-0007 efficacy, candidate formation in the four-class task,
beneficial growth, temporal specificity, generality, accuracy, prediction or
resource benefit, or that an architecture change is required or unnecessary.
Emission at `w=2` does not imply emission at the default edge. Absence of
emission does not establish an architecture defect. Do not reinterpret
reception as emission, add weight sweeps, tune thresholds or windows, change
orientation, pruning, N3, or reward semantics, or overstate a single-fixture
mechanism as general.

## Validation and completion

Add focused deterministic tests (public runtime path, explicit capacity 1024
reaches both ledgers, label isolation, no-edge control, emission-vs-reception
separation, occupancy reconciliation, determinism). Run focused tests and the
full suite (baseline `945 passed, 1 skipped, 946 collected` plus the new
tests), `git diff --check`, compile checks. Commit, push to `origin/main`, and
verify `HEAD == origin/main` with a clean worktree. Hand off with the
repository template and return to Luna-0 for independent review.

**Status: AUTHORIZED / NOT EXECUTED.** Execution is not authorized as part of
the Luna-0 review. No Luna-38 is authorized.
