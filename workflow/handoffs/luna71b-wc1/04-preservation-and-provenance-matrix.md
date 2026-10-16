# Luna-71B-WC1 — Preservation and Provenance Matrix

Classification is based on exact worktree/ref/file inventory, not cleanliness
alone. All current worktrees are **KEEP** or **CANDIDATE — AFTER
PRESERVATION**. None is `ELIGIBLE — REVIEWED REDUNDANT`.

| Worktree | Current evidence / condition | Classification | Proposed action |
|---|---|---|---|
| `TPCN` | C4.1 governance baseline; 27 untracked entries including I/J handoffs; ignored checkpoints and Luna-47A evidence | **KEEP — ACTIVE** | Preserve baseline and all handoffs; no cleanup |
| `_worktrees/luna71b-c4-2-j` | Detached at C4.2; 2 substantive tracked changes; 217 untracked entries; corrected implementation and evidence | **KEEP — ACTIVE** | Retain entire J checkout and artifacts |
| `TPCN-luna63a` | Published historical branch; 34 ignored Luna-47A evidence files duplicated in main checkout | **KEEP — HISTORICAL** | Retain its worktree context and evidence copy |
| `TPCN-luna63b` | Clean, separately named Luna-63B design branch | **KEEP — HISTORICAL** | Preserve branch/worktree identity |
| `TPCN-luna63c` | Clean Luna-63C design branch | **KEEP — HISTORICAL** | Preserve frozen design context |
| `TPCN-luna63c-archive` | Clean archive branch with distinct commit/tree | **KEEP — HISTORICAL** | Preserve archive |
| `TPCN-luna63c-corrective` | Clean corrective reconciliation branch | **KEEP — HISTORICAL** | Preserve governance provenance |
| `TPCN-luna63c-E` | Clean lane-E branch; one ignored cache entry | **KEEP — HISTORICAL** | Preserve lane and its ref |
| `TPCN-luna63c-governance` | Clean artifact-reconciliation branch | **KEEP — HISTORICAL** | Preserve governance record |
| `TPCN-luna63c-T` | Clean lane-T branch; one ignored cache entry | **KEEP — HISTORICAL** | Preserve lane and its ref |
| `TPCN-luna63c-W` | Clean lane-W branch; one ignored runtime/cache entry | **KEEP — HISTORICAL** | Preserve lane and its ref |
| `TPCN-luna64-r4.3-pilot-20261010` | Clean; same HEAD/tree as the lifecycle-correction worktree; separate pilot branch and HEAD reflog | **CANDIDATE — AFTER PRESERVATION** | Possible worktree-only removal after archived reflog and independent review |
| `TPCN-luna64-r4.3-reward-lifecycle-correction-20261010` | Clean; same HEAD/tree as pilot worktree; separate correction branch and HEAD reflog | **CANDIDATE — AFTER PRESERVATION** | Possible worktree-only removal after archived reflog and independent review |
| `TPCN-luna66-functional` | 6 untracked source/test/evidence files | **KEEP — HISTORICAL** | Preserve unique Luna-66 artifacts |
| `TPCN-luna67-four-class` | 13 untracked source/test/evidence files | **KEEP — HISTORICAL** | Preserve unique Luna-67 artifacts |
| `TPCN-luna68-prediction-omission` | 15 untracked source/result files | **KEEP — HISTORICAL** | Preserve unique Luna-68 artifacts |
| `TPCN-luna70-corrective-readout` | 14 untracked source/result/manifest files | **KEEP — HISTORICAL** | Preserve Luna-70 results and provenance |
| `TPCN-luna71b` | 34 untracked plans, capture records, tests, sources, and evidence | **KEEP — HISTORICAL** | Preserve Luna-71B source/replay lineage |
| `TPCN-luna71b-c4` | 4 untracked C4 inventory/review artifacts | **KEEP — HISTORICAL** | Preserve C4 recovery documents |
| `TPCN-luna71b-c4-2` | 76 untracked C4.2 source, plan, fixture, and test artifacts | **KEEP — ACTIVE** | Preserve checkpoint worktree and every artifact |
| `TPCN-luna71b-c4-2-gn` | 116 untracked GN source, fixture, tests, and results | **KEEP — HISTORICAL** | Preserve original GN package unchanged |
| `TPCN-luna71b-c4-2-h` | 6 status-marked tracked entries (2 substantive source files plus 4 status-only); 200 untracked entries | **KEEP — ACTIVE** | Preserve corrected H and original GN evidence |
| `TPCN-r14-publication` | Clean, separately named R14 governance branch | **KEEP — HISTORICAL** | Preserve governance package |

The full unique-content and duplicate evidence is in
[`05-duplicate-content-analysis.json`](./05-duplicate-content-analysis.json).
The two Luna-64 worktrees have identical checked-out Git trees and no
untracked/ignored evidence, but each has a distinct branch name and HEAD
reflog. This is not sufficient for a `KEEP` downgrade: removal would erase
worktree-specific reflog/context unless first exported. All worktrees with a
shared baseline tree (Luna-66 through Luna-71B and the C4.2 family) contain
distinct untracked evidence and are not duplicates as research artifacts.

## Provenance and authority

- C4.1 and C4.2 published revisions remain the authoritative baselines
  listed in the worktree inventory.
- I/J documentary files are untracked in the C4.1 main checkout. Their
  exact identities are not promoted by local agent refs or object presence.
- J is detached at the published C4.2 commit; the corrected capture/driver
  files are uncommitted working-tree changes.
- The C4.2-N fixture and parameters are new, independently identified
  experimental inputs, not historical R6 recovery.
- No branches or refs are deleted; duplicate content remains in its
  originating paths to retain scientific role and provenance.
