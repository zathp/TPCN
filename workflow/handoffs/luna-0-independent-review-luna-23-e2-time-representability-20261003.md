# Luna-0 Independent Review - Luna-23 E2 Logical-Time Representability

```yaml
tpcn_handoff:
  agent: "Luna-0"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent verification of Luna-23 E2 timestamp correction"
  task_id: "luna-0-independent-review-luna-23-e2-time-representability-20261003"
  component: "ACP-0004 E2 analytic S_REARM scheduling"
  status: "PASS; Luna-23 closed; Luna-22 remains blocked"
  contract_version: "1.1"
  branch: "main"
  base_revision: "10687cf4a21d75eb5a0552635282f889df1e4005"
  result_revision: "c0e3e6905e329e5c268d6c63cbb3bd8d89345136"
  dependencies:
    - "Luna-23 implementation and completion handoff"
    - "Accepted ACP-0004 E2 semantics and unchanged A01-A15"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["INDEPENDENT CORRECTIVE REVIEW", "ADVERSARIAL NUMERICAL VERIFICATION", "REGRESSION VERIFICATION"]
  hypothesis: "The E2 software reference can preserve positive analytic return and strict-future ordering at a float representability boundary without changing the canonical delay rule."
  counter_hypothesis: "The fallback broadens valid scheduling, breaks bounded return, or alters E1, IR-2, or accepted timing semantics."
  interfaces_relied_on:
    - "MultiExcursionNeuron local time, pending S_REARM validation and event budget"
    - "Closed SingleExcursionNeuron E1 scheduler"
    - "TPCN-IR-2 revision-1 E2 standalone adapters"
  label_information_boundary:
    - "No labels, future inputs, global clock or task metric enters the E2 scheduler."
  timing_assumptions:
    - "Analytic S_REARM delay is positive and finite."
    - "Software-reference event timestamps must be finite and strictly future."
  reset_boundaries:
    - "No reset semantics changed."
  resource_bounds:
    - "One valid pending event and existing finite event/generation budgets."
  authorized_scope:
    - "Read-only independent review, bounded probes, focused regression execution, review handoff and governance status update."
  unauthorized_scope:
    - "Luna-24, downstream consumer migration, dataset repair, ACP text changes and Luna-22 closure."
  controls:
    - "Configured non-advancing-delay rejection"
    - "E1 regression suite"
    - "E2/IR-2 continuation and identity checks"
    - "Full CPU suite and seven original representability failure paths"
  measurements:
    - "Analytic delay, rounded timestamp, next representable due time, processed event timestamps, event count and test outcomes."
  information_boundary_check:
    - "Correction and probes use only local neuron state, local time and configuration."
  hardware_mapping:
    - "IEEE-754 nextafter is treated only as a software-reference representation operation; no hardware equivalence is claimed."
  architecture_invariants_touched: ["A01", "A02", "A03", "A08", "A15"]
  preserves:
    - "A01-A15, ACP-0004 state transitions, E1 semantics, E2 identity/generation validation, and IR-2 schema revision 1."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna-23-e2-time-representability-20261003.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Focused E2 suite: 42 passed."
    - "E1/E2/IR-2 reference suites: 203 passed."
    - "Luna-22 prescribed integration regression set: 320 passed."
    - "Full CPU suite: 775 passed; 24 remaining failures; 1 CUDA-unavailable skip."
  tests_failed:
    - "The full CPU suite retains 24 pre-existing downstream failures, detailed below; none fails from the original E2 representability exception."
  tests_not_run:
    - "Hardware/backend equivalence."
    - "A retained, reproducible sequential dataset/split/per-class evaluation."
  assumptions:
    - "The erroneous non-Git revision token included in the task snapshot is not a repository object; real ancestry is taken from valid Git commits."
    - "Direct calls to private _schedule with malformed same-time S_REARM values are not public runtime behavior; actual E2 call sites were inspected."
  unresolved:
    - "Luna-22 remains blocked by integrated IR-2 residual provenance, dataset reproducibility/per-class evidence, and downstream compatibility decisions."
    - "Luna-24 remains authorized but not executed."
  recommended_next_agent:
    - "Luna-24 under its already published authorization."
```

## Review baseline and valid commit lineage

**OBSERVED:** Review began from `10687cf4a21d75eb5a0552635282f889df1e4005`
(`docs: finalize Luna-23 handoff revision`) with `main == origin/main` and a
clean worktree. Luna-23's implementation commit is
`4c1efd6c31aed86748dcacf596401579c2b94bc8`, its actual parent is
`3ec3c4a7991c28f59e1419c9f3656267efed2875`, the first completion-handoff
publication is `7ce73cb194128f6ecd4a5068f4bbdd72d42b5eea`, and the finalized
handoff revision is `10687cf4a21d75eb5a0552635282f889df1e4005`.
Git ancestry checks confirm the implementation-to-publication and
publication-to-final links.

The source snapshot also contains a string formatted like a shortened
revision, but Git cannot resolve it to an object. It was not used as a commit
identifier. The valid pre-implementation revision recorded in Luna-23's
handoff and confirmed as the implementation parent is
`3ec3c4a7991c28f59e1419c9f3656267efed2875`; the corrected Luna-0 review
publication is present in its ancestry.

This independent review and governance outcome were first published in
`c0e3e6905e329e5c268d6c63cbb3bd8d89345136`.

The complete implementation delta from `3ec3c4a` to `4c1efd6` contains only:

- `tpcn/excursion_neuron.py`: E2 `_schedule()` conditionally represents an
  analytically valid `S_REARM` with `nextafter(current, +inf)` when its
  positive finite analytic addition rounds exactly to the current timestamp.
- `tests/test_e2_multi_excursion.py`: configurable test decay rate and initial
  timestamp plus a two-polarity pending-event continuation regression.

No IR-2, integration, dataset, visualization, topology, or other production
file changed.

## E2 call-site audit and private-call boundary

**OBSERVED:** Source inspection found these `S_REARM` occurrences:

| Call site | Runtime reachability | Scheduled time |
|---|---|---|
| `SingleExcursionNeuron._update_after_external` | E1 only; overridden by E2 | `clock + _rearm_delay(magnitude)` |
| Inherited `_emit_ordinary` | E2 ordinary `S_PENDING` may use it | `clock + _rearm_delay(abs(x))` |
| Inherited `_finish_rearm` | E2 `S_RETURN` continuation | `clock + _rearm_delay(magnitude)` |
| `MultiExcursionNeuron._update_after_external` | E2 `S_RETURN` after external input | `clock + _rearm_delay(magnitude)` |

All production-reachable E2 calls that can invoke the new fallback originate
from the local analytic return calculation. E2 `M_EMIT` and `M_REARM` call
sites use configured delays and do not receive the fallback. No call site
passes an arbitrary same-time timestamp.

**OBSERVED adversarial private probe:** Directly calling the private
`MultiExcursionNeuron._schedule(S_REARM, current_time, ...)` with a state
whose analytic delay is below the timestamp resolution does map to
`nextafter(current_time, +inf)`, even though that direct request did not
originate at an analytic call site. The fallback cannot establish caller
provenance; it rechecks the local state's analytic delay, finiteness,
positivity and rounded sum. The private API can therefore legalize this
malformed direct request.

**INFERRED classification:** This is a bounded private-call widening, not an
exploitable public-path defect in the current code: normal production call
sites were enumerated and all pass the analytic sum. A future internal caller
must preserve this precondition. Public E2 IR-2 reconstruction separately
rejects pending timestamps `<= local_last_update_time`, so it does not offer
an alternate malformed same-time entry path.

## Independent numerical and state-machine probes

Both polarities were independently processed through a valid pending
`S_REARM` and the real `process_pending()` / `receive_event()` transitions.
The pre-event state was initialized at the immediately previous representable
timestamp so local exponential decay reaches the required exact state at the
observed clock.

| Polarity | Local time | State at return | Analytic delay | Raw sum | Stored due time |
|---|---:|---:|---:|---:|---:|
| Negative | `45.27906122689938` | `-0.2500000000000003` | `1.110223024625156e-15` | `45.27906122689938` | `45.27906122689939` |
| Positive | `45.27906122689938` | `+0.2500000000000003` | `1.110223024625156e-15` | `45.27906122689938` | `45.27906122689939` |

For each polarity, the analytic delay is finite and positive, its sum equals
the current timestamp, and the stored due time equals
`math.nextafter(clock, math.inf)`. The queued event timestamp, pending-slot
timestamp and embedded payload timestamp agree.

**OBSERVED continuation:** Both runs process exactly:

```text
[45.27906122689938, 45.27906122689939]
```

Every consecutive timestamp is strictly greater. The second event closes
`S_RETURN` to `N`; the queue empties; the pending slot is cleared; processed
event count is 2; and no duplicate emission is created. The transition is
deterministic across repeated runs and does not walk timestamps by repeated
ULPs.

### Adversarial scheduling boundaries

- At the largest finite IEEE-754 timestamp, a positive analytic delay rounds
  to the same current time and `nextafter(max_float, +inf)` becomes infinity.
  The final finite/strict-future guard raises `ValueError`; no queue event is
  inserted.
- Same-time requests for `M_EMIT` and `M_REARM` are rejected.
- A `S_REARM` timestamp in the past, NaN, or same-time with a state whose
  analytic delay is representable is rejected.
- A direct same-time private `S_REARM` with the reproduced unrepresentable
  state is accepted at the next representable timestamp; see private-call
  classification above.
- `test_positive_configured_delay_that_cannot_advance_float_time_is_rejected`
  passes. Its `1e308` current timestamp and smallest positive configured
  `m_emit_delay` remain rejected; no blanket `due_time <= current_time`
  normalization was introduced.

## E1, identity, state machine and IR-2 preservation

The source delta changes only `MultiExcursionNeuron._schedule()`. The
`SingleExcursionNeuron` base scheduler, reset, event ordering and state
machine are unchanged; E1 tests pass. The E2 code does not change mode
transitions, episode/lineage/event identities, generation allocation, queue
sequence validation or stale-event checks. The new due time flows through the
existing scheduling path.

The standalone E2 IR-2 tests pass, including pending-event continuation,
stale-generation validation and counter continuity. `IR2_SCHEMA_REVISION`
remains `1`; `test_e2_ir2.py` asserts the round-trip document revision is 1.
No serialized schema, reconstruction path or integrated startup code changed.

## Validation record

Environment: Windows, workspace Python 3.11. Relevant pytest commands were
run from the repository root.

| Command / procedure | Observed result |
|---|---|
| `pytest -q tests/test_e2_multi_excursion.py` | **42 passed** |
| `pytest -q tests/test_excursion_neuron.py tests/test_e2_multi_excursion.py tests/test_e2_ir2.py tests/test_ir2.py` | **203 passed** |
| Luna-22 prescribed 13-file regression command | **320 passed** |
| Four explicit tests: four-class label invariance, fixed policy, requested scale, spiral label invariance | **4 passed** |
| `pytest -q tests/test_luna12l_temporal_scale.py tests/test_spiral_benchmark.py` | **9 failed, 9 passed**; the failures are structural/default-model boundaries, not E2 representability errors |
| `pytest -q -rs` | **24 failed, 775 passed, 1 skipped** |
| `pytest --collect-only -q` | **800 tests collected** |
| `python -m compileall -q tpcn tests` | **Passed** |
| Pylance diagnostics: `tpcn/excursion_neuron.py`, `tests/test_e2_multi_excursion.py` | **No diagnostics** |
| `git diff --check` | **Passed** |

The only full-suite skip is
`tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`,
skipped because CUDA is unavailable.

## Seven original representability exceptions

**OBSERVED:** The Luna-0 second review had seven failing cases whose initial
failure cause was the E2 positive-delay representability exception:

| Original case | Current disposition |
|---|---|
| `test_labels_do_not_change_canonical_four_class_trace` | **Pass**; exception removed and test passes. |
| `test_requested_policy_is_executed_by_classifier[fixed]` | **Pass**; exception removed and test passes. |
| `test_requested_scale_reaches_classifier_configuration` | **Pass**; exception removed and test passes. |
| `test_scale_runner_retains_all_policies_and_causal_evidence` | Representability blocker removed; test still fails later on unavailable structural/default-model behavior. |
| `test_policy_changes_classifier_execution_state` | Representability blocker removed; test still fails later on unavailable structural/default-model behavior. |
| `test_policy_scale_cross_product_preserves_provenance_and_serialization` | Representability blocker removed; test still fails later on unavailable structural/default-model behavior. |
| `test_control_results_are_deterministic_and_include_required_order_controls` | Representability blocker removed; test still fails later when its structural control requests unavailable plasticity. |

Thus all seven representability exceptions are removed as the failure cause.
Only three tests pass outright; the other four are not claimed as fixed.

The pre-Luna-23 full-suite baseline was 27 failed, 770 passed, 1 skipped
(798 observed outcomes). Current collection is 800. The exact test delta adds
two parametrized polarity cases and removes no tests, skips or xfails.
Arithmetic agrees: three former failures turn into passes, four former
representability failures continue to fail later, and the two new test cases
pass, yielding 24 failed, 775 passed, 1 skipped.

## Remaining 24 full-suite failures

**OBSERVED:** Every remaining failure is outside Luna-23's source delta and
matches the previously identified consumer/default-model groups:

| File | Count | Remaining cause |
|---|---:|---|
| `tests/test_cpu_visualization.py` | 3 | TPCV-1 `NeuronRecord` assumes scalar `.activation` on E2. |
| `tests/test_luna12b_integration.py` | 4 | Structural consumers request plasticity with fixed `EXCURSION_V1`. |
| `tests/test_luna12e_integration.py` | 2 | Legacy prediction-loss and reset-time observable assumptions. |
| `tests/test_luna12l_temporal_scale.py` | 8 | Structural/default-model configuration failures, including four earlier representability paths now proceeding farther. |
| `tests/test_spiral_benchmark.py` | 1 | Later structural control requests unavailable plasticity after E2 no-learning work. |
| `tests/test_temporal_analysis.py` | 3 | Fixtures request the rejected structural CPU experiment path. |
| `tests/test_viewer_3d.py` | 3 | Fixtures request structural CPU training rejected by `EXCURSION_V1`. |
| **Total** | **24** | No downstream failure was repaired or suppressed. |

## Architecture and governance disposition

| Clause | Independent disposition |
|---|---|
| A01 | Event-triggered scheduling remains; there is no global neural timestep. |
| A02 | Local analytic decay/rearm remains unchanged; a finite positive return is now represented by a strictly later software timestamp. |
| A03 | The accepted internal return transition is strictly future and finite; unrepresentable overflow is rejected rather than enqueued. |
| A08 | One pending event and the existing finite event budget remain authoritative; observed return terminates in two events. |
| A15 | `nextafter` is a float-reference representability operation only, not canonical FPGA/FPAA timing or hardware-equivalence evidence. |

**INFERRED:** This is an implementation correction within ACP-0004's
analytic return and strict-future ordering requirements. It does not
introduce a canonical epsilon, timestep, alternate decay equation or
hardware-specific timing rule. ACP text and A01-A15 are unchanged.

**Luna-23 terminal verdict: PASS — LUNA-23 E2 LOGICAL-TIME REPRESENTABILITY
CORRECTION INDEPENDENTLY VERIFIED / CLOSED.**

**Luna-22:** remains **BLOCKED / NOT CLOSED**. Outstanding blockers include
the Luna-24 integrated IR-2 provenance/truncation startup boundary, retained
reproducible sequential dataset/split/per-class evidence, and separately
authorized downstream compatibility decisions.

**Luna-24:** **AUTHORIZED / NOT EXECUTED**. It is the next bounded execution
assignment under its existing authorization. This review did not implement
Luna-24, edit its owned files, migrate consumers, or change dataset artifacts.

**NOT TESTED:** hardware/backend equivalence, calibration, and reproducible
real-dataset efficacy.
