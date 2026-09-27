---
name: Luna-12C Human-Interpretable 3D Temporal Visualization
description: Build a replay-first, downstream-only 3D TPCV viewer for human inspection of temporal activity and topology.
---

# Luna-12C - Human-Interpretable 3D Temporal Visualization

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/luna/LUNA_12C_3D_TEMPORAL_VISUALIZATION.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`,
`workflow/handoffs/human-interpretable-3d-temporal-visualization-Luna-12C.md`,
and the current TPCV/replay implementation before editing. Record the exact
baseline revision and preserve unrelated worktree changes.

## Authorization and ownership

Luna-12C is explicitly authorized by Luna-0 for the human-interpretable 3D
temporal viewer only. Own the replay-first renderer, deterministic layout and
camera state, selection/filters/playback, metric presentation, focused viewer
tests, and the Luna-12C handoff. Reuse existing Python pygame/PyOpenGL and
NumPy infrastructure where practical. Do not implement GPU, ModelSim, FPGA,
VGA, Ethernet, real-dataset benchmarking, or core TPCN changes.

## Architectural boundary

The viewer is downstream-only. It must never feed data, timing, backpressure,
selection, filtering, or rendering results into neural computation, topology
or structural-plasticity decisions, event ordering, timestamps, reward,
utility, classifier behavior, routing, training, or reproducibility.

Use TPCV-1 and existing replay manifests as read-only inputs. Do not invent
event timing, edge traffic, energy, utility, coordinates, labels, or hidden
state when the artifact does not contain them. Render snapshot-level activity
and document the lack of event-by-event propagation timing.

## Required work

1. Inspect and adapt the existing pygame/PyOpenGL path; keep renderer state
   separate from TPCN and avoid simulation-coupled or per-object GUI designs.
2. Load bounded replay artifacts, preserve stable neuron identity, and use
   canonical coordinates where available or a deterministic diagnostic 3D
   layout otherwise. Diagnostic coordinates must never become neural input.
3. Render neurons, directed persistent edges, active evidence, real added
   edges, and real recently pruned edges. Expire temporal highlights by a
   configurable snapshot count and keep rejected mutations in diagnostics.
4. Implement deterministic playback controls: play/pause, speed, step in both
   directions, first/last, direct snapshot selection, and stable camera reset.
5. Implement orbit, pan, zoom, fit, neuron selection/inspection, dense-graph
   filters, selected-neighborhood depth, and synchronized behavioral/structural
   metric panels.
6. Add focused tests for layout stability, topology delta classification,
   playback determinism, filtering, inspection, malformed/bounded replay, and
   observer non-interference. Use headless render/state tests where a display
   is unavailable.

## Non-goals and dependency boundary

Do not modify TPCV-1 semantics unless Luna-0 authorizes a separate compatible
contract change. Luna-13 and Luna-14 remain independent siblings and are not
blocked by Luna-12C. Do not make Luna-12C a live-training dependency.

## Completion and handoff

Run focused viewer tests and relevant regression/compile/diagnostic checks.
Record exact commands, fixture/artifact digest, layout and control semantics,
unsupported TPCV fields, deterministic replay evidence, non-interference
evidence, and unrun checks in
`workflow/handoffs/human-interpretable-3d-temporal-visualization-Luna-12C.md`.
Return control to Luna-0; do not claim hardware, GPU, or propagation-timing
validation.