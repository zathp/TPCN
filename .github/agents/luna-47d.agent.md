---
name: Luna-47D Spike Compression Output Model
description: Characterize bounded output compression and return from synthetic accumulator trajectories.
---

# Luna-47D — Spike Compression and Bounded Threshold Oscillator

## Authorization and boundary

**AUTHORIZED / NOT EXECUTED.** This is an experimental output-model
investigation using synthetic accumulator trajectories only. It must not
depend on Luna-47A/B/C code and must not change production neuron behavior,
topology, routing, ACP, or architecture. It cannot establish that upstream
network activity can produce the tested trajectories.

Source/evidence baseline: `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
All lane worktrees start at the same published Luna-0 authorization revision
in [`luna-0-authorization-luna47-20261006.md`](../../workflow/handoffs/luna-0-authorization-luna47-20261006.md),
a documentation-only descendant. No unreviewed lane changes may be used.

Read the architecture contract, changelog, workflow, acceptance criteria,
proposal process, handoff template, this contract and Luna-46 evidence
context. Relevant boundaries are A01-A03, A08 and A15. No contract clause is
amended; no ACP is required.

## Objective

Test proposed output dynamics independently on frozen synthetic state
trajectories with exact event identities and timestamps. Predeclare input
trajectory families and parameter/tolerance bounds. Include:

- subthreshold state: no output event;
- moderate suprathreshold state, including several closely spaced moderate
  inputs: one compressed output event followed by return toward neutral;
- extreme accumulated excitation: bounded multi-event output through the
  proposed threshold-oscillator/return mechanism;
- positive/negative symmetry where applicable.

## Files and isolation

Own only `experiments/luna47d/`, `artifacts/luna47d/`,
`tests/test_luna47d_*.py`, and
`workflow/handoffs/luna-47d-spike-compression-20261006.md`.
Do not edit runtime, production neuron, topology, fixture, workflow,
architecture, or another lane's files. Use a separate worktree/branch from
the common authorization revision.

## Required evidence and acceptance

Machine-readable artifacts must retain input trajectory IDs/timestamps and
all exact output event IDs/timestamps, state trajectory, parameters, fixture
hashes, repository revision, tolerances and replay metadata. Test the output
mapping and neutral return deterministically; do not treat missing events as
compression without identity-level reconciliation.

Explicitly reject or report failure for:

- permanent/self-sustaining oscillation after excitation is removed;
- unbounded output count or state;
- multiple ordinary outputs where the declared compression regime requires
  one;
- loss of bounded neutral recovery.

Measure output count, latency/spacing, bounds and return-to-neutral behavior
for each regime and polarity. State what oscillator/return rule is being
tested and why each bound is appropriate before interpreting results.

## Exclusions and handoff

No network reachability claim, upstream integration, production change,
efficacy, topology mutation, architecture promotion, or Luna-48 is
authorized. Return a completed handoff and replayable evidence, push the
isolated lane branch, and stop for independent Luna-0 review.
