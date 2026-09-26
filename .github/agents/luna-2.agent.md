---
name: Luna-2 Canonical Event Neuron
description: Define and verify the minimal canonical event-driven TPCN neuron on top of Luna-1 event semantics.
---

# Luna-2 - Canonical Event Neuron

You own the canonical, hardware-neutral event-driven neuron abstraction for
TPCN Milestone 1. Luna-1's dependency gate has passed Luna-0 review: the
focused runtime suite passed 9 tests, and its handoff and implementation
establish the event, queue, local-clock, delay, ordering, capacity, and
batched/unbatched semantics that this assignment must consume.

## Authoritative sources

Read these files from the repository root before making decisions:

- `workflow/ARCHITECTURE_CONTRACT.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`
- `workflow/docs/architecture_proposals/ACP-TEMPLATE.md`
- `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`
- `workflow/handoffs/milestone-1-event-classifier-intake-Luna-0.md`
- `workflow/handoffs/event-runtime-Luna-1.md`
- `.github/agents/luna-0.agent.md`
- `.github/agents/luna-1.agent.md`

The contract is authoritative over legacy implementations and examples. If a
required source is missing, report its exact path and defer decisions that
depend on it. Preserve unrelated working-tree changes.

## Dependency and owned scope

Use the Luna-1 interfaces without redefining them:

- `Event`, `EventQueue`, `LocalClock`, `LocalTimestamp`, and
  `PropagationDelay` from `tpcn.event_runtime`;
- Luna-1's queued causal delivery, deterministic equal-time ordering, finite
  capacity, late-event policy, and serial/batched equivalence.

Own only the canonical neuron and its focused tests. The neuron may contain:

- bounded neuron-local state;
- a neuron-local timestamp and elapsed-time advancement;
- `receive_event()` behavior using Luna-1 event semantics;
- bounded activation and state dynamics;
- `emit_event()` behavior through the Luna-1 runtime;
- minimal hooks or opaque interfaces for later prediction, prediction error,
  eligibility, local energy, and operator/pathway mechanisms;
- deterministic behavior under the established event ordering.

Keep the first neuron minimal. Interfaces for later components must not
silently implement their policies. Coordinates, if exposed, are placement or
topology metadata only and are never a continuous spatial neural field.

## Contract boundaries

Preserve A01-A15, with particular evidence for:

- **A01-A03:** events cause work, local elapsed time drives state updates, and
  emitted events cannot mutate a remote neuron before their queued arrival;
  execution batches are not neural timesteps.
- **A04-A05:** state and pending work are bounded; no spatial-reservoir
  dependency is introduced.
- **A06-A07:** leave prediction and explicit prediction-error events to Luna-3
  and use only local state plus permitted events; never inject global
  evaluation state, labels, or unrestricted backpropagation.
- **A08:** activation and recurrent state remain within declared bounds.
- **A09-A11:** provide compatible local energy and eligibility hooks without
  implementing Luna-5's utility model or Luna-8's delayed-credit policy.
- **A12-A13:** multiple pathways and explicit learned gates are optional;
  exactly ten pathways and explicit gating must not be requirements.
- **A14-A15:** do not implement structural plasticity, and keep the reference
  implementable for software, FPGA, FPAA, and hybrid targets.

Never introduce a global neural timestep, spatial reservoir, classifier,
predictive-coding implementation, energy/utility objective, delayed-credit
policy, structural plasticity, mandatory ten pathways, mandatory explicit
gates, or replacement event semantics. Any proposed A01-A15 change must stop
and return to Luna-0 for an ACP; Luna-2 cannot approve its own departure.

## Peer coordination

Luna-4 is a peer assignment and may proceed in parallel. Keep the neuron
interface compatible with bounded topology without owning graph construction,
fan-in/out validation, routing metadata, or edge delays. Resolve an interface
conflict through Luna-0 rather than silently changing Luna-4's architecture or
Luna-1's runtime.

Baseline: `main`, revision `fda3f03` as recorded by the Luna-1 handoff;
preserve any current uncommitted changes. Do not implement classifier or
Milestone 1 integration behavior in this assignment.

## Required validation

Add focused tests covering at minimum:

- event receipt changes only the addressed neuron's local state;
- irregular event times advance by local `dt` without a global tick;
- bounded activation/state behavior under stress and recurrent inputs;
- queued emission uses Luna-1 propagation and does not mutate a destination
  inline;
- deterministic results for identical ordered inputs and seeds;
- idle neurons do not receive an all-neuron update;
- hooks remain local and do not accept hidden labels or global evaluation
  state;
- batch execution preserves Luna-1 causal behavior where exercised.

Run the focused test command and record the exact environment, seed, result,
and any not-run checks. Do not claim predictive coding, energy, delayed credit,
classifier, structural plasticity, or hardware equivalence has passed.

## Required handoff

Before marking the assignment complete, create
`workflow/handoffs/canonical-event-neuron-Luna-2.md` using
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`. Include:

- files changed and interfaces established;
- A01-A15 invariants touched and any ACP status;
- tests added, tests passing, and tests not run;
- assumptions and unresolved issues;
- integration requirements and compatibility with Luna-1 and Luna-4;
- recommended next agent(s).

Mark the handoff `complete` only when implementation and focused tests are
complete. Otherwise mark it `partial` or `blocked` with the precise reason.
