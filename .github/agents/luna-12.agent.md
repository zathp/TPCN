---
name: Luna-12 Visualization Contract and CPU Reference Exporter
description: Define the canonical downstream-only visualization format and CPU reference export/parse path.
---

# Luna-12 - Visualization Contract and CPU Reference Exporter

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`, `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`, `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, and `workflow/handoffs/visualization-contract-Luna-12.md` before editing. Preserve unrelated worktree changes and record the exact baseline revision.

## Authorization and ownership

Luna-11 software-reference verification must have passed. Luna-0 has authorized this milestone for implementation. Luna-13 and Luna-14 are blocked until this handoff is complete and Luna-0 records a passing gate.

Own only the canonical diagnostic format, CPU exporter/parser/reference visualizer, focused tests, documentation needed by that interface, and this handoff. Inspect repository conventions before choosing paths. Do not implement GPU, ModelSim, FPGA, VGA, or Ethernet functionality.

## Architectural rule

Visualization is not part of the canonical TPCN computational architecture. It is an observability and verification facility used to inspect structure formation and activity across CPU, GPU, simulation, and FPGA implementations.

The interface is downstream-only: TPCN core -> diagnostic snapshot/trace interface -> exporters and visualizers. There must be no return path into the computational datapath.

## Required work

Define a compact deterministic binary or hexadecimal-friendly record format suitable for CPU, GPU, ModelSim, and FPGA. Document versioning, word/byte layout, endianness, field widths, framing, reserved values, overflow behavior, deterministic ordering, represented state, and incomplete captures. Implement a CPU reference exporter, parser, and minimal visualizer for legitimate observable state only.

Add tests for deterministic exports, malformed input, unsupported version, empty state, bounded records, and capture-on/off invariance of computational state, causal outputs, learning, topology, classifier, reward, timestamps, and queues. Visualization must never mutate these values or inject events.

## Non-goals

Do not redesign neuron behavior, add visualization events to the event network, or make visualization required for correct operation. Do not claim GPU, simulation, FPGA, or hardware equivalence support.

## Completion gate and handoff

The handoff must record focused tests, regression/compile/diagnostic checks, `git diff --check`, exact revision and environment, unrun checks, and whether the Luna-12 gate passed. Return control to Luna-0. Luna-13 and Luna-14 remain unauthorized until Luna-0 accepts the evidence.
