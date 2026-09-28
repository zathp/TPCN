# Luna-12J Temporal-Associative Structural Learning Efficacy and Causal Verification

```yaml
tpcn_handoff:
  agent: Luna-12J Temporal-Associative Structural Learning Efficacy and Causal Verification
  luna_identifier: "Luna-12J"
  task_id: "temporal-associative-structural-learning-efficacy-luna-12j"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  baseline_revision: "05d23eba86b806e9fe7e43d5dc66321f2c4bf612"
  result_revision: "uncommitted"
  dependencies: ["Luna-12I", "Luna-12H", "Luna-12E", "Luna-4", "Luna-10"]
  classification: ["EXPERIMENT", "VERIFICATION"]
  architecture_change: false
  gate: "PASS WITH FOLLOW-UP"
  result: "partially supported"
```

## Scope and implementation

The experiment used the existing `BoundedTopology`,
`StructuralPlasticityController`, `EventQueue` and `TPCNNeuron` path. No
second topology was created and no architecture contract or A14 requirement
was changed. Labels are external evaluation metadata only.

The smallest deterministic temporal fixture has five bounded nodes (`a`, `b`,
`target`, `d1`, `d2`) and two evaluation sequences:

- `a-first`: `a(+1.0,t=0.0)`, then `b(-1.0,t=0.5)`.
- `b-first`: `b(-1.0,t=0.0)`, then `a(+1.0,t=0.5)`.

Conditions use the same fan-in `2`, fan-out `2`, edge capacity `4`, candidate
capacity `8`, history capacity `8`, positive delay `1.0`, queue capacity `16`,
event budget `16`, and two growth attempts:

1. `fixed`: no structural mutation.
2. `baseline`: pre-12I controller selection over six legal candidates.
3. `random`: two legal candidates sampled from that same six-candidate space.
4. `temporal`: Luna-12I source-local temporal-association candidates.
5. `reversed`: temporal association with destroyed local ordering.

Declared seeds were `0, 1, 2, 3, 4`; all results were retained. Raw output is
in `artifacts/temporal-efficacy-12j/results.json`, with configuration in
`artifacts/temporal-efficacy-12j/config.json`.

## OBSERVED

Means across the five seeds:

| condition | accuracy | class separation | events | energy proxy | edges | convergent motifs |
|---|---:|---:|---:|---:|---:|---:|
| fixed | 0.500 | 0.000000 | 4.0 | 3.046377 | 0.0 | 0.0 |
| baseline | 0.500 | 0.000000 | 8.0 | 5.614437 | 2.0 | 0.0 |
| random | 0.500 | 0.000000 | 8.0 | 5.234297 | 2.0 | 0.0 |
| temporal | 1.000 | 0.336928 | 8.0 | 4.664183 | 2.0 | 1.0 |
| reversed | 0.500 | 0.000000 | 4.0 | 3.046377 | 0.0 | 0.0 |

Temporal seed-0 formed `a -> target` and `b -> target`, both delay `1.0`.
Target fan-in was `2`, source fan-out was `1` each, active-edge utilization
was `1.0`, mean path length/delay were `1.0/1.0`, and both mutations were
accepted. Rejection, replacement, pruning and duplicate counts were zero.
The target states were `-0.168464` and `0.168464` for `a-first` and `b-first`.

Baseline filled `a -> d1` and `a -> d2`, leaving target fan-in at zero. Random
varied by seed and sometimes formed a distractor convergence or one target
edge, but did not produce task separation in the declared seed set.

The temporal condition produced prediction loss `1.284030` across two errors,
`8` events/activations, and `4.664183` activity-cost-proxy units. Utility was
reported using the existing net reward-adjusted proxy, not calibrated joules.
No meaningful path shortening was observed: there was no pre-existing long
route, so `path_shortening=0.0` is a limitation rather than a positive claim.

## Causal intervention

For temporal seed-0, pruning learned `a -> target` and replaying identical
inputs reduced routed events from `8` to `6` and changed the `a-first` target
state from `-0.168464` to `-0.761594`. This demonstrates a changed downstream
contribution on the real routed path, rather than topology/accuracy
correlation alone.

## INFERRED

- In this bounded synthetic workload, local temporal evidence organized limited
  connectivity toward useful convergent fan-in more effectively than the tested
  baseline and random selections.
- The difference is attributable to a real temporal route: baseline and random
  used the same two-edge/eight-event budget without class separation, and edge
  removal changed the downstream replay.
- The capacity concern is supported for this fixture: ordinary baseline growth
  consumed two outgoing slots from `a` while useful target fan-in remained zero.

## HYPOTHESIZED

- Similar source-local selection may help larger workloads with competing
  paths, but this fixture establishes no scale, real-data or generalization
  claim.
- A workload with an existing long-path alternative might demonstrate path
  shortening; that mechanism remains untested here.

## Direct answers

1. **More useful convergence?** Yes in this fixture: temporal had one target
   motif; baseline/random means had zero.
2. **Meaningful path shortening?** Not established; no initial long path.
3. **Effect on neural computation?** Yes; routed events and target state
   changed, including under edge removal.
4. **Task/resource improvement?** Yes in this fixture: accuracy and separation
   improved at equal accepted-edge/event budgets, with lower proxy energy than
   baseline.
5. **Comparable budgets?** Accepted growth, edge capacity and fan-in/out were
   equal. Candidate exposure was not perfectly equal: baseline saw six
   candidates while random/temporal attempted two from the same six-candidate
   space. This is recorded as a limitation.
6. **Destroyed timing effect?** Yes; reversed ordering produced no candidates
   and no task separation.
7. **Promotion review?** Sufficient for Luna-0 to review the optional
   mechanism, not sufficient to promote the specific algorithm into A14.

## Fan-in conclusion

The motivating capacity concern is observed in the fixture, not generalized:
baseline growth reached two edges and zero target convergence, while temporal
growth reached target fan-in two before any saturation. No replacement was
needed, no unused-edge dominance was measured beyond the baseline distractor
edges, and path shortening was not testable in this workload.

## Validation record

| Check | Result |
|---|---|
| Focused Luna-12J tests | **passed: 4** |
| Luna-12I tests | **passed: 4** |
| Luna-12H temporal tests | **passed: 9** |
| Luna-12E routing/integration tests | **passed: 5** |
| Affected structural/runner/classifier/benchmark slice | **passed: 43** |
| Full pytest | **passed: 175, skipped: 1** |
| Compile/static validation | **passed** |
| Workspace diagnostics | **passed** for touched Python files |
| `git diff --check` | **passed**; existing line-ending warnings only |
| Real dataset, GPU/FPGA/ModelSim, hardware equivalence | **not applicable** |

## Files and reproduction

Changed for Luna-12J: `tpcn/temporal_efficacy.py`,
`tests/test_luna12j_temporal_efficacy.py`, `run_temporal_efficacy.py`,
`tpcn/__init__.py` (exports only), the two files under
`artifacts/temporal-efficacy-12j/`, and this handoff.

```text
python run_temporal_efficacy.py --output artifacts/temporal-efficacy-12j --seeds 0 1 2 3 4
python -m pytest -q tests/test_luna12j_temporal_efficacy.py
```

## Gate and recommendation

**Result: partially supported.**

**Gate: PASS WITH FOLLOW-UP.** The policy produced bounded structural and
computational benefit with a focused causal intervention and deterministic
five-seed evidence. The result remains limited by the small synthetic fixture,
absence of a long-path alternative, zero rejection/replacement pressure, and
unequal candidate exposure.

Return control to Luna-0. Before any A14 promotion decision, authorize only a
separately scoped follow-up with equal candidate exposure, a larger bounded
competing-path workload, explicit capacity/rejection pressure, and a meaningful
path-shortening intervention. Do not promote the specific algorithm, amend
A14, or authorize a later implementation Luna from this handoff.