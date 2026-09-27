# Luna-12C - Human-Interpretable 3D Temporal Visualization

## Status and authority

Luna-12C is authorized by Luna-0 on 2026-09-27 as an observational,
replay-first milestone. It is a downstream visualization facility, not a
change to the TPCN architecture. No ACP is required.

The milestone is a sibling of Luna-12A and Luna-12B after Luna-12. It may
consume their existing CPU replay artifacts, including structural mutation
history, but it must not become a prerequisite for Luna-13 or Luna-14.

## Purpose

Provide an interactive 3D view in which a human can inspect stable neuron
identity and position, activation and state, directed connections, topology
changes, snapshot metrics, and the relationship between structure and
behavior during recorded learning.

The primary entry point is replay of an existing TPCV artifact, for example:

```text
python <3d-viewer>.py artifacts/cpu-tpcv-12b
```

The exact filename and optional `Main.py viz3d` forwarding command are owned
by Luna-12C implementation work and must follow the current repository layout.

## Recommended graphics stack

Adapt the existing Python `pygame` + `PyOpenGL` implementation, using NumPy
for packed neuron and edge buffers. The repository already contains a
pygame/OpenGL 3D viewer with camera and text-overlay patterns, while the
older GLFW implementation is coupled to simulation objects and CuPy. The
12C viewer should reuse the useful interaction/rendering patterns without
importing either legacy simulation or signal-copy computation.

The renderer owns its window, camera, buffers, selection state, filters, and
playback state. It does not own or mutate TPCN computation state.

## Required viewer behavior

- Use canonical coordinates when supplied. Otherwise derive a deterministic
  diagnostic 3D layout from stable neuron IDs and recorded topology.
- Keep positions stable between snapshots unless recorded model coordinates
  change. Mark diagnostic coordinates as visualization-only.
- Render neurons with separate encodings for activity/state magnitude and use
  available event counts, energy, or utility as distinct visual channels or
  inspection fields rather than overloading one color.
- Render persistent directed edges, active edges when evidence exists, added
  edges, and recently pruned edges from replay history. Added-edge emphasis
  expires after a configurable snapshot count; rejected mutations remain
  diagnostics and are never rendered as edges.
- Support active-neuron, changed-edge, utilization-threshold, selected
  neighborhood, graph-depth, new/pruned-edge, high-energy, and high-utility
  filters where the artifact contains the required fields.
- Provide deterministic camera placement plus orbit, pan, zoom, reset, and
  fit-to-network controls.
- Provide play, pause, forward/backward step, first/last snapshot, direct
  snapshot selection, and configurable playback speed.
- Permit neuron selection and show legitimate recorded fields: ID, state,
  activation, processed events, fan-in/out, topology changes, and available
  metrics. Labels and hidden training inputs are not neuron state.
- Show synchronized snapshot/epoch, accuracy, prediction loss, reward,
  energy, utility, active-neuron fraction, active-edge count, additions,
  removals, and rejected mutations when present.
- Use packed/batched drawing and culling rather than one heavyweight GUI
  object per neuron or edge. Keep a path open for later run/seed comparison.

Snapshot-level activity may be shown as node and edge intensity. Event pulses
or moving propagation must not be synthesized from snapshot order.

## TPCV-1 limitation

TPCV-1 records contain timestamp, epoch, stable IDs, optional 2D position,
state, activation, processed-event count, and directed edges. The CPU replay
manifest adds metrics and mutation history. The current artifacts do not
provide canonical 3D coordinates, event-by-event propagation timing,
per-edge traffic, or per-neuron energy/utility fields. Luna-12C must therefore
use deterministic diagnostic 3D coordinates and snapshot-level playback;
actual propagation animation is deferred unless a future version records it.
The viewer must display unavailable fields as unavailable, never as fabricated
values.

## Non-interference contract

Loading, parsing, layout, rendering, selection, filtering, playback timing,
window events, dropped frames, and a disconnected or slow viewer must not
affect event ordering, timestamps, queues, routing, topology or structural
plasticity decisions, reward, utility, classifier behavior, training,
reproducibility, or recorded computation. Replay is read-only and the
renderer is not part of the TPCN architecture.

## Completion gate

Luna-12C passes when bounded existing TPCV replay loads; stable 3D neurons and
directed edges render; topology additions/removals are distinguishable;
playback and deterministic navigation work; neuron inspection and dense-graph
filters work; synchronized metrics are visible; repeated replay produces the
same layout and view state; focused viewer tests and relevant regression tests
pass; and capture/rendering-on versus off behavior remains unchanged.

The handoff must record unsupported fields, artifact fixtures, controls,
filter semantics, deterministic-layout algorithm, commands, tests, and all
checks not run. Visual evidence supplements, but does not replace,
downstream-only and non-interference evidence.