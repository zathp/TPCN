---
name: Luna-24 ACP-0006 IR-2 Quiescent Provenance Boundary Correction
description: Reject residual assigned provenance and sticky provenance truncation at integrated IR-2 startup without changing schema revision 1.
---

# Luna-24 - ACP-0006 IR-2 Quiescent Provenance Boundary Correction

## Authorization and baseline

Luna-24 is authorized for **IMPLEMENTATION + VERIFICATION** of the remaining
integrated IR-2 quiescent-startup defect independently reproduced in the
Luna-0 second review of Luna-22. Start from the published Luna-0 review
revision recorded in `workflow/handoffs/luna-0-second-independent-review-ACP-0006-Luna-22-20261003.md`,
then synchronize to the exact authorized repository tip before editing.
Record branch and worktree state.

This is a bounded experiment-adapter correction under accepted ACP-0006.
It does not authorize IR-2 schema changes, E2 converter changes or a live
network checkpoint. If rejection of residual provenance conflicts with the
accepted boundary, stop and return the evidence to Luna-0.

## Observed defect

`ExcursionCharacterRuntime.from_quiescent_ir2()` rejects nonzero `x` and
unassigned provenance count/truncation, but currently accepts both:

- a non-empty assigned `IR2Neuron.provenance` tuple when mode is N and x is
  exactly zero;
- `provenance_truncated=True` when mode is N and x is exactly zero.

The accepted ACP-0006 startup boundary requires no residual provenance and
permits restoration only of approved counters/configuration. The existing
implementation silently carries these residual fields through integrated
reconstruction.

## Bounded file ownership

Own only:

- `tpcn/experiment_excursion_runtime.py`, limited to
  `from_quiescent_ir2()` boundary validation;
- `tests/test_excursion_integration.py` for focused startup-boundary cases;
- `workflow/handoffs/luna-24-ir2-quiescent-provenance-20261003.md`.

Do not edit `tpcn/ir2.py`, E1/E2 neuron conversion, schema revision 1,
Luna-22 experiment selection, visualization/research consumers, dataset code,
or workflow/changelog files.

## Hypothesis and counter-hypothesis

- **Hypothesis:** Integrated startup can reject assigned residual provenance
  and sticky provenance truncation while preserving valid quiescent startup,
  permitted identity high-water counters, and standalone E2 reference
  round trips.
- **Counter-hypothesis:** These fields are required at the integrated
  initialization boundary by the accepted ACP or a valid restart use case.

## Required behavior and controls

- Accept a uniformly EXCURSION_V1, mode-N, exact `x == 0.0` network with no
  pending event, active episode/lineage, provenance entries, provenance
  truncation or unassigned provenance.
- Preserve only the explicitly permitted static configuration and identity
  high-water counters.
- Reject nonzero positive, negative and tiny finite `x` without epsilon
  normalization.
- Independently reject positive `unassigned_provenance_count`,
  `unassigned_provenance_truncated=True`, non-empty assigned provenance, and
  `provenance_truncated=True`.
- Continue rejecting S_PENDING, active S_RETURN, M_ACTIVE, pending live state,
  mixed dynamics models and non-empty shared-queue state.
- Preserve standalone active/pending E2 IR-2 round trips; do not change IR-2
  schema revision 1 or the standalone E2 adapter.

## Interfaces, information and architecture

- The adapter may validate only serialized local neuron state, model tags,
  queue/topology records and declared startup configuration.
- No labels, task metrics, future events or global neural state enter
  computation.
- A01-A08 and A15 are preserved; startup is an integration boundary, not a
  new canonical neuron rule.
- No ACP is required for enforcing the accepted ACP-0006 boundary. If schema
  modification or a broader checkpoint is required, stop and return to
  Luna-0.
- No hardware equivalence is claimed.

## Acceptance and validation

Required evidence:

1. Parameterized integrated-startup tests reject each residual-provenance
   condition independently and exercise valid high-water counters.
2. Positive, negative and smallest finite nonzero x remain rejected exactly.
3. Clean quiescent reconstruction and deterministic continuation remain
   passing.
4. S_PENDING, S_RETURN, M_ACTIVE, mixed-model and pending-event cases remain
   explicitly rejected.
5. Standalone E2 active/pending IR-2 round trips and schema revision 1 tests
   remain passing.
6. Run the focused Luna-22 tests, prescribed regression set and full suite;
   report remaining downstream failures rather than changing those consumers.
7. Report `compileall`, relevant diagnostics where available, and
   `git diff --check`.

Separate passed, failed, not-run and not-applicable checks in the handoff.

## Explicit exclusions

No IR-2 schema revision, new live-network checkpoint, E1/E2 neuron state
change, Model-B change, prediction/credit/reward redesign, structural
plasticity, dataset work, visualization, legacy-consumer migration, A01-A15
amendment, N3, H2, backend, GPU, FPGA, FPAA, IR-3, calibration or hardware
equivalence.

## Completion and stop boundary

Publish the required handoff with exact baseline/result revisions, files,
valid/invalid startup matrix, standalone round-trip evidence, tests and
remaining limitations. Return the evidence to Luna-0 for independent
verification. Luna-24 must stop after this boundary correction and must not
execute downstream migration or claim Luna-22 closure.
