---
name: Luna-19 ACP-0004 E1 Canonical Single-Excursion Neuron
description: Implement and verify only the authorized ACP-0004 E1 software-reference stage.
---

# Luna-19 - ACP-0004 E1 Canonical Single-Excursion Neuron

Read these sources before editing:

- `workflow/ARCHITECTURE_CONTRACT.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`
- `workflow/docs/architecture_proposals/ACP-0003.md`
- `workflow/docs/architecture_proposals/ACP-0004.md`
- `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`
- `.github/agents/luna-0.agent.md`
- this contract

ACP-0004 is **Accepted for staged implementation**. This contract authorizes
only E1, the static leaky accumulator and single-excursion software reference.
Record the exact starting revision, branch and worktree state before editing.
Preserve unrelated changes and return to Luna-0 for independent review.

## Authorization and ownership

Own only the minimal canonical/reference neuron implementation, its focused
tests, and the Luna-19 completion handoff. Confirm exact file ownership with
Luna-0 if the existing module boundary is unclear. Do not reorganize the
repository or implement a successor architecture.

E1 must implement:

- bounded signed `x` and local last-update timestamp;
- explicit modes `N`, `S_PENDING` and `S_RETURN`;
- local exponential decay before each ordered contribution;
- Model-B payload source `a_i = p_exc`;
- thresholds satisfying
  `0 < theta_R < theta_E <= theta_hold < theta_M <= X_max`;
- fixed positive finite ordinary emission delay `Delta_t_E`;
- exact ordinary amplitude map using bounded `m_peak`;
- admission-time captured polarity;
- exactly one digital event per canonical excursion;
- analytic finite re-arm at `theta_R`;
- deterministic external-before-internal equal-time processing;
- bounded generation-token cancellation and stale-event no-op behavior;
- one valid pending internal event per neuron;
- bounded provenance with `P <= 64`, oldest eviction and
  `provenance_truncated`;
- unique event identity and bounded lineage;
- deterministic fixtures and replay.

The E1 implementation may expose the M transition boundary for testing, but it
must not implement the M generator or repeated excursions.

## Canonical E1 behavior

The persistent state is `x`, local timestamp and explicit mode. Bounded
bookkeeping includes pending event kind/time, ordinary episode and lineage
identity, captured polarity, `m_peak`, provenance and generation token. Do not
add persistent `y`.

For an arrival at `t_k`:

```text
x(t_k-) = x(t_(k-1)+) * exp(-lambda * (t_k - t_(k-1)))
x(t_k+) = clip[-X_max, X_max](x(t_k-) + v_ij(t_k))
```

In `N`, values below `theta_E` remain in `N`; values in
`[theta_E, theta_M)` enter `S_PENDING`; values at or above `theta_M` must be
reported as outside E1 scope rather than silently producing an ordinary
excursion.

Admission allocates an ordinary episode, captures `sign(x)`, initializes
`m_peak = abs(x)`, and schedules `S_EMIT` at `t_admit + Delta_t_E`.
External events before that internal event update `x`, provenance and
`m_peak`. If `abs(x) >= theta_M`, cancel the ordinary event through generation
invalidation and report/promote to the separately unauthorized M boundary.

At valid `S_EMIT`, emit one event with:

```text
A_exc = A_min + (A_max - A_min) *
        clip((m_peak - theta_E) / (theta_M - theta_E), 0, 1)
p_exc = captured_polarity * A_exc
```

Then enter `S_RETURN`. If `abs(x) <= theta_R`, enter `N`; otherwise schedule
`S_REARM` at:

```text
t_emit + ln(abs(x) / theta_R) / lambda
```

During `S_RETURN`, external input cancels and reschedules re-arm, retains the
updated state/provenance, and promotes to the unauthorized M boundary if
`abs(x) >= theta_M`. No second ordinary excursion may be emitted before `N`.
At valid `S_REARM`, enter `N` when `abs(x) <= theta_R`.

## Required tests

Add focused tests for:

1. irregular timestamps and local decay without a global timestep;
2. threshold equality at `theta_E` and strict re-arm at `theta_R`;
3. close contributions producing one excursion;
4. widely spaced contributions producing no excursion;
5. moderate overshoot producing at most one excursion;
6. admission-time polarity under later opposite-sign input;
7. exact amplitude map and saturation;
8. external-before-internal equal-time ordering;
9. cancellation, generation invalidation and stale-event no-op;
10. input during `S_RETURN` and finite analytic re-arm;
11. unique event identity and bounded lineage;
12. provenance overflow and explicit truncation;
13. deterministic replay and batched/unbatched equivalence;
14. bounded state and event-budget behavior.

Tests must not claim M behavior, IR-2 behavior, hardware equivalence or
learning evidence.

## Explicit prohibitions

Luna-19 MUST NOT implement or authorize:

- `M_ACTIVE`, M emissions, multi-excursion discharge or oscillator behavior;
- learning, edge learning, predictive-learning changes or reward changes;
- ACP-0002 N3 or later stages;
- TPCN-IR-2 or IR migration;
- GPU, FPGA, FPAA, CUDA, VHDL or hardware execution;
- approximation, calibration or cross-backend equivalence;
- Luna-13F reopening, Luna-13G or changes to A01-A15;
- a global timestep or hidden polling loop;
- labels, future inputs or global evaluation state in neuron computation.

## Completion and handoff gate

The handoff must report the starting and result revisions, exact files,
parameter configuration, state/mode behavior, timing and cancellation rules,
event/provenance bounds, focused tests, deterministic replay, unchanged
Model-B semantics, A01-A15, ACP-0004, H2, ACP-0002 N3, Luna-13F and Luna-13G.

A successful implementation may report:

`PASS - ACP-0004 E1 CANONICAL SINGLE-EXCURSION REFERENCE IMPLEMENTED`

but Luna-19 does not independently accept ACP-0004 or authorize M, IR-2,
backends or later stages. Return to Luna-0 for independent verification.
