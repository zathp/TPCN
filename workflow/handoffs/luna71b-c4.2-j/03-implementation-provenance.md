# Luna-71B-C4.2-J — Candidate implementation provenance

**Disposition:** J-only static implementation and synthetic validation are
complete; no neural execution or adoption claim. This document distinguishes
published Git identity, H candidate material, and J worktree bytes.

## Published baselines

| Source | Identity |
|---|---|
| C4.1 PPC-11 contract | Commit `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`; manifest SHA-256 `2f18d694784a6a583b0a7c01e6cc89f1313c2d65c7c6b5346a7cd4d993d3f1fa` |
| Published C4.2 | Commit `e91818a5c974282e848dc43e52d3c0a534dcbf45`; tree `f14f23f0eb00e8b4aa8946e34acc71ab46ab5749` |
| C4.2-I final inventory | `workflow/handoffs/luna71b-c4.2-i/10-artifact-manifest.json`, 100,231 bytes, SHA-256 `1cc1f19b288c20601cfa7853382d0aff4f5b5392afbc8cc185ef0752b861b775` |
| Luna-0-audited I inventory candidate | `workflow/handoffs/luna71b-c4.2-i/10-review-inventory-candidate.json`, 98,884 bytes, SHA-256 `c7deff6e407f5e3f8f19ace657bc3616d101420b2552a01303229fa078918b4c` |

The nine C4.2-I analysis and adjudication documents are individually
identified in the final I inventory. The I worktree and package are retained
unchanged.

## H candidate and J isolation

H remains the separate dirty worktree
`C:\Users\Patrick\Documents\ActiveCode\TPCN-luna71b-c4-2-h`, branch
`governance/luna71b-c4-2-h-corrections`, HEAD
`e91818a5c974282e848dc43e52d3c0a534dcbf45`. The J worktree is
`C:\Users\Patrick\Documents\ActiveCode\TPCN\_worktrees\luna71b-c4-2-j`,
detached at the same published C4.2 commit and tree. No H file was modified
to create or populate J.

Two H-modified tracked implementation files were copied byte-for-byte into
the J worktree after checking their C4.2 Git blobs:

| Path | C4.2 HEAD blob | H/J input bytes | Raw SHA-256 |
|---|---|---:|---|
| `experiments/luna71b_c4_2/ppc11/capture.py` | `ea8da564f9e977d087c1b937379a5a544313079f` | 13,978 | `9d85a05e767c227a9a21d5d789b9ca4b9c0cdbf6e4bd9d9e15d70c5314eee84f` |
| `experiments/luna71b_c4_2/ppc11/driver.py` | `79ea73e0409e689f17604c82a06c3a51218b7d1b` | 14,930 | `91639f7866967b18501b98e8ecc67554e6d77194e1c30445ca3ce2d7dc9f9de6` |

The exact H GN artifact manifest at
`experiments/luna71b_c4_2/gn/gn-artifact-manifest.json` is 37,135 bytes,
SHA-256 `b2cf392f1d596b352e5af0add83c269c91fc1c0a19f701a9e54de4f41eb1ec16`.
Its 125 listed artifact files were copied and byte/hash-verified in J. The
H GN source manifest is 20,446 bytes, SHA-256
`1c12a5f149d022f9e7a4304aa2b32f0110fc802f855d018bee32014580ae5095`;
all 80 bilateral source-copy rows were independently checked by the I
inventory and are present as H inputs. Their original H paths and manifests
are preserved in the separate H worktree.

The six H source-copy rows marked `modified_from_checkpoint=true` are
`tpcn/eligibility.py`, `tpcn/luna70_readout_learning.py`, and
`tpcn/predictive_coding.py` on both original and instrumented sides. The H
source manifest records each baseline and candidate digest. J-specific hook
changes, if needed, are confined to J copies; they do not alter the preserved
H GN source inventory.

The completed J package includes a separate v2 injected-pair interface and
identity-bound source/implementation manifests. These are candidate bytes,
not a production neural backend:

| J artifact | Bytes | SHA-256 |
|---|---:|---|
| `experiments/luna71b_c4_2/j/j-source-manifest.json` | 18,762 | `605a730361da6252173d5466e11fa412ffdecca45c26ffabc31ca384b23d2ec0` |
| `experiments/luna71b_c4_2/j/j-source-manifest.sha256` | 66 | `5665d7b7c8ed617edc471b914ec65fb5da9e6e61467a1ad695505aaea3e2f6c0` |
| `experiments/luna71b_c4_2/j/j-implementation-manifest.json` | 1,822 | `5625a596ed8a134de0fce0ebaa79eaae6749b9f6f4672f65d606d3d63326540e` |
| `experiments/luna71b_c4_2/j/j-implementation-manifest.sha256` | 66 | `4b3f6da15f8e69d6c4573e3643dac56c3afcc1c06230984fbbfeffc0db10e66c` |
| `experiments/luna71b_c4_2/j/driver_v2.py` | 6,464 | `e388d229a60a221dfe0a683ba446dfd71b2b40d86fab669efec35ab221bbe4cb` |
| `experiments/luna71b_c4_2/j/CORRECTIVE-PROVENANCE.md` | 28,655 | `3ac6e6f3b57f21e208066757c6d3f671ae58326db7365d7e62f2303927168b13` |

The J source manifest inventories 80 original/instrumented source copies;
the implementation manifest binds the v1 overlays and v2 implementation.
The corrected J handoff verifies all 125 H GN artifact paths against the
copied GN manifest. The final J synthetic suite is 35 passed and includes
fail-closed source-trigger settlement linkage, typed P11 diagnostics,
unsupported lifecycle-coverage rejection, fixture/exposure input binding,
exact source callsites, and process-control exception propagation. A
source-order settlement without an earlier lifecycle reference remains
incomplete; no settlement is synthesized. Detailed file sizes, full digests,
test outcomes, and limitations are recorded in
[`04-focused-validation-and-regression-disposition.md`](./04-focused-validation-and-regression-disposition.md)
and the J corrective provenance report.

## Fixture identity

The new fixture remains separate from historical R6:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Fixture ID `L71B-C4.2-N-FOURCLASS-SEED17-V1` manifest | 2,368 | `839e58df80da69cdf7b63618afc9626b85a9aa9817885931189c58a6f9658f40` |
| Whole event payload | 39,796 | `520b1cedfeefe8b285d02dba7d26583f6581ac29cd82dc8571a4b9ba5ed4970e` |
| Initial parameters | 112 | `5a53d0cc7e41a7431d584bd711f0a1d0ba735a69f6e84b1b9298fa41f289948a` |

The unresolved historical `43fb851cf45fdcc9910215cc7d13cd6364860d32891febd203ef6f7c33474719`
source-manifest and `0ad1d9e1e407393b797ace9b04be6a6cd30de45ad00b898e493ffc41b4752697`
test-index references remain unchanged. C4.1's historical preparation and
six split-identity requirements remain mandatory for any R6 claim; this
fixture cannot satisfy or waive them.

## Scope boundary

The J code candidate uses the identity-bound H source/capture implementation
as its starting point, with separately hashed J-only v2 observation hooks.
C4.1 PPC-11 v1 contract/schema remains frozen; the H-corrected `capture.py`
and `driver.py` are explicit overlays relative to published C4.2 and are not
claimed byte-identical to that checkout. Synthetic/static checks establish
neither runtime passivity nor neural parity. No fixture was executed through
the neural runner. Neural execution, training/inference, pilot, commit/push,
and publication remain unauthorized.
