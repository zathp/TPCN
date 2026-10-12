# Luna-0 — Luna-64 A6 Enforcement Closure and Owner Decision Gate

**Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6`  
**Disposition:** **BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE**  
**Scope:** Governance-only resource-policy proposal and owner decision gate.
No supervisor, qualification case, corrective test, or scientific workload was
implemented or executed.

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-64 A6 enforcement closure and owner decision gate"
  task_id: "L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6"
  component: "Experimental execution resource governance"
  status: "blocked"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "b758b411e568b41c516228e7d3bdff26058114cc"
  result_revision: "Uncommitted working-tree governance record; A6 blocked and not published"
  dependencies: ["Frozen R4.3", "owner-authorized corrective gate", "A1-A5 blocked supervisor amendments"]
  owner: "Repository owner"
  classification: ["GOVERNANCE ONLY", "NO QUALIFICATION AUTHORIZATION", "NO CORRECTIVE EXECUTION AUTHORIZATION"]
  hypothesis: "The retained Hyper-V/systemd/cgroup architecture can enforce an owner-approved replacement resource contract if CPU cutoff, staged termination and complete artifact mediation are qualified."
  counter_hypothesis: "The host/guest control paths have no defensible finite termination bound, or the artifact namespace cannot preserve the frozen test filesystem behavior under a hard logical-size limit."
  interfaces_relied_on: ["Hyper-V control", "systemd 259 service/cgroup v2", "one read-only source volume", "host watchdog channel", "bounded FUSE artifact volume"]
  label_information_boundary: ["No scientific records, labels, model state, or task payloads are permitted in qualification."]
  timing_assumptions: ["Host QPC is authoritative; no OS response-time bound is claimed."]
  reset_boundaries: ["A6 qualification marker is separate from the parent corrective marker and all historical pilot records."]
  resource_bounds: ["Original corrective allowance remains unused; all A6 resource values are proposals requiring approval."]
  authorized_scope: ["Read-only provenance review", "Governance proposal and independent review", "Workflow publication"]
  unauthorized_scope: ["Supervisor implementation", "Qualification execution", "Corrective tests", "Scientific workloads", "Infrastructure changes", "Luna-63C changes"]
  controls: ["Exact A5 identity verification", "Owner-reported platform evidence labeled as such", "Separate qualification budget", "Three independent domain reviews"]
  measurements: ["Git ancestry and hashes", "source/document semantics", "resource-policy arithmetic"]
  information_boundary_check: ["No labels, scientific inputs, training, reward traces, or Luna-63C artifacts used."]
  hardware_mapping: ["Execution containment only; no hardware-equivalence claim."]
  architecture_invariants_touched: ["A01-A15 unchanged; no TPCN computational architecture change."]
  preserves: ["Frozen R4.3", "accepted reject-only second-origin policy", "A1-A5 findings", "original pilot NOT SUPPORTED verdict", "unused corrective allowance", "Luna-63C isolation"]
  architecture_change: false
  proposal: null
  files_changed: ["A6 proposal", "A6 evidence", "A6 integrated review", "LUNA_WORKFLOW.md"]
  tests_added: []
  tests_passing: ["A5 proposal/review hashes and A5 publication ancestry verified.", "A6 JSON syntax and proposed budget arithmetic validated.", "Independent CPU/wall, artifact, and governance reviews reconciled."]
  tests_failed: []
  tests_not_run: ["All qualification cases", "All corrective tests", "All scientific workloads", "All host/guest enforcement checks"]
  assumptions: ["Owner-supplied Windows/Ubuntu inventory remains unverified reviewer evidence."]
  unresolved: ["Hard CPU cutoff and termination bound", "VM-off latency", "FUSE implementation/compatibility", "owner approval of proposed resource changes"]
  recommended_next_agent: ["Repository owner: decide whether to authorize the disclosed memory, CPU, wall, artifact, infrastructure and qualification-budget amendments; no A7 is proposed."]
```

## 1. Purpose and evidence labels

A6 is a bounded successor to the published A5 block. It retains the existing
Hyper-V host, Ubuntu systemd/cgroup v2 guest, dedicated service cgroup,
separate resource monitor, restricted artifact volume, and host-controlled
emergency termination. It does not reopen architecture selection unless
qualification demonstrates a contradiction.

Evidence labels used here:

- **OBSERVED (repository):** exact Git and file identities verified from this
  checkout.
- **OWNER-REPORTED:** host and guest inventory summarized by the owner; raw
  captures, per-command times, and hashes were not supplied and were not
  independently rerun.
- **DOCUMENTED:** behavior specified in the cited operating-system
  documentation.
- **PROPOSED / UNQUALIFIED:** design parameters and resource values below.
  They are not evidence of runtime enforcement.

## 2. Verified authority and frozen boundary

| Record | Identity and retained status |
|---|---|
| A5 package | `12f84a41fe7c91c17c5df8e975fce24efbadf9ad` |
| A5 workflow closure | `b758b411e568b41c516228e7d3bdff26058114cc` |
| A5 proposal | SHA-256 `5BCDAC72E7EBDEA777E9964F25554834C4460D97075E6871690BD441BA00C6E5` |
| A5 integrated review | SHA-256 `54D11A362EDED451292330C6FA5627B570BD6103ADE0F69E115F5CDC3C7B934D` |
| Frozen R4.3 content / governance closure | `64a214e310de3b982b90a8ad215598bc1e9f8b1c` / `ea1b10456cbf4ca726e473076d239a4f6e53b9c7` |
| Frozen manifest | SHA-256 `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B` |
| Corrective gate | SHA-256 `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369` |
| Corrective owner authorization | Commit `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`; authorization file SHA-256 `972701FBD7394AF655F27E8CCDC394483AAD7B018F25E7A5A41A2C98F9E8BA44` |
| A1 | `d20aab249e42575ccc571c9c72153a3bb4b412db` — **BLOCKED — RESOURCE SUPERVISION UNRESOLVED** |
| A2 | `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c` — **BLOCKED**. Preserve review hash `E00B75004D3085EFDA60D7163D57153F2FCB2D089162574358794BBA54145591`, published Git-blob hash `9FAF922016726FBB5B1EAEBBC8B9488A293E99FC830738E02F3A9A9CD7D958AD`, and CRLF checkout hash `05C401518A74B1957697E6F12C8877E4D9F8F734A4A7B1432CDF3C9520AE835A`; discrepancy is not repaired or elevated to approval. |
| A3 | `8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0` — **BLOCKED — NO QUALIFIED EXECUTION ARCHITECTURE** |
| A4 package / closure | `7bd440565c38dee81ace3606fde3fb686de6a0ef` / `f86c25844a4863ac57cd6634f364c28bcf2f511f` — **BLOCKED — ISOLATION QUALIFICATION UNRESOLVED** |
| A5 | Package `12f84a41fe7c91c17c5df8e975fce24efbadf9ad`; closure `b758b411e568b41c516228e7d3bdff26058114cc` — **BLOCKED — A5 QUALIFICATION INCOMPLETE** |
| Original pilot | **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not an efficacy result; scientific budget exhausted |
| Corrective allowance | One invocation, three exact focused tests, zero retries, 512 combined synthetic records, one logical CPU, 120 aggregate CPU seconds, 180 wall seconds, 512 MiB original aggregate peak Windows working set, and 5 MiB artifacts; remains unused |
| Luna-63C | Unchanged and isolated |

The published original owner authorization explicitly accepts only the
**reject-only malformed second-reward-origin policy**: reject the second
distinct origin without changing, replacing, delaying, resetting, reopening,
settling twice, or charging again for the first; the first proceeds under the
frozen lifecycle, including after zero-delay settlement. No additional
malformed-input policy is inferred.

A1, A2, A3, A4, and A5 retain their published blocked findings. A2's
review/published-blob/checkout discrepancy is preserved. In particular, A5
remains **BLOCKED — A5 QUALIFICATION INCOMPLETE**. A6 does not use its
qualification budget as authority and does not consume, replace, or replenish
the parent's corrective allowance.
The A6 proposal does not close or supersede A1-A5. Any future corrective or
scientific execution request must separately address each applicable prior
blocker; neither owner policy approval nor a future A6 qualification pass
automatically clears those historical verdicts.

The A5-reported infrastructure remains **OWNER-REPORTED**: Windows 10 Pro
build 19045; Hyper-V VM `TPCN-Isolated-Training`,
`60e9baef-706e-4490-80d7-38618710546e`; Ubuntu 26.04.1, systemd 259, cgroup
v2; networking disconnected; four reported vCPUs and 8 GiB fixed guest RAM.
The A5 review did not independently verify host/guest runtime settings or
termination latency. A6 did not run diagnostics or touch the VM.

## 3. Retained execution architecture and trusted boundary

| Component | Proposed role / trust | Workload influence and current evidence |
|---|---|---|
| Windows Hyper-V host, VMMS, hypervisor, host QPC | Trusted outer boundary and emergency VM control; host controller binds all operations to the exact VM GUID and name. | Corrective workload has no host credentials or writable host mount. Owner reports elevated token and VM configuration; authority, controller scheduling and maximum `TurnOff` latency remain unqualified. |
| Ubuntu kernel and systemd PID 1 | Trusted cgroup placement, unit policy and process termination. | Workload runs unprivileged with no cgroup delegation, capabilities, unit-control socket, mount privilege, or writable system files. Kernel/systemd behavior is documented, not runtime-qualified here. |
| Dedicated workload service cgroup | Contains supervisor, the three exact child tests and all descendants. No workload process may migrate itself or create a delegated subtree. | All fork/exec descendants inherit membership unless a privileged actor migrates them; exact ancestor controls and all process membership require qualification. |
| Root-managed guest monitor | Separate systemd service/cgroup in the dedicated accounting slice; samples aggregate `cpu.stat`, observes the workload leaf's `cgroup.events`, records bounded evidence, and signals host on cutoff/failure. | Workload cannot ptrace or reconfigure it. A proposed 5% cgroup CPU share protects monitor scheduling budget; same guest kernel/scheduler remain shared. It is trusted but not independent of guest/kernel/VM failure. |
| Host watchdog/controller | Uses QPC, authenticates guest status, enforces the wall deadline and requests `Stop-VM -TurnOff` when required. | Workload cannot access its token or storage. It is not independent of Windows scheduling, VMMS, Hyper-V host failure, or its control channel. |
| Guest-host control/evidence channel | Required for authenticated heartbeat, cutoff requests, counter/evidence receipt and health state. | Owner-reported guest networking is disconnected and Guest Service Interface is disabled. A supported transport, authentication, ACLs, failure behavior and timing are not identified or verified; the guest must not assume network or Guest Service Interface access. This is an open admission blocker. |
| Artifact filesystem daemon and fixed backing volume | Trusted quota mediator plus dedicated mounted artifact namespace. A candidate FUSE service handles POSIX file operations and a root-only failure reserve. | Workload receives only the mediated mount; no direct backing-volume descriptor, writable alternative path, or daemon control channel. Implementation and compatibility are not established. A proposed 5% cgroup CPU share protects its service budget. |
| Frozen test processes | Untrusted execution target; exactly the authorized three commands and required validator descendants. | May create temporary files and attempt any accessible write path; cannot alter supervisor, policy, cgroups, monitor, host or backing storage directly. |

**Bootstrap rule:** VM boot, read-only source verification and policy
provisioning are preparation, not corrective workload. They must complete
before the one-shot invocation. Immediately before dispatch, the host verifies
VM identity, no active workload, locked systemd unit, cgroup ancestors,
effective controls, monitor health, and artifact mount. Any mismatch consumes
the one-shot attempt and dispatches no corrective command. The host admission
clock begins immediately before requesting the already-booted service start.
No unbounded workload launcher runs before the service cgroup is effective.

**Trusted computing base:** Windows administrator account, host controller and
watchdog, VMMS/hypervisor, guest firmware/kernel/systemd, root-owned monitor,
FUSE daemon, source-image verifier, cgroup configuration, filesystem backing
device and evidence verifier. The workload and all its descendants are
untrusted. The monitor does not become trustworthy merely by being in a
sibling cgroup; qualification must demonstrate its privileges, channel
isolation and failure response. The present proposal does not select or
qualify a guest-host status transport; no workload may start until a
non-network, host-controlled authenticated channel is specified and admitted.

## 4. Proposed memory decision

### Exact replacement offered to the owner

Replace the original **512 MiB aggregate Windows peak working-set** condition
with **512 MiB of Linux cgroup-accounted memory**, and permit **zero additional
cgroup swap usage**:

```ini
MemoryMax=512M
MemorySwapMax=0
MemoryOOMGroup=yes
```

The effective workload-leaf values must be queried directly and equal:

```text
memory.max       = 536870912
memory.swap.max  = 0
memory.oom.group = 1
```

`MemoryMax=512M` uses systemd's base-1024 suffix and maps to the exact byte
limit shown. `MemoryMax` controls `memory.max`; `MemorySwapMax` controls
`memory.swap.max`; `MemoryOOMGroup=yes` requests group treatment for a kernel
OOM kill through `memory.oom.group`. These controls must be applied before
the supervisor is executed and must remain effective in the leaf and all
descendant cgroups.

The cgroup charge is not a Windows working-set measurement. It is hierarchical
memory-controller accounting for processes in the cgroup subtree, including
at least charged anonymous/file-cache categories and kernel-accounted memory
as reported by the guest kernel. Descendant processes are included by cgroup
membership, not by inspecting a Windows-style process tree. A child cannot
escape by reparenting; moving itself requires permissions that the workload
must not possess. `memory.max` may cause reclaim and then cgroup OOM handling;
it is not a promise that every allocation fails at a single exact resident
byte count.

`MemorySwapMax=0` forbids additional swap charged to this cgroup. It does not
by itself establish zero guest-wide swap, disable host-side Hyper-V memory
overcommit, or bound unrelated guest memory. Qualification must inspect
`memory.swap.current`, effective ancestor limits, guest swap configuration,
and `memory.events`; any nonzero charge or unexpected counter increase fails
the run. The proposed no-swap policy must also rule out configured zswap or
other mechanisms that would undermine the intended accounting, or document
their distinct treatment and obtain owner approval.

Record before/after `memory.peak`, `memory.current`, `memory.swap.current`,
`memory.events`, `memory.events.local`, and `memory.stat`. An increment in
`max`, `oom` or `oom_kill`, a nonzero swap charge, or an OOM exit makes any
corrective invocation fail, even if tests otherwise exit successfully. The
intentional qualification memory-probe case passes only when it causes the
declared limit behavior, terminates the probe's entire leaf, and retains
failure evidence. No memory-limit event is allowed in ordinary cases.

This is a **material policy change**, not a finding of equivalence. It requires
explicit owner approval of the metric, exact byte limit, zero-swap rule,
scope, and failure treatment before qualification or corrective execution.
The Linux metric is a proposed Linux-only replacement and is not equivalent
to, or evidence for, the original Windows working-set behavior. Until the
owner approves this replacement, no Linux cgroup memory limit is authorized
as a substitute; the original requirement remains the governing policy and
has not been demonstrated by the available guest diagnostics.

## 5. Cumulative CPU and termination proposal

### Accounting scope

The workload service cgroup starts empty and contains the corrective
supervisor before its first instruction. Its child tests run serially in the
same subtree, including the 23 required sequential validator CLI descendants
of the first test. A dedicated parent slice contains only the workload unit,
root-managed guest monitor and FUSE daemon. After those trusted services are
ready, the host records the slice's baseline `cpu.stat` immediately before
activating the workload unit at `T0`. The measured quantity is the subsequent
`usage_usec` delta from that baseline; monitor and FUSE CPU after `T0` are
included. `usage_usec` is cumulative user-plus-kernel CPU time in
microseconds; `user_usec` and `system_usec` are components for reconciliation
and must not be added again. The final sample is taken by a trusted
out-of-slice evidence collector only after the workload leaf, guest monitor
and FUSE daemon have exited and the measured slice reports `populated=0`;
retain the slice until that read is sealed. The evidence collector/bootstrap
CPU is outside this corrective metric, separately accounted in the outer
qualification budget, and requires explicit owner approval as part of the
measurement scope. If a host emergency stop prevents a complete final sample,
classify the attempt as containment failure, never as within-budget. Use a
unique one-shot slice/unit so counters cannot be reset or contaminated by a
prior invocation.

The dedicated guest accounting slice's counter includes the supervisor, every
test descendant, guest monitor and FUSE-daemon CPU. It excludes host
controller/watchdog CPU, VM boot, preflight and unrelated guest services,
which are reported separately. The host-controller and evidence-collector
exclusions and the start boundary require explicit owner approval. The outer qualification cgroup
includes the guest monitor, FUSE daemon and all qualification processes; its
aggregate counter includes those guest processes, while the host controller
remains separately accounted.

### Candidate monitor and explicit margin

The candidate policy constrains the dedicated accounting slice to one
effective CPU using an enabled `cpuset` hierarchy and a single-CPU
`cpuset.cpus.effective`, plus parent `cpu.max=100000 100000`. Candidate child
quotas are 90% for the workload, 5% for the monitor and 5% for the FUSE
daemon, all in the same 100 ms period; their effective `cpu.max` values must
be read back before dispatch. This reserves bounded rate capacity for the
monitor/mediator but does not guarantee either process a real-time schedule.
`CPUQuota`/`cpu.max` is a bandwidth ceiling, not a lifetime CPU-seconds
limit. If cpuset cannot be enabled through preapproved root-managed ancestors
or the exact quota hierarchy cannot be verified, do not launch.

The guest monitor polls `cpu.stat` at a **100 ms target interval**, retaining
A5's proposed interval rather than silently tightening it. A host heartbeat
is considered stale at **250 ms** after the last authenticated message; this
is an acceptance target, not a measured maximum. Monitor and FUSE CPU are
included in the measured parent-slice total and are bounded by their proposed
5% child quotas. At
`usage_usec >= 120000000`, the monitor immediately writes `1` to the
workload `cgroup.kill`. If `cgroup.events` still reports `populated 1` one
second after that request, the host watchdog requests `Stop-VM -TurnOff`. The
VM must be confirmed Off within nine seconds after that host request and by
`T0+180s`, whichever is earlier.

The explicit replacement candidate is **120 CPU seconds of authorized work
plus a 10.1 CPU-second termination reserve, for a 130.1-second absolute
guest-slice ceiling**. The conditional derivation is one effective CPU
multiplied by the 0.1-second polling target, one-second cgroup-kill stage and
nine-second VM-Off stage. The monitor's CPU is included in this slice total.
No additional overshoot is permitted. This is a disclosed resource-policy
amendment, not a silent reinterpretation of the original 120-second ceiling.

The 100 ms polling interval, 250 ms heartbeat, and 1+9 second response
envelope are **targets, not guaranteed bounds**. Linux scheduling,
FUSE/kernel stalls, a guest monitor failure, host scheduling, the control
channel, VMMS and Hyper-V
turn-off have no demonstrated maximum response time here. `cgroup.kill` is a
kernel termination request, but documented semantics do not establish a
real-time completion bound for an arbitrary workload. One vCPU bounds
consumption rate only while the VM is actually ceasing within a bounded
time. A delayed or failed host request can exceed 130.1 CPU seconds. Therefore
the proposed 130.1-second amended ceiling is a transparent owner decision
candidate but is **not presently enforceable or independently justified as a
hard maximum**.

Required failure classification:

1. Counter discontinuity, unreadable `cpu.stat`, monitor heartbeat loss,
   cgroup escape, failed `cgroup.kill`, missing `populated 0`, delayed VM-Off,
   or failed host request is **CONTAINMENT FAILURE**; evidence is rejected,
   the one-shot is consumed, and no retry is permitted.
2. `usage_usec` above 120 seconds consumes the proposed termination reserve.
3. `usage_usec > 130100000` or any workload CPU after confirmed VM-Off is
   **RESOURCE-BOUNDARY BREACH**. The run fails; no evidence can convert it to
   a pass.
4. A run ending below the CPU ceiling with all counters and timestamps
   complete is only **WITHIN MEASURED BUDGET**; it does not prove a universal
   maximum response time.

The only supported ways to close this blocker are to demonstrate a genuine
hard cumulative CPU enforcement mechanism in the fixed architecture, or for
the owner to explicitly consider the 130.1-second candidate plus its
termination assumptions and authorize a separate qualification budget. Owner
approval alone cannot make an unbounded stop operation enforceable.

## 6. Monotonic wall-time and two-stage termination

The host controller uses `QueryPerformanceCounter` as the authoritative
monotonic clock and records its frequency and raw ticks. `T0` is immediately
before it requests activation of the already-booted, preconfigured service.
This proposed scope includes systemd service start, supervisor bootstrap,
all three tests, guest cleanup, log flush/seal, workload-cgroup emptiness,
guest shutdown/forced-off, host evidence receipt and integrity verification.
VM boot, offline-source import and policy provisioning occur before `T0` and
must be separately bounded by qualification; they are not charged to the
corrective invocation. No pause, clock reset, second start or resumed
invocation is allowed.

At normal early completion, first verify the workload cgroup is empty and
seal the artifact ledger; request guest shutdown and allow at most five
seconds for confirmed VM Off. If not Off, issue one host `Stop-VM -TurnOff`
request. If that request errors or Off is not confirmed by the hard deadline,
classify the result as **TERMINATION FAILURE**, reject all results, consume
the marker and do not retry.

At the hard wall cutoff:

| Time from `T0` | Required action |
|---|---|
| `T0+170 s` | Guest monitor requests immediate workload `cgroup.kill`; begin recording raw request time. |
| `T0+171 s` | If `populated` is still nonzero, heartbeat is missing, or guest confirmation is unavailable, host watchdog issues `Stop-VM -TurnOff` immediately. No graceful-shutdown wait follows. |
| `T0+180 s` | Latest permitted confirmed VM-Off time and evidence-seal state. Any later/unknown state is a hard boundary breach. |

On early normal completion the same second-stage host control is used after
the five-second guest-shutdown opportunity. Host-side confirmation requires
the exact VM GUID to report `State=Off`, followed by a second independent
state query after at least one host scheduling turn; process/API return alone
is not sufficient.

**DOCUMENTED:** `Stop-VM -TurnOff` requests a power-off rather than a guest
shutdown. Microsoft documentation does not specify a maximum command or
VM-Off latency. QPC provides a monotonic counter, not a scheduling guarantee.
Failure of the host command, VMMS, watchdog, host, or evidence channel has no
demonstrated alternate path with a finite bound. A blocked host request does
not become safe because the output is rejected. The proposed 10-second wall
reserve and all stage timings remain unqualified; strict cessation by 180
seconds is unresolved.

## 7. Artifact boundary and POSIX compatibility proposal

### Exact measure

The proposed artifact measure is **aggregate per-invocation high-water logical
file length**, not allocated blocks and not byte-write volume:

- Total payload cap: **5,242,880 bytes**.
- Workload-writable allocation: **5,177,344 bytes**.
- Root-only failure-evidence reserve: **65,536 bytes**.
- At most **512 filesystem inodes total**, including workload files,
  directories, the preallocated root failure-reserve file, and bounded
  control files. Preflight must show at least 496 available artifact inodes
  after control files and mount points are provisioned; the failure reserve
  does not require a new inode when used.

For each regular-file inode, charge the highest logical `st_size` reached
during the invocation; sum those per-inode high-water sizes. Sparse holes
count as logical length. Credits are not returned after truncate/unlink, so
create-delete loops cannot recycle the artifact allowance. Rewrites within an
already charged length do not increase it. Hard links, writable `mmap`,
`fallocate`, reflinks and unrecognized file operations are denied. `rename`
preserves the inode charge; cross-boundary links and paths are rejected.
Directories/inodes are separately limited by the 512-inode cap. Filesystem
metadata, journals and allocation structures are outside the 5 MiB logical
payload count, but must fit inside the fixed backing-volume limit below.

All stdout/stderr, JSONL traces, test-generated temporary fixtures, retained
failure records and export-staging files are in this accounting domain.
Failure records use the separate 65,536-byte reserve and cannot consume
workload allowance. If a record cannot be appended, the host marks evidence
incomplete and rejects the run.

### Candidate filesystem and write-path controls

Use one fixed-size, host-ACL-protected **32 MiB VHDX** formatted with a
preconfigured ext4 filesystem for the artifact store, with 4 KiB blocks,
exactly 512 total inodes and a preallocated 4 MiB journal. Pin the filesystem
image hash and UUID before invocation. Preflight must verify exact VHDX length,
filesystem parameters, journal size, all control-file allocations, at least
6,291,456 bytes of available filesystem data blocks after provisioning, and
at least 496 available artifact inodes. These are proposed acceptance
thresholds, not verified fit; reject the image if any value is unmet. The
fixed backing capacity bounds physical filesystem metadata and allocated
blocks independently from the 5 MiB logical artifact cap; the 32 MiB backing
capacity is not an enlargement of the artifact allowance.

The 65,536-byte failure reserve is one preallocated root-owned file, counted
inside both the byte and 512-inode totals. It is not mounted or descriptor-
passed into the workload namespace. The trusted guest monitor receives one
pre-opened append-only descriptor to this file; its writes use a separate
fixed-capacity reserve counter and do not depend on the workload FUSE ledger.
The workload cannot access that descriptor or file path. At most one guest
failure record of at most 65,536 bytes is retained per failed invocation; the
workload allowance cannot be borrowed. Host-side Q10-Q12 records use the
separately budgeted host evidence volume. If the guest reserve is unavailable
or full, the host records incomplete evidence and rejects the run.

A root-managed FUSE daemon presents a single POSIX namespace, enforces the
aggregate ledger for all create/write/truncate/rename operations, and rejects
unsupported operations instead of falling back. The daemon and its backing
volume are outside workload write permissions. Both remain unimplemented
and unqualified.

For each size-increasing `write`, `pwrite`, or `truncate`, the FUSE daemon
serializes the request and durably reserves the resulting logical high-water
credit before modifying backing data. A request that would cross the
allowance returns `ENOSPC` before the backing file or ledger is changed.
Previously accepted requests in a multi-request `writeFile()` may remain;
the frozen corrective invocation fails on any unexpected `ENOSPC`, consumes
its one-shot marker and does not retry or resume. Qualification-only Q08 may
catch the intentionally induced `ENOSPC` to verify that the over-cap request
was rejected without changing file length or ledger. Each successful
filesystem write request is charged against the resulting observed `st_size`;
the prefix accepted by earlier requests in `writeFile()` therefore charges
exactly its resulting logical file length. A short return or ambiguous
backing-store error fails the invocation and retains the entire pre-reserved
candidate charge.

The proposed bounded ledger uses fixed per-inode records and a write-ahead
reservation: reserve and flush the candidate high-water value, perform the
backing operation, then commit the observed size. A full successful operation
is charged to the resulting file size. If a request returns short, the
backing store errors after possible partial modification, or a crash leaves
an uncommitted reservation, retain the larger reserved charge, classify the
invocation as failed, prohibit restart/reuse, and mount read-only for
evidence recovery. Refund credit only when the daemon can prove the backing
operation was not issued; any uncertain result after a backing operation
retains the reservation. A malformed, torn or unreconciled ledger fails admission;
never initialize a fresh ledger for the same one-shot identity. The fixed
record layout, flush ordering, crash recovery and filesystem image sizing are
not implemented or qualified and remain blocking requirements. Unsupported
operations return `EOPNOTSUPP`; inconsistency returns `EIO` and fails closed.

Place the workload in a private mount namespace with a read-only root and
read-only source tree. Bind only the FUSE namespace as the writable location
for `TMPDIR`, `/tmp`, `/var/tmp`, logs, traces and output. Redirect stdout and
stderr to pre-opened files on that namespace. `/dev/shm`, `/run`, caches,
home, repository, host shares, archive VHDX and all other paths are
read-only, absent, or non-writable. Use `NoNewPrivileges=yes`, no Linux
capabilities, no writable cgroup filesystem, no mount/namespace privilege,
no writable inherited descriptors other than the mediated artifact handles,
and no network. Validate mount propagation, `/proc` access, device nodes,
open-but-unlinked files and every inherited descriptor before dispatch.
The systemd service has no socket activation, FD store or passed descriptors;
standard input is `/dev/null`, stdout/stderr are pre-opened FUSE files. A
root-owned admission wrapper verifies mount IDs and closes every descriptor
above 2 before the single `execve`, permitting only the three declared
standard descriptors into the workload. No child is forked between close
and exec. The monitor verifies inherited descriptors before exec and, after
exec, permits only descriptors whose writable target is the mediated FUSE
mount; normal later opens inside that mount are expected. The post-exec
check is anomaly detection, not primary enforcement. New opens remain
confined by the private mount namespace, read-only/absent paths and lack of
capabilities. Any writable descriptor targeting another mount or namespace
escape is a one-shot failure.

The FUSE daemon must account at the filesystem operation boundary, not by a
post-run `du`. Node's frozen `mkdtemp(os.tmpdir())` and `writeFile()` usage
must remain valid without changing the tests. Direct POSIX writes go to the
FUSE mount; temp fixtures count against the same monotonic high-water ledger.
`lseek()` alone changes only the file offset and consumes no credit; a later
write extending `st_size` is charged for the entire resulting logical length,
including sparse holes. A single sparse write or `ftruncate()` that would
cross the limit is rejected as one operation, with unchanged `st_size` and
ledger. Q07/Q08 must exercise `lseek` followed by a one-byte write at the
limit, direct over-limit `ftruncate`, a bounded partial `writeFile()` followed
by expected `ENOSPC`, and readback of both resulting file length and ledger.
Node `writeFile()` does not receive whole-call transactionality: Q08 may
observe an accepted prefix, but the accounting must equal that prefix's
logical file size and the test must not retry or resume it.
The second and third corrective tests' filesystem behavior is not yet
qualified and must be statically inspected before any future qualification
freeze. Q01-Q12 use only synthetic helpers and probes; they do not import,
invoke, or reproduce the corrective test commands. The static source review
is a separate read-only prerequisite and does not consume any test allowance.

After confirmed VM-Off, detach the artifact VHDX and expose it read-only to
the host; verify the ledger, image identity, content manifest and hashes
without an unbounded duplicate copy. Any host-side evidence/control records
must use the protected reserve or the separately budgeted qualification
evidence allocation, and their bytes are included in the applicable cap.
There is no writeable host share in the workload namespace.

This logical high-water rule, 512-inode sublimit, FUSE mediation and fixed
volume are proposals, not the original artifact metric. They require explicit
owner approval and compatibility qualification. If a vetted FUSE mediator
cannot preserve all three frozen tests' POSIX behavior while enforcing the
ledger, no substitute `df`, project-quota, tmpfs-size or post-run measurement
is accepted as equivalent. The owner must then decide whether to amend the
artifact metric to a specific allocated-block policy or request a separately
reviewed test-interface change. No such amendment is made here.

## 8. Separate proposed A6 qualification allowance

A5's ten-case / 180 guest CPU-second / 600 wall-second proposal remains
historical, unapproved evidence. The following is a separate and complete A6
proposal, not approved and not executable:

| Resource | Proposed hard ceiling / scope |
|---|---|
| Invocation / retry | One host-led invocation, one VM start, at most one host `Stop-VM -TurnOff`, zero retries or reruns; durable A6-only marker consumed before start. |
| Cases | Exactly Q01-Q12 below, in order, one pass each; abort on first failure except the planned final Q10-Q12 shutdown/evidence sequence. |
| Guest CPU | 240 aggregate `usage_usec` CPU seconds across the qualification cgroup; one effective guest CPU. Monitor is inside the outer qualification cgroup. This proposed ceiling includes every guest qualification process, but not host controller CPU. |
| Wall | 600 seconds from the host-QPC admission immediately before the single VM start through confirmed VM Off and final evidence-hash verification; boot and cleanup included. No pause or reset. |
| Guest memory | Outer qualification cgroup `memory.max=805306368` bytes (768 MiB), `memory.swap.max=0`; inner memory case `memory.max=536870912` bytes. No Windows-working-set equivalence. |
| Tasks | Outer qualification subtree at most 80 tasks/threads; any test leaf at most 64. |
| Artifacts | At most 6,291,456 payload bytes total: 5,242,880-byte logical-high-water test volume plus 1,048,576 bytes for retained host/guest qualification evidence. Fixed 32 MiB test backing VHDX and 16 MiB bounded host evidence volume; metadata is separately physically bounded. |
| Other | One CPU; no network/GPU/scientific records; no corrective source writable; no original corrective test invocation; no more than 12 synthetic qualification cases. |

This is only a proposed resource envelope for a possible later, separately
authorized qualification request. It cannot be partially consumed, tested,
reserved, or used to implement qualification infrastructure under A6. A6
governance review is intentionally performed before owner policy approval;
owner approval would be required before a future qualification request, and
that request would require its own independent review and explicit execution
authorization.

| Case | Exact identity and single-run acceptance condition |
|---|---|
| Q01 | `A6-Q01-ADMISSION-POLICY`: before dispatch, bind VM GUID/name; verify offline networking, integration-service state, a selected and authenticated non-network control/evidence channel, an exact read-only source-image manifest containing only allowlisted corrective inputs and no Luna-63C paths/artifacts, service lock, monitor, unit/cgroup ancestors, exact memory/swap/task/CPU limits, mount namespace, artifact image and one-shot marker. Any mismatch blocks dispatch and consumes the marker. |
| Q02 | `A6-Q02-DESCENDANT-INHERITANCE`: launch a benign three-generation process tree; verify every PID remains in the workload cgroup with effective limits and all tasks disappear after cgroup kill. |
| Q03 | `A6-Q03-MEMORY-MAX-OOM`: verify exactly 536870912 bytes; run one allocator helper that allocates and touches memory in bounded 16 MiB increments within the 512 MiB leaf until cgroup OOM terminates the `MemoryOOMGroup=yes` leaf. Require `memory.events` `oom` and `oom_kill` increments, no outer-cgroup or guest-global OOM evidence, `populated=0`, and preserved failure evidence. Capture before/after `memory.max`, `memory.peak`, `memory.events`, `memory.events.local`, `memory.stat`, and swap counters. Any host/guest-wide pressure event, unexplained termination, or inability to retain evidence fails and stops qualification. |
| Q04 | `A6-Q04-SWAP-ZERO`: inspect unit property, `memory.swap.max`, `memory.swap.current`, guest swap configuration and applicable zswap state; reject any nonzero workload swap charge or policy mismatch. |
| Q05 | `A6-Q05-AGGREGATE-CPU-CUTOFF`: execute one fixed CPU-bound synthetic helper; verify the dedicated parent-slice `usage_usec` reaches the 120-second trigger, monitor requests workload `cgroup.kill`, and the workload leaf reaches `populated=0` within one second. On this normal pass path the **VM remains Running** so ordered cases can continue; the Q05 criterion is not VM-Off. If the leaf remains populated, the host issues the one allowed TurnOff request, requires VM `State=Off` within nine seconds, and aborts all remaining cases. The final parent-slice usage must not exceed 130100000 usec. This is a probe, not a corrective test. |
| Q06 | `A6-Q06-WALL-TWO-STAGE`: execute one bounded synthetic sleeper. At its own `case T0+170s`, request workload cgroup kill; require `populated=0` by `case T0+171s`. The normal pass path keeps the VM Running for later cases. If the leaf is still populated, heartbeat is stale, or guest confirmation is unavailable at `case T0+171s`, issue the one allowed host TurnOff, require VM `State=Off` by `case T0+180s`, and abort all remaining cases. Record all QPC stage timestamps. |
| Q07 | `A6-Q07-LOGICAL-ARTIFACT-CAP`: write to exactly the ordinary allowance, then attempt one additional logical byte; mediator must reject the excess without crossing 5,177,344 workload bytes, while the protected reserve remains available. |
| Q08 | `A6-Q08-ALTERNATE-AND-SPARSE-PATHS`: probe sparse extension by `lseek` then a one-byte `write` at the cap, direct over-cap `ftruncate`, rename, hardlink, `/tmp`, `/var/tmp`, `/dev/shm`, `/run`, open descriptors and absent paths; every writable operation must reach the same ledger or fail closed. Attempt one bounded `writeFile()` crossing the cap and require `ENOSPC`, accurate accepted-prefix accounting, no orphaned ledger credit, unchanged file size/ledger for the rejected request, and no retry/resume. |
| Q09 | `A6-Q09-FAILURE-RESERVE`: exhaust workload allowance, then append a fixed bounded failure record through the trusted path; verify the 65,536-byte reserve and total 5,242,880 cap. |
| Q10 | `A6-Q10-MONITOR-SUPERVISOR-FAILURE`: inject one monitor failure while a benign sleeper is live. Host watchdog must declare its authenticated heartbeat stale no later than the 250 ms target and immediately issue the one permitted `Stop-VM -TurnOff`; no guest monitor action is assumed after failure. |
| Q11 | `A6-Q11-HOST-EMERGENCY-OFF`: pair with Q10; verify the single TurnOff request was bound to the VM GUID, record command result and QPC state transitions, and require two independent host observations of VM `State=Off` within nine seconds of the request. |
| Q12 | `A6-Q12-ONE-SHOT-EVIDENCE-INTEGRITY`: after VM Off, replay the same admission identity and verify start is denied; verify all counter snapshots, monitor records, reserve, image identity and exported hashes; no second VM start. |

Per-case maximum CPU/wall ceilings are: Q01 10/30 s, Q02 10/30 s,
Q03 15/30 s, Q04 5/20 s, Q05 130.1/150 s, Q06 5/180 s, Q07 10/30 s,
Q08 10/30 s, Q09 5/20 s, Q10 10/30 s, Q11 10/30 s, and Q12 5/20 s.
Their CPU ceilings total **225.1 seconds**; the remaining 14.9 seconds of the
240-second aggregate budget are unallocated reserve and cannot be spent on
extra probes. The sequential wall ceilings total **600 seconds**, including
the Q06 180-second probe and Q10-Q12 final shutdown/evidence sequence.
Qualification fails on any per-case or aggregate limit, and there is no
retry. These limits are themselves proposals; they do not create a safe
execution environment until the independent review and explicit owner
decision gate are passed. The per-case wall figures are maxima, not
allocations: their sum equals the aggregate 600-second wall ceiling, which
also includes VM start, so startup and evidence time necessarily reduce the
time available under one or more case maxima.

## 9. Required owner decisions, review and verdict

Before any future qualification request, the owner must explicitly decide:

1. Whether to replace Windows working set with the exact Linux
   `memory.max=536870912`, `memory.swap.max=0`, OOM/event policy and
   descendant scope in Section 4.
2. Whether the existing 120 CPU-second work allowance may become 120 work
   seconds plus a 10.1-second termination reserve, with a 130.1-second
   absolute proposed ceiling, including guest monitor/FUSE CPU after the
   baseline and excluding host controller/evidence-collector CPU; or require
   the original strict 120-second total.
3. Whether the 180-second wall clock starts at service admission on an
   already-booted VM, includes workload startup/cleanup/export, and requires
   confirmed VM Off by `T0+180s`, with the proposed `170/171/180` stages.
4. Whether the artifact cap means the exact per-invocation logical-file
   high-water ledger and inode/backing-volume controls in Section 7, and
   whether FUSE infrastructure and the fixed VHDX are permitted.
5. Whether the separate A6 qualification budget (12 cases, 240 guest CPU
   seconds, 600 wall seconds, 768 MiB outer memory, 6 MiB payload/evidence
   and no retries) may be submitted for independent prereview. This is not
   approval to execute it.
6. Whether enabling cpuset through systemd ancestors, creating the FUSE
   service/volume, and provisioning an independent host watchdog/control
   channel are permissible infrastructure changes.

These six owner decisions are not prerequisites to reviewing or publishing
this A6 governance proposal. They are prerequisites to requesting any future
qualification. Rejection or silence leaves the existing original policy in
force and no execution authority is created.

Independent reviewers covered: (A) CPU/wall accounting, termination stages,
margin and failure; (B) FUSE/artifact semantics, write-path completeness and
frozen test compatibility; and (C) memory semantics, owner-approval
boundaries, frozen protocol and Luna-63C isolation. Their reports and
Luna-0's integration are recorded in the A6 integrated review handoff. The
artifact reviewer also performed a narrow delta review; its final minor
clarifications were incorporated by Luna-0 but were not separately rerun
through reviewers. All reviewers distinguish documented facts, owner reports,
analysis and untested behavior.

**Integrated disposition: BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE.**

The retained architecture is the only candidate considered. The CPU margin
is explicit but its termination-envelope premise is not independently
established; Windows QPC, guest polling, cgroup kill and Hyper-V TurnOff do
not have a demonstrated worst-case completion bound in supplied evidence.
The required authenticated guest-host heartbeat/control/evidence transport
is not identified, with the owner-reported guest network and Guest Service
Interface unavailable.
The exact artifact ledger requires a FUSE implementation that is not present
or tested, crash recovery and image sizing are unqualified, and compatibility
with frozen test filesystem behavior is unverified.
The Linux memory metric and all budget changes also require explicit owner
approval. These are primarily **unavailable enforcement evidence and
unresolved owner-policy choices**, not a demonstrated impossibility of
engineering such controls.

The smallest next decision is the owner's explicit response to the six
resource/infrastructure items above. A policy approval can authorize only a
later qualification proposal; it cannot certify response bounds or authorize
qualification, corrective execution, scientific rerun, architecture
promotion, or Luna-63C work. No A7 is opened by this blocked outcome.

## References

- Linux kernel, cgroup v2: <https://docs.kernel.org/admin-guide/cgroup-v2.html>
- systemd 259 resource control: <https://www.freedesktop.org/software/systemd/man/259/systemd.resource-control.html>
- Microsoft Hyper-V `Stop-VM`: <https://learn.microsoft.com/en-us/powershell/module/hyper-v/stop-vm?view=windowsserver2025-ps>
- Linux FUSE overview: <https://www.kernel.org/doc/html/latest/filesystems/fuse/fuse.html>
