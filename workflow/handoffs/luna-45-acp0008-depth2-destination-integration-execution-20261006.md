---
tpcn_handoff:
  agent: "Luna-45 separate execution worker; NOT independent reviewer"
  luna_identifier: "Luna-45"
  task_id: "luna-45-acp0008-depth2-destination-integration-execution-20261006"
  status: "execution complete; PASS / NOT SUPPORTED IN THIS SETUP; independent review pending"
  contract_version: "1.2"
  branch: "copilot/luna45-depth2-destination-integration"
  base_revision: "b4536f151cb8f73a173aac225df24c8fc2259c88"
  authorization_revision: "9af6b4435ac581887f04f0951d0f7b16d7d661cd"
  runner_revision: "97a93b394d071413075a1f102fdef695664722ff"
  execution_revision: "97a93b394d071413075a1f102fdef695664722ff"
  runner_sha256: "078a4fb7020414a3a017006291b778576ea72aeff08024063d7040ffe3307085"
  configuration_digest: "cb6621ff403836e1b72b86a65375df11c2841df61030fbe5dd8a654a70394c1a"
  result_revision: "the artifact-publication commit containing this handoff; returned explicitly to the lead"
  independent_review: "NOT PERFORMED; lead orchestrator dispatches fresh Luna-0 separately"
  architecture_change: false
  proposal: null
---

# Luna-45 Phase 2 execution handoff

## Outcome and boundary

**Runner outcome: PASS / NOT SUPPORTED IN THIS SETUP.** All mandatory initial
gates, destination equation verification, and same-environment full replay
passed. The calibrated destination arm has **zero** genuine
integration-mediated canonical emissions. The default and disabled arms also
have zero canonical destination emissions, including zero direct emissions.
This is a valid bounded negative result for the authorized setup, not a
platform failure or task-efficacy result.

This is an execution-worker report, **not independent approval**. No reviewer
was launched. No efficacy, classification, accuracy, prediction benefit,
reward/utility, energy benefit, structural growth, hardware equivalence,
architecture promotion, or Luna-46 claim is made. ACP-0007 is unchanged and
disabled. ACP-0008 remains experimental, opt-in and unpromoted. Historical
Luna-42 PASS WITH FOLLOW-UP, Luna-43 BLOCKED / DESTINATION COMPARISON
UNDETERMINED, and Luna-44 evidence-quality PASS WITH FOLLOW-UP are preserved.

## Superseded stop and pre-execution corrections

The [historical stop handoff](luna-45-acp0008-depth2-destination-integration-20261006.md)
at `0c34722e913042497c7452a3963854a3ce2bbed4` is **unchanged**. This new
handoff supersedes its unresolved execution status, not its factual record.
The first focused test run was **48 passed, 1 failed** and correctly stopped
publication/science at that time.

The owner independently identified the test as overstrict and explicitly
authorized resumption with an invocation-based regression. The contract
prohibits **calling generator/benchmark paths for scientific inputs**, not
transitive imports. Importing production classes transitively loads
`tpcn.spiral_benchmark` through `tpcn/__init__.py`; this does not generate
inputs. No production initializer was changed.

The corrected regression is named
`test_frozen_inputs_forbid_generation_calls_but_allow_transitive_benchmark_import`.
In a fresh process it replaces `generate_spiral`, `make_spiral_dataset`,
`generate_matched_pair`, `generate_traversal_pair`, and `generate_variant`,
including loaded aliases, with immediate failures. It also blocks dedicated
Luna-34 and fixture-builder imports, patches relevant functions if those
modules are present, loads the exact committed frozen fixture, validates
file/semantic identity, and exercises all arms on a **synthetic-only unit
fixture**. Synthetic mechanism checks are not retained scientific results.
The dedicated modules remain absent. The corrected suite first passed all
54 tests.

Runner/tests/config were published at
`2464a2ae13ac1e857ef08ea65c72a45b4f06c8e5`. Its **preflight**, before any
science or output-directory creation, stopped on two byte-identity checks:
the working runner used CRLF while its Git blob used LF, and an overstrict
handoff check conflated the owner's exact working-file SHA with the LF
committed-blob SHA. These were a runner provenance defect, not a scientific
gate failure. No retained output existed and no scientific run started.

The correction retains two independent exact handoff pins, does not normalize
fixture or neural quantities, and leaves the handoff itself unchanged:

- owner-confirmed CRLF working file:
  `c326548c8bd1b6795caca1bc2694993523c291ff1845e47b4f7e0c64dc61228e`;
- exact LF Git blob at baseline `b4536f1...`:
  `498ce49dd8f32f9d971f1c893e46bdce9ea2247007e66461512e885a6e3e41d9`.

An added regression verifies both hashes and demonstrates that the difference
is solely CRLF versus LF. Only the **two owned Luna-45 source files** were
formatted to LF, so working runner bytes exactly equal execution-commit
bytes. No prior file, global Git setting, or scientific tolerance changed.
Final focused tests: **55 passed**. The corrected runner/config publication
is `97a93b394d071413075a1f102fdef695664722ff`; the earlier config-only
publication is retained unchanged, but is not the executed config.

The configuration digest change from earlier candidates reflects only
predeclared evidence-field metadata and the separate exact handoff pins.
Source, relay, destination conditions, resource bounds and topology were
not tuned or changed.

## Execution chronology and exact provenance

Before editing, clean `HEAD` and published branch HEAD were exactly
`b4536f151cb8f73a173aac225df24c8fc2259c88`. Before science, clean local HEAD
and published branch HEAD were exactly
`97a93b394d071413075a1f102fdef695664722ff`, with no untracked files.
Preflight verified authorization/baseline/fixture ancestry, exact committed
runner bytes, exact published configuration bytes, both handoff pins,
historical evidence pins, and the complete frozen fixture/manifest/source pins.

| Identity | Executed value |
|---|---|
| Authorization | `9af6b4435ac581887f04f0951d0f7b16d7d661cd` |
| Final authorization handoff revision | `b4536f151cb8f73a173aac225df24c8fc2259c88` |
| Runner and non-null execution revision | `97a93b394d071413075a1f102fdef695664722ff` |
| Exact executed runner SHA-256 | `078a4fb7020414a3a017006291b778576ea72aeff08024063d7040ffe3307085` |
| Final config digest | `cb6621ff403836e1b72b86a65375df11c2841df61030fbe5dd8a654a70394c1a` |
| Final published config-file SHA-256 | `a19bf911ebe04c52aba7d83e376faac853519db3308419ca8bfcad35143858e1` |
| Frozen fixture revision | `6413cffe6982bccc6698af6bebfae51f04e71dd9` |
| Fixture bytes / file SHA-256 | 3,451,453 / `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629` |
| Fixture semantic digest | `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305` |
| Manifest revision / Git blob | `86e5a2f389af06b06bf04a614edaed88e0847902` / `eb9179abae7eed10891e6022832f16735111b220` |
| Manifest SHA-256 | `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22` |
| Reviewed Luna-44 capture-driver working-byte SHA-256 | `782ab6474251abfbf138156e4126d590536a423c878029a270686081c7caec37` |

The final frozen configuration is
[config.json](../../artifacts/luna45-depth2-frozen-config-20261006-r2/config.json).
Its digest was independently recomputed with `hashlib.sha256` over sorted-key,
compact UTF-8 JSON and compared to the runner result before execution.
The full source manifest is included in the retained execution artifacts.
Every recorded source path/revision/SHA was validated before any arm.

Environment: Windows 10 build 19045, CPython **3.11.5**, MSC v.1936,
64-bit AMD64. Each authoritative terminal Python command used:

```powershell
$env:GIT_CONFIG_COUNT='2'
$env:GIT_CONFIG_KEY_0='core.autocrlf'
$env:GIT_CONFIG_VALUE_0='false'
$env:GIT_CONFIG_KEY_1='core.eol'
$env:GIT_CONFIG_VALUE_1='lf'
$python='C:\Users\zathp\AppData\Local\Programs\Python\Python311\python.exe'
```

All execution metadata includes `sys.float_info`, exact revision/hash/config
identity and environment. Equation reconstruction uses only
`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`.
Copied payloads, elapsed subtraction, identities, source equality, ordering,
classifications/signs, bounds, cross-arm content and replay remain exact.

## Frozen conditions and complete execution

Only committed frozen `x/y/t` are scientific inputs. Each point's `float(x) +
float(y)` was independently computed per arm and replay, never taken from
the stored audit value. No generation/regeneration occurred for science.
The baseline materialization tests invoke their historical builder only as
validation, not as the source of Luna-45 science.

Fixed source integration `None`; fixed relay integration decay **0.0125**;
destination `None` / default **0.1** / calibrated **0.0125**. Existing
ordinary Model-B edges are exactly `source -> relay -> destination`, each
`w=1`, delay `1`, `d=1`, `r=0`, with no shortcut/return edge.
All other neuron parameters remain at reviewed defaults. The common
historical namespace preserves rather than normalizes canonical identities.
Each sequence/arm/replay creates fresh runtime/neuron state.

Both initial and replay each completed **320 sequences per arm**, seeds 0..4,
64 sequences per seed, consuming **5,164 points per arm**. Total:
**1,920 complete character executions**, **30,984 independently computed
point inputs**, **71,520 processed runtime events**.

### Ordered mandatory gates

| Gate | Initial and replay observation |
|---|---|
| G1 historical calibrated upstream | 320 exact retained calibrated records, 340,734 leaf comparisons per phase, all pass; largest equation residual **0** |
| G2 upstream cross-arm invariance | 960 sequence-arm comparisons per phase, canonical content exact, all pass |
| G3 independent admission/actual consumption | 960 sequence-arm reconciliations per phase, both edges and all-route reports pass; all missing/orphan/duplicate/mismatch categories **0** |
| G4 bounds/completion | 960 sequence-arm checks per phase, all pass; pending events **0** |
| Destination equation/discharge/classification | All 235 receptions in each arm verified; each enabled arm has 235 independent recurrence checks, no discharge or canonical emission |
| Same-environment full replay | All records/reports canonical-byte equal; every per-arm initial/replay digest identical |

G1 uses the **initial CALIBRATED** records in the authoritative
`artifacts/luna44-acp0008-independent-routing-rerun-20261005/`:
`results.json`, `summary.json`, `routing-initial-enqueue.json`, and
`routing-initial-reception.json`. Their complete file pins, artifact
digests, runner revision `4baab60f87b820db800e04d0eb3277fb0e94f9b3`, config
digest `942b86a9cd7a3965265ec9d01aff7e0b0e2bf68b309f0e0bd22dc4cbae71884e`,
fixture identity and raw-record correspondence are retained. Compared fields
include source emissions, actual first-edge admissions/receptions, relay
trajectory/integration/emissions and onward admissions, plus raw input
identity/digests. No older result overwrites current evidence.

Queue-side capture is successful `EventQueue.push_propagated` admission plus
separately attached production route context. Receiver capture is successful
`MultiExcursionNeuron.receive_event` consumption, receiver logical timestamp
and before/after state. The source-only mutation regression ran and rejected
reconciliation with a separately reported source mismatch. Complete identities,
payload decimal/hex/bits, roots/truncation, path/depth, queue sequence and
originating emission are retained at both sites.

### Counts, state and bounds

The following values reproduce exactly in replay:

| Arm | Source canonical emissions / actual relay receptions | Relay integrated / direct emissions | Destination receptions | Destination direct / integrated emissions | Maximum destination abs(z) |
|---|---:|---:|---:|---:|---:|
| DESTINATION_DISABLED | 1,715 / 1,715 | 235 / 0 | 235 | 0 / 0 | no integration state (report value 0; location null) |
| DESTINATION_DEFAULT | 1,715 / 1,715 | 235 / 0 | 235 | 0 / 0 | 0.39794417177052166 |
| DESTINATION_CALIBRATED | 1,715 / 1,715 | 235 / 0 | 235 | 0 / 0 | 0.8284450023885981 |

Default maximum: `c01-034`, `relay:excursion:4`, arrival
`199.30530327403912`, signed `z=-0.39794417177052166`.
Calibrated maximum: `c04-017`, `relay:excursion:6`, arrival
`236.40859083136408`, signed `z=-0.8284450023885981`.
Neither reaches unchanged discharge quantum **1.0**. Both enabled arms retain
all independent decay, input, discharge-decision/sign/amount and post-update
fields; the disabled arm has no integration state/trace.

Per arm/phase: **1,950 admissions = 1,950 receptions = 1,950 matched**,
comprising 1,715 source-to-relay and 235 relay-to-destination events.
Per phase across arms: **5,850** matched routes; across initial+replay:
**11,700**. All reported unmatched enqueue/reception, orphan, duplicate
enqueue/reception, source, destination, event-ID, payload, time, path/depth
and provenance mismatch counts are zero.

Identical per-arm high-water marks: queue **3/128**; runtime events per
character **107/1024**; neuron events **69/4096**; activity **25/1024**;
eligibility ledger occupancy **19/1024**; predictions **1/8**, expiry 4.0.
Topology uses two edges/routes against capacities 3, fan-in/out peaks 1
against limits 2. Settling horizon is 4.0; every character completes with no
pending work. Each arm processes 11,920 runtime events per phase. All
per-sequence values and per-ledger capacities/occupancy are retained.

No destination emission occurs, so unique emitting characters, direct
emissions, integration-mediated emissions, genuine chains, and discharges
are all zero. Relay-to-destination-emission timing and receptions-before-
discharge lists are therefore **empty / not applicable**, not fabricated.
All reception-prefix evidence is retained even in this negative case.
The calibrated/default z difference is observed, not efficacy.

The conditional **candidate-opportunity precursor** scan is **not performed**
in any arm because the canonical destination-emission prerequisite is absent.
Counts/pairs are zero/empty with the prerequisite reason implicit in
`scan_performed=false`. The declared window remains 4.0 and endpoints
source canonical emitter -> destination canonical emitter; the relay is never
a precursor endpoint. No candidate, controller, growth or pruning runs.

## Replay and persistent artifacts

| Arm | Identical initial and replay phase digest |
|---|---|
| DESTINATION_DISABLED | `1f2969a59b1febb8464442143b1bb6da1e0b84f4b256f122c3508133314c4a01` |
| DESTINATION_DEFAULT | `abc8c4e288dc4ffb249b62e928c09142dd34fd01491d3deaf95ff5feabc4beba` |
| DESTINATION_CALIBRATED | `fe3c3a7099f172baf7b0d2633dde34945350b91dd79a8e4f2be81a591eac3ede` |

Summary science digest:
`d9e4aa1fe98cd72b4d5fd6a028f722305d95d1ffc784b72dcb1ca2445cc3189b`.
No initial or replay blocker exists. Initial artifacts were persisted before
replay and never replaced. The tested blocker paths produce no replay/science
digest after an initial blocker and preserve the initial digest/files after
a replay blocker.

All raw records and per-arm results are retained in
[the new execution directory](../../artifacts/luna45-acp0008-depth2-destination-integration-20261006/):
config, summary, per-arm initial and replay results/reports, six enqueue and
six reception raw files, and separate initial/replay gate evidence.
There are **22 execution files**, **386,727,576 bytes**, plus the **7,121-byte**
execution-integrity catalog: **23 retained output files** total.

The [integrity catalog](../../artifacts/luna45-acp0008-depth2-destination-integration-20261006/artifact-integrity.json)
records every execution file's SHA-256, internal artifact digest and size,
including summary, without a self-referential digest. Execution readback
verified all file/internal digests, phase digests, raw capture correspondence,
and canonical-byte equality of initial/replay records and reports. This is
persistence verification, **not independent review**.

| Artifact / digest | Value |
|---|---|
| Execution config file SHA-256 | `0c8abbb1fb68f7b856a9f0718b0eef2a307943b3290ccf3e1bfed049d9dd111a` |
| Summary file SHA-256 | `74968daa82fce731b1a7c8445aa75d756c37a89d36431077ab0e9345f7283c32` |
| Summary internal artifact digest | `22f9236c7ce4a597e13ebe0e6543c7cf438a34db46b08736001710bc9f325803` |
| Ordered execution-file catalog digest | `ba8b040fcc57c1e46364f1264a2f64c99d33c4c50844d1653f19f8e38d1caa58` |
| Integrity catalog file SHA-256 | `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e` |
| Integrity catalog internal digest | `60533846dcdc11953edb2c84621e0cfaa122136c9a678c10f01a775fbf87b27f` |

Digest material includes fixture/input/config identities, source emissions,
both independent capture streams, relay trajectory/emissions, complete
destination evidence, arm reports, bounds/pending counts and reconciliation.
No wall-clock/PID/environment fields enter phase digests. Static frozen
provenance paths are part of the frozen config, not volatile output paths.

## Validation commands, results and all failures/skips

Commands below use the process-local environment and `$python` above.
No dependency installation was required.

| Command / check | Result |
|---|---|
| `git rev-parse HEAD`; `git status --porcelain --untracked-files=all`; `git branch --show-current`; `git ls-remote origin refs/heads/copilot/luna45-depth2-destination-integration` | Exact clean start and exact published execution revision verified |
| `& $python -m pytest -q -rs` before implementation | **1089 passed, 2 known failures, 1 CUDA skip**, 36.24 s |
| `runTests` on new absolute test path | No tests discovered; not treated as success; repository pytest used |
| `& $python -m pytest tests\test_luna45_acp0008_depth2_destination_integration.py -q -rs` first attempt | **48 passed, 1 failed**, 9.15 s; overstrict import assertion; stopped and published historical handoff |
| Same command after owner-authorized invocation-guard correction | **54 passed**, 12.63 s |
| Regression selection command below | **327 passed, 2 known failures**, 41.95 s |
| `& $python -m pytest -q -rs` after first implementation | **1143 passed, 2 known failures, 1 CUDA skip**, 68.86 s |
| `& $python run_luna45_acp0008_depth2_destination_integration.py --publish-config` | Config-only r1 publication before science; digest `b1229454807eca1e7d76f638fdc162fffa60a3e3537e25cff438484d3b5a8fec` |
| `collect_provenance()` preflight at `2464a2a...` | **BLOCKED before science**: runner working/committed bytes differed; handoff working/committed hash conflated |
| Same focused pytest command after exact separate-pin correction and owned LF formatting | **55 passed**, 10.60 s |
| `& $python -m pytest -q -rs` final pre-science | **1144 passed, 2 known failures, 1 CUDA skip**, 51.96 s |
| `& $python run_luna45_acp0008_depth2_destination_integration.py --publish-config` with r2 path | Final config digest and file hash in provenance table; no scientific input processing |
| Preflight `collect_provenance()`, independent `hashlib` config digest, `load_inputs()`, `load_history()` at `97a93b3...` | Passed; clean published exact runner, 320/5164 fixture inventory, 320 historical calibrated records, complete pins |
| `& $python run_luna45_acp0008_depth2_destination_integration.py` | One full retained initial + replay run; exit **0**, PASS / NOT SUPPORTED IN THIS SETUP |
| Inline `& $python -` execution readback using `file_hash`, `_artifact_digest`, `phase_digest`, canonical record/report bytes and raw-event correspondence | 22 execution files verified; integrity catalog retained; all checks passed |
| Pylance runner syntax and VS Code Problems for both owned sources | No syntax/errors reported; not independent correctness approval |
| `git diff --check`; `git diff --cached --check` | Passed at publication checkpoints |

Exact regression selection:

```powershell
& $python -m pytest tests\test_luna45_acp0008_depth2_destination_integration.py tests\test_luna44_acp0008_canonical_fixture_rebaseline.py tests\test_luna44_canonical_fixture.py tests\test_luna44_canonical_fixture_verification.py tests\test_excursion_neuron.py tests\test_excursion_integration.py tests\test_e2_multi_excursion.py tests\test_event_runtime.py tests\test_topology.py tests\test_luna38_excursion_integration_state.py tests\test_luna42_acp0008_corrective_calibration.py tests\test_luna43_acp0008_destination_integration_mechanism.py -q -rs
```

Both baseline failures remained unchanged and were never weakened, hidden,
or skipped:

1. `tests/test_luna44_canonical_fixture.py::test_two_fresh_process_materializations_match_committed_fixture`
2. `tests/test_luna44_canonical_fixture_verification.py::test_two_fresh_process_materializations_match_exactly`

The sole skip was `tests/test_gpu_visualization.py:61`: **CUDA unavailable**.
Pytest full/regression runs with the two known failures return exit 1;
the final shell's trailing successful `git diff --check` returned shell exit
0, but did **not** change or conceal the reported pytest failures.
There were no other test failures beyond the initial owner-adjudicated
import-guard false-positive. The pre-science provenance blocker is separately
reported above. No mandatory scientific gate failed.

## Owned publication, limitations and return

Owned implementation:
[runner](../../run_luna45_acp0008_depth2_destination_integration.py) and
[focused tests](../../tests/test_luna45_acp0008_depth2_destination_integration.py).
Only new Luna-45 artifacts and this new execution handoff are added by the
scientific publication. The old stop handoff and both config-only publications
remain unchanged. No architecture/workflow document, previous evidence,
fixture/manifest, generator/builder/verifier, production neuron/runtime/
routing/topology, or ACP was modified.

Limitations: this is the fixed frozen-fixture CPU setup only; no calibrated
destination emission was observed. Genuine-chain/timing/precursor branches
were exercised only in synthetic unit checks, not claimed as positive task
evidence. No cross-platform generator-parity claim or work occurred.

**Return:** the lead orchestrator may dispatch a fresh independent Luna-0
review of this exact executed runner/config and artifact publication. This
worker does not self-review or approve the evidence. No successor or Luna-46
is authorized by this handoff.
