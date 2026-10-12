# Luna-0 Handoff — Luna-65 Corrective Contract Closure R2

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-65 Phase 2A supervisor corrective contract closure"
  task_id: "L65-PHASE2A-SUPERVISOR-AUTH-I-CORRECTIVE-R2"
  component: "Windows Phase 2A supervisor governance"
  status: "blocked"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "1d6325f3ca738b32a6ee9e1a5613d2faa9458770"
  result_revision: "uncommitted"
  dependencies:
    - "Owner-approved Phase 2A resource policy"
    - "Luna-65 supervisor implementation proposal R1"
    - "Fresh exact-byte independent review lanes A-D"
  owner: "Repository owner"
  classification:
    - "governance"
    - "Windows supervisor contract review"
    - "no execution"
  hypothesis: "A single-file corrective design can be made source-reviewable without claiming Windows enforcement or qualification."
  counter_hypothesis: "A remaining helper-lifecycle gap and unresolved policy/profile gates prevent integrated readiness."
  interfaces_relied_on:
    - "Windows process, token, environment, pipe, and Job Object APIs"
    - "QPC-based host supervision"
    - "Controller-owned bounded artifact writer"
  label_information_boundary:
    - "No labels, neural inputs, dataset, or scientific workload used"
  timing_assumptions:
    - "120 seconds monitored aggregate user-plus-kernel CPU"
    - "120 seconds monitored wall time"
    - "Primary stop request at 115 seconds"
    - "Post-budget observation duration remains an owner decision"
  reset_boundaries: []
  resource_bounds:
    - "268435456-byte aggregate concurrent private-commit requirement"
    - "1048576-byte retained-artifact ceiling"
    - "Zero workload retries"
    - "Whole-job termination and containment requirement"
  authorized_scope:
    - "Governance analysis and corrective contract review"
    - "Read-only provenance/hash/Git inspection"
    - "Fresh independent exact-byte review lanes A-D"
    - "Record this blocked handoff"
  unauthorized_scope:
    - "Supervisor source edits"
    - "Supervisor invocation, runtime tests, probes, sizing, or qualification"
    - "Phase 2A/2B fixtures, datasets, training, scoring, or benchmarks"
    - "Workflow publication, staging, commit, or push"
  controls:
    - "Preserve existing source, R1 records, and pre-existing workflow modification"
    - "Review R5 contract bytes by SHA-256"
    - "Do not claim API requests or source review establish enforcement"
  measurements:
    - "Exact checkout SHA-256 and line-ending identity"
    - "Baseline, branch, status, and preserved artifact identities"
    - "Independent design-review verdicts"
  information_boundary_check:
    - "No fixture, model, label, dataset, or production module executed or changed"
  hardware_mapping:
    - "QPC is host supervision time only, not a neural timestep"
    - "No hardware equivalence claim"
  architecture_invariants_touched: []
  preserves:
    - "A01-A15 and all production/core semantics"
    - "Authorization Q and all fixture/benchmark prohibitions"
    - "Historical R1 draft and review findings"
  architecture_change: false
  proposal: "workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_IMPLEMENTATION_AUTH_R1.md"
  files_changed:
    - "workflow/handoffs/luna-0-luna65-phase2a-corrective-contract-review-r2.md"
  tests_added: []
  tests_passing: []
  tests_failed:
    - "Integrated exact-byte R5 review is BLOCKED"
  tests_not_run:
    - "All code execution, compilation, tests, probes, sizing, qualification, fixtures, and benchmarks"
  assumptions:
    - "The listed governance baseline and branch are the controlling starting point"
  unresolved:
    - "Observer may be left running if the primary fails before the watchdog is active"
    - "Exact worker/helper token and environment profiles remain unfrozen"
    - "Memory metric mapping, observation duration, cessation evidence, and Q03 assurance require owner decisions"
    - "Separately authorized 8196-record ledger-sizing prerequisite remains outstanding"
    - "Renewed corrective implementation authorization has not been issued"
  recommended_next_agent:
    - "Luna-0: revise only the helper startup/recovery design to close observer lifetime coverage, then obtain fresh exact-byte A-D review"
    - "Repository owner: resolve the listed policy/profile decisions and ledger prerequisite before issuing any new implementation authorization"
```

## Outcome and provenance

**Disposition: BLOCKED — CORRECTIVE CONTRACT NOT READY FOR OWNER
AUTHORIZATION.** The current reviewed contract is
`workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_AUTH_I_CORRECTIVE_R2.md`,
checkout SHA-256
`9D80C19E9CE5CA82695747DA17D740B7AD0FA679AA0F3141AB214E49CC2708A9`.
It is 80,656 bytes and retains CRLF line endings (1,181 CRLF, zero bare
LF). It remains untracked and unpublished.

**OBSERVED:** branch is
`governance/luna64-r4.3-freeze-20261010`; `HEAD` is
`1d6325f3ca738b32a6ee9e1a5613d2faa9458770`. The expected source and
historical-document identities were rechecked:

| Artifact | SHA-256 | State |
|---|---|---|
| `scripts/luna65_phase2a_supervisor.py` | `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1` | 21,494 bytes, untracked; unchanged |
| `workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_AUTH_I_CORRECTIVE_R1.md` | `4E625C363A239BAB1386E0DE454A11F0F23972BFB5BD9137141946C282750999` | Untracked; unchanged |
| `workflow/handoffs/luna-0-luna65-phase2a-corrective-contract-review-r1-20261012.md` | `04B048E42913B26FFCAB6173A94134BF200055F4435C3536ED08F0D32C4A2C00` | Untracked; unchanged |
| `workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_IMPLEMENTATION_AUTH_R1.md` | `31C2CEDAAC91C78A79D746879AEB52759A92335DDA7D18EDC5F0E055F141EA97` | Tracked; unchanged |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `64AF62CD2E8CD0696BF52EEDF63672FB04399EF949B580FD551360A0F237ED61` | Pre-existing modification; unchanged |

No changes are staged. The pre-existing workflow edit, untracked blocked
source, R1 draft, and R1 handoff were preserved. R2 was revised locally
after the R4 review; R5 below reviewed its resulting exact bytes.

## Corrective design and remaining blocker

R5 closes the R4 ordering and success-publication defects in the contract:

- The workload Job Object is configured before helper startup.
- If Q03 is selected, the observer is started and readiness is checked
  before workload creation.
- The watchdog is created suspended; exact primary, job, and optional
  observer process handles plus the immutable startup record are supplied
  before watchdog resume/readiness.
- Workload creation is gated on required helper readiness, and workload
  resume follows the suspended-root membership and accounting checks.
- Caller-facing success requires validated `EVIDENCE_COMMIT`, successful
  primary handle cleanup, and observed successful primary exit. The
  observation cutoff requires both commit and successful primary exit;
  missing either invokes bounded failure cleanup.

**R5 Lane A blocker:** the selected observer is resumed and active before
the watchdog is created or ready. Both helpers are outside the workload job.
If the primary fails during this interval, no active watchdog or specified
self-expiry/reaper is responsible for stopping the observer and its ETW
session. The contract’s later stop/reap behavior assumes a functioning
controller. This is a source-contract lifecycle gap and must be corrected
and independently reviewed before an integrated PASS. Do not infer
containment from ETW or the workload Job Object.

## Exact-byte independent review

Four fresh lanes reviewed the same R5 checkout SHA-256 shown above. Their
verdicts are design-review results, not runtime qualification:

| Lane | Verdict | Finding |
|---|---|---|
| A — admission, tokens, environment, pipes, Job Object | **BLOCKED** | Observer can outlive a failing primary before watchdog readiness; exact profiles and Q03 query remain owner gates. |
| B — monitoring, termination, cessation, controller failure | **BLOCKED** | Monitoring and bounded failure lifecycle are specified; finite observation duration is still unapproved. |
| C — evidence, memory, artifact lifecycle | **BLOCKED** | Writer and 1-MiB allocation are coherent as a design; ledger fit is unproven pending separately authorized sizing, and memory mapping/observation duration remain owner gates. |
| D — governance, provenance, scope | **PASS** | Scope and authority remain correctly bounded; no implementation, qualification, fixture, or publication authority is granted. |

The integrated disposition is **BLOCKED — CORRECTIVE CONTRACT INCOMPLETE**.
The R5 review did not run code or tests and did not establish enforcement.

## Policy and qualification boundaries

The frozen requirements remain 120 seconds monitored aggregate
user-plus-kernel CPU, 120 seconds wall, a termination request at 115
seconds, 268,435,456 bytes aggregate concurrent private committed memory,
1,048,576 bytes retained artifacts, zero retries, and whole-job
containment. The contract does not demonstrate that the Job Object memory
charge equals the accepted private-commit metric.

The following remain unresolved before a new corrective implementation
request:

1. Owner selection of a memory enforcement metric or accepted conservative
   mapping; job charge is not established as equivalent to aggregate
   concurrent per-process private commit.
2. Owner selection of a finite post-budget observation duration. The
   proposed 15 seconds is not approved and does not extend permitted
   workload time.
3. Owner acceptance of bounded cessation-observation intervals rather than
   an exact physical exit timestamp.
4. Q03 assurance choice: accept and qualify the version-pinned native
   identity-query candidate, approve a supported alternative, or separately
   authorize an OS-enforced boundary.
5. Freeze exact worker/helper token groups and privileges, executable and
   fixture identities, environments, access requirements, and writable-path
   threat model.
6. Separately authorize and complete the proposal-required 8,196-record
   ledger-sizing prerequisite, or explicitly change that prerequisite.
7. Obtain a new affirmative implementation authorization bound to the
   reviewed contract/source identities and resolved decisions.

The single-file implementation allowlist remains
`scripts/luna65_phase2a_supervisor.py`; it is **not authorized** by this
handoff. No other source, production module, fixture, or test may be
modified under the current governance-only scope.

## Validation and status

| Command or procedure | Result |
|---|---|
| Baseline/branch/Git-state inspection | Baseline and branch matched; no staged changes |
| SHA-256 and line-ending inspection | R5 contract hash/CRLF counts verified; preserved identities matched |
| Fresh independent exact-byte review | A BLOCKED, B BLOCKED, C BLOCKED, D PASS |
| Code execution, compilation, tests, probes, sizing, qualification, fixtures, benchmarks | Not run; not authorized |
| Workflow publication, staging, commit, push, remote verification | Not performed; integrated PASS not reached |

**Corrective supervisor implementation: NOT AUTHORIZED.**

**Supervisor qualification: NOT AUTHORIZED.**

**Phase 2A and Phase 2B fixtures: NOT AUTHORIZED.**

**Full Spiral execution: BLOCKED.**

**Luna-64 corrective execution: BLOCKED.**

**Luna-63C: FROZEN.**

## Next bounded assignment

Luna-0 may revise the unpublished R2 draft only to close the observer
startup/recovery gap, after selecting a lifecycle that gives a trusted
watchdog responsibility for the observer before it can run. Preserve the
R5 review findings and obtain a fresh exact-byte A-D review of any changed
draft. Do not publish, update the authoritative workflow, implement the
supervisor, or run sizing/qualification until the governing owner
decisions and separate authorizations are in place.
