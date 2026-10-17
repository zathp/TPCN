# TPCN Luna-71B-WC1-A3 - Four-commit preservation report

## Disposition

| Gate | Result |
|---|---|
| Repository-local bundle | **VERIFIED** |
| Independent off-machine backup | **OFF_MACHINE_BACKUP_PENDING_OWNER_DESTINATION** |
| Four-commit recovery | **VERIFIED** |
| Local protection refs | **PARTIAL: three verified; fourth not created** |
| Source missing-tree condition | **UNCHANGED; unresolved** |
| Independent final review | **PASS WITH FINDINGS** |
| Worktree cleanup | **NOT AUTHORIZED** |
| Publication of preservation refs | **NOT AUTHORIZED** |

## Source baseline and historical commits

The source was SHA-1 format, at
`11b6f52e9aa6725af69bcd3cd098bb2c62e78b76` on branch
`governance/luna71b-c4-1-ppc11-freeze`.

| Commit | Tree | Parent(s) | Source closure |
|---|---|---|---|
| `430b60ed3684dde1d4f618d2e4c8d23410d81928` | `4b825dc642cb6eb9a060e54bf8d69288fbee4904` | none | Incomplete: canonical empty tree is physically absent |
| `77938eb04aa058246e19267326747101664cf777` | `fc7e240c18863c553edfb329ed9ce76353eaeeef` | none | Complete; 220 objects |
| `6db1e4754851cf86389ef6c7b562a6f7606cfacc` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `77938eb04aa058246e19267326747101664cf777` | Complete; 223 objects |
| `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `bcb76a40778d235806cf863dd2a9b753937dabcf` | Complete; 223 objects |

## Bundle and recovery

- Bundle filename: `wc1-a2-four-commits.bundle`
- Size: **347,973,854 bytes**
- SHA-256: **`0455adf8dc0b0a7b7dd0695781ab1776cedf924653c6a757c61c2ea8614d5887`**
- The locally retained bundle advertises exactly the four target commits.
- `git bundle verify` reports complete history, SHA-1, and no
  prerequisite-only dependency.
- The bundle was restored in a fresh repository; all four commit, tree, and
  parent identities were checked and `git fsck --full --strict` passed.
- A repository-local copy was byte/hash checked and independently restored
  with the same successful integrity result.

The bundle binary is excluded from this Git publication. No complete
independent off-machine backup has been established.

## Source protection and unresolved tree

After Luna-0 accepted their complete source closures, these three additive
local refs were created with non-overwriting compare-and-swap updates and
verified with scoped strict full `fsck`:

- `refs/preservation/wc1-a3/77938eb04aa058246e19267326747101664cf777`
- `refs/preservation/wc1-a3/6db1e4754851cf86389ef6c7b562a6f7606cfacc`
- `refs/preservation/wc1-a3/b85eb31e7801c1c8c3ee48968978cfe40a5d8aef`

No source ref was created for `430b60ed3684dde1d4f618d2e4c8d23410d81928`.
Its required empty tree
`4b825dc642cb6eb9a060e54bf8d69288fbee4904` remains absent from the source
object database and source `git fsck` reports it missing. No Git object repair,
garbage collection, or pruning was authorized or performed.

## Independent review and limits

Luna-0's independent review of the completed WC1-A3 local preservation state
was **PASS WITH FINDINGS**. It confirmed the three accepted refs, rejected
fourth ref, bundle identity/recoverability, archive exclusion, and remaining
limitations. No authorized off-machine destination was specified. The
architecture-contract source paths were unavailable to the reviewer, so its
review was limited to archival preservation rather than architecture
compliance.

No worktree was removed. No neural execution, Track B change, push of
preservation refs, or publication occurred as part of WC1-A3. This document
is a sanitized publication derivative of the reviewed local preservation
report; the source archive copy remains unchanged. Exact source-file
classification and identities are in `publication-inventory.md`.

