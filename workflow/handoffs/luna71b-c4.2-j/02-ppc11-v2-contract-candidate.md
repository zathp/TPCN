# Luna-71B-C4.2-J — PPC-11 v2 contract candidate

**Schema proposal:** `ppc11-paired-trace-2`  
**Status:** Independently reviewed PASS WITH FINDINGS; suitable for limited experimental use subject to formal owner adoption. Not adopted.  
**Baseline preserved:** `ppc11-paired-trace-1` and the C4.1 PPC-11 contract remain unchanged.  
**Owner direction:** OD-J-1 through OD-J-6.  
**I design source:** `workflow/handoffs/luna71b-c4.2-i/04-proposed-versioned-trace-schema.md`,
SHA-256 `d756d35037a5412c691024c3a7479cebfe9ec5ff985f0cc47c53e30f8542245f`.
The complete difference inventory is
[`01-v1-v2-contract-difference-matrix.md`](./01-v1-v2-contract-difference-matrix.md).
This candidate adopts only owner-selected diagnostic changes. It makes no
neural, scheduler, routing, learning, RNG, deadline, or queue-admission
change. The independent review found the contract direction suitable for
limited experimental use; the candidate remains subject to formal owner
adoption. This status does not authorize a real-source paired run, neural
execution, training, inference, or pilot.

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
{"state":"UNOBSERVED","reason_code":"CAUSE_NOT_EXPOSED","source_point":"..."}
{"state":"COMPLETE_UNEXERCISED","basis":"complete exposure boundary"}
{"state":"SOURCE_PATH_ABSENT","source_point":"..."}
```

The `value` uses the source type and the number representation below. The
allowed state union depends on field. `COMPLETE_UNEXERCISED` describes an
existing but unexercised branch; `SOURCE_PATH_ABSENT` means the model has no
such transition. Neither is a successful terminal outcome.
`UNOBSERVED` is restricted to evidence such as a P11 cause that the active
source boundary does not expose; it does not mean that no failure occurred.

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
| `expected_symbol_evidence` | `SOURCE_OBSERVED` or `DERIVED` evidence object whose value must exactly equal `expected_symbol`; DERIVED evidence binds mapping ID/revision, exact equation, source file identity/locator, original scalar bits, and provenance. `UNAVAILABLE` invalidates P03 and cannot produce a valid symbol-bearing creation record. |
| `created_at` | Exact source timestamp. |
| `due_time`, `expires_at` | Evidence-value unions distinguishing source time, not applicable, and unavailable. |
| `target_semantics` | Source-observed target kind/key, not inferred from labels. |

The proposed `next-symbol-sign-v1` derivation records the exact source scalar
and applies `A if predicted_value >= 0.0 else B`; rule source identity is
versioned. The evidence must bind the mapping ID and revision, exact equation,
source module's raw SHA-256 and Git blob identity where available, qualified
call site, scalar type/bits, derived value, and source locator. Luna-0 must
independently verify the mapping against the exact H source before the mapping
is used. It is a derivation, not a neural symbol field. The completion
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

The added non-symbol record is not a conversion of a v1 record. OD-J-2
expressly selects this P03 applicability distinction for the v2 candidate.
It does not waive any applicable match, expiry, or settlement requirement;
an absent source path remains incomplete.

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
  carries the frozen v1 `ADMITTED`, `REJECTED_CAPACITY`,
  `REJECTED_INVALID`, or `OTHER_FAILURE` outcome; P04 must not relabel route
  production as queue admission. If the P02 record is missing, the P04
  reference is explicitly `UNAVAILABLE` and P04 is incomplete; do not add an
  `UNAVAILABLE` admission outcome to the v1 field.
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

Keep every v1 queue/admission and terminal observation. P02 remains the
authoritative record for each queue admission decision; P11 does not add a
second admission outcome or redefine the P02 outcome values. Append passive
evidence at the existing scheduler/handler failure boundary:
* `failure_evidence`: active operation, event/lineage when present, exact
  source location, actual exception/failure identity and timestamp when
  exposed, last completed P02 operation, exact queue snapshot, and explicit
  evidence states. Record cause as `SOURCE_OBSERVED` only when the source
  exposes it; otherwise record `UNOBSERVED`. Do not infer a taxonomy or cause
  from a stopped loop, a missing event, or a generic exception.
* `execution_terminal`: source-observed event-loop boundary value, or
  `UNOBSERVED` if no such value is exposed; last completed P02 operation,
  timestamp, processed count, last event, queue occupancy/capacity, and
  ordered pending event IDs and exact source priority keys. Priority fields
  must be read from the scheduler/queue ordering point, not reconstructed
  from output order. Do not create a normal/budget/pair-stop/failure enum
  unless the source itself exposes that exact value.

`failure_record_ref` is a diagnostic locator, not a new model ID or a
substitute for actual failure identity. Preserve the exact source exception
or failure identity when exposed; otherwise report `UNOBSERVED`. A
capture-writer failure must be reported by an independent supervisor/sidecar;
the failing writer cannot attest to its own successful record. Hooks must
observe the existing operation and then preserve the existing result,
exception, queue mutation, event ordering and termination.

Required common field types:

| Field | Type |
|---|---|
| P02 alignment `anchor` | Object of exactly five non-empty strings: `exposure_id`, `event_id`, `source`, `destination`, `event_type`. |
| `occupancy_before`, `occupancy_after`, `capacity`, `processed_count` | Nonnegative typed integers; capacity positive when source provides it. |
| `sequence_assignment` | Tagged state with exact queue sequence when assigned; otherwise explicit `NOT_APPLICABLE` or `UNAVAILABLE`. |
| `boundary_value` | Exact source-provided event-loop boundary value, or `UNOBSERVED`; no candidate-defined terminal category. |
| `operation` | Evidence object containing observed operation and source location; use `UNAVAILABLE` when not exposed. |
| `source_location` | Object `{module, qualified_function, source_line}` with exact values when observed; otherwise explicit `UNAVAILABLE`. A location is diagnostic, not an event identity. |
| `exception_identity`, `reason_code` | Exact source-qualified exception/failure identity or stable reason code when observed; otherwise `UNOBSERVED`. Do not put guessed cause in this field. |
| `failed_event_id`, `lineage_id` | Existing source IDs or explicit NOT_APPLICABLE/UNAVAILABLE evidence objects. |
| `failure_record_ref`, `last_common_record` | Diagnostic locator objects based on trace envelopes; never model-visible IDs and never substitutes for `exception_identity`. |
| `pending` | Ordered array of exact source event IDs, timestamps and queue sequences/priority keys. |
| `terminal_timestamp` | Exact typed source time or explicit UNAVAILABLE state. |

The frozen C4.1 P11 comparison and stopping rules remain the comparator
authority. V2 retains every v1 comparison objective. The operation and
exception/cause identity fields added by OD-J-4 are diagnostic evidence, not
new parity-gating equality criteria. Existing source-defined priority keys
remain exactly compared under P02. The actual terminal boundary, last
completed P02 operation, timestamp, queue occupancy/capacity, and ordered
pending identities/priority keys required by C4.1 remain mandatory P11
evidence; if unavailable, P11 is INCOMPLETE. Mark an unexposed failure cause
`UNOBSERVED`, but do not treat that marker as satisfying some other missing
C4.1 terminal requirement. No new failure-matching rule, stop condition, or
terminal success state is introduced. A pair-gate stop cannot be recoded as a
source runtime failure.

## 8. P01-P11 comparison and failure semantics

The complete preservation/addition matrix is
[`01-v1-v2-contract-difference-matrix.md`](./01-v1-v2-contract-difference-matrix.md).
P01, P02, P05-P10 retain existing exact ordered/bitwise equality with added
fields compared exactly. P03/P04/P11 add the records above; existing mandatory
v1 requirements are not waived. New P03/P04 fields that instantiate their
existing objectives are compared exactly by state, type, value, source
locator/rule and record order. New P11 active-operation, failure-identity and
cause fields are diagnostic only; they do not independently change a P11
parity result. C4.1-required terminal-boundary/queue evidence is not
optional: its absence remains P11 INCOMPLETE. The existing P11 fields and
P02 priority/order requirements retain exact comparison.

At first divergence, preserve the last mutually comparable record on each
side and both failure identities. Stop both sides before the next event.
Never advance a counterpart to find a matching event. One-sided failure is
adjudicated only under the existing C4.1 P11 rule: the counterpart's
already-captured P02 evidence must prove admission of the exact anchor;
otherwise evidence is unavailable and P11 is INCOMPLETE. Do not add a new
failure taxonomy, matching category, or stopping rule. Both traces stopping
is not itself a matched terminal state.

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
| New schema ID, closed v2 records, lossless evidence states | Additive observation and explicit compatibility boundary | No; passive hooks may be needed | Owner-selected direction; independent review required |
| P03 derived symbol with source scalar/rule/revision/provenance | Clarifies a source mapping and its evidence status | No model change | OD-J-2 selected; exact mapping still requires Luna-0 source verification |
| P03 completion `NOT_APPLICABLE` creation | Changes applicability only for a source-established nonsymbol completion prediction | No model change | OD-J-2 selected; settlement remains required where the source defines it |
| P04 lineage, route/admission/delivery/rejection observations | Adds passive evidence and separates existing stages | No model change | OD-J-3 selected; hook passivity requires independent verification |
| P11 operation, actual failure identity, priority and terminal boundary | Adds passive evidence at existing scheduler/handler boundaries; new operation/cause/boundary fields are non-gating diagnostics, while existing priority remains compared under P02 | No model change | OD-J-4 selected; comparator must retain C4.1 stop/adjudication rules |
| Comparator acceptance or failure-stop rule beyond this document | Changes outcome semantics | Not permitted by this candidate | **Not authorized; return for separate owner decision** |
| Historical migration, projection, substituted identities | Changes or weakens evidence | No | Not authorized |
| Neural algorithm, parameters, deadlines, routing, queue decisions, learning, or RNG | Changes model behavior | Yes | Not authorized |

## Conclusion

This is a reviewable candidate schema, not an accepted contract. It preserves
the C4.1 schema and all existing mandatory v1 fields/semantics at the v1
boundary. It does not authorize implementation, neural execution, paired
pilot, RP-2B work, publication, or architectural promotion.
