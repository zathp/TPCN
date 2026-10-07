---
tpcn_handoff:
  agent: "Luna-47B"
  luna_identifier: "Luna-47B"
  descriptive_name: "Drive / accumulation-gain adequacy"
  task_id: "luna-47b-drive-accumulation-gain-20261006"
  component: "Downstream retained-trace first-threshold diagnostic"
  status: "complete; SUPPORTED within the mathematical mechanism scope; independent review pending"
  contract_version: "1.2"
  branch: "copilot/luna47b-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  result_revision: "38891b8 (exact full execution revision in results.json); outcome/handoff publication follows this revision"
  dependencies:
    - "Reviewed Luna46 MIXED corrected output and its 33 pinned retained sources"
    - "Production/evidence baseline 2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
  owner: "Project owner"
  classification: ["OFFLINE EXPERIMENTAL MECHANISM", "VERIFICATION", "NO EFFICACY"]
  hypothesis: "Deposition gain alone can cross the retained threshold in DRIVE-LIMITED streams."
  counter_hypothesis: "No finite legal tested gain rescues the signed streams at fixed decay/threshold."
  interfaces_relied_on:
    - "Reviewed Luna46 read-only integrity, raw reconciliation, and recurrence verification"
    - "Committed Luna44/45 raw captures, trajectories, config and provenance"
  label_information_boundary:
    - "Categories are preserved offline evaluation annotations, not inputs."
    - "No neural computation, learning or routing receives analysis statistics."
  timing_assumptions: ["Exact retained event and prior-clock order; lambda=0.0125, tau=80; no global tick."]
  reset_boundaries: ["A=0 at each character; no cross-character state."]
  resource_bounds: ["320 sequences, at most 512 updates per sequence, seven global arms, gain<=1e6, |A|<=4 before stop."]
  authorized_scope: ["Gain-only first integration-threshold analysis and replay in owned paths."]
  unauthorized_scope: ["Production changes", "decay/threshold/input/routing/topology tuning", "efficacy", "hardware claim", "ACP", "promotion", "successor"]
  controls:
    - "Protocol/code committed before outcome artifact."
    - "All critical gains derived before choosing deterministic 0.99/1.01 brackets."
    - "Baseline signed recurrence, threshold and z_max remain unchanged."
    - "Stop at first integration threshold; do not invent post-trigger network dynamics."
  measurements: ["Critical gains", "rescues", "non-target crossings", "saturation", "finite bounds", "signed cancellation", "exact replay and hashes"]
  information_boundary_check: ["No production execution or core modifications; all statistics downstream."]
  hardware_mapping: ["Dimensional resistor/current scaling assumptions only; no measured circuit data."]
  architecture_invariants_touched: ["A01", "A02", "A03", "A06", "A07", "A08", "A15"]
  preserves: ["Luna46 MIXED and exact categories", "signed input identities", "ACP0007/0008", "production baseline", "A01-A15"]
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna47b/__init__.py"
    - "experiments/luna47b/diagnostic.py"
    - "experiments/luna47b/PROTOCOL.md"
    - "experiments/luna47b/README.md"
    - "tests/test_luna47b_gain.py"
    - "artifacts/luna47b/results.json"
    - "artifacts/luna47b/validation.json"
    - "workflow/handoffs/luna-47b-drive-accumulation-gain-20261006.md"
  tests_added: ["tests/test_luna47b_gain.py"]
  tests_passing: ["16 focused tests", "356 applicable regression tests", "initial internal replay", "33-source immutable-byte integrity", "both raw phase reconstructions"]
  tests_failed:
    - "Applicable regression suite: 2 failed, 7 errors; unchanged Windows checkout/materialization failures, not suppressed."
  tests_not_run: ["Full suite", "hardware", "efficacy", "counterfactual production dynamics"]
  assumptions: ["First integration-threshold sufficiency is not canonical emission or utility.", "Immutable committed blobs are authoritative despite Git CRLF checkout."]
  unresolved: ["Physical realizability and post-threshold network behavior unmeasured.", "Independent Luna0 review pending.", "Regression suite remains failed."]
  recommended_next_agent: ["Luna-0 independent review only; stop after pushed handoff."]
---

## Outcome and owned scope

**OBSERVED verdict: SUPPORTED**, limited to the predeclared mathematical
first integration-threshold question. All 75 DRIVE-LIMITED streams cross
at a legal tested gain with the retained signed input, decay, timestamps,
threshold, reset, topology and routing unchanged. Insufficient deposited
excitation is independently sufficient to account for their non-crossing
in this retained-prefix setup. This is not proof it is the exclusive cause,
that all neurons would emit, or that gains improve a task.

Luna46 remains **MIXED**: 212 NO-RECEPTIONS, 33
TEMPORAL-RETENTION-LIMITED, 75 DRIVE-LIMITED, zero
CANCELLATION-LIMITED and zero ALREADY-CROSSING. Exact 320 stream identities
and all 235 receptions are retained. No shared source, fixture, runtime,
topology, governance, ACP or other-lane file is changed. No other lane's
implementation or results were consumed.

Predeclaration commits:

1. `4b159423e6faf2990fda07976ffebe3674bf2dea`: protocol, implementation, tests;
2. `aa878c3`: code-text materialization gate clarification;
3. `38891b8`: immutable committed-evidence reader, before any outcome artifact.

The first two execution attempts stopped at byte-provenance gates before
outcomes. Windows checkout changed LF to CRLF. No retained file was repaired,
rewritten or tolerance-relaxed. The final reader verifies immutable committed
bytes from the declared evidence baseline, pinned hashes and current blob
identity; checkout mismatches must be *exact* LF-to-CRLF materialization.
Of 34 recorded evidence identities (33-source inventory plus corrected
output), 25 have checkout-only CRLF differences, nine are byte-identical.
Both hashes are retained. No numerical evidence normalization occurs.

## Critical gains and rescues

**INFERRED analytically:** before the first trigger, signed linearity gives
`A_i(g)=g*B_i` with the original `rho_i=exp(-0.0125*dt_i)`, so
`g_critical=1/max_i(abs(B_i))`. Mixed signs cannot invalidate this gain
homogeneity, although they can reduce the unit-gain response.

All 108 reception-bearing sequences have finite critical gains. The 212
NO-RECEPTIONS sequences have zero response and explicit NO-CROSSING results:
no finite gain can manufacture a reception. Across the 108 applicable
streams, min/median/max critical gain is
**1.207080732114708 / 2.553678150694072 / 3.28743886088831**.
For the target 75, min/median/max is
**1.8425872009402644 / 2.8548209160858264 / 3.28743886088831**.
Each individual critical gain and its full unit-gain trajectory is in
`results.json`, with local 0.99/1.01 brackets independently evaluated:
all 108 lower brackets do not cross and all 108 upper brackets cross.
Critical values are binary64 approximations; exact equality is not rounded
into a crossing.

| Tested global gain | Target rescued /75 | Fraction | Other crossings |
|---:|---:|---:|---:|
| 1 | 0 | 0% | 0 |
| 1.1950099247935608 | 0 | 0% | 0 |
| 1.219151539435855 | 0 | 0% | 1 |
| 2.5281413691871313 | 18 | 24% | 33 |
| 2.5792149322010127 | 23 | 30.6667% | 33 |
| 3.254564472279427 | 72 | 96% | 33 |
| 3.3203132494971928 | 75 | 100% | 33 |

Other crossings are **unintended relative to this target**, not erroneous
labels: at the four largest arms they include all 33 retention-limited
streams (100% of the other reception-bearing population; 33/245 =
13.4694% of all non-target sequences). No no-reception stream crosses.
Gain is not category-selective. Threshold crossing alone establishes
neither correct classification nor useful prediction.

## Saturation, signs, finite behavior

**OBSERVED:** signed inputs include 121 positive and 114 negative
receptions, zero zero-valued receptions. The original streams and their
signs were not relabeled. Evaluated prefixes have zero opposing-sign
cancellation and zero sign reversals; their first-boundary cancellation
and sign metrics are retained per event/arm, rather than using sum(abs(E))
as a state substitute. Synthetic tests additionally exercise cancellation,
reversal, decay, equal-time order, exact thresholds and no-response cases.

None of the seven retained global arms saturates z_max=4; their largest
evaluated absolute state is **1.6260639331807014** (at gain
2.5792149322010127). At the all-rescued arm, the largest evaluated absolute
state is **1.2962629607423466**. Larger gain can lower this reported maximum
because evaluation stops earlier at the first crossing, not because of a
claimed stabilizing mechanism. A synthetic gain=1e6 case demonstrates
unchanged clipping at -4 and finite bounded prefix evaluation.

There are no nonfinite inputs/deposits/states in the retained arms.
No instability was observed in these finite prefixes; no long-run stability
claim is made. Post-threshold discharge/admission and future network events
are not simulated. Full original per-event states and inputs remain in the
artifact; gain states after the first crossing are explicitly censored,
never fabricated as production trajectories. This diagnostic cannot answer
post-trigger computation, recurrence or useful-emission questions.

## Hardware interpretation

**HYPOTHESIZED, not measured:** for an isolated charge/current injection
stage, `Delta V=Q/C` or integrated `I/C` can represent deposition gain.
The target's approximately 1.84–3.29 critical ratios, with a 3.32 tested
upper bracket, are modest dimensionless factors compatible in principle
with an ordinary resistor-ratio/transconductance/current-scaling stage.
For ideal voltage-to-current injection at fixed C, an injection resistance
could be reduced by that ratio, *if* its loading does not change the
independent leak time constant. Bipolar drive must preserve both signs.

Changing C alone is **not** an equivalent authorized operation: it changes
the leak RC/time constant as well as deposition. A separate injection stage
and fixed C/leak are assumptions, not demonstrated circuit properties.
No supply/headroom, op-amp bandwidth, noise, component tolerances,
qualification isolation, energy, capacitor scaling or physical calibration
was measured. There is no hardware build, equivalence or realizability
claim. A mathematical critical gain is not a hardware recommendation.

## Architecture evidence

| Clause | Evidence / unchanged boundary |
|---|---|
| A01-A03 | Original event/prior clocks, deterministic queue order and finite-delay raw route reconciliation; no global timestep or new route. |
| A06-A07 | Prediction/error/learning untouched; all calculations downstream, labels/categories never become neural inputs. |
| A08 | Gain bound 1e6, finite budgets, unchanged +/-4 clipping, explicit first-trigger stop; no invented post-trigger dynamics. |
| A15 | Hardware-neutral signed equation; dimensional mapping expressly unmeasured. |

No clause amendment, production departure or ACP is proposed. This isolated
gain diagnostic is an experimental model, not a replacement neuron.
ACP0007/0008 and earlier reviewed dispositions remain unchanged.

## Validation record

All terminal commands explicitly selected the isolated worktree. Python
3.11.5 was the configured interpreter. Exact commands, counts, failed test
identities, provenance gates and output SHA-256 are in `validation.json`.

| Procedure | Observed result |
|---|---|
| Precommit py_compile | PASS |
| 33 pinned source inventory, config/fixture hashes, phase checks | PASS from immutable committed bytes |
| Both retained raw phases -> exact reviewed Luna46 sequence objects | PASS |
| Two complete gain analyses, same canonical bytes/digest | PASS |
| Focused tests | **16 passed**, no failures/errors/skips, 186.01s |
| Eight applicable regression files | **356 passed, 2 failed, 7 errors**, 103.47s; suite failed, not waived |
| Published-artifact clean-tree replay | Pending outcome commit; recorded after execution below |

The Luna46 regression failure is `test_real_retained_artifacts_integrity_only`:
its unchanged reader hashes the CRLF worktree catalog and fails the published
Luna45 catalog hash check. The other failure and seven setup errors arise
from the unchanged Luna44 temporary pinned-source materialization/hash
problem previously documented in Luna46. These failures are disclosed and
not fixed by changing shared tests, hashes, fixtures or runtime. Passing
this lane's committed-blob gates does not turn that regression suite green.
Pylance/editor test tools could not discover the isolated worktree files;
terminal syntax/tests were the explicit fallback.

## Benchmark/resource applicability and limitations

Dataset/task accuracy, train/test splits, prediction loss, energy/utility,
learning efficacy, latency improvement and connectivity utilization are
**not applicable**: this is retained-prefix offline analysis, not a task
run. Retained fixture/input/reset identity and both replay phases are pinned.
Logical time units are inherited unchanged; no physical seconds conversion.
Five bounded retained causal-root truncation metadata cases remain as in
Luna46; raw capture coverage is complete, ancestry expansion is not claimed.

The common scalar gain rescues non-target streams, does not produce inputs
where no route reception exists, and says nothing about beneficial
post-trigger computation. An all-rescued first-boundary result does not
establish exclusive causation, selective response, physical realizability,
noise robustness or task utility. Independent review remains required.
Full repository tests were not run; applicable regression failures remain.

## Reproduction, rollback and next assignment

Use `experiments/luna47b/README.md` and the committed protocol. On a clean
published lane, run `python -m experiments.luna47b.diagnostic --replay`;
it reuses the recorded execution revision and requires exact artifact bytes.
The initial result has SHA-256
`b120d2cc5718649fb0d57d93611ddb89b45113e79c0d3003cf330fe092d0fb83`.
Exact environment/source materialization is recorded; independent
mathematical replay is also available through focused tests.

Rollback affects only this lane's listed files; common authorization
`789dda5988daf72f375d9713bd76a6da2b9e8b34` is the safe restoration point.
No merge or production integration is ready or authorized.
**Next: independent Luna-0 review of the pushed handoff/artifacts only.**
No successor, promotion, further sweep or Luna48 is authorized.
