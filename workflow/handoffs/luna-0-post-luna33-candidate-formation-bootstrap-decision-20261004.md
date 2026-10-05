---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Post-Luna-33 candidate-formation root cause and Luna-34 authorization"
  task_id: "luna-0-post-luna33-candidate-formation-bootstrap-decision-20261004"
  component: "ACP-0007 zero-candidate root cause and downstream-emission bootstrap"
  status: "PASS — ROOT CAUSE CLASSIFIED; LUNA-34 AUTHORIZED / NOT EXECUTED"
  contract_version: "1.2"
  branch: "main"
  base_revision: "1e2f80aa9e37b332e0637f6ff8b0df18d5f2ceb6"
  result_revision: "governance publication containing this handoff"
  dependencies:
    - "Luna-33 independent closure at 1e2f80aa9e37b332e0637f6ff8b0df18d5f2ceb6"
    - "Accepted ACP-0007"
  owner: "Luna-0 Architecture Guardian"
  classification: ["OBSERVATION", "INDEPENDENT VERIFICATION", "GOVERNANCE DECISION"]
  hypothesis: "Luna-33 emitted only at its designated input node, so character-local emission-based ACP-0007 evidence had no legal distinct source/neighbor pair despite routed downstream receipt."
  counter_hypothesis: "An independently observed downstream canonical emitter or candidate would falsify the bootstrap diagnosis and block successor authorization."
  interfaces_relied_on:
    - "ExperimentRunner public training metrics and StructuralDecision evidence"
    - "StructuralObservationPlane / TemporalAssociationPolicy"
    - "MultiExcursionNeuron / E1Config"
    - "ExcursionCharacterRuntime and public event trace"
    - "Edge / BoundedTopology.from_edges() / route()"
    - "SpiralConfig and make_spiral_dataset()"
  label_information_boundary:
    - "Luna-33 audit uses labels only as existing external experiment metadata; structural evidence is actual emissions only."
    - "Authorized Luna-34 must use point streams only, must not read/use labels or correctness, and must not calculate efficacy outcomes."
  timing_assumptions:
    - "Canonical logical timestamps, positive route delay, and ACP-0007 strict 0 < dt <= 4.0."
    - "No global neural timestep or cross-character evidence lifecycle."
  reset_boundaries:
    - "ACP-0007 evidence and E2 neuron state are character-local and reset/destroyed at character end."
    - "Luna-34 must construct fresh per-character evidence and neutral neuron state."
  resource_bounds:
    - "Luna-33 used 8 nodes, 2 initial edges, capacity 16, fan-in/out 2/2, history 8, candidates 4, score 3, event budget 1024."
    - "Luna-34 is limited to two nodes and a direct one-hop static topology with explicit finite queue/event/evidence bounds."
  authorized_scope:
    - "Independently inspect Luna-33 result decisions, runtime metrics, canonical transfer equations and public APIs."
    - "Create the bounded Luna-34 mechanism-only dispatch and publish this decision."
  unauthorized_scope:
    - "No production code, tests, artifacts, ACP-0007, Architecture Contract, or historical findings changed."
    - "No new task-efficacy experiment, accuracy tuning, cross-character evidence, reception-as-emission, pruning, N3, or hardware claim."
  controls:
    - "Luna-33 C and D per-character structural decisions"
    - "No-edge control for the authorized future mechanism experiment"
    - "Default static N2 edge and one predeclared |w|=2 static-bound sensitivity condition"
  measurements:
    - "64 C and D decisions per seed; status/rejection/candidate/attempt/admission reconciliation"
    - "Distinct canonical emitter identities per character and designated input identity"
    - "Receiving/emitting metrics, route depth, edge-transfer proxy"
    - "Default E1 threshold and accepted static Model-B single-transfer bounds"
  information_boundary_check:
    - "Candidate proof is limited to actual canonical emissions; routed receipt and duplicate observer records are not counted as emitters."
  hardware_mapping:
    - "Software-reference mechanism diagnostic only; no hardware mapping/equivalence established."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A10", "A14", "A15"]
  preserves: ["Architecture Contract 1.2 / A01-A15", "accepted ACP-0007", "Luna-33 scientific verdict", "historical Luna-12L and Luna-13F findings"]
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-34.agent.md"
    - "workflow/handoffs/luna-0-post-luna33-candidate-formation-bootstrap-decision-20261004.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Full suite: 920 passed, 0 failed, 1 unchanged CUDA-unavailable skip."
    - "Test collection: 921 tests collected."
    - "Programmatic audit of every C/D training StructuralDecision across all five seeds."
    - "Luna-33 candidate/emitter/metric reconciliation and input-neuron identity assertions."
    - "Default and maximum accepted signal-only Model-B transfer inequalities evaluated."
    - "Starting revision/branch/origin/worktree preconditions passed."
  tests_failed: []
  tests_not_run:
    - "Luna-34 mechanism experiment: authorized but not executed."
    - "Hardware, prediction/resource benefit, and task efficacy: out of scope/not run."
  assumptions:
    - "The published ordered train examples map to ExperimentRunner indices in stored order."
    - "Character-local bounded emission observations faithfully implement the accepted ACP-0007 policy inspected in source."
  unresolved:
    - "Whether repeated routed contributions accumulate sufficiently to cause a downstream emitter under the default edge remains for Luna-34."
    - "Whether the fixed |w|=2 static-bound sensitivity condition creates a bridge remains for Luna-34."
  recommended_next_agent: ["Luna-34 EXCURSION_V1 Multi-Emitter Candidate-Formation Bridge"]
---

# Decision and terminal verdict

**PASS — ACP-0007 CANDIDATE-FORMATION BOOTSTRAP CLASSIFIED;
LUNA-34 AUTHORIZED / NOT EXECUTED.**

Luna-33 is **CLOSED / INDEPENDENTLY VERIFIED**. Its joint H1 remains
**NOT SUPPORTED IN THIS SETUP**. A/B observation non-interference is
**ESTABLISHED**; structural observation was **ENGAGED**, but candidate
formation was **NOT ENGAGED**. Growth attempts and admissions were both zero.
The effect of successfully engaged ACP-0007 growth and its temporal
specificity remain **NOT ESTABLISHED**. Historical Luna-12L and Luna-13F
remain **NOT SUPPORTED / UNCHANGED**. ACP-0007 remains **ACCEPTED /
UNCHANGED**. E2 pruning and N3 remain **NOT AUTHORIZED**.

This review classifies the cause as:

> **WITHIN-CHARACTER MULTI-EMITTER / PROPAGATION-TO-EMISSION BOOTSTRAP GAP**

It is not a candidate-ranking, candidate-capacity, growth-controller,
reporting, or task-accuracy-only failure. No production defect was identified.

## Starting revision, authority, and scope

The review started at clean synchronized `main`:

```text
branch = main
HEAD = origin/main = 1e2f80aa9e37b332e0637f6ff8b0df18d5f2ceb6
subject = docs: close Luna-33 ACP-0007 efficacy experiment
worktree = clean
```

The full regression baseline was independently run at this revision:
`920 passed, 0 failed, 1 skipped`; the unchanged skip is CUDA unavailability
at `tests/test_gpu_visualization.py:61`. Collection reported `921 tests
collected`. The repository Architecture Contract 1.2, ACP-0007, acceptance
criteria, workflow, Luna-33 dispatch/handoffs, configuration, summary, and
runtime/API sources named by the task were read. The large `results.json`
was inspected programmatically, not inferred from its summary.

This decision changes only governance/dispatch documentation. It does not
change production code, tests, Luna-33 artifacts, ACP-0007, Architecture
Contract 1.2, or historical evidence. No ACP is required for the bounded
mechanism experiment because it exercises the already accepted actual-
emission evidence contract and static N2 transfer parameters without
changing architecture.

## Luna-33 decision-level reconciliation

For every C and D seed, the independent programmatic audit read all 64
training `StructuralDecision` records and deduplicated canonical observations
by actual `(emitter_id, event_id)`. It reconciled decision status, candidate
rejections, candidate contents, growth attempts, admissions, and aggregate
metrics.

| Seed | Condition | Decisions | `no_candidate` | Candidate rejections | Retained candidates | Attempts | Admissions |
|---:|:---:|---:|---:|---:|---:|---:|---:|
| 0 | C / D | 64 each | 64 each | 0 | 0 | 0 | 0 |
| 1 | C / D | 64 each | 64 each | 0 | 0 | 0 | 0 |
| 2 | C / D | 64 each | 64 each | 0 | 0 | 0 | 0 |
| 3 | C / D | 64 each | 64 each | 0 | 0 | 0 | 0 |
| 4 | C / D | 64 each | 64 each | 0 | 0 | 0 | 0 |

Every one of the 640 C/D decision records has an empty candidate list,
`candidate_rejections == 0`, `growth_attempted == false`, and no admission.
The summary's zero candidate-opportunity result reconciles with every
decision; this is not a candidate-ranking or reporting discrepancy.

## Distinct emitters and input identity

Multiple observation-plane recipients of one canonical emission were
deduplicated and never counted as separate emitters. The emitter population
and input-neuron mapping independently reproduce the dispatch's expected
pattern:

| Seed | Canonical emissions / observation work (C and D) | Emitting characters | Silent characters | Characters with 2+ distinct emitters | Sole emitter matches designated input |
|---:|---:|---:|---:|---:|---:|
| 0 | 338 / 676 | 59 | 5 | 0 | 59 / 59 |
| 1 | 361 / 722 | 59 | 5 | 0 | 59 / 59 |
| 2 | 306 / 612 | 59 | 5 | 0 | 59 / 59 |
| 3 | 314 / 628 | 59 | 5 | 0 | 59 / 59 |
| 4 | 396 / 792 | 61 | 3 | 0 | 61 / 61 |

No emitting character contained a downstream emitter or an input/emitter
mismatch. For each seed and both C and D, the independently counted
emitting characters equal `ExperimentMetrics.emitting_neuron_count`:
59, 59, 59, 59, and 61. The check deduplicated by event identity and emitter
identity rather than counting duplicate observation-plane recipient rows.
The structural emission totals equal the public metrics, and observation
work is exactly twice the canonical emission total, as expected for the
declared one-successor ring (emitter self-observation plus one reverse
observer). This is direct evidence that the observation plane was active;
these duplicate recipient rows are not counted as distinct emitters.

## Routed reception without downstream emission

`ExcursionCharacterRuntime.end_character()` computes
`receiving_neuron_count` as the number of network neurons with
`processed_event_count > 0` for that character, and
`emitting_neuron_count` as the count of distinct sources in the character's
canonical emission list. `ExperimentRunner._execute()` sums those per-
character values into `ExperimentMetrics`.

The published C training metrics independently report:

| Seed | Receiving-neuron total | Minus 64 source-input neurons | Emitting-neuron total | Prediction errors | Maximum route depth | Edge-transfer proxy |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 79 | 15 | 59 | 0 | 1 | 26.033424 |
| 1 | 78 | 14 | 59 | 0 | 1 | 28.151116 |
| 2 | 80 | 16 | 59 | 0 | 1 | 34.870585 |
| 3 | 79 | 15 | 59 | 0 | 1 | 31.876247 |
| 4 | 80 | 16 | 61 | 0 | 1 | 40.142440 |

Every one of the 64 training characters receives external points at exactly
one designated input neuron, so the no-propagation lower bound for
`receiving_neuron_count` is 64. The observed aggregate exceeds that bound by
14-16 neuron-character receives. All prediction-error counts are zero, so
these additional processed neurons cannot be attributed to routed
prediction-error events. Maximum route depth is one and edge-transfer proxy
is positive in every seed. Together with the inspected runtime, these
independently establish delayed downstream routed/delivered activity, while
the distinct-emitter audit establishes that no downstream canonical
excursion emits.

```text
ROUTED / DELIVERED DOWNSTREAM ACTIVITY: PRESENT
DOWNSTREAM CANONICAL EMISSION: ABSENT
```

The aggregate does not identify which individual destination received an
event; it establishes downstream processing at network level, not a
per-destination event-count distribution.

## Candidate impossibility proof and root-cause alternatives

ACP-0007's accepted candidate rule requires a canonical emission from source
`s` at `t_s`, followed by an actual emission from distinct declared neighbor
`d` at `t_d`, in the same character, with `0 < t_d - t_s <= 4.0`.
Character-local histories reset between characters.

**Observed:** every emitting Luna-33 training character has exactly one
distinct emitter, its designated input neuron. Duplicate observations at the
emitter and reverse observer do not create another actual emitter.

**Inferred:** with no second distinct emitter in any character, no legal
`s -> d` temporal pair can exist, regardless of ring orientation,
association-window size, candidate capacity, score/ranking, or growth budget.
This proof is specific to the observed emission population and the
ACP-0007 actual-emission/character-reset contract; it does not claim a
universal architecture impossibility.

| Proposed explanation | Classification | Evidence |
|---|---|---|
| A. Observation-plane defect | Not supported | Hundreds of canonical emissions produce matching structural observation totals; ring fan-out work reconciles. |
| B. Neighbor-map mismatch | Not causal here | The declared static ring is explicit and bounded, but no second emitter exists to be accepted/rejected as a neighbor. |
| C. Association-window mismatch | Not causal here | No pair of distinct emitters exists; interval cannot be the limiting predicate. |
| D. Single-emitter-per-character activity | Established | Exact counts above; all emitting characters have one emitter only. |
| E. Routed reception without downstream emission | Established as bridge state | Route depth 1 and positive transfer with zero downstream emitters. |
| F. Candidate aggregation/reporting defect | Not supported | All decisions, zero rejections, empty candidate lists, counters, and metrics reconcile. |
| G. Other mechanism defect | Not identified | Existing observations agree with the accepted source-local policy. |

Therefore:

```text
Luna-33 ring orientation: NOT THE ROOT CAUSE OF ZERO CANDIDATES
association_window=4.0: NOT THE ROOT CAUSE OF ZERO CANDIDATES
```

Do not authorize a ring-direction/window sweep to force candidates. Do not
reinterpret reception as emission or carry evidence across characters; either
would change accepted ACP-0007 semantics and require a separate architecture
decision/proposal.

## Canonical transfer and threshold bound

Source inspection confirmed:

- default `E1Config.theta_e` / `theta_E` is `1.0`;
- ordinary and M excursion payload magnitude is bounded by `a_max=1.0`;
- `Edge` defaults to `edge_weight=1.0`, `divider_strength=1.0`,
  `reference=0.0`;
- accepted static Model-B bounds are `edge_weight in [-2, 2]`,
  `divider_strength in [0, 1]`, and `reference in [-1, 1]`;
- `BoundedTopology.route()` transforms numeric `signal`/`excursion` payloads
  by `d * tanh(w * payload) + (1-d) * reference`.

For the default signal-only edge, `|v| <= tanh(1) =
0.7615941559557649 < theta_E`. For any signal-only edge within the accepted
static weight bound, `|v| <= tanh(2) = 0.9640275800758169 < theta_E`.
Thus a single ordinary routed payload from neutral state cannot alone
trigger a downstream ordinary excursion, including at the strongest allowed
signal-only static weight.

```text
DOWNSTREAM EMISSION REQUIRES:
temporal accumulation of multiple routed contributions and/or non-neutral
prior state under the default Model-B path
```

This is an architectural transfer/integration property, not a defect by
itself. Luna-34 starts all neurons neutral and tests within-character temporal
accumulation only. It must not configure biased reference, altered divider,
or non-neutral initial state.

## Initializer disposition

`ExperimentRunner._ensure_topology()` and `BoundedTopology.seeded()` use the
same sorted directed-pair candidate set, `random.Random(seed)` shuffle, and
bounded `connect()` selection for a feasible requested initial edge count.
For the corrected Luna-33 settings, the recorded two-edge public topologies
are valid and A-D matched per seed. The helper's declared capacity metadata
differs (`seeded()` sets edge capacity to requested `edge_count`, whereas the
runner retains its configured capacity 16), but this did not create a
neighbor-map mismatch or the zero-candidate result. It is not a cause and
does not warrant an unrelated initializer correction in this task. The
authorized Luna-34 explicitly builds its one-edge/no-edge controls with
`BoundedTopology.from_edges()` to avoid random initialization as a confound.

## Luna-34 authorization

**Existing public APIs suffice.** `MultiExcursionNeuron` accepts ordinary
public input events; `ExcursionCharacterRuntime` admits timestamped external
values, executes delayed `BoundedTopology` routes, reports bounded event
traces/counters, and offers a public canonical-emission observer callback.
`StructuralObservationPlane.observe_emission()` and `freeze()` consume actual
emissions and expose bounded candidate evidence. `SpiralConfig` and
`make_spiral_dataset()` provide deterministic point streams. No change to
`ExperimentRunner`, initialization, evidence lifecycle, reception semantics,
thresholds, or APIs is needed to determine whether the bridge occurs.

```text
Luna-34 title:
Luna-34 — EXCURSION_V1 Multi-Emitter Candidate-Formation Bridge

classification:
MECHANISM EXPERIMENT + OBSERVATION + CAUSAL DIAGNOSTIC

contract path:
.github/agents/luna-34.agent.md

Luna-34 status:
AUTHORIZED / NOT EXECUTED

owned files:
run_luna34_excursion_v1_multi_emitter_bridge.py
tests/test_luna34_excursion_v1_multi_emitter_bridge.py
artifacts/acp0007-luna34-multi-emitter-bridge/config.json
artifacts/acp0007-luna34-multi-emitter-bridge/results.json
artifacts/acp0007-luna34-multi-emitter-bridge/summary.json
workflow/handoffs/luna-34-excursion-v1-multi-emitter-candidate-formation-bridge-20261004.md
```

The dispatch predeclares a two-node direct edge with positive delay and three
conditions: no-edge causal control; default static edge
`w=1,d=1,r=0`; and a single `w=2,d=1,r=0` accepted static N2 transfer-bound
sensitivity condition. The `w=2` arm is not a search or post-result rescue.
The input is the five-seed Luna-33 training point streams, using only ordered
points and `x+y` payloads, with opaque provenance IDs and no labels or
classification endpoints. Measurement ends at second-emitter/candidate
formation before any topology mutation.

Predeclared terminal classifications are independent axes:
`MULTI-EMITTER BRIDGE ESTABLISHED`,
`MULTI-EMITTER BRIDGE NOT ESTABLISHED UNDER DEFAULT EDGE`,
`STATIC N2 TRANSFER SENSITIVITY ESTABLISHED`,
`CANDIDATE FORMATION ESTABLISHED`,
`CANDIDATE FORMATION NOT ESTABLISHED`, and
`BLOCKED — EXISTING PUBLIC API INSUFFICIENT`.

## Architecture audit

| Clause | Decision |
|---|---|
| A01/A02 | Event-driven execution and local time are unchanged; only public logical timestamps are used. |
| A03 | Positive-delay routed activity exists; direct one-hop path is bounded. |
| A04 | Fixed two-node topology and explicit finite capacities; no mutation. |
| A06 | Prediction semantics are untouched and not an endpoint. |
| A07 | Labels/readout outcomes are excluded; structural evidence remains actual, local canonical emissions. |
| A08 | Existing E2 state/queue/event/settling limits remain in force. |
| A10 | Resource/energy is not optimized or claimed; diagnostics are not a benefit endpoint. |
| A14 | Accepted ACP-0007 evidence semantics remain unchanged; candidates, if any, must follow actual within-character emissions. |
| A15 | Software-reference mechanism study only; no hardware validation. |

No architecture change is required for the authorized question; no ACP is
required. If the public API proves insufficient, Luna-34 must return
`BLOCKED — EXISTING PUBLIC API INSUFFICIENT`, identify the smallest missing
contract, and stop without implementing it.

## Explicit stop conditions and next gate

```text
task-efficacy retry authorized? NO
E2 pruning: NOT AUTHORIZED
N3: NOT AUTHORIZED
cross-character evidence: NOT AUTHORIZED
reception-as-emission evidence: NOT AUTHORIZED
architecture promotion: NOT AUTHORIZED
Luna-34 execution in this invocation: NOT RUN
```

Any later task-efficacy authorization requires demonstrated candidate
formation on a bridge relevant to the integrated E2 path and a separate
Luna-0 governance review. Luna-34 returns to Luna-0 before any follow-up.
