# Independent Luna-0 final adjudication

Reviewer: separate agent `/root/luna0_update_matched_review`, 2026-10-21.

**Publication adjudication: PASS.** The frozen experiment was executed and reported faithfully enough to commit and push this synthetic research packet. **Primary scientific improvement criterion: FAIL.** Publication approval must not be described as a positive method result, neural validation, E1 qualification, or production approval.

## Reviewed identities

| Artifact | SHA-256 |
| --- | --- |
| source-manifest.json | 6cf75309fa99c3928c1e5dd2815a40060d02909994e0b955548be394c329b1eb |
| results.json | e50dd8c8d94750525b40984d576cd0d3450c86d2e7ff293c8105a6e9cfc0abb1 |
| REPORT.md | 4d456084e83c02952b23ec63f03edabc1b51f988c25462d20e34d40ca362f7ae |
| summary.csv | b73bbf8e7f506b141469c667d07813bde5bf60ad62180aa46cba1d4c6ce435af |
| verification.json | 2412564c8a301c79ef95657f49ac529225c2f97a87394a870ba340b60dfe1c20 |
| SOURCE_REVIEW.md | 5fc705b0c99a8d4046f6a9d38e3f3ce6df2a1ecc852603570ec41a73e4f11db7 |

The five prospective source identities and lengths were independently verified again after execution and remain unchanged. See SOURCE_REVIEW.md for exact source/dependency identities and the independently executed 15 passing pre-run focused unit tests. The reviewer made no implementation or experimental-result edits and ran no additional training fits, matrix runs, replay fits, or arbiter choices. Independent analysis is retained in reviewer_audit.py and reviewer-audit-result.json; running that audit only reads archived evidence and recomputes arithmetic.

## Independent evidence checks

The complete 4-case × 8-seed × 6-arm grid contains exactly 192 unique rows. All 160 learning rows have exactly 111 accepted updates and no skipped update; 32 no-learning rows have zero. The reviewer independently checked all 17,760 update audit records against the supplied physical-time interval schedule, feedback delay, expected receipt IDs, exact last-256-receipt window, positive predictor variance, scheduled step, gradient bound, and resulting center update equation. Every final probability, final squared error, quantized positive weights summing to 1000, heldout frequency sanity statistic, pending-feedback count, and reported control/learning update total was checked. These archive checks cannot independently reconstruct raw losses or re-estimate every regression slope because the full per-observation loss stream is not retained; deterministic replays cover three prescribed complete rows.

All overall means and case means were independently recomputed from the 192 rows. The 24 summary CSV rows, including sample standard deviations and last-quarter means, agree with the result records. The report's displayed overall values agree after rounding. Primary ×8 wins three of four cases against both controls, but its overall error `0.00028891090188448227` exceeds the fixed oscillator's `0.00027070758344385553`. Therefore the frozen conjunction of overall and case-count criteria is false, correctly recorded. Exploratory ×4 is not substituted for the primary.

The three retained verification rows correspond exactly to primary ×8, seed 0, fast/delayed/target-shift. Their canonical row hashes match the archived matrix rows, including all update audits and heldout counts. The verification output pins the exact original results hash. This is exact same-implementation replay evidence, not an independent reimplementation of training.

The original counts are 393,216 plant observations and 49,152 heldout choices. Recorded cumulative counts including the three prescribed replays are 399,360 and 49,920, below the frozen 400,000 and 50,000 caps. The 1,758,467-byte result file is below the prospectively declared 4 MiB cap. The combined observed matrix time plus replay command duration is approximately 3.101 seconds, below 60 seconds. Source and report accurately distinguish separate wall guards from a single continuous guard. No future feedback flush or additional learning appears in the driver; pending counts agree with the exact delayed receipt schedule.

## Scope and release conditions

The report candidly describes the changed rolling estimator, moving centers, adaptive per-probe amplitude, phase/lag and endogenous-regressor bias, supplied toy time constants, correlated windows, target-shift staleness, and the absence of neural efficacy claims. The next suggested ×4 confirmation is new research requiring a new prospective test; it is not authorized by this review as an automatic continuation.

Commit/push approval applies to this reviewed packet under the intended versioned experiment directory, preserving these reviewed artifact bytes and the original sibling arbiter dependency. The author must generate a final manifest that inventories retained artifacts including these independent review artifacts, verify copied bytes and repository diff, and commit only the intended packet. This review does not authorize unrelated changes or alter the unresolved E1/R4/Luna-72B state. No blocking findings remain in this experiment packet.
