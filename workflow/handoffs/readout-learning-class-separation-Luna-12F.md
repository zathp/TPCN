# Luna-12F Completion Handoff

```yaml
tpcn_handoff:
  agent: Luna-12F Readout Learning and Class-Separation Verification
  task_id: "readout-learning-class-separation-luna-12f"
  component: "bounded external supervised readout and class-separation diagnostics"
  status: "complete-pending-Luna-0-review"
  contract_version: "1.0"
  baseline_revision: "09c19914ea9a1f06a10acb35390e613a9d4bcef9"
  result_revision: "uncommitted"
  architecture_change: false
  proposal: null
  preserves:
    - "Luna-12E persistent bounded topology and causal event routing"
    - "labels outside canonical events, neuron/predictor state, routing, topology evidence, and energy"
    - "Luna-13 and Luna-14 independence"
  files_changed:
    - "tpcn/experiments.py"
    - "tests/test_experiments.py"
    - "tests/test_temporal_analysis.py"
    - "workflow/handoffs/readout-learning-class-separation-Luna-12F.md"
```

## Result

Class starvation was confirmed for the old production path. The deterministic
one-example A/Z fixture first predicts A correctly and creates A. The next Z
example is selected as A by the learned readout, receives reward `-1.0`, and
the old `if update and learning_enabled and reward > 0.0` gate skips Z forever.
The old final state is therefore A-only and the larger artifact collapses to
A with accuracy `0.5`.

The correction removes positive-reward gating from supervised class acquisition.
During training, the label-free network feature is computed, prediction and
reward are recorded, and the labeled class's bounded `(feature_sum, count)`
state is updated. The centroid is `feature_sum / count`; no examples are
retained. `max_classes` is enforced and state is deterministic/resettable.
Reward still evaluates correctness, affects utility, and is delivered to the
existing eligibility ledger. It is no longer the sole condition for creating
external readout state.

## Minimal fixture evidence

With `seed=7`, one example per class, `correct_reward=0.0`, and one epoch:

| Example | Feature | Raw | Final | Reward | Updated | State after example |
|---|---:|---|---|---:|---|---|
| A-0 | `-1.1614219752914758` | A | A | `0.0` | yes | A centroid `-1.1614219752914758`, count 1 |
| Z-0 | `0.7380859272481534` | Z | A | `-1.0` | yes | A and Z, count 1 each |

The Z feature is distinct from A, but the first readout decision is wrong
because only A exists. The corrected path records the negative reward and
still acquires Z. In the normal reward fixture, A and Z features remain
separable and the final corrected readout selects both classes.

## Diagnostics and isolation

`ReadoutDiagnostic` is emitted per example and included in each bounded epoch
metric and final evaluation. It contains the network feature, external label,
raw/final prediction, reward, update decision, representations, every available
class distance, nearest class, winning and runner-up distances, margin, and
confidence. Aggregate metrics now include per-class accuracy, confusion,
represented/missing classes, prototype count, starvation count, and mean margin.

The regression test relabels identical inputs and compares canonical event
traces, routed topology contents, and event fields. They remain identical;
labels affect only external readout learning and evaluation. The same-seed
prototype and diagnostic test is deterministic. Visualization capture remains
downstream-only; the CPU capture path only serializes metrics after execution.

## A/Z results

For 20 epochs, seed 7, five examples per class:

| Mode | Accuracy | Per-class accuracy | Confusion | Loss | Confidence | Margin | Reward | Energy | Utility | Connections | Updates |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fixed + learning | 1.0 | A 1.0, Z 1.0 | A->A 5, Z->Z 5 | 0.093480 | 0.942466 | 1.484455 | 10 | 23.304455 | -13.304455 | 1 | 200 |
| Structural + learning | 1.0 | A 1.0, Z 1.0 | A->A 5, Z->Z 5 | 0.143936 | 0.852536 | 1.809995 | 10 | 31.121331 | -21.121331 | 7 | 200 |
| Fixed + no learning | 1.0 | A 1.0, Z 1.0 | A->A 5, Z->Z 5 | 0.093480 | 0.064922 | 0.000000 | 10 | 23.304455 | -13.304455 | 1 | 0 |

Both centroids are different (`A=-1.1614219752914758`,
`Z=0.7380859272481534` in the minimal fixture), with no decision overlap in
the tested synthetic workload. The corrected classifier chooses both classes;
the previous all-A result was readout starvation, not a collapsed neural
feature in this fixture. Structural plasticity changes computation and costs,
but has no measurable final classification benefit over fixed topology here.

The required smoke artifacts are:

- `artifacts/cpu-tpcv-12f`: 30 snapshots, 5 examples/class, structural mode,
  accuracy before/after `1.0/1.0`, 8 additions, 8 removals, 7 final edges.
- `artifacts/cpu-tpcv-12f-large`: 50 snapshots, 16 examples/class, structural
  mode, accuracy before/after `1.0/1.0`, 8 additions, 8 removals, 7 final edges.

TPCV-1 still does not encode per-edge event-path counts, so edge-use frequency
is unavailable in replay analysis. Direct Luna-12E causal tests remain the
evidence that reachable topology changes affect computation.

## Validation

Passed:

- `python -m pytest -q tests/test_experiments.py` -> 12 passed.
- Combined Luna-12F/Luna-12E/classifier/reward/structural/visualization slice -> 69 passed.
- `python -m pytest -q` -> 152 passed, 1 skipped.
- `python -m compileall -q tpcn tests train_cpu_visualization.py` -> passed.
- Workspace diagnostics for `tpcn/experiments.py` and `tests/test_experiments.py` -> no errors.
- `git diff --check` -> passed; existing workflow line-ending warning only.
- Required 30-epoch and preferred 50-epoch structural smoke commands -> passed.

Not run or outside authorization: real datasets, GPU/FPGA/ModelSim/FPAA,
hardware acceptance, and Luna-15/Luna-16/Luna-17. Return control to Luna-0;
this handoff does not claim architecture-wide or hardware readiness.
