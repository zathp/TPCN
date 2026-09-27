# Luna-14 Dispatch Handoff

```yaml
tpcn_handoff:
  agent: Luna-14 ModelSim/FPGA Trace Bridge and DE1-SoC Visualization Foundation
  task_id: visualization-fpga-luna-14
  component: ModelSim trace bridge and downstream DE1-SoC diagnostic path
  status: blocked
  contract_version: "1.0"
  branch: main
  base_revision: 1cf4065
  result_revision: not run
  architecture_invariants_touched: [A01, A03, A04, A08, A15]
  preserves:
    - Luna-12 canonical visualization format
    - downstream-only diagnostic capture
    - independent visualization reset and non-blocking core behavior
    - TPCN topology, classifier, reward, and event datapath
  architecture_change: false
  proposal: null
  files_changed: []
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: [all ModelSim, FPGA, DE1-SoC, and visualization checks]
  assumptions:
    - Luna-12 must pass before dispatch.
    - Luna-13 may provide parity evidence but is not required.
  unresolved:
    - board capture resources, VGA timing, and reusable Ethernet infrastructure require implementation review.
  recommended_next_agent: [Luna-0 after Luna-14 gate evidence]
```

## Dispatch status

Luna-14 is blocked. It is not implicitly authorized by Luna-12's prompt or by Luna-13 completion. Luna-0 must record a passing Luna-12 gate and explicitly authorize this milestone.

## Required completion evidence

Record canonical trace decoding, framing/order, X/Z/unknown handling, reset and snapshot boundaries, dropped-record/overflow behavior, downstream-only backpressure tests, DE1-SoC/VGA status, exact commands and environment, and all unrun hardware checks using the handoff template. Do not claim hardware equivalence.
