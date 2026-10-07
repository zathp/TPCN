---
name: Luna-47C Adaptive Noise Qualification
description: Compare fixed and adaptive noise qualification on deterministic synthetic fixtures.
---

# Luna-47C — Adaptive Noise Qualification / Deadband

## Authorization and boundary

**AUTHORIZED / NOT EXECUTED.** This is an isolated input-qualification
experiment. It does not change production computation or implement a
temporal accumulator. No production neuron, topology, routing, ACP, or
architecture change and no efficacy claim are authorized.

Source/evidence baseline: `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
Checkout base for all lanes: the identical published Luna-0 authorization
revision recorded in
[`luna-0-authorization-luna47-20261006.md`](../../workflow/handoffs/luna-0-authorization-luna47-20261006.md),
a documentation-only descendant. Do not consume another lane's unreviewed
changes.

Read the architecture contract, changelog, workflow, acceptance criteria,
proposal process, handoff template, this contract and Luna-46 retained
diagnostic context. Affected boundaries: A01, A02, A07, A08 and A15. Global
evaluation may report results but must not feed a neural input. No A-clause
change or ACP is proposed.

## Objective

Represent three distinct signals:

```text
B(t) = baseline estimate
N(t) = noise-envelope estimate
E(t) = meaningful excess admitted beyond the noise band
```

On deterministic synthetic fixtures compare, at minimum:

1. fixed deadband;
2. adaptive noise-envelope deadband;
3. clipped/robust adaptive estimator that prevents large meaningful spikes
   from strongly inflating their own future rejection threshold.

The lane returns qualified excitation events/values only. Do not couple it
to, consume, or tune Luna-47A's WEMA/accumulator.

Fixtures must include stationary noise, slowly drifting baseline, isolated
real excursions, clustered real excursions, mixed signs, and amplitudes near
the noise boundary. Freeze generation, labels/ground truth, parameters,
initialization, reset behavior, event times and scoring rules before running.
Keep any truth labels in the evaluator, never in the qualifier input.

## Files and isolation

Own only `experiments/luna47c/`, `artifacts/luna47c/`,
`tests/test_luna47c_*.py`, and
`workflow/handoffs/luna-47c-adaptive-noise-qualification-20261006.md`.
Do not edit shared runtime, production neuron, topology, common fixtures,
workflow, architecture, or another lane's files. Use an isolated
branch/worktree from the common authorization revision.

## Required evidence and acceptance

For every fixture and method report false admissions, missed meaningful
excursions, baseline pull, noise-estimator contamination, recovery time, and
positive/negative sign symmetry. Explicitly test the failure chain:

```text
meaningful spike -> inflated noise estimate -> later meaningful spikes suppressed
```

Include event-level `B`, `N`, raw input and `E` outputs with timestamps,
method configuration, fixture identity/hash, repository revision, and
deterministic replay metadata. State numerical comparisons and tolerances
before interpretation. Tests cover fixture coverage, no label access by the
qualifier, determinism, bounded state, sign behavior and the contamination
failure mode. Explain tradeoffs without selecting a winner on a single
aggregate score.

## Exclusions and handoff

No WEMA/accumulator implementation or tuning, production integration,
topology mutation, efficacy, architecture promotion, or Luna-48 is
authorized. Return a completed handoff and machine-readable replay package,
push the lane branch, then stop for independent Luna-0 review.
