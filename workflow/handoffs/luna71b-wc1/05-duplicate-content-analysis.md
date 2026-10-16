# Luna-71B-WC1 — Duplicate-Content Analysis

## Exact-byte results

Exact duplicates are grouped by SHA-256 of raw file bytes, not by filename,
Git tree equality, or presumed scientific interchangeability.

| Scope | File instances | Distinct raw SHA-256 identities | Duplicate groups | Excess exact copies |
|---|---:|---:|---:|---:|
| Untracked regular files | 721 | 200 | 99 | 521 |
| Research-relevant ignored files | 140 | 106 | 34 | 34 |
| **Combined** | **861** | **306** | **133** | **555** |

The eight tracked status paths are inventoried separately from these
untracked/ignored totals. They contain five raw identities: two substantive
corrected source contents, each present in H and J, and four H status-only
contents whose clean blob IDs equal HEAD and whose `git diff` is empty. H's
two corrected contents are byte-identical to J's; the other four status
paths are not source edits.

Including the tracked status paths gives 869 instances, 308 distinct raw
identities, 135 exact duplicate groups, and 561 excess exact copies. The
tracked paths comprise four substantive changed entries (two corrected
contents, each present in H and J), plus four status-only entries. The 268
distinct raw-byte identities absent from cached remotes include the two
substantive corrected contents, but not the status-only baseline contents.

Git-clean identities after the repository's `text=auto` processing are also
grouped separately; in this snapshot they have the same counts, but their
object identities can differ from raw-byte blob IDs. Full duplicate groups,
paths, worktrees, byte sizes, raw hashes, and normalized identities are in
[`05-duplicate-content-analysis.json`](./05-duplicate-content-analysis.json).

## Material duplicate cases

- The main checkout and Luna-63A each contain the same 34 Luna-47A
  `_evidence` files. Both copies are ignored by Git, hash-identical, and
  scientifically relevant. Keep both paths until provenance and archival
  obligations are explicitly closed.
- H and J contain byte-identical corrected `ppc11/capture.py` and
  `ppc11/driver.py` working copies. The copies carry different worktree
  context; neither is a deletion target.
- C4.2, GN, H, and J share published C4.2 HEAD/tree identities but contain
  different local sources, changes, fixtures, tests, and evidence.
- Luna-66, Luna-67, Luna-68, Luna-70, Luna-71B, and C4 share the same
  `f117ce51...` base tree, but contain different untracked files and research
  roles.
- The two Luna-64 worktrees have the same commit/tree and no untracked or
  ignored files, but distinct branch and worktree HEAD-reflog contexts.
  Tree equality does not justify losing those contexts.
- The 72 ignored checkpoint files include repeated content identities; each
  path remains separately recorded in the inventory because a matching
  checkpoint payload does not establish identical training provenance.

No files were deduplicated, moved, rewritten, or removed. Do not use the
duplicate groups as cleanup commands. Path, lineage, branch, manifest, and
reflog provenance remain part of the preservation record.
