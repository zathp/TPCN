# Luna-71B-C4.2-J — P03/P04/P11 source-capture assessment

**Evidence boundary:** Source inspection and synthetic test doubles only.
No neural runner, training, inference, fixture execution, or paired pilot was
run. The J-only paired interface is injected-backend infrastructure, not a
production neural backend.

## P03 — prediction lifecycle

**Status: INCOMPLETE.**

The J source variants capture:

- Symbol prediction creation at the existing `LocalPredictor` call site,
  retaining the original scalar and explicitly marking A/B as `DERIVED`
  through the versioned sign mapping. The mapped symbol is not represented
  as source-observed.
- Completion predictions as non-symbolic `NOT_APPLICABLE`; no expected
  symbol is fabricated.
- Source-observed prediction match, observation event/lineage references,
  expiry, and settlement where those source transitions occur.
- External-deadline absence as a distinct nonsymbolic observation, without
  autonomous silence detection.

Source hook locations in the isolated J copies:

| Event/path | Original source copy | Instrumented source copy |
|---|---|---|
| Prediction creation and match | `experiments/luna71b_c4_2/j/variants/original/tpcn/luna70_readout_learning.py` | `experiments/luna71b_c4_2/j/variants/instrumented/tpcn/luna70_readout_learning.py` |
| Expiry and settlement transitions | `experiments/luna71b_c4_2/j/variants/original/tpcn/predictive_coding.py` | `experiments/luna71b_c4_2/j/variants/instrumented/tpcn/predictive_coding.py` |
| Active failure and terminal queue boundary | `experiments/luna71b_c4_2/j/variants/original/tpcn/event_runtime.py` | `experiments/luna71b_c4_2/j/variants/instrumented/tpcn/event_runtime.py` |

V2 settlement now requires an exact reference to an earlier source match or
expiry record for the same prediction, with matching disposition, outcome,
and timestamp. This prevents an unlinked, dangling, future, mismatched, or
otherwise forged `prediction_settle` from satisfying P03.

The inspected source ordering exposes a real coverage gap. The predictive
coding match callback emits settlement before the caller's v2 match record is
observed; capture therefore emits a P03 gap rather than looking ahead,
reordering events, or fabricating a settlement. Expiry emits the trigger
before settlement and can be linked where the source record is available.
Readout completion predictions still lack a settlement event on every
exposure path. Match or expiry alone does not substitute for settlement, and
the source is not modified to create a missing transition. The synthetic suite
tests valid linked settlement and rejects forged/dangling/mismatched evidence;
the actual source-order gap remains incomplete.

## P04 — omission provenance

**Status: INCOMPLETE for anomalous route/admission paths; normal v2 capture
path is represented statically.**

The existing external-deadline source path obtains the omitted target from
the pending prediction's scalar and preserves the exact derivation. No true
label, evaluation-only field, dataset name, class branch, or classifier result
is read. The hooks capture the originating prediction, trigger, error
identity, existing event and lineage IDs, route attempts and outcomes,
P02 admission references, destination integration, and observed duplicate or
rejection causes. They do not introduce model-visible IDs, autonomous
silence detection, route retries, or queue behavior changes.

Three stale v1-specific `capture_gap` claims were corrected only in the J
v2 source copies because v2 now records the pending prediction target, route
lineage, and duplicate rejection directly. The legacy no-v2 fallback retains
those original gaps. A route that returns an anomalous number of events still
emits a P04 gap; the comparator fails closed if route/admission/delivery
evidence is missing. Synthetic tests exercise both v2 source variants with
label-isolated test doubles and verify that actual P03 and P04 gaps remain
incomplete.

## P11 — terminal priority and failure evidence

**Status: COMPLETE at static/synthetic capture level; runtime parity is
NOT TESTED.**

The isolated event-runtime copies observe the active operation and exception
identity at the failure boundary, with `UNOBSERVED` cause where the source
does not expose one. Terminal queue state preserves the ordered pending
events and source priority keys. The corrected timestamp uses the observed
failed or active event at the boundary when available, including failure
before any event was processed; no timestamp is invented when the source
does not provide one. P02 remains the exact priority/tie-order comparator.

The v1 `terminal_state` evidence remains mandatory and exactly compared.
Added `execution_terminal` and `failure_evidence` records remain
non-gating diagnostics; their semantic field types and ranges are validated,
but differing or absent diagnostic values do not alter P11 comparison
status. Synthetic tests cover a failure before processing, a failure after
prior work, malformed diagnostic types/ranges, and differing or absent
non-gating diagnostic records.

## Overall limit

Static capture code and synthetic records do not establish that a real
original/instrumented neural pair emits these records or behaves identically.
The remaining P03 settlement and anomalous P04 route/admission gaps prevent
static PPC-11 readiness from being declared. Historical identity restrictions
are separately documented in
[`05-historical-identity-reconciliation.md`](./05-historical-identity-reconciliation.md).
