# Luna-0 — Luna-65 Windows Supervisor Qualification R1 Handoff

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-65 Windows Job Object supervisor qualification design"
  task_id: "L65-PHASE2-WINDOWS-SUPERVISOR-QUALIFICATION-R1"
  component: "Phase 2 resource supervision and evidence boundary"
  status: "blocked"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "61b034931f00095549c278c249e9379dd27e8893"
  result_revision: "uncommitted"
  dependencies:
    - "Luna-65 Phase 2 capacity contract and Phase 2A correction"
    - "Owner acceptance of capacity-only replacement for qualification design"
  owner: "Project owner"
  classification:
    - "governance-only"
    - "supervisor-design"
    - "no-execution"
  hypothesis: "Windows Job Objects alone do not demonstrate the accepted aggregate user-plus-kernel CPU and bounded termination requirements."
  counter_hypothesis: "A separately identified and independently qualified control may enforce the unchanged resource terms without weakening them."
  interfaces_relied_on:
    - "Phase 2A direct-neuron fixture command and resource terms"
    - "Phase 2B network-capacity diagnostic envelope"
    - "Windows Job Object process, accounting, memory, and termination APIs"
  label_information_boundary:
    - "No labels or benchmark inputs are used by this design."
    - "Spiral and Simon Says execution are prohibited."
  timing_assumptions:
    - "Proposed 120-second invocation deadline begins at supervisor main entry."
    - "A 15-second termination grace is only a candidate and requires owner approval."
    - "No finite Job Object termination-to-last-exit bound is claimed."
  reset_boundaries:
    - "No neuron, runner, dataset, or benchmark state was created or reset."
  resource_bounds:
    - "Protected Phase 2A profile: 120 seconds aggregate user-plus-kernel job CPU, 268435456 bytes aggregate concurrent private commit, 120 seconds wall, 1048576 retained bytes, zero retries."
    - "Proposed separate qualification profile: 12 cases once, 30 seconds observed aggregate job CPU, 360 seconds wall, 268435456 bytes job memory, 1048576 retained bytes, no network."
    - "Qualification CPU and wall ceilings are not demonstrated hard enforcement."
  authorized_scope:
    - "Read repository, contract, handoff, and source evidence."
    - "Research Windows API semantics."
    - "Draft bounded supervisor qualification design and governance records."
    - "Request independent read-only contract reviews."
  unauthorized_scope:
    - "Supervisor implementation or infrastructure changes."
    - "Qualification probes or Q01-Q12 execution."
    - "Phase 2A or Phase 2B fixture implementation or execution."
    - "Spiral or Simon Says data generation, training, evaluation, or scoring."
    - "Luna-64 corrective execution or changes to frozen Luna-63C evidence."
  controls:
    - "No Job Object API operation, qualification probe, test, fixture, or benchmark was run."
    - "The Phase 1 supervisor and Luna-64 qualification evidence are not borrowed."
    - "Capacity-only replacement acceptance is limited to qualification design."
  measurements:
    - "Baseline branch and HEAD verified; baseline worktree was clean."
    - "Phase 1 implementation/test SHA-256 identities match the published values."
    - "Windows host identified as Windows 10 Pro 22H2 build 19045.6466; no Job Object call was made."
    - "Phase 2A and Phase 2B fixture files and a Job Object supervisor implementation are absent from this checkout."
    - "R1 estimates are analytical only; no JSONL or compression sizing was generated."
  information_boundary_check:
    - "Design is capacity-only and does not change Spiral scientific conditions."
    - "No benchmark data, labels, or outputs were consumed."
  hardware_mapping:
    - "Windows-only execution-control design; no TPCN computation or hardware mapping changed."
  architecture_invariants_touched: []
  preserves:
    - "Luna-12G historical TANH_LEGACY results."
    - "Full-replication E2 capacity uncertainty."
    - "Luna-64 blocked status and Luna-63C frozen evidence."
    - "Separate Phase 2A and Phase 2B execution gates."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2_CAPACITY.md"
    - "workflow/docs/luna/LUNA_65_SUPERVISOR_QUALIFICATION_R1.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-luna65-windows-supervisor-qualification-r1-20261012.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All tests, fixtures, supervisor cases, probes, and benchmark workloads not run by authorization."
  assumptions:
    - "Owner acceptance dated 2026-10-12 permits qualification design only."
    - "Published Phase 2A requirements remain unchanged unless the owner explicitly amends them."
  unresolved:
    - "Hard aggregate user-plus-kernel CPU enforcement."
    - "Finite wall-time termination bound and approved grace semantics."
    - "Reconciliation of Job Object commit limits with aggregate concurrent PrivateUsage."
    - "Bounded workload-to-controller evidence channel or separately qualified storage quota."
    - "Byte-bounded deterministic JSONL schema, record-shape input for Q10, and compressed-ledger fit."
    - "Complete Phase 2A inherited-environment policy beyond PYTHONHASHSEED=0 and TPCN_LUNA65_EVIDENCE_DIR."
    - "Safe Q03 escaped-child recovery and independent process-observer qualification."
    - "Exact supervisor identity and independent qualification evidence."
  recommended_next_agent:
    - "Project owner: decide unresolved resource guarantees, evidence-channel/schema/environment terms, Q03 recovery, and observer protocol; no execution authorization is implied."
```

## Outcome and owned scope

At baseline `61b034931f00095549c278c249e9379dd27e8893` on
`governance/luna64-r4.3-freeze-20261010`, the owner accepted the Phase 2
capacity-only replacement for **qualification design only**. This handoff
records an R1 Windows Job Object supervisor design that remains
**BLOCKED — SUPERVISOR QUALIFICATION CONTRACT INCOMPLETE**. It authorizes no
implementation, qualification, fixture, benchmark, or resource-probe run.

The capacity amendment preserves the exact Phase 2A/2B boundaries and does
not alter the Spiral scientific protocol. Phase 2A remains the direct-neuron
fixture only, at most 8,196 target-counter probes and zero retries. Phase 2B
remains separate, at most 136 calls, 139,264 processed events, and 2,176
external inputs. Neither is authorized to execute.

## Architecture evidence

No A01-A15 clause or neural computation interface is changed. No ACP is
proposed. Job Object limits are execution controls, not TPCN neural
timesteps, architecture behavior, energy accounting, or hardware-equivalence
claims. Luna-12G remains a separate historical `TANH_LEGACY` result;
full-replication E2 capacity is unproven. Simon Says is source-recovery-only.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Git branch/HEAD/status inspection | `61b034931f00095549c278c249e9379dd27e8893`; Windows checkout | Expected branch/HEAD; clean before edits | Repository metadata |
| SHA-256 verification of Phase 1 implementation, runtime, test, and closure | Published Phase 1 identities | All four match | `Get-FileHash` results recorded in session |
| Phase 2A/2B fixture path and source scan | Current checkout | Fixture modules and Job Object source absent | Read-only path/source inspection |
| Windows host identity inspection | Windows 10 Pro 22H2, build 19045.6466 | Host identified; no Job Object API operation | Read-only environment query |
| `git -c core.whitespace=cr-at-eol diff --check` | Windows checkout with repository CRLF convention | Passed | Working-tree whitespace validation |
| Job Object qualification / Q01-Q12 | Not run | Not authorized | No artifacts |
| Phase 2A / Phase 2B / Spiral / Simon Says | Not run | Not authorized or blocked | No datasets or results |

## Benchmark and resource results

No benchmark was executed and there are no new scientific measurements.
Phase 1's published observations are historical and are not supervisor
qualification evidence. The R1 contract's ledger sizes and compression
ratios are analytical estimates, not generated-data measurements.

The key technical mismatch is that Job Object aggregate accounting exposes
user and kernel time but the documented hard job-time limit applies to
user-mode CPU only. The 120-second aggregate user-plus-kernel ceiling is not
therefore demonstrated as hard-enforced. A 120-second wall trigger has no
documented finite maximum termination-to-last-exit latency. The job commit
limit's equivalence to the exact accepted private-commit metric, the
workload-to-controller evidence channel, and the 8,196-record ledger fit
are also unverified. Q03's unexpected outside-job-child recovery is
unqualified under the proposed restricted process ACL.

## Assumptions, limitations and unresolved issues

The corrected analytical arithmetic is `6,147 × 850 + 2,049 × 1,400 =
8,093,550` raw bytes, approximately 7.72 MiB. Neither this likely estimate
nor the 2,048-byte planning envelope is a formal maximum because every
serialized nested checkpoint is not byte-bounded. Q10 therefore requires a
separate schema/writer addendum before its deterministic synthetic input can
be generated. The Phase 2A invocation environment is also incomplete: the
two required overrides are `PYTHONHASHSEED=0` and
`TPCN_LUNA65_EVIDENCE_DIR`, but the full inherited-variable policy still
needs an approved addendum.

Four independent read-only reviews completed:

| Review lane | Disposition | Effect on gates |
|---|---|---|
| Windows Job Object correctness | **PASS** on Q05 specification | Confirms the user-mode limit and bounded sampling description; does not establish hard combined CPU enforcement. |
| Supervisor failure/security behavior | **PASS** on fail-closed framing | Normal breakaway is denied; unexpected outside-job-child recovery remains owner-gated and unqualified. |
| Evidence/artifact budget | **PASS WITH CLARIFICATIONS** on bounded evidence structure | Q05 summary is structurally compatible with its allocation; no ledger-fit proof exists, Q10 needs a schema/writer addendum, and inherited environment handling is unresolved. |
| Governance/provenance | **PASS — PUBLICATION-READY** | Confirms governance-only scope, capacity arithmetic, no execution authorization, and preservation of Luna-64/Luna-63C boundaries. |

**Integrated Luna-0 disposition: BLOCKED — SUPERVISOR QUALIFICATION CONTRACT
INCOMPLETE.** The independent reviews support the design framing, not
execution readiness. Hard combined CPU enforcement, finite wall termination,
memory metric reconciliation, a controller-owned evidence path and exact
ledger fit, full environment policy, Q03 recovery, and observer protocol
remain unresolved. No supervisor has been independently qualified. No
reviewer authorizes execution.

## Reproduction and rollback

No workload reproduction applies. The baseline commit is the safe restoration
point; preserve unrelated work and do not revert or rewrite prior published
evidence. Any later publication is governance-only and must be preceded by
independent exact-byte review, exact allowlist verification, staged-byte and
Git-blob checks, and remote verification.
The independent design reviews recorded above are not this final staged-byte
precommit review; it remains an outstanding publication gate.

## Next assignment

The project owner must decide the unresolved resource guarantees and
evidence-channel/schema/environment questions, Q03 recovery, and observer
protocol. Any future synthetic qualification requires a separately reviewed
final contract, a specifically identified independently qualified
supervisor, and explicit owner authorization.

**Supervisor qualification: NOT AUTHORIZED.**

**Phase 2A: NOT AUTHORIZED. Phase 2B: NOT AUTHORIZED.**

**Full Spiral: BLOCKED. Simon Says: SOURCE RECOVERY ONLY.**

**Luna-64 corrective execution: BLOCKED. Luna-63C: FROZEN.**
