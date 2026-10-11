# Luna-0 - Luna-64 R4.3 A4 Hyper-V / Linux Isolation Qualification Gate

```yaml
tpcn_handoff:
  agent: "Luna-0"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-64 A4 Hyper-V and Linux isolation decision"
  task_id: "L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A4"
  component: "Experimental execution resource governance"
  status: "blocked"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0"
  result_revision: "Containing publication commit reported in the subsequent workflow closure; not self-embedded"
  dependencies: ["frozen R4.3", "owner-authorized corrective gate", "A1-A3 blocked findings", "owner-reported Hyper-V Ubuntu availability"]
  owner: "Repository owner"
  classification: ["GOVERNANCE ONLY", "NO EXECUTION AUTHORIZATION"]
  hypothesis: "A preconfigured systemd service cgroup in a verified isolated Hyper-V guest may provide a reviewable containment candidate for the unchanged corrective tests."
  counter_hypothesis: "Guest configuration, original memory metric, watchdog bounds, bootstrap, or artifact policy cannot be verified and the environment remains unqualified."
  interfaces_relied_on: ["Hyper-V host boundary", "Ubuntu systemd service and cgroup v2", "frozen R4.3 corrective test commands", "resource authorization records"]
  label_information_boundary: ["No training labels, model inputs, evaluation truth, scientific replay, or task data used"]
  timing_assumptions: ["Host time is not neural time", "No bounded watchdog lateness is assumed"]
  reset_boundaries: ["No marker reset; parent and A2 qualification markers remain absent at last recorded check"]
  resource_bounds: ["Original corrective budget unchanged and unused", "Separate qualification proposal unapproved"]
  authorized_scope: ["Governance review", "Read-only host metadata", "Public OS documentation", "Prepare read-only guest diagnostics"]
  unauthorized_scope: ["Guest command execution", "VM start/stop/configuration", "Installation or feature enablement", "Supervisor qualification", "Corrective tests", "Scientific workload"]
  controls: ["Independent reviews", "Exact Git and checkout identities", "Explicit host/guest evidence status", "A2 discrepancy preserved"]
  measurements: ["Host OS/CPU/RAM/hypervisor metadata", "Git ancestry", "file identities", "proposed cgroup and resource semantics"]
  information_boundary_check: ["No task labels or future inputs introduced"]
  hardware_mapping: ["Execution isolation only; no hardware equivalence claim"]
  architecture_invariants_touched: ["A01-A03", "A07-A11", "A15 preserved; no computation change"]
  preserves: ["R4.3 scientific freeze", "A1-A3 blocked findings", "original pilot verdict/budget", "corrective allowance", "Luna-63C isolation"]
  architecture_change: false
  proposal: null
  files_changed: ["A4 governance handoff", "A4 platform evidence", "LUNA_WORKFLOW.md A4 entry"]
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["Guest diagnostics", "All qualification cases", "All corrective tests", "All scientific workloads"]
  assumptions: ["Owner-reported guest settings remain unverified", "Linux charged memory differs from Windows working set"]
  unresolved: ["Guest/platform evidence", "Memory metric approval", "strict CPU and wall termination", "artifact containment", "qualification budget and owner authorization"]
  recommended_next_agent: ["Luna-0: after explicit owner permission, gather read-only guest/host evidence and revise the gate only if technically justified"]
```

**Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A4`

**Scope:** Governance-only reassessment and separate qualification proposal.
No Luna-64 implementation, supervisor, diagnostic guest command, supervisor
qualification, focused test, or scientific workload is run or authorized.

**Disposition submitted for independent review:** **BLOCKED - ISOLATION
QUALIFICATION UNRESOLVED**

**Architecture proposal:** A dedicated, offline Hyper-V Ubuntu guest with
systemd-managed, pre-provisioned **service unit** (not an attach-after-start
scope or a transient-at-invocation unit), unified
cgroup v2 limits, and a separately governed host control plane. The owner-reported
guest is not yet independently inspectable from this token; even if verified,
the parent working-set metric and strict CPU/wall termination guarantees need
separate policy resolution.

## 1. Reconciled authority and preserved outcomes

| Record | Identity / outcome |
|---|---|
| R4.3 content freeze | `64a214e310de3b982b90a8ad215598bc1e9f8b1c` |
| R4.3 governance closure | `ea1b10456cbf4ca726e473076d239a4f6e53b9c7` |
| Frozen manifest SHA-256 | `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B` |
| Corrective gate | `L64-TB-R4.3-CORRECTIVE-20261010`, SHA-256 `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369` |
| Corrective owner authorization | `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`; explicitly approves only its original correction and reject-only malformed second-origin policy |
| A1 publication | `d20aab249e42575ccc571c9c72153a3bb4b412db`; blocked |
| A2 publication | `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c`; blocked |
| A3 publication | `8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0`; **BLOCKED - NO QUALIFIED EXECUTION ARCHITECTURE** |
| Original pilot closure | `515dde66f37ca67c44a39f02e13f2e59b2f10d1d`; **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not an efficacy result |
| Corrective baseline/worktree | branch `experiment/luna64-r4.3-reward-lifecycle-correction-20261010`, clean at `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787` |

Preserve, do not rewrite, A1 and A2. In particular the A2 proposal's recorded
review hash is not its published exact-byte hash. The A3 integrated review
records the CRLF/Git identities and post-review Markdown hard-break change;
reconstruction does not establish an exact-byte A2 approval. A3's blocked
decision remains historically correct for the platform evidence available to
it. New host observations do not retroactively change that finding.

The original scientific budget remains exhausted (5,184 episodes / 20,736
receptions). The corrective allowance remains unused: one supervisor
invocation, three exact focused tests, no retries, 512 combined synthetic
stimulus/trace records, one CPU allocation, 120 CPU seconds, 180 wall seconds,
512 MiB aggregate peak working set, 5 MiB aggregate artifacts. Its one-shot
marker and the separate A2 qualification marker are absent. The latter absence
is retained-state evidence, not proof that no unrecorded external process ever
ran. No scientific rerun is authorized. Luna-63C code, certificate artifacts,
and interpretation remain isolated and unchanged.

The A4 qualification proposal below replaces, and is not additive to or a
reuse of, A3's unapproved provisional qualification proposal. Neither
qualification proposal is authorized or consumed. The corrective allowance
is separate from both and remains unused.

## 2. Platform observations and read-only diagnostics

### Independently observed on the host in this governance session

- Windows 10 Pro x64, build `10.0.19045`.
- `Win32_ComputerSystem`: Gigabyte B650 GAMING X AX V2; physical RAM
  `33,443,172,352` bytes (approximately 31.1 GiB).
- CPU: AMD Ryzen 7 7700X, 8 cores / 16 logical processors; firmware
  virtualization reported enabled.
- `HypervisorPresent=true`; `vmms` and `vmcompute` services are running.
- Hyper-V PowerShell module and read-only query cmdlets are installed.
- `Get-VM` fails with access denied under this medium-integrity token; its
  Administrators group is deny-only. VM configuration, power state, host
  termination authority, and disk/network settings were **not** independently
  read. No VM was started, stopped, or modified.

### Owner-reported only; not verified here

Operational Hyper-V; Ubuntu `26.04.1 LTS`; four guest vCPUs; fixed 8 GiB guest
memory; 128 GB SSD-backed system VHDX; 256 GB secondary archive VHDX; guest
network disconnected. These are useful leads, not A4 platform evidence.

The host VMMS running and hypervisor present establish additional host capability
since A3, not guest boot/configuration, containment, or execution readiness.
No in-guest diagnostic command was run. The VM's lack of networking is not
verified. The inaccessible VM inventory is a current authorization/tool-token
limitation, not evidence that the VM is absent.

### Prepared read-only host queries

Run only from an appropriately authorized host administration session after
explicit owner permission for diagnostics. They do not start/stop or reconfigure
the VM. Replace `$Name` with its exact registered name.

```powershell
$Name = 'Ubuntu-26.04-Luna64'
$vm = Get-VM -Name $Name -ErrorAction Stop
$vm | Select-Object Name, Id, State, Generation, Version, ProcessorCount,
    MemoryStartup, MemoryMinimum, MemoryMaximum, DynamicMemoryEnabled,
    AutomaticStopAction | Format-List
Get-VMProcessor -VMName $Name |
    Select-Object VMName, Count, CompatibilityForMigrationEnabled,
        ExposeVirtualizationExtensions | Format-List
Get-VMMemory -VMName $Name |
    Select-Object VMName, Startup, Minimum, Maximum, DynamicMemoryEnabled |
    Format-List
Get-VMHardDiskDrive -VMName $Name |
    Select-Object VMName, ControllerType, ControllerNumber, ControllerLocation,
        Path | Format-Table -AutoSize
Get-VMNetworkAdapter -VMName $Name |
    Select-Object VMName, Name, IsConnected, SwitchName, MacAddress,
        Status | Format-List
Get-VMIntegrationService -VMName $Name |
    Select-Object Name, Enabled, PrimaryStatusDescription,
        SecondaryStatusDescription | Format-Table -AutoSize
Get-VMHost | Select-Object ComputerName, LogicalProcessorCount,
    MemoryCapacity, VirtualHardDiskPath, VirtualMachinePath | Format-List
whoami /groups
```

For each reported disk, use `Get-VHD -Path <exact-path>` as a read-only query
to record VHD format/type, virtual size, file size and attachment. Do not query
contents by mounting. Network evidence must include the VM NIC connection state
and its switch definition; an Ubuntu interface merely reported down is not proof
of host-side disconnection. A disconnected vNIC/no adapter is preferred. Do
not assume a private/internal switch is offline.

`Get-VM` already failed under the current token. Do not self-elevate, prompt for
credentials, or attempt `Stop-VM` to test authority. Host administrator
permission and stop rights must be separately attested/read-only verified.

### Prepared read-only Ubuntu guest diagnostic bundle

Run only after explicit owner permission, from the VM's local console (no SSH,
network enablement, guest tools installation, or workload launch). This bundle
queries version, unified cgroup, unit defaults, filesystem/quota support,
Hyper-V integration components and current network routes. It writes no files.

```sh
printf '%s\n' '=== identity/kernel ==='
cat /etc/os-release
uname -a
systemd --version
systemd-detect-virt
printf '%s\n' '=== cgroup v2 ==='
stat -fc '%T' /sys/fs/cgroup
findmnt -no SOURCE,FSTYPE,OPTIONS /sys/fs/cgroup
cat /sys/fs/cgroup/cgroup.controllers
cat /sys/fs/cgroup/cgroup.subtree_control
for f in memory.max memory.peak memory.events memory.swap.max \
         cpu.max cpu.stat cpuset.cpus.effective pids.max; do
    if test -r "/sys/fs/cgroup/$f"; then
        printf '%s: ' "$f"; cat "/sys/fs/cgroup/$f"
    else
        printf '%s: unavailable\n' "$f"
    fi
done
printf '%s\n' '=== systemd ==='
systemctl show --property=Version --property=DefaultTimeoutStopUSec \
    --property=InhibitDelayMaxUSec --property=DefaultCPUAccounting \
    --property=DefaultMemoryAccounting
systemctl show systemd-logind.service --property=KillMode \
    --property=TimeoutStopUSec --property=RuntimeMaxUSec
systemctl is-active hv-kvp-daemon.service hv-vss-daemon.service \
    hv-fcopy-daemon.service
printf '%s\n' '=== filesystems/disks ==='
lsblk -e7 -o NAME,SIZE,TYPE,FSTYPE,FSVER,RO,MOUNTPOINTS,UUID
findmnt -no SOURCE,FSTYPE,OPTIONS /
findmnt -no SOURCE,FSTYPE,OPTIONS /tmp
findmnt -no SOURCE,FSTYPE,OPTIONS /var/tmp
df -B1 -T / /tmp /var/tmp
grep -E '^(CONFIG_CGROUPS|CONFIG_MEMCG|CONFIG_CGROUP_PIDS|CONFIG_CGROUP_CPUACCT|CONFIG_CGROUP_SCHED|CONFIG_CGROUP_FREEZER|CONFIG_EXT4_FS|CONFIG_QUOTA)=' \
    "/boot/config-$(uname -r)" 2>/dev/null
printf '%s\n' '=== offline network state ==='
ip -brief link
ip -brief address
ip route show table all
ip -6 route show table all
resolvectl status 2>/dev/null
```

The above does not prove project-quota activation. For a proposed evidence
filesystem, read-only evidence must additionally identify filesystem type,
mount flags, quota capability/activation, current quota state, and project ID/
limit via the applicable filesystem's *report-only* tooling (`repquota`,
`xfs_quota -x -c report`, or equivalent). Do not run `tune2fs` modification,
`quotacheck`, quota enablement, remount, `setquota`, or any write probe during
this governance gate.

**Diagnostic command status:** prepared, **not run** against the guest.
No remote/guest access path is presently verified. Capture outputs, exact
commands, operator identity and timestamps in a later read-only evidence record
before any qualification authorization request.

## 3. Proposed cgroup/systemd containment architecture

### Service, not attach-after-start scope

Use a root-owned, immutable, dedicated, pre-provisioned **systemd service unit**
with a fixed `ExecStart` to the approved supervisor and `Type=exec`; configure
all cgroup/sandbox properties before the manager forks/execs the workload.
The service manager creates the unit cgroup and places the command there before
`execve`. `Type=exec` provides an explicit failure when the executable cannot
be invoked. Do **not** use `systemd-run --scope` as the security boundary: a
scope tracks externally started processes rather than having the service
manager directly start a service process inside the preconfigured cgroup.

The fixed unit definition and drop-ins must be provisioned and locked before
the one-shot operation; do not create it using `systemd-run` at invocation time.
Before start, an independent verifier must query the inactive unit using
`systemctl show` for every configured and effective property, inspect the
effective properties/available controllers along the owning slice ancestry,
and verify controller delegation is disabled. Any unset, inherited, unknown,
or more permissive ancestor property blocks start. This preflight does not
replace the later post-start inspection of the actual service cgroup and its
ancestors/descendants.

“Locked” means unit files, drop-ins, systemd manager configuration, required
slice/dependency units and the verifier configuration are root-owned and not
writable by the execution identity; exact file hashes, ownership, mode and
loaded unit properties are recorded. The independent verifier rechecks those
identities immediately before start; no reload or configuration writer is
permitted between preflight and start. The trusted root administrator and
systemd manager remain inside the declared trusted boundary. The supervisor's
first operation, before starting any focused test child, checks its actual
service cgroup membership and effective limits/ancestor chain and fails closed
on mismatch; this post-`ExecStart` guard supplements, but does not replace, the
pre-start inactive-unit/configuration verification.

The unit must use `KillMode=control-group`, `SendSIGKILL=yes`, finite
`TimeoutStopSec`, `OOMPolicy=kill`/`MemoryOOMGroup=yes` where supported,
`CollectMode=inactive-or-failed` only after terminal evidence is durable, no
delegate rights, no `RemainAfterExit`, and no unapproved `ExecStartPre`,
`ExecStartPost`, shell, or helper. The exact systemd version and property
availability must be established first. If the manager cannot set/query back
all required effective properties, do not start the service.

`KillMode=control-group` is intended to address all
service descendants, including the frozen test's 23 serial validator CLI
descendants. Verify `cgroup.procs`, `pids.current/max`, `memory.*`, and
`cpu.stat` for the service cgroup, every relevant ancestor, and its subtree;
do not mistake a unit-main-PID exit for an empty cgroup. `cgroup.kill` is not a
required fallback in this design; its presence cannot be determined by reading
the file, which is a write-only interface on non-root cgroups. If a later design
proposes it, separately review its availability and write authority.

### Trusted bootstrap and explicit control-plane boundary

1. A named Hyper-V host administrator prepares and verifies the isolated VM,
   disks, network disconnection, fixed memory/vCPU and host stop authority.
   This administrator, VMMS/hypervisor, guest kernel and already-running
   systemd PID 1 form the trusted infrastructure boundary, not experimental
   code. Any infrastructure exclusion/measurement policy requires explicit
   owner approval.
2. Verified source is imported as a read-only, hash-pinned ISO (or equivalent
   read-only virtual medium); no host filesystem share, writable pass-through,
   clipboard, network share, guest-to-host mount or unrestricted integration
   copy path is present during workload execution.
3. A named host administrator starts the already-registered, fixed-configuration
   VM through a recorded host operation, verifies its expected identity/state
   and logs in only through its local Hyper-V console. A pre-existing guest
   login/control session is not assumed. VM boot and login are outside the
   workload cgroup and must not start the supervisor or test. The approved
   operator then requests the single fixed service start using a narrow client
   with no script/command parameter and no ability to run the test itself.
   This client is outside the workload cgroup: **an explicit bootstrap
   exception** requiring independent review and owner authorization. No
   ordinary shell, PowerShell launcher, systemd-run scope or unbounded test
   process may run outside the unit as a fallback. The parent allowance's
   one-shot CPU/wall accounting begins before that invocation; this design has
   no mechanism yet to include outside host-client, VM-boot, or guest-login
   overhead in its whole-invocation CPU ceiling. This remains unresolved and
   is not silently excluded.
4. PID 1 creates/configures the service cgroup and properties, then forks and
   execs the supervisor directly in it. Marker admission is performed
   fail-closed before test execution by a separately approved durable
   single-use authority. Parent and qualification markers are separate and
   never reset.
5. A failed request, unit load, property configuration, execution, or query-back
   creates no fallback process. If unit presence/effective settings cannot be
   established before its `ExecStart`, the workload must not be admitted.
6. All test children use ordinary fork/exec and inherit the service cgroup.
   No cgroup migration/delegation, setuid, namespace escape, ptrace, privileged
   helper, daemonization, alternate unit/job, network, or cgroupfs write is
   permitted. Unsupported systemd features or observed movement out of the
   cgroup fail closed.
7. Systemd sends termination to the service control group. After stop,
   independently verify unit inactive, cgroup empty, all test descendants exited, and no
   surviving process IDs. An API/signal request is not evidence of completed
   termination.

The VM's local systemd can recover many workload failures, but it is not an
independent host watchdog. If the guest kernel/systemd stalls, host VMMS needs
administrator authority to power off the VM. No bounded host-side reaction
latency or automated independent watchdog is presently demonstrated. No
networked host controller is allowed. Do not accept a bootstrap exception,
manager/accounting exclusions, or this proposed trusted boundary without the
owner's explicit approval.

## 4. Linux control semantics and proposed resource map

The guest cgroup memory charge is not Windows aggregate working set. Linux
`memory.current`/`memory.peak` charge cgroup memory (including categories such
as anonymous/file cache and kernel-accounted memory according to kernel
configuration); the counters do not represent only resident user-process pages.
The Hyper-V host's VM-worker process working set is not guest process working
set either.

| Original resource | Candidate enforcement / exact meaning | Evidence | Failure and difference from parent |
|---|---|---|---|
| One CPU allocation | systemd `AllowedCPUs=<one verified effective guest CPU>` plus `CPUQuota=100%` (cgroup `cpuset.cpus` plus `cpu.max` rate). One guest vCPU in Hyper-V would be a separate host setting; current four-vCPU claim is not verified. | Query effective cpuset and `cpu.max`; log host vCPU settings. | Native rate/placement controls for unit tasks; no cumulative CPU limit. Pinning one CPU does not pin systemd/OS or host accounting. |
| 120 CPU seconds | cgroup `cpu.stat` `usage_usec` is aggregate unit CPU time; `user_usec` and `system_usec`, if present, are components for reconciliation and must not be added to the total. These account for unit tasks, not the external host bootstrap client. `cpu.max` limits bandwidth per period, **not lifetime total**. | Before/after `cpu.stat`, in-run samples, final all-descendant exit status and monotonic timestamps. Never add parent/child cgroup aggregate counters or add component counters to `usage_usec`; record bootstrap separately. | Cgroup counter is accounting; watchdog is monitoring/action, not native cumulative cutoff. Host bootstrap work is outside the unit and is not included in the original full-invocation aggregate ceiling by this candidate design. Poll/dispatch/kill delay has no finite bound established. Strict 120s remains unresolved. |
| 180 wall seconds | systemd service `RuntimeMaxSec=180s` requests unit stop; finite `TimeoutStopSec`, `KillMode=control-group`, and `SendSIGKILL=yes`. A separate host-side monitor could `Stop-VM -TurnOff` if guest management fails. | Guest monotonic start/stop and service result; host VM state transitions/time, unit/cgroup empty state. | `RuntimeMaxSec` is manager-driven termination, not hard real-time cessation. Guest scheduling, VM pause and host manager/API completion latency are not bounded. No timeout API has been tested; exact 180s cap remains unresolved. |
| 512 MiB aggregate working set | **No equivalent cgroup control.** Candidate `MemoryMax=536870912` -> `memory.max=536870912` bytes, `MemoryAccounting=yes`, `MemorySwapMax=0`, `MemoryOOMGroup=yes`. | Effective `memory.max`, `memory.swap.max`, `memory.peak`, `memory.events` (`max`, `oom`, `oom_kill`), `memory.stat`; capture before cleanup. | Hard cgroup charged-memory ceiling with reclaim/OOM behavior; not aggregate working set, not Windows working set, and no claim of equivalent resource classes. Requires a separately reviewed **explicit owner-approved metric amendment** before qualification or execution. Without it, original requirement is unmet and no execution is released. |
| 512 synthetic records | Keep exact parent combined stimulus + JSONL trace record counter in software. | Checker reconciles generated inputs and emitted rows to <=512. | Software accounting, not an OS resource limit; exact frozen per-case allotments remain unchanged. |
| 5 MiB artifacts | Dedicated artifact mount with hard filesystem/quota boundary, plus mediated single-writer output and a 64 KiB failure reserve within the 5 MiB total, if exact logical byte counting is proven. | Quota usage and file-size manifest/hashes before export, quota events, mount and inode evidence. | Post-run size check alone is not enforcement. Block quotas count charged blocks, not necessarily logical file lengths; sparse files, alternate streams, temp/stdio paths and metadata need handling. No backing filesystem/support verified. No export to the 256 GB archive as a substitute cap. |
| One supervisor / three child tests / zero retries | One durable marker before unit start, authorization revision and VM/cgroup/unit identity bound to marker; all three exact child test identities invoked once, serially. No optional/retry mode. | Host marker plus guest unit invocation ID, argv/image hashes, monotonic lifecycle record, terminal status. | Marker on guest VHDX can be rolled back/reset; canonical one-shot ledger needs a separately controlled durable host authority. Host ledger is a limited bootstrap exception requiring approval. Parent allowance remains untouched during A4 and qualification. |
| Process descendants | `pids.max`/systemd `TasksMax=` candidate 64 tasks, after checking Node thread use. `KillMode=control-group`. | `pids.current/max/events`, full cgroup tree/PIDs before, during, after; child command audit. | `pids.max` counts tasks/threads, not simply processes; failed fork at limit returns resource failure. 64 is a proposed qualification ceiling, not parent-gate requirement. Existing 23 sequential CLI child launches are preserved, not denied. |
| Offline network | No Hyper-V vNIC or disconnected adapter, no guest routes, `PrivateNetwork=yes` as defense in depth, no network family access. | Host adapter/switch inventory and guest `ip`/route state, service unit network namespace properties. | Guest `ip link` alone cannot prove host isolation. Host state currently inaccessible; no networking changes/run allowed. |

`memory.peak` and `memory.events` measure/record charged-memory state and limit
events. `cpu.stat` measures cumulative usage; `cpu.max` is a hard rate/quota.
`pids.max` is a hard task-count limit. Systemd
`RuntimeMaxSec` and watchdogs are managed stop triggers, not a proven exact
response-time ceiling.

### Memory approval gate

The only numerical same-ceiling Linux proposal is
`memory.max=536870912` charged bytes with swap disabled. It **changes the
original memory metric**, must not be labeled equivalent, and is not selected
or owner-approved. It can be considered only as a separately identified
resource-policy amendment. If the owner does not explicitly approve the
precise metric/scope before qualification, retain the original aggregate
working-set requirement and block.

## 5. Artifact / host storage policy

The owner-reported 128 GB system VHDX and 256 GB archive VHDX are not the 5 MiB
artifact allowance. The large archive is never used as a quota substitute.

Conditional storage design, requiring read-only capability verification and
later explicit authorization:

1. Import only hash-verified corrective source/goldens on a read-only ISO; record
   all paths/hashes. Disable guest networking and do not expose writable host
   filesystem shares, SMB, SSH, clipboard, host mounts or arbitrary
   `Copy-VMFile` while tests run.
2. Do not mount the 256 GB archive VHDX in the workload. Attach a distinct
   evidence VHDX to the guest only if needed. It is a virtual block device,
   not a host directory share. The host does not open/mount it while the guest
   is active.
3. Preconfigure one dedicated guest artifact filesystem/project with a hard
   quota. Use ext4 project quota only if its feature/mount/project-ID state is
   read-only verified; otherwise do not run. Candidate charged-block limit is
   5 MiB total and an inode cap; reserve 64 KiB of that same allowance for
   terminal failure evidence and restrict ordinary logs/data to the remaining
   space. No ordinary output path outside the bounded mount is writable.
4. Route `os.tmpdir()`, `/tmp`, `/var/tmp`, child stdio, JSONL trace and summaries
   into the restricted artifact/work mount or a distinct bounded scratch area
   included in the same total. Restrict unit with `ProtectSystem=strict`,
   `ReadWritePaths` only to those paths, `PrivateDevices`, `PrivateNetwork`,
   `NoNewPrivileges`, read-only home/source, no delegate/capabilities and
   fixed umask. A4 makes no claim these exact sandbox combinations have been
   runtime-validated against Node/systemd.
5. Define the parent artifact acceptance measure as logical lengths of every
   retained test-output and lifecycle-trace file, including supervisor/test
   stdout and stderr, temp inputs that remain at termination, and the retained
   failure record; total <= 5,242,880 bytes. The 65,536-byte failure reserve
   is inside that total, leaving <= 5,177,344 bytes for ordinary artifacts.
   A single artifact filesystem and mediated writer must enforce this same
   aggregate total. Separate scratch volumes/quotas are forbidden unless their
   bytes are charged to that aggregate. systemd journal/manager logs are
   control-plane diagnostics, not parent test-output artifacts, but their
   destinations, maximum size, retention and host-disk cost must be separately
   bounded and accounted for in the reviewed policy.
   Quota alone caps charged blocks, not necessarily logical sparse-file length.
   The writer must mediate every artifact/temp/stdio path or deny all other
   writable paths; it fails synchronously before a write exceeding the total.
   Ordinary writes cannot consume the 65,536-byte emergency reserve. The
   failure path must demonstrate reserved preallocation or an equivalent
   non-allocating record path and durable flush; “if available” is not reserve
   enforcement.
6. On ENOSPC/quota event/write failure, stop the unit, retain the reserved
   failure record, mark evidence incomplete/FAIL and do not retry.
   If termination or evidence durability is unknown, preserve the VM/disk
   read-only and classify as incomplete; no cleanup may erase evidence.
7. After the cgroup is independently confirmed empty and the VM is stopped,
   an owner-controlled host operator may export the bounded evidence VHDX
   read-only into a fixed-destination quarantine. Recompute file hashes and
   verify total size before publication. Host export is an offline review step,
   not a test-run writing channel; host destination limit and provenance need
   separate approval. Do not attach/mount the 256 GB archive to increase space.

This proposal is intentionally not a claim that quota plus post-run size
measurement provides a hard logical-byte cap. Exact quota semantics, sparse
file behavior, scratch accounting, pre-write enforcement, export, and reserved
failure evidence must be independently demonstrated in qualification. If not,
artifact enforcement is unresolved.

## 6. Resource-stop and failure behavior

- Unit creation/effective-property mismatch: refuse unit start; no fallback.
- Cgroup memory high/max/OOM event, CPU threshold or artifact quota event:
  request unit stop; record event and monotonic time; verify the whole cgroup
  is empty and all descendants exited. Do not count an API/signal return as
  completion.
- At 180 seconds: systemd requests stop and `TimeoutStopSec` escalates to
  SIGKILL. A preconfigured host administrator watchdog may turn off the whole
  VM if guest PID 1/control path fails, but its trigger and action latency are
  not yet bounded or authorized.
- Guest kernel/systemd stall or VM pause: in-guest watchdog cannot prove timely
  wall stop. Host authority must independently observe and terminate; no host
  controller/service and no bounded control-plane delay is evidenced now.
- cgroup kill/error or VMMS stop request: preserve cgroup/disk state, query for
  survivors and terminal VM state, record failure. If state cannot be reconciled,
  mark incomplete and retain without retry.
- Out-of-policy service, cgroup, process, network adapter, writable mount,
  unexpected VHDX, unauthorized service/scope or marker ambiguity: refuse before
  workload starts.

An exact strict CPU stop at 120 seconds and exact wall stop at 180 seconds are
not established merely by setting a poll interval or a systemd timeout. A4
proposes no overshoot allowance. If implementation requires a bounded nonzero
stop grace or sampling tolerance, quantify it as a separate proposed resource
amendment and obtain independent review and explicit owner approval; otherwise
do not execute.

## 7. Separate qualification authorization proposal

This A4 qualification proposal **replaces, and is not additive to, A3's
unapproved provisional qualification proposal**; neither proposal is approved
or executable. It is separate from the exhausted scientific pilot and the
parent corrective budget. It is a proposal only; no code/VM changes/tests/runs
are authorized now. Its per-case record allocations must be frozen in an
exact test plan before owner authorization; the aggregate 128-record ceiling
does not authorize inventing or exceeding case-level allocations.

| Resource | Proposed maximum |
|---|---|
| Invocations | One dedicated qualification supervisor invocation, one-shot durable host marker; interruption/uncertainty consumes it; zero retries |
| Cases | Exactly 12 deterministic containment/resource cases below; not a corrective test |
| Synthetic fixture/stimulus/trace records | 128 combined maximum |
| CPU allocation | One effective guest CPU (`AllowedCPUs` one CPU; `CPUQuota` no more than 100%); qualification monitor/control plane is separately recorded and needs explicit scope policy |
| Aggregate CPU | 60 CPU seconds for the entire qualification invocation, including bootstrap/control work. `cpu.stat` `usage_usec` is aggregate for service tasks; `user_usec`/`system_usec` are components for reconciliation, not extra sums. The outside host bootstrap is currently outside this measurement. No unbounded continuation if watcher fails. This proposal is **not executable** until whole-invocation accounting and stop policy are owner-approved and independently reviewed |
| Aggregate wall | 120 monotonic seconds from marker admission through terminal reconciliation; host and guest timestamps; no established maximum watchdog latency, so this budget is **not executable pending** a bounded fail-closed design |
| Qualification cgroup memory | 512 MiB charged memory maximum (`memory.max`) candidate; memory metric is changed and requires explicit owner approval. Guest OS/Hyper-V memory is outside this cgroup and separately observed, not silently claimed within 512 MiB |
| Artifacts | 2 MiB hard quota total, including 64 KiB reserved terminal evidence; qualification outputs only. Separate from parent 5 MiB |
| Process tasks | `pids.max=64` proposed for Node/runtime threads; verify effective count; includes all unit tasks/descendants |
| VM resources | No change to 4-vCPU/8-GiB owner-reported VM; cgroup gets one CPU. Any host VM setting change is separate infrastructure authorization |
| Allowed repository paths | Read-only: frozen R4.3 inputs/tests and reviewed corrective baseline. New qualification implementation only under `experiments/luna64/a4-qualification/`; raw evidence only under `workflow/evidence/luna64-r4.3-a4-qualification-20261011/`; one governance handoff under `workflow/handoffs/`. No edits to protocol/goldens, reward implementation, production/core, ACP or Luna-63C |
| Scientific data/code | No pilot runner/generator, training/evaluation, scientific dataset, labels, benchmark, network, GPU or arm execution |
| Independent review | Exact source/config/binary hash review before execution authorization; read-only qualification evidence review after; no implementer self-approval |
| Downstream effect | Qualification PASS would only qualify the tested supervisor under the exact identified host/guest/kernel/systemd configuration. It does not consume or release the parent corrective allowance or authorize correction/tests/experiment |

**Required cases (all currently NOT RUN):**

1. Source/disk/config hashes, VM identity, guest boot, offline NIC and
   no-writable-host-share preflight.
2. Inactive-unit property/configuration and ancestor preflight before start;
   then first supervisor operation verifies actual service cgroup membership
   and effective limits before any focused-test child `exec`. Failed preflight
   or runtime verification causes no focused child and no fallback.
3. `pids.max` enforcement, nested grandchildren and all descendants retained
   in one unit cgroup; recreate the 23 serial CLI calls only as harmless
   synthetic command probes, not the corrective tests.
4. `memory.max` under-limit behavior, above-limit denial/OOM event, and
   whole-unit kill; verify `memory.peak`, `memory.events`, swap state. Only if
   owner approves changed memory metric.
5. `cpu.max` one-CPU rate and cgroup `cpu.stat` `usage_usec`, `user_usec`,
   `system_usec` (where provided), including exited descendants; validate no
   double count.
6. Cumulative CPU watcher trigger near the proposed 60s limit and stop
   completion; quantify the maximum observed overshoot without claiming it is
   a hard bound unless independently justified.
7. `RuntimeMaxSec` wall trigger, `TimeoutStopSec` escalation, cgroup empty
   verification, monotonic start/termination timestamps; quantify delay.
8. Kill supervisor/controller, hang it, interrupt control path, simulate guest
   pause/resume; host shutdown response, VM terminal state and descendant exit.
9. Filesystem/project quota at cap, one-byte-over write, sparse-file attempt,
   inode exhaustion, temp/stdio diversion, alternate path and export denial.
10. Failure-record reserve, abruptly terminate writer, quota/FS failure and
    post-run hashes/total; ensure no success-shaped fallback.
11. CPU affinity/effective cpuset, guest vCPU inventory and offline network
    (no route/interface connection) evidence.
12. Marker create-new, existing/malformed/inaccessible marker, rerun/rollback
    attempt, incomplete result and allowance reconciliation; parent marker
    remains absent.

The 12-case list includes cases that need the 128-record maximum; case allocation
must be frozen in a future exact test plan before authorization. No fixture or
per-case records are being executed now.

## 8. Readiness blockers and owner-approval separation

1. Host Hyper-V management is present, but the current token cannot inspect the
   VM or demonstrate termination rights. Obtain authorized read-only VM,
   switch, VHDX and integration-service evidence.
2. Obtain guest diagnostic outputs and hashes for Ubuntu/kernel/systemd/cgroup
   v2/controllers/cgroup kill, storage/quota support, network, and shutdown
   integration. Owner-reported details remain claims until then.
3. Obtain independent owner/administrator attestation for the offline VM,
   fixed RAM/vCPU, actual disks, no writable host shares, host poweroff and
   evidence-export path. Do not configure or change anything during A4.
4. Obtain explicit owner approval for a proposed 512 MiB **cgroup charged
   memory** alternative if the original 512 MiB aggregate working-set metric
   cannot be maintained. No approval is inferred from requesting A4 or the
   parent corrective authorization.
5. Resolve exact CPU and wall termination bounds under guest pause, controller
   failure and host scheduling, or propose a quantified nonzero overshoot policy
   and obtain separate owner approval. A runtime timer/poll target is not a
   worst-case bound.
6. Prove hard artifact accounting includes temporary files, stdio, traces,
   sparse writes, reserved failure evidence and export, without host shares.
7. Freeze the executable/descendant list, effective unit properties, systemd
   version, supported kernel controls, durable qualification/parent markers and
   error/terminal evidence; independently review.
8. Owner approval of A4 qualification is separate from approval of the changed
   memory metric and separate from eventual corrective execution authorization.
   A qualification PASS does not automatically authorize the parent one-shot
   correction or any scientific rerun.

## 9. Validation performed in this governance phase

| Procedure | Result |
|---|---|
| A3 publication ref / local HEAD | Verified `8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0` |
| Parent gate checksum / R4.3 manifest checksum | Verified against frozen records |
| Corrective worktree and marker state | Clean baseline `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`; parent and A2 markers absent |
| Host OS/CPU/RAM/hypervisor/service metadata | Observed as reported for Windows/Ryzen/32 GiB/active hypervisor/services |
| Hyper-V VM configuration/stop permission | **Not verified**; `Get-VM` denied by current token |
| Ubuntu/kernel/cgroup/systemd/storage/network/shutdown | **Not verified**; diagnostic bundle prepared, not run |
| cgroup/systemd source semantics | Official kernel/systemd documentation consulted; not runtime proof |
| Installation, enabling, mount/quota changes, VM start/stop | **Not performed** |
| Qualification, corrective tests, scientific workload | **NOT RUN** |

## 10. Sources and status

- Linux kernel [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html):
  `memory.max`, `memory.peak`, `memory.events`, `cpu.max`, `cpu.stat`,
  `pids.max`, cpuset and cgroup-wide controls.
- systemd [resource control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html):
  `MemoryMax=`, `MemorySwapMax=`, `CPUQuota=`, `AllowedCPUs=`,
  `TasksMax=`, accounting and OOM group behavior.
- systemd [service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html):
  `Type=exec`, `RuntimeMaxSec=`, stop/kill modes and timeout semantics.
- systemd [systemd-run](https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html):
  scope versus transient service, property setup, synchronous start/wait.
- Microsoft [Get-VM](https://learn.microsoft.com/en-us/powershell/module/hyper-v/get-vm?view=windowsserver2025-ps)
  and Hyper-V management documentation. Local `Get-VM` could not query due
  token permissions.

The A4 assessment does not amend the TPCN architecture contract or frozen R4.3
scientific protocol. Resource accounting is an execution-governance decision,
not an A01-A15 computation change.

**Stop condition:** until exact guest/platform evidence, memory-policy approval,
strict CPU/wall closure, artifact containment and the separately reviewed
qualification budget are resolved, remain **BLOCKED**. This A4 package is not
permission to qualify, implement, test, rerun the pilot, or promote any
architecture.
