# Luna-12C Completion Handoff

```yaml
tpcn_handoff:
  agent: Luna-12C Human-Interpretable 3D Temporal Visualization
  task_id: "human-interpretable-3d-temporal-visualization-luna-12c"
  component: "replay-first deterministic 3D TPCV viewer"
  status: partial
  contract_version: "1.0"
  branch: main
  base_revision: "1d6dbde3795d57d9cee83a7085843b411105e525"
  result_revision: uncommitted
  architecture_invariants_touched: [A01, A03, A04, A07, A08, A15]
  architecture_change: false
  proposal: null
  tests_added:
    - "tests/test_viewer_3d.py"
  tests_passing:
    - "focused viewer tests: 3 passed"
    - "TPCV, CPU replay, and Luna-12B tests: 20 passed"
    - "compileall: passed"
    - "headless replay CLI and Main.py forwarding: passed"
    - "git diff --check: passed with existing workflow line-ending warning"
  tests_failed:
    - "full pytest collection: unrelated missing tpcn.signal_copy_distance in test_gpu_visualization.py"
  tests_not_run:
    - "interactive graphics smoke: no display/OpenGL context available"
    - "GPU, ModelSim/FPGA, real-dataset, and hardware validation: outside Luna-12C"
```

## Outcome

`VisualizationScene` is a detached, headless-testable renderer model. It loads
`ReplaySequence` read-only, derives stable Fibonacci-sphere diagnostic 3D
coordinates when canonical 2D positions are absent, and exposes nodes, directed
edges, real added/pruned highlights, bounded history, snapshot diffs, metrics,
inspection, bounded neighborhoods, filters, playback, and camera state.

`viz_tpcn_3d.py` adds the lazy pygame/PyOpenGL shell with node/line rendering, a
visible metric/control HUD, direct numbered selection, and `--inspect-only`.
`Main.py viz3d -- ...` forwards to it. The old GLFW path was not reused because
it is coupled to simulation/CuPy objects.

## Semantics and limitations

Modes are overview, activity, structural, neighborhood, and utility when the
recorded metrics contain energy or utility. Rejected mutations remain metric
diagnostics and are never rendered as edges. TPCV-1 lacks event-by-event
propagation timing, per-edge traffic, canonical 3D coordinates, and per-neuron
energy/utility, so the viewer shows snapshot-level activity and diagnostic
coordinates honestly; it does not synthesize propagation pulses.

The tested Luna-12B fixture contains 20 snapshots and a two-neuron synthetic
network. Repeated same-seed scene construction produced identical replay
digests and coordinates. Loading, filtering, selection, and rendering do not
write artifacts or feed back into training, topology, timing, or computation.

## Reproduction

```text
python train_cpu_visualization.py --epochs 20 --seed 7 --examples-per-class 1 --snapshot-every 1 --structural-plasticity --output-dir artifacts/cpu-tpcv-12b
python viz_tpcn_3d.py artifacts/cpu-tpcv-12b --inspect-only
python viz_tpcn_3d.py artifacts/cpu-tpcv-12b
```

The implementation is ready for Luna-0 review. Full-suite status remains
partial because the unrelated GPU test import is broken in this worktree and
an interactive graphics context was unavailable.