---
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-65 Corrective Contract Review"
  task_id: "L65-PHASE2A-SUPERVISOR-AUTH-I-CORRECTIVE-R1"
  component: "Windows Phase 2A supervisor governance"
  status: "blocked"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "1d6325f3ca738b32a6ee9e1a5613d2faa9458770"
  result_revision: "uncommitted"
  dependencies:
    - "Owner-approved Phase 2A resource policy and Authorization I proposal"
  owner: "Repository owner"
  classification:
    - "governance"
    - "Windows process supervision"
    - "no execution"
  hypothesis: "A one-source-file corrective implementation contract can define a safe admission and observation design without qualifying enforcement."
  counter_hypothesis: "Unresolved Windows enforcement and policy choices prevent a complete implementation contract."
  interfaces_relied_on:
    - "Windows Job Object and process APIs"
    - "QPC supervisor-only wall-time accounting"
    - "Controller-owned bounded evidence channel"
  label_information_boundary:
    - "No labels, neural computation, or dataset inputs used"
  timing_assumptions:
    - "Accepted monitored CPU and wall budgets are each 120 seconds"
    - "Primary early wall-stop request is at 115 seconds"
    - "Post-budget observation interval remains owner decision"
  reset_boundaries: []
  resource_bounds:
    - "268435456-byte job-wide memory-control candidate"
    - "1048576-byte retained-artifact ceiling"
    - "Zero retries"
  authorized_scope:
    - "Governance analysis and corrective contract preparation"
    - "Independent read-only review lanes A-D"
    - "Read-only provenance and SHA-256 inspection"
  unauthorized_scope:
    - "Supervisor source edits"
    - "Supervisor/runtime invocation, smoke testing, and qualification"
    - "Capacity fixtures, sizing, stress probes, or benchmarks"
    - "Staging, committing, or publication"
  controls:
    - "Preserve existing source and uncommitted workflow changes"
    - "No code execution or runtime validation"
  measurements:
    - "Checkout byte identities and Git state"
    - "Independent exact-byte review of corrective contract"
  information_boundary_check:
    - "No workload, fixture, or TPCN production data executed"
  hardware_mapping:
    - "Windows APIs described as proposed controls only; enforcement unqualified"
  architecture_invariants_touched:
    - "None; no TPCN architecture or ACP change"
  preserves:
    - "Accepted Phase 2A resource policy"
    - "Authorization Q and all fixture/benchmark prohibitions"
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_AUTH_I_CORRECTIVE_R1.md"
    - "workflow/handoffs/luna-0-luna65-phase2a-corrective-contract-review-r1-20261012.md"
  tests_added: []
  tests_passing: []
  tests_failed:
    - "Current exact-byte contract review is not integrated PASS"
  tests_not_run:
    - "All source static validation"
    - "Supervisor, test, probe, qualification, fixture, and benchmark execution"
  assumptions:
    - "The requested baseline commit is the actual HEAD"
  unresolved:
    - "Owner must freeze post-budget/Q03 observation interval and unconfirmed-cessation point"
    - "Owner must accept or reject observed-cessation QPC evidence"
    - "Owner must resolve JobMemoryLimit mapping to accepted aggregate private commit"
    - "Corrective contract has Windows API, handle-lifecycle, containment, and evidence gaps detailed below"
  recommended_next_agent:
    - "Luna-0: revise corrective contract only after owner/security design choices are resolved, then repeat exact-byte A-D review"
    - "Owner: provide any new implementation authorization only after a PASS contract"
---

# Luna-65 Phase 2A corrective contract review

## Outcome and provenance

**Disposition: BLOCKED — CORRECTIVE CONTRACT NOT READY FOR OWNER
AUTHORIZATION.**

The required baseline is verified: `HEAD` is
`1d6325f3ca738b32a6ee9e1a5613d2faa9458770`, on
`governance/luna64-r4.3-freeze-20261010`, with parent
`d11d370a7c97184529845c9cac984fc22018c576`. The proposal file's checkout
SHA-256 is
`31C2CEDAAC91C78A79D746879AEB52759A92335DDA7D18EDC5F0E055F141EA97`;
its committed Git blob is
`3aefe152d0cf55bb759dec85551efb3239d541fc`.

| Artifact | Observed SHA-256 | Git state / observation |
|---|---|---|
| `scripts/luna65_phase2a_supervisor.py` | `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1` | 21,494 bytes; untracked; unchanged in this task |
| `workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_AUTH_I_CORRECTIVE_R1.md` | `4E625C363A239BAB1386E0DE454A11F0F23972BFB5BD9137141946C282750999` | 40,275 bytes; untracked draft; exact reviewed revision |
| `workflow/docs/luna/LUNA_65_PHASE2A_SUPERVISOR_IMPLEMENTATION_AUTH_R1.md` | `31C2CEDAAC91C78A79D746879AEB52759A92335DDA7D18EDC5F0E055F141EA97` | Tracked; unchanged |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `64AF62CD2E8CD0696BF52EEDF63672FB04399EF949B580FD551360A0F237ED61` | Modified before this task; unchanged in this task |
| `workflow/handoffs/luna-0-luna65-phase2a-authorization-i-review-20261012.md` | `B542AD2FD7BD6B587280420D8210F570CF13A66CA6F4CE86F461DDA3D94A46C4` | Earlier Authorization I source review; untracked |

No files were staged. `git diff --name-only` lists only the pre-existing
workflow modification. A `git diff --check` was run; it returned exit code
2 with trailing-whitespace diagnostics on added lines in the pre-existing
CRLF `-text` workflow file. No source static check was run in this
governance-only task.

## Candidate source inventory

The candidate remains the earlier fail-closed scaffold; this review did not
edit it. Missing implementation includes:

- Suspended worker creation, Job Object assignment, membership verification,
  and controlled resume.
- An independent watchdog, bounded monitor and cessation path, plus process
  tree observer and Q03 recovery.
- Effective restricted-token and filesystem write-boundary enforcement.
- A controller-owned retained-evidence writer with complete failure and
  integrity records.
- A bounded post-budget observation/finalization lifecycle.

The candidate must not be represented as operational or qualified. Its
implementation gap is not evidence of enforcement.

## Corrective contract summary

The draft keeps the implementation allowlist at
`scripts/luna65_phase2a_supervisor.py` and preserves the accepted resource
policy: 120 seconds monitored aggregate user-plus-kernel CPU, 120 seconds
monitored wall, a five-second early stop request at 115 seconds, a
268,435,456-byte Job Object memory-control candidate, 1,048,576 bytes
retained artifacts, zero retries, and whole-process-tree containment.

It specifies admission sequencing, process/job APIs, supervision and
cessation observations, ETW/Q03 recovery, restricted-token and filesystem
design, memory accounting, bounded evidence, and a static-only validation
boundary. These are contract requirements and design candidates, **not
verified enforcement**.

## Independent exact-byte review

Four read-only lanes reviewed the exact contract checkout bytes identified
above. Results:

| Lane | Verdict | Independent finding |
|---|---|---|
| A — process admission / Job Object semantics | **BLOCKED** | §4 line 136 ambiguously says to use `CreateProcessW` for the environment step, while line 142 requires `CreateProcessAsUserW` with the restricted token. Specify local environment-block construction and pass it to `CreateProcessAsUserW`. Parent-side copies of child pipe handles need explicit closure after process creation to permit EOF. Specify the intended Job Object handle in `IsProcessInJob`, including nested-job context (§4 line 143; §6 line 333). |
| B — monitoring / termination / controller failure | **PASS** for lane scope | §5 has a bounded monitoring/request/cessation design, sample freshness, admission deadline, failure classifications, final accounting outcomes, and shared Q03 deadline. Owner decisions remain open: post-budget duration/unconfirmed point and acceptance of observed-cessation QPC (§2, §5.2). |
| C — token / filesystem / containment / evidence | **BLOCKED** | Exact restricted-token group/SID expectations and effective ACL/environment profile remain unpinned (§4 lines 136–137; §7). ETW/Q03 recovery is explicitly unqualified (§6). Job commit is not shown equivalent to accepted aggregate private commit (§8). Writer ownership/failover when primary fails and mandatory failure evidence behavior remain underspecified (§5, §9); ledger fit remains unproven (§9). |
| D — governance / provenance / authority | **BLOCKED** | Provenance, one-source allowlist, static-only scope, and status are consistent; the exact-byte review outcome is recorded here. Contract publication is not supported because A/C block and owner decisions remain unresolved. |

The integrated verdict is **BLOCKED — CORRECTIVE CONTRACT INCOMPLETE**.
Earlier review results against SHA-256
`4171C8FF49D9A0EDD5CE291C571F57F7A545FB51A41CD478CCFFD12FCEFD68FF`
are superseded by the exact-byte review above. Their findings informed the
revision but do not substitute for this final review.

## Validation record

| Command or procedure | Revision / environment | Observed result |
|---|---|---|
| `git rev-parse HEAD`, `git status --short`, `git diff --name-only` | Baseline commit above; Windows checkout | Baseline and existing worktree state confirmed; nothing staged |
| `Get-FileHash -Algorithm SHA256` | Checkout bytes, exact paths above | Identities recorded in provenance table |
| `git diff --check` | Tracked worktree diff | Exit 2; trailing-whitespace diagnostics on added lines in the pre-existing CRLF `-text` workflow file |
| Supervisor `py_compile` | Not authorized in this task | Not run |
| Source no-index whitespace check | Not authorized in this task | Not run |
| Imports, entry point, tests, smoke tests, runtime, probes, qualification, fixtures, capacity, benchmark | Explicitly prohibited | Not run |

## Remaining blockers and owner decisions

1. Correct the process creation/environment wording, pipe-handle closure
   lifecycle, and explicit target-job membership checks; independently
   review the exact revised bytes.
2. Freeze the bounded post-budget/Q03 observation interval and exact
   `TERMINATION_UNCONFIRMED` point.
3. Decide whether the `cessation_confirmed_observed_qpc` evidence rule is
   acceptable; do not claim an exact physical process-exit timestamp.
4. Resolve whether Job Object job-memory accounting can conservatively
   enforce the accepted aggregate concurrent `PrivateUsage` metric.
5. Pin exact token SID/group/privilege expectations, environment values,
   ACL and writable-path matrix, and target invocation profile before
   implementation; do not invent missing values.
6. Define writer ownership/failover and the behavior when the controller or
   evidence writer fails. Preserve mandatory records or report
   `EVIDENCE_INCOMPLETE`; never return success-shaped fallback.
7. Establish ETW privilege, coverage/loss behavior, Q03 recovery,
   filesystem-write containment, and ledger fit during a separately
   authorized qualification. No such qualification is authorized now.

## Authorization and publication status

**Corrective implementation: NOT YET AUTHORIZED.**

**Supervisor qualification: NOT AUTHORIZED.**

**Authorization Q: NOT AUTHORIZED.**

**Phase 2A/2B fixtures: NOT AUTHORIZED.**

**Full Spiral benchmark: BLOCKED.**

**Luna-64 corrective execution: BLOCKED.**

**Luna-63C certification: FROZEN.**

No corrected contract or workflow was published, and no implementation was
staged or committed. The corrective draft SHA-256 above is a checkout
identity, not a publication identity or precommit approval.

## Next bounded assignment

Luna-0 may revise only the corrective contract to resolve the concrete
review findings and record owner decisions; then obtain fresh independent
A–D review against the new exact SHA-256. The repository owner may consider
a separate corrective implementation authorization only after a PASS
contract. Any later implementation remains limited to the exact
owner-authorized file/profile and listed nonexecuting checks. Qualification
and all fixtures/benchmarks require separate later authorization.
