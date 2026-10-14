# RP-2B R14-F — Luna-0 Final Adjudication

**Overall disposition: PASS WITH FINDINGS — documentary adjudication only.**
**RP-2B remains BLOCKED.**

This package is accepted as the R14-F documentary result, not as proof of
capacity fit, implementation readiness, runtime qualification, execution
authorization, or publication approval.

## Adjudication by gate

| Gate | Disposition | Basis |
|---|---|---|
| Documentary integrity | **PASS** | Exact current SHA-256 values match the supplied identities for the six reviewed artifacts. |
| Artifact inventory | **PASS** | R14-A through R14-F and the proof-obligation/owner-decision register are present as the package deliverables. |
| Bounds | **BLOCKED** | R14-A does not establish complete all-attempt Low counts/bytes or complete all-path resource maxima. |
| Resource feasibility | **NOT ESTABLISHED** | Simultaneous copies, retained evidence, frozen-profile compatibility, and terminal reserve fit are not proven. This does not establish that fit is impossible. |
| Terminal semantics/admission | **BLOCKED** | Existing classifications are documented; terminal admission/reachability and new refusal outcomes are not established or adopted. |
| P/O interface completeness | **BLOCKED** | P/O remain candidate source locations; callers, producers, failure/cleanup paths, and ownership boundaries are not closed. |
| Semantic preservation | **NOT ESTABLISHED** | No frozen correction diff or old/new accepted-set and behavior comparison exists. |
| Source allowlist | **NOT AUTHORIZED** | No Category I allowlist is approved. |
| Implementation | **NOT AUTHORIZED** | No source or contract changes are authorized. |
| Testing | **NOT AUTHORIZED** | No tests were run, as required by scope. |
| Static verification | **PASS WITH FINDINGS** | Documentary contents and artifact identities were reviewed. Source-level static analysis or code-level verification was not run. |
| Execution | **NOT AUTHORIZED** | No imports, preflight, runtime, target invocation, or other execution occurred. |
| Publication | **NOT AUTHORIZED** | No repository publication is approved. |

## Reviewed artifact identities

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `rp2b_r14_a_all_path_resource_accounting.md` | 15,183 | `01E66E72D1813F4C31DD5FF76AE9014EBCE4104F0E4FDC39E2F7931D4291717F` |
| `rp2b_r14_b_terminal_admission_failure_matrix.md` | 11,953 | `A4A5FBD0131ACD1ED30DC331E45F37E9A56CDFC9338538EEC90E1B9627494A7B` |
| `rp2b_r14_c_po_interface_semantic_assessment.md` | 8,319 | `53D9B2B07E3C3D9F4EB6EF6D705EE899283195BFE326E53035B3FDC959E146DF` |
| `rp2b_r14_d_cross_lane_blockers.md` | 9,517 | `CA084971541B34DEEBFC84D5329E68728847089BF3F0C5DF81AE5F475686A30D` |
| `rp2b_r14_e_independent_adversarial_review.md` | 3,688 | `2CD8C9AEB154C26CBB9857F917DE95B80976D284D85E99F51A082881C8540932` |
| `rp2b_r14_proof_obligation_owner_decision_register.md` | 6,807 | `E852EF00B7F17484151821F81CCDBBF9865E77CAE6663DADEEB0D510D1107D78` |

Luna-0 initially misquoted the supplied R14-C digest and treated it as an
identity mismatch. On recheck, the supplied digest and current file digest
were confirmed identical. The initial misquotation is corrected here; there
is **no R14-C identity discrepancy**.

## Retained lane and review history

Preserve the prior findings without retroactively changing lane dispositions:

- **R14-A:** BLOCKED — BOUND INCOMPLETE.
- **R14-B:** PASS WITH FINDINGS — existing-result classification only.
- **R14-C:** BLOCKED — complete interface scope not established.
- **R14-D:** BLOCKED — independent technical gates remain open.
- **R14-E:** Retains both stages: initial **BLOCKED — CORRECTION REQUIRED**,
  followed by focused **PASS ON THE R14-E CORRECTIONS**. This focused pass
  closes only the listed documentary corrections, not the broader R14 gates.

The correction review distinguished candidate O's finalization behavior
from contract requirements; described report-write/final-in-process-verdict
divergence; qualified sole-sink failure claims; recorded direct alert-call
exception paths without guaranteeing continuation; and corrected R14-A's
R13 provenance reference. It does not authorize source repair or new result
semantics.

## Preserved uncertainty and classification

```text
frozen_total_max_bytes: null
proposed_total_max_bytes: null
proposed_headroom_bytes: null
N_LOW_all_attempt_max: unsupported
T_LOW_all_attempt_max_bytes: unsupported
```

Do not infer a numeric total, headroom, fit, reserve sufficiency, or
infeasibility. Preserve `RP2_UNKNOWN_FAIL_CLOSED` whenever required Low
cessation evidence is missing. An unadopted candidate-limit breach does not
automatically map to `RP2_FAIL`. An alert attempt is not proof of delivery,
observation, or durable evidence. An individual failed write alone does not
establish total sink unavailability.

Open proof obligations include the complete mandatory-family inventory;
whole-attempt Low count/byte/framing bounds; full-copy/recovery,
simultaneous-lifetime, and partial-write/prefix accounting; console,
operator, and governance-material boundaries; joint terminal-family maxima;
131,072-byte reserve sufficiency and admission reachability; frozen-profile
feasibility; complete P/O interfaces; semantic preservation; and independent
approval of any source allowlist. Phase 2A R2 does not supply Phase 2B
feasibility or authorization.

## Baseline and authority

The reviewed baseline was branch
`governance/luna64-r4.3-freeze-20261010` at
`f117ce51e7a805564e37252d3b5c99bda163ce57`. The repository had pre-existing
untracked paths; no repository files were changed. The expected
`tpcn-luna-workflow/...` paths are absent in this checkout; corresponding
governance documents under `workflow/...` were reviewed.

No ACP or architecture change is proposed. No tests, imports, compilation,
preflight, runtime, source or contract edits, staging, commit, push, merge,
or publication occurred. The manifest records this package's seven
non-manifest artifacts; its own SHA-256 is reported separately after
creation.

**R14-F disposition: PASS WITH FINDINGS — documentary only.**
**RP-2B: BLOCKED / BOUND INCOMPLETE.**
