# TPCN Luna Multi-Agent Workflow — Event-Driven Architecture

## Mission

Evolve TPCN into a hardware-realizable, event-driven predictive-coding network while preserving its core principles.

The immediate benchmark is sequential letter-stroke classification. Each stroke or stroke point is presented as subsequent temporal data rather than converting the complete character into a static image.

The workflow must support eventual:

- FPGA/VHDL implementation
- FPAA implementation
- FPGA/FPAA hybrid implementation
- bounded hardware resources
- local learning
- local energy/resource accounting
- structural plasticity
- asynchronous/event-driven computation

---

## Authoritative contract

Read [ARCHITECTURE_CONTRACT.md](../../ARCHITECTURE_CONTRACT.md) first. Its A01–A15 clauses govern this workflow. A12–A13 are soft/experimental, and example sizes and utility formulas are not invariants.

# 2. Branch Policy

Use:

```text
main

architecture/event-tpcn
    |
    +-- event-core
    +-- predictive-dynamics
    +-- bounded-topology
    +-- energy-utility
    +-- structural-plasticity
    +-- stroke-classifier

hardware/fpga
hardware/fpaa
hardware/hybrid

experiment/explicit-gates
experiment/event-only-gating
experiment/utility-gating
experiment/*

legacy/spatial-reservoir
```

`architecture/event-tpcn` is the integration branch for the candidate architecture.

Do not merge experimental architectural behavior into it without an Architecture Change Proposal.

---

# 3. Luna-0 — Architecture Guardian

## Responsibility

Luna-0 coordinates the other agents.

It should perform minimal implementation work.

Its primary job is preventing architectural drift.

## Responsibilities

Maintain:

```text
ARCHITECTURE_CONTRACT.md
ARCHITECTURE_CHANGELOG.md
docs/architecture/
docs/architecture_proposals/
```

Review changes for:

- accidental global clock assumptions,
- global-state leakage,
- spatial-reservoir reintroduction,
- unlimited connectivity,
- unrestricted backprop replacing local learning,
- energy minimization causing trivial inactivity,
- classifier-specific logic leaking into TPCN core,
- software structures impossible to reasonably map to FPGA/FPAA.

## Luna-0 rule

When implementation convenience conflicts with architecture, implementation must adapt unless an Architecture Change Proposal is accepted.

---

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

# 15. Luna-12 — FPGA/VHDL Branch

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

# 16. Luna-13 — FPAA Branch

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

# 17. Luna-14 — Hardware Equivalence

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

# 18. First Integration Model

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

# 19. Required Metrics

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

# 20. Agent Handoff Format

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

# 21. Architecture Change Proposal

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

# 22. Execution Order

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
     Visualization-1/2
     Contract + CPU viewer
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    Luna-9  Luna-10   Optimization
    Gating  Plasticity
       │       │
       └───┬───┘
           ▼
      Architecture
       evaluation
           │
      ┌────┴─────┐
      ▼          ▼
   Luna-12     Luna-13
    FPGA        FPAA
      \          /
       \        /
        ▼      ▼
         Luna-14
     HW Equivalence
```

---

## Visual Examination / Observability milestone family

This is an implementation observability and validation track, not an extension of the normative TPCN architecture. The snapshot contract is read-only and non-semantic: exporters observe existing state; neither snapshots nor viewers define neuron behavior, event timing/order, routing, learning, plasticity or topology formation. Viewer layouts and capture timestamps must not become neural features or a global neural timestep. No viewer command or exported aggregate may feed back into computation.

Instrumentation must preserve computational behavior with capture enabled or disabled. Report capture, transport and rendering overhead separately. Use bounded observation buffers and explicitly mark dropped/incomplete captures; a slow or disconnected viewer must not impose backpressure on neural execution. Any coherent capture mechanism must preserve existing event semantics and avoid torn state without adding a neural synchronization rule.

### Visualization-1 — Canonical versioned snapshot contract

Define an implementation-neutral observation schema and fixtures after event, neuron and topology interfaces stabilize, before deep optimization. Record schema version, run/configuration/seed identity, backend and source revision, snapshot sequence ID, simulation timestamp/epoch with declared units, and capture boundary/consistency metadata. An epoch is an observation identifier, not a neural tick.

Represent stable neuron IDs (including allocation generation if IDs are reused), existing state/type, directed structural connections and endpoints, relevant weights/strengths, and activity with a declared observation interval. Identify optional/unavailable fields explicitly. Define numeric encoding, units, ordering, version compatibility, completeness and validation rules. Specify a human-readable reference representation plus compact binary/hex serialization; these are observation formats, not execution-state or architecture requirements.

Acceptance: documented schema and valid/invalid fixtures round-trip without losing logical IDs, edges or represented values; unknown versions and incomplete captures are detected explicitly.

### Visualization-2 — CPU exporter and reference viewer

Export CPU reference state through Visualization-1 and build the first host viewer for neuron state, activity and bounded connectivity. Distinguish display coordinates from physical placement metadata. Establish golden snapshots from small reproducible fixtures, initially with structural plasticity disabled.

Acceptance: the viewer reproduces known fixture nodes/edges and state, and capture-on/off runs preserve causal outputs and computational state. Complete this milestone after the first software integration/verification gate and before deep optimization.

### Visualization-3 — GPU exporter using the same logical format

Export GPU state into the same versioned logical snapshot contract and host viewer. Backend-specific memory layouts and transfer formats are adapters only. Capture at declared causally comparable boundaries without treating a CUDA batch as a neural timestep.

Acceptance: matched CPU/GPU fixtures compare IDs, connectivity, activity intervals and represented state under predeclared numerical tolerances; document any unavailable fields and capture overhead.

### Visualization-4 — Temporal snapshot sequences

Support ordered snapshot sequences with run identity, simulation times, capture boundaries and explicit gaps. Provide playback, pause, step and structural differences to inspect formation, pruning, reinforcement and activity propagation. Begin sequence support with fixed topology; add formation/pruning fixtures after Luna-10's verified plasticity work.

Acceptance: known changes appear at the correct recorded boundaries, reused IDs remain distinguishable, and missing captures are shown as gaps rather than inferred neural events. Playback speed and sampling cadence must not alter model execution.

### Visualization-5 — ModelSim/RTL dump and canonical conversion

After software event semantics stabilize, have ModelSim/RTL simulation export a hex or binary state dump with schema/adapter version, field map, widths, signedness, byte/word order, fixed-point scaling and capture metadata. Convert the dump into Visualization-1 snapshots for the same viewer.

Acceptance: a small known RTL fixture decodes to expected neurons, connections and state; malformed/truncated dumps and unknown RTL values are reported rather than silently converted to valid zeros. Compare against software at declared equivalent causal boundaries, not merely equal host or hardware clock counts.

### Visualization-6 — DE1-SoC hardware observability

Use Ethernet as the primary DE1-SoC state-streaming path to the host viewer, with a board-specific transport adapter converting captured state to the canonical snapshot. Plan the FPGA-to-HPS capture/transfer and host framing, sequencing, bounded buffering and loss reporting without making transport part of neural semantics.

Keep VGA optional as an on-board diagnostic view for activity, occupancy and selected local connections. VGA refresh and Ethernet delivery rates are display/transport concerns only; neither may control neuron updates or structural decisions.

Acceptance: host captures decode correctly, disconnects/slow receivers are handled without changing computation, and capture loss/overhead is reported. If VGA is implemented, verify its display-only behavior independently of the host path.

### Visualization-7 — Cross-backend structural validation

Luna-11 and Luna-14 compare CPU, GPU, ModelSim/RTL and FPGA snapshots from matched inputs, seeds, initial topology, resource budgets and supported operations. Match stable IDs and declared causal boundaries; compare nodes, directed edges, fan-in/out, creation/pruning changes, relevant strengths and activity/state under predeclared precision and timing tolerances.

Acceptance: reproducible fixtures, machine-readable structural differences and linked viewer evidence identify the first observed divergence or explicitly report unavailable/incomparable captures. Visual inspection supplements numerical regression and invariant checks; it does not replace them or establish exact equality across differing hardware.

Sequence Visualization-1 → Visualization-2 before deep optimization; add Visualization-3 with GPU work and Visualization-4 with temporal/structural experiments. Visualization-5 and Visualization-6 follow stable software semantics and the FPGA branch. Apply Visualization-7 incrementally as each backend becomes available; final coverage includes all four backends. Luna-0 assigns bounded ownership using the existing roles and handoff format; no new Luna numbering or architecture clause is introduced.

---

# 23. Immediate Success Criteria

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

# 24. Guiding Principle

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

Experimental gating and plasticity begin after the first integrated software milestone passes. FPGA and FPAA branches begin after software event semantics are stable; Luna-14 compares both against versioned reference traces. Hardware-specific clocks, quantization and metering must not redefine neural semantics.

See [acceptance criteria](../architecture/ACCEPTANCE_CRITERIA.md) and [proposal process](../architecture_proposals/README.md).

