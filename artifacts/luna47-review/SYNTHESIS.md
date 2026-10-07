# Luna-47 independent review — 2026-10-06

## Decision

**FOLLOW-UP REQUIRED — promising unresolved mechanisms.**

This closes the requested independent evidence review, **not** an integration,
architecture-change, hardware, or efficacy gate. No lane implementation was
merged/cherry-picked or composed. No production architecture changes.
**No successor is authorized: no Luna-48, successor contract, dispatch, ACP
creation/acceptance, purchase/build, or integrated experiment in this cycle.**
The project owner receives the unresolved questions; recommendations below
are not executable assignments.

Luna-46 remains **MIXED**. ACP-0007/0008 and all predecessor negative,
blocked, and superseded evidence remain unchanged.

## Review identity and independence

Governance worktree: `luna47-review`, branch
`copilot/luna47-independent-review`, review baseline
`4b11e0e828fd6fbcb4cbf9b994f121bde54e4c37`.
Source/evidence baseline: `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
Common lane authorization: `789dda5988daf72f375d9713bd76a6da2b9e8b34`.

The reviewer read the actual `workflow/` authoritative documents, all seven
committed agent contracts, protocols, changed implementations/tests, retained
artifacts and handoffs, and Git declaration/correction history. No review was
delegated and no worker code was repaired. All lane inspections and executions
were read-only with respect to tracked files; test/verification caches were
ignored. Live lane refs were independently checked against the seven pins.

The reviewer-owned `independent_oracle.py` imports **no worker or production
module**. It uses pinned Git objects, independent equation/priority-queue
loops, JSON pointers and deterministic draw reconstruction. Its PASS records
6,245,017 comparison checks; this is a program check count, not independent
trials or a scientific confidence estimate. Equation residuals were zero in
this interpreter for the checked boundaries. `verify_manifests.py` separately
checks the 33 retained input identities, file lengths/SHA-256, Git objects,
checkout transforms and 32 bundle/source claims. Raw Git SHA-1 blob IDs and
content SHA-256 are distinguished, not used interchangeably.

## Per-lane independent decisions

| Lane and pinned revision | Verdict | Independently observed evidence | Strict scope/limitation |
|---|---|---|---|
| A `eb56684eaa10dc9b765927ef8e883c7d56cb025b` | **PARTIALLY SUPPORTED** | tau=800 rescues **19/33** original retention-limited streams; tau=8000 **31/33**. All **75/75** drive-limited streams remain noncrossing. | Signed event-time impulse accumulation, gain=1, unchanged threshold/cap; crossing is representability, not emission. Historical component crossings **108 → 166/167**, clipping **0 → 121/179 events**; longer retention is not behavior-preserving. |
| B `41a0a28f6f85023b8933a47650f66628b0a9ceb0` | **SUPPORTED** | Target critical gain **1.8425872009402644–3.28743886088831**, target median **2.8548209160858264**. Gain **3.3203132494971928** crosses **75/75** target streams, plus **33** non-target streams. | Mathematical first-boundary sufficiency only. Later states are correctly censored, not counterfactual neuron dynamics. Non-target crossing is not measured task harm; hardware, noise sensitivity and selective utility are unproven. |
| C `609b2e5f8a7ae123f9b7f7da5c89378e29353624` | **PARTIALLY SUPPORTED** | **16 fixtures, 48 runs, 23,040 tested/control event records** independently reconstructed. Spike-chain later misses: robust **0/4**, adaptive **4/4**. | Protection is not universal: robust mixed-sign misses **11/20**, drift false admissions **71**; adaptive drift **50**, stationary adaptive/robust **28** each. Fixed misses **3/6** near-band signals. No single universally clean qualifier. |
| D `deb01f07a0d6b315855d2fab57d558be303f95f3` | **SUPPORTED** | **30** signed synthetic trajectories, **44 inputs / 40 outputs**; three short moderate inputs compress to **1** output; isolated extreme drives **8/12/32 → 2/3/7** outputs. Independent queue replay agrees on state, exact rational timing, outputs and neutral recovery. | Only frozen synthetic charge-drain regimes, not reachable network input or preserved information. Threshold/marginal inputs **1/1.01** produce no output after leak; separated moderate inputs produce **2**. Weak-drain negative produces **3**, still fails one-output compression. |
| E `4e413415a31853877333810d7093f415f93f72f7` | **PARTIALLY SUPPORTED** | Eight primitive families; eight exact discrete-part public offers verified from retained sources **and fresh independent GETs**. Two independent FPAA distributor GETs remain **403/BLOCKED**. | Plausible individual parts/compositions, not validated build-ready circuits or owner access. Region/budget/inventory unknown. FPAA tools/CAMs/board interfaces and bounded-output implementation unresolved. E criteria and findings first appear in the **same commit**: prior declaration cannot be proven from committed history. |
| F `8cddf9d5d3fc0ea6971dc54645e8033c290dc852` | **PARTIALLY SUPPORTED** | **2,420** rows; output-drive proxy **2,185** opportunities, **1,950 existing-edge duplicates**, **235** novel geometrical shortcut/fan-in proxies over **108 streams**, all for **one endpoint pair**. Independent pointer, sign, ratio, lag, duplicate/repetition and trigger-direction checks agree. | Novel target-emission associations **0**. Local-deposition **235/235** are existing-edge duplicates. Source intrinsic deltas and source-local return observation unavailable; prospective delay, reachable admission, task utility and meaningful candidate usefulness remain blocked. No mutation occurred. |
| G `42698364392901de955ca04a770c975a1b0a94d2` | **PARTIALLY SUPPORTED** | **3,840** sampled rows plus **168** corners. Reconstructed parameter/noise draws and **516,666** event boundaries in positive, negative and offset-mirror groups. Failed samples per 768: nominal **0**, ±2% **1**, ±10% **81**, ±25% **418**, ±50% **631**. | Independent assumed stand-in, **not A+B+C+D composition or hardware yield**. At ±10% accumulation/compression/return fail **47/14/28**; neutral failures **36** at ±25%, **172** at ±50%. State/output bounds and mathematical mirrors pass by model/fixture assumptions, not physical certification. |

### Predeclaration and retained correction audit

- A: `add3d0c` declares fixed rates; `ec5231d` corrects physical-vs-Git pin
  before retained results. Initial exit-2 abort and distinct hashes remain.
- B: `4b15942` freezes recurrence/first-cross stop and analytical brackets;
  `aa878c3`/`38891b8` record materialization and immutable-blob loading before
  `1530b9c` results. No outcome-driven gain search was found.
- C: `3e03a1b` freezes methods, fixtures and scoring before `609b2e5`.
- D: `6ece0de` freezes regimes. `9c75e54` corrects a weak-drain test
  prediction **2 → 3**, preserving the scientific one-output requirement and
  the initial failure. `ee522bf` changes only empty-input recovery accounting;
  the pre-idle-correction artifact is retained. No drain/fixture/criteria tuning.
- E: `d19b206` contains criteria, code, source catalogs and results together.
  The lane reports writing criteria before classification, but Git does not
  independently demonstrate that ordering. Treat as documentary evidence,
  not a verified preregistered experimental selection.
- F: `8af8d73` freezes the two separate proxy/deposition rules;
  `39f99b1` corrects checkout provenance before `8cddf9d` results.
- G: `8406de7` freezes equations/draws/gates. `b0539cd` is explicitly
  post-outcome packaging/tests; it does not change the frozen model/gates.

Raw lane negative, pre-correction, retrieval-failure and full-test evidence
was neither overwritten nor silently waived.

## What can and cannot be synthesized

**Retention:** finite slower leak helps a subset with actual signed deposited
drive, but does not cure absent/insufficient drive. Historical saturation and
crossings change. Noise retention and useful memory are not interchangeable.

**Gain:** a modest dimensionless deposition factor suffices for these fixed
prefixes at tau=80. That is not exclusive causal attribution or stable/selective
network behavior. No deposition-gain result repairs 212 no-reception streams.

**Noise without self-contamination:** isolated spike inflation can be reduced,
but repeated mixed-sign excursions still inflate the estimator and drifting/
larger noise is falsely admitted. Robustness of a composed baseline estimator,
noise qualifier and accumulator is unmeasured.

**Compression/multievent:** independent dissipative output generation works on
D's declared synthetic trajectories. D's drain=4, delayed opportunities,
unit output and leak are not G's 0.75T discharge, immediate threshold output
and tanh return. Neither establishes that real routed task inputs reach those
regimes. Suppression/consumption may discard predictive information.

**Buildable owner-accessible hardware:** individual discrete parts have public
offers; an owner-accessible, bounded, calibrated circuit has **not** been
demonstrated. Manufacturer FPAA orderability is not independently verified
inventory, tool availability or semantic equivalence. RC/time units, voltage
headroom, signed deposition, reset, finite event control and local energy
accounting still need a design and owner constraints. No purchase/build is
authorized.

**Candidate opportunities without mutation:** F shows one geometrical
source→destination shortcut question repeatedly, not 235 independent useful
edges. Association is mostly forced by retained route delays/trigger selection,
with no capacity pressure or novel downstream emissions. Missing source-local
observations cannot be replaced by global offline scoring as a runtime policy.

**Analog robustness:** G's tight assumed band survives nearly all draws;
ordinary wider bands do not. Correlated R/C, capacitance-dependent deposition,
gain/threshold and leakage interactions matter. Static bounded noise, exact
exponential/tanh/discharge, no integrator bias/parasitics/thermal drift and
limited synthetic fixtures prevent a commercial tolerance/yield inference.

**Unresolved block interactions:** qualifying excess changes amplitude and
timing; longer retention retains both noise and signal; gain affects headroom
and false crossings; capacitance changes both gain and leak; output drain
changes subsequent state and predictions; shortcut admission changes exposure,
delays and cancellation; hardware bias/offset may prevent neutral return.
The isolated successes cannot be multiplied into an integrated success.
No matched composition, predictive-error/delayed-credit preservation,
task accuracy, useful high-cost survival, energy advantage, or hardware
trace parity was measured in this review.

## Validation and evidence interpretation

Fresh focused tests, unchanged lane pins: **306 passed**
(A 74, B 16, C 18, D 98, E 18, F 55, G 27).
Governance core/routing/locality/boundedness/prediction/credit/energy/
structural regression selection: **332 passed**.
Additional explicit canonical-neuron/predictive-coding selection:
**21 passed** (353 passing governance regression tests in these two selections).

Required full suite ran **only in governance** at `4b11e0e`, Python 3.11.5
from the explicitly configured `.venv`, `PYTHONPATH=governance worktree`,
`PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`, with **no Git overrides**:
**1,324 passed, 2 failed, 7 errors, 1 CUDA skip; pytest exit 1**,
192.51 seconds reported by pytest (195.64 seconds harness elapsed).
Harness completion is not a pytest pass. Lane code was deliberately absent
from this suite; focused lane tests are separate, not a composed full suite.

The supplied baseline log at the same revision had **1,325 passed, 1 failed,
7 errors, 1 CUDA skip; exit 1**. The pinned-source failure/seven setup errors
remain. The additional failed check is
`test_luna46_depth_scaling_diagnostic.py::test_real_retained_artifacts_integrity_only`:
catalog Git bytes **7,121**, SHA-256
`a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`,
versus checkout **7,122**, SHA-256
`5c41184dc9b9b5872263bcbbc1e5fc406789101c27942480b9cfb6b33c87da80`.
Exact LF→CRLF transformation explains the difference. Neither hash nor test
assertion was changed; immutable-blob validation does not waive raw-file failure.

The source/fixture pins, scientific equations and retained replay are
interpretable despite these separately disclosed materialization failures.
**Repository-wide green regression/integration readiness is not claimed.**
The supplemental process-local newline diagnosis and exact read-only replay
statuses are recorded in the final handoff and `test-summary.json` /
`replay-executions.json`, not substituted for the raw full result.

Supplemental process-local `core.autocrlf=false`, `core.eol=lf` testing of
Luna-44 fixture/verifier and Luna-46 produced **181 passed, 3 failed,
0 errors; exit 1**. The seven setup errors disappear when the temporary
pinned source has LF bytes. Two failures remain at generated-fixture
comparison (byte offset 490 and semantic digest), plus the unchanged physical
catalog hash failure. Those generated-fixture mismatches are **not merely
line endings**: exact regeneration of the frozen Linux fixture on this
Windows interpreter remains unproven/failed. This is a separate, previously
documented platform reproducibility limitation. The retained frozen bytes
and their internal scientific reconciliation still pass. No global Git
configuration, assertion, source, fixture or lane evidence was modified.

Pylance's file-syntax tool could not resolve this isolated governance file;
runtime execution and compilation are the fallback, not an editor-analysis
pass. No physical experiment, efficacy run, production composition or new
successor was executed.

## Reproduction and navigation

All shell commands must explicitly set the governance worktree. Use
`C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe` with:

- `artifacts/luna47-review/run_tests.py focused`, `boundary`, `predictive`, `full`;
- `artifacts/luna47-review/independent_oracle.py`;
- `artifacts/luna47-review/verify_manifests.py`;
- `artifacts/luna47-review/run_replays.py`;
- `artifacts/luna47-review/verify_public_offers.py` (public GETs; stock changes);
- `artifacts/luna47-review/summarize_tests.py`.

These reviewer harnesses refresh **reviewer-owned** reports only; they do
not regenerate/overwrite worker artifacts. Exact commands, executable,
environment, revisions, raw output, JUnit signatures and report hashes are
retained here. Scientific arithmetic is same-environment binary64; no
cross-platform numerical or hardware equivalence is promised.

Next decision owner: project owner, through Luna-0. Potential questions are
noise/retention/gain margins and information-preserving output behavior;
owner region/budget and build constraints; true source-local candidate
observability; and calibrated rather than assumed analog interactions.
Each would require fresh explicit authorization and a bounded predeclared
scope. **No successor scope or contract is created by this review.**
