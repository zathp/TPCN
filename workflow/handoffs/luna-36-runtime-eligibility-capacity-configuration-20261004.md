# Luna-36 handoff: runtime eligibility-capacity configuration

```yaml
tpcn_handoff:
  agent: Luna-36
  luna_identifier: "Luna-36"
  descriptive_name: "EXCURSION Runtime Eligibility Capacity Configuration"
  task_id: "luna-36-runtime-eligibility-capacity-configuration-20261004"
  component: "tpcn.experiment_excursion_runtime.ExcursionCharacterRuntime"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "5f2e41a845526f2d74b14b6217143fd959b0c9e9"
  result_revision: "see git log (commit containing this file)"
  classification: ["PUBLIC RUNTIME CONFIGURATION", "backward-compatible"]
  hypothesis: "An optional per-ledger eligibility_capacity can be added with the omitted default preserving the legacy derived capacity and all lifecycle behavior."
  counter_hypothesis: "Threading the option changes defaults, admits invalid/unbounded state, or breaks callers. Not observed."
  architecture_change: false
  files_changed:
    - tpcn/experiment_excursion_runtime.py
    - tests/test_luna36_eligibility_capacity_api.py
    - workflow/handoffs/luna-36-runtime-eligibility-capacity-configuration-20261004.md
  tests_added: ["tests/test_luna36_eligibility_capacity_api.py (13 collected cases)"]
  tests_passing: ["focused 87 passed", "full 945 passed, 1 skipped"]
  tests_failed: []
  tests_not_run: []
  unresolved: ["Luna-34 remains BLOCKED / UNDETERMINED; no propagation-to-emission result exists."]
  recommended_next_agent: ["Luna-0 independent post-Luna-36 review"]
```

## Outcome

- OLD (OBSERVED): `start_character` built every ledger with `max_traces = prediction_capacity * max(1, len(neurons))`; no caller control.
- NEW: keyword-only `eligibility_capacity: int | None = None` on `ExcursionCharacterRuntime.__init__` and `from_quiescent_ir2()`; read-only property `eligibility_capacity`.
- Default `None` resolves at construction to the legacy formula (neuron count influences only the default). An explicit value is used unchanged, per ledger, for every node. No scaling by neuron count or prediction capacity.
- Validation: `bool`, non-int, zero, negative raise `ValueError("eligibility_capacity must be a positive integer")`, matching the existing style. Always finite.
- Conversion to ledger capacity: only `start_character` (`max_traces=self._eligibility_capacity`). No other duplicate derivation exists. No resizing after startup.
- Unchanged: predictor `max_outstanding`/expiry, eligibility creation/decay/credit/removal/expiry, rewards, prediction errors, neurons, routing, reset, event order. A too-small capacity still raises the existing `EligibilityCapacityError`.

## Compatibility audit

All existing callers (tests/test_excursion_integration.py, Luna-28, Luna-34, Luna-35 code) use keyword arguments and omit the option; no positional breakage. IR-2 records and serialized formats are untouched (test asserts `eligibility_capacity` is absent from IR-2 JSON).

## Validation record

| Command | Result |
|---|---|
| pytest Luna-36 tests + test_excursion_integration + test_eligibility + test_predictive_coding | 87 passed |
| pytest full suite | 945 passed, 1 skipped (CUDA unavailable, tests/test_gpu_visualization.py:61); 946 collected |
| python -m compileall -q tpcn tests | exit 0 |
| git diff --check | clean (LF/CRLF warning only) |

Count increase 932 -> 945 passed = 13 new parametrized cases from the Luna-36 test file. Baseline was 932 passed, 1 skipped, 933 collected.

## Limits

The Luna-34 sequence and its three edge conditions were NOT run; no explicit non-default capacity was chosen to fit an experiment (tests use arbitrary tiny API values 1, 3, 5). Not established: sufficiency of any capacity, w=1 vs w=2, downstream emission, ACP-0007 candidate formation, efficacy, or hardware equivalence.

## Reproduction and rollback

`python -m pytest tests/test_luna36_eligibility_capacity_api.py`. Rollback: revert the Luna-36 commit.

## Next assignment

Luna-0 independent post-Luna-36 review. No Luna-37 authorized.
