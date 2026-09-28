# Acceptance criteria and first benchmark

These are required verification procedures for future implementation, not test results. Luna-0 and Luna-11 define concrete capacities, tolerances and reproducible fixtures before running them.

## Core checks

| Check | Clauses | Required observation |
|---|---|---|
| test_no_global_neural_clock | A01–A02 | Irregular event times work without updating every neuron on a common neural tick. |
| test_event_causality | A01–A03 | Distant changes have no effect before a permitted event arrives. |
| test_finite_propagation | A03 | Inter-node arrival follows emission by the declared positive delay. |
| test_fan_in_limit / test_fan_out_limit | A04 | Construction and rewiring reject connections exceeding declared budgets. |
| test_no_global_state_leak | A07 | Core updates depend only on locally available state and permitted messages; evaluation instrumentation supplies no hidden input. |
| test_no_spatial_reservoir_dependency | A05 | The benchmark initializes, learns and evaluates without the legacy reservoir. |
| test_idle_network_cost | A01, A09 | With no input or due local events, no all-neuron neural update loop occurs; report host overhead separately. |
| test_delayed_prediction_error | A06 | A prediction matches its later target and produces an explicit, causally propagated error event. |
| test_delayed_credit | A07, A11 | Reward arriving later modifies eligible local activity using elapsed time, not future/global information. |
| test_energy_accounting | A09 | Known activity reconciles with local counters and aggregate reports; report proxy units. |
| test_high_cost_high_reward_survival | A10 | A sufficiently useful expensive operation can remain active under the chosen utility rule. |
| test_high_cost_low_reward_suppression | A10 | Comparable expensive unproductive activity is suppressed without making silence the task solution. |
| test_bounded_state | A08 | Stress and recurrent-event cases remain within declared state bounds. |
| test_intrinsic_temporal_state | A02, A08 | A single event changes bounded persistent local state that remains observable before a declared reset; elapsed-time evolution is event-triggered and deterministic. |
| test_temporal_noncommutativity | A02 | The canonical/reference neuron has at least one deterministic ordered-pair fixture whose state, output, or trace differs when event order is exchanged. |
| test_unequal_path_delay | A03-A04 | Short and multi-hop paths have declared cumulative delays with timestamp-correct arrivals, and path pruning removes the corresponding future effect. |
| test_convergent_temporal_arrival | A01-A04, A08 | Older long-path and newer short-path consequences reach a downstream neuron with preserved timestamps and produce a fixture-level timing-dependent result without unbounded recurrence. |
| test_deterministic_seed | A01–A04 | Same input, configuration, tie ordering and seed reproduce reference behavior. |
| batched/unbatched equivalence | A01–A03 | Ready-event batching preserves causal outputs within predeclared tolerances. |
| bounded structural plasticity | A04, A14 | Allocation, rejection, replacement and pruning respect finite nodes, fan-in/out and routing constraints; failed admissions have explicit causes and in-flight events have defined handling. |
| convergent structural capacity | A04, A14 | A legal enabled policy leaves measurable candidate/admission routes for causally relevant multi-path fan-in; bounded capacity is not treated as an optimization target or silently reported as learning. |
| structural evidence locality | A07, A14 | Candidate evidence is causally/locality available to the component; global topology statistics, labels and future events do not enter canonical structural decisions. |
| structural organization measurements | A04, A14 | Reports distinguish fan-in/out saturation, duplicate proposals, random versus evidence-directed growth, repeated temporal association, path shortening, replacement/pruning, convergent motifs, edge utilization and useful versus unused edges. |

Recommended implementation refinements: define event time units, equal-time ordering, late-event policy, finite queue capacities, overflow/backpressure behavior and prediction/credit expiry. Record decisions; do not silently treat these proposed details as already implemented or additional source-conversation invariants.

## Streaming protocol

1. Identify the actual dataset, version, permitted usage, native stroke representation, classes and train/validation/test split. Dataset choice is still open.
2. Split before fitting preprocessing; prefer writer-disjoint splits when writer identity is available. Fit normalization on training data or use a declared causal online transform.
3. Present START_CHARACTER, ordered stroke/point events and END_CHARACTER. Use native timing where available; document synthetic intervals otherwise.
4. Derive features only from the current/past stream and training-fitted constants. Whole-character centering/scaling using unseen points is not causal preprocessing.
5. Keep labels out of core input. Convert training outcomes to reward/error messages through declared causal interfaces. Do not train on held-out test labels.
6. Declare reset/retention rules between characters, including pending events and eligibility. Prevent unintended cross-split state leakage.
7. Score primary classification after END_CHARACTER using a declared readout/settling rule and finite processing budget. Report optional prefix predictions separately.
8. Record prediction targets, matched error events and loss. Classifier accuracy alone is insufficient.

Start with the workflow's candidate configuration: 256 neurons, 26 outputs if the dataset is A–Z, fan-in/out 8, explicit ten gates off, structural plasticity off, predictive error and local energy accounting on. These values are tunable.

## Measurements and comparisons

Record accuracy, prediction loss, processed events, neuron/operator activations, estimated energy, active connections, connectivity utilization, simulated response latency and host runtime separately. Report per-character distributions and totals. Define energy per correct classification with a stated zero-correct policy.

Record the energy model, units and calibration status. Switching counts and activity estimates are proxies, not physical joules without calibration. Record utility and reward attribution definitions so results can be interpreted.

Compare explicit gates (including the historical ten-pathway reference), event-only activation and utility-mediated computation using matched data splits, seeds, graph/resource budgets and training effort. Report accuracy versus events and energy, prediction loss versus events and energy, and variability across seeds. Do not assume a winning variant.

## Integration gate

The first milestone must demonstrate all twelve immediate success criteria in the workflow, including actual sequential classification, predictive learning/error events, delayed credit and reward-adjusted local energy instrumentation. Report performance honestly; no numerical accuracy threshold was established in the source conversation. Fix any later performance target before evaluating the held-out test set.

Luna-11 supplies evidence for applicable core checks. Failed invariants block integration. Experimental gating and plasticity claims require their own comparative evidence.

## Visualization / Observability gate

The [Visualization / Observability milestone family](../luna/LUNA_WORKFLOW.md#visualization--observability-milestone-family) is a read-only, non-semantic validation track. These are future acceptance checks, not implemented capabilities or passing results. Luna-12 must pass before Luna-12A, Luna-12B, Luna-13, or Luna-14 implementation; Luna-12B additionally depends on the completed Luna-12A CPU path. Luna-12A and Luna-12B are optional CPU integrations and neither is a prerequisite for Luna-13 or Luna-14. Retain the existing Milestone 1 integration criteria.

| Check | Required observation |
|---|---|
| Luna-12 format and CPU reference | Binary/hex fixtures preserve logical IDs, directed edges, represented state, framing, ordering, and declared fields; malformed input, unsupported versions, empty state, overflow, and incomplete captures are explicit and bounded. |
| Luna-12A CPU training integration | Deterministic Luna-9 synthetic training captures bounded TPCV-1 snapshots; replay works without the training process; capture disabled, epoch-frequency, and more-frequent capture runs preserve predictions, metrics, replay digest, updates, topology where applicable, reward/utility state, and final network state; missing/malformed/over-limit snapshots fail clearly. |
| Luna-12A inspection path | A CLI/demo or deterministic replay/export path exposes neuron identity, activity/state, connections, snapshot/epoch index, and available prediction, reward, energy, utility, and accuracy metrics; topology evolution is shown when validated structural plasticity is enabled or explicitly reported deferred. |
| Luna-12B persistent topology and bounded plasticity | One validated bounded topology persists across the declared training scope; Luna-10 mutation accounting exposes additions, removals, rejected candidates/reasons, active edges, fan-in/out utilization, and bounded history; failed admission and pruning preserve valid routing and finite propagation. |
| Luna-12B structure-function observability | Fixed-topology learning, structural-plasticity, and supported no/reduced-learning controls report event/activation coverage, active/inactive neurons, prediction loss, accuracy, reward, energy, utility, topology counts and mutation history; results distinguish unchanged/changed topology from improved/unchanged/degraded behavior without assuming benefit. |
| Luna-12B replay and non-interference | TPCV replay distinguishes unchanged, added, and recently removed connections where history permits; same-seed mutation/final-topology/snapshot sequences reproduce; capture-on/off preserves mutation decisions and functional results; visualization cannot trigger mutations or create computational backpressure. |
| Luna-12C replay and stable 3D layout | Existing bounded TPCV artifacts load; canonical coordinates are preserved when present; otherwise stable deterministic diagnostic coordinates are identical across repeated replay and never enter neural computation. |
| Luna-12C temporal viewer | Play/pause, speed, forward/backward step, first/last, direct snapshot selection, camera orbit/pan/zoom/reset/fit, neuron inspection, and snapshot-level activity playback work deterministically. Event pulses are shown only if a future trace records event timing. |
| Luna-12C topology and dense-graph inspection | Directed persistent edges render; real additions and recently pruned edges are distinguishable with expiring highlights; rejected mutations remain diagnostics; practical active/changed/utilization/neighborhood/depth/new-pruned filters reduce dense graphs without mutating replay. |
| Luna-12C synchronized metrics and non-interference | Available epoch/snapshot, accuracy, prediction loss, reward, energy, utility, active-neuron fraction, active-edge count, additions, removals, and mutation rejections remain synchronized; renderer timing, dropped frames, and disconnected viewers do not alter computation or replay digest. |
| observation non-interference | Matched capture-on/off runs preserve computational state, causal outputs, learning, topology, classifier, reward, timestamps, and queues; a slow/disconnected viewer or full observation buffer cannot backpressure neural execution. |
| Luna-12D temporal dynamics analysis | Reports distinguish active/inactive neurons; existing, exercised, added, removed, and rejected edges; lifetimes; per-epoch mutations; rejection reasons; stabilization; fan-in/out saturation; active-edge utilization; topology/activity concentration; and behavior correlations. Causation is not inferred. |
| Luna-12D connection plateau investigation | The plateau is analyzed from precise recorded rejection reasons, including duplicate edge, source fan-out, destination fan-in, global capacity, nonlocal candidate, candidate capacity, pruning/growth interaction, or no valid candidate; generic capacity claims are insufficient when a precise reason exists. |
| Luna-12D replay and analytical non-interference | Repeated analysis reproduces machine-readable metrics and summaries; analysis cannot mutate replay, topology, computation, training, or backpressure. Missing evidence is explicit rather than inferred. |
| Luna-12E computational topology integration | One persistent bounded topology is used for structural plasticity and event routing; events traverse actual edges; prediction/error behavior derives from propagated activity; and boundedness, finite propagation, local learning, state, and deterministic replay remain valid. |
| Luna-12E causal reachable-edge verification | Matched controlled interventions show that removing a reachable edge changes downstream activity and that adding a reachable edge can change downstream activity when the workload exercises it; functional metrics are compared without treating topology movement alone as causal evidence. |
| Luna-12E integration readiness | Capture/analysis remains downstream-only; add/remove interventions, prediction/error metrics, classification behavior, boundedness, non-interference, and deterministic controls are recorded. Luna-0 reviews the evidence before any readiness claim. |
| Luna-12F readout starvation reproduction | A deterministic A/Z fixture records initial prediction, reward, readout-update decision, and prototype state; an initially misclassified class is tested for representation creation under the existing positive-reward gate. |
| Luna-12F pre-readout separation | Per-example network feature, evaluation-only target label, class distances/scores, prediction, confidence, and winner margin are exposed; A/Z feature separability is measured before readout selection. |
| Luna-12F corrected external readout | A bounded, deterministic, resettable external readout can acquire every declared training class without requiring positive reward; reward remains optional refinement rather than the sole class-creation gate. |
| Luna-12F label isolation | Identical inputs produce the same neural event trace, neuron/predictor state, topology decisions, routing, energy, and prediction/error computation regardless of external target label; labels affect only readout learning and evaluation. |
| Luna-12F class-separation diagnostics | Reports include per-class accuracy, confusion matrix, confidence, margin, prediction loss, reward, energy, utility, readout updates, prototype count, class-starvation count, and explicit missing-class representation status. |
| Luna-12F controlled comparison | Positive-reward-gated and corrected readouts use identical workload and seed; fixed-topology, structural-plasticity, and useful no-learning controls are compared without claiming readout improvement is neural-predictor improvement. |
| Luna-12F bounded deterministic state | Readout state remains bounded by `max_classes`, resettable, and identical for same-seed training; Luna-12E causal, experiment, classifier, structural-plasticity, visualization/analysis, compile, diagnostics, and full-suite checks remain passing. |
| Luna-12G trajectory validity | Left/right center-outward spirals begin at the same center, match radius evolution and sample-count/path-length rules, and differ by handedness/temporal orientation rather than class-specific coordinate signs, starts, duration, or length. |
| Luna-12G nuisance symmetry | Rotation, scale, translation, angular speed, radial growth, sampling timing, coordinate noise, and radial jitter use the same declared seeded distributions for both classes; metadata reproduces each example. |
| Luna-12G split integrity | Training and evaluation generators are deterministic but disjoint; evaluation does not reuse training examples or nuisance combinations verbatim, and preprocessing uses only causal/current-past information. |
| Luna-12G label isolation | Target handedness affects only external readout supervision/evaluation; identical generated input streams produce identical neural events, predictor state, routing, topology decisions, structural evidence, energy, and prediction/error behavior regardless of relabeling. |
| Luna-12G controls | No-learning, fixed-topology learning, structural-plasticity learning, shuffled-order, defined time-reversal, same-class nuisance pairs, and opposite-handed matched pairs are all run and reported without an accuracy threshold. |
| Luna-12G diagnostics | Reports include accuracy, per-class accuracy, confusion, prediction loss, confidence, margin, reward, energy/proxy units, utility, events, active-neuron fraction, connections, mutations, represented readout classes, seeds, and all generator metadata. |
| Luna-12G determinism and bounds | Same seed/configuration reproduces trajectories, metrics, readout state, event results, topology/mutation results, and bounded resources; applicable A01-A11, A14, A15, regression, compile, and diagnostic checks remain valid. |
| Luna-12H intrinsic temporal state and recurrence | A deterministic single-spike fixture proves persistent local state and declared decay/evolution before reset; ordered-pair and equal-multiset/different-order fixtures expose temporal noncommutativity; no global neural timestep or hidden recurrent tick is required. |
| Luna-12H unequal-delay routing | A short `A -> C` path and long `A -> B -> D -> C` path have measured cumulative delays with `D_long > D_short`; arrivals preserve timestamps and deterministic ties; multi-hop delay is not inferred from edge count alone. |
| Luna-12H convergent timing | An older event on the long path and newer event on the short path produce a deterministic downstream state/output difference when their relative arrival timing changes; same total input with different arrival timing also differs in at least one fixture. |
| Luna-12H path pruning and bounded recurrence | Removing a long or short path removes its future causal effect; cycles remain finite under event, lineage/path, queue, fan-in/out and state budgets, with no infinite recurrent propagation. |
| Luna-12H reset and isolation | Character/sequence reset removes prior temporal state and pending state according to a declared policy; topology may persist independently; no state leaks between examples unless explicitly authorized; labels do not affect core temporal traces. |
| Luna-12H determinism and fan-in timing | Same seed/configuration reproduces state, timestamps, queue outcomes and tie order; different-time fan-in events are processed in canonical timestamp order rather than unordered aggregation. |
| Luna-12I temporal-associative structural growth | Fixed topology, existing policy, random legal candidates, and temporal-association candidates use matched budgets/seeds; timing-shuffled and reversed-order controls are included where practical; fan-in formation, path shortening, rejection causes, churn, event/prediction/energy/resource metrics and task behavior are reported without assuming benefit. |
| Luna-12I falsification | The temporal-association hypothesis states a result that would count against it; negative seeds, failed admissions, duplicate proposals and no-improvement results are retained rather than filtered. |
| Luna-12J bootstrap boundaries | Independently prepared modules declare inputs/outputs, event semantics, state, reset, topology/resources, time units, parameter bounds, hardware assumptions and provenance; composition tests causal exchange, timing, bounds, reset/isolation, prediction/error, energy/resource behavior, determinism and post-integration local learning. |
| Luna-12J bootstrap reproducibility | Bootstrap state is serialized/versioned or reproducibly generated; zero/random/simple deterministic initialization remains a legal reference; trainer state is absent from runtime neural inputs and software/hardware equivalence remains testable. |
| Luna-13 CPU/GPU parity | Matched fixtures and declared capture boundaries produce semantically equivalent records through the Luna-12 parser, with fixed precision tolerances and no GPU-specific schema. |
| Luna-14 ModelSim/FPGA bridge | A documented hex/binary field map decodes known traces; truncation and HDL X/Z/unknown values are surfaced; reset and snapshot boundaries are deterministic. |
| DE1-SoC observation | FPGA diagnostic capture is downstream-only, record loss/overflow is visible where practical, and preferred VGA or future Ethernet paths cannot stall or alter computation. |

Visual evidence supplements the core and hardware gates. Snapshot metadata, viewer layouts, transport timing and display refresh must not become computational inputs or impose a global neural clock.

## Hardware gate

Stabilize and version software event semantics before FPGA/VHDL and FPAA implementation. Compare reference traces for causality, predictions, classifications, state/connectivity bounds and energy/utility decisions. Predeclare precision, timing and analog tolerances; exact internal equality is not required. FPGA metering clocks must not impose a neural clock. FPAA energy approximations need not copy digital switching metrics. Record unsupported behavior and calibration limits.

