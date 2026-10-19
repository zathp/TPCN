# Luna-71B-C4.2-I — Proposed versioned PPC-11 trace schema

**Schema proposal:** `ppc11-paired-trace-2`  
**Status:** Design only; not adopted, implemented, or authorized for execution.  
**Baseline preserved:** `ppc11-paired-trace-1` and the C4.1 PPC-11 contract remain unchanged.

## 1. Version boundary and compatibility

Version 1 remains byte-for-byte and semantically frozen. A v1 parser must
continue to enforce the existing required fields, exact P01-P11 comparisons,
branch states, lossless number rules, stop conditions, and empty projection
list. No v1 record is silently upgraded to v2.

V2 uses literal `schema_version="ppc11-paired-trace-2"` in every record and
the same UTF-8 JSONL transport. It preserves the v1 envelope fields and
existing P01-P11 record families; additions below expand observation
capacity. Every record is schema-closed: unknown keys, mixed versions,
duplicate identities, missing conditional evidence, or unsupported number
types fail closed.

V1 continues to require its existing non-empty `expected_symbol` string on
`prediction_create`. V2 preserves that record and field unchanged for
symbol-bearing predictions, and adds `expected_symbol_evidence` alongside it
to identify whether the string was source-observed or derived. V2 adds a
separate `prediction_create_non_symbol` record for a source prediction kind
that has no expected symbol; it carries an explicit `NOT_APPLICABLE` state
instead of omitting or changing the v1 field. This is append-only at the
record/schema boundary, but accepting the new record in place of a v1
symbol-bearing creation changes the P03 applicability rule for non-symbol
predictions. That substantive acceptance change requires express owner
approval.

## 2. Envelope

Preserve all v1 envelope fields and meanings:

| Field | V2 requirement |
|---|---|
| `schema_version` | Literal `ppc11-paired-trace-2`. |
| `side` | `original` or `instrumented`. |
| `run_id` | Stable unique execution identifier. |
| `source_revision` | Git commit plus exact source-manifest digest; also bind uncommitted bytes independently. |
| `runtime_manifest_sha256` | Exact runtime/dependency manifest. |
| `seed`, `arm`, `split`, `example_id`, `exposure_id` | Same frozen types and meanings as v1. Exposure maps to exactly one fixture tuple and is identical across sides. |
| `record_index` | Nonnegative contiguous integer, source-observed order. |
| `comparison_id` | `P01`–`P11` or explicit diagnostic scope allowed by schema. |
| `record_type` | Closed v2 event name. |
| `payload` | Typed closed object; unknown keys fail. |

No new model-visible event identity is permitted for diagnostics. A diagnostic
reference can use `(side, run_id, record_index)`; existing source event,
prediction, feedback, lineage, and parameter IDs remain unchanged.

## 3. Evidence-value algebra

Conditionally applicable fields use a tagged object, never ambiguous `null`:

```json
{"state":"SOURCE_OBSERVED","value":"A","source":{"module":"...","symbol":"..."}}
{"state":"DERIVED","value":"A","rule_id":"next-symbol-sign-v1","inputs":[{"record_index":17}]}
{"state":"NOT_APPLICABLE","basis":"prediction_kind=COMPLETION"}
{"state":"UNAVAILABLE","reason_code":"SOURCE_FIELD_ABSENT","source_point":"..."}
{"state":"COMPLETE_UNEXERCISED","basis":"complete exposure boundary"}
{"state":"SOURCE_PATH_ABSENT","source_point":"..."}
```

The `value` uses the source type and the number representation below. The
allowed state union depends on field. `COMPLETE_UNEXERCISED` describes an
existing but unexercised branch; `SOURCE_PATH_ABSENT` means the model has no
such transition. Neither is a successful terminal outcome.

## 4. Lossless numerical and identity rules

Retain the v1 exact typed-value policy: no model-visible JSON decimal numbers.
Encode `f64` as exact 16-digit lowercase big-endian IEEE-754 bits,
`f32` as exact 8 digits; preserve signed zero and NaN payload. Fixed-width
integers carry exact type and bits; arbitrary-precision integers use
canonical signed decimal text. Timestamps retain source type/bits and are not
rounded. Unknown source numeric types block comparison.

Each raw stream, source/runtime manifest, fixture, initial-parameter
manifest, and comparison output has its own full SHA-256 and byte size.
Record ordering is the order observed by each side; never sort records to
repair ordering differences.

## 5. P03 records

### `prediction_create`

Required fields:

| Field | Type / meaning |
|---|---|
| `prediction_id`, `predictor_id`, `target_key` | Exact source identities and target. |
| `prediction_kind` | Literal `SYMBOL` with source call-site locator. |
| `predicted_value` | Exact typed source scalar, preserved even when a symbol is derived. |
| `expected_symbol` | Required non-empty string, exactly as in v1. |
| `expected_symbol_evidence` | `SOURCE_OBSERVED` or `DERIVED` evidence object whose value must exactly equal `expected_symbol`; `UNAVAILABLE` invalidates P03 and cannot produce a valid creation record. |
| `created_at` | Exact source timestamp. |
| `due_time`, `expires_at` | Evidence-value unions distinguishing source time, not applicable, and unavailable. |
| `target_semantics` | Source-observed target kind/key, not inferred from labels. |

The proposed `next-symbol-sign-v1` derivation records the exact source scalar
and applies `A if predicted_value >= 0.0 else B`; rule source identity is
versioned. It is a derivation, not a neural symbol field. The completion
prediction is represented by the new `prediction_create_non_symbol` record:

| Field | Type / meaning |
|---|---|
| `prediction_id`, `predictor_id`, `target_key` | Non-empty exact source strings. |
| `prediction_kind` | Closed enum `COMPLETION` or `OTHER`, with exact source call-site locator. |
| `predicted_value` | Exact typed source scalar; for the observed completion source this is the class index represented as source float. |
| `expected_symbol_state` | Literal `NOT_APPLICABLE` for completion kind; `UNAVAILABLE` for another kind whose applicability cannot be determined. |
| `created_at` | Exact source timestamp. |
| `due_time`, `expires_at` | Evidence-value objects; never ambiguous null. |
| `target_semantics` | Exact source target key/kind. |

The added non-symbol record is not a conversion of a v1 record. Its use to
satisfy P03 for a completion prediction is an explicit acceptance change and
requires owner approval.

### Lifecycle records

* `prediction_match`: prediction ID, observation event ID and lineage, target
  key, observed value/symbol evidence, exact timestamp, and source match
  outcome.
* `prediction_expire`: prediction ID, source expiry and current timestamp,
  outcome.
* `prediction_settle`: prediction ID, source disposition (`MATCHED` or
  `EXPIRED` as observed), timestamp, and triggering record reference.
* `lifecycle_coverage`: prediction ID, coverage state
  `COMPLETE_UNEXERCISED`, `UNAVAILABLE`, or `SOURCE_PATH_ABSENT`; it is
  diagnostic coverage, not a synthetic lifecycle transition.

`prediction_create_non_symbol` is the additional creation family for a
completion/other non-symbol source prediction. It never contains a fabricated
expected-symbol string.

An expected symbol `NOT_APPLICABLE` does not imply settlement. If completion
settlement is absent in source, emit `SOURCE_PATH_ABSENT` and retain P03
incompleteness.

## 6. P04 records

Add or extend:

* `omission_resolution`: originating prediction ID, target key, omitted
  symbol evidence, deadline trigger/event/time, `PredictionError` values and
  source error identity.
* `omission_route_attempt`: event ID, existing lineage ID, origin prediction
  ID, source/destination/event type, payload identity, route count, and
  `route_construction_outcome` `ROUTE_RETURNED`, `ROUTE_EXCEPTION`,
  `DUPLICATE_REJECTED`, or `UNAVAILABLE`.
* `omission_queue_admission`: a required reference to the exact P02
  `record_index` for each routed event's queue attempt. The P02 record alone
  carries `ADMITTED`, `REJECTED_CAPACITY`, `REJECTED_INVALID`,
  `OTHER_FAILURE`, or `UNAVAILABLE`; P04 must not relabel route production as
  queue admission.
* `omission_route_result`: each routed event/hop with existing IDs, exact
  route, timestamp, sequence/priority, and payload.
* `omission_delivery`: destination event/lineage IDs, integration state,
  `delivery_outcome` `INTEGRATED`, `REJECTED_DUPLICATE`,
  `REJECTED_VALIDATION`, `INTEGRATION_EXCEPTION`, `NOT_ATTEMPTED`, or
  `UNAVAILABLE`; timestamp only after integration.
* `route_cause_evidence`: `SOURCE_OBSERVED`, `DERIVED`, or `UNAVAILABLE`
  cause. No unobserved reason is inferred.

Existing event/prediction/lineage identities are reused. If a source does not
expose a cause, the cause is explicit UNAVAILABLE. Route count may support
NO_ROUTE/MULTIPLE_ROUTES only where the source return value is observed; those
describe route construction, not queue admission. A source exception during
route construction is not a queue rejection unless the P02 queue observer
also records that attempt.

Required common field types:

| Field | Type |
|---|---|
| `prediction_id`, `event_id`, `lineage_id`, `source`, `destination`, `event_type` | Non-empty source strings, except an existing non-string source ID retains its tagged source type. |
| `target_key`, `trigger_kind`, `outcome` | Closed-enum or non-empty string as defined per source value; no free-text inference. |
| `omitted_symbol_evidence` | Tagged evidence object; DERIVED value is a symbol string with rule ID and exact input locator. |
| `error_values` | Closed object of typed exact `predicted_value`, `observed_value`, and `error` source numbers. |
| `trigger_event`, `source_event`, `destination_event` | Trace references to the exact source P01/P02 record indices, or explicit UNAVAILABLE state. |
| `route_construction_outcome` | Closed enum `ROUTE_RETURNED`, `ROUTE_EXCEPTION`, `DUPLICATE_REJECTED`, `UNAVAILABLE`. |
| `route_count` | Nonnegative typed integer only if returned by source; otherwise UNAVAILABLE. |
| `queue_admission_record_index` | Nonnegative typed record index referencing the matching P02 attempt; UNAVAILABLE only if the P02 capture itself failed. |
| `delivery_outcome` | Closed enum `INTEGRATED`, `REJECTED_DUPLICATE`, `REJECTED_VALIDATION`, `INTEGRATION_EXCEPTION`, `NOT_ATTEMPTED`, `UNAVAILABLE`. |
| `route` | Ordered array of non-empty source node strings. |
| `timestamp` | Exact typed source timestamp, not JSON decimal. |
| `queue_sequence` | Nonnegative typed source integer or explicit NOT_APPLICABLE/UNAVAILABLE state. |
| `payload_identity` | Exact typed payload or hash reference to the separately retained typed payload bytes. |
| `cause_evidence` | Tagged source-observed/derived/unavailable object with source point/rule locator. |

An `omission_delivery` record with outcome `INTEGRATED` must include the
destination receive operation reference and source timestamp captured after
normal return. A rejection/failure record must not include a fabricated
integration timestamp.

## 7. P11 records

Keep existing queue/admission and terminal evidence; append:

* `admission_decision`: exact P02 alignment anchor, operation, exact
  pre/post occupancy and capacity, sequence-assignment state, outcome
  `ADMITTED`, `REJECTED_CAPACITY`, `REJECTED_INVALID`, `OTHER_FAILURE`, or
  `UNAVAILABLE`; reason state and source location.
* `failure_evidence`: taxonomy
  `SCHEDULER_FAILURE`, `QUEUE_ADMISSION_FAILURE`, `HANDLER_EXCEPTION`,
  `RUNTIME_TERMINATION`, `TRACE_CAPTURE_FAILURE`, `DRIVER_FAILURE`, or
  `UNKNOWN_UNOBSERVABLE`; active event/lineage when present; operation;
  source location; exception type/code; timestamp; last completed P02
  operation; queue snapshot; explicit availability states.
* `execution_terminal`: actual event-loop boundary, normal/budget/pair-stop/
  failure status, processed count, last event/time, queue occupancy/capacity,
  ordered pending event IDs and source priority keys.

`failure_identity` is a diagnostic locator derived from the record envelope,
not a new model ID. A capture-writer failure must be reported by an
independent supervisor/sidecar; the failing writer cannot attest to its own
successful record.

Required common field types:

| Field | Type |
|---|---|
| P02 alignment `anchor` | Object of exactly five non-empty strings: `exposure_id`, `event_id`, `source`, `destination`, `event_type`. |
| `admission_outcome` | Closed enum `ADMITTED`, `REJECTED_CAPACITY`, `REJECTED_INVALID`, `OTHER_FAILURE`, `UNAVAILABLE`. |
| `occupancy_before`, `occupancy_after`, `capacity`, `processed_count` | Nonnegative typed integers; capacity positive when source provides it. |
| `sequence_assignment` | Tagged state with exact queue sequence when assigned; otherwise explicit `NOT_APPLICABLE` or `UNAVAILABLE`. |
| `failure_kind`, terminal `status` | Closed enums as defined above; runtime termination and pair stop are distinct. |
| `operation` | Evidence object containing operation enum/string and source location; UNKNOWN/UNAVAILABLE must be explicit. |
| `source_location` | Object `{module, qualified_function, source_line}` with exact values when observed; otherwise explicit UNAVAILABLE. A location is diagnostic, not an event identity. |
| `exception_type`, `reason_code` | Non-empty source-qualified type/code string when observed; otherwise UNAVAILABLE. Do not put guessed cause in this field. |
| `failed_event_id`, `lineage_id` | Existing source IDs or explicit NOT_APPLICABLE/UNAVAILABLE evidence objects. |
| `failure_identity`, `last_common_record` | Diagnostic locator objects based on trace envelopes; never model-visible IDs. |
| `pending` | Ordered array of exact source event IDs, timestamps and queue sequences/priority keys. |
| `terminal_timestamp` | Exact typed source time or explicit UNAVAILABLE state. |

Terminal equality compares each side's actual status, operation, cause,
event anchor, all C4.1 P11 occupancy/capacity/admission/processed/drop/
overflow/failure observations, every new terminal field (including processed
count, last event and exact timestamp), and the full ordered pending queue
snapshot with priority keys. No terminal field is projected away. A
pair-gate stop cannot be recoded as a source runtime failure.

## 8. P01-P11 comparison and failure semantics

The complete preservation/addition matrix is
[`05-ppc11-compatibility-matrix.md`](./05-ppc11-compatibility-matrix.md).
P01, P02, P05-P10 retain existing exact ordered/bitwise equality with added
fields compared exactly. P03/P04/P11 add the records above; existing mandatory
v1 requirements are not waived. Every new evidence field is compared by
state, type, exact value, source locator/rule and record order.

At first divergence, preserve the last mutually comparable record on each
side and both failure identities. Stop both sides before the next event.
Never advance a counterpart to find a matching event. One-sided failure is
CONTRADICTED only when the other side's already captured P02 evidence proves
admission of the exact anchor; otherwise evidence is unavailable and P11 is
INCOMPLETE. Both traces stopping is not itself a matched terminal state.

Conditional branch states preserve the v1 rules exactly:
`MEASURED_ZERO`, `MEASURED_POSITIVE`, `COMPLETE_UNEXERCISED`,
`EVIDENCE_UNAVAILABLE`; pair outcomes remain
`BOTH_ZERO`, `EXERCISED_AND_COMPARED`, `UNEXERCISED`,
`ONE_SIDED_OCCURRENCE`, `EVIDENCE_UNAVAILABLE`. Missing fields never become
zero.

## 9. Historical v1 compatibility and rejection

* V1 traces remain readable and comparable only as v1 under the exact v1
  contract and identity conditions.
* Do not synthesize v2 evidence from v1 fields, default missing symbols, infer
  route outcomes, or assign failure causes.
* A v1/v2 comparison is `INCOMPARABLE`; it cannot be projected into a common
  subset because C4.1 projection exclusions are empty.
* New writers require explicit v2 source/contract identity. A schema version
  does not prove implementation identity or parity.

## 10. Change classification and approvals

| Proposal | Effect | Neural source change? | Owner approval before adoption? |
|---|---|---:|---:|
| Evidence-state union and source/derived locators | Adds observation capacity and clarifies missing vs inapplicable | No for schema; passive hooks may be needed | Yes, contract revision |
| Non-symbol creation record and completion `NOT_APPLICABLE` | Clarifies prediction semantics but changes P03 applicability for completion records | No semantic change; may require capture adapter | **Yes, substantive P03 acceptance change** |
| Exact next-symbol scalar mapping | Adds a DERIVED symbol under a reviewed equation | No model behavior change | **Yes, accept derivation as P03 contract evidence** |
| P04 route outcome/lineage correlation | Adds observation capacity; route semantics unchanged | Passive hooks may be required | Yes, schema/hook review |
| P11 failure taxonomy and stop alignment | Clarifies terminal/failure equality and adds observation capacity | Passive hooks may be required | **Yes, substantive P11 comparator adoption** |
| New schema ID and version | Adds explicit compatibility boundary | No | Yes |
| Historical trace migration | No automatic upgrade permitted | No | No migration without separate owner decision |
| Neural algorithm, parameters, deadlines, routing or learning | Not proposed | Would change model behavior | Not authorized |

## Conclusion

This is a reviewable candidate schema, not an accepted contract. It preserves
the C4.1 schema and all existing mandatory v1 fields/semantics at the v1
boundary. It does not authorize implementation, neural execution, paired
pilot, RP-2B work, publication, or architectural promotion.
