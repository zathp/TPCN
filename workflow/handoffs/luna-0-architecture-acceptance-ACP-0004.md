# Luna-0 ACP-0004 Acceptance and E1 Dispatch

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "ACP-0004 canonical excursion contract acceptance"
  task_id: "luna-0-architecture-acceptance-ACP-0004"
  component: "Canonical excursion neuron architecture"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "80b7989ec5b7f5913362e812eddcc3d845b826c4"
  result_revision: "uncommitted ACP-0004 acceptance documentation"
  dependencies:
    - "ACP-0002 N2 CLOSED"
    - "ACP-0003 accepted for staged implementation"
    - "ACP-0003 H1 independently verified and CLOSED"
    - "ACP-0004 independent review complete"
  owner: "Luna-0 Architecture Guardian / project owner"
  classification: ["ARCHITECTURE-PROMOTION", "VERIFICATION"]
  hypothesis: "The revised ACP-0004 defines a complete bounded canonical excursion state machine that E1 can implement without backend-specific interpretation."
  counter_hypothesis: "A required transition, timing, identity, provenance or finite-bound rule remains unspecified or contradicts A01-A15."
  interfaces_relied_on:
    - "ACP-0002 N2 Model-B"
    - "ACP-0003 TPCN-IR-1 boundary"
    - "A01-A15"
  label_information_boundary:
    - "No labels, future inputs or global evaluation/orchestration state enter canonical neuron state."
  timing_assumptions:
    - "Local elapsed decay and finite positive internal-event delays."
    - "External same-time events precede destination-local internal events."
    - "No global neural timestep."
  reset_boundaries:
    - "Ordinary episodes re-arm only after finite S_REARM reaches N."
    - "M final residual enters S_PENDING; no unspecified hard reset."
  resource_bounds:
    - "Finite x, four-mode state, one valid pending internal event, P <= 64 provenance, finite IDs and event budget."
  authorized_scope:
    - "Accept ACP-0004 for staged implementation."
    - "Authorize only Luna-19 E1 dispatch contract."
    - "Update governance records and terminology."
  unauthorized_scope:
    - "E1 implementation execution in this task"
    - "M/multi-excursion implementation"
    - "IR-2, learning, backends, approximation, calibration or hardware equivalence"
    - "ACP-0002 N3, ACP-0003 H2, Luna-13F reopening or Luna-13G"
  controls:
    - "One canonical excursion maps to one digital event."
    - "Fixed positive internal delays and analytic re-arm."
    - "Generation-token cancellation with stale-event no-op."
    - "Oldest provenance eviction with explicit truncation."
  measurements:
    - "No runtime or hardware measurements; architecture/governance revision only."
  hardware_mapping:
    - "Digital event for GPU/software/FPGA; physical spike/analog excursion for FPAA."
    - "No backend-specific implementation is authorized."
  architecture_invariants_touched:
    - "A01"
    - "A02"
    - "A03"
    - "A04"
    - "A06"
    - "A07"
    - "A08"
    - "A09"
    - "A10"
    - "A11"
    - "A15"
  preserves:
    - "A01-A15 unchanged"
    - "ACP-0002 N2 and Model-B transfer"
    - "TPCN-IR-1 current closed scope"
    - "ACP-0002 N3 unauthorized"
    - "ACP-0003 H2 unauthorized"
    - "Luna-13F CLOSED"
    - "Luna-13G unauthorized"
  architecture_change: true
  proposal: "ACP-0004 Accepted for staged implementation; E1 only."
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - ".github/agents/luna-19.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/README.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-architecture-acceptance-ACP-0004.md"
  tests_added: []
  tests_passing:
    - "Starting revision verified as 80b7989ec5b7f5913362e812eddcc3d845b826c4."
    - "Architecture state and authorization boundaries reviewed."
  tests_failed: []
  tests_not_run:
    - "Runtime, neuron, E1, M, IR-2, backend, approximation and hardware tests - not run or unauthorized."
  assumptions:
    - "Project-owner acceptance is represented by this authorized Luna-0 decision."
    - "Luna-19 will return for independent verification before any promotion."
  unresolved:
    - "Empirical E1 implementation evidence."
    - "Future M, IR-2 and backend contracts."
  recommended_next_agent:
    - "Luna-19 for E1 implementation, followed by independent Luna-0 verification."
```

## Decision

**PASS - ACP-0004 ACCEPTED FOR STAGED IMPLEMENTATION; E1/LUNA-19 AUTHORIZED
BUT NOT EXECUTED.**

The revised contract closes the canonical blockers identified in the prior
review. It defines a finite event-driven transition system, exact amplitude
and discharge rules, local timing, cancellation, identity, provenance and
bounded execution semantics.

## Required final report

1. **Starting revision:** `80b7989ec5b7f5913362e812eddcc3d845b826c4`.
2. **Final publication revision:** the commit containing this acceptance
   handoff; uncommitted at handoff creation.
3. **ACP-0004 status:** Accepted for staged implementation.
4. **Mode/state table:** `N`, `S_PENDING`, `S_RETURN`, `M_ACTIVE`; M has
   `ARMED` and `REFRACTORY` phases.
5. **Persistent state:** bounded signed `x`, local last-update timestamp and
   explicit mode.
6. **Bookkeeping:** pending kind/time, ordinary and multi episode IDs,
   captured/current polarity, `m_peak`, M phase, lineage, provenance,
   truncation flag, generation and finite counters.
7. **Threshold ordering:** `0 < theta_R < theta_E <= theta_hold <
   theta_M <= X_max`; `lambda > 0`; all delays and bounds finite.
8. **S admission:** post-update `theta_E <= |x| < theta_M` from N enters
   `S_PENDING`; admission allocates identity, captures polarity and schedules
   `S_EMIT`.
9. **S emission timing:** `S_EMIT` occurs at admission time plus fixed
   positive finite `Delta_t_E`.
10. **Equal-time rule:** destination-local external arrivals retain sequence
    order and execute before due internal events.
11. **Polarity:** ordinary polarity is captured at S admission; M polarity is
    selected from current `sign(x)` at M emission.
12. **Amplitude:** `A_min + (A_max-A_min) * clip((m_peak-theta_E) /
    (theta_M-theta_E), 0, 1)`, with `m_peak` initialized and updated during
    S_PENDING.
13. **S input policy:** update decay, accumulation, provenance and `m_peak`;
    remain pending below M; promote to M at/above M and cancel S emission.
14. **S re-arm:** after emission, analytic `S_REARM` reaches `theta_R`;
    `|x| <= theta_R` enters N; no second ordinary excursion precedes N.
15. **M entry:** `|x| >= theta_M` from N or S promotion enters M_ACTIVE.
16. **M timing machine:** ARMED -> `M_EMIT` -> REFRACTORY -> `M_REARM` ->
    ARMED, with fixed positive finite delays.
17. **M payload:** `sign(x_emit) * A_max`.
18. **M discharge:** `q_after = max(theta_hold, |x|-Delta_x_E)` and
    `x = sign(x) * q_after`.
19. **Finite-return bound:** zero when `q_0 <= theta_hold`, otherwise
    `N_M <= ceil((q_0-theta_hold)/Delta_x_E)`, followed by at most one final S
    excursion and finite S_REARM.
20. **M sign reversal:** opposite input may reverse x while above hold; future
    M emissions use current sign; emitted events are immutable.
21. **Cancellation:** internal records carry neuron, episode, generation,
    kind, timestamp and sequence; generation invalidation makes stale records
    deterministic no-ops.
22. **Pending-event bound:** at most one valid internal event per neuron;
    stale queue records remain bounded by queue/event capacity.
23. **Provenance:** `1 <= P <= 64`; oldest contributor eviction sets
    `provenance_truncated`; complete attribution is not claimed afterward.
24. **Identity:** each excursion/event has unique non-negative identity,
    source, timestamp, payload, type and bounded episode/lineage.
25. **Prediction/error:** accumulator changes are local evidence; predictions
    and explicit prediction errors use causal excursion/event paths.
26. **Model-B:** `a_i := p_exc`, the signed excursion payload; ACP-0002 N2
    transfer remains unchanged.
27. **Legacy mode:** named, trace-labelled compatibility mode only; not a
    second unlabeled canonical neuron behavior.
28. **TPCN-IR-2:** required future schema; IR-1 rejects excursion records;
    IR-2 is not implemented here.
29. **Fixtures:** deterministic compression/leakage, boundaries, M,
    polarity, return input, cancellation, stale generation, provenance,
    replay and batching fixtures are specified in ACP-0004.
30. **A01-A15:** preserved; A01-A04, A06-A08, A09-A11 and A15 are made
    executable; A05 remains reservoir-free; A12-A13 optional; A14 inactive.
31. **ACP-0003 H2:** unauthorized.
32. **ACP-0002 N3:** unauthorized.
33. **Luna-19:** created and authorized for E1, not executed.
34. **Luna-13F:** CLOSED.
35. **Luna-13G:** unauthorized.

## E1 boundary

Luna-19 may implement only the static leaky accumulator and single-excursion
reference: `N`, `S_PENDING`, `S_RETURN`, ordinary amplitude, fixed internal
events, cancellation/generation, one-event cardinality, provenance bounds and
the declared fixtures. It must not implement `M_ACTIVE`, learning, IR-2,
ACP-0002 N3, any backend, approximation, calibration or H2.

## Validation record

| Command or procedure | Revision / environment | Result |
|---|---|---|
| `git rev-parse HEAD` | `80b7989ec5b7f5913362e812eddcc3d845b826c4` | pass |
| Architecture source review | local repository | pass |
| Runtime tests | documentation-only change | not run |
| Backend/hardware/H2/IR-2 checks | unauthorized or not applicable | not run |
| `git diff --check` | final documentation revision | required before commit |
