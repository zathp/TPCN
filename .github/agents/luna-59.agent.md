---
name: "Luna-59 Event-Deadline Reward Interface Design Prerequisite"
description: "Design only: resolve controlled temporal event/deadline prediction and fair omission/silence treatment, including a no-training alternative; no experiment or implementation."
tools: [read, search, edit]
---

# Luna-59 — Event/deadline reward-interface design prerequisite

## Disposition and publication boundary

**TASK OBJECTIVE DEFINED — REWARD SEMANTICS PREREQUISITE REQUIRED.**
**DESIGN PREREQUISITE AUTHORIZED / NOT EXECUTED.**
**LUNA-59 TASK-EFFICACY EXPERIMENT NOT AUTHORIZED.**

The project owner's 2026-10-09 request authorizes the smallest prerequisite
if current reward/credit cannot fairly treat missed positives and correct
silence. This dispatch authorizes one documentation-only interface decision,
not an experiment, implementation, new reward rule, or architecture approval.
The no-training alternative must be considered; reward changes are not
assumed necessary for a fixed-mechanism efficacy study.

Reviewed baseline: `0a6b0125627384a036410ff1588cd1115bf53147`, clean
`main == origin/main` after fetch. The authoritative publication SHA is the
commit containing this contract on `origin/main`, not that predecessor.
Prerequisite work may start only after that publication is verified from a
clean fetched checkout and explicitly assigned. Publication alone does not
authorize scientific execution. Stop after the design handoff for Luna-0 and
owner review; any experiment needs a separate complete authorization.

## Authoritative inputs and responsibilities

Read `workflow/ARCHITECTURE_CONTRACT.md`,
`workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`, the proposal README and
ACP template, and `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`.
The historical `tpcn-luna-workflow/` package is absent in this repository;
the tracked `workflow/` equivalents are the current authorities.

Also read:

- Accepted ACP-0006 sections 5–11 and ACP-0008; A01–A04, A06–A11, A14–A15.
- `tpcn/predictive_coding.py`, `tpcn/eligibility.py`,
  `tpcn/experiment_excursion_runtime.py`, `tpcn/experiments.py`,
  `tpcn/excursion_neuron.py`, and relevant existing tests.
- Luna-58 contract, execution handoff, config and retained summary; Luna-55
  config; Luna-54 runtime config; the frozen Luna-45 configuration.
- `workflow/handoffs/luna-0-owner-task-objective-luna59-governance-20261009.md`.
- The complete project-owner decision source when supplied. The current
  intake contains the owner's restatement, not a separately accessible
  attachment. Do not claim to have read an unavailable attachment; stop if
  its missing content is necessary to resolve a decision.

Responsible role: Luna-59, a Luna-8-led design brief with the Luna-3
prediction-interface responsibility explicitly included. Luna-0 arbitrates
interfaces; only the owner or a delegated decision-maker accepts new
semantics. This does not dispatch agents or require parallel work.

## Frozen owner objective, not a frozen benchmark

The desired future study is controlled deterministic temporal event/deadline
prediction, prioritizing scientific mechanism validation. Negatives and
ambiguous prefixes require correct silence. Premature and late outputs are
errors. Score the first output; duplicates carry an event-efficiency penalty
and cannot rescue the first-output decision.

Held-out balanced accuracy is primary. Meaningful efficacy requires at least
**+10 percentage points** versus the predeclared historical/default
comparator, with at most **+5 percentage points FPR degradation**. If
stochastic, direction must agree in a majority of declared seeds; if
deterministic, require exact independently executed replay. Matched
positive/negative trials and temporal anti-shortcut controls are required.
Application benchmarks are deferred. No E+49 crossing requirement exists:
those historical strata have no defined task-label mapping.

These requirements must not be weakened or turned into measured passes.
The exact target, eligible interval/deadline, comparator, population,
penalty formula and no-training/training decision are not yet frozen.

## Observed interface boundary

1. ACP-0006 predicts the next numeric contribution at a configured input
   port. The adapter creates a `Prediction` from a predictor-source
   `ExcursionEmission`; it does not call `emit_prediction()` to enqueue a
   `PREDICTION_EVENT`. Generic `LocalPredictor.emit_prediction()` exists,
   but its existence does not establish a task-specific causal output path.
2. `expected_resolution_at` is metadata in `LocalPredictor`; observation
   matching uses the target key and expiry, not a lower eligibility window.
   `expire()` removes records without producing an omission error.
   Settling at `t_last + settling_horizon` is not a task deadline.
3. ACP-0006 section 7 permits eligibility only for actual canonical emissions.
   `end_character()` attributes reward to the first readout emission;
   without one it explicitly reports unmatched credit. Negative reward can
   credit an existing identified trace, not a nonexistent silence trace.
4. Ledger credit accounting and the external class-prototype update are
   distinct. Existing prototype learning is not an event/deadline readout
   and does not demonstrate a trainable reward-to-neuron mechanism.

Do not fabricate zero-valued activity, an emission, a prediction ID,
omission credit, a deadline observation, or a new neural learning update to
bridge these boundaries.

## Exactly authorized scope and owned files

The later prerequisite assignment may write only:

- `workflow/docs/luna/LUNA_59_EVENT_DEADLINE_INTERFACE_DESIGN.md`
- `workflow/handoffs/luna-59-event-deadline-interface-design.md`

Deliver one proposed interface specification and one completed handoff.
Read existing code/tests/artifacts; do not run them under this design-only
dispatch. No changes to this authorization, other agents, core, tests,
runners, configurations, datasets, scientific artifacts, ACPs, architecture
contract, workflow or changelog are delegated to the prerequisite worker.
Luna-0/owner retains governance publication authority.

No dataset generation, simulations, scientific replay, benchmark, parameter
calculation/search, tuning, implementation, fixture execution, or application
experiment is authorized. Do not consume the owner's four-experiment quota:
zero experiments are authorized.

## Required bounded deliverable

Produce the following **proposals and compatibility findings**, not invented
established semantics:

1. Specify a causal task-output mapping: actual observable event type,
   source, payload, identity and timestamp; distinguish canonical discharge,
   emission, queued prediction and evaluator decision. Explain how an output
   can occur before its target, including finite route/emission delays.
2. Supply one eight-case, non-executed decision table: on-time positive,
   missed positive, correct negative silence, false-positive negative,
   premature first output, late first output, duplicate after first output,
   and ambiguous-prefix output. For each, identify proposed first-output
   score, timing error, terminal outcome, reward availability time and
   attributable existing trace or explicit absence. Boundary inclusivity,
   same-time ordering and absence resolution must be explicit proposals.
3. Compare only two design dispositions:
   - **Fixed/no-training:** no label-dependent reward, parameter update,
     prototype fit, structural adaptation or cross-trial learned state.
     Use actual observable emissions and a downstream evaluator, with
     native prediction/error instrumentation honestly distinguished from
     task predictions. Explain whether this tests the owner's task without
     pretending omission credit exists. Define the proposed freeze and
     reset boundary and evaluation-only outcome channel.
   - **Training:** show whether all eight cases can use existing governed
     credit identities, causal delivery and finite ledgers fairly. If not,
     specify the smallest missing interface as a proposal for owner review.
     Do not authorize silent-state eligibility or amend ACP-0006 yourself.
     Any material semantic departure must enter the ACP process separately.
4. State what remains to freeze a task contract: target/event schedule,
   eligible interval/deadline, trial generator version and independent
   outcome rule, matched nuisances/counts/amplitudes/durations, disjoint
   provenance/splits, exact held-out counts and independent repetitions,
   comparator and justified mechanism/component arms, budgets, primary
   scoring/FPR/duplicate penalty, secondary metrics and falsification.
   No post-outcome stream selection or historical stratum relabeling.
5. Define anti-shortcut design requirements: identical ambiguous prefixes;
   no class-coded trial ID, marker, amplitude, count or total duration;
   matched-order/gap controls and timing-destroyed/reversed controls with
   independently specified outcomes; no target event influencing a scored
   prediction; a causal route/component intervention; label-swapped
   identical-input non-interference; reset and split isolation.
6. Give a pass/not-supported/missing-evidence matrix for the public
   interfaces above, with exact code/ACP references and an explicit request
   for the owner's choice. Do not fill numeric task values from intuition
   or choose rates by calculating which would cross.

Scope bounds: two documents, two design alternatives, eight logical cases,
zero executions, zero new model state, zero scientific samples. All timing
and reward reasoning is event-local or explicitly external evaluation;
no polling clock, synthetic neural tick or unbounded registry.

## Configuration and metric boundaries

No efficacy arm is authorized. `integration=None` is the canonical disabled
default; `IntegrationConfig` has an opt-in `decay_rate_z=0.1` default.
The retained historical two-component setup uses `0.0125`; Luna-55's
supported component comparison is HH/RH/HR/RR with H=`0.0125` and
R=`0.00125`. These are distinct baselines, not interchangeable "default"
names. Their mechanism evidence may inform a later justified choice, but
does not supply task labels, deadlines, a held-out split, or task efficacy.

Do not automatically adopt Luna-58 destination `0.00001`: it was selected
for six previously inspected nonresponders, not an independent task target.
No rate, gain, threshold, input, topology or horizon search is authorized.

Secondary metric requirements for a future contract: TPR/FNR/FPR,
premature/late counts and latency, duplicate count and explicit efficiency
penalty, native prediction matches/errors/expiry, task errors separately,
processed/emitted/routed events, activity/energy proxy units, topology
utilization, queue/budget/pending/clipping/truncation, and replay identity.
No energy or physical-hardware equivalence claim is authorized.

## Stop-on-missing-interface and completion gate

Stop and report **NOT SUPPORTED BY CURRENT GOVERNED INTERFACE** wherever a
proposal requires an unavailable observable, reward recipient, absence
resolution, learning consumer, or causal target path. Do not patch around it.
Missing owner decisions and missing numeric task/split specifications remain
open; draft proposals do not become authorization through publication.

Completion requires the two bounded documents, all eight cases, both
alternatives, precise incompatibility/ACP classification, explicit unresolved
owner decisions, information/reset/resource boundaries and the repository
handoff template. Hardware mapping is conceptual only, not validated.

Luna-0 and the owner must accept the design and close all task construction,
output, timing, population, attribution/no-training, comparator, arm,
budget, metric and anti-shortcut gates before any scientific dispatch.
Published independent Luna-58 review remains a separate open evidence gate
if its result is relied on. Nothing here closes Luna-58 or promotes ACP-0008.
