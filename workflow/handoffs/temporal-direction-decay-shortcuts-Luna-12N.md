# Luna-12N Execution Handoff

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  luna_identifier: "Luna-12N"
  descriptive_name: "Temporal Direction and Intrinsic-Decay-Gated Shortcut Verification"
  task_id: "temporal-direction-intrinsic-decay-shortcut-verification-luna-12n"
  component: "bounded direction/decay policy comparison using corrected Luna-12M route instrumentation"
  status: "complete-execution"
  contract_version: "1.1"
  branch: "main"
  base_revision: "0d91207ec5db0ab8011e0fc020cc9e4e20915428"
  result_revision: "uncommitted from 0d91207ec5db0ab8011e0fc020cc9e4e20915428"
  dependencies:
    - "Luna-12M PASS WITH FOLLOW-UP corrected TPCN-EDGE-2 instrumentation"
    - "Luna-12K PASS WITH FOLLOW-UP causal path-shortening evidence"
    - "corrected Luna-12L NOT SUPPORTED scale evidence"
    - "Luna-12J, Luna-12I, Luna-12H and Luna-12E evidence"
  owner: "Luna-0 Architecture Guardian"
  classification: ["EXPERIMENT", "VERIFICATION"]
  hypothesis: "Under equal candidate opportunity, legal temporal direction and intrinsic-decay-relative preference can increase the fraction of accepted mutations that reduce measured causal delay and carry routed traffic."
  counter_hypothesis: "Direction and decay-aware variants do not improve used shortcut yield, or apparent gains arise from unequal opportunity, unmeasured traffic, graph-only analysis or nonlocal information."
  interfaces_relied_on:
    - "TPCNNeuron local exponential decay and elapsed timestamps"
    - "TemporalAssociationPolicy and CandidateEvidence"
    - "BoundedTopology and StructuralPlasticityController"
    - "Luna-12E actual routed topology and finite-delay EventQueue"
    - "Corrected Luna-12M TPCN-EDGE-2 lifecycle, traffic, candidate, rejection and decay records"
  label_information_boundary:
    - "Labels remain external evaluation/readout metadata and cannot enter events, predictor state, routing, structural evidence, eligibility or energy."
    - "Global path analysis and shortcut taxonomy are offline only."
  timing_assumptions:
    - "Use canonical local timestamps, positive finite edge delays, declared equal-time ordering and no global neural timestep."
    - "Decay-relative evidence is derived from local lambda and local delta_t; fixed absolute thresholds are controls only."
  reset_boundaries:
    - "Declare and match sequence, neuron, predictor, queue, evidence-history, topology and controller reset policy across all conditions."
  resource_bounds:
    - "Finite nodes, edges, fan-in/out, candidates, histories, queues, event/lineage paths, attempts, pruning/replacement and observation buffers."
    - "Seeds 0-4 and a predeclared finite decay-regime set; no outcome-dependent seed or threshold search."
  authorized_scope:
    - "Create and, after separate authorization, execute the six-condition policy matrix in the 12N specification."
    - "Use corrected Luna-12M instrumentation as the measurement basis and add only the smallest demonstrated exposure fix."
    - "Produce focused tests, bounded machine-readable artifacts, offline taxonomy and causal-intervention evidence."
  unauthorized_scope:
    - "Do not modify A14 or ARCHITECTURE_CONTRACT.md, change pruning/protection, add persistent edge strength/utility/eligibility, or add genetic hyperparameters/micro-NN."
    - "Do not redesign the classifier, use labels/global shortest paths in learning, claim hardware/real-data acceptance, or authorize a successor Luna."
  controls:
    - "Current direction without decay preference"
    - "Reversed legal direction without decay preference"
    - "Current direction with local intrinsic-decay-relative preference"
    - "Reversed legal direction with local intrinsic-decay-relative preference"
    - "Random legal growth with matched exposure"
    - "Fixed topology"
  measurements:
    - "Candidate exposure/counts, attempts, accepted edges, rejection reasons, fan-in/out and capacity limits"
    - "Static shortcut count/yield and used shortcut count/yield"
    - "Phase-scoped old-route, new-edge and new-route traffic from TPCN-EDGE-2"
    - "Hop, cumulative-delay and arrival-time deltas; coexistence/dominance/crossover where established"
    - "Prediction loss/error, proxy energy and units, events, activations, edge utilization, pruning and determinism"
    - "Before/after/removal causal intervention and raw lifecycle records"
  information_boundary_check:
    - "Local policy inputs are timestamps, elapsed time, local decay/residual state, local candidate evidence and legal local edge state."
    - "Global topology/path analysis, labels, task metrics and whole-network resource summaries are offline evaluation only."
  hardware_mapping:
    - "Finite counters, bounded histories, positive-delay routing and local decay arithmetic are reference quantities compatible with eventual hardware mapping."
    - "No FPGA, FPAA, hybrid or physical-energy equivalence is claimed."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "Event-driven computation, local intrinsic state, unequal finite propagation, bounded topology/dynamics, predictive/error events, local energy, delayed credit, label isolation and hardware independence."
  architecture_change: false
  proposal: null
  gate: "PASS WITH FOLLOW-UP"
  files_changed:
    - ".github/agents/luna-12n.agent.md"
    - "workflow/docs/luna/LUNA_12N_TEMPORAL_DIRECTION_DECAY_SHORTCUTS.md"
    - "workflow/handoffs/temporal-direction-decay-shortcuts-Luna-12N.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/README.md"
    - "tpcn/temporal_direction.py"
    - "tests/test_luna12n_temporal_direction.py"
    - "run_temporal_direction.py"
    - "artifacts/temporal-direction-12n/"
  tests_added:
    - "tests/test_luna12n_temporal_direction.py: 7 focused tests"
  tests_passing:
    - "Namespace scan: Luna-12N unused before creation."
    - "Corrected Luna-12M artifact and handoff review: PASS WITH FOLLOW-UP evidence supports the planned measurement basis."
    - "Documentation/static consistency review: agent, specification and handoff agree on identity, scope, policies, metrics and gates."
    - "python -m pytest -q tests/test_luna12n_temporal_direction.py: 7 passed"
    - "Required regression slice: 86 passed"
    - "python -m pytest -q: 211 passed, 1 skipped"
    - "python -m compileall -q tpcn tests run_temporal_direction.py"
    - "Workspace diagnostics: no errors in touched Python files"
    - "git diff --check"
  tests_failed: []
  tests_not_run:
    - "Hardware, real-data and physical-energy validation: not applicable/unauthorized."
    - "Hardware, real-data and architecture-promotion checks: not applicable/unauthorized."
  assumptions:
    - "Repository HEAD and current workflow documents are the authority; uncommitted 12M/12L evidence is retained as documented evidence, not committed history."
    - "Corrected TPCN-EDGE-2 phase traffic is sufficient for the planned first controlled shortcut comparison; unavailable replacement attribution remains explicit."
  unresolved:
    - "Whether direction, intrinsic-decay-relative preference or their combination improves used shortcut yield."
    - "Whether route coexistence, dominance, crossover or pruning timing can be established beyond the 12M fixture."
  recommended_next_agent:
    - "No successor Luna. After explicit execution authorization, assign Luna-12N execution and return the completed evidence to Luna-0."
```

## Dispatch provenance

**OBSERVED:** Execution began at `0d91207ec5db0ab8011e0fc020cc9e4e20915428`.
The worktree already contained the 12N creation scaffold and related workflow
edits; those pre-existing changes were preserved.

**OBSERVED:** Corrected Luna-12M schema `TPCN-EDGE-2` records endpoint-plus-
generation identities, lifecycle records, phase-scoped traffic for old and
new routes, candidate/rejection records, decay context, deterministic replay
and instrumentation ON/OFF equality. Its gate is `PASS WITH FOLLOW-UP`; replace-
ment attribution and hardware export remain unavailable.

**OBSERVED:** 12K demonstrated a real shorter causal route under equal exposure;
corrected 12L did not demonstrate robust four-class/scale benefit. The latter
is not evidence against shortcut formation.

**INFERRED:** 12M instrumentation is sufficient to define a controlled 12N
comparison that separates correlated edge creation from actual causal
compression and route use.

**HYPOTHESIZED:** Direction and decay-relative candidate preference may improve
used shortcut yield under the declared bounded workload. The bounded result
supports direction in this fixture but does not support an additional decay
gain.

## Validation record

| Command or procedure | Revision / environment | Observed result | Evidence |
|---|---|---|---|
| `git rev-parse HEAD`, `git status --short`, branch check | Windows, execution baseline | passed; `main`, HEAD `0d91207...`, pre-existing scaffold changes retained | repository state |
| namespace scan for `Luna-12N` | baseline workflow | passed; identifier unused before creation | workflow search |
| corrected 12M artifact/schema review | current worktree | passed for dependency gate; `TPCN-EDGE-2`, measured phase traffic, lifecycle, rejection and decay records present | `artifacts/edge-instrumentation-12m-corrected/summary.json` |
| required 12H/12I/12J/12K/corrected 12L/12M handoff review | current worktree | passed; evidence boundary and limitations recorded | workflow handoffs |
| documentation/static consistency review | uncommitted creation | passed | agent/spec/handoff cross-check |
| `python run_temporal_direction.py --output artifacts/temporal-direction-12n --seeds 0 1 2 3 4` | Windows, 3 decay rates | passed; 90 records | generated artifacts |
| `python -m pytest -q tests/test_luna12n_temporal_direction.py` | Windows | passed: 7 | focused tests |
| required 12M-to-runtime regression slice | Windows | passed: 86 | focused and prior-Luna tests |
| `python -m pytest -q` | Windows | passed: 211, skipped: 1 | full repository suite |
| `python -m compileall -q tpcn tests run_temporal_direction.py` | Windows | passed | compilation |
| workspace diagnostics | Windows | passed | no errors in touched Python files |
| `git diff --check` | Windows | passed; existing LF/CRLF warning only | worktree validation |

## Execution results

The execution emitted one record for each policy/seed/decay combination in
`artifacts/temporal-direction-12n/results.json`, plus configuration and summary
files. Decay rates were predeclared as `0.25`, `0.5` and `1.0`; seeds were
`0, 1, 2, 3, 4`. Adaptive policies exposed the same six candidates, considered
15 candidates over three attempts, and used the same finite topology bounds.

| policy | static shortcuts | used shortcuts | mean delay delta | mean POST_MUTATION energy | mean prediction loss |
|---|---:|---:|---:|---:|---:|
| current | 15/15 | 15/15 | 2.250 | 11.155 | 1.284 |
| reversed | 0/15 | 0/15 | 0.000 | 12.018 | 1.025 |
| decay | 15/15 | 15/15 | 2.250 | 11.155 | 1.284 |
| reversed_decay | 0/15 | 0/15 | 0.000 | 12.018 | 1.025 |
| random | 3/15 | 3/15 | 0.450 | 9.872 | 1.077 |
| fixed | 0/15 | 0/15 | 0.000 | 7.990 | 1.025 |

**OBSERVED:** A representative current run measured old-route traffic `2/2/2`
in `PRE_MUTATION/POST_MUTATION/POST_REMOVAL`, new-route traffic `2` in
`POST_MUTATION`, cumulative delay `3.0 -> 0.75`, and hop count `3 -> 1`.
Removal changed the replay trace and downstream computation. Old and new routes
coexisted after mutation; traffic dominance/crossover was not established.

**OBSERVED:** Current and decay-aware current each formed and used the shortcut
for all 15 records. Reversed and reversed-decay formed none. Random formed
three used shortcuts. Fixed had no accepted mutations, so its yields are
undefined.

**OBSERVED:** Intrinsic decay records came from `TPCNNeuron` temporal context
and were forwarded to `TPCN-EDGE-2`; changing the predeclared local decay rate
changed the recorded decay context without adding a global time gate.

**INFERRED:** Direction, rather than decay-relative preference, explains the
useful shortcut difference in this fixture. The combined condition adds no
observed improvement over current direction.

**HYPOTHESIZED:** Larger competing-path workloads or lifecycle timing may
separate decay regimes; this experiment does not justify edge protection,
persistent utility/strength, or a permanent decay threshold.

## Completion and rollback

Preserve baseline `0d91207ec5db0ab8011e0fc020cc9e4e20915428`; rollback is
limited to the execution-owned experiment files and must preserve the workflow
scaffold and unrelated worktree changes. No architecture contract, pruning
semantics or persistent edge state changed.

## Next assignment

No successor is authorized. Recommended Luna-0 action: review the raw
`TPCN-EDGE-2` records and retain `PASS WITH FOLLOW-UP` because direction is
reproducibly and causally supported here, while decay adds no gain in this
small fixture and energy/prediction tradeoffs remain unresolved.

## Corrective rerun after Luna-0 BLOCKED review

The initial execution and its `PASS WITH FOLLOW-UP` result above are retained
as historical provenance. Luna-0's subsequent evidence review assigned a
`BLOCKED` gate because the first implementation used one shared `delta_t`,
compared phase-labelled traces, used a shortcut-only yield denominator,
converted undefined fixed-topology yields to `0.0` in the summary, and kept
baseline provenance only in configuration.

**OBSERVED:** The corrective implementation remains bounded and uses the
existing `TPCN-EDGE-2` observer. Candidate records now contain candidate-local
source/destination timestamps, the actual neuron-reported `delta_t`, local
decay rate, residual factor, decay-relative score and deterministic rank. The
fixture exposes six candidates with distinct intervals `0.25`, `0.35`, `0.4`,
`0.75`, `1.0` and `1.2`; at decay rate `0.5`, the current policy ranks
`source -> target` first while the decay-aware policy ranks `n2 -> source`
first.

**OBSERVED:** Corrected output is at
`artifacts/temporal-direction-12n-corrected/` with 90 records, policies
`current`, `reversed`, `decay`, `reversed_decay`, `random`, and `fixed`, seeds
`0, 1, 2, 3, 4`, and decay rates `0.25`, `0.5`, `1.0`. Every result carries
baseline revision `75eaba6deca99b42c8d0921252c4c74dc57983d4`.

| policy | accepted mutations | static shortcuts | used shortcuts | static yield | used yield |
|---|---:|---:|---:|---:|---:|
| current | 30 | 15 | 15 | 0.500 | 0.500 |
| reversed | 45 | 0 | 0 | 0.000 | 0.000 |
| decay | 30 | 15 | 15 | 0.500 | 0.500 |
| reversed_decay | 45 | 0 | 0 | 0.000 | 0.000 |
| random | 30 | 3 | 3 | 0.100 | 0.100 |
| fixed | 0 | 0 | 0 | null | null |

**OBSERVED:** Accepted mutations are recorded individually and all accepted
mutations are the yield denominator. Current and decay-aware current each
accept one shortcut and one non-shortcut per record, so their yields are `0.5`
rather than `1.0`. Fixed topology retains undefined (`null`) yields.

**OBSERVED:** Causal intervention compares normalized computation evidence
only: route trace, target arrivals, arrival delay, downstream target state and
prediction/error evidence. Phase labels are excluded. For representative
current runs, removal changes all independent causal flags and the normalized
route digest; old-route and new-route traffic remain derived from the observer.

**INFERRED:** The corrected fixture supports a reproducible direction effect
relative to reversed legal orientation and random growth. It does not show an
additional used-yield improvement from intrinsic decay preference.

**HYPOTHESIZED:** A larger equal-opportunity workload may distinguish decay
regimes, but this rerun does not authorize a new Luna, alter pruning, add
persistent edge state, promote A14, or claim hardware acceptance.

### Corrective validation

- **Passed:** 11 focused Luna-12N tests, including candidate-local timing and
  ranking, phase-label-only negative control, causal removal, all-mutation
  denominator, null yields and per-record baseline.
- **Passed:** corrected artifact cardinality/provenance audit; 90 records and
  one baseline revision on every result.
- **Passed:** required 12H through 12M regression slice and relevant 12E,
  topology, structural-plasticity, event-runtime, temporal-analysis and
  experiment tests: 88 passed.
- **Passed:** full repository suite: 215 passed, 1 skipped; compilation,
  workspace diagnostics and `git diff --check` also passed.
- **Not applicable:** hardware, real-data and physical-energy acceptance.

**Corrected gate: `PASS WITH FOLLOW-UP`.** The prior `BLOCKED` gate is closed
for the repaired evidence paths. Direction remains supported in this bounded
fixture; decay gain, route dominance, replacement attribution, hardware
equivalence and broader workload generalization remain unresolved. No
successor is authorized.
