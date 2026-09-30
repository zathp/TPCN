# Luna-13D Finite-Resource Utility Handoff

```yaml
tpcn_handoff:
  agent: Luna-13D
  luna_identifier: "Luna-13D"
  descriptive_name: "Finite-Resource Utility, Retention, and Capacity-Pressure Experiment"
  task_id: "finite-resource-utility-capacity-pressure"
  component: "bounded CPU experiment fixture and evidence runner"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "0fa71bcf4614c765c47f07ecdcbd85105edda7f5"
  result_revision: "c35f10e"
  dependencies:
    - "Luna-13B independently verified causal structural crossover"
    - "Luna-13C corrective external-task evidence"
  owner: "Luna-0 / project owner review required"
  classification: ["EXPERIMENT", "VERIFICATION"]
  hypothesis: "Under finite capacity, useful temporal structure is retained or recoverable while low-value structure is pruned or rejected under declared rules, with measurable external task utility."
  counter_hypothesis: "Useful structure is lost without declared reason, low-value structure survives, legitimate capacity blocks useful admission, or resource benefit is only task failure/silence."
  interfaces_relied_on: ["Luna-13B run_condition", "Luna-13C fixed external interval-deadline task", "BoundedTopology", "StructuralPlasticityController", "execute_bounded", "LocalEnergyModel"]
  label_information_boundary: ["fixed external targets are evaluation-only", "labels do not enter events, routing, evidence, utility, pruning or topology decisions"]
  timing_assumptions: ["positive finite delays", "short interval 1.0", "long interval 3.0", "deadline 3.0"]
  reset_boundaries: ["fresh bounded neuron and queue state per task case"]
  resource_bounds: ["event budget 24", "queue capacity 8", "fan-in 2", "fan-out 2", "edge capacity 6", "candidate capacity 8", "five random seeds"]
  authorized_scope: ["CPU fixture", "staged capacity pressure", "declared pruning", "normal post-pruning admission", "fixed/random controls", "artifacts", "focused tests", "handoff"]
  unauthorized_scope: ["atomic replacement invention", "protected-edge lifetime", "new utility objective", "GPU/CUDA requirement", "FPGA/FPAA validation", "Luna-13E"]
  controls: ["fixed topology", "equal-budget random growth seeds 0..4", "comfortable baseline", "distractor pressure", "capacity 4/5/6", "declared pruning"]
  measurements: ["task result", "target latency", "processed events", "proxy energy", "edge traffic", "queue peak", "edge count", "mutation status/reason", "completion status"]
  information_boundary_check: ["fixed target remains on_time/late by interval", "no labels enter neural computation", "no future held-out result enters mutation decisions"]
  hardware_mapping: ["CPU software reference only", "activity-cost proxy is not physical energy", "no hardware equivalence claim"]
  architecture_invariants_touched: ["A04 bounded topology", "A07 local structural evidence", "A08 bounded execution", "A09 local energy accounting", "A10 unproductive-cost interpretation", "A14 explicit finite admission/pruning"]
  preserves: ["A01 event-driven execution", "A02 local temporal state", "A03 finite propagation", "A06 predictive/error path", "A11 delayed credit contract", "A15 hardware independence", "Luna-13B and Luna-13C evidence"]
  architecture_change: false
  proposal: null
  files_changed: ["tpcn/finite_resource.py", "run_finite_resource_13d.py", "tests/test_luna13d_finite_resource.py", "artifacts/finite-resource-utility-13d/results.json", "artifacts/finite-resource-utility-13d/summary.json", "workflow/handoffs/finite-resource-utility-capacity-pressure-Luna-13D.md"]
  tests_added: ["tests/test_luna13d_finite_resource.py"]
  tests_passing: ["focused Luna-13D: 6", "focused preservation bundle: 106", "full CPU suite: 262"]
  tests_failed: []
  tests_not_run: ["optional Stage F workload shift", "CUDA/GPU/FPGA/FPAA"]
  assumptions: ["Luna-13C two-case external target is the fixed primary task", "metadata rebuild/reset remains the available checkpoint boundary"]
  unresolved: ["no full serialized runtime checkpoint", "no matched-utility resource reduction", "post-pruning coexistence lowered task result", "generalization and scalability remain untested"]
  recommended_next_agent: ["Luna-0 independent review"]
```

## Outcome and owned scope

**OBSERVED:** The CPU-only runner reused the Luna-13B `decay_low` structural
learning fixture and reproduced the Luna-13C learned edge `right -> target`
with delay `1.0`. It evaluated the fixed external task whose targets are
`on_time` for interval `1.0` and `late` for interval `3.0`.

The implementation added only the bounded experiment module, runner, focused
tests, artifacts and this handoff. No core topology, pruning threshold,
replacement mechanism, protected lifetime, or architecture contract was
changed.

## Architecture evidence

**OBSERVED:** Atomic edge replacement was not used or added. The experiment
used ordinary bounded admission, existing `prune_by_score`, and ordinary
growth after capacity was freed. `replacement_authorized` is recorded as
false in the artifact.

**OBSERVED:** The useful learned edge survived declared pruning. Low-value
edges `left -> noise` and `noise -> target` were pruned with the lowest
declared utility score. Pruning freed two edge slots. The later candidates
`right -> relay` and `relay -> target` were both admitted through normal
bounded growth.

**INFERRED:** The existing finite controller distinguishes the useful edge
from the low-value distractor population in this fixture. This is a fixture-
scoped mechanism result, not a general utility theorem.

**OBSERVED:** At capacity 4, the final candidate was rejected for
`edge_capacity`. At capacities 5 and 6, the same candidate was rejected for
`fan_in_full`. Full-capacity rejection is reported as a legitimate bounded
admission result.

## Benchmark and resource results

Fixture: `luna-13d-interval-deadline-capacity-v1`. The primary configuration
used event budget `24`, queue capacity `8`, fan-in `2`, fan-out `2`, edge
capacity `6`, and pruning utility threshold `0.1`. The declared proxy unit is
`activity-cost-proxy; uncalibrated`.

| Run | Capacity policy | Useful edge present | Task result | Events | Proxy energy | Latency | Pruned edges | Completion |
|---|---|---:|---:|---:|---:|---|---|---|
| A baseline | comfortable | yes | 2/2 | 8 | 8.0 | 2.0, 4.0 | none | completed |
| A expensive path | comfortable-expensive-useful | no | 2/2 | 12 | 12.0 | 2.0, 4.0 | none | completed |
| B distractor | sufficient capacity | yes | 2/2 | 8 | 8.0 | 2.0, 4.0 | none | completed |
| C capacity 4 | structural pressure | yes | 2/2 | 12 | 12.0 | 2.0, 4.0 | none | completed |
| C capacity 5 | structural pressure | yes | 2/2 | 12 | 12.0 | 2.0, 4.0 | none | completed |
| C capacity 6 | structural pressure | yes | 2/2 | 12 | 12.0 | 2.0, 4.0 | none | completed |
| D pruning | declared score pruning | yes | 2/2 | 8 | 8.0 | 2.0, 4.0 | 2 | completed |
| E post-pruning growth | normal admission | yes | 1/2 | 16 | 16.0 | 1.0, 1.0 | 0 | completed |

The expensive useful path alone preserved `2/2` but cost 12 events versus 8
for the direct baseline. The post-pruning graph retained the direct learned
edge and added the relay path; its second-arrival decision changed the task to
`1/2` and increased cost to 16 events. This is not an efficiency claim.

| Edge role | Uses | Reward/utility evidence | Cost | Age | Pruned | Reason |
|---|---:|---|---:|---:|---|---|
| externally useful `right -> target` | baseline traffic | Luna-13C present 2/2; removal 1/2 | 1 | 0 | no | retained by declared score |
| expensive useful `right -> relay` | path traffic when present | isolated path 2/2 | 2 | 0 | no | not selected for pruning |
| expensive useless `left -> noise` | 0 | no external contribution | 4 | 1 | yes | lowest declared utility score |
| expensive useless `noise -> target` | 0 | no external contribution | 4 | 1 | yes | lowest declared utility score |

| Seed | Policy | Final useful edge | Final graph | Task result | Events | Energy | Pruning outcome |
|---:|---|---|---|---:|---:|---:|---|
| 0 | random growth | `right -> target` | one direct edge | 2/2 | 8 | 8.0 | not applicable |
| 1 | random growth | absent | `left -> target` | 1/2 | 4 | 4.0 | not applicable |
| 2 | random growth | absent | `left -> target` | 1/2 | 4 | 4.0 | not applicable |
| 3 | random growth | absent | `left -> target` | 1/2 | 4 | 4.0 | not applicable |
| 4 | random growth | absent | `left -> target` | 1/2 | 4 | 4.0 | not applicable |

**OBSERVED:** All primary and control runs completed. No run in the generated
artifact was budget exhausted. A focused test with event budget `1` explicitly
produced `budget_exhausted` and was not treated as successful evidence.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest tests/test_luna13d_finite_resource.py -q` | c35f10e / Windows CPU | passed, 6 | focused suite |
| focused preservation bundle | c35f10e / Windows CPU | passed, 106 | 13D, 13C, 13B, 12H, 12N, Stage-0-related, reward, classifier, structural, runtime |
| `python -m pytest tests -q` | c35f10e / Windows CPU | passed, 262; skipped, 1 | complete CPU suite |
| `python -m compileall -q tpcn run_finite_resource_13d.py tests/test_luna13d_finite_resource.py` | c35f10e | passed | compile/static check |
| VS Code diagnostics | c35f10e | no errors | changed Python files |
| `git diff --check` | c35f10e | passed | repository check |
| CUDA/GPU/FPGA/FPAA | CPU-only scope | not applicable | non-gating |

The named Stage-0 test file remains absent; Stage-0 preservation was covered
by the existing reward, classifier, structural, recurrent and runtime tests.
The optional workload-shift Stage F was not run because the core stages were
complete and no replacement or protected-lifetime behavior was authorized.

## Assumptions, limitations and unresolved issues

**OBSERVED:** The generated artifact records baseline revision
`0fa71bcf4614c765c47f07ecdcbd85105edda7f5`, executed revision `c35f10e`,
branch `main`, and clean generation state. The committed artifact paths are
`artifacts/finite-resource-utility-13d/results.json` and
`artifacts/finite-resource-utility-13d/summary.json`.

**OBSERVED:** Labels remain outside the computational path by task design.
The fixed topology and random controls retain the external target semantics;
random growth is not uniformly inferior because seed 0 selects the useful
edge and reaches `2/2`.

**OBSERVED:** The experiment did not implement a full serialized checkpoint
for neuron state, local clocks, queues, eligibility, reward ledgers and random
state. Comparisons use bounded deterministic reconstruction/reset, consistent
with the Luna-13C limitation.

**INFERRED:** Useful structure was retained under the tested pruning pressure,
and declared pruning freed capacity for later normal admission. The result
does not establish general retention, task adaptation, or resource optimality.

**HYPOTHESIZED:** A workload shift may expose a different retention/adaptation
tradeoff, but it remains untested.

## Interpretation and terminal status

The mechanism gate is supported narrowly: the externally useful direct edge
was retained, two unused/low-value edges were pruned for their declared low
score, capacity was freed, and later bounded admission succeeded. The external
task remained `2/2` through baseline, distractor, capacity and pruning stages.

The resource-efficiency gate is not established. The expensive useful path
cost more events, and post-pruning coexistence cost more events while falling
to `1/2`; fewer events in the left-edge random controls reflect task failure.

Terminal status:

`PASS WITH FOLLOW-UP - RETENTION/PRUNING MECHANISM ESTABLISHED, RESOURCE BENEFIT LIMITED`

## Reproduction and rollback

From the committed implementation revision:

```text
python run_finite_resource_13d.py --baseline-revision 0fa71bcf4614c765c47f07ecdcbd85105edda7f5 --executed-revision c35f10e
python -m pytest tests/test_luna13d_finite_resource.py -q
```

The safe restoration point for the pre-experiment contract is
`0fa71bcf4614c765c47f07ecdcbd85105edda7f5`. No unrelated worktree changes
were modified.

## Next assignment

Return this handoff and both artifacts to Luna-0 for independent review.
Luna-13E is not authorized. Broader efficiency, generalization, workload
adaptation, serialized checkpoint equivalence, and hardware claims remain
unproven.