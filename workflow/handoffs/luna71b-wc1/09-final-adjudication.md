# Luna-71B-WC1 — Final Adjudication

## Overall disposition

**INVENTORY COMPLETE; PRESERVATION REQUIRED; CLEANUP NOT AUTHORIZED.**
There are 23 registered worktrees, all physically present; 11 are dirty by
tracked/untracked Git status, one is detached, and none has staged changes.
No worktree qualifies as reviewed-redundant. The two identical clean
Luna-64 worktrees are only candidates after reflog preservation and further
review.

## Required counts

| Measure | Result |
|---|---:|
| Registered worktrees | 23 |
| Existing worktree directories | 23 |
| Dirty worktrees (tracked changes and/or untracked entries) | 11 |
| Detached worktrees | 1 |
| Untracked regular files in baseline inventory | 721 |
| Distinct untracked raw SHA-256 identities | 200 |
| Unique untracked raw-byte identities absent from cached remote refs | 194 |
| Research-relevant ignored file instances / distinct identities | 140 / 106 |
| Unique raw-byte identities absent from cached remotes, combining untracked, research-ignored, and substantive tracked corrections | 268 |
| Combined untracked, research-ignored, and tracked-status instances / distinct raw identities | 869 / 308 |
| Tracked-status paths with substantive content change / status-only anomaly | 4 / 4 |
| Reflog-only commits, not reachable from any ref | 4 |
| Commits unreachable from refs and reflogs | 0 |
| Missing Git object reported by `fsck` | Empty-tree object `4b825dc...` |
| Worktrees proposed for later consideration | Luna-64 pilot/correction pair only |
| Worktrees approved or eligible for immediate removal | 0 |

“Unpublished” in the count means the exact raw content identity is absent
from cached remote-tracking refs; it is not a claim about semantic
publication at every path. The locally cached remote refs were not refreshed
over the network.

## Blocking preservation issues

1. **C4.2-J final manifest review gap:** current 232-entry manifest
   `9fdea20af632f9e3f8d4c14612c2a7cad1706534af2f487ef30e24e4f3243441`
   passes local 232/232 byte verification, but Luna-0's Review 3 identity
   was its 55,286-byte predecessor
   `92bb6b3e55cd3237311f9825aac430cb5b31a33bb66b34c028e85c8cab9c9648`.
   The current manifest and closeout bytes require a fresh independent
   publication review. J remains detached and must be kept.
2. **C4.2-I portability/publication gap:** its 30 declared input identities
   resolve across current local worktrees, but 17 are in cross-worktree
   C4.2/GN/H/J paths, none represented by a current published I branch.
   The 14-file documentation allowlist is only a narrow candidate; v2 is
   not adopted.
3. **Git metadata:** four commits are reachable only from reflogs, and
   `git fsck` reports a missing canonical empty tree referenced by
   reflog-only commit `430b60ed...`. Preserve all refs/reflogs. No object
   repair or garbage collection was attempted.
4. **Ignored research evidence:** 72 checkpoint files and two identical
   34-file Luna-47A evidence trees are ignored by Git. They have been
   inventoried and hashed; they are not expendable caches.
5. **Historical identity:** the prior C4.2-I/J records retain unresolved
   source-manifest preimage
   `43fb851cf45fdcc9910215cc7d13cd6364860d32891febd203ef6f7c33474719`
   and test-index preimage
   `0ad1d9e1e407393b797ace9b04be6a6cd30de45ad00b898e493ffc41b4752697`.
   WC1 neither recovers nor rewrites them. The current shared GN/H/J
   `gn/source/c4.2-source-manifest.json` has identity
   `d3edfd73c4ac9f183f145d49fac4d01e8ca5aaf552f681ddd2bdd253dbccf5a7`;
   it is not either historical preimage.

## Worktree disposition

The per-worktree classifications and actions are in
[`04-preservation-and-provenance-matrix.md`](./04-preservation-and-provenance-matrix.md).
All worktrees require retention now except that the clean Luna-64 pair may
be reconsidered after preservation and separate approval. The machine
inventories preserve full paths, revisions, trees, status entries, file
hashes, Git object identities, and reflog details.

## Verification and authority boundary

- I manifest: 30/30 current local identity records verified; final manifest
  SHA-256 `1cc1f19b288c20601cfa7853382d0aff4f5b5392afbc8cc185ef0752b861b775`.
- J manifest: 232/232 current entries verified; current digest
  `9fdea20af632f9e3f8d4c14612c2a7cad1706534af2f487ef30e24e4f3243441`;
  independent review applies to the predecessor identity, not this final
  digest.
- No neural tests, training, inference, model execution, or pilot ran during
  WC1. Previously reported J/GN/C4.2 tests were not rerun.
- No worktree was removed or pruned. No untracked/ignored file or branch was
  deleted. No historical evidence was rewritten. No commit, push, merge,
  publication, or architecture change occurred.

**Independent-review status:** **PASS WITH FINDINGS**. Luna-0 verified the
inventory counts, exact report identities, manifest reconciliation, and
cleanup boundaries. Review evidence and its full input hashes are in
[`08-independent-review.md`](./08-independent-review.md). The historical
`43fb…`/`0ad1…` preimages remain unresolved. Luna-0's closeout finding about
the not-yet-present review/manifest artifacts is addressed by this report
and the final manifest, subject to a separate manifest-closure check.

## Narrowest next action

If publication is later desired, first obtain a final identity check of the
WC1 manifest, then request separate owner authorization for the exact scope
below. Any I/J staged-tree publication review or Luna-64 worktree removal
requires its own explicit scope and approval; neither is authorized by WC1.

## Separate WC1 publication authorization prompt

The WC1 package is local, untracked, and not published. If the owner later
wants only this documentary audit published, request separate authorization
to place exactly the following 16 files in a new
`governance/luna71b-wc1-preservation-audit` branch based on C4.1 commit
`11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`:

1. `workflow/handoffs/luna71b-wc1/01-worktree-inventory.md`
2. `workflow/handoffs/luna71b-wc1/01-worktree-inventory.json`
3. `workflow/handoffs/luna71b-wc1/02-branch-ref-reflog-inventory.md`
4. `workflow/handoffs/luna71b-wc1/02-branch-ref-reflog-inventory.json`
5. `workflow/handoffs/luna71b-wc1/03-untracked-and-ignored-inventory.md`
6. `workflow/handoffs/luna71b-wc1/03-untracked-ignored-artifact-inventory.json`
7. `workflow/handoffs/luna71b-wc1/03-git-normalized-file-identities.json`
8. `workflow/handoffs/luna71b-wc1/04-preservation-and-provenance-matrix.md`
9. `workflow/handoffs/luna71b-wc1/05-duplicate-content-analysis.md`
10. `workflow/handoffs/luna71b-wc1/05-duplicate-content-analysis.json`
11. `workflow/handoffs/luna71b-wc1/06-c4.2-i-j-publication-readiness.md`
12. `workflow/handoffs/luna71b-wc1/07-proposed-cleanup-plan.md`
13. `workflow/handoffs/luna71b-wc1/08-independent-review.md`
14. `workflow/handoffs/luna71b-wc1/09-final-adjudication.md`
15. `workflow/handoffs/luna71b-wc1/10-artifact-manifest.json`
16. `workflow/handoffs/luna71b-wc1/10-artifact-manifest.sha256`

The authorization request must cover all 16 paths. The final artifact
manifest inventories each documentary artifact except itself and its
checksum sidecar to avoid circular hashing. No source,
model, test, experiment, fixture, cache, worktree, branch deletion, or other
path is in this allowlist. Any later publication requires a fresh exact
staged-tree identity review and separate owner approval; nothing here
authorizes staging, commit, push, merge, or publication.
