---
name: Luna-12K Capacity-Pressure, Equal-Exposure, and Path-Shortening Verification
description: Verify temporal-associative structural growth under equal candidate exposure, bounded capacity pressure, competing paths, and causal shortcut intervention.
---

# Luna-12K - Capacity-Pressure, Equal-Exposure, and Path-Shortening Verification

Read `workflow/ARCHITECTURE_CONTRACT.md`,
`workflow/ARCHITECTURE_CHANGELOG.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`,
`workflow/docs/luna/LUNA_12I_TEMPORAL_ASSOCIATIVE_STRUCTURAL_GROWTH.md`,
`workflow/docs/luna/LUNA_12J_TEMPORAL_ASSOCIATIVE_EFFICACY.md`,
`workflow/docs/luna/LUNA_12K_CAPACITY_PRESSURE_PATH_SHORTENING.md`, and the
12I/12J handoffs before editing. Record the exact baseline revision and
preserve unrelated worktree changes.

## Authorization and ownership

Luna-12K is a controlled `EXPERIMENT` and `VERIFICATION` follow-up to the
12J `PASS WITH FOLLOW-UP` result. This dispatch creates the scope only; it does
not execute the experiment and does not promote the Luna-12I mechanism into
A14. Return all results to Luna-0. Do not authorize Luna-12L or later work.

The execution owner may own:

- `run_temporal_capacity.py` or the smallest existing runner extension needed
  for the declared 12K fixture;
- `tpcn/temporal_capacity.py` or an existing experiment module only for
  bounded fixture/measurement support, not for changing the 12I policy;
- `tests/test_luna12k_capacity_pressure.py`;
- `artifacts/temporal-capacity-12k/` raw configuration, results and analysis;
- the completed 12K handoff.

The dispatch/specification/agent files are workflow-owned. Any production
change must be minimal, demonstrated necessary for measurement, and kept in
existing experiment boundaries. Do not create a second topology.

## Hypothesis and falsifier

Under equal candidate exposure and bounded topology pressure,
temporal-associative structural growth will allocate scarce connection
capacity toward useful causal convergence and can form a legal shortcut that
measurably reduces meaningful propagation path length or delay compared with
temporally uninformed controls.

The hypothesis is falsified in the tested scope when equalized controls match
or exceed useful convergence/path shortening, temporal evidence does not alter
selection, the shortcut does not change real routed computation, capacity
rejections are not actually exercised, or any benefit disappears after the
same-resource and reversed-timing controls are applied. Valid outcomes are
`supported`, `partially supported`, `not supported`, `inconclusive`, and
`blocked`.

## Required controls and equal exposure

Compare fixed topology, pre-12I structural growth, random legal growth,
temporal-associative growth, and reversed or timing-destroyed temporal
conditions. An oracle-like selector is optional and diagnostic only.

For every adaptive condition, equalize or explicitly quantify candidate set,
candidate count, mutation opportunities, growth attempts, edge budget,
fan-in/out limits, pruning/replacement budget, epochs/trials, event workload,
and declared seeds. Candidate exposure must be counted before selection; a
policy cannot receive extra useful candidates or computation and claim the
result. Retain every seed, failed admission and mismatch.

## Required fixture and measurements

Use a deterministic bounded fixture with multiple legal, resource-competitive
candidates, including temporally relevant, temporally irrelevant and
structurally legal edges. Reach real fan-in, fan-out, global-edge,
candidate-capacity or replacement pressure and record exact rejection causes.
Start with a functional finite-delay path such as `source -> n1 -> n2 ->
target`; keep a legal shorter candidate such as `source -> target` initially
absent. Both paths must use normal event routing and explicit positive delays.

Before and after shortcut formation, measure hop count, cumulative path delay,
arrival timestamps, routed events, activations, downstream state/output,
energy/resource proxy and utility. Remove or disable the shortcut and replay
the same event stream. Establish the chain from local temporal evidence to
selection, legal topology change, shorter real path, changed routed behavior,
and changed downstream state. Test whether the shortcut crowds out another
useful edge.

Record task/class separation, prediction loss/errors, candidate edges exposed/
considered/selected, growth attempts, accepted additions, rejection reasons,
pruning/replacement, fan-in/out distributions and saturation, global edge
utilization, convergent motifs, active-edge utilization, duplicate proposals,
edge churn, stabilization and same-seed determinism.

## Architectural boundaries

Preserve A01-A04, A06-A11, A14 and A15. Do not introduce a global neural clock,
future information, labels, global topology statistics, evaluation metrics,
wall-clock state or unrestricted trainer state into canonical events, predictor
state, routing, topology evidence, structural evidence, eligibility or energy
computation. Keep all event queues, histories, candidates, edges, paths,
lineage, mutation records and analysis buffers finite. New edges have positive
finite delay and cannot rewrite emitted or in-flight events.

Labels remain external evaluation/readout metadata. This is not a real-data,
hardware-equivalence, classifier-redesign or architecture-promotion task.
Do not alter A14, rewrite the 12I timing rule, or treat graph-distance change
alone as useful evidence.

## Required validation and handoff

Run focused 12K tests, 12J, 12I, 12H, relevant 12E routing tests, affected
structural-plasticity and classifier/readout regressions, full `pytest`,
compile/static validation, workspace diagnostics and `git diff --check`.
Report each as passed, failed, not run or not applicable. Separate
`OBSERVED`, `INFERRED` and `HYPOTHESIZED` evidence, preserve unfavorable seeds,
and answer all seven path-shortening questions in the specification.

Even a PASS returns to Luna-0 and does not promote the specific mechanism or
authorize a later Luna.
