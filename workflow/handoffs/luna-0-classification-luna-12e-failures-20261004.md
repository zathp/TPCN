# Luna-0 Classification — Luna-12E Downstream Failures

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Classify Luna-12E routed-topology and legacy-observable failures"
  task_id: "luna-0-classification-luna-12e-failures-20261004"
  component: "Luna-12E experiment integration downstream test compatibility"
  status: "classified — no implementation or successor authorized"
  contract_version: "1.1; ACP-0006 integration remains unchanged"
  branch: "main"
  base_revision: "22a0fa59622a11e14bc2688406708717c68379d9"
  result_revision: "documentation-only classification publication"
  dependencies:
    - "Accepted Luna-12E topology integration"
    - "Luna-22 EXCURSION_V1 CPU integration and Luna-26 route correction"
  owner: "Luna-0 Architecture Guardian"
  classification: ["READ-ONLY FAILURE CLASSIFICATION", "GOVERNANCE"]
  hypothesis: "The two listed failures are legacy-observable assertions made incompatible by the later EXCURSION_V1 default; the first test still demonstrates reachable-edge routing."
  counter_hypothesis: "Either failure demonstrates broken event routing or failed character-state reset under the current E2 contract."
  interfaces_relied_on:
    - "ExperimentConfig default neuron_model"
    - "ExperimentRunner.evaluate and last_neurons"
    - "ExcursionCharacterRuntime prediction, settling, and character destruction paths"
    - "BoundedTopology routing and event trace"
  label_information_boundary:
    - "No labels or future data were introduced or used as computational inputs in the classification."
  timing_assumptions:
    - "EXCURSION_V1 uses event-local clocks and an inclusive END_CHARACTER settling horizon."
    - "Character boundaries permit resetting local neuron state and clock origin."
  reset_boundaries:
    - "Runtime start resets neuron state to the character's first timestamp."
    - "Character destruction resets character-local state at the settling horizon."
  resource_bounds:
    - "Classification uses the two bounded existing tests and their fixed two-node topology/workload."
  authorized_scope:
    - "Reproduce and classify only the two known Luna-12E failures."
    - "Publish read-only evidence in this handoff, workflow, and changelog."
  unauthorized_scope:
    - "No Luna-28 creation or execution."
    - "No production/test edits, blanket failure repair, architecture change, or downstream migration."
  controls:
    - "Run only the two known failing tests."
    - "Compare their creation/model lineage with the later EXCURSION_V1 default."
    - "Compare no-edge versus reachable-edge runtime observations."
  measurements:
    - "Focused test run: 2 failed, both at the legacy prediction-loss/exact-clock assertions."
    - "No-edge versus edge: processed events 12 -> 14; edge-transfer proxy 0 -> 1.358357398350786; max route depth 0 -> 1."
    - "Prediction loss remained 1.1724999999999999 in both conditions."
    - "For the clock fixture, final local clocks were [5.0, 5.0]; identity remained stable."
  information_boundary_check:
    - "Prediction targets remain admitted inputs only; this review does not change information flow."
  hardware_mapping:
    - "Software CPU experiment-path classification only; no hardware claims."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A15"]
  preserves:
    - "Current EXCURSION_V1 event-local clock, settling, and reset semantics."
    - "Established routed-edge causal effect."
    - "21 downstream failure classification; these two remain counted within it."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-classification-luna-12e-failures-20261004.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
  tests_added: []
  tests_passing:
    - "Reachable-edge trace and processed-event count differ between no-edge and edge conditions in the reproduced fixture."
    - "Neuron identity assertion passes across repeated evaluate calls."
  tests_failed:
    - "test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes: only prediction_loss-difference assertion fails."
    - "test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary: first exact post-evaluation clock assertion fails."
  tests_not_run:
    - "No full suite."
    - "No alternate legacy-model comparison run; historical source lineage was inspected."
    - "No candidate remediation or Luna-28 work."
  assumptions:
    - "The 2026-09-27 pre-E2 Luna-12E test/default lineage identifies these assertions as legacy-model observables, not E2 invariants."
  unresolved:
    - "A future authorized compatibility task may choose explicit TANH_LEGACY fixtures or E2-appropriate causal assertions; no choice is made here."
    - "The two failures remain in the known 21-failure downstream count."
  recommended_next_agent: []
```

## Classification result

**OBSERVED:** on current `main`, only the two requested tests were executed:

```text
C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe -m pytest -q tests/test_luna12e_integration.py::test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes tests/test_luna12e_integration.py::test_runner_keeps_neuron_identity_across_points_and_resets_at_character_boundary
```

Result: **2 failed**. No production or test files were changed.

### 1. Reachable-edge routing versus `prediction_loss`

**OBSERVED:** the first test passes its no-edge route absence check, its
with-edge trace-presence check, and its processed-event-count comparison. The
focused diagnostic measured:

| Measure | No edge | `neuron-0 -> neuron-1` edge |
|---|---:|---:|
| `prediction_loss` | `1.1724999999999999` | `1.1724999999999999` |
| processed event count | 12 | 14 |
| edge-transfer proxy | 0.0 | 1.358357398350786 |
| maximum route depth | 0 | 1 |

With the edge, the processed event trace includes a delayed
`EXCURSION` delivery from `neuron-0` to `neuron-1` at `t=1.5` and a routed
`prediction_error` event from `neuron-0` to `neuron-1` at `t=2.0`. Thus the
failure is **not evidence that the edge has no causal routing effect**:
reachability, delivered routed activity, event count, edge cost, and route
depth all change.

The failing assertion is specifically the expectation that this one-way
downstream edge must change aggregate `prediction_loss`. In the current
runtime, prediction loss is accumulated when admitted external values are
observed against predictions. Predictions for this scalar target are created
from emissions at `predictor_source`; the tested edge terminates at
`neuron-1` and does not feed back into `neuron-0`. Delivered error traffic
does not retroactively alter the error already measured at the source. The
equal loss therefore coexists with direct routed-topology causation.

**INFERRED:** this is a legacy fixture expectation, not a topology-routing
failure. `test_experiment_readout_consumes_routed_activity_and_prediction_loss_changes`
was introduced in commit `2e8d800b` when the integrated network used
`TPCNNeuron`. The Luna-22 E2 integration later made `EXCURSION_V1` the default
in `ExperimentConfig` (`a206f2e8`); the Luna-12E test module is unchanged
since the pre-E2 parent. This classification does not claim that the current
fixture demonstrates a topology-induced prediction-loss delta. It does
establish that the explicit loss-delta assertion is not a valid proxy for
whether routed topology is causally exercised.

### 2. Neuron identity, character reset, and exact terminal clocks

**OBSERVED:** the test's neuron-identity assertion passes. The failure occurs
on the next assertion, which expects `last_neurons[0].clock.timestamp` to be
exactly `0.0`; pytest observes `5.0`. A focused reproduction reports final
clocks `[5.0, 5.0]`.

The workload points are timestamped `0.0` and `1.0`. The current default
`settling_horizon` is `4.0`, so `END_CHARACTER` settles through
`last_external_timestamp + settling_horizon == 5.0`. The runtime's
`_destroy_character(horizon)` then resets each E2 neuron at that horizon.
When the next character starts, `start_character` resets neurons to that
character's first timestamp before admitting its inputs. `MultiExcursionNeuron`
reset clears `x`, mode, pending work, and other character-local state while
establishing the supplied local-clock timestamp.

The test observes the neurons after the complete evaluation pass; it does not
inspect neutral state immediately before the next character's first event.
Its expected final times `0.0` and `1.0` are inherited per-point-clock
expectations, not the current E2 lifecycle's final clock values.

**INFERRED:** this failure does not establish a missing reset or a violation
of local event time. It is an exact-clock compatibility failure caused by
observing the final settled/reset state using the old scalar-clock oracle.
The identity portion still passes. A future E2-specific verification should
observe reset state at the character boundary and separately assert the
declared settling/local-time behavior, rather than requiring the final clock
to equal the last input-point timestamps.

## Architecture and governance disposition

No A01-A15 or ACP-0006 change is indicated by this classification:

- **A01/A02 — no global clock defect shown:** these are per-neuron logical
  clocks; the configured settling horizon and explicit character reset are
  local/runtime boundaries.
- **A03/A04 — routed causal effect observed:** edge delivery is delayed,
  bounded, and visible in the trace.
- **A06 — no conclusion on predictive efficacy:** the local prediction-loss
  value is unchanged in this particular one-way intervention.
- **A07 — no label/future leakage observed or introduced.**
- **A08 — the fixture remains under configured settling/event bounds.**
- **A15 — software-reference evidence only.**

**HYPOTHESIZED:** future compatibility work should make model choice and
observable expectations explicit: preserve a legacy-only assertion under an
explicit legacy model, or define an E2 fixture in which the selected
topology intervention can causally affect the metric under test. This is
only a classification/recommendation, not an implementation assignment.

The two tests remain in the published 21 downstream failures until a
separately scoped decision addresses them. No issue is attributed to TPCV-2.
**Luna-28 is not created, executed, or authorized.**

## Validation record

| Command/procedure | Environment | Result |
|---|---|---|
| Focused execution of the two named test cases | Windows, Python 3.11.5, clean `main` at `22a0fa59622a11e14bc2688406708717c68379d9` | **2 failed**, at the described prediction-loss and exact-clock assertions |
| Diagnostic reproduction of no-edge/edge and final-clock observations | Same interpreter and current checkout; deterministic workload/configuration from the tests | Event count `12 -> 14`; edge trace appears; loss remains exactly equal; final clocks `[5.0, 5.0]`; identity stable |
| Historical lineage check | Git history | Test authored with `TPCNNeuron` network and unchanged when the default later moved to `EXCURSION_V1` |
| Full repository suite | Not run | Not run |

## Next assignment

**No next Luna is authorized.** Return this classification to the project
owner/Luna Prompt Generator for a separate decision on downstream
compatibility. Do not dispatch Luna-28 or change the existing suite as part
of this review.
