# Luna-0 Final Independent Closure Review: Luna-13F

**BLOCKED - CONTRACT AUDIT INVALID**

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-13F final independent closure review"
  descriptive_name: "Final independent review of runtime-generated local candidate evidence"
  task_id: luna-0-final-closure-review-runtime-generated-local-candidate-evidence-13f
  component: "CPU Luna-13F implementation, controls, artifacts and workflow"
  status: blocked
  contract_version: "1.1"
  branch: main
  base_revision: 2b2432dabd49ecacceef525e8e3e68b909ee09c3
  result_revision: "uncommitted review"
  tree_hash_at_review_start: 033061d3bd647f1806bbcb43bb1e20c0e278fd6c
  head_equals_origin_main: true
  worktree_at_review_start: clean
  implementation_revision_reviewed: 72b6201d6a2793b0bab099df7418aa66904501a1
  artifact_generating_revision: b5815f90522c1704731037c5d5fd1bface264565
  architecture_change: false
  proposal: null
  luna_13g: unauthorized
```

## Independent result

| Mapping | Selected candidate | Evidence scores | Held-out result |
|---|---|---|---|
| P0 | `candidate_A` | relay `4.0`, noise `0.0` | `2/2` |
| P1 | `candidate_A` | noise `4.0`, relay `0.0` | `1/2` |

Both candidates are individually legal and compete for one relevant free edge
slot. The unchanged canonical scorer ranks the higher source-local runtime
association count first. This is a valid negative observation, not a closed
experiment.

## Closure matrix

| Area | Independent finding | Status |
|---|---|---|
| Blinding and mappings | Neutral candidate mappings reproduce P0/P1; no role field is in the 13F configuration | PASS, fixture-scoped |
| Runtime evidence provenance | Event ID/type, source/destination, time, owner, local state and score updates are recorded before decision | PASS |
| Evidence mechanism | Four short source-local associations produce the score; decay leaves score/rank unchanged | PASS, count-based |
| Canonical scorer | Frozen evidence reaches `StructuralPlasticityController`; order reversal preserves the winner | PASS |
| One-slot competition | Two legal candidates, one slot, loser rejected by edge capacity | PASS |
| Chronology | The attack is a timestamp predicate rather than runtime event injection | FAIL |
| Future exclusion | The declared future event is removed by `events[:16]` and never appears in the executed trace | FAIL |
| External-label mutation | Mutated evaluations run and semantic pre-admission fields remain equal; some equality fields are tautological | PASS, limited |
| Locality | Metadata is passed to a parameter the runtime evidence path does not read; no prohibited-state mutation executes | FAIL |
| Lifecycle bounds | Capacity rejection, reset, stale-state reuse and bounded candidate state reproduce | PASS |
| Budget boundary | B-1, B, B+1 and large budget records are stable | PASS |
| Equalization and mirroring | Equal exposure ties; mirrored motif moves preference | PASS, fixture-scoped |
| Regression | Focused, preservation, full CPU, compile and diff checks pass | PASS |
| Contract audit | Artifact reports `26 PASS, 0 FAIL, 2 N/A`, but three PASS claims are not executed evidence | INVALID |

## N/A classifications

1. `candidate_expiry`: **VALID NOT APPLICABLE**. The canonical
   `TemporalAssociationPolicy` has no expiry mechanism; state is retained until
   reset or decision freeze, so the triggering condition is absent.
2. `candidate_eviction`: **VALID NOT APPLICABLE**. The canonical policy does
   not evict at capacity; it records deterministic rejection, so the triggering
   condition is absent.

These legitimate N/A classifications do not cure the invalid PASS entries.

## Resource and proposition findings

No-growth remains `2/2`, 8 events and `8.0` uncalibrated
`activity-cost-proxy` units. Selected P0 growth remains `2/2`, 12 events and
`12.0` units. There is no task improvement, resource benefit or general growth
superiority. P1 shows that the higher runtime score can select harmful growth.

- Proposition 1: **SUPPORTED IN TESTED FIXTURE**. Runtime events generate
  bounded source-local candidate-specific count evidence.
- Proposition 2: **SUPPORTED IN TESTED FIXTURE**. That evidence changes the
  unchanged canonical one-slot admission decision.
- Proposition 3: **NOT SUPPORTED**. The evidence-driven selection does not
  reliably predict useful held-out growth across P0/P1.

## Validation actually performed

| Command or procedure | Result |
|---|---|
| `python -m pytest tests/test_luna13f_runtime_generated_evidence.py -q` | `13 passed` |
| Preservation matrix: Luna-13E, 13D, 13C, 13B, 12H, 12N, 11 | `72 passed` |
| `python -m pytest -q` | `289 passed, 1 skipped` |
| `python -m compileall -q tpcn run_runtime_generated_evidence_13f.py tests` | passed |
| `git diff --check` | passed before this review edit |
| Clean regeneration from `2b2432dabd49ecacceef525e8e3e68b909ee09c3` | P0/P1 reproduced |

Editor diagnostics were unavailable through command validation. CUDA, GPU,
FPGA, FPAA and hardware-equivalence checks are out of scope and non-gating.

## Architecture and next boundary

No A01-A15 modification or ACP is required. The experiment only shows that the
tested count-based runtime signal is insufficient as a general usefulness
predictor. No successor mechanism is proposed or authorized.

Final disposition: **BLOCKED - CONTRACT AUDIT INVALID**. Luna-13F is not
closed, and Luna-13G remains unauthorized. Any future control repair requires
a separate explicit assignment and another independent Luna-0 review.