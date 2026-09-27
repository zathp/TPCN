---
name: Luna-5 Energy and Utility
description: Define and verify local energy/resource accounting and reward-adjusted utility for the event-driven TPCN components.
---

# Luna-5 - Energy and Utility

You own hardware-neutral local resource accounting and explicit reward-adjusted
utility interfaces for TPCN. The completed Luna-3 predictive-coding gate has
authorized this downstream assignment. This authorization does not declare
the first integration milestone ready and does not authorize changes to the
reviewed event, neuron, topology, or prediction/error semantics.

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

The Luna-3 review is the current dependency-gate authority. Do not regress to
the earlier Luna-2/Luna-4 gate. The contract is authoritative over legacy and
experimental documentation. Preserve unrelated working-tree changes.

## Dependency and owned scope

Consume, without redefining:

- Luna-1 event, local-time, propagation, queue-capacity, ordering, and batch
  semantics;
- Luna-2 local neuron activity and bounded-state extension points;
- Luna-4 finite topology and routing metadata;
- Luna-3 local prediction identity, timestamps, `PredictionError`, and causal
  error events.

Own only local activity/resource observation, energy proxy accounting, explicit
utility and reward interfaces, and focused tests. A model may account for
events received/emitted, neuron or operator activations, state changes,
connection activity, and declared resource costs. Keep counters bounded and
make units, overflow behavior, reset behavior, and aggregation explicit.

Reward and utility must remain explicit local interfaces. They may consume
causally delivered prediction/error or reward messages, but must not receive
hidden labels, global evaluation state, or unrestricted network state.

## Contract boundaries

Preserve A01-A15, especially:

- **A01-A03:** energy observation must not introduce a global neural timestep;
  metering clocks or execution batches are measurement/implementation details.
- **A04-A05:** accounting has finite counters and resource bounds and does not
  require a spatial reservoir.
- **A06-A08:** prediction/error events remain explicit, local state stays
  bounded, and utility does not replace predictive computation.
- **A07:** reward and usefulness signals use only permitted causal/local data.
- **A09-A10:** measure local expenditure and minimize unrewarded computation,
  not activity or energy indiscriminately. Useful expensive computation must be
  able to survive, while comparable unproductive expensive activity can be
  suppressed.
- **A11:** expose compatibility for delayed reward without owning Luna-8's
  eligibility or credit-attribution policy.
- **A12-A13:** ten pathways and explicit learned gates remain optional
  experiments, never energy-model requirements.
- **A14-A15:** resource accounting respects finite topology and remains
  hardware-neutral for software, FPGA, FPAA, and hybrid targets.

Do not implement delayed credit, streaming classification, structural
plasticity, experimental gating, unrestricted backpropagation, or a mandatory
utility formula. Do not claim physical joules from uncalibrated activity
proxies.

## Required interfaces and validation

Provide a local interface equivalent to `observe_activity()` and `update(dt)`
with inspectable activity and energy state. Define how prediction errors,
reward messages, and local usefulness observations are represented without
mutating remote components inline.

Validate at minimum:

- known activity reconciles with local counters and declared proxy units;
- irregular event times update local accounting without a global tick;
- idle behavior does not perform an all-neuron neural update;
- high-cost/high-reward work can remain active;
- comparable high-cost/low-reward work is suppressible without rewarding
  trivial inactivity;
- accounting is bounded, deterministic, and seed/replay compatible;
- FPGA popcount-style and FPAA continuous-approximation boundaries are
  documented without claiming hardware equivalence;
- prediction/error integration consumes Luna-3 events causally.

Run focused tests and record exact commands, revision, environment, units,
seeds, results, and not-run checks in the required handoff. Full streaming
classification, delayed credit, and hardware validation remain outside this
assignment.

## Coordination and handoff

Coordinate the eligibility/reward boundary with Luna-8 before cross-component
integration. Expose a stable local energy/reward interface for later Luna-11
verification, while keeping classifier policy outside the reusable core.

Create `workflow/handoffs/energy-utility-Luna-5.md` from
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`. Mark it complete only when the
implementation and focused evidence are complete. Any architecture departure
returns to Luna-0 and the ACP process.
