# Luna-65 Phase 2A Supervisor Implementation Authorization Proposal — R1

**Gate identity:** `L65-PHASE2A-SUPERVISOR-IMPLEMENTATION-AUTH-R1`

**Status:** **GOVERNANCE-ONLY PROPOSAL — IMPLEMENTATION, QUALIFICATION,
FIXTURES, AND BENCHMARKS NOT AUTHORIZED.**

**Integrated disposition:** **PASS — PHASE 2A SUPERVISOR IMPLEMENTATION
PROPOSAL READY FOR OWNER AUTHORIZATION.**

The four independent reviewers reviewed proposal candidate SHA-256
`BACE017427C432CC938AAEBADD8E823F223CBC861689E416AA4B4D7E8B2CDA8AA`
(Git blob `734c0acb549b03a1cb1020e4df0e1c2f5166b770`). This disposition is
proposal readiness only. Implementation, qualification, fixtures, and
benchmark execution remain unauthorized.

This document prepares a narrowly scoped owner decision for implementing a
Windows Job Object supervisor for the synthetic Luna-65 Phase 2A
direct-neuron capacity fixture only. It is not permission to implement the
supervisor, qualify it, run a fixture, or execute a benchmark. This proposal
does not generalize to Phase 2B, Luna-64, any other benchmark, or autonomous
agent workload.

## 1. Verified baseline and provenance

The baseline and repository identities were verified before drafting.

| Source | SHA-256 at baseline | Git blob at baseline |
|---|---|---|
| Branch / HEAD | `governance/luna64-r4.3-freeze-20261010` / `d11d370a7c97184529845c9cac984fc22018c576` | — |
| `workflow/docs/luna/LUNA_65_PHASE2_CAPACITY.md` | `7201219EF6DA0945C7CBD1032BC818E97CDD010087EA5CBCB662BD68588249DD` | `f60897c2b5759ecc3bdd851c7fbff20f449e3883` |
| `workflow/docs/luna/LUNA_65_PHASE2A_RESOURCE_POLICY_R2.md` | `D7BB88F3A6BECC88D32BAFCE0546E72E42B5E3F29E266A94BDAB41294D9723E2` | `ff05fcba5e7b6f53ccc682bdbec51423570305eb` |
| `workflow/docs/luna/LUNA_65_SUPERVISOR_QUALIFICATION_R1.md` | `7DD5EE88EDAC1AF9049C265D28B8E60DD1558AD80D2EC760575D25DE6FB4D93D` | `1fa07ffc844a5890c9ecc86563243993725fb1b2` |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `DB127D707C256850E693B423F44B0D08B1D8AB60D2EA2827E398E3A85BB4CE88` | `762497eca0151ccd0422d904eb1aef5fb21e12f4` |
| Phase 2A correction handoff | `459E4AC9CAC322A88BF580F2F1016082FEF7E7C9A69369C0322BA7305181E684` | `8be29e8aab67084e1c3a9a73c9c1564b3ec7c2c9` |
| Phase 1 closure handoff | `4B4D7BF378C3C38FFC755106ECE597A6FBEEA9EC712CFB5AFF105989E680E022` | `56807d7c3b22224742cfccb435271ba219852b0b` |
| Phase 1 implementation `tpcn/experiments.py` | `CABB81DA36280E7CDCF614B8B3E2CD5567035C20C6706A85B25B1A73310E967D` | `7c915fb92f05725f4a46855f856ecb3e650cd44b` |
| Phase 1 runtime `tpcn/experiment_excursion_runtime.py` | `DF007154939C6C554A3D914C15CE91C87954BEEEBF29DF416EE27D138F119D5A` | `ecf65095f272f5e94b328c6d17aa7d6c73d02373` |
| Phase 1 focused test | `DE32193D0E87059E995331E6B490DBEFD26020EB11C9EAFF3EBD27316D4C7D1D` | `53bb0c75909fa0ab5098e98891a05f2c8d88500e` |
| Luna-65 Spiral contract | `1F1D4DD96E21EE760D32CDDE4F0415576C9BAE6AF01B82DB2A9C4E1D9FB5C777` | `c526ef7124d4aa2fef90e6949eecfbffb50445a4` |
| Frozen Luna-63C design | `670550183F2E9167A6FDB1A12885E57F96554748F083F2D39D6A057F43BA6B5B` | `7cc5b7d94a683109413cb8f5a9383e305e113c2c` |
| Owner's current instruction attachment | `D6DC68106CC783B3EE4356B5CD7A7E6F8A6332C91A02FE85FE61803101BEC2DA` | Read-only user-provided source; not in repository |
| Architecture contract | `A431D0A430CC49FB53FEED04CF5FF7B206714DE6451C6AB96CBC7FBB3D034883` | `3afc85f86dbc6992e01cb7ca26ebadfb49c09cab` |
| Architecture changelog | `0F009383E927DB9D9DAE863C83EA0D302918D994E2B870E7A739313FAAD5E82A` | `d93440f1e54051b476be15a99d3c8d61f91cc7ed` |
| Acceptance criteria | `2B67B9EE6DA889D7CF5B44C5CAEAF90389479CEB99DE7A6F1D83ED398774D920` | `510f44daab83c4def92c70617e2d5c731c5760d6` |
| Architecture proposal README | `46B3BF8E8A1B2C87E5E19579B274EA750CFAB8BB97FD51367E7E1E8F49B6FEAA` | `79f26032d02b84ffe0e4ca3a6962f11b8881bd75` |
| ACP template | `B1C9EB0B516072029170C258E37B1B4A0BB44141EED787D165E957154FEC98C6` | `5ab234b20cc2395ae78bc3ffecea22b1f027cae7` |
| Luna handoff template | `C6929DE1A68B9EF021E15C97F38E2C291690C0BA9A3249CCF2A5216A1B5E28E9` | `098d57a450d4824fdecb1eddd75b214c4111a776` |

Git inspection confirmed that the expected local branch, `HEAD`, and
`origin/governance/luna64-r4.3-freeze-20261010` all matched before drafting,
and the worktree/index were clean. No tracked supervisor, Phase 2A direct
fixture, supervisor qualification test, or synthetic worker exists at this
baseline. The local Windows target is Windows 10 Pro, 22H2, build
19045.6466 (UBR 6466); this is host identification only, not runtime API
qualification.

The Phase 2A and R2 policies are the controlling resource specifications.
R1 remains historical evidence. The latest authoritative workflow records
Luna-64 corrective work as **BLOCKED** and Luna-63C as **FROZEN**; neither
track's code, budget, or supervisor evidence is reused here.

The prior independent R1 A–D review dispositions and integrated blocked
qualification result are recorded inside the versioned R1 supervisor-design
document above. The four independent R2 design/governance PASS dispositions
and their unresolved engineering gates are likewise recorded inside the
versioned R2 policy document above; neither historical review is upgraded by
this proposal.

## 2. Versioned owner decision — five-second early wall stop

**Decision record:** `L65-PHASE2A-WALL-STOP-DECISION-20261012-R1`

**Owner decision date:** 2026-10-12, as explicitly stated in the current
owner instruction. Primary source: the owner-provided read-only
`Pasted text #1.txt` attachment above, §Mission (line 12), which states:
“The repository owner has explicitly accepted a five-second early wall-stop
margin for qualification design.”

> **OWNER ACCEPTED — FIVE-SECOND EARLY WALL-STOP MARGIN FOR PHASE 2A
> QUALIFICATION DESIGN**
>
> The monitored wall budget remains 120 seconds. The controller's early
> stop-request target is `T0 + 115 seconds`; the nominal margin is five
> seconds. Any observed execution beyond 120 seconds fails. Unconfirmed
> process-tree cessation is a containment failure. This acceptance does not
> establish a strict worst-case termination-latency guarantee.

`T0` is the first main-entry instruction of the trusted supervisor, measured
with `QueryPerformanceCounter` (QPC); record `QueryPerformanceFrequency`.
The invoking host's process-start observation is separately recorded because
the supervisor cannot observe its own pre-entry startup time. The 115-second
point is a monitored termination-request target, not a promise that Windows
will stop the workload by 120 seconds. The already accepted 120-second
aggregate job user-plus-kernel CPU budget is unchanged; no CPU overrun
allowance is introduced.

This is a later, versioned owner decision. It supersedes only R2's earlier
statement that the five-second candidate was not yet owner-approved. R2
remains unchanged as historical provenance. The owner decision does not
authorize implementation, qualification, Phase 2A/2B, or benchmark
execution.

## 3. Frozen Phase 2A resource and invocation contract

| Requirement | Phase 2A proposal |
|---|---|
| Scope | Phase 2A direct-neuron capacity fixture only |
| Monitored aggregate CPU | 120 seconds cumulative job-wide user plus kernel CPU |
| Monitored wall | 120 seconds from `T0`; request whole-job termination at `T0 + 115 seconds` |
| Hard job memory | 268,435,456 bytes; Job Object job-wide commit limit, not per-process or working-set limit |
| Hard retained artifacts | 1,048,576 bytes across all governed retained files |
| Retries | Zero |
| Current test module | `tests/test_luna65_capacity_direct.py` (absent at baseline) |
| Exact fixture command | `.\.venv\Scripts\python.exe -m pytest -q -x tests/test_luna65_capacity_direct.py` |
| Working directory | Git top-level directory; baseline absolute path `C:\Users\Patrick\Documents\ActiveCode\TPCN` |

No Phase 2B fixture, network, Spiral dataset generation, training,
evaluation, scoring, or task input is admitted. Any future source, command,
environment, working-directory, or hash mismatch must be rejected before
workload creation. This proposal does not change neuron, predictive-coding,
reward, eligibility, learning, structural-plasticity, or scientific-fixture
semantics.

### 3.1 Runtime API selection for the recorded Windows target

The following documented Win32 interfaces are the proposed implementation
surface for Windows 10 Pro build 19045.6466. API availability in the
installed Windows version is documented; behavior, update resolution,
security settings, and metric equivalence remain unqualified.

| Purpose | Interface |
|---|---|
| Job creation and lifetime | `CreateJobObjectW`; unnamed, fresh job; non-inheritable handles; restrictive job security descriptor |
| Configure hard memory and close behavior | `SetInformationJobObject(JobObjectExtendedLimitInformation, JOBOBJECT_EXTENDED_LIMIT_INFORMATION)` |
| Exact configured flags | `JOB_OBJECT_LIMIT_JOB_MEMORY | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; explicitly do not set `JOB_OBJECT_LIMIT_BREAKAWAY_OK` or `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK` |
| Memory bytes | `JobMemoryLimit = 268435456` |
| Read-back | `QueryInformationJobObject(JobObjectExtendedLimitInformation, ...)`; require exact effective flags and byte value before resume |
| Aggregate job CPU | `QueryInformationJobObject(JobObjectBasicAccountingInformation, JOBOBJECT_BASIC_ACCOUNTING_INFORMATION)`; retain raw `TotalUserTime` and `TotalKernelTime` (100-nanosecond representation), sum them and report seconds |
| Active members/accounting | `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.ActiveProcesses` and `QueryInformationJobObject(JobObjectBasicProcessIdList, ...)`, with a sufficiently sized bounded buffer; reconcile active PID count |
| Confirm membership | `IsProcessInJob` for the suspended root and every observed child |
| Job lifecycle and limit notifications | `CreateIoCompletionPort`; `SetInformationJobObject(JobObjectAssociateCompletionPortInformation, JOBOBJECT_ASSOCIATE_COMPLETION_PORT)`; consume with `GetQueuedCompletionStatus` |
| Create suspended root | `CreateProcessW` with `CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT | EXTENDED_STARTUPINFO_PRESENT`, `STARTUPINFOEX`, and a `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` containing only approved pipe handles |
| Assign before user code | `AssignProcessToJobObject`; confirm membership and effective limits; only then `ResumeThread` |
| Termination request | `TerminateJobObject`; record request and return/error; do not treat API success as proof of cessation |
| Cessation | Wait for the job handle to signal and separately query zero active members; record individual exit observations when available |
| Per-process commit observation | `GetProcessMemoryInfo(PROCESS_MEMORY_COUNTERS_EX).PrivateUsage` for currently enumerated PIDs; sample and record time skew and query failures |
| Job commit high-water | `JOBOBJECT_EXTENDED_LIMIT_INFORMATION.PeakJobMemoryUsed` |
| Elapsed time | `QueryPerformanceCounter` and `QueryPerformanceFrequency`, never wall-clock time |

The documented `JobMemoryLimit` is a limit on virtual memory that can be
committed for the job. The accepted Phase 2A measure is aggregate concurrent
private committed memory. The Job Object limit is the kernel-enforced
candidate control, but the mapping to the exact accepted private-commit
measure is not declared equivalent by this proposal. Qualification must
demonstrate that the effective job limit prevents the accepted metric from
exceeding 268,435,456 bytes on the target build. If comparison, process
coverage, or high-water evidence is insufficient, classify
`RESOURCE_MEASUREMENT_INCONCLUSIVE` and block qualification; do not
substitute per-process limits or working-set measurements.

`PeakJobMemoryUsed` is a high-water value, not a per-process private-commit
sum. The current aggregate private-commit observation is a timestamped sum
of concurrent `PrivateUsage` readings and has sampling skew. Record failed
commit observations from the synthetic worker through the trusted evidence
channel. A job-memory commit denial does not itself prove whole-job
termination; the controller requests `TerminateJobObject` on a classified
limit failure and independently confirms job cessation.

For memory-limit notification evidence, set and read back a matching
`JobObjectNotificationLimitInformation` value with
`JOBOBJECT_NOTIFICATION_LIMIT_INFORMATION.JobMemoryLimit = 268435456` and
`LimitFlags = JOB_OBJECT_LIMIT_JOB_MEMORY`. Associate an I/O completion port
before workload admission and record `JOB_OBJECT_MSG_NOTIFICATION_LIMIT`
through `GetQueuedCompletionStatus`; Microsoft documents notification-limit
messages as guaranteed. This notification is informational and does not
enforce the memory ceiling. The hard enforcement remains
`JobObjectExtendedLimitInformation` with `JOB_OBJECT_LIMIT_JOB_MEMORY`, which
prevents further job commits beyond its limit. Also record
`JOB_OBJECT_MSG_JOB_MEMORY_LIMIT` if received, but ordinary job completion
messages are not guaranteed; absence is not evidence that no limit event
occurred. Record allocation failures, effective setting read-back, job
high-water, and process-private-commit observations independently. Neither
notification replaces those observations or the termination/cessation
checks.

No Job Object hard aggregate user-plus-kernel CPU limit is used. The user-time
only job limit is not an acceptable substitute. CPU is monitored from the
two aggregate accounting fields and can overshoot between observations.

### 3.2 Fail-closed admission sequence and containment

1. Verify exact trusted supervisor/profile identity, reviewed checkout
   revision and clean source, Python/pytest identities, fixture path/hash,
   argument vector, working directory, explicit environment, evidence
   location, and owner-approved profile. Reject any mismatch before process
   creation.
2. Prepare the controller-owned evidence directory and reserve manifest,
   resource, failure, and hash-manifest bytes before admission. Confirm the
   worker identity has no write access to that directory or arbitrary
   filesystem paths.
3. Create an unnamed job with restrictive DACL and non-inheritable handles.
   Configure exactly the approved extended-limit fields before process
   creation; query them back. Do not set either breakaway flag.
4. Start the independent watchdog and required observer before admitting the
   workload. Verify their identities, restricted handle rights, and
   heartbeat/observer-ready state.
5. Build a new environment block from the reviewed allowlist. Do not inherit
   arbitrary caller environment variables. Create only the exact Python
   command with explicit inherited pipe handles, suspended.
6. Assign the suspended process with `AssignProcessToJobObject`. Confirm
   `IsProcessInJob`, job PID-list membership, and exact effective limit
   read-back. On any mismatch, terminate the still-suspended process, confirm
   its exit, write a failure record, and do not resume.
7. Resume the initial thread exactly once. Begin workload CPU accounting at
   the first `ResumeThread` that succeeds. The wall interval continues from
   `T0`, including preflight, admission, job execution, termination/reaping,
   pipe drain, and evidence finalization.
8. On any runtime failure or stop condition, request whole-job termination,
   record request/result, wait for job signaling, independently observe zero
   active job processes, and retain all resource/failure evidence possible.
   A successful API return alone is not confirmation.

The root job handle is owned by the primary controller and duplicated only
to a separate watchdog with the minimum rights needed to query and terminate
the job; neither process handle nor job handle is inheritable by the
workload. `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` is a final kernel fallback
when the last job handle closes, not a cessation record. The watchdog stays
outside the workload job. If the primary loses heartbeat for 100 ms or exits,
the watchdog requests termination. If the watchdog is not ready before
admission, the controller refuses to launch. If watchdog liveness is lost
after admission, the primary immediately fails and terminates the workload.
If both trusted processes fail, the OS closes their owned handles and the
last-handle-close limit is expected to terminate job members; this behavior
requires qualification.

Normal child inheritance is expected to retain job membership because
breakaway is not enabled; nested-job behavior and effective outer-job
composition must still be tested on the identified host. Record job
membership using the Job Object APIs, not parent PID alone. The exact
independent process-observer technology, event-loss signal, and sampling
protocol remain unresolved. Until one is selected and independently
reviewed, an external process-tree claim cannot be made from the Job Object
PID list alone.

**Q03 outside-job-child recovery remains an explicit blocker.** The normal
profile denies breakaway. If the synthetic Q03 case nevertheless produces
an outside-job suspended child, classify `PROCESS_CONTAINMENT_FAILURE`,
stop the suite, and do not admit any later case. R1's direct recovery
procedure—open the reported child with terminate/synchronize/query rights,
terminate it, wait for its exit, reconcile descendants and record evidence—
is not yet qualified for the proposed restricted identity and observer.
Do not resume an outside child, continue the workload, or claim that
kill-on-close covers a process outside the job. Before Q03 or any later
qualification is executable, independently review and qualify a bounded
outside-child recovery protocol, including how it detects any descendants
and proves cessation. This proposal does not claim to resolve that gate.

### 3.3 Explicit environment and identity boundary

The controller constructs, rather than copies, the environment block. The
only permitted names are `SystemRoot`, `WINDIR`, `SystemDrive`, `PATH`,
`TEMP`, `TMP`, `PYTHONHASHSEED`, `PYTHONDONTWRITEBYTECODE`,
`PYTHONNOUSERSITE`, `PYTHONSAFEPATH`, and
`PYTEST_DISABLE_PLUGIN_AUTOLOAD`. Values for OS paths and the pinned virtual
environment are read from the reviewed host/profile and recorded exactly;
`PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONNOUSERSITE=1`, `PYTHONSAFEPATH=1`, and
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`. `TEMP`/`TMP` name a dedicated
non-evidence path on which the workload identity has no write access.

`PYTHONPATH`, `PYTHONHOME`, user-site paths, `PYTEST_ADDOPTS`,
`PYTEST_PLUGINS`, proxy/network variables, arbitrary `LOCALAPPDATA`, and
unlisted variables are absent. The evidence-directory variable is held by
the controller and is not inherited by the workload. Record the final
environment block and its digest. If Python/pytest or the fixture cannot
operate with this environment and read-only source access, fail admission;
do not widen it silently.

The proposed filesystem boundary is a restricted workload token plus
read-only source access and explicit ACLs denying writes to the checkout,
user profile, temp paths, registry locations, and evidence directory. The
only worker outputs are explicit pipe handles to the controller. Required
token rights, DACLs, registry behavior, pytest cache behavior, Python
bytecode behavior, and compatibility of the Phase 2A test with this profile
must be qualified. If a complete deny-write boundary cannot be demonstrated,
do not claim the artifact ceiling is hard and do not proceed to Q.

## 4. Monitoring, escalation, and failure classifications

### 4.1 CPU and wall observation

- Target a 10-ms QPC-based monitor cadence and record each sample's QPC
  timestamp and query result in bounded summaries. Maximum acceptable
  observed gap is 100 ms; these are sampling/data-quality targets, not
  real-time guarantees.
- Start job CPU accounting at the first successful workload-thread resume.
  Poll `JobObjectBasicAccountingInformation`; retain the raw cumulative
  `TotalUserTime`, `TotalKernelTime`, combined 100-ns units, converted
  seconds, QPC time, maximum query gap, threshold-bracketing samples, final
  totals, and actual cessation time. The raw unit does not promise 100-ns
  measurement resolution.
- As soon as an observed user-plus-kernel total reaches or exceeds
  120 seconds (1,200,000,000 100-ns units), request whole-job termination.
  Do not wait for another monitor interval. Record CPU at request and after
  job cessation; report any overshoot. Any final observed total above 120
  seconds is `CPU_BUDGET_EXCEEDED`, even if termination was requested at the
  first threshold sample. No extra CPU allowance is defined.
- At `T0 + 115 seconds`, if the job is active, the primary requests
  `TerminateJobObject`. At `T0 + 120 seconds`, the watchdog issues a final
  escalation request if activity remains. Neither API return nor deadline
  arrival proves cessation. Any observed job cessation or supervisor
  completion after `T0 + 120 seconds` is `WALL_BUDGET_EXCEEDED`.
- The watchdog checks a QPC heartbeat/deadline independently of the primary.
  A 100-ms missed heartbeat is a termination trigger, not an assurance that
  the request or termination is completed within 100 ms. Record every
  request, return/error, QPC timestamp, active-process count, job-signaled
  observation, individual exits where available, pipe EOF, final resource
  observation, and evidence-finalization result.
- Continue observing termination after the 120-second budget only to
  establish actual cessation or an explicit `TERMINATION_UNCONFIRMED`
  outcome. Any observation after the budget remains a failure, never a
  grace-period success. The exact post-budget wait limit is not owner
  accepted and must be frozen before Q; R1's 15-second candidate is not
  implicitly accepted.
- A monitor query failure, CPU counter regression, missing process
  accounting, or observed gap above 100 ms triggers immediate whole-job
  termination and `RESOURCE_MEASUREMENT_INCONCLUSIVE`; do not infer a pass.

### 4.2 Required deterministic classifications

Record the first failure and every subsequently observed failure. A run can
be scientifically successful only when the workload assertions pass, all
resource observations are complete, the job is empty, and all required
evidence is complete and hash-verified.

| Classification | Required interpretation |
|---|---|
| `CPU_BUDGET_EXCEEDED` | Final observed job user-plus-kernel CPU exceeds 120 seconds; fail and terminate. |
| `WALL_BUDGET_EXCEEDED` | Any observed workload cessation or supervisor completion exceeds `T0 + 120 seconds`; fail. |
| `MEMORY_LIMIT_EXCEEDED` | Accepted observed private-commit measure or configured job-commit control exceeds its ceiling; terminate the job and fail. |
| `ARTIFACT_LIMIT_EXCEEDED` | Next retained write would exceed a per-file allocation or combined 1,048,576-byte ceiling; terminate and mark incomplete. |
| `CONTROLLER_FAILURE` | Primary exits, misses required monitor progress, or fails internally; watchdog terminates and classifies. |
| `PROCESS_CONTAINMENT_FAILURE` | Unexpected outside-job process, breakaway, unreconciled membership, or unauthorized launch. |
| `TERMINATION_UNCONFIRMED` | No independent cessation confirmation by the separately frozen observation deadline. |
| `EVIDENCE_INCOMPLETE` | Mandatory resource, failure, manifest, ledger, output status, or integrity record is absent, partial, or unverifiable. |
| `RESOURCE_MEASUREMENT_INCONCLUSIVE` | Required API/query fails, metric mapping is unresolved, process accounting is incomplete, or cadence is outside its limit. |

No failed or incomplete run may be represented as a scientific pass.

## 5. Hard retained-artifact design and ledger sizing

### 5.1 Controller-owned writer and complete accounting

The worker receives no evidence-directory path or writable file handle. It
sends bounded versioned records over an explicit inherited pipe. A single
trusted controller-side writer validates record ordering/schema and accounts
each byte before retaining it. It creates one same-directory `.part` gzip
stream and atomically renames that file only after successful close/flush;
there is no simultaneous raw JSONL copy or second complete output copy.
Every temporary, partial, intermediate, stdout/stderr, manifest, resource,
failure, and hash file counts toward the 1,048,576-byte retained cap.

| Reserved retained item | Maximum bytes |
|---|---:|
| `results.jsonl.gz` | 786,432 |
| `stdout.txt` | 32,768 |
| `stderr.txt` | 32,768 |
| `manifest.json` | 16,384 |
| `resource.json` | 16,384 |
| `failure.json` | 8,192 |
| `sha256.json` | 8,192 |
| Aggregate slack | 147,456 |
| **Combined maximum** | **1,048,576** |

The reservation is checked before admission. The writer enforces both every
per-file allocation and the combined cap, including `.part` and any cleanup
or export intermediate. Rename must be same-volume and may not duplicate the
file. stdout/stderr readers continue draining after their retention quotas
are reached, retaining no additional bytes. Track emitted (when knowable),
read/captured, discarded, and retained bytes separately. Pipe-capture limits
do not claim to cap every byte emitted.

The restricted worker token and ACLs must make arbitrary fixture writes
outside the controller channel fail. If the test can write to an alternate
path, temp directory, profile, registry location, or inherited handle, the
retained-artifact hard cap is not established. No filesystem quota, VHD,
system policy, AppContainer provisioning, or host change is authorized here.
If restricted-token/ACL enforcement is inadequate, identify and obtain
separate owner approval for the smallest additional filesystem restriction
before implementation or qualification. Never treat the pipe cap alone as
proof that all writes are bounded.

If the next record or artifact would exceed its reservation, do not truncate
mandatory data or report success. Stop probe admission, request whole-job
termination, drain/discard bounded pipe data, write a reserved failure record
if possible, and classify `ARTIFACT_LIMIT_EXCEEDED` and
`EVIDENCE_INCOMPLETE`. Preserve only complete verified records plus an
explicitly invalid partial stream if reserved capacity permits.

### 5.2 Analytical ledger assessment

The Phase 2A contract fixes a versioned JSONL schema and up to 8,196
target-counter probes. The required record fields include fixture/schema
version, counter, probe index, initial-state identity, before/after counter
snapshots, target-counter delta, coupled-counter deltas, preparation deltas,
returned identity or typed exception, expected and observed outcome,
completion status, and scenario state checkpoints. Output-event fixtures
also record post-rearm checkpoints. Records use canonical UTF-8 JSON and LF;
counter keys are ordered deterministically. No schema value widths are
currently proven to yield an exact total byte bound.

R1/R2 planning estimates are 4,098,000 bytes at an explicitly invalid compact
structural floor, 8,093,550 bytes at a likely mixed estimate, and 16,777,216
bytes at a conservative planning envelope. Against the 786,432-byte result
allocation these require approximately 5.21:1, 10.29:1, and 21.33:1 lossless
compression, respectively. None is a proven worst-case input size or
compression ratio. The complete 8,196-record ledger is therefore **not
proven to fit**. The 1-MiB total cap, metadata reserves, stdout/stderr, hash
manifest, and temporary files remain hard constraints.

Before Phase 2A implementation or execution, a separately authorized
synthetic sizing case must use a frozen byte-bounded schema/writer addendum,
exactly 8,196 synthetic record shapes covering every checkpoint form, pinned
Python/zlib versions and gzip settings, and no neuron, identity allocation,
counter probe, dataset, or benchmark datum. It must report every raw and
compressed length, maximum record size, peak simultaneous disk bytes,
schema/input-shape digest, and completeness. Any allocation or combined-cap
overflow is a failure; no field or record may be omitted or truncated. No
sizing run is authorized now.

## 6. Exact future authorization requests

### Authorization I — supervisor implementation only

**This is a proposal for a separate explicit owner decision.** If accepted,
the bounded implementation scope is:

- Exact future code allowlist: `scripts/luna65_phase2a_supervisor.py` only.
  This file does not exist at the baseline. It may contain the primary
  controller and separately launched watchdog modes, but may not accept an
  arbitrary executable, shell command, module, working directory, or
  environment.
- Documentation/schema updates are allowed only when explicitly named in
  the signed authorization allowlist. No implicit expansion of files.
- No `tpcn/` code; no neuron, predictive coding, reward, eligibility,
  topology, or structural-plasticity changes.
- No Phase 2A capacity fixture, Phase 2B network fixture, dataset, training,
  scoring, or benchmark code.
- No supervisor qualification test, synthetic worker, resource probe,
  fixture execution, qualification execution, or runtime smoke test.
- Permitted validation is limited to source review, static type/syntax
  checks, and exact-diff/provenance checks named by the owner. The proposed
  syntax-only command is
  `.\.venv\Scripts\python.exe -m py_compile scripts\luna65_phase2a_supervisor.py`;
  `git diff --check` is also permitted. These checks must not import or launch
  the supervisor or any workload.
- All Phase 2A resource terms remain as in §3. No other Luna, benchmark, or
  autonomous workload receives coverage from this code.

**Proposed implementation handoff:** the new supervisor file plus its exact
source hash, API/flag constants, handle/environment policy, and static
validation record. The resulting implementation must be independently
reviewed before an Authorization Q request can be made.

The controller-owned pipe protocol must later be integrated with the
Phase 2A test module without changing its scientific assertions. That
fixture does not exist at this baseline; authoring or changing it requires a
separate exact owner allowlist and is excluded from Authorization I.

### Authorization Q — synthetic supervisor qualification only

**This is a second, later request. It is not inferred from Authorization I.**
Do not submit it for execution until Authorization I has been separately
accepted and implemented, the exact supervisor revision/hash is known, the
qualification test and worker have been separately reviewed, the process
observer and Q03 recovery gates are closed, and a complete byte-bounded
evidence ledger is independently reviewed. The owner must receive the
concrete hashes and final command before deciding.

| Item | Proposed exact bound |
|---|---|
| Working directory | Git top-level of the reviewed checkout |
| Pytest command | `.\.venv\Scripts\python.exe -m pytest -q -x tests\test_luna65_supervisor_qualification.py` |
| Synthetic worker command | `.\.venv\Scripts\python.exe -I -S tests\fixtures\luna65_supervisor_worker.py --case <one-literal-case>` |
| Case invocations | Exactly Q01–Q12 below, one invocation per case |
| Retries/replacements | Zero |
| Aggregate job CPU ceiling | 30 observed seconds user plus kernel |
| Aggregate wall ceiling | 360 seconds, including setup and evidence finalization; observed overrun fails |
| Job memory ceiling | 268,435,456 bytes aggregate job commit; no per-process/working-set substitute |
| Combined retained artifact ceiling | 1,048,576 bytes for the complete qualification invocation |
| Evidence location | A fresh owner-designated external directory under `%LOCALAPPDATA%\TPCN\evidence\luna65\supervisor-qualification\<run-id>\`; never in Git or the checkout |
| Allowed command surface | One pinned Python/pytest command and one fixed worker with one enumerated case value; no shell, network, E2, Phase 2A fixture, dataset, or benchmark input |

The proposed `<run-id>` is a preassigned UTC timestamp in
`YYYYMMDDTHHMMSSZ` format, a hyphen, and the seven-character reviewed
supervisor-implementation commit ID. The directory is unique and never
reused. The controller captures stdout/stderr itself, produces one manifest,
resource summary, failure record when needed, and final hash manifest; no
workload-owned evidence directory or intermediate is allowed.

Proposed exact case set:

| Case | Literal synthetic scenario | Per-case CPU / wall / memory ceiling | Required result |
|---|---|---|---|
| Q01 | `admission` | 1 s / 10 s / 67,108,864 bytes | Suspended workload cannot execute before job assignment and settings read-back. |
| Q02 | `descendants` | 1 s / 10 s / 67,108,864 bytes | One child and grandchild remain assigned; membership and active counts reconcile. |
| Q03 | `breakaway-recovery` | 1 s / 10 s / 67,108,864 bytes | Breakaway is denied; any unexpected suspended outside child invokes the independently approved, qualified recovery protocol. **Blocked until that protocol and observer are reviewed.** |
| Q04 | `nested-job` | 1 s / 10 s / 67,108,864 bytes | Incompatible outer-job conditions reject admission; no resumed workload with weakened settings. |
| Q05 | `cpu-monitor` | 4 s / 20 s / 67,108,864 bytes | Reduced two-second observed combined-CPU threshold exercises monitor, request, actual totals, and overrun classification; it does not claim zero overshoot. |
| Q06 | `job-memory` | 3 s / 20 s / 268,435,456 bytes | Synthetic aggregate commit attempt exercises the exact job memory limit and private-commit reconciliation; failure blocks qualification. |
| Q07 | `wall-monitor` | 2 s CPU / 135 s wall / 67,108,864 bytes | 120-second synthetic sleeper, early request at 115 seconds, final escalation at 120 seconds, and measured cessation. Any overrun fails. The 15-second post-budget observation candidate requires separate owner approval and is not a success allowance. |
| Q08 | `controller-failure` | 1 s / 20 s / 67,108,864 bytes | Primary loss triggers watchdog termination; separately verify last-handle-close behavior. |
| Q09 | `artifact-exhaustion` | 1 s / 20 s / 67,108,864 bytes | Emit more than quota; exact retained cap holds, streams drain, failure is explicit, no success-shaped ledger. |
| Q10 | `ledger-sizing` | 5 s / 30 s / 67,108,864 bytes | Exactly 8,196 synthetic records with every schema shape; complete lossless ledger and all files fit or fail. No neuron/counter/task data. |
| Q11 | `evidence-integrity` | 2 s / 20 s / 67,108,864 bytes | Complete and forced-incomplete evidence sets have correct lengths/hashes/status and no misleading success. |
| Q12 | `command-allowlist` | 1 s / 10 s / 67,108,864 bytes | Exact profile accepted; altered argv, cwd, environment, and hashes rejected before any Phase 2A process is created. |

The sum of listed per-case CPU ceilings is 23 seconds; the aggregate ceiling
is 30 seconds to include supervisor overhead. Listed wall case ceilings sum
to 315 seconds; the aggregate ceiling is 360 seconds. Every case's retained
output shares the single 1-MiB aggregate allocation. A case exceeding its
own or aggregate allowance fails and stops the sequence. The suite runs each
literal case once with no retries or replacement. Q03 is not runnable until
the explicit gate above is closed; excluding it would not qualify the
specified full supervisor boundary.

The supervisor, worker, test, Python, pytest, OS build, checkout, arguments,
and environment hashes/values must be included in the final owner
authorization. The test/worker paths do not exist at baseline, so their
future hashes cannot be truthfully prefilled in this governance proposal.
That is why Authorization Q is a later exact request, not permission here.

## 7. R1 issue reconciliation

| R1 finding | R1 disposition under this proposal | Remaining qualification status |
|---|---|---|
| 1. CPU accounting and sampling behavior | Select `JobObjectBasicAccountingInformation`, combined raw user/kernel accounting, 10-ms target schedule, and 100-ms maximum acceptable observed gap. | Counter update granularity, delay, query latency, regressions, and actual overshoot are unmeasured; monitor is not hard CPU enforcement. |
| 2. Wall monitoring and termination confirmation | Owner accepted `T0 + 115 s` request against a 120-s monitored budget, plus escalation and actual-exit observations. | No bounded OS termination latency; any observed overrun fails. The post-budget observation limit still needs owner selection. |
| 3. Job-wide private-commit enforcement | Select exact `JOB_OBJECT_LIMIT_JOB_MEMORY`/`JobMemoryLimit=268435456`, matching notification-limit read-back, IOCP delivery records, `PeakJobMemoryUsed`, and live `PrivateUsage` samples. | Job committed virtual memory versus aggregate concurrent private commit is not yet reconciled on target build; hard-limit and notification behavior still require qualification. |
| 4. Retained-artifact enforcement | Single bounded controller-owned writer, reserved 1-MiB file allocations, workload write denial, and explicit failure on cap. | Restricted-token/ACL completeness and alternate-write denial are not demonstrated; no filesystem fallback is authorized. |
| 5. Controller-owned evidence capture | Specify explicit pipe transport and no workload evidence-directory access. | Writer and Phase 2A transport are not implemented; the fixture integration needs its own exact authorization. |
| 6. Complete compressed JSONL ledger fit | Carry forward raw-size estimates and specify synthetic Q10 with exactly 8,196 deterministic shapes. | No complete ledger fit or compression ratio is analytically proven; Q10 is separately gated. |
| 7. Process-tree containment | Specify suspended launch, assignment/read-back before resume, noninheritable job handles, no breakaway flags, and kill-on-last-handle-close. | Descendant/nested-job behavior, handle isolation, and external-tree observation require target-build qualification. |
| 8. Inherited environment restrictions | Define a constructed allowlist, absent injection/proxy variables, exact value recording, and no ambient inheritance. | Runtime compatibility and effective-token/environment behavior are unverified. |
| 9. Q03 outside-job-child recovery | Preserve Q03 as an explicit blocker; stop and fail on any escape, with no unsafe claim that job termination covers an outside child. | Direct recovery, escaped descendants, permissions, and confirmed cessation are not qualified; Q03 blocks full qualification. |
| 10. Process-observer protocol | Specify Job Object PID-list and active-count reconciliation for in-job members. | The required independent observer technology, event-loss signal, and sampling protocol are unresolved; no independent external-tree claim is permitted. |
| 11. Controller failure and job-handle lifetime | Specify an out-of-job watchdog, heartbeat cutoff, restricted duplicated job handle, and `KILL_ON_JOB_CLOSE` fallback. | Watchdog/controller crash cases, last-handle closure, evidence capture, and termination confirmation need synthetic qualification. |

## 8. Independent reviews and disposition

Four independent read-only reviews were completed against the proposal
candidate identified above and the verified baseline:

| Reviewer | Bounded review objective |
|---|---|
| A — Windows Job Object correctness | Verify target-build APIs, flags, CPU accounting, memory semantics, suspended assignment, process containment, and cessation claims. |
| B — Supervisor safety and failure handling | Verify environment/identity restrictions, handle ownership, watchdog/controller failures, termination, Q03, observer and fail-closed behavior. |
| C — Artifact and evidence design | Verify complete 1-MiB accounting, direct-write prevention, controller writer, ledger sizing, and synthetic Q10 boundary. |
| D — Governance/provenance | Verify baseline identities, exact owner wall decision, Phase 2A-only scope, Authorization I/Q separation, and Luna-63C/Luna-64 isolation. |

| Reviewer | Disposition | Findings / remaining gate |
|---|---|---|
| A | PASS | Win32 APIs, information classes, memory-notification semantics, job settings, and containment claims are correctly distinguished. The optional `JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO` message is not relied on for cessation; independent job-state checks remain required. |
| B | PASS | No material safety/failure-handling issue. Q03 recovery, independent observer, restricted-token enforcement, and controller-failure behavior remain explicit qualification gates. |
| C | PASS | No material evidence/artifact issue. Complete 8,196-record fit, exact retained-artifact enforcement, and synthetic Q10 remain unqualified gates. |
| D | PASS | Owner-source hash, baseline, Phase 2A-only scope, Authorization I/Q separation, and Luna-63C/Luna-64 boundaries verified. |

The only integrated dispositions permitted are:

**PASS — PHASE 2A SUPERVISOR IMPLEMENTATION PROPOSAL READY FOR OWNER
AUTHORIZATION**

or

**BLOCKED — SUPERVISOR IMPLEMENTATION PROPOSAL INCOMPLETE**

A PASS means only that the proposal may be submitted to the owner for a
separate Authorization I decision. It does not authorize implementation,
supervisor qualification, the Phase 2A/2B fixtures, or benchmark execution.
Q03 recovery, independent process observation, hard artifact-path
enforcement, memory metric equivalence, complete ledger fit, and the final
post-budget termination-observation limit remain qualification gates and
must not be represented as verified.

## 9. Scope and validation boundary

This work is resource/governance design, not a TPCN computational
architecture change. A01–A15, the architecture contract, and the changelog
remain unchanged; QPC is a supervisor measurement clock only, never a
neural/event timestep. No ACP is proposed. Phase 2A is the only subject.
Phase 2B remains separately gated. Full Spiral remains blocked,
Luna-64 corrective execution remains blocked, and Luna-63C remains frozen.

No supervisor or test code was implemented. No Job Object was created or
queried; no synthetic sizing, Q01–Q12, Phase 2A/2B fixture, dataset,
training, scoring, benchmark, or workload was run. This document records
design and source/API research only.

## References

- [Windows Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information)
- [JOBOBJECT_BASIC_ACCOUNTING_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information)
- [JOBOBJECT_NOTIFICATION_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_notification_limit_information)
- [JOBOBJECT_ASSOCIATE_COMPLETION_PORT](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port)
- [QueryInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject)
- [SetInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-setinformationjobobject)
- [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
- [TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject)
- [Nested Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs)
