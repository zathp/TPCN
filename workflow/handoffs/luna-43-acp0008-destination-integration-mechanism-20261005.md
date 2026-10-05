# Luna-43 — ACP-0008 Destination Integration Mechanism

```yaml
tpcn_handoff:
  agent: "Luna-43"
  luna_identifier: "Luna-43"
  descriptive_name: "ACP-0008 destination integration mechanism comparison"
  task_id: "luna-43-acp0008-destination-integration-mechanism-20261005"
  component: "Fixed-topology downstream destination integration"
  status: "BLOCKED — exact historical Phase-B input fixture digest mismatch"
  contract_version: "1.0"
  branch: "copilot/execute-luna-43-cycle"
  authorization_revision: "f304e96f994d5b3f7842589c1b505d09c8fae4c6"
  execution_revision: "50aaa074929d6dfe506689c80c306d7e54be32f2"
  execution_repo_revision: "50aaa074929d6dfe506689c80c306d7e54be32f2"
  owner: "Project owner"
  classification:
    - "bounded CPU software-reference mechanism experiment"
    - "stopped at predeclared historical fixture gate"
    - "no destination-condition outcome or efficacy conclusion"
    - "no production, ACP, architecture, or governance change"
  files_changed:
    - "run_luna43_acp0008_destination_integration_mechanism.py"
    - "tests/test_luna43_acp0008_destination_integration_mechanism.py"
    - "artifacts/luna43-acp0008-destination-integration-mechanism/config.json"
    - "artifacts/luna43-acp0008-destination-integration-mechanism/results.json"
    - "artifacts/luna43-acp0008-destination-integration-mechanism/summary.json"
    - "artifacts/luna43-acp0008-destination-integration-mechanism/replay.json"
    - "workflow/handoffs/luna-43-acp0008-destination-integration-mechanism-20261005.md"
  runner_commit: "50aaa074929d6dfe506689c80c306d7e54be32f2"
  runner_sha256: "f3bdc0288ded146e592587e1849329093f2a0d1702e69956447b4b5862842e5b"
  config_identity: "TPCN-LUNA43-ACP0008-DESTINATION-INTEGRATION-1"
  config_digest: "648db5a29a741332a96304c345a8588b0f7df27aed1e7b474f7527ab868cee59"
  aggregate_run_digest: "365cbede264098af8d57d3ac3a79eed978b1fac866ebe67eae73a316eac56354"
  environment:
    python: "3.12.3"
    platform: "Linux-6.17.0-1022-azure-x86_64-with-glibc2.39"
    pytest: "9.1.1"
  tests_passing:
    - "Luna-43 focused: 4 passed"
    - "Relevant neuron/integration/runtime/routing/topology and Luna-38–42 selection: 217 passed"
    - "Full suite: 1023 passed"
    - "Python compile/import and git diff --check"
    - "CodeQL: 0 alerts"
  tests_failed:
    - "Four known Luna-41/Luna-42 decimal-0.4 exact-float assertions; same failures recorded at authorization baseline"
  tests_skipped:
    - "tests/test_gpu_visualization.py:61 — CUDA unavailable"
  tests_not_run:
    - "Whole-experiment replay — correctly not started after the historical fixture gate stopped the first arm"
    - "ACP-0007 precursor scan — not run; the experiment did not reach the condition-complete emission prerequisite"
    - "Hardware equivalence, task efficacy, classification, and energy benefit — out of scope"
  recommended_next_agent:
    - "Return the fixture/provenance blocker to Luna-0 for independent review; no successor is authorized"
```

## Authorization, exact execution boundary, and frozen configuration

The initial checkout was clean at `HEAD == @{u} ==`
`f304e96f994d5b3f7842589c1b505d09c8fae4c6`, on
`copilot/execute-luna-43-cycle`, with `origin/main` at
`b6ca4a67783bf37ded146944f8dc9afaf5277f11`. I read the active Luna-43
contract and authorization, the superseded test-policy handoff, ACP-0007,
ACP-0008, the Luna-40/41/42 execution and review handoffs, and the raw Luna-42
Phase-B evidence. The earlier test-only authorization was explicitly
superseded before execution. Its Luna-41/Luna-42 assertions were left untouched.

The runner and focused tests were published first in commit
`50aaa074929d6dfe506689c80c306d7e54be32f2`. Immediately before the retained
execution, the worktree was clean and `HEAD == @{u}` at that exact runner
commit. `origin/main` still matched the authorized baseline. The runner itself
records both `execution_revision` and `execution_repo_revision` as that commit;
launch status was empty. No runner or test source was edited after the retained
attempt. The later changes are only retained artifacts and this execution
handoff.

The full frozen configuration is in `config.json`, and is repeated in all
primary JSON artifacts. The fixed configuration was:

| Item | Frozen value |
|---|---|
| Stream | Luna-39/Luna-34 training point sequences, seeds 0–4, 64 characters per seed; ordered points/timestamps only; input `x+y`; same-time batches preserved |
| Nodes / topology | `source`, `relay`, `destination`; only `source -> relay -> destination`; edge delay 1.0, `w=1.0`, `d=1.0`, `r=0.0`; fan-in/out 2; edge/routing capacities 3 |
| Source | `integration=None` |
| Relay | ACP-0008 enabled with `decay_rate_z=0.0125` in every condition |
| Destination conditions | actual `integration=None`; `IntegrationConfig()` (`0.1`); `IntegrationConfig(decay_rate_z=0.0125)` |
| Other ACP-0008 settings | input gain 1.0, discharge quantum/`theta_Z` 1.0, `z_max=4.0`; fast decay 1.0 |
| Full E1 settings | `a_min=.25`, `a_max=1`, `delta_x_e=1`, emission delay `.5`, `event_budget=4096`, `m_emit_delay=1`, `m_rearm_delay=1`, provenance capacity 16, `theta_e=1`, `theta_hold=1.5`, `theta_m=4`, `theta_r=.25`, `x_max=8` |
| Runtime | queue 128; event/activity budgets 1024; settling horizon 4; prediction capacity 8 / expiry 4; eligibility capacity 1024 per ledger; neutral reward |
| Structural behavior | growth, candidate creation, admission, pruning, and topology mutation disabled |
| Historical reference | raw Luna-42 calibrated-relay arm, execution revision `d073ecc13e789105c611181992ce4c8d48c79030`; numeric equation values reconciled with the predeclared `64 * epsilon * max(1, |observed|, |expected|)` rule |

No source, relay, stream, edge, integration, threshold, or resource parameter
was changed to force acceptance. The runner hash, config digest, authorization
revision, execution revision, complete configuration, and environment identity
are recorded in `config.json`, `results.json`, `summary.json`, and `replay.json`.

## Retained execution and stop condition

The experiment stopped **BLOCKED** on its first attempted character:
`DESTINATION_DISABLED`, seed 0, sequence index 0 (`c00-000`). The first
historical gate check found that the current generated input digest differs
from the exact Luna-42 retained input digest:

```text
Luna-43 generated: 176897def09943a3d8276104d562c80b02982c806f2672e8a1c2b484a8921a1d
Luna-42 retained:  e196be616cdd0abe616a82044265dcad3905ea5dc7d2b6c51c207556c4f855e4
```

Both records contain 12 one-point batches. Exactly one point value differs:
at batch 3 / point 0, timestamp `81.33339605974454`, the generated value is
`-0.1646535199398629` while the retained value is `-0.16465351993986282`, an
absolute difference of `8.326672684688674e-17`. This is a cross-environment
binary64 stream discrepancy. The input digest check was predeclared exact, so
the fixture gate failed; it was not relaxed. The raw input batches, runtime
trace, route, emissions, neuron states, eligibility ledgers, and failed
reconciliation are retained in `results.json`.

For that one completed character, the relay/source provenance, source emission,
and `source -> relay` route checks matched the historical record; source
emissions/transfers were 1/1. Relay emissions and relay-to-destination
transfers/receptions were 0/0/0; destination emissions were 0. The queue peak
was 2/128, 15 runtime events were processed against budget 1024, all three
eligibility ledgers reconciled with peak occupancy at most 1/1024, and no
route-root truncation occurred. Prediction capacity was 8; the runtime exposes
expired predictions but not peak pending occupancy (0 expired here).

**No other character or destination condition was executed.** The aggregate
Luna-42 relay gate, complete three-condition input pairing, whole-experiment
replay, and ACP-0007 precursor scan were therefore not run. The replay artifact
records both digests as null with `not_run_after_blocker=true`; there is no
whole-run zero-emission claim, candidate opportunity, or scientific negative
result. The observed zero destination receptions/emissions apply only to
`c00-000`. Do not resume this run by modifying the source or rerunning it under
this retained result; return the fixture/provenance blocker to Luna-0.

## Raw retained artifact identities

All four artifacts have non-null provenance and share aggregate run digest
`365cbede264098af8d57d3ac3a79eed978b1fac866ebe67eae73a316eac56354`.
The hashes below are SHA-256 of the files as retained.

| Artifact | File SHA-256 | Internal `artifact_digest` |
|---|---|---|
| `config.json` | `0b97f064422cbdee531b6d7bc7732a3571a821798321333c4e26ee63913347f2` | `49115b4df94a8aec288e2410452aa4c0be92369667051a85d6438127d234bd4d` |
| `results.json` | `b5c655abe2a653ab32a3d66c569574b5dedbe6f05af851e7678866e4ab513e26` | `a9665bcf19616eed7762f1865cf9d51131ffb4b593e888e87844665f4dd1e407` |
| `summary.json` | `424da866201cece9b5f242702405c8940b046aa2b6d5d981d2c4538ff8031e9a` | `34975a156292cb0483b956fe6830f93b290b058591c832175aca4b2a529a0107` |
| `replay.json` | `a3d6d9648605ab4be4abd9b4c33e714982b2e12c292c8b46e68c15cac3605f1d` | `8510aaead645251dd5f0b272c22fdd49c5508b2b6ddfe5d79d25a5f73fcf2b02` |

## Validation and limitations

Commands and outcomes:

```text
python -m pytest -q tests/test_luna43_acp0008_destination_integration_mechanism.py
  4 passed

python -m pytest -q tests/test_excursion_neuron.py tests/test_excursion_integration.py
  tests/test_e2_multi_excursion.py tests/test_topology.py tests/test_event_runtime.py
  tests/test_luna38_excursion_integration_state.py
  tests/test_luna39_acp0008_propagation_emission_diagnostic.py
  tests/test_luna41_acp0008_temporal_calibration.py
  tests/test_luna42_acp0008_corrective_calibration.py
  217 passed, 4 failed

python -m pytest -q -rs
  1023 passed, 4 failed, 1 skipped; 1028 collected

python -m py_compile run_luna43_acp0008_destination_integration_mechanism.py
  tests/test_luna43_acp0008_destination_integration_mechanism.py
git diff --check
  passed
```

The four failures are the known exact comparisons in the Luna-41/Luna-42 tests:
computed `0.39999999999999997` is compared with literal `0.4`. The authorization
baseline explicitly recorded the same four failures. They were not changed
because the active Luna-43 contract superseded the earlier test-only assignment
before execution. The sole full-suite skip is the pre-existing CUDA-unavailable
GPU visualization test. CodeQL reported zero alerts. The parallel code-review
validation returned no comments but also reported its review service was
unavailable; no independent code review is claimed.

This handoff records a **fixture-gate blocker**, not integration readiness,
mechanism support, or a valid negative destination result. ACP-0008 remains
experimental, opt-in, and unpromoted; ACP-0007 remains disabled and unchanged.
No Luna-44 work or authorization is included.
