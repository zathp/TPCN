# Luna-0 — Spiral and Simon Says Benchmark Resumption Handoff

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Spiral and Simon Says Benchmark Resumption"
  task_id: "luna-0-spiral-simon-resumption-20261011"
  component: "historical benchmark evidence, bounded experimental contracts, and governance"
  status: "blocked"
  contract_version: "1.2"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "f2ce64b1c514d6e2cf5fc9b741418e5c944da59a"
  result_revision: "uncommitted"
  dependencies: []
  owner: "project owner"
  classification: ["RESEARCH DESIGN", "GOVERNANCE", "INDEPENDENT REVIEW"]
  hypothesis: "A reviewed current-network Spiral design and recoverable Simon Says source can support independently bounded benchmark contracts."
  counter_hypothesis: "Missing task provenance, label-boundary defects, or unreviewable resource/instrumentation requirements block one or both contracts."
  interfaces_relied_on:
    - "current ExperimentRunner / EXCURSION_V1 path"
    - "external label/readout boundary"
    - "bounded event queue, topology, prediction, eligibility, and energy metrics"
  label_information_boundary:
    - "Spiral task labels must remain outside event input; neutral reward is required for every benchmark phase."
    - "Simon Says task and label semantics are not recovered."
  timing_assumptions:
    - "Spiral uses 16 ordered point events and explicit 120/240/480 time-unit schedules."
    - "Simon Says timing remains unknown until primary evidence is provided."
  reset_boundaries:
    - "Spiral resets character-scoped runtime state for every example and preserves only declared trained external readout/topology state."
  resource_bounds:
    - "Spiral budget is proposed only and requires owner approval plus a qualified external enforcement path."
    - "Simon Says budget is not specified because the task unit/semantics are unknown."
  authorized_scope:
    - "Repository inspection, research design, governance changes, and independent review only."
  unauthorized_scope:
    - "Any Spiral or Simon Says benchmark execution, training, scoring, or data generation."
    - "Structural-learning efficacy, production changes, architecture promotion, or Hyper-V qualification."
  controls:
    - "Preserve immutable Luna-12G historical evidence."
    - "Paired same-point opposite-order Spiral examples; matched shared-shuffle control; no-learning diagnostic."
    - "Simon Says lane remains separate and blocked on source evidence."
  measurements:
    - "Historical Spiral classification, per-class results, event/energy/connectivity evidence, limitations."
    - "Simon Says metrics unavailable in repository."
  information_boundary_check:
    - "Spiral runner has a label-conditioned evaluation-reward path unless reward_mode=neutral; the contract requires neutral."
  hardware_mapping:
    - "Software reference only; no equivalence claim."
  architecture_invariants_touched: ["A01-A04", "A06-A11", "A14", "A15"]
  preserves:
    - "A01-A15 and ACP status"
    - "Luna-12G artifacts/handoff"
    - "Luna-63C frozen records"
    - "Luna-64 blocked records and unused corrective allowance"
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-65.agent.md"
    - ".github/agents/luna-66.agent.md"
    - "workflow/docs/luna/LUNA_65_SPIRAL_RESUMPTION.md"
    - "workflow/docs/luna/LUNA_66_SIMON_SAYS_RECOVERY.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-spiral-simon-resumption-20261011.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All benchmark workloads, training, scoring, and data generation (prohibited)."
    - "No implementation, API unit tests, deterministic interface/capacity fixtures, or benchmark execution; none was authorized."
  assumptions:
    - "No external Simon Says primary source was supplied in this assignment."
  unresolved:
    - "Simon Says task definition, metrics, split, seeds, and implementation are absent from all examined repository refs."
    - "Owner approval of Spiral task-specific thresholds and proposed resource budget is pending."
    - "External CPU/wall/memory/artifact enforcement is unqualified."
    - "The additive public one-example API and typed runtime budget error are proposed but unimplemented and require exact owner authorization plus independent review."
    - "Full-replication E2 identity-counter sufficiency is not analytically established; bounded fixture checks cannot alone prove it."
    - "Exact owner authorization is still required separately for API implementation/unit tests, capacity fixtures, and any later benchmark execution."
  recommended_next_agent:
    - "Project owner to authorize the exact additive API and focused API unit-test scope, if desired; Luna-0 independently reviews implementation before fixture authorization."
    - "Luna-0 to review separately authorized deterministic capacity-fixture evidence and any full-replication identity-capacity argument."
    - "Project owner to supply Simon Says primary source or authorize a newly defined task explicitly."
```

## Outcome and baseline

**OBSERVED:** Repository baseline is `f2ce64b1c514d6e2cf5fc9b741418e5c944da59a`
on `governance/luna64-r4.3-freeze-20261010`, with clean worktree at start.
The canonical package root is `workflow/`, not the absent
`tpcn-luna-workflow/` path referenced by earlier notes. The architecture
contract is `workflow/ARCHITECTURE_CONTRACT.md`, version 1.2.

This handoff and its linked contracts are governance/design only. No benchmark
runner, workload, data generation, training, scoring, structural experiment,
or external supervisor was executed or changed.

## Historical Spiral evidence

**REPOSITORY-VERIFIED:** Luna-12G source was introduced in commit
`3b2b03208286eca57d86e1d83359b9e233074d32`; its result handoff reports
authorization 2026-09-27 and baseline `d605e5da6c728390abb5916029903133b6e0fbd8`.
The current source explicitly selects `TANH_LEGACY` in `run_controls()`; the
Luna-32 change at `a70c8cd6df7cdbb98ef11e7a76711e5ead918cb8` records that
this was a historical compatibility experiment, not current
`EXCURSION_V1` / ACP-0007 evidence.

Luna-12G's reported 0.53125 reconciles across fixed, structural, shuffled,
and reversal conditions. All four also report per-class accuracy
left=0.46875/right=0.59375 and the exact same confusion counts. Fixed
topology ended at one edge; structural ended at seven after 325 decisions,
12 additions and 8 prunes. This topology change did not change classification.
Structural energy proxy was higher and reported utility lower. Prediction loss
was 0.0 throughout and no-learning had no represented classes. These are
limitations, not evidence of success.

The 12G split was disjoint by sequence digest but had no validation set and
only one seed pair and one readout seed. Its historical point-order controls
kept labels under reversal, whereas the resumption contract defines the label
as directed winding and requires inversion under exact reversal. Thus the
historical equal scores establish no useful evidence of order dependence in
that runner, but do not determine the corrected reversed-label task outcome.
The fixed and structural conditions are a legacy/TANH comparison only.

Historical evidence SHA-256 at the current checkout:

| File | SHA-256 |
|---|---|
| `artifacts/spiral-handedness-12g/config.json` | `4E8E40AC6654AB8B8BC786ED5346B6BA5BC695BF669921ADFFBB54500648CA2B` |
| `artifacts/spiral-handedness-12g/summary.json` | `7D4AF5D8F762ADBF7CC6A0F912137FF47F632B66C594332A63B7FBA3509EA19` |
| `workflow/handoffs/spiral-handedness-temporal-classification-Luna-12G.md` | `F721F74426C357DBF024251641DEA031F87565BB6861B669A5BFA9D695341FF1` |

No historical artifacts were rewritten.

## Historical Simon Says evidence

**REPOSITORY-VERIFIED:** Case-insensitive searches of the tracked tree and
available Git history/refs found no Simon Says source, fixture, result,
handoff, dataset/split, seed, readout/training implementation, or metric.
No historical Simon Says metric can be reported. The delayed symbolic
sequence-memory design notes are not a Simon Says benchmark definition and
are not used to infer one.

**BLOCKER:** An owner-supplied primary task contract or exact original source
identity is required to recover semantics. Luna-66 is therefore only a
read-only recovery/design prerequisite. No Simon Says execution identity is
assigned until source recovery and independent review.

## Capability diagnosis

| Capability / limitation | Classification | Evidence and boundary |
|---|---|---|
| Temporal order discrimination | **VERIFIED limitation for historical Luna-12G; current efficacy untested** | Ordered/shuffled/reversal all 0.53125 in the historical TANH_LEGACY runner. The current E2 path is a separate model. |
| Timing sensitivity | **UNTESTED** | Historical generator jitter varied, but no matched delay-factor intervention or current-network task test was reported. |
| Prediction across delays | **UNTESTED / historical metric uninformative** | Historical prediction loss was 0.0. Current predictor supports bounded local timestamp matching, but the benchmark did not establish task-relevant delayed prediction. |
| Eligibility and delayed credit | **UNTESTED in Luna-12G** | Historical controls used default zero reward delay; they do not test delayed credit. |
| Bounded connectivity | **VERIFIED as a software-reference capability; not task efficacy** | `BoundedTopology` enforces edge, fan-in/out, positive delay limits; current experiment defaults are finite. |
| Early connection saturation | **UNTESTED** | Historical final 7/8 edge count does not establish when/why saturation occurred; per-example lifecycle series was not retained. |
| Useful fan-in formation | **UNTESTED; historical efficacy not demonstrated** | 12G reports no accuracy gain with topology changes and no causal useful-edge intervention. |
| Readout stability | **PARTIALLY VERIFIED determinism; statistical stability untested** | Same-seed results/replay are deterministic; only one run seed, and the scalar external prototype readout has no multi-seed stability evidence. |
| Train/evaluation leakage | **PARTIALLY VERIFIED** | 12G reported disjoint sequence digests and label-relabel isolation. There was no validation split. Current E2 runner can send label-conditioned reward during evaluation unless `reward_mode="neutral"`; Luna-65 makes neutral reward mandatory. |
| Current feature bottleneck | **VERIFIED representation; suspected limitation** | The current E2 experiment adapter feeds `x + y` for each point and scores an aggregate scalar event feature. Whether that lossy projection erases direction or task-relevant spatial distinctions is untested; Luna-65 must retain it rather than silently replace it. |
| Historical/current mechanism difference | **VERIFIED** | Historical controls explicitly use `TANH_LEGACY`; current `ExperimentConfig` defaults to `EXCURSION_V1`, and ACP-0007 structural growth has distinct required observation/policy settings. |

No claim is made that current structural plasticity improves learning.

## Proposed Luna identities and independent lanes

- **Luna-65 — Spiral Current-Network Resumption:** fixed-topology
  `EXCURSION_V1` efficacy test, proposed in
  `workflow/docs/luna/LUNA_65_SPIRAL_RESUMPTION.md`. It is not execution
  authorization. Structural plasticity is explicitly excluded.
- **Luna-66 — Simon Says Historical Recovery and Contract Prerequisite:**
  read-only recovery/design only, proposed in
  `workflow/docs/luna/LUNA_66_SIMON_SAYS_RECOVERY.md`. It cannot execute the
  benchmark or invent missing semantics.
- **Simon Says execution identity:** deliberately unassigned pending original
  task/source recovery and Luna-0 independent contract review. Luna-64's
  unused corrective allowance is not borrowed.

The lanes have independent primary metrics, thresholds, seeds, splits, and
evidence. They may share only read-only inspection and already-approved
downstream diagnostic interfaces. No cross-lane pooled result or model
selection is permitted.

## Shared diagnostic contract

Luna-65 reports currently public metrics and trace-derived values only:
emission/activation/event counts, prediction match/unmatched/error/expiry,
queue occupancy and completion, energy-proxy components, graph edges/capacity
and aggregate fan utilization, readout diagnostics, and deterministic replay
digest. It explicitly marks unexposed prediction admissions, per-example
eligibility creation/expiry, per-edge usage on this runner path, and
source/intermediate/destination breakdowns as unavailable unless the current
bounded trace already supports them.

Any observer extension must be a separately reviewed downstream-only change
with bounded storage and evidence of exact on/off computational equality.
No production or neural behavior change is authorized by this governance
task.

## Budgets and exact authorization boundary

The Luna-65 proposal specifies eight fixed seeds, bounded synthetic examples,
20 epochs, per-example event/queue caps, zero retries, an 8 MiB/seed and
64 MiB aggregate artifact target, and proposed CPU/wall/memory ceilings.
Host CPU, wall, memory, and artifact enforcement is unqualified and is not
claimed by this handoff. No Hyper-V supervisor prerequisite is introduced.
The command is a future CLI requirement because `run_spiral_resumption.py`
does not exist at baseline.

Simon Says has a **zero-workload budget** for this stage: zero benchmark runs,
examples, training, compute, and artifacts. No future sample count, command,
or seed is assigned because original task-unit and duration data are absent.

## Initial independent review and verdict — before interface-plan addendum

Three independent read-only reviews were completed against the initial draft,
followed by one narrow read-only verification of the documented corrections.
No benchmark, code, or test execution was performed.

| Review scope | Independent finding | Disposition |
|---|---|---|
| Historical provenance | Luna-12G results and the `TANH_LEGACY` versus current `EXCURSION_V1` distinction are correctly separated; Simon Says primary evidence and historical metrics are absent. | Historical record retained; Simon Says remains blocked. |
| Spiral science, leakage, and generalization | Flagged the shared-shuffle control's identical-input interpretation, the proposed effect-size threshold, and the need to make timing and validation analyses explicitly secondary and non-adaptive. | Follow-up review confirmed these corrections: shared-shuffle is an information-boundary negative control; the `0.05` effect requires owner acceptance; the paired hierarchical bootstrap, fixed 1.0 primary timing factor, and reporting-only validation/timing diagnostics are explicit. |
| Architecture, resources, and authorization | **BLOCKED** on workload-index-dependent input-node assignment, persistent identity-counter limits across resets, and missing per-example fail-fast completion/capacity handling. Scope exclusions and track separation were otherwise preserved. | At that review point, matched workload positions, equivalent pair-state requirements, and persistent E2 identity ceilings were documented. Existing aggregate `evaluate()`/`train()` calls could not implement per-example stop. The following interface addendum resolves the design choice only; no implementation or benchmark execution is authorized. |
| Corrected-contract verification | **BLOCKED only on fail-fast execution support** at the time of the initial review. | Initial review recommended a separate Luna-0 interface decision; the later Luna-65 interface-plan review below evaluates that proposed path. |

**Integrated verdict: BLOCKED — BENCHMARK RESUMPTION CONTRACTS INCOMPLETE.**
The science/architecture corrections are documentary requirements, not
evidence that the current runner satisfies them. Luna-65 remains blocked on
resolution of the fail-fast interface gap, evidence of identity-capacity
sufficiency, owner acceptance of task-specific criteria and resource limits,
and qualified external enforcement. The current runner cannot satisfy the
first-failure stop rule as an aggregate call. Simon Says remains blocked on
owner-supplied primary evidence. No execution is authorized.

## Architecture and behavior preservation

No architecture contract clause or ACP status changed. A01-A04, A06-A11,
A14, and A15 are discussed only as experiment constraints; no invariant is
redefined. Production code, Luna-63C frozen records, Luna-64 blocked records,
and the unused Luna-64 allowance remain untouched. Software-only design;
hardware equivalence is not claimed.

## Validation and publication

| Check | Result |
|---|---|
| Repository baseline/status | Verified at `f2ce64b1c514d6e2cf5fc9b741418e5c944da59a`; clean at start |
| Historical source/artifact inspection | Performed read-only; identities above |
| Simon Says tree/history search | No source or result found |
| Benchmark execution | Not run; prohibited by assignment |
| Initial independent reviews | Three performed; findings recorded |
| Follow-up review of initial corrections | Performed; aggregate runner path remained insufficient |
| Final Luna-65 interface-plan review | **PASS — LUNA-65 INTERFACE PLAN READY FOR OWNER AUTHORIZATION**; authorization boundary confirmed; no implementation/fixture permission |
| Governance file validation | CRLF-aware `git diff --check` passed; no tests or fixtures were run |
| Initial draft checkout SHA-256 | Captured for the initial six-file package below; values are historical after the current interface review |
| Current interface-review SHA-256 | Recorded for current working-tree package bytes below; no staged or publication identity |
| Staged bytes | None staged; no staged-byte identity applies |
| Commit and remote publication | Not performed; HEAD remains the baseline and the remote branch is unchanged |

Historical SHA-256 identities below identify the working-tree bytes in the
initial governance report; they are not current after the interface-plan
updates. The handoff was excluded to avoid a self-referential digest. These
historical values are not staged, committed, or published identities.

| File | SHA-256 |
|---|---|
| `.github/agents/luna-65.agent.md` | `BAEEFBA64B7A974C51CBF6D137451825E17712DFAD69AE07292A798710EF5BC6` |
| `.github/agents/luna-66.agent.md` | `03A2C72764096B48D1AB3E6189B971568AAA33A94AF047FD82670EF40BF83675` |
| `workflow/docs/luna/LUNA_65_SPIRAL_RESUMPTION.md` | `7281368FF5CF29B415290EFFC3EFF34496C770A8861F3EE62F4B4C12C8B674A3` |
| `workflow/docs/luna/LUNA_66_SIMON_SAYS_RECOVERY.md` | `842C49765DD0FBB90F4BB634FD3F245DABA134C92CD5B8533A85216971E4C8E8` |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `94E10977B1B91791B779184184BEA4D04AE2DC47582D41533C9486678CA1D230` |
| `workflow/ARCHITECTURE_CHANGELOG.md` | `AEDC07AA8FA3EA1847C798988E0568B4E2D1CAAA19532DEEB3F4808C3CB47E1B` |

Current interface-review SHA-256 identities below identify only the latest
working-tree bytes of the listed allowlisted documents. The handoff is
excluded to avoid a self-referential digest. No bytes are staged, committed,
or published.

| File | SHA-256 |
|---|---|
| `.github/agents/luna-65.agent.md` | `C8BA8CD113F8754B2F0187760F0891A97D4FB306BD751DB6EDB555F188E3164B` |
| `.github/agents/luna-66.agent.md` | `03A2C72764096B48D1AB3E6189B971568AAA33A94AF047FD82670EF40BF83675` |
| `workflow/docs/luna/LUNA_65_SPIRAL_RESUMPTION.md` | `1F1D4DD96E21EE760D32CDDE4F0415576C9BAE6AF01B82DB2A9C4E1D9FB5C777` |
| `workflow/docs/luna/LUNA_66_SIMON_SAYS_RECOVERY.md` | `842C49765DD0FBB90F4BB634FD3F245DABA134C92CD5B8533A85216971E4C8E8` |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `8ACB3F2E374F238931EAF04800BFC75A367E2723D484A75613B97A9D6F1EF0A4` |
| `workflow/ARCHITECTURE_CHANGELOG.md` | `0F009383E927DB9D9DAE863C83EA0D302918D994E2B870E7A739313FAAD5E82A` |

## Exact owner authorization needed

**Spiral API implementation/unit tests (first separate authorization):**
authorize only the additive `ExperimentRunner.execute_example()` result/API
in `tpcn/experiments.py`, the dedicated
`RuntimeEventBudgetExceeded` type in
`tpcn/experiment_excursion_runtime.py`, and
`tests/test_luna65_execute_example.py`. Name the exact reviewed contract and
baseline. This permits at most 16 two-point test calls with artificial
placeholder labels, neutral reward, and no `train()`, benchmark data,
scoring, or efficacy run. It does not permit direct private-hook adapters,
capacity fixtures, benchmark generation, or production behavior changes.
Per-process test ceilings are 2 minutes wall time, 2 CPU-minutes, 256 MiB,
1 MiB artifacts, and zero retries; enforcement is not yet qualified.
Luna-0 must review the implementation/tests before the next stage.

**Spiral capacity fixtures (second, separate authorization):** after that
review, authorize only `tests/test_luna65_capacity_fixture.py`, with the
exact contract/baseline, 2-minute wall limit, 2 CPU-minute limit, 256 MiB
memory limit, 1 MiB artifact limit, and zero retries. Its direct-counter lane is capped at
8,196 allocation attempts; its network lane is scheduled for eight seeds ×
16 hand-authored characters (128 maximum), at most 131,072 processed events
and 2,048 external inputs, stopping early at unexpected exhaustion. It
permits no Spiral data, task labels, readout updates, benchmark training, or
scoring. A fixture pass does not itself prove full-replication identity
sufficiency.

**Spiral benchmark (third, distinct exact authorization, not currently
ready):** only after an independently reviewed full-replication capacity
argument, accepted interface/fixture evidence, approved task criteria,
reviewed CLI/metrics, and qualified resource enforcement, the owner must
authorize the exact contract hash, baseline, command, eight seeds, resource
caps/enforcement, neutral-reward label boundary, artifact destination, and
0.50 / 0.05 interpretation criteria. No structural-learning condition,
repeats, or production promotion is implied. Benchmark execution is not
authorized by this handoff.

**Simon Says:** the owner must first provide the original task contract or
exact primary-source revision/path and historical artifacts needed to recover
the actual metrics. Luna-66 then prepares a separate design for independent
Luna-0 review. A later, separate exact owner authorization must name the
reviewed execution contract, command, split/seed, sample count, resource
budget, and outputs. No Simon Says run is authorized now.

## Next bounded assignment

Await the project owner's exact decision on the separate API/unit-test
authorization above. If authorized and completed, Luna-0 reviews it before
the bounded fixture authorization. No benchmark workload is the next step.
To proceed with Simon Says, the owner must provide its original task contract
or primary-source revision/path and historical artifacts.

## Luna-65 interface-plan review addendum — 2026-10-12

### Scope and baseline

This addendum records a governance-only review against baseline
`f2ce64b1c514d6e2cf5fc9b741418e5c944da59a`. The scope was the Luna-65 runner
interface, persistent E2 identity capacity, the existing Spiral scientific
controls, and the exact owner authorization boundary. No code, tests,
fixtures, benchmark examples, training, scoring, data generation, commit, or
publication was performed. Earlier uncommitted benchmark contracts, handoffs,
workflow updates, and historical evidence were preserved.

### Runner options and selected plan

**OBSERVED:** `ExperimentRunner.evaluate()` and `.train()` are aggregate
workload APIs. They do not expose a public indexed single-example operation
with per-example completion/failure and all-node identity snapshots. One
runner does preserve topology, network, and learned readout state across
examples; character reset preserves persistent E2 identity high-water
counters. Full runner reset would rebuild/clear that state. Incomplete
settling can be returned as a result while the aggregate pass continues.

**Option A (existing public APIs): rejected.** Aggregate calls do not support
the required stop-before-next-example boundary or per-example status.

**Option B (downstream adapter): technically possible, not selected.** A
subclass/direct adapter could use private `_ensure_topology`,
`_run_example`, `_ExampleRun`, and network state. It would bypass
`_execute()`'s aggregation and `last_neurons` refresh, require its own metric
aggregation, and need private access for all-node identity snapshots. Pinning
the baseline does not turn those private interfaces into supported APIs.

**Option C (selected proposal, not implemented):** add
`ExperimentRunner.execute_example(example, *, index, update=False)` and an
immutable typed result in `tpcn/experiments.py`. It must execute exactly one
example with the original row index, preserve the same runner/network/
topology/readout and identity counters, expose completion/failure and
per-neuron identity snapshots, and commit a readout update only after a
successful complete execution. Reuse public `neuron_to_ir2_e2()` for
all-node identity high-water/capacity records. Add a dedicated
`RuntimeEventBudgetExceeded` type in
`tpcn/experiment_excursion_runtime.py` in place of the existing untyped
event-budget error; report expected capacity failures explicitly while
allowing unexpected exceptions to remain visible. A failed example stops
the adapter and invalidates the complete replication; there is no rollback
or retry.

The adapter aggregates streamed per-example results without claiming
`TrainingObserver`/`TrainingResult` behavior. Existing `evaluate()` and
`train()` behavior remains unchanged. Exact API success/failure semantics,
readout commit parity, runtime cleanup, and deterministic replay must pass
focused tests before fixture verification.

### Capacity finding and bounded fixture proposal

**OBSERVED:** each E2 identity counter has a 2,048 per-neuron ceiling under
the current `E1Config.event_budget`, and input, episode, lineage, and
output-event high-water identities persist across character reset. Runtime
point admissions use explicit IDs and do not consume the neuron's fallback
input-ID counter. Ordinary/multi-excursion admission, multi-to-ordinary
transition, new lineage, and emission consume the applicable episode,
lineage, and output-event counters.

**INFERRED:** the complete replication allowance is 4,259,840 processed
events over 4,160 example executions per seed. Current evidence does not
establish a tighter per-neuron/per-counter upper bound below 2,048.
Therefore, full-replication identity sufficiency is **not established**;
typical or average usage cannot substitute for a bound.

The contract now separates two future, separately owner-authorized test
stages:

1. `pytest -q tests/test_luna65_execute_example.py`: at most 16
   hand-authored, two-point API calls with artificial label tokens, used only
   to verify prototype sum/count update parity, no update on failed calls,
   result/error typing, cleanup, exact index routing, state continuity and
   replay. Neutral reward is mandatory; no `train()` call, Spiral data,
   task-label scoring, accuracy, or efficacy is involved.
2. `pytest -q tests/test_luna65_capacity_fixture.py`: direct-neuron identity
   tests are bounded to 2,049 allocation attempts for each of four counters
   (8,196 total), including fallback input-ID allocation without an explicit
   ID. The separate network-level check is scheduled at eight seeds × 16
   hand-authored characters (128 maximum), at most 16 external inputs per
   character, queue capacity 128, and 1,024 processed events per character:
   131,072 maximum network events and 2,048 external inputs. Runtime
   external IDs are explicit, so the network-level fixture must verify that
   the fallback input-ID counter does not advance.

Each invocation has proposed ceilings of 2 minutes wall time, 2 CPU-minutes,
256 MiB, 1 MiB of artifacts, and zero retries; these are not yet qualified
enforcement. Predeclared negative unit-test cases may continue only after
asserting exact failure kind, cleanup, counter persistence, and no readout
update. Unexpected exceptions or failures stop the test process; any
network-level capacity exhaustion stops that network check and leaves later
scheduled examples unexecuted. These fixtures can identify tested
exhaustion but cannot alone prove full-replication sufficiency. Benchmark
execution remains blocked absent a separately reviewed capacity argument.

### Scientific contract and independent review

No Spiral experimental conditions changed: fixed-topology
`EXCURSION_V1`; matched forward/reverse sequences; disjoint train, validation,
and test splits; eight fixed seeds; neutral reward; frozen test readout;
primary timing 1.0; secondary timing 0.5 and 2.0; no structural-plasticity
efficacy claim. Training arithmetic remains 22 passes (pre-evaluation, 20
training epochs, post-evaluation), yielding 4,160 sequence executions and a
4,259,840 processed-event allowance per replication. Luna-12G remains a
separate historical `TANH_LEGACY` baseline.

**Independent Luna-11 review:** confirmed that a private-call Option B
adapter is not the lowest-risk choice, because it needs private initialization,
aggregation, and all-node state access. It recommends additive public Option
C, while noting that its exact API must reconcile validation, continuity,
incomplete-result/update semantics, aggregation/observer behavior, and the
22-pass schedule. A subsequent pass identified ambiguities around test
labels/readout scope, expected versus unexpected capacity failures, and
fallback input IDs versus explicit runtime IDs. The contract now separates
the artificial-label API unit tests from the non-updating capacity fixtures,
defines test-stop behavior, and isolates direct fallback-ID tests from
explicit-ID network fixtures. It also bounds the network fixture to 128
scheduled characters and reports any skipped after failure. Final
independent re-review of these documentary corrections is pending.

### Current authorization boundary and next work

The owner must separately authorize (1) only the additive API and focused
API unit tests in `tpcn/experiments.py`,
`tpcn/experiment_excursion_runtime.py`, and the named focused tests; then,
after Luna-0 review, (2) the bounded deterministic identity/capacity fixture
checks. The first scope includes at most 16 artificial-label calls and does
not permit benchmark training; the second uses no task labels or readout
updates. Neither authorization permits Spiral benchmark data generation,
benchmark examples, training, scoring, or a full run. Benchmark execution
requires another exact owner authorization after reviewed capacity reasoning,
interface and replay evidence, CLI/metrics review, and qualified resource
enforcement. No counter-reset, capacity increase, network reconstruction,
retry, topology change, structural-learning condition, or production
promotion is implied.

The authoritative workflow, changelog, and Luna-65 role contract have been
updated to reflect the proposed Option C path and remaining capacity
uncertainty. No architecture clause or ACP changes. The final targeted
independent Luna-11 review found no remaining documentary mismatch and
returned **PASS — LUNA-65 INTERFACE PLAN READY FOR OWNER AUTHORIZATION**. This
is not permission to implement the API or run fixtures. Full-replication
identity sufficiency remains unresolved; benchmark execution remains
unauthorized, and the broader Spiral/Simon benchmark resumption remains
**BLOCKED**.
