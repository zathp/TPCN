---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent review of Luna-44 evidence-quality correction"
  task_id: "luna-0-review-luna44-evidence-quality-20261005"
  component: "Canonical fixture provenance and independent routed-event evidence"
  status: "complete — PASS WITH FOLLOW-UP; task branch not merged"
  contract_version: "1.2"
  branch: "copilot/luna44-independent-routing-evidence"
  base_revision: "b266077e47b71f36dbd87051da3e5b5ec1199b37"
  result_revision: "c271b7812d35b1b951e6e0fc088d28ee8abd8711"
  dependencies:
    - "Luna-44 owner authorization ff4bf51dcaab2e7b66f0409f4d63a33649c3e104"
    - "Luna-44 corrected fixture provenance and independent materialization records"
    - "Evidence-only C correction at 4baab60f87b820db800e04d0eb3277fb0e94f9b3"
    - "Unchanged-configuration scientific rerun at 4baab60f87b820db800e04d0eb3277fb0e94f9b3"
  owner: "Project owner"
  classification:
    - "independent verification"
    - "evidence-quality follow-up"
    - "scientific mechanism supported within the authorized relay-propagation boundary"
    - "no architecture change or promotion"
  hypothesis: "Separate queue-admission and receiver-consumption captures reconcile one-to-one for the frozen Luna-44 conditions and replay."
  counter_hypothesis: "Independent raw event streams contain missing, duplicate, mismatched, or non-causal enqueue-to-consumption records."
  interfaces_relied_on:
    - "Committed Luna-44 canonical raw-point fixture"
    - "EventQueue.push_propagated queue admission"
    - "ExcursionCharacterRuntime._attach route context"
    - "ExcursionCharacterRuntime._process_one event dispatch"
    - "MultiExcursionNeuron.receive_event receiver consumption"
    - "Bounded Model-B source-to-relay-to-destination topology"
  label_information_boundary:
    - "Runner consumes only frozen raw x/y/t fixture values and does not call the point generator."
    - "No label or evaluation metadata is used."
  timing_assumptions:
    - "Use exact binary64 event payload bits and local logical timestamps."
    - "Reception timestamp is the receiving neuron's logical clock after successful consumption."
  reset_boundaries:
    - "The unchanged experiment creates fresh runtime state for each sequence, arm, and replay."
  resource_bounds:
    - "Original fixed queue, event, neuron, eligibility, prediction, settling, and topology bounds are unchanged."
  authorized_scope:
    - "Add independent enqueue/reception evidence capture and replayable, digest-bound artifacts."
    - "Rerun only the exact frozen Luna-44 experiment with the committed canonical fixture, parameters, topology, seeds, and ordering."
    - "Independently review evidence and record findings."
  unauthorized_scope:
    - "No architecture, A01-A15 contract, ACP, neuron equation, integration parameter, threshold, topology, weight, or task-tuning change."
    - "No successor Luna, architecture promotion, efficacy claim, or hardware-equivalence claim."
  controls:
    - "DISABLED relay integration"
    - "DEFAULT relay integration, decay_rate_z=0.1"
    - "CALIBRATED relay integration, decay_rate_z=0.0125"
    - "Same frozen fixture and same-environment replay for all arms"
  measurements:
    - "Independent queue-admission and receiver-consumption identity, payload, timestamp, path, and provenance."
    - "Bounded execution, canonical relay propagation, and deterministic replay."
  information_boundary_check:
    - "Raw x/y/t and identity/order remain canonical fixture identity."
    - "Derived x+y remains a downstream runtime input, independently computed by the runner."
    - "No labels or evaluation outcomes were read."
  hardware_mapping:
    - "Not applicable; CPU software-reference evidence only."
  architecture_invariants_touched:
    - "No A01-A15 clause or production runtime behavior changed."
    - "Observed capture hooks record existing queue and receiver operations only."
  preserves:
    - "Luna-42 PASS WITH FOLLOW-UP."
    - "Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED."
    - "ACP-0007 unchanged and disabled for this experiment."
    - "ACP-0008 experimental, opt-in, and unpromoted."
  architecture_change: false
  proposal: null
  files_changed:
    - "run_luna44_acp0008_canonical_fixture_rebaseline.py"
    - "tests/test_luna44_acp0008_canonical_fixture_rebaseline.py"
    - ".gitattributes"
    - "artifacts/luna44-acp0008-independent-routing-rerun-20261005/"
    - "workflow/handoffs/luna-0-review-luna44-evidence-quality-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added:
    - "Independent enqueue/reception reconciliation and mutation fault cases."
    - "Receiver-consumption requirement and raw capture persistence/replay checks."
  tests_passing:
    - "Luna-44 runner focused tests: 43 passed."
    - "Independent review focused selection: 227 passed."
    - "Broad local selection: 249 passed."
    - "Full local suite under process-scoped LF checkout configuration: 1,089 passed."
    - "Independent fixture manifest, fixture raw-point identity, and raw route-file digest checks."
    - "Compile/import checks and git diff --check."
  tests_failed:
    - "Two fresh-materialization tests reject Windows-generated materializations when compared against the frozen Linux-generated fixture; they are not weakened."
  tests_not_run:
    - "No further scientific rerun after the reviewed unchanged-configuration rerun."
    - "No independent cross-platform determinism claim."
    - "No GPU-only test execution; one CUDA-unavailable test is skipped."
  assumptions:
    - "The declared fixture-generation environment is the scope for its recorded repeated-materialization claim."
    - "Raw initial and replay route artifacts are the evidence source for enqueue-to-consumption reconciliation."
  unresolved:
    - "Task branch is pushed but unmerged; it is not authoritative main."
    - "Historical post-publication materialization A/B output directories were temporary and are no longer available for reopening; their IDs, PIDs, hashes, digests, and comparison are retained in provenance."
    - "Fresh Windows/Python 3.11.5 materializations are identical to each other but differ bitwise from the frozen Linux fixture. No cross-platform identity or determinism is claimed."
    - "The full suite is not entirely green in this environment: the two exact frozen-fixture-versus-Windows-materialization comparisons fail; CUDA test is skipped."
  recommended_next_agent:
    - "Project owner: decide whether to merge the evidence-only branch with the documented platform limitation, and whether cross-platform fixture-generation parity merits a separate authorized task."
---

# Luna-0 independent evidence-quality review

## Outcome and owned scope

**OBSERVED:** Reviewed the pushed task branch at exact revision
`c271b7812d35b1b951e6e0fc088d28ee8abd8711`. It is based on authoritative main
`b266077e47b71f36dbd87051da3e5b5ec1199b37`; the task branch is not merged.
The instrumentation commit is `4baab60f87b820db800e04d0eb3277fb0e94f9b3`;
the unchanged-configuration rerun and retained evidence were published in
`c271b7812d35b1b951e6e0fc088d28ee8abd8711`.

**OBSERVED:** The correction adds evidence-only runner instrumentation,
reconciliation tests, LF checkout attributes for exact-hash inputs, and a
separate rerun artifact directory. It does not change production neuron,
queue, routing, topology, ACP, or architecture behavior. No scientific rerun
was launched by the reviewer.

## Four original findings

| Finding | Disposition | Evidence and limitation |
|---|---|---|
| A — unsupported original two-run provenance claim | **CLOSED** | The current manifest distinguishes one original fixture publication from two later post-publication independent invocations; it states the original independent-materialization count is “not established by retained evidence.” The superseded two-run pre-freeze assertion is not retained as a fact. |
| B — complete manifest not pinned | **CLOSED** | Current 36,113-byte manifest SHA-256 is `6e069f4f948e8a68b93397e12a5c0e4ab46cb5f5189243e6ef62bab2178cdf22`; its exact pinned Git blob at `86e5a2f389af06b06bf04a614edaed88e0847902` is `eb9179abae7eed10891e6022832f16735111b220`. The frozen fixture is 3,451,453 bytes, SHA-256 `66e187350536e6901d8371a1ffbe3e2a0abf3b49341c6ae6c8fed3ae7833b629`, semantic digest `6c262ad1951a48f624d83a594abfc86ffa89d26882b397f6586698c097144305`. |
| C — enqueue/reception not independent | **CLOSED** | Queue admission and successful receiver consumption are distinct capture sites; the four initial/replay enqueue/reception streams are separately persisted and independently reconciled below. No old result was retroactively relabeled. |
| D — two independent fixture runs not performed | **CLOSED, same-environment scope only** | Provenance records two distinct invocation IDs, PIDs, output directories, independently recorded byte/semantic/order/point-bit digests and exact equality in the declared Linux/CPython 3.12.3 environment. Fresh Windows/Python 3.11.5 runs independently reproduced exact A/B equality in that Windows environment, but their resulting fixture differs from the frozen Linux fixture. Cross-environment parity is not claimed. Historical Linux A/B temporary output directories are no longer available for reopening; that forensic limitation remains explicit. |

### Canonical fixture and materialization identities

- Ordered identity digest: `8f9662ce3364ed38d2572bec081f78a1d18a8243d69bd6114bb6fa50a32fe940`.
- Exact raw XYZ bits digest: `6fbed2a68c88ba17c142ef7933ea20e57837ebbb527bba87c25c7c3fe50cf5db`.
- Sequence/point inventory: 320 sequences, 5,164 ordered points.
- Historical post-publication invocation A: ID
  `16d3c11dbfec4963b582377c3ec9939c`, PID 5320.
- Historical post-publication invocation B: ID
  `b6187d9a674045488e01d7cdcc5d7a58`, PID 5323.
- Both historical invocations record the same fixture file SHA, semantic
  digest, sequence/order digest, exact XYZ digest, byte length and counts.
- Authorization handoff SHA-256:
  `a2baf6e0f6fefae6ec5e108688de965940242d34f109b1143c3f6909699cbe40`.

The reviewer independently checked 20,656 decimal/hex binary64 round-trips,
all 5,164 raw-point audit additions, per-sequence raw/audit digests, source
file hashes and fixture ordering/batching.

### Rerun identity and outcome

The frozen fixture, seeds/order, arm parameters and topology are unchanged.
The runner revision is `4baab60f87b820db800e04d0eb3277fb0e94f9b3`, runner
source SHA-256
`2bfd6341b0c2db496ad51efbf4fe6855d25f10824cac72fbd3303d4f1bc5664d`.
The experiment config digest is
`942b86a9cd7a3965265ec9d01aff7e0b0e2bf68b309f0e0bd22dc4cbae71884e`.

**OBSERVED:** The retained rerun is `PASS / SUPPORTED`; initial and replay
records are equal for all 320 sequences in all three arms. Replay digests:

| Arm | Initial and replay digest |
|---|---|
| DISABLED | `edc1c622e4f50f6507dc720350d59d9299fd5863d04d8d6e5cf226e78b855de2` |
| DEFAULT | `fb9a6b7d7533992979430e5c014ce21d58eee61e29ec9af91e4614a598ddcde2` |
| CALIBRATED | `b40e4607f0602cc6adcb24f16b4001529a8307d49858fa0121ca4c8cb6bf36af` |

### Independent routing capture

The enqueue capture occurs after successful `EventQueue.push_propagated`
admission; production route context is attached separately. Reception capture
occurs after `MultiExcursionNeuron.receive_event` successfully processes the
event and increments the receiver counter. Reception timestamps are taken
from the receiver's logical clock, with before/after receiver state retained.
The capture scope is routed `EXCURSION` events, not internal/control events.

Independent raw reconciliation counts, each reproduced identically for
initial and replay:

| Arm | Source→relay enqueued / received / matched | Relay→destination enqueued / received / matched |
|---|---:|---:|
| DISABLED | 1,715 / 1,715 / 1,715 | 0 / 0 / 0 |
| DEFAULT | 1,715 / 1,715 / 1,715 | 0 / 0 / 0 |
| CALIBRATED | 1,715 / 1,715 / 1,715 | 235 / 235 / 235 |
| **Per phase total** | **5,145 / 5,145 / 5,145** | **235 / 235 / 235** |

Across each phase's 5,380 routed events, unmatched enqueue, orphan reception,
duplicate enqueue/reception, event-ID mismatch, receiver identity mismatch,
payload-bit mismatch, timing mismatch, path/depth mismatch and
causal/provenance mismatch counts are all **zero**.

Four raw artifacts and SHA-256:

| Artifact | SHA-256 |
|---|---|
| `routing-initial-enqueue.json` | `61e0040541a4ac877a833f7d7605138edb065547cb154b7a46bade4de1e7139b` |
| `routing-initial-reception.json` | `d1e24f6239e9f0758e3991a2416d826407a5d12adf73c5ef97762ba89861b44a` |
| `routing-replay-enqueue.json` | `0663fee326614a74fb14770c45b4fbe7abb015c3510afd92022f80a43ac88f69` |
| `routing-replay-reception.json` | `c6aa27f550dc6ac6e7e572b8ade143f36a02707f1041f0a0c45a5452ee83c9b0` |

Representative calibrated chain (`c00-001`):

1. Frozen point 1 has x `-1.6304969211847133`, y
   `-1.4645084625808784`, t `18.99604433078976`; independently derived input
   is `-3.0950053837655918`.
2. Source emission `source:excursion:2` at `19.49604433078976`, payload
   `-0.7737513497173334`, is separately enqueued to relay as admission 7;
   Model-B payload is `-0.6491055026728796`, scheduled for
   `20.49604433078976`.
3. Relay consumes admission 7 at its scheduled logical time; the retained
   receiver state changes `processed_events` from 1 to 2. With calibrated
   integration, `z` reaches `-1.1111036124789162`, discharges by `-1`, and
   leaves `x=-1.649105505968115`, residual `z=-0.1111036124789162`.
4. Integration-mediated relay emission `relay:excursion:1` at
   `20.99604433078976`, payload `-0.41227637649202875`, is separately
   enqueued as admission 10 to destination with payload
   `-0.39040381534442403`, scheduled for `21.99604433078976`.
5. Destination consumes that admission at `21.99604433078976`; retained
   processed-event count changes from 0 to 1 and destination `x` changes from
   0 to `-0.39040381534442403`. The onward route's causal roots are exactly
   `c00-001:input:0` and `c00-001:input:1`; each emitted edge has its own
   route path and depth.

## Architecture, scientific scope, and historical results

**OBSERVED:** No A01-A15 architecture clause, production computation, topology,
or ACP changes. The new artifacts and runner preserve bounded, local logical
event processing. This evidence does not establish task efficacy, energy
benefit, hardware equivalence, architecture promotion, or destination
integration behavior.

**INFERRED:** The authorized Luna-44 relay-propagation endpoint is supported
for this frozen fixture and these three conditions because the calibrated
relay has 235 integration-mediated emissions and each independently captured
onward admission is consumed by the disabled destination.

Historical verdicts remain unchanged: Luna-42 **PASS WITH FOLLOW-UP**;
Luna-43 **BLOCKED / DESTINATION COMPARISON UNDETERMINED**. ACP-0007 remains
unchanged/disabled; ACP-0008 remains experimental, opt-in and unpromoted.

## Validation record and limits

| Command/procedure | Environment | Observed result |
|---|---|---|
| `python -m pytest tests/test_luna44_acp0008_canonical_fixture_rebaseline.py -q` | Windows, Python 3.11.5 | 43 passed |
| Independent Luna-0 focused selection | Windows, Python 3.11.5 | 227 passed |
| Full repository pytest with process-scoped `core.autocrlf=false`, `core.eol=lf` | Windows, Python 3.11.5 | 1,089 passed, 2 failed, 1 skipped |
| Independent exact fixture verification | Windows, Python 3.11.5, canonical LF checkout | 320 sequences / 5,164 points and all pinned identities verified |
| `compileall`, import and `git diff --check` | Windows, Python 3.11.5 | Passed |

The two full-suite failures are exact equality assertions comparing fresh
Windows materializations with the frozen Linux-produced fixture. Two separate
Windows processes agree exactly with one another (fixture SHA-256
`60f551e06072b3fb7e814affa97f4a01e079c426d6044d3e710ad9a219ed907e`,
semantic digest
`2822c60d20569d82a220ef0de80813575f0b5adf240c611e011936cfb50a5876`), but
their raw x/y-derived values do not equal the frozen fixture's values.
Assertions were not weakened. This does not establish cross-platform
determinism; a separate owner-authorized decision is needed for any
cross-platform fixture parity investigation. One CUDA-only test is skipped
because CUDA is unavailable.

The independent reviewer could not reopen historical Linux materialization
A/B output directories because they were temporary; the manifest retains their
distinct invocation/process identities, output paths, hashes, digests and
equality comparison. Fresh local Windows A/B runs independently confirm
separate-process repeatability only for that Windows environment.

## Reproduction and next decision

The exact result is published on the task branch at `c271b78`; it is not
`origin/main`. Reproduce the committed rerun with the runner at revision
`4baab60` and a new output directory, never the historical one. No additional
scientific rerun is required by this review.

**Next:** the project owner decides whether to merge this evidence-only branch
with the stated test limitation and whether cross-platform canonical fixture
parity needs a separately bounded authorization. Do not create a successor
Luna or promote ACP-0008 based on this handoff.
