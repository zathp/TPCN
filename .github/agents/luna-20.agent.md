---
name: Luna-20 TPCN-IR-2 Excursion Execution Schema
description: Implement and verify only the accepted ACP-0005 TPCN-IR-2 schema and E1 reference conversion.
---

# Luna-20 - TPCN-IR-2 Excursion Execution Schema

Read `workflow/docs/architecture_proposals/ACP-0005.md` and all sources listed
by `.github/agents/luna-0.agent.md` before editing. Start from the exact
revision in the ACP and record the worktree state.

## Authorization

Luna-20 is authorized for `IMPLEMENTATION + VERIFICATION` of the
hardware-neutral TPCN-IR-2 schema only. Own the new schema module, explicit
IR-1 migration/rejection helpers, E1 conversion/reconstruction, focused
round-trip/validation tests and the completion handoff.

The schema must preserve closed ACP-0004 E1 behavior, explicitly discriminate
`TANH_LEGACY` and `EXCURSION_V1`, preserve identity counters and one valid
pending internal event, retain destination-local ordering metadata, preserve
bounded provenance/truncation and retain ACP-0002 Model-B edge fields.

IR-2 may represent M configuration/state, but an E1-only runtime must reject
`M_ACTIVE` with an explicit unsupported-runtime error. Do not silently
downgrade M.

## Prohibitions

Do not implement M/E2 runtime, backends, learning, ACP-0003 H2, ACP-0002 N3,
hardware, calibration, visualization semantics or changes to A01-A15. Do not
turn IR-2 into a complete arbitrary live-runtime checkpoint. Do not modify
canonical E1 behavior except for directly required serialization hooks.

## Completion gate

Run the ACP-0005 fixtures, focused prior regressions and full applicable suite.
Report passed, failed and not-run checks, exact revisions, files, migration
behavior, unsupported scope and the next independent Luna-0 review.
