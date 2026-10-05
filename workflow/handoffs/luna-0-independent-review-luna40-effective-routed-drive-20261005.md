# Luna-0 Independent Review — Luna-40 Effective Routed Drive

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of bounded Luna-40 mechanism result"
  task_id: "luna-0-independent-review-luna40-effective-routed-drive-20261005"
  component: "ACP-0007 local temporal growth and ACP-0008 effective routed drive"
  status: "complete; no Luna-41 authorized"
  contract_version: "1.0"
  branch: "main"
  base_revision: "ebff91176c02e29e3b9aad38308fc95d0b773817"
  execution_start_revision: "a39dd335e7af1b18a8d28ef3faf7b975304132df"
  execution_revision: "5cbd62f929bdc19fff2f24de936b13d47c5386f8"
  dependencies:
    - "Luna-0 authorization: workflow/handoffs/luna-0-authorization-luna40-effective-routed-drive-20261005.md"
    - "Luna-40 execution: workflow/handoffs/luna-40-effective-routed-drive-20261005.md"
    - "Accepted ACP-0007 and ACP-0008"
  owner: "Luna-0 Architecture Guardian"
  classification:
    - "independent result and contract review"
    - "bounded negative mechanism result"
    - "no production or architecture change"
  verdict: "NOT SUPPORTED IN THIS SETUP; EXECUTION CONTRACT PASS; NO PRODUCTION DEFECT"
  result_class: "NO LEGAL EDGE ADMISSION"
  architecture_change: false
  proposal: null
  follow_up_authorized: false
  files_changed:
    - "workflow/handoffs/luna-40-effective-routed-drive-20261005.md"
    - "workflow/handoffs/luna-0-independent-review-luna40-effective-routed-drive-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_passing:
    - "Luna-40 focused tests: 11 passed"
    - "Full repository suite: 1009 passed, 1 skipped; 1010 collected"
    - "Independent artifact aggregate, route-provenance, control, capacity, and replay checks"
  tests_failed: []
  tests_not_run:
    - "Independent full execution rerun; retained full-run digest and all detailed records were independently audited instead."
    - "Hardware, FPGA/FPAA equivalence, task efficacy, and admitted-shortcut drive; outside this review's authorized result."
  unresolved:
    - "Effective destination drive after a legally admitted shortcut was not tested because no edge was admitted."
    - "No conclusion is made about alternate streams, topologies, weights, delays, integration settings, or task outcomes."
  recommended_next_agent:
    - "Project owner to decide whether to pursue the no-relay-emission boundary; no Luna-41 is authorized."
```

## Review basis and disposition

Review resumed on `main` at
`ebff91176c02e29e3b9aad38308fc95d0b773817`, and `git fetch origin`
confirmed `HEAD == origin/main`. The worktree was not clean at that point:
it contained only the unpublished Luna-0 review draft from the preceding
turn (the two governance documents, this handoff, and the Luna-40 handoff
revision correction); no experiment files or unrelated changes were present.
Those review changes were inspected, completed and are included in this
publication. The execution artifact records its authorized clean starting
revision as
`a39dd335e7af1b18a8d28ef3faf7b975304132df`. The implementation and artifact
revision is `5cbd62f929bdc19fff2f24de936b13d47c5386f8`.

**NOT SUPPORTED IN THIS SETUP; EXECUTION CONTRACT PASS; NO PRODUCTION
DEFECT; NO LUNA-41 AUTHORIZED.** The experiment completed the predeclared
negative branch without a stop condition. The result is **NO LEGAL EDGE
ADMISSION** in the declared fixture. It does not falsify ACP-0007 or
ACP-0008, but it does not support the hypothesis that this stream and
starting topology produce useful effective routed drive through local
growth.

## Independent evidence audit

The detailed results file was parsed independently, and the recorded
aggregates were recomputed across all four arms and five seeds:

| Measure per arm | Independently reconstructed result |
|---|---:|
| Character executions | 320 |
| Source canonical emissions | 1,715 |
| `source->relay` routed transfers | 1,715 |
| Relay / destination canonical emissions | 0 / 0 |
| `relay->destination` / shortcut transfers | 0 / 0 |
| Destination receptions / integration updates | 0 / 0 |
| Ordered source/destination association pairs | 0 |
| Candidate opportunities / candidate records | 0 / 0 |
| Growth attempts / admissions | 0 / 0 |
| Maximum destination `|z|` | 0.0 |

No new edges were created or used. Destination fan-in remained one edge
(`relay->destination`) against a limit of two; that edge carried zero events.
The only used edge was `source->relay`, delay `1.0`, with 1,715 transfers per
arm. There was no destination route, arrival time, integration contribution,
or ACP-0008 retention interval to reconstruct. Thus this run did not realize
convergent fan-in, and the destination's zero `z` is a no-reception result.

The audit additionally verified that each character retained the exact two
declared initial edges, no character mutated the topology, and route records
link to canonical emission identities and runtime events with matching
source/destination, timestamp, delay, payload, and Model-B transform.
Destination reception counts reconcile with integration-trace counts. Every
character settled with no pending events or exhausted event budget; all three
eligibility ledgers per character reconcile under capacity 1024. The declared
observation-only and no-local-evidence controls, as well as the no-admission
growth arm, match the frozen neural/runtime/resource projections for every
seed and character.

The isolated equal-time control uses actual canonical emissions at the same
timestamp and produces zero candidates. It is correctly kept separate from
the primary stream and does not inject evidence into it.

The full deterministic replay digest was recomputed independently from the
retained artifact:

`f5c7f4d8fbc2037c43ac1118e96e6a2a23e4f0241da78cd7bea99a226b730211`

It matches both recorded replay digests. The four arms each report 1,715
source emissions and routed transfers, 11,109 runtime events, queue peak 2,
and maximum eligibility occupancy 19. No capacity error, settling failure,
or replay discrepancy was found.

### Starting state, topology and capacity

For every seed and character, the frozen, observation-only, growth-enabled,
and no-local-evidence arms have matching input digests and starting topology.
All use the same source and relay configurations, destination
`E1Config(theta_E=1.0, event_budget=4096, integration=IntegrationConfig())`,
and ACP-0008 defaults (`decay_rate_z=0.1`, `input_gain=1.0`,
`theta_Z=1.0`, `z_max=4.0`). The only interventions are the predeclared
observation/mutation settings and, for the no-local-evidence control, its
empty source-neighbor declaration.

| Resource | Declared bound | Observed/reconstructed use |
|---|---:|---:|
| Nodes | 3 | 3 |
| Edges / edge capacity | 2 initially / 3 | 2; no additions |
| Fan-in / fan-out limit | 2 / 2 | maximum observed 1 / 1; destination fan-in stayed 1 |
| Routing capacity | 3 | outgoing degree never exceeded 1 |
| Per-source / per-plane candidate capacity | 4 | occupancy 0 |
| Controller candidate capacity | 12 | occupancy 0 |
| Growth attempts per run | 4 | 0 |
| Queue capacity | 128 | peak 2 |
| Runtime event budget | 1,024 per character | maximum processed 88; no exhausted budget |
| Prediction capacity / expiry | 8 / 4.0 | configured through the existing `LocalPredictor` API; no runtime failure |
| Eligibility capacity | 1,024 per ledger | three ledgers per character; maximum peak 19; occupancy reconciles |
| Observation audit bound | 3,072 per character | maximum observed work 19 |

No bound was enlarged or automatically grown. Prediction capacity is verified
from the runner/runtime configuration and existing `LocalPredictor` setup;
the retained Luna-40 record does not expose a per-character outstanding-
prediction peak, so no occupancy maximum is claimed for that resource.

## Method and contract review

The runner uses the inherited Luna-34 point-sequence helper: `SpiralConfig()`,
the specified training/evaluation seeds, 16 examples per class, and the
declared deterministic shuffle. It consumes only training `example.points`,
preserves point timestamps and same-time batching, transforms each point to
`x+y`, sends input only to `source`, and uses neutral reward. The source
contains no label or label-metadata reads.

Structural observations enter the existing `StructuralObservationPlane`
through the runtime's canonical-emission observer callback. Candidate records
come from that plane's frozen evidence, not caller-constructed
`CandidateEvidence`; the controller is invoked only after the character
runtime has settled and torn down. The primary run never admitted an edge.
Separate focused fixtures exercise actual canonical emissions through the
plane/controller, bounded topology rejection, and trace-derived direct versus
integrated-discharge classification. No production mechanism, edge
parameters, ACP, or architecture contract was changed.

This is a valid contract-compliant negative result, but it does **not** test
whether a successfully admitted shortcut would increase destination `z`:
the relay never emitted, so no source-to-destination local association or
candidate was available. Destination `z=0` is therefore an observed
no-reception result, not evidence that an admitted two-path topology would
fail to drive the destination.

### Luna-39 context and scientific interpretation

The independently reviewed Luna-39 result provides context, not a required
reproduction target: with one fixed `w=1` route into the ACP-0008 destination,
maximum `|z|` was `0.763164` with no destination emission; its separately
declared static `w=2` sensitivity reached maximum `|z|=1.118173` and produced
31 integration-mediated emissions on 27/320 characters, with zero direct
emissions. In Luna-40, destination reception count was zero and maximum
`|z|=0.0` in every arm. Because the relay did not emit and no grown edge
existed, neither a second fixed-`w=1` route nor its timing overlap was
observed. The experiment therefore cannot compare topology multiplicity
against Luna-39's stronger single-edge sensitivity or establish that
convergence functionally substitutes for stronger individual coupling.

Answer to the architecture question: **No, not under this declared fixture:
the existing structural-growth mechanism did not engage because it received
no legal source-local candidate.** This is not a finding that ACP-0007 cannot
compose with ACP-0008 through the existing APIs: the composition ran without
an API blocker. It also is not a finding that an admitted convergent route
would be temporally inadequate; that causal branch was never reached.

## Validation

| Validation | Result |
|---|---|
| `python -m pytest -q tests/test_luna40_structural_effective_routed_drive.py` | 11 passed |
| `python -m pytest -q -rs` | 1009 passed, 1 skipped; 1010 collected in 20.18s (11 more than the pre-Luna-40 999). Skip: `tests/test_gpu_visualization.py:61`, CUDA unavailable |
| Independent full-artifact digest | Matches both recorded replay digests |
| Independent per-character resource, route, topology and paired-control audit | No discrepancies |

The Luna-40 execution handoff had a mistyped `result_revision` field. It has
been corrected to the actual execution commit
`5cbd62f929bdc19fff2f24de936b13d47c5386f8`; the experiment records and
execution outcome were not changed.

## Limits and governance

No edge was admitted and no shortcut route was used. The experiment therefore
provides no evidence about downstream drive after admission, classification,
task efficacy, generalization, candidate usefulness, energy, utility,
calibration, hardware equivalence, or ACP-0008 promotion. The result is
specific to the frozen stream, topology, event bounds, and default
ACP-0008 configuration. No production defect is established; no prior
Luna-33/34/37/38/39 or ACP-0007 verdict is changed.

This negative outcome does not justify tuning weights, fan-in, delays,
thresholds, or ACP-0008 parameters. The specific unresolved boundary is that
the declared task stream failed to produce relay emissions and therefore
failed to engage source-local growth. Return that boundary to the project
owner for direction; do not infer a general structural-plasticity failure.
ACP-0008 remains experimental/opt-in and unpromoted. No Luna-41 was created
or authorized.
