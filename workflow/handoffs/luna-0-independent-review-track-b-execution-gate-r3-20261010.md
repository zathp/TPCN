# Independent review — Luna-64 Track B execution gate R3

**GATE:** `L64-TB-GATE-20261010-R3`  
**REVIEW VERDICT:** **BLOCKED — not ready for owner authorization**  
**REVIEW SCOPE:** Independent, read-only governance review of the exact R3
package identified by its manifest.  
**SOURCE BASELINE:** `73aaa50f97ceab322907875ae4dcf23e7541c3b5`  
**OWNER APPROVAL:** NOT PROVIDED  
**EXECUTION AUTHORIZATION:** NOT GRANTED  
**ARCHITECTURE PROMOTION:** NOT AUTHORIZED

This review is separate from the R3 proposal and local consistency report.
It is not owner approval, execution authorization, or architecture approval.

## Exact-byte and repository verification

The reviewer verified `HEAD` at
`73aaa50f97ceab322907875ae4dcf23e7541c3b5` on `main`. All six candidate
artifact hashes match
[`luna-0-track-b-execution-gate-r3-manifest-20261010.json`](luna-0-track-b-execution-gate-r3-manifest-20261010.json).
The predecessor R2 proposal and review hashes also match. The consistency
report's five artifact hashes match their manifest entries.

The worktree is not clean. The pre-existing modified workflow/changelog and
untracked Luna-64 and R0–R3 governance files remain outside the source
baseline. The reviewer made no edits. No execution branch/worktree,
implementation, experiment, or promotion was performed.

## Blocking findings

1. **The specified credit rule is not temporally selective — high confidence.**
   The protocol gives every eligible input the same share of the final
   episode-level readout eligibility:
   `e_i=(1/n)*(2*a-1)*concat(h,1)`. Summing those shares yields an update
   based on final `h`; input identity, timing, and contribution do not change
   its share. Since the task lasts at most 5 TU and the eligibility window is
   8 TU, all task inputs are eligible at activation; expiry behavior is
   exercised only in lifecycle fixtures. This does not establish the
   contract's temporal-selectivity objective.

   **Required resolution:** define and justify genuinely local,
   input-specific temporal eligibility, or obtain an explicit owner decision
   narrowing the experimental claim/objective. Do not describe the current
   rule as selective attribution.

2. **The multi-event PCN recurrence is incomplete — high confidence.**
   The protocol defines an objective, gradient, and inference update but does
   not define how `z0` is formed from the previous latent state and elapsed
   time, or an unambiguous latent initialization value for every episode.
   The one-event golden fixture's zero-valued `z_previous`/`z0` does not
   specify the four-event task transition. Reset at cleanup also does not
   specify the reset value. Different conforming implementations could
   therefore produce different task representations.

3. **The validator does not enforce duplicate-key rejection — high
   confidence.** The protocol requires Draft 2020-12 validation rejecting
   duplicate JSON object keys, but the local validator uses native
   `JSON.parse`, which silently resolves duplicate keys. The recursive
   checker cannot recover duplicates after parsing. The structural PASS in
   the consistency report does not satisfy this freeze requirement.

4. **Statistical decision and replay rules are incomplete — high
   confidence.** The bootstrap does not define exact key assignment for its
   root seed, comparison, replicate, and sampled index, so results cannot be
   independently replayed solely from the protocol. Decision branches also
   leave intermediate cases unspecified (for example D balanced accuracy
   between 0.55 and 0.70, or positive effects below the success threshold),
   and failure/inconclusive rules can overlap without precedence.

5. **The 20-seed design and 32-unit ceiling are not sufficiently justified
   for their proposed decision use — medium-high confidence.** The proposal
   acknowledges that 20 seeds are exploratory and not power-derived, but
   still makes seed-cluster percentile intervals part of hard success
   criteria without a precision target or adequacy basis. It raises the
   planned work to 1.2 million episodes while retaining a four-hour limit.
   The 32 computational-unit cap is explicitly defined but not shown to be
   informative: its counting rule excludes external channels, parameters,
   and scratch, and current arms use only 1/5/9/13/13 units.

6. **Runtime feasibility remains unresolved — high confidence.** Operation
   ceilings are analytical, and the protocol explicitly marks runtime and
   memory feasibility as unmeasured. With no authorized smoke run or
   benchmark, feasibility of 1.2 million episodes within four hours and
   2 GiB is unknown. This remains an R2 blocker, not a passed acceptance
   check.

7. **Governing Luna-64 contract and prior governance record are not bound to
   the manifest — high confidence.** The Luna-64 contract and governance
   handoff are untracked and absent from the stated baseline commit, and are
   not included in the R3 manifest. The workflow/changelog Track B additions
   are likewise uncommitted. The manifest therefore does not bind all
   governing inputs by hash and committed freeze revision. The prior
   governance PASS is a documentation-only governance result, not approval
   of R3; R0 and R2 gate reviews are BLOCKED.

   **Required resolution:** bind exact hashes for the governing contract and
   prior governance record to an immutable committed freeze revision before
   seeking owner authorization.

8. **The cost-benefit objective is not demonstrated — medium confidence.**
   The readout update is reward-only; the configured activity-cost proxy
   charges once per input and zero for reward settlement, with identical
   input counts across arms. Raw operation counters are reported separately,
   but no predeclared cost-effectiveness threshold or cost term allows the
   gate to conclude whether additional computation is justified. The
   correctness oracle is explicit rather than hidden, but its signed reward
   is label-equivalent information when combined with the recorded
   prediction; the owner must knowingly accept that oracle boundary.

## R2 finding disposition

- **Addressed in candidate form:** protocol/golden package; task schedule
  and readout definition; post-prediction correctness-only reward; Arm-E
  mapping and physical-clock separation; 8-TU admission versus 16-TU
  settlement; removal of unapproved LWC from acceptance.
- **Still blocking:** selective credit; multi-event PCN transition;
  duplicate-key validation; replayable bootstrap keys and exhaustive,
  non-overlapping decision outcomes; justification of seed/unit limits;
  empirical resource feasibility; immutable provenance for the governing
  contract and prior governance record.
- **Preserved:** Luna-63C evidence remains outside the allowlist and was not
  modified. No global neural timestep or physical-clock remapping is implied.
  No implementation, execution branch/worktree, or architecture promotion
  is authorized.

## Validation performed by reviewer

The reviewer read the R3 manifest and candidate package, R2 and R0 reviews,
governance handoff, Luna-64 contract, Luna-63C boundaries, architecture
contract, acceptance criteria, workflow/proposal guidance, and handoff
template. The reviewer checked repository revision/status, computed
manifest and predecessor SHA-256 values, and cross-checked consistency-report
hashes against the manifest.

The reviewer did **not** run the R3 validator, formal Draft 2020-12
validation, tests, a fresh finite-difference calculation, generator or
statistical replay, training, experiments, evaluations, benchmarks, or a
smoke run. The local consistency report's PASS results remain package
claims, not independently rerun results.

## Disposition and next bounded assignment

**Review verdict:** **BLOCKED — not ready for owner authorization.**  
**Owner approval:** NOT PROVIDED for this exact package.  
**Execution authorization:** NOT GRANTED.

Next bounded assignment: prepare a versioned corrective governance package
resolving temporal credit attribution and PCN state transitions, completing
duplicate-key-safe parsing and statistical replay/outcome rules, justifying
resource and sample-size choices, and binding the exact governing inputs to
an immutable freeze. Submit that exact package to an independent Luna-0
review. No Luna-64 implementation or scientific execution is authorized
while these gates remain open.
