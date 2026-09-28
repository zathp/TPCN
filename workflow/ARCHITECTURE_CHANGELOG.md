# Architecture Changelog

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

For later changes record date, contract version, accepted ACP, decision owner, clauses affected, evidence, compatibility and migration/rollback implications.

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

