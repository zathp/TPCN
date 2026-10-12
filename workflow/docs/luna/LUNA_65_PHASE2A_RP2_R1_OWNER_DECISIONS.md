# Luna-65 RP-2 R1 owner-decision closure

**Gate:** `L65-PHASE2A-RP2-R1-OWNER-DECISION-CLOSURE`
**Date:** 2026-10-12
**Status:** Owner decisions accepted for synthetic diagnostic DESIGN only.
Governance publication authorized subject to exact-byte package verification.
RP-2A implementation and RP-2B execution NOT AUTHORIZED.

## 1. Authority and immutable design identity

The project owner's current instruction explicitly adopts D-RP2-DIRECT-1,
D-RP2-MEDIUM-1 and D-RP2-OUTER-1 for this diagnostic design.
This record prospectively changes their decision status, not the reviewed
technical design or historical bytes. The owner's instruction is the approval
source; an agent verdict is not owner acceptance.

Expected baseline, observed HEAD and fetched governance remote before
publication: `45121227d96c6fa13357c6bdf5fba0d99d8d7352`.
Branch `governance/luna64-r4.3-freeze-20261010`; initial index empty.

The accepted technical dependency is the unchanged
[R1 contract](LUNA_65_PHASE2A_RP2_OUTER_LAUNCHER_CORRECTIVE_R1.md):

| Representation | Identity |
|---|---|
| Reviewed checkout SHA-256 (CRLF) | `F9913AC44C268291988F549A110B2EFCC4777139A2BB8BD0DA407DF020FABEFB` |
| Raw CRLF Git blob | `7c6c5113494604b1f2f9494c4ab207c8d3705226` |
| Git-clean LF blob | `8abb50dfef732da71cee94b1623c61b3f4f8e49e` |

Its four same-checkout independent reviews returned
**PASS - RP-2 DIRECT CONTRACT READY FOR OWNER DECISION**.
See the immutable [R1 handoff](../../handoffs/luna-0-luna65-rp2-outer-launcher-corrective-r1-20261012.md)
for A-D results and reviewer interpretation limits.
That handoff checkout SHA-256 is
`996D81FDD720257C728321FEF65BDFB00D272782F6AADA2D8B7C69385F1D7E3F`.
This acceptance record governs decision status where historical R1 section 7
says proposed/unaccepted; it does not rewrite those historical statements.

## 2. Decision reconciliation

### D-RP2-DIRECT-1 - ACCEPTED FOR DIAGNOSTIC DESIGN

Permit only the frozen base
`C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe`,
SHA-256 `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F`,
Python 3.11.4 AMD64. Preserve Low restricted primary token, suspended
CreateProcessAsUserW, explicit X-L process/thread descriptors, three Low
pipe writes, exact four-variable environment and reviewed synthetic-workload
specification. No implemented literal/hash is falsely claimed to exist.
Do not substitute another interpreter, change the literal behavior or install
dependencies to manufacture feasibility.

Acceptance corresponds to the preserved direct candidate section 8 and R1
section 7 dependency. It neither replaces production venv Python nor proves
production pytest, root-to-base forwarding, venv internal job or environment/
startup compatibility. Those remain independent prerequisites.

### D-RP2-MEDIUM-1 - ACCEPTED FOR DIAGNOSTIC DESIGN

Existing non-elevated Windows PowerShell 5.1 is attended outer O. Reviewed
CreateProcessW creates suspended Medium probe P under its existing security
context, with NULL process/thread security attributes and ordinary Windows-
issued descriptors. No custom X-M or OWNER RIGHTS denial is required for
P/initial thread. Preserve complete pre-resume descriptor/token readback,
image verification, PID plus creation time and retained creation-returned
process/thread handles; operational masks 0x00121401 and 0x00120042.

Two Medium capture streams and O-controlled sole diagnostic evidence writing
are accepted exactly as R1 sections 3-4 and section 7 propose. Preserve the
single-writer, all-representation 1 MiB aggregate ceiling and failure reserve.
L still has explicit Low SDs and only three inherited Low-pipe writes.
No new privileges, elevation, security repair, ACL modification or Low-to-
trusted-process ACL-denial/U4/U6 claim. Production B-min W/P unchanged.

### D-RP2-OUTER-1 - ACCEPTED WITH EXPLICIT DIAGNOSTIC LIMITATIONS

For this bounded synthetic diagnostic only, O independently observes/stops
P, not L after P loss. P keeps sole nonduplicated unnamed job ownership.
Preserve one Medium invocation, one trusted-parent Low creation attempt,
zero retries, 10 s active, <=5 s cleanup, 20 s outer deadline, and at most
one TerminateProcess request through the exact retained P handle.
Bounded waits and observed exit/EOF matter; a successful request is not proof.

On missing required Low cessation evidence, report
**RP2_UNKNOWN_FAIL_CLOSED**, never RP2_PASS. The outer verdict/diagnostic must
explicitly alert the attending operator: containment remains unresolved;
an unconfirmed Low child/descendant may still be active. Do not silently
advance to RP-3, supervisor work or fixtures. If O is itself unavailable,
the incomplete/absent terminal record cannot be interpreted as success;
the attended protocol requires operator recognition of unresolved status.

This notification makes explicit the already-reviewed R1 UNKNOWN/attended
stop boundary; it adds no recovery authority, extra attempt, deadline extension
or new containment guarantee. R1 section 5 remains authoritative for its
failure races. A surviving unobserved Low process may outlive the deadline.
Acceptance is not approval of that behavior for production B-min.

## 3. B01, token access and unqualified envelope preserved

SeChangeNotifyPrivilege present and ONLY enabled Low-child privilege; other
entries may remain disabled; complete LUID/name/attribute readback required.
Unexpected enablement fails. Preserve DISABLE_MAX_PRIVILEGE, Low 4096,
policy NO_WRITE_UP | NEW_PROCESS_MIN = 3 readback without repair, frozen
group rules, no restricting SIDs, no source-token adjustment or impersonation.

R1 section 6 token-object matrix is preserved, including source mask 0x2008B
because CreateRestrictedToken returns input-handle rights. Actual token-object
owner/DACL/label observed and checked, not inferred from TokenUser or contained
IL. No token SD edits or privileged fallback.

64 MiB proposed job-memory charge, eight-process safety backstop, five-second
job user-time, 1 MiB logical evidence, one invocation and zero retries remain
unqualified/unexecuted. No TPCN, E2, fixture, dataset or scientific workload.
No A01-A15 or ACP/core change; no hardware-equivalence claim.

## 4. Narrow governance publication allowlist

Exactly these ELEVEN paths, no source/configuration files:

1. `workflow/docs/luna/LUNA_65_PHASE2A_RP2_RESTRICTED_TOKEN_COMPATIBILITY_CONTRACT.md`
2. `workflow/docs/luna/LUNA_65_PHASE2A_RP2_DIRECT_INTERPRETER_DESIGN.md`
3. `workflow/docs/luna/LUNA_65_PHASE2A_RP2_OUTER_LAUNCHER_CORRECTIVE_R1.md`
4. `workflow/handoffs/luna-0-luna65-rp2-contract-preparation-20261012.md`
5. `workflow/handoffs/luna-0-luna65-rp2-b01-b02-correction-20261012.md`
6. `workflow/handoffs/luna-0-luna65-rp2-direct-interpreter-review-20261012.md`
7. `workflow/handoffs/luna-0-luna65-rp2-outer-launcher-corrective-r1-20261012.md`
8. `workflow/docs/luna/LUNA_65_PHASE2A_RP2_R1_OWNER_DECISIONS.md`
9. `workflow/docs/luna/LUNA_65_PHASE2A_RP2A_IMPLEMENTATION_AUTHORIZATION_CANDIDATE.md`
10. `workflow/handoffs/luna-0-luna65-rp2-r1-owner-decision-closure-20261012.md`
11. `workflow/docs/luna/LUNA_WORKFLOW.md`

Items 1-7 publish unchanged historical dependencies/reviews; their BLOCKED
or then-pending status remains intact. Item 11 preserves its existing two
historical RP-2 entries and adds this prospective closure only. Publishing
these dependencies prevents dangling authoritative links on the remote.
No historical source or verdict is retroactively approved by inclusion.

Excluded untracked supervisor SHA-256
`67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`;
excluded S1-B final authorization record
`BB9134CB7FF1813D495575FA80F912EEFB6E6A7C7A86F720CDAD829CAC925451`.
Probe and proposed outer-wrapper sources remain absent/untouched.

Before commit: independent package reconciliation, full path allowlist,
checkout hashes/raw and Git-clean blobs, stage/line-ending verification.
Keep R1 checkout bytes unchanged; text normalization changes Git storage
to LF, not semantic requirements. Workflow is -text and remains raw CRLF.
No .gitattributes change. Push normally to the existing authorized governance
branch, fetch it and compare exact commit and all published blobs.
Publication identities are reported after actual publication, never invented
inside the commit that they would identify.

## 5. Next gate and unchanged prohibitions

The [RP-2A authorization candidate](LUNA_65_PHASE2A_RP2A_IMPLEMENTATION_AUTHORIZATION_CANDIDATE.md)
is a request for a SEPARATE owner grant, not granted here. Design-policy closure
removes pending owner decisions; source/static-review bindings and host/runtime
feasibility remain future work. No implementation-readiness claim substitutes
for publication verification or RP-2A source authority.

RP-2A implementation, RP-2B execution, RP-3, supervisor implementation/
qualification and Phase 2A/2B fixtures NOT AUTHORIZED. Full Spiral and Luna-64
corrective execution BLOCKED. Luna-63C FROZEN. No compatibility invocation
consumed and no new run ID, evidence directory, token or job created.
