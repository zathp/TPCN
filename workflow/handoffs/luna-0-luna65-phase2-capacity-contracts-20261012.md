# Luna-0 Handoff — Luna-65 Phase 2 Capacity Contracts

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-65 Phase 2 capacity contract preparation and review"
  task_id: "luna65-phase2-capacity-contracts-20261012"
  component: "Persistent E2 identity capacity characterization"
  status: "complete"
  contract_version: "1.0-reviewed-proposal"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "5a374c9ddab30517d863696a28f7f801a31f26bc"
  result_revision: "governance-only publication; Git commit recorded in the final report"
  dependencies:
    - "Published Luna-65 Phase 1 closure"
    - "Separate owner authorization for each fixture lane"
  owner: "repository owner"
  classification:
    - "governance-only"
    - "bounded synthetic capacity fixture design"
  hypothesis: "Bounded fixtures can verify exact identity-boundary failure behavior and characterize a frozen network schedule without implying full-replication sufficiency."
  counter_hypothesis: "The fixture paths, counter ordering, resource bounds, or replay design are incomplete or cannot be executed within the frozen authorization limits."
  interfaces_relied_on:
    - "MultiExcursionNeuron.receive_contribution()"
    - "MultiExcursionNeuron.process_pending()"
    - "MultiExcursionNeuron.reset()"
    - "ExperimentRunner.execute_example()"
    - "neuron_to_ir2_e2() public identity serializer"
  label_information_boundary:
    - "No task or benchmark labels are used."
    - "The network fixture uses one fixed artificial evaluator token with neutral reward and readout updates disabled."
  timing_assumptions:
    - "Direct E2 defaults except the output-event fixture setting decay_rate=0.0001, m_emit_delay=0.001, m_rearm_delay=0.001, and delta_x_e=0.001."
    - "Network synthetic timestamps are fixed at 0.0 through 15.0."
  reset_boundaries:
    - "Direct fixtures reset character-local state while retaining all four E2 identity counters."
    - "Network fixtures reuse one runner, topology, and identity state per seed."
  resource_bounds:
    - "Each separately authorized test invocation: 120 s wall, 120 s aggregate job CPU, 256 MiB memory, 1 MiB retained artifacts, zero retries."
    - "Phase 1 resource observations do not qualify an execution supervisor."
  authorized_scope:
    - "Read-only source review."
    - "Drafting governance contracts and handoff."
  unauthorized_scope:
    - "Fixture implementation or materialization."
    - "Fixture/test execution."
    - "Benchmark data generation, training, scoring, or scientific runs."
    - "Production code changes."
    - "Luna-64 corrective work or Luna-63C changes."
  controls:
    - "Phase 2A and Phase 2B require distinct owner authorizations."
    - "The proposed supplement replaces prior capacity-fixture module/count terms only after explicit owner acceptance and publication; until then the published Luna-65 contract controls."
    - "Expected direct counter rejection is only at the declared 2,049th target-counter boundary probe."
    - "Any Phase 2B failure stops the entire lane; no retry or replacement fixture."
    - "The proposed Phase 2B c00 replay sentinel changes only the capacity diagnostic count and requires owner acceptance."
  measurements:
    - "Source-level identity check and increment sites were inspected."
    - "No runtime measurements or fixture outcomes were collected."
  information_boundary_check:
    - "No benchmark task labels, generated datasets, or training paths are included."
  hardware_mapping:
    - "Software reference only; no hardware-equivalence claim."
  architecture_invariants_touched: []
  preserves:
    - "Luna-65 Spiral scientific conditions and acceptance criteria."
    - "Luna-12G TANH_LEGACY historical result and artifacts."
    - "Frozen Luna-63C and blocked Luna-64 boundaries."
    - "No counter reset or capacity increase."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2_CAPACITY.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-luna65-phase2-capacity-contracts-20261012.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "Phase 2A direct-counter fixture."
    - "Phase 2B fixed-network fixture."
    - "All benchmarks, training, scoring, and dataset generation."
  assumptions:
    - "The current checkout remains at the published Phase 1 closure baseline until independently verified otherwise."
  unresolved:
    - "Phase 2A direct-counter replay equivalence is not established by one 8,196-probe run."
    - "The Phase 2B replay sentinel raises the prior diagnostic ceiling to 136 calls and requires owner acceptance."
    - "Phase 1 resource control observations do not qualify CPU, memory, process-tree termination, or strict emitted-output caps."
    - "Full-replication identity sufficiency remains unproven."
  recommended_next_agent:
    - "Repository owner: consider accepting and publishing the capacity-only amendment, then separately authorize Phase 2A and Phase 2B only after qualified resource controls."
    - "Luna-65: implement and execute only the specifically authorized fixture lane; do not execute Spiral without its separate full-capacity gate."
```

## Source evidence and outcome

The published baseline was recorded as
`5a374c9ddab30517d863696a28f7f801a31f26bc` on
`governance/luna64-r4.3-freeze-20261010`. The authoritative Luna-65 contract
SHA-256 was previously verified as
`1F1D4DD96E21EE760D32CDDE4F0415576C9BAE6AF01B82DB2A9C4E1D9FB5C777`.
This is a governance-only proposal; its publication does not authorize
fixture execution.

**OBSERVED:** `MultiExcursionNeuron` initializes all four persistent identity
counters at zero; `reset()` clears character-local state without resetting
those counters. Capacity is checked against `E1Config.event_budget` before
the respective identity increment. Ordinary admission checks episode before
lineage; a new M lineage checks lineage before episode. Ordinary and M
emission paths both check output-event capacity. The runner constructs E2
neurons with `event_budget=queue_capacity * 16`, yielding 2,048 under the
Luna-65 queue setting.

**INFERRED:** For direct input, ordinary episode, and new-lineage M
admission, a zero-state neuron can make 2,048 successful allocations across
reset boundaries and reject the next attempt on the documented guard.
Output-event identities require a multi-emission schedule spanning resets;
an individual character's event budget otherwise masks a naive 2,049th
emission attempt. The proposed delta and event accounting target that
interaction, but it has not been executed.

**HYPOTHESIZED:** The deterministic high-activation network schedule and
one replay sentinel will characterize whether those fixed inputs complete
under the configured identity bounds. It cannot establish full-replication
sufficiency.

The initial direct output-event recipe was rejected during independent review:
with default decay and delays, the M excursion transitions out of M mode long
before the proposed repeated-emission count. The revised draft proposes a low
positive decay, short positive delays, and a small discharge decrement, with
the exact per-character allocation of 1,023 + 1,023 + 2 output identities
before asserting rejection on the next character. This is a source-based
fixture design only and remains unexecuted; the revised output-event dynamics
received a read-only follow-up PASS.

The revised supplement expressly treats the split fixture modules and
136-call/139,264-event network ceiling as a proposed capacity-only
replacement for the prior one-module/128-call/131,072-event terms. Until
owner acceptance and publication of that amendment, the published
Luna-65 contract remains controlling.

An independent Phase 2B review identified specification gaps in exact label
handling, replay comparison, and observable counter continuity. The draft
now fixes every `SyntheticExample.label` to `capacity-neutral` and states
that it may appear only in evaluator-side diagnostic metadata, not event
inputs, routing, prototype updates, or reward. Replay digest and deterministic
per-example fields are required to match exactly, with no numeric tolerance;
identity snapshots instead must be monotonic for every node across calls on
the same runner. Input and topology digest record shapes and canonical JSON
serialization are specified for an external manifest, without requiring a
runner API change. These are design clarifications only.

## Independent review ledger

| Review dimension | Initial finding | Follow-up disposition |
|---|---|---|
| E2 counter paths and Phase 2A | BLOCKED: the original repeated-M-emission recipe did not sustain M mode; 8,196 was ambiguously described as total allocation attempts. | PASS after the recipe was revised to the bounded 1,023 + 1,023 + 2 M-emission schedule and the count was relabeled as target-counter boundary probes. |
| Phase 2B runner compatibility | BLOCKED: fixed label mapping, exact replay equality, and identity-counter continuity were insufficiently explicit. | PASS after fixing the evaluator token, exact result equality, per-call monotonic snapshots and stop-before-next-call at the capacity boundary; external canonical manifest fields were specified. |
| Resource/provenance boundaries | PASS. | Retained-file cap is distinguished from bytes emitted/read before termination; Phase 1 observations do not qualify Phase 2 enforcement. |
| Contract relationship and governance isolation | Initially BLOCKED: replacement of the original one-module/128-call/131,072-event capacity terms was not explicit. | PASS after stating the original Luna-65 capacity protocol controls until an owner accepts and publishes this capacity-only amendment. Spiral science remains unchanged. |
| Final prepublication allowlist review | BLOCKED on the initial exact-allowlist snapshot: handoff timing assumptions omitted three Phase 2A output-fixture settings; next-agent assignment was stale; final review verdict was not recorded. | PASS — GOVERNANCE PUBLICATION READY after correcting the handoff timing assumptions, next-agent assignment, review ledger, and validation status, and aligning the Phase 2A fixture-rules settings. |

These reviews were read-only. No test, fixture, benchmark, dataset, training,
scoring, or scientific workload was run. The final prepublication review
initially returned BLOCKED; all findings were corrected and the independent
final prepublication review returned **PASS — GOVERNANCE PUBLICATION READY**.

## Validation and publication status

No fixture was materialized. No test, benchmark, data generation, training,
or scoring command was run. No production source was changed. The independent
final prepublication review returned **PASS — GOVERNANCE PUBLICATION READY**
for the exact three-file governance allowlist. Raw SHA-256 identities and
the Git publication identity are reported with the final publication report.

The Phase 1 closure's supervisor evidence is not sufficient to claim hard
aggregate CPU/memory enforcement or a strict emitted-byte limit. Future
execution remains gated on an independent supervisor review and separate
owner authorizations for Phase 2A and Phase 2B. Full Spiral execution remains
blocked pending a reviewed full-replication capacity argument or another
owner-approved resolution.
