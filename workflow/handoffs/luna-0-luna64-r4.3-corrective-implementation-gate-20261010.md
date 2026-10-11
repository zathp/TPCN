# Luna-0 — Luna-64 R4.3 corrective implementation gate

**Gate ID:** `L64-TB-R4.3-CORRECTIVE-20261010`  
**Status:** **BLOCKED — REVISED PACKAGE AWAITS INDEPENDENT PREREVIEW**  
**Owner approval:** Not granted for corrective implementation  
**Scientific workload authorization:** None  
**Original pilot disposition:** **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**  
**Scientific efficacy:** Not assessed

This is a governance-only proposal to correct and unit-verify the delayed
reward lifecycle implicated by the closed pilot. It does not authorize code
changes, a pilot rerun, or any scientific workload. Implementation may begin
only after an independent prereview returns
**PASS — CORRECTIVE GATE READY FOR OWNER AUTHORIZATION** and the repository
owner separately approves this exact gate.

## 1. Frozen evidence and identity reconciliation

Reviewed identities:

- R4.3 content freeze:
  `64a214e310de3b982b90a8ad215598bc1e9f8b1c`.
- R4.3 governance closure:
  `ea1b10456cbf4ca726e473076d239a4f6e53b9c7`.
- R4.3 manifest SHA-256:
  `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`.
- Owner pilot authorization:
  `b401deed8b85728e8c78b93d42922d65fb43f3e4`.
- Pilot implementation/artifacts:
  `d709c5aab0a841a8dfb193bd26b306d9b4198392`.
- Execution handoff:
  `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`.
- Independent pilot closure:
  `515dde66f37ca67c44a39f02e13f2e59b2f10d1d`.
- Original pilot branch:
  `experiment/luna64-track-b-r4.3-pilot-20261010`.

The frozen manifest SHA, ten package raw identities, published blob mappings
and 32-entry inventory identities were independently reconciled to the
freeze Git objects and Stage-B attestation during the original review. The
present worktree is at governance commit
`515dde66f37ca67c44a39f02e13f2e59b2f10d1d`; its remote governance ref and
the original experimental ref resolve to the recorded commits above. These
commits document evidence and authorization boundaries; none grants
corrective implementation or additional workload authority.

The original pilot used exactly two passes, 5,184 episodes and 20,736
receptions; that budget is exhausted. The retained artifact digest is not a
protocol-compliance or efficacy result. Its outcome remains
**NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**.

## 2. Confirmed root cause

The frozen R4.3 protocol at
`experiments/luna64/luna64-track-b-protocol-r4.json` defines:

- physical ticks as the reward, eligibility-age and cleanup clock;
- delays `[0, 1, 8, 9, 15, 16]` TU, represented as
  `[0, 1000000, 8000000, 9000000, 15000000, 16000000]` ticks;
- a deadline at activation + `16000000` ticks, inclusive;
- expiry at activation + `16000001` ticks;
- same-tick order:
  `EXPIRY`, `RECEPTION_AND_COST`, `LOCAL_UPDATE_AND_PREDICTION`,
  `ACTIVATION_AND_CAPTURE`, `REWARD_ORIGIN`, `REWARD_DELIVERY`,
  `CREDIT_SETTLEMENT`, `LOGICAL_COMPLETION`, `PHYSICAL_CLEANUP`;
- zero-delay capture before origin, delivery and settlement; immutable
  eligibility capture; capacity eight with typed invalidation and no
  eviction/truncation; one stable per-episode reward ID with duplicate
  delivery as a no-op; cleanup at activation + expiry after settle, withhold
  or reject; one immediate input-cost charge and zero reward-cost charge.

The retained implementation at `experiments/luna64/run-luna64-r4.3-pilot.mjs`
assigns `dueTick = activationTick + delay` in `runEpisode` but immediately
calls `applyRewardOnce` in that same path. `applyRewardOnce` applies a model
update without checking delivery time. The runner has no due-time dispatch
queue or expiry/deadline transition. Its focused duplicate helper test proves
only that helper's repeated-call behavior; it does not test reward timing.
This directly confirms the independent closure's root cause from source, not
only from the handoff.

## 3. Corrective scope and protected behavior

### Proposed modification allowlist

Only the following may be modified or added on a future, separately
authorized corrective branch:

1. Modify `experiments/luna64/run-luna64-r4.3-pilot.mjs` only in its reward
   scheduler, due-time enforcement, eligibility retention, pending-record
   lifecycle, deadline/expiry, same-time dispatch, episode settlement/
   cleanup, duplicate guard and corresponding instrumentation.
2. Add focused lifecycle tests and deterministic fixture data under
   `experiments/luna64/` (new files only).
3. Add the bounded Windows test supervisor
   `experiments/luna64/run-r4.3-corrective-checks.ps1`; it may launch only the
   three named focused test commands in Section 7 and enforce the proposed
   affinity and aggregate resource limits.
4. Add the execution handoff
   `workflow/handoffs/luna-64-r4.3-corrective-implementation-20261010.md`.
5. Add the test-only review handoff
   `workflow/handoffs/luna-0-independent-review-luna64-r4.3-corrective-implementation-20261010.md`.
6. Add raw focused-test logs, JSONL lifecycle traces and provenance metadata
   only under
   `workflow/evidence/luna64-r4.3-corrective-implementation-20261010/`;
   the aggregate contents must remain within the Section 7 artifact cap.

Do not modify existing frozen R4.3 specifications, schemas, goldens,
validators, manifests, inventories, publication attestation, historical
pilot artifacts, or original pilot handoff. Do not change equations or
nonlinear PCN behavior, arm definitions, model dimensions, benchmark
generator, statistical policy, cost-benefit criteria, or event-cost policy.
Do not edit production/core, ACP, architecture contract, general workflow,
or any Luna-63C file. If correctness requires work beyond this list, stop
and request a separately reviewed scope amendment before editing.

The proposed handling of malformed second reward origins, reused IDs with
changed payloads, and stale inputs is defensive behavior not specified by
R4.3. A second distinct origin is reject-only: it cannot invalidate,
withhold, roll back or otherwise alter the first origin, whether that origin
is pending, delivered, settled or terminal. The first origin proceeds under
the frozen lifecycle. Before any implementation starts, the owner must
explicitly accept or reject these proposals as part of the corrective
authorization. If rejected, pause for a separately reviewed policy
amendment rather than guessing.

Proposed isolated implementation branch:
`experiment/luna64-r4.3-reward-lifecycle-correction-20261010`, based on the
published original pilot handoff tip
`d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`. The historical pilot commit and
artifacts remain reachable unchanged; the branch name is proposed, not
created or authorized by this gate.

## 4. Frozen reward and episode lifecycle

All times below are integer physical ticks. Let activation occur at `A`,
deadline be `D=A+16000000`, and expiry/cleanup tick be `X=A+16000001`.
The configured TU delays are converted exactly to ticks. Decoder timestamps
continue to affect only the frozen PCN elapsed-time transition; they do not
drive reward or cleanup scheduling.

1. **Reward origin creation:** after irrevocable TRAIN prediction and
   immutable eligibility capture at activation, the evaluator creates one
   signed reward origin with stable identity
   `L64-R4.3/<seed>/<arm>/<global-ordinal>/reward` and associated activation
   identity. The scalar payload is only `+1` or `-1`; it carries no target or
   label.
2. **Due-time calculation:** calculate `due=A+assigned_delay_ticks` using
   checked integer arithmetic. Record origin and due timestamps. Never
   equate calculation with delivery.
3. **Pending admission:** at most one origin is valid for a protocol-valid
   active episode because the frozen task has one activation and one reward
   assignment. A repeated message ID while pending is a duplicate only if
   reward payload, activation identity, origin timestamp and due timestamp
   all exactly match the original; it creates no new queue entry. Reuse of
   an ID with differing provenance or payload is `ID_COLLISION_INVALID_INPUT`,
   never a second reward. A second distinct origin ID is outside the frozen
   valid task. The proposed defensive policy is reject-only: preserve the
   first origin's exact current state, reject the second as
   `SECOND_ORIGIN_REJECTED_INVALID_INPUT`, and do not invalidate the episode,
   withhold a pending first origin, or roll back an already settled first
   origin. This policy is not specified by R4.3 and requires explicit owner
   acceptance before implementation; it must not be represented as a frozen
   protocol rule.
4. **Deadline admission:** an origin with `due>D` is rejected as
   `REJECTED_AFTER_DEADLINE`; it is never deliverable or settleable. Keep
   captured credit bounded until the protocol expiry/cleanup phase at `X`.
5. **Logical-time advancement:** advance only to the next scheduled physical
   input, reward due time, deadline/expiry, or cleanup event. Do not run
   neural updates during silence and do not introduce a global neural tick.
   The scheduler may advance host/logical processing time to handle a due
   reward without changing decoder state.
6. **Same-time phase execution:** apply the exact frozen phase list, in order,
   at each physical timestamp. At equal-time receptions, retain canonical
   event-ID then child-ordinal serialization. Expiry at `X` occurs before
   any same-tick reception or reward-delivery attempt. The zero-delay
   prediction/capture at `A` precedes reward origin, delivery and settlement.
7. **Delivery:** a nonduplicate admitted reward is delivered only when
   scheduler time reaches its due timestamp. Reject early delivery. At
   `t>D`, or if its eligibility/episode has expired, reject as expired/late.
   A delivery delayed by processing until `X` is too late: expiry wins the
   same-tick ordering and it cannot settle.
8. **Credit settlement:** settle only after successful delivery and before
   expiry, using the immutable captured eligibility vector, event identities,
   physical ages and readout snapshot taken at activation. Never recalculate
   eligibility from later events or use expired credit. Record at most one
   applied update for each stable reward ID. Duplicate delivery is a no-op;
   record its attempt without charging input energy or applying another
   update. Empty eligibility produces the frozen zero/unattributed result.
9. **Expiry:** at `X`, any unsettled captured eligibility expires and is
   unusable. Pending reward records become terminal
   `WITHHELD_EXPIRED` with `reason_not_settled=REJECTED_EXPIRED`; records
   already rejected for a more specific reason retain `terminal_state=REJECTED`
   and that reason. Settled reward records remain `SETTLED`; only their
   residual eligibility snapshot expires. No update can occur after expiry.
10. **Logical completion and cleanup:** completion of the four input
    receptions is not reward settlement and does not discard pending state.
    Keep the episode isolated until settlement/withhold/rejection and cleanup
    at `X`; only then release episode state/queue/eligibility and start the
    next serial episode. A terminal settled record's duplicate guard remains
    through cleanup; after cleanup the next episode has a new identity scope.
11. **Energy accounting:** charge one immediate activity-cost-proxy unit per
    distinct received input event at `RECEPTION_AND_COST`, independent of
    reward lifecycle. A duplicate input identity must not double-charge.
    Reward origin, queueing, delivery, settlement, expiry and duplicate
    reward delivery each have zero input-energy charge.
12. **EVAL:** retain the frozen no-target/no-reward/no-settlement/no-update
    rule.

### Eligibility boundaries

The frozen **eligibility-selection horizon** is distinct from the longer
**episode retention/cleanup expiry**. At activation `A`, select captured
inputs whose physical age satisfies `0 <= A-event_tick <= 8,000,000` ticks;
age exactly 8 TU is included and age 8 TU plus one tick is excluded. Capture
the selected event IDs, ages, vectors, contribution factors and readout
snapshot immutably. Retain that bounded snapshot only through the reward
terminal outcome or expiry `X`; never add later inputs and never use it
after `X`.

Concrete reference fixture: one eligible record at age 8,000,000 ticks,
`g=+1`, prediction `a=1`, and latent vector `z=[0.25,-0.5,1,0]` yields
`K=exp(-4)` and local-temporal vector
`exp(-4)*[0.25,-0.5,1,0,1]`. At age 8,000,001 the record is excluded; with
no other eligible records the captured vector is `[0,0,0,0,0]`. Expected
values are formula-based, not rounded decimal approximations.

Exactly eight eligible identities are all captured in canonical event
order. A ninth eligible identity produces the frozen typed episode-invalid
result with no eviction or truncation. A due-at-deadline reward at `D` uses
the original capture unchanged; at `X` that snapshot is expired and
unusable.

### Due-time and deadline invariants

For each trace record that says an update was applied:

- `settlement_timestamp >= due_timestamp`;
- delivery occurred at exactly `due_timestamp` (no early delivery);
- `due_timestamp <= deadline_timestamp`;
- `settlement_timestamp <= deadline_timestamp`;
- settlement phase follows delivery phase at that timestamp;
- settlement precedes expiry and cleanup;
- eligibility contains only captured input identities within the inclusive
  frozen 8-TU horizon and remains immutable through settlement;
- the reward ID has no earlier applied settlement.

An equality of settlement and due time is allowed. Delivery/settlement at the
inclusive deadline `D` is allowed because it precedes expiry at `X`. At `X`,
the `EXPIRY` phase precedes `REWARD_DELIVERY`, so no reward first delivered
at `X` can settle. Any settled reward lacking an origin, activation identity,
due time or provenance is invalid evidence and fails the gate.

## 5. Deterministic reference fixture matrix

Reference origin `A=0`, `D=16,000,000`, and `X=16,000,001` ticks. `E@A`
denotes the immutable eligible event identity/vector snapshot captured at
activation. `r` is a unique stable reward ID; all valid fixture rewards
originate after prediction and capture. “Cleanup” always means reset after
the frozen settle/withhold/reject outcome at `X`, not immediately on input
completion.

| Fixture | Origin/due and scheduler checkpoints | Expected pending queue / delivery / settlement / expiry / cleanup |
|---|---|---|
| Delay 0 TU | Origin and due at `0`; activation capture phase precedes reward phases. | Queue transiently admits `r@0`, deliver and settle once at `0` using `E@A`; no pending record afterward; `E@A` retained only for audit until expiry; expire residual state and cleanup at `X`. |
| Delay 1 TU | Due `1,000,000`. | `r` pending on `[0,1,000,000)`; no delivery/update before due; deliver and settle once at `1,000,000`; cleanup at `X`. |
| Delay 8 TU | Due `8,000,000`. | `r` pending until `8,000,000`; one delivery/settlement at due from original `E@A`; cleanup at `X`. |
| Delay 9 TU | Due `9,000,000`. | `r` pending until `9,000,000`; one delivery/settlement at due from original `E@A`; cleanup at `X`. |
| Delay 15 TU | Due `15,000,000`. | `r` pending until `15,000,000`; one delivery/settlement at due from original `E@A`; cleanup at `X`. |
| Delay 16 TU | Due equals inclusive deadline `D=16,000,000`. | `r` pending through times `<D`; deliver and settle exactly at `D`; settlement precedes expiry at `X`; cleanup at `X`. |
| Delay 17 TU | Due `17,000,000>D`. | Reject at admission as `REJECTED_AFTER_DEADLINE`; queue remains empty; no delivery or settlement; `E@A` expires at `X`; cleanup at `X`; later due callback is stale and ignored/rejected. |
| Early delivery attempt | Delay `1 TU`; attempt delivery at `0`, then process the due event at `1,000,000`. | Early attempt is logged `NOT_YET_DUE` with non-null attempt time and null delivery/settlement times; `r` remains the sole pending record and parameters are unchanged. At due, deliver and settle once; cleanup at `X`. |
| Due exactly at expiry | Synthetic origin has due `X=16,000,001`, which is beyond inclusive deadline `D`. | Reject at admission as `REJECTED_AFTER_DEADLINE`; queue remains empty; no delivery or settlement at `X`; expiry then cleanup occur at `X`. This tests the due-time boundary, not an authorized delay value. |
| Valid due delivered at expiry | Origin due is `D`, but an adversarial scheduler fixture delays actual delivery attempt until `X`. | At `X`, expiry runs first; `E@A` expires; delivery attempt is rejected `REJECTED_EXPIRED`; no settlement; cleanup last at `X`. This is a late-delivery stress fixture, not a new protocol delay. |
| Reward after expiry | Due `D`, delivery attempted at `X+1`. | Expiry and cleanup at `X`; queue and credit cleared; late attempt is rejected against closed episode, has no effect, no settlement and no energy charge. |
| Duplicate while pending | Delay `8 TU`; after admitting `r`, submit the same ID again with identical reward value, activation ID, origin timestamp and due timestamp. | Second submission is `DUPLICATE_ALREADY_PENDING`, creates no queue entry and changes no parameters; original remains the sole pending item and settles once at `8,000,000`. |
| Second origin after zero-delay settlement | Settle first origin `r1` at `A` with delay zero; submit distinct origin `r2` before episode cleanup. | Reject `r2` as `SECOND_ORIGIN_REJECTED_INVALID_INPUT`; first update remains applied exactly once; no rollback, invalidation or second settlement. This defensive policy requires owner acceptance. |
| ID collision while pending | Delay `8 TU`; submit same ID with altered reward value or activation/due provenance. | Reject as `ID_COLLISION_INVALID_INPUT`; do not overwrite origin or queue state. Proposed defensive invalid-input outcome requires owner acceptance; no second settlement. |
| Duplicate delivery | Delay `1 TU`; deliver `r` at `1,000,000`, then redeliver the same ID with identical payload/provenance after settlement. | First attempt removes pending record and settles once; duplicate is logged `DUPLICATE_ALREADY_SETTLED`, no second update, no queue entry, no charge; expiry/cleanup at `X`. |
| Logical completion before due | Delay `8 TU`; four input events and prediction complete at `A=0`. | Mark input/logical completion but preserve pending `r` and `E@A`; no next episode; deliver/settle at `8,000,000`; expire/cleanup at `X`. |
| TRAIN reward with empty eligibility | At capture, all event ages exceed the horizon or history is empty; normal TRAIN oracle still creates its assigned signed reward. | Reward follows assigned due time; delivery is logged; zero eligibility causes the frozen zero update and `UNATTRIBUTED_EMPTY_ELIGIBILITY`; no withholding. Expiry/cleanup at `X`. |
| EVAL without reward | EVAL has no target or delay and no reward origin. | Queue remains empty; no delivery, settlement or update; mark `EVAL_NO_REWARD_BY_PROTOCOL`; cleanup at `X`. |
| Multiple pending identities / capacity | Admit `r1`; inject distinct `r2` before cleanup in the same episode. | Valid state never exceeds one origin. Proposed defensive policy: reject `r2` only and preserve `r1`'s exact existing state. If `r1` is pending, it remains queued and settles at its frozen due time; if already delivered/settled, no rollback or second update occurs. This policy requires explicit owner acceptance. Repeating `r1` is duplicate only if payload, activation, origin and due provenance match; changed content under the same ID is `ID_COLLISION_INVALID_INPUT`. |
| Episode cleanup | Settle a delay-0 reward at `A`, then advance to `X`. | Applied-settlement guard for `r` remains through `X`; expiry removes residual credit; cleanup clears pending/eligibility/history/state only after terminal outcome; a following episode starts empty with distinct ID namespace. |
| Same-time reception, reward and expiry | At `X`, inject a fifth physical reception tagged to the already input-complete old episode, a late delivery for its reward ID, expiry and cleanup. This is an invalid stale-input fixture, not a legal new episode or workload. | Expiry first; reception/cost records and charges the distinct physical reception exactly once; then reject it as `STALE_EPISODE_INPUT` without decoder update/history append; reject delivery as expired; no settlement; logical completion; cleanup last. It cannot belong to the next episode, whose admission follows cleanup. This defensive policy requires owner acceptance. |
| Same-time canonical receptions | Two reception IDs at same physical tick and a due reward at that tick. | Process receptions in canonical event-ID then child-ordinal order within the reception phase, charging each distinct identity exactly once; then follow remaining frozen phases. At `A`, activation capture is before zero-delay reward origin/delivery/settlement. |
| Eligibility horizon | At capture `A=16,000,000`, events `e8@8,000,000` and `e8plus1@7,999,999` have ages 8,000,000 and 8,000,001. Use `g=+1`, `a=1`, `z=[0.25,-0.5,1,0]`. | Capture only `[e8]`, age `[8000000]`, vector `exp(-4)*[0.25,-0.5,1,0,1]`; excluded ID is absent. A second variant with only `e8plus1` has empty IDs and zero vector. |
| Eligibility capacity eight/nine | Capture eight distinct in-horizon IDs, then test a ninth before activation capture. | Eight-record fixture captures all eight in canonical order. Nine-record fixture is typed invalid; no eviction, truncation, partial settlement, or shortened provenance. |
| Eligibility immutability and lifetime | Capture `E@A`; deliver at deadline `D`; separate withheld snapshot advances to `X`. | At `D`, settlement uses byte-identical capture digest and original ages. At `X`, expiry precedes other same-tick phases and the snapshot cannot settle. Retention/expiry state is explicit. |

The seven configured-delay cases plus boundary/adversarial fixtures above
are deterministic scheduler/reference fixtures only. They do not invoke the
benchmark generator, compare arms, train/evaluate a model, or consume the
closed scientific pilot budget. Delay 17 TU, due-at-`X`, late delivery,
second-origin and stale-input cases are defensive synthetic inputs, not
additional configured delays or valid-task behavior. R4.3 does not specify
these malformed-input policies; owner acceptance is required before
implementation.

### Independent reference versus implementation tests

Before implementation, an independent reviewer must derive and approve the
expected state transitions in the matrix and an executable pure-reference
fixture oracle from the frozen protocol text. The reference oracle must not
import the production/candidate lifecycle implementation. After a future
owner approval, focused implementation tests compare the implementation's
queue, trace and terminal state to those reference outputs. Test logs must
identify reference-derived assertions separately from implementation
assertions. A passing implementation test is not scientific evidence.

## 6. Machine-readable instrumentation and audit

Emit bounded JSONL records under proposed exact schema
`L64-R4.3-CORRECTIVE-TRACE-1`. Emit one record for each scheduler
phase/event transition, using exactly this field order:

```text
schema, episode_id, arm_id, seed, global_ordinal, record_index,
record_timestamp, phase_ordinal, phase, event_type, reward_origin_id,
activation_id, reward_value, origin_timestamp, due_timestamp,
delivery_attempt_timestamp,
delivery_timestamp, settlement_timestamp, deadline_timestamp,
expiry_timestamp, eligibility_ids, eligibility_snapshot_id,
eligibility_capture_timestamp, eligibility_expiry_timestamp,
pending_queue_depth, reward_delivery_attempt, update_applied,
settlement_count, reason_not_settled, terminal_state, input_event_id,
input_child_ordinal,
input_charge_id, input_charge_timestamp, input_charge_count,
reward_energy_charge, before_parameter_hash, after_parameter_hash
```

`schema`, IDs, enum fields and hashes are strings; `seed`, `global_ordinal`,
`record_index`, queue depth and counts are nonnegative integers; timestamps
and `reward_energy_charge` are integer ticks/units; `update_applied` is
boolean; `reward_delivery_attempt` is boolean and true only on a row whose
`event_type` is `REWARD_DELIVERY_ATTEMPT`; `input_child_ordinal` is a
nonnegative integer for input reception records and `null` otherwise;
`reward_value` is integer `-1`, `+1` or `null`;
`eligibility_ids` is an ordered string array. Nonapplicable optional scalar
fields are explicit JSON `null`, never omitted. Hashes are 64 lowercase
hexadecimal characters or `null` when no parameter state exists.
`record_index` is contiguous from zero per episode and `phase_ordinal` starts
at zero for each physical timestamp and increments in frozen phase order.

`phase` is exactly one frozen phase-order enum value. `event_type` is one of
`REWARD_ORIGIN_CREATED`, `PENDING_ADMITTED`, `PENDING_DUPLICATE`,
`PENDING_REJECTED`, `TIME_ADVANCED`, `REWARD_DELIVERY_ATTEMPT`,
`REWARD_DELIVERED`, `CREDIT_SETTLED`, `CREDIT_WITHHELD`,
`ELIGIBILITY_EXPIRED`, `INPUT_CHARGED`, `INPUT_REJECTED`,
`EPISODE_COMPLETED`, `EPISODE_CLEANED`.
`reason_not_settled` is one of `null`, `NO_REWARD_ORIGIN`,
`EVAL_NO_REWARD_BY_PROTOCOL`, `UNATTRIBUTED_EMPTY_ELIGIBILITY`,
`NOT_YET_DUE`, `REJECTED_AFTER_DEADLINE`, `REJECTED_EXPIRED`,
`DUPLICATE_ALREADY_PENDING`, `DUPLICATE_ALREADY_SETTLED`,
`ID_COLLISION_INVALID_INPUT`, `SECOND_ORIGIN_REJECTED_INVALID_INPUT`,
`STALE_EPISODE_INPUT`, `EPISODE_INVALID`, `CAPACITY_INVALID`.
`terminal_state` is one of `null`, `PENDING`, `SETTLED`,
`WITHHELD_EXPIRED`, `REJECTED`, `EXPIRED`, `CLEANED`. `PENDING` begins at
admission. `SETTLED` records the single terminal credit outcome, including
the frozen empty-eligibility zero update. A pending reward at `X` transitions
to `WITHHELD_EXPIRED` with reason `REJECTED_EXPIRED`; a settled reward
remains `SETTLED` while its residual eligibility snapshot expires; an
already rejected record retains `REJECTED` and its original, more-specific
reason. `EXPIRED` marks an eligibility snapshot only, and `CLEANED` marks
episode cleanup.

The checker validates exact key order, types/enums, contiguous indices,
monotonic scheduler timestamps, frozen same-time phase sequence, queue
transitions, charge identities exactly once, duplicate ID/payload/provenance
consistency, and parameter hashes on no-op attempts. It requires
`reward_delivery_attempt=true` exactly for `REWARD_DELIVERY_ATTEMPT` rows and
false otherwise. For reception rows it checks canonical event-ID order
followed by the recorded integer `input_child_ordinal`, matching the frozen
protocol's `canonical event ID then child ordinal` serialization. Attempt time is
distinct from successful delivery time: failed attempts have a non-null
`delivery_attempt_timestamp` and null `delivery_timestamp` and
`settlement_timestamp`. Traces are bounded by Section 7 and decoder-facing
reward records contain only a signed scalar and opaque identity, never a
target/label.

An independent trace checker must fail closed if:

- a settled reward has missing or inconsistent provenance;
- `settlement_timestamp < due_timestamp`, successful delivery does not occur
  exactly at `due_timestamp`, or
  settlement occurs after deadline/expiry;
- a due time exceeds the inclusive deadline and is nevertheless delivered
  or settled;
- a reward ID settles more than once or a duplicate changes parameters;
- an eligibility identity is not in the activation-time capture or is used
  after expiry;
- a pending queue exceeds one record per episode, drops an identity, evicts,
  truncates or crosses an episode boundary;
- a reception identity is charged zero or more than one time, or reward
  lifecycle charges input energy;
- phase ordering, cleanup state, EVAL boundary or frozen same-time reception
  ordering is violated.

Matching replay digests remain a useful deterministic check but are never a
substitute for trace invariants or deadline checking.

## 7. Distinct corrective-development resource proposal

These ceilings are a new, proposed corrective-development budget and do not
reuse or replenish the exhausted pilot budget:

- **Allowed future implementation paths:** exact allowlist in Section 3,
  only on the separately authorized corrective branch. During this
  governance preparation, only this proposal and the authoritative workflow
  may be changed.
- **Exact focused-test invocations:** invoke exactly once, from the isolated
  corrective worktree:
  `powershell.exe -NoProfile -File experiments/luna64/run-r4.3-corrective-checks.ps1 -Mode All`.
  `All` is the sole accepted mode and serially launches exactly these three
  child commands, once each, in this order:
  `node experiments/luna64/test-track-b-gate-r4.mjs`,
  `node experiments/luna64/test-luna64-r4.3-reward-reference.mjs`, and
  `node experiments/luna64/test-luna64-r4.3-reward-lifecycle.mjs`. The
  supervisor rejects any other mode/command and any second invocation for
  this authorization ID. Before launching children it atomically creates a
  one-shot marker at
  `%LOCALAPPDATA%\\TPCN\\luna64-r43-corrective-implementation-20261010.json`
  using create-new semantics; marker creation is durable and precedes test
  startup. The marker is capped at 4 KiB, records authorization ID, worktree
  revision, start state and terminal outcome, and is protected by a
  current-user-only ACL. `RUNNING` or `CONSUMED` markers both fail closed;
  interruption or uncertain outcome consumes the invocation and cannot be
  reset under this budget. The only recovery is a new owner-approved budget.
  This puts all three child tests under one supervisor lifetime; CPU, wall,
  process-tree working set and artifact totals are accumulated in memory
  across the entire run. The supervisor may not spawn
  `run-luna64-r4.3-pilot.mjs`, the benchmark generator, or any network/GPU
  tool.
- **Maximum synthetic fixture size:** define one scheduler/trace record as
  either one scripted lifecycle stimulus (e.g. origin, advance, delivery
  attempt, expiry, cleanup) or one emitted JSONL phase/event trace row; each
  counts once toward the combined total. Allocate per-case maximums:
  configured delays 0/1/8/9/15/16/17 TU, 16 each; early-delivery attempt
  16; due-at-expiry 24;
  late-at-expiry 20; after-expiry 20; duplicate 24;
  completion-before-due 24; multiple-origin/capacity 32;
  empty-eligibility TRAIN 20; EVAL no-reward 20; cleanup 24;
  same-time expiry/reception/reward 36; same-time canonical reception
  ordering 36; horizon inclusion/exclusion 24; eligibility capacity eight/
  nine 32; immutability through deadline/expiry 32; second origin after
  zero-delay settlement 16. Allocated maximum is 512; combined hard ceiling
  is 512, with no unallocated records and no capacity to add fixtures.
  At most eight eligible identities are captured in a valid episode; a
  ninth is only a rejected negative input.
  At most one active episode per fixture and two reward-origin IDs in the
  capacity-negative fixture.
- **Compute:** one logical CPU; 120 CPU seconds and 180 wall seconds total.
- **Memory:** 512 MiB aggregate peak working set for the supervisor and its
  complete child process tree.
- **Artifacts:** 5 MiB aggregate maximum for test outputs and lifecycle
  traces; retain failures and logs, do not expand the cap.
- **Enforcement:** the one supervisor invocation must launch each child with
  Windows `CREATE_SUSPENDED`, set and verify process affinity mask `0x1`,
  start resource monitoring, and only then resume the child thread. This
  supervisor-held launch gate requires no edits to the frozen
  `test-track-b-gate-r4.mjs`. The supervisor accumulates CPU time and wall
  time over the single invocation, polls aggregate process-tree peak working
  set and artifact bytes, and terminates/fails on any cap breach. The
  one-shot marker makes invocation count enforceable across process restarts;
  the marker is never reset by the supervisor. Missing affinity,
  process-tree accounting, monitoring or atomic marker support is a blocker,
  not permission to assume compliance. The reviewer checks the exact
  child-command allowlist and confirms no pilot runner/generator is imported
  or reachable from test entry points.
- **Prohibited:** any benchmark-generator or scientific workload execution;
  any of the original 5,184 episodes/20,736 receptions being repeated;
  extra seeds, arms, training/evaluation, scoring, omission replay, efficacy,
  cost-benefit, performance tuning, or hardware/GPU/network use.

Stop on any cap breach, unexplained state transition, failed invariant,
path violation, or need to change frozen semantics. This gate does not
authorize any new pilot after the focused correction tests.

## 8. Required focused acceptance checks

Before implementation authorization, the independent prereview must approve
the protocol interpretation and all reference fixture expectations above.
If separately authorized, implementation acceptance requires:

1. Exact due-time queueing and delivery for every configured delay.
2. No settlement before due; inclusive-deadline behavior at 16 TU; rejection
   after deadline; expiry-first rejection at the exact expiry tick.
3. Immutable eligibility capture through its bounded lifetime; no use after
   expiry; no eviction/truncation; typed invalidation on capacity overflow.
4. Correct TRAIN origin/reward identity and signed-only payload; no EVAL
   origin, settlement or update.
5. At-most-once settlement; duplicate delivery is a logged no-op.
6. Correct simultaneous phase and event-ID ordering.
7. Correct completion-versus-cleanup distinction and next-episode reset.
8. One immediate input charge per distinct received event, independent of
   the reward lifecycle; zero reward charge.
9. Independent trace checker enforces all invariants and reconciles every
   settled record to origin, activation, due, delivery, eligibility and
   parameter hashes.
10. Frozen R4.3 package and all original pilot artifacts remain byte-for-byte
    unchanged; diff contains only allowed paths.
11. No scientific workload invocation and no efficacy interpretation.

## 9. Independent prereview record

Reviewer must not be the author of this corrective package and must review
the exact package bytes. Required dimensions:

- root cause independently confirmed from original runner source;
- exact frozen protocol interpretation and phase/deadline semantics;
- fixture completeness and expected queue/delivery/settlement/expiry states;
- trace schema and independent invariant checker sufficiency;
- one-pending-record derivation, capacity behavior and episode isolation;
- corrective path/resource allowlists and prohibitions;
- original pilot outcome/artifact preservation;
- no changes to PCN equations, frozen R4.3 specification or Luna-63C;
- no scientific workload execution in preparation or prereview.

The first prereview of draft SHA-256
`6C62B7F9D40C1336AD86324E9F11899A18F96F500BC3AD08794D4534928E1DE3`
returned **BLOCKED — CORRECTIVE GATE INCOMPLETE**. This revision addresses
those findings by replacing TRAIN withholding with frozen empty-eligibility
and EVAL-no-reward cases; explicitly marking second-origin, reused-ID
collision and stale-input outcomes as defensive policy requiring owner
acceptance; adding concrete horizon, capacity and immutability fixtures;
specifying trace field order/types/enums and distinct attempt/delivery times;
and allocating exact per-fixture record budgets, command invocations and
resource enforcement. The initial verdict does not approve this revision.

The second prereview of SHA-256
`C5248A3572CEF71205DA7508E374AF1926B073CDDE71B539538328BFED652208`
also returned **BLOCKED — CORRECTIVE GATE INCOMPLETE**. This revision made
second-origin handling reject-only without invalidating or rolling back the
first origin, required successful delivery exactly at due time, added an
early-delivery fixture, and consolidated all focused checks under a
one-shot, supervisor-held launch gate with aggregate resource monitoring.

The third prereview of SHA-256
`00F79FB732F8934588E14DE324D9019DE8B1AB946FD60061F891805ECC7BE295`
also returned **BLOCKED — CORRECTIVE GATE INCOMPLETE**. Its remaining
findings were absence of a child-ordinal field for frozen equal-time input
ordering, undefined type/value semantics for `reward_delivery_attempt`, and
an incomplete terminal-state enum for `WITHHELD_EXPIRED`. This draft adds
`input_child_ordinal` with reception-only integer/null typing and checker
ordering, binds the attempt field to a boolean/event-type rule, and defines
the `WITHHELD_EXPIRED` terminal transition and its relation to rejected,
settled, expired-eligibility and cleaned states. The third verdict does not
approve this revision.

**Prereview verdict:** PASS — CORRECTIVE GATE READY FOR OWNER AUTHORIZATION.  
**Reviewer identity:** Independent Luna-0 Architecture Guardian subagent
`50a4a727-a8a8-482a-bf11-4614032cf5c9`.  
**Reviewed package SHA-256:** `86F30AA80A6979EA6FC27CD57879412554299A616C8B36A6B94BACC1B35A8045`.  
**Review evidence:** [independent prereview record](luna-0-independent-review-luna64-r4.3-corrective-gate-20261010.md).
The gate's publication commit will be recorded in the authoritative Luna
workflow after publication.

Allowed prereview verdicts:

- **PASS — CORRECTIVE GATE READY FOR OWNER AUTHORIZATION**
- **BLOCKED — CORRECTIVE GATE INCOMPLETE**

A PASS authorizes no implementation. Only after the review result is
published may the repository owner approve this exact corrective budget and
scope. No owner approval is present in this record.

## 10. Governance disposition and next gate

This gate proposes only a corrective implementation prerequisite. The
original pilot remains closed and **NOT SUPPORTED AS A
PROTOCOL-COMPLIANT PILOT**. No corrected runner has been built, no focused
corrective fixture has been executed, and no scientific workload has been
run for this task.

Current status:

- Corrective implementation: **NOT AUTHORIZED**.
- Scientific rerun: **NOT AUTHORIZED**; the prior budget is exhausted.
- Efficacy, attribution and cost-benefit: **NOT ASSESSED**.
- Architecture promotion, ACP and production integration: **NOT AUTHORIZED**.
- Luna-63C: **UNCHANGED AND ISOLATED**.

After a prereview PASS, the next decision belongs to the repository owner:
approve or reject the exact corrective implementation budget. Any later
scientific workload requires a separate protocol review and explicit
authorization; this gate cannot automatically authorize one.
