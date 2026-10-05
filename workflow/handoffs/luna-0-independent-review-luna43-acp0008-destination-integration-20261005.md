# Luna-0 Independent Review — Luna-43 ACP-0008 Destination Integration

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent post-Luna-43 destination integration review"
  task_id: "independent-review-luna43-acp0008-destination-integration-20261005"
  component: "ACP-0008 fixed-topology downstream destination integration"
  status: "complete — experiment BLOCKED at exact historical input identity gate"
  contract_version: "1.2"
  branch: "copilot/execute-luna-43-cycle"
  base_revision: "32898e3b50daf0834c6ddb8889dd5127f7fb489d"
  result_revision: "the commit publishing this handoff and governance update"
  authorization_revision: "f304e96f994d5b3f7842589c1b505d09c8fae4c6"
  execution_revision: "50aaa074929d6dfe506689c80c306d7e54be32f2"
  owner: "Luna-0; unresolved source-stream comparability returned to project owner"
  classification:
    - "independent raw-artifact and source review"
    - "scientific result BLOCKED / destination comparison UNDETERMINED"
    - "execution protocol and scope CONTRACT PASS WITH FOLLOW-UP"
    - "no destination-condition verdict, no promotion, no successor authorization"
  hypothesis: "The committed execution stops at the predeclared exact Luna-42 input-identity gate before evaluating destination conditions."
  counter_hypothesis: "The retained gate, execution chronology, provenance, or raw evidence fails independent reconstruction."
  interfaces_relied_on:
    - "Committed Luna-43 runner and focused tests"
    - "Raw Luna-42 calibrated-arm Phase-B character records"
    - "MultiExcursionNeuron, ExcursionCharacterRuntime, Model-B topology"
  label_information_boundary:
    - "Runner consumes ordered point coordinates/timestamps via the Luna-34 helper; no labels or evaluation outcomes are read."
    - "No task, classification, prediction-improvement, reward, utility, energy, or efficacy endpoint is evaluated."
  timing_assumptions:
    - "Exact point timestamps and same-time batches are part of the historical input identity."
    - "No global neural timestep; fixed two-hop delays are 1.0."
  reset_boundaries:
    - "One complete fresh c00-000 runtime in DESTINATION_DISABLED was retained before the historical identity mismatch stopped execution."
  resource_bounds:
    - "Retained character: queue 2/128; 15 runtime events/1024; eligibility peak at most 1/1024 per ledger; no pending events."
  authorized_scope:
    - "Independently audit the exact published Luna-43 runner, tests, handoff, four raw artifacts, Luna-42 source artifact, and relevant governance/production code."
    - "Replay the recorded runner revision only in a disposable /tmp worktree and write replay output outside the repository."
    - "Rerun the focused, relevant regression, and full repository test suites."
    - "Publish this review handoff and update workflow/changelog status."
  unauthorized_scope:
    - "Do not modify or rerun/publish the experiment in the main worktree."
    - "Do not change experiment artifacts, runner/tests, production/API, ACP-0007/ACP-0008, or historic scientific outcomes."
    - "No numerical-tolerance relaxation, input canonicalization, retuning, WEMA, efficacy, structural growth, calibration, promotion, or Luna-44."
  controls:
    - "Exact historical source-stream digest gate."
    - "Exact canonical event, route, timestamp, and same-run copied payload identity where applicable."
  measurements:
    - "Independent SHA-256 and canonical artifact/configuration digest reconstruction."
    - "Exact first-character inputs, event/route IDs, counts, and resource high-water marks."
    - "Disposable same-revision replay output identity."
    - "Focused, ACP-0008/routing/runtime, and full-suite test results."
  information_boundary_check:
    - "Source review confirms the helper returns example.points; no labels, class correctness, or task outcomes are consumed."
  hardware_mapping:
    - "Not run and not applicable; no hardware-equivalence claim."
  architecture_invariants_touched:
    - "A01/A03: observed finite-delay event route on one completed character only."
    - "A04: fixed three-node, two-edge topology in runner; no topology mutation."
    - "A07/A08: local bounded integration and runtime configuration; no global/task input."
    - "A14: structural plasticity disabled; no candidate/admission/pruning."
    - "A15: no hardware claim."
  preserves:
    - "A01-A15 contract text and ACP-0007 unchanged."
    - "ACP-0008 experimental, opt-in, and unpromoted."
    - "Luna-42 PASS WITH FOLLOW-UP; Luna-41 BLOCKED."
    - "Luna-40 NOT SUPPORTED IN THIS SETUP; Luna-39 PASS WITH FOLLOW-UP."
    - "Historical Luna-37 NOT SUPPORTED IN THIS SETUP and Luna-34 BLOCKED / UNDETERMINED."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna43-acp0008-destination-integration-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Luna-43 focused: 4 passed."
    - "Disposable replay at the exact runner commit reproduces all four retained artifact files byte-for-byte."
    - "Full repository suite: 1023 passed; no new failures."
    - "git diff --check (final review changes): passed."
  tests_failed:
    - "tests/test_luna41_acp0008_temporal_calibration.py::test_isolated_routed_input_matches_normalized_amplitude_and_leaks"
    - "tests/test_luna41_acp0008_temporal_calibration.py::test_near_pair_records_source_residual_payload_deviation"
    - "tests/test_luna42_acp0008_corrective_calibration.py::test_isolated_routed_input_preserves_exact_provenance"
    - "tests/test_luna42_acp0008_corrective_calibration.py::test_near_pair_uses_actual_production_routed_payloads"
  tests_skipped:
    - "tests/test_gpu_visualization.py:61 — CUDA unavailable."
  tests_not_run:
    - "Full three-arm experiment and its declared whole-experiment replay: correctly not reached after the first-character historical gate."
    - "Destination ACP-0008 equation checks beyond the retained first-character record; that record has zero destination receptions."
    - "Hardware equivalence, efficacy, energy benefit, structural adaptation, and ACP promotion."
  assumptions:
    - "Observed one-point difference is consistent with the recorded Windows/Python-3.11.5 versus Linux/Python-3.12.3 environments; the precise lower-level library cause is not established."
  unresolved:
    - "Project owner must decide whether exact historical input identity remains required across environments, whether a separately frozen source stream is needed, or whether another independently justified protocol is appropriate. Do not weaken the existing gate in this review."
  recommended_next_agent:
    - "Project owner to decide the source-stream comparability question; no Luna-44 or automatic successor is authorized."
```

## Outcome and independent verdict

**Scientific result: BLOCKED / destination comparison UNDETERMINED.** The
committed runner correctly stops on its predeclared exact historical input
identity check at `DESTINATION_DISABLED`, seed `0`, sequence `0`, character
`c00-000`. It does not run another character, either other destination arm, or
the whole-experiment replay. There is no condition-complete destination trace
and no scientific result—positive, negative, or null—about destination
integration or destination emissions.

**Execution protocol and contract: PASS WITH FOLLOW-UP.** The exact stop is
implemented before continuing the arm/character loops, and the retained
execution is bounded and label-free. No A01-A15 requirement or accepted ACP
was amended or silently promoted. The follow-up is the unresolved cross-source
stream comparability question, which belongs to the project owner; it is not
evidence of a production/API defect and does not authorize an automatic
Luna-44.

## Evidence reconstructed from committed source and raw artifacts

The reviewed HEAD was clean at
`32898e3b50daf0834c6ddb8889dd5127f7fb489d`; the branch was
`copilot/execute-luna-43-cycle`, and `origin/main` was the authorized baseline
`b6ca4a67783bf37ded146944f8dc9afaf5277f11`. The authorization commit
`f304e96f994d5b3f7842589c1b505d09c8fae4c6` precedes the runner commit
`50aaa074929d6dfe506689c80c306d7e54be32f2`. The SHA-256 of the committed and
published runner is
`f3bdc0288ded146e592587e1849329093f2a0d1702e69956447b4b5862842e5b`.
The final publication adds only the four artifacts and execution handoff;
the runner/test source did not change after the recorded execution commit.

I reconstructed the stop directly from `results.json` and the raw Luna-42
Phase-B calibrated record at `artifacts/luna42-acp0008-corrective-calibration/results.json`.
The two records each contain 12 one-point batches with identical timestamps and
identical values except batch 3 / point 0:

| Source | Value | Binary64 hex |
|---|---:|---|
| Luna-43 generated | `-0.1646535199398629` | `-0x1.5135dd5a81039p-3` |
| Luna-42 retained | `-0.16465351993986282` | `-0x1.5135dd5a81036p-3` |

The absolute difference is `8.326672684688674e-17`, exactly 3 ULPs at that
magnitude. Accordingly the canonical input digests differ:

```text
Luna-43: 176897def09943a3d8276104d562c80b02982c806f2672e8a1c2b484a8921a1d
Luna-42: e196be616cdd0abe616a82044265dcad3905ea5dc7d2b6c51c207556c4f855e4
```

This is consistent with the recorded source environments: Luna-42 was generated
on Windows 10 / Python 3.11.5, while Luna-43 ran on Linux /
Python 3.12.3. Same-environment replay reproduced the Luna-43 input and gate
exactly. This establishes environment-associated numeric divergence, not the
specific library or operation responsible for it. The exact digest requirement
was predeclared and is not relaxed here.

The remaining historical checks in the failed record all pass: source canonical
emissions, relay emission records, relay integration trace, source-to-relay and
relay-to-destination route lists, and destination-reception identity. The
observed source event is `source:excursion:1`; its route event has the same
event ID, timestamp `299.7195236202522`, sequence `14`, lineage `1`, route
`source -> relay`, and route depth `1` as the historical event. The current
Model-B route payload is `0.31144875735993677`, versus historical
`0.3114487573599367` (one ULP); the current route payload is the production
`tanh(0.32214899243574596)`. This is an equation-derived numeric difference
within the declared binary64 rule. The current relay reception copies the
current route payload exactly. Neither route-list order nor event identity is
the failed comparison; the exact `input_digest` is.

For this one completed character only, observed counts are one source emission,
one source-to-relay transfer/reception, zero relay emissions, zero
relay-to-destination transfers/receptions, and zero destination emissions.
The queue peak is 2/128; 15 events were processed against budget 1024; all
three eligibility ledgers reconcile with peak occupancy at most 1/1024; the
runtime settles with no pending events. These are not aggregate or
condition-complete results. The sole retained route/equation evidence is
limited to the `c00-000` source-to-relay event and relay reception. No
destination ACP-0008 recurrence can be checked because this character has no
destination reception; destination equation checks are therefore **not
applicable**, and no destination emission inference is drawn.

### Artifact integrity and replay

All file SHA-256 values, internal artifact digests, the frozen configuration
digest, and aggregate digest were independently recomputed from the retained
bytes and canonical JSON:

| Artifact | File SHA-256 | Internal artifact digest |
|---|---|---|
| `config.json` | `0b97f064422cbdee531b6d7bc7732a3571a821798321333c4e26ee63913347f2` | `49115b4df94a8aec288e2410452aa4c0be92369667051a85d6438127d234bd4d` |
| `results.json` | `b5c655abe2a653ab32a3d66c569574b5dedbe6f05af851e7678866e4ab513e26` | `a9665bcf19616eed7762f1865cf9d51131ffb4b593e888e87844665f4dd1e407` |
| `summary.json` | `424da866201cece9b5f242702405c8940b046aa2b6d5d981d2c4538ff8031e9a` | `34975a156292cb0483b956fe6830f93b290b058591c832175aca4b2a529a0107` |
| `replay.json` | `a3d6d9648605ab4be4abd9b4c33e714982b2e12c292c8b46e68c15cac3605f1d` | `8510aaead645251dd5f0b272c22fdd49c5508b2b6ddfe5d79d25a5f73fcf2b02` |

Frozen configuration digest:
`648db5a29a741332a96304c345a8588b0f7df27aed1e7b474f7527ab868cee59`.
Aggregate artifact digest:
`365cbede264098af8d57d3ac3a79eed978b1fac866ebe67eae73a316eac56354`.

I created a disposable detached worktree at the exact execution revision,
supplied the committed Luna-42 raw source artifact, and ran the committed
runner once with its recorded provenance and output under `/tmp`. All four
generated artifacts matched the retained files byte-for-byte. This independently
reproduces the retained attempt and its blocked gate. It is **not** a
whole-experiment replay: the runner's `initial_digest` and `replay_digest`
remain null with `not_run_after_blocker=true`, correctly recording that the
second full execution was never started.

## Scope and architecture review

The runner reads only ordered point streams (`example.points`) and timestamps;
the Luna-34 helper selects point sequences and shuffles the sequence list
without the Luna-43 runtime reading labels. It uses the authorized fixed
`source -> relay -> destination` graph, `w=1` Model-B edges, fixed calibrated
relay, the three specified destination configurations, fresh character state,
bounded event/queue/eligibility settings, neutral reward, and disabled growth.
No production API, topology, parameter, previous artifact, ACP, or architecture
contract file was changed. The runner includes a post-condition precursor scan
path, but the historical gate prevents that scan from running in this retained
execution; there was no candidate creation or topology mutation.

The experiment gives bounded single-character evidence relevant only to A01,
A03, A04, A07, A08 and A14. It does not test the full predictive-coding
acceptance criteria or establish integration readiness. A15 hardware
equivalence is not applicable and was not run. ACP-0008 remains experimental,
opt-in, and unpromoted; ACP-0007 remains unchanged and disabled. No ACP or
contract revision is warranted by this review.

## Validation record

Environment: Python 3.12.3, pytest 9.1.1, NumPy 2.5.3, SciPy 1.18.1,
PyTorch 2.14.1+cu130, Linux 6.17.0-1022-azure x86_64. CUDA is unavailable.

| Command / procedure | Result |
|---|---|
| `python -m pytest -q tests/test_luna43_acp0008_destination_integration_mechanism.py` | 4 passed |
| `python -m pytest -q tests/test_excursion_neuron.py tests/test_excursion_integration.py tests/test_e2_multi_excursion.py tests/test_topology.py tests/test_event_runtime.py tests/test_luna38_excursion_integration_state.py tests/test_luna39_acp0008_propagation_emission_diagnostic.py tests/test_luna41_acp0008_temporal_calibration.py tests/test_luna42_acp0008_corrective_calibration.py` | 217 passed, 4 failed |
| `python -m pytest -q -rs` | 1023 passed, 4 failed, 1 skipped; 1028 collected |
| `git diff --check` | Passed on final review changes |

The same four exact-comparison failures recorded in the authorization baseline
persist: Luna-41 and Luna-42 tests compare computed `0.39999999999999997` with
literal `0.4`: `test_isolated_routed_input_matches_normalized_amplitude_and_leaks`
and `test_near_pair_records_source_residual_payload_deviation` in the Luna-41
file, plus `test_isolated_routed_input_preserves_exact_provenance` and
`test_near_pair_uses_actual_production_routed_payloads` in the Luna-42 file.
The relevant regression selection had 217 passing tests alongside these four
failures. No new or unrelated failure appeared. The one skip remains
`tests/test_gpu_visualization.py:61` because CUDA is unavailable. No assertion,
runner criterion, or scientific tolerance was changed.

## Remaining issue and next assignment

The source-stream identity mismatch is a verified protocol blocker, not a
destination result, a production/API defect, or a reason to retry under altered
inputs. Return to the project owner the narrow unresolved question of how to
compare or freeze point-stream identity when the historical record and the
authorized execution were generated on different Python/platform environments.
Any later work requires a separate owner decision, independent justification,
bounded contract, and acceptance gate. **No Luna-44 is created or authorized
here.**

The historical record remains intact: Luna-42 **PASS WITH FOLLOW-UP**,
Luna-41 **BLOCKED**, Luna-40 **NOT SUPPORTED IN THIS SETUP**, Luna-39
**PASS WITH FOLLOW-UP**, Luna-37 **NOT SUPPORTED IN THIS SETUP**, Luna-34
**BLOCKED / UNDETERMINED**, ACP-0007 unchanged, and ACP-0008 experimental,
opt-in, and unpromoted.
