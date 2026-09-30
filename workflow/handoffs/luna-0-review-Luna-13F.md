# Luna-0 Independent Review: Luna-13F

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-13F independent review"
  descriptive_name: "Independent review of runtime-generated local candidate evidence"
  task_id: "luna-0-review-runtime-generated-local-candidate-evidence-13f"
  component: "CPU Luna-13F implementation, controls, artifacts and workflow"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "0ba668ebe6cccd52fb0953638e1159090a79221e"
  result_revision: "published review package; final revision reported by publication verification"
  dependencies: ["Luna-13B", "Luna-13C", "corrected Luna-13D", "independently reviewed Luna-13E"]
  owner: "Luna-0 / project owner"
  classification: ["VERIFICATION", "EXPERIMENT", "ARCHITECTURE-REVIEW", "CPU-only"]
  hypothesis: "The committed Luna-13F implementation provides valid runtime-generated bounded evidence for the unchanged canonical scorer."
  counter_hypothesis: "The evidence is fixture/oracle assigned, is not frozen, or cannot be separated from held-out evaluation without an architecture change."
  interfaces_relied_on: ["TPCNNeuron", "TemporalAssociationPolicy", "CandidateEvidence", "StructuralPlasticityController", "execute_bounded", "Luna-13E external evaluator"]
  label_information_boundary: ["Labels and held-out outcomes must remain evaluator-only; the implementation does not use them in the primary scorer, but held-out chronology is invalid."]
  timing_assumptions: ["Runtime evidence must precede or equal the structural decision; held-out events must be later."]
  reset_boundaries: ["Fresh neuron, policy and queue per runtime run; evidence is intended to freeze at the decision boundary."]
  resource_bounds: ["event budget 32 by default", "queue 16", "history 8", "candidate capacity 2", "edge capacity 3", "fan-in 2", "fan-out 1"]
  authorized_scope: ["Independent review, direct source/artifact inspection, bounded probes, preservation validation, workflow and handoff updates"]
  unauthorized_scope: ["Corrective implementation execution", "architecture promotion", "Luna-13G", "hardware validation"]
  controls: ["no-evidence", "time shuffle", "reverse", "uniform intervals", "neutral decay", "relabel", "mirror", "equalization", "candidate order", "future mutation", "label isolation", "locality", "deterministic replay", "bounded execution"]
  measurements: ["event provenance", "local neuron state", "policy scores", "decision/admission timestamps", "held-out timestamps", "completion and pending events", "task result", "proxy energy", "regression counts"]
  information_boundary_check: ["Failed: beneficial/harmful role flags determine primary event exposure; held-out evaluation starts before the structural decision timestamp."]
  hardware_mapping: ["CPU-only review; no new hardware semantics or equivalence claim"]
  architecture_invariants_touched: ["A01", "A02", "A04", "A07", "A08", "A14", "A15"]
  preserves: ["Canonical production architecture and A01-A15 contract unchanged", "truthful blocked status in the verified handoff/artifacts", "Luna-13G unauthorized"]
  architecture_change: false
  proposal: null
  files_changed: ["artifacts/runtime-generated-local-evidence-13f/resumption-audit-20260930/audit-results.json", "workflow/docs/luna/LUNA_WORKFLOW.md", "workflow/ARCHITECTURE_CHANGELOG.md", "workflow/handoffs/luna-0-review-Luna-13F.md"]
  tests_added: []
  tests_passing: ["Focused Luna-13F: 8", "Required preservation matrix: 123", "Full CPU suite: 284 with 1 skipped", "compileall/py_compile", "git diff --check"]
  tests_failed: ["13F contract audit: 8 checks"]
  tests_not_run: ["Editor diagnostics", "CUDA/GPU/FPGA/FPAA and hardware equivalence"]
  assumptions: ["The committed audit and verified artifacts are the authoritative resumed execution path; the original unqualified artifact is historical and incomplete."]
  unresolved: ["A contract-valid matched-exposure fixture remains to be executed; whether it yields useful discrimination is unknown."]
  recommended_next_agent: ["Luna-13F corrective execution under the existing contract; another Luna-0 review is mandatory; no Luna-13G"]
```

## Verdict

**BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION CONFIRMED**

**LUNA-13F CORRECTIVE PASS ELIGIBLE UNDER EXISTING CONTRACT**

The implementation defect is experimental, not architectural: the existing runtime can produce bounded source-local policy counts and the unchanged canonical scorer consumes them. The current fixture nevertheless assigns the informative pattern through `beneficial_role`/`harmful_role`, so it cannot support the requested causal claim. No architecture change is required by this review, and no positive Luna-13F claim is established.

## Repository and provenance

**OBSERVED:** After `git fetch origin`, review revision is `0ba668ebe6cccd52fb0953638e1159090a79221e`, branch `main`, worktree clean before this review, and `origin/main` remains `f0821bd5eb0441ea892c463cbbcf173c80d09be6`. `HEAD` is one commit ahead of origin/main and origin/main is an ancestor; no pull/rebase was needed. The reviewed implementation tree is `d21027a8efdd2c5318d5f0bd84efbfcc8032cca3`. No commit or push was performed by this review.

Reviewed directly: `.github/agents/luna-13f.agent.md`, `tpcn/runtime_generated_evidence.py`, runner, focused tests, audit script/results, both 13F artifact generations, the execution and authorization handoffs, Luna-13E handoff/review, workflow, architecture contract/changelog and acceptance criteria.

## Causal-chain classification

| Stage | Independent finding | Status |
|---|---|---|
| Runtime events | Real addressed events are processed by `execute_bounded`; event timestamps and event IDs are recorded. | Implemented but contract-invalid as a primary experiment because the schedule is role-authored. |
| Local runtime state | `TPCNNeuron` receives events and `TemporalAssociationPolicy` owns bounded source-local history/count state. | Implemented correctly as an existing mechanism; its informative input is fixture-controlled. |
| Candidate-specific bounded evidence | Policy counts are transferred to `CandidateEvidence`; storage bounds and reset are documented. | Implemented but contract-invalid for this fixture; G/H exposure is not matched and candidate identity determines the informative pattern. |
| Canonical candidate score | `StructuralPlasticityController` is invoked without replacing the score. | Implemented correctly, but it scores contaminated evidence. |
| One-slot structural decision | Both candidates are legal, one slot is free, and one candidate is admitted. | Implemented correctly for the completed run; incomplete runs incorrectly admit. |
| Held-out external outcome | Luna-13E evaluator produces the expected G `2/2`, H `1/2`, and no-growth `2/2`. | Implemented but chronology-invalid: route traces begin at `0.0`, before decision `6.0`. |

## Evidence ownership and contamination boundary

| Evidence field | G source | H source | Runtime generated? | Fixture keyed? | Used by scorer? |
|---|---|---|---:|---:|---:|
| candidate observation schedule | `_schedule`: three short events at `0.5, 1.5, 2.5` | `_schedule`: one long event at `6.0` | No, the event pattern is authored by the fixture roles | Yes, via `beneficial_role`/`harmful_role` | Indirectly |
| local neuron residual/state | `TPCNNeuron.receive_event` | `TPCNNeuron.receive_event` | Yes | No direct score assignment | No |
| temporal association count | `TemporalAssociationPolicy.observe` count `3` | same policy count `0` | Mechanically yes, but informative exposure is fixture supplied | Yes, the schedule makes G short and H long | Yes, through `CandidateEvidence.score` |
| CandidateEvidence score | runtime policy count | runtime policy count | Derived from policy state | Candidate identity indexes the state, while role flags determine value | Yes |
| held-out result/labels | evaluator only | evaluator only | After evaluation | Not used by scorer | No |

The earliest invalid dependency is `_schedule` selecting `short_role` and `long_role` from `beneficial_role` and `harmful_role`. The addressed event definitions are legitimate controlled inputs; assigning their informative frequency/timing to the externally known beneficial/harmful roles is where controlled fixture input becomes oracle evidence. Renaming or moving the tuple construction would not repair that boundary.

The old Luna-13E tuple helpers are removed from the primary path, but the replacement is still a role-keyed schedule. Changing that schedule changes the primary score/choice without any independent change to ordinary runtime history. The canonical scorer is not itself overridden; the contamination occurs before scoring.

## Freeze, chronology and budget

**OBSERVED:** Primary evidence timestamps are `0.5, 1.5, 2.5, 6.0`; the declared decision timestamp is `6.0`; admission follows scoring. Mutating only events strictly after the original decision (`7.0` through `13.5`) changes scores from `3/0` to `3/4`, moves the decision to `13.5`, and changes admission from G to H. Evidence is accumulated after the supposed boundary; there is no immutable evidence snapshot or phase separation.

**OBSERVED:** Held-out route traces have minimum timestamp `0.0`, earlier than the primary decision `6.0`. The implementation does not offset held-out execution into a later phase, so the required `evidence <= decision < held-out evaluation` ordering is false.

**OBSERVED:** At budget `2`, execution processes `2` events, leaves `6` pending and reports `budget_exhausted`, but `_admit` still grows G. This is an implementation defect and invalid scientific accounting, not evidence of architectural insufficiency.

## Control matrix

| Control | Status | Independent finding |
|---|---|---|
| No-evidence | FAIL | Removing candidate events removes the candidate set and yields no admission; it does not test two zero-evidence candidates. |
| Time shuffle | FAIL | Runs, but inherits role-keyed evidence and has no valid independent expectation. |
| Reversed timing | FAIL | Runs, but inherits invalid fixture construction. |
| Uniform intervals | FAIL | Runs, but remains role-keyed and is not an uncontaminated temporal control. |
| Neutral/zero decay | NOT RUN | Count scorer has no decay parameter; the valid neuron-decay control was not run. |
| Relabeling | FAIL | G remains preferred under relabeling, but the relabeled schedule still assigns the same role pattern; it cannot clear contamination. |
| Mirrored roles | FAIL | The preference follows the explicitly swapped fixture schedule, not an independent runtime role. |
| Evidence equalization | FAIL | Scores are `2/1`, not a tie; deterministic tie-breaking is not isolated. |
| Candidate-order reversal | PASS | Ranking remains score-driven for the contaminated scores. |
| Future-event mutation | FAIL | Post-decision events alter evidence, score, rank and admission. |
| External-label mutation | NOT RUN | No independent label mutation control is present in the audit. |
| Locality attack | NOT RUN | Required attack was not run. |
| Deterministic replay | PASS | Repeated `run_experiment` results are equal. |
| Increased-budget execution | FAIL | Incomplete-budget behavior admits; no valid successful-evidence accounting follows budget exhaustion. |

The reported audit totals are independently reproduced: `5 passed`, `8 failed`, `5 not run`. The matrix above expands the scientific meaning of those categories; controls that execute but inherit contaminated input cannot validate the primary hypothesis.

## Architecture sufficiency and corrective authority

**OBSERVED:** Existing `TemporalAssociationPolicy` provides bounded source-local history and count accumulation, `TPCNNeuron` provides bounded local temporal state, and `StructuralPlasticityController` provides the unchanged canonical scoring/admission path. These are enough to attempt a contract-valid fixture.

**INFERRED:** The architecture is **partially sufficient**, and the current failure is an experiment implementation defect. A valid fixture still needs matched, non-role-authored runtime exposure, immutable pre-admission evidence, later held-out timestamps, and admission gating on completed bounded execution. No missing production capability has been demonstrated.

**HYPOTHESIZED:** A contract-valid fixture may tie or fail to predict G/H; that outcome would be scientifically valid. No architecture decision packet is required by this review. The smallest corrective work is confined to the authorized 13F fixture/runner, evidence freeze and validation/control accounting.

Therefore: **LUNA-13F CORRECTIVE PASS ELIGIBLE UNDER EXISTING CONTRACT**. Luna-0 explicitly authorizes the bounded corrective pass under the existing `luna-13f.agent.md` contract. This review did not execute it. Another independent Luna-0 review is mandatory after corrective execution, and Luna-13G remains unauthorized.

## Artifact truthfulness

The verified artifact pair under `artifacts/runtime-generated-local-evidence-13f-verified/` and the resumption audit report the blocked status. The original pair under `artifacts/runtime-generated-local-evidence-13f/` was generated at the pre-audit revision and has no `terminal_status` field in either `results.json` or `summary.json`; it therefore does not consistently report blocked status and must be treated as historical/incomplete, not as a positive result. The execution handoff truthfully reports the blocked status and does not claim readiness or authorize 13G.

## Regression and validation

| Check | Result |
|---|---|
| Focused Luna-13F | PASS: 8 |
| Contract audit | 5 passed, 8 failed, 5 not run |
| Required preservation matrix: 13F, 13E, corrected 13D, 13C, 13B, 12H, 12N, Stage-0 and adversarial/runtime surfaces | PASS: 123 |
| Full CPU suite | PASS: 284, SKIP: 1 |
| Python compilation | PASS |
| `git diff --check` | PASS before review edits; rerun after edits required |
| Editor diagnostics | NOT RUN |
| CUDA/GPU/FPGA/FPAA/hardware equivalence | NOT APPLICABLE / NOT RUN |

## Workflow and next boundary

The workflow and architecture changelog are updated by this review with the implementation revision, review revision state, terminal blocker, freeze/chronology/budget findings, control accounting, architecture sufficiency and corrective authority. A01-A15 and ACP status remain unchanged. No architecture proposal is created. No corrective implementation is executed in this publication task. The exact next boundary is the explicitly authorized Luna-13F corrective pass under the existing contract, followed by another independent Luna-0 review; Luna-13G remains unauthorized regardless of that result.
