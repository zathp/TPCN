---
tpcn_handoff:
  agent: "Luna-47D implementation worker; independent Luna-0 review pending"
  luna_identifier: "Luna-47D"
  descriptive_name: "Spike compression and bounded threshold oscillator"
  task_id: "luna-47d-spike-compression-20261006"
  component: "Independent synthetic output model"
  status: "protocol declared; NOT EXECUTED"
  contract_version: "1.2"
  branch: "copilot/luna47d-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  result_revision: "not executed; filled at evidence publication"
  dependencies: ["Published Luna-0 authorization", "Luna-46 reviewed MIXED context only"]
  owner: "Project owner"
  classification: ["experimental output model", "synthetic mechanism only"]
  hypothesis: "A dissipative charge-drain output mapping compresses short moderate clusters and produces finite extreme bursts with bounded recovery."
  counter_hypothesis: "Count, timing, state bound, symmetry or recovery fails under the frozen fixtures."
  interfaces_relied_on: ["experiments/luna47d/PROTOCOL.md", "experiments/luna47d/fixtures.json"]
  label_information_boundary: ["No labels, network or global training data enter the model."]
  timing_assumptions: ["Exact rational logical event times; input-before-due ties; no global tick."]
  reset_boundaries: ["Charge, pending opportunity and contributors reset per synthetic trajectory."]
  resource_bounds: ["16 inputs; absolute drive/state <=32; one pending opportunity; 128-opportunity watchdog; primary output <=32; tail 144."]
  authorized_scope: ["Owned isolated model, tests, synthetic artifacts and this handoff only."]
  unauthorized_scope: ["No A/B/C dependency, production/topology/governance edits, upstream reachability, efficacy, ACP, promotion, merge, successor or delegation."]
  controls: ["Pre-outcome protocol/code commit", "Polarity mirroring", "Weak-drain negative", "Invalid-domain and record-fault controls", "Exact replay"]
  measurements: ["Input/output identities/times", "State trajectory", "Count/latency/spacing", "Neutral recovery", "Hashes/revisions/configuration"]
  information_boundary_check: ["Standalone standard-library model; no feedback into TPCN."]
  hardware_mapping: ["Not tested; synthetic dimensionless software model, not hardware equivalence."]
  architecture_invariants_touched: ["A01/A02 event-triggered analytic local evolution", "A03 strict-future output opportunities; no inter-node route claim", "A08 dissipative bounded state/event budget", "A15 no portability/equivalence claim; no clause change"]
  preserves: ["Luna-46 MIXED", "A01-A15", "ACP-0007/ACP-0008", "Production/evidence baseline 2cef8ea4b37a4ae586e3f383511cba63c9268ddc"]
  architecture_change: false
  proposal: null
  files_changed: ["experiments/luna47d/", "tests/test_luna47d_output_model.py", "workflow/handoffs/luna-47d-spike-compression-20261006.md"]
  tests_added: ["Frozen regime, analytic recurrence/burst, exact identities, negative boundaries, failure gates, symmetry and replay"]
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All checks: protocol/code phase not yet executed"]
  assumptions: ["Synthetic accumulator increments are exogenous, not claims about reachable network excitation."]
  unresolved: ["Outcome unknown", "Independent Luna-0 review required"]
  recommended_next_agent: ["Independent Luna-0 review after evidence publication; no successor authorization"]
---

# Luna-47D pre-outcome handoff

HYPOTHESIZED, not observed: the frozen dissipative reservoir rule may support
the specified compression and burst regimes. The exact mechanism, fixtures,
parameter domain, tolerances, bounds, negative controls and verdict criteria
are declared in `experiments/luna47d/PROTOCOL.md`. No outcome has been generated.
Validation, reproduction and observed limitations will be completed after the
pre-outcome protocol/code commit. Rollback is the authorization baseline;
there are no production changes to revert.
