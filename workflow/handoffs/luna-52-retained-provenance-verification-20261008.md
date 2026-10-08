---
tpcn_handoff:
  agent: "Luna-52 retained provenance verification"
  luna_identifier: "Luna-52"
  descriptive_name: "Historical source compatibility and public check adversarial coverage"
  task_id: "luna-52-retained-provenance-verification-20261008"
  component: "Luna-47B historical analyzer provenance and Luna-47F public verification"
  status: "complete — clean-checkout validation PASS; Luna-0 documentation follow-up PASS"
  contract_version: "1.1"
  branch: "main"
  base_revision: "e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e"
  result_revision: "publication commit containing this handoff"
  dependencies:
    - "Luna-52 authorization commit bdd97f8fee77b1477103fc9101c622ee8611f2c7"
    - "Luna-0 governance handoff workflow/handoffs/luna-0-review-luna51-authorize-luna52-20261008.md"
    - "Luna-51 execution/review publication e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e"
    - "Luna-47B retained protocol, result, validation, and execution handoff"
    - "Luna-47F public replay and retained evidence"
  owner: "Project owner; next review by independent Luna-0"
  classification:
    - "correction-only provenance and test coverage"
    - "no scientific replay or architecture change"
    - "PASS — independent documentation follow-up review completed"
  hypothesis: "Historical analyzer provenance and current reviewed source identity can be verified separately while retaining exact historical reconstruction and public mutation rejection."
  counter_hypothesis: "Separating historical/current source identities or invoking public CLI checks may weaken retained evidence protection or change scientific outputs."
  interfaces_relied_on:
    - "Git pinned revisions/blobs for historical and current Luna-46 analyzer source"
    - "Luna-47B retained protocol, source identities, and exact evidence files"
    - "Luna-47F public experiments/luna47f/diagnostic.py --check path"
    - "Luna-47F twelve consumed input identities and protected runtime snapshot"
  label_information_boundary:
    - "No labels or task outcomes entered TPCN computation."
    - "All replay inputs were already retained artifacts; tests did not generate neural or task evidence."
  timing_assumptions:
    - "No neural timing was evaluated."
  reset_boundaries:
    - "No TPCN runtime was created or reset."
  resource_bounds:
    - "No scientific experiment, training, topology, efficacy, sensitivity, or hardware run."
    - "Public CLI mutation fixtures ran only in disposable local Git clones."
  authorized_scope:
    - "Authenticate and use the exact historical Luna-46 analyzer object for Luna-47B retained reconstruction."
    - "Check reviewed current Luna-46 source identity separately from the historical source."
    - "Add Luna-47B source, protocol, result, validation, and input identity controls."
    - "Add isolated subprocess adversarial tests through Luna-47F's real --check entry point, including live pre/post mutation."
    - "Allow only the bounded Luna-52-owned current source/test/handoff paths through the Luna-47F uncommitted-change scope gate."
    - "Update the Luna-52 execution handoff, workflow, and changelog."
  unauthorized_scope:
    - "No historical protocol or retained artifact edits, regeneration, or rebaseline."
    - "No Luna-46 scientific code or output change."
    - "No changes to neural behavior, routing, recurrence, thresholds, eligibility, growth, or scientific verdicts."
    - "No A01-A15 change, ACP, hardware equivalence claim, or Luna-53."
  controls:
    - "Fetched origin; verified HEAD == origin/main == bdd97f8fee77b1477103fc9101c622ee8611f2c7, clean worktree, and authorization ancestry before edits."
    - "Recorded all seven protected artifact hashes before and after; all remained byte-identical."
    - "Historical Luna-46 analyzer source was retrieved from Git, checked against its expected Git blob and against the recorded Luna-47B execution revision."
    - "Current Luna-46 source was independently checked against the reviewed Luna-51 revision/blob; only exact Git LF-to-CRLF materialization was accepted for checkout bytes."
    - "The full deterministic Luna-47B reconstruction test fails if current analyzer verification functions are substituted for the loaded historical analyzer module."
    - "Luna-47F negative and positive CLI cases ran in cloned temporary repositories, not in the authoritative checkout."
    - "Live mutation harness altered only a disposable clone and verified the CLI's actual pre/post protected snapshot error."
    - "No protected file was modified in the authoritative checkout."
  measurements:
    - "Starting full suite: 1,670 passed, 1 failed, 1 skipped; sole failure was the Luna-47B current-source-equals-historical-source assertion."
    - "Starting direct Luna-47F `python experiments/luna47f/diagnostic.py --check`: PASS: retained analysis, replay, inputs, code and protected hashes."
    - "Final full suite: 1,693 passed, 1 skipped, zero failures/errors."
    - "Historical/core and Luna-34 through Luna-45 selection: 286 passed."
    - "Independent review at 522a5dbf67be1f188f8f8a6e4fc0d1bad4872a23 found all ten public CLI tests failed before CLI invocation because the clean published clone had no verifier change to commit."
    - "Corrective public CLI and bootstrap selection: 12 passed, 58 deselected; all ten real public CLI cases plus both bootstrap-state tests passed."
    - "Three retained-result/protocol/current-source mutation cases rejected through Luna-47B `reconstruct()`."
    - "Corrective full suite: 1,698 passed, 1 skipped, zero failed/errors; final clean committed-state run recorded after publication."
  information_boundary_check:
    - "PASS: no evidence or analysis output was fed into TPCN computation."
  hardware_mapping:
    - "Not applicable; no hardware execution or equivalence claim."
  architecture_invariants_touched:
    - "No A01-A15 clause changed."
  preserves:
    - "Luna-44 canonical fixture and parked historical Linux regeneration limitation."
    - "Luna-46 verdict remains MIXED."
    - "Luna-47 remains non-integrated; task efficacy and useful structural growth are unestablished."
    - "Luna-47G remains synthetic tolerance evidence; hardware equivalence is unestablished."
    - "Alternate-runtime downstream scientific sensitivity remains UNKNOWN / NOT TESTED."
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna47b/diagnostic.py"
    - "tests/test_luna47b_gain.py"
    - "experiments/luna47f/diagnostic.py"
    - "tests/test_luna47f_diagnostic.py"
    - "workflow/handoffs/luna-52-retained-provenance-verification-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added:
    - "Historical/current analyzer pin separation, source retrieval, Git object byte integrity, and unauthorized current checkout controls."
    - "Full retained reconstruction exercises the dynamically loaded historical analyzer while current analyzer verification functions are replaced with test failures."
    - "Retained Luna-47B result/validation and protocol mutation rejection; consumed Luna-45 input mutation rejection through reconstruction."
    - "Ten public Luna-47F --check subprocess cases: consumed input mutation, wrong historical Git identity substitution, protocol mutation, configuration mutation, retained result mutation, retained validation mutation, same-path content substitution, unrelated repository evolution, exact LF/CRLF materialization, and live pre/post mutation."
    - "Two CLI clone bootstrap states: changed verifier commits when required; already-committed identical verifier proceeds without a no-op commit."
    - "Three Luna-47B retained result, protocol, and current-source substitutions rejected through the actual `reconstruct()` route."
  tests_passing:
    - "Luna-52-specific selection: 22 passed, 79 deselected."
    - "Luna-47B focused suite: 28 passed."
    - "Luna-47F diagnostic and retained suites: 73 passed."
    - "Luna-46 provenance suite: 175 passed, 1 Windows directory-symlink privilege skip."
    - "Luna-44/Luna-51 provenance suites: 21 passed."
    - "Historical/core plus Luna-34 through Luna-45 regression selection: 286 passed."
    - "Full repository suite: 1,693 passed, 1 skipped, zero failed/errors."
    - "Clean-checkout corrective full suite: 1,698 passed, 1 skipped, zero failed/errors; the sole skip remains the Windows directory-symlink privilege limitation."
    - "Luna-47B corrective suite: 31 passed."
    - "Luna-47F diagnostic and retained suites: 75 passed."
    - "Luna-44/Luna-46 regressions: 196 passed, 1 Windows directory-symlink privilege skip."
    - "Luna-51/materialization/non-mutation selection: 8 passed."
    - "Core/runtime/topology plus Luna-34 through Luna-45 selection: 377 passed."
    - "Public clean `python experiments/luna47f/diagnostic.py --check`: exit 0."
    - "Changed Python files compile; `git diff --check` passes."
  tests_failed: []
  tests_not_run:
    - "No scientific/neural experiment, task efficacy, topology growth, sensitivity comparison, or hardware run."
    - "Fresh historical CPython 3.12.3/Linux/glibc 2.39 Luna-44 regeneration remains unavailable and was not attempted."
  assumptions:
    - "The historical analyzer Git blob at the pinned authorization/execution revisions is the authoritative Luna-47B verifier implementation; repository Git object integrity is trusted."
    - "The single Windows directory-symlink skip remains a host privilege limitation, not a Luna-52 failure."
  unresolved:
    - "None for the Luna-52 correction; scientific mechanism and efficacy questions are separate."
  recommended_next_agent:
    - "Project owner through Luna-0 for a separately bounded scientific question; no automatic scientific conclusion."
---

# Luna-52 retained provenance verification execution

## Clean-checkout corrective pass — 2026-10-08

**CORRECTIVE PASS COMPLETE — CLEAN-COMMIT VALIDATION PASS; LUNA-0 DOCUMENTATION FOLLOW-UP PASS.**
The clean-checkout failure reported by Luna-0 was reproduced: all ten public
CLI tests stopped because `_cli_repository()` tried to commit verifier bytes
already present at `HEAD`. The bootstrap now compares staged verifier content
to `HEAD`, commits only when it differs, propagates actual Git errors, and
verifies that the temporary repository is clean before returning. Focused
tests exercise both an already-committed verifier and a changed verifier that
must be committed, then introduce a committed adversarial input mutation.

The public subprocess helper confirms it launched the intended
`diagnostic.py --check` arguments. All ten public CLI adversarial cases pass,
including live mutation detection through the real check process. Luna-47B
adds three route-level tests: `reconstruct()` rejects retained result,
protocol, and unreviewed current analyzer changes. Historical/current source
pins and all seven protected artifact bytes remain unchanged.

Corrective validation: Luna-47B **31 passed**; Luna-47F diagnostic and
retained **75 passed**; Luna-44/Luna-46 **196 passed, 1 Windows symlink
privilege skip**; Luna-51/materialization/non-mutation **8 passed**;
historical/core selection **377 passed**; full suite **1,698 passed, 1
skipped, zero failures/errors**. The sole skip remains the existing Windows
`WinError 1314` directory-symlink privilege limitation.

The exact clean published correction commit
`0d49c780ee1f4fd63089b1ee9ae17f156c80c668` was validated with the full suite
(**1,698 passed, 1 skipped**), the focused public CLI/bootstrap selection
(**12 passed**), the combined Luna-47B/Luna-47F suites (**106 passed**), and
the public `python experiments/luna47f/diagnostic.py --check` (**PASS**).
All seven protected artifact hashes matched their pinned values after the
commit; `HEAD` matched `origin/main` and the worktree was clean.

The first independent Luna-0 review confirmed the test routes, production
verifier boundary, and protected artifact status, but returned BLOCK because
the workflow page and changelog still said clean-commit validation was
pending. Luna-0 then reviewed the documentation-only correction at published
commit `ef257f5030fba5814c0f8a2c729a4f740e90f576` and returned **PASS**:
validation and review status are aligned, the handoff records the earlier
BLOCK and its correction, no scientific-successor authorization was claimed,
and no artifacts changed. That follow-up closes the Luna-52 review gate.

## Outcome

**OBSERVED:** Luna-47B historical reconstruction now retrieves and executes
the authenticated Luna-46 analyzer source from Git revision
`789dda5988daf72f375d9713bd76a6da2b9e8b34`, path
`run_luna46_depth_scaling_diagnostic.py`, Git blob
`08f217daec167b2abc82f5988dba660c19f4ae0e`. The blob is also present at the
recorded Luna-47B execution revision
`38891b81754ce385c55f96e4020e2bf04c2b9a5d`.

The currently reviewed Luna-46 analyzer remains separately authenticated at
revision `e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e`, Git blob
`59d24b08ffa0a2a9a1ebe03a35ae595fb646fcd4`. Historical and current blobs
are distinct. Current checkout bytes are accepted only when byte-identical
or the exact Git LF-to-CRLF materialization. Reconstruction metadata reports
both identities and states that the historical Git object was used. The
determinism test makes use of the current analyzer's verifier functions fail
immediately; reconstruction still passes, proving it uses the isolated
historical module rather than silently substituting current source.

The exact historical analyzer SHA-256 is
`2603b710fa7f06e22a385a30a2cd407dd26466115819477b53b7861285168a0c`.
The reviewed current analyzer Git-object SHA-256 is
`8a6bfdb956b8bf6865c65265a241f79b3a1fed0775cefd59be6bcf4133262d92`;
the Windows checked-out bytes are
`fb8842c7b92ef13e9b5b657beb2f4754d0754d1bd7776c46a8c82eaa0e67155f`,
classified as the permitted exact Git LF-to-CRLF transformation.

**OBSERVED:** The original Luna-47B test failure is resolved without changing
its scientific rules or retained result. The historical source revision/blob,
execution revision, historical protocol, input evidence, retained result and
validation are independently authenticated. Wrong pins, missing objects,
modified historical bytes, altered current source, protocol/result/validation
substitution, and consumed input changes are rejected.

## Luna-47F public check

All adversarial cases use the actual
`experiments/luna47f/diagnostic.py --check` subprocess in a disposable local
Git clone. The clone commits the reviewed verification source, so each
mutation reaches the intended provenance guard instead of being rejected
solely as an uncommitted change.

| Public CLI case | Result |
|---|---|
| Unchanged authenticated evidence | PASS; exact retained replay message and exit 0 |
| Substantive consumed scientific input mutation at the same path | Rejected; nonzero exit at canonical input-byte check |
| Historical input Git identity substitution using a disposable Git replace object | Rejected; Git blob identity differs from retained baseline |
| Protocol mutation | Rejected by historical protocol materialization check |
| Configuration mutation | Rejected by consumed-input historical identity check |
| Retained diagnostic result mutation | Rejected by fixed retained-result identity |
| Retained validation mutation | Rejected by fixed retained-validation identity |
| Same-path raw phase content substitution | Rejected by exact baseline input-byte check |
| Later unrelated governance and test/source additions | PASS; exit 0 |
| Exact Git LF-to-CRLF checkout materialization | PASS; exit 0 |
| Deterministic mutation of protected validation during public check | Rejected by the actual pre/post protected snapshot comparison |

The live-mutation case uses a disposable `sitecustomize` harness that changes
the cloned validation file immediately after the CLI's pre-snapshot reads
it. The process then exits nonzero with
`protected live input changed during verification`. The authoritative
worktree and all retained evidence remain untouched.

The implementation adds only Luna-52's exact Luna-47B source/test and
execution-handoff paths to Luna-47F's uncommitted-owned-path allowlist, so the
public check remains usable while this authorized correction is in progress.
It does not relax historical input identity or unrelated committed
repository-evolution checks.

## Baseline and validation

Baseline started from authorization commit
`bdd97f8fee77b1477103fc9101c622ee8611f2c7`, with `HEAD == origin/main` and a
clean worktree. The seven protected artifact hashes below were recorded
before implementation and checked again after validation.

| Baseline procedure | Result |
|---|---|
| `python -m pytest -q -rs` | 1,670 passed, 1 failed, 1 skipped; sole failure was Luna-47B `test_full_retained_reconstruction_and_determinism` |
| `python experiments/luna47f/diagnostic.py --check` | Exit 0; `PASS: retained analysis, replay, inputs, code and protected hashes` |

| Validation command/procedure | Result |
|---|---|
| Luna-52 selection: both Luna-47B and Luna-47F files with `-k luna52` | 22 passed, 79 deselected |
| `python -m pytest -q tests/test_luna47b_gain.py` | 28 passed |
| `python -m pytest -q tests/test_luna47f_diagnostic.py tests/test_luna47f_retained.py` | 73 passed |
| `python -m pytest -q tests/test_luna46_depth_scaling_diagnostic.py` | 175 passed, 1 skipped |
| Luna-44 canonical fixture and verification tests | 21 passed |
| Core/runtime/topology plus Luna-34 through Luna-45 selection | 286 passed |
| `python experiments/luna47f/diagnostic.py --check` on final working tree | Exit 0; retained analysis, replay, inputs, code and protected hashes pass |
| `python -m py_compile` on changed Python implementation/tests | Exit 0 |
| `git diff --check` | Exit 0 |
| Full `python -m pytest -q -rs` | **1,693 passed, 1 skipped, zero failed/errors** |

The only skip is the existing Luna-46 directory-symlink test, which requires
Windows symlink privilege unavailable on this host. No skip, xfail, deleted
test, weakened assertion, or retained-artifact regeneration was introduced.

## Protected retained evidence

| Artifact | SHA-256 before and after |
|---|---|
| Luna-47B `results.json` | `b120d2cc5718649fb0d57d93611ddb89b45113e79c0d3003cf330fe092d0fb83` |
| Luna-47B `validation.json` | `1ef630d88e4699e9bcc1e5d05e2cc868f12f38a3958f8f1a065a4132df628fe0` |
| Luna-46 original retained output | `32561efb9f81996133bc930751083b2678c455668e47f0cd854e7985ad0616df` |
| Luna-46 corrective pre-label output | `1c3843127c3de1e9b380fd06571282f0c19cf48a820730bc3ffa1dd5b11e65d4` |
| Luna-46 corrective retained output | `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e` |
| Luna-47F `diagnostic.json` | `f24a56bf5a92f622c4dfdb661116a83a76df1f7b0ae0056d20920360ca3cbb7c` |
| Luna-47F `validation.json` | `e3c8cb236f57908319893c2e109a2c94f5dd8d50e6953f48810da74259a62c29` |

No protected scientific artifact changed.

## Architecture and scientific boundaries

No A01-A15 clause, ACP, neuron/routing/recurrence/threshold behavior,
eligibility rule, growth policy, fixture, scientific classification, retained
analysis, or output changed. Luna-46 remains **MIXED**. Luna-47 still does not
establish an integrated mechanism, task efficacy, or useful structural growth.
Luna-47G remains synthetic tolerance evidence; hardware equivalence is
unestablished. Alternate-runtime downstream scientific sensitivity remains
**UNKNOWN / NOT TESTED**.

> Fresh exact Luna-44 regeneration under CPython 3.12.3/Linux/glibc 2.39 remains unverified because Luna-50 lacked a usable Linux runtime. The committed canonical fixture remains the authenticated historical input; exact alternate-runtime binary64 identity is not claimed.

## Disposition and next assignment

**PASS — RETAINED PROVENANCE VERIFICATION CLOSED.** All Luna-52 acceptance
gates passed, including a meaningfully green full suite, unchanged protected
artifacts, historical/current analyzer separation, public-path adversarial
rejection, and public-path live mutation detection.

Next and only review role: independent Luna-0 review of the exact published
Luna-52 revision and this handoff. This execution authorizes no Luna-53 or
scientific follow-up.
