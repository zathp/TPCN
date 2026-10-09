# Luna agent handoff — owner task objective and Luna-59 prerequisite

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Controlled event/deadline task governance"
  task_id: "owner-task-objective-luna59-governance-20261009"
  component: "Task objective and reward/prediction interface readiness"
  status: "complete - governance only; design prerequisite authorized, not executed"
  contract_version: "1.2"
  branch: "main"
  base_revision: "0a6b0125627384a036410ff1588cd1115bf53147"
  result_revision: "The publication commit containing this handoff; obtain with git log -1 --format=%H -- this path."
  dependencies:
    - "Current project-owner request dated 2026-10-09"
    - "Accepted ACP-0006 emission/prediction/eligibility boundaries"
    - "Experimental opt-in ACP-0008, not promoted"
    - "Luna-58 retained publication; independent review still pending"
  owner: "Project owner; Luna-0 coordinates governance, not self-approval of new semantics"
  classification: ["OBSERVATION", "VERIFICATION"]
  hypothesis: "Not a scientific experiment. Readiness proposition: existing governed interfaces support a fair causal event/deadline task without invented credit or output semantics."
  counter_hypothesis: "Absent task-output/deadline semantics or absent credit identity for silence blocks a trained task contract; a fully specified no-training design could avoid credit changes."
  interfaces_relied_on:
    - "LocalPredictor create_prediction/emit_prediction/observe/expire"
    - "EligibilityLedger record_activity/apply_signal and RewardSignal identity"
    - "ExcursionCharacterRuntime _consume_emission/end_character/reset"
    - "E1Config/IntegrationConfig and actual ExcursionEmission"
    - "External prototype readout in tpcn/experiments.py"
  label_information_boundary:
    - "Owner requires outcomes/evaluation labels outside neural inference."
    - "No new inputs, rewards, labels or scientific observations supplied by this governance pass."
  timing_assumptions:
    - "No task window or deadline inferred from settling_horizon or historical crossing times."
    - "Premature and late first outputs are errors; exact numeric boundaries remain unapproved."
  reset_boundaries:
    - "Existing runtime destroys per-character queue, predictor/eligibility/readout state and resets neurons."
    - "Future train/evaluation and generator split boundaries must be frozen before execution."
  resource_bounds:
    - "This pass: read-only source/artifact inspection and four governance files; zero runtime/scientific executions."
    - "Prerequisite: two documents, eight logical cases, two design alternatives, zero executions."
  authorized_scope:
    - "Publish .github/agents/luna-59.agent.md as a design prerequisite only."
    - "Record owner objective, readiness findings, workflow and changelog."
  unauthorized_scope:
    - "No experiment, benchmark, scientific replay, dataset generation, tuning, core/test/runner/config edit or reward semantic change."
    - "No architecture promotion, hardware claim, Luna-58 independent closure or application benchmark."
  controls:
    - "Live fetch plus clean main/HEAD/origin-main equality."
    - "Five retained Luna-58 artifact SHA256 comparisons to its handoff."
    - "Parsed initial/replay stream equality; not an independently executed replay."
  measurements:
    - "No new accuracy, FPR, prediction-loss, event, reward, energy or task-efficacy measurement."
    - "Retained Luna-58 summary and immutable hashes inspected, not regenerated."
  information_boundary_check:
    - "Native next-input prediction is distinguished from the proposed event/deadline task."
    - "No-emission credit remains unmatched; negative reward is not falsely reported as absent-trace learning."
  hardware_mapping:
    - "Not run. A future proposal must describe finite local state/identity/deadline resources and external evaluator placement."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "All core behavior, ACPs, historical experiments/artifacts, A01-A15 and contract version 1.2."
    - "ACP-0008 experimental, opt-in, disabled-by-default status."
    - "ACP-0006 emission-only eligibility and explicit unmatched silence reward."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-59.agent.md"
    - "workflow/handoffs/luna-0-owner-task-objective-luna59-governance-20261009.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All Python tests, scientific runners/replays, parameter searches and dataset generators."
    - "New task-output, omission-credit, held-out efficacy and hardware validation."
  assumptions:
    - "The full current user request and its owner-decision restatement are the available decision source; no separate attachment was accessible."
  unresolved:
    - "Fair trained omission/correct-silence credit versus a justified fixed/no-training design."
    - "Task prediction event, target construction, eligibility window/deadline, absence/premature/late resolution."
    - "Deterministic generator/splits/provenance, exact held-out population/repetitions and anti-shortcut controls."
    - "Historical/default comparator identity, mechanism/component arms and finite task budgets."
    - "Duplicate efficiency penalty formula and detailed scoring/timing boundaries."
    - "Independent Luna-58 review and any unavailable complete owner decision attachment."
  recommended_next_agent:
    - "Luna-59: explicitly assigned documentation-only Luna-8-led interface design under the new contract."
    - "Luna-0/project owner: accept or reject that design before any implementation or efficacy authorization."
```

## Outcome and disposition

**TASK OBJECTIVE DEFINED — REWARD SEMANTICS PREREQUISITE REQUIRED.**

The high-level scientific objective is defined by the owner. A fully bounded
task-efficacy experiment is not ready. This pass authorizes only the smallest
design prerequisite to decide fair attribution or a legitimate no-training
alternative. The prerequisite has not been executed. No efficacy experiment
is authorized, and none of the allowed four parallel-experiment slots is used.

### Owner decisions read and preserved

The available source is the complete 2026-10-09 task message, including its
restatement of owner decisions. No separately attached decision text/file was
accessible in the supplied context or tracked repository. This record does
not claim otherwise; any omitted binding attachment must be obtained before
resolving dependent details.

The owner selects controlled deterministic temporal event/deadline
prediction; correct silence on negatives and ambiguous prefixes; premature
and late output errors; first-output scoring with duplicate event-efficiency
penalty; scientific mechanism validation priority; primary held-out balanced
accuracy; minimum +10 percentage-point improvement versus a declared
historical/default comparator; maximum +5 percentage-point FPR degradation;
majority seed direction if stochastic or exact independent replay if
deterministic; matched positive/negative and temporal anti-shortcut controls;
no E+49 crossing requirement without a task mapping; deferred application
benchmarks. Up to four parallel experiments is permission, not a quota.
Candidate configuration is not specified; Luna-58's rate is not automatically
the candidate. Governance only; stop before execution.

## Sources and exact reviewed baseline

**OBSERVED:** `git fetch origin` succeeded; the worktree was clean and
`HEAD == origin/main == 0a6b0125627384a036410ff1588cd1115bf53147`
on `main`. No old turn's SHA was used as the current baseline.

The requested historical `tpcn-luna-workflow/` directory is absent. Each of
the seven named authorities was resolved to its tracked equivalent under
`workflow/` and read: Architecture Contract (v1.2), changelog's current
status entries, workflow's current status/Future Luna Contract/role rules,
acceptance criteria, proposal README, ACP template, and handoff template.
`workflow/README.md` documents the old package layout; no competing authority
was invented. Actual handoff publication follows `workflow/handoffs/`.
No root/nested `AGENTS.md`, `copilot-instructions.md` or instructions file
was found in the inspected repository; applicable Luna-58 contract was read.

Additional source evidence:

| Source | Read evidence and relevance |
|---|---|
| `workflow/docs/architecture_proposals/ACP-0006.md` §§5–11 | Numeric next-input predictions; emission-only eligibility; first-readout reward; silence unmatched; external readout learning; finite settling/reset |
| `workflow/docs/architecture_proposals/ACP-0008.md` | Opt-in bounded slow integration; disabled/default distinction; reward and prediction interfaces unchanged |
| `.github/agents/luna-58.agent.md` | Single fixed destination-rate mechanism authorization, frozen strata/budgets, no task-efficacy claim |
| `workflow/handoffs/luna-58-finite-destination-retention-execution-20261009.md` | Authorization/implementation identities, retained hashes/results, reported tests, explicit independent-review stop |
| `workflow/handoffs/delayed-credit-Luna-8.md` | Stable reward identity, bounded at-most-once local credit, unmatched credit behavior |
| `tpcn/predictive_coding.py` | `Prediction`, metadata expected time, generic event emitter, key/expiry matching, expiry without omission error |
| `tpcn/eligibility.py` | Required trace/prediction identity, signed credit, bounded FIFO duplicate identities, unmatched nonexistent trace |
| `tpcn/experiment_excursion_runtime.py` | Source-emission prediction creation; no queued task prediction; emission-only activity; first-emission terminal reward; settling/reset |
| `tpcn/experiments.py` | Label-free streaming then outer label-based reward/readout update; prototype learning is distinct from neural credit |
| `tpcn/excursion_neuron.py` | Bounded E2/slow-integration configuration and actual canonical emission path |
| `experiments/luna54/run.py`, `experiments/luna54/config.json` | Retained causal routing driver, neutral reward, bounded queue/events/eligibility; not a deadline-task generator |
| `experiments/luna55/config.json`, `experiments/luna58/config.json` | Exact supported component conditions, single rescue intervention, fixed historical budgets |
| `artifacts/luna45-depth2-frozen-config-20261006-r2/config.json` | Historical 0.0125 and opt-in default/disabled arms, frozen topology and normalized thresholds |
| `tests/test_luna58_finite_destination_retention.py` | Retained-result checks inspected only, not run |
| `artifacts/luna58/{rr-control-initial,rr-control-replay,finite-initial,finite-replay,summary}.json` | SHA identities and retained stream equality checked without runner import/execution |

## Readiness findings

**OBSERVED — prediction/output:** `_consume_emission()` creates a local
next-`external-input:scalar` `Prediction` for the configured source. It never
calls the generic `emit_prediction()`; its observable emission is not already
a task-specific event/deadline forecast. The emission observer exposes
source, ID and timestamp but is not itself a forecast schema/scorer.
`LocalPredictor.observe()` matches key/expiry; `expected_resolution_at` does
not enforce a not-before window. Expiration increments/removes records,
without creating a missed-target/negative-trial error. A settling horizon is
a runtime-processing limit, not a frozen scientific deadline.

**OBSERVED — reward:** signed negative `RewardSignal` is supported for a real
identified trace. The adapter records eligibility only on emissions, rewards
the first readout-source trace, and marks no-emission reward unmatched.
ACP-0006 explicitly requires that behavior. Hence a missed positive with no
readout emission and a correctly silent negative do not acquire local
reward credit through the current interface. An outer utility reward record
does not establish matched local credit or a parameter-learning consumer.
The classifier's zero-evidence result and mean feature `0.0` are not emissions.

**INFERRED:** training under that attribution rule cannot be presented as
fairly crediting all task outcomes. Adding silent-prefix eligibility, a fake
zero activity, a fabricated prediction, or a new deadline outcome signal
would invent semantics and may amend accepted ACP-0006. This pass approves
none of them.

**INFERRED — no-training alternative:** fixed E2 configurations plus an
external, first-event deadline scorer could in principle evaluate omissions
and correct silence without neural reward. This is a viable design
alternative, not evidence that the current scalar predictor already performs
the owner's task. It still needs a frozen causal forecast mapping, independent
target rule, population, temporal controls and exact held-out protocol.
Therefore reward changes are not declared universally necessary; the
prerequisite must resolve this alternative before proposing a semantic change.

### Can the complete experiment be frozen without guessing?

| Requirement | Current disposition |
|---|---|
| High-level task and meaningful-effect thresholds | Owner-defined; preserved |
| Exact target/event construction and prediction/readout observable | Not frozen; native scalar prediction does not establish task-event prediction |
| Eligibility time, deadline, premature/late/absence resolution | Not frozen; expected time and settling are insufficient |
| Independent matched positive/negative generator, splits and provenance | No pinned task dataset/generator; historical outcome-selected strata are not task labels |
| Reward timing/identity/attribution and update consumer | Existing emission trace identities work; omission/silence unmatched; training or no-training unresolved |
| Comparator and mechanism/component arms | Supported choices identified, not a task-specific justified selection |
| Exact held-out population and repetitions | Not frozen; 320 historical streams and initial/replay cannot be repurposed as independent held-out samples |
| Finite execution/state/topology budgets | Existing reference bounds known; proposed task horizon/population must justify its own finite limits |
| Primary/secondary scoring and falsification | Owner thresholds fixed; first-event interval and duplicate-penalty equation unresolved |
| Temporal/causal anti-shortcut controls and isolation | Required, but not yet instantiated on an independent task population |

## Configuration and metric decisions

No scientific arm, input stream, task deadline, sample count or parameter is
authorized by this pass. In particular, do not select destination
`decay_rate_z=0.00001` merely because Luna-58 rescued inspected streams.

Supported options have different meanings: canonical `integration=None`;
opt-in `IntegrationConfig` default `0.1`; historical relay/destination
`0.0125`; and retained HH/RH/HR/RR component controls with H=`0.0125`,
R=`0.00125`. The component controls provide mechanistic motivation for a
future composition test; they are not evidence of task efficacy or a reason
to fill four experiment slots. The final comparator must explicitly say
which historical/default configuration it denotes.

The owner-defined primary metric is held-out balanced accuracy, with +10 pp
improvement and <=+5 pp FPR degradation as joint meaningful-effect criteria.
First-output timing governs success; duplicates cannot salvage a wrong first
output. The exact duplicate penalty remains a required design decision.
Secondary requirements include timing/latency errors, duplicates/events,
prediction matches/loss/expiry, task errors separately, resource/proxy energy
and connectivity use, bounds/pending/clipping/truncation and replay identity.
An all-silent network must not be reported as useful task efficiency.

Future controls must match counts, amplitude and duration nuisances, preserve
ambiguous prefixes, break temporal shortcuts without outcome-derived
selection, and expose causal route/retention dependence. Labels/outcomes,
strata and oracle results must remain evaluator-only during inference; any
training signal would be explicitly delayed to causally available outcome
time and excluded from held-out evaluation. No synthetic negative target
event may be inserted as a hidden label input. No E+49 mapping is invented.

## Luna-58 evidence and review status

Authorization publication:
`7dd3dc868e7518a33418d4df94b07c15dea52adb`.
Scientific implementation/results:
`187df41dffed7fad2ed2f5f657575229d5e6d015`.
Current publication:
`0a6b0125627384a036410ff1588cd1115bf53147`.

**OBSERVED in retained records:** six primary nonresponders and ten
responders cross; E+49/E0 10/NR1 189/NR0 23 remain at zero; the secondary
33-stream stratum is separate. Retained summary reports 421 reconciled routes,
exact replay, zero clipping/pending/bound failures and seven inherited
off-target truncations. The handoff reports 1,752 passing tests and one
Windows symlink capability skip; those tests were **not rerun here**.
Current workflow/changelog still require independent Luna-0 review, and no
separate published Luna-58 independent review was found. This pass does not
close that gate or recast mechanism crossing as task success.

Five raw artifact hashes match the handoff:

| Artifact under `artifacts/luna58/` | SHA-256 |
|---|---|
| `rr-control-initial.json` | `5ba742838dc068f244191f672fac0663d74d55f4394ca430e5397acb3e6c99e8` |
| `rr-control-replay.json` | `7d929a1ab053266e6e78e84ebf69d359cd37791b142f59a3d8fda46696cd0fde` |
| `finite-initial.json` | `926b44b2a2ab3a576864cd3738b6e9f7fb5ff1df58177fc2af13b17f99c104b4` |
| `finite-replay.json` | `83b1c9cc2e1720656398e211b7d32c840adefbd267e23d30b2fbb89e0a538977` |
| `summary.json` | `ba33ac051d305dc526060cbe0edc84b9c50b827edcce03b5be93b84dfd58d1ea` |

PowerShell JSON parsing and serialization of the retained `streams` arrays
found equality within each pair. This is an integrity/retained-record check,
not exact independently executed replay or fresh scientific evidence.

## Architecture and validation record

A01–A04/A08: retain causal finite delays, local elapsed time and bounded
execution. A06: distinguish native prediction/error from future task output;
do not claim omitted-target errors already exist. A07/A11: preserve explicit
local credit identities and labels outside inference. A09/A10: proxy
measurements and usefulness, not energy-only silence. A14: no structural
adaptation authorized. A15: no hardware equivalence claimed. A05/A12/A13 are
unchanged. No ACP, architecture-contract or accepted semantic change.

| Procedure | Revision | Result |
|---|---|---|
| Fetch, branch, HEAD/origin-main, porcelain status | Reviewed baseline above | PASS, clean main equality |
| Source/ACP/contract and retained metadata inspection | Same baseline | Completed; readiness gaps identified |
| `Get-FileHash` against five handoff hashes | Same baseline | PASS, 5/5 |
| `ConvertFrom-Json` / parsed `streams` pair comparison | Same baseline | PASS, both retained pairs; not runtime replay |
| Scientific runners, benchmark/tuning/generators | N/A | NOT RUN |
| Python tests, compile and runtime interface fixtures | Same baseline | NOT RUN; no code changed |
| `git diff --check`, four-file ownership, frontmatter shape and workflow links | Governance draft | PASS; staged/publication checks repeated before commit/push and reported in final response |
| Editor Problems for all four changed Markdown files | Governance draft | PASS; no errors reported |
| Hardware validation/new efficacy validation | N/A | NOT RUN |

## Next assignment, publication and rollback

Only `.github/agents/luna-59.agent.md` is newly authorized, and only as a
documentation design prerequisite. It freezes two deliverables, eight logical
cases, two alternatives and zero executions. It contains an explicit
stop-on-missing-interface gate and requires authoritative publication before
assignment starts.

Owner/Luna-0 must resolve that design, any unavailable decision attachment,
task mapping/timing/scoring, no-training or accepted reward semantics,
independent generator/splits/population/repetitions, comparator/arms,
budgets and controls before authorizing efficacy execution. No integration
readiness or successor experiment is established.

Publication follows the existing main-branch governance pattern requested by
the owner: validate the four-file diff, commit, push, fetch, verify clean
`HEAD == origin/main`, then stop. The publication SHA is reported externally
to avoid a self-referential commit hash in its own content. Rollback, if
requested, reverts only this governance commit; all core, tests, runners and
scientific evidence remain untouched.
