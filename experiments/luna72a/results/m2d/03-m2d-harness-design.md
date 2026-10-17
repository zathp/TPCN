# Luna-72A-M2D Isolated E1 Harness Design

## Status

Design only under owner-authorized Option 1. No harness, executable source, or
test is implemented. The design does not substitute E1 into R3 or the
production E2 runtime.

## Experimental boundary

The harness composes three standalone `SingleExcursionNeuron` instances with
the existing `EventQueue` and static `BoundedTopology` primitives:

```text
B --edge-BX--> X --edge-XD--> D
```

The two positive-delay Model-B edges are immutable during a trial. There are
no other nodes, edges, incoming inputs at X in the primary condition, or
incoming inputs at D. The route is acyclic and has maximum depth two. It does
not include `ExcursionCharacterRuntime`, which currently accepts E2
`MultiExcursionNeuron`, and does not call R3 `Engine.drain`.

Harness responsibility is limited to:

1. Build fresh B/X/D E1 instances, a bounded queue and the frozen topology.
2. Admit only the declared trial's exogenous root events.
3. Dequeue events in established timestamp/sequence order and dispatch each
   addressed event to exactly one E1 instance.
4. Pass the actual shared bounded queue to E1 so valid local `S_EMIT` and
   `S_REARM` events are scheduled by the existing neuron implementation.
5. If E1 returns an `ExcursionEmission`, construct the corresponding
   excursion event using its distinct emission identity/lineage and submit it
   to the existing topology route API.
6. Record bounded observer-only state/route evidence. Observer data must not
   mutate E1 state, payloads, identities, edge weights or queue order.
7. Stop on completion or any frozen bound/invariant failure; never silently
   drop or retry events.

This is an adapter composition contract, not an existing runtime interface.
The future exact API signatures must match the verified current APIs in
`02-m2d-e1-interface-audit.md`. The implementation must call E1's methods for
decay, contribution integration, threshold handling, internal-event
validation, emission and rearm; it must not reimplement those equations.

## Fixed proposed E1 configurations

Use ACP-0004 E1 ordinary excursion only: no M/multi-excursion region is
entered, no ACP-0008 slow integration is enabled, and no prediction/error,
eligibility, reward, learning, adaptation, or labels enter the neural path.
All configurations satisfy the accepted strict parameter constraints. Each
neuron starts neutral with `x=0`, local time `0`, no pending event and empty
provenance. The exact `E1Config` field names must follow source; values below
are the proposed numeric contract, not a source-code constructor signature.

| Neuron | `lambda` | `X_max` | `theta_R` | `theta_E` | `theta_hold` | `theta_M` | `Delta_t_E` | `A_min/A_max` | `P` | E1 event budget | `integration` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| B | 1.0 | 8 | 0.25 | 1.0 | 1.5 | 4.0 | 0.5 | 0.25 / 1.0 | 16 | 16 | `None` |
| X | 0.05 | 8 | 0.10 | 0.5 | 1.5 | 4.0 | 0.5 | 0.25 / 1.0 | 16 | 16 | `None` |
| D | 1.0 | 8 | 0.05 | 0.2 | 1.5 | 4.0 | 0.5 | 0.25 / 1.0 | 16 | 16 | `None` |

`P=16` is a bounded fixture choice within the accepted `1..64` provenance
limit. All three also freeze `m_emit_delay=1.0`, `m_rearm_delay=1.0`,
`delta_x_e=1.0`, and `event_budget=16`; M parameters are inactive because
no state may reach `theta_M`. `integration=None` disables ACP-0008. The
complete `E1Config` constructor names/defaults must match the source audit;
these are direct numeric settings, not a new neuron model.

## Fixed topology and transfer

Use two edge descriptors only; freeze every `Edge` field explicitly:

| Edge ID | Endpoints | Propagation delay | Routing cost | Model-B `w` | Divider `d` | Reference `r` | Legacy identity |
|---|---|---:|---:|---:|---:|---:|---|
| `edge-BX` | B to X | 0.1 | 1 | 1.0 | 1.0 | 0.0 | `true` |
| `edge-XD` | X to D | 0.1 | 1 | 1.0 | 1.0 | 0.0 | `true` |

For numeric excursion payload `a`, these parameters yield the existing
Model-B transform
`d*tanh(w*a) + (1-d)*r = tanh(a)` and retain its sign. The exact edge API
accepts `edge_weight` only in `[-2,2]`, `divider_strength` in `[0,1]`,
`reference` in `[-1,1]`, positive integer routing cost, and positive finite
delay. Use immutable configuration identity for each edge; there is no edge
generation in this static topology. All bounds and transforms must be
verified against the exact implementation before a future run.

## Analytically chosen primary sequence

The primary positive condition admits two `+1.1` external numeric root events
at B, at logical times `0.0` and `2.0`. No X or D sensory event is present.
This interval gives B time to complete its first ordinary return/rearm. Under
the proposed E1 parameters:

1. B's first input crosses `theta_E=1`, schedules `S_EMIT` at `0.5`, and
   produces a positive excursion amplitude
   `0.25 + 0.75*(1.1-1)/(4-1) = 0.275`.
2. With B's analytic return at `ln(4.4)`, the second input produces a second
   positive ordinary excursion; its amplitude follows the same E1 equation
   applied to B's actual state at `t=2`. The anticipated value is about
   `0.312`, to be checked by future tests against the source implementation.
3. Each B excursion arrives at X after the `0.1` edge delay. Transfer applies
   the fixed Model-B transform. The first X contribution is about `0.268`;
   the second is about `0.302`.
4. At X's `lambda=0.05`, the two contributions two time units apart produce
   approximately `0.268*exp(-0.1)+0.302 = 0.545`, above
   `theta_E=0.5`, but below `theta_M=4`. X therefore admits one ordinary
   excursion without independent X input.
5. X's output is routed to D with positive delay `0.1`. Its transferred
   magnitude is expected to exceed D's `theta_E=0.2`, so D's recorded
   reception/state transition supplies the downstream endpoint.

Approximate derived values are explanatory design calculations, not observed
execution outputs. The exact protocol artifact must serialize the full
parameters and stimuli before execution, and the implementation must verify
the event/state trace using the existing E1 implementation. If the actual E1
source calculation does not support the predicted margins, return to owner
disposition rather than tune after observing a run.

## Dispatch, ordering, reset and termination

- Logical time is local event time. No global neural update loop or timestep
  exists.
- Queue events carry finite timestamps and deterministic insertion sequences.
  Preserve established destination-local same-time ordering. The primary
  stimuli intentionally avoid a collision between an external arrival and a
  due internal event at the same destination/time; a separate future unit test
  must verify the existing equal-time E1 contract.
- At the start of every condition/replay, construct fresh neurons and an empty
  queue at timestamp zero. Do not retain state, pending internal events,
  provenance, credit, learning, or edges across conditions.
- Process due events through logical time `40.0`. P's slow-decay X rearm is
  expected to finish before this horizon; all conditions must end with an
  empty queue. A remaining pending event at the horizon is an incomplete-run
  failure, not success.
- Preserve each queue/event/edge failure explicitly. Stop before processing
  beyond a cap. Do not partially accept a fan-out, silently discard a branch,
  increase a limit, retry, or repair parameters after a failure.
- Trial/condition identity is orchestration metadata only. It is not an E1
  input, payload, threshold, route choice, or emission feature.

## Explicitly excluded

No R3 mutation, E2 behavior change, `ExcursionCharacterRuntime` change,
global-time stepping, hidden X/D stimulus in primary conditions, automatic
relay-on-receipt, learned topology, reward/error conversion, recurrence,
structural plasticity, R4 comparison, or Luna-72B activity is part of this
design.
