---
name: Luna-13D Finite-Resource Utility, Retention, and Capacity-Pressure Experiment
description: Test bounded retention, pruning, and task/resource tradeoffs when useful and low-value temporal structure compete for finite capacity.
---

# Luna-13D - Finite-Resource Utility, Retention, and Capacity-Pressure Experiment

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/architecture_proposals/README.md`,
`workflow/docs/architecture_proposals/ACP-TEMPLATE.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, the Luna-13B and Luna-13C
contracts/handoffs, and the independent Luna-0 Luna-13C review before
implementation. Record the exact starting revision, branch, tree and worktree
state. Preserve unrelated changes.

This contract is creation-only until Luna-0 gives a separate explicit
execution assignment. Do not execute Luna-13D while creating or reviewing
this contract. The synchronized review tree is currently
`df297c446856d07b2822702202bbb61e81cf38a4`; verify the actual baseline rather
than assuming it remains current. The corrective Luna-13C implementation
source was `685cd721f7ca108278aa2e3044b53d46981e5bbd`, reviewed in tree
`09995add7643e63f61c45602922238e319965113`.

## Authority, question and classification

Luna-13D is CPU-only `EXPERIMENT` and `VERIFICATION`. It preserves A01-A15,
does not promote A14, and must not authorize Luna-13E. CUDA, GPU
visualization, FPGA, FPAA and hardware-equivalence work are out of scope; an
optional CUDA skip is non-gating.

The scientific question is:

> When useful and non-useful structural opportunities compete under finite
> topology and execution capacity, does the temporal structural mechanism
> retain or recover externally useful connectivity, prune or reject lower-
> value structure according to declared rules, and expose the resulting
> task/resource tradeoff without violating bounded execution?

The falsifiable hypothesis is:

> Under declared finite capacity pressure, useful temporally learned
> connectivity is preferentially retained or recoverable while stale, unused
> or low-value connectivity is pruned, rejected or left unadmitted according
> to existing architecture rules, and task utility remains measurable against
> a fixed external target.

Evidence against it includes useful edges being pruned while lower-value
edges survive without a declared reason, useful candidates being blocked with
legitimate capacity available, or a claimed resource improvement being caused
only by task failure or silent truncation.

Luna-13B established causal local evidence and structural admission change.
Luna-13C established a narrow reproducible external task effect for one
learned edge, with `2/2` present, `1/2` targeted removal and `2/2` exact
restoration, while retaining limitations about two cases, random reproduction,
generalization, efficiency and full-state checkpointing. Luna-13D must reuse
that validated external-task semantics where practical; it must not re-prove
13B or 13C from scratch and must not replace the external target with an
internal topology-dependent activation.

## Ownership and boundaries

Own only the bounded CPU fixture/runner, experiment policy exposure needed for
the declared pressure conditions, focused tests, machine-readable and
human-readable artifacts, relevant documentation, and
`workflow/handoffs/finite-resource-utility-capacity-pressure-Luna-13D.md`.
Production changes are authorized only when they preserve the contract and
are necessary to expose existing bounded behavior. If a core architecture
change, new protected-edge lifetime, new utility objective, or new replacement
mechanism is needed, stop that portion and return an ACP/decision packet to
Luna-0 and the project owner.

Preserve event-driven execution, local timestamps and elapsed time, positive
finite propagation, predictive coding and explicit error events, local
learning, delayed credit, reward idempotency, bounded state/queues/history,
structural admission atomicity, bounded recurrent execution, label isolation,
deterministic replay and hardware-neutral behavior. Do not introduce a global
neural timestep, future-point preprocessing, future/held-out information,
global topology statistics as neural input, unrestricted backpropagation,
unbounded candidate/history state, silent queue truncation or topology-derived
ground truth.

### Replacement boundary

Inspect the current architecture contract, implementation and tests before
testing replacement. A14 permits explicit finite replacement policies but does
not by itself authorize inventing an atomic edge-replacement production
mechanism for this experiment. If an existing documented and tested atomic
replacement mechanism is already authorized, Luna-13D may measure it. If not,
restrict the experiment to bounded admission, coexistence, pruning, and later
normal growth after legitimate capacity is freed. A full topology must be
allowed to block admission as an observed result. Do not add protected-edge
lifetime or implicit replacement to force a positive result.

## Fixed external task and information boundary

Reuse the Luna-13C fixed external target, task semantics, decision rule and
causal learned-edge provenance where practical. Freeze fixture identity,
examples, split, target, metric/loss, thresholds, intervention definitions,
budgets, capacity configuration and seeds before held-out evaluation. Labels
may affect only declared external readout/evaluation supervision after
label-free neural computation; they must not enter events, routing, energy,
prediction/error state, candidate evidence, utility decisions or pruning.

Distinguish task utility (external correctness, loss, target arrival and
latency) from resource cost (events, queue peak, proxy energy, edge count and
capacity), retention, pruning, replacement, capacity failure and execution
failure. Do not call fewer events efficient when the task fails. Do not define
a single scalar winner unless an existing architecture interface already
defines one; prefer Pareto-style reporting. At matched utility, freeze any
non-inferiority and resource-reduction thresholds before held-out evaluation.
Use raw case counts for the tiny deterministic fixture rather than invented
percentages.

## Required structural fixture

Construct or reuse a bounded fixture containing, with provenance: a useful
learned edge whose external utility is demonstrated or revalidated; an unused
or low-value edge with little/no useful traffic or reward; an expensive useful
path where feasible; and an expensive useless path where feasible.

For every useful edge record creation time, first use, use count, reward or
utility association, external contribution, age/lifetime, strength/state when
available, pruning decision/reason and retained status. For every pruned edge
record evidence, inactivity since last use, accumulated utility/reward, cost,
pruning timestamp, reason and graph state before/after. Identifier ordering,
age alone or recency alone must not silently decide the outcome.

At each pressure point record external task result/loss, target arrival and
latency, graph state, useful-edge presence, accepted/rejected mutations and
reasons, edge traffic, processed events, proxy energy and units, queue peak,
edge count and completion status.

## Controlled stages and pressure dimensions

Do not vary every resource at once in the primary fixture. Stage fan-in,
fan-out, total edge capacity, event budget, queue capacity where safely
configurable, distractor candidates, unused edges, expensive low-value edges
and useful competing edges.

### Stage A - Baseline utility/resource characterization

Reproduce the useful learned edge under comfortable capacity and record task
and resource metrics.

### Stage B - Distractor pressure

Add irrelevant or low-value candidates while capacity remains sufficient.
Measure useful-edge retention, traffic, cost and rejection causes.

### Stage C - Structural capacity pressure

Test capacity below full, approaching full and full. At full capacity present
a useful candidate, a useless/distractor candidate and, where valid, an
existing useful and stale unused edge. Observe the current architecture. Do
not manufacture replacement; blocked admission is a legitimate result.

### Stage D - Pruning

Enable only declared pruning semantics. Test stale/unused versus useful edges,
record reasons and verify that pruning does not select by identifier artifact.

### Stage E - Post-pruning growth

Where pruning legitimately frees capacity, present a later useful candidate
and test ordinary bounded admission. This is preferred to undeclared atomic
replacement.

### Stage F - Workload shift (optional)

Within the bounded fixture, make an edge useful in phase A less useful in phase
B or make another edge newly useful. Report whether adaptation occurs. Do not
require successful replacement when the architecture does not support it.

## Controls, seeds and checkpointing

Include fixed topology, the verified temporal structural policy, and equal-
budget random structural growth with genuine independent seeds (at least five
when consistent with the fixture and existing contract style). Record the
actual graph chosen under each seed. Deterministic parameter sweeps are not
stochastic replication. Where useful, include capacity-preserving growth with
pruning disabled. Preserve all failed and negative controls.

Inspect Luna-13C's reset/rebuild plus metadata fingerprint limitation. If
architecture-neutral and practical, add a deterministic serializable
experiment checkpoint covering neuron state, queues, eligibility, reward
ledgers and random state. If broad production changes would be required,
document the limitation and keep checkpoint work subordinate to the resource
experiment.

## Bounded execution and failure accounting

Every run must report configured event budget, processed events, pending
events, queue peak where supported, termination reason and exactly whether it
was `completed` or `budget_exhausted`. No budget-exhausted run counts as
successful evidence; no silent truncation is allowed and no global timestep
may be introduced.

Report separately task failure, admission failure, queue rejection, budget
exhaustion, pruning-related failure and capacity-related failure. A full
topology with no freed capacity may legitimately reject a useful candidate.

## Required artifacts and metrics

Machine-readable and human-readable summaries must include tables equivalent
to:

| Run | Capacity policy | Useful edge present | Task result | Events | Proxy energy | Latency | Pruned edges | Completion |
|---|---|---:|---|---:|---:|---:|---|---|

| Edge role | Uses | Reward/utility evidence | Cost | Age | Pruned | Reason |
|---|---:|---|---:|---:|---:|---|

| Seed | Policy | Final useful edge | Final graph | Task result | Events | Energy |
|---:|---|---:|---|---|---:|---:|

Record baseline and executed revision/tree, clean/dirty state, fixture,
capacity and pruning configuration, policy, seeds, target, budgets, resource
units, environment, threshold definitions, graph fingerprints and all
completion/failure statuses. Proxy energy is an activity-cost estimate, not
calibrated physical energy unless separately established.

## Interpretation gates and terminal statuses

The mechanism gate passes only if useful versus low-value structure responds
differently under declared pruning/retention rules without external task
regression or bounded-execution violation. A separate resource-efficiency gate
may pass only when a predeclared resource reduction is observed at matched
task utility. The second gate is not required for the first.

Permitted terminal statuses are:

- `PASS - USEFUL STRUCTURE RETAINED UNDER RESOURCE PRESSURE, READY FOR LUNA-0 REVIEW`
- `PASS WITH FOLLOW-UP - RETENTION/PRUNING MECHANISM ESTABLISHED, RESOURCE BENEFIT LIMITED`
- `MECHANISM VERIFIED - RESOURCE EFFICIENCY NOT ESTABLISHED`
- `NEGATIVE RESULT - USEFUL STRUCTURE NOT RETAINED UNDER TESTED PRESSURE`
- `BLOCKED - PRUNING/RETENTION EVIDENCE INVALID`
- `BLOCKED - CAPACITY ACCOUNTING INVALID`
- `BLOCKED - EXTERNAL UTILITY REGRESSION`
- `BLOCKED - INVARIANT REGRESSION`
- `BLOCKED - REGRESSION`

Successful claims remain narrow: tested useful structure survived stated
pressure, declared pruning freed capacity for later normal admission, or a
predeclared matched-utility resource reduction was observed. Do not claim
broad efficiency superiority, random-policy superiority, scalability,
generalization, hardware/FPGA/FPAA equivalence or biological equivalence.

## Required validation and handoff

Focused tests must cover useful-edge retention, unused-edge pruning and
reason, below/near/full capacity behavior, post-pruning admission, fixed
topology, random growth and seed provenance, resource accounting, fixed
external target, bounded execution, no silent truncation, label isolation and
deterministic replay where applicable. Test checkpoint equivalence if added.

Run regressions for Luna-13C corrective evidence, Luna-13B crossover, Stage-0
invariants, Luna-12H, corrected Luna-12N, the complete CPU suite, compile/static
checks, diagnostics and `git diff --check`. CUDA remains optional and
non-gating. Separate passed, failed, not-run and not-applicable checks.

Use `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md` and write
`workflow/handoffs/finite-resource-utility-capacity-pressure-Luna-13D.md`.
The handoff must answer which resource was pressured; which edge was useful;
which edges were stale/useless; whether useful connectivity survived; what was
pruned and why; whether capacity was freed; whether later useful structure was
admitted; task, events, energy and latency effects; budget exhaustion; fixed
and random-control behavior across seeds; utility sacrifices; architecture
changes; and remaining unproven claims. Label evidence `OBSERVED`,
`INFERRED` or `HYPOTHESIZED`, and classify every check.

Return all results to Luna-0 for independent review. Luna-13D must not
authorize Luna-13E. No execution, architecture promotion or successor
dispatch is implied by this contract.