# WC1-A1-R - Repository-local relocation report

## Disposition

Relocated the WC1-A1 package by exact-byte copy into `workflow/archives/wc1-a1/`.
The original external files remain in place. The historical manifest and its
checksum sidecar were copied unchanged. The bundle remains explicitly partial:
it contains three recovered commits, not all four WC1 targets.

## Relocation map

External source directory:
`C:\Users\Patrick\Documents\ActiveCode\TPCN-preservation\luna71b-wc1-a1\`

| Original filename | Repository-local destination |
|---|---|
| `01-four-commit-identity-inventory.md` | `workflow/archives/wc1-a1/reports/01-four-commit-identity-inventory.md` |
| `02-reference-reachability-analysis.md` | `workflow/archives/wc1-a1/reports/02-reference-reachability-analysis.md` |
| `03-preservation-bundle-and-recovery.md` | `workflow/archives/wc1-a1/reports/03-preservation-bundle-and-recovery.md` |
| `04-independent-preservation-review.md` | `workflow/archives/wc1-a1/reports/04-independent-preservation-review.md` |
| `05-local-protection-ref-verification.md` | `workflow/archives/wc1-a1/reports/05-local-protection-ref-verification.md` |
| `06-missing-tree-investigation.md` | `workflow/archives/wc1-a1/reports/06-missing-tree-investigation.md` |
| `07-unreachable-object-analysis.md` | `workflow/archives/wc1-a1/reports/07-unreachable-object-analysis.md` |
| `08-preservation-adjudication.md` | `workflow/archives/wc1-a1/reports/08-preservation-adjudication.md` |
| `09-publication-and-remote-backup-recommendation.md` | `workflow/archives/wc1-a1/reports/09-publication-and-remote-backup-recommendation.md` |
| `10-artifact-manifest.json` | `workflow/archives/wc1-a1/manifests/10-artifact-manifest.json` |
| `10-artifact-manifest.sha256` | `workflow/archives/wc1-a1/manifests/10-artifact-manifest.sha256` |
| `wc1-a1-three-commits-partial.bundle` | `workflow/archives/wc1-a1/local-bundles/wc1-a1-three-commits-partial.bundle` |

The original manifest records absolute source paths and is intentionally
unchanged. Its detached checksum remains valid for the copied manifest.
Destination identity checks compare each copied file's raw byte count and
SHA-256 to the original and, for the ten manifest-listed payloads, to the
manifest. The relocation report is an additional record and is not inserted
into the historical manifest.

## Bundle handling

The relocated bundle was verified with `git bundle verify`; its size is
347,973,648 bytes and its SHA-256 is
`97fc628794b0ba4aeb90392aa5d16cfd8a4823dbe7eb2a19da0ec87c00a19a08`.
It remains a three-commit partial bundle. This relocation does not resolve
the missing/effectively ambiguous empty-tree dependency or preserve the
fourth commit.

The exact archive-relative bundle path is excluded using one repository-local
rule in `.git/info/exclude`:

`/workflow/archives/wc1-a1/local-bundles/wc1-a1-three-commits-partial.bundle`

`git check-ignore -v` confirms that rule matches the relocated bundle.
Documentary files remain visible as untracked files and are eligible for
separate review and staging under the allowlist below.

## Proposed documentary publication allowlist

No files were staged, committed, pushed, merged or published in this gate.
If separately authorized, the narrow allowlist is:

- `workflow/archives/wc1-a1/reports/01-four-commit-identity-inventory.md`
- `workflow/archives/wc1-a1/reports/02-reference-reachability-analysis.md`
- `workflow/archives/wc1-a1/reports/03-preservation-bundle-and-recovery.md`
- `workflow/archives/wc1-a1/reports/04-independent-preservation-review.md`
- `workflow/archives/wc1-a1/reports/05-local-protection-ref-verification.md`
- `workflow/archives/wc1-a1/reports/06-missing-tree-investigation.md`
- `workflow/archives/wc1-a1/reports/07-unreachable-object-analysis.md`
- `workflow/archives/wc1-a1/reports/08-preservation-adjudication.md`
- `workflow/archives/wc1-a1/reports/09-publication-and-remote-backup-recommendation.md`
- `workflow/archives/wc1-a1/reports/11-relocation-report.md`
- `workflow/archives/wc1-a1/manifests/10-artifact-manifest.json`
- `workflow/archives/wc1-a1/manifests/10-artifact-manifest.sha256`

The `.bundle` is expressly excluded from ordinary Git publication. Publication
requires separate authorization and exact staged-tree review.

## Scope confirmation

The external originals are retained. No deletion, overwrite, tracked source
change, Git history rewrite, object repair, garbage collection, neural
execution, commit or push was performed. The local bundle exclusion is the
only repository configuration adjustment; it is in `.git/info/exclude`, not
a tracked ignore file.
