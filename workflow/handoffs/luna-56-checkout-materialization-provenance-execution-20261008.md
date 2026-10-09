---
tpcn_handoff:
  agent: "Luna-56"
  luna_identifier: "Luna-56"
  descriptive_name: "Historical evidence identity and checkout correction"
  task_id: "luna-56-checkout-materialization-provenance-20261008"
  component: "Luna-47F/Luna-53 retained artifact checkout identity; Luna-46 catalog test"
  status: "complete - PASS; awaiting independent Luna-0 review"
  contract_version: "1.2"
  branch: "main"
  base_revision: "a2ffea9d9e265a5e28caab77cc0377ae29ea4309"
  result_revision: "ec4ff50b4c8ca85243d986c9ebb7aa67f6ba7888"
  dependencies:
    - "Luna-56 authorization and governing contract: a2ffea9d9e265a5e28caab77cc0377ae29ea4309"
    - "Luna-0 governance disposition: a2ffea9d9e265a5e28caab77cc0377ae29ea4309"
    - "Luna-55 retained evidence publication: 8369c8e70209c553be0662b6d705177308151d68"
    - "Luna-47F retained artifact publication: 39bedbce47055a7b180593ea312c6b646510c566"
    - "Luna-53 pinned-input authorization: 04305a2917195888cbbcccf378eba7971551e9b5"
  owner: "Project owner; next action is independent read-only Luna-0 review"
  classification:
    - "correction-only historical provenance and checkout-materialization regression"
    - "PASS - CHECKOUT-MATERIALIZATION PROVENANCE CLOSED"
  hypothesis: "The five baseline failures are false negatives caused by requiring one checkout representation where the pinned Git objects and evidence are intact."
  counter_hypothesis: "Any exact-LF/CRLF mismatch outside the authorized transform, changed historical object, or altered scientific artifact would invalidate the correction."
  interfaces_relied_on:
    - "Pinned Luna-46 catalog and diagnostic Git objects"
    - "Luna-47F retained-result and validation objects and existing read-only --check"
    - "Luna-53 original PINNED_FILES Git identities and provenance-only verifier"
  label_information_boundary:
    - "No labels, strata, or scientific results enter the provenance validators."
  timing_assumptions:
    - "Not applicable; no scientific execution."
  reset_boundaries:
    - "Not applicable; no scientific execution."
  resource_bounds:
    - "Bounded byte/hash/Git-object verification and regression tests only."
  authorized_scope:
    - "Correct exactly five checkout-sensitive regression failures while retaining fixed historical Git objects and SHA literals."
    - "Prove exact LF/CRLF acceptance and substantive mutation/object-substitution rejection."
    - "Run the contracted provenance, historical/core, and full test suites."
  unauthorized_scope:
    - "No Luna-44–55 experiment/replay, no Luna-55 six-stream analysis, no task efficacy, no hardware evaluation, no architecture/ACP change, and no Luna-57."
  controls:
    - "Fetched origin and verified clean HEAD == origin/main == authorization revision before editing."
    - "Reproduced all five failing test nodes before editing; exact baseline output and object forms are recorded below."
    - "Committed implementation/tests at ec4ff50b4c8ca85243d986c9ebb7aa67f6ba7888, then ran the required focused tests and full suite from a clean checkout."
    - "Compared protected evidence to the authorization tree and historical publication Git objects; accepted only exact bytes or exact LF-to-CRLF materialization."
    - "No artifact, protocol, configuration, .gitattributes, TPCN runtime, ACP, or architecture file changed."
  measurements:
    - "Luna-46 catalog: revision d1f901d3d995dc013f22dd086ae1ed8ffd28293d, blob b1aaef4006422f321922bfb58425e4fb646d96b9, canonical SHA-256 a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e, 7,121 bytes; worktree is exact LF. The exact CRLF form is 7,122 bytes with SHA-256 5c41184dc9b9b5872263bcbbc1e5fc406789101c27942480b9cfb6b33c87da80."
    - "Luna-47F result: revision 39bedbce47055a7b180593ea312c6b646510c566, blob 74c6859555caf8cb9c5a51f713080b238d716c79, canonical SHA-256 aec4e589102b0e40a31de725f97471072fdfb03fa7ee0a263d716f7de0d7e3ef, 4,431,419 bytes; worktree is exact LF. Its exact CRLF hash remains the literal f24a56bf5a92f622c4dfdb661116a83a76df1f7b0ae0056d20920360ca3cbb7c."
    - "Luna-47F validation: revision 39bedbce47055a7b180593ea312c6b646510c566, blob c70c9f1d4ae6f5712b672d54e2e71cef0629cc2a, canonical SHA-256 176069a349584347fd312e58439aee5f7128356f20d32c29b1b79ac18677f3cf, 6,773 bytes; worktree is exact CRLF with preserved SHA-256 e3c8cb236f57908319893c2e109a2c94f5dd8d50e6953f48810da74259a62c29."
    - "Luna-53 Luna-46 input: authorization revision 04305a2917195888cbbcccf378eba7971551e9b5, blob 9506369d97babf7bc0ef15ed52efb738dcdcd549, canonical SHA-256 54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51, 2,337,376 bytes; worktree is exact LF. The unchanged recorded SHA-256 0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e and size 2,337,377 describe exactly its CRLF form."
    - "Luna-47F current checkout aggregate over its two retained JSON files: 48315bfb8d2393b8f1874df40a644fc5045baa0751745987e9b21be4de73cb6a."
    - "Luna-53 current checkout aggregate over five retained JSON files: bd76677378308ad27d97db3d6168becbc2d1832879f72cb79bb0a244e9d67fb4."
    - "Luna-54 current checkout aggregate over 13 retained JSON files: f0d4277637903439c765b863dfb1d8ce2e91a2315068c9017dd96ccdaf929dd0; all are exact CRLF materializations of their publication Git objects."
    - "Luna-55 current checkout aggregate over seven retained JSON files: 8ca2f5a8923f73e144fa0b307842354d7dacac09d5f3b51e4a29a119cb633bdb; all are exact LF publication bytes."
    - "Protected-artifact aggregate procedure is SHA-256 over sorted paths and each current file SHA-256, delimited by NUL; aggregate output and per-file hashes were checked against the authorization tree. All checkout forms were exact or exact CRLF; zero invalid files."
    - "Environment: Python 3.11.5 on Windows 10.0.19045."
  information_boundary_check:
    - "PASS: no scientific computation or label-dependent execution occurred."
  hardware_mapping:
    - "Not applicable; no hardware work."
  architecture_invariants_touched:
    - "None; A01-A15, ACP-0008, runtime, neuron, routing, and topology behavior are unchanged."
  preserves:
    - "All historical Git blob IDs, source revisions, semantic digests, recorded materialization SHA/length values, and retained scientific artifacts."
    - "Luna-55 result: 10/16 predeclared target streams cross only in RR; HH/RH/HR are 0; six targets remain noncrossing; controls remain separate with zero crossings."
    - "Luna-55's 421 routes reconcile; recurrence/resource checks pass; no clipping or pending events."
    - "No scientific result, efficacy, production, hardware, or architecture-conformance claim."
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna47f/diagnostic.py"
    - "experiments/luna53/run.py"
    - "tests/test_luna46_depth_scaling_diagnostic.py"
    - "tests/test_luna47f_diagnostic.py"
    - "tests/test_luna53_retention.py"
    - "workflow/handoffs/luna-56-checkout-materialization-provenance-execution-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added:
    - "Exact LF/CRLF retained-artifact acceptance, fixed Git-object identity, wrong revision/object, missing object/file, changed-character/numeric, whitespace, same-path substitution, malformed newline, and EOF-mutation tests."
    - "Independent literal Luna-46 catalog revision/blob/SHA assertions plus exact and CRLF materialization checks."
  tests_passing:
    - "Luna-56 focused adversarial matrix: 14 passed."
    - "Five originally failing test nodes: 8 passed (the retained-result node has four LF/CRLF form combinations)."
    - "Luna-47F diagnostic and retained/public-check modules: 86 passed."
    - "Luna-46 focused module: 176 passed."
    - "Luna-53 provenance/integrity module: 7 passed."
    - "Luna-54/55 retained phase and factorial integrity modules: 16 passed."
    - "Luna-51/Luna-52 retained provenance/public-check selectors: 21 passed, 65 deselected."
    - "Historical/core checks: 72 passed."
    - "GPU module: 3 passed, 1 existing CUDA-unavailable skip."
    - "Full repository suite at clean committed candidate ec4ff50b4c8ca85243d986c9ebb7aa67f6ba7888: 1,732 passed, 1 skipped, 0 failed."
  tests_failed: []
  tests_not_run:
    - "Independent Luna-0 review of this Luna-56 publication remains pending."
    - "Scientific replay, efficacy, hardware, and six-stream follow-up were prohibited and not run."
  assumptions:
    - "The Git blob at each declared historical revision/path defines evidence identity; checkout bytes may be that exact blob or its exact LF-to-CRLF transformation only."
  unresolved:
    - "Independent read-only Luna-0 review is required before any later work."
    - "No standalone persisted Luna-55 independent-review handoff exists; its qualified PASS and reviewed revision e6a5b7c900a023c70aa2776e039a4094f02962b4 are recorded in the Luna-0 governance handoff and session checkpoint."
  recommended_next_agent:
    - "Luna-0 Architecture Guardian: independently review this exact publication read-only, verify the five repaired provenance gates and green suite, then return PASS/BLOCKED without implementing successor work."
---

# Luna-56 checkout-materialization provenance correction

## Outcome and disposition

**PASS — CHECKOUT-MATERIALIZATION PROVENANCE CLOSED.** The five baseline
failures were reproduced before edits and classified as checkout-materialization
defects. Each now authenticates the same pinned historical Git object while
accepting only exact canonical bytes or that LF Git object's exact CRLF
materialization. Changed content, wrong objects/revisions, and malformed
line-ending forms remain rejected.

The implementation/test commit `ec4ff50b4c8ca85243d986c9ebb7aa67f6ba7888`
was clean when all acceptance suites, including the full repository suite,
ran. This handoff and status-only workflow updates are published separately;
they do not modify code or tests. No experiment, scientific replay, artifact
regeneration, or architecture change occurred.

## Baseline reproduction and corrections

All five test nodes failed at baseline `a2ffea9d9e265a5e28caab77cc0377ae29ea4309`.
No failure reached scientific replay or analysis.

| Baseline test | Historical object and checkout form | Baseline comparison and exact failure | Correction |
|---|---|---|---|
| `tests/test_luna46_depth_scaling_diagnostic.py::test_luna51_catalog_identity_is_pinned_to_the_expected_git_object` | L45 catalog `artifact-integrity.json`; revision `d1f901d3d995dc013f22dd086ae1ed8ffd28293d`, blob `b1aaef4006422f321922bfb58425e4fb646d96b9`; canonical and checkout SHA `a47046da...`; exact LF. | `AssertionError: assert 'exact' == 'exact-Git-LF-to-CRLF-checkout'`. | Keep fixed revision/blob/SHA assertions, allow either governed identity class, and independently exercise the exact CRLF transform. Expected identity literals now live in the test rather than being copied from the production verifier. |
| `tests/test_luna47f_diagnostic.py::test_luna51_protocol_and_execution_code_keep_their_historical_git_identities` | Retained result `diagnostic.json`; revision `39bedbce47055a7b180593ea312c6b646510c566`, blob `74c6859555caf8cb9c5a51f713080b238d716c79`; exact LF; canonical hash `aec4e589...`, recorded CRLF hash `f24a56bf...`. | `ValueError: retained Luna47F result identity differs`, before protocol/code historical checks. | Authenticate result and validation Git blobs at fixed revision `39bedb...`; retain original SHA literals and accept only exact LF or exact LF-to-CRLF bytes before parsing. Historical protocol/code checks remain unchanged. |
| `tests/test_luna47f_diagnostic.py::test_luna51_retained_artifact_hashes_reject_result_and_validation_substitution` | Same fixed result object as above; current exact LF. Validation blob `c70c9f1d4ae6f5712b672d54e2e71cef0629cc2a`; current exact CRLF and recorded CRLF SHA `e3c8cb23...`. | `ValueError: retained Luna47F result identity differs`, before either substitution branch. | The original test node now exercises all four result/validation LF/CRLF combinations and then rejects appended bytes. Additional tests reject changed characters/numbers, whitespace, malformed newlines, same-path substitution, wrong revision/blob and missing objects/files. |
| `tests/test_luna47f_retained.py::test_reproduction_check_is_read_only` | Same pinned `diagnostic.json` result object and exact LF checkout as above. | Public `--check` exited 1 with `ValueError: retained Luna47F result identity differs`, before the non-mutation assertion. | Same fixed-object verification correction; read-only/public `--check`, live pre/post guard, consumed-input inventory, and unrelated-evolution behavior remain covered and pass. |
| `tests/test_luna53_retention.py::test_pinned_inputs_reconcile_without_running_neurons` | Luna-46 diagnostic input; revision `04305a2917195888cbbcccf378eba7971551e9b5`, blob `9506369d97babf7bc0ef15ed52efb738dcdcd549`; exact LF checkout SHA `54220205...`, 2,337,376 bytes; unchanged pin SHA `0d32926f...` is exact CRLF, 2,337,377 bytes. | `GateError: file SHA-256 mismatch for artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json`. | Retrieve bytes from the pinned Git blob, verify its original blob ID, and compare checkout bytes to exact LF or exact CRLF. Keep the original SHA literal and verify that it hashes one permitted representation; no evidence pin was updated. |

The first error is a test assertion over a helper already permitting either
representation. The three Luna-47F failures share one result-hash gate. The
Luna-53 error is a separate pinned-input check; its stored hash identifies
the exact CRLF transform of the same historical object.

## Implemented verification boundary

- Luna-47F retained artifacts are read from the caller's checkout path, but
  their expected canonical bytes are obtained with `git show` at the fixed
  publication revision. The `git rev-parse revision:path` blob must equal
  each independently pinned blob literal. Existing CRLF SHA literals are
  checked against only the canonical LF bytes or their exact LF-to-CRLF
  transform.
- Luna-53 PINNED_FILES verification retrieves each canonical blob using
  `git cat-file blob` only after verifying the original authorization
  revision/path/blob. The checkout is compared to that canonical content;
  the recorded per-file SHA/size can describe only exact LF or its exact
  CRLF materialization.
- The Luna-46 catalog test uses test-owned historical revision/blob/SHA
  literals, passes exact LF and exact CRLF through the verifier, and retains
  wrong-revision/wrong-blob and content-mutation rejection tests.
- No broad text normalization, `.strip()`, global line-ending rewrite,
  `.gitattributes` change, artifact update, or new skip was introduced.

The Luna-47F public `--check` regression suite still rejects consumed-input,
historical identity, protocol/configuration, retained evidence, same-path,
and live mutations; it accepts exact CRLF materialization and unrelated
future repository evolution. The 12-entry historical consumed-input set
remains fixed.

## Adversarial evidence

**PASS:** Both LF and exact CRLF forms of Luna-47F diagnostic/validation
artifacts pass in every combination. Exact LF and exact CRLF forms of the
Luna-53 pinned Luna-46 object pass. The catalog's exact LF and exact CRLF
forms pass.

**REJECTED:** One printable-character change, one numeric change, added or
removed ordinary whitespace, same-path validation-as-result substitution,
mixed line endings, a lone CR, a missing final newline, an appended byte,
wrong historical revision, wrong Git blob, missing object, and missing
checkout file. Tests use isolated temporary checkouts and independently
fixed expected object/hash literals.

## Protected scientific evidence

Every current artifact was compared to the Luna-56 authorization tree and
its declared historical/publication Git object. Checkout materialization
was exact for all files except Luna-47F validation and Luna-54, which match
only their exact Git LF-to-CRLF transforms. No protected artifact was
modified.

Aggregate checkout hashes below are SHA-256 over sorted relative paths and
the SHA-256 of each file, delimited by NUL bytes. The Luna-47F/53/54/55
aggregates were captured both before edits and after the full suite and are
identical. The affected Luna-46 file's pre- and post-edit canonical checkout
SHA-256 is `54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51`;
all three Luna-46 files still match the authorization tree:

| Protected set | Files | Final checkout aggregate SHA-256 |
|---|---:|---|
| Luna-46 retained files | 3 | `0a1e1dbb9dfe6e8543b0a549890b529ecc0bc80a2254baaaff3afc4f2e7eff4c` |
| Luna-47F retained result and validation | 2 | `48315bfb8d2393b8f1874df40a644fc5045baa0751745987e9b21be4de73cb6a` |
| Luna-53 phase records and summary | 5 | `bd76677378308ad27d97db3d6168becbc2d1832879f72cb79bb0a244e9d67fb4` |
| Luna-54 retained JSON | 13 | `f0d4277637903439c765b863dfb1d8ce2e91a2315068c9017dd96ccdaf929dd0` |
| Luna-55 factorial JSON | 7 | `8ca2f5a8923f73e144fa0b307842354d7dacac09d5f3b51e4a29a119cb633bdb` |

The Luna-55 `summary-v3.json` and integrity catalog remain unchanged at
publication `8369c8e70209c553be0662b6d705177308151d68`; all 421 RR routes,
recurrence/resource evidence, and separate 10/16 primary target result
remain intact. Luna-55 remains **PARTIALLY SUPPORTED** in the frozen setup:
HH/RH/HR = 0, RR = 10, six target streams do not cross, and frozen negative
controls have zero crossings. No inference about the six noncrossers is
made here.

## Validation record

All checks ran with Python 3.11.5 on Windows 10.0.19045.

| Command/procedure | Observed result |
|---|---|
| Baseline exact five test nodes at `a2ffea9d9e265a5e28caab77cc0377ae29ea4309` | 5 failed, with messages recorded above; no analysis/replay reached. |
| Focused Luna-56 exact LF/CRLF and adversarial matrix | 14 passed. |
| Exact five previously failing test nodes after correction | 8 passed; the retained result test has four materialization combinations. |
| `pytest -q tests/test_luna47f_diagnostic.py tests/test_luna47f_retained.py` | 86 passed. |
| `pytest -q tests/test_luna46_depth_scaling_diagnostic.py` | 176 passed. |
| `pytest -q tests/test_luna53_retention.py` | 7 passed. |
| `pytest -q tests/test_luna55_factorial.py tests/test_luna54_relay_retention.py` | 16 passed. |
| Luna-51/Luna-52 retained provenance/public `--check` selectors | 21 passed, 65 deselected. |
| `pytest -q tests/test_luna44_canonical_fixture.py tests/test_event_runtime.py tests/test_excursion_neuron.py` | 72 passed. |
| `pytest -q -rs tests/test_gpu_visualization.py` | 3 passed, 1 skipped: `test_cuda_records_have_cpu_semantics`, reason `CUDA is unavailable`. |
| `pytest -q -rs --tb=short`, clean implementation commit `ec4ff50b4c8ca85243d986c9ebb7aa67f6ba7888` | 1,732 passed, 1 skipped, 0 failed (624.53 seconds). |
| `git diff --check`; protected artifact object/materialization audit | Pass; zero artifact changes. |

The full-suite skip remains the existing CUDA-unavailable GPU test. No
symlink-related skip or other new skip was observed.

## Architecture, publication, and next action

No A01-A15 clause, ACP, architecture contract, production behavior, or
scientific artifact changed. Luna-53/54 narrow causal results and the
Luna-55 10/16 bounded interaction result are preserved; task efficacy,
hardware equivalence, and architecture conformance are not claimed.

The Luna-55 independent review returned a qualified PASS on
`e6a5b7c900a023c70aa2776e039a4094f02962b4`. A standalone persisted
Luna-55 review handoff was not present; this disposition is documented in
the Luna-0 governance handoff and prior session checkpoint.

**Next and only action:** independent, read-only Luna-0 review of the final
Luna-56 publication. Do not authorize Luna-57 or any scientific successor.
