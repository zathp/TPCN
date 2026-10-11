# Luna-0 Integrated Independent Review — Luna-64 Supervisor Amendment A2

**Amendment:** `L64-TB-R4.3-CORRECTIVE-SUPERVISOR-A2`
**Review outcome:** **BLOCKED — RESOURCE SUPERVISION UNRESOLVED**
**Review scope:** Governance-only review and static evidence reconciliation. No supervisor, qualification case, corrective test, implementation, benchmark, or scientific workload was executed.

## Reviewed identities

| Artifact | SHA-256 |
|---|---|
| A2 proposal | `E00B75004D3085EFDA60D7163D57153F2FCB2D089162574358794BBA54145591` |
| A2 resource-policy JSON | `A448646B7B38DE1BE09DC693C20C00DDDEF7C731216C1BE1BD1C462437654E12` |
| A2 resource-policy JSON Schema | `FFAECD55A7BAEA79BF2635AEDC1DE0B0AD62910AB17051308015C85BCF7ADC44` |
| Parent corrective gate | `L64-TB-R4.3-CORRECTIVE-20261010`, SHA-256 `8EE37445B1F3DAC9F085D7BE00C9FA4B11CC5FAB62779F8A424746A9BAFDE369` |
| A1 publication | `d20aab249e42575ccc571c9c72153a3bb4b412db` |
| Corrective implementation baseline | `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787` |
| Original pilot closure | `515dde66f37ca67c44a39f02e13f2e59b2f10d1d` |

The original pilot verdict remains **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**, not a scientific efficacy result. The original pilot budget remains exhausted. The corrective implementation budget remains distinct and unused.

## Independent review outcomes

Three independent read-only reviews examined the A2 proposal and its exact policy/schema revisions from Windows enforcement, governance/resource-accounting, and scientific-isolation perspectives. All returned **BLOCKED — RESOURCE SUPERVISION UNRESOLVED**.

### Windows enforcement

- The 512 MiB `JOB_OBJECT_LIMIT_JOB_MEMORY` candidate is a native job-wide committed-memory ceiling, not an aggregate peak working-set ceiling. It is neither selected nor authorized and cannot be described as proof that the original working-set requirement is met.
- There is no verified, already-authorized outer boundary constraining the trusted launcher while it creates/configures the inner Job Object and starts the child. A measured bootstrap maximum is telemetry, not enforcement.
- Job membership, breakaway controls, nested-job handling, and descendant containment after assignment do not close the pre-assignment/bootstrap gap.
- Job notifications and completion-port messages are asynchronous/advisory; they do not form a fail-closed pre-allocation memory barrier or guarantee termination at a threshold.
- Strict aggregate user-plus-kernel CPU-time enforcement remains unresolved. Wall-time and artifact-cap enforcement also remain unqualified.

### Governance and resource accounting

- The A2 policy correctly selects Option D (remain blocked), leaves `selected_memory_policy` null, and records owner approval, qualification, corrective execution, and scientific rerun as unauthorized.
- The parent allowances remain one supervisor invocation and three exact focused tests, with zero retries; their states remain unused. The separate proposed qualification allowance is not approved.
- The corrective and qualification one-shot markers are absent. The corrective worktree is clean at the authorized implementation baseline.
- The tightened schema pins the blocked/unauthorized state, baseline budgets, CPU status, qualification marker, and qualification cases. The independent reviewer checked the schema by inspection rather than running a validator. A local one-off evaluator applied the schema constraints used by the current policy (`type`, `const`, `required`, `properties`, `additionalProperties`, `items`, array bounds/uniqueness, `allOf`, and `oneOf`) and passed. This was not a full JSON Schema conformance validation.

### Scientific isolation

- The proposed amendment changes resource-governance framing only; it does not modify the frozen scientific protocol, reward lifecycle, arm definitions, implementation, tests, benchmark generators, acceptance criteria, or original pilot evidence.
- No production/core, ACP, or Luna-63C content is modified.
- No unauthorized implementation, focused test, supervisor qualification, or scientific execution occurred.

## Reconciled state and validation

- The exact proposal, policy, and schema hashes above were confirmed.
- The corrective worktree is clean at `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`; the corrective supervisor and evidence directory are absent.
- The parent corrective marker and A2 qualification marker are absent.
- Policy and schema JSON parsing and the bounded local policy/schema constraint evaluation passed. `git diff --check` passed.
- No standalone, third-party JSON Schema conformance tool was used. No Windows supervisor behavior was tested; no process-tree, memory, affinity, CPU-time, wall-time, or artifact-cap enforcement is claimed as validated.

## Verdict and authorization boundary

**BLOCKED — RESOURCE SUPERVISION UNRESOLVED**

Option D is the only defensible current disposition. The original aggregate working-set requirement remains unmet; no alternative metric is approved. The absence of a pre-established outer boundary and unresolved strict CPU, wall-time, and artifact-cap enforcement prevent a fail-closed execution authorization.

This review is not owner approval. The A2 publication records a blocked governance proposal only. It does not authorize supervisor qualification, corrective implementation, consumption of the unused focused-test allowance, or another scientific pilot. The parent authorization does not extend to a changed resource-accounting definition. No successor pilot, full-scale Track B run, production integration, or architecture promotion is authorized.

## Remaining blockers

1. Establish and independently verify an authorized outer resource boundary that contains the trusted launcher before any inner-job setup or child execution.
2. Resolve the original aggregate peak working-set requirement, or obtain explicit owner approval of a technically enforceable alternative without representing it as equivalent.
3. Demonstrate enforceable strict aggregate user-plus-kernel CPU, wall-time, and artifact-size limits under a separately approved qualification boundary.
4. Obtain explicit owner approval of any final amended resource policy before implementation or any qualification invocation.

Until all applicable blockers are resolved and authorized, preserve the original pilot evidence and verdict, leave the one-shot allowances unused, and keep corrective execution and scientific rerun authorization disabled.
