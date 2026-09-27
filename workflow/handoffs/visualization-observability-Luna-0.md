# Luna-0 Visualization / Observability Workflow Handoff

```yaml
tpcn_handoff:
  agent: Luna-0 Architecture Guardian
  task_id: visualization-observability-workflow
  component: visualization milestone workflow and authorization gates
  status: complete
  luna_12_gate: PASSED
  luna_13_authorization: AUTHORIZED
  luna_14_authorization: AUTHORIZED
  contract_version: "1.0"
  branch: main
  base_revision: 1cf4065
  result_revision: uncommitted
  architecture_invariants_touched: [A01, A03, A04, A07, A08, A15]
  preserves:
    - canonical TPCN computational architecture and existing milestone contracts
    - Luna-9 and Luna-10 ownership and authorization boundaries
    - historical Luna-11 handoff and its original evidence
    - downstream-only visualization with no computational return path
  architecture_change: false
  proposal: null
  files_changed:
    - workflow/docs/luna/LUNA_WORKFLOW.md
    - workflow/README.md (existing worktree change reviewed)
    - workflow/docs/architecture/ACCEPTANCE_CRITERIA.md (existing worktree change reviewed)
    - workflow/ARCHITECTURE_CHANGELOG.md (existing worktree change reviewed)
    - workflow/docs/luna/VISUALIZATION_CONTRACT.md (existing worktree change reviewed)
    - .github/agents/luna-12.agent.md (existing worktree addition reviewed)
    - .github/agents/luna-13.agent.md (existing worktree addition reviewed)
    - .github/agents/luna-14.agent.md (existing worktree addition reviewed)
    - workflow/handoffs/visualization-contract-Luna-12.md (existing worktree addition reviewed)
    - workflow/handoffs/visualization-gpu-Luna-13.md (existing worktree addition reviewed)
    - workflow/handoffs/visualization-fpga-Luna-14.md (existing worktree addition reviewed)
    - workflow/handoffs/visualization-observability-Luna-0.md
  tests_added: []
  tests_passing:
    - `python -m pytest -q tests/test_visualization.py`: 13 passed
    - focused visualization, energy, and Luna-11 suite: 30 passed
    - affected former strict-xfail tests: 2 passed
    - `python -m pytest -q`: 118 passed, clean exit
    - `python -m compileall -q tpcn tests`: passed
    - git diff --check
    - milestone heading uniqueness check
  tests_failed: []
  tests_not_run:
    - repository-specific workflow lint: no workflow lint command was documented or found
    - GPU, ModelSim, FPGA, VGA, Ethernet, and hardware equivalence: outside this Luna-0 workflow task
  assumptions:
    - owner-supplied Luna-11 verification state is the current authorization premise
    - current uncommitted visualization implementation artifacts are pre-existing worktree changes and were not modified by Luna-0
  unresolved: []
  recommended_next_agent:
    - Luna-13 GPU-Compatible Visualization Path and Luna-14 ModelSim/FPGA Trace Bridge and DE1-SoC Visualization Foundation
```

## Outcome and owned scope

Luna-12: PASSED. The CPU reference implementation and TPCV-1 contract meet the
completion gate. The two strict-xfail markers were stale metadata around
already-fixed Luna-7 behavior; their assertions were retained and the markers
were removed. Luna-13: AUTHORIZED. Luna-14: AUTHORIZED. Luna-14 is independent
of Luna-13 and does not wait for its completion. Luna-15, Luna-16, and Luna-17
are not authorized by this review.

The workflow now defines a distinct downstream-only observability track after Luna-11:

- Luna-12 defines the canonical visualization contract and CPU reference exporter/parser.
- Luna-13 produces GPU-compatible records using the Luna-12 format.
- Luna-14 bridges the format into ModelSim/FPGA diagnostics and the Terasic DE1-SoC foundation.

The workflow contains the required one-way path from TPCN core to diagnostic snapshot/trace, CPU/GPU exporters, ModelSim/FPGA traces, VGA, and Ethernet host visualization. No visualization component may return data to the TPCN computational datapath.

The former FPGA/VHDL, FPAA, and hardware-equivalence milestones were renumbered from Luna-12/Luna-13/Luna-14 to Luna-15/Luna-16/Luna-17 to resolve the visualization milestone collision. No other existing non-visualization milestone was renumbered.

## Authority and authorization record

The owner-supplied Luna-11 state is authoritative for this workflow change: the adversarial suite passed 10 checks, focused reward/replay/bounded/label checks passed 5 checks, full regression passed 89 checks, compilation passed, diagnostics reported no errors, and `git diff --check` passed. The existing stale Luna-11 handoff was preserved and does not reopen Luna-11 or block Luna-12.

Current authorization:

- Luna-12: PASSED.
- Luna-13: AUTHORIZED for the GPU-compatible visualization path.
- Luna-14: AUTHORIZED independently for the ModelSim/FPGA diagnostic bridge and DE1-SoC visualization foundation; Luna-13 is optional.
- Luna-15, Luna-16, and Luna-17: not authorized by this review.

Luna-9 and Luna-10 authorization boundaries remain unchanged. No ACP is required because this adds workflow observability infrastructure without changing canonical computation.

## Validation record

| Command or procedure | Revision / environment | Observed result |
|---|---|---|
| Read authoritative contract, changelog, acceptance criteria, proposal docs, workflow, and handoff template | `1cf4065`, Windows PowerShell | completed |
| Inspect current branch, status, and recent history | `main`, `1cf4065`, dirty worktree | completed; unrelated changes preserved |
| Check milestone heading uniqueness | current worktree | pass: one definition each for Luna-12/13/14 and Luna-15/16/17 |
| Check TPCV-1 deterministic, bounded, downstream-only behavior | current worktree | pass: focused format, malformed-input, bounds, and capture-on/off invariance tests |
| `git diff --check` | current worktree | pass |
| Repository workflow lint | current worktree | not run; no documented command found |

## Next assignment

The next authorized milestones are Luna-13 and Luna-14. Luna-13 owns the GPU-compatible visualization path. Luna-14 independently owns the ModelSim/FPGA diagnostic bridge and DE1-SoC visualization foundation; it does not wait for Luna-13. Luna-15, Luna-16, and Luna-17 remain future, separately gated milestones.
