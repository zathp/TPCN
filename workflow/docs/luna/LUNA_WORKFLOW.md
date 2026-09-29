# TPCN Luna Multi-Agent Workflow — Event-Driven Architecture

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

**Stage-0 gate:** remains open because reward-delivery authority is internally
inconsistent. No Luna-13B, broad efficacy experiment, or hardware milestone is
authorized. After Luna-0/project-owner resolves the reward contract and the
legacy replay-status follow-up, the next bounded scientific target may be only
the one-slot structural competition in which causally observed local temporal
evidence produces a predicted decay-dependent admission crossover. Synthetic
endpoint timing tables must not serve as proof of online learning.

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

