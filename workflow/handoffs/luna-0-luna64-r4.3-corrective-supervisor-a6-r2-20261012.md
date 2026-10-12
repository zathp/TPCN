# Luna-0 — Luna-64 A6 R2 Enforcement Design Closure

- **Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6-R2`
- **Disposition:** **BLOCKED — ENFORCEMENT DESIGN INCOMPLETE**
**Scope:** Governance-only design and independent prereview. No infrastructure was changed, installed, started, or tested. No supervisor qualification, corrective test, or scientific workload was run.

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-64 A6 R2 enforcement design closure"
  task_id: "L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6-R2"
  component: "Experimental execution governance"
  status: "blocked"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "f1cfb6e98cfc872753ea262bdb56e4a66ab40c05"
  dependencies:
    - "Frozen R4.3 protocol and original corrective owner authorization"
    - "Published A1-A5 blocked findings and A6 technical block"
    - "Published A6 owner-policy reconciliation R1 and review"
    - "Owner decisions D1-D6 as recorded by R1"
  classification:
    - "GOVERNANCE ONLY"
    - "DESIGN AND INDEPENDENT PREREVIEW ONLY"
    - "NO INFRASTRUCTURE CHANGE AUTHORITY"
    - "NO QUALIFICATION EXECUTION AUTHORITY"
    - "NO CORRECTIVE OR SCIENTIFIC EXECUTION AUTHORITY"
  authorized_scope:
    - "Read-only baseline and provenance verification"
    - "Design analysis of authenticated offline control, artifacts, CPU, wall time, and qualification budget"
    - "Independent review A-D"
    - "Governance publication of this blocked design and findings"
  unauthorized_scope:
    - "Installing or configuring a virtual COM channel, service, job object, filesystem, quota, or supervisor"
    - "Starting or operating the Hyper-V VM"
    - "Running any qualification case"
    - "Resuming corrective implementation or tests"
    - "Running a scientific workload or using Luna-63C material"
  architecture_change: false
  execution_authorized: false
```

## 1. Authority, predecessor identities, and result boundary

R2 is a design-only successor to R1. It does not amend or reopen the frozen
scientific specification, original owner authorization, accepted reject-only
malformed second-origin policy, or any prior verdict.

| Evidence | Verified identity / retained status |
|---|---|
| R4.3 content freeze / governance closure | `64a214e310de3b982b90a8ad215598bc1e9f8b1c` / `ea1b10456cbf4ca726e473076d239a4f6e53b9c7` |
| Frozen R4.3 manifest | SHA-256 `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B` |
| Original corrective authorization | `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`; implementation authority remains unused |
| A1 | `d20aab249e42575ccc571c9c72153a3bb4b412db`; prior supervisor amendment **BLOCKED** |
| A2 | `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c`; prior supervisor amendment **BLOCKED** |
| A3 | `8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0`; prior execution-environment gate **BLOCKED** |
| A4 package / closure | `7bd440565c38dee81ace3606fde3fb686de6a0ef` / `f86c25844a4863ac57cd6634f364c28bcf2f511f`; **BLOCKED** |
| A5 package / closure | `12f84a41fe7c91c17c5df8e975fce24efbadf9ad` / `b758b411e568b41c516228e7d3bdff26058114cc`; **BLOCKED — A5 QUALIFICATION INCOMPLETE** |
| A5 proposal / review | SHA-256 `5BCDAC72E7EBDEA777E9964F25554834C4460D97075E6871690BD441BA00C6E5` / `54D11A362EDED451292330C6FA5627B570BD6103ADE0F69E115F5CDC3C7B934D` |
| A6 proposal / environment evidence / independent review | SHA-256 `AD952D9AB7656313D03E0E58BF48469D420B74C5E9CB6BA6738915AA0D34C4C4` / `CB4FA2BBB72DFD1371312641A101F3F5E77A1BDF99540521EE366069AED0C7AE` / `500611264036C1602D280294030F1459FFA817C8DB1CE64AE4E1F4F8E28DB405` |
| R1 package / closure | `f00dea13d64657cbc976d21daf50739ddf9722fe` / `f1cfb6e98cfc872753ea262bdb56e4a66ab40c05` |
| R1 proposal / review / manifest | SHA-256 `A619E3A4361B712471B8C3A7FD2AA784992ED6B4F5F0E218ED0449B16144319D` / `DD7E0F840F8C3F34A7016351C28F63CA50F313618DC1B218B81A509CBD8E4D36` / `D51C207C5ED7E91B59C661FB39B67E88F27C0FA47CDEF708AA1F0ADFB7DEE958` |

The working branch was `governance/luna64-r4.3-freeze-20261010` at R1
closure `f1cfb6e98cfc872753ea262bdb56e4a66ab40c05`; it was clean and the
remote branch resolved to the same commit before R2 changes. All R1 source
checkout hashes above were re-computed and matched. A5/A4/A1-A3 blocked
findings, the original pilot verdict **NOT SUPPORTED AS A
PROTOCOL-COMPLIANT PILOT** (not an efficacy result), the unused corrective
allowance, and Luna-63C isolation are preserved.

R1 owner decisions D1-D6 remain exactly as recorded. In particular, the
130.1 CPU-second and 170/171/180-second stages are unverified targets;
the proposed qualification budget is planning-only; and D6 authorizes no
infrastructure changes. R2 proposes semantics for previously unspecified
budget fields; none of those proposed metric changes has owner approval.

Evidence labels used below:

- **VERIFIED—REPOSITORY:** Git object, ancestry, checkout-hash, and worktree
  checks performed for this publication.
- **OWNER-SUPPLIED:** platform diagnostics recorded by R1; not re-executed.
- **DOCUMENTED / ANALYTICAL:** behavior inferred from referenced interfaces;
  not an enforcement test on this VM.
- **PROPOSED / UNQUALIFIED:** design choices requiring review, owner decision,
  implementation authorization, and qualification.

## 2. Authenticated offline host–guest control

### 2.1 Candidate comparison

| Candidate | Control/authentication properties | R2 assessment |
|---|---|---|
| Host Hyper-V management plus guest-local monitor, no guest channel | Host can inspect VM state and request `TurnOff`; guest-local cgroup monitor can stop the workload. No authenticated heartbeat, command acknowledgement, or guest evidence reaches the host. | Insufficient for the required evidence and prompt guest-stop coordination. |
| Hyper-V sockets | Potential non-network transport, but availability for this Windows 10 / Ubuntu guest, endpoint ACLs, peer identity, and message security have not been verified. | Not selected; feature availability alone is not proof. |
| Host-controlled virtual COM port connected to a local named pipe | Hyper-V documents binding a VM COM port to a local named pipe. Windows pipe ACLs can restrict the endpoint to the dedicated host service SID and SYSTEM. This is a byte transport, not an authentication protocol. | **Selected design candidate**, conditional on owner authorization and qualification of the exact VM/COM-port/pipe configuration. |
| Verified virtual media, one-way transfer | Read-only guest input media can carry pre-provisioned configuration; writable evidence media can carry sealed output after VM Off. It cannot promptly deliver a stop request or heartbeat. | Use only for provisioning or offline export if separately authorized; not the live control path. |

The controlling proposal is one virtual COM port attached only to VM GUID
`60e9baef-706e-4490-80d7-38618710546e`, terminating at a host-local named
pipe. The Hyper-V host controller creates/owns the pipe with a restrictive
ACL; the VM-to-pipe mapping is configured from the host. The Ubuntu guest
uses a root-owned serial client. Guest networking remains disconnected.
The host does not expose a general shell, RPC, or arbitrary command channel.

### 2.2 Authentication, authorization, and failure protocol

The host and the unique read-only guest image are provisioned with the same
random 256-bit one-shot key. It is never sent over the serial channel and is
readable inside the guest only by the root monitor. The host secret is
revoked after the run; the VM/image identity is retired and never booted
again. The design does not claim secure erasure of a key from a VHDX or
support key rotation within a read-only image. Reusing/cloning the image is
prohibited. Guest root, kernel, and monitor are trusted; compromise of any
defeats guest-side authentication.

Wire framing is fixed and versioned: a 4-byte big-endian frame length,
followed by a fixed-width header (`magic[8]`, `version:u16be`,
`run_id[16]`, `session_id[32]`, `vm_guid[16]` in RFC 4122 byte order,
`direction:u8`, `sequence:u64be`, `type:u16be`, `payload_length:u32be`),
the payload, and a 32-byte HMAC-SHA-256. The MAC covers the exact header and
payload bytes; the length prefix is validated before allocation and is
bounded at 4 KiB. Payloads use fixed schemas per message type, not
free-form text. The host creates `run_id` and a cryptographically random
256-bit challenge. It sends `HELLO` with the challenge and a host-direction
MAC. The guest verifies it and returns `AUTH` with HMAC over the protocol
domain string, run ID, VM GUID, challenge, and guest direction. The host
verifies the response. `session_id` is
`SHA-256("TPCN-L64-A6-R2" || run_id || vm_guid || challenge)`. Sequence
counters start at 1 after handshake, increase independently in each
direction, and are persisted by the host. Any duplicate, gap, reordering,
malformed frame, bad MAC, or reconnect invalidates the session; there is no
counter reset or resume.

Each subsequent frame MAC covers the full versioned header and payload.
Replayed/stale frames, wrong run/session/GUID, and unauthenticated content are
rejected and logged. Host commands are limited to an enumerated operation
(`START_CASE`, `KILL_CGROUP`, `SEAL`, `SHUTDOWN`, or status challenge) plus a
case identifier; no frame contains executable text, a path, or a free-form
command. The host authorizes only the fixed qualification state machine and
only the exact VM GUID.

Host authorization relies on the dedicated Windows service identity,
named-pipe ACL, and an exclusive pipe-path mapping verified against all
configured VM COM ports before admission. The one-shot guest image key
authenticates the root monitor; it is not hardware attestation. An asserted
GUID alone is not proof of the VM peer. This design relies on the host being
trusted to ensure that only the approved VM is mapped to the pipe and that
the unique keyed image is not cloned. HMAC supplies integrity and peer-key
proof, but no confidentiality and no protection after either endpoint is
compromised. The consumed qualification ID and retired image reject
subsequent sessions.

The host QPC watchdog and Hyper-V management API are independent of the
guest channel. If the pipe disconnects, authentication fails, or the
heartbeat is stale for 250 ms, the host marks the attempt failed, sends no
further workload commands, records raw timestamps, and requests
`Stop-VM -TurnOff` for the exact GUID at the next watchdog action. The
guest-local monitor independently requests `cgroup.kill` when its own local
deadline or monitor fault requires it. Loss of the guest channel never
removes host turn-off authority. An API success return is not Off
confirmation; two host state reads of the exact VM ID must report `Off`.
The host controller issues the one permitted TurnOff request asynchronously
so the QPC watchdog can continue state polling while the API call is pending.
If the call errors, remains pending at the deadline, or Off is not confirmed,
no duplicate request is sent; the attempt fails and no VM restart follows.

If the host controller/watchdog itself crashes, hangs, or is starved, the
design cannot guarantee a timely Off request. The attempt is a termination
failure; the host service manager or administrator may observe and manually
issue the single emergency TurnOff only if no request has already been made,
but neither recovery nor completion latency is guaranteed. No autonomous
fallback beyond the trusted host OS, Hyper-V/VMMS, and controller is claimed.

**Unverified assumptions:** a Windows 10 Pro host can create and ACL the
selected local named pipe for the Hyper-V COM connection in the intended
service context; Ubuntu's guest sees and can exclusively open the configured
serial port; the OS/Hyper-V stack preserves the mapping to the stated VM; and
the message client can meet its intended heartbeat/latency behavior. The
owner diagnostics did not establish any of these. The named-pipe COM feature
is documented, but not its security for this deployment. These assumptions
are qualification gates, not verified capabilities.

### 2.3 Trusted computing base and influence

| Component | Trust / influence |
|---|---|
| Windows host kernel, administrator, Hyper-V/VMMS, named-pipe ACL, QPC watchdog, and exact-VM host controller | Trusted. Workload cannot write host state or invoke host APIs. Host compromise defeats containment and is outside the qualification claim. |
| Ubuntu guest kernel, systemd PID 1, root provisioner, root monitor, serial client, and artifact quota configuration | Trusted. Workload receives no root, capabilities, device access, cgroup delegation, mount authority, or monitor credentials. Guest-root/kernel compromise is outside the workload threat model. |
| HMAC protocol and per-run key | Trusted implementation and secret material; generated and protected before execution. Key secrecy from guest root is not claimed. |
| Corrective tests, synthetic cases, workload UID, and every descendant | Untrusted. Can emit arbitrary bytes, create files through permitted paths, fork within bounded resources, and attempt alternate paths. |
| Hyper-V serial device, pipe transport, and guest configuration | Trusted only after exact identity/configuration checks and qualification. Device presence alone conveys no authentication. |

## 3. Artifact containment decision

### 3.1 Alternatives

| Mechanism | Strength | Limitation for frozen direct temporary writes |
|---|---|---|
| Fixed-size ext4 image alone | Hard upper bound on image capacity; durable after VM Off. | Bounds allocated filesystem storage, not aggregate logical high-water file lengths. Image metadata consumes capacity. |
| Bounded `tmpfs` | Can bind `/tmp` and other temporary roots into a size-limited namespace; volatile and simple. | Size constrains allocated pages, not aggregate logical high-water bytes; sparse files and metadata semantics differ, it consumes guest memory, and failure evidence is not durable. |
| Project quotas | Hard per-project allocated-block and inode ceilings on a supporting filesystem. | Not an aggregate logical-length ledger; sparse files can have large logical sizes with little allocated storage; block and metadata accounting must be qualified. |
| Read-only mount namespace plus limited writable mounts | Prevents writes to the source/root and centralizes writable paths; no workload mount capability. | Does not cap writes to the permitted mount; does not revoke an already-open descriptor outside the namespace by itself. |
| Per-process `RLIMIT_FSIZE` | Can constrain an individual file's maximum size. | Not aggregate across multiple files/descendants; not the frozen logical high-water policy. |
| Post-run scan | Detects some final-state overages. | Not hard enforcement; cannot recover deleted, truncated, sparse, or transient high-water outputs. |

**Selected design candidate:** a preallocated fixed-size 32 MiB ext4 output
image with project quotas and inode limits, combined with a private
read-only-root mount namespace. A single ext4 project is applied to all workload-visible output
and temporary directories; a second, root-only project reserves failure
evidence. Host evidence is written by a dedicated low-privilege local
account, with a separate account for the root-equivalent emergency recorder;
each account's file-owner SID has an NTFS hard quota. Both the ext4 image
size and NTFS quotas are proposals; no filesystem is created or mounted.
This is the simplest plausible
allocated-storage design, not an installed or qualified control, and not a
substitute already approved by the owner.

### 3.2 Paths and write controls

Source inspection of the R4 test suite found a direct temp-path writer in
`experiments/luna64/test-track-b-gate-r4.mjs`: it calls
`mkdtemp(path.join(os.tmpdir(), ...))` and writes CLI fixtures beneath that
directory. Its protocol/schema/golden inputs are resolved from the source
tree and must remain read-only. Therefore the eventual launcher must set
`TMPDIR`, `TMP`, and `TEMP` before Node starts, verify `os.tmpdir()` resolves
inside the artifact project, and use a read-only working/source tree. The
schema generator writes its schema beside the source; it is not permitted in
qualification. This source check is not an exhaustive inventory of the
future corrective child-test commands, which must be enumerated before any
execution.

The proposed guest namespace is:

- Source tree and runtime image: read-only bind mounts.
- `/tmp`, `/var/tmp`, `/dev/shm`, `TMPDIR`, `TMP`, and `TEMP`: all redirected
  or bind-mounted to the same quota-controlled workload project.
- stdout, stderr, JSONL traces, generated fixtures, test temporary files,
  failure output, and export staging: paths beneath that workload project.
- A separate root-only path in the failure-evidence project: only the
  supervisor/monitor may write there; workload UID cannot traverse or open it.
- Every other filesystem mount read-only or absent; no host shares, network,
  writable home directory, writable `/run` path, device node, or alternate
  output mount is exposed to the workload.

The launcher must create the mount namespace before executing any test,
close unrelated inherited file descriptors, and start all descendants inside
the same namespace and cgroup. The workload has no `CAP_SYS_ADMIN`,
`CAP_DAC_OVERRIDE`, `CAP_FOWNER`, or cgroup write access. Symlinks are
resolved within the permitted namespace; the root-owned parent directories
are not writable, so the workload cannot replace the mount roots. Hard links
cannot cross the ext4 filesystem boundary; link creation is limited by
ordinary ownership and the same project quota. Existing descriptors are
limited to explicitly opened output handles and remain charged to the same
filesystem if inherited. Attempts to write through an outside directory FD,
device, `memfd`, alternate mount, or inherited host handle are denied or
treated as a failed containment case; the workload has no serial-device or
host-pipe handle. The synthetic alternate-path test must verify all path
resolution from the exact launcher working directory and effective
environment. `O_TMPFILE` on the quota volume remains charged as allocated
blocks; anonymous memory objects are denied to the extent supported by the
selected syscall policy, are not artifact files under the proposed metric,
and remain subject to the memory/cgroup limit.

The host evidence directory is writable only by a dedicated restricted local
account used as the primary file owner of the pre-created ordinary controller
log and final receipt. A separate restricted emergency-recorder account owns
one pre-created reserved evidence file. No new host evidence file may be
created during a run. Their exact SIDs, owner ACLs, quota assignments, and
file ownership must be read back; service-SID membership alone does not prove
NTFS quota charging. The host controller and emergency recorder cannot write
each other's evidence area. Host events and guest output are not counted
twice: guest files are counted by ext4 project allocation; host evidence is
counted by NTFS quota usage for the verified owner SIDs.

### 3.3 Accounting, sparse files, and failure evidence

The frozen R4.3 requirement is an aggregate **logical high-water file length**
of 5,242,880 bytes, counting sparse holes and bytes from unlinked or truncated
files that previously existed. No stock choice above enforces that aggregate
metric across all direct temporary-file writers without changing the frozen
tests or adding an accounting mediator. A fixed-size filesystem and project
quota charge allocation, not logical high-water bytes. `RLIMIT_FSIZE` is
per-file. Post-run scanning is too late. R2 therefore does **not** claim the
original 5 MiB logical cap is enforced.

The smallest stock-policy alternative proposed for owner decision is a
**maximum simultaneously allocated storage** policy. Project quotas enforce
current charged allocation, not cumulative bytes emitted or lifetime
high-water usage. Deleting/unlinking and freeing blocks makes quota space
available again; a workload may therefore write and delete more than 5 MiB
over time while remaining below the live-allocation cap. This proposal does
not claim to bound cumulative stdout, stderr, fixture churn, or total bytes
ever written. If the owner requires those lifetime totals, no stock control
described here is equivalent.

1. Replace the 5,242,880-byte aggregate logical high-water cap with a
   **5,242,880-byte peak sum of two ext4 project block-quota hard limits**,
   charged in exact 4,096-byte units: workload project 5,177,344 bytes
   (1,264 blocks), failure-evidence project 65,536 bytes (16 blocks).
   Their sum is 1,280 blocks / 5 MiB. `memory.max=536870912` continues to
   bound memory separately.
2. Set the workload project inode hard limit to 512 and the root-only
   failure-evidence project inode hard limit to 16. These limits, including
   directory/inode consumption, must be read back and exercised; the fixed
   32 MiB image separately bounds all filesystem metadata and journal
   consumption.
3. Apply a per-file `RLIMIT_FSIZE` of 5,242,880 bytes as defense in depth,
   not as proof of an aggregate logical cap. State plainly that many sparse
   files can still have aggregate logical lengths above 5 MiB while staying
   below the allocated-block quota.
4. Keep the ext4 image itself fixed-size so filesystem metadata, journal,
   quota files, and uncharged root metadata cannot grow without limit.

For the separate qualification allowance, propose 5 MiB of guest ext4
project-charged allocation plus 1 MiB of host NTFS per-owner quota usage,
for a policy sum of 6,291,456 bytes. Guest quota is split into 1,264
workload blocks and 16 failure-evidence blocks. Host quota usage is split
into 983,040 bytes for ordinary records and 65,536 bytes for emergency
evidence, charged to separate verified file-owner SIDs. The host value is
NTFS quota usage, not allocated blocks: NTFS quota treatment of sparse files
can charge nominal file size, so no physical-allocation equivalence is
claimed. Only the trusted host writers can create host evidence; sparse,
compressed, and additional-stream files are not permitted. Failure evidence
is included, not added on top. The fixed ext4 image capacity and filesystem
metadata are separately bounded and recorded; image capacity is not
represented as the artifact-byte metric. This mixed-metric sum and the
proposed 5 MiB policy change require independent review and explicit owner
approval.

Sparse holes count toward per-file logical size but not allocated blocks;
unlinked open files remain allocated and quota-charged until last close;
unlink/recreate does not reclaim quota until blocks are freed. Once blocks
are freed, quota can be reused; cumulative output volume is not bounded by
this proposed metric. Metadata and inode exhaustion produce explicit case
failure. In Q07, quota denial at the live-allocation limit is the expected
synthetic outcome; quota read failure, missing output, or inability to seal
reserved evidence fails qualification and stops the session. The protected
reserve is only useful if it remains inaccessible to the workload and the
filesystem has enough pre-reserved metadata/inodes; this must be demonstrated
in qualification. No evidence is permitted to grow beyond the aggregate
quota by writing to an alternate path.

The candidate policy does **not** satisfy the original logical high-water
definition and does not cap cumulative output volume. If the owner will not
approve this live allocated-storage metric, qualification and corrective
execution remain blocked unless a separately authorized mediator or
frozen-test change can provide exact aggregate high-water accounting.

## 4. Memory, cumulative CPU, and wall-time contracts

### 4.1 Memory policy retained from D1

The candidate remains:

```ini
MemoryAccounting=yes
MemoryMax=512M
MemorySwapMax=0
```

Before admission, read back `memory.max=536870912` and
`memory.swap.max=0` on the workload cgroup and all controlling ancestors.
Record `memory.current`, `memory.peak`, and `memory.events` (`max`, `oom`,
`oom_kill`, `oom_group_kill` where available) before and after each case.
Descendants count only while in the non-delegated workload subtree; all
process creation is confined there and cgroup migration is denied. Any
limit mismatch, cgroup escape, counter error, or unexplained discontinuity
fails the case. In actual corrective execution, any OOM event rejects the run.
In the synthetic Q04 case only, the expected OOM/limit event is a successful
qualification result if it kills the synthetic child, leaves the trusted
monitor intact, and is fully recorded; it is never workload success.

`MemorySwapMax=0` maps to `memory.swap.max=0`; it does not prove that every
form of memory overcommit is impossible. Inspect guest swap configuration,
`memory.swap.current`, and effective ancestors. This Linux charged-memory
metric is materially different from the original Windows aggregate peak
working-set metric and remains a material owner decision before
enforcement/qualification.

### 4.2 Cumulative CPU candidate

The aggregate qualification value is the baseline-subtracted delta in the
single, fresh, non-delegated qualification-parent
`cpu.stat:usage_usec`. It is cumulative aggregate user-plus-kernel CPU time
in microseconds. `user_usec` and `system_usec` are retained for
reconciliation; they are not added again to `usage_usec`. A trusted external
reader records the parent counter while the parent is empty and before any
guest monitor or workload admission. The guest monitor and each case's
supervisor/workload descendants run beneath this parent, so their CPU after
baseline is included. At each case boundary, the external reader samples the
same parent counter; the case delta is charged against that case's
reservation. The final value is read after the monitor and complete subtree
have exited, after `cgroup.events` reports `populated 0`, and before cgroup
removal. Host controller/watchdog CPU, VM boot/PID 1 activation, and host
VM-off CPU are excluded from this guest metric and must be separately
recorded.

The `130100000`-usec candidate belongs to a single corrective invocation,
not to the entire 12-case qualification. Q06 creates its own nested,
non-delegated accounting child containing the synthetic case monitor and
burner, with a case-local baseline sealed immediately before the monitor is
admitted. Q06 threshold decisions use only
`q06_usage_delta=current_q06_usage-baseline_q06_usage`. The qualification
parent remains continuous and is never reset; its delta still charges every
case, including Q06 monitor CPU, against the aggregate 240-second budget.
This separates the Q06 candidate reproduction from the session-wide
resource total without resetting or excluding CPU.

Candidate monitor procedure:

1. Root creates the qualification parent and case child cgroups with no
   process running; no process may delegate or write cgroup control files.
2. A trusted external reader seals the qualification-parent baseline,
   effective `cpuset.cpus.effective`, and `cpu.max` before launching the
   guest monitor. The parent counter is continuous through all 12 cases.
3. For Q06, create a separate nested accounting child and workload grandchild.
   Seal the Q06 child baseline before launching its monitor; place that
   monitor in the Q06 accounting child and the burner in its workload
   grandchild.
4. The Q06 monitor samples its accounting child's `cpu.stat` at a 100 ms
   target interval. `cpu.max=100000 100000` and a verified single effective
   CPU constrain the aggregate execution rate; this is not a lifetime CPU cap.
5. At `q06_usage_delta >= 120000000` usec, the Q06 monitor records the
   threshold and requests `cgroup.kill` on the burner grandchild. If it
   remains populated one second after the request, the host watchdog requests
   immediate `Stop-VM -TurnOff` for the exact VM.
6. The accepted R1 candidate is a Q06-local
   `q06_usage_delta=130100000` usec stop-and-fail target, not authorized
   overshoot and not the aggregate qualification threshold. Retain raw
   counters plus derived deltas, request, ack, and final counter values.
   At the first sample at or above `130100000` usec, the monitor records a
   candidate-boundary failure and immediately requests `cgroup.kill`; the
   host requests its single `Stop-VM -TurnOff` if no request has already
   been made. This response is an action-on-detection rule, not a guarantee
   that the candidate cannot be crossed between samples or before shutdown.
   Counter loss, late response, workload after completion, or any Q06 delta
   above the candidate invalidates the attempt.

Under the *assumed but unproved* response envelope, a one-CPU cap allows at
most approximately 0.1 CPU-second between samples, plus one second for
guest kill and nine seconds for host-Off, yielding the proposed 10.1-second
reserve over the original 120-second ceiling. There is no demonstrated upper
bound on scheduling delay, monitor starvation, cgroup kill completion,
serial delivery, host scheduling, VMMS/Hyper-V response, or confirmed VM
Off. Thus the 130.1-second value is not a mathematical lifetime guarantee.
Qualification can measure examples and identify failures; it cannot prove a
universal maximum. A strict 120-second hard ceiling is not established by
`cpu.max`, polling, or a successful test.

**CPU decision required:** preserve 130.1 seconds as a conditional candidate
with explicit acceptance of unbounded worst-case response, or require a
genuine hard lifetime CPU enforcement mechanism. The current design does not
claim that either is already accepted for execution. If the aggregate
qualification ceiling of 240 guest CPU seconds cannot itself be hard-enforced,
qualification must not start under that ceiling.

### 4.3 Wall-time contract

`QueryPerformanceCounter` (QPC) on the trusted Windows host is the proposed
monotonic source; record frequency and raw ticks. `Q0` starts immediately
before the single VM-start request and covers boot, admission, all 12 cases,
cleanup, evidence seal, and confirmed VM Off. No pause, reset, restart, or
retry is permitted. For an eventual corrective invocation, `T0` is recorded
immediately before the host requests activation of its workload service;
its bootstrap, tests, cleanup, and termination are included. Qualification
case clocks `Tcase` are separately recorded dispatch times within the single
Q0 interval; they do not redefine the future corrective `T0`.

Candidate stages, relative to `T0`:

| Time | Action |
|---|---|
| `T0 + 170 s` | Host QPC watchdog sends the authenticated `KILL_CGROUP` request; guest monitor requests `cgroup.kill` on the workload child and returns an authenticated acknowledgement. |
| `T0 + 171 s` | If the child is still populated, heartbeat is missing, or authenticated guest confirmation is unavailable, host immediately requests `Stop-VM -TurnOff` for the exact GUID. |
| `T0 + 180 s` | Proposed latest time for confirmed VM `Off` and sealed evidence. Any later or unknown state is a termination failure and boundary breach. |

During qualification, normally completed cases are sealed and the same VM
remains running for the next fixed case. No guest shutdown occurs before
Q11. After Q11's stop/turnoff test, case 12 is offline only. In a future
corrective invocation, normal early completion would verify the workload
subtree empty, seal guest output, request guest shutdown, and allow at most
five seconds for confirmed VM Off; otherwise the single host `TurnOff`
request is used. VM Off requires two independent host state reads of the
exact GUID reporting `Off`, with at least one host scheduling turn between
reads. A command/API return does not establish Off.

No finite worst-case completion time for guest kill, graceful shutdown,
`Stop-VM -TurnOff`, VMMS, host scheduling, or state observation has been
established. QPC is a clock, not a scheduling or power-off guarantee. If the
host control API errors, the watchdog does not observe Off by the proposed
deadline, or evidence is incomplete, classify **TERMINATION FAILURE**,
reject evidence, consume the one-shot, and do not retry. The R2 design does
not claim a hard 180-second termination bound.

**Wall decision required:** owner must choose whether the 170/171/180
numbers remain best-effort qualification targets with any late/unknown
termination an automatic failure, or whether execution requires a proved
hard stop mechanism. No owner approval can convert an unbounded API latency
into a guaranteed deadline.

## 5. Proposed qualification allowance and fixed case matrix

The D4 allowance remains a separate planning-only budget and does not consume
the unused corrective allowance:

| Resource | Proposed aggregate maximum |
|---|---:|
| Synthetic cases | 12, in the fixed order below |
| Guest qualification-parent CPU (`cpu.stat:usage_usec` delta) | 240 CPU seconds |
| Host QPC wall | 600 seconds from `Q0` to confirmed Off and evidence seal |
| Host control-plane private commit | 805,306,368 bytes (768 MiB), proposed split: controller job 738,197,504 bytes (704 MiB) plus watchdog job 67,108,864 bytes (64 MiB) |
| Guest artifact allocation | 5,242,880 bytes (5 MiB) peak ext4 project allocation in the fixed 32 MiB image |
| Host evidence quota usage | 1,048,576 bytes (1 MiB) NTFS hard quota usage charged to verified file-owner SIDs |
| Combined artifact/evidence accounting | 6,291,456 bytes (6 MiB) policy sum of guest peak project allocation and host quota usage; metrics are distinct and declared; failure evidence included |
| Hyper-V VM starts | 1 |
| Host `Stop-VM -TurnOff` requests | At most 1 |
| Retries, restarts, or replays | 0 |

The 768 MiB choice is a proposed **host control-plane committed-memory**
metric, not an aggregate Windows working-set cap and not a cap on host OS,
Hyper-V/VMMS, or the VM's fixed 8 GiB guest RAM. The two host Job Objects
would use `JOB_OBJECT_LIMIT_JOB_MEMORY`, with all descendants assigned before
execution and breakaway disabled; `PeakJobMemoryUsed` is evidence. The
separate hard limits sum exactly to 768 MiB, but do not bound excluded
processes. This replacement definition requires owner approval. Guest
`memory.max` remains a separate 512 MiB workload charge.

The host evidence allowance is split into a 983,040-byte ordinary-log owner
quota and a 65,536-byte emergency-evidence owner quota. They use distinct
restricted local accounts and verified file owner SIDs. Host output is
limited to pre-created, fixed-name log/receipt files; no guest process has a
host filesystem handle. Filesystem metadata,
NTFS journal/MFT allocation, and the guest ext4 image's fixed metadata are
bounded by their backing filesystems but are not part of the proposed
6 MiB policy sum. Any requirement that includes such
metadata needs a separately specified byte measure.

Case CPU and wall allocations are reservation ceilings. They are not
borrowable, cumulative maxima sum exactly to 240 CPU seconds and 600 wall
seconds, and an early case does not increase a later allocation. Q01's
60-second wall interval begins at Q0 and includes VM boot/admission; no
separate boot-time allowance exists. Every inter-case transition is charged
to the immediately active case interval. The actual hard aggregate CPU and
wall enforcement remains unproved; do not execute until a future
authorization resolves that gap.

`Q0` is the one host QPC start for the entire session. Each case has a
recorded monotonic `Tcase` at dispatch and no pause or retry; case wall
allocations are included in the single `Q0` total. The final timed case uses
its own `Tcase` for the 170/171/180 candidate stages. A single guest
accounting parent is sampled continuously; deltas at case boundaries include
guest bootstrap/monitor CPU after the baseline and are charged to that
case's allocation. The aggregate `usage_usec` delta from the sealed baseline
through the final empty-parent sample must be no more than 240 seconds.
VM boot and PID 1 activation CPU are outside this D4 metric but must be
recorded separately as R1 requires. No per-case counter reset is allowed.

| # / case | Purpose and permitted synthetic behavior | Expected enforcement result | Guest CPU reservation / Q0 wall duration | Required evidence | Failure classification / stop |
|---|---|---|---:|---|---|
| 1 `Q01-ADMISSION` | One VM boot; authenticate the configured COM pipe, verify VM GUID, unit, fresh cgroup, effective limits, one-shot marker, and read-only source. No benchmark code. | Admit only the approved synthetic case after every readback matches; otherwise no workload starts. | 10 s / 60 s | VM ID/state, pipe ACL/config IDs, HMAC challenge transcript, cgroup/control readbacks, baseline, marker, QPC. | Any mismatch is **ADMISSION FAILURE**; stop before workload; no retry. |
| 2 `Q02-CGROUP-CONTAINMENT` | Synthetic process attempts writes to cgroup control files, move itself, gain capabilities, and access host/network paths. | All privileged/escape attempts denied; process remains in approved subtree. | 5 s / 20 s | Cgroup membership, effective UID/caps, denied-operation results, mount/network inventory. | Escape or unverifiable denial is **CONTAINMENT FAILURE**; stop. |
| 3 `Q03-DESCENDANT-INHERITANCE` | Spawn bounded child/grandchild processes; attempt delayed fork and inherited-FD writes. | All descendants inherit cgroup, namespace, credentials, and artifact restrictions. | 5 s / 20 s | PID-to-cgroup snapshots, namespace IDs, FD inventory, process exit and final counters. | Missing descendant or escaped FD/path is **CONTAINMENT FAILURE**; stop. |
| 4 `Q04-MEMORY-HARD-LIMIT` | Synthetic allocator grows past 512 MiB cgroup charge, no task data. | `memory.max=536870912` is enforced; expected OOM/limit event kills only the synthetic child, is recorded, and the empty case cgroup is verified before case 5. | 10 s / 25 s | `memory.current/peak/events`, kernel/systemd OOM evidence, final cgroup state, failure record. | Wrong limit, no observable enforcement, missing OOM evidence, or continued work is **MEMORY FAILURE**; stop. |
| 5 `Q05-ZERO-SWAP` | Synthetic memory pressure under no-swap cgroup policy. | Effective `memory.swap.max=0`; no cgroup swap charge; any OOM is recorded as the expected contained result, not recovered workload success. | 10 s / 25 s | Ancestor settings, `memory.swap.current`, guest swap inventory, `memory.events`, raw timestamps. | Any swap charge, hidden swap path, or unreadable counter is **SWAP-POLICY FAILURE**; stop. |
| 6 `Q06-CPU-CUTOFF` | One-CPU synthetic burner only. Run to the 120-second observation threshold; monitor requests child kill, with the 130.1-second value as absolute candidate stop/fail target. | `cpu.stat:usage_usec` delta is monotonic and complete; request and final usage are captured; no claim of strict max absent a hard mechanism. | 150 s reserved / 160 s wall; 130.1 s is the stop/fail target | Baseline/samples/final `cpu.stat`, `cpu.max`, affinity, timestamps, heartbeat, cgroup events. | The 150 s reservation is not permission to exceed 130.1 s; any delta above 130.1 s, incomplete cessation, or counter gap is **CPU/CONTAINMENT FAILURE**; stop VM, no retry. |
| 7 `Q07-ARTIFACT-QUOTA` | Write/fill/unlink/recreate files in synthetic patterns; include stdout/stderr, JSONL, temporary fixtures, truncation, sparse and open-unlinked files. | Project and host quotas deny further allocation at hard limit; failure reserve remains writable by root only. | 5 s / 20 s | Quota before/after, allocated blocks, inode counts, sparse logical sizes, denied writes, sealed reserve record. | Any write beyond quota, inaccessible reserve, or unaccounted file is **ARTIFACT FAILURE**; stop. |
| 8 `Q08-ALTERNATE-PATHS` | Try `/`, source, home, `/run`, `/dev/shm`, `O_TMPFILE`, memfd, device paths, symlink/hard-link escape, and inherited descriptors. | Only quota-controlled output paths can persist files; all alternate writes denied or explicitly classified non-artifact bounded memory. | 5 s / 20 s | Mount table, path outcomes, FD inventory, namespace state, quota delta, audit log. | Any uncharged persistent writer or ambiguous path is **ARTIFACT CONTAINMENT FAILURE**; stop. |
| 9 `Q09-SUPERVISOR-FAILURE` | Terminate only the synthetic workload supervisor while leaving independent guest monitor and host watchdog alive. No corrective command. | Monitor detects failure, kills workload child, seals reserved failure evidence, authenticates status to host. | 5 s / 20 s | Injected fault time, monitor and heartbeat events, `cgroup.kill`, `populated`, evidence seal and hash. | Monitor failure, missing record, or workload continuation is **SUPERVISOR FAILURE**; host stops VM; no retry. |
| 10 `Q10-EVIDENCE-INTEGRITY` | Synthetic output with known bytes/hashes and deliberate malformed/reordered/replayed control frames. | Host rejects altered/replayed evidence, accepts only canonical MACed sequence, verifies hashes and run identity. | 5 s / 20 s | Raw frames, sequence/MAC outcomes, pre/post hashes, key identifier (never key), append-only host audit. | Any accepted forgery, hash mismatch, lost provenance, or log overflow is **EVIDENCE FAILURE**; stop. |
| 11 `Q11-WALL-LOSS-AND-TURNOFF` | Final live-VM case: start its host-QPC timer and run only the synthetic workload. At `Tcase+170`, deliver authenticated `KILL_CGROUP`, require guest-monitor acknowledgement, then immediately suppress the channel before `+171`. No scientific or corrective runner. | Guest monitor requests `cgroup.kill` and acknowledges at the first stage; missing heartbeat/confirmation then causes one host `TurnOff` no later than `+171`; host observes exact VM Off twice by `+180`. These are targets, not guarantees. | 30 s / 180 s | QPC raw ticks/frequency, stage-1 request/ack, pipe-loss time, host command request/return, VM state polls, final guest CPU and artifact counters. | Lost/late control, late/unknown Off, second TurnOff, or budget overrun is **TERMINATION FAILURE**; stop; no retry. |
| 12 `Q12-OFF-CLEANUP-ONESHOT` | Offline post-VM verification only; no guest restart. Inspect marker, immutable evidence, counters, image hashes, and cleanup state. | Confirm two Off reads, no process/VM restart, evidence seals, one-shot consumed, and no second TurnOff/retry. | 0 s / 30 s | Final host and guest evidence manifests, hashes, marker, VM GUID/state, start/TurnOff counts, quota and resource totals. | Incomplete evidence, residual active VM, altered artifact, or reused marker is **CLEANUP/PROVENANCE FAILURE**; preserve artifacts; do not restart. |

The per-case reservations use the same global hard-limit candidates:
512 MiB cgroup-accounted workload memory with zero cgroup swap, up to
5 MiB guest ext4 project-charged allocation, 1 MiB host NTFS quota usage,
and 768 MiB host control-plane private commit. They are planning ceilings,
not runtime-verified enforcement. The arithmetic is exact: CPU allocations are
`10+5+5+10+10+150+5+5+5+5+30+0 = 240` seconds; wall reservations are
`60+20+20+25+25+160+20+20+20+20+180+30 = 600` seconds. Case 11 is the only
planned test that intentionally triggers host `TurnOff`; an earlier
containment/termination failure may also require the single permitted
request, in which case the matrix stops immediately and later cases are
**NOT RUN**. The total is not a promise all cases will complete after an
early failure. Case 12 is offline and cannot start/restart the VM.
Qualification must never invoke the actual Luna-64 corrective runner,
validator, dataset, or scientific pipeline.

The one-shot marker applies to the entire qualification session: each listed
case may run once in order, but no whole-session retry, restart, or replay is
allowed. An expected synthetic limit event is a case success only when the
required containment and evidence checks pass. Any unexpected containment,
resource, evidence, or termination failure stops the remaining cases; their
status is **NOT RUN**, not silently retried.

The host Job Object and NTFS quota mechanics, ext4 project quota, outer-memory
metric, mixed artifact metric, case resource limits, wall origin, and
one-shot behavior are all proposals. The 240-second guest CPU ceiling and
600-second wall ceiling cannot be asserted as hard maxima while response
latency remains unbounded.

## 6. Independent review and integrated verdict

Four bounded independent read-only reviews were requested:

| Reviewer | Required scope | Result |
|---|---|---|
| A — Host/guest security | Named-pipe/COM identity, HMAC protocol, authorization, VM binding, trust and failure behavior | **BLOCKED** — handshake/replay design is now specified; COM/pipe-to-VM exclusivity, key non-reuse, and autonomous recovery after host watchdog failure remain assumed or untested. |
| B — CPU and wall enforcement | Cgroup accounting, candidate margin, rate limit, QPC stages, overshoot and fail-closed behavior | **BLOCKED** — Q06-local vs continuous parent accounting and Q0/Tcase lifecycle are clarified; the 130.1-second candidate and 240/600-second ceilings still have no hard enforcement or bounded termination. |
| C — Artifact containment | ext4/NTFS/project quota, direct temp paths, sparse files, inode/metadata, evidence reserve, metric change | **BLOCKED** — quota/path accounting is specified, but the proposed live-allocation metric does not satisfy the frozen aggregate logical high-water cap and requires owner approval. |
| D — Governance and provenance | R1 owner decisions, frozen protocol, budgets/case arithmetic, predecessor and exact byte identity, Luna-63C isolation | **BLOCKED** — identities, preserved decisions, case lifecycle, and arithmetic reconcile; infrastructure/metric approvals and enforcement evidence are absent. |

The final integrated Luna-0 review and exact findings are in the companion
review record
`workflow/handoffs/luna-0-independent-review-luna64-r4.3-corrective-supervisor-a6-r2-20261012.md`.
All reviews were documentary and read-only; no independent reviewer executed
platform enforcement or qualification.

## 7. Blockers, approvals, and stopping rule

The R2 gate is **BLOCKED — ENFORCEMENT DESIGN INCOMPLETE** pending resolution
of the following:

1. **Host/guest identity and recovery:** the COM/pipe ACL and exclusive
   mapping to the authorized VM are unqualified; key non-cloning/non-reuse
   is a policy assumption. A failed or starved host controller/watchdog has
   no autonomous recovery and no guaranteed VM-Off deadline.
2. **CPU hard boundary:** the accepted 130.1-second candidate and 240-second
   qualification aggregate lack a demonstrated hard cumulative CPU cutoff
   and finite termination latency.
3. **Wall hard boundary:** QPC is monotonic, but Hyper-V `TurnOff`, VMMS, and
   Off confirmation have no demonstrated finite completion bound. A late
   operation can exceed 180/600 seconds.
4. **Artifact policy:** no stock method in this design enforces the frozen
   5 MiB aggregate logical high-water metric. The allocated-block alternative
   is a material policy change that needs explicit owner approval.
5. **Qualification measurement changes:** 768 MiB is proposed as host
   control-plane private commit, not whole-system memory; 6 MiB combines
   declared guest and host allocation charges. Both need explicit owner
   approval and independent prereview.
6. **Runtime uncertainty:** COM pipe ACL/mapping, cgroup quota enforcement,
   filesystem quota accounting, Job Object boundaries, and evidence durability
   have not been installed or qualified. Owner diagnostics are not reviewer
   execution.
7. **Authority:** D6 denies infrastructure changes; D4 is planning-only.
   No qualification or corrective execution authority exists.

This is an **unavailable-enforcement-evidence and owner-policy** blocker, not
a demonstrated engineering impossibility. Do not automatically initiate R3.
The smallest next action is an owner decision on the proposed artifact and
qualification-memory accounting changes, followed by a separately authorized
technical feasibility/implementation qualification plan that supplies a
genuine hard aggregate CPU/wall boundary or explicitly changes those
resource guarantees. An owner decision alone cannot establish the missing
termination bound.

**A6 remains BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE.** The original pilot
remains **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not an efficacy
result. The corrective allowance remains unused. No scientific rerun,
production integration, architecture promotion, or Luna-63C work is
authorized. Stop here.

## 8. References and validation limits

Design references (availability/documentation only; no runtime claim):

- Microsoft `Set-VMComPort` documents mapping a VM COM port to a local named
  pipe: <https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmcomport?view=windowsserver2025-ps>.
- Linux cgroup v2 interface documentation:
  <https://docs.kernel.org/admin-guide/cgroup-v2.html>.
- systemd resource-control directives:
  <https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html>.
- Windows Job Objects and job memory limits:
  <https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects> and
  <https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information>.
- Linux ext4 project quota interface documentation:
  <https://docs.kernel.org/filesystems/quota.html> and
  <https://docs.kernel.org/filesystems/ext4/special_inodes.html>.
- Microsoft documents that sparse files affect Windows user quotas by
  nominal file size rather than actual allocated disk space:
  <https://learn.microsoft.com/en-us/windows/win32/fileio/sparse-files-and-disk-quota>.

Validation performed: before R2 drafting, the R1 package/closure
existence and ancestry, branch `governance/luna64-r4.3-freeze-20261010`,
starting HEAD and upstream at `f1cfb6e98cfc872753ea262bdb56e4a66ab40c05`,
and the three exact R1 checkout SHA-256 values were verified. The R2
proposal, review, manifest, workflow entry, and attribute changes are
uncommitted blocked-state records; no R2 publication commit or remote
revision exists. Four independent documentary reviewers assessed the design,
and the 12-case arithmetic was checked separately.

Not run: VM diagnostics, COM/pipe setup, HMAC protocol, service/cgroup
configuration, Job Objects, filesystem images, quotas, any qualification
case, corrective tests, or scientific work. Passing document checks and
independent design review do not prove runtime enforcement.
