# Luna-0 — Luna-64 A6 R2 Owner-Policy Reconciliation R1

**Reconciliation:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6-R2-OWNER-RECONCILIATION-R1`  
**Parent:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6-R2`  
**Disposition:** **PASS — A6 R2 OWNER-POLICY RECONCILIATION VERIFIED; ENFORCEMENT DESIGN REMAINS UNQUALIFIED**
**Parent verdict, unchanged:** **BLOCKED — ENFORCEMENT DESIGN INCOMPLETE**  
**Scope:** Governance-only policy reconciliation, proof-obligation definition, and independent review. No infrastructure, supervisor, qualification case, corrective test, or scientific workload was implemented or executed.

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: Luna-0
  descriptive_name: Luna-64 A6 R2 owner-policy reconciliation R1
  task_id: L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6-R2-OWNER-RECONCILIATION-R1
  component: Experimental execution governance
  status: conditional-publication-after-independent-pass
  branch: governance/luna64-r4.3-freeze-20261010
  base_revision: f1cfb6e98cfc872753ea262bdb56e4a66ab40c05
  dependencies:
    - Frozen R4.3 protocol and original corrective authorization
    - Published A1-A5 blocked findings
    - A6 R2 proposal, review, manifest, and workflow candidate
    - Owner decisions D1-D6 recorded by R1
    - Owner decisions R2-D7 and R2-D8 supplied in this task conversation
  classification:
    - GOVERNANCE ONLY
    - POLICY RECONCILIATION
    - NO INFRASTRUCTURE CHANGE AUTHORITY
    - NO QUALIFICATION EXECUTION AUTHORITY
    - NO CORRECTIVE OR SCIENTIFIC EXECUTION AUTHORITY
  architecture_change: false
  execution_authorized: false
```

## 1. Authority and verified repository baseline

This reconciliation records only owner decisions D7 and D8 supplied in the
current task conversation. It does not infer owner intent from technical
review, the R2 proposal, or prior diagnostics. D1-D6 remain as recorded in
the published R1 owner-policy reconciliation. D7 and D8 supplement those
decisions prospectively for qualification design; they do not retroactively
authorize work or change a prior verdict.

At the start of this reconciliation:

- Branch: `governance/luna64-r4.3-freeze-20261010`.
- HEAD and upstream: `f1cfb6e98cfc872753ea262bdb56e4a66ab40c05`.
- HEAD is the R1 workflow closure and descends from package commit
  `f00dea13d64657cbc976d21daf50739ddf9722fe`.
- The R1 proposal, review, and manifest checkout SHA-256 values match the
  R1 manifest.
- No changes were staged. Existing unstaged state consisted of the R2
  candidate `.gitattributes`/workflow changes and the three untracked R2
  proposal, review, and manifest files. No unrelated changes were observed.
- R2 candidate paths use path-specific `-text` attributes. The rules are
  required to preserve exact checkout bytes; repository-wide `text=auto`
  remains unchanged. The workflow remains under its pre-existing text
  normalization rule.
- The R4.3 Stage-A freeze and Stage-B attestation are in the R1 ancestry.
  The frozen manifest in Stage A hashes to the expected
  `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`.
  All ten R4.3 package blobs in the attestation were rehashed from Git and
  match their raw SHA-256 and published blob OID entries. The 32-entry
  governing-input inventory matches its recorded SHA-256; each raw hash
  reconciles at the Stage-A freeze, with 9 direct blob-byte matches and 23
  exact LF-to-CRLF materializations. All 32 recorded Git object IDs exist.
  The published attestation reports 26 unchanged recorded OIDs and six
  exact-byte remappings. This historical check uses Stage A because the
  workflow has subsequent R1/R2 additions; later workflow bytes are not
  compared as if they were the frozen 32-entry source.
- The original corrective authorization, R1 proposal/review/manifest,
  A6-R1/R2 and Luna-63C authorization records have been hashed/read from the
  current checkout or pinned Git objects. The parent R2 evidence and R1
  decision record are not modified by this reconciliation.

### 1.1 R2 candidate byte identities protected by this reconciliation

All expected checkout SHA-256 values supplied for the current R2 candidates
were recomputed and matched. These four original R2 artifacts are evidence
inputs, not editable reconciliation targets:

| R2 candidate | Checkout SHA-256 | Handling |
|---|---|---|
| Proposal | `9BD03652AB06208FAEF9EA2C2B1EB3BD96FF79CCE16C379D46935D5CD8256DD0` | Preserve exact bytes |
| Independent review | `598315F87962C9073558E84995A1749E0EADAB91082AD7ADD8FB07B4836D4162` | Preserve exact bytes |
| Manifest | `E1347D71E7714DFA9E4D00321CB2E784510638A592C9EDDBFDC9D603B03BE93E` | Preserve exact bytes; do not regenerate |
| R2 workflow candidate | `A43E9C634F20C78DD6EFB37BB037D1CEADFB4FEAAEF185C7C1BF2C732A8DCC72` | Preserve as the R2 package-stage workflow bytes; any R1 workflow closure is a subsequent, separately identified additive commit |

The package must retain a commit containing the exact verified R2 candidate
state before the separate R1 workflow-closure commit. If Git staging would
materialize any protected R2 candidate differently, stop rather than
silently accepting a byte-identity change.

### 1.2 Frozen and historical authority

The following identities were checked as existing Git commits and as
ancestors of the R1 closure:

| Evidence | Identity and status |
|---|---|
| R4.3 content freeze / governance closure | `64a214e310de3b982b90a8ad215598bc1e9f8b1c` / `ea1b10456cbf4ca726e473076d239a4f6e53b9c7` |
| Frozen R4.3 manifest | SHA-256 `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B` |
| Original corrective authorization | `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`; corrective allowance remains unused |
| A1 / A2 / A3 | `d20aab249e42575ccc571c9c72153a3bb4b412db` / `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c` / `8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0`; prior blocked findings retained |
| A4 package / closure | `7bd440565c38dee81ace3606fde3fb686de6a0ef` / `f86c25844a4863ac57cd6634f364c28bcf2f511f`; blocked |
| A5 package / closure | `12f84a41fe7c91c17c5df8e975fce24efbadf9ad` / `b758b411e568b41c516228e7d3bdff26058114cc`; **BLOCKED — A5 QUALIFICATION INCOMPLETE** |
| A5 proposal / review SHA-256 | `5BCDAC72E7EBDEA777E9964F25554834C4460D97075E6871690BD441BA00C6E5` / `54D11A362EDED451292330C6FA5627B570BD6103ADE0F69E115F5CDC3C7B934D` |
| R1 package / closure | `f00dea13d64657cbc976d21daf50739ddf9722fe` / `f1cfb6e98cfc872753ea262bdb56e4a66ab40c05` |
| R1 proposal / review / manifest SHA-256 | `A619E3A4361B712471B8C3A7FD2AA784992ED6B4F5F0E218ED0449B16144319D` / `DD7E0F840F8C3F34A7016351C28F63CA50F313618DC1B218B81A509CBD8E4D36` / `D51C207C5ED7E91B59C661FB39B67E88F27C0FA47CDEF708AA1F0ADFB7DEE958` |
| Parent A6 R2 | **BLOCKED — ENFORCEMENT DESIGN INCOMPLETE**; preserved unchanged |
| Original scientific pilot | **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**; not an efficacy result |

The original authorization remains limited to the exact corrective
implementation and focused tests in its immutable gate. Its original 120
CPU-second / 180 wall-second / 512 MiB working-set / 512 combined synthetic
fixture-and-trace record / 5 MiB artifact limits, one-logical-CPU ceiling,
stop conditions, one-shot and verification constraints are not amended by
R2-D7 or R2-D8. The parent R2 and this reconciliation do not resume that
allowance.

The Luna-63C isolation boundary is retained: its distinct certificate-gated,
isolated mechanism lane and artifacts remain untouched. No Luna-63C files or
scientific material were used or changed by this reconciliation.

## 2. Owner decisions reconciled

### 2.1 Decisions D1-D6 retained

1. **D1 — memory:** Linux cgroup-accounted memory is accepted as a
   qualification-design replacement for Windows working-set accounting,
   with `memory.max=536870912` and proposed `memory.swap.max=0`. It is
   materially non-equivalent and has not been enforced or qualified.
2. **D2 — CPU/wall:** 130.1 CPU seconds and 170/171/180-second stages are
   monitored, unverified design targets; they are not hard bounds.
3. **D3 — storage alternatives:** simpler supported containment mechanisms
   are considered before custom FUSE; no infrastructure is implemented.
4. **D4 — budget:** the separate qualification budget is planning-only.
5. **D5 — control:** authenticated non-network host/guest control is
   required.
6. **D6 — authority:** infrastructure changes remain unauthorized.

### 2.2 R2-D7 — distinct artifact allocation targets

The owner accepts, **for qualification design only**:

- Guest authorized writable artifact space: maximum **5 MiB**, measured as
  guest ext4 project allocation.
- Host evidence and control records: maximum **1 MiB**, measured as host
  NTFS quota usage.

These are distinct accounting domains. The nominal 6 MiB sum is not a
unified logical-byte measurement, physical-allocation measure, or
already-enforced common quota. It is non-equivalent to the frozen 5 MiB
aggregate logical-byte high-water criterion. D7 approves the target metrics
for design, not their implementation, enforcement, qualification, or use
for corrective execution.

D7 does not authorize filesystem creation, ext4 project quota configuration,
NTFS quota changes, namespace changes, FUSE, an artifact mediator, or any
qualification run. The fifteen proof obligations in §4.4 remain open.

The design candidate is the R2 fixed-size ext4 image with the ext4 project
quota feature enabled (`prjquota`), inherited project IDs for the workload
and root-only reserve directories, and block/inode hard limits assigned to
those project IDs. The future implementation must assign and read back
project IDs (including inheritance flags) and query/configure project quota
through the Linux filesystem quota interfaces; it must show actual charged
block and inode counters at each relevant boundary. Host evidence uses
built-in NTFS per-owner hard quotas keyed to the verified file-owner SID;
the hard limit and current usage must be read back for each ordinary and
emergency recorder account. These are proposed mechanisms, not installed
controls.

### 2.3 R2-D8 — monitored CPU and wall targets

The owner accepts, **as monitored qualification-design targets**:

- Normal CPU budget: **120 aggregate CPU seconds**.
- Candidate cutoff: **130.1 aggregate CPU seconds**.
- A detected overrun is a qualification failure.
- Wall termination/escalation stages: **170, 171, and 180 seconds**.
- These values do not guarantee that workload cessation or VM-Off occurs by
  a particular deadline.

The 130.1-second candidate does not establish a strict lifetime CPU bound.
Rate limits are not lifetime cutoffs. The existing original corrective
authorization remains at 120 CPU seconds; changing that authorization would
require a separate explicit owner decision. No D8 decision transfers,
extends, or consumes the parent corrective allowance.

For the proposed qualification protocol, retain the distinct R2 accounting
levels and assign explicit failure semantics:

- Q06-local measurement uses a fresh nested accounting cgroup baseline
  immediately before its synthetic monitor is admitted. The monitor and
  burner descendants are within the measured Q06 subtree. At a 120-second
  observation threshold, the monitor records budget exhaustion, stops
  dispatching work, and requests child termination. The 120-second normal
  budget is not extended by cleanup: CPU consumed through final cessation
  remains counted. Any final measured Q06 delta above 120 seconds is a
  normal-budget overrun and a qualification failure. The 130.1-second value
  is a later candidate cutoff/escalation observation, not permission to use
  an extra 10.1 seconds. At the first observation at/above 130.1 seconds, the
  monitor records the candidate-boundary failure and immediately requests
  termination; the host may issue its one permitted VM `TurnOff` if not
  already requested. This is action on observation, not a guarantee the
  value cannot be crossed between samples or before cessation.
- The qualification-parent `cpu.stat:usage_usec` counter is continuous from
  its empty-parent baseline through final empty-subtree confirmation.
  It includes all in-scope guest monitor, supervisor, case, descendant, and
  in-cgroup cleanup CPU after baseline and is charged to the aggregate
  240-second planning ceiling. It is not reset for Q06.
- Future corrective invocation CPU scope begins immediately before
  workload-service activation. The guest invocation-parent cgroup and its
  baseline must exist before this point. It includes the guest invocation
  monitor, supervisor bootstrap, tests, descendants, and cleanup through
  final empty-subtree confirmation. The killable workload is a nested child;
  the trusted guest monitor may remain in the invocation parent while it
  completes and records the stop. Any guest monitor started before service
  activation must be charged to a separately declared, finite pre-admission
  allocation and must not disappear from both scopes. Host controller and
  host watchdog CPU are measured in a separate, explicit host budget. VM/OS
  boot and PID 1 activity before service activation are not silently treated
  as zero or unbounded exceptions: they must be separately measured and
  bounded by an explicit future authorization.

These D8 monitored targets do not relax the original corrective gate. That
gate's 120 CPU-second and 180 wall-second limits remain binding unless a
separate owner authorization explicitly changes them. Since this design
does not prove a hard 120-second cessation or guaranteed 180-second VM-Off,
corrective execution remains prohibited. Qualification may record whether
monitored targets were met or missed, but cannot qualify an execution
contract whose stated hard limits are not enforced.

For wall-time design, preserve R2's distinct clocks:

- `Q0` is host QPC immediately before the single VM-start request. The
  proposed 600-second qualification wall allowance includes VM boot,
  admission, all cases, cleanup, evidence sealing, and confirmed VM-Off.
- `Tcase` is the host-QPC dispatch time for an individual qualification
  case. Q11 uses its `Tcase` for the 170/171/180 stages.
- A future corrective `T0` is immediately before activation of the approved
  workload service. That invocation's bootstrap, tests, cleanup, and
  termination are within its wall scope; a 170-second guest-stop request,
  171-second host escalation, and 180-second Off/evidence target are
  monitored candidates, not guaranteed deadlines.

Neither a successful request return nor a failed qualification verdict
proves containment. Final state must distinguish resource-budget failure
from integrity failure and from **CONTAINMENT FAILURE** where activity or VM
state cannot be confirmed stopped. Preserve raw observations and evidence
even on failure; do not claim a runaway workload was contained merely
because the attempt was rejected.

## 3. Revised qualification resource-policy candidate

This policy reconciles the newly accepted D7/D8 design targets with the
planning-only D4 allowance. It is not enforcement evidence or execution
authority.

| Domain | Candidate | Meaning and status |
|---|---:|---|
| Cases | 12 | Fixed order and identities in §4.5; synthetic only |
| Guest qualification CPU | 240 CPU seconds | Continuous qualification-parent `cpu.stat:usage_usec` delta; planning ceiling, not hard enforcement |
| Q06 normal/candidate CPU | 120 / 130.1 CPU seconds | Q06-local nested-subtree monitored targets; any observed overrun fails; not a lifetime guarantee |
| Wall time | 600 seconds | QPC `Q0` through confirmed VM-Off and evidence seal; planning ceiling without finite completion guarantee |
| Wall stages | 170 / 171 / 180 seconds | `Tcase`/`T0` relative stop, escalation, and Off/evidence targets; not guaranteed deadlines |
| Guest memory | 536,870,912 bytes | Linux cgroup charge hard-limit candidate; zero swap candidate; runtime unqualified |
| Guest artifact allocation | 5,242,880 bytes | Guest ext4 project allocation per R2-D7; separate metric from host NTFS usage |
| Host evidence/control records | 1,048,576 bytes | Host NTFS quota usage per R2-D7; distinct metric |
| Nominal guest-plus-host allowance | 6,291,456 bytes | Arithmetic sum only; not one unified metric or quota |
| Host control-plane memory | 805,306,368 bytes | R2 candidate private-commit metric; no new owner acceptance supplied; exact implementation and approval remain open |
| VM starts / TurnOff / retries | 1 / at most 1 / 0 | Planning limits only; no execution authority |
| Corrective allowance | Separate, unused | No transfer to/from qualification; original authorization unchanged |

The exact reservation vectors in the R2 candidate are CPU
`[10,5,5,10,10,150,5,5,5,5,30,0]` seconds and wall
`[60,20,20,25,25,160,20,20,20,20,180,30]` seconds. They sum to exactly
240 CPU seconds and 600 wall seconds. Q06's 150-second reservation is a
planning allocation only and does not authorize exceeding its 130.1-second
candidate. A case stopping early does not enlarge any later reservation.

The 768 MiB host private-commit metric is not accepted by D7/D8 and does not
become owner-approved through this reconciliation. It must be defined,
bounded, and expressly accepted before any future authorization.

## 4. R2-to-reconciliation findings and proof-obligation matrix

| Blocker | Current evidence | Owner decision | Unverified assumptions | Required implementation/design | Required qualification | Required authorization | Status |
|---|---|---|---|---|---|---|---|
| **B1 — Authenticated host/guest control** | R2 specifies virtual COM/local named pipe candidate and HMAC framing, sequence, and challenge. R1 requires authenticated non-network control. No channel was configured or tested. | D5 requires authenticated non-network control; D6 denies infrastructure changes. | Exclusive pipe-to-VM mapping, peer identity, endpoint ACLs, key generation/storage/retirement and image non-reuse. HMAC proves key possession, not the correct VM. | Bind the exact host-created endpoint to the authorized VM configuration; verify all COM mappings and exclusivity before admission; use a one-shot unpredictable run identity/challenge, authenticated host and guest direction, complete MAC coverage, sequence/replay/reconnect rejection, strict command allowlist, protected key custody and retirement. Define host authorization and logging. | Verify VM/pipe binding, ACL and device mapping on the actual host; authenticate both directions; reject wrong VM/run, malformed/MAC-invalid/replayed/gapped frames and reconnect; exercise channel loss. | New exact infrastructure-change and qualification authorization; no D5 inference is execution permission. | **BLOCKED** |
| **B2 — Cumulative CPU termination** | `cpu.stat:usage_usec`, nested Q06 accounting scope, continuous 240-second parent delta, rate restriction, sampling and kill requests are design-only. | D2 and D8 accept 120/130.1 targets only; aggregate qualification allowance remains planning-only. | Scheduling/polling delay, monitor starvation, cgroup-kill latency, host response and final counter behavior. `cpu.max` is a rate limit only. | Implement a trusted monitor and read-only external counter verification; seal baseline, sample raw `usage_usec`, request termination at 120 and on first observed 130.1 crossing; include all approved descendants and supervisor CPU. Confirm cgroup `populated 0`; preserve final counters. | Inject threshold-crossing synthetic load; measure per-sample and final overshoot; test counter discontinuity, monitor loss, cgroup-kill failure, delayed response, and host escalation. Report observed overshoot, never as universal maximum. | New implementation/qualification authorization with exact metric, CPU affinity/rate ceiling, maximum observed-vs-allowed criteria, and explicit acceptance that monitored values are not hard bounds—or a separately evidenced hard cutoff. | **BLOCKED** |
| **B3 — Wall termination** | QPC `Q0`, `Tcase`/`T0`, 170/171/180 actions, asynchronous TurnOff, two Off reads and failure classification are design-only. | D2/D8 accept stage targets only; D4's 600-second session allowance is planning-only. | Host scheduler and watchdog availability; guest acknowledgement; VMMS/Hyper-V TurnOff and Off-observation latency have no proven maximum. | Keep a trusted host monotonic clock/watchdog outside the guest. At stage 1 send guest cgroup stop; at stage 2 issue at most one exact-GUID TurnOff if still active/unconfirmed; verify two Off reads and sealed evidence. Define controller crash/loss behavior; no duplicate/retry. | Exercise guest channel loss, guest stop delay, watchdog/controller failure, API error/pending call, absent Off confirmation, and evidence failure. A failure must explicitly distinguish resource overrun from containment failure. | New infrastructure and qualification authorization, with stop/failure criteria and any policy response to unbounded completion latency. | **BLOCKED** |
| **B4 — Artifact quota** | D7 explicitly accepts 5 MiB guest ext4 project allocation and 1 MiB host NTFS quota usage as separate design targets. R2 identifies direct temp writes; R2 analysis and Microsoft documentation distinguish allocation/quota metrics from logical file length. | D7 accepts only these design metrics; no implementation or execution authorization. Original logical high-water criterion remains unchanged as historical frozen policy. | Complete writer inventory, quota charging, project inheritance, reserve durability, SID charging, and alternate-path closure. | Enumerate all writable paths, direct temp behavior, stdout/stderr, JSONL, fixtures, failure reserve, export, cleanup, sparse/unlinked files, symlinks/hard links, inherited FDs and host evidence. Use OS-supported restricted writable mounts and quotas; do not rely on post-run measurement. | Exercise exhaustion and denied alternate paths; verify project/NTFS quota counters, sparse/unlinked behavior, reserve use, inode/metadata exhaustion, evidence reconciliation, and frozen-test compatibility. | Separate filesystem/quota implementation and qualification authorization. D7 does not authorize creating or modifying storage. | **BLOCKED** |
| **B5 — Qualification protocol** | R2 gives fixed Q01-Q12 identities, ordered behaviors, expected results, evidence, per-case reservations, and stop behavior. Arithmetic is independently recomputed in this reconciliation. | D4 allows planning only; D7/D8 accept resource targets for design only. | Actual tests, exact commands/fixtures, host/guest setup, evidence durability and all enforcement remain untested. | Freeze exact twelve case IDs, scripts/commands, order, synthetic inputs, per-case limits, fixture hashes, negative controls, evidence schema, failure classifications, no-retry rule, and cleanup protocol in a reviewed immutable spec before execution. | Independent prereview; then one authorized run only, no corrective runner/dataset/task data; retain raw records, measured overshoot, hashes, start/TurnOff counts and NOT-RUN statuses after early stop. | A new explicit owner authorization referencing exact spec hashes, infrastructure allowlist, resources, single-use run ID, and independent prereview PASS. | **BLOCKED** |
| **B6 — Bootstrap and trust boundary** | R2's guest cgroup baseline excludes VM boot/PID 1 activation CPU from the guest aggregate; Q0 wall includes VM start through Off. Host controller CPU is separately measured. | D8 requires an explicitly defined approved CPU scope; D6 denies infrastructure changes. | Resource use and authority of pre-admission host/guest bootstrap; service/cgroup creation and monitor startup behavior. | Enumerate every process/action before workload cgroup admission: host controller/watchdog/VMMS calls; guest boot/PID 1; root provisioner; systemd unit start; monitor and serial client. Apply privilege separation, exact write/command allowlists and finite per-phase resource/time ceilings. Start workload only after cgroup/limits are read back. No blanket bootstrap exemption. | Instrument phase boundaries and separate host/guest CPU, memory, wall and artifact use; fault-inject before/at admission and verify fail-closed no-workload behavior and evidence. | Explicit authorization must cover bootstrap resources and trusted components; no infrastructure operation under this reconciliation. | **BLOCKED** |

### 4.1 Authenticated non-network channel minimum evidence

The R2 HMAC proposal alone is not proof of VM identity. Before any future
qualification, evidence must establish: (a) exact host VM GUID and configured
COM endpoint; (b) exclusive host pipe ACL and no second VM/device mapping;
(c) guest serial peer and approved image identity; (d) fresh one-shot key,
run challenge and direction-bound MAC; (e) command allowlist and durable
monotonic sequence state; (f) rejection of stale/replayed/reconnected
sessions; (g) protected key custody, retirement and no image reuse; (h)
channel-loss response independent of guest cooperation; and (i) host
TurnOff authority not delegated to the guest. Each is currently
**PROPOSED/UNQUALIFIED**, not a verified property.

### 4.2 CPU, wall, and containment verdict semantics

Record separately:

- **Budget compliance:** whether cumulative in-scope CPU, memory, artifact,
  and elapsed-time observations met their accepted candidate criteria.
- **Containment integrity:** whether the workload subtree reached
  `populated 0`, no descendant or writable handle escaped its boundary, and
  the exact VM reached the required confirmed Off state.
- **Evidence integrity:** whether raw counters, request/ack timestamps,
  state observations, errors, and artifact hashes are complete and
  internally consistent.

An overrun is a qualification failure even if subsequent containment
succeeds. A failed or delayed termination, unknown final process/VM state,
missing observation, or incomplete evidence is explicitly a **CONTAINMENT
FAILURE** (and may also be a resource/evidence failure). Never equate a
rejected run with a successfully contained runaway process.

### 4.3 Bootstrap and trusted components

Trusted components proposed by R2 are the Windows host OS/administrator,
Hyper-V/VMMS, host controller and QPC watchdog, guest kernel/systemd PID 1,
root provisioner, root monitor, serial client, and quota configuration.
Workload code and descendants are untrusted and must have no host API,
device, cgroup delegation, mount authority, capability, or key access.

No time or resource allowance is implicitly unlimited before cgroup
admission. The future qualification spec must enumerate all bootstrap
processes, start/end boundaries, privilege, file/device access, CPU/memory/
wall/artifact allocations, failure evidence, and cleanup. Guest boot and
PID 1 CPU excluded from the workload cgroup delta must be separately
measured and bounded; host control-plane work must have its own explicit
metric and ceiling. Admission is denied unless all readbacks match before
any synthetic case is dispatched.

### 4.4 Artifact enforcement proof obligations

Before runtime qualification, the implementation design must specify and
prove coverage for all of the following:

1. Exact project-quota/filesystem mechanism and hard-limit units/readback.
2. Exact ext4 project allocation semantics and NTFS owner-quota usage
   semantics as separate counters.
3. Every writable guest/host path and every writer identity.
4. Frozen test direct temporary writes (`TMPDIR`, `TMP`, `TEMP`, runtime
   temp resolution) and any child process temporary paths.
5. Sparse file allocation/charge behavior versus logical length.
6. Hard-link and symlink creation/resolution and escape prevention.
7. Unlinked-but-open file charge until final close.
8. Inherited descriptors, directory handles, stdout/stderr pipes and
   descendant access.
9. Standard output, standard error, JSONL traces, generated fixtures,
   failure records, and export staging.
10. A protected failure-evidence reserve, metadata/inode headroom and
    durability if workload quota is exhausted.
11. Quota exhaustion behavior, including file, block, inode, journal and
    metadata exhaustion; no success-shaped fallback.
12. Host/guest evidence reconciliation without double-counting and with
    owner SID/quota identity readback.
13. Alternate output prevention, including read-only root, restricted
    mount namespace, devices, `/run`, `/dev/shm`, outside directory FDs,
    memfd/O_TMPFILE, and host handles.
14. Export staging, immutable hash/seal, cleanup and post-VM verification.
15. Compatibility with the exact frozen test behavior and no modification
    of frozen test artifacts.

Prefer bounded ext4 project quotas plus read-only root and narrowly mounted
writable areas over custom FUSE where they cover the direct writes. If exact
scope cannot be demonstrated, remain blocked; do not substitute a
post-run scan or label filesystem capacity as a logical-byte cap.

## 5. Frozen proposed qualification matrix and authorization boundary

The exact twelve identities already in the R2 candidate are retained and
must be frozen with scripts, fixture hashes and evidence schema in the
future authorization package:

1. `Q01-ADMISSION`
2. `Q02-CGROUP-CONTAINMENT`
3. `Q03-DESCENDANT-INHERITANCE`
4. `Q04-MEMORY-HARD-LIMIT`
5. `Q05-ZERO-SWAP`
6. `Q06-CPU-CUTOFF`
7. `Q07-ARTIFACT-QUOTA`
8. `Q08-ALTERNATE-PATHS`
9. `Q09-SUPERVISOR-FAILURE`
10. `Q10-EVIDENCE-INTEGRITY`
11. `Q11-WALL-LOSS-AND-TURNOFF`
12. `Q12-OFF-CLEANUP-ONESHOT`

Their purposes, synthetic behavior, expected controls, reservations,
evidence, failure classes and stop behavior remain exactly those in the
preserved R2 proposal. Q11 is the planned final live-VM case; Q12 is offline
only. Any unexpected failure stops the sequence, and all later cases are
reported **NOT RUN**. Exactly one VM start, at most one host `TurnOff`, and
zero retries/restarts/replays are planning controls, not runtime-proven
facts.

### 5.1 Proposed future infrastructure-change boundary

No change is authorized now. A future exact owner authorization and
independent prereview would need to enumerate, by path/object and hash:

- One dedicated root-managed systemd unit and non-delegated cgroup tree
  with reviewed CPU/memory/swap/pids/cpuset controls.
- A narrowly scoped host controller/watchdog and exact-VM Hyper-V actions.
- The selected authenticated non-network COM/pipe endpoint and ACL, if its
  feasibility and security are independently established.
- A read-only root and bounded guest ext4 artifact image/project, plus
  host evidence directory and NTFS quota assignments.
- Explicit bootstrap and workload identities, privilege/capability sets,
  writable mount points, temporary environment, and command allowlist.
- Versioned qualification scripts, synthetic fixtures, evidence schema,
  hash/seal process and one-shot marker.

The allowlist excludes frozen R4.3 artifacts, production/core/ACP files,
datasets, labels, the actual corrective runner during qualification, all
scientific arms, Luna-63C records, and unlisted host or guest changes.
Rollback, evidence preservation, VM cleanup and stop authority must be
specified. Authorization must include the exact source revision, resource
definitions, maximum counts, no-retry policy and a single-use run identity.

### 5.2 Required future qualification authorization

Before any qualification execution, require all of:

1. Explicit owner approval of the D7 metrics and any other changed resource
   definitions, including the unaccepted 768 MiB host memory metric.
2. A reviewed exact 12-case spec with immutable hashes and a frozen order.
3. Independent prereview PASS of design, threat model, source, and staged
   publication identities.
4. Exact platform/infrastructure change allowlist, rollback and trusted
   bootstrap limits.
5. A feasible authenticated host/guest identity/control design with
   demonstrated channel-loss and host-failure response.
6. Resource ceilings that distinguish guest qualification parent, Q06
   local target, host control-plane memory, bootstrap, wall clocks,
   separate artifact domains, metadata and failure reserve.
7. A truthful policy for unbounded termination response: either accept the
   monitored-target semantics with explicit failure/containment reporting
   and bounded external emergency policy, or establish an actual hard
   enforcement boundary. Do not claim the current design proves either.
8. A single VM/run identity, one start, at most one `TurnOff`, no retries,
   and explicit stop on any discrepancy.
9. Confirmation that no corrective allowance is consumed and no actual
   corrective runner, task data, dataset, labels, or scientific workload
   is invoked.
10. Final owner authorization tied to the exact reviewed commit/tree and
    remote revision. D7/D8 by themselves do not satisfy this gate.

## 6. Independent review and decision

Independent reviewers must assess this reconciliation and its exact staged
bytes in four disjoint scopes:

- **A — Policy/governance:** D7/D8 attribution; preservation of D1-D6,
  frozen/R1/R2 statuses, original pilot disposition, and Luna-63C isolation;
  policy acceptance versus execution authorization.
- **B — Resource semantics:** separate ext4/NTFS metrics; artifact
  non-equivalence; CPU/wall target meaning; bootstrap and scope; overrun
  versus containment failure; budget arithmetic; no hard-bound claims.
- **C — Security/enforcement:** authenticated identity requirements,
  host/guest binding, bootstrap TCB, artifact path coverage, future
  implementation/qualification boundaries and no authority leakage.
- **D — Provenance/publication:** all four R2 identities, frozen/R1
  identities, Git attributes and normalization, allowlist, historical
  record preservation and staged/committed byte identities.

The required independent review record is
`workflow/handoffs/luna-0-independent-review-luna64-r4.3-a6-r2-owner-reconciliation-r1-20261011.md`.
No reviewer may claim runtime qualification or infrastructure capability
from this governance review.

**Integrated decision:** **PASS — A6 R2 OWNER-POLICY RECONCILIATION
VERIFIED.** Independent reviewers A–D passed the governance, resource,
security/enforcement, and proposal-level provenance review of the exact
proposal bytes recorded in the reconciliation manifest. Reviewer D's
publication-stage verification remains a separate pre-commit gate: the
reconciliation review, manifest, allowlisted index, committed blobs, and
remote ancestry must still be checked as specified in §7.

This PASS leaves the parent **BLOCKED — ENFORCEMENT DESIGN INCOMPLETE** and
confers no infrastructure, qualification, corrective, or scientific
execution authority. Any failed identity or publication-stage check blocks
publication; it does not retroactively change the proposal-level review.

## 7. Publication and stop rules

Publication is conditional on independent PASS. The initial package commit
has this literal allowlist and no other paths:

1. `.gitattributes` — exact-path `-text` rules for the new reconciliation
   artifacts and `workflow/docs/luna/LUNA_WORKFLOW.md`; no global
   normalization-policy changes; checkout SHA-256
   `5EE757DD2EAADE72DB7DADFBA79DE304DC93EEDF2D0BEF3D432C0587832418D7`,
   raw Git blob
   `11d6bdf41216045d5989002a1684aa015ce8b58f`.
2. `workflow/docs/luna/LUNA_WORKFLOW.md` — the byte-for-byte R2 candidate
   workflow only, checkout SHA-256
   `A43E9C634F20C78DD6EFB37BB037D1CEADFB4FEAAEF185C7C1BF2C732A8DCC72`,
   raw Git blob
   `78e0f1d16d19a4f3e20de3fcf18ab341732732d5`.
3. `workflow/handoffs/luna-0-luna64-r4.3-corrective-supervisor-a6-r2-20261012.md`
   — protected checkout SHA-256
   `9BD03652AB06208FAEF9EA2C2B1EB3BD96FF79CCE16C379D46935D5CD8256DD0`,
   raw Git blob
   `9f57e3779522dd3a16569378d5fc2c95146c2e9d`.
4. `workflow/handoffs/luna-0-independent-review-luna64-r4.3-corrective-supervisor-a6-r2-20261012.md`
   — protected checkout SHA-256
   `598315F87962C9073558E84995A1749E0EADAB91082AD7ADD8FB07B4836D4162`,
   raw Git blob
   `3752aedda542783b718b1d00e784229994d3f28b`.
5. `workflow/handoffs/luna64-r4.3-a6-r2-20261012-manifest.json`
   — protected checkout SHA-256
   `E1347D71E7714DFA9E4D00321CB2E784510638A592C9EDDBFDC9D603B03BE93E`,
   raw Git blob
   `f85c5e9e45e73d6ba966c647ca85c834d01bfa82`.
6. `workflow/handoffs/luna-0-luna64-r4.3-corrective-supervisor-a6-r2-owner-reconciliation-r1-20261011.md`
   — this reconciliation proposal, exact checkout SHA-256 and Git blob to
   be recorded in its pre-stage identity manifest.
7. `workflow/handoffs/luna-0-independent-review-luna64-r4.3-a6-r2-owner-reconciliation-r1-20261011.md`
   — the independent A–D review, exact checkout SHA-256 and Git blob to be
   recorded in the same pre-stage identity manifest.
8. `workflow/handoffs/luna64-r4.3-a6-r2-owner-reconciliation-r1-manifest-20261011.json`
   — reconciliation identity manifest. Its own checkout SHA-256 and Git
   blob cannot be stored inside itself; the independent publication
   reviewer must verify and record that one self-identity externally in the
   review handoff.

Commit 1 stages all eight listed paths, including the reconciliation
proposal, independent review, and manifest. None of items 6–8 is deferred
to commit 2. Commit 2 changes only item 2; commit 3 changes only item 8.

Before staging, the independent publication reviewer must verify all seven
non-self path identities against the actual checkout bytes and raw Git
blobs and record them in the reconciliation manifest. The manifest's own
checkout SHA-256 and raw Git blob must also be independently verified and
recorded externally, not embedded in that manifest; it is the sole
self-reference exception. No ellipsis may remain in any recorded identity
or in the staged or committed manifest, review, or final report.

Only after the package commit is published and verified may a second commit
change `workflow/docs/luna/LUNA_WORKFLOW.md`, add the reconciliation closure,
and nothing else. Its complete UTF-8 checkout bytes, SHA-256, staged Git
blob, committed Git blob, and tree must be independently checked before
commit; the workflow closure links the package and review identities.

Because a commit cannot contain its own commit SHA, a third, manifest-only
commit is required after the second commit is verified. It may update only
`workflow/handoffs/luna64-r4.3-a6-r2-owner-reconciliation-r1-manifest-20261011.json`
and must record the package and workflow-closure commit/tree IDs, the
workflow closure checkout SHA-256 and committed Git blob, remote ref and
fetched ancestry, plus final hashes for all package files. The package-stage
manifest must mark the future workflow closure and this final identity
recording as not yet published; the third commit replaces it with the
completed record. The final manifest's own checkout SHA-256, Git blob,
tree, and commit are reported externally in the final handoff because a
manifest cannot contain its own final identity.

The independent publication reviewer must check the staged path set and
byte/blob correspondence separately before each commit. Review cached diffs
and exact path sets for all three commits; verify frozen R4.3 and Luna-63C
identities remain unchanged. Any unexpected path, normalization, identity,
ancestry, or remote mismatch blocks publication. Push/fetch ancestry and
every committed blob hash must be verified before reporting publication.
Do not rewrite or regenerate the protected R2 proposal, review, or manifest
to describe D7/D8; this reconciliation is a separate successor record.

If a reviewer blocks, leave the R2 artifacts and this reconciliation
unpublished, preserve all local evidence, and report the exact unresolved
finding. Do not proceed to A7 or any execution.

## 8. Validation and execution status

Observed for this reconciliation:

- The stated R1 HEAD/upstream and ancestry match.
- The Git index contains no staged changes at reconciliation start.
- The four supplied R2 candidate checkout SHA-256 values match exactly.
- The R2-specific Git attributes are path-scoped `-text`; repository-wide
  `text=auto` remains unchanged.
- Required frozen/R1/A1-A5 commit objects exist and are ancestors of the R1
  closure.

Not executed:

- No VM or infrastructure diagnostics or changes.
- No COM/pipe, systemd/cgroup, filesystem, quota, Job Object, watchdog, or
  termination test.
- No qualification case, supervisor, corrective focused test, or scientific
  workload.
- No runtime efficacy inference.

The original corrective allowance remains **unused and separate**. The
parent A6 R2 remains **BLOCKED — ENFORCEMENT DESIGN INCOMPLETE**. The
original scientific pilot remains **NOT SUPPORTED AS A PROTOCOL-COMPLIANT
PILOT**, not an efficacy result. No scientific rerun is authorized.

## 9. References

- [A6 R2 proposal](luna-0-luna64-r4.3-corrective-supervisor-a6-r2-20261012.md)
- [A6 R2 independent review](luna-0-independent-review-luna64-r4.3-corrective-supervisor-a6-r2-20261012.md)
- [A6 R2 manifest](luna64-r4.3-a6-r2-20261012-manifest.json)
- [R1 owner-policy reconciliation](luna-0-luna64-r4.3-corrective-supervisor-a6-owner-reconciliation-r1-20261011.md)
- [R1 independent review](luna-0-independent-review-luna64-r4.3-a6-owner-reconciliation-r1-20261011.md)
- [R1 manifest](luna64-r4.3-a6-owner-reconciliation-r1-manifest-20261011.json)
- [Original corrective authorization](luna-0-authorization-luna64-r4.3-corrective-implementation-20261010.md)
- [Luna-63C isolation authorization](luna-0-luna63c-mechanism-authorization-20261009.md)
