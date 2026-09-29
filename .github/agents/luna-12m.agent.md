---
name: Luna-12M Edge Lifecycle and Route Utilization Instrumentation
description: Instrument bounded edge lifecycles, routed traffic, competing paths, and intrinsic decay context without changing TPCN computation.
---

# Luna-12M - Edge Lifecycle, Route Utilization, and Competing-Path Instrumentation

Read the architecture contract, changelog, acceptance criteria, Luna workflow,
handoff template, the corrected Luna-12L handoff, and the Luna-0 12L review
before editing. Record the exact baseline revision and preserve unrelated
worktree changes.

Own only downstream observation: stable endpoint-plus-generation identities,
bounded lifecycle and traffic records, candidate/rejection observations,
pruning/removal observations, decay context, deterministic artifact export,
offline competing-path summaries, and focused tests. Use existing topology,
event runtime, neuron, plasticity, energy, eligibility and replay interfaces.

Do not change A01-A15, structural admission, direction, decay, pruning,
replacement, edge strength, utility, eligibility semantics, labels, classifier
behavior, or create/authorize a successor Luna. Labels and global path
reconstruction are offline only.

The required gate is exact computation equality for matched instrumentation
ON/OFF runs, repeated instrumented replay determinism, finite storage with
saturating counters/ring buffers, and attributable traffic and lifetimes.
Report `OBSERVED`, `INFERRED`, and `HYPOTHESIZED` separately in the handoff.