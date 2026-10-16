# WC1-A1 - Git reference and reachability analysis

## Current repository state

- Checkout: `C:\Users\Patrick\Documents\ActiveCode\TPCN`
- Branch / HEAD: `governance/luna71b-c4-1-ppc11-freeze` / `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`
- Git status: no tracked modifications; pre-existing untracked entries remain `_worktrees/`, `workflow/handoffs/luna71b-c4.2-i/`, `workflow/handoffs/luna71b-c4.2-j/`, and `workflow/handoffs/luna71b-wc1/`.
- Registered worktrees: 24 (23 branch-attached, one detached)
- `refs/heads/*`: 30; `refs/remotes/*`: 36 (includes symbolic `origin/HEAD`); `refs/agents/*`: 186; tags: 0.

The counts are refreshed observations, not copies of WC1-P's historical snapshot (23 worktrees, 29 heads, 35 remote refs and 182 agent refs).

## WC1-P publication verification

The local branch `governance/luna71b-wc1-preservation-inventory` and cached remote-tracking branch `origin/governance/luna71b-wc1-preservation-inventory` both resolve to commit `d5493b741a514a96009641b0e565df1648ffa975`, tree `7549caa7c6604320f8b2ee7c9dca179fa9803988`, as authorized. The historical artifact manifest's raw SHA-256 is `2ed6d610bf39a69267b0567cb0e2e34e9bd45ca1e659943c581d481539e591e8`; its sidecar raw SHA-256 is `ce82884f8d661fd9d92dc8acfb833d40773b3f423841ae393cb720eec03cc838`. This verifies the local published snapshot identity only; no remote fetch or live-server query was made.

## Target reachability and provenance

`git rev-list --all` versus `git rev-list --reflog --all` reproduces exactly these four reflog-only commits: `430b60ed3684dde1d4f618d2e4c8d23410d81928`, `6db1e4754851cf86389ef6c7b562a6f7606cfacc`, `77938eb04aa058246e19267326747101664cf777`, and `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef`. For each, `git for-each-ref --contains <commit>` returns no ordinary ref. No current worktree HEAD is at any target commit.

The reflog records place `77938eb...` and `6db1e475...` in both the shared `refs/heads/main` reflog and the primary `HEAD` reflog. `b85eb31...` is recorded in the shared main reflog and primary `HEAD` reflog at rebase finish/pick. `430b60ed...` appears in primary `HEAD` at rebase start; the main reflog rebase-finish message names it as the `onto` target, while the commit itself has no parent. Both main and primary `HEAD` reflogs later record a reset at 2026-04-01 11:44:09 -04:00 to `bcb76a40778d235806cf863dd2a9b753937dabcf`. None of the target IDs appeared in registered linked-worktree `HEAD` reflogs. These entries establish historical main/primary-checkout context, not a current worktree association.

No protective refs were created. No branch, ref, reflog or worktree was deleted or replaced; no remote was contacted.