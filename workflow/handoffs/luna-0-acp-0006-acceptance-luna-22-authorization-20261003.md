# Luna-0 Acceptance and Dispatch Handoff — ACP-0006 / Luna-22

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "ACP-0006 owner acceptance and Luna-22 dispatch-readiness review"
  task_id: "luna-0-acp-0006-acceptance-luna-22-authorization-20261003"
  component: "First CPU software-reference excursion integration"
  status: "complete; ACP-0006 accepted; Luna-22 authorized and not executed"
  contract_version: "1.1"
  branch: "main"
  base_revision: "7eb997ebcb78f5a64074cd27a7a6181dbf693fa3"
  result_revision: "acceptance publication commit; exact SHA recorded after commit"
  dependencies:
    - "ACP-0002 N2 static Model-B edge transfer, closed"
    - "ACP-0003 H1 Execution IR/backend interface, closed"
    - "ACP-0004 E1/E2 excursion runtime, closed"
    - "ACP-0005 TPCN-IR-2 revision 1/E2 reconstruction, closed"
    - "Luna-21 corrective implementation independently verified and closed"
  owner: "Project owner"
  classification: ["OWNER ACCEPTANCE RECORDING", "FINAL ARCHITECTURE DISPATCH REVIEW", "SUCCESSOR CONTRACT CREATION / AUTHORIZATION"]
  hypothesis: "The accepted ACP-0006 network-level integration can be implemented as a bounded CPU experiment-path composition using existing closed component interfaces, without new canonical interpretation."
  counter_hypothesis: "An accepted integration boundary is contradictory or a required behavior cannot be implemented without additional canonical decisions, so first integration dispatch must remain blocked."
  interfaces_relied_on:
    - "_ComputationalNetwork / ExperimentRunner"
    - "TPCNNeuron legacy experiment path"
    - "MultiExcursionNeuron / ExcursionEmission / PendingInternalEvent"
    - "EventQueue / bounded event execution"
    - "BoundedTopology Model-B signal and opaque control routing"
    - "LocalPredictor / Prediction / PredictionError"
    - "EligibilityLedger / EligibilityActivity / RewardSignal"
    - "StreamingCharacterClassifier"
    - "LocalEnergyModel activity-cost-proxy"
    - "IR-2 E1/E2 reconstruction adapters"
    - "StrokeStreamEncoder / DatasetMetadata protocol"
  label_information_boundary:
    - "Labels remain external until post-readout evaluation, outer reward and prototype update."
    - "Prediction observation is the next actually admitted numeric contribution at its configured input port."
    - "No future point, held-out test label or global evaluation statistic may enter neural computation."
  timing_assumptions:
    - "Logical timestamps are monotonic; no global neural timestep or wall-clock settling."
    - "At next external time t, queued work strictly earlier than t runs first; all currently available external inputs at t are admitted before eligible work through t."
    - "Destination-local external-before-internal ordering and positive finite edge delays remain unchanged."
    - "END_CHARACTER uses finite declared horizon and finite event budget."
  reset_boundaries:
    - "Character reset occurs after settle/readout and applicable label-authorized outer reward."
    - "Character queue and sidecar are destroyed, neuron-local episodes and character-local predictor/ledger/error/readout state are cleared."
    - "E2 event, episode, lineage and input identity high-water counters remain monotonic across character reset."
    - "Experiment/model reset creates a fresh network/topology/readout namespace."
  resource_bounds:
    - "Finite per-character queue, execution/settling budgets and configured predictor/readout bounds."
    - "Existing E2 event and provenance capacities; causal-root sidecar bound follows provenance capacity with sticky truncation."
    - "Finite route path/depth and per-character prediction-error delivery guard."
    - "Finite activity-cost-proxy counters/totals."
  authorized_scope:
    - "Record explicit owner acceptance of ACP-0006 as written at proposal revision 7eb997ebcb78f5a64074cd27a7a6181dbf693fa3."
    - "Create .github/agents/luna-22.agent.md for bounded first CPU reference integration."
    - "Record accepted status and Luna-22 AUTHORIZED / NOT EXECUTED in workflow and changelog."
    - "Publish this handoff and stop before executing Luna-22."
  unauthorized_scope:
    - "Executing Luna-22 in this task."
    - "Modifying production implementation in this governance task."
    - "Changing A01-A15 text or reopening ACP-0002 N2, ACP-0003 H1, ACP-0004 E1/E2, ACP-0005/IR-2 revision 1, Luna-19, Luna-20 or Luna-21."
    - "ACP-0002 N3, ACP-0003 H2, IR-3, structural/edge learning, prediction/reward/eligibility redesign, GPU/FPGA/FPAA, backend approximation, hardware equivalence or calibration."
  controls:
    - "Network-wide explicitly selected TANH_LEGACY compatibility/replay control."
    - "Network-wide EXCURSION_V1 backed by E2-capable runtime."
    - "Equivalent ordered stream, fixed topology/Model-B, timestamps, declared budgets, resets and label boundary; no numerical-equality requirement."
  measurements:
    - "Repository branch, synchronization, clean-state, accepted proposal revision, Luna-number inventory and runtime-interface compatibility."
    - "Dispatch blocker analysis for every specifically named ACP-0006 boundary."
  information_boundary_check:
    - "Source contracts keep labels and future points out of neural events, predictor observations, topology and local learning."
  hardware_mapping:
    - "None; CPU software-reference integration only, with no hardware equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "A01-A15 text."
    - "ACP-0002 N2, ACP-0003 H1, ACP-0004 E1/E2, ACP-0005 schema revision 1 and Luna-21 closures."
    - "Luna-17 RESERVED / NOT AUTHORIZED / NO ACTIVE CONTRACT."
    - "Fixed topology and structural-plasticity-off first integration."
  architecture_change: true
  proposal: "ACP-0006, Accepted by project owner on 2026-10-03"
  files_changed:
    - "workflow/docs/architecture_proposals/ACP-0006.md"
    - ".github/agents/luna-22.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-acp-0006-acceptance-luna-22-authorization-20261003.md"
  files_reviewed:
    - "workflow/ARCHITECTURE_CONTRACT.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/docs/architecture/ACCEPTANCE_CRITERIA.md"
    - "workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md"
    - "workflow/docs/architecture_proposals/README.md"
    - "workflow/docs/architecture_proposals/ACP-0002.md"
    - "workflow/docs/architecture_proposals/ACP-0003.md"
    - "workflow/docs/architecture_proposals/ACP-0004.md"
    - "workflow/docs/architecture_proposals/ACP-0005.md"
    - "workflow/docs/architecture_proposals/ACP-0006.md"
    - "workflow/handoffs/luna-0-post-e2-integration-dependency-review-20261003.md"
    - "workflow/handoffs/luna-0-architecture-decision-ACP-0006-20261003.md"
    - "workflow/handoffs/luna-0-independent-corrective-review-ACP-0004-E2-Luna-21-20261003.md"
    - "tpcn/experiments.py"
    - "tpcn/canonical_neuron.py"
    - "tpcn/excursion_neuron.py"
    - "tpcn/event_runtime.py"
    - "tpcn/topology.py"
    - "tpcn/predictive_coding.py"
    - "tpcn/eligibility.py"
    - "tpcn/streaming_classifier.py"
    - "tpcn/energy_utility.py"
    - "tpcn/ir2.py"
    - "tpcn/stroke_dataset.py"
    - ".github/agents/luna-19.agent.md"
    - ".github/agents/luna-20.agent.md"
    - ".github/agents/luna-21.agent.md"
    - "tests/test_stroke_dataset.py"
  tests_added: []
  tests_passing:
    - "Fetched origin/main; branch main; HEAD == origin/main == accepted starting revision; worktree was clean before edits."
    - "Repository numbering inventory found no Luna-22 contract or active parallel assignment; see numbering evidence."
    - "Focused source/governance review found no dispatch-blocking contradiction; see readiness analysis."
    - "`git diff --check`: PASS."
  tests_failed: []
  tests_not_run:
    - "All runtime tests and integration tests; Luna-22 has not executed."
    - "Sequential classification dataset run; none was executed during governance."
    - "All hardware/backend and energy-calibration checks."
  assumptions:
    - "Owner direction in the received task is an explicit project-owner acceptance under the ACP proposal lifecycle."
    - "ACP-0006 is accepted in full at its published proposal revision; status/decision metadata updates do not revise its numbered behavioral clauses."
    - "Dataset selection remains open under the accepted repository sequential classification protocol and is delegated to the bounded implementation report."
  unresolved:
    - "Luna-22 must select and document a suitable permitted dataset/split and report whether it can run."
    - "Any implementation evidence, test status, actual integration readiness and task efficacy remain unknown until Luna-22 and subsequent Luna-0 review."
  recommended_next_agent:
    - "Luna-22: execute the accepted first CPU integration strictly within .github/agents/luna-22.agent.md; return complete handoff to Luna-0."
    - "Luna-0: independently review Luna-22 implementation and evidence; do not infer pass from authorization."
```

## Synchronization and explicit owner decision

**OBSERVED:** `git fetch origin` completed. The current task started on branch
`main` with a clean worktree and
`HEAD == origin/main == 7eb997ebcb78f5a64074cd27a7a6181dbf693fa3`,
subject `Propose ACP-0006 excursion integration contract`. No newer commit
was present, so the accepted proposal had not been superseded.

**OWNER DECISION:** The project owner explicitly instructed: **ACCEPT
ACP-0006 AS WRITTEN**, applying to all 17 numbered integration boundaries.
The accepted text is the full ACP-0006 published at revision
`7eb997ebcb78f5a64074cd27a7a6181dbf693fa3`. Acceptance date is
2026-10-03. The acceptance record changes status/decision metadata and does
not reinterpret or selectively omit accepted clauses.

## Final dispatch-readiness review

The governing A01-A15 contract, ACP-0002 through ACP-0006, acceptance
criteria, workflow, proposal policy and relevant implementation surfaces
were read at the synchronized baseline.

| Boundary reviewed | Dispatch finding |
|---|---|
| Prediction target and matching | ACP-0006 names the configured numeric input port/schema and the next actually admitted contribution; `LocalPredictor` already supports bounded target-key/FIFO matching, finite timestamps and expiry. Event payload comes from `e.payload`, not `TPCNNeuron.activation`. Implementable without changing prediction arithmetic. |
| Prediction-error delivery | `PredictionError` is complete metadata. `BoundedTopology.route()` already transforms only numeric `signal`/`excursion` events and preserves opaque control payloads and delay. A per-character bounded prediction/destination guard prevents convergence duplicates. The neuron never receives the error as a numeric E2 contribution. |
| Eligibility trace ownership | A canonical excursion event ID is namespaced and stable; the accepted rule uses it as the local trace ID and links only its own prediction ID. Existing ledger accepts bounded timestamped activity and later error/reward signals. Silent state updates create no trace. |
| Reward targeting | ACP-0006 targets the first actual readout-source excursion trace in deterministic order and explicitly reports unmatched if none exists. Existing `RewardSignal` supports trace IDs and idempotent message IDs. No reward formula or multi-trace allocation needs invention. |
| Readout aggregation | Two distinct existing surfaces are specified: the streaming classifier consumes every actual ordered `ACTIVITY_EVENT`; the outer prototype path uses bounded signed-payload sum/count mean, or `0.0` with no events. The current runner selects the learned prototype when trained prototypes exist and otherwise uses the classifier result. This is existing behavior, not a new architecture rule. |
| Settling | Horizon and event budget are declared finite configuration values; inclusive deadline, incomplete status, pending work and beyond-deadline discards are explicit. No numeric global timing constant is imposed. |
| Queue and route sidecar | `EventQueue` is finite and exposes timestamp-ordered `peek`/`pop_ready`; an integration-owned scheduler can gate processing on each newly admitted input timestamp. Sidecar state can be one bounded record per queue sequence, with fixed node/path bounds. No future input is pre-enqueued. |
| Causal roots | ACP-0006 explicitly merges active-episode roots within provenance capacity and makes truncation sticky/observable. Internal work inherits roots; each emission starts a distinct route path. Queue sequence, event ID, episode and lineage remain separate. |
| Event ordering and E2 cancellation | Existing queue policy is destination-local external-before-internal. E2 external updates can cancel/reschedule a pending S or M event before its due time. A persistent character queue can implement the required `t0 < t1 < t2` admission fixture. |
| Energy proxy | `LocalEnergyModel` already supports finite saturating counters and activity-cost-proxy units. ACP-0006 enumerates event, amplitude, edge and error components; no calibrated-energy claim is needed. |
| IR-2 startup | ACP-0005 excludes shared live-network scheduler/predictor/ledger/readout state. ACP-0006 restricts integration to quiescent clean startup with empty queue/sidecar and fresh outer state. The integration builder can reject unsupported live resume without changing IR-2. |
| Structural / hardware boundary | Fixed topology and structural plasticity off; N3, H2, IR-3, backends, calibration and hardware equivalence remain excluded. |

**INFERRED:** No numbered ACP-0006 clause conflicts with another or requires
Luna-0 to invent a new canonical choice before implementation. Numeric
capacity/horizon values, dataset selection and experiment configuration are
declared and reported implementation parameters; the architecture already
specifies their finite bounds and required behavior. Dataset selection is
open in the workflow protocol, so Luna-22 must identify version, permitted
use, classes and splits, use train-only or causal preprocessing, and report a
data availability blocker rather than claim the sequential-classification
gate passed on synthetic data alone.

**DISPATCH DECISION:** PASS — ACP-0006 is internally dispatchable. Create and
authorize Luna-22 for the CPU software-reference experiment-path integration
only. This decision is not evidence that code exists, tests pass, the dataset
benchmark passes, integration is complete or task efficacy is established.

## Luna numbering evidence

**OBSERVED:** `.github/agents/` has existing numbered contracts through
Luna-21. The active assignment table records Luna-17 as
`RESERVED / NOT AUTHORIZED / NO ACTIVE CONTRACT`; Luna-18 is closed H1,
Luna-19 is closed E1, Luna-20 is closed IR-2 and Luna-21 is closed E2.
Search of `.github/agents/`, `workflow/docs/luna/LUNA_WORKFLOW.md` and
`workflow/handoffs/` found no Luna-22 contract, creation authorization or
active parallel Luna-22 assignment. Older historical text saying no Luna-22
or ACP-0006 existed predates the published proposal and is not a current
reservation. **Luna-22 is the next legitimate unused numbered role.**

## Authorized scope and controls

The authoritative implementation scope is
`.github/agents/luna-22.agent.md`: modify the experiment path and focused
tests only; use the closed component APIs; create a narrowly scoped runtime
adapter only if needed; do not redesign components. Any underlying component
API blocker returns to Luna-0 before such a file is changed.

The contract requires:

- network-wide E2-capable `EXCURSION_V1` production selection, explicit
  network-wide `TANH_LEGACY` control and mixed-model rejection;
- one bounded queue per character and the input watermark:
  process times `< t`, admit all currently available external inputs at `t`,
  then process eligible work through `t`;
- mandatory `t0` external / `t2` internal / `t1` external fixture, with
  `t0 < t1 < t2`, observed order `t0, t1, t2`, and `t1` able to alter,
  cancel or reschedule due internal work;
- emission-only routing with `a_i = e.payload` and unchanged Model-B:
  `z_ij = tanh(w_ij * a_i)`,
  `v_ij = d_ij * z_ij + (1 - d_ij) * r_ij`;
- bounded distinct queue/causal-root/path/excursion/episode/lineage metadata;
- event-centric prediction, opaque explicit prediction-error propagation,
  emission-based eligibility, accepted reward attribution, event-based
  classifier input and bounded prototype mean;
- finite END settling and explicit incomplete/pending results; E2-safe
  character reset with monotonic identity high-water counters;
- quiescent IR-2 startup only; activity-cost-proxy accounting; fixed topology,
  structural plasticity off; no label/future-point leakage.

Controls must use equivalent ordered streams, fixed topology/Model-B,
timestamps, declared budgets, resets, label boundary and readout protocol
where applicable; no numerical or accuracy equality is required.

Focused test names and the adversarial cases (overflow, exhausted budget,
late/multiple same-time inputs, canceled stale E2 work, silence, multiple M
emissions, incomplete settle, model mixing and unsupported IR-2 live resume)
are listed in the Luna-22 contract. It also requires regressions for
`test_experiments.py`, `test_excursion_neuron.py`,
`test_e2_multi_excursion.py`, `test_event_runtime.py`, `test_topology.py`,
`test_predictive_coding.py`, `test_eligibility.py`,
`test_streaming_classifier.py`, `test_energy_utility.py`, `test_ir2.py`,
`test_e2_ir2.py`, `test_stroke_dataset.py`, and the full CPU suite.

The sequential benchmark must identify an actual dataset/version/permitted
use/classes/native format/split and writer-disjoint status where available.
It reports classification and per-class results, prediction loss and
matched/unmatched/expired counts, delayed-credit attribution, processed
events, queue peak, pending/incomplete settling, excursion/silence/readout
coverage, proxy units and deterministic replay. No accuracy threshold is
added.

## STOP boundary

This handoff creates and authorizes Luna-22 only. **Luna-22 has not been
executed in this task.** After publishing this acceptance, workflow/changelog
updates, contract and handoff, stop. The next action is a separate Luna-22
execution turn, followed by independent Luna-0 review; authorization is not
execution or integration readiness.
