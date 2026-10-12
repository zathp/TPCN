# Luna-65 Phase 2A RP-2 Restricted-Token Compatibility Contract

**Gate:** `L65-PHASE2A-RP2-CONTRACT-PREPARATION`
**Date:** 2026-10-12
**Status:** BLOCKED - RP-2 CONTRACT INCOMPLETE; four-lane review completed.
Compatible post-review clarifications below are an unreviewed candidate,
not a reviewed PASS or implementation/execution authorization.
The B01/B02 correction candidate in section 10 governs the current review;
sections 1-9 preserve the preceding draft and its historical BLOCKED findings.

## 1. Scope, provenance, and publication boundary

Baseline is `45121227d96c6fa13357c6bdf5fba0d99d8d7352` on
`governance/luna64-r4.3-freeze-20261010`, equal to its upstream at preparation.
Git ancestry checks succeeded for S1-B corrected verification
`948f5e70a43a3524dfef6bbe8f04bbd041770fd6`, RP-1 publication
`65de223151ff196c72263f79e50719a7b6dbbd07`, RP-1 adjudication
`c05cc6d88cb4aa224e7c53b4b4fe3ca0589bc7e6`, and prospective correction
`2a07b1e9f20d758df218981a9a8563c5f953d4b5`.

The finalized RP-1 corrective handoff has blob
`bd0a457045fadeb2bc817ff7a080bbe8374eb5a0` and CRLF checkout SHA-256
`4537ADD62A7037713F3F3E7FF14A15B43FE8537E327540C610AB59B32A4C8861`.
The unchanged RP-1 probe has blob
`2ac7eccd62b0d9d32c15d9f262da47379d38df73` and SHA-256
`E538FFC2FCC5E38A80E711440AFE4E1BC079E7413832E0BB9A8C4943034CC049`.
The original invocation `20261012T220000Z-5d2e7b4` remains consumed with
historical verdict **RP1_CONTRACT_DEFECT**. No RP-1 inspection is repeated.

Authoritative D-R7-4 input is
[R7 owner decisions and profiles](LUNA_65_PHASE2A_R7_OWNER_DECISIONS_AND_PROFILES.md)
sections 3, 4.1-4.5, and 6.1: blob
`0759087811610f40c73de91d8662c28d8ebce54d`; LF blob SHA-256
`6C5EBFD955EFDF472897B18E0126E83C85AFF56AE98BA5BE0D5D3564EF984671`;
CRLF checkout SHA-256
`9CA2E34DCC1F35BA72156B86C889365C2EB6873979E7863248594AF214169B73`.
[R7 readiness](LUNA_65_PHASE2A_R7_PREIMPLEMENTATION_READINESS.md) sections
3 and 5 supplies the unresolved U1-U8 matrix and candidate RP-2 envelope,
not authorization. Historical evidence is diagnostic, not an enforcement PASS.

No architecture clause or ACP changes. No supervisor, watchdog, neuron,
fixture, benchmark, dataset, or training behavior is implemented or executed.
The untracked supervisor and S1-B authorization record remain untouched.

Conditional governance publication allowlist is exactly this contract,
`workflow/handoffs/luna-0-luna65-rp2-contract-preparation-20261012.md`,
and `workflow/docs/luna/LUNA_WORKFLOW.md`. Integrated BLOCKED means retain
draft findings without publishing a PASS. Do not amend prior commits.

## 2. Frozen profile: requirements, not newly observed host facts

| Field | Exact R7 requirement and RP-2 treatment |
|---|---|
| User | `DESKTOP-AFORJRI\Patrick`, SID `S-1-5-21-3301679920-2322392626-2066554248-1001`; source primary token from the invoking filtered, non-elevated, same-session Medium account. Refuse mismatches; do not invent a portable identity. |
| Launcher privileges | `SeChangeNotifyPrivilege` may be enabled; every other present privilege disabled. Refuse if any of `SeDebug`, `SeAssignPrimaryToken`, `SeIncreaseQuota`, `SeTcb`, `SeImpersonate`, `SeBackup`, `SeRestore`, `SeTakeOwnership`, `SeLoadDriver` is present in any state. Use the full `...Privilege` names in evidence. No enabling, elevation, credentials, impersonation, or adjustment of the launcher token. |
| Derived primary token | `CreateRestrictedToken` from that primary token, flags exactly `DISABLE_MAX_PRIVILEGE`; then `SetTokenInformation(TokenIntegrityLevel)` to `S-1-16-4096`. Not an impersonation token, AppContainer, alternate user, or `LUA_TOKEN` substitute. |
| Groups | Enumerate actual source groups; disable every group except user SID, Everyone `S-1-1-0`, BUILTIN\Users `S-1-5-32-545`, Authenticated Users `S-1-5-11`. Do not add absent groups or enable a source deny-only group. Preserve the user as enabled, not deny-only. Record source and derived SID/attribute pairs, including integrity-labelled entries, and any API rejection. |
| Restricting SIDs | Empty, by design; `RestrictedSidCount=0`, no `SidsToRestrict`. No `RESTRICTED` SID replacement or new ACL grants. Restriction is deny-only groups/privileges plus MIC, not a second restricting-SID access check. |
| Integrity/policy | Low RID 4096; `TokenMandatoryPolicy` must read back `NO_WRITE_UP | NEW_PROCESS_MIN` (3). Never silently repair mandatory policy or raise integrity. |
| Workload privileges | R7 says `SeChangeNotifyPrivilege` retained and read back as the **only privilege**, and all others explicitly disabled. This literal requirement is subject to blocker B01 below; no extra removal step is assumed. |
| Interpreter | `C:\Users\Patrick\Documents\ActiveCode\TPCN\.venv\Scripts\python.exe`, SHA-256 `B5442B36A3855E9A02E5745DB3449D8EC91F4FFEFD9CF92CC8B0535112F0F0CE`; base `C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe`, SHA-256 `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F`; Python 3.11.4, 64-bit. Verify the launcher/base chain; never bypass the launcher on failure. |
| Production arguments | R7 adds `-B` and `-p no:cacheprovider` to `-m pytest -q -x tests/test_luna65_capacity_direct.py`. That absent fixture must not be created or run here. RP-2 substitutes only `-B -c <fixed reviewed synthetic literal>`; no `-I` (would ignore PYTHONHASHSEED), no `-m pytest`, tests, or plugin discovery. This synthetic substitution must be expressly accepted in RP-2A/RP-2B, not represented as the production invocation. |
| Child environment | Exactly `PYTHONHASHSEED=0`, `TPCN_LUNA65_LEDGER_HANDLE=<decimal inherited ledger write handle>`, `PYTHONDONTWRITEBYTECODE=1`, `SYSTEMROOT=<verified host SystemRoot>`. Unicode block, explicitly built and terminated; all other variables absent, including PATH, TEMP, TMP, USERPROFILE, LOCALAPPDATA, PYTHONPATH and evidence path. No variable added on startup failure. |
| Working directory | `C:\Users\Patrick\Documents\ActiveCode\TPCN`; no relocation to a disposable directory as a workaround. |
| Inheritance | Only stdout write, stderr write, and ledger write anonymous-pipe handles; exact `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`, `bInheritHandles=TRUE`. Every other owned handle non-inheritable; explicit `STARTF_USESTDHANDLES`, stdout/stderr assigned, stdin NULL (no fourth handle). Verify actual stdin state; failure is not repaired with a file/pipe. Close parent copies of the three child ends before resume. |
| No-console/UI | `DETACHED_PROCESS`, not `CREATE_NEW_CONSOLE` or an assumed equivalent; `CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT | EXTENDED_STARTUPINFO_PRESENT`. All eight UI bits from R7: HANDLES, READCLIPBOARD, WRITECLIPBOARD, SYSTEMPARAMETERS, DISPLAYSETTINGS, GLOBALATOMS, DESKTOP, EXITWINDOWS, mask `0xFF`, configured/read back on the probe job. HANDLES refers to USER handles, not kernel pipes. No attempt to modify clipboard/display/desktop/system state. |
| Permissions | Existing interpreter/library/repository read and execute permissions only, no ACL edits. R7 relies on default Medium objects and Low NO_WRITE_UP, but RP-1 displayed ACLs, not effective-access tests. No child file-write permission granted, no TEMP/TMP. Existing Low-writable locations and network access remain uncontained; U4-U8 stay open. |
| Process/thread descriptors | R7 says parent creates them and retains full access, with no ACE granting workload-side principals. Their exact realization is blocker B02; do not substitute a default descriptor or invent an SDDL. |

### 2.1 Mandatory governance blockers before RP-2A

**B01 - privilege semantics conflict.** Microsoft documents
`DISABLE_MAX_PRIVILEGE` as disabling all privileges except
`SeChangeNotifyPrivilege`, not promising deletion of their token entries.
The observed source token has disabled Shutdown, Undock, IncreaseWorkingSet,
and TimeZone privileges. R7's "only privilege" readback is stronger than its
specified construction and differs from "only enabled privilege".
Neither reinterpretation nor `AdjustTokenPrivileges` deletion nor a second
`CreateRestrictedToken` operation is authorized here. Owner/profile review
must resolve the exact invariant and approved construction before source
implementation. A literal readback mismatch is failure, never PASS.

**B02 - child security descriptor specificity.** R7 gives the parent and child
the same user SID while requiring parent access and no ACE for workload-side
principals. The enabled user SID is present in both. The source profile does
not supply a concrete process/thread descriptor or state whether its exclusion
means no child-specific ACE versus no same-user ACE. MIC's access-check
distinction cannot silently reinterpret the DACL term or establish U6.
A separately reviewed exact descriptor/access plan is needed. This is not
proven impossible: the parent can retain the full-access creation-returned
root handle without a same-user allow ACE. The plan must also cover acquiring
the base interpreter's query/duplicate/wait handles without an impermissible
same-user grant, reopening workaround or security modification. R7 already
specifies labels on W/P; merely specifying a compatible descriptor is not
automatically a profile change. Escalate only if the literal exclusion cannot
be honored. RP-2 cannot quietly weaken it, add a relabel privilege, or claim
U4/U6. Exact owner/DACL/label and required access are still unresolved here.

These are preparation findings, not observed runtime incompatibilities.
The contract is BLOCKED for an implementation decision while either is open.
Missing `SeIncreaseQuotaPrivilege` and `SeAssignPrimaryTokenPrivilege`,
venv ledger forwarding, no-variable imports, creation-time job/UI compatibility,
and snapshot/access availability are instead experimental feasibility questions:
do not assert they are achievable from the Medium account without results.

## 3. Intended U1-U3 design after blockers and separate authorizations

This sequence is a proposed single experiment, not executable instructions.
No source or run ID is frozen by this preparation.

1. Future preflight binds commit, reviewed probe and embedded-child literal
   hashes, both interpreter hashes, R7 profile, exact outer command, fresh
   run ID, paths, and attended operator. Verify no unreviewed tracked changes,
   no existing destination, and source/token host identity without broad host
   enumeration. A failure before the authorized invocation means not consumed.
2. Within the one invocation, read launcher token fields with
   `OpenProcessToken`/`GetTokenInformation`: User, Type, Groups, Privileges,
   IntegrityLevel, MandatoryPolicy, RestrictedSids, Elevation, SessionId.
   Bound each query allocation to 64 KiB and 256 entries; exhaustion is
   explicit incomplete evidence, never a truncated PASS.
3. Create an unnamed probe-only job, non-inheritable. Set/read back kill-on-close,
   no breakaway, job-memory 67,108,864 bytes, active-process ceiling 8, user-time
   backstop 5 seconds with TERMINATE_AT_END_OF_JOB, and UI mask 0xFF.
   No B-min controller/watchdog is implemented. Detect ambient job membership;
   inability to nest with these limits is a compatibility failure, not reason
   to use breakaway or post-creation assignment.
4. Create three anonymous pipes (`CreatePipe`, `SetHandleInformation`).
   Read ends non-inheritable; only three write ends inheritable. Create one
   unnamed, inert event as an inheritable negative-control sentinel, expressly
   omitted from the handle list. It is not a child input or synchronization
   channel. Inventory the launcher's handles before creation, keep
   non-inheritable object-reference duplicates for comparison, cap 256 entries.
   No references to unrelated processes or user files are acquired.
5. Construct/read back the frozen derived token, distinct from creation
   success. Token handle requires QUERY, DUPLICATE, ASSIGN_PRIMARY and
   ADJUST_DEFAULT for Low label setting. Do not adjust launcher privileges.
   Apply the literal group rule to every TokenGroups entry, including an
   entry flagged SE_GROUP_INTEGRITY if returned; do not silently filter such
   an entry out. Record any rejection, then independently query the resulting
   TokenIntegrityLevel and MandatoryPolicy. A different group treatment needs
   profile review, not a source workaround.
   Build the exact environment and `STARTUPINFOEXW` attributes
   HANDLE_LIST=[three writes], JOB_LIST=[probe job].
6. Make **one** `CreateProcessAsUserW` call using the absolute venv executable,
   mutable correctly quoted command line, reviewed process/thread descriptors,
   and flags in section 2. No alternative API, base-interpreter fallback,
   credentials, second creation call, or retry. Capture return/error immediately.
7. On creation success, keep the root/thread handles. While root is suspended,
   confirm job membership, image, token, and complete bounded handle inventory.
   Close parent copies of child write ends, verify closure and read-end
   inheritance flags. Any mismatch terminates without resume.
8. Resume once only after checks. The only accepted R7 topology is root venv
   image/PID followed by a distinct base-image/PID whose parent is that root,
   argv is the frozen synthetic argv, and READY reports that base PID.
   The base process must have the bound base image and Python 3.11.4 identity.
   An unexpected single-process topology is a profile mismatch, not an
   alternative successful interpretation. An expected chain that cannot be
   observed completely remains incomplete; never infer it from sys.executable.
   Continuously drain all three streams through
   bounded readers; poll job membership/process identity and CPU/memory every
   25 ms nominally. Acquire exact handles only for probe-job members; PID plus
   creation time/image binds identity, not bare PID. Record final base
   interpreter identity/token, not only the venv launcher's token.
9. Synthetic child emits a READY record with PID and standard/ledger handle
   values, then spends a fixed two seconds in sleep to permit one final
   interpreter handle snapshot. This is best-effort observation, not a
   synchronization guarantee: missing the window is PARTIAL, no second child.
   No new inherited control handle, polling file, or environment variable.
   Order is: all allowed imports and read-only observations, one READY on each
   stream, two-second dwell, then one END on each stream, close, exit zero.
   Capture once after the parent receives all three READY records and before
   END. If the window is missed, no repeat capture to manufacture success.
10. Require child/root exit status, zero active job members, all three EOFs,
    closed references, timings, cleanup outcomes. Finalize once; no restart.

### 3.1 U3 evidence beyond successful capture

Use documented Process Snapshotting: `PssCaptureSnapshot` with
`PSS_CAPTURE_HANDLES | PSS_CAPTURE_HANDLE_BASIC_INFORMATION` only,
`PssWalkMarkerCreate`, `PssWalkSnapshot(PSS_WALK_HANDLES)`, marker free and
`PssFreeSnapshot`. No VA clone, process dump, memory scanning, system-wide
handle enumeration, snapshot clone process, or breakaway flags. Bound
enumeration to 256 handles per snapshot, parent/root/final only.
The capture allocation occurs before the walk cap can be checked. That cap
does not hard-bound PSS or parent memory; record this accepted observation
limitation, and cap overflow makes evidence incomplete, not PASS. No VA
capture is permitted to obtain a stronger memory/handle assertion.

Compare independently held references using `DuplicateHandle` from the exact
probe-owned process and `CompareObjectHandles`, with no DUPLICATE_CLOSE_SOURCE.
Require all three expected pipe objects, values, and flags. Record every
parent-object match outside the allowlist (especially sentinel, job, token,
read ends, evidence files, and process handles) as unintended inheritance.
`PSS_HANDLE_ENTRY.GrantedAccess` is documented as OS-reserved: it alone is
**not** proof of access rights. RP-2A must independently review a precise
ABI before using the following method: dynamically resolve `NtQueryObject`
from the system `ntdll.dll`; query `ObjectBasicInformation` on same-access,
non-inheritable duplicate references using the documented 56-byte
`PUBLIC_OBJECT_BASIC_INFORMATION` (four 32-bit fields then ten reserved
32-bit fields). Record NTSTATUS, returned length, Attributes and GrantedAccess;
never interpret reserved fields. Compare granted masks with the original
parent pipe ends and require write-data, not read-data access. Use
`GetHandleInformation`/snapshot attributes for the original inheritance flags,
not the duplicate's flags. Microsoft warns NtQueryObject may change or be
removed: failed resolution, ABI/length mismatch, incomplete query or inability
to duplicate a handle makes U3 incomplete, never PASS or a fallback.

The root snapshot before resume distinguishes inheritance from runtime opens.
The final interpreter snapshot must reconcile objects with the parent inventory
and classify newly opened runtime objects separately. A full bounded snapshot
and sentinel absence at READY is evidence only at that checkpoint, not proof
that a transient handle never existed or that arbitrary future workloads
inherit nothing. If identities/rights cannot be established, cap exceeded,
access denied, or chain missed, mark U3 PARTIAL. Successful stdout capture is
never a substitute. Inspectable source and inventory explain the finite claim.

## 4. Smallest proposed synthetic Python workload

One fixed child literal embedded in the proposed probe; no generated script
or production fixture. Exact literal bytes, quoting and dependency closure
must be independently frozen at RP-2A and named by RP-2B.

Allowed direct imports: `sys`, `os`, `json`, `ctypes`, `ctypes.wintypes`,
`time`, `msvcrt`, and `pytest` (import/version only, no pytest invocation,
collection, entry-point/plugin loading or TPCN imports). RP-2A reviews the
installed dependency/import closure and freezes an allowed module-origin
and content-identity manifest. Include Python startup before the literal:
site initialization, all applicable .pth executable lines and data, potential
sitecustomize/usercustomize and user-site resolution, repository-cwd import
precedence, and transitive pytest imports. Bind the complete effective search
path, hook/dependency contents and approved absence where applicable; origins
alone are insufficient. Verify that closure in RP-2B preflight before any
invocation is consumed. Unresolved side effects or drift block execution,
not an implicit -S/-I/environment workaround. No package
installation or broad user-data reads. Imports prove only this synthetic
closure, not the absent production fixture's future imports.

The literal reads its four-variable environment, versions/executable/prefixes,
module origins, PID; calls read-only token/standard-handle/console APIs
through ctypes; writes distinct fixed ASCII nonce-tagged READY/end records
directly to stdout, stderr, ledger using `WriteFile`; sleeps two seconds;
closes its handles and exits zero. It performs no other file open/write,
network, child creation, token adjustment, GUI action, dataset access,
TPCN import, E2 allocation, training, or benchmark. No arbitrary code, path,
or command is accepted as an argument.

Console evidence: `GetConsoleWindow`, `GetConsoleCP`, and console-mode
queries on std handles with exact error/results. NULL/zero/pipe handles are
reconciled with creation flags; GetConsoleWindow alone is not proof.
UI evidence is job membership and effective 0xFF readback plus static absence
of UI operations, not destructive testing of UI restrictions.

RP-2A must freeze the exact ASCII record grammar, bytes/count/order and
nonce binding separately for stdout, stderr and ledger: exactly one READY
and one END per stream, no other child output, same base PID and run nonce,
observations satisfying the bound manifest. No missing, duplicated, reordered,
extra or truncated record may PASS. Fixed diagnostics caused by import
failure are retained as failure evidence, not accepted success output.

The four-variable block above is the workload block only. The probe is not
W or P and does not implement their environment/heartbeat design. R7's text
that W/P use "the same allowlist" is retained, not silently rewritten into a
new parent environment. Its process-local ledger-value meaning still needs
an exact separately reviewed controller interpretation; no W/P environment
compatibility is claimed. RP-2B must bind the probe/outer invocation environment
independently, prohibit inheritance of that block into the child, and retain
the exact four-variable child block. This distinction is not permission to
expand the workload allowlist.

No child-created files and no disposable child directory are needed.
Only the Medium probe writes its new evidence leaf: candidate
`C:\Users\Patrick\AppData\Local\TPCN\evidence\luna65\rp2-<frozen-run-id>`.
RP-2B must approve one fully resolved fresh leaf and files, verify existing
parents and all reparse/redirection components, and allow leaf creation only.
No recursive parent creation, ACL/integrity-label edit or deletion of existing
content. Retain evidence; cleanup removes only in-memory objects/handles.
Any future evidence deletion requires separate explicit authority.

## 5. Independently justified resource and cleanup envelope

| Bound | Proposed RP-2 envelope and enforcement status |
|---|---|
| Attempts | One attended probe invocation; one CreateProcessAsUserW attempt; one permitted venv-to-base chain; zero retries of invocation, token repair, child creation, or fallback. Internal bounded observations are not retries of the experiment. |
| Active wall | 10 seconds from probe entry, monotonic. At deadline stop admission/output and request job termination. Covers small setup, no-op imports, two-second snapshot dwell, exit. A slow host produces incomplete/failure evidence, not an extended run. |
| Outer supervision | 20 seconds from outer start: 10 active + at most 5 cessation/drain + 5 wrapper overhead. Attended stop of exact probe PID/creation identity at outer deadline; no name-based killing. Best-effort, no hard real-time guarantee. Stop request and last/first cessation observations retained. |
| CPU | Sample job user+kernel time and probe GetProcessTimes; measured seconds, not neural energy. Job user-time 5-second supplementary backstop only, not kernel/aggregate CPU enforcement. Probe and outer wrapper CPU not enforced; samples can miss peaks. |
| Memory | Job-memory charge hard configured at 64 MiB (candidate RP-2 bound, not S1-B nor B-min 256 MiB). Small startup/import workload only; API readback required. Record peak job charge and probe working set/private usage when queryable. Parent/snapshot allocations outside job not hard bounded by OS; caps bound retained buffers, not whole process memory. |
| Processes | Job active-process limit 8, no breakaway, kill-on-close. Only root plus expected base interpreter may be observed; any other member fails. Ceiling is a safety backstop, not permission for six extra processes. Membership/no-breakaway readback is not full supervisor qualification. |
| Output | Aggregate all files, stdout, stderr, ledger, report and intermediates <=1,048,576 logical bytes while retained. Reserve 131,072 bytes for failure/finalization; streaming payload at most 917,504 bytes. No whole-stream buffering. Individual record <=16,384 bytes, inventories <=256 entries, token buffers <=64 KiB. Ceiling enforcement is probe/wrapper source-level, not filesystem quota; peer same-user writes out of boundary. |
| Overflow | Stop retaining payload, record counted/discarded bytes within reserved budget, request termination, bounded drain/discard; overflow/inventory truncation never PASS. Capture wrapper stdout/stderr into the same accounted budget, not uncounted redirections. Failure of evidence writing makes evidence incomplete. |
| Cleanup | On any post-creation failure, TerminateJobObject; for exact suspended root not confirmed in job, TerminateProcess(root) before any resume; wait on owned handles, re-read active job count, drain all three pipes to EOF, close duplicates/snapshots/marker/token/thread/process/pipes/event/job. No broad process enumeration or kill. |
| Cessation | At most five seconds after termination request for observation/drain. Job termination or kill-on-close success is a request, not cessation proof. Require zero active job count plus signaled retained process handles and pipe EOF; missing observation, failed wait, outstanding readers/writers, leaked handle, probe loss or uncertain child state fails closed. |

Independent design rationale, not measured timing: allocate the ten active
seconds as two for bounded preflight/setup/token/job/pipe queries, four for
launcher/base startup and the small static import closure, two for the
declared snapshot dwell and two for snapshot/exit observations. These
allocations motivate a small test rather than a sizing/benchmark budget and
are not stage extensions or feasibility guarantees. The five cleanup seconds
permit bounded termination/wait/drain on three small streams, not guaranteed
Windows termination latency. The outer five-second overhead allowance covers
entry/exit and bounded finalization; no assumed timer precision.

Let O be outer start, T probe entry, F the first normal terminal observation
(expected root exit and job-zero) or first failure/termination request. All
successful drain, handle closure and finalization must finish by the earliest
of F+5 seconds, T+15 seconds and O+20 seconds. Active admission/observations
stop by T+10 or O+20, whichever comes first. If normal completion is not
observed by the active cutoff, request termination and enter cleanup then.
Wrapper overhead consumes the outer allowance; it never moves O+20.
Early operator stop uses the same bounded cleanup without extending any
deadline. Missing EOF/cessation at the earliest deadline is UNKNOWN_FAIL_CLOSED;
confirmed cessation but incomplete finalization is at least PARTIAL.

One output accounting model counts the logical lengths of every retained
representation/file at the same time, including encoded raw stream files,
wrapper capture, structured evidence and temporary/final copies. Pipe bytes
not retained do not consume the artifact ceiling but their read/discard
counters are evidence. If raw bytes are also copied into a report, both
representations count while both exist; do not count raw input once as proof
that all representations fit. Single-writer accounting reserves capacity
before every extending write; bounded per-file lengths and aggregate
high-water are updated and recorded, including payload and finalization
reserve consumption. Payload cannot spend the 131,072-byte reserve.
Finalization capacity is reserved for counts/errors/verdict/closure/hashes;
inability to complete within it makes evidence incomplete. Require final
length reconciliation plus aggregate all-file high-water evidence, retained
payload bytes, consumed reserve bytes, encoded-copy overhead and discarded
bytes. Ceiling crossing or loss of accounting certainty cannot PASS. This
is source-level control, not a filesystem quota or protection from peers.

No memory-stress, CPU-stress, fault-injection or extra negative child is
included. Read-back/error paths may falsify feasibility without modifying
settings. The envelope is a proposal requiring separate RP-2B acceptance.

## 6. Evidence, error mapping and independent result criteria

Medium probe emits one bounded structured record stream with sequence,
monotonic offsets, section, API/stage, success, return value, error code and
system message. Record errors immediately; APIs returning error codes directly
(PSS) are not interpreted using stale GetLastError. Query-sizing
ERROR_INSUFFICIENT_BUFFER and snapshot ERROR_NO_MORE_ITEMS are expected only
in their specific bounded protocols. Never suppress other errors.

Evidence includes: bound commit/source/child-literal/interpreter/profile
identities; OS edition/build/bitness; input and derived token SID/group/
privilege/policy/elevation/type/session attributes; construction and creation
outcomes separately; exact flags/descriptors/environment/argv/cwd; effective
job limits; suspended-root and READY-base identities/tokens/inventories;
handle values, object comparisons, rights evidence and sentinel results;
imports/versions/origins; console observations; stream bytes, EOF, exit codes;
monotonic request/last-active/first-zero times; resource observations and
limits, skipped sections with causes, cleanup ledger and artifact hashes/sizes.
No secret/user-data dumps. Preserve all partial evidence and immutable originals.

| Class | Required interpretation (independent review overrides probe claim) |
|---|---|
| RP2_PASS | Entire authorized single experiment follows the hash-bound contract; profile blockers closed before implementation; exact frozen profile verified in derived/root/base tokens; intended API succeeds; exact synthetic imports/environment/no-console/UI observations match; U3 identity/rights/inventory/sentinel checks complete at declared checkpoints; expected outputs, exit 0, EOF and cessation established, all bounds/cleanup met. Means bounded U1 and synthetic U2/U3 compatibility only, not production-fixture or supervisor/security qualification. |
| RP2_PARTIAL | No demonstrated contradiction, cessation confirmed, but necessary observations incomplete (missed base snapshot, unsupported reliable rights readback, bounded inventory/output loss, unavailable measurement). Unobserved U1-U3 elements remain open. No retry. |
| RP2_FAIL | Safely ceased but demonstrated incompatibility/mismatch: token construction or creation error, wrong token/profile, absent import/library, invalid ledger/stdio, unexpected inherited object/process, wrong environment/UI/console, nonzero child exit, memory/time boundary or cleanup violation with cessation established. Exact stage recorded; construction success alone cannot pass U1. |
| RP2_UNKNOWN_FAIL_CLOSED | Any unknown cessation/process state, outstanding pipe writer/reader, missing EOF without explanation/confirmation, probe loss, failed termination/wait, or unconfirmed membership after creation. Takes precedence for safety; preserve any contract-defect/failure tags. No later run. |
| RP2_CONTRACT_DEFECT | Source/command/profile differs from reviewed authorization, forbidden behavior, ambiguous criterion used as PASS, unauthorized fallback or missing approved binding. Original evidence retained, independent re-review required; cannot correct retrospectively by rerun. |

If cessation is confirmed, CONTRACT_DEFECT precedes FAIL, then PARTIAL, then
PASS. If no process was created, explicitly record that fact; do not invent
process cessation or EOF. RP2_PASS still requires successful creation/exit.

Expected failure codes include 1314 PRIVILEGE_NOT_HELD (especially U1),
5 ACCESS_DENIED (token, file, desktop/job or handle stage), 87 INVALID_PARAMETER
(attributes/ABI), 2/3 FILE/PATH_NOT_FOUND, 6 INVALID_HANDLE, 50 NOT_SUPPORTED,
8/14 memory allocation failure, 193 BAD_EXE_FORMAT and 126 MOD_NOT_FOUND.
112 DISK_FULL and 109 BROKEN_PIPE require stage-aware handling; 109 after all
writers close is EOF, not generic success. Record unexpected errors too.
No elevation, account change, ACL/label/firewall change, privilege grant,
CreateProcessWithLogonW/WithTokenW, or alternate interpreter is a remedy
authorized by RP-2. A runtime 1314 means current design not demonstrated
feasible without a separately reviewed owner decision.

## 7. Separate future authorizations (neither granted)

**RP-2A - implementation/static review:** owner must first resolve B01/B02
through a reviewed profile interpretation/amendment, and accept this bounded
synthetic substitution/envelope. Proposed source allowlist is only
`scripts/luna65_phase2a_rp2_compatibility_probe.py`, plus a new RP-2A handoff
and authoritative workflow entry. No supervisor, RP-1, fixture or dependency
manifest edits; no executable wrapper/helper generation or package installation.
Use stdlib Windows FFI; exact APIs/ABI, import closure, quoting, handle census/
rights method, output accounting and every cleanup path statically reviewed.
No importing/running probe or creating tokens/jobs/children during static review.
Nonexecuting syntax checks must not create repository bytecode. Any needed
additional source file/tool changes require a new allowlist decision, not an
implicit implementation convenience.

**RP-2B - execution:** after RP-2A independent PASS and source publication/
fetch verification, a new explicit owner authorization must name full commit,
probe/embedded-child hashes/blobs, interpreter identities, frozen profile,
approved exact cmd.exe/PowerShell invocation and byte-preserving accounted
capture mechanism, run ID, path/empty-directory preflight, accepted envelope,
attending operator and exact stop procedure. The command does not exist yet;
do not improvise one from this contract. One invocation, zero retries.
No implementation/static PASS is execution authority.

## 8. Independent review and promotion boundary

Four independent lanes reviewed the first draft, handoff and workflow:
A Windows token/process/integrity; B interpreter/environment/console/UI/
inheritance; C probe safety/resource/evidence/cleanup; D governance/provenance/
scientific isolation/authorization. Each reported concrete findings.

**Integrated verdict: BLOCKED — RP-2 CONTRACT INCOMPLETE.**

| Lane | Independent result on first draft | Findings retained |
|---|---|---|
| A | BLOCKED | B01 confirmed; B02 specificity, not demonstrated impossibility; integrity-group treatment needs precision. |
| B | BLOCKED | Parent/workload environment distinction, exact launcher/base topology, startup import closure, snapshot checkpoint and exact stream grammar. PSS/duplicate/compare/NtQueryObject supports finite checkpoint U3 claims with stated caveats. |
| C | BLOCKED | Startup content binding, independently justified phase deadlines for both normal/failure completion, all-file high-water/reserve accounting evidence. |
| D | PASS, lane only | Baseline/ancestry/R7 and RP-1 identities, governance allowlist and all authorization/scientific boundaries preserved; no integrated PASS. |

Reviewed first-draft checkout SHA-256:
`5186CB531E77826180206C350A735CEE00AD401F347B5C3666DF2080715FC8A3`;
raw CRLF blob `4a8ce6554727e2344bdea1278a711573ecce5511`;
LF SHA-256 `9D5BED4F0A3F9E7CD23EC6C700EB198DEBE9DFB5F887A4B3C2E3351F3898B31C`;
Git-clean LF blob `a41272f83f26ee01bf52af152c1597ba6c3c7ff0`.
Do not confuse the reviewers' raw-byte blob with Git publication normalization.

Compatible clarifications addressing B/C and integrity-group precision were
added after review and have not received a new independent verdict. They
cannot remove B01 or supply the missing B02 descriptor plan. The reviewed
BLOCKED findings remain authoritative for this preparation; no package is
staged, committed or pushed. Further review must cover the exact revised
package after explicit profile resolution, not rely on these old hashes.

PASS requires no unresolved design/profile ambiguity, including B01/B02 and
a reviewed U3 rights method. Experimental feasibility
may remain unknown; contract completeness may not. On BLOCKED retain findings,
do not publish an unsupported resolution. On PASS freeze every allowlisted
file's reviewed checkout SHA-256, normalized/raw blob SHA-256 as appropriate
and Git blob; independent allowlist verification; CRLF-aware diff checks;
commit/push/fetch/compare exact paths/blobs and remote revision. The future
integrated PASS wording is **PASS — RP-2 CONTRACT READY FOR OWNER
IMPLEMENTATION DECISION**; no such verdict was obtained here.

U4-U8, Job Object/full B-min qualification, production imports/fixture behavior,
network enforcement, complete Low-writable coverage and peer Medium tampering
remain outside this experiment. RP-1 consumed/no retry and historical
RP1_CONTRACT_DEFECT; RP-2 implementation/execution, RP-3, supervisor,
Phase 2A/2B fixtures not authorized; full Spiral and Luna-64 corrective execution
blocked; Luna-63C frozen. Stop after governance review/conditional publication.

## 9. Documentation basis (retrieved 2026-10-12; no host API executed)

- [CreateRestrictedToken](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createrestrictedtoken): disable semantics, deny-only SIDs.
- [CreateProcessAsUserW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasuserw): primary-token access, restricted-token privilege exception, quota privilege caveat, mutable argv, inheritance/session.
- [SetTokenInformation](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-settokeninformation): token access and information setting; no launcher-token changes.
- [UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute): explicit HANDLE_LIST and creation-time JOB_LIST.
- [Job UI restrictions](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_ui_restrictions): eight bits, USER-handle distinction.
- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects): nesting, breakaway, resource and membership limits.
- [PssCaptureSnapshot](https://learn.microsoft.com/en-us/windows/win32/api/processsnapshot/nf-processsnapshot-psscapturesnapshot), [capture flags](https://learn.microsoft.com/en-us/windows/win32/api/processsnapshot/ne-processsnapshot-pss_capture_flags), [PSS_HANDLE_ENTRY](https://learn.microsoft.com/en-us/windows/win32/api/processsnapshot/ns-processsnapshot-pss_handle_entry): bounded handle inventory and OS-reserved GrantedAccess limitation.
- [CompareObjectHandles](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-compareobjecthandles): kernel-object identity, not access-right proof.
- [NtQueryObject](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntqueryobject): documented basic-information GrantedAccess, NTSTATUS/ABI and change/removal caveat; no reserved-field inference.

## 10. B01/B02 corrective candidate - governance/design only

**Gate:** `L65-PHASE2A-RP2-B01-B02-CORRECTION`.
Baseline remains `45121227d96c6fa13357c6bdf5fba0d99d8d7352`.
The preceding unpublished candidate was verified before editing: raw checkout
SHA-256 `840D06F6F28ABA6CDF285C375A9CB6E8882A6BAEF4BF74A8B4A9986E9F0D1099`.
Its exact contract/handoff/workflow bytes were preserved in the session
artifact directory `rp2-before-b01-b02`; the historical first-review verdicts
and original preparation handoff are not rewritten. Sections 1-9 are historical
requirements/design except where this section explicitly identifies a
prospective replacement or unresolved contradiction. None is owner acceptance.

### 10.1 B01 proposed amendment - awaiting affirmative owner approval

Proposed replacement, not currently accepted:

> SeChangeNotifyPrivilege shall be the only enabled privilege in the restricted
> Low-integrity child token. Other privilege entries may remain present only
> if disabled. Full token privilege enumeration and attribute readback are
> required. An unexpected enabled privilege constitutes a profile failure.

Require SeChangeNotifyPrivilege present and enabled, enumerate every LUID and
attributes, resolve names, and reject any other SE_PRIVILEGE_ENABLED bit.
Do not confuse ENABLED_BY_DEFAULT or USED_FOR_ACCESS with ENABLED. Unresolved
names, incomplete enumeration or attribute reads cannot pass. This preserves
CreateRestrictedToken(DISABLE_MAX_PRIVILEGE), Low SID, mandatory policy 3,
frozen groups/deny-only rules, no restricting SIDs, Medium non-elevated caller,
no new privileges, no privilege enabling/deletion/repair and the single intended
CreateProcessAsUserW API. Source state must already retain ChangeNotify enabled.

Microsoft's CreateRestrictedToken documentation says DISABLE_MAX_PRIVILEGE
disables all privileges except ChangeNotify and ignores privilege-deletion
parameters when that flag is used. This supports the proposed enabled-state
invariant, not a guarantee of deleting other entries or enabling ChangeNotify
if disabled initially. No owner statement in this gate affirmatively accepts
the replacement. **B01 remains awaiting owner approval.**

### 10.2 Explicit object/descriptor/access matrix

Notation: U is the frozen user SID; M is Medium SID S-1-16-8192; L is Low
S-1-16-4096. An empty DACL is present with zero ACEs (deny discretionary access),
not a NULL/absent DACL (which grants access). It does not by itself remove
owner-implied READ_CONTROL/WRITE_DAC. OWNER RIGHTS is S-1-3-4, not a new token
group or restricting SID. Its use below is a candidate descriptor mechanism
only; no host object is created or modified.

| Object | Creation / descriptor source | Owner, DACL and mandatory label | Required/returned/new handles and inheritance | Low-access implications / disposition |
|---|---|---|---|---|
| Existing Medium probe/launcher process | Future outer invocation, not a W/P implementation; existing descriptor from its caller/token, not changed here | Read back TokenOwner, actual process owner/DACL/label; expect frozen U and Medium token. Existing process-object label is not inferred from token label. No new security configuration | Outer retains exact creation-returned process handle for wait/query/terminate; probe holds only owned exact references; no launcher process/token/job/evidence handle in child list | Same-user ACEs may exist; no assertion of U4 denial or W/P protection. Probe does not qualify the supervisor. |
| Existing launcher thread(s) | Outer/runtime creation; existing descriptors read only | Actual owner/DACL/label recorded where needed, not fabricated | No child inheritance; no new thread control outside owned initial thread; query only where independently needed | No Low-denial claim; U4/U6 unchanged. |
| Synthetic root = venv launcher process (one object, not two roots) | One CreateProcessAsUserW with explicit lpProcessAttributes; proposed literal-compatible root descriptor below | Owner U; protected zero-allow DACL with OWNER RIGHTS deny READ_CONTROL and WRITE_DAC (0x00060000); candidate Low label NO_WRITE_UP. No allow ACE to any child-enabled SID | Creation-returned PROCESS_ALL_ACCESS retained, mask recorded, never inherited. Supports root query, snapshot, duplicate, synchronize and terminate without reopening. Any local reduced references non-inheritable; READ_CONTROL needed for descriptor evidence; token opened QUERY only | Owner rights suppression avoids treating zero ACEs as proof of no owner authority. Self-process behavior/venv startup under this descriptor remains untested. Descriptor is candidate only, not selected to make design pass. |
| Root initial thread | Same creation call, explicit lpThreadAttributes | Owner U; same protected DACL and candidate Low label | Creation-returned THREAD_ALL_ACCESS, record actual granted mask; initial resume via THREAD_SUSPEND_RESUME; optional query/wait via QUERY_INFORMATION/SYNCHRONIZE; close thread after final use; never inherited | No thread handle transmitted. Root creation-returned access does not grant Medium probe handles to base descendants. |
| Base interpreter process (distinct PID/image) | Venv's internal CreateProcessW(NULL, cmdline, NULL, NULL, TRUE, 0, NULL, NULL, ...); parent does NOT supply explicit SD | Owner from venv primary token TokenOwner; DACL from that token TokenDefaultDacl; expected Low token, process-object label/policy requires actual readback. Unspecified owner/DACL/label never replaced by an invented grant | Base creation-returned PROCESS_ALL_ACCESS exists in venv, NOT Medium probe. Probe would require OpenProcess with SYNCHRONIZE(0x00100000), QUERY_INFORMATION(0x400), QUERY_LIMITED_INFORMATION(0x1000), DUP_HANDLE(0x40), READ_CONTROL(0x20000): union 0x00121440; rights verified independently. No SE_DEBUG or owner-DACL rewrite | Unmodified default DACL may grant U (also enabled in Low token). Enforcing no workload-principal allow ACE there removes the proposed Medium reopening path. No creation-returned base handle is delivered to the probe. B02 unresolved. |
| Base initial thread | Internal CreateProcessW NULL thread attributes | Owner/default DACL from venv token; expected Low, actual label not assumed | THREAD_ALL_ACCESS returned to venv, which closes pi.hThread; probe has none and does not need base thread resume/terminate. No OpenThread fallback | No guarantee of no same-user rights from default DACL; cannot claim parent-specified descendant SD. |
| Venv-owned base-process handle | Internal creation-returned handle | Handle access is capability, not DACL grant to Medium probe | Full access retained by venv for wait/exit query; bInheritHandle FALSE for creation-returned process handle; remains in venv inventory at READY if chain live | It is a runtime-created descendant-control handle, not a leak from Medium. Prohibit treating its presence as an unintended inherited parent object. |
| Probe job/process/token/snapshot/evidence references | Probe creates/opens exact owned objects only | No new rights grants to child; protected descriptors outside root/base question not silently inferred | Non-inheritable; excluded from root HANDLE_LIST; duplicate references non-inheritable; no DUPLICATE_CLOSE_SOURCE | Any identity match at root/base to probe-owned forbidden objects fails; inability to inspect remains incomplete, never PASS. |
| Three pipe writes and sentinel | Probe CreatePipe; inert unnamed event negative control | Object identities/access masks recorded; no directory/registry/config writes | Root list exactly three writes. Sentinel inheritable but omitted. Venv duplicates std writes; ledger expected carried by generic inheritance. All read ends/reference duplicates non-inheritable | Exact root handle values apply at root boundary. Base stdout/stderr numeric values may differ; compare pipe object + same granted mask, not root numeric equality. Ledger variable/value and object must match at base. Sentinel absent at both checkpoints. |

Candidate root SD is assembled in memory via InitializeSecurityDescriptor,
SetSecurityDescriptorOwner(U), InitializeAcl/AddAccessDeniedAce(OWNER RIGHTS,
READ_CONTROL|WRITE_DAC), SetSecurityDescriptorDacl(present), protected-DACL
control, and a label-only SACL at L/NO_WRITE_UP. Set both SECURITY_ATTRIBUTES
inheritance flags FALSE. Bind exact self-relative bytes/SDDL and verify
GetSecurityInfo with OWNER/DACL/LABEL information and READ_CONTROL, without
requesting an audit SACL/SeSecurityPrivilege. Applying a label to a new object
is proposed future creation behavior, not an existing-object security edit.
Readback/creation failure refuses resume. No claim of U6 qualification follows.
Exact proposed root process/thread SDDL, with U expanded to its frozen SID,
is `O:UD:P(D;;0x00060000;;;OW)S:(ML;;NW;;;LW)`; U is a notation placeholder,
not literal SDDL text, and OW denotes OWNER RIGHTS. The DACL has one deny ACE
and zero allow ACEs, not the zero-ACE empty DACL described for contrast above.
No group field or inherited ACE is added. Self-relative byte identity would
be frozen in RP-2A; runtime readback compares semantics as well as bytes.
On target Windows 10, SDK PROCESS_ALL_ACCESS and THREAD_ALL_ACCESS are
0x001FFFFF; record actual returned masks rather than assume these constants
establish a successful creation. Root reduced observation union is 0x00121440;
root termination additionally requires PROCESS_TERMINATE(1); initial-thread
resume requires THREAD_SUSPEND_RESUME(2), query THREAD_QUERY_INFORMATION(0x40)
and wait SYNCHRONIZE(0x00100000). Base termination is by outer job only;
no extra PROCESS_TERMINATE or thread-control ACE is proposed.

This root plan demonstrates why retained creation handles can avoid an allow
ACE, but does not close the complete descendant plan. Do not set
TokenDefaultDacl, add a shared-U allow ACE, change token owner, impersonate,
inject, debug the launcher, or edit a descendant SD under this candidate.
An empty default DACL would also remove the Medium base observation route.
Owner rights cannot be used to rewrite it after creation as a workaround.

**B02 disposition: not resolved for the full frozen chain.** The stock
launcher does not accept the probe's process/thread descriptors for its base
child, nor return its base handles to the probe. Root-only protection cannot
be promoted into chain-wide protection. The same-user default ACL route is
in tension with the literal no-workload-principal ACE requirement; allowing
that route would require an explicit profile amendment. Documentation/source
analysis identifies this design incompatibility, not a measured host failure.

Smallest proposed policy issue to decide (not accepted): limit the
"parent-created SD/no workload-principal ACE" requirement to objects directly
created by the trusted parent, while explicitly permitting the frozen venv's
token-default descriptors on its own base child and same-user observation
rights on **workload objects only**. Do not grant Low rights over W/P or the
evidence tree. This does not by itself specify an acceptable base ACL: the
exact existing TokenDefaultDacl/owner/label must be bound and independently
reviewed; if it lacks the required probe rights, fail rather than add an ACE.
If the owner rejects that exception, an alternative topology/descriptor
design is needed in a separate gate; no base-direct fallback or modified
interpreter is proposed as authorized here.

### 10.3 Frozen venv source consequences and further owner questions

Public CPython v3.11.4 PCbuild/venvlauncher.vcxproj compiles PC/launcher.c
with VENV_REDIRECT. That branch reads pyvenv.cfg/home, inserts
__PYVENV_LAUNCHER__ with the original launcher path, and invokes run_child.
run_child duplicates stdout/stderr via DuplicateHandle with inheritable
same-access copies, tolerates invalid stdin by setting NULL, creates base via
CreateProcessW with TRUE generic inheritance and NULL process/thread
descriptors, zero flags/environment/cwd overrides, and retains base handle
for wait. It also creates a launcher-owned unnamed job with kill-on-close and
SILENT_BREAKAWAY_OK, then calls AssignProcessToJobObject without checking
its result. These are stock-launcher operations, not additional probe attempts.

The local frozen binary is hash-bound but not reproducibly linked to this
source by the current evidence. RP-2A must establish reviewed source/build
correspondence or bound static-binary behavior before using these details as
claims about that binary; no binary execution is allowed for this review.

Consequences requiring review/decision rather than silent success criteria:

- Four variables are the environment supplied to the suspended root. Stock
  launcher supplies an additional transient __PYVENV_LAUNCHER__ to base.
  Its handling/removal before the synthetic literal must be source-bound.
  Requiring exactly four at every chain stage conflicts with this source;
  propose owner acceptance of this one precisely bound intermediate variable,
  not PATH/TEMP/etc or a generic environment expansion.
- HANDLE_LIST controls trusted parent -> root only. Stock root -> base uses
  generic inheritance. Define that distinction and require complete bounded
  inventories at both checkpoints. Do not claim explicit allowlist enforcement
  at the second boundary. A literal chain-wide HANDLE_LIST requirement needs
  a separately accepted policy exception or another design.
- Permit only the launcher-owned internal job as documented runtime behavior
  if separately accepted; its SILENT_BREAKAWAY_OK is not permission to loosen
  the outer probe job. Outer no-breakaway/membership must still be verified.
  Internal assignment compatibility with outer UI limits remains runtime
  unknown. Never treat unchecked assignment in launcher as proof of membership.
- Image topology: Medium probe -> Low venv root -> distinct Low base image.
  Base GetModuleFileName image differs from possible venv-valued sys.executable.
  Hash/image/PID/parent/creation-time are authoritative, sys.executable alone
  is not. Base argv[0] may be replaced with base path while -B/-c tail remains
  fixed; require source-bound expected mapping, not byte-equal full command lines.

These source behaviors do not change the selected B-min architecture. They
show that compatibility design cannot assume a custom venv launch API. Pending
owner/profile decisions and static identity binding prevent technical or
owner-authorized readiness; B01 acceptance alone is insufficient.

### 10.4 Revisit of prior B/C findings: exact acceptance obligations

The earlier clarification text is not accepted just because it was added.
Fresh reviewers assess the following same-byte correction:

| Prior issue | Current obligation / residual |
|---|---|
| Startup/hooks/content | Section 4 requires full effective startup and import closure including site/.pth/customization/user-site/cwd/transitive pytest, content hashes and absence bindings; perform bounded static read-only review in future RP-2A, not installed interpreter execution. Complete manifest/path resolution is an RP-2A deliverable; inability to bind closure blocks RP-2B. |
| Literal identity | RP-2A owns one fixed embedded literal and exact Windows quoting, schema, stream count/order and validation. RP-2B names literal SHA-256; no arbitrary literal/source supplied at runtime. No implementation text/literal is generated now. |
| Environment/topology | Sections 10.2/10.3 replace root/base value-equality assumptions with explicit per-boundary process/image/argv/object mapping. Intermediate environment and default-descriptor policies remain unapproved. |
| READY-base | Read exactly one READY on each stream for same base PID/nonce, then obtain one snapshot during the two-second dwell before END; no manufacture/retry if missed. PID may come from bounded job list or READY, never unrelated process enumeration. Acquiring base handles depends on B02; no guaranteed checkpoint coverage. |
| Inventories | Parent and suspended-root complete PSS census; base runtime census compares parent-object identities plus duplicated pipe objects/access, separates runtime opens/internal job/base handles, checks sentinel absence. Original number equality at root only; base stdout/stderr may be duplicates. NtQueryObject caveats retained, no OS-reserved rights inference. |
| Deadlines | Section 5 independently allocates 10 s active, <=5 s cleanup, 20 s outer; earliest F+5,T+15,O+20 governs normal/failure finalization. F includes any confirmed terminal/error outcome even before a process exists. Outer probe death without cessation evidence remains UNKNOWN. |
| Evidence budget | Every representation counts simultaneously; pre-write reserve, all-file high-water, 131,072-byte finalization reservation and <=1 MiB ceiling required. Counting plan and exact schema independently reviewed in RP-2A; lack of certainty cannot PASS. |
| Classification | A proven identity/access/output mismatch is FAIL, not PARTIAL. Missed/unsupported observation without proven mismatch and with confirmed cessation is PARTIAL. Unknown cessation/EOF/reader/writer state is UNKNOWN_FAIL_CLOSED; source/profile/authorization contradiction is tagged CONTRACT_DEFECT with safety precedence preserved. |

Pipes are synchronously drained by bounded worker threads with cancel/wait
ownership specified in future static source review; deadline handlers must
not block behind an unbounded ReadFile or snapshot call. CancelSynchronousIo
and exact worker waits are design requirements if that I/O model is selected;
any remaining worker or unknown child at cutoff is fail-closed, no hung-worker
PASS. Snapshot/API calls have no promised Windows latency bound; the attended
outer stop remains best-effort and does not turn this into hard enforcement.
No additional pipe, file handshake or child retry is introduced.

Retain proposed one attended invocation, one trusted-parent process-creation
attempt, stock venv-to-base chain only, zero retries, 10/5/20 s deadlines,
64 MiB job charge candidate, 8-process backstop, 5 s job user-time backstop,
and 1 MiB retained ceiling. No limits are qualified or executed.

### 10.5 Exact-byte review and authorization outcome

All four fresh lanes must review this same final corrected candidate identity.
Technical completeness and owner approval are distinct. B01 proposal and B02/
intermediate-launcher policy proposals have not been accepted. No affirmative
owner acceptance is inferred from requesting this corrective design review.
Even a conditional technical recommendation cannot authorize implementation
or publication. The previous BLOCKED record in section 8 remains preserved.

Current governing disposition pending fresh results is
**BLOCKED — RP-2 CONTRACT INCOMPLETE**. No publication unless every required
owner decision and independent exact-byte review passes. Do not edit this
candidate after identity freeze for review; record reviewer outcomes in a
separate corrective handoff. On unresolved findings retain locally, unstaged.

Future RP-2A prerequisites: explicit B01 acceptance; reviewed B02 exact plan
and any necessary narrowly stated owner exception; intermediate environment/
inheritance/internal-job decisions; frozen-binary behavior binding; A-D review
of one exact candidate; conditional governance publication and fetched identity;
then separate owner source allowlist authorization. RP-2B remains separate
after reviewed/published source, literal/closure, exact command/run-id/paths/
operator preflight. Nothing here implements or runs either step.

### 10.6 Corrective authoritative sources

- [CPython 3.11.4 venv build](https://github.com/python/cpython/blob/v3.11.4/PCbuild/venvlauncher.vcxproj) and [launcher source](https://github.com/python/cpython/blob/v3.11.4/PC/launcher.c): VENV_REDIRECT, run_child, safe_duplicate_handle; public source not proof of local binary correspondence.
- [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw): default process/thread descriptors from creator token, inherited environment/cwd, returned process/thread handles.
- [Process access rights](https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights): returned PROCESS_ALL_ACCESS versus DACL-checked OpenProcess, exact observation rights.
- [Owner of a new object](https://learn.microsoft.com/en-us/windows/win32/secauthz/owner-of-a-new-object): default owner, implicit WRITE_DAC, no invented alternate owner.
- [Mandatory integrity control](https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control): token integrity versus object label, MIC before DACL, no read-up assumption from Low alone.
- [CreateRestrictedToken](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createrestrictedtoken): disabled privilege entries versus deletion; no privilege acquisition.
