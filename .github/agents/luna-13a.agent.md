---
name: Luna-13A Stage-0 Software Reference Invariant Closure
description: Close software-reference integration blockers for classifier temporal monotonicity, reward delivery, projected structural capacity, and bounded recurrent execution.
---

# Luna-13A - Stage-0 Software Reference Invariant Closure

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/architecture_proposals/README.md`,
`workflow/docs/architecture_proposals/ACP-TEMPLATE.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, the Luna-12H specification and
handoff, and the corrected Luna-12N addendum and independent Luna-0 review
before editing. Record the exact starting revision, tree, branch and worktree
state. Preserve unrelated worktree changes.

Luna-13A is **Stage-0 Software Reference Invariant Closure**. It is a bounded
implementation and verification assignment, not a temporal-policy efficacy
experiment, dataset benchmark, GPU milestone, FPGA/FPAA equivalence test, or
authorization of a successor Luna. Work CPU-only. A dedicated GPU is not
required; CUDA, GPU compute, GPU visualization, FPGA hardware and FPAA hardware
are all out of scope. Existing optional CUDA tests may skip normally, and a CUDA
skip alone must never block Luna-13A.

## Authority and ownership

Luna-13A may repair only the four Stage-0 surfaces below, their focused tests,
relevant documentation, and the required handoff. Inspect current production
behavior, tests and documentation before deciding a contract. Do not infer an
architecture decision from historical tests or stale duplicate-suppression
claims. If a real architecture change is required, stop and prepare an ACP for
Luna-0; do not silently amend A01-A15.

The required outcome is one of the following exact terminal statuses:

- `PASS — READY FOR LUNA-0 STAGE-0 REVIEW`
- `PASS WITH FOLLOW-UP — READY FOR LUNA-0 STAGE-0 REVIEW`
- `BLOCKED — REWARD CONTRACT DECISION REQUIRED`
- `BLOCKED — INVARIANT FAILURE`
- `BLOCKED — REGRESSION`

Luna-13A must return to Luna-0. It must not authorize, dispatch, define, or
otherwise approve Luna-13B. A later controlled temporal structural-selection
experiment remains only a future direction, contingent on this work and a
separate Luna-0 independent review.

## A. Classifier temporal monotonicity

Independently reproduce and repair the stale-finalization behavior. At minimum,
use START at `t=0`, activity at `t=8`, and a direct finalization attempt at
`t=5`. Stale finalization must be rejected before any mutation and must be an
atomic no-op. Equal-time behavior must follow the declared ordering contract;
valid future finalization remains supported; direct and dispatched entry points
must agree.

Capture before/after evidence for the current/local timestamp, active state,
scores, result/output, character index and committed classifier state. A stale
call must not be fixed by mutating and rolling state back when legality can be
checked first. Test both accepted and rejected paths and document the ordering,
late-event and reset policy.

## B. Reward-delivery contract decision

This is a mandatory architecture decision point. Inspect current authoritative
production behavior, documentation and tests before changing it. Luna-13A must
not invent or silently choose a reward contract.

Resolve one of these coherent models through current repository authority and
document the decision:

- **Model A - retry-idempotent logical delivery:** the same logical reward
  message may be retried but credits once; distinct messages with identical
  numeric values credit independently. Implement bounded reward identity
  tracking and declare reset, retention and eviction behavior.
- **Model B - repeated-application delivery:** every delivered reward event is
  another credit application; identical values may repeatedly affect
  eligibility/credit. Remove obsolete duplicate-suppression or exactly-once
  claims if this is authoritative.

If current authority is contradictory, stop only the reward portion and return
exactly `REWARD CONTRACT DECISION REQUIRED`. The decision packet must include
current production behavior, conflicting docs/tests, consequences of Model A
and Model B, affected files, bounded-state implications, replay implications,
and a clearly labeled recommendation if one is offered. Safe independent
Stage-0 work may continue, but the terminal status must remain blocked. Never
hide the contradiction behind a test-only choice or an unbounded identity set.

For the selected model, test same logical reward twice, distinct rewards,
equal-valued distinct rewards, reset, and bounded retention/eviction when
applicable. Report whether replay is deterministic and whether duplicate
handling is part of the public contract.

## C. Projected structural-capacity accounting

Require projected batch-capacity validation before mutation. Individually valid
candidate edges must not bypass finite topology constraints when jointly
committed. Cover projected fan-in overflow, projected fan-out overflow,
global/edge capacity where supported, duplicate/existing edges, and simultaneous
failure causes.

Where the architecture requires it, admission is all-or-none: a rejected batch
leaves the topology unchanged. The public result preserves a meaningful reason.
Observer/instrumentation on and off must not alter computation. For simultaneous
failures, choose and document deterministic reason precedence or represent
multiple reasons; do not leave the result ambiguous. Test projected capacity,
atomic rejection, duplicate handling, reason semantics and observer equivalence.

## D. Bounded recurrent execution

Bounded queue occupancy is not bounded lifetime work. Standardize or verify an
execution-budget contract that distinguishes at least `completed` from
`budget_exhausted`. Every run reports configured event budget, processed event
count, pending event count and termination reason. Use a recurrent fixture with
positive finite edge delays and continued-activity-capable routing.

Run budgets `1`, `2`, `8` and `64`. An exhausted run must never masquerade as
normal completion. Preserve local timestamps, finite propagation and
 deterministic tie ordering. Do not introduce a global timestep, centrally
clocked neural execution, hidden recurrent tick or unbounded retry/work loop.

## Architecture preservation

Preserve A01 event-driven operation, A02 intrinsic temporal state, positive
finite inter-neuron delays, A04 bounded topology, A06 predictive coding and
explicit error events, A07 local learning, A11 delayed credit, A15 hardware
independence, no label leakage, and bounded state/dynamics under A08. Preserve
the existing reset and information-boundary rules.

Do not introduce a global timestep, centrally clocked neural execution,
unbounded reward identity storage, unbounded recurrent processing, future-
observation leakage, global mutable learning state, or spatial-reservoir
dependence. Labels, evaluation aggregates and instrumentation must not become
core neural inputs. No unrestricted backpropagation may replace local learning.

## Luna-12N preservation boundary

Do not regress configured-versus-actual operation accounting, real metadata
negative controls, measured arrival timestamps, weighted cumulative-delay path
analysis, explicit event-budget status, strengthened provenance, synthetic
evidence labeling, score/rank/admitted-edge/final-graph distinctions, or
intervention labeling. Do not reinterpret Luna-12N as decay efficacy: its
corrected fixture shows score/rank changes but no different admitted edge set or
final graph, and it does not establish external prediction improvement,
classification improvement, resource efficiency or general temporal-learning
superiority.

## Required validation

Run focused Stage-0 tests and the applicable existing suites. At minimum:

- Classifier: stale, equal-time and future finalization; direct and dispatched
  paths; atomic before/after state comparison.
- Reward: tests required by the selected Model A or Model B, including same
  logical, distinct, equal-valued distinct rewards and reset, with bounded
  retention/eviction when applicable.
- Structural plasticity: projected fan-in and fan-out, simultaneous causes,
  atomic rejection, meaningful reason(s), and observer on/off equivalence.
- Recurrence: a positive-delay recurrent loop, budgets `1`, `2`, `8` and `64`,
  processed/pending counts, and explicit completion/exhaustion.

Also run relevant Luna-12H regressions, Luna-12N corrective regressions, the
full CPU regression suite, established compile/static checks, and `git diff
--check`. Record optional CUDA/GPU skips as not applicable to CPU-only Stage 0;
do not treat them as architecture failure. Separate passed, failed, not-run and
not-applicable checks. Do not run GPU, FPGA or FPAA work as a substitute for
software-reference validation.

## Handoff and evidence

Use `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md` and write the expected
handoff as `workflow/handoffs/stage0-invariant-closure-Luna-13A.md`. Include at
least:

- starting revision, ending revision/tree and dirty/clean state;
- changed files and exact classifier disposition;
- stale-call before/after evidence;
- reward-contract disposition and decision packet or selected model;
- projected-capacity evidence and rejection-reason semantics;
- recurrent-budget semantics and budgets `1`, `2`, `8`, `64` evidence;
- focused test, full regression, compile/static and diff-check results;
- remaining blockers and readiness for Luna-0 independent review.

Separate `OBSERVED`, `INFERRED` and `HYPOTHESIZED` claims. Do not report a
planned check as passing. Do not claim dataset, GPU, hardware, physical-energy
or architecture-promotion evidence.

## Future direction and promotion boundary

The likely next scientific question is a controlled temporal structural-
selection experiment with locally observed causal temporal evidence, one free
structural admission slot, competing candidates, an analytically predicted
score crossover, decay-rate manipulation, held-out crossover intervals and
negative controls. Record this only as a future direction. It is not authorized
by Luna-13A, and Luna-13A must not authorize Luna-13B or any other successor.

Return one exact terminal status from the list above and explicitly state that
Luna-0 independent Stage-0 review is required before any next Luna is
considered.
