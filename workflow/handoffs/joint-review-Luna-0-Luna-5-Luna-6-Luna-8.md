# Luna-0 Joint Integration Review: Luna-5, Luna-6, and Luna-8

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  task_id: "joint-review-luna-5-luna-6-luna-8"
  component: "joint review of local energy/utility, sequential stroke events, and delayed credit"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "uncommitted"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10", "A11", "A15"]
  preserves:
    - "Luna-1 through Luna-4 event, local-time, predictive-error, bounded-neuron, and bounded-topology interfaces."
    - "Luna-6 keeps labels and future stroke points out of event payloads and emits START_CHARACTER, ordered stroke events, and END_CHARACTER."
    - "Luna-5 owns local activity cost and explicit utility policy; Luna-8 owns local eligibility, decay, expiry, and credit attribution."
    - "No global neural clock, spatial reservoir dependency, unrestricted global state, or classifier logic was added to the reusable core."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/energy_utility.py"
    - "tests/test_eligibility.py"
    - "workflow/handoffs/energy-utility-Luna-5.md"
    - "workflow/handoffs/sequential-stroke-dataset-Luna-6.md"
    - "workflow/handoffs/delayed-credit-Luna-8.md"
    - "workflow/handoffs/joint-review-Luna-0-Luna-5-Luna-6-Luna-8.md"
  tests_added:
    - "RewardMessage-to-RewardSignal causal boundary regression"
  tests_passing:
    - "Focused Luna-5/Luna-6/Luna-8 suite: 20 passed"
    - "Full regression suite: 59 passed"
    - "python -m compileall -q tpcn tests"
    - "git diff --check"
    - "Deterministic explicit-timestamp stream replay and reward conversion smoke check"
  tests_failed: []
  tests_not_run:
    - "Actual A-Z sequential stroke benchmark: no dataset/version/split selected."
    - "Luna-7 streaming classifier: intentionally not started in this review."
    - "Luna-11 independent acceptance matrix."
    - "FPGA, FPAA, hybrid, and calibrated hardware validation."
  unresolved:
    - "Dataset, licensing, class set, native timing, and writer-disjoint split remain Luna-0 decisions."
    - "Final utility coefficients and hardware precision tolerances remain unselected."
    - "The combined Luna-5/Luna-6/Luna-7/Luna-8 gate remains pending Luna-7 and a real benchmark run."
  recommended_next_agent:
    - "Luna-7: implement the external streaming classification interface."
```

## Outcome

The joint gate passes after one interface defect was repaired. Luna-5 now
exposes `RewardMessage.to_reward_signal()`, which maps opaque `credit_id` to
the Luna-8 local prediction identity and preserves reward amount. Callers
deliver the converted payload in an addressed Luna-1 `Event` at the original
reward timestamp. Luna-8 retains ownership of matching, exponential decay,
expiry, bounded credit, and attribution. No ACP is required.

Luna-6's event protocol is compatible with Luna-1 through Luna-4: it emits
causal runtime events in temporal order, derives features from current and
past points plus training-fitted constants, resets between characters, and
contains no labels. Its finite point bound and the runtime queue bound remain
the applicable resource limits.

## Gate Evidence

| Check | Result | Evidence |
|---|---|---|
| Shared Luna-5/Luna-8 reward interface | Passed | Typed adapter regression and 20-test joint suite |
| Sequential event semantics | Passed | START, ordered stroke, END, timestamp/reset/label tests |
| Delayed reward causality | Passed | Later addressed reward decays and credits only on ledger receipt |
| Bounded state | Passed | Saturating energy/counters, finite traces/credit, max points and queue capacity |
| Deterministic seeded execution | Passed for available reference components | No RNG is consumed; explicit timestamp replay and fixed fixtures reproduce identically |
| Luna-1 through Luna-4 compatibility | Passed | Full regression, including runtime, neuron, topology, prediction, and the three local suites |

The focused command was:

```text
python -m pytest -q tests/test_energy_utility.py tests/test_stroke_dataset.py tests/test_eligibility.py
```

It passed with 20 tests. The full command `python -m pytest -q` passed with 59
tests. Compilation and `git diff --check` also passed. The initial interface
defect was assigned to Luna-5, repaired, and the same joint gate was rerun.

## Authorization and Boundary

Luna-7 is explicitly authorized to begin the streaming classification
interface. Its implementation must expose 26 A-Z class outputs only when the
selected dataset has those classes, derive them only from TPCN activity, keep
labels out of inference, and emit no authoritative character classification
before `END_CHARACTER`. Intermediate diagnostic confidence/state is allowed,
but is not a final classification.

Luna-11, hardware acceptance, and any claim of benchmark accuracy remain
deferred. The next gate is the combined Luna-5/Luna-6/Luna-7/Luna-8 review.
