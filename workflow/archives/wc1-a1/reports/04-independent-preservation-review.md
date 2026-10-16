# WC1-A1 - Independent preservation review

## Review authority and verdict

Reviewer: Luna-0 Architecture Guardian, assigned read-only to review the WC1-A1 preservation candidate before any source-repository protection refs. Reviewed baseline: `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76` on `governance/luna71b-c4-1-ppc11-freeze`.

**Verdict: BLOCKED.** Partial preservation is verified for three of four targets. Complete four-target preservation is not available in the reviewed candidate, so no local protection refs may be created under this authorization.

## Findings

- All four target commit identities, trees and parent histories match the read-only original-repository inventory; `for-each-ref --contains` finds no ordinary ref for any target.
- The candidate bundle is 347,973,648 bytes with SHA-256 `97fc628794b0ba4aeb90392aa5d16cfd8a4823dbe7eb2a19da0ec87c00a19a08`. It advertises exactly `6db1e4754851cf86389ef6c7b562a6f7606cfacc`, `77938eb04aa058246e19267326747101664cf777`, and `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef`. `git bundle verify` reports complete history for those three refs. The isolated recovery repository resolves their exact commit/tree/parent identities, and `git fsck --full` passes there.
- The candidate does not contain `430b60ed3684dde1d4f618d2e4c8d23410d81928`; the isolated recovery repository cannot resolve it. Thus bundle integrity for the three included targets is not a four-target recovery pass.
- Reflog-inclusive `git fsck --full --unreachable` exits 2 and reports missing tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904`. In contrast, direct `git cat-file` resolves that ID as an empty tree of size zero, and hashing its empty-tree payload yields that ID. No loose object or pack-index entry was found. **The physical storage absence is confirmed, but effective availability is unresolved.** Do not synthesize or repair the object under this authorization.
- The WC1-P local branch and cached remote-tracking branch both resolve to `d5493b741a514a96009641b0e565df1648ffa975`, tree `7549caa7c6604320f8b2ee7c9dca179fa9803988`; its manifest and sidecar hashes match the authorized identities.
- Refreshed counts are 24 worktrees, 30 local heads, 36 remote refs, 186 `refs/agents`, and 0 tags. Existing untracked worktree/handoff directories remain.

## Independent boundary check

The reviewer reports no changes to files, refs, branches or worktrees; no repair, pruning, push or neural execution. No handoff file was written because the review assignment was explicitly read-only. Disposition: **do not create source-repository protection refs from the partial candidate**.