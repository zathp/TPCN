---
name: Luna-13C Useful Causal Effect of Learned Temporal Structure
description: Test whether a frozen edge selected by the verified Luna-13B mechanism causally improves a fixed external temporal task outcome.
---

# Luna-13C - Useful Causal Effect of Learned Temporal Structure

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/architecture_proposals/README.md`,
`workflow/docs/architecture_proposals/ACP-TEMPLATE.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, the Luna-12H and Luna-12N
specifications and handoffs, the Luna-13A handoff, the Luna-13B contract and
handoff, and the independent Luna-0 review of Luna-13B before implementation.
Record the exact starting revision, executed revision/tree, branch and
worktree state. Preserve unrelated changes.

This contract is creation-only until Luna-0 gives a separate explicit
execution assignment. Do not execute Luna-13C while creating or reviewing this
contract. The reviewed Luna-13B implementation checkpoint is
`816929fa097e049ce7d82a1f7c63fb9cc4e8bd3f`; the independent Luna-0 review is
`04f2088725c71eb20b808ae07dbd99a02d4cd459`. Verify the actual baseline rather
than assuming these revisions remain current.

## Authority, question and classification

Luna-13C is a CPU-only `EXPERIMENT` and `VERIFICATION`. It preserves A01-A15,
does not promote A14, and does not authorize Luna-13D. CUDA, GPU
visualization, FPGA, FPAA and hardware-equivalence validation are optional or
out of scope; an optional CUDA skip is not a failure.

The scientific question is:

> Does a structural edge admitted through the independently verified Luna-13B
> local temporal-selection mechanism causally improve a declared external task
> outcome, and does targeted removal remove the benefit while exact restoration
> recovers it?

The primary falsifiable hypothesis is:

> A structural edge admitted from causally observed temporal evidence produces
> a predeclared practical benefit on a fixed external task target. Removing
> that exact edge materially reduces or abolishes the benefit, restoring the
> exact edge recovers the benefit within a frozen tolerance, and sham or
> irrelevant-edge interventions do not reproduce the effect.

A result that changes topology or an internal trace without changing the
external task outcome counts against useful causal efficacy. A statistically
detectable but practically meaningless change does not pass the primary gate.
If the fixed useful-edge positive control cannot improve the task metric, the
fixture is insensitive or invalid and a negative learned-edge result is not
interpretable.

Luna-13B established runtime-local evidence, decay-sensitive score crossover,
rank reversal, one-slot competition, admitted-edge reversal, final-graph
change, relabeling/mirroring resistance, deterministic ties and bounded
execution. It did not establish task usefulness, prediction improvement,
classification improvement, resource efficiency, scalability, hardware
equivalence or general temporal-learning superiority. Luna-13C must reuse the
verified structural-selection mechanism rather than invent a second unrelated
learner, and must not weaken its causal-evidence requirements.

## Ownership and boundaries

Own only the bounded CPU task fixture, reuse or minimally expose the Luna-13B
selection mechanism, frozen-state intervention runner, focused tests,
machine-readable artifacts, relevant documentation and
`workflow/handoffs/useful-causal-effect-Luna-13C.md`. Production changes are
authorized only in declared experiment components and their focused tests.
Do not silently redesign the canonical neuron, event runtime, topology,
classifier, reward/credit contract, predictive coding or decay semantics. If a
core change or A01-A15 departure is required, stop and return an ACP/decision
packet to Luna-0.

Preserve event-driven execution, local timestamps and elapsed time, finite
positive propagation, bounded nodes/edges/fan-in/fan-out/state/queues/history,
local learning, predictive/error events, delayed credit, local resource
accounting, deterministic tie ordering, finite recurrence and hardware-neutral
semantics. Do not introduce a global neural timestep, future-point or
future-event preprocessing, label/global-topology leakage, unrestricted
backpropagation, topology-derived ground truth, unbounded candidate/history
state, instantaneous edge effects or silent budget truncation.

Labels and external targets may be used for evaluation and declared external
readout supervision only after label-free neural computation. They must not
enter candidate generation, local scoring, structural admission, runtime
neuron state before permitted evaluation, routing, energy or prediction/error
computation. The correct external target must remain identical when the graph
is intervened on.

## Fixed external task

Choose the smallest controlled temporal task that genuinely exercises the
Luna-13B mechanism. Prefer temporal-order discrimination with the same event
payload multiset in different orders, an interval-dependent prediction with
the same event types and different elapsed intervals, or a delayed-cue task.
A small number of held-out orders, intervals or cues is sufficient. Do not
begin with the full A-Z streaming dataset unless the simple causal utility
fixture is first established. Do not use `predict the activation produced by
the current topology` or any target derived from selected edge identity, path
length, current-topology activation, candidate score or the model's own
prediction.

Freeze before held-out evaluation:

- fixture identity, task definition, examples and train/held-out split;
- external target definition and prediction quantity;
- decision rule and loss function, if applicable;
- primary metric and practical effect threshold;
- intervention definitions, seeds, budgets and configurations.

The target is fixed independently of the learned topology. Record exactly the
predicted quantity, fixed external target, decision rule and loss/metric. Use
per-case correctness when the fixture is small; do not overstate population
accuracy. The same inputs, payload multiset, targets and evaluation budget
must be used for every structural condition.

## Structural learning and freeze protocol

Construct or train the structural state using the verified Luna-13B mechanism:
runtime-local candidate evidence, analytic crossover semantics where relevant,
one-slot competition where useful, bounded admission, deterministic replay and
bounded execution. Candidate records must retain source/target, observation
timestamps, elapsed intervals, local state/residual, scoring decay, score,
rank, decision time, candidate identity and rejection reason. No future,
label, global aggregate or held-out outcome may affect scoring or admission.

Use this sequence:

1. Construct/train the causal structural state on the declared training data.
2. Record the frozen checkpoint and graph fingerprint.
3. Freeze all learned structural state before comparative evaluation.
4. Clone/fork that identical frozen state for each condition, or restore the
   exact same checkpoint before every condition.
5. Evaluate the same held-out inputs and fixed targets under the declared
   intervention only.

Do not retrain independently after edge removal, restoration, sham or
irrelevant-edge intervention. Preserve non-intervened neuron, predictor,
readout, queue, initialization and configuration state as closely as the
fixture permits. Prove computational equivalence of condition starting states
except for the intended intervention.

## Required paired interventions

Run at least these conditions:

1. **Learned edge present:** evaluate the frozen learned topology normally.
2. **Targeted learned edge removed:** remove only the exact claimed edge.
3. **Exact learned edge restored:** restore the same source, target, delay,
   weight/strength and every metadata field that affects computation.
4. **Sham intervention:** perform metadata/no-op intervention without changing
   the computational graph.
5. **Irrelevant-edge removal:** remove an unused or analytically irrelevant
   edge not expected to mediate the claimed benefit.

Restoration is actual computational restoration, not a partial graph rollback.
Use explicit edge-set comparison or a graph fingerprint and verify that the
present and restored graphs agree for the relevant structure. Record the
removed edge and all intervention effects. Interventions must run from
independent clones or deterministically identical restored checkpoints, never
from a mutating sequence that contaminates later conditions.

## Required controls

The primary matrix must also include:

- fixed topology with no structural growth;
- equal-budget random structural growth with explicit stochastic seeds;
- a fixed useful-edge positive control known analytically or by construction
  to help the task;
- Luna-13B mechanism controls that preserve candidate exposure and resource
  ceilings, including appropriate timing/order, score-decay and one-slot
  controls;
- deterministic repeats distinguished from independent stochastic seeds.

Random controls must receive equivalent candidate opportunity, event budget,
queue capacity, structural capacity and mutation/resource ceilings. Do not
require this Luna to establish broad statistical superiority over random
selection, but report whether random growth reproduces the specific causal
effect. Retain fixed-topology and all failed/negative controls.

## Matched metrics and evidence

Declare metrics before held-out evaluation. Require at least one externally
meaningful primary metric: task accuracy, fixed-target prediction loss,
correct target arrival, correct response latency or another bounded task-level
decision outcome. Record mechanism diagnostics separately:

- target arrival time and target state;
- prediction errors and route traffic;
- total processed events, pending events and queue peak where available;
- configured event budget and termination reason;
- proxy energy, its units and utility definition;
- edge set/fingerprint, source/target/delay/strength/metadata;
- initialization/checkpoint identity and non-intervened state comparison.

Proxy energy is secondary unless the experiment is explicitly designed around
matched utility. Do not call a shorter path better task performance or call a
mechanism efficient solely because it used fewer events. Report higher-cost
benefit, lower-cost equal performance, latency tradeoffs and no-effect results
without requiring a resource reduction for causal utility.

Every intervention report must contain a paired table equivalent to:

| Condition | Learned edge present? | Fixed external target | Prediction/decision | Loss/accuracy | Target arrival | Events | Completion |
|---|---:|---|---|---:|---|---:|---|

Also produce an edge-intervention summary:

| Condition | Primary task metric | Delta vs present | Graph fingerprint | Expected result |
|---|---:|---:|---|---|

For prediction loss, the target is common across all graph conditions. For
accuracy, freeze the decision rule and thresholds before evaluation. Record
per-case outcomes for tiny fixtures.

## Causal utility gate

A successful causal result requires all of the following:

1. The learned edge was derived through the verified Luna-13B local causal
   mechanism.
2. The frozen learned topology shows the predeclared external task benefit.
3. Targeted removal materially reduces or abolishes that benefit.
4. Exact restoration recovers it within the predeclared practical tolerance.
5. Sham intervention produces no material change.
6. Irrelevant-edge removal is null or materially smaller than targeted removal.
7. The fixed useful-edge positive control behaves as expected.
8. The external target is unchanged across conditions.
9. Evaluation inputs and all paired resources are matched.
10. Every run completes without silent budget exhaustion.

The practical effect threshold must be frozen before inspecting held-out
comparative outcomes. Report confidence/statistical summaries where useful,
but practical materiality is mandatory. A positive-control failure blocks
interpretation rather than proving learned-edge uselessness.

Required causal questions are: Does removal reduce the external benefit? Does
exact restoration recover it? Is sham null? Is irrelevant-edge removal null or
smaller? Does the useful positive-control edge work? Does random growth
reproduce the effect? Does fixed topology reproduce it? Were topology, trace
and task outcome separately measured?

## Bounded execution and information checks

Every run must record configured event budget, processed events, pending
 events, queue peak where available, termination reason and either `completed`
or `budget_exhausted`. A budget-exhausted run cannot count as successful task
evidence. No global timestep or hidden recurrent tick may be introduced.

Test label isolation by relabeling identical input streams and proving that
neural events, local state, predictor/error behavior, routing, structural
candidates/admission and energy are unchanged. Labels may change only declared
external readout/evaluation behavior. Test future-information exclusion and
verify that held-out targets and comparative outcomes are unavailable to
structural learning. Test that capture/diagnostics do not alter execution.

## Required artifacts and provenance

Machine-readable artifacts and the handoff must retain:

- baseline and executed revision/tree, branch and clean/dirty state;
- fixture identity, task/target definition, examples and split;
- frozen trained-state/checkpoint and graph fingerprints;
- exact intervention definitions and edge properties;
- primary metric, decision rule/loss and frozen practical threshold;
- seeds, environment and configuration;
- event/queue budgets and completion status;
- results for every paired intervention and control;
- OBSERVED, INFERRED and HYPOTHESIZED evidence labels.

## Required validation

Focused tests must cover learned-edge present, targeted removal, exact
restoration, sham, irrelevant-edge removal, useful-edge positive control,
fixed topology, equal-budget random growth, fixed external target, matched
inputs, graph fingerprint/equivalence, label isolation, future-information
exclusion, deterministic replay, held-out freeze and completion status.

Then run regressions for Luna-13B, Stage-0, Luna-12H and corrected Luna-12N,
the full CPU suite, repository compile/static checks, standard diagnostics and
`git diff --check`. Optional CUDA tests may skip and are non-gating. Separate
passed, failed, not-run and not-applicable checks. Do not execute GPU, FPGA or
FPAA work as a substitute for CPU validation.

## Preservation and promotion boundary

Luna-13C must not regress classifier temporal monotonicity, retry-idempotent
reward delivery and bounded identity retention, projected structural
capacity/admission and rejection semantics, bounded recurrent execution,
Luna-12H temporal mechanics, Luna-12N corrective semantics or Luna-13B causal
structural crossover. Luna-12J's manual replay termination-status gap remains
non-gating unless Luna-13C directly relies on that path.

This is an experimental result, not an A14 promotion or architecture change.
A successful result may claim only:

> A structural edge learned through the verified local temporal-selection
> mechanism causally improves the specified bounded external task under the
> tested conditions, because targeted removal reduces the predeclared benefit
> and exact restoration recovers it while sham and irrelevant interventions do
> not.

It may not claim general temporal-learning superiority, broad generalization,
superior classification architecture, energy efficiency without independent
evidence, scalability, hardware equivalence or biological equivalence. Luna-
13C must not authorize Luna-13D; only a later Luna-0 decision may define a
successor.

## Required handoff and terminal statuses

Use `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md` and write
`workflow/handoffs/useful-causal-effect-Luna-13C.md`. The handoff must answer:

1. What external task and topology-independent target were used?
2. How was the learned edge obtained and was state frozen before intervention?
3. Did the present topology meet the predeclared benefit?
4. What happened on targeted removal and exact restoration?
5. What happened under sham and irrelevant-edge removal?
6. Did the fixed useful-edge positive control work?
7. How did fixed topology and equal-budget random growth behave?
8. Were inputs, targets, graphs and starting states paired/equivalent?
9. Were any runs budget exhausted or labels/future/global information leaked?
10. What narrow causal task claim is supported, what resource tradeoff was
    observed and what remains unproven?

Use exactly one terminal status:

- `PASS — USEFUL CAUSAL EFFECT ESTABLISHED, READY FOR LUNA-0 REVIEW`
- `PASS WITH FOLLOW-UP — CAUSAL TASK EFFECT ESTABLISHED, LIMITATIONS REMAIN`
- `MECHANISM VERIFIED — EXTERNAL TASK BENEFIT NOT ESTABLISHED`
- `BLOCKED — POSITIVE CONTROL FAILED`
- `BLOCKED — INTERVENTION INVALID`
- `BLOCKED — EXTERNAL TARGET INVALID`
- `BLOCKED — CAUSAL EVIDENCE INVALID`
- `BLOCKED — INVARIANT REGRESSION`
- `BLOCKED — REGRESSION`

Return every result to Luna-0 for independent review. No terminal status
authorizes Luna-13D.
