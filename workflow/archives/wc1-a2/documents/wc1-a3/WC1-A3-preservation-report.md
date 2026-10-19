# TPCN Luna-71B-WC1-A3 - Preservation report and publication candidate

## Disposition

| Gate | Result |
|---|---|
| Repository-local bundle | **VERIFIED** |
| Independent off-machine backup | **PENDING OWNER DESTINATION** |
| Four-commit recovery | **VERIFIED** |
| Local protection refs | **PARTIAL: three verified; fourth not created** |
| Original missing-tree condition | **UNCHANGED** |
| Independent final review | **PASS WITH FINDINGS** |
| Worktree cleanup | **NOT AUTHORIZED; none performed** |
| Publication | **NOT AUTHORIZED; candidate only** |

## Source baseline and target identities

Source repository: `C:\Users\Patrick\Documents\ActiveCode\TPCN`  
Branch: `governance/luna71b-c4-1-ppc11-freeze`  
HEAD: `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`  
Object format: SHA-1

| Commit | Tree | Parent(s) | Source closure |
|---|---|---|---|
| `430b60ed3684dde1d4f618d2e4c8d23410d81928` | `4b825dc642cb6eb9a060e54bf8d69288fbee4904` | none | Incomplete in source: canonical empty tree is absent |
| `77938eb04aa058246e19267326747101664cf777` | `fc7e240c18863c553edfb329ed9ce76353eaeeef` | none | Complete; 220 objects |
| `6db1e4754851cf86389ef6c7b562a6f7606cfacc` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `77938eb04aa058246e19267326747101664cf777` | Complete; 223 objects |
| `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `bcb76a40778d235806cf863dd2a9b753937dabcf` | Complete; 223 objects |

## Bundle identity and recovery

The authoritative A2 bundle was verified before copying:

- File: `bundle/wc1-a2-four-commits.bundle`
- Size: **347,973,854 bytes**
- SHA-256: **`0455adf8dc0b0a7b7dd0695781ab1776cedf924653c6a757c61c2ea8614d5887`**
- Advertised target refs: exactly the four commit IDs above.
- `git bundle verify`: complete history, SHA-1, no prerequisite-only dependency.
- Independent recovery before copy: successful into a fresh bare repository;
  strict full `git fsck` passed.
- Copy: raw byte copy into the repository-local archive; byte count and
  SHA-256 match the authoritative source artifact.
- Recovery from repository-local copy: successful in a separate fresh bare
  repository; the four commit IDs, trees and parents matched and
  `git fsck --full --strict` passed.

The local binary is excluded from Git staging using only the exact path rule
in this worktree's `.git/info/exclude`:

```text
/workflow/archives/wc1-a2/bundle/wc1-a2-four-commits.bundle
```

`git check-ignore -v` confirmed that exact rule. `git add --dry-run --all
workflow/archives/wc1-a2` listed documentary files and checksum metadata but
not the binary bundle. No files were actually staged.

## Qualified source refs

Luna-0 independently accepted only the three complete source closures before
creation. The following refs were then created with compare-and-swap
`git update-ref <ref> <target> <all-zero-old-object-id>` updates, which fail
rather than overwrite an existing ref:

- `refs/preservation/wc1-a3/77938eb04aa058246e19267326747101664cf777`
- `refs/preservation/wc1-a3/6db1e4754851cf86389ef6c7b562a6f7606cfacc`
- `refs/preservation/wc1-a3/b85eb31e7801c1c8c3ee48968978cfe40a5d8aef`

Each exact ref target and source closure was rechecked; scoped full strict
`fsck` passed for each. No pre-existing source ref protected these targets.
No ref was created for
`430b60ed3684dde1d4f618d2e4c8d23410d81928`: its source closure still lacks
tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904`, and scoped strict full fsck
reports it missing. Its unchanged commit identity and complete recovery are
preserved in the local bundle. Source repair requires separate authorization.

## Backup destination

No owner-authorized off-machine destination was named in this authorization or
the predecessor preservation records. A OneDrive environment path is visible
on this machine, but it is not treated as owner authorization or as a verified
backup destination. No copy was sent to OneDrive, another drive, or a remote.

**OFF_MACHINE_BACKUP_PENDING_OWNER_DESTINATION**

## Documentary publication candidate

This directory contains copied A2 recovery/source-verification reports and A3
preservation results, the preliminary Luna-0 ref-acceptance record, the final
Luna-0 review, a bundle checksum sidecar, and an updated SHA-256/size manifest.
The 348 MB binary is separate and excluded from ordinary Git staging.

Luna-0's final review is **PASS WITH FINDINGS** for the local preservation
state. Its findings are that no authorized off-machine destination was
specified, and that the prior manifest/report incorrectly marked the review
pending before this final response was recorded. The report and manifest have
now been updated to include the completed review. See
`independent-final-review.md`.

This is a documentary candidate only. Nothing was staged, committed, pushed,
uploaded, or published. Publication and pushing private historical refs
require separate authorization.

## Preservation boundaries

No source Git object was repaired or materialized. No GC, pruning, worktree
removal, neural execution, Track B change, branch/tag movement, history
rewriting, or publication occurred. The registered worktrees were only
inspected; none was deleted or overwritten. Existing experiments and
historical evidence were not deleted or overwritten.

The authoritative file inventory and SHA-256 values are in
`../../manifests/wc1-a3-preservation-manifest.json`; that manifest excludes
itself to avoid self-referential hashing, with its own identity recorded in the
manifest checksum sidecar and final handoff.
