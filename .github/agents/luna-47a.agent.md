---
name: Luna-47A WEMA Temporal Retention
description: Isolate event-time leaky accumulation as a temporal-retention mechanism experiment.
---

# Luna-47A — WEMA / Temporal Retention

## Authorization and boundary

**AUTHORIZED / NOT EXECUTED.** This is an experimental-model mechanism
investigation only. The production architecture and retained Luna-46 evidence
are the baseline; no production neuron, threshold, weights, topology, routing,
ACP, or architecture contract may be changed. No efficacy or hardware claim
is authorized.

The source/evidence baseline is repository revision
`2cef8ea4b37a4ae586e3f383511cba63c9268ddc`. Dispatch must use the identical
published Luna-0 authorization revision recorded in
[`luna-0-authorization-luna47-20261006.md`](../../workflow/handoffs/luna-0-authorization-luna47-20261006.md),
which is a documentation-only descendant of that baseline. No lane may
consume another lane's unreviewed code or artifacts.

Read the architecture contract, changelog, Luna workflow, acceptance criteria,
proposal process, handoff template, this contract, and the Luna-46 diagnostic
contract and retained handoffs/artifacts before execution. Preserve Luna-46's
MIXED verdict and its category definitions; do not reinterpret the result.
Affected clauses: A01, A02, A06, A08 and A15 are relevant boundaries, not
proposed amendments. An ACP is not required for this isolated experiment.

## Objective

Test whether an explicitly defined WEMA-like or equivalent continuous-time
leaky accumulator retains temporally separated meaningful excitation enough
to address Luna-46 retention-limited cases, while separately tracking
drive-limited sequences.

Keep the stages conceptually distinct:

1. baseline estimation;
2. noise qualification (use a frozen/pass-through qualified input stream for
   this lane; do not implement or tune a new noise gate);
3. meaningful-excitation accumulation.

Compare current temporal-state behavior with one or more declared
WEMA/leaky-accumulator variants using the exact event timestamps. For
continuous-time variants, analytically relax state between events. A discrete
WEMA approximation is permitted only if its behavior is shown equivalent to
its declared continuous-time target within a predeclared numerical tolerance.
No global neural timestep may be introduced.

## Files and isolation

Own only `experiments/luna47a/`, `artifacts/luna47a/`,
`tests/test_luna47a_*.py`, and
`workflow/handoffs/luna-47a-wema-temporal-retention-20261006.md`.
Do not edit shared runtime, production neuron, topology, fixture, workflow,
architecture, or another lane's files. Use a separate branch/worktree rooted
at the common authorization revision.

## Required evidence and acceptance

Predeclare the accumulator equations/parameters, reset boundary, units,
event ordering, numerical tolerances, and comparison protocol before
interpretation. Retain machine-readable inputs, per-event outputs, and
configuration with repository revision, configuration/fixture identities
and hashes, and software/environment metadata sufficient for replay.

Measure per relevant reception:

- retained state before and after the event, elapsed time and decay factor;
- signed state and threshold margin at every relevant reception;
- retention-limited sequences made representable/crossing and
  drive-limited sequences that remain so;
- changes to historical behavior outside the target diagnostic;
- boundedness and numerical stability, including extreme supported event
  spacing and values.

Do not count input-amplitude increases, threshold changes, weight changes,
topology changes or output changes as WEMA success. Preserve sequence
identities and distinguish observed results from inference. Tests must cover
the declared recurrence, event-time semantics, replay determinism, bounds,
and tolerance against any continuous-time target. Classify the outcome as
**SUPPORTED**, **PARTIALLY SUPPORTED**, **NOT SUPPORTED**, or **BLOCKED**,
with explicit evidence-based criteria and counts.

## Exclusions and handoff

No task-efficacy run, parameter search beyond the predeclared accumulator
variants, neuron/output integration, topology mutation, architecture
promotion, or Luna-48 is authorized. Return a completed handoff, replayable
artifacts, exact commands/results, known baseline failures if tested, and a
recommendation limited to what this mechanism evidence supports. Push the
lane branch/artifacts, then stop for independent Luna-0 review.
