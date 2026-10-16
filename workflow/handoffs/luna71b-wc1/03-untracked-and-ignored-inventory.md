# Luna-71B-WC1 — Untracked and Ignored Artifact Inventory

## Inventory counts

At the pre-WC1-output snapshot, the registered worktrees contained:

- **722 untracked status entries:** 721 regular files plus the main checkout's
  pointer to the separately inventoried J worktree.
- **200 distinct raw SHA-256 content identities** across those regular files.
- **194 distinct raw-byte identities** whose exact raw-byte Git blob was not
  reachable from the locally cached remote refs. These represent
  2,417,743,223 bytes after exact-content deduplication. Six raw identities
  were reachable somewhere in cached remote history, which does not by
  itself mean the same artifact/path was published.
- After `text=auto` / `core.autocrlf=true` path cleaning, **162 distinct clean
  Git blob identities** were not reachable from cached remote refs; 26 were
  reachable from local refs/reflogs but not cached remotes, and 136 were not
  found in refs or reflogs.
- Counting untracked files, research-relevant ignored files, and the
  substantive corrected tracked source contents together yields **268
  distinct raw-byte identities** absent from cached remote refs. This is an
  exact-content count, not a path-level publication or scientific-uniqueness
  claim.
- **84 `--ignored=matching` entries.** For experiment-relevant ignored data,
  140 file instances were individually hashed across three trees: 72
  checkpoint files, 34 Luna-47A evidence files in the main checkout, and
  the same 34 Luna-47A evidence files in the Luna-63A checkout. They
  represent 106 distinct raw identities and 20,198,585,681 bytes after
  exact-content deduplication.

The 72 ignored checkpoints total 19,704,610,690 bytes. Each of the two
Luna-47A evidence trees totals 493,974,991 bytes. These are preserved
research artifacts, not disposable caches. Cache, virtual-environment,
bytecode, and runtime dependency paths are listed with per-tree file/size
counts but are not treated as scientific evidence. No ignored or untracked
file was removed.

## Exact identities and reference coverage

[`03-untracked-ignored-artifact-inventory.json`](./03-untracked-ignored-artifact-inventory.json)
contains the per-file untracked/ignored inventory, exact path, worktree,
byte size, raw SHA-256, duplicate group, and tracked-modification records.
[`03-git-normalized-file-identities.json`](./03-git-normalized-file-identities.json)
records the raw-byte Git blob identity separately from the identity after
Git's configured path-clean operation, plus cached-remote, local-ref, and
reflog object reachability. These object-presence flags refer to content
identities anywhere in the corresponding ref set; they are not claims that a
file was published at its current path.

Structured path references are also checked against the C4.2-I 30-record
manifest, the C4.2-J 232-entry manifest, the preserved GN 114-entry
manifest, and the expanded H/J 125-entry manifests. Exact per-file
resolutions are included in the JSON inventory. Narrative-text references
outside these manifests were not exhaustively searched.

The shared `gn/source/c4.2-source-manifest.json` in GN/H/J has SHA-256
`d3edfd73c4ac9f183f145d49fac4d01e8ca5aaf552f681ddd2bdd253dbccf5a7`.
This is not the unavailable historical correction-record preimage
`43fb851cf45fdcc9910215cc7d13cd6364860d32891febd203ef6f7c33474719`.
The historical test-index preimage `0ad1d9e1e407393b797ace9b04be6a6cd30de45ad00b898e493ffc41b4752697`
also remains unavailable.

The current main checkout is based on C4.1 and has 27 baseline untracked
entries, including its nested J worktree pointer and the untracked I/J
documentary packages. WC1's own reports were generated after the source
snapshot and are intentionally excluded from these baseline candidate
counts; the final WC1 manifest inventories those reports separately.

### CRLF/LF and tracked-status anomalies

Raw SHA-256 values are over the exact checkout bytes. The report does not
normalize historical records. `git hash-object --path` is recorded as a
separate canonical object identity because the system Git configuration
enables `core.autocrlf=true` and sampled text paths use `text=auto`.

J's corrected `capture.py` and `driver.py` are checked out as CRLF text and
have different raw bytes from their C4.2 HEAD blobs. Their normalized clean
Git blob IDs also differ from the original HEAD IDs, confirming substantive
source corrections rather than line-ending-only changes. H has the same two
corrected normalized identities. Four additional H porcelain `M` entries
have identical HEAD/index/worktree clean blob IDs and empty `git diff`
output; they are status-only anomalies and are not classified as content
changes.

No conclusions about historical checkout materialization are inferred from
Git blob bytes alone. Existing historical CRLF/LF discrepancies remain
preserved as recorded.
