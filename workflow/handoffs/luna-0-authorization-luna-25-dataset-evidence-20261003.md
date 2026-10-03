# Luna-0 Authorization Handoff — Luna-25 Dataset Evidence

```yaml
tpcn_handoff:
  agent: "Luna-0"
  luna_identifier: "Luna-25"
  descriptive_name: "ACP-0006 sequential dataset evidence reproducibility"
  task_id: "luna-25-uci-character-trajectories-reproducible-evidence-20261003"
  component: "UCI Character Trajectories CPU benchmark input, split and report"
  status: "authorized; not executed"
  contract_version: "1.1"
  branch: "main"
  base_revision: "1642b991f82403140d0f29b5a2ff10b3d2628cda"
  result_revision: "not executed"
  dependencies:
    - "Accepted ACP-0006"
    - "Luna-22 first CPU integration"
    - "Luna-0 independent closure of Luna-24"
    - "Luna-0 second independent review of Luna-22"
  owner: "Project owner / Luna-0 Architecture Guardian"
  classification: ["DATASET-ADAPTER IMPLEMENTATION", "BENCHMARK VERIFICATION"]
  hypothesis: "A retained deterministic loader/split/report can reproduce or replace the reported UCI subset with label-isolated sequential execution and complete per-class evidence."
  counter_hypothesis: "The source or adapter cannot produce a validated, causal, repeatable integrated dataset run without changing core semantics."
  interfaces_relied_on:
    - "UCI Character Trajectories dataset DOI 10.24432/C58G7V"
    - "Existing sequential dataset inputs and ACP-0006 EXCURSION_V1 experiment path"
  label_information_boundary:
    - "Labels are permitted only for declared outer train/evaluation orchestration."
    - "No label or future point may enter neural events, topology, prediction or credit inputs."
  timing_assumptions:
    - "Trajectory points are admitted in source temporal order using existing logical-time semantics."
  reset_boundaries:
    - "Train, validation and test partitions use fresh state; no implicit state crosses splits."
  resource_bounds:
    - "Reuse declared finite event, queue, settling, prediction and activity limits; report incompleteness."
  authorized_scope:
    - "New standalone loader/benchmark script, focused tests, non-raw-data run manifest/report and completion handoff."
  unauthorized_scope:
    - "Reusable neural/runtime/core changes, experiment semantic changes, downstream consumer migration, dataset raw-data commits or Luna-22 closure."
  controls:
    - "Two fresh deterministic runs on the exact same split and configuration."
    - "Stable class/sample manifest and verified label/future-point isolation."
  measurements:
    - "Dataset identity/hash, usable example/class counts, split counts and identities, per-class results, prediction/error/credit outcomes, activity, settling, topology and energy-proxy components."
  information_boundary_check:
    - "Audit dataset adapter call sites and demonstrate labels/future samples are excluded from neural event input."
  hardware_mapping:
    - "CPU software-reference benchmark only; no hardware-equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A06", "A07", "A08", "A09", "A10", "A11", "A15"]
  preserves:
    - "Accepted ACP-0006 and A01-A15."
    - "Existing `EXCURSION_V1` computation, schema and downstream consumer boundaries."
  architecture_change: false
  proposal: null
  files_changed:
    - ".github/agents/luna-25.agent.md"
    - "workflow/handoffs/luna-0-authorization-luna-25-dataset-evidence-20261003.md"
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "All loader, parser, benchmark and experiment execution; Luna-25 has not executed."
  assumptions:
    - "If the old split cannot be reconstructed, an explicitly versioned replacement can provide new dataset evidence but cannot be described as a reproduction of the prior result."
  unresolved:
    - "Dataset reproducibility/per-class gate remains open until an independently reviewed completion handoff."
    - "The 24 downstream failures require separate consumer-specific compatibility decisions."
  recommended_next_agent:
    - "Luna-25 to execute only the authorized dataset-evidence task, then return to Luna-0."
```

## Authorization

Luna-0 authorizes the bounded task in
[`.github/agents/luna-25.agent.md`](../../.github/agents/luna-25.agent.md)
from base revision `1642b991f82403140d0f29b5a2ff10b3d2628cda`.

The reported historical UCI subset lacks a retained exact loader/split
procedure and per-class table. Luna-25 must first test whether the prior split
is reconstructable from retained evidence. If it is not, it may produce a
clearly versioned deterministic replacement run; it must not claim that the
new split reproduces the old reported result.

This authorization is deliberately separate from downstream compatibility
work. No visualization, structural-plasticity, legacy-observable, spiral,
temporal-analysis or viewer migration is authorized. Luna-25 returns all
evidence to Luna-0 and does not close Luna-22.
