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
  result_revision: "65de223151ff196c72263f79e50719a7b6dbbd07"
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
  measurements:
    - "Windows 10 Pro 22H2 build 19045 (UBR 6466)"
    - "RP-1 elapsed_ms=1347; stdout=66533 bytes; stderr=0 bytes; combined=66533 bytes"
    - "stdout SHA-256 D5540237E3B6577704DF45ED44E1634EB928660614CBF9CF65E01BCCD72D8D8E"
    - "stderr SHA-256 E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
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
  tests_failed:
    - "Independent review classified RP1_CONTRACT_DEFECT: contract prohibits New-* commands, but probe uses New-Object twice"
  tests_not_run:
    - "RP-2 and RP-3 compatibility qualification"
    - "Full low-writable filesystem coverage"
    - "Low-token process-right enforcement"
    - "Job Object runtime availability and semantics"
  assumptions:
    - "Owner decisions in the 2026-10-12 authorization govern this gate"
    - "The pre-authorization text in the frozen contract is historical and is not edited"
  unresolved:
    - "Resolve contract/source New-Object discrepancy through a separately authorized review"
    - "U1 low-token process creation remains untested"
    - "U2 low-token interpreter launch, UI restrictions, no-console, and imports remain untested"
    - "U3 handle inheritance remains untested"
    - "U4 denied process rights under Low remain untested"
    - "U5 sample is incomplete; complete Low-writable coverage and owner decision remain open"
    - "U6 label-at-creation capability remains untested"
    - "U7 network non-use/enforcement remains unproven"
    - "U8 remains unprovable under the accepted limit"
    - "No RP-1 retry or RP-2/RP-3 execution is authorized"
  recommended_next_agent:
    - "Luna-0: route the contract/source discrepancy for owner-authorized review; do not advance to RP-2"
```

## Outcome and owned scope

**OBSERVED:** At baseline `948f5e70a43a3524dfef6bbe8f04bbd041770fd6`, the
reviewed contract and PowerShell probe were untracked and matched their
owner-supplied SHA-256 and Git blob identities. The only other untracked files
were a supervisor scaffold and an S1-B authorization record; neither was
staged or published.

**AUTHORIZED:** The owner accepted the PowerShell replacement, S06 bounded
sample limitation, documented RP-1 omissions, publication-before-execution,
and exactly one attended invocation subject to preflight. Publication was
committed as `65de223151ff196c72263f79e50719a7b6dbbd07` and verified against
the fetched remote. The single invocation was consumed. Its emitted
`RP1_COMPLETE` is overridden by the contract's `RP1_CONTRACT_DEFECT` class
after independent review.

## Architecture evidence

No architecture clause is changed. RP-1 is bounded host observation and does
not qualify enforcement or runtime compatibility. No ACP is required or
authorized. RP-2, RP-3, supervisor implementation/qualification, fixtures,
full Spiral, Luna-64 corrective execution, and Luna-63C status remain outside
this gate.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| SHA-256, Git blob, allowlist, commit and fetched remote verification | Windows checkout; publication commit `65de223151ff196c72263f79e50719a7b6dbbd07` | Expected source identities verified; exact four-file allowlist committed; fetched remote equals HEAD | Commit and pre/post-push command records |
| Evidence-directory path/reparse preflight and leaf creation | `C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\rp1` | All existing parent components ordinary directories; created only missing leaf; empty before invocation | Host preflight record |
| Frozen attended RP-1 command, run `20261012T220000Z-5d2e7b4` | Published HEAD; Windows PowerShell 5.1; operator present | Exactly one invocation; command exit 0; no retry | Retained stdout/stderr listed below |
| Output sections, classifications and limits | RP-1 output | S00-S08 each have BEGIN/END with status OK; emitted `RP1_COMPLETE`; no ERROR/TIMEOUT/START_FAIL/SKIPPED/EXIT_NONZERO/CAP_TRUNCATED; two S06 `TRUNCATED_LINES`; retained output within ceilings | stdout: 66,533 bytes, 1,142 lines; stderr: 0 bytes; combined: 66,533 bytes |
| Independent evidence review by Luna-11 Adversarial Architectural Verification | Review against published contract/probe and retained output; no rerun or modification | **`RP1_CONTRACT_DEFECT`**: contract §3.3 prohibits `New-*`, probe has `New-Object` at script lines 37 and 99; no evidence of persistent mutation from those constructors | Independent review disposition in session record |

## Benchmark and resource results

Not applicable to TPCN benchmark efficacy. RP-1 was observational;
resource bounds are cooperative and do not constitute hard enforcement.
Reported elapsed time was 1,347 ms; stdout 66,533 bytes, stderr 0 bytes, and
combined retained output 66,533 bytes. Memory was not measured or enforced.

## Host observations

The exact retained files are:

- `C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\rp1\rp1-20261012T220000Z-5d2e7b4.out.txt`
  (66,533 bytes; SHA-256
  `D5540237E3B6577704DF45ED44E1634EB928660614CBF9CF65E01BCCD72D8D8E`)
- `C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\rp1\rp1-20261012T220000Z-5d2e7b4.err.txt`
  (0 bytes; SHA-256
  `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`)

The output binds run ID `20261012T220000Z-5d2e7b4`, probe SHA-256
`E538FFC2FCC5E38A80E711440AFE4E1BC079E7413832E0BB9A8C4943034CC049`,
PowerShell 5.1.19041.6456, and working directory. The process was interactive,
64-bit, Medium integrity, and not in the administrator role; UAC `EnableLUA=1`
and `ConsentPromptBehaviorAdmin=5`. The displayed privilege list does not
include `SeAssignPrimaryTokenPrivilege`, `SeIncreaseQuotaPrivilege`, or
`SeRelabelPrivilege`. This is context only, not a Low-token execution test.

Windows reported Microsoft Windows 10 Pro, version 10.0.19045, build 19045,
22H2, UBR 6466. Both the base interpreter and `.venv` launcher reported Python
3.11.4 (64-bit); their observed hashes were respectively
`4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F` and
`B5442B36A3855E9A02E5745DB3449D8EC91F4FFEFD9CF92CC8B0535112F0F0CE`. The
`.venv` configuration points to that base interpreter. This establishes the
observed interpreter identities, not low-token launch compatibility.

The repository existed, reported HEAD
`65de223151ff196c72263f79e50719a7b6dbbd07`, and the repository/scripts/venv
paths were reported as ordinary non-reparse directories. S05 displayed ACLs
for the repository, scripts, `.venv\Scripts`, base Python directory and
evidence paths; those displays are not denied-access tests under a Low token.
No mandatory integrity-label line was reported for those S05 target paths.

S06 is explicitly a bounded sample. It exposed Low Mandatory Level labels,
including the `Favorites` path and `AppData\LocalLow` plus sampled children.
It has two `TRUNCATED_LINES` markers (for profile-root and
`AppData\Local` child output). The probe states that the listing is not a
complete Low-writable enumeration and does not evaluate registry
`AppDataLow`; neither effective write access nor complete coverage is
established.

Domain, Private, and Public firewall profiles each reported `State ON` and
`Firewall Policy BlockInbound,AllowOutbound`. These are policy observations
only; network non-use and enforcement are not established. The Job Object API
was not evaluated. RP-1 does not establish U3 handle inheritance, low-token
process-right denial, low-token UI/no-console behavior, or label-at-creation
capability.

## Independent evidence review and disposition

Luna-11 independently reviewed the published contract, probe, and retained
outputs without rerunning or modifying the probe. The source contains
`New-Object` at lines 37 and 99, contradicting contract §3.3's prohibition on
`New-*` commands and its required static scan. The reviewer found the
constructors create in-memory objects and found no evidence of persistent
host mutation from them. Nevertheless, contract §5 assigns a contradiction
`RP1_CONTRACT_DEFECT` and requires return for re-review. The probe's emitted
`RP1_COMPLETE` therefore is not accepted as the final evidence verdict.

### U1-U8 unresolved prerequisites

- **U1:** Low-token process creation is untested.
- **U2:** Low-token interpreter launch, imports, UI restrictions, and no-console
  behavior are untested; only interpreter identity/version were observed.
- **U3:** Launcher handle inheritance is untested.
- **U4:** Denial of specified process rights to a Low process is untested;
  observed ACL displays do not establish it.
- **U5:** Only a bounded sample was observed; complete Low-writable coverage,
  registry `AppDataLow`, and the owner decision on Low-writable locations remain
  open.
- **U6:** Whether labeling can be attached at creation without
  `SeRelabelPrivilege` is untested.
- **U7:** Firewall policy was observed; network non-use and enforcement remain
  unproven.
- **U8:** Remains unprovable under the accepted limit.

The reported token and policy observations do not constitute enforcement
qualification.

## Assumptions, limitations and unresolved issues

The contract's pre-authorization status was superseded only for this single
authorized invocation. Its hash-bound source and contract were not edited.
Independent review found a source/contract discrepancy. The execution is not
accepted as `RP1_COMPLETE_OBSERVED`; its disposition is `RP1_CONTRACT_DEFECT`.
The output retains two bounded S06 line truncations. Memory remains unmeasured
and unenforced. No retry is permitted.

## Reproduction and rollback

Publication and execution were performed against commit
`65de223151ff196c72263f79e50719a7b6dbbd07`; the exact command in contract
§3.1 consumed run ID `20261012T220000Z-5d2e7b4` once. Both output files are
preserved without modification at the paths above. Do not retry or overwrite
them. Do not delete or overwrite unexpected host files.

## Next assignment

Luna-0 routes the `New-Object` contract/source discrepancy for separate owner
decision and review. Do not rerun RP-1 or proceed to RP-2/RP-3. Any future
compatibility gate requires its own owner authorization after this discrepancy
is resolved and the relevant contract/source identities are independently
reviewed.
