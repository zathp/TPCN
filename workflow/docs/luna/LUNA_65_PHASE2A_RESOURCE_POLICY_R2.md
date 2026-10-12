# Luna-65 Phase 2A Monitored Resource-Policy Amendment — R2

**Gate identity:** `L65-PHASE2A-MONITORED-RESOURCE-POLICY-R2`

**Status:** **GOVERNANCE/DESIGN ONLY — IMPLEMENTATION AND EXECUTION NOT
AUTHORIZED.** The owner accepted the policy below for the Phase 2A
qualification design. This R2 amendment specifies monitored CPU and wall
budgets, while retaining hard job-wide memory and retained-artifact ceilings.
It does not qualify a supervisor or authorize any synthetic qualification,
Phase 2A fixture, Phase 2B fixture, or benchmark.

## 1. Authority and verified baseline

| Item | Identity |
|---|---|
| Branch | `governance/luna64-r4.3-freeze-20261010` |
| Baseline HEAD | `eaa55bdd777da348ed317360f1482eb00b3e279c` |
| Prior published Phase 2 capacity contract | SHA-256 `51BE7271DB57E0AFF9E9ED8BB317382D49F22C53BC8E1D13667FAED893BE76CB`; Git blob `b785ae680bd239d86fbbbe62951aed8caf0abf32` |
| Historical R1 supervisor design | SHA-256 `7DD5EE88EDAC1AF9049C265D28B8E60DD1558AD80D2EC760575D25DE6FB4D93D`; Git blob `1fa07ffc844a5890c9ecc86563243993725fb1b2` |
| Authoritative workflow at baseline | SHA-256 `43A6D957A0EDBC368F08D3642A5EB3DB8E4843B2A52C17E057F3168A5E17A93E`; Git blob `9502a45aea7d3e14f7d062fb59f755c60ba83c2a` |
| Phase 2A correction handoff | SHA-256 `459E4AC9CAC322A88BF580F2F1016082FEF7E7C9A69369C0322BA7305181E684`; Git blob `8be29e8aab67084e1c3a9a73c9c1564b3ec7c2c9` |
| Phase 1 closure handoff | SHA-256 `4B4D7BF378C3C38FFC755106ECE597A6FBEEA9EC712CFB5AFF105989E680E022`; Git blob `56807d7c3b22224742cfccb435271ba219852b0b` |
| Phase 1 implementation `tpcn/experiments.py` | SHA-256 `CABB81DA36280E7CDCF614B8B3E2CD5567035C20C6706A85B25B1A73310E967D`; Git blob `7c915fb92f05725f4a46855f856ecb3e650cd44b` |
| Phase 1 runtime `tpcn/experiment_excursion_runtime.py` | SHA-256 `DF007154939C6C554A3D914C15CE91C87954BEEEBF29DF416EE27D138F119D5A`; Git blob `ecf65095f272f5e94b328c6d17aa7d6c73d02373` |
| Phase 1 focused test | SHA-256 `DE32193D0E87059E995331E6B490DBEFD26020EB11C9EAFF3EBD27316D4C7D1D`; Git blob `53bb0c75909fa0ab5098e98891a05f2c8d88500e` |
| Luna-65 Spiral contract | SHA-256 `1F1D4DD96E21EE760D32CDDE4F0415576C9BAE6AF01B82DB2A9C4E1D9FB5C777` |

The Phase 2A correction and Phase 1 closure are referenced as provenance;
their test evidence is not rerun or upgraded here. The independent R1 review
dispositions are preserved in the workflow at baseline `eaa55bd`: Windows
API correctness PASS on the Q05 design, supervisor fail-closed framing
PASS, evidence/artifact structure PASS WITH CLARIFICATIONS, and
governance/provenance PASS. Those findings did not establish resource
enforcement, ledger fit, or supervisor qualification. This R2 does not edit
or supersede that historical R1 record; it narrows the Phase 2A policy as
accepted below.

The architecture contract and changelog are unchanged: this is execution
resource governance, not a TPCN computation or architecture change. The
Phase 2 capacity contract remains the authority for the four direct-neuron
counter fixtures and the 8,196 target-counter-probe maximum.

## 2. Explicit owner acceptance

**Owner decision date:** 2026-10-12.

The owner accepts the following **for Luna-65 Phase 2A qualification
design only**:

> **Aggregate CPU:** budget 120 seconds cumulative job-wide user-plus-kernel
> CPU. A trusted supervisor monitors Windows Job Object aggregate CPU
> accounting and requests whole-job termination when its observed value
> reaches or exceeds the configured stop threshold. Any observed value above
> 120 seconds is a failed result. This is not a strict zero-overshoot
> guarantee.
>
> **Wall time:** budget 120 seconds elapsed. A trusted supervisor uses a
> monotonic clock and an early termination trigger. The design must specify
> a stop margin, escalation, actual termination observations, and a bounded
> monitoring schedule. No stop-margin value has been approved. Any observed
> budget overrun is a failure; a termination request does not guarantee
> cessation at exactly 120 seconds.
>
> **Memory:** retain the hard ceiling of 268,435,456 bytes, measured as
> aggregate concurrent job-wide private committed memory and enforced using
> the appropriate Windows Job Object limit. Read back effective limit flags
> and byte values. Per-process memory limits and working-set accounting are
> not substitutes.
>
> **Retained artifacts:** retain the hard combined ceiling of 1,048,576
> bytes across every artifact covered by the Phase 2A contract. Distinguish
> emitted, captured, and retained bytes; a pipe-output limiter is not a
> limit on every byte emitted before termination.
>
> **Retries:** zero. **Scope:** Phase 2A direct-neuron capacity verification
> only. This acceptance does not automatically apply to Phase 2B.

This acceptance changes the required CPU and wall enforcement semantics
from the hard limits proposed in R1 to monitored budgets with fail-on-
observed-exceedance. It does not relax the hard memory or artifact limits,
authorize a stop-margin value, resolve engineering evidence, or authorize
implementation or execution.

## 3. Scope and preserved boundaries

This amendment is only for **Phase 2A direct-neuron capacity fixture**:

- At most 8,196 target-counter probes, as specified in the Phase 2 capacity
  contract; coupled identity-counter changes remain separately recorded.
- Exact Phase 2A command, working directory, per-counter initial conditions,
  JSONL schema, and evidence destination remain unchanged except where this
  amendment adds resource-observation fields and the controller-owned
  evidence transport requirement.
- No neural computation, predictive coding, reward, learning, structural
  plasticity, readout, test schedule, or benchmark protocol changes.
- No implementation, supervisor qualification, fixture execution, E2
  capacity probe, dataset generation, training, evaluation, or scoring is
  authorized.

Phase 2B retains its separate authorization and is not changed by this
amendment. The earlier R1 supervisor document remains the historical
qualification-design record; its Phase 2B resource expectations are not
amended by the Phase 2A owner decision. Luna-12G remains historical
`TANH_LEGACY`; full Spiral remains blocked; Simon Says remains source
recovery only; Luna-64 corrective execution remains blocked; Luna-63C
remains frozen and untouched.

## 4. Monitored termination semantics

These are requirements for a future implementation, not demonstrated
behavior.

### 4.1 Clock and accounting boundaries

- Use `QueryPerformanceCounter` (QPC) and retain
  `QueryPerformanceFrequency`; do not use wall-clock time for elapsed
  duration.
- Set `T0` at the trusted supervisor's first main-entry instruction. Record
  the invoking host's process-start observation separately because time
  before supervisor user code is not available to that process.
- The wall budget starts at `T0`. Record preflight, admission, workload,
  termination/reaping, pipe drain, and evidence finalization timestamps.
  Record **workload cessation time** as the QPC observation when the job is
  signaled and has zero active processes. Also record **supervisor
  completion** after evidence finalization. Any observed elapsed interval
  exceeding 120 seconds is a failed wall-budget result.
- The workload CPU interval starts when the first assigned workload thread
  is resumed and ends only after all job processes have ceased. Query the
  job's final totals after cessation. Controller, watchdog, and observer
  CPU are separately observed and excluded from the workload-job CPU total.
- Query `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION` using
  `QueryInformationJobObject`; record raw `TotalUserTime` and
  `TotalKernelTime` in 100-nanosecond units and their sum in raw ticks and
  seconds. The tick unit is a representation, not a guarantee of counter
  update resolution. Qualification must characterize observed granularity,
  update delay, query delay, and any counter regression/discontinuity.

### 4.2 CPU monitor and trigger

- Target a 10-ms QPC-based sampling cadence from first workload resume until
  the job is confirmed empty. Retain bounded evidence: QPC frequency,
  configured cadence, sample count, maximum observed query gap and its
  endpoints, threshold-bracketing samples, final user/kernel totals, and
  termination/exit timestamps. Do not retain an unbounded sample trace.
- The configured CPU stop threshold is **120 seconds** (1,200,000,000
  100-ns units). As soon as a sample reports
  `TotalUserTime + TotalKernelTime >= 1,200,000,000`, request whole-job
  termination. Do not wait for the next polling interval after detecting a
  crossing. Re-query after termination and after process cessation.
- A sample interval is a target, not a real-time guarantee. Qualification
  must declare a maximum acceptable monitoring gap; the R2 proposal is
  **100 ms**. A gap above that value, missing/regressing accounting, or
  monitor failure makes CPU compliance inconclusive and triggers immediate
  termination. It is not a claim of zero overshoot.
- If final observed job CPU is greater than 120 seconds, classify
  **CPU_BUDGET_EXCEEDED**, even if termination was requested at the first
  sample at/above threshold. If the observed total equals the threshold and
  the job is stopped, record a threshold-triggered termination, not a strict
  enforcement proof. Report actual CPU at cessation and overshoot relative
  to the budget; never success-shape an overrun.

### 4.3 Wall monitor, early trigger, escalation

- Target the same 10-ms QPC monitoring cadence, using an independent
  watchdog heartbeat/deadline monitor outside the workload job.
- **Proposed, not owner-approved:** use a five-second stop margin,
  `T_stop = T0 + 115 seconds`. At that trigger the primary requests
  `TerminateJobObject` for the complete workload job. The five-second
  margin is a design candidate only; a separate owner decision must accept
  an exact margin before implementation or qualification.
- If the primary does not heartbeat within 100 ms, exits, or cannot issue
  termination, the watchdog requests whole-job termination. The watchdog
  repeats termination on a failed wait or still-active job, records every
  request/result, and continues observing until process cessation or a
  declared qualification wait expires. Repetition is escalation, not a
  retry of the workload.
- A second monotonic wall trigger at `T0 + 120 seconds` is a final
  escalation point, not proof of cessation. Record deadline reached,
  request time, `TerminateJobObject` return/error, job-signaled observation,
  active-process count, individual process exits when available, pipe EOF,
  final resource sample, evidence flush/hash completion, and supervisor
  completion.
- If cessation is not confirmed by the predeclared qualification wait,
  classify **TERMINATION_UNCONFIRMED** and **EVIDENCE_INCOMPLETE**. Any
  observed workload cessation or supervisor completion after `T0+120
  seconds` is also **WALL_BUDGET_EXCEEDED**. A request to terminate is
  never reported as proof of exit.

## 5. Hard job-wide memory limit and containment

### 5.1 Memory requirement

- Configure `JOBOBJECT_EXTENDED_LIMIT_INFORMATION.JobMemoryLimit` to exactly
  **268,435,456 bytes** and set `JOB_OBJECT_LIMIT_JOB_MEMORY` in
  `BasicLimitInformation.LimitFlags`. Read back and record the effective
  `LimitFlags` and `JobMemoryLimit` before resuming the workload.
- Do not substitute `JOB_OBJECT_LIMIT_PROCESS_MEMORY`, working-set limits,
  notifications, or the sum of individual process peaks.
- Independently sample each concurrently live job process's
  `PROCESS_MEMORY_COUNTERS_EX.PrivateUsage`, sum the live private commit,
  and retain current/peak observations, query times, job memory usage/peak,
  commit-failure observations, and process lifecycle. Demonstrate that the
  enforced Job Object committed-memory limit prevents the accepted
  aggregate-concurrent-private-commit metric from exceeding the exact
  ceiling on the target Windows build. The mapping is not assumed: if the
  metrics do not reconcile or a process is unaccounted, classify
  **MEMORY_LIMIT_EXCEEDED** or **RESOURCE_MEASUREMENT_INCONCLUSIVE** and do
  not qualify the supervisor.
- At a commit denial near the ceiling, the synthetic worker reports the
  failed request through the trusted evidence channel. Job-memory denial
  alone is not presumed to terminate the process. If the configured limit
  is crossed, terminate the entire job and fail the run.

### 5.2 Admission and process-tree containment

The future supervisor must use this fail-closed sequence:

1. Validate exact repository revision, clean source, supervisor/watchdog/
   observer identities, Python and pytest identities, fixture hash, command,
   working directory, environment, evidence path, and owner-approved profile.
2. Create a fresh unnamed job with a restrictive security descriptor.
   Set `JOB_OBJECT_LIMIT_JOB_MEMORY` and
   `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; do not set
   `JOB_OBJECT_LIMIT_BREAKAWAY_OK` or
   `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK`. Record every requested and
   read-back limit flag/value.
3. Require controller and independent watchdog ready before admission.
   Create the exact child suspended using an explicit inherited-handle list;
   assign it to the job and verify with `IsProcessInJob` and job process-list
   accounting before `ResumeThread`.
4. Do not pass the job handle, controller-process handle, or evidence
   directory write access to the workload. Restrict process creation and
   handle duplication rights so the workload cannot create a breakaway
   child or retain a job handle. Test `CREATE_BREAKAWAY_FROM_JOB` behavior;
   an observed escape is a containment failure and remains gated on the
   separate Q03 recovery protocol below.
5. Child/grandchild association is expected to inherit job membership only
   when breakaway and applicable nested-job rules allow it. Confirm every
   reported child while held at a barrier with `IsProcessInJob`; reconcile
   active-process counts and an independent process observer. Do not infer
   containment from parent PID alone.
6. On any pre-resume mismatch, terminate the suspended child and do not
   launch the test. On a runtime failure, issue `TerminateJobObject`, wait
   on the job handle, query active process count, and confirm zero members.
   The successful API return alone is only a request result.
7. Retain the final job handle in trusted controller/watchdog ownership.
   `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` is a last fallback only; it is not
   evidence of cessation until job signaled/zero active members are
   observed. Qualification must verify inherited-handle restrictions,
   breakaway behavior, controller crash, watchdog failure, and final-handle
   closure. System/kernel/power/disk failures can prevent evidence finality.

OS settings provide configured controls, not a blanket proof: nested-job
composition, process ACLs, handle lists, breakaway behavior, and memory
metric equivalence all require target-host qualification. No containment
control has been implemented or tested for R2.

## 6. Deterministic result and failure classification

The controller records a first failure reason and all subsequently observed
failures. `failure.json` is required for every incomplete or failed result.
The run can be successful only if all predeclared fixture assertions pass,
all resource budgets are observed within limits, the job is empty, and
required evidence is complete and hash-verified.

| Classification | Trigger and required outcome |
|---|---|
| `CPU_BUDGET_EXCEEDED` | Final observed job CPU exceeds 120 s, or a sample reaches the threshold and the termination result shows exceedance. Request/continue whole-job termination; result fails. |
| `WALL_BUDGET_EXCEEDED` | Observed job cessation or supervisor completion exceeds `T0+120 s`. Result fails, even if termination succeeded. |
| `MEMORY_LIMIT_EXCEEDED` | The observed accepted private-commit measure exceeds 268,435,456 bytes, or observed job commit crosses the configured hard limit. Terminate job; fail. |
| `ARTIFACT_LIMIT_EXCEEDED` | Any governed retained byte would exceed the 1,048,576-byte reservation. Stop admission/probes, request termination, continue bounded drain/discard, and mark evidence incomplete. |
| `CONTROLLER_FAILURE` | Primary monitor/writer exits, stalls beyond heartbeat limit, or reports an internal error. Watchdog terminates the job; failed watchdog escalation also makes termination unconfirmed. |
| `PROCESS_CONTAINMENT_FAILURE` | Any running process is outside the assigned job, breakaway succeeds contrary to the approved profile, membership cannot be reconciled, or an unauthorized process/command is admitted. |
| `TERMINATION_UNCONFIRMED` | No verified job signal and zero active members by the predeclared wait; a request/API return is insufficient. |
| `EVIDENCE_INCOMPLETE` | Mandatory record, manifest, resource observation, failure record, output status, or digest is missing/partial/unverifiable, including controller/host/storage failure. |
| `RESOURCE_MEASUREMENT_INCONCLUSIVE` | Required Job Object memory flags/value are absent or incorrect; accounting gaps/regression, unavailable counters, unresolved private-commit metric relationship, unaccounted process, or monitor interval beyond its accepted maximum prevents a valid determination. |
| `FIXTURE_FAILURE` | Any Phase 2A expected identity, exception, state, count, or serialization assertion differs. No retry or scientific success claim. |

Where more than one applies, preserve all observed classifications and
identify the first trigger separately. No failed/incomplete run can be
reported as a scientific success or a passing capacity result.

## 7. Controller-owned evidence and retained-artifact limit

### 7.1 Data path

The fixture process receives no writable evidence path. It sends versioned,
length-prefixed records over a dedicated inherited pipe to the trusted
controller-side writer. The controller validates schema version, record
order, bounded message length, probe index, and required fields, then
serializes canonical UTF-8 JSONL and streams it directly through gzip to a
single same-directory `.part` file. On successful completion it closes,
flushes, hashes, and atomically renames the file; it never retains a raw
JSONL copy or simultaneous full staging/final copies. A partial `.part` file
is retained only with an explicit incomplete status and counts in full
toward the cap.

The controller alone has write access to the unique external evidence
directory. The workload can only write bounded messages to controller-owned
pipes. The controller checks all per-file and aggregate quotas before each
disk write. Pipe bytes emitted (when independently knowable), bytes read,
bytes retained, and bytes drained/discarded are distinct measurements.
Readers continue draining/discarding after a retention threshold to prevent
pipe deadlock; this does not imply a hard cap on emitted bytes.

### 7.2 Proposed allocation

| Retained object | Hard allocation (bytes) |
|---|---:|
| `results.jsonl.gz` | 786,432 |
| `stdout.txt` | 32,768 |
| `stderr.txt` | 32,768 |
| `manifest.json` | 16,384 |
| `resource.json` | 16,384 |
| `failure.json` | 8,192 |
| `sha256.json` | 8,192 |
| Aggregate slack | 147,456 |
| **All simultaneous retained/staging files** | **1,048,576** |

Metadata/failure reservations are held before admission. Every partial,
temporary, or intermediate retained file counts. The `.part` to final rename
is same-volume atomic and creates no second copy. No other scratch artifact
may remain. The writer stops before the next write that would exceed any
allocation or the combined cap, records `ARTIFACT_LIMIT_EXCEEDED`, terminates
the workload, drains/discards bounded pipe data, and retains only complete
records plus an explicitly invalid partial stream if space permits. It never
truncates and reports a complete ledger. A failure record is written from
reserved bytes; absence of any required record is `EVIDENCE_INCOMPLETE`.
`sha256.json` contains lengths and SHA-256 for all finalized evidence files
except itself; its own digest is recorded in the external archive receipt
after transfer.

The maximum counts apply to retained artifacts; controller memory buffers
are governed by the hard memory requirement and must also be bounded.
Arbitrary workload filesystem writes are prevented by identity/ACL, not by
Job Object artifact quotas.

### 7.3 Ledger sizing gate

The Phase 2A schema requires exactly 8,196 records for a complete run. R1's
source-based planning estimates were 4,098,000 bytes even at an invalid
compact structural floor, 8,093,550 bytes at its likely mixed estimate, and
16,777,216 bytes at the conservative planning envelope. These are not
formal bounds. The 768-KiB ledger allocation requires at least 10.29:1
compression even against the 8,093,550-byte likely estimate; no such ratio
is assumed. Current schema values do not impose a proven byte maximum for
every serialized state/checkpoint value.

**Conclusion:** exact complete-ledger fit within 786,432 bytes is not
established analytically. Before fixture implementation or execution, require
a separate owner-authorized synthetic sizing check using a frozen,
byte-bounded record-shape/writer addendum. It must produce no neuron, counter
allocation, Phase 2A probe, benchmark datum, or task example. It must retain
the exact 8,196 versioned JSONL record shapes, gzip framing/settings,
maximum single-record size, raw and compressed byte counts, peak
simultaneous disk bytes, Python/zlib versions, and input-shape digest. The
test passes only if all mandatory fields are represented losslessly and all
simultaneous files fit their allocations and the combined 1-MiB cap. No
favorable ratio may be presumed. If the result exceeds any cap, stop and
seek a lossless schema/representation revision or explicit owner-approved
artifact-budget amendment; no records may be dropped or truncated.

The existing Phase 2A environment still needs a reviewed complete inherited-
variable policy. R2 does not silently resolve it.

## 8. Separately authorized synthetic qualification plan

The qualification plan is **not authorized or implemented**. It is separate
from Phase 2A and Phase 2B, and does not use the 8,196 Phase 2A probes.
Future implementation requires a new exact owner authorization naming the
supervisor and test hashes, host build, budgets, evidence path, and all
cases. Proposed invocation, from the repository root, is exactly:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -x tests\test_luna65_supervisor_qualification.py
```

The future test module must invoke only the exact trusted supervisor
executable and the fixed synthetic worker profile
`tests\fixtures\luna65_supervisor_worker.py`; no shell strings, arbitrary
commands, E2 modules, datasets, network access, or benchmark inputs. Each
case is invoked once with one fixed `--case` value. The exact synthetic
worker command template is
`.\.venv\Scripts\python.exe -I -S tests\fixtures\luna65_supervisor_worker.py --case <case>`;
the supervisor constructs this argument vector directly, without a shell.
Substitute only the ten literal case values shown in the matrix below.
This names proposed paths only; neither file currently exists. Pin and record executable,
supervisor, watchdog, observer, test, worker, Python, pytest, OS build,
checkout, argument vector, and environment hashes/values.

| Case | Fixed synthetic scenario | Required observation |
|---|---|---|
| S01 Admission | `--case admission` | Suspended worker does not execute before assignment and effective setting readback; resumes only after `IsProcessInJob`. |
| S02 Descendants/breakaway | `--case descendants` | One child and grandchild remain in-job; breakaway attempt is denied; independent observer and job counts reconcile. An unexpected escape stops the suite under the separately approved recovery procedure. |
| S03 CPU monitor | `--case cpu-monitor` | A reduced 2-second cumulative CPU stop threshold exercises aggregate user+kernel sampling, trigger, termination request, actual totals, overrun classification, and cadence. It does not prove zero overshoot or characterize the 120-second production threshold. |
| S04 Wall monitor | `--case wall-monitor` | Reduced 10-second elapsed budget and proposed 1-second margin exercise QPC scheduling, early trigger, watchdog escalation, actual cessation, and overrun classification. It does not approve the Phase 2A margin or prove hard real-time cessation. |
| S05 Job memory | `--case job-memory` | Readback of exact 268,435,456-byte job-wide setting/flags; commit pressure and private-commit reconciliation; no per-process/working-set substitute. |
| S06 Artifact exhaustion | `--case artifact-exhaustion` | Bounded worker exceeds retained output allocation; controller stops retention at quota, continues drain/discard, terminates, and records incomplete status with no overflow. |
| S07 Evidence integrity | `--case evidence-integrity` | Normal and forced-incomplete synthetic records, byte lengths, atomic completion, required failure record, and hashes reconcile; no E2 data. |
| S08 Controller failure | `--case controller-failure` | Kill primary controller at barrier; independent watchdog detects heartbeat loss and requests job termination; final process state and evidence loss are classified honestly. |
| S09 Exit confirmation | `--case exit-confirmation` | Whole-job termination of a child tree; distinguish API return from signaled job/zero active members and observed last exit; timeout is `TERMINATION_UNCONFIRMED`. |
| S10 Command allowlist | `--case command-allowlist` | Exact future Phase 2A command/profile accepted for validation only; alternate argv, module, cwd, environment, and hashes rejected before process creation; fixture is never launched. |

Per-case resource ceilings are proposed as follows; every case uses the
same shared evidence directory and combined artifact ceiling, not a
per-case allocation:

| Case | Max workload-job CPU (observed) | Max elapsed wall | Hard job memory | Shared retained-artifact ceiling |
|---|---:|---:|---:|---:|
| S01 | 1 s | 10 s | 67,108,864 B | 1,048,576 B |
| S02 | 1 s | 20 s | 67,108,864 B | 1,048,576 B |
| S03 | 5 s | 20 s | 67,108,864 B | 1,048,576 B |
| S04 | 1 s | 20 s | 67,108,864 B | 1,048,576 B |
| S05 | 5 s | 30 s | 268,435,456 B | 1,048,576 B |
| S06 | 2 s | 20 s | 67,108,864 B | 1,048,576 B |
| S07 | 2 s | 20 s | 67,108,864 B | 1,048,576 B |
| S08 | 2 s | 30 s | 67,108,864 B | 1,048,576 B |
| S09 | 2 s | 20 s | 67,108,864 B | 1,048,576 B |
| S10 | 1 s | 10 s | 67,108,864 B | 1,048,576 B |

Proposed total envelope: one pytest invocation; exactly ten cases once;
zero retries/replacements; at most 30 seconds observed workload-job
user-plus-kernel CPU, 360 seconds elapsed controller wall including
finalization, 268,435,456 bytes hard job-memory limit, and 1,048,576 bytes
combined retained artifacts; network disabled. S03 and S04 use reduced
thresholds to test monitor operation within this envelope. Per-case expected
limits, threshold values, stop margins, and a bounded termination wait must
be frozen in the eventual exact owner authorization. A hit on any overall
ceiling stops further cases. This plan does not qualify the full-duration
120-second cutoff by execution; it checks the same monitor path at smaller
declared test thresholds.

Evidence destination, if separately authorized, is a unique external
directory under `%LOCALAPPDATA%\TPCN\evidence\luna65\supervisor-r2\<run-id>\`.
The test output and invocation manifest are retained under the same 1-MiB
combined quota. The proposed working directory is the reviewed repository
root, network access is disabled, and the only currently named override is
`PYTHONHASHSEED=0`; the inherited-environment allowlist/clearing policy must
be frozen in the future exact authorization. No artifacts are created by
this R2 governance task.

## 9. R1 issue reconciliation

| R1 issue | Effect of owner policy | R2 disposition |
|---|---|---|
| 1. CPU accounting and sampling | Resolves the demand for a hard 120-s CPU cap; accepts monitored job-wide user+kernel accounting and observed-overrun failure instead. | **Design specified; engineering evidence required.** Counter update resolution, sampling gaps, process inclusion, monitor health, and actual overshoot must be qualified. |
| 2. Wall monitoring/termination | Resolves the hard cessation-by-120-s requirement; accepts monitored 120-s budget and overrun failure. | **Partially specified.** QPC and escalation are specified. Five-second early margin is only a proposal; exact owner acceptance, schedule qualification, and observed exits remain required. |
| 3. Job-wide private commit | Not changed. | **Unresolved engineering gate.** Exact Job Object metric-to-private-commit relationship and effective hard limit require target-host evidence. |
| 4. Retained-artifact enforcement | Not changed; 1 MiB remains hard. | **Design specified; engineering gate.** Quotas, reservations, atomic single-copy writing, and failure behavior defined; test exact byte accounting. |
| 5. Controller-owned evidence capture | Not changed. | **Design specified; engineering gate.** Bounded framed pipe to trusted writer; prove workload cannot write/bypass ACL or writer quotas. |
| 6. Complete gzip ledger fit | Not changed. | **Unresolved.** No analytical fit; requires byte-bounded schema/writer addendum and separately authorized synthetic sizing. |
| 7. Process-tree containment | Not changed. | **Design specified; engineering gate.** Suspended admission, no breakaway flags, child checks, observer, nested-job behavior, ACL/handle checks must be qualified. |
| 8. Inherited environment | Not changed. | **Unresolved.** Freeze allowlist/clearing policy while preserving `PYTHONHASHSEED=0` and `TPCN_LUNA65_EVIDENCE_DIR`. |
| 9. Q03 outside-job-child recovery | Not changed. | **Unresolved and owner-gated.** Normal breakaway denial is expected; unexpected escaped-child recovery must be explicitly approved and independently reviewed before its case. |
| 10. Process-observer protocol | Not changed. | **Unresolved.** Specify technology, loss detection, polling/event semantics, and resource boundaries. |
| 11. Controller failure/job-handle lifetime | Not changed. | **Design specified; engineering gate.** Separate watchdog, heartbeat, restricted handles, kill-on-close fallback, and complete process/evidence outcomes require qualification. |

## 10. Independent reviews, verdict, and next authorization

Four independent review lanes assessed the R2 design bytes at baseline
`eaa55bdd777da348ed317360f1482eb00b3e279c`:

| Reviewer | Scope |
|---|---|
| A — Windows resource semantics | Job Object CPU accounting units/update behavior; hard job-memory setting and private-commit relationship; suspended admission, descendants, breakaway, nested jobs, and handle containment. |
| B — Termination/failure handling | CPU/wall monitored cutoff, proposed margins, watchdog/escalation, controller loss, process cessation confirmation, and deterministic overrun/incomplete classifications. |
| C — Evidence/artifacts | Exact JSONL record and gzip sizing, writer channel, simultaneous retained-byte accounting, stdout/stderr, partial/failure records, and hash integrity. |
| D — Governance/provenance | Exact owner acceptance, Phase 2A-only effect, Phase 2B and scientific isolation, source/review identities, budget separation, and Luna-63C/Luna-64 boundaries. |

| Reviewer | Disposition | Findings retained as gates |
|---|---|---|
| A — Windows resource semantics | **PASS — design consistency** | Job Object accounting source and configuration are specified; actual CPU update resolution, `JobMemoryLimit` equivalence to aggregate live `PrivateUsage`, and target-build effective readback remain qualification requirements. |
| B — Termination/failure handling | **PASS** | Monitored triggers, escalation, overrun classes, and exit confirmation are coherent; no hard-real-time or exact-cessation guarantee is claimed. The Phase 2A wall margin remains unapproved. |
| C — Evidence/artifacts | **PASS** | Allocation arithmetic and controller-owned writer design are coherent. Exact full-ledger fit is not analytically established and remains gated on the separate synthetic sizing check. |
| D — Governance/provenance | **PASS** | Owner decision, Phase 2A-only scope, Phase 2B separation, exact source identities, no-execution boundaries, and Luna-63C/Luna-64 isolation are preserved. |

**Integrated disposition: PASS — PHASE 2A RESOURCE-POLICY AMENDMENT
VERIFIED.** This confirms governance and design consistency only. It does
not establish supervisor qualification, metric equivalence, exact ledger
fit, resource enforcement, fixture readiness, or authorization to execute.
The reviewers identified no unauthorized scope or execution.

**PASS — PHASE 2A RESOURCE-POLICY AMENDMENT VERIFIED**

or

**BLOCKED — PHASE 2A RESOURCE-POLICY AMENDMENT INCOMPLETE**

A PASS here has only the limited meaning stated above.

Before any implementation, the owner must accept the exact five-second
Phase 2A early wall-stop margin or specify another value and issue an exact
implementation authorization with file/process allowlists. Before
qualification execution, the owner must separately authorize the ten-case
synthetic suite with exact identities, host, resource envelope, environment
and evidence path. Before Phase 2A fixture implementation/execution, the
owner must separately resolve inherited environment, evidence/schema sizing,
memory-metric proof, Q03 recovery, observer design, and issue an exact Phase
2A authorization. No decision here authorizes Phase 2B or benchmark
execution.

## 11. References and validation boundary

- [Luna-65 Phase 2 capacity contract](LUNA_65_PHASE2_CAPACITY.md)
- [Historical R1 supervisor qualification design](LUNA_65_SUPERVISOR_QUALIFICATION_R1.md)
- [Authoritative Luna workflow](LUNA_WORKFLOW.md)
- Windows references listed in the historical R1 design: Job Objects,
  `JOBOBJECT_BASIC_LIMIT_INFORMATION`,
  `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION`,
  `JOBOBJECT_EXTENDED_LIMIT_INFORMATION`, and `TerminateJobObject`.

No source code, supervisor, test, synthetic worker, fixture, dataset, or
evidence artifact was created or run for this contract. No Job Object API
was invoked. All future behavior in this document remains proposed until
independently qualified.
