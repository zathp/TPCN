# Luna agent handoff

Copy to handoffs/<task-id>-Luna-X.md. Replace placeholders; use “not run” for checks not executed.

```yaml
tpcn_handoff:
  agent: Luna-X
  task_id: "<task-id>"
  component: "<component>"
  status: "<complete|blocked|partial>"
  contract_version: "1.0"
  branch: "<branch>"
  base_revision: "<revision>"
  result_revision: "<revision or uncommitted>"
  architecture_invariants_touched: []
  preserves: []
  architecture_change: false
  proposal: null
  files_changed: []
  tests_added: []
  tests_passing: []
  tests_failed: []
  tests_not_run: []
  assumptions: []
  unresolved: []
  recommended_next_agent: []
```

## Outcome and owned scope

State what changed and why. List exact files and interfaces, including any shared ownership.

## Architecture evidence

Map touched A01–A15 clauses to evidence. Identify experimental departures and their ACP/status. Do not characterize optional gates as required invariants.

## Validation record

| Command or procedure | Revision / environment / seed | Observed result | Evidence |
|---|---|---|---|
| <actual command, or planned/not run> | <details> | <pass/fail/not run> | <log/artifact> |

## Benchmark and resource results

Record dataset/version/split, configuration, time units, classification and prediction metrics, event and activation counts, local energy proxy and units, utility definition, connectivity utilization, latency and capacity behavior. Mark non-applicable items explicitly.

## Assumptions, limitations and unresolved issues

Distinguish measured results from estimates. Identify decisions needed and responsible role.

## Reproduction and rollback

Give exact reproduction steps and a safe restoration point; preserve unrelated work.

## Next assignment

Name the next role, inputs it needs, remaining checks and whether integration is ready or blocked.

