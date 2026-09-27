---
name: Luna-14 ModelSim FPGA Trace Bridge and DE1-SoC Visualization Foundation
description: Bridge the canonical visualization format into simulation and downstream DE1-SoC diagnostic infrastructure.
---

# Luna-14 - ModelSim/FPGA Trace Bridge and DE1-SoC Visualization Foundation

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`, `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`, `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, and `workflow/handoffs/visualization-fpga-Luna-14.md` before editing. Preserve unrelated worktree changes and record the exact baseline revision.

## Authorization and ownership

Luna-12 must have a passing handoff and Luna-0 must explicitly authorize Luna-14. Luna-13 is an optional parity reference, not a prerequisite. Own only the ModelSim/RTL trace adapter, downstream FPGA diagnostic interface, DE1-SoC visualization foundation, focused tests, relevant documentation, and this handoff.

## Architectural rule

Visualization is not part of the canonical TPCN computational architecture. It is an observability and verification facility used to inspect structure formation and activity across CPU, GPU, simulation, and FPGA implementations. The branch is downstream-only and has no return path into the TPCN computational datapath.

## Required work

Use Luna-12's canonical format. Implement deterministic ModelSim-compatible hex/binary framing and ordering; define HDL X/Z/unknown handling, reset and snapshot boundaries; and decode known topology/activity traces with reference tooling. Define a downstream-only FPGA diagnostic snapshot/stream for the Terasic DE1-SoC. Diagnostic overflow may drop records rather than stall computation; expose loss/overflow status where practical. Prefer VGA as the first local display foundation. Keep Ethernet as a planned richer host path and do not add a full stack unless reusable infrastructure already exists.

Verify that removing visualization leaves TPCN behavior unchanged, visualization reset is independent of core reset unless board-wide reset intentionally couples them, and visualization backpressure never becomes computational backpressure. Do not modify topology, classifier, reward, or core reset semantics.

## Non-goals

Do not redefine the format, inject events, implement a full Ethernet stack solely for this milestone, or claim hardware equivalence.

## Completion gate and handoff

Record trace-decoding, malformed/truncated/unknown-value, reset-boundary, non-blocking overflow, downstream-only, regression/compile/diagnostic, and `git diff --check` evidence. Mark hardware checks not run when unavailable. Return control to Luna-0; later hardware implementation remains separately gated.
