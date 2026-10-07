---
tpcn_handoff:
  agent: "Luna-47C implementation worker; independent Luna-0 review pending"
  luna_identifier: "Luna-47C"
  descriptive_name: "Adaptive noise qualification and deadband"
  task_id: "luna-47c-adaptive-noise-qualification-20261006"
  component: "Isolated synthetic input qualifier"
  status: "complete - PARTIALLY SUPPORTED; independent review pending"
  contract_version: "1.2"
  branch: "copilot/luna47c-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  implementation_revision: "3e03a1b3ad5f020a752dab796db157764cb784b5"
  result_revision: "Outcome publication commit containing this handoff; returned in final report"
  dependencies: ["Luna-0 published authorization", "Luna-46 reviewed MIXED context only"]
  owner: "Project owner"
  classification: ["MECHANISM EXPERIMENT", "SYNTHETIC", "NOT EFFICACY"]
  hypothesis: "Robust target clipping reduces spike-induced envelope contamination and later suppression."
  counter_hypothesis: "Robust estimation still suppresses meaningful clusters or under-tracks noise."
  interfaces_relied_on: ["experiments/luna47c/PROTOCOL.md", "Qualifier.process(timestamp, raw)"]
  label_information_boundary: ["Truth is evaluator-only; no production imports or output feedback."]
  timing_assumptions: ["Strict increasing dyadic synthetic timestamps; event-local elapsed time; first dt=1."]
  reset_boundaries: ["Fresh B=0,N=.25,last_time=None per fixture, method and control."]
  resource_bounds: ["Three scalar state values plus immutable configuration; 16 fixtures x 240 events x 3 methods; matched controls."]
  authorized_scope: ["Fixed, adaptive and robust deadbands; synthetic scoring, replay, tests and publication."]
  unauthorized_scope: ["Accumulator, other lane consumption, production, topology, ACP, efficacy, merge, successor or promotion."]
  controls: ["Committed pre-outcome protocol", "Signal-free paired controls", "Exact sign mirrors", "Fixed tolerances and verdict gates"]
  measurements: ["False admissions, misses, baseline error/pull, noise contamination, recovery and sign symmetry"]
  information_boundary_check: ["PASS: mechanism accepts time/raw only; evaluator truth mutation preserves traces; no production imports or feedback."]
  hardware_mapping: ["Software binary64 only; no physical realization or equivalence claim."]
  architecture_invariants_touched: ["A01/A02 event-local state", "A07 truth isolation", "A08 finite bounds", "A15 portability not established"]
  preserves: ["All production/governance/topology files", "Luna-46 MIXED", "ACP-0007/0008 status"]
  architecture_change: false
  proposal: null
  files_changed: ["experiments/luna47c/", "tests/test_luna47c_qualification.py", "artifacts/luna47c/", "workflow/handoffs/luna-47c-adaptive-noise-qualification-20261006.md"]
  tests_added: ["Fixture coverage, truth isolation, exact equations, bounds, time/config validation, sign symmetry, contamination and replay"]
  tests_passing: ["Focused 18", "Boundary regression 79", "Combined 97", "Full suite passing cases 1342", "Compileall", "Exact replay/source/manifest verification", "git diff --check"]
  tests_failed: ["Full suite exit 1: 2 failures, 7 errors; exact retained JUnit signatures and baseline line-ending diagnostic in artifacts/luna47c/"]
  tests_not_run: ["Physical hardware, production integration and task efficacy excluded", "CUDA test skipped: unavailable", "Pylance worktree discovery unavailable"]
  assumptions: ["Synthetic truth is injected-source presence, not threshold crossing."]
  unresolved: ["Independent Luna-0 review pending", "Full suite remains failed on inherited pinned-source/catalog checkout checks", "Synthetic noise/admission tradeoffs do not establish a universally useful qualifier"]
  recommended_next_agent: ["Independent Luna-0 review after pushed completion; no successor"]
---

# Luna-47C adaptive noise qualification

## Outcome and owned scope

**OBSERVED — PARTIALLY SUPPORTED** under the predeclared protocol. The explicit
spike-contamination suppression chain occurs, and robust clipping protects the
four later probes, but false admissions and mixed-sign misses remain. No method
is promoted or selected using an aggregate score.

Protocol, generator, all mechanism/evaluator code, tests and pre-outcome handoff
were committed as `3e03a1b3ad5f020a752dab796db157764cb784b5` before any tests
or scoring. The initial handoff state is retained in that commit. The first
scoring package records that exact clean source revision. No outcome-driven
parameter, fixture, truth, metric, test or code revision occurred.

Owned files:

* `experiments/luna47c/{__init__.py,qualifier.py,fixtures.py,evaluate.py,PROTOCOL.md}`
* `tests/test_luna47c_qualification.py`
* `artifacts/luna47c/{replay.json,summary.json,manifest.json,validation.json}`
* `artifacts/luna47c/{focused.xml,boundary-regression.xml,full-suite.xml,.gitattributes}`
* this handoff.

The lane-local attributes preserve canonical artifact bytes through Windows
checkout; they do not change repository/global settings or shared artifacts.
Raw pytest JUnit XML is marked binary for diff only (still readable XML) to
retain traceback whitespace without enormous line diffs. Source/docs and
text-evidence whitespace checks pass; no traceback contents are removed.
Only immutable configuration plus B, N and last timestamp persists inside the
qualifier. E is computed from prior B/N and returned, never accumulated.
Evaluation traces and signal-free control runs are downstream-only.

## Architecture evidence

| Boundary | Evidence and preserved constraint |
|---|---|
| A01 | Qualifier executes only on explicit irregular arrivals; no global tick/idle loop. |
| A02 | Timestamp-local baseline/noise updates use actual elapsed time; fresh reset per run. This is a qualifier, not a canonical-neuron replacement. |
| A07 | `process(timestamp,raw)` accepts no truth; fixture/evaluator modules never imported by mechanism; truth-mutation test preserves outputs. Global metrics never feed it. |
| A08 | Raw bound 16, baseline bound 4, noise .05..16; three scalar state values; 10,000-event stress per method; 23,040 bounded retained event records including controls. |
| A15 | Binary64 software reference only; scalar operations are descriptive, no physical hardware or backend equivalence established. |

No A-clause departure/change, ACP, production/neuron/runtime, topology, routing,
governance, other lane implementation/result consumption, accumulator, efficacy,
branch merge or successor. Luna-46 reviewed **MIXED** remains context only and
unchanged. A retained catalog was hashed solely to diagnose the inherited
Luna-46 full-suite failure, not used to construct or tune qualification.

## Numerical results and comparisons

Strict admission is nonzero signed excess beyond `2*N_before`; no epsilon in
that decision. Binary64 comparison tolerance is **absolute 1e-12**, mirror
maximum observed error **0**; same-environment replay and count equality exact.
Recovery threshold **.025** for both paired baseline/noise differences, five
consecutive events. The formulas, tolerances, generation, evaluator truth,
reset and gates are frozen in PROTOCOL.md. Every fixture identity/hash,
configuration, timestamp, raw, B, N, E, post-state and control is in replay.json.

The table reports the + orientation; - orientation has identical scalar metrics,
false/miss counts and recovery times. All 24 method/family mirror comparisons
pass with zero error. Per-sign meaningful/missed/wrong-sign counts for **all
48 runs** are in summary.json and replay.json; no wrong-sign admission occurred.
B-error is maximum |B_before - actual baseline|; B-pull and N-contamination are
maximum differences from matched signal-free controls as defined in the protocol.
Recovery is elapsed synthetic time after the last meaningful excursion; N/A
means no meaningful signal, not zero recovery.

| Fixture | Method | False admissions | Misses/meaningful | Max B-error | Max B-pull | Max N-contamination | Recovery |
|---|---|---:|---:|---:|---:|---:|---:|
| stationary | fixed | 0 | 0/0 | .046833 | 0 | 0 | N/A |
| stationary | adaptive | 28 | 0/0 | .046833 | 0 | 0 | N/A |
| stationary | robust | 28 | 0/0 | .046833 | 0 | 0 | N/A |
| drift | fixed | 0 | 0/0 | .215453 | 0 | 0 | N/A |
| drift | adaptive | 50 | 0/0 | .215453 | 0 | 0 | N/A |
| drift | robust | 71 | 0/0 | .215453 | 0 | 0 | N/A |
| isolated | fixed | 0 | 0/3 | .050012 | .010464 | 0 | .5 |
| isolated | adaptive | 21 | 0/3 | .050012 | .010464 | 1.769729 | 17.75 |
| isolated | robust | 28 | 0/3 | .050012 | .010464 | .043734 | 2.75 |
| clustered | fixed | 0 | 0/16 | .125808 | .091983 | 0 | 27.75 |
| clustered | adaptive | 22 | 10/16 | .125808 | .091983 | .900186 | 27.75 |
| clustered | robust | 28 | 0/16 | .125808 | .091983 | .400265 | 27.75 |
| mixed signs | fixed | 0 | 0/20 | .048175 | .087130 | 0 | 22.5 |
| mixed signs | adaptive | 23 | 17/20 | .048175 | .087130 | .991238 | 22.5 |
| mixed signs | robust | 23 | 11/20 | .048175 | .087130 | .966523 | 22.5 |
| near boundary | fixed | 0 | 3/6 | .056494 | .021100 | 0 | .5 |
| near boundary | adaptive | 23 | 0/6 | .056494 | .021100 | .113213 | 5.75 |
| near boundary | robust | 27 | 0/6 | .056494 | .021100 | .050248 | 2 |
| contamination chain | fixed | 0 | 0/5 | .053400 | .053400 | 0 | 15.5 |
| contamination chain | adaptive | 0 | 4/5 | .053400 | .053400 | 1.758534 | 15.5 |
| contamination chain | robust | 0 | 0/5 | .053400 | .053400 | .048290 | 15.5 |
| noise step | fixed | 50 | 0/0 | .214666 | 0 | 0 | N/A |
| noise step | adaptive | 32 | 0/0 | .214666 | 0 | 0 | N/A |
| noise step | robust | 47 | 0/0 | .214666 | 0 | 0 | N/A |

**OBSERVED contamination chain:** N before the +8 spike is .05 for both
adaptive variants. Immediately after it, naive N is **1.8085337745823313**
(signal-free control .05), robust N is **.061059960846429756**.
Four later +.9 injections at indices 61,62,64,68 all cross their matched
signal-free thresholds. Adaptive misses **4/4**, robust **0/4**, fixed **0/4**.
Robust post-spike N is less than one-quarter naive N, so both predeclared chain
gates pass. The mirror produces the same result with signs reversed.

**OBSERVED negative results:** robust suppression is not prevented indefinitely:
mixed-sign activity produces noise contamination **.966523**, approaching
adaptive **.991238**, and **11/20** meaningful misses. Drift false admissions
increase from adaptive **50** to robust **71**. Stationary false admissions
are **28** in both adaptive variants. Fixed avoids many such admissions but
misses **3/6** near-band injections and admits **50** noise-step events, versus
adaptive **32** and robust **47**. The universal-no-errors gate fails.

**INFERRED tradeoff:** clipping limits one large event's immediate self-threshold
inflation, not all repeated-excursion contamination. The absolute-residual mean
tracker used here is not a guaranteed maximum noise envelope; multiplying it by
two does not eliminate peak admissions on the irregular periodic fixture.
Clipping can also delay tracking genuinely larger noise. Shared clipped baseline
tracking causes identical baseline errors/pull across methods, intentionally
isolating noise-estimator policy rather than jointly optimizing B and N.
No-signal paired contamination is zero by construction and says nothing about
noise-estimation accuracy. Recovery is incremental contamination recovery,
not a guarantee of correct subsequent noise rejection.

No aggregate winner, generalization, task efficacy or production utility is
inferred. Classification/prediction loss, reward, energy/joules, connectivity,
route latency and learning utility are **not applicable** to this isolated lane.

## Validation record

Interpreter: `C:/Users/zathp/Documents/programming/TPCN/.venv/Scripts/python.exe`,
Python 3.11.5, Windows, source revision `3e03a1b`. No RNG/seed, training or split.
Each terminal command used explicit Set-Location to the isolated worktree.

| Command/procedure | Observed result | Evidence |
|---|---|---|
| pytest focused plus event/runtime/neuron/topology selection | **97 passed** | initial terminal execution |
| pytest tests/test_luna47c_qualification.py | **18 passed** | focused.xml |
| pytest event_runtime, canonical_event_neuron, excursion_neuron, topology | **79 passed** | boundary-regression.xml |
| pytest full repository | **1342 passed, 2 failed, 7 errors, 1 skipped**, exit 1 | full-suite.xml, validation.json |
| python -m experiments.luna47c.evaluate | Completed, PARTIALLY SUPPORTED | replay/summary/manifest.json |
| same-process duplicate and fresh-process --verify | Exact science/source/manifest match | replay provenance and validation.json |
| compileall lane code/test; git diff --check | PASS | terminal and validation.json |
| VS Code tests/Pylance discovery | Could not discover isolated files; not a validation pass | validation.json; terminal fallback above |

The full suite remains **FAILED**. Exact failures:

1. `tests/test_luna44_canonical_fixture.py::test_two_fresh_process_materializations_match_committed_fixture`:
   worker rejects pinned-source bytes. Seven setup errors in
   `tests/test_luna44_canonical_fixture_verification.py` share that worker
   failure. This is consistent with the documented baseline Windows
   pinned-source/autocrlf materialization limitation; no assertions relaxed.
2. `tests/test_luna46_depth_scaling_diagnostic.py::test_real_retained_artifacts_integrity_only`:
   `published Luna45 catalog hash differs`. Read-only triage confirms checkout
   bytes 7122 / SHA256 `5c41184dc9b9b5872263bcbbc1e5fc406789101c27942480b9cfb6b33c87da80`;
   authorization-baseline Git bytes 7121 / SHA256
   `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`.
   Replacing CRLF with LF in memory exactly matches the baseline blob and
   expected digest. `core.autocrlf=true`. No shared evidence was changed.

CUDA unavailable accounts for the one skip. Full error messages are retained
in JUnit. No new shared implementation changes exist; a fresh full baseline run
was not performed, so wholesale baseline/full-suite equivalence is not claimed.

## Assumptions, limitations and unresolved gates

Synthetic injected-source truth is independent of admission, including
sub-band meaningful values. Eight deterministic families and mirrors are not
statistical generalization. Time-weighted periodic noise may alias. No parameter
search, sensitivity sweep, data-driven initialization, hardware, task efficacy,
real sensor benchmark or production integration. Exact replay is established in
this Python/libm environment only; cross-platform absolute tolerance is declared
but cross-platform execution is not tested.

Hash identities are captured from the committed frozen generator/source and
include full truth/input fixture serialization in replay.json; no external
preexisting fixture or other lane is needed. Evidence output is confined to the
lane package. Canonical SHA-256 hashes and the manifest establish bytes, not
protection against concurrent filesystem tampering.

Independent Luna-0 review is pending; full-suite checkout failures remain
unresolved. No winner or architecture recommendation is authorized.

## Reproduction and rollback

In the specified isolated worktree, use the configured interpreter:

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47c'
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m experiments.luna47c.evaluate --verify
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m pytest -q tests/test_luna47c_qualification.py
```

Fresh outcome capture requires a separate clean checkout of `3e03a1b` with no
existing replay.json; capture refuses overwriting retained science. Current
published checkout supports --verify without rewriting evidence.
Rollback is removal/revert of lane-owned commits only, or a separate checkout
of authorization `789dda5`; no production state or shared file changed.

## Next assignment and publication boundary

Push the completed owned package on `copilot/luna47c-investigation`; final
response records exact publication commit and remote parity. Stop after push
for independent **Luna-0 review** of code/truth isolation, frozen protocol,
fixture identities, metrics, limitations and retained failures. No merge,
integration, successor, Luna-48, ACP or architecture promotion is authorized.
