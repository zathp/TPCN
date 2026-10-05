# Luna-0 independent post-Luna-36 review — eligibility capacity API

```yaml
tpcn_handoff:
  agent: Luna-0
  task_id: "luna-0-independent-review-luna36-eligibility-capacity-api-20261004"
  status: "complete"
  reviewed_revision: "8f8824a185a2b1ebc3fd74cbd29eef8d75cbd818"
  base_revision: "8f8824a185a2b1ebc3fd74cbd29eef8d75cbd818"
  verdict: "PASS"
  architecture_change: false
  production_defect: false
  next_authorized: "Luna-37 AUTHORIZED / NOT EXECUTED"
```

## Verification of state

`origin/main == HEAD == 8f8824a...`, clean worktree. Luna-36 changed exactly
its three owned files (193 insertions, 1 deletion): runtime, new test file,
handoff. No governance, Luna-34/35, ACP, eligibility, predictor or
`ExperimentRunner` files changed.

## Contract compliance

OBSERVED from the diff: keyword-only `eligibility_capacity: int | None = None`
added to `ExcursionCharacterRuntime.__init__` and `from_quiescent_ir2()`
(forwarded); validation (`bool`/non-int/<=0 -> `ValueError`); read-only
`eligibility_capacity` property; one changed line in `start_character`
(`max_traces=self._eligibility_capacity`). Predictor construction, expiry,
eligibility creation/retirement, reward, prediction-error, neuron emission,
routing and event ordering are untouched. No resizing after startup; IR-2
records not modified. No Luna-34 experiment was run; no Luna-37 was authorized
by Luna-36.

## Independent capacity reconstruction

Traced from public input to ledger and confirmed by an independent snippet
(two nodes, `prediction_capacity=8`):

| Construction | property | per-ledger `max_traces` | predictor `max_outstanding` |
|---|---|---|---|
| omitted (legacy) | 16 | n0=16, n1=16 | 8 |
| `eligibility_capacity=1024` | 1024 | n0=1024, n1=1024 | 8 |

Capacity is per ledger (one ledger per node), the default scaling by neuron
count occurs exactly once at construction, and an explicit value is used
unchanged with no scaling. A caller can predict it from the property.

## Backward compatibility

All pre-existing callers use keywords and omit the option; no positional
breakage; no new required fields; no serialization change; no duplicate
derivation elsewhere. Default 16 for the two-node `prediction_capacity=8`
fixture is unchanged.

## Boundedness

Independent snippet with `eligibility_capacity=2`: the third eligibility
creation raised `EligibilityCapacityError("eligibility trace capacity
reached")` with n0 occupancy 2. Capacity stays finite; no eviction, retry or
growth was introduced.

## Delayed-credit regression

Full suite includes the historical eligibility, predictive-coding, reward,
excursion-integration and Luna-35 lifecycle tests, all passing unchanged;
eligibility surviving predictor expiry and delayed reward are intact.

## Validation

| Check | Result |
|---|---|
| Focused (Luna-36 + excursion integration + eligibility + predictive coding + Luna-35 lifecycle) | 90 passed |
| Full suite | 945 passed, 1 skipped (CUDA unavailable, `tests/test_gpu_visualization.py:61`) |
| Collected | 946 |
| `git diff --check` | clean |

Increase from 932/933 is exactly the 13 new Luna-36 test cases.

## Findings

Verdict **PASS**. The public-API blocker is **resolved**: a future bounded
diagnostic can instantiate the production runtime with an explicit finite
per-ledger eligibility capacity without changing lifecycle semantics. No
production defect exists. Not established: any propagation-to-emission result,
`w=1` vs `w=2`, candidate formation, efficacy. Luna-34 remains historically
**BLOCKED / UNDETERMINED**; Luna-33 and ACP-0007 unchanged.

## Next governance state

Luna-37 created: `.github/agents/luna-37.agent.md`, **AUTHORIZED / NOT
EXECUTED**. It is a clean successor to Luna-34's mechanism diagnostic (same
three conditions, same streams/bounds) with predeclared
`eligibility_capacity=1024`, derived from the declared per-character event
budget (one trace per canonical emission, each emission consumes at least one
event), retained occupancy evidence, and stop on overflow. No efficacy,
growth, pruning or ACP change. No Luna-38 authorized.
