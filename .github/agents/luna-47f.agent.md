---
name: Luna-47F Fan-In Shortcut Candidate Diagnostic
description: Replay retained evidence to evaluate bounded shortcut/fan-in candidate opportunities without topology mutation.
---

# Luna-47F — Fan-In / Shortcut Candidate-Generation Diagnostic

## Authorization and boundary

**AUTHORIZED / NOT EXECUTED.** Replay-only diagnostic; no topology mutation.
No edge may be created, removed, admitted, reprioritized or used for a
counterfactual production run. No production, ACP, or architecture change and
no efficacy claim are authorized.

Source/evidence baseline: `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
Use the identical published Luna-0 authorization revision recorded in
[`luna-0-authorization-luna47-20261006.md`](../../workflow/handoffs/luna-0-authorization-luna47-20261006.md),
a documentation-only descendant. Preserve Luna-46 MIXED and all source
provenance; do not consume another lane's unreviewed changes.

Read the architecture contract, changelog, workflow, acceptance criteria,
proposal process, handoff template, this contract, Luna-46/12-series
applicable handoffs, and retained candidate/replay evidence. Relevant
boundaries: A01-A04, A07, A08 and A14. No A-clause change or ACP is proposed.

## Objective

Replay retained traces and evaluate the candidate-generation hypothesis:
when two relevant nodes show compatible causal deltas within a short
temporal relationship, preferentially *propose* a connection directed from
the earlier causal structure toward the later one. Determine whether this
creates useful candidate opportunities for path shortening and fan-in
before any topology mutation is separately considered.

Predeclare delta-compatibility and temporal-window rules from the available
trace units before scoring. If the retained evidence cannot support a rule,
report the specific dependency/blocker; do not generate synthetic evidence
and present it as retained replay.

## Files and isolation

Own only `experiments/luna47f/`, `artifacts/luna47f/`,
`tests/test_luna47f_*.py`, and
`workflow/handoffs/luna-47f-candidate-generation-diagnostic-20261006.md`.
Do not edit production or topology code, source fixtures, shared workflow,
architecture files or another lane's files. Use an isolated branch/worktree
from the common authorization revision.

## Required evidence and acceptance

Record machine-readable candidate rows and source trace identities/hashes,
repository revision, configuration, scoring/window rules, and replay
environment. Capture at minimum:

- total candidate opportunities and candidate timing;
- source/target identities, causal ordering and delta similarity;
- predicted shortcut length reduction;
- fan-in creation opportunity count (not actual creation);
- duplicate candidates, cycle-forming candidates and candidates into
  already-saturated connection sets;
- temporal specificity and association with useful downstream activity.

Count-only positivity is not efficacy. Reconcile every candidate to retained
causal observations, distinguish opportunity from usable/reachable edge,
and state capacity information limits. Tests must assert replay determinism,
causal direction, duplicate/cycle/saturation classifications and strict
non-mutation. Record pre/post hashes or equivalent evidence proving no
topology artifacts changed.

## Exclusions and handoff

No graph changes, admissions, topology policy change, task efficacy,
architecture promotion or Luna-48 is authorized. Return a completed handoff
and replayable diagnostics, push the isolated lane branch, and stop for
independent Luna-0 review.
