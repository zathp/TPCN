# WC1-A1 - Four-commit identity inventory

## Scope and baseline

Read-only inventory against repository HEAD `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76` (`governance/luna71b-c4-1-ppc11-freeze`) on 2026-10-16. Object format: SHA-1. All four identities were independently obtained from the current reflog/ref graph, not copied solely from the WC1-P inventory.

| Commit | Tree | Parent(s) | Author / committer time (local) | Subject | Reflog evidence | Unique content / closure |
|---|---|---|---|---|---|---|
| `430b60ed3684dde1d4f618d2e4c8d23410d81928` | `4b825dc642cb6eb9a060e54bf8d69288fbee4904` | none | author 2026-04-01 11:32:03 -04:00; committer 2026-04-01 11:32:03 -04:00 | (empty) | `HEAD@{2026-04-01T11:32:03-04:00}` rebase-start checkout; later named as the main reflog rebase `onto` target | Empty root commit; no paths/blobs. Its tree object is reported missing by fsck and is not physically present in the object database. Preservation incomplete. |
| `77938eb04aa058246e19267326747101664cf777` | `fc7e240c18863c553edfb329ed9ce76353eaeeef` | none | author 2026-04-01 11:30:45 -04:00; committer 2026-04-01 11:30:45 -04:00 | `Initial commit` | `refs/heads/main` and primary `HEAD` reflogs, 11:30:45 | Root snapshot with 197 blob/path entries. Commit and full tree closure were recovered from the partial bundle. |
| `6db1e4754851cf86389ef6c7b562a6f7606cfacc` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `77938eb04aa058246e19267326747101664cf777` | author 2026-04-01 11:31:42 -04:00; committer 2026-04-01 11:31:42 -04:00 | `Create .gitignore` | `refs/heads/main` and primary `HEAD` reflogs, 11:31:42 | Adds `.gitignore`; 198 blob/path entries. Commit and full tree closure were recovered from the partial bundle. |
| `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `bcb76a40778d235806cf863dd2a9b753937dabcf` | author 2026-04-01 11:30:45 -04:00; committer 2026-04-01 11:32:46 -04:00 | `Initial commit` | `refs/heads/main` rebase-finish reflog and primary `HEAD` reflogs, 11:32:46 | Distinct commit/parent history, but same tree as `6db1e475...`; no unique tree content relative to that commit. Complete history recovered from the partial bundle. |

The target commit IDs, trees, parent links, timestamps and subjects were checked with Git object queries. The three included bundle commits retain their exact identities and parent history. No commit history was rewritten.

## Source-artifact overlap

The 197 paths in `77938eb...` contain 197 blob entries; 104 entries have blob IDs already reachable from current ordinary refs, and five paths have the same path and blob ID as current `HEAD`. The 198 entries in `6db1e475...` / `b85eb31...` have 105 blob entries reachable from ordinary refs and six exact same-path/same-blob matches in current `HEAD` (the five above plus `.gitignore`). These are partial overlaps, not proof that the historical source tree is fully represented elsewhere. A read-only raw-Git-blob hash scan of 737 regular untracked files across 24 registered worktrees found no match among the 1,275 no-reflog unreachable blob IDs; ignored files were not part of that scan.

## Disposition

Identity inventory: VERIFIED. Full preservation for all four: INCOMPLETE because `430b60ed...` references the missing empty-tree object. The other three commits have a separately recovered, self-contained bundle closure.