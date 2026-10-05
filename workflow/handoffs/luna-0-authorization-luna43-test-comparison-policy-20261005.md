---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-43 test comparison policy authorization"
  task_id: "luna-0-authorization-luna43-test-comparison-policy-20261005"
  component: "Auxiliary ACP-0008 calibration test assertions"
  status: "complete"
  contract_version: "1.2"
  branch: "copilot/execute-luna-43-cycle"
  base_revision: "b6ca4a67783bf37ded146944f8dc9afaf5277f11"
  result_revision: "the commit publishing this authorization"
  dependencies:
    - "Luna-41 execution and independent review"
    - "Luna-42 corrective execution and independent review"
    - "Current task instruction authorizing a bounded Luna-43 governance pass"
  owner: "Project owner"
  classification:
    - "governance-only authorization"
    - "test-only numerical assertion correction"
    - "Luna-43 AUTHORIZED / NOT EXECUTED"
  hypothesis: "Test-only comparisons using the declared binary64 rule correct nominal-value false failures without changing runner acceptance or recorded scientific outcomes."
  counter_hypothesis: "The focused suites retain a failure outside those assertions, or the helper changes exact causal/provenance checks."
  interfaces_relied_on:
    - "Luna-41 and Luna-42 test and runner comparisons"
    - "Declared rule: 64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))"
    - "Exact event/route/reception identity comparisons"
  label_information_boundary:
    - "No labels or task inputs are consumed; no experiment is authorized."
  timing_assumptions:
    - "Not applicable; do not execute calibration runners."
  reset_boundaries:
    - "Not applicable; test-only assertions."
  resource_bounds:
    - "No runtime, topology, or experiment bounds may change."
  authorized_scope:
    - "Edit only tests/test_luna41_acp0008_temporal_calibration.py and tests/test_luna42_acp0008_corrective_calibration.py."
    - "Replace exact decimal equality or abs_tol=1e-12 only for floating equation-derived nominal values/symmetry with the declared binary64 comparison rule."
    - "Run both focused test files, the full suite, and git diff --check."
  unauthorized_scope:
    - "Do not execute or republish Luna-41/Luna-42 experiments."
    - "Do not change runner acceptance, production code, ACPs, architecture, evidence artifacts, historical verdicts, or unrelated tests."
    - "Do not add dependencies, tune scientific tolerances, or authorize another Luna."
  controls:
    - "Preserve exact source-emission/route/reception identity and payload-copy assertions."
    - "Preserve Luna-41 near-pair blocked expectation and route mismatch."
    - "Keep Luna-42 runner selection and all published artifacts unchanged."
  measurements:
    - "Baseline and post-change focused/full test counts, failures, and skips."
    - "Changed paths and git diff --check."
  information_boundary_check:
    - "No labels, predictions, rewards, or task outcomes enter comparisons."
  hardware_mapping:
    - "Not applicable; no hardware or neural runtime change."
  architecture_invariants_touched: []
  preserves:
    - "A01-A15 and all ACPs unchanged."
    - "Luna-41 remains historically BLOCKED."
    - "Luna-42 remains independently reviewed; its artifacts and verdict are unchanged."
    - "ACP-0008 remains experimental, opt-in, and unpromoted."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-43.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna43-test-comparison-policy-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Baseline full suite: 1019 passed before four targeted comparison failures."
    - "Focused Luna-41 baseline: 4 passed before two targeted comparison failures."
    - "Focused Luna-42 baseline: 6 passed before two targeted comparison failures."
    - "git diff --check on the clean baseline passed."
  tests_failed:
    - "Baseline full suite: 4 failures, all exact computed-float versus decimal-0.4 assertions in the two assigned test files."
  tests_not_run:
    - "Luna-43 has not run; this handoff only authorizes its bounded test-only work."
    - "Calibration runners and hardware checks are not authorized."
  assumptions:
    - "The four baseline failures are within the explicitly scoped test-comparison issue; no unrelated failure was observed."
    - "The two test-only abs_tol=1e-12 assertions noted by Luna-0 are part of the same comparison-policy correction."
  unresolved:
    - "Luna-43 execution and its post-change focused/full validation remain outstanding."
  recommended_next_agent:
    - "Luna-43 to perform only the owned test assertion correction and validation."
---

# Luna-0 authorization — Luna-43 test comparison policy correction

## Decision

**Luna-43 is AUTHORIZED / NOT EXECUTED** for a narrowly scoped, test-only
correction of floating-point comparison assertions in the Luna-41 and Luna-42
focused test files. This does not supersede or revise the historical scientific
reviews. The prior Luna-0 review accurately recorded that no successor was
authorized at that review's publication; this is a new, later authorization
based only on the non-blocking test-policy follow-up and the bounded baseline
failures below.

The task instruction explicitly requests a Luna-43 contract and authorization
if safe. The follow-up is safe because every failure in the current full-suite
baseline is a strict comparison of an equation-derived floating value to
literal decimal `0.4` in the two owned test files. No unrelated failure was
observed. Do not broaden the assignment to address any future unrelated test
failure.

## Evidence reviewed

The reviewed source is the exact current revision
`b6ca4a67783bf37ded146944f8dc9afaf5277f11`, branch
`copilot/execute-luna-43-cycle`, with a clean worktree and `HEAD == origin/main`.
The architecture sources were read from their repository locations under
`workflow/` (the checkout does not contain a `tpcn-luna-workflow/` directory).
No Architecture Contract clause or ACP needs amendment.

Luna-42's independent review identified two test-only `abs_tol=1e-12`
assertions as a non-blocking discrepancy from its predeclared binary64 formula.
Raw tests additionally show strict computed-value comparisons at:

- Luna-41: `z_after_input == 0.4` and first routed payload `== 0.4`.
- Luna-42: `z_after_input == 0.4` and first routed payload `== 0.4`.

On this Linux/Python 3.12 environment the observed first routed value and
integrated state are `0.39999999999999997`. The Luna-41 runner independently
continues to record its predeclared near-pair route mismatch and blocked result;
the test-only fix must not relax or rewrite that outcome. Luna-42 already
checks its actual route/reception payload copy exactly and computes its
scientific equation checks with the declared formula.

Raw evidence reviewed:

- `workflow/handoffs/luna-40-effective-routed-drive-20261005.md` and its
  `artifacts/luna40-effective-routed-drive/` JSON.
- `workflow/handoffs/luna-41-acp0008-temporal-calibration-20261005.md`, the
  Luna-41 independent review, `.github/agents/luna-41.agent.md`, runner,
  focused tests, and all four Luna-41 artifacts.
- `workflow/handoffs/luna-42-acp0008-corrective-calibration-20261005.md`, the
  Luna-42 independent review, `.github/agents/luna-42.agent.md`, runner,
  focused tests, and all four Luna-42 artifacts.

Luna-42's independent results remain: selected `decay_rate_z=0.0125`,
production-derived payloads, reproducible fixed-topology relay emissions and
onward transfers, no destination emission, and no supported structural-growth
opportunity. Luna-41 remains historically BLOCKED; neither conclusion is
altered.

## Baseline validation

The initial test attempt reported that pytest was unavailable. For validation
only, pytest, NumPy, SciPy, and PyTorch were installed into the runner's user
environment; no repository dependency files were added or changed. The full
baseline command was `python -m pytest -q -rs`. The environment was Python
3.12.3, pytest 9.1.1, NumPy 2.5.3, SciPy 1.18.1, and PyTorch 2.14.1; CUDA
was unavailable:

| Check | Result |
|---|---|
| Full repository suite | 1019 passed, 4 failed, 1 skipped; 1024 collected |
| Skip | `tests/test_gpu_visualization.py:61`, CUDA unavailable |
| Luna-41 focused suite | 4 passed, 2 failed; both strict nominal-0.4 assertions |
| Luna-42 focused suite | 6 passed, 2 failed; both strict nominal-0.4 assertions |
| `git diff --check` | Passed; baseline worktree clean |

All four full-suite failures are the same in-scope computed-float equality
issue. No unrelated failure was observed. The full suite did not pass at
baseline; this handoff records that accurately and does not claim otherwise.

## Luna-43 authorized work

Luna-43 may change only:

- `tests/test_luna41_acp0008_temporal_calibration.py`
- `tests/test_luna42_acp0008_corrective_calibration.py`

For expected floating equation results and floating symmetry, use the exact
already-declared formula:

`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`

Retain exact checks for event identity, ordering, route/reception identity and
copied payload equality. Keep the Luna-41 near-pair expected failure and
blocked verdict. The work must not change runner acceptance, experiment
criteria, scientific tolerance, artifact contents, or any historical record.
No Luna-41/Luna-42 runner execution is authorized.

After the edits, run both focused test files, the full suite and
`git diff --check`. Report actual outcomes, all skips, and the exact modified
paths. If an unrelated failure appears, stop and return it to Luna-0 without
expanding scope.

## Architecture and integration readiness

No A01-A15 clause is changed; no ACP is created or amended. ACP-0008 remains
experimental, opt-in and unpromoted; ACP-0007 is unchanged. This is not
integration approval, calibration revalidation, efficacy evidence, or
hardware validation. Integration readiness is **not applicable** to this
test-only governance assignment.

## Next assignment

Luna-43 owns only the two test files above and the post-change validation.
Return the completed handoff to Luna-0. No successor is authorized by this
decision.
