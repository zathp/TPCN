# TPCN Luna Multi-Agent Workflow — Event-Driven Architecture

## Mission

Evolve TPCN into a hardware-realizable, event-driven predictive-coding network while preserving its core principles.

The immediate benchmark is sequential letter-stroke classification. Each stroke or stroke point is presented as subsequent temporal data rather than converting the complete character into a static image.

The workflow must support eventual:

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

# 18. Luna-15 — FPGA/VHDL Branch

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
             Luna-12 (authorized next)
             Contract + CPU exporter
                 │
              ┌────┴────┐
              ▼         ▼
             Luna-13    Luna-14
            GPU       ModelSim/FPGA
                   bridge
              └────┬────┘
                 ▼
             Post-observability
             hardware track
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

