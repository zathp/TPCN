# Luna-65 Phase 2 — E2 Capacity Fixture Contracts

**Status:** Governance draft only. No fixtures have been materialized or run.
Phase 2A and Phase 2B require separate explicit owner authorization.
Full-replication E2 identity capacity remains unproven and Spiral execution
remains blocked.

**Baseline:** `5a374c9ddab30517d863696a28f7f801a31f26bc` on
`governance/luna64-r4.3-freeze-20261010`.

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

**Proposed module and invocation:**

```powershell
.\.venv\Scripts\python.exe -m pytest -q -x tests/test_luna65_capacity_direct.py
```

The module is not present at the baseline. Creating it is permitted only
after owner authorization for Phase 2A implementation and its bounded
verification. No production file change is required or proposed.

**Fixture rules:**

- Construct a fresh `MultiExcursionNeuron` for each counter scenario with
  `E1Config(event_budget=2048, provenance_capacity=16)` and all other E1
  parameters at their existing defaults, except the output-event scenario's
  explicitly listed `decay_rate=0.0001`, `m_emit_delay=0.001`,
  `m_rearm_delay=0.001`, and `delta_x_e=0.001`.
- Use fixed neuron ID `l65-capacity-node`, fixed timestamps, and explicit
  input IDs except in the input-counter scenario. No dataset examples,
  `ExperimentRunner`, task labels, readout updates, or non-neutral reward.
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
   The 2,049th call must reject before creating another input identity.
2. **Episode / ordinary admission:** Call
   `receive_contribution(timestamp=0.0, contribution=1.0,
   event_id="episode-<ordinal>")` 2,048 times, resetting after each
   successful ordinary admission. Verify consecutive episode IDs 1–2,048
   and the associated lineage high-water. On attempt 2,049, ordinary
   admission checks the episode guard first and must raise the episode
   identity error without advancing any identity.
3. **Lineage / new M admission:** Call
   `receive_contribution(timestamp=0.0, contribution=4.0,
   event_id="lineage-<ordinal>")` 2,048 times, resetting after each
   successful new M admission. Verify consecutive lineage IDs 1–2,048 and
   the associated episode high-water. On attempt 2,049, new M admission
   checks the lineage guard first and must raise the lineage identity error
   without advancing any identity.
4. **Output event:** Use `E1Config(event_budget=2048, decay_rate=0.0001,
   m_emit_delay=0.001, m_rearm_delay=0.001, delta_x_e=0.001)`. For each
   character, admit one M excursion using an explicit input ID and
   contribution `8.0`. Process pending internal events until the specified
   number of M emissions has occurred, resetting character-local state
   between characters while retaining identities:
   - Character 1: exactly 1,023 M emissions. This uses 2,047 processed events
     (one external admission and 1,023 M_EMIT plus 1,023 M_REARM events).
   - Character 2: exactly 1,023 M emissions, also 2,047 processed events.
   - Character 3: exactly 2 M emissions, five processed events.

   The slow positive decay, short positive delays, and small discharge
   decrement are frozen to keep the magnitude above `theta_hold` for these
   finite schedules. The exact observed modes, magnitudes, emission count,
   and processed-event count must be checked; if the expected M rearm path
   does not occur, stop and report a fixture failure rather than adjusting
   parameters. These three characters produce output identities 1–2,048
   without exceeding the per-character event budget. On character 4, admit
   one M excursion and process its first pending M_EMIT. That output
   allocation is attempt 2,049 and must raise the output-event identity
   error after only two processed events in the character.

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
| Memory | 268,435,456 bytes |
| Retained test artifacts | 1,048,576 bytes |
| Retries | 0 |

Record baseline and test revision, config, exact per-attempt counter
transitions, allocated IDs, exact rejection types/messages, final serializer
snapshots, test output, resource accounting, and raw SHA-256 identities.
Retain a compact JSONL ledger with one record per allocation attempt and
reject any saved artifact larger than 1 MiB. The artifact limit is a cap on
retained bytes; it is not a claim that the child process cannot emit more
bytes into a buffered pipe before termination.

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
| Memory | 268,435,456 bytes |
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
reference. The 120-second wall, 120-second aggregate job-CPU, 256-MiB memory,
and 1-MiB retained-artifact values above are proposed execution bounds, not
demonstrated controls. A future execution request must include a separate
review of the exact host supervisor showing:

- The test process and all descendants are assigned to the bounded job before
  they can execute; the job is terminated on wall or CPU limit and on
  controller failure.
- CPU accounting/termination is aggregate across the job, not merely a
  per-process timer. Report accounting resolution and termination latency.
- Memory enforcement is explicitly identified as per-process or aggregate
  job memory; it must match the declared 256-MiB limit.
- Retained artifacts are at most 1 MiB. Report bytes retained separately
  from bytes read/emitted before termination, including pipe-buffer
  overshoot. Do not claim a strict emitted-byte ceiling from a retained-file
  cap.
- Monitoring and enforcement are listed separately; observed use below a
  target is not evidence that the target was enforced.

If those controls cannot be demonstrated within separately approved host
restrictions, neither fixture lane may run. No Hyper-V qualification is
presumed necessary. Any change to existing execution restrictions needs
explicit owner approval.

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
capacity-only replacement for the earlier fixture protocol, implementation of
`tests/test_luna65_capacity_direct.py`; its single exact command above; 8,196
target-counter boundary probes with the listed configurations and zero
retries; permission to run only the bounded API/direct-neuron capacity
fixture; and acceptance of the resource monitoring/enforcement terms after
the supervisor is independently qualified. It does not authorize Phase 2B.

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
