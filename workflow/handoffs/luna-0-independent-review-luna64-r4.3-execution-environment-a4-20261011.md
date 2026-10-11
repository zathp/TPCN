# Luna-0 Integrated Independent Review: Luna-64 A4

**Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A4`

**Integrated verdict:** **BLOCKED - ISOLATION QUALIFICATION UNRESOLVED**

**Scope:** Independent, read-only technical, scientific-compatibility, resource,
artifact, Hyper-V, and governance review of the A4 proposal. No guest command,
VM start/stop/configuration, installation, qualification, corrective test, or
scientific workload was run or authorized.

## 1. Exact reviewed package and ancestry

| Artifact | Reviewed checkout SHA-256 |
|---|---|
| [A4 proposal](luna-0-luna64-r4.3-corrective-supervisor-amendment-a4-20261011.md) | `BEF21B2E2E4005383657E490A05AAB57D59FCA1C716AEAAD7116724991B0D165` |
| [A4 evidence](luna64-r4.3-execution-environment-a4-evidence-20261011.json) | `660A9077886F1D99B94F1CB17BAD34A20BA89989E30434405B9F533F0D8BFDA6` |

The reviewed files are the exact checkout materializations above; publication
Git objects and commit IDs are reported by the subsequent governance closure,
not self-embedded in these artifacts.

| Predecessor | Identity and result |
|---|---|
| R4.3 content freeze | `64a214e310de3b982b90a8ad215598bc1e9f8b1c` |
| Freeze governance closure | `ea1b10456cbf4ca726e473076d239a4f6e53b9c7` |
| R4.3 manifest | SHA-256 `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`, Git blob `d1993728e53fff2cdec712607012786bfeba3fb2` |
| A1 | `d20aab249e42575ccc571c9c72153a3bb4b412db` - **BLOCKED** |
| A2 | `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c` - **BLOCKED** |
| A3 | `8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0` - **BLOCKED - NO QUALIFIED EXECUTION ARCHITECTURE** |
| Corrective gate | SHA-256 `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369` |
| Corrective owner authorization | `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a` |
| Original pilot closure | `515dde66f37ca67c44a39f02e13f2e59b2f10d1d` - **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not an efficacy result |
| Corrective worktree | `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`, clean, corrective branch |

The local governance HEAD and live remote governance ref matched A3 at
`8ca543aa6e6e356de6a08edc1ba5c56fb540f9d0` during this review. Freeze,
closure, corrective authorization, A1, and A2 are ancestors of that baseline.
The current manifest checkout hash matches the frozen manifest identity and
all ten current package files match the manifest's raw SHA-256 entries. The
32-entry inventory checksum is
`D507293DAAC22E353CB47ABC813726B70A832F5BD0A5462F2BEB4FB76850B2D8`.
The prior A3 independent post-publication attestation reconciles all 32 raw
and Git identities (26 unchanged object IDs and six exact-byte remappings);
A4 preserves that mapping rather than rewriting or claiming a new independent
remote re-audit of every entry.

The A2 discrepancy is preserved: its review record reports proposal hash
`E00B75004D3085EFDA60D7163D57153F2FCB2D089162574358794BBA54145591`, whereas
its published proposal hash is
`9FAF922016726FBB5B1EAEBBC8B9488A293E99FC830738E02F3A9A9CD7D958AD`;
the distinct checkout hash is
`05C401518A74B1957697E6F12C8877E4D9F8F734A4A7B1432CDF3C9520AE835A`.
Reconstruction is not exact-byte approval. A1/A2 and A3 remain historically
blocked; A4 does not amend or retroactively revise their findings.

## 2. Independent review scopes

Six separate read-only Luna-0 Architecture Guardian reviews were integrated.
Their detailed responses are retained in the review conversations; their
scope-specific dispositions are summarized here.

| Scope | Independent result |
|---|---|
| Governance, provenance and authorization | **BLOCKED**. Reconciled predecessor identities, A2 mismatch, boundaries and unchanged Luna-63C paths; A4 is not owner-approved or published at review time. |
| Linux cgroup v2 / systemd | **BLOCKED** overall. Confirmed the proposed service-vs-scope distinction, rate-vs-total CPU semantics, and memory-metric distinction. Review caught and the A4 proposal corrected: invalid `cgroup.kill` read probe, missing actual-unit/ancestor checks, transient-start/pre-exec ambiguity. The corrected design is not runtime qualified. |
| Hyper-V bootstrap and isolation | **BLOCKED**. VM/guest settings, administrator stop authority, shutdown behavior, vNIC/switch state, integration channels, VHDX attachments and host-side response bounds remain unverified. The proposed trust boundary and console/control start path are design, not observed controls. |
| Resource accounting and stop semantics | **BLOCKED**. Linux cgroup CPU does not include external host bootstrap; no cumulative CPU cutoff or bounded wall-stop completion is demonstrated. Charged memory does not satisfy original working-set semantics. |
| Artifact containment | **BLOCKED**. No verified hard quota, complete logical-byte writer boundary, durable failure reserve, or export limit exists. The clarified arithmetic/intent is not enforcement evidence. |
| Scientific/protocol compatibility | **PASS WITH LIMITATIONS — static compatibility only**. Confirmed the unchanged first frozen test makes 23 planned serial validator CLI descendants in a complete successful pass; no Linux execution or compatibility of the two absent corrective tests was demonstrated. This review is not a qualification PASS. |

The final proposal materialization was confirmed at the exact SHA-256 above.
Clarifications explicitly distinguish a locked, pre-provisioned unit from a
transient unit; check inactive-unit configuration before start and the actual
service cgroup/ancestors before any focused test child; remove `cgroup.kill`
as a required mechanism; define logical artifact/reserve arithmetic; and state
that the A4 qualification proposal replaces rather than adds to A3's
unapproved proposal. Reviewers found these textual corrections consistent
with the documented mechanisms. They are not runtime evidence.

## 3. Technical decision

The proposed candidate is a fixed, pre-provisioned systemd service unit in an
offline Hyper-V Ubuntu guest. No architecture is selected or qualified.

### Platform and bootstrap

**Observed host facts:** Windows 10 Pro `10.0.19045`, Ryzen 7 7700X, about
31.1 GiB RAM, hypervisor present, and VM management services running.
`Get-VM` was denied under the medium-integrity token, so actual VM settings,
power state and host stop rights could not be queried.

**Owner reports only:** Ubuntu 26.04.1, four guest vCPUs, fixed 8 GiB RAM,
128 GB system VHDX, 256 GB archive VHDX, and disconnected guest networking.
These claims, as well as cgroup v2, systemd version/properties, storage/quota,
shutdown integration, switch/NIC and host termination authority, remain
unverified. No guest command was run.

The proposed trusted boundary includes the Hyper-V host administrator/VMMS,
guest kernel, systemd PID 1 and the external service-start control client.
That client and VM boot/login are outside the workload service cgroup. The
proposal does not demonstrate how their CPU is included in the original
whole-invocation budget, nor bounded independent host termination latency if
the guest is stalled. An API or signal request is not proof that all
descendants stopped.

### Resource-policy gaps

- **Memory:** Parent authorization is 512 MiB aggregate peak Windows working
  set. `memory.max=536870912` limits Linux cgroup-charged memory through
  reclaim/OOM behavior; it is not the parent metric. No substitution is
  owner-approved. The parent requirement remains unmet unless retained or
  separately amended by explicit owner approval.
- **CPU:** `cpu.stat` `usage_usec` is an aggregate usage counter;
  `user_usec`/`system_usec` are component/reconciliation counters, not extra
  totals. `cpu.max` is a rate/bandwidth limit, not a lifetime CPU-seconds
  cutoff. The proposed service counter excludes the outside host bootstrap.
  Watcher observation and stop latency have no established worst-case bound.
- **Wall time:** systemd `RuntimeMaxSec=180s`, `TimeoutStopSec` and
  `KillMode=control-group` are stop mechanisms, not proof of cgroup-empty
  termination by an exact wall deadline. Guest pause/kernel/systemd failure
  and host controller/API delay are unresolved.
- **Artifacts:** The parent cap is 5,242,880 bytes; the proposed 65,536-byte
  failure reserve would leave 5,177,344 bytes for ordinary artifacts if
  both are enforced as one logical-byte aggregate. No filesystem quota,
  complete mediation/denial of alternate temp and stdio paths, sparse-file
  behavior, durable reserve, journal bounds, or stopped-VM export limit has
  been verified. Post-run size measurement is not a hard cap; the 256 GB
  archive drive is not a substitute.
- **Descendants:** The proposed service cgroup can preserve the 23 serial
  validator CLI launches, unlike a single-process rewrite, but actual
  containment, inherited limits, ancestors, and termination were not tested.
- **Qualification:** A proposed 12-case, one-invocation qualification budget
  is separate from the scientific budget and the parent corrective allowance,
  and replaces (is not additive to) A3's unapproved provisional qualification
  proposal. It remains unapproved, not executable, and lacks frozen per-case
  record allocation. It does not release the parent corrective allowance.

## 4. Governance and experiment state

- Original pilot remains **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not
  an efficacy result; its 5,184-episode / 20,736-reception scientific budget
  is exhausted.
- Corrective allowance remains unused: one supervisor invocation, three exact
  focused tests, zero retries, 512 combined synthetic records, one CPU,
  120 CPU seconds, 180 wall seconds, 512 MiB aggregate working-set metric and
  5 MiB artifacts.
- The parent corrective marker and A2 qualification marker were rechecked
  absent; the separate corrective worktree was rechecked clean at
  `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`. These observations cannot prove
  absence of unrecorded external execution.
- No A4 qualification, corrective test, scientific rerun, production change,
  architecture promotion, installation, VM modification, or guest command
  occurred.
- Luna-63C code, design, authorization and certificate boundaries are
  unchanged. No Luna-63C artifacts were reused.
- No owner approval for the changed memory metric, A4 qualification budget,
  bootstrap exception, or corrective execution is inferred.

## 5. Verdict and required next gates

**BLOCKED - ISOLATION QUALIFICATION UNRESOLVED.**

The A4 package is a governance proposal, not a qualified architecture or an
execution authorization. Read-only host/guest evidence, actual unit/hierarchy
verification, full-invocation CPU accounting, bounded CPU/wall termination,
hard artifact containment, and explicit owner decisions remain prerequisites.
The original working-set metric cannot be replaced without a distinct,
explicitly approved policy amendment. Any proposed stop grace/overshoot also
requires exact bounds, independent review and owner approval. Qualification
must then receive its own exact authorized budget and independent pre/post
review; PASS would still not consume the parent corrective allowance.

The original pilot verdict/budget, A1/A2/A3 blocked outcomes, A2 provenance
discrepancy, R4.3 freeze and Luna-63C isolation remain unchanged.
Corrective execution and scientific rerun authorization remain **not
released**.
