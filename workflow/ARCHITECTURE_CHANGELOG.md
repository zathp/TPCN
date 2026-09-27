# Architecture Changelog

## 1.0 — 2026-09-26

Established the documented candidate contract from the source conversation and current owner request.

- Event-driven operation with local time, finite propagation, bounded topology and bounded dynamics.
- Spatial reservoir deprecated from core; legacy comparisons remain separate.
- Predictive coding, explicit error events, local learning and delayed credit preserved.
- Local energy accounting is reward-adjusted: minimize unrewarded expenditure.
- Exactly ten pathways and explicit gating are soft/experimental.
- Sequential letter strokes are the first integration target.
- FPGA/VHDL, FPAA and hybrid realizations remain eventual branches.
- Added role workflow, acceptance criteria, ACP and handoff templates.

This entry records documentation establishment, not completed implementation or hardware validation.

For later changes record date, contract version, accepted ACP, decision owner, clauses affected, evidence, compatibility and migration/rollback implications.

## Workflow observability track — 2026-09-27

Added a distinct downstream-only visualization and verification track:

- Luna-12: canonical visualization contract and CPU reference exporter/parser.
- Luna-13: GPU-compatible exporter using the Luna-12 format, gated on Luna-12.
- Luna-14: ModelSim/FPGA trace bridge and Terasic DE1-SoC visualization foundation, gated on Luna-12.
- Luna-12A: optional CPU training and TPCV-1 replay integration after Luna-12, using the deterministic Luna-9 synthetic path; not a prerequisite for Luna-13 or Luna-14.

Visualization is not part of the canonical TPCN computational architecture. It is an observability and verification facility used to inspect structure formation and activity across CPU, GPU, simulation, and FPGA implementations. No return path into the TPCN computational datapath is permitted. The former FPGA/VHDL, FPAA, and hardware-equivalence milestone contracts were preserved as Luna-15, Luna-16, and Luna-17 to resolve the existing numbering conflict. This is a workflow change, not a contract change or implementation result; Luna-12 is the only new milestone eligible for explicit authorization, and Luna-13/Luna-14 remain blocked until its gate passes.

## Luna-12B authorization — 2026-09-27

Authorized Luna-12B, Persistent Topology and Structural Plasticity Visualization Integration, after the owner-supplied Luna-12A completion evidence: full suite 130 passed with 1 skipped, focused Luna-12A tests 3 passed, compilation and diagnostics passed, `git diff --check` passed, and a three-snapshot smoke run replayed deterministically.

- Luna-12B integrates one persistent bounded Luna-4 topology with the validated Luna-10 structural-plasticity API in the deterministic Luna-9 CPU path.
- It is an integration/observability milestone, not a canonical architecture change; A01-A15 remain unchanged and no ACP is required.
- Luna-12B is not a prerequisite for independently authorized Luna-13 or Luna-14.
- Real-dataset benchmarking and Luna-15/Luna-16/Luna-17 remain separately gated and are not authorized by this entry.

