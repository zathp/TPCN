# Luna-0 Handoff — Luna-65 Phase 2A Contract Correction

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-65 Phase 2A direct-counter specification correction"
  task_id: "luna65-phase2a-contract-correction-20261012"
  component: "Direct E2 identity capacity fixture contract"
  status: "ready_to_publish"
  contract_version: "1.1-correction-proposal"
  specification_verdict: "PASS — PHASE 2A SPECIFICATION CORRECTED; EXECUTION STILL GATED"
  execution_readiness: "BLOCKED — no exact supervisor has been independently qualified"
  owner_acceptance: "pending"
  correction_publication: "pending; current governance correction is uncommitted"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "dc62469a099f27f2b8d43142dd8aecb407b2e663"
  result_revision: "uncommitted governance correction; exact-allowlist precommit review passed"
  dependencies:
    - "Baseline-published Luna-65 Phase 2 capacity supplement; owner acceptance remains pending"
    - "Prior blocked Luna-65 Phase 2A authorization-readiness review"
  owner: "repository owner"
  classification:
    - "governance-only"
    - "direct-neuron capacity fixture specification"
  hypothesis: "Source-derived checkpoints, a versioned probe ledger, and a bounded external evidence plan can make Phase 2A independently implementable without production changes."
  counter_hypothesis: "A source-derived assertion, schema element, command boundary, or resource term remains ambiguous or unsupported."
  interfaces_relied_on:
    - "MultiExcursionNeuron.receive_contribution()"
    - "MultiExcursionNeuron.process_pending()"
    - "MultiExcursionNeuron.reset()"
    - "neuron_to_ir2_e2() public serializer"
  authorized_scope:
    - "Read-only source inspection."
    - "Governance contract, workflow, and handoff correction."
    - "Independent review of exact governance bytes and precommit allowlist."
  unauthorized_scope:
    - "Fixture implementation or execution."
    - "Supervisor implementation, qualification, or execution."
    - "Production code changes."
    - "Phase 2B network fixtures."
    - "Spiral/Simon Says data generation, training, evaluation, scoring, or scientific runs."
    - "Luna-64 corrective work or Luna-63C changes."
  controls:
    - "Phase 2A execution remains NOT AUTHORIZED."
    - "Phase 2B execution remains NOT AUTHORIZED."
    - "Full Spiral benchmark execution remains BLOCKED."
    - "No Phase 2A replay-equivalence claim; the specification defines one deterministic run."
    - "The 8,196 cap counts target-counter probes only, not coupled secondary increments."
    - "Resource limits are proposed controls until an exact supervisor is independently qualified."
  resource_bounds:
    - "Wall time: 120 seconds."
    - "Aggregate job CPU: 120 seconds."
    - "Aggregate concurrent private commit charge: 268,435,456 bytes."
    - "Combined retained artifacts: 1,048,576 bytes."
    - "Retries: zero."
  measurements:
    - "No fixture, test, benchmark, dataset, training, or scoring command was run."
    - "No evidence directory or artifact was created."
    - "No supervisor was qualified."
  architecture_change: false
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2_CAPACITY.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-luna65-phase2a-contract-correction-20261012.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "Phase 2A direct-neuron capacity fixture."
    - "Phase 2B network capacity fixture."
    - "All benchmarks, training, scoring, and dataset generation."
  unresolved:
    - "Publication has not occurred."
    - "No exact Phase 2 supervisor identity or qualification evidence is available."
    - "Complete compressed-ledger size has not been measured; the fixture contract requires fail-closed incomplete status if its artifact cap would be exceeded."
    - "Repository owner has not accepted the proposed capacity-only amendment."
    - "Full-replication identity sufficiency remains unproven."
  recommended_next_agent:
    - "Luna-0: publish only if all independent specification reviews and the exact-byte precommit review pass."
    - "Repository owner: after publication, separately accept the capacity-only amendment and authorize Phase 2A only after supervisor qualification."
```

## Baseline and preserved evidence

The expected branch and checkout were verified as
`governance/luna64-r4.3-freeze-20261010` at
`dc62469a099f27f2b8d43142dd8aecb407b2e663`, with a clean worktree before
this correction. The published Phase 2 contract SHA-256 was
`FE47995A1E52A93BF485D446CE2D50629C788CEFFADC7847D8F1062659BC0A17`;
the authoritative Luna-65 Spiral contract hash was
`1F1D4DD96E21EE760D32CDDE4F0415576C9BAE6AF01B82DB2A9C4E1D9FB5C777`.
The Phase 1 closure and prior Phase 2 handoff identities were also verified
at this checkout. The Phase 1 record continues to report an unqualified
supervisor; no Luna-64 qualification evidence is borrowed. Frozen Luna-63C
and blocked Luna-64 governance paths are not modified.

The prior authorization-readiness review returned
**BLOCKED — EXECUTION PREREQUISITES INCOMPLETE**. Its direct-counter review
found no production defect, but identified missing fixed output input IDs and
checkpoint oracle, undefined direct-neuron snapshot/ledger units, and an
ambiguous “API/direct-neuron” phrase. Independent governance review also
identified that the Phase 2A scope and Phase 2B command needed to be explicit
before their respective authorizations. The resource review found no
qualified exact supervisor, no selected memory measurement semantics, and no
specified external evidence destination.

## Correction summary

The contract now defines:

- Four fresh zero-state neurons, one per counter, the exact contribution and
  event-ID sequences, each coupled counter high-water, and exact typed
  exhaustion strings and guard order.
- The output-event input IDs, one external INPUT at timestamp `0.0` per
  character, the alternating M_EMIT/M_REARM schedule, event counts, identity
  ranges, reset positions, and expected state after the character-4
  2,049th-output rejection.
- A recurrence oracle for every output magnitude, derived from source
  event-time decay and discharge order without executing the fixture.
- Versioned `luna65-phase2a-probe-v1` JSONL fields, target-versus-coupled
  counter deltas, deterministic counter ordering, existing public
  `neuron_to_ir2_e2()` snapshots, and an explicit statement that this is one
  deterministic run, not a replay-equivalence test.
- Exact test path and invocation, literal expected absolute working directory
  `C:\Users\Patrick\Documents\ActiveCode\TPCN`,
  Windows `.venv` environment, zero retries, and explicit prohibitions on
  API, Phase 2B, benchmark, training, scoring, and production-code paths.
- External evidence destination under `%LOCALAPPDATA%`, file names,
  combined retained-byte accounting, fail-closed behavior near the cap, and
  hash/manifest requirements.
- The unchanged proposed limits, with memory defined as maximum aggregate
  concurrent private commit charge. The control mechanism remains unselected
  and unqualified.

The amendment does not change neural behavior, Spiral conditions, the
Phase 2B authorization boundary, Luna-64 authorization, or frozen Luna-63C
evidence. It remains a proposal; the repository owner has not accepted it.

## Independent review ledger

| Review area | Disposition |
|---|---|
| Counter and output-event semantics | PASS; rejection checkpoints and output schedule are source-consistent. |
| JSONL schema and provenance | PASS; fields, ordering, serializer mapping, and fail-closed artifact semantics are specified. |
| Exact command and fixture boundaries | PASS; command, absolute cwd, environment, 8,196-probe bound, and exclusions are explicit. |
| Resource policy and scientific isolation | PASS for proposed specification only; supervisor qualification is absent and execution remains blocked. |

Reviewers are restricted to read-only examination. No reviewer is asked to
run a fixture, test, or supervisor qualification.

## Validation, publication, and gates

Source-derived values were inspected from `tpcn/excursion_neuron.py` and the
public serializer in `tpcn/ir2.py`. No runtime value, fixture outcome, or
cross-platform exact floating-point result was observed. The recurrence
specifies expected binary64 operations in source order; the fixture must
record actual binary64 values without rounding and fail rather than tune if
the frozen schedule does not meet its stated inequalities/checkpoints.

Independent specification review returned
**PASS — PHASE 2A SPECIFICATION CORRECTED; EXECUTION STILL GATED**. No fixture,
test, benchmark, dataset, training, or scoring command was run. No evidence
directory was created. Resource limits remain proposed, not demonstrated;
complete compressed-ledger size remains unverified. Phase 2A and Phase 2B
execution remain **NOT AUTHORIZED**. Full Spiral execution remains
**BLOCKED** pending a reviewed full-replication capacity argument,
separately qualified controls, and exact owner authorization.

The exact governance allowlist and staged bytes passed independent precommit
review with no findings. Commit and publish only these reviewed bytes;
publication is not owner acceptance or execution authorization.
