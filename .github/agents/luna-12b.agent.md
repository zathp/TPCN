---
name: Luna-12B Persistent Topology and Structural Plasticity Visualization Integration
description: Integrate persistent bounded topology and validated structural plasticity into the CPU TPCV-1 path with structure-function observability.
---

# Luna-12B - Persistent Topology and Structural Plasticity Visualization Integration

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`, `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`, `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, `workflow/handoffs/cpu-training-visualization-Luna-12A.md`, `workflow/handoffs/experimental-learning-evaluation-Luna-9.md`, and `workflow/handoffs/structural-plasticity-Luna-10.md` before editing. Record the exact baseline revision and preserve unrelated worktree changes.

## Authorization and ownership

Luna-12A passed its stated completion gate on the deterministic Luna-9 synthetic path. Luna-0 explicitly authorizes this CPU integration milestone only. Own the persistent-topology experiment integration, structural-plasticity metrics, TPCV replay/inspection additions, focused tests, and `workflow/handoffs/persistent-topology-structural-plasticity-Luna-12B.md`. Do not select or benchmark a real dataset. Luna-13 and Luna-14 remain independently authorized and are not dependencies of this work; Luna-15, Luna-16, and Luna-17 are not authorized by this dispatch.

## Architectural boundary

Use one existing public Luna-4 bounded topology and the validated Luna-10 structural-plasticity API. Do not create a second topology model or visualization-only mutation mechanism. Structural adaptation remains experimental A14 behavior and must preserve A01-A15:

- no global neural clock or execution-batch timestep;
- causal finite propagation and routing;
- bounded fan-in, fan-out, state, routing, candidate storage, and mutation history;
- local/causal mutation evidence and label isolation;
- predictive/error, energy, reward, and utility semantics unchanged;
- no spatial-reservoir dependency;
- hardware-neutral reference behavior.

TPCV remains downstream-only. Capture, serialization, replay, rendering, storage limits, viewer timing, and dropped records must not approve or trigger mutations, alter event ordering/routing/reward/classifier/training, or create computational backpressure.

## Required work

1. Retain one bounded topology across the declared examples and epochs. Define reset and persistence scope explicitly.
2. Integrate the existing Luna-10 controller without changing Luna-4/Luna-10 contracts. Expose candidate additions, accepted additions, removals, rejected mutations and reasons, active connections, fan-in/out utilization, and bounded mutation history.
3. Add activity and behavior diagnostics: active-neuron count and fractions, receiving/emitting coverage, never-activated fraction, events, activations, connection utilization, prediction loss, accuracy, reward, energy, utility, and mutation count where available.
4. Add matched fixed-topology learning, structural-plasticity, and supported no/reduced-learning controls. Report beneficial and harmful results without assuming plasticity improves behavior.
5. Extend TPCV replay so actual added, unchanged, and recently removed connections can be distinguished where replay history permits, alongside active/inactive neurons, epoch/snapshot indices, and structural/behavioral metrics.
6. Add a repository-convention CLI equivalent to `python <runner>.py --epochs 20 --structural-plasticity --snapshot-every 1`, with a clear summary of starting/ending connections, additions, removals, rejected mutations, active-neuron fraction, prediction loss, accuracy, reward, energy, and utility before/after.
7. Add inertness reporting based on measured topology, prediction, classification, reward, utility, event, and activation metrics. Zero mutations alone are not a failure.
8. Add deterministic and non-interference tests: same-seed mutation sequence/final topology/snapshots/results, capture-on/off equivalence, bounded admission/pruning/routing, and no observer backpressure.

## Non-goals

Do not implement a real-dataset benchmark, GPU or ModelSim/FPGA path, hardware equivalence, new core architecture, new topology abstraction, unrestricted global learning, label-fed mutation evidence, or any Luna-15/Luna-16/Luna-17 work. Do not weaken or silently amend the contract. An ACP is not needed for a compatible integration; route any incompatible API or architecture request to Luna-0.

## Completion gate and handoff

Record exact commands, environment, seeds, workload/configuration, topology limits, mutation rules, metric definitions and units, comparison results, replay evidence, boundedness/non-interference results, compile/diagnostic/regression checks, and unrun checks in `workflow/handoffs/persistent-topology-structural-plasticity-Luna-12B.md` using the handoff template. Explicitly classify observed topology/behavior combinations: unchanged/unchanged, unchanged/improved, changed/unchanged, changed/improved, and changed/degraded where present. Return control to Luna-0; do not claim integration readiness without the required evidence.
