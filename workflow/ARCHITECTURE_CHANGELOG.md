# Architecture Changelog

## Luna-0 owner-directed ACP-0008 calibration decision — Luna-41 AUTHORIZED / NOT EXECUTED - 2026-10-05

The project-owner-directed follow-up is sufficiently bounded for
**Luna-41 AUTHORIZED / NOT EXECUTED**. It may calibrate only the existing
optional ACP-0008 `decay_rate_z` configuration over the predeclared finite set
`{0.1, 0.05, 0.025, 0.0125}`. `theta_E=1`, `theta_Z=1`, `input_gain=1`,
`z_max=4`, fast decay `1`, ACP-0007 disabled, and all production behavior
remain unchanged. Phase A uses normalized routed `0.4` inputs, a 12.9
near-gap and a 51.6 far-gap with isolated, near-pair, near-triple,
far-triple, negative-sign, and integration-disabled controls. It requires
equation-consistent, bounded state; exactly one integration-mediated near
triple emission; no control emissions; neutral return; and deterministic
replay. Selection is the largest passing decay rate; no parameter/grid
expansion is authorized. Analytic equations predict only `0.0125` will pass,
but this is not a runtime observation.

Only after Phase-A selection is frozen may Phase B characterize paired
unlabeled fixed-`w=1` relay-stream arms (calibrated, default, disabled).
Task outcomes cannot select or retune the parameter; no-emission is a valid
negative result. This is configuration evidence under accepted ACP-0008,
not an architecture change, efficacy study, or promotion. ACP-0008 remains
experimental, opt-in, and unpromoted. Luna-40's independent no-candidate/
no-admission verdict, and all previous Luna/ACP findings, are unchanged.
See `.github/agents/luna-41.agent.md` and
`workflow/handoffs/luna-0-acp0008-calibration-decision-20261005.md`.

## Luna-0 independent post-Luna-40 review — existing structural growth and effective routed drive - 2026-10-05

**NOT SUPPORTED IN THIS SETUP; EXECUTION CONTRACT PASS; NO PRODUCTION
DEFECT; NO LUNA-41 AUTHORIZED.** Independent review of the completed
Luna-40 artifact confirms the exact negative branch **NO LEGAL EDGE
ADMISSION**. Across five seeds and four arms (1,280 character runs), no
relay/destination canonical emissions or source/destination temporal pairs
formed, so there were no candidates, attempts, admissions, shortcut routes,
destination receptions, or ACP-0008 `z` updates. Source emissions and
`source->relay` routes were 1,715 per arm. All paired neural records and
runtime/resource projections match; the full artifact digest was independently
recomputed and matches both replay records. The focused 11-test suite and the
full repository suite (1009 passed, 1 skipped because CUDA is unavailable)
pass. No production defect or architecture change is established. The run
does not test effective drive after admission, makes no efficacy or ACP-0008
promotion claim, and applies only to its frozen fixture. Historical
Luna-33/34/37/38/39 and ACP-0007 verdicts remain unchanged; no Luna-41 is
authorized. Review: `workflow/handoffs/luna-0-independent-review-luna40-effective-routed-drive-20261005.md`.

For the architecture question, the answer under this fixture is **no**:
growth did not engage because the source-local candidate was absent. Existing
APIs composed without a blocker, but no conclusion is available about
post-admission convergence or temporal alignment. Luna-39's default `w=1`
integration result (`max |z|=0.763164`, no emission) and static `w=2`
sensitivity (31 integrated emissions, `max |z|=1.118173`) are context only;
Luna-40 had no destination input and cannot establish that convergent
topology substitutes for stronger individual coupling. Return the
no-relay-emission boundary to the project owner; no successor is authorized.

# Luna-0 owner-directed audit — routed-strength capability; Luna-40 AUTHORIZED / NOT EXECUTED - 2026-10-05

**No edge-weight plasticity exists.** `Edge` is immutable and Model-B
transfer remains the static N2 transform `tanh(w * payload)` followed by the
declared divider/reference transform; `w` is bounded `[-2, 2]` at
construction. Reward and eligibility update local credit only. The accepted,
opt-in ACP-0007 `e2_local_temporal` mechanism can change effective routed
drive only by adding a locally evidenced, bounded convergent edge, with
default fixed Model-B parameters (`w=1`, `d=1`, `r=0`) and a declared positive
delay. Fan-in, edge/routing capacities, candidate state, and growth attempts
remain bounded and deterministic. Prior Luna-12I and independent Luna-28
evidence establishes mechanism-level candidate/admission/routing behavior,
not task efficacy or an ACP-0008 discharge result.

The independently reviewed Luna-39 result is **PASS WITH FOLLOW-UP**:
default `w=1` ACP-0008 integration reached `max |z|=0.763164` with zero
destination canonical emissions; the predeclared static `w=2` sensitivity
produced 31 trace-verified integration-mediated emissions on 27/320
characters and zero direct emissions. ACP-0008 remains experimental,
opt-in, and unpromoted. Luna-37's prior-architecture verdict and Luna-38/39
mechanism verdicts are preserved.

Following the owner-directed audit from clean `main` at
`6ae253dd53b2b7a9ba1589c10035690a5b65e416`, Luna-40 is
**AUTHORIZED / NOT EXECUTED** as a mechanism-only characterization of
whether the existing ACP-0007 local growth mechanism creates effective
convergent routed drive under ACP-0008's unchanged defaults. It may not
change edge-weight semantics, production code, ACPs, thresholds, decay,
reward/eligibility, or topology bounds; no efficacy, pruning, classification,
or ACP-0008 promotion is authorized. See `.github/agents/luna-40.agent.md`
and `workflow/handoffs/luna-0-authorization-luna40-effective-routed-drive-20261005.md`.

# Luna-0 independent post-Luna-39 review — ACP-0008 propagation-to-emission diagnostic - 2026-10-05

**PASS WITH FOLLOW-UP; bounded mechanism supported only under the predeclared static N2 sensitivity.** Independent post-Luna-39 review verified `a185c6321b06f58df2bd7b22c56b1d23cb7d67e5`: the legacy arm exactly reproduces all Luna-37 records; destination-only ACP-0008 integration preserves upstream source/routing schedules; `w=1` yields zero canonical destination emissions, while `w=2` yields 31 trace-verified integration-mediated emissions on 27/320 characters. Independent aggregate, equation, capacity, and full replay audits pass; full rerun digest is unchanged. No direct emissions, production defect, or architecture change. ACP-0008 stays accepted as experimental/opt-in, not promoted. Luna-37 remains historically NOT SUPPORTED IN THIS SETUP; Luna-34 BLOCKED / UNDETERMINED; Luna-33 and ACP-0007 unchanged. No Luna-40 created or authorized; a possible natural/learned routed-strength follow-up is returned to the project owner for direction. Full evidence and validation: `workflow/handoffs/luna-0-independent-review-luna39-acp0008-propagation-emission-20261005.md`.

# Luna-0 independent post-Luna-38 review — ACP-0008 temporal integration - 2026-10-05

PASS WITH FOLLOW-UP: the Luna-38 implementation (`58ad086`) matches ACP-0008 equation by equation, keeps `theta_E` as the existing configurable `E1Config.theta_e` (default 1, no hidden constant, no `theta_I`), and is bounded, event-driven and deterministic on unit fixtures; direct and integration-mediated emissions are distinguishable from the retained trace. Full suite 990 passed, 1 skipped, 991 collected. ACP-0008 remains accepted as experimental and opt-in; `ARCHITECTURE_CONTRACT.md`, ACP-0007 and the Luna-33/34/37 verdicts are unchanged and no promotion is made. Luna-39 (Luna-37 fixture rerun with an integration-enabled destination at default `theta_E`, plus a legacy reproduction arm) is AUTHORIZED / NOT EXECUTED. Source: `workflow/handoffs/luna-0-independent-review-luna38-acp0008-temporal-integration-20261005.md`, `.github/agents/luna-39.agent.md`.

# ACP-0008 accepted (experimental, opt-in) - slow temporal-integration state; Luna-38 AUTHORIZED / NOT EXECUTED - 2026-10-05

Project-owner decision after the post-Luna-37 review: add an optional, default-disabled slow integration state `z` (`lambda_z=0.1`, `kappa=1`, `theta_Z=1`, `Z_max=4`) to the EXCURSION_V1 neuron so temporally separated sub-threshold inputs can compress into one canonical emission via subtractive discharge through the unchanged ordinary emission path. Rationale: Luna-37 showed sub-threshold magnitude (max 0.6855/0.9327 < `theta_E=1`) plus fast decay over gaps of at least 12.9 prevented accumulation. The E2 `M` oscillator regime is unchanged; a `z`-driven oscillator is staged to a later Luna. `ARCHITECTURE_CONTRACT.md`, ACP-0007 and the Luna-33/34/37 verdicts are unchanged; promotion awaits independent post-Luna-38 review. Unit-scale parameters are not calibrated and are not expected to rescue Luna-37 streams. Amendment: `theta_E` is recorded as an explicit configurable per-neuron parameter (existing `E1Config.theta_e`, default 1, fixed during execution, serialized by IR-2); temporal integration (how evidence accumulates) and activation threshold (how much is required) stay distinct, with predeclared Luna-38 fixtures J-L and no adaptive-threshold work. Sources: `workflow/docs/architecture_proposals/ACP-0008.md`, `workflow/handoffs/luna-0-owner-decision-acp0008-temporal-integration-20261005.md`, `.github/agents/luna-38.agent.md`.

# Luna-0 independent post-Luna-37 review — propagation-to-emission diagnostic - 2026-10-05

**NOT SUPPORTED IN THIS SETUP; CONTRACT PASS; NO LUNA-38 AUTHORIZED.** Luna-37 (`295309866c367cfeda7e42b4a42a47e813dd88ec`) validly ran the bounded mechanism diagnostic at `eligibility_capacity=1024`: valid routing, zero downstream canonical emissions in all three conditions (max destination state 0.6855 at w=1, 0.9327 at w=2, below `theta_E=1`; no accumulation). Bootstrap-gap classification strengthened. No production defect, no architecture change, ACP-0007 and Luna-33 unchanged, Luna-34 remains BLOCKED / UNDETERMINED. Full 952 passed, 1 skipped, 953 collected. Review: `workflow/handoffs/luna-0-independent-review-luna37-propagation-emission-diagnostic-20261004.md`.

# Luna-0 independent post-Luna-36 review — eligibility capacity API - 2026-10-04

**PASS — PUBLIC-API BLOCKER RESOLVED; LUNA-37 AUTHORIZED / NOT EXECUTED.** Luna-36 (`8f8824a185a2b1ebc3fd74cbd29eef8d75cbd818`) added an optional finite per-ledger `eligibility_capacity` to the EXCURSION runtime with the legacy default preserved, bounded overflow intact, and no lifecycle/predictor/reward change. Focused 90 passed; full 945 passed, 1 skipped, 946 collected. No production defect and no architecture change. Luna-37 is authorized (not executed) as a Luna-34 mechanism-only successor with predeclared `eligibility_capacity=1024`. Luna-34 stays BLOCKED / UNDETERMINED; Luna-33 and ACP-0007 unchanged. Review: `workflow/handoffs/luna-0-independent-review-luna36-eligibility-capacity-api-20261004.md`.

# Luna-0 independent post-Luna-35 review — eligibility lifecycle and capacity API - 2026-10-04

**PASS — LUNA-35 EVIDENCE INDEPENDENTLY RECONSTRUCTED; NO PRODUCTION
LIFECYCLE DEFECT ESTABLISHED; LUNA-36 AUTHORIZED / NOT EXECUTED.** Review
started from clean synchronized `main` at
`b0507cb68776011dba482907b0ac763bec2a225f`. Luna-35 used exactly its two
authorized no-edge fixtures and changed no production semantics. Focused
Luna-35, eligibility, excursion-integration and prediction tests: **77
passed**. Full suite: **932 passed, 1 skipped, 933 collected**; the one skip
is the CUDA visualization test because CUDA is unavailable. The increase
from the pre-Luna-35 930 collected is exactly the three Luna-35 tests.
Deterministic replay digests match. Exact commands, fixtures, and evidence:
`workflow/handoffs/luna-0-independent-review-luna35-eligibility-capacity-20261004.md`.

The reproducer reconciles `0 + 16 creations - 0 removals = 16` in the
source ledger. The seventeenth unique trace is rejected at the existing
finite per-ledger bound. Predictor expiry removes predictor records but does
not retire matching eligibility. Delayed-credit behavior accepts a later
reward by retained prediction identity after predictor expiry; deleting that
trace at predictor expiry would destroy this supported credit path. The
one-point control's neutral reward matched its explicit trace ID and decayed
the value without removing it (`1 -> 1`); character destruction released
that trace and the next character's ledgers were empty. Thus the live state
is bounded and character-scoped, not an unbounded cross-character leak.

Classification: **EXPECTED BOUNDED BEHAVIOR** for the overflow;
**CONTRACT AMBIGUITY / PUBLIC API LIMITATION** for the workload-to-capacity
relationship. Neither caller/fixture lifecycle misuse nor a production
lifecycle defect is established. Luna-34 remains historically **BLOCKED /
UNDETERMINED**; its mechanism question was not rerun. Luna-33 and ACP-0007
remain unchanged.

Luna-36 is authorized only to add a backward-compatible optional finite
per-ledger `eligibility_capacity` setting to the EXCURSION runtime, preserving
the exact existing derived default when omitted. It may not change
eligibility retirement, predictor expiry, reward behavior, or event ordering;
it is API compatibility work, not a Luna-34 mechanism rerun or efficacy
experiment. No architecture change or Luna-37 is authorized.

# Luna-0 independent post-Luna-34 review — eligibility capacity/lifecycle - 2026-10-04

**PASS — LUNA-34 BLOCKER INDEPENDENTLY REPRODUCED; LUNA-35 AUTHORIZED /
NOT EXECUTED.** From clean revision
`4d77489eaebadf638f22996d1d0d49e162b378ab`, the first fixed no-edge stream
failure reproduces at seed 0, sequence index 4 (`c00-004`): the seventeenth
source emission attempts a new unique eligibility trace while the source
ledger has 16/16 entries. The runtime derives 16 entries per ledger from
`prediction_capacity=8` times two neurons and allocates two per-node ledgers.
All 16 linked predictions had expired, but eligibility entries remained
resident; no errors or reward reached the ledger before failure. The
character did not reach its reset boundary.

The hard overflow is established bounded behavior, including an existing
test requiring deterministic rejection without eviction. The relationship
between predictor capacity and eligibility capacity, and retention after
predictor expiry, are not a documented execution-capacity contract. No
production defect is established; the exact contract-fixed workload cannot
complete through the required public runtime without changing inputs or
capacity. Luna-34 is correctly **BLOCKED**; all three conditions, the
multi-emitter bridge, and candidate formation remain **UNDETERMINED**. Its
initial artifacts remain honest; the independent exact failure coordinates
and lifecycle observations are recorded in
`workflow/handoffs/luna-0-independent-review-luna34-eligibility-capacity-20261004.md`.

Luna-35 is authorized solely for two-fixture eligibility lifecycle
characterization (the exact 20-point no-edge reproducer and a one-point
character-reset control). No topology-edge condition, propagation-to-emission
retry, efficacy endpoint, capacity/expiry tuning, production edit, ACP,
architecture promotion, or Luna-36 was authorized at that time. This
historical status is superseded by the post-Luna-35 review above. Architecture Contract
1.2, ACP-0007, the Luna-33 verdict, and the Luna-34 mechanism hypothesis are
unchanged. Independent regression: 71 focused tests passed; full suite
929 passed, 1 CUDA-unavailable skip; 930 collected, exactly nine more than
the pre-Luna-34 baseline due to Luna-34's nine added tests.

# Luna-0 candidate-formation bootstrap decision - Luna-34 mechanism authorization - 2026-10-04

**PASS - ACP-0007 CANDIDATE-FORMATION BOOTSTRAP CLASSIFIED;
LUNA-34 AUTHORIZED / NOT EXECUTED.** Independent audit of every C/D
training decision in the published five-seed Luna-33 results confirms zero
candidate opportunities, zero distinct multi-emitter characters, and no
candidate rejection or growth attempt. Each emitting character's sole
canonical emitter is its designated input neuron. Routed downstream
activity is present (route depth 1 and positive edge-transfer proxy), but
downstream canonical emission is absent. The bounded root cause is a
within-character multi-emitter / propagation-to-emission bootstrap gap.
Ring direction and association window are not causal because a second
emitter is absent.

One default signal-only Model-B transfer is bounded by `tanh(1) < theta_E`;
even accepted static `|w| <= 2` is bounded by `tanh(2) < theta_E`. Repeated
within-character temporal accumulation is the authorized mechanism question.
Existing public EXCURSION_V1 runtime, fixed topology, point input, and
emission-observation interfaces suffice. No architecture change or ACP is
required; Architecture Contract 1.2 and accepted ACP-0007 are unchanged.

Luna-34 may conduct only the predeclared two-node, fixed-edge,
label-free mechanism experiment, with no-edge, default `w=1,d=1,r=0`, and
static N2 bound-sensitivity `w=2,d=1,r=0` conditions. It is **NOT TASK
EFFICACY**, does not alter emission-based character-local ACP-0007 evidence,
and must return to Luna-0 before any follow-up. No accuracy retry, reception-
as-emission, cross-character history, architecture promotion, E2 pruning, or
N3 is authorized. See
`.github/agents/luna-34.agent.md` and
`workflow/handoffs/luna-0-post-luna33-candidate-formation-bootstrap-decision-20261004.md`.
Luna-33's scientific H1 remains **NOT SUPPORTED IN THIS SETUP**; historical
Luna-12L/Luna-13F remain **NOT SUPPORTED / UNCHANGED**.

# Luna-0 independent closure - Luna-33 ACP-0007 four-class EXCURSION_V1 efficacy - 2026-10-04

**PASS - LUNA-33 ACP-0007 FOUR-CLASS EXCURSION_V1 EFFICACY EXPERIMENT
INDEPENDENTLY VERIFIED / CLOSED** within the exact declared synthetic
four-class experiment scope. Independent review handoff:
`workflow/handoffs/luna-0-independent-review-luna-33-acp0007-four-class-efficacy-20261004.md`.
The committed experiment was independently reproduced byte-for-byte; all 20
seed/condition runs were valid, and A/B observation non-interference and
held-out non-mutation were independently verified.

The joint predeclared H1 is **NOT SUPPORTED IN THIS SETUP**: mean C-A and C-D
are both 0.0 (0/5 positive seeds). Structural observations were present, but
candidate opportunities were zero, all C/D decisions were `no_candidate`,
growth attempts and admissions were zero, and no admitted edge was later
used. The effect of successfully engaged growth and its temporal specificity
remain **NOT ESTABLISHED**. Prediction benefit, resource benefit, and
hardware equivalence remain **NOT ESTABLISHED**.

Historical Luna-12L remains **NOT SUPPORTED / UNCHANGED**; Luna-13F remains
**NOT SUPPORTED / UNCHANGED**. Architecture Contract 1.2 and accepted
ACP-0007 are **UNCHANGED**; no architecture or core/runtime change was made.
E2 pruning and ACP-0002 N3 remain **NOT AUTHORIZED**. Hardware equivalence
remains **NOT ESTABLISHED**. Luna-33 is closed only for this experiment
scope; Luna-34 and any successor remain **NOT AUTHORIZED**.

# Luna-0 corrective authorization — Luna-33 topology feasibility - 2026-10-04

**AUTHORIZED — CORRECTED LUNA-33 / NOT EXECUTED.** After the original
eight-edge Luna-33 profile stopped before efficacy execution, Luna-0 swept
public initialization for initial edge counts 0–8 and required seeds 0–4.
Two edges is the maximum count feasible for every seed, and each resulting
topology retains 7–8 statically legal absent directed ring candidates under
the unchanged edge-capacity and fan-in/out bounds. Evidence and the complete
matrix/topologies are recorded in
`workflow/handoffs/luna-0-luna33-topology-feasibility-correction-20261004.md`.
Only `topology_initial_edges` changes from 8 to 2 in the Luna-33 dispatch;
the seeds, node count, capacity, fan limits, observation fabric, growth bounds,
dataset, A–D design, D intervention, endpoint, and support rule are unchanged.
This is a pre-outcome experimental-profile correction within accepted
ACP-0007; Architecture Contract 1.2, A01–A15, ACP-0007 and acceptance
criteria remain unchanged; no ACP is required. The efficacy experiment was
not run. Historical Luna-12L remains **NOT SUPPORTED / UNCHANGED**,
Luna-13F useful-growth prediction remains **NOT SUPPORTED / UNCHANGED**,
E2 pruning and N3 remain **NOT AUTHORIZED**, and task efficacy, prediction
benefit, resource benefit, and hardware equivalence remain **NOT ESTABLISHED**.
Luna-33 must return to Luna-0 for independent review; no successor is
authorized.

# Luna-0 authorization — ACP-0007 four-class EXCURSION_V1 efficacy (Luna-33) - 2026-10-04

**AUTHORIZED / NOT EXECUTED.** Following Luna-32's independently verified
closure, Luna-0 verified the full baseline (908 passed, 0 failed, 1
CUDA-unavailable skip; 909 collected) and found the existing public
`ExperimentRunner` APIs sufficient for matched seeded topology, structural
decision evidence, held-out metrics, and exact later route-use accounting.
Luna-33 is authorized for a bounded four-class EXCURSION_V1 experiment only;
the frozen A–D design and falsifiable paired accuracy/engagement rules are
recorded in `.github/agents/luna-33.agent.md` and
`workflow/handoffs/luna-0-post-luna32-acp0007-four-class-efficacy-decision-20261004.md`.
No outcome-bearing preview or experiment was run. This is within accepted
ACP-0007: Architecture Contract 1.2, A01-A15, ACP-0007, and acceptance
criteria are unchanged; no ACP required. Historical Luna-12L remains
**NOT SUPPORTED / UNCHANGED**. Task efficacy, prediction benefit, resource
benefit, and hardware equivalence remain **NOT ESTABLISHED**. E2 pruning and
N3 remain **NOT AUTHORIZED**. Luna-33 must return to Luna-0 for independent
review; no successor is authorized.

# Luna-0 independent closure — Luna-32 historical Luna-12L / spiral model compatibility - 2026-10-04

**PASS — LUNA-32 HISTORICAL LUNA-12L / SPIRAL MODEL-EXPLICIT COMPATIBILITY INDEPENDENTLY VERIFIED / CLOSED** within the exact historical compatibility scope. Independent review handoff: `workflow/handoffs/luna-0-independent-review-luna-32-historical-temporal-spiral-model-compatibility-20261004.md`. Historical `TANH_LEGACY` is explicit for all five Luna-12L classifier policies (including `fixed`) and all ten spiral controls; no policy/model confound or ACP-0007 alias exists. The historical Luna-12L verdict remains **NOT SUPPORTED / UNCHANGED**, and the current explicit-TANH compatibility run is not the same experiment as the retained historical artifact. Artifacts and historical evidence remain unchanged. Current `EXCURSION_V1` default and ACP-0007 are unchanged; no new E2 four-class experiment was performed. E2 pruning and N3 remain **NOT AUTHORIZED**. Task efficacy, resource benefit, and hardware equivalence remain **NOT ESTABLISHED**. Luna-33 is **NOT AUTHORIZED**.

# Luna-0 decision — Luna-12L / spiral historical model compatibility (Luna-32) - 2026-10-04

**AUTHORIZED — LUNA-32 HISTORICAL MODEL-EXPLICIT COMPATIBILITY; NOT EXECUTED.** At 392ce25, the nine remaining failures (8 Luna-12L, 1 spiral) were reproduced and traced to the implicit model default moving to EXCURSION_V1; legacy policies baseline/random/temporal/reversed have no E2 equivalent. Luna-32 may make TANH_LEGACY explicit for all conditions (no cross-model mix) in temporal_scale.py, spiral_benchmark.py and their tests only. Explicit-TANH probes are not the same experiment as the retained corrected Luna-12L result (energy/replay digests differ), which stays NOT SUPPORTED and frozen. A current ACP-0007 four-class experiment requires a new contract. No architecture promotion; Contract 1.2 and ACP-0007 unchanged; E2 pruning and N3 unauthorized; successor not authorized.

# Luna-0 closure — Luna-31 Luna-12E EXCURSION_V1 observable compatibility - 2026-10-04

**PASS — LUNA-31 INDEPENDENTLY VERIFIED / CLOSED** (implementation 9efc5f1, test-only). Luna-12E E2 observable compatibility: CLOSED / VERIFIED. Causal routing: DIRECTLY VERIFIED. Prediction-loss delta: NOT REQUIRED FOR THIS FIXTURE. E2 terminal reset oracle: VERIFIED. TANH legacy timing: PRESERVED AS MODEL-SPECIFIC REGRESSION. Production code, Architecture Contract and ACP-0007: UNCHANGED. Task efficacy, resource benefit, hardware equivalence: NOT ESTABLISHED. Successor not authorized; E2 pruning and N3 remain unauthorized.

# Luna-0 authorization — Luna-12E EXCURSION_V1 observable compatibility correction (Luna-31) - 2026-10-04

**AUTHORIZED — LUNA-31 TEST-ONLY COMPATIBILITY CORRECTION; NOT EXECUTED.**
At clean synchronized `main`,
`HEAD == origin/main == 8d5f7f5ad1c594df3cd886de327eb14c3dfbe15c`,
Luna-0 reproduced and classified the two remaining Luna-12E failures as stale
observable expectations. The routed-edge fixture demonstrates a real causal
routing effect through route trace, event count, edge-transfer proxy, and route
depth even though prediction loss is equal. The reset fixture's public E2
state is neutral at the configured terminal horizon, with no pending event and
stable neuron identity. Evidence and the explicit assertion matrix are in
`workflow/handoffs/luna-0-post-luna30-luna12e-e2-observable-decision-20261004.md`.

Luna-31 owns only
`tests/test_luna12e_integration.py` and
`workflow/handoffs/luna-31-luna12e-e2-observable-compatibility-20261004.md`.
Production files, E2/prediction/routing/reset semantics, Luna-12L and spiral,
and the first three historical Luna-12E topology component tests are excluded.
The default E2 test must retain identity and assert horizon-derived terminal
time, neutral state/mode, and no pending work. The prediction-loss inequality
is removed as a required routing oracle; an explicit TANH_LEGACY clock
regression is optional and not an authorization gate.

Architecture change: **NO**. ACP required: **NO**. Architecture Contract 1.2,
A01-A15, and accepted ACP-0007 remain unchanged. Task efficacy, resource
benefit, and hardware equivalence are not established. Required sequence:
`Luna-0 -> Luna-31 -> Luna-0`.

# Luna-0 independent review — Luna-30 TPCV-2 replay consumer compatibility correction closed - 2026-10-04

**PASS — LUNA-30 TPCV-2 REPLAY CONSUMER COMPATIBILITY CORRECTION
INDEPENDENTLY VERIFIED / CLOSED** for its exact downstream replay-consumer
scope. The review began at clean synchronized `main`,
`HEAD == origin/main == 188dfd49fddc6702e86c56210f26455e6513050f`; full
independent evidence is recorded in
`workflow/handoffs/luna-0-independent-review-luna-30-tpcv2-replay-consumer-compatibility-20261004.md`.

TPCV-2 viewer compatibility: **INDEPENDENTLY VERIFIED**. TPCV-2 scalar
activation remains **ABSENT / None**, and TPCV-1 scalar activation is
**PRESERVED**. Temporal-analysis accepted/rejection accounting is
**RESTORED / VERIFIED**: `accepted` counts only `accepted_additions`.
TPCV schema: **UNCHANGED**. ACP-0007: **UNCHANGED / ACCEPTED**. E2 pruning
and ACP-0002 N3 remain **NOT AUTHORIZED**. Task efficacy, resource benefit,
and hardware equivalence are **NOT ESTABLISHED**.

Independent validation: focused consumers **19 passed**, combined
consumer/prerequisite suite **108 passed**, full suite **896 passed, 11
failed, 1 skipped**, and **908 collected**. The remaining failures are
outside scope: 2 Luna-12E, 8 Luna-12L, and 1 spiral; temporal-analysis and
3D-viewer failures: **0**. No production or test files were changed by this
review. No successor Luna is authorized.

# Luna-0 authorization — Luna-30 TPCV-2 replay consumer compatibility correction - 2026-10-04

**AUTHORIZED — LUNA-30 TPCV-2 REPLAY CONSUMER COMPATIBILITY CORRECTION;
NOT EXECUTED.** At clean synchronized `main`,
`HEAD == origin/main == 727a00aed08a4ba2c7194a70cde603f60ab35065`,
Luna-0 authorized the bounded downstream correction in
`.github/agents/luna-30.agent.md` and
`workflow/handoffs/luna-0-authorization-luna-30-tpcv2-replay-consumer-compatibility-20261004.md`.
The prior blocked review identified valid TPCV-2 `ExcursionNeuronRecord`
values reaching `VisualizationScene.nodes()` and `inspect()` and raising
`AttributeError` because scalar activation is not defined for EXCURSION_V1.

Authorized projection: retain TPCV-1's exact activation float; represent
TPCV-2 activation as absent (`None`) and continue to use canonical `active`
for activity filtering. Also authorized are version-neutral temporal-analysis
capability-limit wording and migration of only the assigned temporal-analysis
and viewer tests to deterministic detached TPCV-2 replay with explicit
metrics. Generic snapshot-difference removal highlighting is visualization
behavior, not E2 pruning evidence.

Architecture change: **NO**. ACP required: **NO**. TPCV schema change: **NO**.
Viewer compatibility correction: **AUTHORIZED**. Consumer fixture migration:
**AUTHORIZED**. E2 pruning and N3: **NOT AUTHORIZED**. Architecture Contract
1.2, A01-A15, and accepted ACP-0007 remain unchanged. Luna-30 is
**AUTHORIZED / NOT EXECUTED**; mandatory sequence is
`Luna-0 -> Luna-30 -> Luna-0`.

# Luna-0 independent review — Luna-29 closed - 2026-10-04

**PASS — LUNA-29 CPU-HELPER COMPATIBILITY INDEPENDENTLY VERIFIED AND CLOSED
FOR ITS AUTHORIZED SCOPE.** Review began at clean synchronized `main`,
`HEAD == origin/main == 6e1387967de2d1170d5743a38927afe08b9ddab8`.
Implementation `252fa15073e983a793a06b0ba3c79c84ced84637` was verified
against the authorization and completion handoffs. The explicit
`ExperimentConfig` pass-through, preserved scalar convenience route,
conflict rejection, deterministic bounded E2 growth fixture, downstream-only
capture, label isolation, TPCV-2 edge addition, E2 no-pruning behavior, and
TANH_LEGACY/generic replay controls passed. The helper is supported for
configuration pass-through only; its fixed synthetic workload is not
required by the Luna-29 contract to generate E2 growth.

Independent focused runs passed: Luna-12B 13, Luna-28 44, CPU/TPCV 32,
combined 89, and experiment regression 12. The full suite reported 880
passed, 17 failed, and 1 CUDA-unavailable skip (898 collected). The 17
failures comprise 2 previously documented Luna-12E legacy-observable
assertions and 15 downstream tests that still construct structural-plasticity
configurations without the ACP-0007 observation settings (8 Luna-12L, 1
spiral, 3 temporal-analysis, 3 3D viewer). Those consumers are outside the
Luna-29 delta and were not repaired; the full suite is not green.

The complete evidence and A01-A15 matrix are in
`workflow/handoffs/luna-0-independent-review-luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md`.
Architecture Contract 1.2, A01-A15, and accepted ACP-0007 are unchanged.
This closes only Luna-29's authorized compatibility scope; it establishes no
downstream readiness, efficacy/resource benefit, or hardware equivalence and
authorizes no successor.

# Luna-29 execution-lineage clarification - 2026-10-04

This governance correction distinguishes the verified decision revision
`c654ffe9c8d4a6d179781696d9ba5cd239e12795` from the authorization-package
publication and execution-lineage floor
`aad4b0db09773ebca9314d188c3b24297ad17c44`. The dispatch token
`F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` is not a Git object and is
ignored as repository provenance. This does not change architecture, ACP-0007,
or Luna-29's substantive scope, and does not enable pruning; it only clarifies
decision baseline versus publication/execution lineage.

# Luna-0 authorization — Luna-29 CPU structural replay compatibility - 2026-10-04

**AUTHORIZED — LUNA-29 DOWNSTREAM CPU-HELPER COMPATIBILITY + FOCUSED
VERIFICATION ONLY; NOT STARTED.** At clean `main`,
`HEAD == origin/main == c654ffe9c8d4a6d179781696d9ba5cd239e12795`
(`docs: close independent Luna-28 review`), Luna-0 classified the four
Luna-12B failures as pre-ACP-0007 callers rejected by the intentional E2
missing-observation guard. Luna-29 may expose an explicit existing
`ExperimentConfig` through the CPU helper and migrate only the Luna-12B
integration and CPU capture tests to accepted growth-only E2 semantics.

No ACP is required: this adapts a downstream wrapper to accepted ACP-0007.
The boolean-only E2 request must remain invalid; no implicit neighborhoods
or profile are allowed. E2 pruning, N3, TPCV codec changes, the CPU CLI and
other downstream migrations remain unauthorized. TPCV-2 already captures
actual bounded topology edges and its adjacent-snapshot timeline can represent
additions. The exact scope and acceptance gate are in
`.github/agents/luna-29.agent.md` and
`workflow/handoffs/luna-0-authorization-luna-29-acp0007-cpu-structural-replay-compatibility-20261004.md`.
This dispatch changes neither ACP-0007 nor A01-A15 and makes no efficacy,
resource-benefit, downstream-readiness or hardware claim.

# Luna-0 independent review — Luna-28 closed - 2026-10-04

**PASS — LUNA-28 IMPLEMENTATION INDEPENDENTLY VERIFIED / CLOSED FOR ITS
AUTHORIZED MECHANISM SCOPE.** Review began at clean `main`,
`HEAD == origin/main == 028b5793917efb2c1af279691d1611427de3a86c`.
The implementation is `ac321abba6f4772f18fa459d4442e8f4ef4867e4`; its
parent-to-implementation delta is exactly the four authorized implementation
and test files. The handoff and revision pin are separate commits
`512b7cab73446ba036cb5e9189afe49e4b9c2393` and
`028b5793917efb2c1af279691d1611427de3a86c`. A separate identifier supplied
in the review brief did not resolve as a Git commit and was not used.

The independent audit confirmed bounded emission-only local observations,
character-local evidence freeze/discard, quiescent post-character mutation,
finite aggregate candidate and topology capacity, deterministic admission,
preserved fixed-topology defaults and TANH_LEGACY compatibility, and a real
later E2 route at `4.4 = 4.0 + 0.4`. Focused Luna-28 tests passed (44), closed
component regressions passed (168), compilation and Pylance checks passed.
The independent full suite reported 865 passed, 21 failures and 1 existing
CUDA-unavailable skip (887 collected). All 21 match the documented downstream
opt-in-guard failures (19) and stale Luna-12E assertions (2); no Luna-28
regression was found. Full details and the A01-A15 review matrix are in
`workflow/handoffs/luna-0-independent-review-luna-28-excursion-local-temporal-growth-20261004.md`.

This is a governance-only closure of the accepted ACP-0007 implementation
review. Contract version 1.2 and A01-A15 are unchanged. Mechanism validity is
established for the tested path; task efficacy, resource benefit, downstream
integration readiness, pruning, N3 learning, A14 promotion, and hardware
equivalence are not established or authorized. No downstream migration or
successor assignment follows from this review.

# Luna-0 acceptance — ACP-0007 and Luna-28 authorization - 2026-10-04

**ACCEPTED — BOUNDED EXCURSION_V1 STRUCTURAL GROWTH EXPERIMENT; LUNA-28
AUTHORIZED, NOT EXECUTED.** The project owner accepted ACP-0007 with the
complete local structural-observation contract. Architecture contract version
is 1.2. No A01-A15 clause text or scope is changed; ACP-0006 §17 is clarified
only for this separately authorized, opt-in, growth-only experiment. Fixed
topology remains the EXCURSION_V1 default.

The accepted E2 evidence source is only an actual canonical emission's
identity and timestamp, observed over an explicit bounded static local
neighborhood independent of mutable neural connectivity. Temporal-association
scores use only strictly ordered, bounded local emission counts. Evidence is
character-local, frozen after successful settling, consumed after at most one
post-character admission attempt, and cannot mutate topology while runtime
work is active. The configured finite positive delay is fixed, the growth
attempt budget is finite, and the same bounded topology serves later E2
routing. Pruning is not authorized.

Luna-28 is authorized for implementation and verification only under
`.github/agents/luna-28.agent.md` and
`workflow/handoffs/luna-0-authorization-luna-28-excursion-local-temporal-growth-20261004.md`.
The owner decision and terms are recorded in
`workflow/handoffs/luna-0-owner-decision-acp0007-excursion-structural-growth-20261004.md`.
At acceptance-publication time, no Luna-28 implementation or tests had been
run. The previous readiness result remains historically valid: 19 downstream
failures stopped at the guard, 12 passed, and the 69 structural/evidence
regressions passed. Those
results do not establish post-guard downstream behavior. The separately
classified Luna-12E failures still distinguish real routed-topology effects
from unchanged legacy aggregate `prediction_loss` and post-evaluation clock
expectations.

No Luna-13F useful-growth claim, A14 promotion, N3 edge-parameter learning,
pruning, downstream migration, hardware work, or hardware-equivalence claim
follows from this authorization. The fixed-topology ACP-0006 §17 path remains
the rollback/default; acceptance of mechanism tests will not imply task or
resource efficacy.

# Luna-0 EXCURSION_V1 structural re-entry readiness - 2026-10-04

**BLOCKED — EXCURSION_V1 STRUCTURAL RE-ENTRY REQUIRES ARCHITECTURE
DECISION.** At clean `main`, baseline
`d9abe5e3a5b9b3c6d6049ac4c64647463c33ba2d`, Luna-0 reran the five known
structurally dependent test groups: `19 failed, 12 passed`; all 19 failed at
the intentional `EXCURSION_V1 + structural_plasticity` configuration guard.
The focused structural controller/evidence regression slice passed
(`69 passed`). These results locate the immediate dependency root but do not
prove post-guard downstream assertions pass.

The historical `_adapt_topology()` score `abs(run.feature) + run.loss`,
index/policy-based endpoints, and feature-based pruning are not accepted
source-local E2 evidence. Luna-13F's bounded temporal-association mechanism
remains supported only in its tested experimental fixture; useful-growth
prediction was **NOT SUPPORTED**, resource benefit **NOT ESTABLISHED**, and
production reuse is not authorized. E2-local observation mapping, evidence
score/delay provenance, chronology/freeze/reset, incomplete-settling behavior,
and local pruning evidence remain unresolved.

Draft `workflow/docs/architecture_proposals/ACP-0007.md` is submitted for
project-owner architecture review. It is not accepted and changes neither
A01-A15 nor ACP-0006. Growth and pruning are not authorized; the E2 guard
remains; Luna-28 is not created or executed. The complete readiness matrix,
test details, downstream dispositions and next decision are in
`workflow/handoffs/luna-0-excursion-structural-reentry-readiness-20261004.md`.
Initial governance publication: `5679cb9189418cadfd4e4c8df790896509f3ee54`.

# Luna-0 classification — Luna-12E downstream failures - 2026-10-04

**CLASSIFIED — TWO LEGACY-OBSERVABLE ASSERTIONS; NO LUNA-28
AUTHORIZED.** Luna-0 reproduced only the two known failing tests in
`tests/test_luna12e_integration.py`. The edge-intervention test still shows
causal topology routing: the reachable `neuron-0 -> neuron-1` edge adds
delayed `EXCURSION` and routed prediction-error deliveries, increases
processed events from 12 to 14, and raises edge-transfer proxy from 0 to
`1.358357398350786`. Its only failing assertion requires aggregate
`prediction_loss` to change; measured loss is exactly
`1.1724999999999999` in both conditions. A downstream one-way edge can
causally change routed activity without changing the source-local prediction
loss.

The exact-clock test's stable-neuron-identity assertion passes. Its expected
final clocks `0.0` and `1.0` conflict with the current E2 lifecycle: points
at 0 and 1 settle through timestamp 5 (last input plus the 4-second
settling horizon), after which character destruction resets neurons at that
horizon. Character startup resets them at the next character's start
timestamp. The test observes post-evaluation clocks, not neutral state at the
next character boundary. This is classified as a legacy-clock oracle, not
evidence of a reset defect.

Both assertions predate the default-model switch: the tests were written for
the `TPCNNeuron` path and were unchanged when Luna-22 made `EXCURSION_V1`
the default. The two failures remain part of the 21 known downstream failures
until a separate compatibility decision. No production/test edit, A01-A15
change, ACP, remediation assignment, or Luna-28 creation/execution is made.
Details and exact focused-run evidence:
`workflow/handoffs/luna-0-classification-luna-12e-failures-20261004.md`.

# Luna-0 independent review — Luna-27 closed - 2026-10-04

**PASS — LUNA-27 TPCV-2 EXCURSION_V1 SNAPSHOT VISUALIZATION
INDEPENDENTLY VERIFIED / CLOSED.** This closure applies only to bounded CPU
TPCV-2 instantaneous `EXCURSION_V1` snapshot capture, versioned
encoding/decoding, and offline replay. It is an observability result, not
architecture promotion. No ACP is required and A01-A15 are unchanged.

The review began at clean `main` with
`HEAD == origin/main == 50230a30e9d1372891d9665f9b4a0d09ccd5d817`,
subject `docs: record Luna-27 TPCV-2 verification`. Published lineage:

- Authorization baseline: `10b9bfa09c949576099a220c2f507d939c01c337`.
- Implementation: `3bb8edc9346f7c2ec80112058d6e97b64f75bd11`,
  `feat: add TPCV-2 excursion snapshot support`.
- Completion handoff: `50230a30e9d1372891d9665f9b4a0d09ccd5d817`,
  `docs: record Luna-27 TPCV-2 verification`.

The baseline-to-completion diff contains exactly the six authorized Luna-27
files: `tpcn/visualization.py`, `tpcn/cpu_visualization.py`,
`tests/test_visualization.py`, `tests/test_cpu_visualization.py`,
`workflow/docs/luna/VISUALIZATION_CONTRACT.md`, and
`workflow/handoffs/luna-27-tpcv2-excursion-snapshot-visualization-20261003.md`.
No production code or tests were changed during this governance review.

**TPCV-1 preserved:** the independent review confirmed version 1's historical
record bytes and scalar semantics were not changed. The pre-change golden
fixture remains 120 bytes with SHA-256
`0ad558e8e229f1a4598513987b44715a051f43f399540c82e2515137af9b6eb8`.
Version 1 retains its historical scalar state, scalar activation, `active`
meaning, and processed-event representation; it is not reinterpreted as
`EXCURSION_V1`.

**TPCV-2 closed / CPU instantaneous observation only:** version 2 identifies
an instantaneous `EXCURSION_V1` observation, with `state=x`,
`active=(mode != N)`, explicit mode (`N`, `S_PENDING`, `S_RETURN`,
`M_ACTIVE`), `pending_internal_work=(pending_internal_event is not None)`,
and `processed_events=processed_event_count`. TPCV-2 has no scalar
activation; where a shared decoded representation requires the historical
field, `activation=None` means unavailable, never numeric zero. It is not a
runtime checkpoint, IR-2, IR-3, event log, emission-history format, or
interval-activity format.

The review independently verified version dispatch, mode/active consistency,
pending-work and processed-event mappings, strict malformed and bounded
validation, mixed-version rejection, homogeneous-version offline replay,
downstream-only capture, and capture-frequency computation invariance. The
focused independent command was:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m pytest -q tests/test_visualization.py tests/test_cpu_visualization.py tests/test_gpu_visualization.py
```

**Independent focused result: 33 passed, 1 skipped.** The independent reviewer
did not rerun the full repository suite. The implementation-run full-suite
evidence is **821 passed, 21 failed, 1 skipped (843 collected)** and is
recorded as **NOT INDEPENDENTLY RERUN BY LUNA-0**.

The same 21 downstream failures remain separately unresolved and outside
Luna-27 scope: Luna-12B structural integration (4), Luna-12E legacy
observables (2), Luna-12L temporal scale (8), spiral benchmark (1), temporal
analysis (3), and 3D viewer (3). They are not attributed to TPCV-2 and were
not repaired.

Architecture audit, limited to the reviewed representation:

- **A01 — PASS:** capture cadence remains epoch-boundary observation, not
  neural time.
- **A04 — PASS:** records, IDs, parser input, and replay resources remain
  bounded.
- **A07 — PASS:** no labels or future information enter snapshot state.
- **A08 — PASS:** encoding, parsing, and replay are deterministic and bounded.
- **A15 — PASS:** TPCV-2 is a backend-neutral downstream representation;
  no hardware realization or equivalence is claimed.

Not established: GPU `EXCURSION_V1`, ModelSim/FPGA TPCV-2, GPU/FPGA or
hardware equivalence, 3D viewer/temporal-analysis/structural-plasticity
compatibility, predictive efficacy, useful delayed-credit learning, or
physical energy calibration.

The full review evidence is
`workflow/handoffs/luna-0-independent-review-luna-27-tpcv2-excursion-visualization-20261004.md`.
**Successor status: NOT AUTHORIZED.** No Luna-28 contract or downstream
migration is authorized by this closure.

# Luna-0 post-Luna-22 TPCV / EXCURSION_V1 compatibility review - 2026-10-03

**DECISION C — VERSIONED EXCURSION VISUALIZATION FORMAT REQUIRED;
LUNA-27 AUTHORIZED.**
Review began on clean branch `main`, with `HEAD == origin/main ==
622a62c78df2af696920c4c5d1d85c10ecc15baf`, subject `docs: pin independent
closure revision`. Luna-22 and Luna-26 remain closed only within the bounded
fixed-topology `EXCURSION_V1` CPU integration and corrective routing scopes
recorded above; no broader efficacy or downstream-migration claim is made.

The three CPU visualization failures were reproduced independently. All fail
in `NeuronRecord.from_neuron()` because the current `MultiExcursionNeuron`
does not expose `activation`; the adapter otherwise reads its valid `state`
alias (`x`) and expects the differently named `processed_events` counter.
TPCV-1 and its existing CPU/GPU/replay consumers do not identify the dynamics
model. The existing Luna-12C governance requires snapshot-level activity and
forbids synthesized event pulses or timing, but it does not define an honest
excursion meaning for TPCV-1 `activation` or `active`.

No mapping into TPCV-1 is accepted: the scalar and activity meanings cannot be
inferred from `x`, mode, pending work, or an old emission without changing or
inventing field semantics. Under the requested pragmatic fallback, TPCV-2 is
selected for instantaneous EXCURSION_V1 snapshots: `state=x`, `active=(mode !=
N)` meaning a currently admitted non-neutral mode, explicit bounded mode and
pending-work flags, and no scalar activation, last emission, or interval
history. TPCV-1 remains byte- and meaning-compatible. The full matrix and
contract are in
`workflow/handoffs/luna-0-post-acp0006-tpcv-excursion-compatibility-decision-20261003.md`.

No ACP or A01-A15 change is proposed. Luna-27 is authorized but not executed;
its exact contract is `.github/agents/luna-27.agent.md`, and the authorization
is published in
`workflow/handoffs/luna-0-authorization-luna-27-tpcv2-excursion-snapshot-20261003.md`.
The other 21 classified full-suite downstream failures remain outside this
authorization.

# Luna-0 independent corrective review — Luna-26 closed; Luna-22 closed - 2026-10-03

**PASS — LUNA-26 ACP-0006 MULTI-HOP PREDICTION-ERROR ROUTING
INDEPENDENTLY VERIFIED / CLOSED. PASS — LUNA-22 ACP-0006 FIRST CPU
SOFTWARE-REFERENCE INTEGRATION INDEPENDENTLY VERIFIED / CLOSED**, limited to
the accepted fixed-topology `EXCURSION_V1` integration semantics. Review of
the corrective implementation began at `8a14681fe6a770e75136227c5059bc9c76ae5d46`
on clean `main == origin/main`.

The corrective API adds optional per-call destination exclusions to
`BoundedTopology.route()`; existing callers with the default empty exclusion
retain the old behavior. The integrated error adapter supplies its current
`RouteContext.route_path`, filtering only back-edges to a node already on
that path before queue preflight and admission. The independent runtime test
produced only `n0 -> n0 @ 1.00`, `n0 -> n1 @ 1.25`, and legal sibling
`n1 -> n2 @ 1.85`; the prohibited `n1 -> n0` return is not enqueued, receives
no sequence or sidecar, incurs no processed-event or edge cost, and has no
repeated path. An equal-time diamond still preserves distinct sibling paths,
applies local error once at convergence, and forwards downstream once.
Atomic capacity handling, opaque metadata/identity, local ledger ownership,
neuron isolation, causal input, character reset, and delayed-credit
idempotency remain verified. The earlier actual emission-to-prediction-to-
nonzero-error chain and unequal-delay two-hop route remain valid.

Independent validation on the corrective publication: topology plus focused
integration **60 passed**; prescribed ACP-0006 regression plus focused
integration **342 passed**; full CPU suite **24 failed, 804 passed, 1
CUDA-unavailable skip**; collection **829**; compileall, diagnostics and
diff checks passed. All 24 failures remain the known downstream
visualization, structural, legacy-observable, temporal-scale, benchmark,
analysis and viewer groups; their ownership/cause is unchanged and they are
not Luna-22 core correctness failures under this bounded contract.

**GOVERNANCE:** Luna-26 is **CLOSED / INDEPENDENTLY VERIFIED** for the
authorized adapter/topology route-path correction. Luna-22 is **CLOSED /
INDEPENDENTLY VERIFIED** only for the accepted first fixed-topology
`EXCURSION_V1` CPU software-reference integration; the previously identified
error-routing blocker is resolved and the prior Luna-0 closure-readiness
review had found no other owned core correctness blocker. This closure does
not demonstrate predictive efficacy, useful delayed-credit learning,
downstream migration, structural plasticity integration, reconstruction of
the historical Luna-22 split, writer-disjointness, hardware equivalence,
physical-energy calibration or repository-wide architecture completion.
Luna-23, Luna-24 and Luna-25 remain closed within their exact prior scopes.
ACP-0006 and A01-A15 are unchanged. The full evidence and exclusions are in
`workflow/handoffs/luna-0-independent-review-luna-26-prediction-error-routing-20261003.md`.
The next governance action, if any, is selection of one bounded downstream
compatibility semantic unit; no consumer migration is automatically
authorized.

# Luna-0 independent review of Luna-26 route-path behavior - 2026-10-03

**BLOCKED — LUNA-26 VIOLATES ACP-0006 RULE 3 ROUTE-PATH NO-REVISIT.
LUNA-22 REMAINS IMPLEMENTED / BLOCKED / NOT CLOSED.** Review began on clean
`main == origin/main == c7fc9b7477e8419af2282969b936db3a242e751b`,
`docs: record Luna-26 implementation revision`. The supplied expected token
`F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` is not a resolvable Git
object; the valid actual publication SHA is recorded here and in the review
handoff.

The implementation lineage is authorized baseline
`e5d31236432ca5301ca5ca4ba8eb699006a55b09`, implementation
`9f2e5d98e9abfd3702eb55a4af76c41009872abc`, then completion-handoff
publication `c7fc9b7477e8419af2282969b936db3a242e751b`. The independent
review reproduced the original source-forwarding defect on the exact
authorization baseline using a real E2 emission, prediction, later admitted
input and nonzero error. The Luna-26 fix now reaches `n0 -> n1 -> n2` at
`1.00`, `1.25`, and `1.65` with unequal edge delays, opaque metadata intact.

Adversarial cycle execution found the distinct current defect: on
`n0 -> n1 -> n0`, the actual return event is enqueued and processed at `1.65`
with route path `("n0", "n1", "n0")`. The delivery guard terminates forwarding
only after this prohibited revisit. ACP-0006 rule 3 explicitly forbids node
repetition within one routed-event path, so this is an implementation
violation, not a contract ambiguity. Numeric route depth `2` is within the
two-node cap, but does not cure the repeated-node path.

Validation on the reviewed publication: focused integration **49 passed**;
prescribed ACP-0006 regression plus focus **340 passed**; full CPU suite
**24 failed, 802 passed, 1 skipped**; collection **827**; compileall,
diagnostics and diff checks passed. The full-suite failures match the
previously classified downstream compatibility groups. The diamond,
metadata, no-neuron, causal-input, delayed-credit, queue-capacity, sidecar,
reset and accounting controls remain supported; none waives rule 3.

**GOVERNANCE:** Luna-26 is **BLOCKED — ROUTE-PATH NO-REVISIT INVARIANT**.
Luna-22 remains **IMPLEMENTED / BLOCKED / NOT CLOSED**. Luna-0 authorizes a
same-identifier Luna-26 corrective pass. Because the existing topology API
cannot filter a path-revisiting edge while preserving other legal outgoing
edges and atomic queue preflight, the correction may add one optional,
default-preserving destination-exclusion argument to `BoundedTopology.route()`.
The adapter must pass only the current event's route path; no global visited
set is permitted, and the convergent destination guard remains required.
The exact authorization is
`workflow/handoffs/luna-0-authorization-luna-26-corrective-route-path-20261003.md`.
No ACP or A01-A15 amendment is made. Independent review evidence is in
`workflow/handoffs/luna-0-independent-review-luna-26-prediction-error-routing-20261003.md`.
Downstream compatibility failures remain separate. Luna-25's zero prediction
matches/errors/credit remain efficacy observations; predictive efficacy and
useful delayed-credit learning are not established. Luna-0 must review the
corrective handoff before reconsidering Luna-22 closure.

# Luna-0 ACP-0006 / Luna-22 closure-readiness review - 2026-10-03

**SCENARIO C — LUNA-22 REMAINS BLOCKED BY ONE VERIFIED MULTI-HOP
PREDICTION-ERROR FORWARDING DEFECT.** Review began on clean
`main == origin/main == 42026a9fc3ccc1b1fdc83e0344c79312f2d76b14`.
The review and Luna-26 authorization were published at
`ffbf5ed3241ea6291955a6e1bba98bd6be27b54a`.
The request's token `F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` is not a
resolvable Git object. The actual implementation/review/correction lineage
was verified from the repository's commit graph and is documented in the
closure-readiness handoff.

Focused Luna-22 integration passed **43 tests** and the prescribed ACP-0006
regression passed **334 tests**. Real local prediction matching produced a
nonzero error from a later admitted target; real positive-delay reward
modified the corresponding emitted-excursion eligibility trace, and replaying
the reward ID was a no-op. Neither observation establishes dataset efficacy.
An independent three-node path probe reproduced a matched error at `n0`, its
finite-delay arrival at `n1`, then a repeated route from `n0` to `n1` instead
of the reachable `n2`. The runtime adapter passes the original event source
to `BoundedTopology.route()` at each hop. This violates already accepted
ACP-0006 rule 6; no ACP or A01-A15 change is required.

Luna-25's reproducibility gate remains closed for `luna25-v1`; the historical
Luna-22 sample is not reconstructable. Its zero matches/errors/credit and
classification result are task-efficacy/configuration observations, not
additional correctness gates. The rerun full suite reported **24 failed,
796 passed, 1 skipped, 821 collected**. Every failure is individually
classified as downstream consumer compatibility under fixed EXCURSION_V1
topology/model boundaries; none is a Luna-22 core blocker by itself. No
consumer fix was made or authorized here.

**GOVERNANCE:** Luna-22 is **IMPLEMENTED / BLOCKED / NOT CLOSED** solely for
the multi-hop error-forwarding defect among reviewed core items. Luna-23,
Luna-24 and Luna-25 remain closed in their exact scopes. Luna-26 is
**AUTHORIZED / NOT EXECUTED** to correct and verify adapter-only hop-local
forwarding, with actual matched-error path, identity/payload/delay,
reachability, convergence/deduplication and bounds coverage. It may not
change topology APIs, neuron/predictor/ledger behavior, ACP-0006, architecture
or downstream consumers. Full evidence and the exact bounded assignment are
in `workflow/handoffs/luna-0-acp-0006-luna-22-closure-readiness-20261003.md`,
`.github/agents/luna-26.agent.md` and
`workflow/handoffs/luna-0-authorization-luna-26-prediction-error-multihop-routing-20261003.md`.
Luna-0 must independently review Luna-26 before reconsidering Luna-22
closure. This fresh classification supersedes the earlier Luna-25 changelog
wording that grouped dataset efficacy and downstream compatibility among
Luna-22 blockers. ACP-0006 and A01-A15 are unchanged.

# Luna-0 independent review of Luna-25 dataset evidence - 2026-10-03

**PASS — LUNA-25 `luna25-v1` DATASET/SPLIT/RESULT REPRODUCIBILITY EVIDENCE
INDEPENDENTLY VERIFIED / CLOSED.** Review began at published revision
`425180bfb2b02691cf64f392f071795cc812cd72`, clean `main == origin/main`.
The verified lineage is authorization/publication
`7e174de664bc116db77aad89c8bed08ca750bcd3`, implementation/evidence
`5cb17d9bb79c848c27805cb79484d9ab3cd0f5b8`, and separate Luna-25 handoff
publication `425180bfb2b02691cf64f392f071795cc812cd72`.

An independent UCI retrieval reproduced the archive/source SHA-256 values,
2,858-record/20-class MATLAB schema and exact published `luna25-v1` split
membership/ranks. Two fresh benchmark runs matched the published stable
output digest `236835bf31c001ff520ef9389674e969435c63fb7038fd6f0797292cdefa69cc`
and training replay digest
`441184878990df3a61fba67b72ea996b917650e19166cd2d0360e1c909ca39b6`.
Independent confusion, per-class and macro metric recomputation matched the
reports. Instrumented prediction creations matched reported emissions and
expiry for train post-training evaluation, validation and test (138, 67 and
63 respectively); all matched counts and prediction errors were zero. Source
point, event, settling, queue/topology and energy-proxy arithmetic reconciled.
Counterfactual-label and differing-future-suffix probes found no pre-readout
label or unadmitted-future effect. Labels do select post-readout
reward/utility accounting; validation/test use `update=False` and do not
update prototypes.

The original Luna-22 subset remains unreconstructable; aggregate accuracy
equality does not establish the old membership or preprocessing. The retrieved
MAT metadata contains no writer/subject identity, so writer-disjointness is
not claimed. Luna-25 closes reproducibility for the new baseline only; zero
matched predictions/errors and zero matched credit do not establish
predictive efficacy or useful delayed-credit learning.

Validation: Luna-25 focused **7 passed**; prescribed ACP-0006 regression
**334 passed**; full CPU suite **24 failed, 796 passed, 1 skipped**;
collection **821**. All 24 failures remain in the previously classified
downstream visualization, structural/default-model, legacy-observable,
temporal-analysis and viewer groups; no Luna-25 test failed. No consumer
migration was performed. The consumer-specific decision matrix and detailed
evidence are in
`workflow/handoffs/luna-0-independent-review-luna-25-dataset-evidence-20261003.md`.

**GOVERNANCE:** Luna-25 is **CLOSED / INDEPENDENTLY VERIFIED** for
`luna25-v1` evidence. Luna-22 remains **BLOCKED / NOT CLOSED**: historical
split reconstruction is not possible, downstream compatibility remains
unresolved, and predictive/error/delayed-credit integration efficacy is not
demonstrated. Luna-23 and Luna-24 remain closed. No A01-A15, ACP-0006 or
hardware contract changed. No successor consumer implementation is assigned
until the project owner/Luna-0 chooses a specific compatibility contract.

# Luna-0 independent review of Luna-24 - 2026-10-03

**PASS — LUNA-24 ACP-0006 IR-2 QUIESCENT PROVENANCE BOUNDARY
INDEPENDENTLY VERIFIED / CLOSED.** Review began at the exact published
Luna-24 handoff tip `e59e8933bfa98cd607ca424250a051499b519b5a` on clean
`main == origin/main`. The verified lineage is baseline
`6c012f9feeff6481a44bd6d40414b4749b21db17`, implementation
`8e184e1bdceeb2873b2ea7479da953760b58ffbf`, then handoff publication
`e59e8933bfa98cd607ca424250a051499b519b5a`. Luna-23 closure commit
`c0e3e6905e329e5c268d6c63cbb3bd8d89345136` remains in the ancestry.

The implementation delta contains only `tpcn/experiment_excursion_runtime.py`
and `tests/test_excursion_integration.py`. The startup boundary now rejects
assigned provenance entries and sticky provenance truncation, alongside the
pre-existing exact residual-x and unassigned-provenance checks, before
reconstruction. Independent inspection of the exact parent showed both
assigned-provenance cases passed the old guard and were copied by the
unchanged standalone E2 converter. Valid revision-1 provenance remains
representable and reconstructable through standalone E2 adapters; this is
not a global schema rule.

Validation: focused integration **43 passed**; standalone IR-2/E2 references
**203 passed**; Luna-22 focused controls **55 passed**; prescribed regression
set **334 passed**; full CPU suite **789 passed, 24 failed, 1 skipped**;
collection **814**. The one skip is CUDA unavailable. The 24 failures match
the already classified visualization, structural/default-model,
legacy-observable, benchmark, temporal-analysis and viewer groups. No
Luna-24-attributable failure was found. `compileall`, Pylance diagnostics and
diff checks passed.

The field audit found no over-rejection or hidden startup ambiguity.
High-water identity counters survive character start; local event counters,
generation, `m_peak` and local timestamp are reset at the explicit
`START_CHARACTER` boundary before integrated event processing. Mode-N active
episode/pending combinations are schema-owned invalidity. Empty `TPCNIR2(())`
is schema-permitted but cannot create an integrated runtime: bounded-topology
construction rejects the empty node set. No adapter/schema duplication is
needed.

No A01-A15, ACP or schema revision changed. Luna-24 is **CLOSED /
INDEPENDENTLY VERIFIED** and Luna-23 remains closed. Luna-22 remains
**BLOCKED / NOT CLOSED**: the retained loader/split/per-class dataset evidence
is still absent, and downstream compatibility decisions remain separately
unresolved. No dataset benchmark or downstream migration was performed in
this review. Full evidence is in
`workflow/handoffs/luna-0-independent-review-luna-24-ir2-provenance-20261003.md`.

# Luna-0 authorization of Luna-25 dataset evidence - 2026-10-03

Following Luna-24's independent closure, Luna-0 authorized Luna-25 from
`1642b991f82403140d0f29b5a2ff10b3d2628cda` for the separate, bounded
ACP-0006 UCI Character Trajectories evidence gate. Luna-25 owns a standalone
deterministic loader/split/report, focused tests and a completion handoff;
it may not alter reusable core/runtime semantics or downstream consumers.
It must distinguish an exact reconstruction of the previously reported split
from a newly versioned deterministic split, and it may not claim the latter
reproduces the former. Dataset execution and evidence are **NOT RUN** at this
authorization. The dataset gate remains open until Luna-0 independently
reviews the resulting evidence.

No downstream migration is included. The remaining visualization,
structural/default-model, legacy-observable, spiral, temporal-analysis and
viewer failures have different intended contracts and require later
consumer-specific governance rather than a broad test-green task.

# Luna-0 independent review of Luna-23 - 2026-10-03

**PASS — LUNA-23 E2 LOGICAL-TIME REPRESENTABILITY CORRECTION INDEPENDENTLY
VERIFIED / CLOSED.** Review started at `10687cf4a21d75eb5a0552635282f889df1e4005`
with `main == origin/main` and a clean worktree. The implementation commit
`4c1efd6c31aed86748dcacf596401579c2b94bc8` has parent
`3ec3c4a7991c28f59e1419c9f3656267efed2875`; the first handoff publication
`7ce73cb194128f6ecd4a5068f4bbdd72d42b5eea` and finalized handoff
`10687cf4a21d75eb5a0552635282f889df1e4005` are descendants. The exact
implementation delta contains only `tpcn/excursion_neuron.py` and
`tests/test_e2_multi_excursion.py`.

Independent execution reproduced the negative and positive states at logical
time `45.27906122689938`; each analytic rearm delay was finite and positive
(`1.110223024625156e-15`), while adding it rounded to the current float. E2
stored `45.27906122689939`, the next representable future timestamp. Actual
pending-event processing yielded the strictly increasing trace
`[45.27906122689938, 45.27906122689939]`, then returned to `N` in two
processed events without emissions or a pending event. At the largest finite
timestamp, the next-float overflow was rejected before queue insertion.
Configured `M_EMIT`/`M_REARM` non-advancing delays, NaN and past times remain
rejected. The configured-delay regression passed.

Validation: focused E2 **42 passed**; E1/E2/IR-2 references **203 passed**;
the Luna-22 prescribed regression set **320 passed**; full CPU suite **24
failed, 775 passed, 1 skipped** (CUDA unavailable); current collection **800
tests**. The three former representability failures that now pass are the
four-class label-invariance test, fixed-policy classifier test, and requested
scale test. The other four former E2 exceptions proceed beyond representability
but still fail later at existing structural/default-model boundaries; they
are not counted as passing. Remaining failures match the pre-existing
visualization scalar assumptions (3), structural/default-model consumers
(13, counting Luna-12B, Luna-12L and the spiral control), Luna-12E legacy
observables (2), temporal-analysis consumers (3), and 3D viewer consumers (3).
No downstream consumer was changed.

The `_schedule()` fallback accepts a deliberately malformed direct private
same-time `S_REARM` call when the current state itself has an unrepresentable
analytic delay. Source inspection found that every E2 production call site
uses the analytic rearm calculation; the malformed request is therefore a
private-call misuse, not an externally reachable production path. This scope
is recorded in the independent handoff. E1's base scheduler/reset, E2 identity
and stale-event validation, and standalone TPCN-IR-2 schema revision 1 remain
unchanged. `math.nextafter()` is a software-reference representation detail,
not a canonical hardware timing rule. No ACP or A01-A15 change is made.

**GOVERNANCE:** Luna-23 is **CLOSED / INDEPENDENTLY VERIFIED**. Luna-22 remains
**BLOCKED / NOT CLOSED**; its IR-2 residual-provenance, dataset reproducibility
and downstream compatibility blockers remain. Luna-24 remains
**AUTHORIZED / NOT EXECUTED**. No consumer migration or dataset work is
authorized here. Full evidence is in
`workflow/handoffs/luna-0-independent-review-luna-23-e2-time-representability-20261003.md`.

# Luna-0 second independent review of ACP-0006 / Luna-22 - 2026-10-03

**VERDICT: BLOCKED / LUNA-22 NOT CLOSED.** Review started from the published
implementation revision
`a206f2e8fec8f0c72d9196b2bcca9d2e734c7974` on clean `main`, synchronized with
`origin/main`. The exact five-file implementation delta is recorded in
`workflow/handoffs/luna-0-second-independent-review-ACP-0006-Luna-22-20261003.md`.

The focused Luna-22 tests passed (41), and the prescribed component/integration
regression set passed (318). The independently rerun full suite had 27
failures, 770 passes and one CUDA-unavailable skip. The review independently
confirmed causal `t0/t1/t2` admission, same-time ordering, generation-guarded
stale-event no-op, emission-only routing, synthetic prediction/error and
delayed-credit mechanics, finite settling and reset.

Two corrective defects block closure:

1. E2 can calculate a mathematically positive rearm delay that rounds to the
   current floating-point timestamp, then raise instead of scheduling
   representable strictly future work.
2. Integrated IR-2 startup accepts a non-empty assigned provenance tuple and
   `provenance_truncated=True`, despite the accepted quiescent boundary
   requiring no residual provenance.

The reported UCI Character Trajectories subset is not repository-reproducible:
the ad-hoc loader/split procedure and per-class results were not retained.
The report shows low accuracy and zero matched test predictions; no numerical
accuracy threshold is inferred.

**NUMBERING / AUTHORIZATION:** Luna-23 is authorized / not executed for the
bounded ACP-0004 E2 logical-time representability correction in
`.github/agents/luna-23.agent.md`, dispatched in
`workflow/handoffs/luna-0-authorization-luna-23-e2-time-representability-20261003.md`.
Luna-24 is authorized / not executed for the bounded ACP-0006 integrated IR-2
residual-provenance correction in `.github/agents/luna-24.agent.md`, dispatched
in `workflow/handoffs/luna-0-authorization-luna-24-ir2-provenance-20261003.md`.
Their implementation file ownership is disjoint. Downstream visualization,
structural/research and benchmark consumer migration is not authorized by
this review. ACP-0006 remains accepted and unchanged; A01-A15 and IR-2 schema
revision 1 are unchanged.

The first pushed review-publication commit is
`baec12ad368239d959ca747d5a4e28c96746dd6e`; it adds this entry, the review
handoff, both authorization handoffs and both bounded Luna agent contracts.
This review does not claim integration readiness, dataset reproducibility,
predictive efficacy or hardware equivalence.

# Project-owner acceptance of ACP-0006 and Luna-22 dispatch - 2026-10-03

**ACP-0006 ACCEPTED AS WRITTEN; LUNA-22 AUTHORIZED / NOT EXECUTED.**

The project owner explicitly accepted ACP-0006 as written in the owner
direction received 2026-10-03. Accepted proposal revision:
`7eb997ebcb78f5a64074cd27a7a6181dbf693fa3` (`Propose ACP-0006 excursion
integration contract`). The acceptance and dispatch review started from that
revision after fetching `origin/main`; branch `main` was clean and
`HEAD == origin/main`. The acceptance publication revision is recorded in
`workflow/handoffs/luna-0-acp-0006-acceptance-luna-22-authorization-20261003.md`.

**DISPATCH REVIEW:** ACP-0006 is implementable as a bounded experiment-path
composition using the existing E2-capable neuron, finite `EventQueue`,
Model-B topology, predictor, eligibility ledger, streaming classifier,
activity-cost proxy and IR-2 adapters. The numbered rules identify the
external-input watermark and same-time ordering, queue/sidecar bounds and
causal ancestry, emission-only routing, causal prediction/error handling,
eligibility/reward attribution, two distinct existing readout surfaces,
bounded settling/reset, and quiescent IR-2 startup. The scheduler can hold
future internal events while admitting later-but-earlier external points;
the mandatory `t0 < t1 < t2` test remains a hard gate. The classifier consumes
actual readout emissions; the existing outer prototype learner consumes the
bounded signed-payload mean. No contradiction requiring new canonical
semantics was found. Dataset choice remains open in the existing sequential
dataset protocol and is a documented benchmark selection/reporting duty,
not a new architecture choice.

**NUMBERING:** Repository inspection found existing contracts through
Luna-21, with Luna-17 still reserved and unauthorized and Luna-19 through
Luna-21 already assigned/closed as recorded. No Luna-22 agent contract,
creation handoff, or active parallel Luna-22 assignment existed. Luna-22 is
the next legitimate unused identifier; it is authorized only for the first
CPU software-reference integration described in
`.github/agents/luna-22.agent.md`. That contract limits file ownership to
the experiment integration surface and focused tests, requires legacy and
excursion controls, all focused/adversarial tests and existing regressions,
and mandates an actual sequential-classification dataset/split report.

The authorization is creation-only in this task: **Luna-22 has not executed**.
No runtime test, dataset run or production implementation was performed here.
A01-A15 remain unchanged; ACP-0002 N2, ACP-0003 H1, ACP-0004 E1/E2,
ACP-0005/IR-2 revision 1, and Luna-21 remain closed and were not reopened.
N3, H2, IR-3, structural/edge learning, backends, hardware equivalence and
calibration remain unauthorized. Full decision evidence and next handoff
requirements are in
`workflow/handoffs/luna-0-acp-0006-acceptance-luna-22-authorization-20261003.md`.

# Luna-0 excursion integration contract proposal - 2026-10-03

**ACP-0006 CREATED / UNDER REVIEW; OWNER ACCEPTANCE REQUIRED. NO INTEGRATION
IMPLEMENTATION OR SUCCESSOR LUNA IS AUTHORIZED.**

The review synchronized to published `main` revision
`813186f87e7074415b550cf051ad2435c028d52a`, subject
`Reconcile Luna-21 status and integration readiness`; `HEAD == origin/main`,
branch `main`, and the pre-review worktree was clean.

**OBSERVED:** The normal experiment network constructs continuous
`TPCNNeuron` instances, makes an inference/routing decision on every scalar
activation, and uses the scalar path for prediction, eligibility, energy and
readout. The E1/E2 runtime instead emits zero or more canonical
`ExcursionEmission` records as bounded state changes and future internal
events are processed. The per-point experiment queue drains future events
without an external-input watermark. ACP-0004 fixes the post-migration
Model-B source as `p_exc` but does not specify this integrated queue, model
selection, predictor, error, credit, readout, settling, reset and startup
composition. ACP-0005 excludes complete live-network scheduler, predictor,
ledger and classifier state from IR-2.

**DECISION / RECOMMENDATION:** Choice C is recommended: a separate
integration/migration ACP, not an amendment to ACP-0004's neuron state machine
and not an implementation-only Luna task. ACP-0001 through ACP-0005 exist;
ACP-0006 is the next unused proposal number. The proposal gives candidate
decisions for all 17 requested integration boundaries, the mandatory
`t0 < t1 < t2` causal fixture, matched legacy/excursion controls and future
acceptance tests. It proposes the first normal integrated path as network-wide
E2-capable `EXCURSION_V1`, keeps `TANH_LEGACY` explicit, uses fixed topology,
and restricts IR-2 startup to quiescent clean state.

The architecture proposal lifecycle requires acceptance by the project owner
or an explicitly delegated architecture decision-maker. The available
governance record identifies the project owner as decision owner and contains
no explicit acceptance for ACP-0006. Accordingly it remains **Under review**;
no contract promotion, production code, successor Luna agent contract, Luna
number assignment or implementation authorization was created. A01-A15,
ACP-0002 N2, ACP-0004 E1/E2 and ACP-0005 remain unchanged.

**Remaining project-owner choices:** accept ACP-0006 as written; request
specific revisions; or reject it. No tests or runtime experiments were run;
this was a governance/documentation-only proposal. `git diff --check` passed.
The complete decisions, source evidence, future acceptance contract and
handoff are in `workflow/docs/architecture_proposals/ACP-0006.md` and
`workflow/handoffs/luna-0-architecture-decision-ACP-0006-20261003.md`.

# Luna-0 post-E2 integration dependency review - 2026-10-03

**LUNA-21 STATUS RECONCILED; E1/E2-TO-PREDICTIVE-CODING INTEGRATION IS NOT
READY OR AUTHORIZED.** Review baseline was published `main` revision
`c872dc8fbf74bf1a4e836619f1e02a96271c8633`, with a clean worktree.

**OBSERVED:** Luna-21's bounded IR-2 correction was already independently
verified and closed. The Luna-21 status table in `LUNA_WORKFLOW.md` still
reported the superseded blocker; that current-state row is corrected to
`CLOSED / independently verified`. The prior blocked review remains historical
evidence and is not removed.

**OBSERVED:** The ordinary `ExperimentRunner` network constructs
`TPCNNeuron` objects, routes the scalar activations they return, and supplies
those values to the prediction, eligibility and readout path. The
`LocalPredictor` neuron adapter is specifically typed for `TPCNNeuron`.
`SingleExcursionNeuron` / `MultiExcursionNeuron` are exported reference
components and are used by their own runtime and IR-2 serializers/reconstructors;
the production experiment network does not consume them. Existing excursion
and E2 IR-2 tests exercise the components and reconstruction, not integration
into that network.

**OBSERVED:** ACP-0004 specifies the post-migration Model-B source value
`a_i := p_exc`, and that the legacy continuous output is only an explicitly
labelled compatibility mode. It does not define a concrete network-level
migration/model-selection interface or the end-to-end prediction, error,
eligibility and readout wiring when an excursion runtime replaces the current
continuous neuron. ACP-0005/IR-2 defines transferable excursion state, not a
complete live-network checkpoint or an integration selector. The existing
acceptance criteria require predictive coding and delayed credit on the actual
streaming classification path.

**DECISION:** Treat component closure and computational-path integration as
separate gates. Integration is **not ready**. The available evidence does not
justify dispatching a successor Luna contract: the owner / Luna-0 must first
decide and record the migration/model-selection boundary and required
excursion-to-prediction/error/eligibility/readout interface. No production code,
ACP, Luna contract, or architecture promotion was created. This review does
not change ACP-0004's staged status, ACP-0005, A01-A15, or any hardware and
backend gates.

Validation was documentation-only: source/document inspection and
`git diff --check`; no tests or runtime experiments were run. Detailed evidence
and the next bounded decision are in
`workflow/handoffs/luna-0-post-e2-integration-dependency-review-20261003.md`.

# Luna-0 independent corrective review of Luna-21 ACP-0004 E2 - 2026-10-03

**PASS — LUNA-21 ACP-0004 E2 IMPLEMENTATION AND IR-2 CORRECTION
INDEPENDENTLY VERIFIED AND CLOSED.**

Review synchronized at published `main` revision
`3fb6d8c5128277bc8ecc5b2beea7288c214b772d`; `HEAD == origin/main`, branch
`main`, and the pre-review worktree was clean. The prior blocking review
`a9077997740ccdc374c7ad89deef122112967369`, corrective implementation
`ac2e822e5c7656d649c6e77f62024c6d6e4cf72f`, and corrective-handoff
publication `3fb6d8c5128277bc8ecc5b2beea7288c214b772d` are in the published
ancestry. The review handoff records the exact publication lineage and
evidence.

**OBSERVED:** An isolated detached checkout of the prior blocking revision
reproduced all three original defects: an ordinary active identity behind its
high-water counter was accepted and reused on promotion to M; an ordinary
`N` record with `next_event_identity = 2` and `event_budget = 1` survived a
JSON round trip; and an equal-time `S_EMIT` with absent optional M settings
was reconstructed and executed at local time zero.

**OBSERVED:** The correction rejects each malformed identity/high-water pair
in `S_PENDING`, `S_RETURN`, and `M_ACTIVE`; accepts active-ID/high-water
equality; and enforces the seven execution-counter bounds in every supported
mode. Independent boundary probes accepted `event_budget - 1` and
`event_budget`, and rejected `event_budget + 1`. E2 reconstruction rejects
pending work at or before local time even when optional M settings are
absent. The historical E1 adapter still executes a valid equal-time ordinary
pending record, and it still rejects `M_ACTIVE`.

The review identified the remaining empty-queue assertions in
`test_e2_reconstruction_restores_counters_and_continues_with_unique_ids` as
a **FIXTURE / ORACLE DEFECT**. Luna-0 made a test-only correction: the test
now executes bounded pending continuation and requires nonempty output and
transition traces, output IDs different from the prior emission, strictly
increasing output sequences, and final `N` with no pending event. Independent
execution produced 13 subsequent outputs, beginning at sequence 2 after
prior sequence 1, and reached `N`.

The shared counter check also applies to `TANH_LEGACY`, consistent with
bounded transferable counters; the explicit IR-1 upgrade path remains valid
and emits schema revision 1. IR-2 reconstruction preserves state, local
time, configuration, pending tuple, counters, provenance, truncation and
unassigned-provenance metadata without reset or automatic duplicate
scheduling. Exact-capacity and overflow provenance round trips preserved
causal identity, timestamp, signed contribution, ownership, order and sticky
truncation.

Active zero-valued lineage (and the no-pending `S_RETURN` zero-ID boundary)
is admitted by IR-2's nonnegative identifier domain. ACP-0004/ACP-0005 do not
require one-based IDs; subsequent allocation remains above the serialized
high-water mark. A pending generation of zero is rejected, matching the
runtime scheduler's positive generation allocation. No architecture
ambiguity or serialization defect was established by these probes.

**OBSERVED:** The corrective production diff from `a907799...` to
`ac2e822...` remains limited to `tpcn/ir2.py`, `tests/test_ir2.py`, and
`tests/test_e2_ir2.py`. `tpcn/excursion_neuron.py`, event runtime, topology,
Model-B routing, public exports, E1, N2 and schema revision were not changed.
No production code was changed during this independent review.

**Validation:** focused E2/E2-IR-2, 45 passed; E1/IR-2, 156 passed;
N2/event runtime, 254 passed; topology, 9 passed; final IR-2/E2-IR-2, 116
passed; full CPU, 768 passed and 1 skipped; `compileall` and diff checks
passed. The sole skip is `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`
because CUDA is unavailable; it is unrelated to the software-reference
closure and no backend/hardware checks were run.

A01-A15, ACP-0004 staged status, ACP-0005/TPCN-IR-2 revision 1, ACP-0002 N2,
closed E1, and all prohibitions remain unchanged. This closes only Luna-21's
implementation review; it does not claim hardware equivalence, integration
readiness, or authorize a successor. No successor Luna is assigned here.
Detailed evidence: `workflow/handoffs/luna-0-independent-corrective-review-ACP-0004-E2-Luna-21-20261003.md`.

The following blocking review is retained as historical evidence. Its verdict
was superseded by the independent corrective review above.

# Luna-0 independent review of Luna-21 ACP-0004 E2 - 2026-10-03

**BLOCKED — IR-2 RECONSTRUCTION DEFECT. LUNA-21 IS IMPLEMENTED BUT NOT
INDEPENDENTLY CLOSED.**

Review synchronized at `5d0171f46b90664b1a6aca5709cc2f07f19b7f4e` after
fetching `origin/main`; `HEAD == origin/main`, branch `main`, and the
pre-review worktree was clean. The authorized start
`0d26c3d6bd253ce3be1a3877ec5f2fcb0cf62868`, implementation
`bfc866be053f9692382d1be5e048f5b4d280e5f6`, and completion handoff
`5d0171f46b90664b1a6aca5709cc2f07f19b7f4e` exist in the stated ancestry.

The runtime review and requested regression commands passed. Independent
round-trip probes nevertheless showed that an `S_PENDING` IR-2 record with
`ordinary_episode_id = lineage_id = 2`, `next_episode_identity =
next_lineage_identity = 1` is accepted and reconstructed; promotion to M then
allocates `multi_episode_id = 2`, reusing the prior S episode identity. An
ordinary-mode record with identity counters greater than `event_budget` is
also accepted; the current counter-budget check is restricted to
`M_ACTIVE`. An E1-compatible pending record with optional M configuration
absent and `pending.timestamp == local_last_update_time` also passes schema
construction and can execute at that same timestamp through the E2 adapter.
See the independent-review handoff for exact reproductions and test results.

The checked-in REFRACTORY round-trip fixture also drains newly empty queues for
both runs, so its comparison can be empty-vs-empty and does not prove pending
M_REARM continuation. Independent direct execution of both restored and
original pending work matched 13 subsequent outputs, 26 state transitions,
identity counters, provenance, and final N state; this supports runtime
continuation but does not cure the fixture/oracle defect.

**Bounded corrective gate:** before closure, update the shared IR-2
cross-field validation and E2 reconstruction boundary so all execution
counters are within budget in every supported mode; ordinary active episode
and lineage identities are covered by their serialized high-water marks;
and an E2 reconstruction cannot execute a pending internal event at or
before local time. Preserve valid E1-only `neuron_from_ir2` behavior,
TPCN-IR-2 schema revision 1, and the explicitly named E2 capability. Replace
the empty-queue continuation fixture with a bounded regression that actually
executes reconstructed pending work and compares its trace and final state.
Re-run focused E2/IR-2, closed E1/IR-2, N2/event-runtime, topology, full CPU,
compileall, and diff checks. No production correction was made by this review.

A01-A15, ACP-0004 staged status, E1 closure, ACP-0005/TPCN-IR-2 revision 1,
ACP-0002 N2 closure, Luna-17's reservation, Luna-13F closure, and all
prohibitions remain unchanged. No successor Luna or architecture expansion is
authorized. Detailed evidence: `workflow/handoffs/luna-0-independent-review-ACP-0004-E2-Luna-21-20261003.md`.

# Luna-0 ACP-0004 E2/M clarification and Luna-21 authorization - 2026-10-03

**PASS — ACP-0004 E2/M IMPLEMENTATION BOUNDARY CLARIFIED; LUNA-21
AUTHORIZED BUT NOT EXECUTED.**

Starting from published revision
`40b453784b015552738f202c9a765a2f0587f533`, the four prior dispatch blockers
were resolved without changing A01-A15 or reopening closed E1/IR-2 behavior:

- ordinary and M episode IDs share one monotonic episode high-water counter;
- final residual S receives a new ordinary episode ID and preserves lineage;
- active provenance is re-owned to final S with sticky truncation;
- direct M-to-N creates no empty S episode;
- M reset clearing, stale queued-event behavior, retained counters and
  generation semantics are explicit;
- `neuron_from_ir2` remains E1-only while
  `neuron_to_ir2_e2`/`neuron_from_ir2_e2` form the separate E2 capability
  boundary;
- TPCN-IR-2 `schema_revision: 1` remains unchanged.

Luna-21 is authorized only for bounded E2 runtime and E2-capable IR-2
reconstruction implementation plus focused verification. It was not
executed by this governance task. ACP-0003 H2, ACP-0002 N3, backends,
hardware, calibration, Luna-13F reopening and Luna-13G remain unauthorized.

# Luna-0 final ACP-0004 E2/M dispatch review - 2026-10-03

**E2/M DISPATCH BLOCKED — CANONICAL IDENTITY, RESET, AND IR-2
RECONSTRUCTION BOUNDARIES REQUIRE EXPLICIT CLARIFICATION.**

Verified starting revision `8136c0e298a8fc8a72722eca349fd047b01f9aa0`.
ACP-0004 and the independently closed ACP-0005 define the bounded M state
machine, thresholds, positive event delays, promotion/cancellation,
discharge, finite-return bound, provenance capacity, identity uniqueness,
Model-B transfer and schema-level M representation. They do not unambiguously
define the final residual ordinary episode/provenance ownership, reset state
while M is active, or the named E2-capable IR-2 reconstruction boundary.

This review added an explicit clarification gate to ACP-0004. No E2 runtime
code, schema revision, Luna-21 contract, or implementation authorization was
created. E1, IR-2, A01-A15, ACP-0003 H2, ACP-0002 N3, backend/hardware
boundaries and Luna-13F/Luna-13G statuses remain unchanged.

## Luna-0 independent closure of ACP-0005 - 2026-10-03

**PASS — TPCN-IR-2 EXCURSION EXECUTION SCHEMA INDEPENDENTLY VERIFIED AND
CLOSED.**

Reviewed published revision `630af038dafd91903e3b03c26059989585b3760c` and
applied surgical schema corrections in the corrective review revision:

- preserved pre-admission provenance count and truncation state;
- preserved TANH legacy neuron gain, represented IR-1 events and all finite
  network resource limits during explicit IR-1 upgrade;
- rejected undeclared endpoints and duplicate directed edges;
- validated M episode ownership and ARMED/REFRACTORY pending-event pairing;
- stopped E1 conversion from fabricating M timing and residual parameters;
- added explicit IR-2 events, limits and adversarial fixtures.

Focused validation passed 73 tests. The full CPU suite, compilation and clean
publication status are recorded in the independent closure handoff.
E2/M runtime, H2, N3, backends, hardware, calibration, Luna-13F reopening and
Luna-13G remain unauthorized.

## Luna-0 ACP-0005 TPCN-IR-2 schema decision - 2026-10-03

**PASS — TPCN-IR-2 SCHEMA ACCEPTED FOR IMPLEMENTATION; LUNA-20 AUTHORIZED
BUT NOT EXECUTED.**

At starting revision `439e419a7e949d51fa487cac1acef0634c83215f`, accepted
ACP-0004 E1 was closed and ACP-0003 H1/IR-1 was closed. ACP-0005 defines the
explicit `TPCN-IR-2` version boundary and `TANH_LEGACY` /
`EXCURSION_V1` dynamics discriminator.

The schema contract preserves E1 modes, local time and decay configuration,
one valid pending internal event, destination-local external-before-internal
ordering, bounded provenance/truncation, episode/lineage/event/generation
identity continuity, Model-B edge fields and explicit reset-versus-transfer
semantics. It represents future M fields while requiring an explicit
unsupported-runtime error until E2 is separately authorized and implemented.

IR-1 remains frozen and cannot accept excursion records. TPCV-1, backend
realization state and calibration remain separate. A01-A15 are unchanged.
ACP-0003 H2, ACP-0002 N3, E2/M, backends, hardware, Luna-13F reopening and
Luna-13G remain unauthorized. Evidence and the implementation boundary are in
`workflow/docs/architecture_proposals/ACP-0005.md` and
`workflow/handoffs/luna-0-architecture-decision-IR-2.md`.

## Luna-0 independent closure of ACP-0004 E1 - 2026-10-02

**PASS — ACP-0004 E1 CANONICAL SINGLE-EXCURSION REFERENCE INDEPENDENTLY
VERIFIED AND CLOSED.**

Reviewed the published Luna-19 implementation at
`f0a5977db1a56ac559262e52413f31ebf15092f5` and applied only directly required
closure fixes:

- episode/lineage ownership and isolation for bounded provenance;
- destination-local external-before-internal equal-time ordering, preserving
  prior sequence ordering for unrelated destinations;
- ULP-scale numeric termination handling at a valid analytic re-arm boundary;
- adversarial tests for configuration bounds, reset stale-event isolation,
  stale re-arm cancellation, non-default Model-B fan-out and identity
  preservation.

Focused E1/runtime validation passed 59 tests. The broader review regression
bundle passed 429 tests, and the full CPU suite passed 612 tests with one
existing skip. Compile and diff validation are recorded in
`workflow/handoffs/luna-0-independent-closure-ACP-0004-E1.md`.

A01-A15 remain unchanged. M/multi-excursion execution, TPCN-IR-2,
ACP-0003 H2, ACP-0002 N3, backends, hardware equivalence, learning changes,
Luna-13F reopening and Luna-13G remain unauthorized. The next recommended
dependency is a separately reviewed TPCN-IR-2 schema before any E2/M work;
this entry does not authorize it.

## Luna-0 ACP-0004 acceptance and E1 authorization - 2026-10-02

**PASS — ACP-0004 ACCEPTED FOR STAGED IMPLEMENTATION.**

Revised ACP-0004 from the `80b7989ec5b7f5913362e812eddcc3d845b826c4`
baseline and closed the remaining canonical blockers without changing A01-A15
or implementing runtime code.

- The explicit bounded mode machine is `N`, `S_PENDING`, `S_RETURN` and
  `M_ACTIVE`, with `M_ACTIVE` phases `ARMED` and `REFRACTORY`.
- Ordinary admission, one-event emission, analytic finite re-arm, M
  promotion, M discharge, final residual S behavior and sign handling are
  defined exactly.
- Internal events use positive finite delays, deterministic external-before-
  internal equal-time ordering, bounded generation cancellation and one valid
  pending event per neuron.
- The amplitude map, M payload, saturating discharge, finite-return bound,
  provenance capacity/overflow, identity/lineage and Model-B `a_i` semantics
  are canonical.
- `TPCN-IR-2` is required for a future excursion schema; IR-1 remains closed
  and no IR-2 implementation is included.
- E1 is authorized for Luna-19: static leaky accumulation and
  single-excursion reference only. M, learning, backends, approximation,
  calibration, H2 and IR-2 remain excluded.

Created `.github/agents/luna-19.agent.md` as an implementation contract;
Luna-19 is authorized but not executed by this review. ACP-0002 N3 remains
unauthorized, Luna-13F remains CLOSED, Luna-13G remains unauthorized and
Luna-17 remains reserved.

Evidence: `workflow/docs/architecture_proposals/ACP-0004.md` and
`workflow/handoffs/luna-0-architecture-acceptance-ACP-0004.md`.

## Luna-0 independent review of ACP-0004 - 2026-10-02

**ACP-0004 REMAINS DRAFT — NOT ACCEPTED FOR STAGED IMPLEMENTATION.**

Reviewed the committed proposal `c18757739f4055bbb5721520a14382701e177d64`
against the A01-A15 contract, ACP-0002 N2, and the closed ACP-0003 H1
boundary. The proposal is directionally compatible with event-driven,
bounded, hardware-neutral computation, but its canonical state machine is not
yet implementable without backend-specific interpretation.

- Canonical terminology is **excursion**. GPU/software and FPGA reference
  semantics require exactly one digital event per excursion; FPAA physical
  spikes/analog excursions remain realizations.
- Compression is
  `C_E = N_input_contributions / N_output_excursions`; multi-excursion
  encoding is a separate behavior.
- The required persistent state boundary is signed bounded `x` plus a local
  timestamp, with bounded mode/phase, lineage, provenance, payload and
  pending-event bookkeeping. A persistent `y` is not accepted as redundant
  state without evidence.
- Blockers are exact autonomous-event timestamps and cancellation, complete
  ordinary and multi-excursion transition rules, input-during-return behavior,
  finite provenance/overflow semantics, amplitude/sign rules, and versioned
  excursion IR migration (expected `TPCN-IR-2`).
- The draft's cross-domain comparison `h_L >= theta_hold` is rejected;
  oscillator hysteresis and accumulated-state hold thresholds must have
  separate domains.
- ACP-0003 future-neuron wording was clarified to use canonical excursion and
  one-event digital realization without authorizing H2 or an IR extension.

No production neuron, backend, IR-2 implementation, Luna-19 contract, H2,
ACP-0002 N3, Luna-13F reopening or Luna-13G authorization follows. Evidence
and the complete 35-item review record are in
`workflow/handoffs/luna-0-architecture-review-ACP-0004.md`.

## Luna-0 independent closure of ACP-0003 H1 - 2026-10-02

Independently reviewed the Luna-18 corrective H1 implementation at
`4aee46829807072e9af0f08842d561026555006d`, following the original blocked
review and corrective implementation `414491edc3d9ff0e8e8f751f534e5e93ab88b6d0`.

**PASS — ACP-0003 H1 EXECUTION IR/BACKEND INTERFACE INDEPENDENTLY VERIFIED AND
CLOSED**

- Blocker 1 CLOSED: only the explicitly discoverable `tanh` activation is
  supported, and reconstruction rejects unsupported semantics.
- Blocker 2 CLOSED: sequence identities are unique within `ExecutionIR`,
  including across timestamps; equal-time ordering survives reconstruction.
- Blocker 3 CLOSED: `ApproximationContract` now declares the supported IR
  version, optional numeric/timing tolerances, statistical requirement,
  bounded approximation boundary, E0-E4 claims and equal-time policy.
- Blocker 4 CLOSED: IR-1 is explicitly a configuration plus transferable
  initial/reference-state representation, not a full live-runtime checkpoint.
- Independent focused bundle: `381 passed, 1 skipped`; full CPU suite:
  `567 passed, 1 skipped`; compilation, diagnostics, direct probes and
  `git diff --check` passed.
- A01-A15 remain unchanged. TPCV-1 remains downstream-only and distinct from
  TPCN-IR-1. No backend, approximation, calibration, attractor or edge-learning
  implementation was added.

H2 remains unauthorized. ACP-0002 N3 remains unauthorized, Luna-13F remains
closed and Luna-13G remains unauthorized. The next dependency is a separately
authorized attractor/event-compression neuron architecture contract before H2
approximation work; the current IR version boundary is compatible with such a
future extension but does not implement it.

Evidence: `workflow/handoffs/luna-0-independent-corrective-review-ACP-0003-H1.md`.

## Luna-0 Luna-18 creation and numbering reconciliation - 2026-10-02

Created and authorized `.github/agents/luna-18.agent.md` for ACP-0003 H1,
**Execution IR and Backend Interface Skeleton**, at publication baseline
`a757fe510c5b3545da2161b27a53deaae01676bf`.

- Luna-15 current role is ACP-0002 N1, edge/neuron data model and compatibility.
- Luna-16 current role is ACP-0002 N2, static Model-B edge transfer; N2 is
	closed.
- The older Luna-15 FPGA/VHDL and Luna-16 FPAA reservations are preserved as
	historical planning records but superseded as current assignments.
- Luna-17 remains `RESERVED / NOT AUTHORIZED / NO ACTIVE CONTRACT` for
	hardware-equivalence / cross-backend hardware acceptance. No Luna-17 contract
	is created here.
- Luna-18 is `AUTHORIZED / NOT STARTED`; H1 uses `TPCN-IR-1`, declares
	`SEQUENTIAL_DETERMINISTIC` and future `COINCIDENT_WINDOW` policies, and does
	not authorize H2, production
	backends, approximation, calibration, attractor neurons or hardware work.
- ACP-0002 N3 remains unauthorized, Luna-13F remains closed, Luna-13G remains
	unauthorized and A01-A15 remain unchanged.

The creation/authorization handoff is
`workflow/handoffs/luna-18-h1-creation-authorization-Luna-0.md`.

## Luna-0 ACP-0003 heterogeneous execution architecture update - 2026-10-02

Created **ACP-0003 — Heterogeneous Execution and Backend Separation** from
the project-owner request at baseline revision
`434a000029ebf52d87d15ece6d3681eafdfd23f1`.

- Status: **UNDER REVIEW**; project-owner acceptance is still required.
- Establishes the proposed boundary
	`canonical semantics -> device approximation contract -> device implementation`.
- Defines a conceptual hardware-neutral TPCN Execution IR, portable logical
	state, separate backend realization/calibration state, equivalence classes,
	staged comparison levels and logical-versus-physical resource accounting.
- Reviews GPU native, GPU FPGA approximation, FPGA native, GPU FPAA
	approximation, FPAA native and a possible FPGA+FPAA hybrid.
- Equal-time fan-in remains ACP-0002 N2's deterministic sequential semantic;
	simultaneous FPAA summation is explicitly unresolved/approximate unless a
	later contract declares serialization or tolerance.
- A01-A15 remain unchanged. No production backend, IR implementation,
	calibration, edge learning, ACP-0002 N3, Luna-13F reopening or Luna-13G
	authorization follows from this entry.

Evidence and the bounded next assignment are recorded in
`workflow/handoffs/luna-0-architecture-update-ACP-0003.md`.

## Luna-0 ACP-0003 staged-implementation decision - 2026-10-02

ACP-0003 is **ACCEPTED FOR STAGED IMPLEMENTATION** with one bounded first
stage. Equal-time FPAA fan-in uses Model C through canonical Model B semantics:
strict serialization is a validation/reference mode, while coincident analog
integration is a backend approximation governed by a calibrated backend
coincidence window, never canonical network state.

- Equivalence levels are E0 semantic, E1 numerical, E2 event, E3 functional
	and E4 statistical, with requirements varying by backend and mode.
- The canonical workload/resource boundary and architecture/calibration failure
	taxonomy are now explicit, including hardware-limit failure.
- Luna-18 is authorized for H1, the Execution IR/backend interface skeleton
	only. No numerical approximation, production backend, hardware calibration,
	attractor neuron, edge learning, ACP-0002 N3, Luna-13F reopening or Luna-13G
	authorization follows.

The updated decision and dispatch are recorded in
`workflow/handoffs/luna-0-architecture-update-ACP-0003.md` and
`workflow/handoffs/luna-18-execution-ir-backend-interface-Luna-0.md`.

## Luna-15 ACP-0002 Stage N1 - 2026-09-30

Implemented the accepted-for-staged-implementation ACP-0002 N1 data-model
boundary. Edges now represent bounded efficacy, divider strength and reference
state, and neurons expose bounded `neuron_gain` with a compatibility
`input_gain` alias. Legacy topology construction, deterministic rebuilds,
observer inspection and raw payload routing remain compatible.

This entry does not activate the Model-B transfer equation, add edge learning,
change structural admission/pruning semantics or authorize N2. A01-A15 remain
unchanged; Luna-13F remains closed and Luna-13G remains unauthorized.

## Luna-0 independent review of ACP-0002 Stage N1 - 2026-09-30

Reviewed implementation revision
`7ddf00b6c7a8f01ad4ebe3483bc553c83dbe26d3` after synchronization with
`origin/main`; the worktree was clean and `HEAD == origin/main`.

**PASS - ACP-0002 N1 DATA MODEL AND COMPATIBILITY INDEPENDENTLY VERIFIED**

- Edge bounds, defaults, equality, direct construction and public topology
	paths were independently checked.
- Extreme valid transfer fields remained dormant: routing preserved the exact
	legacy payload, event metadata, delay and sequence ordering.
- Neuron `input_gain` and `neuron_gain` were equivalent with one stored value;
	conflicting aliases were rejected.
- Explicit edge state survived pruning/rebuild; candidate scores were not
	copied into new edge parameters; bounded admission/pruning behavior was
	unchanged.
- TPCV-1 remains a documented version-1 observability boundary that omits
	transfer fields until a future format version; canonical edge equality,
	topology replay and edge instrumentation retain them.

Evidence and exact commands are recorded in
`workflow/handoffs/luna-0-review-ACP-0002-N1.md`. ACP-0002 remains accepted
for staged implementation, N2 remains unauthorized, A01-A15 remain unchanged,
Luna-13F remains closed and Luna-13G remains unauthorized.

## Luna-16 ACP-0002 Stage N2 - 2026-09-30

Implemented static Model-B edge transfer under the controlled canonical
cutover. For numeric neural `signal` events, routing computes
`z=tanh(w*a)` and `v=d*z+(1-d)*r`, then schedules `v` after the existing
positive finite delay. Control and metadata payloads remain opaque. Existing
destination local-time decay, bounded integration, neuron gain and fixed
activation remain unchanged.

Implementation revision: `ed8aaff2d0d0d031c2c1f84b311251f530282479`.
The N2 baseline is `artifacts/acp-0002-n2-model-b-baseline/baseline.json`.
Focused N2 tests: 267 passed. Full CPU suite: 549 passed, 1 skipped.
Compilation and `git diff --check` passed. Causality, timestamps, positive
delays, deterministic ordering, bounded queue/state/execution, structural
defaults and reconstruction, label/future isolation, reward boundaries and
observer behavior remain invariant; numeric payload/state traces are expected
to change at the N2 boundary.

TPCV-1 remains valid only as its limited downstream observational format and
does not claim active transfer-state equivalence. No A01-A15 text changed.
Luna-13F remains closed; Luna-13G and N3/later ACP-0002 stages remain
unauthorized.

## Luna-0 independent review of ACP-0002 Stage N2 - 2026-09-30

Reviewed publication revision `7652e6fc33b690766b49f29b07894e395d3756d7`
after synchronization with `origin/main`; the worktree was clean and
`HEAD == origin/main`. The implementation revision was
`ed8aaff2d0d0d031c2c1f84b311251f530282479` and the tree was
`dcc226ae9ad4da0b40f893a42b2883b056d9d679`.

**PASS - ACP-0002 N2 STATIC MODEL-B TRANSFER INDEPENDENTLY VERIFIED AND CLOSED**

- Direct analytic probes verified `z=tanh(w*a)` and
	`v=d*z+(1-d)*r`, including divider endpoints, weight zero, signed values,
	independent parameter effects, finite extremes and distinct fan-out payloads.
- Destination processing is `clip(decay(s,dt)+v)` followed once by
	`tanh(neuron_gain*s)`; the baseline equation string was corrected to match
	this executed path.
- Equal-time arrivals remain deterministic and sequential by queue order.
	A destination may emit downstream work after the first arrival and before
	the second; this is canonical event-driven semantics, not synchronous sum.
	Unequal delays decay over actual elapsed local time, and bounded recurrence
	stops only at the explicit execution budget.
- Structural defaults, non-default reconstruction, observer ON/OFF equality,
	control-payload opacity, reward/eligibility boundaries, predictive coding,
	label isolation and TPCV-1 limited-purpose governance remain preserved.
- The inherited `legacy_identity` field was probed and has no routing effect;
	no hidden legacy bypass exists. It remains a non-computational N1 residue,
	not an active N2 mode.

Independent validation selected 103 focused invariant tests, the full CPU
suite (`549 passed, 1 skipped`), compilation, direct analytic/runtime probes,
baseline parsing and test-change audit. A01-A15 remain unchanged. ACP-0002
N2 is closed; N3 and later stages remain unauthorized, Luna-13F remains
closed and Luna-13G remains unauthorized. Evidence is recorded in
`workflow/handoffs/luna-0-review-ACP-0002-N2.md`.

## Luna-16 ACP-0002 Stage N2 authorization - 2026-09-30

Following publication and independent verification of N1, Luna-0 selected
**CONTROLLED CANONICAL CUTOVER**. N1 is the final representation-compatible
legacy-execution version. Luna-16 is authorized to activate the accepted
Model-B static transfer as the new canonical execution revision:

`z_ij = tanh(w_ij * a_i)` and
`v_ij = d_ij * z_ij + (1 - d_ij) * r_ij`.

The contribution is delayed by the existing positive finite `tau_ij` and then
uses the existing destination local-time decay, bounded integration, neuron
gain and fixed nonlinearity. The N1 defaults `w=1,d=1,r=0` intentionally yield
`tanh(a)`, not raw `a`; no legacy-equivalence claim is made. Historical
committed results retain their original architecture context, and future
experiments must identify the N2 revision. No permanent per-edge legacy flag
is introduced.

This authorization is static only. Edge learning, edge maturation,
probationary edges, new utility/pruning policy, temporal mini-networks,
hardware-specific voltage semantics and later ACP-0002 stages remain
unauthorized. Luna-16 must establish analytic transfer and deterministic
Model-B baseline evidence while preserving A01-A15, causality, bounded
topology/dynamics, label/future isolation and observer non-interference.
TPCV-1 remains an explicit observational boundary; any versioning dependency
must be returned to Luna-0 rather than silently losing active edge state.

The authorization contract is `.github/agents/luna-16.agent.md` and the
governance handoff is `workflow/handoffs/luna-16-n2-authorization-Luna-0.md`.

## 1.0 — 2026-09-26

Established the documented candidate contract from the source conversation and current owner request.

- Event-driven operation with local time, finite propagation, bounded topology and bounded dynamics.
- Spatial reservoir deprecated from core; legacy comparisons remain separate.
- Predictive coding, explicit error events, local learning and delayed credit preserved.
- Local energy accounting is reward-adjusted: minimize unrewarded expenditure.
- Exactly ten pathways and explicit gating are soft/experimental.
- Sequential letter strokes are the first integration target.
- FPGA/VHDL, FPAA and hybrid realizations remain eventual branches.
- Added role workflow, acceptance criteria, ACP and handoff templates.

This entry records documentation establishment, not completed implementation or hardware validation.

## 1.1 — 2026-09-28 — ACP-0001

Accepted by explicit project-owner direction in the post-12H architecture
request; exact temporal-association and bootstrap algorithms remain
experimental and are not promoted by this entry.

- Strengthened A14 so bounded structural plasticity must retain a legal,
	measurable route to useful convergent causal structure without prescribing a
	graph shape or learning formula.
- Required explicit bounded admission/replacement/pruning outcomes and
	rejection causes, including duplicate and capacity/locality/utility causes.
- Permitted causally available temporal relationships and finite-delay path
	shortening as experimental evidence, without making a timing rule mandatory.
- Clarified under A07 that offline/module bootstrap initialization may prepare
	reproducible state but cannot leak global trainer information into runtime
	neural computation.
- Added the Future Luna Contract, Luna-12I temporal-associative structural
	growth, and Luna-12J modular/bootstrap initialization milestones.

This is a contract/governance change, not evidence that temporal association or
modular bootstrap training works. Luna-13 through Luna-17 retain their prior
meanings and independent observability/hardware gates.

## Luna-12J dispatch scaffold - 2026-09-28

Re-scoped the previously unexecuted Luna-12J placeholder as **Temporal-
Associative Structural Learning Efficacy and Causal Verification** after the
Luna-12I handoff returned **PASS WITH FOLLOW-UP**. This is a workflow and
experiment-scope update, not an architecture change.

- Luna-12J is classified `EXPERIMENT`, `VERIFICATION` and follows Luna-12I.
- It compares fixed topology, the pre-12I policy, random legal growth and
	Luna-12I temporal growth under comparable resources and temporal controls.
- It verifies that learned topology changes the real Luna-12E routed path and
	uses a causal intervention; topology appearance alone is insufficient.
- A14 remains unchanged. A successful result returns to Luna-0 for separate
	architecture review and does not authorize a later implementation Luna.
- Luna-13 and Luna-14 remain independent siblings. No real-data, hardware or
	bootstrap-trainer work is authorized by this entry.

For later changes record date, contract version, accepted ACP, decision owner, clauses affected, evidence, compatibility and migration/rollback implications.

## Luna-13A creation - 2026-09-29

Created the formal **Stage-0 Software Reference Invariant Closure** contract
from the synchronized reviewed checkpoint
`fdda3b59014109ce5aac6c5b2c9690b02acf85e9` after the independent review of
the corrected Luna-12N work.

- Luna-12N remains **PASS WITH FOLLOW-UP — MEASUREMENT CORRECTED, EFFICACY
	STILL UNESTABLISHED**. Its corrected evidence separates configured from
	actual operations, uses independent metadata controls and replay-measured
	arrivals, distinguishes weighted delay from hop count, exposes budget
	exhaustion and provenance, and does not show a decay-caused admitted-edge or
	final-graph difference.
- Luna-13A is a CPU-only Stage-0 implementation/verification assignment for
	classifier temporal monotonicity, reward-delivery contract consistency,
	projected structural-capacity rejection semantics and bounded recurrent
	execution. No dedicated GPU, CUDA, GPU visualization, FPGA or FPAA is
	required.
- The reward contract is a mandatory pause condition: contradictory repository
	authority returns `REWARD CONTRACT DECISION REQUIRED` with both model
	consequences and bounded-state/replay implications. No Luna-13B or other
	successor is authorized. Luna-0 must independently review the completed
	Stage-0 handoff before determining the next assignment.

This is a workflow and implementation-scope update only. A01-A15 and the
architecture contract are unchanged; no ACP is created.

## Workflow observability track — 2026-09-27

Added a distinct downstream-only visualization and verification track:

- Luna-12: canonical visualization contract and CPU reference exporter/parser.
- Luna-13: GPU-compatible exporter using the Luna-12 format, gated on Luna-12.
- Luna-14: ModelSim/FPGA trace bridge and Terasic DE1-SoC visualization foundation, gated on Luna-12.
- Luna-12A: optional CPU training and TPCV-1 replay integration after Luna-12, using the deterministic Luna-9 synthetic path; not a prerequisite for Luna-13 or Luna-14.

Visualization is not part of the canonical TPCN computational architecture. It is an observability and verification facility used to inspect structure formation and activity across CPU, GPU, simulation, and FPGA implementations. No return path into the TPCN computational datapath is permitted. The former FPGA/VHDL, FPAA, and hardware-equivalence milestone contracts were preserved as Luna-15, Luna-16, and Luna-17 to resolve the existing numbering conflict. This is a workflow change, not a contract change or implementation result; Luna-12 is the only new milestone eligible for explicit authorization, and Luna-13/Luna-14 remain blocked until its gate passes.

## Luna-12B authorization — 2026-09-27

Authorized Luna-12B, Persistent Topology and Structural Plasticity Visualization Integration, after the owner-supplied Luna-12A completion evidence: full suite 130 passed with 1 skipped, focused Luna-12A tests 3 passed, compilation and diagnostics passed, `git diff --check` passed, and a three-snapshot smoke run replayed deterministically.

- Luna-12B integrates one persistent bounded Luna-4 topology with the validated Luna-10 structural-plasticity API in the deterministic Luna-9 CPU path.
- It is an integration/observability milestone, not a canonical architecture change; A01-A15 remain unchanged and no ACP is required.
- Luna-12B is not a prerequisite for independently authorized Luna-13 or Luna-14.
- Real-dataset benchmarking and Luna-15/Luna-16/Luna-17 remain separately gated and are not authorized by this entry.

## Luna-12C authorization - 2026-09-27

Authorized Luna-12C, Human-Interpretable 3D Temporal Visualization, as a
replay-first observational milestone after the existing Luna-12 TPCV contract
and CPU replay integrations.

- Luna-12C adapts the existing Python pygame/PyOpenGL and NumPy infrastructure
	for deterministic 3D replay, stable layout, topology-change inspection,
	playback, filtering, neuron selection, and synchronized metrics.
- Luna-12C is downstream-only and does not change A01-A15, TPCV-1 semantics,
	computation, event ordering, timestamps, topology decisions, reward,
	classifier behavior, training, or reproducibility; no ACP is required.
- Current TPCV-1 lacks canonical 3D coordinates, event-by-event propagation
	timing, per-edge traffic, and per-neuron energy/utility fields. The viewer
	must show snapshot-level activity and unavailable fields honestly rather
	than fabricate pulses or values.
- Luna-12C is not a prerequisite for Luna-13 or Luna-14; their dependencies
	and authorization boundaries are unchanged. Luna-15/Luna-16/Luna-17 remain
	separately gated and unauthorized by this entry.

## Luna-12D/12E workflow authorization - 2026-09-27

Added two separate follow-up milestones after Luna-12C without changing the
canonical architecture contract or requiring an ACP.

- Luna-12D, Temporal Interpretability and Network-Dynamics Analysis, is
	authorized to analyze existing replay artifacts and permitted deterministic
	synthetic runs. It measures topology/activity dynamics and investigates
	plateau rejection reasons without repairing topology/computation coupling.
- Luna-12E, Computational Topology Integration and Causal Learning
	Verification, is blocked until Luna-12D completes and Luna-0 reviews its
	evidence. It owns future integration of persistent topology into the actual
	event-routing path and controlled causal verification.
- Luna-13 and Luna-14 remain independent siblings and do not depend on 12D or
	12E. Real-dataset benchmarking, hardware acceptance, and Luna-15/16/17 are
	not authorized by this entry.

## Luna-12F authorization - 2026-09-27

Authorized Luna-12F, Readout Learning and Class-Separation Verification, after
the accepted Luna-12E evidence established persistent bounded topology in the
actual event-routing path and causal reachable-edge effects. The current
implementation condition `reward > 0.0` for prototype updates is confirmed as
an observed gate and remains a root-cause hypothesis for Z class starvation
until the 12F fixture verifies it.

- Luna-12F is an external supervised-readout milestone, not a topology
	milestone and not a change to A01-A15; no ACP is required.
- Labels remain forbidden from canonical events, neuron/predictor state,
	topology mutation evidence, routing, structural-plasticity decisions, and
	energy computation.
- Luna-12F follows Luna-12E and preserves its computational topology
	integration. Luna-13 and Luna-14 remain independent siblings with no new
	dependency on 12F.
- Real-dataset benchmarking, Luna-15/Luna-16/Luna-17, and an architecture-wide
	classifier redesign remain unauthorized.

## Luna-12G authorization - 2026-09-27

Accepted the Luna-12F completion handoff for the corrected bounded external
readout and authorized Luna-12G, Spiral Handedness Temporal Classification
Benchmark.

- Luna-12G replaces the shortcut-prone synthetic A/Z workload with disjoint,
	seeded center-outward left/right spiral trajectories whose primary class
	information is ordered handedness.
- The benchmark requires class-independent nuisance variation, no-learning,
	fixed-topology, structural-plasticity, shuffled-order, time-reversal,
	matched-nuisance, and opposite-handed controls.
- Labels remain external to canonical events, neuron/predictor state, routing,
	topology evidence, structural-plasticity evidence, and energy computation.
- Luna-12G is a synthetic software-reference experiment and does not authorize
	real handwriting, GPU/FPGA/ModelSim acceptance, or hardware promotion.
- Luna-13 and Luna-14 remain independent siblings with no new dependency on
	Luna-12G. No A01-A15 clause changed and no ACP is required.

## Luna-12H authorization - 2026-09-27

Authorized Luna-12H, Intrinsic Temporal State, Recurrence, and Unequal-Delay
Convergence, after the Luna-12G evidence showed identical ordered, shuffled,
and reversed classification results. This is a core implementation and
verification clarification, not a benchmark-specific handedness rule.

- The existing contract already permits local elapsed-time state, finite
	recurrent dynamics, finite propagation, and locally scheduled events. The
	contract now explicitly requires the canonical/reference path to expose
	persistent bounded local state, deterministic temporal noncommutativity,
	unequal cumulative path delays, timestamp-preserving fan-in, reset/isolation
	policy, and bounded cycle behavior.
- Luna-12H must verify intrinsic temporal state and network/path temporal state
	without a mandatory global neural timestep or hidden recurrent tick. It must
	use the accepted Luna-12E event-routing path and Luna-12G limitation as
	motivation, while keeping labels outside the neural core.
- No ACP is required: these semantics are already permitted by A01-A03 and
	A08; this entry makes their canonical evidence obligations explicit.
- Luna-12H follows Luna-12G. Luna-13 and Luna-14 remain independent siblings
	and do not depend on 12H. Real-dataset, hardware, and post-observability
	milestones remain separately gated.

## Luna-12K creation - 2026-09-28

Created the formal **Capacity-Pressure, Equal-Exposure, and Path-Shortening
Verification** follow-up from the current HEAD
`e0f308f5aa76cdf41578f0574a2135b9bb0b256d` after verifying the Luna-12J
`partially supported` / `PASS WITH FOLLOW-UP` result.

- Luna-12K is classified `EXPERIMENT` and `VERIFICATION`; it requires equal
	candidate exposure, competing legal candidates, actual bounded capacity
	pressure with precise rejection causes, and a functional long-path fixture
	with a causal shortcut intervention.
- The 12J raw evidence and handoff confirm five declared seeds, temporal
	accuracy `1.0`, one convergent motif, eight routed events, lower proxy
	energy than baseline, the eight-to-six causal intervention, and no
	demonstrated path shortening because no initial long path existed.
- This entry authorizes milestone creation only. Luna-12K execution requires
	a separate explicit assignment and returns to Luna-0; no A14 clause,
	architecture contract, ACP status, Luna-12L or later work is authorized.
- Luna-13 and Luna-14 remain independent siblings, and the legacy baseline is
	preserved.

## Luna-12L creation - 2026-09-28

Created **Energy/Prediction Tradeoff and Four-Class Temporal Scale
Verification** from the Luna-0 review of Luna-12K at current HEAD
`3122c7dbae2589c1c78fe6169d394f525c212ec1`.

- Luna-12L is classified `EXPERIMENT` and `VERIFICATION`; it compares fixed,
	pre-12I, random, temporal-associative and reversed/shuffled timing controls
	on a four-class spiral benchmark at reference and modest expanded scales.
- It directly addresses the observed Luna-12K tradeoff: temporal proxy energy
	`9.850877` versus adaptive-control `9.274247`, and temporal prediction loss
	`1.284030` versus `1.025229`.
- It requires class-neutral inward/outward generation, no class-marker events,
	equal declared budgets, seeds `0..4`, joint classification/prediction/
	resource measurements, class-conflict analysis and a learned-edge causal
	intervention.
- This is a workflow and experiment-scope update only. A14 and the
	architecture contract are unchanged; execution requires a separate explicit
	assignment and all results return to Luna-0. No later Luna is authorized.

## Luna-12M creation and execution - 2026-09-28

Created and executed **Edge Lifecycle, Route Utilization, and Competing-Path
Instrumentation** from the Luna-0 12L direction/decay review at baseline
`7f8ea2df5896d3ea7cd7d41a4f1bd8298c0dc015`.

- Luna-12M is `OBSERVATION`, `VERIFICATION` and `IMPLEMENTATION`; it adds a
	downstream-only bounded observer and deterministic competing-path fixture.
- Endpoint-plus-generation identities, lifecycle transitions, routed traffic,
	decay context and candidate/pruning observations are exported separately
	from TPCV-1 as versioned `TPCN-EDGE-1` JSON.
- Focused ON/OFF evidence preserves traces, digests and mutation outcomes;
	persistent edge strength, utility and eligibility remain absent rather than
	being invented. No A01-A15 clause or pruning/decay policy changed.
- The evidence gate is `PASS WITH FOLLOW-UP` because replacement attribution
	and hardware-facing export remain unavailable. Results return to Luna-0 and
	no successor Luna is authorized by this entry.

## Luna-0 Luna-12M evidence review - 2026-09-28

Reviewed the Luna-12M artifact and focused evidence. The observer’s identity,
bounds, determinism, decay context and ON/OFF non-interference passed, but the
milestone is **BLOCKED** pending three bounded repairs: replace hard-coded
competing-path summary fields with phase-scoped measured traffic, stop using
`0.0` as an unavailable growth timestamp, and emit capacity/fan-in/fan-out
rejection lifecycle records. This is an evidence-quality decision, not an
A01-A15 change or successor authorization.

## Luna-12N creation - 2026-09-28

Created **Temporal Direction and Intrinsic-Decay-Gated Shortcut Verification**
from the corrected Luna-12M `PASS WITH FOLLOW-UP` evidence at baseline
`0d91207ec5db0ab8011e0fc020cc9e4e20915428`.

- Luna-12N is classified `EXPERIMENT` and `VERIFICATION`; it compares current
	and reversed legal direction, intrinsic-decay-relative variants, random legal
	growth and fixed topology under equal candidate opportunity.
- The primary metric is used shortcut yield: accepted mutations that both
	reduce measured cumulative causal delay and carry measured routed traffic,
	reported separately from static shortcut yield. Corrected Luna-12M
	`TPCN-EDGE-2` phase-scoped traffic, lifecycle, candidate/rejection and decay
	records remain the measurement basis.
- The experiment preserves A01-A15, does not alter pruning or persistent edge
	state, does not create an ACP, and does not make direction or decay gating
	mandatory. No execution or successor Luna is authorized by this creation.

## Luna-0 independent review of corrected Luna-12N - 2026-09-29

Reviewed pushed revision `2d4726a9b9aa3e19afdc458a2f448f8d72a4c3f7` and
reproduced the corrected artifact under CPU-only execution. The repository was
clean and synchronized with `origin/main`. The review found and repaired two
reporting defects during verification: exact event-budget truncation could
report `completed: true` when only one workload example had finished, and
current-versus-decay admitted-edge comparison was order-sensitive rather than
set-sensitive.

- Closed: fixed-topology operation accounting, independent metadata negative
	control, replay-measured arrivals, weighted delay paths, explicit truncation,
	candidate evidence provenance, graph-state intervention labels and
	baseline/executed-revision separation.
- Reproduced: decay changes score magnitude and rank in all paired seed/rate
	runs, but admitted edge sets and final graphs do not differ. The fixture is
	synthetic; prediction loss is topology-dependent internal activation error;
	resource efficiency and general temporal-learning efficacy remain
	unestablished.
- Validation: focused corrective tests, Luna-12H and relevant topology/
	structural/predictive tests, full CPU regression, compilation and
	`git diff --check` pass. Existing optional CUDA skips are not Luna-12N
	failures.
- Open: the fixture is small and synthetic; no external prediction target,
	calibrated energy, hardware equivalence or general task benefit is shown.
- Decision: **PASS WITH FOLLOW-UP — MEASUREMENT CORRECTED, EFFICACY STILL
	UNESTABLISHED**. Stage 0 / Luna-13A remains deferred. The next authorized
	action is Luna-0 review of this record; no successor implementation is
	authorized.

## Luna-13B contract creation - 2026-09-29

Created the CPU-only **Causal Local Temporal Structural Crossover** contract
after the independently reviewed Stage-0 closure at
`ecb3f412b55d6978c5551798900cb1bacf76a238`.

- The controlled question is whether actual causally observed local temporal
	evidence crosses a frozen, analytically predicted decay-dependent scoring
	boundary and changes the admitted edge when exactly one structural slot is
	available to competing candidates.
- The contract separates score, rank, admitted-edge and final-graph outcomes;
	requires provenance, one-slot pressure, matched opportunity, mirrored and
	relabeled fixtures, negative controls, deterministic ties/replay and bounded
	execution status.
- Stage-0 remains closed with `127 passed` in the review slice and `242 passed,
	1 skipped` in the full CPU suite. The Luna-12J replay termination-status item
	remains a non-gating follow-up. Luna-13B execution requires a later explicit
	assignment and independent Luna-0 review; Luna-13C remains unauthorized.

This is a workflow and experiment-scope change only. A01-A15 are unchanged and
no ACP is created.

## Luna-0 independent review of Luna-13B - 2026-09-29

Reviewed implementation and artifact revision
`816929fa097e049ce7d82a1f7c63fb9cc4e8bd3f` after synchronization with
`origin/main`; the review started from a clean tree with matching `HEAD` and
`origin/main`.

- Independent runtime attacks reproduced the frozen scoring crossover
	`0.07833747196936626` and the complete causal chain: local runtime evidence,
	opposite score/rank ordering, different one-slot admitted edges and
	different final edge sets.
- Capacity/admission is valid: both candidates were locally valid from zero
	edges, exactly one edge slot remained, and the loser was rejected with
	`edge_capacity`.
- Relabeling, mirroring, exact/near ties, deterministic replay, future-probe
	exclusion, extended-budget replay and required negative controls passed.
- Scoring decay and execution decay remain separately configurable; no claim
	of task efficacy, energy benefit, scalability, hardware equivalence or
	general superiority follows.
- Preservation validation passed: review slice `135 passed`; full CPU suite
	`250 passed, 1 skipped`; compileall, diagnostics and `git diff --check`
	passed. The Luna-12J manual replay termination-status issue remains a
	non-gating follow-up.

**Decision:** **PASS — LUNA-13B CAUSAL STRUCTURAL CROSSOVER INDEPENDENTLY
VERIFIED**. Luna-13C remains unauthorized. No A01-A15 clause changed and no
ACP or architecture promotion is created by this review.

## Luna-13C contract creation - 2026-09-29

Created the CPU-only **Useful Causal Effect of Learned Temporal Structure**
contract after the independent Luna-0 PASS of Luna-13B at review revision
`04f2088725c71eb20b808ae07dbd99a02d4cd459`, reviewing implementation revision
`816929fa097e049ce7d82a1f7c63fb9cc4e8bd3f`.

- Luna-13B's causal structural crossover is independently established:
	runtime-local evidence, analytic decay-sensitive score crossover,
	rank/admitted-edge/final-graph reversal, one-slot competition, controls,
	deterministic replay and bounded execution passed. Task usefulness,
	external prediction/classification benefit, resource efficiency, scalability
	and hardware equivalence remain unproven.
- Luna-13C tests whether the learned edge has a useful causal effect on a
	fixed external target independent of the evaluated topology. It requires
	frozen learned state, paired present/remove/exact-restore/sham/irrelevant-
	edge conditions, fixed topology, equal-budget random growth and a fixed
	useful-edge positive control.
- The target, metric, decision rule, practical threshold, interventions,
	inputs, seeds and budgets freeze before held-out evaluation. Graph
	fingerprints, internal trace and task outcome are separate evidence;
	budget exhaustion is not successful evidence; labels remain isolated; and
	proxy energy is secondary.
- Luna-13C is CPU-only and preserves A01-A15 without an ACP or architecture
	promotion. The lifecycle is contract creation, explicit 13C execution,
	independent Luna-0 review, then a separate successor decision. Luna-13D
	remains unauthorized.

This is a workflow and experiment-scope update only. No Luna-13C experiment
was executed, no architecture clause changed, and no ACP was created.

## Luna-0 independent review of Luna-13C - 2026-09-29

Reviewed implementation/artifact revision
`575c2407db21786b21d64cb57d640d2a1a940ac0` from a clean synchronized
`main` tree. The independent review reproduced the default external-task
matrix: learned edge `2/2`, targeted removal `1/2`, exact restoration `2/2`,
sham `2/2`, irrelevant removal `2/2`, fixed topology `1/2`, and seed-0 random
growth `1/2`. Target arrivals and the short-case failure identify the route
effect; all runs completed without budget exhaustion, and budget 30 replay was
unchanged.

The review found non-gating evidence limitations: the sham is a literal
same-graph no-op that bypasses intervention machinery; the fixed useful-edge
control is the exact learned edge rather than an independently specified
positive control; seed 1 random growth also selects the useful edge and scores
`2/2`; and the 13C label test does not mutate labels. The checkpoint
fingerprint is a metadata hash rather than a complete serialized computational
state. These limitations prevent the stronger independent-verification status
but do not negate the reproduced narrow route-level task effect in this
bounded fixture.

Independent focused validation passed `41` tests; the full CPU suite passed
`255` with `1` optional skip; compile, diagnostics and `git diff --check`
passed. No A01-A15 clause changed, no ACP was created, and no Luna-13D was
created or authorized.

**Decision:** **PASS WITH FOLLOW-UP — CAUSAL TASK EFFECT VERIFIED,
NON-GATING LIMITATIONS REMAIN**. The next authorization boundary is explicit
project-owner direction for any follow-up contract and a new Luna-0 review.

## Luna-13C corrective evidence pass - 2026-09-29

Revision `685cd721f7ca108278aa2e3044b53d46981e5bbd` closes the four evidence
limitations identified by the independent review: sham now uses the shared
topology-rebuild path without changing the graph; the useful positive control
is distinct from the learned edge; random growth uses independent seeded
`random.Random(seed).choice` selection; and evaluation-label mutation is
checked against structure and pre-output computation. The artifact records
positive control `2/2`, random seed 0 `2/2`, random seed 1 `1/2`, and all
conditions completed without budget exhaustion.

The corrective result remains `PASS WITH FOLLOW-UP — CAUSAL TASK EFFECT
ESTABLISHED, LIMITATIONS REMAIN`: one random seed reproduces the task effect,
so selection superiority and broader usefulness remain unproven. No A01-A15
clause changed and no Luna-13D was created or authorized.

## Luna-0 independent corrective re-review - 2026-09-29

Luna-0 independently reviewed synchronized revision
`09995add7643e63f61c45602922238e319965113`. The artifact source revision is
`685cd721f7ca108278aa2e3044b53d46981e5bbd`, with baseline
`ea60610b7ba637e05ee986ffde2864e529a08f2c` and clean generation state.

The sham traverses the same bounded topology-rebuild machinery as removal and
restoration and preserves graph/fingerprint and the `2/2` result. The learned
edge is `right -> target, 1.0`; the distinct positive control is the
hand-designed `right -> target, 0.5`, which also scores `2/2`. Genuine seeded
random replay yields `right -> target`, `2/2` for seed 0 and
`left -> target`, `1/2` for seed 1. Label mutation leaves structure,
candidate evidence, decisions, and pre-output traces unchanged. The causal
intervention remains `2/2 -> 1/2 -> 2/2`, with only the short case changing.

The targeted independent bundle passed `124` tests and the full CPU suite
passed `256` with `1` skip. Artifact regeneration was byte-identical;
compileall, diagnostics, and diff checks passed. The result is
`PASS WITH FOLLOW-UP — CAUSAL EFFECT VERIFIED, BOUNDED LIMITATIONS REMAIN`:
the checkpoint is not a serialized full computational-state clone, the
fixture has only two cases, and random growth can reproduce the outcome. No
A01-A15 clause changed and no Luna-13D was created or executed. Later Luna-13D
contract creation requires explicit project-owner authorization.

## Luna-13D contract creation - 2026-09-29

Created the CPU-only **Finite-Resource Utility, Retention, and Capacity-Pressure
Experiment** contract after the independent corrective Luna-13C review closed
at `df297c446856d07b2822702202bbb61e81cf38a4`. The reviewed corrective source
was `685cd721f7ca108278aa2e3044b53d46981e5bbd`, synchronized in tree
`09995add7643e63f61c45602922238e319965113`.

- Luna-13D tests whether externally useful temporal structure is retained or
	recoverable under finite capacity while stale, unused or low-value structure
	is pruned, rejected or left unadmitted under declared rules.
- It stages structural and runtime pressure, preserves the fixed external
	Luna-13C target, separates task utility from resource cost, requires useful
	and low-value edge populations, fixed/random controls, lifecycle/pruning
	evidence, real seed provenance and bounded completion accounting.
- Atomic replacement is conditional: only an already documented and tested
	authorized mechanism may be measured. Otherwise the experiment is limited
	to admission, coexistence, pruning and later growth after freed capacity;
	no protected-edge lifetime or replacement mechanism is invented.
- Execution is CPU-only. Results require a Luna-13D handoff and independent
	Luna-0 review. Luna-13E is not authorized.

This is a workflow and experiment-scope update only. A01-A15 are unchanged;
no ACP or architecture promotion is created by this entry.

## Luna-0 independent review of Luna-13D - 2026-09-29

Reviewed implementation revision
`f11a44f24fa9ad84e111435ed0ae8390b41c49a6` from synchronized clean `main`
with `HEAD == origin/main` at review start.
The Luna-0 review publication revision is `8449562`.

- Independently confirmed the useful `right -> target, 1.0` edge, fixed task
	result, capacity 4/5/6 rejection semantics, two genuinely freed slots,
	normal post-pruning relay admission, random seeds, budget stability, Luna-
	13C/13B preservation and byte-identical artifact regeneration.
- Baseline and immediate post-pruning both remain `2/2`, 8 events and proxy
	energy `8.0`. Post-growth becomes `1/2`, 16 events and proxy energy `16.0`
	because duplicate direct/relay arrivals alter the fixed decision. No
	resource-efficiency claim is accepted.
- Pruning/retention evidence is invalid: the runner uses an endpoint-keyed
	literal score map, configured utility/inactivity thresholds are inert, and
	the fixed node tuple prevents identity-independent relabeling. The edge
	removals and capacity release are observed topology facts, not evidence of
	local utility-derived pruning.
- Final status: `BLOCKED — PRUNING/RETENTION EVIDENCE INVALID`.

The implementation revision is not promoted or reverted by this review. A
separately reviewed evidence-derived pruning correction may be eligible later;
Luna-13E is not created or authorized. No A01-A15 clause changed and no ACP
was created.

## Luna-13D corrective pass - 2026-09-29

The corrective pass started from Luna-0 review publication state
`89de90b183cd54f1ae24f433b6161f1b14c23c0e` and produced implementation
revision `9ae2fb6`.

- The endpoint-keyed pruning score map was removed. Bounded runtime evidence
	now includes use count, last use, inactivity age, observed utility, cost and
	pruning score.
- Frozen semantics are `inactivity_age >= inactivity_threshold OR
	observed_utility < utility_threshold`; inactivity equality is eligible and
	utility equality is retained. Threshold sweeps are recorded, and relabeled
	and mirrored fixtures follow evidence roles rather than endpoint names.
- The useful edge is retained from four observed uses while two zero-use stale
	edges are pruned, releasing two actual slots. Later relay growth remains
	ordinary bounded admission without replacement.
- The fixed task remains `2/2` after pruning and falls to `1/2` after relay
	growth at 16 events versus 8 baseline events. Resource efficiency and useful
	adaptation are not established.
- Corrective validation passed `10` focused tests, `100` preservation tests,
	and `266` full CPU tests with `1` optional skip; compile, diagnostics and
	diff checks passed.

Final corrective status:
`PASS WITH FOLLOW-UP — RETENTION/PRUNING ESTABLISHED, USEFUL ADAPTATION NOT
ESTABLISHED`. The corrected handoff returns to Luna-0 for independent review.
Luna-13E is not created or authorized. No A01-A15 clause changed and no ACP
was created.

## Luna-0 independent review of corrected Luna-13D - 2026-09-29

Reviewed corrected implementation
`9ae2fb6574a4a45fa6a47c18e9aa7270bd4d3080` from synchronized published tree
`206a3b8463ef857db5e5d5b8d2679d7e877f3bab`; the worktree was clean and
`HEAD == origin/main`.

- The prior pruning blockers are closed for the tested fixture. Runtime route
	use count, last-use timestamp, inactivity age, observed utility and cost now
	drive bounded pruning evidence; endpoint identity is not a primary decision
	input.
- The frozen rule is `inactivity_age >= threshold OR observed_utility <
	threshold`, with inclusive inactivity equality and strict utility inequality.
	Four OR combinations, threshold boundaries, arbitrary relabeling and
	mirrored task-source roles independently pass.
- The useful edge is retained from four observed uses; two zero-use stale edges
	are pruned and two actual topology slots are released. Later relay growth is
	ordinary bounded admission without replacement.
- Baseline/post-pruning remain `2/2`, 8 events, energy `8.0`; post-growth is
	`1/2`, 16 events, energy `16.0`. Resource efficiency and useful adaptation
	remain unestablished.
- Corrected validation: focused `10` passed, preservation `100` passed, full
	CPU `266` passed with `1` skip, compile/diagnostics/diff passed, and artifact
	regeneration is byte-identical.

Final review status:
`PASS WITH FOLLOW-UP — RETENTION/PRUNING VERIFIED, USEFUL ADAPTATION NOT
ESTABLISHED`. Luna-13E is not created or authorized. No A01-A15 clause or ACP
status changed.

The final Luna-0 review publication revision is
`becf38952fe5c1cf738dd875246b672f82836093`.

## Luna-13E contract creation - 2026-09-30

Created the formal **Post-Pruning Admission Quality and Harmful-Growth
Discrimination Experiment** contract after the independently reviewed
corrected Luna-13D state. The final reviewed published repository state is
`b7e3bdc6028381a5fa6912c0212aff79528beae1`; the corrected implementation
revision was `9ae2fb6574a4a45fa6a47c18e9aa7270bd4d3080`.

- Luna-13D status is `PASS WITH FOLLOW-UP — RETENTION/PRUNING VERIFIED,
	USEFUL ADAPTATION NOT ESTABLISHED`.
- Evidence-based retention/pruning and capacity release are established;
	useful post-pruning adaptation and resource efficiency are not established.
- Luna-13E tests whether existing local causal pre-admission evidence can
	distinguish beneficial from harmful growth under exactly one competing free
	slot, after reproducing the harmful Luna-13D post-growth result.
- Beneficial/harmful ground truth is external evaluation only. Field-level
	provenance, no-oracle/future-information enforcement, endpoint-independent
	scoring, label isolation, fixed/no-growth and seeded random controls are
	mandatory.
- If reliable admission requires unauthorized utility-aware state or another
	architecture change, execution must stop with a decision packet; no
	production mechanism may be added by stealth.
- The scope is CPU-only, with optional non-gating CUDA checks, and requires
	Luna-0 independent review afterward. Luna-13F remains unauthorized.

This is a workflow and experiment-scope update only. A01-A15 are unchanged,
no ACP is created, and no Luna-13E execution is authorized by this entry.

## Luna-13F creation - 2026-09-30

Created the formal **Runtime-Generated Local Candidate Evidence Experiment**
contract after the independent Luna-13E review returned **PASS WITH FOLLOW-UP
- HARMFUL GROWTH AVOIDED, GENERALITY NOT ESTABLISHED**.

- Synchronized reviewed state: `8c41267e47bc0543ff9f05e994dc7ea086b23e36`.
- Luna-13E review package: `7faf8d3f1c82927304875bb6263219d5954a463d`;
	corrected implementation reviewed there:
	`0a53b01b398d461eac3a962431b9ffcdae459e55`.
- Fixture-controlled evidence established only harmful-growth avoidance:
	no-growth `2/2 @ 8`, G `2/2 @ 12`, and H `1/2 @ 12`; G and H used proxy
	energy `12.0`, while no-growth used `8.0`.
- Luna-13F is CPU-only and tests runtime-generated bounded local candidate
	evidence under true one-slot competition using the unchanged canonical
	scorer first. Fixture-keyed evidence, oracle/endpoint roles, future
	outcomes and labels are prohibited.
- If current authorized mechanisms cannot generate the evidence, execution
	stops for an architecture-change decision packet; no learning subsystem may
	be added silently. Luna-13F returns to Luna-0 for independent review.
- Lifecycle: Luna-0 creates 13F -> 13F executes -> Luna-0 independently
	reviews 13F -> only then determine Luna-13G eligibility. Luna-13G is not
	authorized by this entry.

This is a workflow and experiment-scope update only. A01-A15 are unchanged;
no ACP is created.

## Luna-13E independent review - 2026-09-30

Luna-0 independently reviewed the synchronized Luna-13E implementation at
`0a53b01b398d461eac3a962431b9ffcdae459e55`; the final review package revision
is `7faf8d3f1c82927304875bb6263219d5954a463d`. Status:

**PASS WITH FOLLOW-UP — HARMFUL GROWTH AVOIDED, GENERALITY NOT ESTABLISHED**

- G/H legality and exactly one relevant free slot were independently verified.
- The canonical current policy selected G from pre-admission scores `3.0`
	versus `0.0`; presentation-order, relabel, mirror and future/label controls
	did not change the evidence-following result. Equalized evidence was
	explicitly classified as deterministic tie-breaking.
- The fixed external matrix was independently reconstructed as no-growth
	`2/2` (8 events, energy 8.0), G `2/2` (12 events, energy 12.0), and H
	`1/2` (12 events, energy 12.0). This supports avoiding harmful growth while
	preserving utility, not improving utility over no-growth or reducing cost.
- Reward, prediction/error and predicted total-cost evidence were unavailable;
	the controlled temporal observations were bounded fixture evidence. No
	general utility or resource-efficiency claim is promoted.
- The review corrected stale H frozen-ground-truth metadata from `0/2` to
	`1/2`. A01-A15 and ACP status remain unchanged. Luna-13F is not created,
	executed or authorized.

## Luna-13F execution authorization - 2026-09-30

Luna-0 authorized execution of the committed CPU-only **Runtime-Generated
Local Candidate Evidence Experiment** from clean synchronized revision
`4f4129f3d9eda736fe1c2434b79e21d387e2fedc` (`HEAD == origin/main`). The
prerequisite chain is sufficiently closed: Luna-13B crossover, Luna-13C
bounded causal task effect, corrected Luna-13D evidence-based pruning, and
the Luna-13E bounded harmful-growth-avoidance review are recorded. Luna-13F
targets Luna-13E's remaining fixture-evidence limitation.

- Status: `AUTHORIZED — LUNA-13F EXECUTION PENDING`.
- Runtime-generated bounded local evidence and the unchanged canonical scorer
	are the authorized scientific question under true one-slot competition.
- Fixture-keyed candidate evidence, labels, future outcomes, endpoint-role
	tables and experiment-side score injection remain prohibited.
- The architecture-change stop condition remains mandatory; no new utility
	memory, probation, rollback, reward channel, oracle, unbounded history or
	abstention may be added silently.
- CPU-only execution is valid; optional CUDA is non-gating. Luna-13F must
	return to Luna-0 for independent review, and Luna-13G remains unauthorized.

This is an experiment authorization boundary only. A01-A15, ACP status and
the canonical architecture are unchanged.

## Luna-13F independent review - 2026-09-30

Luna-0 reviewed the completed Luna-13F implementation revision
`0ba668ebe6cccd52fb0953638e1159090a79221e` after refreshing `origin/main`.
The review confirms:

- Terminal status: **BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION
	CONFIRMED**.
- The earliest invalid dependency is the fixture schedule assigning the
	beneficial role three short observations and the harmful role one long
	observation. Runtime neuron/policy state and the unchanged canonical scorer
	exist, but the informative evidence is role-authored before runtime.
- Post-decision mutation changes evidence and admission; held-out timestamps
	begin before the structural decision; and incomplete-budget execution still
	admits with pending events.
- The architecture is partially sufficient. No A01-A15 clause changed, no
	ACP is required, and the missing work is a corrective experiment/validation
	repair rather than a new architecture mechanism.
- The required preservation matrix passed 123 tests; the full CPU suite passed
	284 with 1 skipped; the contract audit reproduced 5 passed, 8 failed and 5
	not run. Editor diagnostics and hardware checks were not run and are outside
	the CPU-only gate.
- The original artifact pair has no terminal-status field; the verified pair
	and audit report the blocked status. This is recorded as an artifact
	truthfulness defect, not a positive result.

**LUNA-13F CORRECTIVE PASS ELIGIBLE UNDER EXISTING CONTRACT.** This is not an
execution authorization. A separately bounded corrective 13F assignment and
another Luna-0 review are required. Luna-13G remains unauthorized. A01-A15
and ACP status remain unchanged.

## Luna-13F corrective execution authorization - 2026-09-30

Following the independent Luna-0 review, corrective Luna-13F execution is
explicitly authorized under the existing `.github/agents/luna-13f.agent.md`
contract. No new Luna contract, ACP or architecture promotion is created.

The bounded corrective scope covers only removal of role/oracle knowledge from
the evidence schedule, explicit pre-admission evidence freeze, actual held-out
chronology, incomplete-budget admission rejection, genuine runtime evidence
equalization and the required invalid/not-run controls. It may not add utility
memory, probation, rollback, speculative edges, a new reward channel, global
task utility, an oracle cost predictor, global candidate history, protected
candidate classes or new architecture semantics.

If existing mechanisms prove insufficient, Luna-13F must stop with
`BLOCKED - ARCHITECTURE CHANGE REQUIRED FOR RUNTIME EVIDENCE`. The first 13F
execution remains blocked; ties and negative results remain valid; another
independent Luna-0 review is mandatory after corrective execution. Luna-13G
remains unauthorized.

## Luna-0 independent review of corrected Luna-13F - 2026-09-30

Reviewed synchronized corrected revision
`dcee582fa8fb347f578793c2ef383bd936e83234` with `HEAD == origin/main`.

- Final status: **BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION**.
- `_schedule()` no longer reads the utility-role fields, but
	`_candidate_edges()`, `_base_edges()` and held-out topology construction
	still map G through `beneficial_role` and H through `harmful_role`. The
	short-association motif is therefore assigned to the known useful endpoint.
- The observed 4.0/0.0 values are bounded source-local association counts
	from `TemporalAssociationPolicy`: four within-window relay associations and
	zero within-window noise associations. This is not independent utility
	prediction or autonomous training experience.
- A true A/B permutation/blinding attack and a valid mirrored-role control
	were not run. The five audit not-run items are all required but missing:
	external-label mutation, locality attack, neutral-decay sweep,
	candidate-saturation/reset/eviction, and valid mirrored roles.
- Reported utility remains G `2/2`, H `1/2`, no-growth `2/2`; this supports
	only harmful-growth avoidance. No-growth is 8 events/8.0 proxy units and G
	is 12 events/12.0 proxy units, so resource benefit is not established.
- Artifact provenance is inconsistent: the artifact records executed revision
	`3379403a8b58649a85c2604ba3044e55e4fe99e9` rather than the corrected commit
	reviewed. Held-out chronology is not independently established because its
	timestamps are hard-coded while route traces reset at 0.0.

No A01-A15 clause changed and no ACP is required. The existing bounded runtime
may support a later corrected experiment, but only after explicit
project-owner authorization and another Luna-0 review. Luna-13G remains
unauthorized.

## Luna-13F blinded-mapping corrective authorization - 2026-09-30

Luna-0 authorizes one additional corrective Luna-13F pass under the existing
`.github/agents/luna-13f.agent.md` contract from synchronized revision
`dcee582fa8fb347f578793c2ef383bd936e83234`.

- Final authorization status: **PASS — LUNA-13F BLINDED-MAPPING CORRECTIVE
	PASS AUTHORIZED**.
- This is not a new Luna-13F contract, does not execute the experiment, does
	not change A01-A15, and does not authorize Luna-13G.
- The valid partial result is preserved: bounded runtime association evidence
	exists and reaches the unchanged canonical scorer. The remaining blocker is
	`beneficial_role -> candidate/topology assignment -> G`.
- The corrective pass must use neutral candidate identities, remove utility
	roles from all pre-evaluation construction and scoring paths, freeze a
	predeclared seeded mapping, run at least two endpoint/motif permutations,
	and classify utility only after admission and held-out evaluation.
- It must identify the actual cause of 4.0/0.0 and execute or contractually
	justify all five outstanding controls: `external_label_mutation`,
	`locality_attack`, `neutral_decay_runtime_sweep`,
	`candidate_saturation_reset_eviction` and `valid_mirrored_roles`.
- The completed pass must regenerate artifacts, run required validation and
	return to Luna-0. No architecture change is currently required; a need for
	new runtime semantics is an explicit stop condition.

The independent Luna-0 review remains mandatory after corrective execution.
Luna-13G remains unauthorized.

## Luna-0 independent review of blinded-mapping corrective Luna-13F - 2026-09-30

The independent review reproduced the raw blinded experiment but did not close
Luna-13F. P0 maps `candidate_A` to `relay`, selects it from runtime evidence
`4.0` versus `0.0`, and obtains `2/2`; P1 maps the same neutral candidate to
`noise`, selects it again, and obtains `1/2`. The no-growth reference remains
`2/2` with 8 events and `8.0` uncalibrated activity-cost-proxy units; the
selected P0 growth case uses 12 events and `12.0` units.

The source-local bounded association count and unchanged canonical scorer are
independently reproducible, and the decay sweep confirms the score is count-
based rather than decay-sensitive. However, the required controls are not all
validly executed: external-label mutation and locality are declarative fields,
future events are removed before runtime execution, held-out timestamps are
hard-coded over a reset evaluator, no complete contract-audit artifact exists,
and saturation/reset does not exercise eviction or the full budget boundary
matrix.

Final status: **BLOCKED - REQUIRED CONTRACT CONTROLS NOT EXECUTED**. The raw
negative result remains an experiment observation, not an independently
verified Luna-13F closure. No A01-A15 clause changed, no ACP was created, no
architecture change was authorized, and Luna-13G remains unauthorized.

## Luna-13F contract-control completion authorization - 2026-09-30

Luna-0 published the independent review at
`c05015527063053ee789d0fc19ae21a02627f319` with status **BLOCKED - REQUIRED
CONTRACT CONTROLS NOT EXECUTED**. The review independently reproduced the
blinded negative result: P0 selected `candidate_A` with held-out `2/2`, and
P1 selected `candidate_A` with held-out `1/2`.

One narrowly scoped Luna-13F contract-control completion pass is authorized
under the existing `.github/agents/luna-13f.agent.md` contract. The scope is
limited to chronology and queue-boundary proof, external-label mutation,
locality attacks and provenance, bounded candidate saturation/reset/expiry/
eviction-or-rejection semantics with stale-state reuse, budget-boundary and
larger-budget stability, complete requirement-level audit accounting, and
truthful artifact regeneration. Required preservation suites and static,
diagnostic and diff checks remain part of execution. The P0/P1 mapping,
runtime evidence semantics and canonical scorer are preserved; any genuine
contract defect that changes the scientific result requires rerunning both
mappings and disclosing the prior result.

This is a workflow authorization only. No A01-A15 clause changed, no ACP is
required, Luna-13F was not executed by this publication, and Luna-13G remains
unauthorized. Final Luna-0 closure review is required after execution.

## Luna-13F final independent closure review - 2026-09-30

Luna-0 independently reproduced the blinded negative observation from
implementation revision `72b6201d6a2793b0bab099df7418aa66904501a` and artifact
generation revision `b5815f90522c1704731037c5d5fd1bface264565` at synchronized
review revision `2b2432dabd49ecacceef525e8e3e68b909ee09c3`.

- P0: `candidate_A` selected, held-out `2/2`.
- P1: `candidate_A` selected, held-out `1/2`.
- Proposition 1 (bounded local runtime evidence): observed in the tested
	fixture; Proposition 2 (canonical admission affected): observed in the
	tested fixture; Proposition 3 (evidence predicts useful growth): not
	supported.
- The evidence mechanism is primarily source-local observation-count/
	association-window accumulation, not a decay-sensitive score.
- The raw result retains no-growth `2/2 @ 8 events / 8.0 proxy` versus selected
	P0 growth `2/2 @ 12 events / 12.0 proxy`; there is no task or resource
	improvement claim, and P1 demonstrates harmful growth remains possible.

The final review does not close Luna-13F because the future-event, chronology
and locality controls reported as PASS are not independently executed in the
implementation. The generated audit is consequently **BLOCKED - CONTRACT
AUDIT INVALID** despite its `26/0/2` aggregate. `candidate_expiry` and
`candidate_eviction` are both **VALID NOT APPLICABLE**: the canonical policy
has no expiry path and uses explicit rejection rather than eviction at full
capacity. A01-A15 and ACP status are unchanged. No successor or architecture
mechanism is authorized; Luna-13G remains unauthorized.

## Luna-13F runtime-attack corrective authorization - 2026-09-30

After the final independent review remained **BLOCKED - CONTRACT AUDIT
INVALID**, Luna-0 authorizes one narrowly scoped corrective pass under the
existing Luna-13F contract. This is an authorization and workflow update only;
Luna-13F is not executed here.

The authorized work repairs exactly three controls:

- future-event exclusion through a causally continuous post-admission runtime
	continuation that processes a score-changing future observation while
	preserving the immutable historical admission record;
- chronology through actual queued before-decision, equal-timestamp and
	strictly-after-decision held-out injections with recorded processing order;
- locality through mutation of genuinely accessible prohibited runtime state,
	including a cross-candidate private-state attack where available.

The P0/P1 fixture and scientific interpretation remain protected: P0
`candidate_A -> 2/2`, P1 `candidate_A -> 1/2`, with bounded source-local
temporal association counts rather than decay-sensitive scoring. The two valid
N/A classifications remain unchanged. No A01-A15 change, ACP, new runtime
semantics, utility memory, reward path, probation, rollback, speculative edge,
global utility state or new candidate-state behavior is authorized. If a real
architecture change is required, execution must stop and return
**BLOCKED - ARCHITECTURE CHANGE REQUIRED**. Luna-13G remains unauthorized.

## Luna-13F closure - 2026-09-30

Luna-0 independently reviewed and closed Luna-13F at review publication
revision `e595a9f`, from implementation and artifact revision
`83266f92d750939ef0b9904073e9f75badc35fbb`.

- P0 selects `candidate_A` for held-out `2/2`; P1 selects `candidate_A` for
	held-out `1/2`.
- The evidence mechanism is bounded source-local temporal-association counts,
	not decay-sensitive structural utility prediction. The unchanged canonical
	scorer admits one candidate from a genuine one-slot competition.
- The future continuation was processed through the same runtime and changed
	live losing-candidate evidence `0.0 -> 5.0` without changing the frozen
	historical decision. Actual queued before/equal chronology attacks were
	invalidated and the strictly-after attack was valid. The real cross-candidate
	locality mutation left candidate-A evidence unchanged.
- Bounded lifecycle, reset/stale reuse, budget boundary, label isolation,
	mirroring, equalization, no-evidence and deterministic replay were verified.
	Expiry and eviction are valid N/A cases: expiry is unsupported by policy and
	full capacity deterministically rejects rather than evicts.
- The complete audit is `26 PASS / 0 FAIL / 2 valid N/A`. Focused validation is
	`15 passed`; preservation is `72 passed`; full CPU validation is `291 passed,
	1 skipped`.
- No-growth remains `2/2` at 8 events and proxy `8.0`; selected P0 growth is
	also `2/2` at 12 events and proxy `12.0`. No task or resource improvement is
	established, and P1 demonstrates that higher evidence can select harmful
	growth.

Proposition 1 (bounded runtime evidence) and Proposition 2 (canonical
admission effect) are **SUPPORTED IN TESTED FIXTURE**. Proposition 3 (greater
evidence predicts held-out useful growth) is **NOT SUPPORTED**. The final
status is **NEGATIVE RESULT - LUNA-13F RUNTIME EVIDENCE DOES NOT PREDICT
USEFUL GROWTH, INDEPENDENTLY VERIFIED AND CLOSED**.

**NO A01-A15 CHANGE REQUIRED. NO ACP REQUIRED. LUNA-13F CLOSED - SUCCESSOR
NOT AUTHORIZED.** Luna-13G remains unauthorized. The final closure handoff is
`workflow/handoffs/luna-0-final-closure-review-Luna-13F-closed.md`.

## ACP-0002 creation - 2026-09-30

Created **Independent Edge Signal Transformation and Neuron Gain Separation**
from the project-owner architecture request at synchronized revision
`25aa7697d523c13f0fdcf56c84170ceb553cc229`.

- ACP-0002 was initially recorded as **Under review**. It proposed bounded
	signed edge efficacy, independent divider strength and logical reference, a
	fixed edge `tanh` transfer, and explicit separation of edge state from
	destination-neuron gain.
- The initial subtraction candidate
	`e_ij = d_ij * (tanh(w_ij * a_i) - r_ij)` was later rejected in the focused
	mathematical review because `d=0` erased the independent reference. The
	destination retains event-driven elapsed-time decay, clipping and fixed
	neuron `tanh` activation.
- A01-A15 remain unchanged. This is a material canonical signal-path and
	ownership proposal, so an ACP is required even though no implementation is
	authorized. The contract remains version 1.1.
- The closed Luna-13F negative result is preserved unchanged. Luna-13G remains
	unauthorized. No production code, edge learning, temporary maturation or
	local time-series predictor is authorized by this entry.
- At creation, implementation was blocked pending acceptance and the staged
	analytic/regression evidence specified in ACP-0002; the later acceptance and
	N1-only authorization are recorded below.

The proposal and Luna-0 handoff are
`workflow/docs/architecture_proposals/ACP-0002.md` and
`workflow/handoffs/luna-0-architecture-review-ACP-0002.md`.

## ACP-0002 mathematical review and staged acceptance - 2026-09-30

Luna-0 performed the requested focused mathematical review before changing
ACP-0002 status. The original subtraction form
`d * (tanh(w * a) - r)` was rejected for the project-owner's independently
buffered per-edge reference intent because `d=0` forces the output to zero for
every `r`.

- The selected canonical equation is Model B:
	`v_ij = d_ij * tanh(w_ij * a_i) + (1 - d_ij) * r_ij`.
- `w` remains signed bounded efficacy, `d` remains signal/reference divider
	weight, and `r` remains an independent bounded edge reference. `w` and `d`
	are not redundant: `w` changes nonlinear signed efficacy and saturation,
	while `d` interpolates between the transformed signal and reference.
- The delivered value is the absolute normalized edge signal `v_ij`; no
	destination-neuron reference is added. `v` is bounded in `[-1,1]` and the
	existing destination state clip bounds recurrence.
- The analytic grid, endpoint checks, positive/negative source checks and
	boundedness review passed. No production code or runtime semantics changed.
- ACP-0002 is now **Accepted for staged implementation**. Only **N1 -
	edge/neuron data model and compatibility representation** is authorized.
	N2 transfer execution, edge learning, temporary/probationary maturation,
	local time-series predictors and Luna-13G remain unauthorized.

A01-A15 and contract version 1.1 remain unchanged. Luna-13F remains closed
with its negative result; Luna-13G remains unauthorized.

## Luna-15 ACP-0002 Stage N1 contract creation and authorization - 2026-09-30

Starting from revision `a24773eac26151c02b953158df9eb19766184c60`, Luna-0
created and authorized `.github/agents/luna-15.agent.md`, **Luna-15 -
ACP-0002 Edge/Neuron Data Model and Compatibility**.

- ACP-0002 remains **Accepted for staged implementation**.
- The only authorized scope is **N1 - edge/neuron data model and compatibility
	representation**.
- N1 must represent edge-owned `edge_weight/w_ij` in `[-2,2]`,
	`divider_strength/d_ij` in `[0,1]`, `reference/r_ij` in `[-1,1]`, the
	existing positive finite propagation delay, and neuron-owned
	`neuron_gain/g_j` in `[0,2]`.
- N1 must preserve legacy constructors, structural-plasticity interfaces,
	deterministic representation/replay, observer/instrumentation behavior and
	routed payload semantics, with analytic and regression tests proving those
	compatibility requirements.
- The accepted future Model-B equation remains deferred. N1 must not activate
	transfer execution or change routed payload semantics.
- N2 propagation, adaptive edge learning, temporary/probationary connections,
	maturation, local time-series mini-NNs, new utility-learning mechanisms,
	hardware work and all A01-A15 changes are prohibited.
- N1 completion does not authorize N2. Luna-15 must return to Luna-0 for
	independent review.

Luna-13F remains **CLOSED**, Luna-13G remains unauthorized, and A01-A15 and
contract version 1.1 remain unchanged. The creation handoff is
`workflow/handoffs/luna-15-n1-contract-creation-Luna-0.md`.
# Luna-0 ACP-0004 attractor excursion architecture draft - 2026-10-02

Created the next repository-valid proposal, **ACP-0004 — Attractor Excursion
and Event-Compression Neuron**, from the expected baseline revision
`c1c7a4948b7e96908da8d2334687d238d6949379`.

The draft separates the backend-neutral canonical **excursion** from its
realizations: software/ GPU TPCN events, FPGA digital event/pulse records and
FPAA analog spikes or excursions. It proposes a bounded leaky accumulator with
single-excursion and explicitly entered multi-excursion returns, signed
behavior, deterministic logical emission timing, bounded causal provenance,
compression metrics and mandatory finite-return fixtures.

A01-A15, ACP-0002 N2, ACP-0003 H1 closure, ACP-0003 H2 unauthorized status,
ACP-0002 N3 unauthorized status, Luna-17 reservation, Luna-13F closure and
Luna-13G unauthorized status are unchanged. No production neuron, learning
rule, backend, edge learning or Luna-19 contract was created. ACP-0004 remains
Draft pending project-owner decision.

Evidence: `workflow/docs/architecture_proposals/ACP-0004.md` and
`workflow/handoffs/luna-0-architecture-update-ACP-0004.md`.
# Luna-0 independent review of ACP-0004 - 2026-10-02

Reviewed committed proposal `c18757739f4055bbb5721520a14382701e177d64`.
**ACP-0004 remains Draft and is not accepted for staged implementation.**

The proposal's backend-neutral excursion direction is compatible with A01-A15,
but implementation authorization is blocked by unresolved canonical decisions:
exact one-excursion/one-digital-event cardinality, persistent versus
bookkeeping state ownership, S re-arm and M entry rules, fixed amplitude map,
no-crossing discharge and finite-return proof, explicit autonomous internal
event timing, polarity point, bounded provenance overflow, post-migration
Model-B `a_i` meaning, and a required versioned `TPCN-IR-2` decision.

ACP-0003 future-neuron terminology now uses canonical excursion and explicitly
maps GPU/software and FPGA digital events separately from FPAA physical
spikes/analog excursions. This is terminology clarification only; ACP-0003 H2,
ACP-0002 N3, all backends, edge learning, Luna-13G and Luna-19 remain
unauthorized.

Evidence: `workflow/docs/architecture_proposals/ACP-0004.md` and
`workflow/handoffs/luna-0-independent-review-ACP-0004.md`.
