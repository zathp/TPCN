tpcn_handoff:
  agent: Luna-11 Adversarial Architectural Verification
  task_id: "adversarial-verification-luna-11"
  component: "independent integrated TPCN architectural verification"
  status: "dispatched"
  contract_version: "1.0"
  branch: "main"
  base_revision: "cab30253d6aeeea4abc3c7ebfa7bba1105e21488"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "Luna-1 through Luna-8 interfaces and the existing integration baseline."
    - "Classifier remains an external readout; labels remain outside inference."
    - "Experimental gating, structural plasticity, real dataset benchmarking, and hardware acceptance remain deferred."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-11.agent.md"
    - "workflow/handoffs/adversarial-verification-Luna-11.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All Luna-11 adversarial attacks: dispatched, not run."
    - "Focused adversarial suite count: not run."
    - "Full regression, compilation, diagnostics, and git diff --check by Luna-11: not run."
  assumptions:
    - "The prior joint-review handoff is the supplied integration baseline; Luna-11 must independently reproduce or challenge it."
    - "The exact current worktree is dirty; unrelated user changes must be preserved."
  unresolved:
    - "All required adversarial verification outcomes remain pending."
  recommended_next_agent:
    - "Luna-11: execute the attack matrix and complete this handoff with evidence."
    - "Luna-0: review the completed Luna-11 handoff and gate later phases only after unresolved findings are cleared."

## Outcome and owned scope

Luna-11 is dispatched to actively falsify the integrated Luna-1 through Luna-8
architecture. It owns adversarial tests, code-path inspection, minimal
reproducers, and evidence reporting only. It must not patch production defects
or authorize Luna-9, Luna-10, the real dataset benchmark, or hardware work.

## Architecture evidence required

| Area | Contract mapping | Required adversarial evidence |
|---|---|---|
| Causality and temporal boundaries | A01-A03, A06-A07 | Future labels/rewards, queued events, retries, out-of-order delivery, and END_STROKE/END_CHARACTER attacks cannot alter an earlier authoritative result. |
| Label isolation and local state | A07 | Identical inference activity remains identical when labels are changed/removed until a legitimate learning update; independent instances do not cross-talk. |
| Finite topology and propagation | A03-A04 | Positive-hop delivery, bounded fan-in/out, route/queue capacity, retry behavior, and no convenience-path bypass. |
| Bounded dynamics and state | A04, A08, A11, A14 | Long legal streams keep queues, traces, rewards, classifier state, topology, caches, and diagnostics within declared bounds. |
| Prediction, credit, and energy | A06-A11 | Error identity, delayed reward timestamps, expiry, duplicate handling, local accounting, and useful/high-cost versus unproductive/high-cost behavior. |
| Portability and clock discipline | A01, A02, A15 | No hidden wall clock/global timestep/global mutable state; event semantics remain software-reference and hardware-portable. |

No ACP is required for verification. An observed architectural departure or
ambiguous contract must be reported to Luna-0 before any promotion decision.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| Luna-11 hostile attack matrix | Pending dispatch execution | not run | To be recorded by Luna-11 |
| Focused adversarial suite | Pending dispatch execution | not run | To be recorded by Luna-11 |
| Full regression | Pending dispatch execution | not run by Luna-11 | Prior joint-review evidence is not independent Luna-11 evidence |
| Compilation | Pending dispatch execution | not run by Luna-11 | To be recorded by Luna-11 |
| Diagnostics | Pending dispatch execution | not run by Luna-11 | To be recorded by Luna-11 |
| `git diff --check` | Pending dispatch execution | not run by Luna-11 | To be recorded by Luna-11 |

## Completion gate

Luna-11 passes only with no unresolved production defects or architectural
ambiguities affecting required invariants. Every area must be classified as
passed, failed, not run, or not applicable, with exact commands and evidence.
The final report must identify fixture defects, owning Luna for repairs,
regression tests, focused/full counts, and remaining limitations.

## Reproduction and rollback

Run from the recorded baseline/worktree with unrelated changes preserved.
Do not create branches or alter architecture. If a production repair is
needed, return ownership to the relevant Luna and retain a minimal reproducer.

## Next assignment

After a completed, passing Luna-11 handoff, return control to Luna-0. No later
experimental, benchmark, or hardware role is authorized by this dispatch.
