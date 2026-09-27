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
| test_deterministic_seed | A01–A04 | Same input, configuration, tie ordering and seed reproduce reference behavior. |
| batched/unbatched equivalence | A01–A03 | Ready-event batching preserves causal outputs within predeclared tolerances. |
| bounded structural plasticity | A04, A14 | Allocation/pruning respects finite nodes, fan-in/out and routing constraints; in-flight events have defined handling. |

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

## Visual Examination / Observability gate

The [Visual Examination / Observability milestone family](../luna/LUNA_WORKFLOW.md#visual-examination--observability-milestone-family) is a read-only, non-semantic validation track. These are future acceptance checks, not implemented capabilities or passing results. Complete Visualization-1 and Visualization-2 before deep optimization; retain the existing Milestone 1 integration criteria.

| Check | Required observation |
|---|---|
| versioned snapshot contract | Human-readable and binary/hex fixtures preserve the same logical IDs, directed edges and represented state; unsupported versions, absent fields and incomplete captures are explicit. |
| observation non-interference | Matched capture-on/off runs preserve computational state, causal outputs, learning and topology decisions; a slow/disconnected viewer or full observation buffer cannot backpressure neural execution. Report observation overhead and losses separately. |
| CPU/GPU snapshot parity | Matched fixtures and declared capture boundaries produce comparable logical snapshots through the same viewer, with precision tolerances fixed before comparison. |
| temporal structure inspection | Sequence playback and differences expose known creation, pruning, reinforcement and activity changes; gaps and ID reuse are unambiguous. |
| ModelSim/RTL conversion | A documented hex/binary field map decodes a known fixture into the canonical snapshot; truncation and unknown RTL values are surfaced. |
| DE1-SoC observation | Ethernet supplies the primary host stream with bounded capture buffering and loss reporting; optional VGA remains a display-only diagnostic path. |
| cross-backend structural validation | CPU/GPU/ModelSim/FPGA fixtures compare nodes, edges, bounds and structural changes at equivalent causal boundaries; record numeric/timing tolerances, machine-readable differences and unsupported coverage. |

Visual evidence supplements the core and hardware gates. Snapshot metadata, viewer layouts, transport timing and display refresh must not become computational inputs or impose a global neural clock.

## Hardware gate

Stabilize and version software event semantics before FPGA/VHDL and FPAA implementation. Compare reference traces for causality, predictions, classifications, state/connectivity bounds and energy/utility decisions. Predeclare precision, timing and analog tolerances; exact internal equality is not required. FPGA metering clocks must not impose a neural clock. FPAA energy approximations need not copy digital switching metrics. Record unsupported behavior and calibration limits.

