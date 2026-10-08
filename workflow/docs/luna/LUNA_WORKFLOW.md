# TPCN Luna Multi-Agent Workflow — Event-Driven Architecture

## Luna-53 destination-retention mechanism — SUPPORTED; independent review required — 2026-10-08

**SUPPORTED WITHIN THE FROZEN RETAINED-INPUT MECHANISM SETUP. INDEPENDENT
LUNA-0 REVIEW IS THE NEXT GATE.** The implementation was published at
`2e527934692d96439207b8e15ee6a99eab683a65`; all four fresh-process executions
and the summary are retained under [artifacts/luna53/](../../../artifacts/luna53/).
The summary reports exact initial/replay scientific digests for each
condition, historical-control compatibility on all 320 streams and 235
destination traces per phase, and no-reception isolation.

At the one predeclared intervention (`decay_rate_z=0.00125` versus
`0.0125`), 19/33 temporal-retention-limited streams produced new E2 discharge
with linked canonical emission. These are exactly the 19 predeclared
Luna-47A tau=800 accumulator-crossing streams. None of the 75 drive-limited
or 212 no-reception streams discharged or emitted; there was no clipping or
budget exhaustion. This supports the narrow transfer from the isolated
retention result to the bounded E2 destination discharge/emission path. It
does not establish task efficacy, useful prediction, production parameter
selection, architecture promotion, or hardware equivalence.

The full suite on the execution revision passed **1,704 tests with 1
governed Windows directory-symlink privilege skip**. See the [Luna-53
execution handoff](../../handoffs/luna-53-acp0008-destination-retention-20261008.md),
[execution contract](../../../.github/agents/luna-53.agent.md), and
[Luna-0 scientific selection handoff](../../handoffs/luna-0-scientific-successor-selection-luna53-20261008.md).
No later successor is authorized; stop at independent Luna-0 review.

## Luna-52 clean-checkout correction — complete; documentation follow-up PASS — 2026-10-08

**CORRECTION COMPLETE — CLEAN-COMMIT VALIDATION PASS; LUNA-0 DOCUMENTATION FOLLOW-UP PASS.**
The Luna-0 review found that all ten public CLI subprocess tests failed in
clone setup when the verifier was already committed and identical. The
bootstrap now conditionally commits only changed verifier content, preserves
real Git errors, and asserts its baseline clone is clean. Two bootstrap tests
cover the changed and already-committed states. Three Luna-47B tests now
exercise retained result, protocol, and current-source mutations through
`reconstruct()`.

The corrected focused public-path group passes **12 tests**; the Luna-47B
suite passes **31**, Luna-47F diagnostic/retained **75**, Luna-44/Luna-46
**196 with the existing one Windows symlink-privilege skip**,
Luna-51/materialization **8**, and historical/core **377**. The full suite
ran from clean published commit `0d49c780ee1f4fd63089b1ee9ae17f156c80c668`:
**1,698 passed, 1 skipped, zero failures/errors**. All seven protected
artifact hashes remain unchanged. Luna-0 independently reviewed that commit
and found no test or verifier defect, but initially blocked closure because
this section and the changelog still described clean-commit validation as
pending. Luna-0's follow-up review of the corrected documentation returned
PASS; that review gate is closed. The separate Luna-53 authorization above
is a new scientific-governance decision, not a Luna-52 outcome.

See the [independent Luna-0 review](../../handoffs/luna-0-independent-review-luna52-20261008.md),
[Luna-52 execution handoff](../../handoffs/luna-52-retained-provenance-verification-20261008.md),
[Luna-52 authorization handoff](../../handoffs/luna-0-review-luna51-authorize-luna52-20261008.md),
and [Luna-52 contract](../../../.github/agents/luna-52.agent.md).

## Luna-51 execution — corrections complete; governance required — 2026-10-08

**BLOCKED — GOVERNANCE REQUIRED.** Luna-0 authorized this correction-only
follow-up. Execution started at `44ac1c8c7c8934a140da1b51dd807e429fd5b172`.
The three provenance-boundary corrections and focused adversarial checks are
complete; historical scientific artifacts remain unchanged. Luna-44 focused
tests pass (21), Luna-46 pass (175, 1 Windows symlink privilege skip), Luna-47F
pass (63), and the historical/core plus Luna-34–45 selection passes (318).
The full suite reports **1,670 passed, 1 failed, 1 skipped**. The sole failure
is `tests/test_luna47b_gain.py::test_full_retained_reconstruction_and_determinism`,
whose strict source pin requires the now-corrected
`run_luna46_depth_scaling_diagnostic.py` to match the pre-Luna-51 source at
`789dda5988daf72f375d9713bd76a6da2b9e8b34`. Luna-47B files were not changed;
this requires Luna-0 governance. No test was suppressed or weakened.

Luna-50's
**BLOCKED — HISTORICAL RUNTIME UNAVAILABLE** outcome is a missing capability,
not contradictory evidence. The canonical Luna-44 fixture remains the
authenticated historical input; fresh exact Linux reproduction and exact
cross-runtime binary64 identity are not claimed. Source provenance is closed,
and retained records support within-environment determinism without replacing
a fresh replay. Scientific sensitivity to alternate-runtime-generated inputs
remains unknown.

The authorized corrections repaired:
Luna-44's unconditional alternate-runtime exact comparison, Luna-46's
checkout-byte versus pinned Git-blob check, and Luna-47F's whole-repository
retained snapshot/checkout-sensitive input inventory. Preserve exact artifact
and same-runtime checks; adversarial mutation tests pass. Luna-47F's
consumed-input guard and live pre/post non-mutation check remain distinct
requirements. No scientific replay, evidence rebaseline, architecture/ACP
change, or Luna-52 is authorized. See the
[Luna-51 execution handoff](../../handoffs/luna-51-provenance-guard-correction-20261008.md),
[Luna-0 governance handoff](../../handoffs/luna-0-independent-review-luna50-and-authorization-luna51-20261008.md),
and [Luna-51 contract](../../../.github/agents/luna-51.agent.md).

Next: **Luna-0 independent review** of the execution and disposition of the
Luna-47B source pin. No next causal mechanism experiment is selected or
authorized.

## Luna-50 historical runtime reconstruction — 2026-10-08

**BLOCKED — HISTORICAL RUNTIME UNAVAILABLE.** Execution began at exact Luna-50
authorization revision `b49f6642957ea630598b576c3c57f8862e436a14`; the
contract's `be6e2d2df179be842208724d20b00d9497d4e4a4` field identifies the
Luna-49 execution baseline, not the mandatory Luna-50 starting revision.
The current Windows 10/CPython 3.11.4 host has no usable Linux runtime, WSL
distribution, Docker/Podman, or supplied remote endpoint. No provisioning or
installation was attempted. The target is **UNAVAILABLE**; two independent
historical-runtime materializations and Windows/Linux primitive comparison
were **NOT RUN / NOT AVAILABLE**. CUDA was not used.

A CPU-only Windows point-3 control reproduces its own output exactly and
records raw MT draws, Gaussian cached-state/transforms, trigonometric values,
coordinate operation order, binary64 bits, serialization round trips, and
source/runtime identities in
[`windows-control.json`](../../../artifacts/luna50-historical-runtime-20261008/windows-control.json).
Against the historical final point, x and y each differ by 1 ULP and t is
bit-identical. Historical intermediates are unavailable; the divergence cause
remains unassigned, with no libm attribution. Canonical fixture and provenance
hashes are unchanged. See the [Luna-50 execution handoff](../../handoffs/luna-50-historical-runtime-reconstruction-20261008.md).

Validation: Luna-50 **6 passed**; Luna-49 **7 passed**; Luna-44 standalone
verifier passed; Luna-44 fixture/provenance tests **17 passed, 2 known
failures**; Luna-46 **165 passed, 1 known failure, 1 skipped**; Luna-47A-G
**306 passed, 1 known failure**; historical/core selection **350 passed, 2
known failures**; full suite **1,651 passed, 4 known failures, 1 skipped**.
The four failures are the two Windows-versus-frozen Luna-44 comparisons,
Luna-46 checkout-byte catalog hash, and Luna-47F stale retained inventory.
No retained evidence was repaired. Required next step: **Luna-50 execution ->
Luna-0 independent review**. No architecture clause, ACP, or successor is
authorized.

## Luna-0 independent review — Luna-49 runtime reproducibility — 2026-10-08

**LUNA-49 FOLLOW-UP REQUIRED — HISTORICAL RUNTIME REPRODUCTION.** Review at
`be6e2d2df179be842208724d20b00d9497d4e4a4` independently verified the
canonical fixture/provenance hashes, Windows materialization hashes, first
1-ULP `x` divergence, and full-fixture difference counts. Luna-49's diagnostic
is **CORRECT WITH FOLLOW-UP**: it establishes the observed Windows comparison,
but does not compare historical primitive intermediates or establish exact
historical-runtime reproduction.

The current host is Windows 10 x64 with an RTX 4070 SUPER and CUDA driver
support; WSL has no installed Linux distribution and Docker is unavailable.
The generator imports CPU Python `math`/`random` and repository code only; CUDA
does not participate. No Linux materialization was performed. Historical exact
reproduction remains **NOT ESTABLISHED**, and fresh-runtime neural/category
decision sensitivity remains **NOT TESTED / UNKNOWN**. Source provenance is
**CLOSED**; fixture validity remains **VALID — ENVIRONMENT-PINNED**.

Luna-0 authorizes **Luna-50**, a single bounded historical CPU runtime
reconstruction and primitive/PRNG-vs-math characterization, **AUTHORIZED / NOT
EXECUTED**. It excludes GPU generation, downstream scientific replay, and
Luna-46/Luna-47 retained-evidence repair. The Luna-46 CRLF catalog failure and
Luna-47F stale whole-repository snapshot are separate retained-provenance
issues and remain unmodified. See the [independent review handoff](../../handoffs/luna-0-independent-review-luna49-runtime-reproducibility-20261008.md)
and [Luna-50 contract](../../../.github/agents/luna-50.agent.md).

Validation: Luna-49 focused **7 passed**; Luna-44 provenance/materialization
**60 passed, 2 failed**; Luna-46 **165 passed, 1 failed, 1 skipped**; Luna-47
focused **306 passed, 1 failed**; historical/core **676 passed, 2 failed**;
full suite **1,645 passed, 4 failed, 1 skipped**. The four failures are the
two Luna-44 exact environment comparisons, Luna-46 raw checkout catalog hash,
and Luna-47F retained input drift. No failure was suppressed or repaired.
Next step: **Luna-50 execution -> Luna-0 independent review**.

## Luna-49 execution — PASS WITH FOLLOW-UP — 2026-10-08

The runtime/numerical characterization is complete from clean baseline
`7739ad7af868e2b2f5ebcf9685c25978022a25af`. Two independent CPython 3.11.4
Windows materializations agree byte-for-byte at fixture SHA
`60f551e06072b3fb7e814affa97f4a01e079c426d6044d3e710ad9a219ed907e`; the
canonical Linux fixture and provenance hashes remain unchanged. The first
observable binary64 difference is `c00-000`, point 3 `x`, at 1 ULP. The
current operation trace reproduces the coordinate, but historical trig and
Gaussian-noise intermediates were not retained. Windows/libm variation is a
leading candidate, not an isolated cause; the exact Python 3.12.3/Linux
historical environment could not be replayed.

Sequence order, point identities, batch ordinals, and timestamps are identical
for all 5,164 points. The retained downstream data has no counterpart decisions
for the fresh coordinates, so threshold crossings, route changes, and
Luna-46 category sensitivity remain **UNKNOWN / NOT TESTED**. The fixture
remains **VALID AND ENVIRONMENT-PINNED**; scientific reproducibility is not
established. Details, runtime metadata, ULP histograms, and the operation trace
are in the [Luna-49 execution handoff](../../handoffs/luna-49-runtime-reproducibility-20261008.md)
and its [diagnostic artifact](../../../artifacts/luna49-runtime-reproducibility-20261008/characterization.json).

Validation: Luna-49 focused **7 passed**; Luna-44 provenance/materialization
**60 passed, 2 failed**; Luna-46 retained gate **165 passed, 1 failed, 1
skipped**; Luna-47 focused **306 passed, 1 failed**; historical/core regression
**676 passed, 2 failed**; full suite **1,645 passed, 4 failed, 1 skipped**.
The two Luna-44 failures remain environment-pinned exact-comparison failures;
Luna-46 hashes a CRLF checkout rather than its matching Git blob; Luna-47F
reports stale retained input/snapshot drift following reviewed source and
governance changes. None was suppressed or repaired. Canonical and retained
scientific artifacts were not changed.

**PASS WITH FOLLOW-UP.** Exact historical-runtime regeneration and downstream
neural-decision sensitivity remain open. No efficacy, mechanism, architecture,
ACP, hardware, or Luna-50 conclusion is authorized. The required next step is
**Luna-49 execution -> Luna-0 independent review**.

## Luna-0 post-Luna-48 review — Luna-49 runtime reproducibility authorized — 2026-10-07

**LUNA-48 PASS WITH FOLLOW-UP — RUNTIME REPRODUCIBILITY.** The independent
post-execution review accepted the Luna-48 Git-object source correction:
canonical fixture/provenance hashes remain unchanged, CRLF/LF-equivalent
materialization is checked without hiding substantive source changes, and two
current Windows materializations agree byte-for-byte. The historical fixture
was generated under Python 3.12.3/Linux; fresh Python 3.11.5/Windows output
differs first at a one-ULP trigonometric coordinate and is not yet proven
cross-runtime identical. The fixture remains valid and environment-pinned.

Luna-49 is authorized only to characterize and govern this runtime/numerical
reproducibility boundary. It must not regenerate or alter the canonical
fixture, run Luna-44/Luna-46/Luna-47 scientific paths, compose mechanisms,
change scientific parameters, repair retained evidence, or authorize Luna-50.
See [Luna-49](../../../.github/agents/luna-49.agent.md) and the
[independent Luna-48 review](../../handoffs/luna-0-independent-review-luna48-20261007.md).

## Luna-0 post-Luna-47 review — Luna-48 authorized / not executed — 2026-10-07

**CORRECTIVE FOLLOW-UP AUTHORIZED.** Independent review of published commit
`39bedbce47055a7b180593ea312c6b646510c566` confirmed that the remaining
Luna-44 gate fails before fixture generation: the pinned historical worktree
does not carry the later LF checkout attribute, so Windows materializes its
Python sources as CRLF while the worker compares checkout bytes with canonical
Git-blob SHA-256 values. The committed source and fixture identities verify
in the current checkout; the failure is a materialization/provenance defect,
not evidence that the canonical fixture should change.

Luna-48 is authorized only to correct this provenance path while preserving
the pinned source revision, fixture bytes, semantic digest, generation
parameters, and all existing acceptance criteria. Its contract is
[Luna-48](../../../.github/agents/luna-48.agent.md), and its authorization
handoff is [here](../../handoffs/luna-0-authorization-luna48-20261007.md).
Luna-48 is **not executed in this governance pass**. No causal composition of
Luna-47 mechanisms, production promotion, ACP action, Luna-49, or Luna-48
scientific readiness is authorized. After the correction, Luna-0 must make a
separate decision on any single causal mechanism question.

## Luna-47 final corrective pass — 2026-10-07

**FINAL CORRECTIVE PASS INCOMPLETE — no Luna-48 authorization.** The
integrated Luna-47F retained replay guard now checks only staged and unstaged
working-tree mutations, so the published integrated `main` revision is a
valid replay context. The regenerated retained artifact passes its code and
protocol identity checks. The Luna-47 focused suite passes **307 tests** and
the historical/core compatibility audit passes **377 tests**.

The repository-wide suite remains red: **1 failed, 7 errors, 1632 passed,
1 skipped**. The failure and errors are the existing Luna-44 canonical-fixture
source/materialization mismatch on this Windows checkout. More importantly,
Luna-47A–G remain isolated mechanism/model investigations; no composed causal
efficacy, hardware-equivalence, or production evidence exists. The exact
corrective record is in the
[final Luna-47 handoff](../../handoffs/luna-47-final-corrective-pass-20261007.md).
Luna-0 must independently review this result before any separately bounded
follow-up. No Luna-48 contract, composition experiment, ACP action, or
production promotion is authorized.

## Luna-47 independent review and synthesis — 2026-10-06

**Review complete; FOLLOW-UP REQUIRED — promising unresolved mechanisms.**
The seven pushed, isolated lane pins were independently inspected and tested
without merging or composing their implementations. Reviewer verdicts:
**A PARTIALLY SUPPORTED; B SUPPORTED (mathematical first-crossing only);
C PARTIALLY SUPPORTED; D SUPPORTED (synthetic output regimes only);
E PARTIALLY SUPPORTED (documentary primitives only);
F PARTIALLY SUPPORTED (geometrical proxy only); G PARTIALLY SUPPORTED
(assumed independent stand-in only).**

Evidence, exact pins, predeclaration/correction audit, independent oracles,
test failures and interpretation boundaries are in the
[completed Luna-0 handoff](../../handoffs/luna-0-independent-review-luna47-20261006.md)
and [review synthesis](../../../artifacts/luna47-review/SYNTHESIS.md).
Fresh focused lane tests: **306 passed**; governance boundary regressions:
**332 passed**, with **21 additional canonical-neuron/predictive checks passed**.
The required raw governance full suite remains **FAILED**:
**1,324 passed, 2 failed, 7 errors, 1 CUDA skip; exit 1**.
The supplied same-revision baseline had 1,325 passed, 1 failed, 7 errors,
1 skip; the additional raw catalog failure is an exactly verified LF/CRLF
checkout mismatch, not a changed scientific blob or a waived test.

These results do not establish a composed neuron, task efficacy, selective
noise rejection, useful source-local candidate growth, owner-accessible
validated hardware, or commercial analog yield. E's reported prior criteria
freeze is not independently proven by Git: criteria and findings first appear
in the same commit. Keep all lane negative and pre-correction history.

**No architecture change or successor authorization.** No Luna-48, other
successor contract/dispatch, composition/integration experiment, production
promotion, ACP action, purchase or hardware build is authorized in this cycle.
Luna-46 remains **MIXED**; ACP-0007/0008 and A01–A15 are unchanged.
The project owner, through Luna-0, is the next decision recipient. Questions
for separately authorized follow-up are recommendations, not active work.
The following authorization entry remains as history at its publication date.

## Luna-47 evidence-lane authorization — 2026-10-06

**Luna-47A through Luna-47G are AUTHORIZED / NOT EXECUTED**, solely for the
isolated experimental investigations described in their contracts:
[47A temporal retention](../../../.github/agents/luna-47a.agent.md),
[47B drive gain](../../../.github/agents/luna-47b.agent.md),
[47C noise qualification](../../../.github/agents/luna-47c.agent.md),
[47D output compression](../../../.github/agents/luna-47d.agent.md),
[47E hardware realizability](../../../.github/agents/luna-47e.agent.md),
[47F replay-only candidate generation](../../../.github/agents/luna-47f.agent.md),
and [47G analog variation robustness](../../../.github/agents/luna-47g.agent.md).
The project-owner instruction is recorded in the
[Luna-0 authorization handoff](../../handoffs/luna-0-authorization-luna47-20261006.md).

### Luna-47A execution status — 2026-10-07

**Luna-47A execution is complete with a PARTIALLY SUPPORTED verdict.** The
completed experiment, replayable results, and handoff are recorded in the
[Luna-47A WEMA temporal-retention handoff](../../handoffs/luna-47a-wema-temporal-retention-20261006.md).
Luna-47B through Luna-47G remain authorized and not executed.

The exact experimental source/evidence baseline is
`2cef8ea4b37a4ae586e3f383511cba63c9268ddc`. Every lane must start from the
same published Luna-0 authorization revision recorded in that handoff; it
must be a documentation-only descendant of the stated baseline. Execute each
lane in an isolated branch/worktree. Retained read-only evidence may be
shared; lane code, generated changes, and unreviewed results may not. Each
lane must preserve replayable, machine-readable evidence with source revision,
configuration, fixture identities/hashes and numerical tolerances. A lane
that needs another lane's result must report that dependency and may use only
its separately published, reviewed evidence.

The authorization permits mechanism/evidence work only. The current
production architecture remains the comparison baseline. There is no
authorization to promote WEMA or any other experimental model, alter
production neuron semantics, topology or A01-A15, claim task efficacy or
hardware equivalence, create an ACP, or execute Luna-48. Preserve Luna-46's
independently reviewed **MIXED** scientific verdict and retained artifacts;
do not silently reinterpret its evidence. Each lane must complete its
handoff, push its changes/artifacts, and stop for independent Luna-0 review.
Only after review may Luna-0 determine whether a separately bounded follow-up
or an architecture proposal is warranted.

## Luna-46 corrective completion — 2026-10-06

**Corrective cycle complete; independent Luna-0 review PASS; scientific
verdict MIXED, unchanged.** The corrective implementation is
`96d015ecd8f6b5684237c489898ee33e4496a1cd`; Luna-0's independent corrective
review is recorded in
[`luna-46-corrective-verification-20261006.md`](../../handoffs/luna-46-corrective-verification-20261006.md).
The retained corrected output is
`artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json`.

The correction adds canonical output-path protection for the frozen Luna-44
fixture and retained evidence, plus analytical critical-rate classifications.
It does not change diagnostic categories, retained evidence, or the
predeclared **MIXED** scientific result: 212 `NO-RECEPTIONS`, 33
`TEMPORAL-RETENTION-LIMITED`, 75 `DRIVE-LIMITED`, 0
`CANCELLATION-LIMITED`, and 0 `ALREADY-CROSSING`. Of 320 sequences, 108 are
reception-bearing, with 235 destination receptions. No production
computation, tuning, efficacy study, ACP change, or architecture promotion
occurred.

Validation on Windows: Luna-46 focused tests **167 passed**. The full suite
reported **1 failed, 7 errors, 1 skipped, 1,325 passed**. The failure and
errors are the documented Luna-44 pinned-source materialization issue:
global `core.autocrlf=true` converts the pinned LF source to CRLF in the
temporary worktree, causing its pinned-source hash check to fail. This full
suite remains failed; no failures were hidden or waived.

The independent review retains two limitations: mixed-sign cases are
conservatively classified as uniqueness-unproven rather than exhaustively
root-solved; and output-path validation cannot eliminate a filesystem alias
replacement race after validation but before writing. Earlier workflow
entries recording a review as pending describe their state at the time and
are preserved for audit; this corrective completion supersedes that pending
status. **No successor Luna is authorized.**

## Luna-0 independent review — Luna-46 retained depth-scaling diagnostic — 2026-10-06

**PASS for the bounded evidence gates; independently recomputed verdict:
MIXED.** Fresh Luna-0 review was performed read-only at published Commit C
`b601ffecf6c0ddc8b87b878a31f4366b8fa3ac0a`. It independently checked the
33 pinned input identities, all 22 Luna-45 catalog entries and internal
digests, six initial/replay phase digests, output SHA-256/internal digest,
and exact initial/replay raw-capture identities. All 1,950 captured route
enqueue/reception pairs per phase reconcile; the 235 relay-to-destination
pairs have zero duplicates, orphans, missing rows, or mismatches.

Independent reconstruction of all 235 destination updates used retained
prior timestamps and `lambda=0.0125`, `tau=80`, `theta_Z=1`. The largest
recurrence residual was `1.1102230246251565e-16`, below the committed
64-epsilon bound; no actual threshold crossing, direct admission, discharge,
clipping, or destination canonical emission occurred. The signed offline
zero-decay oracle crossed in 33 streams. The exact partition is 212
`NO-RECEPTIONS`, 0 `ALREADY-CROSSING`, 33
`TEMPORAL-RETENTION-LIMITED`, 0 `CANCELLATION-LIMITED`, and 75
`DRIVE-LIMITED`. With `N=108`, cutoffs are 27/11/81, yielding the
predeclared **MIXED** verdict.

Five `roots_truncated=true` flags match between enqueue and reception,
each with the retained bounded 16-root list. This marks incomplete causal-root
metadata, not missing capture rows; full ancestry expansion is not claimed
for those five events. The matched Luna-44 first-hop versus Luna-45 second-hop
timing, signs, and run statistics were independently recomputed and remain
descriptive, not a causal depth or efficacy conclusion. The evidence supports
considering a future separately authorized adaptive-timescale question only;
it does not establish a finite useful rate, and is not a WEMA, ACP-0008,
parameter, or efficacy recommendation.

Validation: Luna-46 focused **122 passed**; the selected Luna-38–45,
Luna-44, runtime, and topology regression set **237 passed** with the same
two known Windows-versus-frozen-Linux fixture-materialization failures;
full suite **1,286 passed, 2 known failures, 1 CUDA-unavailable skip**.
`py_compile` and `git diff --check` passed. No new failure was observed.
The failures remain failures and cross-platform parity remains unresolved.

Luna-42 **PASS WITH FOLLOW-UP**, Luna-43 **BLOCKED / DESTINATION COMPARISON
UNDETERMINED**, Luna-44's reviewed canonical-fixture relay-propagation
baseline, and Luna-45 **NOT SUPPORTED IN THIS SETUP** are preserved.
ACP-0007 is unchanged/disabled; ACP-0008 remains experimental, opt-in, and
unpromoted. No A01–A15 or ACP amendment was made. The independent review and
full evidence are in
[`luna-0-independent-review-luna46-depth-scaling-diagnostic-20261006.md`](../../handoffs/luna-0-independent-review-luna46-depth-scaling-diagnostic-20261006.md).
No Luna-47 is authorized.

## Luna-0 Luna-46 authorization gate - 2026-10-06

**LUNA-46 AUTHORIZED / NOT EXECUTED; Commit A is governance only.** Baseline is
`d1f901d3d995dc013f22dd086ae1ed8ffd28293d` on the clean, published
`copilot/luna46-depth-scaling-diagnostic` branch. The merged Luna-45 corrective
review commit `5ebc9ae7dcaae7ff45f0769686885dcae3f2dea4` is an ancestor.
The retained corrective review reports retained-provenance-only ancestry,
canonical replay byte equality, and no blocking correctness findings; its
verification JSON matches the recorded SHA-256. This authorization gate is
not a new independent review or scientific interpretation.

Current baseline validation: Luna-45 focused tests **75 passed**, exit 0;
the existing provenance/routing/ACP-0008/runtime regression command **348
passed, 2 failed**, exit 1; full suite **1,164 passed, 2 failed, 1 skipped**,
exit 1. Both failures are the previously documented Windows-versus-frozen-Linux
fixture-materialization comparisons; CUDA is unavailable. No new failure was
observed. `git diff --check` passed. Exact commands and exceptions are recorded
in the [authorization handoff](../../handoffs/luna-0-authorization-luna46-depth-scaling-diagnostic-20261006.md).

The owner's exact attachment specification was forwarded by the lead in a
same-task correction; the earlier uncommitted missing-attachment blocker was
a delegation omission, not absent owner authorization. The
[Luna-46 contract](../../../.github/agents/luna-46.agent.md) predeclares the
signed lambda=0.0125 recurrence (tau=80, theta_Z=1), offline zero-decay
accumulator, NO-RECEPTIONS / ALREADY-CROSSING / TEMPORAL-RETENTION-LIMITED /
CANCELLATION-LIMITED / DRIVE-LIMITED partition, and reception-bearing
denominator. Substantial means ceil(25% of N); material means ceil(10% of N).
Support requires retention substantial with drive/cancellation under material,
or drive/cancellation at least 75% with retention under material; other valid
splits are MIXED. Insufficient/corrupt evidence, missing required raw inputs
or recurrence mismatch are BLOCKED. Counts/fractions accompany every verdict.

Later bounded work uses retained Luna-45 calibrated raw emissions/enqueues/
successful receptions first, with independent one-to-one reconciliation,
trajectory reconstruction under the committed numerical policy, exact
threshold classification, signed/retention/timing metrics, and fair retained
Luna-44 first-hop comparison where possible. Only proven missing observations
permit observation-only capture with the unchanged frozen experiment and
non-interference checks. Offline accumulators are not production neurons.
Comprehensive synthetic tests and retained integrity checks precede analysis.
No code, tests, artifacts, sequence analysis, or science was performed in
Commit A. No tuning, parameter/configuration sweep, alternate run, production
configuration change, WEMA, ACP/core/runtime/topology/fixture change, efficacy,
or Luna-47 is authorized.

Luna-42 **PASS WITH FOLLOW-UP**, Luna-43 **BLOCKED / DESTINATION COMPARISON
UNDETERMINED**, the Luna-44 reviewed canonical-fixture relay-propagation
baseline, and Luna-45 **NOT SUPPORTED IN THIS SETUP** are preserved.
ACP-0007 remains unchanged/disabled; ACP-0008 remains experimental, opt-in,
and unpromoted. No A01-A15 or ACP change.

## Luna-0 corrective review — Luna-45 ancestry and replay evidence — 2026-10-06

**CORRECTIVE VERIFICATION PASS; original scientific disposition unchanged.**
The independent Luna-0 review of branch revision
`de6df64afda00d9ee4a63aa4de52d35c895b31a9` found no blocking correctness
issues in the corrected source-root ancestry reconstruction or canonical replay
byte acceptance. The correction is limited to the Luna-45 runner, focused
tests, and an offline verifier over retained evidence; it does not rerun the
experiment or alter the 2026-10-06 raw artifacts.

The verifier at revision `2392b78fe5ed0ae773ac957cd0b384c71d0f1eed` recomputed
the canonical initial/replay phase material for all three arms. Each pair was
byte-identical with equal SHA-256 and no byte difference; all 22 files in the
original integrity catalog still match. The original result remains
**NOT SUPPORTED IN THIS SETUP**. There were zero destination canonical
emissions, so real retained destination ancestry validation is not applicable;
exact-root and corruption cases are exercised by synthetic focused tests.

Non-blocking review notes: raw-file non-mutation is supported by read-only
verifier inspection and the unchanged catalog hashes, not by a before/after
snapshot. Validation on Windows/Python 3.11.5: Luna-45 focused tests **75
passed**; relevant regression selection **332 passed, 2 failed**; full suite
**1,164 passed, 2 failed, 1 skipped**. Both failures are the known Windows
versus frozen-Linux fixture-materialization comparisons; the CUDA test was
skipped because CUDA is unavailable. `py_compile` and `git diff --check`
passed. Full corrective evidence:
`artifacts/luna45-corrective-verification-20261006-r1/verification.json`;
the independent disposition is appended to
`workflow/handoffs/luna-0-independent-review-luna45-depth2-destination-integration-20261006.md`.
No successor, tuning, promotion, or Luna-46 is authorized.

## Luna-0 owner-authorized Luna-45 — depth-2 destination integration mechanism — 2026-10-06

**LUNA-45 — AUTHORIZED / NOT EXECUTED.** The project owner directly authorized
a bounded mechanism experiment at baseline
`dbb440c763509781ee7ac5e4f2924851dde8e19c` on
`copilot/luna45-depth2-destination-integration` (published from current
`origin/main`). This is a governance-only update: no code, test, fixture, ACP
or experiment change and no scientific result.

Scope: consume the frozen committed Luna-44 fixture (3,451,453 bytes; file
SHA-256 `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`;
semantic digest
`6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`; seeds
`0..4`, 320 sequences, 5,164 ordered points) with complete pinned provenance
and no generator call. Fixed `source -> relay -> destination` topology with
ordinary `w=1`, delay `1.0`, `d=1`, `r=0` edges; source integration `None`;
relay calibrated `decay_rate_z=0.0125` unchanged; only the destination varies:
disabled, default `0.1`, or calibrated `0.0125`. Required: historical gate,
upstream invariance, independently captured and reconciled enqueue/reception
streams with exact source equality (and the retained source-mutation test),
destination recurrence and direct-versus-integrated emission accounting,
bounds, replay semantics, artifact provenance and retained execution evidence.

Not authorized: tuning, topology change, ACP-0007 candidate instantiation or
growth, efficacy/classification/energy claims, Windows/Linux parity work, ACP
changes, promotion, or Luna-46. Historical verdicts are preserved: Luna-42
PASS WITH FOLLOW-UP; Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED;
Luna-44 evidence-quality PASS WITH FOLLOW-UP. ACP-0008 remains experimental,
opt-in and unpromoted; ACP-0007 unchanged/disabled.

Baseline evidence is recorded in the authorization handoff
`workflow/handoffs/luna-0-authorization-luna45-depth2-destination-integration-20261006.md`
and contract `.github/agents/luna-45.agent.md`.
## Luna-0 review of Luna-44 evidence-quality correction — 2026-10-05

**PASS WITH FOLLOW-UP; task branch published but not merged.** The independent
review applies to `c271b7812d35b1b951e6e0fc088d28ee8abd8711` on
`copilot/luna44-independent-routing-evidence`; authoritative `main` remains
`b266077e47b71f36dbd87051da3e5b5ec1199b37`. The evidence-only change adds
separate queue-admission and successful receiver-consumption captures,
one-to-one exact event reconciliation, four initial/replay raw artifacts, and
fault-injection tests. No production computation, topology, ACP, architecture,
or A01-A15 contract change was made.

The four prior review findings are explicitly dispositioned:

- **A CLOSED:** current provenance says one original fixture publication and
  that its original independent-materialization count is not established;
  two later invocations are reported separately.
- **B CLOSED:** the complete current provenance manifest is pinned by the
  exact Git blob at `86e5a2f389af06b06bf04a614edaed88e0847902` and complete
  SHA-256 `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22`.
- **C CLOSED:** independent initial and replay enqueue/reception streams each
  reconcile. Per phase, 5,145 source-to-relay and 235 calibrated
  relay-to-destination events match, with zero unmatched, orphan, duplicate,
  payload, timing, identity, route/path, or provenance mismatches.
- **D CLOSED within tested-environment scope:** distinct process/invocation
  records establish post-publication repeated materialization in its declared
  Linux environment. Independent Windows/Python 3.11.5 materializations are
  also identical to each other but differ from the frozen Linux fixture; no
  cross-platform identity claim is made. Historical Linux A/B output
  directories were temporary and cannot now be reopened.

The unchanged-configuration scientific rerun is retained in
`artifacts/luna44-acp0008-independent-routing-rerun-20261005/`, tied to
runner revision `4baab60f87b820db800e04d0eb3277fb0e94f9b3`. It reports
**PASS / SUPPORTED** for the authorized relay-propagation endpoint and exact
replay. This is not task efficacy, a destination-integration result, an energy
benefit, or an architecture promotion.

Validation: Luna-44 focused runner tests **43 passed**; the independent
Luna-0 focused selection **227 passed**. The full suite under process-scoped
LF checkout configuration reported **1,089 passed, 2 failed, 1 skipped**.
Both failures are exact frozen-fixture-versus-fresh-Windows-materialization
comparisons; they are not relaxed. One CUDA-only test was skipped. The native
Windows/Python 3.11.5 materializations are repeatable with each other, but
cross-platform canonical fixture parity remains unresolved.

Luna-42 remains **PASS WITH FOLLOW-UP** and Luna-43 remains **BLOCKED /
DESTINATION COMPARISON UNDETERMINED**. ACP-0007 is unchanged/disabled;
ACP-0008 remains experimental, opt-in, and unpromoted. The task branch is not
authoritative main. The complete review and validation record is
`workflow/handoffs/luna-0-review-luna44-evidence-quality-20261005.md`; return
the merge and any cross-platform parity decision to the project owner. No
successor Luna is authorized by this evidence review.

## Luna-0 owner-authorized Luna-44 — canonical fixture and relay propagation

**LUNA-44 AUTHORIZED / NOT EXECUTED.** The project owner has authorized a frozen
point-level fixture from the stipulated existing generator (seeds `0..4`, 64
ordered sequences per seed) and a three-condition relay-propagation experiment
with replay. Each point records seed, sequence index, deterministic label-free
stream ID `c{seed:02d}-{sequence_index:03d}`, zero-based point index in source
order, zero-based sequence-local batch ordinal, raw `x/y/t`, and `x+y` as an
audit value; number sequences from zero in generator order, and do not use
generator metadata IDs that may contain labels. Store every float as decimal
text that round-trips to the same binary64 value plus reversible binary64 text
(prefer `float.hex`). Define same-time batches by production `_point_batches`
semantics: convert timestamps to `float`, reject decreasing numeric timestamps,
group consecutive points whose converted timestamps compare numerically equal
(including `+0.0 == -0.0`), assign batch ordinals in first-seen order, and
preserve within-batch point order. Construct the fixture audit `x+y` once with production-declared
`float(x) + float(y)`. The canonical UTF-8 JSON/SHA-256 binds **only** ordered
seed/sequence/stream/point/batch identities and exact raw `x/y/t` bits;
exclude the audit `x+y`, neural results, events, and condition outcomes. A
separate audit digest may bind the canonical fixture identity to ordered audit
`x+y` bits, but it is not canonical identity. The runner loads raw values from
reversible `float.hex` representations (checking decimal round-trip) and must
never call the spiral generator. Exclude labels and evaluation metadata.
For each point in every condition and replay, independently execute the
production-declared `float(x) + float(y)`, retain that run's exact derived value
as decimal plus `float.hex` with point/arm/replay identity, and feed it to the
runtime; do not feed the fixture audit value. Compare each run's derived `x+y`
separately against the fixture audit value using
`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`; record
observed, expected, residual, and bound per point/run. This is distinct from
exact raw `x/y/t` identity and is not inferred from Luna-43's mismatch.

Use fixed `source -> relay -> destination` topology with ordinary Model-B
`w=1`, delay `1` edges; source integration is `None`, destination integration
is disabled in every arm, and relay integration is disabled, default
(`decay_rate_z=0.1`), or calibrated (`decay_rate_z=0.0125`). The endpoint is
relay propagation: require integration-mediated relay canonical emissions to
reconcile to actual ordinary `relay -> destination` onward transfers, with at
least one causally matched onward transfer to meet the endpoint. No historical
count is required; the destination is only a passive disabled receiver, with no
destination integration or state/emission endpoint; capture it only to verify
that onward transfers arrive.

Record authorization revision/handoff digest, fixture-generation
revision/fixture digest, runner revision/file hash, execution revision and
execution/artifact digests, plus config/run/replay provenance. The numerical policy is predeclared by quantity: fixture/raw-input identity and
discrete behavior remain exact; per-run `x+y`, source-emission payload, each
edge's Model-B payload, each relay recurrence field, and each derived
onward-arrival timestamp are separately reported using
`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`.
Elapsed-time deltas are exact timestamp subtraction. Hard bounds, event
classifications, within-run payload copies, strict-future causality, and
same-environment replay remain exact. The policy is not inferred from Luna-43's
historical mismatch.

Starting revision: `a79494cd66be28fd291ed11eddd62d342f457cfd`. The owner reports
`git fetch origin main` returned this as `FETCH_HEAD`; this shallow checkout has
no `origin/main` ref, so synchronized-main status is not claimed. Luna-44 must
verify and record the published authorization revision
`ff4bf51dcaab2e7b66f0409f4d63a33649c3e104`. No code, tests, agent profile,
experiment, or scientific result is included in this governance update. No destination-integration variation,
destination-state/emission analysis, tuning, efficacy, WEMA, or Luna-45 is
authorized. Preserve Luna-42 **PASS WITH FOLLOW-UP** and Luna-43 **BLOCKED /
DESTINATION COMPARISON UNDETERMINED**. ACP-0007 remains disabled/unchanged;
ACP-0008 remains opt-in/unpromoted. Full scope and provenance:
`workflow/handoffs/luna-0-authorization-luna44-canonical-fixture-rebaseline-20261005.md`.

## Luna-0 independent post-Luna-43 review — destination integration

**SCIENTIFIC RESULT BLOCKED / DESTINATION COMPARISON UNDETERMINED; EXECUTION
PROTOCOL AND CONTRACT PASS WITH FOLLOW-UP.** Independently reviewed the clean
published result `32898e3b50daf0834c6ddb8889dd5127f7fb489d`, the authorized
contract, committed runner/tests, raw Luna-43 artifacts, raw Luna-42 calibrated
records, and relevant runtime/topology code. The exact historical input gate
stopped at `DESTINATION_DISABLED`, seed 0, sequence 0 (`c00-000`): the 12-batch
stream digest differed due to one value at batch 3 / point 0
(`-0.1646535199398629` versus `-0.16465351993986282`, 3 ULP). All other
historical checks on that completed record passed. The runner did not execute
another character or destination condition; no condition-complete destination
trace, full replay, or destination scientific verdict exists.

Independently recalculated all four file hashes, internal artifact/configuration
digests, and aggregate digest. Replayed the exact committed runner in a
disposable detached worktree using the committed Luna-42 source artifact; its
four output files matched retained artifacts byte-for-byte. The retained replay
record correctly says whole-run replay was not run after the blocker, with null
digests. The environment pair is Luna-42 Windows/Python 3.11.5 versus Luna-43
Linux/Python 3.12.3; the specific cause of the binary64 difference is unknown.
The predeclared exact identity gate remains intact.

The only destination equation status is **not applicable**: this retained
first character has no destination reception. No conclusion about destination
emissions, integration, efficacy, or a negative mechanism result follows.
Reran Luna-43 focused tests (4 passed), the ACP-0008/runtime/routing selection
(217 passed, the same four nominal-0.4 exact-float failures as baseline), and
the full suite (1023 passed, the same four failures, 1 CUDA-unavailable skip).
No new or unrelated test failure was found.

Return the source-stream comparability question to the project owner. This is
not a production/API correction or automatic successor; **no Luna-44 is
authorized**. A01-A15 and ACP-0007 remain unchanged; ACP-0008 remains
experimental, opt-in, and unpromoted. Historical Luna-42 remains **PASS WITH
FOLLOW-UP**, Luna-41 **BLOCKED**, Luna-40 **NOT SUPPORTED IN THIS SETUP**,
Luna-39 **PASS WITH FOLLOW-UP**, Luna-37 **NOT SUPPORTED IN THIS SETUP**, and
Luna-34 **BLOCKED / UNDETERMINED**. Full evidence and commands:
`workflow/handoffs/luna-0-independent-review-luna43-acp0008-destination-integration-20261005.md`.

## Luna-0 owner-directed authorization — Luna-43 destination integration mechanism

**Luna-43 AUTHORIZED / NOT EXECUTED.** The current project-owner direction
supersedes the post-Luna-42 review's then-current "no Luna-43 authorized"
disposition and the mistakenly published test-only assignment. Luna-43 may
run only the bounded mechanism comparison with the relay fixed at ACP-0008
`decay_rate_z=0.0125` and destination integration disabled/default/calibrated.
Use only the fixed `source -> relay -> destination` topology, ordinary `w=1`
on both hops, no shortcut, ACP-0007 growth disabled, and all remaining
parameters/streams/bounds frozen as reviewed. No task efficacy, promotion, or
hardware claim is authorized; ACP-0008 remains experimental, opt-in, and
unpromoted; ACP-0007 is unchanged. The full baseline was 1019 passed, 4 known
Luna-41/Luna-42 nominal-float assertion failures, and 1 CUDA-unavailable skip;
the focused ACP-0008/runtime/routing selection was 217 passed with only those
same 4 failures. No unrelated failure was observed. Do not execute the
superseded test-only assignment. Full authorization and baseline evidence:
`workflow/handoffs/luna-0-authorization-luna43-destination-integration-20261005.md`;
executor contract: `.github/agents/luna-43.agent.md`. No Luna-43 experiment was
run in this authorization pass.

## Luna-0 independent post-Luna-42 review — ACP-0008 calibration

**PASS WITH FOLLOW-UP — corrected calibration and frozen fixed-topology
mechanism result independently reproduced; no Luna-43 authorized.** Reviewed
the final Luna-42 publication at
`3af1c1bcc0f4a0121752103211aa702fc6a6e85a` from clean synchronized `main`.
The non-null recorded execution revision is
`d073ecc13e789105c611181992ce4c8d48c79030`; the preceding Phase-B fix only
initializes arm-keyed paired-input digests and adds a regression test. It
does not change scientific stimuli, parameters, topology, or criteria.

Independent digest reconstruction, 68-step Phase-A recurrence reconstruction,
and Phase-A/Phase-B replay reproduce the retained evidence. The exact
predeclared candidate set and selection rule select `decay_rate_z=0.0125`;
the other candidates fail the near-triple integration fixture. In the
fixed-`w=1` Phase-B topology, the calibrated arm has 235 integration-mediated
relay emissions and matching ordinary onward routes/receptions; default and
disabled controls have none, with paired source streams. There are no
destination emissions. The only 235 within-character ordered emitter pairs
inside the ACP-0007 window are `source -> relay` pairs across the existing
edge; no missing-edge opportunity is evidenced. This supports neither
structural growth nor task efficacy, optimality, energy benefit, ACP
promotion, or hardware equivalence.

Two auxiliary test assertions retain `abs_tol=1e-12`, although runner
acceptance and artifact comparisons use the declared
`64 * sys.float_info.epsilon * max(1, |a|, |b|)` rule. These test-only checks
do not feed scientific selection or artifact generation; record as a
non-blocking test-policy follow-up without changing the reviewed Luna-42
run. The full suite is 1023 passed, 1 CUDA-unavailable skip, 1024 collected
(baseline: 1015 passed, 1 skipped, 1016 collected). Full review evidence:
`workflow/handoffs/luna-0-independent-review-luna42-acp0008-corrective-calibration-20261005.md`.

ACP-0008 remains experimental/opt-in/unpromoted; ACP-0007 is unchanged and
was disabled. Luna-41 remains historically **BLOCKED**. No Luna-43,
additional calibration search, WEMA, structural growth/pruning, efficacy,
or promotion is authorized.

## Luna-0 corrective decision — ACP-0008 fixture/provenance; Luna-42 AUTHORIZED / NOT EXECUTED

**CALIBRATION RESULT UNRESOLVED DUE TO FIXTURE SPECIFICATION / PROVENANCE
DEFECT. Luna-41 remains BLOCKED; this is not a demonstrated ACP-0008
mechanism failure. Luna-42 is AUTHORIZED / NOT EXECUTED.** Starting revision
verified clean
and synchronized: `0ebb59c4fa61c5f2aad6ffa09341de1b342745bf`. Luna-41's
repeated near-spaced source events routed `0.4000008889685561` and
`0.4000008889707768` rather than the contract's literal `0.4`; its
`1e-12` tolerance was undocumented, and its `results.json` omitted
`execution_revision`. Mechanics were reproduced accurately and the analytic
threshold prediction was partly confirmed, but no candidate validly passed
Phase A. Phase B correctly did not run.

The bounded corrective successor changes only the fixture/provenance and
formal numerical-comparison contract. It uses the same source external
stimulus/configuration and original timing, routes via the existing
production `source -> relay` `w=1` path, records the actual payload, and
uses that value in the recurrence oracle. It neither injects an idealized
`0.4` nor encodes an observed route value as a constant. Exact discrete
criteria remain exact; independent floating-equation checks use
`64 * sys.float_info.epsilon * max(1, |a|, |b|)`, predeclared as a
conservative binary64 operation-rounding allowance. Every artifact must
carry a non-null execution revision, runner hash, config digest, artifact
digest and replay identity; missing provenance blocks the claim. Candidate
set (`0.1, 0.05, 0.025, 0.0125`), fastest-decay-passing rule, thresholds,
near/far times, ACP-0008 equations and bounds remain unchanged. ACP-0007
remains unchanged and disabled. ACP-0008 remains experimental/opt-in/
unpromoted. WEMA is an unresolved alternative idea only; no implementation
or experiment is authorized. No efficacy, optimality, promotion or hardware
claim is authorized. Full decision and contract:
`workflow/handoffs/luna-0-acp0008-corrective-calibration-decision-20261005.md`;
executor:
`.github/agents/luna-42.agent.md`.

## Luna-0 independent post-Luna-41 review — ACP-0008 temporal calibration

**BLOCKED at the Phase-A normalized-routed-payload gate; bounded execution
and Phase-B gate PASS WITH PROVENANCE CAVEAT; no candidate selected; Phase B
NOT RUN.** Reviewed Luna-41 ending
revision `e8639fc2563862b9d35bb7d9c951c59e137c12d0` from a clean synchronized
`main`. The committed runner tested exactly the four authorized
`decay_rate_z` values and held all other ACP-0008 parameters fixed with
ACP-0007 disabled. Independent equation reconstruction matched all 68
enabled integration-trace steps within `1.271e-21`; independent Phase-A
replays matched the retained digest. Only `0.0125` produced the predicted
positive and negative near-triple integrated relay emissions, and all
isolated/far controls were silent. However, repeated near-spaced source
emissions routed `0.4000008889685561` and `0.4000008889707768` instead of the
declared `0.4`, exceeding the runner's `1e-12` tolerance. Since the contract
requires stopping when source routes fail to deliver the declared payload,
no candidate validly passes. The analytic threshold-crossing prediction is
partly confirmed, not a calibration result. Phase B and multi-hop onward
routing were not tested. The review verdict is BLOCKED, not a valid
calibration success or a valid no-relay negative finding under normalized
repeated inputs. ACP-0008 remains experimental/opt-in/unpromoted; historical
Luna-40 and prior results are unchanged. No Luna-42, retuning, tolerance
change, WEMA, or ACP-0007 diagnostic is authorized. Return the fixture
amplitude/tolerance issue to the project owner. `results.json` omits its
execution revision, although the enclosing commit and independent replay
identify/reproduce the committed source:
`workflow/handoffs/luna-0-independent-review-luna41-acp0008-temporal-calibration-20261005.md`.

## Luna-0 owner-directed calibration decision — ACP-0008; Luna-41 AUTHORIZED / NOT EXECUTED

**A task-independent, bounded calibration is specified; Luna-41 is
AUTHORIZED / NOT EXECUTED.** This decision follows Luna-40's independently
reviewed **NOT SUPPORTED IN THIS SETUP** result, in which no relay emission
or ACP-0007 candidate/admission formed. That negative result remains intact
and does not establish a production defect or predict calibration success.

Luna-41 may vary only `decay_rate_z` over the four predeclared values
`0.1, 0.05, 0.025, 0.0125`, keeping `theta_E=1`, `theta_Z=1`,
`input_gain=1`, `z_max=4`, fast decay `1`, and ACP-0007 disabled. Its
normalized Phase-A fixtures require a single `0.4` input and two inputs at
12.9 local-time spacing to remain subthreshold, three near inputs to yield
exactly one integration-mediated relay emission, three inputs at the fixed
far interval `51.6` to remain subthreshold, a sign-mirrored result, a
disabled control, bounded/equation-consistent state, neutral return, and
deterministic replay. Candidate choice is by the predeclared fastest-decay
passing rule; no candidate expansion or task-based fitting is permitted.
The `0.4` amplitude and timing anchor derive from normalized ACP-0008
fixtures and previously reviewed local routed-arrival evidence, not Phase-B
task success. These are planned criteria and analytic predictions, not
observed experiment results.

Only after Phase-A results and configuration are frozen may Phase B
characterize identical unlabeled point streams through paired calibrated,
default, and disabled relay arms over the unchanged fixed-`w=1` topology.
No efficacy, accuracy, growth, promotion, or hardware claim is authorized;
zero relay emissions is a valid outcome. No production code, ACP-0007,
ACP-0008 equations, thresholds, topology, or Architecture Contract change
is authorized. ACP-0008 remains experimental, opt-in, and unpromoted. Full
authorization, fixtures, stop rules, bounds, and ownership:
`.github/agents/luna-41.agent.md` and
`workflow/handoffs/luna-0-acp0008-calibration-decision-20261005.md`.

## Luna-0 independent post-Luna-40 review — Existing structural growth and effective routed drive

**NOT SUPPORTED IN THIS SETUP; EXECUTION CONTRACT PASS; NO PRODUCTION
DEFECT; NO LUNA-41 AUTHORIZED.** Reviewed the completed bounded Luna-40 run
at `ebff91176c02e29e3b9aad38308fc95d0b773817`, with its authorized start
revision `a39dd335e7af1b18a8d28ef3faf7b975304132df`. The five-seed, four-arm
artifact contains 1,280 character runs: every arm has 1,715 source emissions
and source-to-relay transfers, but no relay or destination emissions,
source/destination temporal pair, candidate, growth attempt, admission,
destination reception, or `z` update. Independently reconstructed all
per-arm totals, route/event/payload provenance, control equality, bounds,
and the full replay digest
`f5c7f4d8fbc2037c43ac1118e96e6a2a23e4f0241da78cd7bea99a226b730211`.
Focused tests: 11 passed; full suite: 1009 passed, 1 skipped (CUDA
unavailable; 1010 collected, 11 more than the prior 999). At review
resumption, `HEAD == origin/main`; the only worktree changes were the
unpublished Luna-0 review draft from the preceding turn, with no unrelated
or experiment changes. The result is specifically **NO LEGAL EDGE ADMISSION**;
because no shortcut was admitted or used, it does not test post-admission
effective drive. It does not imply a production defect or generalize beyond
the frozen fixture. ACP-0008 remains experimental/opt-in and unpromoted;
Luna-33/34/37/38/39 and ACP-0007 verdicts are unchanged. No follow-up is
authorized. Full review and limitations:
`workflow/handoffs/luna-0-independent-review-luna40-effective-routed-drive-20261005.md`.

**Architecture question:** Existing structural plasticity did not supply the
routed-drive mechanism Luna-39 showed ACP-0008 could use in this fixture,
because no legal candidate formed. The run was not blocked by API
composition, and it does not test whether admitted convergent paths could
substitute for Luna-39's `w=2` sensitivity. The declared stream's failure to
produce relay emissions is returned to the project owner; it does not
authorize tuning or a successor Luna.

## Luna-0 owner-directed audit — existing routed-strength mechanisms; Luna-40 AUTHORIZED / NOT EXECUTED

**The only accepted endogenous routed-strength mechanism identified is
optional ACP-0007 E2 local structural growth, which can add bounded
convergent edges at fixed Model-B parameters; edge weights themselves are
not learnable.** Luna-39's independently reviewed result remains
**PASS WITH FOLLOW-UP**: ACP-0008 integration at `w=1` accumulated to
`max |z|=0.763164` without destination emissions; the predeclared `w=2`
sensitivity produced 31 trace-verified integration-mediated emissions on
27/320 characters and zero direct emissions. ACP-0008 remains experimental
and opt-in, with no promotion or efficacy claim.

The audit verified a clean synchronized baseline at
`6ae253dd53b2b7a9ba1589c10035690a5b65e416`. Existing reward/eligibility
updates local credit, not edge parameters. ACP-0007 structural growth uses
actual source-local canonical-emission timing evidence, mutates only after
quiescent character completion, and inserts default `w=1`, `d=1`, `r=0`
edges under finite deterministic bounds. Prior Luna-12I/Luna-28 evidence
supports mechanism validity and legal fan-in, not efficacy or present
ACP-0008 bridge success.

Luna-40 is authorized only to characterize whether that existing local
growth mechanism can generate effective convergent routed drive under a
predeclared ACP-0008 configuration and matched frozen controls. It may not
learn weights, tune parameters, modify production code, evaluate accuracy,
prune, or promote ACP-0008. **Luna-40 is AUTHORIZED / NOT EXECUTED.** See
`.github/agents/luna-40.agent.md` and
`workflow/handoffs/luna-0-authorization-luna40-effective-routed-drive-20261005.md`.
All prior Luna verdicts and historical no-authorization records remain
unchanged.

## Luna-0 independent review — Luna-39 ACP-0008 propagation-to-emission diagnostic
**PASS WITH FOLLOW-UP; BOUNDED MECHANISTIC BRIDGE SUPPORTED ONLY UNDER STATIC N2 SENSITIVITY.** Reviewed `a185c6321b06f58df2bd7b22c56b1d23cb7d67e5`, starting from clean synchronized `main`. The 1,920-execution Luna-39 run passes historical reproduction: all 960 legacy-arm records exactly match Luna-37; source streams are invariant across arms. Independently reconstructed all six aggregate cells, 3,430 integration traces and 3,840 ledger-capacity records. Under ACP-0008, `w=1` accumulates (`max |z|=0.763164`) but produces zero destination emissions; the predeclared `w=2` sensitivity produces 31 integration-mediated canonical emissions on 27/320 characters. There are zero direct emissions. Capacity remains 1024 per ledger, peak occupancy 19; equations reconcile. Independent full rerun reproduced digest `5a19be65e2386e585eb50877c80f3114ee7383fda7b2a8324642440618b963d6`. Focused 227 passed; full suite 998 passed, 1 skipped (CUDA unavailable), 999 collected. ACP-0008 remains experimental/opt-in; no promotion, efficacy or ACP-0007 claim. Luna-37 remains historically NOT SUPPORTED IN THIS SETUP; Luna-34 remains BLOCKED / UNDETERMINED; Luna-33/ACP-0007 unchanged. A possible natural/learned-strength follow-up requires project-owner direction; no Luna-40 created or authorized. See `workflow/handoffs/luna-0-independent-review-luna39-acp0008-propagation-emission-20261005.md`.

## Luna-0 independent review — Luna-38 ACP-0008 temporal-integration state
**PASS WITH FOLLOW-UP; ACP-0008 IMPLEMENTED AS SPECIFIED; NO PRODUCTION DEFECT; LUNA-39 AUTHORIZED / NOT EXECUTED.** Reviewed Luna-38 at `58ad0868bdbf907ed9d40aeee4f39fe1e5740e8f`. Only contract-owned files changed (neuron module, two IR-2/TPCV guards, 38 new tests, fixture artifact, handoff); disabled mode is the unchanged legacy path. Independently reconstructed: closed-form `z` oracle matches; fixture B emits once at 6.5 after discharge; spacing 2 emits while 10 and 40 do not (same amplitude); K (`theta_e=1.5`) adds no emission and is a timestamp subset of default; L (`theta_e=0.5`) emits an isolated 0.6 directly (`z=0`, no discharge) while the 0.4 stream emits only via a `theta_Z` discharge after four integrated inputs; neutral attractor, boundedness, determinism and `theta_E` configurability (no hard-coded emission constant, no `theta_I`) verified. Validation: 316 focused, full suite 990 passed, 1 skipped, 991 collected (952 + 38). Follow-ups: integration-enabled neurons are not IR-2/TPCV representable, `IntegrationConfig` not package-exported, fixture I uses a private `_z` poke, parameters uncalibrated. ACP-0008 stays ACCEPTED (EXPERIMENTAL, OPT-IN); no promotion into the Architecture Contract. Luna-39 is authorized only as a mechanism-only rerun of the Luna-37 two-node fixture with the destination neuron integration-enabled at default `theta_E=1` and a built-in integration-disabled reproduction arm; no sweeps, efficacy, growth or Luna-40. Luna-37 stays NOT SUPPORTED IN THIS SETUP (previous architecture); Luna-34 BLOCKED / UNDETERMINED; Luna-33 and ACP-0007 unchanged. See `workflow/handoffs/luna-0-independent-review-luna38-acp0008-temporal-integration-20261005.md` and `.github/agents/luna-39.agent.md`.

## Luna-0 owner decision — ACP-0008 slow temporal-integration state
**ACP-0008 ACCEPTED (EXPERIMENTAL, OPT-IN); LUNA-38 AUTHORIZED / NOT EXECUTED.** Following the post-Luna-37 result (no destination emissions; sub-threshold state plus fast decay, gaps of at least 12.9), the project owner approved a distinct slower integration state `z` in the excursion neuron, default disabled, with subtractive discharge into the unchanged ordinary emission path and the E2 `M` regime untouched (`z`-driven oscillator staged out). Luna-38 implements and verifies only this on unit fixtures A-D, F-I with a temporal-selectivity comparison (spacing 2, 10, 40); it must return BLOCKED if it needs changes to reward, prediction-error, ACP-0007, structural growth, eligibility lifetime, event ordering, a global timestep or unbounded same-time generation. No efficacy, Luna-37 rescue, calibration or contract promotion is authorized. Luna-37 stays NOT SUPPORTED IN THIS SETUP; Luna-33/34 and ACP-0007 unchanged. Owner amendment: canonical threshold `theta_E` stays an explicit per-neuron config parameter (already `E1Config.theta_e`, default 1, fixed per execution, no `theta_I`); Luna-38 adds threshold-causality fixtures J-L (three predeclared values, no sweep) and no threshold learning, homeostasis or tuning. See `workflow/docs/architecture_proposals/ACP-0008.md`, `workflow/handoffs/luna-0-owner-decision-acp0008-temporal-integration-20261005.md` and `.github/agents/luna-38.agent.md`.

## Luna-0 independent review — Luna-37 propagation-to-emission diagnostic

**NOT SUPPORTED IN THIS SETUP; CONTRACT PASS; NO PRODUCTION DEFECT; NO LUNA-38 AUTHORIZED.** Reviewed Luna-37 at `295309866c367cfeda7e42b4a42a47e813dd88ec`. 960 executions (seeds 0–4, three conditions, `eligibility_capacity=1024`, peak occupancy 19, no capacity errors). Routing occurred (1715 transfers per edge condition, depth 1) but downstream canonical emissions were 0 in all conditions; the no-edge control is a valid negative control. Maximum post-transfer destination state was 0.6855 (w=1) and 0.9327 (w=2), below `theta_E=1`, with no accumulation (gaps ≥12.9 vs decay 1.0). Replay digest independently reproduced. Full 952 passed, 1 skipped, 953 collected (+7). The bootstrap-gap classification is strengthened and refined; Luna-33 verdict, Luna-34 (BLOCKED / UNDETERMINED) and ACP-0007 are unchanged. Further direction requires a project-owner decision. See `workflow/handoffs/luna-0-independent-review-luna37-propagation-emission-diagnostic-20261004.md`.

## Luna-0 independent review — Luna-36 eligibility capacity API

**PASS — PUBLIC-API BLOCKER RESOLVED; NO PRODUCTION DEFECT; LUNA-37 AUTHORIZED / NOT EXECUTED.** Reviewed Luna-36 at `8f8824a185a2b1ebc3fd74cbd29eef8d75cbd818` (clean, `HEAD == origin/main`). Only the three owned files changed. The optional keyword-only per-ledger `eligibility_capacity` defaults to the unchanged legacy `prediction_capacity * max(1, nodes)` (16 for the two-node, `prediction_capacity=8` fixture); an explicit 1024 yields 1024 per ledger; a deliberately small capacity still raises `EligibilityCapacityError`. Focused: 90 passed. Full: 945 passed, 1 skipped (CUDA), 946 collected; +13 from Luna-36 tests. Lifecycle, predictor, reward and delayed-credit semantics are unchanged. Luna-34 remains historically **BLOCKED / UNDETERMINED**; Luna-33 and ACP-0007 are unchanged.

Luna-37 is authorized only as a clean mechanism-only successor to Luna-34 (no-edge, default static edge, single `|w|=2` condition) with predeclared `eligibility_capacity=1024` derived from the per-character event budget. No efficacy, growth, pruning, architecture change or Luna-38 is authorized. See `.github/agents/luna-37.agent.md` and `workflow/handoffs/luna-0-independent-review-luna36-eligibility-capacity-api-20261004.md`.

## Luna-0 independent review — Luna-35 eligibility capacity/lifecycle

**PASS — LUNA-35 EVIDENCE INDEPENDENTLY RECONSTRUCTED; NO PRODUCTION
LIFECYCLE DEFECT ESTABLISHED; LUNA-36 AUTHORIZED / NOT EXECUTED.** Review
started from clean synchronized `main` at
`b0507cb68776011dba482907b0ac763bec2a225f`. The fixed 20-point no-edge
`c00-004` fixture independently reconciles 16 successful source eligibility
creations, zero removals, peak/final occupancy `16/16`, and rejection of
`source:excursion:17` at `255.79833294576443`. All 16 linked predictors
expired while their eligibility entries remained resident; no reward or
prediction-error signal reached that ledger before the overflow. In the
one-point control, a matched neutral reward at time 4.0 updated/decayed the
entry but did not remove it. Character destruction released the runtime's
ledger references, and the next character received fresh empty ledgers.
The full independent reconstruction and validation are in
`workflow/handoffs/luna-0-independent-review-luna35-eligibility-capacity-20261004.md`.

The capacity overflow is **EXPECTED BOUNDED BEHAVIOR**; the independent
eligibility-capacity configuration gap is a **CONTRACT AMBIGUITY / PUBLIC API
LIMITATION**. Predictor expiration is not an eligibility-retirement event,
and retention supports delayed credit after predictor expiry. Luna-34 remains
historically **BLOCKED / UNDETERMINED**; the propagation-to-emission
hypothesis was not rerun or answered. Luna-33 and ACP-0007 are unchanged.
Luna-36 is authorized only for an optional finite per-ledger capacity setting
whose omitted default exactly preserves current behavior. No lifecycle,
predictor, reward, or architecture semantics change and no experiment rerun
is authorized. See `.github/agents/luna-36.agent.md`.

## Luna-0 independent review — Luna-34 eligibility-capacity blocker

Luna-34's reported eligibility overflow was independently reproduced at
`4d77489eaebadf638f22996d1d0d49e162b378ab`: seed 0,
`NO_EDGE_CONTROL`, sequence index 4 (`c00-004`), source emission 17 with
16 resident traces in a 16-entry per-ledger capacity. The prior 16 linked
predictor records had expired, but the runtime's eligibility ledgers have no
configured expiry and retain entries until the character lifecycle ends.
The overflow exception is consistent with the existing deterministic bounded
overflow behavior; whether this retention/capacity relationship is intended
for the complete workload is not established, and no production defect is
claimed. Luna-34 remains **BLOCKED** and its propagation-to-emission
hypothesis **UNDETERMINED**. A bounded lifecycle-only diagnostic is
**AUTHORIZED / NOT EXECUTED** as Luna-35 under
`.github/agents/luna-35.agent.md`. It may not retry the propagation
experiment, change capacity/expiry, or modify production behavior. At that
post-Luna-34 point, no Luna-36 was authorized; that historical status is
superseded by the post-Luna-35 review above. Full review:
`workflow/handoffs/luna-0-independent-review-luna34-eligibility-capacity-20261004.md`.

## ACP-0003 heterogeneous execution review

ACP-0003 is accepted for staged implementation as an architecture-governance
proposal for separating canonical TPCN semantics from GPU, FPGA and FPAA
realization contracts. The selected equal-time policy is Model C: strict
serialized mode is a validation path, while coincident FPAA integration is a
declared approximation under Model B semantics. Luna-18 is authorized only for
the H1 hardware-neutral execution IR/backend interface skeleton. The proposed
order is canonical/reference behavior, H1 IR, GPU native reference, GPU FPGA
approximation, GPU FPAA approximation, and only then device-specific
implementation. ACP-0002 N2 remains closed and authoritative;
ACP-0002 N3 and later stages remain unauthorized, Luna-13F remains closed and
Luna-13G remains unauthorized.

ACP-0004, **Attractor Excursion and Event-Compression Neuron**, is accepted for
staged implementation. The canonical output term is **excursion**:
GPU/software and FPGA reference semantics use exactly one digital event per
excursion, while FPAA may provide a physical spike/analog excursion under a
later approximation contract. Luna-19 is authorized only for E1, the static
leaky accumulator and single-excursion reference; it must not implement M,
learning, IR-2, backends, approximation or H2. ACP-0002 N3, ACP-0003 H2,
Luna-13F reopening and Luna-13G remain unauthorized.

ACP-0005 authorizes the next schema dependency: TPCN-IR-2 may represent
excursion-aware transferable E1 state and future M state, but does not execute
M. Luna-20 implementation and the independent Luna-0 closure are complete.
The final Luna-0 E2/M dispatch review clarified final residual identity and
provenance ownership, reset semantics during M, and the separate E2-capable
IR-2 reconstruction boundary. Luna-21 implementation was published at
`bfc866be053f9692382d1be5e048f5b4d280e5f6`, with its completion handoff at
`5d0171f46b90664b1a6aca5709cc2f07f19b7f4e`. The initial independent review
at `a9077997740ccdc374c7ad89deef122112967369` was
**BLOCKED — IR-2 RECONSTRUCTION DEFECT**: validated S-state records could
have identity high-water counters behind active IDs or counters beyond the
event budget, allowing episode identity reuse. Its bounded correction gate
and evidence remain in
`workflow/handoffs/luna-0-independent-review-ACP-0004-E2-Luna-21-20261003.md`.
The authorized correction was implemented at
`ac2e822e5c7656d649c6e77f62024c6d6e4cf72f`; its handoff was published at
`3fb6d8c5128277bc8ecc5b2beea7288c214b772d`.
Luna-21's bounded IR-2 correction was independently reviewed and closed at
the review publication recorded in
`workflow/handoffs/luna-0-independent-corrective-review-ACP-0004-E2-Luna-21-20261003.md`.
The review independently reproduced the prior blockers on the pre-correction
revision, verified corrected validation and continuation, and repaired the
remaining vacuous unique-ID test oracle without changing production runtime
code. ACP-0004 remains staged; this closure is not architecture promotion or
integration readiness. ACP-0003 H2, ACP-0002 N3, backends, calibration and
hardware remain separately gated.

## Mission

Evolve TPCN into a hardware-realizable, event-driven predictive-coding network while preserving its core principles.

The immediate benchmark is sequential letter-stroke classification. Each stroke or stroke point is presented as subsequent temporal data rather than converting the complete character into a static image.

The workflow must support eventual:

## Future Luna Contract

Every newly created Luna must publish a bounded dispatch record before
implementation begins. The record is normative for the workflow and must use
the handoff template.

### Required identity and classification

Declare the Luna identifier, descriptive name, task ID, baseline repository
revision, dependencies, owner and exact owned files/components. Classify the
work as one or more of `OBSERVATION`, `VERIFICATION`, `EXPERIMENT`,
`INTEGRATION`, `IMPLEMENTATION`, `ARCHITECTURE-PROMOTION` and `HARDWARE`.
Classification controls scope: an experiment does not amend the canonical
architecture; verification should not repair unrelated production behavior;
architecture promotion requires explicit Luna-0/project-owner approval and the
ACP process.

### Required hypothesis, invariants and scope

An experimental Luna must state a falsifiable hypothesis and the result that
would count against it. It must list clauses touched and preserved, interfaces,
label/information boundaries, resource bounds, timing assumptions and reset
boundaries. It must state authorized files/components and production-code
authority, plus relevant explicit exclusions such as labels, global learning,
unbounded topology, hardware acceptance, real-data claims, classifier redesign
or unrelated refactoring.

### Required controls and evidence

Controls and comparison conditions must be declared before implementation.
Metrics must be declared before running the experiment, including negative
results and failed seeds. Record baseline revision, seeds, configuration,
workload/dataset version, commands and environment where applicable. Every
mechanism must account for finite state, events, queues, fan-in, fan-out,
edges, candidate lists, history/eligibility, lineage/path depth, memory and
hardware representation. Do not add an effectively unbounded structure to the
canonical path without architecture review.

### Required boundary and verification checks

State whether each information source is available to a physical local
component; global evaluation/orchestration may remain outside canonical neural
computation. For canonical mechanisms, describe eventual FPGA, FPAA or hybrid
mapping and identify software-only conveniences. The completion record must
separate passed, failed, not-run and not-applicable results and include focused
tests, relevant prior-Luna regressions, full regression where applicable,
compile/static validation, diagnostics and `git diff --check`.

### Promotion and handoff boundary

Experimental success does not change the architecture. Promotion requires
completed evidence, Luna-0 review, explicit owner decision where required, an
ACP for material contract changes, synchronized contract/changelog revisions,
and updated acceptance criteria. Every Luna leaves a machine-readable and
human-readable handoff distinguishing `OBSERVED`, `INFERRED` and
`HYPOTHESIZED`, with changes, unchanged behavior, measurements, failures,
uncertainty, gate decision and authorized next work.

# 4. Luna-1 — Event Runtime

## Goal

Create the hardware-neutral event semantics.

Implement concepts equivalent to:

```text
Event
EventQueue
LocalTimestamp
PropagationDelay
EventType
EventPayload
```

Minimum event information:

```text
timestamp
source
destination
type
payload
```

Optional fields may later include:

```text
prediction_id
credit_id
operator
priority
energy_metadata
```

## Critical requirement

Execution batching is allowed.

For example, CUDA may process thousands of ready events simultaneously.

However:

\[
\text{execution batch}\neq\text{neural timestep}.
\]

Batching must preserve causal event ordering.

---

# 5. Luna-2 — Canonical Event Neuron

## Goal

Create the smallest useful TPCN neuron.

Initial neuron should contain:

```text
TPCNNeuron
    state
    local_time

    receive_event()
    advance_state(dt)

    prediction_state
    prediction_error

    eligibility_state

    energy_state

    emit_event()
```

Avoid prematurely implementing ten pathways.

Start with the minimum computational operator necessary to establish learning.

The interface must later permit multiple operators.

---

# 6. Luna-3 — Predictive Coding and Error Events

## Goal

Ensure the model remains a predictive-coding architecture.

Given event history:

\[
e_0,\ldots,e_t
\]

produce a prediction:

\[
\hat e_{t+1}.
\]

When the next event arrives:

\[
\epsilon_{t+1}
=
e_{t+1}-\hat e_{t+1}.
\]

Represent this error through the event system.

Investigate:

- local prediction,
- delayed prediction matching,
- prediction identifiers,
- error-event propagation,
- eligibility traces,
- temporal credit.

## Acceptance test

Changing a distant neuron must not instantaneously change another neuron's prediction/error state.

The effect must arrive causally through permitted connections.

---

# 7. Luna-4 — Bounded Connectivity

## Goal

Replace spatial-reservoir assumptions with a hardware-realizable graph.

Represent:

\[
G=(V,E)
\]

with constraints such as:

\[
|\mathcal N_i^{in}|\le D_{in}
\]

and

\[
|\mathcal N_i^{out}|\le D_{out}.
\]

Support optional physical coordinates for placement/routing.

Coordinates constrain possible connectivity but are not neural features unless an experiment explicitly makes them so.

## Prepare for hardware

Model concepts such as:

```text
node capacity
fan-in
fan-out
routing distance
propagation latency
connection cost
```

Do not simulate a continuous spatial field.

---

# 8. Luna-5 — Energy and Utility

## Goal

Build a hardware-neutral local energy API.

Software reference:

```text
LocalEnergyModel
    observe_activity()
    update(dt)
    energy
    activity
```

Track useful quantities such as:

```text
events received
events emitted
neuron activations
operator activations
state changes
connection activity
```

## FPGA model

Prepare for:

\[
C[n]
=
\operatorname{popcount}
(Q[n]\oplus Q[n-1]).
\]

A local hardware clock may measure this activity.

That clock is an energy-metering clock, not the TPCN clock.

## FPAA model

Prepare for tuned continuous approximations such as:

\[
\frac{d\hat E}{dt}
=
-\frac{\hat E}{\tau_E}
+
\sum_k \alpha_kA_k(t).
\]

## Utility

Measure both energy and usefulness.

Do not implement:

```text
lowest energy = best neuron
```

Instead investigate:

\[
U=R-\lambda E
\]

and

\[
U=\frac{R}{E+\epsilon}.
\]

High-energy computation should survive when sufficiently useful.

---

# 9. Luna-6 — Sequential Stroke Dataset

## Goal

Build the first benchmark.

Do not present completed letters as static images.

Encode handwriting as a temporal event stream.

Candidate event:

```text
StrokeEvent
    timestamp
    x
    y
    dx
    dy
    pen_state
    stroke_boundary
```

Start with the dataset's native representation wherever possible.

Avoid adding information unavailable in a real streaming system.

## Sequence

```text
START_CHARACTER

stroke event
stroke event
stroke event
...

END_CHARACTER
```

Only then evaluate final character classification for the primary benchmark.

Intermediate predictions may also be recorded.

---

# 10. Luna-7 — Classification Interface

## Goal

Provide classification without contaminating the core TPCN architecture.

Initial target:

```text
26 class outputs
A-Z
```

The classifier reads activity produced by the TPCN.

Do not give internal neurons direct access to the correct label.

Labels belong to the learning/reward mechanism.

Track confidence throughout the stroke sequence where useful:

\[
P(c\mid e_0,\ldots,e_t).
\]

This lets us measure how quickly the network recognizes a character.

---

# 11. Luna-8 — Credit and Reward

## Goal

Determine which computation was useful.

Maintain local eligibility:

\[
\frac{de_i}{dt}
=
-\frac{e_i}{\tau_e}.
\]

When delayed reward/error information arrives:

\[
\Delta R_i
\propto
e_i\Delta r_i.
\]

Extend this eventually to:

```text
neuron eligibility
connection eligibility
operator eligibility
event eligibility
```

The major research question is:

> Which expensive computations materially contributed to successful prediction/classification?

This agent should coordinate closely with Luna-5.

---

# 12. Luna-9 — Emergent Gating Experiments

Do not modify the core architecture solely to prove one gating hypothesis.

Maintain three experiments.

## Experiment A — Explicit gates

Reference historical TPCN:

\[
y_i=\sum_k g_{ik}F_k(x_i).
\]

## Experiment B — Event-only gating

No explicit learned pathway gates.

A computation happens because relevant events reach it.

## Experiment C — Utility-mediated computation

Operators compete based on local event state, historical usefulness and energy cost.

Candidate principle:

\[
P(\text{operator active})
=
f(\text{event},h_i,R_i,E_i).
\]

Compare all three.

Do not assume which wins.

---

# 13. Luna-10 — Structural Plasticity

## Goal

Allow topology to evolve without violating bounded hardware constraints.

Begin with connection-level plasticity.

Possible process:

```text
inactive/unproductive connection
        ↓
utility decreases
        ↓
candidate for pruning

useful missing relationship
        ↓
local evidence
        ↓
candidate connection
        ↓
hardware constraint check
        ↓
connection created
```

Later extend to:

- operator removal,
- operator creation,
- neuron-node allocation,
- neuron removal.

Never allow structural growth to create effectively unlimited connectivity.

---

# 14. Luna-11 — Verification Agent

Luna-11 does not design new architecture.
It attempts to break implementations.

Required tests include:

```text
test_no_global_neural_clock
test_event_causality
test_finite_propagation
test_fan_in_limit
test_fan_out_limit
test_no_global_state_leak
test_no_spatial_reservoir_dependency
test_idle_network_cost
test_delayed_prediction_error
test_delayed_credit
test_energy_accounting
test_high_cost_high_reward_survival
test_high_cost_low_reward_suppression
test_bounded_state
test_deterministic_seed
```

Also test that batching events produces behavior consistent with unbatched causal execution within defined numerical tolerances.

---

# Visualization / Observability Milestone Family

Visualization is not part of the canonical TPCN computational architecture. It is an observability and verification facility used to inspect structure formation and activity across CPU, GPU, simulation, and FPGA implementations.

The branch is strictly downstream and has no return path into the TPCN computational datapath:

```text
TPCN core
|
+--> diagnostic snapshot/trace interface
|
+--> CPU exporter / visualizer
+--> GPU exporter
+--> ModelSim hex/binary trace
+--> FPGA diagnostic stream
|
+--> VGA local visualization
+--> Ethernet host visualization
```

The snapshot/trace interface is observational only. Capture, transport, rendering, reset, and display timing must not become computational inputs, a global neural clock, or computational backpressure. Dropped or incomplete records must be explicit.

## Luna-12 — Visualization Contract and CPU Reference Exporter

**Authorization:** The owner-supplied Luna-11 software-reference gate is authoritative for this dispatch: adversarial suite 10 passed, focused reward/replay/bounded/label checks 5 passed, full regression 89 passed, compilation passed, diagnostics reported no errors, and `git diff --check` passed. The existing Luna-11 handoff remains historical evidence and is not rewritten or used to reopen Luna-11. Luna-0 authorizes Luna-12 as the next visualization milestone; existing Luna-9/Luna-10 boundaries are unchanged.

**Purpose:** Define a canonical diagnostic snapshot/event format and implement the first CPU reference export, parse, and minimal visualization path.

**Scope:** Define a compact deterministic binary or hexadecimal-friendly format suitable for CPU, GPU, ModelSim, and FPGA use; document versioning, layout, endianness, field widths, framing, reserved values, overflow behavior, deterministic ordering, and legitimate observable state; implement the CPU reference exporter/parser/visualizer; and add deterministic, malformed-input, version-mismatch, empty-state, boundedness, and capture-on/off invariance checks.

**Explicit non-goals:** Do not redesign neuron behavior, inject visualization events, mutate classifier/reward/topology/timestamp/queue state, or implement GPU, ModelSim, VGA, or Ethernet support beyond compatibility stubs required by the format.

**Expected handoff:** A stable canonical visualization format plus CPU reference exporter/parser that later implementations can target.

**Completion gate:** Record focused serialization, parser, boundedness, and non-interference evidence. Luna-13 and Luna-14 remain blocked until Luna-12 passes.

## Luna-12A — CPU Training Visualization Integration

**Authorization:** Luna-12 has passed its CPU reference/exporter gate. Luna-0 explicitly authorizes Luna-12A for the deterministic Luna-9 synthetic training/evaluation path only. This authorization does not select or authorize a real dataset benchmark, and it does not make Luna-12A a prerequisite for Luna-13 or Luna-14.

**Purpose:** Run bounded CPU-side TPCN training while capturing TPCV-1 snapshots so activity, represented state, connectivity, reward/utility behavior, and any validated structural changes can be inspected over time.

**Dependency shape:**

```text
Luna-12
|
+--> Luna-12A  CPU training + visualization integration
|
+--> Luna-13  GPU-compatible visualization
|
+--> Luna-14  ModelSim/FPGA visualization
```

Luna-13 and Luna-14 remain separate downstream branches. Neither depends on Luna-12A unless Luna-0 later records an explicit decision.

**Scope:** Integrate the Luna-9 deterministic synthetic workload with TPCV-1 capture; provide a configurable CPU runner for epochs and snapshot intervals; store and replay bounded snapshots through the Luna-12 parser; expose epoch/snapshot indices, neuron identity, active state, represented state or activation magnitude, connections, metrics, and topology evolution where available; and provide a lightweight viewer or deterministic replay/export path that a user can run from the command line.

Visualization is strictly downstream-only and non-semantic. Capture, serialization, replay, rendering, storage limits, viewer timing, and dropped/incomplete records must not influence event ordering, neuron updates, predictions, reward, eligibility, classifier behavior, topology decisions, queue behavior, timestamps, or training results. The same deterministic workload with visualization disabled, snapshots every epoch, and more frequent snapshots must produce identical predictions, metrics, replay digest, update/parameter counts, topology where applicable, reward/utility state, and final network state.

Use Luna-10 structural plasticity only when its existing public API can be consumed without architecture changes and bounded topology invariants remain enforced. Fixed topology is the valid default. If those conditions are not met, defer structural-plasticity visualization and report that limitation; do not redesign the topology or core interfaces under Luna-12A.

**Explicit non-goals:** Do not implement GPU or ModelSim/FPGA visualization, authorize real-dataset benchmarking, alter TPCV-1 semantics, add a visualization return path, or weaken any A01-A15 invariant. This milestone does not authorize Luna-13 or Luna-14 work.

**Expected handoff:** A reproducible CPU training/demo runner, bounded TPCV-1 snapshot capture and replay evidence, a minimal inspection path, non-interference results, deterministic replay tests, and an explicit structural-plasticity included/deferred decision.

**Completion gate:** CPU training runs through the current Luna-9 event-driven experiment path; snapshots decode and replay through Luna-12 tooling; malformed, missing, and over-limit captures fail clearly; visualization-on/off and snapshot-frequency comparisons match; deterministic snapshot sequences pass; relevant regression and compile checks pass; and no architecture invariant is weakened. Real-dataset benchmarking remains separately gated.

## Luna-12B — Persistent Topology and Structural Plasticity Visualization Integration

**Authorization:** Luna-12A has passed its stated completion gate on the deterministic Luna-9 synthetic path: full suite 130 passed, 1 skipped; focused Luna-12A tests 3 passed; compilation passed; diagnostics reported no errors; `git diff --check` passed; and a three-snapshot smoke run was saved and replayed deterministically. Luna-0 explicitly authorizes Luna-12B as the next CPU visualization/integration milestone. This authorization does not authorize real-dataset benchmarking, Luna-15, Luna-16, or Luna-17. Luna-13 and Luna-14 remain independently authorized from Luna-12 and do not depend on Luna-12B.

**Purpose:** Integrate a persistent bounded Luna-4 topology into the CPU experiment path so the validated Luna-10 structural-plasticity mechanism can operate across examples and epochs, and expose measured structure/function behavior through TPCV-1.

**Dependency shape:**

```text
Luna-12
|
+--> Luna-12A  CPU training + visualization integration
|      |
|      +--> Luna-12B  persistent topology + structural plasticity
|
+--> Luna-13  GPU-compatible visualization
|
+--> Luna-14  ModelSim/FPGA visualization
```

Luna-12B depends on the completed Luna-12A CPU capture/replay path and the public Luna-9/Luna-10 interfaces. It must not create a second topology model, redefine TPCN architecture, or become a prerequisite for Luna-13 or Luna-14.

**Scope:** Preserve topology across examples and epochs where adaptation requires it; use the existing bounded topology and Luna-10 mutation APIs; capture accepted additions, removals, rejected mutations and reasons, active edge count, fan-in/out utilization, bounded mutation history, and replay-visible topology deltas; and add fixed-topology/learning, structural-plasticity, and supported no/reduced-learning comparisons. Report activity coverage and structure/function metrics sufficient to distinguish active, adaptive, useful-static, changing-without-benefit, and inert outcomes using measurements rather than subjective labels.

The runner should follow repository CLI conventions and support an equivalent developer command to `python <runner>.py --epochs 20 --structural-plasticity --snapshot-every 1`. A completed run must report starting/ending connections, additions, removals, rejected mutations, active-neuron fraction, prediction loss, accuracy, reward, energy, and utility before/after. Zero mutations are not automatically a failure; interpret them with behavior, reward, utility, event activity, and activation coverage.

TPCV remains downstream-only. Replay may distinguish unchanged, added, and recently removed connections from history, active/inactive neurons, snapshot/epoch index, and structural/behavioral metrics, but capture and viewing must not approve, trigger, or alter mutations, event ordering, routing, reward, classifier behavior, training, or backpressure.

**Required evidence:** Same-seed mutation sequences, final topology, snapshot sequences, and functional results reproduce where the underlying contracts guarantee determinism; capture-on/off results match; fan-in/out, finite propagation, bounded state/history, failed admission, pruning, routing validity, and non-interference checks pass. Record all beneficial and harmful outcomes and explicitly report topology/behavior combinations: unchanged/unchanged, unchanged/improved, changed/unchanged, changed/improved, and changed/degraded where observed.

**Explicit non-goals:** Do not select or benchmark a real dataset, redesign Luna-4/Luna-10 APIs, invent visualization-only mutations, alter TPCV-1 semantics, add a visualization return path, authorize Luna-15/Luna-16/Luna-17, or weaken A01-A15.

**Expected handoff:** A persistent-topology CPU runner, bounded structural-plasticity and structure/function evidence, TPCV replay artifacts/tests, inertness reporting, deterministic capture-on/off comparisons, and an explicit integration-readiness decision returned to Luna-0.

**Completion gate:** The implementation uses one validated bounded topology across the declared training scope; mutation accounting and rejection reasons are inspectable; fixed/plasticity/control comparisons run; topology and activity replay is deterministic and downstream-only; boundedness and non-interference checks pass; metrics support an evidence-based inertness/usefulness classification; and no architecture invariant is weakened.

## Luna-12C - Human-Interpretable 3D Temporal Visualization

**Authorization:** Luna-12C is authorized by Luna-0 on 2026-09-27 as an observational, replay-first milestone. It preserves the downstream-only TPCV architecture and does not change A01-A15 or require an ACP.

**Dependency shape:**

```text
Luna-12
|
+--> Luna-12A  CPU training + replay
|      |
|      +--> Luna-12B  persistent topology + plasticity observability
|
+--> Luna-12C  human-interpretable 3D temporal viewer
|
+--> Luna-13  GPU-compatible visualization
|
+--> Luna-14  ModelSim/FPGA visualization
```

Luna-12C may consume Luna-12A/B replay artifacts but is not a prerequisite for Luna-13 or Luna-14. Those milestones remain independent siblings under their existing authorization records.

**Purpose:** Provide human-interpretable 3D replay of stable neuron identity, activity, directed connections, structural changes, and synchronized behavioral/structural metrics during recorded learning.

**Graphics strategy:** Adapt the existing Python `pygame` + `PyOpenGL` path with NumPy buffers. The older GLFW path is coupled to simulation objects and CuPy, so it is not the primary foundation for this replay viewer.

**Scope:** Load bounded TPCV replay artifacts; preserve canonical coordinates when present or derive a deterministic diagnostic 3D layout; render neurons and directed edges with separate readable encodings; distinguish persistent, added, and recently pruned edges where replay history permits; provide configurable topology highlights and dense-graph filters; support play/pause, speed, both-direction stepping, first/last, direct snapshot selection, orbit, pan, zoom, reset, fit, neuron inspection, and synchronized metrics; and use packed/batched rendering with a path for later run/seed comparison.

TPCV-1 currently lacks canonical 3D coordinates, event-by-event propagation timing, per-edge traffic, and per-neuron energy/utility fields. Luna-12C must therefore show deterministic diagnostic positions and snapshot-level activity, display unavailable fields as unavailable, and never synthesize event pulses or timing.

**Non-interference:** Loading, layout, rendering, filters, playback, selection, window timing, dropped frames, and a slow viewer must not affect event ordering, timestamps, queues, routing, topology or structural plasticity, reward, utility, classifier behavior, training, or reproducibility. The renderer is not part of the TPCN architecture.

**Explicit non-goals:** Do not alter TPCV-1 semantics, implement GPU or ModelSim/FPGA paths, select a real dataset, add live-training coupling, create visualization-only mutations, or authorize Luna-15/Luna-16/Luna-17.

**Expected handoff:** A replay-first 3D viewer, deterministic layout and playback evidence, neuron inspection and filtering, synchronized metric presentation, focused headless/viewer tests, artifact fixtures/digests, unsupported-field documentation, and an explicit non-interference result.

**Completion gate:** Existing replay artifacts load; stable neurons and edges render; topology changes are distinguishable; deterministic playback/navigation, inspection, filters, and metrics work; repeated replay produces the same layout/view state; focused and relevant regression tests pass; and visualization has no effect on recorded computation.

## Luna-12D - Temporal Interpretability and Network-Dynamics Analysis

**Authorization:** Authorized by Luna-0 for analysis of existing TPCV-1/replay
artifacts and permitted deterministic synthetic runs. This remains authorized
even if Luna-12C has an unavailable interactive graphics check. It does not
authorize real-dataset benchmarking, hardware acceptance, or Luna-15/16/17.

**Purpose:** Measure and interpret the current system without repairing the
known separation between persistent topology mutation and the computational
path used by `_run_example()`.

**Dependency shape:**

```text
Luna-12 -> Luna-12A -> Luna-12B -> Luna-12C -> Luna-12D
                                |
                                v
                              Luna-12E

Luna-12 -> Luna-13  GPU-compatible visualization
Luna-12 -> Luna-14  ModelSim/FPGA visualization
```

Luna-13 and Luna-14 remain independent siblings and do not depend on 12D or
12E. Luna-12D may consume 12C-compatible replay artifacts, but all analysis
remains downstream-only.

**Scope:** Produce human-readable summaries and machine-readable metrics for
active/inactive neurons; persistent, exercised, added, removed, and rejected
edges; edge lifetimes; additions/removals per epoch; rejection reasons; graph
stabilization; fan-in/out saturation; active-edge utilization; topology-change
and activity concentration; and correlation with accuracy, prediction loss,
reward, and utility. Distinguish edge existence from computational exercise
where evidence exists, and never infer causation from correlation.

Explicitly investigate the connection plateau using precise causes such as
duplicate edge, source fan-out full, destination fan-in full, global edge
capacity, nonlocal candidate, candidate capacity, pruning/growth interaction,
or no valid candidate remaining. Classify observed states as stable/active,
stable/inactive, structurally changing/behaviorally flat, improving,
degrading, or high-churn/low-functional change.

**Non-goals:** Do not integrate topology into event routing, alter TPCV-1,
change neuron/classifier/training behavior, claim causality, select a real
dataset, accept hardware behavior, or authorize 13/14/15/16/17 work.

**Expected handoff:** Reproducible summaries, machine-readable metrics,
plateau/rejection evidence, correlation-limited interpretation, focused tests,
and a recommendation for Luna-0 review before 12E dispatch.

**Completion gate:** Requested topology/activity categories are represented or
explicitly unavailable; existing versus exercised edges are distinguished;
rejection reasons are precise; plateau behavior is explained from recorded
evidence; summaries and metrics reproduce; and analysis has no return path.

## Luna-12E - Computational Topology Integration and Causal Learning Verification

**Authorization:** Blocked until Luna-12D completes and Luna-0 reviews its
evidence. Creating this entry does not authorize implementation, real-dataset
benchmarking, hardware acceptance, or Luna-15/16/17.

**Purpose:** Make persistent bounded topology the actual event-routing network
used by the experiment path, then verify that structural changes can causally
alter network behavior.

**Dependency shape:**

```text
Luna-12C -> Luna-12D -> Luna-12E
```

**Scope:** Use the same bounded topology for structural plasticity and
computation. Verify event propagation through actual edges; removal of a
reachable edge changing downstream activity; addition of a reachable edge
changing downstream activity when relevant; prediction/error behavior derived
from propagated activity; and functional metrics responding to topology under
a workload that exercises the changed path. Use controlled reachable-edge
interventions and matched controls.

**Non-goals:** Do not weaken A01-A15, introduce a global neural clock, create a
second topology model, bypass finite routing, use unrestricted global learning,
select a real dataset, or claim hardware acceptance. Do not dispatch before
the 12D evidence review.

**Expected handoff:** Integrated routing evidence, reachable-edge intervention
results, prediction/error and classification metrics, boundedness and
determinism results, and an explicit Luna-0 readiness decision.

**Completion gate:** Structural plasticity and event computation share one
validated bounded topology; add/remove interventions produce causal routing
effects; prediction/error and functional metrics derive from propagated
activity; matched controls rule out observational confounds; and applicable
core/non-interference checks pass.

**Luna-0 downstream-failure classification (2026-10-04):** the two known
Luna-12E failures are legacy-observable assertions retained across the later
EXCURSION_V1 default switch. The routed-edge intervention still produces
delayed delivered activity and increases processed events; the test's
additional unconditional `prediction_loss`-must-change assertion is not
supported by its one-way source-to-sink topology. The second test's neuron
identity assertion passes, but its final-clock expectations compare settled
E2 local clocks against pre-E2 per-point values; it does not demonstrate
missing character-state reset. See
`workflow/handoffs/luna-0-classification-luna-12e-failures-20261004.md`.
These tests remain unresolved downstream compatibility failures. This
classification authorizes no code/test change and no Luna-28 creation or
execution; a separate governance decision is required before follow-on work.

## Luna-12F - Readout Learning and Class-Separation Verification

**Authorization:** Luna-12E is complete and accepted by Luna-0 for the
computational-topology gate. Luna-0 authorizes Luna-12F for deterministic
synthetic A/Z readout verification and correction of the external supervised
readout path only. This does not authorize real-dataset benchmarking,
Luna-15/Luna-16/Luna-17, or an architecture-wide classifier redesign.

**Purpose:** Determine whether the current positive-reward-only readout update
condition starves an initially misclassified class, measure class separation
before readout selection, and apply the smallest bounded external-readout
correction that permits every supervised training class to acquire a
representation.

**Dependency shape:**

```text
Luna-12C -> Luna-12D -> Luna-12E -> Luna-12F

Luna-12 -> Luna-13  GPU-compatible visualization
Luna-12 -> Luna-14  ModelSim/FPGA visualization
```

Luna-12F preserves the successful Luna-12E event-routing and persistent
bounded-topology integration. Luna-13 and Luna-14 remain independent siblings
and do not depend on Luna-12F.

**Architectural boundary:** Labels may enter only the external supervised
training/readout layer after label-free neural computation has completed. They
must not enter canonical events, neuron or predictor state, topology mutation
evidence, structural-plasticity decisions, routing, or energy computation.
Readout state is external, bounded by `max_classes`, deterministic, and
resettable. Reward may modulate refinement, but reward sign must not be the
sole condition for creating a supervised class representation.

**Required work:**

1. Reproduce the current gate with a deterministic A/Z fixture, recording
  initial prediction, reward, update decision, and prototype/readout state;
  explicitly test whether a misclassified Z can create Z state.
2. Expose pre-readout network features, target label for evaluation only,
  class distances/scores, prediction, confidence, and winner margin. Measure
  whether A and Z are separable before the readout and whether the readout
  discards that difference.
3. Implement the smallest compatible supervised prototype/centroid or class
  statistics correction. Separate target acquisition from any
  reward-modulated refinement and report missing declared class
  representations.
4. Compare positive-reward-gated and corrected readouts on identical seeds
  and workloads. Report accuracy, per-class accuracy, confusion matrix,
  confidence/margin, prediction loss, reward, energy, utility, topology,
  update count, prototype count, and starvation count.
5. Compare fixed topology, structural plasticity, and useful no-learning
  controls after readout correction. Do not require topology to improve
  accuracy and do not claim readout changes improve the neural predictor.
6. Add replay-side diagnostics where compatible with existing TPCV-1 fields;
  keep capture and analysis downstream-only and avoid incompatible schema
  changes without Luna-0 review.

**Required tests:** Both classes acquire bounded readout state; an initially
misclassified Z can become correct after supervised updates; label changes do
not change the neural event trace for identical inputs; labels affect only
external readout learning/evaluation; `max_classes` bounds state; and same-seed
training reproduces readout state. Include Luna-12E causal integration,
experiment, classifier/readout, structural-plasticity, and relevant
visualization/analysis regressions.

**Non-goals:** Do not modify canonical event semantics, neuron/predictor
state, topology mutation logic, routing, energy computation, TPCV-1 semantics,
or sibling milestone dependencies. Do not benchmark a real dataset or replace
the network with a large unrelated classifier.

**Expected handoff:** A reproducible before/after starvation analysis,
pre-readout separation diagnostics, bounded corrected-readout implementation,
fixed/plasticity/control comparisons, focused and full validation results, and
an explicit statement of whether the readout bottleneck was confirmed.

**Completion gate:** All required label-isolation, boundedness, determinism,
class-acquisition, before/after, and topology-interaction evidence is recorded;
the Luna-12E causal tests remain passing; applicable regression, compile,
diagnostic, and diff checks pass; and no A01-A15 invariant is weakened.

## Luna-12G - Spiral Handedness Temporal Classification Benchmark

**Authorization:** Luna-12F is accepted by Luna-0 for the corrected external
readout dependency. Luna-0 authorizes Luna-12G on 2026-09-27 as a synthetic
software-reference benchmark. This authorization does not authorize real
handwriting data, GPU/FPGA/ModelSim acceptance, hardware promotion, or an
architecture-wide classifier redesign.

**Purpose:** Replace the overly separable synthetic A/Z workload with a
two-class center-outward spiral benchmark whose primary class information is
ordered temporal handedness: left-handed versus right-handed trajectories.
Both classes start at the center and share the same nuisance distributions.

**Dependency shape:**

```text
Luna-12C -> Luna-12D -> Luna-12E -> Luna-12F -> Luna-12G

Luna-12 -> Luna-13  GPU-compatible visualization
Luna-12 -> Luna-14  ModelSim/FPGA visualization
```

Luna-12G consumes the accepted Luna-12E event-routing path and Luna-12F
external readout. Luna-13 and Luna-14 remain independent siblings and do not
depend on 12G.

**Scope:** Define a deterministic seeded generator and disjoint train/eval
streams for left/right center-outward spirals. Sample global rotation, scale,
translation, angular speed, bounded radial growth, sampling timing, mild
coordinate noise, and mild radial jitter independently of class. Record
generator metadata for reproduction, but feed only ordered stroke and timing
events plus legitimate boundary events to the neural computation.

Run fixed-topology learning, structural-plasticity learning, and a no-learning
control with external readout learning disabled. Add shuffled-order, carefully defined time-reversal, same-class
nuisance-invariance, and opposite-handed matched-pair controls. Report
accuracy without treating 1.0 as a success threshold; investigate any perfect
no-learning result as possible benchmark leakage.

**Architectural boundary:** Handedness labels remain external. They must not
enter canonical events, node or neuron IDs, event types, predictor state,
topology mutation evidence, structural-plasticity decisions, energy state, or
routing. Readout supervision may use the target only after label-free neural
processing, through the bounded Luna-12F readout interface.

**Non-goals:** Do not alter A01-A15, add a global neural timestep, introduce a
spatial reservoir, use future points or whole-example normalization, benchmark
real handwriting, or authorize sibling visualization/hardware work.

**Expected handoff:** A benchmark specification and reproducible implementation
with exact seeds/splits, trajectory metadata, all controls, per-class and
confusion diagnostics, prediction/readout/energy/utility/event/topology/
mutation metrics, label-isolation evidence, and a report of whether fixed or
structural topology contributes useful behavior.

**Completion gate:** Train and evaluation examples are disjoint and nuisance
combinations are not copied verbatim; both classes and all required controls
are measured; labels are isolated from neural computation; no-learning,
fixed-topology, and structural-plasticity results are separately reported;
ordered, shuffled, and reversal behavior is analyzed; deterministic replay and
bounded core/regression checks pass; and no accuracy threshold is invented.

## Luna-12H - Intrinsic Temporal State, Recurrence, and Unequal-Delay Convergence

**Authorization:** Authorized by Luna-0 on 2026-09-27 after the Luna-12G
benchmark reported identical ordered, shuffled, and reversed classification
results. The existing architecture already permits local elapsed-time state,
finite propagation, and bounded recurrent dynamics; this milestone makes the
canonical evidence requirements explicit. No ACP is required. This dispatch
does not authorize a real dataset, hardware acceptance, or a spiral-specific
neuron/classifier redesign.

**Purpose:** Determine whether the neural core itself preserves temporal
information before adding a more sophisticated external temporal classifier.
Verify two distinct mechanisms: intrinsic local state that persists and
evolves between events, and network/path temporal state in which consequences
with unequal cumulative delays converge at a downstream neuron.

**Dependency shape:**

```text
Luna-12C -> Luna-12D -> Luna-12E -> Luna-12F -> Luna-12G -> Luna-12H

Luna-12 -> Luna-13  GPU-compatible visualization
Luna-12 -> Luna-14  ModelSim/FPGA visualization
```

Luna-12H uses the accepted Luna-12E event-routing path and the Luna-12G
temporal-order limitation as motivation. Luna-13 and Luna-14 remain
independent siblings and do not depend on 12H.

**Canonical temporal semantics:** A neuron is not a memoryless event
transform. Processing may depend on `state_before`, `incoming_event`, and
`elapsed_local_time`. Conceptually, local state evolves analytically or when
an event is processed:

```text
s(t1-) = Phi(s(t0+), t1 - t0)
s(t1+) = F(s(t1-), event_t1)
```

A single event must be able to perturb bounded state that is observable later
before a declared character/sequence reset. The reference neuron must expose
at least one deterministic temporal noncommutativity fixture where exchanging
event order changes state, output, or trace; this is a capability requirement,
not a claim that every parameter choice is order-sensitive. Elapsed time comes
from canonical event timestamps and local neuron time. No synchronous whole-
network step, global frame update, or hidden recurrent tick may be required
for correctness. Internally scheduled events may be documented and tested only
if already supported cleanly; do not invent autonomous events merely to pass
these checks when analytic event-time evolution is sufficient.

**Routing and recurrence semantics:** Permit `A -> C` and
`A -> B -> D -> C` to have different cumulative causal delays; path delay is
the sum of declared edge delays, not edge count. Preserve event timestamps and
canonical deterministic tie-breaking at fan-in. An older long-path consequence
must be able to converge with a newer short-path consequence and affect the
downstream result according to relative arrival timing. Cycles remain subject
to finite event budgets, lineage/path safeguards, queue bounds, monotonic local
time, bounded state and deterministic ordering. Luna-12H must not enable
infinite recurrent propagation.

**Reset and isolation:** Temporal neuron state persists within a character or
sequence and resets only at declared reset boundaries. Topology may persist
independently. Pending events, internal state, eligibility and prediction
records require an explicit boundary policy. No state may leak between
examples unless explicitly authorized, and labels remain outside neural
events, state, routing, topology, energy and prediction/error computation.

**Required controlled fixtures:**

1. Single-spike persistence: `+1` at `t=0`, then observe state before reset.
2. Ordered-pair noncommutativity: `(+1 at 0, -1 at 1)` versus
  `(-1 at 0, +1 at 1)` produces a state/output/trace difference.
3. Equal-event multiset distinction: the same event values with different
  order produce a deterministic difference.
4. Same values, changed interval: `+1 at 0, -1 at 1` versus
  `+1 at 0, -1 at 5` differs when elapsed time is relevant.
5. Unequal paths: verify `D_long > D_short` and timestamp-correct arrival for
  direct and multi-hop paths.
6. Convergent old/new arrival: an older event uses the long path and a newer
  event uses the short path; changing their timing relationship changes the
  downstream result.
7. Path pruning: pruning either path removes its future causal effect.
8. Arrival timing: the same total input with different arrival timing changes
  downstream state/output in at least one deterministic fixture.
9. Character reset: reset removes prior temporal state according to policy.
10. Same-seed determinism: state, queue, timestamps and ties reproduce.
11. Bounded recurrence: cycles terminate under declared budgets and bounds.
12. Label isolation: relabeling identical streams does not alter core traces.

**Expected handoff:** A focused implementation and verification slice for the
canonical neuron and event-routing path, fixture-level traces with units and
seeds, explicit decay/evolution/reset and tie policies, bounded-cycle and
pruning evidence, focused tests, applicable regression/compile/diagnostic
results, and a Luna-0 readiness decision. Report whether intrinsic or path
temporal state is demonstrated; do not infer temporal representation from
external classifier accuracy alone.

**Non-goals:** Do not hard-code spiral handedness, introduce a mandatory
global timestep, replace the event queue with synchronous stepping, add a
spatial reservoir, leak labels or future points into the core, or redesign the
external classifier before the core fixtures are measured.

**Completion gate:** All twelve controlled checks and the four minimal fixture
families are run or explicitly marked not applicable; timestamps, cumulative
delays and fan-in order are evidenced; reset/isolation and label isolation
pass; cycles remain bounded; same-seed replay passes; and no A01-A15 invariant
is weakened. An absent temporal effect is a valid result, but must be reported
as a failed capability check rather than hidden by readout changes.

## Luna-12I - Temporal-Associative Structural Growth and Fan-In Formation

**Authorization:** A post-12H experiment specified by ACP-0001 and the
project-owner request. It is not evidence that the mechanism works and does
not promote its rule into A14. Luna-13 and Luna-14 remain independent siblings.

**Classification:** `EXPERIMENT`, with `VERIFICATION` of bounded topology and
locality invariants. **Baseline:** the current repository revision recorded in
the dispatch handoff. **Dependencies:** accepted 12H semantics, Luna-4
bounded topology, Luna-10 structural-plasticity API, and the Luna-12E actual
event-routing path.

**Hypothesis:** If activity at two neurons repeatedly occurs in a consistent
short causal sequence, locally available timing evidence can increase
preference for a directed edge from the earlier neuron to the later neuron.
This may encourage causal path shortening and useful fan-in without global
topology knowledge. Evidence against the hypothesis includes no increase in
convergent causal structure over controls, timing-shuffled/reversed controls
performing equivalently, or increased churn/energy/resource use without
improved structural organization or task behavior.

**Controls:** Compare matched fixed topology, the existing structural-
plasticity policy, random legal candidate selection, and temporal-association
candidate selection. Where practical add timing-destroyed/shuffled and
reversed-order association controls. Keep seeds, budgets, workload, delays,
reset policy and training effort matched.

**Measurements:** Report fan-in/out distributions and saturation, edge
utilization, accepted growth, every rejection cause, duplicate proposals,
candidate availability, path lengths and cumulative causal delays, convergent
motif count, repeated temporal associations, path shortening,
replacement/pruning, edge lifetimes/churn, event count, prediction error,
energy/resource proxy with units, utility, task performance and determinism.
Distinguish degree saturation, random growth, duplicate churn and true useful
convergent fan-in. Record negative results and unavailable fields explicitly.

**Scope and invariants:** Production changes are authorized only in the
declared experiment components and tests. Preserve A01-A08, A07 label/local
information boundaries, A09-A11 accounting, A14 finite admission and causal
growth, and A15 portability. The mechanism may use only causal/local temporal
evidence; it may not inspect global topology, labels, future events or
evaluation-only metrics. A direct edge is a new positive-delay path and cannot
rewrite in-flight events. Bound candidate lists, evidence/history retention,
edge count, mutation count, event/lineage/queue budgets and all hardware-facing
representations.

**Non-goals:** Do not claim a useful learner from topology appearance alone,
make a timing window/correlation formula mandatory, redesign the classifier,
perform real-dataset or hardware acceptance, promote A14, add global learning
or implement unbounded topology.

**Expected handoff and gate:** Include the full Future Luna Contract fields,
controlled traces, all seeds/configurations/commands, negative results,
rejection accounting and `OBSERVED`/`INFERRED`/`HYPOTHESIZED` labels. The
mechanism is not accepted merely because it runs; Luna-0 reviews whether the
evidence supports a later experiment or ACP.

## Luna-12J - Temporal-Associative Structural Learning Efficacy and Causal Verification

**Authorization:** This is a separately dispatched `EXPERIMENT` and
`VERIFICATION` milestone after Luna-12I. Creating the scaffold does not
execute it. It does not amend A14, authorize temporal association as
mandatory, or block Luna-13, Luna-14, Luna-15, Luna-16 or Luna-17.

**Question and hypothesis:** Determine whether Luna-12I temporal-associative
growth produces useful computational or task-level benefit attributable to
learned topology rather than merely added edges or churn. Repeated local
temporal succession is hypothesized to guide bounded growth toward useful
convergence and/or shorter causal paths. Equivalent controls, no causal effect,
temporal-order destruction, or resource/churn costs that erase benefit count
against the hypothesis. Valid results include supported, partially supported,
not supported, inconclusive and blocked.

**Required controls:** Compare fixed topology, the existing pre-12I policy,
random legal structural growth and Luna-12I growth under comparable nodes,
edges, fan-in/out, candidates, state, events, mutation attempts, epochs,
delays, resets and seeds. Include shuffled, reversed, destroyed-timing or
matched-event-multiset controls where practical. Record and explain any budget
mismatch; do not search for favorable seeds.

**Computational and information boundary:** Use the persistent Luna-12E
topology and actual event-routing path. A disconnected visualization graph,
auxiliary topology or topology-only correlation is not evidence. Labels, future
events, global topology statistics, evaluation metrics and unrestricted trainer
state remain outside events, predictor state, routing, topology evidence,
structural evidence, eligibility and energy computation.

**Measurements and intervention:** Record task/class separation, prediction and
error behavior, events, activations, energy/resource proxy and units, edges,
additions/removals/rejections, fan-in/out and convergent motifs, utilization,
path delays/shortening, duplicates, replacement, churn, stabilization and
same-seed determinism. Perform a focused removal, freeze, legal replacement or
before/after replay intervention to test the chain from local evidence through
real topology and routed events to downstream state/output. Explicitly answer
whether ordinary growth saturates capacity before useful fan-in forms.

**Expected handoff and gate:** The handoff must include the full dispatch fields,
raw and summarized measurements, negative results, limitations and direct
answers to the seven Luna-12J questions. Separate `OBSERVED`, `INFERRED` and
`HYPOTHESIZED`, and passed/failed/not-run/not-applicable checks. Gate values are
PASS, PASS WITH FOLLOW-UP, INCONCLUSIVE, NOT SUPPORTED and BLOCKED. Any result
returns to Luna-0; even PASS does not promote A14 or automatically authorize
Luna-12K execution. Luna-0 may separately create a bounded follow-up after a
PASS WITH FOLLOW-UP decision.

## Luna-12K - Capacity-Pressure, Equal-Exposure, and Path-Shortening Verification

**Authorization:** Luna-12K is a separately scoped `EXPERIMENT` and
`VERIFICATION` follow-up created after the verified Luna-12J result
`partially supported` with gate `PASS WITH FOLLOW-UP`. Creation does not
execute the experiment. Execution requires an explicit assignment and a
completed 12K handoff; no A14 promotion or Luna-12L/later work is authorized.

**Question and hypothesis:** Under equal candidate exposure and bounded
topology pressure, temporal-associative structural growth is hypothesized to
allocate scarce connection capacity toward useful causal convergence and to
create a legal shortcut that measurably reduces meaningful propagation path
length or delay compared with temporally uninformed controls. The hypothesis
is falsified when equalized controls match or exceed useful allocation, real
capacity pressure is absent, temporal evidence does not alter selection, the
shortcut does not change routed computation, or the result disappears under
reversed/timing-destroyed evidence. Valid results are supported, partially
supported, not supported, inconclusive or blocked.

**Controls and equal exposure:** Compare fixed topology, pre-12I structural
growth, random legal growth, Luna-12I temporal growth and reversed/shuffled or
timing-destroyed temporal evidence. Equalize candidate set/count, mutation
opportunities, growth attempts, edge/fan-in/out bounds, pruning/replacement
budget, trials, event workload and seeds. Measure candidates exposed,
considered and selected. Record and quantify every mismatch; do not credit a
policy for extra useful candidates or computation. An oracle-like selector is
diagnostic only and is not a legal learning mechanism.

**Fixture and intervention:** Use multiple legal, resource-competitive
candidates, including temporally relevant and irrelevant edges. Reach actual
fan-in, fan-out, global-edge, candidate-capacity or replacement/pruning
pressure and record precise rejection causes. Begin with a functional
finite-delay long path and a legal initially absent shortcut in the actual
Luna-12E routed topology. Compare before growth, after shortcut formation and
after shortcut removal on hop count, cumulative delay, arrival timestamps,
routed events, activations, downstream state/output, prediction/error and
energy/resource proxy. Graph-distance change alone is insufficient.

**Invariants and evidence:** Preserve A01-A04, A06-A11, A14 and A15. Labels,
future events, global topology statistics, evaluation metrics, wall-clock state
and unrestricted trainer state remain outside canonical events, predictor
state, routing, topology evidence, structural evidence, eligibility and
energy computation. All candidates, histories, queues, paths, mutations and
analysis buffers are finite. The handoff must distinguish `OBSERVED`,
`INFERRED` and `HYPOTHESIZED`, retain unfavorable seeds, and classify every
focused, regression, full-suite, compile, diagnostic and diff check as passed,
failed, not run or not applicable. Any result returns to Luna-0.

## Luna-12L - Energy/Prediction Tradeoff and Four-Class Temporal Scale Verification

**Authorization:** Luna-12L is a separately scoped `EXPERIMENT` and
`VERIFICATION` follow-up created after the Luna-12K `PASS WITH FOLLOW-UP`
review. Creation does not execute the experiment, amend A14 or authorize a
later Luna. Execution requires a separate explicit assignment and a completed
12L handoff returning to Luna-0.

**Question and hypothesis:** Determine whether temporal-associative growth
retains useful classification and causal path-allocation behavior when the
Luna-12G spiral task expands to four classes combining handedness and
traversal direction, and whether the Luna-12K proxy-energy/prediction-loss
cost is bounded, explained or improved without destroying the causal benefit.
The primary hypothesis is falsified by loss of useful classification or path
allocation at the expanded scale, temporal-order controls performing
equivalently, or an unfavorable resource/prediction tradeoff without a
measured compensating benefit. A negative result is valid.

**Four-class benchmark:** Use the existing Luna-12G naming convention extended
to `spiral-left-outward`, `spiral-right-outward`, `spiral-left-inward` and
`spiral-right-inward`. Inward examples must use the same trajectory family as
outward examples and depend on traversal direction rather than a static class
marker. Match point count, radius, center, scale, noise, sampling, amplitude,
duration, payload conventions and identifiers across classes where practical.
Labels remain external to canonical events, prediction, routing, topology,
structural evidence, eligibility and energy. A reused sequence boundary/check
event must be identical and class-neutral across all classes.

**Controls and scales:** At both a seven-node reference scale and a modest
12-node expanded scale, compare fixed topology, pre-12I growth, random legal
growth, Luna-12I temporal growth and reversed/shuffled/timing-destroyed
evidence. Use seeds `0, 1, 2, 3, 4` and equal candidate exposure, mutation
budgets, bounds, workload and reset policy within each scale. The reference
scale preserves 12K capacities; the expanded scale uses bounded capacities of
10 edges, fan-in/out 3, candidate/history 12 and queue/event 24 with five
growth attempts. Serialize exact configurations before execution.

**Measurements and intervention:** Report four-class and per-class accuracy,
four-by-four confusion, handedness/direction pair confusion, class separation,
prediction loss/error activity, proxy energy and units, events, activations,
edges/utilization, path hops/delays, candidate exposure, mutations,
rejections, fan-in/out pressure, class-specific utilization and causal
shortcut evidence. Calculate accuracy/resource and prediction/resource
summaries without making them permanent objectives. Retain the 12K learned-edge
removal replay and compare routed traces, downstream state/output,
classification, prediction, energy and path delay. Investigate the 12K
prediction-loss increase without redesigning the predictor.

**Evidence and gate:** Focused tests must cover deterministic four-class
generation, matched inward/outward pairs, label and boundary-event isolation,
same-seed replay, equal bounds, four-class readout, temporal-order intervention,
consistent energy/prediction metrics and causal edge removal. The handoff must
separate `OBSERVED`, `INFERRED` and `HYPOTHESIZED` evidence and classify all
validation as passed, failed, not run or not applicable. Gates are `PASS`,
`PASS WITH FOLLOW-UP`, `NOT SUPPORTED`, `INCONCLUSIVE` and `BLOCKED` as
defined in the 12L specification. Any result returns to Luna-0; no A14
promotion, permanent energy/prediction formula, real-data claim, hardware
acceptance or successor authorization follows automatically.

## Luna-12M - Edge Lifecycle, Route Utilization, and Competing-Path Instrumentation

**Authorization:** Created and executed by Luna-0 at baseline
`7f8ea2df5896d3ea7cd7d41a4f1bd8298c0dc015` after the corrected Luna-12L
direction/decay review. This is an `OBSERVATION`, `VERIFICATION` and
`IMPLEMENTATION` milestone; it does not change A01-A15 or authorize a
successor.

**Purpose:** Instrument existing bounded topology and event routing so offline
analysis can distinguish shortcut creation, first/last use, route coexistence,
traffic crossover, pruning and replacement where supported. Global paths and
labels remain offline only.

**Boundary and gate:** The optional observer uses endpoint-plus-generation edge
identities, bounded ring buffers and saturating counters. It must preserve
event traces, timestamps, neuron/predictor state, routing, structural choices,
energy, eligibility and classifier results. `PASS` requires lifecycle and
traffic attribution, competing-path and decay-context evidence, deterministic
storage and ON/OFF equality. Missing replacement attribution or hardware
export may be `PASS WITH FOLLOW-UP`; execution influence, unboundedness or
ambiguous lifetimes is `BLOCKED`. Results return to Luna-0 and do not create a
direction/decay-gated shortcut experiment.

## Luna-12N - Temporal Direction and Intrinsic-Decay-Gated Shortcut Verification

**Authorization:** Luna-12N is a creation-only `EXPERIMENT` and
`VERIFICATION` milestone at baseline `0d91207ec5db0ab8011e0fc020cc9e4e20915428`,
created after corrected Luna-12M reached `PASS WITH FOLLOW-UP`. Creation does
not execute the experiment, amend A14, change the architecture contract,
authorize hardware acceptance or authorize a successor. Execution requires a
separate explicit assignment and returns to Luna-0.

**Question and hypotheses:** Determine whether locally legal edge direction and
intrinsic-neuron-decay-relative candidate preference increase genuinely used
causal shortcut yield under equal opportunity. H1 tests current versus
reversed orientation, H2 tests local decay-relative separation versus no decay
preference, and H3 tests their combination. A new correlated edge is not a
shortcut unless measured route use and causal compression are both present.

**Policy matrix:** Compare current/no-decay, reversed/no-decay,
current/decay-aware, reversed/decay-aware, random legal growth and fixed
topology. Preserve the same candidate pair for direction intervention where
legal; document an equivalent legal comparison when literal reversal is not
valid. Use seeds `0..4` and a predeclared finite set of decay-relative regimes;
do not tune global timing thresholds after inspecting outcomes.

**Locality and measurement:** Runtime policy inputs are limited to local event
timestamps, elapsed time, the neuron's own decay parameter/residual state,
local candidate evidence and legal local edge state. Global path analysis is
offline only. Use corrected Luna-12M `TPCN-EDGE-2` phase-scoped traffic,
endpoint-plus-generation lifecycle, candidate/rejection, pruning and decay
records. Measure exposure, attempts, admissions, rejection reasons, fan-in/out
and capacity, old/new route traffic, hop/cumulative-delay/arrival changes,
prediction/error, proxy energy, events and activations. Report static and used
shortcut yield separately and run matched present/remove/identical-replay
causal interventions.

**Boundary:** Do not change pruning, protection, persistent edge strength,
utility or eligibility, add a permanent threshold, inject labels or global
topology, add genetic hyperparameters or a micro-network, redesign the
classifier, modify A14 or claim hardware equivalence. Record premature-removal
protection and inherited-parameter ideas only as future research notes if
direct evidence warrants them. The result gates are `PASS`, `PASS WITH
FOLLOW-UP`, `NOT SUPPORTED`, `INCONCLUSIVE` and `BLOCKED`; all results return
to Luna-0 and no successor is authorized.

## Luna-13A - Stage-0 Software Reference Invariant Closure

**Authorization:** Luna-13A is a CPU-only `IMPLEMENTATION` and `VERIFICATION`
milestone created from the Luna-0 independent review of the corrected
Luna-12N work at reviewed checkpoint
`fdda3b59014109ce5aac6c5b2c9690b02acf85e9`. The reviewed result is
**PASS WITH FOLLOW-UP — MEASUREMENT CORRECTED, EFFICACY STILL UNESTABLISHED**.
Luna-12N established corrected configured-versus-actual accounting, independent
metadata controls, replay-measured arrivals, weighted cumulative-delay paths,
explicit event-budget status and strengthened provenance. Its synthetic fixture
showed score/rank changes but no different admitted edge set or final graph;
external prediction improvement, classification improvement, resource
efficiency and general temporal-learning superiority remain unestablished.

The sequence is explicit:

```text
Luna-12N corrective
  -> Luna-0 review
  -> Luna-13A Stage-0 invariant closure
  -> Luna-0 independent Stage-0 review
  -> determine whether a next Luna is authorized
```

Luna-13A closes software-reference integration blockers in four bounded areas:
classifier temporal monotonicity and stale-finalization atomicity, a declared
reward-delivery contract, projected structural-capacity rejection semantics,
and bounded recurrent execution. It is not a temporal-policy efficacy
experiment, dataset benchmark, GPU milestone or FPGA/FPAA equivalence test.
The assignment explicitly permits execution without a dedicated GPU and does
not require CUDA, GPU visualization, FPGA hardware or FPAA hardware. Optional
CUDA skips do not block it.

The reward-delivery behavior is a mandatory pause point. Luna-13A must inspect
current production behavior, documentation and tests and must not invent the
contract. It must either establish retry-idempotent logical delivery with
bounded identity retention or repeated-application delivery with obsolete
exactly-once claims removed. If repository authority remains contradictory, the
reward portion stops with **REWARD CONTRACT DECISION REQUIRED** and returns a
decision packet covering both models, affected files, bounded-state and replay
consequences. Safe non-reward Stage-0 work may continue, but the assignment
remains blocked.

The handoff must use
`workflow/handoffs/stage0-invariant-closure-Luna-13A.md` and include exact
revision/tree and worktree state, classifier before/after evidence, reward
disposition, projected-capacity and rejection-reason evidence, recurrent budget
semantics for budgets `1`, `2`, `8` and `64`, focused and full CPU validation,
remaining blockers and readiness for Luna-0 independent review. Terminal
statuses are constrained to the five statuses in the Luna-13A agent contract.
No Luna-13B is authorized by this entry. The likely future controlled
temporal structural-selection experiment remains contingent on Luna-13A and
the independent Luna-0 Stage-0 review.

### Luna-13A reward-contract resolution - 2026-09-29

The project owner selected **MODEL A — RETRY-IDEMPOTENT LOGICAL REWARD
DELIVERY**. `RewardSignal.message_id` is the explicit stable logical identity;
`RewardMessage.message_id` may provide it, and otherwise the existing
`RewardMessage.credit_id` is used as the stable identity. `EligibilityLedger`
owns a bounded FIFO retention window of accepted identities, default capacity
64 and configurable per ledger. Duplicate delivery within that window returns
`duplicate` without advancing the ledger clock, decaying traces or changing
credit. Distinct IDs apply independently even when all numeric and attribution
fields are equal. Reset clears identities and traces; deterministic FIFO
eviction permits a post-eviction identity to apply again. The guarantee is
bounded at-most-once credit application within one ledger scope, not permanent
global exactly-once processing.

Luna-13A implementation status is **PASS WITH FOLLOW-UP — READY FOR LUNA-0
STAGE-0 REVIEW**. Focused reward tests cover first delivery, immediate and
many duplicate retries, distinct equal-valued IDs, identical fields with
different IDs, deterministic replay, reset, bounded retention, FIFO eviction,
post-eviction behavior and independent eligibility expiry. The prior Luna-11
duplicate-application assertion is amended as historical evidence and now
expects retry suppression; intentional repeated reinforcement uses distinct
message IDs. Luna-13A returns to Luna-0 for independent verification. Luna-13B
remains unauthorized.

### Luna-0 independent review - 2026-09-29

This section records the pre-resolution review at revision
`047d2dd59905934a5100dcafb791835e93708b37`; the reward finding below is
historical and is superseded by the owner decision and implementation recorded
in the preceding resolution section.

**Reviewed revision:** `047d2dd59905934a5100dcafb791835e93708b37`, pushed as
`origin/main`; the source tree was clean at review time. The Luna-13A handoff
is `workflow/handoffs/stage0-invariant-closure-Luna-13A.md`.

**Independent result:** **BLOCKED — REWARD CONTRACT DECISION REQUIRED**.

- **Classifier:** PASS. An independent probe with START at `0`, activity at
  `8`, and direct stale finalization at `5` rejected before mutation. Time,
  active state, scores, result, character index and committed result state
  were unchanged. Equal-time, future-time and dispatched finalization agreed
  with direct semantics.
- **Reward contract:** BLOCKED. Independent delivery of the same
  `RewardSignal` applied credit twice. `RewardSignal` exposes only `reward`,
  `trace_id` and `prediction_id`; it has no delivery identity. The Luna-8
  handoff still claims bounded `message_id` retention, while the production
  implementation and adversarial test assert repeated application. Luna-0
  does not select Model A or Model B here.
- **Structural admission:** PASS. Independent jointly-invalid fan-in and
  fan-out batches, edge-capacity exhaustion, atomic topology preservation,
  deterministic public causes, and observer ON/OFF equivalence all passed.
- **Recurrence budget:** PASS for the canonical `execute_bounded` path.
  Positive-delay loop probes at budgets `1`, `2`, `8`, and `1` reported the
  exact processed budget, one pending event, `budget_exhausted`, and
  `completed=False`; finite work reported `completed=True`. No global neural
  timestep was introduced. A legacy Luna-12J efficacy replay still uses a
  manual bounded loop without returning termination status; this is recorded
  as follow-up evidence and is not silently promoted as canonical execution.
- **Regression:** The independent temporal/runtime/credit/topology slice
  passed `109` tests. The complete CPU suite passed `234` tests with `1`
  optional CUDA/GPU skip, which is not a failure. `compileall` and
  `git diff --check` passed. Luna-12H and Luna-12N corrective tests passed;
  Luna-12N is not reinterpreted as decay efficacy evidence.
- **Architecture conformance:** Core A01/A02/A03/A04/A07/A08/A11/A15
  behavior checked here remains conformant for the reviewed paths. Reward
  identity semantics remain unresolved, and Luna-12J's legacy replay status
  reporting should be normalized before broader reuse.

### Luna-0 independent Stage-0 review - 2026-09-29 - resolved reward contract

The post-Model-A review was performed independently against published
implementation revision `fba6e4de5fb93b150f6a7e7e545622d48ae7b3c5` and the
clean review baseline `db459c1e6dff8b90f74288a67e898552c12dc85f`.

**Independent result:** **PASS WITH FOLLOW-UP - STAGE-0 READY.**

- **Reward identity attack matrix:** PASS. Direct adversarial replay verified
  duplicate suppression without clock or credit mutation, including a valid
  stale timestamp; distinct equal-valued identities applied independently;
  FIFO eviction reopened an evicted identity; reset cleared identity scope;
  identical IDs were independent across ledgers; fallback and explicit
  `RewardMessage` identities mapped as documented; deterministic replay
  matched across fresh ledgers; and 1,000 accepted identities never exceeded
  a four-entry retention window.
- **Stage-0 preservation slice:** PASS, `127` passed.
- **Full CPU regression:** PASS, `242` passed and `1` optional CUDA/GPU test
  skipped. Compilation and `git diff --check` passed.
- **Documentation finding:** The Luna-13A handoff had stale pre-Model-A
  counts and a pending tree-state phrase; these were corrected in the review
  publication. No production-code defect was found in the identity semantics.
- **Architecture:** A11 is conformant as bounded at-most-once credit
  application within one ledger retention scope. No ACP is required and no
  permanent global exactly-once claim is made.

The legacy Luna-12J manual replay termination-status follow-up remains open and
non-gating. Stage-0 is independently reviewed as ready at the published
checkpoint `ecb3f412b55d6978c5551798900cb1bacf76a238`: classifier temporal
monotonicity, bounded reward identity/idempotency, projected structural
admission and bounded recurrent execution passed; the Stage-0 slice recorded
`127 passed`, and the full CPU suite recorded `242 passed, 1 skipped`. The
optional CUDA/GPU skip is non-blocking. Luna-13B creation is now authorized,
but execution still requires its own explicit assignment and independent
Luna-0 review.

## Luna-13B - Causal Local Temporal Structural Crossover

**Authorization boundary:** The authoritative sequence is:

```text
Stage-0 Luna-0 closure
  -> Luna-0 creates Luna-13B contract
  -> Luna-13B executes
  -> Luna-0 independently reviews Luna-13B
  -> determine whether Luna-13C is authorized
```

Creating the contract does not execute Luna-13B. Luna-13B is a CPU-only
`EXPERIMENT` and `VERIFICATION`; CUDA, GPU visualization, FPGA and FPAA are
not required. Luna-13C remains unauthorized until the independent Luna-0
review explicitly determines otherwise.

**Scientific question and gate:** Determine whether actual causally observed
local temporal evidence produces a predicted decay-dependent structural
admission decision when finite capacity forces competing candidates to contend
for exactly one available slot. Luna-12N showed score/rank sensitivity but no
admitted-edge or final-graph difference; Luna-13B tests that missing causal
structural-selection step.

Candidate evidence must come from runtime observations available to the local
decision component, with provenance for source, timestamps, elapsed intervals,
local state/residual, decay, score and decision time. A frozen analytic
crossover must predict opposite winners before held-out evaluation. At least
two equally exposed candidates must compete for the one slot, and the final
graph must reveal the selected edge. Reports must distinguish score, rank,
admitted-edge and final-graph changes. Labels, future observations, global
statistics and hand-authored endpoint timing tables are excluded from the
decision.

Required controls include ordinary and decay-informed association, reversed and
time-shuffled observations, random/score-shuffled selection, fixed topology,
uniform intervals, neutral/zero decay where valid, mirrored/relabelled
fixtures, exact/near ties and deterministic replay. Matched capacity,
candidate exposure, bounded execution and rejection accounting are mandatory.
Every run reports budget, processed/pending work, queue peak where available,
termination reason and `completed` or `budget_exhausted`; exhaustion is not a
successful observation.

The required handoff is
`workflow/handoffs/causal-local-temporal-crossover-Luna-13B.md`, using the
standard template and separating `OBSERVED`, `INFERRED` and `HYPOTHESIZED`
claims. All results return to Luna-0. Scores/ranks without a changed admitted
edge must be reported as `SCORING/RANK SENSITIVITY CONFIRMED — STRUCTURAL
CROSSOVER NOT ESTABLISHED`. Luna-13B cannot authorize Luna-13C.

### Luna-0 independent review of Luna-13B - 2026-09-29

Reviewed implementation and published artifact revision
`816929fa097e049ce7d82a1f7c63fb9cc4e8bd3f` after synchronizing with
`origin/main`. The review tree was clean and `HEAD == origin/main` at review
start. The contract is `.github/agents/luna-13b.agent.md`, the execution
handoff is `workflow/handoffs/causal-local-temporal-crossover-Luna-13B.md`,
and the artifacts are under
`artifacts/causal-local-temporal-crossover-13b/`.

**Independent result:**
**PASS — LUNA-13B CAUSAL STRUCTURAL CROSSOVER INDEPENDENTLY VERIFIED**.

- Runtime-local evidence passed. Candidate residuals and scores were derived
  from routed finite-delay events and canonical-neuron local state; timestamps,
  elapsed intervals, source events and decision times were reconstructable.
- The production equation reproduced the frozen crossover
  `mu* = 0.07833747196936626`. Low/high scoring decay produced opposite ranks,
  admitted edges and explicit final edge sets under one remaining slot.
- One-slot capacity passed: two locally valid candidates competed from zero
  edges, one edge was grown, and the other was rejected with `edge_capacity`.
- Relabeling and mirroring followed semantic temporal evidence rather than
  identifier order. Exact ties used the declared deterministic identifier rule;
  near-boundary replay was deterministic.
- Reversed, shuffled, uniform, neutral, random, score-shuffled and fixed
  controls behaved according to their declared purposes. Score-shuffled
  preserved raw rank while changing the selected edge, demonstrating why
  structural choice was separately measured.
- Scoring decay and execution decay were independently configurable. The
  primary crossover held execution decay fixed; the review also ran an
  execution-decay factorial comparison and makes no claim that runtime decay
  is irrelevant.
- Primary and control runs completed without budget exhaustion. The review
  reproduced `7` processed events, `0` pending events and peak queue occupancy
  `4`; increasing the budget to `30` did not change the result.
- Stage-0/Luna-12H/Luna-12N preservation passed. The review slice passed `135`
  tests and the full CPU suite passed `250` with `1` optional CUDA/GPU skip;
  compileall, diagnostics and `git diff --check` passed.

The result is narrow: Luna-13B establishes a bounded software-reference
mechanism in which causally observed local temporal evidence can reverse a
decay-sensitive candidate ranking and change one-slot structural admission and
the final graph. The controlled intervals are finite runtime fixture delays;
this review does not establish task usefulness, classification or prediction
improvement, energy efficiency, scalability, hardware equivalence, biological
plausibility or general superiority. Luna-12J's manual replay termination
status remains a non-gating follow-up. Luna-13C is not authorized. A future
contract may be proposed for causal usefulness of a learned edge against an
external task target, subject to a new owner request and Luna-0 review.

## Luna-13C - Useful Causal Effect of Learned Temporal Structure

**Authorization boundary:** The lifecycle is:

```text
Luna-13B independent PASS
  -> Luna-0 creates Luna-13C contract
  -> Luna-13C executes under a separate explicit assignment
  -> Luna-0 independently reviews Luna-13C
  -> determine whether any successor is authorized
```

The independent Luna-13B review is recorded at review revision
`04f2088725c71eb20b808ae07dbd99a02d4cd459`, reviewing implementation revision
`816929fa097e049ce7d82a1f7c63fb9cc4e8bd3f`. It established runtime-local
causal evidence, the predicted decay-sensitive crossover, rank and admitted-
edge reversal under one-slot competition, final-graph change, controls,
determinism and bounded execution. It did not establish task usefulness,
external prediction or classification improvement, resource efficiency,
scalability or hardware equivalence. Luna-12J's manual replay termination
status issue remains non-gating.

Luna-13C is a CPU-only `EXPERIMENT` and `VERIFICATION` contract. It reuses the
verified Luna-13B structural-selection mechanism and asks whether the learned
edge produces a useful effect on a fixed external task target independent of
the topology being evaluated. Prefer the smallest bounded temporal-order,
interval-dependent or delayed-cue task; defer the full A-Z benchmark until
the simple causal mechanism is established. CUDA, GPU visualization, FPGA and
FPAA are not required, and an optional CUDA skip is non-gating.

Freeze the task, topology-independent external target, decision rule/loss,
primary metric, practical effect threshold, interventions, seeds and budgets
before held-out evaluation. Freeze the learned structural state once, then
clone or restore that identical state for paired conditions using the same
inputs, targets, initialization and execution resources. Require:

- learned edge present;
- targeted removal of only the claimed learned edge;
- exact restoration of the same source, target, delay, strength and
  computation-affecting metadata;
- sham metadata/no-op intervention;
- irrelevant or unused edge removal;
- fixed topology with no growth;
- equal-budget random growth with explicit seeds; and
- a fixed useful-edge positive control.

The external target must not be generated from edge identity, path length,
current-topology activation, candidate score or the model's own prediction.
Measure topology, internal trace and external task outcome separately. The
causal gate requires present-graph benefit, material targeted-removal loss,
exact restoration within tolerance, null or smaller sham/irrelevant effects,
an expected positive-control result, matched inputs/targets/resources and
completion without silent budget exhaustion. A failed positive control blocks
interpretation rather than proving learned-edge uselessness. Labels and
targets remain outside candidate generation, local scoring, structural
admission and core runtime state.

Every run records configured and processed events, pending events, termination
status, graph fingerprints, external metrics, target arrival/decision state
and proxy energy where available. Proxy energy is secondary and need not
decrease. The required handoff is
`workflow/handoffs/useful-causal-effect-Luna-13C.md`, using the standard
template and separating `OBSERVED`, `INFERRED` and `HYPOTHESIZED` evidence.
Validation covers all interventions and controls, fixed-target and matched-
input semantics, exact graph restoration, label/future isolation,
deterministic replay, held-out freeze and completion status, followed by
Luna-13B, Stage-0, Luna-12H, corrected Luna-12N, full CPU, compile/static,
diagnostic and `git diff --check` regressions. Results return to Luna-0.
Luna-13C must not authorize Luna-13D.

### Luna-0 independent review of Luna-13C - 2026-09-29

Reviewed implementation and artifact revision
`575c2407db21786b21d64cb57d640d2a1a940ac0` after synchronizing with
`origin/main`; the review started from a clean tree with matching `HEAD` and
`origin/main`. The review handoff is
`workflow/handoffs/luna-0-review-Luna-13C.md`.

- **External target valid:** the fixed targets are `on_time` for the short
  interval and `late` for the long interval, independent of topology. The
  default learned-present result is `2/2`; targeted removal is `1/2`; exact
  restoration is `2/2`; sham is `2/2`; irrelevant removal is `2/2`; fixed
  topology is `1/2`; seed-0 random growth is `1/2`.
- **Causal task effect reproduced:** target arrivals change from `(1.0, 2.0)`
  to no arrivals for the short case when `right -> target` is removed; exact
  graph restoration recovers the arrivals and result. All primary runs
  complete without budget exhaustion, and an event-budget increase to 30 does
  not change the result.
- **Follow-up limitations:** sham bypasses intervention machinery; fixed
  useful control is the exact learned edge rather than an independent edge;
  seed 1 random growth reproduces `2/2`; and the 13C label test repeats the
  same run rather than mutating labels. The checkpoint fingerprint is a
  metadata hash, not a serialized neuron/queue/eligibility checkpoint.
- **Preservation:** the independent focused slice passed `41` tests and the
  full CPU suite passed `255` with `1` existing optional skip. Compile,
  diagnostics and diff checks passed. No dedicated Stage-0 test file exists;
  this is recorded as not applicable rather than claimed as a separate pass.

**Decision:** **PASS WITH FOLLOW-UP — CAUSAL TASK EFFECT VERIFIED, NON-GATING
LIMITATIONS REMAIN**. The narrow supported claim is that, in this bounded
fixture, the edge learned through the verified Luna-13B mechanism causally
improves the fixed external outcome, with targeted removal reducing the
short-case result and exact restoration recovering it. This does not establish
general task utility, random-selection superiority, resource benefit,
scalability, hardware equivalence or biological equivalence. No A01-A15
clause changed, no ACP was created, and Luna-13D remains unauthorized. The
next action is project-owner direction for any follow-up contract, followed by
Luna-0 review.

### Luna-13C corrective evidence pass - 2026-09-29

The corrective pass at revision `685cd721f7ca108278aa2e3044b53d46981e5bbd`
used shared topology-rebuild machinery for sham, a distinct useful edge with
delay `0.5`, independent seeded random selection, and an actual evaluation
label-mutation attack. The corrected artifact records sham graph equality,
positive-control accuracy `2/2`, random seed 0 accuracy `2/2`, random seed 1
accuracy `1/2`, and unchanged structure/pre-output computation under relabeled
targets. Focused corrective validation passed `6` tests; the focused temporal
regression slice passed `42` tests.

The narrow causal task effect remains supported, but random growth reproduces
it for one independent seed. This is therefore `PASS WITH FOLLOW-UP — CAUSAL
TASK EFFECT ESTABLISHED, LIMITATIONS REMAIN`; no A01-A15 clause changed and
Luna-13D remains unauthorized.

### Luna-0 independent corrective re-review - 2026-09-29

The independent re-review synchronized clean `main` at revision
`09995add7643e63f61c45602922238e319965113`, with `HEAD == origin/main`.
The corrective artifact identifies source revision
`685cd721f7ca108278aa2e3044b53d46981e5bbd`, baseline
`ea60610b7ba637e05ee986ffde2864e529a08f2c`, and clean generation state.

The same-path sham was independently instrumented and passed: it rebuilt the
bounded graph through the intervention path, preserved the learned edge and
fingerprint, matched present traces, and scored `2/2`. The learned edge is
`right -> target, 1.0`; the distinct hand-designed positive control is
`right -> target, 0.5` and scored `2/2`. Random seeds independently produced
`right -> target`, `2/2` for seed 0 and `left -> target`, `1/2` for seed 1.
Label mutation preserved structural evidence, decisions, traces, event
counts, and completion state. Present/removal/restoration reproduced
`2/2 -> 1/2 -> 2/2`; only the short case changes, because removing the route
removes its deadline-meeting target arrivals.

The independent targeted bundle passed `124` tests; the full CPU suite passed
`256` with `1` skip; compileall, diagnostics, and diff checks passed; and
temporary artifact regeneration was byte-identical. The named Stage-0 file is
absent, so that check is not applicable; relevant reward, structural,
recurrent, classifier, runtime, Luna-12H, Luna-12N, and Luna-13B tests ran.
The checkpoint remains a metadata fingerprint over fresh reset/rebuild state,
not a serialized queue/eligibility/random-state clone. The two-case fixture
does not establish generalization, efficiency, scalability, hardware
equivalence, or random-growth superiority.

**Decision:** `PASS WITH FOLLOW-UP — CAUSAL EFFECT VERIFIED, BOUNDED
LIMITATIONS REMAIN`. Luna-13D was not created or executed; it is eligible for
later contract creation only by explicit project-owner authorization. The next
scientific boundary is a separately authorized finite-resource utility study
covering pressure, retention/pruning/replacement, and event/energy tradeoffs.

## Luna-13D - Finite-Resource Utility, Retention, and Capacity-Pressure Experiment

**Authorization boundary:**

```text
Luna-0 creates Luna-13D contract
  -> Luna-13D executes under a separate explicit assignment
  -> Luna-0 independently reviews Luna-13D
  -> determine whether any successor is authorized
```

The synchronized Luna-13C corrective review closed at final review revision
`df297c446856d07b2822702202bbb61e81cf38a4`, reviewing corrective source
`685cd721f7ca108278aa2e3044b53d46981e5bbd` in tree
`09995add7643e63f61c45602922238e319965113`. Its result was
`PASS WITH FOLLOW-UP — CAUSAL EFFECT VERIFIED, BOUNDED LIMITATIONS REMAIN`.
The narrow effect is retained; two task cases, one random reproduction,
generalization, efficiency, scalability and full-state checkpointing remain
limited or unproven.

Luna-13D is a CPU-only `EXPERIMENT` and `VERIFICATION` of finite-resource
utility, useful-edge retention, low-value pruning and capacity pressure. It
reuses Luna-13C's fixed external task semantics and causal learned-edge
provenance where practical. It separates task utility from events, queue peak,
proxy energy, latency and edge/capacity cost, and must not call silence
efficient when task utility is lost.

The scope is staged pressure over fan-in, fan-out, total edge capacity,
event/queue capacity and competing useful, distractor, unused and expensive
paths. Stages cover baseline utility, distractor pressure, below/near/full
capacity, declared pruning, post-pruning normal growth and an optional bounded
workload shift. Useful-edge lifecycle, pruning evidence/reasons, graph state,
capacity failures, queue rejections, budget exhaustion, task outcome, events,
proxy energy and latency remain observable. Fixed topology and genuine seeded
random growth are required controls.

Replacement is not automatically authorized. Luna-13D may test an existing
documented and tested atomic replacement policy only if one is already
authorized. Otherwise it is restricted to admission, coexistence, pruning and
later growth after legitimately freed capacity; it must not invent replacement
or a protected-edge lifetime. Any required architecture change returns as an
ACP/decision packet to Luna-0/project-owner review.

Every run requires configured/processed/pending events, queue peak where
available, termination reason and `completed` versus `budget_exhausted`.
Artifacts preserve revisions, fixture, capacity/pruning configuration, seeds,
external target, thresholds and resource units. CUDA is optional and
non-gating. The standard handoff is
`workflow/handoffs/finite-resource-utility-capacity-pressure-Luna-13D.md`.
Results return to Luna-0 for independent review. Luna-13D does not authorize
Luna-13E.

### Luna-0 independent review of Luna-13D - 2026-09-29

Reviewed implementation revision
`f11a44f24fa9ad84e111435ed0ae8390b41c49a6` from a clean synchronized tree
with `HEAD == origin/main`. The contract, implementation, tests, handoff and
both artifacts were present. Independent reproduction confirmed the fixed
external task, baseline/pruning/post-growth metrics, capacity reasons,
budget stability, random seeds, Luna-13C causal matrix, and byte-identical
artifact regeneration.

The Luna-0 review publication revision is `8449562`.

The review separates the findings. The useful `right -> target, 1.0` edge is
task-relevant and remains in the graph after pruning. The graph has three
edges before pruning and one afterward, releasing two actual edge-capacity
slots. `right -> relay` and `relay -> target` are admitted through ordinary
bounded growth without replacement. Baseline and immediate post-pruning both
remain `2/2` at 8 events and proxy energy `8.0`. Post-growth produces duplicate
target arrivals, changes the result to `1/2`, and uses 16 events and proxy
energy `16.0`; this is a utility regression, not an efficiency result.

Capacity accounting is valid: capacity 4 reaches `edge_capacity`, while
capacities 5 and 6 reject the final relay exit for `fan_in_full`. Budgets 24
and 48 reproduce the result. Random seed 0 selects the useful edge and scores
`2/2`; seeds 1-4 select the non-useful edge and score `1/2`. The Luna-13C,
13B, temporal and Stage-0-related regressions remain passing.

The pruning/retention mechanism evidence is invalid. The implementation
passes an endpoint-keyed literal score map to `prune_by_score`; declared
`pruning_utility_threshold` and `pruning_inactivity_threshold` do not control
eligibility. Changing the utility threshold from `0.0` to `100.0` leaves the
same edges pruned, and the fixed node tuple prevents a relabeling attack.
The removals and capacity release are observed, but useful-versus-low-value
local evidence did not cause the decision. The review status is therefore
`BLOCKED — PRUNING/RETENTION EVIDENCE INVALID`.

The next eligible boundary is a separately reviewed correction or experiment
with evidence-derived pruning, meaningful frozen thresholds and identity-
independent checks. Luna-13E is not created or authorized.

### Luna-13D corrective pass - 2026-09-29

The corrective pass started from Luna-0 review publication state
`89de90b183cd54f1ae24f433b6161f1b14c23c0e` and produced implementation
revision `9ae2fb6`. It preserves the independently valid prior findings:
the fixed Luna-13C task, real capacity release, normal post-pruning admission,
capacity rejection reasons, random seed behavior, and post-growth regression
from `2/2` at 8 events to `1/2` at 16 events.

The endpoint-keyed pruning score map was removed. Pruning now records bounded
runtime edge use count, last-use timestamp, inactivity age, observed utility,
observed cost and pruning score. Frozen semantics are:
`inactivity_age >= inactivity_threshold OR observed_utility < utility_threshold`;
inactivity equality is eligible and utility equality is retained. Eligible
edges are selected by lowest observed score, with a bounded maximum of two.
Threshold sweeps, relabeled IDs and mirrored task-source roles show decisions
follow measured evidence rather than endpoint names. The useful edge remains
retained; two zero-use stale edges are pruned and release two slots.

The corrected result is
`PASS WITH FOLLOW-UP — RETENTION/PRUNING ESTABLISHED, USEFUL ADAPTATION NOT
ESTABLISHED`. Resource efficiency remains unproven and relay growth still
degrades the fixed task. The corrected handoff and artifacts return to Luna-0
for independent review. Luna-13E is not created or authorized.

### Luna-0 independent review of corrected Luna-13D - 2026-09-29

Reviewed corrected implementation
`9ae2fb6574a4a45fa6a47c18e9aa7270bd4d3080` from synchronized published tree
`206a3b8463ef857db5e5d5b8d2679d7e877f3bab`. The worktree was clean and
`HEAD == origin/main`; the contract, corrected handoff, implementation, tests
and artifacts were present.

The prior blockers are closed for the tested fixture. Pruning eligibility uses
runtime route use count, last-use timestamp, inactivity age, observed utility
and observed cost; endpoint identity is not an input to the primary Boolean
decision. The declared rule is
`inactivity_age >= threshold OR observed_utility < threshold`, with inclusive
inactivity equality and strict utility inequality. All four OR combinations,
threshold boundaries, arbitrary relabeling and mirrored task-source roles were
independently reproduced. The useful edge is retained from four observed uses;
two zero-use stale edges are pruned and two real slots are released.

The valid prior resource/task distinction remains: baseline and immediate
post-pruning are `2/2`, 8 events and proxy energy `8.0`; relay growth is normal
bounded admission but changes the result to `1/2` at 16 events and energy
`16.0`. Resource efficiency and useful adaptation are not established.

Validation passed: corrected focused `10`, preservation bundle `100`, full CPU
suite `266` with `1` optional skip, compileall, diagnostics and diff checks;
corrected artifact regeneration is byte-identical. Final review status:
`PASS WITH FOLLOW-UP — RETENTION/PRUNING VERIFIED, USEFUL ADAPTATION NOT
ESTABLISHED`. The next question may examine harmful post-pruning admission;
Luna-13E is not created or authorized.

The final Luna-0 review publication revision is
`becf38952fe5c1cf738dd875246b672f82836093`.

### Luna-13E creation - 2026-09-30

The corrected Luna-13D state was independently reviewed with final published
repository state `b7e3bdc6028381a5fa6912c0212aff79528beae1`. The review status
is `PASS WITH FOLLOW-UP — RETENTION/PRUNING VERIFIED, USEFUL ADAPTATION NOT
ESTABLISHED`:

- evidence-based retention/pruning is established, including measured route
  evidence, inclusive inactivity eligibility, strict utility comparison,
  relabeling and mirrored-role preservation;
- useful post-pruning adaptation is not established and resource efficiency is
  not established;
- normal bounded post-pruning growth can degrade the fixed task from `2/2`, 8
  events and energy `8.0` to `1/2`, 16 events and energy `16.0`.

Luna-0 creates Luna-13E, **Post-Pruning Admission Quality and Harmful-Growth
Discrimination Experiment**:

```text
Luna-0 creates Luna-13E contract
  -> Luna-13E executes under a separate explicit assignment
  -> Luna-0 independently reviews Luna-13E
  -> only then determine whether Luna-13F is eligible
```

Luna-13E is a CPU-only experiment and verification of whether existing local,
causal, bounded evidence available before mutation can distinguish a beneficial
candidate from a harmful candidate under true one-slot competition. It must
reproduce the corrected Luna-13D harmful-growth baseline first, freeze
beneficial/harmful ground truth for external evaluation only, and record
field-level pre-admission evidence provenance. Endpoint identity, labels,
future events, future task outcomes and post-hoc oracle information may not
drive admission. Fixed/no-growth and seeded random controls are required.

If current architecture cannot make the distinction without new utility-aware
admission state or another architecture change, Luna-13E must stop and return
an architecture-change decision packet. It must not add a hidden mechanism,
alter pruning, invent probation/rollback or claim utility prediction. CUDA is
optional and non-gating. All applicable boundedness, locality, label-isolation,
determinism and regression checks remain required.

Luna-13E returns to Luna-0 for independent review. It does not authorize,
create or dispatch Luna-13F. No A01-A15 clause or ACP status changes by this
workflow entry.

### Luna-13E independent review - 2026-09-30

Luna-0 independently reviewed Luna-13E at implementation revision
`0a53b01b398d461eac3a962431b9ffcdae459e55`, based on synchronized published
revision `dd241ec9ee7af7456ae70bae2192d4237dab5d21` and the corrected artifact
  metadata committed during review. The review package revision is
  `7faf8d3f1c82927304875bb6263219d5954a463d`. The review status is:

**PASS WITH FOLLOW-UP — HARMFUL GROWTH AVOIDED, GENERALITY NOT ESTABLISHED**

- G and H were individually legal at the same decision point with exactly one
  relevant free edge slot. The canonical scorer used local `CandidateEvidence`
  scores `3.0` and `0.0`, selected G, and remained independent of candidate
  presentation order, relabeling and mirrored endpoint roles.
- Independent held-out replay measured no-growth `2/2` with 8 events and
  proxy energy `8.0`, G `2/2` with 12 events and proxy energy `12.0`, and H
  `1/2` with 12 events and proxy energy `12.0`. G therefore preserved task
  utility while avoiding the harmful candidate; it did not improve the task
  over no-growth and was not resource-efficient relative to no-growth.
- Equalized evidence selected by deterministic tie-breaking only. Future-event
  and external-label mutation controls preserved the admission decision.
  Reward, prediction/error and predicted total-cost evidence were unavailable;
  propagation delay was available but not used in the score.
- The score-driving observations are a bounded controlled fixture, not a
  demonstrated general runtime predictor. General utility prediction,
  workload-shift robustness, resource efficiency and hardware equivalence
  remain unestablished. Current admission still has no abstention threshold;
  no utility-aware production mechanism was added.
- The stale frozen H metadata (`0/2`) was corrected to the observed `1/2` in
  the review revision. No A01-A15 clause changed, no ACP was required, and
  Luna-13F remains unauthorized. A successor may be considered only after a
  separate project-owner authorization.

### Luna-13F creation - 2026-09-30

The final synchronized reviewed state is
`8c41267e47bc0543ff9f05e994dc7ea086b23e36`. Luna-13E's independent review
package is `7faf8d3f1c82927304875bb6263219d5954a463d`, reviewing corrected
implementation `0a53b01b398d461eac3a962431b9ffcdae459e55`. The review status
is **PASS WITH FOLLOW-UP - HARMFUL GROWTH AVOIDED, GENERALITY NOT
ESTABLISHED**.

The review established only that fixture-controlled bounded observations
selected G over H in the tested one-slot fixture. No-growth remains `2/2` at
8 events and energy `8.0`; G remains `2/2` at 12 events and energy `12.0`; H
remains `1/2` at 12 events and energy `12.0`. G therefore avoids harmful
growth but provides neither task improvement nor resource benefit over
no-growth. Runtime-generated candidate evidence remains unestablished.

Luna-0 creates Luna-13F, **Runtime-Generated Local Candidate Evidence
Experiment**:

```text
Luna-0 creates Luna-13F contract
  -> Luna-13F executes under a separate explicit assignment
  -> Luna-0 independently reviews Luna-13F
  -> only then determine whether Luna-13G is eligible
```

Luna-13F is CPU-only and asks whether ordinary runtime neuron/event activity
generates bounded, candidate-specific local evidence before admission. The
primary chain is runtime events -> local state -> accumulated evidence -> the
unchanged canonical scorer -> true one-slot decision -> held-out outcome.
Fixture-keyed score tuples, G/H lookup tables, candidate-role flags,
experiment-side timing or score injection, labels, future outcomes and
endpoint-oracle evidence are prohibited. Candidate identifiers may index
bounded state but may not determine evidence values.

The contract requires runtime provenance, evidence timestamps no later than
the decision, bounded state and reset/eviction semantics, matched G/H
exposure, temporal controls, relabeling, mirrored roles, future/label
isolation, candidate-order independence and no-growth reporting. The current
architecture must be audited first. If existing mechanisms cannot generate
the evidence, Luna-13F must stop and return an architecture-change decision
packet; it may not silently add a learning subsystem or new candidate
semantics. CUDA is optional and non-gating.

Luna-13F returns to Luna-0 for independent review. No A01-A15 clause changes,
no ACP is created by this workflow entry, and Luna-13G is not authorized.

### Luna-13F execution authorization - 2026-09-30

Luna-0 reviewed the committed Luna-13F contract and prerequisite evidence at
authorization baseline `4f4129f3d9eda736fe1c2434b79e21d387e2fedc`. The
repository was synchronized with `origin/main`, on `main`, and clean with
`HEAD == origin/main`.

The prior Luna-13B causal crossover, Luna-13C bounded external causal effect,
corrected Luna-13D evidence-based retention/pruning, and Luna-13E harmful-
growth-avoidance review gates are sufficiently closed for this bounded
follow-up. Luna-13E's remaining limitation is the use of fixture-controlled
score-driving observations rather than demonstrated organically runtime-
generated candidate evidence.

**AUTHORIZED - LUNA-13F EXECUTION PENDING.** Luna-13F may now execute from
authorization revision `4f4129f3d9eda736fe1c2434b79e21d387e2fedc` or a later
synchronized revision containing no incompatible architecture or workflow
changes. The authorized question is whether ordinary event-driven runtime
activity generates bounded candidate-specific local evidence for the unchanged
canonical scorer under true one-slot competition.

The primary decision remains prohibited from using fixture-keyed G/H scores,
candidate-role tables, endpoint-specific tuples, expected-winner metadata,
labels, held-out outcomes, or experiment-side score injection. The existing
architecture must be audited first; if it cannot generate sufficient evidence,
Luna-13F must stop with its architecture-change decision packet and must not
add production semantics silently. Execution remains CPU-only; optional CUDA
skips are non-gating. Luna-13F must return to Luna-0 for independent review.
Luna-13G remains unauthorized.

### Luna-13F independent review - 2026-09-30

Luna-0 independently reviewed the completed Luna-13F implementation at
`0ba668ebe6cccd52fb0953638e1159090a79221e` after refreshing `origin/main`.
The review was performed on `main`; `HEAD` was one commit ahead of
`origin/main` (`f0821bd5eb0441ea892c463cbbcf173c80d09be6`), and the worktree
was clean before review edits.

The terminal status is:

**BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION CONFIRMED**

The earliest invalid dependency is the Luna-13F `_schedule` path: it uses
`beneficial_role` and `harmful_role` to assign three short candidate events to
G and one long event to H. The runtime neuron and bounded temporal policy are
real, and the unchanged canonical scorer is called, but the informative value
is assigned by the experiment fixture before runtime processing. The review
also confirmed that post-decision events change the accumulated score and
admission, held-out route timestamps begin before the decision, and an
event-budget-exhausted run can still admit G with pending events.

The existing architecture is **partially sufficient**: bounded local policy
state, neuron state and the canonical scorer already exist. No architecture
change or ACP is required by this review. The implementation may receive a
separately authorized corrective pass under the existing contract:

**LUNA-13F CORRECTIVE PASS ELIGIBLE UNDER EXISTING CONTRACT**

This eligibility does not authorize execution. The corrective scope must use
matched non-role-authored exposure, freeze pre-admission evidence, place
held-out execution strictly later, reject incomplete runs for scientific
admission, and complete the required controls. The original unqualified 13F
artifact pair lacks a terminal-status field; the verified artifact pair and
resumption audit truthfully report the blocked status. A01-A15 and ACP status
remain unchanged. No corrective work was executed by this review, and
Luna-13G remains unauthorized.

### Luna-13F corrective execution authorization - 2026-09-30

Following the independent review above, Luna-0 explicitly authorizes a
corrective Luna-13F pass under the existing `.github/agents/luna-13f.agent.md`
contract. This is a corrective execution boundary, not a new Luna contract,
architecture promotion or successor authorization.

The authorized corrective scope is limited to the identified experiment
violations: remove beneficial/harmful-role knowledge from evidence scheduling;
freeze evidence before the structural decision; place held-out events after
the decision in actual timestamps; reject incomplete-budget admissions;
construct a genuine runtime-generated evidence-equalization control; and run
the required missing or invalid controls. Controlled event schedules remain
allowed when they do not encode later held-out usefulness.

The corrective pass must not add utility memory, probation, rollback,
speculative edges, a reward channel, global task utility, an oracle cost
predictor, global candidate history, protected candidate classes or new
architecture semantics. If an existing mechanism is insufficient, Luna-13F
must stop and return **BLOCKED - ARCHITECTURE CHANGE REQUIRED FOR RUNTIME
EVIDENCE**. A positive result is not required; ties, non-predictive evidence
and negative results are valid outcomes. The first Luna-13F execution remains
blocked, the architecture remains unchanged, and Luna-13G remains
unauthorized.

The next action is Luna-13F corrective execution, followed by another
independent Luna-0 review. No corrective Luna-13F execution was performed as
part of this authorization/publication task.

### Luna-13F corrective independent review - 2026-09-30

Luna-0 independently reviewed corrected implementation revision
`dcee582fa8fb347f578793c2ef383bd936e83234` on synchronized `main` with
`HEAD == origin/main` and a clean worktree at review start. The committed
focused output reports 10 passed, the preservation output reports 62 passed,
and the full CPU output reports 286 passed with 1 skipped. No experiment was
rerun after the user froze execution.

The terminal status is:

**BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION**

The schedule body is neutral with respect to the two role fields, but the
complete dependency chain is not. `_candidate_edges()` maps G to
`beneficial_role`, `_base_edges()` uses the same role mapping, and held-out
topology construction reuses those helpers. Therefore the short-association
motif is still assigned to the endpoint already designated useful by the
fixture. The reported 4.0/0.0 values are bounded source-local
`TemporalAssociationPolicy` association counts, not independent utility
evidence. The required A/B blinding and valid mirrored-role test were not run.

The five audit not-run items are all classified **REQUIRED BUT MISSING**:
external-label mutation, locality attack, neutral-decay sweep,
candidate-saturation/reset/eviction, and valid mirrored roles. The audit's
13 passed, 0 failed, 5 not-run total therefore cannot support a scientific
PASS, and its role-dependency check inspected only `_schedule`.

The artifact also records executed revision `3379403a8b58649a85c2604ba3044e55e4fe99e9`,
not the corrected commit under review. The held-out timestamps are hard-coded
metadata while route traces reset at 0.0, so cross-phase chronology is not
independently established. No A01-A15 clause changed and no ACP is required.
The existing runtime may be sufficient for a later corrected experiment, but
that requires explicit project-owner authorization and another Luna-0 review.
Luna-13G remains unauthorized.

### Luna-13F blinded-mapping corrective authorization - 2026-09-30

Following the independent review above, Luna-0 authorizes **one additional
Luna-13F corrective pass under the existing `.github/agents/luna-13f.agent.md`
contract**. This is an experiment-level authorization only: it does not create
a new Luna-13F contract, execute the experiment, change A01-A15 or authorize
Luna-13G.

The current partial result is preserved: ordinary runtime activity generates
bounded source-local association evidence and the unchanged canonical scorer
consumes it. The remaining blocker is the pre-evaluation mapping
`beneficial_role -> candidate/topology assignment -> G`. The corrective pass
must remove `beneficial_role` and `harmful_role` from every candidate endpoint,
base topology, neutral schedule, ordering, evidence and scoring path. Those
fields may remain only in post-hoc utility reporting.

Use neutral candidate identities such as `candidate_A` and `candidate_B`,
freeze a predeclared seeded mapping before held-out evaluation, and run at
least two independent endpoint/motif permutations with identical schedule
generation. Compute runtime evidence, canonical scores and admission before
assigning task-preserving or task-harming descriptions. Preserve the valid
runtime-events -> bounded association-state -> canonical-score chain and
identify whether 4.0/0.0 is caused by count, interval, ordering, decay or
another canonical state variable.

The five outstanding audit controls remain mandatory unless the existing
contract independently demonstrates conditional inapplicability:
`external_label_mutation`, `locality_attack`, `neutral_decay_runtime_sweep`,
`candidate_saturation_reset_eviction` and `valid_mirrored_roles`. The pass must
return complete artifacts and validation to Luna-0 for independent review.
No architecture change is currently required. If the blinded experiment
requires new runtime semantics, it must stop with the authorized architecture-
change status and decision packet. Luna-13G remains unauthorized.

### Luna-0 independent review of blinded-mapping corrective Luna-13F - 2026-09-30

Luna-0 independently reproduced the reported P0/P1 decisions and held-out
outcomes from the dirty corrective worktree. The focused suite passed 10 tests
and the preservation slice passed 62 tests, but the review found that the
required information-boundary controls are not independently executed.

- P0 maps `candidate_A` to `relay` and selects it with runtime evidence
  `4.0` versus `0.0`; its held-out result is `2/2`.
- P1 maps `candidate_A` to `noise` and applies the same short/long motif rule;
  it selects the same neutral candidate and its held-out result is `1/2`.
- The runtime association count and canonical scorer chain are reproduced, but
  `external_label_mutation` and `locality_attack` are declarative artifact
  fields rather than mutation attacks. Future events are sliced out before
  execution, and held-out timestamps are hard-coded metadata over a fresh
  time-zero evaluator rather than one continuous runtime chronology.
- No complete contract-audit artifact exists for the corrected run. The
  saturation control demonstrates bounded rejection/reset, but not eviction;
  the budget tests cover an incomplete run, not the required boundary matrix.

Final review status: **BLOCKED - REQUIRED CONTRACT CONTROLS NOT EXECUTED**.
The raw execution remains a negative utility-prediction result, not a verified
Luna-13F closure. No A01-A15 clause or ACP status changed, no architecture
change is authorized, and Luna-13G remains unauthorized. A separately
authorized evidence-control repair is required before closure; do not add a
utility predictor or issue Luna-13G from this review.

### Luna-13F contract-control completion authorization - 2026-09-30

Luna-0 published the independent blinded-experiment review at revision
`c05015527063053ee789d0fc19ae21a02627f319`. The review independently
reproduced the central negative result: evidence-driven `candidate_A` was
selected in both mappings, with held-out results P0 `2/2` and P1 `1/2`.
The scientific observation remains valid but is not yet contract-closed.

The terminal review status is:

**BLOCKED - REQUIRED CONTRACT CONTROLS NOT EXECUTED**

Luna-0 authorizes exactly one narrowly scoped Luna-13F contract-control
completion pass under the existing `.github/agents/luna-13f.agent.md`
contract. This authorization covers only testing, experiment orchestration,
instrumentation and truthful artifact accounting. It does not create a new
Luna-13F contract, execute Luna-13F, change A01-A15, require an ACP, or
authorize Luna-13G.

The corrective pass must execute and independently evidence:

1. Continuous chronology for pre-admission evidence, evidence completion,
  freeze, score, decision, admission and held-out events, including queue
  state and an adversarial event-at/before-boundary chronology attack.
2. External-label mutation using otherwise identical executions, with exact
  mutated metadata and equality of all pre-held-out computational fields.
3. Per-field evidence provenance and an adversarial locality attack proving
  prohibited private state, labels, held-out metadata and unrelated global
  metadata cannot change raw local evidence.
4. The actual bounded candidate-state container, declared capacity and
  lifecycle semantics, plus saturation and reset/expiry/eviction-or-rejection
  tests and stale-state reuse.
5. Budget-boundary runs at `B-1`, `B`, `B+1` and a substantially larger budget,
  with incomplete runs barred from valid admission and completed decisions
  stable at larger budgets.
6. A complete machine-readable and human-readable contract audit. Every
  requirement must be `PASS`, `FAIL`, or
  `NOT APPLICABLE - CONTRACT CONDITION NOT TRIGGERED`, with an exact reason
  for conditional inapplicability and no unexplained mandatory `NOT RUN`.

The pass must retain final evidence for neutral decay, valid mirrored roles,
no-evidence, equalization, candidate-order reversal, future exclusion,
relabeling and deterministic replay. It must regenerate `results.json`,
`summary.json`, `audit-results.json` and the Luna-13F handoff so all mappings,
scores, selections, outcomes, chronology, isolation results, bounds, budget
status and terminal status agree. It must run the focused controls, the
Luna-13F preservation matrix, Luna-13E, corrected Luna-13D, Luna-13C,
Luna-13B, Stage-0, relevant Luna-12H/Luna-12N checks, the full CPU suite,
compile/static checks, diagnostics and `git diff --check`, recording exact
counts. This task performs none of those experiment executions.

The P0/P1 mapping, runtime evidence semantics and canonical scorer remain
unchanged unless a genuine contract defect requires correction. Any change
capable of changing the central result requires re-execution of both mappings
and disclosure of the prior result. No utility memory, probation, rollback,
speculative edge, reward channel, global utility state, oracle predictor or
new persistent learning subsystem is authorized. If a control requires one,
stop with **BLOCKED - ARCHITECTURE CHANGE REQUIRED** and return a decision
packet to Luna-0 and the project owner.

After execution, Luna-13F must return to Luna-0 for final independent closure
review. A negative result remains an acceptable successful scientific outcome;
the expected terminal interpretation, if controls pass and P0/P1 remain
`2/2` and `1/2`, is **NEGATIVE RESULT - RUNTIME EVIDENCE GENERATED BUT DOES
NOT PREDICT USEFUL GROWTH**. Luna-13G remains unauthorized.

## Luna-13F final independent closure review - 2026-09-30

Luna-0 independently reviewed the synchronized implementation at
`2b2432dabd49ecacceef525e8e3e68b909ee09c3`, the generated artifacts, the
contract audit, the execution handoff and the runtime control code. The raw
blinded result reproduces: P0 selects `candidate_A` and obtains `2/2`; P1
selects `candidate_A` and obtains `1/2`. The score is a bounded source-local
temporal-association count (`4.0` versus `0.0`), and neutral decay changes
local neuron state without changing score or rank. No-growth remains `2/2`
with 8 events and `8.0` uncalibrated activity-cost-proxy units; selected P0
growth remains `2/2` with 12 events and `12.0` units.

The negative observation is scientifically informative, but closure is blocked.
The declared future-event control appends an event and then removes it before
runtime execution (`events[:16]`); the chronology attack is a timestamp
predicate rather than an injected runtime event; and the locality attack passes
metadata that the runtime path does not read. Consequently the audit's three
corresponding PASS claims are not executed evidence. The aggregate `26 PASS,
0 FAIL, 2 NOT APPLICABLE` is therefore invalid as a closure audit.

Final status: **BLOCKED - CONTRACT AUDIT INVALID**. The two N/A entries are
valid only as conditional lifecycle cases: candidate expiry is not a mechanism
of the canonical policy, and eviction is not triggered because full capacity
uses explicit rejection. No A01-A15 clause changed, no ACP was created, and no
architecture mechanism or successor was authorized. Luna-13G remains
unauthorized. A future assignment would require a separately authorized
control repair and another independent Luna-0 review.

## Luna-13F runtime-attack corrective authorization - 2026-09-30

Following the final independent review at implementation/review baseline
`2b2432dabd49ecacceef525e8e3e68b909ee09c3`, Luna-0 authorizes exactly one
narrow corrective pass under the existing `.github/agents/luna-13f.agent.md`.
The authorization repairs only the invalid runtime controls: live future-event
injection after admission, queued chronology-boundary attacks, and a locality
attack that mutates genuinely accessible prohibited state. It does not execute
Luna-13F during this publication task.

The P0/P1 fixture, bounded source-local association-count mechanism and
canonical scorer remain unchanged unless a genuine runtime defect is found. The
corrective run must preserve or disclose any changed P0/P1 result, regenerate
all artifacts and the audit, and return to Luna-0. The two prior N/A cases
(unsupported expiry and deterministic full-capacity rejection rather than
eviction) remain valid; no expiry or eviction implementation is authorized.

The corrective pass may not add utility memory, reward pathways, probation,
rollback, speculative edges, global utility state, new candidate semantics,
architecture changes or an ACP. If valid future exclusion requires new
production architecture semantics, stop with **BLOCKED - ARCHITECTURE CHANGE
REQUIRED**. Luna-13G remains unauthorized, and a final Luna-0 closure review is
mandatory after the corrective artifacts.

## Luna-13F final independent closure - 2026-09-30

Luna-0 independently closed Luna-13F at review publication revision `e595a9f`
from implementation and artifact revision `83266f92d750939ef0b9904073e9f75badc35fbb`, with `HEAD ==
origin/main` and a clean synchronized review start. The corrected runtime
controls were reproduced rather than accepted from aggregate totals.

- P0 selects neutral `candidate_A` and obtains `2/2`; P1 selects neutral
  `candidate_A` and obtains `1/2`.
- Runtime evidence is a bounded source-local temporal-association count
  (`4.0` versus `0.0`). Neutral decay changes local state but not score,
  rank or selection.
- The same runtime processes the future continuation; live losing-candidate
  evidence changes `0.0 -> 5.0`, while frozen historical admission and
  topology remain unchanged.
- Actual queued before-decision and equal-time held-out events invalidate
  chronology; the strictly later event is accepted. Mutating real
  candidate-B private score state leaves candidate-A evidence unchanged.
- Candidate bounds, reset/stale-state reuse, budget threshold, label
  isolation, mirroring, equalization, no-evidence and deterministic replay
  pass. Expiry and eviction remain valid conditional N/A cases because the
  policy has no expiry path and deterministically rejects at full capacity.
- The complete audit is `26 PASS / 0 FAIL / 2 valid N/A`. Focused validation
  is `15 passed`, preservation is `72 passed`, and full CPU validation is
  `291 passed, 1 skipped`.

The terminal scientific result is **NEGATIVE RESULT - LUNA-13F RUNTIME
EVIDENCE DOES NOT PREDICT USEFUL GROWTH, INDEPENDENTLY VERIFIED AND CLOSED**.
Proposition 1 (bounded runtime evidence) and Proposition 2 (canonical
admission effect) are supported in the tested fixture; Proposition 3
(prediction of held-out useful growth) is not supported. No-growth remains
`2/2 @ 8` events and proxy `8.0`; selected P0 growth is also `2/2` at 12
events and proxy `12.0`, so no resource benefit is established. No A01-A15
change or ACP is required. **LUNA-13F CLOSED - SUCCESSOR NOT AUTHORIZED**;
Luna-13G remains unauthorized.

### ACP-0002 architecture review - 2026-09-30

The project owner requested an architecture reorganization beginning at the
neuron/edge signal path after Luna-13F closed with a negative result. Luna-13F
remains closed and its result is not being repaired or reinterpreted.

Luna-0 created ACP-0002, **Independent Edge Signal Transformation and Neuron
Gain Separation**, at synchronized revision
`25aa7697d523c13f0fdcf56c84170ceb553cc229`. The proposal was initially **Under
review**: it defined a bounded edge efficacy `w`, divider strength `d`,
independent logical reference `r`, fixed edge transfer `tanh`, positive edge
delay and a separate destination-neuron gain. It preserves A01-A15 and does
not define an edge learning rule, probation/maturation mechanism or local
time-series predictor.

This is a material canonical signal-path and ownership proposal, therefore an
ACP is required. Following the focused mathematical review, the subtraction
form was rejected because `d=0` erased the independent reference. ACP-0002 now
selects the Model B interpolation `v=d*tanh(w*a)+(1-d)*r` and is **Accepted for
staged implementation**. Only N1, edge/neuron data model and compatibility
representation, is authorized; N2 transfer execution and all adaptive or
temporary-edge mechanisms remain unauthorized. Luna-13G remains unauthorized.

N1 must preserve bounded `w`, `d`, `r` and `neuron_gain`, provide explicit
legacy identity compatibility, and add no production transfer execution or
learning. N1 returns to Luna-0 for verification before any later stage.

### Luna-15 ACP-0002 Stage N1 contract creation - 2026-09-30

Luna-0 creates and authorizes `.github/agents/luna-15.agent.md`, **Luna-15 -
ACP-0002 Edge/Neuron Data Model and Compatibility**, at the published
authorization revision recorded in its creation handoff. ACP-0002 remains
**Accepted for staged implementation**.

Luna-15 is authorized for exactly **N1 - edge/neuron data model and
compatibility representation**:

- edge-owned `edge_weight` / `w_ij` in `[-2,2]`;
- edge-owned `divider_strength` / `d_ij` in `[0,1]`;
- edge-owned `reference` / `r_ij` in `[-1,1]`;
- existing positive finite propagation delay;
- neuron-owned `neuron_gain` / `g_j` in `[0,2]`;
- legacy constructor, structural-plasticity, deterministic replay and
  observer/instrumentation compatibility;
- analytic and regression tests proving representation compatibility.

The future accepted Model-B equation is documented by ACP-0002 but **must not
be activated in N1**. N1 must not change routed payload semantics, event
identity, timestamps, sequence ordering or delay behavior. N1 completion does
not automatically authorize N2; Luna-15 must return to Luna-0 for independent
review before any later stage is considered.

Luna-15 is explicitly prohibited from N2 propagation changes, adaptive edge
learning, temporary/probationary connections, edge maturation, local
time-series mini-NNs, new utility-learning mechanisms, A01-A15 changes,
hardware implementation, reopening Luna-13F or authorizing Luna-13G. Luna-13F
remains **CLOSED**, Luna-13G remains unauthorized, and A01-A15 remain
unchanged.

## Luna-13 — GPU-Compatible Visualization Path

**Authorization:** Blocked until Luna-12 passes and Luna-0 explicitly authorizes this milestone. The prompt or handoff alone is not authorization.

**Purpose:** Produce semantically compatible GPU visualization records using the Luna-12 format.

**Scope:** Use no GPU-specific schema; implement GPU snapshot/export support; evaluate device buffers, periodic capture, double buffering, or host transfer as appropriate; add CPU/GPU parity and visualization-on/off invariance tests; consume records with Luna-12 tooling; and document synchronization/performance implications without making performance an architecture contract.

**Explicit non-goals:** Do not alter neuron updates, event ordering, propagation, topology, reward, classifier, bounded state, or synchronization semantics. Do not implement ModelSim, FPGA, VGA, or Ethernet visualization.

**Expected handoff:** A GPU exporter producing records semantically consumable by the Luna-12 parser/visualizer.

**Completion gate:** Record CPU/GPU parity and non-interference evidence. This milestone does not authorize Luna-14.

## Luna-14 — ModelSim/FPGA Trace Bridge and DE1-SoC Visualization Foundation

**Authorization:** Blocked until Luna-12 passes and Luna-0 explicitly authorizes this milestone. Luna-13 is an optional parity reference, not a prerequisite.

**Purpose:** Bridge the canonical format into ModelSim and downstream FPGA diagnostic infrastructure for the Terasic DE1-SoC.

**Scope:** Implement deterministic ModelSim-compatible hex/binary framing and ordering; define HDL X/Z/unknown handling and reset/snapshot boundaries; decode known traces with reference tooling; define a downstream-only FPGA diagnostic stream with non-blocking overflow/drop reporting; establish VGA as the preferred first local display path; and retain Ethernet as a later richer host path without adding a full stack solely for this milestone.

**Explicit non-goals:** Do not redefine the Luna-12 format, inject events, modify topology/classifier/reward/core reset semantics, make visualization backpressure computational backpressure, or claim hardware equivalence.

**Expected handoff:** A ModelSim trace bridge, hardware diagnostic interface, and DE1-SoC visualization foundation suitable for later VGA and Ethernet expansion.

**Completion gate:** Record trace-decoding, reset-boundary, overflow/non-blocking, and downstream-only evidence. Removing visualization must leave TPCN behavior unchanged.

---

## Current numbering reconciliation and Luna-18 H1

The current role assignments supersede older planning reservations while
preserving those records below as historical context:

| Luna | Current role | Status |
|---|---|---|
| Luna-15 | ACP-0002 N1 edge/neuron data model and compatibility | completed historical implementation |
| Luna-16 | ACP-0002 N2 static Model-B edge transfer | CLOSED |
| Luna-17 | hardware-equivalence / cross-backend hardware acceptance | RESERVED / NOT AUTHORIZED / NO ACTIVE CONTRACT |
| Luna-18 | ACP-0003 H1 Execution IR and backend interface skeleton | CLOSED / independently verified |
| Luna-19 | ACP-0004 E1 canonical single-excursion neuron | CLOSED / independently verified |
| Luna-20 | ACP-0005 TPCN-IR-2 excursion execution schema | CLOSED / independently verified |
| Luna-21 | ACP-0004 E2 multi-excursion return runtime | CLOSED / independently verified |
| Luna-22 | ACP-0006 first CPU software-reference excursion integration | CLOSED / INDEPENDENTLY VERIFIED (bounded fixed-topology EXCURSION_V1 CPU integration) |
| Luna-23 | ACP-0004 E2 positive-delay logical-time representability correction | CLOSED / INDEPENDENTLY VERIFIED |
| Luna-24 | ACP-0006 integrated IR-2 residual-provenance boundary correction | CLOSED / INDEPENDENTLY VERIFIED |
| Luna-25 | ACP-0006 sequential dataset evidence reproducibility | CLOSED / INDEPENDENTLY VERIFIED (`luna25-v1` only) |
| Luna-30 | TPCV-2 detached replay consumer compatibility correction | CLOSED / INDEPENDENTLY VERIFIED (downstream compatibility only) |

The following review records preserve the chronology of previously published
gate findings. Later corrections and the final current Luna-22 closure
decision are recorded after those historical findings below.

Luna-19, Luna-20 and Luna-21 are closed component implementations; this does
not itself establish experiment-path integration. **OBSERVED:** the ordinary
experiment path at the ACP-0006 baseline constructs `TPCNNeuron` instances
and uses scalar activations for routing, prediction and readout, while E1/E2
excursion runtimes and IR-2 remain separate reference components.

The project owner accepted ACP-0006, **Excursion Runtime Integration and
Migration Contract**, as written at published proposal revision
`7eb997ebcb78f5a64074cd27a7a6181dbf693fa3` on 2026-10-03. The architecture
decision and final dispatch-readiness review found no internal contradiction
requiring new canonical behavior: prediction matching retains bounded FIFO
semantics; prediction errors remain opaque routed metadata; eligibility and
reward identify bounded traces; the classifier consumes actual emissions
while the existing outer prototype path uses its bounded signed-payload mean;
settling, sidecar/provenance bounds, proxy-energy counters and quiescent IR-2
startup are all implementable using explicit configuration and existing
interfaces. Dataset selection remains an implementation/reporting choice
under the existing open sequential-dataset protocol, not a new core semantic.

Luna-22 implemented and published the first CPU software-reference
integration at `a206f2e8fec8f0c72d9196b2bcca9d2e734c7974`. Luna-0's second
independent review is **BLOCKED / NOT CLOSED**: it reproduced an E2
positive-delay representability failure in valid temporal workloads and found
that integrated IR-2 startup still accepts assigned residual provenance and
sticky provenance truncation. The reported UCI Character Trajectories subset
also lacks a retained loader/split script and per-class results. The exact
review evidence is in
`workflow/handoffs/luna-0-second-independent-review-ACP-0006-Luna-22-20261003.md`.
No downstream visualization or research consumer migration is authorized.

Luna-23's bounded E2 strict-future representability correction is
**CLOSED / INDEPENDENTLY VERIFIED** under ACP-0004. The independent review
confirmed both polarities, finite strictly increasing local timestamps,
preserved configured-delay rejection, unchanged E1 and IR-2 behavior, and
removal of all seven E2 representability exceptions as their original failure
cause. The review and evidence are in
`workflow/handoffs/luna-0-independent-review-luna-23-e2-time-representability-20261003.md`.
This does not close Luna-22.

Luna-24 rejected assigned residual provenance and sticky truncation only at
the ACP-0006 integrated IR-2 startup boundary. Luna-0 independently verified
the published implementation, standalone E2/IR-2 preservation, schema
revision 1, clean startup, identity continuity, and the complete applicable
regression set. Luna-24 is **CLOSED / INDEPENDENTLY VERIFIED**; its evidence is
in
`workflow/handoffs/luna-0-independent-review-luna-24-ir2-provenance-20261003.md`.
Luna-23 remains **CLOSED / INDEPENDENTLY VERIFIED**. Neither correction
changes A01-A15, ACP-0004, ACP-0006 or IR-2 schema revision 1, and neither
authorizes visualization, structural-plasticity, dataset or benchmark-consumer
migrations.

Luna-22 remains **IMPLEMENTED / BLOCKED / NOT CLOSED**. A fresh
closure-readiness review verified a concrete remaining core defect: an actual
matched `PredictionError` reaches the first downstream node but is re-routed
from the original source and never reaches a reachable second hop, contrary
to ACP-0006 rule 6. This is the sole identified Luna-22 core correctness
blocker; the review does not close Luna-22.

Luna-23 and Luna-24 remain **CLOSED / INDEPENDENTLY VERIFIED**. Luna-25
remains **CLOSED / INDEPENDENTLY VERIFIED** for reproducibility of the new
`luna25-v1` dataset/split/results only; it did not reconstruct the historical
Luna-22 split. Focused evidence confirms local causal prediction/error
matching and positive-delay delayed-credit attribution work. Luna-25's zero
matched predictions/errors/credit, low classification accuracy and the
unreconstructable old split are respectively task-efficacy and
historical-evidence observations, not further integration correctness gates.
No accuracy threshold or efficacy requirement is added.

The full CPU suite was rerun: 24 failures, 796 passes, one CUDA-unavailable
skip, 821 collected. All 24 failures were individually inspected and
classified as downstream visualization, structural-experiment,
legacy-observable, temporal/spiral analysis or viewer compatibility
assumptions. They do not block Luna-22 under the fixed-topology EXCURSION_V1
contract and the existing requirement to run/report (not blanket-repair) the
full suite. No downstream migration is authorized by this review.

Luna-26 is **AUTHORIZED / NOT EXECUTED** solely to correct and test hop-local
opaque prediction-error forwarding in the Luna-22 integration adapter. Its
contract is `.github/agents/luna-26.agent.md`; its authorization record is
`workflow/handoffs/luna-0-authorization-luna-26-prediction-error-multihop-routing-20261003.md`.
The full closure-readiness evidence, including exact suite-failure matrix and
A01-A15 assessment, is
`workflow/handoffs/luna-0-acp-0006-luna-22-closure-readiness-20261003.md`.
Luna-26 must not change topology APIs, ACP-0006, canonical behavior or
downstream consumers, and does not itself close Luna-22. Luna-0 must
independently review its completion before reconsidering closure.
This fresh classification supersedes earlier wording that treated dataset
efficacy or all 24 downstream compatibility failures as Luna-22 core gates.

The independent Luna-0 review of the published Luna-26 correction found a
separate ACP-0006 rule-3 violation. On `n0 -> n1 -> n0`, the error return
event is queued and processed with route path `("n0", "n1", "n0")`; the
destination guard suppresses it only after the prohibited revisit has
occurred. Luna-26 is therefore **BLOCKED — ROUTE-PATH NO-REVISIT INVARIANT**,
and Luna-22 remains **IMPLEMENTED / BLOCKED / NOT CLOSED**. The independent
review and exact trace are recorded in
`workflow/handoffs/luna-0-independent-review-luna-26-prediction-error-routing-20261003.md`.

Luna-0 has authorized a bounded corrective pass under the existing Luna-26
identifier. The current topology API can route only the complete outgoing
fan-out, so it cannot omit a path-revisiting edge while retaining other legal
outgoing edges and atomic queue-capacity preflight. The corrective pass may
add one optional, default-preserving destination-exclusion argument to
`BoundedTopology.route()` and apply the current error event's `route_path`
only to that event's route. This must not become a global visited set; the
existing per-destination guard remains necessary for convergent paths.
The new authorization is
`workflow/handoffs/luna-0-authorization-luna-26-corrective-route-path-20261003.md`,
and the Luna-26 agent contract records its exact narrow override. No ACP,
A01-A15, Model-B equation, delay, credit, dataset or downstream-consumer
change is authorized. Luna-0 must independently review this corrective pass
before any Luna-22 closure decision.

The authorized same-Luna correction added optional, backward-compatible
destination exclusions to `BoundedTopology.route()` and uses only the
current prediction-error route path to omit revisits before queue admission.
Independent Luna-0 review confirmed that the cycle return is never queued,
legal outgoing fan-out remains available, and convergent duplicate suppression
is preserved. Luna-26 is **CLOSED / INDEPENDENTLY VERIFIED** for this bounded
correction. Luna-22 is now **CLOSED / INDEPENDENTLY VERIFIED** for the
accepted first fixed-topology `EXCURSION_V1` CPU software-reference
integration only. The final closure evidence and exact validation appear in
`workflow/handoffs/luna-0-independent-review-luna-26-prediction-error-routing-20261003.md`.

The independent Luna-26 review reran the focused integration suite (**49
passed**), prescribed ACP-0006 regression plus focused suite (**340
passed**), full CPU suite (**24 failed, 802 passed, 1 skipped**), and test
collection (**827**). Failure identities remain in the previously classified
downstream compatibility groups. The additional cycle invariant is an
owned blocker resolved by the reviewed corrective pass; it was not one of
those downstream failures. The corrective review recorded topology plus
integration **60 passed**, the prescribed ACP-0006 regression set **342
passed**, full CPU suite **24 failed, 804 passed, 1 skipped**, and **829
collected**. The 24 downstream compatibility failures remain a separate
backlog and do not undo this bounded core closure. Luna-25's zero dataset
prediction/error/credit matches and low accuracy remain task-efficacy
observations, not routing defects.

Closure does not establish predictive efficacy, useful delayed-credit
learning, downstream consumer migration, integrated structural plasticity,
historical Luna-22 split reconstruction, writer-disjointness,
hardware/backend equivalence, calibrated physical energy, or repository-wide
architecture completion. No consumer migration was authorized. The next
governance action is for the project owner / Luna-0 to select one bounded
downstream compatibility semantic unit, if desired.

The original Luna-25 authorization was for a retained, deterministic UCI
Character Trajectories loader/split/report under the unchanged ACP-0006
`EXCURSION_V1` path. Its contract was
`.github/agents/luna-25.agent.md`; the authorization handoff is
`workflow/handoffs/luna-0-authorization-luna-25-dataset-evidence-20261003.md`.
The published implementation/evidence and completion handoff are
`5cb17d9bb79c848c27805cb79484d9ab3cd0f5b8` and
`425180bfb2b02691cf64f392f071795cc812cd72`. The subsequent independent review
closed the dataset evidence gate specifically for `luna25-v1`; it found that
the old split is not reconstructable and did not call the new split a
reproduction. The review is recorded in
`workflow/handoffs/luna-0-independent-review-luna-25-dataset-evidence-20261003.md`.

The 24 downstream failures remain a separate governance track. The independent
review reran the full suite with 24 failures, 796 passes, one CUDA-unavailable
skip and 821 collected tests; all failures remain in previously classified
consumer groups. No blanket consumer migration is authorized; visualization,
structural experiments, legacy observables, temporal/spiral analysis and the
3D viewer require consumer-specific intent and scoped review before
implementation. The Luna-25 review assigns no successor implementation because
these groups require distinct decisions.

The original acceptance and dispatch decision is in
`workflow/handoffs/luna-0-acp-0006-acceptance-luna-22-authorization-20261003.md`;
the implementation contract is `.github/agents/luna-22.agent.md`. The
preceding dependency and under-review proposal records remain historical.

The former Luna-15 FPGA/VHDL and Luna-16 FPAA assignments remain historical
workflow planning records and are superseded as current assignments by the
actual ACP-0002 contracts. Future FPGA-native and FPAA-native roles receive new
identifiers when separately authorized. Luna-17 is not created or executed by
H1.

Luna-18 H1 was limited to a versioned hardware-neutral Execution IR, minimal
backend identity/capability/equivalence/policy interfaces, canonical conversion
and safe reference reconstruction. Luna-0 independently verified and closed H1
at reviewed revision `4aee46829807072e9af0f08842d561026555006d`; the evidence is
in `workflow/handoffs/luna-0-independent-corrective-review-ACP-0003-H1.md`.
The IR-1 scope is canonical network configuration plus transferable initial
execution state for the supported reference reconstruction path, not a full
live-runtime checkpoint. H1 preserves Model-B parameters, timing,
deterministic ordering, bounded state, prediction/error behavior,
reward/idempotency and structural decisions. H1 does not authorize H2,
production backends, approximations, calibration, attractor neurons, edge
learning, ACP-0002 N3, Luna-13F reopening, Luna-13G or A01-A15 changes.

TPCN-IR-2 is a separate version boundary. It explicitly tags
`TANH_LEGACY` versus `EXCURSION_V1`, preserves E1 state and identity
continuation, rejects excursion records in IR-1, and represents M state without
claiming M reconstruction support. Its scope is transferable reference state,
not a complete live-runtime checkpoint.

---

# Historical hardware-role reservations (superseded)

The following sections are retained to preserve the original numbering and
planning history; they are not current assignments.

## Historical Luna-15 — FPGA/VHDL Branch

Begin only after software event semantics stabilize.

Target modules:

```text
tpcn_event_cell.vhd
tpcn_event_inbox.vhd
tpcn_event_router.vhd

tpcn_local_time.vhd

tpcn_energy_arbiter.vhd
tpcn_popcount.vhd

tpcn_predictor.vhd
tpcn_error_unit.vhd
```

Energy arbiter reference:

\[
C[n]
=
\operatorname{popcount}
(Q[n]\oplus Q[n-1]).
\]

Later allow weighted hardware activity.

Do not claim this is literal physical energy without calibration.

Treat it initially as architectural switching cost.

---

# 19. Luna-16 — FPAA Branch

Investigate analog realization of:

- neuron state,
- bounded nonlinear dynamics,
- leaky temporal state,
- prediction,
- error,
- energy approximation,
- operator selection.

Energy may use continuous approximations rather than digital transition counting.

Example:

\[
\tau_E\dot E=-E+\sum_k\alpha_kA_k.
\]

Maintain behavioral compatibility with the software reference rather than attempting to reproduce FPGA switching metrics.

---

# 20. Luna-17 — Hardware Equivalence

Compare:

```text
Software TPCN
      │
      ├── FPGA implementation
      │
      └── FPAA implementation
```

Compare observable behavior:

- event causality,
- predictions,
- classifications,
- state bounds,
- connectivity constraints,
- energy/utility decisions.

Exact internal numerical equality is not required across fundamentally different hardware.

---

# 21. First Integration Model

Start conservatively.

Candidate configuration:

```text
neurons:             256
classes:              26
bounded fan-in:        8
bounded fan-out:       8

execution:
    event driven

spatial reservoir:
    disabled

explicit 10 gates:
    disabled

structural plasticity:
    initially disabled

energy accounting:
    enabled

predictive error:
    enabled

classification:
    enabled
```

Do not optimize these values prematurely.

The first objective is proving the architecture works.

---

# 22. Required Metrics

Every training run should record:

\[
A=\text{classification accuracy}
\]

\[
L_p=\text{prediction loss}
\]

\[
N_e=\text{events processed}
\]

\[
N_a=\text{neuron activations}
\]

\[
E=\text{estimated energy}
\]

\[
C=\text{active connections}
\]

and eventually:

\[
U=\text{reward-adjusted computational utility}.
\]

Report per-character values where possible.

Also track:

```text
accuracy vs events
accuracy vs energy
prediction error vs events
prediction error vs energy
events per character
activations per character
energy per correct classification
connectivity utilization
```

---

# 23. Agent Handoff Format

Every Luna agent must leave:

```yaml
tpcn_handoff:
  agent: Luna-X
  component: component_name

  architecture_invariants_touched:
    - A01
    - A04

  preserves:
    - event_driven_execution
    - bounded_connectivity

  architecture_change: false

  files_changed:
    - path/file.py

  tests_added:
    - test_name

  tests_passing:
    - test_name

  assumptions:
    - assumption

  unresolved:
    - issue

  recommended_next_agent:
    - Luna-Y
```

No agent should silently change architecture.

---

# 24. Architecture Change Proposal

If an agent discovers that an invariant should change, create:

```text
docs/architecture_proposals/ACP-XXXX.md
```

containing:

```text
Current invariant

Observed problem

Proposed change

Why implementation alone cannot solve it

Expected benefits

Expected disadvantages

Hardware implications

Learning implications

Compatibility implications

Required experiments

Rollback plan
```

The change remains experimental until reviewed.

---

# 25. Execution Order

Run agents in this dependency order:

```text
Luna-0
Architecture Guardian
        │
        ▼
Luna-1
Event Semantics
        │
        ├──────────────┐
        ▼              ▼
Luna-2              Luna-4
Neuron              Topology
        │              │
        └──────┬───────┘
               ▼
            Luna-3
       Prediction/Error
               │
        ┌──────┼───────┐
        ▼      ▼       ▼
     Luna-5  Luna-6  Luna-8
     Energy  Dataset  Credit
        │      │       │
        └──────┼───────┘
               ▼
            Luna-7
          Classifier
               │
               ▼
           INTEGRATION
               │
               ▼
           Luna-11
          Verification
               │
                 ▼
             Luna-12 (passed)
             Contract + CPU exporter
               │
              ┌─┼──────────────────────────────┐
              ▼ ▼                              ▼
             12A 13                             14
              │  GPU                            ModelSim/
              ▼  visualization                  FPGA
             12B
              │
             12C
              │
             12D
              │
             12E
              │
             12F
              │
             12G
              │
             12H
              ├───────► 12I  structural growth
              │
              └───────► 12J  efficacy + causal verification
                      │
                      ▼
                   12K capacity pressure
                     and path shortening
                      │
                      ▼
                        12L energy / prediction
                        four-class temporal scale
                          │
                          ▼
                    Luna-0 review

        Stable software event semantics
                     │
                     ▼
                Post-observability
                Luna-15 / Luna-16 / Luna-17
```

---

# 26. Immediate Success Criteria

The first milestone is successful when a software TPCN can:

1. Receive letter strokes sequentially as events.
2. Operate without a global neural timestep.
3. Process only causally activated neurons.
4. Maintain bounded connectivity.
5. Maintain bounded neuron state.
6. Predict subsequent stroke information.
7. Generate explicit prediction-error events.
8. Classify the completed sequence.
9. Track local computational/energy cost.
10. Associate useful computation with delayed reward.
11. Run without the spatial reservoir.
12. Produce sufficient instrumentation to compare explicit gating against naturally emerging event-driven selectivity.

Accuracy does not need to be exceptional for Milestone 1.

Correct architectural behavior comes first.

---

# 27. Guiding Principle

TPCN should not ask:

> How can every neuron compute as cheaply as possible?

It should ask:

> Which computations are worth their cost?

The target system is therefore:

\[
\boxed{
\text{Event Driven}
+
\text{Predictive}
+
\text{Local}
+
\text{Resource Bounded}
+
\text{Utility Driven}
+
\text{Structurally Adaptive}
}
\]

The FPGA and FPAA implementations are physical realizations of those principles rather than definitions of them.
## Operational execution rules

These are role definitions for future implementation work, not a request to launch fifteen simultaneous agents. Allocate roles on demand; one worker may handle multiple roles sequentially. Keep verification independent of implementation when resources permit.

Before dispatch, Luna-0 records the repository revision, existing changes, accepted interfaces, owned files, dependencies, acceptance checks and a bounded task for each active role. Inspect actual repository instructions before assigning paths. The branch names above are proposed names; no branches are created by this documentation package. Component branches should use names such as feature/event-core rather than assuming the diagram is a filesystem layout.

Only parallelize tasks after their shared interfaces are stable and their file ownership does not overlap. Luna-2 and Luna-4 depend on Luna-1's event contract. Luna-5 and Luna-8 must agree on local activity, eligibility and delayed reward interfaces before classifier integration. Resolve interface changes through Luna-0 rather than letting workers edit shared files concurrently.

Use the [handoff template](AGENT_HANDOFF_TEMPLATE.md) for every completed or blocked assignment. Luna-11 records actual commands and observed results; proposed tests must never be reported as passing. Failed invariants block integration. Luna-0 integrates only compatible, verified changes, then updates the architecture changelog when a decision changes.

Experimental gating and plasticity begin after the first integrated software milestone passes. The visualization track begins after Luna-11 and remains downstream-only. FPGA and FPAA implementation branches begin after software event semantics are stable; post-observability hardware equivalence compares implementations against versioned reference traces. Hardware-specific clocks, quantization and metering must not redefine neural semantics.

See [acceptance criteria](../architecture/ACCEPTANCE_CRITERIA.md) and [proposal process](../architecture_proposals/README.md).

### Luna-0 independent review of ACP-0002 Stage N1 - 2026-09-30

At reviewed revision `7ddf00b6c7a8f01ad4ebe3483bc553c83dbe26d3`, synchronized
with `origin/main` on a clean `main` worktree, Luna-0 independently verified
ACP-0002 N1 as:

**PASS - ACP-0002 N1 DATA MODEL AND COMPATIBILITY INDEPENDENTLY VERIFIED**

The bounded edge schema, compatibility defaults, neuron-gain migration,
legacy payload routing, topology reconstruction, structural-growth defaults,
observer non-interference and deterministic representation passed direct and
automated checks. The existing TPCV-1 format intentionally remains a
version-1 observability boundary that omits future connection transfer fields;
this is now documented and does not claim complete N1 edge-state fidelity.

Validation recorded in the Luna-0 handoff includes 18 focused N1 tests, 83
selected topology/neuron/structural/replay/regression tests, 309 full CPU
tests with 1 skipped, direct adversarial probes, compileall and diff checks.
N1 is complete. ACP-0002 remains accepted for staged implementation; N2 is
not authorized. A01-A15 remain unchanged, Luna-13F remains closed and
Luna-13G remains unauthorized.

### Luna-16 ACP-0002 Stage N2 authorization - 2026-09-30

After N1 publication and independent review, Luna-0 selected **CONTROLLED
CANONICAL CUTOVER**. N1 is the final representation-compatible version of
legacy raw-payload execution. N2 intentionally activates the accepted ACP-
0002 Model-B transfer as the new canonical execution equation; the N1 defaults
`w=1`, `d=1`, `r=0` produce `tanh(a)`, not raw `a`, and must not be described
as signal identity.

Historical closed experiment revisions remain reproducible from their
committed code and are not reinterpreted as Model-B results. New N2-and-later
experiments must identify the new architecture revision. No permanent
per-edge legacy/model-B flag is part of the canonical architecture.

Luna-16 is authorized for **static execution only**:

```text
z_ij = tanh(w_ij * a_i)
v_ij = d_ij * z_ij + (1 - d_ij) * r_ij
```

The contribution `v_ij` is scheduled after the existing positive finite edge
delay and then follows the existing local-time decay, bounded integration,
neuron gain and fixed-neuron-nonlinearity path. No global neural timestep is
introduced. Edge parameters are immutable during N2 execution.

Luna-16 must establish a new Model-B analytic/replay baseline. It must keep
causality, deterministic ordering, finite delays, queue and structural bounds,
label/future isolation, reward identity, observer non-interference and bounded
recurrence invariant. Numeric payload/state/activation and downstream metrics
may change and are not legacy regressions by themselves. TPCV-1 remains an
explicit observational version-1 boundary; any computationally active field
serialization/version change requires an explicit governance result.

Luna-16 must not implement edge learning, probationary or maturing edges,
new structural utility prediction, new pruning, reward-driven edge updates,
temporal mini-networks or hardware-specific voltage behavior. It must return
to Luna-0 after implementation. Luna-13F remains closed, Luna-13G remains
unauthorized, ACP-0002 remains accepted for staged implementation, and
A01-A15 remain unchanged.

### Luna-16 N2 implementation result - 2026-09-30

**OBSERVED:** Static Model-B transfer is active for numeric neural signal
routing at implementation revision `ed8aaff2d0d0d031c2c1f84b311251f530282479`:
`z=tanh(w*a)` and `v=d*z+(1-d)*r`. Numeric signal payloads are delayed by the
existing edge delay; control and metadata payloads are not transformed.

**OBSERVED:** The focused N2 suite passed 267 tests and the full CPU suite
passed 549 tests with 1 skipped. Compile, deterministic replay, observer
ON/OFF, fan-out, equal-time fan-in, unequal delays, bounded recurrence,
structural defaults/reconstruction and control-payload boundary checks passed.

**INFERRED:** N2 preserves event causality, local temporal state, finite
propagation, bounded topology/dynamics, label/future isolation, reward
identity and observer non-interference. Numeric payload/state/activation and
downstream metrics are expected to differ from pre-N2 execution.

**TPCV GOVERNANCE RESULT:** `TPCV-1 REMAINS VALID FOR ITS LIMITED DECLARED
PURPOSE`. TPCV-1 is downstream-only and does not serialize active `w`, `d` or
`r`; no silent format expansion was made. Computationally equivalent transfer
state replay would require a separately governed format decision.

**HYPOTHESIZED:** The new bounded edge transform provides the authorized
Model-B computational substrate without establishing task improvement. The
analytic/replay baseline is recorded at
`artifacts/acp-0002-n2-model-b-baseline/baseline.json`.

N2 returns to Luna-0 for independent review. It does not authorize N3 or any
later ACP-0002 stage, probationary/maturing edges, temporal mini-networks or
Luna-13G. Luna-13F remains closed.

## Luna-27 — TPCV-2 EXCURSION_V1 Snapshot Visualization

**Authorization:** Luna-0 authorizes one bounded CPU visualization
representation implementation after the post-Luna-22 compatibility review.
The exact agent contract is `.github/agents/luna-27.agent.md`; the
authorization record is
`workflow/handoffs/luna-0-authorization-luna-27-tpcv2-excursion-snapshot-20261003.md`.
This entry authorizes implementation but does not execute it.

**Decision:** `DECISION C — VERSIONED EXCURSION VISUALIZATION FORMAT
REQUIRED; LUNA-27 AUTHORIZED.` TPCV-2 is dedicated to instantaneous
`EXCURSION_V1` snapshots at existing CPU epoch boundaries. TPCV-1 bytes,
decoding, and historical meanings remain unchanged. The format version is
the model discriminator; model type must not be inferred from values.

**TPCV-2 observer contract:**

- `state` is the existing E2 `state` alias (`x`).
- `active` is true iff `mode != N`, meaning a non-neutral excursion mode is
  currently admitted at capture; it does not mean nonzero TANH output.
- `mode` is the bounded enum `N`, `S_PENDING`, `S_RETURN`, or `M_ACTIVE`.
- `pending_internal_work` indicates only whether internal work is pending.
- `processed_events` is the E2 `processed_event_count`, including processed
  external and internal events.
- No scalar activation is serialized or fabricated; a shared decoded API may
  explicitly report activation as unavailable. No last emission, interval
  activity, event history, or runtime checkpoint state is included.

The format retains finite deterministic records, canonical ordering, strict
malformed/oversize rejection, and TPCV-1 bounds. TPCV-2 uses the existing
32-byte big-endian header with version byte 2; its neuron record contains a
bounded UTF-8 ID, flags for active/optional position/pending work, explicit
mode code, finite state, bounded processed-event count, and optional signed
coordinates. Connection records keep their TPCV-1 layout. No ACP or A01-A15
change is made.

**Owned files:** `tpcn/visualization.py`, `tpcn/cpu_visualization.py`,
`tests/test_visualization.py`, `tests/test_cpu_visualization.py`,
`workflow/docs/luna/VISUALIZATION_CONTRACT.md`, and the Luna-27 completion
handoff. No other visualization code is authorized.

**Required gate:** preserve TPCV-1 byte/semantic behavior; test deterministic
TPCV-2 round-trip and explicit model semantics; reject unsupported, malformed,
oversize, and mixed-version sequences; pass all three CPU visualization tests,
the existing visualization suite, and GPU TPCV-1 regression; verify offline
replay and capture disabled/every-epoch/every-N result equivalence. Keep
capture downstream-only, labels/future data isolated, and fixed topology
unchanged. Report other 21 baseline downstream failures without repairing
them. Stop and return to Luna-0 if core/runtime changes or ownership expansion
is required.

**Mandatory sequence:** `Luna-0 -> Luna-27 -> Luna-0`. Luna-27 returns with
its evidence handoff and may not authorize a successor.

**Final status (2026-10-04): CLOSED / INDEPENDENTLY VERIFIED.** Luna-0
independently reviewed the published implementation and focused test set and
passed the bounded CPU TPCV-2 instantaneous `EXCURSION_V1` snapshot capture,
versioned codec, and homogeneous-version offline replay scope. The independent
review handoff is
`workflow/handoffs/luna-0-independent-review-luna-27-tpcv2-excursion-visualization-20261004.md`.
TPCV-1 bytes and historical meanings remain unchanged. This closure is
observability-only: it is not architecture promotion, requires no ACP, and
does not authorize GPU/FPGA support, downstream migrations, or a successor
Luna. The implementation full-suite evidence remains 821 passed, 21 failed,
1 skipped; the independent reviewer did not rerun the full suite. The 21
previously classified downstream failures remain separate and unresolved.

## Luna-0 EXCURSION_V1 structural re-entry readiness - 2026-10-04

At baseline `d9abe5e3a5b9b3c6d6049ac4c64647463c33ba2d`, Luna-0 classified
the 19 Luna-12B/Luna-12L/spiral/temporal-analysis/3D-viewer failures as
terminating at the intentional EXCURSION_V1 structural-mode guard. This is
the immediate test dependency, not proof that all assertions pass after the
guard. The historical ExperimentRunner's index/policy endpoints,
`abs(run.feature) + run.loss` score, and feature-derived pruning score do not
establish source-local E2 evidence.

Luna-13F's runtime temporal-association mechanism remains an experimental
fixture result: evidence generation and canonical admission were supported
there, useful-growth prediction was not supported, and resource benefit was
not established. Its use in ordinary E2 training required an explicit
project-owner decision. At the time of this readiness finding, ACP-0007 was
draft and growth/pruning and Luna-28 were not authorized. See
`workflow/handoffs/luna-0-excursion-structural-reentry-readiness-20261004.md`
for the historical result and
`workflow/handoffs/luna-0-owner-decision-acp0007-excursion-structural-growth-20261004.md`
for the superseding decision.

## Luna-0 owner decision — ACP-0007 accepted - 2026-10-04

**ACCEPTED WITH OWNER-SPECIFIED LOCAL OBSERVATION CONTRACT.** The project
owner accepted ACP-0007 as an optional, explicitly selected EXCURSION_V1
growth-only experiment. Architecture contract version 1.2 records this
interpretation without changing the substantive text or scope of A01-A15.
Fixed topology remains the default. Acceptance does not establish useful
growth, accuracy/prediction/reward/energy improvement, resource benefit,
pruning, A14 promotion, or hardware equivalence. ACP-0002 N3 and all
downstream consumer migrations remain unauthorized.

## Luna-0 authorization — Luna-28 local temporal growth - 2026-10-04

**AUTHORIZED — IMPLEMENTATION + VERIFICATION ONLY; NOT STARTED.** Luna-28 may
implement the bounded CPU E2 observation and post-character growth path under
accepted ACP-0007. Its exact file ownership, interfaces, required tests,
regressions, exclusions, and stop conditions are in
`.github/agents/luna-28.agent.md` and the authorization handoff at
`workflow/handoffs/luna-0-authorization-luna-28-excursion-local-temporal-growth-20261004.md`.
The mandatory sequence is `Luna-0 owner decision -> Luna-0 authorization ->
Luna-28 implementation/verification -> Luna-0 independent review`. Do not
create or run a downstream migration from this authorization. Luna-28 has not
yet been executed at this authorization point.

## Luna-0 independent review — Luna-28 closed - 2026-10-04

**PASS — AUTHORIZED LUNA-28 MECHANISM SCOPE INDEPENDENTLY VERIFIED.** The
review began at clean `main`, `HEAD == origin/main ==
028b5793917efb2c1af279691d1611427de3a86c`. Boundedness, locality,
character lifecycle, deterministic growth, fixed-topology and TANH_LEGACY
compatibility, and later real causal routing passed review. Focused tests
(44), closed-component regressions (168), compilation, and Pylance checks
passed. The independent full suite remains at 865 passed, 21 known failures,
and 1 existing CUDA-unavailable skip: 19 downstream compatibility failures
at the intentional opt-in guard and 2 stale Luna-12E assertions. No
Luna-28 regression was identified.

The full independent evidence, failure reconciliation, and A01-A15 matrix
are recorded in
`workflow/handoffs/luna-0-independent-review-luna-28-excursion-local-temporal-growth-20261004.md`.
This closes the implementation review only; it does not establish task
efficacy, resource benefit, downstream integration readiness, or hardware
equivalence. ACP-0007 remains accepted and unchanged; contract version 1.2
and A01-A15 are unchanged. No downstream migration or successor is
authorized.

## Luna-0 authorization — Luna-29 CPU structural replay compatibility - 2026-10-04

**AUTHORIZED — DOWNSTREAM CPU-HELPER COMPATIBILITY + FOCUSED VERIFICATION
ONLY; NOT STARTED.** Luna-29 may adapt `run_cpu_training()` to accept an
explicit existing `ExperimentConfig` and migrate the Luna-12B CPU replay
tests to the accepted ACP-0007 growth-only E2 behavior. The config must
carry the explicit bounded structural neighborhood and all required finite
settings; `structural_plasticity=True` alone remains invalid for E2 and must
not synthesize hidden defaults. E2 pruning remains unauthorized. The exact
contract and file ownership are in `.github/agents/luna-29.agent.md` and
`workflow/handoffs/luna-0-authorization-luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md`.

The four Luna-12B tests reproduce at the intentional missing-observation
guard. TPCV-2 connection records and existing adjacent-snapshot replay
adequately represent added edges; no codec change or ACP is required.
Explicit TANH_LEGACY regression behavior and generic edge-removal replay
remain separate. Luna-29 does not include the CLI, temporal-analysis,
3D-viewer, Luna-12L, spiral, or Luna-12E consumers. Mandatory sequence:
`Luna-0 -> Luna-29 -> Luna-0`. This authorization does not execute Luna-29
or establish task efficacy, resource benefit, downstream readiness, or
hardware equivalence.

The verified decision revision was
`c654ffe9c8d4a6d179781696d9ba5cd239e12795`; the authorization package was
published at `aad4b0db09773ebca9314d188c3b24297ad17c44`. Luna-29 may execute
from clean synchronized `main` descending from the publication revision when
any intervening commits are governance-only clarifications/pinning for this
authorization. The supplied `F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb`
token is not a Git object and is not repository provenance. Status remains
**AUTHORIZED / NOT EXECUTED**.

## Luna-0 independent review — Luna-29 closed - 2026-10-04

**PASS — LUNA-29 CPU-HELPER COMPATIBILITY INDEPENDENTLY VERIFIED AND CLOSED
FOR ITS AUTHORIZED SCOPE.** Review began at clean synchronized `main`,
`HEAD == origin/main == 6e1387967de2d1170d5743a38927afe08b9ddab8`.
Implementation `252fa15073e983a793a06b0ba3c79c84ced84637` was verified
against the authorization and completion handoffs. The config-taking helper,
legacy no-config behavior, conflict handling, capture non-interference,
bounded deterministic growth-only fixture, label isolation, TPCV-2 admitted
edge replay, metric semantics, E2 no-pruning behavior, generic removed-edge
replay, and separate TANH_LEGACY regression passed independent review.

The public helper is **SUPPORTED FOR CONFIGURATION PASS-THROUGH ONLY**.
Luna-29's contract does **NOT REQUIRE** the helper's fixed synthetic workload
to produce an admitted E2 edge. Real growth and TPCV-2 replay were verified
in the explicit bounded `ExperimentRunner` fixture; no claim is made that the
default helper workload grows.

Focused runs passed: Luna-12B 13, Luna-28 44, CPU/TPCV 32, combined 89, and
experiment regressions 12. The independent full suite reported 880 passed,
17 failed, and 1 CUDA-unavailable skip (898 collected). The 17 failures are
outside Luna-29's changed paths: 2 known Luna-12E legacy-observable
assertions, plus 15 downstream callers still using pre-ACP-0007 structural
configurations (8 Luna-12L, 1 spiral, 3 temporal-analysis, 3 3D viewer).
No unrelated repair was made; all Luna-12B focused tests pass.

The review handoff,
`workflow/handoffs/luna-0-independent-review-luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md`,
contains the clause matrix and complete validation record. Contract 1.2,
A01-A15, and accepted ACP-0007 are unchanged. This closes only Luna-29's
authorized adapter scope; it does not establish downstream migration,
task/resource efficacy, integration readiness, or hardware equivalence.
No successor is authorized.

## Luna-0 authorization — Luna-30 TPCV-2 replay consumer compatibility correction - 2026-10-04

**AUTHORIZED — LUNA-30 TPCV-2 REPLAY CONSUMER COMPATIBILITY CORRECTION;
NOT EXECUTED.** Authorization starts at clean synchronized `main`,
`HEAD == origin/main == 727a00aed08a4ba2c7194a70cde603f60ab35065`
(`docs: classify replay consumer compatibility blockers`). The preceding
Luna-0 review remains **BLOCKED — CURRENT DOWNSTREAM REPLAY CONSUMER
DEFECT** pending implementation and independent review.

The confirmed bounded defect is `VisualizationScene.nodes()` and
`VisualizationScene.inspect()` accessing scalar `activation` on canonical
TPCV-2 `ExcursionNeuronRecord`, which intentionally has no activation field.
Luna-30 may project activation as `float | None` (TPCV-1 preserves its exact
float; TPCV-2 returns `None`) without synthesizing a value, while continuing
to filter TPCV-2 activity using `active`. Luna-30 may also make
TPCV-1-specific temporal-analysis capability-limit wording version-neutral;
per-edge use remains unavailable without event-path evidence.

The six failing consumer fixtures are stale bare structural-plasticity helper
calls stopped by the ACP-0007 observation guard. Migrate these downstream
tests to deterministic detached TPCV-2 replay with explicit metrics.
Synthetic edge disappearance is visualization-only snapshot-difference
evidence, not E2 pruning. Luna-29 already verified a real E2-added edge in
TPCV-2; Luna-30 need not rerun structural learning.

Exact ownership, prohibited files, tests, and completion checks are in
`.github/agents/luna-30.agent.md` and
`workflow/handoffs/luna-0-authorization-luna-30-tpcv2-replay-consumer-compatibility-20261004.md`.
Only `tpcn/viewer_3d.py`, limited `tpcn/temporal_analysis.py` wording,
`tests/test_viewer_3d.py`, `tests/test_temporal_analysis.py`, and the Luna-30
completion handoff are owned. No TPCV schema/codec, CPU helper, experiment,
topology, structural-learning, CLI, hardware, Luna-12L, spiral, or Luna-12E
files are authorized. If any prohibited file is required, stop and return to
Luna-0.

ACP required: **NO**. Architecture Contract 1.2 and A01-A15 remain unchanged.
E2 pruning and N3 remain unauthorized. Mandatory sequence:
`Luna-0 -> Luna-30 -> Luna-0`; Luna-30 is **AUTHORIZED / NOT EXECUTED**.

## Luna-0 independent review — Luna-30 closed - 2026-10-04

**PASS — LUNA-30 TPCV-2 REPLAY CONSUMER COMPATIBILITY CORRECTION
INDEPENDENTLY VERIFIED / CLOSED** for the authorized downstream replay
consumer scope. Review began at clean synchronized `main`,
`HEAD == origin/main == 188dfd49fddc6702e86c56210f26455e6513050f`.

The independent source, replay, provenance, and test audits verified that
canonical TPCV-2 `ExcursionNeuronRecord` intentionally has no scalar
activation. The viewer returns `None` for that field in both node projection
and inspection, including an active nontrivial-state adversarial record; it
preserves the exact TPCV-1 activation float and filters TPCV-2 activity from
the canonical `active` field. No TPCV-2 scalar is synthesized.

The initial Luna-30 implementation's bounded temporal-accounting scope defect
was corrected before review. Accepted additions are counted only through
`accepted_additions`; rejection reason keys do not become accepted growth.
The version-neutral limitation continues to state that topology existence
does not prove per-edge routed-event use. Generic detached snapshot removal
remains visualization evidence only, not an E2 pruning event.

Independent tests: focused consumer suite **19 passed**; combined
consumer/prerequisite suite **108 passed**; full suite **896 passed, 11
failed, 1 skipped**; collection **908 tests**. The 11 remaining failures
reconcile to 2 Luna-12E, 8 Luna-12L, and 1 spiral historical failures; there
are zero temporal-analysis or 3D-viewer failures. Compileall, diagnostics for
all four reviewed Python/test files, and `git diff --check` passed. Full
evidence is recorded in
`workflow/handoffs/luna-0-independent-review-luna-30-tpcv2-replay-consumer-compatibility-20261004.md`.

Architecture Contract 1.2, A01-A15, and accepted ACP-0007 are unchanged.
No ACP, schema change, or architecture change was required. E2 pruning and
N3 remain unauthorized. Task efficacy, resource benefit, and hardware
equivalence are not established. Luna-30 closure does not authorize Luna-31
or any successor; the remaining Luna-12E, Luna-12L, and spiral work requires
separate governance decisions.

## Luna-0 authorization — Luna-12E EXCURSION_V1 observable compatibility correction (Luna-31) - 2026-10-04

**AUTHORIZED — LUNA-31 TEST-ONLY COMPATIBILITY CORRECTION; NOT EXECUTED.**
This is a new bounded decision following the Luna-30 closure above; it does
not revise the historical closure finding. The current verified baseline is
clean synchronized `main`,
`HEAD == origin/main == 8d5f7f5ad1c594df3cd886de327eb14c3dfbe15c`.
The opaque revision token in the source request could not be resolved by Git;
the live `origin/main` commit has the requested Luna-30 closure subject.

Luna-0 reproduced the two named Luna-12E failures and independently probed
their observables. The edge intervention changes route trace, event count,
edge-transfer proxy and route depth while prediction loss remains equal.
Equality is permitted; no prediction or task-efficacy claim follows. The E2
character reset leaves stable neuron objects at the configured terminal
horizon with neutral public state/mode and no pending event. The old exact
terminal clocks `0.0`/`1.0` are legacy-only; an explicit TANH_LEGACY control
retains those values, but is not required.

Luna-31 may change only
`tests/test_luna12e_integration.py` and its completion handoff
`workflow/handoffs/luna-31-luna12e-e2-observable-compatibility-20261004.md`.
The dispatch contract is `.github/agents/luna-31.agent.md`; the decision,
baseline, evidence, assertion matrix, exclusions and acceptance checks are
recorded in
`workflow/handoffs/luna-0-post-luna30-luna12e-e2-observable-decision-20261004.md`.
No production changes, Luna-12L/spiral work, or edits to the three historical
Luna-12E topology component tests are authorized. If public E2 observables
prove insufficient, stop and return to Luna-0.

Run the full Luna-12E file, relevant E2 integration/routing and Luna-26
multi-hop regressions, and the full suite. Require zero Luna-12E failures and
no new applicable regressions. The previously established remaining groups
are Luna-12L (8) and spiral (1); do not hard-code an aggregate pass count.
Architecture change: **NO**. ACP required: **NO**. Architecture Contract 1.2,
A01-A15, and accepted ACP-0007 are unchanged. Sequence:
`Luna-0 -> Luna-31 -> Luna-0`; Luna-31 is **AUTHORIZED / NOT EXECUTED**.

### Luna-31 closure - 2026-10-04

Luna-31 = **CLOSED / INDEPENDENTLY VERIFIED** within the exact Luna-12E EXCURSION_V1 test-observable compatibility scope (commit 9efc5f1; review: workflow/handoffs/luna-0-independent-review-luna-31-luna12e-e2-observable-compatibility-20261004.md). Production code, Architecture Contract 1.2 and ACP-0007 unchanged. Remaining failures: 8 Luna-12L, 1 spiral. Successor: NOT AUTHORIZED. E2 pruning and N3 remain unauthorized.

### Luna-32 authorization - 2026-10-04

Luna-32 (Historical Luna-12L / Spiral Model-Explicit Compatibility) is **AUTHORIZED / NOT EXECUTED**. Contract: .github/agents/luna-32.agent.md; decision: workflow/handoffs/luna-0-post-luna31-luna12l-spiral-policy-compatibility-decision-20261004.md. Scope is **historical experiment compatibility** only: make TANH_LEGACY explicit for all five Luna-12L classifier policies and all ten spiral run_controls, preserving real legacy policy execution and provenance guards. It is **not** current E2 scientific validation: no legacy-to-e2_local_temporal aliasing, no core/ACP change, and the corrected Luna-12L NOT SUPPORTED result and artifacts remain frozen (an explicit-TANH rerun is not the same experiment). A current ACP-0007 four-class experiment would need a new contract. Sequence: Luna-0 -> Luna-32 -> Luna-0. Luna-33 NOT AUTHORIZED.

### Luna-32 independent closure - 2026-10-04

Luna-32 = **CLOSED / INDEPENDENTLY VERIFIED** for historical Luna-12L/spiral model-explicit compatibility only. All five Luna-12L classifier policies, including `fixed`, and all ten spiral controls use the same explicit `TANH_LEGACY` model; historical policy execution, provenance, scale separation, and deterministic matched-model controls were independently verified. The full suite passed (908 passed, 0 failed, 1 unchanged CUDA-unavailable skip; 909 collected). Evidence: `workflow/handoffs/luna-0-independent-review-luna-32-historical-temporal-spiral-model-compatibility-20261004.md`.

The corrected historical Luna-12L verdict remains **NOT SUPPORTED / UNCHANGED**. The explicit legacy compatibility run is not the same experiment as the retained artifact; artifacts and historical result handoffs are unchanged. Current `EXCURSION_V1` default and ACP-0007 are unchanged. No current E2 four-class experiment or efficacy result was established. E2 pruning and N3 remain **NOT AUTHORIZED**; task efficacy, resource benefit, and hardware equivalence remain **NOT ESTABLISHED**. Luna-33 is **NOT AUTHORIZED**.

### Luna-33 authorization — ACP-0007 four-class EXCURSION_V1 efficacy — 2026-10-04

**AUTHORIZED / NOT EXECUTED.** After Luna-32's independent closure at clean
synchronized `main` (`cc66e6a4affb044bf726d92510bcfd214c1f698f`), Luna-0
verified a green baseline (908 passed, 0 failed, 1 CUDA-unavailable skip;
909 collected) and audited the public `ExperimentRunner` evidence surfaces.
They expose deterministic seeded starting topology, structural decisions and
before/after topology snapshots, held-out task/prediction metrics, and exact
runtime route paths. A matched efficacy experiment needs no private topology
injection or core/API change.

Luna-33 is authorized to test whether growth-only ACP-0007
`e2_local_temporal` improves four-class canonical held-out accuracy over
matched fixed topology and whether any gain depends on preserved training
point order. It uses four paired conditions (fixed A, observation-only B,
growth C, temporal-order-destroyed training D), five seeds, one explicitly
bounded eight-node synthetic reference setup, and a fixed canonical held-out
split. The full configuration, label boundary, engagement/route-use gates,
and falsifiable supported/not-supported/inconclusive rules are in
`.github/agents/luna-33.agent.md` and
`workflow/handoffs/luna-0-post-luna32-acp0007-four-class-efficacy-decision-20261004.md`.

This is a distinct current EXCURSION_V1 experiment, not historical
TANH_LEGACY compatibility and not a reuse of Luna-12L results or artifacts.
The efficacy experiment and all outcome-bearing previews were **NOT RUN** for
authorization. Contract 1.2, A01-A15, ACP-0007, and acceptance criteria are
unchanged; **no ACP required**. The historical Luna-12L verdict remains
**NOT SUPPORTED / UNCHANGED**. Task efficacy, prediction benefit, resource
benefit, and hardware equivalence remain **NOT ESTABLISHED** until separate
evidence exists. E2 pruning and N3 remain **NOT AUTHORIZED**. Sequence:
`Luna-0 -> Luna-33 -> Luna-0`; Luna-33 must return to Luna-0 for independent
review and may not self-close or authorize a successor.

### Luna-33 topology-feasibility correction — 2026-10-04

**AUTHORIZED — CORRECTED LUNA-33 / NOT EXECUTED.** The original
`topology_initial_edges=8` setting failed public initialization for four of
five required seeds. Before any four-class efficacy run or outcome-bearing
inspection, Luna-0 swept the public `ExperimentRunner` initializer over
initial edge counts 0–8 and seeds 0–4. The maximum all-seed feasible count is
2. The exact success/error matrix, resulting seed-specific two-edge
topologies, and static ring headroom are recorded in
`workflow/handoffs/luna-0-luna33-topology-feasibility-correction-20261004.md`.
Each topology retains at least seven legal absent ring candidates under the
unchanged fan-in/out limits of two and edge capacity 16.

Only `topology_initial_edges` is corrected from 8 to 2 in
`.github/agents/luna-33.agent.md`. Seeds, eight-node scale, edge capacity,
fan-in/out, ring observation fabric, structural-growth bounds, dataset and
split, A/B/C/D design, D intervention, primary metric, support rule, and
public initializer remain unchanged. The original blocked-execution handoff
is preserved unchanged as historical evidence. Contract 1.2, A01–A15,
ACP-0007 and acceptance criteria are unchanged; no ACP is required. Luna-33
is **AUTHORIZED / NOT EXECUTED** and may resume under the corrected dispatch,
then must return to Luna-0. No efficacy outcome was examined or produced.
Historical Luna-12L remains **NOT SUPPORTED / UNCHANGED**; Luna-13F
useful-growth prediction remains **NOT SUPPORTED / UNCHANGED**; E2 pruning
and N3 remain **NOT AUTHORIZED**. Task efficacy, prediction benefit,
resource benefit and hardware equivalence remain **NOT ESTABLISHED**.
Successor work is not authorized.

### Luna-33 independent closure - 2026-10-04

**PASS - LUNA-33 ACP-0007 FOUR-CLASS EXCURSION_V1 EFFICACY EXPERIMENT
INDEPENDENTLY VERIFIED / CLOSED** within the exact declared four-class
synthetic efficacy experiment scope. The Luna-0 independent review is
recorded in
`workflow/handoffs/luna-0-independent-review-luna-33-acp0007-four-class-efficacy-20261004.md`.
The committed runner reproduced all three result artifacts byte-for-byte;
all 20 seed/condition runs were valid, and A/B observation non-interference
and held-out non-mutation passed independent checks.

The joint predeclared H1 is **NOT SUPPORTED IN THIS SETUP** (mean C-A and
C-D are both 0.0; 0/5 positive seeds). Structural observations were present;
candidate opportunities, growth attempts, and admissions were zero, and no
edge was later route-used. The effect of successfully engaged growth and
temporal specificity of engaged growth remain **NOT ESTABLISHED**.
Prediction benefit, resource benefit, and hardware equivalence remain
**NOT ESTABLISHED**.

Architecture Contract 1.2, A01-A15, and accepted ACP-0007 are unchanged.
There is no architecture, core, runtime, or API change. Historical Luna-12L
remains **NOT SUPPORTED / UNCHANGED**; Luna-13F remains **NOT SUPPORTED /
UNCHANGED**. E2 pruning and N3 remain **NOT AUTHORIZED**. Luna-33 is closed
only within the declared experiment scope. **Luna-34 and any successor are
NOT AUTHORIZED.**

### Luna-0 post-Luna-33 candidate-formation bootstrap decision - 2026-10-04

**PASS - ACP-0007 CANDIDATE-FORMATION BOOTSTRAP CLASSIFIED;
LUNA-34 AUTHORIZED / NOT EXECUTED.** Independent audit of all 64 C and D
training decisions for each of five seeds found 64 `no_candidate` decisions,
zero candidate rejections, retained candidates, attempts, or admissions per
seed. Distinct-emitter deduplication found respectively 59/59/59/59/61
emitting characters, 5/5/5/5/3 silent characters, and zero multi-emitter
characters. Every emitted character's sole emitter was its designated input
neuron; `emitting_neuron_count` reconciles exactly.

Downstream receives are present without downstream canonical emissions:
C receiving totals are 79/78/80/79/80, emitting totals 59/59/59/59/61,
maximum route depth is 1 in every seed, and edge-transfer proxies are
positive. The root cause is the **WITHIN-CHARACTER MULTI-EMITTER /
PROPAGATION-TO-EMISSION BOOTSTRAP GAP**, not observation, ranking, capacity,
reporting, or growth-controller failure. With no second distinct emitter,
no legal ACP-0007 earlier-source/later-neighbor emission pair can form;
ring orientation and `association_window=4.0` are **NOT THE ROOT CAUSE**.

Default `theta_E=1`, `A_max=1`, and static Model-B signal-only transfer gives
`tanh(1) < 1`; even the accepted `|edge_weight| <= 2` bound gives
`tanh(2) < 1`. A single routed payload from neutral state cannot trigger a
downstream ordinary excursion. Repeated within-character temporal
accumulation is a mechanism question, not a defect. The public E2 runtime,
fixed topology, point input and observation APIs suffice; no architecture
change or ACP is required.

Luna-34 is authorized **only** for a label-free, mechanism-only bridge
experiment using a two-node direct fixed edge, the default static Model-B
condition, and one predeclared `|w|=2` static-bound sensitivity condition
plus a no-edge control. It must stop before topology mutation, use no
classification/efficacy endpoints, retain actual emission and route
evidence, and return to Luna-0. This is **not task efficacy**, not
architecture promotion, and not authority to alter ACP-0007, treat
reception as emission, carry evidence across characters, or run a new
accuracy experiment. The exact bounded dispatch and file scope are in
`.github/agents/luna-34.agent.md`; review evidence is in
`workflow/handoffs/luna-0-post-luna33-candidate-formation-bootstrap-decision-20261004.md`.
Luna-33's H1 remains **NOT SUPPORTED IN THIS SETUP**; engaged-growth task
effect and temporal specificity remain **NOT ESTABLISHED**. Historical
Luna-12L/Luna-13F and accepted ACP-0007 are unchanged. E2 pruning and N3
remain **NOT AUTHORIZED**.
