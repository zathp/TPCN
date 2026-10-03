# Luna-25 Completion Handoff — UCI Character Trajectories

```yaml
tpcn_handoff:
  agent: "Luna-25"
  luna_identifier: "Luna-25"
  task_id: "luna-25-uci-character-trajectories-reproducible-evidence-20261003"
  component: "UCI Character Trajectories sequential CPU benchmark adapter"
  status: "implementation/evidence published; handoff publication in progress"
  branch: "main"
  authorized_base_revision: "1642b991f82403140d0f29b5a2ff10b3d2628cda"
  execution_checkout_revision: "7e174de664bc116db77aad89c8bed08ca750bcd3"
  implementation_evidence_revision: "5cb17d9bb79c848c27805cb79484d9ab3cd0f5b8"
  result_revision: "implementation_evidence_revision plus this separate handoff publication commit; the latter is not self-recorded"
  architecture_change: false
  proposal: "Accepted ACP-0006; no ACP or A01-A15 changes"
  files_changed:
    - "scripts/benchmark_uci_character_trajectories.py"
    - "tests/test_uci_character_trajectories_benchmark.py"
    - "artifacts/luna-25-uci-character-trajectories/run_manifest.json"
    - "artifacts/luna-25-uci-character-trajectories/split_manifest.json"
    - "artifacts/luna-25-uci-character-trajectories/per_class_report.json"
    - "workflow/handoffs/luna-25-uci-character-trajectories-20261003.md"
  preserves:
    - "EXCURSION_V1 production/runtime semantics and accepted ACP-0006"
    - "Fixed topology, no structural-plasticity or downstream migration changes"
    - "No raw dataset committed"
  recommended_next_agent:
    - "Luna-0 Architecture Guardian for independent review"
```

## Scope, baseline, and repository state

The authorization names `1642b991f82403140d0f29b5a2ff10b3d2628cda` as
baseline. Publication started on `main` at `HEAD == origin/main ==
7e174de664bc116db77aad89c8bed08ca750bcd3`, the authorization publication
commit; the authorized baseline is its ancestor. The publication-start
worktree had the six Luna-25 deliverables untracked and no tracked diff. The
initial worktree state before the earlier partial implementation was not
captured, so this handoff makes no claim about that earlier state.

Adapter, tests, and three non-raw-data artifacts were committed as
`5cb17d9bb79c848c27805cb79484d9ab3cd0f5`. This completion handoff is
published separately after recording that implementation revision. No
production or unrelated files were changed.

The historical 160-record Luna-22 subset is **not reproducible from retained
evidence**: its exact member IDs and original loader/preprocessing code were
not retained. Accordingly, this work does not claim to reconstruct or
reproduce Luna-22's old result. It defines a new, explicitly versioned
`luna25-v1` benchmark baseline.

The work is limited to the standalone adapter, focused tests, non-raw-data
artifacts, and this handoff. No production core/runtime, experiment semantics,
visualization, research consumer, or existing handoff was modified. This
handoff does not close Luna-22 and does not assert repository-wide ACP-0006
integration readiness.

## Dataset identity and parser

Source: [UCI Character Trajectories, dataset 175](https://archive.ics.uci.edu/dataset/175/character+trajectories),
DOI `10.24432/C58G7V`, CC BY 4.0. The retrieved archive was
`character-trajectories.zip` from the UCI static download URL recorded in the
run manifest. Retrieval date: `2026-10-03`.

| Input artifact | SHA-256 |
|---|---|
| `character-trajectories.zip` | `5d2db017ef0d8cf0e65ed060c9e90399f78eb9f1e3cb63e22ca8c3ef4ba67d52` |
| `mixoutALL_shifted.mat` | `00ab9af03f74167b5ddee9d5f3e7ed3da8df0bc49d2e9c4078c51857fdc13ebe` |

The raw archive and `.mat` source remain outside the repository. The parser
validates the observed MATLAB schema: `mixout` contains one 3-by-T trajectory
per record; `consts.charlabels` holds one-based integer class codes;
`consts.key` maps those codes to class labels; and `consts.dt` is `0.005`
seconds. It verified **2,858 usable finite examples in 20 classes**, with
observed trajectory lengths 109–205 points. The class mapping in one-based
source-key order is `1:a, 2:b, 3:c, 4:d, 5:e, 6:g, 7:h, 8:l, 9:m, 10:n,
11:o, 12:p, 13:q, 14:r, 15:s, 16:u, 17:v, 18:w, 19:y, 20:z`.

The UCI schema describes the three retained dimensions as x, y, and pen-tip
force, and says the data were numerically differentiated and Gaussian
smoothed. `consts.dt` confirms the 200 Hz interval. The adapter takes only
the current point's first two rows, interpreted as x/y velocity components,
and computes `x_velocity + y_velocity`; it ignores the third row (pen-tip
force). It preserves source point order and does no whole-character or
future-point normalization. The declared 256-point cap exceeds the observed
maximum of 205, so no selected record is truncated.

## Split recipe and membership

Version `luna25-v1` uses seed `20261003` but does not use a language/library
RNG. Within each class, records are ranked by the SHA-256 digest of the UTF-8
bytes of:

```text
luna25-v1\0{seed}\0{class_label}\0{example_id}
```

Ties are broken by `example_id`. The first eight ranked records are selected;
ranks 0–3 go to train, 4–5 to validation, and 6–7 to test. IDs use the source
filename and zero-based `mixout` index. Each class contributes exactly 4/2/2
records, giving 80 train, 40 validation, and 40 test examples. The complete
membership, source indices, class codes, and within-class ranks are in
[`split_manifest.json`](../../artifacts/luna-25-uci-character-trajectories/split_manifest.json),
whose canonical JSON SHA-256 (UTF-8, sorted keys, compact separators, ASCII
escaping, no trailing newline) is
`79248deaa64b9b0f6143e5abc52beb01a46448434607bd920a1c0574d3557d80`.

## Execution and label boundary

Execution uses the existing `ExperimentRunner` sequential CPU
`EXCURSION_V1` path. Each repetition creates a fresh `ExperimentRunner`, trains
on the train partition, then evaluates validation and test without updating
the learned readout. Per-character queue, predictor, credit, and settling
state follow the existing runtime reset boundary; the train-learned model and
readout are retained for validation/test evaluation.

The input stream interval is 0.005 logical seconds, timestamps reset per
character, and source order is preserved. The adapter retains labels only on
the outer `SyntheticExample` used by train/evaluation and post-readout reward
or prototype orchestration. Labels are not placed in `StrokePoint`, neural
event payloads, prediction observations, or topology. The focused boundary
test instruments `admit_external_batch` and verifies three successive
singleton admissions at 0, 0.005, and 0.01 seconds with only the corresponding
current scalar (3, 7, and 11); the input event trace contains no label.
Unseen points are not submitted in advance.

The full experiment and `E1Config` settings are retained in
[`run_manifest.json`](../../artifacts/luna-25-uci-character-trajectories/run_manifest.json).
Important bounds and settings:

| Setting | Value |
|---|---:|
| Model / epochs / seed | `EXCURSION_V1` / 3 / 20261003 |
| Max points per character | 256 |
| Shared queue / event budget per character | 512 / 4,096 |
| E1/E2 neuron event budget / provenance capacity | 8,192 / 16 |
| Settling horizon | 10 logical seconds |
| Prediction capacity / expiry | 8 / 4 logical seconds |
| Topology | 80 nodes, 1 initial edge, edge capacity 8, fan-in/out 2 |
| Reward | dense, +1 correct / -1 incorrect, zero delay |
| Structural plasticity | disabled; fixed topology |
| Activity energy units | proxy units, not joules |

All scalar neuron thresholds/delays and bounds, experiment parameters, class
mapping, split counts, software versions, commands, and replay digests are
machine-readable in the run manifest. Derived runtime defaults are retained
there as well: classifier activity capacity 4,096; eligibility capacity 640
traces per neuron, 4-second decay, trace/credit limits 1, and 64 retained
reward identities; energy-meter counter cap 32,768 and energy cap 1,000,000;
net utility, weight 1, threshold 0, epsilon `1e-9`, and 1,024 message cap.

## Results

All three partitions completed settling. There were no budget exhaustions,
incomplete characters, pending events, beyond-deadline events, or truncated
provenance. The train row below is post-training resubstitution evaluation;
epoch-by-epoch training metrics are also retained in the run manifest.

| Split | N | Accuracy | Macro precision | Macro recall | Macro F1 |
|---|---:|---:|---:|---:|---:|
| Train, post-training | 80 | 0.150 | 0.0851 | 0.1500 | 0.0727 |
| Validation | 40 | 0.125 | 0.0270 | 0.1250 | 0.0428 |
| Test | 40 | 0.175 | 0.0998 | 0.1750 | 0.0989 |

No accuracy threshold is asserted. Validation accuracy (0.125) and test
accuracy (0.175) happen to equal the previously reported Luna-22 aggregate
accuracies; aggregate equality does not identify sample membership or
preprocessing and is **not** evidence of historical-run reproduction.
Per-class counts and accuracy:

| Class | Train correct / 4 (accuracy) | Validation correct / 2 (accuracy) | Test correct / 2 (accuracy) |
|---|---:|---:|---:|
| a | 4/4 (1.00) | 2/2 (1.00) | 2/2 (1.00) |
| b | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| c | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| d | 4/4 (1.00) | 2/2 (1.00) | 2/2 (1.00) |
| e | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| g | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| h | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| l | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| m | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| n | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| o | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| p | 3/4 (0.75) | 1/2 (0.50) | 1/2 (0.50) |
| q | 1/4 (0.25) | 0/2 (0.00) | 0/2 (0.00) |
| r | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| s | 0/4 (0.00) | 0/2 (0.00) | 1/2 (0.50) |
| u | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| v | 0/4 (0.00) | 0/2 (0.00) | 1/2 (0.50) |
| w | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| y | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |
| z | 0/4 (0.00) | 0/2 (0.00) | 0/2 (0.00) |

Confusion matrices, per-class precision/recall/F1, and per-example predictions
are in [`per_class_report.json`](../../artifacts/luna-25-uci-character-trajectories/per_class_report.json).

| Measure | Train | Validation | Test |
|---|---:|---:|---:|
| Prediction target observations (admitted input points) | 13,724 | 6,862 | 6,862 |
| Matched / unmatched target observations | 0 / 13,724 | 0 / 6,862 | 0 / 6,862 |
| Expired predictions / prediction errors | 138 / 0 | 67 / 0 | 63 / 0 |
| Prediction loss | 0 | 0 | 0 |
| Matched / unmatched delayed credit | 0 / 1 | 0 / 1 | 0 / 1 |
| Processed events | 25,353 | 12,670 | 12,400 |
| Emissions / silent events | 138 / 25,215 | 67 / 12,603 | 63 / 12,337 |
| Peak queue / capacity | 189 / 512 | 188 / 512 | 187 / 512 |
| Peak queue utilization | 36.9% | 36.7% | 36.5% |
| Connections / configured capacity | 1 / 8 | 1 / 8 | 1 / 8 |
| Fan-in / fan-out utilization | 0.00625 / 0.00625 | 0.00625 / 0.00625 | 0.00625 / 0.00625 |

Energy component totals (activity-cost proxy units; **not joules or calibrated
physical energy**):

| Split | Event processing | Emitted amplitude | Edge transfer | Prediction error | Total |
|---|---:|---:|---:|---:|---:|
| Train | 25,353.0000 | 96.2244 | 1.1200 | 0 | 25,450.3444 |
| Validation | 12,670.0000 | 47.2421 | 1.1200 | 0 | 12,718.3620 |
| Test | 12,400.0000 | 44.5256 | 0.7051 | 0 | 12,445.2308 |

Training history has 80 updates per epoch (240 cumulative after epoch 3);
epoch accuracies were `0.1625`, `0.1500`, and `0.1625`, with rewards `-54`,
`-56`, and `-54`. No prediction matched an observed target and no prediction error was
generated: **predictive efficacy is not established**. Runtime credit
accounting executed, but no delayed-credit outcome matched: useful
delayed-credit learning is not demonstrated.

## Reproduction and validation

Portable Windows PowerShell reproduction:

```powershell
$root = Join-Path $env:TEMP 'luna25-uci-c58g7v'
New-Item -ItemType Directory -Force $root | Out-Null
$archive = Join-Path $root 'character-trajectories.zip'
Invoke-WebRequest -Uri 'https://archive.ics.uci.edu/static/public/175/character+trajectories.zip' -OutFile $archive
(Get-FileHash $archive -Algorithm SHA256).Hash
Expand-Archive -LiteralPath $archive -DestinationPath $root -Force
$data = Join-Path $root 'mixoutALL_shifted.mat'
(Get-FileHash $data -Algorithm SHA256).Hash
python -m scripts.benchmark_uci_character_trajectories --data $data --output-dir artifacts\luna-25-uci-character-trajectories --repetitions 2
```

Expected archive and source hashes are listed above. The actual invocation,
with resolved interpreter/data/output paths, is recorded verbatim in
`run_manifest.json`.

Two repetitions created fresh runner state on the identical `luna25-v1` split
and configuration. Both stable-output digests were
`236835bf31c001ff520ef9389674e969435c63fb7038fd6f0797292cdefa69cc`; both
training replay digests were
`441184878990df3a61fba67b72ea996b917650e19166cd2d0360e1c909ca39b6`.
The manifest reports `repeated_run_stable_outputs_match: true`.

The separately run Luna-25 focused test command passed **7 tests**:

```powershell
python -m pytest -q tests\test_uci_character_trajectories_benchmark.py
```

The separately run prescribed ACP-0006 regression command passed **334 tests**:

```powershell
python -m pytest -q tests\test_experiments.py tests\test_excursion_neuron.py tests\test_e2_multi_excursion.py tests\test_event_runtime.py tests\test_topology.py tests\test_predictive_coding.py tests\test_eligibility.py tests\test_streaming_classifier.py tests\test_energy_utility.py tests\test_ir2.py tests\test_e2_ir2.py tests\test_stroke_dataset.py tests\test_excursion_integration.py
```

Combined, these were **341 passed**. `git diff --check` reported no tracked
whitespace errors, and a trailing-whitespace scan of all six new deliverables
found none; test execution and JSON parsing validated the source and reports.
The command `python -m compileall -q scripts tests` passed, and the editor
Problems check found no errors in the new Python files. Direct Pylance
diagnostics could not be queried because its MCP endpoint returned a
transport error.

Full CPU suite status: **NOT RERUN DURING LUNA-25 IMPLEMENTATION/PUBLICATION**.
The latest Luna-0
independent review recorded the existing unrelated baseline as **24 failed,
789 passed, 1 skipped** (`python -m pytest -q -rs`, 814 collected), with the
known downstream failure groups in CPU visualization, Luna-12B/12E/12L,
spiral benchmark, temporal analysis, and 3D viewer tests. None was repaired or
changed here.

## Limitations and disposition

- This is a small stratified subset of 2,858 examples, not a full-dataset,
  writer-disjoint, or statistical-efficacy claim.
- The old Luna-22 split cannot be reconstructed, so `luna25-v1` is a new
  baseline, not an old-run reproduction.
- Prediction matches and prediction errors were zero; predictive efficacy is
  not established. Runtime credit accounting executed, but delayed credit had
  no matched outcome and useful delayed-credit learning is not demonstrated.
- Energy is reported only in activity-cost proxy units; it is not joules or
  calibrated physical energy. No accuracy threshold is claimed.
- Full-suite failures remain as previously classified; Pylance diagnostics
  were unavailable during this task.
- Return this evidence to Luna-0 for independent review. Do not claim Luna-22
  closure or downstream integration readiness.
