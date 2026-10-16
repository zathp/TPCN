# Luna-71B-WC1 — Independent Luna-0 Review

## Verdict

**PASS WITH FINDINGS** — the preservation inventory and identity counts are
internally consistent. No worktree is eligible for removal. Historical
`43fb…` and `0ad1…` preimages remain unresolved. The reviewer also identified
a closeout gap at review time: the exact 16-path publication proposal did
not yet have its review report or final manifest/sidecar. This gap is closed
documentarily by this review record and the artifact manifest; publication
remains unauthorized.

The Luna-0 review was read-only. No repository or worktree files were
modified by the reviewer. No cleanup, deletion, pruning, neural execution,
commit, fetch, or publication was performed.

## Reviewed baseline and exact evidence

Main checkout: branch
`governance/luna71b-c4-1-ppc11-freeze`, HEAD
`11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`, tree
`1c124b2105e3c30593e28e9b503c72325a56f567`. The report snapshot was
`2026-10-16T18:21:20.892251Z`.

Luna-0 verified the following exact report bytes. These identities bind the
pre-closeout review inputs; the final manifest separately binds this
independent-review record and the refreshed adjudication.

| Evidence file | Bytes | Raw SHA-256 |
|---|---:|---|
| `01-worktree-inventory.md` | 5,597 | `4bcc2206fff9ba66f755e9821d307be2cf125e74b81bfe344eda7b3ab0efad9e` |
| `01-worktree-inventory.json` | 587,001 | `d231c5b1d995edf298b6ea966a07144dba05db8fdc9270976ee6335cdb92d46a` |
| `02-branch-ref-reflog-inventory.md` | 4,145 | `8dc2b2acfe87961db8899361a793998e21e1e1ae6752006b61e7199e3e165a6b` |
| `02-branch-ref-reflog-inventory.json` | 119,696 | `5dd2941cc1ec6df865aaa5bcd58a41ff55514b3b14f76985207303b743f93f9f` |
| `03-untracked-and-ignored-inventory.md` | 4,960 | `bc8c57b89f487c973169cc0920af3dd32655bec200595f0e509dddb273d2397f` |
| `03-untracked-ignored-artifact-inventory.json` | 1,667,517 | `23a7673996765472e96511cd59a691400409610c20cf0595a605436c0995dd43` |
| `03-git-normalized-file-identities.json` | 598,294 | `3a92c36acf95f8e44819decc5ee4754f39b371f088cab75e88738a73ac594ccc` |
| `04-preservation-and-provenance-matrix.md` | 5,208 | `c051455e80c05ab2c6bf19b0fd77836d6f088a1a321c4e3c0728cea7a7e94093` |
| `05-duplicate-content-analysis.md` | 3,162 | `b048aac7492da87da841300afdc25aeb2d596224453d8ac7a099bfa294441f33` |
| `05-duplicate-content-analysis.json` | 1,230,969 | `9d242dbd4117ebcc64f1c43a5da61dfbf70fd2649256578e1bd093c18daac74e` |
| `06-c4.2-i-j-publication-readiness.md` | 11,237 | `3bc383fc49550289111bf9620360e0e3db4679001ad6dcc002922ec2be568f20` |
| `07-proposed-cleanup-plan.md` | 2,910 | `98b210d6fee1b6c02d2b23182e5ea301910013172bea216358695528101ec0ca` |
| `09-final-adjudication.md` | 7,402 | `dd138e8e7992a76d0698f68d28a4e121d24e38c8dba6570443a4993a89dd5109` |

## Independent checks

- **Worktrees:** all 23 registered paths exist. Recorded HEADs, trees, and
  branch/detached states matched. The 11 dirty, one detached, zero staged
  counts describe the inventory snapshot before WC1 reports were created.
- **Refs and Git metadata:** 29 local heads, 35 remote refs, 182 agent refs,
  and zero tags reconcile to 246 refs. The remote assessment is only against
  cached refs; no fetch or live remote check occurred. Reflog-only commits,
  unreachable blobs, and the missing canonical empty-tree object are
  accurately reported; these remain preservation risks.
- **Raw identities:** the reviewer independently recomputed 861
  untracked/research-ignored instances as 306 unique raw identities, 266
  absent from cached remotes. Eight tracked-status paths add five identities,
  two absent from cached remotes. Combined: 869 instances, 308 identities,
  and 268 absent from cached remotes. Duplicate counts reconcile from 133
  groups/555 excess copies to 135 groups/561 excess copies after the tracked
  overlay. Four H entries are substantive changes; four are status-only.
- **C4.2-I/J and GN manifests:** I's 30/30 declared inputs match locally,
  with 13 in the main checkout and 17 in other worktrees. J's current
  232-entry, 55,999-byte manifest matches locally, but Luna-0's earlier
  review was of a different 55,286-byte predecessor. The original GN
  manifest verifies 114/114 entries; the expanded H/J manifest verifies
  125/125 in each worktree. These are separate identities.
- **Source-manifest reconciliation:** original GN
  `experiments/luna71b_c4_2/gn/source-manifest.json` is 20,446 bytes,
  SHA-256 `d9483916…`; H/J same-path manifests are 20,446 bytes,
  SHA-256 `1c12a5f1…`; shared
  `gn/source/c4.2-source-manifest.json` is 14,826 bytes,
  SHA-256 `d3edfd73…`. They are untracked worktree evidence absent from
  their C4.2 base trees; the stated commits identify base revisions, not
  commits containing these files. None replaces historical
  `43fb851cf45fdcc9910215cc7d13cd6364860d32891febd203ef6f7c33474719`;
  historical test-index preimage
  `0ad1d9e1e407393b797ace9b04be6a6cd30de45ad00b898e493ffc41b4752697`
  is also unresolved.
- **Cleanup:** neither Luna-64 worktree is currently eligible for removal.
  Identical HEAD/tree does not erase the separate branch and worktree
  reflog/context. A future worktree-only removal could lose that context
  without preservation and independent review first.

## Findings and disposition

1. The exact WC1 publication allowlist was prospective at review time and
   missing the review record and final manifest/sidecar. This documentary
   closeout creates those artifacts and updates the adjudication. It does
   not authorize staging or publication; any future staged-tree review is
   still required.
2. The historical `43fb…` source-manifest and `0ad1…` test-index preimages
   remain unresolved. The current `d3ed…`, `d948…`, and `1c12…` artifacts
   are not historical substitutes.

No proposed removal or publication is approved by this review. See
[`09-final-adjudication.md`](./09-final-adjudication.md) for final status and
the exact separately authorized publication request.
