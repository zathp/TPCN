---
tpcn_handoff:
  agent: "Luna-51 provenance guard correction execution"
  luna_identifier: "Luna-51"
  descriptive_name: "Historical evidence identity regression correction"
  task_id: "luna-51-provenance-guard-correction-20261008"
  component: "Luna-44, Luna-46, and Luna-47F provenance/test guards"
  status: "blocked"
  contract_version: "1.1"
  branch: "main"
  base_revision: "44ac1c8c7c8934a140da1b51dd807e429fd5b172"
  result_revision: "publication commit containing this handoff"
  dependencies:
    - "Luna-51 authorization and contract at 44ac1c8c7c8934a140da1b51dd807e429fd5b172"
    - "Luna-0 governance decision: workflow/handoffs/luna-0-independent-review-luna50-and-authorization-luna51-20261008.md"
    - "Luna-50 blocked historical-runtime reconstruction"
    - "Luna-44 canonical fixture, Luna-46 retained diagnostic, Luna-47F retained diagnostic"
  owner: "Project owner; next review by Luna-0"
  classification:
    - "correction-only provenance/test-invariant work"
    - "no scientific replay or architecture change"
    - "authorized corrections complete; full-suite integration gate blocked"
  hypothesis: "Historical scientific identity can be checked independently from checkout materialization and unrelated repository evolution."
  counter_hypothesis: "Any accepted variation can mask a substantive source/input change, or a protected scientific object has changed."
  interfaces_relied_on:
    - "Pinned Git objects and exact repository revisions"
    - "Luna-44 canonical fixture/provenance and runtime records"
    - "Luna-46 retained catalog and per-file inventory"
    - "Luna-47F protocol, twelve consumed inputs, retained result, and pre/post guard"
  label_information_boundary:
    - "No labels or neural/task outcomes entered computation."
    - "Validation exercised existing offline retained-data checks only; no task or neural replay was performed."
  timing_assumptions:
    - "No neural timing was evaluated."
  reset_boundaries:
    - "No TPCN runtime was created or reset."
  resource_bounds:
    - "No scientific run, training, mechanism, efficacy, route, threshold, or sensitivity experiment was run."
  authorized_scope:
    - "Correct Luna-44 canonical-runtime versus alternate-runtime test scope."
    - "Authenticate the Luna-46 catalog and JSON artifacts using pinned Git objects while allowing only exact governed LF/CRLF checkout materialization."
    - "Replace Luna-47F's broad historical snapshot comparison with the exact consumed-input identity boundary and independent live pre/post check."
    - "Add adversarial tests and update this handoff, LUNA_WORKFLOW.md, and ARCHITECTURE_CHANGELOG.md."
  unauthorized_scope:
    - "No changes to historical fixtures, provenance, retained scientific artifacts, Luna-46 verdict, or Luna-47F retained result."
    - "No changes to Luna-47B files/tests; its source-pin failure requires Luna-0 governance."
    - "No scientific replay, ACP/A01-A15 change, architecture promotion, hardware claim, runtime provisioning, or Luna-52."
  controls:
    - "Fetched remotes; verified HEAD == origin/main == 44ac1c8c7c8934a140da1b51dd807e429fd5b172 and a clean worktree before editing."
    - "Reproduced the four focused provenance failures before edits."
    - "Pinned Git objects are read at the historical revisions; checkout bytes are checked separately."
    - "The Luna-47F consumed-input list is fixed at the twelve historically declared paths."
    - "Luna-47F's historical 878-entry pre/post manifest is retained and validated internally, not compared to today's whole repository."
    - "Live pre/post hashes cover the twelve inputs plus Luna-47F code, protocol, diagnostic result, and validation record."
    - "Protected artifact hashes and Luna-44 semantic digest were identical before and after validation."
  measurements:
    - "Baseline focused suite: 4 failed, 239 passed, 1 skipped; all four were the authorized provenance-boundary failures."
    - "Final Luna-44 focused suite: 21 passed."
    - "Final Luna-46 focused suite: 175 passed, 1 Windows symlink privilege skip."
    - "Final Luna-47F focused suite: 63 passed."
    - "Final historical/core and Luna-34 through Luna-45 selection: 318 passed."
    - "Final full repository suite: 1,670 passed, 1 failed, 1 skipped."
  information_boundary_check:
    - "PASS: correction tests and retained checks did not feed data or output into TPCN computation."
  hardware_mapping:
    - "Not applicable; no hardware execution or equivalence claim."
  architecture_invariants_touched:
    - "No A01-A15 clause changed."
  preserves:
    - "Luna-44 canonical fixture and provenance hashes and semantic digest."
    - "Luna-46 verdict remains MIXED."
    - "Luna-47 remains non-integrated; task efficacy and useful structural growth are not established."
    - "Luna-47G remains synthetic tolerance evidence; hardware equivalence remains unestablished."
    - "Luna-50 historical-runtime limitation remains parked."
  architecture_change: false
  proposal: null
  files_changed:
    - "scripts/build_luna44_canonical_fixture.py"
    - "scripts/verify_luna44_canonical_fixture.py"
    - "tests/test_luna44_canonical_fixture.py"
    - "tests/test_luna44_canonical_fixture_verification.py"
    - "run_luna46_depth_scaling_diagnostic.py"
    - "tests/test_luna46_depth_scaling_diagnostic.py"
    - "experiments/luna47f/diagnostic.py"
    - "tests/test_luna47f_diagnostic.py"
    - "workflow/handoffs/luna-51-provenance-guard-correction-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added:
    - "Luna-44 exact checkout conversion, authenticated canonical-runtime exactness, and alternate-runtime difference reporting."
    - "Luna-46 exact LF/CRLF catalog materialization, wrong revision/blob, substantive edits, whitespace, missing content, mixed line endings, and per-artifact checkout controls."
    - "Luna-47F twelve-input membership/identity, wrong revision/blob, substitution, protocol/code/result identity, unrelated repository evolution, and live pre/post mutation controls."
  tests_passing:
    - "Luna-51 adversarial selection: 18 passed, 242 deselected."
    - "Combined Luna-44, Luna-46, and Luna-47F focused files: 259 passed, 1 skipped."
    - "Luna-44: 21 passed."
    - "Luna-46: 175 passed, 1 skipped."
    - "Luna-47F: 63 passed."
    - "Historical/core and Luna-34 through Luna-45: 318 passed."
    - "Standalone scripts/verify_luna44_canonical_fixture.py: exit 0."
    - "py_compile on changed Python files and git diff --check: exit 0."
  tests_failed:
    - "Combined Luna-47A-G selection: 311 passed, 1 failed. tests/test_luna47b_gain.py::test_full_retained_reconstruction_and_determinism fails because experiments/luna47b/diagnostic.py requires run_luna46_depth_scaling_diagnostic.py to equal the older Git source at 789dda5988daf72f375d9713bd76a6da2b9e8b34. Luna-51 is authorized to correct the Luna-46 guard in that file, so this assertion rejects the authorized provenance-only source change."
    - "Full suite: 1,670 passed, 1 failed, 1 skipped; the sole failure is the same Luna-47B source-pin check. No other failure or error remained."
  tests_not_run:
    - "Fresh Luna-44 regeneration on CPython 3.12.3/Linux/glibc 2.39: unavailable and not attempted."
    - "Any neural/scientific replay, training, efficacy, topology, or alternate-runtime sensitivity experiment: not authorized and not run."
    - "No Luna-47B source/test modification was attempted because it is outside the committed Luna-51 file scope."
  assumptions:
    - "The Luna-47B failure checks an older complete analyzer source identity rather than separating analyzer semantics from the authorized provenance-guard correction; Luna-0 must decide whether a bounded follow-up is authorized."
  unresolved:
    - "Full-suite acceptance is not met until Luna-0 governs how the Luna-47B source pin should treat the authorized Luna-46 provenance correction."
    - "The task is not integration-ready; do not proceed with scientific work on this result before Luna-0 disposition."
  recommended_next_agent:
    - "Luna-0 independent review of this exact publication and governance disposition of the single Luna-47B source-pin failure; no successor Luna is authorized."
---

# Luna-51 provenance guard correction execution

## Outcome and scope

**OBSERVED:** The three authorized guard corrections are implemented and their
focused adversarial tests pass. The full repository suite is **not green**:
`tests/test_luna47b_gain.py::test_full_retained_reconstruction_and_determinism`
fails because its guard requires the current Luna-46 analyzer file to match
the complete source at `789dda5988daf72f375d9713bd76a6da2b9e8b34`. The authorized
Luna-51 correction necessarily changes `run_luna46_depth_scaling_diagnostic.py`
to distinguish canonical Git objects from exact checkout materialization.
Changing the Luna-47B test or analyzer is outside Luna-51's committed file
scope. No exception, skip, xfail, or weakened assertion was introduced.

Therefore the final disposition is **BLOCKED — GOVERNANCE REQUIRED**. Luna-0
must independently review the corrections and decide whether the Luna-47B
source pin needs a narrowly governed compatibility correction before this
branch is considered integration-ready.

### Luna-44

The old test required every fresh materialization to equal the historical
Linux fixture exactly. The corrected boundary preserves exact canonical
fixture/provenance verification and exact equality between two independent
materializations in one tested environment. Canonical-runtime output must
still match the canonical fixture byte-for-byte and point-bit-for-point-bit.
For other runtimes, the comparison returns exact byte/semantic identities,
point-bit equality, differing point count, and first differing point as
diagnostic evidence. It does not normalize values or claim that alternate
output is canonical.

### Luna-46

The old guard hashed the checked-out catalog bytes as though they were the
canonical Git object. The corrected guard verifies the catalog at pinned
revision `d1f901d3d995dc013f22dd086ae1ed8ffd28293d`, blob
`b1aaef4006422f321922bfb58425e4fb646d96b9`, and canonical SHA-256
`a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`.
It separately verifies the checked-out bytes as either the same bytes or the
exact Git LF-to-CRLF transform. All 22 Luna-45 JSON artifacts and the
specifically pinned historical inputs continue to be checked against canonical
hashes, parsed content, internal digests, inventory, and provenance pins.
Substantive mutation, wrong revision/blob, whitespace changes, mixed endings,
and missing content remain failures.

### Luna-47F

The old check compared a historical whole-repository snapshot and
materialization-specific worktree hashes with later repository state. The
historically consumed input set is now exactly:

1. `artifacts/luna45-acp0008-depth2-destination-integration-20261006/config.json`
2. `artifacts/luna45-acp0008-depth2-destination-integration-20261006/artifact-integrity.json`
3. `artifacts/luna45-acp0008-depth2-destination-integration-20261006/summary.json`
4. `artifacts/luna45-acp0008-depth2-destination-integration-20261006/initial-destination_calibrated.json`
5. `artifacts/luna45-acp0008-depth2-destination-integration-20261006/initial-destination_calibrated-enqueue.json`
6. `artifacts/luna45-acp0008-depth2-destination-integration-20261006/initial-destination_calibrated-reception.json`
7. `artifacts/luna45-acp0008-depth2-destination-integration-20261006/replay-destination_calibrated.json`
8. `artifacts/luna45-acp0008-depth2-destination-integration-20261006/replay-destination_calibrated-enqueue.json`
9. `artifacts/luna45-acp0008-depth2-destination-integration-20261006/replay-destination_calibrated-reception.json`
10. `artifacts/luna44-canonical-fixture/fixture.json`
11. `artifacts/luna44-canonical-fixture/provenance.json`
12. `artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json`

Each input is authenticated against the Luna-47F evidence baseline
`2cef8ea4b37a4ae586e3f383511cba63c9268ddc`, its Git blob recorded in the
retained inventory, its canonical digest, and the exact permitted checkout
transformation. Protocol and execution-source identities are checked against
their published Git revisions; the retained Luna-47F result and validation
files have fixed SHA-256 pins. Historical source-inventory records are no
longer compared as a proxy for current checkout bytes.

Live pre/post non-mutation is separate from historical identity and covers
those twelve consumed inputs plus `experiments/luna47f/diagnostic.py`,
`experiments/luna47f/PROTOCOL.md`, `artifacts/luna47f/diagnostic.json`, and
`artifacts/luna47f/validation.json`. The historic 878-entry snapshot remains
unaltered and self-validated but is not required to match future unrelated
repository evolution.

## Immutable artifact evidence

| Artifact | SHA-256 before and after |
|---|---|
| Luna-44 canonical fixture | `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629` |
| Luna-44 semantic digest | `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305` |
| Luna-44 canonical provenance | `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22` |
| Luna-46 original retained diagnostic | `32561efb9f81996133bc930751083b2678c455668e47f0cd854e7985ad0616df` |
| Luna-46 corrective pre-label artifact | `1c3843127c3de1e9b380fd06571282f0c19cf48a820730bc3ffa1dd5b11e65d4` |
| Luna-46 corrective retained diagnostic | `0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e` |
| Luna-47F retained diagnostic | `f24a56bf5a92f622c4dfdb661116a83a76df1f7b0ae0056d20920360ca3cbb7c` |
| Luna-47F validation record | `e3c8cb236f57908319893c2e109a2c94f5dd8d50e6953f48810da74259a62c29` |

No protected scientific artifact changed.

## Validation record

Environment: CPython 3.11.4, Windows 10 x64. Tests below ran against the
working tree based at `44ac1c8c7c8934a140da1b51dd807e429fd5b172`.

| Command / procedure | Result |
|---|---|
| Focused baseline: Luna-44 builder/verifier, Luna-46 diagnostic, Luna-47F diagnostic/retained tests | 4 failed, 239 passed, 1 skipped; reproduced all four authorized failures |
| New adversarial cases across the authorized focused files, `-k luna51` | 18 passed, 242 deselected |
| Luna-44 focused provenance/materialization files | 21 passed |
| Luna-46 focused diagnostic file | 175 passed, 1 skipped (Windows directory-symlink privilege unavailable) |
| Luna-47F diagnostic and retained files | 63 passed |
| Combined Luna-44, Luna-46, and Luna-47F focused files | 259 passed, 1 skipped |
| Combined Luna-47A-G eight-file selection | 311 passed, 1 failed (Luna-47B historical analyzer source pin) |
| Historical/core and Luna-34 through Luna-45 selection | 318 passed |
| Full repository `python -m pytest -q -rs` | 1,670 passed, 1 failed (same Luna-47B source pin), 1 skipped |
| `python scripts/verify_luna44_canonical_fixture.py` | Exit 0 |
| `python -m py_compile` on changed implementation and test files | Exit 0 |
| `git diff --check` | Exit 0 |

**OBSERVED:** The sole full-suite failure is independent of canonical artifact
mutation and comes from the Luna-47B test's complete-source equality check
against a pre-Luna-51 Luna-46 revision. It remains unsuppressed and requires
Luna-0 governance before the acceptance gate can be considered green.

## Architecture evidence

No A01-A15 clause was changed. The edits only correct evidence identity and
test/provenance checks; they do not modify event execution, neuron behavior,
routing, topology, plasticity, reward, or energy semantics. No ACP, architecture
promotion, or hardware mapping was proposed.

## Benchmark and resource results

Not applicable. No dataset, neural run, training, task metric, prediction
metric, event count, activation count, energy proxy, utility, connectivity,
latency, or capacity measurement was generated.

## Scientific interpretation and retained limitation

No scientific result, threshold, configuration, hypothesis, or verdict was
changed. Luna-46 remains **MIXED**. Luna-47 remains non-integrated and does not
establish task-level efficacy or useful structural growth. Luna-47G remains
synthetic tolerance evidence; hardware equivalence is unestablished.
Downstream alternate-runtime scientific sensitivity remains
**UNKNOWN / NOT TESTED**.

> Fresh exact Luna-44 regeneration under the historical CPython 3.12.3/Linux/glibc 2.39 runtime remains unverified because Luna-50 lacked a usable Linux execution environment. The canonical committed fixture remains the authenticated historical experimental input. Exact binary64 identity for alternate runtimes is not claimed.

## Reproduction and rollback

Run the focused checks with:

```powershell
python -m pytest -q tests/test_luna44_canonical_fixture.py tests/test_luna44_canonical_fixture_verification.py
python -m pytest -q tests/test_luna46_depth_scaling_diagnostic.py
python -m pytest -q tests/test_luna47f_diagnostic.py tests/test_luna47f_retained.py
python -m pytest -q -rs
python scripts/verify_luna44_canonical_fixture.py
```

The full suite is expected to remain blocked by the recorded Luna-47B source
pin until Luna-0 decides on the compatibility scope. Preserve all unrelated
work; rollback only the Luna-51-owned implementation, tests, and documentation
as a coherent change if Luna-0 rejects it. Do not alter protected historical
artifacts or reset the branch.

## Next assignment

**Next and only review role: Luna-0 independent review.** Review this exact
publication, the immutable artifact hashes, the three corrected guard
boundaries, and the single Luna-47B source-pin failure. Decide whether a
bounded compatibility correction for the authorized Luna-46 provenance-only
change is permitted. No scientific work, integration-readiness claim, or
Luna-52 authorization follows from this handoff.
