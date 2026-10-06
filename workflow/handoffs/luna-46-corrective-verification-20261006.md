---
tpcn_handoff:
  agent: "Luna-46 corrective verification; independent review pending"
  luna_identifier: "Luna-46"
  descriptive_name: "Output guard and critical-rate corrective verification"
  task_id: "luna-46-corrective-verification-20261006"
  component: "Downstream offline evidence analysis"
  status: "complete - MIXED; independent corrective review pending"
  contract_version: "1.2"
  branch: "copilot/luna46-depth-scaling-diagnostic"
  base_revision: "7f063b1013f0274083e70e931333446c23e47ab5"
  result_revision: "Corrective implementation 96d015ecd8f6b5684237c489898ee33e4496a1cd; this handoff and output are published in the containing commit"
  dependencies:
    - "Luna-46 authorization bb080228bac2287da49c1b47fc1484b436a59106"
    - "Luna-46 independent review 7f063b1013f0274083e70e931333446c23e47ab5"
    - "Corrective implementation 96d015ecd8f6b5684237c489898ee33e4496a1cd"
  owner: "Project owner"
  classification:
    - "OFFLINE ANALYSIS"
    - "MECHANISM DIAGNOSTIC"
    - "MIXED"
    - "corrective verification; not efficacy or production-configuration evidence"
    - "independent corrective review pending"
  hypothesis: "The path guard rejects all canonical overlap with retained evidence and the frozen Luna-44 fixture, and analytical critical-rate statuses preserve the original diagnostic verdict."
  counter_hypothesis: "Path aliases may still reach protected evidence, or corrected critical-rate handling may change classifications, retained reconciliation, or the MIXED verdict."
  interfaces_relied_on:
    - "Committed Luna-46 downstream-only analyzer at 96d015ecd8f6b5684237c489898ee33e4496a1cd"
    - "Retained Luna-44 and Luna-45 evidence and canonical fixture"
  label_information_boundary:
    - "No labels were used; analysis remained downstream-only and did not feed neural computation."
  timing_assumptions:
    - "Retained logical-time units; lambda=0.0125, tau=80, theta_Z=1.0."
    - "Critical-rate analysis is mathematical only over the signed retained recurrence and nonnegative rate domain."
  reset_boundaries:
    - "Each retained character remains independently reset; no cross-character accumulation."
  resource_bounds:
    - "320 retained sequences, at most 4096 observations per sequence, and 100 MiB input-file limit."
  authorized_scope:
    - "Add canonical overlap protection for output paths, including the frozen Luna-44 fixture."
    - "Add explicit analytical critical-rate cases required by the committed contract."
    - "Rerun the unchanged retained analysis to a new Luna-46 output path and verify fixture identity."
  unauthorized_scope:
    - "No parameter/configuration changes, sweeps, alternate runs, production/neuron/runtime/topology/fixture edits, WEMA, ACP changes, efficacy, architecture promotion, or Luna-47."
  controls:
    - "Output validation resolves canonical filesystem paths, rejects protected-tree overlap in either direction, and requires the artifacts/luna46-* namespace."
    - "Path tests use synthetic temporary layouts; symlink and junction alias cases ran without skips."
    - "The previous retained JSON was not overwritten; output is a new unique file."
    - "Reconciled retained initial/replay captures and exact replay analytical bytes."
    - "Reverified fixture manifest, file, and semantic digests after the full-suite attempt."
  measurements:
    - "Retained analysis rerun: 320 sequences, 108 reception-bearing sequences, 235 destination receptions."
    - "Categories remain 212 NO-RECEPTIONS, 33 TEMPORAL-RETENTION-LIMITED, 75 DRIVE-LIMITED, 0 CANCELLATION-LIMITED, and 0 ALREADY-CROSSING."
    - "Predeclared cutoffs remain substantial=27, material=11, and drive/cancellation=81; result remains MIXED."
    - "Critical-rate status counts: 33 UNIQUE, 32 ABSENT: NO CROSSING AT ANY NONNEGATIVE RATE, 43 NO FINITE CRITICAL RATE: SINGLETON, and 212 NOT APPLICABLE: NO RECEPTIONS."
    - "Actual maximum absolute state remains 0.8284450023885981; signed zero-decay maximum absolute state remains 2.071533974476769."
  information_boundary_check:
    - "PASS: corrected analysis reads retained evidence and emits downstream-only diagnostics; no result is fed to TPCN."
  hardware_mapping:
    - "Not applicable; no hardware execution or equivalence claim."
  architecture_invariants_touched:
    - "No A01-A15 or ACP changes; offline analysis only."
  preserves:
    - "Luna-42 PASS WITH FOLLOW-UP"
    - "Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED"
    - "Luna-44 reviewed canonical-fixture relay-propagation baseline"
    - "Luna-45 NOT SUPPORTED IN THIS SETUP"
    - "ACP-0007 unchanged/disabled; ACP-0008 experimental, opt-in, unpromoted"
  architecture_change: false
  proposal: null
  files_changed:
    - "run_luna46_depth_scaling_diagnostic.py"
    - "tests/test_luna46_depth_scaling_diagnostic.py"
    - "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json"
    - "workflow/handoffs/luna-46-corrective-verification-20261006.md"
  tests_added:
    - "Contract-to-test matrix A-G for unique, absent, already-crossing, zero-boundary, non-monotone, cancellation, and singleton/no-reception critical-rate cases."
    - "Canonical output-guard rejection and acceptance cases, including relative aliases, parent overlap, symlinks, and junctions."
  tests_passing:
    - "Focused Luna-46 suite: 167 passed."
    - "Corrected retained analysis: completed with MIXED verdict; analytical initial/replay bytes equal."
    - "Fixture verification after analysis and tests: PASS; 5,164 points, 320 sequences."
  tests_failed:
    - "Repository-wide pytest: 1 failed, 7 errors, 1 skipped, 1,325 passed. The failed test and seven setup errors are the Luna-44 pinned-source materialization checks; workers report 'authorized generator source differs from the pinned baseline'. The Git blob at pinned revision a79494cd66be28fd291ed11eddd62d342f457cfd hashes to the expected 17e581cf702fae1f56889472a967d2e8e5fec37cc041edba8247da14a0a8b5db, while a Windows temporary worktree checkout hashes to c16a099b6c27c5af15c56f90614ccfdd420b6d984dd5a810acfd5ad2e0530d44. Git core.autocrlf is true. This is consistent with the previously documented Windows/frozen-source materialization incompatibility; exact equivalence to the two baseline failure signatures was not established."
  tests_not_run:
    - "Independent Luna-0 corrective review is pending."
    - "GitHub PR description could not be updated: browser is signed out and gh has no write authentication."
    - "No CUDA execution; one test skipped because CUDA is unavailable."
  assumptions:
    - "The critical-rate solver is invoked only for same-sign retention-limited sequences; its domain is lambda >= 0, its finite boundary is bisected on [0, 0.0125], and all supporting statuses are explicit in output policy."
    - "Mixed-sign cases receive no selected root; absent or non-applicable cases receive no fabricated rate."
  unresolved:
    - "Independent verification of the corrective commit and new retained output."
    - "The exact source of the Windows temporary-worktree hash transformation should be independently reviewed; no fixture or generator source was modified."
    - "PR #6 body still describes the earlier governance-only stage."
  recommended_next_agent:
    - "Fresh read-only Luna-0 review of commit 96d015ecd8f6b5684237c489898ee33e4496a1cd, this handoff, and the new output; do not authorize Luna-47."
---

# Luna-46 corrective verification

## Outcome and scope

**OBSERVED:** Corrective implementation commit
`96d015ecd8f6b5684237c489898ee33e4496a1cd` adds a canonical output-path
guard and analytical critical-rate classifications. It changes no production
computation, topology, fixture, ACP, or prior retained output.

**OBSERVED:** The retained analysis was rerun from that pushed, clean code
revision to
`artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json`.
The artifact is 2,336,500 bytes with SHA-256
`3a54776b1186934381e585779643bd1289805880a90c00361f4ad97f3aadb601`.
Its schema is `TPCN-LUNA46-OFFLINE-1`, its recorded code revision is
`96d015ecd8f6b5684237c489898ee33e4496a1cd`, and its `MIXED` verdict and
category counts match the previously reviewed result.

The corrected analysis reports 33 `UNIQUE` mathematical boundaries, 32
drive-limited sequences with no nonnegative-rate crossing, 43 single-reception
sequences with no finite rate-dependent boundary, and 212 sequences with no
receptions. It does not select roots for mixed-sign cases or alter the
predeclared category verdict.

## Fixture and replay identity

**OBSERVED:** Fixture verification after the rerun reported:

| Identity | Value |
|---|---|
| Fixture SHA-256 | `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629` |
| Manifest SHA-256 | `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22` |
| Semantic fixture SHA-256 | `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305` |
| Fixture bytes / points / sequences | 3,451,453 / 5,164 / 320 |

The corrected initial and replay analytical outputs are byte-identical
(SHA-256 `a4220d7796d0b99c709ef3dfd265be12146d574c8644f1e0e080a9c9c808b7c0`).
The three retained phase-pair canonical byte checks also passed.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_luna46_depth_scaling_diagnostic.py` | Corrective code at `96d015e`; Windows; Python 3.11.5 | 167 passed | Focused test run |
| `python run_luna46_depth_scaling_diagnostic.py --output artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json` | Corrective code at `96d015e`; retained inputs only | `MIXED`; replay equality passed | New JSON artifact |
| Canonical fixture verification | After analysis and full-suite attempt | PASS, 5,164 points / 320 sequences | Pinned fixture, manifest, semantic digests above |
| `python -m pytest -q` | Windows checkout; Git `core.autocrlf=true` | 1 failed, 7 errors, 1 skipped, 1,325 passed | All failed/error cases are Luna-44 pinned-source materialization checks |
| Temporary pinned-source probe | Git revision `a79494cd66be28fd291ed11eddd62d342f457cfd` | Git blob matches expected SHA; temporary worktree file differs | Expected `17e581cf…a0a8b5db`; checkout `c16a099b…2e0530d44` |

The full-suite failures are recorded, not suppressed. They arise before
fixture materialization: the worker rejects the generator source hash.
Although the Git blob at the pinned revision matches the expected hash, its
Windows temporary-worktree bytes do not. This is consistent with the
previously documented platform materialization limitation, but the precise
relationship to the two earlier baseline failure signatures is unresolved.
No generator, fixture, or test expectation was changed to bypass the failure.

## Assumptions, limitations and unresolved issues

**OBSERVED:** The previously published output remains untouched. No retained
input was regenerated, no alternate configuration was run, and no parameter
was changed. Critical-rate values are analytical results only and are not
production tuning recommendations.

**UNRESOLVED:** A fresh Luna-0 reviewer must independently verify the output
guard, rate classification matrix, retained artifact identities, and the
Windows materialization exception before this corrective pass is considered
independently reviewed. PR #6 still has its stale description because no
authenticated GitHub write session is available.

## Next assignment

Request a read-only Luna-0 review of the corrective implementation, this
handoff, and the new artifact. Preserve the `MIXED` result unless independent
verification invalidates it. Do not authorize Luna-47.
