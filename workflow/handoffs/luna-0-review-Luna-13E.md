# Luna-0 Independent Review: Luna-13E

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-13E review"
  descriptive_name: "Independent post-pruning admission-quality review"
  task_id: "luna-0-review-post-pruning-admission-quality-13e"
  component: "CPU Luna-13E fixture, bounded admission path, artifacts and workflow"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "dd241ec9ee7af7456ae70bae2192d4237dab5d21"
  result_revision: "7faf8d3f1c82927304875bb6263219d5954a463d"
  dependencies: ["Luna-13B", "Luna-13C", "corrected Luna-13D"]
  owner: "Luna-0 / project owner"
  classification: ["VERIFICATION", "EXPERIMENT", "ARCHITECTURE-REVIEW"]
  hypothesis: "In the declared post-pruning one-slot fixture, existing bounded local pre-admission evidence selects the candidate that preserves the fixed external task over a harmful legal candidate."
  counter_hypothesis: "The current score does not distinguish the candidates, or selection depends on future outcome, labels, endpoint identity, ordering, or invalid capacity pressure."
  interfaces_relied_on: ["BoundedTopology", "CandidateEvidence", "StructuralPlasticityController", "EventQueue", "execute_bounded"]
  label_information_boundary: ["Labels and held-out outcomes remain external evaluation only; label mutation leaves admission unchanged."]
  timing_assumptions: ["Positive finite edge delays; fixed interval task; decision at fixture time 4.0 after bounded observations."]
  reset_boundaries: ["Each held-out case creates fresh neurons and queue; topology is fixed per policy evaluation."]
  resource_bounds: ["event budget 24", "queue capacity 8", "edge capacity 3", "fan-in 2", "fan-out 1", "candidate capacity 8", "maximum growth 1", "observation history max 3 records per candidate"]
  authorized_scope: ["Independent reconstruction, attack controls, artifact verification, workflow/changelog update, review handoff."]
  unauthorized_scope: ["Luna-13F", "utility-aware production admission", "abstention mechanism", "ACP promotion", "hardware validation"]
  controls: ["order swap", "relabel", "mirror", "equalized evidence", "future mutation", "label mutation", "fixed/no-growth", "random seeds 0-4", "score boundary", "increased event budget", "deterministic replay"]
  measurements: ["task result", "arrivals/latency", "events", "proxy energy", "queue peak", "completion", "graph fingerprint", "scores/ranks"]
  information_boundary_check: ["Passed for the canonical CandidateEvidence path; controlled score generation remains fixture-authored rather than demonstrated runtime observation."]
  hardware_mapping: ["No new hardware claim; bounded score/evidence fields are representable, but no hardware trace was run."]
  architecture_invariants_touched: ["A04 bounded topology", "A07 local evidence and label isolation", "A14 bounded local structural adaptation"]
  preserves: ["A01-A03 event timing", "A08 bounded execution", "A09 proxy accounting", "A15 software-reference boundary"]
  architecture_change: false
  proposal: null
  files_changed: ["tpcn/post_pruning_admission.py metadata correction", "focused test assertion", "workflow/LUNA_WORKFLOW.md", "workflow/ARCHITECTURE_CHANGELOG.md", "review and execution handoffs", "corrected artifacts"]
  tests_added: []
  tests_passing: ["92-test preservation matrix", "276 full CPU tests with 1 skip"]
  tests_failed: []
  tests_not_run: ["CUDA/GPU", "hardware equivalence"]
  assumptions: ["The declared fixed interval-deadline task is the external ground truth; proxy energy is not calibrated physical energy."]
  unresolved: ["Generality across workloads, runtime evidence generation, utility prediction, cost prediction, and abstention remain unestablished."]
  recommended_next_agent: ["No successor authorized; project owner may later choose a bounded follow-up hypothesis."]
```

## Verdict

**PASS WITH FOLLOW-UP — HARMFUL GROWTH AVOIDED, GENERALITY NOT ESTABLISHED**

This is a narrower result than the experiment runner's provisional PASS. The independent review verifies that the current canonical admission path selects G in the declared fixture and that the selected G graph preserves the fixed task while H degrades it. Because G and no-growth both achieve `2/2`, the result is avoidance of harmful growth, not task improvement.

## Repository and Provenance

**OBSERVED.** Review began after `git pull --ff-only origin main`.

- Published review base: `dd241ec9ee7af7456ae70bae2192d4237dab5d21`
- `HEAD == origin/main` at review start: yes
- Branch: `main`
- Worktree at review start: clean
- Reviewed contract: [.github/agents/luna-13e.agent.md](../../.github/agents/luna-13e.agent.md)
- Implementation: [post_pruning_admission.py](../../tpcn/post_pruning_admission.py)
- Runner: [run_post_pruning_admission_13e.py](../../run_post_pruning_admission_13e.py)
- Tests: [test_luna13e_post_pruning_admission.py](../../tests/test_luna13e_post_pruning_admission.py)
- Results: [results.json](../../artifacts/post-pruning-admission-13e/results.json)
- Summary: [summary.json](../../artifacts/post-pruning-admission-13e/summary.json)
- Execution handoff: [post-pruning-admission-quality-Luna-13E.md](post-pruning-admission-quality-Luna-13E.md)
- Authoritative workflow: [LUNA_WORKFLOW.md](../docs/luna/LUNA_WORKFLOW.md)
- Changelog: [ARCHITECTURE_CHANGELOG.md](../ARCHITECTURE_CHANGELOG.md)

The experiment artifact recorded exact baseline and executed revisions, branch, Python/platform, and generation dirty state. The stale H frozen text (`0/2`) was found during review and corrected to the observed `1/2` at review implementation revision `0a53b01b398d461eac3a962431b9ffcdae459e55`.

## Independent Reconstruction

### Candidate legality and one-slot competition

**OBSERVED.** Immediately before ranking:

| Item | Value |
|---|---|
| Base edges | `relay -> target (0.5)`, `noise -> target (2.0)` |
| Edge count/capacity | `2/3` |
| Remaining relevant slots | `1` |
| Target fan-in | `2/2` |
| Source fan-out | `0/1` |
| Relay/noise fan-out | `1/1` each |
| G | `source -> relay`, delay `0.5`, individually legal |
| H | `source -> noise`, delay `1.0`, individually legal |

Both candidates were independently connected against the same base topology without exceeding edge, fan-in, fan-out, or routing limits. H did not lose through structural invalidity. Both were presented at the same ranking point and the controller's `max_growth_per_adaptation` was `1`.

### External ground truth

**OBSERVED.** Independent evaluation using the fixed interval-deadline task produced:

| Condition | Task | Events | Proxy energy | Latency | Queue peak | Completion |
|---|---:|---:|---:|---|---:|---|
| Corrected Luna-13D post-pruning/no-growth reference | 2/2 | 8 | 8.0 | `(2.0, 4.0)` | 2 | completed |
| G admitted | 2/2 | 12 | 12.0 | `(2.0, 4.0)` | 2 | completed |
| H admitted | 1/2 | 12 | 12.0 | `(4.0, 6.0)` | 2 | completed |

The no-growth reference and G both preserve task utility. G uses more events and proxy energy than the reference and is not resource-beneficial.

### Pre-admission evidence and score reconstruction

**OBSERVED.** The production `StructuralPlasticityController` receives only `CandidateEvidence` fields. The raw controlled fixture evidence was:

| Candidate | Raw bounded temporal evidence | Score arithmetic | Cost/reward/error evidence | Rank |
|---|---|---:|---|---:|
| G | three elapsed intervals `0.5, 0.5, 0.5`; each counts because `elapsed <= 1.0` | `1 + 1 + 1 = 3.0` | propagation delay `0.5` available but not scored; reward/prediction-error/predicted cost unavailable | 1 |
| H | one elapsed interval `3.0`; does not count | `0 = 0.0` | propagation delay `1.0` available but not scored; reward/prediction-error/predicted cost unavailable | 2 |

The canonical key is `(-score, source, destination, evidence_id)`. Recomputing it yields G before H. Swapping candidate presentation order still selects G. Boundary checks selected H when H score exceeded G and selected G when G exceeded H; equal scores selected by deterministic endpoint/evidence tie-breaking.

**LIMITATION.** The raw observations are controlled tuples constructed by `_local_observations("G"/"H")`; they are not emitted by a runtime source-neuron observation buffer. The admission controller itself does not receive G/H identity or ground truth, but the fixture-level evidence generator is keyed by candidate label. This supports a bounded score-path check, not a general claim that runtime local state predicts usefulness.

### Time and causality

**OBSERVED.** Recorded evidence availability was G `2.5`, H `3.0`, and the declared decision time was `4.0`. All score-driving records satisfy `evidence_time <= decision_time`. The held-out evaluator is called after ranking/admission. Future mutation added a post-decision record but preserved score, rank, selected candidate and graph fingerprint.

No reward or eligibility term contributed. No prediction/error term contributed. No post-admission event count or held-out result contributed to ranking.

### Endpoint and ordering attacks

**OBSERVED.** Node relabeling with changed lexical IDs preserved the G preference and task result. The mirrored fixture shifted beneficial/harmful endpoint roles and preserved the evidence-role preference and G `2/2` result. Candidate list order reversal preserved G selection. These controls test the canonical score path; they do not remove the fixture generator's explicit G/H evidence construction limitation described above.

### Equalized evidence

**OBSERVED.** Setting both scores to `1.0` produced equal scores. H was selected only through deterministic tie-breaking and obtained `1/2`; this is not evidence of beneficial-growth prediction.

### Future and label mutation

**OBSERVED.** Adding future records after the decision left evidence, scores, ranks, selected candidate and graph unchanged. Mutating external labels changed evaluation metadata to `late`, `on_time` while preserving runtime input, evidence, scores, ranks, admission and pre-output computation.

### Reward and cost legitimacy

**OBSERVED.** No reward, eligibility, reward-adjusted cost or prediction/error evidence was available before admission. Propagation delay was available as edge metadata but was explicitly excluded from the score. Post-admission event count and proxy energy were used only for evaluation; they were not copied backward into predicted cost.

Current architecture has no score threshold, confidence threshold or abstention. Negative-score H evidence can still grow when directly selected. No abstention was invented during review.

## Harmful and G Mechanisms

**OBSERVED.** The Luna-13D harmful trace has long-case target arrivals `(1.0, 1.0, 4.0, 4.0)`, target state recorded, and fixed target `late`. Duplicate direct/relay arrivals cause the long case to be classified `on_time`, producing `1/2`.

**OBSERVED.** G preserves target latencies `(2.0, 4.0)` and produces `2/2`, matching the no-growth utility result. It does not improve the fixed task over no-growth; its contribution is avoiding H's harmful timing interference.

## Controls, Replay and Bounds

**OBSERVED.** Relabel, mirror, equalized, future, label, random, fixed/no-growth, score-boundary, order-swap, repeated replay, and increased-budget controls completed within declared finite budgets. Representative deterministic replay produced identical evidence, scores, ranks, graphs, task outcomes and event counts. Increasing the event budget from 24 to 48 and queue capacity from 8 to 16 did not change the G result or graph. Evidence history was bounded at three records for G and one for H; candidate capacity was eight.

Random controls were genuinely seeded and selected both candidates:

| Seed | Selected | Task | Events | Energy | Completion |
|---:|---|---:|---:|---:|---|
| 0 | H | 1/2 | 12 | 12.0 | completed |
| 1 | G | 2/2 | 12 | 12.0 | completed |
| 2 | G | 2/2 | 12 | 12.0 | completed |
| 3 | G | 2/2 | 12 | 12.0 | completed |
| 4 | G | 2/2 | 12 | 12.0 | completed |

This five-seed sample does not establish broad superiority over random admission.

## Preservation and Validation

| Area | Result | Evidence |
|---|---|---|
| Luna-13E focused tests | PASS: 10 | `python -m pytest tests/test_luna13e_post_pruning_admission.py -q` |
| Independent preservation matrix | PASS: 92 | Luna-13E, 13D, 13C, 13B, 12H, 12N, Stage-0 reward/runtime and label tests |
| Full CPU suite | PASS: 276, SKIP: 1 | `python -m pytest tests -q` |
| Compile/static | PASS | `python -m compileall -q ...` |
| Diagnostics | PASS | VS Code diagnostics reported no errors on touched Python files |
| Whitespace | PASS | `git diff --check` |
| Artifact replay | PASS after correction stabilized | Repeated generation produced identical hashes; one first-run difference was the intended stale-metadata correction |
| CUDA/GPU/hardware | NOT APPLICABLE / NOT RUN | CPU-only Luna-13E scope |

Corrected Luna-13D, Luna-13C, Luna-13B, and Stage-0 preservation remained passing. No invariant regression was observed.

## Interpretation and Boundary

**INFERRED.** In this tested post-pruning one-slot fixture, the existing canonical score path prefers the candidate whose held-out route preserves the fixed task and avoids H's harmful growth.

**INFERRED.** Because no-growth and G are both `2/2`, the supported claim is: **bounded pre-admission evidence avoided the harmful candidate while preserving task utility**. It is not task improvement, resource efficiency, general utility prediction, or general superiority to random.

**HYPOTHESIZED.** A broader claim would require runtime-generated local evidence and workload-shifted, matched candidate populations; an abstention or utility-aware mechanism may be a future architecture question, but none is authorized by this review.

No ACP is required. A01-A15 remain unchanged. No architecture mechanism was added, no production admission threshold was invented, and Luna-13F was not created, executed, or authorized. A successor may be considered only after separate project-owner authorization.

## Required Next Boundary

No next Luna is authorized by this handoff. The project owner may later select a bounded follow-up hypothesis from the observed limitations, such as runtime evidence generation, workload-shift robustness, abstention semantics, or task utility versus resource cost. Any such work requires its own dispatch and review boundary.
