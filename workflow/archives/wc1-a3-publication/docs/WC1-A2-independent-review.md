# Luna-71B-WC1-A2 - Independent review

## Reviewer and scope

Reviewer: Luna-0 Architecture Guardian  
Review mode: independent, read-only  
Source baseline: `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76` on `governance/luna71b-c4-1-ppc11-freeze`

## Verdict

**PASS** for isolated reconstruction and four-commit bundle restoration. This
does not mean the source repository was repaired; its empty-tree object remains
physically absent.

| Criterion | Verdict | Evidence |
|---|---|---|
| Source baseline and lookup configuration | PASS | SHA-1 format and exact baseline HEAD/branch verified. No alternates, promisor markers, replacement refs, or object-directory environment variables were found. |
| `cat-file` versus physical empty-tree presence | PASS | Source `cat-file` reports the canonical tree as type `tree`, size 0, and succeeds on `-e`; source `fsck` reports the tree missing and all-object enumeration does not list it. Effective lookup is not proof of physical storage. |
| Canonical empty tree | PASS | Empty payload materialized only in staging; `hash-object` returned `4b825dc642cb6eb9a060e54bf8d69288fbee4904`; staging reports type `tree`, size 0. |
| Exact fourth commit identity | PASS | Source raw commit payload is 194 bytes. Its independently computed Git object ID and staging `hash-object` result both equal `430b60ed3684dde1d4f618d2e4c8d23410d81928`. |
| Isolation from source | PASS, caveat noted | Reconstruction writes and temporary refs target the separate bare staging repository. Luna-0 verified the source HEAD/branch and no tracked modifications; it could not independently attribute untracked directories without an earlier status snapshot. The orchestrator's initial and final status outputs match, including `_worktrees/` and workflow directories. |
| Four target identities and parents | PASS | All four commits resolve to the expected trees and exact parents. The parent `bcb76a40778d235806cf863dd2a9b753937dabcf` of `b85eb31e...` is included as required ancestry, not as a target ref. |
| Closure and external prerequisites | PASS | The complete reachable object list has 228 entries and SHA-256 `94ecd65fed4e59caf9685017716f977bc7de9c784989af877bf01a932f5a68cc`. Bundle verification reports complete history and SHA-1, with no prerequisite-only dependency; the restored repository has no alternates or promisor markers. |
| Second fresh-repository recovery | PASS | All four bundle refs were restored into a separately initialized bare repository; exact identities were rechecked and `git fsck --full --strict` exited 0. |
| Integrity | PASS | Both staging and restored repositories pass strict full `fsck`. Bundle size is 347,973,854 bytes; SHA-256 is `0455adf8dc0b0a7b7dd0695781ab1776cedf924653c6a757c61c2ea8614d5887`. |
| Unauthorized source mutation | No indication found | Reviewed commands use source reads only; writes are confined to the isolated repositories and local A2 preservation directory. No source refs were created, no worktrees removed, and nothing was published or copied off-machine. |

## Caveat

Source `git fsck --full --unreachable` exits 2 and reports the missing empty
tree, alongside unreachable blobs. The missing source object remains
unrepaired. The source status also contains untracked `_worktrees/` and
workflow directories; the initial and final status outputs match.
