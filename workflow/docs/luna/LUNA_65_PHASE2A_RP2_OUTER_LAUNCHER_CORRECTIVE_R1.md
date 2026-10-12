# Luna-65 RP-2 Medium launcher and token-descriptor closure R1

**Gate:** `L65-PHASE2A-RP2-OUTER-LAUNCHER-CORRECTIVE-R1`
**Date:** 2026-10-12
**Scope:** Governance/design only; no implementation or execution.
**Status:** Corrective candidate for independent A-D review and owner decisions.
No proposed profile exception in this document is accepted by this gate.

## 1. Provenance, precedence and preservation

Expected and observed HEAD/local upstream:
`45121227d96c6fa13357c6bdf5fba0d99d8d7352`;
branch `governance/luna64-r4.3-freeze-20261010`. Index empty; existing tracked
workflow modifications and untracked documents/scaffold retained, not reverted.
No fetch, staging, commit or push performed.

The [direct candidate](LUNA_65_PHASE2A_RP2_DIRECT_INTERPRETER_DESIGN.md) remains
checkout SHA-256 `374AB0328B62966EEA7C1E52E9E9E25BB40D973863177DEC4160D077E1C2A476`;
raw blob `d76c14c0fd9c50dd1e57245bad0a5c1cc5c566f0`;
Git-clean blob `66356a9328e6fc4dfc28e8b8eb2fdbbfc0cdf15d`.
The [older corrected RP-2 contract](LUNA_65_PHASE2A_RP2_RESTRICTED_TOKEN_COMPATIBILITY_CONTRACT.md)
remains SHA-256 `E573ADA32D746E6766D21420C845FF6AA09B18107F05523A6F1BE8913EE3A313`.
Its full-chain B02 blocker and all previous findings stay historical, intact.
The prior direct review handoff is SHA-256
`91B72964FD0B8C8CAE16DEFD777F4569F01BD6350F156DD54EE1FC0249BE5204`;
existing workflow `3B6A1BB5E27A4182B9E186E7395D91B8BC9E80F8DC5D5A7CF69E00181AD73008`;
untracked supervisor `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`.
None is changed. RP-1 remains consumed with RP1_CONTRACT_DEFECT, no retry.

This is an additive prospective correction, not a rewrite of reviewed bytes.
Sections 2-7 govern ONLY Medium admission, outer supervision and token-object
binding if later reviewed/accepted. Everything else refers to the hash-bound
direct candidate. Prior A/C BLOCKED, B/D lane-only PASS are preserved.
No A01-A15 core/ACP change; no neural or hardware acceptance check claimed.
Configured tpcn-luna-workflow paths remain absent; authoritative repository
counterparts under workflow were used, as recorded in the previous gate.

Owned outputs are this document and a new completed handoff only. Existing
workflow is not edited while decisions remain open. No probe source/wrapper
is generated, imported, launched or qualified. No token/job/fixture or Windows
configuration change is authorized. All future steps below are design only.

## 2. Frozen Low profile and scientific isolation

B01 remains prospectively accepted: SeChangeNotifyPrivilege present and the
only enabled child privilege; other entries may remain disabled; full LUID/
name/attribute readback mandatory; unexpected enabled privilege fails.
No privilege enabling, repair, acquisition, elevation or impersonation.
Primary CreateRestrictedToken(DISABLE_MAX_PRIVILEGE), Low S-1-16-4096,
mandatory policy NO_WRITE_UP | NEW_PROCESS_MIN = 3 read back, not repaired;
frozen SID/group rules and no restricting SIDs remain.

Low process/thread X-L descriptors, three P-L pipe objects, suspended
CreateProcessAsUserW with HANDLE_LIST/JOB_LIST, stdin NULL, direct Python
identity, four-variable child environment, fixed synthetic-workload
specification, import/closure/grammar obligations and U1-U3 inspection do
not change. No fourth pipe or outer-control handle reaches the Low child.
No implemented literal bytes exist yet: freeze the unchanged specified
literal once in RP-2A, never invent a prior literal hash.

Expected Low interpreter (also the proposed Medium probe host below):
`C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe`,
SHA-256 `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F`,
Python 3.11.4 AMD64. Hash reverified read-only in this gate; prior version
resource/PE and retained RP-1 runtime identity evidence remain applicable.
No new interpreter invocation. No TPCN/E2/dataset/fixture/training access.

Candidate envelope unchanged: one Medium-probe invocation, one trusted-parent
Low creation attempt, zero retries; 10 s active, <=5 s cleanup, 20 s attended
outer; 64 MiB job-memory charge, eight-process backstop, five-second job
user-time backstop, 1 MiB aggregate logical evidence. Unexecuted/unqualified.
No extra observer job, service, ETW, system-wide census or new Python runtime.

## 3. Medium probe admission: ordinary Windows-issued descriptors

Roles: O = existing attended Windows PowerShell 5.1 outer caller; P = newly
created Medium Python probe; L = the one intended restricted Low Python
child; D = any unexpected job descendant (always failure, never extra work).
O is not a B-min watchdog/controller implementation. The operator starts one
future reviewed outer script in an existing non-elevated same-user Medium
PowerShell session. The existing shell is not silently reconfigured.

The future outer source would use native CreateProcessW directly, not
Start-Process, ShellExecute, cmd indirection, runas or a replacement launch
API for L. A reviewed native interop surface hosted by that PowerShell is a
later source-allowlist deliverable; no Add-Type/interop source is generated now.
No second outer process is required. Bind its host executable/version and
startup/module closure in RP-2B; an arbitrary PowerShell host is not accepted.

O verifies its own frozen account U, Medium S-1-16-8192, non-elevation,
session, source privilege rules and absence of a thread impersonation token.
P gets O's existing primary-token security context through CreateProcessW:
no hToken argument, DuplicateTokenEx, credentials or token adjustment.
Do not promise token-object identity equality; independently query P's token.
If O/P is elevated, Low/High, another account/session or impersonating, refuse.

One CreateProcessW call:

- lpApplicationName = exact bound base executable above.
- Mutable argv = that executable, -B and the absolute reviewed probe-source
  path plus the frozen run nonce and O0 uptime-millisecond deadline metadata.
  No child literal is supplied by the operator.
  Source/nonce grammar/quoting and exact command bytes freeze in RP-2A/RP-2B.
- lpProcessAttributes=NULL; lpThreadAttributes=NULL. P process and initial
  thread descriptors come from Windows/creator primary token rules, NOT X-M.
  Returned process/thread handles are non-inheritable.
- CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT | EXTENDED_STARTUPINFO_PRESENT
  | DETACHED_PROCESS. No breakaway, alternate desktop or outer JOB_LIST.
  Ambient-job incompatibility fails; no host job setting is changed.
- STARTF_USESTDHANDLES, stdin NULL; exact HANDLE_LIST of two Medium-capture
  pipe writes, stdout/stderr only, bInheritHandles=TRUE. These are P->O report/
  diagnostic streams, NOT additional Low-child pipes. Both objects have
  ordinary O-created Medium descriptors read back, no ACL/label modification.
  O's read ends and all process/thread/token/job/evidence handles excluded.
- Explicit Unicode P environment: PYTHONHASHSEED=0,
  PYTHONDONTWRITEBYTECODE=1, SYSTEMROOT=<verified host SystemRoot>, no other
  variables. No TPCN_LUNA65_LEDGER_HANDLE in P; P creates the Low child's
  ledger itself. Cwd repository root. No implicit host-environment inheritance.
  This three-variable Medium block does NOT replace L's four-variable block.
  Static startup/import closure covers the distinct Medium probe invocation.

O alone receives PROCESS_INFORMATION. Verify real handle type/access:
returned PROCESS_ALL_ACCESS 0x001FFFFF and THREAD_ALL_ACCESS 0x001FFFFF,
using the already-reviewed basic rights query; do not assume grant from API
success. O retains them non-inheritable, never sends them to P/L.
Required P reduced union: READ_CONTROL 0x20000, QUERY_INFORMATION 0x400,
QUERY_LIMITED_INFORMATION 0x1000, TERMINATE 0x1, SYNCHRONIZE 0x100000 =
0x00121401. No DUP_HANDLE, memory access, injection or owner/DACL editing
is used even if returned handles include them. Thread requires resume 0x2,
QUERY_INFORMATION 0x40, READ_CONTROL 0x20000, SYNCHRONIZE 0x100000 =
0x00120042. Close thread after admission use; process after bounded exit query.

Before P resume, O queries process/thread owner, group, DACL/control flags,
mandatory label using OWNER/GROUP/DACL/LABEL_SECURITY_INFORMATION only,
plus image, PID from handle, creation FILETIME from GetProcessTimes, token,
session and ambient job status. Store raw self-relative SD and canonical
decoded ACEs under the shared evidence cap. No fake static SDDL is claimed.
Observe the descriptor label independently of contained token integrity.
For new P process/initial thread require owner U and effective Medium label;
present non-NULL DACL; ordinary inherited/protected status recorded, not
required to be protected or to have OWNER RIGHTS denial. Reject missing or
unreadable descriptor evidence; no rewrite. Explicit or OS-default effective
Medium label is recorded distinctly; no added NO_READ_UP denial is assumed.
Source TokenOwner used by Windows must agree with observed owner, not be
inferred solely from TokenUser.

P's host-assigned SD bytes are bound at this one invocation as evidence,
not retrospectively declared a pre-known creation SDDL. No denial test or
U4/U6 claim follows. Same-user Medium peer access and potential Low access
under the ordinary DACL are outside the claim; handles to O/P are still
prohibited in L's inheritance. Low-to-trusted-process denial needs separate
qualification under the frozen production profile, not this exception.

A custom protected X-M DACL is unnecessary to O's retained-handle stop route.
An OW deny would not revoke already returned handles, but is not needed and
could obstruct legitimate future reopen/readback paths. P/initial thread
therefore use ordinary SDs under proposed D-RP2-MEDIUM-1, not accepted.
For newly P-created job/sentinel and native reader threads the previous X-M
target stays unchanged. P's runtime-created threads use ordinary runtime
SDs, inventoried as such, not claimed X-M. They inherit no handles into L.
CancelSynchronousIo uses only retained native reader-thread handles.

CreateProcessW failure: capture GetLastError immediately; output handles
invalid unless success. No resume, no Low attempt, no retry; record launch
failure, close only actually created O objects. If P creation succeeds but
admission fails, one TerminateProcess on retained P handle, bounded wait;
L cannot have been created while P's initial thread stayed suspended.
Resume P exactly once only after admission and reader readiness.
ERROR_PRIVILEGE_NOT_HELD/access/ABI failures never trigger a fallback.

## 4. Outer ownership, budget and finite stop procedure

| Component | Owned handles and exclusive operations |
|---|---|
| O, existing Medium outer | Creation-returned P process/initial thread; two P capture reads; temporary capture writes until P admission; own query token references and own reader-thread handles; evidence writer. No L process/thread/token or job handle. |
| P, Medium trusted probe | Sole unnamed job handle, non-inheritable, never duplicated; creation-returned L process/thread; three Low-pipe reads and initial writes; source/derived/query tokens, snapshots/references, sentinel and workers. No O process/thread handle inherited. |
| L | Only the three intended Low pipe writes inherited; own runtime/self-query handles as already reviewed. No O/P/job/token references from parent. |
| Operator | Attends O; authorizes the one invocation and can request its same finite stop procedure. No PID-name kill or general process sweep. |

O starts monotonic outer deadline O0 immediately before its single P creation
attempt, after source/path/descriptor-route policy preflight. Both O and P use
native GetTickCount64 (system uptime milliseconds, same boot/host epoch).
P0 is P's first entry, published once in its bounded report; active deadline
P0+10 seconds. P records wall/uptime offsets and stop request/last-active/
first-zero values. Do not compare arbitrary Python/PowerShell stopwatch epochs.
Missing P0 cannot extend O0+20. P active ends by P0+10;
cleanup/finalization ends by min(F+5,P0+15,O0+20), retaining prior F definition.
O0 milliseconds and fixed 20,000-ms allowance are supplied as frozen command
metadata; exact integer parsing/unit conversion freezes in RP-2A.
Ambiguous, future-dated or expired metadata cannot PASS or extend a deadline.
No unreviewed environment variable or Low input is added for this purpose.

O is the sole evidence-file writer in this proposed diagnostic amendment.
P emits its report and byte-preserving encoded captures of the three separate
Low streams over its Medium capture stdout; stderr is failure diagnostics,
not a second unaccounted file writer. P does not create an evidence leaf,
temporary/intermediate file or hash manifest. O alone performs the prior
fresh-leaf/reparse checks, bounded artifact writes, hashing and finalization.
This moves only the trusted diagnostic evidence-writer role, not Low inputs
or production B-min ownership, and is included in D-RP2-MEDIUM-1.
P's source-level bounded buffers/read-discard counters remain required.
U1-U3 records and each Low stream's original bytes/order stay independently
recoverable; encoding/version/sequence/length errors or lost capture fail.
No existing fixed child literal changes to support this relay.

O enforces the unchanged aggregate 1,048,576 logical-byte ceiling with
917,504 payload maximum and 131,072 failure/finalization reserve. Raw Medium
capture, decoded Low-stream copies, structured report and all simultaneous
representations count separately if retained. Reserve before every write;
no assumed equivalence of raw and decoded lengths. P output cannot consume
O's finalization reserve. O tracks/discards overflow with bounded counters,
initiates the finite stop and cannot report PASS after accounting loss.
This explicit single-writer plan avoids independent P/O budgets that could
sum beyond the cap. O still is not filesystem- or peer-tamper-contained.

O waits/polls its exact P handle at nominal 25 ms, with bounded byte-preserving
capture readers. O does not block its deadline thread on ReadFile/PSS/token
query. Sizing/walk caps and cancellation remain source obligations; API call
latency is not hard-bounded. All O setup after O0 consumes the 20 s.
There is no second active allowance if P starts late.

Normal completion: O waits for P signalled, obtains exit code, drains two
Medium capture streams to EOF and finalizes before O0+20. P separately must
provide L signalled/exit, job-zero, three Low EOFs and cleanup ledger within
its earlier deadlines. O distinguishes its own P-exit observation from P's
reported L/job observation. A success-shaped report without underlying
evidence is rejected by independent review.

Stop is finite, idempotent, no retries of process creation or experiment:

1. On explicit operator stop, P error/crash, output/identity violation, missing
   expected finalization or O0+15 with P still active, mark stop requested.
   P internally starts cleanup by P0+10 or its earlier failure. There is no
   unimplemented cooperative IPC stop/ack protocol; do not wait for one.
2. If retained P handle is not signalled, issue at most ONE
   TerminateProcess(P, frozen nonzero stop code); record return/error/time.
   Never use taskkill, Stop-Process -Name, a PID-only replacement handle,
   TerminateThread or an escalation/reopen operation.
3. Use WaitForSingleObject in bounded slices until min(request+5,O0+20);
   query P exit only from that same retained handle. If already signalled,
   do not call termination; record its observed exit instead.
4. Cancel/drain/join O readers within the same absolute bound. No forgotten
   capture writer or outstanding worker is accepted as complete. Close
   owned local handles; retain evidence and record missing observations.
   Unknown P cessation is UNKNOWN_FAIL_CLOSED, regardless of API success.

Launching P or terminating it cannot be promised to complete by a hard
Windows deadline. O0+15 stop request reserves at most five seconds for outer
observation; it is not permission for P or L to run beyond active deadlines.
If O's own API call or runtime hangs, an attended operator can only use the
already-defined exact handle operation when responsive. O loss/hang itself
is an uncontained residual; no additional supervisor is introduced.

## 5. Independent observation boundary and documented blocker

P is the sole job owner by the frozen candidate. An O-held query-only job
duplicate would keep the last job handle open and defeat kill-on-P-loss.
The unnamed job cannot be reopened by name. Retained P access is not a job
query handle and does not independently confer L's returned capabilities.
Low X-L's zero-allow DACL prevents relying on O's OpenProcess(L) route.
No descriptor change, job duplication or capability handoff is introduced.

P emits incremental nonce/sequence-bound bounded records over its existing
Medium stdout capture: BEFORE_LOW_ATTEMPT, CREATE_RESULT or explicit
NO_LOW_CREATED, L PID/creation-time/image/hash/token identity, job membership,
bounded active-job list and observation results, termination request, L exit/
signalled observation, job-zero, Low EOFs, cleanup, FINAL. Output grammar is
an RP-2A deliverable; no literal code or extra child input is added. Bound
job list <=8 (unexpected D fails); corroborate job identities through P-owned
exact process references where access permits. Do not infer D access from
root handles; unavailable identity/exit observation is incomplete.

O records P as PID+creation-time+image+source hash from its retained handle.
L and D identities are explicitly P-observed reports, not O-measured exits.
No system-wide enumeration or bare parent-PID tree inference is used.
Incomplete records, unknown create result, absent handle, PID reuse,
unconfirmed membership/EOF or unobserved descendant cessation fail closed.
No later independent OpenProcess with guessed PID may manufacture a PASS.

| Failure | Exact existing-authority response and result |
|---|---|
| P hangs after Low admission | O's one P termination request; sole job handle closes if P actually exits. Independently wait P; L/job termination is requested indirectly, NOT confirmed by that wait. Without already complete P evidence, L/D cessation UNKNOWN, overall UNKNOWN_FAIL_CLOSED. |
| P crashes before Low attempt | If O never resumed P, L was never created. Otherwise a missing report is not proof no attempt occurred. A received NO_LOW_CREATED is P-reported only; a crash in constructor/creation remains potentially unknown. P exit alone does not close L evidence. |
| P crashes during/after creation | Same job kill-on-close request if L was assigned; no independent L handle. Creation/result-publication race remains UNKNOWN, no automatic recovery guarantee. |
| L remains active while P responsive | P uses TerminateJobObject, and retained root TerminateProcess if suspended membership unconfirmed; waits/readback/EOF under <=5 s cleanup. If still unknown at cutoff, UNKNOWN_FAIL_CLOSED and no retry. |
| L never assigned/intended membership unconfirmed | P never resumes; terminates exact suspended L through returned process handle as well as job request. If P dies before this, job close cannot kill a nonmember: unknown/outside survivor cannot be safely recovered by O. |
| Sole job handle unexpectedly closes | Kill-on-close applies to actual members only. Record error, never replace/reopen job or admit more children. Responsive P can wait retained L; job-zero unavailable makes evidence incomplete. On P loss, L/D state unknown. |
| Enumeration, identity or termination query fails | Preserve immediate error and stage; never treat missing member as absent. Known failed termination or unknown state gives UNKNOWN_FAIL_CLOSED. No broad kill/census/privilege repair. |
| P termination request succeeds, wait does not signal | P cessation unknown; job handle closure also unknown; overall UNKNOWN_FAIL_CLOSED. |
| P signalled but L/D cessation not independently known | Record P ceased; L/D reported/unknown distinctly. Normal complete P evidence can support bounded compatibility, not independent fault recovery. Missing evidence never PASS. |
| O hangs/crashes or exceeds deadline | Best-effort attended control unavailable/late; no hard guarantee. Preserve available artifacts and UNKNOWN_FAIL_CLOSED; no permission for another invocation. |

**INFERRED limitation:** independent containment/cessation observation for
L/D on P loss is NOT established under existing sole-job/no-transfer rules.
The production B-min owner's W-loss/race residuals do not silently approve
this RP-2 observation limitation. UNKNOWN is a safety verdict, not a remedy
or proof that no process remains alive.

Smallest proposed policy choice D-RP2-OUTER-1 accepts this narrower diagnostic
fault boundary explicitly (section 7). If that is rejected, design is BLOCKED:
a separately reviewed authority/handle-transfer or ownership design must
provide O with trustworthy Low/job observation/recovery capabilities.
Do not add an observer job/service/ETW or claim such a design is impossible.
Even a query-only job duplicate needs lifecycle redesign, not a quick fix.

## 6. Token-object access and descriptor binding closure

Token contents (User/Owner/DefaultDacl/groups/privileges/IL/mandatory policy/
type/session/elevation/restrictions) differ from the SECURITY_DESCRIPTOR
protecting the kernel token object. TokenOwner and TokenDefaultDacl govern
other object defaults; neither is the actual token-object owner/DACL.
Contained Low IL does not prove a Low token-object mandatory label.

Object SD route: bounded GetKernelObjectSecurity with OWNER, GROUP, DACL
and LABEL information only, via READ_CONTROL; no audit SACL query,
ACCESS_SYSTEM_SECURITY or SeSecurityPrivilege. Raw self-relative bytes,
owner/group, DACL-present/null/protected/defaulted flags, all ACE types/SIDs/
masks and mandatory-label state are retained and decoded completely.
An absent explicit label records effective OS-default Medium separately.
No token-object label or owner is fabricated from TokenUser/IL.
No NULL/absent DACL or undecodable/truncated SD can PASS this diagnostic.

The acceptance binding is OS-issued, immutable observed descriptors, not
a requested custom token SDDL: record exact actual bytes at the first query,
query again before last relevant use and compare semantics for drift.
No token-object security edits are permitted. Byte-representation differences
without semantic drift are separately reported, not silently normalized away.
No equality of source/derived/child SDs or token object identities is assumed.
Unrelated same-user access to token objects is not qualified as denied.
This does not relax frozen Low privilege/group/IL/mandatory-policy checks.

| Token | Origin/type/intended contained IL | Acquisition and exact rights | SD origin, readback, ownership/closure |
|---|---|---|---|
| O primary query reference | Existing PowerShell process primary; Medium, frozen U/session/non-elevation | OpenProcessToken(O self, TOKEN_QUERY 0x8 plus READ_CONTROL 0x20000 = 0x20008); process QUERY_LIMITED_INFORMATION prerequisite | Existing Windows-issued token SD; O reads/records actual SD and fields, no new SD, non-inheritable; O closes. |
| P admission query reference held by O | Primary token assigned during CreateProcessW; Medium same security context as O, not asserted same token object | OpenProcessToken(retained P, 0x20008); no token duplication or adjustment by O | OS-assigned actual token SD, not P process SD; O reads before P resume, closes. Failed access/readback aborts admission. |
| P own source token construction reference | P's own primary Medium token, same frozen U/session | OpenProcessToken(P self, TOKEN_ASSIGN_PRIMARY 0x1, TOKEN_DUPLICATE 0x2, TOKEN_QUERY 0x8, TOKEN_ADJUST_DEFAULT 0x80, READ_CONTROL 0x20000 union 0x2008B) | Existing OS token SD, actual readback; P holds non-inheritable reference solely to construct/launch derived token, NEVER adjusts its own source token. Closes after derived construction/launch/reference work. |
| R derived restricted token | Exactly one CreateRestrictedToken on P source, same primary type; contained Low IL set on R only | CreateRestrictedToken returns SAME access rights as input: 0x2008B, independently verified. TOKEN_ADJUST_DEFAULT used ONLY for SetTokenInformation(TokenIntegrityLevel). ASSIGN_PRIMARY/QUERY/DUPLICATE support CreateProcessAsUserW | Constructor-assigned OS token SD, no lpSecurityAttributes parameter, no fabricated default-DACL formula. P reads actual SD/fields before Low creation and final relevant use, no SD edit; never inherited; closes on all paths. |
| L primary-token query reference held by P | Actual admitted child's primary token; Low, matching frozen restricted field policy, not asserted same R object | OpenProcessToken(retained L process, 0x20008), no adjustment; process QUERY_LIMITED_INFORMATION prerequisite is available in retained process handle | Creation/OS-issued actual token SD; P independently queries before resume and READY observation; never inherited; closes after readback. Process ALL_ACCESS alone is not token-access proof. |
| L self-query reference inside unchanged literal | L's own actual primary token; Low | Existing specified literal's OpenProcessToken(self, TOKEN_QUERY=0x8); no READ_CONTROL added to the frozen workload | No token SD change or new descriptor query in child literal. P supplies SD evidence; L supplies independent token-field readback. Non-inheritable, child closes. |

Source construction-mask correction is necessary: previous 0x2000A
(QUERY/DUPLICATE/READ_CONTROL) cannot yield a returned R handle with
ASSIGN_PRIMARY/ADJUST_DEFAULT when the constructor preserves input rights.
Requesting 0x2008B is acquisition of TOKEN object access rights under its
existing DACL, NOT acquisition/enabling of a privilege. Do not silently request
TOKEN_ALL_ACCESS, MAXIMUM_ALLOWED, TOKEN_ADJUST_PRIVILEGES,
TOKEN_ADJUST_GROUPS, TOKEN_ADJUST_SESSIONID, TOKEN_IMPERSONATE or
TOKEN_QUERY_SOURCE. No SYNCHRONIZE on tokens (unsupported), no
WRITE_DAC/WRITE_OWNER or object security repair.

OpenProcessToken handles start non-inheritable; verify flags. R returned
handle also must read back non-inheritable; clear local HANDLE_FLAG_INHERIT
if needed before any process admission and record it, not an object ACL edit.
No token handle is in either P or L HANDLE_LIST; no token is sent to O from P.
No OpenThreadToken/impersonation fallback. To check no thread impersonation,
bounded OpenThreadToken query yields ERROR_NO_TOKEN; any actual thread token
or other error refuses admission, closes any returned reference, no RevertToSelf
repair. Such a rejected token is not an authorized workload token.

Complete GetTokenInformation/readback includes source/derived/admitted
privileges, group flags/restricting SIDs, integrity, mandatory policy,
TokenType/User/Owner/DefaultDacl/session/elevation. Handle GrantedAccess and
inheritance attributes are separately evidenced by the reviewed rights ABI.
R must already have ChangeNotify enabled from source; no privilege adjustment.
Policy 3 is read back only, no TokenMandatoryPolicy-setting repair.

Access-denied constructor-mask, token SD/field query failure, incomplete name/
attribute readback, semantic drift or wrong type/policy prevents resume.
Before L creation fail without inventing cessation; after creation P uses
existing bounded termination. Proven wrong fields/SD drift are FAIL;
unsupported incomplete observation with confirmed cessation PARTIAL;
unknown cessation UNKNOWN_FAIL_CLOSED. No retry/new privileges/ACL repair.
Successful ordinary token opens are experimental questions, not assumed facts.
Exact generated SD bytes cannot be statically pre-observed without forbidden
creation; the above complete runtime readback rule closes the design binding
without falsely claiming they were measured in this gate.

## 7. Precisely scoped owner decisions, not accepted

D-RP2-DIRECT-1 from the preserved direct candidate remains unaccepted:
exact direct-base Low experiment only, not production interpreter substitution.

**D-RP2-MEDIUM-1 proposed:**

> For this RP-2 diagnostic only, permit the attended non-elevated same-user
> Medium outer caller to create the Medium probe with CreateProcessW and
> NULL process/thread security attributes, using ordinary Windows-issued
> descriptors read back as specified in this R1 contract. No custom protected
> X-M DACL or OWNER RIGHTS denial is required for that probe or initial thread.
> Accept that this makes no Low-to-trusted-process ACL-denial/U4/U6 claim.
> Permit two Medium probe-capture pipes and the outer caller as sole diagnostic
> evidence-file writer, preserving byte-recoverable independent Low-stream
> evidence and the existing single-writer aggregate ceiling/reserve accounting.
> Retain exact returned-handle stop authority and no process/token/job handle
> inheritance into the Low child. This exception does not amend the production
> B-min W/P descriptors or qualify its security boundary.

**D-RP2-OUTER-1 proposed, smallest residual-policy decision:**

> For this single RP-2 diagnostic only, accept independent outer authority
> to observe and terminate the exact Medium probe, with the probe remaining
> sole owner of the unnamed kill-on-close job. Outer termination and job
> closure are best-effort requests, not proof of Low-child/descendant cessation.
> On probe loss, creation/publication races, unconfirmed membership or missing
> Low cessation evidence, record UNKNOWN_FAIL_CLOSED; an unknown or surviving
> Low process may remain beyond the observation deadline and no containment
> guarantee is claimed. Accept the corresponding attended stop limitation,
> including outer loss/hang, without granting retries or permission for further
> workload execution. This is not supervisor qualification or a production
> B-min fault-model amendment.

If the owner requires independent confirmation/recovery of every Low process
under these faults, reject D-RP2-OUTER-1 and dispatch a separate bounded
authority/lifecycle design. The present sole-job/no-transfer design cannot
meet that stronger requirement by changing only Medium DACLs.
No fault-model acceptance is inferred from ordering UNKNOWN before PASS.

The two capture pipes/outer interop and native reader bindings require a
future explicit source allowlist for an attended outer wrapper in RP-2A.
They are not permission to create one in this gate. No new implementation
file path is authorized here; proposed path/host/source hashes must be
separately approved. The existing probe path remains untouched/absent.

## 8. Review, publication and exact next gates

A-D must independently verify this same final candidate checkout hash and
review it together with the preserved direct-candidate identity it references.
A: Medium admission/SD/token rights; B: Low/direct/three handles unchanged;
C: outer fault response and limits; D: provenance/policy/scientific isolation.
No candidate edits after freeze. Record actual lane verdicts in new handoff.
Technical clarity, host feasibility, owner acceptance and source authorization
are distinct; pending decision alone is not measured incompatibility.

Required integrated wording:
**PASS - RP-2 DIRECT CONTRACT READY FOR OWNER DECISION**, or
**BLOCKED - RP-2 DIRECT CONTRACT INCOMPLETE**.
If lack of independent Low fault containment remains incompatible with the
required fault model, record BLOCKED, not a synthetic PASS.
No implementation-readiness publication while policy decisions are pending.

Conditional future governance allowlist: this R1, its new handoff and additive
authoritative workflow entry; preserve prior contracts/reviews as immutable
dependencies. Independently verify the entire publication package and exact
raw/clean identities, then commit/push/fetch only after all necessary owner
decisions and reviews pass. No publication is performed by this candidate.

RP-2A prerequisites: reviewed complete design/fault-policy disposition,
D-RP2-DIRECT-1/MEDIUM-1/OUTER-1 accepted or a separately reviewed stronger
alternative; governance publication/fetched identity; new explicit source
allowlist grant including exact outer wrapper/interop host; static FFI,
rights/SD decoding, token-mask fix, command quoting/environments/time-base
conversion, literal/closure/grammar, capture/accounting/reserve/cancellation/
cleanup and failure-state review. No probe import/run during static review.
RP-2B remains later and separate: published/reviewed source and bindings,
exact invocation/run-id/path/attending operator/stop procedure and explicit
execution grant. No current command or run ID is created.

RP-2 implementation/execution, RP-3, supervisor implementation/qualification,
Phase 2A/2B fixtures NOT AUTHORIZED; full Spiral and Luna-64 corrective
execution BLOCKED; Luna-63C FROZEN. Production venv compatibility remains
independent: root-to-base handles, internal job, environment/startup and full
pytest invocation. Direct synthetic U1-U3 cannot establish any of those.

## 9. Authoritative documentation used, no host API experiment

- [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw): caller primary security context, default descriptors, PROCESS_INFORMATION and suspended creation.
- [CreateRestrictedToken](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createrestrictedtoken): new handle has SAME access as input, same token type; no custom SD parameter.
- [OpenProcessToken](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken): requested token rights checked against TOKEN object DACL.
- [Token-object access rights](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-rights-for-access-token-objects): TOKEN masks, token SD queries, no token SYNCHRONIZE.
- [DuplicateHandle](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-duplicatehandle): capability transfer is a separate operation, not granted by a PID report.
- [Job objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects): last-handle closure, unnamed-job reopen limitation and kill-on-close semantics.
- Prior direct/blocked contracts retain the unchanged Low process/pipe and PSS/NtQueryObject API basis and their limitations.
