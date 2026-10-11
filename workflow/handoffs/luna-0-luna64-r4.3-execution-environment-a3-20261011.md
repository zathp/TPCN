# Luna-0 - Luna-64 R4.3 A3 Execution Environment Decision Gate

**Identifier:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A3`

**Decision:** **NO QUALIFIED EXECUTION ENVIRONMENT**

**Disposition proposed for independent review:** **BLOCKED - NO QUALIFIED EXECUTION ARCHITECTURE**

**Scope:** Governance-only architecture comparison. No supervisor, qualification,
corrective implementation, focused test, benchmark, or scientific workload is
authorized or executed. A1/A2 are not adopted by default.

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-64 A3 execution environment decision"
  task_id: "L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A3"
  component: "Experimental execution resource governance"
  status: "blocked"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "a9fbe2158b7858a8bb5523f3730af31dbb7ea81c"
  result_revision: "containing publication commit; reported separately"
  dependencies: ["frozen R4.3", "owner-authorized corrective gate", "A1 and A2 blocked records"]
  owner: "Repository owner"
  classification: ["GOVERNANCE ONLY", "NO EXECUTION AUTHORIZATION"]
  hypothesis: "Not applicable; no scientific experiment"
  counter_hypothesis: "Not applicable"
  interfaces_relied_on: ["Windows process/job APIs", "frozen Node CLI test", "resource authorization records"]
  label_information_boundary: ["No model input, evaluator truth, training or scientific replay executed"]
  timing_assumptions: ["Host time is not neural time", "No unproved watchdog lateness bound"]
  reset_boundaries: ["Parent marker remains absent and must not be reset"]
  resource_bounds: ["Original corrective budget unchanged", "Qualification proposal unapproved"]
  authorized_scope: ["Read-only platform queries", "Documentation research", "A3 governance publication"]
  unauthorized_scope: ["Implementation", "Qualification", "Focused tests", "Scientific workload", "Infrastructure setup"]
  controls: ["Four independent read-only review scopes", "Exact Git and checkout identities"]
  measurements: ["Platform metadata", "File hashes", "Static CLI-call count"]
  information_boundary_check: ["No execution or Luna-63C reuse"]
  hardware_mapping: ["OS capability analysis only; no hardware-equivalence claim"]
  architecture_invariants_touched: ["A01-A03", "A07-A11", "A15"]
  preserves: ["R4.3", "Parent authorization", "A1/A2 blocked verdicts", "Original pilot closure", "Luna-63C isolation"]
  architecture_change: false
  proposal: null
  files_changed: ["A3 decision", "A3 platform evidence", "A3 independent review", "LUNA_WORKFLOW.md A3 entry"]
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: ["All supervisor qualification", "All corrective tests", "All scientific workloads"]
  assumptions: ["API support is not runtime qualification"]
  unresolved: ["Complete pre-start containment", "Strict CPU and wall cutoff", "Output containment", "Owner approval"]
  recommended_next_agent: ["Luna-0: separately authorized environment inventory and resource-policy design"]
```

## 1. Authoritative reconciliation and identity exception

Repository layout is `workflow/`, not the obsolete profile prefix
`tpcn-luna-workflow/` (that directory is absent). The actual contract, changelog,
workflow, acceptance criteria, proposal README/template and handoff template
were inspected. No missing-prefix file is invented as authority.

| Evidence | Identity / observation |
|---|---|
| Content freeze | `64a214e310de3b982b90a8ad215598bc1e9f8b1c` |
| Freeze governance closure | `ea1b10456cbf4ca726e473076d239a4f6e53b9c7` |
| R4.3 manifest SHA-256 | `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B` |
| Corrective gate SHA-256 | `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369` |
| Final gate publication | `439c0c930489ed032dc10950bbd51fe3f153d05a` |
| Corrective owner authorization | `0bdddaeaefe47a97ea6433d82bcc143adfe13b5a`; reject-only second-origin policy approved |
| Original implementation / handoff | `d709c5aab0a841a8dfb193bd26b306d9b4198392` / `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787` |
| Original closure | `515dde66f37ca67c44a39f02e13f2e59b2f10d1d` |
| A1 publication | `d20aab249e42575ccc571c9c72153a3bb4b412db`; BLOCKED |
| A2 publication | `a9fbe2158b7858a8bb5523f3730af31dbb7ea81c`; local HEAD and remote governance ref matched at reconnaissance |
| Corrective worktree | `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna64-r4.3-reward-lifecycle-correction-20261010`, clean at `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787` |
| Corrective branch | `experiment/luna64-r4.3-reward-lifecycle-correction-20261010`; original pilot branch retained separately at the same handoff tip |

Ten frozen manifest file raw hashes match current package bytes. All 32 input
inventory Git identities match the content-freeze objects after applying the
published Stage-B package OID mapping; an initial comparison without that mapping
reported a representation mismatch, not a scientific change. The evolving
workflow's current bytes are not substituted for its frozen inventory identity.

### A2 published versus reviewed bytes

| Artifact | Current CRLF checkout SHA-256 | Published Git blob SHA-256 |
|---|---|---|
| A2 proposal | `05C401518A74B1957697E6F12C8877E4D9F8F734A4A7B1432CDF3C9520AE835A` | `9FAF922016726FBB5B1EAEBBC8B9488A293E99FC830738E02F3A9A9CD7D958AD` |
| A2 policy | `A448646B7B38DE1BE09DC693C20C00DDDEF7C731216C1BE1BD1C462437654E12` | `DCDBA16C8E3A63DCF7FA3A7AE77BDEC8A37CE58BD1CBBA48D6D15CEEE211DACE` |
| A2 schema | `FFAECD55A7BAEA79BF2635AEDC1DE0B0AD62910AB17051308015C85BCF7ADC44` | `FC5CADC7296BD66F32B127BF97ED6549A036516922A3AFE3C3533192D978DD1A` |

A2's review/workflow and preceding final response report proposal hash
`E00B75004D3085EFDA60D7163D57153F2FCB2D089162574358794BBA54145591`.
**That is not the current or published proposal identity.** Reconstructing
the published LF blob as CRLF and adding exactly two trailing spaces to each
header line 3 through 9 yields that reported hash. This identifies a
post-review Markdown hard-break removal as well as checkout normalization.
Reconstruction is metadata analysis, not an independently retained original
review artifact or approval of the published bytes. A2's proposal still says
prereview pending; the separate review records its blocked outcome.

Preserve A2 unmodified. Do not claim its recorded exact-byte review hash matches
publication. A3 independently reviews the actual published evidence with this
exception disclosed. No failed identity is used to release execution.

Both the parent marker and A2 qualification marker under
`%LOCALAPPDATA%\TPCN` are absent. The corrective supervisor, new reference/lifecycle
tests and corrective evidence directory are absent. The original pilot budget is
exhausted at 5,184 episodes / 20,736 receptions, with verdict **NOT SUPPORTED AS
A PROTOCOL-COMPLIANT PILOT**. Repository/marker observations show no retained
corrective execution or consumed allowance; they cannot prove no unrecorded
process ever ran elsewhere.

## 2. Guarantees and policies that cannot be silently substituted

### Scientific invariants (unchanged)

Frozen PCN/readout equations, dimensions, event identities, reward provenance,
TRAIN/EVAL separation, immediate input charging, arms, goldens, statistical
and cost-benefit criteria remain unchanged. Eligibility horizon is inclusive
8 TU; deadline is `A+16000000` ticks inclusive; expiry is `A+16000001`
ticks with expiry precedence; capacity is eight without eviction/truncation.
Delivery is exactly at due time; settlement requires valid captured credit;
duplicates and owner-approved malformed second origins never update twice or
alter the valid first origin. Frozen phase order and canonical ID/child ordinal
ordering are preserved. Host scheduling does not redefine logical event time.

The three primary tests, once each in listed order, are:

1. `node experiments/luna64/test-track-b-gate-r4.mjs`
2. `node experiments/luna64/test-luna64-r4.3-reward-reference.mjs`
3. `node experiments/luna64/test-luna64-r4.3-reward-lifecycle.mjs`

No scientific rerun, benchmark, new experiment identity, production/core, ACP,
architecture promotion or Luna-63C code/evidence change is allowed.

### Original corrective budget (not replenished)

| Requirement | Exact parent policy |
|---|---|
| Supervisor | One `powershell.exe -NoProfile -File experiments/luna64/run-r4.3-corrective-checks.ps1 -Mode All` invocation; no alternative mode or retry |
| Primary tests | Three exact serial child commands above, once each |
| Synthetic data | 512 combined scripted stimuli and emitted trace records, with frozen per-case allocations |
| CPU allocation | One logical CPU, child affinity mask `0x1` verified before resume |
| CPU time | 120 seconds aggregate across entire invocation; A2 interprets/requires user plus kernel, not just user time |
| Wall time | 180 seconds aggregate across entire invocation |
| Memory | 536870912 bytes aggregate peak working set, supervisor plus complete descendant tree |
| Artifacts | 5242880 bytes aggregate test outputs and traces; failures retained within cap |
| One shot | Durable create-new marker before test startup, current-user ACL, at most 4096 bytes; RUNNING/CONSUMED/uncertain states prohibit retry |
| Launch | Suspended process creation, membership/accounting/affinity verification and monitoring before resume |

The gate describes polling and fail-on-breach, not a documented zero-latency OS
barrier for CPU/wall/output. A1/A2 blocked interpretations require enforceable
ceilings. A3 does not reinterpret polling as a strict bound or silently weaken
the prior stop requirement. Any finite lateness tolerance, changed memory/CPU
metric, scope exclusion, process architecture, command allowlist or artifact
accounting requires independent review and explicit owner approval.

## 3. Actual platform inventory (2026-10-11)

Read-only CIM, command/service/registry, feature and quota queries only:

- Windows 10 Pro x64, `10.0.19045`; `HypervisorPresent=false`.
- CPU reports VM monitor extensions, SLAT, and firmware virtualization enabled.
  Hardware eligibility is not proof of installed/runnable Hyper-V.
- `wsl.exe` is present. Docker/Podman executables, Hyper-V `Get-VM`/`Get-VHD`
  commands and `vmms`, `vmcompute`, `LxssManager`, `WslService`,
  `com.docker.service` services were not found in this query context.
- Current-user WSL registration key is absent. `wsl.exe --list --verbose`
  returned installation-oriented usage, not a valid running/installed-distro
  inventory. It launched no distro; don't infer a universal absence of other
  users' distributions or arbitrary remote infrastructure.
- Optional feature queries for Hyper-V, VirtualMachinePlatform and WSL require
  elevation; their enabled/disabled states remain **unknown**, not "disabled".
  An initial array-valued feature query had a parameter error; individual
  queries established the elevation limitation.
- Current token is medium integrity; Administrators group is deny-only.
  C: is NTFS; `fsutil quota query C:` failed with Access denied. Quota state
  is **unknown**, not "off". No feature, quota or privilege was changed.
- No separately administered execution host, credentials, approved preconfigured
  service/job, VM image, container image or dedicated storage boundary is
  established in the inspected authority. No remote host was probed.

The companion [platform evidence JSON](luna64-r4.3-execution-environment-a3-evidence-20261011.json)
records supported observations and explicit unknowns. OS support and source
inspection are not runtime qualification.

## 4. Single-process architecture evaluation

**Not compatible with the unchanged frozen test.** Source
`test-track-b-gate-r4.mjs` imports `node:child_process` and calls `spawnSync`
for every golden validator-negative case (20), plus three other CLI calls.
There are **23 serial descendant Node executions** in this one primary test,
not 23 extra corrective test invocations. It also creates a temporary directory
under `os.tmpdir()`, writes CLI inputs, asserts status/stdout/stderr, and removes
that directory in `finally`. Static counting was done by reading golden JSON,
not executing test/generator code.

Importing the three tests sequentially into one Node process preserves neither
the three exact child commands nor necessarily isolation of globals/module
cache, exit codes and failure cleanup. Two corrective tests do not yet exist,
so their compatibility cannot be asserted. Worker threads are not OS
descendants, but do not reproduce validator CLI process exit/stdio semantics.
Replacing `spawnSync` with in-process calls, interception, or a modified frozen
test is not an authorized workaround. A future separately reviewable runner
proposal must establish equivalence and retain the frozen tests unchanged;
currently none exists.

An active-process Job Object limit of one can prevent ordinary associated
children once the sole test occupies the job, but would make the required
CLI assertions fail. A process-count limit is not a universal denial of
out-of-job creation by WMI/service brokers; token rights, broker access,
breakaway flags and inherited handles must also be controlled.

Per-process **hard** working-set maximum is a real documented candidate:
`SetProcessWorkingSetSizeEx` with `QUOTA_LIMITS_HARDWS_MAX_ENABLE`
states the working set will not exceed the maximum. Ordinary working-set
targets and `JOB_OBJECT_LIMIT_WORKINGSET` without a proved hard-maximum
configuration must not be confused with this flag. For one fully contained
process it can address that process's resident working set, not supervisor/
bootstrap pages, kernel memory, or commitment. CPU measurement
`GetProcessTimes` sums all threads' user and kernel time, but provides no
pre-execution stop barrier. Time watchdog, output storage and bootstrap remain
unresolved even if no child existed.

## 5. External isolation alternatives

| Candidate | Memory / CPU boundaries | Bootstrap, failure and artifacts | Availability / authorization |
|---|---|---|---|
| Hyper-V VM | Fixed guest RAM could constrain guest physical allocation; dynamic-memory maximum is a different policy. Neither includes all host VM/management overhead nor equals process working-set sum. One vCPU is allocation, not a 120-second total CPU budget. Guest and host accounting must be declared separately. | A preconfigured VM might contain guest bootstrap from guest launch; host manager, boot, teardown, watchdog and VM worker still need a declared trusted boundary. Host-side forced shutdown, failure evidence, immutable guest image/runtime and quota-backed restricted export require qualification. | Hardware appears eligible, but no running hypervisor or management commands/services observed. Feature state inaccessible. No image, authorized setup or demonstrated 512 MiB boot/operation. Not selected. |
| WSL2 | `.wslconfig` configures the shared WSL2 VM memory/processors/swap; not a per-test Windows working-set ceiling or cumulative CPU-time limit. Cgroup memory accounting/CPU bandwidth are again different metrics. | Distro/container bootstrap, shared VM, Windows manager and export path must be scoped. Global WSL settings affect other work; shutdown/termination of shared infrastructure is not authorized. Need pinned distro/kernel/runtime, hard artifact restriction and independent failure manager. | Only launcher stub observed; no current-user registration or service established. No installation, feature enablement, distro start, or global settings change permitted. Not selected. |
| Container (Windows or Linux) | Windows process isolation still relies on qualified host/job policy; Hyper-V isolation adds VM overhead. Linux `memory.max` is charged cgroup memory, can temporarily exceed limit in documented circumstances; `cpu.max` is bandwidth per period, not total elapsed CPU budget. Swap/page cache/kernel accounting need explicit policy. | Runtime daemon/bootstrap and all test descendants require preexisting containment; no privileged/broker escapes, alternate mounts/network, unbounded logs or export writes. Abrupt kill must retain bounded host evidence. Pinned digest/kernel/runtime required. | Docker/Podman and relevant runtime services not observed. No image/daemon/environment authorization established. Not selected. |
| Separately administered host | Administrator might establish job/cgroup/VM and storage policy before any experiment launcher starts. Actual metrics, process accounting, non-real-time time bounds and accounting of the manager remain to be proved. | Dedicated unprivileged account, restricted storage, pre-start enclosure, independent failure controller, audited teardown and offline evidence export required. No source/code transfer to a third party under this gate. | No identified available/approved host or operator attestation. An authorization and static capability inventory are required first. Not selected. |
| Already-authorized native enclosure | A preinstalled administrator-controlled service/job could remove experiment-side bootstrap creation. Hard memory/accounting restrictions must match the explicit policy. | Controller may be infrastructure only if owner approves scope/exclusion; otherwise it too needs containment. Kill-on-last-handle-close depends on handle ownership and leakage. | None established. Existing shell/tool harness containment is unknown and not claimed as a resource guarantee. Not selected. |

Do not assume a 512 MiB guest can boot, run Node/PowerShell and export evidence.
Boot/swap/host overhead cannot be silently excluded or charged to another
unapproved budget. Cross-OS execution changes executable paths, PowerShell
assumptions, path/CLI behavior and possibly floating-point runtime results;
even unchanged equations need compatibility review and provenance.

## 6. Revised Windows-native possibilities, not adopted

### Direct documented OS controls

- Job commitment ceiling `JobMemoryLimit=536870912` with
  `JOB_OBJECT_LIMIT_JOB_MEMORY`; commit that would exceed the limit fails.
  It does not itself guarantee immediate job termination and is not working set.
- Active-process count and affinity can be configured as native job limits;
  ordinary associated children inherit job restrictions. No breakaway flags,
  broker escapes or inherited assignment-capable handles may be allowed.
- A multiple-process working-set alternative is worth independent investigation:
  for at most four accounted processes, hard maximum 128 MiB per process would
  algebraically imply a 512 MiB sum **if every relevant process is hard-bounded
  from creation and the process count/containment invariant holds continuously**.
  Four represents outer launcher, PowerShell supervisor, primary Node test and
  validator grandchild simultaneously; the two future tests would require
  proof they add no other concurrent process.
  This is a sufficient conditional bound, not a qualified mechanism: no
  inherited hard-flag proof, before-first-page enforcement, outer launcher,
  broker restriction, effective nested-job context or viable 128 MiB runtime
  exists here. Setting limits after suspended creation does not erase earlier
  allocation/working-set usage. Process count alone does not prove the bound.
- Native job user-time limits exclude kernel time and are checked periodically.
  Job accounting can measure user plus kernel, including departed members,
  without creating a strict total-time termination guarantee.
- NTFS quotas are administrator-configured user/volume data limits, not a
  per-directory sum of test artifact bytes. A dedicated account/volume quota
  might prevent disk growth but requires policy for allocation/logical size,
  temporary inputs, filesystem overhead, final evidence and excluded storage.
  Existing ACLs alone cannot enforce a byte quota.

### Watchdog-dependent quantities

| Quantity | Proposed observation path | Maximum delay / missed event | Failure consequence / required boundary |
|---|---|---|---|
| Aggregate user+kernel CPU | Job accounting plus process handles; never sum per-process peaks as a substitute | Poll interval plus scheduler/query/termination delays; no finite worst-case bound established. A proposed 100 ms poll target is not guaranteed latency. | Missing query/handle fails closed by requesting job termination; actual cessation time must be proved. Controller must already be within an approved trusted enclosure. Controller death can leave work running unless sole-handle kill-on-close and outer coverage are proved. |
| Monotonic wall cutoff | Independent monotonic clock/timer, start includes declared bootstrap, boot if in scope, tests and teardown | Timer resolution is not a dispatch or termination bound. Non-real-time host scheduling can delay watchdog; no justified headroom or permitted overshoot exists. | Timer/controller failure must cause containment-layer termination independent of that controller; ordinary external PowerShell polling is not such a proof. |
| Artifact bytes | Bounded writer/broker checks requested bytes before accepting output, plus restricted quota-backed storage | Polling allows overrun between samples. Pre-write guard is only enforceable for writes that cannot bypass broker; no complete mediation/finite reconciliation latency established. | Reject write before cap, reserve bounded failure evidence, deny alternate/temp/stdout destinations; broker/controller failure cannot allow unmediated continuation. ACL/quota/process identity and storage scope must be owner-approved. |
| Working-set telemetry / process notices | Current and peak process counters, job membership queries, completion-port notifications | Samples can miss transient peaks or short-lived processes. Ordinary messages are not guaranteed; advisory notification is asynchronous. | Missing evidence marks incomplete/FAIL, never proof of compliance by silence. Hard containment must not depend solely on message delivery. |

Kill-on-last-job-handle-close can provide crash cleanup if the trusted owner is
the last handle holder and no child inherits/duplicates/opens another handle.
It does not catch a hung living controller, retroactively enclose the launcher,
or guarantee exact CPU/wall cutoff on a non-real-time host. No bound is invented
by choosing a large empirical safety margin. A revised policy could expressly
accept a measured stop trigger plus owner-approved overshoot/scope treatment,
but that would be a substantive resource-policy change, not compliance with
the current strict interpretation.

## 7. Feasibility decision matrix

| Architecture | Resource enforcement | Bootstrap / complete tree | Frozen test compatibility | OS support | Complexity / reproducibility | Additional authority | Current result |
|---|---|---|---|---|---|---|---|
| One Node process, no descendants | Hard process WS possible; CPU/wall/output unresolved | Launcher/controller still unresolved; brokers require restriction | Fails existing 23 CLI assertions without redesign | Process/job APIs present in OS generation, not exercised | Low only if test behavior is changed; unproved reset/CLI equivalence | Runner/command policy, equivalence review, environment qualification | Not qualified |
| Managed Windows enclosure, serial tests | Commit/active count/affinity available; hard-WS/count alternative conditional; strict time/output unresolved | Could enclose before start only with a preestablished administrator boundary | Original three tests and 23 validator descendants can be retained | Windows supports APIs; token/nested-job/quota context unqualified | Medium; exact images, limits and handles required | Admin setup, metric/scope/watchdog policy, descendant allowlist, qualification budget | Not qualified |
| Hyper-V VM | Guest memory/vCPU policy only; host overhead/time/output unresolved | Guest boot enclosed if preconfigured; host manager unresolved | Windows guest may retain CLI behavior; 512 MiB operation unproved | Hardware eligible; runnable environment not established | High; pin image/boot/export/accounting | Infrastructure, guest/host policy, qualification | Not qualified |
| WSL2/container | VM/cgroup/commit metrics not original WS; total CPU deadline unresolved | Shared runtime/daemon and export gaps | OS/PowerShell/CLI compatibility review required | No ready runtime established | High; kernel/image/mount/provenance required | Infrastructure, metric, test-host compatibility and qualification | Not qualified |
| Separate controlled host | Unknown until administrator evidence | Unknown; could provide independent pre-start enclosure | Unknown | No identified authorized host | Unknown; audit/immutable environment required | Explicit host/setup/data handling and resource policy | Not qualified |

**Selection: none. NO QUALIFIED EXECUTION ENVIRONMENT.** No candidate presently
demonstrates every required guarantee. The simplest plausible *future* direction
is to inventory an administrator-established Windows enclosure that retains
the original three CLI tests and their validator descendants. That is not a
selected execution architecture, authorization or promise of feasibility.

## 8. Future execution specification prerequisites (not a released specification)

Since no architecture is viable now, do not invent allowed executables or
launch an incomplete specification. A future selected design must independently
freeze all of these before owner approval:

1. Named host/enclosure and administrator attestation; trusted manager scope,
   privilege/identity, startup, boot, teardown and controller accounting.
2. Exact executable/runtime hashes and argv: three primary commands plus the
   existing validator CLI descendant allowlist, without runner/generator access.
3. Exact hard byte limits, CPU metric/allocation, observation/cutoff delays,
   accepted overshoot (if any), and complete scope; never relabel metrics.
4. Limits installed and proved effective before any in-scope process executes;
   creation/allocation phase coverage and nested-job effective settings.
5. Descendant, broker, job-handle and storage restrictions; proof of no escapes.
6. Independent fail-closed crash/hang response, abrupt termination, live-process
   reconciliation and reserved bounded failure evidence.
7. All persistent/temp/stdio/export destinations mediated; immutable reference
   inputs versus output artifacts clearly scoped.
8. Durable one-shot ledger outside disposable guest/container storage, tied to
   gate, worktree revision and terminal outcome; never reset the parent marker.
9. Qualification sources/configuration, exact cases and aggregate budget
   independently reviewed before any qualification invocation.
10. After qualification, separate corrective execution approval and later
    independent implementation review; no automatic scientific rerun.

### Distinct provisional qualification request (not authorized)

For a future complete, owner-approved environment only: one qualification
invocation, zero retries, 16 cases below, at most 128 combined stimulus/trace
records; one logical CPU; aggregate 120 user+kernel CPU seconds, 180 wall
seconds, 536870912-byte commitment ceiling **only if separately approved with
outer scope fully declared**; at most four active processes including launcher
and controller; at most 5242880 artifact bytes with 65536 bytes reserved
inside that cap for terminal evidence. Working-set metric changes, controller
exclusions or overshoot are not approved by this provisional proposal.

No qualification can start under this provisional budget while its own
bootstrap/time/storage limits remain unresolved. A final candidate-specific
qualification gate must resolve that dependency without exempting itself.
The candidate memory value is not a selected alternative to the parent memory
requirement. No code or command for this qualification is supplied.

Q01 pre-start limit/query-back; Q02 setup/assignment failure before resume;
Q03 child/grandchild containment with abrupt parent exit; Q04 count overflow,
breakaway and broker-access denial; Q05 below-limit normal case;
Q06 controlled over-limit commitment denial; Q07 hard-WS/count boundary if that
alternative is selected; Q08 aggregate user+kernel CPU cutoff, including
kernel-heavy work; Q09 monotonic wall cutoff under scheduler delay;
Q10 controller crash, hang and handle leakage; Q11 quota/broker pre-write
overrun rejection and temp/stdio escape denial; Q12 artifact/monitor failure
and reserved evidence; Q13 affinity and nested-job effective settings;
Q14 atomic marker creation, inaccessible/existing/uncertain marker and replay;
Q15 normal/abrupt cleanup with no surviving member;
Q16 environment/revision/trace identities and deterministic evidence.

All cases are **NOT RUN**. These are resource-mechanism cases, not the three
corrective tests, an experimental reproduction, or a scientific dataset.
The qualification allowance is separate and proposed, not derived from A2
or the unused parent allowance. Success would not automatically release
corrective implementation or scientific work.

## 9. Documentation and validation basis

Authoritative pages consulted on 2026-10-11 (summaries, not copied manuals):

- [Microsoft Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects): default CreateProcess membership, WMI exception, breakaway, message reliability.
- [Basic Job limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information): active count, affinity, periodic user-time checks and last-handle termination.
- [Extended Job limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information): commitment and peak job memory.
- [Hard process working set](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-setprocessworkingsetsizeex): hard maximum flag versus ordinary paging targets.
- [GetProcessTimes](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes): complete thread-summed user/kernel measurement, not enforcement.
- [Job assignment](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject): rights and effective nested-job restrictions.
- [Hyper-V requirements](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements): Windows Pro, firmware/SLAT and host RAM planning, not a 512 MiB guest boot guarantee.
- [WSL configuration](https://learn.microsoft.com/en-us/windows/wsl/wsl-config): global WSL2 VM configuration, not per-test containment.
- [NTFS quotas](https://learn.microsoft.com/en-us/windows/win32/fileio/managing-disk-quotas): administrator user/volume limits, not directory byte sums.
- [Linux cgroup v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html): charged memory, possible temporary overage, CPU bandwidth versus usage accounting.

Initial web-fetch/MCP and default curl retrieval failed. Curl with
`--ssl-no-revoke` fetched the cited pages over HTTPS; certificate revocation
checking was disabled for those retrievals, so no revocation-validation
claim is made. A first quota URL returned HTTP failure; the corrected
Microsoft URL above succeeded. Only public documentation was retrieved.

| Procedure | Observed status |
|---|---|
| Git ancestry/ref and checkout/blob hashing | Verified predecessor objects/ref; disclosed A2 proposal mismatch |
| Ten package raw hashes / 32 freeze inventory OIDs | Verified with Stage-B mapping |
| Corrective tree / markers / static test inspection | Clean baseline, no retained execution, 23 validator CLI launches identified |
| Platform queries | Observed capabilities with explicit privilege/inventory limits |
| OS API behavior, VM boot, quota enforcement, containment qualification | NOT RUN |
| Corrective tests / scientific efficacy or reproduction | NOT RUN |

No core architecture change requires an ACP here. A01-A03 logical causality,
A07 local information, A08 finite state, A09-A11 independent energy/credit
and A15 portability are protected constraints, not measured results.

## 10. Publication, review and next authority

Independent review must inspect actual A2 Git/checkout identities, platform
observations and cited documentation rather than accept this proposal's
claims. Four scopes: OS/resource enforcement; bootstrap/failure; scientific
compatibility; governance/authorization. Review reports and exact A3 hashes
are recorded separately so this decision artifact need not be rewritten
after review.

Preserve A1/A2 blocked records and the original NOT SUPPORTED pilot verdict;
scientific efficacy remains unassessed. Parent corrective authorization is
preserved but execution remains blocked. No A3 resource policy, infrastructure
setup, qualification, implementation or scientific rerun is owner-approved.

Next bounded assignment is Luna-0 governance-only identification of a specific
administrator-controlled host and a reviewable resource policy with complete
bootstrap and cutoff semantics, **only if separately requested**. Integration
is not ready. Rollback consists of retaining the pre-A3 governance revision;
do not reset or alter any experimental worktree, historical artifact or marker.
