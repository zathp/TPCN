---
name: Luna-12H Intrinsic Temporal State, Recurrence, and Unequal-Delay Convergence
description: Implement and verify bounded intrinsic temporal state, recurrent event routing, and unequal-delay convergence without a global neural timestep.
---

# Luna-12H - Intrinsic Temporal State, Recurrence, and Unequal-Delay Convergence

Read `workflow/ARCHITECTURE_CONTRACT.md`,
`workflow/ARCHITECTURE_CHANGELOG.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`,
`workflow/docs/luna/LUNA_12H_TEMPORAL_STATE_RECURRENCE.md`, and the accepted
`workflow/handoffs/spiral-handedness-temporal-classification-Luna-12G.md`
before editing. Record the exact baseline revision and preserve unrelated
worktree changes.

## Authorization and ownership

Luna-12H is authorized by Luna-0 after the Luna-12G temporal-order limitation.
Own the canonical neuron temporal-state behavior, focused event-routing
fixtures/tests, bounded recurrence checks, timing/reset diagnostics, and
`workflow/handoffs/intrinsic-temporal-state-recurrence-unequal-delay-convergence-Luna-12H.md`.
No ACP is required unless implementation discovers that the requested
semantics cannot be expressed by the existing A01-A15 contract. Do not claim
an ACP or architecture promotion without Luna-0 review.

## Required behavior

Verify both intrinsic local temporal state and network/path temporal state.
State evolution may depend on state before the event, incoming event, and
elapsed local time. A single event must persist observably before reset, and
at least one deterministic ordered-pair fixture must be noncommutative.
Use event timestamps/local time; do not add a global neural timestep, whole-
network stepping, or hidden recurrent tick. An analytic event-time decay is
preferred over invented autonomous events.

Use bounded finite routing with direct and multi-hop paths of unequal
cumulative delay. Preserve timestamps and deterministic fan-in tie ordering.
Verify older long-path and newer short-path consequences can converge and
change downstream state/output according to relative arrival timing. Cycles
must terminate under existing event, lineage/path, queue, state and topology
bounds. Pruning a path must remove its future effect.

Keep temporal state within declared character/sequence reset boundaries,
allow topology retention only where explicitly configured, and keep labels and
future points outside neural events, predictor state, routing, topology,
energy, and error computation. Do not hard-code spiral handedness or redesign
the external readout before core temporal evidence exists.

## Required fixtures and validation

Run the twelve Luna-12H acceptance checks, including single-spike persistence,
ordered-pair and equal-multiset/different-order distinction, changed interval,
unequal direct/multi-hop delay, convergent old/new arrival, path pruning,
different-arrival timing, reset, same-seed determinism, bounded recurrence, and
label isolation. Record time units, decay/evolution rule, capacities, queue
policy, tie policy, path delays, seeds, traces, and exact commands.

Run focused Luna-12H tests, Luna-12E causal-routing regressions, relevant
canonical-neuron/runtime/topology/predictive tests, full pytest, compile,
workspace diagnostics, and `git diff --check` as applicable. Separate passed,
failed, not-run and not-applicable checks. Report absence of temporal effect as
evidence, not as a reason to add a classifier shortcut. Return control to
Luna-0 with an explicit integration-readiness decision.
