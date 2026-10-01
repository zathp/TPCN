---
name: Luna-15 ACP-0002 Edge/Neuron Data Model and Compatibility
description: Implement only ACP-0002 Stage N1 edge/neuron data model and compatibility representation.
---

# Luna-15 - ACP-0002 Edge/Neuron Data Model and Compatibility

Read `workflow/ARCHITECTURE_CONTRACT.md`, `workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/architecture_proposals/ACP-0002.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, and this contract before
editing. Record the exact starting revision, branch and worktree state.
Preserve unrelated changes. ACP-0002 is **Accepted for staged implementation**;
this contract authorizes only Stage N1.

## Authorization and ownership

Own only the edge/neuron data model, validation, compatibility representation,
focused analytic/regression tests, relevant documentation and the Luna-15
handoff. The exact authorized scope is:

- Add explicit edge-owned `edge_weight` / `w_ij` in `[-2, 2]`.
- Add explicit edge-owned `divider_strength` / `d_ij` in `[0, 1]`.
- Add explicit edge-owned `reference` / `r_ij` in `[-1, 1]`.
- Preserve the existing positive finite edge propagation delay `tau_ij`.
- Add or represent neuron-owned `neuron_gain` / `g_j` in `[0, 2]`.
- Preserve legacy constructor compatibility, including a deliberate mapping or
  alias for the existing input-gain API and an explicit legacy identity
  representation where raw-payload comparisons require it.
- Preserve structural-plasticity compatibility: topology rebuilds, existing
  edge creation and bounded capacity checks must be able to carry or initialize
  the complete N1 record without enabling plasticity.
- Preserve deterministic representation and replay: finite validation,
  stable serialization/inspection and no dependence on unordered iteration.
- Preserve observer/instrumentation compatibility and observer non-interference.
- Preserve existing event identity, timestamps, sequence ordering, positive
  delays and routed payload semantics. N1 must not change the routed payload.

The accepted future Model-B equation is:

```text
v_ij = d_ij * tanh(w_ij * a_i) + (1 - d_ij) * r_ij
```

N1 MUST NOT compute, activate, route or otherwise introduce this transfer
function. N1 only represents validated state and compatibility; transfer
execution is a later separately authorized stage.

## Required validation

Add focused analytic and regression tests proving N1 is behaviorally
compatible. At minimum verify:

- accepted bounds and rejection of non-finite/out-of-range values;
- existing positive finite propagation-delay validation;
- legacy constructors and identity-adapter behavior;
- structural-plasticity topology creation/rebuild compatibility without
  changing admission, pruning or maturation behavior;
- deterministic representation and replay across repeated runs;
- observer/instrumentation compatibility and no observer effect;
- routed payload, event identity, timestamps, sequence ordering and delay
  behavior remain unchanged;
- no Model-B transfer activation occurs in N1.

Run the focused tests, relevant regression tests and `git diff --check`. Record
passed, failed and not-run checks with exact commands and revision in the
handoff. Return to Luna-0 for independent review after N1 implementation.
N1 completion does **not** automatically authorize N2.

## Explicit prohibitions

Luna-15 MUST NOT:

- change N2 propagation or transfer execution;
- activate the Model-B equation in any route or event path;
- add adaptive edge learning;
- add temporary or probationary connections;
- add edge maturation or new utility-learning mechanisms;
- add local time-series mini-neural-networks;
- change A01-A15 or amend the architecture contract;
- authorize, create, dispatch or imply authorization of Luna-13G;
- reinterpret or reopen the closed Luna-13F result;
- claim hardware equivalence or implement FPGA/FPAA behavior;
- treat N1 completion as authorization for N2 or any later ACP-0002 stage.

## Completion gate

The terminal result must distinguish representation compatibility from transfer
semantics. Report exact files changed, schema/default decisions, bounds,
legacy mapping, structural/observer compatibility, deterministic replay and
payload-preservation evidence. The handoff must state `OBSERVED`, `INFERRED`
and `HYPOTHESIZED` evidence where applicable, return control to Luna-0, and
leave ACP-0002 **Accepted for staged implementation**, A01-A15 unchanged,
Luna-13F **CLOSED**, Luna-13G unauthorized, and N2 unauthorized.
