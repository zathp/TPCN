# Luna agent handoff

```yaml
tpcn_handoff:
  agent: Luna-5 Energy and Utility
  task_id: "energy-utility"
  component: "bounded local activity/resource accounting and explicit utility interfaces"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "e2b8276"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A04", "A07", "A09", "A10", "A11", "A15"]
  preserves:
    - "Luna-1 event and local-time semantics; metering time is not neural time."
    - "Luna-2 neuron, Luna-4 topology, and Luna-3 prediction/error semantics."
    - "Opaque local reward/usefulness inputs without hidden labels or global state."
  architecture_change: false
  proposal: null
  files_changed:
    - "tpcn/energy_utility.py"
    - "tpcn/__init__.py"
    - "tests/test_energy_utility.py"
    - "workflow/handoffs/energy-utility-Luna-5.md"
  tests_added:
    - "tests/test_energy_utility.py"
  tests_passing:
    - "Focused Luna-5 suite: 7 passed"
    - "Full available regression suite: pending final run"
    - "Package and test compilation: pending final run"
  tests_failed: []
  tests_not_run:
    - "Luna-8 delayed-credit implementation and integration"
    - "Luna-11 acceptance matrix and streaming stroke benchmark"
    - "FPGA, FPAA, hybrid, and calibrated hardware validation"
  assumptions:
    - "Energy is measured in declared activity-cost proxy units; no physical joules are claimed."
    - "Saturating counters and energy define deterministic finite overflow behavior."
    - "Utility formula is explicitly selected per instance; the core mandates neither net nor ratio utility."
  unresolved:
    - "Luna-8 must choose eligibility decay, attribution, expiry, and whether it consumes cost snapshots or utility decisions."
    - "Luna-0/Luna-11 must set integration-level proxy coefficients, capacities, and hardware precision tolerances."
  recommended_next_agent:
    - "Luna-8: consume RewardMessage.credit_id/timestamp and local activity cost without moving attribution policy into Luna-5."
    - "Luna-11: independently verify the acceptance matrix after delayed credit and streaming classification exist."
```

## Outcome and owned scope

Added `LocalEnergyModel` in `tpcn/energy_utility.py`. It records local activity,
events, and Luna-3 `PredictionError` observations in declared proxy units. Its
finite counters and cumulative energy saturate at configured bounds. `update(dt)`
advances only the meter's local measurement clock and does not update neurons or
create a global neural tick.

Added `RewardAdjustedUtility`, immutable `RewardMessage`,
`UsefulnessObservation`, `UtilityDecision`, and `EnergySnapshot`. Net utility
(`reward - lambda * cost`) and ratio utility are explicit selectable policies;
neither is promoted to a permanent architecture formula. Retention requires
positive-cost work and utility above the configured threshold, so idle work is
not rewarded as useful efficiency.

## Architecture evidence

- **A01-A02:** meter timestamps and `update(dt)` are local measurement details;
  irregular times are accepted independently and no neural tick exists.
- **A04/A08:** counter, energy, and reward/usefulness message capacities are
  finite; numeric overflow saturates or rejects at the declared boundary.
- **A07:** reward and usefulness are explicit local messages. `credit_id` is
  opaque, and no labels, global evaluation state, or remote mutation is used.
- **A09:** activity categories and costs reconcile to a bounded local energy
  proxy with a declared unit.
- **A10:** useful high-cost work can be retained while comparable low-reward
  work is suppressed; inactivity is not retained by default.
- **A11:** `RewardMessage` carries causal timestamp, opaque `credit_id`, and an
  optional explicit stable `message_id` for delayed-credit compatibility.
  When omitted, `credit_id` is the logical message identity. Luna-5 performs
  no eligibility or attribution.
- **A15:** fixed-schema records, finite state, and abstract proxy units leave
  FPGA popcount and FPAA continuous approximation as documented hardware
  mappings, without claiming equivalence.

No Architecture Change Proposal is required. Ten-pathway gating, structural
plasticity, classifier behavior, delayed credit, and hardware validation remain
outside this assignment.

## Luna-8 coordination boundary

Luna-8 may consume `RewardMessage.credit_id`, `RewardMessage.timestamp`, local
activity timestamps/costs, and `UtilityDecision` results. Luna-5 does not retain
eligibility traces, match rewards to prior activity, decay credit, or mutate a
neuron/connection. A delayed reward must arrive as an explicit local message;
the energy model does not infer reward from labels or prediction outcomes.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `python -m pytest -q tests/test_energy_utility.py` | `e2b8276`, Windows PowerShell, Python 3.10.8; deterministic inputs | Pass, 7 tests | Focused Luna-5 suite |
| `python -m pytest -q` | `e2b8276`, Windows PowerShell, Python 3.10.8; existing seed 17 tests | Pending final run | Full available regression |
| `python -m compileall -q tpcn tests` | Windows PowerShell, Python 3.10.8 | Pending final run | Package and tests compile |

## Benchmark and resource results

No dataset, split, classification, connectivity, latency, or hardware result
applies to this local component. Energy unit is
`activity-cost-proxy`; calibration to joules is not performed. FPGA popcount
switching estimates and FPAA continuous approximations are future mappings, not
equivalent measurements. Utility behavior is covered by focused deterministic
net-utility tests; no seed is required.

## Assumptions, limitations and unresolved issues

The meter's `activity` and `energy` are cumulative bounded proxy values; idle
time is inspection metadata and does not decay or generate cost. Activity
categories are a fixed finite set. Reward totals are bounded by message count
but do not attribute credit. Luna-8 must define its eligibility trace
representation and attribution rules before cross-component integration.

## Reproduction and rollback

From the repository root:

```text
python -m pytest -q tests/test_energy_utility.py
python -m pytest -q
python -m compileall -q tpcn tests
```

The result is uncommitted on `main` at base `e2b8276`. Removing the new energy
module, its exports/tests, and this handoff rolls back Luna-5 while preserving
unrelated worktree changes.

## Next assignment

Luna-8 should implement bounded local eligibility and delayed reward attribution
against this explicit boundary. Luna-11 should independently verify energy,
usefulness, delayed credit, hardware limitations, and the complete streaming
milestone. The architecture is not integration-ready until those checks pass.
