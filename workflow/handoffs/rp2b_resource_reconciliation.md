# RP-2B Lane B-R: resource reconciliation

**Revision:** Corrective R1 — 2026-10-12  
**Disposition: BLOCKED — owner decision and evidence gates remain open.**

This is a corrective, static-only reconciliation of the RP-2B resource
profile. It is not an authorization, implementation review, or resource
qualification. It does not execute the probe, wrapper, preflight, tests, or
runtime.

## Review identity and evidence boundary

Reviewed the requested baseline `96fb4aec100578db6939136b4ed7985478f18bb8`
on `governance/luna64-r4.3-freeze-20261010`. The two new artifacts in this
review are additive; no existing file is intentionally overwritten. The
pre-existing untracked files were preserved.

Primary records:

- Frozen RP-2 profile: `workflow/docs/luna/LUNA_65_PHASE2A_RP2_RESTRICTED_TOKEN_COMPATIBILITY_CONTRACT.md`,
  especially §5 (resource and cleanup envelope) and §6 (result classifications).
- Accepted RP-2 owner decision: `workflow/docs/luna/LUNA_65_PHASE2A_RP2_R1_OWNER_DECISIONS.md`,
  §§1–3, especially D-RP2-OUTER-1 and §3's explicit statement that resource
  bounds are unqualified and unexecuted. Its publication handoff,
  `workflow/handoffs/luna-0-luna65-rp2-r1-owner-decision-closure-20261012.md`,
  §§1–3, independently says RP-2B execution is not authorized.
- Resource Policy R2: `workflow/docs/luna/LUNA_65_PHASE2A_RESOURCE_POLICY_R2.md`,
  §§1–3, 4.1–4.3, 5, 6, and 7. R2 is accepted for Phase 2A qualification
  design only; §3 expressly says it does not amend Phase 2B.
- Prior Lane B: `workflow/handoffs/rp2b_lane_b_resource_readiness.md`,
  §§“Authority and profile compatibility” and “Resource and evidence-budget
  risk table.” Current integration: `workflow/handoffs/rp2b_authorization_readiness.md`,
  §§“Blocking findings” (B1–B2), “What is and is not established,” and
  “Required follow-up and next permitted gate.”
- Static source inspected, not run:
  `scripts/luna65_phase2a_rp2_compatibility_probe.py:1041–1113` and
  `scripts/luna65_phase2a_rp2_outer_wrapper.ps1:22–27,604–640,928–952,1014–1033`.

## Claim-level reconciliation

| Claim | Classification | Static finding and exact reference |
|---|---|---|
| A 256 MiB / 120-second / 1 MiB envelope was requested for this review. | **Review input, not verified contract incorporation** | The request supplies these values. The existing R2 policy does not make them RP-2B requirements: R2 §2 accepts 120-second aggregate user-plus-kernel CPU and elapsed-wall budgets, 268,435,456-byte memory policy, and 1,048,576 retained-artifact bytes **for Phase 2A qualification design only**; R2 §3 says Phase 2B remains separate and is not amended. |
| The request itself unambiguously specifies a hard 256 MiB job-wide committed-memory metric. | **Not established from the reviewed RP-2B record** | Current readiness B1 (`rp2b_authorization_readiness.md:57–73`) characterizes the request that way, but this checkout's frozen RP-2 contract and owner-decision record do not incorporate that requested profile for RP-2B. This review treats the requested values as a question requiring owner reconciliation, not as an already-approved metric definition. |
| “256 MiB committed memory” is a fully specified metric. | **Not established; needs owner precision** | R2 §2 describes 268,435,456 bytes as aggregate concurrent job-wide private committed memory enforced using a Job Object limit; §5.1 configures `JobMemoryLimit` and separately requires sampling/summing live-process `PrivateUsage` and demonstrating that the enforced charge bounds that metric. The mapping is expressly not assumed. R7 owner decision D-R7-2, in `LUNA_65_PHASE2A_R7_OWNER_DECISIONS_AND_PROFILES.md` §2 (detail in §6), records replacement of aggregate private commit by Job Object job-memory charge and calls out non-equivalence. A future decision must say whether it means job charge, live private commit, or both, and how they are related. Neither is a system-wide resident-memory or working-set limit. |
| Frozen RP-2 source configures the requested 256 MiB and 120-second CPU/wall policy. | **Contradicted by source** | RP-2 contract §5 table sets a 64 MiB Job Object job-memory charge, 8-process backstop, 5-second job user-time backstop, 10-second active period, at most 5 seconds cleanup, 20-second outer deadline, and zero retries. The probe configures `job_time=50,000,000` 100-ns units, `active=8`, and `job_memory=67,108,864` bytes (`probe.py:1047–1051`, with readback at 1058–1062). The wrapper's deadline/stop path uses `O0+15,000` and `O0+20,000` ms (`outer_wrapper.ps1:928–952`). |
| Probe's CPU fields implement aggregate 120-second CPU enforcement. | **Contradicted as an enforcement claim** | The probe records Job Object `user` and `kernel` accounting and separately queries the current probe process's `GetProcessTimes` (`probe.py:1073–1113`); resource sampling is gated by a 250-ms interval at line 1095. It also configures the 5-second job user-time limit at 1047. The frozen contract §5 explicitly calls that a supplementary job user-time backstop, not aggregate user-plus-kernel CPU enforcement; it says probe and outer-wrapper CPU are not enforced and samples can miss peaks. Recording CPU fields is not the R2 §4.2 120-second monitored-budget implementation. |
| Frozen timing implements monitored 120-second elapsed wall with hard cessation. | **Contradicted as a profile match; cessation guarantee unknown** | The frozen envelope is 10 seconds active, up to 5 seconds cleanup, 20 seconds outer supervision (RP-2 contract §5; owner record D-RP2-OUTER-1). The contract describes this as best-effort, without a hard real-time guarantee. R2 §§4.1 and 4.3 likewise distinguish elapsed wall time from CPU and say a termination request does not prove cessation; R2's 120-second design is monitored and fails on observed overrun, not a guarantee of stopping exactly at 120 seconds. |
| The 1 MiB cap is shared, therefore all required evidence is known to fit. | **Value partly shared; fit unknown** | Frozen RP-2 contract §5 sets 1,048,576 logical bytes total across files, stdout, stderr, ledger, report, and intermediates; source constants are 1,048,576 total, 917,504 payload, 131,072 reserve, and 393,216 remote-representation reservation (`outer_wrapper.ps1:22–27`). `Charge`, `Retain-O`, and `Write-Artifact` charge representations before file writes (`604–640`); final file lengths are reconciled at `1014–1017`. These are static logical accounting/cap controls, not proof that every mandatory maximum-size success or failure record fits, nor an OS filesystem quota. R2 §7.3 itself says exact ledger fit is not analytically established for its separate Phase 2A schema and requires a sizing gate. Current readiness B2 correctly rejects Lane D's typical-volume estimate as a worst-case proof. |
| “Working set” establishes the requested memory bound. | **Incorrect terminology** | The probe emits both `P_private_bytes` and `P_working_set`, labels `P_memory_OS_bounded` false, and reports Job Object peak charge separately (`probe.py:1082–1110`). The contract §5 says working-set accounting is not a substitute. Do not relabel Job Object committed-memory charge as working set. |
| Prior owner acceptance already resolves the new RP-2B request. | **Not established** | D-RP2-OUTER-1 is explicitly accepted “for this bounded synthetic diagnostic only” (`LUNA_65_PHASE2A_RP2_R1_OWNER_DECISIONS.md` §2). Its §3 retains the 64 MiB / 8-process / 5-second user-time / 1 MiB envelope as unqualified and unexecuted. R2's Phase 2A owner acceptance cannot silently extend to RP-2B (R2 §§2–3). |

The above distinguishes **job-wide Job Object committed charge** from **working
set** and from **aggregate live private commit**; **aggregate job user-plus-
kernel CPU** from **job user-time** or a single process's CPU; **elapsed wall**
from CPU time; a stop/termination request from confirmed cessation; and a
retained-byte limit from a demonstrated maximum-size evidence fit.

## Options for owner disposition

These are proposals for a later owner decision, not approvals:

1. **Option A — frozen-profile compliance.** Keep the exact RP-2 envelope in
   contract §5 and the source unchanged. The owner must explicitly state that
   the new 256 MiB / 120-second request does not govern RP-2B and that the
   frozen 64 MiB / 10-second active / up-to-5-second cleanup / 20-second outer
   envelope is the intended RP-2B profile (including the 8-process and
   5-second job-user-time backstops and 1 MiB logical evidence cap). This would
   resolve which policy is intended, **not** establish runtime compliance,
   evidence fit, or authorization.
2. **Option B — contract amendment.** If the request is intended to govern
   RP-2B, issue an explicit owner-approved, separately reviewed amendment
   before implementation or execution. It must define the memory metric
   (Job Object charge versus live aggregate private commit, or both), hard
   limit/readback and enforcement relation; define 120-second aggregate
   user-plus-kernel CPU monitoring, trigger, sampling/gap and overrun semantics;
   define 120-second elapsed-wall trigger, escalation, cleanup, and what
   constitutes confirmed cessation; reconcile these with the existing 8-process
   and job-user-time controls, 10/5/20 timing, retries, and termination/UNKNOWN
   handling; and specify the exact retained-byte scope and maximum-size
   evidence accounting under 1 MiB. Update the controlled contract/owner
   record, source and traceability/review evidence only under explicit
   authorization. A request alone does not authorize those changes.
3. **Option C — blocked.** Do not select an envelope, change source/contract,
   authorize execution, or represent resource qualification as passed until
   the owner resolves A versus B and the independent evidence gates close.

**Current review recommendation: Option C (BLOCKED) as the disposition only.
No option is approved by this report.** The owner decision must be explicit
and recorded before a later exact RP-2B authorization can rely on either
profile.

## Provenance limits and verification boundary

Facts above are static statements about the requested Git baseline and cited
documents/source. The underlying request is identified here by the current
task and its characterization in the readiness package; no separate,
RP-2B-specific owner acceptance of the 256 MiB / 120-second profile is
identified in the reviewed contract/decision records. This review did not
verify host counters, Job Object
semantics on a target Windows build, sampling cadence in operation, actual
termination or process cessation, emitted/captured/retained byte totals, or
worst-case evidence fit. The prior Lane B and integrated readiness package
are review artifacts, not runtime evidence. R2's Phase 2A authorization scope
and sizing design are not RP-2B approval.

No probe, wrapper, preflight, tests, imports, or runtime was executed. No
frozen source or contract was modified. This report does not authorize
publication, implementation, or an RP-2B invocation.
