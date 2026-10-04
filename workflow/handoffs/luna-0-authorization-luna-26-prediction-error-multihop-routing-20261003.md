# Luna-0 Authorization — Luna-26 Multi-Hop Prediction-Error Routing

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Authorize bounded Luna-26 error-forwarding correction"
  task_id: "luna-0-authorization-luna-26-prediction-error-multihop-routing-20261003"
  component: "ACP-0006 opaque prediction-error forwarding"
  status: "authorized; not executed"
  contract_version: "1.1"
  branch: "main"
  base_revision: "42026a9fc3ccc1b1fdc83e0344c79312f2d76b14"
  result_revision: "42026a9fc3ccc1b1fdc83e0344c79312f2d76b14 (reviewed code baseline)"
  dependencies:
    - "Accepted ACP-0006"
    - "Luna-23 CLOSED / independently verified"
    - "Luna-24 CLOSED / independently verified"
    - "Luna-25 CLOSED / independently verified for luna25-v1"
    - "Luna-0 closure-readiness finding: multi-hop prediction-error forwarding defect"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "The integration adapter can forward a real matched opaque PredictionError hop-by-hop over existing finite-delay edges without changing any closed component contract."
  counter_hypothesis: "Node-local forwarding cannot be corrected without altering topology or canonical architecture semantics."
  interfaces_relied_on:
    - "ExcursionCharacterRuntime._deliver_prediction_error"
    - "BoundedTopology.route"
    - "LocalPredictor causal observation and PredictionError"
    - "EligibilityLedger bounded per-destination attribution"
  label_information_boundary:
    - "No label is available to prediction creation, error matching or routing."
    - "Only actually admitted input contributes an observation; no future point may be inspected."
  timing_assumptions:
    - "Every hop uses the existing positive finite edge delay and shared EventQueue."
    - "Equal-time ordering remains deterministic."
  reset_boundaries:
    - "Error-deduplication and route state remain character-scoped and clear at the existing character reset."
  resource_bounds:
    - "Existing character queue/event budgets and per-prediction/destination delivery guard remain bounded."
    - "Existing topology node, edge, fan-in, fan-out and routing capacities remain unchanged."
  authorized_scope:
    - "Only .github/agents/luna-26.agent.md, workflow authorization/governance records, and the Luna-26-owned files listed in that contract."
    - "Luna-26 implementation ownership: tpcn/experiment_excursion_runtime.py limited to prediction-error forwarding; tests/test_excursion_integration.py; Luna-26 completion handoff."
  unauthorized_scope:
    - "No topology API, neuron, predictor, ledger, schema, ACP, A01-A15, benchmark, artifact or downstream consumer changes."
    - "No predictor/credit efficacy tuning or Luna-22 closure claim."
  controls:
    - "Actual E2 excursion -> prediction -> later admitted scalar -> nonzero PredictionError."
    - "One-hop and two-hop directed paths, plus unreachable reverse node."
    - "Convergent diamond testing per-destination duplicate suppression."
  measurements:
    - "Error IDs and complete payload fields per hop."
    - "Finite event timestamps, queue ordering, reachability, local error-consumer calls and duplicate-credit counts."
  information_boundary_check:
    - "Require runtime-generated matching/error and incremental input admission; no injected future target or label."
  hardware_mapping:
    - "CPU software-reference correction only; no hardware equivalence claim."
  architecture_invariants_touched: ["A01", "A03", "A04", "A06", "A07", "A08", "A11", "A15"]
  preserves:
    - "Accepted ACP-0006 rule 6 and unchanged A01-A15."
    - "BoundedTopology numeric Model-B transfer and all closed neuron/predictor/ledger interfaces."
    - "Luna-23, Luna-24 and Luna-25 closures."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-26.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-26-prediction-error-multihop-routing-20261003.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Authorization-baseline focused suite: 43 passed; includes local matched prediction/error and delayed-credit mechanics."
    - "Prescribed ACP-0006 regression set: 334 passed."
    - "Independent valid three-node probe reproduced a matched nonzero error that reached n0 and n1 but never reachable n2."
  tests_failed:
    - "The independent multi-hop prediction-error forwarding probe violates ACP-0006 rule 6."
  tests_not_run:
    - "Luna-26 correction tests and post-correction regression: not run; implementation is not authorized in this turn."
    - "Hardware equivalence: not run/not authorized."
  assumptions:
    - "The received Git token `F9h8mimKAXJ74YAEM4NsrHja2pxrrFaJyX29rnc7RyLb` is not a resolvable Git object in this repository; the actual commit chain was verified using published commit hashes."
  unresolved:
    - "Luna-22 remains blocked until Luna-26 completion and independent Luna-0 review."
    - "Downstream compatibility failures remain separately classified; they are not Luna-22 closure blockers under the accepted ownership/scope."
    - "Predictive task efficacy and useful delayed-credit learning remain unestablished."
  recommended_next_agent:
    - "Luna-26 for the bounded multi-hop forwarding correction."
```

## Authorization decision

Luna-26 is authorized only to correct the reproducible node-local
prediction-error forwarding defect specified in
[`.github/agents/luna-26.agent.md`](../../.github/agents/luna-26.agent.md).
The accepted ACP-0006 rule is already explicit; this requires no new
architecture decision or ACP. Luna-26 must stop and return to Luna-0 if the
adapter-only correction proves insufficient.

Luna-26 must not execute during this authorization/review publication. Its
completion handoff returns to Luna-0 for an independent review. Luna-22
remains BLOCKED until then.
