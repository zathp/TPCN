---
name: Luna-25 ACP-0006 Sequential Dataset Evidence Reproducibility
description: Retain and execute a deterministic UCI Character Trajectories evaluation for the ACP-0006 CPU integration gate.
---

# Luna-25 — ACP-0006 Sequential Dataset Evidence Reproducibility

## Authorization and baseline

Luna-25 is authorized for **DATASET-ADAPTER IMPLEMENTATION + BENCHMARK
VERIFICATION** only, starting from
`1642b991f82403140d0f29b5a2ff10b3d2628cda` on `main`. This assignment is
created after Luna-0 independently closes Luna-24. It addresses the retained
loader/split/per-class evidence gap only; it does not close Luna-22.

Read accepted ACP-0006, the Luna-22 implementation and completion handoff,
the Luna-0 second review, and the Luna-0 independent Luna-24 review before
execution. Record branch, exact revision and worktree state.

## Objective

Produce a repository-reproducible, label-isolated, sequential
UCI Character Trajectories CPU evaluation using the integrated
`EXCURSION_V1` path. Preserve the loader, exact source/version identity,
split recipe, stable example IDs, invocation, metrics and outputs needed for
an independent rerun.

First investigate whether the previously reported 160-example split can be
reconstructed from retained evidence. If its exact record membership or
loader cannot be proven, do **not** claim to reproduce the old run. Instead,
define and version a deterministic replacement split in the task handoff and
label its results as a new benchmark baseline.

## Bounded ownership

Own only:

- a new standalone dataset benchmark/loader under `scripts/`;
- focused deterministic parser/split tests under `tests/`;
- a machine-readable run manifest and per-class report under
  `artifacts/luna-25-uci-character-trajectories/`, excluding raw dataset data;
- `workflow/handoffs/luna-25-uci-character-trajectories-20261003.md`.

Do not modify reusable core, closed components, experiment semantics,
visualization, research consumers, or any existing handoff other than this
authorization's completion reference if governance asks for it.

## Required data protocol

- Use the public UCI Character Trajectories dataset identified by DOI
  `10.24432/C58G7V`; record the retrieved source filename/version, retrieval
  details and SHA-256 of the input artifact. Do not commit raw dataset data.
- Verify and report the actual number of usable examples and classes; do not
  assume the handoff's reported 2,858 examples/20 classes without checking.
- The prior handoff describes an 8-example-per-class subset (4 train, 2
  validation, 2 test) over 20 classes, seed `20261003`. Attempt exact
  reconstruction only if retained evidence identifies membership and
  preprocessing. Otherwise call any new deterministic split `luna25-v1`,
  report that it is not the old split, and specify a stable stratified
  selection/split recipe and sample manifest. The recipe must not depend on
  unspecified Python or library RNG behavior.
- Preserve temporal order within each trajectory. Use the documented
  current-point scalar `x_velocity + y_velocity` only if validated against
  the source schema. Do not normalize from whole-character/future values or
  enqueue unseen points.
- Feed labels only to outer train/evaluation orchestration at the ACP-0006
  boundary. Demonstrate that labels and future points are absent from neural
  event inputs.
- Record all configuration, logical time units, event/queue/settling limits,
  seed/split manifest, class mapping, and exact reproduction command.

## Required measurements and checks

Report train/validation/test sizes and per-class counts, per-class accuracy,
confusion matrix, overall classification metrics, prediction targets/matches/
errors, delayed-credit outcomes, events/emissions/silence, queue and topology
utilization, settling completion, energy-component totals and proxy units.
State that proxy units are not joules and do not invent an accuracy threshold.
If the run is incomplete, report it as incomplete.

Run the same declared split twice from fresh state and compare stable outputs
or traces. Add focused tests for source parsing, stable split membership,
class coverage, temporal ordering and label isolation. Run the focused tests
and the ACP-0006 prescribed regression set; report the known unrelated full
suite failures without repairing them.

## Prohibitions

Do not change:

- `tpcn/experiments.py`, `tpcn/experiment_excursion_runtime.py`,
  `tpcn/excursion_neuron.py`, `tpcn/ir2.py`, or other production core/runtime
  modules;
- classifier, predictor, learning, reward, topology, energy, reset or
  settling semantics;
- the dataset gate by substituting synthetic data;
- downstream visualization, Luna-12B/12E/12L, spiral, temporal-analysis or
  viewer consumers;
- ACP-0006, A01-A15, IR-2 schema revision 1, or Luna-22/Luna-24 closure state.

If the reported historical split cannot be recovered, record that limitation
and keep the replacement split clearly versioned. If the UCI source/schema
cannot be validated or the stream cannot be label-isolated without core
changes, stop and return the evidence to Luna-0.

## Completion gate

Publish a completion handoff with exact baseline/result revisions, owned
files, dataset source/hash, parser and split recipe, sample manifest,
configuration, exact commands, repeated-run comparison, per-class and
prediction/credit/resource results, failed/not-run checks, label-boundary
evidence, and remaining limitations. Return to Luna-0 for independent review.
Luna-25 must stop before downstream migration and must not claim Luna-22
closure or repository-wide ACP-0006 integration readiness.
