# Luna-0 Independent Review of Luna-13D

## Review status

`BLOCKED — PRUNING/RETENTION EVIDENCE INVALID`

The narrow capacity-accounting, bounded-admission, route-level task
regression, and artifact-reproduction observations are valid. The stronger
claim that the architecture demonstrated evidence-based useful-edge retention
versus low-value pruning is not independently established.

## Provenance

- Starting/reviewed implementation revision:
  `f11a44f24fa9ad84e111435ed0ae8390b41c49a6`
- Implementation parent: `c35f10e`
- Contract publication: `0fa71bcf4614c765c47f07ecdcbd85105edda7f5`
- Branch: `main`
- Worktree: clean; `HEAD == origin/main` at review start
- Contract: `.github/agents/luna-13d.agent.md`
- Handoff: `workflow/handoffs/finite-resource-utility-capacity-pressure-Luna-13D.md`
- Artifacts: `artifacts/finite-resource-utility-13d/results.json` and
  `artifacts/finite-resource-utility-13d/summary.json`
- Implementation: `tpcn/finite_resource.py`,
  `run_finite_resource_13d.py`
- Focused tests: `tests/test_luna13d_finite_resource.py`

## Independent attack table

| Area | Independent result | Status | Limitation |
|---|---|---|---|
| Repository provenance | Synchronized `main`; exact source and artifacts present; clean tree and remote parity | passed | Review publication revision follows this record |
| Useful edge identity | `right -> target`, delay `1.0` exists in baseline and immediate post-pruning graph; graph fingerprint remains `3962ea30...` | partial | The runner hard-codes `USEFUL_EDGE` and the pruning score map by endpoint |
| Useful-edge task relevance | Baseline and Luna-13C rerun produce `2/2`; target removal remains `1/2`; restoration remains `2/2` | passed | Relevance is inherited from Luna-13C, not newly established by pruning |
| Low-value traffic | `left -> noise` and `noise -> target` receive zero traffic in the baseline direct-task run | partial | No reward/utility ledger or observed inactivity-to-score rule is used |
| Pruning derivation | `prune_by_score` receives literal scores `{useful: 1.0, distractors: 0.0}` | failed | `pruning_utility_threshold` and inactivity threshold do not control eligibility; endpoint identity is encoded in the fixture |
| Relabeling attack | Relabeled nodes cannot be built because `NODES` is fixed to `left/right/target/relay/noise` | failed | Identifier-independence was not demonstrated |
| Capacity release | Before pruning: 3 edges, capacity 6, 3 slots; after: 1 edge, 5 slots; two slots are genuinely freed | passed | This validates topology accounting, not pruning quality |
| Post-pruning admission | `right -> relay` and `relay -> target` are admitted through `StructuralPlasticityController.grow`; no replacement API exists | passed | Newly admitted path is not proven useful under the external task |
| Baseline vs pruning | Both are `2/2`, 8 events, energy 8.0, latencies `(2.0, 4.0)` | passed | Pruning-only efficiency was not demonstrated because resources are unchanged |
| Post-growth utility | Four target arrivals `(1.0, 1.0, 2.0, 2.0)` and `(1.0, 1.0, 4.0, 4.0)` change the long decision to `on_time`; result `1/2`, 16 events, energy 16.0 | passed | The regression is honest and reflects route competition/decision semantics |
| Capacity 1/4/5/6 | Capacity 1 and 4 reject on `edge_capacity`; 5 and 6 reject the final relay exit on `fan_in_full` | passed | Capacity 1 is a direct bounded-construction edge case |
| Budget stability | Budgets 24 and 48 reproduce baseline `2/2`, 8 events and post-growth `1/2`, 16 events | passed | No latent pending work observed |
| Random controls | Seed 0 selects `right -> target`, `2/2`, 8 events; seeds 1-4 select `left -> target`, `1/2`, 4 events | passed | Five seeds do not establish policy superiority |
| Proxy energy | Energy equals processed event count under the same local activity-cost model | passed | Not calibrated physical energy |
| Luna-13C preservation | Learned present `1.0`, targeted removal `0.5`, restoration `1.0`, sham `1.0` | passed | Existing two-case limitation remains |
| Luna-13B preservation | Dedicated Luna-13B tests pass | passed | No new crossover claim is made here |
| Stage-0/temporal preservation | Relevant classifier, reward, structural, recurrence, Luna-12H and Luna-12N tests pass | passed | Named Stage-0 test file remains absent |
| Artifact reproduction | Temporary regeneration is byte-identical for both JSON artifacts | passed | Reproduction preserves the same pruning design flaw |

## OBSERVED

The useful edge has the reported endpoint and delay before pressure and remains
in the post-pruning graph. Its computational task relevance is independently
confirmed by the Luna-13C matrix. The graph has three edges before pruning and
one after pruning, so two actual edge-capacity slots are released. The two
relay candidates are admitted through ordinary bounded growth and no atomic
replacement mechanism was introduced.

The baseline and immediate post-pruning graph both produce `2/2`, 8 events,
proxy energy `8.0`, and target latencies `(2.0, 4.0)`. After relay growth, the
direct and relay routes produce duplicate target arrivals. The task result is
`1/2`, events are `16`, proxy energy is `16.0`, and latencies are `(1.0, 1.0)`.
This is a task-utility regression, not an efficiency result.

Capacity accounting is internally consistent: capacity 4 reaches the edge
limit; capacities 5 and 6 reach the target fan-in limit for the final relay
exit. Increased budget does not alter the result. Random seed 0 reproduces the
useful edge; seeds 1-4 select the left edge and score `1/2`.

## INFERRED

The bounded topology and admission APIs correctly account for capacity and
normal post-pruning growth. The fixed external task result tracks whether the
direct useful edge is selected in this tiny fixture. These are narrower than a
validated retention/pruning mechanism.

## HYPOTHESIZED

The intended next experiment could test utility-derived pruning or
utility-aware admission, but that requires a separately reviewed correction.
This review does not select or authorize Luna-13E.

## Critical pruning finding

The runner declares `pruning_inactivity_threshold` and
`pruning_utility_threshold`, but does not use either to determine pruning.
Instead, `run_experiment()` constructs an endpoint-keyed literal score map:

```text
right -> target: 1.0
left -> noise: 0.0
noise -> target: 0.0
```

It then calls `prune_by_score()` with `maximum=2`. Changing the configured
utility threshold to `0.0`, `0.1` or `100.0` produces the same two removals.
The edge records are also authored from fixed role labels rather than a
runtime reward/utility ledger. A relabeling construction is unsupported by
the fixed `NODES` tuple, so identity-independent pruning was not shown.

Therefore the review cannot accept the claim that observed useful versus
low-value evidence caused the retention/pruning outcome. The two removals and
capacity release are observed topology operations, but their mechanism
evidence is invalid under the Luna-13D contract.

## Validation record

| Command or procedure | Result |
|---|---|
| Independent threshold attack and route tracing | Passed attack; threshold invariance and hard-coded score defect observed |
| Capacity 1/4/5/6 attack | Passed; reasons matched projected topology limits |
| Budget 24/48 replay | Results unchanged |
| Artifact regeneration in temporary directory | `results.json` and `summary.json` byte-identical |
| `python -m pytest tests/test_luna13d_finite_resource.py -q` | 6 passed |
| Luna-13B, Luna-12H, Luna-12N, reward, structural, classifier regressions | 80 passed |
| Luna-13C preservation matrix | 6 passed; present/removal/restoration/sham preserved |
| `python -m pytest tests -q` | 262 passed, 1 skipped |
| `python -m compileall -q ...` | passed |
| Diagnostics | no errors |
| `git diff --check` | passed |
| CUDA/GPU/FPGA/FPAA | not applicable and non-gating |

## Review conclusion

Separate conclusions are required:

- **Useful-edge retention:** task-relevant edge remains present, but
  evidence-based retention is not established because pruning eligibility is
  endpoint/score authored.
- **Low-value pruning:** two edges were removed and two slots were released,
  but the pruning mechanism evidence is invalid.
- **Capacity release:** independently verified.
- **Later admission:** independently verified through normal bounded growth.
- **Task utility:** pruning-only state preserves `2/2`; post-growth state
  regresses to `1/2`.
- **Resource efficiency:** not established. The post-growth state uses twice
  the events and proxy energy while performing worse.

The reported Luna-13D status is therefore not accepted. Final review status:

`BLOCKED — PRUNING/RETENTION EVIDENCE INVALID`

## Workflow and authorization boundary

This review updates the authoritative workflow and architecture changelog.
Luna-13E is not created or authorized. The next eligible work is a separately
reviewed correction or experiment that derives pruning from declared local
evidence, uses thresholds meaningfully, supports identity-independent fixture
checks, and keeps capacity reuse separate from useful adaptation.