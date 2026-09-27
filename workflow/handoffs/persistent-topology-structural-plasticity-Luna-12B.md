# Luna-12B Completion Handoff

```yaml
tpcn_handoff:
  agent: Luna-12B Persistent Topology and Structural Plasticity Visualization Integration
  task_id: "persistent-topology-structural-plasticity-luna-12b"
  component: "persistent bounded CPU topology, Luna-10 structural plasticity, and TPCV observability"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "acc2a8ac20ace2a4cd9088acebcaf91e959b540f"
  result_revision: "uncommitted"
  architecture_invariants_touched: [A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, A11, A14, A15]
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/experiments.py"
    - "tpcn/cpu_visualization.py"
    - "tpcn/visualization.py"
    - "train_cpu_visualization.py"
    - "tests/test_luna12b_integration.py"
    - "workflow/handoffs/persistent-topology-structural-plasticity-Luna-12B.md"
  tests_passing:
    - "Focused Luna-12B plus Luna-9/Luna-10/Luna-12 suites: 41 passed"
    - "Full pytest: 134 passed, 1 skipped"
    - "compileall, diagnostics, and git diff --check: passed"
  tests_failed: []
  tests_not_run:
    - "Real dataset, GPU, ModelSim/FPGA, FPAA, and hardware equivalence: not authorized"
  unresolved:
    - "Synthetic results do not establish real-dataset generalization."
    - "Temporal mutation/behavior correlation is not causal proof."
  recommended_next_agent:
    - "Luna-0 Architecture Guardian"
```

## Outcome and owned scope

`ExperimentRunner` now creates one deterministic `BoundedTopology` per declared
workload and retains it across examples and epochs. `StructuralPlasticityController`
is the only mutation path. Candidate evidence contains source-local activity and
prediction-error magnitude; labels and reward are not mutation inputs. Atomic
Luna-10 replacement topologies are refreshed by the runner after growth/pruning.

Per-epoch metrics include activity coverage, never-activated fraction, events,
activations, prediction loss, accuracy, reward, energy, utility, connection
counts/capacity, fan-in/out utilization, additions, prunings, rejection count,
bounded mutation history, and actual topology edges. TPCV snapshots receive the
actual topology at the epoch boundary. Replay adds a derived timeline of
unchanged, added, and recently-pruned endpoints and makes no mutation decisions.

The smoke command is:

```text
python train_cpu_visualization.py --epochs 20 --seed 7 --examples-per-class 1 --snapshot-every 1 --structural-plasticity --output-dir artifacts/cpu-tpcv-12b
python train_cpu_visualization.py --replay artifacts/cpu-tpcv-12b
```

The 20-epoch run reported starting/ending connections `1/1`, additions `8`,
removals `8`, rejected mutations `20`, active-neuron fraction `1.0`, prediction
loss `0.0840410359053751` before and after, accuracy `1.0 -> 0.5`, reward `2.0 ->
0.0`, energy `4.401482863923839` before and after, and utility `-2.401482863923839
-> -4.401482863923839`.

## Architecture evidence

- **A01-A03:** Existing canonical event processing is unchanged; topology mutation
does not add a neural clock or inline routing. Pruning changes future routing
only and preserves already queued events.
- **A04/A08:** Fan-in/out, edge capacity, candidate capacity, and mutation history
are finite. Atomic admission and pruning preserve valid routing.
- **A05:** No spatial reservoir or coordinate dependency was introduced.
- **A06-A07/A11:** Prediction loss and local activity are observable signals;
labels/reward remain external and are not candidate evidence. Predictive/error
and delayed-credit semantics are unchanged.
- **A09-A10:** Energy remains `activity-cost-proxy`; utility remains the net
formula `reward - energy_weight * energy`. Inactivity is not success.
- **A14:** This remains experimental bounded structural plasticity through the
validated Luna-10 API, not a promoted core invariant.
- **A15:** The implementation remains a deterministic hardware-neutral reference.

## Validation record

| Command or procedure | Environment / seed | Result |
|---|---|---|
| `python -m pytest -q tests/test_luna12b_integration.py tests/test_experiments.py tests/test_structural_plasticity.py tests/test_cpu_visualization.py tests/test_visualization.py` | Windows PowerShell; seeds 2, 3, 5, 7 | 41 passed |
| `python -m pytest -q` | Current worktree | 134 passed, 1 skipped |
| `python -m compileall -q tpcn tests train_cpu_visualization.py` | Current worktree | Passed |
| Workspace diagnostics | Touched implementation and tests | No errors |
| `git diff --check` | Current worktree | Passed; existing workflow line-ending warning only |
| 20-epoch structural CLI smoke | Seed 7, one A/Z example each, snapshot every epoch | 20 snapshots, 8 additions, 8 removals, 20 rejections |
| Capture off/on comparison | Seed 3, four epochs, structural mode | Equal `TrainingResult`; deterministic replay |

## Benchmark and resource results

The only workload is the authorized deterministic synthetic A/Z stream: one or
two examples per class, three timestamped points per example. Energy is measured
in activity-cost-proxy units, not calibrated joules. Utility uses the net formula
with energy weight `1.0`. Defaults are fan-in 2, fan-out 2, edge capacity 8,
initial edge count 1, candidate capacity 16, maximum growth 1 per epoch, and
mutation history limit 32.

Matched four-epoch controls with seed 7 and one example per class:

| Mode | Accuracy before/after | Prediction loss before/after | Reward before/after | Utility before/after | Ending connections |
|---|---|---|---|---|---|
| Fixed topology, learning enabled | 1.0 / 0.5 | 0.0840410359053751 / 0.0840410359053751 | 2.0 / 0.0 | -2.401482863923839 / -4.401482863923839 | 1 |
| Structural plasticity, learning enabled | 1.0 / 0.5 | 0.0840410359053751 / 0.0840410359053751 | 2.0 / 0.0 | -2.401482863923839 / -4.401482863923839 | 1 |
| Structural plasticity disabled, learning disabled | 1.0 / 1.0 | 0.0840410359053751 / 0.0840410359053751 | 2.0 / 2.0 | -2.401482863923839 / -2.401482863923839 | 1 |

Topology changed in the structural run, but this workload showed no behavioral
improvement. The descriptive result is **changed/degraded** relative to its
before/after behavior; fixed topology also degraded, so mutation is not claimed
as the cause. The replay timeline showed real unchanged, prune, and add edges.
The recorded local signals were `local_activity_prediction_error` and
`local_activity_retention`; correlation is not treated as causation.

The network was behaviorally active, not inert: every tested neuron received
events and emitted activity, and the 20-epoch run made 16 accepted mutations.
Topology, candidate storage, and history remained bounded. Capture did not
approve or inject mutations.

Observed categories include unchanged/unchanged, unchanged/degraded,
changed/unchanged, and changed/degraded. Changed/improved and unchanged/improved
were not observed. No emergent-intelligence or useful-self-organization claim is
made.

## Reproduction and rollback

Run the smoke command above, then replay the saved directory. The implementation
is uncommitted; restore only the Luna-12B-owned implementation/test/handoff files
if rollback is authorized, preserving the pre-existing workflow edits.

## Next assignment

Return control to Luna-0 Architecture Guardian. Luna-12B passes its software
integration and observability gate subject to Luna-0 review. Real data, GPU,
FPGA/ModelSim, hardware equivalence, and broader causal usefulness studies remain
outside this authorization.
