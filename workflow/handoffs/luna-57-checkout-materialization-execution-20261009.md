---
tpcn_handoff:
  agent: "Luna-57"
  luna_identifier: "Luna-57"
  descriptive_name: "Luna-55 checkout-materialization provenance correction"
  task_id: "luna-57-checkout-materialization-execution-20261009"
  component: "Luna-55 retained phase and Luna-46 provenance checks"
  status: "complete"
  contract_version: "1.2"
  branch: "main"
  base_revision: "7d54aee4cc4ed904c5cb8a98a697cad4b62beb15"
  result_revision: "Implementation commit b6b4a54b82cd89f486d2b56495371f9a89b7f5f8; validation record updated in this publication"
  dependencies:
    - "Published Luna-57 authorization at 7d54aee4cc4ed904c5cb8a98a697cad4b62beb15"
    - "Luna-56 exact Git-object/materialization verifier semantics"
  owner: "Parent orchestrator; independent Luna-0 review pending"
  classification:
    - "OBSERVED: three authorized Luna-55 regression failures reproduced before edits"
    - "OBSERVED: historical phase hashes and L46 helper hash identify exact permitted materializations"
    - "INFERRED: the three failures shared a checkout-representation comparison defect"
  hypothesis: "Luna-55 can preserve pinned Git-object and semantic identities while accepting only exact LF or exact Git LF-to-CRLF checkout bytes."
  counter_hypothesis: "Any changed artifact identity, unlisted byte representation, semantic digest mismatch, or scientific output change falsifies the correction."
  interfaces_relied_on:
    - "Luna-55 AUTHORIZATION_REVISION and eight ARTIFACT_PINS"
    - "Luna-55 frozen selection checkout_sha256 values"
    - "Luna-53 _verified_file and _verify_checkout_materialization exact materialization helper"
    - "Luna-46 retained Git blob and embedded semantic digest"
  label_information_boundary:
    - "No label, neural input, or scientific result was changed or used as a new computational input."
    - "No six noncrossing target streams were inspected or reinterpreted."
  timing_assumptions:
    - "Not applicable; provenance-only tests."
  reset_boundaries:
    - "Not applicable; no scientific runtime was invoked."
  resource_bounds:
    - "Unit fixtures used small temporary files; no scientific replay or output generation."
  authorized_scope:
    - "Correct only experiments/luna55/run.py and tests/test_luna55_factorial.py."
    - "Add this single execution handoff under workflow/handoffs/."
    - "Run only authorized regression/unit checks."
  unauthorized_scope:
    - "No experiments/luna55/run.py CLI, run_phase, summarize, replay, parameter sweep, or artifact generator."
    - "No edit to data, configuration, selection membership, pinned literals, .gitattributes, other runners/tests, or Luna-55 outputs."
    - "No full repository suite, commit, push, Luna-58, or scientific successor."
  controls:
    - "Started on clean main at HEAD == origin/main == 7d54aee4cc4ed904c5cb8a98a697cad4b62beb15."
    - "Authenticated phase bytes through fixed revision 312eba8c8e036927408fb2156756a50d15762bc8 and each frozen Git blob."
    - "Used Luna-53's exact materialization verification with canonical bytes supplied; did not use broad newline normalization."
    - "Used temporary test fixtures only for byte mutations and missing-path/object checks."
    - "Verified protected artifact paths have no Git diff and published Luna-55 objects still match HEAD."
  measurements:
    - "All eight current retained phase files matched their authenticated Git bytes exactly (LF)."
    - "All eight selection checkout_sha256 literals match exactly one allowed form independently: four Luna-54 entries match exact CRLF forms; four Luna-53 entries match exact LF forms."
    - "Luna-46 current file is exact CRLF for fixed blob 9506369d97babf7bc0ef15ed52efb738dcdcd549; its measured SHA-256 and length are 0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e / 2,337,377."
    - "Luna-46 exact LF identity is SHA-256 54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51 / 2,337,376; exact CRLF matches the unchanged legacy helper identity."
    - "Adversarial temporary fixtures rejected altered character/number/space/content, same-path substitution, added/removed bytes, mixed LF/CRLF, lone CR, malformed EOF, wrong revision/blob, and missing Git object/current file."
  information_boundary_check:
    - "PASS: no scientific computation, replay, or label flow occurred."
  hardware_mapping:
    - "Not applicable; test/provenance-only."
  architecture_invariants_touched: []
  preserves:
    - "A01-A15 and ACP-0008 unchanged."
    - "Every historical hash, blob, revision, artifact, semantic digest, and selection literal unchanged."
    - "Luna-55 accepted result and published outputs unchanged."
    - "Luna-56 strict exact-object/CRLF materialization contract."
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna55/run.py"
    - "tests/test_luna55_factorial.py"
    - "workflow/handoffs/luna-57-checkout-materialization-execution-20261009.md"
  tests_added:
    - "Exact LF and CRLF current-checkout acceptance and historical-hash equality/inequality cases."
    - "Temporary-file rejection cases for content, whitespace, same-path substitution, malformed newline/EOF, and missing current file."
    - "Fixed revision/blob, unrelated historical hash/length, and simulated missing historical Git object rejection."
  tests_passing:
    - "Three required Luna-55 selectors: 3 passed."
    - "Complete tests/test_luna55_factorial.py: 22 passed."
    - "Focused Luna-46/Luna-47F/Luna-53/Luna-54 provenance modules excluding the in-tree ownership check: 277 passed, 1 skipped, 1 deselected."
    - "Luna-47F public experiments/luna47f/diagnostic.py --check in a clean disposable worktree: PASS."
    - "test_reproduction_check_is_read_only in a clean disposable worktree: 1 passed."
  tests_failed:
    - "An initial combined focused-module run invoked test_reproduction_check_is_read_only in the modified working tree and failed with ValueError: non-owned change because Luna-57's uncommitted authorized edits violate Luna-47F's ownership guard. The same test and public --check passed from clean disposable worktrees."
  tests_not_run:
    - "Clean committed-state validation: exact three targets 3 passed; Luna-55/Luna-54 integrity 32 passed; Luna-46/Luna-47F/Luna-53 provenance 268 passed, 1 capability skip; historical/core 72 passed."
    - "Full repository test suite at implementation commit b6b4a54b82cd89f486d2b56495371f9a89b7f5f8: 1,748 passed, 1 capability skip, 0 failed or errors."
    - "CUDA-specific test: not part of this focused run; authorization handoff reports its baseline test passed."
    - "Scientific runners, run_phase, summarize, replay, parameter sweep, and artifact generation: prohibited and not run."
  assumptions:
    - "The exact current Git object or its exact LF-to-CRLF transform are the only permitted checkout byte forms."
    - "Selection checkout_sha256 remains historical metadata and must match one exact allowed form, not every present checkout."
  unresolved:
    - "Full suite and clean committed-state validation remain pending with the parent orchestrator."
    - "Independent Luna-0 review is the next gate."
  recommended_next_agent:
    - "Luna-0: independent review of the bounded correction and evidence."
---

# Luna-57 execution handoff

## Outcome and owned scope

**EXECUTED / CORRECTION COMPLETE; STOPPING FOR INDEPENDENT LUNA-0 REVIEW.**
The working baseline was clean `main`, with
`HEAD == origin/main == 7d54aee4cc4ed904c5cb8a98a697cad4b62beb15`.
The published authorization handoff and Luna-57 contract were read, along
with the architecture contract, workflow, changelog, acceptance criteria,
and handoff template. No authorization or workflow documentation was edited.

Before edits, the three authorized selectors reproduced the specified
failures: both phase-based tests stopped at the current raw SHA comparison
for `artifacts/luna54/control-initial.json`; the helper test failed because it
required the valid legacy CRLF SHA to differ from the current CRLF SHA.

`experiments/luna55/run.py` now authenticates each phase's fixed revision and
Git blob, then delegates current-checkout and historical SHA/length checks to
the existing Luna-53/Luna-56 strict `_verified_file(...,
canonical_bytes=...)` path. This accepts only exact object bytes or the exact
LF-to-CRLF transform. The pinned `checkout_sha256` is explicitly checked
against the immutable selection value and remains independently validated
against the two permitted representations; it is no longer required to equal
the current checkout SHA.

The Luna-46 helper path retains its fixed object and current `HEAD` blob
check, uses the same exact verifier, and validates the unchanged legacy
SHA/length (`0d32926f...7722e`, 2,337,377 bytes) as the exact CRLF materialization.
Its embedded semantic digest and the `try/finally` restoration of temporarily
adapted Luna-54 helper state remain intact. Hash equality on a current CRLF
checkout is explicitly covered and accepted.

The only edited files are the two authorized code/test files and this
execution handoff. Historical literals, result bytes, data, configurations,
selection membership, `.gitattributes`, other tests/runners, and published
outputs were not edited.

## Architecture evidence

This is a test/provenance correction; no A01-A15 clause, ACP, runtime,
computation, topology, learning behavior, event semantics, or scientific
interpretation changed. No ACP is required. The evidence is restricted to
fixed-object identity, permitted byte materialization, semantic/artifact
integrity, and bounded test fixtures.

### Directly verified retained identities

The fixed phase revision is
`312eba8c8e036927408fb2156756a50d15762bc8`. The table records current
checkout SHA-256s measured on Windows with `core.autocrlf=true`; every current
phase file was byte-equal to its authenticated Git object (LF). Recorded
selection SHA values remain exactly the historical values.

| Retained phase path | Fixed blob | Current form / SHA-256 | Frozen selection SHA-256; independently verified form |
|---|---|---|---|
| `artifacts/luna54/control-initial.json` | `e1229a04c4388fbf84dc099295f2f38515b2be5e` | LF / `2d63eb997676b38a6f09a128a8ce353bdec4e32667d589f9a2089c62b2334751` | `b38f974c55536c118ae45c672a0afa0c59ee005af4112840ae2919cf1233b76d` — exact CRLF |
| `artifacts/luna54/control-replay.json` | `0024079a7009f8807bdb531567f0f0bf134c61d8` | LF / `9f1dacf0a41945087d76ca231c0a0abff89ecc7e488d3df2949f4c489952d53b` | `6f733031b4514a03ce8c52b985b9642233be755a6571baa9e9b00ea2b25e33eb` — exact CRLF |
| `artifacts/luna54/intervention-initial.json` | `6de22f1f5406f378e115a818e01e459ec6ddf3e6` | LF / `62b4fe16da456a37ffe7014d495ce1e74ddad174bd853e1656a40256eee7b702` | `fe629408f976138fd2c375b8be41a8c874d629ffcadc12a16696596fb841f940` — exact CRLF |
| `artifacts/luna54/intervention-replay.json` | `684fc1f3adfbd26dbbca1a656c1d14c5e8ac92a8` | LF / `d7c3d69f9a6f184517eb465393eb6ace57e9210ef27a8cd5e8a5c52e1fb57bc4` | `93a56cb7dd993e9342e0e8045cd92b43d5483def8dc2ecd5a6786708ea7e1710` — exact CRLF |
| `artifacts/luna53/luna53-control-initial.json` | `c1b73424a0be31bd95f7ac36bfe0cd3594927460` | LF / `cc9530821835c8df002ca6d9c9f8ec3df005fd1223c1e8f60ced70d65f82395c` | `cc9530821835c8df002ca6d9c9f8ec3df005fd1223c1e8f60ced70d65f82395c` — exact LF |
| `artifacts/luna53/luna53-control-replay.json` | `0aa2d1eb3cdf83ea84deabb616b6c14a7c26c8f2` | LF / `3398e98bd1230d78bd973b486e732b623f79d3db14083642cf9d31f1ab878366` | `3398e98bd1230d78bd973b486e732b623f79d3db14083642cf9d31f1ab878366` — exact LF |
| `artifacts/luna53/luna53-intervention-initial.json` | `e7901d1495ae123c75d31d98ef771aff27b9c9e0` | LF / `93a4c52b0ba079942b98040c7c8b7fa1fdc94da8685b06f8ce8f0ab0b3d4d818` | `93a4c52b0ba079942b98040c7c8b7fa1fdc94da8685b06f8ce8f0ab0b3d4d818` — exact LF |
| `artifacts/luna53/luna53-intervention-replay.json` | `557e4932023200a63f72fd178f695dbe648c2937` | LF / `b733da050b2b4223cddf02ed7d8c6c0e3859f6000f330e89b828972cee54625c` | `b733da050b2b4223cddf02ed7d8c6c0e3859f6000f330e89b828972cee54625c` — exact LF |

The canonical LF-to-CRLF SHA-256 values in the first four rows are,
respectively, the recorded selection hashes. For the last four rows, the
recorded selection hash is the canonical LF hash. No hash, blob, revision, or
selection literal was changed.

For Luna-46, the fixed blob remains
`9506369d97babf7bc0ef15ed52efb738dcdcd549`; canonical LF SHA/length are
`54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51` /
2,337,376, and exact CRLF SHA/length are
`0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e` /
2,337,377. The current bytes are exactly CRLF; current and legacy SHA values
are equal, as permitted. The existing Luna-46 semantic digest remains
`f72ba671f6d1618ab60cf81d85ac664395646de43c3ad77c226f41b9aa657628`.

Published Luna-55 selection and output Git objects were rechecked against
`HEAD`; byte hashes matched:

| Protected published file | Git blob |
|---|---|
| `artifacts/luna55-selection/post-luna54-destination-oracle.json` | `a63a5edddd6f24b2625192b398b74a84125b97bb` |
| `artifacts/luna55/rr-initial.json` | `b29e76709a6d502ee8f48aa4e4ea4f31fa9388ca` |
| `artifacts/luna55/rr-replay.json` | `61baf5aa4c42a0c518d0c0fbf91e110acd8fe987` |
| `artifacts/luna55/summary.json` | `b39ce827f546f483f0c47cb1bcb7f5724ecf59ea` |
| `artifacts/luna55/summary-v2.json` | `b5ea24311f10ff8452ccaca887c1b89bbc4589c8` |
| `artifacts/luna55/summary-v3.json` | `063b03ea84933f930ce95b2fe15e8ee83e0e4172` |
| `artifacts/luna55/summary-v2-integrity.json` | `5bdf614b683796a73ba92795859ec62ce6e32476` |
| `artifacts/luna55/summary-v3-integrity.json` | `31f90451a3c799ae2a578d5565052c5f7db1acd1` |

## Validation record

Environment: Windows host (`Windows_NT`), Python 3.11.4,
pytest 9.1.1, `core.autocrlf=true`. Tests were regression/unit tests only.

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Three required baseline selectors, before edits | `7d54aee4cc4ed904c5cb8a98a697cad4b62beb15`; Windows/Python 3.11.4 | **3 failed as authorized:** two phase SHA failures for control-initial; helper SHA inequality assertion failed on equality | Exact pytest output captured in session; no runner invoked |
| `python -m pytest -q tests/test_luna55_factorial.py` | Luna-57 implementation worktree; Windows/Python 3.11.4 | **22 passed** | Includes all new exact-materialization and adversarial tests |
| Three required selectors | Luna-57 implementation worktree | **3 passed** | The exact three contract nodes |
| `python -m pytest -q -rs tests/test_luna46_depth_scaling_diagnostic.py tests/test_luna47f_diagnostic.py tests/test_luna47f_retained.py tests/test_luna53_retention.py` | Clean implementation commit `b6b4a54b82cd89f486d2b56495371f9a89b7f5f8`; Windows/Python 3.11.4 | **268 passed, 1 skipped** | Skip is the directory-symlink `WinError 1314` capability limitation |
| `python -m pytest -q tests/test_luna55_factorial.py tests/test_luna54_relay_retention.py` | Clean implementation commit `b6b4a54b82cd89f486d2b56495371f9a89b7f5f8` | **32 passed** | Complete Luna-55 factorial and Luna-54 integrity modules |
| `python -m pytest -q tests/test_luna44_canonical_fixture.py tests/test_event_runtime.py tests/test_excursion_neuron.py` | Clean implementation commit `b6b4a54b82cd89f486d2b56495371f9a89b7f5f8` | **72 passed** | Historical/core regression set |
| Luna-47F public `--check` | Clean implementation commit `b6b4a54b82cd89f486d2b56495371f9a89b7f5f8` | **PASS** | Retained analysis, replay, inputs, code and protected hashes |
| `python experiments/luna47f/diagnostic.py --check` | Disposable detached worktree at clean `7d54aee4cc4ed904c5cb8a98a697cad4b62beb15` | **PASS: retained analysis, replay, inputs, code and protected hashes** | Worktree removed after command |
| `test_reproduction_check_is_read_only` | Same clean disposable baseline worktree | **1 passed** | Worktree removed after command |
| Exact identity comparison for eight phase inputs and protected Luna-55 publication objects | Modified worktree; post-test | **8/8 current phase bytes exact LF; all selection hashes identify allowed forms; all protected output blobs match HEAD** | Measurements in this handoff |
| Protected-path diff check | Modified worktree; post-test | **No changes** in artifacts/luna53, artifacts/luna54, artifacts/luna55, artifacts/luna55-selection, or `.gitattributes` | `git diff --exit-code HEAD -- ...` returned 0 |
| `python -m pytest -q -rs --tb=short` | Clean implementation commit `b6b4a54b82cd89f486d2b56495371f9a89b7f5f8`; Windows/Python 3.11.4 | **1,748 passed, 1 skipped, 0 failed** | Only skip: directory symlink unsupported, Windows `WinError 1314`; CUDA was not skipped |
| Protected artifact diff and clean worktree | Implementation commit | **PASS** | Protected historical artifacts and `.gitattributes` unchanged; source tree clean after tests |

The sole skip in both the focused provenance run and full suite was the
Luna-46 directory-symlink capability case: Windows `WinError 1314`, “A
required privilege is not held by the client.” No CUDA skip appeared in the
full suite. The targeted `test_luna46_depth_scaling_diagnostic` suite
otherwise passed.

## Benchmark and resource results

Not applicable. No benchmark, scientific computation, event execution,
replay, summarization, parameter sweep, or artifact generation ran.

## Assumptions, limitations and unresolved issues

Observed evidence is limited to exact Git-object authentication,
materialization SHA/length identity, embedded semantic digest, retained
artifact/selection pins, and unit/regression behavior. No claim is made about
Luna-55's scientific limitations or efficacy beyond preservation of the
accepted result. The full repository suite and committed-state gates are
pending parent orchestration.

## Reproduction and rollback

Run the focused commands in the validation table with Python 3.11.4. The
authorized source change is limited to the exact-materialization checks and
regression fixtures described above. To roll back only this execution, restore
the three listed files to the base revision; do not touch retained artifacts
or unrelated work.

## Next assignment

Stop for **independent Luna-0 review** of this handoff, the two code/test
changes, measured identities, and clean committed-state test evidence. No
Luna-58 or scientific work is authorized.
