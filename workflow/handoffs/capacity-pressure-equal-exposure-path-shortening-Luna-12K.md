# Luna-12K Execution Handoff

```yaml
tpcn_handoff:
  agent: Luna-12K Capacity-Pressure, Equal-Exposure, and Path-Shortening Verification
  luna_identifier: "Luna-12K"
  descriptive_name: "Capacity-Pressure, Equal-Exposure, and Path-Shortening Verification"
  task_id: "capacity-pressure-equal-exposure-path-shortening-luna-12k"
  component: "controlled bounded-topology experiment with equal candidate exposure and real path-shortening intervention"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "e0f308f5aa76cdf41578f0574a2135b9bb0b256d"
  result_revision: "uncommitted"
  dependencies:
    - "Luna-12J PASS WITH FOLLOW-UP evidence"
    - "Luna-12I temporal-association policy"
    - "Luna-12H intrinsic temporal state and unequal-delay semantics"
    - "Luna-12E persistent routed topology"
    - "Luna-4 bounded topology"
    - "Luna-10 structural plasticity"
  owner: "Luna-12K execution owner"
  classification: ["EXPERIMENT", "VERIFICATION"]
  hypothesis: "Under equal candidate exposure and bounded topology pressure, temporal-associative growth allocates scarce capacity toward useful convergence and can create a causally measurable shorter path than temporally uninformed controls."
  counter_hypothesis: "After equal exposure and resource matching, temporal growth is no better than controls, capacity pressure is absent, or a selected shortcut does not change real routed computation and downstream state."
  interfaces_relied_on:
    - "BoundedTopology and StructuralPlasticityController"
    - "Luna-12E actual event-routing path"
    - "Luna-12I local CandidateEvidence policy"
    - "EventQueue, canonical timestamps and finite positive delays"
  label_information_boundary:
    - "Labels remain external evaluation/readout metadata and cannot enter events, prediction, routing, topology evidence, structural evidence, eligibility or energy computation."
  timing_assumptions:
    - "All edges have explicit positive finite delays."
    - "Equal-time ordering, time units, late-event handling and reset boundaries must be declared before execution."
  reset_boundaries:
    - "Event and local temporal evidence reset at declared sequence boundaries; matched topology/controller reset policy must be identical across conditions."
  resource_bounds:
    - "Finite nodes, edges, fan-in/out, candidate exposure/list capacity, event and queue budgets, history, lineage/path depth, mutation attempts, pruning/replacement, state and analysis buffers."
  authorized_scope:
    - "Use one bounded fixture, runner, raw artifact and focused tests to compare equal-exposure conditions."
    - "Use the existing topology, structural controller and actual routed event path; record raw configuration and all declared seeds."
  unauthorized_scope:
    - "Do not promote temporal association into A14, amend the architecture contract, or authorize Luna-12L or later."
    - "Do not redesign Luna-12I, create an auxiliary topology, amend A14, change the architecture contract, claim hardware/real-data acceptance, or authorize Luna-12L or later work."
  controls:
    - "Fixed topology"
    - "Pre-12I structural-growth policy"
    - "Random legal growth"
    - "Luna-12I temporal-associative growth"
    - "Reversed, shuffled or timing-destroyed temporal evidence"
    - "Optional oracle-like diagnostic selector only as a non-architectural upper bound"
  measurements:
    - "Equal candidate exposure: exposed, considered and selected candidates"
    - "Growth attempts, accepted edges, precise rejection causes, pruning/replacement and edge budget"
    - "Fan-in/out distributions and saturation, global/active-edge utilization, convergent motifs, duplicates, churn and stabilization"
    - "Long-path and shortcut hop count, cumulative delay, arrival timestamps and path-shortening frequency"
    - "Routed events, activations, prediction/error, task/class separation, energy/resource proxy and utility"
    - "Same-seed candidate, topology and replay determinism"
  information_boundary_check:
    - "The planned structural evidence is local and causally available; global evaluation may log measurements but cannot feed canonical decisions."
  hardware_mapping:
    - "The experiment uses finite counters, histories, edge records and positive-delay routing compatible with bounded FPGA/FPAA/hybrid resource modeling; no hardware equivalence is claimed."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "Event-driven computation, intrinsic temporal state, finite unequal-delay propagation, bounded topology/dynamics, predictive coding, locality, delayed credit, local energy semantics, label isolation and hardware-neutral reference behavior."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/temporal_capacity.py"
    - "run_temporal_capacity.py"
    - "tests/test_luna12k_capacity_pressure.py"
    - "tpcn/__init__.py"
    - "artifacts/temporal-capacity-12k/config.json"
    - "artifacts/temporal-capacity-12k/results.json"
    - "workflow/handoffs/capacity-pressure-equal-exposure-path-shortening-Luna-12K.md"
  tests_added:
    - "tests/test_luna12k_capacity_pressure.py: 7 focused tests"
  tests_passing:
    - "python -m pytest -q tests/test_luna12k_capacity_pressure.py: 7 passed."
    - "Prior and affected regression slice: 47 passed."
    - "python -m pytest -q: 182 passed, 1 skipped."
    - "compileall: passed; workspace diagnostics: no errors; git diff --check: passed with existing line-ending warning only."
  tests_failed: []
  tests_not_run:
    - "None of the required software checks."
    - "Real dataset, GPU/FPGA/ModelSim, hardware equivalence and architecture promotion: not applicable or unauthorized."
  assumptions:
    - "The 12J PASS WITH FOLLOW-UP handoff and current owner dispatch authorize creation of this separately scoped follow-up."
    - "The existing Luna-12E routed topology and mutation authority remain the only computational topology."
  unresolved:
    - "Scale beyond the seven-node synthetic fixture and the energy/prediction tradeoff remain untested."
    - "The five-seed result does not establish real-data, hardware or architecture-wide benefit."
  recommended_next_agent:
    - "Luna-0 Architecture Guardian for evidence review and a separate resource/scale decision."
    - "No Luna-12L or later authorization."
```

## Dispatch provenance

**OBSERVED:** Current repository HEAD is
`e0f308f5aa76cdf41578f0574a2135b9bb0b256d`. No existing Luna-12K milestone,
agent, specification or handoff was present. The worktree was clean before
this creation task.

**OBSERVED:** The Luna-12J handoff reports result `partially supported` and
gate `PASS WITH FOLLOW-UP`, with declared seeds `0, 1, 2, 3, 4`, fixed,
baseline, random, temporal and reversed conditions, and the explicit follow-up
of equal candidate exposure, capacity pressure and a long-path intervention.

**OBSERVED:** The raw Luna-12J artifact records temporal accuracy `1.0`, one
convergent fan-in motif, `8` events, proxy energy `4.6641830877` versus
baseline `5.6144365919`, and the seed-0 causal intervention from `8` routed
events to `6` with changed target state. It records `path_shortening: 0.0`
because no initial long competing path existed.

**OBSERVED:** The creation scaffold authorized this bounded execution from the
same baseline; the execution checks and results below supersede its
creation-only not-run status.

**INFERRED:** The 12J result authorizes a separately scoped Luna-0 follow-up
creation, not an implementation claim or automatic architecture promotion.

**HYPOTHESIZED:** Equal exposure and real capacity pressure will distinguish
useful temporal allocation from the candidate-exposure artifact and establish
whether a legal shortcut changes meaningful causal computation.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `git rev-parse HEAD`, `git status --short` | Windows, baseline before edits | passed; clean worktree, HEAD `e0f308f5aa76cdf41578f0574a2135b9bb0b256d` | repository state |
| Raw 12J JSON/config inspection | Current HEAD, seeds 0-4 | passed; declared bounds, conditions and intervention evidence present | `artifacts/temporal-efficacy-12j/config.json`, `results.json` |
| `python run_temporal_capacity.py --output artifacts/temporal-capacity-12k --seeds 0 1 2 3 4` | Windows, baseline `e0f308f5aa76cdf41578f0574a2135b9bb0b256d`, seeds 0-4 | passed; 25 condition results retained | `artifacts/temporal-capacity-12k/results.json` |
| `python -m pytest -q tests/test_luna12k_capacity_pressure.py` | Windows | passed: 7 | focused 12K tests |
| `python -m pytest -q tests/test_luna12j_temporal_efficacy.py tests/test_luna12i_temporal_association.py tests/test_luna12h_temporal.py tests/test_luna12e_integration.py tests/test_structural_plasticity.py tests/test_streaming_classifier.py` | Windows | passed: 47 | prior and affected regression slice |
| `python -m pytest -q` | Windows | passed: 182, skipped: 1 | full repository regression |
| `python -m compileall -q tpcn tests run_temporal_capacity.py run_temporal_efficacy.py run_spiral_benchmark.py train_cpu_visualization.py` | Windows | passed | compilation |
| Workspace diagnostics | Windows | passed; no errors in touched files | diagnostics |
| `git diff --check` | Windows | passed; existing Git LF/CRLF warning only | worktree diff |
| Real dataset, GPU/FPGA/ModelSim, hardware equivalence, architecture promotion | Luna-12K scope | not applicable / unauthorized | excluded by specification |

## Execution evidence

The execution used the existing `BoundedTopology`,
`StructuralPlasticityController`, `TemporalAssociationPolicy`, `EventQueue`,
`TPCNNeuron`, `LocalPredictor` and `LocalEnergyModel`. No second topology was
created. The initial actual routed topology was:

```text
source -1.0-> n1 -1.0-> n2 -1.0-> target
```

The initially absent shortcut was `source -0.75-> target`. The seven-node
fixture used fan-in `2`, fan-out `2`, edge capacity `6`, routing capacity `6`,
candidate capacity `8`, history capacity `8`, queue capacity `16`, event
budget `16`, three growth attempts and two replay examples. Equal-time events
use queue sequence order; all delays are positive finite time units; each
replay resets neuron, predictor, queue and event history state; topology is
reset between conditions; no late events or cycles are admitted.

Policies were defined before the run as follows:

| Condition | Candidate evidence |
|---|---|
| fixed | No mutation; the same candidate set is exposed for accounting. |
| baseline | Pre-12I deterministic scores `(3.0, 2.0, 1.0, 0.5)`. |
| random | Seeded permutation of scores `1..4` over the same candidate set. |
| temporal | Luna-12I local source history yields `source -> target` score `3`; all other exposed legal candidates score `0`. |
| reversed | Six local observations with all target observations before source observations; all exposed scores are `0`. |

The same four legal candidates, in the same exposure order, were used for
every condition: `source -> decoy`, `source -> target`, `zalternate -> target`
and `zzsource -> target`. The first is a structurally legal distractor; the
second is the temporally relevant shortcut; the remaining candidates are
legal, temporally uninformed competitors. Every adaptive condition exposed
`4` candidates, considered `9` pending candidates across `3` selections,
selected `3` candidates and made `3` growth attempts. The fixed condition
exposed the same set and selected none.

Across seeds `0, 1, 2, 3, 4`, temporal selected the shortcut `5/5`; baseline,
random and reversed selected it `0/5`. Temporal accepted one candidate and
recorded `fan_in_full: 1` and `fan_out_full: 1`. Baseline, random and reversed
accepted two candidates and each recorded one capacity rejection. No
candidate was silently counted as learned; no replacement, pruning or
duplicate proposal occurred during growth. Target fan-in reached `2` in the
temporal condition and source fan-out reached `2`; this is observed resource
pressure, not graph-appearance inference.

Mean post-growth measurements over five seeds were:

| condition | shortcut rate | accepted | rejected | routed events | neuron events | energy proxy | prediction loss | shortest delay | class separation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fixed | 0.0 | 0.0 | 0.0 | 6.0 | 8.0 | 7.990217 | 1.025229 | 3.00 | 1.132540 |
| baseline | 0.0 | 2.0 | 1.0 | 8.0 | 10.0 | 9.274247 | 1.025229 | 3.00 | 1.132540 |
| random | 0.0 | 2.0 | 1.0 | 8.0 | 10.0 | 9.274247 | 1.025229 | 3.00 | 1.132540 |
| temporal | 1.0 | 1.0 | 2.0 | 8.0 | 10.0 | 9.850877 | 1.284030 | 0.75 | 1.627047 |
| reversed | 0.0 | 2.0 | 1.0 | 8.0 | 10.0 | 9.274247 | 1.025229 | 3.00 | 1.132540 |

The pre-growth long path produced two target arrivals at timestamp `3.0`,
three hops and six routed events over the two-example replay. With the
temporal shortcut present, target arrivals were at `0.75` and `3.0`, one and
three hops, eight routed events, ten processed events, and a changed target
state. Removing `source -> target` and replaying the identical input stream
restored the two three-hop arrivals at `3.0`, six routed events, eight
processed events and the pre-growth target states. Seed-0 present/removed
energy was `9.850877`/`7.990217` proxy units and prediction loss was
`1.284030`/`1.025229`.

## Evidence classification

**OBSERVED:** Equal candidate exposure, equal topology/resource bounds, equal
adaptive growth attempts, actual fan-in/fan-out rejection, deterministic
five-seed replay, functional initial long path, legal temporal shortcut
formation, shorter real arrival path, altered routed event trace and altered
downstream state were all measured. Reversed timing removed the temporal
shortcut preference. Temporal growth used more proxy energy and prediction
loss than the controls in this fixture, while routed event counts after growth
were equal.

**INFERRED:** Under this bounded workload, local temporal evidence allocated
scarce structural capacity toward a real shorter causal route more reliably
than the tested baseline, random and reversed controls under equal candidate
exposure. The intervention supports a causal contribution rather than a
topology-only claim. The result is not an energy-efficiency win.

**HYPOTHESIZED:** Temporal association may retain useful path-selection value
at larger bounded scales, but its energy/prediction tradeoff and behavior
under other capacity regimes remain untested.

## Direct answers

1. **Did temporal growth select a real shorter path?** Yes, in `5/5` seeds;
  uninformed controls selected it `0/5`.
2. **Was it formed from legal local evidence?** Yes; only source-local,
  causally ordered observations generated the nonzero temporal score.
3. **Did it reduce cumulative delay or routed work?** Delay changed from `3.0`
  to `0.75`; routed work increased relative to fixed topology and matched
  the two-edge controls after growth.
4. **Did it alter downstream state/output?** Yes; target arrival timing,
  target state, activation trace and prediction-error measurements changed.
5. **Did removing it reverse the effect?** Yes; the identical replay restored
  the long-path arrivals and removed the shortcut contribution.
6. **Did the benefit survive equal exposure?** Yes for structural/path
  selection; the temporal condition had the same candidate exposure,
  consideration count, attempt count and bounds.
7. **Did it crowd out another useful edge?** It rejected one alternate
  target edge at fan-in and one source distractor at fan-out; whether either
  is useful for a different workload is unresolved.
8. **Did temporal growth outperform controls in useful allocation?** Yes for
  shortcut frequency and path delay, not for proxy energy or prediction loss.
9. **Did destroyed timing weaken preference?** Yes; reversed timing selected
  no shortcut in all five seeds.
10. **Is this architecture promotion evidence?** No. It is bounded synthetic
   experiment evidence for Luna-0 review only.

## Gate and next assignment

**Primary gate: PASS WITH FOLLOW-UP.** The core hypothesis receives credible
support under equal exposure, actual capacity pressure and causal shortcut
intervention. The bounded follow-up is required because the fixture is small
and synthetic, temporal growth has a measurable proxy-energy and
prediction-loss cost, and only one capacity regime was tested. Luna-0 should
review this evidence and decide whether to retain the policy as an optional
experimental mechanism or request a separately authorized scale/resource
study. This handoff does not promote A14, amend the contract, or authorize
Luna-12L or any later Luna.
