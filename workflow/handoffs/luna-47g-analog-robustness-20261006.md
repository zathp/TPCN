---
tpcn_handoff:
  agent: "Luna-47G"
  luna_identifier: "Luna-47G"
  descriptive_name: "Analog component tolerance and mismatch robustness"
  task_id: "luna-47g-analog-robustness-20261006"
  component: "Independent synthetic simulation stand-in"
  status: "preregistered - NOT EXECUTED"
  contract_version: "1.2"
  branch: "copilot/luna47g-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  result_revision: "Not yet executed; containing preregistration commit"
  dependencies: ["Reviewed component specifications unavailable; unreviewed Luna-47E excluded"]
  owner: "Project owner"
  classification: ["simulation only", "not hardware feasibility", "not efficacy"]
  hypothesis: "The independent stand-in preserves the six regimes under the predeclared tolerance bands."
  counter_hypothesis: "Tolerance draws break one or more regimes, sign behavior, bounds, or finite neutral return."
  interfaces_relied_on: ["experiments/luna47g/config.json", "experiments/luna47g/fixtures.json"]
  label_information_boundary: ["No labels, dataset, production computation, or other lane mechanism inputs"]
  timing_assumptions: ["Dimensionless local event time, analytic elapsed-time decay, positive local return delay 0.1"]
  reset_boundaries: ["Independent zero-state reset per signed fixture"]
  resource_bounds: ["State 8, output 1, 128 inputs, 192 events, 16 outputs per fixture"]
  authorized_scope: ["Simulation and evidence within exclusively owned lane paths"]
  unauthorized_scope: ["No production/topology/governance edits, ACP, efficacy, hardware claim, composition, or successor"]
  controls: ["Nominal, matched signs, offset-reversed and zero-offset mirrors, temporal spacing, fixed corner interactions"]
  measurements: ["Predeclared in PROTOCOL.md; outcomes not yet run"]
  information_boundary_check: ["Standalone Python standard library; no TPCN imports or result feedback"]
  hardware_mapping: ["Assumed dimensionless multipliers only; missing reviewed part specifications"]
  architecture_invariants_touched: ["A01-A03 event semantics", "A04 no topology", "A08 finite bounds", "A09 local count proxies", "A15 no feasibility claim"]
  preserves: ["All production files and baseline evidence; Luna-46 MIXED; ACP status unchanged"]
  architecture_change: false
  proposal: null
  files_changed: ["experiments/luna47g/", "tests/test_luna47g_robustness.py", "workflow/handoffs/luna-47g-analog-robustness-20261006.md"]
  tests_added: ["Standalone event-time, signed, boundedness, validation and retained evidence tests"]
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All tests and sampling; this document is committed before execution"]
  assumptions: ["Uniform bounded static variation and event-sampled bounded noise, not real fabrication distributions"]
  unresolved: ["Execution, source hashes, outcomes, publication, independent Luna-0 review"]
  recommended_next_agent: ["Independent Luna-0 review after lane execution and publication; no delegation or successor"]
---

# Luna-47G preregistration

**HYPOTHESIZED:** The six-regime invariant may survive small but not broad
component variation in this explicitly experimental stand-in. Nothing here
establishes real-hardware feasibility. The model and every criterion are frozen
in `experiments/luna47g/PROTOCOL.md`, `config.json`, and `fixtures.json` before
outcomes. Only these owned paths are edited. This handoff will be completed
after execution without changing the protocol to fit outcomes.
