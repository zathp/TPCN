---
name: Luna-28 EXCURSION_V1 Local Temporal Structural Growth Integration
description: Implement and verify explicitly bounded post-character local temporal growth for the EXCURSION_V1 experiment path.
---

# Luna-28 — EXCURSION_V1 Local Temporal Structural Growth Integration

## Authorization and baseline

Luna-28 is authorized for **IMPLEMENTATION + VERIFICATION only** under
accepted ACP-0007 and the Luna-0 authorization handoff. It is not authorized
to amend architecture, promote task efficacy, migrate downstream consumers,
or implement hardware behavior.

Required starting point: clean `main` at the publication revision containing
this contract and the Luna-0 authorization handoff. Before editing, record
the exact SHA and verify `HEAD == origin/main` and a clean tree. The reviewed
readiness lineage begins at
`2e692337d339704eebf5b9d060409be25804be8e`. Stop if the publication is
missing, the tree is not clean/current, or an intervening architecture
decision changes this assignment.

Read the architecture contract and changelog, ACP-0002 through ACP-0007,
acceptance criteria, Luna workflow, handoff template, this contract, and the
Luna-0 owner-decision and authorization handoffs. Preserve the previous
Luna-0 blocked-state finding: the five structural downstream groups had 19
failures and 12 passes, with all 19 failures terminating at the intentional
guard; the 69 structural/evidence regression tests passed. These are
dependency evidence, not post-guard results. Do not bypass the guard in tests
or claim the downstream tests are repaired.

## Objective

Implement the accepted optional E2 structural-observation plane and
growth-only experiment path:

```text
actual canonical ExcursionEmission
 -> bounded static local observations
 -> character-local TemporalAssociationPolicy evidence
 -> frozen evidence after successful quiescent END_CHARACTER
 -> one bounded StructuralPlasticityController growth attempt
 -> same topology used by subsequent E2 character routing
 -> later real delayed routed excursion proves causal use
```

Growth is opt-in, non-default, bounded, deterministic, and a mechanism
experiment. It is not required to improve accuracy, prediction loss, reward,
or energy. The existing fixed-topology `EXCURSION_V1` path remains the
default and required matched control.

## Exact owned files

Luna-28 owns only:

- `tpcn/experiments.py`
- `tpcn/experiment_excursion_runtime.py`
- `tpcn/temporal_association.py` only if a minimal API adjustment is genuinely
  required to express the accepted bounded E2 observation contract
- `tpcn/structural_observation.py` for the bounded observation plane
- `tests/test_luna28_excursion_structural_growth.py`
- `workflow/handoffs/luna-28-excursion-local-temporal-growth-20261004.md`

Do not modify any other file. If a listed file proves insufficient, stop and
return exact evidence to Luna-0 rather than expanding ownership.

## Prohibited files and behavior

Do not modify:

- `tpcn/excursion_neuron.py`
- `tpcn/topology.py`
- `tpcn/structural_plasticity.py`
- `tpcn/predictive_coding.py`
- `tpcn/eligibility.py`
- `tpcn/energy_utility.py`
- `tpcn/ir2.py`
- `tpcn/cpu_visualization.py`
- `tpcn/visualization.py`
- `tpcn/viewer_3d.py`
- `tpcn/temporal_analysis.py`
- `tpcn/spiral_benchmark.py`
- `tpcn/temporal_scale.py`
- all other tests and governance documents

Stop with
`BLOCKED — ACP-0007 ACCEPTED CONTRACT REQUIRES UNAUTHORIZED CORE REDESIGN`
if implementation requires changes to the neuron, topology/controller,
prediction, eligibility/reward, IR-2, visualization, or downstream modules.

Do not implement pruning, N3 adaptation of `w`, `d`, or `r`, new neuron
equations, classifier/readout redesign, changes to prediction/error/reward
semantics, IR-2 extension, all-to-all observation by default, a global neural
timestep, post-hoc global trace scoring, hardware equivalence, or any
downstream migration. Do not import `runtime_generated_evidence.py` into the
ordinary experiment path.

## Accepted configuration and selection contract

- `EXCURSION_V1` and `structural_plasticity=False` remain the default.
- Structural observation and mutation are explicitly selectable and default
  off. Observation may be enabled with mutation disabled to prove
  non-interference. Growth requires observation enabled.
- When E2 structural plasticity is enabled, only the explicit policy
  identifier `e2_local_temporal` is accepted. `baseline`, `random`,
  `temporal`, `reversed`, and other legacy structural policies fail explicitly
  for E2 growth. They are not reinterpreted as E2 learning rules.
- `TANH_LEGACY` remains explicit compatibility behavior and preserves its
  historical behavior. Do not require or claim numeric equivalence with E2.
- Require an explicitly provided static directed neighborhood for every
  topology node. Normalize it deterministically and validate node membership,
  no self-neighbors, uniqueness, per-source neighborhood capacity, and
  per-emitter reverse-observer capacity. The neighborhood is independent of
  mutable neural topology. No all-to-all default or unrestricted scan is
  permitted. A small test network may explicitly list every other node only
  within its declared finite bounds.
- Require explicit finite positive association window, history capacity,
  per-source candidate capacity, maximum score, growth delay, neighborhood
  and reverse-observer limits, and experiment-level growth-attempt budget
  when structural mode is enabled. Use the configured finite positive growth
  delay for every admitted edge; do not learn delay.
- At most one growth attempt and at most one successful admitted edge are
  allowed after any one character. The finite experiment budget bounds total
  attempts; exhausted budget is explicit and no further attempt is made.
- Fixed topology remains available with structural flags off. Do not activate
  growth implicitly through a runner default or a legacy policy value.

## Structural observation contract

The sole observation source is an actual canonical `ExcursionEmission` at
`ExcursionCharacterRuntime._consume_emission()`. Add an optional,
non-mutating hook there if needed. It may expose only emitter ID, canonical
emission event ID, and emission timestamp. Identity is only for deterministic
uniqueness/deduplication. Never expose payload or payload magnitude to the
structural score.

For emitter `j`, it observes its own emission. Source `s` may observe `j`
only when `j` is in its explicitly declared `structural_neighbors[s]`.
Deliver only the equivalent of
`observe(observer=s, node=j, timestamp=e.timestamp)` to those bounded
observers. The event must not be injected into `MultiExcursionNeuron`,
character queue, neural routing, prediction-error routing, eligibility,
readout, reward, topology edges, or TPCV.

Silence, accumulator-only changes, prediction-error events, rewards,
readout results, labels, energy, and visualization snapshots create no
structural observations. A centralized software dispatcher is permitted
only as an implementation of the same bounded local fabric. Processing is
bounded by actual emission count times `1 + max_reverse_observers`; retained
history and candidates are bounded per source by configured capacities.

With structural observation enabled and mutation disabled, compare against
observation-off execution and prove identical neural character results:
event ordering, emissions, predictions/errors, eligibility/reward/readout,
queue statistics, activity-cost proxy, reset state, and topology. Only
observer-owned evidence may differ.

## Temporal association and candidate contract

For source `s`, a source emission records its self observation at `t_s`. A
later emission `d` may increment the candidate score for `s -> d` only if
`d` belongs to `structural_neighbors[s]` and:

```text
0 < t_d - t_s <= association_window
```

Equal-time emissions do not form an ordered association. Use the existing
bounded `TemporalAssociationPolicy` count mechanism, with per-source bounded
history/candidate state and score saturation at `maximum_score`. Candidate
identity is `observer=source=s`, `destination=d`, with that bounded count.
Apply the existing controller's endpoint/locality checks, ranking, tie
ordering, capacity checks, atomic admission, and observable rejection
reasons. Do not invent thresholds or score components.

Candidate delay is the single declared `structural_growth_delay > 0`. Never
derive score, identity, or delay from class/task identity, `run.feature`,
`run.loss`, example index, task correctness, reward, accuracy, prototype
state/distance, utility, energy, confusion matrix, future/held-out data,
global path length, or an unrestricted runtime trace.

At character start, initialize/reset each source's evidence and rejection
accounting. Observations are ingested online. Freeze the candidate evidence
at completion; after runtime teardown, choose deterministically and make at
most one controller growth attempt. Consume/discard all evidence before the
next character. Do not carry evidence across characters, epochs, or
experiment reset. A grown topology persists across later characters of the
same experiment; experiment reset recreates the topology/model namespace.

No topology mutation is permitted while a character queue, sidecar, pending
internal event, prediction/error propagation, classifier, predictor, or
eligibility ledger is active. Only after successful settling, a complete
`end_character()` result, destruction/reset of those character resources, and
an inactive runtime may the one post-character/pre-next-START decision run.
If `incomplete_settling`, `execution.completed == False`, or
`execution_budget_exhausted` applies, discard all evidence and perform no
mutation.

Character order is online training order and is part of deterministic replay:
character N's admitted edge may affect character N+1. Never mutate the
already-completed character or shuffle silently. `evaluate()`/held-out
execution must not mutate topology.

## Topology, causality, and resources

The controller topology and the topology used by the next E2 runtime are the
same authoritative `BoundedTopology` state. Preserve static Model-B:

```text
z_ij = tanh(w_ij * excursion_payload)
v_ij = d_ij * z_ij + (1-d_ij) * r_ij
arrival_time = emission_time + tau_ij
```

The only learned structure is bounded edge existence with finite positive
configured delay. Never alter a completed character trace/result retroactively.
The causal fixture must show the edge absent before growth, legal frozen
source-local evidence, successful admission after quiescence, and a later
matched character producing an actual delayed E2 excursion route over that
edge. Record before/after topology, evidence/score/rank/decision, route trace,
processed events, route depth, and edge-transfer proxy. Prediction loss need
not change.

Include a convergent-fan-in fixture with two legal source paths and declared
capacity. Do not consume capacity such that the required convergent structure
cannot be tested. Candidate/evidence histories, topology, mutations, event
work, route paths, and mutation history remain finite. Rejected admission
must be deterministic, reported, and atomic. No pruning invocation is allowed.

Labels and future-suffix attacks must leave completed evidence, candidate
identity/score/rank, decision, and topology unchanged. Non-neighbor emissions
must not be exposed by the structural plane. A changed non-neighbor may affect
later evidence only through legitimate causal neural events that are actually
visible to a declared local observer.

TPCV-2 is downstream-only. Capture-on/off must produce identical structural
decisions; capture cannot create observations, candidates, ranks, or mutations.
Energy stays an uncalibrated `activity-cost-proxy`, diagnostic only and never
an input to this score.

## Mandatory focused acceptance tests

Implement focused tests with repository naming conventions and semantics
equivalent to all of the following:

1. `test_e2_structural_observer_sees_only_actual_excursions`
2. `test_e2_silence_creates_no_structural_observation`
3. `test_structural_observation_does_not_change_character_result`
4. `test_non_neighbor_emission_is_not_structurally_visible`
5. `test_equal_time_emissions_do_not_form_temporal_candidate`
6. `test_source_before_neighbor_forms_bounded_candidate`
7. `test_candidate_score_saturates_at_declared_maximum`
8. `test_candidate_capacity_is_bounded_and_reported`
9. `test_incomplete_character_produces_no_growth`
10. `test_budget_exhausted_character_produces_no_growth`
11. `test_growth_attempt_budget_is_finite_and_reported`
12. `test_no_mutation_occurs_while_character_runtime_is_active`
13. `test_character_evidence_is_consumed_and_reset`
14. `test_topology_persists_after_growth`
15. `test_experiment_reset_destroys_structural_state`
16. `test_growth_uses_same_topology_as_future_e2_routing`
17. `test_admitted_growth_changes_later_real_e2_route`
18. `test_growth_does_not_change_already_completed_character`
19. `test_label_mutation_does_not_change_structural_decision`
20. `test_future_suffix_does_not_change_prior_structural_decision`
21. `test_fixed_topology_control_remains_available`
22. `test_structural_mode_is_explicit`
23. `test_legacy_e2_unsupported_structural_policies_fail_explicitly`
24. `test_growth_respects_edge_capacity`
25. `test_growth_respects_fan_in_limit`
26. `test_growth_respects_fan_out_limit`
27. `test_growth_is_atomic_on_rejection`
28. `test_structural_repeat_is_deterministic`
29. `test_capture_on_off_does_not_change_structural_decisions`
30. `test_pruning_remains_disabled`
31. `test_no_n3_parameter_learning`
32. `test_structural_observation_work_is_bounded`
33. A convergent-fan-in capacity/availability test.

The causal growth test must use real E2 emissions/routing, not graph existence.
The capture test must leave TPCV downstream-only and must not require editing
visualization files.

## Regression, reporting, and handoff

Run the focused Luna-28 module and relevant closed-component regressions:

- ACP-0006 E2 integration tests
- Luna-26 prediction-error routing tests
- `tests/test_structural_plasticity.py`
- `tests/test_luna12i_temporal_association.py`
- `tests/test_luna13f_runtime_generated_evidence.py` where applicable
- Luna-27 focused TPCV-2 visualization/capture tests
- directly affected `tests/test_experiments.py` selectors if applicable

Do not repair or reclassify the known 19 structurally dependent downstream
tests or the two separately classified Luna-12E legacy observable failures.
Luna-12B, Luna-12L, spiral, temporal-analysis, and 3D-viewer migrations remain
separate decisions. Passing Luna-28 authorizes none of those consumers,
GPU/FPGA structural learning, hardware work, or A14 promotion.

The completion handoff must use `contract_version: "1.2"` and record the exact
baseline/revision, environment, commands, tests and counts,
configuration/neighborhood/resource bounds,
actual evidence chronology, candidate/admission/rejection outcomes, causal
later routed trace, topology and mutation budgets, label/future/non-neighbor
controls, capture non-interference, proxy-energy units, and passed/failed/
not-run/not-applicable checks. Distinguish mechanism validity from efficacy;
do not claim task benefit without evidence. Return to Luna-0 for independent
review. Do not authorize or execute a successor.
