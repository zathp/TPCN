# PPC-11-C4.1 Paired Trace Schema and Comparison Specification

**Schema identifier:** `ppc11-paired-trace-1`  
**Wire format:** UTF-8 JSON Lines, one record per line; exactly one
`schema_version` per record.  
**Purpose:** Specify independent raw evidence, lossless numeric values, and
strict exact comparison. This is a future implementation contract, not an
implemented writer or parser.

## Trace file identity

- `*-original.jsonl` contains records captured directly from the original
  implementation's own execution.
- `*-instrumented.jsonl` contains records captured directly from the
  instrumented implementation's own execution.
- The two raw files are never copied, reconstructed, joined, or inferred from
  each other. Each has a separately recorded SHA-256, byte size, source
  identity, runtime identity, and capture provenance.
- A missing raw side, missing provenance, or unknown field blocks the
  comparison. Keep both raw traces immutable; derived comparison output is a
  separate file.

## Record envelope

Every record contains these exact envelope fields:

| Field | Type and semantics |
|---|---|
| `schema_version` | Literal string `ppc11-paired-trace-1` |
| `side` | Literal `original` or `instrumented` |
| `run_id` | Stable unique execution identifier, string |
| `source_revision` | Git commit identifier plus working-tree source-manifest digest |
| `runtime_manifest_sha256` | SHA-256 of exact runtime/dependency identity manifest |
| `seed` | Typed integer value; required value 17 |
| `arm` | One of `A`, `B`, `C`, `D` |
| `split` | One of `train`, `validation`, `test` |
| `example_id` | Frozen fixture identity; never generated as a substitute |
| `exposure_id` | Stable string mapped by the frozen fixture manifest to exactly one `(seed, arm, split, example_id)` tuple; identical across sides and not side-specific |
| `record_index` | Nonnegative typed integer, contiguous within a raw stream |
| `comparison_id` | One of `P01` through `P11`, or `BRANCH` |
| `record_type` | Closed, versioned event name defined by the reviewed writer |
| `payload` | Typed record object; unknown keys are schema errors |

The schema rejects duplicate record identity tuples
`(side, run_id, arm, split, example_id, record_index)`, missing required
fields, unknown enum members, malformed order, and unsupported type tags.
JSON numbers are not accepted for any model-visible numeric value.

## Lossless typed value encoding

Encode each number as a type-tagged raw representation; do not serialize a
model float as a JSON decimal number.

```json
{"kind":"f64","bits_be_hex":"3ff0000000000000"}
```

`bits_be_hex` is exactly the IEEE-754 bit pattern in network/big-endian byte
order: 16 lowercase hexadecimal digits for `f64`, 8 for `f32`. Preserve every
bit, including sign of zero and NaN payload. For exact-width signed/unsigned
integer source types, encode all source bits as fixed-width big-endian hex and
include the exact kind (for example `i64` or `u32`). For arbitrary-precision
integer source types, use canonical base-10 signed integer text with a
separate exact kind. Strings, booleans, null, symbols, and identities remain
typed source values. Unsupported source types are blocked rather than
coerced.

Typed values compare by exact kind and complete encoded representation.
Timestamps compare by their source type and exact value; no time rounding,
normalization, or tolerance is permitted.

## Required record families

The writer must emit enough independent records to satisfy the exact
requirements below. Each source observation is captured at the point where
that implementation makes or receives it; a post-hoc inference is not a
capture.

| P ID | Minimum record families and required payload |
|---|---|
| P01 | `input_event`: type, typed payload, timestamp, source/input order, channel ID, model-visible event ID |
| P02 | `enqueue`, `schedule`, `dequeue`, `process`: operation; complete anchor tuple (`exposure_id`, event ID, source, destination, event type); enqueue order; scheduled timestamp; queue sequence/tie key; dequeue/process timestamp; tie-break cause; `admission_outcome` on every enqueue record |
| P03 | `prediction_create`, `prediction_match`, `prediction_expire`, `prediction_settle`: prediction ID, expected symbol, create/due/match/expire/settle time, exact outcome |
| P04 | `omission_resolve`, `omission_route`, `omission_delivery`: origin prediction ID, omitted symbol/time, route, payload, emitted event ID, delivery result |
| P05 | `readout_feature`: decision identity/time, exact `z=s` typed value |
| P06 | `readout_drive`, `readout_activation`, `readout_decision`: each class index, exact weight/bias/feature/drive values, post-transfer activation, winner, tie set, tie-break order |
| P07 | `eligibility_create`, `eligibility_expire`, `eligibility_consume`, `eligibility_admission`: trace ID, weight/bias owner, value, creation/expiry/consume times, capacity and decision |
| P08 | `feedback_schedule`, `feedback_apply`, `feedback_reject`: feedback ID/origin, due/application time/order, sign, magnitude, duplicate/rejection reason |
| P09 | `parameter_initial`, `parameter_transition`, `parameter_final`: stable parameter ID, weight/bias kind, exact old/new bits, update cause, transition order/time |
| P10 | `classification_output`: example ID, predicted class, output time, model-visible emission identity and content |
| P11 | `queue_state`, `admission_decision`, `event_processed`, `queue_failure`: occupancy and capacity, exact P02 anchor tuple, processed count, drop/overflow/failure reason, admission outcome |

Record ordering is the source-observed order. Each trace preserves its own
event and operation order; comparison aligns by frozen paired exposure and
ordered model-visible records, never by a sorting pass that could erase
ordering differences. Source-specific bookkeeping must remain explicit. It
may not be discarded unless listed as an individually reviewed diagnostic
projection exclusion. The current exclusion list is empty.

## Conditional outcome register

For each of the nine branches, capture an explicit per-side state:
`MEASURED_ZERO`, `MEASURED_POSITIVE`, `COMPLETE_UNEXERCISED`, or
`EVIDENCE_UNAVAILABLE`, as defined by the contract. Derive one pair outcome:
`BOTH_ZERO` (both measured zero), `EXERCISED_AND_COMPARED` (both positive
with all occurrences exactly compared), `UNEXERCISED` (both conclusively
non-occurring, at least one complete-unexercised, neither positive),
`ONE_SIDED_OCCURRENCE` (one positive, counterpart conclusively
non-occurring), or `EVIDENCE_UNAVAILABLE` (either side lacks complete
occurrence evidence). A one-sided occurrence contradicts parity; absent
evidence is neither zero nor unexercised. A positive counter without its
occurrence records is evidence unavailable. Preserve the nine historical
statuses as `UNEXERCISED / NOT_EVIDENCED`, not measured zero.

## Comparator and stop semantics

1. Verify schema version, both source/runtime manifests, fixture hash, arm,
   split, example identity, and independently captured initial-parameter
   manifests before matching records.
2. Reject any schema drift, unknown field, duplicate record identity,
   missing required field, unsupported numeric representation, unexplained
   event-order divergence, or unapproved projection.
3. Compare each P01-P11 typed value and ordered record exactly. Floats compare
   by bit string; all other values compare by exact type and value.
4. Emit a complete machine-readable status for every P item, exact evidence
   locators for both sides, all mismatch/missing-field paths, branch status,
   source/fixture/parameter identities, and input/output hashes.
5. Any mismatch is `CONTRADICTED`; absent evidence is `INCOMPLETE`;
   unjustified mapping is `INCOMPARABLE`. Only fully evidenced exact
   comparisons may be `READY`.
6. For P11, align an attempted admission by the exact P02 tuple
   `(exposure_id, event_id, source, destination, event_type)`. All five
   fields are required non-empty strings and must match exactly. `exposure_id`
   is mapped by the frozen fixture manifest to `(seed, arm, split,
   example_id)` and is identical across both sides. Compare timestamp,
   payload, and sequence assignment/status separately. Every P02 enqueue
   record has required `admission_outcome` with one of `ADMITTED`, `REJECTED_CAPACITY`,
   `REJECTED_INVALID`, or `OTHER_FAILURE`; `ADMITTED` means the operation
   completed normally and the event was queued with an assigned sequence.
   On the first P11 failure, capture its triggering attempt and exact
   pre-failure queue state, then stop both executions for that exposure before
   either processes another event. Capture each side's actual event-loop
   boundary, last completed P02 operation, time, occupancy/capacity, and
   ordered pending identities/priority keys. Do not advance the counterpart
   to seek an event. Classify a one-sided failure only if the counterpart's
   pre-stop trace already contains the exact anchor admission with
   `admission_outcome = "ADMITTED"`. If that event has not been reached, or
   exact alignment/terminal evidence is unavailable, mark the branch
   `EVIDENCE_UNAVAILABLE` and P11 INCOMPLETE; a terminal snapshot cannot
   prove future behavior. The stop is not success and does not authorize a
   rerun.

No comparator implementation or neural trace was produced or executed under
C4.1.
