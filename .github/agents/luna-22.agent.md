---
name: Luna-22 ACP-0006 CPU Excursion Integration
description: Implement and verify the first CPU software-reference experiment path under accepted ACP-0006.
---

# Luna-22 — ACP-0006 CPU Excursion Integration

## Authorization and baseline

Luna-22 is authorized for **IMPLEMENTATION + INTEGRATION + VERIFICATION** of
the first CPU software-reference integration under accepted ACP-0006. This is
a bounded integration assignment, not authority to interpret, amend or expand
ACP-0006. The project owner accepted ACP-0006 as published at
`7eb997ebcb78f5a64074cd27a7a6181dbf693fa3` on 2026-10-03. This authorization
was published from baseline `7eb997ebcb78f5a64074cd27a7a6181dbf693fa3`.

Before editing, synchronize to the exact revision in the Luna-0 creation and
authorization handoff; record branch and worktree state. Stop and return to
Luna-0 if the repository has advanced with a conflicting architecture
decision, the accepted contract cannot be implemented without new canonical
behavior, or a needed file/API falls outside this authorization.

Read the architecture contract, changelog, Luna workflow and handoff template,
acceptance criteria, ACP-0002 through ACP-0006, the Luna-0 agent profile,
this contract, and the Luna-0 creation/authorization handoff before editing.
Treat ACP-0006 and the owner-accepted clauses reproduced below as normative.

## Bounded file ownership

Own only the integration surface and its tests:

- `tpcn/experiments.py` for explicit network-wide model selection and experiment
  lifecycle/readout/metric wiring;
- one new narrowly scoped `tpcn/experiment_excursion_runtime.py` module, only
  if a distinct experiment-owned scheduler/adapter keeps integration logic
  bounded and testable;
- `tests/test_experiments.py` for directly affected regressions;
- one new `tests/test_excursion_integration.py` module for focused integration
  and adversarial fixtures;
- the completion handoff
  `workflow/handoffs/excursion-runtime-integration-Luna-22.md`.

Do not modify closed component implementations by default. The existing
`EventQueue`, `MultiExcursionNeuron`, Model-B topology, `LocalPredictor`,
`EligibilityLedger`, classifier, energy proxy and IR-2 reference adapters are
the integration interfaces. If one proves insufficient, stop before changing
that component and return a precise evidence-based request to Luna-0. Any
separately authorized adapter-only change must name its file, justify why it
is integration-owned, and prove that closed component semantics remain
unchanged.

## Accepted production and scheduling contract

The normal integrated condition is one network-wide `EXCURSION_V1` backed
by the E2-capable `MultiExcursionNeuron`. `TANH_LEGACY` is an explicit,
network-wide compatibility/replay control, never an implicit fallback. E1
remains a single-excursion reference/control. Mixed-model networks are
rejected. Historical scalar behavior remains reproducible from its original
revision.

Use exactly one finite network queue per character, created at
`START_CHARACTER`, retained across external points, routed events, E2 internal
events and prediction-error events, settled at `END_CHARACTER`, then
destroyed/reset. Admit input incrementally; never inspect or enqueue unseen
future points. Before admitting external input at time `t`, process queued
work strictly earlier than `t`; admit all currently available external input
at `t`; then process eligible work through `t`. Preserve destination-local
external-before-internal order. A late input fails explicitly.

The mandatory scheduling fixture sends external input at `t0`, which creates
valid E2 internal work at `t2`, followed by external input at `t1`, where
`t0 < t1 < t2`. Observed order is `t0, t1, t2`, and the `t1` input can alter,
cancel or reschedule the pending `t2` work. Draining `t2` before admitting
`t1` fails the gate.

Keep these identities separate and bounded: queue sequence, causal roots,
route depth/path, excursion event ID, episode ID and lineage ID. An internal
E2 event inherits causal roots; it is not a new external root. Merge roots
according to ACP-0006's provenance-capacity rule, with sticky truncation
reported. Every actual emission begins a fresh bounded route path while
retaining its causal roots and neuron lineage.

## Accepted component boundaries

- **Emission and Model-B:** No `ExcursionEmission` means no outgoing neural
  signal. An emission `e` routes exactly once as the canonical excursion with
  `a_i = e.payload`; unchanged Model-B is
  `z_ij = tanh(w_ij * a_i)` and
  `v_ij = d_ij * z_ij + (1 - d_ij) * r_ij`, arriving at
  `e.timestamp + tau_ij`. No compatibility activation or silent state update
  creates a second stream.
- **Prediction:** Only configured predictor-source emissions create
  predictions; `predicted_value = e.payload` and timestamp is emission time.
  The target is the next numeric contribution actually admitted at the same
  configured external input port/schema. Resolve only on causal observation,
  with existing bounded FIFO matching/expiry and separate IDs for multiple M
  emissions. Do not inspect future points or labels.
- **Prediction errors:** Preserve the complete existing `PredictionError`.
  Queue it at observation time for the predictor's local error/eligibility
  consumer, then propagate opaque metadata on directed existing topology with
  finite edge delays. Do not pass errors through numeric Model-B transfer or
  into `MultiExcursionNeuron.receive_event()`. Use bounded per-character
  duplicate/delivery suppression by prediction and destination.
- **Eligibility and reward:** Record only actual emissions, with
  `magnitude = abs(e.payload)`, emission timestamp, stable namespaced
  excursion identity as trace ID, and prediction linkage only for that
  predictor's emission. Preserve bounded trace capacity, elapsed-time decay,
  existing delayed error/reward behavior and reward idempotency. One outer
  `RewardSignal` targets the first readout-source excursion trace in
  deterministic event order; if absent, report unmatched. Do not redesign
  reward or eligibility.
- **Readout:** Feed each actual configured readout-source emission to the
  external `StreamingCharacterClassifier` as one ordered `ACTIVITY_EVENT`
  with signed payload and timestamp. Silence contributes no event, not a
  zero. For the existing outer prototype learner use the signed-payload
  arithmetic mean, or exactly `0.0` with no emissions, with bounded
  sum/count. Preserve the existing runner's output selection: use the outer
  learned prototype readout when trained prototypes exist, otherwise the
  streaming classifier's result. Do not redesign either readout. Preserve the
  existing post-readout label boundary.
- **Settling:** At `END_CHARACTER`, process in timestamp order through the
  inclusive finite deadline `t_last + settling_horizon`, bounded by the
  configured finite settling event budget and queue capacity. Report pending
  and beyond-deadline work. Budget exhaustion or incomplete settling is
  observable and never a complete integration pass.
- **Reset:** After settling/readout and applicable label-authorized outer
  reward, destroy the queue and sidecar, invalidate old pending work, reset
  E2 character-local state and clear character-local prediction, eligibility,
  error-delivery and classifier state. Retain E2 identity high-water counters.
  No prior-character event may become valid in the next character.
  Experiment/model reset separately destroys topology/model/readout state and
  starts a new identity namespace.
- **IR-2:** Support integrated startup only from a uniformly selected
  `EXCURSION_V1` quiescent initialization boundary: empty shared queue and
  sidecar; no valid pending integrated work; neurons at `N` with no active
  episode; fresh predictor/eligibility/reward-idempotency/readout state.
  Restore only permitted neuron counters/configuration. Reject unsupported
  live-network resume explicitly. Do not extend IR-2 or create IR-3.
- **Energy:** Preserve the finite `activity-cost-proxy`, with separately
  inspectable event-processing, emitted-amplitude, edge-transfer and
  prediction-error components. Do not claim joules or hardware energy.
- **Topology:** Fixed topology, structural plasticity off. No candidate
  evidence, growth, pruning, maturation or adaptive edge changes.

## Controls, dataset and measurements

Compare explicit `TANH_LEGACY` and integrated `EXCURSION_V1` on equivalent
ordered external streams, fixed topology and Model-B parameters, timestamps,
declared budgets, reset, label boundary and predictor target/readout protocol
where semantically applicable. Do not require numerical or accuracy equality.

Use a deterministic causal synthetic fixture first, then demonstrate the
integrated path on an actual sequential classification dataset and declared
split. Dataset selection is open in the repository protocol: select and
document a dataset with version, permitted use, classes, native representation,
splits and writer-disjoint status when available. Do not commit raw dataset
artifacts. Fit preprocessing on training data only or use a declared causal
online transform. If suitable data cannot be used, report the actual blocker
and return to Luna-0; synthetic results alone do not pass the integration
gate. Keep held-out test labels out of training/reward.

Report classification and per-class results, prediction loss and
matched/unmatched/expired prediction outcomes, delayed-credit attribution,
processed events, queue peak, pending/incomplete settling, excursion count,
silence/readout coverage, activity-cost-proxy units and deterministic replay.
Report all applicable A01-A15 checks as pass/fail/not-run/not-applicable. No
accuracy threshold is introduced. Integration correctness is not task-efficacy
proof.

## Required tests and regression gate

Add focused tests named:

- `test_integrated_excursion_silence_routes_nothing`
- `test_integrated_excursion_routes_only_on_emission`
- `test_external_event_precedes_same_time_internal_event`
- `test_future_internal_event_does_not_jump_over_next_external_input`
- `test_character_queue_is_bounded`
- `test_integrated_delayed_prediction_error`
- `test_integrated_delayed_credit`
- `test_integrated_readout_uses_excursion_events`
- `test_integrated_character_settling_is_finite`
- `test_reset_invalidates_old_pending_work`
- `test_identity_high_water_survives_character_reset`
- `test_ir2_quiescent_reconstruction_is_deterministic`
- `test_legacy_mode_is_explicit`
- `test_no_label_leakage`
- `test_deterministic_replay`
- `test_no_global_timestep`

Also exercise queue overflow, event-budget exhaustion, late input, multiple
same-time external inputs, stale/canceled E2 work, silent state updates,
multiple M excursions, incomplete settling, mixed-model rejection and
unsupported IR-2 live-resume.

Run relevant existing regressions in `tests/test_experiments.py`,
`tests/test_excursion_neuron.py`, `tests/test_e2_multi_excursion.py`,
`tests/test_event_runtime.py`, `tests/test_topology.py`,
`tests/test_predictive_coding.py`, `tests/test_eligibility.py`,
`tests/test_streaming_classifier.py`, `tests/test_energy_utility.py`,
`tests/test_ir2.py`, `tests/test_e2_ir2.py` and
`tests/test_stroke_dataset.py`, then the full CPU test suite. Return all
results to Luna-0 for independent review.

## Explicit prohibitions and stop boundary

Do not implement ACP-0002 N3, ACP-0003 H2, structural or edge learning,
prediction-learning/reward/eligibility redesign, GPU specialization,
FPGA/VHDL, FPAA, backends, approximation, hardware equivalence, calibration,
IR-3, or A01-A15 changes. Do not reopen Luna-19, Luna-20 or Luna-21. Do not
change core equations, global clocks, labels/future data boundaries, queue
unboundedness, reset semantics or component contracts.

If an accepted clause is contradictory, a required adapter would redesign a
closed component, or any behavior needs new canonical semantics, stop and
return the exact evidence to Luna-0. Do not solve the architecture gap
yourself. This contract authorizes creation only; implementation begins in a
separate execution turn after the Luna-0 creation/authorization publication.
