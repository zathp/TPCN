# PPC-11-C4.1 P01-P11 Capture Requirement Matrix

**Contract:** [`02-ppc11-reconstituted-contract.md`](./02-ppc11-reconstituted-contract.md)  
**Rule:** "Contract complete" is independent of "source capture ready." Statuses
below preserve C3.1 source-level findings; this matrix does not assert that
future bilateral trace implementation exists.

| ID | Exact comparison fields | Source-level status | Existing gap / implementation evidence needed |
|---|---|---|---|
| P01 Input events | Type, typed payload, timestamp, input order, channel, model-visible ID | READY (source level only) | Future paired traces still need independent source-side records and exact per-exposure comparison. |
| P02 Scheduler ordering | Enqueue operation, scheduled event, identity, queue/tie key, dequeue, process time/order | INCOMPLETE | No enqueue instant or explicit scheduled-event record; deriving the scheduled set needs review. Existing processed-row sequence is enqueue/tie-break order; internal events may defer behind same-time external events to the same destination. An absence-observation row has no queue sequence and must be handled explicitly. |
| P03 Prediction lifecycle | Create/ID/expected symbol/create and due time/match/expiry/settlement | INCOMPLETE | Missing original-side prediction due/expiration identity and time records. `prediction_expired_count` is exposure-level only; expiration is observation-time driven and does not settle the readout prediction. |
| P04 Omission resolution | Origin prediction, omitted symbol/time, route, payload/event ID, delivery | READY (source level only) | C3.1 source-level assessment retains this status. No bilateral C4 capture or parity is established. |
| P05 Readout feature | Decision-time `z=s` exact typed value and bits | READY (source level only) | Future evidence must independently capture both sides' exact decision-time scalar. |
| P06 Readout competition | Four pre-transfer affine drives, post-transfer values, winner, ties/order | INCOMPLETE | Original-side `drive` is local and not exposed. Post-edge payload is not a bit-exact substitute; `atanh` inversion is impermissible. Four affine values need capture or a separately justified exact derivation. Prior review found no evidenced tie mismatch; that does not close missing-drive capture. |
| P07 Eligibility | Weight/bias traces, values, ownership, expiry, consume, capacity/admission | INCOMPLETE | Creation activity and some consumption attribution are exposed, but ledger-internal trace values, exact expiry boundary/events, and capacity decisions are missing. |
| P08 Feedback lifecycle | ID/origin/schedule/due/application time/order/sign/magnitude/duplicate/rejection | INCOMPLETE | Feedback scheduling and application ordering are absent from original-side capture. Duplicate/rejected outcomes remain branch evidence requirements. |
| P09 Parameter transitions | Initial snapshot, every ordered weight/bias update, next-symbol ordering, final state | INCOMPLETE | Ordered next-symbol parameter updates are not captured bilaterally. Independently verify complete initial and terminal states. |
| P10 Classification output | Class, output time, model-visible emissions and identities | READY (source level only) | This is not an execution or parity result; future independent captures still required. |
| P11 Queue and admission | Occupancy at each transition, admission, processed count, drop/overflow/failure | INCOMPLETE | Existing counters are not a substitute for true occupancy/admission/drop evidence. No hard-coded or missing-as-zero measurements. |

## Decision rule

All eleven comparison definitions and exact acceptance rules are
contractually complete. Source-level capture remains **PARTIAL**: P01, P04,
P05, and P10 were assessed READY at source level by C3.1; P02, P03, P06, P07,
P08, P09, and P11 remain INCOMPLETE. None is promoted by drafting this
contract. No C4 bilateral passive capture or reviewed paired driver is
implemented.

For every branch, record the contract's per-side evidence state and pair
outcome separately. The nine historical statuses remain
`UNEXERCISED / NOT_EVIDENCED`, not measured zero. A one-sided positive
occurrence with a conclusively non-occurring counterpart is CONTRADICTED; a
missing occurrence record is EVIDENCE_UNAVAILABLE, never zero or
unexercised.
