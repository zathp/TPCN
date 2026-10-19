# WC1-A3 - Luna-0 independent final review

## Overall recommendation: PASS WITH FINDINGS

The WC1-A3 local preservation state passes the integrity checks reviewed. This
is not a completed off-machine backup or publication: no owner-authorized
destination was specified. Luna-0 made no changes.

| Criterion | Verdict | Evidence |
|---|---|---|
| Source identity, refs, and worktrees | PASS | HEAD is `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76` on `governance/luna71b-c4-1-ppc11-freeze`. Exactly three `refs/preservation/wc1-a3/*` refs point to the accepted commits; no ref exists for `430b60ed...`. Full strict fsck exited 0 for all three accepted commits. The rejected commit's strict fsck still reports missing tree `4b825dc...`; physical object enumeration does not list it. `cat-file -e` returned 0, so physical-closure assessment relies on enumeration and fsck. There are 25 registered worktrees; none was removed. |
| Bundle and recovery | PASS | Authoritative and repository-local bundles are 347,973,854 bytes, SHA-256 `0455adf8dc0b0a7b7dd0695781ab1776cedf924653c6a757c61c2ea8614d5887`, and byte-equal. Verification advertises the four expected commits, complete history, and no prerequisite-only dependency. The recorded fresh bare-repository recovery from the archive copy shows successful recovery and strict full fsck exit 0. Luna-0 did not create another temporary repository. |
| Exclude and staging | PASS | `git check-ignore -v` confirms the exact `/workflow/archives/wc1-a2/bundle/wc1-a2-four-commits.bundle` rule. `git add --dry-run --all workflow/archives/wc1-a2` omitted the bundle while listing documentary files as eligible. No staged changes are present. |
| Manifest and documentary archive | PASS WITH FINDING | The manifest sidecar digest matches the manifest. All 22 previously listed files match their byte lengths and SHA-256 values, and their paths exist. The manifest and sidecar are excluded to avoid self-reference; the bundle checksum sidecar is included. The report still said the independent final review was pending and would be added; this review records that finding, and the report/manifest are now updated. |
| Destination and publication | PASS WITH FINDING | No owner-authorized off-machine destination was specified. The disposition remains `OFF_MACHINE_BACKUP_PENDING_OWNER_DESTINATION`. No remote push, upload, or publication is evidenced or was performed. |

Source status showed the expected branch and baseline HEAD, with untracked
`_worktrees/`, `workflow/archives/`, and three handoff directories; the index
was clean. No branch, tag, or worktree was changed by this review.

The workflow-level architecture contract paths requested in the guardian
instructions are absent, so this is an archival-preservation review only, not
an architecture-compliance finding.

## Remaining gate

An owner-authorized off-machine destination is required before backup can be
treated as complete. Publication also remains unauthorized.

