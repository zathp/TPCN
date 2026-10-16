# WC1-A1 - Publication and remote-backup recommendation

## Current disposition

No artifact was committed, published, pushed, or copied off-machine. The verified partial bundle and this report package reside only in the local dedicated directory `C:\Users\Patrick\Documents\ActiveCode\TPCN-preservation\luna71b-wc1-a1\`, outside the TPCN worktrees. Off-machine preservation was not authorized. The bundle preserves three commits; it must not be described as complete preservation of all four.

## Exact scope for a later owner authorization

Recommend a separate, explicit owner decision for an off-machine integrity-preserving backup of:

1. The exact partial bundle `wc1-a1-three-commits-partial.bundle`, 347,973,648 bytes, SHA-256 `97fc628794b0ba4aeb90392aa5d16cfd8a4823dbe7eb2a19da0ec87c00a19a08`.
2. The nine WC1-A1 report files `01-four-commit-identity-inventory.md`, `02-reference-reachability-analysis.md`, `03-preservation-bundle-and-recovery.md`, `04-independent-preservation-review.md`, `05-local-protection-ref-verification.md`, `06-missing-tree-investigation.md`, `07-unreachable-object-analysis.md`, `08-preservation-adjudication.md`, and `09-publication-and-remote-backup-recommendation.md`.
3. The final `10-artifact-manifest.json` and its SHA-256 sidecar `10-artifact-manifest.sha256`.

Use the manifest's exact file sizes, SHA-256 identities and source dependencies as the transfer allowlist. The destination/storage service and any Git branch are intentionally unspecified because no remote destination or publication authorization was supplied. Prefer controlled artifact storage for the 348 MB bundle rather than placing it in a governance Git commit. Do not push refs or publish the reports under this gate.

A separate follow-up authorization is needed before investigating recovery/repair of the missing empty-tree object, creating a complete four-target bundle, creating any source-repository protective refs, or publishing anything. The historical `43fb...` source-manifest and `0ad1...` test-index preimages remain unresolved; no recovery is inferred from these commits. Until then, preserve the local bundle and all original refs, reflogs and worktrees unchanged.