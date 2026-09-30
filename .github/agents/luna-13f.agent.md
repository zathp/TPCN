---
name: Luna-13F Runtime-Generated Local Candidate Evidence Experiment
description: Determine whether ordinary TPCN runtime activity generates bounded local pre-admission evidence that distinguishes beneficial from harmful structural candidates.
---

# Luna-13F - Runtime-Generated Local Candidate Evidence Experiment

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/architecture_proposals/README.md`,
`workflow/docs/architecture_proposals/ACP-TEMPLATE.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, the Luna-13B, Luna-13C,
corrected Luna-13D and Luna-13E contracts and handoffs, and the independent
Luna-0 Luna-13E review before implementation. Record the exact starting
revision, executed revision/tree, branch and worktree state. Preserve
unrelated changes.

This contract is creation-only until Luna-0 gives a separate explicit
execution assignment. Do not execute Luna-13F while creating or reviewing
this contract. The synchronized reviewed checkpoint is
`8c41267e47bc0543ff9f05e994dc7ea086b23e36`. The Luna-13E substantive review
package is `7faf8d3f1c82927304875bb6263219d5954a463d`; the corrected Luna-13E
implementation reviewed there is `0a53b01b398d461eac3a962431b9ffcdae459e55`.
Verify the actual baseline rather than assuming it remains current.

## Authority, question and classification

Luna-13F is a CPU-only `EXPERIMENT` and `VERIFICATION`. It preserves A01-A15,
does not promote A14, and must not authorize Luna-13G. CUDA, GPU
visualization, FPGA, FPAA and hardware-equivalence work are out of scope; an
optional CUDA skip is non-gating.

The Luna-13E independent result was **PASS WITH FOLLOW-UP - HARMFUL GROWTH
AVOIDED, GENERALITY NOT ESTABLISHED**. G and H were individually legal with
one relevant slot; the canonical controlled scores were G `3.0` and H `0.0`.
No-growth was `2/2`, 8 events, energy `8.0`; G was `2/2`, 12 events, energy
`12.0`; H was `1/2`, 12 events, energy `12.0`. Thus Luna-13E established only
that bounded fixture-controlled observations can avoid H. It did not establish
that deployed neurons/runtime autonomously generate the informative evidence.

The scientific question is:

> Can ordinary event-driven TPCN runtime activity generate, accumulate and
> expose candidate-specific bounded local evidence that predicts the narrow
> G-versus-H structural preference before admission, without fixture-keyed
> score tuples, endpoint-role tables, future outcomes, labels or experiment-
> side score injection?

The required causal chain is:

`runtime events -> local neuron/path state -> candidate-specific accumulated evidence -> canonical score -> one-slot decision -> held-out external outcome`

A positive result may claim only the tested post-pruning fixture supports
harmful-growth avoidance. It must not claim general utility prediction,
broad structural superiority, resource efficiency, scalability, generalization,
hardware equivalence or biological equivalence.

## Ownership and architecture stop condition

Own only the bounded CPU fixture/runner, runtime instrumentation or permitted
experiment-policy exposure, focused tests, machine-readable artifacts,
relevant documentation and
`workflow/handoffs/runtime-generated-local-candidate-evidence-Luna-13F.md`.
Use the current architecture first. Audit whether existing authorized
mechanisms already provide the evidence: local residual/state, observed event
timing and elapsed time, activation history, prediction/error observations,
eligibility, prior reward, route/path use, local clocks, temporal association
state and bounded candidate observations. Prefer existing production/local
state; instrumentation is preferred to new production semantics.

If the current runtime cannot generate the required candidate-specific
pre-admission evidence, stop. Return an architecture-change decision packet
to Luna-0 and the project owner instead of silently adding a learning
subsystem, parallel experiment-only neural state, new normalization, score,
threshold, utility memory, probation, rollback, reward channel or abstention.
The packet must state available evidence, insufficiency, minimal change,
bounded-state/capacity, reset/eviction and timing semantics, pruning/reward
interactions, FPGA/VHDL and FPAA implications, affected clauses, tests,
compatibility and rollback. Do not implement that proposal during Luna-13F.
No ACP or architecture promotion is implied by this contract.

Preserve A01-A08, A11, A14 and A15: event-driven execution, local timestamps
and elapsed time, finite positive propagation, bounded topology/state/dynamics,
local learning, predictive/error events, bounded delayed credit, finite
admission and hardware-neutral semantics. Preserve A09-A10 accounting without
calling activity proxies physical energy. Do not introduce a global neural
timestep, future/held-out information, global topology input, unrestricted
backpropagation, labels, endpoint-role privilege, topology-derived ground
truth, unbounded history or silent budget truncation.

## Runtime-generated evidence protocol

Remove the Luna-13E fixture-controlled G/H evidence tuple from the primary
decision path. The fixture may define input events, topology and candidate
opportunities, but runtime behavior must produce every score-driving
observation. Prohibit primary evidence supplied through candidate-keyed
 dictionaries, G/H lookup tables, preselected score arrays, candidate-role
flags, directly assigned candidate timing tuples, hard-coded beneficial or
harmful fields, externally assigned utility, expected-winner metadata or
post-hoc task results. A candidate identifier may index bounded state only; it
must not determine the evidence value.

Use this phase order:

1. Declare topology/state and a true one-slot competition.
2. Deliver bounded causal event sequences through the normal runtime.
3. Let local neuron/path state evolve naturally and accumulate evidence only
   from those runtime events.
4. Freeze evidence at the structural-decision event.
5. Expose G and H as individually legal candidates and run the unchanged
   canonical structural scorer first.
6. Admit at most one candidate.
7. Evaluate G-selected, H-selected where appropriate, and no-growth conditions
   on held-out external inputs after the decision.

Held-out evaluation events and labels must not enter evidence generation,
scoring or admission. Evidence timestamps must satisfy
`evidence_timestamp <= decision_timestamp`; held-out timestamps must be later.
Future mutations must not alter stored scores. If reward contributes, it must
arrive through real prior runtime delayed-credit events. Prediction/error and
cost terms must be causally available before admission; do not copy future
post-growth event counts into candidate evidence.

For every score-driving observation retain enough provenance to reconstruct
candidate, event ID/type, source, destination, timestamp, receiving local
component, local state before/after where available, elapsed local time,
evidence update and evidence timestamp. Preserve bounded diagnostics without
fabricating unavailable neuron fields. Candidate evidence state must document
owner, per-candidate size, maximum tracked candidates, retention/expiry,
reset, eviction and numeric bounds. No unbounded event log may be required by
runtime decision making; offline artifacts may retain detailed traces.

Where possible derive an analytic expected G/H ordering from the event schedule
and existing local equations before held-out evaluation. Compare measured
runtime evidence and canonical scores to that frozen expectation, not to the
final task result. The unchanged canonical scorer is the first and primary
scorer; do not retune it using held-out outcomes. A score tie or wrong ranking
is an informative negative result.

## Required fixture, controls and measurements

Preserve the Luna-13E G/H interpretation where practical: G preserves the
fixed external task (`2/2`) and H degrades it (`1/2`). Both candidates must be
individually legal, receive matched exposure, and compete for exactly one
relevant structural slot (one relevant free slot). Record total capacity, edge count, fan-in/out, candidate
set, legality, scores, ranks, selected/rejected candidate and reason. No
candidate may win through unrelated structural invalidity.

Require these controls: time-shuffled exposure preserving event/payload
multiset; reversed temporal exposure; uniform-interval exposure; mathematically
valid zero/neutral decay; no-evidence admission; relabeling; mirrored roles;
evidence equalization; candidate-order swap; future-event mutation;
external-label mutation; locality attack; deterministic replay; and bounded
execution.
The higher score must win independent of enumeration order. Equal evidence may
select only by declared deterministic tie-breaking. Mirroring must move the
preference with runtime evidence. Relabeling must preserve equivalent evidence
and decisions. Local evidence for G must not inspect H private state, and
vice versa, unless an existing canonical local mechanism explicitly permits it.

Record for every candidate the actual event observations, exposure window,
local state/diagnostics that exist, evidence updates, score, rank, admission,
decision time and provenance. Record condition, chosen edge, held-out task
result, arrivals/latency, processed/pending events, queue peak, proxy energy
and units, completion and termination reason. Every run retains configured
event budget; `budget_exhausted` runs cannot contribute successful evidence.
There is no global timestep.

Retain the reference outcomes unless runtime-generated dynamics legitimately
change them: no-growth `2/2 @ 8` and energy `8.0`; G `2/2 @ 12` and energy
`12.0`; H `1/2 @ 12` and energy `12.0`. If G remains equal to no-growth,
explicitly report harmful-growth avoidance, not task or resource improvement.

## Artifacts and provenance

Produce a machine-readable runtime evidence artifact equivalent to:

`Candidate | Runtime observations | Derived local evidence | Score | Rank | Admitted`

and provenance equivalent to:

`Observation | Candidate | Event/time | Source/destination | Local state before/after | Update | Evidence time`

Evaluation records must include:

`Condition | Chosen edge | Task result | Events | Proxy energy | Completion`

Artifacts and handoff must include starting/executed revision and tree,
generation dirty state, branch, fixture identity, event schedule, candidate
definitions, runtime evidence records, score configuration, decision time,
one-slot topology, held-out task/split, seeds, event/queue budgets and
environment. Compare prior Luna-13E tuples only diagnostically; they must not
drive the primary decision.

## Outcomes and terminal statuses

Use exactly one terminal status:

- `PASS - RUNTIME-GENERATED LOCAL EVIDENCE SUPPORTS HARMFUL-GROWTH AVOIDANCE, READY FOR LUNA-0 REVIEW`
- `PASS WITH FOLLOW-UP - RUNTIME EVIDENCE DISTINGUISHES CANDIDATES, GENERALITY NOT ESTABLISHED`
- `NEGATIVE RESULT - RUNTIME EVIDENCE GENERATED BUT DOES NOT PREDICT USEFUL GROWTH`
- `NEGATIVE RESULT - CURRENT RUNTIME DOES NOT GENERATE DISTINGUISHING PRE-ADMISSION EVIDENCE`
- `BLOCKED - ARCHITECTURE CHANGE REQUIRED FOR RUNTIME EVIDENCE`
- `BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION`
- `BLOCKED - CAPACITY COMPETITION INVALID`
- `BLOCKED - INVARIANT REGRESSION`
- `BLOCKED - REGRESSION`

Outcome A is valid only when runtime evidence selects G over H and survives
controls. Outcome B is valid when runtime evidence differs but unchanged
canonical scoring ties/selects H/inconsistently. Outcome C is valid when
runtime generates no distinguishing evidence. Outcome D requires the
architecture-change packet. Outcome E blocks any result depending on fixture
identity or oracle leakage.

## Required validation and handoff

Focused tests must cover fixture-keyed evidence removal, runtime generation,
causal timestamps, bounded candidate state, score reconstruction, one-slot
competition, time shuffle, reversal, uniform intervals, neutral decay,
no-evidence, relabeling, mirrored roles, equalized evidence, candidate order,
future exclusion, label isolation, locality, deterministic replay and bounded
execution. Then run preservation coverage for Luna-13E, corrected Luna-13D,
Luna-13C, Luna-13B, Stage-0, relevant Luna-12H/Luna-12N behavior, the full
CPU suite, compile/static checks, diagnostics and `git diff --check`. CUDA is
optional and non-gating.

The handoff must explicitly answer: what fixture evidence was removed; what
runtime mechanism and production/local state generated evidence; whether it is
bounded; which events produced G/H evidence; whether evidence preceded
admission; whether canonical scores used it directly; G/H scores and admitted
candidate; order, relabel, mirror, shuffle, reversal, interval, decay,
no-evidence, label and future-control results; whether G preserved utility;
whether no-growth remained cheaper; whether the runtime evidence predicts the
narrow distinction; whether an architecture change is required; and what
remains unproven. Label narrative evidence `OBSERVED`, `INFERRED` or
`HYPOTHESIZED`, and classify checks passed, failed, not run or not applicable.
Return to Luna-0 for independent review. Luna-13F must not authorize, create
or dispatch Luna-13G.
