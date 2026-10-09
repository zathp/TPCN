---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent Luna-56 checkout-materialization review"
  task_id: "luna-0-independent-review-luna56-20261009"
  component: "Historical Git-object identity and LF/CRLF checkout verification"
  status: "complete - correction properties PASS; repository provenance closure BLOCKED"
  contract_version: "1.2"
  branch: "main"
  base_revision: "f691e543d24343de14e07c682af6c9ead40d2ded"
  result_revision: "f691e543d24343de14e07c682af6c9ead40d2ded (reviewed source state)"
  dependencies:
    - "Luna-56 authorization a2ffea9d9e265a5e28caab77cc0377ae29ea4309"
    - "Luna-56 implementation ec4ff50b4c8ca85243d986c9ebb7aa67f6ba7888"
    - "Luna-56 publication f691e543d24343de14e07c682af6c9ead40d2ded"
    - "Luna-46, Luna-47F, Luna-53, Luna-54 and Luna-55 historical evidence records"
  owner: "Project owner; no successor authorized"
  classification:
    - "independent read-only provenance review"
    - "checkout-materialization correction properties PASS"
    - "repository-wide provenance closure NOT ESTABLISHED"
  hypothesis: "The Luna-56 verifier accepts only fixed historical Git-object bytes or their exact governed LF-to-CRLF checkout transform, while rejecting substantive changes and substitutions."
  counter_hypothesis: "Any broader normalization, mutable identity, historical substitution, or failed required regression gate prevents closure."
  interfaces_relied_on:
    - "Luna-47F retained-artifact and public --check verifier"
    - "Luna-53 PINNED_FILES historical-object verifier"
    - "Luna-46 catalog identity and checkout verifier"
  label_information_boundary:
    - "No scientific computation, label use, replay, or result regeneration occurred."
  timing_assumptions:
    - "Not applicable; read-only provenance review."
  reset_boundaries:
    - "Not applicable; no experiment."
  resource_bounds:
    - "Targeted provenance tests, one full suite, Git object/hash checks, and temporary isolated baseline worktrees."
  authorized_scope:
    - "Independently verify Luna-56's exact LF/CRLF acceptance and strict historical identity rejection."
    - "Publish an independent review handoff and additive workflow/changelog status."
  unauthorized_scope:
    - "No implementation or scientific artifact changes."
    - "No investigation of the six Luna-55 noncrossing streams."
    - "No Luna-57 or other scientific successor authorization."
  controls:
    - "Fetched origin; verified HEAD == origin/main == f691e543d24343de14e07c682af6c9ead40d2ded and clean worktree before review."
    - "Verified the authorization, implementation, and publication commits are ancestors of the reviewed HEAD."
    - "Reproduced the five baseline failures in a disposable a2ffea9 LF-materialized worktree using exact historical Git blob bytes; removed that worktree afterward."
    - "Ran focused regression modules and the full suite against the published source state."
    - "Compared protected artifacts and .gitattributes across authorization-to-review revisions; no changes."
  measurements:
    - "The five reported baseline failures reproduce under exact LF materialization: one L46 catalog checkout-label assertion; three L47F tests stop at the same retained-result hash gate; one L53 pinned-L46 SHA/length gate."
    - "The exact five current regression selectors pass: 8 passed, including the four L47F result/validation LF/CRLF combinations."
    - "The broader focused batch reports 281 passed, 3 failed and 1 skipped; all three failures are in pre-existing Luna-55 integrity assertions, not Luna-56 files."
    - "The full suite at the reviewed source state reports 1,729 passed, 3 failed and 1 skipped in Python 3.11.4 on Windows."
    - "The full-suite failures are two Luna-55 retained-phase checks stopping at the L54 control-initial raw SHA pin, and one Luna-55 assertion expecting the old L46 helper SHA to differ from its CRLF checkout SHA."
    - "Current L54 control-initial bytes hash to 2d63eb997676b38a6f09a128a8ce353bdec4e32667d589f9a2089c62b2334751, while the Luna-55 test pin is b38f974c55536c118ae45c672a0afa0c59ee005af4112840ae2919cf1233b76d. No pin or artifact was changed."
    - "The full-suite skip is test_luna46_depth_scaling_diagnostic.py's directory-symlink privilege case (WinError 1314); the reported CUDA-unavailable skip was not observed in this run."
    - "The Luna-47F public `--check` reports PASS for retained analysis, replay, inputs, code, and protected hashes."
    - "All protected artifacts and .gitattributes are unchanged from the Luna-56 authorization tree; all Luna-55 artifacts are unchanged since publication 8369c8e70209c553be0662b6d705177308151d68."
  information_boundary_check:
    - "PASS: no neural execution or scientific information flow."
  hardware_mapping:
    - "Not applicable; no hardware execution."
  architecture_invariants_touched:
    - "None; no A01-A15 or ACP change."
  preserves:
    - "Every historical object ID, materialization hash, semantic digest, protocol/configuration, and scientific artifact."
    - "The Luna-55 10/16 RR result and six noncrossers without further analysis."
    - "No claim of task efficacy, hardware equivalence, or cross-runtime binary64 identity."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna56-20261009.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Five Luna-56 regression selectors: 8 passed."
    - "Luna-47F public `--check`: PASS."
    - "Focused comparison, mutation, wrong-object, missing-object/file, and materialization tests passed within the broader batch."
    - "Protected-artifact no-diff and historical identity checks passed."
  tests_failed:
    - "Full suite: three Luna-55 integrity tests fail as detailed in the review findings; suite is not green."
  tests_not_run:
    - "Fresh historical Linux Luna-44 regeneration: PARKED LIMITATION; not run."
    - "Cross-runtime exact binary64 identity: NOT CLAIMED and not tested."
    - "No Luna-55 noncrosser analysis or scientific successor."
  assumptions:
    - "The reported L55 pin mismatch is outside Luna-56 scope; no attempt was made to repair or reinterpret it."
    - "Full-suite results are specific to the observed Windows checkout, Python 3.11.4 and current privilege environment."
  unresolved:
    - "Repository-wide full regression gate and provenance closure remain blocked until the three L55 failures and environment-conditioned skip discrepancy are resolved by a separately authorized correction-only decision."
  recommended_next_agent:
    - "Project owner / Luna-0: separately authorize a bounded, non-scientific review of the L55 retained-artifact test pin mismatch and checkout-dependent assertion; no Luna-57."
---

# Luna-56 independent review

## Disposition

**The Luna-56 comparison correction passes Properties A and B. The published
`PASS — CHECKOUT-MATERIALIZATION PROVENANCE CLOSED` disposition is not accepted
as repository-wide closure in this review.** The exact five repaired selectors,
public Luna-47F check, and mutation tests pass. However, the required full-suite
gate is not green at this reviewed checkout: three Luna-55 integrity tests fail,
and the sole skip differs from the reported CUDA-unavailable skip.

This is a read-only review. No source, test, scientific artifact, configuration,
protocol, `.gitattributes`, ACP, or architecture contract was changed. The
independent review and governance updates are the only publication changes.

## Revisions and initial state

| Item | SHA / result |
|---|---|
| Reviewed authoritative revision | `f691e543d24343de14e07c682af6c9ead40d2ded` |
| Luna-56 authorization | `a2ffea9d9e265a5e28caab77cc0377ae29ea4309` |
| Luna-56 implementation | `ec4ff50b4c8ca85243d986c9ebb7aa67f6ba7888` |
| Luna-56 publication | `f691e543d24343de14e07c682af6c9ead40d2ded` |
| Fetch / branch | `origin` fetched; `HEAD == origin/main` before review |
| Ancestry | Authorization, implementation, and publication commits all ancestors |
| Initial worktree | Clean |

The current working checkout uses `core.autocrlf=true`. The reported baseline
failures depend on exact LF checkout bytes, so they were reproduced in an
isolated disposable worktree at the authorization revision after materializing
the three relevant paths from their fixed historical Git blobs. The baseline
worktree was removed. A control run using the default CRLF materialization does
not reproduce those baseline failures.

## Baseline failure classifications

All five exact test nodes failed under the controlled exact-LF baseline:

| Test | Observed baseline failure | Classification |
|---|---|---|
| `tests/test_luna46_depth_scaling_diagnostic.py::test_luna51_catalog_identity_is_pinned_to_the_expected_git_object` | Expected `exact-Git-LF-to-CRLF-checkout`; observed `exact` for the pinned L45 catalog blob. | Checkout-label expectation defect; historical identity remains the pinned catalog blob. |
| `tests/test_luna47f_diagnostic.py::test_luna51_protocol_and_execution_code_keep_their_historical_git_identities` | `retained Luna47F result identity differs` before source checks. | Exact LF retained result was rejected against its recorded CRLF checksum. |
| `tests/test_luna47f_diagnostic.py::test_luna51_retained_artifact_hashes_reject_result_and_validation_substitution` | Same retained-result identity error before either substitution branch. | Same shared verification gate, not an independent artifact defect. |
| `tests/test_luna47f_retained.py::test_reproduction_check_is_read_only` | Public `--check` exited before the non-mutation assertion with retained-result identity error. | Same shared verification gate blocked the read-only check. |
| `tests/test_luna53_retention.py::test_pinned_inputs_reconcile_without_running_neurons` | SHA mismatch for the historical Luna-46 diagnostic; the fixed recorded SHA and length identify its exact CRLF form. | Checkout-materialization defect, not a changed source object. |

The baseline run reported five failures. The three Luna-47F failures share one
early retained-result gate.

## Comparison semantics and adversarial review

The Luna-47F retained verifier obtains bytes at the fixed
`39bedbce47055a7b180593ea312c6b646510c566` revision, checks the fixed Git blob,
and accepts checkout bytes only when equal to the object or its exact
LF-to-CRLF transform. The Luna-53 PINNED_FILES path first checks the historical
revision/path/blob and passes those canonical bytes to the strict checkout
comparator. No broad whitespace, JSON, Unicode, or content normalization is
used on these corrected paths.

| Property / attack | Independent evidence |
|---|---|
| Exact LF acceptance | Passed in current test fixtures and exact-LF baseline reproduction. |
| Exact CRLF acceptance | Passed; the four Luna-47F result/validation representation combinations pass. |
| Changed character | Rejected by focused Luna-47F mutation tests. |
| Changed number | Rejected by focused Luna-47F mutation tests. |
| Ordinary whitespace add/remove | Rejected by focused adversarial tests. |
| Same-path result/validation substitution | Rejected. |
| Mixed, lone-CR, missing-final-newline, and appended-byte forms | Rejected. |
| Wrong revision / wrong object | Rejected against fixed historical literals. |
| Missing object / missing checkout file | Rejected. |
| Wrong materialization identity for the L46 catalog | Rejected; test-owned revision/blob/hash expectations remain fixed. |

### Historical identities

- **Luna-46 catalog:** revision
  `d1f901d3d995dc013f22dd086ae1ed8ffd28293d`, blob
  `b1aaef4006422f321922bfb58425e4fb646d96b9`, canonical SHA-256
  `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`.
  The current test accepts exact LF and exact CRLF while retaining wrong-blob
  and mutation rejection.
- **Luna-47F result:** revision
  `39bedbce47055a7b180593ea312c6b646510c566`, blob
  `74c6859555caf8cb9c5a51f713080b238d716c79`, canonical SHA-256
  `aec4e589102b0e40a31de725f97471072fdfb03fa7ee0a263d716f7de0d7e3ef`,
  4,431,419 bytes; the recorded exact-CRLF SHA remains
  `f24a56bf5a92f622c4dfdb661116a83a76df1f7b0ae0056d20920360ca3cbb7c`.
- **Luna-47F validation:** same publication revision, blob
  `c70c9f1d4ae6f5712b672d54e2e71cef0629cc2a`, canonical SHA-256
  `176069a349584347fd312e58439aee5f7128356f20d32c29b1b79ac18677f3cf`,
  6,773 bytes; the recorded exact-CRLF SHA remains
  `e3c8cb236f57908319893c2e109a2c94f5dd8d50e6953f48810da74259a62c29`.
- **Luna-53 Luna-46 pin:** authorization revision
  `04305a2917195888cbbcccf378eba7971551e9b5`, blob
  `9506369d97babf7bc0ef15ed52efb738dcdcd549`, canonical SHA-256
  `54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51`,
  2,337,376 bytes. The unchanged hash
  `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e`
  and 2,337,377-byte size identify the exact CRLF form. Its semantic digest
  remains `f72ba671f6d1618ab60cf81d85ac664395646de43c3ad77c226f41b9aa657628`.
- **Luna-47F original output:** the earlier commit
  `8cddf9d5d3fc0ea6971dc54645e8033c290dc852` remains in the history/object
  record; no output was overwritten or re-dated.

The Luna-47F public `--check` was executed and returned:
`PASS: retained analysis, replay, inputs, code and protected hashes`. Its fixed
12-entry consumed-input set and historical protocol/code revisions remain
covered; unrelated later repository evolution is not substituted for those
historical inputs.

## Protected evidence and Luna-55

`git diff --quiet` confirms no artifact changed between the Luna-56
authorization and reviewed publication revisions. The `.gitattributes` file
also did not change in that range. Luna-55 artifacts are unchanged since
publication `8369c8e70209c553be0662b6d705177308151d68`; its 421-route evidence,
10/16 RR response, six noncrossers, controls, and summary are preserved. No
Luna-55 scientific run or analysis was performed.

The reviewer checkout's full suite nevertheless exposes a separate retained
integrity gate problem: two Luna-55 tests stop at the expected raw SHA for
`artifacts/luna54/control-initial.json` (the current bytes match the Luna-54
published file hash `2d63eb997676b38a6f09a128a8ce353bdec4e32667d589f9a2089c62b2334751`;
the Luna-55 test pin is `b38f974c55536c118ae45c672a0afa0c59ee005af4112840ae2919cf1233b76d`).
A third test assumes the historical L46 helper SHA differs from checkout SHA;
in this checkout both are `0d32926f...`. These failures were not repaired or
reinterpreted because they are outside Luna-56's authorized code/evidence
scope. They block repository-wide provenance closure.

## Validation performed

| Command / procedure | Environment | Result |
|---|---|---|
| Exact five baseline nodes at authorization revision with exact LF objects | Disposable worktree; Python 3.11.4 / Windows | 5 failed with the classifications above. |
| Exact five current regression nodes | Published source state | 8 passed. |
| Luna-46, Luna-47F, Luna-53, Luna-54 and Luna-55 focused modules | Published source state | 281 passed, 3 failed, 1 skipped; the failures are Luna-55 as above. |
| `python experiments\luna47f\diagnostic.py --check` | Published source state | PASS; retained analysis, replay, inputs, code and protected hashes. |
| `python -m pytest -q -rs --tb=short` | Windows, Python 3.11.4, `core.autocrlf=true` | 1,729 passed, 3 failed, 1 skipped. |
| Sole full-suite skip | Windows privilege limitation | L46 directory-symlink test skipped with WinError 1314; the reported CUDA-unavailable skip was not observed. |
| Protected-artifact and `.gitattributes` diff against authorization | Git tree comparison | No changes. |
| Luna-55 artifact diff from publication | Git tree comparison | No changes. |

The reported result of 1,732 passed, 1 skipped, 0 failed and its CUDA-only skip
was not reproduced in this checkout. The full-suite gate is therefore
**BLOCKED**, not green. Fresh historical Linux Luna-44 regeneration remains a
**PARKED LIMITATION**. Cross-runtime exact binary64 identity is **NOT CLAIMED**.

## Provenance closure classification

| Gate | Independent disposition |
|---|---|
| Source provenance | CLOSED for corrected Luna-47F/Luna-53 historical-object paths. |
| Retained-artifact integrity | PARTIAL; corrected targets pass, but the independent L55 gate is red. |
| Historical/current source separation | CLOSED for fixed Luna-47F and Luna-53 identities; no current-HEAD substitution. |
| Checkout-materialization handling | CLOSED for exact LF / exact CRLF correction paths and adversarial fixtures. |
| Public verification path | CLOSED for Luna-47F `--check`. |
| Full regression gate | BLOCKED: 3 failures and a symlink privilege skip; reported result not reproduced. |
| Fresh historical Linux Luna-44 regeneration | PARKED LIMITATION. |
| Cross-runtime exact binary64 identity | NOT CLAIMED. |

**Final answer to the review question:** Luna-56's corrected comparison accepts
the exact Git LF object or its exact LF-to-CRLF transform and rejects the
tested scientifically meaningful changes and substitutions. That correction
is justified. The broader claim that the repository provenance sequence is
closed is not established until the independently observed L55 test failures
and full-suite discrepancy receive a separately authorized, non-scientific
resolution.

No Luna-57 or scientific successor is authorized. The six unresolved
Luna-55 target streams remain untouched.
