# Luna-0 independent review — Luna-31 Luna-12E EXCURSION_V1 observable compatibility

```yaml
tpcn_handoff:
  agent: Luna-0
  task_id: "luna-0-independent-review-luna-31-luna12e-e2-observable-compatibility-20261004"
  contract_version: "1.2"
  status: "complete"
  branch: main
  base_revision: "9efc5f1bb509c916a5499e421fbc51bc60101cb2"
  architecture_change: false
  proposal: null
  terminal_verdict: "PASS — LUNA-31 LUNA-12E EXCURSION_V1 OBSERVABLE COMPATIBILITY CORRECTION INDEPENDENTLY VERIFIED / CLOSED"
```

## Revisions and lineage
- Review start: `9efc5f1bb509c916a5499e421fbc51bc60101cb2` (`test: align Luna-12E observables with EXCURSION_V1`); branch main, HEAD == origin/main, clean.
- Authorization baseline `8d5f7f5` -> authorization publication `2177038` -> implementation/handoff `9efc5f1`; ancestry verified. The opaque token `F9h8m...` is not a Git revision and was not used.

## Publication scope
`git diff 2177038..9efc5f1` touches exactly `tests/test_luna12e_integration.py` and the Luna-31 handoff. 0 production, workflow, ACP, Luna-12L, spiral, visualization or hardware paths changed.

## Test audit
- First three historical component tests unchanged (diff contains no hunks in them); classified lower-level topology component regressions, not authorization of integrated E2 pruning.
- Rename `..._and_prediction_loss_changes` -> `test_experiment_readout_consumes_routed_activity_and_topology_changes_work`: semantic rename; all original routing assertions (no-edge absence, with-edge trace, event_count increase) retained. Collection 908 -> 909 (rename + one added TANH test); no deletion/xfail/skip/deselect.
- Explicit `neuron_model="EXCURSION_V1"` in both migrated tests (hardening, no runtime change).

## Independent reproduction (Python 3.11.5)
- No-edge: no `neuron-0 -> neuron-1` trace; event_count 12; edge_transfer_proxy 0.0; maximum_route_depth 0.
- With edge (neuron-0 -> neuron-1, delay 1.0): real trace entries — EXCURSION at t=1.5 and routed prediction_error at t=2.0; event_count 14; edge_transfer_proxy 1.358357398350786; maximum_route_depth 1.
- prediction_loss: 1.1724999999999999 in both. Migrated test requires only finiteness. Delta NOT REQUIRED FOR THIS FIXTURE (fixture-specific; no claim that loss cannot depend on topology).
- Causal-oracle sufficiency: trace + event count + transfer proxy + route depth are all real runtime observations; oracle STRENGTHENED, not weakened.
- Identity: object ids stable across repeated evaluate.
- Fixture timestamps: `make_synthetic_workload(1, 2)` yields points at t=0.0 and 1.0 (inspected). Hard-coded `last_external_timestamp = 1.0` ACCEPTABLE: the test builds the fixed two-point workload itself and the value is scoped to it.
- Settling horizon 4.0; expected terminal 5.0; observed both neurons 5.0, mode `E1Mode.N`, state 0.0, `pending_event is None` (from accepted character-destruction semantics; test only reads public properties). The test observes post-evaluation terminal state, not the instant before the next character's first input.
- TANH_LEGACY (explicit model): clocks [0.0, 1.0]; cannot run against the default model.
- "Not a gate" governance interpretation: the TANH test is a normal collected regression that participates in the suite; "not a gate" meant only that legacy timing is not a premise for the E2 oracle. Imprecise phrasing, not a defect.

## Verification
- `tests/test_luna12e_integration.py`: 6 passed.
- EXCURSION_V1 integration, E2 multi-excursion, E2 IR-2, Luna-28 growth, predictive-coding/multi-hop routing: 152 passed.
- Full suite: 899 passed, 9 failed, 1 skipped, 909 collected. Failures: 8 in `test_luna12l_temporal_scale.py` and 1 in `test_spiral_benchmark.py` (known structural-plasticity configuration error "structural plasticity is unavailable unless structural observation is enabled"); 0 Luna-12E; 0 new regressions. Skip: `test_gpu_visualization.py:61` CUDA unavailable. Failures not repaired.
- `compileall -q tpcn tests`: exit 0. `git diff --check`: clean. Diagnostics on the test file: none (reported by Luna-31 and unchanged since).

## Architecture audit
A01 PASS; A02 PASS; A03 PASS; A04 PASS; A06 PASS (loss-delta removed as fixture-stale oracle); A07 PASS; A08 PASS; A15 PASS FOR SOFTWARE REFERENCE ONLY.
Contract 1.2 UNCHANGED; ACP-0007 UNCHANGED; ACP required NO; architecture change NO; production change NO; E2 pruning and N3 NOT AUTHORIZED.

## Status
- Luna-12E observable compatibility: ESTABLISHED
- Causal routed-topology exercise: ESTABLISHED
- Task efficacy / prediction-loss benefit / resource benefit / hardware equivalence: NOT ESTABLISHED
- Successor: NOT AUTHORIZED (Luna-32 not authorized; Luna-12L/spiral migration not chosen)

## Terminal verdict
PASS — LUNA-31 LUNA-12E EXCURSION_V1 OBSERVABLE COMPATIBILITY CORRECTION INDEPENDENTLY VERIFIED / CLOSED
