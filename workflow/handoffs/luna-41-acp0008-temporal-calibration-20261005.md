# Luna-41 — ACP-0008 Temporal Calibration Execution

```yaml
tpcn_handoff:
  agent: Luna-41
  luna_identifier: "Luna-41"
  descriptive_name: "ACP-0008 Temporal Calibration"
  task_id: "Luna-41"
  component: "Bounded ACP-0008 software-reference calibration"
  status: "blocked"
  contract_version: "1.0"
  branch: "main"
  base_revision: "714cad5a7eea55af4cd8529b0244a8c5723e2fd7"
  execution_revision: "See commit containing this handoff and its owned evidence."
  dependencies:
    - "Luna-0 authorization: workflow/handoffs/luna-0-acp0008-calibration-decision-20261005.md"
    - "Accepted experimental ACP-0008"
    - "Luna-38/39 mechanism contracts and reviews"
    - "Luna-40 effective-routed-drive execution and independent review"
  owner: "Luna-0"
  classification:
    - "bounded configuration-calibration experiment"
    - "Phase-A blocked"
    - "no candidate selected"
    - "no ACP or architecture change"
  hypothesis: "A predeclared decay_rate_z candidate yields one normalized, integration-mediated relay emission for three near-spaced 0.4 routed inputs, while all declared controls remain silent."
  outcome: "No candidate selected: repeated source events yielded Model-B payloads measurably above the declared 0.4 target."
  authorized_scope:
    - "Execute all four fixed Phase-A decay candidates and six declared fixtures."
    - "Replay Phase A from reset and compare serialized records and digests."
    - "Run Phase B only after all Phase-A criteria pass and the selected configuration is frozen."
    - "Modify only the runner, focused tests, Luna-41 artifacts, and this handoff."
  completed_scope:
    - "All four candidates and six fixtures executed through public neuron, event queue, and BoundedTopology APIs."
    - "Phase-A replay completed with identical aggregate digest."
    - "Phase B was not started because Phase A selected no candidate."
  architecture_invariants_touched: []
  architecture_change: false
  acp_change: false
  acp0007_enabled: false
  acp0008_status: "experimental, opt-in, and unpromoted"
  files_changed:
    - "run_luna41_acp0008_temporal_calibration.py"
    - "tests/test_luna41_acp0008_temporal_calibration.py"
    - "artifacts/luna41-acp0008-temporal-calibration/config.json"
    - "artifacts/luna41-acp0008-temporal-calibration/phase_a_freeze.json"
    - "artifacts/luna41-acp0008-temporal-calibration/results.json"
    - "artifacts/luna41-acp0008-temporal-calibration/summary.json"
    - "workflow/handoffs/luna-41-acp0008-temporal-calibration-20261005.md"
  tests_passing:
    - "Luna-41 focused tests: 6 passed."
    - "Full repository suite: 1015 passed, 1 skipped."
    - "git diff --check."
  tests_failed: []
  tests_not_run:
    - "Phase-B temporal stream characterization; its Phase-A prerequisite failed."
  integration_readiness: "Not ready for Phase B. Return the payload mismatch and evidence to Luna-0 for independent review and disposition."
  recommended_next_agent:
    - "Luna-0 for independent review; do not tune or extend this experiment without new authorization."
```

## Baseline and execution environment

The authorization baseline was fetched and verified before execution:
branch `main`, clean index and worktree, and
`HEAD == origin/main == 714cad5a7eea55af4cd8529b0244a8c5723e2fd7`.
The experiment used Python 3.11.5 from `.venv\Scripts\python.exe` on
Windows. No production module, ACP, architecture contract, shared governance
document, or prior Luna evidence was changed.

Commands:

```powershell
.\.venv\Scripts\python.exe .\run_luna41_acp0008_temporal_calibration.py
.\.venv\Scripts\python.exe -m pytest tests\test_luna41_acp0008_temporal_calibration.py -q
.\.venv\Scripts\python.exe -m pytest -q
git diff --check
```

The run used only the fixed candidate order
`0.1, 0.05, 0.025, 0.0125`, with `theta_E=1.0`, `theta_Z=1.0`,
`input_gain=1.0`, `z_max=4.0`, fast `decay_rate=1.0`, and ACP-0007
disabled. Phase-A queue and event limits remained 64; each neuron event
budget remained 64. No parameter, stimulus, interval, amplitude, or resource
limit was changed.

## Phase-A outcome

**BLOCKED — no candidate was selected.** The runner executed 24
candidate/fixture records (four candidates by six fixtures) and replayed
Phase A from reset. The initial and replay digests matched:

`fcbea9694a19ce407544c6394cb51432a64ff59d39437e834abc193aff4f9cd2`

For isolated inputs and all far triples, the source-to-relay transfers
matched the expected signed `0.4` payload, recurrence checks matched the
production trace, and the relay remained silent. The corrected neutral probe
was issued strictly more than `10 * tau_z` after the final input/discharge;
every enabled fixture returned to `|z| < 1e-4` without an emission.

Near-spaced source inputs did not each produce the declared normalized
payload. The first routed payload was `0.4`; subsequent measured payloads
were `0.4000008889685561` and `0.4000008889707768` (negative mirror:
`-0.4000008889685561` and `-0.4000008889707768`). The maximum absolute
deviation was `8.889707767689714e-7`, above the runner's `1e-12` numerical
tolerance. This is a state-dependent deviation, not floating-point
round-off: the production source neuron retains fast state between the
predeclared inputs, changing its later canonical-emission amplitude. The
contract specifies a `0.4` routed payload but does not define a looser
tolerance; no tolerance was broadened to accept the observed dynamics.

At `decay_rate_z=0.0125`, the near positive and negative triples each
produced exactly one integration-mediated relay emission with payloads
`+0.350000472048906` and `-0.350000472048906`. Production trace
classification, polarity, and the ordinary emission-amplitude rule matched.
These observed emissions do not validate the normalized fixture because its
input payload criterion failed. The positive and negative near triples,
near pairs, and integration-disabled near-triple controls therefore failed
candidate acceptance on the same source-payload mismatch. This outcome is
not evidence for a calibrated candidate.

The recorded Phase-A resource maxima were 15 processed events per fixture,
queue peak 4, 9 source events, and 6 relay events, within the fixed limits.
All recorded state bounds, ACP-0008 recurrence checks, and neutral-return
checks passed after correcting the probe timestamp to the next representable
float above the exact `10 * tau_z` boundary.

The runner's payload tolerance and the contract's unspecified numerical
tolerance are explicitly reported for independent review. The measured
residual-state deviation is several orders of magnitude larger than the
applied tolerance, so this does not change the terminal decision.

## Phase-B gate

**NOT RUN.** Phase A did not select a candidate, so no Phase-B stream was
generated or consumed. The Phase-A freeze artifact records a null selection
and the Phase-B prerequisite failure. There are no Phase-B arms, stream
outcomes, event high-water marks, or replay digest to report.

## Status by requirement

| Status | Evidence |
|---|---|
| Passed | Exact authorized baseline, candidate set, fixed parameters, and all six Phase-A fixtures executed. |
| Passed | Isolated/far fixture acceptance; ACP-0008 production-trace recurrence; bounded state; neutral decay probe; no direct relay emissions. |
| Passed | Phase-A deterministic replay; initial and replay digest identical. |
| Failed | Every near-payload fixture requiring repeated source emissions exceeded the `0.4` target by up to `8.889707767689714e-7`. |
| Failed | No candidate satisfied every Phase-A fixture; selection is `null`. |
| Not run | Phase B and its deterministic replay; correctly gated by failed Phase A. |
| Not applicable | Accuracy/efficacy, task optimization, energy benefit, structural-growth benefit, hardware equivalence, biological realism, or architecture promotion. |

## Evidence and digests

Artifacts are under
`artifacts/luna41-acp0008-temporal-calibration/`:

| File | SHA-256 |
|---|---|
| `config.json` | `8128e16c7c67ca0d7db2425433d7421f7bf19d3940730cd6001a28b7c133b6be` |
| `phase_a_freeze.json` | `1064ec6c90f72e681783f9636d5bbffa7432678e698d0e96c1dea06be5c8b353` |
| `results.json` | `cff0cf66fe02452768e436cd779b1796c3cfa2f512f7f29d31229c2a35ce7015` |
| `summary.json` | `89c856a762cc2d85dd5d285799d6c81fd901dddfd720efba7b0daf3b11110010` |

The summary's `results_digest` is
`be6791cad0dd6f869115ba7d11ad18c5a36b9aa842e2fa9a1597c49e2074643d`.
The detailed JSON artifacts retain all candidate/fixture event traces,
validation outcomes, fatal criteria, fixed configuration, and replay
digests.

## Validation and disposition

Focused Luna-41 tests passed: **6 passed**. The full repository suite passed:
**1015 passed, 1 skipped**. `git diff --check` passed.

**Integration readiness: not ready for Phase B.** Return the complete result
and source-payload mismatch to Luna-0 for independent review. Do not extend
the candidate set, change the fixture, broaden the tolerance, or run Phase B
unless new authorization explicitly resolves this blocker. ACP-0008 remains
experimental, opt-in, and unpromoted regardless of this outcome.
