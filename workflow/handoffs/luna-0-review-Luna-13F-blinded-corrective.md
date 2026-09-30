# Luna-0 Independent Review: Blinded-Mapping Corrective Luna-13F

**BLOCKED - REQUIRED CONTRACT CONTROLS NOT EXECUTED**

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-13F independent review"
  descriptive_name: "Independent review of blinded runtime-generated local candidate evidence"
  task_id: luna-0-review-runtime-generated-local-candidate-evidence-13f-blinded-corrective
  component: "CPU Luna-13F implementation, controls, artifacts and workflow"
  status: blocked
  contract_version: "1.1"
  branch: main
  base_revision: 435277323badea0fc1fd11b56b8a51e9033db053
  implementation_revision_reviewed: "authorized corrective changes in worktree at review start; not committed"
  review_revision: "uncommitted review publication"
  tree_hash_at_review_start: dcee582fa8fb347f578793c2ef383bd936e83234
  worktree_at_review_start: dirty
  head_equals_origin_main: true
  owner: Luna-0 / project owner
  classification: [VERIFICATION, EXPERIMENT, ARCHITECTURE-REVIEW, CPU-only]
  architecture_change: false
  proposal: null
  luna_13g: unauthorized
  dependencies:
    - .github/agents/luna-13f.agent.md
    - blinded corrective authorization revision 435277323badea0fc1fd11b56b8a51e9033db053
    - artifacts/runtime-generated-local-evidence-13f-verified/results.json
    - artifacts/runtime-generated-local-evidence-13f-verified/summary.json
  raw_execution_status: "NEGATIVE RESULT - RUNTIME EVIDENCE GENERATED BUT DOES NOT PREDICT USEFUL GROWTH"
  final_review_status: "BLOCKED - REQUIRED CONTRACT CONTROLS NOT EXECUTED"
  preservation: "focused 10 passed; preservation 62 passed; reported full CPU 286 passed, 1 skipped"
```

## Review basis

**OBSERVED:** The repository started on `main` at
`435277323badea0fc1fd11b56b8a51e9033db053`, equal to `origin/main`, with a
dirty worktree containing the authorized corrective implementation and
artifacts. The source, tests, handoff, authorization, workflow, contract and
changelog were inspected directly. No `audit-results.json` exists for the
verified artifact; the older resumption audit is stale and explicitly records
the prior role-contaminated execution.

**OBSERVED:** Independent execution reproduces the raw result:

| Mapping | Candidate A endpoint | Candidate B endpoint | Selected | Selected held-out |
|---|---|---|---|---|
| P0 | relay | noise | candidate_A | 2/2 |
| P1 | noise | relay | candidate_A | 1/2 |

P0 and P1 both give the neutral candidate A the short motif and candidate B the
long motif. The endpoint permutation is deterministic, but the actual event
schedule differs in endpoint identities as expected. The base topology remains
relay-to-target delay `0.5` and noise-to-target delay `2.0`; both candidates
remain individually legal with one free edge slot.

## Independent review matrix

| Area | Independent result | Interpretation | Status |
|---|---|---|---|
| Pre-admission blinding | No `beneficial_role`, `harmful_role`, G/H or utility lookup remains in the reviewed module | Neutral candidate names are used; endpoint roles still encode the fixed fixture topology, so this does not by itself prove utility-independence | passed, limited |
| P0 mapping | A->relay, B->noise; A selected; 4.0/0.0; 2/2 | Reproduced | passed |
| P1 mapping | A->noise, B->relay; A selected; 4.0/0.0; 1/2 | Reproduced negative utility correspondence | passed, limited |
| Runtime evidence | Eight candidate observations; four short associations increment A, four long observations do not increment B | Actual source-local count evidence is reconstructed | passed |
| Evidence mechanism | `TemporalAssociationPolicy` count increments within a 2.0 window | Primarily observation-count/interval gating; not decay-sensitive score evidence | passed |
| Canonical scorer | Frozen `CandidateEvidence` reaches `StructuralPlasticityController`; no override found | Score/rank/selection reproduced | passed |
| One-slot competition | Both candidates legal; edge capacity 3 with two base edges; loser rejected by capacity | Structural competition is valid in the executed path | passed |
| Held-out chronology | Decision is runtime timestamp 19.0, but held-out evaluator resets event time and adds hard-coded metadata 20.0 | Actual cross-phase chronology is not established | failed |
| External-label mutation | Artifact sets `pre_admission_unchanged: true` and repeats scores; no label-mutated execution is performed | Declarative claim, not an attack | failed |
| Locality attack | Artifact reports no private-state/global access based on the same trace | No adversarial nonlocal mutation or alternate-state attack | failed |
| Neutral decay sweep | Rates 0.0, 0.1, 1.0 reproduce count scores; only neuron state changes | Supports count-based interpretation; record lacks complete per-run rank/selection table | passed, limited |
| Saturation/reset/eviction | Capacity rejection and reset are reproduced | No eviction path is exercised; reset is not a separate candidate-identity contamination attack | failed |
| Valid mirror | Mirror swaps neutral motif endpoint; candidate B wins | Evidence preference moves, but held-out utility is not independently paired as a causal mirror control | passed, limited |
| No-evidence | Zero scores and deterministic selection are present | Tie-breaking is distinguishable from evidence; no utility advantage shown | passed, limited |
| Equalization | Runtime schedule produces equal scores | Actual runtime tie is present; no direct score assignment found | passed |
| Candidate order | Reversal retains selected endpoint/candidate | Ranking is order-independent in this case | passed |
| Future exclusion | Future event is placed in `future_events` and excluded by `events[:16]` before execution | Not a live post-admission mutation/freeze attack | failed |
| Budget behavior | Below-budget run is incomplete and blocked from admission | Exact completion and above-boundary matrix are not run | failed |
| No-growth | 2/2, 8 events, 8.0 activity-cost-proxy | Growth does not improve task or resource cost | observed |
| Resource cost | P0 selected growth: 12 events, 12.0 proxy units | No resource-efficiency claim | observed |
| Contract audit | No corrected `audit-results.json`; five controls are not independently evidenced | Aggregate focused tests cannot substitute for requirement-level audit | failed |
| Preservation | Focused 10 and preservation 62 pass; reported full CPU 286/1 skip | Shared behavior remains intact in available checks | passed |
| Final claim | Raw negative utility result is reproducible | Closure is not valid until controls are actually executed | blocked |

## Scientific interpretation

**OBSERVED:** Proposition 1 is supported for this fixture: ordinary runtime
events generate bounded source-local candidate-specific association counts
before admission.

**OBSERVED:** Proposition 2 is supported in the narrow fixture: those counts
reach the unchanged canonical scorer and affect a legal one-slot admission.

**NOT ESTABLISHED:** Proposition 3 is not a verified positive claim. The raw
P0/P1 result is consistent with the reported negative interpretation, but the
review cannot treat it as a scientifically closed negative experiment because
label/locality attacks, live future exclusion, actual chronology, eviction and
complete budget-boundary/audit evidence are missing.

The no-growth baseline remains `2/2`, 8 events and `8.0` uncalibrated
activity-cost-proxy units. P0 selected growth remains `2/2`, 12 events and
`12.0` units. The decay sweep indicates count accumulation rather than a
decay-sensitive score. No architecture change is required or authorized by
this review; no utility predictor, ACP, Luna-13G contract or Luna-13G
authorization is created.

## Required disposition

The implementation and raw artifact should remain available as review evidence,
but Luna-13F is **not closed**. A separately authorized corrective execution
must provide executable external-label and locality attacks, actual continuous
phase chronology with held-out events after admission, complete candidate
lifecycle semantics including eviction or an explicit contract-supported
non-eviction result, exact/above budget controls, and a requirement-level audit
artifact. This review does not authorize another pass by itself and does not
choose a future architecture mechanism.
