---
name: Luna-23 ACP-0004 E2 Logical-Time Representability Correction
description: Correct and verify the strict-future E2 scheduling boundary when a positive delay is smaller than the current float timestamp resolution.
---

# Luna-23 - ACP-0004 E2 Logical-Time Representability Correction

## Authorization and baseline

Luna-23 is authorized for **IMPLEMENTATION + VERIFICATION** of the single
E2 logical-time representability defect independently reproduced in the
Luna-0 second review of Luna-22. Start from the published Luna-0 review
revision recorded in `workflow/handoffs/luna-0-second-independent-review-ACP-0006-Luna-22-20261003.md`,
then synchronize to the exact authorized repository tip before editing.
Record branch and worktree state.

This is a bounded correction within accepted ACP-0004 E2 semantics. It does
not authorize a state-machine, learning, topology or timing-model redesign.
If strict-future behavior cannot be preserved with a compatible numerical
correction, stop and return the evidence to Luna-0 for architecture review.
Do not invent a new delay equation or silently skip an internal transition.

## Observed defect

The deterministic `test_labels_do_not_change_canonical_four_class_trace`
workload reaches:

```text
clock       = 45.27906122689938
x           = -0.2500000000000003
theta_r     = 0.25
computed_dt = 1.110223024625156e-15
clock + dt  = 45.27906122689938
nextafter   = 45.27906122689939
```

The computed decay/rearm duration is positive, but adding it to the current
binary floating-point timestamp rounds to the same value. `_schedule()` then
raises instead of representing the earliest valid future event.

## Bounded file ownership

Own only:

- `tpcn/excursion_neuron.py`, limited to E2 strict-future logical timestamp
  calculation/validation;
- `tests/test_e2_multi_excursion.py` for the focused numerical-boundary
  regression;
- `workflow/handoffs/luna-23-e2-time-representability-20261003.md`.

Do not edit Luna-22's experiment adapter, dataset loader, visualization,
structural/research consumers, IR-2 startup, or workflow/changelog files.

## Hypothesis and counter-hypothesis

- **Hypothesis:** A mathematically positive finite E2 return delay can be
  represented by a deterministic strictly later logical timestamp without
  changing the E2 state machine or introducing a zero-time burst.
- **Counter-hypothesis:** Any correction changes canonical event timing beyond
  the existing contract or cannot guarantee bounded finite return.

## Required behavior and controls

- Preserve the existing analytic decay/rearm rule and strict causal ordering.
- If the computed positive delay is unrepresentable at the current timestamp,
  the correction must not produce `due_time <= current_time`.
- Do not silently discard the pending internal event or convert it into a
  same-time transition.
- Preserve deterministic replay, event identity, generation validation,
  event-budget termination and standalone E2 IR-2 behavior.
- Preserve independently closed E1 scheduling and reset behavior; do not alter
  shared E1 semantics to repair an E2-only representability failure.
- Test the exact observed values and both positive and negative state
  polarities where applicable.
- Include a finite-return assertion showing no zero-time loop or unbounded
  recurrence.

## Interfaces, information and architecture

- No labels, future points, task metrics, wall-clock timers or global clock
  enter the neuron.
- Only neuron-local state, local logical time, E2 configuration and the pending
  internal event may determine the correction.
- A01-A03, A08 and A15 are the relevant clauses. A01-A15 text is unchanged.
- No ACP is required for a compatible numerical implementation correction.
  If the solution requires new canonical timing semantics, stop before
  implementing them and request an ACP decision from Luna-0.
- No hardware-equivalence claim is permitted. Describe the operation in
  hardware-neutral terms and identify any floating-point-specific limitation.

## Acceptance and validation

Required evidence:

1. The focused test at the observed clock/state completes deterministically
   with a strictly future due timestamp.
2. Positive/negative return cases remain finite, bounded and ordered.
3. Existing E1 and E2 tests, E2 IR-2 tests, and the Luna-22 non-structural
   label-invariance case pass.
4. The prescribed regression set is run; full-suite failures are reported
   individually and are not hidden by fixing downstream consumers.
5. `compileall`, relevant diagnostics where available, and `git diff --check`
   are reported.

Do not modify consumers to make unrelated failures pass. Separate passed,
failed, not-run and not-applicable results. Leave all 15-problem categories
identified in the Luna-0 handoff unchanged.

## Explicit exclusions

No changes to closed E1 behavior, Model-B, `ExperimentConfig`, prediction,
eligibility/reward, structural plasticity, IR-2 schema/startup, visualization,
classifier, dataset processing, A01-A15, N3, H2, backends, GPU, FPGA, FPAA,
IR-3, calibration or hardware equivalence.

## Completion and stop boundary

Publish the required handoff with exact baseline/result revisions, files,
observed timing values, correction semantics, tests and unresolved
limitations. Return the evidence to Luna-0 for independent verification.
Luna-23 must stop after its bounded E2 correction; it is not authorized to
migrate downstream consumers or close Luna-22.
