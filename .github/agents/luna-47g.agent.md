---
name: Luna-47G Analog Variation Robustness
description: Simulate qualitative neuron behavior under bounded component mismatch and noise.
---

# Luna-47G — Analog Component Tolerance and Mismatch Robustness

## Authorization and boundary

**AUTHORIZED / NOT EXECUTED.** Simulation/evidence only; not a hardware
feasibility demonstration. Keep production neuron behavior and topology
unchanged. No ACP, architecture promotion or efficacy claim is authorized.

Source/evidence baseline: `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
Use the common published Luna-0 authorization revision recorded in
[`luna-0-authorization-luna47-20261006.md`](../../workflow/handoffs/luna-0-authorization-luna47-20261006.md),
a documentation-only descendant. Do not consume another lane's unreviewed
changes. Read-only, published Luna-47E part/tolerance findings may be
incorporated if available before this lane starts; otherwise declare
assumptions and any missing-component dependency, without waiting for or
merging an unreviewed implementation.

Read the architecture contract, changelog, workflow, acceptance criteria,
proposal process, handoff template, this contract and Luna-46 context.
Relevant boundaries: A01-A04, A08, A09 and A15. No A-clause change or ACP is
proposed.

## Objective

Perturb experimental parameters corresponding to resistance, capacitance,
gain, comparator threshold/offset, leakage and input noise over multiple
predeclared tolerance bands. Use component specifications from Luna-47E
where available; otherwise state the assumed distributions/ranges and their
limits. Do not imply mathematical sampling establishes real-hardware
feasibility.

The primary qualitative invariant is:

```text
ordinary noise rejected
-> meaningful excursions admitted
-> nearby meaningful inputs accumulate
-> moderate accumulated excitation compresses
-> extreme excitation produces bounded multi-event return
-> state returns toward neutral
```

## Files and isolation

Own only `experiments/luna47g/`, `artifacts/luna47g/`,
`tests/test_luna47g_*.py`, and
`workflow/handoffs/luna-47g-analog-robustness-20261006.md`.
Do not edit runtime, production neuron, topology, common fixtures, shared
workflow, architecture files, or another lane's files. Use an isolated
branch/worktree from the common authorization revision.

## Required evidence and acceptance

Predeclare tolerance bands, distributions, correlations, random seeds,
sample counts, model equations, numerical tolerances, and qualitative
pass/fail definitions. Use deterministic, replayable sampling and preserve
per-sample parameter draws and outcomes in machine-readable artifacts with
revision, configuration and fixture hashes.

Report transition failures, sensitivity ranking, parameter interactions,
per-band failure fractions and uncertainty/coverage limits. Identify blocks
requiring tighter selection or calibration. Verify bounded state/output,
symmetry where applicable, and return-to-neutral behavior. Compare the
observed sequence of regimes against the predeclared invariant; do not hide
failures in aggregate averages.

## Exclusions and handoff

No physical hardware test, hardware-feasibility claim, production integration,
topology mutation, efficacy, architecture promotion or Luna-48 is authorized.
Return a completed handoff and replayable parameter/outcome data, push the
isolated lane branch, and stop for independent Luna-0 review.
