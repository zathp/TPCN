# WC1-A3 four-commit preservation evidence

This publication records the isolated recovery and verified local preservation
of four historical Git commits. The complete Git bundle is intentionally not
published; only its filename, byte size, and SHA-256 checksum are included.

## Disposition

- Four-commit bundle: locally verified and restored independently.
- Local source protection refs: three created after independent acceptance;
  the fourth was not created because its source closure lacks the empty-tree
  object.
- Source missing-tree condition: unchanged and unresolved.
- Independent off-machine backup:
  `OFF_MACHINE_BACKUP_PENDING_OWNER_DESTINATION`.
- Worktree cleanup: not authorized.
- Publication of preservation refs: not authorized.
- Final Luna-0 review of the local A3 state: **PASS WITH FINDINGS**.
- Review scope limitation: architecture contract source paths were
  unavailable, so Luna-0 reviewed archival preservation only.

## Files

- [WC1-A3 preservation report](WC1-A3-preservation-report.md)
- [Luna-0 final review](independent-final-review.md)
- [Luna-0 preliminary ref acceptance](preliminary-ref-acceptance.md)
- [WC1-A2 independent review](WC1-A2-independent-review.md)
- [WC1-A2 final adjudication (sanitized publication derivative)](WC1-A2-final-adjudication.md)
- [Publication inventory and source-file classification](publication-inventory.md)
- [Publication manifest](wc1-a3-publication-manifest.json)
- [Bundle checksum](wc1-a2-four-commits.bundle.sha256)

The manifest lists the exact published file identities. The adjacent
`.sha256` file authenticates the manifest's raw bytes. It also records Git blob
identities calculated with the publication worktree's path filters, to make
line-ending normalization auditable.

