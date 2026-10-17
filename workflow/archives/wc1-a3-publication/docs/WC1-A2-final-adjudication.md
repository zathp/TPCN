# Luna-71B-WC1-A2 - Final adjudication (publication derivative)

**Source artifact:** `06-final-adjudication.md`  
**Source size:** 4,788 bytes  
**Source SHA-256:** `35e1f822a4203368b4bc27a6e3f602344ea6d3954a8c34addd14c4ead7875a9c`

This is a distinct, sanitized publication derivative. The unchanged source
artifact remains in the local WC1-A2 archive. Machine-local absolute paths
were omitted; the recovery findings and immutable Git identities are retained.

## Source finding

The source repository used SHA-1 and contained readable commit
`430b60ed3684dde1d4f618d2e4c8d23410d81928`, whose tree is
`4b825dc642cb6eb9a060e54bf8d69288fbee4904` and which has no parent. Source
`cat-file` reported the named tree as type `tree`, size zero, and empty
payload; source `git fsck --full --unreachable` exited 2 and reported the
empty-tree object missing. All-object enumeration did not list that tree.
Effective `cat-file` lookup therefore did not establish physical object
presence. The source repository was not repaired.

## Isolated recovery

In a separate fresh SHA-1 bare repository, the canonical empty payload
materialized as tree
`4b825dc642cb6eb9a060e54bf8d69288fbee4904`. The original 194-byte commit
payload was imported unchanged; its independently computed object ID and the
staging write both returned
`430b60ed3684dde1d4f618d2e4c8d23410d81928`. The isolated repository passed
full strict `git fsck`.

| Commit | Tree | Parent(s) |
|---|---|---|
| `430b60ed3684dde1d4f618d2e4c8d23410d81928` | `4b825dc642cb6eb9a060e54bf8d69288fbee4904` | none |
| `77938eb04aa058246e19267326747101664cf777` | `fc7e240c18863c553edfb329ed9ce76353eaeeef` | none |
| `6db1e4754851cf86389ef6c7b562a6f7606cfacc` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `77938eb04aa058246e19267326747101664cf777` |
| `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `bcb76a40778d235806cf863dd2a9b753937dabcf` |

## Bundle and adjudication

The complete self-contained bundle advertises the four target commits and
passed bundle verification. Restoration into a second fresh bare repository
verified the commit/tree/parent identities and passed `git fsck --full
--strict`.

- Bundle size: **347,973,854 bytes**
- Bundle SHA-256:
  **`0455adf8dc0b0a7b7dd0695781ab1776cedf924653c6a757c61c2ea8614d5887`**
- Reachable closure listing: 228 object lines; SHA-256
  `94ecd65fed4e59caf9685017716f977bc7de9c784989af877bf01a932f5a68cc`

The original WC1-A2 Luna-0 review verdict was **PASS** for isolated recovery
and bundle restoration. WC1-A2 disposition: empty-tree issue **EXPLAINED**;
fourth commit **RECOVERED**; four-commit bundle **VERIFIED**; source
repository unmodified; off-machine preservation and publication not
authorized.

