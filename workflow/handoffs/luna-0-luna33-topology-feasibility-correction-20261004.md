# Luna-0 Decision — Luna-33 Topology Feasibility Correction

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Pre-outcome Luna-33 topology feasibility correction"
  task_id: "luna-0-luna33-topology-feasibility-correction-20261004"
  component: "Public seeded topology initialization and static growth headroom"
  status: "AUTHORIZED — CORRECTED LUNA-33 / NOT EXECUTED"
  contract_version: "1.2"
  branch: "main"
  base_revision: "6206eb11f2160adcd38b032ee7b7fe86fcc187d9"
  result_revision: "governance-only publication"
  dependencies:
    - "Luna-33 original authorization and frozen A–D experiment design"
    - "Accepted ACP-0007"
  owner: "Luna-0 Architecture Guardian"
  classification: ["OBSERVATION", "VERIFICATION", "EXPERIMENT"]
  hypothesis: "A lower fixed initial edge count permits public deterministic initialization for all five required seeds while preserving legal static ring growth candidates."
  counter_hypothesis: "No initial edge count from 0 through 8 initializes for every required seed, or the maximum all-seed feasible topology has no legal ring candidate."
  interfaces_relied_on:
    - "ExperimentConfig"
    - "ExperimentRunner.evaluate()"
    - "ExperimentRunner.topology"
  label_information_boundary:
    - "One synthetic probe point was used solely to trigger public topology initialization."
    - "No metric or task outcome from the probe was inspected."
  timing_assumptions: ["Initial topology edge delay is the public initializer's 1.0."]
  reset_boundaries: ["A fresh ExperimentRunner was constructed for each seed and edge-count probe."]
  resource_bounds:
    - "8 nodes"
    - "edge capacity 16"
    - "fan-in 2 and fan-out 2"
    - "eight directed static observation-ring candidates"
  authorized_scope:
    - "Sweep topology_initial_edges=0..8 for seeds 0..4 through public ExperimentRunner initialization."
    - "Choose the maximum count feasible for all five seeds."
    - "Statically verify absent ring candidates satisfy edge-capacity and fan-in/out limits."
    - "Correct only Luna-33's topology_initial_edges value if feasibility and headroom are established."
  unauthorized_scope:
    - "Running the four-class efficacy experiment or inspecting outcome-bearing metrics."
    - "Changing seeds, node count, edge capacity, fan-in/out, observation fabric, growth bounds, dataset, A–D design, endpoint, or support rule."
    - "Private topology injection or production/runtime changes."
    - "Architecture promotion, pruning, ACP-0002 N3, or hardware-equivalence claims."
  controls: ["The same public initializer and all frozen settings were held fixed while only requested initial edge count varied."]
  measurements:
    - "Initialization success/error for each of 9 edge counts x 5 seeds."
    - "Exact five initial topologies at the maximum all-seed feasible count."
    - "Number and identity of currently legal absent ring candidates per topology."
  information_boundary_check:
    - "No label, accuracy, growth evidence, prediction loss, route-use outcome, or resource proxy was inspected."
  hardware_mapping: ["Not applicable; no hardware behavior or equivalence was evaluated."]
  architecture_invariants_touched: ["A04", "A14"]
  preserves: ["Architecture Contract 1.2 and A01-A15", "Accepted ACP-0007", "Luna-33 scientific design other than the justified initial-edge correction"]
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-33.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-luna33-topology-feasibility-correction-20261004.md"
  tests_added: []
  tests_passing: ["Full baseline suite: 908 passed, 1 skipped; 909 collected."]
  tests_failed: []
  tests_not_run: ["Luna-33 efficacy execution and all outcome-bearing previews."]
  assumptions: ["The public one-point evaluate call is used only to materialize topology; its task-result metrics are discarded and not inspected."]
  unresolved: ["Luna-33 experiment outcome and all efficacy, prediction, resource, and hardware claims remain unestablished."]
  recommended_next_agent: ["Luna-33"]
```

## Decision and evidence

**OBSERVED:** The original Luna-33 profile requested eight initial edges on
eight nodes with edge capacity 16 and fan-in/fan-out limits of two. Its
existing stop handoff records initialization failure for seeds 0, 1, 3, and 4
at that count.

**OBSERVED:** Starting from clean synchronized `main` at
`6206eb11f2160adcd38b032ee7b7fe86fcc187d9`, the full baseline suite passed:
908 passed, 0 failed, 1 CUDA-unavailable skip; 909 tests collected.

**OBSERVED:** A pre-outcome sweep used a fresh `ExperimentRunner` configured
with the frozen Luna-33 shared settings, varying only
`topology_initial_edges` over 0 through 8 and `seed` over 0 through 4. Each
probe called public `evaluate()` on one synthetic point to invoke topology
initialization, discarded the returned task metrics, and read only the
public `runner.topology`. Capacity exceptions were recorded. No four-class
workload or outcome-bearing efficacy metric was evaluated.

| Initial edges | Seed 0 | Seed 1 | Seed 2 | Seed 3 | Seed 4 |
|---:|---|---|---|---|---|
| 0 | Pass | Pass | Pass | Pass | Pass |
| 1 | Pass | Pass | Pass | Pass | Pass |
| 2 | Pass | Pass | Pass | Pass | Pass |
| 3 | Pass | Pass | Pass | Fail: destination fan-in | Pass |
| 4 | Pass | Pass | Pass | Fail: destination fan-in | Pass |
| 5 | Pass | Pass | Pass | Fail: destination fan-in | Fail: source fan-out |
| 6 | Fail: source fan-out | Pass | Pass | Fail: destination fan-in | Fail: source fan-out |
| 7 | Fail: source fan-out | Fail: destination fan-in | Pass | Fail: destination fan-in | Fail: source fan-out |
| 8 | Fail: source fan-out | Fail: destination fan-in | Pass | Fail: destination fan-in | Fail: source fan-out |

Therefore **2 is the maximum all-seed feasible initial edge count** in the
declared sweep. This is a topology feasibility result only, not an efficacy
result and not a substitute for changing the public initializer.

At two initial edges, the exact deterministic topologies and static ring
headroom were:

| Seed | Initial directed edges (delay 1.0) | Legal absent ring candidates |
|---:|---|---:|
| 0 | `neuron-7 -> neuron-4`, `neuron-6 -> neuron-2` | 8 |
| 1 | `neuron-3 -> neuron-5`, `neuron-7 -> neuron-6` | 8 |
| 2 | `neuron-2 -> neuron-1`, `neuron-4 -> neuron-1` | 7 |
| 3 | `neuron-2 -> neuron-4`, `neuron-6 -> neuron-4` | 7 |
| 4 | `neuron-3 -> neuron-4`, `neuron-4 -> neuron-0` | 7 |

The headroom audit used only each resulting edge set and the existing
eight-edge directed ring `neuron-i -> neuron-(i+1 mod 8)`. An absent ring
edge counted as statically legal only when source out-degree was below two,
destination in-degree was below two, and total edge count was below 16.
Every seed retains at least seven legal ring candidates. The result is a
static capacity check; it does not predict candidate evidence, admission, or
later route use.

## Corrective authorization

**INFERRED:** With the required node count and finite edge/fan bounds
unchanged, initial edge count two resolves the observed deterministic
initialization blocker for all required seeds and preserves ample static ring
growth headroom.

Luna-0 therefore authorizes a correction to **only**
`topology_initial_edges`, from 8 to 2, in `.github/agents/luna-33.agent.md`.
All other frozen scientific and architectural terms remain unchanged:
seeds 0–4, eight nodes, capacity 16, fan-in/out two, ring observation fabric,
structural bounds, dataset and split, A/B/C/D conditions, D intervention,
primary endpoint, support rule, and public initialization path.

The original stop handoff remains an immutable record of the original
eight-edge blocker. This correction does not revise it or reinterpret its
results. It does not change the accepted ACP-0007, Architecture Contract
1.2, or acceptance criteria, and requires no ACP. Historical Luna-12L remains
**NOT SUPPORTED / UNCHANGED**; Luna-13F useful-growth prediction remains
**NOT SUPPORTED / UNCHANGED**. E2 pruning and N3 remain **NOT AUTHORIZED**.
Task efficacy, prediction benefit, resource benefit, and hardware equivalence
remain **NOT ESTABLISHED**.

## Validation and next assignment

| Procedure | Result |
|---|---|
| `git fetch origin`; branch and revision checks | Clean synchronized `main` at `6206eb11f2160adcd38b032ee7b7fe86fcc187d9` before edits |
| Full baseline `python -m pytest -q -rs` | 908 passed, 0 failed, 1 skipped (CUDA unavailable) |
| `python -m pytest --collect-only -q` | 909 tests collected |
| Public topology sweep, initial edge count 0–8 x seeds 0–4 | Maximum all-seed feasible count 2; full matrix above |
| Static ring-candidate headroom at two edges | 7–8 legal candidates for every required seed |
| Four-class efficacy experiment or outcome-bearing preview | Not run |
| Production/runtime changes and private topology injection | Not performed |

**HYPOTHESIZED / NOT ESTABLISHED:** The corrected two-edge topology may permit
Luna-33 to complete its declared matched experiment; only the subsequent
authorized experiment can establish whether ACP-0007 growth affects its
task endpoint.

Next assignment: **Luna-33** may resume only under the corrected dispatch,
must still verify exact starting revision and design, preserve every failed
seed, run the frozen experiment and return to Luna-0. No successor or
architecture promotion is authorized by this correction.
