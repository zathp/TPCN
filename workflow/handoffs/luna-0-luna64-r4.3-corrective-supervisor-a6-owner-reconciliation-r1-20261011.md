# Luna-0 — Luna-64 A6 Owner-Policy Reconciliation R1

**Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6-OWNER-RECONCILIATION-R1`  
**Disposition:** **A6 OWNER-POLICY RECONCILIATION VERIFIED — QUALIFICATION DESIGN MAY PROCEED**  
**A6 technical verdict:** **BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE**  
**Scope:** Governance-only reconciliation of six owner decisions. No supervisor, qualification harness, infrastructure control, corrective test, or scientific workload was implemented or executed.

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-64 A6 owner-policy reconciliation R1"
  task_id: "L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6-OWNER-RECONCILIATION-R1"
  component: "Experimental execution governance"
  status: "complete"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "b758b411e568b41c516228e7d3bdff26058114cc"
  result_revision: "Recorded by R1 governance publication"
  dependencies:
    - "Frozen R4.3 protocol and original corrective authorization"
    - "Published A1-A5 blocked findings"
    - "A6 proposal, evidence and independent review"
    - "Owner policy decisions D1-D6 supplied in the 2026-10-11 task conversation"
  owner: "Repository owner"
  classification:
    - "GOVERNANCE ONLY"
    - "QUALIFICATION DESIGN ONLY"
    - "NO INFRASTRUCTURE CHANGE AUTHORITY"
    - "NO QUALIFICATION EXECUTION AUTHORITY"
    - "NO CORRECTIVE OR SCIENTIFIC EXECUTION AUTHORITY"
  hypothesis: "The explicit D1-D6 decisions resolve policy prerequisites sufficiently to continue design, while technical enforcement remains unqualified."
  counter_hypothesis: "A decision is missing, the evidence/provenance conflicts with the frozen boundary, or the decisions are incorrectly treated as runtime authorization."
  interfaces_relied_on:
    - "R4.3 frozen protocol and corrective owner authorization"
    - "Windows Hyper-V host and Ubuntu systemd/cgroup v2 candidate"
    - "Host-controlled, non-network host-guest control requirement"
    - "Bounded artifact accounting requirement"
  label_information_boundary:
    - "Qualification design must use synthetic controls only; no scientific records, labels, model data, or task payloads."
  timing_assumptions:
    - "The accepted 100 ms, 1 s, 9 s, 170 s, 171 s and 180 s values remain unverified design targets, not guaranteed bounds."
  reset_boundaries:
    - "Any future qualification has a separate one-shot identity and allowance; it cannot reset or consume the parent corrective authorization."
  resource_bounds:
    - "The 12-case / 240 guest CPU-second / 600-second wall / 768 MiB outer-memory / 6 MiB evidence / one-start / one-TurnOff / zero-retry allowance is accepted for planning only."
  authorized_scope:
    - "Read-only source and provenance reconciliation"
    - "Recording owner decisions D1-D6"
    - "Independent governance, resource-policy, and infrastructure/provenance review"
    - "Governance publication if independent review passes"
  unauthorized_scope:
    - "Creating or running a supervisor or qualification harness"
    - "Changing host or guest infrastructure"
    - "Running corrective tests or scientific workloads"
    - "Using or altering Luna-63C records"
    - "Changing the frozen protocol or A6 technical verdict"
  controls:
    - "Exact predecessor commit and SHA-256 checks"
    - "A6 candidate artifacts preserved byte-for-byte"
    - "R1 allowance and parent corrective allowance kept separate"
    - "Explicit D6 denial of infrastructure-change authority"
  measurements:
    - "Repository commit/object, checkout SHA-256, and Git attribute observations"
    - "Documented resource-policy arithmetic and semantics"
  information_boundary_check:
    - "No scientific execution, data, labels, or Luna-63C artifact access."
  hardware_mapping:
    - "Hyper-V/systemd/cgroup isolation only; no hardware-equivalence claim."
  architecture_invariants_touched:
    - "No A01-A15 computation or learning invariant is changed."
  preserves:
    - "Frozen R4.3 and original corrective authorization"
    - "Reject-only malformed second-origin policy"
    - "A1-A5 findings and A6 technical BLOCKED verdict"
    - "Original pilot NOT SUPPORTED verdict"
    - "Unused corrective allowance"
    - "Luna-63C isolation"
  architecture_change: false
  proposal: null
  files_changed:
    - ".gitattributes: path-scoped byte-preservation rules only"
    - "R1 owner-policy reconciliation"
    - "R1 identity manifest"
    - "R1 independent review"
    - "LUNA_WORKFLOW.md R1 closure entry"
  tests_added: []
  tests_passing:
    - "Predecessor identity, commit existence, and ancestry checks"
    - "A6 raw checkout hashes matched supplied expected identities"
    - "Independent read-only R1 reviews"
  tests_failed: []
  tests_not_run:
    - "All infrastructure changes and systemd/cgroup/Hyper-V controls"
    - "All qualification cases"
    - "All corrective tests"
    - "All scientific workloads"
  assumptions:
    - "D1-D6 are owner decisions as explicitly supplied in the current task conversation; they are not inferred from technical review."
  unresolved:
    - "Authenticated non-network control transport is not selected or qualified."
    - "CPU and wall termination bounds are not proved."
    - "No simpler existing filesystem primitive is established to enforce the frozen aggregate logical high-water byte cap."
  recommended_next_agent:
    - "Luna-0: complete design-only alternatives analysis and independent prereview for a separately authorized qualification request; do not execute."
```

## 1. Purpose, authority and evidence labels

R1 records the repository owner's D1-D6 policy decisions supplied in the
2026-10-11 task conversation. This is the authority for the decisions below;
the decisions are not inferred from host diagnostics, operating-system
documentation, or an independent reviewer. The repository does not contain a
signed or separately authenticated owner statement, so provenance is stated
as the owner authorization supplied in that conversation.

Evidence labels:

- **OBSERVED (repository):** commit-object, ancestry, file-byte, and Git
  attribute checks performed against the checkout.
- **OWNER-SUPPLIED:** diagnostics and policy decisions supplied by the owner;
  not independently re-executed.
- **DOCUMENTED / ANALYTICAL:** interpretation of documented interfaces or
  policy arithmetic; not a runtime enforcement observation.
- **PROPOSED / UNQUALIFIED:** candidate controls and thresholds for future
  design and qualification; not deployed and not approved for execution.

R1 supplements A6 only. It does not edit, replace, approve, or turn any A6
candidate into an enforcement result. The A6 technical verdict remains
**BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE**.

## 2. Verified predecessor identities

| Record | Verified identity and retained status |
|---|---|
| R4.3 content freeze / governance closure | `64a214e310de3b982b90a8ad215598bc1e9f8b1c` / `ea1b10456cbf4ca726e473076d239a4f6e53b9c7` |
| R4.3 manifest | SHA-256 `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B` |
| Corrective authorization | Commit `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a` |
| A1 / A2 / A3 | `d20aab249e42575ccc571c9c72153a3bb4b412db` / `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c` / `8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0` — all prior blocked results retained |
| A4 package / closure | `7bd440565c38dee81ace3606fde3fb686de6a0ef` / `f86c25844a4863ac57cd6634f364c28bcf2f511f` — blocked |
| A5 package / workflow closure | `12f84a41fe7c91c17c5df8e975fce24efbadf9ad` / `b758b411e568b41c516228e7d3bdff26058114cc` — **BLOCKED — A5 QUALIFICATION INCOMPLETE** |
| A5 proposal / review | SHA-256 `5BCDAC72E7EBDEA777E9964F25554834C4460D97075E6871690BD441BA00C6E5` / `54D11A362EDED451292330C6FA5627B570BD6103ADE0F69E115F5CDC3C7B934D` |
| A6 proposal / evidence / integrated review | SHA-256 `AD952D9AB7656313D03E0E58BF48469D420B74C5E9CB6BA6738915AA0D34C4C4` / `CB4FA2BBB72DFD1371312641A101F3F5E77A1BDF99540521EE366069AED0C7AE` / `500611264036C1602D280294030F1459FFA817C8DB1CE64AE4E1F4F8E28DB405` |
| A6 pre-R1 workflow candidate | SHA-256 `58C46144B8546AD82739880AF4FB75DC23A171103E4DB2AA610F8FD9A5394BAA` |

All listed commits exist locally; A5 package commit is an ancestor of the
current baseline. The A6 raw checkout files matched their supplied SHA-256 identities before R1
edits. Their original checkout bytes are retained unchanged in the R1
package. Git initially normalized CRLF checkout bytes under `text: auto`;
R1 adds path-scoped `-text` rules for the three immutable A6 files and the
three R1 handoff artifacts, preserving the exact reviewed bytes in Git
objects without changing the repository-wide conversion policy. The
workflow file remains governed by the existing `text: auto` rule; its
checkout materialization and Git-object identity are recorded separately.
The R1 manifest lists each included file and records the immutable A6
checkout SHA-256 and Git-object SHA-1 identities separately.

The frozen scientific protocol, original corrective authorization, accepted
reject-only malformed second-origin policy, original pilot **NOT SUPPORTED**
verdict, unused one-shot corrective allowance, A1-A5 blocked findings, and
Luna-63C isolation remain unchanged. A6's `130.1` CPU-second and staged
termination values are design candidates, not established hard limits.

## 3. Owner decisions recorded

| Decision | Owner policy decision | R1 interpretation and boundary |
|---|---|---|
| D1 — memory | Approves replacing the Windows working-set metric with Linux cgroup-accounted memory **for qualification design only**. | Candidate `MemoryMax=512M`, effective `memory.max=536870912`, `MemorySwapMax=0` / `memory.swap.max=0`. This is materially different from Windows aggregate peak working set. No deployment, qualification, or corrective execution follows. |
| D2 — CPU and wall targets | Accepts the proposed `130.1` guest CPU seconds and the `170/171/180`-second wall stages as unverified design targets. | They are not guaranteed deadlines or enforcement evidence. Bootstrap and termination accounting must remain explicit; overshoot or uncertain termination fails closed. |
| D3 — artifact controls | Evaluate simpler artifact-containment alternatives before considering custom FUSE. | No FUSE filesystem/daemon may be created under R1. No allocated-block or post-run size proxy silently replaces the logical-byte requirement. |
| D4 — qualification budget | Accepts the proposed qualification allowance for planning only. | Not an executable grant and does not consume, replace, or replenish the unused parent corrective allowance. |
| D5 — host/guest control | Requires authenticated non-network control. | Must bind messages and commands to the exact VM identity, resist workload-controlled command forgery, retain auditable evidence, and fail closed on channel failure. Network disconnection or Hyper-V feature availability alone is insufficient. |
| D6 — infrastructure | Infrastructure changes are not authorized. | No services, units, filesystems, endpoints, packages, VM settings, or supervisor may be installed, changed, started, or tested. Any future change needs an exact allowlist, resource budget, independent prereview, and new explicit owner authorization. |

## 4. Reconciliation of A6 findings

| A6 finding | R1 effect | State after R1 |
|---|---|---|
| Linux memory metric requires owner decision | D1 supplies the policy choice for design. | **Policy resolved for design; enforcement and qualification not run.** |
| CPU lifetime limit and response margin lack proven bounds | D2 accepts the proposed target but not its guarantee. | **Still unresolved; target is not a hard ceiling.** |
| Wall-time stop and confirmed VM-Off latency lack proven bounds | D2 accepts the staged timing targets but not their guarantee. | **Still unresolved; targets are not termination bounds.** |
| Aggregate logical-byte artifact containment and frozen test compatibility unresolved | D3 directs comparison of simpler controls first. | **Still unresolved; no method adopted or qualified.** |
| Separate qualification allowance lacks approval | D4 accepts it for planning only. | **Planning authorization only; no qualification authority.** |
| Authenticated offline host/guest command and evidence channel absent | D5 makes this a mandatory requirement. | **Still unresolved; no transport selected, implemented, or tested.** |
| Infrastructure modifications require authorization | D6 expressly denies that authority. | **No changes authorized.** |

**Reconciled result:** owner policy choices suffice to continue a bounded,
design-only analysis. They do not close A6 enforcement blockers, approve an
enforcement implementation, authorize qualification execution, or authorize
the parent corrective work.

## 5. Candidate resource policy and proof obligations

### 5.1 Memory policy — D1

The candidate service configuration is:

```ini
MemoryAccounting=yes
MemoryMax=512M
MemorySwapMax=0
```

The admission check must independently read back:

- `memory.max` exactly `536870912` bytes;
- `memory.swap.max` exactly `0`;
- the effective properties on the dedicated workload cgroup and every
  controlling ancestor;
- the systemd unit's effective memory settings before any workload process
  can execute.

The measured metric is cgroup v2 charged memory for the controlled subtree,
not aggregate Windows process-tree peak working set. `memory.current`,
`memory.peak`, and the before/after deltas in `memory.events` (`max`, `oom`,
`oom_kill`, and `oom_group_kill`, where available) must be captured by a
trusted monitor. Candidate policy treats any OOM event, limit-hit event,
counter-read failure, unexplained discontinuity, or limit mismatch as a
failed qualification case and rejects its evidence. Descendant processes are
covered only while they remain in the measured cgroup subtree; migration,
delegation, or cgroup escape must be prevented by root-managed controls and
tested.

`MemorySwapMax=0` limits swap accounting charged to the cgroup; it is not a
proof that all forms of host or guest overcommit are impossible. The
qualification must inspect actual swap configuration and counters and must
not infer no-overcommit from this setting alone. These are proposed checks,
not deployed settings or runtime results.

### 5.2 Cumulative CPU policy — D2

The accepted design target is `130100000` microseconds of aggregate guest
CPU charged to one pre-created, dedicated parent cgroup, comprising the
original 120-second corrective ceiling plus a disclosed 10.1-second
termination reserve. Before any process is admitted, a trusted root-side
admission component verifies that the parent cgroup is fresh and empty,
records its initial `cpu.stat` `usage_usec`, and confirms its effective
limits. The host records QPC `T0` immediately before requesting service
activation. The measured CPU value is the parent-cgroup `usage_usec` delta
from that pre-admission baseline until the complete child subtree is empty
and the final counter is read. No process may execute workload or monitoring
code before the baseline is sealed.

The measured cgroup must contain the guest monitor, supervisor bootstrap,
every corrective child and descendant, and guest cleanup that runs before
cgroup emptiness. Their CPU is included from first admission through
termination. R1 does not authorize or assume an artifact mediator, including
FUSE; if a separate artifact-accounting component is selected under a later
authorization, its CPU must also be included in this budget or explicitly
charged to an independently approved resource allowance. PID 1's
service-activation work, guest VM boot, host
controller/watchdog CPU, and host-side VM-off CPU are outside this cgroup CPU
metric and must be separately logged; they are not silently counted as zero.
The guest and host timing clocks still include their declared wall-time
stages. No workload-controlled process may run outside the measured cgroup;
an escaped or unaccounted process is containment failure. This explicit
scope is a proposed accounting boundary, not a measured resource guarantee.

The trusted guest monitor is outside the workload's write permissions and
reads cumulative `cpu.stat` usage for the complete, non-delegated workload
subtree. Candidate effective affinity is one guest CPU. Polling targets
100 ms. At or above 120,000,000 usec it requests `cgroup.kill`; at 1 second
after the request, a still-populated cgroup triggers the external host
controller's immediate VM-off request. The absolute 130,100,000-usec target
is a stop-and-fail boundary, not permission to silently overshoot.

**Analytical limitation:** one vCPU limits execution rate but does not bound
scheduler delay, monitor starvation, cgroup-kill completion, control-channel
delay, host scheduling, VMMS response, or confirmed VM-Off. The sum
`0.1 + 1 + 9 = 10.1` seconds is therefore a conditional planning calculation,
not a proven worst-case CPU margin. Counter failure, stale monitor, escape,
failed termination request, missing completion confirmation, or CPU use
above the accepted absolute target is containment/boundary failure and
invalidates the run. Independent qualification must measure and stress the
controls but cannot by itself prove an unconditional operating-system
deadline.

### 5.3 Wall-time policy — D2

The host-side `QueryPerformanceCounter` (QPC) is the proposed monotonic
authority. `T0` is recorded immediately before the host requests activation
of the already booted, preconfigured qualification service. The service
startup, guest supervisor/bootstrap, synthetic cases, cleanup, evidence
flush, and termination are included through independently confirmed VM Off.
VM boot and provisioning are outside `T0` and must remain separately
bounded and recorded. The watchdog is host-controlled and remains outside
the guest workload.

| Candidate time | Action |
|---|---|
| `T0 + 170 s` | Request immediate guest workload-cgroup termination; record request time. |
| `T0 + 171 s` | If the workload is populated, the heartbeat is stale, or guest confirmation is unavailable, request host `Stop-VM -TurnOff` for the exact VM ID. |
| `T0 + 180 s` | Latest accepted target for confirmed VM Off and sealed evidence. Unknown or later state is termination failure and evidence rejection. |

At normal early completion, verify the workload cgroup is empty, seal guest
artifacts, request shutdown, and allow at most five seconds before issuing
the same host emergency power-off request. A host API return is not
confirmation; the host must read the exact VM ID as `Off` twice with a
scheduling turn between checks. If the request fails or Off is not confirmed,
record termination failure; do not retry the experiment or treat the
unconfirmed VM as safely stopped.

QPC monotonicity does not guarantee scheduler or Hyper-V response latency.
The stage values remain unverified targets, not a guaranteed 180-second
cessation bound. Qualification must preserve raw request/acknowledgement and
VM-state timestamps and classify missing evidence as failure.

### 5.4 Artifact policy — D3

The controlling policy requirement remains the frozen **aggregate logical
high-water file-length cap of 5,242,880 bytes** across stdout, stderr,
JSONL traces, direct temporary fixtures, failure records, and export staging.
The A6 candidate divides it into 5,177,344 workload bytes plus a protected
65,536-byte failure-evidence reserve, and caps the namespace at 512 inodes.
Charges are per-inode maximum logical `st_size` reached; sparse holes count,
and truncation/unlink does not refund credit. Filesystem metadata is outside
that logical-payload metric but must fit in a separately bounded backing
volume. These are candidate accounting semantics, not qualified controls.

| Simpler candidate | Useful containment | Why it does not yet prove the required cap |
|---|---|---|
| Read-only root/source plus a private mount namespace | Restricts paths and removes unintended writable mounts when every descriptor and mount is controlled. | Does not itself bound writes through the allowed output mount or inherited descriptors. |
| One fixed-size dedicated ext4 volume with a strict inode limit and project/user quota | Bounds backing capacity and allocated blocks; can place all temporary/output paths in one namespace. | Filesystem quotas account allocated blocks, not aggregate logical high-water `st_size`; sparse files, holes, unlink/recreate, and metadata semantics do not match the cap. |
| `tmpfs` with size and inode limits | Provides a bounded volatile filesystem and can centralize temporary paths. | Bounds resident allocation, not necessarily aggregate logical file lengths; sparse/truncate semantics and cgroup memory pressure remain distinct from the 5 MiB measure. |
| Per-process `RLIMIT_FSIZE` | Limits an individual file's growth per process. | Not an aggregate cap across many files or descendants. |
| Post-run size scan (`du`, `stat`, or export check) | Detects some final-state overages. | Is not hard pre-write enforcement and cannot recover deleted/high-water outputs. |

All writable paths, including direct `mkdtemp(os.tmpdir())` and `writeFile()`
calls in the frozen tests, must be in the enforcement domain. Restricting only
one output directory is insufficient. Do not change the frozen tests to
accommodate a proposed storage mechanism under R1. No evaluated stock
filesystem primitive has yet been shown to enforce the required aggregate
logical high-water semantics. D3 therefore requires alternatives analysis
first; custom FUSE remains only a possible later candidate, not selected or
authorized. If exact aggregate logical-byte enforcement requires a changed
accounting policy or frozen-test modification, that conflict requires a
separately reviewed proposal and explicit owner decision before any
qualification.

## 6. Trusted boundary and authenticated offline control

| Component | Candidate trust status | Required boundary |
|---|---|---|
| Windows host administrator, Hyper-V/VMMS, QPC watchdog | Trusted and outside workload influence. | Bind every control action to VM ID `60e9baef-706e-4490-80d7-38618710546e`; restrict authority to the one approved VM and record monotonic timestamps. |
| Host-guest control channel | Trusted control path only after selection and authentication. | Non-network, authenticated, integrity-protected, VM-bound messages; no generic command execution; reject replay, wrong identity, stale sequence, and malformed control; fail closed on loss. |
| Ubuntu kernel, systemd PID 1, root provisioner | Trusted enforcement base. | Install effective limits before workload admission; keep cgroup and mounts non-delegated; workload cannot modify limits, mount namespaces, or move itself. |
| Guest resource monitor / artifact mediator | Trusted enforcement components, separate from workload credentials. | Observe and control the complete workload subtree; preserve raw evidence; run no scientific command; any monitor or ledger fault fails closed. |
| Corrective tests and all descendants | Untrusted. | No root, capabilities, network, writable cgroup, host shares, or unmediated writable path; no ability to signal or reconfigure trusted components. |

The owner-supplied disconnected NIC and disabled Guest Service Interface are
observations, not proof of a secure control channel. Host shutdown integration
may provide a host-originated shutdown path but does not establish an
authenticated guest-to-host heartbeat or evidence channel. Hyper-V sockets,
virtual serial, and other non-network mechanisms are only candidates for
read-only design comparison; none is selected, enabled, or claimed available.
Their identity binding, ACLs, channel ownership, replay protection, failure
semantics, and host API behavior must be independently reviewed before any
future authorization.

## 7. Proposed qualification allowance — planning only

D4 accepts this separate proposed allowance for planning; it is **not an
execution grant**:

| Resource / count | Aggregate ceiling |
|---|---:|
| Synthetic qualification cases | 12; each exact case declared before authorization, no retries |
| Guest CPU | 240 CPU seconds total |
| Wall time | 600 seconds total, host monotonic clock |
| Outer memory | 768 MiB (`805,306,368` bytes) maximum |
| Combined payload and evidence | 6 MiB (`6,291,456` bytes) maximum |
| VM starts | 1 |
| Host `Stop-VM -TurnOff` | At most 1 |
| Retry/restart/replay | 0 |

The allowance is separate from the unused parent corrective allowance and
must not be charged to it. Its 240 guest CPU-second total is proposed for
the aggregate synthetic workload cgroup, measured from a fresh, empty
baseline through its final empty-cgroup counter read. Host-side CPU and guest
PID 1/VM-boot CPU are recorded separately and are not silently reported as
part of that total; before any future execution, the owner must confirm this
scope or explicitly amend the budget to cover those excluded activities.
The other D4 values are also planning ceilings, not complete executable
measurement contracts:

- **Wall time:** candidate origin `Q0` is host QPC immediately before the
  single VM-start request; the proposed 600 seconds would include boot,
  qualification setup, all cases, cleanup, evidence sealing, and confirmed
  VM Off. The owner and independent prereview must confirm this origin and
  scope before any execution; no pause or reset is permitted.
- **Outer memory:** 768 MiB (`805,306,368` bytes) is the numeric planning
  ceiling, but the measured object, memory metric, boot/host boundary, and
  hard enforcement mechanism are not selected. They must be specified and
  approved before execution; no cgroup or working-set equivalence is
  inferred.
- **Combined payload/evidence:** the 6 MiB (`6,291,456` byte) value is one
  combined planning ceiling, not an additional reserve. The aggregate
  accounting metric (logical high-water bytes versus allocated storage),
  failure-evidence allocation, and complete writer set remain to be
  specified and approved. No post-run scan is accepted as hard enforcement.
- **Test identities:** R1 does not authorize a particular set of 12 cases.
  A future request must list each synthetic case, exact command/entry point,
  order, resource allocation, and failure behavior before approval.

Synthetic cases may address only admission and
cgroup containment, descendant inheritance, memory/swap control, cumulative
CPU cutoff, wall cutoff, artifact accounting and alternate write paths,
monitor/supervisor failure, host emergency termination, one-shot behavior,
and evidence integrity. Cases must be fixed and ordered before any new
request; an emergency VM-off ends the session, and no later case or retry is
permitted. No R4.3 validator, frozen corrective test, benchmark, training,
labels, scientific workload, or Luna-63C data may be invoked.

Before an executable request, the case list must allocate the 12 slots and
budget among these controls, state whether failure injection consumes the
single permitted TurnOff, account all bootstrap/monitoring CPU and output,
and prove that the failure-evidence reserve fits inside the 6 MiB combined
payload/evidence ceiling. This R1 does not silently invent per-case limits or
authorize a pilot.

## 8. Proposed future infrastructure allowlist — not authorized

This section is a proposal to make the next owner decision concrete. It
authorizes **no** current change. If a new request is approved, its exact
allowlist should be limited to:

1. A new synthetic-only repository subtree,
   `workflow/experiments/luna64-a6-r1/`, containing only the qualification
   controller, guest service/monitor configuration, synthetic test inputs,
   and evidence schema explicitly named in that later authorization.
2. A host controller identity restricted to the single recorded VM GUID,
   with only the exact start, status, authenticated-control, and one
   emergency-turnoff operations named in the approved test plan.
3. A single dedicated systemd qualification unit and its separately
   identified monitor under `/etc/systemd/system/`, one non-delegated
   workload slice, and the specific cgroup settings authorized after
   independent prereview.
4. One read-only source mount and one restricted artifact mount in a private
   namespace. A filesystem image, quota, mount, or mediator may be created
   only after the logical-cap alternatives are resolved and the exact
   device/image identity and capacity appear in the later authorization.
5. At most one non-network host-guest control endpoint, but only after the
   transport, ACL, peer authentication, VM binding, message format, and
   failure behavior are selected and prereviewed. R1 does not grant permission
   to enable or configure any endpoint.
6. The 12 synthetic cases and evidence destinations explicitly enumerated in
   the later authorization; no other repository paths, VM settings, packages,
   user accounts, services, storage, networking, or Luna records.

The endpoint type and artifact enforcement method remain intentionally
unselected because the current evidence does not establish that either is
feasible and secure. The allowlist above is therefore a design boundary, not
a complete executable change list. The next owner authorization must identify
the exact transport and storage implementation or explicitly stop the
qualification design. No generic privilege or discretionary change authority
is implied.

## 9. Authorization state and next gate

**Owner policy choices:** recorded as supplied (D1-D6).  
**Qualification design:** may proceed in read-only analysis only.  
**Infrastructure modifications:** not authorized (D6).  
**Qualification execution:** not authorized (D4 is planning only).  
**Corrective implementation/execution:** not authorized by R1.  
**Scientific execution or efficacy claim:** not authorized.  
**A6 technical status:** **BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE**.  
**Original pilot:** **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**; not an
efficacy result.  
**Luna-63C:** remains isolated and unchanged.

The smallest next step is a read-only, independently prereviewed design
submission that selects and specifies (a) an authenticated non-network
host/guest channel, (b) a feasible exact logical-byte enforcement method
compatible with the frozen direct temporary-file behavior, and (c) honest
CPU/wall failure bounds or an explicitly revised policy. Any subsequent
infrastructure change or qualification execution requires a separate,
exactly scoped owner authorization. A6 does not automatically advance to A7.

## 10. Validation and publication record

R1 validation is limited to the predecessor commit/ancestry checks, supplied
A6 checkout-hash reconciliation, independent read-only review, document and
manifest validation, and exact publication-byte verification. No host or
guest command, infrastructure change, qualification case, corrective test,
or scientific workload is run.

The companion [R1 identity manifest](luna64-r4.3-a6-owner-reconciliation-r1-manifest-20261011.json)
records inputs, expected checkout identities, source attributes, and the
publication inventory. The independent review is recorded in
[R1 independent review](luna-0-independent-review-luna64-r4.3-a6-owner-reconciliation-r1-20261011.md).
