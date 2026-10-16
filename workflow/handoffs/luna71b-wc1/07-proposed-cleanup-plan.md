# Luna-71B-WC1 — Proposed Cleanup Plan

## Current action

**No cleanup operation is approved or executed.** All 23 registered
worktrees exist; none is stale or missing. No worktree is classified
`ELIGIBLE — REVIEWED REDUNDANT`. The J worktree and all original GN/H/J
evidence remain preservation-critical.

The only future worktree-only candidates are the two clean Luna-64 checkouts:

- `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna64-r4.3-pilot-20261010`
- `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna64-r4.3-reward-lifecycle-correction-20261010`

They have the same HEAD `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`, same tree
`640fd9e8e311`, no staged/modified/untracked/ignored entries, and distinct
branches and worktree HEAD reflogs. These are **CANDIDATE — AFTER
PRESERVATION**, not safe-to-delete. Retain the chosen primary checkout and
branch; export both per-worktree HEAD reflogs and record the branch-to-task
mapping before considering removal. The worktree-specific log is provenance
even though its commit IDs are otherwise reachable.

Only after (1) a separate written owner approval, (2) independent review of
the reflog/archive and reference checks, and (3) a final clean-status and
same-tree check, one of the following **worktree-only** commands could be
considered. Neither command was run. Do not use `-f`; do not delete either
branch.

```powershell
git -C "C:\Users\Patrick\Documents\ActiveCode\TPCN" worktree remove "C:\Users\Patrick\Documents\ActiveCode\TPCN-luna64-r4.3-reward-lifecycle-correction-20261010"
```

or, only if the owner instead selects the pilot checkout for removal:

```powershell
git -C "C:\Users\Patrick\Documents\ActiveCode\TPCN" worktree remove "C:\Users\Patrick\Documents\ActiveCode\TPCN-luna64-r4.3-pilot-20261010"
```

No branch deletion command is proposed. No command is proposed for any other
worktree. No `git worktree prune`, `git clean`, reset, garbage collection,
reflog expiration, recursive deletion, or file deletion is permitted by this
handoff.

## Required preservation sequence before any future removal

1. Export the candidate worktree's HEAD reflog and branch/ref identities to a
   separately hashed archive.
2. Reconfirm that the worktree has no untracked/ignored files and that its
   exact HEAD/tree still match the retained twin.
3. Review external document/manifest references and confirm no task or
   operator depends on the worktree path.
4. Preserve the branch ref; compare it against the export and remote refs.
5. Obtain independent read-only review of the archive and exact removal
   target.
6. Obtain separate owner approval naming one absolute path.
7. After any later authorized removal, verify that the retained branch,
   worktree registry, and preserved reflog archive remain intact.

This plan is a proposal only. No known evidence loss is accepted.
