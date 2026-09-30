# Luna-0 Independent Review: Corrective Luna-13F

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-13F independent review"
  descriptive_name: "Independent review of corrected runtime-generated local candidate evidence"
  task_id: "luna-0-review-runtime-generated-local-candidate-evidence-13f-corrective"
  component: "CPU Luna-13F implementation, controls, artifacts and workflow"
  status: "blocked"
  contract_version: "1.1"
  branch: "main"
  base_revision: "dcee582fa8fb347f578793c2ef383bd936e83234"
  result_revision: "uncommitted review documentation"
  dependencies: ["Luna-13B", "Luna-13C", "corrected Luna-13D", "independently reviewed Luna-13E"]
  owner: "Luna-0 / project owner"
  classification: ["VERIFICATION", "EXPERIMENT", "ARCHITECTURE-REVIEW", "CPU-only"]
  hypothesis: "The corrected 13F fixture generates candidate evidence independently of held-out utility and role semantics."
  counter_hypothesis: "Utility knowledge remains in candidate mapping, topology construction, or an experiment-side convention, or required controls are absent."
  interfaces_relied_on: ["TPCNNeuron", "TemporalAssociationPolicy", "CandidateEvidence", "StructuralPlasticityController", "execute_bounded", "Luna-13E external evaluator"]
  label_information_boundary: ["No independent external-label mutation control was run; held-out labels remain evaluator metadata in the inspected path."]
  timing_assumptions: ["Evidence must be frozen before scoring/admission and held-out events must be causally later, not merely given later metadata."]
  reset_boundaries: ["Fresh neuron, policy and queue are constructed per runtime call; actual post-freeze live mutation was not independently demonstrated."]
  resource_bounds: ["event budget 32", "queue 16", "history 8", "candidate capacity 2", "edge capacity 3", "fan-in 2", "fan-out 1"]
  authorized_scope: ["Independent source and artifact review", "use of already captured test output", "workflow and changelog update", "review handoff"]
  unauthorized_scope: ["Luna-13G", "architecture promotion", "corrective implementation", "rerunning the frozen experiment"]
  controls: ["role permutation/blinding", "semantic-role relabeling", "runtime provenance", "one-slot competition", "freeze", "chronology", "budget", "equalization", "no-evidence", "shuffle", "reverse timing", "uniform intervals", "neutral decay", "mirroring", "relabeling", "candidate order", "future mutation", "label isolation", "preservation"]
  measurements: ["repository provenance", "schedule dependencies", "runtime observations", "policy scores", "candidate mapping", "capacity legality", "artifact chronology", "audit not-run items", "reported regression counts"]
  information_boundary_check: ["FAILED: the schedule text is neutral, but G/H and base topology are still constructed from beneficial_role/harmful_role; the reported audit checks only _schedule and misses this dependency."]
  hardware_mapping: ["CPU-only review; no hardware equivalence claim"]
  architecture_invariants_touched: ["A01", "A02", "A04", "A07", "A08", "A14", "A15"]
  preserves: ["A01-A15 and ACP status unchanged", "no Luna-13G creation, execution or authorization", "no architecture rewrite"]
  architecture_change: false
  proposal: null
  files_changed: ["workflow/docs/luna/LUNA_WORKFLOW.md", "workflow/ARCHITECTURE_CHANGELOG.md", "workflow/handoffs/luna-0-review-Luna-13F-corrective.md"]
  tests_added: []
  tests_passing: ["Committed focused output: 10 passed", "Committed reported preservation output: 62 passed", "Committed reported full CPU output: 286 passed, 1 skipped", "Repository provenance: HEAD == origin/main"]
  tests_failed: ["Independent review: fixture/oracle contamination confirmed", "Independent review: required blinding and several controls not executed or invalid"]
  tests_not_run: ["No experiment rerun after user froze execution", "editor diagnostics", "CUDA/GPU/FPGA/FPAA and hardware equivalence"]
  assumptions: ["The committed revision and artifacts are the review target; no uncommitted implementation changes are accepted as evidence."]
  unresolved: ["Whether a genuinely blinded neutral schedule selects a useful candidate remains unknown."]
  recommended_next_agent: ["A separately authorized corrective Luna-13F execution, then another Luna-0 review; no Luna-13G"]
```

## Verdict

**BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION**

The corrected commit is synchronized and reproducible as a repository state, but
its PASS claim is not independently valid. The schedule body no longer reads
`beneficial_role` or `harmful_role`, yet `_candidate_edges()` maps `G` to
`config.beneficial_role`, `_base_edges()` uses the same mapping, and held-out
edge construction also uses those helpers. Thus the neutral temporal motif is
assigned to the endpoint already designated as useful by the fixture. A true
A/B permutation before runtime evidence generation was not performed.

The independent review does not authorize, create or execute Luna-13G.

## Provenance

| Item | Observed value |
|---|---|
| Branch | `main` |
| HEAD | `dcee582fa8fb347f578793c2ef383bd936e83234` |
| `origin/main` | `dcee582fa8fb347f578793c2ef383bd936e83234` |
| Worktree at review start | clean |
| Corrected implementation revision named by request | `dcee582fa8fb347f578793c2ef383bd936e83234` |
| Artifact provenance fields | `3379403a8b58649a85c2604ba3044e55e4fe99e9` |
| Contract | version 1.1 |
| Architecture change | none; no ACP |

The artifact provenance does not identify the committed corrected revision as
its executed revision. This is a provenance inconsistency that prevents a clean
artifact-to-source claim even though the current tree is synchronized.

## Review Matrix

| Area | Independent attack | Result | Status | Limitation |
|---|---|---|---|---|
| Schedule neutrality | Inspect all callers and mappings | `_schedule` is role-text neutral, but candidate/topology mapping is not | **FAIL** | Utility knowledge moved outside `_schedule` |
| Role permutation/blinding | Swap neutral A/B identities before evidence | Not run | **REQUIRED BUT MISSING** | No frozen A/B mapping independent of G/H |
| Runtime evidence provenance | Reconstruct artifact observations | Four short relay associations produce 4.0; noise produces 0.0 | **OBSERVED** | Mechanically runtime-generated, fixture-authored exposure |
| Evidence ownership/bounds | Inspect policy and artifact bounds | Source-local policy, capacity 2, history 8, score bound 8 | **PASS LIMITED** | Offline provenance is detailed; live freeze is not demonstrated |
| Canonical scorer | Trace `_admit` | Frozen `CandidateEvidence` is passed to the unchanged controller | **PASS LIMITED** | It scores contaminated evidence |
| One-slot competition | Inspect capacity and legality | Two legal candidates, one free slot, loser rejected by edge capacity | **PASS** | Does not cure oracle assignment |
| Decision freeze | Future mutation attack | Existing committed audit appends events, but its `all_appended_after_original_decision` is false; no real post-freeze phase is demonstrated | **FAIL** | Slice-based evidence partition is not a live freeze proof |
| Held-out chronology | Compare artifact fields and route traces | Metadata says 20.0 after 19.0, but route traces reset at 0.0 and timestamps are hard-coded | **NOT ESTABLISHED** | Actual cross-phase chronology is not independently proven |
| Budget exhaustion | Inspect committed audit and focused output | Incomplete budget is rejected by `_admit` | **PASS** | Only the committed output was used; no rerun here |
| Equalization | Inspect artifact | 2.0/2.0 tie | **PASS LIMITED** | Tie control does not test blinding |
| No-evidence control | Inspect artifact | Two zero-score candidates remain; deterministic selection occurs | **PASS LIMITED** | No-evidence does not remove role-keyed G/H mapping |
| Shuffle | Inspect artifact | Reported control exists | **NOT VALIDATING** | Role mapping remains contaminated |
| Reverse timing | Inspect artifact | Reported control exists | **NOT VALIDATING** | Same contamination boundary |
| Uniform intervals | Inspect artifact | Reported control exists | **NOT VALIDATING** | Count/association behavior is not isolated from endpoint mapping |
| Neutral decay | Audit marks not run | TPCNNeuron has decay, but score uses count policy | **REQUIRED BUT MISSING** | The contract explicitly requested a valid neutral/zero-decay control |
| Mirroring | Inspect implementation | Motif is swapped by explicit role convention; no blinded endpoint remap | **REQUIRED BUT MISSING** | Preference following a scripted mirror is not independent |
| Relabeling | Inspect committed test/control | Node IDs are changed but semantic role fields remain | **NOT VALIDATING** | Endpoint identity and utility designation were not independently permuted |
| Candidate order | Inspect artifact | Reverse presentation retains relay score winner | **PASS LIMITED** | Order independence is shown only after contaminated scoring |
| Future exclusion | Inspect control and slicing | Future control event can be included in the first 16 events; audit mutation is not actually post-decision | **FAIL** | Historical snapshot is asserted, not exercised |
| Label isolation | Audit item not run | No external-label mutation attack | **REQUIRED BUT MISSING** | Mandatory for this outcome |
| Locality attack | Audit item not run | No independent cross-candidate private-state attack | **REQUIRED BUT MISSING** | Mandatory for local-evidence claim |
| Candidate capacity/reset/eviction | Audit item not run | Not exercised beyond nominal capacity | **REQUIRED BUT MISSING** | Bounds are documented, lifecycle behavior is not demonstrated |
| Held-out utility | Inspect artifact | G 2/2, H 1/2, no-growth 2/2 | **OBSERVED** | Supports harmful-growth avoidance only, not improvement |
| Resource comparison | Inspect artifact | no-growth 8 events/8.0 proxy; G 12 events/12.0 proxy | **OBSERVED** | No resource benefit; proxy is uncalibrated |
| Artifact reproduction | Inspect provenance and files | Artifact says executed revision 3379403, while target commit is dcee582 | **FAIL** | Revision identity is stale/inconsistent |
| Preservation | Use committed reported counts | 62 preservation, 286 full CPU, 1 skipped | **REPORTED** | No rerun after the freeze instruction |
| Workflow update | This review | New blocked review entry added | **PASS** | Requires publication/commit by normal repository process |

## Mechanism behind 4.0 / 0.0

**OBSERVED:** `TemporalAssociationPolicy` increments a source-local candidate
score when a candidate observation follows a source anchor inside the 2.0
association window. Relay receives four such short associations; noise receives
four observations separated beyond that window. The difference is therefore
primarily association-count evidence, not neuron decay, eligibility, prediction
error, or held-out utility. Calling it general temporal discrimination would be
an overclaim.

## Five not-run audit items

| Audit item | Contract requirement | Classification | Reason |
|---|---|---|---|
| `external_label_mutation` | Labels must not alter pre-admission computation or decision | **REQUIRED BUT MISSING** | Explicitly required by the 13F contract; “count scorer” is not a waiver |
| `locality_attack` | Candidate evidence must use only permitted local information | **REQUIRED BUT MISSING** | No attack was executed |
| `neutral_decay_runtime_sweep` | Run valid neutral/zero-decay control where runtime decay exists | **REQUIRED BUT MISSING** | The neuron exposes decay; score indirection does not make the requested control unnecessary |
| `candidate_saturation_reset_eviction` | Demonstrate bounded candidate lifecycle and reset/eviction semantics | **REQUIRED BUT MISSING** | Nominal capacity is not a saturation/lifecycle test |
| `valid_mirrored_roles` | Mirror the causal motif without using utility identity | **REQUIRED BUT MISSING** | Existing mirror is role-scripted and therefore invalid for neutrality |

All five are required for the claimed runtime/locality outcome. The audit's
`13 passed, 0 failed, 5 not run` total therefore cannot support a scientific
PASS. The prior `5 passed, 8 failed, 5 not run` matrix was not repaired by a
complete independent re-execution; several checks were reclassified or tested
against only `_schedule`.

## Interpretation and boundary

The strongest supported statement is: this controlled fixture can produce a
bounded source-local association count and the unchanged scorer can select the
endpoint receiving the short-association motif. It does **not** establish
utility-independent candidate discrimination, autonomous training experience,
general utility prediction, task improvement over no-growth, resource
improvement, scalability, hardware equivalence or biological equivalence.

No architecture change is required by the evidence reviewed here. The failure
is experimental/provenance control failure. A later corrective execution may be
eligible only after explicit project-owner authorization under the existing
13F contract and must return to Luna-0. Luna-13G remains unauthorized.

## Validation record

| Command or procedure | Result |
|---|---|
| `git fetch origin` and provenance inspection | Completed; `HEAD == origin/main` at dcee582 |
| Committed focused output | 10 passed, already captured before the freeze instruction |
| Committed audit artifact | 13 passed, 0 failed, 5 not run, but independent review rejects its neutrality check |
| Reported preservation/full CPU output | 62 passed; 286 passed, 1 skipped |
| Experiment rerun | Not run after user instruction; frozen |
| Editor diagnostics and hardware checks | Not run / non-gating for this CPU review |

## Next assignment

A separately authorized Luna-13F corrective execution must remove the
beneficial/harmful mapping from candidate and topology construction, freeze and
record a real pre-admission phase, run true A/B blinding and all mandatory
controls, regenerate artifacts with the actual committed revision, and return
to Luna-0. No Luna-13G contract, implementation or execution is authorized.
