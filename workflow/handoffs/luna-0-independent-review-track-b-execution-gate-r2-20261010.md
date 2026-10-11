# Independent review — Luna-64 Track B execution gate R2

**GATE:** `L64-TB-GATE-20261010-R2`  
**REVIEW VERDICT:** **BLOCKED**  
**REVIEW SCOPE:** Read-only governance and mathematical consistency review of
the exact R2 proposal identified below.  
**R2 PROPOSAL SHA-256:** `64529FD816824A3EAA246856C3BEF46E6FDD97CCDF8ED48830C27AEF558D5A0A`  
**SOURCE BASELINE:** `73aaa50f97ceab322907875ae4dcf23e7541c3b5`  
**OWNER APPROVAL:** NOT PROVIDED  
**EXECUTION AUTHORIZATION:** NOT GRANTED

No files were edited by the reviewer. No experiment, benchmark,
microbenchmark, branch, or worktree was created. The review was confined to
R2 and relevant repository governance/runtime sources. R0 and R1 remain
unchanged.

## Findings

### Blocking

1. **No R2 machine-readable protocol or golden benchmark fixtures.** R2 is a
   prose proposal but its own R1-to-R2 matrix promises comparison “to protocol
   JSON.” The only referenced protocol is the R1 JSON, which predates the R2
   timebase correction and still contains `tu_per_integer_tick: 1000000`.
   That field conflicts with R2's `1 tick = 10^-6 TU`. This is not evidence
   that the R2 prose is inverted; it is a failure to provide an R2 protocol
   and leaves a known incompatible predecessor artifact as the apparent
   counterpart. Do not freeze until a new protocol is either produced and
   byte-bound to R2 or the protocol-JSON requirement is explicitly removed.
   If retained, use unambiguous reciprocal fields and test them.

2. **Task generator and output contract remain unspecified.** R2 does not
   define the temporal-ordering and timing-reward sequence distributions,
   exact event sequences, labels/targets in the evaluator, generator PRNG
   algorithm and draw order, split assignment, or a decoder-to-task output
   mapping. Consequently the benchmark matrix is not executable and its
   balanced-accuracy thresholds cannot be assessed. R2 itself acknowledges
   the missing readout and absent golden fixtures. This blocks any efficacy
   execution gate.

3. **Reward source and scientific objective remain open.** The proposed
   positive reward is not tied to a predeclared correct temporal prediction or
   other accepted local utility; R2 says the source is not approved. A fixed
   positive reward on B reception is not a resolved timing-dependent reward
   assignment. The owner/scientific decision must be made before the gate can
   define what a successful reward decoder does.

4. **Arm E and dual-clock semantics are not closed.** The complementary-gap
   transform is causally computable from the current gap, but it is not the
   originally requested time-shuffled control, and the proposal leaves
   decoder-local elapsed time and physical reward delivery in separate clock
   domains without a validated scheduling rule. The reviewer cannot establish
   fair paired exposure or identical reward opportunities from the prose
   alone. Choose and fully specify the authorized control and define the
   event/queue integration before freeze.

5. **Credit snapshot and settlement rules are incomplete at 16-TU delay.**
   Per-input eligibility expires after 8 TU, while reward may arrive at 16 TU.
   R2 mentions an activation-associated snapshot but does not define exactly
   which eligible inputs/gradient values the activation captures, their
   decay reference time, or the update applied at settlement. The cleanup
   horizon is also expressed relative to final input, while the proposed
   episode duration/maximum reward delay is not reconciled for a final input
   at the boundary. Provide event traces covering activation, final input,
   due reward, due+1 expiry, sequence close, settlement, and reset.

6. **Execution budget is not established.** R2 gives analytic caps but no
   executable per-event operation accounting; the bound does not include
   demonstrated interpreter, serialization, hashing, output and test-runner
   overhead. The four-hour/one-core/2-GiB limits are explicitly unmeasured.
   No empirical smoke test is authorized in the current phase, so feasibility
   remains an execution prerequisite rather than a passed gate.

7. **LWC is a new, unapproved metric.** The proposed coefficients have no
   repository or hardware authority, and instrumentation semantics (including
   counter ownership and exact operation counting) are not implemented or
   validated. R2 correctly labels it a proposal; it must not be a gate metric
   absent owner approval and a reproducible specification. Raw counters and
   the existing `activity-cost-proxy` may be reported separately with their
   limitations.

### Non-blocking for governance review; required before scientific claims

8. **Finite-difference and fixture validation not performed.** The reviewer
   manually checked the one-step worked example's arithmetic and found it
   consistent to the stated rounding. This does not verify the full
   four-iteration model gradients, clipping behavior, parameter updates,
   eligibility decay, or serialization. R2 correctly marks those checks
   unrun; they remain mandatory before any experimental freeze.

9. **Five-seed interval is exploratory.** The `5^5 = 3,125` enumeration and
   nearest-rank indices 20 and 3,106 are arithmetically consistent with the
   proposed quantiles. Five seed clusters do not establish interval coverage
   or power. R2 acknowledges this limitation; do not present this interval as
   validated confirmatory inference without a justified design.

10. **Luna-63C and source isolation claims preserved.** R2 explicitly forbids
    Luna-63C and production paths and keeps the source baseline separate from
    execution. No R2 execution branch/worktree exists. These are consistent
    with the stated isolation objective; authorization is still absent.

## R1 finding traceability

| R1 issue | R2 review disposition |
|---|---|
| Reward origin/order | Unresolved; fixed B-reception reward not approved or linked to task correctness |
| Eligibility expiry and episode lifetime | Partially formalized; 8-TU trace versus 16-TU settlement and final-input horizon remain unresolved |
| Model and learning equations/count | Candidate equations and 40-parameter count are specified; hand example is consistent, but readout and independent derivative validation remain open |
| Dataset/generator reproducibility | Unresolved; no complete generator, PRNG draw contract, or golden fixtures |
| Arm fairness / temporal control | Unresolved; E is a complementary-gap control, not a shuffled-order control, and clock integration is not frozen |
| Statistics | Arithmetic specified; five-seed coverage/power unvalidated and exploratory |
| Runtime feasibility | Analytic proposal only; measured feasibility not established |
| LWU / resource metric | LWU appropriately not claimed; LWC is unapproved and must not be used as an acceptance metric yet |

**Fully resolved R1 findings:** none. R2 makes useful specification progress,
but the unresolved items are correctly disclosed and remain gates.

## Verdict and next bounded action

**BLOCKED — not ready for owner authorization.** This verdict is independent
of owner approval; none was provided. It does not authorize code, an
experiment, branch/worktree creation, or any change to the Luna-64 contract.

Next bounded action: prepare a new immutable protocol/fixture package only
after resolving the task generator/readout, reward source, control-arm
semantics, and credit lifecycle; bind it to the proposal and rerun an
independent review. Do not alter R0, R1, or this review. Owner approval must
then explicitly identify the reviewed package bytes. Even a future review
PASS means only READY FOR OWNER AUTHORIZATION.
