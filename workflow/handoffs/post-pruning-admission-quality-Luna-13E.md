# Luna-13E Execution Handoff

## Status

**PASS — PRE-ADMISSION EVIDENCE DISTINGUISHES BENEFICIAL FROM HARMFUL GROWTH, READY FOR LUNA-0 REVIEW**

This is a CPU-only experiment result for the declared fixture. It does not generalize beyond the fixture, change A01-A15, authorize an architecture change, or authorize Luna-13F.

## Provenance

- Starting/baseline revision: `455386746cbb1b0c46d61f507c3750a7780b9b30`
- Executed implementation revision: `f5b84ee67517294ddba377d4933359eacc9688d3`
- Branch: `main`
- Worktree at artifact generation: dirty only because the newly generated artifact directory was untracked; unrelated changes were preserved.
- Environment: Windows 10, Python 3.10.8
- Fixture: `luna-13e-post-pruning-admission-v1`
- Artifacts: [results.json](../../artifacts/post-pruning-admission-13e/results.json), [summary.json](../../artifacts/post-pruning-admission-13e/summary.json)

## Stage A Reference Reproduction

**OBSERVED.** The corrected Luna-13D reference was reproduced before policy comparison:

| Policy/control | Chosen candidate | Task result | Events | Proxy energy | Latency | Completion |
|---|---:|---:|---:|---:|---|---|
| Baseline/post-pruning | none | 2/2 | 8 | 8.0 | recorded per case | completed |
| Harmful post-growth | harmful relay | 1/2 | 16 | 16.0 | long case arrives at 1.0 instead of 3.0 | completed |

The diagnostic trace records target arrivals `(1.0, 1.0, 4.0, 4.0)` in the harmful long case. The duplicate direct/relay arrivals make the long case `on_time`, while the frozen external target is `late`. This is the observed task degradation mechanism. Prediction/error records were empty in this fixture; no unavailable prediction signal was invented.

## Frozen Competition

**OBSERVED.** One newly freed relevant structural slot was available. G and H were each individually legal against the same post-pruning topology and finite fan-in/out limits. The candidates were deliberately constructed before policy comparison; beneficial/harmful roles were used only for external held-out evaluation.

| Candidate | Temporal evidence | Utility/reward evidence | Cost evidence | Score | Rank | Admitted | Held-out task |
|---|---|---|---|---:|---:|---|---|
| G | three bounded local short-interval observations | none available | propagation delay available; no predicted total path cost | 3.0 | 1 | yes | 2/2 |
| H | one bounded local long-interval observation | none available | propagation delay available; no predicted total path cost | 0.0 | 2 | no | 1/2 |

Both candidate evaluations completed with 12 processed events and proxy energy 12.0. The selected G graph has one additional `source -> relay` edge and graph fingerprint `9136c83c7ef4e818f986385172e86be2ba06a93e3bd82cf9212c29bead114831`.

The canonical current policy selected G. It used `CandidateEvidence.score`, with source/destination/evidence ID only providing deterministic ordering. It did not receive the held-out target, beneficial/harmful flag, endpoint-role table, or post-admission traffic.

## Field-Level Provenance

| Field | Candidate | Source/owner | Available time | Decision time | Local | Bounded | Pre-admission | Future/label/identity dependent |
|---|---|---|---|---|---:|---:|---:|---|
| temporal observations | G/H | source-local controlled fixture evidence | before admission | admission selection | yes | yes | yes | no/no/no |
| `CandidateEvidence.score` | G/H | structural plasticity candidate evidence | before admission | admission selection | yes | yes | yes | no/no/no |
| propagation delay | G/H | candidate edge metadata | before admission | available but not used in canonical score | yes | yes | yes | no/no/no |
| held-out task result | G/H | external evaluator | after admission | not available | no | bounded per run | no | future/label dependent |
| post-admission route traffic | G/H | runtime execution | after admission | not available | no | bounded per run | no | future dependent |
| endpoint role/name | G/H | fixture construction only | not supplied to scorer | not used | no | bounded | no | identity dependent if used |
| reward/eligibility | G/H | existing architecture | unavailable in this fixture | not used | n/a | n/a | no | no |

The score was computed from bounded source-local temporal evidence. No future event was delivered before the decision. Future delivery after the decision left score, rank, admission, and graph fingerprint unchanged. Mutating external labels changed only evaluator labels, not runtime input or admission.

## Controls

**OBSERVED.**

- Relabeling preserved the G preference and `2/2` held-out result.
- Mirrored roles preserved the G preference and `2/2` held-out result.
- Evidence-equalized candidates both scored `1.0`; H was selected by deterministic tie-breaking, not utility discrimination, and its result was `1/2`.
- Label mutation preserved G score, rank, admission, and graph; mutated external targets were `late`, `on_time`.
- Future events delivered after selection preserved score, rank, admission, and graph.
- The fixed/no-growth Stage A condition outperformed harmful post-growth: `2/2` versus `1/2`. In the one-slot competition fixture, fixed/no-growth itself was `1/2`, with 4 events and proxy energy 4.0; this difference is recorded rather than conflated with the Stage A reference.
- Random controls used independent seeds `0..4`. Results were recorded per seed in `results.json`; this small matrix is not a broad random-policy claim.
- All runs completed within bounded event and queue budgets. No run was treated as evidence when budget-exhausted.

## Architecture Boundary

**OBSERVED.** The current admission path has no score threshold, confidence threshold, abstention, utility memory, predicted-cost model, probation edge, rollback, or reward-aware admission channel. A negative-score candidate can still grow when selected. This is an architecture limitation, not a missing experiment flag.

**INFERRED.** For this deliberately controlled fixture, existing local temporal evidence was sufficient to distinguish the beneficial candidate from the harmful candidate before structural mutation.

**HYPOTHESIZED.** General tasks may require additional authorized local evidence because this fixture does not establish utility prediction, resource-cost prediction, or reliable discrimination under arbitrary candidate distributions.

No production utility-aware admission mechanism was added. No architecture-change packet is required for the narrow fixture result; a future proposal for general utility-aware admission would require a separate ACP and Luna-0 authorization.

## Required Questions

1. **What caused harmful Luna-13D growth?** Duplicate direct/relay arrivals changed the long case from `late` to `on_time`.
2. **What beneficial candidate was used, and were both legal?** G was the `source -> relay` candidate; G and H were both individually legal.
3. **Exactly one free slot?** Yes, one relevant free slot.
4. **What evidence existed before admission?** Bounded source-local temporal observations, candidate score, and propagation-delay metadata. Only score affected canonical ranking.
5. **Did current policy choose G, H, tie, or neither?** G.
6. **Did preference survive relabeling and mirrored roles?** Yes, in this fixture.
7. **Did label mutation leave admission unchanged and future events stay excluded?** Yes.
8. **Could local evidence predict usefulness or resource cost?** It predicted the tested fixture’s task usefulness; it did not establish general usefulness or cost prediction. Propagation delay was available but not scored.
9. **Did no-growth outperform harmful growth?** Yes in the reproduced Luna-13D Stage A reference, `2/2` versus `1/2`.
10. **Does current architecture permit abstention?** No.
11. **Is an architecture change necessary for reliable beneficial admission?** Not for this fixture-bound result; likely required for a general utility-aware guarantee, which remains unproven and unauthorized here.
12. **What claim is supported?** Under this tested post-pruning one-slot fixture, valid bounded local pre-admission temporal evidence distinguished G from H and the selected admission preserved the fixed task. Nothing broader is supported.

## Validation

Passed:

- `python -m pytest tests/test_luna13e_post_pruning_admission.py -q` -> 10 passed
- `python -m pytest tests/test_luna13e_post_pruning_admission.py tests/test_luna13d_finite_resource.py -q` -> 20 passed
- Python compilation for the new runner, experiment module, and focused tests
- `git diff --check`

Not yet run in this handoff: the full CPU suite and the broader Luna-13B, Luna-13C, Luna-12H, Luna-12N, Stage-0, static diagnostics, and repository-wide regression matrix. CUDA remains optional and non-gating. Luna-13F was not executed, created, or authorized.

Return this handoff and the linked artifacts to Luna-0 for independent review.
