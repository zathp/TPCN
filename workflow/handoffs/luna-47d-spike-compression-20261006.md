---
tpcn_handoff:
  agent: "Luna-47D implementation worker; independent Luna-0 review pending"
  luna_identifier: "Luna-47D"
  descriptive_name: "Spike compression and bounded threshold oscillator"
  task_id: "luna-47d-spike-compression-20261006"
  component: "Independent synthetic output model"
  status: "complete - SUPPORTED in frozen synthetic regimes; independent review pending; regressions remain failed"
  contract_version: "1.2"
  branch: "copilot/luna47d-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  production_evidence_revision: "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
  protocol_code_revision: "6ece0de652270bd3aef1c0a04e487773e81154f7"
  assertion_correction_revision: "9c75e547a67239027d6f8ec8b7f26bc1eae3188e"
  canonical_source_revision: "ee522bf6c4882bb09b9bc0af2520e50c3d1a3589"
  result_revision: "Containing evidence/handoff publication commit; exact SHA returned after push"
  dependencies: ["Published Luna-0 authorization", "Luna-46 reviewed MIXED context only; no retained trace is a model input"]
  owner: "Project owner"
  classification: ["experimental output model", "synthetic mechanism only", "SUPPORTED within declared regimes", "not production-ready"]
  hypothesis: "A dissipative charge-drain output mapping compresses short moderate clusters and produces finite extreme bursts with bounded recovery."
  counter_hypothesis: "Count, timing, state bound, symmetry or recovery fails under the frozen fixtures."
  interfaces_relied_on: ["experiments/luna47d/PROTOCOL.md", "experiments/luna47d/fixtures.json", "Standalone standard-library model and replay writer"]
  label_information_boundary: ["No labels, network or global training data enter the model.", "Expected counts are downstream acceptance truth, not inputs to the dynamics."]
  timing_assumptions: ["Exact rational logical event times; input-before-due ties; no global tick.", "Recovery crossing is a binary64 analytic metric, not an event timestamp."]
  reset_boundaries: ["Charge, pending opportunity and contributors reset per synthetic trajectory."]
  resource_bounds: ["16 inputs; absolute drive/state <=32; one pending opportunity; 128-opportunity watchdog.", "Primary output <=32; observed maximum 7.", "Primary neutral recovery bound <138.249972; observation tail 144."]
  authorized_scope: ["Owned isolated model, tests, synthetic artifacts and this handoff only."]
  unauthorized_scope: ["No A/B/C dependency, production/topology/governance edits, upstream reachability, efficacy, ACP, promotion, merge, successor or delegation."]
  controls: ["Pre-outcome protocol/code commit", "Polarity mirroring", "Weak-drain negative", "Invalid-domain and record-fault controls", "Exact identities, source hashes and fresh-process replay"]
  measurements: ["30 trajectories; 44 primary inputs; 40 exact primary output events.", "Count/latency/spacing, full state boundaries, neutral recovery, configuration and hashes."]
  information_boundary_check: ["Standalone standard-library model; no feedback into TPCN, no cross-lane dependency."]
  hardware_mapping: ["Not tested; dimensionless software model only. Hardware equivalence, analog oscillator realizability and calibrated energy are not established."]
  architecture_invariants_touched: ["A01/A02 event-triggered analytic local evolution", "A03 strict-future output opportunities; no inter-node route claim", "A08 dissipative bounded state/event budget", "A15 no portability/equivalence claim; no clause change"]
  preserves: ["Luna-46 MIXED", "A01-A15", "ACP-0007/ACP-0008", "Production/evidence baseline unchanged"]
  architecture_change: false
  proposal: null
  files_changed: ["experiments/luna47d/PROTOCOL.md", "experiments/luna47d/fixtures.json", "experiments/luna47d/model.py", "experiments/luna47d/run.py", "tests/test_luna47d_output_model.py", "artifacts/luna47d/", "workflow/handoffs/luna-47d-spike-compression-20261006.md"]
  tests_added: ["98 focused cases: frozen regimes, analytic recurrence/burst, exact identities, negative boundaries, failure gates, causal ties/reset, symmetry and replay"]
  tests_passing: ["Final focused 98 passed", "Applicable regressions 374 passed (one failure retained)", "Full suite 1422 passed (two failures, seven errors and one skip retained)", "Fresh-process canonical replay and compileall PASS", "Whitespace check PASS excluding raw pytest XML traceback text"]
  tests_failed: ["Initial focused 97 passed / 1 failed: weak-drain assertion expected two instead of three; corrected test only.", "Applicable: Luna-46 catalog checkout-byte hash check.", "Full: Luna-44 pinned-source materialization one failure / seven setup errors, plus Luna-46 catalog hash one failure."]
  tests_not_run: ["Independent Luna-0 review", "CUDA execution (unavailable; one skip)", "Production integration, network reachability, efficacy, learning, hardware or architecture promotion"]
  assumptions: ["Synthetic accumulator increments are exogenous, not claims about reachable network excitation.", "The moderate regime is a declared short cluster; arbitrary arrival trains are not compressed to one."]
  unresolved: ["Independent Luna-0 review required.", "Repository regression suite remains failed; no production fix or assertion relaxation authorized.", "Cross-platform binary64 byte replay and physical implementation are unverified.", "Output-path guard cannot rule out concurrent filesystem alias replacement after validation."]
  recommended_next_agent: ["Independent Luna-0 review of pushed evidence and corrections only; no successor authorization"]
---

# Luna-47D completed handoff

## Outcome and owned scope

**OBSERVED: SUPPORTED** under the predeclared synthetic-regime criteria.
All 30 primary trajectories (15 families, positive and negative) pass their
declared count, timing, state/output bounds, recovery, symmetry and exact-replay
checks. Forty output events reconcile to 44 admitted input identities; no
input/output identities or timestamps are dropped. All 13 negative controls
are detected, including an alternate configuration that genuinely fails
ordinary compression. This is a model-specific result, not independent review.

Only owned files changed. The starting worktree was clean on the requested
branch at `789dda5`; its diff from `2cef8ea` was documentation-only.
No production/runtime/topology/fixture/governance file was edited.
No A/B/C code or result was consumed, and no delegation occurred.

## Tested oscillator/return rule and predeclaration

**HYPOTHESIZED before execution:** a leaky signed reservoir with threshold 1,
drain quantum 4, decay rate 0.125 and local opportunity period 1/2 could
compress moderate clusters, permit finite extreme bursts and recover.
The protocol, frozen fixture, code, tests and planned handoff were committed
at `6ece0de` before any outcome artifact.

At an opportunity, emit signed unit output only if the remaining absolute
charge is at least 1, subtract up to 4 without sign reversal, and schedule
another opportunity only if residual charge remains suprathreshold.
Between boundaries, use analytic exponential decay. There is no autonomous
pump, global timestep, artificial post-horizon reset or silent truncation.
The exact rule/domain/why these bounds are appropriate appears in
`experiments/luna47d/PROTOCOL.md`.

**INFERRED from the rule, checked by tests:** finite total absolute drive <=32
bounds state by 32. Each primary output consumes at least one unit, so count
<=32 independently of runtime guards. Leakage alone bounds epsilon recovery
by `log(32/1e-6)/0.125 = 138.24997168611202 < 144` after final excitation.
The 4-unit drain exceeds the moderate cluster's <=3.75-unit total drive;
this is a selected finite mechanism, not a claim about a universal oscillator.

## Counts, timing, recovery and bounds

Each row below applies identically to both polarities. Time units are synthetic
logical units. Recovery delay is measured from the **last input** to permanent
`abs(q)<=1e-6`; latency is measured from the **first input**.

| Family | Outputs per polarity | Exact output times | Recovery delay | Max absolute state |
|---|---:|---|---:|---:|
| idle | 0 | none | 0 | 0 |
| subthreshold | 0 | none | 104.978907 | 0.5 |
| subthreshold-near | 0 | none | 110.516080 | 0.999 |
| subthreshold-cluster | 0 | none | 109.556851 | 0.886119 |
| threshold-boundary | 0 | none | 110.524084 | 1 |
| marginal-crossing | 0 | none | 110.603687 | 1.01 |
| moderate-low | 1 | 1/2 | 0.5 | 1.25 |
| moderate-high | 1 | 1/2 | 0.5 | 2.5 |
| moderate-cluster | 1 | 1/2 | 0.25 | 3.692162 |
| extreme-low | 2 | 1/2, 1 | 1 | 8 |
| extreme | 3 | 1/2, 1, 3/2 | 1.5 | 12 |
| extreme-cap | 7 | 1/2, 1, 3/2, 2, 5/2, 3, 7/2 | 3.5 | 32 |
| extreme-cluster | 3 | 1/2, 1, 3/2 | 1.25 | 11.814919 |
| cancellation | 0 | none | 0 | 2.5 |
| separated-moderate | 2 | 1/2, 5/2 | 0.5 | 1.25 |

All emitting streams have exact first latency 1/2. Extreme spacing is exactly
1/2; separated moderate spacing is 2. No-output latency/spacing is
null/empty, not zero. Every emitted positive event has a matching negative
event with identical time and opposite sign; all scalar magnitude metrics
match. The maximum observed primary recovery delay is 110.60368711053954,
below the bound. Maximum final nonzero residual is
1.5382279542159754e-8, below epsilon. All emitting primary streams reach
exact zero after their final output. No opportunities remain pending at
the horizon, no output occurs after permanent neutral recovery, and the
largest observed opportunity/output count is 7, below both guards.

Every moderate-cluster input (`i0`, `i1`, `i2`) is retained at its exact
0, 1/8, 1/4 time and maps to the single output at 1/2. Non-emissions retain
explicit opportunity records and below-threshold decisions where applicable.
Continuous trajectories reconstruct from pre/post states and the analytic
between-event equation; no arbitrary sampling grid is used.

## Preserved negatives and corrections

**OBSERVED negative boundaries:** threshold=1 and marginal=1.01 inputs cross
the input-time threshold but decay below it before the opportunity, producing
no output. Subthreshold residuals recover by leakage, not an artificial reset.
Two separated ordinary inputs produce two outputs, outside the compressed
short-cluster regime.

The fixed weak-drain control (quantum=1) produces **three**, not one, outputs
for each moderate-cluster polarity at 1/2, 1 and 3/2; residual recovery delay
is 103.05282640591254. It genuinely fails the primary compression criterion.
Zero leak, zero period, zero drain, too-short tail, oversized drive and
nonfinite drive are rejected explicitly. Synthetic record faults representing
self-sustaining output, missing output, state overflow, output-budget overflow
and failed neutral recovery fail their gates and exact identity replay.
These corrupt records are clearly labeled **not model observations**.
Tests bypass parameter admission for deliberate nondissipative mutants and
confirm hard output-budget/watchdog exceptions rather than truncated success.

The first focused run failed one test assertion (97 passed): the weak-drain
test incorrectly expected two events. Runtime inspection and the recurrence
showed three. Commit `9c75e54` corrects **only the test count assertion**.
The frozen one-output criterion, protocol, fixture and parameters did not change.

Post-generation inspection then found an idle-only metric bug: the absence
of an initial trace row caused recovery to be reported at observation time
144 instead of zero. Commit `ee522bf` corrects that metric and adds idle
assertions; it preserves the complete old artifact as
`initial-pre-idle-correction.json`. A full primary-record comparison confirms
only idle/positive and idle/negative recovery time/delay changed. Every
non-idle primary record is identical. Counts, dynamics, parameters, fixtures
and verdict criteria were not tuned after outcomes.

## Architecture and information-boundary evidence

* **A01/A02:** standalone event-triggered local evolution; analytic elapsed-time
  decay, exact ties, no idle tick loop, explicit per-trajectory reset.
* **A03:** positive rational opportunity delay; prefix causality test; this is
  NOT an inter-node propagation or network reachability demonstration.
* **A08:** finite input/drive/state/contributor/pending/output bounds, dissipative
  drain/leak and raising guards. No self-sustaining output in the primary fixtures.
* **A15:** no production portability requirement is altered; arbitrary logical
  units, binary64 arithmetic and exact rationals are software evidence only.

No clause is amended, no ACP is created and no architecture departure is
promoted. The model omits full TPCN learning, prediction and reward behavior
because it is an isolated output mapping, not a replacement neuron.
Luna-46's reviewed **MIXED** verdict is preserved. Its data is not fed into
this mechanism. Accuracy, prediction loss, energy/joules, reward, utility,
connectivity utilization and training splits are **not applicable/not measured**.

## Validation record

All terminal commands used explicit `Set-Location` to the specified worktree
and the configured `.venv/Scripts/python.exe` (Python 3.11.5 on Windows).
Full commands and machine-readable counts are in `artifacts/luna47d/validation.json`.

| Procedure | Revision | Observed result | Retained evidence |
|---|---|---|---|
| Initial focused pytest | 6ece0de | 97 passed, 1 assertion failure | Correction commit and validation.json |
| Corrected focused pytest | 9c75e54 | 98 passed | validation.json |
| Final focused pytest | ee522bf | 98 passed | focused-tests.xml |
| Applicable event/neuron/E2/topology/Luna-38/Luna-46 regressions | 9c75e54 | 374 passed, 1 failed; exit 1 | applicable-tests.xml |
| Full pytest | ee522bf | 1422 passed, 2 failed, 7 errors, 1 skipped; exit 1 | full-tests.xml |
| compileall on owned code/tests | ee522bf | PASS | validation.json |
| Fresh-process `run --verify` | ee522bf and publication checkout | PASS, all identities/states/metrics/controls match | evidence.json / validation.json |
| Whitespace check excluding raw pytest XML reports | owned changes | PASS | validation.json |
| Raw staged whitespace check | publication staging | FAIL on original pytest traceback whitespace; raw report retained | validation.json / full-tests.xml |

The editor could not discover worktree tests/Pylance user files. Its problems
tool reported no errors, but that is not claimed as complete static analysis.
Configured-interpreter compileall, runtime inspections and pytest provide the
execution evidence.

The raw staged whitespace check also detects trailing spaces in the captured
pytest traceback/source text in `full-tests.xml`. That generated report is
preserved without text normalization. The scoped whitespace check excludes
only pytest XML reports; code, protocol, handoff and JSON evidence pass.
This reporting exception does not waive any scientific or regression failure.

**Regression failures remain failures.** Luna-44 pinned-source materialization
has one test failure and seven setup errors, consistent with the documented
Windows pinned-source issue; this lane did not independently extract subprocess
stderr to prove its exact cause. Luna-46's integrity-only test fails the raw
Luna-45 catalog hash. A read-only diagnosis verified:

* Expected/pinned Git-blob SHA-256:
  `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`.
* CRLF checkout SHA-256:
  `5c41184dc9b9b5872263bcbbc1e5fc406789101c27942480b9cfb6b33c87da80`.
* LF-normalized checkout bytes equal the authorization Git blob exactly and
  hash to the expected value; `core.autocrlf=true`.

No retained file was rewritten, configuration changed, assertion relaxed or
failed gate waived. CUDA is unavailable. These failures prevent a clean
repository regression claim, but do not enter the independent synthetic
model's acceptance predicate. This lane does not assert integration readiness.

## Evidence identities and reproduction

Canonical artifact: `artifacts/luna47d/evidence.json`.
Source revision: `ee522bf6c4882bb09b9bc0af2520e50c3d1a3589`.
Canonical LF file SHA-256:
`c595a16fa3decad5090755e434fdc556478675c72f431c500b2622581dcc5f46`.
Internal integrity SHA-256:
`3fc0f575952cf085a7cf5c6d22c3a32a12d7387fc92649efc5e666ba02f94daf`.
Initial/replay record SHA-256 (both):
`f66fa63245cae4e689bc475550802dc913e34c3aac2eeae3c11169f1ffc28e47`.

The artifact includes its complete configurations, per-trajectory fixture
hashes, source Git blobs and normalized-LF SHA-256 hashes, exact input/output
IDs/times, full state boundaries, identity-level mapping, bounds, tolerances,
interpreter/platform, initial/replay records and all negative controls.
No seed is used. Replay comparisons and identities/timestamps are exact;
equation checks use predeclared abs/rel 1e-12; threshold tolerance is zero.

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47d'
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m experiments.luna47d.run --verify
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m pytest -q tests/test_luna47d_output_model.py
```

For new generation use a fresh clean checkout of the recorded source revision,
with no `artifacts/luna47d/evidence.json`, and `run --generate`. The generator
refuses dirty state and uses exclusive creation at the fixed owned path.
Do not overwrite retained evidence. Git may convert checkout newlines;
internal JSON integrity and code SHA-256 use declared canonical LF semantics.

## Limitations, rollback and next authorized action

**NOT ESTABLISHED:** upstream reachability, useful neural computation, task
efficacy, physical oscillator/FPAA/FPGA equivalence, energy advantage,
cross-platform byte replay or production suitability. "Compressed" means
three known short-cluster identities produce one known event under this
fixed drain; it is not a universal temporal encoder or information-retention
claim. Future external drive or different parameters can change counts.
Contributors are participation identities, not causal weight attribution.
Finite-budget proof applies only to the declared input/configuration domain.
Filesystem alias races after path validation are not excluded.

Rollback/restoration point is the authorization revision; no production
changes need reversal. Preserve the isolated branch and negative evidence.
The evidence/handoff publication is to be pushed to
`origin/copilot/luna47d-investigation`, with clean status and ref parity checked
and returned in the final report. The implementation worker then stops.
**Independent Luna-0 review only** is next: review the protocol ordering,
corrections, exact replay, boundedness, negative evidence and failed regressions.
No merge, production integration, architecture promotion, successor or Luna-48
is authorized by this result.
