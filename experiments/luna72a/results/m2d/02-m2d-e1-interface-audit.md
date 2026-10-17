# Luna-72A-M2D E1 Interface Audit

## Audit scope and status

Static source audit at baseline `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`.
No code/tests/workloads were run. This records current interfaces separately
from the proposed M2D composition; it is not an implementation.

## Current standalone E1 interface

`SingleExcursionNeuron` is the E1 implementation. Its constructor is:

```text
SingleExcursionNeuron(
    neuron_id: str,
    *,
    config: E1Config | None = None,
    initial_state: Real = 0.0,
    initial_timestamp: Real = 0.0,
) -> None
```

Relevant methods:

| Current method | Signature / behavior |
|---|---|
| `receive_event` | `receive_event(event: Event, queue: EventQueue[Event] \| None = None) -> ExcursionEmission \| None`. The destination must match `neuron_id`; internal events are separately validated. For an external numeric event, E1 advances its local clock, applies its configured event-time decay, adds/clips the signed contribution, updates provenance and the ordinary mode state machine. External admission normally returns `None`; the later valid internal `S_EMIT` returns an `ExcursionEmission`. |
| `receive_contribution` | `receive_contribution(timestamp: Real, contribution: Real, *, source: str = "external", event_id: str \| int \| None = None, queue: EventQueue[Event] \| None = None) -> ExcursionEmission \| None`. This processes immediately; the optional queue is only for its internal scheduling, not for enqueueing this external input. The proposed harness should queue `Event`s instead to preserve sequence ordering and event identity. |
| `process_pending` | `process_pending(*, through: Real \| None = None, queue: EventQueue[Event] \| None = None) -> ExcursionEmission \| None`. For the queue-driven composition, do not invoke this while the neuron's scheduled internal event is still in the queue; doing so can leave a later stale queued event. |
| `reset` | `reset(*, timestamp: Real = 0.0) -> None`. Reset clears character-local state/provenance but retains event, episode and lineage identity counters. M2D proposes fresh neuron objects per condition rather than cross-condition reset/reuse. |

Observable state includes `state`, `last_update_timestamp`, `provenance`,
`pending_event`, `last_emission`, `integration_state`,
`integration_trace`, mode, pending internal event and bounded emissions.
Source: `tpcn/excursion_neuron.py`, `SingleExcursionNeuron` lines 292-395,
`receive_event` lines 396-529, `process_pending` lines 507-581, and reset/
state accessors around lines 321-395.

## E1 configuration and output records

`E1Config` defaults include `decay_rate=1.0`, `x_max=8.0`,
`theta_r=0.25`, `theta_e=1.0`, `theta_hold=1.5`, `theta_m=4.0`,
`emission_delay=0.5`, `a_min=0.25`, `a_max=1.0`,
`provenance_capacity=16`, `event_budget=4096`, and `integration=None`.
It validates finite non-boolean real parameters, threshold ordering
`theta_r < theta_e <= theta_hold < theta_m <= x_max`, positive decay/delay,
provenance capacity `1..64`, and positive integer event budget.
`integration` is optional ACP-0008 slow-state configuration; M2D keeps it
disabled (`None`). Source: `tpcn/excursion_neuron.py`, E1Config lines 61-191.

`ExcursionEmission` includes `event_id`, neuron-local `sequence`, `source`,
`timestamp`, numeric `payload`, `lineage_id`, `episode_id`, and excursion
event type. It exposes `as_event(destination)` and `enqueue(queue, destination,
delay=0.0)`. Emission sequence and queue insertion sequence are distinct;
`EventQueue` assigns the latter. Source: `excursion_neuron.py` lines 252-290.

With a supplied queue, E1 schedules an `INTERNAL` event to itself and stores
the assigned queue sequence in the pending record. Its handler validates
pending episode/generation/kind/time/sequence before an internal event can
emit. A stale internal event returns `None` but still consumes E1's event
budget. M2D must pass the same shared queue to `receive_event`; it must not
invent internal events or bypass queue-owned work. Source:
`excursion_neuron.py` lines 507-581 and 603-730.

## Current event queue and topology interfaces

- `EventQueue.push(event)` assigns a sequence and may raise
  `QueueCapacityError` on a full queue.
- `push_propagated(emission_time, source, destination, event_type, payload,
  delay, *, event_id=None, lineage_id=None) -> Event` enqueues a delayed copy
  by calling `self.push`. The queue API permits zero delay, so M2D must rely
  on positive-delay `BoundedTopology` edges rather than the broader queue
  allowance.
- `peek()` observes the next eligible event; `pop_ready(through)` pops the
  next eligible event only if its timestamp is at or before `through`.
  `execute_bounded` has an event budget but no logical-horizon argument, so
  the proposed M2D dispatcher should use `peek`/`pop_ready(40.0)` to enforce
  its horizon rather than claim that `execute_bounded` enforces one.
- Equal-timestamp queue dispatch selects external before internal events for
  the same destination; unrelated destinations preserve sequence ordering.
- `execute_bounded(queue, handler, *, event_budget)` dispatches events and
  returns `BoundedExecutionResult` with completion, processed count, pending
  count, last timestamp and peak occupancy.

Source: `tpcn/event_runtime.py` lines 59-90, 116-233, 234-280.

`Edge` is a directed static record with positive `propagation_delay`,
`routing_cost`, `edge_weight`, `divider_strength`, `reference`, and
`legacy_identity`; it has no generation field. `BoundedTopology.route(
event, queue, *, observer=None, exclude_destinations=())` fans out from
`event.source`, applies Model-B transfer to numeric `signal`/`excursion`
payloads, and preserves `event_id`/`lineage_id` across routed copies. It
preflights the full fan-out against routing and queue capacity. A route
carrier may be `emission.as_event(emission.source)`; topology uses its source
to select outgoing edges. Source: `tpcn/topology.py` lines 52-77 and 204-251.

## Failure behavior

- Wrong E1 destination: `ValueError`.
- Non-real or non-finite external contribution: `TypeError` /
  `ValueError`.
- Earlier-than-local-clock arrival: `LateEventError`.
- Reaching the E1 `theta_m` boundary records an out-of-scope report; later
  external input raises `E1OutOfScopeBoundary`. The M2D harness must stop on
  the first boundary report and never switch to E2.
- Neuron event/generation limit: `E1EventBudgetExceeded`.
- Queue capacity failure: `QueueCapacityError`.
- `execute_bounded` pops before invoking its handler and propagates handler
  exceptions; it does not roll back queue or neuron mutations. E1 can mutate
  state before an internal-scheduling queue push fails. These are terminal
  failed conditions: preserve bounded partial evidence, do not continue,
  retry or publish success-shaped output.

Source: `excursion_neuron.py` lines 396-482, 603-730, 764-775;
`event_runtime.py` lines 129-148 and 248-280.

## Proposed M2D dispatch contract (not an existing API)

1. Construct exactly one `SingleExcursionNeuron` per topology node and one
   shared finite `EventQueue`.
2. Put exogenous `Event` records into that queue. For each popped event, look
   up `event.destination`; unknown nodes are a terminal failure.
3. Call `neuron.receive_event(event, queue)` using the shared queue.
4. Record a bounded state/identity observation after the call.
5. If and only if E1 returns an `ExcursionEmission`, build an event carrier
   via `emission.as_event(emission.source)` and call
   `BoundedTopology.route(carrier, queue)` to apply the fixed edge delay and
   Model-B transfer. Do not inline-update X or D and do not use direct
   `emission.enqueue` in place of topology routing.
6. Use an isolated `EventQueue` subclass that prechecks the cumulative
   admission cap in `push` and then delegates to `super().push`; current
   `push_propagated` calls `self.push`, so root, E1-internal and topology
   admissions all pass through the same counter without changing ordering.
   Dispatch with `peek` and `pop_ready(through=40.0)` under the processed-event
   cap. At successful completion require an empty queue and no valid pending
   E1 event. A counting push that delegates exactly once is a proposed
   experimental helper, not an API that exists today.

This adapter/observer is new experimental code proposed only for a later,
separately authorized implementation. It makes no change to E1, E2, R3,
`EventQueue`, or `BoundedTopology`.
