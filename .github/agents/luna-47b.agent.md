---
name: Luna-47B Drive Accumulation Gain
description: Isolate input-to-accumulator gain adequacy using retained Luna-46 sequences.
---

# Luna-47B — Drive / Accumulation-Gain Adequacy

## Authorization and boundary

**AUTHORIZED / NOT EXECUTED.** This is an experimental-model mechanism
investigation only. Keep the production architecture and retained Luna-46
evidence unchanged. No production neuron, temporal decay, firing threshold,
topology, routing, ACP, or architecture change is permitted; no efficacy
claim is authorized.

The source/evidence baseline is repository revision
`2cef8ea4b37a4ae586e3f383511cba63c9268ddc`. Use the identical published
Luna-0 authorization revision recorded in
[`luna-0-authorization-luna47-20261006.md`](../../workflow/handoffs/luna-0-authorization-luna47-20261006.md),
a documentation-only descendant, as the common checkout base. Do not consume
another lane's unreviewed changes.

Read the architecture contract, changelog, Luna workflow, acceptance criteria,
proposal process, handoff template, this contract, and Luna-46 diagnostic
contract/handoffs/artifacts. Preserve the MIXED verdict and exact retained
sequence/category identities. Affected boundaries are A01-A03, A06-A08 and
A15; no clause is amended and no ACP is required.

## Objective

Test whether insufficient deposited excitation independently accounts for
Luna-46's drive-limited population. Hold temporal decay/state update
semantics, thresholds, topology and routing fixed. For already-qualified
meaningful input excursion `E`, vary only the experimental deposition gain:

```text
ΔA = g_A * E
```

Use the retained signed event stream and declared threshold. Derive the
critical gain for each applicable sequence analytically where possible before
choosing tested gains. Any gain sweep must bracket the derived boundary with
predeclared values; no threshold lowering, altered decay, amplitude increase,
or input relabeling is allowed.

## Files and isolation

Own only `experiments/luna47b/`, `artifacts/luna47b/`,
`tests/test_luna47b_*.py`, and
`workflow/handoffs/luna-47b-drive-accumulation-gain-20261006.md`.
Do not edit shared runtime, production neuron, topology, retained fixtures,
workflow, architecture, or another lane's files. Work in an isolated
branch/worktree from the common authorization revision.

## Required evidence and acceptance

Freeze and record event order, timestamps, retained temporal recurrence,
threshold, reset boundary, numerical tolerances and gain protocol before
analysis. Machine-readable records must include full per-event inputs/states,
per-sequence critical gain or a stated unbounded/no-crossing result,
configuration and fixture hashes, repository revision and replay metadata.

Report:

- critical gain required for threshold crossing per applicable sequence;
- count/fraction of drive-limited cases rescued at each tested gain;
- unintended crossings outside the target population;
- saturation, instability, sign/cancellation behavior and finite bounds;
- whether required gains plausibly map to ordinary resistor/current/capacitor
  scaling, with assumptions explicitly separated from measured circuit data.

Replay and tests must verify the baseline recurrence remains invariant,
critical-gain calculations against exact per-event trajectories, threshold
classification, determinism, finite behavior and reported count summaries.
The conclusion must answer whether insufficient deposited excitation is
independently responsible in this setup; distinguish a mathematical critical
gain from physical realizability. Negative and mixed outcomes are valid.

## Exclusions and handoff

No temporal-retention tuning, threshold changes, topology changes, production
integration, efficacy study, hardware build claim, architecture promotion, or
Luna-48 is authorized. Return a completed handoff and replayable artifacts,
push the isolated lane branch, and stop for independent Luna-0 review.
