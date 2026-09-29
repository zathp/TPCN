# Luna-0 Independent Review of Luna-13C

## Review status

`PASS WITH FOLLOW-UP — CAUSAL TASK EFFECT VERIFIED, NON-GATING LIMITATIONS REMAIN`

This review does not create or authorize Luna-13D.

## Provenance

- Reviewed implementation/artifact revision: `575c2407db21786b21d64cb57d640d2a1a940ac0`
- Review source/tree: `main`, clean worktree, `HEAD == origin/main` at review start
- Luna-13C contract: `.github/agents/luna-13c.agent.md`
- Luna-13C handoff: `workflow/handoffs/useful-causal-effect-Luna-13C.md`
- Artifacts: `artifacts/useful-causal-effect-13c/results.json` and `summary.json`
- Runner: `run_temporal_efficacy_13c.py`
- Focused tests: `tests/test_luna13c_causal_utility.py`
- Luna-13B contract/review: `.github/agents/luna-13b.agent.md`,
  `workflow/handoffs/luna-0-review-Luna-13B.md`
- CPU environment: Windows, Python 3.10.8

## Independent attack table

| Area | Independent attack | Result | Status | Limitation |
|---|---|---|---|---|
| External target | Traced `_examples()` and each evaluation case | Targets are fixed as `on_time` for interval 1.0 and `late` for interval 3.0; no topology-derived target | passed | Two synthetic cases |
| Training/evaluation separation | Inspected `run_experiment()` ordering and immutable config | Luna-13B learning occurs before deterministic held-out construction/evaluation; metric and threshold are predeclared in code | passed | No serialized held-out checkpoint object |
| Learned-edge provenance | Traced `_learn()` to `run_condition("decay_low")` | Runtime-local records produce learned edge `right -> target`, delay `1.0`; no external target is passed to learning | passed | Weight/strength is not a separate learned field |
| Frozen-state equivalence | Compared condition construction and checkpoint fields | Fresh deterministic neurons/topologies are constructed per condition and results share a metadata fingerprint | partial | No clone/restore of neuron, queue, eligibility or random-state checkpoint; checkpoint hash is not full computational state |
| Learned edge present | Independent `run_experiment()` | `2/2` correct, accuracy `1.0`; arrivals `(1.0,2.0)` and `(1.0,4.0)` | passed | Fixture-level result |
| Targeted removal | Same inputs/targets with learned edge absent | `1/2` correct, accuracy `0.5`; both target-arrival lists empty, short case changes from on-time to late | passed | Direct graph reconstruction rather than removal API |
| Exact restoration | Compared edge set/fingerprint and replayed | Restored graph equals present graph; `2/2`, accuracy `1.0` | passed | No metadata beyond endpoint/delay exists in this fixture |
| Intervention contamination | Inspected fresh per-condition construction and repeated runs | No hidden mutation observed; repeated outputs are equal | passed | Fresh reconstruction makes this a deterministic equivalence check, not a stateful remove/restore test |
| Sham | Inspected `conditions["sham"]` | Sham graph is exactly the present tuple and bypasses intervention machinery; output `2/2` | follow-up | Too weak to test mutation-path side effects |
| Irrelevant-edge removal | Removed `left -> target`; retained learned `right -> target` | Graph changes, learned edge remains, `2/2` correct | passed | Irrelevance is analytic in this tiny fixture |
| Positive control | Reproduced fixed useful edge | `2/2` correct | follow-up | It is exactly the learned `right -> target` edge, not an independently specified edge |
| Fixed topology | No edges, same task inputs/targets | `1/2` correct; short fails, long default-late succeeds | passed | Default-late rule makes the negative baseline interpretable but asymmetric |
| Random growth | Replayed seed 0 and seed 1 | Seed 0: `1/2`; seed 1: `2/2` | follow-up | Implementation selects `source_ids[seed % 2]`; this is not a genuine random candidate-selection procedure |
| Metric semantics | Inspected accuracy calculation and case records | Accuracy is correct-case count / 2; no incomplete run counted as ordinary failure | passed | Small denominator: 0.5 is one case |
| Delay sensitivity | Replayed with propagation delay `3.0` | Learned-present becomes `1/2`; second arrivals are `4.0`/`6.0`; confirms route/deadline dependence | passed | Sensitivity is expected for this task construction |
| Deterministic replay | Repeated present/remove/restore/sham runs | Inputs, targets, arrivals, outputs, event counts, graph state and completion reproduce | passed | Not independent stochastic replication |
| Bounded execution | Replayed default and event budget `30` | All conditions completed, pending `0`, no exhaustion; budget increase unchanged outputs | passed | No energy/utility measurement in this fixture |
| Label/future leakage | Inspected learner inputs and 13B future-probe check | No labels enter learner; 13B semantic future evidence/admission unchanged | partial | 13C label test repeats the same run; it does not mutate evaluation labels, and 13C future test is not direct |
| Artifact reproduction | Regenerated representative/default and perturbation results from committed source | Default matrix and provenance match committed artifacts; artifact tree state was clean | passed | Artifact provenance predates this review documentation commit |
| Luna-13B preservation | Ran 13B and focused temporal regression slice | `41 passed` including 13B, 12H and corrected 12N tests | passed | Existing 13B limitations remain bounded to its fixture |
| Stage-0/prior regressions | Searched for dedicated Stage-0 file and ran complete CPU suite | No dedicated Stage-0 test file exists; full suite `255 passed, 1 skipped` | passed / N/A | Stage-0 is covered only by existing general tests, not a named slice |
| Workflow update | Added this handoff and authoritative records | Review result and next boundary recorded; no 13D created | passed | Publication commit follows review execution |

## OBSERVED

The external target is topology-independent. The learned edge is selected by
the previously reviewed Luna-13B runtime-local mechanism. The default causal
chain is reproducible:

`right -> target present: 2/2 -> targeted removal: 1/2 -> exact restoration: 2/2`

The short case is the changed case: with the edge, target arrivals are
`1.0, 2.0` and the decision is `on_time`; without the learned edge, there are
no target arrivals and the decision is `late`. The long case is `late` in both
conditions. All primary runs completed with no pending events or budget
exhaustion. Increasing the event budget from 12 to 30 did not change results.

The fixed topology is `1/2`; the default random seed 0 is `1/2`; alternate
seed 1 selects the useful right edge and is `2/2`. The delay-3.0 perturbation
reduces learned-present performance to `1/2`, showing the metric is sensitive
to the declared arrival deadline.

## INFERRED

Within this bounded fixture, the learned edge has a genuine task-level causal
route effect: removing that edge removes the only route that can make the
short interval arrive before the fixed deadline, and exact graph restoration
recovers the result. This supports the narrow task-effect claim, but not a
claim that the learning process discovers task utility in general.

## HYPOTHESIZED

The task may be useful as a minimal mechanistic bridge from Luna-13B structure
to external behavior. It does not establish generalization, random-selection
superiority, energy/resource benefit, scalability, hardware equivalence or
biological equivalence.

## Validation record

| Command/procedure | Result |
|---|---|
| `python -m pytest tests/test_luna13c_causal_utility.py tests/test_luna13b_temporal_crossover.py tests/test_luna12h_temporal.py tests/test_luna12n_temporal_direction.py -q` | `41 passed` |
| `python -m pytest tests -q` | `255 passed, 1 skipped` |
| `python -m compileall -q tpcn run_temporal_efficacy_13c.py tests/test_luna13c_causal_utility.py` | passed |
| Standard diagnostics on changed Python files | no errors |
| `git diff --check` | passed |
| CUDA/GPU/FPGA/FPAA | not applicable to this CPU-only review |

## Limitations and next boundary

The required follow-up is to strengthen the experimental evidence if this
fixture is reused: implement an actual sham through the intervention path,
use an independently specified useful edge, implement genuine seeded random
candidate selection, and perform a real label-mutation/future-isolation test.
Also serialize or compare the complete computational checkpoint if later
conditions carry nonzero learned neuron or eligibility state.

This review does not promote A14, amend A01-A15, authorize Luna-13D, or
authorize another implementation. A future experiment may be eligible for a
new contract only after explicit project-owner direction and a new Luna-0
review.

## Final status

`PASS WITH FOLLOW-UP — CAUSAL TASK EFFECT VERIFIED, NON-GATING LIMITATIONS REMAIN`