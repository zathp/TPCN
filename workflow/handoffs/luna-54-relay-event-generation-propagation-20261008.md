# Luna-54 retained-input relay event-generation and propagation

**EXECUTED — SUPPORTED WITHIN THE CONTRACTED BOUNDED MECHANISM; INDEPENDENT
LUNA-0 REVIEW PENDING.** Execution stopped at this result. This is not task
efficacy, generalization, production configuration, architecture promotion, or
hardware evidence. No Luna-55 or other successor is authorized.

## Contract and frozen conditions

The run started from the authorized clean baseline
`09701f7c5a1d7063dffecb7734eb199d1c0b0176`. The experiment replays only the
exact authenticated Luna-45 source-to-relay E2 receptions, using the retained
Luna-45 relay and destination configurations and the existing governed E2
runtime/relay-to-destination route. The historical control relay uses
`decay_rate_z=0.0125`; the sole intervention is relay
`decay_rate_z=0.00125`. The destination remains at `0.0125`; source, other
neuron settings, edge, topology, delays, route, and bounds are unchanged.
Evaluator strata are attached after execution; labels do not enter neural
computation.

The Luna-45 initial and replay retained phase digest is
`fe3c3a7099f172baf7b0d2633dde34945350b91dd79a8e4f2be81a591eac3ede`; the
authenticated source-to-relay input digest for both is
`d73c99d83847b50bb5cb66920b95c3546d818874f582b6b6d9d8c5bfa90aaa3b`.
Each phase contains 320 streams, 1,715 source-to-relay input events, and 235
historical relay-to-destination pairs. Preflight independently recomputed the
phase digests and reconciled input enqueue/reception identities, timestamps,
ordering, payload bits, lineage, roots, and routes.

Pinned inputs and unchanged runtime source identities are recorded in every
phase artifact. At the starting baseline, the retained evidence identities
were: Luna-45 catalog Git blob
`b1aaef4006422f321922bfb58425e4fb646d96b9`; Luna-46 retained result Git blob
`9506369d97babf7bc0ef15ed52efb738dcdcd549` (file SHA-256
`0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e`); and
Luna-53 summary Git blob
`b03993adfb358c575c80f6637e7b50903061ddb2`. The phase artifacts pin the
initial/replay Luna-45 arm, enqueue, and reception artifacts individually.
The E2/event-runtime/topology Git blobs and source hashes are also recorded
per run; no core/runtime source was changed.

## Four phase records

All phases report `PASS`, 320 streams, finite bounds, complete route
reconciliation, and a passing independent recurrence audit. Each phase
artifact contains every source input and its ID/time/order/payload/lineage,
all runtime events, relay and destination traces/states, emissions, route
enqueues/receptions, recurrence checks, and resource measurements.

| Phase | Invocation ID | Execution revision | Scientific digest | Artifact digest | File SHA-256 |
| --- | --- | --- | --- | --- | --- |
| Control / initial | `L54-CONTROL-INITIAL-004-20261008` | `632378c553c3828e7a7a200df142e1134829978d` | `a4e07430b0cea7d682f867c7244cfc2ffbcf96d37c409b98ff04cc1ad1b20272` | `57346d5c439b216263f1882452a9140665865e53ca45a5ab414dc40def7e4448` | `2d63eb997676b38a6f09a128a8ce353bdec4e32667d589f9a2089c62b2334751` |
| Control / replay | `L54-CONTROL-REPLAY-001-20261008` | `4f2d9850b71a87edc0751dd25a178465ca1d7dd8` | `a4e07430b0cea7d682f867c7244cfc2ffbcf96d37c409b98ff04cc1ad1b20272` | `c9d1742d478194414903d05c4280dc8aac34727cdfa1015628a360ebe2ffd1b5` | `9f1dacf0a41945087d76ca231c0a0abff89ecc7e488d3df2949f4c489952d53b` |
| Intervention / initial | `L54-INTERVENTION-INITIAL-001-20261008` | `e2fc448baf52afe957ad4bbe072d221b9480676d` | `4170a2688438a2f86a7b9c907d86efff006309ecdc5bf57e14011d6a5033ed54` | `68e7d9369ee7cf72882c392f4695fba2659fb941dc688d02f973e382cb84d68b` | `62b4fe16da456a37ffe7014d495ce1e74ddad174bd853e1656a40256eee7b702` |
| Intervention / replay | `L54-INTERVENTION-REPLAY-001-20261008` | `e2fc448baf52afe957ad4bbe072d221b9480676d` | `4170a2688438a2f86a7b9c907d86efff006309ecdc5bf57e14011d6a5033ed54` | `9e58cbe47ee82c20280e7fe710f8d2d5c4484c85658207d16a6a0a1e0e89ddde` | `d7c3d69f9a6f184517eb465393eb6ace57e9210ef27a8cd5e8a5c52e1fb57bc4` |

Control initial and replay reproduce all 320 historical stream results, all
1,715 source-to-relay inputs, all 235 relay emissions/routes/destination
receptions, and zero destination threshold crossings, with zero field
mismatches. Same-condition initial/replay stream records are byte-identical
after canonicalization and have identical scientific digests. The intervention
uses the same authenticated source input digest and same-condition replay is
also byte-identical. Route reconciliation is 235/235 for each control phase
and 421/421 for each intervention phase, with zero mismatches. Source root
metadata is preserved without truncation. The bounded E2 runtime marked some
onward relay routes as root-truncated: 5 in control (all in the primary group)
and 7 in intervention (3 primary, 4 upstream-active `NO-RECEPTIONS`, 0 in the
other strata). Every one of the 78 additional primary emission IDs is
non-truncated on both enqueue and reception, with matching complete roots and
exact originating-emission identity; these alone qualify for the primary
response. Truncation flags on other routes are preserved in the phase records,
not misrepresented as complete lineage.

## Results and decision

The primary group is the predeclared 75 `DRIVE-LIMITED` streams (676 retained
inputs in each condition). The control produced 109 relay discharges, 109
linked canonical relay emissions, and 109 destination receptions. The
intervention produced 187, an increase of 78 linked emissions and 78
destination receptions. **65/75 streams** had an increased linked relay
emission count and increased routed-reception count; the exact stream and
additional event-ID lists are in `summary.json` under
`primary.complete_valid_routed_increase_streams` and
`primary.new_linked_emission_ids_by_stream`. All 187 treatment relay
emissions were canonically emitted and reconciled to a destination reception.
The destination crossed its own discharge threshold zero times in the control
and zero times in the primary intervention group; it emitted nothing there.
Relay discharge/emission/routing is therefore not conflated with destination
threshold crossing.

Every retained source-to-relay event integrated exactly once at the relay:
676/676 in the primary group, 558/558 in the upstream-active no-reception
group, 0/0 in the 23 zero-input streams, and 481/481 in the temporal group.
Each relay discharge reported in these results corresponds to one canonical
emission; each emission has exactly one reconciled destination enqueue,
reception, and destination integration. Destination counts by group are
therefore given separately in the table and crossing counts remain distinct.

The contract-required secondary strata remain distinct:

| Evaluator stratum | Streams / retained inputs | Control relay emissions / destination receptions | Intervention relay emissions / destination receptions | Increased / complete-lineage streams | Destination threshold crossings (control → intervention) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `DRIVE-LIMITED` (primary) | 75 / 676 | 109 / 109 | 187 / 187 | 65 / 65 | 0 → 0 |
| `NO-RECEPTIONS` with upstream input | 189 / 558 | 0 / 0 | 65 / 65 | 58 / 54 | 0 → 0 |
| `NO-RECEPTIONS` with zero source input | 23 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 → 0 |
| `TEMPORAL-RETENTION-LIMITED` (reported separately) | 33 / 481 | 126 / 126 | 169 / 169 | 33 / 33 | 0 → 1 |

The 33-stream secondary group also had one destination discharge and canonical
destination emission under intervention; this is reported as the contracted
secondary outcome, not used to broaden the primary claim. The 23 zero-input
streams remained isolated: no relay integration, discharge, emission, route,
destination reception, or crossing in either condition. The 189 upstream-
active `NO-RECEPTIONS` streams are not treated as negative controls; 65
acquired a relay emission/reception in intervention, with 58 streams showing
an increase. Four streams have only root-truncated additional treatment
routes and therefore do not count as complete-lineage increases; 54/58 have
at least one complete-lineage increase. This remains secondary and does not
contribute to the primary verdict.

Class-level max-absolute-z and margin-to-unit-discharge-quantum (`1 - max
|z|`) outcomes are:

| Stratum | Relay max `|z|`, control → intervention (margin) | Destination max `|z|`, control → intervention (margin) |
| --- | --- | --- |
| `DRIVE-LIMITED` | `1.285688` (−0.285688) → `1.471807` (−0.471807) | `0.542715` (+0.457285) → `0.667750` (+0.332250) |
| `NO-RECEPTIONS` with upstream input | `0.995339` (+0.004661) → `1.337691` (−0.337691) | `0` (+1.000000) → `0.400760` (+0.599240) |
| `NO-RECEPTIONS` with zero input | `0` (+1.000000) → `0` (+1.000000) | `0` (+1.000000) → `0` (+1.000000) |
| `TEMPORAL-RETENTION-LIMITED` | `1.369273` (−0.369273) → `1.592523` (−0.592523) | `0.828445` (+0.171555) → `1.003884` (−0.003884) |

The summary verdict is **SUPPORTED** for the narrow, bounded relay
event-generation/propagation mechanism: the sole relay decay intervention
produced additional linked canonical relay events that were routed to the
unchanged destination in 65 of 75 predeclared primary streams. It does not
show downstream destination emission in that primary stratum and does not
establish task efficacy or generalization.

## Recurrence, bounds, and execution audit

The independent binary64 oracle replays `z` state from zero through the
timestamp-ordered per-neuron E2 event timeline, including intervening internal
events, and checks decay, input, discharge, state, and destination threshold
outcomes with `64 * epsilon * max(1, |observed|, |expected|)` for state
comparisons and no threshold tolerance. It passed all 1,715 relay input
updates and 235 control / 421 intervention destination updates in each phase.
The oracle checks exact runtime event elapsed times; no input/source generation
or proxy recurrence is used.

All conditions use queue capacity 128, runtime event budget 1,024, per-neuron
budget 4,096, and settling horizon 4.0. The observed peak queue occupancy was
19; peak runtime events were 38 in control and 43 in intervention; peak relay
neuron events were 32 and 36; peak destination neuron events were 6 and 8.
Every stream completed settling with zero pending events. All resource and
finite-state bounds passed, and every enqueue/reception pair reconciled. No relay or destination `z` input
update clipped to its configured `z_max`, and no recorded integration trace
reached `x_max`. All 23 zero-input streams remained silent. Route-root
truncation is explicitly reported above; no truncated route is used as a
qualifying additional primary event.

Execution environment: CPython 3.11.4, Windows 10 build 19045, AMD64,
IEEE-754 binary64 (`epsilon=2.220446049250313e-16`, 53-bit mantissa).

Several initial **runner attempts**, all before any treatment phase, were
aborted and are retained transparently. The first `blocked.json`
(`d3413a741ca32a07978ba7fbad9c015191292ead9d8428848fb4723640825b33`)
records a recurrence-auditor failure: its first implementation incorrectly
assumed consecutive integration inputs were consecutive neuron events. A
second attempt exposed that the independent oracle also had to decay through
intervening E2 internal events. The oracle was corrected to audit the full
per-neuron runtime event timeline; the corrected historical control initial
and replay then both passed all reproduction gates before intervention was
run. Three later command attempts exposed environment/CLI
result-serialization defects; one produced no phase artifact, and two phase
artifacts were fully written and passed but their CLI summaries failed after
write. Those reporting defects were corrected without changing the scientific
inputs or recurrence engine. The persisted control artifacts and replay
checks were loaded and verified before treatment. The first blocked record is
preserved, not misrepresented as a scientific control failure or silently
deleted.

The final summary supersedes and preserves the earlier derived summaries and
integrity catalogs made before the metric-label and lineage-diagnostic
corrections. Those files remain in the integrity catalog with
`-pre-...-correction.json` names; no phase data was rewritten.

## Published result artifacts

- `artifacts/luna54/control-initial.json`
- `artifacts/luna54/control-replay.json`
- `artifacts/luna54/intervention-initial.json`
- `artifacts/luna54/intervention-replay.json`
- `artifacts/luna54/summary.json` — artifact digest
  `a9bb2601051be1a36caac84e0c1c8a9ea06850f26b9b500190adfd69d237ff3c`,
  LF file SHA-256
  `8ec93dd6c83719feba7a34cd85239bf684cc47813c3d5a6cba5197ad781cb684`,
  exact CRLF materialization SHA-256
  `519e69b21ac797b12d3b802061189ddd52dd0e22a7feab52c61de852a2bd0f47`
- `artifacts/luna54/integrity.json` — artifact digest
  `166169d6dee66651ddf8db12460bb2b1186e6ab27be6bbc6213e8dff8d7c508e`,
  LF file SHA-256
  `8ec53ad073c76761d68b8409b748e0d4a373778770c05ff391d246e3793c32b2`,
  exact CRLF materialization SHA-256
  `8e0e7826e7bc910c8b5b9cadac896b5456e479021049b7c81c5f44b173cf56d9`

The final integrity catalog validates all twelve catalogued files and internal
digests, recomputed phase digests, authenticated inputs, historical control
reproduction, and relay-to-destination route reconciliations. For every
catalogued JSON artifact, it accepts only the exact LF bytes or their
one-to-one CRLF checkout materialization; all canonical artifact digests stay
identical across that representation.

Final validation on the publication checkout: Luna-54 focused tests passed
**10/10**; full repository suite passed **1,713**, skipped **1**, failed **0**.
The runner preflight and final summary/integrity validation passed.

One full-suite attempt made while the final Luna-54 JSON files were still
uncommitted reported one failure in the unrelated Luna-47F
`test_reproduction_check_is_read_only`: its verifier correctly rejected the
then-visible non-Luna-47F staged/unstaged paths. The other 1,713 tests passed
and one was skipped. The experiment outputs were committed before the final
clean-checkout suite run; no test or diagnostic logic was changed to suppress
that guard.

**Independent Luna-0 review has not occurred. Stop here for that read-only
review. No ACP/A01-A15 change, task-efficacy claim, or successor authorization
is made.**
