# Luna-0 — Luna-64 A5 Verified Hyper-V Isolation Qualification Gate

**Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A5`
**Status:** **BLOCKED — A5 QUALIFICATION INCOMPLETE**
**Scope:** Governance-only execution-boundary and separate qualification proposal.
No supervisor, guest command, qualification case, corrective test, or scientific workload was executed or authorized.

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-64 A5 Hyper-V isolation qualification gate"
  task_id: "L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A5"
  component: "Experimental execution resource governance"
  status: "blocked"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "f86c25844a4863ac57cd6634f364c28bcf2f511f"
  result_revision: "Recorded in post-publication workflow closure"
  dependencies: ["frozen R4.3", "original corrective authorization", "A1-A4 blocked amendments", "owner-supplied Hyper-V/Ubuntu diagnostics"]
  owner: "Repository owner"
  classification: ["GOVERNANCE ONLY", "NO QUALIFICATION AUTHORIZATION", "NO CORRECTIVE EXECUTION AUTHORIZATION"]
  hypothesis: "The reported Hyper-V Ubuntu guest can host a root-managed, systemd/cgroup-bounded corrective verifier if a complete CPU cutoff and fail-closed host stop boundary are demonstrated."
  counter_hypothesis: "No available CPU-seconds mechanism provides the exact 120-second aggregate ceiling with a bounded fail-closed termination delay."
  interfaces_relied_on: ["Hyper-V VM control", "Ubuntu systemd 259", "cgroup v2", "read-only source import and bounded evidence export", "frozen corrective test commands"]
  label_information_boundary: ["No scientific input, label, reward, model state, benchmark, or evaluation data is in the qualification service."]
  timing_assumptions: ["Host QPC is the candidate wall clock; guest monotonic time is corroborating evidence only; neither host stop completion nor guest scheduling is assumed hard real-time."]
  reset_boundaries: ["A5 qualification marker is separate from and cannot reset the parent corrective marker."]
  resource_bounds: ["Parent corrective allowance remains unused; separate A5 qualification budget is proposed but unapproved."]
  authorized_scope: ["Read-only repository and provenance review", "Governance proposal and independent review", "Workflow publication"]
  unauthorized_scope: ["Infrastructure changes", "Supervisor/qualification implementation or execution", "Corrective tests", "Scientific workload", "Luna-63C changes"]
  controls: ["Frozen byte and ancestry checks", "Owner-reported evidence remains explicitly attributed", "Separate exact qualification budget", "Independent domain reviews"]
  measurements: ["Git ancestry", "manifest/package/inventory identities", "owner-reported host/guest diagnostics", "documented cgroup and systemd semantics"]
  information_boundary_check: ["No labels, task data, scientific payloads, or Luna-63C artifacts used."]
  hardware_mapping: ["Execution isolation only; no hardware-equivalence claim."]
  architecture_invariants_touched: ["A01-A15 preserved; no computational architecture change."]
  preserves: ["R4.3 freeze", "original pilot NOT SUPPORTED verdict", "A1-A4 blocked outcomes", "A2 byte-provenance discrepancy", "unused corrective allowance", "Luna-63C isolation"]
  architecture_change: false
  proposal: null
  files_changed: ["A5 proposal", "A5 evidence", "A5 independent review", "LUNA_WORKFLOW.md"]
  tests_added: []
  tests_passing: ["Frozen protocol manifest, ten package bytes, and 32 governing-input identities rechecked against the frozen Git objects."]
  tests_failed: []
  tests_not_run: ["All ten A5 qualification cases", "All corrective tests", "All scientific workloads", "Host/guest diagnostics"]
  assumptions: ["Owner-provided platform diagnostics are accurate but are not independently re-executed evidence."]
  unresolved: ["Lifetime CPU-seconds enforcement", "bounded termination latency", "host/guest startup and termination qualification", "artifact filesystem quota and complete write mediation", "explicit owner approvals"]
  recommended_next_agent: ["Luna-0: obtain a separately reviewed enforceable CPU cutoff design or request an explicit resource-policy amendment before proposing a successor gate."]
```

## 1. Frozen authority and predecessor reconciliation

The repository is on `governance/luna64-r4.3-freeze-20261010` at A4 closure
`f86c25844a4863ac57cd6634f364c28bcf2f511f`, which is descended from A4 package
commit `7bd440565c38dee81ace3606fde3fb686de6a0ef` and A3 publication
`8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0`. The frozen content commit
`64a214e310de3b982b90a8ad215598bc1e9f8b1c` is an ancestor of the A4 closure.

| Record | Identity / disposition retained |
|---|---|
| R4.3 content freeze / closure | `64a214e310de3b982b90a8ad215598bc1e9f8b1c` / `ea1b10456cbf4ca726e473076d239a4f6e53b9c7` |
| R4.3 manifest | SHA-256 `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B` |
| Frozen package / inputs | Ten package bytes rehashed from the checkout; all 32 input inventory hashes matched the frozen objects directly or by the recorded LF-to-CRLF materialization (9 direct, 23 materialized). |
| Corrective gate / owner authorization | Gate SHA-256 `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369`; authorization commit `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`. |
| A1 | `d20aab249e42575ccc571c9c72153a3bb4b412db` — **BLOCKED — RESOURCE SUPERVISION UNRESOLVED**. |
| A2 | `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c` — **BLOCKED**. Preserve the recorded proposal-hash discrepancy: review `E00B75004D3085EFDA60D7163D57153F2FCB2D089162574358794BBA54145591`, published Git blob `9FAF922016726FBB5B1EAEBBC8B9488A293E99FC830738E02F3A9A9CD7D958AD`, and CRLF checkout `05C401518A74B1957697E6F12C8877E4D9F8F734A4A7B1432CDF3C9520AE835A`. It is not repaired or elevated to approval. |
| A3 | `8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0` — **BLOCKED — NO QUALIFIED EXECUTION ARCHITECTURE**. |
| A4 package / closure | `7bd440565c38dee81ace3606fde3fb686de6a0ef` / `f86c25844a4863ac57cd6634f364c28bcf2f511f` — **BLOCKED — ISOLATION QUALIFICATION UNRESOLVED**. |
| Original pilot | Closure `515dde66f37ca67c44a39f02e13f2e59b2f10d1d`; **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not an efficacy result. Its 5,184-episode / 20,736-reception budget is exhausted. |

The original corrective authorization remains limited to its exact corrective
scope. Its unused allowance is one invocation, three exact tests, zero retries,
512 combined synthetic stimulus/trace records, one CPU, 120 CPU seconds,
180 wall seconds, 512 MiB aggregate peak Windows working set, and 5 MiB
artifacts. A5 neither consumes nor replenishes it. The A2 published-versus-
reviewed byte discrepancy remains exactly as recorded by A3/A4; no predecessor
verdict is retroactively changed. Luna-63C source, design, authorization,
certificate boundaries and artifacts are outside this gate and unchanged.

## 2. Evidence provenance and platform reconciliation

**OBSERVED (repository):** the A4 package and closure identities, branch
ancestry, freeze manifest SHA-256, ten frozen package bytes, and 32 input
inventory identities were checked in this session. The inventory matches
comprise nine direct raw Git-byte matches and 23 exact LF-to-CRLF materialized
matches, consistent with the retained publication attestation.

**OWNER-REPORTED (not independently rerun):** the diagnostics supplied in the
2026-10-11 task message report:

- Windows 10 Pro build 19045; AMD Ryzen 7 7700X; elevated administrator token.
- Hyper-V running; VM `TPCN-Isolated-Training`, ID
  `60e9baef-706e-4490-80d7-38618710546e`, generation 2, configuration 9.0.
- Four virtual processors, fixed 8 GiB guest memory, disconnected guest
  networking, Guest Service Interface disabled, host shutdown integration
  enabled, checkpoints disabled, and two dynamically expanding VHDX disks.
- Ubuntu 26.04.1 LTS; systemd 259; unified cgroup v2; controllers
  `cpuset cpu io memory hugetlb pids rdma misc dmem`; `cpu memory pids`
  enabled at root and `system.slice`; `MemoryAccounting=yes` and
  `TasksAccounting=yes` on `system.slice`.
- Effective guest CPUs 0–3; about 7.2 GiB usable guest memory; four guest
  logical processors; two mounted ext4 filesystems; no active guest network
  route.

No raw command transcripts, output files, timestamps per observation, or
diagnostic hashes accompanied the summary. These facts improve the A4
inventory but are not independently verified host/guest checks and do not
demonstrate runtime enforcement. No VM, guest or filesystem diagnostic was
run in this A5 task.

A4 recorded `Get-VM` access denied under a medium-integrity token. The new
elevated-token statement may describe a later context, but without raw output
and a repeatable identity-bound query it does not independently establish VM
management rights. The reported controller list includes `cpuset`, but the
enabled root and `system.slice` controller lists omit it. Therefore effective
single-CPU affinity is not established; a qualification must verify
`cpuset.cpus.effective` and its ancestors and obtain approval before enabling
or changing controllers.

## 3. Proposed execution boundary

This is the candidate to be assessed in a separately authorized qualification,
not a selected or qualified execution architecture.

1. **Host TCB:** an elevated, root-owned-equivalent Windows controller, VMMS,
   Hyper-V, host QPC, host one-shot ledger and protected export directory.
   Every operation must bind to VM GUID
   `60e9baef-706e-4490-80d7-38618710546e` and confirm the reported name
   `TPCN-Isolated-Training`; mismatch or ambiguous identity blocks start and
   stop. The host controller's CPU is measured separately; excluding it from
   the parent's 120-second ceiling is a resource-policy change requiring
   explicit owner approval.
2. **Guest TCB:** trusted Hyper-V virtual hardware, Ubuntu kernel, systemd
   PID 1, a pre-provisioned locked systemd service and a separate root-owned
   admission/accounting monitor. The corrective service leaf contains the
   supervisor and every test descendant; its `MemoryMax=512M`,
   `MemorySwapMax=0`, `MemoryOOMGroup=yes`, `TasksMax=64`, one-CPU affinity
   and rate limit apply to that tree. The separate monitor is outside that
   leaf, so its memory is not charged to the parent replacement metric. A
   dedicated non-delegated parent slice contains both monitor and workload;
   its `cpu.stat` is the proposed aggregate guest CPU source. The unprivileged
   service cannot write cgroup control files, change unit properties, move
   itself, set `Delegate=`, use privileged capabilities, or access a writable
   cgroup hierarchy. The monitor's CPU is included in the guest CPU total;
   whether that scope is accepted is an owner decision.
3. **Bootstrap:** the guest is booted and preflighted before the corrective
   invocation clock starts. The service and all resource properties are
   provisioned and query-checked before any corrective command. The host
   controller creates the one-shot admission record immediately before
   triggering the already-booted guest service. The monitor and corrective
   service start under the dedicated slice; guest OS boot and host controller
   CPU are outside `cpu.stat`, recorded separately, and require an explicit
   scope decision rather than being silently treated as part of the 120-second
   limit. Service startup failure, policy mismatch, unrecognized revision,
   absent monitor, or unavailable evidence channel means no workload start.
   No control channel is established by the supplied diagnostics. A dedicated
   host-ACL-protected virtual serial/named-pipe channel is one candidate, not
   an observed or approved facility; it would need its own bootstrap/security
   review and owner approval. Hyper-V heartbeat alone is not cgroup telemetry.
4. **Allowed workload:** exactly the three frozen corrective child commands,
   serially and once, from the authorized corrective worktree revision:
   `node experiments/luna64/test-track-b-gate-r4.mjs`,
   `node experiments/luna64/test-luna64-r4.3-reward-reference.mjs`, and
   `node experiments/luna64/test-luna64-r4.3-reward-lifecycle.mjs`.
   The first test's 23 required sequential validator CLI descendants remain
   allowed and must stay in the service cgroup. No single-process rewrite,
   benchmark runner, generator, network/GPU tool, training, scoring, or
   scientific replay is permitted.
5. **Process boundary:** proposed `KillMode=control-group`, a verified
   dedicated unit cgroup and ancestors, `TasksMax=64` on the corrective
   service leaf (tasks/threads, including its supervisor and all descendants),
   no breakaway/delegation, and pre/post PID-tree accounting. The monitor is
   outside that leaf. All test descendants must be in the leaf before dispatch
   and absent before acceptance.
6. **Emergency control:** a separately administered host controller monitors
   authenticated guest-unit status and the host monotonic deadline. If guest
   monitoring fails or the guest stops responding, it requests
   `Stop-VM -TurnOff`, does not wait for guest shutdown, and holds evidence
   export until the VM is confirmed Off. The supplied diagnostics identify no
   counter/status channel and establish no completion-latency guarantee for
   this Hyper-V management path. If the host controller or VMMS fails, no
   independent termination authority is established. This is an unresolved
   blocker, not permission to retry, kill arbitrary host processes, or claim
   fail-closed resource cessation. A failed/late stop is a boundary breach;
   withholding evidence is only fail-closed acceptance, not proof of cessation.

## 4. Resource policy proposal and exact semantics

### Memory — proposed owner-approved metric amendment

Replace only the parent's Windows aggregate peak working-set metric with
**512 MiB = 536,870,912 bytes of Linux cgroup-accounted memory**, configured
as `MemoryMax=512M`; qualification must query the effective
`memory.max` and require exactly `536870912`.

- `memory.max` is the hard cgroup memory charge boundary, hierarchically
  accounting tasks in the cgroup and descendants, with reclaim and possible
  cgroup OOM behavior. It is not a working-set or total-RAM metric.
- Require effective `memory.max=536870912` and `memory.swap.max=0`.
  cgroup v2 exposes swap limit files through the memory controller; swap is
  not a separate cgroup controller. If `memory.swap.max` is unavailable, a
  separately verified guest-wide no-swap configuration is required; a missing
  file alone is not a pass.
- Capture `memory.peak`, `memory.events` and `memory.events.local`, including
  `max`, `oom`, and `oom_kill`, plus `memory.stat` before cleanup. A limit
  event/OOM is an expected injected outcome only in qualification case 3;
  it is a failed corrective run. Qualification must distinguish ordinary
  reclaim/allocation failure from an actual OOM event. `MemoryOOMGroup=yes` /
  effective `memory.oom.group=1` requests group treatment for a kernel OOM
  kill; it does not guarantee every limit crossing will cause an OOM kill.
  The monitor remains outside the killed service leaf and must record the
  failure.
- Charged memory may include anonymous and file cache and kernel-accounted
  categories, depending on kernel configuration. It is not equivalent to
  Windows process-tree aggregate working set or guest physical allocation.
- Apply the 512 MiB cap and peak/event capture to the corrective service leaf
  containing the supervisor and all test descendants, not to a sibling
  monitor. Apply the qualification's 768 MiB ceiling to its separate outer
  qualification cgroup and identify that counter scope independently.

This is a material resource-policy replacement. It is **not owner-approved**.
Until the owner explicitly approves this exact metric and scope, the original
working-set requirement remains in force and execution stays blocked.

### CPU — accounting available; lifetime cutoff unresolved

Read the dedicated parent slice's `cpu.stat` (`usage_usec`, `user_usec`,
`system_usec`) before, during and after the single invocation. `usage_usec`
is the aggregate total; user and system fields are components for
reconciliation and must not be added to the total. Do not rely on
`CPUAccounting=yes` on systemd 259; the directive is a disabled legacy
compatibility setting there. Verify the actual cgroup counters directly.
The guest parent slice includes the monitor, supervisor, all three tests and
every descendant after service admission; guest OS boot and host-controller
CPU are excluded and separately recorded, requiring explicit owner approval
of that accounting boundary.

`AllowedCPUs`/`cpuset.cpus` plus `CPUQuota=100%`/`cpu.max` can confine the
workload to one guest CPU and impose a rate limit. They do **not** impose a
120 CPU-second lifetime limit. `cpu.stat` is accounting, not enforcement;
systemd has no proposed native aggregate CPU-seconds kill control here.

A host watchdog that polls reported `cpu.stat` and powers off the VM is only
the candidate response path. A tentative qualification target of no more than
100 ms observation interval, 250 ms lost-heartbeat detection, and one second
from deadline to confirmed VM Off is a test criterion, not a verified bound.
The owner-supplied diagnostics establish neither those maxima nor what occurs
if the controller is descheduled, the communication channel fails, VMMS is
unresponsive, or turn-off is delayed. A threshold guard band alone cannot
prove the 120-second ceiling if the delay is unbounded. Therefore the exact
120 CPU-second aggregate ceiling is **not enforceable on present evidence**.
No CPU cutoff architecture is selected; a hard mechanism or separately
approved resource-policy amendment is required before any qualification run.

### Wall time — monotonic deadline proposed; completion bound unresolved

Use the host controller's monotonic QPC as the authoritative clock, starting
at the one-shot admission point immediately before the already-booted guest
service is triggered. Guest `CLOCK_MONOTONIC` and service elapsed time are
corroborating only. Preserve the hard 180-second cessation deadline: request
service stop early enough that the whole service cgroup is confirmed empty no
later than `T0+180s`; the provisional one-second maximum response target means
the host stop request must begin by `T0+179s`. No 181-second grace is allowed.
A graceful shutdown, `RuntimeMaxSec=180s`, a stop request, or a successful
PowerShell return is not itself proof that all descendants ceased by the
deadline. Host QPC/VMMS scheduling and stop completion are not shown to have
a finite worst-case delay. Failure to confirm empty/Off by `T0+180s` is a
hard boundary breach; evidence rejection alone is not cessation. Until a
defensible bound and failure escalation are demonstrated, the 180-second
hard cutoff is unresolved.

### Artifacts and storage — hard quota candidate, not yet verified

Preserve a total 5 MiB boundary (`5,242,880` bytes) across stdout, stderr,
JSONL, fixtures, temp files, failure records and export staging. Candidate
design:

- A dedicated evidence filesystem with ext4 project quota, fixed inode cap,
  and aggregate hard charged-block quota no larger than 5,242,880 bytes.
  Reserve 65,536 bytes under a separate root-only failure-evidence project;
  ordinary output is limited to 5,177,344 bytes (5,056 generic quota
  1-KiB units plus 64 units for the reserve). Project quotas limit project-
  charged space and inodes, not all shared ext4 metadata such as inode tables,
  allocation maps, superblocks, journals or the backing VHDX. A separate
  fixed-capacity evidence volume must bound filesystem overhead; that volume
  capacity is not an increase to the 5 MiB artifact allowance.
- Project-ID inheritance, existing inode ownership, both space and inode
  hard limits, and rejection of cross-project rename/hardlink/reassignment
  must be preconfigured and checked. Sparse extents, open-unlinked files,
  replacement temporaries and alternate writers must be included. Project
  quotas bound charged blocks, not aggregate logical file lengths.
- A separate preallocated, root-only failure-record file is required; a
  project quota allowance alone does not reserve physical blocks, inodes,
  journal capacity or successful durable writes. Preflight must verify the
  reserved allocation and a bounded fixed-capacity backing volume. Shared
  ext4 metadata and the VM's dynamic VHDX growth are separate storage budgets,
  not included in the 5 MiB artifact quota; their maxima and host-volume
  headroom must be pinned before qualification.
- The first frozen corrective test directly uses Node `mkdtemp(os.tmpdir())`
  and `writeFile()` for CLI fixtures. A pipe-only output broker with no
  writable temporary filesystem is not compatible with those direct POSIX
  writes. A syscall-compatible mediated filesystem (for example, a bounded
  userspace filesystem) could preserve those calls while enforcing aggregate
  logical length, but is not selected, implemented or verified. The two new
  corrective test files' write behavior is also not qualified here.
- `ProtectSystem=strict`, read-only source, `NoNewPrivileges`, private
  mount/network namespaces, no capabilities and a read-only repository are
  candidate controls only. The exact sandbox must deny writable repository,
  home, `/tmp`, `/var/tmp`, host mounts, archive disk and arbitrary paths
  while preserving the unchanged test's temporary-file semantics. It must
  also inventory API filesystems, `/dev/shm`, managed state/cache/log/runtime
  paths, inherited writable file descriptors and mount propagation.
  `PrivateTmp=yes` is not a write-denial control for `/tmp` or `/var/tmp`.
  A post-run `du`/manifest is not enforcement.
- Import source only from a hash-verified read-only ISO. Export evidence only
  after the VM is Off, through a separately bounded staging location with
  hash verification. The 5 MiB synthetic artifact payload is not copied to
  host staging; only a bounded manifest, counters, logs and failure evidence
  (at most 1 MiB under the qualification budget) are exported, avoiding an
  uncounted duplicate. Seal and flush the source volume before shutdown; if a
  forced stop leaves evidence incomplete, report failure rather than
  recovering or modifying it implicitly. Do not attach the 256 GB archive as
  a writable workload path or use it as a substitute for 5 MiB.

Owner diagnostics establish two ext4 mounts but not project-quota support or
activation, inode quota, a bounded evidence volume, a compatible logical-byte
mediator, mount restrictions, sparse-write rejection, or complete mediation.
Artifact containment is unresolved and blocks qualification.

## 5. Separate proposed A5 qualification budget

This is a new, non-additive governance proposal. It does not consume the
exhausted scientific allowance or the unused corrective one-shot allowance.
It is **not authorized or executable**. Qualification may start only after
independent prereview, explicit owner approval of this complete budget and
memory policy, and resolution of the CPU/wall termination blockers.

| Item | Exact proposed ceiling |
|---|---|
| Invocation | One host-led qualification invocation; one VM start and one VM stop; one durable host one-shot marker; zero retries or reruns. |
| Cases | At most ten cases below, sequentially once each in the fixed order; abort on the first failure, with no retries or extra probes. |
| Compute | One guest CPU for test workloads; maximum 180 aggregate guest cgroup CPU seconds for the entire qualification. Host controller CPU is logged separately; this exclusion requires explicit owner approval. |
| Wall | 600 seconds from host-QPC admission immediately before the one qualification VM start through confirmed VM Off; includes boot and any failed startup, with no pause/reset or extension. The synthetic corrective wall-cutoff case must still cease by its own `T0+180s` deadline. |
| Memory | One outer qualification cgroup with `memory.max=805306368` (768 MiB), swap disabled, plus an inner 512 MiB memory-policy test. These are proposed charged-memory caps, not Windows working-set values. |
| Artifacts | At most 6 MiB total: one 5 MiB hard-quota test volume plus no more than 1 MiB total retained host/guest qualification evidence. No unbounded journald or host console capture. |
| Other bounds | At most 80 tasks/threads in the outer qualification boundary and `TasksMax=64` per workload leaf; no network; no GPU; no model/scientific records; no corrective sources writable; at most 10 synthetic resource-probe cases. |
| Paths | Guest: preconfigured read-only source ISO and `/var/lib/tpcn/a5-qualification/<one-shot-id>/` quota test volume only. Host: protected `C:\ProgramData\TPCN\L64-A5\<one-shot-id>\` marker/evidence directory. No repository checkout, home, archive VHDX or shared writable host path. |

Exact permitted case order is 1, 2, 3, 4, 5, 6, 9, 10, 7, 8. The guest VM is
started once and remains powered through the cases. The qualification outer
boundary caps the entire probe/monitor tree at 80 tasks; each workload leaf
has `TasksMax=64`. Cases 7 and 8 are the
paired final monitor-failure/host-termination event: it is one forced VM stop,
with two separately recorded acceptance criteria. If any earlier case
requires a VM turn-off, abort the invocation; do not restart or retry.

1. **Pre-start policy:** verify the VM GUID/name, host token, vNIC/switch,
   every enabled integration service, attached media, VHDX identity/storage
   bounds, and offline state; verify service is pre-provisioned, inactive,
   locked, revision-pinned, and all effective ancestor/leaf cgroup properties
   including `cpuset.cpus.effective` match before admission. Mismatch must
   prevent start. Any controller enablement or VM reconfiguration is separately
   approved before qualification.
2. **Descendant containment:** launch a controlled benign multi-generation
   process tree; verify every PID/task remains in the approved cgroup with
   inherited limits and is absent after stop.
3. **Memory hard limit:** query exactly `536870912` bytes, swap zero, drive a
   bounded synthetic allocator across the limit, and verify the expected
   counter/OOM behavior and descendant termination. The case passes only for
   its declared injected failure and complete retained evidence; an OOM during
   a corrective test would fail that run.
4. **CPU cutoff:** run a CPU-bound synthetic probe against the exact 120 CPU
   second policy and verify no more than 120 aggregate `usage_usec` seconds
   for all in-scope guest processes before confirmed stop. This case cannot
   pass on CPUQuota or accounting alone.
5. **Wall cutoff:** run a bounded synthetic sleeper and verify its full
   service cgroup is empty by `T0+180s`; begin any host stop request by
   `T0+179s`. There is no one-second extension beyond the frozen 180-second
   ceiling. Record request, state-transition, and confirmed-empty timestamps
   separately.
6. **Artifact quota:** attempt over-limit writes, sparse extension, alternate
   temp/stdout paths, inode exhaustion and failure-reserve writes; verify the
   hard 5 MiB boundary and retained evidence.
9. **One-shot behavior:** consume a test-only host marker, replay the same
   admission identity, and verify the second start is denied; interruption
   consumes the marker.
10. **Evidence integrity:** before shutdown, verify source ISO hash,
    unit/cgroup configuration identity, timestamps, raw counter snapshots,
    artifacts and the pending export manifest; reject incomplete or modified
    evidence. Final export and hash verification occur only after case 8
    confirms the VM is Off.
7. **Monitor/supervisor failure:** last live-workload probe, terminate or
   disconnect the guest monitor during a synthetic child; the independent
   host controller must initiate the one final forced VM turn-off.
8. **Host termination authority:** paired acceptance criterion for case 7;
   under the effective elevated token, record the host turn-off operation,
   state transition and confirmed Off time against the pinned VM GUID. No
   second VM start or retry is allowed; unavailable authority, late transition
   or VMMS failure is a failed gate. Only after confirmed Off, export through
   the bounded host staging path and verify the final evidence hashes. The
   exported manifest must report any unflushed/incomplete guest artifacts;
   no journal replay or filesystem repair is allowed in this gate.

No test case may execute the three corrective tests or any scientific code.
The qualification budget's current gate is **blocked** because cases 4 and 5
lack an enforceable, bounded stop mechanism. The budget must not be used as an
implicit request to execute those probes.

## 6. Independent review, authorization and disposition

Five independent read-only reviews are recorded in the paired review handoff:
(1) Linux systemd/cgroup enforcement, (2) Hyper-V containment
and bootstrap, (3) CPU/wall cutoff semantics, (4) artifact quota/filesystem
containment, and (5) frozen protocol/governance boundaries. Each reviewer
must separate owner-reported facts, documented OS semantics, analytical
proposals and untested runtime claims.

Before even qualification can be authorized, the owner must separately
approve: (a) replacing the Windows working-set metric with Linux cgroup-charged
memory exactly as specified; (b) the independent qualification budget and any
infrastructure change/control-channel exception; and (c) any disclosed
bootstrap/controller CPU scope exclusion or resource-bound change. Approval
of A5 cannot authorize corrective tests. Corrective execution still requires
a qualified architecture, its own explicit owner approval, and the original
unused marker/allowance under the parent gate.

**Integrated verdict: BLOCKED — A5 QUALIFICATION INCOMPLETE.**

The new diagnostics answer inventory questions but do not prove limit
enforcement. Most importantly, no hard aggregate lifetime CPU-seconds
termination primitive or bounded host response is established, and wall-time
completion is likewise not bounded. Artifact project quota and a
syscall-compatible logical-byte boundary remain unverified. A5 is not ready
to authorize qualification.
The original pilot remains **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**;
scientific rerun and corrective execution remain unauthorized; A1-A4 verdicts
and Luna-63C isolation remain unchanged.

## 7. Validation and next bounded assignment

| Procedure | Result |
|---|---|
| Git ancestry and A4 closure/package identities | **PASS**, read-only; A4 closure `f86c25844a4863ac57cd6634f364c28bcf2f511f`. |
| R4.3 manifest raw SHA-256 and ten frozen package raw hashes | **PASS**, checked against published identities. |
| 32 governing-input hashes | **PASS**, 9 direct Git-byte matches and 23 exact LF-to-CRLF materializations. |
| Owner-supplied host/guest diagnostics | **Received, not independently rerun**; provenance limitations recorded above. |
| Hyper-V/cgroup runtime qualification, resource cutoff, quota, corrective tests, scientific workload | **NOT RUN**; expressly unauthorized. |

Next assignment: Luna-0 to obtain an independently reviewed, technically
enforceable CPU-seconds cutoff and bounded VM-stop architecture, or ask the
owner for an explicit resource-policy change. Only then prepare a successor
qualification gate; no corrective or scientific execution is ready.
