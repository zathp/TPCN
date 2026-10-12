# Independent Review — Luna-64 A6 R2 Enforcement Design

- **Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6-R2`
- **Integrated verdict:** **BLOCKED — ENFORCEMENT DESIGN INCOMPLETE**
**Review scope:** Documentary, read-only review of the R2 design and its R1
governance baseline. No infrastructure, qualification, corrective workload,
or scientific experiment was executed.

## 1. Baseline and preserved authority

The R2 proposal is assessed against the R1 owner-policy reconciliation:

- R1 package commit: `f00dea13d64657cbc976d21daf50739ddf9722fe`
- R1 workflow closure: `f1cfb6e98cfc872753ea262bdb56e4a66ab40c05`
- R1 proposal SHA-256:
  `A619E3A4361B712471B8C3A7FD2AA784992ED6B4F5F0E218ED0449B16144319D`
- R1 independent-review SHA-256:
  `DD7E0F840F8C3F34A7016351C28F63CA50F313618DC1B218B81A509CBD8E4D36`
- R1 manifest SHA-256:
  `D51C207C5ED7E91B59C661FB39B67E88F27C0FA47CDEF708AA1F0ADFB7DEE958`

The frozen R4.3 content freeze remains
`64a214e310de3b982b90a8ad215598bc1e9f8b1c`, its governance closure remains
`ea1b10456cbf4ca726e473076d239a4f6e53b9c7`, and its manifest SHA-256 remains
`62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`.
The owner-provided D1-D6 decisions remain design/planning decisions only.
Prior A1-A5 blocked findings, the original pilot verdict
**NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, the unused corrective
allowance, and Luna-63C isolation are preserved. No approval for
infrastructure changes, qualification, corrective execution, scientific
rerun, production integration, or architecture promotion is inferred.

## 2. Independent reviewer outcomes

### Reviewer A — Host/guest security

**Verdict: BLOCKED.**

- Resolved as a design-specification gap: the proposal defines fixed frame
  structure, MAC coverage, challenge-response, session derivation,
  direction-specific sequence counters, and invalidation on reconnect.
- The one-shot key/image retirement policy is explicit, but uniqueness,
  non-cloning, and non-reuse remain policy assumptions, not enforced facts.
- The VM GUID is an asserted protocol field, not proof that the COM pipe peer
  is the authorized VM. Pipe ACLs, exclusive mapping, mapping readback, and
  VM-to-device identity remain unqualified.
- Hyper-V COM-port-to-local-named-pipe mapping is documented; deployment
  compatibility and security are untested.
- A crashed, hung, or starved host controller/watchdog has no autonomous
  fallback and no guaranteed VM-Off latency. The limitation is disclosed but
  remains an enforcement blocker.

### Reviewer B — CPU and wall enforcement

**Verdict: BLOCKED.**

- Resolved as a specification ambiguity: the 240-second total uses one
  continuous qualification-parent `cpu.stat:usage_usec` baseline; Q06 uses a
  nested local baseline for the 130.1-second candidate without resetting or
  excluding usage from the aggregate counter.
- Resolved as a lifecycle ambiguity: Q0 is the session clock, case intervals
  are recorded as Tcase dispatches within Q0, Q01 includes boot/admission,
  and Q11 uses its own Tcase for the 170/171/180 stages.
- Budget arithmetic is consistent: case CPU reservations total 240 seconds
  and wall reservations total 600 seconds. Q06's 150-second reservation is
  expressly not permission to exceed its 130.1-second stop/fail target.
- The proposal now specifies an immediate kill/TurnOff response on first
  observed Q06 candidate-boundary crossing. This is action on detection, not
  prevention of crossing before a poll or confirmed cessation.
- `cpu.max` limits execution rate, not lifetime CPU. Polling, monitor
  scheduling, cgroup kill, host scheduling, Hyper-V TurnOff, and Off
  confirmation have no demonstrated finite bound. Neither the 130.1-second
  candidate nor aggregate 240-second CPU ceiling is a proven hard maximum.
- QPC supplies a monotonic time source but does not bound host scheduling or
  TurnOff completion. The 170/171/180 stages and 600-second Q0 ceiling remain
  planning targets, not guaranteed termination deadlines.

### Reviewer C — Artifact containment

**Verdict: BLOCKED.**

- Resolved or clarified: the proposal identifies the frozen test's
  `mkdtemp(os.tmpdir())` temporary-file path; specifies temp/output
  redirection and readback; distinguishes guest ext4 project-charged
  allocation from host NTFS quota usage; and addresses sparse files,
  unlinked files, inode limits, and the failure-evidence reserve.
- The guest split is 1,264 workload blocks plus 16 reserved blocks, totaling
  1,280 × 4,096 = 5,242,880 bytes. The host split is 983,040 bytes plus
  65,536 bytes, totaling 1,048,576 bytes. Their 6,291,456-byte sum combines
  distinct metrics and is not one common allocation measure.
- Microsoft documentation states sparse files affect Windows user quotas by
  nominal file size rather than actual allocated disk space. The proposal
  accordingly does not label NTFS quota usage as physical allocation.
- The proposed ext4 project-allocation cap does **not** enforce the frozen
  5 MiB aggregate logical high-water metric: sparse logical lengths and
  cumulative write/delete cycles can exceed the live allocated quota.
  Per-file `RLIMIT_FSIZE` and post-run scanning are not aggregate substitutes.
  Replacing the frozen metric requires explicit owner approval.
- Exact temporary-path completeness, quota behavior, reserve usability,
  metadata/inode headroom, and evidence durability are proposals requiring
  qualification; none was tested.

### Reviewer D — Governance and provenance

**Verdict: BLOCKED.**

- The R2 proposal distinguishes A1-A3 commit identities and retains the R4.3,
  original authorization, A4/A5, and R1 history; prior outcomes, the original
  pilot verdict, unused corrective allowance, and Luna-63C isolation remain
  intact.
- D1-D6 are preserved within their limits: design-only memory metric;
  unverified CPU/wall targets; simpler storage alternatives considered
  before custom mediation; D4 planning-only budget; authenticated
  non-network control requirement; and no infrastructure-change authority.
- The fixed 12-case lifecycle is coherent: one VM start; Q11 is the final
  live-VM case; Q12 is offline-only; any unexpected failure stops the
  sequence; no retry or restart is allowed. Arithmetic is consistent:
  240 guest CPU seconds and 600 wall seconds.
- The 768 MiB host control-plane private-commit metric and mixed 6 MiB
  artifact/evidence accounting are proposals requiring owner approval and
  do not establish enforcement.
- A text splice found in an earlier draft was corrected. The final proposal
  now records each reviewer's blocked outcome. The R2 manifest and workflow
  entry are blocked-state governance records only; no package publication
  or execution is represented as complete.

## 3. Integrated blockers

1. **Host/guest binding and recovery:** the COM/pipe mapping and exclusive
   identity binding are unqualified; key non-cloning/non-reuse is an
   assumption; host controller/watchdog failure has no autonomous recovery.
2. **CPU enforcement:** no hard lifetime CPU mechanism or finite termination
   latency establishes the Q06 candidate or 240-second aggregate ceiling.
3. **Wall enforcement:** the 170/171/180 and 600-second values are targets;
   no finite bound for TurnOff and confirmed Off is established.
4. **Artifact policy:** the selected quota design does not implement the
   frozen aggregate logical high-water cap. The alternative metric needs
   explicit owner approval.
5. **Qualification accounting and runtime evidence:** host control-plane
   memory, mixed artifact metrics, containment, quotas, evidence reserves,
   and durability remain unapproved or unqualified.
6. **Execution authority:** D4 is planning-only and D6 denies infrastructure
   changes. No qualification, corrective execution, or scientific workload
   is authorized.

These are unavailable-enforcement-evidence and owner-policy blockers, not a
demonstrated engineering impossibility. Do not automatically initiate R3.
The smallest next step is an owner decision on the proposed artifact and
qualification accounting changes, plus a separately authorized feasibility
design that supplies a genuine hard CPU/wall boundary or an explicit revised
resource policy. Owner approval alone cannot prove termination latency.

## 4. Disposition and validation

**Integrated verdict: BLOCKED — ENFORCEMENT DESIGN INCOMPLETE.**

The R2 design may be retained as a blocked governance record only. No
qualification was executed; no infrastructure was installed or modified; no
corrective implementation or scientific workload ran. Do not treat this
review or its arithmetic checks as runtime qualification, resource-policy
approval, efficacy evidence, or authorization to proceed.

The reviewer assessments were read-only and documentary. Arithmetic was
checked for the twelve case allocations and declared storage accounting.
Runtime cgroup, filesystem, COM/pipe, Job Object, watchdog, VM termination,
and evidence-integrity behavior remain **NOT TESTED**.
