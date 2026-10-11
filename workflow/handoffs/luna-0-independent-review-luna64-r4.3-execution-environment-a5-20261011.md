# Luna-0 Integrated Independent Review — Luna-64 A5

**Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A5`

**Integrated verdict:** **BLOCKED — A5 QUALIFICATION INCOMPLETE**

**Scope:** Independent read-only review of the A5 Hyper-V/Linux execution
proposal, resource policy, separate qualification budget and governance
boundaries. No diagnostic command, VM operation, installation, qualification,
corrective test, or scientific workload was run or authorized.

## 1. Reviewed evidence and review procedure

Five independent reviewers examined the initial proposal/evidence draft in
bounded scopes. Their findings were integrated into a revised A5 draft. A
separate delta reviewer then inspected the corrected proposal and evidence
against the specific material findings below and checked the retained
validator's filesystem operations.

| Final A5 artifact | SHA-256 after delta review |
|---|---|
| [A5 proposal](luna-0-luna64-r4.3-corrective-supervisor-amendment-a5-20261011.md) | `5BCDAC72E7EBDEA777E9964F25554834C4460D97075E6871690BD441BA00C6E5` |
| [A5 evidence](luna64-r4.3-execution-environment-a5-evidence-20261011.json) | `3B0CE1F1DD81EDA00C121010FBF5D857E650D9EE9DDD718AAEEDFBE65EDE9A3D` |

The A5 author independently verified the repository's A4 baseline, ancestry,
frozen manifest, ten package hashes, and 32 governing-input identities. The
delta reviewer confirmed that the A2 hash discrepancy and authorization
boundaries remain consistent, but did not independently recompute every
frozen hash. Owner-reported platform diagnostics remain owner-reported; no
reviewer independently queried the host or guest.

## 2. Independent domain findings

### Linux systemd and cgroups

The documented cgroup v2 distinctions in A5 are sound:

- `MemoryMax=512M` maps to a proposed exact `memory.max=536870912` byte limit;
  charged memory is not Windows working set. `memory.peak`, hierarchical and
  local event counters, swap limits, and OOM-group behavior are evidence and
  controls with distinct semantics.
- `cpu.stat usage_usec` is aggregate subtree accounting; `user_usec` and
  `system_usec` are components. `cpu.max`/`CPUQuota` provides bandwidth, not
  a cumulative CPU-seconds kill switch.
- `TasksMax`/`pids.max` counts tasks/threads, and cgroup placement determines
  which processes are included. `KillMode=control-group` and
  `RuntimeMaxSec` do not prove a hard response-time bound.

The review identified scope ambiguity, OOM-test pass/fail ambiguity, and
systemd 259's legacy `CPUAccounting=` behavior. The revised A5 assigns the
512 MiB and 64-task limits to the corrective service leaf, keeps the monitor
outside that leaf, uses the parent slice's `cpu.stat` for guest CPU, treats
the OOM outcome as expected only in its isolated qualification probe, and
requires direct counter inspection rather than `CPUAccounting=`. It also
records that `cpuset` was reported available but not enabled in the reported
root/`system.slice` controller set; effective single-CPU affinity remains
unverified.

**Reviewer disposition:** the blocked CPU/memory/descendant qualification
status is justified. No cgroup enforcement was exercised.

References: [Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html);
[systemd 259 resource control](https://www.freedesktop.org/software/systemd/man/259/systemd.resource-control.html);
[systemd 259 kill behavior](https://www.freedesktop.org/software/systemd/man/259/systemd.kill.html);
[systemd 259 service timeouts](https://www.freedesktop.org/software/systemd/man/259/systemd.service.html).

### Hyper-V containment and bootstrap

The owner's VM/guest inventory is useful but was supplied as a summary without
raw commands, per-observation timestamps, or hashes. It does not establish the
effective elevated token, VMMS response, control channel, integration-service
inventory, host networking/storage containment, or stop completion. A4's
earlier medium-integrity `Get-VM` access denial remains a separate historical
observation.

`Stop-VM -TurnOff` is an emergency host-side power-off request, not a documented
maximum-latency guarantee. QPC measures elapsed time; it does not guarantee
controller scheduling. No independent stop authority when VMMS or the host
controller fails is established. The revised proposal binds all future
operations to the reported GUID and name, discloses that no guest counter
channel was reported, and makes pre-start host/guest identity, networking,
integration services, VHDX and controller checks qualification prerequisites.

One initial reviewer reported a different VM name in a supposed query block.
The final A5 proposal contains no such query block or alternate name; the
delta reviewer directly checked that claim and it is not used as evidence.

**Reviewer disposition:** A5 must remain blocked pending owner-authorized
identity-bound diagnostics and a defensible stop/failure boundary.

References: [Hyper-V architecture](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/architecture);
[Stop-VM](https://learn.microsoft.com/en-us/powershell/module/hyper-v/stop-vm?view=windowsserver2025-ps);
[Hyper-V integration services](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-integration-services);
[QPC guidance](https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps).

### CPU and wall cutoff semantics

Reviewers confirmed that cgroup CPU accounting plus `CPUQuota=100%` does not
enforce the 120 CPU-second lifetime ceiling. The proposed 100 ms polling,
250 ms heartbeat timeout and one-second stop target are unverified targets,
not maxima. A guard band does not solve an unbounded observation or VMMS
response delay. Host controller and guest boot CPU are outside the proposed
guest parent cgroup; their separate reporting is not equivalent to counting
them under the original aggregate ceiling, and requires explicit owner
approval.

The revised proposal now requires the corrective service cgroup to be empty
by `T0+180s`, with any host stop request started by `T0+179s`; it does not
accept a 181-second run. The separate 600-second qualification wall budget
includes its single VM startup and final confirmed Off state. Reviewers note
that a finite qualification observation cannot establish a universal
worst-case OS scheduling or management-path latency.

**Reviewer disposition:** the strict 120-second CPU and 180-second cessation
limits remain unresolved. The A5 blocked verdict is required.

References: [cgroup v2 CPU interface](https://docs.kernel.org/admin-guide/cgroup-v2.html#cpu-interface-files);
[CFS bandwidth control](https://docs.kernel.org/scheduler/sched-bwc.html);
[systemd v259 parser for legacy `CPUAccounting`](https://github.com/systemd/systemd/blob/v259/src/core/load-fragment-gperf.gperf.in);
[QueryPerformanceCounter](https://learn.microsoft.com/en-us/windows/win32/api/profileapi/nf-profileapi-queryperformancecounter);
[Windows scheduling remarks](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-sleep#remarks);
[Hyper-V state-change API](https://learn.microsoft.com/en-us/windows/win32/hyperv_v2/requeststatechange-msvm-computersystem).

### Artifact quota and filesystem containment

The initial draft overstated what ext4 project quota charges and proposed a
pipe-only broker incompatible with the unchanged first test. Review confirmed
the test calls `mkdtemp(os.tmpdir())` and `writeFile()` directly. The revised
proposal now:

- separates logical artifact lengths, project-charged blocks/inodes and
  shared ext4 metadata;
- records the 5,056 ordinary plus 64 failure-reserve 1-KiB quota units;
- does not claim that a quota allowance reserves physical space, and requires
  a preallocated failure record and a separately bounded backing volume;
- identifies that a pipe-only broker cannot preserve direct Node temporary
  writes and leaves a syscall-compatible logical-byte mediator unselected;
- records unverified sparse/link/alternate-path controls, journald and
  sandbox paths, and delays export until VM Off without copying the 5 MiB
  synthetic payload.

The owner report of two ext4 filesystems does not demonstrate project-quota
support/configuration, inode quotas, or the necessary mediator. The artifact
boundary is not qualified.

**Reviewer disposition:** artifact containment remains blocked.

References: [ext4 inode tables](https://docs.kernel.org/filesystems/ext4/inodes.html);
[ext4 journal](https://docs.kernel.org/filesystems/ext4/journal.html);
[kernel quota subsystem](https://docs.kernel.org/filesystems/quota.html);
[Linux quota UAPI](https://github.com/torvalds/linux/blob/master/include/uapi/linux/quota.h);
[systemd 259 execution sandbox](https://www.freedesktop.org/software/systemd/man/259/systemd.exec.html);
[ext4 administration](https://docs.kernel.org/admin-guide/ext4.html).

### Governance, protocol and provenance

The frozen manifest and package/input inventory identities reconcile to the
retained publication attestation. The corrective authorization is exact and
does not approve the changed memory metric. A1-A4 outcomes, the original
pilot's **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT** disposition and
exhausted scientific budget, unused corrective allowance, and Luna-63C
isolation remain unchanged. The three exact corrective test commands remain
the only candidate workload; no one-process replacement or scientific
execution is proposed.

The A2 proposal review/published/checkout hash discrepancy is preserved as
three distinct values. No corrective allowance or scientific budget is
consumed, and no execution approval is inferred.

**Reviewer disposition:** governance boundaries are preserved, subject to
explicit owner approval before qualification or any resource-policy change.

## 3. Delta-review confirmation and remaining blockers

The separate final delta reviewer returned **PASS — DOCUMENTARY CORRECTIONS
ONLY** for the revised wall ceiling, v259 CPU accounting statement, cgroup
scopes, qualification sequence/budget, artifact disclosures and A2/freeze
boundary. This confirms the listed corrections; it does not qualify the
platform or resolve resource enforcement.

Blocking issues:

1. No verified hard aggregate 120 CPU-second cutoff exists.
2. No finite host-controller/VMMS observation and stop-completion bound is
   established for the 180-second cessation requirement.
3. The proposed guest counter/control channel, host authority, effective
   cpuset, systemd unit and descendant containment have not been qualified.
4. The exact 5 MiB artifact/logical-byte boundary is not implemented or
   verified; the direct-write-compatible mediator is unresolved.
5. The Windows working-set-to-Linux-charged-memory replacement, CPU/bootstrap
   scope, qualification budget, and any infrastructure/controller changes
   require explicit owner approval.

**Integrated verdict: BLOCKED — A5 QUALIFICATION INCOMPLETE.** A5 is not ready
to authorize qualification. This is not a finding that Hyper-V cannot isolate
a guest; it is a finding that this particular resource boundary and its
termination behavior are not demonstrated or fully specified.

## 4. Authorization and validation status

| Item | Status |
|---|---|
| A5 proposal/evidence review | **Completed**, read-only, with the initial domain reviews and final delta confirmation described above. |
| Host/guest diagnostics | **Not independently rerun**; the supplied summary lacks raw captures and hashes. |
| Qualification cases | **Not run**; budget proposed, not approved or executable. |
| Corrective tests/supervisor | **Not run**; original corrective allowance remains unused. |
| Scientific rerun | **Not authorized**; original scientific budget remains exhausted. |
| Luna-63C | **Unchanged and isolated**; no artifact reuse. |
| Memory-policy amendment | **Proposed, not approved**; cgroup charged memory is not working set. |

Next bounded assignment: resolve the CPU-seconds and strict wall-stop
mechanisms, define whether host/guest bootstrap CPU is included, and produce a
compatible hard artifact boundary. Then obtain explicit owner approval for
the changed memory policy, exact qualification budget and any infrastructure
changes before a new independent readiness review. No qualification or
corrective execution follows automatically.
