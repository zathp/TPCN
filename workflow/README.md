# TPCN Luna Workflow

## Current architecture review

ACP-0003, **Heterogeneous Execution and Backend Separation**, is under review.
It proposes a canonical execution IR and explicit GPU/FPGA/FPAA approximation
contracts without changing A01-A15. It does not authorize production backend
code or hardware validation. See [ACP-0003](docs/architecture_proposals/ACP-0003.md)
and the [Luna-0 handoff](handoffs/luna-0-architecture-update-ACP-0003.md).

Documentation package for the event-driven TPCN candidate architecture, based on the project conversation “Create TPCN Workflow” (6ab8027c-d158-83ea-a527-d72af7052855) and the owner's current decisions. Prepared 2026-09-26.

## Read in this order

1. [Authoritative architecture contract](ARCHITECTURE_CONTRACT.md)
2. [Luna multi-agent workflow](docs/luna/LUNA_WORKFLOW.md)
3. [Acceptance criteria and benchmark protocol](docs/architecture/ACCEPTANCE_CRITERIA.md)
4. [Architecture change process](docs/architecture_proposals/README.md) and [ACP template](docs/architecture_proposals/ACP-TEMPLATE.md)
5. [Agent handoff template](docs/luna/AGENT_HANDOFF_TEMPLATE.md)
6. [Architecture changelog](ARCHITECTURE_CHANGELOG.md)

## Visualization / observability and post-12H milestones

The [workflow milestone family](docs/luna/LUNA_WORKFLOW.md#visualization--observability-milestone-family) adds Luna-12 (canonical contract and CPU exporter), Luna-12A through Luna-12H (CPU/replay, topology, readout, spiral and intrinsic temporal milestones), Luna-12I (temporal-associative structural growth and fan-in formation), Luna-12J (temporal-associative efficacy and causal verification), [Luna-12K](docs/luna/LUNA_12K_CAPACITY_PRESSURE_PATH_SHORTENING.md) (capacity pressure, equal exposure and path shortening), [Luna-12L](docs/luna/LUNA_12L_ENERGY_PREDICTION_FOUR_CLASS_SCALE.md) (energy/prediction tradeoff and four-class temporal scale verification), [Luna-12M](docs/luna/LUNA_12M_EDGE_LIFECYCLE_ROUTE_UTILIZATION.md) (edge lifecycle and route utilization instrumentation), and [Luna-12N](docs/luna/LUNA_12N_TEMPORAL_DIRECTION_DECAY_SHORTCUTS.md) (temporal direction and intrinsic-decay-gated shortcut verification). Luna-12M is downstream-only and Luna-12N is creation-only until explicit execution authorization; neither promotes A14 or authorizes a successor. Luna-13A is the CPU-only Stage-0 software-reference invariant-closure milestone and requires a later independent Luna-0 review before any next Luna is considered. Luna-13, Luna-14, Luna-15, Luna-16 and Luna-17 remain separately gated. Visualization remains downstream-only, non-semantic infrastructure, and the canonical Luna-12 format is documented in [VISUALIZATION_CONTRACT.md](docs/luna/VISUALIZATION_CONTRACT.md).

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

## CPU training and replay smoke test

From the implementation repository root, run:

```text
python train_cpu_visualization.py --epochs 3 --seed 7 --examples-per-class 1 --snapshot-every 1 --output-dir artifacts/cpu-tpcv
python train_cpu_visualization.py --replay artifacts/cpu-tpcv
python viz_tpcn_3d.py artifacts/cpu-tpcv --inspect-only
python viz_tpcn_3d.py artifacts/cpu-tpcv
```

This uses only the deterministic Luna-9 synthetic A/Z workload. The first
command writes bounded TPCV-1 records and a metrics timeline; the second loads
them without running training. The third command validates a replay without a
graphics context; the fourth opens the Luna-12C pygame/PyOpenGL viewer.
Structural plasticity remains deferred for this CPU smoke example, and no
real-dataset benchmark is implied.

Open decisions include the exact dataset/version and split, event tie handling and time units, credit attribution, utility formula, resource capacities beyond the initial examples, and hardware tolerances. Record these before their dependent implementation or experiments.

