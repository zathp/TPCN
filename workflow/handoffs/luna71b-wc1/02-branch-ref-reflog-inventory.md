# Luna-71B-WC1 — Branch and Git Reference Inventory

## Snapshot and reference counts

This is a read-only inventory of the local Git reference snapshot at
2026-10-16. No fetch or live remote query was made; `refs/remotes/origin/*`
means the locally cached remote-tracking refs, not a current server response.

| Reference namespace | Count | Disposition |
|---|---:|---|
| `refs/heads/*` | 29 | Local branches; none deleted |
| `refs/remotes/*` | 35 | 34 remote branches plus symbolic `origin/HEAD -> origin/main` |
| `refs/agents/*` | 182 | Local agent/workspace refs; preserved as opaque references |
| Tags | 0 | None |
| **Total** | **246** | Full exact identities in the JSON inventory |

There are 22 branch-attached worktrees and one detached worktree. Seven local
heads do not currently have a registered worktree:

- `archive/luna65-rp2b-local-drafts-20261015`
- `draft/luna65-phase2a-supervisor-scaffold-20261012`
- `experiment/luna63c-stage-a-certificate`
- `experiment/luna71b-c4-2-bilateral-capture`
- `feature/single-replay-3d-plasticity`
- `governance/luna64-r4.3-freeze-20261010`
- `main`

No branch is declared stale from absence of a worktree or upstream. Several
branches have different scientific/governance names but the same commit;
branch identity and reflog context are retained separately from tree
equality.

## Reachability and reflogs

- 516 commits are reachable from the cached remote-tracking refs.
- 343 distinct commits are reachable from some local ref or reflog but not
  from the cached remote-tracking refs. The full commit list is in the JSON
  inventory. This includes private agent references and must not be treated
  as safe-to-delete history.
- 4 commits are reachable only from reflogs and not any ref:
  `430b60ed3684dde1d4f618d2e4c8d23410d81928`,
  `6db1e4754851cf86389ef6c7b562a6f7606cfacc`,
  `77938eb04aa058246e19267326747101664cf777`, and
  `b85eb31e7801c1c8c3ee48968978cfe40a5d8aef`.
  Their exact tree/parent/subject identities are recorded in the JSON.
- 209 per-worktree `HEAD` reflog entries were inspected across the 23
  worktrees. The four root-only reflog commits above are the only commits
  not reachable from a ref; none is unique to an external worktree's HEAD
  reflog. Worktree-specific reflog entries are still provenance and should
  be exported before any later worktree removal.
- With reflogs included, `git fsck --full --unreachable` reported no
  unreachable commits but exited 2 because the canonical empty-tree object
  `4b825dc642cb6eb9a060e54bf8d69288fbee4904` is missing. The initial,
  reflog-only commit `430b60ed...` names that tree. It also reported 1,164
  unreachable blobs.
- With reflogs excluded, `git fsck --full --unreachable --no-reflogs`
  exited 0 and reported 4 commit objects, 14 trees, and 1,257 blobs outside
  refs. The four commits are the reflog-only commits above; no cleanup or
  repair was attempted.

Accordingly, the count of commits currently unreachable from both refs and
reflogs is **0**, but there are **4 reflog-only commits**, 1,164 unreachable
blobs, and a missing empty-tree object. The missing object and orphaned blobs
are unresolved Git-metadata preservation risks. Do not prune, expire reflogs,
run garbage collection, or remove related local references under WC1.

## Worktree/remote relationship

All registered worktree HEADs and full branch/object IDs are included in
[`01-worktree-inventory.json`](./01-worktree-inventory.json). All local and
remote refs, per-branch commit IDs, cached-remote reachability sets,
per-worktree HEAD reflogs, fsck output classification, and ref namespace
counts are in
[`02-branch-ref-reflog-inventory.json`](./02-branch-ref-reflog-inventory.json).

The repository contains 6,135 objects reachable from all refs and 5,366
objects reachable from cached remote refs. Object presence is not equivalent
to publication of a particular file at a particular path; the file-level
inventory separately records exact-byte and Git-clean-blob reachability.
No branch, ref, reflog, or Git object was intentionally modified.
