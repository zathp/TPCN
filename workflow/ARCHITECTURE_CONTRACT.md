# TPCN Architecture Contract

All Luna agents must preserve these constraints unless working on an explicitly designated experimental architecture branch.

## Contract clauses

A01–A11, A14 and A15 define core requirements or supported capabilities. A12 and A13 explicitly preserve experimental freedom; they do not require ten pathways or explicit gates.

### A01 — Event-driven computation

TPCN has no required global neural clock.

Neurons execute because events arrive or because a locally scheduled event becomes due.

Hardware clocks may exist for implementation purposes but must not implicitly become the neural network clock.

### A02 — Local time and intrinsic temporal state

Neurons may maintain persistent local state, local timestamps and elapsed time.
Neuron computation may depend on the state before an event, the incoming event,
and elapsed local time. Conceptually, for a neuron whose last state update was
at local time \(t_0\),

\[
s(t_1^-)=\Phi(s(t_0^+),t_1-t_0)
\]

is applied before an event at \(t_1\), followed by

\[
s(t_1^+)=F(s(t_1^-),e_{t_1}).
\]

The implementation may evaluate \(\Phi\) analytically or when an event is
processed; it need not step through every intermediate time. A single event
must be capable of changing state that remains observable at a later event or
local observation before a declared character/sequence reset. The state,
decay/evolution rule and reset boundary must be explicit and bounded.

State evolution should support:

\[
\Delta t_i=t_{\text{event}}-t_i^{last}
\]

rather than assuming fixed simulation timesteps.

The canonical/reference neuron must expose at least one deterministic fixture
where event order changes the resulting state, output or trace. The contract
does not require every parameter choice to be order-sensitive, but permits
temporal noncommutativity such as

\[
F(F(s,e_1),e_2)\ne F(F(s,e_2),e_1).
\]

### A03 — Finite propagation

Information cannot move instantaneously through the network.

An event emitted at time \(t_e\) has an arrival time such as

\[
t_a=t_e+\tau_{ij}.
\]

Path delay is the cumulative causal delay over all edges in a path, not merely
its hop count. The topology must permit convergent paths with unequal delays,
so an older consequence on a long path can arrive alongside a newer
consequence on a short path. Fan-in processing preserves event timestamps and
the canonical deterministic ordering; events at different times must not be
collapsed into an unordered sum before neuron processing.

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

Outer or offline training orchestration may prepare reproducible initial
parameters, bounded topology fragments and other explicitly declared module
state. This is initialization, not a runtime exception to locality. Once
execution begins, trainer state and global statistics must not become hidden
neural inputs. Independently initialized reference configurations remain
legal.

### A08 — Bounded dynamics

Neuron state and recurrent dynamics must include mechanisms preventing
uncontrolled divergence. Recurrent topology and cycles are permitted only
within finite propagation, event-budget, lineage/path, queue and state bounds.
Monotonic local time and deterministic tie ordering remain required. A cycle
must never require an implicit global tick or enable infinite propagation.

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

Structural changes must respect hardware/topological constraints and explicit
finite admission, replacement and pruning policies.

Bounded fan-in, fan-out, edge and routing capacities are resource limits, not
objectives. An enabled structural-learning policy must retain a legal route to
useful convergent causal structure: it must not systematically consume
available capacity in a way that makes relevant multi-path fan-in impossible
before it can be evaluated. This does not require a particular graph shape or
fan-in at every node.

Growth, rejection, replacement and pruning outcomes must be observable. A
failed admission must not be counted as successful learning, and the policy
must record an explicit cause where applicable, including duplicate, source
fan-out full, destination fan-in full, global edge capacity, candidate
unavailable, locality restriction, utility rejection, replacement rejection or
another declared cause.

Causally/locality available temporal relationships between activity events may
be used as structural evidence. This permits experiments with directed
earlier-to-later associations and path shortening, but does not require a
matching interval, timing window, correlation formula, path-shortening
equation or fan-in heuristic. A new edge is a new finite-delay causal path; it
must not retroactively alter emitted events or create instantaneous
propagation. Structural learning remains subject to A01-A08, A07 locality,
resource bounds, reset/learning boundaries and A15 hardware realizability.

### A15 — Hardware independence

The architectural behavior must remain implementable by:

- software reference model,
- FPGA,
- FPAA,
- hybrid FPGA/FPAA systems.

Software conveniences that fundamentally prevent hardware implementation should not silently become architecture requirements.

---


## Authority and interpretation

Version: 1.1 — 2026-09-28. This is the authoritative contract for the candidate event-driven TPCN architecture. It governs new core work; it does not claim that the existing implementation already conforms.

Current project-owner decisions take precedence. This contract takes precedence over workflow examples, legacy documentation and experimental results. Accepted changes require an [Architecture Change Proposal](docs/architecture_proposals/ACP-TEMPLATE.md), a contract revision and a changelog entry. Experiments may depart from named clauses on isolated branches, but must identify the departure and cannot silently become the core.

A10 means **minimize unrewarded energy expenditure, not energy itself**. Reward attribution, utility formulas and tuning coefficients remain research choices. Evaluate both high-cost/high-reward retention and high-cost/low-reward suppression. An inactive network is not evidence of useful efficiency.

A14 requires constrained, locally informed structural adaptation as a supported direction; the first integration model may keep structural plasticity disabled. When enabled, its policy must leave useful convergent causal structure measurable and attainable under the finite resource budget, with explicit failed-admission accounting. Temporal association and path-shortening rules remain experimental. A15 is a portability requirement, not a claim of completed hardware validation.

Modular/offline bootstrap initialization is a supported training direction, not
a mandatory runtime feature or the only legal initialization path. A module
must declare its boundaries, event semantics, state, reset behavior, resource
requirements, time units, parameter bounds, hardware assumptions and training
provenance before composition. Initial state must be serializable/versionable
or reproducibly generated, and post-composition local learning and causal
behavior require separate evidence.

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

