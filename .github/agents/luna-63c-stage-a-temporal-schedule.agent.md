---
name: "Luna-63C Stage-A Temporal Schedule Completion"
description: "Complete blocked Stage-A event-time mappings from owner-frozen numeric inputs; no fixture change, Lane S/N5, or Stage-B execution."
tools: [read, search, edit]
agents: []
---

# Luna-63C Stage-A temporal schedule completion

**CONTRACT PREPARED / EXECUTION NOT AUTHORIZED.** This is a bounded,
unnumbered assignment under the existing Luna-63C certificate chain. The
published T inventory and schedule already reconcile all 191 event IDs and
identify the nine certified rows; do not treat the parent's distinct
untracked T copy as authority. This contract does not assign a new Luna
identifier or itself authorize Lane T. Start only after the project owner
freezes the missing numeric schedule inputs and separately dispatches this
completion.

## Baseline and authoritative inputs

Before work, fetch and verify the exact owner-approved baseline and refs:

- C0-C7 fixture publication: `583148e2812b93d519a3dc2821944d08446497b7`
- Fixture freeze: `experiments/luna63c/fixture-freeze/fixtures.json`
- Reviewed design: `3e7d31b9a527e908b21abee3766906084e7cd082`
- N4 schema: `9cc92adb56e388d8675d538410b319fd8d8841a5`
- Arithmetic governance: `87179ba2f5da13da7bc70727e72c000de924ed80`
- W: `17907c67d52cc338249b66f28c3179cd97572c6e`
- T: `0a8c34b7e6febf681917d915082a8559eea998f7`
- E: `651f18fdf3c7ae8e32cd210ebc68527f86531e32`
- Owner-approved supplemental numeric schedule hash (must be supplied before
  execution). The existing published event-ID crosswalk is pinned by the T
  commit and must be retained, not reconstructed.

The listed revisions are claims until verified from the remote and their
manifests. If any pin conflicts, stop and report the exact mismatch.

## Affected clauses and interface

Preserve A01-A03 event-driven/local-time/causal behavior and A08 bounded
lifecycle/event state. Use the already reviewed C0-C7 semantics, the
owner-clarified C2/A=1 checkpoints and strict `< theta/4` comparison, and
the owner-clarified C7 reset/output persistence, represented expiry
coalescence and strict mathematical re-arm-before-quiet behavior.

No global neural timestep, periodic external input, synthetic event, new
packet type, changed field/parameter/threshold, changed clock domain,
expanded event identity, resource increase, or inferred queue-order rule is
allowed.

## Owned files

Only edit, after explicit dispatch:

- `experiments/luna63c/certificate/lane-t/`
- `workflow/handoffs/luna63c-stage-a-lane-t-correction-<owner-approved-id>.md`

Do not edit the published fixture, design, N4 schema, W/E artifacts,
production/runtime code, core contract, ACP, or unrelated handoffs.
If the owner-approved schedule needs governance integration, ask Luna-0 to
coordinate separately; do not edit common workflow files from this
implementation assignment.

## Required inputs and authority

The owner must freeze the exact numeric schedule bytes before work starts.
Use exact external binary64 bit patterns and delivery ordinals for the
already-published identities. The owner clarifications already govern
reset-after-processed-output, expiry equality at the represented binary64
timestamp, and analytic `t_rearm < t_quiet`; do not reopen those semantic
decisions or invent a new `t_emit` policy. Any bounded envelope must state
its endpoints and include a sound proof over the full domain. Keep exact-real
event order distinct from binary64 ceiling equality. Existing precedence is
authoritative; do not resolve ties by insertion/allocation order.

## Acceptance criteria

1. Verify the published T inventory and schedule reconcile the same 191
   unique semantic event IDs exactly once, including the 119 expanded C7
   identities; retain the separate 15 observation-only rows outside the
   event ledger.
2. Preserve the nine already-certified semantic IDs, exact values, ceilings,
   ordinals and W evidence. Preserve the other 182 IDs with their existing
   exact blocker reasons; do not recast a blocked row as certified merely
   because its identity is known.
3. Do not invent missing packet times, origins, timer identities, or
   ordinals. Fail closed when enclosure ceilings differ, strict-future or
   domain checks fail, a causal order is unresolved, or evidence caps are
   exhausted.
4. Preserve N4 arithmetic: MPFR C API 4.2.2/GMP 6.3.0, directed outward
   intervals, exact dyadic active-time sums, 256/512-bit agreement and only
   authorized 1024-bit escalation; at most 128 root bisections; no host
   `libm` for scientific transcendental reference values.
5. Keep numerical witness rows, exact schedule fixtures, bounded-envelope
   proofs and property tests distinct. Do not claim finite tests prove a
   universal timing property.
6. Validate fixture/source raw identities against manifests; verify
   deterministic regeneration; test exact represented-time ties, strict
   future, near-clock-domain boundaries and all owner-approved coalescence
   cases using the frozen inputs.
7. Preserve C0-C7 fixture bytes and resource accounting
   `16+1+24+1=42`. The original fixture may not be expanded.
8. Publish a new immutable Lane T correction result and handoff. Obtain
   independent E re-audit and read-only Luna-0 review against exact hashes.
   A T correction alone does not close N1, N3 or N4.

## Stop conditions and prohibited work

Stop if any required owner-frozen numeric input is missing or conflicts with
existing authority; any schedule requires changing a fixture identity or
scientific semantics; the published event-ID crosswalk fails verification;
or any N4 obligation remains unresolved at its authorized cap.

This contract does **not** authorize Lane S/N5, N6, Stage B, a solver/runtime
implementation, C0-C7 scientific execution, a mechanism experiment, ACP
adoption, production/default edits, hardware claims, or architecture
promotion. Each requires its own existing gate and explicit authorization.

## Independent handoff

Use `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`. Report verified refs,
all artifact hashes, verification of the published per-ID reconciliation,
preserved certified rows, blocked rows, exact commands/tests and their
outcomes, unrun checks, limitations, independent E/Luna-0 review status, and
the next gate.
