---
tpcn_handoff:
  agent: "Luna-53"
  luna_identifier: "Luna-53"
  descriptive_name: "ACP-0008 Destination Retention Causal Confirmation"
  task_id: "luna-53-acp0008-destination-retention-20261008"
  component: "Retained-input E2 destination integration/discharge/emission mechanism"
  status: "complete - SUPPORTED within the frozen mechanism setup; independent review required"
  contract_version: "1.0"
  branch: "main"
  base_revision: "04305a2917195888cbbcccf378eba7971551e9b5"
  result_revision: "2e527934692d96439207b8e15ee6a99eab683a65"
  dependencies:
    - "Luna-53 authorization and contract at 04305a2917195888cbbcccf378eba7971551e9b5"
    - "Luna-45 frozen destination configuration and authenticated raw-route captures"
    - "Luna-46 corrected diagnostic and category strata"
    - "Luna-47A retained tau=800 accumulator inputs and results"
  owner: "Project owner; next reviewer is Luna-0 Architecture Guardian"
  classification:
    - "bounded mechanism confirmation"
    - "retained destination-arrival replay only"
    - "SUPPORTED only within the frozen setup"
    - "not task efficacy, network efficacy, production integration, or architecture promotion"
  hypothesis: "Changing only destination decay_rate_z from 0.0125 to 0.00125 causes an E2 discharge with linked canonical emission in at least one of 33 temporal-retention-limited streams, and none in the 75 drive-limited or 212 no-reception controls."
  counter_hypothesis: "The isolated tau=800 accumulation response does not transfer to E2 discharge/emission, or the response is not selective against the retained negative controls."
  interfaces_relied_on:
    - "tpcn.excursion_neuron.MultiExcursionNeuron and IntegrationConfig"
    - "tpcn.event_runtime.EventQueue and execute_bounded"
    - "Authenticated Luna-45 destination reception captures"
    - "Luna-46 recurrence/category result and Luna-47A retained inputs/results"
  label_information_boundary:
    - "PASS: runtime invocation accepts only retained arrivals and E1Config; category labels are excluded."
    - "Category strata appear only in result aggregation; no label, task outcome, or future point enters computation."
  timing_assumptions:
    - "Original retained timestamps and deterministic retained queue order; no global neural timestep."
    - "All reported time values are logical event time; no physical-time conversion is claimed."
  reset_boundaries:
    - "A fresh destination neuron and empty event queue per stream and condition."
    - "Internal E2 events are processed within each isolated stream; destination emissions are not routed onward."
  resource_bounds:
    - "320 streams and 235 destination arrivals in each phase."
    - "Queue capacity 128; neuron/runtime event budget 4096."
    - "Maximum observed processed events per stream: 6 control, 8 intervention; maximum queue occupancy 6."
    - "All 1,280 stream-condition-phase executions completed; no pending events, budget exhaustion, or clipping."
  authorized_scope:
    - "Replay authenticated retained destination arrivals through the existing E2 runtime."
    - "Compare historical decay_rate_z=0.0125 to exactly one predeclared intervention, 0.00125."
    - "Record local state, recurrence checks, discharges, canonical emissions, controls, provenance, and deterministic replay."
    - "Publish immutable run records, summary, and execution handoff; stop for independent Luna-0 review."
  unauthorized_scope:
    - "No upstream route or fixture rerun and no downstream routing of emitted events."
    - "No rate/gain/threshold/topology/qualification sweep or fallback configuration."
    - "No task efficacy, prediction utility, production parameter recommendation, architecture promotion, or hardware claim."
    - "No successor experiment authorization."
  controls:
    - "Execution code revision 2e527934692d96439207b8e15ee6a99eab683a65 is published on origin/main."
    - "Preflight passed: both 320-stream phases reconcile against 235 retained destination arrivals."
    - "Both historical control phases match the Luna-45 baseline across 320 streams and 235 integration traces with zero mismatches."
    - "Both control phases have identical phase-independent scientific digest; both intervention phases have identical phase-independent scientific digest."
    - "The 75 drive-limited and 212 no-reception streams are retained unchanged as negative controls."
  measurements:
    - "Control: zero threshold crossings, E2 integration discharges, or canonical emissions in all strata."
    - "Intervention: 19/33 temporal-retention-limited streams crossed threshold, discharged, and emitted canonically; 19/19 emissions link to the corresponding integration discharge."
    - "Those 19 streams exactly match the predeclared Luna-47A tau=800 crossing identities."
    - "Drive-limited: zero threshold crossings, discharges, or canonical emissions across 75 streams."
    - "No-reception: zero arrivals, zero state changes, zero discharges, and zero emissions across 212 streams."
    - "No clipping, event-budget exhaustion, pending events, or recurrence-audit failures; all 320 stream audits pass in each run."
    - "Verdict: SUPPORTED as a selective retained-input E2 mechanism result only."
  information_boundary_check:
    - "PASS: no labels, category names, or summary metrics are passed into run_stream."
    - "PASS: upstream_route_executed=false and destination_outputs_rerouted=false in each run artifact."
  hardware_mapping:
    - "Not applicable; no physical, FPGA, analog, or hardware-equivalence test was authorized or run."
  architecture_invariants_touched:
    - "No A01-A15 clause changed."
    - "Existing local event-time integration and finite bounded execution are exercised; no global neural timestep is introduced."
    - "ACP-0008 remains accepted, experimental, opt-in, and disabled by default."
  preserves:
    - "Luna-46 MIXED status and all original class identities."
    - "The result is a mechanism outcome, not task efficacy or general TPCN performance."
    - "Historical Luna-45/46/47 artifacts remain unmodified."
    - "No production parameter choice, ACP amendment, architecture promotion, or successor authorization."
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna53/__init__.py"
    - "experiments/luna53/config.json"
    - "experiments/luna53/protocol.json"
    - "experiments/luna53/run.py"
    - "tests/test_luna53_retention.py"
    - "artifacts/luna53/luna53-control-initial.json"
    - "artifacts/luna53/luna53-control-replay.json"
    - "artifacts/luna53/luna53-intervention-initial.json"
    - "artifacts/luna53/luna53-intervention-replay.json"
    - "artifacts/luna53/summary.json"
    - "workflow/handoffs/luna-53-acp0008-destination-retention-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added:
    - "tests/test_luna53_retention.py"
  tests_passing:
    - "python -m py_compile experiments\\luna53\\run.py tests\\test_luna53_retention.py"
    - "python -m experiments.luna53.run --preflight: PASS; 320 streams and 235 arrivals reconciled in each phase."
    - "python -m pytest tests\\test_luna53_retention.py -q: 6 passed."
    - "Focused E2 and Luna-45/Luna-46/Luna-47A/Luna-53 regression batch: 481 passed, 1 governed skip."
    - "python -m pytest -q on Python 3.11.4 / Windows: 1,704 passed, 1 governed Windows directory-symlink privilege skip."
    - "Control initial/replay and intervention initial/replay each executed in a separate fresh Python process; all four returned PASS."
    - "python -m experiments.luna53.run --summarize: PASS; contract verdict SUPPORTED."
  tests_failed: []
  tests_not_run:
    - "Independent Luna-0 review is pending by design."
    - "No efficacy, integration, successor, hardware, or architecture-promotion test was authorized."
  assumptions:
    - "The published contract's retained route records and Luna-47A strata are the authorized evidence boundary."
    - "Initial/replay phases are deterministic replays, not independent scientific samples."
  unresolved:
    - "Independent Luna-0 review of the published execution artifacts and interpretation remains required."
  recommended_next_agent:
    - "Luna-0 Architecture Guardian: read-only independent review of this handoff, protocol/runner, four immutable run records, summary, and execution revision; do not authorize a successor or architecture change."
---

# Luna-53 — ACP-0008 destination-retention mechanism execution

## Outcome and owned scope

**OBSERVED:** the historical `decay_rate_z=0.0125` control reproduced the
Luna-45 destination integration traces in both retained phases. Under the
single intervention `decay_rate_z=0.00125`, 19 of the 33
`TEMPORAL-RETENTION-LIMITED` streams produced new integration discharge with
linked canonical E2 emission. The set of 19 is exactly the predeclared
Luna-47A tau=800 crossing set. None of the 75 `DRIVE-LIMITED` streams
discharged or emitted; none of the 212 `NO-RECEPTIONS` streams received input,
changed state, discharged, or emitted.

The initial/replay phase-independent scientific digests are identical within
each condition. The recurrence oracle passed for all 320 streams in all four
executions. Every execution completed with an empty queue and no clipping or
budget exhaustion. The measured maximum was 8 processed events in one
intervention stream and queue occupancy never exceeded 6.

**INFERRED, narrowly:** the selected slower destination z decay transfers the
previously observed scalar retention response into the existing E2
discharge/emission path on the authenticated retained input set, without a
response in the two predeclared negative-control strata. This does not imply
task-level usefulness or generalization beyond this fixed replay.

No E2 production behavior, ACP, architecture clause, or protected historical
artifact was changed. The lane adds only the experiment runner/configuration,
its focused tests, run records, summary, and this documentation.

## Architecture evidence

| Clause / boundary | Evidence |
|---|---|
| A01-A02 local event-time behavior | Existing E2 state is exercised on retained timestamps; no global timestep was added. |
| A03 causal propagation | Only authenticated relay-to-destination arrivals are replayed; emitted destination outputs are not routed. No new propagation claim is made. |
| A06 prediction/error events | Not manipulated or measured by this experiment. |
| A07 information locality | Category labels are evaluator-only; `run_stream` receives only arrivals and configuration. |
| A08 bounded state/execution | Queue capacity 128, event budget 4096; no run exhausted bounds; recurrence and pending-event audits pass. |
| A15 observability boundary | Per-event traces are downstream-only artifacts and do not affect computation. |

**HYPOTHESIZED before execution:** `decay_rate_z=0.00125` would yield a
selective E2 response on some retention-limited streams. **OBSERVED:** 19
streams responded with discharge and linked canonical emission and both
negative-control groups remained non-responding. ACP-0008 stays experimental,
opt-in, and disabled by default. No hardware mapping or architecture
promotion is inferred.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m experiments.luna53.run --preflight` | Execution revision `2e527934692d96439207b8e15ee6a99eab683a65`; Python 3.11.4 / Windows | PASS; 320 streams and 235 destination arrivals reconciled in both phases | Each run's `provenance.phase_reconciliation` |
| Control initial execution | Fresh process; execution revision above | PASS; Luna-45 baseline compatibility; 320 streams / 235 traces; zero mismatches | Control initial run record |
| Control replay execution | Separate fresh process | PASS; Luna-45 baseline compatibility; 320 streams / 235 traces; zero mismatches | Control replay run record |
| Intervention initial execution | Separate fresh process; control gate passed first | PASS; 320 streams; recurrence audit and bounds pass | Intervention initial run record |
| Intervention replay execution | Separate fresh process; control gate passed first | PASS; 320 streams; exact same-condition scientific replay | Intervention replay run record |
| `python -m experiments.luna53.run --summarize` | Execution revision above | PASS; contract verdict SUPPORTED; no-reception invariant PASS | `artifacts/luna53/summary.json` |
| `python -m pytest tests\test_luna53_retention.py -q` | After four results were generated | 6 passed | Luna-53 focused tests |
| Focused E2 and retained-evidence batch | Python 3.11.4 / Windows | 481 passed, 1 governed skip | E2 runtime, Luna-45, Luna-46, Luna-47A, and Luna-53 tests |
| `python -m pytest -q` | Execution revision above; Python 3.11.4 / Windows | 1,704 passed, 1 skipped; zero failures | Existing Luna-46 directory-symlink privilege limitation |

An earlier pre-execution artifact-presence check was run before the four
outcome files existed; it was rerun after generation and passed. The
pre-execution check did not alter or overwrite evidence.

## Benchmark and resource results

This is not a sequential classification benchmark. Dataset splits,
classification, prediction loss, energy, utility, topology utilization, and
latency metrics are **not applicable**. This experiment measures only the
frozen local destination mechanism:

| Condition / stratum | Streams | Arrivals | Threshold-crossing streams | Discharge streams / count | Canonical emission streams / count |
|---|---:|---:|---:|---:|---:|
| Control — temporal-retention-limited | 33 | 126 | 0 | 0 / 0 | 0 / 0 |
| Intervention — temporal-retention-limited | 33 | 126 | 19 | 19 / 19 | 19 / 19 |
| Control — drive-limited | 75 | 109 | 0 | 0 / 0 | 0 / 0 |
| Intervention — drive-limited | 75 | 109 | 0 | 0 / 0 | 0 / 0 |
| Control — no-receptions | 212 | 0 | 0 | 0 / 0 | 0 / 0 |
| Intervention — no-receptions | 212 | 0 | 0 | 0 / 0 | 0 / 0 |

All phase/condition runs had 320/320 completed stream executions, 0 pending
events, 0 budget exhaustion, 0 clipping, and 320/320 recurrence-oracle
passes. The historical control compared 235 destination traces per phase
with no mismatches. Maximum processed events per stream was 6 for control
and 8 for intervention; maximum observed queue occupancy was 6 of capacity
128. The configured event budget was 4096 per stream.

## Evidence identities

| Artifact | SHA-256 |
|---|---|
| `artifacts/luna53/luna53-control-initial.json` | `cc9530821835c8df002ca6d9c9f8ec3df005fd1223c1e8f60ced70d65f82395c` |
| `artifacts/luna53/luna53-control-replay.json` | `3398e98bd1230d78bd973b486e732b623f79d3db14083642cf9d31f1ab878366` |
| `artifacts/luna53/luna53-intervention-initial.json` | `93a4c52b0ba079942b98040c7c8b7fa1fdc94da8685b06f8ce8f0ab0b3d4d818` |
| `artifacts/luna53/luna53-intervention-replay.json` | `b733da050b2b4223cddf02ed7d8c6c0e3859f6000f330e89b828972cee54625c` |
| `artifacts/luna53/summary.json` | `a647be0f6dfe09d0cf51b6dc0d9ee5e250db989f4ae87b82377401ecefadba03` |

Control initial/replay scientific digest:
`5a33d0c9700a7b72b594cfa476657bc3e82b2dfd397646bf2aae5482ae304181`.
Intervention initial/replay scientific digest:
`41624a5bf4e39af7ae96dc8598eb57c2cab1ca313ed5a72019caca2b427ec502`.
The result files retain distinct fresh-process execution IDs and byte hashes.

## Assumptions, limitations and unresolved issues

- The outcome is limited to these authenticated retained destination inputs,
  the stated E2 configuration, and the tested Python/Windows runtime.
- The two phases are deterministic replays, not independent samples.
- The 19 observed emissions establish neither useful downstream computation
  nor improved classification, prediction, energy, or utility.
- Exact hardware behavior and cross-platform numerical identity were not
  tested.
- Independent Luna-0 review of the published evidence and interpretation is
  still required. No successor or production integration is authorized.

## Reproduction and rollback

Use the published execution revision and preserve the existing result files.
The runner refuses output overwrite and requires both compatible controls
before intervention:

```powershell
python -m experiments.luna53.run --preflight
python -m experiments.luna53.run --run-one --phase initial --condition control --execution-id luna53-control-initial-2e52793
python -m experiments.luna53.run --run-one --phase replay --condition control --execution-id luna53-control-replay-2e52793
python -m experiments.luna53.run --run-one --phase initial --condition intervention --execution-id luna53-intervention-initial-2e52793
python -m experiments.luna53.run --run-one --phase replay --condition intervention --execution-id luna53-intervention-replay-2e52793
python -m experiments.luna53.run --summarize
```

The four run artifacts and summary are immutable published evidence; do not
delete or regenerate them in place. The exact execution code and frozen
configuration remain available at the recorded execution revision.

## Next assignment

**Luna-0 Architecture Guardian — independent, read-only review.** Review the
authorization, execution code/configuration, all four retained run records,
summary, artifact hashes, protocol interpretation, and validation record.
Confirm the narrow mechanism claim and architecture boundaries. Do not
authorize a successor, production integration, ACP amendment, or architecture
promotion in this review.
