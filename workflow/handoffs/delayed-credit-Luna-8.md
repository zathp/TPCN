# Luna agent handoff

```yaml
tpcn_handoff:
  agent: Luna-8 Delayed Credit and Reward
  task_id: "delayed-credit"
  component: "bounded local eligibility traces and causal delayed credit"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "e2b8276"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A07", "A08", "A11", "A15"]
  preserves:
    - "Luna-1 event timestamps and causal delivery; no global neural clock."
    - "Luna-3 local prediction IDs, timestamps, signed PredictionError records, and bounded outstanding state."
    - "Luna-5 ownership of resource accounting and final reward-versus-energy utility policy."
    - "Finite trace, expiry, credit, and deterministic overflow behavior."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/eligibility.py"
    - "tpcn/__init__.py"
    - "tests/test_eligibility.py"
    - "workflow/handoffs/delayed-credit-Luna-8.md"
  tests_added:
    - "tests/test_eligibility.py"
  tests_passing:
    - "python -m pytest -q tests/test_eligibility.py: 6 passed"
    - "python -m pytest -q: 50 passed"
    - "python -m compileall -q tpcn tests: passed"
    - "git diff --check: passed"
  tests_failed: []
  tests_not_run:
    - "Luna-5 energy/resource accounting and reward-adjusted utility validation."
    - "Luna-6 stream integration, Luna-7 classifier, and Luna-11 acceptance matrix."
    - "FPGA, FPAA, hybrid, hardware-equivalence, and calibrated energy validation."
  assumptions:
    - "Time units are the abstract nonnegative floating-point units of Luna-1."
    - "A signed PredictionError is a local causal learning signal; this does not define a global loss or utility objective."
    - "Trace identity is local and may be associated with one Luna-3 prediction_id."
  unresolved:
    - "Luna-0 and Luna-5 must agree on reward units, producer/interface, and how reward availability crosses the local resource boundary before integration."
    - "Luna-0 must retain ownership of the final reward-versus-energy utility formula, coefficients, and retention/suppression policy; Luna-8 does not choose them."
  recommended_next_agent:
    - "Luna-5: define the compatible local resource/usefulness adapter and reward signal contract."
    - "Luna-11: independently verify delayed-credit behavior after Luna-5 and integration interfaces exist."
```

## Outcome and owned scope

Implemented `EligibilityLedger` in `tpcn/eligibility.py`. Local activity is
submitted as an addressed `EligibilityActivity` event and creates or updates
a trace keyed by a local `trace_id`, optionally linked to a Luna-3
`prediction_id`. A later addressed `RewardSignal` or `PredictionError` event
identifies the trace locally and returns a `CreditAttribution` result.

Trace values and accumulated credit use deterministic exponential decay from
the elapsed time between local event timestamps. Trace count, trace magnitude,
credit magnitude, and optional age are finite. New traces at capacity raise
`EligibilityCapacityError`; no state is silently evicted. Expired matched
traces are removed and reported as `expired`. Unmatched signals do not advance
the local clock or mutate any trace.

The implementation deliberately does not calculate energy, usefulness,
utility, reward normalization, classifier output, structural plasticity, or
global reward broadcast. It does not mutate a remote component inline; callers
deliver the typed payload through the existing event runtime.

## Architecture evidence

- **A01-A02:** decay is evaluated only when this local ledger receives an
  addressed event with a later timestamp; no network-wide tick is used.
- **A07:** attribution searches only the ledger's finite local trace table and
  the causal event payload. Prediction IDs are consumed as local metadata;
  there is no global prediction registry or backpropagation.
- **A08:** `max_traces`, `trace_limit`, `credit_limit`, and optional `expiry`
  bound stored state and updates. Overflow and expiry are deterministic.
- **A11:** activity remains eligible after further events and can receive a
  later reward or prediction error with elapsed-time decay.
- **A15:** the reference uses fixed-schema records, scalar bounded state, and
  abstract timestamps suitable for software and later hardware mapping.
- **A09-A10:** intentionally left at the Luna-5 boundary. Credit is a raw
  local attribution signal, not a final energy or utility decision. No ACP is
  required; no contract clause was changed.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_eligibility.py` | `main`, uncommitted, Python 3.10.8; no random state | Pass, 6 tests | Delayed reward, irregular decay, bounds, unmatched reward, prediction error, overflow, expiry |
| `python -m pytest -q` | `main`, uncommitted, Python 3.10.8 | Pass, 50 tests | Full available repository regression |
| `python -m compileall -q tpcn tests` | `main`, uncommitted, Python 3.10.8 | Pass | Package and all tests compile |
| `git diff --check` | `main`, uncommitted | Pass | No whitespace errors |

The focused tests verify that reward changes eligible local activity only at
causal arrival, irregular timestamps decay deterministically, trace and credit
values remain bounded, unrelated rewards do not mutate local traces, local
prediction IDs identify error attribution without global state, and expired
work cannot receive late credit.

## Benchmark and resource results

No dataset, classification metric, connectivity utilization, calibrated energy
unit, hardware timing, or final utility formula applies to this local
component. The configured reference values in tests are abstract units:
decay time constants 1.0 or 2.0, finite trace capacities 1 or 2, and explicit
trace/credit bounds. A signed prediction error is propagated as a local
signal; its interpretation as reward, loss, or utility remains outside this
assignment.

## Assumptions, limitations and unresolved issues

The ledger currently supports one local trace per `trace_id`; repeated local
activity accumulates into that trace and clamps at `trace_limit`. A signal
matches by explicit `trace_id` or `prediction_id`, with deterministic
lexicographic tie selection if a signal identifies multiple local traces.
This is a compatible reference choice, not a permanent architecture mandate.

The Luna-5 agent definition is present, but no accepted Luna-5 implementation
handoff or resource interface exists in the current worktree. Cross-component
integration is therefore intentionally unresolved and should return to Luna-0
for interface review. The complete first integration milestone remains not
ready.

## Reproduction and rollback

From the repository root, run the commands in the validation table. The
implementation is uncommitted on `main` at `e2b8276`; removing the new
eligibility module, its package exports, focused tests, and this handoff
restores Luna-8 work while preserving unrelated working-tree changes.

## Next assignment

Luna-5 should define the local resource/usefulness adapter and agree with
Luna-0 on reward units and delivery ownership. Luna-11 should then independently
verify delayed credit together with energy, streaming classification, and the
remaining acceptance matrix. This handoff does not claim benchmark,
energy/utility, Luna-11, or hardware readiness.