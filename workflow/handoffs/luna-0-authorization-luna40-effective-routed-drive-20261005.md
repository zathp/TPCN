# Luna-0 Governance Decision — Luna-40 Effective Routed Drive

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Production routed-strength audit and Luna-40 authorization"
  task_id: "luna-0-authorization-luna40-effective-routed-drive-20261005"
  component: "Existing Model-B edge parameters, ACP-0007 local growth, ACP-0008 temporal integration"
  status: "complete; Luna-40 AUTHORIZED / NOT EXECUTED"
  contract_version: "1.2"
  branch: "main"
  base_revision: "6ae253dd53b2b7a9ba1589c10035690a5b65e416"
  result_revision: "commit containing this handoff"
  dependencies:
    - "Independent Luna-0 post-Luna-39 review"
    - "Accepted ACP-0007 and independently reviewed Luna-28 implementation"
    - "Accepted experimental ACP-0008 and independently reviewed Luna-38/39"
  owner: "Luna-0 Architecture Guardian; scope explicitly requested by project owner"
  classification: ["GOVERNANCE AUDIT", "MECHANISM CHARACTERIZATION AUTHORIZATION"]
  hypothesis: "Accepted source-local E2 structural growth may raise effective routed drive by admitting a bounded convergent route; no edge-weight learning exists."
  counter_hypothesis: "No locally evidenced edge is admitted from the declared start, or its later routed input does not reach the ACP-0008 discharge-capable regime."
  interfaces_relied_on:
    - "BoundedTopology and immutable Model-B Edge"
    - "StructuralObservationPlane and TemporalAssociationPolicy"
    - "StructuralPlasticityController"
    - "ExcursionCharacterRuntime and opt-in ACP-0008 IntegrationConfig"
  label_information_boundary:
    - "Luna-40 may consume only points from the declared stream; labels are forbidden inputs."
    - "Structural evidence remains canonical-emission identity and timestamp only."
  timing_assumptions:
    - "Positive edge delays and canonical equal-time ordering remain unchanged."
    - "Mutation remains post-character, after successful settling and runtime teardown."
  reset_boundaries:
    - "Neuron/integration and structural evidence state reset at character boundaries."
    - "Only accepted topology persists within a run."
  resource_bounds:
    - "Finite node, edge, routing, fan-in/out, queue, event, eligibility, observation, candidate and growth-attempt capacities."
  authorized_scope:
    - "Audit of the exact existing production mechanisms and their bounds."
    - "Create the bounded mechanism-only Luna-40 contract and update governance."
  unauthorized_scope:
    - "Run Luna-40 now; alter production code or edge learning; change ACPs or core architecture."
    - "Task efficacy, accuracy, pruning, parameter sweeps, ACP-0008 promotion, or successor authorization."
  controls:
    - "Frozen topology with observation off."
    - "Frozen topology with accepted observation on."
    - "Existing local growth enabled."
    - "No-local-evidence and equal-time negative evidence controls."
  measurements:
    - "No experiment measurements produced in this governance pass."
    - "Luna-39 reviewed result: w=1 max |z|=0.763164, zero destination emissions; predeclared w=2 produced 31 integrated emissions on 27/320 characters."
  information_boundary_check:
    - "The existing ACP-0007 scorer consumes source-local temporal association counts; rewards and labels do not drive it."
  hardware_mapping:
    - "Software-reference mechanism only; no hardware equivalence is claimed."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A14", "A15"]
  preserves:
    - "Static N2 Model-B transfer; edge weights are not learned."
    - "ACP-0007 remains optional accepted E2 growth; ACP-0008 remains experimental and opt-in."
    - "Historical Luna-33/34/37/38/39 verdicts."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-40.agent.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
    - "workflow/handoffs/luna-0-authorization-luna40-effective-routed-drive-20261005.md"
  tests_added: []
  tests_passing:
    - "Baseline equality and cleanliness verified before edits."
    - "Source, reviews, ACPs, implementation and Luna-39 config/results/summary inspected."
    - "Documentation-only diff; no production files changed."
  tests_failed: []
  tests_not_run:
    - "Luna-40 experiment: explicitly not executed."
    - "Production test suites: not rerun because this change is governance-only."
    - "Hardware, FPGA, FPAA, GPU equivalence: not run."
  assumptions:
    - "Existing public APIs can compose ACP-0007's observer/controller path with the direct ACP-0008-capable character runtime without production changes; Luna-40 must stop if not."
  unresolved:
    - "Whether the current accepted growth mechanism can form the required local candidate and reach the ACP-0008 discharge boundary is unknown until Luna-40 is independently reviewed."
    - "The exact Luna-39 outcome is a mechanism result, not efficacy or task evidence."
  recommended_next_agent:
    - "Luna-40 executes only its authorized bounded mechanism characterization, then returns evidence to Luna-0 for independent review."
```

## Outcome and baseline

**OBSERVED:** The audit began on clean `main` at
`6ae253dd53b2b7a9ba1589c10035690a5b65e416`, with
`HEAD == origin/main`. The starting worktree and index were clean.

**OBSERVED:** Luna-39's independently reviewed result is **PASS WITH
FOLLOW-UP**. Under ACP-0008 at default parameters and `theta_E=1`, the
default `w=1` condition accumulated to maximum `|z|=0.763164` but emitted no
destination event. The declared `w=2` sensitivity produced 31
trace-reconstructed integration-mediated canonical emissions on 27/320
characters, with zero direct destination emissions. ACP-0008 remains
experimental and opt-in; the result is not efficacy.

## Production routed-strength audit

| Mechanism | Location and status | Effect on routed drive | Evidence, bounds, determinism, review |
|---|---|---|---|
| Static Model-B edge transfer | `tpcn/topology.py`; accepted ACP-0002 N2 | `tanh(w * payload)`, then divider/reference transform. `Edge` is frozen; `w` is constrained to `[-2, 2]`. No existing-edge update API. | Constructor-configured only; deterministic route order; independent N2 verification. A literal `w=2` is a static fixture setting, not learned strength. ACP-0002 N3 remains unauthorized. |
| Accepted E2 local temporal growth | `tpcn/structural_observation.py`, `tpcn/temporal_association.py`, `tpcn/structural_plasticity.py`, integrated by `tpcn/experiments.py` and `tpcn/experiment_excursion_runtime.py`; opt-in through accepted ACP-0007 | Does not alter existing weights. May add a new convergent edge, increasing the number/timing of separately routed events into a destination. New edges use the existing default Model-B values (`w=1`, `d=1`, `r=0`) and declared positive delay. | Evidence is bounded source-local canonical-emission temporal association; no reward/eligibility, labels, payload magnitude or task readout. Candidate score saturates at configured maximum; deterministic rank/ties; finite edge/routing/fan-in/out/candidate/attempt limits. Luna-12I established bounded candidate-based fan-in in a fixture; Luna-28 independently reviewed the E2 post-character implementation and a later causal route. Useful task growth is not established. |
| Eligibility and reward | `tpcn/eligibility.py`; active local delayed-credit mechanism | Updates bounded local eligibility credit; no edge, topology, or routed-weight mutation. | Reward/error identities, trace count and values are bounded; deterministic local timestamp decay. It has no connection to Model-B `w`, `d`, or `r`. |
| Historical outer structural path | `ExperimentRunner._adapt_topology()` in `tpcn/experiments.py` | Legacy policy can construct candidates from outer feature/loss and prune, but is not the accepted E2 local evidence rule and is not eligible for Luna-40. | Explicitly excluded by ACP-0007 for EXCURSION_V1. No use of this path, labels, reward, loss, or pruning is authorized. |
| Static convergent topology | `BoundedTopology` in `tpcn/topology.py` | Multiple admitted/initial edges can deliver separate routed events to one node; ACP-0008 then processes them event-by-event through its bounded `z` state. | Fan-in is explicitly bounded; no unordered sum or new combination rule exists. Luna-12I and Luna-28 fixtures support legal convergent structure, not task efficacy. |

**INFERRED:** No existing production mechanism increases an existing edge's
effective weight or reinforces it toward `w=2`. The only currently accepted
endogenous way to change routed strength is optional ACP-0007 topology growth:
it can create more causal input paths, each using fixed Model-B parameters.
Whether ordinary input produces the necessary local evidence and whether that
additional path reaches the ACP-0008 discharge boundary remain untested.

**Decision:** A narrow Luna-40 is justified as an existing-mechanism
characterization of bounded convergent route growth, not edge-weight learning.
It is authorized **NOT EXECUTED**. The complete binding scope, paired
controls, network, stream, bounds, measurements, endpoints, stop conditions,
and prohibitions are in `.github/agents/luna-40.agent.md`.

## Architecture and historical disposition

No A01-A15 text changes and no ACP is created or amended. ACP-0007 remains
accepted and optional for the separately authorized local E2 growth path.
ACP-0008 remains accepted as experimental, opt-in, and disabled by default.
No weight-learning rule, N3 behavior, pruning, accuracy/efficacy, or
promotion is authorized.

Luna-37 remains historically **NOT SUPPORTED IN THIS SETUP** under the
pre-ACP-0008 neuron; Luna-38 and Luna-39 remain **PASS WITH FOLLOW-UP** within
their declared mechanism scopes. Luna-33 and Luna-34 are unchanged. Earlier
statements that Luna-40 was not yet authorized remain historical records and
are superseded only by this owner-directed decision.

## Validation and limits

- Verified `HEAD == origin/main == 6ae253dd53b2b7a9ba1589c10035690a5b65e416`;
  clean index and worktree before edits.
- Inspected the independent Luna-39 review, Luna-39 agent contract and
  `config.json`, `results.json`, and `summary.json`; Luna-37's corresponding
  artifacts and review; ACP-0008; Luna-38 implementation/review; ACP-0007;
  topology, edge transfer, eligibility, structural observation/admission,
  and experiment integration; Luna-12I, Luna-13F and Luna-28 structural
  evidence.
- **Not run:** Luna-40, production tests, or hardware validation. Production
  code is unchanged; this is a governance-only authorization.
- `git diff --check`: passed before publication.
- Final `HEAD == origin/main` and clean worktree: verify after publication.

The narrow assumption that current public APIs can compose local structural
growth with an integration-enabled destination must be verified before
execution. If doing so requires any production/interface change, Luna-40
returns blocked to Luna-0; no change is authorized.

## Next assignment

Luna-40 may execute only the bounded mechanism characterization defined in
`.github/agents/luna-40.agent.md`, then return the complete evidence to Luna-0.
Luna-40 cannot self-close or authorize an efficacy, pruning, or follow-on
candidate-opportunity experiment.
