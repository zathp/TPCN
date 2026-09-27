# Luna agent handoff

```yaml
tpcn_handoff:
  agent: Luna-7 Streaming Character Classification
  task_id: "streaming-classification"
  component: "bounded label-free streaming A-Z classifier readout"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "cab3025"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A07", "A08", "A15"]
  preserves:
    - "Canonical Luna-1 Event records and local timestamp/sequence semantics."
    - "Luna-5, Luna-6, and Luna-8 public contracts and the RewardMessage.to_reward_signal() boundary."
    - "Labels remain external metadata and do not enter inference or TPCN state."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-7.agent.md"
    - "tpcn/streaming_classifier.py"
    - "tpcn/__init__.py"
    - "tests/test_streaming_classifier.py"
    - "workflow/handoffs/streaming-classification-Luna-7.md"
  tests_added:
    - "tests/test_streaming_classifier.py"
  tests_passing:
    - "Focused Luna-7 suite: 12 passed"
    - "Full regression suite: 71 passed"
    - "python -m compileall -q tpcn tests: passed"
    - "git diff --check: passed"
    - "Editor diagnostics for touched Python files: no errors"
  tests_failed: []
  tests_not_run:
    - "Actual A-Z dataset benchmark and Luna-0 joint review: not run"
    - "Hardware and Luna-11 acceptance: not run"
  assumptions:
    - "The selected alphabet is A-Z; dataset selection remains a Luna-0 decision."
    - "Numeric Event payloads represent permitted upstream TPCN activity; labels are not an API input."
  unresolved:
    - "No dataset/version/split has been selected, so no accuracy claim is made."
  recommended_next_agent:
    - "Luna-0: run the planned Luna-5/Luna-6/Luna-7/Luna-8 joint integration review."
```

## Outcome and owned scope

Added `StreamingCharacterClassifier` as an external readout. It consumes
canonical `Event` records carrying the public `ACTIVITY_EVENT` numeric
activity type, exposes immutable `ClassEvidence`, and emits one immutable
`ClassificationResult` only from an active character's `END_CHARACTER`.
Authoritative results include all 26 scores and probabilities plus boundary
identity and timing. `START_CHARACTER` clears all character-local scores and
counters. `END_STROKE` returns non-authoritative evidence and never finalizes;
boundary and non-activity events are rejected outside their protocol. The 26
saturating score values, event counter, boundary metadata, and last result are
bounded persistent state; no event history is retained.

The public API is `ACTIVITY_EVENT`, `ingest_event`, `ingest_activity`, `evidence`,
`finalize_character`, `authoritative_result`, `is_active`, `activity_event_count`,
and `reset`. Final results preserve source, sequence, timestamps, character
index, and activity count. No label parameter or label-derived state exists.

### Temporal acceptance semantics

Rejected input is observationally atomic with respect to classifier temporal
state: protocol-invalid or out-of-order events cannot advance the committed
timestamp or character-local state. A later valid event behaves as though the
rejected event was never submitted. Every accepted transition that advances
causal time commits its timestamp once, including direct
`finalize_character()` calls. That timestamp is used by subsequent ordering
checks, while one accepted `END_CHARACTER` still emits exactly one result.

## Architecture evidence

- **A01-A03:** processing is event-driven, timestamps must be nondecreasing,
  and boundary/event identity is preserved without a global neural timestep.
- **A04/A08:** scores are fixed at 26 entries and activity is limited by
  `max_activity_events`; overflow uses explicit backpressure.
- **A05:** no spatial reservoir or private neuron/topology access is required.
- **A07:** inference consumes only supplied public activity events; external
  labels are absent from the API and regression trajectories are identical.
- **A15:** immutable dataclasses and bounded Python reference state keep the
  semantics suitable for later hardware mapping; no hardware equivalence is
  claimed.

No ACP is required: this is a compatible external readout and does not amend
the architecture contract.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_streaming_classifier.py` | Windows PowerShell, deterministic fixtures | Pass, 12 tests | Focused Luna-7 suite |
| `python -m pytest -q` | Windows PowerShell, deterministic fixtures | Pass, 71 tests | Full repository regression |
| `python -m compileall -q tpcn tests` | Windows PowerShell | Pass | Package and test compilation |
| `git diff --check` | `main`, uncommitted | Pass | No whitespace errors |
| Editor diagnostics | Touched Python files | No errors found | `streaming_classifier.py`, package export, focused tests |

The focused tests cover exact class count, pre-boundary suppression,
`END_STROKE`, one-result finalization, consecutive-character reset,
empty-character behavior, deterministic replay, bounded streams,
label-independent inference, side-effect-free evidence, and event identity.

## Benchmark and resource results

No dataset, version, split, classification accuracy, prediction metric, energy
proxy, utility result, connectivity utilization, or hardware result is claimed.
The classifier's declared bounds are 26 scores and `max_activity_events` per
character; upstream event queues remain separately bounded.

## Assumptions, limitations and unresolved issues

The classifier is a deterministic external reference readout, not a trained
alphabet benchmark model. Dataset class confirmation, training/evaluation
policy, prediction/error instrumentation, reward/eligibility integration, and
benchmark configuration remain open to Luna-0. Malformed boundary behavior is
explicitly rejected rather than silently producing a result.

## Reproduction and rollback

From the repository root:

```text
python -m pytest -q tests/test_streaming_classifier.py
python -m pytest -q
python -m compileall -q tpcn tests
git diff --check
```

The result is uncommitted on `main`, based on `cab3025`, and can be removed by
reverting only the five files listed above while preserving unrelated worktree
changes.

## Next assignment

Luna-0 should complete the full validation record and conduct the planned
Luna-5/Luna-6/Luna-7/Luna-8 joint integration review. Luna-7 does not authorize
Luna-11, hardware acceptance, or later phases.