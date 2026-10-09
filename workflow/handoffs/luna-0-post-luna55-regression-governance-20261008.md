---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Post-Luna-55 regression provenance governance"
  task_id: "luna-0-post-luna55-regression-governance-20261008"
  component: "Read-only classification of historical provenance/materialization failures"
  status: "complete - evidence valid; Luna-56 correction-only follow-up authorized / not executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "53c68b0f8e9fb89c0a405baa332891755066c001"
  result_revision: "commit containing this handoff"
  dependencies:
    - "Luna-55 authorization 312eba8c8e036927408fb2156756a50d15762bc8"
    - "Luna-55 execution/result publication 8369c8e70209c553be0662b6d705177308151d68"
    - "Luna-55 independent review of e6a5b7c900a023c70aa2776e039a4094f02962b4"
    - "Luna-55 metadata correction 53c68b0f8e9fb89c0a405baa332891755066c001"
    - "Luna-53/54/47F retained result publications and Luna-46 pinned object"
  owner: "Project owner; next execution by Luna-56, then independent Luna-0 review"
  classification:
    - "read-only post-Luna-55 regression governance"
    - "SCIENTIFIC RESULT VALID — REPOSITORY GATE FOLLOW-UP REQUIRED"
    - "CORRECTIVE REGRESSION FOLLOW-UP AUTHORIZED"
  hypothesis: "All five red tests reject permitted exact LF Git-object checkouts or their correct representation metadata rather than detecting changed historical evidence."
  counter_hypothesis: "Any failing comparison reveals an unrecoverable or substantively changed historical object, changed scientific artifact, or unsupported checkout transform."
  interfaces_relied_on:
    - "Luna-46 canonical Git object and semantic result"
    - "Luna-47F fixed 12-path consumed-input set, retained result, protocol/code provenance, and read-only pre/post guard"
    - "Luna-53 original fixed Git-object and materialization pins"
    - "Luna-54 and Luna-55 immutable retained artifacts and integrity manifests"
  label_information_boundary:
    - "No experiment or neural runtime was invoked; governance reads and targeted provenance tests are evaluation-only."
  timing_assumptions:
    - "Not applicable; no scientific execution."
  reset_boundaries:
    - "Not applicable; no scientific execution."
  resource_bounds:
    - "Read-only Git/blob/hash verification and exact failing-test reproduction only."
  authorized_scope:
    - "Classify the five failures and their shared canonical-object versus checkout-materialization cause."
    - "Authorize exactly one correction-only Luna-56 follow-up; execute no correction or scientific experiment in this assignment."
  unauthorized_scope:
    - "No Luna-55 rerun, six-target analysis, Luna-57, task/production/hardware experiment, or architecture/ACP change."
  controls:
    - "Fetched origin; HEAD equals origin/main at 53c68b0f8e9fb89c0a405baa332891755066c001; clean worktree."
    - "Resolved and verified Luna-55 execution reviewed revision e6a5b7c900a023c70aa2776e039a4094f02962b4 and post-review documentation revision 53c68b0f8e9fb89c0a405baa332891755066c001 in ancestry."
    - "Individually reproduced each of the five failing test nodes. No experiment or production entrypoint was run."
    - "Verified current artifacts against their historical publication Git objects and checked internal digests/materializations."
  measurements:
    - "Luna-55 accepted verdict PARTIALLY SUPPORTED: HH/RH/HR each cross 0/16 primary targets; RR crosses 10/16; the other six do not cross."
    - "The frozen negative groups E+ 49, E0 10, NR1 189 and NR0 23 remain separately reported and each has 0 crossings in every arm."
    - "The secondary temporal-retention group remains separate: 33 streams, crossings HH 0, RH 1, HR 19, RR 33."
    - "RR routing is 421 enqueued, 421 received, 421 matched, zero mismatches; replay, recurrence and bounds passed with no clipping or pending events."
    - "Luna-53: all five pinned Git blobs match the original authorization revision; all five stored SHA values match either the canonical Git object or its exact CRLF transformation. Four execution artifacts and the summary are unchanged at their publication objects; the summary's embedded digest passes."
    - "Luna-54: all 13 result JSON files match exact CRLF materialization of publication objects at b3253bb2f2181450330ac588aaf4790781de0ef4; all 13 embedded artifact digests pass."
    - "Luna-55: all seven JSON files match exact LF publication bytes at 8369c8e70209c553be0662b6d705177308151d68; all seven embedded artifact digests pass."
    - "Luna-46 L46 object: pinned Git blob 9506369d97babf7bc0ef15ed52efb738dcdcd549 remains available; canonical checkout SHA-256 54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51; expected Luna-53 SHA-256 0d32926f... is exactly the CRLF-transformed hash; semantic digest f72ba671f6d1618ab60cf81d85ac664395646de43c3ad77c226f41b9aa657628 passes; 320 sequences."
    - "Luna-46 failing L45 catalog has unchanged pinned Git blob b1aaef4006422f321922bfb58425e4fb646d96b9 and canonical SHA-256 a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e; this Windows checkout is exact, while the test demands CRLF."
    - "Luna-47F result and validation at publication revision 39bedbce47055a7b180593ea312c6b646510c566 remain blobs 74c6859555caf8cb9c5a51f713080b238d716c79 and c70c9f1d4ae6f5712b672d54e2e71cef0629cc2a. Result is exact LF; validation is exact CRLF. Recorded f24a56bf... and e3c8cb23... are precisely their respective CRLF materialization hashes. The earlier 8cddf9d... result blob remains recoverable."
    - "Luna-47F analysis digest passes; all 12 inputs verify at historical baseline 2cef8ea4b37a4ae586e3f383511cba63c9268ddc; the declared protocol and code source revisions verify. Its latest source inventory is not a whole-repository equality requirement."
    - "Five-test baseline suite result: 5 failed individually as reported. Three Luna-47F tests all stop at the same `verify_retained_files` materialization check; the substitution test does not reach its mutations."
    - "The recorded full suite is 1,715 passed, 5 failed, 1 skipped. The single skip is `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics` because CUDA is unavailable. The Luna-46 directory symlink/junction alias tests both ran without a skip on this machine."
  information_boundary_check:
    - "PASS: this task performs no neural execution or information flow; all tests read-only."
  hardware_mapping:
    - "Not applicable; no hardware work."
  architecture_invariants_touched:
    - "No architecture clauses or ACP changed. This is a provenance/test correction, with no scientific computation."
  preserves:
    - "Accepted Luna-55 conclusion only: within the frozen retained-input setup, selective serial interaction is observed on 10 of 16 predeclared streams."
    - "Every target/control group, negative result and secondary group remains separately reported."
    - "All historical source/evidence objects and prior Luna-47F result versions remain recoverable."
    - "No efficacy, production, hardware or architecture-conformance claim."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-56.agent.md"
    - "workflow/handoffs/luna-0-post-luna55-regression-governance-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Read-only artifact identity review: L53 five pins, L54 13 embedded digests, L55 seven embedded digests, L47F exact/CRLF identities and input inventory, L46 Git blob/semantic digest."
    - "Luna-47F analysis digest and declared historical protocol/code source identities."
    - "Luna-46 targeted suite: the other 175 tests passed; both Windows alias cases executed without skip."
    - "GPU visualization module: 3 passed, 1 existing CUDA-unavailable skip."
  tests_failed:
    - "Five authorized baseline test nodes individually reproduce their materialization/provenance failure; see the findings table in the narrative."
    - "Luna-46 targeted module has one expected, individually reproduced failure: the catalog test's CRLF-only materialization assertion."
  tests_not_run:
    - "No corrective implementation, corrected targeted suite, or post-correction full-suite run; these belong to Luna-56."
    - "No scientific experiment, replay, or analysis of the six remaining Luna-55 target streams."
  assumptions:
    - "The explicit historical Git objects and reviewed phase artifacts are the source of truth; checkout SHA and size describe a separate exact materialization."
  unresolved:
    - "Repository regression gate remains red until Luna-56 passes all acceptance criteria and Luna-0 independently reviews its publication."
    - "The six non-crossing Luna-55 targets remain a future scientific uncertainty, not authorized current work."
  recommended_next_agent:
    - "Luna-56: implement only the correction contract, run its targeted adversarial checks and full suite, publish, and stop for independent Luna-0 review."
---

# Post-Luna-55 regression provenance decision

## Outcome

**OBSERVED:** The authoritative starting revision is
`53c68b0f8e9fb89c0a405baa332891755066c001`, equal to fetched `origin/main`;
the worktree was clean. Luna-55 execution and result publication are
`ca378b216e962de2a81b0d3ada741867fa4b1fce` and
`8369c8e70209c553be0662b6d705177308151d68`. Luna-0 independently reviewed
revision `e6a5b7c900a023c70aa2776e039a4094f02962b4`. The later
documentation-only contract-version correction is
`53c68b0f8e9fb89c0a405baa332891755066c001`.

**OBSERVED:** All five failing tests compare checkout representation to a
single LF/CRLF hash or label, while their canonical historical Git objects
and associated semantic evidence remain available and match. No failure
reveals a changed scientific object, lost input, invalid semantic digest, or
substantive mutation.

The disposition is **SCIENTIFIC RESULT VALID — REPOSITORY GATE FOLLOW-UP
REQUIRED**. The current tests are genuine red tests, but the evidence shows
they are false negatives caused by requiring one allowed checkout form. Do
not call the full suite green: it remains 1,715 passed, 5 failed and 1
skipped until a separately executed correction passes.

## Individual failure classification

| Failing test | Historical invariant | Current governed invariant | Why it fails now | Classification | Required Luna-56 action |
|---|---|---|---|---|---|
| `tests/test_luna46_depth_scaling_diagnostic.py::test_luna51_catalog_identity_is_pinned_to_the_expected_git_object` | The L45 artifact catalog at `artifacts/luna45-acp0008-depth2-destination-integration-20261006/artifact-integrity.json` is pinned by Git revision `d1f901d3d995dc013f22dd086ae1ed8ffd28293d`, blob `b1aaef4006422f321922bfb58425e4fb646d96b9`, and canonical SHA-256 `a47046da...`. | Canonical Git bytes and checkout bytes are distinct identities; exact Git bytes and exact LF-to-CRLF are both valid. | The catalog's current Windows checkout is byte-exact with its Git object, but the test unconditionally requires a CRLF classification. Its helper already accepts either identity. | `CHECKOUT-MATERIALIZATION DEFECT` | Keep Git blob/SHA checks. Test both allowed forms, do not assert a single host's form, and retain tests rejecting wrong object/content. |
| `tests/test_luna47f_diagnostic.py::test_luna51_protocol_and_execution_code_keep_their_historical_git_identities` | Result/protocol/code are authenticated at their explicitly declared historical revisions; the consumed input set is fixed at 12 paths. | A historical Git object remains the identity anchor; working-tree text may be exactly LF or exact CRLF. | The test fails first because its expected result SHA is the CRLF transform while current worktree bytes are exact LF; protocol/code identity assertions are not reached. | `CHECKOUT-MATERIALIZATION DEFECT` | Authenticate result and validation Git objects at the declared result publication; allow only exact bytes or exact CRLF. Then preserve the protocol/code historical Git checks. |
| `tests/test_luna47f_diagnostic.py::test_luna51_retained_artifact_hashes_reject_result_and_validation_substitution` | Both retained artifacts must reject substitution. | Same pinned Git object plus exact permitted materialization; substantive substitution must remain rejected. | The precondition fails on the result's permitted exact LF representation before the test attempts tampering. | `CHECKOUT-MATERIALIZATION DEFECT` | Keep both mutation tests; first accept either permitted representation for each artifact, then show appended/content changes fail. |
| `tests/test_luna47f_retained.py::test_reproduction_check_is_read_only` | The check command must validate retained evidence and leave it unchanged. | Read-only verification uses fixed historical Git objects, not one required checkout form. | The CLI exits at the same result SHA comparison before the non-mutation postcondition. | `CHECKOUT-MATERIALIZATION DEFECT` | Let the check reach its historical identity and before/after protection gates; prove bytes remain unchanged. |
| `tests/test_luna53_retention.py::test_pinned_inputs_reconcile_without_running_neurons` | Luna-53 pins five input Git objects at authorization `04305a2917195888cbbcccf378eba7971551e9b5`, together with SHA/size evidence. | Keep each Git blob and historical SHA literal; accept only exact LF bytes or its exact LF-to-CRLF transform. | For L46, expected SHA `0d32926f...` is exactly the CRLF transform (2,337,377 bytes) of the same still-pinned blob; the current exact Git checkout is 2,337,376 bytes and SHA `54220205...`. | `CHECKOUT-MATERIALIZATION DEFECT` | Verify canonical Git bytes at Luna-53 authorization, retain the legacy CRLF hash/length, validate exact LF/CRLF forms, and reject any other bytes. Do not replace a historical pin with `HEAD`. |

The Luna-47F triad is one verification gate, not three distinct source or
evidence defects. No failing test is a `GENUINE EVIDENCE REGRESSION`, a
`VALID HISTORICAL ASSERTION`, or a whole-repository snapshot defect. The
L47F live pre/post guard already protects its fixed paths during a run; its
historical input inventory contains exactly the 12 declared dependencies
and does not require current repository equality.

## Scientific artifact preservation audit

The canonical Git object is authoritative. Worktree files were compared
only to the exact object or its exact allowed CRLF transformation:

| Evidence | Historical publication/reference | Verified result |
|---|---|---|
| Luna-53 | Artifacts published at `1bee6673ac68e99303d33053e197f41fe78b913f`; source pins at authorization `04305a2917195888cbbcccf378eba7971551e9b5` | Five result JSONs at publication match exact canonical bytes; one embedded self-digest passes. All five input Git blobs match, and each existing SHA is the hash of either exact LF or exact CRLF. No Luna-53 artifact changed. |
| Luna-54 | Result publication `b3253bb2f2181450330ac588aaf4790781de0ef4`; independent review recorded in `workflow/handoffs/luna-0-independent-review-luna54-20261008.md` | All 13 retained JSON artifacts match exact CRLF materialization of their historical Git objects; all 13 embedded digests pass. |
| Luna-55 | Evidence publication `8369c8e70209c553be0662b6d705177308151d68` | All seven JSON artifacts match their exact LF Git bytes; all seven embedded digests pass. RR, replay, routes, recurrence, bounds, clipping, and label-isolation evidence remain intact. |
| Luna-46 | L46 file blob `9506369d97babf7bc0ef15ed52efb738dcdcd549`, authenticated at the Luna-53 baseline | Blob is still recoverable and exact in the current checkout. SHA-256 `54220205...`; semantic digest `f72ba671...`; 320 sequences. The Luna-53 SHA `0d32926f...` is proven to be this exact object's CRLF transform. The L45 catalog blob/hash also remain exact. |
| Luna-47F | Current result publication `39bedbce47055a7b180593ea312c6b646510c566` | The result and validation Git blobs are unchanged. Result checkout is exact LF; validation is exact CRLF. The expected hashes `f24a56bf...` and `e3c8cb23...` equal those objects' exact CRLF transforms. The earlier result object at `8cddf9d5d3fc0ea6971dc54645e8033c290dc852` remains recoverable. The current analysis self-digest passes, all 12 consumed historical inputs verify at `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`, and historical protocol/code sources verify. |

Luna-55 specifically consumes the unchanged pinned Luna-46 bytes whose
Git-object identity, exact checkout bytes, and semantic digest were checked
by both the published Luna-55 loader and this review. The failed Luna-53
helper comparison is a checkout-representation mismatch, not evidence that
Luna-55 consumed different input. Therefore the correct closure class is
**SCIENTIFIC RESULT VALID — REPOSITORY GATE FOLLOW-UP REQUIRED**, not
conditionally valid or evidence at risk.

## Regression and skip record

The exact five test nodes were individually rerun at the clean baseline and
each fails at the reported materialization comparison. The L47F substitution
test does not reach its mutation branches until that precondition is
corrected. Luna-46's focused module reports 175 passed and the one expected
catalog assertion failure; its directory symlink/junction alias tests both
execute without skips on this host.

The sole full-suite skip is
`tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`,
reason `CUDA is unavailable` (confirmed directly: 3 passed, 1 skipped). It
is not a symlink limitation. No new skip is proposed.

The known full-suite result remains **1,715 passed, 5 failed, 1 skipped**.
This governance review does not claim to have rerun the full suite.

## Luna-55 closure and authorized next step

**OBSERVED:** Luna-55 remains **PARTIALLY SUPPORTED** within its frozen
bounded setup: HH/RH/HR each cross 0/16 primary targets; RR crosses 10/16;
the other six do not cross. Each negative-control population remains
separate and has zero crossings; the 33-stream secondary population is
reported independently (HH 0, RH 1, HR 19, RR 33). All 421 RR routes
reconcile, replay is exact, recurrence/resource checks pass, and there is no
clipping or pending event. This is not task efficacy, production suitability,
hardware equivalence, optimal parameter selection, or architecture
conformance.

**AUTHORIZED:** Luna-56 may correct only the five read-only provenance and
test gates under
[the Luna-56 correction contract](../../.github/agents/luna-56.agent.md).
Its scope must preserve historical pins, reject substantive changes, run
adversarial exact-LF/CRLF tests, and deliver a green full suite with only the
pre-existing CUDA-unavailable skip. Luna-56 is **not executed by this
governance decision**. It must stop for independent Luna-0 review.

No Luna-57 or scientific successor is authorized. The six non-crossing
Luna-55 targets remain a future scientific uncertainty only; do not analyze
them until the regression correction has passed Luna-0 review.
