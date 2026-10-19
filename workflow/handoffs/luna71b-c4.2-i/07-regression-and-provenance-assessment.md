# Luna-71B-C4.2-I — Regression and untracked-file provenance assessment

**Status:** Static documentary assessment only. No tests or neural code were executed in this I round.  
**Disposition:** Regression compatibility **INCOMPLETE BY DESIGN**; key untracked candidate sources are identity-bound, with remaining copy-provenance limits documented.

## Two blocked C4.2 focused tests

H-E reports the H focused-suite result as 34 tests: 32 passed, two blocked,
one previously failing identity-mismatch test now passing. The two blocked
legacy tests are:

| Test | Frozen assertion/purpose | Why the H candidate blocks it | Disposition |
|---|---|---|---|
| `test_driver_fails_closed_before_calling_execution_adapter` | Uses a missing fixture-payload manifest to require a `PreflightError` before adapter invocation and before importing `tpcn` | H's corrected implementation-identity preflight gate rejects the uncommitted H capture identity before the test reaches its expected missing-fixture failure. The test remains unchanged. | **BLOCKED / NOT PASS**; historical expected gate order is not attained on the H candidate. |
| `test_driver_rejects_mismatched_source_identity` | Mutates one source-file hash and expects `PreflightError("source identity mismatch")` | H's PPC-11 implementation identity check precedes the deliberately mismatched source-file assertion; it therefore fails at the earlier version gate. | **BLOCKED / NOT PASS**; test remains unchanged. |

The separate `test_driver_rejects_mismatched_implementation_identity` is
reported PASS in H-E and is not one of the two blocked tests. A prior
read-only audit result described an additional “two identity blockers” but
misidentified this passing test; this assessment follows the named tests and
dispositions in H-E and the actual legacy test source. The older suite's
fail-closed fixture assertion must not be confused with the historical
`0ad1…` test-index digest.

The expected identities are version-qualified:

* C4.2 baseline source manifest: LF blob SHA-256 `d3edfd73c4ac9f183f145d49fac4d01e8ca5aaf552f681ddd2bdd253dbccf5a7`;
  current CRLF checkout SHA-256
  `84070d2a414dc037611e842e71faf4fab66736e8a38a1f59465c2584a69ae383`;
  Git blob SHA-1 `85f1f2c79f69ee675fa8ab600be74bbf2469a3cc`.
* Published C4.2 test file `tests/test_luna71b_c4_2.py`: LF blob SHA-256
  `a02fd154e7d7d25866418f8d3990586c0a8151a493016e90814451ddd6a8535b`;
  CRLF checkout SHA-256
  `d7c4c90bf4ed7cc1871b835b5f620132cfcb14f6fba6ca83d485f57d49251c83`;
  Git blob SHA-1 `4758d9a45f7aaecf487c57e489717dd8750e2df1`.
* H candidate source manifest (`gn/source-manifest.json`): raw H checkout SHA-256
  `1c12a5f149d022f9e7a4304aa2b32f0110fc802f855d018bee32014580ae5095`.
* H synthetic test is `tests/test_luna71b_c4_2_gn.py`, 35,464 bytes, raw
  SHA-256 `f6fdf063c2223eedc26a56d7a9009647031b7ddf856ebcdca4f07c501eb24f71`;
  it is distinct from the published C4.2 test above.
* H branch/HEAD/tree are
  `governance/luna71b-c4-2-h-corrections`,
  `e91818a5c974282e848dc43e52d3c0a534dcbf45`,
  `f14f23f0eb00e8b4aa8946e34acc71ab46ab5749`; the dirty working tree and
  source manifests are also required because HEAD does not identify H edits.
* H corrected identity manifest: SHA-256
  `8524de661d68715f8e257d058649b5ea8d158f8f3c55f3cbc6be803bd515d878`;
  preserved pre-correction identity manifest:
  `6b9d34c9e079d7f26f2cc480a2014d0405e4393e7938c40e5afd09cc64041179`.

The `43fb…` source-manifest and `0ad1…` historical test-index expected
identities remain unresolved and are not replaced with any of these current
identities.

## Design-only version-qualified regression strategy

Preserve the original C4.2 tests and exact historical expectations unchanged.
Add (only after separate implementation authorization) a second fixture-backed
test family keyed by
`(contract/schema version, source-manifest identity, commit/tree, Git blob
identity, raw checkout hash, line-ending mode)`. Use synthetic source/fixture
manifests and test doubles, never the neural runner:

1. H-qualified fail-closed test: exact valid H implementation identities,
   then a deliberately missing fixture; assert no adapter call and no `tpcn`
   import, and assert the intended missing-fixture gate.
2. H-qualified source-mismatch test: valid H implementation identities and
   fixture scaffolding, then mutate one source-file digest; assert the
   source-identity rejection.
3. H-qualified implementation-mismatch test: valid source identity then
   mutate the corrected PPC-11 implementation digest; assert the identity
   rejection.
4. Historical tests remain bound to the original C4.2 source/test identities.
   If their historical fixture or source/index preimage is unavailable, keep
   their outcome BLOCKED/NOT APPLICABLE with explicit evidence; do not count
   it as pass and do not rewrite expected hashes.
5. Do not combine fixtures, permit cross-version hash substitutions, or treat
   raw SHA-256 as a Git blob SHA-1. A fixture-missing test and source-mismatch
   test must have separate, deliberate gate arrangements.

No test was run for this design assessment.

## Untracked files, identities, and classification

The H independent review found extra variant/input copies and run/test
helpers. Exact H source rows and current byte hashes are captured in the
machine-readable I artifact manifest; H's existing
`gn/source-manifest.json` contains all 80 bilateral variant rows, with each
path's baseline SHA-256, candidate SHA-256, and `modified_from_checkpoint`
flag. H `gn/gn-artifact-manifest.json` records byte sizes and SHA-256 values
for its GN package. The I artifact inventory is
[`10-artifact-manifest.json`](./10-artifact-manifest.json), with detached
checksum [`10-artifact-manifest.sha256`](./10-artifact-manifest.sha256);
the exact manifest digest is returned in the final handoff. That inventory
carries per-file identities and classifications rather than attributing
untracked content to the C4.2 Git tree.

| File group | Identity/provenance evidence | Classification and limit |
|---|---|---|
| 39 original + 41 instrumented variant source files | Per-file H source-manifest baseline/candidate hashes and GN artifact byte hashes. Six hook-modified source files are flagged: `eligibility.py`, `luna70_readout_learning.py`, `predictive_coding.py` on both sides. | Unmodified checkpoint copies: **VERIFIED SOURCE DEPENDENCY** as exact-byte copies of the stated checkpoint inventory. Six hook-modified copies: **REVIEWED IMPLEMENTATION ARTIFACT** at their recorded hashes, not Git-committed source. Their untracked status remains explicit. |
| `variants/instrumented/luna71b_trace.py` and copied original/instrumented run/test helpers | Exact per-file manifest hashes; runner/test content can be matched to local prior Luna-71B evidence where that exact content is available. | Trace helper: **AUXILIARY TOOL / REVIEWED IMPLEMENTATION ARTIFACT**. Run/test copies: **AUXILIARY TOOL**; exact bytes are bound, but untracked copies do not become committed artifacts. |
| `inputs/L71B-C-paired-pilot-plan.json` | 133,178 bytes; SHA-256 `60cde6b4929be4408fcecdcf3ac7104d5cb7b3365d94d55b568431e54fb5bc3f`; byte-identical to the untracked plan in `TPCN-luna71b` at branch `experiment/luna71b-instrumented-learning`, HEAD `f117ce51e7a805564e37252d3b5c99bda163ce57`, and to the recovered C4.1 inventory. | **HISTORICAL EVIDENCE COPY — CONTENT RECOVERED.** Neither copy is Git-committed; the copy-time chain/use by H is not established. It is not the new C4.2-N fixture and cannot be substituted for it. |
| `gn/inputs/*`, fixture/config/artifact manifests | Exact bytes are hash-bound by H GN artifact and fixture manifests; new identity is separate from R6. | **GENERATED FIXTURE / CONFIG**, as classified by the H manifests. The I review did not regenerate or execute them. |
| `gn/*.py` manifest, preflight, source identity, capture, driver, comparator | H artifact identities and corrected PPC-11 identity manifest; this I review read them statically only. | **AUXILIARY TOOL** or **REVIEWED IMPLEMENTATION ARTIFACT** per I artifact inventory; no source execution. |
| H GN review reports | Exact H artifact-manifest identities; earlier report/addendum remain historical pre-H records. | **HISTORICAL EVIDENCE / REVIEW RECORD**; no rewriting. |
| `tests/test_luna71b_c4_2_gn.py` | 35,464 bytes, SHA-256 `f6fdf063c2223eedc26a56d7a9009647031b7ddf856ebcdca4f07c501eb24f71`, H artifact-manifest entry. | **REVIEWED SYNTHETIC TEST ARTIFACT**; no tests rerun in I. |

The source inventory and artifact manifest distinguish raw checkout hashes,
Git path/blob identity, and baseline references. An untracked file is not
identified by HEAD. No file was deleted, cleaned, rewritten, or adopted into
the C4.2 commit. The historical plan copy's matching bytes correct the earlier
unknown-content concern, but do not establish its use or the provenance of
other helpers.

## Conclusion

Regression compatibility remains **INCOMPLETE BY DESIGN**: the two H-blocked
legacy tests stay blocked and unchanged pending recovered historical
identities/fixtures or an approved version-qualified correction. Untracked
identities are bound; source-copy provenance is verified where manifest
baseline equality permits, the plan's exact content is recovered, and
committed provenance/copy-time history remains explicitly limited. No suites
were executed in this I round.
