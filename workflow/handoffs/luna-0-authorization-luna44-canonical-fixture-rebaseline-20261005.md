---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-44 canonical point-fixture and relay propagation authorization"
  task_id: "luna-0-authorization-luna44-canonical-fixture-rebaseline-20261005"
  component: "Frozen generated point fixture and bounded ACP-0008 relay propagation comparison"
  status: "complete — Luna-44 AUTHORIZED / NOT EXECUTED; this governance publication is uncommitted"
  contract_version: "1.2"
  branch: "copilot/establish-new-canonical-baseline"
  base_revision: "a79494cd66be28fd291ed11eddd62d342f457cfd"
  result_revision: "uncommitted governance-only changes based on a79494cd66be28fd291ed11eddd62d342f457cfd"
  authorization_revision: "this handoff; obtain its immutable publication revision before Luna-44 begins"
  dependencies:
    - "Explicit project-owner authorization in the 2026-10-05 task direction"
    - "Accepted ACP-0008; opt-in and unpromoted"
    - "Luna-42 PASS WITH FOLLOW-UP and its retained Phase-B protocol"
    - "Luna-43 BLOCKED / DESTINATION COMPARISON UNDETERMINED; historical result preserved"
  owner: "Project owner"
  classification:
    - "governance-only authorization"
    - "bounded canonical-fixture construction and CPU software-reference experiment"
    - "source-to-relay-to-destination propagation with relay-only conditions and deterministic replay"
    - "AUTHORIZED / NOT EXECUTED"
    - "no scientific outcome or architecture change"
  hypothesis: "With an immutable point-level fixture shared by all arms, the predeclared disabled, default, and calibrated relay configurations can be compared and replayed, and integration-mediated relay emissions can propagate over the fixed ordinary onward edge."
  counter_hypothesis: "The frozen fixture cannot be reconstructed exactly, causal routing/replay checks fail, or no integration-mediated relay emission yields an ordinary onward transfer."
  interfaces_relied_on:
    - "Owner-stipulated existing Luna-39/Luna-34 make_spiral_dataset point-sequence generator"
    - "MultiExcursionNeuron and per-neuron ACP-0008 IntegrationConfig"
    - "ExcursionCharacterRuntime and bounded event queue"
    - "BoundedTopology and ordinary Model-B source-to-relay and relay-to-destination edges"
  label_information_boundary:
    - "Use generator seeds 0..4 and its 64 ordered sequences per seed."
    - "Fixture records seed, zero-based sequence index in generator order, deterministic label-free stream ID c{seed:02d}-{sequence_index:03d}, zero-based source-order point index, zero-based sequence-local batch ordinal, raw x/y/t, and x+y as an audit value only; do not use generator metadata IDs or copy/read labels, classes, or evaluation outcomes."
    - "Construct the fixture once from the stipulated generator; the experiment runner loads raw x/y/t from reversible float.hex values (checking decimal round-trip) and never calls the spiral generator."
    - "For every condition and replay, the runner independently computes float(x) + float(y), retains that run's exact derived value, and supplies that value as the point input; it must not feed the fixture's audit x+y value."
    - "Keep raw x/y/t, identity, order, and batching unchanged across conditions and replays; compare each run's derived x+y separately against the fixture audit value under the predeclared policy."
  timing_assumptions:
    - "Preserve generator timestamps and point order; define batches using production _point_batches semantics (float-converted numeric timestamp equality, consecutive points, first-seen order), not generator metadata or bit-identical timestamp grouping."
    - "Use local event timestamps and fixed positive delay 1.0 on both ordinary edges; no global neural timestep."
  reset_boundaries:
    - "Fresh source, relay, and runtime state for each sequence and relay condition."
    - "Replay the same frozen fixture from reset; no cross-sequence neural state."
  resource_bounds:
    - "Retain reviewed Luna-42 Phase-B bounds: queue 128; runtime event/activity budgets 1024; neuron event budget 4096; eligibility capacity 1024 per ledger; prediction capacity 8 / expiry 4.0; settling horizon 4.0."
    - "Finite three-node topology with only source->relay and relay->destination edges; fan-in/out limits 2 and edge/routing capacities 3; no topology mutation."
  authorized_scope:
    - "Construct and freeze one point-level fixture from the owner-stipulated generator using seeds 0..4, exactly 64 ordered sequences per seed; fixture construction may call the generator once, but the experiment runner must load the frozen fixture and must never call the spiral generator."
    - "For every point, freeze seed, zero-based sequence index in generator order, deterministic label-free stream ID c{seed:02d}-{sequence_index:03d}, zero-based point index in source order, zero-based sequence-local batch ordinal, raw x/y/t, and x+y as a fixture audit value. Store every float as decimal text that round-trips to the same binary64 value and an exact reversible binary64 representation (prefer float.hex); never use generator metadata IDs that may contain labels."
    - "Define same-time batches by production _point_batches semantics: convert timestamps to float, reject decreasing numeric timestamps, and group consecutive points while converted timestamps compare numerically equal (including +0.0 == -0.0); assign batch ordinals in first-seen order and preserve within-batch point order."
    - "Define the canonical SHA-256 over ONLY the ordered seed/sequence/deterministic-stream/point/batch identities and exact raw x/y/t binary64 bits; use canonical UTF-8 JSON (sorted keys, compact separators). Exclude fixture audit x+y, neural outputs, events, and condition results. If useful, a separate audit digest may bind canonical fixture identity to ordered x+y audit bits, but it is not the canonical fixture digest."
    - "Construct the fixture audit x+y using production-declared float(x) + float(y), retaining its exact decimal and float.hex representations; this stored value is for audit/comparison, not runtime input."
    - "Before any condition run, publish the canonical fixture, point/sequence counts, exact raw x/y/t input digests, fixture digest, generator/source identity, fixture-generation revision, environment, and provenance."
    - "Run only three relay conditions: source integration=None; relay integration disabled (None), default IntegrationConfig() (decay_rate_z=0.1), or calibrated IntegrationConfig(decay_rate_z=0.0125); destination integration=None in every arm."
    - "Use only fixed ordinary Model-B edges source->relay and relay->destination, each delay 1.0, w=1.0, d=1.0, r=0.0. Hold all other neuron/runtime settings, topology, fixture, and ordering fixed to the reviewed Luna-42 Phase-B configuration and bounds."
    - "Require each integration-mediated relay canonical emission to reconcile to its actual ordinary relay->destination transfer; require at least one such causally matched onward transfer for the relay-propagation endpoint to be met. Do not require any historical count."
    - "Perform a same-environment deterministic replay of each condition. Record authorization revision and handoff digest, fixture-generation revision and fixture digest, runner revision and file hash, execution revision and execution/artifact digests, plus configuration, run, and replay identities."
    - "Own only a new Luna-44 fixture builder/fixture, runner, focused tests, artifacts under a new Luna-44 directory, and completed execution handoff; return to Luna-0 for independent review."
  unauthorized_scope:
    - "No destination integration variation or destination-state/emission comparison; destination integration stays disabled and is used only to receive ordinary onward transfers."
    - "No destination-response, task/classification efficacy, prediction benefit, reward/utility result, or energy benefit."
    - "No changes to production APIs, neuron equations, routing/topology semantics, ACP-0007, ACP-0008, architecture contract, or prior experiment criteria."
    - "No WEMA, structural growth/pruning, calibration search, parameter tuning, hardware-equivalence claim, architecture promotion, or successor assignment."
    - "Do not touch .github/agents, Python/code/tests outside new Luna-44-owned paths, or any historical Luna-42/Luna-43 handoff or artifact."
    - "No Luna-45 authorization."
  controls:
    - "Three predeclared relay integration conditions: disabled, default 0.1, calibrated 0.0125; source and destination integration disabled in every arm."
    - "Identical frozen point fixture and source configuration in all conditions."
    - "A second run from reset for each condition using the identical fixture."
    - "Fixed ordinary w=1, delay=1 source-to-relay and relay-to-destination Model-B edges; ACP-0007 disabled."
  measurements:
    - "Fixture point/sequence counts, ordering, exact input digests, canonical fixture digest, generator and repository provenance."
    - "Exact raw x/y/t fixture identity across arms and replays; per-point, per-condition, per-replay derived x+y observed/expected/residual/tolerance evidence, with the observed value used as the runtime input."
    - "Source canonical emissions, relay integration traces/emissions, and ordinary first- and onward-hop route/reception identities, timestamps, paths, payload copies, and counts."
    - "Causal reconciliation from each integration-mediated relay canonical emission to its ordinary relay->destination transfer; no historical count target."
    - "Per-relay-condition direct/integrated/none emission classifications, bounded state, resource high-water marks, settling, and replay digests."
    - "Separate observed, expected, residual, and tolerance for each applicable floating equation quantity."
  information_boundary_check:
    - "Runtime loads exact frozen raw x/y/t and computes float(x) + float(y) per point in each condition and replay; it does not consume the fixture audit x+y as input. Labels and evaluation records are absent from the fixture and condition selection."
  hardware_mapping:
    - "CPU software-reference only; hardware equivalence not run and not claimed."
  architecture_invariants_touched:
    - "A01/A02/A03: event-triggered local-time processing, ordered fixture events, and finite-delay two-hop routing."
    - "A04: fixed finite three-node topology and declared capacities."
    - "A07/A08: local bounded neuron state and execution; no labels or global task input."
    - "A14: structural adaptation disabled."
    - "A15: no hardware-equivalence claim."
  numerical_policy:
    fixture_and_input_identity: "For every point, preserve seed, zero-based sequence index in generator order, deterministic label-free stream ID c{seed:02d}-{sequence_index:03d}, zero-based point index in source order, zero-based sequence-local batch ordinal, and raw x/y/t; exact raw binary64 values and point identities must match across arms/replays. Retain x+y only as a fixture audit value. Apply production _point_batches semantics: convert t to float, reject decreasing numeric timestamps, group consecutive points whose converted timestamps compare numerically equal (so +0.0 and -0.0 share a batch), assign batch ordinals in first-seen order, and preserve within-batch point order. Per-sequence raw-input digests and the canonical UTF-8 JSON/SHA-256 bind ONLY ordered identities and exact raw x/y/t bits. Exclude audit x+y and neural results from canonical identity. No tolerance or normalization applies to raw identity."
    point_input_payload: "For each point in every arm and replay, independently execute production-declared float(x) + float(y) from the exact raw fixture values, retain the run's decimal and float.hex derived value, and use that observed value as the event input. Compare it separately to the fixture's audit x+y using 64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected)); report observed, expected, residual, and bound per point/run. Predeclare this comparison before fixture construction; do not infer it from Luna-43's mismatch."
    exact_behavior: "Exact sequence/point counts, raw fixture identity/digests, event identity/order, route, condition, event classification/count, copied queued-payload-to-reception identity within a run, topology, and same-environment replay digest. Derived x+y is compared separately under point_input_payload policy."
    elapsed_time: "For each relay event, dt must be the exact binary64 subtraction of its ordered timestamps; report the observed and recomputed dt and require exact equality."
    source_emission_payload: "For each event, compare the independently reconstructed source-emission payload using 64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected)); retain observed, expected, absolute residual, and bound."
    model_b_routed_payload: "For each ordinary edge event, compare the independently reconstructed Model-B payload using the same formula; separately require each receiver to copy that run's queued routed payload exactly."
    onward_route_time: "For each relay->destination transfer, compare the derived arrival timestamp (relay emission timestamp + fixed edge delay 1.0) using the same formula; require strict-future causality, exact event/route identity, and exact same-run copied payload at reception."
    relay_recurrence_quantities: "For each applicable event, require elapsed-time delta to equal the difference of the exact captured timestamps; compare x/z after elapsed-time decay, x/z after input, discharge amount, and post-discharge x/z against the independent recurrence oracle using the same formula, reporting each field separately."
    bounds_and_classification: "Hard configured state/resource bounds and discrete threshold/emission classifications remain exact runtime acceptance checks; the floating equation allowance cannot waive them."
    derivation: "The multiplier and formula are fixed before fixture construction as a binary64 equation-reconstruction policy. They are not selected, expanded, or justified from the historical Luna-43 point mismatch."
  preserves:
    - "Luna-42 remains PASS WITH FOLLOW-UP."
    - "Luna-43 remains BLOCKED / DESTINATION COMPARISON UNDETERMINED; its partial record and historical artifacts remain untouched."
    - "ACP-0007 remains disabled and unchanged."
    - "ACP-0008 remains opt-in and unpromoted."
    - "No A01-A15 contract revision or ACP is proposed."
  architecture_change: false
  proposal: null
  files_changed:
    - "workflow/handoffs/luna-0-authorization-luna44-canonical-fixture-rebaseline-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "No experiment, runner, replay, or test suite was executed in this governance-only pass."
    - "No independent Luna-0 review of future Luna-44 execution evidence has occurred."
  assumptions:
    - "The explicit project-owner direction authorizes the generator protocol and three-condition relay-propagation/replay scope stated here."
    - "The accepted Luna-42 Phase-B source/runtime bounds apply unchanged unless the frozen Luna-44 configuration records a narrower bound."
    - "The repository's governance root is workflow/; there is no tpcn-luna-workflow/ directory in this checkout."
  unresolved:
    - "The authorization handoff and workflow/changelog edits are uncommitted; Luna-44 must not start until it can record and verify the immutable publication revision."
    - "No origin/main ref exists in this shallow checkout. The owner-provided fetch result is recorded as FETCH_HEAD == a79494cd66be28fd291ed11eddd62d342f457cfd; this does not establish or claim synchronized origin/main."
  recommended_next_agent:
    - "Luna-44, only after this governance authorization is immutably published; then Luna-0 for independent review."
    - "No Luna-45."
---

# Luna-0 authorization — Luna-44 canonical point fixture and relay propagation

## Decision and baseline provenance

**Luna-44 is AUTHORIZED / NOT EXECUTED**, solely for the frozen point-level
fixture construction and three-condition relay-propagation/replay experiment
specified in this handoff. This decision records the explicit project-owner
direction in the current task. It supersedes the earlier “no automatic Luna-44”
disposition only for this bounded scope; it does not revise the historical
Luna-43 verdict.

The authoritative starting revision is
`a79494cd66be28fd291ed11eddd62d342f457cfd`, on
`copilot/establish-new-canonical-baseline`. The owner reports that
`git fetch origin main` returned this revision as `FETCH_HEAD`. There is no
`refs/remotes/origin/main` in this checkout; the repository is shallow.
Therefore this handoff does **not** claim `HEAD == origin/main` or synchronized
main. Record the immutable publication revision of this authorization and the
execution branch/HEAD/status when Luna-44 starts. Luna-44 must not begin from
this uncommitted governance diff.

The repository governance files are under `workflow/`. This publication does
not touch `.github/agents`, implementation code, tests, or historical
Luna-42/Luna-43 records.

## Frozen fixture and experiment boundary

Construct the fixture once from the owner-stipulated existing Luna-39/Luna-34
`make_spiral_dataset` generator using seeds `0, 1, 2, 3, 4` and exactly 64
ordered sequences per seed. Number sequences from zero in generator order.
For each point, freeze seed, zero-based sequence index, deterministic label-free
stream ID `c{seed:02d}-{sequence_index:03d}`, zero-based point index in source
order, zero-based sequence-local batch ordinal, and raw `x`, `y`, and `t`; do not use generator
metadata IDs that may contain labels. Retain the fixture-construction audit
`x+y`, calculated once with production-declared `float(x) + float(y)`, not as a
runtime input. Store every float as decimal text that round-trips to the same
binary64 value and an exact reversible representation, preferably
`float.hex()`.

Define same-time batches exactly as production `_point_batches`: convert each
timestamp to `float`, reject decreasing numeric timestamps, and group
consecutive points when converted timestamps compare numerically equal.
Assign zero-based sequence-local batch ordinals in first-seen order and
preserve within-batch point order; therefore `+0.0` and `-0.0` compare equal
for batching even though their raw bits remain distinct.

Define the canonical SHA-256 over canonical UTF-8 JSON (sorted keys and compact
separators) binding **only** the ordered seed/sequence/deterministic-stream/
point/batch identities and exact binary64 bits for raw `x`, `y`, and `t`.
Explicitly exclude fixture audit `x+y`, neural results, events, and condition
outcomes. Retain per-sequence raw-input digests over the same source fields. If
useful, a distinct audit digest may bind the canonical fixture identity to the
ordered fixture `x+y` audit bits, but it is never the canonical fixture digest.
The fixture-generation
revision and digest must identify this source data. The experiment runner must
load exact raw `x/y/t` from their reversible `float.hex()` forms (checking the
decimal round-trip) and must never call the spiral
generator or regenerate source inputs. For every point in each condition and
replay, it must independently execute production-declared `float(x) +
float(y)`, retain that run's exact derived value, and feed the computed value
into the runtime. It must not feed the fixture's audit `x+y`.

Run the fixed three-node topology `source -> relay -> destination` with only
ordinary Model-B edges `source -> relay` and `relay -> destination`, each with
`delay=1.0`, `w=1.0`, `d=1.0`, and `r=0.0`. Source integration is `None`;
destination integration is disabled in every arm. Vary only relay integration:
disabled, default (`decay_rate_z=0.1`), and calibrated
(`decay_rate_z=0.0125`). Hold all other source, relay, topology, and runtime
settings fixed to the reviewed Luna-42 Phase-B configuration and bounds. Use
fresh state per sequence and condition, then replay each condition from reset
with the same fixture. Keep ACP-0007 disabled.

The scientific endpoint is **relay propagation**. Reconcile each
integration-mediated relay canonical emission to its actual ordinary
`relay -> destination` transfer; require at least one causally matched onward
transfer for the endpoint to be met. Do not require or compare against any
historical count. Destination integration remains disabled; destination
state/emissions are not an endpoint. No tuning, efficacy, task scoring,
promotion, hardware claim, or successor is authorized.

## Comparison policy and acceptance boundary

Raw `x/y/t` values, timestamps, ordering, batching, sequence membership, point
identity, raw-input/fixture digests, event identities/order, route identity,
condition identity, discrete emission classifications/counts, topology,
within-run copied transfer/reception payloads, and same-environment replay
digests are exact. Compare each run's derived `x+y` separately to the fixture
audit value under the point-input policy below; retain its exact binary64
representation in per-run evidence. Do not use tolerance-based raw-input
matching or normalize the historical Luna-43 mismatch. Require actual onward
transfer reconciliation; there is no historical-count target.

For each applicable equation-derived field, independently record
`observed`, `expected`, absolute residual, and the predeclared bound
`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))`:

1. source canonical-emission payload reconstruction;
2. each ordinary Model-B edge's routed-payload reconstruction;
3. each relay recurrence quantity separately: `dt` is the exact binary64
   subtraction of captured timestamps; compare `x`/`z` after elapsed-time
   decay, `x`/`z` after input, discharge amount, and post-discharge `x`/`z`;
4. each `relay -> destination` arrival timestamp derived from relay emission
   timestamp plus the fixed edge delay.

For each point in every arm and replay, independently run the production-declared
`float(x) + float(y)` using exact raw fixture values. Retain the run's exact
derived value in decimal and `float.hex()` form, together with its point/arm/
replay identity, and use that value as the runtime input. Compare it separately
to the fixture's retained `x+y` audit value using
the predeclared
`64 * sys.float_info.epsilon * max(1.0, abs(observed), abs(expected))` policy.
Record observed, expected, residual, and bound per point/run. This point-input
comparison is fixed before fixture construction and is not inferred from the
historical mismatch; raw `x/y/t` identity remains exact.

The same formula does not relax exact event classifications, configured hard
state/resource bounds, exact payload copying within a run, or strict-future
causality. Freeze the formula and quantity list before fixture construction;
do not derive, fit, or expand the allowance from the historical Luna-43
mismatch. Each artifact must carry authorization revision/handoff digest,
fixture-generation revision/fixture digest, runner revision/file hash,
execution revision/execution and artifact digests, configuration digest, and
run/replay identity.
Record the runtime environment and machine float metadata. Any missing
provenance, fixture identity failure, capacity failure, causal inconsistency,
or replay mismatch stops the run as blocked without retries or parameter
changes.

## Ownership, preservation, and return

Luna-44 owns only its new runner, focused tests, new artifact directory and
completed execution handoff. No agent profile is added by this authorization.
Luna-0 owns this authorization and the workflow/changelog updates; Luna-0
independently reviews the returned evidence. Do not change the architecture
contract, ACP-0007/ACP-0008, production API, prior tests, or historical
Luna-42/43 handoffs/artifacts. ACP-0007 remains disabled and unchanged;
ACP-0008 remains opt-in and unpromoted. No WEMA or Luna-45 is authorized.

No scientific outcome is asserted here. The next bounded assignment is Luna-44
after this governance authorization has an immutable publication revision.
