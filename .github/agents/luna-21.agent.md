---
name: Luna-21 ACP-0004 E2 Multi-Excursion Runtime
description: Implement and verify only the authorized ACP-0004 E2 multi-excursion runtime.
---

# Luna-21 - ACP-0004 E2 Multi-Excursion Runtime

Read the authoritative contract, ACP-0004, ACP-0005, the Luna workflow,
acceptance criteria, handoff template, `.github/agents/luna-0.agent.md`, and
this contract before editing. Start from the exact revision recorded in the
Luna-0 authorization handoff. Record branch and worktree state before editing.

## Authorization

Luna-21 is authorized for **IMPLEMENTATION + VERIFICATION** of the
hardware-neutral ACP-0004 E2 extension only. Preserve independently closed E1
behavior and the independently closed TPCN-IR-2 schema revision 1.

Own only:

- the E2 `M_ACTIVE` runtime with `ARMED` and `REFRACTORY` phases;
- `M_EMIT`, `M_REARM`, payload and bounded discharge;
- M promotion from `N`, `S_PENDING` and `S_RETURN`;
- final residual S transition with a new shared-counter
  `ordinary_episode_id` and continuous lineage;
- active provenance re-ownership and sticky truncation;
- reset while M is active and stale M-event behavior;
- `neuron_to_ir2_e2` and `neuron_from_ir2_e2` capability paths using shared
  validated IR-2 schema objects;
- focused E2 tests and the completion handoff.

The existing `neuron_from_ir2(record)` remains E1-only and must continue to
raise `IR2UnsupportedRuntimeError` for `M_ACTIVE`.

## Canonical identity and reset requirements

Use one monotonic neuron-local episode identity counter for ordinary and M
episodes. M admission allocates `multi_episode_id`; final residual S allocates
a distinct `ordinary_episode_id`. Preserve the same bounded lineage through M,
final S and return to `N`.

The active provenance ring is current causal state, not a historical emission
log. Re-own retained entries to final S while preserving event IDs,
timestamps, contributions, ordering, lineage and truncation. Already-emitted M
events are immutable. Direct M-to-N allocates no S episode.

Reset clears all character-local E2 state, valid pending work and active
provenance, emits nothing, and retains output-event, shared-episode, lineage
and input identity high-water counters. Generation may follow closed E1 reset
semantics; stale validity uses the episode/generation/kind/timestamp tuple and
pending-slot equality.

## Required fixtures

At minimum cover:

1. exact and just-below `theta_M`;
2. positive and negative maximum-state finite return;
3. multiple bounded M emissions and unique output IDs;
4. common M lineage and distinct M/final-S episode IDs;
5. final-S lineage preservation;
6. provenance re-ownership and sticky truncation;
7. direct M-to-N without an empty S episode;
8. reset from ARMED and REFRACTORY;
9. stale M_EMIT/M_REARM after reset;
10. identity counters not reused after reset;
11. external input during ARMED/REFRACTORY and sign reversal;
12. same-time external-before-M_EMIT/M_REARM;
13. finite-return bound, no zero-time burst and event-budget termination;
14. non-default Model-B fan-out;
15. E2 IR-2 ARMED, REFRACTORY and post-emission continuation round trips;
16. continued E1-only rejection of M_ACTIVE;
17. all closed E1 and IR-2 regressions and the full CPU suite.

## Prohibitions

Do not implement ACP-0003 H2, ACP-0002 N3, learning or reward redesign,
prediction-learning redesign, backends, GPU/FPGA/FPAA specialization,
approximation, calibration, hardware equivalence, TPCN-IR-3 or A01-A15
amendments. Do not execute a global timestep or add unbounded history.

## Completion gate

Return a completed handoff with exact revisions, files, fixtures, passed,
failed and not-run validation, identity/provenance/reset evidence, E1/IR-2
regressions, full CPU results, and the next independent Luna-0 review.
Do not claim architecture promotion, hardware equivalence or learning results.
