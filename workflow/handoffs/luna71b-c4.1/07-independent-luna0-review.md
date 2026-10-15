# Luna-71B-C4.1 Independent Luna-0 Review

**Reviewer:** Luna-0 Architecture Guardian  
**Review type:** Independent, read-only documentary/adversarial review  
**Reviewed repository baseline:** `54315aa8ac9340233c19d14f720eae771639fdea`  
**Final verdict:** `PASS WITH LIMITATIONS`

## Review history and preserved findings

| Round | Verdict | Finding | Correction recorded |
|---|---|---|---|
| Initial review | CORRECTION REQUIRED | Pair-level branch labels mixed measured zero, unexercised, and unavailable evidence; missing evidence could be mistaken for non-occurrence. | `02`, `03`, and `05` now define separate per-side states and pair outcomes, including one-sided occurrence and evidence-unavailable cases. |
| Initial review | CORRECTION REQUIRED | P11 overflow/failure stop did not define the triggering record, paired-side treatment, or disposition when stopping prevented bilateral comparison. | `02` and `05` now require pre-stop trigger evidence, actual terminal state, no inferred failure/zero, and explicit incomplete versus contradicted outcomes. |
| Initial review | CORRECTION REQUIRED | Full-split hash source attribution was incorrect; readiness wording implied completion before review. | `04` attributes full-split values to the hashed preparation plan and R6 result; `06` reports contractual status only after review while preserving partial capture readiness. |
| Follow-up | CORRECTION REQUIRED | "Same comparison boundary" was not operationally defined; a stopped counterpart could not prove a future matching event would not occur. | `02` and `05` define the exact P02 alignment tuple, immediate paired stop, actual terminal states, and `EVIDENCE_UNAVAILABLE` unless the counterpart's matching admission is already recorded. |
| Follow-up | CORRECTION REQUIRED | The P11 alignment tuple and successful admission outcome were not explicit in the trace schema. Review also noted non-ASCII rendering and inconsistent readiness status. | `05` adds `exposure_id`, full required anchor fields, and typed `admission_outcome`; `01` uses ASCII punctuation; `06` records the reviewed contractual status consistently. |
| Final review | PASS WITH LIMITATIONS | P11 schema and stop boundary now provide an unambiguous documentary test; no remaining material ambiguity was identified. | The final review pass is recorded below; source-capture and execution limitations remain. |

The successive findings and corrections are preserved; none are deleted or
recast as if the first draft had passed. Luna-0 independently confirmed the
final branch distinctions, exact P11 anchor/outcome, source-identity
attribution, and the revised readiness disposition.

## Exact candidate bytes reviewed

The final candidate files 01-06 below were read and hashed by the reviewer.
These are the exact bytes reviewed for the final PASS WITH LIMITATIONS
verdict:

| File | Bytes | Raw SHA-256 |
|---|---:|---|
| `01-historical-provenance-recovery.md` | 4,536 | `931ab5f3cc5b3927d3355c7d9ae013a44efd811a701872ff4b9fbf6d711ed20d` |
| `02-ppc11-reconstituted-contract.md` | 11,695 | `9885947c48dd464646e4291695ff949543eb3a45187eb742cf3d7a7c45e8b1d0` |
| `03-p01-p11-capture-requirement-matrix.md` | 4,363 | `791e0c91513880b2b1973aca9c9a46875c74451e62d914ce43e4a629c130ab82` |
| `04-source-identity-inventory.md` | 7,594 | `bd3228983268274f994b9d4330f5078b3f2824598e53afea1c30920070525e30` |
| `05-paired-trace-schema-and-comparison.md` | 9,564 | `65057cecc9b8913752d5479544651724554da9842abd0c80a22ee7f29f9f3073` |
| `06-c4-implementation-readiness.md` | 3,874 | `00109be7e8d9d4175d5634c830fbbba75a6ff40a2c3e084607897907c9fd2430` |

After the PASS WITH LIMITATIONS review, the reviewer requested only that the
PPC-11 requirements row in `06` be aligned with the already-reviewed opening
disposition and contract-completeness row. The integrator made that
disposition-only correction, and Luna-0 confirmed the revised `06` above
(3,874 bytes, SHA-256
`00109be7e8d9d4175d5634c830fbbba75a6ff40a2c3e084607897907c9fd2430`) was
consistent with its verdict. No other candidate content changed in that
final confirmation.

## Scope and limits

Verified by this review:

- Owner documentary-only authorization boundary.
- C3.1 exact-hash recovery and preservation of its historical limitations.
- All eleven comparison requirements and exact acceptance policy.
- Per-side branch evidence and pair-outcome distinctions.
- P11 alignment tuple, completed admission outcome, stop boundary, and
  unavailable-versus-contradicted disposition.
- C3.1 P01/P04/P05/P10 source-level READY and seven remaining capture gaps.
- Dataset/parameter identity limitations, trace independence, projection,
  stop conditions, and reporting requirements.

The review does not establish source readiness, bilateral trace production,
parity, efficacy, architecture promotion, execution authority, or historical
source-to-run lineage. The historical Luna-71A package remains unavailable.
The nine previously unexercised branches remain `UNEXERCISED / NOT_EVIDENCED`.

No files were edited by the reviewer. No source changes, driver, model,
training, inference, model-behavior test, trace, paired pilot, or other neural
execution occurred.
