---
tpcn_handoff:
  agent: "Luna-46 corrective verification and independent Luna-0 review"
  luna_identifier: "Luna-46"
  descriptive_name: "Output guard and critical-rate corrective verification"
  task_id: "luna-46-corrective-verification-20261006"
  component: "Downstream offline evidence analysis"
  status: "complete - PASS / MIXED; independent corrective verification"
  contract_version: "1.2"
  branch: "copilot/luna46-depth-scaling-diagnostic"
  base_revision: "7f063b1013f0274083e70e931333446c23e47ab5"
  result_revision: "Metric reporting code 8eab7112e61a24d260da6984450a17a49bc90578; regenerated output records source revision 6af1c0167c6a506477d6fe3f9c40b19692fce0ec; updated handoff is published in its containing commit"
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
    - "independent Luna-0 corrective review PASS"
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
    - "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006-pre-label-correction.json"
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
    - "GitHub PR description could not be updated: browser is signed out and gh has no write authentication."
    - "No CUDA execution; one test skipped because CUDA is unavailable."
  assumptions:
    - "The critical-rate solver is invoked only for same-sign retention-limited sequences; its domain is lambda >= 0, its finite boundary is bisected on [0, 0.0125], and all supporting statuses are explicit in output policy."
    - "Mixed-sign cases receive no selected root; absent or non-applicable cases receive no fabricated rate."
  unresolved:
    - "The full suite remains failed on Windows pinned-source materialization; no failure was suppressed."
    - "Mixed-sign critical-rate cases are conservatively classified as uniqueness-unproven; the implementation does not enumerate all roots."
    - "Output-path validation is not a defense against concurrent replacement of parent filesystem aliases between validation and writing."
    - "PR #6 body still describes the earlier governance-only stage."
  recommended_next_agent:
    - "No successor is authorized; preserve MIXED and do not authorize Luna-47."
---

# Luna-46 corrective verification

## Outcome and scope

**OBSERVED:** Corrective implementation commit
`96d015ecd8f6b5684237c489898ee33e4496a1cd` adds a canonical output-path
guard and analytical critical-rate classifications. Reporting correction
commit `8eab7112e61a24d260da6984450a17a49bc90578` separates inter-arrival
statistics from event rates without changing the underlying counts or rates.
No production computation, topology, fixture, or ACP changed.

**OBSERVED:** The corrected retained analysis was rerun from pushed code
revision `6af1c0167c6a506477d6fe3f9c40b19692fce0ec` to
`artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json`.
The regenerated artifact is 2,337,376 bytes with SHA-256
`54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51`.
Its schema is `TPCN-LUNA46-OFFLINE-1`, and its `MIXED` verdict and category
counts match the previously reviewed result. The formerly reviewed JSON was
preserved byte-for-byte as
`artifacts/luna46-depth-scaling-diagnostic-corrective-20261006-pre-label-correction.json`.

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

## Independent corrective review

**OBSERVED:** Luna-0 independently reviewed publication commit
`3fba4ac3b60e6d4f5dd6c08a5a8e9af54110e7b2`, corrective code revision
`96d015ecd8f6b5684237c489898ee33e4496a1cd`, and the prior output now
preserved under the `pre-label-correction` filename. Disposition:
**PASS — corrective evidence review; scientific verdict remains MIXED**.
The reviewer independently checked the path guard, analytical-rate rationale,
all 33 retained input identities, raw enqueue/reception reconciliation,
recurrence, replay, categories, cutoffs, and frozen fixture hashes. No
corrective mismatch was found.

The review clarifies that mixed-sign cases are conservatively classified as
uniqueness-unproven; this is not an exhaustive signed-root solver and does not
enumerate possible multiple roots. It also notes the ordinary filesystem
time-of-check/time-of-use boundary: a concurrent replacement of parent
symlinks or junctions after validation is outside the guard's guarantee.
Neither caveat changes the retained classifications or verdict.

### Metric semantic/reporting correction

The depth-comparison object previously called `frequency` measured interval
count divided by summed first-to-last arrival duration within streams. This is
the reciprocal of mean inter-arrival duration, not routed event count divided
by the observation window. It is now explicitly `interval_statistics`, with
interval count, observed duration, mean interval duration, reciprocal mean
interval, and units. The distinct matched-window quantity is now
`common_fixture_event_rate`, with routed reception count, observation-window
duration, and events per retained logical-time unit.

| Hop | Interval count / duration | Mean interval duration | Reciprocal mean interval | Event count / common window | Event rate |
|---|---:|---:|---:|---:|---:|
| Source -> relay | 1,418 / 40,194.06825478446 | 28.345605257252796 | 0.03527883743968141 intervals per time unit | 1,715 / 89,358.19552048748 | 0.01919241978881272 receptions per time unit |
| Relay -> destination | 127 / 10,798.242968719456 | 85.02553518676737 | 0.011761172661876184 intervals per time unit | 235 / 89,358.19552048748 | 0.0026298651022571362 receptions per time unit |

This is a semantic/reporting correction: no prior interval-rate or
event-rate numerical value changed; the corrected report makes their
different denominators explicit and adds the mean interval duration.
Inter-arrival gap distributions remain duration statistics. No separate
per-gap reciprocal-frequency aggregate is claimed.

This disposition is not owner approval, architecture promotion, or
authorization of Luna-47. No repository files were changed and no analysis
was rerun as part of the independent review.

The metric naming/reporting correction below was made after this independent
review. It changes only report field names and explicit metric definitions;
the retained counts, numerical interval/event rates, category counts, and
verdict are unchanged. That reporting-only correction is not represented as a
separate Luna-0 review.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_luna46_depth_scaling_diagnostic.py` | Metric-reporting code at `8eab711`; Windows; Python 3.11.5 | 167 passed | Focused test run |
| `python run_luna46_depth_scaling_diagnostic.py --output artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json` | Analyzer source revision `6af1c0167c6a506477d6fe3f9c40b19692fce0ec`; retained inputs only | `MIXED`; replay equality passed | Regenerated corrected JSON artifact |
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

**OBSERVED:** The previously reviewed output remains preserved byte-for-byte
under the `pre-label-correction` filename; the canonical corrective artifact
was regenerated with explicit metric names. No retained input was regenerated,
no alternate configuration was run, and no parameter was changed.
Critical-rate values are analytical results only and are not production
tuning recommendations.

**UNRESOLVED:** The full suite remains failed on the Windows pinned-source
materialization checks described above. The reviewer independently confirmed
that the Git LF-to-CRLF conversion under global `core.autocrlf=true` explains
the source-hash difference; this is a platform materialization limitation,
not a new Luna-46 corrective regression. The PR #6 description remains stale
because GitHub CLI is unauthenticated and the browser session is signed out.

## Next assignment

No further successor is authorized. Preserve the `MIXED` result. Do not
authorize Luna-47.
