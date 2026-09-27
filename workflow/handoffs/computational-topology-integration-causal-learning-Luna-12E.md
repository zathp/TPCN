# Luna-12E Dispatch Handoff

```yaml
tpcn_handoff:
  agent: Luna-12E Computational Topology Integration and Causal Learning Verification
  task_id: "computational-topology-integration-causal-learning-luna-12e"
  component: "persistent topology event-routing integration and causal verification"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "0f0e75d"
  result_revision: "uncommitted"
  architecture_invariants_touched: [A01, A02, A03, A04, A06, A07, A08, A09, A10, A11, A14, A15]
  preserves:
    - "finite bounded topology and causal event propagation"
    - "local predictive/error, credit, and energy semantics"
    - "Luna-13 and Luna-14 independence"
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/canonical_neuron.py"
    - "tpcn/experiments.py"
    - "tests/test_experiments.py"
    - "tests/test_luna12e_integration.py"
    - "tests/test_temporal_analysis.py"
  tests_added:
    - "tests/test_luna12e_integration.py: 5 causal integration tests"
  tests_passing:
    - "Luna-12E, experiment, and Luna-12B integration slice: 17 passed"
    - "combined Luna-12E and owning runtime/topology/plasticity/predictive/neuron/CPU regressions: 72 passed"
    - "python -m compileall -q tpcn tests train_cpu_visualization.py"
    - "Workspace diagnostics for owned files: no errors"
    - "git diff --check"
  tests_failed: []
  tests_not_run:
    - "full pytest after this integration: not run"
    - "real-dataset, GPU, ModelSim/FPGA, and hardware acceptance: not authorized"
  assumptions:
    - "12D must establish what topology and activity evidence the current path exposes"
  unresolved:
    - "full-workspace collection remains subject to pre-existing unrelated suite coverage"
  recommended_next_agent:
    - "Luna-0 Architecture Guardian after Luna-12D completion"
```

## Blocking decision

Luna-12D is complete and approved by Luna-0. Implementation remains limited to
the declared milestone scope: make the persistent bounded topology the actual
event-routing network, then test reachable-edge additions and removals with
matched controls.

## Required evidence after authorization

Show shared topology ownership, causal event propagation, downstream activity
changes after reachable-edge interventions, prediction/error metrics derived
from propagated activity, functional metric responses under a relevant
workload, boundedness, deterministic replay, and downstream-only analysis.

## Implementation evidence

`ExperimentRunner` now owns one persistent `_ComputationalNetwork` per workload.
The network creates one stable `TPCNNeuron` per topology node, injects input at
the declared source node, and processes a bounded `EventQueue`. Each delivered
event is handled by its destination neuron; that activation is then emitted
from the receiving neuron and routed through the same `BoundedTopology`.
Structural-plasticity replacement topologies are installed into this network
immediately after adaptation, so growth and pruning affect subsequent routing
without a second graph.

Event lineages carry bounded internal path bookkeeping. A lineage may traverse
each node at most once, preventing cyclic structural mutations from violating
local monotonic time or exceeding the finite event budget. Propagation remains
queued and delayed; pending events are not retroactively removed by pruning.

Neurons persist by identity across points, strokes, and epochs, while neural
state, local clocks, energy counters, eligibility state, and pending per-input
queues reset at each character boundary. Topology and mutation state persist
across the full runner workload. Labels remain external to events, neurons,
topology evidence, and predictive state.

Prediction and readout consume routed activations. The causal fixture uses a
two-example A/Z workload with zero initial edges: adding `neuron-0 ->
neuron-1` adds delayed downstream events, increases processed activity, and
changes prediction loss. Removing the edge eliminates future delivery. A
separate A -> B -> C fixture verifies cumulative finite delay.

## Validation record

Environment: Windows PowerShell, Python 3.10.8, baseline revision
`0f0e75df6e69bd924f0be4692425613da9dda596`, current dirty worktree. Causal
fixtures use deterministic inputs and no real dataset.

| Check | Result |
|---|---|
| no path, edge addition, pruning, propagation delay, in-flight pruning | passed |
| multi-hop A -> B -> C routing | passed |
| experiment routed activity and prediction-loss intervention | passed |
| persistent identity and character reset policy | passed |
| same focused tests repeated with Luna-9/Luna-12B integration | 17 passed |
| owning runtime/topology/plasticity/predictive/neuron/CPU regressions | 55 passed |
| deterministic replay and capture non-interference controls | passed in Luna-12B slice |
| compileall, diagnostics, diff check | passed |
| real dataset, GPU, FPGA/ModelSim, hardware equivalence | not run; outside authorization |

The result establishes functional topology causation for the controlled
software-reference workload. It does not claim improved benchmark accuracy,
real-dataset generalization, hardware behavior, or core promotion. Luna-0
Architecture Guardian review remains required.

## Post-implementation verification

Verification baseline: `0b81f5fdd2ce632ecdd87cdb8a3baa3725f068d6`, Windows
PowerShell, Python 3.10.8, dirty worktree containing the pre-existing
untracked `artifacts/cpu-tpcv-12e/` directory. No architecture contract or
implementation code was changed during verification. The stale 12D temporal
analysis expectation that prediction loss remain flat was updated in
`tests/test_temporal_analysis.py` after the integrated routing path correctly
made loss vary.

Exact smoke command:

```text
python train_cpu_visualization.py --epochs 20 --seed 7 --examples-per-class 1 --snapshot-every 1 --structural-plasticity --output-dir artifacts/cpu-tpcv-12e-verify
```

The run produced 20 snapshots with digest
`5b27a2ab5ec07f3963ebc8f51664efe843948ec8aa25d76f7a6ccd04fe24e6d3`.
Starting/ending connections were `1/1`; accepted additions/removals were
`8/8`; rejected mutations were `20`, all recorded as duplicate proposals.
Two unique edges appeared, one persisted and one was transient. TPCV-1 does
not encode per-edge exercise counters or event paths, so artifact-level
exercised-versus-unused counts are unavailable. Direct routed event traces
and the causal tests prove that added edges were exercised.

The smoke timeline showed prediction loss varying during training in the
structural run (`0.1312365340324925`, `0.18658415897657313`, and
`0.13938866084945573` recurring), while the final evaluation loss was
`0.1312365340324925`. Accuracy was `1.0 -> 0.5`; reward `2.0 -> 0.0`; energy
`5.698523707618888 -> 5.698523707618888`; utility
`-3.6985237076188877 -> -5.698523707618888`; active-neuron fraction was `0.5`
at the final evaluation. Added edges coincided with the next pass increasing
activity from 9 to 12 events and activating both neurons; pruning then reduced
the next pass to 9 events. The topology plateaued as persistent two-edge churn,
with 20 duplicate rejections and no fan-in, fan-out, capacity, nonlocal,
candidate-capacity, invalid, or no-valid-candidate rejections.

Matched 20-epoch controls used seed 7, one A/Z example per class, and the
same synthetic workload. Fixed topology plus learning ended at accuracy 0.5,
loss `0.1312365340324925`, reward 0.0, energy `5.698523707618888`, utility
`-5.698523707618888`, and one connection. Structural plasticity plus learning
had the same final functional metrics but changed intermediate loss, energy,
utility, active-neuron count, and event count. Structural plasticity plus no
learning preserved accuracy 1.0 and reward 2.0, with the same topology churn.
Therefore structural plasticity had no measurable final functional benefit
under this workload; it exposed a causal activity/loss response but did not
improve the task result.

Capture-disabled and capture-enabled structural runs were identical in
training result, replay digest, and mutation sequence; the enabled run saved
20 snapshots. The focused Luna-12E/runtime/topology/predictive/structural/
experiment slice passed 56 tests. The Luna-12B/12C/12D/12E and visualization
slice passed 34 tests. Full pytest passed `148` tests with `1` skip; compileall,
diagnostics, and `git diff --check` passed.

Verification answers: topology affects computation **YES**; added edges are
actually exercised **YES** in direct causal routing, although per-edge
artifact counters are unavailable; pruned edges stop affecting future routing
**YES**; prediction loss changes during training **YES** in the structural
run; accuracy changes over training **YES** (`1.0 -> 0.5`); topology plateaued
**YES**, due to repeated duplicate proposals combined with alternating
pruning/re-growth, not a hard capacity limit.
