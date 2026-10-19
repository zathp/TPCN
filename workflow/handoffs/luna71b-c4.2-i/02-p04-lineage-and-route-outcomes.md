# Luna-71B-C4.2-I — P04 omission lineage and route outcomes

**Status:** Documentary design; not adopted or implemented.  
**Disposition:** P04 representation is **RESOLVED BY DESIGN**, conditionally; source capture and contract adoption remain pending.  
**Authority:** Design-only OD-I-1 through OD-I-4.

## Source path and label-isolation finding

The H-corrected `luna70_readout_learning.py` path is:

1. The `observation_deadline` event arrives after one input.
2. The source builds a deadline-absence `Observation` for the pending
   `next_after_<first symbol>` prediction.
3. `LocalPredictor.process_observation` / `observe` matches and settles that
   pending prediction; the resulting `PredictionError` retains prediction ID,
   target key, predicted/observed numeric values, and source/timestamps.
4. The source maps that pending error's scalar to A/B using
   `A if predicted_value >= 0.0 else B`, constructing `OmissionErrorSignal`.
5. `omission_resolve` records prediction identity, predicted target, deadline
   resolution time, and external-deadline outcome.
6. If omission routing is enabled, the source forms the event ID
   `{exposure_id}:omission-error:{prediction_id}` and sets the existing
   `Event.lineage_id` to the prediction ID.
7. `BoundedTopology.route` is called; exactly one returned route is expected.
8. `EventQueue.push` exposes admission or queue failure (through P02).
9. The destination sequence handler calls `sequence_neuron.receive_event`.
   The H `omission_delivery` capture occurs after that call returns.

The predicted target is sourced from the existing pending prediction carried
through `PredictionError`. It is not read from the true label, evaluation
record, data filename, a class branch, or a post-hoc classifier result. The
deadline remains external. This is not autonomous silence detection.

## Existing visibility versus representation gaps

| Evidence | Source visibility | Frozen PPC-11 limitation | v2 treatment |
|---|---|---|---|
| Pending prediction identity and target | Present in `PredictionError` | P04 record does not carry all lifecycle identity fields | Preserve exact source prediction ID and target key. |
| Omitted symbol | Derived from `predicted_value` by the source's explicit threshold equation | Frozen P04 expects a symbol without distinguishing source-observed from derived | Mark DERIVED, with rule ID and exact scalar input locator. Never copy a label. |
| Deadline trigger/time | Existing external deadline event and observation timestamp | Trigger not fully typed as an external deadline cause | Add `trigger_kind=EXTERNAL_OBSERVATION_DEADLINE` and source event ID/time. |
| Error construction | Existing `PredictionError`; H signal retains source values | Error and omission identities are not represented together | Link prediction ID, error payload fields, generated route event ID, and source lineage ID. |
| Route construction | `BoundedTopology.route` returns a sequence of routed events; caller checks cardinality | Frozen route/delivery records do not bind all attempts and outcomes | Record every attempt, route cardinality, routed events and explicit result. |
| Queue admission | Existing P02 queue observer | P04 cannot link every P02 admission/rejection to prediction/lineage | Add cross-record references using existing event/prediction IDs; do not create model-visible IDs. |
| Duplicate before route | Source duplicate guard detects the same prediction ID and raises | Frozen P04 has no typed duplicate result | Emit a passive route-attempt outcome `DUPLICATE_REJECTED` at the guard before the existing raise. |
| No route / multiple routes | Caller observes returned route count; it raises if count is not one | Cause details inside topology may not be returned | Record source-observed `route_count`; classify no/multiple from that count. Set detailed cause `UNAVAILABLE` unless source provides it. |
| Route exception / queue failure | Exception/queue outcome is observable at source boundary; H P02 records queue admission failure | P04 lacks correlated typed rejection event | Add passive outcome callback around the existing operation; preserve exception type/queue result only if observed. |
| Destination integration | `receive_event` call, then delivery capture on normal return | Frozen P04 has no explicit integration/rejection state | Capture `INTEGRATED` only after return. On exception or duplicate rejection, record exact outcome if available; otherwise mark cause unavailable and P11 failure. |
| Lineage | `Event.lineage_id` exists and is set to prediction ID | Frozen P04 records do not have it | Record existing lineage as source-observed; no new model ID. |

## Minimal passive hook proposal

The current H correction can report successful route plus delivery and emits
capture gaps for unrepresented lineage/route failures. A future implementation
may add observation-only callbacks at:

* the duplicate guard, before its existing exception;
* the return/exception boundary of `BoundedTopology.route`;
* each existing queue admission/rejection boundary; and
* the destination receive/integration return/exception boundary.

The callbacks must only serialize values already present at those boundaries.
They must not alter route selection, retry an event, create or rewrite event
IDs, affect event priority, or change destination handling. The source's
existing result count supports a derived `NO_ROUTE` / `MULTIPLE_ROUTES`
classification; an internal reason not exposed by the source remains
`UNAVAILABLE`, not a guessed cause. Hook exceptions must surface as capture
failures and must not be swallowed.

## Proposed P04 v2 record contract

Use linked records with the same trace envelope and exact source identities:

* `omission_resolution`: `prediction_id`, `target_key`, expected/omitted symbol
  evidence, source error values, external deadline event/time, and explicit
  trigger. Symbol is DERIVED by the approved equation, never a label.
* `omission_route_attempt`: source event ID and `lineage_id`, source and
  destination, event type, payload identity, `route_construction_outcome`
  (`ROUTE_RETURNED`, `ROUTE_EXCEPTION`, `DUPLICATE_REJECTED`, or
  `UNAVAILABLE`), and observed route count.
* `omission_queue_admission`: reference to the exact P02 record by
  `record_index`, containing no duplicated or reclassified queue outcome.
  P02 alone reports `ADMITTED`, `REJECTED_CAPACITY`, `REJECTED_INVALID`, or
  another queue result.
* `omission_route_result`: one record per returned routed event, retaining
  event ID, lineage, hop, source/destination, timestamp, payload, queue
  sequence and priority where present.
* `omission_delivery`: destination event/lineage identity and
  `delivery_outcome` (`INTEGRATED`, `REJECTED_DUPLICATE`,
  `REJECTED_VALIDATION`, `INTEGRATION_EXCEPTION`, `NOT_ATTEMPTED`, or
  `UNAVAILABLE`). Record integration timestamp only after successful return.
* `route_cause_evidence`: a tagged `SOURCE_OBSERVED`, `DERIVED`, or
  `UNAVAILABLE` cause; never turn a generic exception or missing code into an
  inferred reason.

Diagnostic record references use existing event/prediction IDs or trace
`record_index` locators. If a local attempt ordinal is needed for ordering, it
is capture-only, side-specific metadata and must never enter model state,
event payload, routing, or learning.

## Conclusion

The representation can separate prediction lineage, the external deadline,
error creation, route admission/rejection, delivery, destination integration,
and duplicate outcomes. It preserves the label-free source and existing
external-deadline semantics. **P04 capture remains INCOMPLETE** until
contract adoption and any required passive hooks are separately authorized,
implemented, and independently tested. This design makes no claim of
autonomous silence detection or completed neural computation.
