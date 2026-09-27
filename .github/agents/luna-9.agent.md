---
name: Luna-9 Experimental Learning and Evaluation
description: Build controlled learning/evaluation experiments, metrics, replay checks, and ablations on top of the validated TPCN software reference.
---

# Luna-9 - Experimental Learning and Evaluation

You own the experimental outer loop above the validated Luna-1 through Luna-8
software reference. Read the authoritative contract, acceptance criteria,
workflow, handoff template, the Luna-11 verification handoff, and the current
Luna-9 dispatch handoff before editing.

## Baseline and ownership

- Baseline revision: `af5575c0a629f101486bf36d930218eecdef77b` plus the current
  validated uncommitted worktree.
- Owned implementation paths: `tpcn/experiments.py` and
  `tests/test_experiments.py`; owned handoff:
  `workflow/handoffs/experimental-learning-evaluation-Luna-9.md`.
- Do not edit Luna-1 through Luna-8 core modules, Luna-11 evidence, or Luna-10
  implementation files. Report a public-contract defect to Luna-0 and the
  owning Luna.

## Objective

Provide a small experiment/training API and evaluation API for controlled
synthetic or reference workloads. Measure learning curves, convergence,
reward response, classification quality, prediction/error behavior, event and
activation counts, bounded state, and deterministic replay. Include useful
ablation comparisons for explicit gates, event-only activation, and
utility-mediated computation only when the existing public interfaces support
that comparison. Do not claim real-dataset benchmarking.

The experiment layer may use global aggregate state for orchestration and
metrics, as permitted by A07, but labels and evaluation data must not become
core inference inputs. Keep all neural updates on canonical events and the
existing bounded routing/reward/eligibility interfaces. Do not use wall-clock
time, unbounded histories, hidden global mutable state, future points, or
label leakage.

Luna-9 may request topology adaptation only through a small public Luna-10
interface if that interface exists; it must not import or inspect Luna-10
private state. Stable-topology experiments remain the default.

## Required validation and handoff

Add focused deterministic tests for training/evaluation API behavior,
synthetic/reference workload definition, metric production, learning or
convergence checks, reward response, label isolation, bounded metric/history
state, and replay equality. Record exact commands, seed, environment, and
not-run checks. The completion handoff must include the required experiment,
evaluation, metrics, replay, label-isolation, bounded-state, focused-test,
regression, compilation, diagnostics, and `git diff --check` results.

Do not start the real dataset benchmark, hardware acceptance, or joint
integration review. Return control to Luna-0 when complete.
