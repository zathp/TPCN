---
tpcn_handoff:
  agent: "Luna-47G"
  luna_identifier: "Luna-47G"
  descriptive_name: "Analog component tolerance and mismatch robustness"
  task_id: "luna-47g-analog-robustness-20261006"
  component: "Independent synthetic simulation stand-in"
  status: "complete - PARTIALLY SUPPORTED; independent Luna-0 review pending"
  contract_version: "1.2"
  branch: "copilot/luna47g-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  result_revision: "Artifact/handoff publication is this containing commit; exact hash returned in final report"
  protocol_execution_revision: "8406de77e7328908e70525982336b74edc234124"
  packaging_revision: "Exact revision recorded in artifacts/luna47g/package-manifest.json"
  dependencies: ["Reviewed component specifications unavailable; unreviewed Luna-47E excluded"]
  owner: "Project owner"
  classification: ["simulation only", "not hardware feasibility", "not efficacy"]
  hypothesis: "The independent stand-in preserves the six regimes under the predeclared tolerance bands."
  counter_hypothesis: "Tolerance draws break one or more regimes, sign behavior, bounds, or finite neutral return."
  interfaces_relied_on: ["experiments/luna47g/config.json", "experiments/luna47g/fixtures.json"]
  label_information_boundary: ["No labels, dataset, production computation, or other lane mechanism inputs"]
  timing_assumptions: ["Dimensionless local event time, analytic elapsed-time decay, positive local return delay 0.1"]
  reset_boundaries: ["Independent zero-state reset per signed fixture"]
  resource_bounds: ["State 8, output 1, 128 inputs, 192 events, 16 outputs per fixture"]
  authorized_scope: ["Simulation and evidence within exclusively owned lane paths"]
  unauthorized_scope: ["No production/topology/governance edits, ACP, efficacy, hardware claim, composition, or successor"]
  controls: ["Nominal, matched signs, offset-reversed and zero-offset mirrors, temporal spacing, fixed corner interactions"]
  measurements: ["3840 sampled rows plus 168 controlled corners; per-band failures 0, 1, 81, 418, 631 of 768"]
  information_boundary_check: ["Standalone Python standard library; no TPCN imports or result feedback"]
  hardware_mapping: ["Assumed dimensionless multipliers only; missing reviewed part specifications"]
  architecture_invariants_touched: ["A01-A03 event semantics", "A04 no topology", "A08 finite bounds", "A09 local count proxies", "A15 no feasibility claim"]
  preserves: ["All production files and baseline evidence; Luna-46 MIXED; ACP status unchanged"]
  architecture_change: false
  proposal: null
  files_changed: ["experiments/luna47g/", "artifacts/luna47g/", "tests/test_luna47g_robustness.py", "tests/test_luna47g_packaging.py", "workflow/handoffs/luna-47g-analog-robustness-20261006.md"]
  tests_added: ["Standalone event-time, signed, boundedness, validation, retained-row and provenance/corner tests"]
  tests_passing: ["27 final focused tests", "139 event/excursion/slow-state regressions", "Additional combined run: 206 passed, includes 24 focused tests", "Fresh-process exact model and packaging replay"]
  tests_failed: ["One additional regression: Luna-46 retained Luna-45 catalog raw hash mismatch from CRLF; not waived"]
  tests_not_run: ["Full repository suite", "Physical hardware, efficacy, cross-platform replay", "Independent Luna-0 review"]
  assumptions: ["Uniform bounded static variation and event-sampled bounded noise, not real fabrication distributions"]
  unresolved: ["Reviewed component specifications absent", "Broad-band qualitative failures", "Baseline Windows raw catalog hash regression", "Independent Luna-0 review"]
  recommended_next_agent: ["Independent Luna-0 review after lane execution and publication; no delegation or successor"]
---

# Luna-47G analog tolerance/mismatch simulation

## Outcome and owned scope

**OBSERVED — PARTIALLY SUPPORTED**, solely for the independent synthetic
stand-in and its predeclared fixtures. The nominal and selected (.02) bands
meet the <=1% sampled-failure gate; .10/.25/.50 do not. No physical
hardware-feasibility, production robustness, efficacy, or architecture
promotion claim follows. This completed investigation stops for independent
Luna-0 review; no integration or successor is authorized.

The protocol, equations, bounds, signs, distributions, seeds, fixtures,
sample counts and acceptance rules were committed **before tests or outcomes**
in `8406de77e7328908e70525982336b74edc234124`. Scientific files and the
original tests were not changed afterwards. A second commit adds only
post-outcome provenance packaging, explanatory subfailure counts and package
tests; it does not alter draws, model, predeclared metrics, verdict or
outcomes. That distinction is explicit in the package source and manifest.
The containing publication commit retains all outcomes and this handoff.

Exact owned files:

- `experiments/luna47g/{PROTOCOL.md,config.json,fixtures.json,simulate.py,package_evidence.py}`
- `tests/test_luna47g_{robustness,packaging}.py`
- `artifacts/luna47g/{samples.jsonl.gz,corners.jsonl.gz,summary.json,manifest.json,sample-provenance.jsonl.gz,diagnostics.json,package-manifest.json,validation.json}`
- `artifacts/luna47g/.gitattributes` (lane-local exact-byte evidence preservation)
- `workflow/handoffs/luna-47g-analog-robustness-20261006.md`

No runtime, production neuron, topology, common fixture, shared workflow,
architecture, ACP, or another lane's files are edited. No unreviewed
Luna-47A/B/C/D model or Luna-47E files/results were read or composed. All
component variations are assumptions, not part specifications. The reviewed
Luna-46 **MIXED** result remains context only, unchanged.

## Model, controls and information boundary

**ASSUMED:** Dimensionless R/C/gain/threshold/leakage multipliers; comparator
offset O; bounded event-sampled additive noise N. Analytic local decay rate
L/(RC), gain-qualified input deposition Gx/C, fixed +/-8 saturation,
threshold T, tanh output, ideal .75T discharge and one-shot .1-time-unit
local returns are independently authored experimental equations. They do not
model a physical circuit or the canonical TPCN neuron.

Bands b=0/.02/.10/.25/.50; three seeds 470601/470602/470603, each 256
samples per band. R/C share a latent draw (theoretical correlation .5);
T is shared between admission and output comparators. Remaining multiplier,
offset and noise-amplitude draws are independent bounded uniforms. R/C
marginals are triangular. Bands reuse unit draws, so cross-band comparisons
are paired. Even nominal includes N=.08 bounded noise. All details and
numeric values are frozen in PROTOCOL.md/config.json.

Each sample includes positive/negative physical-polarity trials with matched
noise and unchanged offset, offset-reversed mathematical mirrors and
zero-offset mirrors. Nine fixture types include pure noise, single,
near/far meaningful pairs, moderate/extreme excitation, cancellation and
order reversal. Each fixture resets; local decay is evaluated only at input,
scheduled return or terminal observation, with explicit input-before-return
tie order. There is no global timestep, network routing, task label, future
signal input, training, prediction/error computation, reward or topology.
Offline sensitivity, criteria, fixture names and reports never feed any
production computation.

## Quantitative results and transitions

Failure fractions and Wilson 95% intervals quantify this finite synthetic
sampling procedure, **not hardware yield or population uncertainty**.
Each band has 768 samples. Gate counts overlap and must not be summed to
obtain total failures.

| Band | Assumed b | Failed | Fraction | Wilson 95%, percent |
|---|---:|---:|---:|---:|
| nominal | 0 | 0 | 0.000% | 0.000–0.498 |
| selected | .02 | 1 | 0.130% | 0.023–0.734 |
| general | .10 | 81 | 10.547% | 8.567–12.919 |
| loose | .25 | 418 | 54.427% | 50.891–57.919 |
| stress | .50 | 631 | 82.161% | 79.296–84.707 |

| Band | Noise rejection | Single admission regime | Near accumulation | Moderate compression | Extreme return | Neutral by 20 |
|---|---:|---:|---:|---:|---:|---:|
| nominal | 0 | 0 | 0 | 0 | 0 | 0 |
| selected | 0 | 0 | 1 | 0 | 0 | 0 |
| general | 0 | 0 | 47 | 14 | 28 | 0 |
| loose | 0 | 14 | 247 | 218 | 138 | 36 |
| stress | 54 | 201 | 441 | 488 | 272 | 172 |

**OBSERVED:** The isolated selected-band failure is
`selected:470602:195`: near peak 1.0053448041603774 is below
T=1.0111705409976681, so no near output occurs. Both physical signs fail.
Its transition is single PASS -> accumulation FAIL -> compression PASS.
It is retained, not deleted as an outlier.

General-band failures include 47 single-PASS -> accumulation-FAIL
transitions and 28 compression-PASS -> return-FAIL transitions. These 28
extreme cases still produce bounded multi-event output, but cumulative
output exceeds absolute deposited drive, violating the predeclared return
compression guard. This is an important limitation of the ideal discharge
stand-in, not a hidden runaway or hardware observation.

Loose-band single failures are early outputs (14); near-no-output cases
dominate accumulation failure. Moderate cases show both missing output and
multiple outputs/admission loss. Return compression fails in 138 cases;
36 samples miss the finite neutral deadline.
Stress includes 54 noise-rejection failures, sign-dependent qualification,
early single output or missing/weak admission, insufficient or prematurely
discharged near accumulation, missing/multiple moderate outputs,
39 extreme cases with fewer than two outputs and 233 with cumulative output
above deposition (272 total return failures), and 172 neutral failures.

Every row preserves failed gate names, adjacent regime transitions,
signed gate results, all parameter/noise draws, output times/kinds, raw and
clipped state, admission flags, discharge state, return scheduling, and
terminal state. `summary.json` retains all per-band/per-sign gate counts,
per-seed failure counts, transition counts and sensitivity rankings.
`diagnostics.json` supplies first witnesses and explanatory subfailure counts,
which may overlap. No aggregate average substitutes for failures.

### Sensitivities and controlled interactions

**OBSERVED:** Leading absolute high-minus-low quartile failure-risk contrasts
(percentage points; observational, not causal):

| Band | Leading parameters and signed contrast |
|---|---|
| general | G −25.52, C +20.83, R +10.42, L −6.77 |
| loose | G −39.06, C +32.81, L −19.27, R +18.23 |
| stress | G −25.52, T −23.44, R +17.19, L −14.58 |

Nominal has no parameter variance/failures, hence no meaningful sensitivity.
Selected has only one failure; its tied .52-point contrasts are not stable
rank evidence. R/C correlation and shared T confound observational contrasts.
Pearson correlations and full rankings are retained, without claiming
uncertainty intervals or monotone calibration from these descriptive values.

There are 42 controlled pair experiments, four corners each (168 rows);
111 corners fail one or more gates. These are deterministic coverage probes,
not IID frequency or yield estimates. Fixed seed 470699 supplies identical
noise units across corners. Other parameters stay nominal.
For loose C/G, (--),(-+),(+-),(++) failure indicators are (0,1,1,0),
so difference-in-differences is −2: opposing capacitance/gain corners break
accumulation/compression, while matched corners pass. Loose R/L has
(0,0,1,0), difference −1, exposing slow-retention interaction.
Other nonzero binary interactions: loose R/T, C/T, G/T; stress R/L, R/N,
C/T, G/T, L/N. All four corner states/gates and zero as well as nonzero
interaction results are retained. Binary saturation and the fixed background
can hide higher-order effects; no three-way exhaustive search was done.

**INFERRED, conditional on this stand-in:** Deposition/emission margins
G/(CT), admission margins relative to gain/noise/offset, and decay ratio
RC/L require joint selection/calibration rather than independent broad
tolerances. Tight selected-band assumptions limit observed failures but do
not establish a real part-selection requirement. The fixed .75T discharge
versus tanh output also merits model-level scrutiny because cumulative
return compression fails. No repair or additional calibration was performed.
Changing T can suppress unwanted output and simultaneously starve meaningful
excitation; the stress contrast is not a recommendation to increase T.

## Bounds, signs, return and architecture evidence

**OBSERVED:** All sampled mandatory bounds, offset-reversed mirrors and
zero-offset mirrors pass (0 failures in every band). These bounds partly
hold by construction and do not constitute hardware evidence.
Max state/output across samples: 8 and 0.9999997749296758; maximum processed
events per fixture 17 and maximum outputs 10, below 192/16 limits.
Stress has 19 positive fixture runs with clipping, explicitly recorded;
other bands have zero. No sampled budget exhaustion or invalid future
schedule was hidden.

Neutral at 20 is stricter than eventual tendency to neutral. Max absolute
terminal state increases from 1.586e-9 nominal to 1.814e-3 stress.
Positive leakage gives ideal analytic convergence toward zero, but the
finite neutral criterion fails under slow assumed retention; this is not
reported as a universal finite-settling success. Comparator offsets cause
physical admission/output-count asymmetry in 84 loose and 298 stress
samples, versus zero in nominal/selected/general. Appropriate mathematical
sign mirrors pass; equal-offset physical symmetry is **not** presumed.

| Clause | Evidence and limit |
|---|---|
| A01–A02 | Irregular event-time fixture processing, analytic idle decay with two updates for a single input, time-translation, order sensitivity and reset tests; no neural tick |
| A03 | Strict-future local returns and representability rejection tested; no inter-node routing/propagation claim |
| A04 | No topology constructed or mutated; finite input/event/output limits only, not network fan-in/fan-out evidence |
| A08 | Saturation, bounded outputs, explicit budget failure tests, finite return sequence and retained final-state checks |
| A09 | Local update/output counts retained as operation proxies; no joules, utility or physical-energy claim |
| A15 | Simulation-only assumptions and missing part dependency explicit; physical portability/realizability not demonstrated |

No A-clause changes or ACP are proposed. This stand-in is not a replacement
for canonical predictive coding, local learning or energy accounting.
Luna-46 MIXED, ACP-0007/0008 and all baseline evidence remain unchanged.

## Validation record

Executed with Python 3.11.5 from the configured existing `.venv` on Windows,
always explicitly in the isolated worktree. `validation.json` retains
commands/results; model and package manifests retain execution revisions
and source/file hashes.

| Procedure | Observed result |
|---|---|
| Initial focused tests, frozen commit | 23 passed, 1 pre-execution artifact check skipped |
| Event runtime, E1/E2 and ACP-0008 slow-state regressions | 139 passed |
| Frozen sampled/corner run, second in-memory replay | Completed, exact replay, PARTIALLY SUPPORTED |
| Fresh-process `simulate.py --verify` | All compressed payload bytes and source hashes equal |
| Focused + canonical-event/energy/Luna-46 combined tests | 206 passed, 1 failed; includes 24 focused tests |
| Final focused model + package tests | 27 passed, 0 failed, 0 skipped |
| Fresh-process package replay | Exact bytes/hashes/model-manifest linkage pass |
| Editor Problems on initial model/tests | No errors; Pylance syntax/editor test discovery could not see isolated files, terminal pytest used |
| Final package editor checks / compileall / git diff --check | No errors / passed / passed |
| Full repository suite / hardware / efficacy / independent review | Not run |

The failed regression is
`test_luna46_depth_scaling_diagnostic.py::test_real_retained_artifacts_integrity_only`,
reporting `published Luna45 catalog hash differs`. Its source/tests/catalog
have no diff from authorization baseline. The committed catalog hash and
LF-normalized worktree hash both equal pinned
`a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`.
Raw CRLF worktree hash is
`5c41184dc9b9b5872263bcbbc1e5fc406789101c27942480b9cfb6b33c87da80`;
bytes differ only by CRLF, and `core.autocrlf=true`.
This is observed baseline materialization incompatibility, not a waived pass.
No shared file was normalized or repaired, and no global Git setting changed.

## Provenance, resources and limitations

`manifest.json` records frozen model revision, actual raw SHA256 and Git-blob
SHA256 for source/protocol/config/fixtures/tests, canonical configuration and
fixture hashes, platform/Python and numeric tolerances. The compressed JSONL
rows are lossless. `sample-provenance.jsonl.gz` links **each of 4,008 rows**
to its canonical row hash, source revision/hashes, configuration/fixture
hashes and numeric/neutral tolerances. The package manifest separately
identifies post-outcome packaging. No scientific protocol amendment occurred.
The lane-local artifact `.gitattributes` disables newline conversion for
JSON/gzip evidence, preserving exact payload bytes in committed blobs and
future Windows checkouts without changing any shared Git configuration.
Raw execution-source hashes retain the original Windows CRLF materialization;
exact replay requires those bytes, not merely semantically equivalent source.

The sample/control local-event counts are 165120, 165120, 164230, 164410,
165995 by ascending band; output counts are 23040, 22930, 21375, 20918,
25849. These include mirror/control runs and are not task-resource efficacy.
Samples compress to about 12.3 MB and corners to .44 MB. There is no dataset,
train/test split, class accuracy, prediction metric, reward, utility,
connectivity utilization, routing latency or measured physical energy:
all are **not applicable**.

**ASSUMED / NOT ESTABLISHED:** Real component tolerances, leakage vs bias,
temperature/supply drift, parasitics, colored/continuous noise, jitter,
cross-talk, hysteresis, metastability, rail recovery, aging, fabrication
tails and higher-order correlations. Exact exponential/tanh/ideal discharge
do not imply physical feasibility. Sparse static event-noise fixtures do not
cover continuous noise-induced arrivals or biased integrator equilibrium.
The three seeds and Wilson intervals address sampling variability only,
not model error or real-device populations. Zero observed failures is not
zero risk. Cross-platform/Python/zlib byte parity is not certified.
Canonical path guards cannot prevent concurrent filesystem alias replacement
between checking and writing; no concurrent mutator is assumed.

## Reproduction, publication and rollback

From the exact isolated lane checkout, PowerShell:

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47g'
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' experiments/luna47g/simulate.py --verify
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' experiments/luna47g/package_evidence.py --verify
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m pytest tests/test_luna47g_robustness.py tests/test_luna47g_packaging.py -q
```

For first execution in a new isolated checkout with no retained lane
outputs, run without `--verify`; the writer refuses overwrites. Do not remove
published evidence to replay in place: use comparison mode. Preserve all
unrelated work. Safe pre-lane restoration point is authorization
`789dda5988daf72f375d9713bd76a6da2b9e8b34`; lane changes are isolated and
not merged. Publication commit hashes, clean worktree and exact
origin/local ref parity are returned after push in the final response.

## Next assignment

**Independent Luna-0 review only**, with protocol/source provenance,
complete failed rows, interactions, replay, regression failure and missing
component-spec dependency. No delegation, merge, production integration,
ACP, hardware demonstration, efficacy or Luna-48 is authorized. Integration
readiness is not claimed.
