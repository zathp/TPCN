---
name: Luna-12G Spiral Handedness Temporal Classification Benchmark
description: Build and verify a harder synthetic temporal benchmark for left- and right-handed center-outward spiral classification.
---

# Luna-12G - Spiral Handedness Temporal Classification Benchmark

Read `workflow/ARCHITECTURE_CONTRACT.md`,
`workflow/ARCHITECTURE_CHANGELOG.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`,
`workflow/docs/luna/LUNA_12G_SPIRAL_HANDEDNESS_BENCHMARK.md`, and the accepted
`workflow/handoffs/readout-learning-class-separation-Luna-12F.md` before
editing. Record the exact baseline revision and preserve unrelated worktree
changes.

## Authorization and ownership

Luna-12G is authorized by Luna-0 after the accepted Luna-12F corrected
external-readout evidence. Own the synthetic generator, benchmark runner,
controls, focused tests, diagnostics, and
`workflow/handoffs/spiral-handedness-temporal-classification-Luna-12G.md`.
Do not select a real handwriting dataset or implement GPU, FPGA, ModelSim,
FPAA, or hardware acceptance work.

## Required benchmark

Generate two center-outward spiral classes with the same start, matched radius
schedule, sample count, duration, and path-length rules. Their primary class
signal is ordered handedness. Apply identical seeded nuisance distributions
for rotation, scale, translation, angular speed, bounded radial growth,
sampling timing, coordinate noise, and radial jitter. Use disjoint derived
train/evaluation streams and detect sequence/metadata reuse.

Run no-learning with external readout learning disabled, fixed-topology learning, structural-plasticity learning,
random point-order, defined time-reversal, same-class nuisance-pair, and
opposite-handed matched-pair controls. Do not impose a numeric accuracy
threshold. Investigate perfect no-learning results as possible leakage.

## Architectural boundary

Feed only ordered stroke/timing and legitimate boundary events to the neural
system. Keep labels external to canonical events, IDs, event types, predictor
state, routing, topology mutation evidence, structural-plasticity evidence,
energy, and prediction/error computation. Use the bounded Luna-12F readout
only after label-free neural processing. Do not introduce a global neural
timestep, future-point preprocessing, a spatial reservoir, or a second graph.

## Diagnostics and completion

Record per-example metadata and accuracy, per-class accuracy, confusion,
prediction loss, confidence, margin, reward, energy/proxy units, utility,
events, active-neuron fraction, connections/utilization, mutation counts, and
represented readout classes. Prove same-seed replay, label isolation, bounded
resources, split integrity, and applicable regression/compile/diagnostic
checks. Report whether fixed topology and structural plasticity improve,
match, or harm behavior. Return control to Luna-0; do not claim architectural
or hardware readiness.