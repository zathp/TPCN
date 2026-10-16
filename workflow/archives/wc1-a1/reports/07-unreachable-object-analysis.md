# WC1-A1 - Unreachable-object analysis

## Bounded fsck results

| Invocation | Exit | Unreachable commits | Unreachable trees | Unreachable blobs | Other diagnostics |
|---|---:|---:|---:|---:|---|
| `git fsck --full --unreachable --no-reflogs` | 0 | 4 | 14 | 1,275 | none reported |
| `git fsck --full --unreachable` | 2 | 0 | 0 | 1,182 | one missing tree: `4b825dc642cb6eb9a060e54bf8d69288fbee4904` |

The four commits reported outside refs by the no-reflog check are the same four identified in the reflog-only inventory. No commit is unreachable from both refs and reflogs. The 93-blob count difference (1,275 versus 1,182) is consistent with blob objects reached through reflog-only history; it is an object-count classification, not proof of file provenance. The remaining 1,182 blobs are outside refs and reflogs; their origins were not resolved by the bounded file scan. The 14 trees are reported unreachable when reflogs are excluded from roots; reflog traversal makes target-history trees reachable. No object was deleted.

Against the WC1-P snapshot, the no-reflog unreachable-blob count moved from 1,257 to 1,275, while the reported commit/tree counts stayed 4/14. With reflogs included, the blob count moved from 1,164 to 1,182. The identical +18 aggregate delta is recorded without attributing a cause: current reference/worktree counts also changed, and the full prior object identity set was not available for a per-object delta comparison. An increased unreachable count alone is not evidence of progressive damage.

## Active untracked-file comparison

A read-only scan of 737 regular untracked files across the 24 registered worktrees computed raw Git blob IDs without writing objects. **Zero** file instances matched the 1,275 no-reflog unreachable blob IDs; all 1,275 therefore remain without this active-untracked-file provenance match. Ignored files were not included in this scan and remain outside this classification. The earlier WC1 inventory describes ignored research evidence; this gate did not infer that any unreachable blob was corrupt or expendable.

## Source overlap and integrity

Of the 197 blob/path entries in the initial `77938eb...` tree, 104 entries' blob IDs are reachable from current ordinary refs; five paths are exact same-path/same-blob matches in current `HEAD`. For the 198 entries in `6db1e475...` and `b85eb31...`, 105 entries' blob IDs are reachable from refs and six paths match current `HEAD` exactly. The source trees are therefore only partially represented by other current histories. The four reflog-only commit objects and their original ref/reflog provenance remain distinct from file-content duplication.

No corruption diagnostic other than the missing empty-tree dependency was found. No repair, deletion, pruning, GC or reflog expiration was performed.