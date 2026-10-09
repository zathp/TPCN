# Luna-0 Governance Review — Luna-57 Checkout-Materialization Authorization

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-55 provenance failure governance review"
  task_id: "luna-57-checkout-materialization-authorization-20261009"
  component: "Luna-55 retained provenance tests"
  status: "complete"
  contract_version: "1.2"
  branch: "main"
  base_revision: "a5d145d6751ee82a5fae1e2f8ad2f647d06438bc"
  result_revision: "See the commit containing this authorization handoff"
  dependencies: ["Luna-56 checkout-materialization correction"]
  owner: "Luna-0"
  classification: ["OBSERVED: three reproducible test failures", "INFERRED: one shared exact-materialization comparison defect"]
  hypothesis: "All three Luna-55 failures conflate an authenticated historical checkout digest with the exact current checkout representation."
  counter_hypothesis: "Any mismatch in pinned Git objects, permitted exact materializations, semantic/artifact digests, or scientific output would falsify the shared-defect finding."
  interfaces_relied_on: ["Luna-55 fixed phase pins", "Luna-54 integrity catalog", "Luna-46 Git-object and semantic-digest verification"]
  label_information_boundary: ["No labels or runtime inputs changed; no six noncrossing stream identities or values investigated."]
  timing_assumptions: ["Not applicable; no scientific replay."]
  reset_boundaries: ["Not applicable; no runtime execution."]
  resource_bounds: ["Review and three test nodes only; no experiment or artifact regeneration."]
  authorized_scope: ["Publish correction-only Luna-57 agent contract and governance status."]
  unauthorized_scope: ["Do not execute Luna-57.", "No scientific replay, stream-level analysis, artifact mutation, or Luna-58 authorization."]
  controls: ["Fixed historical Git object/revision", "L54 exact LF/CRLF integrity metadata", "L55 selection and publication artifacts"]
  measurements: ["Three specified Luna-55 test nodes reproduced as failures.", "All eight frozen phase pins authenticate to the exact LF object or exact CRLF transform.", "Protected Luna-55 output artifacts match their publication Git objects and catalog hashes."]
  information_boundary_check: ["No scientific data or labels enter computation; review did not run computation."]
  hardware_mapping: ["Not applicable; provenance/test-only correction."]
  architecture_invariants_touched: []
  preserves: ["A01-A15", "ACP-0008 status", "Luna-55 retained result and all historical pins", "Luna-56 comparison contract"]
  architecture_change: false
  proposal: null
  files_changed: [".github/agents/luna-57.agent.md", "workflow/ARCHITECTURE_CHANGELOG.md", "workflow/docs/luna/LUNA_WORKFLOW.md", "workflow/handoffs/luna-0-luna57-checkout-materialization-authorization-20261009.md"]
  tests_added: []
  tests_passing: ["Capability-specific alias/GPU check: 2 passed; directory-symlink case skipped for WinError 1314."]
  tests_failed: ["The three authorized-to-correct Luna-55 nodes reproduce their baseline failures."]
  tests_not_run: ["Full suite at this exact revision; Luna-57 execution and scientific replay."]
  assumptions: ["The exact LF and LF-to-CRLF forms in retained integrity metadata remain the only accepted checkout forms."]
  unresolved: ["Luna-57 must implement the correction, pass its scoped regressions, and stop for independent Luna-0 review."]
  recommended_next_agent: ["Luna-57 bounded correction execution", "Luna-0 independent post-execution review"]
```

## Outcome and owned scope

**DECISION: CORRECTION-ONLY LUNA-57 AUTHORIZED / NOT EXECUTED.** At clean
`main`/`origin/main` revision
`a5d145d6751ee82a5fae1e2f8ad2f647d06438bc`, Luna-0 reproduced the three
remaining Luna-55 failures. All three are the same exact-materialization
provenance issue. No scientific execution was performed, and no Luna-57 code
or tests were changed.

Two nodes fail in `_phase_pins_and_populations()` at the raw SHA check for
`artifacts/luna54/control-initial.json`. The current checkout is the exact
canonical Git object (`e1229a04c4388fbf84dc099295f2f38515b2be5e`, SHA-256
`2d63eb997676b38a6f09a128a8ce353bdec4e32667d589f9a2089c62b2334751`); the
selection's recorded SHA (`b38f974c55536c118ae45c672a0afa0c59ee005af4112840ae2919cf1233b76d`)
is the exact CRLF transform, as explicitly recorded in the Luna-54 integrity
catalog. The same relationship holds for all four Luna-54 phases. All eight
frozen Luna-53/Luna-54 phase inputs authenticate to their pinned object and
are exact LF or exact CRLF materializations.

The third node asserts the Luna-46 helper SHA differs from the checkout SHA.
The fixed object is `9506369d97babf7bc0ef15ed52efb738dcdcd549`; its canonical
SHA/length are `54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51` /
2,337,376, and its exact CRLF SHA/length are the pinned helper identity
`0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e` /
2,337,377. This Windows checkout is exactly CRLF, so equality is correct. The
inequality is not a valid invariant across permitted checkouts.

The selected phase-input records and Luna-55 RR initial/replay, summary, and
integrity catalog match their published Git objects. The three entries in the
Luna-55 integrity catalog match their current bytes. Historical science is
unchanged; the established bounded result remains HH/RH/HR 0, RR 10/16 with
421 route reconciliations. No six-noncrosser stream was investigated.

## Architecture evidence

The correction preserves A01–A15 and does not alter ACP-0008, event/runtime
semantics, scientific interpretation, topology, or accepted results. It is a
test/provenance correction, not an architecture departure; no ACP is needed.

Luna-57 may edit only `experiments/luna55/run.py`,
`tests/test_luna55_factorial.py`, and its execution handoff. It must preserve
fixed Git object/revision checks; accept only exact object bytes or the exact
LF-to-CRLF transform; validate historical materialization metadata separately
from the current checkout; retain semantic and artifact digest checks; and
reject altered/malformed representations. It must not modify historical pins,
artifacts, configurations, `.gitattributes`, the six noncrossers, or any
scientific outputs. Scientific runners, replay, sweeps, and artifact
regeneration are prohibited.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Three named `pytest` nodes | `a5d145d6751ee82a5fae1e2f8ad2f647d06438bc`, Windows, Python 3.11.4 | **Fail: 3 reproduced** | First/third stop at current-vs-recorded raw SHA for control-initial; second fails only on SHA inequality. |
| Exact LF/CRLF and fixed-object comparisons for eight selected phase pins | Same revision | **Pass: 8/8** | Each current file equals its pinned Git object; each recorded checkout SHA matches canonical or exact CRLF identity. |
| Luna-46 fixed-object/materialization comparison | Same revision | **Pass** | Current bytes equal exact CRLF; helper SHA and length equal exact CRLF identity. |
| Luna-55 published artifacts and integrity catalog | Publication `8369c8e70209c553be0662b6d705177308151d68` | **Pass** | RR initial/replay, summary, catalog, and selection match publication blobs; catalog member hashes pass. |
| Symlink/junction and CUDA semantic tests | Same revision, Windows | **Pass with capability skip** | 2 passed, 1 skipped; symlink creation is explicitly capability-gated and raised `WinError 1314`; CUDA node passed. |
| Full repository suite at exact review revision | Same revision | **Not run** | The code-equivalent prior independent review at `f691e543d24343de14e07c682af6c9ead40d2ded` reported 1,729 passed, 3 failed, 1 skipped. |
| Luna-57 implementation, scientific replay, artifact generation | Not authorized in this review | **Not run** | Explicit stop boundary. |

## Assumptions, limitations and unresolved issues

Observed evidence establishes one common exact-materialization cause; no
artifact or scientific-integrity inconsistency was found. The single skip in
the capability check is the Windows directory-symlink privilege case; the CUDA
test passes in this environment. The full suite was not rerun at this
documentation-only review head.

## Reproduction and rollback

Reproduce the three failures with:

```powershell
.\.venv\Scripts\python.exe -m pytest -q `
  tests\test_luna55_factorial.py::test_luna55_retained_phase_pins_and_population_partition `
  tests\test_luna55_factorial.py::test_luna55_reauthenticates_stale_luna46_file_pin_without_mutating_history `
  tests\test_luna55_factorial.py::test_composed_rr_preserves_relay_route_identity_from_rh
```

The read-only review made no code or artifact changes. Revert only the
governance authorization commit if it must be withdrawn; do not rewrite
history or alter unrelated work.

## Next assignment

Luna-57 performs the bounded correction against the published contract,
validates exact LF/CRLF acceptance and adversarial rejection, runs the named
regression nodes and required test suites, records a handoff, and stops.
Luna-0 independently reviews that handoff. No Luna-58 or scientific
successor is authorized.
