# Luna-0 Independent Architecture Review: ACP-0004

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent ACP-0004 attractor excursion architecture review"
  task_id: "luna-0-architecture-review-ACP-0004"
  component: "Canonical excursion neuron semantics"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "c1c7a4948b7e96908da8d2334687d238d6949379"
  reviewed_proposal_revision: "c18757739f4055bbb5721520a14382701e177d64"
  result_revision: "uncommitted documentation review"
  dependencies:
    - "A01-A15 architecture contract"
    - "ACP-0002 N2 CLOSED"
    - "ACP-0003 accepted for staged implementation"
    - "ACP-0003 H1 independently verified and CLOSED"
  owner: "Luna-0 Architecture Guardian / project owner for acceptance"
  classification: ["VERIFICATION", "ARCHITECTURE-PROMOTION"]
  hypothesis: "The proposal can define a bounded, hardware-neutral excursion state machine without backend-specific interpretation."
  counter_hypothesis: "A required state, transition, timing, identity or finite-bound rule remains ambiguous or contradicts an existing canonical interface."
  interfaces_relied_on:
    - "ACP-0002 N2 Model-B edge transfer"
    - "TPCN-IR-1"
    - "ACP-0003 backend separation"
    - "A01-A15"
  label_information_boundary:
    - "No labels, future inputs, global evaluation state or global orchestration state may enter canonical neuron state."
  timing_assumptions:
    - "Local elapsed-time analytic decay remains canonical."
    - "External and internal events require finite logical timestamps and deterministic sequence ordering."
    - "A backend clock cannot become a global neural timestep."
  reset_boundaries:
    - "No hard reset is accepted as an unspecified substitute for ordinary return."
    - "A return episode must explicitly reach N and re-arm before another ordinary excursion."
  resource_bounds:
    - "x, amplitude, mode/phase, provenance, lineage, pending internal events and event budgets are finite."
  authorized_scope:
    - "Review and amend ACP-0004 documentation."
    - "Clarify ACP-0003 terminology and workflow status."
    - "Record acceptance blockers and the smallest possible future implementation stage."
  unauthorized_scope:
    - "Production neuron or learning implementation"
    - "TPCN-IR-2 implementation"
    - "ACP-0003 H2 or any backend/approximation/calibration work"
    - "ACP-0002 N3, Luna-19, Luna-13F reopening or Luna-13G"
  controls:
    - "One canonical excursion to one canonical digital event for GPU/software/FPGA reference semantics."
    - "Separate x-domain hold thresholds from h-domain oscillator hysteresis."
    - "Saturating positive discharge toward zero."
    - "Explicit provenance truncation rather than complete-credit claims after eviction."
  measurements:
    - "No runtime, benchmark, energy or hardware measurements; this is an architecture review."
  information_boundary_check:
    - "The reviewed contract preserves local state and bounded causal provenance only."
  hardware_mapping:
    - "Digital event is the GPU/software/FPGA realization; physical spike/analog excursion is FPAA realization."
    - "No backend-specific clock, voltage, register or scheduling detail is canonical."
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
    - "ACP-0002 N2 and canonical Model-B transfer"
    - "TPCN-IR-1 H1 closure and scope"
    - "ACP-0003 H2 unauthorized"
    - "ACP-0002 N3 unauthorized"
    - "Luna-13F CLOSED"
    - "Luna-13G unauthorized"
  architecture_change: true
  proposal: "ACP-0004 remains Draft; acceptance is blocked by missing canonical semantics."
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/docs/architecture_proposals/ACP-0003.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-architecture-review-ACP-0004.md"
  tests_added: []
  tests_passing:
    - "Repository state and proposal revision inspection completed."
    - "Documentation references and status consistency reviewed."
  tests_failed: []
  tests_not_run:
    - "Runtime, neuron, IR-2, GPU, FPGA, FPAA, calibration and hardware-equivalence checks — not applicable or unauthorized."
  assumptions:
    - "The project owner retains the acceptance decision."
    - "The one-to-one digital cardinality and saturating discharge are review requirements, not implementation evidence."
  unresolved:
    - "Exact internal-event transition table and cancellation/rescheduling."
    - "Complete input-during-return policy and multi-excursion generator table."
    - "Final amplitude function and IR-2 schema."
  recommended_next_agent:
    - "Project owner/Luna-0 to request a revised ACP-0004; only then consider a bounded E1 implementation role."
```

## Review outcome

**ACP-0004 REMAINS DRAFT — NOT ACCEPTED FOR STAGED IMPLEMENTATION.**

The reviewed proposal revision is
`c18757739f4055bbb5721520a14382701e177d64`. Its direction is compatible with
the architecture contract, but the canonical state machine, autonomous timing,
return rules and finite identity/provenance semantics were not sufficiently
specified to support implementation without backend-specific choices.

## Required itemized decisions

1. **Reviewed proposal revision:** `c18757739f4055bbb5721520a14382701e177d64`.
2. **ACP-0004 status:** remains Draft; no staged implementation acceptance.
3. **Terminology:** `canonical excursion` is the backend-neutral concept.
   `event` is the GPU/software/FPGA realization and `spike` is reserved for
   an FPAA physical realization or explicitly labelled legacy language.
4. **Cardinality:** one canonical excursion maps to exactly one canonical
   digital emission event for GPU/software/FPGA reference semantics. Multiple
   excursions map to multiple events. Any exception requires a new bounded
   identity contract.
5. **Persistent state:** signed bounded `x` and its local last-update
   timestamp. A persistent independent `y` is not required.
6. **Bounded bookkeeping:** mode, ordinary-return phase, generator
   armed/disarmed phase, pending excursion identity and captured polarity,
   amplitude, bounded provenance/lineage, truncation flag and a finite
   pending-internal-event set.
7. **Accumulator:** apply
   `x(t_k-) = x(t_(k-1)+) exp(-lambda * (t_k-t_(k-1)))`, then
   `x(t_k+) = clip[-X_max,X_max](x(t_k-) + v_ij(t_k))` sequentially.
   There is no global timestep.
8. **N/S/M boundaries:** `N` is `|x| < theta_E`; `S` is
   `theta_E <= |x| < theta_M`; `M` is `|x| >= theta_M`. Equality belongs
   exactly as shown.
9. **Entry semantics:** evaluate membership after each ordered accumulation or
   due internal transition. Active `S` does not emit repeatedly merely because
   later input remains in `S`; `S -> M` is allowed at the exact boundary.
10. **Ordinary re-arm:** after the single ordinary emission, no new ordinary
    excursion is eligible until the return completes in `N`. This prevents
    threshold chatter.
11. **Ordinary return:** one bounded trajectory begins from accumulated state,
    emits once, terminates finitely and converges to neutral without input.
    Exact geometry remains a blocker until specified as transitions rather
    than an optional lobe.
12. **Amplitude map:** `A_exc=f(|x_peak|)` must be deterministic, finite,
    bounded, monotone over its declared range and explicit about saturation.
    Sign is applied separately from a captured excursion polarity.
13. **Oscillator variables:** `h` is a bounded generator coordinate with
    `h_min <= h <= h_max` and `h_L < h_H`. It is not the accumulated state.
14. **`h_L` versus `theta_hold`:** direct comparison is rejected as
    dimensionally/semantically invalid. `theta_hold` independently satisfies
    `0 <= theta_hold < theta_M` in the x-domain.
15. **M entry/exit:** enter at `|x| >= theta_M`; remain active while
    `|x| > theta_hold`; exit at `|x| <= theta_hold` into `S` ordinary return,
    then `N`.
16. **Discharge:** use
    `x <- sign(x) * max(|x|-Delta_x_E,0)` with `Delta_x_E > 0` for the first
    stage. It cannot cross zero or reverse sign.
17. **Finite-return proof:** with no input, discharges are zero when
    `|x_0| <= theta_hold`, otherwise at most
    `ceil((|x_0|-theta_hold)/Delta_x_E)`, followed by finite ordinary return.
    This requires finite generator-cycle duration and explicit
    `|x_0|=theta_M`, `X_max`, negative and zero-crossing fixtures.
18. **Input during ordinary return:** input is locally decayed, accumulated,
    clipped and retained in `x`; it may promote `S -> M`. It must not
    retroactively change an emitted payload. The exact pending-emission
    amplitude/update table remains an acceptance blocker.
19. **Input during multi-excursion return:** input must not be dropped and must
    deterministically affect `x` and the remaining generator/discharge. Exact
    extension, rescheduling and opposite-sign rules remain an acceptance
    blocker.
20. **Sign/polarity:** the first-stage requirement is to capture polarity when
    an excursion is admitted. Later input cannot mutate that excursion's
    identity or payload; retained opposite-sign state is processed by a later
    episode.
21. **Logical timestamp:** emission occurs at a deterministic local return
    transition. The proposal must declare a positive finite delay and compute
    timestamp from the triggering event and local state.
22. **Autonomous events:** continuation without external input requires bounded
    internal neuron events at finite future logical timestamps, never a hidden
    timestep loop. Equal-time ordering and cancellation/rescheduling are
    missing blockers.
23. **Multi-excursion timing:** repeated emissions require a positive finite
    inter-excursion delay, deterministic ordering, a finite pending-event
    bound and defined update/cancellation behavior.
24. **Identity/lineage:** every digital emission has a unique non-negative
    identity/sequence and timestamp. One episode may share a bounded lineage
    identifier while each excursion remains distinct.
25. **Provenance:** declare finite capacity `P`; oldest-contributor eviction
    plus `provenance_truncated` is the required overflow policy. Complete
    attribution cannot be claimed after eviction.
26. **Predictive coding:** local accumulator changes remain internal evidence;
    predictions and explicit prediction errors remain event-driven and
    causally propagated, with bounded lineage/provenance.
27. **Model-B `a_i`:** after migration, `a_i` is the signed excursion payload
    `p_exc`; Model-B remains `tanh(w_ij*a_i)` followed by its existing divider
    and reference combination.
28. **Compatibility mode:** legacy continuous output may exist only as a
    named, trace-labelled comparison mode. It is not a second canonical
    output and must identify its Model-B source semantics.
29. **IR version:** excursion state, pending events, modes, payload and
    provenance require a new explicit schema, strongly expected to be
    `TPCN-IR-2`; IR-1 must reject rather than silently reconstruct it.
30. **ACP-0003 terminology:** clarified to use canonical excursion, one-event
    digital realization and FPAA physical realization. No H2 authorization.
31. **A01-A15 impact:** preserved. A01-A04, A06-A08, A09-A11 and A15 gain
    explicit review requirements; A05 remains reservoir-free; A12-A13 remain
    optional; A14 is not activated.
32. **Implementation staging:** if later accepted, start with E1: static
    accumulator and single-excursion return only. Multi-excursion, learning,
    approximation and IR-2 implementation remain separate gates.
33. **Luna-19:** not created, not authorized and not dispatched.
34. **H2:** ACP-0003 H2 remains unauthorized.
35. **ACP-0002 N3 / Luna-13F / Luna-13G:** ACP-0002 N3 remains unauthorized;
    Luna-13F remains CLOSED; Luna-13G remains unauthorized.

## Acceptance blockers

The proposal cannot advance until it specifies executable transition tables
for ordinary and multi-excursion return, all input-during-return cases,
positive finite autonomous timing, equal-time internal/external ordering,
cancellation/rescheduling, finite provenance overflow, amplitude saturation,
and the versioned IR migration. The required deterministic fixtures must
then be implemented and independently verified by an authorized assignment.

## Validation record

| Command or procedure | Revision / environment | Observed result | Evidence |
|---|---|---|---|
| `git rev-parse HEAD` | local repository | pass; `c1c7a4948b7e96908da8d2334687d238d6949379` | repository state |
| `git show c187577...` | committed proposal | pass; proposal and original handoff reviewed | proposal revision |
| Source/status/reference search | local workflow docs | pass; no Luna-19 or IR-2 implementation found | repository search |
| Runtime tests | unchanged production code | not run; documentation-only review | not applicable |
| GPU/FPGA/FPAA/H2 validation | current authorization state | not run; unauthorized/not applicable | governance boundary |
| `git diff --check` | review worktree | required after edits | pending final validation |

## Next assignment

The project owner should request a revised ACP-0004 that closes every listed
blocker. Only after acceptance should Luna-0 consider creating a narrowly
owned E1 implementation contract; independent verification must remain a
separate gate. No integration is ready.
