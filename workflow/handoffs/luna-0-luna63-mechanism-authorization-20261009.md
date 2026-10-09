# Luna-0 — isolated alternative mechanism authorization

## Prior independent review, then authorization

The [independent Luna-62 review](luna-0-independent-review-luna62-20261009.md)
was completed first: **PASS WITH LIMITATIONS**, design only, reviewed
`8123147e04c6044d12023f541cf63130cdbb7dcc`, design commit
`c33f4195d10d2c5de8e715ac4ad63349a724aa34`.
The FIFO-like candidate remains **PROPOSED — ACP REQUIRED**, not adopted
or discarded. Its unresolved close/bridge/flush/drive/A15 gates remain.

| Lane | Disposition | Precisely authorized future scope |
|---|---|---|
| 63A | **AUTHORIZED / NOT EXECUTED** | Isolated binary adaptive-decay scalar mechanism, frozen below/in agent contract; branch and published freeze are execution prerequisites |
| 63B | **DESIGN PREREQUISITE REQUIRED / DESIGN ONLY AUTHORIZED** | Define missing bounded local PCN equations/state separation and unexecuted protocol; no trials or implementation |
| 63C | **NOT YET BOUNDED** | No executable or design-worker contract created; exact missing field recorded below |

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-63 alternative mechanism lane governance"
  task_id: "luna-0-luna63-mechanism-authorization-20261009"
  component: "Isolated pre-ACP mechanism/design authorization only"
  status: "complete; A authorized, B design prerequisite, C not yet bounded; none executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "8123147e04c6044d12023f541cf63130cdbb7dcc"
  result_revision: "uncommitted governance; parent handles publication"
  dependencies: ["Independent Luna-62 design review", "Owner 1033-line mechanism attachment with current narrower scope", "Contract and ACP process", "Source and historical primitive inspection"]
  owner: "Project owner"
  classification: ["GOVERNANCE", "ISOLATED EXPERIMENT AUTHORIZATION", "DESIGN PREREQUISITE"]
  hypothesis: "Adaptive retention is independently testable; vector interpretation and nonlinear replay need defined models first."
  counter_hypothesis: "A lane requires ungoverned state, evaluator feedback or invented dynamics to produce support."
  interfaces_relied_on: ["Local exponential recurrence", "Current scalar predictor/E2", "Isolated experiment allowance"]
  label_information_boundary: ["No truth/sequence buffer/evaluator replay in computation", "Cues carry only gate values"]
  timing_assumptions: ["Prior gate settles elapsed interval", "TTL equality preempts cue", "No global neural clock"]
  reset_boundaries: ["A: fresh instance and absolute TTL=64", "B: must specify finite proposed lifecycle"]
  resource_bounds: ["A: one scalar, 32 local events/instance, 33 frozen instances", "B: one compartment, two ports/encoding coordinates, at most 10 scalar coordinates"]
  authorized_scope: ["New lane A/B contracts", "This handoff", "Additive workflow/changelog indexes"]
  unauthorized_scope: ["All scientific execution here", "Production/default/test/artifact edits here", "Luna-62 or ACP edits", "63C execution", "Luna-64/integrated echo"]
  controls: ["A frozen normal/HOLD/release/switch/zero/expiry/duplicate matrix", "B matched-count/count-confound/scalar/commutative design controls"]
  measurements: ["None in governance; future A direct retention/closed-form error only"]
  information_boundary_check: ["Read-only source inspection; no scientific process instantiated"]
  hardware_mapping: ["A gate/register/expiry qualitative mapping only", "B/C precision/vector-field mapping unresolved"]
  architecture_invariants_touched: ["A01-A15 considered; ACP-0008 positivity/fixed-effective-decay departure named for A only"]
  preserves: ["Core A01-A15", "ACP statuses", "Luna-62 candidate", "Luna-61 conversation-only PASS caveat", "Prediction/error/credit semantics"]
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-63a.agent.md"
    - ".github/agents/luna-63b.agent.md"
    - "workflow/handoffs/luna-0-luna63-mechanism-authorization-20261009.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All scientific, unit/regression/replay and hardware execution; governance only"]
  assumptions: ["Owner authorizes isolated named departures, not architecture adoption."]
  unresolved: ["Published contract SHA", "Future isolated worktrees/executor", "B equations", "C vector field and event conversion"]
  recommended_next_agent: ["Luna-63A only on frozen isolated branch", "Luna-63B design only", "Independent Luna-0 after each deliverable", "Owner/Luna-0 for missing C design scope"]
```

## Outcome, process and authority

OBSERVED: the entire current 1,033-line read-only attachment was read in
sections. This invocation is governance only. The reviewer/author did not
stage, commit or push; the parent orchestrator owns the owner's requested
documentation publication. No branch/worktree was created and no scientific
executor ran. Read-only Git and documentation checks are not experiments.

OBSERVED: architecture contract authority permits named departures on
isolated branches. ACP README explicitly permits an experiment within
authorized scope on an **isolated experiment branch**, not promotion to core.
Thus this owner-authorized pre-ACP scalar probe is lawful only as an opt-in,
standalone experimental model with named deviations. A separate directory
on main is insufficient. Nothing here accepts an ACP or implements the
Luna-62 chain. Adopted/persistent production semantics still need proposal,
owner decision, verification and contract/changelog governance.

`tpcn-luna-workflow/` governing paths are absent; the existing repository
`workflow/` counterparts were used as documented in the independent review.
Tracked instruction inventory found no AGENTS.md, copilot-instructions.md
or separate instruction files; existing agent patterns and the requested
customization `references/agents.md` were read. Quoted name/description and
minimal tool aliases follow those patterns; B has no execute/agent tool.

Luna-61 PASS remains conversation-provided, not tracked-verified. Actual
Luna-62 authorization is `084033b03968c256dc47c8d24fbafa56f085b729`;
the historical mistype is not repaired in place.

## Source/provenance register and actual model availability

All ranges/pins refer to the reviewed baseline, not claims of runtime tests.
The governing/source pins in the independent review are authoritative inputs
to both contracts; this table adds the relevant primitive evidence.

| Actual source | Git blob | Ranges and observed significance |
|---|---|---|
| `workflow/docs/architecture_proposals/ACP-0008.md` | `1fa832472ce1797061b117e96417d88238a35491` | 1-143, full: opt-in scalar z, finite positive lambda_z, fixed config; discharge on qualifying external inputs; M staged separately |
| `experiments/luna47a/PROTOCOL.md` | `2c0ceb1250af69a712e5f5ac0e5dcaa50efc6d9c` | 1-142: event-time signed impulse accumulation, finite-rate historical variants, no discharge/output, not normalized WEMA |
| `experiments/luna47d/PROTOCOL.md` | `a5e9e596bb8a2c62a91f8b5ae6d477dd15e7b380` | 1-144: synthetic scalar charge drain, scheduled opportunities, not TPCN neuron |
| `experiments/luna47d/model.py` | `f4143b7e2c5809b9082b072ff8deb5501d4feddf` | 1-180: scalar q/analytic leak/threshold/dissipative drain; no spiral coordinates/vector field |
| `Initial-Architecture-Attempts/TPCN_inspiration/wema_predictive_coding_docs/02_wema_formulation.md` | `7197a294a294aa7701fa232f17e35fb542cad7e6` | Full: indexed `y_t=alpha_t*x_t+(1-alpha_t)*y_(t-1)`; learnable trust concept |
| Same directory, `05_multiscale_wema.md` | `ea41ab5ec77768feb46975b9b443f9e0ef3733b8` | Full: independent filter bank and weighted sum, not proposed local PCN equations |
| `Initial-Architecture-Attempts/TPCN_inspiration/predictive_coding/cpcn/cpcn.py` | `a9c7f9353566085462a53eec020d7e262996f1c7` | 1-120: layered reservoir/world-step model, global error and optimizer; not governed event-local spike interpretation |
| `tpcn/predictive_coding.py` | `8c391703bb2361c77fc768407eb343da73677166` | 1-300: scalar keyed prediction/error matching/expiry, not multidimensional F_PCN |
| `tpcn/excursion_neuron.py` | `c0bdece6b15009db4e2b7d69c3242be174b5de80` | 60-160,371-499,530-735,847-1090: x/z scalar state, captured m_peak/polarity, analytic decay and S/M scheduled emission/return |

Read historical independent Luna-47 review 133-176: A partially supported
finite retention, D supported synthetic regimes only; other lanes have
explicit proxy/model/documentary limitations. These are historical reported
results, not reproduced here or permission to compose them.

Targeted repository search for peak-hold/vector-field/spiral-return/local
interpretation, plus governing/current/legacy source reads, found no frozen
model matching the owner's complete proposed dynamics. This is scoped
source evidence, not a proof that no untracked/private model exists.
Legacy spatial visualizer flow/curl is reservoir/display context, not a
governed local nonlinear output trajectory. Benchmark spiral input geometry
is not neuron spiral-return dynamics. Neither may satisfy the missing field.
`m_peak`/captured polarity is excursion amplitude evidence, not a governed
polarity-preserving input peak-hold pipeline. No peak-hold model is invented.

## 63A exact freeze and lawful departure

See [63A contract](../../.github/agents/luna-63a.agent.md) for the complete
matrix, future owned paths and checks. Frozen equation:
`dz/dt=-(1/8)*R*z`; R binary; zero leak identity, not floating infinity;
z0=-3/4,0,+3/4; |z|<=4; TTL=64; at most 32 events/instance.
H in {2,8,32}; unequal observation intervals and prior-gate-switch negative
are fixed. Eleven schedules x three initial values = 33 instances; exact
initial/replay and independent Decimal closed-form oracle, abs+relative
tolerance `1e-12 + 1e-12*abs(expected)`; exact HOLD bits/timing/status.
Normal, HOLD, delayed normal comparator, no-preload, duplicate cue, switch
and expiry equality controls are compulsory. No partial gate/no parameter
search/no noise. Invalid/fault rows remain visible.

Cue first settles dt with R_old and then changes leak only; it never
injects state or writes a spike/threshold. Expiry preempts equal-time cue
in every handler. New preload occurs only at initialization. The model
has no output dynamics: output disconnected/no-output is a by-construction
anti-command check, not support for canonical recall or output release.

Named isolated departures: ACP-0008's strictly positive effective decay
and immutable per-execution effective rate become zero HOLD leak and
runtime-local gate-modulated rate; TTL is a declared wrapper lifetime.
Production IntegrationConfig/E1Config are unchanged and never mutated.
A01-A08 causal/local/bounded boundaries apply; A06/A09-A11 capabilities
are not part of this component assay and remain required in TPCN.
A12-A13 optional; A14 absent; A15 qualitative only. No core promotion.

## 63B disposition and design separation

See [63B contract](../../.github/agents/luna-63b.agent.md).
No frozen local F_PCN currently matches the proposed peak/delta/z dynamics.
Authorize two documentation files only, not a random network or trials.
Design envelope: one compartment, A/B ports, two z coordinates, at most
10 scalar coordinates across roles and two local prediction records.
Must specify polarity/capture/expiry, predictor/explicit error equations,
causal interpretation, bounded elapsed vector evolution, all state roles
and the unexecuted separation criterion. If this cannot be done honestly
as a PCN, report BLOCKED rather than relabel an arbitrary map.

AB/BA and AAB/ABA matched-count comparisons; AA/A count-confounded control;
identical-history replay, finite delay robustness, scalar leaky recency
control and commutative aggregate baseline. Scalar WEMA is not universally
order-insensitive. Freeze schedules, finite constants, numerical tolerances
and separation margins in the design before independent review; no execution
authorization follows merely from a proposed equation. No RECALL/decoder.

## 63C exact missing field — no executable contract

**NOT YET BOUNDED.** The proposed notation
`dx/dt=G(R,x,z)*F(x,z)` with possible `G(R)=R` defines only a gate, not F.
E2 has scalar x and finite S/M scheduled events, not a frozen proposed
multidimensional/spatial spiral-return vector field. Optional scalar z
does not make that field exist. Historical scalar 47D is not canonical
ExcursionEmission and cannot substitute for it.

Missing before any 63C executable authorization:

1. Governing source path/revision and exact finite-dimensional F(x,z),
   parameters/domain, displaced/neutral attractors and bounded return proof.
2. Separation of retained z versus excursion coordinates; which variables
   HOLD freezes and which continue; prior-gate interval/tie/expiry semantics.
3. Canonical event conversion surface, polarity/amplitude/identity and
   strictly future emission rule derived from trajectory, not a digital cue.
4. Predicted neutral/subthreshold/single-excursion conditions, and a
   multi-spike region only if mathematically present; exact independent
   oracle, tolerances, schedules, budgets and observation/TTL boundary.

Required future controls would be neutral+RECALL, subthreshold+RECALL,
no-RECALL to finite expiry, identical preloaded states after several holds,
and ordinary ungated trajectory reference. They are **not executable
fixtures** yet. No spiral, oscillator, threshold surface or parameter set
is invented to make this lane appear ready.
The owner permits bounded alternatives but does not require three contracts.
No 63C design-only agent is necessary for the current deliverable: owner/
Luna-0 must separately scope missing-field design or supply a governed field.
B is not authorized to fill C's output dynamics.

## Future ownership, regression and independent-review gates

No parallel execution authorized here. Future A/B use isolated branches,
disjoint files/artifacts and no interlane results. A owns only the exact
new module/test/artifact/handoff files in its contract; B only its two
design documents. Neither edits shared governance/core/historical records.
C owns nothing. No branch is created or contract executed by this record.

Future A must run focused analytic/mechanism/deterministic/oracle/fault
tests and the seven named event/E2/ACP-0008/predictor/47A/47D regression
files. Report exact counts/skips, inherited failures, interpreter/platform
and provenance/integrity checks. Production changes are forbidden; stop
instead of treating full-suite requirements as permission to touch core.
No full suite required for the isolated-only scope; B runs no science.

Pin scientific starting SHA, published authorization SHA/blob,
pre-outcome freeze, implementation/design revision, constants/schedules,
initial state, raw trace, results/replay and canonical Git versus checkout
byte identities. Initial/replay is deterministic replication, not independent
samples or task generalization. No hidden oracle import or answer feedback.
After each deliverable, independent Luna-0 must inspect the exact model/
equations, controls/oracle, locality, bounds, artifact identities, regressions
and non-claims. Relevant reviews must close before even considering a
separately bounded integrated prototype. No automatic successor.

## Validation record, remaining issues and reproduction

Actual: fetched origin, verified clean initial main=origin/main at stated
baseline; resolved Git blobs/commit ancestry and historical mistype; read
governing sources, attachment/customization reference and relevant code;
completed the independent review before authorization; authored only
governance documents/contracts/index additions using apply_patch.
Documentation whitespace/scope/frontmatter/link checks follow the patch.
All scientific tests/runners/training/replay/benchmarks/hardware are
**NOT RUN / NOT AUTHORIZED HERE**. No scientific PASS is recorded.

| Actual post-edit check | Observed result / limitation |
|---|---|
| `git diff --check` | PASS, no tracked whitespace diagnostics |
| `git diff --no-index --check -- NUL <each of four new files>` | PASS, no whitespace diagnostics; content-difference exit 1 on each is expected |
| Tracked diff plus untracked inventory against six-file allowlist | PASS, exactly the two new contracts, two new handoffs and two additive indexes |
| `git diff --cached --name-only` | Empty; no staged changes |
| Frontmatter lexical check for quoted name/description, tool list, agents list and delimiters | PASS both new contracts; not a runtime agent-load/schema execution test |
| Relative link target existence in four new files | PASS |
| Editor Problems check for all six paths | No errors reported; not scientific validation |
| Final ref comparison | HEAD and origin/main remain the reviewed `8123147...`; worktree intentionally has six unstaged/new documentation files |

Dataset/splits/accuracy/prediction loss/event counts/energy/utility/task
latency/capacity/hardware evidence: N/A to governance; not measured.
Integration readiness: **not established**. A awaits published freeze and
isolated executor; B awaits design; C awaits governed field. No architecture
promotion, predictive/error/reward rewrite, FIFO rejection or integrated echo.

Reproduce governance by reading pinned sources and contracts at baseline,
not by running experiments. Parent owns documentation publication and pins
the governance content revision in this handoff after commit. Safe rollback,
if owner requests, uses a documentation-only follow-up affecting only these new
governance files/additive index sections, preserving historical records.
Next bounded assignments: Luna-63A isolated scalar probe; Luna-63B
design-only prerequisite; independent Luna-0 after each. C remains pending
owner/Luna-0 missing-field design decision. No Luna-64.
