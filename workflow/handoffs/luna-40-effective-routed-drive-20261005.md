# Luna-40 — Existing Structural Growth and Effective Routed Drive

```yaml
tpcn_handoff:
  agent: Luna-40
  luna_identifier: "Luna-40"
  descriptive_name: "Existing Structural Growth and Effective Routed Drive"
  task_id: "Luna-40"
  component: "Bounded EXCURSION_V1 mechanism characterization"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "a39dd335e7af1b18a8d28ef3faf7b975304132df"
  result_revision: "5cbd62f929bdc19fff2f24de936b13d47c5386f8"
  dependencies:
    - "Luna-0 authorization: workflow/handoffs/luna-0-authorization-luna40-effective-routed-drive-20261005.md"
    - "ACP-0007 local EXCURSION_V1 structural growth"
    - "ACP-0008 opt-in slow temporal integration"
    - "Luna-28 and Luna-39 accepted mechanism baselines"
  owner: "Luna-0"
  classification:
    - "mechanism characterization"
    - "bounded"
    - "negative result"
    - "no architecture or ACP change"
  hypothesis: "Under the frozen stream and defaults, ordinary local evidence admits source->destination and its later routed contribution increases destination z toward or across theta_Z=1."
  counter_hypothesis: "No legal candidate/admission forms, or an admitted path fails to increase retained z; these are valid negative outcomes."
  interfaces_relied_on:
    - "ExcursionCharacterRuntime with actual canonical emission observation callback"
    - "StructuralObservationPlane and e2_local_temporal evidence"
    - "StructuralPlasticityController post-character admission"
    - "BoundedTopology and ordinary Model-B Edge"
    - "MultiExcursionNeuron with opt-in IntegrationConfig on destination only"
    - "Luna-39/Luna-34 make_spiral_dataset stream helper"
  label_information_boundary:
    - "Consumed only ordered example.points; labels and label-bearing metadata are not read."
    - "Each point contributes point.x + point.y at its original timestamp; same-time input batching is preserved."
    - "External input is delivered only to source; reward is constant 0.0."
  timing_assumptions:
    - "Strictly ordered source-local actual emission timestamps are required for association."
    - "Association window 4.0; structural growth delay 0.4; settling horizon 4.0."
    - "No global neural timestep or weight summation is used as an endpoint."
  reset_boundaries:
    - "Fresh neuron/runtime state and reset structural evidence for each character."
    - "Only admitted topology persists across characters within a run."
    - "Structural mutation occurs only after completed settling and quiescent teardown."
  resource_bounds:
    - "Nodes source, relay, destination; fan-in/out limits 2; edge/routing capacity 3."
    - "Queue 128; runtime event budget 1024; max activity events 1024; prediction capacity 8; prediction expiry 4.0."
    - "Eligibility capacity explicitly 1024 per ledger; neuron event budget 4096."
    - "Candidate capacity 4 per source; history 8; attempt budget 4 per run; at most one successful growth per character."
  authorized_scope:
    - "Run four frozen/observation/growth/no-local-evidence arms on seeds 0..4 and 64 training sequences per seed."
    - "Record actual observations, evidence, controller outcomes, routes, destination integration trace, resources, and deterministic replay."
    - "Check equal-time exclusion with actual canonical emissions in an isolated fixture."
  unauthorized_scope:
    - "No production mechanism, ACP, architecture, edge-weight semantics, or controller change."
    - "No efficacy/classification claim, parameter sweep, weight/delay/threshold/decay tuning, or task score."
    - "No hand-authored candidate or topology mutation during a live runtime."
    - "No ACP-0008 promotion, self-closure, or successor authorization."
  controls:
    - "FROZEN_NO_OBSERVATION"
    - "FROZEN_OBSERVATION_ONLY"
    - "LOCAL_GROWTH_ENABLED"
    - "NO_LOCAL_EVIDENCE_CONTROL with empty source structural-neighbor list"
    - "Actual equal-time source/destination canonical emissions produce no candidate"
  measurements:
    - "Initial/intermediate/final edges and bounded topology utilization"
    - "Actual structural observations, association pairs, candidate evidence, attempts, and admissions"
    - "Canonical emissions, route identity/payload/timing, destination receptions and ACP-0008 z trace"
    - "Eligibility reconciliation, runtime completion/events, queue peak, and replay digest"
  information_boundary_check:
    - "All arms use identical unlabeled streams and neural inputs."
    - "Observation-only and no-local-evidence controls match frozen neural event behavior."
    - "Focused label-isolation tests passed; no class/label fields appear in the experiment records."
  hardware_mapping:
    - "Not applicable: software-reference mechanism characterization only; no hardware mapping or equivalence claim."
  architecture_invariants_touched: []
  preserves:
    - "Canonical event-driven runtime and causal routed-event semantics"
    - "Label-isolated neural/structural computation"
    - "Bounded topology, runtime, eligibility, candidate, and growth-attempt limits"
    - "Static edge parameters and post-character quiescent topology mutation"
  architecture_change: false
  proposal: null
  files_changed:
    - "run_luna40_structural_effective_routed_drive.py"
    - "tests/test_luna40_structural_effective_routed_drive.py"
    - "artifacts/luna40-effective-routed-drive/config.json"
    - "artifacts/luna40-effective-routed-drive/results.json"
    - "artifacts/luna40-effective-routed-drive/summary.json"
    - "workflow/handoffs/luna-40-effective-routed-drive-20261005.md"
  tests_added:
    - "11 deterministic Luna-40 focused tests"
  tests_passing:
    - "Luna-40 focused tests: 11 passed"
    - "Luna-39/Luna-28/ACP-0008 and related structural/topology/runtime/eligibility/neuron regressions: 342 passed"
    - "Full repository suite: 1009 passed, 1 skipped"
    - "compileall for tpcn, tests, and Luna-40 runner"
    - "git diff --check"
  tests_failed: []
  tests_not_run: []
  assumptions:
    - "Results apply only to this frozen stream, topology, and default ACP-0008 parameters."
    - "Evaluation-seed examples are generated by the inherited dataset helper but are not consumed as neural input; only ordered training point sequences are used."
  unresolved:
    - "Independent Luna-0 review and disposition are pending."
    - "No conclusion is made about other streams, topologies, weights, integration settings, or task outcomes."
  recommended_next_agent:
    - "Luna-0 for independent review of this bounded mechanism result; no successor is authorized by Luna-40."
```

## Outcome and owned scope

**OBSERVED —** The authorized baseline was fetched and verified before execution:
branch `main`, clean index/worktree, and
`HEAD == origin/main == a39dd335e7af1b18a8d28ef3faf7b975304132df`.
This is the exact revision recorded in the run configuration. The four-arm
experiment and its full deterministic replay completed without a stop
condition. No production files, ACPs, architecture documents, or edge update
semantics were modified.

**OBSERVED —** The outcome is **NO LEGAL EDGE ADMISSION** for every seed
0–4. Across each arm's 320 characters, source emitted 1,715 times, all 1,715
routed transfers used only `source->relay`, and only source emitted
canonically (297 of 320 characters). Relay emitted zero times. Consequently
there were no `relay->destination` transfers, destination receptions,
destination `z` updates, or destination emissions. Destination maximum
observed `|z|` was `0.0`, below `theta_Z=1.0`.

In observation-enabled arms, all 1,715 structural observations were actual
source emissions. There were zero ordered source/destination association
pairs, candidate opportunities, candidate records, candidate rejections,
growth attempts, admissions, or shortcut transfers. The one legal local
neighbor was declared in the growth arm; the no-local-evidence arm declared an
empty source-neighbor list. The growth budget remained unused.

The two initial edges remained the complete topology in all arms:
`source->relay` and `relay->destination`, each with delay 1.0, `w=1.0`,
`d=1.0`, and `r=0.0`. The optional `source->destination` edge (delay 0.4,
`w=1.0`, `d=1.0`, `r=0.0`) was never proposed or inserted. Edge-capacity
utilization remained 2/3; maximum outgoing routing utilization was 1/3;
observed fan-in/out maxima were 1/2 limits.

**OBSERVED — controls:** the observation-only arm and the no-local-evidence
arm matched the frozen arm's neural events, emissions, routes, integration
state, and resources. The isolated equal-time check generated actual canonical
source and destination emissions at the same timestamp and produced zero
candidates. The full-run digest, including that check, was identical across
the two passes:

`f5c7f4d8fbc2037c43ac1118e96e6a2a23e4f0241da78cd7bea99a226b730211`

## Architecture evidence

This experiment exercised only the existing runtime emission-observation
callback, `StructuralObservationPlane`, `e2_local_temporal` evidence,
`StructuralPlasticityController`, bounded topology, and opt-in destination
integration trace. It did not change or authorize changes to A01–A15
architecture clauses. No architecture invariant was edited or weakened.

**INFERRED — bounded to this fixture:** the accepted ordinary stream did not
produce a relay emission or a source/destination temporal pair within the
declared local observation path. Therefore the existing admission mechanism
could not form a candidate in this run. Because no edge was admitted and no
route reached the destination, the experiment does not test the causal
effective-drive effect of an admitted shortcut. It does not identify a
production defect or imply that the mechanism cannot form evidence on other
streams or configurations.

**HYPOTHESIZED — not tested here:** a stream that generates the required
strictly ordered source-local evidence could admit the fixed-parameter
shortcut; whether it would then raise retained destination `z` remains
unanswered by this run.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Authorization baseline gate (`git fetch origin`; branch/status/revision comparison) | `main`, `a39dd335e7af1b18a8d28ef3faf7b975304132df` | Clean; `HEAD == origin/main` before execution | `config.json` `start_revision`; Luna-0 authorization handoff |
| `.\.venv\Scripts\python.exe run_luna40_structural_effective_routed_drive.py` | Python 3.11.5, five seeds, four arms, two complete passes | Completed; 1,280 character executions per pass; replay identical; no stop | `results.json`, `summary.json` |
| Luna-40 focused tests | Python 3.11.5 | 11 passed | `tests/test_luna40_structural_effective_routed_drive.py` |
| Luna-39/Luna-28/ACP-0008 and related structural/topology/runtime/eligibility/neuron regression selection | Python 3.11.5 | 342 passed | Test-run output in session record |
| `.\.venv\Scripts\python.exe -m compileall -q tpcn tests run_luna40_structural_effective_routed_drive.py` | Python 3.11.5 | Passed | No syntax/compile errors |
| `.\.venv\Scripts\python.exe -m pytest -q` | Python 3.11.5 | 1009 passed, 1 skipped in 20.06s; skip is CUDA-unavailable GPU visualization | Full-suite output; skipped test is `tests/test_gpu_visualization.py:61` |
| `git diff --check` | Luna-40 result changes | Passed | Final staged-diff check |
| Label isolation, control equality, bounded replay and actual-evidence fixtures | Five seeds; identical frozen run configuration | Passed; no label access; controls do not alter neural behavior; exact replay | Luna-40 focused tests and run artifacts |

No experiment capacity/runtime failure, invalid timestamp, non-finite state,
incomplete settling, or nondeterministic replay occurred. The one skipped GPU
test is environment-dependent; no other failed test or baseline failure was
observed.

## Benchmark and resource results

This is not a classification benchmark. The generated data are the inherited
synthetic spiral training point sequences: `SpiralConfig()`, 16 examples per
class, training seed `12007 + seed`, evaluation seed `22017 + seed`, and
`random.Random(330000 + seed)` ordering for seeds 0–4. Only ordered training
`example.points` were consumed. Each point became `x+y` at its original
timestamp with same-time batching. The evaluation partition was not neural
input.

Frozen topology/configuration: three nodes; initial edges
`source->relay` and `relay->destination`; fan-in/out 2; edge and routing
capacity 3. Source and relay used `MultiExcursionNeuron(E1Config(event_budget=4096))`
without integration. Destination used the same event budget and default
`IntegrationConfig()`; ACP-0008 remained at decay 0.1, gain 1.0,
`theta_Z=1.0`, and `z_max=4.0`. The structural policy was unchanged
`e2_local_temporal`, with source neighbors `[destination]` only in the growth
arm, 4.0 association window, history 8, candidate capacity 4, maximum score
3, delay 0.4, and total attempt budget 4.

Per arm (320 characters):

| Measure | Result |
|---|---:|
| Canonical source emissions | 1,715 |
| Canonical relay / destination emissions | 0 / 0 |
| Routed transfers, all on `source->relay` | 1,715 |
| `relay->destination` / shortcut transfers | 0 / 0 |
| Destination receptions / integration updates | 0 / 0 |
| Maximum destination `|z|` / `theta_Z` | 0.0 / 1.0 |
| Active observation-arm structural observations | 1,715 (source only) |
| Association pairs / candidate opportunities / candidate records | 0 / 0 / 0 |
| Growth attempts / successful admissions | 0 / 0 |
| Runtime events processed | 11,109 |
| Queue peak | 2 of 128 |
| Maximum eligibility-ledger occupancy | 19 of 1,024 |
| Eligibility reconciliation/capacity errors | 0 / 0 |

All character runtimes completed and settled with empty event queues. The
mechanistic interpretation for every seed is **NO LEGAL EDGE ADMISSION**;
therefore neither “endogenous drive reached” nor “endogenous drive increased”
is supported. No task, energy, utility, prediction, accuracy, calibration,
generalization, or hardware metric was defined or inferred.

## Assumptions, limitations and unresolved issues

- **Measured:** the no-candidate/no-admission branch and zero destination drive
  for this one frozen stream, topology, and default integration configuration.
- **Not measured:** drive after an admitted shortcut, because none was
  admitted; a direct-only emission comparison; alternate candidate opportunity
  streams; or any task-level outcome.
- The result is not evidence of a production defect and cannot be generalized
  to other inputs, topology, weights, delays, or integration settings.
- **Unresolved:** Luna-0 independent review and disposition. Luna-40 does not
  close itself, promote ACP-0008, or authorize a successor.

## Reproduction and rollback

From a clean checkout at the authorized baseline with the project Python
environment configured:

```powershell
.\.venv\Scripts\python.exe run_luna40_structural_effective_routed_drive.py
.\.venv\Scripts\python.exe -m pytest -q tests/test_luna40_structural_effective_routed_drive.py
.\.venv\Scripts\python.exe -m compileall -q tpcn tests run_luna40_structural_effective_routed_drive.py
.\.venv\Scripts\python.exe -m pytest -q
```

The runner writes `config.json`, `results.json`, and `summary.json` under
`artifacts/luna40-effective-routed-drive/`. Reproduction consumes no labels.
To roll back the Luna-40 deliverable, revert only the Luna-40 implementation,
test, handoff, and artifact files listed above; no production mechanism file
requires restoration.

## Next assignment

Return this evidence, the implementation/evidence revision, and artifact paths
to Luna-0 for independent review. Integration of no production changes is
required. Do not promote ACP-0008 or assign/authorize a follow-up from this
handoff.
