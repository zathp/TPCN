---
name: Luna-36 EXCURSION Runtime Eligibility Capacity Configuration
description: Add a bounded, backward-compatible per-ledger eligibility-capacity option to the EXCURSION runtime without changing lifecycle semantics or running efficacy/mechanism experiments.
---

# Luna-36 — EXCURSION Runtime Eligibility Capacity Configuration

## Authorization and baseline

```text
Luna-0 -> Luna-36 -> Luna-0
```

Luna-36 is **AUTHORIZED / NOT EXECUTED** by the independent post-Luna-35
review in
`workflow/handoffs/luna-0-independent-review-luna35-eligibility-capacity-20261004.md`.
The authorization baseline is the published Luna-0 review revision recorded
in that handoff. Verify a clean `main` synchronized with `origin/main` before
implementation and record the exact execution baseline.

This is a compatible **PUBLIC RUNTIME CONFIGURATION** change only. This
contract does not authorize a Luna-34 retry, a propagation-to-emission
experiment, task efficacy, or an architecture change. Return the API
implementation and tests to Luna-0. No subsequent Luna is authorized here.

## Observed problem and primary hypothesis

The integrated `ExcursionCharacterRuntime.start_character()` currently
constructs one `EligibilityLedger` per node with:

```text
max_traces = prediction_capacity * max(1, neuron_count)
```

Luna-35 independently confirmed that with two nodes and
`prediction_capacity=8`, the fixed no-edge `c00-004` workload fills the
16-entry source ledger at its sixteenth eligibility creation and rejects the
seventeenth. Predictor expiry does not retire eligibility, and automatic
retirement on predictor expiry would break the supported delayed-credit path.
The runtime constructor has no independent control for the per-ledger trace
bound. Therefore a caller cannot declare a different finite eligibility
capacity while preserving the independent prediction capacity.

**H1:** An optional explicit per-ledger eligibility-capacity setting can be
added while the omitted/default setting preserves the exact existing derived
capacity and all existing lifecycle behavior.

**Counter-hypothesis:** The optional setting cannot be threaded through every
runtime construction path without changing default behavior, accepting
invalid/unbounded state, or breaking existing callers.

## Authorized interface change

Add an optional keyword-only `eligibility_capacity: int | None = None` to
`ExcursionCharacterRuntime` construction and
`ExcursionCharacterRuntime.from_quiescent_ir2()`.

- `None` means the existing rule exactly:
  `prediction_capacity * max(1, len(neurons))`.
- A supplied value is a positive integer **per ledger**, used unchanged for
  each node's `EligibilityLedger.max_traces`.
- Reject `bool`, non-integers, zero, and negative values with the repository's
  established validation style.
- Expose the effective positive integer as a read-only runtime property named
  `eligibility_capacity`, including when the caller omits the argument.
- `from_quiescent_ir2()` must preserve the same default and forward an
  explicit value.
- The setting must not affect predictor `max_outstanding`, predictor
  expiration, eligibility expiration, trace creation/decay/credit/removal,
  rewards, prediction errors, neurons, routing, reset, or event ordering.
- Do not add capacity resizing or mutation after character startup.

The optional argument must preserve all existing call sites and serialized
IR-2 schemas. Do not add the setting to IR-2 records or serialized experiment
formats in this assignment.

## Exact owned files

Luna-36 may add/change only:

```text
tpcn/experiment_excursion_runtime.py
tests/test_luna36_eligibility_capacity_api.py
workflow/handoffs/luna-36-runtime-eligibility-capacity-configuration-20261004.md
```

Do not edit eligibility ledger semantics, prediction/reward behavior,
`ExperimentRunner`, experiment configurations, Luna-34 or Luna-35 code and
artifacts, ACP files, Architecture Contract, workflow, changelog, Luna-33
evidence, or the post-Luna-35 review handoff. Do not create experiment
artifacts or modify dependency manifests.

## Required tests

Use focused tests to demonstrate:

1. With the argument omitted, the effective property and every created
   ledger retain the legacy formula for one-node and two-node networks.
2. An explicit small positive per-ledger value is exposed and applied
   identically to every node without changing `prediction_capacity`.
3. Invalid explicit values (`True`, non-integer, zero, and negative) fail
   explicitly at runtime construction.
4. `from_quiescent_ir2()` preserves the legacy default and forwards the
   explicit value.
5. Existing runtime inputs/results, reward and prediction-error behavior,
   deterministic replay, reset, and eligibility overflow behavior remain
   unchanged when the option is omitted.
6. No caller breakage, serialization change, production eligibility
   retirement, predictor-expiry coupling, or event-order change is introduced.

Do not feed the Luna-34 `c00-004` sequence to an explicit non-default
capacity. Do not choose a capacity based on a desired experimental outcome.
These are API compatibility tests, not an experiment.

## Stop conditions

Stop and return to Luna-0 if:

- preserving the old default requires changing `prediction_capacity`
  semantics or eligibility lifecycle behavior;
- an explicit capacity cannot remain finite and positive;
- a change outside the owned files is necessary;
- the API requires an ACP or changes architecture semantics; or
- existing compatibility/regression tests fail after focused investigation.

Do not broaden scope to fix overflow, tune limits, modify retention, or run
the propagation diagnostic.

## Prohibited conclusions

Luna-36 must not claim:

- that any eligibility capacity is generally sufficient for all workloads;
- that predictor expiration should retire eligibility;
- a production lifecycle defect or architecture defect;
- any Luna-34 edge-condition or propagation-to-emission result;
- ACP-0007 candidate formation or efficacy;
- an accuracy, prediction-benefit, resource-benefit, structural-growth, or
  hardware-equivalence result.

## Validation and completion

Run the focused Luna-36 API tests, `tests/test_excursion_integration.py`,
`tests/test_eligibility.py`, `tests/test_predictive_coding.py`, the full
repository suite, Python compilation, and `git diff --check`. Preserve exact
skip reasons and report default/explicit capacities, compatibility facts,
tests and unresolved questions.

Produce a completed handoff using
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`. Commit and push only the
authorized files, verify `HEAD == origin/main` and a clean worktree, and
return to Luna-0. This authorization does not authorize or imply any
propagation-to-emission rerun, Luna-37, or a later task.
