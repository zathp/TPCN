---
name: Luna-34 EXCURSION_V1 Multi-Emitter Candidate-Formation Bridge
description: Determine whether task-derived EXCURSION_V1 inputs can produce a second within-character emitter over a fixed bounded Model-B edge; mechanism only, not efficacy.
---

# Luna-34 — EXCURSION_V1 Multi-Emitter Candidate-Formation Bridge

## Authorization and baseline

```text
Luna-0 -> Luna-34 -> Luna-0
```

Luna-34 is **AUTHORIZED / NOT EXECUTED** by the bounded decision in
`workflow/handoffs/luna-0-post-luna33-candidate-formation-bootstrap-decision-20261004.md`.
The verified starting revision is
`1e2f80aa9e37b332e0637f6ff8b0df18d5f2ceb6`; use the public APIs at that
revision. The work is a **MECHANISM EXPERIMENT + OBSERVATION + CAUSAL
DIAGNOSTIC**, not task efficacy, architecture promotion, or an ACP amendment.
Return all results and any public-API limitation to Luna-0. Do not self-close
or authorize another Luna.

## Scientific question

Does the current canonical EXCURSION_V1 transfer/integration path permit
label-free task-derived temporal input to produce a second distinct
within-character emitter over a declared fixed Model-B edge, and thus permit
a legal ACP-0007 temporal candidate before any task-efficacy question is
asked?

**H1:** At least one fixed-edge condition produces a destination canonical
emission after a source emission within the same character; with the declared
source-to-destination evidence neighborhood and `0 < dt <= 4.0`, the
structural observation plane consequently exposes a legal candidate.

**Counter-hypothesis:** No destination emitter/candidate occurs in the
predeclared streams and conditions, or the required events/evidence cannot be
observed through existing public APIs. Preserve which edge condition, if
any, establishes the bridge; a negative result does not authorize changing
the contract.

The primary gate is the occurrence of a second distinct emitter, before any
topology mutation. A legal candidate is the subsequent evidence gate. No
successful edge admission is required.

## Binding architecture and exclusions

Use accepted `workflow/docs/architecture_proposals/ACP-0007.md` as the
unchanged structural-evidence contract. Candidate evidence requires actual
canonical emissions, source-local earlier/later observations, a declared
neighbor, and the accepted positive association interval. Evidence is
character-local and resets at every character boundary.

Do not treat a routed reception as a canonical emission. Do not carry
evidence across characters. Do not change neuron thresholds/amplitudes,
`ExperimentRunner` input semantics, public APIs, Model-B bounds, or ACP-0007.
Do not run or report classification accuracy, class correctness, held-out
benefit, prediction benefit, resource benefit, or an efficacy endpoint.
Labels, readout results, rewards based on correctness, and class-derived
metadata are excluded from the experiment and artifacts. Sample provenance
may use only opaque deterministic IDs.

No pruning, N3, learned edge parameters, nonzero edge reference, altered
divider, arbitrary weight search, architecture promotion, or hardware
equivalence is authorized.

## Public interfaces

Use only:

- `make_spiral_dataset`, `SpiralConfig`, and generated point sequences as
  temporal inputs;
- `MultiExcursionNeuron` with its default `E1Config`;
- `Edge`, `BoundedTopology.from_edges`, and `BoundedTopology.route`;
- `ExcursionCharacterRuntime` and its public character/input/result
  interfaces;
- `StructuralObservationPlane` and its public emission/freeze interfaces.

The existing experiment input transform is `point.x + point.y` at the point's
declared timestamp. Reproduce the Luna-33 training point sequences for seeds
0-4 using 16 examples per class from `make_spiral_dataset` with
`train_seed=12007 + seed`, `evaluation_seed=22017 + seed`, and
`SpiralConfig()`, then use the declared per-seed training order stream
`random.Random(330000 + seed)`. Read only each example's `points`; never read,
pass, persist, or derive a result from its label or label-bearing metadata.
Use an opaque ID derived only from seed and sequence index.

For each character and edge condition, start fresh neutral neurons and
character-local structural evidence. Use a two-node network (`source`,
`destination`) and a static observation map declaring only
`source -> destination`, with explicit finite limits. Route the source's
EXCURSION events through the fixed topology. The topology/evidence neighbor
map must be fixed before execution and identical across paired conditions.
Keep evidence character-local; do not adapt topology.

Use the same explicit bounds for every condition:

```text
nodes = 2
edge_capacity = 1
routing_capacity = 1
fan_in_limit = 1
fan_out_limit = 1
propagation_delay = 1.0
queue_capacity = 128
runtime_event_budget = 1024 per character
neuron = MultiExcursionNeuron(config=E1Config())  # default finite E1Config
settling_horizon = 4.0
prediction_capacity = 8
prediction_expiry = 4.0
max_activity_events = 1024
structural_neighborhood_limit = 1
structural_reverse_observer_limit = 1
structural_history_capacity = 8
structural_candidate_capacity = 4
structural_association_window = 4.0
structural_maximum_score = 3
structural_growth_delay = 0.4
```

Each seed has 64 training characters; the complete paired design therefore
has 320 input streams and 960 character-condition executions. The no-edge
arm has zero active edges while retaining the same declared edge capacity
and observation map. Group equal-timestamp points into the public runtime's
same-timestamp external batch without changing point order.

## Predeclared conditions and controls

Use the same generated streams, node configuration, positive propagation
delay `1.0`, and finite execution bounds in every condition:

1. **NO_EDGE_CONTROL:** no route edge; retain the same declared
   source-to-destination observation neighborhood.
2. **DEFAULT_STATIC_EDGE:** one `source -> destination` Model-B edge with
   `edge_weight=1.0`, `divider_strength=1.0`, `reference=0.0`.
3. **STATIC_N2_BOUND_SENSITIVITY:** one otherwise identical edge with
   `edge_weight=2.0`, `divider_strength=1.0`, `reference=0.0`. This is the
   accepted static N2 bound only, predeclared as transfer-bound sensitivity;
   it is not outcome tuning.

Do not test other weights or alter delay, divider, reference, neuron
thresholds, or amplitudes after seeing outcomes. Declare and retain finite
node, edge, fan-in/out, queue, event, history, candidate, score, settling,
and per-character resource bounds above in the run configuration. Retain
event-level emission/route evidence only up to each character's 1024-event
execution bound; never retain a cross-character neural history.

## Required observations and measurements

For every seed, condition, and character, retain bounded evidence sufficient
to independently reconstruct:

- actual canonical source and destination emissions, with emitter identity,
  event identity, timestamp, payload sign, and magnitude;
- each routed contribution's emission and arrival timestamp, transformed
  payload, positive delay, destination receive count, maximum route depth,
  and edge-transfer proxy;
- inter-emission intervals, consecutive routed-contribution sign runs, and
  the maximum decayed destination accumulator magnitude before threshold
  crossing, observed directly or inferred/replayed from the public canonical
  equations and trace;
- distinct emitters per character, characters with at least two distinct
  emitters, source-before-destination interval checks, and candidate counts
  from the frozen public `StructuralObservationPlane` snapshot;
- execution completion, pending work, settling, queue/event bounds, and
  deterministic replay digests.

Deduplicate canonical emissions by emission identity and emitter identity;
never count multiple observation-plane recipients of one emission as
multiple emitters. A candidate is valid only if its actual canonical source
emits at `t_s`, its distinct declared neighbor emits later at `t_d`, and
`0 < t_d - t_s <= 4.0` in the same character.

Use only a constant neutral reward. Runtime readout output may be produced by
the existing adapter but must not be read, scored, or serialized. Do not
measure or inspect class correctness, accuracy, prediction benefit, resource
benefit, or held-out benefit as an endpoint.

## Frozen transfer expectations

The inspected default `E1Config` has `theta_E=1.0` and `A_max=1.0`.
`Edge` applies the canonical signal transform
`d * tanh(w * payload) + (1-d) * reference`. With neutral reference zero,
signal-only `d=1`, and `|payload| <= A_max`, a default edge has maximum
single-transfer magnitude `tanh(1) < 1`; at the accepted `|w| <= 2` static
bound it is at most `tanh(2) < 1`. A single routed ordinary payload therefore
cannot independently cross `theta_E` from neutral state. Treat repeated
temporally accumulated routed contributions as the mechanism under test, not
as a defect. Do not initialize a neuron non-neutrally.

## Predeclared terminal classifications

Report the following as independent mechanism axes; do not force a single
success-shaped summary:

- `MULTI-EMITTER BRIDGE ESTABLISHED`
- `MULTI-EMITTER BRIDGE NOT ESTABLISHED UNDER DEFAULT EDGE`
- `STATIC N2 TRANSFER SENSITIVITY ESTABLISHED`
- `CANDIDATE FORMATION ESTABLISHED`
- `CANDIDATE FORMATION NOT ESTABLISHED`
- `BLOCKED — EXISTING PUBLIC API INSUFFICIENT`

A bridge under the `w=2` sensitivity condition does not imply a bridge under
the default edge. Report the bridge separately for every edge condition.
`STATIC N2 TRANSFER SENSITIVITY ESTABLISHED` requires at least one paired
input stream where the `w=2` condition produces a downstream canonical
emitter or legal candidate absent under `w=1`; a routed-payload magnitude
difference alone does not meet this classification. Candidate formation is
established only from actual distinct canonical emissions and the ACP-0007
interval/locality test. A blocked result must identify the smallest missing
public interface or contract; do not implement it.

## Exact owned files

Luna-34 may add/change only:

```text
run_luna34_excursion_v1_multi_emitter_bridge.py
tests/test_luna34_excursion_v1_multi_emitter_bridge.py
artifacts/acp0007-luna34-multi-emitter-bridge/config.json
artifacts/acp0007-luna34-multi-emitter-bridge/results.json
artifacts/acp0007-luna34-multi-emitter-bridge/summary.json
workflow/handoffs/luna-34-excursion-v1-multi-emitter-candidate-formation-bridge-20261004.md
```

All production/core/runtime/API files, `ExperimentRunner` semantics,
`ExperimentConfig`, E1/E2 thresholds, topology transfer code, structural
observation/association code, ACP-0007, Architecture Contract, workflow,
changelog, Luna-33 files/artifacts, and historical Luna-12L/Luna-13F evidence
are prohibited. If the owned-file scope or an accepted semantic must change,
stop and return to Luna-0.

## Completion and return

Add focused deterministic tests for the public runtime path, emitted/routed
identity reconciliation, distinct-emitter counting, per-character reset,
candidate locality/order/window, fixed Model-B conditions, absence of label
use, negative results, and serialized-result determinism. Run the focused
tests, experiment once to its authorized output directory, compile the
runner/tests, and `git diff --check`. Do not perform a parameter sweep or a
task-efficacy retry.

Return to Luna-0 with the exact baseline/revision, commands/environment,
per-seed and per-condition mechanism evidence, passed/failed/not-run checks,
terminal classifications, uncertainties, and evidence supporting or
falsifying the bridge. Keep the claim bounded to the declared streams and
static edges. The result is not task efficacy, A14 promotion, resource or
prediction benefit, or hardware validation.
