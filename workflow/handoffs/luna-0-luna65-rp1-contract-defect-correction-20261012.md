# Luna-0 Luna-65 RP-1 Contract/Source Corrective Reconciliation

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "RP-1 contract/source corrective reconciliation"
  task_id: "L65-PHASE2A-RP1-CONTRACT-DEFECT-CORRECTION"
  component: "Luna-65 Phase 2A RP-1 contract governance"
  status: "complete"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "c05cc6d88cb4aa224e7c53b4b4fe3ca0589bc7e6"
  result_revision: "2a07b1e9f20d758df218981a9a8563c5f953d4b5"
  dependencies: ["Owner governance-only authorization"]
  owner: "Project owner"
  classification: ["governance-only", "historical evidence reconciliation"]
  hypothesis: "Both exact New-Object statements construct only in-memory framework objects and are necessary to the already authorized read-only observations."
  counter_hypothesis: "Either target constructor performs effects outside the approved read-only host-inspection boundary."
  interfaces_relied_on:
    - "Original published RP-1 contract and unchanged PowerShell probe"
    - "Retained RP-1 stdout/stderr for run 20261012T220000Z-5d2e7b4"
  label_information_boundary: ["Host observations remain outside the reusable TPCN core."]
  timing_assumptions: ["No execution or host timing measurement in this governance-only correction."]
  reset_boundaries: ["Original run remains consumed; no retry."]
  resource_bounds: ["Governance review only; no host inspection."]
  authorized_scope:
    - "Verify original publication and evidence identities."
    - "Review exact constructor semantics and prepare a prospective, exact-source amendment to §3.3."
    - "Reconcile observed host facts separately from U1-U8 compatibility requirements."
    - "Obtain independent review; publish governance-only correction only on integrated PASS."
  unauthorized_scope:
    - "Modify or rerun the original probe."
    - "Execute additional host inspections."
    - "RP-2 or RP-3."
    - "Supervisor implementation or qualification."
    - "Phase 2A/2B fixtures, full Spiral, or Luna-64 corrective execution."
  controls:
    - "Preserve original publication commit 65de223151ff196c72263f79e50719a7b6dbbd07 and adjudication commit c05cc6d88cb4aa224e7c53b4b4fe3ca0589bc7e6."
    - "Publish the reviewed governance-only correction as 2a07b1e9f20d758df218981a9a8563c5f953d4b5 and verify the fetched remote."
    - "Do not alter the original probe or retained outputs."
    - "Permit only the two exact reviewed New-Object statements, bound to the original source identity."
  measurements:
    - "Original stdout 66,533 bytes; stderr 0 bytes; reported elapsed 1,347 ms."
    - "Original stdout SHA-256 D5540237E3B6577704DF45ED44E1634EB928660614CBF9CF65E01BCCD72D8D8E."
    - "Original stderr SHA-256 E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855."
  information_boundary_check:
    - "No new host observations or execution are part of this task."
  hardware_mapping: ["not applicable"]
  architecture_invariants_touched: []
  preserves:
    - "Original RP1_CONTRACT_DEFECT verdict."
    - "One consumed invocation and no retry."
    - "All U1-U8 requirements remain unproven."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/docs/luna/LUNA_65_PHASE2A_RP1_HOST_INSPECTION_CONTRACT.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/handoffs/luna-0-luna65-rp1-contract-defect-correction-20261012.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "No executable code or host inspection run."
  assumptions:
    - "Only the original authorized PowerShell source identity is in scope for the precise constructor exception."
  unresolved:
    - "Smallest safe prerequisite and separate authorization for any future RP-2 contract."
  recommended_next_agent:
    - "Luna-0: only after separate owner authorization, prepare a bounded RP-2 contract for independent review; no RP-2/RP-3 execution is authorized."
```

## Provenance and preserved disposition

The expected original repository HEAD was
`c05cc6d88cb4aa224e7c53b4b4fe3ca0589bc7e6`. The RP-1 publication was
`65de223151ff196c72263f79e50719a7b6dbbd07`. At both publication and current
HEAD, the unchanged probe blob is
`2ac7eccd62b0d9d32c15d9f262da47379d38df73` (SHA-256
`E538FFC2FCC5E38A80E711440AFE4E1BC079E7413832E0BB9A8C4943034CC049`), and the
original contract blob is `76d0c07bb432073f9b48c2d55fa7a40eb94a67e3` (SHA-256
`15466F43775455E4B5BABF5A50DD2159322E7DDC6572833A1C69C2107F98152D`).

The invocation for run `20261012T220000Z-5d2e7b4` remains consumed. Its
historical disposition is **`RP1_CONTRACT_DEFECT`**. The probe's emitted
`RP1_COMPLETE` does not replace that independent procedural verdict. The
original probe and stdout/stderr are unchanged by this governance correction.

## Constructor semantics review basis

**Observed source statement, probe line 37:**

```powershell
$psi = New-Object Diagnostics.ProcessStartInfo
```

This resolves to `System.Diagnostics.ProcessStartInfo` with no constructor
arguments. The .NET Framework Reference Source at commit
`ec9fa9ae770d522a5b5f0607898044b7478574a3` defines `public ProcessStartInfo()
{ }`. This allocates the in-memory start-information object only; it does not
start a process, access filesystem/registry state, change Windows settings, or
invoke external code. The later and separate
`[Diagnostics.Process]::Start($psi)` call in `RunNative` starts only the
contract-listed, fixed-argument read-only child executable.

**Observed source statement, probe line 99:**

```powershell
$pr = New-Object Security.Principal.WindowsPrincipal($id)
```

This resolves to `System.Security.Principal.WindowsPrincipal` with the already
obtained `$id` as its sole `WindowsIdentity` constructor argument. In .NET
Framework Reference Source at the same revision, the constructor null-checks
the identity, delegates it to `ClaimsPrincipal`'s in-memory identity
collection, then assigns `m_identity = ntIdentity`. It does not query roles,
start a process, write persistent state, alter token or Windows configuration,
or call an external executable. The subsequent, separately authorized
`$pr.IsInRole(...)` operation performs the read-only current-token role check.

Neither statement uses COM activation. No constructor-invoked external
side-effecting code was found in the reviewed .NET Framework constructor
implementations. These statements are needed by the existing read-only
contract operations: `ProcessStartInfo` configures the fixed child process,
and `WindowsPrincipal` supplies the current-identity role query.

Review sources:

- .NET Framework Reference Source, [`ProcessStartInfo.cs`](https://github.com/microsoft/referencesource/blob/ec9fa9ae770d522a5b5f0607898044b7478574a3/System/services/monitoring/system/diagnosticts/ProcessStartInfo.cs)
- .NET Framework Reference Source, [`WindowsPrincipal.cs`](https://github.com/microsoft/referencesource/blob/ec9fa9ae770d522a5b5f0607898044b7478574a3/mscorlib/system/security/principal/windowsprincipal.cs)
- .NET Framework Reference Source, [`ClaimsPrincipal.cs`](https://github.com/microsoft/referencesource/blob/ec9fa9ae770d522a5b5f0607898044b7478574a3/mscorlib/system/security/claims/ClaimsPrincipal.cs)
- [PowerShell 5.1 `New-Object` documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/new-object?view=powershell-5.1)
- [.NET Framework `ProcessStartInfo` constructor documentation](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo.-ctor?view=netframework-4.8.1)
- [.NET Framework `WindowsPrincipal(WindowsIdentity)` constructor documentation](https://learn.microsoft.com/en-us/dotnet/api/system.security.principal.windowsprincipal.-ctor?view=netframework-4.8.1)

## Prospective §3.3 correction

The modified contract contains a narrowly bound §3.3.1 amendment. It permits
only the two exact statements above, each exactly once, only for the original
probe SHA-256/blob pair. It continues to prohibit every other `New-*` command,
COM activation, unreviewed constructor, source change, and state-changing or
external executable behavior. It explicitly applies prospectively and
preserves the original `RP1_CONTRACT_DEFECT` verdict.

## Retained original evidence and interpretation

The original retained files and hashes are:

- stdout, 66,533 bytes, SHA-256
  `D5540237E3B6577704DF45ED44E1634EB928660614CBF9CF65E01BCCD72D8D8E`
- stderr, 0 bytes, SHA-256
  `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`

The output reports elapsed time 1,347 ms; S00–S08 each have matching BEGIN and
END markers and report `status=OK`; it emits `RP1_COMPLETE`; two S06
`TRUNCATED_LINES` markers are present. No retry occurred.

Observed host facts for diagnostic use only: Windows 10 Pro 22H2, build 19045
(UBR 6466); base and venv Python 3.11.4 interpreter identities and hashes;
interactive 64-bit Medium-integrity process, not in the administrator role;
the displayed privilege listing omits `SeAssignPrimaryTokenPrivilege`,
`SeIncreaseQuotaPrivilege`, and `SeRelabelPrivilege`; ACL displays for
repository/interpreter/evidence targets; sampled Low Mandatory Level labels
including `Favorites` and `AppData\LocalLow`; and Domain/Private/Public
firewall profiles reported ON with `BlockInbound,AllowOutbound`.

These observations do not establish any U1–U8 requirement. In particular,
Low-token process/interpreter launch and UI behavior, denied process rights,
handle inheritance, Job Object runtime behavior, full Low-writable coverage,
label-at-creation capability, network non-use/enforcement, and U8 remain
unproven. The S06 sample is incomplete by design and its two truncated listings
further bound interpretation. The original procedural verdict remains
**`RP1_CONTRACT_DEFECT`** regardless of any prospective amendment acceptance.

## Independent review and publication gate

Independent review A–D was completed read-only by Luna-11 Adversarial
Architectural Verification on 2026-10-12. Integrated verdict:

**PASS — RP-1 CONTRACT DEFECT RECONCILED FOR FUTURE USE**

The reviewer accepted the exact constructor semantics (A), prospective
source/hash/blob-bound exception and continuing read-only boundary (B),
original evidence integrity and non-enforcement interpretation (C), and
provenance, scope, and historical preservation (D). The reviewer confirmed
that the plain diff-check warning was solely the existing CRLF checkout
behavior; `git -c core.whitespace=cr-at-eol diff --check` passes. The three-file
governance-only allowlist was eligible for publication using that CRLF-aware
check. At review completion, publication was still pending.

The reviewed dimensions were:

- **A:** Exact constructor semantics and side effects, against the framework
  reference implementations and bound probe statements.
- **B:** Whether §3.3.1 is sufficiently exact and preserves the read-only
  boundary without creating a general `New-*` exception.
- **C:** Integrity and interpretation of the retained original outputs,
  including classification and scientific/enforcement limits.
- **D:** Provenance, authorization boundaries, historical preservation, and
  whether the correction is strictly governance-only.

Integrated verdict must be exactly one of:

- `PASS — RP-1 CONTRACT DEFECT RECONCILED FOR FUTURE USE`
- `BLOCKED — RP-1 CONTRACT DEFECT UNRESOLVED`

No changes are made to the original probe. On BLOCKED, preserve the findings
without claiming a resolution. Even on PASS, the original run remains
`RP1_CONTRACT_DEFECT`; RP-1 is consumed, and RP-2/RP-3 remain unauthorized.

## Governance-only publication verification

The reviewed three-file allowlist was committed as
`2a07b1e9f20d758df218981a9a8563c5f953d4b5` and pushed to
`origin/governance/luna64-r4.3-freeze-20261010`. A subsequent fetch confirmed
the remote branch resolves to the same commit. Local and fetched remote trees
match for the contract (`e0baff6c0229303f1a04c2a5ce21eea434099e20`), workflow
(`134d27412ee9d4e67e07130dd237ad13a5aee262`), and corrective handoff
(`9d32af939eb2fc1ab60f145f7a0bcbe2c72df9cd`).

This publication reconciles the contract prospectively only. It does not
change the original `RP1_CONTRACT_DEFECT`, authorize another RP-1 invocation,
or authorize RP-2/RP-3 execution.

## Smallest remaining prerequisite

For a separately authorized RP-2 contract, obtain separate owner authorization
to prepare and independently review a distinct bounded RP-2 contract for the
specific runtime-compatibility questions RP-1 did not test, including Low-token
process/interpreter launch and handle inheritance. RP-2 execution requires its
own explicit owner authorization; this handoff grants none.
