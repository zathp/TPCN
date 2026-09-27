---
name: Luna-12F Readout Learning and Class-Separation Verification
description: Verify external readout class starvation, correct bounded readout learning, and measure class separation without changing label-free neural computation.
---

# Luna-12F - Readout Learning and Class-Separation Verification

Read `workflow/ARCHITECTURE_CONTRACT.md`,
`workflow/ARCHITECTURE_CHANGELOG.md`,
`workflow/docs/luna/LUNA_WORKFLOW.md`,
`workflow/docs/architecture/ACCEPTANCE_CRITERIA.md`,
`workflow/docs/luna/AGENT_HANDOFF_TEMPLATE.md`, and
`workflow/handoffs/computational-topology-integration-causal-learning-Luna-12E.md`
before editing. Record the exact baseline revision and preserve unrelated
worktree changes.

## Authorization and ownership

Luna-12E has been accepted by Luna-0 for the computational-topology gate.
Luna-0 authorizes this milestone for the deterministic synthetic A/Z workload
and the external supervised readout path only. Own the readout investigation,
smallest compatible readout correction, focused tests, diagnostics, relevant
replay-side metrics, and
`workflow/handoffs/readout-learning-class-separation-Luna-12F.md`.

Do not benchmark a real dataset, authorize Luna-15/Luna-16/Luna-17, redesign
the architecture-wide classifier, or change Luna-13/Luna-14 dependencies.

## Architectural boundary

The neural computation must complete before external supervised readout
selection and update. Labels may be used for external target comparison,
readout learning, reward/evaluation, and reporting only. They must not enter
canonical events, neuron state, predictor state, topology mutation evidence,
structural-plasticity decisions, event routing, or energy computation.

Preserve the Luna-12E persistent bounded topology and causal event path. Do not
create a second topology, alter TPCV-1 incompatibly, add a global neural clock,
or replace the network with a large unrelated classifier. Readout state must be
bounded by `max_classes`, deterministic, resettable, and external to the
neural core.

## Required work

1. Reproduce the current positive-reward-gated behavior with a deterministic
   A/Z fixture. Record initial prediction, reward, update decision, and
   prototype/readout state. Test explicitly whether an initially misclassified
   Z can create or update a Z representation. Treat the `reward > 0.0` gate as
   an observed condition; confirm or reject starvation with the fixture.
2. Expose the pre-readout network feature for every example, with example ID,
   evaluation-only true label, predicted class, confidence, winner margin, and
   distance/score to every available class representation. Determine whether
   A/Z features are separable before readout selection and whether readout
   selection discards useful differences.
3. Apply the smallest compatible correction, such as bounded supervised
   prototype creation/update or class-local centroid statistics. Separate
   supervised target acquisition from reward-modulated refinement. Report an
   explicit diagnostic when a declared training class has no representation.
4. Compare the current gated readout and corrected readout on identical seeds
   and synthetic workloads. Report accuracy, per-class accuracy, confusion
   matrix, confidence, margin, prediction loss, reward, energy, utility,
   topology metrics, readout update count, prototype count, and starvation
   count. Do not claim the readout improves the neural predictor itself.
5. After correction, compare fixed topology, structural plasticity, and a
   useful no-learning control. Topology need not improve classification; report
   positive, neutral, and negative outcomes without forcing a benefit claim.
6. Expose compatible class-separation metrics to replay/analysis where
   possible. Keep observation downstream-only and do not modify TPCV-1
   incompatibly without Luna-0 review.

## Required tests and validation

Add focused tests for:

- both classes acquiring readout state;
- an initially misclassified Z becoming correct after supervised readout updates;
- removing positive-reward-only gating from class creation without label leakage;
- identical neural event traces for identical inputs despite different external labels;
- labels affecting only external readout learning and evaluation;
- the `max_classes` bound;
- deterministic same-seed readout state.

Run the Luna-12F focused tests, Luna-12E causal integration tests, experiment
and classifier/readout tests, structural-plasticity tests, relevant
visualization/analysis tests, full `pytest`, `python -m compileall -q tpcn
tests train_cpu_visualization.py`, workspace diagnostics, and `git diff
--check`. Record passed, failed, and not-run checks with exact commands and
revision in the handoff. Return control to Luna-0; do not claim integration
readiness beyond the evidence actually collected.
