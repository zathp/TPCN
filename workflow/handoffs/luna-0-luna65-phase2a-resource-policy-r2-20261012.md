# Luna-0 — Luna-65 Phase 2A Monitored Resource-Policy R2 Handoff

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-65 Phase 2A monitored resource policy R2"
  task_id: "L65-PHASE2A-MONITORED-RESOURCE-POLICY-R2"
  component: "Phase 2A resource monitoring, containment, and evidence"
  status: "complete"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "eaa55bdd777da348ed317360f1482eb00b3e279c"
  result_revision: "uncommitted"
  dependencies:
    - "Published Luna-65 Phase 2 capacity and Phase 2A correction"
    - "R1 Windows supervisor qualification design and review record"
    - "Explicit owner acceptance of R2 monitored CPU/wall policy for Phase 2A design"
  owner: "Project owner"
  classification:
    - "governance-only"
    - "resource-policy-design"
    - "no-execution"
  hypothesis: "A fail-on-observed-overrun monitored CPU/wall design can replace the previous hard CPU/wall cessation requirements for Phase 2A design without changing the hard memory/artifact limits or scientific lane."
  counter_hypothesis: "The monitoring, metric, evidence, or containment design is underspecified or cannot support the accepted Phase 2A policy."
  interfaces_relied_on:
    - "Windows Job Object aggregate CPU accounting and job memory limits"
    - "QPC monotonic elapsed-time observations"
    - "Phase 2A versioned probe JSONL and external evidence directory"
    - "Controller-owned bounded evidence writer"
  label_information_boundary:
    - "No task labels, benchmark inputs, or benchmark outputs used."
    - "No Spiral or Simon Says execution."
  timing_assumptions:
    - "120-second monitored cumulative job-wide user-plus-kernel CPU budget."
    - "120-second monitored elapsed wall budget."
    - "Ten-millisecond target sampling cadence and 100-ms maximum acceptable observation gap are proposals requiring qualification."
    - "Five-second Phase 2A wall stop margin is proposed and not owner-approved."
    - "No zero CPU overshoot or exact-time process cessation guarantee."
  reset_boundaries:
    - "No neuron, runner, dataset, or benchmark state created or reset."
  resource_bounds:
    - "Phase 2A target-counter probes remain bounded at 8,196 with zero retries."
    - "Hard job-wide concurrent private-commit ceiling: 268,435,456 bytes."
    - "Hard combined retained-artifact ceiling: 1,048,576 bytes."
    - "Qualification plan is proposed separately: ten synthetic cases once, observed job CPU <=30 seconds, elapsed wall <=360 seconds, job memory <=268,435,456 bytes, artifacts <=1,048,576 bytes, network disabled."
  authorized_scope:
    - "Read and verify repository/governance/provenance."
    - "Record owner-accepted Phase 2A monitored resource policy."
    - "Prepare a bounded supervisor and synthetic qualification design."
    - "Request independent read-only review."
    - "Publish reviewed governance documents only if all requested review gates pass."
  unauthorized_scope:
    - "Supervisor implementation or infrastructure changes."
    - "Synthetic supervisor qualification or sizing execution."
    - "Phase 2A/2B fixture implementation or execution."
    - "Spiral/Simon Says data generation, training, evaluation, or scoring."
    - "Luna-64 corrective execution or Luna-63C changes."
  controls:
    - "No production files changed."
    - "No Job Object API operation, supervisor, worker, test, sizing run, fixture, or benchmark executed."
    - "R1 retained as historical evidence; Phase 2B resource policy is not amended."
    - "Hard memory/artifact ceilings and zero retries preserved."
  measurements:
    - "Baseline branch, HEAD, origin ref, and clean worktree verified."
    - "Phase 1 source/test and closure hashes match published values."
    - "Phase 2 capacity, R1, Phase 2A correction, and Spiral contract identities recorded."
    - "R1 analytic likely raw ledger estimate is 8,093,550 bytes; no compression ratio or fit assumed."
    - "No runtime resource measurements made."
  information_boundary_check:
    - "Phase 2A direct-neuron capacity verification only."
    - "No Phase 2B, benchmark, or scientific acceptance criteria changed."
  hardware_mapping:
    - "Execution-control design only; no TPCN computation or hardware mapping changed."
  architecture_invariants_touched: []
  preserves:
    - "Luna-12G historical TANH_LEGACY results."
    - "Full-replication E2 capacity uncertainty."
    - "Luna-64 blocked status."
    - "Luna-63C frozen evidence."
    - "Separate Phase 2A and Phase 2B authorization gates."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2A_RESOURCE_POLICY_R2.md"
    - "workflow/docs/luna/LUNA_65_PHASE2_CAPACITY.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-luna65-phase2a-resource-policy-r2-20261012.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All tests, synthetic qualification cases, sizing checks, fixtures, probes, and benchmarks not run by authorization."
  assumptions:
    - "Owner instruction accepts the monitored CPU/wall semantics as stated."
    - "No exact Phase 2A wall stop margin is approved."
  unresolved:
    - "Owner acceptance of an exact Phase 2A wall stop margin."
    - "Job-wide private commit versus concurrent PrivateUsage enforcement proof."
    - "Exact 8,196-record compressed ledger fit and sizing addendum."
    - "Controller-owned evidence channel implementation/qualification."
    - "Complete inherited environment policy."
    - "Process observer, Q03 recovery, controller/watchdog, and termination qualification."
  recommended_next_agent:
    - "Project owner: decide exact proposed wall stop margin and authorize implementation only under a separate exact allowlist."
    - "Supervisor implementation role: only after explicit owner authorization and closure of applicable resource/evidence prerequisites."
```

## Outcome and scope

The owner accepted monitored CPU and wall budgets for Phase 2A qualification
design. R2 retains the 120-second CPU and wall budgets but replaces hard
CPU/wall cessation guarantees with trusted monitoring, whole-job termination
requests, and failure on observed overruns. The hard 268,435,456-byte
job-wide private-commit and 1,048,576-byte retained-artifact ceilings remain.
The proposed five-second wall stop margin has not been approved.

R2 is a Phase 2A-only overlay. Phase 2B, the Spiral scientific protocol,
Simon Says, Luna-64, and frozen Luna-63C are unchanged. No implementation,
test, qualification, fixture, or workload was executed.

## Provenance verified

Baseline: `eaa55bdd777da348ed317360f1482eb00b3e279c` on
`governance/luna64-r4.3-freeze-20261010`; origin pointed to the same commit
and the worktree was clean.

| Evidence | SHA-256 |
|---|---|
| Phase 2 capacity contract at baseline | `51BE7271DB57E0AFF9E9ED8BB317382D49F22C53BC8E1D13667FAED893BE76CB` |
| Historical R1 supervisor design | `7DD5EE88EDAC1AF9049C265D28B8E60DD1558AD80D2EC760575D25DE6FB4D93D` |
| Phase 2A correction handoff | `459E4AC9CAC322A88BF580F2F1016082FEF7E7C9A69369C0322BA7305181E684` |
| Phase 1 closure handoff | `4B4D7BF378C3C38FFC755106ECE597A6FBEEA9EC712CFB5AFF105989E680E022` |
| `tpcn/experiments.py` | `CABB81DA36280E7CDCF614B8B3E2CD5567035C20C6706A85B25B1A73310E967D` |
| `tpcn/experiment_excursion_runtime.py` | `DF007154939C6C554A3D914C15CE91C87954BEEEBF29DF416EE27D138F119D5A` |
| `tests/test_luna65_execute_example.py` | `DE32193D0E87059E995331E6B490DBEFD26020EB11C9EAFF3EBD27316D4C7D1D` |
| Luna-65 Spiral contract | `1F1D4DD96E21EE760D32CDDE4F0415576C9BAE6AF01B82DB2A9C4E1D9FB5C777` |

The R1 review dispositions and limitations are preserved in the workflow at
the verified baseline. No architecture clause or ACP is changed.

## Validation and review

| Procedure | Result |
|---|---|
| Branch/HEAD/origin/worktree inspection | PASS; expected branch and baseline, clean before edits |
| SHA-256 verification of Phase 1 and Luna-65 sources/handoffs | PASS; values above |
| Architecture contract, changelog, acceptance criteria, ACP guidance, handoff template review | Read; no architecture modification warranted |
| Tests, synthetic sizing, supervisor, fixtures, benchmarks | NOT RUN; prohibited by scope |
| Independent R2 review A — Windows resource semantics | PASS for design consistency; CPU update resolution, memory metric mapping, and target-build readback remain qualification gates |
| Independent R2 review B — termination/failure handling | PASS; no hard-real-time guarantee and wall margin remains unapproved |
| Independent R2 review C — evidence/artifacts | PASS; 1-MiB allocation arithmetic coherent, exact ledger fit unproven |
| Independent R2 review D — governance/provenance | PASS; phase separation, provenance, no-execution boundaries preserved |
| Integrated Luna-0 disposition | PASS — PHASE 2A RESOURCE-POLICY AMENDMENT VERIFIED |
| Exact-byte precommit review | Pending |

## Resource and scientific evidence

No runtime resource measurements were made. R1's ledger sizes remain
estimates, not measured results. The likely raw mixed estimate is 8,093,550
bytes; no compression ratio is assumed. Exact fit under 786,432 bytes is not
established. A separate owner-authorized synthetic sizing check is required
after a byte-bounded record-shape/writer addendum. Any overflow is a failed
artifact result; truncation or omission is forbidden.

## Remaining gates and next assignment

The four independent R2 reviews are complete and the integrated
governance/design disposition is PASS, but no supervisor is qualified. The
next owner decision is to accept the exact five-second early wall stop margin
or name another value. Any implementation, synthetic
qualification, sizing check, Phase 2A, or Phase 2B run requires a separate
explicit owner authorization with exact paths, identities, resource bounds,
environment, evidence destination, and stop conditions.

**Supervisor implementation: NOT AUTHORIZED.**

**Supervisor qualification: NOT AUTHORIZED.**

**Phase 2A fixtures: NOT AUTHORIZED. Phase 2B fixtures: NOT AUTHORIZED.**

**Full Spiral: BLOCKED. Luna-64 corrective execution: BLOCKED. Luna-63C:
FROZEN.**
