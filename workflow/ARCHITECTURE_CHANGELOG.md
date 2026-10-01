# Architecture Changelog

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

Implementation revision: `9cf9feed2a7436b321d2c9d7a960e8e393fd21c7`.
The N2 baseline is `artifacts/acp-0002-n2-model-b-baseline/baseline.json`.
Focused N2 tests: 264 passed. Full CPU suite: 546 passed, 1 skipped.
Compilation and `git diff --check` passed. Causality, timestamps, positive
delays, deterministic ordering, bounded queue/state/execution, structural
defaults and reconstruction, label/future isolation, reward boundaries and
observer behavior remain invariant; numeric payload/state traces are expected
to change at the N2 boundary.

TPCV-1 remains valid only as its limited downstream observational format and
does not claim active transfer-state equivalence. No A01-A15 text changed.
Luna-13F remains closed; Luna-13G and N3/later ACP-0002 stages remain
unauthorized.

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

