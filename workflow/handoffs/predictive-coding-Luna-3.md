# Luna agent handoff

```yaml
tpcn_handoff:
  agent: Luna-3 Predictive Coding and Error Events
  task_id: "predictive-coding"
  component: "bounded local prediction matching and causal prediction-error events"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "53ae36d"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A15"]
  preserves:
    - "Luna-1 Event, EventQueue, LocalClock, timestamp, ordering, capacity, and queued propagation semantics."
    - "Luna-2 TPCNNeuron local state and activation interface; no neuron policy was redefined."
    - "Luna-4 BoundedTopology finite routing, positive edge delay, and atomic fan-out admission."
    - "Classification, local energy utility, delayed credit, structural plasticity, and hardware validation remain outside this assignment."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/predictive_coding.py"
    - "tpcn/__init__.py"
    - "tests/test_predictive_coding.py"
    - "workflow/handoffs/predictive-coding-Luna-3.md"
  tests_added:
    - "tests/test_predictive_coding.py"
  tests_passing:
    - "Focused Luna-3 suite: 12 passed"
    - "Full available regression suite: 39 passed"
    - "Focused and full package diagnostics: no errors"
  tests_failed: []
  tests_not_run:
    - "Luna-11 acceptance matrix and streaming stroke classification benchmark"
    - "Local energy and reward-adjusted utility validation"
    - "Delayed credit and eligibility policy validation"
    - "FPGA, FPAA, hybrid, and hardware-equivalence validation"
  assumptions:
    - "Scalar target values are the minimal reusable reference representation; richer local target payloads remain downstream extensions."
    - "The explicit target key is the deterministic observation association key."
    - "Prediction expiry is exclusive: an observation at expires_at is eligible, and later observations are unmatched."
    - "Queue and topology capacity exceptions provide the existing bounded backpressure policy."
  unresolved: []
  recommended_next_agent:
    - "Luna-5: consume PredictionError for local energy/resource accounting without adding reward policy here."
    - "Luna-7: consume prediction and error records for an external streaming classifier interface."
    - "Luna-8: consume prediction IDs and timestamps as local causal metadata for delayed credit."
    - "Luna-11: independently verify the complete acceptance matrix after downstream components exist."
```

## Outcome and owned scope

Implemented `LocalPredictor` in `tpcn/predictive_coding.py` and exported its
public records from `tpcn`. The predictor has finite outstanding capacity,
local time, deterministic prediction IDs, local prediction creation from an
explicit scalar or a `TPCNNeuron` activation, delayed observation matching,
expiry, bounded counters, queued prediction emission, and explicit
`PredictionError` records. It does not maintain a global registry or run a
fixed prediction timestep.

## Prediction and observation semantics

- A prediction is a local scalar target value, created at the predictor's
  local timestamp or an explicitly supplied local timestamp. Its identity is
  `predictor_id:prediction:<sequence>`, where the sequence is a deterministic
  local counter. It includes a target key, predicted value, creation time,
  optional expected resolution time, and optional expiry time.
- An observation is an `Observation(target_key, observed_value)` payload in a
  later `Event`. The target key is the complete deterministic association key;
  no global event index, label, or future data is consulted.
- A matching observation may arrive after any local-time interval. The oldest
  eligible outstanding prediction for the key is selected by
  `(created_at, prediction_id)`. Thus multiple simultaneous predictions are
  deterministic and one observation resolves at most one prediction.
- Error is `observed_value - predicted_value`. A matched prediction is removed
  from outstanding state and returned with its `PredictionError`.
- A prediction may be emitted as a queued `prediction` event from its local
  creation timestamp. This is a transport record only; it does not mutate the
  remote destination inline or alter matching state.
- Expiry is exclusive. Explicit expiration or observation processing removes
  records whose expiry is strictly before the current local timestamp. An
  observation at the expiry timestamp remains eligible. Unresolved records
  remain bounded and outstanding until matched or expired; unmatched and
  duplicate observations increment a bounded counter and produce no error.
- A matched error event has source `predictor_id`, destination
  `error_destination`, event type `prediction_error`, and the observation's
  timestamp. With no topology it is queued with Luna-1 at that timestamp; with
  `BoundedTopology` it is admitted through finite positive edge delays. No
  remote destination is mutated inline.

## Architecture evidence

- **A01-A03:** prediction creation and matching advance only one local clock;
  irregular timestamps work without a global timestep. Error events are
  queued, and topology routing preserves finite propagation and equal-time
  queue ordering.
- **A04/A08:** outstanding predictions are capped by `max_outstanding`; full
  capacity raises `PredictionCapacityError`, and expiry removes records
  deterministically. Error delivery uses the existing finite queue and
  topology budgets.
- **A06:** local components form scalar predictions and represent subsequent
  error explicitly in both a record and a routable event.
- **A07:** matching uses only the predictor's local records and the permitted
  observation event. No labels, global registry, future stroke points, loss
  broadcast, or backpropagation is introduced.
- **A15:** records are fixed-schema dataclasses, state is bounded, and the
  implementation uses abstract local time and opaque event payloads suitable
  for a hardware-neutral reference.
- **A05, A09-A14:** no spatial reservoir, energy policy, delayed-credit policy,
  mandatory gates/pathways, or structural plasticity was added.

No Architecture Change Proposal is required. The implementation fills the
downstream A06 semantics authorized by the contract and accepted handoffs; it
does not amend A01-A15.

## Interfaces exposed for downstream roles

Luna-7 can consume `Prediction`, `Observation`, `PredictionError`, and
`PredictionResolution` without importing classifier policy. Luna-8 can use
prediction IDs, creation/observation timestamps, target keys, and signed
errors as local causal metadata without receiving an eligibility or reward
implementation from Luna-3.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_predictive_coding.py` | Windows PowerShell, Python 3.10.8; no random state required | Pass, 12 tests | Focused Luna-3 suite |
| `python -m pytest -q` | Windows PowerShell, Python 3.10.8; existing deterministic seed 17 tests | Pass, 39 tests | Full available regression suite |
| `python --version; git rev-parse --short HEAD; git status --short` | `main`, base `53ae36d`, uncommitted worktree | Python 3.10.8; expected uncommitted Luna work present | Reproduction metadata |
| VS Code file diagnostics | Current workspace | No errors in predictive module, tests, or package export | Focused diagnostics |

The focused tests cover prediction creation, deterministic identity, local
neuron sourcing, queued prediction emission, delayed matching, signed error
computation, explicit error events, positive-delay topology propagation,
unmatched/duplicate observations, expiry, unresolved bounded state,
simultaneous predictions, equal-time matching, irregular local time, queue
compatibility, neuron compatibility, and topology compatibility. No seeded
randomness is used by Luna-3; deterministic identity is tested directly and
the existing seeded runtime/topology regression tests remain passing.

## Benchmark and resource results

No dataset, classification metric, energy unit, utility formula, connectivity
utilization benchmark, or hardware measurement applies to this local component.
The declared resource result is the finite `max_outstanding` prediction
capacity plus the existing finite queue/topology capacity. The first-milestone
streaming benchmark remains not run.

## Assumptions, limitations, and unresolved issues

Scalar prediction and observation payloads are the minimal reference contract.
The target key is intentionally explicit so downstream roles can define their
own local target namespaces without a global prediction registry. Queue or
topology backpressure raises the established capacity exception; callers must
retry according to the Luna-1/Luna-4 policy. No architecture decision remains
unresolved for this assignment.

## Reproduction and rollback

From the repository root, run:

```text
python -m pytest -q tests/test_predictive_coding.py
python -m pytest -q
```

The result is uncommitted on `main`, based on `53ae36d`. Removing the three
Luna-3 implementation/export/test additions and this handoff restores this
assignment while preserving the unrelated existing Luna-2 and Luna-4 worktree
changes.

## Next assignment

Luna-5, Luna-7, and Luna-8 may consume the exposed local prediction/error
records within their own policies. Luna-11 must independently verify the full
acceptance matrix, including energy, delayed credit, streaming classification,
and integration readiness. This handoff does not declare the broader milestone
integration-ready.