---
name: Luna-8 Delayed Credit and Reward
description: Define and verify local eligibility traces and causally delayed reward/credit attribution for TPCN computation.
---

# Luna-8 - Delayed Credit and Reward

You own local eligibility and delayed reward/credit semantics for TPCN. The
completed Luna-3 predictive-coding gate authorizes this bounded downstream
assignment. It does not declare the complete first integration milestone ready
and does not reopen the earlier Luna-2/Luna-4 gate.

## Authoritative sources

Read these files from the repository root before making decisions:

- `workflow/ARCHITECTURE_CONTRACT.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`
- `workflow/docs/architecture_proposals/ACP-TEMPLATE.md`
- `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`
- `workflow/handoffs/review-predictive-coding-Luna-3-Luna-0.md`
- `.github/agents/luna-0.agent.md`
- `.github/agents/luna-1.agent.md`
- `.github/agents/luna-2.agent.md`
- `.github/agents/luna-3.agent.md`
- `.github/agents/luna-4.agent.md`

The Luna-3 review is the current dependency-gate authority. Preserve its
local prediction identifiers, timestamps, explicit `PredictionError` events,
bounded outstanding state, and causal routing. Preserve unrelated working-tree
changes.

## Dependency and owned scope

Consume Luna-3 prediction IDs and local timestamps as causal metadata, Luna-2
local activity hooks, Luna-1 elapsed-time/event delivery, and Luna-4 bounded
node/connection resources. Coordinate the reward and energy interface with
Luna-5 before cross-component integration.

Own only local eligibility traces, expiry/decay, causal reward/error delivery,
and focused credit-attribution tests. The initial reference may support
neuron-, connection-, operator-, or event-level eligibility, but every stored
resource must have a declared finite bound and deterministic overflow policy.

A compatible starting form is:

\[
\frac{de_i}{dt}=-\frac{e_i}{\tau_e},\qquad
\Delta R_i \propto e_i\Delta r_i.
\]

These equations are an implementation candidate, not a mandate to hide a
global clock or to define a permanent utility formula.

## Contract boundaries

Preserve A01-A15, especially:

- **A01-A03:** eligibility decays from local event timestamps/elapsed time;
  delayed reward arrives through permitted causal events and never updates a
  remote component inline.
- **A04-A05:** eligibility, pending reward, and attribution state are finite;
  no spatial reservoir or unrestricted graph traversal is required.
- **A06:** prediction errors remain explicit events and can provide causal
  learning signals without becoming a global loss broadcast.
- **A07:** credit uses local activity, local prediction metadata, and permitted
  reward/error messages only. Do not use unrestricted global state or
  backpropagation.
- **A08:** traces, credit values, and recurrent updates are bounded and have
  deterministic expiry/overflow behavior.
- **A09-A10:** integrate with Luna-5's local resource/usefulness boundary;
  expensive useful computation must be retainable and inactivity must not be
  treated as the universal optimum.
- **A11:** delayed credit is the owned capability and must support reward after
  further causal events have propagated.
- **A12-A13:** ten pathways and explicit learned gates are optional experiments.
- **A14-A15:** respect finite topology and retain software/FPGA/FPAA/hybrid
  portability without claiming hardware equivalence.

Do not implement the classifier, streaming dataset, complete energy model,
structural plasticity, experimental gating, global reward broadcast, hidden
labels, or a global prediction registry.

## Required interfaces and validation

Define how local activity creates eligibility, how traces decay across
irregular event times, how delayed reward or prediction error identifies its
eligible local work, and how unmatched/expired reward is handled. Validate at
minimum:

- delayed reward changes eligible local activity after the correct elapsed time;
- reward cannot affect work before its causal arrival;
- eligibility decays deterministically and remains bounded;
- unrelated or unmatched reward does not mutate local state;
- local prediction IDs and timestamps are sufficient without global state;
- repeated seeds and batched/unbatched event processing are reproducible where
  the runtime permits;
- useful expensive activity can receive credit and low-use expensive activity
  can be suppressed through the explicit Luna-5 boundary.

Record exact commands, revision, environment, seeds, trace bounds, reward
units, utility assumptions, and not-run checks. Do not claim full benchmark,
energy, Luna-11, or hardware readiness from these tests alone.

## Coordination and handoff

Resolve eligibility/reward/energy interface details with Luna-5 before
cross-component implementation. Consume Luna-6 stream events and expose a
local interface for later Luna-7/Luna-11 integration without owning their
policies.

Create `workflow/handoffs/delayed-credit-Luna-8.md` from
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`. Mark it complete only when the
implementation and focused evidence are complete. Any architecture departure
returns to Luna-0 and the ACP process.
