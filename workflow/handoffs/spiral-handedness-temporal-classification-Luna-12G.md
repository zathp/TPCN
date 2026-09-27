# Luna-12G Dispatch Handoff

```yaml
tpcn_handoff:
  agent: Luna-12G Spiral Handedness Temporal Classification Benchmark
  task_id: "spiral-handedness-temporal-classification-luna-12g"
  component: "synthetic temporal spiral generator, controls, and benchmark diagnostics"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "d605e5da6c728390abb5916029903133b6e0fbd8"
  result_revision: "uncommitted"
  architecture_invariants_touched: [A01, A02, A03, A04, A06, A07, A08, A09, A10, A11, A14, A15]
  preserves:
    - "label-free neural computation and bounded external Luna-12F readout"
    - "persistent bounded topology and causal event routing from Luna-12E"
    - "Luna-13 and Luna-14 independence"
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/spiral_benchmark.py"
    - "tpcn/experiments.py"
    - "tpcn/__init__.py"
    - "tests/test_spiral_benchmark.py"
    - "run_spiral_benchmark.py"
    - "workflow/docs/luna/LUNA_12G_SPIRAL_HANDEDNESS_BENCHMARK.md"
    - "workflow/handoffs/spiral-handedness-temporal-classification-Luna-12G.md"
    - "artifacts/spiral-handedness-12g/"
  tests_added:
    - "tests/test_spiral_benchmark.py: 6 focused generator/control tests"
  tests_passing:
    - "python -m pytest -q tests/test_spiral_benchmark.py: 6 passed"
    - "python -m pytest -q tests/test_experiments.py tests/test_spiral_benchmark.py: 18 passed"
    - "python -m pytest -q: 158 passed, 1 skipped"
    - "python -m compileall -q tpcn tests run_spiral_benchmark.py"
    - "git diff --check"
  tests_failed: []
  tests_not_run:
    - "GPU/FPGA/ModelSim, real-dataset, and hardware acceptance"
    - "real-dataset, GPU/FPGA/ModelSim, and hardware acceptance"
  assumptions:
    - "Luna-12F corrected readout and label-isolation evidence is accepted by this authorization"
    - "the existing Luna-12E event-routing path is the benchmark execution path"
  unresolved:
    - "The current external readout and scalar event feature do not show order dependence; this is evidence about this runner, not a claim that temporal classification is solved."
  recommended_next_agent:
    - "Luna-0 Architecture Guardian for evidence review"
```

## Authorization decision

Luna-12F is accepted sufficiently for this dependency: its handoff records the
corrected bounded readout, both-class acquisition, label isolation, same-seed
determinism, fixed/structural/no-learning comparisons, full regression, and
the observed A/Z shortcut limitation. Luna-0 therefore authorizes 12G.

## Outcome and owned scope

`tpcn/spiral_benchmark.py` adds deterministic `spiral-left` and
`spiral-right` center-outward generation, class-neutral IDs, metadata and
sequence digests, stream-separated train/evaluation seeds, matched pairs,
shuffle/reversal transforms, nuisance variants, and the bounded external
Luna-12F control runner. `run_spiral_benchmark.py` writes `config.json`,
`benchmark.json`, and `summary.json` under
`artifacts/spiral-handedness-12g/`. The only shared runner change derives
character and reward boundaries from the final point timestamp, preserving
causal non-unit timing.

The exact reference formula is `r = radial_growth * t / duration`,
`theta = angular_speed * 2*pi*t / duration + rotation`,
`x = offset_x + scale * (r*cos(theta))`, and
`y = offset_y + handedness * scale * (r*sin(theta))`, with rotation applied
before translation and mild seeded perturbations after the first point.
Positive y and increasing theta define `spiral-left` as handedness `+1` and
`spiral-right` as `-1`.

## Benchmark results

Configuration: 32 examples/class for train and evaluation, 20 epochs, seeds
12007 and 12017, 12-20 points, 240-320 time units, and the bounds recorded in
the benchmark specification. Train and evaluation sequence digests are
disjoint; class-neutral derived IDs are also disjoint. The full control
summary is machine-readable in `artifacts/spiral-handedness-12g/summary.json`.

| Control | Accuracy | Left | Right | Connections | Mutations |
|---|---:|---:|---:|---:|---:|
| no-learning | 0.0000 | 0.0000 | 0.0000 | 1 | 0 |
| fixed-topology + learning | 0.53125 | 0.46875 | 0.59375 | 1 | 0 |
| structural-plasticity + learning | 0.53125 | 0.46875 | 0.59375 | 7 | 325 decisions, 12 additions, 8 prunes |
| shuffled temporal order | 0.53125 | 0.46875 | 0.59375 | 1 | 0 |
| time reversal | 0.53125 | 0.46875 | 0.59375 | 1 | 0 |
| rotated held-out | 0.49219 | see artifact | see artifact | 1 | 0 |
| scale/translation | 0.48438 | see artifact | see artifact | 1 | 0 |
| mild noise | 0.53125 | see artifact | see artifact | 1 | 0 |

The matched-pair control scored 0.5000 and the same-class nuisance pair scored
0.5000 on the two-example diagnostic. Prediction loss was 0.0 in this runner;
fixed utility was -353.6535 and structural utility was -367.0408. Structural
plasticity made 325 bounded mutation decisions, accepted 12 additions and 8
prunes, and ended with 7 connections; it did not improve classification.

## Interpretation and limitations

The benchmark is balanced, deterministic, split-disjoint, label-isolated, and
not perfect under no-learning. However, shuffled order and reversal exactly
match ordered evaluation, so this implementation provides no evidence that
the current scalar event/readout path uses temporal order. The likely shortcut
is order-invariant accumulated activity (`x + y`) and the external prototype
distance, not label leakage: relabeling identical streams preserves event
trace, energy, and prediction loss. The benchmark should therefore be
classified as a valid diagnostic with an unresolved temporal-feature
limitation, not as evidence of learned spiral handedness.

No numeric accuracy threshold or architecture-readiness claim is made. Real
datasets and hardware paths remain outside this milestone.

## Reproduction and next assignment

From the repository root:

`python run_spiral_benchmark.py --output artifacts/spiral-handedness-12g --examples-per-class 32 --epochs 20`

The exact pre-edit revision is `d605e5da6c728390abb5916029903133b6e0fbd8`;
unrelated pre-existing workflow changes were preserved. Return control to
Luna-0 for acceptance review, with the temporal-order limitation explicitly
carried forward.

## Owned scope and constraints

Implement the benchmark specification in
`workflow/docs/luna/LUNA_12G_SPIRAL_HANDEDNESS_BENCHMARK.md`. Use disjoint
deterministic train/evaluation streams, class-symmetric nuisance sampling,
center-outward matched spirals, and all required controls. Keep labels out of
neural events and all core state. Do not modify the architecture contract or
create an ACP.

## Required evidence

Record exact commands, revision, environment, seeds, parameter ranges,
split/example digests, metadata, timing units, readout configuration, and
all required metrics. Separate no-learning, fixed-topology, and structural
plasticity results. Explain shuffled-order and time-reversal semantics before
interpreting their results. Report poor, neutral, or harmful outcomes as
valid evidence; do not use 1.0 as a success criterion.

## Completion gate

The handoff must show disjoint data, class-symmetric nuisances, no shortcut
from start/sign/path length/sample count, label isolation, deterministic
replay, bounded resources, both-class diagnostics, all controls, and passing
applicable regression/compile/diagnostic checks. Return the completed handoff
to Luna-0 for acceptance review. This dispatch does not authorize 12G
promotion to a core architecture requirement or any hardware milestone.