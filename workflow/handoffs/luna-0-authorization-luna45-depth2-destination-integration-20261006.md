---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-45 depth-2 destination integration mechanism authorization"
  task_id: "luna-0-authorization-luna45-depth2-destination-integration-20261006"
  component: "ACP-0008 destination integration on the frozen Luna-44 fixture, fixed two-hop route"
  status: "complete — Luna-45 AUTHORIZED / NOT EXECUTED"
  contract_version: "1.2"
  branch: "copilot/luna45-depth2-destination-integration"
  base_revision: "dbb440c763509781ee7ac5e4f2924851dde8e19c"
  result_revision: "9af6b4435ac581887f04f0951d0f7b16d7d661cd"
  authorization_revision: "9af6b4435ac581887f04f0951d0f7b16d7d661cd"
  dependencies:
    - "Explicit project-owner authorization of the Luna-45 experiment (2026-10-06)"
    - "Accepted ACP-0008; experimental, opt-in, unpromoted"
    - "Luna-42 PASS WITH FOLLOW-UP; Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED; Luna-44 evidence-quality PASS WITH FOLLOW-UP (all preserved)"
    - "Frozen committed Luna-44 fixture and pinned provenance"
  owner: "Project owner"
  classification:
    - "governance-only authorization"
    - "bounded CPU software-reference mechanism experiment"
    - "AUTHORIZED / NOT EXECUTED"
    - "no scientific outcome or architecture change"
  hypothesis: "Destination integration configuration (disabled, default 0.1, calibrated 0.0125) can change destination integration-mediated emissions under the fixed routed stream behind a frozen calibrated relay."
  counter_hypothesis: "Destination emissions are identical across arms or absent; a null or negative result is valid. Failure of reconciliation, invariance, bounds or replay is a failed gate, not a mechanism result."
  interfaces_relied_on:
    - "MultiExcursionNeuron with per-neuron ACP-0008 IntegrationConfig"
    - "ExcursionCharacterRuntime and bounded event queue"
    - "BoundedTopology and ordinary Model-B edges"
    - "Luna-44 runner reconciliation (_reconcile_route_events) and frozen fixture loader/verifier"
  label_information_boundary:
    - "Consume only ordered point x/y/t from the frozen fixture; no labels, classes, evaluation data or label-bearing metadata."
    - "Per point/arm/replay, compute float(x)+float(y) independently; do not feed the stored audit value."
    - "The fixture builder and spiral generator must not be called."
  timing_assumptions:
    - "Local event timestamps; fixed positive delay 1.0 on both edges; no global neural timestep."
  reset_boundaries:
    - "Fresh source, relay and destination state per sequence and arm; replay from reset."
  resource_bounds:
    - "Luna-44 limits: queue 128; runtime event and activity budgets 1024; neuron event budget 4096; eligibility capacity 1024 per ledger; prediction capacity 8 / expiry 4.0; settling horizon 4.0."
    - "Three nodes; fan-in/out limit 2; edge/routing capacity 3; static topology."
  authorized_scope:
    - "Consume the frozen committed fixture artifacts/luna44-canonical-fixture/fixture.json: 3,451,453 bytes; file SHA-256 66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629; semantic digest 6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305; seeds 0..4, 64 sequences per seed, 320 sequences, 5,164 ordered points; IDs c{seed:02d}-{sequence_index:03d}."
    - "Verify complete pinned provenance: artifacts/luna44-canonical-fixture/provenance.json SHA-256 6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22, Git blob eb9179abae7eed10891e6022832f16735111b220, manifest revision 86e5a2f389af06b06bf04a614edaed88e0847902, fixture revision 6413cffe6982bccc6698af6bebfae51f04e71dd9, and all recorded source paths/revisions/SHA-256 values."
    - "Topology source -> relay -> destination with existing ordinary Model-B edges, w=1, delay 1.0, d=1.0, r=0.0; no shortcut or return edge."
    - "Source integration None. Relay calibrated IntegrationConfig(decay_rate_z=0.0125), unchanged in all arms."
    - "Vary only destination integration: disabled (None), default IntegrationConfig() (decay_rate_z=0.1), calibrated IntegrationConfig(decay_rate_z=0.0125)."
    - "Historical gate on Luna-44 retained evidence/verdicts; upstream invariance across arms."
    - "Independent enqueue/reception capture for both edges, one-to-one reconciliation including exact enqueue.source == reception.source, with the retained source-only mutation regression test."
    - "Destination recurrence reconciliation; direct versus integration-mediated destination emission accounting per arm and between arms."
    - "Bounds high-water marks, completion/settling, same-environment deterministic replay; equation-derived floats use 64*sys.float_info.epsilon*max(1.0, abs(observed), abs(expected)); identities and discrete behaviour exact."
    - "Artifact provenance and retained execution: authorization revision/handoff digest, fixture digests, runner revision/hash, non-null execution revision, config digest, environment, raw captures and artifact digests in a new Luna-45 artifacts directory; retain failed arms."
    - "Own only a new Luna-45 runner, focused tests, new artifact directory and completed execution handoff; return to Luna-0 for independent review."
  unauthorized_scope:
    - "No fixture generation or regeneration; no spiral generator or builder call; no fixture/provenance edits."
    - "No parameter tuning, calibration search, topology change, or relay variation."
    - "No ACP-0007 candidate instantiation, growth or pruning."
    - "No classification/task efficacy, prediction/reward/utility/energy claim."
    - "No Windows/Linux fixture-parity work; the two known parity failures are not relaxed and do not block Luna-45."
    - "No production, ACP, architecture-contract, prior runner/test/artifact/handoff change; no promotion."
    - "No Luna-46 or other successor."
  controls:
    - "Disabled-destination arm; relay, source and all inputs held identical across arms."
  measurements:
    - "Destination z recurrence, direct and integration-mediated emissions per arm, between-arm differences, reconciliation counts, high-water marks, replay equality."
  information_boundary_check:
    - "Not run; to be performed by Luna-45."
  hardware_mapping:
    - "Not applicable; hardware-neutral software reference, no hardware-equivalence claim."
  architecture_invariants_touched:
    - "A01-A03 event/local time; A04-A05 bounded topology; A06-A08 local, label-free computation; A15 hardware-neutral reference. No clause amended."
  preserves:
    - "Luna-42 PASS WITH FOLLOW-UP; Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED; Luna-44 evidence-quality PASS WITH FOLLOW-UP."
    - "ACP-0008 experimental, opt-in, unpromoted; ACP-0007 unchanged and disabled."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-45.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-authorization-luna45-depth2-destination-integration-20261006.md"
  tests_added: []
  tests_passing:
    - "Baseline (Python 3.11.5, process-local GIT_CONFIG core.autocrlf=false, core.eol=lf): source-mutation reconciliation test, 1 passed."
    - "Baseline: py -3.11 scripts/verify_luna44_canonical_fixture.py passed."
    - "git diff --check clean."
  tests_failed:
    - "Focused baseline selection: 287 passed, 2 failed; both failures are the known Windows-versus-frozen-Linux fixture materialization comparisons."
    - "Full baseline suite: 1089 passed, 2 failed, 1 skipped; both failures are those same comparisons."
    - "Failing tests: test_two_fresh_process_materializations_match_committed_fixture and test_two_fresh_process_materializations_match_exactly; unchanged baseline condition, not relaxed, not a Luna-45 blocker."
  tests_not_run:
    - "No Luna-45 experiment or Luna-45 tests; none exist."
    - "CUDA-specific test was skipped by the full-suite run."
  assumptions:
    - "Baseline results were run by the lead orchestrator at dbb440c on Windows/Python 3.11.5 with process-local Git LF overrides."
  unresolved:
    - "The final committed handoff SHA-256 must be recorded in Luna-45 provenance."
    - "Cross-platform fixture parity remains an unresolved owner decision, out of scope."
  recommended_next_agent:
    - "Luna-45 (execute under .github/agents/luna-45.agent.md), then Luna-0 independent review"
---

# Luna-45 authorization handoff

## Outcome and owned scope

**Luna-45 — AUTHORIZED / NOT EXECUTED.** Governance only, at baseline
`dbb440c763509781ee7ac5e4f2924851dde8e19c` on
`copilot/luna45-depth2-destination-integration`. Files: the new
`.github/agents/luna-45.agent.md` contract, a new entry in
`workflow/docs/luna/LUNA_WORKFLOW.md`, a new entry in
`workflow/ARCHITECTURE_CHANGELOG.md`, and this handoff. No code, tests,
fixtures, ACPs or experiment artifacts changed. Governance was committed at
authorization revision `9af6b4435ac581887f04f0951d0f7b16d7d661cd`; no
scientific execution has occurred.

## Contract scope note (final authorization contract)

Authorization ownership: the **project owner** authorizes Luna-45; Luna-0
records and gates it and does not self-authorize or review its own
authorization. Execution is not permitted until the owner approves publication
and the authorization revision is recorded. The contract
`.github/agents/luna-45.agent.md` now encodes, as ordered blocking gates:
G1 historical calibrated Luna-44 upstream reconciliation against retained
evidence (Luna-44's committed float policy `64 * sys.float_info.epsilon *
max(1.0, abs(observed), abs(expected))` only; all discrete quantities exact);
G2 cross-arm invariance; G3 independent queue-side and receiver-side captures
with separately reported reconciliation categories and exact source equality
plus the retained mutation test; G4 capacity bounds, high-water marks and
pending events. It also specifies full destination evidence fields with
independent `z_new`/discharge recomputation, the per-arm report, conditional
"candidate-opportunity precursor" analysis from source canonical emitters to
destination canonical emitters (never candidate instantiation), the full
reconstructable causal chain required for support in the calibrated destination
arm, NOT SUPPORTED IN THIS SETUP only after all gates pass, replay digest
material, equality and blocker-preservation semantics, and the restated
no-tuning exclusions. No code, test, fixture, ACP or experiment artifact was
changed; no experiment was executed. Governance authorization was committed
as `9af6b4435ac581887f04f0951d0f7b16d7d661cd`; this handoff records that
authorization revision.
## Architecture evidence

**OBSERVED:** Luna-0 gate review at the baseline found: reconciliation requires
`enqueue.source == reception.source` (`run_luna44_acp0008_canonical_fixture_rebaseline.py`
lines 871 and 900); `test_route_reconciliation_rejects_source_mutation_with_details`
(test line 517) fails reconciliation on a source-only mutation; the committed
fixture matches the owner-stated size, file SHA-256, semantic digest and
inventory; the manifest and source pins are listed above. **INFERRED:** the
frozen fixture is a suitable immutable input. **HYPOTHESIZED:** destination
integration may alter destination emissions; this is untested. The manifest
revision `86e5a2f…` is a commit revision; the committed manifest's Git blob is
`eb9179a…` (identical at that revision and at HEAD).

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| `py -3.11 -m pytest tests/test_luna44_acp0008_canonical_fixture_rebaseline.py::test_route_reconciliation_rejects_source_mutation_with_details -q` | dbb440c; Windows/Python 3.11.5; process-local GIT_CONFIG core.autocrlf=false, core.eol=lf | 1 passed | lead-run baseline |
| `py -3.11 scripts/verify_luna44_canonical_fixture.py` | same | passed | lead-run baseline |
| Luna-44/ACP-0008/runtime/routing/topology focused selection | same | 287 passed, 2 failed (the two known Windows materialization comparisons) | lead-run baseline |
| `py -3.11 -m pytest -q` | same | 1089 passed, 2 failed, 1 skipped (same two known comparisons versus the frozen Linux fixture; CUDA skip) | lead-run baseline |
| `git diff --check` | same | clean | lead-run baseline |
| Direct Python 3.10 run without LF overrides | Windows, system Git autocrlf | not authoritative: 7 additional source-pin fixture setup errors caused by CRLF checkout, resolved by the reviewed Python 3.11 + LF rerun | Luna-0 gate pass |
| Luna-45 experiment and tests | n/a | not run | not authorized in this pass |

The Luna-0 gate pass also ran the Luna-44 tests under Python 3.10 with LF
overrides (58 passed, 2 failed, the same two known comparisons); this is
supplementary, not the authoritative baseline.

## Benchmark and resource results

Not applicable; no experiment was executed.

## Assumptions, limitations and unresolved issues

The fixture was generated on Linux/Python 3.12.3; fresh Windows
materializations differ from it. Luna-45 consumes the frozen fixture and does
not regenerate it, so this does not block it. Parity needs a separately
authorized task. Required execution environment: Python 3.11.5 with
process-local `GIT_CONFIG_COUNT=2`, `GIT_CONFIG_KEY_0=core.autocrlf`,
`GIT_CONFIG_VALUE_0=false`, `GIT_CONFIG_KEY_1=core.eol`,
`GIT_CONFIG_VALUE_1=lf`.

## Reproduction and rollback

Reproduce the baseline with the commands in the validation table under the
stated environment. Roll back by deleting the new profile and handoff and
reverting the two workflow entries; the baseline is `dbb440c`.

## Next assignment

Luna-45 executes under its contract, returning a completed handoff for Luna-0
independent review. Integration readiness is not claimed. No Luna-46 is
authorized.