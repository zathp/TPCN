---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-50 governance review and Luna-51 provenance correction authorization"
  task_id: "luna-0-review-luna50-authorize-luna51-20261008"
  component: "Historical fixture provenance limits and regression-gate provenance invariants"
  status: "complete - Luna-50 limitation parked; Luna-51 authorized / not executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "da67433220d92d926d4c4e84e5b9fa08cda4bb10"
  result_revision: "published governance commit containing this handoff"
  dependencies:
    - "Luna-50 authorization b49f6642957ea630598b576c3c57f8862e436a14"
    - "Luna-50 execution da67433220d92d926d4c4e84e5b9fa08cda4bb10"
    - "Luna-50 independent review accepted as BLOCKED - HISTORICAL RUNTIME UNAVAILABLE"
    - "Luna-44 canonical fixture and provenance"
    - "Luna-46 MIXED retained diagnostic"
    - "Luna-47F replay-only retained diagnostic"
  owner: "Project owner; Luna-0 governance decision"
  classification:
    - "read-only evidence/governance review"
    - "historical runtime limitation parked"
    - "correction-only Luna-51 authorized / not executed"
  hypothesis: "The four full-suite failures are provenance identity guard defects, not contradictions of the historical fixture or scientific evidence."
  counter_hypothesis: "The failures expose changed protected science inputs or an invariant that requires exact cross-runtime regeneration before continued work."
  interfaces_relied_on:
    - "workflow/ARCHITECTURE_CONTRACT.md"
    - "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-50-historical-runtime-reconstruction-20261008.md"
    - "workflow/handoffs/luna-49-runtime-reproducibility-20261008.md"
    - "tests/test_luna44_canonical_fixture.py and verifier"
    - "run_luna46_depth_scaling_diagnostic.py"
    - "experiments/luna47f/PROTOCOL.md and diagnostic.py"
  label_information_boundary:
    - "No labels or neural/task outcomes entered any computation."
  timing_assumptions:
    - "No neural timing or scientific behavior was evaluated."
  reset_boundaries:
    - "No TPCN runtime was created or reset."
  resource_bounds:
    - "Read-only inspection of published evidence and test guards."
  authorized_scope:
    - "Classify historical fixture, source and retained determinism evidence."
    - "Review four reported regression failures and authorize a minimal correction-only contract if warranted."
    - "Park historical Linux reproduction if the missing capability does not invalidate canonical evidence."
  unauthorized_scope:
    - "No Luna-51 execution in this governance turn."
    - "No canonical or retained scientific artifact edits, regeneration or rebaseline."
    - "No scientific runtime-sensitivity replay, mechanism experiment, ACP or architecture change."
    - "No Luna-52 authorization."
  controls:
    - "Fetched remotes; verified HEAD == origin/main at da67433220d92d926d4c4e84e5b9fa08cda4bb10 and clean worktree before review."
    - "Verified Luna-50 execution is an ancestor of current HEAD."
    - "Luna-50 independent review outcome accepted; execution remained explicitly unavailable rather than contradicted."
    - "Canonical artifact hashes independently checked in the preceding accepted Luna-0 review and remain pinned by the new contract."
  measurements:
    - "Luna-44 compares alternate-runtime materializations to the canonical Linux fixture as an unconditional exact-output assertion."
    - "Luna-46 hashes checked-out catalog bytes against the pinned Git-object SHA despite verified CRLF-only checkout difference."
    - "Luna-47F stores hashes for all non-owned tracked files and compares that historic whole-repository set on later replay; consumed-input identity also includes materialization-specific byte hashes."
    - "Luna-47F protocol itself pins 12 consumed inputs and separately specifies live pre/post non-mutation."
    - "No tests or scientific runners executed during this read-only review."
  information_boundary_check:
    - "PASS: no experiment inputs were fed into neural computation."
  hardware_mapping:
    - "Not applicable; no hardware execution or equivalence claim."
  architecture_invariants_touched:
    - "No A01-A15 clause changed."
  preserves:
    - "Canonical fixture and provenance hashes."
    - "Luna-46 MIXED verdict."
    - "Luna-47 non-integrated status and absence of task efficacy/useful-growth evidence."
    - "Luna-50 BLOCKED disposition and unassigned numerical cause."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-51.agent.md"
    - "workflow/handoffs/luna-0-independent-review-luna50-and-authorization-luna51-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "No tests run; this is a governance-only review and authorization."
    - "Full-suite counts are reviewed from the Luna-50 handoff and not independently rerun in this decision."
  assumptions:
    - "The canonical fixture is the declared historical experimental object for existing results and can remain the reference for future experiments."
    - "Experiments that require newly generated point streams need an explicit runtime/determinism contract; they are conditionally blocked until then."
  unresolved:
    - "Fresh exact Linux regeneration and the first cross-runtime primitive divergence remain unestablished."
    - "Alternate-runtime effects on neural threshold/route/category decisions remain unknown."
    - "A next scientific causal question is not selected or authorized by this provenance decision."
  recommended_next_agent:
    - "Luna-51 correction-only implementation, then Luna-0 independent review."
---

# Luna-0 Review: Luna-50 Provenance Limitation and Luna-51 Authorization

## Decision

**CORRECTIVE PROVENANCE FOLLOW-UP AUTHORIZED.** Luna-50's accepted result is
**BLOCKED — HISTORICAL RUNTIME UNAVAILABLE**, which is a missing capability,
not evidence contradicting the historical fixture. Park the fresh Linux
reconstruction as an explicit provenance limitation. The canonical fixture
remains the authoritative historical input; exact fresh regeneration is not
claimed, and exact cross-runtime binary64 portability is not established.

Authorize exactly one correction-only successor, **Luna-51**, under
`.github/agents/luna-51.agent.md`. It is **AUTHORIZED / NOT EXECUTED**. It may
correct only the Luna-44, Luna-46 and Luna-47F provenance regression guards
and focused tests described there. It may not run scientific computation,
modify/rebaseline historical evidence, or authorize Luna-52.

## Repository State and Evidence

At review start, remotes were fetched; `HEAD == origin/main` at
`da67433220d92d926d4c4e84e5b9fa08cda4bb10`, the worktree was clean, and the
Luna-50 execution commit was in ancestry. The current workflow and changelog
record Luna-50's unavailable Linux environment, Windows-only control, preserved
canonical hashes, and four known regression failures. The Luna-50 execution
handoff records the blocked gate; its independent review accepted that result.

The accepted evidence supports these classifications:

| Question | Review classification |
|---|---|
| Historical fixture authenticity | **AUTHENTICATED RETAINED ARTIFACT**: canonical file and semantic digests are pinned; existing experimental results consumed this committed object. This authenticates the accepted artifact, not an independently recreated historical process. |
| Generator/configuration/input source authenticity | **CLOSED / AUTHENTICATED** through pinned Git-object identities and the canonical provenance manifest. |
| Historical within-runtime determinism | **CREDIBLY SUPPORTED BY RETAINED RECORDS**: two distinct historical invocation/PID records report the same fixture and digests. Original temporary outputs are unavailable, so the records are not a fresh independent audit. |
| Fresh historical reproduction | **NO**: Luna-50 could not provision Linux and did not run two historical-runtime materializations. |
| Cross-runtime exact binary64 portability | **NOT ESTABLISHED; evidence shows it is not general**: reviewed Windows outputs are deterministic within their runs but differ from the canonical Linux fixture. |
| Scientific validity of results that used the canonical fixture | **NOT CONTRADICTED**: those results used the authenticated committed fixture. Sensitivity of hypothetical/fresh Windows-generated inputs remains **NOT TESTED / UNKNOWN**, not invalidity. |

Canonical identities remain:

- Fixture SHA-256: `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`.
- Semantic digest: `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`.
- Provenance SHA-256: `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22`.

The first primitive cause remains unassigned. Platform/libm variation is
plausible but unproven.

## Regression Failure Review

### Luna-44: two cross-runtime exact comparisons

**HISTORICAL-RUNTIME INVARIANT APPLIED TOO BROADLY.** Exact fresh output is
valid when asserting the declared canonical environment, but unconditional
Windows equality is not a portable invariant. Preserve exact canonical
artifact verification and exact same-runtime independent-run determinism.
Report alternate-runtime mismatch without treating it as historical artifact
mutation. Do not delete or weaken the identity checks.

### Luna-46: retained catalog raw checkout hash

**PROVENANCE TEST DEFECT.** The pinned Git blob is valid; the Windows working
copy differs by CRLF and LF normalization exactly yields the pinned bytes.
This is the same class of canonical Git identity versus checkout-byte
confusion corrected by Luna-48. Authenticate the blob identity and parse/check
the exact governed materialization; substantive catalog changes must continue
to fail.

### Luna-47F: retained whole-repository and input inventory

**OVERBROAD PROTECTED-INVENTORY INVARIANT, WITH CHECKOUT-SENSITIVE INPUT
IDENTITIES.** Its protocol consumes a bounded set of twelve historical
scientific inputs and separately requires fresh pre/post non-mutation. The
implementation instead persists all non-owned tracked-file hashes and later
requires the current repository to match that historic inventory. This
confuses legitimate governance/source evolution with scientific input
mutation. Keep a bounded, historically anchored consumed-input/source/protocol
manifest; maintain a live pre/post check for changes during each run. Preserve
the retained result bytes and all scientific pins.

These three classes share one provenance principle but require distinct
checks. One task is appropriately bounded if it maintains independent
Luna-44 runtime, Luna-46 Git-object, and Luna-47F consumed-input acceptance
gates. Luna-47F's live non-mutation boundary must not be collapsed into the
Git-blob correction.

## Scientific and Runtime Boundary

Historical Linux exact regeneration is a **PARKABLE PROVENANCE LIMITATION**
for work consuming the committed canonical fixture. It is a **CONDITIONAL
BLOCKER** for experiments that intend to regenerate that input and claim exact
historical-runtime reproduction. The architecture contract and first-benchmark
workflow do not require perpetual regeneration of a frozen point fixture.

Downstream scientific runtime sensitivity is **USEFUL BUT NON-BLOCKING** if
future experiments use the authenticated canonical fixture. Do not execute or
authorize that experiment here. If a future experiment depends on freshly
generated alternate-runtime inputs, it must explicitly address that limitation
before making claims that depend on those inputs.

Scientific state is unchanged: Luna-46 remains **MIXED**; Luna-47 does not
establish an integrated mechanism, task-level efficacy, or useful structural
growth; Luna-47G remains synthetic tolerance evidence; hardware equivalence is
not established. This review does not choose the next causal mechanism
question. Existing evidence is insufficient to authorize a broad composition
experiment.

## Luna-51 Scope and Gates

Luna-51 owns only the provenance guard/test surfaces listed in its contract.
It must preserve exact canonical fixture/provenance identities and all retained
scientific artifacts; prove rejection of protected source, revision, input,
protocol/configuration, result and fixture mutations; prove acceptance only of
the exact allowed checkout transformation and unrelated later repository
evolution; and restore the relevant and full repository suite to green without
skips, broad xfails, deleted assertions, blanket normalization or rebaselining.
No A01-A15 clause or ACP changes.

**Next required flow: Luna-0 authorization -> Luna-51 correction-only
execution -> Luna-0 independent review.** This commit authorizes Luna-51 but
does not execute it. No Luna-52 is authorized.

## Subsequent governance decision — Luna-51 follow-ups

This section records a later decision; it does not change the scope or
historical outcome above. After the Luna-51 publication was independently
accepted with follow-up, Luna-0 reviewed the remaining Luna-47B historical
source compatibility failure and Luna-47F public `--check` coverage gap.
Both are authorized together as **Luna-52 corrective follow-up / NOT
EXECUTED**, from starting revision
`e6bd96a13eb2d5bb19fce8ef6c4b3aa3ec8f8c2e`. See the
[Luna-52 governance handoff](luna-0-review-luna51-authorize-luna52-20261008.md)
and [Luna-52 contract](../../.github/agents/luna-52.agent.md).

Luna-47B must retrieve and use its historical Luna-46 analyzer source, while
separately recognizing the Luna-51-reviewed current source. Luna-47F must add
isolated adversarial tests through the real `--check` entry point. No retained
scientific evidence may change, and no scientific work, architecture change,
or Luna-53 is authorized. The required next flow is **Luna-52 execution ->
independent Luna-0 review**.