---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent post-execution review of Luna-48"
  task_id: "luna-0-independent-review-luna48-20261007"
  component: "Canonical fixture source provenance and runtime reproducibility review"
  status: "complete - PASS WITH FOLLOW-UP"
  contract_version: "1.2"
  branch: "main"
  base_revision: "82e5abdfd65651eeb591e84d71a91c10c773f073"
  result_revision: "governance review publication commit"
  dependencies:
    - "Luna-48 authorization commit 59e5ab7b475b74a23faeddc2563eedf1e044"
    - "Luna-48 execution commit 82e5abdfd65651eeb591e84d71a91c10c773f073"
    - "Luna-44 canonical fixture and retained provenance"
    - "Luna-46 MIXED retained evidence"
    - "Luna-47 isolated retained evidence"
  owner: "Project owner"
  classification:
    - "independent post-execution review"
    - "provenance correction accepted"
    - "runtime reproducibility follow-up required"
    - "no scientific experiment"
  hypothesis: "Luna-48 correctly separates canonical Git-object identity from platform-dependent checkout bytes."
  counter_hypothesis: "The correction normalizes substantive source changes, mutates the historical object, or leaves the pinned identity unverified."
  interfaces_relied_on:
    - ".github/agents/luna-48.agent.md"
    - "scripts/build_luna44_canonical_fixture.py"
    - "scripts/verify_luna44_canonical_fixture.py"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  label_information_boundary:
    - "No labels, evaluation outcomes, neural outputs, or mechanism results were supplied to computation."
  timing_assumptions:
    - "Review used retained fixture timestamps and structural input ordering only."
  reset_boundaries:
    - "No neural or experiment runtime was executed."
  resource_bounds:
    - "Two bounded independent fixture materializations; no topology or neural state mutation."
  authorized_scope:
    - "Independently inspect the Luna-48 diff and source identity boundary."
    - "Verify canonical artifacts, materializations, runtime divergence, and retained test results."
    - "Authorize only the separate Luna-49 runtime-reproducibility characterization."
  unauthorized_scope:
    - "No fixture regeneration or normalization."
    - "No Luna-44/Luna-46/Luna-47 scientific rerun or mechanism composition."
    - "No architecture, ACP, efficacy, hardware, or production claim."
  controls:
    - "HEAD and origin/main both 82e5abdfd65651eeb591e84d71a91c10c773f073."
    - "Clean worktree before and after review."
    - "Pinned Git objects read with git cat-file and compared as raw bytes."
    - "Canonical fixture and provenance hashes checked independently."
  measurements:
    - "Pinned source SHA-256 values."
    - "Historical/current first differing binary64 values and ULP distances."
    - "Full fixture divergence counts and maximum ULP/absolute differences."
    - "Independent materialization byte hashes and structural counts."
    - "Focused, retained, and full-suite test counts."
  information_boundary_check:
    - "PASS: all review computations were downstream-only provenance or numeric analysis."
  hardware_mapping:
    - "Not applicable; no hardware execution or equivalence claim."
  architecture_invariants_touched:
    - "No A01-A15 invariant changed."
  preserves:
    - "Luna-46 MIXED verdict."
    - "Luna-47 isolated evidence and non-composition boundary."
    - "Luna-44 fixture bytes, semantic digest, source revision, and parameters."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-49.agent.md"
    - "workflow/handoffs/luna-0-independent-review-luna48-20261007.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Luna-44/Luna-46 gates: 210 passed."
    - "Luna-47 retained focused suite: 306 passed."
    - "Luna-44 source/provenance mutation subset: 7 passed."
    - "Full repository suite: 1639 passed, 3 failed, 1 skipped."
    - "Two fresh current-environment materializations: byte-identical."
  tests_failed:
    - "Luna-44 fresh materializations differ from the historical Python 3.12.3/Linux fixture under Python 3.11.5/Windows."
    - "Luna-47F retained read-only check reports protected snapshot drift after the Luna-48 source change."
  tests_not_run:
    - "Historical Python 3.12.3/Linux regeneration; unavailable in the review environment."
    - "Fresh downstream Luna-44/Luna-46/Luna-47 scientific execution; excluded by the Luna-48 contract."
    - "Discrete downstream decision equivalence on a regenerated fixture; not established."
  assumptions:
    - "The recorded Python 3.12.3/Linux provenance is sufficient to authenticate the historical generation environment, but not yet a complete reproducible environment image."
  unresolved:
    - "Whether the binary64 divergence is solely Windows CRT/libm variation or includes another runtime dependency."
    - "Whether any downstream discrete threshold or route decision changes under fresh values."
    - "Whether exact regeneration should remain environment-pinned or receive a governed cross-runtime canonicalization."
    - "No dedicated Luna-48 execution handoff was published; this review records the independently reproduced execution evidence."
  recommended_next_agent:
    - "Luna-49 runtime-reproducibility characterization, governance-only and not scientific."
---

# Outcome

**OBSERVED:** Luna-48's source correction is **CORRECT**. The builder obtains
the sequence-builder and point-generator bytes from the pinned Git revision
`a79494cd66be28fd291ed11eddd62d342f457cfd`, compares the executed checkout
after CRLF-to-LF normalization, and records the executed-byte hashes
separately. Substantive source changes are rejected. The verifier checks
manifest identities against pinned Git objects and still requires source files
to exist.

**OBSERVED:** The fixture and provenance remain unchanged:

- fixture SHA-256:
  `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`
- provenance SHA-256:
  `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22`

The four pinned source SHA-256 values match raw Git-object content. The
worktree was clean at review start and end, and `HEAD == origin/main`.

## Runtime divergence

**OBSERVED:** The first difference is stream `c00-000`, point index `3`:

| Field | Historical | Current | Absolute difference | Relative difference | ULP |
|---|---:|---:|---:|---:|---:|
| `x` | `0.16917642496961385` | `0.16917642496961388` | `2.7755575615628914e-17` | `1.6406290427649215e-16` | 1 |
| `y` | `-0.33382994490947676` | `-0.3338299449094767` | `5.551115123125783e-17` | `1.6628571546003924e-16` | 1 |
| `x+y` audit | `-0.1646535199398629` | `-0.16465351993986282` | `8.326672684688674e-17` | `5.0570875665032e-16` | 3 |

Timestamps are bit-identical. Across the full 5164-point comparison, `x`
differs at 219 points, `y` at 195, timestamps at 0, and audit sums at 231.
Maximum differences were 128 ULP / `4.440892098500626e-16` for `x`, 64 ULP /
`2.220446049250313e-16` for `y`, and 256 ULP /
`4.440892098500626e-16` for audit sums.

The earliest divergence is in the spiral generator's trigonometric path
(`math.sin`/`math.cos`, followed by rotated coordinates and Gaussian noise);
the nuisance parameters, point counts, timestamps, stream ordering, and the
first differing point on Python 3.10 Windows match the current Python 3.11
Windows result. This supports **platform/libm variation** over a
Python-version-only cause, but Linux reproduction was unavailable and the
exact historical libm operation has not been independently captured.

**OBSERVED:** The LF checkout and the CRLF historical worktree produce the
same current-environment fixture hash
`60f551e06072b3fb7e814affa97f4a01e079c426d6044d3e710ad9a219ed907e`.
This independently supports executable semantic equivalence for the
line-ending transformation in the current Python/Windows environment; it
does not establish cross-platform numerical equivalence.

## Reproducibility classification

- Source provenance: **PASS**.
- Execution provenance: **PASS for current materializations**.
- Runtime provenance: **PARTIAL**; Python 3.12.3/Linux and build/platform
  information are recorded, but exact regeneration was not reproduced here.
- Exact numerical reproducibility: **NOT ESTABLISHED cross-platform**.
- Scientific reproducibility: **NOT ESTABLISHED for downstream discrete
  decisions**; only structural input invariants and current materialization
  equality were verified without rerunning the scientific path.
- Historical fixture: **VALID AND ENVIRONMENT-PINNED**, not invalidated.

The historical Luna-44 contract records runtime provenance and same-environment
replay, but does not establish a cross-runtime byte-identical regeneration
guarantee. The exact fixture remains the authoritative scientific object.

## Governance disposition

The source-materialization defect is closed, but runtime reproducibility needs
a separate bounded characterization before claiming cross-platform exact
regeneration or resuming a scientific successor that depends on fresh
materialization. Luna-49 is authorized as a governance-only corrective
follow-up; it must not execute a scientific experiment or alter retained
evidence.

**LUNA-48 PASS WITH FOLLOW-UP — RUNTIME REPRODUCIBILITY**
