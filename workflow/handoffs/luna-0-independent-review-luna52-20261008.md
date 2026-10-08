---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent post-execution review of Luna-52"
  task_id: "luna-0-independent-review-luna52-20261008"
  component: "Luna-47B historical provenance and Luna-47F public verification"
  status: "complete - LUNA-52 CORRECTION REQUIRED; no scientific successor assessed"
  contract_version: "1.2"
  branch: "main"
  reviewed_revision: "a700024cb44e1c24df1d1284b96a9e75aeb1e261"
  result_revision: "publication commit containing this handoff"
  dependencies:
    - "Luna-52 contract .github/agents/luna-52.agent.md"
    - "Luna-52 execution a700024cb44e1c24df1d1284b96a9e75aeb1e261"
    - "Luna-52 execution handoff workflow/handoffs/luna-52-retained-provenance-verification-20261008.md"
    - "Luna-51 provenance correction and Luna-50 runtime limitation records"
    - "Luna-46 MIXED and Luna-47A/B/D/F/G retained evidence"
  owner: "Project owner; next bounded correction requires authorization"
  classification:
    - "independent post-execution provenance review"
    - "Luna-47B historical/current source separation CORRECT"
    - "Luna-47F public verification behavior demonstrated; committed adversarial test harness fails from clean published checkout"
    - "LUNA-52 CORRECTION REQUIRED"
    - "no scientific successor decision"
  hypothesis: "The Luna-52 implementation preserves historical evidence while independently exercising the public guard, and all committed acceptance tests pass from the published revision."
  counter_hypothesis: "A clean published checkout exposes a test-fixture defect that prevents public adversarial tests and the full regression suite from passing."
  interfaces_relied_on:
    - "Luna-47B historical and current Luna-46 analyzer Git objects"
    - "Luna-47B retained result, validation, protocol, and Luna-45 evidence"
    - "Luna-47F public experiments/luna47f/diagnostic.py --check"
    - "Luna-47F consumed-input and pre/post protected snapshot guards"
  label_information_boundary:
    - "No labels or task outcomes were fed into computation."
    - "No neural execution or scientific experiment was run."
  timing_assumptions:
    - "No neural timing was evaluated."
  reset_boundaries:
    - "No TPCN runtime was created or reset."
  resource_bounds:
    - "Review tests and public CLI checks only; mutation cases used isolated temporary Git clones."
  authorized_scope:
    - "Independently inspect Luna-52 implementation, contract, tests, hashes, and published state."
    - "Independently run public verification, targeted regression suites, and the complete test suite."
    - "Publish this review and update current workflow/changelog state."
  unauthorized_scope:
    - "No retained artifact edits, regeneration, normalization, or rebaseline."
    - "No scientific replay, parameter search, task efficacy, topology/growth, or hardware experiment."
    - "No new scientific Luna or successor contract because the review gate did not pass."
    - "No Luna-52 implementation/test correction in this independent-review change."
  controls:
    - "Fetched origin and verified HEAD == origin/main at execution a700024cb44e1c24df1d1284b96a9e75aeb1e261 with a clean worktree."
    - "Verified Luna-52 authorization bdd97f8fee77b1477103fc9101c622ee8611f2c7 is an ancestor and the execution contract/handoff are committed."
    - "Independently checked all seven protected artifact SHA-256 values against the contract."
    - "All public mutation cases were run in disposable local clones; the authoritative worktree and remote were not mutated."
    - "No scientific artifact or experimental interpretation was changed."
  measurements:
    - "Historical analyzer Git blob at authorization and execution revisions: 08f217daec167b2abc82f5988dba660c19f4ae0e."
    - "Reviewed Luna-51 current analyzer Git blob: 59d24b08ffa0a2a9a1ebe03a35ae595fb646fcd4."
    - "Full suite on exact published execution: 1,683 passed, 10 failed, 1 skipped."
    - "All ten failures are Luna-52 public CLI tests failing in _cli_repository because its source commit has nothing to commit on the already-published clean revision."
    - "Independent Luna-47B suite: 28 passed."
    - "Luna-44/Luna-46 regression selection: 196 passed, 1 Windows symlink-privilege skip."
    - "Luna-51/materialization/non-mutation selection: 7 passed, 1 Luna-52 public fixture setup failure."
    - "Manual isolated public CLI checks: clean and exact CRLF pass; consumed-input, historical identity, protocol, configuration, retained result, retained validation, same-path, and live mutation fail; unrelated evolution passes."
  information_boundary_check:
    - "PASS: no review output or evidence entered TPCN computation."
  hardware_mapping:
    - "Not applicable; no hardware execution or equivalence claim."
  architecture_invariants_touched:
    - "No A01-A15 clause changed."
  preserves:
    - "All seven protected scientific artifact hashes."
    - "Luna-46 MIXED."
    - "No integrated Luna-47 mechanism, task efficacy, or useful structural-growth efficacy."
    - "Luna-47G remains synthetic tolerance evidence; hardware equivalence is unestablished."
    - "Fresh historical Linux regeneration remains parked; cross-runtime binary64 equality is not claimed."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna52-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Clean authoritative `python experiments/luna47f/diagnostic.py --check`: PASS."
    - "`python -m pytest -q --tb=short tests/test_luna47b_gain.py`: 28 passed."
    - "Luna-44 canonical fixture tests plus Luna-46 depth-scaling tests: 196 passed, 1 Windows symlink-privilege skip."
    - "Luna-51/materialization/non-mutation selection: 7 passed."
    - "Independent public CLI clone cases passed their expected accept/reject outcomes, including live pre/post mutation."
  tests_failed:
    - "`python -m pytest -q -rs`: 1,683 passed, 10 failed, 1 skipped. Each failure is a public CLI adversarial test blocked before invocation because `_cli_repository` unconditionally commits a verifier copy that is identical to the committed verifier on this revision."
    - "`python -m pytest -q tests/test_luna47f_diagnostic.py -k 'luna51 or materialization or nonmutation'`: 7 passed, 1 failed; the failure is the same published-checkout fixture setup defect."
  tests_not_run:
    - "No separate reconstructed historical/core regression selection beyond the complete suite."
    - "No scientific successor experiment or next causal question, because Luna-52 did not pass."
    - "No fresh CPython 3.12.3/Linux/glibc 2.39 regeneration; this remains a governed parked limitation."
  assumptions:
    - "The repository Git object database and the literal source pins in the Luna-52 contract are trusted."
  unresolved:
    - "The public CLI adversarial test helper must support both the pre-publication dirty-source case and a clean clone where the reviewed verifier is already committed."
    - "The complete repository test suite must be green on the corrected published revision before Luna-52 can pass."
    - "Committed Luna-47B protocol/result mutation tests call the metadata helper directly; add reconstruction-route regressions even though independent direct reconstruction rejects those mutations."
  recommended_next_agent:
    - "Project owner to authorize a narrowly scoped Luna-52 test-harness correction, then return the exact published revision for fresh Luna-0 review."
---

# Luna-0 independent review — Luna-52 retained provenance

## Review disposition

**LUNA-52 CORRECTION REQUIRED.** The provenance implementation and live
public-path protection behave as intended under independent inspection and
isolated CLI checks. However, the committed Luna-47F adversarial subprocess
tests do not run from the exact published clean checkout: their setup
unconditionally commits a copy of the reviewed verifier, but that file is
already identical to `HEAD`, so Git correctly exits with “nothing to commit.”
All ten public-path cases fail in setup, and the required full-suite green gate
is not met. No scientific-successor readiness decision is made.

## Identity and publication audit

- `git fetch origin` succeeded.
- Review started with `HEAD == origin/main ==
  a700024cb44e1c24df1d1284b96a9e75aeb1e261`, clean worktree.
- The reviewed execution commit exists and is the published Luna-52 commit.
- Luna-52 authorization commit
  `bdd97f8fee77b1477103fc9101c622ee8611f2c7` is in its ancestry.
- `.github/agents/luna-52.agent.md` and the Luna-52 execution handoff are
  committed. At review start, workflow/changelog correctly described the
  execution as awaiting independent review.

## Protected artifacts

Every required artifact hash independently matched its pinned value:

| Artifact | SHA-256 |
|---|---|
| Luna-47B `results.json` | `b120d2cc5718649fb0d57d93611ddb89b45113e79c0d3003cf330fe092d0fb83` |
| Luna-47B `validation.json` | `1ef630d88e4699e9bcc1e5d05e2cc868f12f38a3958f8f1a065a4132df628fe0` |
| Luna-46 original output | `32561efb9f81996133bc930751083b2678c455668e47f0cd854e7985ad0616df` |
| Luna-46 pre-label output | `1c3843127c3de1e9b380fd06571282f0c19cf48a820730bc3ffa1dd5b11e65d4` |
| Luna-46 corrective output | `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e` |
| Luna-47F `diagnostic.json` | `f24a56bf5a92f622c4dfdb661116a83a76df1f7b0ae0056d20920360ca3cbb7c` |
| Luna-47F `validation.json` | `e3c8cb236f57908319893c2e109a2c94f5dd8d50e6953f48810da74259a62c29` |

The tests and review did not write to these artifacts.

## Luna-47B assessment — CORRECT

Git independently resolves the historical analyzer path to blob
`08f217daec167b2abc82f5988dba660c19f4ae0e` at both historical authorization
revision `789dda5988daf72f375d9713bd76a6da2b9e8b34` and recorded Luna-47B
execution revision `38891b81754ce385c55f96e4020e2bf04c2b9a5d`. The reviewed
current source at `e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e` resolves to the
distinct blob `59d24b08ffa0a2a9a1ebe03a35ae595fb646fcd4`.

The reconstruction obtains historical bytes with `git show`, verifies the
literal expected blob and the execution revision's blob, computes Git's
canonical blob identity, then compiles the historical bytes into an isolated
module. It uses that module for integrity, reconciliation, and recurrence
verification. The imported current module is not substituted for those
historical operations; it supplies only separate hash/canonical utilities.
The current analyzer is independently authenticated to its reviewed Git
revision/blob, with only exact LF-to-CRLF worktree materialization accepted.
An unauthorized current checkout mutation fails closed.

Historical protocol and retained result/validation identities are pinned;
consumed Luna-45 evidence is read from its declared evidence-baseline Git
objects and checked against current `HEAD` blobs. The 28-test Luna-47B suite
passes, including wrong pins, unavailable/mutated historical object, current
source mutation, protocol/result/validation mutation, consumed-input mutation,
and the full deterministic reconstruction test that rejects use of current
verifier functions. The test's expected historical/current identities are
literal values and independently agree with Git history. The committed
protocol/result mutation tests call `verify_historical_lane_metadata()`
directly rather than `reconstruct()`. Independent disposable-clone calls to
`reconstruct()` with mutated retained result, protocol, and current analyzer
bytes all failed closed with the expected identity/materialization errors.
Add those route-level negative cases to the durable test suite.

**Finding: CORRECT.** Property A is established for the reviewed pins.
Historical source is not conflated with current source. As required by the
contract, unreviewed current-source changes fail closed until separately
reviewed pins are updated. Add route-level negative tests as a bounded
regression improvement.

## Luna-47F public verification assessment

The clean authoritative command
`python experiments/luna47f/diagnostic.py --check` passes. The added tests
invoke that exact script with `--check` via a subprocess in temporary local
Git clones; mutations are committed in those clones to pass the dirty-change
guard and reach historical evidence checks. The live-mutation harness uses
`sitecustomize` to alter only the clone's validation file immediately after
the actual CLI reads it in `protected_snapshot`; the CLI's post-snapshot
comparison rejects it.

Independent direct CLI runs in disposable clones produced these outcomes:

| Case | Observed public result |
|---|---|
| Clean authoritative verification | Exit 0; retained analysis/replay/input/hash PASS |
| Consumed scientific input changed at the same path | Exit 1; baseline bytes mismatch |
| Historical input Git identity substituted with `git replace` | Exit 1; historical Git object identity mismatch |
| Protocol mutation | Exit 1; protected historical/materialization check |
| Configuration mutation | Exit 1; baseline input bytes mismatch |
| Retained diagnostic result mutation | Exit 1; fixed retained identity mismatch |
| Retained validation mutation | Exit 1; fixed retained identity mismatch |
| Same-path raw input substitution | Exit 1; baseline input bytes mismatch |
| Unrelated governance and test additions | Exit 0; retained verification PASS |
| Exact Git LF-to-CRLF materialization | Exit 0; retained verification PASS |
| Deterministic live mutation during `--check` | Exit 1; protected live input changed during verification |

These manual cases used temporary clones; cleanup was executed in `finally`.
The authoritative working tree, remote, and retained artifacts were not
modified. Public error paths exit nonzero and identify a meaningful protection
category.

**Committed test-harness defect:** `tests/test_luna47f_diagnostic.py`'s
`_cli_repository()` always writes `FILE.read_bytes()` over the cloned
`experiments/luna47f/diagnostic.py`, stages it, then runs `git commit` with
`check=True`. On the published revision, the clone already contains exactly
those bytes. Git reports “nothing to commit” and returns 1, before any of the
ten public subprocess adversarial cases run. This explains why those cases
could pass while the verifier was uncommitted during execution but fail from
the final published checkout. A clean published `pytest` run is the
authoritative state for acceptance.

**Finding:** The public protection behavior (Property B) was independently
demonstrated in isolated CLI runs, but the required committed public-path
regression coverage is not executable from `HEAD` and the full suite fails.
The implementation is not shown to weaken evidence protection; the required
test/regression gate is incomplete.

## Prior provenance corrections and repository gate

- Luna-44 fixture and Luna-46 provenance regressions: **196 passed, 1
  skipped**. The sole skip is the existing Windows directory-symlink privilege
  limitation (`WinError 1314`).
- Luna-51/materialization/non-mutation selection: **7 passed, 1 failed**.
  The failure is the Luna-52 CRLF public CLI test hitting the same empty-commit
  setup defect.
- Full suite on the exact reviewed SHA: **1,683 passed, 10 failed, 1 skipped**.
  All ten failures are Luna-52 public subprocess tests and share the
  `_cli_repository()` setup failure. No xfail/xpass was reported.
- Luna-47B focused suite: **28 passed**.
- No separate historical/core selection was run; those tests are included in
  the complete suite.

The required full regression gate is therefore **not green**. The prior
Luna-44 canonical-fixture authentication and exact runtime-scoped rules remain
intact; Luna-46 Git-object/checkout distinction remains intact; Luna-47F
consumed-input and live pre/post guards remain intact.

## Scientific state and disposition

No scientific readiness review or next causal uncertainty selection was
performed because the prerequisite Luna-52 pass condition failed. Preserve
the established record: Luna-46 **MIXED**; Luna-47A/B/D/F mechanisms remain
isolated evidence, not an integrated causal mechanism or task efficacy;
Luna-47G remains synthetic tolerance evidence; no useful structural-growth
efficacy or hardware equivalence is established. Fresh historical
CPython 3.12.3/Linux/glibc 2.39 regeneration remains a parked limitation,
cross-runtime binary64 equality is not claimed, and alternate-runtime
scientific sensitivity remains **UNKNOWN / NOT TESTED**.

**LUNA-52 CORRECTION REQUIRED.** The minimum next assignment is a test-only
repair of the temporary-clone bootstrap so it works both when the reviewed
verifier differs from the clone's base and when the verifier is already
committed at `HEAD`, plus reconstruction-route regressions for Luna-47B
retained result/protocol/current-source mutation. Preserve the real subprocess
entry point, all adversarial cases, and strict expected failure categories.
Then run all public cases and the full suite on the exact clean published
revision, reconfirm all seven hashes, and return for independent Luna-0 review.
Do not create a scientific successor contract or resume scientific work
before that review passes.
