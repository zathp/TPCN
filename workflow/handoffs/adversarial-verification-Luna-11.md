tpcn_handoff:
  agent: Luna-11 Adversarial Architectural Verification
  task_id: "adversarial-verification-luna-11"
  component: "independent integrated TPCN architectural verification"
  status: "blocked"
  contract_version: "1.0"
  branch: "main"
  base_revision: "af5575ce0a629f101486bf36d930218eecdef77b"
  result_revision: "uncommitted"
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10", "A11", "A14", "A15"]
  preserves:
    - "Luna-1 through Luna-8 interfaces and the existing integration baseline."
    - "Classifier remains an external readout; labels remain outside inference."
    - "Experimental gating, structural plasticity, real dataset benchmarking, and hardware acceptance remain deferred."
  architecture_change: false
  proposal: null
  files_changed:
    - "tests/test_luna11_adversarial.py"
    - "workflow/handoffs/adversarial-verification-Luna-11.md"
  tests_added:
    - "tests/test_luna11_adversarial.py: 10 focused adversarial tests"
  tests_passing:
    - "Focused Luna-11 suite: 8 passed, 2 strict xfailed for confirmed Luna-7 defects"
    - "Full regression suite: 84 passed, 2 strict xfailed"
    - "python -m compileall -q tpcn tests"
    - "git diff --check"
    - "Workspace diagnostics for touched tests and tpcn: no errors"
  tests_failed:
    - "Luna-7 retry ordering: rejected future event advances classifier timestamp"
    - "Luna-7 direct finalization: public finalization does not commit classifier timestamp"
  tests_not_run:
    - "Actual dataset benchmark: deferred and not applicable to architectural verification."
    - "FPGA, FPAA, hybrid, and calibrated hardware validation: deferred."
  assumptions:
    - "The prior joint-review handoff is the supplied integration baseline; Luna-11 must independently reproduce or challenge it."
    - "The exact current worktree is dirty; unrelated user changes must be preserved."
  unresolved:
    - "Luna-7 must repair or explicitly resolve the two timestamp-ordering defects before the gate can pass."
    - "Historical finding superseded by the owner-selected Luna-13A Model A implementation: reward identity is now explicit and duplicate delivery is bounded retry-idempotent within each ledger retention window."
  recommended_next_agent:
    - "Luna-11: execute the attack matrix and complete this handoff with evidence."
    - "Luna-0: review the completed Luna-11 handoff and gate later phases only after unresolved findings are cleared."

## Outcome and owned scope

Luna-11 actively falsified the integrated Luna-1 through Luna-8
architecture. It owns adversarial tests, code-path inspection, minimal
reproducers, and evidence reporting only. It did not patch production defects
or authorize Luna-9, Luna-10, the real dataset benchmark, or hardware work.

## Findings and classification

1. **Production defect, Luna-7 owner:** `StreamingCharacterClassifier.ingest_event()`
  commits `_last_timestamp` before validating the event kind. A rejected event
  at timestamp 1.0 poisons a legal retry at timestamp 0.5. This is covered by
  `test_rejected_classifier_event_can_be_retried_without_poisoning_order` and
  remains an unresolved causality/retry failure.
2. **Production defect, Luna-7 owner:** the public `finalize_character()` path
  emits a result at timestamp 10.0 without committing that timestamp. A later
  `START_CHARACTER` at timestamp 5.0 is then accepted. This is covered by
  `test_direct_finalization_rejects_earlier_next_character` and remains an
  unresolved local-time ordering failure.
3. **Historical finding, resolved by Luna-13A:** at this revision duplicate
  `RewardMessage` delivery cumulatively applied credit because neither message
  type carried a delivery identity. Luna-13A now adds explicit stable message
  identity and bounded retry-idempotent retention. The original observation is
  preserved as historical evidence; its former production behavior is no
  longer the current contract.

All other focused attacks passed: END_STROKE did not finalize; finalization was
single-shot; delayed credit retained the old character identity; classifier
instances were isolated; fan-out admission was atomic; positive propagation
was queued; batched and eventwise queue delivery matched; long classifier and
energy workloads remained bounded; and read-only evidence inspection was
side-effect free.

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
| Baseline revision and environment | `af5575ce0a629f101486bf36d930218eecdef77b`, Windows PowerShell, Python 3.10.8 | recorded | Existing unrelated worktree item: `.github/agents/luna-11.agent.md` untracked and preserved |
| `python -m pytest -q tests/test_luna11_adversarial.py` | Same revision/environment; deterministic fixtures | 8 passed, 2 strict xfailed | 10 focused tests; xfails are the two Luna-7 production reproducers |
| `python -m pytest -q` | Same revision/environment | 84 passed, 2 strict xfailed | Full regression including focused adversarial tests |
| `python -m compileall -q tpcn tests` | Same revision/environment | passed | No compilation output/errors |
| Workspace diagnostics | Touched test and `tpcn` paths | no errors | `get_errors` result |
| `git diff --check` | Same worktree | passed | No whitespace errors |

## Completion gate

Luna-11 is **blocked**: two unresolved Luna-7 production defects affect causal
timestamp ordering, and duplicate reward idempotency is an unresolved
contract question. The remaining areas are classified below and have exact
focused evidence. Luna-0 must route the production repairs to Luna-7 and
resolve the reward identity policy before promotion.

| Area | Result | Classification |
|---|---|---|
| Causality and character boundaries | failed | Luna-7 timestamp defects; END_STROKE and one-shot finalization otherwise passed |
| Label isolation | passed | Existing and adversarial label-free paths showed no leakage |
| Finite propagation/connectivity | passed | Positive delay, bounded fan-out, atomic capacity handling |
| Hidden global clock/state | passed | No core wall-clock or mutable global state found; legacy timing is outside core |
| Independent instances | passed | Interleaving did not cross-contaminate state |
| Delayed credit | passed with ambiguity | Old identity preserved; duplicate delivery policy undocumented |
| Energy/utility accounting | passed for bounded local accounting | Saturation and read-only behavior checked; duplicate accounting policy remains unspecified |
| Bounded state | passed | Long classifier and energy workload stayed within declared bounds |
| Deterministic replay | passed | Existing replay plus deterministic batch/eventwise order |
| Batching equivalence | passed | Queue batching matched event-at-a-time delivery |
| Dataset benchmark and hardware acceptance | not applicable | Explicitly deferred by workflow |

## Reproduction and rollback

Run from the recorded baseline/worktree with unrelated changes preserved.
Do not create branches or alter architecture. If a production repair is
needed, return ownership to the relevant Luna and retain a minimal reproducer.

## Next assignment

After a completed, passing Luna-11 handoff, return control to Luna-0. No later
experimental, benchmark, or hardware role is authorized by this dispatch.
