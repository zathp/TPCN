# Luna-0 Authorization — Luna-28 EXCURSION_V1 Local Temporal Growth

**AUTHORIZED — IMPLEMENTATION + VERIFICATION ONLY; NOT EXECUTED.**

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  luna_identifier: "Luna-0 authorization for Luna-28"
  descriptive_name: "Bounded E2 local temporal observation and growth"
  task_id: luna-0-authorization-luna-28-excursion-local-temporal-growth-20261004
  component: "EXCURSION_V1 optional local temporal structural growth"
  status: complete
  contract_version: "1.2"
  branch: main
  base_revision: 2e692337d339704eebf5b9d060409be25804be8e
  result_revision: "this handoff's authorization publication commit"
  dependencies:
    - "Accepted ACP-0007"
    - "Luna-0 owner-decision handoff"
    - "ACP-0006 CPU EXCURSION_V1 integration"
    - "Closed structural controller and TemporalAssociationPolicy contracts"
  owner: "Luna-0"
  classification: ["IMPLEMENTATION", "VERIFICATION", "EXPERIMENT", "INTEGRATION"]
  hypothesis: "Actual local E2 emission chronology can produce bounded candidate evidence whose admitted edge causally affects a later real E2 route."
  counter_hypothesis: "No legal local candidate can be admitted and causally used under the declared finite capacity and quiescent lifecycle."
  interfaces_relied_on:
    - "ExperimentConfig and ExperimentRunner"
    - "ExcursionCharacterRuntime._consume_emission() and end_character()"
    - "ExcursionEmission identity and timestamp"
    - "TemporalAssociationPolicy and CandidateEvidence"
    - "StructuralPlasticityController"
    - "BoundedTopology"
    - "TPCV-2 downstream capture"
  label_information_boundary:
    - "Structural score cannot use labels, payload magnitude, loss, reward, readout, correctness, accuracy, energy, global metrics, or future/held-out values."
  timing_assumptions:
    - "E2 local timestamps; only 0 < t_neighbor - t_source <= association_window counts."
    - "One admission attempt only after complete successful quiescent character teardown."
    - "No global neural timestep."
  reset_boundaries:
    - "Evidence/candidates/rejections reset and are consumed each character."
    - "Topology persists between characters within an experiment."
    - "Experiment reset creates a new model/topology namespace."
  resource_bounds:
    - "Explicit finite static-neighborhood and reverse-observer limits."
    - "Explicit finite history and per-source candidate capacity; saturating score."
    - "Finite configured positive edge delay and finite experiment growth-attempt budget."
    - "At most one attempt/edge per completed character; no pruning."
  authorized_scope:
    - "Implement/verify the accepted opt-in `e2_local_temporal` CPU experiment."
    - "Use only the exact owned files in `.github/agents/luna-28.agent.md`."
    - "Add the focused acceptance module and completion handoff."
  unauthorized_scope:
    - "All files outside the Luna-28 agent contract."
    - "Pruning, N3, core neuron/topology/controller changes, prediction/reward/readout changes, IR-2 changes, visualization changes, downstream migrations, GPU/FPGA work, hardware equivalence, and efficacy claims."
  controls:
    - "Fixed-topology E2 with structural flags disabled."
    - "Observation enabled with mutation disabled."
    - "Label and future-suffix non-interference."
    - "Capture on/off structural-decision equality."
  measurements:
    - "Actual evidence chronology, candidate score/rank/rejection, admission, topology, budget use, later routed event trace/depth, and edge-transfer proxy."
  information_boundary_check:
    - "Observation adapter accepts only actual emission ID, emitter node ID, and timestamp."
  hardware_mapping:
    - "No hardware implementation or equivalence is authorized or claimed."
  architecture_invariants_touched: ["A01", "A03", "A04", "A07", "A08", "A14", "A15"]
  preserves:
    - "Fixed-topology E2 default"
    - "TANH_LEGACY explicit compatibility behavior"
    - "ACP-0006 neuron, prediction, error, reward, and IR-2 semantics"
    - "Luna-13F negative efficacy/resource status"
    - "Luna-12E legacy observable failure classification"
  architecture_change: false
  proposal: "Accepted ACP-0007; no further architecture change authorized"
  files_changed:
    - ".github/agents/luna-28.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-28-excursion-local-temporal-growth-20261004.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All implementation and acceptance tests; Luna-28 has not started."
    - "Downstream structural assertions after the intentional guard."
    - "Hardware/GPU equivalence."
  assumptions:
    - "The authorization publication commit is the required clean implementation-start baseline; Luna-28 must record its exact SHA and stop if main is not clean/current."
  unresolved:
    - "Whether growth improves any task or resource metric; efficacy is outside this authorization."
  recommended_next_agent:
    - "Luna-28 implementation/verification"
    - "Luna-0 independent review after Luna-28 handoff"
```

## Baseline and authority

The readiness review's verified baseline was clean `main` at
`2e692337d339704eebf5b9d060409be25804be8e`. This authorization is published
on that lineage. Luna-28 must start from clean `main` containing this
authorization and the accepted ACP-0007 publication, record the exact
implementation-start SHA, verify `HEAD == origin/main`, and stop if either
condition fails or a conflicting architecture decision appears.

Read the contract version 1.2, ACP-0007, architecture changelog, acceptance
criteria, Luna workflow, handoff template, owner-decision handoff, readiness
handoff, and `.github/agents/luna-28.agent.md` before implementation. The
agent contract is normative for exact file ownership, API semantics,
acceptance tests, regressions, and stop conditions.

## Authorized objective

Implement the separately selected CPU EXCURSION_V1 structural-observation
and growth-only path under accepted ACP-0007. Structural observation and
mutation remain explicitly disabled by default; observation-only mode must
prove non-interference. E2 growth requires explicit `e2_local_temporal`
selection and explicit finite local observation and mutation bounds. The
fixed-topology E2 path remains available and is the required matched control.

The required causal result is an admitted edge, selected only from frozen
source-local actual-emission temporal evidence, followed by a later real E2
excursion routed over that edge with the configured positive delay. Graph
existence alone does not pass. Mechanism validity is separate from task
efficacy: no accuracy, prediction loss, reward, or resource improvement is
required or implied.

## Mandatory exclusions and preservation

Keep the two previously classified Luna-12E failures distinct: topology
changes already caused observable routed activity, while the old
`prediction_loss must change` assertion was unchanged; exact post-evaluation
clock assumptions conflict with the E2 settle/reset lifecycle. Do not use
either legacy assertion as evidence that local growth does or does not work.
Likewise, retain the prior 19 guard-only structural downstream failures as
unresolved after-guard behavior; no claim that they pass is permitted.

Do not widen ownership or repair unrelated downstream consumers. Any need to
modify a prohibited core, topology/controller, prediction, reward, IR-2, or
visualization module returns to Luna-0 as a blocker. No successor is
authorized.

## Required completion and sequence

Luna-28 must record exact revision/tree, actual commands and test outcomes,
all resource bounds, deterministic candidate/admission evidence, later routed
trace, non-interference controls, relevant component regressions, limitations,
and passed/failed/not-run/not-applicable states in its completion handoff.
No result may be claimed without execution evidence. The sequence is:

```text
Luna-0 owner decision -> Luna-0 authorization
-> Luna-28 implementation/verification -> Luna-0 independent review
```

This publication does not create or execute Luna-28 work. At the point of
authorization, implementation and acceptance tests are **NOT RUN**.
