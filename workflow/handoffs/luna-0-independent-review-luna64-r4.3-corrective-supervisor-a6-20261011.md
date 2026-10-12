# Luna-0 Independent Review — Luna-64 Corrective Supervisor A6

**Gate:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A6`  
**Integrated verdict:** **BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE**  
**Review scope:** Governance proposal only. No supervisor, qualification case,
corrective test, scientific workload, guest/host diagnostic, or infrastructure
operation was executed.

## 1. Governing identity reconciliation

Luna-0 verified the A5 package and workflow closure identities against the
current baseline:

| Evidence | Verified identity |
|---|---|
| A5 package commit | `12f84a41fe7c91c17c5df8e975fce24efbadf9ad` |
| A5 workflow closure | `b758b411e568b41c516228e7d3bdff26058114cc` |
| A5 proposal SHA-256 | `5BCDAC72E7EBDEA777E9964F25554834C4460D97075E6871690BD441BA00C6E5` |
| A5 integrated-review SHA-256 | `54D11A362EDED451292330C6FA5627B570BD6103ADE0F69E115F5CDC3C7B934D` |
| A5 closure ancestry | Verified as an ancestor of the A6 baseline |
| Frozen R4.3 content / governance closure | `64a214e310de3b982b90a8ad215598bc1e9f8b1c` / `ea1b10456cbf4ca726e473076d239a4f6e53b9c7` |
| Frozen R4.3 manifest SHA-256 | `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B` |
| Corrective gate SHA-256 | `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369` |
| Owner-authorization SHA-256 | `972701FBD7394AF655F27E8CCDC394483AAD7B018F25E7A5A41A2C98F9E8BA44` |

The frozen R4.3 protocol, original owner authorization, accepted reject-only
second-origin policy, original pilot **NOT SUPPORTED** verdict, unused
corrective allowance, all A1-A5 blocked findings, and Luna-63C isolation are
preserved. A6 does not close or supersede any predecessor gate.

## 2. Independent review records

Three read-only reviewers received distinct bounded scopes. A further
artifact-only delta review examined the revised storage specification.

### Reviewer A — CPU and termination

The reviewer found the CPU/wall arithmetic and Q05/Q06/Q10/Q11 state semantics
internally coherent in the reviewed draft:

- `120 + 10.1 = 130.1` CPU seconds, or `130100000` usec.
- Per-case CPU caps sum to `225.1` seconds; `14.9` seconds remain unallocated
  within the proposed 240-second qualification budget.
- Per-case wall caps sum to the proposed 600-second aggregate wall limit.
- The CPU-margin arithmetic is explicitly conditional on a 100 ms polling
  target, one-second guest cgroup-kill stage, and nine-second host VM-Off
  stage.
- Normal Q05/Q06 success leaves the VM running; an escalation powers it off
  and aborts later cases.

The reviewer confirmed these are not demonstrated bounds. CPU monitor
scheduling, cgroup-kill completion, host scheduling, control transport,
VMMS/Hyper-V command response, and confirmed VM-Off latency remain unbounded
by supplied evidence. The later A6 draft also names the absent authenticated
guest-host channel as an admission blocker. Reviewer A did not independently
rerun or certify host/guest latency.

### Reviewer B — artifact containment

The initial review was **BLOCKED** on unimplemented FUSE mediation, durable
ledger/recovery, `writeFile()` partial-write treatment, sparse-file
accounting, descriptor inheritance, backing-volume sizing, root-only failure
reserve, and incomplete Q07-Q09 acceptance.

The artifact delta review found the revised proposal clearer on these
contracts: pre-operation `ENOSPC`; accepted-prefix accounting; sparse `lseek`
and `ftruncate` behavior; close-before-exec descriptor policy; 512-total-inode
and backing-capacity thresholds; root-only reserve; and synthetic-only
qualification probes. It confirmed the artifact remains unqualified and
blocked. It also requested clarification of uncertain rollback evidence,
short-write accounting, failure-reserve availability after ledger failure,
and later-opened descriptors. Luna-0 incorporated conservative
no-refund-on-uncertain-write behavior, explicit resulting-`st_size` charging,
a failure-reserve descriptor independent of the workload ledger, and
mount-scoped post-exec descriptor policy.

Those last wording changes were not sent for another independent pass. They
do not supply an implementation or runtime evidence; the FUSE daemon, fixed
ledger, crash recovery, and 32 MiB image fit remain unimplemented and
unqualified. Q07-Q09 are proposed synthetic cases only and cannot execute the
corrective tests.

### Reviewer C — memory and governance

The reviewer identified wording risks around memory-metric equivalence,
whether A6 implicitly cleared A1-A5, owner-decision sequencing, and explicit
Luna-63C isolation. The A6 proposal now states directly that Linux
`memory.max=536870912` is a non-equivalent replacement policy requiring owner
approval; no Linux substitute is authorized before approval. It also states
that A6 does not clear A1-A5, adds a source-image allowlist that excludes
Luna-63C paths, and distinguishes A6 governance review from owner approval
required before any future qualification request.

The reviewer's suggested order to obtain owner policy approval before
reviewing A6 was not adopted: the A6 task specifically requires independent
review of the governance proposal before presenting the owner decision gate.
No owner approval is inferred from this review.

## 3. Integrated findings

| Area | Disposition | Evidence / unresolved condition |
|---|---|---|
| Frozen protocol and predecessor governance | Preserved | Exact identities and A5 ancestry checked; A1-A5 verdicts remain historical and blocked. |
| Memory replacement | Proposed; owner decision required | 512 MiB cgroup-accounted memory (`memory.max=536870912`), `memory.swap.max=0`, and group OOM handling are not equivalent to Windows working set. No runtime qualification. |
| Cumulative CPU | Blocked | 120-second trigger and 130.1-second candidate are explicit, but monitor/poll/kill/host-off response bounds are targets, not hard limits. |
| Wall termination | Blocked | QPC stages are specified, but no bounded scheduling or VM-Off latency is established. |
| Guest-host control/evidence | Blocked | No authenticated non-network transport is selected or verified. Owner-reported networking and Guest Service Interface are unavailable. |
| Artifact cap | Blocked | Proposed logical high-water FUSE ledger, reserve, filesystem image, and compatibility have no implementation or qualification evidence. Crash consistency and capacity fit remain unverified. |
| Qualification allowance | Proposed only | 12 synthetic cases, 240 guest CPU seconds, 600 wall seconds, 768 MiB outer memory, 6 MiB combined payload/evidence, one VM start, at most one host TurnOff, zero retries. It is unusable under A6 and requires owner approval, a later request, independent prereview and separate explicit authorization. |
| Scientific efficacy / architecture | Not assessed | No scientific workload ran; no efficacy claim or architecture promotion follows. |
| Luna-63C | Preserved | No Luna-63C artifact, state, or computation was used. Future source image must exclude its paths. |

The proposed A6 budget arithmetic was mechanically checked from the JSON:
`225.1 + 14.9 = 240` guest CPU seconds; per-case wall maxima sum to 600
seconds; workload artifact allowance plus failure reserve is `5,242,880`
bytes. JSON parsing succeeded. These checks validate document syntax and
arithmetic only, not resource enforcement.

## 4. Verdict and stopping boundary

**BLOCKED — ENFORCEMENT CONTRACT INCOMPLETE.**

The blocker is unavailable enforcement evidence and unresolved owner-policy
decisions, not a demonstrated engineering impossibility. Specifically:

1. CPU and wall termination latency are not bounded by evidence.
2. The authenticated guest-host status/control/evidence channel is unspecified.
3. FUSE artifact mediation, its crash-safe ledger, descriptor and failure
   paths, and the 32 MiB backing image have not been implemented or qualified.
4. The owner has not approved the Linux memory replacement, CPU margin/scope,
   wall-stage contract, artifact metric/infrastructure, or separate
   qualification budget.

No qualification, corrective implementation, corrective test, scientific
workload, infrastructure change, A7, production integration, architecture
promotion, or Luna-63C work is authorized. The original corrective allowance
remains unused. Stop at this documented blocker; any next step requires an
explicit owner response and a separately scoped authorization.

## 5. Reviewed artifacts

| Artifact | SHA-256 |
|---|---|
| A6 proposal | `AD952D9AB7656313D03E0E58BF48469D420B74C5E9CB6BA6738915AA0D34C4C4` |
| A6 machine-readable evidence | `CB4FA2BBB72DFD1371312641A101F3F5E77A1BDF99540521EE366069AED0C7AE` |

The integrated review file's own SHA-256 and the final workflow file identity
are recorded after this review is finalized.
