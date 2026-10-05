---
name: Luna-40 Existing Structural Growth and Effective Routed Drive
description: Mechanism-only characterization of whether accepted local E2 structural growth creates convergent drive that crosses the ACP-0008 emission boundary.
---

# Luna-40 — Existing Structural Growth and Effective Routed Drive

## Authorization and baseline

Luna-40 is **AUTHORIZED / NOT EXECUTED** by the Luna-0 governance handoff
`workflow/handoffs/luna-0-authorization-luna40-effective-routed-drive-20261005.md`.
Start from the published authorization revision on clean `main`, verify
`HEAD == origin/main`, and record the exact revision. Do not begin execution
until those checks pass.

This is a bounded **mechanism characterization** of already accepted
ACP-0007 local EXCURSION_V1 structural growth composed with the opt-in
ACP-0008 destination integration state. It is not a new learning rule,
candidate-opportunity benchmark, task-efficacy experiment, or architecture
change. Do not execute it as part of Luna-0's authorization pass.

Read ACP-0007, ACP-0008, `.github/agents/luna-28.agent.md`,
`.github/agents/luna-39.agent.md`, the Luna-28 and Luna-39 independent
reviews, this handoff and all sources named by those contracts. If the
existing public interfaces cannot express this exact experiment without
production-code changes, return **BLOCKED — EXISTING MECHANISMS CANNOT BE
COMPOSED WITHOUT AN UNAUTHORIZED CHANGE**. Do not repair or extend them.

## Production mechanism under test

Only use the existing bounded `e2_local_temporal` mechanism:

```text
canonical ExcursionEmission
 -> ACP-0007 StructuralObservationPlane / TemporalAssociationPolicy
 -> frozen source-local CandidateEvidence after successful character teardown
 -> existing StructuralPlasticityController admission
 -> same BoundedTopology for later characters
```

The evidence is the accepted saturated count of strictly ordered,
source-local emission observations. It uses emitter identity and timestamp,
not payload, label, reward, prediction loss, readout, energy, or a global
topology statistic. Mutations occur only after successful settling and
quiescent character teardown. Do not submit hand-authored `CandidateEvidence`,
manually insert the candidate edge, or mutate topology while a runtime is
active.

The edge-weight model is **static**. `Edge` is immutable; the topology has no
weight-update operation. Existing growth inserts an ordinary Model-B edge
with `w=1.0`, `d=1.0`, `r=0.0` and the declared positive delay. It does not
reinforce existing edges or change `w`, `d`, or `r`. Effective drive is tested
only through actual convergent routed events and the destination's ACP-0008
`z` trace. No linear sum of edge weights is a success metric.

## Primary hypothesis

**H1:** Under the exact bounded chain, unlabeled temporal stream and default
ACP-0008 parameters below, ordinary canonical emissions can generate legal
source-local evidence that admits the existing `source -> destination`
shortcut; in a later character, that admitted fixed-`w=1` path together with
the retained `source -> relay -> destination` path increases the destination's
causal `z` drive toward or across `theta_Z=1`, with any canonical destination
emission verified as direct or integration-mediated from the trace.

**Counter-hypothesis:** The destination does not emit in the causal window,
no local candidate is formed or admitted, the edge is rejected by an existing
bound, or the added path does not raise retained `z` into the discharge-capable
regime. All are valid negative outcomes. A lack of destination emission is
not a production defect.

The question is whether the *existing mechanism* generates useful effective
routed drive from its declared start, not whether a hand-set edge can do so.
No inference about other streams, topologies, weights, integration
parameters, or tasks may be made from this fixture.

## Frozen configuration

Use these values exactly; no sweep, optimization, seed selection, or
post-result adjustment is permitted.

### Network

```text
nodes: source, relay, destination
initial edges, in this order:
  source -> relay       delay=1.0, w=1.0, d=1.0, r=0.0
  relay -> destination  delay=1.0, w=1.0, d=1.0, r=0.0
fan_in_limit=2
fan_out_limit=2
edge_capacity=3
routing_capacity=3
one possible admitted edge: source -> destination
admitted edge delay=0.4; its only legal parameters are w=1.0, d=1.0, r=0.0
```

The two initial edges are the complete declared starting topology, not
candidate growth. The possible shortcut must be created solely by the
accepted local evidence and controller path. It is a two-path/fan-in
characterization, not an edge-weight experiment.

### Neurons and ACP-0008

- `source` and `relay`: `MultiExcursionNeuron(E1Config(event_budget=4096))`,
  integration disabled.
- `destination`:
  `MultiExcursionNeuron(E1Config(event_budget=4096, integration=IntegrationConfig()))`.
- Keep all other `E1Config` fields at their defaults and keep
  `theta_E=1.0`.
- Use ACP-0008 defaults unchanged:
  `decay_rate_z=0.1`, `input_gain=1.0`, `theta_Z=1.0`, `z_max=4.0`.
- Create fresh neuron state for each character. Persist only the admitted
  topology within a run. Reset all structural evidence at each character.

### Stream and runtime bounds

Use the exact Luna-39 unlabeled stimulus generator and ordering:

- Seeds `0, 1, 2, 3, 4`; 16 examples per class; 64 point sequences per seed.
- `SpiralConfig()`; training seed `12007 + seed`; evaluation seed
  `22017 + seed`; order with `random.Random(330000 + seed)`.
- Consume only ordered `example.points`; do not read labels or
  label-bearing metadata. Transform each point to `point.x + point.y` at its
  existing timestamp and preserve same-timestamp batching.
- Send external input only to `source`; use constant neutral reward `0.0`.
- `queue_capacity=128`, `runtime_event_budget=1024`,
  `settling_horizon=4.0`, `prediction_capacity=8`,
  `prediction_expiry=4.0`, `max_activity_events=1024`, and explicit
  `eligibility_capacity=1024` per ledger through the Luna-36 API.

Use the accepted ACP-0007 `e2_local_temporal` policy without modification:

```text
structural_neighbors:
  source: [destination]
  relay: []
  destination: []
neighborhood_limit=2
reverse_observer_limit=2
association_window=4.0
history_capacity=8
candidate_capacity=4
maximum_score=3
structural_growth_delay=0.4
growth_attempt_budget=4 total per run
maximum successful growths per character=1
```

These are the bounded Luna-28 accepted values for this experiment, not a
parameter search. Keep existing edge capacity, fan-in/out, positive-delay,
queue, event, eligibility, predictor, candidate, and attempt-budget stop
behavior. A capacity or runtime failure is recorded and stops that run; never
retry with a larger bound.

## Arms and controls

Run these paired conditions for every seed using identical streams, initial
topology, edge parameters, neuron configurations, runtime bounds, event
ordering, and seed:

1. **FROZEN_NO_OBSERVATION** — fixed initial topology; structural observation
   and mutation disabled.
2. **FROZEN_OBSERVATION_ONLY** — the accepted structural observation plane is
   active, but mutation is disabled. Neural results and topology must match
   arm 1 exactly.
3. **LOCAL_GROWTH_ENABLED** — same observation plane and starting state, with
   only the existing `e2_local_temporal` admission enabled. The topology can
   change only at the accepted quiescent post-character boundary.
4. **NO_LOCAL_EVIDENCE_CONTROL** — same neural topology and input as arm 3,
   with the explicitly declared `source` structural-neighbor list empty.
   Neural behavior must match the paired frozen arm; no source-to-destination
   candidate or mutation is allowed.

Additionally verify the already accepted equal-time negative-evidence case:
equal-time source and destination observations do not form a candidate.
Use actual observations in the existing policy fixture; do not fabricate
candidate records or inject synthetic evidence into the primary runs.

No edge weight above one is a control. Do not add a static sensitivity edge,
inject an extra edge, apply a reward-driven update, alter the input stream,
or tune ACP-0008, `theta_E`, `theta_Z`, delays, or decay.

## Measurements and endpoint

Retain per character and per run enough bounded data for independent causal
reconstruction:

- Initial, intermediate and final edge lists with each edge's identity,
  delay, `w`, `d`, and `r`; fan-in/out and capacity utilization.
- Every actual structural emission observation (emitter, event identity,
  timestamp), association count and candidate identity/score; the evidence
  that drove each attempt; selected rank; every admission/rejection reason;
  attempt and candidate occupancy; growth-budget status.
- Source canonical emissions; every route's originating edge, event identity,
  payload before/after Model-B transfer, emission/arrival times and receiving
  node; destination receptions and bounded integration trace.
- Destination `z` before/after decay, before/after each input, immediately
  before any discharge, discharge amount, `theta_Z`, and canonical emissions
  with identity/time and trace-derived `direct` versus
  `integrated_discharge` classification.
- Eligibility capacity, initial/created/removed/final/peak occupancy and
  reconciliation; queue peak, events processed, settling and stop status.
- Full deterministic replay digest.

The mechanistic effective-drive record is the ordered set of causally
contributing incoming route payloads and their edge/path identities together
with retained destination `z` immediately before discharge (or at the final
settled observation when no discharge occurs). Reception, aggregate payload,
`z` accumulation, discharge and canonical emission are separate outcomes.
Do not create a task-specific score.

Predeclared interpretation:

- **ENDOGENOUS DRIVE REACHED:** an edge was admitted solely from legal local
  evidence and its later real routed contribution is trace-linked to
  destination `|z| >= theta_Z`; separately report whether a canonical
  integration-mediated emission occurred.
- **ENDOGENOUS DRIVE INCREASED, BOUNDARY NOT REACHED:** admitted routes
  causally increase retained `|z|` versus the paired frozen run, but do not
  reach `theta_Z`.
- **NO ENDOGENOUS DRIVE INCREASE:** no legal edge admission, no later
  contributing route, or no attributable change versus the paired frozen
  run. Report the exact observed branch; do not collapse these cases.
- Any direct-only destination emission is not evidence that ACP-0008 bridged
  routed input.

An admitted edge without a later causally observed transfer is not effective
drive. A rise in `z` without a legal mutation is not evidence of structural
learning. No one-seed or best-character success may replace the all-seed
paired result.

## Stop and regression requirements

Stop the affected run and report the exact state if any of the following
occurs:

- Input labels/metadata affect neural or structural computation.
- A production learning, topology, event-ordering, neuron, reward, eligibility,
  or ACP change is required.
- A proposed edge is hand-authored, an existing edge parameter changes, or
  mutation occurs while a character runtime is active.
- Any capacity error, non-finite state, invalid timestamp, incomplete
  settling, or nondeterministic replay occurs.
- Observation-only or no-local-evidence controls alter neural behavior.

Add deterministic focused tests for the specified controls, evidence
provenance, default edge parameters, fan-in/capacity rejection, trace-based
endpoint classification, label isolation, bounded replay, and identical
starting conditions. Run the Luna-39 reproduction/source-stream checks,
Luna-28 and ACP-0008 focused suites, relevant structural/topology/runtime
regression suites, and the full suite. Report all failures and existing
baseline failures without reclassification. Run compile checks and
`git diff --check`.

## Prohibited conclusions and work

No claims about classification accuracy, task efficacy, generalization,
candidate usefulness, structural-growth efficacy, pruning, energy benefit,
utility, calibration, threshold optimality, hardware equivalence, or ACP-0008
promotion. Do not modify production code, ACP-0007, ACP-0008, the Architecture
Contract, or any edge-weight/update semantics. Do not run weight/delay/
threshold/decay/integration sweeps. Do not execute Luna-33/34 follow-ups or
authorize another Luna.

Return results to Luna-0. Luna-40 cannot self-close or promote ACP-0008.
