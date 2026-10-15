# PPC-11-C4.1-RECONSTITUTED

**Status:** New self-contained documentary candidate; subject to independent
review.  
**Purpose:** Define the eleven exact paired behavioral comparisons and the
evidence rules required for any separately authorized C4 implementation.  
**Execution authority:** None. This contract does not authorize source edits,
instrumentation, a paired driver, model execution, training, inference, pilot
execution, or publication.

## 1. Pairing unit and identity

The pairing unit is one identified example exposure, within a frozen split,
arm, and implementation pair. An implementation pair consists of the
original-side execution and instrumented-side execution for the same
seed-17 arm, split, example identity, and initial parameter identity.
Comparison is per exposure and ordered trace, not aggregate accuracy.

Preserve the prepared pilot unchanged:

- Seed 17; four arms A, B, C, D.
- Four temporal classes AB, BA, A-only, B-only.
- Twelve examples per class in each of train, validation, and test.
- 48 examples per split; 144 distinct split exposures per arm.
- 576 exposures per implementation across the four arms; 1,152 paired
  implementation exposures in total.

These counts do not prove fixture identity. Before any future execution,
verify the exact historical preparation artifacts and six full-split
identities from R6. Do not regenerate a fixture or treat a replacement as
historical. The test split is for parity verification only under separate
execution authorization; it is not available for learning-rule tuning.

For each arm and side, capture the complete pre-exposure parameter manifest.
The R6 initial-parameter digest
`5a53d0cc7e41a7431d584bd711f0a1d0ba735a69f6e84b1b9298fa41f289948a` is
reported for all seeds and is therefore seed-independent; it cannot establish
seed identity by itself. Future evidence must show both sides' exact
parameter identities independently before exposure.

## 2. Exact behavioral requirements

Every P01-P11 comparison is an ordered, per-exposure comparison between
independently captured original and instrumented evidence. Compare model
visible values and identities exactly. No decimal tolerance, epsilon, inferred
field, aggregate proxy, missing-as-zero behavior, or broad projection is
permitted.

| ID | Required observations on both sides | Acceptance |
|---|---|---|
| P01 - Input events | Event type; payload and payload type; timestamp; enqueue/input order; channel identity; model-visible event identity | Exact ordered equality |
| P02 - Scheduler ordering | Enqueue operation; scheduled model event and identity; queue/tie key; dequeue; processing timestamp; deterministic tie-breaking order | Exact ordered equality |
| P03 - Prediction lifecycle | Prediction creation and identity; expected symbol; creation and due time; match observation; expiration; settlement and disposition | Exact ordered equality |
| P04 - Omission resolution | Originating prediction identity; omitted symbol; omission time; route construction; emitted payload and event identity; delivery outcome | Exact ordered equality |
| P05 - Readout feature | Exact decision-time scalar `z = s`, including its source representation | Exact binary-floating-point bit equality |
| P06 - Readout competition | All four `d_k(z) = w_k*z + b_k` affine drives; post-transfer activations; candidate/winner; ties; tie-breaking rule and result | Exact equality, including float bits and order |
| P07 - Eligibility | Weight and bias eligibility creation; trace identity/value; owner; expiry; consumption; capacity/admission and rejection decisions | Exact ordered equality |
| P08 - Feedback lifecycle | Feedback identity and origin; scheduling/due/application times; application order; sign/magnitude; duplicate and rejection outcomes | Exact ordered equality |
| P09 - Parameter transitions | Initial parameters; each ordered weight/bias transition; update cause and next-symbol update order; final parameters | Exact transition order and float-bit equality |
| P10 - Classification output | Predicted class; output time; each model-visible output emission and associated identities | Exact ordered equality |
| P11 - Queue and admission | Queue occupancy trajectory; each admission decision; processed event counts; drops; overflow; failure result | Exact ordered equality |

No comparison is waived because a branch does not occur. A required source
field that cannot be captured or justified is INCOMPLETE; an unsupported
cross-implementation semantic mapping is INCOMPARABLE; an observed mismatch
is CONTRADICTED. READY requires complete bilateral evidence, exact fixture
and parameter identity, and an independently reviewed comparison.

## 3. Exact numerical policy

Compare integer values, symbols, IDs, timestamps, order, statuses, event and
queue outcomes by exact typed value. Compare floating-point values by the
complete source bit pattern, not by formatted decimal text. Preserve signed
zero and all NaN payload bits if the source emits them. Do not convert through
JSON numeric literals or `atanh`/other inverse calculations. If the source
numeric type or exact bits cannot be established, the affected comparison is
blocked pending an explicit owner decision; no tolerance may be substituted.

The lossless wire representation is specified in
[`05-paired-trace-schema-and-comparison.md`](./05-paired-trace-schema-and-comparison.md).

## 4. Independent evidence and conditional branches

`*-original.jsonl` is evidence captured independently from the original-side
execution. `*-instrumented.jsonl` is evidence captured independently from
the instrumented-side execution. Each raw stream must be generated directly
from its own execution. Copying, inferring, mirroring, or deriving one side's
hidden observations from the other side's trace is prohibited.

For every conditional branch, record a per-side evidence state and a
separate pair outcome.

Per-side evidence states:

- `MEASURED_ZERO`: complete capture contains an independently measured
  occurrence counter equal to zero.
- `MEASURED_POSITIVE`: complete capture contains a positive occurrence
  counter and the corresponding occurrence records.
- `COMPLETE_UNEXERCISED`: complete execution evidence proves the branch was
  not reached; no occurrence is asserted and no zero counter is inferred.
- `EVIDENCE_UNAVAILABLE`: the capture is incomplete or the branch occurrence
  cannot be determined. Never treat this as zero or unexercised.

Pair outcomes:

- `BOTH_ZERO`: both sides are `MEASURED_ZERO`.
- `EXERCISED_AND_COMPARED`: both sides are `MEASURED_POSITIVE` and every
  corresponding occurrence is exactly compared.
- `UNEXERCISED`: both sides conclusively establish no occurrence, with at
  least one side `COMPLETE_UNEXERCISED` and neither side positive.
- `ONE_SIDED_OCCURRENCE`: one side is `MEASURED_POSITIVE` and the other
  conclusively establishes no occurrence; the comparison is CONTRADICTED.
- `EVIDENCE_UNAVAILABLE`: either side is `EVIDENCE_UNAVAILABLE`, or the
  available records cannot resolve the pair. No absence or zero is inferred.

If a side records a positive count but its occurrence records are missing,
that side is `EVIDENCE_UNAVAILABLE`, not `MEASURED_POSITIVE`. An exact
comparison cannot proceed on the count alone. Do not replace missing fields
or counters by zero or present hard-coded zero counters as measurements.
Preserve the nine historically `UNEXERCISED / NOT_EVIDENCED` branches:
queue overflow/drop/failure; duplicate feedback; rejected feedback;
prediction expiration; prediction settlement; omission resolution; score
ties/tie-breaks; eligibility expiration; eligibility consumption. This
historical label is not a per-side zero measurement. Do not broaden the frozen
pilot to force their exercise.

## 5. Diagnostic projection

The C4.1 projection exclusion list is empty. All model-visible, state,
identity, timing, ordering, parameter, queue, and outcome fields remain in
the parity comparison. Any future diagnostic-only projection must enumerate
each exact field path individually, document its source and rationale, and
receive separate independent review and owner decision before use. Unknown
fields fail closed. Wildcard, prefix, regex, or "all diagnostics" exclusions
are forbidden.

## 6. Stop conditions and reporting

Before any separately authorized execution, verify both source identities,
runtime/dependencies, split identities, arm mapping, and independent
initial-parameter manifests. Stop before exposure if any identity is missing
or differs. During a future separately authorized run, stop the affected
pair on missing required data, unsupported numeric encoding, schema drift,
overflow/failure, or first exact mismatch; preserve both raw files and the
failure record. A stop is not success and does not authorize a rerun or
repair.

The comparison report must identify each P01-P11 status, both evidence
locators, fixture/parameter/source identities, every missing or mismatched
field observed through the stop boundary, per-side and pair branch states,
and raw input/output hashes. Preserve all evidence immutably and issue a new
contract revision for any substantive correction.

For P11 overflow, drop, queue-capacity, or admission failure, capture the
triggering attempt and exact pre-failure queue state on the side that detects
it before stopping that exposure. The alignment anchor is the exact P02
enqueue/admission tuple `(exposure_id, event_id, source, destination,
event_type)` for the attempted event; timestamp, payload, and sequence
assignment/status are separately compared and are not substitutes for this
identity. In the trace envelope, `exposure_id` is a stable string mapped by
the frozen fixture manifest to exactly one `(seed, arm, split, example_id)`
tuple. It is identical across the original and instrumented sides and is not
side-specific. The P02 record must contain the complete five-field anchor;
each field is a non-empty string and compares exactly.

On the first P11 failure, stop model-event processing for both executions of
that paired exposure before either processes another event. Capture an
explicit terminal record on each side at its actual event-loop boundary:
last completed P02 operation, current timestamp, queue occupancy/capacity,
and ordered pending event identities/priority keys. Do not advance the
counterpart to seek a matching event. A `ONE_SIDED_OCCURRENCE` /
CONTRADICTED outcome is permitted only if the counterpart's independently
captured pre-stop P02 records already contain the exact alignment-anchor
admission with `admission_outcome = "ADMITTED"`. This outcome means the
admission operation returned normally and the event was queued with an
assigned queue sequence. If the counterpart has not reached that admission,
lacks the record, or cannot establish the exact anchor, classify the branch
`EVIDENCE_UNAVAILABLE` and P11 INCOMPLETE; a terminal queue snapshot does not
prove what would have happened later. A stop is neither success nor
permission to rerun; any rerun requires separate authorization.

## 7. Non-claims

Contractual completeness does not establish source capture readiness,
implementation completeness, a paired driver, parity, efficacy, or
architecture conformance. No model or instrumentation change, neural
execution, pilot, test split learning, commit, push, merge, or publication
occurred under this contract. Any implementation and any execution require
separate explicit owner authorization and independent review.
