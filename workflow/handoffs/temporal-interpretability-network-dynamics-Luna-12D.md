# Luna-12D Dispatch Handoff

```yaml
tpcn_handoff:
  agent: Luna-12D Temporal Interpretability and Network-Dynamics Analysis
  task_id: "temporal-interpretability-network-dynamics-luna-12d"
  component: "replay analysis, topology/activity dynamics, and plateau diagnosis"
  status: "complete-approved-by-Luna-0"
  contract_version: "1.0"
  branch: "main"
  base_revision: "0f0e75d"
  result_revision: "uncommitted"
  architecture_invariants_touched: [A01, A03, A04, A06, A07, A08, A09, A10, A11, A14, A15]
  preserves:
    - "downstream-only TPCV observation"
    - "current topology/computation coupling, as an observation to measure"
    - "Luna-13 and Luna-14 independence"
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/temporal_analysis.py"
    - "tpcn/structural_plasticity.py"
    - "tpcn/experiments.py"
    - "tpcn/cpu_visualization.py"
    - "tpcn/viewer_3d.py"
    - "tpcn/__init__.py"
    - "train_cpu_visualization.py"
    - "tests/test_temporal_analysis.py"
    - "workflow/handoffs/temporal-interpretability-network-dynamics-Luna-12D.md"
  tests_added:
    - "tests/test_temporal_analysis.py: 6 deterministic analysis tests"
  tests_passing:
    - "Luna-12D, Luna-12C, Luna-12B, Luna-12A, structural, visualization, and experiment suites: 50 passed"
    - "compileall: passed"
    - "workspace diagnostics for touched files: no errors"
    - "git diff --check: passed; existing workflow LF/CRLF warning only"
    - "20-epoch structural replay and replay comparison CLI: passed"
  tests_failed:
    - "Full pytest collection is blocked by pre-existing ModuleNotFoundError: tpcn.signal_copy_distance in tests/test_gpu_visualization.py"
  tests_not_run:
    - "Full pytest execution after collection error: not run"
    - "real-dataset, GPU, ModelSim/FPGA, and hardware acceptance: not authorized"
  assumptions:
    - "existing TPCV-1/replay artifacts are valid inputs for observational analysis"
    - "12C interactive graphics availability is not required for artifact analysis"
  unresolved:
    - "TPCV-1 still cannot identify event paths carried by individual edges"
    - "older artifacts without mutation_rejection_reasons expose only partial rejection evidence"
  recommended_next_agent:
    - "Luna-0 Architecture Guardian after 12D evidence review"
```

## Luna-0 review decision

- Decision: **Approved for completion as the Luna-12D observational milestone.**
- Review basis: focused temporal-analysis tests passed 6/6; compile and diff
  checks passed; the recorded 20-epoch replay is deterministic and reports
  activity, topology lifetimes/churn, precise duplicate rejection evidence,
  functional-metric flatness, and unavailable edge-use fields explicitly.
- Architecture result: no A01-A15 change and no ACP required. The analysis is
  downstream-only and does not claim topology causation.
- Conditions: per-edge exercise remains unavailable in TPCV-1; the duplicate
  rejection diagnosis is limited to the recorded run; 12E must establish
  actual event routing through the persistent topology and perform controlled
  reachable-edge causal checks.
- Next assignment: Luna-12E is unblocked for its separately scoped
  computational-topology integration and causal-verification work.

## Dispatch scope

Measure the current system as it exists. Produce human-readable and
machine-readable temporal summaries covering neuron activity, edge existence
versus exercise, additions/removals/rejections, lifetimes, utilization,
concentration, behavior correlations, and graph stabilization. Investigate the
connection plateau from precise rejection reasons. Do not repair computational
topology coupling and do not infer causation.

## Implementation and evidence

The downstream analyzer is `tpcn.temporal_analysis`. It exports per-snapshot
metrics, per-neuron activity/lifetime records, per-edge lifetime records,
addition/removal timelines, rejection counts, flat-metric ranges, descriptive
stability classification, and raw comparison deltas. `train_cpu_visualization.py`
now writes `analysis.json` beside each replay and supports `--compare` in replay
mode. The 3D viewer summary exposes the analysis classification and edge-use
availability without feeding analysis back into rendering or computation.

Mutation results preserve existing statuses and decisions while adding precise
diagnostic reasons where the current controller knows them. Epoch metrics now
serialize per-epoch rejection reason counts. No routing, learning, event order,
topology choice, reward, or TPCV-1 field semantics were changed.

Long replay command:

```text
python train_cpu_visualization.py --epochs 20 --seed 7 --examples-per-class 1 --snapshot-every 1 --structural-plasticity --output-dir artifacts/cpu-tpcv-12d
```

Artifact: `artifacts/cpu-tpcv-12d/analysis.json`; replay digest:
`cc8c38806182a320f7536874c16dc41e20b0aa67d10d900cebffa8ccfeb50230`.

Observed 20-epoch results:

- 2 neurons were always active; 0 remained permanently inactive; active-neuron fraction was 1.0 at every snapshot.
- 2 unique edges were observed; 1 persisted to the final snapshot and 1 was transient. Mean/median lifetime was 15 snapshots.
- Transition churn was 1.0: 9 observed additions and 10 removals; final graph size was 1.
- 35 growth attempts were recorded: 10 accepted and 25 duplicate rejections. Fan-in-full, fan-out-full, edge-capacity, nonlocal, candidate-capacity, invalid, and no-valid-candidate counts were all 0.
- The plateau mechanism supported by this run is repeated duplicate proposals combined with pruning/replacement, not hard fan-in/out or global edge capacity. The analyzer does not claim more than the recorded evidence.
- Accuracy was exactly 0.5, prediction loss 0.0840410359053751, reward 0.0, utility -4.401482863923839, and energy 4.401482863923839 for every captured training epoch. Functional metric response was not observed.
- Edge utilization is unavailable: TPCV-1 records edge existence and propagation delay, not per-edge event paths. Processed-event totals are not used to infer edge use.

The descriptive classification is **persistent churn / no functional response**.
This is a correlation-oriented observation only; it is not a causal topology
claim. No real dataset or hardware behavior was selected or benchmarked.

## Completion gate

Return exact commands, revision, artifacts, seeds, metrics, rejection reasons,
reproducibility evidence, unavailable fields, and passed/failed/not-run checks.
Luna-0 must review the evidence before Luna-12E can be authorized.
