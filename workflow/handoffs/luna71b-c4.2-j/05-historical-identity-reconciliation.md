# Luna-71B-C4.2-J — Historical identity reconciliation

**Disposition:** PARTIAL; historical R6 identity remains BLOCKED where the
unavailable preimages are required. No historical record has been rewritten.

## Verified identities available in this round

| Artifact | Revision / provenance | Bytes | SHA-256 |
|---|---|---:|---|
| Published C4.1 PPC-11 contract manifest | Commit `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76` | — | `2f18d694784a6a583b0a7c01e6cc89f1313c2d65c7c6b5346a7cd4d993d3f1fa` |
| Published C4.2 source tree | Commit `e91818a5c974282e848dc43e52d3c0a534dcbf45`, tree `f14f23f0eb00e8b4aa8946e34acc71ab46ab5749` | — | Git identities above |
| C4.2-I final artifact manifest | Preserved I handoff package | 100,231 | `1cc1f19b288c20601cfa7853382d0aff4f5b5392afbc8cc185ef0752b861b775` |
| C4.2-I preserved candidate manifest | Preserved I handoff package | 98,884 | `c7deff6e407f5e3f8f19ace657bc3616d101420b2552a013029fa078918b4c` |
| H source manifest used by J | H worktree source inventory, copied and identity-checked in J | 20,446 | `1c12a5f149d022f9e7a4304aa2b32f0110fc802f855d018bee32014580ae5095` |
| New C4.2-N fixture manifest | `L71B-C4.2-N-FOURCLASS-SEED17-V1`; new lineage only | 2,368 | `839e58df80da69cdf7b63618afc9626b85a9aa9817885931189c58a6f9658f40` |
| New C4.2-N event payload | Fixture named above | 39,796 | `520b1cedfeefe8b285d02dba7d26583f6581ac29cd82dc8571a4b9ba5ed4970e` |
| New initial-parameter payload | Fixture named above | 112 | `5a53d0cc7e41a7431d584bd711f0a1d0ba735a69f6e84b1b9298fa41f289948a` |

The listed C4.2-I documents were previously verified against the final I
manifest. These identities identify the available current and candidate
bytes; they do not recover the missing historical preimages.

## Unresolved historical references

| Historical reference | Available evidence | Missing evidence | Disposition |
|---|---|---|---|
| Source-manifest preimage `43fb851cf45fdcc9910215cc7d13cd6364860d32891febd203ef6f7c33474719` | Historical correction record refers to it; a separate source-manifest reference was reported with prefix `d3ed…` | Exact preimage bytes, full identity for the `d3ed…` reference, byte size, revision, and committed blob identity are unavailable in the verified package | UNRESOLVED; do not reconcile by filename or assume normalization |
| Test-index preimage `0ad1d9e1e407393b797ace9b04be6a6cd30de45ad00b898e493ffc41b4752697` | Historical record refers to this identity | Exact preimage bytes, byte size, revision, and committed blob identity are unavailable; the final C4.2 artifact test identity is a distinct available identity | UNRESOLVED; preserve both references |

Without those preimages, it is not possible to determine whether the
discrepancies were caused by different revisions, line-ending normalization,
different contents or inventories, superseded artifacts, incorrect
historical references, or another cause. No raw SHA-256, byte size, Git blob
identity, or provenance is asserted for unavailable bytes.

## Scope consequence

The new C4.2-N fixture has its own verified lineage and is not a recovered
historical R6 fixture. It cannot substitute for either missing preimage or
waive C4.1's historical preparation and split-identity requirements.
Published PPC-11 clauses that depend on the unavailable R6 identities remain
blocked; the historical identity gate is not reconciled. Historical evidence
and superseded identities remain preserved unchanged.
