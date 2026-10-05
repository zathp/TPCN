# Luna-39 Handoff — ACP-0008 Propagation-to-Emission Mechanism Diagnostic

```yaml
tpcn_handoff:
  agent: Luna-39
  task_id: "luna-39-acp0008-propagation-emission-diagnostic-20261005"
  status: "complete; returned to Luna-0"
  base_revision: "5ff87535ace61137892f7063a81f5f63e542fa4d"
  result_revision: "see Git log (commit containing this file)"
  verdict: "SUPPORTED under STATIC_N2_BOUND_SENSITIVITY only"
  experiment_type: "bounded mechanism-only diagnostic"
  production_changes: false
  architecture_promotion: false
  next_authorized: "none"
```

## Starting state and scope

Fetched `origin/main` before editing. At start:

- `HEAD == origin/main == 5ff87535ace61137892f7063a81f5f63e542fa4d`
- worktree clean
- revision matches the authorized Luna-39 baseline.

The committed `.github/agents/luna-39.agent.md` governed execution. Exactly the
six authorized files were added:

- `run_luna39_acp0008_propagation_emission_diagnostic.py`
- `tests/test_luna39_acp0008_propagation_emission_diagnostic.py`
- `artifacts/acp0008-luna39-propagation-emission-diagnostic/config.json`
- `artifacts/acp0008-luna39-propagation-emission-diagnostic/results.json`
- `artifacts/acp0008-luna39-propagation-emission-diagnostic/summary.json`
- this handoff.

No production, runtime, eligibility, neuron, routing, ACP, governance, Luna-33
through Luna-38, or historical evidence files were changed. No threshold or
integration sweep, task-efficacy test, growth or pruning test, or Luna-40 was
run or authorized.

## Design and fixed configuration

The runner reused the Luna-34 input/character helper and Luna-37 capacity
path read-only. It consumed only each example's `points`, transformed each
point as `point.x + point.y`, preserved same-timestamp batching, and used
the declared seeds, stream order, neutral reward, topology, and bounds.

| Parameter | Value |
|---|---|
| Seeds | `0, 1, 2, 3, 4` |
| Streams per seed | 64 |
| Arms | `LEGACY_REPRODUCTION`; `ACP0008_INTEGRATION` |
| Conditions | `NO_EDGE_CONTROL`; `DEFAULT_STATIC_EDGE` (`w=1.0`); `STATIC_N2_BOUND_SENSITIVITY` (`w=2.0`) |
| Full executions | `2 × 3 × 5 × 64 = 1920` |
| Source neuron, both arms | `MultiExcursionNeuron(E1Config())` |
| Legacy destination | `MultiExcursionNeuron(E1Config())` |
| Integrated destination | `MultiExcursionNeuron(E1Config(integration=IntegrationConfig()))` |
| `theta_E` | `1.0`, read from the configured neuron |
| Integration config | `decay_rate_z=0.1`, `input_gain=1.0`, `discharge_quantum (theta_Z)=1.0`, `z_max=4.0` |
| Eligibility capacity | explicit `1024` per ledger through the Luna-36 runtime API |
| Edge | source to destination, delay `1.0`, divider `1.0`, reference `0.0` |

The source configuration is identical in both arms; destination integration
is the sole neuron-configuration intervention. The destination has no outgoing
edge. Each character gets fresh neurons. The full run was replayed in full.

## Historical-equivalence and stream checks

**LEGACY ARM REPRODUCES LUNA-37.** The gate passed:

| Condition | Source emissions | Transfers | Destination receptions | Destination canonical emissions |
|---|---:|---:|---:|---:|
| `NO_EDGE_CONTROL` | 1715 | 0 | 0 | 0 |
| `DEFAULT_STATIC_EDGE` | 1715 | 1715 | 1715 | 0 |
| `STATIC_N2_BOUND_SENSITIVITY` | 1715 | 1715 | 1715 | 0 |

The source-emitting-character pattern is `59 / 59 / 59 / 59 / 61` by seed,
for `297/320` emitting characters in every arm and condition. Across arms,
source input events and source canonical emissions (identity, time and
payload), and the routed transfer identities, times, transformed values,
delays, receive order/count and route depth match exactly.

One runtime-global metadata field differs: `receive_sequence` differs on 171
paired transfer records after destination-only events consume global queue
sequence numbers. Those sequence values are retained in the per-event result;
they do not change the transfer identities, relative receive order, arrival
times, payloads, delays, or route depth. No source event or source-generated
routing behavior changed. This scheduler-metadata distinction is reported for
independent review rather than hidden.

## Quantitative results

Every table row below summarizes 320 characters (64 for each of five seeds).
“Receiving characters” is the number with at least one destination reception;
“emitting characters” is the number with at least one destination canonical
emission. Reception, state update, slow-state accumulation, discharge,
transfer, and canonical emission are counted separately.

| Arm | Condition | Source emitting chars | Receiving chars | Emitting chars | Source emissions | Transfers / receptions | Fast-state changes | `z` accumulations | Discharges | Destination emissions (integrated / direct) | Max `|z|` | Max `|x|` | Max route depth | Peak / max-final ledger occupancy | Runtime events |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Legacy | No edge | 297/320 | 0/320 | 0/320 | 1715 | 0 / 0 | 0 | 0 | 0 | 0 (0 / 0) | 0 | 0 | 0 | 19 / 19 | 9394 |
| Legacy | Default `w=1` | 297/320 | 297/320 | 0/320 | 1715 | 1715 / 1715 | 1715 | 0 | 0 | 0 (0 / 0) | 0 | 0.685455 | 1 | 19 / 19 | 11109 |
| Legacy | N2 `w=2` | 297/320 | 297/320 | 0/320 | 1715 | 1715 / 1715 | 1715 | 0 | 0 | 0 (0 / 0) | 0 | 0.932688 | 1 | 19 / 19 | 11109 |
| ACP-0008 | No edge | 297/320 | 0/320 | 0/320 | 1715 | 0 / 0 | 0 | 0 | 0 | 0 (0 / 0) | 0 | 0 | 0 | 19 / 19 | 9394 |
| ACP-0008 | Default `w=1` | 297/320 | 297/320 | 0/320 | 1715 | 1715 / 1715 | 1715 | 1715 | 0 | 0 (0 / 0) | 0.763164 | 0.685455 | 1 | 19 / 19 | 11109 |
| ACP-0008 | N2 `w=2` | 297/320 | 297/320 | 27/320 | 1715 | 1715 / 1715 | 1715 | 1715 | 31 | 31 (31 / 0) | 1.118173 | 1.913373 | 1 | 19 / 19 | 11186 |

Per seed, the integrated N2 condition produced:

| Seed | Source emissions | Destination-emitting characters | Integrated destination emissions | Max `|z|` | Peak / final occupancy |
|---:|---:|---:|---:|---:|---:|
| 0 | 338 | 4/64 | 5 | 1.118173 | 18 / 18 |
| 1 | 361 | 9/64 | 10 | 1.099432 | 17 / 17 |
| 2 | 306 | 4/64 | 4 | 1.066626 | 17 / 17 |
| 3 | 314 | 4/64 | 4 | 1.051841 | 17 / 17 |
| 4 | 396 | 6/64 | 8 | 1.074559 | 19 / 19 |

No-edge cells had no edge, transfer, destination reception, destination
integration trace, slow-state activity, or destination emission. They are
valid negative controls in both arms. Default-edge cells received 1715
transfers and updated destination state but emitted zero times in both arms.

## Emission classification and timing evidence

The integration-enabled destination produced **31 canonical emissions on
27/320 characters, all under the predeclared `w=2` condition**. The default
`w=1` and no-edge conditions produced none. All 31 were independently
classified from trace state as `integrated_discharge`; there were zero direct
emissions. Each has at least two temporally distributed integrated receptions,
nonzero retained `z` before the final input, a `theta_Z` discharge, and the
canonical emission at the ordinary `emission_delay` afterward. The 31 detailed
timing reconstructions and all 3430 destination integration trace entries are
in `results.json`.

There were 4 additional destination emissions beyond the first emission in
each emitting character. Distinct-emitter counts in the N2 condition were:
27 characters with both source and destination emitters, 270 with the source
only, and 23 with no emitter.

Across those emission reconstructions, the retained contributing-reception
count ranged from 2 to 17; consecutive contributing arrivals were separated
by 12.927767 to 79.889902 time units. The measured slow-state retained fraction
between consecutive contributing receptions ranged from 0.000339 to 0.274507.

Representative trace (`seed 0`, `c00-001`, `w=2`):

1. At `t=1.5`, routed input `-0.87228433696` yields `z=-0.87228433696`.
2. At `t=20.49604433079`, the next routed input is `-0.91337250374`, after a
   gap of `18.99604433079`. Decay retains fraction `0.1496277953`, leaving
   `z=-0.13051798224` immediately before the second input.
3. The second input contributes `-0.91337250374`, giving `z=-1.04389048598`
   before discharge. The destination discharges `-1.0` at that event time.
4. The destination emits canonically at `t=20.99604433079`, following the
   configured `0.5` emission delay.

Thus the observed N2 emissions use retained evidence across multiple routed
inputs. They are not inferred from reception, nonzero state, or a stored
classification flag alone.

## Capacity, settling, and replay

- Effective runtime capacity and each of the two ledgers: `1024`.
- Across all 3840 ledger records: all occupancy equations reconcile as
  `0 + created - removed = final`.
- No capacity errors; maximum peak and final occupancy: `19/1024`.
- Per cell, eligibility creations/removals: legacy `1715/0` in each condition;
  integrated no-edge and `w=1` `1715/0`; integrated `w=2` `1746/0` (1715
  source plus 31 destination emissions).
- No character had incomplete settling; per-character runtime-event use and
  settling evidence are retained.
- Full-run replay digests are equal:
  `5a19be65e2386e585eb50877c80f3114ee7383fda7b2a8324642440618b963d6`.

## Classification and interpretation boundary

- `LEGACY ARM REPRODUCES LUNA-37`
- `INTEGRATED DESTINATION EMISSION PRESENT ONLY UNDER STATIC N2 SENSITIVITY`
- `STATIC N2 CHANGES RESULT RELATIVE TO DEFAULT`

The bounded H1 mechanism is **supported only under the predeclared
`|w|=2` sensitivity condition**. It is not observed at the default static
edge (`w=1`). This result does not establish task efficacy, ACP-0007 candidate
formation, structural growth, pruning usefulness, accuracy, temporal
specificity, generality, calibration, hardware equivalence, or ACP-0008
promotion. ACP-0008 remains experimental and opt-in. Luna-37 remains
historically **NOT SUPPORTED IN THIS SETUP** under its prior architecture;
Luna-34 remains **BLOCKED / UNDETERMINED**; Luna-33 and ACP-0007 are
unchanged.

Inherited non-blocking Luna-38 follow-ups remain out of scope: integration
export to IR-2/TPCV-2, package-root `IntegrationConfig` export, the private
`_z` setup in Luna-38 fixture I, and parameter calibration.

## Validation

| Check | Result |
|---|---|
| Focused Luna-39 tests | 8 passed |
| Full suite | 998 passed, 1 skipped |
| Collected | 999 |
| Skip | CUDA visualization test; CUDA unavailable in this environment |
| Test-count change | +8 Luna-39 tests over the reviewed 990 passed / 1 skipped / 991 collected baseline |
| `compileall` | clean |
| Pylance syntax checks | no syntax errors in runner or tests |
| `git diff --check` | clean |

## Return

Returned to Luna-0 for independent post-Luna-39 review. No Luna-40 is
authorized.
