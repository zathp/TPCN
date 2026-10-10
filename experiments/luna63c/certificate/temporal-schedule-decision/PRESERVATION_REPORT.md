# Luna-63C artifact preservation and reconciliation report

**Source:** `experiment/luna63c-stage-a-certificate` at `19caa49d7620062c06ad74d19528e47725f86b37`; source tracking branch was at the same revision. No staged changes were present before reconciliation. The original checkout contains two prior-turn tracked workflow edits and the untracked artifacts listed in the local `ARTIFACT_RECONCILIATION.json` snapshot. Its workstation-root paths are redacted in the sanitized publication view.

## Preservation findings

- Three sibling lane worktrees (W, T, E) are clean at the exact published commits; the Luna-63C design worktree is at `a303ebb835b72fdd01c86df478431b8638aacbb4`.
- The **parent checkout's** untracked W/T/E trees and handoffs are not byte-identical to their named remote lane commits. Parent W: none of its 11 visible files matched the same published path/blob; its local manifest expectations disagree for `INVENTORY.md`, `README.md`, and the W handoff. Parent T: 6 files are absent and 4 same-path files differ from the published T tree. Parent E: 7 files are absent and its manifest differs. The three parent handoffs differ from their published versions. These files are classified **F — uncertain provenance**, retained unchanged, and excluded from authoritative publication.
- The ignored W `.engine` directory contains 26 files (4,049,892 bytes). It remains untouched and excluded. The five native DLL hashes referenced by the local E manifest match the local binaries exactly; this does not attest vendor provenance or certify N4.
- The existing fixture/W/T/E branch references and commits were fetched/verified. Published T reports 191/9/182 and contains a complete 191-row semantic-ID crosswalk, including 119 C7 identities and the nine certified event IDs. The parent-checkout T copy is a different, untracked artifact and was not used as authority.
- Two tracked workflow documents and the corrected decision package, identity-level blocker inventory, schedule-completion contract, and handoff are draft governance artifacts. They may be published only after independent review. They do not constitute scientific certification or authorize T execution.

## Disposition

Publish only the reviewed decision-preparation/governance set on the dedicated governance branch. The sanitized `PUBLICATION_ARTIFACT_RECONCILIATION.json` records relative artifact paths, raw SHA-256 values, sizes, tracking states, same-path blob comparisons, and disposition. The original `ARTIFACT_RECONCILIATION.json`, with local worktree roots, remains in the parent checkout and is not published. Do not stage, copy, delete, regenerate, or rewrite the untracked W/T/E copies, lane handoffs, or ignored `.engine` files. Preserve the source checkout and all sibling worktrees.

## Excluded work and authority limits

No W/T/E checker or test was rerun; no numerical calculation, fixture execution, T correction, E re-audit, Lane S/N5, N6, Stage B, or LTRD experiment ran. W remains scoped to its reported witness rows, T remains blocked at N3, all applicable N4-A audit obligations pass (N4-A evidence audited, not candidate implementation certification), N4-B remains incomplete, and overall N4 is not closed. Global N1/N3/N4 closure is not established. LTRD is a separate candidate future experimental pathway only.
