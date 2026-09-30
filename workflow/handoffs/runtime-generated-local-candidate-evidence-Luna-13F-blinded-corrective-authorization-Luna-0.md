---
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-13F blinded-mapping corrective authorization"
  descriptive_name: "Authorize one corrective Luna-13F pass under the existing contract"
  task_id: "runtime-generated-local-candidate-evidence-Luna-13F-blinded-corrective-authorization"
  component: "Luna-13F experiment authorization boundary"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "dcee582fa8fb347f578793c2ef383bd936e83234"
  result_revision: "documentation publication pending"
  dependencies:
    - "Independent Luna-0 review: BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION"
    - "Existing .github/agents/luna-13f.agent.md contract"
    - "Luna-13B, Luna-13C, corrected Luna-13D and Luna-13E review records"
  owner: "Luna-13F corrective execution, returning to Luna-0"
  classification: ["AUTHORIZATION", "EXPERIMENT", "VERIFICATION", "CPU-only"]
  hypothesis: "After utility-independent candidate/topology blinding, bounded runtime evidence may or may not predict the held-out task-preserving candidate."
  counter_hypothesis: "Evidence follows endpoint or motif assignment without utility prediction, or another oracle dependency remains."
  interfaces_relied_on: ["TemporalAssociationPolicy", "TPCNNeuron", "CandidateEvidence", "StructuralPlasticityController", "execute_bounded", "Luna-13E evaluator"]
  label_information_boundary: ["Held-out labels and utility classifications are post-admission only; they must not construct candidates, schedules, evidence or scores."]
  timing_assumptions: ["Neutral mapping and schedule are frozen before held-out evaluation; evidence freeze precedes scoring/admission; held-out timestamps are later in actual runtime chronology."]
  reset_boundaries: ["Candidate evidence, live state, future-event exclusion and candidate-capacity reset/eviction must be documented and tested."]
  resource_bounds: ["Finite event/queue/history/candidate/topology/fan-in/fan-out budgets", "exactly one relevant free structural slot"]
  authorized_scope: ["One corrective Luna-13F pass under the existing agent contract", "neutral candidate_A/candidate_B representation", "seeded/predeclared permutation and mandatory controls", "focused tests, artifacts and handoff"]
  unauthorized_scope: ["New Luna-13F contract", "Luna-13G", "architecture semantics", "utility memory, oracle, reward channel, probation, rollback, abstention, unbounded history or production redesign"]
  controls:
    - "Two blinded candidate/endpoint mappings with identical schedule-generation rules"
    - "No-evidence, shuffled, reversed, uniform, neutral/zero-decay where applicable"
    - "Relabeling, mirrored motif, genuine equalization, candidate-order reversal"
    - "Future mutation/exclusion, label mutation, locality, budget boundaries, deterministic and increased-budget replay"
    - "Candidate saturation/reset/eviction and complete audit matrix"
  measurements: ["Neutral mapping seed and endpoints", "runtime event provenance", "bounded evidence and canonical scores", "admission and chronology", "post-hoc held-out utility", "events, queue/resource proxy and preservation counts"]
  information_boundary_check: ["Current blocker is experiment-level oracle mapping; no architecture change is authorized unless the blinded pass proves existing mechanisms insufficient."]
  hardware_mapping: ["CPU-only; CUDA optional and non-gating; no hardware equivalence claim"]
  architecture_invariants_touched: ["A01", "A02", "A04", "A07", "A08", "A14", "A15"]
  preserves: ["Runtime-generated bounded association mechanism", "unchanged canonical scorer", "Luna-13E/13D/13C/13B and Stage-0 behavior", "Luna-13G unauthorized"]
  architecture_change: false
  proposal: null
  files_changed: ["workflow/docs/luna/LUNA_WORKFLOW.md", "workflow/ARCHITECTURE_CHANGELOG.md", "workflow/handoffs/runtime-generated-local-candidate-evidence-Luna-13F-blinded-corrective-authorization-Luna-0.md"]
  tests_added: []
  tests_passing: ["Authorization provenance inspection", "Existing review evidence inspection"]
  tests_failed: []
  tests_not_run: ["Corrective Luna-13F experiment and all execution tests: explicitly not run", "Diagnostics and full validation: owned by corrective execution", "Luna-13G: not created or authorized"]
  assumptions: ["The existing Luna-13F contract remains authoritative and the implementation pass will return to Luna-0."]
  unresolved: ["Whether blinded evidence predicts utility remains unknown until the authorized corrective execution."]
  recommended_next_agent: ["Luna-13F corrective execution under the existing contract", "Luna-0 independent review of its completed artifacts"]
---

## Authorization Outcome

**PASS — LUNA-13F BLINDED-MAPPING CORRECTIVE PASS AUTHORIZED**

This authorizes exactly one additional corrective Luna-13F pass under the
existing `.github/agents/luna-13f.agent.md` contract. It does not create a new
contract, execute the experiment, alter A01-A15, or authorize Luna-13G.

## Remaining blocker

The current implementation has real bounded runtime association evidence, but
`beneficial_role -> candidate/topology assignment -> G` remains an oracle
mapping. The corrective pass must remove `beneficial_role` and
`harmful_role` from all pre-evaluation candidate, topology, schedule, ordering,
evidence and scoring paths. Those names may appear only in post-hoc reporting.

## Required blinded protocol

Use neutral `candidate_A` and `candidate_B` identities, freeze endpoints,
topology, event schedule and capacity before held-out evaluation, and record a
predeclared seeded permutation. Run at least two endpoint/motif mappings with
the same schedule-generation rule. Compute runtime evidence and canonical
scores before any held-out task classification. Preserve the valid event to
bounded association state to score chain and report whether the 4.0/0.0 result
is count-, interval-, ordering-, decay- or other-state-driven.

## Five outstanding audit controls

The following exact audit entries remain **REQUIRED BUT MISSING** and must be
executed unless the authoritative contract independently proves conditional
inapplicability:

1. `external_label_mutation`: labels must not alter pre-admission computation or decision.
2. `locality_attack`: candidate evidence must use only permitted local information.
3. `neutral_decay_runtime_sweep`: run a valid neutral/zero-decay control where runtime decay is applicable.
4. `candidate_saturation_reset_eviction`: verify bounded candidate lifecycle, reset and eviction behavior.
5. `valid_mirrored_roles`: mirror the runtime motif without utility-informed endpoint assignment.

No missing mandatory control may be relabeled `not applicable` merely because
the current count scorer does not use that field.

## Terminal and publication boundary

The corrective execution must use only statuses authorized by the existing
contract, regenerate all four required artifacts, run focused/preservation/full
CPU/compile/diagnostic/diff checks, and return to Luna-0. A positive result is
not presumed. If blinding still reveals oracle dependence, remain blocked; if
runtime mechanisms are insufficient, stop with the authorized architecture-
change status and decision packet. Luna-13G remains unauthorized.
