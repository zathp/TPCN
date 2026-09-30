---
name: Luna-13E Post-Pruning Admission Quality and Harmful-Growth Discrimination Experiment
description: Determine whether bounded local pre-admission evidence can distinguish beneficial from harmful structural growth after evidence-based pruning.
---

# Luna-13E - Post-Pruning Admission Quality and Harmful-Growth Discrimination Experiment

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/architecture_proposals/README.md`,
`workflow/docs/architecture_proposals/ACP-TEMPLATE.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, the Luna-13B and Luna-13C
contracts and handoffs, the corrected Luna-13D contract and handoff, and the
independent Luna-0 review of corrected Luna-13D before implementation.
Record the exact starting revision, executed revision/tree, branch and
worktree state. Preserve unrelated changes.

This contract is creation-only until Luna-0 gives a separate explicit
execution assignment. Do not execute Luna-13E while creating or reviewing
this contract. The final independently reviewed Luna-13D state is
`b7e3bdc6028381a5fa6912c0212aff79528beae1`; verify the actual baseline rather
than assuming it remains current. The corrected implementation revision was
`9ae2fb6574a4a45fa6a47c18e9aa7270bd4d3080`. The independent review status was
`PASS WITH FOLLOW-UP — RETENTION/PRUNING VERIFIED, USEFUL ADAPTATION NOT
ESTABLISHED`.

## Authority, question and classification

Luna-13E is a CPU-only `EXPERIMENT` and `VERIFICATION`. It preserves A01-A15,
does not promote A14, and must not authorize Luna-13F. CUDA, GPU
visualization, FPGA, FPAA and hardware-equivalence work are out of scope; an
optional CUDA skip is non-gating.

The scientific question is:

> After evidence-based pruning frees finite capacity, can existing local causal
> evidence distinguish a task-beneficial candidate from a harmful candidate
> before one is admitted, without external labels, future task outcomes,
> endpoint identity or post-hoc oracle information?

Luna-13B established local temporal evidence changing structural choice.
Luna-13C established a narrow causal external task effect. Corrected Luna-13D
established evidence-based retention/pruning and capacity release, but not
useful post-pruning adaptation or resource efficiency. Luna-13E investigates
why ordinary legal post-pruning growth can degrade the task.

A successful result must show discrimination from valid pre-admission evidence,
not merely that the experiment's G candidate is useful and H candidate is
harmful. A failure is a valid result when the current architecture cannot
make that distinction.

## Ownership and architecture boundary

Own only the bounded CPU fixture/runner, experiment-policy exposure required
to inspect the existing admission path, focused tests, machine-readable and
human-readable artifacts, relevant documentation and
`workflow/handoffs/post-pruning-admission-quality-Luna-13E.md`.

First audit the architecture and implementation to identify evidence
legitimately available before structural mutation. Candidate evidence may
include temporal association, residual/local state, prediction/error evidence,
eligibility, prior reward evidence, route-use statistics, local cost,
reward-adjusted cost or other already-authorized bounded local signals. For
every decision-driving field record its source, owner, local timestamp,
availability time, locality, boundedness, future-event dependency,
label dependency and endpoint-identity dependency.

Do not assume a utility-aware admission mechanism exists. Do not invent production state,
a new score, weighting, threshold, utility memory,
predicted-cost model, probation edge, rollback trial, reward channel,
protected candidate class or global task score merely to make G win. Do not
use a post-admission event count as pre-admission cost evidence. Do not add
abstention if the architecture does not already permit it. Do not alter
Luna-13D pruning rules to avoid H.

If reliable discrimination requires an unauthorized mechanism, stop that
portion and return an architecture-change decision packet to Luna-0 and the
project owner containing: evidence available before admission; why it is
insufficient; the minimal additional local evidence proposed; bounded-state
implications; hardware implications; required contract changes; required
tests; compatibility and rollback. Do not silently implement the mechanism.
An ACP is required for a real architecture departure. A permitted experiment
must remain explicitly experimental.

Preserve event-driven execution, local timestamps and elapsed time, finite
positive propagation, predictive/error events, local learning, delayed credit,
bounded topology/state/queues/history, finite structural admission and
pruning, deterministic replay, label isolation and hardware-neutral
semantics. Do not introduce a global neural timestep, future preprocessing,
future/held-out information, endpoint-role lookup, unrestricted
backpropagation, topology-derived ground truth, unbounded candidate history,
instantaneous edge effects or silent budget truncation.

## Reuse and required reference result

Begin after legitimate Luna-13D pruning has freed capacity. Reuse the fixed
Luna-13C/13D external task, decision rule, target definitions, timing and
resource units where practical. Before testing discrimination, reproduce the
verified negative post-growth result exactly enough to diagnose it:

- baseline/post-pruning: `2/2`, 8 processed events, proxy energy `8.0`;
- harmful post-growth: `1/2`, 16 processed events, proxy energy `16.0`.

Trace routes, arrivals, local timing, target state, event count and relevant
prediction/error evidence. Identify exactly how the harmful relay changes one
case. This trace is diagnostic only; its held-out result must not enter
admission.

Keep task utility separate from resource cost. Report raw case counts,
arrival latency, routes, processed/pending events, queue peak, proxy energy
and units, completion, edge count and capacity. A useful expensive candidate
may remain useful; a harmful cheap candidate may still be harmful.

## Frozen G/H one-slot fixture

Before comparing policies, predeclare two structurally legal candidates:

- **G**: beneficial under the fixed held-out external task;
- **H**: harmful or materially utility-degrading under that same task.

The experiment may construct these candidates deliberately, but the admission
mechanism must not receive beneficial/harmful flags, expected task score,
future outcome, endpoint-role table or hard-coded candidate identity. Ground
truth is for external evaluation only and must be frozen before policy
comparison.

Create a true forced competition with exactly one relevant free slot (one
newly freed structural slot). G and H must both be individually legal before ranking and
must receive equal opportunity. Do not admit both and call ranking a
successful discrimination. Record topology before competition, capacity,
fan-in/out, candidate set, candidate evidence, scores, ranks, chosen and
rejected candidates, rejection reason and final graph/fingerprint.

The required candidate evidence table is equivalent to:

| Candidate | Temporal evidence | Utility/reward evidence | Cost evidence | Score | Rank | Admitted | Held-out task |
|---|---|---|---|---:|---:|---:|---|

The required provenance table is equivalent to:

| Field | Candidate | Source/owner | Available time | Decision time | Local | Bounded | Pre-admission | Future/label/identity dependent |
|---|---|---|---|---|---:|---:|---:|---|

Record field-level provenance, not only a final aggregate score.

## Admission policy and controls

Run the current post-pruning admission policy unchanged first. Report whether
it chooses G, H, a tie or neither. If it chooses H, preserve that negative
result. If current policy already distinguishes them, report the exact
legitimate mechanism without generalizing utility prediction.

Where feasible, ablate existing evidence terms mechanistically and in a small
predeclared matrix: temporal evidence only; utility/reward evidence removed;
cost evidence removed; residual-state evidence removed; prediction/error
evidence removed. Separate score, rank, admitted edge and external outcome.
Where the implemented rule permits it, freeze an analytic/predeclared G/H
ordering from pre-admission evidence before held-out evaluation and compare
predicted admission, actual admission and held-out outcome.

Required controls are:

- fixed/no-new-growth post-pruning state;
- equal-opportunity random candidate choice with genuine independent seeds;
- mirrored candidate roles with beneficial/harmful roles shifted while endpoint
  labels do not answer the question;
- relabeling preserving topology, timing, evidence, capacity and task
  semantics;
- evidence-equalized G/H control, where identity alone must not create a
  utility preference;
- future-event delivery/withholding after the decision;
- external-label/metadata mutation with runtime evidence unchanged; and
- any existing admission score threshold, confidence threshold or abstention
  behavior tested operationally.

A deterministic tie-break must be reported as tie-breaking, not utility
discrimination. If architecture forces growth whenever a positive score is
present, document that; do not invent abstention. If no meaningful threshold
exists, report its absence rather than adding one.

For every random seed record selected candidate, task result, events, energy
and completion. Do not claim broad random-policy superiority. Include a
fixed/no-growth condition because Luna-13D showed that no growth can
outperform harmful growth.

## Information and causality gates

Every decision-driving field must have existed before mutation and must be
local or otherwise explicitly authorized. Future task results, held-out
labels, external evaluation metadata, post-admission traffic, endpoint
identity and post-hoc oracle fields must not alter a computed ranking.

If prior reward is used, demonstrate that it arrived causally before admission
through the authorized bounded delayed-credit mechanism. Do not fabricate
history for the designated beneficial candidate. If pre-exposure is needed,
keep it bounded and matched. Mutating labels or evaluation metadata without
changing runtime evidence must leave candidate evidence, score, rank,
admission and pre-output computation unchanged. Future events delivered after
the decision must not retroactively change it.

Relabeling and mirrored controls must show that preference follows evidence,
not node names, direction/name privilege or candidate identity. Equalized
evidence must not support a utility claim even if a stable tie-break chooses
one candidate.

## Bounded execution and artifacts

Every run must retain event budget, processed events, pending events, queue
peak where available, termination reason and `completed` versus
`budget_exhausted`. An exhausted run is not task evidence. No global timestep
or silent truncation is permitted. Candidate/evidence state must remain
bounded and preserve existing replay guarantees.

Artifacts and handoff must include baseline revision, executed revision/tree,
generation dirty state, branch, fixture identity, post-pruning graph identity,
G/H definitions, field-level evidence provenance, capacity and fan-in/out,
scoring configuration, frozen evaluation target, split, seeds, event/queue
budgets, environment, routes, arrivals, target state, prediction/error
records, task results, events, energy, latency and termination status.

Include tables equivalent to:

| Policy/control | Chosen candidate | Task result | Events | Proxy energy | Latency | Completion |
|---|---|---|---:|---:|---|---|

| Field | Candidate | Available before decision | Used in score/rank | Evidence source | Local/bounded |
|---|---|---:|---:|---|---|

## Validation and preservation

Focused tests must cover harmful-growth reproduction and trace, beneficial
candidate validation, one-slot legal G/H competition, provenance,
endpoint-independent scoring, current-policy baseline, score/rank/admission
separation, analytic prediction where applicable, relabeling, mirrored roles,
evidence-equalized control, future exclusion, label isolation, reward/evidence
causality, cost-awareness boundary, existing threshold/abstention behavior,
random selection, fixed/no-growth, bounded evidence state, deterministic
replay and bounded execution.

Then run regressions for corrected Luna-13D, Luna-13C causal utility,
Luna-13B crossover, Stage-0 invariants, relevant Luna-12H and Luna-12N
behavior, the full CPU suite, compile/static checks, repository diagnostics and
`git diff --check`. CUDA remains optional and non-gating. Separate passed,
failed, not-run and not-applicable checks. Do not execute Luna-13F.

The handoff must answer explicitly:

1. What exactly caused harmful Luna-13D growth to degrade the task?
2. What beneficial candidate was used, and were G and H both legal?
3. Was there exactly one relevant free slot?
4. What evidence existed before admission and which fields affected ranking?
5. Did current policy choose G, H, tie or neither?
6. Did preference survive relabeling and mirrored roles?
7. Did label mutation leave admission unchanged and future events excluded?
8. Could local evidence predict task usefulness or resource cost?
9. Did no-growth outperform harmful growth?
10. Does current architecture permit abstention?
11. Is an architecture change necessary for reliable beneficial admission?
12. What exact claim is supported and what remains unproven?

Label narrative evidence `OBSERVED`, `INFERRED` or `HYPOTHESIZED`, and classify
every check. Return all results to Luna-0 for independent review.

## Terminal statuses and promotion boundary

Use exactly one terminal status:

- `PASS — PRE-ADMISSION EVIDENCE DISTINGUISHES BENEFICIAL FROM HARMFUL GROWTH, READY FOR LUNA-0 REVIEW`
- `PASS WITH FOLLOW-UP — BENEFICIAL ADMISSION ESTABLISHED, GENERALITY NOT ESTABLISHED`
- `NEGATIVE RESULT — CURRENT PRE-ADMISSION EVIDENCE DOES NOT PREDICT USEFUL GROWTH`
- `BLOCKED — ARCHITECTURE CHANGE REQUIRED FOR UTILITY-AWARE ADMISSION`
- `BLOCKED — ORACLE/FUTURE EVIDENCE CONTAMINATION`
- `BLOCKED — CAPACITY COMPETITION INVALID`
- `BLOCKED — INVARIANT REGRESSION`
- `BLOCKED — REGRESSION`

A narrow positive claim may state only that under the tested post-pruning
fixture, valid local causal pre-admission evidence distinguished beneficial
from harmful growth under one-slot competition and the selected admission
preserved the fixed task. A negative result may state that under the current
architecture the tested candidates could not be reliably distinguished before
commitment. Neither result generalizes beyond the fixture or changes A01-A15.

Luna-13E must return to Luna-0 for independent review. It must not authorize,
create or dispatch Luna-13F. No architecture change, utility-aware admission,
probation or rollback mechanism is authorized by this contract.
