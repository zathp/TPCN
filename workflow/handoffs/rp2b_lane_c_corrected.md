# RP-2B Lane C-R — Corrected Static Race and Cessation Review

**Revision:** Corrective R1 — 2026-10-12  
**Baseline:** `96fb4aec100578db6939136b4ed7985478f18bb8`  
**Disposition:** **BLOCKED — CORRECTION REQUIRED**  
**Execution / downstream qualification:** **NOT AUTHORIZED**

This is a static correction of the historical Lane C report, not a replacement
for the frozen contract, a source change, or a runtime result. The original
`rp2b_lane_c_native_race_readiness.md` remains untouched. This correction is
limited to the two new handoffs named in the assignment.

## Review boundary and evidence

Read-only inputs:

- Frozen authority: `workflow/docs/luna/LUNA_65_PHASE2A_RP2_RESTRICTED_TOKEN_COMPATIBILITY_CONTRACT.md`
  (especially §§2–6 and 10.3–10.5).
- Defective prior report: `workflow/handoffs/rp2b_lane_c_native_race_readiness.md`.
- Luna-0 findings: `workflow/handoffs/rp2b_luna0_independent_review.md:240-267`.
- Current disposition: `workflow/handoffs/rp2b_authorization_readiness.md:1-5, 35-56, 72-112`.
- Implementations at the requested baseline:
  `scripts/luna65_phase2a_rp2_compatibility_probe.py` and
  `scripts/luna65_phase2a_rp2_outer_wrapper.ps1`.

For compact citations below, `contract.md`, `probe.py`, `outer_wrapper.ps1`,
`luna0_review.md`, and `rp2b_authorization_readiness.md` refer to the exact
paths listed above.

The checkout HEAD is the requested baseline. The review did not execute,
import, dot-source, compile, test, preflight, or invoke either implementation;
it did not call Windows APIs or create a token, job, process, or thread. No
runtime result is inferred below. The untracked
`scripts/luna65_phase2a_supervisor.py` is an excluded scaffold, not evidence
for the RP-2 probe implementation.

### Status vocabulary

- **Supported:** the narrow source/contract statement is present and correctly
  described; this is not runtime proof.
- **Qualified:** a source branch or static design exists, but the prior report
  overstated its reach, completeness, or guarantee.
- **Unsupported:** the source and reviewed contract do not establish the
  stated conclusion.
- **Incorrect:** the claim contradicts the inspected source, contract, or
  readable/verified evidence.

## Audit of material prior claims

| Prior claim / location | Status | Corrected static finding and evidence |
|---|---|---|
| The report is a clean, auditable source record; opening metadata and code excerpts are intact (prior report lines 1–34, §§4.2–4.3, 7.3). | **Incorrect** | Luna-0 found 9 NUL bytes, 16 other non-whitespace control bytes, a malformed opening YAML fence, and corrupted identifiers/excerpts. It found the concrete `PSS_HANDLE_ENTRY` discrepancy as well. The historical report cannot serve as its own reliable evidence trail (Luna-0 review `:240-258`). |
| Six-path Git/source identity proves the source claims and supports Lane C PASS (prior report lines 41–66, 378–386). | **Qualified** | The readiness package records the requested baseline and source-pair identities (`rp2b_authorization_readiness.md:6-24`); Luna-0 independently cross-checked the candidate identities (`rp2b_luna0_independent_review.md:29-45`). Git identity establishes which bytes were reviewed, not correctness of embedded metadata or contract compatibility. The probe emits `BASELINE = "f47c48a947e48867c629817fa1031cb93729e440"` (`probe.py:16, 1362-1365`), which is not the requested `96fb4aec...` baseline. The frozen contract requires binding the commit and reviewed probe/literal (`contract.md:111-119`). This is a source/provenance inconsistency, not a runtime observation. |
| All native declarations and x64 structures strictly conform to the Windows ABI; New-Interop validates all 33 method bindings and immediately rejects a missing export (prior report §§4.1–4.4, especially lines 140–153). | **Unsupported; the PSS size/count details are incorrect** | The probe explicitly defines structures and checks selected sizes in its x64 guard (`probe.py:283-362`); the wrapper declares P/Invoke return/argument types (`outer_wrapper.ps1:210-333`). Those are static declarations/guards, not independent SDK conformance tests or runtime ABI verification. `PROCESS_INFORMATION` 24 bytes, `STARTUPINFOEX` 112, and job extended-limit structure 144 are the source’s asserted x64 sizes; retain them as source assertions only. The report’s specific `PSS_HANDLE_ENTRY = 128` is **incorrect**: the probe’s structure plus guard say 136 bytes (`probe.py:341-362`), corroborated by Luna-0 (`workflow/handoffs/rp2b_luna0_independent_review.md:250-258`). The wrapper list contains 34 declaration tuples (`outer_wrapper.ps1:220-253`), and `New-Interop` creates the type/delegate/reader then returns them (`:320-333`); it does not contain the report’s stated 33-entry/API-export preflight. Thus the report’s count and “missing export immediately triggers” claim are unsupported/incorrect. No API declaration is runtime certified. |
| Optional PSS and NT interfaces always degrade safely to PARTIAL (prior report §4.2, lines 128–138). | **Qualified / partly incorrect** | Once `Native` and `Controller` exist, the top-level handler maps selected PSS errors 50/120 and selected `NtQueryObject` statuses to `partial` (`probe.py:1743-1781`). This is conditional error mapping, not general graceful degradation. `Native()` is constructed before the handler around controller execution (`probe.py:1743-1757`); missing exports or ABI/setup failure there are not covered by that mapping. A PSS call that stalls is not an “unsupported” return and can leave an unjoined worker; it is not guaranteed PARTIAL. |
| Process/thread access rights, suspended admission, and pre-resume checks are strictly ordered and thereby validated (prior report §§5.1–5.2). | **Qualified** | The wrapper requests suspended creation (`outer_wrapper.ps1:872-875`), reads back retained P/thread identities and token state, starts readers, closes the parent write ends, performs final readback, then marks and calls `ResumeThread` (`:881-933`). The probe creates the Low child suspended with a creation-time handle/job attribute list, records returned handles, checks job membership and token/inventory state, and resumes later (`probe.py:1241-1290, 1400-1450`). This establishes intended source ordering only. API results, rights, descriptor semantics, scheduler ordering, or successful suspension are not proven by reading code. A failure before or during any step must be classified from actual observations; no static PASS follows. |
| Explicit handle allowlists prevent all unintended inheritance throughout the complete Low process tree (prior report §5.3, lines 173–182). | **Incorrect as a chain-wide/runtime claim; supported only at the direct creation boundaries in source** | O supplies a two-handle `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` to its direct `CreateProcessW` call (`outer_wrapper.ps1:850-872`). P supplies three pipe-write handles and a `JOB_LIST` to its direct `CreateProcessAsUserW` call (`probe.py:1241-1277`). These are source-level controls on those direct calls; they do not prove all descendants or runtime inheritance behavior. The historical contract §10.3 describes the stock venv-launcher root→base generic-inheritance topology (`contract.md:570-606`), but later owner decision D-RP2-DIRECT-1 accepts a hash-bound direct-base executable for this diagnostic's design only (owner decisions §2, D-RP2-DIRECT-1). Accordingly, do not characterize the current direct-base design choice as an unresolved venv-topology contradiction. Neither the decision nor static handle lists establish runtime inheritance, source-to-binary behavior, or RP-2B execution authority. |
| All handle ownership, pipe-end closure, EOF, and lifecycle cleanup are guaranteed (prior report §§5.3–5.4, 6.4–6.5). | **Qualified** | Source explicitly tracks owned handles and checks selected flags/access (`outer_wrapper.ps1:348-370`; `probe.py:940-960, 966-978`); O closes its direct child write copies before resuming P (`outer_wrapper.ps1:913-933`); P closes Low write copies before resuming (`probe.py:1430-1450`). Readers treat broken-pipe error 109 as EOF (`outer_wrapper.ps1:210-333` reader IL; `probe.py:1706-1741`). These are intended direct-boundary mechanics, not proof that all writers/descendants terminated or every close succeeds. Contract requires EOF plus process/job evidence and explicitly says missing EOF/cessation is UNKNOWN (`contract.md:173-174, 291-313`). |
| Reader and token-query workers are bounded, cancellable, joined, and their runspaces/resources cannot race cleanup (prior report §§5.4, 6.2, 6.5, 8 R-08/R-14, 9.2). | **Incorrect as a guarantee; partial ownership controls are supported** | O readers are native threads running emitted IL that calls synchronous `ReadFile`; O token-query workers are native threads executing a PowerShell pipeline in a dedicated Runspace configured `UseCurrentThread` (`outer_wrapper.ps1:512-584`). In `finally`, O requests `CancelSynchronousIo` for reader threads and waits at most the remaining portion capped at 100 ms; token-query workers receive only an immediate zero-time wait, with no cancellation call or bounded join (`:964-984`). O retains pinned callbacks/resources when workers remain unjoined (`:984-991`), and the result is incomplete/UNKNOWN when outstanding workers remain (`:997-1005`). P similarly uses native worker threads; cleanup requests cancellation and performs a short bounded wait, defers owned-resource/job closure while workers remain, and includes outstanding workers in its cessation predicate (`probe.py:1524-1650, 1657-1741`). Retention reduces use-after-free risk but does not prove a blocked PSS call or query runspace will stop. |
| The 10/5/20-second schedule is a strict monotonic hard stop (prior report §6.1 and R-11). | **Qualified; “hard” is unsupported** | The source uses `GetTickCount64`, a P active end of `min(P0+10s,O0+20s)`, and cleanup end `min(F+5s,P0+15s,O0+20s)` (`probe.py:848-916`). O polls, requests exact-handle P termination at its 15-second stop cutoff, and bounds its follow-up loop by the 20-second outer deadline (`outer_wrapper.ps1:934-963`). Contract §5 requires these latest cutoffs and says they are not hard real-time guarantees (`contract.md:284-313`). Timers do not guarantee a native call, worker, finalizer, or OS termination completes by a deadline. Reaching cutoff without required cessation observations is UNKNOWN, not a proven stop. |
| One outer `TerminateProcess` request and P’s `TerminateJobObject`/root termination guarantee cessation (prior report §§6.2–6.3, R-04/R-11/R-12). | **Qualified** | `Stop-Exact` is idempotent and calls `TerminateProcess` at most once on retained P when its wait says active; the source records that it is not cessation proof (`outer_wrapper.ps1:754-767`). P requests `TerminateJobObject` when its job is nonzero and separately requests `TerminateProcess` for an unassigned, unsignalled suspended root (`probe.py:1524-1545`). P then polls retained root/job state and drains streams; its final cessation predicate requires known creation result, root signal, job zero, all three EOFs, no unknown descendant, no outstanding worker, no owned handles, and freed descriptors (`probe.py:1560-1645`). These are conditions for reporting a result, not guarantees that Windows honors a request or that the tree stopped. |
| Deferral of P’s job close keeps the containment umbrella active as long as any probe worker is alive (prior report §6.5, lines 226–233). | **Qualified; the stated guarantee is unsupported** | P closes non-job resources and then its job only when no worker is outstanding (`probe.py:1611-1629`); O likewise avoids freeing its registered backing resources while a reader/query worker is unjoined (`outer_wrapper.ps1:984-991`). This is a deliberate retention branch. A job handle close or termination request still does not prove descendant cessation, and O can terminate P; contract and Luna-0 expressly limit this to best-effort semantics (`contract.md:285, 291-313`; `luna0_review.md:260-267`). |
| O independently observes Medium only; missing required Low evidence is UNKNOWN and alerts (prior report §7, lines 239–305). | **Supported with strict scope** | O records `O_independently_observes_Low=$false` and requires P-reported cessation, Low signal/job-zero, three Low EOFs, no outstanding worker/owned handle, plus O-side P signal/EOF/worker conditions (`outer_wrapper.ps1:83-85, 993-1005, 1018`). If any required Low or outer condition is unknown, O sets `RP2_UNKNOWN_FAIL_CLOSED` and calls `Alert-Unresolved` (`:1001`; alert text `:83-85`). This is the required rule: **Medium cessation is not Low cessation; missing or unreliable Low cessation evidence is `RP2_UNKNOWN_FAIL_CLOSED` and requires an operator alert.** The alert is a console write, not proof of delivery or inclusion in the accounted evidence artifact (`:83-85, 1018-1038`; Luna-0 `:260-267`). The narrow source branch that treats `ResumeAttempted == false` as no Low exposure is valid only if the Medium process is statically known never to have been resumed; it must never excuse missing Low evidence after P may have run (`outer_wrapper.ps1:929-933, 993-1001`). |
| PSS/NT inventories and 256-entry caps prove complete, race-free handle state (prior report §§4.2, 5.3, R-07–R-08). | **Unsupported as an absolute claim** | P captures and walks PSS handle snapshots, rejects the 257th entry rather than silently treating a capped list as complete, checks required basic information, and compares finite inventories (`probe.py:1115-1225`). O requires parent/suspended/READY inventory completion before its PASS predicate (`outer_wrapper.ps1:997-1005`). Snapshot checkpoints cannot prove that a transient handle never existed, bound snapshot-call latency, or observe an object outside the captured process; contract §10.4 preserves these caveats and requires checkpoint-specific comparisons (`contract.md:627-638`). A missed/unsupported observation with confirmed cessation is at most PARTIAL; unknown worker/process/EOF state is UNKNOWN. |
| Any “normal completion” matrix row is a statically guaranteed PASS (prior report §8 R-01). | **Unsupported** | The PASS branches are present (`probe.py:1629-1645`; `outer_wrapper.ps1:993-1005`), but PASS requires actual successful creation/exit, all required observations, complete EOF/cessation and cleanup evidence under the accepted contract (`contract.md:358-366`). No such runtime outcome was obtained. |
| Cleanup, output, memory, or evidence limits cannot overrun and all finalization is safe (prior report §8 R-10/R-13 and §10, lines 357–373). | **Unsupported / qualified** | Source caps individual records and retained logical representations, reserves finalization space, records accounting high-water, and rejects extension past configured limits (`probe.py:23-35, 890-938`; `outer_wrapper.ps1:22-27, 604-640, 1006-1038`). These are source-level checks, not an OS memory/filesystem quota or worst-case proof that every required artifact fits. The readiness package correctly leaves worst-case fit unresolved (`rp2b_authorization_readiness.md:35-56`); Luna-0 also notes console alert output is outside the artifact writer (`luna0_review.md:260-267`). A finalization failure can prevent a usable report; it cannot be reported as PASS. |
| No source-level ambiguities or blocking defects remain; the implementation is strictly aligned with the frozen contract (prior report §§9–11, lines 332–389). | **Incorrect** | The corrupted report, PSS size error, and unsupported ABI/lifecycle guarantees invalidate its PASS. Separately, the embedded `BASELINE` equals the reviewed source commit's parent and the RP-2A handoff's `base_revision`; it is not a mismatch with reviewed `HEAD` (`96fb4aec...`). The direct-base executable is accepted by later owner decision D-RP2-DIRECT-1 for diagnostic design only; that decision is not a contract amendment, runtime qualification, or RP-2B grant. O's token-query worker also lacks the report's asserted cancellation/join guarantee. Thus the historical PASS remains rejected, but the baseline/direct-base observations themselves are not additional unresolved design contradictions. See the corrected source/profile rows following this audit and the owner decision file, §2, D-RP2-DIRECT-1. |

## Corrected assessment

### Reviewed revision versus source baseline and direct-base design

The probe's `BASELINE = "f47c48a947e48867c629817fa1031cb93729e440"` denotes
the source commit's parent (`HEAD^`) and matches the RP-2A handoff's
`base_revision`; it is not the reviewed `HEAD`, which is separately bound by
revision and source identities. This is **not** a mismatch on the reviewed
evidence. Preserve the distinction in provenance; do not edit the embedded
field or call it a contract defect.

The historical RP-2 text retains venv-chain language, but later owner decision
D-RP2-DIRECT-1 accepts the hash-bound direct-base executable for the bounded
diagnostic **design only** (owner decisions §2). Treat the direct-base design
choice as adjudicated for design, not as an unresolved design contradiction.
That decision does not amend the frozen contract, qualify runtime behavior,
or authorize RP-2B. A future grant must bind that accepted design and exact
source/literal/interpreter identities. No venv, production-import, or runtime
compatibility claim follows.

The prior report’s PASS and “static guarantee” language is withdrawn. Narrow
source facts remain useful: there are explicit direct-child suspended-create
paths, per-boundary handle lists, retained process/thread handles, bounded
polling, termination requests, cleanup branches, and an explicit outer
Medium-only observer with an UNKNOWN alert branch. None proves successful ABI
behavior, complete isolation, hard deadlines, worker cancellation, OS
termination, or Low/tree cessation.

For classification, preserve the frozen precedence: unknown process/Low
cessation state is **`RP2_UNKNOWN_FAIL_CLOSED`** first; with cessation
confirmed, a source/profile/authorization contradiction is
**`RP2_CONTRACT_DEFECT`**, then a demonstrated mismatch is **`RP2_FAIL`**, an
incomplete observation without a demonstrated mismatch is **`RP2_PARTIAL`**,
and only all accepted observations can support **`RP2_PASS`**
(`contract.md:358-366, 629-631`). The detailed conditional cases are in
`rp2b_race_classification_corrected.md`.

Static limits: this correction does not establish actual host/API/ABI results,
source-to-binary correspondence for the venv launcher, access semantics,
worker completion, real timing, child/descendant termination, alert delivery,
or maximum-size evidence fit. No implementation, frozen contract, historical
artifact, or existing readiness artifact was changed.

**RP-2B EXECUTION: NOT AUTHORIZED.**  
**DOWNSTREAM QUALIFICATION: NOT AUTHORIZED.**
