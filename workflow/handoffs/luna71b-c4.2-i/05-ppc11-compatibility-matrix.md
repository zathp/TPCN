# Luna-71B-C4.2-I — PPC-11 compatibility and equality matrix

**Status:** Proposed v2 compatibility design; adoption requires a separate owner decision.  
**Frozen baseline:** PPC-11 C4.1 at commit `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`, manifest SHA-256 `2f18d694784a6a583b0a7c01e6cc89f1313c2d65c7c6b5346a7cd4d993d3f1fa`.

## Compatibility rules

* `ppc11-paired-trace-1` and its C4.1 contract are unchanged.
* `ppc11-paired-trace-2` is a proposed append-only schema with an explicit
  version boundary. No v1 record is silently migrated or weakened.
* Exact, typed, ordered and bitwise equality remains the comparison rule.
* Unknown fields, absent evidence, unsupported numeric types, unapproved
  projections, and cross-version comparisons fail closed.
* Source observation, justified derivation, non-applicability, unavailability,
  unexercised behavior, and absent source paths are different states.

## P01-P11 matrix

| ID | Frozen C4.1 requirement retained | Proposed v2 addition | Equality / incomplete disposition | Change class and approval |
|---|---|---|---|---|
| P01 Input events | Type, typed payload, timestamp, order, channel, model-visible identity | No required behavioral change; evidence-state envelope may identify unavailable locator | Exact ordered values and bits | Adds provenance only; owner approval for schema |
| P02 Scheduler ordering | Enqueue/schedule/dequeue/process, queue/tie key, timestamp, deterministic tie-break | Carry explicit operation evidence and admission outcome link | Exact order, source queue sequence, tie-break cause and timestamp | Adds observation capacity; passive capture only, owner approval |
| P03 Prediction lifecycle | Creation/identity, expected symbol, create/due, match, expiry, settlement/disposition | Preserve existing `prediction_create`/required string for symbol-bearing predictions; add symbol provenance evidence and a separate `prediction_create_non_symbol` with explicit `NOT_APPLICABLE` state | Compare kind, field state/rule/value, every source transition. `SOURCE_PATH_ABSENT` is incomplete, never a settlement. | Adds record type, but changes P03 applicability for completion predictions and permits a DERIVED symbol; **owner decision required** |
| P04 Omission resolution | Origin prediction, omitted symbol/time, route construction, emitted payload/event, delivery | Link prediction/error/route event/lineage; explicit admission, rejection, duplicate, delivery and integration outcomes | Exact existing identities and event order; unavailable cause remains unavailable | Adds observation capacity; passive hooks; owner approval |
| P05 Readout feature | Exact decision-time `z=s` | No relaxation; source/availability locator only | Exact source bits; missing field blocks | Adds provenance; no acceptance change |
| P06 Readout competition | All four drives, activations, candidate/winner/ties/tie-break | No relaxation; preserve source order/bit representation | Exact typed values, bits and ordering | Adds provenance; no acceptance change |
| P07 Eligibility | Create/trace/owner/value/expiry/consume/capacity/admission | Explicit reason/evidence state for rejection and unexercised paths | Exact values and transition order; no missing-as-zero | Adds observation capacity; owner approval |
| P08 Feedback lifecycle | Identity/origin/schedule/due/apply/order/sign/magnitude/duplicate/rejection | Explicit source-vs-derived reason evidence | Exact event order/value; unknown cause remains unavailable | Clarifies ambiguity; owner approval |
| P09 Parameter transitions | Initial, every transition, cause/order, final | No reduction; link transitions to source events where available | Exact complete bitwise transition path | Adds reference only; no acceptance change |
| P10 Classification output | Predicted class, time, each model-visible emission/identity | No reduction; preserve output event identity and type | Exact order/content/time | Adds provenance only |
| P11 Queue/admission | Occupancy/admission/processed/drops/overflow/failure | Failure taxonomy, operation/location, source cause evidence, actual terminal state, paired stop/alignment refs | Exact comparison of every C4.1 P11 observation and every v2 terminal field, including timestamp, processed count, last event, occupancy/capacity, pending identity/order/priority, and admission/failure result; one-sided failure requires exact already-admitted anchor; two stops are not a match | Adds observation capacity and changes failure comparison details; **owner decision required** |

The P01-P11 list is complete. No projection or omission is proposed. P05-P10
remain no less strict than the frozen C4.1 comparator.

## Failure alignment and first divergence

The comparator first validates both v2 schemas and independent source,
runtime, fixture, exposure, and initial-parameter identities. It compares
ordered records within each exposure and reports the first exact divergence
with both record indices and all later evidence preserved as raw data.

P11 admission alignment uses the exact P02 five-field anchor
`(exposure_id,event_id,source,destination,event_type)`, all non-empty strings.
Timestamp, payload, sequence, priority, and admission result compare
separately. At a failure, stop both sides before either processes a further
event; retain both real terminal snapshots and last common operation. Do not
advance the counterpart.

P11 compares every frozen C4.1 queue/admission/processed/drop/overflow/failure
observation and every v2 terminal field: terminal status, operation, cause,
last completed operation, timestamp, last event, processed count, occupancy,
capacity, ordered pending identities/priority keys, and both failure locators.
There is no terminal diagnostic projection.

* Exact matching evidence on both sides can establish a matched P11
  transition only when operation, source cause and aligned event all compare.
* One side fails and the counterpart has already admitted the exact anchor:
  `CONTRADICTED` if its next behavior differs under the contract.
* Counterpart has not admitted the anchor, or evidence is unavailable:
  `EVIDENCE_UNAVAILABLE`, P11 `INCOMPLETE`.
* Both traces stop: no automatic match; compare actual terminal status, event,
  operation and cause. A pair gate stop is not a source failure.

## Historical traces and versioned test strategy

V1 traces retain their exact historical interpretation. V2 cannot be
backfilled from missing v1 fields. A mixed v1/v2 pair is `INCOMPARABLE`, not
equal on a projection. Legacy regression expectations remain immutable.
Version-qualified tests must key expectations by contract version, source
manifest revision, commit/tree, Git blob identity, raw checkout hash and line
ending materialization. A historical expected identity is not replaced by
the H identity.

The corresponding regression proposal is documented in
[`07-regression-and-provenance-assessment.md`](./07-regression-and-provenance-assessment.md).

## Change classification

| Proposed item | Adds observation capacity | Clarifies ambiguity | Changes acceptance | Neural source modification | Owner decision |
|---|---:|---:|---:|---:|---:|
| Source/derived/unavailable tagged values | Yes | Yes | No for old requirements | No; capture-only | Contract adoption |
| P03 non-symbol creation record and explicit NA symbol | Yes | Yes | Yes | No model change; capture adapter may change | Required |
| Derived next-symbol mapping | Yes | Yes | Yes | No model change | Required |
| P04 route/failure/lineage records | Yes | Yes | No if missing data stays INCOMPLETE | Passive hooks may be needed | Required |
| P11 typed failure/stop alignment | Yes | Yes | Yes for failure disposition | Passive hooks may be needed | Required |
| New v2 identity, records and parser rules | Yes | Yes | No acceptance relaxation | No | Required |
| Historical migration/projection | No | No | Would weaken evidence | No | Not proposed; prohibited without another decision |

## Conclusion

PPC-11 C4.1 remains authoritative and unchanged. The matrix is a proposed
v2-compatible expansion only; it is not an approval of the schema, its
acceptance changes, implementation readiness, neural parity, or pilot.
