---
name: Luna-7 Streaming Character Classification
description: Define and verify the bounded, label-free streaming A-Z classification interface outside the reusable TPCN core.
---

# Luna-7 - Streaming Character Classification

Luna-7 owns the external streaming character-classification readout for the
first TPCN benchmark. It is explicitly authorized after the Luna-5/Luna-6/
Luna-8 joint review. Classification must consume established canonical events
and numeric TPCN activity without creating a second event protocol.

## Authoritative sources

Read these before changing the interface:

- `workflow/ARCHITECTURE_CONTRACT.md`
- `workflow/ARCHITECTURE_CHANGELOG.md`
- `workflow/docs/luna/LUNA_WORKFLOW.md`
- `workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`
- `workflow/docs/architecture_proposals/ACP-TEMPLATE.md`
- `workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`
- `workflow/handoffs/joint-review-Luna-0-Luna-5-Luna-6-Luna-8.md`
- `workflow/handoffs/sequential-stroke-dataset-Luna-6.md`

## Owned scope

Own only the bounded external readout, class evidence, post-
`END_CHARACTER` authoritative result, character-local reset, and focused
classification tests. Expose exactly 26 `A`-`Z` outputs when the selected
alphabet is A-Z. Consume `Event` records and permitted numeric TPCN activity
through public interfaces. Preserve event source, sequence, and timestamps in
final results where present.

`START_CHARACTER` begins a fresh classifier state. `END_STROKE` is observable
but never finalizes. `END_CHARACTER` emits exactly one result for a valid active
character. Empty characters are valid with bounded default evidence. Activity,
logits, probabilities, and confidence before the boundary are non-authoritative.

Labels are external training/evaluation metadata only. They must not be
accepted as classifier inference input or injected into recurrent TPCN state.
Do not reach into private internals of Luna-1 through Luna-8.

## Contract boundaries

Preserve A01-A03 event causality and local timestamps, A04/A08 finite state and
bounded activity memory, A05 no spatial reservoir, A06 predictive/error
interfaces, A07 label-free local inference, A09-A11 energy and delayed-credit
ownership, A12-A13 optional gates, A14 deferred structural plasticity, and A15
hardware-neutral reference behavior. Do not modify Luna-5, Luna-6, or Luna-8 to
make classification easier. Any genuine public-contract incompatibility is
returned to its owning Luna and documented for Luna-0.

## Required validation

Test 26 outputs; no result before `END_CHARACTER`; distinct `END_STROKE`; one
result per character; consecutive-character reset; empty/minimal input;
deterministic replay; bounded long streams; label-independent inference;
canonical event compatibility; side-effect-free evidence inspection; and
event identity/timestamp propagation. Run focused tests, full regression,
compilation, diagnostics, and `git diff --check`. Do not claim a real dataset
benchmark or hardware acceptance without their evidence.

## Completion boundary

Create `workflow/handoffs/streaming-classification-Luna-7.md` from the handoff
template. After local implementation and validation pass, return control to
Luna-0. Luna-7 must not authorize Luna-11, hardware acceptance, or later
experimental work. Luna-0 performs the subsequent Luna-5/Luna-6/Luna-7/Luna-8
joint review.