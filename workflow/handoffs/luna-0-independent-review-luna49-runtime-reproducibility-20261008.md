---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of Luna-49 runtime reproducibility"
  task_id: "luna-0-independent-review-luna49-runtime-reproducibility-20261008"
  component: "Independent numerical/provenance review and historical runtime decision"
  status: "complete - FOLLOW-UP REQUIRED; Luna-50 authorized / not executed"
  contract_version: "1.2"
  branch: "main"
  reviewed_revision: "be6e2d2df179be842208724d20b00d9497d4e4a4"
  result_revision: "the published commit containing this handoff"
  dependencies:
    - "Luna-49 contract published in 7739ad7af868e2b2f5ebcf9685c25978022a25af"
    - "Luna-49 execution be6e2d2df179be842208724d20b00d9497d4e4"
    - "Luna-48 independent review and Luna-44 canonical provenance"
    - "Luna-46 MIXED and Luna-47 isolated retained evidence"
  owner: "Project owner; review request delegates bounded successor decision to Luna-0"
  classification:
    - "independent post-execution review"
    - "runtime provenance follow-up required"
    - "no scientific decision replay or architecture change"
  hypothesis: "Luna-49 correctly characterizes the observed Windows-vs-historical fixture differences, but exact historical-runtime regeneration remains untested."
  counter_hypothesis: "A currently accessible Linux/CUDA runtime may be close enough to the historical runtime to establish exact reproduction or isolate the first primitive divergence."
  interfaces_relied_on:
    - ".github/agents/luna-49.agent.md"
    - "scripts/luna49_runtime_characterization.py and focused tests"
    - "scripts/build_luna44_canonical_fixture.py and verifier"
    - "Luna-44 canonical fixture/provenance"
    - "retained Luna-46 diagnostic and Luna-47F replay guard"
    - "workflow architecture contract, workflow, acceptance criteria, ACP process, and handoff template"
  label_information_boundary:
    - "No labels or evaluation results were read into computation."
    - "No neural/scientific path was replayed."
  timing_assumptions:
    - "Reviewed timestamp/order/batch identity only; no new neural timing analysis."
  reset_boundaries:
    - "No production runtime or network state was created."
  resource_bounds:
    - "Only fixture comparisons and existing test suites; no GPU computation."
  authorized_scope:
    - "Independently verify commit ancestry, clean publication, canonical hashes, report, test counts, host runtime availability, and retained-check failures."
    - "Create one bounded Luna-50 contract for historical CPU runtime reconstruction."
    - "Update this handoff, LUNA_WORKFLOW.md, and ARCHITECTURE_CHANGELOG.md."
  unauthorized_scope:
    - "No canonical fixture/provenance edits."
    - "No Luna-44/Luna-46/Luna-47 scientific replay or decision-margin evaluation."
    - "No Luna-46/Luna-47 evidence repair or rebaseline."
    - "No CUDA/GPU point generation, ACP, architecture promotion, or Luna-51."
  controls:
    - "Fetched remotes and verified HEAD equals origin/main at review start and after publication."
    - "Verified exact Luna-48 authorization SHA 59e5ab7b475b74a23faeddc2563eed87adf1e044 and Luna-49 ancestry."
    - "Canonical artifact SHA-256 verified before/after review."
    - "No test expectations or retained evidence were changed."
  measurements:
    - "Independent exact-bit fixture comparison and ULP summary."
    - "Windows/Linux/CUDA availability and generator dependency inspection."
    - "Luna-49, Luna-44, Luna-46, Luna-47, historical/core, and full test results."
  information_boundary_check:
    - "PASS: read-only provenance review; no labels, neural replay, or feedback into computation."
  hardware_mapping:
    - "RTX 4070 SUPER/CUDA available on Windows; CPU-only generator does not import CUDA/GPU libraries."
    - "No hardware equivalence or GPU numerical result claimed."
  architecture_invariants_touched:
    - "No A01-A15 or ACP change; this is external generator/runtime provenance."
  preserves:
    - "Luna-44 canonical fixture and provenance hashes."
    - "Luna-46 MIXED verdict and retained evidence."
    - "Luna-47 isolated evidence and no-composition boundary."
    - "Luna-49 PASS WITH FOLLOW-UP execution findings."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-50.agent.md"
    - "workflow/handoffs/luna-0-independent-review-luna49-runtime-reproducibility-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Luna-49 focused: 7 passed."
    - "Luna-44 verifier: passed."
    - "Luna-44 tests: 60 passed."
    - "Luna-46 tests: 165 passed, 1 skipped."
    - "Luna-47 focused suite: 306 passed."
    - "Historical/core regression: 676 passed."
  tests_failed:
    - "Luna-44 materialization comparisons: 2 failures against historical Linux fixture."
    - "Luna-46 raw catalog checkout-byte hash: 1 failure; pinned Git blob verified."
    - "Luna-47F retained input replay: 1 failure on stale inventory/snapshot."
    - "Full repository: 1,645 passed, 4 failed, 1 skipped."
  tests_not_run:
    - "Exact historical CPython 3.12.3/Linux/glibc 2.39 materialization; no Linux runtime/container was available."
    - "Downstream fresh-runtime neural decisions/margins; excluded and no counterpart outputs retained."
  assumptions:
    - "The recorded historical Python/platform provenance is internally consistent but lacks exact libm binary identity."
  unresolved:
    - "Historical exact reproduction and primitive PRNG/math divergence remain open."
    - "Downstream scientific decision sensitivity remains unknown."
    - "Luna-46 and Luna-47F retained guard corrections are separate future provenance work, not Luna-50 scope."
  recommended_next_agent:
    - "Luna-50 historical CPU runtime reconstruction, then Luna-0 independent review."
---

# Luna-0 Independent Review — Luna-49 Runtime Reproducibility

## Review Disposition

**LUNA-49 FOLLOW-UP REQUIRED — HISTORICAL RUNTIME REPRODUCTION.** Luna-49's
reported Windows materialization comparison and numerical summary are
independently reproduced. The historical Linux runtime remains unaudited by a
fresh run in this review because the current machine is Windows despite its
visible CUDA-capable GPU. The exact provenance question is therefore not
closed.

The project-owner review request delegates Luna-0 to decide whether a bounded
successor is warranted. One Luna-50 is authorized for historical CPU runtime
reconstruction and primitive numerical isolation only. It does not authorize
downstream scientific decisions, category margins, Luna-46/Luna-47 changes,
or any architecture/ACP work. No Linux execution was claimed.

## Identity and Publication Audit

- `git fetch --all --prune` completed.
- Review start revision, `HEAD`, and `origin/main`:
  `be6e2d2df179be842208724d20b00d9497d4e4a4`.
- Luna-49 execution is the current commit and its contract baseline
  `7739ad7af868e2b2f5ebcf9685c25978022a25af` is an ancestor.
- Exact Luna-48 authorization commit is
  `59e5ab7b475b74a23faeddc2563eed87adf1e044`. The authorization ID printed in
  the Luna-49 report omits `87adf`; repository ancestry resolves the complete
  revision. Luna-48 review commit `82e5abdfd65651eeb591e84d71a91c10c773f073`
  remains in history.
- Luna-49 execution handoff and diagnostic report exist at the paths linked
  below.
- Worktree was clean at review start. Canonical fixture SHA-256 remains
  `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`;
  canonical provenance SHA-256 remains
  `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22`.

## Luna-49 Diagnostic Assessment

**CORRECT WITH FOLLOW-UP.** Independent binary64 comparison of the committed
canonical fixture and materialization A reports 5,164 points, `x` differing at
219 points (maximum 128 ULP), `y` at 195 (maximum 64 ULP), audit `x+y` at 231
(maximum 256 ULP), and timestamps at zero differences. All 320 sequence
identities/order, point identities, and batch ordinals match. An independently
implemented monotone-bit ULP comparison confirms the report. No equal-valued
but bit-distinct fields (including signed-zero cases) occur in this fixture
comparison.

The first difference is `c00-000`, point 3 `x`: historical
`0.16917642496961385`, bits `3fc5a792b63fd50d`; Windows
`0.16917642496961388`, bits `3fc5a792b63fd50e`; absolute difference
`2.7755575615628914e-17`, relative difference `1.6406290427649215e-16`, 1
ULP. The recorded `y` is also 1 ULP different and `x+y` 3 ULP different.
The canonical artifacts are unchanged.

The builder's two current runs have distinct invocation IDs/PIDs and fixture
files; the builder itself launches separate subprocesses and enforces equality
of output bytes, bits, order, and semantic digest. Historical provenance also
retains two distinct Linux invocation/PID records. The Luna-49 comparison
helper, however, trusts some equality metadata recorded in the two
`materialization.json` files rather than recomputing every corresponding
record digest; the committed builder's own comparison does recompute and
validate those fields. This is a test/validator-hardening follow-up, not a
contradiction of the recorded current-run evidence.

The operation trace reconstructs current point 3 from generator parameters,
math, and Gaussian draws, but no historical intermediate values were
recorded. It therefore does not identify the first primitive operation where
the historical and current outputs diverged. The standard-library generator
uses CPU `math` and `random`; the GPU is not part of its path. Serialization
correctly records the already-different binary64 values and is not evidenced
as the origin. The report's current Windows runtime metadata is appropriate
for this run, but its source function hardcodes a Windows CRT observation, so
must be generalized before a Linux capture. Neither limitation changes the
measured report summary.

## Host and Historical Runtime Availability

Observed host: Windows 10 Pro 22H2, build 19045, x64; CPython 3.11.4 in the
workspace venv (the Luna-49 materializations used this runtime); NVIDIA
GeForce RTX 4070 SUPER, driver 616.56, NVIDIA-SMI CUDA UMD 13.4, and installed
NVCC 12.9.41. This is Windows, not Linux. `wsl --list --quiet` found no installed
distribution, Docker is absent, and no Linux shell/container runtime was
available. No remote Linux host credentials/endpoint were supplied. No
system/runtime was installed or modified during this review.

The generator's imported path is CPU-only Python standard-library `math` and
`random` plus repository modules; it imports no CUDA, CuPy, Torch, NumPy, or
other GPU numerical package for point creation. CUDA is provenance context
only and was not used.

Historical provenance records CPython 3.12.3, Linux x86_64, glibc 2.39,
GCC 13.3.0, and two independently identified historical materializations.
Those records show within-environment byte determinism, but are not a fresh
reproduction in this review. Exact historical-runtime reproduction is
**NOT ESTABLISHED**. A disposable Ubuntu 24.04/glibc 2.39 environment with
CPython 3.12.3/GCC 13.3 is a credible near/exact-runtime route when a Linux
runner is provided, making one bounded reconstruction worth authorizing.

The retained records identify run A as invocation
`16d3c11dbfec4963b582377c3ec9939c` / PID 5320 and run B as
`b6187d9a674045488e01d7cdcc5d7a58` / PID 5323. Both record fixture SHA
`66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`, semantic
digest `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`,
5,164 points, and the same order and XYZ-bit digests. The original temporary
run directories are not retained, so this review confirms the committed
provenance records rather than reopening their generated files.

## PRNG and Primitive Cause

The exact pinned generator seeds `random.Random` for nuisance parameters and a
separate `random.Random(seed ^ 0x5EED5EED)` for point timing, radial jitter,
and Gaussian coordinate noise. CPython's `Random.gauss` consumes the MT19937
backed `random()` values and transforms pairs using `_log`, `_sqrt`, `_cos`,
and `_sin`, caching the second Gaussian result. Thus math-library operations
occur both in the spiral/rotation path and Gaussian conversion. Luna-49 did
not retain raw uniform draws or `gauss` transform intermediates on both
platforms; this review cannot attribute the first difference to `sin`,
`cos`, Gaussian conversion, or later arithmetic. Platform/libm remains
plausible but unproven. Luna-50 is authorized to record the draw sequence and
compare identical operands; it must report an unisolated cause if the required
Linux target is unavailable.

## Scientific Sensitivity and Margin

Input order, point identity, timestamp bits, and batch ordinals are
**EXACTLY IDENTICAL**. The canonical fixture hash/semantic identity gate
changes on fresh Windows output, which is an expected identity distinction,
not a scientific decision change.

For the timestamp-order decision, the minimum positive historical adjacent
timestamp gap is `12.926386673536356` time units and observed timestamp
variation is exactly zero; the measured change is zero against that positive
margin. No threshold values or margins for neuron emissions/routes/categories
were recomputed.

Neural threshold crossings, routes, Luna-46 categories, and Luna-47 selections
are **NOT EVALUATED** under alternate-runtime input. Their threshold margins
and scientific sensitivity remain unknown. Replaying those scientific paths
is prohibited by the Luna-49 contract; this review did not do so. The retained
Luna-46 category counts remain historical evidence only and cannot establish
alternate-runtime stability.

## Retained Check Classification

**Luna-46:** The expected catalog Git blob is valid. Its Windows working copy
is one CRLF byte longer and normalizing CRLF to LF exactly matches the blob.
The raw checkout-byte hash assertion therefore fails due to a checkout
materialization invariant, not scientific artifact corruption. Do not
rebaseline it here.

**Luna-47F:** The read-only reproduction fails on retained input drift. Its
stored protected snapshot has 995 entries; the current protected inventory has
999 entries, with 54 differences. The differences include later reviewed
source/governance changes and Git LF-to-CRLF materialization of retained JSON.
This is legitimate post-run repository evolution bound by an overbroad
historical whole-repository snapshot invariant; the Luna-47F code/protocol and
retained scientific rows were not thereby shown mutated. Do not rewrite or
rebaseline the Luna-47 evidence in this review. A future retained-invariant
correction is separate from Luna-50.

## Validation

Environment: CPython 3.11.4, Windows 10 Pro x64, pytest 9.1.1; no Linux
runtime. Results independently observed:

| Selection | Result |
|---|---|
| Luna-49 focused | 7 passed |
| Luna-44 verifier | Passed |
| Luna-44 provenance/materialization tests | 60 passed, 2 failed |
| Luna-46 retained suite | 165 passed, 1 failed, 1 skipped |
| Luna-47 focused suite | 306 passed, 1 failed |
| Historical/core and Luna-34 through Luna-45 selection | 676 passed, 2 failed |
| Full repository suite | 1,645 passed, 4 failed, 1 skipped |

The four full-suite failures are the two Luna-44 cross-environment exact
comparisons, Luna-46 raw checkout catalog SHA, and Luna-47F retained input
drift. No assertion or artifact was altered. Canonical hashes were verified
before and after. Detailed failure traces were retained in the command output
for this review; full suite remains red.

## Governance Decision

**Luna-50 AUTHORIZED / NOT EXECUTED.** Its sole purpose is historical CPU
runtime reconstruction and first-primitive/PRNG-vs-math provenance under
`.github/agents/luna-50.agent.md`. The task must use an ephemeral/provisioned
Linux runtime, not CUDA computation, and must retain two independently
generated runs. No downstream decision comparison, retained-guard repair,
scientific experiment, architecture/ACP change, or Luna-51 is authorized.

Source provenance is **CLOSED** by Luna-48's verified Git-object correction.
Within-runtime determinism is **BYTE-DETERMINISTIC** for the two retained
Linux records, Luna-48's two Windows 3.11.5 runs, and Luna-49's two Windows
3.11.4 runs. Historical exact reproducibility is **NOT ESTABLISHED**.
Cross-runtime numerical reproducibility is **NON-EXACT BUT CHARACTERIZED**.
Scientific reproducibility is **NOT ESTABLISHED**. Fixture validity remains
**VALID — ENVIRONMENT-PINNED**. No A01-A15 clause or ACP is changed.

The next step is **Luna-50 execution -> Luna-0 independent review**. Luna-46
and Luna-47F retained-guard corrections remain separate governance questions.