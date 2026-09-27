---
name: Luna-10 Structural Plasticity and Topology Adaptation
description: Implement and verify bounded, local, deterministic topology adaptation through the validated event-routing topology.
---

# Luna-10 - Structural Plasticity and Topology Adaptation

You own the structural plasticity layer above the validated Luna-1 through
Luna-4 topology and Luna-5 through Luna-8 integration. Read the authoritative
contract, acceptance criteria, workflow, handoff template, Luna-11 verification
handoff, Luna-4 topology handoff, and this dispatch handoff before editing.

## Baseline and ownership

- Baseline revision: `af5575c0a629f101486bf36d930218eecdef77b` plus the current
  validated uncommitted worktree.
- Owned implementation paths: `tpcn/structural_plasticity.py` and
  `tests/test_structural_plasticity.py`; owned handoff:
  `workflow/handoffs/structural-plasticity-Luna-10.md`.
- Do not edit `tpcn/topology.py`, Luna-9 experiment/metrics files, Luna-11
  evidence, or foundational runtime/neuron/classifier modules. Use only the
  public `BoundedTopology` API. Route any incompatible API requirement to
  Luna-0 and Luna-4 rather than changing the owner’s module.

## Objective

Implement a finite structural-plasticity controller with explicit local
candidate evidence, deterministic tie-breaking, finite growth and shrinkage,
fan-in/fan-out and edge-capacity checks, and an inspectable bounded topology
state. Edge creation/removal must be legal through the public topology
interface and must preserve routing metadata and causal event semantics.

Define deterministic behavior for rejected candidates, duplicate candidates,
full capacity, pruning, and in-flight events. No hidden global optimization,
all-to-all search, arbitrary non-local connectivity, unbounded history, wall-
clock learning, label input, or global timestep is permitted. Structural
plasticity is an experimental A14 layer and must not be promoted to a core
invariant; no ACP is needed unless an implementation request would change the
contract or a public foundational API.

## Required validation and handoff

Add focused tests for locality, capacity, fan-in/out, deterministic candidate
selection, growth, pruning, finite propagation, finite connectivity, bounded
topology state, replay equality, and stable routing semantics. Record exact
commands, seed, environment, and not-run checks. The completion handoff must
include the required structural-plasticity API, mutation rules, locality,
bounds, selection, growth/pruning, finite propagation/connectivity, replay,
bounded-topology, focused-test, regression, compilation, diagnostics, and
`git diff --check` results.

Do not start the real dataset benchmark, hardware acceptance, or joint
integration review. Return control to Luna-0 when complete.
