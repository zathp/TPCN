---
name: Luna-12A CPU Training Visualization Integration
description: Integrate deterministic CPU training with downstream-only TPCV-1 capture, replay, and inspection.
---

# Luna-12A - CPU Training Visualization Integration

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`, `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`, `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, `workflow/handoffs/visualization-contract-Luna-12.md`, `workflow/handoffs/experimental-learning-evaluation-Luna-9.md`, and `workflow/handoffs/structural-plasticity-Luna-10.md` before editing. Preserve unrelated worktree changes and record the exact baseline revision.

## Authorization and ownership

Luna-12 passed and Luna-0 explicitly authorized this CPU integration milestone. Own only the CPU training/demo integration, TPCV-1 snapshot capture/storage/replay, minimal inspection path, focused tests, and this handoff. Use the existing Luna-9 deterministic synthetic training/evaluation path. Do not select or benchmark a real dataset. Luna-13 and Luna-14 are separate authorized branches and are not dependencies of this work.

## Architectural rule

Visualization is downstream-only and non-semantic:

```text
TPCN training -> TPCV-1 snapshot capture -> bounded storage/parser -> replay/viewer
```

Capture, serialization, replay, rendering, storage limits, viewer timing, and dropped/incomplete records must never influence event ordering, neuron updates, predictions, reward, eligibility, classifier behavior, topology decisions, queue behavior, timestamps, or training results. Do not introduce a global neural timestep, computational backpressure, visualization events, or a return path into the TPCN datapath.

## Required work

1. Add a configurable CPU runner/demo for deterministic synthetic training, epoch count, and snapshot interval, following repository conventions.
2. Capture bounded TPCV-1 snapshots containing legitimate observable identity, activity/state, connections, epoch/snapshot metadata, and available prediction loss, reward, energy, utility, and accuracy metrics.
3. Store and replay snapshots after training without requiring the original training process. Make malformed, missing, unsupported, incomplete, and over-limit data fail clearly.
4. Provide a lightweight viewer or deterministic replay/export path that lets a user inspect activity/state and connectivity over time.
5. Add non-interference tests comparing visualization disabled, every-epoch capture, and more frequent capture. Compare predictions, metrics, replay digest, update/parameter counts, topology where applicable, reward/utility state, and final network state.
6. Add deterministic snapshot-sequence and parser/replay tests, including bounded snapshot storage.

## Luna-10 structural plasticity boundary

Fixed topology is the valid default. Use Luna-10 only if the existing public API is stable, no architecture change is required, and bounded topology invariants remain enforced by focused tests. If those conditions are not met, defer structural-plasticity visualization and record that it is deferred; do not redesign topology or core interfaces.

## Non-goals

Do not modify TPCV-1 semantics, redesign the event-driven core, authorize real-data benchmarking, implement GPU or ModelSim/FPGA visualization, or claim hardware equivalence. Do not make the viewer required for correct training.

## Completion gate and handoff

Record exact commands, environment, seed, synthetic workload/configuration, snapshot bounds, parser/replay evidence, non-interference results, structural-plasticity included/deferred status, regression/compile results, and unrun checks in `workflow/handoffs/cpu-training-visualization-Luna-12A.md` using the handoff template. Return control to Luna-0. The next task after a passing handoff is a Luna-0 evidence review; Luna-13 and Luna-14 remain independently authorized and do not wait for Luna-12A.
