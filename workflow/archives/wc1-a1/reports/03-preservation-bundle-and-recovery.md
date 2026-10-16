# WC1-A1 - Preservation bundle identity and recovery verification

## Candidate

- Status: **PARTIAL ONLY - three of four target commits**
- Bundle: `C:\Users\Patrick\Documents\ActiveCode\TPCN-preservation\luna71b-wc1-a1\wc1-a1-three-commits-partial.bundle`
- Exact size: **347,973,648 bytes**
- SHA-256: **`97fc628794b0ba4aeb90392aa5d16cfd8a4823dbe7eb2a19da0ec87c00a19a08`**
- Object format: SHA-1
- Advertised refs: `refs/preservation/luna71b-wc1-a1/<full-commit-sha>` for `6db1e4754851cf86389ef6c7b562a6f7606cfacc`, `77938eb04aa058246e19267326747101664cf777`, and `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef`.

The initial bundle construction was done in a dedicated bare staging repository outside all TPCN worktrees. The advertised preservation refs existed only in that temporary staging repository/bundle; none was written to the original repository. `git bundle verify` reported that the bundle records a complete history and has no prerequisite-only dependency. The bundle uses SHA-1 and advertises exactly three refs.

## Isolated recovery

The candidate was cloned from the bundle into a separate fresh bare repository. In that recovered repository, the three target refs resolved to the exact expected commit identities and trees:

| Commit | Recovered tree | Recovered parent(s) |
|---|---|---|
| `77938eb04aa058246e19267326747101664cf777` | `fc7e240c18863c553edfb329ed9ce76353eaeeef` | none |
| `6db1e4754851cf86389ef6c7b562a6f7606cfacc` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `77938eb04aa058246e19267326747101664cf777` |
| `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef` | `1edcdec78e6d8f05bdacc2cd56529592c5c9a886` | `bcb76a40778d235806cf863dd2a9b753937dabcf` |

`git fsck --full` in the recovered bare repository exited 0. This proves isolated recovery of the three included histories; it does not qualify `430b60ed...`.

## Blocked fourth target

`430b60ed3684dde1d4f618d2e4c8d23410d81928` is not advertised by the bundle. Its commit object names tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904`; `git fsck --full --unreachable` reports that tree missing. Under the owner instruction not to create the missing object, no complete four-commit bundle can be claimed. The candidate is therefore partial, not a successful WC1-A1 four-commit backup.