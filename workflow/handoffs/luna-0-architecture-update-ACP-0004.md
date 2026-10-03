# Luna-0 Architecture Update Handoff: ACP-0004

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Attractor excursion and event-compression neuron architecture update"
  task_id: "luna-0-architecture-update-ACP-0004"
  component: "Canonical neuron semantics"
  status: "complete"
  contract_version: "1.1"
  branch: "copilot/architecture-update-next-canonical-neuron-model"
  base_revision: "c1c7a4948b7e96908da8d2334687d238d6949379"
  result_revision: "uncommitted ACP-0004 draft"
  dependencies:
    - "ACP-0002 N2 CLOSED; canonical Model-B edge transfer active"
    - "ACP-0003 accepted; H1 independently verified and CLOSED"
  owner: "Luna-0 Architecture Guardian / project owner for acceptance"
  classification: ["ARCHITECTURE", "REVIEW"]
  hypothesis: "A bounded leaky accumulator with explicit single- and multi-excursion returns can compress signed delayed contributions while preserving causal timing, prediction/error compatibility, and finite termination."
  counter_hypothesis: "A scalar persistent accumulator plus bounded return metadata loses required temporal or predictive information, cannot terminate finitely, or cannot map truthfully to all supported hardware realizations."
  interfaces_relied_on:
    - "ACP-0002 N2 Model-B edge transfer"
    - "A01-A15 architecture contract"
    - "ACP-0003 TPCN-IR-1 and backend separation"
    - "local prediction/error and bounded delayed-credit interfaces"
  label_information_boundary:
    - "No task labels, future points or global orchestration state enter canonical neuron state or provenance."
  timing_assumptions:
    - "Local elapsed-time analytic decay; no global neural timestep."
    - "Finite positive edge delays and deterministic sequence ordering."
    - "Logical emission transition is canonical; FPAA peak/crossing time is observational."
  reset_boundaries:
    - "Neutral attractor is (x,y)=(0,0)."
    - "No hard reset is required after discharge; residual state returns through bounded ordinary return."
  resource_bounds:
    - "Finite x, phase, hysteresis, provenance, queue, lineage and event-budget bounds."
    - "theta_M > theta_E; h_L < h_H and h_L >= theta_hold."
  authorized_scope:
    - "Create and review ACP-0004 terminology and canonical semantic proposal."
    - "Record A01-A15 preservation, required fixtures, migration and rollback."
  unauthorized_scope:
    - "Production neuron implementation or learning implementation"
    - "ACP-0003 H2, GPU/FPGA/FPAA backends, calibration or hardware equivalence"
    - "ACP-0002 N3, edge learning, Luna-19 creation or implementation dispatch"
  controls:
    - "Canonical excursion terminology is separated from digital event and analog spike realization."
    - "Model-B edge transfer remains unchanged."
    - "Multi-excursion output requires explicit M-region entry and bounded discharge."
    - "Compatibility continuous mode is isolated from canonical emission semantics."
  measurements:
    - "No runtime measurements; proposal defines required future compression, bound and fixture metrics."
  information_boundary_check:
    - "Proposal retains only bounded causal provenance for delayed credit."
    - "No labels, future data, global statistics or backend physical timing become neural inputs."
  hardware_mapping:
    - "GPU/software: TPCN events; FPGA: bounded digital event/pulses; FPAA: analog spikes/excursions."
    - "No backend execution or equivalence claim is made."
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
    - "ACP-0002 N2 Model-B semantics and finite delayed routing"
    - "ACP-0003 H1 closure, IR-1 scope, and H2 unauthorized state"
    - "Luna-17 reserved/not authorized; Luna-13F CLOSED; Luna-13G unauthorized"
  architecture_change: true
  proposal: "ACP-0004 Draft — Attractor Excursion and Event-Compression Neuron"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/handoffs/luna-0-architecture-update-ACP-0004.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Repository revision verification: HEAD c1c7a4948b7e96908da8d2334687d238d6949379"
    - "Architecture source and proposal-number search: ACP-0004 was unused before this update"
  tests_failed: []
  tests_not_run:
    - "Neuron/runtime tests: not run; no production code was changed."
    - "GPU, FPGA, FPAA, H2, calibration and hardware-equivalence checks: unauthorized/not applicable."
  assumptions:
    - "The project owner will decide whether the proposed scalar-state model is sufficient."
    - "A future accepted proposal or implementation handoff will version any IR/schema extension explicitly."
  unresolved:
    - "Acceptance/rejection of ACP-0004."
    - "Parameter selection and empirical sufficiency of scalar x plus bounded return metadata."
    - "Whether a future implementation role is justified; Luna-19 is not created."
  recommended_next_agent:
    - "Project owner for ACP-0004 decision; if accepted, a separately authorized implementation role with independent verification."
```

## Outcome and owned scope

**OBSERVED:** the repository was at the expected baseline revision and contains
ACP-0001 through ACP-0003 but no ACP-0004 or Luna-19 contract.

**CHANGED:** ACP-0004 documents the proposed canonical excursion vocabulary,
minimal state, operating regions, hysteretic multi-excursion return, finite
termination argument, backend mapping, predictive/credit boundary, migration
and deterministic fixtures. This handoff records the review boundary.

**UNCHANGED:** no production neuron, learning rule, backend, edge transfer,
contract clause, ACP-0002 N3 authorization, ACP-0003 H2 authorization or Luna-19
dispatch was created.

## Architecture evidence

The proposal preserves A01-A04, A06-A11 and A15 directly, leaves optional
A12-A13 optional, and does not activate A14. It explicitly retains finite
propagation, local elapsed time, signed Model-B contributions, bounded state,
local predictive/error bookkeeping, delayed-credit provenance and truthful
hardware separation. The proposed change is a canonical semantic change, so it
remains Draft pending independent project-owner acceptance.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `git rev-parse HEAD` | local repository | pass; expected revision verified | `c1c7a4948b7e96908da8d2334687d238d6949379` |
| Search for ACP-0004/Luna-19 | baseline tree | pass; neither existed before edit | repository search |
| Runtime tests/build/lint | unchanged codebase | not run; no production code changed | not applicable |
| GPU/FPGA/FPAA/H2 validation | current authorization state | not run; unauthorized | not applicable |

## Benchmark and resource results

No dataset, seed, runtime, energy proxy, classification, prediction or
connectivity measurements were produced. ACP-0004 predeclares the required
compression, excursion-count, state-bound, finite-return and fixture metrics
for a future authorized implementation.

## Assumptions, limitations and unresolved issues

This is an architecture proposal, not evidence that the proposed dynamics work
in the reference runtime or on hardware. The scalar-state decision,
parameterization, schema migration and any implementation dispatch require a
separate decision. A proposal draft does not amend the contract.

## Reproduction and rollback

Review `workflow/docs/architecture_proposals/ACP-0004.md` at this revision.
Rollback to `c1c7a4948b7e96908da8d2334687d238d6949379` removes the draft files
and restores the prior architecture documentation; no runtime state migration
is required.

## Next assignment

Project owner/Luna-0 should accept, reject, or request revision of ACP-0004.
Only after acceptance should a bounded implementation and independent
verification assignment be considered. Luna-19 remains uncreated and
unauthorized.
