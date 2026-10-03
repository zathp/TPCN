# Luna-0 Authorization Handoff - Luna-23 E2 Time Representability

```yaml
tpcn_handoff:
  agent: "Luna-0"
  luna_identifier: "Luna-23"
  descriptive_name: "ACP-0004 E2 positive-delay logical-time representability correction"
  task_id: "luna-23-e2-time-representability-20261003"
  component: "MultiExcursionNeuron strict-future internal scheduling"
  status: "authorized; not executed"
  contract_version: "1.1"
  branch: "main"
  base_revision: "baec12ad368239d959ca747d5a4e28c96746dd6e"
  result_revision: "not executed"
  dependencies:
    - "ACP-0004 E2 / Luna-21 independently closed"
    - "Luna-0 second independent review of Luna-22 published"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["IMPLEMENTATION", "VERIFICATION"]
  hypothesis: "A positive finite E2 return delay can be represented as a deterministic strictly later timestamp without changing the E2 state machine."
  counter_hypothesis: "Any compatible numerical correction changes canonical event timing or fails to guarantee bounded return."
  interfaces_relied_on:
    - "MultiExcursionNeuron local timestamp, pending event and generation validation"
    - "Closed SingleExcursionNeuron/E1 behavior"
    - "TPCN-IR-2 revision-1 standalone E2 reconstruction"
  label_information_boundary:
    - "No labels, future inputs, task metrics or global clock are available to the neuron."
  timing_assumptions:
    - "Analytic E2 decay/rearm delay is positive and finite."
    - "The stored due timestamp must be strictly greater than local time."
  reset_boundaries:
    - "Existing E2 reset and identity high-water behavior remain unchanged."
  resource_bounds:
    - "Existing finite event budget, one valid pending event and bounded E2 state."
  authorized_scope:
    - "Only E2 strict-future timestamp calculation/validation in tpcn/excursion_neuron.py."
    - "Focused numerical-boundary tests in tests/test_e2_multi_excursion.py."
    - "One Luna-23 completion handoff."
  unauthorized_scope:
    - "E1 behavior, Luna-22 experiment adapter, downstream consumers, IR-2 schema, dataset work, learning, topology, backends and hardware."
  controls:
    - "Closed E1 scheduling and reset regressions."
    - "Existing E2 finite-return and standalone IR-2 regressions."
  measurements:
    - "Computed positive delay, current timestamp, representable due timestamp, event ordering and finite-return bound."
  information_boundary_check:
    - "Correction depends only on local state, configuration and local logical time."
  hardware_mapping:
    - "Hardware-neutral reference correction only; no equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A08", "A15"]
  preserves:
    - "A01-A15 and accepted ACP-0004 E2 state transitions."
    - "Independently closed E1 behavior and TPCN-IR-2 schema revision 1."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-23.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-23-e2-time-representability-20261003.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All implementation tests; Luna-23 has not executed."
  assumptions:
    - "The observed defect is a compatible floating-point timestamp representation issue."
  unresolved:
    - "Luna-23 must stop and return to Luna-0 if strict-future behavior requires new canonical timing semantics."
  recommended_next_agent:
    - "Luna-0 for independent verification; downstream migration remains unauthorized."
```

## Authorized assignment

Implement and verify only the E2 logical-time representability correction
described in [luna-23.agent.md](../../.github/agents/luna-23.agent.md).
The reproducer and exact timestamp values are recorded in
[the Luna-0 second-review handoff](luna-0-second-independent-review-ACP-0006-Luna-22-20261003.md).

Preserve the existing analytic delay equation, strict future ordering,
generation validity and bounded return. Do not affect E1 or any downstream
consumer. If a compatible correction is not clear, stop and return evidence
to Luna-0 before changing semantics.

No implementation or tests were run as part of this authorization. Luna-23
must publish a completion handoff and return it to Luna-0 for independent
verification.
