# Luna-13F Corrective Execution Handoff

**PASS WITH FOLLOW-UP - RUNTIME EVIDENCE DISTINGUISHES CANDIDATES, GENERALITY NOT ESTABLISHED**

```yaml
tpcn_handoff:
  agent: Luna-13F
  task_id: runtime-generated-local-candidate-evidence-Luna-13F
  status: pass_with_follow_up
  classification: [EXPERIMENT, VERIFICATION, CPU-only]
  starting_revision: 3379403a8b58649a85c2604ba3044e55e4fe99e9
  executed_revision: 3379403a8b58649a85c2604ba3044e55e4fe99e9
  branch: main
  starting_tree_state: clean
  execution_tree_state: dirty_by_corrective_changes
  architecture_change_required: false
  luna_13g: unauthorized
  fixture_id: luna-13f-runtime-generated-local-evidence-v1
  event_budget: 32
  queue_capacity: 16
  candidate_capacity: 2
  edge_capacity: 3
  one_slot_competition: true
  neutral_schedule: "relay receives four short associations; noise receives four long intervals; assignment is independent of utility labels"
  evidence_owner: source-local TemporalAssociationPolicy at source
  evidence_bounds: "history 8, maximum score 8, maximum two candidate records, reset per run, frozen at decision"
  decision_timestamp: 19.0
  freeze_timestamp: 19.0
  admission_timestamp: 19.0
  first_held_out_timestamp: 20.0
  primary_evidence: {relay: 4.0, noise: 0.0}
  canonical_scores: {relay: 4.0, noise: 0.0}
  selected_candidate: G
  held_out: {G: "2/2", H: "1/2"}
  no_growth: "2/2"
  no_growth_events: 8
  selected_candidate_events: 12
  no_growth_proxy_energy: 8.0
  selected_candidate_proxy_energy: 12.0
  proxy_energy_unit: "activity-cost-proxy; uncalibrated"
  contract_audit: {passed: 13, failed: 0, not_run: 5}
  focused_tests: "10 passed"
  preservation_tests: "62 passed"
  full_cpu_suite: "286 passed, 1 skipped"
  next_action: independent Luna-0 review
```

## Corrective answers

**OBSERVED:** `_schedule` now uses neutral endpoint order (`relay`, `noise`) and
never reads `beneficial_role` or `harmful_role`. Swapping those external
designations leaves the pre-admission schedule unchanged. Both candidates get
four observations. Relay observations follow source anchors within the local
association window; noise observations are three time units apart and do not
form associations.

**OBSERVED:** `TemporalAssociationPolicy` generates bounded source-local counts
from ordinary runtime events. Provenance records event ID/type,
source/destination, timestamp, receiving component, neuron state before/after,
elapsed local time, score delta, policy state and evidence timestamp. The
unchanged `StructuralPlasticityController` scores the frozen evidence directly.

**OBSERVED:** Evidence freezes at `19.0` before admission. Later events do not
change historical score, rank or selected edge. Budget-exhausted evidence is
marked incomplete and performs no scientific admission. Held-out evaluation
starts at `20.0`, strictly after admission.

**OBSERVED:** Primary evidence and scores are relay `4.0`, noise `0.0`; `G` is
selected under the default external mapping. Equalization produces runtime
equality (`2.0`, `2.0`). No-evidence produces two legal zero-score candidates;
any selection is recorded as deterministic tie-breaking, not utility evidence.
Matched exposure, order reversal, relabeling, mirroring, shuffle, reversal,
uniform interval, replay and bounded execution are recorded as passed in the
audit. Five controls remain explicitly not run.

**OBSERVED:** Selected `G` preserves the held-out task at `2/2`, equal to
no-growth `2/2`, but uses 12 events and `12.0` activity-cost-proxy units versus
8 events and `8.0` units for no-growth. This is not a task or resource
improvement claim. General utility prediction, scalability and generalization
remain unproven.

**INFERRED:** No architecture change is required by this corrective execution;
the existing bounded local policy and canonical admission path suffice for this
fixture. Return to Luna-0 for independent review. Luna-13F does not create,
authorize or dispatch Luna-13G.