# TPCN Luna Workflow

Documentation package for the event-driven TPCN candidate architecture, based on the project conversation “Create TPCN Workflow” (6ab8027c-d158-83ea-a527-d72af7052855) and the owner's current decisions. Prepared 2026-09-26.

## Read in this order

1. [Authoritative architecture contract](ARCHITECTURE_CONTRACT.md)
2. [Luna multi-agent workflow](docs/luna/LUNA_WORKFLOW.md)
3. [Acceptance criteria and benchmark protocol](docs/architecture/ACCEPTANCE_CRITERIA.md)
4. [Architecture change process](docs/architecture_proposals/README.md) and [ACP template](docs/architecture_proposals/ACP-TEMPLATE.md)
5. [Agent handoff template](docs/luna/AGENT_HANDOFF_TEMPLATE.md)
6. [Architecture changelog](ARCHITECTURE_CHANGELOG.md)

## Visualization / observability milestones

The [workflow milestone family](docs/luna/LUNA_WORKFLOW.md#visualization--observability-milestone-family) adds Luna-12 (canonical contract and CPU exporter), Luna-13 (GPU-compatible exporter), and Luna-14 (ModelSim/FPGA trace bridge and DE1-SoC foundation). Visualization is downstream-only, non-semantic infrastructure and must not affect computation or change the normative TPCN architecture; its checks are in the [acceptance criteria](docs/architecture/ACCEPTANCE_CRITERIA.md#visualization--observability-gate). The canonical Luna-12 format is documented in [VISUALIZATION_CONTRACT.md](docs/luna/VISUALIZATION_CONTRACT.md).

## Package layout

```text
tpcn-luna-workflow/
  README.md
  ARCHITECTURE_CONTRACT.md
  ARCHITECTURE_CHANGELOG.md
  docs/
    architecture/
      ACCEPTANCE_CRITERIA.md
    architecture_proposals/
      README.md
      ACP-TEMPLATE.md
    luna/
      LUNA_WORKFLOW.md
      AGENT_HANDOFF_TEMPLATE.md
      handoffs/
        README.md
```

Extract the ZIP into C:\Users\zathp\Documents\programming\TPCN. It creates the self-contained tpcn-luna-workflow folder. All documentation paths in this package, including the workflow's proposal and contract paths, are relative to that folder unless explicitly identified as implementation-repository paths.

## Start an implementation assignment

Give the worker the contract, workflow, current repository instructions, a specific Luna role, owned files and acceptance checks. Require a completed handoff. Establish the event interface first; follow the workflow's dependency order. Preserve the old implementation as the research baseline.

The folder supplies documentation only. It does not create Git branches, launch agents, install models, alter implementation code, select a dataset or claim that benchmark or hardware tests have passed. “Luna” names the coordinated roles from the source workflow; execution/model selection is a separate runtime choice.

Open decisions include the exact dataset/version and split, event tie handling and time units, credit attribution, utility formula, resource capacities beyond the initial examples, and hardware tolerances. Record these before their dependent implementation or experiments.

