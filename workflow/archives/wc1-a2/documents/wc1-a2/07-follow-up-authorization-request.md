# Follow-up authorization request - Luna-71B-WC1-A3

## Purpose

Request a separate owner decision for durable preservation of the verified
four-commit history and protection in the original repository. This request
does not authorize any action until explicitly approved.

## Evidence baseline

- Original repository: `C:\Users\Patrick\Documents\ActiveCode\TPCN`
- Reviewed HEAD: `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`
- Verified local bundle:
  `C:\Users\Patrick\Documents\ActiveCode\TPCN-preservation\luna71b-wc1-a2\wc1-a2-four-commits.bundle`
- Bundle size: 347,973,854 bytes
- Bundle SHA-256:
  `0455adf8dc0b0a7b7dd0695781ab1776cedf924653c6a757c61c2ea8614d5887`
- Four target commits:
  `430b60ed3684dde1d4f618d2e4c8d23410d81928`,
  `77938eb04aa058246e19267326747101664cf777`,
  `6db1e4754851cf86389ef6c7b562a6f7606cfacc`, and
  `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef`.

## Decisions requested

1. **Source object repair (optional, exact scope):** authorize writing only the
   canonical empty-tree object with empty payload to the original repository,
   and only if absent. Require the resulting object ID to equal
   `4b825dc642cb6eb9a060e54bf8d69288fbee4904`, then verify it with read-only
   `cat-file` and `fsck`. No other object writes, garbage collection, pruning,
   or reflog changes.
2. **Source protection refs:** authorize creating exactly four refs named
   `refs/preservation/luna71b-wc1-a2/<full-commit-id>` for the four target
   commits above. Do not move or rewrite existing branches or tags.
3. **Local durable retention:** authorize retaining the verified bundle,
   checksum sidecar, closure listing, and verification/adjudication reports in
   the existing local preservation directory. No source-repository publication
   is implied.
4. **Off-machine backup, if desired:** provide the approved destination,
   access/retention requirements, and explicit transfer authorization. The
   bundle must be copied byte-for-byte and its SHA-256 verified at the
   destination. No destination has been selected and no off-machine copy is
   authorized by this request.

Worktree cleanup and publication/pushing refs are not requested. If not
authorized, the source repository remains untouched; the verified local bundle
continues to be the independent preservation candidate.

