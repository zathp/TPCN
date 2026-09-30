# Luna-0 Independent Review of Corrected Luna-13D

## Review status

`PASS WITH FOLLOW-UP — RETENTION/PRUNING VERIFIED, USEFUL ADAPTATION NOT ESTABLISHED`

The corrected pass closes the prior endpoint-score, inert-threshold and fixed-
identity defects for the tested bounded fixture. It does not establish useful
post-pruning adaptation or resource efficiency.

## Provenance

- Review starting revision: `206a3b8463ef857db5e5d5b8d2679d7e877f3bab`
- Corrective implementation reviewed:
  `9ae2fb6574a4a45fa6a47c18e9aa7270bd4d3080`
- Corrective starting revision:
  `89de90b183cd54f1ae24f433b6161f1b14c23c0e`
- Corrective publication revision:
  `206a3b8463ef857db5e5d5b8d2679d7e877f3bab`
- Contract: `.github/agents/luna-13d.agent.md`
- Corrected handoff:
  `workflow/handoffs/finite-resource-utility-capacity-pressure-Luna-13D.md`
- Artifacts: `artifacts/finite-resource-utility-13d/results.json` and
  `artifacts/finite-resource-utility-13d/summary.json`
- Runner: `run_finite_resource_13d.py`
- Tests: `tests/test_luna13d_finite_resource.py`
- Worktree: clean at review start; `HEAD == origin/main`

## Independent attack table

| Area | Independent result | Status | Limitation |
|---|---|---|---|
| Endpoint independence | `_pruning_eligibility` consumes only age and observed utility; endpoint names are fixture/reporting inputs | passed | Structural controller lexical tie-break remains outside the primary unequal-score decision |
| Evidence reconstruction | Useful edge uses 4, last use 3.0, horizon 4.0, age 1.0, utility 4.0, cost 4.0, score 4.0; zero-use edges have age 4.0, utility 0.0, cost 0.0, score 0.0 | passed | Decision horizon is a declared fixture constant |
| Inactivity threshold | Ages 1/2/3 with threshold 2 produce false/true/true; equality is inclusive | passed | Positive integer threshold validation excludes zero |
| Utility threshold | Recent zero-use evidence with thresholds 0.0/0.1 produces false/true; equality is strict | passed | Utility is route-use proxy, not reward/eligibility credit |
| OR semantics | Inactive/low combinations produce retain, prune, prune, prune with reasons retained/utility/inactivity/inactivity_and_utility | passed | No alternate policy is claimed |
| Cost and score | Cost is diagnostic; pruning score equals observed use count and orders eligible edges | passed | Cost does not independently drive eligibility |
| Relabeling | Arbitrary IDs preserve evidence-role pruning and two-slot release | passed | Same synthetic topology/stream |
| Mirrored roles | Task source moved to left; useful left path retained, unused right/noise paths pruned | passed | Mirror is a bounded fixture control, not a new learned benchmark |
| Useful retention | `right -> target`, delay 1.0 is recent/sufficient-utility and retained | passed | Task relevance inherited from Luna-13C |
| Low-value pruning | `left -> noise` and `noise -> target` have zero use, age 4.0 and utility 0.0; both prune for inactivity_and_utility | passed | No reward ledger participates |
| Capacity release | 3 edges/capacity 6 before, 1 edge/5 free slots after; two slots released | passed | Topology accounting is fixture-scoped |
| Post-pruning utility | `2/2`, 8 events, proxy energy 8.0, latency `(2.0, 4.0)` | passed | No pruning-only efficiency gain |
| Relay admission | Both relay edges enter through normal bounded `grow`; no replacement | passed | New route is not useful adaptation |
| Post-growth regression | Duplicate arrivals change result to `1/2`; 16 events, energy 16.0, latency `(1.0, 1.0)` | passed | Not fixed in this review |
| Capacity reasons | Capacity 4: edge_capacity; 5/6: fan_in_full | passed | Reasons match projected topology constraints |
| Random controls | Seed 0 useful/right `2/2`; seeds 1-4 left/non-useful `1/2`, all complete | passed | No superiority claim |
| Bounded evidence state | Per-run evidence is bounded by finite topology edges; no production history is added | passed | Offline JSON is larger but finite per run |
| Label isolation | Labels are compared only after runtime; evidence uses route traffic, not targets | passed | No reward-based utility path tested |
| Deterministic replay | Repeated runs reproduce evidence, graph, task and resources | passed | Random controls remain seed-declared |
| Artifact regeneration | After clean-provenance correction, results and summary regenerate byte-identically | passed | Environment is the same CPU reference |

## OBSERVED

The primary pruning path is:

```text
route observer -> use count/timestamps -> age and observed utility
  -> OR threshold eligibility -> observed-score ordering -> bounded prune
```

The useful edge has route use count `4`, last-use timestamp `3.0`, declared
decision horizon `4.0`, inactivity age `1.0`, observed utility `4.0`, observed
cost `4.0`, and pruning score `4.0`. With inactivity threshold `2` and utility
threshold `0.1`, it is retained.

The two low-value edges have zero route uses, no last-use timestamp, sentinel
age equal to the declared horizon `4.0`, utility `0.0`, cost `0.0`, and score
`0.0`. They satisfy both pruning branches and are removed with reason
`inactivity_and_utility`.

The four OR cases were independently reconstructed:

| Inactive | Low utility | Decision |
|---:|---:|---|
| no | no | retain |
| no | yes | prune |
| yes | no | prune |
| yes | yes | prune |

Inactivity equality is operational (`>=`); utility equality is retained (`<`).
Cost is recorded but does not enter the Boolean eligibility decision. The
pruning score is the measured use-count proxy used for eligible-edge ordering.

Relabeled IDs preserve the decisions. In the mirrored fixture, `m-left` is the
task source and useful path; `m-right -> m-noise -> m-target` is unused and is
pruned. This follows measured traffic rather than the original `right` name.

## Task and resource separation

| State | Task | Events | Proxy energy | Latency | Completion |
|---|---:|---:|---:|---|---|
| Baseline | 2/2 | 8 | 8.0 | 2.0, 4.0 | completed |
| Immediately after pruning | 2/2 | 8 | 8.0 | 2.0, 4.0 | completed |
| After relay growth | 1/2 | 16 | 16.0 | 1.0, 1.0 | completed |

The post-growth route emits duplicate direct/relay target arrivals. The long
case changes to `on_time`, causing the external task regression. Lower resource
cost in non-useful random controls reflects missing useful output and is not
efficiency evidence. `RESOURCE EFFICIENCY NOT ESTABLISHED` remains the correct
resource conclusion.

## Capacity and controls

Capacity 4 fills the total edge budget before the final relay exit. At 5 and 6
edges, total capacity remains but target fan-in reaches its limit. The result
change from `edge_capacity` to `fan_in_full` is therefore explained by actual
projected topology state, not stale state or candidate-order drift.

The random controls are genuine seeded choices: seed 0 selects the useful
source and scores `2/2`; seeds 1, 2, 3 and 4 select the non-useful source and
score `1/2`. This supports only the bounded observation that task outcome
tracks whether the useful edge is selected.

## Validation record

| Command or procedure | Result |
|---|---|
| Corrected Luna-13D focused suite | 10 passed |
| Preservation bundle | 100 passed |
| Luna-13C tests | 6 passed |
| Complete CPU suite | 266 passed, 1 skipped |
| Compileall | passed |
| Diagnostics | no errors |
| `git diff --check` | passed |
| Corrected artifact replay | results and summary byte-identical |
| CUDA/GPU/FPGA/FPAA | not applicable, non-gating |

Relevant Stage-0 coverage remains represented by existing classifier, reward,
structural, recurrent and runtime tests; no dedicated Stage-0 test file is
present.

## INFERRED

Under this bounded fixture, pruning decisions are driven by measured route use,
inactivity and observed utility rather than endpoint identity. The useful edge
is retained, two stale zero-use edges are pruned, and two genuine topology
slots are released without degrading the external task.

Normal bounded capacity reuse is demonstrated, but the later relay path is not
useful adaptation: it reduces task utility and doubles event/proxy-energy
cost. No resource benefit, policy superiority, generalization, scalability,
full-state checkpoint equivalence, or hardware equivalence follows.

## HYPOTHESIZED

The next scientific question may investigate why local structural admission
accepts a route that degrades the external target and whether local evidence
can distinguish beneficial from harmful candidates before admission. This is a
future direction only; no successor contract is created or authorized.

## Final conclusion

`PASS WITH FOLLOW-UP — RETENTION/PRUNING VERIFIED, USEFUL ADAPTATION NOT ESTABLISHED`

Luna-13E is not created or authorized. The next action is project-owner/Luna-0
handling of this review record, not successor execution.