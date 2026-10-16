# WC1-A1 - Missing-tree investigation

## Finding

- Repository object format: SHA-1 (`git rev-parse --show-object-format`).
- Expected object ID: `4b825dc642cb6eb9a060e54bf8d69288fbee4904`.
- This is the conventional empty-tree ID, SHA-1 of the canonical empty tree payload (`tree 0\0`).
- Referencing object: commit `430b60ed3684dde1d4f618d2e4c8d23410d81928`, whose raw commit header names this tree.
- `git fsck --full --unreachable` exits 2 and reports exactly `missing tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904`; no other missing/corrupt diagnostic was observed.

## Stored-object check and interpretation

The target ID was not present as a loose object at `.git/objects/4b/825dc642cb6eb9a060e54bf8d69288fbee4904`, was not found in either pack index, and was absent from `git cat-file --batch-check --batch-all-objects`. Direct `git cat-file -t` lookup nevertheless reports `tree`, `git cat-file -s` reports `0`, and the empty payload hashes to the expected canonical ID. Thus physical object-store absence is confirmed, but Git lookup supplies an effective empty-tree result. The reflog-inclusive fsck still reports the tree missing, and the reviewed bundle/recovery repository do not contain target commit `430b60ed...`; effective availability for this preservation gate is unresolved.

The complaint concerns the tree field of a reflog-only root commit, not an ordinary source artifact or an audit-report string. Git can read the commit metadata and other commits; refs, reflogs and ordinary working-tree status were readable. Under the explicit gate, do not claim a complete object closure or four-commit recovery for `430b60ed...` while fsck reports the dependency missing and the bundle does not contain the commit.

## Boundary and recommendation

No empty-tree object was written, copied, repaired or synthesized. No `git fsck --lost-found`, repair, garbage collection, pruning or reflog expiration was run. A future recovery would require a separate owner decision authorizing the exact-source/recovery or repair step, followed by full bundle/recovery verification. The current WC1-A1 authorization does not grant that step.