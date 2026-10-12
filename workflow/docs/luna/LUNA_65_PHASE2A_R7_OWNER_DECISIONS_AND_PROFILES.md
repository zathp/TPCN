# Luna-65 Phase 2A R7 Owner Decisions and Security-Profile Closure

**Gate:** `L65-PHASE2A-R7-OWNER-DECISION-AND-PROFILE-CLOSURE`
**Role:** Luna-0, governance and Windows security design only.
**Status:** contract text for independent review. Not an authorization.

This document records the owner's R7 decisions, resolves D-R7-4 by design,
and states the complete simplified (B-min) supervisor contract at source
level. It implements nothing, runs nothing and qualifies nothing. It amends
[the published R7 simplification review](LUNA_65_PHASE2A_SUPERVISOR_SIMPLIFICATION_R7.md)
only where this document says so; R7 stays as published.

## 1. Baseline and provenance

| Item | Verified value |
|---|---|
| Branch | `governance/luna64-r4.3-freeze-20261010` |
| Expected R7 baseline | `2e6095dd72a82fcea0b0634776bca0ea5f262123` (ancestor of HEAD) |
| HEAD at start | `baf03722e3b8a21e3af65602691cdb63663e1dd3` = `origin/<branch>` |
| R7 contract (published) | SHA-256 `7096BB6782CFE1092B5B4F4DF1803788664D69DCFADF4F885D78F00066C073E2` |
| R7 handoff (published, checkout bytes) | `73786CA64F3A28F98A42531AE8920ED069DE6FE9069EB7131D31382AC8884998` |
| Capacity contract (checkout bytes) | `234043BC7963AE603C1AC0E419691DE60D14760405614E6C1057BAA8F0D971DE` |
| Resource policy R2 (checkout bytes) | `D7BB88F3A6BECC88D32BAFCE0546E72E42B5E3F29E266A94BDAB41294D9723E2` |
| R6 contract / handoff | `5747D1DD…C152` / `8D681CAF…C3D2` (unchanged, BLOCKED verdict preserved) |
| Scaffold (untracked, local) | `67542EDF59EBB236B61B2714000D7DBFC89462F7352F7C92346673D45CDA0AA1`, verified from actual bytes |
| Scaffold draft branch | `origin/draft/luna65-phase2a-supervisor-scaffold-20261012` at `9cb909a95392c971b98ffa796a015ab90e032f1f` |

The task text calls R1/R2/R6 and the Authorization I entry "unpublished".
They were published after R7, in `baf0372` (byte-preserved, BLOCKED verdicts
intact). The scaffold stays untracked locally and on its separate draft
branch, is nonoperational, unqualified and not executable, and is not
published under this task. Luna-63C records remain frozen and Luna-64
corrective records blocked; neither is touched.

Owner-decision provenance: the owner's instruction text for this gate was
supplied as a pasted attachment that was accessible at review time
(10,739 bytes, 334 lines, SHA-256
`F25EAD255CF10059738059A41B0894A32746823C0C516B872647E82588B0A4F8`). That
hash identifies the pasted text only. It is **not** the hash of the earlier,
inaccessible R6 owner attachment, which remains unverified and unreproduced.

## 2. Recorded owner decisions

| ID | Decision (owner-accepted) | Reconciliation in this document |
|---|---|---|
| D-R7-1 | **B-min**: minimal watchdog launches and supervises the controller; the controller exclusively owns the workload Job Object handle; watchdog holds only controller terminate/wait authority. Residuals accepted as disclosed: undetectable watchdog hang; watchdog death racing admission; controller hang with watchdog loss. No guaranteed recovery is claimed. | §5 |
| D-R7-2 | **Replacement metric**: 268,435,456 bytes of Windows Job Object job-memory charge replaces aggregate private commit. **Non-equivalence is recorded.** Requires correct configuration, effective-limit observation, descendant accounting, later synthetic qualification. | §6 |
| D-R7-3 | **Narrowed Q03**: owner-C1 = verified Job membership plus OS-enforced no-breakaway. Owner-C2 (injection into an existing process) is **excluded** from the claimed boundary. No system-wide process-creation detection is claimed. The narrower Q03-B outside-child recovery qualification is preserved. | §7 |
| D-R7-4 | Delegated to Luna-0 and reviewers for profile design only. | §4 |
| D-R7-5 | **Preparation only**: a separately reviewable synthetic sizing contract. No records generated, nothing executed. | §9 |
| D-R7-6 | Heartbeat 50 ms; stale 500 ms; unconditional watchdog controller-termination trigger at `T0 + 135 s`. 115 s early workload stop request, 120 s monitored budget and 15 s trusted observation preserved. No deadline-compliance guarantee is claimed. | §5.4 |
| D-R7-7 | OS user-time limit included as a supplementary backstop. It never replaces the monitored 120 s aggregate user-plus-kernel CPU budget; any observed aggregate-budget exceedance is a failure. | §6.3 |
| D-R7-8 | Retained-artifact metric: aggregate **logical size** of all files under the evidence tree, including temporary and intermediate files while they exist; maximum 1,048,576 bytes; high-water enforcement required, not merely a final check. Filesystem allocation limits and pipe limits are not assumed to establish it. | §8 |

Unchanged owner terms: 120 s monitored aggregate job CPU, 120 s monitored
wall, 115 s early termination request, up to 15 s post-budget trusted
observation (observation time only, never workload execution permission),
bounded cessation-observation intervals rather than exact exit timestamps,
and zero retries.

**Q03 naming reconciliation.** R7 used A/B/C1/C2 with C1 meaning system-wide
detection of outside-job process creation. The owner's D-R7-3 uses C1 for
"verified membership plus OS-enforced no-breakaway". This document adopts the
owner's names:

| Owner name | Meaning | Disposition |
|---|---|---|
| Q03-C1 | verified membership + OS-enforced no-breakaway (R7 "A" with the membership check) | claimed; qualification required (§7) |
| Q03-B | recovery of a cooperatively reported outside child | preserved as qualification requirement, only if no-breakaway read-back fails |
| Q03-C2 | injection into an existing process | **excluded** from the claim |
| (R7 "C1") | system-wide outside-job process-creation detection | **not provided; not claimed** |

## 3. Observed environment (evidence, not configuration)

Read-only probes on 2026-10-12. No system setting was changed and no
supervisor or workload ran.

- Windows 10 Pro, `10.0.19045`.
- Invoking account: `DESKTOP-AFORJRI\Patrick`, SID
  `S-1-5-21-3301679920-2322392626-2066554248-1001`. Token is a **filtered
  standard-user token**: `BUILTIN\Administrators` and the local-account-admin
  group are *deny only*; integrity **Medium**; privileges present:
  `SeChangeNotifyPrivilege` (enabled), `SeShutdownPrivilege`,
  `SeUndockPrivilege`, `SeIncreaseWorkingSetPrivilege`, `SeTimeZonePrivilege`
  (disabled). `SeIncreaseQuotaPrivilege` and `SeAssignPrimaryTokenPrivilege`
  are **absent**.
- Python 3.11.4. Launcher `.venv\Scripts\python.exe` SHA-256
  `B5442B36A3855E9A02E5745DB3449D8EC91F4FFEFD9CF92CC8B0535112F0F0CE`;
  `pyvenv.cfg`: `include-system-site-packages = false`, `home` =
  `C:\Users\Patrick\AppData\Local\Programs\Python\Python311`; base
  `python.exe` SHA-256
  `4FB049EEDDD221E5470CD33177299DD13F85EBA25BEEF7ACED7A0890AD85181F`.
- DACLs on the interpreter, its directory, the repository root and
  `%LOCALAPPDATA%` grant only `SYSTEM`, `BUILTIN\Administrators`, the
  invoking user and `CodexSandboxUsers` (read/execute). **No ACE grants
  `Users`, `Everyone`, `Authenticated Users` or `RESTRICTED`.**
- `%LOCALAPPDATA%\TPCN\evidence` does not exist. `tests\test_luna65_capacity_direct.py`
  does not exist. `.venv` is git-ignored.

These values are bound as expected identities (§4.3); the supervisor must
refuse on any mismatch. The SID is host- and account-specific evidence and is
not a portable constant.

## 4. D-R7-4 — frozen security profiles

All three profiles use **no administrator rights, no elevation and no new
privileges**. Process and thread SDs are created by the parent; unspecified
handle inheritance is **off**.

Common construction: every handle is created non-inheritable unless this
section names it; inheritance is then enabled only by an explicit
`PROC_THREAD_ATTRIBUTE_HANDLE_LIST`.

### 4.1 Minimal watchdog `W`

| Field | Frozen value |
|---|---|
| Identity | the invoking interactive account (the launching shell's user) |
| Token | the launching shell's unmodified primary token (filtered standard user, §3); no restricted/derived token |
| Groups, restricting SIDs | as inherited; none added; no restricting SIDs |
| Integrity | Medium (`S-1-16-8192`); `P` refuses to start the workload if either differs from the runtime read-back |
| Privileges required | none. The program never uses, enables or adjusts any privilege. Accepted token state (read back at start, matching §3): `SeChangeNotifyPrivilege` may be present and enabled (default for standard users; it is not adjusted); every other privilege present must be in the **disabled** state |
| Explicitly forbidden | refuse to run if any privilege other than `SeChangeNotifyPrivilege` is **enabled**, or if any of `SeDebug`, `SeAssignPrimaryToken`, `SeIncreaseQuota`, `SeTcb`, `SeImpersonate`, `SeBackup`, `SeRestore`, `SeTakeOwnership`, `SeLoadDriver` is present in any state (the §3 baseline token contains none of these) |
| Process / thread SD | default owner and DACL from the token, plus a mandatory-label ACE at Medium with `NO_WRITE_UP \| NO_READ_UP`, so a Low-integrity workload cannot open `W` |
| Handles held | only: (a) a duplicate of the `P` process handle reduced to `PROCESS_TERMINATE \| SYNCHRONIZE \| PROCESS_QUERY_LIMITED_INFORMATION` (the full-access `CreateProcess` handle and thread handle are closed immediately); (b) the two heartbeat/ack pipe ends. **No job handle, no workload handle, no evidence-file handle** |
| Inheritance | `W` passes to `P` only the pipe ends and a `SYNCHRONIZE`-only duplicate of its own process handle, by explicit handle list |
| Environment | built explicitly from an allowlist (§4.4); none inherited wholesale |
| Working directory | repository root |
| Read access | repository (source-level behavior) |
| Writable paths | none **by program behavior only**: `W` contains no write code path. This is **not** token- or ACL-enforced; `W` holds the same-user Medium token and could in principle write anything that user can write. Residual R-TRUST (§11) |
| Network | none required, none used |
| Child processes | exactly one: `P` |
| Termination authority | `TerminateProcess(P)` only, by the cutoff rules of §5.4 |
| Source identity | the supervisor source SHA-256 (single file, §10.2) |

`W` authority is `PROCESS_TERMINATE | SYNCHRONIZE | PROCESS_QUERY_LIMITED_INFORMATION`
on `P`. R7 listed `TERMINATE | SYNCHRONIZE`; the added query-limited right is
only for recording `P`'s exit code and confers no job or workload authority.

### 4.2 Trusted controller `P`

| Field | Frozen value |
|---|---|
| Identity / token | as `W`: same user, same filtered Medium token (inherited from `W`, which created it with that token) |
| Privileges | same acceptance rule as `W` (§4.1): no privilege use, enabling or adjustment; `SeChangeNotifyPrivilege` may be present and enabled; every other present privilege must be disabled; refuse if any `W`-forbidden privilege is present in any state or any other privilege is enabled |
| Process / thread SD | as `W` (Medium label, `NO_WRITE_UP \| NO_READ_UP`) |
| Handles held | the sole job handle (unnamed, non-inheritable, never duplicated, `JOB_OBJECT_ALL_ACCESS` as returned by `CreateJobObject`); the workload process handle; controller-side pipe read ends; evidence-file handles; `SYNCHRONIZE`-only handle to `W`; heartbeat pipe ends |
| Inheritance | only the three workload-side pipe write ends reach the workload, by explicit handle list; controller closes its copies of those ends immediately after `CreateProcessAsUser` returns and before resume |
| Environment | allowlist (§4.4) |
| Working directory | repository root |
| Repository access | `P` contains no repository write code path. Read-only is **enforced** only for the **workload** (Low integrity); for `P` it is program behavior, not token/ACL enforced (R-TRUST, §11) |
| Writable paths | only the evidence tree (§8), by program behavior; not token/ACL-confined for `P` (R-TRUST) |
| Evidence root (frozen) | `P` derives `<LocalAppData>\TPCN\evidence\luna65-phase2a\<run-id>` from `FOLDERID_LocalAppData` of its own token (never from an environment variable). `W` passes only the nonce, not the path; `<run-id>` is `<UTC yyyymmddThhmmssZ>-<nonce hex>`. The run directory is created with `CREATE_NEW` semantics; an existing run directory means refuse (no reuse, no overwrite). The root is absent from the workload environment, handle list, command line and working directory. Missing parent directories are created by `P` with the same protected DACL and label |
| Evidence-tree ACL | protected (no inheritance) DACL granting the controller's token user, `SYSTEM` and `BUILTIN\Administrators` full control; **no ACE for Users, Everyone, RESTRICTED or any Low-integrity principal**; Medium label with `NO_WRITE_UP \| NO_READ_UP` (so the Low workload has neither write nor read access); label application at creation without `SeRelabelPrivilege` is prerequisite U6 |
| Network | none required, none used |
| Child processes | only the workload root, created suspended inside the job |
| Termination authority | the job handle (`TerminateJobObject`, kill-on-close) and the exact root-process handle before resume |

### 4.3 Restricted Phase 2A Python workload

The workload runs as a **Low-integrity, privilege-stripped restricted
primary token** derived from `P`'s own token.

| Field | Frozen value |
|---|---|
| Identity | the invoking user's SID remains an **enabled** group (needed to read the interpreter and repository, whose DACLs name only that user; §3) |
| Token type | primary, `CreateRestrictedToken` of `P`'s token with `DISABLE_MAX_PRIVILEGE`, then `SetTokenInformation(TokenIntegrityLevel)` to Low (`S-1-16-4096`) |
| Groups | every group of the source token is made *deny-only* via `SidsToDisable` **except** the user SID, `Everyone` (`S-1-1-0`), `BUILTIN\Users` (`S-1-5-32-545`) and `Authenticated Users` (`S-1-5-11`) |
| Restricting SIDs | **none, by design.** A restricting-SID list needs a DACL grant to a restricting SID on the interpreter and repository; the observed DACLs grant none to `RESTRICTED`, `Everyone` or `Users`. Adding one would be a system ACL change and is therefore not used. Containment instead rests on Mandatory Integrity Control (below) |
| Integrity | Low. Default token mandatory policy `NO_WRITE_UP \| NEW_PROCESS_MIN` is required and read back; `NEW_PROCESS_MIN` keeps descendants at or below Low |
| Privileges required | none. `DISABLE_MAX_PRIVILEGE` removes all but `SeChangeNotifyPrivilege`, which is retained (needed for path traversal; deleting it risks breaking interpreter loading) and is read back as the **only** privilege |
| Explicitly disabled | all other privileges, including those in §4.1; read back before resume |
| Process / thread SD | created by `P`; `P` holds all access; no ACE grants workload-side principals |
| Handle access / inheritance | only three inherited handles: stdout write, stderr write, ledger write (all anonymous pipes). No directory, file, process, job or token handle. No `DuplicateHandle` authority over `P`/`W` (their Medium labels with `NO_READ_UP`; verified by qualification, not assumed) |
| Environment | allowlist (§4.4) |
| Working directory | repository root |
| Interpreter identity | launcher `.venv\Scripts\python.exe` (SHA-256 §3, bound) and the base interpreter it starts (SHA-256 §3, bound); Python 3.11.4; refuse on mismatch. The launcher is expected to create a second process (launcher → interpreter); both stay in the job |
| Script and source hashes | the test file `tests/test_luna65_capacity_direct.py` (does not exist; its blob/SHA-256 and the exact checkout commit must be bound by the future implementation authorization) and the supervisor source SHA-256; clean checkout required |
| Repository access | read only. Writes are denied by `NO_WRITE_UP` because repository objects carry the default Medium label |
| Writable temporary paths | **none granted**. `TEMP`/`TMP` are not provided; `-B` / `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` prevent bytecode and pytest cache writes |
| Evidence tree | no write or read access intended (Medium `NO_WRITE_UP \| NO_READ_UP` label + protected DACL + no handle); denial verified by qualification, not assumed (U4, U6) |
| Network | **not technically restricted.** Low integrity does not block network access, and Windows Firewall/AppContainer need system configuration. Phase 2A requires none; absence of network use is an assumption to be confirmed by static review of the test, not an enforced property. Requires owner decision if enforcement is wanted |
| Child processes | permitted only within the job: launcher → interpreter chain; `JOB_OBJECT_LIMIT_ACTIVE_PROCESS` proposed at 8 pending Q01 observation; no breakaway |
| Termination authority | none over `P`/`W`; whole-job termination by `P` only |

### 4.4 Environment allowlist and the published "two overrides" statement

The published capacity contract permits only `PYTHONHASHSEED` and the external
evidence-directory setting. Under the owner's controller-owned evidence
design the workload must **not** hold the evidence path, so this document
amends the *workload* environment allowlist as follows (all other variables
absent):

| Variable | Value | Reason |
|---|---|---|
| `PYTHONHASHSEED` | `0` | published |
| `TPCN_LUNA65_LEDGER_HANDLE` | decimal value of the inherited ledger pipe handle | replaces `TPCN_LUNA65_EVIDENCE_DIR` for the workload; the test must write canonical JSONL records to this handle and not to a path |
| `PYTHONDONTWRITEBYTECODE` | `1` | no workload write attempts |
| `SYSTEMROOT` | the host's `%SystemRoot%` | required by Windows/Python runtime |

`P` and `W` use the same allowlist plus the run nonce and `T0` carried over
their pipes, not the environment. The substitution and the three hygiene
variables are a reconciliation of the published capacity contract's
environment term; they are flagged for explicit owner acknowledgement in the
implementation authorization (§12).

### 4.5 Sequence feasibility and unresolved profile prerequisites

Exact intended sequence in `P`:

1. Verify own token: non-elevated, Medium, user SID equals `W`'s, no forbidden privilege; verify `W` ack (§5.2).
2. Verify file identities (§3); verify clean checkout; read-only.
3. Create the evidence tree with the protected ACL and Medium label; reserve budget (§8).
4. Create three anonymous pipes; mark only the workload ends inheritable.
5. Create the unnamed job; configure limits (§6); read back effective flags and limits.
6. Build the restricted Low token (§4.3); read back groups, privileges, integrity, mandatory policy.
7. Build the environment block (§4.4).
8. `CreateProcessAsUser` (suspended, detached, extended startup info with `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` and `PROC_THREAD_ATTRIBUTE_JOB_LIST` containing the job, std handles redirected to the pipes). The process begins life inside the job, so there is no separate assignment race; "failed process assignment" is a creation failure.
9. Verify membership (`IsProcessInJob`, job process list) and read the child's token back.
10. Close the controller's copies of the workload-side pipe ends (so EOF is observable); confirm the child, not the controller, holds them.
11. Recheck `W` unsignaled; resume only if all checks hold.
12. Monitor (§5.4), terminate, observe cessation, finalize evidence, exit.

Mechanisms that **cannot be established without a runtime probe or system
configuration** are retained as unresolved qualification prerequisites, not
as certainty:

- **U1** `CreateProcessAsUser` with the derived restricted/Low token succeeds *without* `SeAssignPrimaryTokenPrivilege`/`SeIncreaseQuotaPrivilege` (absent here). Documentation describes a restricted version of the caller's own primary token as assignable; this host is untested. If it fails with privilege-not-held, the Low-token workload is **infeasible without privilege or policy configuration** and the owner must decide; no administrator escalation is assumed.
- **U2** The exact interpreter (venv launcher → base interpreter, Python 3.11.4) starts and runs the test under the Low token, with `UILIMIT` restrictions and a detached (no-console) process, and cannot write anything it should not.
- **U3** The launcher passes the ledger handle to its child interpreter (launcher inheritance behavior is undocumented here). If not, owner decision on running the base interpreter directly.
- **U4** The Medium `NO_READ_UP | NO_WRITE_UP` labels on `P`/`W` actually deny a Low process `PROCESS_DUP_HANDLE`, `PROCESS_TERMINATE`, `VM_WRITE` and query rights (Q09).
- **U5** Enumeration of existing **Low-labeled writable locations** (for example the user's `AppData\LocalLow`, and the `AppDataLow` registry key). MIC denies writes to Medium objects but permits Low-labeled ones, so "no writes outside the evidence tree" is **not** claimed; it is restricted to non-Low-labeled objects, and the Low-writable set must be enumerated and either accepted by the owner or removed. Bytes written there are not counted by D-R7-8.
- **U6** The mandatory-label ACE on `P`/`W` at creation without `SeRelabelPrivilege`.
- **U7** Network non-use for the workload (§4.3).
- **U8** Same-user, Medium-or-higher processes (including other sessions) can still tamper with `P`, `W` and the evidence tree; they are outside this boundary.

## 5. B-min supervisor contract (complete)

### 5.1 Ownership

`W` is the first process and creates `P` itself, receiving its handle from
`CreateProcess` (no duplication into `W`). `P` owns the sole job handle.
Neither process holds a named kernel object, ETW session or observer. There
is no bootstrap job, observer job, handle-transfer protocol or status pipe.
No additional helper may be introduced without a separately justified
requirement.

### 5.2 Startup, readiness and nonce-bound acknowledgement

`W` generates a 128-bit run nonce, creates the two anonymous pipes and `P`,
and sends `T0` and the nonce. `P` emits heartbeat sequence 1 carrying the
nonce; `W` replies with an acknowledgement bound to the nonce and sequence 1.
`P` validates it before creating the suspended workload. Readiness is
established only by that exchange. Any timeout, mismatch or either process's
earlier exit fails closed before resume.

### 5.3 Admission-death race (acknowledged residual)

`P` checks that `W` is unsignaled immediately before creating the workload
and again immediately before resume. The check is not atomic with `W`'s death
between that check and workload start. This is a disclosed D-R7-1 residual:
design-controlled, qualification-required, **not guaranteed**.

### 5.4 Monitoring, timing and cutoff

- Heartbeat emitted by `P`'s control loop (never an independent thread) every 50 ms with sequence and QPC; `W` requests termination of `P` when none arrives for 500 ms.
- `P` samples job accounting at 10 ms; an accounting gap over 100 ms or a failed query closes admission and requests whole-job termination.
- `P` requests whole-job termination at `T0 + 115 s`; monitored workload budget 120 s CPU and 120 s wall; trusted observation continues up to 15 s and is observation only.
- `P` stops new observations and durably commits its terminal record and manifest by `T0 + 130 s`, then sends `W` a nonce-bound committed-status message. That message is evidence delivery only.
- **Unconditional cutoff:** `W` requests `TerminateProcess(P)` at its first control-loop execution at or after `T0 + 135 s` if `P` is still alive. A committed status never waives it. This is a logical cutoff, not a guaranteed physical kill time; `W` records late-wake and request timestamps. If the cutoff precedes commit, uncommitted evidence is incomplete.
- All blocking calls in `P` (file writes, pipe reads, termination) run on single-flight worker threads and never in the control loop.
- None of these parameters guarantees deadline compliance. Timeliness of kill-on-close and `TerminateJobObject` has no documented bound.

### 5.5 Failure behavior (unchanged from R7 §5/§9, restated for the frozen profiles)

| Condition | Classification |
|---|---|
| `P` crash after admission (sole handle closes) | OS-enforced kill-on-close; cessation interval design-observed |
| `P` hang after admission | design-controlled (`W` converts to death) + OS-enforced follow-through; qualification required |
| `W` crash after admission | `P` observes, terminates the job, finalizes as controller-supervised failure; design-controlled |
| `W` hang | **undetectable**; hung-controller defense lost for the rest of the run; unresolved (accepted residual) |
| `P` hang with `W` dead or hung | **unresolved**; no independent mechanism beyond the OS user-time backstop; recovery not claimed |
| `W` and `P` both dead | OS kill-on-close; cessation unconfirmed; fails closed |
| Job-handle duplication or leakage | design-controlled (non-inheritable, never duplicated, no named object) + runtime qualification; same-user Medium processes with `DUP_HANDLE` on `P` remain an unresolved risk (U4/U8) |
| Failed creation or membership read-back | design-controlled fail-closed before resume |
| Failed process termination | unresolved; no claim of guaranteed termination |
| Evidence-writer failure | design-controlled: drain-and-discard, mark `EVIDENCE_INCOMPLETE`, request termination |
| Job-memory exceedance | OS-enforced limit (metric per §6), runtime qualification of its observable behavior |
| Wall/CPU budget violation | design-controlled (monitored); user-time backstop OS-enforced partially |
| Process escape | OS-enforced no-breakaway when read back (§7); Q03-C2 excluded; owner-accepted |
| Incomplete cessation evidence | recorded as an observation interval or "unconfirmed"; never silently complete |

## 6. Job Object and memory policy

### 6.1 Configuration (read back before resume)

Unnamed job; `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; **no**
`BREAKAWAY_OK`, `SILENT_BREAKAWAY_OK`; `JOB_OBJECT_LIMIT_JOB_MEMORY` at
268,435,456 bytes; `JOB_OBJECT_LIMIT_ACTIVE_PROCESS` (proposed 8, to be
confirmed at Q01); the OS user-time limit (§6.3);
`JobObjectEndOfJobTimeInformation` explicitly set to
`JOB_OBJECT_TERMINATE_AT_END_OF_JOB` and read back; basic UI restrictions
(`JOB_OBJECT_UILIMIT_*` handles, desktop, display settings, exit windows,
global atoms, clipboard, system parameters), unless Q01/U2 shows Python cannot
start with them, which would be an owner decision. Limit flags and values are
read back through `JobObjectExtendedLimitInformation` and
`JobObjectBasicUIRestrictions` and must equal the configured values before the
workload resumes.

### 6.2 Memory metric

The enforced and reported metric is the **Job Object job-memory charge**
(`JobMemoryLimit` 268,435,456; `PeakJobMemoryUsed` observed), applied to all
job members including descendants. **Non-equivalence is recorded:** Windows
does not document this charge as equal to, or conservatively stronger or
weaker than, the earlier "aggregate private commit" (sum of members'
`PrivateUsage`). No claim is made in either direction, and no result obtained
under this metric is evidence under the old one. The 268,435,456-byte
numerical ceiling is unchanged. `P` and `W` are outside the job and are not
counted.

Required before any reliance: correct configuration and read-back (§6.1);
observation that the effective limit is in force (Q06 demonstrates that a
commit beyond it fails within the job, including from a descendant); descendant
accounting (Q01/Q06); and per-sample records of `PeakJobMemoryUsed` and
allocation-failure outcomes. Failed commits are distinct evidence from
terminations.

### 6.3 CPU backstop (D-R7-7)

`JOB_OBJECT_LIMIT_JOB_TIME` with the end-of-job action above is a
**supplementary backstop only**: it counts user-mode time, is checked
periodically, and cannot fire before combined user-plus-kernel CPU reaches
120 s because combined CPU ≥ user CPU. It never replaces the monitored
120 s aggregate user-plus-kernel budget; any observed aggregate exceedance is
a failure regardless of backstop state. Wall time and combined CPU are
design-monitored, not OS-enforced.

## 7. Q03 assurance boundary

Claimed (owner-C1): job membership verified by `IsProcessInJob` and the job
process list before resume; descendant inheritance; OS-enforced no-breakaway
(no breakaway limit flags, read back); no child ends up outside the job under
that configuration. The pass criterion is "no outside-job child", not
`CreateProcess` failure.

Preserved (Q03-B): if the read-back or runtime evidence shows a child outside
the job, recovery of a cooperatively reported outside child is a separate
qualification requirement.

Not claimed: Q03-C2 injection into an existing process; system-wide
process-creation detection; attribution of the requester of any creation; any
containment against same-user Medium processes. The `Job Object` cannot
contain a process created by a different, uncontained party.

## 8. Artifact enforcement design (D-R7-8)

The controller is the **only** writer to the evidence tree. The workload has
no write path to it (§4.3) and no handle to it. Workload stdout, stderr and
the JSONL ledger arrive only through the three controller-owned anonymous
pipes; their workload-side ends are the only inherited handles, and the
controller closes its copies of them immediately after creation.

- **Metric:** Σ logical size (end-of-file length) of every file under the evidence tree, including `.partial`, temporary and intermediate files while they exist, plus any alternate streams (none may be created). Cap 1,048,576.
- **High-water enforcement:** one accounting object, reserve-before-write. Before every write of `n` bytes to file `F` with current logical length `L_F`, the controller checks `Σ_current + n ≤ cap − reserved_remaining`; otherwise it writes nothing. The accounting tracks the maximum reached. A tree enumeration at checkpoints and at finalization **verifies** (not replaces) the accounting; any excess is a failure.
- **No preallocation, no `SetEndOfFile` extension, no sparse files:** each would change logical size outside accounting. No truncation: complete records are kept and the run is marked incomplete.
- **Buffering and pipes:** three reader threads feed a bounded queue (sizes frozen at implementation authorization from the sizing result) into a single writer. Pipe capacity does not enforce the cap; when the writer cannot accept bytes, readers drain and discard, count the dropped bytes, and the run is marked `EVIDENCE_INCOMPLETE`. A dropped ledger record is never silently omitted: a gap-marking record is reserved for, or the run fails.
- **Compression:** the ledger is gzip-streamed (RFC 1952, level 9, `mtime=0`, no filename) directly into its final path as `results.jsonl.gz.partial`, accounted at its current logical length. No uncompressed intermediate file exists. The compressed length of each pending chunk is known before it is written, which is the quantity checked. Flush interval and finalization margin (deflate end block plus 8-byte trailer) are frozen from the sizing result.
- **Atomic replacement:** rename of the finished `.partial` to its final name (no copy, no double counting). A manifest or hash file is written to a `.partial` of its own, closed, then renamed.
- **stdout/stderr, failure and hash manifests, `resource.json`, `manifest.json`:** each has a pre-reserved share, written once or streamed under the same accounting. The R2 reservation split (ledger 786,432; stdout and stderr 32,768 each; invocation and resource records 16,384 each; failure and hash manifests 8,192 each; slack 147,456; total 1,048,576) is carried forward; its fit is **unproven** (§9).
- **Cleanup:** failure never deletes complete records. Stray `.partial` files are either renamed as explicitly invalid partial artifacts with recorded length and hash, or removed and the removal recorded. The tree is made read-only after finalization.
- **Not assumed:** filesystem quota, allocation size and pipe limits do not establish the cap; the writer's reservation does.

**Retained blocker:** the exact 1 MiB bound is enforceable for bytes written by the controller. It is **not** enforceable against writes by other same-user Medium processes or by the filesystem itself, and cannot be shown to hold for the 8,196-record ledger until sizing (§9) completes. These remain open; D-R7-8 is not weakened.

**Owner decision D-R7P-2 (required, not assumed).** The D-R7-8 metric is defined over every file under the evidence tree. The architecture can enforce it against the controller and the Low-integrity workload, but not against peer same-user Medium processes, because the workload and `P`/`W` share the user SID and no separate identity is available without administrator action. The owner must either (a) accept that peer same-user tampering is outside the enforced boundary, with the finalization enumeration serving as post-hoc detection that fails the run on any excess, or (b) direct a separate-identity design. This contract does not amend the metric or the cap; it records the gap as a precondition to implementation authorization.

## 9. Synthetic ledger-sizing contract (preparation only; not authorized for execution)

**ID:** `L65-PHASE2A-LEDGER-SIZING-S1`. Nothing here is run, and no record is
generated under this governance task.

- **Schema:** `schema_version = luna65-phase2a-probe-v1`, `fixture_version = l65-phase2a-v1`; the exact record fields and canonical serialization of the published capacity contract (§"Phase 2A JSONL result schema": `json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)`, one LF, gzip level 9, `mtime=0`, no filename).
- **Records:** exactly 8,196 = four counters × 2,049 probes in execution order `input`, `episode`, `lineage`, `output_event`; `probe_index` 1–2,049; probe 2,049 per counter has the exact `E1EventBudgetExceeded` exception object and message from the published contract.
- **Target and coupled-counter fields:** `counter_snapshot_before/after`, `target_counter_delta` (1 for probes 1–2,048, 0 for 2,049), `coupled_counter_deltas`, `preparation_counter_deltas` (output-event only), `allocated_identity`, `state_checkpoint`, `post_rearm_checkpoint`. Values are produced by closed-form formulas of `(counter, probe_index)`; coupled deltas follow the published contract's rules (lineage identity on admissions, episode identity on new-M admissions).
- **Two deterministic profiles:** *nominal* (structured, derived values) and *width-bound* (every integer at its maximum digit width, every `x`/timestamp a maximum-length finite binary64 `repr`, identity strings at maximum length, high-entropy low-order digits). The width-bound profile is a conservative upper-bound estimator of per-record cost, not a prediction of real values. The generator seeds only from a fixed constant; no `random` without fixed seed, no clock, no environment.
- **Generator:** a single new standard-library-only source (`json`, `gzip`/`zlib`, `hashlib`); it **must not** import TPCN, allocate E2 identities, run the neuron runtime, train, score, or produce Spiral benchmark data.
- **Compression format and counting:** the compressed size is obtained with a counting sink; a `.gz` is written only if it is no larger than the 786,432-byte ledger allocation. Report both uncompressed JSONL length and compressed size, bytes per record, and the margin to the allocation net of the finalization margin.
- **Resource budget (proposal, bounded):** wall 30 s, CPU 30 s, in-process memory below 128 MiB by construction (streaming, one line retained), output ≤ 1,048,576 bytes total under the same accounting, zero retries.
- **Execution model decision:** the supervisor does not yet exist, so sizing runs unsupervised with in-process guards (record-count and elapsed-time checks per record). That is owner decision **D-R7P-1**.
- **Evidence destination:** `%LOCALAPPDATA%\TPCN\evidence\luna65\phase2a-sizing\<run-id>\`, `<run-id>` per the capacity contract's convention; files `sizing.json` (canonical) and `sha256.json`; never reuse a directory.
- **Result classifications:** `FITS_WORST_AND_NOMINAL` (width-bound compressed size within allocation minus margin); `FITS_NOMINAL_ONLY` (nominal within, width-bound over: owner path required); `EXCEEDS_BOTH` (blocker: owner path required before any implementation of the ledger writer); `GENERATOR_FAILURE`.
- **Failure conditions:** any exception, count other than 8,196, nonconsecutive probe index, field-width violation, output over cap, elapsed > 30 s, or non-deterministic output (two in-process generations within the same run must hash identically; this is internal determinism, not a cross-run replay claim) → `GENERATOR_FAILURE`; no retry.
- **Future allowlist (not authorized):** `scripts/luna65_phase2a_ledger_sizing.py` only, with its own contract SHA-256 binding.

**Dependency (explicit):** the flush interval, finalization margin, queue
sizes and the owner's ledger-size path all depend on the sizing outcome. A
completed sizing result of `FITS_WORST_AND_NOMINAL`, or an owner-accepted path
for any other classification, is therefore **required before supervisor
implementation authorization**. It does not authorize or qualify anything.

## 10. Implementation and qualification path (future; none authorized)

### 10.1 Source obligations
Those of R7 §10.1, with §4–§8 of this document replacing the unfrozen token/ACL,
memory-metric and artifact obligations, plus: the watchdog holds no job
handle; the controller verifies all token read-backs before resume; refuse on
any identity, privilege, limit or integrity mismatch; unsupported APIs fail
closed.

### 10.2 Permitted file allowlist proposal
Implementation: `scripts/luna65_phase2a_supervisor.py` only. Sizing:
`scripts/luna65_phase2a_ledger_sizing.py` only, under its own authorization.
Governance of this task: this contract, its handoff and the `LUNA_WORKFLOW.md`
entry. Not allowed: TPCN production modules, fixtures, datasets, tests,
Luna-64/Luna-63C records, and the existing scaffold's publication.

### 10.3 Static-review acceptance criteria
Exact-byte identity and single-file scope; no TPCN/fixture/dataset import; no
ETW; no `DuplicateHandle` of the job handle; job creation parameters,
non-inheritance and read-back; token construction exactly §4.3 with read-back;
handle list and job list in use; no blocking call in the control loop;
reserve-before-write on every evidence write; no truncation, preallocation or
alternate stream path; heartbeat from the control loop; unconditional `T0+135`
cutoff independent of committed status; environment allowlist exactly §4.4; no
network, no retry; owner decisions D-R7-1…8 reflected.

### 10.4 Synthetic qualification requirements
Q01 suspended admission, job-from-birth, process-chain and `ACTIVE_PROCESS`;
Q02 child and grandchild; Q03-C1 no-breakaway and membership; Q03-B only if
needed; Q04 nested jobs on the target build; Q05 user-time limit and sampling
gap; Q06 job-memory limit including a descendant and the effective limit;
Q07 wall termination and the 15 s observation; Q08 controller crash and hang,
watchdog crash and hang, kill-on-close timing; Q09 workload access to `P`/`W`
(U4); Q10 evidence quota, writer failure and ledger gaps; Q11 token read-back,
Low-integrity writes to repository, evidence tree and Low-labeled locations
(U1–U6); Q12 interpreter launcher chain and ledger-handle passing (U2, U3).
Each case needs its own resource budget; none is authorized.

## 11. Outstanding risks and unresolved qualification prerequisites

Hung `P` with dead or hung `W`; undetectable `W` hang; admission-death race;
failed termination; no latency bound on kill-on-close; metric non-equivalence
(owner-accepted); Q03-C2; network not enforced; U1–U8; ledger fit unproven;
same-user tampering outside the boundary; sampling-based CPU monitoring.

**R-TRUST.** `W` and `P` run under the same-user Medium token. Their "no writes outside the evidence tree" and "repository read-only" properties are source-level program behavior, verified by static review, not enforced by token, ACL or label. A defect or compromise of `W` or `P` is not contained by the OS.

## 12. Authorization state and exact future requirements

**Supervisor implementation: NOT AUTHORIZED.**
**Supervisor qualification: NOT AUTHORIZED.**
**Synthetic ledger sizing: NOT AUTHORIZED FOR EXECUTION.**
**Phase 2A fixtures: NOT AUTHORIZED.**
**Phase 2B fixtures: NOT AUTHORIZED.**
**Full Spiral benchmark: BLOCKED.**
**Luna-64 corrective execution: BLOCKED.**
**Luna-63C certification: FROZEN.**

A PASS on this contract establishes source-level contract readiness only.
Before supervisor implementation can be authorized, the owner must provide:

1. A completed and reviewed sizing result, and a decision on D-R7P-1 (unsupervised execution of the sizing run) and on the ledger-size path.
2. Acknowledgement of the §4.4 environment allowlist reconciliation.
3. Disposition of U1 (`CreateProcessAsUser` with the Low token and no assign-primary/quota privilege): proof, or a decision on the alternative, with no administrator assumption.
4. Disposition of U2/U3/U5/U7 (interpreter under the Low token; launcher handle passing; Low-writable locations; network non-use).
5. Disposition of U4/U6: a supported least-privilege method, demonstrated on this host without administrator action, to apply the Medium `NO_READ_UP | NO_WRITE_UP` labels to `W`, `P` and the evidence tree, with the Low-workload access-denial result (DUP_HANDLE, TERMINATE, VM_WRITE, evidence read/write); or an owner-approved redesign. Q09 denial is not claimed until shown.
6. Owner decision D-R7P-2 (§8) on peer same-user tampering and acknowledgement of R-TRUST (§11).
7. The exact checkout commit, the test-file identity, the contract SHA-256 and the supervisor and sizing source hashes to bind.
8. An explicit single-file allowlist and non-execution static-validation authorization.
