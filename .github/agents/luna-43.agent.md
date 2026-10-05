---
name: Luna-43 ACP-0008 Test Comparison Policy Correction
description: Align Luna-41/Luna-42 auxiliary test assertions with the predeclared binary64 comparison rule; test files only.
---

# Luna-43 — ACP-0008 Test Comparison Policy Correction

## Authorization and baseline

Luna-43 is **AUTHORIZED / NOT EXECUTED** by
`workflow/handoffs/luna-0-authorization-luna43-test-comparison-policy-20261005.md`.
Start only from the published authorization revision, with a clean worktree,
and record the exact revision before editing. This is a test-only correction;
it is not permission to run or republish either calibration experiment.

Read `workflow/ARCHITECTURE_CONTRACT.md`,
`workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, the Luna-41 and Luna-42 agent
contracts and execution handoffs, the independent Luna-42 review, and both
focused tests and runner comparison rules. A01-A15 and ACP status are
unaffected; do not reinterpret the scientific outcomes.

## Objective

Correct auxiliary floating-point assertions in the two calibration test files
so nominal equation-derived values are checked using the already declared
binary64 rule:

`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`

The current Linux/Python 3.12 baseline has four failures, all caused by tests
requiring exact equality between a computed normalized value and decimal `0.4`.
The independent Luna-42 review also noted two test-only `abs_tol=1e-12`
assertions that are looser than the declared comparison policy. Correct only
these test-policy discrepancies.

## Owned files and interface

Own only:

- `tests/test_luna41_acp0008_temporal_calibration.py`
- `tests/test_luna42_acp0008_corrective_calibration.py`

Implement a small, test-local helper in each file (or an equally narrow
test-only approach) using the exact declared formula. Use it only where a test
compares a floating equation result to a nominal expected value or checks
floating symmetry. Preserve exact comparisons for event IDs, event ordering,
route/reception identity, and copied payload equality.

Do not edit runners, production code, ACP documents, architecture documents,
artifacts, prior handoffs, or test selection/configuration. Do not add
dependencies, change scientific tolerances, relax runner acceptance, regenerate
evidence, or modify the recorded Luna-41/Luna-42 verdicts. In particular,
Luna-41's near-pair failure at the runner's `ROUTE_PAYLOAD_TOLERANCE` remains
failed; correcting a test assertion must not convert it into a passing
calibration or change candidate selection.

## Acceptance checks

1. The only changed paths are the two owned test files.
2. Nominal `0.4` and floating-symmetry assertions use the declared binary64
   comparison formula; exact causal/event/provenance assertions remain exact.
3. Luna-41's tests still assert the near-pair payload mismatch and blocked
   result; Luna-42 scientific acceptance and artifacts are untouched.
4. Run the Luna-41 focused tests, Luna-42 focused tests, and full repository
   suite. Report exact pass/fail/skip counts and skip reasons. The governance
   baseline recorded four target failures and one CUDA-unavailable skip; no
   unrelated failure was observed.
5. Run `git diff --check` and verify no runner, production, ACP, architecture,
   artifact, or handoff file changed.

If any unrelated failure occurs, stop without altering its cause. Report
target-test failures separately from unrelated failures. Do not execute the
Luna-41 or Luna-42 experiment runners.

## Architectural and claim boundaries

No A01–A15 invariant or ACP is changed. ACP-0008 remains experimental,
opt-in, and unpromoted; ACP-0007 remains unchanged. This assignment makes no
claim about calibration validity, efficacy, structural growth, energy,
hardware, or architecture promotion. No new experiment or Luna successor is
authorized by completing this test-only correction.

## Handoff

Return the exact revision, owned-file diff, focused/full test results,
`git diff --check` result, and any limitations to Luna-0 in a completed
handoff under `workflow/handoffs/`.
