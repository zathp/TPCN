# TPCN Luna Multi-Agent Workflow — Event-Driven Architecture

## ACP-0003 heterogeneous execution review

ACP-0003 is accepted for staged implementation as an architecture-governance
proposal for separating canonical TPCN semantics from GPU, FPGA and FPAA
realization contracts. The selected equal-time policy is Model C: strict
serialized mode is a validation path, while coincident FPAA integration is a
declared approximation under Model B semantics. Luna-18 is authorized only for
the H1 hardware-neutral execution IR/backend interface skeleton. The proposed
order is canonical/reference behavior, H1 IR, GPU native reference, GPU FPGA
approximation, GPU FPAA approximation, and only then device-specific
implementation. ACP-0002 N2 remains closed and authoritative;
ACP-0002 N3 and later stages remain unauthorized, Luna-13F remains closed and
Luna-13G remains unauthorized.

ACP-0004, **Attractor Excursion and Event-Compression Neuron**, is accepted for
staged implementation. The canonical output term is **excursion**:
GPU/software and FPGA reference semantics use exactly one digital event per
excursion, while FPAA may provide a physical spike/analog excursion under a
later approximation contract. Luna-19 is authorized only for E1, the static
leaky accumulator and single-excursion reference; it must not implement M,
learning, IR-2, backends, approximation or H2. ACP-0002 N3, ACP-0003 H2,
Luna-13F reopening and Luna-13G remain unauthorized.

ACP-0005 authorizes the next schema dependency: TPCN-IR-2 may represent
excursion-aware transferable E1 state and future M state, but does not execute
M. Luna-20 implementation and the independent Luna-0 closure are complete.
The final Luna-0 E2/M dispatch review clarified final residual identity and
provenance ownership, reset semantics during M, and the separate E2-capable
IR-2 reconstruction boundary. Luna-21 implementation was published at
`bfc866be053f9692382d1be5e048f5b4d280e5f6`, with its completion handoff at
`5d0171f46b90664b1a6aca5709cc2f07f19b7f4e`. The initial independent review
at `a9077997740ccdc374c7ad89deef122112967369` was
**BLOCKED — IR-2 RECONSTRUCTION DEFECT**: validated S-state records could
have identity high-water counters behind active IDs or counters beyond the
event budget, allowing episode identity reuse. Its bounded correction gate
and evidence remain in
`workflow/handoffs/luna-0-independent-review-ACP-0004-E2-Luna-21-20261003.md`.
The authorized correction was implemented at
`ac2e822e5c7656d649c6e77f62024c6d6e4cf72f`; its handoff was published at
`3fb6d8c5128277bc8ecc5b2beea7288c214b772d`.
Luna-21's bounded IR-2 correction was independently reviewed and closed at
the review publication recorded in
`workflow/handoffs/luna-0-independent-corrective-review-ACP-0004-E2-Luna-21-20261003.md`.
The review independently reproduced the prior blockers on the pre-correction
revision, verified corrected validation and continuation, and repaired the
remaining vacuous unique-ID test oracle without changing production runtime
code. ACP-0004 remains staged; this closure is not architecture promotion or
integration readiness. ACP-0003 H2, ACP-0002 N3, backends, calibration and
hardware remain separately gated.

## Mission

Evolve TPCN into a hardware-realizable, event-driven predictive-coding network while preserving its core principles.

The immediate benchmark is sequential letter-stroke classification. Each stroke or stroke point is presented as subsequent temporal data rather than converting the complete character into a static image.

The workflow must support eventual:

## Future Luna Contract

Every newly created Luna must publish a bounded dispatch record before
implementation begins. The record is normative for the workflow and must use
the handoff template.

### Required identity and classification

Declare the Luna identifier, descriptive name, task ID, baseline repository
revision, dependencies, owner and exact owned files/components. Classify the
work as one or more of `OBSERVATION`, `VERIFICATION`, `EXPERIMENT`,
`INTEGRATION`, `IMPLEMENTATION`, `ARCHITECTURE-PROMOTION` and `HARDWARE`.
Classification controls scope: an experiment does not amend the canonical
architecture; verification should not repair unrelated production behavior;
architecture promotion requires explicit Luna-0/project-owner approval and the
ACP process.

### Required hypothesis, invariants and scope

An experimental Luna must state a falsifiable hypothesis and the result that
would count against it. It must list clauses touched and preserved, interfaces,
label/information boundaries, resource bounds, timing assumptions and reset
boundaries. It must state authorized files/components and production-code
authority, plus relevant explicit exclusions such as labels, global learning,
unbounded topology, hardware acceptance, real-data claims, classifier redesign
or unrelated refactoring.

### Required controls and evidence

Controls and comparison conditions must be declared before implementation.
Metrics must be declared before running the experiment, including negative
results and failed seeds. Record baseline revision, seeds, configuration,
workload/dataset version, commands and environment where applicable. Every
mechanism must account for finite state, events, queues, fan-in, fan-out,
edges, candidate lists, history/eligibility, lineage/path depth, memory and
hardware representation. Do not add an effectively unbounded structure to the
canonical path without architecture review.

### Required boundary and verification checks

State whether each information source is available to a physical local
component; global evaluation/orchestration may remain outside canonical neural
computation. For canonical mechanisms, describe eventual FPGA, FPAA or hybrid
mapping and identify software-only conveniences. The completion record must
separate passed, failed, not-run and not-applicable results and include focused
tests, relevant prior-Luna regressions, full regression where applicable,
compile/static validation, diagnostics and `git diff --check`.

### Promotion and handoff boundary

Experimental success does not change the architecture. Promotion requires
completed evidence, Luna-0 review, explicit owner decision where required, an
ACP for material contract changes, synchronized contract/changelog revisions,
and updated acceptance criteria. Every Luna leaves a machine-readable and
human-readable handoff distinguishing `OBSERVED`, `INFERRED` and
`HYPOTHESIZED`, with changes, unchanged behavior, measurements, failures,
uncertainty, gate decision and authorized next work.

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

## Luna-12A — CPU Training Visualization Integration

**Authorization:** Luna-12 has passed its CPU reference/exporter gate. Luna-0 explicitly authorizes Luna-12A for the deterministic Luna-9 synthetic training/evaluation path only. This authorization does not select or authorize a real dataset benchmark, and it does not make Luna-12A a prerequisite for Luna-13 or Luna-14.

**Purpose:** Run bounded CPU-side TPCN training while capturing TPCV-1 snapshots so activity, represented state, connectivity, reward/utility behavior, and any validated structural changes can be inspected over time.

**Dependency shape:**

```text
Luna-12
|
+--> Luna-12A  CPU training + visualization integration
|
+--> Luna-13  GPU-compatible visualization
|
+--> Luna-14  ModelSim/FPGA visualization
```

Luna-13 and Luna-14 remain separate downstream branches. Neither depends on Luna-12A unless Luna-0 later records an explicit decision.

**Scope:** Integrate the Luna-9 deterministic synthetic workload with TPCV-1 capture; provide a configurable CPU runner for epochs and snapshot intervals; store and replay bounded snapshots through the Luna-12 parser; expose epoch/snapshot indices, neuron identity, active state, represented state or activation magnitude, connections, metrics, and topology evolution where available; and provide a lightweight viewer or deterministic replay/export path that a user can run from the command line.

Visualization is strictly downstream-only and non-semantic. Capture, serialization, replay, rendering, storage limits, viewer timing, and dropped/incomplete records must not influence event ordering, neuron updates, predictions, reward, eligibility, classifier behavior, topology decisions, queue behavior, timestamps, or training results. The same deterministic workload with visualization disabled, snapshots every epoch, and more frequent snapshots must produce identical predictions, metrics, replay digest, update/parameter counts, topology where applicable, reward/utility state, and final network state.

Use Luna-10 structural plasticity only when its existing public API can be consumed without architecture changes and bounded topology invariants remain enforced. Fixed topology is the valid default. If those conditions are not met, defer structural-plasticity visualization and report that limitation; do not redesign the topology or core interfaces under Luna-12A.

**Explicit non-goals:** Do not implement GPU or ModelSim/FPGA visualization, authorize real-dataset benchmarking, alter TPCV-1 semantics, add a visualization return path, or weaken any A01-A15 invariant. This milestone does not authorize Luna-13 or Luna-14 work.

**Expected handoff:** A reproducible CPU training/demo runner, bounded TPCV-1 snapshot capture and replay evidence, a minimal inspection path, non-interference results, deterministic replay tests, and an explicit structural-plasticity included/deferred decision.

**Completion gate:** CPU training runs through the current Luna-9 event-driven experiment path; snapshots decode and replay through Luna-12 tooling; malformed, missing, and over-limit captures fail clearly; visualization-on/off and snapshot-frequency comparisons match; deterministic snapshot sequences pass; relevant regression and compile checks pass; and no architecture invariant is weakened. Real-dataset benchmarking remains separately gated.

## Luna-12B — Persistent Topology and Structural Plasticity Visualization Integration

**Authorization:** Luna-12A has passed its stated completion gate on the deterministic Luna-9 synthetic path: full suite 130 passed, 1 skipped; focused Luna-12A tests 3 passed; compilation passed; diagnostics reported no errors; `git diff --check` passed; and a three-snapshot smoke run was saved and replayed deterministically. Luna-0 explicitly authorizes Luna-12B as the next CPU visualization/integration milestone. This authorization does not authorize real-dataset benchmarking, Luna-15, Luna-16, or Luna-17. Luna-13 and Luna-14 remain independently authorized from Luna-12 and do not depend on Luna-12B.

**Purpose:** Integrate a persistent bounded Luna-4 topology into the CPU experiment path so the validated Luna-10 structural-plasticity mechanism can operate across examples and epochs, and expose measured structure/function behavior through TPCV-1.

**Dependency shape:**

```text
Luna-12
|
+--> Luna-12A  CPU training + visualization integration
|      |
|      +--> Luna-12B  persistent topology + structural plasticity
|
+--> Luna-13  GPU-compatible visualization
|
+--> Luna-14  ModelSim/FPGA visualization
```

Luna-12B depends on the completed Luna-12A CPU capture/replay path and the public Luna-9/Luna-10 interfaces. It must not create a second topology model, redefine TPCN architecture, or become a prerequisite for Luna-13 or Luna-14.

**Scope:** Preserve topology across examples and epochs where adaptation requires it; use the existing bounded topology and Luna-10 mutation APIs; capture accepted additions, removals, rejected mutations and reasons, active edge count, fan-in/out utilization, bounded mutation history, and replay-visible topology deltas; and add fixed-topology/learning, structural-plasticity, and supported no/reduced-learning comparisons. Report activity coverage and structure/function metrics sufficient to distinguish active, adaptive, useful-static, changing-without-benefit, and inert outcomes using measurements rather than subjective labels.

The runner should follow repository CLI conventions and support an equivalent developer command to `python <runner>.py --epochs 20 --structural-plasticity --snapshot-every 1`. A completed run must report starting/ending connections, additions, removals, rejected mutations, active-neuron fraction, prediction loss, accuracy, reward, energy, and utility before/after. Zero mutations are not automatically a failure; interpret them with behavior, reward, utility, event activity, and activation coverage.

TPCV remains downstream-only. Replay may distinguish unchanged, added, and recently removed connections from history, active/inactive neurons, snapshot/epoch index, and structural/behavioral metrics, but capture and viewing must not approve, trigger, or alter mutations, event ordering, routing, reward, classifier behavior, training, or backpressure.

**Required evidence:** Same-seed mutation sequences, final topology, snapshot sequences, and functional results reproduce where the underlying contracts guarantee determinism; capture-on/off results match; fan-in/out, finite propagation, bounded state/history, failed admission, pruning, routing validity, and non-interference checks pass. Record all beneficial and harmful outcomes and explicitly report topology/behavior combinations: unchanged/unchanged, unchanged/improved, changed/unchanged, changed/improved, and changed/degraded where observed.

**Explicit non-goals:** Do not select or benchmark a real dataset, redesign Luna-4/Luna-10 APIs, invent visualization-only mutations, alter TPCV-1 semantics, add a visualization return path, authorize Luna-15/Luna-16/Luna-17, or weaken A01-A15.

**Expected handoff:** A persistent-topology CPU runner, bounded structural-plasticity and structure/function evidence, TPCV replay artifacts/tests, inertness reporting, deterministic capture-on/off comparisons, and an explicit integration-readiness decision returned to Luna-0.

**Completion gate:** The implementation uses one validated bounded topology across the declared training scope; mutation accounting and rejection reasons are inspectable; fixed/plasticity/control comparisons run; topology and activity replay is deterministic and downstream-only; boundedness and non-interference checks pass; metrics support an evidence-based inertness/usefulness classification; and no architecture invariant is weakened.

## Luna-12C - Human-Interpretable 3D Temporal Visualization

**Authorization:** Luna-12C is authorized by Luna-0 on 2026-09-27 as an observational, replay-first milestone. It preserves the downstream-only TPCV architecture and does not change A01-A15 or require an ACP.

**Dependency shape:**

```text
Luna-12
|
+--> Luna-12A  CPU training + replay
|      |
|      +--> Luna-12B  persistent topology + plasticity observability
|
+--> Luna-12C  human-interpretable 3D temporal viewer
|
+--> Luna-13  GPU-compatible visualization
|
+--> Luna-14  ModelSim/FPGA visualization
```

Luna-12C may consume Luna-12A/B replay artifacts but is not a prerequisite for Luna-13 or Luna-14. Those milestones remain independent siblings under their existing authorization records.

**Purpose:** Provide human-interpretable 3D replay of stable neuron identity, activity, directed connections, structural changes, and synchronized behavioral/structural metrics during recorded learning.

**Graphics strategy:** Adapt the existing Python `pygame` + `PyOpenGL` path with NumPy buffers. The older GLFW path is coupled to simulation objects and CuPy, so it is not the primary foundation for this replay viewer.

**Scope:** Load bounded TPCV replay artifacts; preserve canonical coordinates when present or derive a deterministic diagnostic 3D layout; render neurons and directed edges with separate readable encodings; distinguish persistent, added, and recently pruned edges where replay history permits; provide configurable topology highlights and dense-graph filters; support play/pause, speed, both-direction stepping, first/last, direct snapshot selection, orbit, pan, zoom, reset, fit, neuron inspection, and synchronized metrics; and use packed/batched rendering with a path for later run/seed comparison.

TPCV-1 currently lacks canonical 3D coordinates, event-by-event propagation timing, per-edge traffic, and per-neuron energy/utility fields. Luna-12C must therefore show deterministic diagnostic positions and snapshot-level activity, display unavailable fields as unavailable, and never synthesize event pulses or timing.

**Non-interference:** Loading, layout, rendering, filters, playback, selection, window timing, dropped frames, and a slow viewer must not affect event ordering, timestamps, queues, routing, topology or structural plasticity, reward, utility, classifier behavior, training, or reproducibility. The renderer is not part of the TPCN architecture.

**Explicit non-goals:** Do not alter TPCV-1 semantics, implement GPU or ModelSim/FPGA paths, select a real dataset, add live-training coupling, create visualization-only mutations, or authorize Luna-15/Luna-16/Luna-17.

**Expected handoff:** A replay-first 3D viewer, deterministic layout and playback evidence, neuron inspection and filtering, synchronized metric presentation, focused headless/viewer tests, artifact fixtures/digests, unsupported-field documentation, and an explicit non-interference result.

**Completion gate:** Existing replay artifacts load; stable neurons and edges render; topology changes are distinguishable; deterministic playback/navigation, inspection, filters, and metrics work; repeated replay produces the same layout/view state; focused and relevant regression tests pass; and visualization has no effect on recorded computation.

## Luna-12D - Temporal Interpretability and Network-Dynamics Analysis

**Authorization:** Authorized by Luna-0 for analysis of existing TPCV-1/replay
artifacts and permitted deterministic synthetic runs. This remains authorized
even if Luna-12C has an unavailable interactive graphics check. It does not
authorize real-dataset benchmarking, hardware acceptance, or Luna-15/16/17.

**Purpose:** Measure and interpret the current system without repairing the
known separation between persistent topology mutation and the computational
path used by `_run_example()`.

**Dependency shape:**

```text
Luna-12 -> Luna-12A -> Luna-12B -> Luna-12C -> Luna-12D
                                |
                                v
                              Luna-12E

Luna-12 -> Luna-13  GPU-compatible visualization
Luna-12 -> Luna-14  ModelSim/FPGA visualization
```

Luna-13 and Luna-14 remain independent siblings and do not depend on 12D or
12E. Luna-12D may consume 12C-compatible replay artifacts, but all analysis
remains downstream-only.

**Scope:** Produce human-readable summaries and machine-readable metrics for
active/inactive neurons; persistent, exercised, added, removed, and rejected
edges; edge lifetimes; additions/removals per epoch; rejection reasons; graph
stabilization; fan-in/out saturation; active-edge utilization; topology-change
and activity concentration; and correlation with accuracy, prediction loss,
reward, and utility. Distinguish edge existence from computational exercise
where evidence exists, and never infer causation from correlation.

Explicitly investigate the connection plateau using precise causes such as
duplicate edge, source fan-out full, destination fan-in full, global edge
capacity, nonlocal candidate, candidate capacity, pruning/growth interaction,
or no valid candidate remaining. Classify observed states as stable/active,
stable/inactive, structurally changing/behaviorally flat, improving,
degrading, or high-churn/low-functional change.

**Non-goals:** Do not integrate topology into event routing, alter TPCV-1,
change neuron/classifier/training behavior, claim causality, select a real
dataset, accept hardware behavior, or authorize 13/14/15/16/17 work.

**Expected handoff:** Reproducible summaries, machine-readable metrics,
plateau/rejection evidence, correlation-limited interpretation, focused tests,
and a recommendation for Luna-0 review before 12E dispatch.

**Completion gate:** Requested topology/activity categories are represented or
explicitly unavailable; existing versus exercised edges are distinguished;
rejection reasons are precise; plateau behavior is explained from recorded
evidence; summaries and metrics reproduce; and analysis has no return path.

## Luna-12E - Computational Topology Integration and Causal Learning Verification

**Authorization:** Blocked until Luna-12D completes and Luna-0 reviews its
evidence. Creating this entry does not authorize implementation, real-dataset
benchmarking, hardware acceptance, or Luna-15/16/17.

**Purpose:** Make persistent bounded topology the actual event-routing network
used by the experiment path, then verify that structural changes can causally
alter network behavior.

**Dependency shape:**

```text
Luna-12C -> Luna-12D -> Luna-12E
```

**Scope:** Use the same bounded topology for structural plasticity and
computation. Verify event propagation through actual edges; removal of a
reachable edge changing downstream activity; addition of a reachable edge
changing downstream activity when relevant; prediction/error behavior derived
from propagated activity; and functional metrics responding to topology under
a workload that exercises the changed path. Use controlled reachable-edge
interventions and matched controls.

**Non-goals:** Do not weaken A01-A15, introduce a global neural clock, create a
second topology model, bypass finite routing, use unrestricted global learning,
select a real dataset, or claim hardware acceptance. Do not dispatch before
the 12D evidence review.

**Expected handoff:** Integrated routing evidence, reachable-edge intervention
results, prediction/error and classification metrics, boundedness and
determinism results, and an explicit Luna-0 readiness decision.

**Completion gate:** Structural plasticity and event computation share one
validated bounded topology; add/remove interventions produce causal routing
effects; prediction/error and functional metrics derive from propagated
activity; matched controls rule out observational confounds; and applicable
core/non-interference checks pass.

**Luna-0 downstream-failure classification (2026-10-04):** the two known
Luna-12E failures are legacy-observable assertions retained across the later
EXCURSION_V1 default switch. The routed-edge intervention still produces
delayed delivered activity and increases processed events; the test's
additional unconditional `prediction_loss`-must-change assertion is not
supported by its one-way source-to-sink topology. The second test's neuron
identity assertion passes, but its final-clock expectations compare settled
E2 local clocks against pre-E2 per-point values; it does not demonstrate
missing character-state reset. See
`workflow/handoffs/luna-0-classification-luna-12e-failures-20261004.md`.
These tests remain unresolved downstream compatibility failures. This
classification authorizes no code/test change and no Luna-28 creation or
execution; a separate governance decision is required before follow-on work.

## Luna-12F - Readout Learning and Class-Separation Verification

**Authorization:** Luna-12E is complete and accepted by Luna-0 for the
computational-topology gate. Luna-0 authorizes Luna-12F for deterministic
synthetic A/Z readout verification and correction of the external supervised
readout path only. This does not authorize real-dataset benchmarking,
Luna-15/Luna-16/Luna-17, or an architecture-wide classifier redesign.

**Purpose:** Determine whether the current positive-reward-only readout update
condition starves an initially misclassified class, measure class separation
before readout selection, and apply the smallest bounded external-readout
correction that permits every supervised training class to acquire a
representation.

**Dependency shape:**

```text
Luna-12C -> Luna-12D -> Luna-12E -> Luna-12F

Luna-12 -> Luna-13  GPU-compatible visualization
Luna-12 -> Luna-14  ModelSim/FPGA visualization
```

Luna-12F preserves the successful Luna-12E event-routing and persistent
bounded-topology integration. Luna-13 and Luna-14 remain independent siblings
and do not depend on Luna-12F.

**Architectural boundary:** Labels may enter only the external supervised
training/readout layer after label-free neural computation has completed. They
must not enter canonical events, neuron or predictor state, topology mutation
evidence, structural-plasticity decisions, routing, or energy computation.
Readout state is external, bounded by `max_classes`, deterministic, and
resettable. Reward may modulate refinement, but reward sign must not be the
sole condition for creating a supervised class representation.

**Required work:**

1. Reproduce the current gate with a deterministic A/Z fixture, recording
  initial prediction, reward, update decision, and prototype/readout state;
  explicitly test whether a misclassified Z can create Z state.
2. Expose pre-readout network features, target label for evaluation only,
  class distances/scores, prediction, confidence, and winner margin. Measure
  whether A and Z are separable before the readout and whether the readout
  discards that difference.
3. Implement the smallest compatible supervised prototype/centroid or class
  statistics correction. Separate target acquisition from any
  reward-modulated refinement and report missing declared class
  representations.
4. Compare positive-reward-gated and corrected readouts on identical seeds
  and workloads. Report accuracy, per-class accuracy, confusion matrix,
  confidence/margin, prediction loss, reward, energy, utility, topology,
  update count, prototype count, and starvation count.
5. Compare fixed topology, structural plasticity, and useful no-learning
  controls after readout correction. Do not require topology to improve
  accuracy and do not claim readout changes improve the neural predictor.
6. Add replay-side diagnostics where compatible with existing TPCV-1 fields;
  keep capture and analysis downstream-only and avoid incompatible schema
  changes without Luna-0 review.

**Required tests:** Both classes acquire bounded readout state; an initially
misclassified Z can become correct after supervised updates; label changes do
not change the neural event trace for identical inputs; labels affect only
external readout learning/evaluation; `max_classes` bounds state; and same-seed
training reproduces readout state. Include Luna-12E causal integration,
experiment, classifier/readout, structural-plasticity, and relevant
visualization/analysis regressions.

**Non-goals:** Do not modify canonical event semantics, neuron/predictor
state, topology mutation logic, routing, energy computation, TPCV-1 semantics,
or sibling milestone dependencies. Do not benchmark a real dataset or replace
the network with a large unrelated classifier.

**Expected handoff:** A reproducible before/after starvation analysis,
pre-readout separation diagnostics, bounded corrected-readout implementation,
fixed/plasticity/control comparisons, focused and full validation results, and
an explicit statement of whether the readout bottleneck was confirmed.

**Completion gate:** All required label-isolation, boundedness, determinism,
class-acquisition, before/after, and topology-interaction evidence is recorded;
the Luna-12E causal tests remain passing; applicable regression, compile,
diagnostic, and diff checks pass; and no A01-A15 invariant is weakened.

## Luna-12G - Spiral Handedness Temporal Classification Benchmark

**Authorization:** Luna-12F is accepted by Luna-0 for the corrected external
readout dependency. Luna-0 authorizes Luna-12G on 2026-09-27 as a synthetic
software-reference benchmark. This authorization does not authorize real
handwriting data, GPU/FPGA/ModelSim acceptance, hardware promotion, or an
architecture-wide classifier redesign.

**Purpose:** Replace the overly separable synthetic A/Z workload with a
two-class center-outward spiral benchmark whose primary class information is
ordered temporal handedness: left-handed versus right-handed trajectories.
Both classes start at the center and share the same nuisance distributions.

**Dependency shape:**

```text
Luna-12C -> Luna-12D -> Luna-12E -> Luna-12F -> Luna-12G

Luna-12 -> Luna-13  GPU-compatible visualization
Luna-12 -> Luna-14  ModelSim/FPGA visualization
```

Luna-12G consumes the accepted Luna-12E event-routing path and Luna-12F
external readout. Luna-13 and Luna-14 remain independent siblings and do not
depend on 12G.

**Scope:** Define a deterministic seeded generator and disjoint train/eval
streams for left/right center-outward spirals. Sample global rotation, scale,
translation, angular speed, bounded radial growth, sampling timing, mild
coordinate noise, and mild radial jitter independently of class. Record
generator metadata for reproduction, but feed only ordered stroke and timing
events plus legitimate boundary events to the neural computation.

Run fixed-topology learning, structural-plasticity learning, and a no-learning
control with external readout learning disabled. Add shuffled-order, carefully defined time-reversal, same-class
nuisance-invariance, and opposite-handed matched-pair controls. Report
accuracy without treating 1.0 as a success threshold; investigate any perfect
no-learning result as possible benchmark leakage.

**Architectural boundary:** Handedness labels remain external. They must not
enter canonical events, node or neuron IDs, event types, predictor state,
topology mutation evidence, structural-plasticity decisions, energy state, or
routing. Readout supervision may use the target only after label-free neural
processing, through the bounded Luna-12F readout interface.

**Non-goals:** Do not alter A01-A15, add a global neural timestep, introduce a
spatial reservoir, use future points or whole-example normalization, benchmark
real handwriting, or authorize sibling visualization/hardware work.

**Expected handoff:** A benchmark specification and reproducible implementation
with exact seeds/splits, trajectory metadata, all controls, per-class and
confusion diagnostics, prediction/readout/energy/utility/event/topology/
mutation metrics, label-isolation evidence, and a report of whether fixed or
structural topology contributes useful behavior.

**Completion gate:** Train and evaluation examples are disjoint and nuisance
combinations are not copied verbatim; both classes and all required controls
are measured; labels are isolated from neural computation; no-learning,
fixed-topology, and structural-plasticity results are separately reported;
ordered, shuffled, and reversal behavior is analyzed; deterministic replay and
bounded core/regression checks pass; and no accuracy threshold is invented.

## Luna-12H - Intrinsic Temporal State, Recurrence, and Unequal-Delay Convergence

**Authorization:** Authorized by Luna-0 on 2026-09-27 after the Luna-12G
benchmark reported identical ordered, shuffled, and reversed classification
results. The existing architecture already permits local elapsed-time state,
finite propagation, and bounded recurrent dynamics; this milestone makes the
canonical evidence requirements explicit. No ACP is required. This dispatch
does not authorize a real dataset, hardware acceptance, or a spiral-specific
neuron/classifier redesign.

**Purpose:** Determine whether the neural core itself preserves temporal
information before adding a more sophisticated external temporal classifier.
Verify two distinct mechanisms: intrinsic local state that persists and
evolves between events, and network/path temporal state in which consequences
with unequal cumulative delays converge at a downstream neuron.

**Dependency shape:**

```text
Luna-12C -> Luna-12D -> Luna-12E -> Luna-12F -> Luna-12G -> Luna-12H

Luna-12 -> Luna-13  GPU-compatible visualization
Luna-12 -> Luna-14  ModelSim/FPGA visualization
```

Luna-12H uses the accepted Luna-12E event-routing path and the Luna-12G
temporal-order limitation as motivation. Luna-13 and Luna-14 remain
independent siblings and do not depend on 12H.

**Canonical temporal semantics:** A neuron is not a memoryless event
transform. Processing may depend on `state_before`, `incoming_event`, and
`elapsed_local_time`. Conceptually, local state evolves analytically or when
an event is processed:

```text
s(t1-) = Phi(s(t0+), t1 - t0)
s(t1+) = F(s(t1-), event_t1)
```

A single event must be able to perturb bounded state that is observable later
before a declared character/sequence reset. The reference neuron must expose
at least one deterministic temporal noncommutativity fixture where exchanging
event order changes state, output, or trace; this is a capability requirement,
not a claim that every parameter choice is order-sensitive. Elapsed time comes
from canonical event timestamps and local neuron time. No synchronous whole-
network step, global frame update, or hidden recurrent tick may be required
for correctness. Internally scheduled events may be documented and tested only
if already supported cleanly; do not invent autonomous events merely to pass
these checks when analytic event-time evolution is sufficient.

**Routing and recurrence semantics:** Permit `A -> C` and
`A -> B -> D -> C` to have different cumulative causal delays; path delay is
the sum of declared edge delays, not edge count. Preserve event timestamps and
canonical deterministic tie-breaking at fan-in. An older long-path consequence
must be able to converge with a newer short-path consequence and affect the
downstream result according to relative arrival timing. Cycles remain subject
to finite event budgets, lineage/path safeguards, queue bounds, monotonic local
time, bounded state and deterministic ordering. Luna-12H must not enable
infinite recurrent propagation.

**Reset and isolation:** Temporal neuron state persists within a character or
sequence and resets only at declared reset boundaries. Topology may persist
independently. Pending events, internal state, eligibility and prediction
records require an explicit boundary policy. No state may leak between
examples unless explicitly authorized, and labels remain outside neural
events, state, routing, topology, energy and prediction/error computation.

**Required controlled fixtures:**

1. Single-spike persistence: `+1` at `t=0`, then observe state before reset.
2. Ordered-pair noncommutativity: `(+1 at 0, -1 at 1)` versus
  `(-1 at 0, +1 at 1)` produces a state/output/trace difference.
3. Equal-event multiset distinction: the same event values with different
  order produce a deterministic difference.
4. Same values, changed interval: `+1 at 0, -1 at 1` versus
  `+1 at 0, -1 at 5` differs when elapsed time is relevant.
5. Unequal paths: verify `D_long > D_short` and timestamp-correct arrival for
  direct and multi-hop paths.
6. Convergent old/new arrival: an older event uses the long path and a newer
  event uses the short path; changing their timing relationship changes the
  downstream result.
7. Path pruning: pruning either path removes its future causal effect.
8. Arrival timing: the same total input with different arrival timing changes
  downstream state/output in at least one deterministic fixture.
9. Character reset: reset removes prior temporal state according to policy.
10. Same-seed determinism: state, queue, timestamps and ties reproduce.
11. Bounded recurrence: cycles terminate under declared budgets and bounds.
12. Label isolation: relabeling identical streams does not alter core traces.

**Expected handoff:** A focused implementation and verification slice for the
canonical neuron and event-routing path, fixture-level traces with units and
seeds, explicit decay/evolution/reset and tie policies, bounded-cycle and
pruning evidence, focused tests, applicable regression/compile/diagnostic
results, and a Luna-0 readiness decision. Report whether intrinsic or path
temporal state is demonstrated; do not infer temporal representation from
external classifier accuracy alone.

**Non-goals:** Do not hard-code spiral handedness, introduce a mandatory
global timestep, replace the event queue with synchronous stepping, add a
spatial reservoir, leak labels or future points into the core, or redesign the
external classifier before the core fixtures are measured.

**Completion gate:** All twelve controlled checks and the four minimal fixture
families are run or explicitly marked not applicable; timestamps, cumulative
delays and fan-in order are evidenced; reset/isolation and label isolation
pass; cycles remain bounded; same-seed replay passes; and no A01-A15 invariant
is weakened. An absent temporal effect is a valid result, but must be reported
as a failed capability check rather than hidden by readout changes.

## Luna-12I - Temporal-Associative Structural Growth and Fan-In Formation

**Authorization:** A post-12H experiment specified by ACP-0001 and the
project-owner request. It is not evidence that the mechanism works and does
not promote its rule into A14. Luna-13 and Luna-14 remain independent siblings.

**Classification:** `EXPERIMENT`, with `VERIFICATION` of bounded topology and
locality invariants. **Baseline:** the current repository revision recorded in
the dispatch handoff. **Dependencies:** accepted 12H semantics, Luna-4
bounded topology, Luna-10 structural-plasticity API, and the Luna-12E actual
event-routing path.

**Hypothesis:** If activity at two neurons repeatedly occurs in a consistent
short causal sequence, locally available timing evidence can increase
preference for a directed edge from the earlier neuron to the later neuron.
This may encourage causal path shortening and useful fan-in without global
topology knowledge. Evidence against the hypothesis includes no increase in
convergent causal structure over controls, timing-shuffled/reversed controls
performing equivalently, or increased churn/energy/resource use without
improved structural organization or task behavior.

**Controls:** Compare matched fixed topology, the existing structural-
plasticity policy, random legal candidate selection, and temporal-association
candidate selection. Where practical add timing-destroyed/shuffled and
reversed-order association controls. Keep seeds, budgets, workload, delays,
reset policy and training effort matched.

**Measurements:** Report fan-in/out distributions and saturation, edge
utilization, accepted growth, every rejection cause, duplicate proposals,
candidate availability, path lengths and cumulative causal delays, convergent
motif count, repeated temporal associations, path shortening,
replacement/pruning, edge lifetimes/churn, event count, prediction error,
energy/resource proxy with units, utility, task performance and determinism.
Distinguish degree saturation, random growth, duplicate churn and true useful
convergent fan-in. Record negative results and unavailable fields explicitly.

**Scope and invariants:** Production changes are authorized only in the
declared experiment components and tests. Preserve A01-A08, A07 label/local
information boundaries, A09-A11 accounting, A14 finite admission and causal
growth, and A15 portability. The mechanism may use only causal/local temporal
evidence; it may not inspect global topology, labels, future events or
evaluation-only metrics. A direct edge is a new positive-delay path and cannot
rewrite in-flight events. Bound candidate lists, evidence/history retention,
edge count, mutation count, event/lineage/queue budgets and all hardware-facing
representations.

**Non-goals:** Do not claim a useful learner from topology appearance alone,
make a timing window/correlation formula mandatory, redesign the classifier,
perform real-dataset or hardware acceptance, promote A14, add global learning
or implement unbounded topology.

**Expected handoff and gate:** Include the full Future Luna Contract fields,
controlled traces, all seeds/configurations/commands, negative results,
rejection accounting and `OBSERVED`/`INFERRED`/`HYPOTHESIZED` labels. The
mechanism is not accepted merely because it runs; Luna-0 reviews whether the
evidence supports a later experiment or ACP.

## Luna-12J - Temporal-Associative Structural Learning Efficacy and Causal Verification

**Authorization:** This is a separately dispatched `EXPERIMENT` and
`VERIFICATION` milestone after Luna-12I. Creating the scaffold does not
execute it. It does not amend A14, authorize temporal association as
mandatory, or block Luna-13, Luna-14, Luna-15, Luna-16 or Luna-17.

**Question and hypothesis:** Determine whether Luna-12I temporal-associative
growth produces useful computational or task-level benefit attributable to
learned topology rather than merely added edges or churn. Repeated local
temporal succession is hypothesized to guide bounded growth toward useful
convergence and/or shorter causal paths. Equivalent controls, no causal effect,
temporal-order destruction, or resource/churn costs that erase benefit count
against the hypothesis. Valid results include supported, partially supported,
not supported, inconclusive and blocked.

**Required controls:** Compare fixed topology, the existing pre-12I policy,
random legal structural growth and Luna-12I growth under comparable nodes,
edges, fan-in/out, candidates, state, events, mutation attempts, epochs,
delays, resets and seeds. Include shuffled, reversed, destroyed-timing or
matched-event-multiset controls where practical. Record and explain any budget
mismatch; do not search for favorable seeds.

**Computational and information boundary:** Use the persistent Luna-12E
topology and actual event-routing path. A disconnected visualization graph,
auxiliary topology or topology-only correlation is not evidence. Labels, future
events, global topology statistics, evaluation metrics and unrestricted trainer
state remain outside events, predictor state, routing, topology evidence,
structural evidence, eligibility and energy computation.

**Measurements and intervention:** Record task/class separation, prediction and
error behavior, events, activations, energy/resource proxy and units, edges,
additions/removals/rejections, fan-in/out and convergent motifs, utilization,
path delays/shortening, duplicates, replacement, churn, stabilization and
same-seed determinism. Perform a focused removal, freeze, legal replacement or
before/after replay intervention to test the chain from local evidence through
real topology and routed events to downstream state/output. Explicitly answer
whether ordinary growth saturates capacity before useful fan-in forms.

**Expected handoff and gate:** The handoff must include the full dispatch fields,
raw and summarized measurements, negative results, limitations and direct
answers to the seven Luna-12J questions. Separate `OBSERVED`, `INFERRED` and
`HYPOTHESIZED`, and passed/failed/not-run/not-applicable checks. Gate values are
PASS, PASS WITH FOLLOW-UP, INCONCLUSIVE, NOT SUPPORTED and BLOCKED. Any result
returns to Luna-0; even PASS does not promote A14 or automatically authorize
Luna-12K execution. Luna-0 may separately create a bounded follow-up after a
PASS WITH FOLLOW-UP decision.

## Luna-12K - Capacity-Pressure, Equal-Exposure, and Path-Shortening Verification

**Authorization:** Luna-12K is a separately scoped `EXPERIMENT` and
`VERIFICATION` follow-up created after the verified Luna-12J result
`partially supported` with gate `PASS WITH FOLLOW-UP`. Creation does not
execute the experiment. Execution requires an explicit assignment and a
completed 12K handoff; no A14 promotion or Luna-12L/later work is authorized.

**Question and hypothesis:** Under equal candidate exposure and bounded
topology pressure, temporal-associative structural growth is hypothesized to
allocate scarce connection capacity toward useful causal convergence and to
create a legal shortcut that measurably reduces meaningful propagation path
length or delay compared with temporally uninformed controls. The hypothesis
is falsified when equalized controls match or exceed useful allocation, real
capacity pressure is absent, temporal evidence does not alter selection, the
shortcut does not change routed computation, or the result disappears under
reversed/timing-destroyed evidence. Valid results are supported, partially
supported, not supported, inconclusive or blocked.

**Controls and equal exposure:** Compare fixed topology, pre-12I structural
growth, random legal growth, Luna-12I temporal growth and reversed/shuffled or
timing-destroyed temporal evidence. Equalize candidate set/count, mutation
opportunities, growth attempts, edge/fan-in/out bounds, pruning/replacement
budget, trials, event workload and seeds. Measure candidates exposed,
considered and selected. Record and quantify every mismatch; do not credit a
policy for extra useful candidates or computation. An oracle-like selector is
diagnostic only and is not a legal learning mechanism.

**Fixture and intervention:** Use multiple legal, resource-competitive
candidates, including temporally relevant and irrelevant edges. Reach actual
fan-in, fan-out, global-edge, candidate-capacity or replacement/pruning
pressure and record precise rejection causes. Begin with a functional
finite-delay long path and a legal initially absent shortcut in the actual
Luna-12E routed topology. Compare before growth, after shortcut formation and
after shortcut removal on hop count, cumulative delay, arrival timestamps,
routed events, activations, downstream state/output, prediction/error and
energy/resource proxy. Graph-distance change alone is insufficient.

**Invariants and evidence:** Preserve A01-A04, A06-A11, A14 and A15. Labels,
future events, global topology statistics, evaluation metrics, wall-clock state
and unrestricted trainer state remain outside canonical events, predictor
state, routing, topology evidence, structural evidence, eligibility and
energy computation. All candidates, histories, queues, paths, mutations and
analysis buffers are finite. The handoff must distinguish `OBSERVED`,
`INFERRED` and `HYPOTHESIZED`, retain unfavorable seeds, and classify every
focused, regression, full-suite, compile, diagnostic and diff check as passed,
failed, not run or not applicable. Any result returns to Luna-0.

## Luna-12L - Energy/Prediction Tradeoff and Four-Class Temporal Scale Verification

**Authorization:** Luna-12L is a separately scoped `EXPERIMENT` and
`VERIFICATION` follow-up created after the Luna-12K `PASS WITH FOLLOW-UP`
review. Creation does not execute the experiment, amend A14 or authorize a
later Luna. Execution requires a separate explicit assignment and a completed
12L handoff returning to Luna-0.

**Question and hypothesis:** Determine whether temporal-associative growth
retains useful classification and causal path-allocation behavior when the
Luna-12G spiral task expands to four classes combining handedness and
traversal direction, and whether the Luna-12K proxy-energy/prediction-loss
cost is bounded, explained or improved without destroying the causal benefit.
The primary hypothesis is falsified by loss of useful classification or path
allocation at the expanded scale, temporal-order controls performing
equivalently, or an unfavorable resource/prediction tradeoff without a
measured compensating benefit. A negative result is valid.

**Four-class benchmark:** Use the existing Luna-12G naming convention extended
to `spiral-left-outward`, `spiral-right-outward`, `spiral-left-inward` and
`spiral-right-inward`. Inward examples must use the same trajectory family as
outward examples and depend on traversal direction rather than a static class
marker. Match point count, radius, center, scale, noise, sampling, amplitude,
duration, payload conventions and identifiers across classes where practical.
Labels remain external to canonical events, prediction, routing, topology,
structural evidence, eligibility and energy. A reused sequence boundary/check
event must be identical and class-neutral across all classes.

**Controls and scales:** At both a seven-node reference scale and a modest
12-node expanded scale, compare fixed topology, pre-12I growth, random legal
growth, Luna-12I temporal growth and reversed/shuffled/timing-destroyed
evidence. Use seeds `0, 1, 2, 3, 4` and equal candidate exposure, mutation
budgets, bounds, workload and reset policy within each scale. The reference
scale preserves 12K capacities; the expanded scale uses bounded capacities of
10 edges, fan-in/out 3, candidate/history 12 and queue/event 24 with five
growth attempts. Serialize exact configurations before execution.

**Measurements and intervention:** Report four-class and per-class accuracy,
four-by-four confusion, handedness/direction pair confusion, class separation,
prediction loss/error activity, proxy energy and units, events, activations,
edges/utilization, path hops/delays, candidate exposure, mutations,
rejections, fan-in/out pressure, class-specific utilization and causal
shortcut evidence. Calculate accuracy/resource and prediction/resource
summaries without making them permanent objectives. Retain the 12K learned-edge
removal replay and compare routed traces, downstream state/output,
classification, prediction, energy and path delay. Investigate the 12K
prediction-loss increase without redesigning the predictor.

**Evidence and gate:** Focused tests must cover deterministic four-class
generation, matched inward/outward pairs, label and boundary-event isolation,
same-seed replay, equal bounds, four-class readout, temporal-order intervention,
consistent energy/prediction metrics and causal edge removal. The handoff must
separate `OBSERVED`, `INFERRED` and `HYPOTHESIZED` evidence and classify all
validation as passed, failed, not run or not applicable. Gates are `PASS`,
`PASS WITH FOLLOW-UP`, `NOT SUPPORTED`, `INCONCLUSIVE` and `BLOCKED` as
defined in the 12L specification. Any result returns to Luna-0; no A14
promotion, permanent energy/prediction formula, real-data claim, hardware
acceptance or successor authorization follows automatically.

## Luna-12M - Edge Lifecycle, Route Utilization, and Competing-Path Instrumentation

**Authorization:** Created and executed by Luna-0 at baseline
`7f8ea2df5896d3ea7cd7d41a4f1bd8298c0dc015` after the corrected Luna-12L
direction/decay review. This is an `OBSERVATION`, `VERIFICATION` and
`IMPLEMENTATION` milestone; it does not change A01-A15 or authorize a
successor.

**Purpose:** Instrument existing bounded topology and event routing so offline
analysis can distinguish shortcut creation, first/last use, route coexistence,
traffic crossover, pruning and replacement where supported. Global paths and
labels remain offline only.

**Boundary and gate:** The optional observer uses endpoint-plus-generation edge
identities, bounded ring buffers and saturating counters. It must preserve
event traces, timestamps, neuron/predictor state, routing, structural choices,
energy, eligibility and classifier results. `PASS` requires lifecycle and
traffic attribution, competing-path and decay-context evidence, deterministic
storage and ON/OFF equality. Missing replacement attribution or hardware
export may be `PASS WITH FOLLOW-UP`; execution influence, unboundedness or
ambiguous lifetimes is `BLOCKED`. Results return to Luna-0 and do not create a
direction/decay-gated shortcut experiment.

## Luna-12N - Temporal Direction and Intrinsic-Decay-Gated Shortcut Verification

**Authorization:** Luna-12N is a creation-only `EXPERIMENT` and
`VERIFICATION` milestone at baseline `0d91207ec5db0ab8011e0fc020cc9e4e20915428`,
created after corrected Luna-12M reached `PASS WITH FOLLOW-UP`. Creation does
not execute the experiment, amend A14, change the architecture contract,
authorize hardware acceptance or authorize a successor. Execution requires a
separate explicit assignment and returns to Luna-0.

**Question and hypotheses:** Determine whether locally legal edge direction and
intrinsic-neuron-decay-relative candidate preference increase genuinely used
causal shortcut yield under equal opportunity. H1 tests current versus
reversed orientation, H2 tests local decay-relative separation versus no decay
preference, and H3 tests their combination. A new correlated edge is not a
shortcut unless measured route use and causal compression are both present.

**Policy matrix:** Compare current/no-decay, reversed/no-decay,
current/decay-aware, reversed/decay-aware, random legal growth and fixed
topology. Preserve the same candidate pair for direction intervention where
legal; document an equivalent legal comparison when literal reversal is not
valid. Use seeds `0..4` and a predeclared finite set of decay-relative regimes;
do not tune global timing thresholds after inspecting outcomes.

**Locality and measurement:** Runtime policy inputs are limited to local event
timestamps, elapsed time, the neuron's own decay parameter/residual state,
local candidate evidence and legal local edge state. Global path analysis is
offline only. Use corrected Luna-12M `TPCN-EDGE-2` phase-scoped traffic,
endpoint-plus-generation lifecycle, candidate/rejection, pruning and decay
records. Measure exposure, attempts, admissions, rejection reasons, fan-in/out
and capacity, old/new route traffic, hop/cumulative-delay/arrival changes,
prediction/error, proxy energy, events and activations. Report static and used
shortcut yield separately and run matched present/remove/identical-replay
causal interventions.

**Boundary:** Do not change pruning, protection, persistent edge strength,
utility or eligibility, add a permanent threshold, inject labels or global
topology, add genetic hyperparameters or a micro-network, redesign the
classifier, modify A14 or claim hardware equivalence. Record premature-removal
protection and inherited-parameter ideas only as future research notes if
direct evidence warrants them. The result gates are `PASS`, `PASS WITH
FOLLOW-UP`, `NOT SUPPORTED`, `INCONCLUSIVE` and `BLOCKED`; all results return
to Luna-0 and no successor is authorized.

## Luna-13A - Stage-0 Software Reference Invariant Closure

**Authorization:** Luna-13A is a CPU-only `IMPLEMENTATION` and `VERIFICATION`
milestone created from the Luna-0 independent review of the corrected
Luna-12N work at reviewed checkpoint
`fdda3b59014109ce5aac6c5b2c9690b02acf85e9`. The reviewed result is
**PASS WITH FOLLOW-UP — MEASUREMENT CORRECTED, EFFICACY STILL UNESTABLISHED**.
Luna-12N established corrected configured-versus-actual accounting, independent
metadata controls, replay-measured arrivals, weighted cumulative-delay paths,
explicit event-budget status and strengthened provenance. Its synthetic fixture
showed score/rank changes but no different admitted edge set or final graph;
external prediction improvement, classification improvement, resource
efficiency and general temporal-learning superiority remain unestablished.

The sequence is explicit:

```text
Luna-12N corrective
  -> Luna-0 review
  -> Luna-13A Stage-0 invariant closure
  -> Luna-0 independent Stage-0 review
  -> determine whether a next Luna is authorized
```

Luna-13A closes software-reference integration blockers in four bounded areas:
classifier temporal monotonicity and stale-finalization atomicity, a declared
reward-delivery contract, projected structural-capacity rejection semantics,
and bounded recurrent execution. It is not a temporal-policy efficacy
experiment, dataset benchmark, GPU milestone or FPGA/FPAA equivalence test.
The assignment explicitly permits execution without a dedicated GPU and does
not require CUDA, GPU visualization, FPGA hardware or FPAA hardware. Optional
CUDA skips do not block it.

The reward-delivery behavior is a mandatory pause point. Luna-13A must inspect
current production behavior, documentation and tests and must not invent the
contract. It must either establish retry-idempotent logical delivery with
bounded identity retention or repeated-application delivery with obsolete
exactly-once claims removed. If repository authority remains contradictory, the
reward portion stops with **REWARD CONTRACT DECISION REQUIRED** and returns a
decision packet covering both models, affected files, bounded-state and replay
consequences. Safe non-reward Stage-0 work may continue, but the assignment
remains blocked.

The handoff must use
`workflow/handoffs/stage0-invariant-closure-Luna-13A.md` and include exact
revision/tree and worktree state, classifier before/after evidence, reward
disposition, projected-capacity and rejection-reason evidence, recurrent budget
semantics for budgets `1`, `2`, `8` and `64`, focused and full CPU validation,
remaining blockers and readiness for Luna-0 independent review. Terminal
statuses are constrained to the five statuses in the Luna-13A agent contract.
No Luna-13B is authorized by this entry. The likely future controlled
temporal structural-selection experiment remains contingent on Luna-13A and
the independent Luna-0 Stage-0 review.

### Luna-13A reward-contract resolution - 2026-09-29

The project owner selected **MODEL A — RETRY-IDEMPOTENT LOGICAL REWARD
DELIVERY**. `RewardSignal.message_id` is the explicit stable logical identity;
`RewardMessage.message_id` may provide it, and otherwise the existing
`RewardMessage.credit_id` is used as the stable identity. `EligibilityLedger`
owns a bounded FIFO retention window of accepted identities, default capacity
64 and configurable per ledger. Duplicate delivery within that window returns
`duplicate` without advancing the ledger clock, decaying traces or changing
credit. Distinct IDs apply independently even when all numeric and attribution
fields are equal. Reset clears identities and traces; deterministic FIFO
eviction permits a post-eviction identity to apply again. The guarantee is
bounded at-most-once credit application within one ledger scope, not permanent
global exactly-once processing.

Luna-13A implementation status is **PASS WITH FOLLOW-UP — READY FOR LUNA-0
STAGE-0 REVIEW**. Focused reward tests cover first delivery, immediate and
many duplicate retries, distinct equal-valued IDs, identical fields with
different IDs, deterministic replay, reset, bounded retention, FIFO eviction,
post-eviction behavior and independent eligibility expiry. The prior Luna-11
duplicate-application assertion is amended as historical evidence and now
expects retry suppression; intentional repeated reinforcement uses distinct
message IDs. Luna-13A returns to Luna-0 for independent verification. Luna-13B
remains unauthorized.

### Luna-0 independent review - 2026-09-29

This section records the pre-resolution review at revision
`047d2dd59905934a5100dcafb791835e93708b37`; the reward finding below is
historical and is superseded by the owner decision and implementation recorded
in the preceding resolution section.

**Reviewed revision:** `047d2dd59905934a5100dcafb791835e93708b37`, pushed as
`origin/main`; the source tree was clean at review time. The Luna-13A handoff
is `workflow/handoffs/stage0-invariant-closure-Luna-13A.md`.

**Independent result:** **BLOCKED — REWARD CONTRACT DECISION REQUIRED**.

- **Classifier:** PASS. An independent probe with START at `0`, activity at
  `8`, and direct stale finalization at `5` rejected before mutation. Time,
  active state, scores, result, character index and committed result state
  were unchanged. Equal-time, future-time and dispatched finalization agreed
  with direct semantics.
- **Reward contract:** BLOCKED. Independent delivery of the same
  `RewardSignal` applied credit twice. `RewardSignal` exposes only `reward`,
  `trace_id` and `prediction_id`; it has no delivery identity. The Luna-8
  handoff still claims bounded `message_id` retention, while the production
  implementation and adversarial test assert repeated application. Luna-0
  does not select Model A or Model B here.
- **Structural admission:** PASS. Independent jointly-invalid fan-in and
  fan-out batches, edge-capacity exhaustion, atomic topology preservation,
  deterministic public causes, and observer ON/OFF equivalence all passed.
- **Recurrence budget:** PASS for the canonical `execute_bounded` path.
  Positive-delay loop probes at budgets `1`, `2`, `8`, and `1` reported the
  exact processed budget, one pending event, `budget_exhausted`, and
  `completed=False`; finite work reported `completed=True`. No global neural
  timestep was introduced. A legacy Luna-12J efficacy replay still uses a
  manual bounded loop without returning termination status; this is recorded
  as follow-up evidence and is not silently promoted as canonical execution.
- **Regression:** The independent temporal/runtime/credit/topology slice
  passed `109` tests. The complete CPU suite passed `234` tests with `1`
  optional CUDA/GPU skip, which is not a failure. `compileall` and
  `git diff --check` passed. Luna-12H and Luna-12N corrective tests passed;
  Luna-12N is not reinterpreted as decay efficacy evidence.
- **Architecture conformance:** Core A01/A02/A03/A04/A07/A08/A11/A15
  behavior checked here remains conformant for the reviewed paths. Reward
  identity semantics remain unresolved, and Luna-12J's legacy replay status
  reporting should be normalized before broader reuse.

### Luna-0 independent Stage-0 review - 2026-09-29 - resolved reward contract

The post-Model-A review was performed independently against published
implementation revision `fba6e4de5fb93b150f6a7e7e545622d48ae7b3c5` and the
clean review baseline `db459c1e6dff8b90f74288a67e898552c12dc85f`.

**Independent result:** **PASS WITH FOLLOW-UP - STAGE-0 READY.**

- **Reward identity attack matrix:** PASS. Direct adversarial replay verified
  duplicate suppression without clock or credit mutation, including a valid
  stale timestamp; distinct equal-valued identities applied independently;
  FIFO eviction reopened an evicted identity; reset cleared identity scope;
  identical IDs were independent across ledgers; fallback and explicit
  `RewardMessage` identities mapped as documented; deterministic replay
  matched across fresh ledgers; and 1,000 accepted identities never exceeded
  a four-entry retention window.
- **Stage-0 preservation slice:** PASS, `127` passed.
- **Full CPU regression:** PASS, `242` passed and `1` optional CUDA/GPU test
  skipped. Compilation and `git diff --check` passed.
- **Documentation finding:** The Luna-13A handoff had stale pre-Model-A
  counts and a pending tree-state phrase; these were corrected in the review
  publication. No production-code defect was found in the identity semantics.
- **Architecture:** A11 is conformant as bounded at-most-once credit
  application within one ledger retention scope. No ACP is required and no
  permanent global exactly-once claim is made.

The legacy Luna-12J manual replay termination-status follow-up remains open and
non-gating. Stage-0 is independently reviewed as ready at the published
checkpoint `ecb3f412b55d6978c5551798900cb1bacf76a238`: classifier temporal
monotonicity, bounded reward identity/idempotency, projected structural
admission and bounded recurrent execution passed; the Stage-0 slice recorded
`127 passed`, and the full CPU suite recorded `242 passed, 1 skipped`. The
optional CUDA/GPU skip is non-blocking. Luna-13B creation is now authorized,
but execution still requires its own explicit assignment and independent
Luna-0 review.

## Luna-13B - Causal Local Temporal Structural Crossover

**Authorization boundary:** The authoritative sequence is:

```text
Stage-0 Luna-0 closure
  -> Luna-0 creates Luna-13B contract
  -> Luna-13B executes
  -> Luna-0 independently reviews Luna-13B
  -> determine whether Luna-13C is authorized
```

Creating the contract does not execute Luna-13B. Luna-13B is a CPU-only
`EXPERIMENT` and `VERIFICATION`; CUDA, GPU visualization, FPGA and FPAA are
not required. Luna-13C remains unauthorized until the independent Luna-0
review explicitly determines otherwise.

**Scientific question and gate:** Determine whether actual causally observed
local temporal evidence produces a predicted decay-dependent structural
admission decision when finite capacity forces competing candidates to contend
for exactly one available slot. Luna-12N showed score/rank sensitivity but no
admitted-edge or final-graph difference; Luna-13B tests that missing causal
structural-selection step.

Candidate evidence must come from runtime observations available to the local
decision component, with provenance for source, timestamps, elapsed intervals,
local state/residual, decay, score and decision time. A frozen analytic
crossover must predict opposite winners before held-out evaluation. At least
two equally exposed candidates must compete for the one slot, and the final
graph must reveal the selected edge. Reports must distinguish score, rank,
admitted-edge and final-graph changes. Labels, future observations, global
statistics and hand-authored endpoint timing tables are excluded from the
decision.

Required controls include ordinary and decay-informed association, reversed and
time-shuffled observations, random/score-shuffled selection, fixed topology,
uniform intervals, neutral/zero decay where valid, mirrored/relabelled
fixtures, exact/near ties and deterministic replay. Matched capacity,
candidate exposure, bounded execution and rejection accounting are mandatory.
Every run reports budget, processed/pending work, queue peak where available,
termination reason and `completed` or `budget_exhausted`; exhaustion is not a
successful observation.

The required handoff is
`workflow/handoffs/causal-local-temporal-crossover-Luna-13B.md`, using the
standard template and separating `OBSERVED`, `INFERRED` and `HYPOTHESIZED`
claims. All results return to Luna-0. Scores/ranks without a changed admitted
edge must be reported as `SCORING/RANK SENSITIVITY CONFIRMED — STRUCTURAL
CROSSOVER NOT ESTABLISHED`. Luna-13B cannot authorize Luna-13C.

### Luna-0 independent review of Luna-13B - 2026-09-29

Reviewed implementation and published artifact revision
`816929fa097e049ce7d82a1f7c63fb9cc4e8bd3f` after synchronizing with
`origin/main`. The review tree was clean and `HEAD == origin/main` at review
start. The contract is `.github/agents/luna-13b.agent.md`, the execution
handoff is `workflow/handoffs/causal-local-temporal-crossover-Luna-13B.md`,
and the artifacts are under
`artifacts/causal-local-temporal-crossover-13b/`.

**Independent result:**
**PASS — LUNA-13B CAUSAL STRUCTURAL CROSSOVER INDEPENDENTLY VERIFIED**.

- Runtime-local evidence passed. Candidate residuals and scores were derived
  from routed finite-delay events and canonical-neuron local state; timestamps,
  elapsed intervals, source events and decision times were reconstructable.
- The production equation reproduced the frozen crossover
  `mu* = 0.07833747196936626`. Low/high scoring decay produced opposite ranks,
  admitted edges and explicit final edge sets under one remaining slot.
- One-slot capacity passed: two locally valid candidates competed from zero
  edges, one edge was grown, and the other was rejected with `edge_capacity`.
- Relabeling and mirroring followed semantic temporal evidence rather than
  identifier order. Exact ties used the declared deterministic identifier rule;
  near-boundary replay was deterministic.
- Reversed, shuffled, uniform, neutral, random, score-shuffled and fixed
  controls behaved according to their declared purposes. Score-shuffled
  preserved raw rank while changing the selected edge, demonstrating why
  structural choice was separately measured.
- Scoring decay and execution decay were independently configurable. The
  primary crossover held execution decay fixed; the review also ran an
  execution-decay factorial comparison and makes no claim that runtime decay
  is irrelevant.
- Primary and control runs completed without budget exhaustion. The review
  reproduced `7` processed events, `0` pending events and peak queue occupancy
  `4`; increasing the budget to `30` did not change the result.
- Stage-0/Luna-12H/Luna-12N preservation passed. The review slice passed `135`
  tests and the full CPU suite passed `250` with `1` optional CUDA/GPU skip;
  compileall, diagnostics and `git diff --check` passed.

The result is narrow: Luna-13B establishes a bounded software-reference
mechanism in which causally observed local temporal evidence can reverse a
decay-sensitive candidate ranking and change one-slot structural admission and
the final graph. The controlled intervals are finite runtime fixture delays;
this review does not establish task usefulness, classification or prediction
improvement, energy efficiency, scalability, hardware equivalence, biological
plausibility or general superiority. Luna-12J's manual replay termination
status remains a non-gating follow-up. Luna-13C is not authorized. A future
contract may be proposed for causal usefulness of a learned edge against an
external task target, subject to a new owner request and Luna-0 review.

## Luna-13C - Useful Causal Effect of Learned Temporal Structure

**Authorization boundary:** The lifecycle is:

```text
Luna-13B independent PASS
  -> Luna-0 creates Luna-13C contract
  -> Luna-13C executes under a separate explicit assignment
  -> Luna-0 independently reviews Luna-13C
  -> determine whether any successor is authorized
```

The independent Luna-13B review is recorded at review revision
`04f2088725c71eb20b808ae07dbd99a02d4cd459`, reviewing implementation revision
`816929fa097e049ce7d82a1f7c63fb9cc4e8bd3f`. It established runtime-local
causal evidence, the predicted decay-sensitive crossover, rank and admitted-
edge reversal under one-slot competition, final-graph change, controls,
determinism and bounded execution. It did not establish task usefulness,
external prediction or classification improvement, resource efficiency,
scalability or hardware equivalence. Luna-12J's manual replay termination
status issue remains non-gating.

Luna-13C is a CPU-only `EXPERIMENT` and `VERIFICATION` contract. It reuses the
verified Luna-13B structural-selection mechanism and asks whether the learned
edge produces a useful effect on a fixed external task target independent of
the topology being evaluated. Prefer the smallest bounded temporal-order,
interval-dependent or delayed-cue task; defer the full A-Z benchmark until
the simple causal mechanism is established. CUDA, GPU visualization, FPGA and
FPAA are not required, and an optional CUDA skip is non-gating.

Freeze the task, topology-independent external target, decision rule/loss,
primary metric, practical effect threshold, interventions, seeds and budgets
before held-out evaluation. Freeze the learned structural state once, then
clone or restore that identical state for paired conditions using the same
inputs, targets, initialization and execution resources. Require:

- learned edge present;
- targeted removal of only the claimed learned edge;
- exact restoration of the same source, target, delay, strength and
  computation-affecting metadata;
- sham metadata/no-op intervention;
- irrelevant or unused edge removal;
- fixed topology with no growth;
- equal-budget random growth with explicit seeds; and
- a fixed useful-edge positive control.

The external target must not be generated from edge identity, path length,
current-topology activation, candidate score or the model's own prediction.
Measure topology, internal trace and external task outcome separately. The
causal gate requires present-graph benefit, material targeted-removal loss,
exact restoration within tolerance, null or smaller sham/irrelevant effects,
an expected positive-control result, matched inputs/targets/resources and
completion without silent budget exhaustion. A failed positive control blocks
interpretation rather than proving learned-edge uselessness. Labels and
targets remain outside candidate generation, local scoring, structural
admission and core runtime state.

Every run records configured and processed events, pending events, termination
status, graph fingerprints, external metrics, target arrival/decision state
and proxy energy where available. Proxy energy is secondary and need not
decrease. The required handoff is
`workflow/handoffs/useful-causal-effect-Luna-13C.md`, using the standard
template and separating `OBSERVED`, `INFERRED` and `HYPOTHESIZED` evidence.
Validation covers all interventions and controls, fixed-target and matched-
input semantics, exact graph restoration, label/future isolation,
deterministic replay, held-out freeze and completion status, followed by
Luna-13B, Stage-0, Luna-12H, corrected Luna-12N, full CPU, compile/static,
diagnostic and `git diff --check` regressions. Results return to Luna-0.
Luna-13C must not authorize Luna-13D.

### Luna-0 independent review of Luna-13C - 2026-09-29

Reviewed implementation and artifact revision
`575c2407db21786b21d64cb57d640d2a1a940ac0` after synchronizing with
`origin/main`; the review started from a clean tree with matching `HEAD` and
`origin/main`. The review handoff is
`workflow/handoffs/luna-0-review-Luna-13C.md`.

- **External target valid:** the fixed targets are `on_time` for the short
  interval and `late` for the long interval, independent of topology. The
  default learned-present result is `2/2`; targeted removal is `1/2`; exact
  restoration is `2/2`; sham is `2/2`; irrelevant removal is `2/2`; fixed
  topology is `1/2`; seed-0 random growth is `1/2`.
- **Causal task effect reproduced:** target arrivals change from `(1.0, 2.0)`
  to no arrivals for the short case when `right -> target` is removed; exact
  graph restoration recovers the arrivals and result. All primary runs
  complete without budget exhaustion, and an event-budget increase to 30 does
  not change the result.
- **Follow-up limitations:** sham bypasses intervention machinery; fixed
  useful control is the exact learned edge rather than an independent edge;
  seed 1 random growth reproduces `2/2`; and the 13C label test repeats the
  same run rather than mutating labels. The checkpoint fingerprint is a
  metadata hash, not a serialized neuron/queue/eligibility checkpoint.
- **Preservation:** the independent focused slice passed `41` tests and the
  full CPU suite passed `255` with `1` existing optional skip. Compile,
  diagnostics and diff checks passed. No dedicated Stage-0 test file exists;
  this is recorded as not applicable rather than claimed as a separate pass.

**Decision:** **PASS WITH FOLLOW-UP — CAUSAL TASK EFFECT VERIFIED, NON-GATING
LIMITATIONS REMAIN**. The narrow supported claim is that, in this bounded
fixture, the edge learned through the verified Luna-13B mechanism causally
improves the fixed external outcome, with targeted removal reducing the
short-case result and exact restoration recovering it. This does not establish
general task utility, random-selection superiority, resource benefit,
scalability, hardware equivalence or biological equivalence. No A01-A15
clause changed, no ACP was created, and Luna-13D remains unauthorized. The
next action is project-owner direction for any follow-up contract, followed by
Luna-0 review.

### Luna-13C corrective evidence pass - 2026-09-29

The corrective pass at revision `685cd721f7ca108278aa2e3044b53d46981e5bbd`
used shared topology-rebuild machinery for sham, a distinct useful edge with
delay `0.5`, independent seeded random selection, and an actual evaluation
label-mutation attack. The corrected artifact records sham graph equality,
positive-control accuracy `2/2`, random seed 0 accuracy `2/2`, random seed 1
accuracy `1/2`, and unchanged structure/pre-output computation under relabeled
targets. Focused corrective validation passed `6` tests; the focused temporal
regression slice passed `42` tests.

The narrow causal task effect remains supported, but random growth reproduces
it for one independent seed. This is therefore `PASS WITH FOLLOW-UP — CAUSAL
TASK EFFECT ESTABLISHED, LIMITATIONS REMAIN`; no A01-A15 clause changed and
Luna-13D remains unauthorized.

### Luna-0 independent corrective re-review - 2026-09-29

The independent re-review synchronized clean `main` at revision
`09995add7643e63f61c45602922238e319965113`, with `HEAD == origin/main`.
The corrective artifact identifies source revision
`685cd721f7ca108278aa2e3044b53d46981e5bbd`, baseline
`ea60610b7ba637e05ee986ffde2864e529a08f2c`, and clean generation state.

The same-path sham was independently instrumented and passed: it rebuilt the
bounded graph through the intervention path, preserved the learned edge and
fingerprint, matched present traces, and scored `2/2`. The learned edge is
`right -> target, 1.0`; the distinct hand-designed positive control is
`right -> target, 0.5` and scored `2/2`. Random seeds independently produced
`right -> target`, `2/2` for seed 0 and `left -> target`, `1/2` for seed 1.
Label mutation preserved structural evidence, decisions, traces, event
counts, and completion state. Present/removal/restoration reproduced
`2/2 -> 1/2 -> 2/2`; only the short case changes, because removing the route
removes its deadline-meeting target arrivals.

The independent targeted bundle passed `124` tests; the full CPU suite passed
`256` with `1` skip; compileall, diagnostics, and diff checks passed; and
temporary artifact regeneration was byte-identical. The named Stage-0 file is
absent, so that check is not applicable; relevant reward, structural,
recurrent, classifier, runtime, Luna-12H, Luna-12N, and Luna-13B tests ran.
The checkpoint remains a metadata fingerprint over fresh reset/rebuild state,
not a serialized queue/eligibility/random-state clone. The two-case fixture
does not establish generalization, efficiency, scalability, hardware
equivalence, or random-growth superiority.

**Decision:** `PASS WITH FOLLOW-UP — CAUSAL EFFECT VERIFIED, BOUNDED
LIMITATIONS REMAIN`. Luna-13D was not created or executed; it is eligible for
later contract creation only by explicit project-owner authorization. The next
scientific boundary is a separately authorized finite-resource utility study
covering pressure, retention/pruning/replacement, and event/energy tradeoffs.

## Luna-13D - Finite-Resource Utility, Retention, and Capacity-Pressure Experiment

**Authorization boundary:**

```text
Luna-0 creates Luna-13D contract
  -> Luna-13D executes under a separate explicit assignment
  -> Luna-0 independently reviews Luna-13D
  -> determine whether any successor is authorized
```

The synchronized Luna-13C corrective review closed at final review revision
`df297c446856d07b2822702202bbb61e81cf38a4`, reviewing corrective source
`685cd721f7ca108278aa2e3044b53d46981e5bbd` in tree
`09995add7643e63f61c45602922238e319965113`. Its result was
`PASS WITH FOLLOW-UP — CAUSAL EFFECT VERIFIED, BOUNDED LIMITATIONS REMAIN`.
The narrow effect is retained; two task cases, one random reproduction,
generalization, efficiency, scalability and full-state checkpointing remain
limited or unproven.

Luna-13D is a CPU-only `EXPERIMENT` and `VERIFICATION` of finite-resource
utility, useful-edge retention, low-value pruning and capacity pressure. It
reuses Luna-13C's fixed external task semantics and causal learned-edge
provenance where practical. It separates task utility from events, queue peak,
proxy energy, latency and edge/capacity cost, and must not call silence
efficient when task utility is lost.

The scope is staged pressure over fan-in, fan-out, total edge capacity,
event/queue capacity and competing useful, distractor, unused and expensive
paths. Stages cover baseline utility, distractor pressure, below/near/full
capacity, declared pruning, post-pruning normal growth and an optional bounded
workload shift. Useful-edge lifecycle, pruning evidence/reasons, graph state,
capacity failures, queue rejections, budget exhaustion, task outcome, events,
proxy energy and latency remain observable. Fixed topology and genuine seeded
random growth are required controls.

Replacement is not automatically authorized. Luna-13D may test an existing
documented and tested atomic replacement policy only if one is already
authorized. Otherwise it is restricted to admission, coexistence, pruning and
later growth after legitimately freed capacity; it must not invent replacement
or a protected-edge lifetime. Any required architecture change returns as an
ACP/decision packet to Luna-0/project-owner review.

Every run requires configured/processed/pending events, queue peak where
available, termination reason and `completed` versus `budget_exhausted`.
Artifacts preserve revisions, fixture, capacity/pruning configuration, seeds,
external target, thresholds and resource units. CUDA is optional and
non-gating. The standard handoff is
`workflow/handoffs/finite-resource-utility-capacity-pressure-Luna-13D.md`.
Results return to Luna-0 for independent review. Luna-13D does not authorize
Luna-13E.

### Luna-0 independent review of Luna-13D - 2026-09-29

Reviewed implementation revision
`f11a44f24fa9ad84e111435ed0ae8390b41c49a6` from a clean synchronized tree
with `HEAD == origin/main`. The contract, implementation, tests, handoff and
both artifacts were present. Independent reproduction confirmed the fixed
external task, baseline/pruning/post-growth metrics, capacity reasons,
budget stability, random seeds, Luna-13C causal matrix, and byte-identical
artifact regeneration.

The Luna-0 review publication revision is `8449562`.

The review separates the findings. The useful `right -> target, 1.0` edge is
task-relevant and remains in the graph after pruning. The graph has three
edges before pruning and one afterward, releasing two actual edge-capacity
slots. `right -> relay` and `relay -> target` are admitted through ordinary
bounded growth without replacement. Baseline and immediate post-pruning both
remain `2/2` at 8 events and proxy energy `8.0`. Post-growth produces duplicate
target arrivals, changes the result to `1/2`, and uses 16 events and proxy
energy `16.0`; this is a utility regression, not an efficiency result.

Capacity accounting is valid: capacity 4 reaches `edge_capacity`, while
capacities 5 and 6 reject the final relay exit for `fan_in_full`. Budgets 24
and 48 reproduce the result. Random seed 0 selects the useful edge and scores
`2/2`; seeds 1-4 select the non-useful edge and score `1/2`. The Luna-13C,
13B, temporal and Stage-0-related regressions remain passing.

The pruning/retention mechanism evidence is invalid. The implementation
passes an endpoint-keyed literal score map to `prune_by_score`; declared
`pruning_utility_threshold` and `pruning_inactivity_threshold` do not control
eligibility. Changing the utility threshold from `0.0` to `100.0` leaves the
same edges pruned, and the fixed node tuple prevents a relabeling attack.
The removals and capacity release are observed, but useful-versus-low-value
local evidence did not cause the decision. The review status is therefore
`BLOCKED — PRUNING/RETENTION EVIDENCE INVALID`.

The next eligible boundary is a separately reviewed correction or experiment
with evidence-derived pruning, meaningful frozen thresholds and identity-
independent checks. Luna-13E is not created or authorized.

### Luna-13D corrective pass - 2026-09-29

The corrective pass started from Luna-0 review publication state
`89de90b183cd54f1ae24f433b6161f1b14c23c0e` and produced implementation
revision `9ae2fb6`. It preserves the independently valid prior findings:
the fixed Luna-13C task, real capacity release, normal post-pruning admission,
capacity rejection reasons, random seed behavior, and post-growth regression
from `2/2` at 8 events to `1/2` at 16 events.

The endpoint-keyed pruning score map was removed. Pruning now records bounded
runtime edge use count, last-use timestamp, inactivity age, observed utility,
observed cost and pruning score. Frozen semantics are:
`inactivity_age >= inactivity_threshold OR observed_utility < utility_threshold`;
inactivity equality is eligible and utility equality is retained. Eligible
edges are selected by lowest observed score, with a bounded maximum of two.
Threshold sweeps, relabeled IDs and mirrored task-source roles show decisions
follow measured evidence rather than endpoint names. The useful edge remains
retained; two zero-use stale edges are pruned and release two slots.

The corrected result is
`PASS WITH FOLLOW-UP — RETENTION/PRUNING ESTABLISHED, USEFUL ADAPTATION NOT
ESTABLISHED`. Resource efficiency remains unproven and relay growth still
degrades the fixed task. The corrected handoff and artifacts return to Luna-0
for independent review. Luna-13E is not created or authorized.

### Luna-0 independent review of corrected Luna-13D - 2026-09-29

Reviewed corrected implementation
`9ae2fb6574a4a45fa6a47c18e9aa7270bd4d3080` from synchronized published tree
`206a3b8463ef857db5e5d5b8d2679d7e877f3bab`. The worktree was clean and
`HEAD == origin/main`; the contract, corrected handoff, implementation, tests
and artifacts were present.

The prior blockers are closed for the tested fixture. Pruning eligibility uses
runtime route use count, last-use timestamp, inactivity age, observed utility
and observed cost; endpoint identity is not an input to the primary Boolean
decision. The declared rule is
`inactivity_age >= threshold OR observed_utility < threshold`, with inclusive
inactivity equality and strict utility inequality. All four OR combinations,
threshold boundaries, arbitrary relabeling and mirrored task-source roles were
independently reproduced. The useful edge is retained from four observed uses;
two zero-use stale edges are pruned and two real slots are released.

The valid prior resource/task distinction remains: baseline and immediate
post-pruning are `2/2`, 8 events and proxy energy `8.0`; relay growth is normal
bounded admission but changes the result to `1/2` at 16 events and energy
`16.0`. Resource efficiency and useful adaptation are not established.

Validation passed: corrected focused `10`, preservation bundle `100`, full CPU
suite `266` with `1` optional skip, compileall, diagnostics and diff checks;
corrected artifact regeneration is byte-identical. Final review status:
`PASS WITH FOLLOW-UP — RETENTION/PRUNING VERIFIED, USEFUL ADAPTATION NOT
ESTABLISHED`. The next question may examine harmful post-pruning admission;
Luna-13E is not created or authorized.

The final Luna-0 review publication revision is
`becf38952fe5c1cf738dd875246b672f82836093`.

### Luna-13E creation - 2026-09-30

The corrected Luna-13D state was independently reviewed with final published
repository state `b7e3bdc6028381a5fa6912c0212aff79528beae1`. The review status
is `PASS WITH FOLLOW-UP — RETENTION/PRUNING VERIFIED, USEFUL ADAPTATION NOT
ESTABLISHED`:

- evidence-based retention/pruning is established, including measured route
  evidence, inclusive inactivity eligibility, strict utility comparison,
  relabeling and mirrored-role preservation;
- useful post-pruning adaptation is not established and resource efficiency is
  not established;
- normal bounded post-pruning growth can degrade the fixed task from `2/2`, 8
  events and energy `8.0` to `1/2`, 16 events and energy `16.0`.

Luna-0 creates Luna-13E, **Post-Pruning Admission Quality and Harmful-Growth
Discrimination Experiment**:

```text
Luna-0 creates Luna-13E contract
  -> Luna-13E executes under a separate explicit assignment
  -> Luna-0 independently reviews Luna-13E
  -> only then determine whether Luna-13F is eligible
```

Luna-13E is a CPU-only experiment and verification of whether existing local,
causal, bounded evidence available before mutation can distinguish a beneficial
candidate from a harmful candidate under true one-slot competition. It must
reproduce the corrected Luna-13D harmful-growth baseline first, freeze
beneficial/harmful ground truth for external evaluation only, and record
field-level pre-admission evidence provenance. Endpoint identity, labels,
future events, future task outcomes and post-hoc oracle information may not
drive admission. Fixed/no-growth and seeded random controls are required.

If current architecture cannot make the distinction without new utility-aware
admission state or another architecture change, Luna-13E must stop and return
an architecture-change decision packet. It must not add a hidden mechanism,
alter pruning, invent probation/rollback or claim utility prediction. CUDA is
optional and non-gating. All applicable boundedness, locality, label-isolation,
determinism and regression checks remain required.

Luna-13E returns to Luna-0 for independent review. It does not authorize,
create or dispatch Luna-13F. No A01-A15 clause or ACP status changes by this
workflow entry.

### Luna-13E independent review - 2026-09-30

Luna-0 independently reviewed Luna-13E at implementation revision
`0a53b01b398d461eac3a962431b9ffcdae459e55`, based on synchronized published
revision `dd241ec9ee7af7456ae70bae2192d4237dab5d21` and the corrected artifact
  metadata committed during review. The review package revision is
  `7faf8d3f1c82927304875bb6263219d5954a463d`. The review status is:

**PASS WITH FOLLOW-UP — HARMFUL GROWTH AVOIDED, GENERALITY NOT ESTABLISHED**

- G and H were individually legal at the same decision point with exactly one
  relevant free edge slot. The canonical scorer used local `CandidateEvidence`
  scores `3.0` and `0.0`, selected G, and remained independent of candidate
  presentation order, relabeling and mirrored endpoint roles.
- Independent held-out replay measured no-growth `2/2` with 8 events and
  proxy energy `8.0`, G `2/2` with 12 events and proxy energy `12.0`, and H
  `1/2` with 12 events and proxy energy `12.0`. G therefore preserved task
  utility while avoiding the harmful candidate; it did not improve the task
  over no-growth and was not resource-efficient relative to no-growth.
- Equalized evidence selected by deterministic tie-breaking only. Future-event
  and external-label mutation controls preserved the admission decision.
  Reward, prediction/error and predicted total-cost evidence were unavailable;
  propagation delay was available but not used in the score.
- The score-driving observations are a bounded controlled fixture, not a
  demonstrated general runtime predictor. General utility prediction,
  workload-shift robustness, resource efficiency and hardware equivalence
  remain unestablished. Current admission still has no abstention threshold;
  no utility-aware production mechanism was added.
- The stale frozen H metadata (`0/2`) was corrected to the observed `1/2` in
  the review revision. No A01-A15 clause changed, no ACP was required, and
  Luna-13F remains unauthorized. A successor may be considered only after a
  separate project-owner authorization.

### Luna-13F creation - 2026-09-30

The final synchronized reviewed state is
`8c41267e47bc0543ff9f05e994dc7ea086b23e36`. Luna-13E's independent review
package is `7faf8d3f1c82927304875bb6263219d5954a463d`, reviewing corrected
implementation `0a53b01b398d461eac3a962431b9ffcdae459e55`. The review status
is **PASS WITH FOLLOW-UP - HARMFUL GROWTH AVOIDED, GENERALITY NOT
ESTABLISHED**.

The review established only that fixture-controlled bounded observations
selected G over H in the tested one-slot fixture. No-growth remains `2/2` at
8 events and energy `8.0`; G remains `2/2` at 12 events and energy `12.0`; H
remains `1/2` at 12 events and energy `12.0`. G therefore avoids harmful
growth but provides neither task improvement nor resource benefit over
no-growth. Runtime-generated candidate evidence remains unestablished.

Luna-0 creates Luna-13F, **Runtime-Generated Local Candidate Evidence
Experiment**:

```text
Luna-0 creates Luna-13F contract
  -> Luna-13F executes under a separate explicit assignment
  -> Luna-0 independently reviews Luna-13F
  -> only then determine whether Luna-13G is eligible
```

Luna-13F is CPU-only and asks whether ordinary runtime neuron/event activity
generates bounded, candidate-specific local evidence before admission. The
primary chain is runtime events -> local state -> accumulated evidence -> the
unchanged canonical scorer -> true one-slot decision -> held-out outcome.
Fixture-keyed score tuples, G/H lookup tables, candidate-role flags,
experiment-side timing or score injection, labels, future outcomes and
endpoint-oracle evidence are prohibited. Candidate identifiers may index
bounded state but may not determine evidence values.

The contract requires runtime provenance, evidence timestamps no later than
the decision, bounded state and reset/eviction semantics, matched G/H
exposure, temporal controls, relabeling, mirrored roles, future/label
isolation, candidate-order independence and no-growth reporting. The current
architecture must be audited first. If existing mechanisms cannot generate
the evidence, Luna-13F must stop and return an architecture-change decision
packet; it may not silently add a learning subsystem or new candidate
semantics. CUDA is optional and non-gating.

Luna-13F returns to Luna-0 for independent review. No A01-A15 clause changes,
no ACP is created by this workflow entry, and Luna-13G is not authorized.

### Luna-13F execution authorization - 2026-09-30

Luna-0 reviewed the committed Luna-13F contract and prerequisite evidence at
authorization baseline `4f4129f3d9eda736fe1c2434b79e21d387e2fedc`. The
repository was synchronized with `origin/main`, on `main`, and clean with
`HEAD == origin/main`.

The prior Luna-13B causal crossover, Luna-13C bounded external causal effect,
corrected Luna-13D evidence-based retention/pruning, and Luna-13E harmful-
growth-avoidance review gates are sufficiently closed for this bounded
follow-up. Luna-13E's remaining limitation is the use of fixture-controlled
score-driving observations rather than demonstrated organically runtime-
generated candidate evidence.

**AUTHORIZED - LUNA-13F EXECUTION PENDING.** Luna-13F may now execute from
authorization revision `4f4129f3d9eda736fe1c2434b79e21d387e2fedc` or a later
synchronized revision containing no incompatible architecture or workflow
changes. The authorized question is whether ordinary event-driven runtime
activity generates bounded candidate-specific local evidence for the unchanged
canonical scorer under true one-slot competition.

The primary decision remains prohibited from using fixture-keyed G/H scores,
candidate-role tables, endpoint-specific tuples, expected-winner metadata,
labels, held-out outcomes, or experiment-side score injection. The existing
architecture must be audited first; if it cannot generate sufficient evidence,
Luna-13F must stop with its architecture-change decision packet and must not
add production semantics silently. Execution remains CPU-only; optional CUDA
skips are non-gating. Luna-13F must return to Luna-0 for independent review.
Luna-13G remains unauthorized.

### Luna-13F independent review - 2026-09-30

Luna-0 independently reviewed the completed Luna-13F implementation at
`0ba668ebe6cccd52fb0953638e1159090a79221e` after refreshing `origin/main`.
The review was performed on `main`; `HEAD` was one commit ahead of
`origin/main` (`f0821bd5eb0441ea892c463cbbcf173c80d09be6`), and the worktree
was clean before review edits.

The terminal status is:

**BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION CONFIRMED**

The earliest invalid dependency is the Luna-13F `_schedule` path: it uses
`beneficial_role` and `harmful_role` to assign three short candidate events to
G and one long event to H. The runtime neuron and bounded temporal policy are
real, and the unchanged canonical scorer is called, but the informative value
is assigned by the experiment fixture before runtime processing. The review
also confirmed that post-decision events change the accumulated score and
admission, held-out route timestamps begin before the decision, and an
event-budget-exhausted run can still admit G with pending events.

The existing architecture is **partially sufficient**: bounded local policy
state, neuron state and the canonical scorer already exist. No architecture
change or ACP is required by this review. The implementation may receive a
separately authorized corrective pass under the existing contract:

**LUNA-13F CORRECTIVE PASS ELIGIBLE UNDER EXISTING CONTRACT**

This eligibility does not authorize execution. The corrective scope must use
matched non-role-authored exposure, freeze pre-admission evidence, place
held-out execution strictly later, reject incomplete runs for scientific
admission, and complete the required controls. The original unqualified 13F
artifact pair lacks a terminal-status field; the verified artifact pair and
resumption audit truthfully report the blocked status. A01-A15 and ACP status
remain unchanged. No corrective work was executed by this review, and
Luna-13G remains unauthorized.

### Luna-13F corrective execution authorization - 2026-09-30

Following the independent review above, Luna-0 explicitly authorizes a
corrective Luna-13F pass under the existing `.github/agents/luna-13f.agent.md`
contract. This is a corrective execution boundary, not a new Luna contract,
architecture promotion or successor authorization.

The authorized corrective scope is limited to the identified experiment
violations: remove beneficial/harmful-role knowledge from evidence scheduling;
freeze evidence before the structural decision; place held-out events after
the decision in actual timestamps; reject incomplete-budget admissions;
construct a genuine runtime-generated evidence-equalization control; and run
the required missing or invalid controls. Controlled event schedules remain
allowed when they do not encode later held-out usefulness.

The corrective pass must not add utility memory, probation, rollback,
speculative edges, a reward channel, global task utility, an oracle cost
predictor, global candidate history, protected candidate classes or new
architecture semantics. If an existing mechanism is insufficient, Luna-13F
must stop and return **BLOCKED - ARCHITECTURE CHANGE REQUIRED FOR RUNTIME
EVIDENCE**. A positive result is not required; ties, non-predictive evidence
and negative results are valid outcomes. The first Luna-13F execution remains
blocked, the architecture remains unchanged, and Luna-13G remains
unauthorized.

The next action is Luna-13F corrective execution, followed by another
independent Luna-0 review. No corrective Luna-13F execution was performed as
part of this authorization/publication task.

### Luna-13F corrective independent review - 2026-09-30

Luna-0 independently reviewed corrected implementation revision
`dcee582fa8fb347f578793c2ef383bd936e83234` on synchronized `main` with
`HEAD == origin/main` and a clean worktree at review start. The committed
focused output reports 10 passed, the preservation output reports 62 passed,
and the full CPU output reports 286 passed with 1 skipped. No experiment was
rerun after the user froze execution.

The terminal status is:

**BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION**

The schedule body is neutral with respect to the two role fields, but the
complete dependency chain is not. `_candidate_edges()` maps G to
`beneficial_role`, `_base_edges()` uses the same role mapping, and held-out
topology construction reuses those helpers. Therefore the short-association
motif is still assigned to the endpoint already designated useful by the
fixture. The reported 4.0/0.0 values are bounded source-local
`TemporalAssociationPolicy` association counts, not independent utility
evidence. The required A/B blinding and valid mirrored-role test were not run.

The five audit not-run items are all classified **REQUIRED BUT MISSING**:
external-label mutation, locality attack, neutral-decay sweep,
candidate-saturation/reset/eviction, and valid mirrored roles. The audit's
13 passed, 0 failed, 5 not-run total therefore cannot support a scientific
PASS, and its role-dependency check inspected only `_schedule`.

The artifact also records executed revision `3379403a8b58649a85c2604ba3044e55e4fe99e9`,
not the corrected commit under review. The held-out timestamps are hard-coded
metadata while route traces reset at 0.0, so cross-phase chronology is not
independently established. No A01-A15 clause changed and no ACP is required.
The existing runtime may be sufficient for a later corrected experiment, but
that requires explicit project-owner authorization and another Luna-0 review.
Luna-13G remains unauthorized.

### Luna-13F blinded-mapping corrective authorization - 2026-09-30

Following the independent review above, Luna-0 authorizes **one additional
Luna-13F corrective pass under the existing `.github/agents/luna-13f.agent.md`
contract**. This is an experiment-level authorization only: it does not create
a new Luna-13F contract, execute the experiment, change A01-A15 or authorize
Luna-13G.

The current partial result is preserved: ordinary runtime activity generates
bounded source-local association evidence and the unchanged canonical scorer
consumes it. The remaining blocker is the pre-evaluation mapping
`beneficial_role -> candidate/topology assignment -> G`. The corrective pass
must remove `beneficial_role` and `harmful_role` from every candidate endpoint,
base topology, neutral schedule, ordering, evidence and scoring path. Those
fields may remain only in post-hoc utility reporting.

Use neutral candidate identities such as `candidate_A` and `candidate_B`,
freeze a predeclared seeded mapping before held-out evaluation, and run at
least two independent endpoint/motif permutations with identical schedule
generation. Compute runtime evidence, canonical scores and admission before
assigning task-preserving or task-harming descriptions. Preserve the valid
runtime-events -> bounded association-state -> canonical-score chain and
identify whether 4.0/0.0 is caused by count, interval, ordering, decay or
another canonical state variable.

The five outstanding audit controls remain mandatory unless the existing
contract independently demonstrates conditional inapplicability:
`external_label_mutation`, `locality_attack`, `neutral_decay_runtime_sweep`,
`candidate_saturation_reset_eviction` and `valid_mirrored_roles`. The pass must
return complete artifacts and validation to Luna-0 for independent review.
No architecture change is currently required. If the blinded experiment
requires new runtime semantics, it must stop with the authorized architecture-
change status and decision packet. Luna-13G remains unauthorized.

### Luna-0 independent review of blinded-mapping corrective Luna-13F - 2026-09-30

Luna-0 independently reproduced the reported P0/P1 decisions and held-out
outcomes from the dirty corrective worktree. The focused suite passed 10 tests
and the preservation slice passed 62 tests, but the review found that the
required information-boundary controls are not independently executed.

- P0 maps `candidate_A` to `relay` and selects it with runtime evidence
  `4.0` versus `0.0`; its held-out result is `2/2`.
- P1 maps `candidate_A` to `noise` and applies the same short/long motif rule;
  it selects the same neutral candidate and its held-out result is `1/2`.
- The runtime association count and canonical scorer chain are reproduced, but
  `external_label_mutation` and `locality_attack` are declarative artifact
  fields rather than mutation attacks. Future events are sliced out before
  execution, and held-out timestamps are hard-coded metadata over a fresh
  time-zero evaluator rather than one continuous runtime chronology.
- No complete contract-audit artifact exists for the corrected run. The
  saturation control demonstrates bounded rejection/reset, but not eviction;
  the budget tests cover an incomplete run, not the required boundary matrix.

Final review status: **BLOCKED - REQUIRED CONTRACT CONTROLS NOT EXECUTED**.
The raw execution remains a negative utility-prediction result, not a verified
Luna-13F closure. No A01-A15 clause or ACP status changed, no architecture
change is authorized, and Luna-13G remains unauthorized. A separately
authorized evidence-control repair is required before closure; do not add a
utility predictor or issue Luna-13G from this review.

### Luna-13F contract-control completion authorization - 2026-09-30

Luna-0 published the independent blinded-experiment review at revision
`c05015527063053ee789d0fc19ae21a02627f319`. The review independently
reproduced the central negative result: evidence-driven `candidate_A` was
selected in both mappings, with held-out results P0 `2/2` and P1 `1/2`.
The scientific observation remains valid but is not yet contract-closed.

The terminal review status is:

**BLOCKED - REQUIRED CONTRACT CONTROLS NOT EXECUTED**

Luna-0 authorizes exactly one narrowly scoped Luna-13F contract-control
completion pass under the existing `.github/agents/luna-13f.agent.md`
contract. This authorization covers only testing, experiment orchestration,
instrumentation and truthful artifact accounting. It does not create a new
Luna-13F contract, execute Luna-13F, change A01-A15, require an ACP, or
authorize Luna-13G.

The corrective pass must execute and independently evidence:

1. Continuous chronology for pre-admission evidence, evidence completion,
  freeze, score, decision, admission and held-out events, including queue
  state and an adversarial event-at/before-boundary chronology attack.
2. External-label mutation using otherwise identical executions, with exact
  mutated metadata and equality of all pre-held-out computational fields.
3. Per-field evidence provenance and an adversarial locality attack proving
  prohibited private state, labels, held-out metadata and unrelated global
  metadata cannot change raw local evidence.
4. The actual bounded candidate-state container, declared capacity and
  lifecycle semantics, plus saturation and reset/expiry/eviction-or-rejection
  tests and stale-state reuse.
5. Budget-boundary runs at `B-1`, `B`, `B+1` and a substantially larger budget,
  with incomplete runs barred from valid admission and completed decisions
  stable at larger budgets.
6. A complete machine-readable and human-readable contract audit. Every
  requirement must be `PASS`, `FAIL`, or
  `NOT APPLICABLE - CONTRACT CONDITION NOT TRIGGERED`, with an exact reason
  for conditional inapplicability and no unexplained mandatory `NOT RUN`.

The pass must retain final evidence for neutral decay, valid mirrored roles,
no-evidence, equalization, candidate-order reversal, future exclusion,
relabeling and deterministic replay. It must regenerate `results.json`,
`summary.json`, `audit-results.json` and the Luna-13F handoff so all mappings,
scores, selections, outcomes, chronology, isolation results, bounds, budget
status and terminal status agree. It must run the focused controls, the
Luna-13F preservation matrix, Luna-13E, corrected Luna-13D, Luna-13C,
Luna-13B, Stage-0, relevant Luna-12H/Luna-12N checks, the full CPU suite,
compile/static checks, diagnostics and `git diff --check`, recording exact
counts. This task performs none of those experiment executions.

The P0/P1 mapping, runtime evidence semantics and canonical scorer remain
unchanged unless a genuine contract defect requires correction. Any change
capable of changing the central result requires re-execution of both mappings
and disclosure of the prior result. No utility memory, probation, rollback,
speculative edge, reward channel, global utility state, oracle predictor or
new persistent learning subsystem is authorized. If a control requires one,
stop with **BLOCKED - ARCHITECTURE CHANGE REQUIRED** and return a decision
packet to Luna-0 and the project owner.

After execution, Luna-13F must return to Luna-0 for final independent closure
review. A negative result remains an acceptable successful scientific outcome;
the expected terminal interpretation, if controls pass and P0/P1 remain
`2/2` and `1/2`, is **NEGATIVE RESULT - RUNTIME EVIDENCE GENERATED BUT DOES
NOT PREDICT USEFUL GROWTH**. Luna-13G remains unauthorized.

## Luna-13F final independent closure review - 2026-09-30

Luna-0 independently reviewed the synchronized implementation at
`2b2432dabd49ecacceef525e8e3e68b909ee09c3`, the generated artifacts, the
contract audit, the execution handoff and the runtime control code. The raw
blinded result reproduces: P0 selects `candidate_A` and obtains `2/2`; P1
selects `candidate_A` and obtains `1/2`. The score is a bounded source-local
temporal-association count (`4.0` versus `0.0`), and neutral decay changes
local neuron state without changing score or rank. No-growth remains `2/2`
with 8 events and `8.0` uncalibrated activity-cost-proxy units; selected P0
growth remains `2/2` with 12 events and `12.0` units.

The negative observation is scientifically informative, but closure is blocked.
The declared future-event control appends an event and then removes it before
runtime execution (`events[:16]`); the chronology attack is a timestamp
predicate rather than an injected runtime event; and the locality attack passes
metadata that the runtime path does not read. Consequently the audit's three
corresponding PASS claims are not executed evidence. The aggregate `26 PASS,
0 FAIL, 2 NOT APPLICABLE` is therefore invalid as a closure audit.

Final status: **BLOCKED - CONTRACT AUDIT INVALID**. The two N/A entries are
valid only as conditional lifecycle cases: candidate expiry is not a mechanism
of the canonical policy, and eviction is not triggered because full capacity
uses explicit rejection. No A01-A15 clause changed, no ACP was created, and no
architecture mechanism or successor was authorized. Luna-13G remains
unauthorized. A future assignment would require a separately authorized
control repair and another independent Luna-0 review.

## Luna-13F runtime-attack corrective authorization - 2026-09-30

Following the final independent review at implementation/review baseline
`2b2432dabd49ecacceef525e8e3e68b909ee09c3`, Luna-0 authorizes exactly one
narrow corrective pass under the existing `.github/agents/luna-13f.agent.md`.
The authorization repairs only the invalid runtime controls: live future-event
injection after admission, queued chronology-boundary attacks, and a locality
attack that mutates genuinely accessible prohibited state. It does not execute
Luna-13F during this publication task.

The P0/P1 fixture, bounded source-local association-count mechanism and
canonical scorer remain unchanged unless a genuine runtime defect is found. The
corrective run must preserve or disclose any changed P0/P1 result, regenerate
all artifacts and the audit, and return to Luna-0. The two prior N/A cases
(unsupported expiry and deterministic full-capacity rejection rather than
eviction) remain valid; no expiry or eviction implementation is authorized.

The corrective pass may not add utility memory, reward pathways, probation,
rollback, speculative edges, global utility state, new candidate semantics,
architecture changes or an ACP. If valid future exclusion requires new
production architecture semantics, stop with **BLOCKED - ARCHITECTURE CHANGE
REQUIRED**. Luna-13G remains unauthorized, and a final Luna-0 closure review is
mandatory after the corrective artifacts.

## Luna-13F final independent closure - 2026-09-30

Luna-0 independently closed Luna-13F at review publication revision `e595a9f`
from implementation and artifact revision `83266f92d750939ef0b9904073e9f75badc35fbb`, with `HEAD ==
origin/main` and a clean synchronized review start. The corrected runtime
controls were reproduced rather than accepted from aggregate totals.

- P0 selects neutral `candidate_A` and obtains `2/2`; P1 selects neutral
  `candidate_A` and obtains `1/2`.
- Runtime evidence is a bounded source-local temporal-association count
  (`4.0` versus `0.0`). Neutral decay changes local state but not score,
  rank or selection.
- The same runtime processes the future continuation; live losing-candidate
  evidence changes `0.0 -> 5.0`, while frozen historical admission and
  topology remain unchanged.
- Actual queued before-decision and equal-time held-out events invalidate
  chronology; the strictly later event is accepted. Mutating real
  candidate-B private score state leaves candidate-A evidence unchanged.
- Candidate bounds, reset/stale-state reuse, budget threshold, label
  isolation, mirroring, equalization, no-evidence and deterministic replay
  pass. Expiry and eviction remain valid conditional N/A cases because the
  policy has no expiry path and deterministically rejects at full capacity.
- The complete audit is `26 PASS / 0 FAIL / 2 valid N/A`. Focused validation
  is `15 passed`, preservation is `72 passed`, and full CPU validation is
  `291 passed, 1 skipped`.

The terminal scientific result is **NEGATIVE RESULT - LUNA-13F RUNTIME
EVIDENCE DOES NOT PREDICT USEFUL GROWTH, INDEPENDENTLY VERIFIED AND CLOSED**.
Proposition 1 (bounded runtime evidence) and Proposition 2 (canonical
admission effect) are supported in the tested fixture; Proposition 3
(prediction of held-out useful growth) is not supported. No-growth remains
`2/2 @ 8` events and proxy `8.0`; selected P0 growth is also `2/2` at 12
events and proxy `12.0`, so no resource benefit is established. No A01-A15
change or ACP is required. **LUNA-13F CLOSED - SUCCESSOR NOT AUTHORIZED**;
Luna-13G remains unauthorized.

### ACP-0002 architecture review - 2026-09-30

The project owner requested an architecture reorganization beginning at the
neuron/edge signal path after Luna-13F closed with a negative result. Luna-13F
remains closed and its result is not being repaired or reinterpreted.

Luna-0 created ACP-0002, **Independent Edge Signal Transformation and Neuron
Gain Separation**, at synchronized revision
`25aa7697d523c13f0fdcf56c84170ceb553cc229`. The proposal was initially **Under
review**: it defined a bounded edge efficacy `w`, divider strength `d`,
independent logical reference `r`, fixed edge transfer `tanh`, positive edge
delay and a separate destination-neuron gain. It preserves A01-A15 and does
not define an edge learning rule, probation/maturation mechanism or local
time-series predictor.

This is a material canonical signal-path and ownership proposal, therefore an
ACP is required. Following the focused mathematical review, the subtraction
form was rejected because `d=0` erased the independent reference. ACP-0002 now
selects the Model B interpolation `v=d*tanh(w*a)+(1-d)*r` and is **Accepted for
staged implementation**. Only N1, edge/neuron data model and compatibility
representation, is authorized; N2 transfer execution and all adaptive or
temporary-edge mechanisms remain unauthorized. Luna-13G remains unauthorized.

N1 must preserve bounded `w`, `d`, `r` and `neuron_gain`, provide explicit
legacy identity compatibility, and add no production transfer execution or
learning. N1 returns to Luna-0 for verification before any later stage.

### Luna-15 ACP-0002 Stage N1 contract creation - 2026-09-30

Luna-0 creates and authorizes `.github/agents/luna-15.agent.md`, **Luna-15 -
ACP-0002 Edge/Neuron Data Model and Compatibility**, at the published
authorization revision recorded in its creation handoff. ACP-0002 remains
**Accepted for staged implementation**.

Luna-15 is authorized for exactly **N1 - edge/neuron data model and
compatibility representation**:

- edge-owned `edge_weight` / `w_ij` in `[-2,2]`;
- edge-owned `divider_strength` / `d_ij` in `[0,1]`;
- edge-owned `reference` / `r_ij` in `[-1,1]`;
- existing positive finite propagation delay;
- neuron-owned `neuron_gain` / `g_j` in `[0,2]`;
- legacy constructor, structural-plasticity, deterministic replay and
  observer/instrumentation compatibility;
- analytic and regression tests proving representation compatibility.

The future accepted Model-B equation is documented by ACP-0002 but **must not
be activated in N1**. N1 must not change routed payload semantics, event
identity, timestamps, sequence ordering or delay behavior. N1 completion does
not automatically authorize N2; Luna-15 must return to Luna-0 for independent
review before any later stage is considered.

Luna-15 is explicitly prohibited from N2 propagation changes, adaptive edge
learning, temporary/probationary connections, edge maturation, local
time-series mini-NNs, new utility-learning mechanisms, A01-A15 changes,
hardware implementation, reopening Luna-13F or authorizing Luna-13G. Luna-13F
remains **CLOSED**, Luna-13G remains unauthorized, and A01-A15 remain
unchanged.

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

## Current numbering reconciliation and Luna-18 H1

The current role assignments supersede older planning reservations while
preserving those records below as historical context:

| Luna | Current role | Status |
|---|---|---|
| Luna-15 | ACP-0002 N1 edge/neuron data model and compatibility | completed historical implementation |
| Luna-16 | ACP-0002 N2 static Model-B edge transfer | CLOSED |
| Luna-17 | hardware-equivalence / cross-backend hardware acceptance | RESERVED / NOT AUTHORIZED / NO ACTIVE CONTRACT |
| Luna-18 | ACP-0003 H1 Execution IR and backend interface skeleton | CLOSED / independently verified |
| Luna-19 | ACP-0004 E1 canonical single-excursion neuron | CLOSED / independently verified |
| Luna-20 | ACP-0005 TPCN-IR-2 excursion execution schema | CLOSED / independently verified |
| Luna-21 | ACP-0004 E2 multi-excursion return runtime | CLOSED / independently verified |
| Luna-22 | ACP-0006 first CPU software-reference excursion integration | CLOSED / INDEPENDENTLY VERIFIED (bounded fixed-topology EXCURSION_V1 CPU integration) |
| Luna-23 | ACP-0004 E2 positive-delay logical-time representability correction | CLOSED / INDEPENDENTLY VERIFIED |
| Luna-24 | ACP-0006 integrated IR-2 residual-provenance boundary correction | CLOSED / INDEPENDENTLY VERIFIED |
| Luna-25 | ACP-0006 sequential dataset evidence reproducibility | CLOSED / INDEPENDENTLY VERIFIED (`luna25-v1` only) |

The following review records preserve the chronology of previously published
gate findings. Later corrections and the final current Luna-22 closure
decision are recorded after those historical findings below.

Luna-19, Luna-20 and Luna-21 are closed component implementations; this does
not itself establish experiment-path integration. **OBSERVED:** the ordinary
experiment path at the ACP-0006 baseline constructs `TPCNNeuron` instances
and uses scalar activations for routing, prediction and readout, while E1/E2
excursion runtimes and IR-2 remain separate reference components.

The project owner accepted ACP-0006, **Excursion Runtime Integration and
Migration Contract**, as written at published proposal revision
`7eb997ebcb78f5a64074cd27a7a6181dbf693fa3` on 2026-10-03. The architecture
decision and final dispatch-readiness review found no internal contradiction
requiring new canonical behavior: prediction matching retains bounded FIFO
semantics; prediction errors remain opaque routed metadata; eligibility and
reward identify bounded traces; the classifier consumes actual emissions
while the existing outer prototype path uses its bounded signed-payload mean;
settling, sidecar/provenance bounds, proxy-energy counters and quiescent IR-2
startup are all implementable using explicit configuration and existing
interfaces. Dataset selection remains an implementation/reporting choice
under the existing open sequential-dataset protocol, not a new core semantic.

Luna-22 implemented and published the first CPU software-reference
integration at `a206f2e8fec8f0c72d9196b2bcca9d2e734c7974`. Luna-0's second
independent review is **BLOCKED / NOT CLOSED**: it reproduced an E2
positive-delay representability failure in valid temporal workloads and found
that integrated IR-2 startup still accepts assigned residual provenance and
sticky provenance truncation. The reported UCI Character Trajectories subset
also lacks a retained loader/split script and per-class results. The exact
review evidence is in
`workflow/handoffs/luna-0-second-independent-review-ACP-0006-Luna-22-20261003.md`.
No downstream visualization or research consumer migration is authorized.

Luna-23's bounded E2 strict-future representability correction is
**CLOSED / INDEPENDENTLY VERIFIED** under ACP-0004. The independent review
confirmed both polarities, finite strictly increasing local timestamps,
preserved configured-delay rejection, unchanged E1 and IR-2 behavior, and
removal of all seven E2 representability exceptions as their original failure
cause. The review and evidence are in
`workflow/handoffs/luna-0-independent-review-luna-23-e2-time-representability-20261003.md`.
This does not close Luna-22.

Luna-24 rejected assigned residual provenance and sticky truncation only at
the ACP-0006 integrated IR-2 startup boundary. Luna-0 independently verified
the published implementation, standalone E2/IR-2 preservation, schema
revision 1, clean startup, identity continuity, and the complete applicable
regression set. Luna-24 is **CLOSED / INDEPENDENTLY VERIFIED**; its evidence is
in
`workflow/handoffs/luna-0-independent-review-luna-24-ir2-provenance-20261003.md`.
Luna-23 remains **CLOSED / INDEPENDENTLY VERIFIED**. Neither correction
changes A01-A15, ACP-0004, ACP-0006 or IR-2 schema revision 1, and neither
authorizes visualization, structural-plasticity, dataset or benchmark-consumer
migrations.

Luna-22 remains **IMPLEMENTED / BLOCKED / NOT CLOSED**. A fresh
closure-readiness review verified a concrete remaining core defect: an actual
matched `PredictionError` reaches the first downstream node but is re-routed
from the original source and never reaches a reachable second hop, contrary
to ACP-0006 rule 6. This is the sole identified Luna-22 core correctness
blocker; the review does not close Luna-22.

Luna-23 and Luna-24 remain **CLOSED / INDEPENDENTLY VERIFIED**. Luna-25
remains **CLOSED / INDEPENDENTLY VERIFIED** for reproducibility of the new
`luna25-v1` dataset/split/results only; it did not reconstruct the historical
Luna-22 split. Focused evidence confirms local causal prediction/error
matching and positive-delay delayed-credit attribution work. Luna-25's zero
matched predictions/errors/credit, low classification accuracy and the
unreconstructable old split are respectively task-efficacy and
historical-evidence observations, not further integration correctness gates.
No accuracy threshold or efficacy requirement is added.

The full CPU suite was rerun: 24 failures, 796 passes, one CUDA-unavailable
skip, 821 collected. All 24 failures were individually inspected and
classified as downstream visualization, structural-experiment,
legacy-observable, temporal/spiral analysis or viewer compatibility
assumptions. They do not block Luna-22 under the fixed-topology EXCURSION_V1
contract and the existing requirement to run/report (not blanket-repair) the
full suite. No downstream migration is authorized by this review.

Luna-26 is **AUTHORIZED / NOT EXECUTED** solely to correct and test hop-local
opaque prediction-error forwarding in the Luna-22 integration adapter. Its
contract is `.github/agents/luna-26.agent.md`; its authorization record is
`workflow/handoffs/luna-0-authorization-luna-26-prediction-error-multihop-routing-20261003.md`.
The full closure-readiness evidence, including exact suite-failure matrix and
A01-A15 assessment, is
`workflow/handoffs/luna-0-acp-0006-luna-22-closure-readiness-20261003.md`.
Luna-26 must not change topology APIs, ACP-0006, canonical behavior or
downstream consumers, and does not itself close Luna-22. Luna-0 must
independently review its completion before reconsidering closure.
This fresh classification supersedes earlier wording that treated dataset
efficacy or all 24 downstream compatibility failures as Luna-22 core gates.

The independent Luna-0 review of the published Luna-26 correction found a
separate ACP-0006 rule-3 violation. On `n0 -> n1 -> n0`, the error return
event is queued and processed with route path `("n0", "n1", "n0")`; the
destination guard suppresses it only after the prohibited revisit has
occurred. Luna-26 is therefore **BLOCKED — ROUTE-PATH NO-REVISIT INVARIANT**,
and Luna-22 remains **IMPLEMENTED / BLOCKED / NOT CLOSED**. The independent
review and exact trace are recorded in
`workflow/handoffs/luna-0-independent-review-luna-26-prediction-error-routing-20261003.md`.

Luna-0 has authorized a bounded corrective pass under the existing Luna-26
identifier. The current topology API can route only the complete outgoing
fan-out, so it cannot omit a path-revisiting edge while retaining other legal
outgoing edges and atomic queue-capacity preflight. The corrective pass may
add one optional, default-preserving destination-exclusion argument to
`BoundedTopology.route()` and apply the current error event's `route_path`
only to that event's route. This must not become a global visited set; the
existing per-destination guard remains necessary for convergent paths.
The new authorization is
`workflow/handoffs/luna-0-authorization-luna-26-corrective-route-path-20261003.md`,
and the Luna-26 agent contract records its exact narrow override. No ACP,
A01-A15, Model-B equation, delay, credit, dataset or downstream-consumer
change is authorized. Luna-0 must independently review this corrective pass
before any Luna-22 closure decision.

The authorized same-Luna correction added optional, backward-compatible
destination exclusions to `BoundedTopology.route()` and uses only the
current prediction-error route path to omit revisits before queue admission.
Independent Luna-0 review confirmed that the cycle return is never queued,
legal outgoing fan-out remains available, and convergent duplicate suppression
is preserved. Luna-26 is **CLOSED / INDEPENDENTLY VERIFIED** for this bounded
correction. Luna-22 is now **CLOSED / INDEPENDENTLY VERIFIED** for the
accepted first fixed-topology `EXCURSION_V1` CPU software-reference
integration only. The final closure evidence and exact validation appear in
`workflow/handoffs/luna-0-independent-review-luna-26-prediction-error-routing-20261003.md`.

The independent Luna-26 review reran the focused integration suite (**49
passed**), prescribed ACP-0006 regression plus focused suite (**340
passed**), full CPU suite (**24 failed, 802 passed, 1 skipped**), and test
collection (**827**). Failure identities remain in the previously classified
downstream compatibility groups. The additional cycle invariant is an
owned blocker resolved by the reviewed corrective pass; it was not one of
those downstream failures. The corrective review recorded topology plus
integration **60 passed**, the prescribed ACP-0006 regression set **342
passed**, full CPU suite **24 failed, 804 passed, 1 skipped**, and **829
collected**. The 24 downstream compatibility failures remain a separate
backlog and do not undo this bounded core closure. Luna-25's zero dataset
prediction/error/credit matches and low accuracy remain task-efficacy
observations, not routing defects.

Closure does not establish predictive efficacy, useful delayed-credit
learning, downstream consumer migration, integrated structural plasticity,
historical Luna-22 split reconstruction, writer-disjointness,
hardware/backend equivalence, calibrated physical energy, or repository-wide
architecture completion. No consumer migration was authorized. The next
governance action is for the project owner / Luna-0 to select one bounded
downstream compatibility semantic unit, if desired.

The original Luna-25 authorization was for a retained, deterministic UCI
Character Trajectories loader/split/report under the unchanged ACP-0006
`EXCURSION_V1` path. Its contract was
`.github/agents/luna-25.agent.md`; the authorization handoff is
`workflow/handoffs/luna-0-authorization-luna-25-dataset-evidence-20261003.md`.
The published implementation/evidence and completion handoff are
`5cb17d9bb79c848c27805cb79484d9ab3cd0f5b8` and
`425180bfb2b02691cf64f392f071795cc812cd72`. The subsequent independent review
closed the dataset evidence gate specifically for `luna25-v1`; it found that
the old split is not reconstructable and did not call the new split a
reproduction. The review is recorded in
`workflow/handoffs/luna-0-independent-review-luna-25-dataset-evidence-20261003.md`.

The 24 downstream failures remain a separate governance track. The independent
review reran the full suite with 24 failures, 796 passes, one CUDA-unavailable
skip and 821 collected tests; all failures remain in previously classified
consumer groups. No blanket consumer migration is authorized; visualization,
structural experiments, legacy observables, temporal/spiral analysis and the
3D viewer require consumer-specific intent and scoped review before
implementation. The Luna-25 review assigns no successor implementation because
these groups require distinct decisions.

The original acceptance and dispatch decision is in
`workflow/handoffs/luna-0-acp-0006-acceptance-luna-22-authorization-20261003.md`;
the implementation contract is `.github/agents/luna-22.agent.md`. The
preceding dependency and under-review proposal records remain historical.

The former Luna-15 FPGA/VHDL and Luna-16 FPAA assignments remain historical
workflow planning records and are superseded as current assignments by the
actual ACP-0002 contracts. Future FPGA-native and FPAA-native roles receive new
identifiers when separately authorized. Luna-17 is not created or executed by
H1.

Luna-18 H1 was limited to a versioned hardware-neutral Execution IR, minimal
backend identity/capability/equivalence/policy interfaces, canonical conversion
and safe reference reconstruction. Luna-0 independently verified and closed H1
at reviewed revision `4aee46829807072e9af0f08842d561026555006d`; the evidence is
in `workflow/handoffs/luna-0-independent-corrective-review-ACP-0003-H1.md`.
The IR-1 scope is canonical network configuration plus transferable initial
execution state for the supported reference reconstruction path, not a full
live-runtime checkpoint. H1 preserves Model-B parameters, timing,
deterministic ordering, bounded state, prediction/error behavior,
reward/idempotency and structural decisions. H1 does not authorize H2,
production backends, approximations, calibration, attractor neurons, edge
learning, ACP-0002 N3, Luna-13F reopening, Luna-13G or A01-A15 changes.

TPCN-IR-2 is a separate version boundary. It explicitly tags
`TANH_LEGACY` versus `EXCURSION_V1`, preserves E1 state and identity
continuation, rejects excursion records in IR-1, and represents M state without
claiming M reconstruction support. Its scope is transferable reference state,
not a complete live-runtime checkpoint.

---

# Historical hardware-role reservations (superseded)

The following sections are retained to preserve the original numbering and
planning history; they are not current assignments.

## Historical Luna-15 — FPGA/VHDL Branch

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
             Luna-12 (passed)
             Contract + CPU exporter
               │
              ┌─┼──────────────────────────────┐
              ▼ ▼                              ▼
             12A 13                             14
              │  GPU                            ModelSim/
              ▼  visualization                  FPGA
             12B
              │
             12C
              │
             12D
              │
             12E
              │
             12F
              │
             12G
              │
             12H
              ├───────► 12I  structural growth
              │
              └───────► 12J  efficacy + causal verification
                      │
                      ▼
                   12K capacity pressure
                     and path shortening
                      │
                      ▼
                        12L energy / prediction
                        four-class temporal scale
                          │
                          ▼
                    Luna-0 review

        Stable software event semantics
                     │
                     ▼
                Post-observability
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

### Luna-0 independent review of ACP-0002 Stage N1 - 2026-09-30

At reviewed revision `7ddf00b6c7a8f01ad4ebe3483bc553c83dbe26d3`, synchronized
with `origin/main` on a clean `main` worktree, Luna-0 independently verified
ACP-0002 N1 as:

**PASS - ACP-0002 N1 DATA MODEL AND COMPATIBILITY INDEPENDENTLY VERIFIED**

The bounded edge schema, compatibility defaults, neuron-gain migration,
legacy payload routing, topology reconstruction, structural-growth defaults,
observer non-interference and deterministic representation passed direct and
automated checks. The existing TPCV-1 format intentionally remains a
version-1 observability boundary that omits future connection transfer fields;
this is now documented and does not claim complete N1 edge-state fidelity.

Validation recorded in the Luna-0 handoff includes 18 focused N1 tests, 83
selected topology/neuron/structural/replay/regression tests, 309 full CPU
tests with 1 skipped, direct adversarial probes, compileall and diff checks.
N1 is complete. ACP-0002 remains accepted for staged implementation; N2 is
not authorized. A01-A15 remain unchanged, Luna-13F remains closed and
Luna-13G remains unauthorized.

### Luna-16 ACP-0002 Stage N2 authorization - 2026-09-30

After N1 publication and independent review, Luna-0 selected **CONTROLLED
CANONICAL CUTOVER**. N1 is the final representation-compatible version of
legacy raw-payload execution. N2 intentionally activates the accepted ACP-
0002 Model-B transfer as the new canonical execution equation; the N1 defaults
`w=1`, `d=1`, `r=0` produce `tanh(a)`, not raw `a`, and must not be described
as signal identity.

Historical closed experiment revisions remain reproducible from their
committed code and are not reinterpreted as Model-B results. New N2-and-later
experiments must identify the new architecture revision. No permanent
per-edge legacy/model-B flag is part of the canonical architecture.

Luna-16 is authorized for **static execution only**:

```text
z_ij = tanh(w_ij * a_i)
v_ij = d_ij * z_ij + (1 - d_ij) * r_ij
```

The contribution `v_ij` is scheduled after the existing positive finite edge
delay and then follows the existing local-time decay, bounded integration,
neuron gain and fixed-neuron-nonlinearity path. No global neural timestep is
introduced. Edge parameters are immutable during N2 execution.

Luna-16 must establish a new Model-B analytic/replay baseline. It must keep
causality, deterministic ordering, finite delays, queue and structural bounds,
label/future isolation, reward identity, observer non-interference and bounded
recurrence invariant. Numeric payload/state/activation and downstream metrics
may change and are not legacy regressions by themselves. TPCV-1 remains an
explicit observational version-1 boundary; any computationally active field
serialization/version change requires an explicit governance result.

Luna-16 must not implement edge learning, probationary or maturing edges,
new structural utility prediction, new pruning, reward-driven edge updates,
temporal mini-networks or hardware-specific voltage behavior. It must return
to Luna-0 after implementation. Luna-13F remains closed, Luna-13G remains
unauthorized, ACP-0002 remains accepted for staged implementation, and
A01-A15 remain unchanged.

### Luna-16 N2 implementation result - 2026-09-30

**OBSERVED:** Static Model-B transfer is active for numeric neural signal
routing at implementation revision `ed8aaff2d0d0d031c2c1f84b311251f530282479`:
`z=tanh(w*a)` and `v=d*z+(1-d)*r`. Numeric signal payloads are delayed by the
existing edge delay; control and metadata payloads are not transformed.

**OBSERVED:** The focused N2 suite passed 267 tests and the full CPU suite
passed 549 tests with 1 skipped. Compile, deterministic replay, observer
ON/OFF, fan-out, equal-time fan-in, unequal delays, bounded recurrence,
structural defaults/reconstruction and control-payload boundary checks passed.

**INFERRED:** N2 preserves event causality, local temporal state, finite
propagation, bounded topology/dynamics, label/future isolation, reward
identity and observer non-interference. Numeric payload/state/activation and
downstream metrics are expected to differ from pre-N2 execution.

**TPCV GOVERNANCE RESULT:** `TPCV-1 REMAINS VALID FOR ITS LIMITED DECLARED
PURPOSE`. TPCV-1 is downstream-only and does not serialize active `w`, `d` or
`r`; no silent format expansion was made. Computationally equivalent transfer
state replay would require a separately governed format decision.

**HYPOTHESIZED:** The new bounded edge transform provides the authorized
Model-B computational substrate without establishing task improvement. The
analytic/replay baseline is recorded at
`artifacts/acp-0002-n2-model-b-baseline/baseline.json`.

N2 returns to Luna-0 for independent review. It does not authorize N3 or any
later ACP-0002 stage, probationary/maturing edges, temporal mini-networks or
Luna-13G. Luna-13F remains closed.

## Luna-27 — TPCV-2 EXCURSION_V1 Snapshot Visualization

**Authorization:** Luna-0 authorizes one bounded CPU visualization
representation implementation after the post-Luna-22 compatibility review.
The exact agent contract is `.github/agents/luna-27.agent.md`; the
authorization record is
`workflow/handoffs/luna-0-authorization-luna-27-tpcv2-excursion-snapshot-20261003.md`.
This entry authorizes implementation but does not execute it.

**Decision:** `DECISION C — VERSIONED EXCURSION VISUALIZATION FORMAT
REQUIRED; LUNA-27 AUTHORIZED.` TPCV-2 is dedicated to instantaneous
`EXCURSION_V1` snapshots at existing CPU epoch boundaries. TPCV-1 bytes,
decoding, and historical meanings remain unchanged. The format version is
the model discriminator; model type must not be inferred from values.

**TPCV-2 observer contract:**

- `state` is the existing E2 `state` alias (`x`).
- `active` is true iff `mode != N`, meaning a non-neutral excursion mode is
  currently admitted at capture; it does not mean nonzero TANH output.
- `mode` is the bounded enum `N`, `S_PENDING`, `S_RETURN`, or `M_ACTIVE`.
- `pending_internal_work` indicates only whether internal work is pending.
- `processed_events` is the E2 `processed_event_count`, including processed
  external and internal events.
- No scalar activation is serialized or fabricated; a shared decoded API may
  explicitly report activation as unavailable. No last emission, interval
  activity, event history, or runtime checkpoint state is included.

The format retains finite deterministic records, canonical ordering, strict
malformed/oversize rejection, and TPCV-1 bounds. TPCV-2 uses the existing
32-byte big-endian header with version byte 2; its neuron record contains a
bounded UTF-8 ID, flags for active/optional position/pending work, explicit
mode code, finite state, bounded processed-event count, and optional signed
coordinates. Connection records keep their TPCV-1 layout. No ACP or A01-A15
change is made.

**Owned files:** `tpcn/visualization.py`, `tpcn/cpu_visualization.py`,
`tests/test_visualization.py`, `tests/test_cpu_visualization.py`,
`workflow/docs/luna/VISUALIZATION_CONTRACT.md`, and the Luna-27 completion
handoff. No other visualization code is authorized.

**Required gate:** preserve TPCV-1 byte/semantic behavior; test deterministic
TPCV-2 round-trip and explicit model semantics; reject unsupported, malformed,
oversize, and mixed-version sequences; pass all three CPU visualization tests,
the existing visualization suite, and GPU TPCV-1 regression; verify offline
replay and capture disabled/every-epoch/every-N result equivalence. Keep
capture downstream-only, labels/future data isolated, and fixed topology
unchanged. Report other 21 baseline downstream failures without repairing
them. Stop and return to Luna-0 if core/runtime changes or ownership expansion
is required.

**Mandatory sequence:** `Luna-0 -> Luna-27 -> Luna-0`. Luna-27 returns with
its evidence handoff and may not authorize a successor.

**Final status (2026-10-04): CLOSED / INDEPENDENTLY VERIFIED.** Luna-0
independently reviewed the published implementation and focused test set and
passed the bounded CPU TPCV-2 instantaneous `EXCURSION_V1` snapshot capture,
versioned codec, and homogeneous-version offline replay scope. The independent
review handoff is
`workflow/handoffs/luna-0-independent-review-luna-27-tpcv2-excursion-visualization-20261004.md`.
TPCV-1 bytes and historical meanings remain unchanged. This closure is
observability-only: it is not architecture promotion, requires no ACP, and
does not authorize GPU/FPGA support, downstream migrations, or a successor
Luna. The implementation full-suite evidence remains 821 passed, 21 failed,
1 skipped; the independent reviewer did not rerun the full suite. The 21
previously classified downstream failures remain separate and unresolved.

## Luna-0 EXCURSION_V1 structural re-entry readiness - 2026-10-04

At baseline `d9abe5e3a5b9b3c6d6049ac4c64647463c33ba2d`, Luna-0 classified
the 19 Luna-12B/Luna-12L/spiral/temporal-analysis/3D-viewer failures as
terminating at the intentional EXCURSION_V1 structural-mode guard. This is
the immediate test dependency, not proof that all assertions pass after the
guard. The historical ExperimentRunner's index/policy endpoints,
`abs(run.feature) + run.loss` score, and feature-derived pruning score do not
establish source-local E2 evidence.

Luna-13F's runtime temporal-association mechanism remains an experimental
fixture result: evidence generation and canonical admission were supported
there, useful-growth prediction was not supported, and resource benefit was
not established. Its use in normal E2 training would be a promotion requiring
a project-owner architecture decision. Draft ACP-0007 records the unresolved
E2-local observation feed, evidence/score provenance, chronology and reset,
and pruning questions. It is not accepted. The current guard remains;
growth/pruning and Luna-28 are not authorized or executed. See
`workflow/handoffs/luna-0-excursion-structural-reentry-readiness-20261004.md`.
