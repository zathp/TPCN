---
tpcn_handoff:
  agent: "Luna-58"
  luna_identifier: "Luna-58"
  descriptive_name: "Finite destination-retention rescue"
  task_id: "luna-58-finite-destination-retention-execution-20261009"
  component: "Bounded ACP-0008 source-to-relay-to-destination E2 mechanism experiment"
  status: "complete - EXECUTED / SELECTIVE RESCUE SUPPORTED WITHIN THE FROZEN SETUP; independent Luna-0 review required"
  contract_version: "1.2"
  branch: "main"
  base_revision: "7dd3dc868e7518a33418d4df94b07c15dea52adb"
  result_revision: "Scientific implementation and immutable results: 187df41dffed7fad2ed2f5f657575229d5e6d015; this handoff/workflow publication is the subsequent main commit."
  dependencies:
    - "Published Luna-58 contract and one-point authorization at 7dd3dc868e7518a33418d4df94b07c15dea52adb"
    - "Accepted Luna-57 provenance correction at b6b4a54b82cd89f486d2b56495371f9a89b7f5f8"
    - "Pre-execution independent Luna-0 PASS as reported by the project owner"
    - "Authenticated Luna-55 frozen population, source/replay records, RR condition, and selection"
  owner: "Project owner; next action is independent read-only Luna-0 review"
  classification:
    - "single predeclared finite destination-retention mechanism test"
    - "selective rescue supported within this frozen 320-stream software-reference setup"
    - "initial/replay are deterministic checks, not independent samples"
    - "ACP-0008 remains experimental, opt-in, and disabled by default"
  hypothesis: "A destination decay_rate_z of 0.00001, with the relay fixed at 0.00125, produces an actual threshold discharge on each of the six fixed Luna-55 RR nonresponders without changing source/relay/destination-route signatures or crossing in E+, E0, NR1, or NR0."
  counter_hypothesis: "A missed primary crossing, any new specified negative-control crossing, route/input drift, RR control mismatch, nondeterminism, invalid provenance, clipping, pending work, or failed runtime bound blocks the selective-rescue claim."
  interfaces_relied_on:
    - "Authenticated Luna-54 intervention source phases and Luna-55 RR complete causal E2 runner."
    - "Existing Luna-54 bounded source-to-relay-to-destination event path and local event-time integration."
    - "Frozen Luna-55 RR initial/replay records and post-Luna-54 destination-oracle selection."
  label_information_boundary:
    - "PASS: all stream executions receive only fixed source inputs, neuron configurations, topology, and runtime bounds."
    - "The frozen strata are joined only after each stream completes; no label, target flag, evaluator stratum, or oracle result is passed to run_stream."
    - "Initial/replay phases are determinism checks and are not counted as independent samples."
  timing_assumptions:
    - "Source and route timestamps are unchanged; integration uses the existing event-time local elapsed intervals."
    - "No global neural timestep or changed settling horizon was introduced."
  reset_boundaries:
    - "Fresh source/relay/destination runtime state per stream and phase, matching Luna-55."
    - "No reset or refractory transition preceded a primary threshold crossing; the original complete runtime-event trace is retained per stream."
  resource_bounds:
    - "320 streams per condition/phase; 1,715 source inputs and 421 relay-to-destination routes per phase."
    - "Queue capacity 128; runtime-event budget 1,024; per-neuron event budget 4,096; settling horizon 4.0."
    - "Observed phase maxima: queue 19; runtime events 48; relay-neuron events 36; destination-neuron events 13."
    - "All phases: zero pending events, zero clipping, zero bound failures."
  authorized_scope:
    - "Authenticate the contract's seven frozen Git objects and embedded scientific identities."
    - "Freshly reproduce both retained RR control phases before interpreting the single finite destination-decay intervention."
    - "Execute initial and deterministic replay for RR control and the single finite intervention through the unchanged complete causal E2 path."
    - "Add only Luna-58 runner/config/tests/results, one execution handoff, and additive Luna workflow/changelog status."
  unauthorized_scope:
    - "No other decay value or parameter search; no threshold, input gain, payload, timestamp, source, topology, relay, route, model, or budget change."
    - "No edits to core, ACP-0008, Luna-55 source/config/runner/tests, historical evidence, frozen selection, labels, or other runners."
    - "No task efficacy, generalization, production, physical-energy, hardware-equivalence, or architecture-promotion claim."
    - "No Luna-59 or other parameter-search authorization."
  controls:
    - "Authenticated RR initial/replay retained inputs and outputs at fixed object identities."
    - "Ten RR primary responders remain positive controls."
    - "E+ (49), E0 (10), NR1 (189), and NR0 (23) remain distinct negative/control strata."
    - "33-stream secondary temporal-retention stratum is separately reported."
  measurements:
    - "All source inputs, relay emissions, destination receptions, exact route signatures, recurrence audits, integration traces, discharges, emissions, per-stream runtime/resource records, and replay records are retained in four phase artifacts."
    - "421/421 route reconciliation in each phase; seven pre-existing off-target truncation flags match exactly; no target truncation."
    - "Six nonresponders cross 6/6; ten RR responders cross 10/10; E+, E0, NR1, NR0 each cross 0; secondary stratum 33/33 crossing streams and 43 actual discharges/emissions."
    - "Observed first-crossing times and signed input/pre-addition/post-addition/post-discharge z are listed below."
  information_boundary_check:
    - "PASS: retained labels and population membership are downstream-only and the summary records labels_entered_runtime=false."
  hardware_mapping:
    - "Not run; this is software-reference mechanism evidence, not hardware equivalence."
  architecture_invariants_touched:
    - "No architecture/runtime source modified. A01-A03, A07-A08, and A15 are relied on but this is not an architecture conformance certification."
    - "No A01-A15 clause or ACP text changed; ACP-0008 remains experimental/opt-in/disabled by default."
  preserves:
    - "All 55 protected Luna-45/46/53/54/55 evidence artifacts and Git blob identities."
    - "Luna-55 PARTIALLY SUPPORTED disposition within its frozen setup; the six historical RR nonresponders were not reclassified as architectural failures."
    - "All historical source, route, artifact, configuration, and selection identities."
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna58/run.py"
    - "experiments/luna58/config.json"
    - "tests/test_luna58_finite_destination_retention.py"
    - "artifacts/luna58/rr-control-initial.json"
    - "artifacts/luna58/rr-control-replay.json"
    - "artifacts/luna58/finite-initial.json"
    - "artifacts/luna58/finite-replay.json"
    - "artifacts/luna58/summary.json"
    - "workflow/handoffs/luna-58-finite-destination-retention-execution-20261009.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added:
    - "Four acceptance tests verify artifact digests, the sole configuration delta and fixed bounds, per-phase route reconciliation and root-truncation parity, initial/replay identity, separate stratum outcomes, and observed first-discharge values."
  tests_passing:
    - "Committed Luna-58 focused suite at 187df41dffed7fad2ed2f5f657575229d5e6d015: 4 passed."
    - "Full repository suite at 187df41dffed7fad2ed2f5f657575229d5e6d015: 1,752 passed, 1 skipped, 0 failed."
    - "Skip: tests/test_luna46_depth_scaling_diagnostic.py:906, Windows directory symlink unavailable with WinError 1314 (required privilege not held)."
    - "Post-commit experiments.luna58.run --verify: all four phase digests and summary digest valid."
    - "Protected Luna-45/46/53/54/55 artifact object manifest: 55/55 Git blobs unchanged; manifest SHA-256 c984541a505d66429fc7bf8381f783efba94b0db749f80aa6de13ee8857cc61c."
  tests_failed:
    - "One first runner invocation completed an in-memory 320-stream RR-control initial phase, then stopped before writing an artifact or running the intervention because the new runner looked up expected_inherited_truncated_streams in the Luna-54 source configuration instead of Luna-58's contract configuration. The orchestration defect was corrected within the authorized Luna-58 runner. The failed attempt generated no artifact and was not treated as scientific evidence; the subsequent control and intervention phases all passed."
  tests_not_run:
    - "Independent post-execution Luna-0 review: pending; this handoff stops for that review."
    - "Task efficacy, generalization, hardware mapping, calibrated energy, and production suitability: not authorized/not applicable."
  assumptions:
    - "The contract-pinned Git objects at publication revision 7dd3dc868e7518a33418d4df94b07c15dea52adb are authoritative; the contract's authorization paragraph names predecessor c6adc71c26f6226bcbbfb442c4c22cb11cdb3cd2, and that discrepancy is recorded rather than silently substituted."
    - "The exact Git object or its exact LF-to-CRLF materialization is the only accepted raw checkout form."
  unresolved:
    - "Independent Luna-0 review of the final pushed publication remains the next gate."
    - "No claim extends beyond the fixed conditions, streams, event path, and software reference."
  recommended_next_agent:
    - "Luna-0 Architecture Guardian: independent read-only post-execution review; do not implement follow-on work or authorize Luna-59."
---

# Luna-58 finite destination-retention rescue — execution

## Outcome and execution boundary

**EXECUTED — SELECTIVE RESCUE SUPPORTED WITHIN THE FROZEN SETUP; STOPPING
FOR INDEPENDENT READ-ONLY LUNA-0 REVIEW.**

**OBSERVED:** The single predeclared finite destination rate
`decay_rate_z=0.00001` rescues all six fixed Luna-55 RR nonresponders under
the actual complete E2 source → relay → destination event path. All ten RR
responders continue to cross. The separate E+, E0, NR1, and NR0 populations
remain at zero crossings. The secondary 33-stream temporal-retention stratum
is separate: 33 streams cross and have 43 discharges/canonical emissions.
No intervention route, source input, or relay event changed.

This is one bounded ACP-0008 mechanism result. It is not task efficacy,
generalization, production suitability, a physical-energy measurement,
hardware equivalence, architecture conformance, or an architecture/ACP
promotion. Luna-55 remains **PARTIALLY SUPPORTED within its frozen setup**.

## Baseline, authorization and provenance

The actual execution authorization was the published contract revision
`7dd3dc868e7518a33418d4df94b07c15dea52adb`, verified after fetching origin:
`HEAD == origin/main == 7dd3dc868e7518a33418d4df94b07c15dea52adb`, clean
worktree. The contract's authorization paragraph retains the predecessor
`c6adc71c26f6226bcbbfb442c4c22cb11cdb3cd2`; the current contract publication
is used here as the execution authorization SHA, as directed. The project
owner reported the required pre-execution independent Luna-0 PASS for the
accepted Luna-57 correction at `b6b4a54b82cd89f486d2b56495371f9a89b7f5f8`.

The committed implementation state is
`187df41dffed7fad2ed2f5f657575229d5e6d015`. Its Luna-58 runner Git blob is
`62ccfd1a5415bb457a1874b7e45fd04a466ea561` (working-file SHA-256
`175e0e3094c113050474b4a9426981ef55423e02a2d3e5167791a75da2fa1358`); config
blob is `99df94aeb5a3492222f8ad68191e4190a86a53ac`; focused test blob is
`f99953017832a9156781d0a8785a0afdb9060c35`.

The seven required inputs were authenticated by their pinned Git blob at
`7dd3dc868e7518a33418d4df94b07c15dea52adb`, then by exact checkout bytes
(object bytes or exact CRLF form) and the contract's SHA-256. All seven pins
passed:

| Input | Pinned Git blob | Contract checkout SHA-256 |
|---|---|---|
| `experiments/luna55/config.json` | `197ebd8efc5449e1e973d4c6d96bdf12f40e1f31` | `103594c2906fafb60684fc4f67adf22ffc0722eb268506e9d35d027bd98fcbba` |
| `artifacts/luna54/intervention-initial.json` | `6de22f1f5406f378e115a818e01e459ec6ddf3e6` | `62b4fe16da456a37ffe7014d495ce1e74ddad174bd853e1656a40256eee7b702` |
| `artifacts/luna54/intervention-replay.json` | `684fc1f3adfbd26dbbca1a656c1d14c5e8ac92a8` | `d7c3d69f9a6f184517eb465393eb6ace57e9210ef27a8cd5e8a5c52e1fb57bc4` |
| `artifacts/luna55-selection/post-luna54-destination-oracle.json` | `a63a5edddd6f24b2625192b398b74a84125b97bb` | `2ac7b79015c00d5055b1b6226ce23239f691ba07a368e80768737e39f0b2bd57` |
| `artifacts/luna55/rr-initial.json` | `b29e76709a6d502ee8f48aa4e4ea4f31fa9388ca` | `2043a03744af925345a34ee3e7e704914c35f13faf1e9175bab9c9e600ad8b8b` |
| `artifacts/luna55/rr-replay.json` | `61baf5aa4c42a0c518d0c0fbf91e110acd8fe987` | `7445773d6907488501a90d97064ebece57ccb9b0508b75df3f54fbe9a0555085` |
| `artifacts/luna55/summary-v3.json` | `063b03ea84933f930ce95b2fe15e8ee83e0e4172` | `5f1bba890f00c117a019dccf39948ec9b2169579f3ce749c81c03edfd85a3f86` |

The current Luna-55 config checkout is its exact LF-to-CRLF representation;
the other six checkout files are the authenticated Git-object bytes.
Luna-54 initial/replay embedded artifact and scientific digests pass, with
common scientific digest
`4170a2688438a2f86a7b9c907d86efff006309ecdc5bf57e14011d6a5033ed54`.
Both retained RR phase artifact digests and summary-v3's embedded digest
recompute successfully. RR configuration digest is
`d99b31646791f37e9242dfb9089e299dc6ab31e21bc0f96b244e92a6f4bed708`;
the common input-phase digest is
`d73c99d83847b50bb5cb66920b95c3546d818874f582b6b6d9d8c5bfa90aaa3b`.
All 320 selection entries and the frozen 16/49/10/189/23/33 partition were
validated before execution.

## Intervention and finite RR control

**OBSERVED:** Before interpreting the intervention, two fresh bounded RR
control phases were run through `luna54.run_stream` using the unchanged
Luna-55 RR relay and destination configuration. Each matched its respective
retained RR stream set exactly for source inputs, relay emissions, relay and
destination integration traces, destination receptions and emissions,
route reconciliation, recurrence-oracle records, runtime resources, and
destination state. All 421 route signatures in each phase match the
authenticated retained RR routes.

Only after this control reproduced did the runner copy the frozen RR
condition and change exactly
`destination.integration.decay_rate_z: 0.00125 -> 0.00001`.
`relay.integration.decay_rate_z` remained `0.00125`; the config comparison
reports exactly one changed path. Input gain, threshold, fast decay, `z_max`,
source data, payloads, timestamps, topology, route rules, neuron model,
runtime bounds and settling horizon are unchanged.

The execution artifacts are:

| Phase artifact | SHA-256 | Embedded artifact digest |
|---|---|---|
| `artifacts/luna58/rr-control-initial.json` | `5ba742838dc068f244191f672fac0663d74d55f4394ca430e5397acb3e6c99e8` | `9df84a8382944d9b39713a4b652110e9ba11b0eba3b79cfd6d5ce1ea37ca0057` |
| `artifacts/luna58/rr-control-replay.json` | `7d929a1ab053266e6e78e84ebf69d359cd37791b142f59a3d8fda46696cd0fde` | `ec4a0074b11993dc76bb19d216f3a00f556031cf0cfefa9cd8dfd7570b90b330` |
| `artifacts/luna58/finite-initial.json` | `926b44b2a2ab3a576864cd3738b6e9f7fb5ff1df58177fc2af13b17f99c104b4` | `f359e80818d51a788ac2da06e967146db39509c1ccc2a9f6f87b0f36a190a800` |
| `artifacts/luna58/finite-replay.json` | `83b1c9cc2e1720656398e211b7d32c840adefbd267e23d30b2fbb89e0a538977` | `2f1c67362356fd6d46f160cc55c213c5e553f7c23b76040cfcc766afcab41656` |
| `artifacts/luna58/summary.json` | `ba33ac051d305dc526060cbe0edc84b9c50b827edcce03b5be93b84dfd58d1ea` | `3b97221ffffee4d895e6b2663d17af02fd6aca1c36d276051b80a508637a02f3` |

The RR control configuration digest remains
`d99b31646791f37e9242dfb9089e299dc6ab31e21bc0f96b244e92a6f4bed708`;
the intervention's derived effective-configuration digest is
`b81a71fe90b5a7c45602406db07c46e6fbd57d90f8026dad45c3ae73d31837c3`.
All four phase files and summary pass the post-commit
`python -m experiments.luna58.run --verify` digest check.

One initial runner invocation completed a fresh 320-stream RR-control
computation in memory and then stopped before writing an artifact or starting
the intervention: a runner configuration lookup requested the truncation
allow-list from the Luna-54 source config instead of the Luna-58 contract
config. The error and correction are disclosed here; that attempt produced no
artifact and is not scientific evidence. The corrected runner then executed
and retained the four phases above. No scientific parameter was changed or
tuned.

## Causal routes, event recurrence and bounded execution

**OBSERVED:** Each retained phase has 1,715 source inputs, 421 relay
emissions, 421 destination receptions, and 421/421 enqueued/received/matched
routes with zero mismatches. For every stream, the full destination signature
including event ID, payload bits, timestamp, source, destination, causal roots,
lineage, route depth/path and scheduled delivery time is identical between
fresh RR control and intervention. Source inputs and relay event objects also
match exactly. Initial and replay `streams` objects are exactly equal within
both conditions.

The seven inherited truncation IDs are exactly
`c00-019, c00-059, c01-006, c01-008, c01-035, c02-058, c04-046` in every
phase, with no new flags. All 16 primary targets have complete source and
relay root expansion and zero truncation. Independent relay and destination
E2 recurrence oracles pass for all 320 streams in all four phases. Every
stream settles, has zero pending events, passes queue/runtime/per-neuron/state
bounds, and has no clipping. Measured maxima are queue 19/128, runtime
48/1,024, relay neuron 36/4,096, destination neuron 13/4,096.

All phase records retain the complete per-stream source-input, relay
emission, destination reception, route, integration, state, discharge,
runtime-event, resource, and replay traces. In the finite initial phase,
the 16 primary targets have 58 destination receptions, 16 discharges and 16
canonical emissions. Their integration events are in mode N before input;
there is no reset or refractory transition before a target's crossing.
Across the primary nonresponders, responders, E+, E0, NR1, NR0, and secondary
strata, observed destination internal transitions are:

| Separate stratum | Streams | Source inputs | Relay emissions | Destination receptions | Crossings | Discharges / S_EMIT | S_REARM | Destination mode before reception |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Six RR nonresponders | 6 | 57 | 18 | 18 | 6 | 6 / 6 | 9 | N for all 18 arrivals |
| Ten RR responders | 10 | 121 | 40 | 40 | 10 | 10 / 10 | 17 | N for all 40 arrivals |
| E+ zero-decay-insufficient | 49 | 436 | 117 | 117 | 0 | 0 / 0 | 0 | N for all 117 arrivals |
| E0 no additional arrival | 10 | 62 | 12 | 12 | 0 | 0 / 0 | 0 | N for all 12 arrivals |
| NR1 upstream active, no historical reception | 189 | 558 | 65 | 65 | 0 | 0 / 0 | 0 | N for all 65 arrivals |
| NR0 no input | 23 | 0 | 0 | 0 | 0 | 0 / 0 | 0 | No destination arrivals |
| Secondary temporal-retention | 33 | 481 | 169 | 169 | 33 | 43 / 43 | 63 | N for all 169 arrivals |

No reset/refractory internal event occurs in these traces; each stream has
fresh state at its declared boundary. `S_EMIT` and `S_REARM` are preserved
from the runtime-event trace and summarized above.

## Primary target actual E2 crossings

Each row records the *observed* first discharge-triggering destination
reception time, signed input, `z` after elapsed decay and before input,
`z` immediately after input, and post-discharge `z`. These are trace values,
not the unreset arithmetic peak after crossing.

| Frozen target | RR | source / relay / destination count | First crossing time | Signed input | z before input | z after input | z after discharge |
|---|:---:|---:|---:|---:|---:|---:|---:|
| c00-011 | N | 9 / 3 / 3 | 213.591223342 | +0.336656685305 | +0.663960996679 | +1.000617681985 | +0.000617681985 |
| c00-032 | R | 11 / 4 / 4 | 178.962071773 | -0.359204730305 | -0.653373554032 | -1.012578284337 | -0.012578284337 |
| c00-037 | N | 10 / 3 / 3 | 216.387230875 | -0.361662935499 | -0.639922079716 | -1.001585015214 | -0.001585015214 |
| c01-012 | R | 13 / 4 / 4 | 242.807160882 | +0.328420262956 | +0.974923637483 | +1.303343900438 | +0.303343900438 |
| c01-020 | N | 10 / 3 / 3 | 281.623657328 | -0.322018582959 | -0.686537754530 | -1.008556337490 | -0.008556337490 |
| c01-041 | R | 13 / 4 / 4 | 234.431737432 | -0.319898974372 | -0.691027166389 | -1.010926140761 | -0.010926140761 |
| c01-050 | R | 12 / 4 / 4 | 191.822645313 | -0.360719467996 | -0.639960286429 | -1.000679754425 | -0.000679754425 |
| c02-010 | R | 13 / 4 / 4 | 283.365428045 | -0.365227676435 | -0.978606343379 | -1.343834019814 | -0.343834019814 |
| c02-015 | N | 9 / 3 / 3 | 257.980581329 | +0.313578584431 | +0.687667239631 | +1.001245824063 | +0.001245824063 |
| c02-019 | R | 13 / 4 / 4 | 265.151743691 | -0.311722276605 | -0.978726418255 | -1.290448694860 | -0.290448694860 |
| c02-023 | N | 9 / 3 / 3 | 263.858830087 | +0.304983530543 | +0.703323710799 | +1.008307241343 | +0.008307241343 |
| c02-046 | N | 10 / 3 / 3 | 308.437076925 | +0.345770872010 | +0.657429607609 | +1.003200479619 | +0.003200479619 |
| c03-023 | R | 10 / 4 / 4 | 190.370835301 | -0.366845059031 | -0.684457318247 | -1.051302377279 | -0.051302377279 |
| c03-058 | R | 13 / 4 / 4 | 308.531524262 | -0.312671199989 | -0.994428342076 | -1.307099542065 | -0.307099542065 |
| c04-001 | R | 11 / 4 / 4 | 248.422932763 | +0.310874567298 | +0.693384964803 | +1.004259532101 | +0.004259532101 |
| c04-043 | R | 12 / 4 / 4 | 276.751534492 | -0.380029832145 | -0.988491443405 | -1.368521275550 | -0.368521275550 |

`N` means noncrossing in frozen Luna-55 RR; `R` means RR responder.
The six predicted RR nonresponders all have an actual integration-threshold
discharge, linked canonical emission and observed first-crossing time.
All ten pre-existing RR responders continue to cross.

## Separate population outcomes

| Population | Count | Source inputs | Relay emissions | Destination receptions | Finite-initial crossings | Discharges | Canonical emissions |
|---|---:|---:|---:|---:|---:|---:|---:|
| Primary RR nonresponders | 6 | 57 | 18 | 18 | 6 | 6 | 6 |
| Primary RR responders | 10 | 121 | 40 | 40 | 10 | 10 | 10 |
| E+ zero-decay-insufficient | 49 | 436 | 117 | 117 | 0 | 0 | 0 |
| E0 no additional arrival | 10 | 62 | 12 | 12 | 0 | 0 | 0 |
| NR1 upstream active/no historical reception | 189 | 558 | 65 | 65 | 0 | 0 | 0 |
| NR0 no input | 23 | 0 | 0 | 0 | 0 | 0 | 0 |
| Secondary temporal-retention | 33 | 481 | 169 | 169 | 33 | 43 | 43 |

Negative/control strata are not combined. The secondary stratum is not
included in the primary claim. Initial and replay produce identical per-stream
results in each condition; these phase pairs are not independent samples.

## Validation and protected historical evidence

| Command/procedure | Revision/environment | Result |
|---|---|---|
| `git fetch origin`; `git rev-parse HEAD` and `origin/main`; clean-worktree check | Before implementation; Windows, main | PASS, both `7dd3dc868e7518a33418d4df94b07c15dea52adb` |
| Frozen Luna-55 preflight | Authorization baseline | PASS: eight historical phase pins; 320 stream partition; both phases check 235 retained arrivals/traces |
| Seven contract-pinned Git objects, checkout hashes, embedded digests | Authorization baseline | PASS |
| Fresh finite RR control initial/replay | Implementation run | PASS; all named measurements and 421 route signatures match retained RR |
| Four Luna-58 phase artifacts and summary self-digests | Implementation run and committed verification | PASS |
| `python -m pytest -q -rs tests/test_luna58_finite_destination_retention.py` | Committed implementation `187df41dffed7fad2ed2f5f657575229d5e6d015`; Python 3.11.4 | 4 passed |
| `python -m pytest -q -rs` | Same committed implementation; Windows | 1,752 passed, 1 skipped, 0 failed |
| Skip detail | Same full run | `tests/test_luna46_depth_scaling_diagnostic.py:906`; Windows WinError 1314 prevented creating a directory symlink because the required privilege is unavailable |
| `python -m experiments.luna58.run --verify` | Committed implementation | PASS; all phase and summary artifact digests |

The authorization tree's manifest over the 55 protected Luna-45/46/53/54/55
artifact paths was reconstructed from the fixed base revision and compared
with the post-execution tree. Its path-to-Git-blob manifest hash remained
`c984541a505d66429fc7bf8381f783efba94b0db749f80aa6de13ee8857cc61c`
(55/55 exact object identities). No protected historical artifact,
selection, runner, test, ACP, core runtime, or architecture contract changed.

## Architecture boundary, unresolved gates and next action

**OBSERVED:** The sole intended destination decay change, source/relay
invariance, exact routing, recurrence, boundedness, deterministic replay,
selective primary rescue, and negative-control silence all passed in this
frozen setup.

**INFERRED narrowly:** lowering only destination `decay_rate_z` to the single
predeclared finite value suffices for actual causal destination discharge on
the six frozen Luna-55 RR nonresponders in this replayable source/path.
The result does not generalize beyond these conditions and streams.

No A01-A15 contract clause, canonical core behavior, or ACP status changed.
ACP-0008 remains experimental, opt-in, and disabled by default. No task,
production, hardware, physical-energy, generalization or architecture
promotion claim follows. No Luna-59 or parameter search is authorized.

## Reproduction and rollback

The immutable phase and summary evidence is under `artifacts/luna58/`.
Post-publication integrity verification is
`python -m experiments.luna58.run --verify`; focused and full test commands
are recorded in the validation table. The scientific command was
`python -m experiments.luna58.run` from the clean authorization checkout
before the run artifacts existed. It is not to be rerun from the publication
checkout: the runner enforces its authorization baseline, and existing output
paths use exclusive creation. Do not invoke it against the published outputs.
No rollback was performed or is requested; if this publication is rejected,
revert only the Luna-58-owned files/records and workflow status, preserving
all pre-existing Luna evidence.

**Next action:** stop here for independent read-only Luna-0 review of the
final pushed publication. Do not perform the review in this execution and do
not implement follow-on work.
