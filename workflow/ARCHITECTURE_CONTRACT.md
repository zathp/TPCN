# TPCN Architecture Contract

All Luna agents must preserve these constraints unless working on an explicitly designated experimental architecture branch.

## Contract clauses

A01–A11, A14 and A15 define core requirements or supported capabilities. A12 and A13 explicitly preserve experimental freedom; they do not require ten pathways or explicit gates.

### A01 — Event-driven computation

TPCN has no required global neural clock.

Neurons execute because events arrive or because a locally scheduled event becomes due.

Hardware clocks may exist for implementation purposes but must not implicitly become the neural network clock.

### A02 — Local time

Neurons may maintain local timestamps and elapsed time.

State evolution should support:

\[
\Delta t_i=t_{\text{event}}-t_i^{last}
\]

rather than assuming fixed simulation timesteps.

### A03 — Finite propagation

Information cannot move instantaneously through the network.

An event emitted at time \(t_e\) has an arrival time such as

\[
t_a=t_e+\tau_{ij}.
\]

### A04 — Bounded topology

TPCN exists within a finite implementation space.

There are:

- finite neuron nodes,
- finite connectivity,
- bounded fan-in,
- bounded fan-out,
- finite routing resources.

Spatial coordinates may represent physical implementation topology but do not need to participate in neural computation.

### A05 — No spatial reservoir

The previous spatial reservoir is not part of the new TPCN core.

Do not reintroduce a spatial reservoir merely to implement locality.

Legacy reservoir implementations may remain for comparison under legacy or experimental code.

### A06 — Predictive coding remains fundamental

TPCN must not become merely an event-driven classifier.

Neurons/network components should form predictions.

When subsequent information arrives, prediction error should be explicitly represented:

\[
\epsilon=x-\hat{x}.
\]

Prediction-error information should itself be capable of local/event-driven propagation.

### A07 — Local learning

A neuron cannot obtain unrestricted global network state.

Learning mechanisms operating inside TPCN should use information causally/locality available to that component.

Global statistics are permitted for:

- evaluation,
- logging,
- visualization,
- offline analysis,
- outer training orchestration.

They must not silently become neural inputs.

### A08 — Bounded dynamics

Neuron state and recurrent dynamics must include mechanisms preventing uncontrolled divergence.

### A09 — Energy is local

Every computational unit may maintain a local estimate of computational/resource expenditure.

Abstract interface:

\[
E_i=\mathcal E_i(\text{local activity}).
\]

The exact implementation is hardware dependent.

### A10 — Energy is not simply minimized

TPCN should minimize **unproductive computation**, not computation itself.

Expensive computation may survive when its usefulness compensates for its cost.

Candidate utility models include:

\[
U=R-\lambda E
\]

and

\[
U=\frac{R}{E+\epsilon}.
\]

Neither formula is initially a permanent architecture requirement.

### A11 — Delayed credit is allowed

Useful computation may produce reward only after additional events propagate.

Eligibility/credit mechanisms must therefore support delayed reward.

### A12 — Multiple computational pathways are optional

The historical ten gated pathways are now a soft constraint.

A TPCN neuron may expose multiple operators/pathways, but:

\[
K_i \neq 10
\]

is allowed.

Exactly ten pathways remain an experimental/reference configuration.

### A13 — Explicit gating is optional

Event-driven activation may naturally produce computational gating.

Explicit learned pathway gates must therefore be tested rather than assumed necessary.

### A14 — Structural plasticity

Connections and eventually computational resources may change based on locally obtainable evidence.

Structural changes must respect hardware/topological constraints.

### A15 — Hardware independence

The architectural behavior must remain implementable by:

- software reference model,
- FPGA,
- FPAA,
- hybrid FPGA/FPAA systems.

Software conveniences that fundamentally prevent hardware implementation should not silently become architecture requirements.

---


## Authority and interpretation

Version: 1.0 — 2026-09-26. This is the authoritative contract for the candidate event-driven TPCN architecture. It governs new core work; it does not claim that the existing implementation already conforms.

Current project-owner decisions take precedence. This contract takes precedence over workflow examples, legacy documentation and experimental results. Accepted changes require an [Architecture Change Proposal](docs/architecture_proposals/ACP-TEMPLATE.md), a contract revision and a changelog entry. Experiments may depart from named clauses on isolated branches, but must identify the departure and cannot silently become the core.

A10 means **minimize unrewarded energy expenditure, not energy itself**. Reward attribution, utility formulas and tuning coefficients remain research choices. Evaluate both high-cost/high-reward retention and high-cost/low-reward suppression. An inactive network is not evidence of useful efficiency.

A14 requires constrained, locally informed structural adaptation as a supported direction; the first integration model may keep structural plasticity disabled. A15 is a portability requirement, not a claim of completed hardware validation.

## First integration target

Sequential letter-stroke classification is the first integration benchmark. Feed strokes or stroke points in temporal order, retain causal state, predict subsequent information and emit explicit error events. Completed static character images must not replace streaming input. Classification belongs outside the reusable core.

The initial candidate has 256 neurons, 26 A–Z outputs, fan-in/out limits of 8, energy and predictive-error accounting enabled, and explicit ten-pathway gating and structural plasticity disabled. These are starting experiment settings, not invariants. Confirm dataset classes before adopting 26 outputs.

## Do not reintroduce

- A mandatory global neural timestep, including one disguised as execution batching.
- A spatial reservoir dependency in core to implement locality.
- Unlimited node, connection, routing or state growth.
- Unrestricted global state or backpropagation replacing local core learning.
- Raw task labels or future stroke data as hidden core inputs.
- An energy-only objective that rewards inactivity.
- Exactly ten pathways or explicit learned gates as mandatory core behavior.

See [acceptance criteria](docs/architecture/ACCEPTANCE_CRITERIA.md) for evidence required before integration.

