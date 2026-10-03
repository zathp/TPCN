# Luna-0 Authorization Handoff - Luna-24 IR-2 Provenance Boundary

```yaml
tpcn_handoff:
  agent: "Luna-0"
  luna_identifier: "Luna-24"
  descriptive_name: "ACP-0006 integrated IR-2 residual-provenance boundary correction"
  task_id: "luna-24-ir2-quiescent-provenance-20261003"
  component: "Integrated quiescent IR-2 startup validation"
  status: "authorized; not executed"
  contract_version: "1.1"
  branch: "main"
  base_revision: "a206f2e8fec8f0c72d9196b2bcca9d2e734c7974"
  result_revision: "not executed"
  dependencies:
    - "Accepted ACP-0006 and Luna-22 published implementation"
    - "Luna-0 second independent review of Luna-22 published"
    - "TPCN-IR-2 schema revision 1 independently closed"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "Integrated IR-2 startup can reject assigned residual provenance and sticky truncation while preserving valid quiescent startup and standalone E2 round trips."
  counter_hypothesis: "The accepted ACP-0006 boundary requires restoring these provenance fields or cannot distinguish safe initialization."
  interfaces_relied_on:
    - "ExcursionCharacterRuntime.from_quiescent_ir2"
    - "IR2Neuron revision-1 local state and provenance fields"
    - "Standalone E2 IR-2 conversion and continuation"
  label_information_boundary:
    - "Only serialized local state and declared model/configuration may be checked."
  timing_assumptions:
    - "Integrated startup is a fresh quiescent boundary, not a live-network resume."
  reset_boundaries:
    - "Character-local provenance, state and pending work are absent at integrated startup."
  resource_bounds:
    - "Existing finite provenance capacity, event budget, queue and topology bounds remain unchanged."
  authorized_scope:
    - "Only integrated startup validation in tpcn/experiment_excursion_runtime.py."
    - "Focused startup-boundary tests in tests/test_excursion_integration.py."
    - "One Luna-24 completion handoff."
  unauthorized_scope:
    - "IR-2 schema, standalone E2 adapter, neuron state machine, experiment selection, dataset, visualization and research consumers."
  controls:
    - "Valid empty-provenance quiescent startup with permitted identity counters."
    - "Standalone active/pending E2 IR-2 round trips."
  measurements:
    - "Valid/invalid startup matrix, deterministic continuation, schema revision and standalone round-trip outcomes."
  information_boundary_check:
    - "No labels, future events, global state or task metrics enter the adapter."
  hardware_mapping:
    - "Hardware-neutral software-reference adapter only; no equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A08", "A15"]
  preserves:
    - "A01-A15, accepted ACP-0006 and TPCN-IR-2 schema revision 1."
    - "Standalone active/pending E2 IR-2 support."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-24.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-24-ir2-provenance-20261003.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All implementation tests; Luna-24 has not executed."
  assumptions:
    - "The accepted quiescent-startup requirement 'no residual provenance' includes assigned entries and provenance_truncated."
  unresolved:
    - "Stop and return to Luna-0 if the accepted boundary does not justify rejecting these fields."
  recommended_next_agent:
    - "Luna-0 for independent verification; downstream migration remains unauthorized."
```

## Authorized assignment

Implement and verify only the integrated startup correction described in
[luna-24.agent.md](../../.github/agents/luna-24.agent.md). The independently
observed acceptance of assigned provenance and sticky truncation is recorded
in [the Luna-0 second-review handoff](luna-0-second-independent-review-ACP-0006-Luna-22-20261003.md).

Reject residual provenance without modifying the schema or standalone E2
conversion. Preserve valid quiescent startup, permitted identity high-water
counters and standalone active/pending E2 reference round trips. Stop and
return to Luna-0 if the accepted boundary does not support this correction.

No implementation or tests were run as part of this authorization. Luna-24
must publish a completion handoff and return it to Luna-0 for independent
verification.
