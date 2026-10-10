# Luna-63C Stage A — C0-C7 fixture-freeze handoff, 2026-10-10

**Disposition: FIXTURE FREEZE — INDEPENDENT LUNA-0 PASS.**

This handoff reports the design-derived C0-C7 fixture inventory and its
validation. It is a fixture-freeze prerequisite, not a numerical certificate,
scientific execution, Stage-B authorization, or claim of efficacy.

## Revision and source identity

| Item | Identity |
|---|---|
| Branch | `experiment/luna63c-stage-a-certificate` |
| Starting HEAD | `47dd26f08dfa113565ad41f1abe34888eed0e0bf` |
| `origin/main` | `73aaa50f97ceab322907875ae4dcf23e7541c3b5` |
| Reviewed Luna-63C design revision | `3e7d31b9a527e908b21abee3766906084e7cd082` |
| Latest design handoff revision | `a303ebb835b72fdd01c86df478431b8638aacbb4` |
| N4 schema revision | `9cc92adb56e388d8675d538410b319fd8d8841a5` |
| N4 schema independent review revision | `47dd26f08dfa113565ad41f1abe34888eed0e0bf` |

The tracked worktree was clean at the starting revision. Pre-existing
untracked W/T/E lane directories and handoffs were preserved and not used as
authority or modified. The freeze adds:

- `experiments/luna63c/fixture-freeze/FIXTURE_FREEZE.md`
- `experiments/luna63c/fixture-freeze/fixtures.json`
- this handoff, the workflow entry, and the changelog entry.

The normative v1 blocked certificate files, expected-outcomes table, and
manifest were not edited. The new fixture freeze is separate and explicitly
identifies those values as historical blocked evidence.

## Owner decisions represented

1. For post-commit reset, output remains pending/persistent from mathematical
   crossing `t_root` until processing at `t_emit`; cleanup follows processing.
   A represented timestamp tie gives processing precedence.
2. Expiry coalescence is equality after governed binary64 ceiling conversion
   of distinct real event times; reviewed expiry precedence applies. No
   artificial exact-real equality is introduced.
3. Mathematical re-arm precedes quiet strictly; no synthetic equality
   fixture is introduced. If represented timestamps coalesce, retain the
   analytic order and apply reviewed precedence.
4. C2/A=1 observation times are exact active/reference-time rationals
   `{0,1/2,1,2}` TU, not runtime events/timers.
5. Candidate/oracle comparison is strict L2 `< theta/4`; equality fails and
   a straddling certified interval is unresolved. `theta/4` is an acceptance
   ceiling, not an asserted implementation error.

At A=1, quiet occurs at `s_q=ln(1/q)=pi/4+(ln 2)/2<2`. Thus the ideal
hybrid candidate has terminal state `(0,0)` at `s=2`, while the independent
unreset semigroup oracle remains
`p*exp(-2)*(cos(2),sin(2))`; the exact ideal discrepancy is `exp(-2)`.
The freeze records the strict mathematical margin
`exp(-2)<theta/4` for independent certification. This is not an observed
candidate result; no candidate implementation exists or was run.

## Fixture coverage and mapping

The machine-readable inventory includes all eight repository fixture
identities C0-C7. C7 retains all fourteen design-listed edge-case categories.
Every repeated event occurrence has a unique identity; bounded input ranges
expand to one identity per attempt. The overflow case is frozen as one STORE,
eight RECALLs including duplicates, and seven semantically rejected STORE
attempts, followed by attempt 17 without timestamp validation. Output is
processed before the later 14 inputs, and the committed output persists
through overflow cleanup. The positive sub-ULP case includes its RECALL at
the STORE timestamp and measures strict-future delay from that processed
cause. C3 is only the held observation family; release after `{0,1,2}` is
confined to C5.

It includes stable event/case identities, exact or mathematical time-source
definitions, causal and precedence dependencies, checkpoint identities,
N1 witness mappings, N3 event mappings, and applicable N4-A/N4-B obligations.
It deliberately leaves computed numeric enclosures, binary64 ceilings, and
final destination ordinals for numerical lanes. The C7 inventory now fixes
`p=+1` for every `A=4` occurrence, including cases that inherit the C4
schedule; no C7 A=4 case leaves polarity implicit.

The exact field, `alpha=omega=1`, `g`, `theta`, `q`, event surface, `H`,
`T_q`, `T_life`, clock domain, and arithmetic profile are carried forward.
Existing resource bounds remain 16 within-budget attempts, one overflow
attempt, 24 timer records, one output, and 42 unique records. The inventory
does not expand a bound or promote any experimental mechanism.

## Validation

Observed checks:

- Parsed `fixtures.json` with Python's standard-library JSON parser.
- Confirmed fixture IDs are exactly `C0` through `C7`.
- Confirmed all 14 C7 subcase IDs are present and distinct.
- Confirmed the machine-readable C3 inputs contain only the held STORE
  schedule, with release after the listed HOLD durations reserved for C5.
- Confirmed overflow input occurrences account for exactly 16 within-budget
  attempts before timestamp-free attempt 17; the committed output is processed
  before those later inputs.
- Confirmed the positive sub-ULP case includes STORE, RECALL, quiet, and
  expiry, with strict-future measured from the processed RECALL cause.
- Expanded the C7 case event/action identities and confirmed all 119
  fully-qualified occurrences are distinct, including the timestamp-invalid
  variants and the 16-input/attempt-17 overflow path.
- Confirmed named fresh-instance boundaries, explicit C4/C3 inheritance,
  and the creation/cancellation/pop/invalidation references for relevant
  C7 timer records.
- Confirmed A=1 checkpoint times are `["0","1/2","1","2"]`.
- Confirmed C2/A=1 has separate P/N checkpoint identities at each exact
  active-time observation and every C7 A=4 schedule is explicitly `p=+1`.
- Confirmed resource arithmetic `16+1+24+1=42`.
- `git diff --check` passed.
- Historical certificate files remained unchanged.

No solver, runtime, numerical evaluator, C0-C7 execution, numerical
certification, W/T/E calculation/resume, Lane S, or N5 synthesis was run.
No 63A implementation or 63B result was imported or used.

## Gate state and independent review

The first read-only independent Luna-0 review returned **BLOCKED** on three
findings: C3's machine-readable schedule included release while expecting no
output; the C7 positive sub-ULP case omitted RECALL; and repeated/aggregate
C7 input occurrences were not uniquely identified. Those issues have been
corrected in this revision of the working artifacts. A new independent
Luna-0 review of the exact corrected hashes is required before W/T/E resume.
Until that review returns PASS, W/T/E remain paused; Lane S/N5 and Stage B
remain blocked. The freeze itself does not close N1, N3, N4, N5, or N6 and
does not authorize integrated sequence echo, Luna-64, an ACP change, an
A01-A15 change, or production/default integration.

Reviewer assignment should be read-only and verify the exact inventory
against the reviewed design, N4 schema, and the two owner clarifications,
including the C2 active/reference-time interpretation and the C7
represented-time/lifecycle ordering. The reviewer must not run scientific
fixtures or numerical calculations.

The first independent review verified its supplied working-tree SHA256
identities and returned **BLOCKED** with three corrections: C3 had combined
HOLD and release in its machine-readable inputs while requiring zero output;
the positive sub-ULP case omitted RECALL and its processed-cause dependency;
and repeated/aggregate C7 occurrences did not have unique event identities.
The current working artifacts address each finding as described above.
The correction validation passed; this is not itself independent approval.

A subsequent independent review returned **BLOCKED** because several C7
schedules still lacked complete causal setup and timer-record lifecycle
coverage. It specifically identified alternating RECALL, re-arm/quiet,
expiry coalescence, stale timer origin, output/expiry coalescence, and
near-clock fresh-instance schedules. The current working inventory adds
explicit symbolic predecessors/constraints, fresh-instance or inherited
prefix rules, unique timer record identities, and creation/cancellation/
pop/invalidation references without assigning computed timestamps or
ordinals. This correction batch has passed local structural validation only
and requires another independent review.

## Independent review disposition

Independent Luna-0 review returned **PASS — fixture-freeze gate only** for
the exact snapshot listed below. All five supplied SHA-256 values matched
before and after review; the reviewer found no blockers within scope:

| Reviewed file | SHA-256 |
|---|---|
| `experiments/luna63c/fixture-freeze/fixtures.json` | `AF81F3390274B2D565F90CBF12C116C78F45C5DF65D6C28BA88194E9DF2F70FB` |
| `experiments/luna63c/fixture-freeze/FIXTURE_FREEZE.md` | `B3BB25D65A8344363DF17F2A6FF3085034FDC431605B6FBA729499D512BE667F` |
| This handoff, as reviewed | `4349EDA2ADD8E1A07E63FF72BA01DBCEC788CA4BA46128E7E22B114867464378` |
| `workflow/docs/luna/LUNA_WORKFLOW.md` | `95CA14905194C9C779622A55B24B8A7AA8BA2DDCA3E4271E564B3AD2F0468340` |
| `workflow/ARCHITECTURE_CHANGELOG.md` | `1DEEC45F28DC9780B85A4C3919C349D316FD69F488ABF25ACB7C11857C7AA5AE` |

The review independently confirmed the normative design, handoff, N4 schema,
and execution contract pins; C0-C7 mappings; the exact field and 42-record
cap; owner-specified C2/A=1 and C7 semantics; explicit C7 A=4 polarity; and
119 unique expanded C7 event/action identities. It found no freeze-scope
blocker. This appended section records the review outcome; the reviewed
fixture inventory and freeze report above remain unchanged.

This PASS closes only the fixture-freeze review. It does not authorize
resuming W/T/E, numerical certification, Lane S/N5, Stage B, solver/runtime
implementation, or scientific fixture execution. The owner clarification
did not authorize any of those successor activities, so they remain paused.
No source was edited by the reviewer, and no experiment was run.
