# Luna agent handoff

```yaml
tpcn_handoff:
  agent: Luna-6 Sequential Stroke Dataset
  task_id: "sequential-stroke-dataset"
  component: "bounded causal sequential stroke event adapter and protocol"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "e2b8276"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A04", "A07", "A08", "A15"]
  preserves:
    - "Luna-1 Event and EventQueue timestamp, ordering, capacity, and delivery semantics."
    - "Luna-3 local prediction/error interfaces; no prediction or classifier policy was redefined."
    - "Labels, split metadata, classifier policy, energy, delayed credit, and hardware claims remain outside the reusable core."
    - "Legacy static-image and signal-copy implementations remain untouched."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/stroke_dataset.py"
    - "tpcn/__init__.py"
    - "tests/test_stroke_dataset.py"
    - "workflow/handoffs/sequential-stroke-dataset-Luna-6.md"
  tests_added:
    - "tests/test_stroke_dataset.py"
  tests_passing:
    - "python -m pytest -q tests/test_stroke_dataset.py: 6 passed"
    - "python -m pytest -q: 45 passed"
    - "python -m compileall -q tpcn tests: passed"
    - "git diff --check: passed"
  tests_failed: []
  tests_not_run:
    - "Actual sequential letter-stroke benchmark: no dataset is present or selected."
    - "Luna-11 acceptance matrix and post-END_CHARACTER classification: not implemented."
    - "Luna-5 local energy and reward-adjusted utility validation."
    - "Luna-8 delayed-credit and eligibility validation."
    - "FPGA, FPAA, hybrid, and hardware-equivalence validation."
  assumptions:
    - "The adapter accepts externally supplied native points and does not claim a dataset, version, license, class set, or split."
    - "Training normalization is fit only from caller-supplied training points; split enforcement belongs to the dataset runner."
    - "A declared synthetic interval is permitted only when native timestamps are absent."
  unresolved:
    - "Luna-0 must select the actual permitted dataset and version, native stroke representation, classes, and train/validation/test split."
    - "Writer-disjoint splitting remains unresolved until writer identity is known."
    - "Native timestamp availability and units remain unresolved; synthetic interval is explicitly configurable but not a benchmark decision."
    - "Luna-7 must define the external readout and post-END_CHARACTER classification policy."
    - "Luna-5 and Luna-8 must define reward, energy, eligibility, and error-boundary integration."
  recommended_next_agent:
    - "Luna-0: resolve dataset, split, licensing, class, and timing decisions before benchmark claims."
    - "Luna-7: consume the label-free stream and define external classification after END_CHARACTER."
    - "Luna-11: verify the complete acceptance matrix after dataset and downstream interfaces exist."
```

## Outcome and owned scope

Added `tpcn/stroke_dataset.py` with a hardware-neutral, bounded external stream
adapter. `StrokePoint` represents native point input. `StrokeStreamEncoder`
emits ordered `START_CHARACTER`, `STROKE_EVENT`, and `END_CHARACTER` runtime
events through Luna-1-compatible `Event` records. Stroke payloads contain only
current/past-derived `x`, `y`, `dx`, `dy`, `pen_state`, and `stroke_boundary`
features. Boundary payloads carry only a local sequence index.

`CausalNormalizer.fit_training()` creates fixed affine constants from explicitly
provided training points. Encoding uses those constants and the current point
plus the immediately previous point; it does not center, scale, or otherwise
inspect future points in the active character. Missing timestamps require an
explicit positive synthetic interval. A finite `max_points` rejects oversized
characters, and reset clears previous-point state so deltas cannot cross
character boundaries. `serialize_stream()` provides deterministic, label-free
replay data.

`LabeledCharacter` and `DatasetMetadata` are external records only. Labels and
split membership are not accepted by or inserted into stream event payloads.
No classifier, readout, reward, energy, credit, spatial reservoir, static-image
benchmark, or global timestep was added.

## Architecture evidence

- **A01-A03:** native timestamps are preserved in nondecreasing order; events
  are emitted in temporal order and remain queued `Event` records. Synthetic
  time is explicit and positive. The adapter does not introduce a global tick.
- **A04/A08:** character point count is bounded by `max_points`; encoded output
  is finite; reset prevents cross-character pending feature state.
- **A05:** no spatial reservoir or spatial computation is required.
- **A06:** event payloads are compatible with Luna-3 downstream prediction/error
  processing, but this adapter does not implement prediction policy.
- **A07:** only current/past points and training-fitted constants enter stroke
  features. Labels, test metadata, future points, and global evaluation state
  are absent from core events.
- **A09-A11:** boundaries are exposed for downstream activity/credit handling;
  energy, utility, reward, and delayed credit are not implemented.
- **A12-A13:** no pathway count or explicit gating assumption was added.
- **A14:** no structural plasticity was added.
- **A15:** fixed dataclasses, bounded buffers, deterministic ordering, and
  serialization provide a software reference suitable for later mapping; no
  hardware validation is claimed.

No Architecture Change Proposal is required. This is a compatible external
adapter implementation and does not amend A01-A15.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_stroke_dataset.py` | Windows PowerShell, Python 3.10.8; deterministic fixtures | Pass, 6 tests | Focused Luna-6 protocol suite |
| `python -m pytest -q` | Windows PowerShell, Python 3.10.8 | Pass, 45 tests | Full available repository regression |
| `python -m compileall -q tpcn tests` | Windows PowerShell, Python 3.10.8 | Pass | Package and test compilation |
| `git diff --check` | `main`, uncommitted | Pass | No whitespace errors |

Focused tests cover ordered START/stroke/END events, causal feature derivation,
label absence, bounded point capacity, declared synthetic timing, reset and
cross-character delta isolation, timestamp rejection, deterministic
serialization, and Luna-1 queue delivery/equal-time ordering.

## Benchmark and resource results

No actual dataset is present in this repository, so no dataset/version,
permitted-use statement, class count, split, writer-disjoint result, seed,
classification metric, prediction metric, event-count benchmark, energy proxy,
utility result, or hardware result is claimed. The implementation supports
caller-supplied `DatasetMetadata`, but does not populate it with invented
values. The declared adapter resource bound is `max_points` per character;
Luna-1 `EventQueue` capacity bounds pending delivery.

## Assumptions, limitations and unresolved issues

The adapter assumes points are supplied in native order and that any supplied
native timestamps use the same nonnegative local time units. The current
normalizer is a training-fitted affine transform over supplied point
coordinates and a bounded delta scale; the benchmark runner must fit it only
on the training split. Dataset split enforcement, licensing, class semantics,
writer identity, and native timing are not inferable from the current
repository and are returned to Luna-0 as open decisions.

The primary benchmark must classify only after `END_CHARACTER`; prefix
measurements, if later added, must be separately reported. Luna-3 prediction
and error events, Luna-5 energy, Luna-8 delayed credit, and Luna-7 readout
remain downstream responsibilities.

## Reproduction and rollback

From the repository root:

```text
python -m pytest -q tests/test_stroke_dataset.py
python -m pytest -q
python -m compileall -q tpcn tests
```

The result is uncommitted on `main`, based on `e2b8276`. Removing the stroke
adapter, its package exports, its focused tests, and this handoff restores the
Luna-6 changes without reverting unrelated worktree changes.

## Next assignment

Luna-0 should resolve the actual dataset/version, permitted use, classes,
native timing, and split before benchmark execution. Luna-7 may then build the
external classifier/readout against this label-free stream. Luna-11 should
independently verify streaming classification, prediction/error instrumentation,
reset/retention, bounded resources, and the remaining energy, credit, and
hardware gates. This handoff does not declare the broader integration milestone
ready.
