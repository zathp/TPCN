# Luna-71B-C4.2-I — P11 failure attribution and terminal ordering

**Status:** Documentary design; not adopted or implemented.  
**Disposition:** P11 representation is **RESOLVED BY DESIGN**, conditionally; source/driver failure observation is incomplete.  
**Authority:** Design-only OD-I-1 through OD-I-4.

## Source-defined ordering

The inspected `EventQueue` stores `(timestamp, assigned_sequence, event)`;
`_snapshot` orders by those source fields. `pop_ready` asks
`_tie_break_cause` before dequeue. For same-time events, the source suppresses
an internal event when a pending external event targets the same destination;
otherwise it returns the timestamp/assigned-sequence rule. H terminal pending
rows preserve `[timestamp, queue_sequence]`; dequeue evidence preserves the
source tie-break cause. The I extension must retain these keys and the
enqueue/process order independently rather than recreating them from outputs.

`execute_bounded` wraps the event loop in `except BaseException`, calls
`observer.execution_failed(queue)`, then re-raises. That callback receives
neither the exception nor the active operation/event. H capture therefore
records a P11 gap for handler/runtime failure instead of inventing a cause.
Queue admission separately observes `BufferError`/`ValueError` type names and
the failed event/queue state; this does not identify every failure cause.

## Failure-kind taxonomy

The proposed v2 closed enum is:

| Kind | Meaning | Required evidence |
|---|---|---|
| `SCHEDULER_FAILURE` | Failure in queue peek, dequeue, priority selection, or scheduler operation | Exact operation and source location, source event/queue state, observed exception type if present. |
| `QUEUE_ADMISSION_FAILURE` | Queue push rejected an event | Attempt anchor, pre-failure occupancy/capacity, actual rejection outcome and source-observed reason. |
| `HANDLER_EXCEPTION` | Event handler failed while processing an identified event | Active event identity, handler operation/location, observed exception type, last completed operation. |
| `RUNTIME_TERMINATION` | Runtime ended without normal queue completion (excluding explicit paired stop) | Source-defined termination outcome and timestamp; do not infer from two traces ending. |
| `TRACE_CAPTURE_FAILURE` | Capture/serialization/write failure | External supervisor or independently written sidecar evidence; trace writer cannot be trusted to record its own failure. |
| `DRIVER_FAILURE` | Pair driver/supervisor failure outside model execution | Driver-side log identity, operation, and stop status; not neural source evidence. |
| `UNKNOWN_UNOBSERVABLE` | Failure occurred but operation/cause is not observable | Explicit unavailable cause and source point; P11 incomplete. |

An exception type or source code location is not automatically a semantic
cause. Cause fields are `SOURCE_OBSERVED`, `DERIVED` from an exact source
branch, or `UNAVAILABLE`. Raw exception messages are not required; preserve
type and stable source reason code where available. Do not assert which
component failed from the fact that the loop stopped.

## Proposed failure record and minimal hook

`failure_evidence` is a versioned diagnostic record with:

* `failure_kind` and source/driver domain;
* side, run/exposure envelope and monotonic `record_index`;
* active event ID/lineage ID if one exists;
* `operation` and `source_location` evidence state;
* source timestamp and last completed P02 operation;
* exception type/reason code as source-observed, or explicit `UNAVAILABLE`;
* queue occupancy/capacity and pending `(event_id, timestamp, sequence)`
  snapshot at the actual boundary;
* `failure_identity` derived only from `(side, run_id, record_index)` as a
  trace locator, not a new model-visible event/neuron identifier.

The minimal handler hook is an observer callback at the existing
`execute_bounded` exception boundary that receives the active operation,
event, and caught exception classification before the unchanged re-raise.
Queue admission capture may report the exact source branch (capacity versus
invalid event) only when the branch condition is observed. The hook must not
swallow the exception, continue processing, mutate queue state, or alter
termination. If the trace writer fails, an independent supervisor sidecar is
required; a missing trace record cannot be converted into a model failure.

Normal completion, event-budget exhaustion, pair-gate stop, and failure must
have distinct terminal statuses. A paired stop imposed by the supervisor is
not a runtime failure.

## Failure alignment and comparison termination

1. Compare P01-P11 ordered evidence through the last mutually comparable
   source operation. For queue attempts use the frozen exact P02 anchor
   `(exposure_id,event_id,source,destination,event_type)`, comparing timestamp,
   payload, sequence assignment/status separately.
2. On the first P11 failure, stop both sides before either processes another
   event. Do not advance a counterpart to manufacture the failing event.
3. Preserve each side's failure record, actual terminal boundary, last
   completed operation, and pending queue snapshot. The comparison summary
   stores both failure locators and the last common record locator.
4. If the counterpart's already-captured trace proves it admitted the exact
   alignment anchor and one side then fails while the other continues, classify
   that branch as a one-sided occurrence / `CONTRADICTED`, not a matched
   failure.
5. If the counterpart had not reached or cannot prove that exact admission,
   classify `EVIDENCE_UNAVAILABLE` and P11 `INCOMPLETE`; terminal queue state
   cannot establish hypothetical future behavior.
6. `BOTH_TERMINAL` is not a parity result. Two stopped traces are not matched
   merely because both ended. Matched failure requires both observed failures
   to have exactly equal source operation, source cause/code, aligned event,
   and terminal semantics under an owner-approved v2 comparator. Different
   failure identity or one failure plus a normal/budget/pair stop is
   contradicted or incomplete according to the available alignment evidence.

Failure record identities are diagnostic evidence locators. No model-visible
IDs, neural state, scheduler order, or learning semantics are added.

## Conclusion

The schema can distinguish scheduler, queue, handler, runtime, capture, and
driver failures, while retaining unknown causes as unknown. The present source
observer does not identify the handler operation/exception and remains
**INCOMPLETE** for that path. The design does not create a terminal key, cause,
or success state absent from source evidence. Adoption and any hook require a
separate owner decision.
