# Luna-72A-M2D Event Identity and Provenance Contract

## Status and provenance rule

This is a proposed downstream-only observer contract. Current TPCN event and
E1 identity fields are reused, but M2D's transfer/arrival/state-transition
records and contributor-root map do not currently exist. The observer must not
change E1 computation, event payloads, lineage, or queue ordering.

**Immediate parent is not sole attribution.** Every state transition records
the immediate event that triggered it. An emission also carries the bounded
ordered set of all E1 input event IDs that contributed to its active episode.
At a convergent or multi-arrival neuron, there may be several contributors;
the trigger is one member, not a claim that it alone caused the output.

## Existing fields

`Event` currently supplies timestamp, source, destination, event type, payload,
queue-assigned sequence, optional `event_id`, and optional `lineage_id`.
`ExcursionEmission` supplies a distinct neuron-local emission ID/sequence,
source, timestamp, signed payload, episode and lineage. E1's
`ProvenanceEntry` records input event ID, timestamp, signed contribution,
episode ID and lineage ID. Topology preserves an emission's event and lineage
identity on routed copies while each copy gets a new queue sequence.

These fields support event identity and E1 contributor event IDs, but do not
alone identify the edge transfer instance, queue arrival instance, root set,
dispatch order, or full multi-contributor ancestry. E1's lineage is an
episode/group key, not a complete parent graph.

## Proposed records

Every observer `record_ref` is scoped by immutable `protocol_id`,
`condition_id`, and `queue_epoch`. Raw E1 event IDs are retained exactly;
because standalone neurons may generate identical local IDs in different
arms, refer to an emission as `(condition_scope, raw_event_id)` rather than
claiming the raw ID is globally or cross-condition unique. The execution
attempt number is stored outside the canonical trace. An original condition
and its replay use the same protocol/condition identity scope, queue epoch,
neuron IDs and ordinals so their semantic trace can compare byte-for-byte.

Matched arms share `stimulus_id` for exogenous slots with the same causal
role (for example, the two B-root slots in P/C/O+/O-); condition-scoped root
record references remain distinct. Raw input IDs may be reused across arms
but are never compared without their condition scope. This preserves matching
without conflating separate execution records.

| Record | Required fields |
|---|---|
| **Root** | `root_id`, input `event_id`, stable matched `stimulus_id`, source/destination, event type, logical timestamp, signed payload, protocol stimulus ordinal. `stimulus_id` identifies the corresponding exogenous slot across matched arms; event/root IDs are condition-scoped. Root identity does not encode a label or outcome. |
| **Arrival** | `arrival_ref=(protocol_id, condition_id, queue_epoch, queue_sequence)`, raw event/lineage IDs, source/destination/type/payload, timestamp, dispatch ordinal, and optional incoming `transfer_id`. Event ID is not rewritten across a routed transfer; arrival reference distinguishes each delivery. |
| **State transition** | transition ordinal, neuron ID, event/local timestamp, immediate triggering `arrival_ref` or internal `arrival_ref`, pre-event observed `x`, source-equation-derived post-decay `x`, signed contribution if external, post-update observed `x`, mode before/after, episode/lineage ID, and provenance-truncation state. |
| **Emission** | `emission_ref=(protocol_id, condition_id, raw_E1_event_id)` plus the unchanged E1 raw event ID and neuron-local sequence, source, timestamp, payload, episode/lineage, immediate parent reference (normally the valid internal `S_EMIT` dispatch), ordered contributor arrival references, ordered contributor event IDs, bounded root-ID union, and truncation/omitted-count fields. |
| **Transfer** | Condition-scoped `transfer_id`, source `emission_ref`, static `edge_id`, source/destination, send time, configured delay, arrival time, transfer parameters/config digest, pre/post-transfer payload, fan-out ordinal, and generated arrival reference. Edge generation is **N/A**: the proposed fixture has immutable static edges and no generation API. |
| **Blocked-route decision** | Bounded `decision_ref`, source emission reference, static `edge_id` descriptor, source/destination, send time, excluded destination/reason, and untransferred source payload. It has no `transfer_id`, no transformed payload, no queue sequence and no `arrival_ref`, because no transfer or arrival occurred. |
| **Terminal state** | per-neuron final local time/state/mode, pending internal event, out-of-scope status, provenance count/truncation, final queue count, processed/created counts, and failure/complete status. |

`edge_id` is a stable key over the canonical directed endpoints and frozen
edge configuration. A separate `transfer_id` identifies each use of that
static route. Do not add an imaginary mutable edge generation.

## Root and contributor relationships

- A root event gets its own event ID and root ID. Its root set is `{root_id}`.
- A B emission's E1 provenance contributor list contains B's admitted input
  arrival(s); the observer maps those to root IDs.
- A B-X routed arrival preserves the B emission's `event_id` and lineage, but
  receives a distinct transfer record and queue arrival reference.
- X's E1 provenance contributor IDs identify the B-X input event(s) that
  updated X. For X's new emission, list every contributor retained for the
  active episode and map each through the observer to root event IDs.
- `immediate_parent_ref` for an X state transition names the arrival being
  processed. `immediate_parent_ref` for the generated excursion names its
  scheduled internal `S_EMIT` event. `contributor_arrival_refs` separately
  identify the upstream event(s) that contributed to X's threshold episode.
- D's arrival references the X emission and X-D transfer. The event lineage
  is preserved for route continuity; a D state transition is not assigned
  sole causal credit from lineage alone.
- C's excluded B-X route is represented only by a blocked-route decision
  record, not by a fabricated transfer or arrival. `BoundedTopology.route`
  filters excluded destinations before creating routed events, and its route
  observer receives only actual routes.
- If E1 reports provenance truncation or the observer cannot resolve any
  contributor/root/transfer link, propagate `ancestry_complete=false` to
  descendants. Such a run cannot satisfy complete causal attribution.

Observer records are explanatory evidence only. They never participate in
weight/threshold calculations, route choice, or condition selection.

## Ordering and replay

Record all of:

1. event logical timestamp;
2. queue epoch and insertion sequence;
3. deterministic dispatch ordinal (actual processing order);
4. E1 local state clock before/after the event;
5. topology fan-out ordinal and route configuration identity.

The current public E1 receive method does not expose its internal post-decay
intermediate state. Capture pre/post `x` directly and label the intermediate
decayed value **source-equation-derived** from the prior observed state,
elapsed local time and frozen E1 decay equation; do not present it as a direct
API observation or add a production hook.

Use the queue's established timestamp and same-destination external-before-
internal ordering. Dispatch ordinal is the canonical processing order because
same-time dispatch may prioritize event kind/destination beyond insertion
sequence. Each condition starts a fresh queue epoch. Frozen protocol inputs
have stable ordinals and IDs; observer insertion must not change order or
create neural events.

Replay compares canonical serialized event, state, emission, transfer,
arrival, contributor and terminal records byte-for-byte on the same exact
source/runtime. Wall time and host memory samples are recorded but are not
required to match bitwise. Any numeric tolerance must be predeclared and
limited to numeric state fields; identity/order mismatches always fail.

## Bounded observer capacities

The proposed resource contract caps queue-event admissions/creations at 32
per condition, so keep at most 32 arrival/dispatch records, 32 transition
records, 8 transfer records, 8 blocked-route decisions, 8 emission records,
and 128 contributor/root references per condition. A condition exceeding any
record capacity fails closed. IDs and references are stored in bounded
tables; there is no unbounded append-only sidecar. The condition record cap
is part of the protocol and not a production API.

## Source anchors

- `tpcn/event_runtime.py`: `Event` fields/validation lines 59-90; queue
  admission, sequence and ordering lines 116-233.
- `tpcn/topology.py`: immutable `Edge` lines 52-77; static endpoint lookup
  and route/fan-out/transfer lines 173-251.
- `tpcn/excursion_neuron.py`: `ProvenanceEntry`, `PendingInternalEvent`,
  `ExcursionEmission` lines 224-290; bounded neuron storage lines 321-336;
  provenance recording/truncation lines 737-763.
- `tpcn/experiment_excursion_runtime.py`: `RouteContext` and bounded roots
  are E2 runtime sidecars (lines 47-52, 367-425), not an existing standalone
  E1 observer.
