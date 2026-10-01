---
name: Luna-16 ACP-0002 N2 Static Model-B Edge Transfer
description: Implement and verify only the static ACP-0002 Model-B edge transfer after the controlled canonical cutover.
---

# Luna-16 - ACP-0002 N2 Static Model-B Edge Transfer

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/architecture_proposals/ACP-0002.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, and this contract before
editing. Record the exact starting revision, branch and worktree state.
Luna-0 has selected **CONTROLLED CANONICAL CUTOVER** and authorizes this
contract only. Do not execute N2 while creating or reviewing this contract.

## Authorization and migration boundary

N1 is the final representation-compatible version of legacy raw-payload
execution. N2 intentionally activates Model B as the new canonical execution
revision. With N1 defaults `w=1`, `d=1`, `r=0`, Model B yields `tanh(a)`, not
raw `a`; do not claim signal identity and do not bypass the nonlinearity for
legacy-looking edges. Historical committed experiments remain reproducible
under their original revisions and are not reinterpreted as N2 results. New
N2-and-later artifacts must identify the architecture revision. Do not add a
per-edge legacy/model-B mode to the canonical architecture.

## Exact authorized computation

For an emission from source `i` over edge `i -> j`, use immutable bounded edge
parameters and existing event semantics:

```text
z_ij = tanh(w_ij * a_i)
v_ij = d_ij * z_ij + (1 - d_ij) * r_ij
```

Schedule `v_ij` after the existing positive finite delay `tau_ij`. At arrival:
advance destination local time, apply existing elapsed-time decay to `s_j`,
integrate and clip the contribution, apply neuron-owned gain `g_j`, apply the
ACP-approved fixed neuron nonlinearity, and emit later events normally. There
is no global neural timestep, synchronous matrix sum, or inline destination
mutation. Follow ACP-0002 if its exact neuron equation differs from a prompt
example.

The edge parameters are static in N2. Newly grown edges retain the currently
approved compatibility defaults (`w=1`, `d=1`, `r=0`) unless ACP-0002 says
otherwise; candidate association scores must never become edge parameters.
Structural growth remains bounded and atomic.

## Required analytic and integration evidence

Add focused tests for:

- `d=1`, `d=0`, `r=0`, and `w=0` endpoint/reference behavior;
- positive and negative `w` and `a`;
- `r=-1,0,+1` and `d=0.25,0.5,0.75`;
- `w=-2,0,+2` and independent effects of every edge dimension;
- two-edge fan-in comparisons for differing `w`, `d` and `r`;
- deterministic equal-time fan-in without replacing event processing with a sum;
- unequal delays with zero pre-arrival influence and actual causal timestamps;
- bounded recurrent motifs under extreme allowed values, finite state and
  activation, explicit event/queue budgets, and no NaN/inf or unbounded queue;
- deterministic replay and observer ON/OFF computational equality;
- label isolation, future-information isolation, topology capacity,
  structural-plasticity defaults and reward identity/idempotency where touched.

Create a new committed analytic Model-B baseline. Separate invariants that must
remain identical (causality, timestamps/order, positive delays, queue and
structural capacity, label isolation, reward identity, bounded execution and
observer behavior) from values expected to change (payload magnitude, state,
activation, prediction/error traces and downstream task metrics). Accuracy
improvement is not required.

## TPCV and resource boundary

TPCV-1 currently omits transfer fields as an explicit version-1 observational
boundary. Determine whether active transfer-state export needs a new format or
other governance decision. Do not silently claim that TPCV-1 preserves active
edge parameters. If the existing contract does not authorize a version change,
stop that part and return a governance dependency to Luna-0.

Record the additional bounded static operations per routed edge: multiply for
`w*a`, fixed `tanh`, divider interpolation and bounded arithmetic. Use the
existing activity-cost-proxy/resource interface only where its semantics permit;
do not claim calibrated joules or hardware equivalence.

## Explicit prohibitions

Luna-16 MUST NOT implement or authorize:

- learning or adaptation of `w`, `d` or `r`;
- temporary, probationary or maturing edges;
- new structural utility prediction, reward-driven edge updates or pruning;
- time-series mini-networks or classifier redesign;
- hardware-specific voltage semantics, FPGA/FPAA acceptance or a global clock;
- changes to A01-A15, retrospective historical artifact claims or Luna-13F;
- Luna-13G or N3/later ACP-0002 stages.

Preserve A01-A15, predictive/error interfaces, local learning boundaries,
delayed credit, bounded topology/dynamics, hardware independence, observer
non-interference and label/future isolation.

## Completion handoff

Use `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md` and return to Luna-0.
Report the starting and implementation revisions, migration strategy, exact
edge and neuron equations, all analytic cases, divider endpoints, signed
weight/activation behavior, independent reference behavior, equal-time and
unequal-delay results, recurrence/budget results, structural-plasticity and
observer invariance, TPCV/versioning result, focused and relevant regression
checks, full CPU suite, A01-A15 status, ACP-0002 status, Luna-13F historical
status and Luna-13G status. Separate OBSERVED, INFERRED and HYPOTHESIZED
claims and mark every unrun check explicitly. Successful N2 does not
authorize any later stage.
