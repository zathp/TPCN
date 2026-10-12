# Luna-0 Luna-65 RP-1 Host Inspection Publication and Execution Authorization

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "RP-1 host-inspection publication and execution"
  task_id: "L65-PHASE2A-RP1-HOST-INSPECTION-EXECUTION"
  component: "Luna-65 Phase 2A RP-1 host inspection"
  status: "partial"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "948f5e70a43a3524dfef6bbe8f04bbd041770fd6"
  result_revision: "publication pending"
  dependencies: []
  owner: "Project owner"
  classification: ["governance", "host inspection"]
  hypothesis: "not applicable; bounded observational inspection"
  counter_hypothesis: "not applicable"
  interfaces_relied_on:
    - "Published RP-1 PowerShell 5.1 read-only probe and frozen contract"
  label_information_boundary:
    - "Host observations only; no labels enter neural computation"
  timing_assumptions:
    - "27-second cooperative internal budget and 45-second attended outer limit"
  reset_boundaries: ["not applicable"]
  resource_bounds:
    - "4,000,000-character stdout cap"
    - "5 MiB combined retained-output ceiling, checked after execution"
    - "Memory unmeasured and unenforced"
    - "Exactly one invocation; zero retries"
  authorized_scope:
    - "Publish the hash-bound contract and PowerShell probe"
    - "Publish this handoff and the authoritative workflow entry"
    - "Prepare the exact RP-1 evidence directory after path and reparse checks"
    - "One attended RP-1 invocation only after successful publication and final preflight"
  unauthorized_scope:
    - "RP-2 and RP-3"
    - "Supervisor implementation or qualification"
    - "Phase 2A or 2B fixtures"
    - "S1-B generator or wrapper reruns"
    - "Full Spiral benchmark and Luna-64 corrective execution"
    - "Any retry of RP-1"
  controls:
    - "Frozen baseline, source hashes, Git blobs, command, paths, and run ID"
    - "Pre-execution empty evidence-directory and run-ID checks"
    - "Independent review of retained RP-1 evidence before findings publication"
  measurements: ["not yet collected"]
  information_boundary_check:
    - "Probe uses fixed read-only host queries and writes only to designated stdout/stderr files"
  hardware_mapping: ["not applicable"]
  architecture_invariants_touched: []
  preserves:
    - "Event-driven architecture and all existing benchmark results"
    - "No inference of OS enforcement from observational evidence"
  architecture_change: false
  proposal: null
  files_changed:
    - "scripts/luna65_phase2a_rp1_host_inspection.ps1"
    - "workflow/docs/luna/LUNA_65_PHASE2A_RP1_HOST_INSPECTION_CONTRACT.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-luna65-rp1-host-inspection-20261012.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "Publication, remote identity verification, host path checks, final preflight, and RP-1 execution are pending"
  assumptions:
    - "Owner decisions in the 2026-10-12 authorization govern this gate"
    - "The pre-authorization text in the frozen contract is historical and is not edited"
  unresolved:
    - "Publication commit and remote identity"
    - "Evidence-directory preparation"
    - "Attended execution preflight and RP-1 result"
    - "Independent evidence-review disposition"
  recommended_next_agent:
    - "Luna-0: finish publication/preflight and perform only the authorized RP-1 execution"
```

## Outcome and owned scope

**OBSERVED:** At baseline `948f5e70a43a3524dfef6bbe8f04bbd041770fd6`, the
reviewed contract and PowerShell probe were untracked and matched their
owner-supplied SHA-256 and Git blob identities. The only other untracked files
were a supervisor scaffold and an S1-B authorization record; neither is in the
publication allowlist.

**AUTHORIZED:** The owner accepted the PowerShell replacement, S06 bounded
sample limitation, documented RP-1 omissions, publication-before-execution,
and exactly one attended invocation subject to preflight. This handoff records
publication and execution authorization only; it does not claim execution or
host findings.

## Architecture evidence

No architecture clause is changed. RP-1 is bounded host observation and does
not qualify enforcement or runtime compatibility. No ACP is required or
authorized. RP-2, RP-3, supervisor implementation/qualification, fixtures,
full Spiral, Luna-64 corrective execution, and Luna-63C status remain outside
this gate.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `git rev-parse HEAD`, status, branch and remote inspection | Frozen baseline `948f5e70a43a3524dfef6bbe8f04bbd041770fd6` | HEAD and branch matched; tracked tree clean; four untracked files identified | Pre-publication command log |
| SHA-256 and `git hash-object` for contract and probe | Windows checkout at frozen baseline | Both SHA-256 and blob identities matched owner-supplied values | Pre-publication command log |
| Allowlist staging and publication verification | Not run | Pending | Not run |
| Evidence-directory checks and creation | Host paths not yet inspected | Pending | Not run |
| RP-1 exact invocation | Not run | Pending; no run ID consumed | Not run |
| Independent evidence review | Not run | Pending | Not run |

## Benchmark and resource results

Not applicable to TPCN benchmark efficacy. Host evidence and RP-1 resource
observations have not yet been collected. The experiment is observational;
resource bounds are cooperative and do not constitute hard enforcement.

## Assumptions, limitations and unresolved issues

The contract's pre-authorization status is historical. The owner's explicit
authorization permits only the scope listed above and does not amend or change
the hash-bound contract. RP-1's S06 scan is a bounded sample, not complete
Low-writable filesystem coverage. Memory remains unmeasured and unenforced.
The exact source, contract, evidence directory, outputs, run ID, remote state,
and operator-attendance checks remain binding preflight items.

## Reproduction and rollback

Before execution, verify the published commit and remote, clean tracked tree,
contract/probe identities, exact empty evidence destination, unused run ID,
frozen command, limits, and attended operator. Execute only the command in
contract §3.1 with run ID `20261012T220000Z-5d2e7b4`; do not retry. Preserve
both output files without modification. Do not delete or overwrite unexpected
host files.

## Next assignment

Luna-0 completes the authorized publication and host preflight, then either
stops on any discrepancy or consumes exactly one attended RP-1 invocation.
Afterward, an independent reviewer must disposition the evidence before RP-1
findings are published. No subsequent compatibility gate is authorized here.
