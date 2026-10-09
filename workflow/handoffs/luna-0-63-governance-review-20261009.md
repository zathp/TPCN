# Luna-0 governance review — Luna-63A/B evidence integration and next bounded work

**GOVERNANCE REVIEW COMPLETE — Luna-63B execution remains blocked on a numerical prerequisite.**
This record integrates the owner's 781-line governance assignment. It does not
authorize experiments during this governance pass.

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-63A/B evidence integration and Luna-63C design authorization"
  task_id: "luna-0-63-governance-review-20261009"
  component: "Evidence integration, architecture governance, bounded successor decisions"
  status: "complete; A/B evidence integrated by distinct dispositions; 63B numerical prerequisite remains blocked"
  contract_version: "1.2"
  branch: "main"
  base_revision: "e52098b2141a3f121f23b512e877783a64ef8baa"
  result_revision: "Pending final governance publication"
  dependencies:
    - "Published Luna-63A final revision 1c3e33d6285c2d3aeb107f27aad07e57de2ba50f"
    - "Published Luna-63B final revision fe3ebe5fdd2e018e79dd640fa4f94548ebba8701"
    - "Independent Luna-0 reviews of the exact A and B publications"
    - "Owner-supplied governance assignment, 781 lines"
    - "Architecture contract v1.2 and current workflow/ACP sources"
  owner: "Project owner"
  classification: ["GOVERNANCE", "INDEPENDENT REVIEW", "EVIDENCE INTEGRATION"]
  hypothesis: "Reviewed evidence can be retained without converting isolated experimental departures into core/default behavior."
  counter_hypothesis: "Integration would imply promotion, lose provenance, or obscure an unresolved numerical prerequisite."
  interfaces_relied_on: ["Published lane refs, immutable artifacts, handoff and review records"]
  label_information_boundary: ["No task labels, sequence answer, or evaluator data entered a model"]
  timing_assumptions: ["No neural/runtime time behavior exercised by governance"]
  reset_boundaries: ["No stateful experiment or runtime instantiated"]
  resource_bounds: ["No scientific execution in this governance pass"]
  authorized_scope:
    - "Classify and decide evidence integration for exact A/B revisions"
    - "Write this Luna-0 governance record and update workflow/changelog"
    - "Create bounded Luna-63C design-only assignment"
    - "Independently substantiate 63B oracle/tolerance and decide readiness"
    - "Publish authorized governance documentation"
  unauthorized_scope:
    - "Run new 63B or 63C experiments, simulations or efficacy studies"
    - "Integrated sequence echo, recall/replay experiment, task training or scoring"
    - "Luna-64, ACP adoption, architecture/core/default promotion"
    - "Merging the 63A executable lane into main"
  controls:
    - "Separate branch content decisions for A and B"
    - "Static check of 63A module imports/default behavior and test scope"
    - "Independent read-only review of each exact published lane"
    - "Independent mathematical oracle/tolerance substantiation before any B execution decision"
  measurements:
    - "Existing 63A retained measurements and test counts, independently rechecked where stated"
    - "No new scientific measurements"
  information_boundary_check:
    - "No A/B lane results cross-used by either scientific lane"
    - "63C design contract forbids evaluator truth, sequence buffers and unpublished lane results"
  hardware_mapping: ["No hardware execution or equivalence claim"]
  architecture_invariants_touched: ["A01-A15 reviewed; no clauses amended"]
  preserves:
    - "Luna-62 remains proposed and ACP-required"
    - "ACP-0008 remains unchanged"
    - "A/B isolated experimental departures are not promoted"
    - "63A manifest containing-commit placeholder remains visible"
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_63B_LOCAL_PCN_STATE_DESIGN.md"
    - "workflow/handoffs/luna-63b-local-pcn-state-design-20261009.md"
    - ".github/agents/luna-63c.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-luna63b-numerical-prerequisite-review-20261009.md"
    - "workflow/handoffs/luna-0-63-governance-review-20261009.md"
  tests_added: []
  tests_passing:
    - "Luna-63A focused: 69 passed"
    - "Luna-63A required regressions: 327 passed"
  tests_failed: []
  tests_not_run:
    - "Full test suite"
    - "63B numerical oracle, runtime, replay, or separation protocol"
    - "63C implementation, simulation, event conversion, or hardware"
    - "Integrated sequence echo"
  assumptions: ["The owner's attachment is the active governance instruction."]
  unresolved:
    - "63B scalar exponential-error certificate and exact observation/metadata oracle"
    - "Owner/Luna-0 resolution of 63B numerical freeze; execution remains unauthorized"
    - "Independent review of future 63C design deliverable"
  recommended_next_agent: ["Owner/Luna-0 to resolve the 63B numerical prerequisite; separately assigned Luna-63C design worker after this governance publication"]
```

## 1. Starting identity and governing sources

OBSERVED: authoritative starting `main` and `origin/main` were clean and equal
at `e52098b2141a3f121f23b512e877783a64ef8baa`. The separately registered lane
worktrees were clean at their published final revisions:

| Lane | Final local / remote SHA | Independent review |
|---|---|---|
| Luna-63A | `1c3e33d6285c2d3aeb107f27aad07e57de2ba50f` | PASS WITH LIMITATIONS |
| Luna-63B | `fe3ebe5fdd2e018e79dd640fa4f94548ebba8701` | PASS WITH LIMITATIONS — design only |

Read the current `workflow/ARCHITECTURE_CONTRACT.md` (v1.2), `workflow/
ARCHITECTURE_CHANGELOG.md`, `workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`, proposal README/template,
handoff template, Luna-62 independent review, Luna-63 authorization, both lane
contracts, both complete published handoffs, both published lane diffs, and
the owner's current governance attachment. Repository sources use `workflow/`;
the historical alias `tpcn-luna-workflow/` is not present. No contract or ACP
revision is inferred from an unverified version label.

## 2. Evidence integration decisions

### Luna-63A — KEEP BRANCH EXTERNAL; RECORD SHA ON MAIN

The baseline-to-final diff is exactly ten authorized files:

| Classification | Files |
|---|---|
| Experimental implementation | `experiments/luna63a/{__init__.py,model.py,run.py,protocol.json,README.md}` |
| Experimental tests | `tests/test_luna63a_adaptive_decay.py` |
| Retained evidence/artifact | `artifacts/luna63a/{results.json,replay.json,manifest.json}` |
| Execution handoff | `workflow/handoffs/luna-63a-binary-adaptive-decay-20261009.md` |
| Review record | Independent review recorded in this governance handoff |

The module is opt-in and has no production import path; the model is imported
only by its runner/tests. Existing production modules and tests are unchanged.
The new test is additive and verifies the isolated model; it does not weaken
existing invariants. The execution handoff explicitly names the zero-leak,
mutable-gate and terminal-TTL departures from ACP-0008.

Because the authorized mechanism must remain on an isolated experiment branch,
putting executable departure code and its tests on `main` would undermine that
boundary even in a separate directory. The external branch preserves a
reproducible implementation, protocol, immutable outcomes, manifest and
execution handoff at the exact reviewed SHA. This main handoff records its SHA,
accepted claim, measurements, test evidence, and limitations. No A code or
279-KB outcome JSON is copied to main.

### Luna-63B — CHERRY-PICK REVIEWED EVIDENCE ONLY

The branch diff is exactly two Markdown files: one proposed design report and
its execution/design handoff. It contains no executable PCN, tests, trials, or
scientific artifacts. The independent review classifies the equations, bounds,
and order-separation protocol as a **design proposal**, not validated runtime
behavior. Those two reviewed documents were cherry-picked onto main without
the lane branch's unrelated implementation (none exists). The report retains
prospective labels and the handoff states scientific/runtime checks were not
run. The 63B publication SHA remains pinned in the imported handoff.

This does not validate the proposed oracle/tolerance or authorize an
experiment. That is a separate independent prerequisite recorded below.

## 3. Luna-63A accepted conclusion and provenance limitation

**OBSERVED:** the frozen isolated software probe supports exact binary64 HOLD
of a bounded scalar under `R=0`, followed by the frozen analytic recurrence
under `R=1`, with prior-gate settlement and terminal TTL equality semantics.
The exact model is `dz/dt = -(1/8) R z`, `R ∈ {0,1}`. It says only that this
scalar state can wait and resume decay.

The published outcome contains 33 instances and 249 rows per materialization;
results and replay are byte-identical with SHA256
`58120206f245c9d59e0b0a621ee450ebea393b2ed149ea9e1bbb9dbd126e6b7a`.
The reviewed handoff reports 69 focused and 327 required regression tests;
both commands were rerun on the exact isolated branch here and passed.

The manifest's `publication.outcome_containing_commit` field remains a
documented placeholder. The handoff pins outcome commit
`0b3913641ff0ecf0afc4f3c987ceb79635159d5d` and final published commit
`1c3e33d6285c2d3aeb107f27aad07e57de2ba50f`. Per owner instruction, no history
rewrite or unapproved manifest correction is performed.

Not established: event identity, symbol/order memory, recall/replay, output
gating, learning, task efficacy, hardware equivalence, ACP acceptance, core
or default promotion. No integrated echo was run.

## 4. Luna-63B independent design review and numerical gate

The independent review of publication `fe3ebe5fdd2e018e79dd640fa4f94548ebba8701`
found **PASS WITH LIMITATIONS — design prerequisite met**, with no correction
required to the two design documents. It checked scope, exact update order,
ten-scalar budget, bounded lifecycle, local fixed prediction/error effect,
conditional noncommutativity, matched-count/recency/scalar controls, and
publication provenance. No implementation, oracle, simulation, replay,
non-interference test, or trial was executed. In particular, the proposed
`0.04 SU` margin and numerical tolerance are not observed outcomes.

**INDEPENDENT NUMERICAL REVIEW — BLOCKED:** the separate Luna-0 review
independently derived the candidate's rational terminal-state equations and
found the 64u-per-packet bound and geometric bound
`512u*((9/8)^32-1) < 2.45e-12 SU` defensible under stated operation-order
assumptions. It found the candidate-state and separation tolerances ample
analytically, but did not adopt the proposed 0.04 SU criterion. The full
prerequisite remains blocked:

- disposition: **LUNA-63B NUMERICAL ORACLE PREREQUISITE REQUIRED**;
- the leaky scalar control's exponential-error budget lacks a library/build
  error guarantee; 80-digit Decimal alone is not a certificate;
- the complete exact observation/metadata oracle does not freeze fault-time
  timestamp handling, expiry/validation precedence, scheduled/lazy observation
  settlement, IDs/generation/deadline cleanup, or signed-zero conventions;
- prefix versus terminal/HOLD observations need explicit anchors for long
  controls;
- no 63B execution authorization or experiment contract is issued;
- no trial is run in this governance pass.

The independent review's exact candidate equations, control oracle, forward-
error derivation and blockers are preserved in
`luna-0-luna63b-numerical-prerequisite-review-20261009.md`. Do not pick another
tolerance or edit constants to force execution. The owner/Luna-0 must publish
the exact platform, operation order, scalar exponential error certificate,
complete metadata and observation semantics, oracle ownership, and explicit
disposition of 0.04 SU before a new separately versioned execution
authorization can be considered.

## 5. Luna-63C design-only authorization

The owner-supplied requirements make a **design-only** 63C prerequisite
sufficiently bounded to assign, not to execute. New contract
`.github/agents/luna-63c.agent.md` requires comparison of candidate dynamical
families and specification of at most one explicit bounded vector field,
stable rest, HOLD/RECALL gating, neutral and subthreshold non-emission,
single-excursion output, return-to-rest, strict-future event conversion,
independent numerical criteria, and an unexecuted falsification protocol.
It forbids implementation, simulation, trials, integrated echo, ACP/core
promotion, and Luna-64. The design must report **LUNA-63C DESIGN STILL
UNBOUNDED** if those equations/criteria cannot be made explicit.

No 63C design report or scientific run is produced here. Independent Luna-0
review remains mandatory after a future design deliverable; even a bounded
design only makes a separate mechanism decision eligible.

## 6. Architecture status and next gates

No A01-A15 clause, `workflow/ARCHITECTURE_CONTRACT.md`, or ACP was changed.
The isolated 63A zero-leak behavior is not promoted into ACP-0008's fixed
positive-decay default. The 63B vector/identity-HOLD proposal remains an
experimental design. Luna-62 remains **PROPOSED — ACP REQUIRED**; it is
neither adopted nor discarded.

No task efficacy, training, reward/credit change, hardware validation, or
integrated sequence echo ran. **No ACP was adopted. No Luna-64 was authorized.**
The next bounded actions are: (1) close the independent 63B oracle/tolerance
gate and then decide whether to publish a separate execution authorization;
(2) assign the newly authorized 63C design-only prerequisite on an isolated
worktree; and (3) review its deliverable before any experiment. These tracks
must not consume one another's unpublished evidence.

## Validation and publication status

| Check | Result |
|---|---|
| Main starting branch/ref/worktree | PASS at owner-supplied baseline |
| A and B local/remote final branch SHAs | PASS; exact refs above |
| A/B baseline diff scopes | PASS; A exactly ten allowed paths, B exactly two documentation paths |
| A isolated module/default boundary | PASS by static search and file review |
| A focused tests | PASS, rerun: 69 passed |
| A required regression tests | PASS, rerun: 327 passed |
| B rational candidate oracle / binary64 recurrence bound | PASS analytically under stated operation order |
| B full oracle/tolerance prerequisite | BLOCKED: scalar exponential certificate and exact metadata/observation oracle unresolved |
| 63B/63C experiments, simulation, efficacy, hardware | NOT RUN / NOT AUTHORIZED |
| Integrated echo | NOT RUN / NOT AUTHORIZED |
| Full suite | NOT RUN; documentation/governance plus isolated A tests only |
| Main commit/push/fetch/clean verification | PENDING final records |

**Next assignment:** owner/Luna-0 resolve the listed 63B numerical/oracle
blockers before any execution decision. After governance publication, a
separately assigned design worker may execute only the 63C documentation
contract above. No automatic experiment or architecture successor is
authorized.
