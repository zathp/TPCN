# Luna-42 — ACP-0008 Corrective Calibration Replication

```yaml
tpcn_handoff:
  agent: Luna-42
  luna_identifier: "Luna-42"
  descriptive_name: "ACP-0008 Corrective Calibration Replication"
  task_id: "Luna-42"
  component: "Bounded ACP-0008 corrective calibration with production-derived routed inputs"
  status: "completed"
  contract_version: "1.0"
  branch: "main"
  authorization_revision: "db4774a60cd849a016a2d249c8c0bc3432b834d9"
  execution_revision: "d073ecc13e789105c611181992ce4c8d48c79030"
  dependencies:
    - "Luna-0 corrective authorization: [luna-0-acp0008-corrective-calibration-decision-20261005.md](./luna-0-acp0008-corrective-calibration-decision-20261005.md)"
    - "Luna-41 execution: [luna-41-acp0008-temporal-calibration-20261005.md](./luna-41-acp0008-temporal-calibration-20261005.md)"
    - "Luna-0 post-Luna-41 review: [luna-0-independent-review-luna41-acp0008-temporal-calibration-20261005.md](./luna-0-independent-review-luna41-acp0008-temporal-calibration-20261005.md)"
    - "Accepted experimental ACP-0008"
  owner: "Luna-0"
  classification:
    - "corrective replication"
    - "bounded calibration"
    - "production-derived routed stimulus"
    - "ACP-0007 disabled"
    - "Phase A selected one predeclared candidate"
    - "Phase B descriptive replay passed"
  architecture_change: false
  acp_change: false
  acp0007_enabled: false
  acp0008_status: "experimental, opt-in, and unpromoted"
  files_changed:
    - "run_luna42_acp0008_corrective_calibration.py"
    - "tests/test_luna42_acp0008_corrective_calibration.py"
    - "artifacts/luna42-acp0008-corrective-calibration/config.json"
    - "artifacts/luna42-acp0008-corrective-calibration/phase_a_freeze.json"
    - "artifacts/luna42-acp0008-corrective-calibration/results.json"
    - "artifacts/luna42-acp0008-corrective-calibration/summary.json"
    - "workflow/handoffs/luna-42-acp0008-corrective-calibration-20261005.md"
  tests_passing:
    - "Focused Luna-42 tests: 8 passed."
    - "Full repository suite: 1023 passed, 1 skipped."
    - "git diff --check."
  tests_failed: []
  tests_not_run: []
  integration_readiness: "Return to Luna-0 for independent post-Luna-42 review. No successor authorized here."
  recommended_next_agent:
    - "Luna-0 for independent review only."
```

## Baseline, execution provenance, and corrective scope

Luna-42 started from the exact authorized governance revision
`db4774a60cd849a016a2d249c8c0bc3432b834d9`, implemented only its owned
runner/tests, published that runner, corrected one Phase-B bookkeeping bug in
the published runner, and then executed from the synchronized clean runner
revision `d073ecc13e789105c611181992ce4c8d48c79030` with
`HEAD == origin/main` and an empty porcelain status at startup.

The retained execution provenance in every primary JSON artifact records:

- execution revision: `d073ecc13e789105c611181992ce4c8d48c79030`
- runner SHA-256:
  `dd36a2be784921b5b774f1da199b8ba60fcce4a5d8124c79ba1f3d4843a1a376`
- frozen configuration digest:
  `e6c17c12f56e5661aef99215ef41bbc82c1d61f617600fb08c7f98504addafad`
- aggregate run digest:
  `f903a6ca5f3f454ce66a793bfdfec707ca131bcb049d2c696b1892e430e3e339`
- Python:
  `3.11.5 (tags/v3.11.5:cce6ba9, Aug 24 2023, 14:38:34) [MSC v.1936 64 bit (AMD64)]`
- platform: `Windows-10-10.0.19045-SP0`
- `sys.float_info.epsilon`: `2.220446049250313e-16`

Luna-42 preserved the Luna-41 candidate set and all fixed parameters. The
only scientific correction was the contract-authorized shift from an idealized
literal repeated routed payload of `0.4` to the actual production-derived
payloads produced by:

`declared source input -> ordinary source emission -> Model-B edge -> queued routed event -> relay reception`

No production neuron, topology, ACP, workflow, or architecture files were
changed.

## Exact and floating-point criteria

Discrete/exact criteria remained exact:

- candidate set and selected candidate
- fixture schedule and configured binary64 timestamps
- source emission, routed transfer, and relay reception counts
- one-to-one event identities
- route path and ordering
- relay emission classification
- exact routed-payload equality between the routed queue event and the matching
  relay reception
- deterministic replay digests

Floating-point equation checks used only the predeclared Luna-42 rule:

`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`

This rule was used for:

- source ordinary-emission amplitude reconstruction
- Model-B transform reconstruction
- ACP-0008 recurrence/oracle checks
- relay ordinary-emission amplitude reconstruction
- neutral-state bound check

No hidden or adaptive tolerance was introduced.

## Phase A — causal production-derived calibration

### Pre-execution ideal-input hypothesis

The retained frozen configuration preserved the prior idealized hypothesis:
only `decay_rate_z = 0.0125` was expected to cross threshold on the three-input
near triple if the routed input repeated at the idealized `0.4` amplitude.
This hypothesis was retained only as a pre-execution reference and did not
select the candidate.

### Observed production-derived routed payloads

The actual routed payloads retained for the selected candidate `0.0125` were:

| Fixture | Routed payloads |
|---|---|
| ISOLATED | `0.4` |
| NEAR_PAIR | `0.4`, `0.4000008889685561` |
| NEAR_TRIPLE | `0.4`, `0.4000008889685561`, `0.4000008889707768` |
| FAR_TRIPLE | `0.4`, `0.4`, `0.4` |
| NEGATIVE_NEAR_TRIPLE | `-0.4`, `-0.4000008889685561`, `-0.4000008889707768` |
| INTEGRATION_DISABLED | `0.4`, `0.4000008889685561`, `0.4000008889707768` |

Every routed transfer reconciled one-to-one with its source canonical emission,
and every routed payload matched the matching relay reception payload exactly.

### Analytic/oracle reconstruction and residuals

For every enabled fixture, the oracle was recomputed from the observed routed
payloads and the actual relay-arrival timestamps. Across all Phase-A records,
the maximum absolute recurrence residuals were:

- `z_after_decay`: `1.2705494208814505e-21`
- `z_after_input`: `1.2705494208814505e-21`
- `discharge_amount`: `0.0`
- `z_post_discharge`: `1.2705494208814505e-21`

These values stayed far below the declared binary64 tolerance rule and matched
the prior Luna-41 numerical picture while now respecting the corrected causal
stimulus definition.

### Phase-A outcome table

| Candidate | ISOLATED | NEAR_PAIR | NEAR_TRIPLE | FAR_TRIPLE | NEGATIVE_NEAR_TRIPLE | INTEGRATION_DISABLED | Passed |
|---|---:|---:|---:|---:|---:|---:|---:|
| `0.1` | pass | pass | fail | pass | fail | pass | no |
| `0.05` | pass | pass | fail | pass | fail | pass | no |
| `0.025` | pass | pass | fail | pass | fail | pass | no |
| `0.0125` | pass | pass | pass | pass | pass | pass | yes |

The fixed selection rule chose the **largest** passing candidate. Only
`0.0125` passed every fixture, so the selected candidate is:

`decay_rate_z = 0.0125`

For the selected candidate:

- NEAR_TRIPLE produced exactly one positive integration-mediated relay
  emission with payload `0.350000472048906`
- NEGATIVE_NEAR_TRIPLE produced exactly one negative integration-mediated
  relay emission with payload `-0.350000472048906`
- NEAR_PAIR produced no relay emission
- FAR_TRIPLE produced no relay emission
- INTEGRATION_DISABLED produced no relay slow-state trace and no relay
  emission

The selected candidate’s actual-input oracle predicted threshold crossing for
the positive and negative near triples and did not predict crossing for the
isolated, near-pair, far-triple, or disabled controls; production matched
those predictions exactly.

## Freeze and gated Phase B

The Phase-A freeze was written to
[phase_a_freeze.json](../../artifacts/luna42-acp0008-corrective-calibration/phase_a_freeze.json)
before any Phase-B stream generation and round-tripped canonically before
Phase-B execution. Its artifact digest is:

`0707d5931b9fdbe141496a4de501ac9c9fc9bd5b332c641a76a862bb73592f7f`

The Phase-A replay digest was:

`5b5b34acaee7034c600dd31ccbb800acb5426bbe40822b7f77df3b3a4ce41040`

Phase B then ran only with the frozen selected candidate `0.0125` and replayed
deterministically with digest:

`4547c9b59441d4af0af6fb1de3c6c70943c9a4ae8cd7907f1b320eeb683a765d`

## Phase B — descriptive paired relay validation

Phase B remained descriptive and used the fixed paired topology
`source -> relay -> destination` with both edges fixed at `w=1`, `d=1`,
`r=0`, delay `1.0`, and ACP-0007 disabled.

Summary across five seeds and 320 characters per arm:

| Arm | Relay integrated emissions | Relay total emissions | Relay→destination transfers | Destination receptions | Max `|z|` | Queue peak | Runtime event peak |
|---|---:|---:|---:|---:|---:|---:|---:|
| CALIBRATED (`0.0125`) | 235 | 235 | 235 | 235 | `1.3692730293667474` | 3 | 107 |
| DEFAULT (`0.1`) | 0 | 0 | 0 | 0 | `0.7631640317970756` | 2 | 88 |
| DISABLED | 0 | 0 | 0 | 0 | `0.0` | 2 | 88 |

All arms preserved paired-input invariance and all recorded Phase-B causality
checks passed. No destination arm produced a canonical emission. The calibrated
arm alone generated relay integrations and onward routed transfers under the
fixed topology, which is the descriptive Phase-B outcome retained in the
artifacts.

## Artifacts and digests

Artifacts are under
[artifacts/luna42-acp0008-corrective-calibration/](../../artifacts/luna42-acp0008-corrective-calibration/):

| File | Artifact SHA-256 |
|---|---|
| [config.json](../../artifacts/luna42-acp0008-corrective-calibration/config.json) | `28060a611c866e8cd584843f962423bbc5c2404b3fc7b852884d91cb98fbf996` |
| [phase_a_freeze.json](../../artifacts/luna42-acp0008-corrective-calibration/phase_a_freeze.json) | `0707d5931b9fdbe141496a4de501ac9c9fc9bd5b332c641a76a862bb73592f7f` |
| [results.json](../../artifacts/luna42-acp0008-corrective-calibration/results.json) | `597787249549329709ec996a280631d3c609521d2fb4afaaa8b03c620ba5a595` |
| [summary.json](../../artifacts/luna42-acp0008-corrective-calibration/summary.json) | `5df95f21ec7d40f13fa3bdd0758506841117240b5e71ae8ebb938cab4a545006` |

Aggregate run digest:

`f903a6ca5f3f454ce66a793bfdfec707ca131bcb049d2c696b1892e430e3e339`

## Validation

Executed validation commands:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_luna42_acp0008_corrective_calibration.py -q
.\.venv\Scripts\python.exe .\run_luna42_acp0008_corrective_calibration.py
.\.venv\Scripts\python.exe -m pytest -q
git diff --check
```

Focused Luna-42 tests passed with `8 passed`.

The full repository suite passed with:

`1023 passed, 1 skipped`

The sole skip remained the pre-existing CUDA-unavailable skip in
`tests/test_gpu_visualization.py`.

`git diff --check` passed with no output.

## Interpretation boundary and limitations

This run supports only the bounded corrective conclusion authorized by Luna-0:

- the Luna-41 fixture/provenance defect is corrected
- existing ACP-0008 slow integration can be validly calibrated under the
  declared production-derived source/route contract
- the valid calibrated candidate in this fixed set is `0.0125`
- the fixed calibrated relay produces descriptive downstream routing activity
  in Phase B, while default and disabled controls do not

This run does **not** authorize ACP change, WEMA, ACP-0007, structural growth,
task efficacy, promotion, hardware equivalence, or any Luna-43 work.

## Return

Luna-42 execution is complete and published for independent Luna-0 review only.
