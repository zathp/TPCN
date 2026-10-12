# Luna-65 Phase 2 — E2 Capacity Fixture Contracts

**Status:** Governance-only Phase 2A correction proposal. Independent review
found the corrected Phase 2A specification complete; this correction remains
unpublished and does not constitute owner acceptance or execution
authorization. No fixtures have been materialized or run. Phase 2A and
Phase 2B require separate explicit owner authorization and qualified resource
controls. Full-replication E2 identity capacity remains unproven and Spiral
execution remains blocked.

**Protocol baseline:** `5a374c9ddab30517d863696a28f7f801a31f26bc`.
**Correction review baseline:** `dc62469a099f27f2b8d43142dd8aecb407b2e663`
on `governance/luna64-r4.3-freeze-20261010`.

**Authority:** [Luna-65 Spiral resumption contract](LUNA_65_SPIRAL_RESUMPTION.md),
whose SHA-256 at this baseline is
`1F1D4DD96E21EE760D32CDDE4F0415576C9BAE6AF01B82DB2A9C4E1D9FB5C777`.
This supplement specifies only bounded capacity diagnostics. It does not
alter the Spiral scientific protocol or amend the production architecture.

**Contract relationship:** This document proposes a capacity-only replacement
for the earlier fixture-module and network-count terms in the published
contract's “Separately authorized deterministic interface/capacity fixture
protocol.” Specifically, the earlier single
`tests/test_luna65_capacity_fixture.py` invocation and 128-execution /
131,072-event network ceiling would be replaced by separate Phase 2A and
Phase 2B modules and the limits stated below, if and only if the repository
owner explicitly accepts this supplement and publishes the amendment. Until
that acceptance and publication, the existing Luna-65 contract controls.
This proposal does not replace or amend any Spiral scientific condition,
seed, workload, timing, metric, or acceptance criterion. Phase-separated
owner authorization is likewise proposed governance for these two capacity
lanes and is not active execution authority.

## Disposition boundary

The existing E2 identity limit is 2,048 for each of four persistent counters
on each neuron. `E1Config.event_budget` supplies this identity limit. In the
experiment runner, each EXCURSION_V1 neuron's `event_budget` is
`queue_capacity * 16`; the Spiral configuration therefore sets it to 2,048
while the separate runtime event budget is 1,024 per example.

The following facts are distinguished:

| Claim | Status |
|---|---|
| The identity guards reject `current >= event_budget` before allocating. | Source-verified |
| The four counters start at zero and survive `MultiExcursionNeuron.reset()`. | Source-verified |
| Character-local processed-event count and pending computation reset between characters. | Source-verified |
| A passing bounded fixture would show the tested paths and schedule did not exhaust. | Fixture result; not yet available |
| The complete eight-seed Spiral replication fits the identity limits. | Unproven; remains a benchmark blocker |

No average, single-example limit, fixture pass, or total-network event
aggregate substitutes for a per-neuron, per-counter full-replication bound.
Neither phase below authorizes training, scoring, dataset generation,
structural plasticity, Simon Says execution, or scientific conclusions.

## Source-verified allocation map

| Counter | Initialization and reset | Identity-consuming operations | Integrated-path qualification |
|---|---|---|---|
| Input | Starts at 0. Persists across reset. | Fallback `receive_contribution(..., event_id=None)` allocates in the base contribution method. The E2 guard checks capacity before that increment. | Runner-admitted external events have explicit IDs and do not consume this counter. |
| Episode | Starts at 0. Persists across reset. | Ordinary admission; new M admission; M-to-ordinary completion. Each checks before increment. | These pathways can be reached by external contributions. Ordinary admission checks episode before lineage; new M admission checks lineage before episode. |
| Lineage | Starts at 0. Persists across reset. | Ordinary admission and M admission when a new lineage is needed. Preserved-lineage M admission does not allocate a new lineage. | New-lineage M admission checks lineage before episode. No source-level bound proves its replication high-water. |
| Output event | Starts at 0. Persists across reset. | Every ordinary emission and M emission checks before increment. | Runner event budget bounds per-character processed events, but resets allow output identities to accumulate across characters. |

`generation_token`, processed-event count, emissions held as character-local
state, and pending internal computation are reset at character boundaries;
the four identity high-water counters are not. Structural-plasticity state is
not involved in either phase.

## Phase 2A — direct-counter boundary fixture

**Purpose:** Verify all four identity guards at their exact 2,048 boundary
using deterministic direct-neuron calls. This is a failure-detection fixture,
not evidence of complete-replication sufficiency.

**Scope:** Phase 2A direct-neuron capacity fixture only. It does not invoke
`ExperimentRunner`, the Spiral dataset or benchmark, training, evaluation,
scoring, or Phase 2B network fixtures. No production change is required or
authorized.

**Test module:** `tests/test_luna65_capacity_direct.py`.

**Exact invocation:**

```powershell
.\.venv\Scripts\python.exe -m pytest -q -x tests/test_luna65_capacity_direct.py
```

The working directory is the Git top-level directory of the reviewed checkout
(the expected current path is
`C:\Users\Patrick\Documents\ActiveCode\TPCN`; a different path requires
authorization text to be updated). The applicable environment is Windows
PowerShell with the repository's `.venv` interpreter, `PYTHONHASHSEED=0`, no
network access, and only the two specified environment overrides:
`PYTHONHASHSEED` and the external evidence-directory setting defined below.
Record OS build, Python and pytest versions, executable path, relevant
package versions, environment overrides, and exact checkout revision in the
invocation manifest. This command runs this test module only; retries are
zero.

**Fixture rules:**

- Construct a fresh `MultiExcursionNeuron` for each counter scenario with
  `E1Config(event_budget=2048, provenance_capacity=16)` and all other E1
  parameters at their existing defaults, except the output-event scenario's
  explicitly listed `decay_rate=0.0001`, `m_emit_delay=0.001`,
  `m_rearm_delay=0.001`, and `delta_x_e=0.001`.
- Use fixed neuron ID `l65-capacity-node`, initial timestamp `0.0`, fixed
  timestamps, and explicit input IDs except in the input-counter scenario.
  All four fresh instances start in mode `N`, with `x=0.0` and all four
  identity counters zero. No dataset examples, task labels, readout updates,
  reward, or runner calls.
- For each counter, permit exactly 2,049 target-counter boundary probes: attempts
  1–2,048 must allocate the consecutive identities; attempt 2,049 must raise
  `E1EventBudgetExceeded` with the matching counter name. Do not retry a
  failed allocation. The expected 2,049th rejection is asserted, after which
  the next independent counter scenario may run.
- After each successful allocation, retain its identity for uniqueness
  checks, capture all four high-water values, then call `reset()` where the
  scenario specifies. After the rejected allocation, verify no identity
  counter changed, the target remains exactly 2,048, and the other three
  counters match their pre-attempt values.

**Exact paths:**

1. **Input:** Call `receive_contribution(timestamp=0.0, contribution=0.0)`
   without `event_id` 2,048 times, resetting after each successful call.
   Verify fallback provenance IDs are the consecutive
   `l65-capacity-node:input:<ordinal>` identities from 0 through 2,047.
   After each successful call and before reset, expect mode `N`, `x=0.0`,
   local time `0.0`, processed-event count 1, and that generated ID as the
   sole provenance entry. The final identity snapshot is input `2048`,
   episode `0`, lineage `0`, output-event `0`.
   The 2,049th call must reject before creating another input identity.
   The failed call raises
   `E1EventBudgetExceeded("E2 input identity budget exhausted")` before
   processing the input; its post-error state is mode `N`, phase null,
   `x=0.0`, local time `0.0`, no pending event, processed-event count 0.
2. **Episode / ordinary admission:** Call
   `receive_contribution(timestamp=0.0, contribution=1.0,
   event_id="l65-phase2a-episode-<ordinal:04d>")` 2,048 times, with
   ordinal `0001` through `2048`, resetting after each successful ordinary
   admission. Each success allocates exactly one episode and one lineage
   identity: both high-water values reach `2048`; input and output-event
   remain zero. Before each reset, the successful call has mode `S_PENDING`,
   `x=1.0`, local time `0.0`, processed-event count 1, allocated ordinary
   episode and lineage IDs equal to that attempt's ordinal, and pending
   `S_EMIT@0.5`. On attempt 2,049, ordinary admission checks the episode
   guard first and raises
   `E1EventBudgetExceeded("E2 episode identity budget exhausted")`;
   no identity counter advances on that failed admission. The external event
   has already consumed one character-local event, so the expected post-error
   state is mode `N`, phase null, `x=1.0`, local time `0.0`, no pending
   event, processed-event count 1; identity counters remain input `0`,
   episode `2048`, lineage `2048`, output-event `0`. Retain provenance
   entry `l65-phase2a-episode-2049` unassigned to any episode or lineage for
   this failed attempt and do not call reset on this neuron.
3. **Lineage / new M admission:** Call
   `receive_contribution(timestamp=0.0, contribution=4.0,
   event_id="l65-phase2a-lineage-<ordinal:04d>")` 2,048 times, with
   ordinal `0001` through `2048`, resetting after each successful new M
   admission. Each success allocates one new lineage and one episode:
   both high-water values reach `2048`; input and output-event remain zero.
   Before each reset, the successful call has mode `M_ACTIVE`, phase
   `ARMED`, `x=4.0`, local time `0.0`, processed-event count 1, and pending
   `M_EMIT@1.0`; multi-episode and lineage IDs both equal that attempt's
   ordinal.
   On attempt 2,049, new M admission checks lineage before episode and
   raises `E1EventBudgetExceeded("E2 lineage identity budget exhausted")`;
   no identity counter advances on that failed admission. The external event
   has already consumed one character-local event, so the expected post-error
   state is mode `N`, phase null, `x=4.0`, local time `0.0`, no pending
   event, processed-event count 1; identity counters remain input `0`,
   episode `2048`, lineage `2048`, output-event `0`. Retain provenance
   entry `l65-phase2a-lineage-2049` unassigned to any episode or lineage for
   this failed attempt and do not call reset on this neuron.
4. **Output event:** Use exactly
   `E1Config(event_budget=2048, provenance_capacity=16, decay_rate=0.0001,
   m_emit_delay=0.001, m_rearm_delay=0.001, delta_x_e=0.001)` with all
   remaining defaults. For characters 1 through 4, call
   `receive_contribution(timestamp=0.0, contribution=8.0,
   event_id="l65-phase2a-output-<character:02d>")`, in ascending character
   order. Each call processes one external INPUT event, admits one new M
   lineage/episode, and schedules the first `M_EMIT` at `0.001`. Immediately
   after admission, the expected state is `M_ACTIVE`, phase `ARMED`,
   `x=8.0`, clock `0.0`, and pending `M_EMIT@0.001`. Process
   exactly the following pending internal events in order using
   `process_pending()` with no `through` argument:
   first `M_EMIT` at `tE_1=0.0+0.001`, `M_REARM` at `tR_1=tE_1+0.001`,
   next `M_EMIT` at `tE_2=tR_1+0.001`, then alternating `M_REARM` and
   `M_EMIT` by adding the configured delay to the preceding event timestamp.
   There are no other input events. Timestamps are calculated by those
   sequential binary64 additions, not by multiplying an integer by `0.001`.
   Each target probe is exactly one
   `process_pending()` call that consumes an `M_EMIT`. Record its immediate
   post-call state; then consume its following `M_REARM` with one
   `process_pending()` call before starting the next target probe. M_REARM is
   preparation for the next M_EMIT, not a target-counter probe. Record the
   post-rearm state separately in `post_rearm_checkpoint`. After the final
   required M_EMIT for a character, consume its following M_REARM and store
   the final state there before reset.

   For the exact magnitude oracle, let `d=0.0001`,
   `h_emit=h_rearm=0.001`, `delta=0.001`, and `theta_hold=1.5`.
   Define event timestamps and binary64 magnitudes in source operation order:
   `tE_1=0.0+h_emit`;
   `tR_n=tE_n+h_rearm`;
   `tE_(n+1)=tR_n+h_emit`;
   `a_1=8.0*exp(-d*(tE_1-0.0))`;
   `b_n=max(theta_hold,a_n-delta)`;
   `c_n=b_n*exp(-d*(tR_n-tE_n))`;
   `a_(n+1)=c_n*exp(-d*(tE_(n+1)-tR_n))`.
   Here `a_n` is `abs(x)` immediately before the nth M_EMIT, `b_n`
   immediately after that M_EMIT, and `c_n` immediately after its following
   M_REARM. For every `n=1..2048`, the expected mode after M_REARM is
   `M_ACTIVE`, phase `ARMED`; clock is `tR_n`; the pending event is
   `M_EMIT@tE_(n+1)`; and `abs(x)=c_n`. Immediately after the nth successful
   M_EMIT, expected state is `M_ACTIVE`, phase `REFRACTORY`, clock `tE_n`,
   pending `M_REARM@tR_n`, and `x=b_n` (positive). Its emission ID is
   `l65-capacity-node:excursion:<global-output-ordinal>` where the ordinal
   is unpadded decimal 1 through 2,048; `sequence` equals that ordinal,
   `source` is `l65-capacity-node`, payload is `+1.0`, and lineage/episode
   IDs are the current character's one-based admission IDs. The recurrence
   stays strictly above `theta_hold` through n=2,048: before the last
   M_EMIT, elapsed logical time is less than 4.096 seconds and at most
   2.048 total discharge has occurred, so
   `a_2048 > 8*exp(-0.0001*4.096)-2.048 > 5.94`; thus
   `b_2048 > 5.939 > theta_hold`. No `max` clamp or M-to-ordinary
   transition occurs in the frozen schedule. Record binary64 values as
   JSON numbers without rounding. This is an operation-order oracle for one
   specified environment; it does not claim cross-platform bitwise replay.

   Process and checkpoint:
   - Character 1: 1,023 emissions, output IDs 1–1,023, then 1,023
     M_REARM events; processed-event count 2,047. Final magnitude
     `c_1023`, clock `tR_1023`, pending `M_EMIT@tE_1024`, and counters
     input 0, episode 1, lineage 1, output-event 1,023.
   - Character 2: 1,023 emissions, output IDs 1,024–2,046, then 1,023
     M_REARM events; processed-event count 2,047. Final magnitude
     `c_1023`, clock `tR_1023`, pending `M_EMIT@tE_1024`, and counters
     input 0, episode 2, lineage 2, output-event 2,046.
   - Character 3: 2 emissions, output IDs 2,047–2,048, then 2 M_REARM
     events; processed-event count 5. Final magnitude `c_2`, clock
     `tR_2`, pending `M_EMIT@tE_3`, and counters input 0, episode 3,
     lineage 3, output-event 2,048.
   - Character 4: the external admission makes the counters input 0,
     episode 4, lineage 4, output-event 2,048, with mode `M_ACTIVE`,
     phase `ARMED`, `x=8.0`, and pending `M_EMIT@0.001`. Processing that
     event advances the clock to `0.001` and magnitude to `a_1`, then raises
     `E1EventBudgetExceeded("E2 output-event identity budget exhausted")`
     before incrementing output-event identity or discharging `x`.
     After the exception the exact expected state is mode `M_ACTIVE`,
     phase `ARMED`, `x=a_1`, no pending event, processed-event count 2,
     and counters input 0, episode 4, lineage 4, output-event 2,048.

   Per-character `reset(timestamp=0.0)` occurs after characters 1–3 only,
   preserving all four identity counters. It is not called after the
   expected character-4 exhaustion. All per-character processed-event counts
   remain below 2,048.

The 8,196 figure is the total number of target-counter boundary probes
(four counters × 2,049 attempts each), not the count of all guard checks or
all identity increments caused by those public calls. Successful ordinary
admissions also allocate lineage identities, and successful new-M admissions
also allocate episode identities. Record every counter's before/after state
for every probe, including these coupled allocations.

Unexpected exceptions, a wrong counter name, a nonconsecutive identity, a
counter change on rejection, or an event-budget failure in place of the
predeclared output-identity rejection fails the lane and stops the process.
No retry or boundary adjustment is permitted.

The output-event scenario exercises the M-emission guard. The source also
guards ordinary emissions; its guard is the same output-event counter and
must be reviewed in source. If reviewers require a runtime assertion for the
ordinary-emission guard as a separate allocation site, add its exact
predeclared calls to a reviewed budget before owner authorization; do not
quietly exceed the 8,196-attempt allowance.

**Phase 2A budget and evidence:**

| Bound | Proposed maximum |
|---|---:|
| Target-counter boundary probes | 8,196 total: 2,049 per counter |
| Wall time | 120 seconds |
| Job CPU time | 120 seconds |
| Aggregate concurrent private commit charge | 268,435,456 bytes |
| Retained artifacts, all files combined | 1,048,576 bytes |
| Retries | 0 |

### Phase 2A JSONL result schema

The sole result is gzip-compressed JSON Lines at `results.jsonl.gz`. Its
decompressed payload is UTF-8 JSON, one object per LF-terminated line, with
exactly 8,196 records when the lane completes. Generate each canonical JSON
line using the serialization below, then compress with RFC 1952 gzip,
compression level 9, `mtime=0`, and no embedded filename. Record the Python
and zlib versions in the manifest. This is a single execution artifact, not
a cross-run byte-identity or replay claim. Each decompressed record has:

| Field | Type and meaning |
|---|---|
| `schema_version` | String `luna65-phase2a-probe-v1`. |
| `fixture_version` | String `l65-phase2a-v1`. |
| `counter_under_test` | One of `input`, `episode`, `lineage`, `output_event`. |
| `probe_index` | Integer 1–2,049 within that counter scenario. |
| `initial_state_id` | Stable ID `l65-phase2a-<counter>-fresh-zero-v1`; identifies the fresh neuron/config/reset history for that scenario. |
| `neuron_id` | String `l65-capacity-node`. |
| `counter_snapshot_before` | Object with integer fields `episode`, `input`, `lineage`, `output_event`, sampled immediately before the target attempt. |
| `counter_snapshot_after` | Same object sampled immediately after the attempt, including after the expected exception. |
| `target_counter_delta` | Integer change only for the target counter in this target attempt; expected 1 for allocation, 0 for capacity rejection. |
| `coupled_counter_deltas` | Object listing all non-target counter deltas caused during the same public-call probe; zero-valued fields are included. |
| `preparation_counter_deltas` | For output-event probes only, deltas from the character's external admission since the preceding character reset; zero-valued fields otherwise. |
| `allocated_identity` | Allocated identity string or integer, or JSON null on exception. For input/output use the emitted/provenance ID; for episode/lineage use the newly allocated counter value. |
| `exception` | JSON null, or object `{type, message}` with exact class name `tpcn.excursion_neuron.E1EventBudgetExceeded` and exact message. |
| `expected_outcome` | `allocated` for probes 1–2,048; `capacity_rejected` for probe 2,049. |
| `observed_outcome` | `allocated`, `capacity_rejected`, or `unexpected_exception`. |
| `completion_status` | `expected` only when the observed outcome and all frozen assertions match; otherwise `failed`. |
| `state_checkpoint` | Object containing the scenario-required mode, phase, local timestamp, `x`, pending-event kind/time, and processed-event count; null only for counters where not applicable. |
| `post_rearm_checkpoint` | For successful output-event probes, the same checkpoint fields after its following M_REARM; null for other counters and the expected fourth-character exhaustion. |

Each probe index denotes one public-call attempt directed at the named
target guard, not each incidental guard evaluation or each secondary
identity increment. `target_counter_delta` and `coupled_counter_deltas`
describe changes during that call only; `preparation_counter_deltas`
separately accounts for output-character admission before the M_EMIT probe.
The 8,196 ceiling counts those target probes only and does not constrain
secondary identity increments beyond their own configured 2,048 guards.
The four counter keys are serialized in lexical order. Records use canonical
JSON: UTF-8, `json.dumps(sort_keys=True, separators=(",", ":"),
ensure_ascii=True, allow_nan=False)`, followed by exactly one LF. Numbers
are JSON integers or finite binary64 values; no rounding is permitted.
JSONL records are ordered in execution order: `neuron_id`, counter scenario
`input`, `episode`, `lineage`, `output_event`, then ascending `probe_index`.
Within every snapshot, counter keys are ordered lexically as
`episode`, `input`, `lineage`, `output_event`.

Counter snapshots are obtained by calling the existing public
`neuron_to_ir2_e2(neuron)` serializer and mapping its
`next_episode_identity`, `next_input_identity`, `next_lineage_identity`, and
`next_event_identity` fields to the four schema keys. State checkpoints use
the corresponding serialized mode, phase, timestamp, `x`, pending internal
event, and processed-event count. The test may additionally read the public
provenance and emissions collections to record returned/generated identity
strings; it must not use new production APIs or mutate private counters.
For output-event probes, `state_checkpoint` is immediately after that
probe's M_EMIT. `post_rearm_checkpoint` captures the subsequent M_REARM,
including the final character checkpoint before reset. For character 4's
expected exhaustion, `state_checkpoint` is the post-exception state and
`post_rearm_checkpoint` is null.

### Evidence destination and retained artifacts

Set `TPCN_LUNA65_EVIDENCE_DIR` before the exact command to
`%LOCALAPPDATA%\TPCN\evidence\luna65\phase2a\<run-id>\`, outside the
repository. `<run-id>` is a preassigned UTC timestamp in
`YYYYMMDDTHHMMSSZ` form, a hyphen, and the implementation checkout's
seven-character Git commit ID; never reuse a directory. The run directory
contains:

- `results.jsonl.gz` — gzip-compressed probe records above.
- `manifest.json` — invocation, environment, checkout, test/config identity,
  resource terms, and declared expected-record count.
- `stdout.txt` and `stderr.txt` — complete bounded invocation streams.
- `failure.json` — required on any incomplete or failed lane, with first
  failure category, probe identity if available, and stopped/unrun ranges.
- `sha256.json` — SHA-256 for every retained file except itself, with byte
  length and path; canonical JSON serialization as above.

Retain the directory read-only until the repository owner confirms transfer
to the designated project evidence archive; do not commit result artifacts
to Git. The 1,048,576-byte cap applies to retained on-disk bytes after gzip
compression, across all listed files and metadata combined; report both
uncompressed JSONL length and compressed artifact size. One external
supervisor owns this combined retained limit. Reserve space for `failure.json`,
`manifest.json`, and `sha256.json` before starting and account for each
write before retaining it. If the next write would exceed the cap, stop the
lane before the next probe, preserve only complete records, write the bounded
failure record if reserved space permits, and mark the run incomplete; never
truncate and report a complete ledger. A partial compressed stream must be
closed and labelled incomplete if possible; otherwise retain it only as an
explicitly invalid partial artifact and record its hash/length. Keep
stdout/stderr retained-byte
accounting separate from bytes read/emitted, including pipe-buffer
overshoot. The retained-file cap is not a strict emitted-byte cap. A hash
manifest is finalized only for files fully written and closed; report any
missing failure/hash record explicitly.

This evidence plan is a specification only. It creates no directory or
artifacts under this governance task.

The direct lane's finite deterministic schedule and single-run record provide
a replay reference but do not, by themselves, compare two independent
executions. Do not claim verified replay equivalence unless a separately
reviewed replay allowance is added without violating the 8,196-attempt limit.

**Interpretation:** A pass verifies the four tested counter boundaries and
preservation across the specified character resets. It does not prove that
all distinct episode allocation sites or both emission types are equivalent
under every state, nor that a full Spiral replication is within capacity.
Source review remains required for every allocation site.

## Phase 2B — fixed-network capacity characterization

**Purpose:** Observe persistent identity high-water values under a small,
high-activation, label-neutral workload on the current fixed eight-node
EXCURSION_V1 runner path. This is not a representative Spiral workload or a
capacity proof.

**Configuration for each seed `s` in `65001..65008`:**

```text
neuron_model             = EXCURSION_V1
learning_enabled         = false
reward_mode              = neutral
reward_delay             = 0
activation_mode          = event_only
structural_plasticity    = false
structural_observation   = false
topology_node_count      = 8
topology_initial_edges   = 8
topology_edge_capacity   = 8
topology_fan_in          = 2
topology_fan_out         = 2
queue_capacity           = 128
event_budget             = 1024 per example
prediction_capacity      = 16
max_points               = 16
prediction_expiry        = 64
settling_horizon         = 65
runner seed              = s
E2 identity capacity     = 2048 per node and counter
```

Use the existing seeded topology construction. Before the first example,
record the exact eight-node edge list, edge parameters, and a canonical
topology SHA-256 in the external fixture manifest. Reuse one runner, network,
topology, and persistent E2 counters for that seed's entire schedule; create
a separate runner for each seed. `execute_example(..., index=0,
update=False)` assigns all fixtures to `neuron-0`; this is a deliberate
source-concentrated stress input, not the Spiral benchmark's workload-row
assignment. Set every fixture's required `SyntheticExample.label` to the
same fixed token `capacity-neutral`. This evaluator-side metadata may appear
in the returned readout diagnostic, but `learning_enabled=false`,
`update=False`, and `reward_mode=neutral` ensure it causes neither a
prototype update nor a label-dependent reward; it must not appear in neural
event inputs or routing.

For each seed, define the 16 unique fixture IDs
`l65-cap-v1-s<seed>-c00` through `c15`. Each fixture has exactly 16 points
with timestamps `0.0` through `15.0`, `x=4.0`, and `y=0.0`. No random
generator is used. Serialize each input record with exactly these fields:
`example_id`, `label`, and `points`; each point has exactly `timestamp`, `x`,
and `y`. Serialize the topology record with exactly `nodes` (sorted string
array), `fan_in_limit`, `fan_out_limit`, `edge_capacity`, `routing_capacity`,
and `edges`. Serialize each edge as exactly `source`, `destination`,
`propagation_delay`, `routing_cost`, `edge_weight`, `divider_strength`,
`reference`, and `legacy_identity`, ordered lexically by
`(source,destination)`. For input and topology records, compute SHA-256 over
UTF-8 output of Python's `json.dumps(value, sort_keys=True,
separators=(",", ":"), ensure_ascii=True, allow_nan=False)`; do not
pre-round floats or convert numeric values to strings. The versioned fixture
specification, expanded input digests, and topology digests must be recorded
in the external fixture manifest before a future execution authorization.
Computing these provenance values does not require or authorize changes to
`ExampleExecutionResult` or the runner API.

Execute c00 through c15 in order. After the 16th unique fixture, execute c00
once more on the same runner, with the same points, example ID, index, label,
and configuration as a predeclared replay sentinel. This is a deterministic
replay control, not a retry: it is always executed once if the preceding
schedule completed and is never used to replace an incomplete fixture.
Require the `replay_digest` to match c00 exactly. Also require exact equality
for every `ExampleExecutionResult` field except `identity_snapshots`; compare
all fields exactly, including event trace, feature, prediction, reward,
completion/budget fields, processed-event count, `pending_event_count`, and
`peak_queue_occupancy`. Do not use numeric tolerances: any replay mismatch
invalidates the lane. Identity snapshots are excluded from equality because
high-water values are expected to increase; instead, compare each node's four
counters after every execution with its previous snapshot, require each
counter to be nondecreasing, and require every next-identity value to remain
strictly below 2,048. If any next-identity value reaches 2,048, stop before
admitting another example and report identity capacity as exhausted even if
no allocation attempt has yet raised the typed exception. This is the runtime
evidence that identity counters were retained across calls on the same
runner.

At the first non-completed result, typed capacity outcome, identity
next-counter reaching 2,048, incomplete settling, unexpected exception, or
replay mismatch, stop the entire Phase 2B lane immediately. Do not start
another fixture or seed. Record all unrun fixtures explicitly. A predeclared
failure is an observed technical failure, not a passing negative case and not
a scientific result.

**Phase 2B arithmetic:** 16 unique characters × 8 seeds = 128 unique
executions; one c00 replay sentinel × 8 seeds = 8 additional executions;
136 maximum `execute_example` calls total. At no more than 16 external
inputs and 1,024 processed events per execution, the maxima are 2,176
external inputs and 139,264 processed events. At most 17 character resets
occur per seed. This sentinel raises the earlier 128-execution capacity
proposal by eight calls; it does not alter the Spiral experiment's examples,
seeds, timing conditions, or acceptance criteria. It is a proposed
diagnostic-budget amendment and requires explicit owner acceptance before
Phase 2B can be authorized.

**Phase 2B budget and evidence:**

| Bound | Proposed maximum |
|---|---:|
| Seeds | 8, exactly 65001–65008 |
| Unique fixtures | 128 total |
| Replay sentinels | 8 total |
| Total example executions | 136 |
| Processed events | 139,264 |
| External inputs | 2,176 |
| Wall time | 120 seconds |
| Job CPU time | 120 seconds |
| Aggregate concurrent private commit charge | 268,435,456 bytes |
| Retained test artifacts | 1,048,576 bytes |
| Retries | 0 |

Record exact configuration and revision, all eight edge lists and hashes,
fixture input digest, every per-example result, all-node identity snapshots,
processed-event and queue high-water values, replay comparison, termination
reason, resource measurements, and raw SHA-256 identities. Store only
summary records, traces/digests required for replay, and identity snapshots;
do not retain full expanded internal event traces unless separately
authorized and shown to fit the artifact cap.

**Interpretation:** A pass means only that these 136 synthetic executions
completed, their c00 replay sentinels agreed on the defined observables, and
the captured counters stayed within their ceilings. It cannot establish
capacity sufficiency for 4,160 benchmark examples per seed, any held-out
condition, or the complete 33,280-example replication. Full-replication
capacity remains unproven unless a separate reviewed analytical bound covers
every per-neuron input, episode, lineage, and output-event allocation.

## Resource enforcement and authorization

The Phase 1 closure observed 400 ms wall time, 29,847,552 bytes process
memory, 101 retained output bytes, and a CPU measurement rounded to 0 ms.
Its output-limit probe captured 1,114,112 pipe bytes before termination while
retaining no more than 1 MiB. CPU and memory limits were configured but not
stress-tested. These facts do not qualify its supervisor for either phase.

The per-character event and queue ceilings are enforced by the software
reference. The 120-second wall, 120-second aggregate job-CPU, 256-MiB
aggregate concurrent private commit charge, and 1-MiB combined
retained-artifact values above are proposed execution bounds, not
demonstrated controls. The memory metric is the maximum over time of the sum
of private commit charge for all concurrently live processes assigned to the
execution job; it is not a per-process limit, working-set sum, or sum of
each process's independent peak. A future execution request must identify
the supervisor by exact
executable path, version, and SHA-256, and include independent evidence for:

- The test process and all descendants are assigned to the bounded job before
  they can execute; the job is terminated on wall or CPU limit and on
  controller failure.
- Aggregate job CPU is capped at 120 seconds. Report CPU accounting
  resolution and limit-termination latency.
- The defined aggregate concurrent private commit charge is capped at 268,435,456
  bytes. Demonstrate the exact measured quantity, enforcement boundary,
  accounting resolution, and termination behavior.
- Wall time is capped at 120 seconds; demonstrate the timer's start boundary,
  termination behavior, and latency.
- Controller failure terminates the complete job, with no surviving child.
- Report process-tree inclusion, all limit-accounting resolutions, and
  termination latency.
- Retained artifacts are at most 1 MiB. Report bytes retained separately
  from bytes read/emitted before termination, including pipe-buffer
  overshoot. Do not claim a strict emitted-byte ceiling from a retained-file
  cap.
- Demonstrate evidence integrity: completed files are closed before hashing,
  manifest entries match byte lengths and SHA-256 digests, and partial runs
  are explicitly marked incomplete without success-shaped manifests.
- Monitoring and enforcement are listed separately; observed use below a
  target is not evidence that the target was enforced.

No exact Phase 2 supervisor identity or qualification evidence is currently
recorded. The Phase 1 supervisor does not satisfy this gate, and Luna-64
qualification evidence may not be borrowed or reinterpreted. If the listed
controls cannot be demonstrated within separately approved host restrictions,
neither fixture lane may run. No Hyper-V qualification is presumed necessary.
Any change to existing execution restrictions needs explicit owner approval.

## Review, phase gates, and exact authorization

The planned independent review dimensions are:

1. Counter initialization, all allocation sites, reset persistence, boundary
   ordering, and output-event event-budget interaction.
2. Direct fixture reachability, exact attempt arithmetic, failure
   classification, and what the fixture does not prove.
3. Network schedule, topology identity, replay sentinel, all-node snapshots,
   state continuity, and exact workload arithmetic.
4. Resource accounting, termination controls, artifact-vs-emitted bytes,
   provenance, and separation from frozen Luna-63C/Luna-64 evidence.

Each review must assess the exact draft bytes and return findings or an
explicit PASS/BLOCKED verdict. No reviewer can authorize execution.

**Phase 2A owner authorization must explicitly name:** acceptance of this
capacity-only replacement for the earlier fixture protocol; the reviewed
contract and checkout revision; implementation of
`tests/test_luna65_capacity_direct.py`; the exact command and working
directory above; all four zero-state counter scenarios and output-event
recurrence; the 8,196 target-counter probe maximum and zero retries; the
external evidence directory and combined retained-artifact limit; and
permission to run the **Phase 2A direct-neuron capacity fixture only** after
the exact supervisor has passed its independent qualification gate. It must
explicitly prohibit Phase 2B, Spiral dataset generation, benchmark
evaluation, training, scoring, and any production-code changes. It does not
authorize Phase 2B.

**Phase 2B owner authorization must explicitly name:** acceptance of this
capacity-only replacement for the earlier fixture protocol and of the
increase from 128 to 136 total calls / 131,072 to 139,264 processed events;
implementation of
`tests/test_luna65_capacity_network.py`; the eight listed seeds, 16 unique
fixtures per seed and one c00 replay sentinel; the 136-call, 139,264-event,
2,176-input ceilings; zero retries; and the independently qualified
supervisor/resource terms. It does not authorize benchmark generation,
training, scoring, or full Spiral execution.

Passing Phase 2A does not authorize Phase 2B. Passing either phase does not
authorize the other, establish full-replication capacity, or authorize the
Spiral benchmark. A later Spiral run requires a separately reviewed
full-replication capacity argument or other owner-approved resolution,
qualified execution controls, and its own exact execution authorization.
