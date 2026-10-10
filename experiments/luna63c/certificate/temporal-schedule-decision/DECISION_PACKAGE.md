# Luna-63C Stage-A schedule reconciliation

**Disposition: CORRECTED EVIDENCE — T REMAINS BLOCKED AT N3.** The published
T commit already contains the complete event-identity crosswalk. The prior
decision draft incorrectly treated a different, untracked parent-checkout
copy as the published T schedule. This package corrects that claim and
records the remaining numeric schedule blockers. It does not rerun a lane,
change the fixture, or authorize Lane T, Lane S/N5, N6, or Stage B.

## Verified source revisions

The source checkout is `experiment/luna63c-stage-a-certificate` at
`19caa49d7620062c06ad74d19528e47725f86b37`. The published lane commits are:

| Evidence | Commit | Disposition |
|---|---|---|
| Frozen C0-C7 fixture | `583148e2812b93d519a3dc2821944d08446497b7` | Immutable fixture authority |
| W | `17907c67d52cc338249b66f28c3179cd97572c6e` | 100/100 assigned mathematical-witness rows certified; scoped result only |
| T | `0a8c34b7e6febf681917d915082a8559eea998f7` | 9/191 event rows certified; 182 blocked; N3 remains open |
| E | `651f18fdf3c7ae8e32cd210ebc68527f86531e32` | N4-A evidence audited; N4-B incomplete; N4 overall not complete |
| Reviewed design / N4 schema | `3e7d31b9a527e908b21abee3766906084e7cd082` / `9cc92adb56e388d8675d538410b319fd8d8841a5` | Governing design and verification requirements |

The published T manifest pins `inventory.json` SHA-256
`51F54F8F10645030D7DD20EC2C160803C4959609E46062F45ED25C4BBF4CA2A1`
(Git blob `d7c243239ffb9b6cb0f8d8ea25e4954ab4f8fade`) and `schedule.json`
SHA-256 `E47E96711C10ECDA9675868C4BD6324B91163E8BAF576203DE71A99DFAF2F18E`
(Git blob `8f93d36a3da90e15426dd5f66fe5bde4aa0d2a8c`).

## Published T identity reconciliation

The authoritative T `inventory.json` lists 191 event identities; its
`schedule.json` has 191 corresponding rows. Direct set reconciliation against
the exact published commit found 191 unique IDs in each artifact, zero
duplicate schedule IDs, zero missing IDs, and zero extra IDs. These are
event records; the separate 15 observation-only rows are not N3 events.

The fixture totals reconcile as C1 2, C2 31, C3 4, C4 8, C5 24, C6 3, and C7
119, for 191 events. C7's 119 rows are expanded across 14 published cases:

| C7 case | Rows |
|---|---:|
| DUPLICATE_RECALL | 5 |
| ALTERNATING_RECALL | 16 |
| RESET_BEFORE_COMMIT | 7 |
| RESET_AFTER_COMMIT | 11 |
| STALE_TIMER | 7 |
| REARM_BEFORE_QUIET | 12 |
| EXPIRY_COALESCENCE_VALID | 4 |
| EXPIRY_COALESCENCE_INVALID | 4 |
| TIMESTAMP_INVALID | 12 |
| OVERFLOW_17 | 25 |
| POST_ABORT_INGRESS | 1 |
| OUTPUT_EXPIRY_COALESCENCE | 6 |
| NEAR_CLOCK_LIMIT | 3 |
| POSITIVE_SUB_ULP | 6 |
| **Total** | **119** |

The nine certified rows are explicitly identified in the published schedule:

- `C7.NEAR_CLOCK_LIMIT.STORE_LAST_IN_DOMAIN_ORIGIN_1`
- `C7.NEAR_CLOCK_LIMIT.TIMER_EXPIRY_CREATED_FOR_INSTANCE_1`
- `C7.NEAR_CLOCK_LIMIT.STORE_NEXT_ORIGIN_1`
- `C7.POSITIVE_SUB_ULP.STORE_UPPER_Q_NEIGHBOR_1`
- `C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_CREATED_1`
- `C7.POSITIVE_SUB_ULP.RECALL_ON_1`
- `C7.POSITIVE_SUB_ULP.TIMER_QUIET_CREATED_1`
- `C7.POSITIVE_SUB_ULP.TIMER_QUIET_1`
- `C7.POSITIVE_SUB_ULP.TIMER_EXPIRY_INVALIDATED_AT_QUIET_1`

Their certified values, event-time ceilings, ordinals, W evidence references,
and status are retained in the source schedule and copied into the corrected
row-level [`blocker-inventory.json`](blocker-inventory.json). No value or
ordinal was recomputed in this reconciliation.

## Remaining T blockers and A-E classification

The published T handoff reports 182 blocked rows. Their primary blocker
counts reconcile exactly:

| Primary reason | Rows |
|---|---:|
| `ABSOLUTE_ORIGIN_t_store_UNFROZEN` | 85 |
| `EXTERNAL_INPUT_TIME_UNSPECIFIED` | 80 |
| `INVALID_TIMESTAMP_ENVELOPE_NOT_FROZEN` | 12 |
| `RELEASE_ORIGIN_NOT_FROZEN_NUMERICALLY` | 3 |
| `NO_TIMESTAMP_BY_RULE_PRECEDENCE_DEPENDS_ON_BLOCKED_INSTANCE_SCHEDULE` | 2 |
| **Total** | **182** |

The full row-level IDs, source/time descriptions, ordinal state, and exact
reason arrays are recorded in `blocker-inventory.json`; it is no longer a
family-level approximation. Classification is by the present blocker, not
by a downstream obligation:

- **A — derivable/certified:** the nine published T rows above.
- **B — missing concrete schedule information:** the other 182 rows, with
  the exact published primary reason retained per row. The two
  no-timestamp-by-rule records remain blocked on their schedule-dependent
  precedence/ordinal context; no timestamp is invented for them.
- **C — missing semantics:** none identified by this reconciliation. The
  frozen design and owner clarifications govern event precedence and
  lifecycle order.
- **D — numerical boundary ambiguity:** no additional independent D blocker
  is asserted before the missing schedule inputs exist. The required
  N4-B conversion, ceiling, domain, strict-future, and tie checks remain
  downstream work after inputs are frozen.
- **E — other:** none identified in the published T primary blocker set.

No numeric `t_store`/fixture origin, external input times, invalid-envelope
values, reset/pause times, or missing delivery ordinals may be supplied by
inference. The C7 owner decisions already freeze reset after processed
output, represented-binary64 expiry equality, and analytic
`t_rearm < t_quiet`; C2/A=1 checkpoints remain `{0, 1/2, 1, 2}` with strict
L2 error `< theta/4`. These semantics are not reopened here. The actual
schedule values and resulting N3/N4-B mappings remain unfrozen.

## W/E disposition and gate status

W's 100/100 certified rows establish completion only within its assigned
mathematical-witness scope; they do not close global N1. E contains 1,905
obligation rows: 623 PASS, 1,128 BLOCKED, and 154 N/A. All applicable N4-A
audit obligations pass, so N4-A evidence is audited within E's defined scope.
N4-A does not certify a future candidate implementation. N4-B remains
incomplete because the full concrete event schedules and mappings are
absent. E does not choose the missing schedule inputs. Global N1, N3, and N4
are not closed. Lane S/N5 is unauthorized, N6 is deferred, and Stage B is
blocked.

## Provenance and preservation

The parent checkout's untracked W/T/E directories and lane handoffs are
distinct from the named published lane commits. In particular, the
parent-checkout T `schedule.json` is not the published T schedule and is not
used as authority. These local artifacts and the ignored W `.engine/`
payload remain preserved and excluded from the controlled publication set.
The sanitized
[`PUBLICATION_ARTIFACT_RECONCILIATION.json`](PUBLICATION_ARTIFACT_RECONCILIATION.json)
retains relative artifact paths and hashes. The original
`ARTIFACT_RECONCILIATION.json` preservation snapshot, containing workstation
roots, remains local and is not included in publication.

## Validation and next bounded action

**Performed:** rechecked the clean published W/T/E worktrees and exact
commit IDs; parsed the published T inventory and schedule; compared their
semantic-ID sets; reconciled per-fixture and C7 case counts; listed all nine
certified IDs; reconciled all 182 primary blocker counts; and inspected the
published E handoff and 1,905-row matrix summary.

**Not performed:** no lane checker or test rerun, schedule generation,
numerical calculation, fixture execution, T correction, E re-audit, N5
synthesis, N6, Stage B, or LTRD work.

The next bounded action is to obtain an owner-frozen supplemental schedule
for the missing numeric origins, external envelopes, reset/pause inputs, and
ordinals, then separately dispatch only an authorized Lane T completion
against those exact bytes. Preserve the existing 191-ID ledger and nine
certified rows. Independent review of this corrected governance package is
still required before controlled publication. No architecture change or ACP
is proposed.
