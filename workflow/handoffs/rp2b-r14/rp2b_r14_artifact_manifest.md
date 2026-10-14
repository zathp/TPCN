# RP-2B R14 — Artifact Manifest

**Package:** R14-A through R14-F, proof-obligation/owner-decision register,
and this manifest (**8 files total**).

The seven non-manifest artifacts are listed with exact byte counts and
SHA-256 identities. The manifest is the eighth package file; its own byte
count and SHA-256 are reported separately in the R14 completion response
because a manifest cannot embed its own final digest.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `rp2b_r14_a_all_path_resource_accounting.md` | 15,183 | `01E66E72D1813F4C31DD5FF76AE9014EBCE4104F0E4FDC39E2F7931D4291717F` |
| `rp2b_r14_b_terminal_admission_failure_matrix.md` | 11,953 | `A4A5FBD0131ACD1ED30DC331E45F37E9A56CDFC9338538EEC90E1B9627494A7B` |
| `rp2b_r14_c_po_interface_semantic_assessment.md` | 8,319 | `53D9B2B07E3C3D9F4EB6EF6D705EE899283195BFE326E53035B3FDC959E146DF` |
| `rp2b_r14_d_cross_lane_blockers.md` | 9,517 | `CA084971541B34DEEBFC84D5329E68728847089BF3F0C5DF81AE5F475686A30D` |
| `rp2b_r14_e_independent_adversarial_review.md` | 3,688 | `2CD8C9AEB154C26CBB9857F917DE95B80976D284D85E99F51A082881C8540932` |
| `rp2b_r14_f_luna0_final_adjudication.md` | 6,269 | `97B8F8EA179D63C9E2C5174DC822D5C56FCFBAF8CB7228A8D203BAF8D6C0321A` |
| `rp2b_r14_proof_obligation_owner_decision_register.md` | 6,807 | `E852EF00B7F17484151821F81CCDBBF9865E77CAE6663DADEEB0D510D1107D78` |
| `rp2b_r14_artifact_manifest.md` | Self-entry; identity reported separately | Self-entry; identity reported separately |

## Integrity note

R14-C's supplied SHA-256
`53D9B2B07E3C3D9F4EB6EF6D705EE899283195BFE326E53035B3FDC959E146DF`
matches the verified current bytes. Luna-0 initially misquoted the digest;
the resulting claimed mismatch was corrected and is not an artifact defect.

## Scope and status

This manifest covers session-state documentary artifacts only. It does not
claim source changes, capacity fit, implementation authority, qualification,
execution authorization, or publication. RP-2B remains BLOCKED / BOUND
INCOMPLETE.
