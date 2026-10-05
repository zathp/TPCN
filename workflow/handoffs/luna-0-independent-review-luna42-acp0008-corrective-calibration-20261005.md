# Luna-0 Independent Post-Luna-42 Review — ACP-0008 Corrective Calibration

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-0"
  descriptive_name: "Independent post-Luna-42 calibration review"
  task_id: "independent-review-luna42-acp0008-corrective-calibration-20261005"
  component: "ACP-0008 EXCURSION_V1 slow temporal integration"
  status: "complete"
  contract_version: "1.1"
  branch: "main"
  base_revision: "3af1c1bcc0f4a0121752103211aa702fc6a6e85a"
  result_revision: "the commit publishing this handoff and governance update"
  dependencies:
    - "Luna-42 corrective calibration publication"
    - "Accepted ACP-0008"
    - "Accepted ACP-0007, unchanged"
  owner: "Luna-0"
  classification:
    - "independent scientific review"
    - "evidence reconstruction"
    - "governance review"
  hypothesis: "The corrected production-derived calibration selects a valid bounded decay value and its frozen fixed-w=1 relay condition produces causally routed integration-mediated activity."
  counter_hypothesis: "Provenance, replay, controls, recurrence, or bounded causal routing fails independent reconstruction."
  interfaces_relied_on:
    - "Luna-42 runner and frozen configuration"
    - "Canonical EXCURSION_V1 source emission"
    - "Model-B source-to-relay and relay-to-destination routing"
    - "ACP-0008 local slow-integration state"
  label_information_boundary:
    - "Phase-B point inputs are obtained from each example's points; labels are not used by the runtime input helper."
    - "No accuracy or task-efficacy endpoint was measured."
  timing_assumptions:
    - "Luna-42 predeclared near/far fixture times and Phase-B production timestamps."
    - "Model-B route delay is fixed at 1.0."
  reset_boundaries:
    - "Phase-A fixture state is isolated per candidate and fixture."
    - "Phase-B records are character-local."
  resource_bounds:
    - "Luna-42's predeclared neuron, event, eligibility, queue, topology, and character limits were retained."
  authorized_scope:
    - "Independently audit the committed Luna-42 evidence, provenance, runner chronology, replay, scientific criteria, and tests."
    - "Publish this review handoff and update workflow/changelog governance records."
  unauthorized_scope:
    - "Do not change, repair, retune, or rerun-publish Luna-42."
    - "Do not implement or test WEMA."
    - "Do not enable ACP-0007 growth, pruning, or efficacy."
    - "Do not authorize Luna-43 or another calibration search."
    - "Do not promote ACP-0008 or claim hardware equivalence."
  controls:
    - "Phase-A isolated, near-pair, near-triple, far-triple, signed, and integration-disabled fixtures."
    - "Phase-B CALIBRATED, DEFAULT, and DISABLED arms on paired streams."
  measurements:
    - "Independent recurrence and provenance reconstruction."
    - "Exact discrete event/selection and replay identity."
    - "Phase-B emission, reception, route, and within-character ordered-emitter counts."
  information_boundary_check:
    - "No label-derived runtime input or class correctness endpoint."
    - "Structural candidate/opportunity analysis is a review-only offline diagnostic; no candidate was submitted or admitted."
  hardware_mapping:
    - "Not run; no hardware-equivalence claim."
  architecture_invariants_touched:
    - "A01: observed event-driven causal emission/routing sequence."
    - "A03: fixed positive finite route delay; no global neural timestep introduced."
    - "A07: bounded local integration state and fixed runtime limits."
  preserves:
    - "ACP-0008 remains experimental, opt-in, and unpromoted."
    - "ACP-0007 remains unchanged and disabled throughout Luna-42."
    - "Luna-41 remains historically BLOCKED; its verdict is not overwritten."
    - "No architecture-contract clause text is changed."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna42-acp0008-corrective-calibration-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "Focused Luna-42 suite: 8 passed."
    - "Full repository suite: 1023 passed, 1 skipped, 1024 collected."
    - "GPU skip independently confirmed: CUDA unavailable."
    - "Phase-A and Phase-B retained replay digests independently reproduced."
  tests_failed: []
  tests_not_run:
    - "Hardware/FPGA/FPAA equivalence (out of scope)."
    - "Structural growth, pruning, efficacy, and WEMA (explicitly unauthorized)."
  assumptions:
    - "The recorded commit revision and execution-identical runner are the provenance identity for the published evidence."
  unresolved:
    - "Two auxiliary focused-test assertions use abs_tol=1e-12 instead of the predeclared experiment comparison formula; they do not feed runner acceptance, candidate selection, or artifact generation. Record as a non-blocking test-policy follow-up; do not alter the reviewed run."
    - "A future structural-opportunity experiment is not justified by this result: every observed within-window ordered emitter pair is over the existing source-to-relay edge, and the destination never emits."
  recommended_next_agent:
    - "No new Luna assignment authorized. Retain the evidence and await a separate owner decision if a distinct, testable missing-edge candidate question is proposed."
```

## Outcome and reviewed scope

**PASS WITH FOLLOW-UP — Luna-42's bounded calibration and frozen Phase-B
mechanism result are independently reproducible. No Luna-43 is authorized.**

The exact requested starting point was fetched and verified before review:
`HEAD == origin/main == 3af1c1bcc0f4a0121752103211aa702fc6a6e85a`, branch
`main`, with a clean worktree/index. The reviewed publication chain is:

```text
db4774a  Luna-42 authorization
900a034  runner/tests
d073ecc  Phase-B input-digest initialization fix; recorded execution revision
3af1c1b  final artifact and handoff publication
```

The `d073ecc` correction changes only Phase-B `input_digests` initialization
from an empty mapping to arm-keyed mappings and adds its focused regression
test. It does not change stimuli, topology, weights/delays, neuron settings,
Phase-A selection, or Phase-B criteria. It precedes the actual recorded
execution revision. The final publication adds artifacts and the executor
handoff without changing the runner or tests. The committed runner's recorded
SHA-256 is
`dd36a2be784921b5b774f1da199b8ba60fcce4a5d8124c79ba1f3d4843a1a376`;
after normalizing the Windows checkout line endings, its content matches the
execution revision. The earlier Luna-41 review remains **BLOCKED**; nothing
in this review rewrites its historical result.

## Scientific reconstruction

The candidate set is exactly `{0.1, 0.05, 0.025, 0.0125}` for
`decay_rate_z`; all other ACP-0008 parameters and fixture timings remain
fixed. Source stimulus traverses the production source neuron, canonical
emission, fixed Model-B edge, and destination reception. The recorded
production payload is used as the recurrence input; no downstream `0.4`
payload is manually injected or required. ACP-0007 is disabled.

All four artifact digests, the frozen configuration digest
`e6c17c12f56e5661aef99215ef41bbc82c1d61f617600fb08c7f98504addafad`, and
aggregate run digest
`f903a6ca5f3f454ce66a793bfdfec707ca131bcb049d2c696b1892e430e3e339`
were independently recomputed. The execution revision is the non-null
`d073ecc13e789105c611181992ce4c8d48c79030`.

The declared floating comparison rule is
`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`.
Independent reconstruction of all 68 enabled Phase-A recurrence steps
agrees with the retained trace; the maximum state residual is
`1.2705494208814505e-21`, and discharge amounts match exactly. The retained
positive near-triple routed inputs are
`0.4`, `0.4000008889685561`, and `0.4000008889707768`; the negative fixture
is sign mirrored. The declared recurrence rule and exact discrete criteria
are used by the runner; no hidden runner-only `1e-12` acceptance tolerance
was found.

The predeclared Phase-A selection rule selects `0.0125`: `0.1`, `0.05`, and
`0.025` fail the near-triple integrated-emission criterion, while `0.0125`
passes all required fixtures, including isolated/near-pair subthreshold
controls, near-triple single integrated discharge, far-triple silence,
signed symmetry, and the disabled control. The selected candidate's neutral
probe returns `z=1.815997190499391e-05` (isolated),
`3.361558798139755e-05` (near pair),
`1.3696127392068382e-06` (near triple),
`3.26867386164279e-05` (far triple), and
`-1.3696127392068382e-06` (negative near triple); all are below the
predeclared `1e-4` bound, with no post-probe relay emissions.

The frozen configuration identity is retained before Phase-B stream
construction; no Phase-B behavior selects or retunes the value. Independent
replay from the execution-identical runner reproduces the exact Phase-A
digest `5b5b34acaee7034c600dd31ccbb800acb5426bbe40822b7f77df3b3a4ce41040`
and Phase-B digest
`4547c9b59441d4af0af6fb1de3c6c70943c9a4ae8cd7907f1b320eeb683a765d`.

Phase B contains 320 paired character records per arm. Each arm has the
same 1,715 source emissions and source-to-relay production routes:

| Arm | Relay emissions | Integration-mediated | Direct | Relay-to-destination transfers/receptions | Destination emissions |
|---|---:|---:|---:|---:|---:|
| CALIBRATED (`decay_rate_z=0.0125`) | 235 | 235 | 0 | 235 | 0 |
| DEFAULT | 0 | 0 | 0 | 0 | 0 |
| DISABLED | 0 | 0 | 0 | 0 | 0 |

Model-B transfer checks and recorded causality checks pass. Both route edges
are ordinary local hops with `route_depth=1`; together they constitute a
two-edge causal sequence, not one route event with cumulative depth two.
Maximum calibrated relay `|z|` is `1.3692730293667474`. This supports a
bounded, task-independent calibration and a fixed-topology causal
integration/routing result only; it does not establish task efficacy,
optimality, growth benefit, energy benefit, ACP promotion, or hardware
equivalence.

### ACP-0007 opportunity gate

An independent scan of every character's canonical emitter timestamps finds
exactly 235 within-character ordered pairs satisfying `0 < dt <= 4.0`, all
`source -> relay` in the CALIBRATED arm. The same scan finds no such pairs in
DEFAULT or DISABLED. These pairs are over the already-existing
`source -> relay` edge. No destination canonical emission occurs, so neither
`source -> destination` nor `relay -> destination` obtains a later-emitter
pair. A routed reception is not an emission and cannot supply that evidence.
Therefore the result does **not** evidence a legal missing-edge candidate
opportunity; it does not justify a candidate-formation diagnostic as the
next experiment. No Luna-43 contract or authorization is created.

### Follow-up: auxiliary test tolerance

The runner's scientific comparisons use only the declared binary64 rule.
Two auxiliary assertions in `tests/test_luna42_acp0008_corrective_calibration.py`
use `abs_tol=1e-12` for the isolated nominal `0.4` and positive/negative
symmetry checks. Those test-only assertions do not supply route inputs, feed
the candidate-selection predicate, change artifact generation, or accept a
scientific result. They are a non-blocking test-policy discrepancy to correct
in a separately scoped test-only change if desired. Luna-42 was not modified
to address it.

## Validation record

| Command or procedure | Revision / environment | Observed result | Evidence |
|---|---|---|---|
| `.\.venv\Scripts\python.exe -m pytest .\tests\test_luna42_acp0008_corrective_calibration.py -q` | Published runner, repository `.venv`, Windows/Python 3.11.5 | 8 passed | `tests/test_luna42_acp0008_corrective_calibration.py` |
| `.\.venv\Scripts\python.exe -m pytest -q -rs` | Published runner, repository `.venv`, Windows/Python 3.11.5 | 1023 passed, 1 skipped; 1024 collected | Full test run; matches executor totals |
| `.\.venv\Scripts\python.exe -m pytest .\tests\test_gpu_visualization.py -q -rs` | Same environment | 3 passed, 1 skipped; CUDA unavailable | `tests/test_gpu_visualization.py:61` |
| Artifact/configuration digest reconstruction | Published artifacts | All retained digests match | Luna-42 artifact set |
| Phase-A recurrence reconstruction | All candidates and fixtures | All 68 enabled steps match tolerance; max residual `1.2705494208814505e-21` | `results.json`, Phase-A records |
| Phase-A and Phase-B replay | Execution-identical runner | Both retained replay digests reproduced | Replay digests above |
| Phase-B route/emission audit | 960 character-arm records | Paired inputs and causal transfers reconcile; counts in table above | `results.json` |
| Within-window ordered-emitter scan | All 960 character-arm records | Only the 235 existing `source -> relay` pairs in CALIBRATED | Independent scan of canonical emissions |
| Hardware equivalence | Not run; out of scope | Not applicable | No hardware claim |

The pre-Luna-42 reviewed baseline was 1015 passed, 1 skipped, 1016
collected. The current suite's increase of eight collected/passing tests is
consistent with the focused Luna-42 tests; the pre-existing CUDA-unavailable
skip remains.

## Architecture and integration disposition

Relevant evidence concerns A01/A03 causal event routing and A07 bounded
opt-in temporal integration. The experiment keeps fixed bounded topology;
it does not test or mutate A14 structural adaptation. No architecture
contract clause, ACP, production neuron, routing, or ACP-0007 semantics
changed. ACP-0008 remains experimental, opt-in, and unpromoted. WEMA remains
untested and unauthorized.

**Integration readiness:** the Luna-42 calibration/mechanism evidence passes
independent review with the auxiliary test-tolerance follow-up above.
Structural opportunity formation, efficacy, and architecture promotion are
not established. No further Luna task is authorized by this review.

## Next assignment

No next Luna assignment. Return to the project owner/Luna-0 for any new,
separately bounded question. Do not infer authorization for Luna-43,
additional calibration values, WEMA, ACP-0007 growth/pruning, efficacy, or
promotion from this review.
