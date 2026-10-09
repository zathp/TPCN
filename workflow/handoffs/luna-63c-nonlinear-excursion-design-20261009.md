# Luna-63C — nonlinear excursion design handoff

```yaml
tpcn_handoff:
  agent: "Luna-63C Nonlinear Excursion Neuron Design Prerequisite"
  luna_identifier: "Luna-63C"
  descriptive_name: "Bounded stable-focus excursion design"
  task_id: "luna-63c-nonlinear-excursion-design-20261009"
  component: "Documentation-only local excursion candidate and future protocol"
  status: "documentation correction to be published in this handoff's containing commit; parent remote verification and independent re-review pending"
  contract_version: "1.2"
  branch: "experiment/luna63c-nonlinear-excursion-design"
  base_revision: "d006e1bc6ff09627df8fe7f6c1213380b953291f"
  result_revision: "a1a7d377a0f48af750fbfe6da62fe54179bf833b (design-content publication)"
  correction_status: "correction will be published in this handoff's containing commit; parent push/fetch equality and clean-status verification pending"
  dependencies:
    - "Owner attachment 0db88cfc-a144-4171-a155-fea721c1bbe9"
    - "Luna-63C committed contract at the stated baseline"
    - "Current architecture, ACP-0008, governance and runtime sources pinned in the design report"
  owner: "Project owner"
  classification: ["DESIGN ONLY", "HYPOTHESIZED", "NO EXPERIMENT"]
  hypothesis: "A stable focus with one oriented threshold section can release a bounded stored displacement into one event and return without RECALL acting as excitation."
  counter_hypothesis: "The analytic field, threshold margins, gate semantics, bounded quiet reset, or event-time conversion fail independent review."
  interfaces_relied_on:
    - "Proposed local signed stored state and binary RECALL gate only"
    - "Current finite event queue and canonical ExcursionEmission shape as inspected references, not integrated APIs"
  label_information_boundary:
    - "No task label, evaluator truth, sequence identity, answer buffer, 63B equation/result, or unpublished/raw 63A artifact is an input."
  timing_assumptions:
    - "Normalized local time; active time advances only while R=1"
    - "Event roots are local scheduled events; no global neural timestep"
    - "Count/audit addressed inputs first; attempts 1–16 continue through timestamp validation; the 17th is the single bounded overflow record, aborts before timestamp validation/settlement, and closes episode ingress"
    - "Reserve timestamp-admissible external pair without installing it; settle due old-gate internal records first, including same-time boundaries, then install the external pair before semantic validation"
    - "Malformed, late, out-of-domain, or unorderable timestamps are rejected without model-time or ordering-key advance; timestamp-admissible packets install the key after settlement even if later semantically rejected"
    - "A unified monotone destination ordinal places same-time internal boundaries before external records; internal boundary precedence and external delivery ordinals break ties within their respective classes; expiry equality preempts a semantically invalid packet"
    - "Quiet-at-entry is atomically committed by STORE with mode READY and retained QUIET_ENTRY reason"
    - "RESET commits terminal_reason=ABORTED before READY; new STORE resets terminal_reason to NONE"
    - "Crossing/re-arm/quiet/expiry times require certified upward-rounded binary64 boundaries; nonrepresentable ordering fails closed"
    - "Exact mathematical root state is distinct from the converted canonical event timestamp"
  reset_boundaries:
    - "STORE starts one bounded episode"
    - "A STORE with A<=q atomically commits QUIET_ENTRY and remains READY"
    - "RESET records ABORTED as its terminal reason; a later STORE starts a fresh reason"
    - "Attempt 17 atomically commits REJECTED_CAP_OVERFLOW, aborts generation, clears uncommitted state/tokens, retains ABORTED and any committed output, then enters READY and closes episode ingress"
    - "Quiet threshold or absolute expiry clears the two coordinates and invalidates episode generation"
    - "No new store until quiet or expiry"
  resource_bounds:
    - "Two continuous coordinates in the invariant disk x^2+y^2<=16"
    - "One output maximum per episode; at most eight recall records"
    - "At most 16 within-budget input attempts plus one addressed cap-overflow attempt, 24 created timer records, and one committed output: 42 unique records maximum"
    - "At most 128 bisections per root and 1024-bit precision in the proposed future interval bounds; caps fail closed and do not certify results"
    - "Finite absolute episode lifetime T_life=2+T_q+1 TU"
  authorized_scope:
    - "Compare required candidate families"
    - "Specify at most one bounded candidate and unexecuted C0-C7 protocol"
    - "Write only the Luna-63C design report and this handoff"
  unauthorized_scope:
    - "Production/runtime code, tests, ACPs, contracts, workflow/changelog/indexes, artifacts, Luna-63A, Luna-63B"
    - "Any solver run, simulation, trajectory, trial, training, task-efficacy or hardware execution"
    - "Integrated sequence echo, architecture promotion, ACP adoption, or Luna-64"
  controls:
    - "Neutral no-RECALL and neutral + RECALL"
    - "Subthreshold state held/released"
    - "Supra-threshold state held without output and released for one event"
    - "Unequal HOLD duration, ungated reference, duplicate cue, expiry equality with timestamp-admissible semantically invalid payload, malformed/late/out-of-domain timestamp without settlement, 17th-attempt overflow/post-abort ingress, and representable-future timing"
  measurements:
    - "No observed scientific measurements"
    - "Only hand-derived eigenvalues, Lyapunov derivative, threshold peak, and radius/expiry bounds"
  information_boundary_check:
    - "Candidate uses only local bounded stored displacement and gate; no evaluator or label inputs"
    - "No 63B state/result or unpublished/raw 63A material used"
  hardware_mapping:
    - "Qualitative two-register/linear arithmetic/FSM FPGA mapping"
    - "Qualitative coupled-integrator/comparator/switch analog mapping"
    - "No feasibility, performance, or equivalence evidence"
  architecture_invariants_touched: ["A01-A15 assessed; none amended"]
  preserves:
    - "A06 prediction/error and A07 locality as separate core obligations"
    - "No claim of A09-A11 learning, energy/utility, or delayed credit"
    - "ACP-0008 and E1/E2 canonical/default semantics unchanged"
    - "Luna-62 remains proposed and ACP-required"
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_63C_NONLINEAR_EXCURSION_DESIGN.md"
    - "workflow/handoffs/luna-63c-nonlinear-excursion-design-20261009.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All tests, candidate implementation, numerical oracle, solver, simulation, trajectory, trial, training, task efficacy, and hardware checks"
  assumptions:
    - "The proposed local stored displacement can be supplied by a separately authorized future fixture or local source; no upstream WEMA coupling is specified here."
    - "The selected stable-focus flow plus hybrid event conversion satisfies the design-only candidate boundary; independent Luna-0 review must decide."
  unresolved:
    - "Correction will be published in this handoff's containing commit; parent remote push/fetch equality and clean-status verification remain pending"
    - "Independent Luna-0 review of the corrected revision remains pending"
    - "Any future implementation and mechanism execution require separate authorization and a frozen platform/oracle"
    - "FPGA/analog/FPAA realization is qualitative only"
  recommended_next_agent:
    - "Independent Luna-0 review of the corrected report and handoff after parent remote verification"
```

## Outcome and owned scope

**HYPOTHESIZED:** the design report specifies one candidate: a signed,
two-coordinate stable-focus flow, gated by binary RECALL, with a derived
section threshold, one-event latch, hysteretic re-arm, finite quiet reset,
and bounded absolute episode lifetime. The field is mathematically linear;
the proposed neuron is hybrid-nonlinear at its threshold/lifecycle boundary.
The report explicitly limits the claim to the one-excursion mechanism.

**Changed:** only the two owner-authorized Markdown deliverables listed in
the YAML. **Unchanged:** production code, tests, artifacts, ACPs, architecture
contract/changelog, workflow, Luna-63A and Luna-63B. The prior design content was published at `a1a7d377a0f48af750fbfe6da62fe54179bf833b`. The current documentation-only correction will be published in this handoff's containing commit, whose SHA is intentionally not self-referenced. Parent remote push/fetch equality and clean-status verification, followed by independent Luna-0 review, remain pending; neither is claimed complete. No workflow index update is authorized here.

No scientific quantity was measured. The equations and analytic derivations are proposals; no solver, simulation, trajectory, or executable oracle was run. The earlier published content received an independent Luna-0 **BLOCKED** verdict with four corrections: (1) entry-region and lifecycle/reset completeness; (2) exact event precedence and record budgets; (3) root/tangency/direction/timestamp certification; and (4) representable absolute-time ordering, including below-one-ULP and C5 semantics. This report correction, to be published in this handoff's containing commit, addresses those findings without changing the field, thresholds, or fixtures. The exact baseline, contract
blob, required source pins, inspected ranges, owner-attachment read extents,
and derivation provenance appear in Section 8 of the design report.

## Architecture evidence

The design report's A01–A15 table (Section 7) preserves each contract clause.
In particular, A06 prediction/error and A07 locality remain separate core
obligations; this candidate implements neither learning nor prediction/error
propagation. A09–A11 energy, utility and delayed credit are explicitly not
claimed. A08 is addressed only as a proposed experiment through an invariant
disk, event/solver budgets and finite expiry.

The proposal is an isolated departure from ACP-0008, not an extension of its
accepted semantics. It does not change ACP-0008, E1/E2, canonical defaults,
or any A01–A15 clause. It supplies no spatial reservoir, evaluator input,
answer buffer or label-conditioned state. Luna-62 remains **PROPOSED — ACP
REQUIRED**; no alternative is adopted.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Read-only baseline, branch and clean-status check | `d006e1bc6ff09627df8fe7f6c1213380b953291f`; assigned Windows worktree | PASS; exact branch and clean baseline observed before edits | Current Git metadata |
| Read owner request in sections | Attachment `0db88cfc-a144-4171-a155-fea721c1bbe9`, 927 lines; sections 1–240, 241–480, 481–720, 721–927 | PASS; all lines read | Read-only attachment |
| Hand analysis of fixed point, eigenvalues, Lyapunov derivative and first-lobe crossing | Proposed exact equations only | Not independently reviewed; no numerical execution | Design report §§3–5 and derivation provenance |
| Original publication validation | Published design revision `a1a7d377a0f48af750fbfe6da62fe54179bf833b` | Historical baseline validation only; not evidence about this correction | Parent publication record |
| Follow-up correction validation | Two authorized Markdown paths prepared for this handoff's containing commit | PASS local `git diff --check`; exactly the two authorized paths; parent push/fetch equality and clean-status verification pending | Parent verification required |
| Candidate code/tests/solver/trajectory/trial/training/hardware | Not applicable; prohibited | **NOT RUN** | No artifacts created |

No self-review is offered. Parent remote publication/fetch equality verification remains pending. A separate Luna-0 re-review of the corrected, parent-published revision also remains pending.

## Benchmark and resource results

Not applicable: no benchmark, dataset, classification, prediction, energy,
utility, topology, latency, event-count measurement, or resource profiling
was performed. Candidate state/event/solver limits are prospective design
bounds, not measured resource results.

## Assumptions, limitations and unresolved issues

1. A future mechanism fixture may initialize or locally load a signed bounded
   stored state. This report does not claim that current software exposes
   this input or that an upstream PCN produces it.
2. The selected stable focus is globally stable, but output emission still
   depends on the proposed oriented section, state amplitude, hybrid event
   conversion and strict-future scheduler. None exists as a current integrated
   API.
3. Root, tangency, event-order and binary64 timestamp claims require independent review. State error tolerance is not a root/time certificate; unresolved interval signs, ceilings, or boundary order must fail closed.
4. The current event queue has its own deterministic tie semantics; the
   proposed expiry precheck is a component-specific experimental rule and
   does not amend that queue.
5. Qualitative FPGA/analog mappings are not evidence of feasibility or
   equivalence. All analog tolerance/noise and hardware budget questions
   remain open.
6. No current or future claim of recall, sequence memory, task efficacy,
   learning, ACP acceptance, core/default promotion, integrated echo, or
   Luna-64 follows from this design.

## Reproduction and rollback

There is no experiment to reproduce. The hand derivations can be independently reconstructed from the exact equations and formulas in the report; no code, trajectory, test output, or scientific artifact exists. Per episode, 16 input attempts are within budget and one additional addressed overflow attempt is recorded before abort; it commits its rejection before clearing uncommitted state/tokens, retaining `ABORTED` and any committed output, and entering `READY`; later ingress is not component-addressed. Together with 24 timer records and one output, this bounds unique records at 42. Timestamp-admissible external pairs are reserved, due internal boundaries settle first (including same-time boundaries ordered before externals by a unified monotone destination ordinal), and the external key is installed afterward even when semantic validation rejects the packet. Malformed, late, out-of-domain, or unorderable timestamps do not advance the key or trigger settlement. The prior design-content publication is `a1a7d377a0f48af750fbfe6da62fe54179bf833b`; the correction will be published in this handoff's containing commit without a self-referenced SHA. Parent push/fetch equality and clean-status verification, followed by independent Luna-0 re-review, remain pending. Roll back only the two authorized Luna-63C documentation paths if needed, preserving unrelated worktree state.

## Next assignment

**Parent push/fetch equality and clean-status verification, then independent Luna-0 re-review** of the corrected report/handoff. The prior design-content publication is `a1a7d377a0f48af750fbfe6da62fe54179bf833b`; the correction will be published in this handoff's containing commit, whose SHA is intentionally not self-referenced. Neither remote verification nor the re-review outcome is claimed here. The re-review should verify the corrected lifecycle/cap-overflow and event-order rules, equations/stability, ACP boundary, and no-execution record. Any mechanism run requires separate owner/Luna-0 authorization.
