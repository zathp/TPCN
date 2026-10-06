---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of Luna-45 depth-2 destination integration"
  task_id: "luna-0-independent-review-luna45-depth2-destination-integration-20261006"
  component: "Frozen-fixture, two-hop ACP-0008 destination mechanism evidence"
  status: "complete — NOT SUPPORTED IN THIS SETUP"
  contract_version: "1.2"
  branch: "copilot/luna45-depth2-destination-integration"
  base_revision: "97a93b394d071413075a1f102fdef695664722ff"
  result_revision: "d9fcaa09be60eaec5eb4e4316305a717006d55e9"
  dependencies:
    - "Luna-45 authorization 9af6b4435ac581887f04f0951d0f7b16d7d661cd"
    - "Luna-45 runner/execution 97a93b394d071413075a1f102fdef695664722ff"
    - "Luna-45 retained artifact publication d9fcaa09be60eaec5eb4e4316305a717006d55e9"
  owner: "Project owner"
  classification:
    - "independent read-only scientific mechanism review"
    - "NOT SUPPORTED IN THIS SETUP"
    - "no architecture change or successor authorization"
  hypothesis: "The frozen Luna-44 calibration can support integration-mediated canonical emission at the destination after a second ordinary w=1 hop."
  counter_hypothesis: "The destination receives routed activity but calibrated integration does not produce a canonical emission."
  interfaces_relied_on:
    - "Committed Luna-45 runner and raw initial/replay artifacts"
    - "Luna-44 canonical fixture and calibrated-arm evidence"
    - "EXCURSION_V1 production receiver and ACP-0008 recurrence"
    - "ACP-0007 source/destination association window policy"
  label_information_boundary:
    - "Reviewer checked raw x/y/t identity and computed source values; no labels or outcomes used."
  timing_assumptions:
    - "Ordinary fixed one-unit delays; exact identities and local event times."
  reset_boundaries:
    - "Initial and replay records compared per sequence and arm."
  resource_bounds:
    - "Queue 128; runtime/activity 1024; neuron 4096; eligibility 1024/ledger; prediction 8; edge/routing 3; fan-in/out 2; horizon 4.0."
  authorized_scope:
    - "Independently inspect evidence and report a verdict; no experiment rerun."
  unauthorized_scope:
    - "No edits, tuning, new experiment, growth, promotion, or Luna-46."
  controls:
    - "Disabled, default, calibrated destination integration; frozen calibrated relay."
  measurements:
    - "Fixture/provenance identity; historical and cross-arm invariance; route captures; destination recurrence; bounds; replay; precursor prerequisite."
  information_boundary_check:
    - "PASS; frozen raw inputs and labels excluded."
  hardware_mapping:
    - "Not applicable; no hardware equivalence claim."
  architecture_invariants_touched:
    - "A01-A08 and A15 preserved by the reviewed setup; ACP-0007 remains disabled; ACP-0008 remains experimental and opt-in."
  preserves:
    - "Luna-42 PASS WITH FOLLOW-UP; Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED; Luna-44 evidence-quality PASS WITH FOLLOW-UP."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna45-depth2-destination-integration-20261006.md"
  tests_added: []
  tests_passing:
    - "Lead rerun of focused Luna-45/provenance/ACP-0008/runtime/routing/topology selection: 328 passed."
    - "Lead rerun of full repository suite: 1144 passed."
    - "Independent raw route reconciliation and all 22 execution artifact hash/Git-blob checks passed."
    - "git diff --check passed."
  tests_failed:
    - "Both test selections retain the same two documented Windows-versus-frozen-Linux fixture materialization failures; no new failure."
  tests_not_run:
    - "The independent reviewer did not rerun pytest; lead reran the focused and full selections after receiving the review."
    - "No new scientific execution."
  assumptions: []
  unresolved:
    - "The calibrated destination generated no integration-mediated canonical emission; no positive precursor scan was eligible."
  recommended_next_agent:
    - "Return disposition to project owner; no successor task authorized."
---

# Luna-45 independent review

## Disposition

**NOT SUPPORTED IN THIS SETUP.** The required gates passed, but the calibrated
destination produced zero genuine integration-mediated canonical emissions.
This is a valid negative result for the frozen conditions, not a platform
failure, efficacy conclusion, or architecture promotion.

This review was read-only. The reviewer did not edit files, run tests, or
execute a new experiment. The lead reran validation after receiving the
independent review. No Luna-46 or other successor is authorized.

## Exact reviewed revisions and provenance

- Authorization: `9af6b4435ac581887f04f0951d0f7b16d7d661cd`.
- Runner and execution: `97a93b394d071413075a1f102fdef695664722ff`.
- Artifact publication / review revision: `d9fcaa09be60eaec5eb4e4316305a717006d55e9`.
- Branch: `copilot/luna45-depth2-destination-integration`; HEAD equals
  `origin/copilot/luna45-depth2-destination-integration`.
- Runner SHA-256:
  `078a4fb7020414a3a017006291b778576ea72aeff08024063d7040ffe3307085`.
- Configuration digest:
  `cb6621ff403836e1b72b86a65375df11c2841df61030fbe5dd8a654a70394c1a`.
- Frozen fixture: 3,451,453 bytes; SHA-256
  `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`;
  semantic digest
  `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`;
  seeds 0–4, 320 sequences, 5,164 ordered points.
- Complete manifest: SHA-256
  `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22`;
  revision `86e5a2f389af06b06bf04a614edaed88e0847902`; Git blob
  `eb9179abae7eed10891e6022832f16735111b220`.
- Execution-integrity catalog SHA-256:
  `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`.

The reviewer independently checked all manifest source-file pins at their
declared Git revisions and compared the fixture against all six arm/phase
input projections: 1,920 sequence records and 30,984 point records, with zero
fixture-sequence, raw-identity, point, computed-source-value, or audit
mismatches. The runner loads the committed fixture and its verifier; no
benchmark or builder path is called for scientific input. A transitive
`tpcn.spiral_benchmark` import is not a generator call; the corrected focused
test replaces generation entry points with failing guards.

The final configuration file SHA-256 is
`a19bf911ebe04c52aba7d83e376faac853519db3308419ca8bfcad35143858e1`.
The final committed authorization-handoff Git-blob SHA-256 is
`498ce49dd8f32f9d971f1c893e46bdce9ea2247007e66461512e885a6e3e41d9`;
the separately pinned checkout bytes are
`c326548c8bd1b6795caca1bc2694993523c291ff1845e47b4f7e0c64dc61228e`.

## Independent gate results

| Gate | Result | Independently observed evidence |
|---|---|---|
| Frozen fixture, full provenance, no scientific generator call | PASS | Exact identity and all source pins verified; 1,920 arm/phase records and 30,984 points match. |
| G1 Luna-44 calibrated upstream | PASS | 320 historical calibrated records; zero field mismatches. 1,715 source emissions and first-hop enqueues/receptions; 235 integrated relay emissions and onward enqueues. |
| G2 cross-arm invariance | PASS | 960 sequence/arm comparisons per phase; zero upstream mismatches. |
| G3 independent queue/reception evidence | PASS | Distinct `EventQueue.push_propagated` and successful `MultiExcursionNeuron.receive_event` capture sites; source equality on all 11,700 routed pairs. |
| G4 resource bounds and settling | PASS | Maxima: queue 3/128; runtime 107/1024; activity 25/1024; neuron 69/4096; eligibility 19/1024; predictions 1/8; topology 2/3; fan-in/out 1/2; pending events zero. |
| Destination recurrence/discharge and classification | PASS | Independently recomputed production recurrence for all 235 receptions per arm and phase; zero equation, identity, or classification mismatches. |
| Replay | PASS | Initial/replay record sets and reports equal; per-arm digests match; no initial or replay blocker. |
| Candidate-opportunity precursor scan | NOT APPLICABLE | No destination canonical emission, so the required conditional source-to-destination emission-pair scan was not performed. No direct source-to-destination edge exists. |
| Independent-review test rerun | NOT RUN BY REVIEWER | Lead reran the focused selection and full suite after review; results below. |

Raw enqueue/reception reconciliation, independently recomputed from the
published queue and receiver capture files:

| Phase | Arm | Enqueued | Received | Matched | Unmatched/orphan | Source/destination/event/payload/time/path/provenance mismatches |
|---|---|---:|---:|---:|---:|---:|
| Initial | Disabled | 1,950 | 1,950 | 1,950 | 0 | 0 |
| Initial | Default | 1,950 | 1,950 | 1,950 | 0 | 0 |
| Initial | Calibrated | 1,950 | 1,950 | 1,950 | 0 | 0 |
| Replay | Disabled | 1,950 | 1,950 | 1,950 | 0 | 0 |
| Replay | Default | 1,950 | 1,950 | 1,950 | 0 | 0 |
| Replay | Calibrated | 1,950 | 1,950 | 1,950 | 0 | 0 |

Totals are 1,715 source→relay and 235 relay→destination events per
arm/phase; 11,700 pairs across both phases and three arms. The source-only
mutation regression is present and requires reconciliation failure; the
reviewer inspected the test but did not rerun it. Duplicate and orphan
counts are also zero.

## Destination observations

| Arm | Receptions per phase | Direct emissions | Integrated emissions | Maximum `|z|` |
|---|---:|---:|---:|---:|
| Disabled | 235 | 0 | 0 | No integration state |
| Default (`decay_rate_z=0.1`) | 235 | 0 | 0 | 0.39794417177052166 |
| Calibrated (`decay_rate_z=0.0125`) | 235 | 0 | 0 | 0.8284450023885981 |

The calibrated maximum occurred on `c04-017`, after
`relay:excursion:6`, at time `236.40859083136408`; its magnitude remained
below the unchanged discharge quantum 1.0. The default maximum was
0.39794417177052166 on `c01-034` after `relay:excursion:4` at
199.30530327403912. Across all arms there were zero destination discharges,
canonical emissions, direct emissions, integrated emissions, genuine chains,
or unique emitting characters. Emission timing and receptions-before-discharge
lists are empty/not applicable; they were not synthesized.

The conditional candidate-opportunity scan was skipped because no destination
canonical emission occurred. Therefore the review does not claim an ACP-0007
precursor opportunity, growth mechanism, or efficacy.

Initial/replay phase digests:

- Disabled:
  `1f2969a59b1febb8464442143b1bb6da1e0b84f4b256f122c3508133314c4a01`
- Default:
  `abc8c4e288dc4ffb249b62e928c09142dd34fd01491d3deaf95ff5feabc4beba`
- Calibrated:
  `fe3c3a7099f172baf7b0d2633dde34945350b91dd79a8e4f2be81a591eac3ede`

The reviewer independently verified equality of full initial/replay records
and reports plus recorded phase digests, but did not independently reimplement
the producer's canonical phase-digest serializer. All 22 execution files
(386,727,576 bytes total) independently match catalogued SHA-256, length, and
published Git blob; the separate integrity catalog is 7,121 bytes.

## Validation after independent review

Environment: Windows 10 build 19045, CPython 3.11.5, process-local Git
overrides `core.autocrlf=false`, `core.eol=lf`.

- Focused Luna-45 plus Luna-44 provenance, ACP-0008, runtime/routing/topology
  selection: **328 passed, 2 failed**. The two failures are the unchanged
  Windows-versus-frozen-Linux materialization comparisons:
  `test_two_fresh_process_materializations_match_committed_fixture` and
  `test_two_fresh_process_materializations_match_exactly`.
- Full repository suite: **1,144 passed, 2 failed, 1 skipped**. The same two
  known materialization failures occurred; `tests/test_gpu_visualization.py:61`
  skipped because CUDA is unavailable.
- `git diff --check`: passed on the reviewed revision range.
- The reviewer did not rerun tests; the lead executed both selections after
  receiving the independent review.

## Scope, limitations, and disposition

The published worktree is clean. The change from runner revision to artifact
publication contains only the new Luna-45 artifact set and execution handoff;
the earlier stop handoff remains unchanged. No production, ACP, topology, or
architecture contract changes occurred. ACP-0008 remains experimental,
opt-in, and unpromoted; ACP-0007 remains unchanged and disabled. Historical
Luna-42/43/44 verdicts remain intact.

**Final scientific disposition: NOT SUPPORTED IN THIS SETUP.** The fixed
calibrated destination did not produce an integration-mediated canonical
emission after the second ordinary `w=1` hop, despite passing the required
provenance, upstream, causal-routing, bounds, recurrence and replay gates.
This result does not authorize tuning, promotion, or Luna-46. Return it to the
project owner for any separately bounded successor decision.

## Corrective evidence review addendum — 2026-10-06

### Independent disposition

**PASS — corrective verification mechanics are sound; no blocking correctness
findings.** A fresh read-only Luna-0 review inspected branch revision
`de6df64afda00d9ee4a63aa4de52d35c895b31a9`. The corrected ancestry logic
follows only retained production causal roots, verifies root identity and
lineage across source emissions/admissions/receptions and the relay emission,
and requires exact root coverage at both hops and the destination emission.
Focused tests exercise valid roots, roots excluded despite temporal proximity,
and malformed, missing, extra, duplicate, truncated, or mutated provenance.

Replay acceptance now requires both canonical byte equality and matching
SHA-256 digests. Per-arm comparisons retain canonical byte lengths, hashes,
equality results, and first-byte-difference context when unequal. The
read-only verifier recomputes canonical phase material for all initial/replay
arm files and checks those hashes against the phase artifacts and summary.

### Evidence and limitations

- Corrective code/test commit: `2392b78fe5ed0ae773ac957cd0b384c71d0f1eed`.
- Corrective evidence publication: `de6df64afda00d9ee4a63aa4de52d35c895b31a9`.
- Retained execution revision remains
  `97a93b394d071413075a1f102fdef695664722ff`; no experiment rerun occurred.
- Verification JSON SHA-256:
  `547336A1140EA89B6B85CC76807AC5E931FB402296AEBE759165804ECD6C103F`.
- All 22 catalogued retained artifacts match their recorded byte lengths and
  SHA-256 values. For each of the three arms, initial and replay canonical
  phase bytes are equal, their byte lengths and hashes match, and no first
  difference exists. Recomputed hashes match the declared phase and summary
  digests.
- The retained experiment has zero destination canonical emissions, so there
  is no actual destination chain to verify. This is **NOT APPLICABLE**, not
  evidence of a real retained chain; the positive ancestry mechanism is
  covered by synthetic tests.
- The reviewer noted that the verifier's no-mutation assertion is descriptive
  rather than a before/after snapshot. This is non-blocking: the verifier
  reads the original evidence, writes only its separate output, and all
  catalogued hashes independently still match.
- Review scope was read-only; the reviewer did not rerun tests, the verifier,
  or the experiment. The lead's CPython 3.11.5 validation was: Luna-45 focused
  tests **75 passed**; relevant regression selection **332 passed, 2 failed**;
  full suite **1,164 passed, 2 failed, 1 skipped**. Both failures are the
  documented Windows-versus-frozen-Linux fixture materialization comparisons;
  the CUDA test was skipped. `py_compile` and `git diff --check` passed.

The original scientific disposition remains **NOT SUPPORTED IN THIS SETUP**.
The independent review authorizes no scientific re-interpretation, tuning,
promotion, successor, or Luna-46.
