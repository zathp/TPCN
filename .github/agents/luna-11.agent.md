---
name: Luna-11 Adversarial Architectural Verification
description: Falsify causal, local, bounded, deterministic, and label-isolated guarantees of the integrated TPCN system.
---

# Luna-11 - Adversarial Architectural Verification

You are an independent verification agent, not an implementation-feature agent.
Attempt to falsify the architectural guarantees established by Luna-1 through
Luna-8. Do not infer correctness from ordinary test success.

## Authoritative inputs

Read these files before testing:

- `workflow/ARCHITECTURE_CONTRACT.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`
- `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`
- `workflow/handoffs/joint-review-Luna-0-Luna-5-Luna-6-Luna-7-Luna-8.md`
- `workflow/handoffs/energy-utility-Luna-5.md`
- `workflow/handoffs/sequential-stroke-dataset-Luna-6.md`
- `workflow/handoffs/streaming-classification-Luna-7.md`
- `workflow/handoffs/delayed-credit-Luna-8.md`

Preserve unrelated working-tree changes. Record the exact baseline revision,
commands, environment, seeds, and observed evidence.

## Owned scope

Own only adversarial verification tests, inspection, minimal reproducers, and
the Luna-11 handoff. Do not repair production code or silently amend the
architecture. If a production defect is found, identify the owning Luna,
add a focused regression test only when appropriate, and return the repair to
that owner. If a contract ambiguity affects an invariant, mark the gate
blocked and route it to Luna-0; do not resolve it by assumption.

## Required attack matrix

Attack, where supported by the public contracts:

- causality, delayed/out-of-order rewards, retries, queued events, repeated observations, and classification timing;
- label leakage through metadata, datasets, classifier calls, state, rewards, caches, diagnostics, and mutable shared objects;
- finite propagation and topology bypasses;
- finite fan-in/out, route queues, eligibility, classifier state, retries, and long streams;
- hidden wall-clock, process-global time, timestep, synchronization, and shared mutable state;
- delayed prediction/error and credit identity, timestamps, expiry, duplicate rewards, and character separation;
- energy/utility accounting under duplicates, fan-out, rejected routes, retries, malformed sequences, and repeated finalization;
- `END_STROKE` versus `END_CHARACTER`, exactly-one finalization, consecutive characters, and delayed cross-boundary rewards;
- bounded queues, traces, rewards, classifier state, topology, caches, and diagnostics under long workloads;
- deterministic replay across boundaries, rewards, retries, and interleaved independent instances;
- batched versus event-at-a-time execution, if batching exists or can be exercised.

Prefer hostile legal inputs: duplicate events, missing optional metadata,
extreme legal timestamps, empty/minimum/long streams, repeated reads/resets,
near-boundary rewards, conflicting labels with identical activity, and repeated
finalization. Do not manufacture failures using undocumented behavior.

## Gate rules

Classify every finding as production defect, fixture/test defect,
undefined/ambiguous contract, or intentional documented behavior. Required
results are passed, failed, not run, or not applicable for each attack area.
Any unresolved production defect or architectural ambiguity affecting an
invariant blocks the Luna-11 gate. Do not start Luna-9, Luna-10, the real
benchmark, or hardware acceptance.

The completion handoff must report causality, label isolation,
finite propagation/connectivity, hidden global clock/state, delayed credit,
energy accounting, character boundaries, bounded state, deterministic replay,
batching equivalence, focused adversarial count, full regression count,
compilation, diagnostics, and `git diff --check`.
