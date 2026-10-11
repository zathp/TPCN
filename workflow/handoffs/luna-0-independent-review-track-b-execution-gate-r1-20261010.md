# Luna-0 independent review — Track B / Luna-64 gate R1

**Gate:** `L64-TB-GATE-20261010-R1`  
**Verdict:** **BLOCKED**  
**Confidence:** High that the package contains unresolved mandatory design gates and internal contradictions.  
**Owner approval:** Not provided.  
**Execution authorization:** Not granted.

This independent review is read-only. It is distinct from the original
documentation-only Track B governance PASS and does not amend that PASS or
the Luna-64 execution contract.

## Reviewed bytes and provenance

| Artifact | SHA-256 verified by reviewer |
|---|---|
| R1 proposal `workflow/handoffs/luna-0-track-b-execution-gate-proposal-20261010-R1.md` | `44BD46E561BDD9329616B38C3AE6A74A1E79BEB497BB274A4D552C6096FC46B6` |
| R1 protocol `experiments/luna64/luna64-track-b-protocol-r1.json` | `A90F167C5C09DC84E7B15B778770A3115CAB7AB91177AE3D0A026E755B013CAF` |
| R1 manifest `workflow/handoffs/luna-0-track-b-execution-gate-r1-manifest-20261010.json` | `ABA66E320A73C9AC687C3608D0E6A06A1B62A8ABA7F8AC93947DA0391FD2A5EF` |
| R0 proposal predecessor | `5B4C8E74C3536AEA7111C749970FF44BA3DB8855317679C6EF013EAB5149CF08` |

The proposal and protocol hashes and R0 predecessor hash match. Both JSON
documents parse. The reviewer confirmed `HEAD`, `main`, and local
`origin/main` at `73aaa50f97ceab322907875ae4dcf23e7541c3b5`; governance
changes remain uncommitted. This is a source baseline candidate, not an
execution freeze. No tests, experiments, generator materialization, model
fixtures, benchmarks, hardware validation, branches, or worktrees were run
or created.

## Findings that block R1

1. **Model equations and parameter budget are incomplete/inconsistent.**
   R1 leaves PCN/update/readout/learning equations unfinished. Its proposed
   eight-channel by four-delay feature interpretation followed by an
   eight-dimensional hidden state and eight-channel prediction requires
   336 parameters for ordinary dense matrices
   (`W=256 + b=8 + V=64 + c=8`), already over the 256-parameter ceiling
   before readout. No approved tying, sparsity, or reduced dimensions are
   frozen. R0 finding 3 remains open.
2. **Protocol and machine-readable timebase disagree.** The prose states
   1 TU is 1,000,000 integer ticks, while JSON says
   `tu_per_integer_tick: 1000000`, the reciprocal relation. The complete
   draw-name scheme, pairing/base IDs, and golden fixture hashes are also
   absent. R0 finding 4 remains open.
3. **Arm E reward schedule conflicts with the local activation rule.** R1
   states that every B reception causes activation and that reward is
   delivered at activation time plus delay, while E reverses event identities
   across time slots. Since B is moved, its activation and reward timestamps
   change; this cannot both preserve the same reward stream and keep
   B-triggered local rewards. Also, forced B activation is not the
   decoder-dependent postsynaptic activation contemplated by the scientific
   objective. R0 findings 1 and 5 remain open.
4. **Credit lifetime and episode lifecycle are contradictory.** The text
   defines expiry both as `nextafter(due,+∞)` and activation plus the maximum
   16-TU delay. For delays 0 and 4 these differ. The identity list references
   an `eligibility_snapshot_id` but does not define its construction. The
   protocol limits an episode to 16 TU while a reward at activation time plus
   16 TU occurs after the episode for positive-time activation. No close,
   drain, or reset semantics resolve it. R0 finding 2 remains open.
5. **Evaluation scoring conflicts with frozen evaluation.** Evaluation
   disallows parameter updates, but attribution metrics ask for parameter
   update deltas and use a 0.01 update threshold. The proposal does not define
   a separate unapplied counterfactual update. Arm A has no predictive output
   yet is used in a correct-per-energy threshold with no correct denominator.
   It also sets a negative-control balanced-accuracy limit while removing
   controls from primary classes without defining control labels/scoring.
   Forced B activations and classifier-positive outputs are not distinguished
   in the false-activation metric. R0 finding 5 remains open.
6. **LWU or a complete alternative meter is still unavailable.** Repository
   `LocalEnergyModel` defaults to `activity-cost-proxy` and exposes
   configurable activity costs; it defines neither LWU nor operation-weight
   coefficients. R1 correctly rejects R0's invented coefficients but
   acknowledges that category costs and metering validation remain missing.
   R0 finding 8 remains open.
7. **Runtime feasibility is not established.** The reviewed arithmetic is
   internally consistent for the stated subtotal: 800,000 episode executions,
   26,214,400,000 scalar operations, and 1,820,445 operations/second for the
   four-hour ceiling. But integrity replay and complete event processing are
   excluded, and the process memory/log caps are not validated. This is not
   a feasibility result. R0 finding 7 remains open.
8. **The matrix corrections are partial, not closure.** Evaluation counts
   total 2,000 and the delayed probes yield 132 per delay; the exhaustive
   `5^5=3,125` resampling count and nearest-rank positions 20 and 3,106 are
   arithmetically correct. The four 98.75% intervals implement the proposed
   Bonferroni family alpha of 0.05, but five seed clusters do not establish
   coverage or power. Required independent generator and statistical fixtures
   are absent. Findings 4 and 6 remain open.

## Finding-to-correction matrix disposition

| R0 finding | R1 independent-review disposition |
|---|---|
| 1 — Reward origin/order | Candidate value, recipient and event phases proposed; reward/E contradiction, unresolved accepted reward semantics, and incomplete identity details prevent closure. |
| 2 — Eligibility lifetime | Option B has a bounded count proposal, but expiry differs by delay and episode drain/reset conflicts with due reward timing. |
| 3 — Model/training lifecycle | Parameter persistence/frozen evaluation are described; central equations and parameter budget are not frozen or reconciled. |
| 4 — Dataset reproducibility | Counts and broad RNG family proposed; reciprocal timebase conflict, complete draw mapping, paired IDs, and golden fixtures are missing. |
| 5 — Arm fairness/scoring | Paired streams are proposed; E reward timing, frozen-update attribution, control scoring, activation meaning, and Arm A efficiency denominator conflict or remain undefined. |
| 6 — Statistical analysis | Proposed bootstrap is deterministic and arithmetic checks pass; the independent analysis fixture and evidential adequacy are absent. |
| 7 — Budget | Upper-bound arithmetic is partially checked; full work/space accounting and empirical budget adequacy are not established. |
| 8 — LWU | No authoritative LWU definition exists; R1 does not invent one, but no fully validated replacement instrumentation contract is frozen. |

The detailed line references and checked arithmetic are retained in the
independent reviewer output summarized above and can be regenerated by
reviewing the exact hashes listed here. No experimental evidence is claimed.

## Architecture, authorization, and next action

The read-only review found the dedicated branch/worktree plan and Luna-63C
write prohibitions compatible on paper. No Luna-63C modification or
dependency is authorized or proposed. The Luna-63C certificate remains
independently gated; Track B does not resolve that gate. A01-A15, ACP status,
and the production baseline are unchanged.

R1 proposes reward timing/source, eligibility representation, allocations,
statistical analysis, and metering choices that remain unaccepted proposals.
The original governance handoff permits documentation-only preparation and
does not authorize execution. Requesting this R1 package is not owner approval.

**Next bounded assignment:** Luna-0 governance-only R2 preparation. Resolve
the exact PCN and reward equations and parameter count; timebase and all
golden generator fixture definitions; reward/E matching; credit expiry and
episode close/drain/reset; update-free attribution diagnostics; control and
Arm A scoring; authoritative meter choice or owner-approved proxy definition;
and complete feasibility bounds. Obtain owner decisions wherever the
resolution changes the preserved Luna-64 scope. Then submit exact R2 bytes
for another independent review.

Until those gates pass: **R1 BLOCKED; OWNER APPROVAL NOT PROVIDED; EXECUTION
NOT AUTHORIZED; NO EXPERIMENT BRANCH/WORKTREE OR LUNA-64 IMPLEMENTATION.**
