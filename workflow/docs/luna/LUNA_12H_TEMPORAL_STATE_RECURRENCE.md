# Luna-12H - Intrinsic Temporal State, Recurrence, and Unequal-Delay Convergence

## Status and boundary

Luna-12H is authorized by Luna-0 on 2026-09-27 after the Luna-12G benchmark
showed identical ordered, shuffled, and reversed classification results. It is
an implementation and verification milestone for the software reference. No
ACP is required because A01-A03 and A08 already permit local elapsed-time
state, finite propagation and bounded recurrent dynamics; this document makes
those permitted semantics explicit and testable.

This milestone does not authorize a real handwriting benchmark, hardware
acceptance, a global neural timestep, or an architecture-wide classifier
redesign. Luna-13 and Luna-14 remain independent siblings.

## Motivation

The Luna-12G controls measured 0.53125 for fixed-topology learning,
structural-plasticity learning, shuffled order and time reversal. That result
is evidence that the current software-reference path does not demonstrate
meaningful temporal-order sensitivity. Before adding an external temporal
classifier, verify whether temporal information exists in the neural core.

Do not count external readout labels or accuracy as evidence of core temporal
state. Do not add spiral-handedness logic to a neuron.

## Canonical semantics

A TPCN neuron is a stateful event transform, not merely a memoryless event
transform. For local time `t0` and a later incoming event at `t1`, the reference
semantics are:

```text
s(t1-) = Phi(s(t0+), t1 - t0)
s(t1+) = F(s(t1-), event_t1)
```

The implementation may evaluate `Phi` analytically when an event is processed.
It need not update idle neurons or step through intermediate times. The state,
decay/evolution rule, bounds, time units and reset boundaries must be explicit.
Elapsed time must come from canonical event timestamps and local neuron time.

The reference neuron must expose at least one deterministic fixture where:

```text
F(F(s, e1), e2) != F(F(s, e2), e1)
```

in state, output or trace. This is a required capability fixture, not a claim
that all parameters or workloads must be order-sensitive.

A single event must be able to alter local state observable later before a
character/sequence reset. State persists within that boundary. Pending events,
prediction state, eligibility and internal temporal state require a declared
reset policy. Topology may persist independently. There is no state leak
between examples unless explicitly authorized.

## Routing and recurrence

Finite propagation uses declared edge delays and cumulative path delay. Verify
both:

```text
A -> C
A -> B -> D -> C
```

with `D_long > D_short`, regardless of hop-count comparisons. Fan-in retains
event timestamps and canonical deterministic ordering; different-time events
must not be silently collapsed into an unordered sum before processing.

The routing path must support an older event on the long path converging with a
newer event on the short path. Changing their relative arrival timing must
change downstream state/output in at least one deterministic fixture. Recurrent
cycles remain bounded by existing event budgets, lineage/path safeguards,
queue bounds, topology limits, state bounds, monotonic local time and tie
ordering. No infinite propagation or hidden recurrent tick is permitted.

If local internally scheduled events already exist or can be exposed without
semantic invention, document and bound them. Do not add autonomous events only
to satisfy this milestone when analytic event-time evolution is sufficient.

## Required fixtures

1. **Intrinsic state:** `+1 at t=0` then observe state before reset.
2. **Ordered pair:** `+1 at t=0, -1 at t=1` versus `-1 at t=0, +1 at t=1`.
3. **Equal multiset:** same event values and multiplicities, different order.
4. **Changed interval:** `+1 at t=0, -1 at t=1` versus `+1 at t=0, -1 at t=5`.
5. **Unequal paths:** direct and multi-hop cumulative delays and exact arrivals.
6. **Convergence:** older long-path and newer short-path consequences near the
   same downstream comparison interval, with a timing-relationship control.

Fixtures 1-4 must identify the observed state/output/trace and declared reset.
Fixtures 5-6 must include edge delays, cumulative delays, emission/arrival
timestamps, queue order, downstream result, and pruning intervention.

## Required acceptance checks

1. Single-spike temporal-state persistence.
2. Ordered-pair noncommutativity.
3. Equal-event multiset and different-order distinction.
4. Unequal path delay.
5. Multi-hop cumulative delay.
6. Convergent old/new arrival interaction.
7. Long/short path pruning removes its future effect.
8. Same total input with different arrival timing differs downstream in one
   deterministic fixture.
9. Character reset removes prior temporal state.
10. Same-seed determinism.
11. Bounded recurrence/cycle behavior.
12. Label isolation.

Record passed, failed, not-run and not-applicable results. A failure to expose
temporal state is a valid finding and blocks a claim that the neural core
preserves temporal information; it does not justify silently moving the
requirement into the external readout.

## Non-goals and compatibility

Do not introduce synchronous whole-network stepping, global frame updates, a
spatial reservoir, future-point preprocessing, label input, unbounded state,
second topology models, or spiral-specific computation. Preserve existing
A01-A15 behavior, hardware-neutral event interfaces, predictive/error events,
local learning, delayed credit, energy accounting, and downstream-only
visualization.

## Completion evidence

The handoff must include the baseline revision, exact commands, time units,
state/evolution and reset policy, event/tie/queue policies, capacities, path
and edge delays, seeds, fixture traces, focused and regression test results,
compile/diagnostic status, and an explicit Luna-0 readiness decision. No
hardware equivalence or classification threshold is implied.
