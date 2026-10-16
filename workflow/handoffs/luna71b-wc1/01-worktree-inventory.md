# Luna-71B-WC1 — Worktree Inventory

## Scope and snapshot

Read-only snapshot of the TPCN repository at **2026-10-16 18:21:20 UTC**,
before WC1 report files were created. Repository root:
`C:\Users\Patrick\Documents\ActiveCode\TPCN`.

The published C4.1 baseline is `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`.
The published C4.2 checkpoint is `e91818a5c974282e848dc43e52d3c0a534dcbf45`,
tree `f14f23f0eb00e8b4aa8946e34acc71ab46ab5749`.

**Discovery:** 23 registered worktrees; all 23 paths existed. The 22
TPCN-named sibling directories and the nested J worktree all correspond to a
registered worktree. No missing registration or unregistered sibling was
found. There are 11 worktrees with tracked changes and/or untracked entries,
one detached worktree, and no staged entries. Ignored-only caches do not make
a worktree dirty for this count.

| Worktree | Branch / HEAD | HEAD | Tree | Staged / modified / untracked / ignored-matching |
|---|---|---|---|---:|
| `TPCN` | `governance/luna71b-c4-1-ppc11-freeze` | `11b6f52e9aa6` | `1c124b2105e3` | 0 / 0 / 27 / 32 |
| `_worktrees/luna71b-c4-2-j` | detached | `e91818a5c974` | `f14f23f0eb00` | 0 / 2 / 217 / 7 |
| `TPCN-luna63a` | `experiment/luna63a-binary-adaptive-decay` | `1c3e33d6285c` | `e4eff84c5964` | 0 / 0 / 0 / 9 |
| `TPCN-luna63b` | `experiment/luna63b-local-pcn-design` | `fe3ebe5fdd2e` | `bf331efa4032` | 0 / 0 / 0 / 0 |
| `TPCN-luna63c` | `experiment/luna63c-nonlinear-excursion-design` | `a303ebb835b7` | `a4cbdf1c30b2` | 0 / 0 / 0 / 0 |
| `TPCN-luna63c-archive` | `archive/luna63c-local-artifacts-20261010` | `f6611520c9c2` | `9d29a60cf42a` | 0 / 0 / 0 / 0 |
| `TPCN-luna63c-corrective` | `governance/luna63c-corrective-reconciliation` | `3b0bc14df01e` | `e77b3e7aa52e` | 0 / 0 / 0 / 0 |
| `TPCN-luna63c-E` | `experiment/luna63c-stage-a-E` | `651f18fdf3c7` | `f3ddf5abfa49` | 0 / 0 / 0 / 1 |
| `TPCN-luna63c-governance` | `governance/luna63c-artifact-reconciliation` | `8f5e785bd2e4` | `841d8718e10f` | 0 / 0 / 0 / 0 |
| `TPCN-luna63c-T` | `experiment/luna63c-stage-a-T` | `0a8c34b7e6fe` | `77b90fd1d3f5` | 0 / 0 / 0 / 1 |
| `TPCN-luna63c-W` | `experiment/luna63c-stage-a-W` | `17907c67d52c` | `42a03741b2eb` | 0 / 0 / 0 / 1 |
| `TPCN-luna64-r4.3-pilot-20261010` | `experiment/luna64-track-b-r4.3-pilot-20261010` | `d93ef139a1fe` | `640fd9e8e311` | 0 / 0 / 0 / 0 |
| `TPCN-luna64-r4.3-reward-lifecycle-correction-20261010` | `experiment/luna64-r4.3-reward-lifecycle-correction-20261010` | `d93ef139a1fe` | `640fd9e8e311` | 0 / 0 / 0 / 0 |
| `TPCN-luna66-functional` | `experiment/luna66-minimal-functional-learning` | `f117ce51e7a8` | `abab7d92ecb4` | 0 / 0 / 6 / 3 |
| `TPCN-luna67-four-class` | `experiment/luna67-four-class-temporal-learning` | `f117ce51e7a8` | `abab7d92ecb4` | 0 / 0 / 13 / 3 |
| `TPCN-luna68-prediction-omission` | `experiment/luna68-prediction-omission-routing` | `f117ce51e7a8` | `abab7d92ecb4` | 0 / 0 / 15 / 3 |
| `TPCN-luna70-corrective-readout` | `experiment/luna70-corrective-readout-learning` | `f117ce51e7a8` | `abab7d92ecb4` | 0 / 0 / 14 / 4 |
| `TPCN-luna71b` | `experiment/luna71b-instrumented-learning` | `f117ce51e7a8` | `abab7d92ecb4` | 0 / 0 / 34 / 5 |
| `TPCN-luna71b-c4` | `experiment/luna71b-c4-bilateral-capture` | `f117ce51e7a8` | `abab7d92ecb4` | 0 / 0 / 4 / 0 |
| `TPCN-luna71b-c4-2` | `governance/luna71b-c4-2-checkpoint` | `e91818a5c974` | `f14f23f0eb00` | 0 / 0 / 76 / 4 |
| `TPCN-luna71b-c4-2-gn` | `experiment/luna71b-c4-2-gn` | `e91818a5c974` | `f14f23f0eb00` | 0 / 0 / 116 / 5 |
| `TPCN-luna71b-c4-2-h` | `governance/luna71b-c4-2-h-corrections` | `e91818a5c974` | `f14f23f0eb00` | 0 / 6 / 200 / 6 |
| `TPCN-r14-publication` | `governance/luna65-r14-documentary-freeze` | `0511762b46aa` | `b9319cda10a4` | 0 / 0 / 0 / 0 |

The exact absolute paths, full HEAD/tree/upstream values, registration
metadata, complete staged/modified/untracked paths, byte sizes, raw SHA-256,
Git object identities, and relevant ignored file identities are in
[`01-worktree-inventory.json`](./01-worktree-inventory.json). The nested J
worktree pointer is counted as an untracked entry in the parent checkout and
is inventoried separately as a worktree; it is not double-counted as a file.

### Identity and line-ending handling

Raw SHA-256 is computed over exact on-disk bytes. The repository uses
Git SHA-1 object IDs, system `core.autocrlf=true`, and `text=auto` for sampled
text paths. The companion identity inventory records both the raw-byte blob
ID and `git hash-object --path`'s clean/filter result. No LF/CRLF conversion
was applied by the audit. A blob hash is not a historical checkout hash.

The H checkout has four porcelain `M` entries whose index, HEAD, and clean
blob IDs match and whose `git diff` is empty; these are status/stat-cache
anomalies, not four source edits. H's `capture.py` and `driver.py` changes
are byte-identical to J's two corrected source files. J/H therefore have two
distinct corrected source contents duplicated across two worktrees, plus
four H status-only entries. No staged changes were found.

No Git submodule entries (`160000`) were found. The only nested registered
worktree discovered is the J checkout inside the main repository.

## Preservation outcome

No worktree is classified `ELIGIBLE — REVIEWED REDUNDANT`. The only obvious
identical source-tree pair is the two clean Luna-64 worktrees; their separate
branch and HEAD-reflog contexts remain preservation-sensitive. See the
preservation matrix and cleanup proposal before considering even a
worktree-only removal.
