# Luna-71B-WC1-A2 - Final adjudication

## Scope and baseline

This adjudication covers only isolated reconstruction, independent
verification, and local preservation-artifact preparation. Source baseline:
repository `C:\Users\Patrick\Documents\ActiveCode\TPCN`, branch
`governance/luna71b-c4-1-ppc11-freeze`, HEAD
`11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`, SHA-1 object format.

All A2 artifacts and isolated repositories are under
`C:\Users\Patrick\Documents\ActiveCode\TPCN-preservation\luna71b-wc1-a2`,
outside the source repository and its registered worktrees. No commit was
rewritten. No source object or ref was written, no worktree was removed, and no
publication or off-machine copy occurred.

## Source finding

The immutable source commit
`430b60ed3684dde1d4f618d2e4c8d23410d81928` is readable. Its payload names
tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904` and contains no parent.
The source `cat-file` commands report the named object as a zero-byte tree and
return an empty payload; `cat-file --batch-check` reports
`430b60ed... commit 194` and `4b825d... tree 0`. However, the tree is absent
from all-object enumeration, there are no alternates or promisor markers, and
`git fsck --full --unreachable` exits 2 with:

```text
missing tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904
```

The apparent `cat-file`/`fsck` contradiction is explained by their different
checks: a successful effective `cat-file` result for the canonical empty tree
does not establish physical object presence. Isolated materialization of the
canonical empty tree restored a complete, integrity-checkable object closure.
The source repository was not repaired.

## Isolated recovery and bundle

In a fresh SHA-1 bare staging repository, the canonical empty payload was
materialized as tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904` (type `tree`,
payload length 0). The original commit bytes were read from source without
replacement refs, measured at 194 bytes, independently hashed, and imported
unchanged. Both the independent Git object hash and the staging write returned
`430b60ed3684dde1d4f618d2e4c8d23410d81928`. A temporary preservation ref was
created only in that isolated repository. Its full strict `git fsck` exited 0.

| Commit | Tree | Parent(s) |
|---|---|---|
| `430b60ed3684dde1d4f618d2e4c8d23410d81928` | `4b825dc642cb6eb9a060e54bf8d69288fbee4904` | none |
| `77938eb04aa058246e19267326747101664cf777` | `fc7e240c18863c553edfb329ed9ce76353eaeeef` | none |
| `6db1e4754851cf86389ef6c7b562a6f7606cfacc` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `77938eb04aa058246e19267326747101664cf777` |
| `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `bcb76a40778d235806cf863dd2a9b753937dabcf` |

The self-contained bundle advertises exactly these four target refs and
includes the complete required ancestry/object closure. Its bundle verification
reports complete history, SHA-1, and no prerequisite-only dependency. It was
restored into a second fresh bare repository without alternates or promisor
objects; exact commit/tree/parent identities were rechecked and full strict
`fsck` exited 0.

- Bundle: `wc1-a2-four-commits.bundle`
- Size: **347,973,854 bytes**
- SHA-256: **`0455adf8dc0b0a7b7dd0695781ab1776cedf924653c6a757c61c2ea8614d5887`**
- Reachable closure listing: 228 object lines; SHA-256
  `94ecd65fed4e59caf9685017716f977bc7de9c784989af877bf01a932f5a68cc`

## Independent review

Luna-0 independently reviewed source verification, empty-tree construction,
exact commit identity, isolation, target identities/parents, object closure,
bundle prerequisites/recovery, integrity checks, and mutation boundaries.
Overall review result: **PASS**. Its detailed evidence and caveat are recorded
in `05-independent-review.md`.

The initial and final source `git status --short --branch` outputs match:
branch and HEAD are unchanged and the same untracked `_worktrees/` and workflow
directories are present. No source Git write operation was performed.

## Required disposition

- Empty-tree issue: **EXPLAINED** (Git effective `cat-file` lookup did not
  establish physical presence; `fsck` correctly reported the absent object).
- Fourth commit: **RECOVERED** (exact original ID, no rewrite).
- Four-commit bundle: **VERIFIED** (self-contained and restored independently).
- Original repository: **UNMODIFIED**.
- Off-machine preservation: **NOT AUTHORIZED**.
- Worktree cleanup: **NOT AUTHORIZED**.
- Publication: **NOT AUTHORIZED**.

The bundle and evidence remain local in the A2 preservation directory. The
separate request in `07-follow-up-authorization-request.md` proposes the next
owner decision; it grants no additional authority.

