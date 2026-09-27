# Luna-13 Dispatch Handoff

```yaml
tpcn_handoff:
  agent: Luna-13 GPU-Compatible Visualization Path
  task_id: visualization-gpu-luna-13
  component: GPU adapter for the Luna-12 visualization format
  status: partial
  authorization: Luna-0 explicitly authorized after Luna-12 PASSED
  contract_version: "1.0"
  branch: main
  base_revision: 884887ec25d74edfef48ca67ee0653d6fed679d0
  result_revision: uncommitted
  architecture_invariants_touched: [A01, A03, A04, A07, A08, A15]
  preserves:
    - Luna-12 canonical record compatibility
    - downstream-only observation and CPU computational behavior
    - event ordering, propagation, topology, reward, classifier, and bounded state
  architecture_change: false
  proposal: null
  files_changed:
    - tpcn/signal_copy_distance/gpu_visualization.py
    - tpcn/signal_copy_distance/__init__.py
    - tests/test_gpu_visualization.py
    - workflow/docs/luna/VISUALIZATION_CONTRACT.md
    - workflow/handoffs/visualization-gpu-Luna-13.md
  tests_added:
    - tests/test_gpu_visualization.py: canonical round-trip, CPU/CUDA parity, capture invariance, and periodic capture
  tests_passing:
    - focused GPU visualization suite: 3 passed, 1 skipped because CUDA is unavailable
  tests_failed: []
  tests_not_run:
    - CUDA parity execution: CUDA is unavailable in the installed `torch 1.12.1+cpu` environment
    - actual CUDA parity execution: unavailable in this environment
  assumptions:
    - Luna-12 passed and Luna-0 authorized Luna-13 before implementation.
    - The signal-copy model's recurrent structural mask is its observable bounded topology.
  unresolved:
    - Actual CUDA parity remains unrun until a CUDA-enabled PyTorch environment is available.
  recommended_next_agent: [Luna-0 after Luna-13 gate evidence]
```

## Dispatch status

Luna-13 is authorized by the Luna-0 visualization review after the Luna-12
gate passed. Implementation remains outside this Luna-0 review.

## Outcome and design

`TorchSnapshotExporter` is a downstream adapter for canonical TPCV-1. It
samples at a positive epoch interval, detaches the selected hidden-state row
and structural mask, copies those tensors to host, and calls the Luna-12
record/export path. There is no device-side schema, callback into the model,
persistent execution state, queue interaction, or synchronization dependency
for computation.

The correctness-first implementation uses a synchronous host transfer rather
than double buffering or compact device records. Capture cost is one transfer
and serialization per selected snapshot. Missing signal-copy observables
default to `0` processed events and `1.0` propagation delay and are not claimed
as native GPU semantics. Labels, rewards, queues, gradients, and optimizer
state are unsupported.

## Architecture evidence

- A01/A03: capture records existing timestamp/epoch and does not create or
  route events.
- A04/A08: structural edges and bounded canonical record limits are reused;
  malformed or oversized exports are rejected by Luna-12.
- A07: no labels, rewards, or hidden global state are captured implicitly.
- A15: the PyTorch adapter is device-neutral and consumes CPU TPCV-1 records.

## Validation record

| Command or procedure | Revision / environment | Observed result |
|---|---|---|
| Baseline | `884887ec25d74edfef48ca67ee0653d6fed679d0`, Windows PowerShell, Python 3.10.8, existing dirty worktree preserved | recorded |
| `python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"` | same environment | `torch 1.12.1+cpu`; CUDA unavailable |
| `python -m pytest -q tests/test_gpu_visualization.py` | same environment | 3 passed, 1 skipped |
| CUDA parity test | CUDA runtime/device | not run; unavailable |
| `python -m pytest -q` | current worktree | 126 passed, 1 skipped |
| `python -m compileall -q tpcn tests` | current worktree | passed |
| `git diff --check` | current worktree | passed |
| workspace diagnostics for touched files | current editor environment | no errors in adapter/test; unrelated existing `pytest` import diagnostic remains in `tests/test_luna11_adversarial.py` |

## Performance and compatibility

The focused test run took approximately 0.95 seconds including pytest
startup, not a model performance benchmark. Transfer synchronization is
limited to a requested capture and cannot backpressure computation because
the adapter has no execution queue or callback path. Records are consumed by
`parse_snapshot` and `ReferenceVisualizer` without GPU-specific parser logic.

## Gate result

The available Luna-13 software gate passes. Full CUDA execution parity remains
unverified until the skipped test is run in a CUDA-enabled environment. Luna-14
remains separately authorized and was not started by this work.

## Required completion evidence

Record CPU/GPU semantic parity through the Luna-12 parser, capture-on/off invariance, synchronization/performance implications, exact commands and environment, and all unrun checks using the handoff template. Do not implement or authorize ModelSim, FPGA, VGA, or Ethernet work.
