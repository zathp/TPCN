# Luna-12N Corrective Addendum - 2026-09-29

This addendum corrects measurement, replay-status, accounting and provenance defects in the existing Luna-12N experiment. It remains Luna-12N, CPU-compatible, and does not authorize Luna-13A or promote A14.

## Provenance

- Starting revision: `5c6a33ef773e6c417cf93e3289877455054e8dc3`
- Starting committed revision: `5c6a33ef773e6c417cf93e3289877455054e8dc3`.
- Ending reviewed revision before this independent review: `bea288aa6f2a7fb54755dc64a703160aaac6c41e`.
- The independent review found and corrected exact-budget completion reporting and order-sensitive admitted-edge comparison; the final review revision is recorded by the Luna-0 changelog entry.
- Initial worktree: clean on `main`; corrective edits are the files listed below.
- Corrected artifact: `artifacts/temporal-direction-12n-corrective-20260929/`
- Artifact patch hash: recorded as `patch_diff_hash` in `config.json`.
- Runtime: Python 3.10.8 on Windows; seeds `0,1,2,3,4`; decay rates `0.25,0.5,1.0`; policies `current`, `reversed`, `decay`, `reversed_decay`, `random`, `fixed`; fixture `luna-12n-competing-candidates-v2`; event budget `16`.

## Changed Files

- `tpcn/temporal_direction.py`
- `tests/test_luna12n_temporal_direction.py`
- `run_temporal_direction.py`
- `artifacts/temporal-direction-12n-corrective-20260929/`
- This corrective addendum.

## Corrected Schema

Each result now separates configured candidate opportunities and mutation budget from actual candidate evaluations, mutation attempts, accepted mutations, rejected mutations and used mutations. Fixed topology reports zero actual evaluations, attempts and acceptances.

Replay records include configured event budget, processed events, pending events, `completed` versus `budget_exhausted`, and termination reason. Static minimum-hop count and positive-delay minimum cumulative transport delay are separate. First target arrival and arrival latency are extracted from replayed event timestamps, not copied from graph delay.

A metadata negative control executes an independent replay under a different phase label and compares normalized trace, target arrivals, target states, internal prediction/error measurements and termination evidence. The control does not compare phase labels. Candidate records identify `synthetic_fixture_timing` or `fallback_fixture_value`; these are controlled fixture inputs, not online learned evidence.

Graph state labels distinguish `baseline`, `post_mutation`, and `post_removal`. The intervention is labeled `shortcut_present_vs_shortcut_removed`, not baseline restoration. Paired decay summaries separately report score change, rank change, admitted-edge change and final-graph change.

## Observed Results

- Full corrected suite: 90 records in the versioned artifact.
- Fixed summary: 90 configured candidate opportunities, 45 configured mutation-budget units, 0 candidate evaluations, 0 mutation attempts, 0 accepted mutations, 0 used mutations; 15 complete runs.
- Paired current versus decay: scores changed and ranks changed at all 15 seed/rate pairs; admitted edge sets did not change, although accepted-edge order changed in some records; final post-mutation graph fingerprints did not change.
- Candidate evidence is synthetic fixture timing/fallback data, not causally observed online learning.
- Target arrivals are replay-measured event timestamps.
- Cumulative-delay paths use a positive-weight Dijkstra calculation; minimum hop count is reported separately.
- Budget exhaustion is explicit and includes pending-event count; exact-boundary truncation with an empty queue is also `completed: false`. Deliberately insufficient budgets are diagnostic and are not silently treated as completed efficacy runs.
- Prediction loss is internal prediction-vs-activation error. Luna-12N has no common topology-independent external prediction target.
- Proxy energy remains a local activity proxy, not calibrated physical energy.

## Validation

- `python -m pytest -q tests/test_luna12n_temporal_direction.py`: 18 passed.
- `python -m pytest -q`: 222 passed, 1 skipped.
- `python -m compileall -q tpcn tests run_temporal_direction.py`: passed.
- `git diff --check`: passed.
- CUDA/GPU validation: optional and not required; the one existing skip is not a Luna-12N failure.

## Interpretation

**OBSERVED:** Decay alters candidate score magnitude and rank in this synthetic fixture. The paired result does not establish a final learned-graph difference. Fixed topology performs no growth operation. Replay truncation is visible. Arrival and path metrics are separately measured/reported.

**INFERRED:** The corrected records can distinguish configured opportunity from actual operation, static path properties from replay traffic/arrival evidence, and metadata invariance from a genuine independent control.

**HYPOTHESIZED:** None of these corrections demonstrates general temporal-learning superiority, decay-guided superiority, classification improvement, external predictive improvement, resource efficiency, or hardware equivalence.

## Required Answers

1. Decay alters score magnitude: **yes, observed in this fixture**.
2. Decay alters candidate rank: **yes, observed in this fixture**.
3. Decay alters admitted edge: **no, not when comparing admitted edge sets**.
4. Decay alters final graph: **no in the paired records**.
5. Candidate evidence: **synthetic fixture timing/fallback, not causally observed online evidence**.
6. Target arrivals: **yes, measured from replayed events**.
7. Cumulative-delay paths: **yes, delay-weighted; hop count is separate**.
8. Budget exhaustion: **yes**.
9. Exhaustion explicit: **yes, with pending count and reason**.
10. Exact reconstruction: **configuration, seeds, runtime, revision/tree and dirty/patch provenance are recorded**.
11. Common external prediction target: **no**.
12. Resource efficiency: **not demonstrated**.
13. General temporal-learning superiority: **not demonstrated**.

## Remaining Limitations

The fixture is synthetic and small. Internal prediction loss is topology-dependent. Replacement attribution, hardware equivalence and calibrated energy remain unavailable. Deterministic policy rows are not independent stochastic replications merely because seeds are repeated. No architecture contract or pruning semantics were changed.

**PASS WITH FOLLOW-UP — LUNA-12N CORRECTED, EFFICACY NOT ESTABLISHED**
