# Luna-65 RP-2 B01 acceptance and direct-interpreter corrective design

**Gate:** `L65-PHASE2A-RP2-DIRECT-INTERPRETER-CORRECTIVE-DESIGN`
**Date:** 2026-10-12
**Status:** Proposed experimental profile; NOT owner-approved; NOT executable.
Fresh A-D verdicts and the frozen identity belong in the separate handoff.
The existing RP-2 contract remains BLOCKED and is preserved byte-for-byte.

## 1. Authority, provenance and bounded ownership

This gate authorizes governance/design and four independent reviews only.
No source implementation, Python invocation/import, token/job creation,
process-launch experiment, fixture, Windows configuration or existing-object
security change is authorized. No RP-2 invocation is consumed.

HEAD and locally recorded upstream are both
`45121227d96c6fa13357c6bdf5fba0d99d8d7352`, branch
`governance/luna64-r4.3-freeze-20261010`. No remote fetch was performed.
The expected S1-B/RP-1 commits are ancestors: `948f5e70a43a3524dfef6bbe8f04bbd041770fd6`,
`65de223151ff196c72263f79e50719a7b6dbbd07`,
`c05cc6d88cb4aa224e7c53b4b4fe3ca0589bc7e6`,
`2a07b1e9f20d758df218981a9a8563c5f953d4b5`.
The final RP-1 reconciliation publication is the current baseline.

Preserved [corrected blocked contract](LUNA_65_PHASE2A_RP2_RESTRICTED_TOKEN_COMPATIBILITY_CONTRACT.md):
checkout SHA-256 `E573ADA32D746E6766D21420C845FF6AA09B18107F05523A6F1BE8913EE3A313`;
raw Git blob `489707e18bf422c370678a1433aad983fd14e552`;
Git-clean blob `f61847d0c93f59b189142c5544caf9791e32bbe4`.
Preserved corrective handoff checkout SHA-256
`5657D44B6D330FFACB0053986F89E835F87409FC4573979CA19ECDBBE5393419`;
preparation handoff `E5EFD7E1BEEB446815CDB4055F9135A13D1312ACFC2181A3125B98EE9AB4A8E3`;
pre-existing workflow `3B6A1BB5E27A4182B9E186E7395D91B8BC9E80F8DC5D5A7CF69E00181AD73008`.
The untracked supervisor remains excluded, SHA-256
`67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`.

Historical first review: A/B/C BLOCKED, D PASS lane only.
Historical corrective review: A/B BLOCKED, C/D PASS lane only.
The full-chain B02 blocker, intermediate environment, generic inheritance,
internal launcher job and unproven local launcher/source correspondence are
not erased by choosing another proposed experiment. RP-1 remains consumed,
no retry, with historical RP1_CONTRACT_DEFECT.

The configured `tpcn-luna-workflow` source paths do not exist. Their tracked
repository counterparts are under `workflow`: architecture contract/changelog,
workflow, acceptance criteria, proposal README/template and handoff template.
These counterparts were consulted. No A01-A15 clause changes; A07 scientific
isolation and A08 boundedness are preserved, not newly runtime-verified.
No ACP or production profile promotion is proposed.

Owned deliverables: this separate candidate and a new template-based handoff.
Do not edit the old contract, historical handoffs, existing workflow or source.
No staging/commit/push unless every required decision and independent review
passes and the exact governance publication package is reviewed.

## 2. B01 affirmative adoption from the current owner instruction

Luna-0 affirmatively adopts the policy supplied in this gate as the owner's
B01 amendment, prospectively; it is not an invented approval inferred from
technical reviewers. The old "only privilege entry" wording stays historical.

> SeChangeNotifyPrivilege is required to be the only enabled privilege in the
> restricted Low-integrity child token. Other privileges may remain present
> only when disabled. Complete privilege enumeration and attribute readback
> are required. An unexpected enabled privilege constitutes failure.

Enumerate all LUIDs/names/attributes in source, derived and admitted child
tokens; require ChangeNotify present and SE_PRIVILEGE_ENABLED, and every
other entry without that bit. ENABLED_BY_DEFAULT and USED_FOR_ACCESS do not
substitute for ENABLED. Unresolved names/attributes or cap exhaustion cannot
PASS. Source ChangeNotify must already be enabled; no enabling or repair.

Preserve exactly CreateRestrictedToken(DISABLE_MAX_PRIVILEGE), primary token,
Low `S-1-16-4096`, mandatory policy NO_WRITE_UP | NEW_PROCESS_MIN = 3,
the frozen SID/group deny-only rule (including integrity-group treatment),
no restricting SIDs, non-elevated Medium same-session invoking account,
no new privileges or administrator elevation. No AdjustTokenPrivileges,
second constructor, TokenDefaultDacl/TokenOwner repair, alternate creation
API, account change, impersonation or privilege acquisition is authorized.
Launcher forbidden-privilege presence rules stay as in the old contract.
B01 adoption alone does not approve direct launch or authorize RP-2A.

## 3. Verified direct-base identity and scope of simplification

**OBSERVED, read-only on this checkout:** expected executable
`C:\Users\Patrick\AppData\Local\Programs\Python\Python311\python.exe`;
SHA-256 `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F`;
FileVersion/ProductVersion 3.11.4, OriginalFilename python.exe;
PE signature 0x00004550, machine AMD64 0x8664, PE32+ magic 0x020B.
These agree with the retained RP-1 3.11.4 64-bit observation and R7 identity.
No interpreter was launched to obtain a new sys.version.

Static existence checks found base `Lib\site-packages\pytest\__init__.py`
and `_pytest\__init__.py`, and `distutils-precedence.pth` (151 bytes).
Base python311._pth, python._pth and pyvenv.cfg were absent at these exact
paths. This is NOT a complete import closure or proof of import success.
User-site, startup hooks, registry/search-path resolution, cwd precedence,
DLLs and all transitive imports require later static identity binding.
Do not install packages, use venv site-packages through PYTHONPATH, add -S/-I,
change cwd or remove pytest from the workload on a failure.

**HYPOTHESIZED:** one Low base process can eliminate the venv-created second
process and let the trusted parent supply that process/thread's descriptors
and retain its creation-returned observation/control handles. This removes
the missing descendant-handle route from this experiment only.
No source correspondence or Windows feasibility is presumed.

Only one CreateProcessAsUserW attempt uses this exact absolute executable.
Application name is explicit; mutable quoted argv is that path plus
`-B -c <the fixed synthetic literal>`. No arbitrary executable or fallback.
Flags: CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT |
EXTENDED_STARTUPINFO_PRESENT | DETACHED_PROCESS. Attributes: HANDLE_LIST
exactly three writes; JOB_LIST exactly the owned configured probe job.
No post-creation job assignment workaround or breakaway flags.
Restricted-primary-token exception for SeAssignPrimaryToken does not prove
the quota-privilege requirement succeeds on this host; 1314 fails, no repair.

Expected topology is Medium trusted probe -> one Low base process, no venv
image or other job member. Eight processes remains a safety backstop only.
The process's image/hash/creation-time/PID and READY PID bind identity;
sys.executable is supporting evidence, never sole image proof.

## 4. Exact descriptor targets and access matrix

U = `S-1-5-21-3301679920-2322392626-2066554248-1001`.
M = `S-1-16-8192`; L = `S-1-16-4096`; OW = OWNER RIGHTS `S-1-3-4`.
U is expanded literally in each target SDDL. DACLs are protected; no
inherited/default allow ACE is silently substituted. No audit SACL is queried.
Mandatory-label readback uses LABEL_SECURITY_INFORMATION, not audit-SACL
access or SeSecurityPrivilege. Owner/DACL/label are independently read back.

Target X-M:
`O:S-1-5-21-3301679920-2322392626-2066554248-1001D:P(D;;0x00060000;;;OW)S:(ML;;NWNR;;;ME)`

Target X-L:
`O:S-1-5-21-3301679920-2322392626-2066554248-1001D:P(D;;0x00060000;;;OW)S:(ML;;NW;;;LW)`

Each has one OWNER RIGHTS deny READ_CONTROL | WRITE_DAC, zero allow ACEs.
It is NOT a NULL DACL and not literally an empty zero-ACE DACL.
OW suppresses implicit owner READ_CONTROL/WRITE_DAC; no child-enabled SID
gets an allow ACE. Existing handle capabilities are distinct from DACL
grants and are not revoked by the descriptor. Own-process/thread pseudo
handles and token query behavior are not a claim of hostile self-denial.

Pipe target P-L:
`O:S-1-5-21-3301679920-2322392626-2066554248-1001D:P(D;;0x00060000;;;OW)(A;;0x0012019B;;;S-1-5-21-3301679920-2322392626-2066554248-1001)S:(ML;;NW;;;LW)`

P-L intentionally permits U the read/write creation operations for these
three pipe objects only: union FILE_GENERIC_READ | FILE_GENERIC_WRITE =
0x0012019F minus FILE_CREATE_PIPE_INSTANCE/APPEND_DATA (0x4) = 0x0012019B.
No generic-write ACE inadvertently permits another pipe instance.
Creation-returned pipe access may contain API-mandated extras; it must be
enumerated, not inferred from the ACE. Low pipe labels permit authorized
WriteFile; a Medium NO_WRITE_UP pipe would contradict this workload.
This pipe ACE is not a process/thread ACE or evidence-tree permission.

| Object | Owner / DACL / object label target | Authority and ownership | Admission, inheritance and cleanup |
|---|---|---|---|
| Medium trusted launcher/probe process | X-M; Medium token independently required | Future outer caller retains creation-returned PROCESS_ALL_ACCESS 0x001FFFFF, verifies rights; uses query/wait/terminate only; probe self access is not a new child capability | No child inheritance. Existing shell/VS Code process SD is NOT claimed to be X-M. Exact future outer creation/admission mechanism is an unresolved prerequisite, not permission to relabel/edit it. |
| Launcher initial/reader threads | X-M for newly explicitly created trusted threads; existing runtime-thread SDs require binding, not invention | Outer initial thread handle closes after necessary use; probe owns exact worker handles for cancellation/wait, never child | Need exact worker creation/descriptors and supported outer invocation in RP-2A; no arbitrary OpenThread or thread-control grants. |
| Restricted Low base Python child process | X-L passed through non-inheritable lpProcessAttributes | Parent creation-returned PROCESS_ALL_ACCESS 0x001FFFFF; no reopening required for query/snapshot/duplicate/wait/terminate | Suspended SD/token/image/job/handle readback before one resume; never inherit/transfer process handle; close after cessation and observations. |
| Initial Low child thread | X-L passed through non-inheritable lpThreadAttributes | Parent creation-returned THREAD_ALL_ACCESS 0x001FFFFF; resume 0x2, query 0x40, wait 0x00100000 | One ResumeThread only after admission; no child inheritance; close after final use. No thread termination alternative. |
| Stdout pipe | P-L, separate anonymous object | Probe owns read and write ends initially; child receives write only, not read | CreatePipe with explicit SD and initially non-inheritable handles; enable only write for HANDLE_LIST; parent closes write before resume; reader drains/waits/cancels and closes read. |
| Stderr pipe | P-L, distinct object | Same ownership; independent stream and grammar | Same exact allowlist/closure rules; stdout success cannot stand in for stderr evidence. |
| Synthetic-ledger pipe | P-L, distinct object | Same ownership; decimal write handle in frozen environment | No fourth/control pipe, file handshake or TPCN ledger fixture; validate object/value/mask independently; close parent write before resume. |
| Unnamed probe Job Object | X-M passed to CreateJobObjectW; no other process obtains a handle | Sole non-inheritable parent creation-returned JOB_OBJECT_ALL_ACCESS 0x001F003F; query 0x4, set 0x2, terminate 0x8 | Never duplicate/inherit job handle. JOB_LIST references membership, not child handle possession. Close last after termination/observation, kill-on-close; failures remain explicit. |
| Source launcher primary token object | Existing owner/DACL/label preserved; exact actual descriptor not yet bound | OpenProcessToken QUERY, DUPLICATE, READ_CONTROL union = 0x0002000A, non-inheritable; source TokenOwner/DefaultDacl also read, never changed | Existing token object SD is NOT inferred from Medium token IL; future bounded descriptor binding required. Close reference on all paths; no child transfer or adjustment. |
| Derived restricted token object | Constructor-generated actual owner/DACL/label, currently unbound; no SD parameter to CreateRestrictedToken | Parent returned handle mask queried; needs QUERY, DUPLICATE, ASSIGN_PRIMARY, ADJUST_DEFAULT, READ_CONTROL union = 0x0002008B for Low IL, creation and readback | Never inherited; no DACL/owner/mandatory-policy repair. Token-object label differs from token's TokenIntegrityLevel. Exact SD binding and safe reference access remain unresolved; no invented X-M default. |
| Admitted child primary-token query reference | Child token object SD remains constructor/creation-generated, actual not yet bound | Parent OpenProcessToken from retained child process, QUERY, READ_CONTROL union = 0x00020008 only, non-inheritable | Used for independent U1 readback, closed after query; no child-token mutation. Failure yields incomplete/mismatch, never a guessed token. |
| Negative-control sentinel event | X-M explicit CreateEventW SD; inert unnamed event | Probe returned handle EVENT_ALL_ACCESS 0x001F0003, actual rights read back; inert comparison references only | Deliberately inheritable sentinel omitted from HANDLE_LIST; no signalling/child protocol. Close after snapshot comparisons. |

Handle references are not securable objects with independent owner/DACL/label;
the table names the referenced objects and separately specifies capabilities.
Required masks are admission requirements, not proof the API grants them.
Read-control queries and token SD access may fail under actual ACLs; no
WRITE_DAC, WRITE_OWNER, SeDebug, label/ACL repair or additional privileges
may be acquired to rescue them.

Parent reduced child observation handle, if used, is 0x00121440
(SYNCHRONIZE | READ_CONTROL | QUERY_INFORMATION |
QUERY_LIMITED_INFORMATION | DUP_HANDLE); add TERMINATE = 1 only for parent
termination. Initial child-thread reduced union is 0x00100042.
Local reduced/reference duplication is non-inheritable within the probe only,
same or lesser rights, never DUPLICATE_CLOSE_SOURCE. Job duplication forbidden.
Observation duplicates of child pipe handles use same-access, non-inheritable
references only and are closed promptly; they can keep a writer alive and
must close before EOF is assessed. Snapshot references/markers are probe-only.

The parent retains returned child/thread handles to avoid reopening an X-L
process with zero allow ACEs. This is a design route, not proof that X-L works
with Python initialization, that all parent-process accesses are denied, or
that self/owner/MIC behavior provides U4/U6. No hostile access tests are added.
Exact outer-launcher/thread admission and actual token-object descriptors
remain explicitly incomplete. These must not be hidden by root-handle success.

## 5. Direct-launch inheritance, environment, workload and U1-U3

Child environment remains exactly PYTHONHASHSEED=0,
TPCN_LUNA65_LEDGER_HANDLE=<decimal inherited ledger write>,
PYTHONDONTWRITEBYTECODE=1, SYSTEMROOT=<verified host SystemRoot>.
No __PYVENV_LAUNCHER__, PATH, TEMP, TMP, USERPROFILE, LOCALAPPDATA,
PYTHONPATH or evidence path. Direct launch creates no intermediate launcher
variable; this does not amend production venv environment semantics.
Unicode double-NUL-terminated block, repository cwd unchanged.
STARTF_USESTDHANDLES gives three-write HANDLE_LIST with bInheritHandles=TRUE,
stdout/stderr set and stdin NULL; actual stdin/console state must be checked.
DETACHED_PROCESS and effective eight-bit job UI mask 0xFF are mandatory.

Preserve the existing section 4 synthetic-workload specification unchanged:
direct imports sys/os/json/ctypes/ctypes.wintypes/time/msvcrt/pytest,
pytest import/version only, read-only runtime/token/stdio/console observations,
one nonce-tagged ASCII READY and END on each of stdout/stderr/ledger,
two-second READY dwell, closes handles, exits zero. No TPCN import, fixture,
plugin discovery, test collection, file writes, network, subprocess or training.
There is no implemented/frozen literal byte identity in the preserved draft;
do not invent one. RP-2A must freeze exactly one literal implementing this
unchanged specification and its quoting/grammar; RP-2B binds its hash.
Direct base prefixes/origins/sys.executable expectations replace venv values,
not workload behavior; static startup/import closure must reflect base roots.
Complete hook/transitive-library identities and absences bind before RP-2B.

U1: source/derived/suspended-child and READY-child token field readbacks,
constructor/API outcomes separate; complete privileges, groups, integrity,
mandatory policy, user, session, type/elevation/restricting SIDs.
U2: base image/hash/PE/version and literal metadata, import origins/content
manifest, exact env/argv/cwd/stdio/console/UI/job membership and exit/outputs.
U3: complete parent and suspended-child inventories, then one runtime-child
snapshot during READY dwell after all three READYs and before any END.
The inherited three handle numbers and object identities remain directly
comparable: no venv stdout/stderr duplication or ledger-forwarding stage.
Runtime-opened handles are classified separately; parent-object matches
outside the allowlist, including sentinel/token/job/reads/evidence/process
references, fail. Missing/capped inspection is not "no leak".

Preserve PSS_HANDLE_BASIC_INFORMATION-only capture/walk, <=256 entries,
no VA clone/dump/system-wide census; DuplicateHandle/CompareObjectHandles
plus reviewed NtQueryObject ObjectBasicInformation 56-byte ABI/access
readback, not OS-reserved PSS GrantedAccess. Query original inheritance flags,
not flags of local duplicate. Resolve errors and actual generic-mapped masks.
Each pipe write must have FILE_WRITE_DATA (0x2), no FILE_READ_DATA (0x1).
No child gets a process/thread/token/job handle from the parent.
Self-opened child query handles do not prove inheritance.

U1-U3 get separate result/evidence fields and explicit not-reached reasons.
Creation/import failure may leave U2/U3 unobserved; that is inspectable failure
evidence, not independently passing U3. Successful stdout or creation alone
never implies U1-U3 PASS. Finite checkpoints cannot exclude transient leaks.
The child may create legitimate runtime duplicates; reconcile those by object
identity, not by asserting its entire census contains only three handles.

## 6. Unchanged single-invocation envelope and failure design

One trusted-parent CreateProcessAsUserW attempt, zero retries/fallbacks.
10 seconds active from probe entry T, <=5 seconds cleanup, 20 seconds
attended outer from O. Finalization ends by min(F+5,T+15,O+20), where F is
first normal terminal outcome or first failure/termination request, including
pre-child failures. No attempt to fill the saved venv stage with extra work.
Preserve the old section 5 independently motivated timing allocations as
upper allowances, not feasibility guarantees or hard real-time claims.

Job limits/readback: 64 MiB (67,108,864) job-memory charge candidate,
8 active-process safety backstop, 5 seconds job user-time with
TERMINATE_AT_END_OF_JOB, KILL_ON_JOB_CLOSE, no breakaway, UI 0xFF.
Only the single expected Python member is accepted. Job-user time is not
aggregate user+kernel enforcement. Parent/PSS memory and outer CPU are
not OS-bounded by this job. No memory/CPU stress or fault-injection workload.

All simultaneously retained files/encoded copies/wrapper capture/intermediates
share <=1,048,576 logical bytes; reserve 131,072 for failure/finalization,
payload <=917,504; record <=16,384 bytes, token buffer <=64 KiB and
enumeration <=256. Reserve-before-write, single-writer accounting, all-file
high-water and final length/hash reconciliation are RP-2A source obligations,
not filesystem quota or same-user-peer protection. Overflow terminates,
bounded drain/discard counters retained; accounting loss cannot PASS.

Start bounded readers before resume. On post-creation failure use
TerminateJobObject; if exact suspended child membership is unconfirmed,
also TerminateProcess on its retained handle, never resume it.
No name-based kill, unrelated-PID enumeration or thread termination.
Outer holds terminate/wait/query over exact probe PID/creation identity only;
if probe is stopped its sole job handle closes, but kill-on-close is NOT
cessation evidence. Outer loss/unknown child state remains fail-closed.
Outer admission/stop mechanism still needs an exact reviewed binding.

Wait for child signalled, exit code, job active count zero, all three EOFs;
close all observation write duplicates before EOF. CancelSynchronousIo on
exact reader threads and bounded waits; close snapshots/markers/references,
token/thread/process/pipe/event/job handles on every path, job last.
No blocking read/snapshot may defeat deadline handling; PSS/Windows latency
has no guaranteed bound. Remaining worker/writer/unknown cessation at cutoff
is UNKNOWN_FAIL_CLOSED, not a cleanup PASS.
No child means explicitly no created process, not fabricated EOF/cessation.
Evidence leaf/path/reparse preflight and retain-not-delete obligations from
the old contract apply; no new evidence directory is created in this gate.

Retain section 6 classes and precedence: UNKNOWN_FAIL_CLOSED first for
unknown cessation; otherwise CONTRACT_DEFECT > FAIL > PARTIAL > PASS.
Actual mismatch/API failure is FAIL, missed unsupported observation with
confirmed cessation PARTIAL, unapproved changes CONTRACT_DEFECT.
All limits are unqualified and unexecuted; no runtime RP2_PASS is claimed.

## 7. Original venv design and production compatibility remain separate

| Frozen venv RP-2 | Proposed direct-base RP-2 only |
|---|---|
| Venv root plus distinct base descendant | One expected base process |
| Base descriptors chosen inside stock launcher | Trusted parent passes both child descriptors |
| Base handles initially held by venv | Trusted parent retains returned base handles |
| Root HANDLE_LIST then generic second-boundary inheritance | One explicit inherited-handle boundary |
| Intermediate __PYVENV_LAUNCHER__ and redirected prefixes | Exact four variables and reviewed base prefixes |
| Launcher internal job behavior/source correspondence unresolved | No venv-owned job in this experiment |

Direct-base evidence does NOT establish venv launcher compatibility,
root-to-base handle forwarding, venv internal Job Object behavior,
venv-specific environment/startup propagation, or full production
`-B -m pytest -q -x -p no:cacheprovider tests/test_luna65_capacity_direct.py`
compatibility. These are independent prerequisites whenever that frozen
production profile is used. The fixture remains absent and unauthorized.
Do not replace the production interpreter or claim full B-min qualification.
U4-U8, peer tampering, network containment, Low-writable coverage,
label-at-creation enforcement and supervisor recovery remain unproven.

## 8. Owner decisions, independent review and publication gate

Proposed owner approval D-RP2-DIRECT-1, NOT accepted:

> For RP-2 only, approve the exact hash-bound direct-base Python 3.11.4
> AMD64 executable in section 3 instead of the frozen venv-launcher chain.
> Approve a single-process experimental profile using the reviewed restricted
> primary token, CreateProcessAsUserW, suspended process/thread descriptors,
> exact three-handle inheritance, unchanged synthetic-workload specification,
> four-variable environment and 10/5/20-second, 64-MiB, eight-process,
> five-second-user-time, one-MiB candidate envelope. This is not a production
> interpreter change and does not close any venv-specific prerequisite.
> Implementation and execution require separate later RP-2A/RP-2B grants.

This decision cannot waive unresolved descriptor or outer-admission design.
Outstanding contract-level specifics: actual source/derived/child token-object
owner/DACL/label binding and a compatible exact Medium outer-launcher and
worker-thread descriptor/admission route without existing-object security edits.
No permission to fabricate those values, use default SD as X-M, add privileges,
or introduce an unreviewed helper is granted. A fresh reviewed correction
must close them before implementation readiness is claimed.

A-D each inspect the SAME final checkout SHA-256, verify it themselves and
report design feasibility separately from owner approval/runtime evidence.
A token/privilege/process security; B direct interpreter/inheritance;
C resources/cleanup/evidence/failure; D owner scope/provenance/isolation.
No edits after identity freeze. Findings and exact verdicts go in the handoff.
All-lane contract completeness yields
**PASS - RP-2 DIRECT-INTERPRETER CONTRACT READY FOR OWNER DECISION**;
any missing contract specifics yields
**BLOCKED - RP-2 DIRECT-INTERPRETER CONTRACT INCOMPLETE**.
Pending owner approval alone is not a technical incompatibility.

No governance publication while any required decision or review is outstanding.
Future publication allowlist: this candidate, its new handoff and an additive
workflow entry, independently reviewed as a package before commit/push/fetch.
Preserved old contract/reviews stay excluded and byte-identical.
Review identity is not publication identity. No publication performed here.

After closure and owner decision: separate RP-2A source allowlist authorization,
then exact FFI/SD serialization/rights/outer admission/quoting/literal/closure/
schema/readers/accounting/cleanup static review, reviewed source publication
and fetched-identity verification. Any needed wrapper/helper needs separate
source-allowlist authority; no silent expansion of old single-file allowlist.
RP-2B later names source/literal hashes, exact outer command/capture, run ID,
fresh path/preflight/operator and stop procedure. No static PASS authorizes it.

RP-2 implementation/execution, RP-3, supervisor implementation/qualification,
Phase 2A/2B fixtures NOT AUTHORIZED; full Spiral and Luna-64 corrective
execution BLOCKED; Luna-63C FROZEN.

## 9. Documentation basis, not host API evidence

- [CreateRestrictedToken](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createrestrictedtoken)
- [CreateProcessAsUserW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasuserw)
- [CreatePipe](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-createpipe)
- [Mandatory integrity control](https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control)
- [Token owner](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_owner)
- Preserved contract sections 3.1, 9 and 10.6 supply the PSS/NtQueryObject,
  process rights, OWNER RIGHTS and stock-venv documentation basis.
