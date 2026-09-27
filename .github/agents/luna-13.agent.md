---
name: Luna-13 GPU-Compatible Visualization Path
description: Produce semantically compatible GPU visualization records using the Luna-12 format.
---

# Luna-13 - GPU-Compatible Visualization Path

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`, `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`, `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, and `workflow/handoffs/visualization-gpu-Luna-13.md` before editing. Preserve unrelated worktree changes and record the exact baseline revision.

## Authorization and ownership

Luna-12 must have a passing handoff and Luna-0 must explicitly authorize Luna-13. The prompt and handoff do not authorize implementation by themselves. Own only the GPU exporter/adapters, focused parity and invariance tests, relevant documentation, and this handoff.

## Architectural rule

Visualization is not part of the canonical TPCN computational architecture. It is an observability and verification facility used to inspect structure formation and activity across CPU, GPU, simulation, and FPGA implementations. The path is downstream-only and has no return path into the TPCN computational datapath.

## Required work

Use the Luna-12 schema without creating a GPU-specific schema. Implement GPU snapshot/export support and choose structured device buffers, periodic capture, double buffering, or host transfer as appropriate. Ensure records are consumed by the Luna-12 parser/visualizer. Document synchronization and performance implications without making performance part of the architecture contract.

Add CPU/GPU semantic parity tests with declared numeric tolerances and visualization-on/off invariance tests. Capture must not alter neuron updates, event ordering, propagation, topology, reward, classifier, bounded state, timestamps, or queue behavior, and GPU synchronization must not become a computational dependency.

## Non-goals

Do not implement ModelSim, FPGA, VGA, or Ethernet visualization. Do not modify core computation or claim hardware equivalence.

## Completion gate and handoff

Record focused parity/invariance tests, regression/compile/diagnostic checks, `git diff --check`, exact revision and environment, unsupported fields, overhead, and unrun checks. Return control to Luna-0. Luna-14 remains separately gated by Luna-12 and is not implicitly authorized by this work.
