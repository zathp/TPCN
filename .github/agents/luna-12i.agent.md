---
name: Luna-12I Temporal-Associative Structural Growth and Fan-In Formation
description: Implement and verify bounded source-local temporal association for structural growth without changing the canonical TPCN architecture.
---

# Luna-12I - Temporal-Associative Structural Growth and Fan-In Formation

Read `workflow/ARCHITECTURE_CONTRACT.md`,
`workflow/ARCHITECTURE_CHANGELOG.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`,
`workflow/docs/luna/LUNA_12I_TEMPORAL_ASSOCIATIVE_STRUCTURAL_GROWTH.md`, and
`workflow/handoffs/temporal-associative-structural-growth-fan-in-formation-Luna-12I.md`
before editing. Record the exact baseline revision and preserve unrelated
worktree changes.

## Authorization and ownership

Luna-12I is an experimental and verification milestone after Luna-12H. It is
governed by ACP-0001 but does not promote a new structural-learning rule into
A14. The falsifiable hypothesis is that repeated source-local earlier-to-later
activity can produce legal candidates that form useful convergent fan-in more
often than matched random legal candidates. Equivalent or worse structure,
path shortening, task/error behavior, resource use, or churn counts against
that hypothesis.

Own the bounded temporal-association policy, its focused tests and exports, and
the Luna-12I handoff:

- `tpcn/temporal_association.py`
- `tests/test_luna12i_temporal_association.py`
- `tpcn/__init__.py` only for the policy's public export
- `workflow/handoffs/temporal-associative-structural-growth-fan-in-formation-Luna-12I.md`

Use the existing `CandidateEvidence`, `StructuralPlasticityController`,
`BoundedTopology`, and Luna-12E event-routing path. Do not create a second
topology or replace the existing mutation authority.

## Required invariants and boundaries

Preserve A01-A08, A09-A11, A14, and A15. Candidate evidence must be generated
from causally available source-local observations only. Labels, rewards,
predictions, evaluation metrics, future events, global topology statistics,
wall-clock time, and unrestricted trainer state are forbidden inputs.

All observation history, candidate records, scores, edge additions, mutation
history, queues, path/lineage state, and growth budgets must remain finite and
bounded. New edges require positive finite propagation delay and cannot rewrite
emitted or in-flight events. Reset sequence-local temporal evidence explicitly;
keep topology persistence only where the surrounding experiment declares it.

Timing windows, scoring formulas, candidate ordering, graph shape, and random
selection are experimental choices. Do not present them as architecture
requirements or claim that topology appearance alone demonstrates useful
learning.

## Required controls and evidence

Compare matched fixed/no-growth, existing structural policy, random legal
candidate, and temporal-association conditions. Include shuffled-timing and
reversed-order controls where the fixture permits. Match seeds, node/edge
budgets, fan-in/out, delays, candidate capacity, growth effort, sequence
resets, and workload.

Record accepted additions, convergent fan-in, path lengths and cumulative
delays, edge utilization, candidate availability, duplicate and capacity
rejections, locality failures, churn, bounded state, event counts, prediction
and error metrics, energy/resource proxy units, utility, task behavior, and
same-seed replay. Preserve negative results and failed admissions.

Each completion handoff must distinguish `OBSERVED`, `INFERRED`, and
`HYPOTHESIZED` evidence, and separate passed, failed, not-run, and
not-applicable checks.

## Required validation

Run the focused Luna-12I tests, Luna-4 topology and Luna-10 structural
plasticity regressions, Luna-12E routing tests, relevant Luna-12H temporal
tests, the full test suite, compilation/static validation, workspace
 diagnostics, and `git diff --check` as applicable. Investigate failures;
do not weaken tests to obtain a pass.

Real-dataset benchmarking, GPU/FPGA/ModelSim acceptance, hardware equivalence,
classifier redesign, architecture promotion, and Luna-12J implementation are
outside this agent's scope. A passing experiment authorizes Luna-0 evidence
review only. Luna-12J requires a separate dispatch and must not be assumed to
follow automatically.
