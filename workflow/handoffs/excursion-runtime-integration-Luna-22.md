# Luna-22 Completion Handoff — ACP-0006 CPU Excursion Integration

```yaml
tpcn_handoff:
  agent: "Luna-22"
  luna_identifier: "Luna-22"
  descriptive_name: "First CPU software-reference excursion integration"
  task_id: "excursion-runtime-integration-Luna-22"
  component: "CPU experiment event path"
  status: "partial; IR-2 boundary correction verified, downstream full-suite compatibility review required"
  contract_version: "1.1"
  branch: "main"
  base_revision: "c13deb06427c64d00f603b1b1a1c75e442392fb8"
  result_revision: "commit containing this handoff; see git history"
  dependencies:
    - "Accepted ACP-0006 at 7eb997ebcb78f5a64074cd27a7a6181dbf693fa3"
    - "ACP-0002 N2 static Model-B edge transfer, closed"
    - "ACP-0003 H1 Execution IR/backend interface, closed"
    - "ACP-0004 E1/E2 excursion runtime, closed"
    - "ACP-0005 TPCN-IR-2 revision 1, closed"
    - "Luna-21 corrective implementation, independently verified and closed"
  owner: "Project owner"
  classification:
    - "IMPLEMENTATION"
    - "INTEGRATION"
    - "VERIFICATION"
  hypothesis: "A bounded experiment-owned scheduler can integrate E2 excursions into the CPU character stream using existing closed component interfaces while preserving causal input watermarks, emission-only routing, label isolation and character reset."
  counter_hypothesis: "A required existing consumer or integration behavior cannot be supported within Luna-22's owned files without expanding scope or changing closed component semantics."
  interfaces_relied_on:
    - "ExperimentRunner and ExperimentConfig"
    - "MultiExcursionNeuron and ExcursionEmission"
    - "EventQueue and bounded event execution"
    - "BoundedTopology and unchanged Model-B route transfer"
    - "LocalPredictor, Prediction and PredictionError"
    - "EligibilityLedger, EligibilityActivity and RewardSignal"
    - "StreamingCharacterClassifier"
    - "LocalEnergyModel and RewardAdjustedUtility"
    - "IR-2 E2 quiescent reconstruction"
    - "StrokePoint sequential dataset interface"
  label_information_boundary:
    - "Neural execution, prediction observation, topology routing and local eligibility do not receive labels."
    - "Labels are consulted only after character readout for the outer reward and prototype update."
    - "Only actually admitted numeric contributions are prediction targets; future points are not pre-enqueued."
  timing_assumptions:
    - "Logical timestamps are monotonic; there is no global neural timestep."
    - "Before external input at t, strictly earlier queued work is processed; available same-time external inputs are admitted before eligible same-time internal work."
    - "END_CHARACTER settles through the inclusive finite deadline last_external_timestamp + settling_horizon."
    - "Event budget exhaustion, pending work and beyond-deadline work are reported as incomplete."
  reset_boundaries:
    - "One queue and sidecar are created per character and destroyed after settling, readout and applicable outer reward."
    - "Character-local predictor, classifier, ledger, error delivery and neuron episode state are reset."
    - "E2 event identity high-water counters survive character reset."
    - "Experiment reset separately rebuilds model, topology, readout and identity namespace."
  resource_bounds:
    - "Finite per-character queue capacity, processing budget, settling horizon, prediction capacity/expiry and classifier activity capacity."
    - "Causal-root sidecar capacity follows E2 provenance capacity; root truncation is sticky and reported."
    - "Bounded route depth/path, event identities and prediction-error delivery suppression."
    - "Fixed finite topology; structural plasticity is rejected for EXCURSION_V1."
    - "Finite activity-cost-proxy counters; no physical-energy calibration is claimed."
  authorized_scope:
    - "tpcn/experiments.py experiment selection and lifecycle/readout/metric wiring"
    - "One experiment-owned bounded adapter module"
    - "Directly affected experiment tests and focused integration/adversarial tests"
    - "This Luna-22 completion handoff"
  unauthorized_scope:
    - "Changing closed neuron, event queue, topology, predictor, eligibility, classifier, energy or IR-2 component semantics"
    - "Changing A01-A15 or ACP-0002 through ACP-0005"
    - "Structural or edge learning, prediction/reward/eligibility redesign, IR-3, GPU/FPGA/FPAA, backend approximation or hardware equivalence"
    - "Migrating downstream visualization and research consumers whose APIs are outside Luna-22 ownership"
  controls:
    - "Normal model: network-wide EXCURSION_V1 backed by MultiExcursionNeuron"
    - "Explicit compatibility/replay control: network-wide TANH_LEGACY"
    - "No mixed-model network; no silent excursion-to-legacy fallback"
    - "Fixed topology and structural plasticity off"
  measurements:
    - "Causal ordering, queue occupancy/capacity, processed events, settling completion, emissions/silence, prediction outcomes, delayed credit, readout coverage and activity-cost-proxy components"
    - "Deterministic synthetic fixtures and deterministic held-out UCI Character Trajectories subset"
    - "Full CPU suite result and downstream compatibility failures"
  information_boundary_check:
    - "Synthetic relabeling tests produce identical neural traces and energy."
    - "UCI preprocessing uses current-point x_velocity + y_velocity only; no test labels or future points are used for neural execution."
    - "Writer-disjointness is unavailable in the dataset metadata."
  hardware_mapping:
    - "Python CPU software reference only; no backend or hardware-equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "A01-A15 text and accepted ACP-0006"
    - "Closed ACP-0002 N2, ACP-0003 H1, ACP-0004 E1/E2 and ACP-0005/TPCN-IR-2 semantics"
    - "TANH_LEGACY explicit control and historical revision reproducibility"
    - "Fixed topology and structural-plasticity-off first integration"
  architecture_change: false
  proposal: "ACP-0006, accepted by project owner on 2026-10-03"
  files_changed:
    - "tpcn/experiments.py"
    - "tpcn/experiment_excursion_runtime.py"
    - "tests/test_experiments.py"
    - "tests/test_excursion_integration.py"
    - "workflow/handoffs/excursion-runtime-integration-Luna-22.md"
  tests_added:
    - "tests/test_excursion_integration.py: required scheduler, routing, prediction, credit, readout, settling, reset, IR-2, labels, replay and no-global-timestep cases"
    - "tests/test_excursion_integration.py: queue overflow, event-budget/watermark exhaustion, late input, stale E2 work, mixed models, structural-plasticity rejection and live IR-2 resume"
    - "tests/test_experiments.py: explicit legacy-control behavior and utility/event-stream parity"
  tests_passing:
    - "Focused: 41 passed, including IR-2 residual/provenance rejection."
    - "Prescribed experiment/component regressions including the new integration tests: 318 passed."
    - "python -m compileall -q tpcn tests: passed."
    - "Pylance diagnostics on tpcn/experiments.py, tpcn/experiment_excursion_runtime.py and tests/test_excursion_integration.py: no diagnostics."
    - "git diff --check: passed."
    - "UCI Character Trajectories deterministic CPU subset execution completed; benchmark details below."
  tests_failed:
    - "Full CPU suite before the IR-2 boundary correction: 27 failed, 767 passed, 1 skipped. Failures are outside Luna-22's owned files and are detailed below."
  tests_not_run:
    - "A separately retained, executable benchmark script for the UCI run; the run used session-only data and an ad-hoc loader and is not directly replayable from the repository."
    - "Per-class UCI metrics were not retained in the available benchmark output."
  assumptions:
    - "The stratified subset split is deterministic with seed 20261003; the exact ad-hoc split/loader code was not retained as a repository artifact."
    - "The tested UCI split is a small protocol demonstration, not a dataset-scale efficacy result."
  unresolved:
    - "Existing CPU visualization assumes scalar-neuron activation fields absent from MultiExcursionNeuron."
    - "Existing structural/research experiment consumers rely on implicit legacy defaults or structural plasticity, both incompatible with the accepted EXCURSION_V1 default and fixed-topology first integration."
    - "Luna-0 must decide whether to authorize a bounded downstream compatibility/migration task or whether the affected consumers should explicitly select TANH_LEGACY."
    - "Luna-0's independent review requested evidence that quiescent IR-2 startup rejects residual state and unassigned provenance; this has been added to the adapter and focused tests."
  recommended_next_agent:
    - "Luna-0 Architecture Guardian: independently review this handoff and the full-suite failures; define the authorized scope for downstream consumer migration before further edits."
```

## Outcome and owned scope

**OBSERVED:** The experiment runner now explicitly selects a uniform
`EXCURSION_V1` network by default. `TANH_LEGACY` remains an explicit
network-wide compatibility/replay control. A character-scoped adapter owns one
finite queue and sidecar across the full input stream, routes only actual
`ExcursionEmission` values, and joins the existing prediction, error,
eligibility, classifier, reward, energy-proxy and IR-2 interfaces.

**OBSERVED:** The mandatory `t0 → t1 → t2` fixture proves that the `t1`
external input is admitted before pending `t2` E2 work. It can cancel or
reschedule that work, and the internal work retains both input causal roots.
The added budget/watermark regression proves that budget exhaustion refuses a
later external input while strictly earlier work remains queued.

**OBSERVED:** All changes are limited to the four authorized implementation
and test files plus this completion handoff. Closed component implementations
and architecture contracts were not changed.

## Architecture evidence

| Invariant | Status | Evidence and limits |
|---|---|---|
| A01 — event-driven computation | PASS | Irregular-time/no-global-timestep and watermark ordering fixtures pass; no global neural tick was added. |
| A02 — local time and intrinsic temporal state | PASS | E2 internal-event ordering and existing E2 regressions pass; character reset bounds local state. |
| A03 — finite propagation | PASS | Emission routes through unchanged positive-delay Model-B topology; focused test verifies delayed arrival and transfer payload. |
| A04 — bounded topology | PASS | Existing bounded-topology regressions pass; queue capacity/overflow and event-budget fixtures pass. |
| A05 — no spatial reservoir | PASS | The integration uses no reservoir implementation or spatial reservoir state. |
| A06 — predictive coding | PASS, mechanics only | Synthetic integration test observes a delayed target and explicit PredictionError. On the real UCI subset, matched predictions were zero; predictive task efficacy is not established. |
| A07 — local learning | PASS | Relabeling leaves neural trace and energy unchanged; eligibility records only emitted excursions and delayed credit test passes. |
| A08 — bounded dynamics | PASS | Finite queue, sidecar, event budget, route/provenance limits, expiry, settling and incomplete-work reporting are tested. |
| A09 — local energy | PASS | Energy-proxy components are separately exposed and the integration asserts their sum; no joule or hardware-energy claim is made. |
| A10 — energy is not simply minimized | PASS, existing policy plus integration parity | Existing utility regression retains useful expensive work and suppresses unproductive work; integration event-only/utility ablation yields identical neural trace and energy, so utility does not suppress neural execution in this integration. |
| A11 — delayed credit | PASS | Synthetic delayed reward matches an emitted excursion eligibility trace; existing idempotency/eligibility regressions pass. |
| A12 — optional multiple pathways | NOT APPLICABLE | Luna-22 does not add or claim multiple computational pathways. |
| A13 — optional explicit gating | NOT APPLICABLE | Luna-22 does not add or claim explicit learned pathway gating. |
| A14 — structural plasticity | NOT APPLICABLE | Accepted first integration keeps topology fixed and rejects structural plasticity for EXCURSION_V1; no structural-learning claim is made. |
| A15 — hardware independence | PASS, software-reference scope | The integration uses hardware-neutral CPU software interfaces. No hardware mapping or equivalence is claimed. |

No A01-A15 text or canonical component semantics were changed.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_experiments.py tests/test_excursion_integration.py` | Windows, Python 3.11.5 | 41 passed after IR-2 correction | Focused Luna-22 test run. |
| `python -m pytest -q tests/test_experiments.py tests/test_excursion_neuron.py tests/test_e2_multi_excursion.py tests/test_event_runtime.py tests/test_topology.py tests/test_predictive_coding.py tests/test_eligibility.py tests/test_streaming_classifier.py tests/test_energy_utility.py tests/test_ir2.py tests/test_e2_ir2.py tests/test_stroke_dataset.py tests/test_excursion_integration.py` | Windows, Python 3.11.5 | 318 passed after IR-2 correction | Prescribed regression set including the focused tests. |
| `python -m pytest -q` | Windows, Python 3.11.5 | 27 failed, 770 passed, 1 skipped after IR-2 correction | Full-suite output captured during execution; failure groups listed below. |
| `python -m compileall -q tpcn tests` | Windows, Python 3.11.5 | Passed | Exit code 0. |
| Pylance diagnostics for the two changed production modules and integration test | Workspace interpreter, Python 3.11.5 | No diagnostics | Each targeted `textDocument/diagnostic` returned an empty item list. |
| `git diff --check` | `main`, base `c13deb06427c64d00f603b1b1a1c75e442392fb8` | Passed | Exit code 0. |
| UCI Character Trajectories CPU experiment | DOI `10.24432/C58G7V`; deterministic subset seed `20261003`; settling horizon 10 logical seconds | Completed all test characters; metrics below | Data remained session-local and raw files were not committed. |

### Independent Luna-0 review and corrective follow-up

**OBSERVED:** Luna-0 reviewed the integration as a partial result and found a
specific ACP-0006 IR-2 startup gap: nonzero residual `x` and unassigned
provenance were not rejected before E2 reconstruction. The reviewer requested
a bounded correction in this runtime and its focused test module, with no
changes to `ir2.py` or closed components.

**CHANGED:** `from_quiescent_ir2()` now rejects nonzero residual state,
positive unassigned-provenance count, or sticky unassigned-provenance
truncation. Parameterized focused tests cover each rejection and the existing
clean quiescent IR-2 reconstruction remains covered.

**REVIEW DECISION:** Luna-0 accepted the overall handoff as partial, not as
full integration readiness. The reviewer classified the 27 full-suite
failures as downstream migration blockers, while identifying the IR-2 issue
as an in-scope Luna-22 defect. Downstream compatibility changes require a
separate narrow authorization naming affected files and whether each consumer
should select `TANH_LEGACY` or migrate to excursion semantics.

### Full-suite failure groups

The 27 failures occurred in these existing consumers, outside the Luna-22
owned files:

- `tests/test_cpu_visualization.py` (3): `NeuronRecord.from_neuron()` assumes
  an `activation` attribute that `MultiExcursionNeuron` does not expose.
- `tests/test_luna12b_integration.py` (4): structural-plasticity experiments
  construct the new default model and are rejected because plasticity is
  unavailable in the fixed-topology excursion integration.
- `tests/test_luna12e_integration.py` (2), `tests/test_luna12l_temporal_scale.py`
  (11), `tests/test_spiral_benchmark.py` (1), `tests/test_temporal_analysis.py`
  (3), and `tests/test_viewer_3d.py` (3): existing benchmark/analysis consumers
  assume legacy scalar activation, classifier provenance/configuration or
  structural behavior that is not part of the new default integrated path.

These failures are not described as passing regressions. Luna-22 does not
modify the closed neuron or downstream visualization/research consumers to
make them pass. Luna-0 must determine whether those consumers should explicitly
select the legacy control where they are legacy-only, or whether a separate
authorized downstream adapter/migration is required.

## Benchmark and resource results

**OBSERVED dataset:** UCI Character Trajectories, DOI `10.24432/C58G7V`,
2,858 examples, 20 classes, native three-feature trajectory arrays and source
metadata sampling interval 0.005 seconds (200 Hz). The UCI material was
identified as CC BY 4.0. Writer IDs/disjoint status were unavailable.

**OBSERVED split:** deterministic stratified 160-example subset, seed
`20261003`, with 80 train, 40 validation and 40 test examples (4/2/2 per
class). This is not a full-dataset or writer-disjoint result.

**OBSERVED preprocessing:** at each admitted point, the scalar input was
`x_velocity + y_velocity`; no whole-character normalization or future-point
preprocessing was used. Labels remained outside neural execution and the
held-out test labels were not used for training/reward.

**OBSERVED results:** validation accuracy 0.125; test accuracy 0.175. Exact
per-class scores were not retained, so no per-class performance claim is
reported. A previous settling-horizon trial at 2.0 logical seconds left work
pending in 33 of 40 test characters. At the selected 10.0 horizon, settling
completed for all test characters.

**OBSERVED test-subset activity:** prediction loss 0; matched/unmatched/expired
predictions `0 / 6,862 / 68`; matched/unmatched credit `0 / 2`; processed
events 12,756; emissions 68; silent events 12,688; peak queue occupancy 187;
pending/beyond-deadline/incomplete characters `0 / 0 / 0`.

**OBSERVED activity-cost-proxy:** event processing 12,756; emitted amplitude
46.6136; edge transfer 19.8008; prediction-error activity 0; total
12,822.4143 activity-cost-proxy units. These are software proxy units, not
joules. The benchmark indicates no matched prediction on this small test
subset and therefore does not establish predictive-learning efficacy.

**OBSERVED replay:** a fresh run over training, validation and test in the
same order reproduced traces/metrics exactly. The ad-hoc dataset loader/split
script and per-class table were not retained, so the dataset measurement is
not directly reproducible from the repository; this is a documentation and
evidence limitation, not a test-pass claim.

## Assumptions, limitations and unresolved issues

- **OBSERVED:** The default model change exposes consumers that assumed scalar
  `TPCNNeuron.activation`, implicit TANH behavior or plastic topology. These
  consumers are outside Luna-22's authorized file ownership.
- **OBSERVED:** The configured full suite is not green: 27 failures remain.
  The focused integration and prescribed component regressions pass.
- **OBSERVED:** The UCI subset completed with low classification accuracy and
  zero matched test predictions; ACP-0006 specified no accuracy threshold,
  but this result is not evidence of useful task efficacy.
- **UNRESOLVED:** The exact benchmark script and per-class metrics were not
  preserved; rerun with a retained, deterministic loader/split report before
  using the benchmark as a reusable baseline.
- **UNRESOLVED:** Luna-0 must review and authorize the downstream compatibility
  scope before any edits to visualization/benchmark consumers or closed
  components.

## Reproduction and rollback

Run the focused tests:

```powershell
C:/Users/zathp/AppData/Local/Programs/Python/Python311/python.exe -m pytest -q tests/test_experiments.py tests/test_excursion_integration.py
```

Run the prescribed component regression set or the full suite using the exact
commands in the validation table. Dataset reproduction requires downloading
the UCI Character Trajectories dataset (DOI `10.24432/C58G7V`) and reconstructing
the documented stratified subset with seed `20261003`; the original ad-hoc
loader was not retained. No raw dataset artifacts were added to the repository.

The implementation is based on `c13deb06427c64d00f603b1b1a1c75e442392fb8`
and is published in the Git commit containing this handoff. Preserve this
scope when reviewing or rolling back; do not reset unrelated work.

## Next assignment

Return this result to Luna-0 for independent review. Request a scope decision
on downstream consumers of the new EXCURSION_V1 default, especially CPU
visualization and legacy structural/research benchmark runners. Do not modify
those consumers or closed components until that decision authorizes the
specific files and expected compatibility semantics. Luna-22 implementation
is ready for architectural review, but full-repository integration is not
verified because the full CPU suite has 27 failures.
