---
name: Luna-56 Historical Evidence Identity and Checkout Correction
description: Correct five historical provenance regressions by separating canonical Git-object identity from exact LF/CRLF checkout materialization.
---

# Luna-56 — Historical Evidence Identity and Checkout Correction

## Authorization

**AUTHORIZED / NOT EXECUTED.** This is a correction-only regression task
authorized by the Luna-0 post-Luna-55 governance handoff at baseline
`53c68b0f8e9fb89c0a405baa332891755066c001`. It does not authorize a
scientific experiment, replay, evidence regeneration, task evaluation,
production change, or successor scientific Luna.

The objective is to correct exactly the five currently failing historical
provenance/materialization tests listed below. Keep their historical Git
identities, scientific artifacts, semantic digests, and mutation rejection
strict. Review `.github/agents/luna-55.agent.md`, this authorization handoff,
the Luna-46/47F/53 source and retained evidence, and the repository's
architecture/workflow governance before editing.

## Baseline and classification

The reproduced baseline is `53c68b0f8e9fb89c0a405baa332891755066c001`.
The five failures are **checkout-materialization defects**, not evidence
mutations:

| Test | Failing invariant as written | Observed reason |
|---|---|---|
| `tests/test_luna46_depth_scaling_diagnostic.py::test_luna51_catalog_identity_is_pinned_to_the_expected_git_object` | Requires the checkout label to be `exact-Git-LF-to-CRLF-checkout` | The verified pinned catalog is materialized `exact`; the verifier already permits either exact bytes or its exact CRLF transform. |
| `tests/test_luna47f_diagnostic.py::test_luna51_protocol_and_execution_code_keep_their_historical_git_identities` | Calls `verify_retained_files` before source-revision assertions | The retained-result literal is the exact CRLF SHA of the final authenticated result object at `39bedbce47055a7b180593ea312c6b646510c566`; current bytes are the exact LF Git object. The test never reaches the historical source assertions. |
| `tests/test_luna47f_diagnostic.py::test_luna51_retained_artifact_hashes_reject_result_and_validation_substitution` | Verifies the retained files before exercising tampering checks | It stops at the same result LF/CRLF mismatch; keep the adversarial substitution checks and make both valid materializations pass. |
| `tests/test_luna47f_retained.py::test_reproduction_check_is_read_only` | Invokes read-only verification | The command stops at the same result LF/CRLF check before it can test non-mutation. |
| `tests/test_luna53_retention.py::test_pinned_inputs_reconcile_without_running_neurons` | Compares current and LF-normalized bytes only to the stored SHA/length | The stored L46 SHA `0d32926f...` and size 2,337,377 describe the exact CRLF transformation. The authenticated historical Git object and current exact checkout have SHA `54220205...` and size 2,337,376. |

The L47F tests share one failing verification gate; do not count them as three
different evidence defects. The failing Luna-46 catalog assertion is a
separate test expectation over the same permitted materialization distinction.
The Luna-53 pin identifies the same canonical L46 object and its exact CRLF
transform; do not replace the historical pin with a new source pin.

## Scope and file ownership

Permitted changes are limited to:

- `experiments/luna53/run.py` — verification logic only; no execution,
  recurrence, condition, or output semantics.
- `experiments/luna47f/diagnostic.py` — retained identity verification only;
  no scoring or analysis semantics.
- `tests/test_luna46_depth_scaling_diagnostic.py`
- `tests/test_luna47f_diagnostic.py`
- `tests/test_luna47f_retained.py`
- `tests/test_luna53_retention.py`
- A Luna-56 execution handoff and additive Luna workflow/changelog status.

Do not edit any file under `artifacts/`, any scientific protocol/configuration,
any `tpcn/` source, any Luna-44–55 runner other than the two explicitly
permitted read-only verifier functions, or any ACP/architecture contract.
No `.gitattributes` change is needed or authorized by this task.

## Governing provenance rule

For each retained input, source, or result:

1. Authenticate its canonical Git blob at the explicit historical revision
   and path. Preserve the existing historical Git-object IDs and semantic
   digests.
2. Separately authenticate checkout bytes. Permit only byte-exact equality
   with the canonical object or that object's exact Git LF-to-CRLF transform
   when the object is LF text without NUL bytes or pre-existing CRLF.
3. Preserve recorded materialization hashes/lengths as historical metadata;
   they may describe either explicitly permitted representation. Never
   normalize arbitrary whitespace, JSON serialization, Unicode, or content.
4. Reject a substantive mutation even if JSON parses, its selected fields
   look equivalent, or a new SHA is supplied by the current checkout.
5. Keep historical source/evidence authentication independent of later
   `HEAD`, whole-repository inventory, or unrelated reviewed changes.
   Luna-47F's original output at `8cddf9d5d3fc0ea6971dc54645e8033c290dc852`
   remains recoverable. Its subsequent retained result is separately pinned
   to its authorized publication source; do not overwrite or re-date either
   historical identity.

For Luna-53, all five original `PINNED_FILES` Git blobs at authorization
revision `04305a2917195888cbbcccf378eba7971551e9b5` are intact. Each recorded
SHA equals either the canonical blob SHA-256 or that blob's exact CRLF
materialization SHA-256. The L46 object `9506369d97babf7bc0ef15ed52efb738dcdcd549`
also has the verified embedded semantic digest
`f72ba671f6d1618ab60cf81d85ac664395646de43c3ad77c226f41b9aa657628`.
Retain these identities and demonstrate that the original CRLF hash remains
checked.

For Luna-47F, verify the retained result and validation at their explicit
historical publication revision `39bedbce47055a7b180593ea312c6b646510c566`,
with Git blobs `74c6859555caf8cb9c5a51f713080b238d716c79` and
`c70c9f1d4ae6f5712b672d54e2e71cef0629cc2a`, respectively. Their current
checkout forms are exact LF for the result and exact LF-to-CRLF for the
validation file. Preserve the currently recorded CRLF SHA literals; check
them against the explicit transform, not unconditionally against worktree
bytes. Continue verifying the result's embedded analysis digest, its fixed
12-input consumed set at `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`, and
the protocol/code Git identities at their declared historical revisions.

## Required acceptance criteria

1. Reproduce the exact five test failures above before correction and record
   their individual baseline output; no scientific condition is run.
2. Preserve every historical Git-object pin, historical SHA/materialization
   record, source revision, and semantic digest. Do not rebaseline evidence.
3. Verify no Luna-46, Luna-47F, Luna-53, Luna-54, or Luna-55 retained
   scientific artifact changes. Specifically preserve the publication objects
   documented in the authorization handoff.
4. Both exact LF and exact LF-to-CRLF materializations pass for the relevant
   verifier fixtures. Arbitrary byte/content changes fail before analysis.
5. Adversarial tests prove:
   - a changed JSON value, appended byte, altered newline pattern, or wrong
     Git blob is rejected;
   - the Luna-47F diagnostic and validation are each rejected when changed;
   - L47F still verifies only its 12 historical consumed inputs and ignores
     unrelated later repository evolution;
   - the read-only check leaves protected bytes unchanged;
   - the L46 catalog test accepts either permitted materialization but rejects
     substantive mutations.
6. All five formerly failing tests pass; directly related tests pass.
7. The full repository suite is green: zero failures and only the existing
   environment-conditioned `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`
   skip when CUDA is unavailable. Add no skip, xfail, or platform bypass.
8. `git diff --check` passes; the handoff identifies every file changed and
   confirms all protected artifact identities before/after.

## Forbidden work

- Do not run or regenerate any Luna-44–55 scientific phase/result, including
  RR, nor execute a Luna-56 scientific experiment.
- Do not modify retained artifacts, their Git pins, semantic hashes,
  scientific interpretation, results, configurations, or protocols.
- Do not update historical pins to `HEAD`, a newer runner, or newer source.
- Do not delete, xfail, skip, or broadly normalize tests or bytes.
- Do not change TPCN runtime/neuron/topology/scoring logic, A01–A15, ACP-0008,
  or any architecture proposal/decision.
- Do not study the six unresolved Luna-55 target streams or authorize Luna-57.

## Completion and stop gate

After satisfying the validation criteria, publish the code/tests/handoff,
push, fetch, verify `HEAD == origin/main` and a clean worktree, then stop for
independent read-only Luna-0 review. Luna-0 must accept the provenance fix and
green suite before any later governance considers a scientific question. This
contract authorizes no such later question.
